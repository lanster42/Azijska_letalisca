#####################################################################################
#importing

from bs4 import BeautifulSoup
import requests

#####################################################################################

import os
print(os.getcwd())


url = "https://ourairports.com/airports/"
""" zahteva = requests.get(url)
if zahteva.status_code == 200:
    # Parsiramo HTML vsebino strani
    soup = BeautifulSoup(zahteva.content, 'html.parser') """




with open(r"Svetovna_letalisca\source.html", 'r', encoding='utf-8') as vhod:
    doc = BeautifulSoup(vhod, "html.parser")
#print(doc.prettify())
poisci_ime = doc.find_all("a")[0]
print(poisci_ime)

#NASLEDNIC:
#  kako lahko prebira vec strani(ne le 50 kot jih gre na stran)
#  kako cisto stripas titles