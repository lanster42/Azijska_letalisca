# Azijska letališča
Pred vami je projektna naloga iz analize podatkov, ki sem jo ustvaril pri predmetu *Uvod v programiranje* na *Fakulteti za matematiko in fiziko Univerze v Ljubljani* v študijskem letu 2023/24.

## Zajem podatkov
Za vsako Letališče bom zajel naslednje podatke: 
* ime letališča in državo, kateri letališče pripada
* tip letališča (major/glavno, regional/regionalno, small/majhno, closed/zaprto ali pa helipad/heliport)
* koliko prihodov (*Arrivals*) je bilo v zadnjih 24 urah, če je ta podatek na strani podan
* iz koliko destinacij obstajajo direktni leti na letališče in koliko letalskih družb na letališču deluje

## Hipopteze in vprašanja
* katere države imajo največ letališč
* katere države imajo največ prihodov skupaj
* katere države imajo največ zaprtih letališč
* hipoteza: letališča z največ prihodi bodo uporabljala tudi največ letalskih družb
* katera letališča bodo imela največjo in najmanjšo zamudo?
 * hipoteza: letališča z najmanj prihodi bodo imela največjo in najmanjšo povprečno zamudo.


## Potek dela
Najprej sem iz strani "https://ourairports.com/continents/AS/airports.html" pobral podatke v `Acquiring_treasure.py`. Te podatke sem nato s pomočjo `Hokus_csv.py` shranil v csv datoteko poimenovano `Ogromna_tabela.csv`. 

## Zapleti in obrazložitve
Šele naknadno sem ugotovil, da te vsak zavihek *Flights* letališča pošlje na prehodno stran, na kateri je v obliki "widgeta" predstavljena vsebina o letih. Želel sem se vmesni strani izogniti tako, da bi najprej poiskal kodo letališča (ki naj bi bila seveda edinstvena glede na letališče), to pa potem ustaviti v url končne strani z leti. To se na žalost ni obneslo, saj sem že pri prvem letališču (gl. letališče v Dubaiju) naletel na težavo: Nekatera letališča imajo več kot eno kodo. Na glavni strani je torej na primer za Dubai podana le koda "OMDB", končna spletna stran z leti pa ima v url drugo kodo: "DXB".
