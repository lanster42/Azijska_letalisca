import os
import csv
import Acquiring_treasure as at

seznam = at.pridobivanje_podatkov(at.frontpage_url)

# S to funkcijo bom sestavil nov seznam s podatki, ki ga bom nato napisal v csv
# Sproti sem dodajal funkcije po potrebi (cisto na koncu sem dodal za zaprta letalisca), zato ni lepa funkcija
def st_letalisc_v_drzavi(seznam):
    nov_slovar = {}
    for slovar in seznam:
        drzava = slovar['Država']
        if drzava not in nov_slovar:
            if slovar["Število prihodov"] == "Ni podatka":
                if slovar["Tip letališča"] == "Closed airport":
                    nov_slovar[drzava] = {"Število letališč": 1, "Št zaprtih": 1, "Število prihodov": 0}
                else:
                    nov_slovar[drzava] = {"Število letališč": 1, "Št zaprtih": 0, "Število prihodov": 0}
            else:
                if slovar["Tip letališča"] == "Closed airport":
                    nov_slovar[drzava] = {"Število letališč": 1, "Št zaprtih": 1, "Število prihodov": int(slovar['Število prihodov'])}  # Pretvori v int
                else:
                    nov_slovar[drzava] = {"Število letališč": 1, "Št zaprtih": 0, "Število prihodov": int(slovar['Število prihodov'])}  # Pretvori v int
        else:
            nov_slovar[drzava]["Število letališč"] += 1
            if slovar["Tip letališča"] == "Closed airport":
                nov_slovar[drzava]["Št zaprtih"] += 1
            if slovar["Število prihodov"] != "Ni podatka":
                nov_slovar[drzava]["Število prihodov"] += int(slovar['Število prihodov'])

    nov_seznam = [{"Država": drzava, **podatki} for drzava, podatki in nov_slovar.items()]
    return nov_seznam

whatever = st_letalisc_v_drzavi(seznam)

def zapisi_dodatni_csv(whatever):
    print(whatever)
    os.makedirs("CSVing", exist_ok=True)
    dat_ime = os.path.join("CSVing", "Supporting.csv")
    with open(dat_ime, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=whatever[0].keys())
        writer.writeheader()
        writer.writerows(whatever)


def st_zaprtih_letalisc(seznam):
    nov_slovar = {}
    for slovar in seznam:
        if slovar["Tip letališča"] == "Closed airport":
            if slovar['Država'] not in nov_slovar:
                nov_slovar[slovar['Država']] = 1
            else:
                nov_slovar[slovar['Država']] += 1
    return nov_slovar