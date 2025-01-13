# Bütçe Yönetim Sistemi

Bu proje, QR kodları ve fiş/fatura üzerindeki metinleri OCR (Optik Karakter Tanıma) teknolojisi kullanarak okuyup işleyen ve bu verileri OpenAI GPT-3.5 ile yorumlayan bir bütçe yönetim sistemidir.

## Projenin Amacı

Bu projenin amacı, kullanıcıların fiş ve faturalarını dijital olarak saklamalarını ve harcamalarını daha iyi yönetmelerini sağlamaktır. QR kodları ve OCR teknolojisi kullanılarak, fiş ve faturalar üzerindeki metinler okunur ve işlenir. OpenAI GPT-3.5 kullanılarak bu veriler yorumlanır ve kullanıcıya anlamlı bilgiler sunulur.

## Kurulum Talimatları

1. **Gereksinimler:**
    - Python 3.6 veya üstü
    - OpenCV
    - pytesseract
    - pyzbar
    - numpy
    - openai

2. **Gereksinimlerin Yüklenmesi:**
    ```bash
    pip install opencv-python pytesseract pyzbar numpy openai
    ```

3. **Tesseract Kurulumu:**
    - Tesseract OCR'ı sisteminize kurmanız gerekmektedir. [Tesseract Kurulumu](https://github.com/tesseract-ocr/tesseract)

4. **OpenAI API Anahtarı:**
    - OpenAI API anahtarınızı almanız gerekmektedir. [OpenAI API Anahtarı](https://beta.openai.com/signup/)
    - Anahtarınızı [main.py](http://_vscodecontentref_/0) dosyasındaki [openai.api_key](http://_vscodecontentref_/1) değişkenine ekleyin.

## IP Webcam Uygulaması

Bu proje, IP Webcam uygulamasını kullanarak kameradan görüntü alır. IP Webcam uygulaması, Android cihazınızı bir IP kameraya dönüştürmenizi sağlar.

### IP Webcam Uygulamasının İndirilmesi

IP Webcam uygulamasını Google Play Store'dan indirebilirsiniz: [IP Webcam İndir](https://play.google.com/store/apps/details?id=com.pas.webcam)

### IP Webcam Uygulamasının Projedeki Payı

IP Webcam uygulaması, Android cihazınızın kamerasını kullanarak görüntüleri bilgisayarınıza aktarır. Bu görüntüler, proje tarafından işlenir ve QR kodları veya fiş/fatura üzerindeki metinler okunur. Uygulama, kameradan alınan görüntüleri bir IP adresi üzerinden yayınlar ve bu IP adresi [main.py](http://_vscodecontentref_/2) dosyasında belirtilir. (113. Satır, ip)

## Kullanım Detayları

1. **Kamerayı Başlatma:**
    - [main.py](http://_vscodecontentref_/3) dosyasını çalıştırarak kamerayı başlatabilirsiniz.
    - QR kodları ve fiş/fatura üzerindeki metinleri kameraya gösterin.

2. **QR Kodları ve Fiş/Fatura Okuma:**
    - QR kodları ve fiş/fatura üzerindeki metinler otomatik olarak okunacak ve işlenecektir.
    - İşlenen veriler JSON formatında [veri.json](http://_vscodecontentref_/4) dosyasına kaydedilecektir.

3. **GPT-3.5 ile Yorumlama:**
    - OCR ile çıkarılan metinler OpenAI GPT-3.5'e gönderilecek ve yorumlanacaktır.
    - Yorumlar konsolda görüntülenecektir.

## Örnek Kullanım

```bash
python main.py