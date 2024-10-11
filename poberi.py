#####################################################################################
#importing

import os
import csv
from bs4 import BeautifulSoup
import requests

#####################################################################################

print(os.getcwd())

frontpage_url = "https://ourairports.com/continents/AS/airports.html"

def dobi_permition(url):
    page = requests.get(url, verify=False)
    if page.status_code == 200:
        # Parsiram HTML vsebino strani
        doc = BeautifulSoup(page.content, "html.parser")
        return doc
    
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
def stevilo_strani(url):
    st_letalisc = int(dobi_permition(url).find(class_="badge hidden-sm").string.replace(",", ""))
    st_strani = st_letalisc//50 + 1
    return st_strani

def pridobivanje_podatkov(url):
    for page in range(stevilo_strani(url) + 1):
        #Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        url = f"{url}start={page*50}"
        page = requests.get(url, verify=False)   #verify sem dodal, saj je strani med procesom potekel certifikat o varnosti :)
        if page.status_code == 200:
        # Parsiram HTML vsebino strani
            doc = BeautifulSoup(page.content, "html.parser")

        #Poišči ime letališča, kraj in drzavo
        Slovar_letalisc = {}
        ime_class = doc.find_all(class_="col-lg-6")
        for letalisce in ime_class:
            ime_letalisca = letalisce.find("h3").find("a").string
            drzava = letalisce.find("p").find("b").string.strip()
            tip_letalisca = letalisce.find("img")["title"]
            Slovar_letalisc[ime_letalisca] = [drzava, tip_letalisca]
        
        #Slovarje hocem zapisati v csv datoteko
        print(Slovar_letalisc)


#Zapiši podatke v csv datoteko
with open("podatki.csv", "w", encoding='utf-8') as izhodna_dat:
    keys = ["Ime letališča", "Država", "Tip letališča"]
    writer = csv.writer(izhodna_dat).writerow(keys)

#NASLEDNIC:
#  flights page(title="Arrivals and departures") --> how many a day