from flask import Flask,render_template,request,redirect,url_for
import requests
import os
import json

app = Flask(__name__)

open("dict.txt","w").close()
open("last_searchs.txt","w").close()

@app.route("/")
def index():
    translateInfo = read_dict()
    return render_template("index.html",info = translateInfo)

@app.route("/translate",methods = ["GET","POST"])
def translate():
    if request.method == "POST":
        input_word_req = request.form.get("input_word")
        input_word = input_word_req.lower().strip()
        if input_word:
            url = create_url(input_word)
            output_word = translateFunc(url)
            writeLastSearch(input_word,output_word)
            translateInfo = dict()
            translateInfo["input_word"] = input_word
            translateInfo["output_word"] = output_word
            translateInfo["last_search"] = printLastSearch()
            write_dict(translateInfo)           
    return redirect(url_for("index"))

@app.route("/last_search_clean")
def last_search_clean():
    clean_Last_Searched()
    clean_dict()
    return redirect(url_for("index"))

def clean_dict():
    open("dict.txt","w").close()

def read_dict():
    if os.stat("dict.txt").st_size != 0:
        with open("dict.txt","r",encoding ="utf-8") as file:
           json_data =  file.read()
        return json.loads(json_data)
    else:
        return None

def write_dict(translateInfo):
    with open("dict.txt","w",encoding = "utf-8") as file:
        file.write(json.dumps(translateInfo))

def create_url(input_word):
    #Yandex Apide Çeviri Url İsteğni oluşturmak için kısımlara ayrıldı.
    #"https://tech.yandex.com/translate/doc/dg/reference/
    # translate-docpage/JSON"
    #temel alınarak oluşturulmuştur.
    #Url'nin ilk değişmeeyen kısmı
    base_url ="https://translate.yandex.net/api/v1.5/tr.json/translate"
    # Api key yandex translate tarafından alınacak.
    # "https://translate.yandex.com/developers/keys"
    key = ("?key=trnsl.1.1.20190121T100542Z.4befbb4bba198843."
        +"b6081dd6370342a5c61258dbb83fb7b9a58dd523")
    #arama yapacağımız kelime - metindir. ilk url oluşturulurken 
    #"Merhaba" yazılmıştır, text = Str() oluşturulabilir.
    text = input_word.strip()
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
    utf-8 hatasından - çince vs hata olursa hata mesajı verir.
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
