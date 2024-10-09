#####################################################################################
#importing

import os
from bs4 import BeautifulSoup
import requests
import csv

#####################################################################################

print(os.getcwd())


url = "https://ourairports.com/continents/AS/airports.html"
page = requests.get(url)
if page.status_code == 200:
    # Parsiram HTML vsebino strani
    doc = BeautifulSoup(page.content, "html.parser")


#poisci linke vseh spletnih strani
#poisci_next_link = doc.find(class_="nav col-sm-12").find(class_="next").find("a")["href"]
#print(poisci_next_link)


#stevilo letalisc
st_letalisc = int(doc.find(class_="badge hidden-sm").string.replace(",", ""))
st_strani = st_letalisc//50 + 1
print(st_strani)

for page in range(st_strani + 1):
    #Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
    url = f"https://ourairports.com/continents/AS/airports.html?start={page*50}"
    page = requests.get(url)
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