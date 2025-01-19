import cv2
import re
import pytesseract
import json
import openai
import os
import numpy as np
from pytesseract import Output
from pyzbar.pyzbar import decode
from datetime import datetime, timedelta

# OpenAI API anahtarını ekliyoruz
openai.api_key = 'YOUR_API_KEY'  # API Anahtarınızı buraya ekleyin

# QR kodlarından gelen veriyi temizlemek için fonksiyon
def veri_temizle(qr_verisi):
    qr_verisi = qr_verisi.lower()  # Veriyi küçük harfe çeviriyoruz
    qr_verisi = qr_verisi.replace("b", "₺")  # 'B' harfini TL sembolüyle değiştiriyoruz
    
    # Ürün ve fiyatları ayırıyoruz, sadece geçerli ürünler ve fiyatlar kalacak
    temizlenmis_veri = re.findall(r'([a-zA-Z\s]+)\s*(\d+[\.,]?\d*)', qr_verisi)
    
    # Geçersiz satırları kaldırıyoruz, sadece ürün adı ve fiyatı olanları tutuyoruz
    temizlenmis_veri = [
        (kelime.strip(), float(sayi.replace(',', '.')))
        for kelime, sayi in temizlenmis_veri
        if len(kelime.strip()) > 1  # 'AD' gibi gereksiz ifadeleri engelliyoruz
    ]
    return temizlenmis_veri

# Görüntüyü işleme ve gürültüyü azaltma fonksiyonu
def goruntu_isle(goruntu):
    cekirdek = np.ones((5,5), np.uint8)  # Açma işlemi için çekirdek
    acma_islemi = cv2.morphologyEx(goruntu, cv2.MORPH_OPEN, cekirdek)  # Açma işlemi uyguluyoruz
    return acma_islemi  # İşlenmiş görüntüyü döndürüyoruz

def metin_uzerine_kutular_ciz(goruntu, metin_kutulari):
    for kutu in metin_kutulari:
        # OCR tarafından çıkarılan her metin kutusunu çiziyoruz
        x, y, genislik, yukseklik = kutu
        cv2.rectangle(goruntu, (x, y), (x + genislik, y + yukseklik), (0, 255, 0), 2)  # Yeşil kutu
    return goruntu

# Görüntü üzerinde OCR işlemi yaparak metin çıkaran fonksiyon
def metin_ve_kutulari_cikar(goruntu):
    ozel_ayarlar = r'--oem 3 --psm 6'
    detaylar = pytesseract.image_to_data(goruntu, output_type=Output.DICT, config=ozel_ayarlar, lang='tur')

    # Metin kutularını çizmek için, OCR sonuçları üzerinden kutu koordinatlarını çıkarıyoruz
    kutular = []
    for i, kelime in enumerate(detaylar['text']):
        if kelime.strip():
            (x, y, genislik, yukseklik) = (detaylar['left'][i], detaylar['top'][i], detaylar['width'][i], detaylar['height'][i])
            kutular.append((x, y, genislik, yukseklik))

    return kutular, detaylar['text']

# OpenAI GPT ile veri yorumlama fonksiyonu
def gpt_yorumla(veri):
    yanit = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "json dosyasındaki veriyi sadece ürün adı ve fiyatı olacak şekilde ekranda göster geri kalan hiçbir şeyi ekranda gösterme (ürün: fiyat). json dosyasındaki tarihlere bakarak günlük ne kadar harcadıklarını ekranda göster ve aynı gün yapılan harcamaları toplayarak günlük harcamayı yaz. Yapılan harcama ile ilgili 10 kelimelik öneride bulun."},
                  {"role": "user", "content": f"Veri: {veri}"}]
    )
    return yanit['choices'][0]['message']['content']

json_dosyasi = 'veri.json'

def json_kaydet(veri, tarih=None, dosya_adi="veri.json"):
    kaydedilecek_veri = {"veri": veri}  # Veriyi kaydedeceğiz

    if tarih:
        kaydedilecek_veri["tarih"] = tarih.strftime('%d/%m/%Y')  # Tarihi 'GG/AA/YYYY' formatında kaydediyoruz
    
    # Dosya yoksa oluştur, yoksa içine ekle
    if not os.path.exists(dosya_adi):
        with open(dosya_adi, "w") as json_dosya:
            json.dump([kaydedilecek_veri], json_dosya, ensure_ascii=False, indent=4)
    else:
        with open(dosya_adi, "r+") as json_dosya:
            try:
                mevcut_veri = json.load(json_dosya)
            except json.JSONDecodeError:
                mevcut_veri = []  # Dosya boşsa, mevcut veriyi boş bir listeyle başlat
            mevcut_veri.append(kaydedilecek_veri)
            json_dosya.seek(0)  # Dosyanın başına dön
            json.dump(mevcut_veri, json_dosya, ensure_ascii=False, indent=4)

# Yeni birleşmiş fonksiyon
def harcamalari_yazdir_ve_topla(temizlenmis_veri):
    toplam = 0
    for i, (urun, fiyat) in enumerate(temizlenmis_veri, 1):
        print(f"{i}. {urun.capitalize()} (x1 adet) - {fiyat:.2f} TL")
        toplam += fiyat  # Fiyatları topluyoruz
    print(f"Toplam Harcama: {toplam:.2f} TL")

# JSON dosyasını okuma işlemi
def gruplara_ayir_ve_topla(json_dosyasi):  # Parametreyi ekledik
    try:
        with open(json_dosyasi, 'r') as dosya:  # json_dosyasi değişkenini burada kullanıyoruz
            veriler = json.load(dosya)  # Dosyadaki veriyi yüklüyoruz
            # Burada json verilerini işlemeye devam edebilirsiniz
            gunluk = sum(item['tutar'] for item in veriler if item['tarih'] == 'günlük')
            haftalik = sum(item['tutar'] for item in veriler if item['tarih'] == 'haftalık')
            aylik = sum(item['tutar'] for item in veriler if item['tarih'] == 'aylık')
            return gunluk, haftalik, aylik
    except FileNotFoundError:
        print(f"{json_dosyasi} dosyası bulunamadı!")
    except json.JSONDecodeError as e:
        print(f"JSON okuma hatası: {e}")

# Kamerayı başlatıyoruz
ip_adresi = 'http://192.168.1.24:8080/video'  # IP webcam adresi
kamera = cv2.VideoCapture(ip_adresi)

okunan_qr_veriler = []  # QR kodlarından okunan verileri depolamak için liste
okunan_qr = ""  # Okunan son QR kodu verisi

foto_don = False  # Fotoğraf alma durumu

while True:
    ret, kare = kamera.read()
    if not ret:
        break

    # Görüntüyü ön işleme
    islenmis_kare = goruntu_isle(kare)

    # QR kodlarını çözme
    qr_kodlari = decode(islenmis_kare)  # QR kodlarını çöz

    if qr_kodlari:  # Eğer QR kodları varsa
        for qr_kod in qr_kodlari:  # Her QR kodunu tek tek işliyoruz
            qr_verisi = qr_kod.data.decode('utf-8')  # QR kodunun verisini alıyoruz
            
            if qr_verisi != okunan_qr:  # Eğer yeni bir QR kodu okunduysa
                okunan_qr = qr_verisi  # QR kodunu kaydediyoruz
                temiz_veriler = veri_temizle(qr_verisi)  # QR verisini temizleyip düzenli hale getiriyoruz
                # Tarihi kontrol et
                tarih = datetime.now()  # Örnek tarih, QR'den alınan tarihe göre değiştirebilirsiniz

                json_kaydet(temiz_veriler, tarih=tarih)

                # GPT'ye gönderiyoruz ve yanıt alıyoruz
                gpt_yanit = gpt_yorumla(temiz_veriler)
                print(gpt_yanit)  # GPT'nin yorumunu yazdırıyoruz

            break  # Döngüyü kırıyoruz, bir QR kodu okunduktan sonra diğerini kontrol etmiyoruz

    if foto_don:
        cv2.putText(kare, "Fotoğraf Alindi!", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        foto_don = False  # Fotoğraf mesajını sadece bir kez gösteriyoruz

    # Görüntü sürekli yenileniyor
    cv2.imshow('QR Kodları veya Fiş/Fatura (Ekran Kaydı İçin "S" Tuşuna Basın):', kare)

    tus = cv2.waitKey(1) & 0xFF  # Kullanıcı tuş basışını bekliyoruz
    if tus == ord('s'):  # "S" tuşuna basıldığında
        islenmis_goruntu = goruntu_isle(kare)  # Görüntüyü işliyoruz
        cv2.imshow("İşlenmiş Görüntü:", islenmis_goruntu)  # İşlenmiş görüntüyü ekranda gösteriyoruz

        metin_kutulari, metin = metin_ve_kutulari_cikar(islenmis_goruntu)  # OCR ile metni çıkarıyoruz

        # Metin kutularını çiziyoruz
        kutulu_islenmis_goruntu = metin_uzerine_kutular_ciz(islenmis_goruntu, metin_kutulari)

        cv2.imshow("Metin Kutularıyla Görüntü:", kutulu_islenmis_goruntu)  # Metin kutuları ile birlikte görüntüyü gösteriyoruz

        if any(kelime.strip() for kelime in metin):  # Eğer liste içindeki herhangi bir kelime boş değilse
            json_kaydet({"type": "OCR", "data": metin}, tarih=datetime.now())

            # GPT'ye gönderiyoruz ve yanıt alıyoruz
            gpt_yanit = gpt_yorumla(' '.join(metin))
            print(gpt_yanit)  # GPT'nin yorumunu yazdırıyoruz
        else:
            print("Fiş/Fatura Okunamadı, Lütfen Daha Net Gösterin!")  # Eğer metin okunmazsa uyarı veriyoruz

    elif tus == ord('q'):  # "Q" tuşuna basıldığında döngüyü sonlandırıyoruz
        break

kamera.release()
cv2.destroyAllWindows()
