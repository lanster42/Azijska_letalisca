import os
import requests
import poberi

frontpage_url = "https://ourairports.com/continents/AS/airports.html"

def shrani_html(frontpage_url):
    os.makedirs("html_datoteke", exist_ok=True)
    
    for page in range(poberi.stevilo_strani(frontpage_url) + 1):
        # Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        main_urls = f"{frontpage_url}?start={page*50}"
        potrdilo = requests.get(main_urls, verify=False)  
        dat_ime = os.path.join("html_datoteke", f"html_dat-{page + 1}.html")

        with open(dat_ime, "w", encoding="utf-8") as file:
            file.write(potrdilo.text)