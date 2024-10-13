# Evropska letališča
Pred vami je projektna naloga iz analize podatkov, ki sem jo ustvaril pri predmetu *Uvod v programiranje* na *Fakulteti za matematiko in fiziko Univerze v Ljubljani* v študijskem letu 2023/24.

## Zajem podatkov
Za vsako Letališče bom zajel naslednje podatke: 
* ime letališča in državo, kateri letališče pripada
* tip letališča (glavno, regionalno, majhno, zaprto ali pa pristajališče za helikopter)
* koliko prihodov (*Arrivals*) je bilo v zadnjih 4 urah, če je ta podatek na strani podan

## Hipopteze in vprašanja
*katere države imajo največ letališč
*katere države imajo največ zaprtih letališč????
*glavna letališča bodo imela največ prihodov v zadnjih 4 urah

## Potek dela
Najprej sem iz strani "https://ourairports.com/continents/AS/airports.html?" pobral podatke v poberi.py. Te podatke sem nato shranil v novo datoteko

## Zapleti in obrazložitve
Šele naknadno sem ugotovil, da te vsak let pošlje na prehodno stran, na kateri je v obliki "widgeta" predstavljena vsebina o letih. Želel sem se vmesni strani izogniti tako, da bi najprej poiskal kodo letališča (ki je seveda edinstvena glede na letališče), to pa potem ustaviti v url končne strani z leti. To se na žalost ni obneslo, saj sem že pri prvem letališču (gl. letališče v Dubaiu) naletel na težavo: Nekatera letališča imajo več kot eno kodo. Na glavni strani je torej na primer za Dubai podana le koda "OMDB", končna spletna stran z leti pa ima v url drugo oznako: "DXB".
