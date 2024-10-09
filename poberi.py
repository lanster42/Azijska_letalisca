#####################################################################################
#importing

import os
from bs4 import BeautifulSoup
import requests

#####################################################################################

print(os.getcwd())


url = "https://ourairports.com/continents/AS/airports.html"
page = requests.get(url)
if page.status_code == 200:
    # Parsiram HTML vsebino strani
    doc = BeautifulSoup(page.content, "html.parser")


#poisci linke vseh spletnih strani
poisci_next_link = doc.find(class_="nav col-sm-12").find(class_="next").find("a")["href"]
#print(poisci_next_link)

#stevilo letalisc
st_letalisc = doc.find(class_="badge hidden-sm").string
st_strani = int(st_letalisc.replace(",", ""))//50 + 1


#Poišči ime letališča, kraj in drzavo
Slovar_letalisc = {}
ime_class = doc.find_all(class_="col-lg-6")
for letalisce in ime_class:
    ime_letalisca = letalisce.find("h3").find("a").string
    drzava = letalisce.find("p").find("b").string.strip()
    tip_letalisca = letalisce.find("img")["title"]
    Slovar_letalisc[ime_letalisca] = [drzava, tip_letalisca]
#print(Slovar_letalisc)


#poisci_ime = doc.find_all("a")[0]
#print(poisci_ime)

#NASLEDNIC:
#  flights page(title="Arrivals and departures") --> how many a day