import os
import csv
import Acquiring_treasure as at
import Supporting_char as sc

seznam = at.pridobivanje_podatkov(at.frontpage_url)

#Zapiši podatke v csv datoteko
def zapisi_v_csv(seznam):
    """
    Funkcija v csv datoteko podano s parametroma "directory" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs("CSVing", exist_ok=True)
    dat_ime = os.path.join("CSVing", "Ogromna_tabela.csv")
    with open(dat_ime, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=seznam[0].keys())
        writer.writeheader()
        writer.writerows(seznam)