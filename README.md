# Yandex Translate API - Python - Flask 

Yandex Translate Api kullanılarak, internet bağlantısı aracılığıyla 
Türkçe - İngilizce çeviri yapan bir flask uygulamasıdır. 

 - Html sayfası oluşturulurken Bootstrap v4.2.1 kullandım.

- Python 3 ve Flask kullanılarak yazılmıştır.

Temel olarak Kullanıcının istediği kelimeyle Yandex Translate Api'ye
uygun url oluşturulmuş. Çevirisi "request" modülü kullanarak, 
Yandex Translate Api'ye get request gönderilmiştir.
Dönen bilgi json verisi verisi olarak işlenmiş flaskla birlikle jinja
kullanılarak, html sayfası render edilmiştir.

Database kullanılmamıştır. Son arananlar json verisi şeklinde 
dict.txt olarak kaydedilmiş ana fonksiyon içinde oradan okuma yapılarak 
html sayfası içerisine gönderilmiştir. 

Programın bir bölümünde kullanılan: 
- "os" modülü; oluşacak son aramalardosyasının boyutuna göre boş olup 
olmadığını kontrol için kullanılmıştır.
- "json" modülü veriyi "dict.txt" dosyasına yazılıp okunması için 
kullanılmıştır.

Program çalıştırıldığı dizinde "last_searchs.txt" isimli bir dosya oluşturur. Son arananları bu dosyaya kaydeder ve bu dosyadan 
okur. 
 
## Uygulamadan fotoğraflar

![Imgur](https://i.imgur.com/mjDEcM5.png?1) 

### Gereklilikler

Python 3 kurulu olması gerekli.

```
Python 3
```

### Yükleme

Githubdan Verileri kopyalamak için
terminalde
```
git clone https://github.com/demirtaserdem/yandex-translate-api-python-flask.git
```
Eklentileri Yüklemek için:
```
pip install -r requirements.txt
```
Lokalde çalıştırmak için
```
python wsgi.py
```

## Test İçin 
- <a href="https://app1.erdemdemirtas.net" target="_blank">Çalışan Uygulama İçin Tıklayın</a>

Uygulamayı [1]'deki dökümantasyona uyarak
aşağıdaki adreste yayınladım.
Amazon Route 53
Yayın ortamı
Amazon Ec2 - Amazon Route 53 - Ubuntu 18.04 - nginx - 
gunicorn - letsencrypt kullanılarak hazırlanmıştır.

##Kaynak
[1]: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
[2]: https://tech.yandex.com/translate/