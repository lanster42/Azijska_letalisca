import os
import csv
import poberi

print(os.getcwd())

#Zapiši podatke v csv datoteko
""" def zapisi_v_csv():
    #To niti podrazno ni narjen do konca
    with open("podatki.csv", "w", encoding='utf-8') as izhodna_dat:
        keys = ["Ime letališča", "Država", "Tip letališča"]
        writer = csv.writer(izhodna_dat).writerow(keys) """
        
        
def zapisi_v_csv():
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    polja = ['Ime letališča',
    'Država', 
    'Tip letališča',
    'Popularnost',
    'Prihodi (zadnjega dne)']
    
    vrstice = poberi.pridobivanje_podatkov()
    
    os.makedirs('Azijska_letalisca', exist_ok=True)
    path = os.path.join('Azijska_letalisca', 'podatki.csv')
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=polja)
        writer.writeheader()
        for vrstica in vrstice:
            writer.writerow(vrstica)
    return

