"""Yandex Translate Api Python Flask
Erdem Demirtaş
demirtaserdem@gmail.com
https://github.com/demirtaserdem/yandex-translate-api-python-flask
https://app1.erdemdemirtas.net
2019.01
"""
"""Bootstrap v4.2.1
ve Jinja Template Kullanularak Hazırlanmıştır. 
"""

"""'requests' yandex translate apiye request göndermek için eklenmiştir
'os' dosya boyutu kontrol etmek için eklenmiştir
'json' dict.txt'yi post-redirect-get PRG yapmak için kullanılmuştır. 
"""
from flask import Flask,render_template,request,redirect,url_for
import requests
import os
import json
#Flask Uygulması Oluşturuldu
app = Flask(__name__)
#Kullanımda Gerekli Dosyalar Oluşturuldu.
open("dict.txt","w").close()
open("last_searchs.txt","w").close()

#Anasayfa
@app.route("/")
def index():
    """Anasayfa Fonksiyonu
    """
    #Veriyi dict() objesi ya da 'None'  olarak alır. 
    translateInfo = read_dict()
    #index.html i render eder jinja bilgileri doner.
    return render_template("index.html",info = translateInfo)


@app.route("/translate",methods = ["GET","POST"])
def translate():
    """Post Requestle Çevir Fonksiyonu
    """
    if request.method == "POST":
        #Post Requestten gelen formdan kelimeyi alır temizlerç
        input_word_req = request.form.get("input_word")
        input_word = input_word_req.lower().strip()
        #Boşluklarla olan post kontrolü
        if input_word:
            #Url Oluşturulur
            url = create_url(input_word)
            #Yandex Api'ye request gönderilip kelime alınır.
            output_word = translateFunc(url)
            #Son Aranan dosyasına yazma işlemi yapılır.
            writeLastSearch(input_word,output_word)
            #Bilgi sözlüğü oluşturulur
            translateInfo = dict()
            #Aranan Kelime
            translateInfo["input_word"] = input_word
            #Çeviri
            translateInfo["output_word"] = output_word
            #Son Arananlar listesi 
            translateInfo["last_search"] = printLastSearch()
            #geçici dict.txt dosyasına bilgiler yazılır json olarak.
            write_dict(translateInfo)           
    return redirect(url_for("index"))

@app.route("/last_search_clean")
    """Son Arananları Temizleme Foksiyonu
    """
def last_search_clean():
    clean_Last_Searched()
    clean_dict()
    return redirect(url_for("index"))

def read_dict():
    """dict.txt deki geçici bilgileri okur.
    json bilgiyi dict e çevirir döndürür. Dosya boşsa None Döndürür.
    """
    if os.stat("dict.txt").st_size != 0:
        with open("dict.txt","r",encoding ="utf-8") as file:
           json_data =  file.read()
        return json.loads(json_data)
    else:
        return None

def clean_dict():
    """Geçici Bilgileri Temizleme Fonksiyonu
    """
    open("dict.txt","w").close()

def write_dict(translateInfo):
    """Geçici bilgileri dict to json yaparak "dict.txt"'ye yazar
    """
    with open("dict.txt","w",encoding = "utf-8") as file:
        file.write(json.dumps(translateInfo))

def create_url(input_word):
    """Yandex Api İçin Url Oluştutur Döner
    """
    #Yandex Apide Çeviri Url İsteğni oluşturmak için kısımlara ayrıldı.
    #https://tech.yandex.com/translate/doc/dg/reference/
    #translate-docpage/JSON
    #temel alınarak oluşturulmuştur.
    #Url'nin ilk değişmeeyen kısmı
    base_url ="https://translate.yandex.net/api/v1.5/tr.json/translate"
    # Api key yandex translate tarafından alınacak.
    # "https://translate.yandex.com/developers/keys"
    key = ("?key=trnsl.1.1.20190121T100542Z.4befbb4bba198843."
        +"b6081dd6370342a5c61258dbb83fb7b9a58dd523")
    #arama yapacağımız kelime - metindir. ilk url oluşturulurken 
    #"Merhaba" yazılmıştır, text = Str() oluşturulabilir.
    text = input_word
    #url'nin devamı kullanılan bir sabit
    base_text = "&text="
    #Çevirilmesi istenen dil değişkeni
    lang = "en" 
    #tr- kısmı çevrinmesi istenen dilin otomatik algılamasını kapatıp
    #türkçeden çeviri yapılmasını sağlıyor. örn. "&lang=tr-eng" ya da
    # otomatik: "&lang=eng" olarak yazılabilir.
    base_lang = "&lang=tr-"
    #oluşan temel url
    translate_url = (base_url + key+base_lang + lang + base_text
        + text)  
    return translate_url

def translateFunc(url):
    """Oluşturulan url'ye istek gönderir, alır, json objesine çevirir
    json objesinin içinden ilgili kısmı dataya yazar. Çevriyi Str 
    olarak döndürür.
    """
    data_get = requests.get(url)
    data_json = data_get.json()
    data = data_json["text"][0]
    return data

def writeLastSearch(input_word,output_word):
    """Çevrilen ve çeviri kelimeyi str olarak alır,
    last_searchs.txt dosyasına yazar konsola yazabiliyorsa yazar, 
    """
    try:
        with open("last_searchs.txt","r+",encoding = "utf-8") as file:
            read = file.read()
            file.seek(0)
            file.write(input_word +" --->>> "+ output_word + "\n" + read)
    except:
        pass

def printLastSearch():
    """Son Arananların listesini
    last_searchs.txt den alır. yazdırır
    """
    #last_searchs.txt olmamısın durumu için hata denetimi.
    try:
        #Dosyanın Boş Olup olmadığı kontol edilmiştir
        if os.stat("last_searchs.txt").st_size == 0:
            return "Son Aranan Kelime Bulunmamaktadır."
        else:
            with open("last_searchs.txt","r",encoding = "utf-8") as file:
                return file.read()
    except:
        pass
        
def clean_Last_Searched():
    """last_searchs.txt dosyasının temizlenmesini ve oluşmasını
    sağlar
    """
    open("last_searchs.txt","w").close()
    

#if __name__ == "__main__":
#    app.run()
