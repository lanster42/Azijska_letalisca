#####################################################################################
#importing
from bs4 import BeautifulSoup
import requests
import time

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
    else:
        return razlika <= timedelta(days=1)

def zamuda(prvi_cas, drugi_cas): # Za pomoc pri izracunu zamude bom uporabil min cas razliko, ker zamuda ne bo nikoli vec od 12 ur
    # Pretvorim oba časa v datetime objekte (brez datuma)
    cas1 = datetime.strptime(prvi_cas, "%H:%M")
    cas2 = datetime.strptime(drugi_cas, "%H:%M")

    # Razlika, ko je cas1 pred cas2 (isti dan)
    razlika1 = cas2 - cas1
    # Razlika, ko je cas2 naslednji dan (čez polnoč)
    cas2_naslednji_dan = cas2 + timedelta(days=1)
    razlika2 = cas2_naslednji_dan - cas1
    
    cas1_naslednji_dan = cas1 + timedelta(days=1)
    razlika3 = cas1_naslednji_dan - cas2
    
    razlika = min(abs(razlika1), razlika2, razlika3)
    minute = razlika.seconds // 60   
    if razlika == razlika1 and razlika1< timedelta(hours=0) or razlika == razlika3:
        return (- minute)
    else:
        return minute

# Primer:
#seznam_tuplov = [("22:00", "22:10"), ("00:10", "23:50"), ("23:40", "00:10")]
    
def povprecna_zamuda(seznam_tuplov):
    sestevek = 0
    brezcasni = 0
    for dvojica in seznam_tuplov:
        try:
            sestevek += zamuda(dvojica[0], dvojica[-1])
        except:
            brezcasni += 1
    return f"{sestevek // (len(seznam_tuplov) - brezcasni)} minut"
        
# Primer:
#widget_url_ = "https://www.avionio.com/widget/en/USM/arrivals"
#local_date_time = "2024-10-13 12:49"

def pridobi_lete_v_24urah(widget_url_):
    previous_url = f"{widget_url_}?page=-0"  # Zacetek, da potem lahko page num spreminjam
    trenutna_stran = 0
    stevilo_letov = 0
    mesta = []
    druzbe = []
    seznam_parov_zamud = []
    
    while True:
        #print(f"Pošiljam zahtevek za stran: {previous_url}")
        third_doc = parsiraj(previous_url) #Na vsaki "strani" lociramo tabelo
        tabela = third_doc.find("tbody")
        if tabela:
            #print(f"Obdelujem stran {trenutna_stran} za URL {previous_url}")
            local_date_time = third_doc.find(id="tt-local-time")["data-date"][:16]
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
                    pristanek = let.find_all("td")[-1].string[-5:]
                     
                    # Pridobivanje letalske druzbe (izognim se podznacki a)
                    try:
                        for a in let.find_all("td")[5].find_all("a"):
                            a.decompose()
                        letalska_druzba = let.find_all("td")[5].get_text(strip=True)
                    except:
                        letalska_druzba = let.find_all("td")[5].string

                    stevilo_letov += 1
                    seznam_parov_zamud.append((cas_leta, pristanek))
                    if zacetno_mesto not in mesta:
                        mesta.append(zacetno_mesto)
                    if letalska_druzba not in druzbe:
                        druzbe.append(letalska_druzba)
                    #print(cas_leta, zacetno_mesto, letalska_druzba, pristanek)
                else:
                    continue
            # Ali je prvi let manj kot 24 ur stran
            if je_v_24urah(prvi_let_datum, prvi_let_cas, local_date_time):
                pass
            else:
                break # Če prvi let ni več znotraj 24 ur, prekini zanko

            trenutna_stran += 1
            previous_url = f"{previous_url[:-len(str(trenutna_stran-1))]}{trenutna_stran}"
        else:
            break
                # Dodaj časovni zamik med zahtevki
                
        time.sleep(0.2)
    #print(stevilo_letov, mesta, druzbe, povprecna_zamuda(seznam_parov_zamud))
    #print("Konec iskanja letov zadnjih 24 ur.")
    return {"Število prihodov": stevilo_letov, "Destinacije": sorted(mesta), 
            "Letalske družbe": sorted(druzbe), "Povprečna zamuda letov": povprecna_zamuda (seznam_parov_zamud)}

def pridobivanje_podatkov(frontpage_url):
    Seznam_slovarjev = []
    for page in range(stevilo_strani(frontpage_url) + 1):
        # Najprej pridobim permition za vsako stran posebaj (po straneh se lahko premikas le po 50 naenkrat)
        main_urls = f"https://ourairports.com/continents/AS/airports.html?start={page*50}"
        doc = parsiraj(main_urls)

        # Poišči ime letališča, drzavo, tip letalisca, kodo letalisca in st. prihodov
        Sez_letalisc = []
        ime_class = doc.find_all(class_="col-lg-6")[:-1]   # Zadnje letališče na n strani je prvo letališče na (n+1) strani
        for letalisce in ime_class: 
            ime_letalisca = letalisce.find("h3").find("a").string
            drzava = letalisce.find("p").find("b").string.strip()
            tip_letalisca = letalisce.find("img")["title"]
            
            # Lotimo se strani z odhodi in prihodi :')
            poisci_prihode = letalisce.find(title="Arrivals and departures")
            # Preverim, ali link obstaja
            if poisci_prihode:
                print(f"Nasel sem prihode od {ime_letalisca}.")
                url_prihodov = f"https://ourairports.com{poisci_prihode.get("href")}"  # Če obstaja, vzamem 'href'
                sec_doc = parsiraj(url_prihodov)
                
                widget_url = sec_doc.find("iframe")["src"] # Kdo mi je zabičou da morm delat z widgeti?! Parsiram widget
                # V posebni funkciji sestavim slovar prihodov
                try:
                    print(widget_url)
                    prihodi = pridobi_lete_v_24urah(widget_url)
                    print("Prihod najden.")
                    #print(prihodi)
                except AttributeError:
                    print("Prihod ni najden.")
                    prihodi = {"Število letov": "Ni podatka", "Destinacije": "Ni podatka", 
            "Letalske družbe": "Ni podatka", "Povprečna zamuda letov": "Ni podatka"}
                    continue
            else:
                print("Element 'Arrivals and departures' ne obstaja")
                prihodi = {"Število letov": "Ni podatka", "Destinacije": "Ni podatka", 
            "Letalske družbe": "Ni podatka", "Povprečna zamuda letov": "Ni podatka"}

            Slovar1 = {"ime letališča" : ime_letalisca, "država": drzava, 
                                 "tip letališča" : tip_letalisca}
            Sez_letalisc.append({**Slovar1, **prihodi})
            print(Sez_letalisc)
        Seznam_slovarjev += (Sez_letalisc)
        #print(Seznam_slovarjev)
    return Seznam_slovarjev

#TO DO:

# Debuggej tazadno funkcijo, zdi se mi, da so ostale okey. 
# Na koncu: "Slovenjenje"