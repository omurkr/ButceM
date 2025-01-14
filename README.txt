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
    pip install opencv-python pytesseract pyzbar numpy openai==0.28
    ```

3. **Tesseract Kurulumu:**
    - Tesseract OCR'ı sisteminize kurmanız gerekmektedir. [UB Mannheim'ın Tesseract sayfasından](https://github.com/UB-Mannheim/tesseract/wiki) Tesseract yükleyicisini indirin.
    - Yükleyiciyi çalıştırın ve yükleme yolunu not edin (örneğin, `C:\Program Files\Tesseract-OCR\tesseract.exe`).
    - Sistem Ortam Değişkenlerini Düzenleye giderek yükleme yolunu sisteminizin PATH ortam değişkenine ekleyin.( Gelişmiş -> Ortam Değişkenleri -> Path )
    - Tesseract'ın optimize bir şekilde çalışması Türkçe dil dosyasını (tur.traineddata) indirin ve tessdata klasörünün içerisine atın. (https://github.com/tesseract-ocr/tessdata)
    - Eğer PATH başarılı olmazsa, .exe'nin bulunduğu klasörü PATH'e ekleyin.('C:\Program Files\Tesseract-OCR')
    - Eğer yine başarısız olursa VS Code editörünü yeniden başlatın.

4. **OpenAI API Anahtarı:**
    - OpenAI API anahtarınızı almanız gerekmektedir. [OpenAI API Anahtarı](https://beta.openai.com/signup/) Güvenlik nedeniyle paylaşılan API keyler geçerliliğini yitirmektedir.
    - Anahtarınızı [main.py](http://_vscodecontentref_/0) dosyasındaki [13.satır, openai.api_key](http://_vscodecontentref_/1) değişkenine ekleyin.

## IP Webcam Uygulaması

Bu proje, IP Webcam uygulamasını kullanarak kameradan görüntü alır. IP Webcam uygulaması, Android cihazınızı bir IP kameraya dönüştürmenizi sağlar.
Uygulamayı indirip açtığınızda size ekran üzerinde bir IP adresi tanımlayacaktır. Buradaki IP adresi, cihaz ve bağlantı tipine göre değişmektedir.
Cihazınızın ve telefonunuzun aynı ağa bağlı olması gerekmektedir.
Koddaki ilgili kısmı cihazının IP'sine göre ayarlayın. (113. satır, ip_adresi:'http://192.168.1.24:8080/video'/Örnektir)

### IP Webcam Uygulamasının İndirilmesi

IP Webcam uygulamasını Google Play Store'dan indirebilirsiniz: [IP Webcam İndir](https://play.google.com/store/apps/details?id=com.pas.webcam)

### IP Webcam Uygulamasının Projedeki Payı

IP Webcam uygulaması, Android cihazınızın kamerasını kullanarak görüntüleri bilgisayarınıza aktarır. Bu görüntüler, proje tarafından işlenir ve QR kodları veya fiş/fatura üzerindeki metinler okunur. Uygulama, kameradan alınan görüntüleri bir IP adresi üzerinden yayınlar ve bu IP adresi [main.py](http://_vscodecontentref_/2) dosyasında belirtilir. (113. Satır, ip)

## Kullanım Detayları

1. **Kamerayı Başlatma:**
    - [main.py](http://_vscodecontentref_/3) dosyasını çalıştırarak kamerayı başlatabilirsiniz.
    - QR kodları ve fiş/fatura üzerindeki metinleri kameraya gösterin.

2. **QR Kodları ve Fiş/Fatura Okuma:**
    - QR kodları üzerindeki metinler otomatik, fiş/fatura üzerindeki metinler "s" tuşuna basıldığında okunacak ve işlenecektir.
    - İşlenen veriler JSON formatında [veri.json](http://_vscodecontentref_/4) dosyasına kaydedilecektir.

3. **GPT-3.5 ile Yorumlama:**
    - OCR ile çıkarılan metinler OpenAI GPT-3.5'e gönderilecek ve yorumlanacaktır.
    - Yorumlar konsolda görüntülenecektir.

## Örnek Kullanım

```bash
python main.py
