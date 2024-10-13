#####################################################################################
#importing
from bs4 import BeautifulSoup
import requests
import re

#####################################################################################
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings()  # Stran je bila varna v prvih 2 tednih dela z njo, a ji je nato potekel certifikat o varnosti

frontpage_url = "https://ourairports.com/continents/AS/airports.html"

#####################################################################################

def parsiraj(zeljen_url):
    potrdilo = requests.get(zeljen_url, verify=False) # Verify sem dodal, saj je strani med pisanjem kode potekel certifikat o varnosti :)
    if potrdilo.status_code == 200:
    # Parsiram HTML vsebino vmesne strani
        return BeautifulSoup(potrdilo.content, "html.parser")

# Stevilo letalisc na frontpage
def stevilo_strani(zeljen_url):
    doc = parsiraj(zeljen_url)
    st_letalisc = int(doc.find(class_="badge hidden-sm").string.replace(",", ""))
    st_strani = st_letalisc//50 + 1
    return st_strani

# Funkcija, ki preveri, če je čas (podan z datum_str in cas_str) manj kot 1 dan pred primerjalnim datumom
def je_v_24urah(datum_str, cas_str, primerjalni_datum_str, moznost=""):
    # Določi trenutni letnik, ker v datumu leta ni
    trenutni_letnik = datetime.now().year

    # Združim datum in čas + pretvorim v datetime objekt (dodam letnik prvemu)
    datum1 = datetime.strptime(f"{trenutni_letnik} {datum_str} {cas_str}", "%Y %d %b %H:%M") # %b je okrajsava meseca (Oct)
    datum2 = datetime.strptime(f"{primerjalni_datum_str}", "%Y-%m-%d %H:%M")
    razlika = datum2 - datum1
    
    # Preverim, ali je datum1 pred datum2 in ali je razlika manjša od 24 ur
    
    if moznost == "strogo":
        return razlika >= timedelta(hours=0) and razlika <= timedelta(days=1)
    else: return razlika <= timedelta(days=1)
    

# Primer:
widget_url_ = "https://www.avionio.com/widget/en/SIN/arrivals"
local_date_time_ = "2024-10-13 12:49"

def pridobi_lete_v_24urah(widget_url_):
    previous_url = f"{widget_url_}?page=-0"
    trenutna_stran = 0
    stevilo_letov = 0
    
    while True:
        fourth_doc = parsiraj(previous_url) #Na vsaki "strani" lociramo tabelo
        local_date_time = fourth_doc.find(id="tt-local-time")["data-date"][:16]
        tabela = fourth_doc.find("tbody")
        if tabela:
            prvi_let_datum = tabela.find_all("tr")[1].find(class_="tt-d").string.strip()
            prvi_let_cas = tabela.find_all("tr")[1].find(class_="tt-t").string.strip()
            
            vsi_leti = tabela.find_all("tr")[1:-1]  # Nocem pobrati se "tr" za previous in next
            filtrirani_leti = [let for let in vsi_leti 
                if not any(cls in ['cancelled', 'tt-child', 'diverted'] for cls in let.get('class'))] # Nocem podvojenih, diverted ali cancelled letov
            
            for let in filtrirani_leti:
                cas_leta = let.find_all("td")[0].string.strip()
                datum_leta = let.find_all("td")[1].string.strip()
                if je_v_24urah(datum_leta, cas_leta, local_date_time, "strogo"):
                    zacetno_mesto = let.find_all("td")[3].string
                    pristanek = let.find_all("td")[-1].string
                     
                    # Pridobivanje letalske druzbe (izognim se podznacki a)
                    try:
                        for a in let.find_all("td")[5].find_all("a"):
                            a.decompose()
                        letalska_druzba = let.find_all("td")[5].get_text(strip=True)
                    except:
                        letalska_druzba = let.find_all("td")[5].string
                    print(cas_leta, zacetno_mesto, letalska_druzba, pristanek)

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
        # Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        main_urls = f"https://ourairports.com/continents/AS/airports.html?start={page*50}"
        doc = parsiraj(main_urls)

        # Poišči ime letališča, drzavo, tip letalisca, kodo letalisca in st. prihodov
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
                sec_doc = parsiraj(url_prihodov)
                print(url_prihodov)
                
                widget_url = sec_doc.find("iframe")["src"] # Kdo mi je zabičou da morm delat z widgeti?!
                third_doc = parsiraj(widget_url)
                print(widget_url)
                
                # Vsak prihod posebaj pogledamo
                tabela = third_doc.find("tbody")
                if tabela:
                    try:
                        local_date_time = third_doc.find(id="tt-local-time")["data-date"][:16]                       
                        print(local_date_time)
                        
                        previous_url = f"{widget_url}?ts=1728763200000&page=-0"
                        fourth_doc = parsiraj(previous_url)
                        tabela2 = fourth_doc.find("tbody")
                        
                        # Preverim, ce je prvi let na tej strani manj kot 24 ur stran od zdaj
                        prvi_let_datum = tabela2.find_all("tr")[1].find(class_="tt-d").string.strip()
                        prvi_let_cas = tabela2.find_all("tr")[1].find(class_="tt-t").string.strip()
                        
                        # Dokler prvi let ni vec kot 24 ur oddaljen, bomo parsirali po previous straneh
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

#  Na koncu: "Slovenjenje"