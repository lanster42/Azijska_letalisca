#####################################################################################
#importing
from bs4 import BeautifulSoup
import requests

#####################################################################################
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings()  #Stran je bila varna v prvih 2 tednih dela z njo in ji je nato potekel certifikat

frontpage_url = "https://ourairports.com/continents/AS/airports.html"

def pridobi_potrdilo(zeljen_url):
    potrdilo = requests.get(zeljen_url, verify=False) #verify sem dodal, saj je strani med pisanjem kode potekel certifikat o varnosti :)
    if potrdilo.status_code == 200:
    #Parsiram HTML vsebino vmesne strani
        return BeautifulSoup(potrdilo.content, "html.parser")

#stevilo letalisc
def stevilo_strani(zeljen_url):
    doc = pridobi_potrdilo(zeljen_url)
    st_letalisc = int(doc.find(class_="badge hidden-sm").string.replace(",", ""))
    st_strani = st_letalisc//50 + 1
    return st_strani

def je_v_24urah(datum_str, cas_str, primerjalni_datum_str):
    # Določi trenutni letnik, ker v tvojem nizu leta ni
    trenutni_letnik = datetime.now().year

    # Združi datum in čas + pretvori v datetime objekt (dodam letnik, kr ni v nizu)
    datum1 = datetime.strptime(f"{datum_str} {trenutni_letnik} {cas_str}", "%d %b %Y %H:%M")
    datum2 = datetime.strptime(f"{primerjalni_datum_str}", "%Y-%m-%d %H:%M")
    razlika = datum2 - datum1
    return razlika <= timedelta(days=1)

def pridobi_lete_v_24urah(widget_url, local_date_time):
    previous_url = f"{widget_url}?ts=1728763200000&page=-0"
    trenutna_stran = 0
    
    # Zanka za pridobivanje podatkov
    while True:
        potrdilo4 = requests.get(previous_url, verify=False)
        if potrdilo4.status_code == 200:
            # Parsiram HTML vsebino strani
            fourth_doc = BeautifulSoup(potrdilo4.content, "html.parser")
            tabela2 = fourth_doc.find("tbody")
            
            if tabela2:
                prvi_let_datum = tabela2.find_all("tr")[1].find(class_="tt-d").string.strip()
                prvi_let_cas = tabela2.find_all("tr")[1].find(class_="tt-t").string.strip()

                # Ali je prvi let manj kot 24 ur stran
                if je_v_24urah(prvi_let_datum, prvi_let_cas, local_date_time):
                    print(previous_url)
                    print(prvi_let_cas)
                else:
                    break  # Če prvi let ni več znotraj 24 ur, prekini zanko

        trenutna_stran += 1
        previous_url = f"{previous_url[:-len(str(trenutna_stran-1))]}{trenutna_stran}"
    
    print("Konec iskanja letov znotraj 24 ur.")


def pridobivanje_podatkov():
    Seznam_slovarjev = []
    for page in range(stevilo_strani(frontpage_url) + 1):
        #Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        main_url = f"https://ourairports.com/continents/AS/airports.html?start={page*50}"
        doc = pridobi_potrdilo(main_url)

        #Poišči ime letališča, drzavo, tip letalisca, kodo letalisca in st. prihodov
        Sez_letalisc = []
        ime_class = doc.find_all(class_="col-lg-6")
        for letalisce in ime_class:
            ime_letalisca = letalisce.find("h3").find("a").string
            drzava = letalisce.find("p").find("b").string.strip()
            tip_letalisca = letalisce.find("img")["title"]
            koda_letalisca = letalisce.find("h3").find("a")["href"].split('/')[2]
            
            # Lotimo se strani z odhodi in prihodi :')
            poisci_prihode = letalisce.find(title="Arrivals and departures")
            # Preverim, ali link obstaja
            if poisci_prihode:
                url_prihodov = f"https://ourairports.com{poisci_prihode.get("href")}"  # Če obstaja, vzamem 'href'
                potrdilo2 = requests.get(url_prihodov, verify=False)
                if potrdilo2.status_code == 200:
                #Parsiram HTML vsebino vmesne strani
                    sec_doc = BeautifulSoup(potrdilo2.content, "html.parser")
                print(url_prihodov)
                #danes = datetime.date.today()
                
                widget_url = sec_doc.find("iframe")["src"] #Kdo mi je zabičou da morm delat z widgeti?!
                print(widget_url)
                potrdilo3 = requests.get(widget_url, verify=False)
                if potrdilo3.status_code == 200:
                # Parsiram HTML vsebino strani
                    third_doc = BeautifulSoup(potrdilo3.content, "html.parser")
                
                #Vsak prihod posebaj pogledamo
                tabela = third_doc.find("tbody")
                if tabela:
                    try:
                        local_date_time = third_doc.find(id="tt-local-time")["data-date"][:16]                       
                        print(local_date_time)
                        
                        previous_url = f"{widget_url}?ts=1728763200000&page=-0"
                        potrdilo4 = requests.get(previous_url, verify=False)
                        if potrdilo4.status_code == 200:
                        # Parsiram HTML vsebino strani
                            fourth_doc = BeautifulSoup(potrdilo4.content, "html.parser")
                        tabela2 = fourth_doc.find("tbody")
                        
                        
                        #Preverim, ce je prvi let na tej strani manj kot 24 ur stran od zdaj
                        prvi_let_datum = tabela2.find_all("tr")[1].find(class_="tt-d").string.strip()
                        prvi_let_cas = tabela2.find_all("tr")[1].find(class_="tt-t").string.strip()
                        
                        #Dokler prvi let ni vec kot 24 ur oddaljen, bomo parsirali po previous straneh
                        trenutna_stran = 0
                        while je_v_24urah(prvi_let_datum, prvi_let_cas, local_date_time):
                            
                            trenutna_stran += 1
                            previous_url = f"{previous_url[:-len(str(trenutna_stran-1))]}{trenutna_stran}"
                            potrdilo4 = requests.get(previous_url, verify=False)
                            if potrdilo4.status_code == 200:
                            # Parsiram HTML vsebino nove strani
                                fourth_doc = BeautifulSoup(potrdilo4.content, "html.parser")
                            print(previous_url)
                            print(prvi_let_cas)
                        else:
                            for prihod in tabela:
                                datum_prihoda = prihod.find_all(class_="tt-d").string
                                #print(datum_prihoda)
                    except AttributeError:
                        print("stran ti sekr ne dela luzr")
                else: 
                    print("Na strani ni podatka o prihodih")
                #print(prihod)
            else:
                print("Element 'Arrivals and departures' ne obstaja")

            Sez_letalisc.append({"ime letališča" : ime_letalisca, "država": drzava, "tip letališča" : tip_letalisca, "koda letališča": koda_letalisca})
            #Slovar_letalisc[ime_letalisca] = [drzava, tip_letalisca]
        Seznam_slovarjev += (Sez_letalisc)
    return Seznam_slovarjev

#TO DO:

#  sestavi funkcijo, ki pogleda uro in vrne stevilo prihodov zadnjih 24 ur(pazi na previous) sidenote: uposteval sem tudi unknown, scheduled in estimated
#  zapisuj si tudi v koliko razlicnih mest letijo in letalsko druzbo. Lahko vzames tut delay (ce si zelo ambiciozen)