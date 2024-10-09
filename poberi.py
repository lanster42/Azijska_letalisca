#####################################################################################
#importing

import os
from bs4 import BeautifulSoup
import requests

#####################################################################################

print(os.getcwd())


url = "https://ourairports.com/continents/AS/airports.html"
result = requests.get(url)
if result.status_code == 200:
    # Parsiram HTML vsebino strani
    doc = BeautifulSoup(result.content, "html.parser")

print(doc.head)


""" with open(r"Svetovna_letalisca\source.html", 'r', encoding='utf-8') as vhod:
    doc = BeautifulSoup(vhod, "html.parser")
#print(doc.prettify())
poisci_ime = doc.find_all("a")[0]
print(poisci_ime) """

#NASLEDNIC:
#  kako lahko prebira vec strani(ne le 50 kot jih gre na stran)
#  kako cisto stripas titles
#  Ime letalisca, drzava, (flag), flights page(title="Arrivals and departures") --> how many a day