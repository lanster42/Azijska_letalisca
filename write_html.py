import os
import requests
import poberi



def shrani_html(frontpage_url):
    os.makedirs("csv_datoteke", exist_ok=True)
    
    for page in range(poberi.stevilo_strani(frontpage_url) + 1):
        # Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        main_urls = f"{frontpage_url}?start={page*50}"
        
        html = requests.get(main_urls)
        
        dat_ime = os.path.join("csv_datoteke", f"html_datoteka{page + 1}.html")

        with open(dat_ime, "w", encoding="utf-8") as file:
            file.write(html.text)