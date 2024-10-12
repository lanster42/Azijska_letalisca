#####################################################################################
#importing
from bs4 import BeautifulSoup
import requests

#####################################################################################
import urllib3

urllib3.disable_warnings()  #Stran je bila varna v prvih 2 tednih dela z njo in ji je nato potekel certifikat

frontpage_url = "https://ourairports.com/continents/AS/airports.html"
stran = requests.get(frontpage_url, verify=False)
if stran.status_code == 200:
    # Parsiram HTML vsebino strani
    doc = BeautifulSoup(stran.content, "html.parser")
    
""" def save_string_to_file(text, directory, filename):
    #Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    #locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    #niz "directory" prazen datoteko ustvari v trenutni mapi.
    
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename) #dobimo polno pot 
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None """

#stevilo letalisc
def stevilo_strani():
    st_letalisc = int(doc.find(class_="badge hidden-sm").string.replace(",", ""))
    st_strani = st_letalisc//50 + 1
    return st_strani

def pridobivanje_podatkov():
    Seznam_slovarjev = []
    for page in range(stevilo_strani() + 1):
        #Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        url = f"https://ourairports.com/continents/AS/airports.html?start={page*50}"
        straan = requests.get(url, verify=False)   #verify sem dodal, saj je strani med procesom potekel certifikat o varnosti :)
        if straan.status_code == 200:
        # Parsiram HTML vsebino strani
            doc = BeautifulSoup(straan.content, "html.parser")

        #Poišči ime letališča, kraj in drzavo
        Sez_letalisc = []
        ime_class = doc.find_all(class_="col-lg-6")
        for letalisce in ime_class:
            ime_letalisca = letalisce.find("h3").find("a").string
            drzava = letalisce.find("p").find("b").string.strip()
            tip_letalisca = letalisce.find("img")["title"]
            Sez_letalisc.append({"ime letališča" : ime_letalisca, "država": drzava, "tip letališča" : tip_letalisca})
            #Slovar_letalisc[ime_letalisca] = [drzava, tip_letalisca]
        #print(Sez_letalisc)
        Seznam_slovarjev += (Sez_letalisc)
    return Seznam_slovarjev

#NASLEDNIC:
#  flights page(title="Arrivals and departures") --> how many a day