# Travian – vojne jedinice

Skup podataka opisuje 10 vojnih jedinica iz pet plemena igre Travian: Romans,
Teutons, Gauls, Egyptians i Huns. Za svako pleme uključene su dvije jedinice.
Skup je pripremljen za kolegij Otvoreno računarstvo na FER-u. Verzija 2.0 dodaje
zgrade za trening, web tablicu s filtriranjem, izvoz prikaza i JSON Schema.

## Metapodaci

| Metapodatak | Vrijednost |
| --- | --- |
| Naziv skupa | Travian – vojne jedinice |
| Autor | Karlo Boras |
| JMBAG | 0036520030 |
| Verzija skupa | 2.0 |
| Jezik | Hrvatski nazivi atributa te engleski nazivi plemena, jedinica, tipova i zgrada |
| Tematsko područje | Računalne strateške igre, statistike vojnih jedinica |
| Ključne riječi | Travian, plemena, vojne jedinice, napad, obrana, resursi |
| Jedinica promatranja | Jedna vojna jedinica |
| Broj jedinica | 10 |
| Broj plemena | 5 |
| Opseg | Odabrane jedinice; skup nije potpun popis jedinica igre |
| Formati | CSV, JSON i SQL dump PostgreSQL baze |
| Kodiranje | UTF-8 |
| Licencija podataka i dokumentacije | Creative Commons Attribution 4.0 International (CC BY 4.0); vidi LICENSE |
| Izvor podataka | [Travian: Legends](https://www.travian.com/) – tablica statistika pojedinačnih jedinica unutar igre (Instructions → Troops → naziv jedinice) |
| Baza podataka | PostgreSQL; priloženi dump izrađen verzijom 18.6 |

## Datoteke

| Datoteka | Sadržaj |
| --- | --- |
| `podaci/travian_troops.csv` | Tablični prikaz, 10 redaka podataka i 17 stupaca |
| `podaci/travian_troops.json` | Niz od 10 objekata jedinica, s nazivom zgrade i ugniježđenim plemenom |
| `baza/travian_db.sql` | Struktura baze, podaci, ključevi i ograničenja |
| `index.html`, `datatable.html` | Početna stranica i tablica jedinica |
| `podaci/schema.json` | JSON Schema za preuzete podatke |
| `backend/server.py`, `backend/data.py` | Poslužitelj, dohvat, filtriranje i izvoz |
| `frontend/table.js`, `frontend/style.css` | Asinkrono učitavanje tablice i izgled sučelja |
| `README.md` | Opis skupa, atributa i postupka korištenja |
| `LICENSE` | Licencijska obavijest za podatke i dokumentaciju |

## Atributi

CSV ima zaglavlje, koristi zarez kao razdjelnik i svaki redak predstavlja jednu jedinicu.
U JSON-u su `id_plemena` i naziv plemena zajedno u objektu `pleme`.
Brojčane vrijednosti u JSON-u zapisane su kao brojevi.

| Atribut u CSV-u | Tip | Značenje |
| --- | --- | --- |
| `pleme` | tekst | Naziv plemena; u JSON-u objekt s poljima `id_plemena` i `naziv` |
| `id_jedinice` | cijeli broj | Jedinstveni identifikator jedinice u ovom skupu |
| `id_plemena` | cijeli broj | Identifikator pripadajućeg plemena; u JSON-u unutar `pleme` |
| `naziv` | tekst | Naziv vojne jedinice |
| `napad` | cijeli broj | Vrijednost napada jedinice |
| `obrana_pjesadija` | cijeli broj | Vrijednost obrane od pješaštva |
| `obrana_konjica` | cijeli broj | Vrijednost obrane od konjice |
| `brzina` | cijeli broj | Brzina kretanja u poljima na sat |
| `nosivost` | cijeli broj | Količina resursa koju jedinica može nositi |
| `drvo` | cijeli broj | Trošak drva za treniranje jedne jedinice |
| `glina` | cijeli broj | Trošak gline za treniranje jedne jedinice |
| `zeljezo` | cijeli broj | Trošak željeza za treniranje jedne jedinice |
| `zito` | cijeli broj | Jednokratni trošak žita za treniranje jedne jedinice |
| `potrosnja_zita` | cijeli broj | Potrošnja žita za održavanje jedne jedinice |
| `vrijeme_treniranja` | cijeli broj | Trajanje treniranja u sekundama prema pregledu jedinice u igri |
| `tip_jedinice` | tekst | `Infantry` (pješaštvo) ili `Cavalry` (konjica) |
| `zgrada` | tekst | Barracks za pješaštvo ili Stable za konjicu |

## Model baze

Podaci su podijeljeni u četiri povezane tablice:

- `plemena`: `id_plemena` (primarni ključ), `naziv` (jedinstven) i `opis`.
- `vojne_jedinice`: `id_jedinice` (primarni ključ), `id_plemena` (strani ključ)
  te naziv i statistike jedinice.
- `zgrade_za_trening`: `tip_jedinice` (primarni ključ) i jedinstven naziv zgrade.
  Strani ključ povezuje više jedinica istog tipa s njihovom zgradom.
- `razine_treninga`: faktor trajanja za svaku kombinaciju zgrade i razine od 1 do 20.
  Faktor je `0,9^(razina − 1)`. [Barracks](https://knowledgebase.legends.travian.com/en-US/buildings/19) · [Great Stable](https://knowledgebase.legends.travian.com/en-US/buildings/30) · [Usporedba Barracksa i Stablea s Hospitalom](https://support.travian.com/en/articles/77-hospital-and-asclepeion).

Odnos je jedan-prema-više: jedno pleme ima više jedinica, a svaka jedinica pripada
jednom plemenu. Strani ključ osigurava da svaka jedinica upućuje na postojeće pleme.
Kombinacija plemena i naziva jedinice jedinstvena je, a tip jedinice ograničen je na
`Infantry` i `Cavalry`. Identifikatori se automatski dodjeljuju.

PostgreSQL omogućuje povezivanje tablica, provjeru integriteta i izvoz SQL upitom.
Opis plemena čuva se u bazi i dumpu, ali nije uključen u trenutačni CSV i JSON izvoz.

## Obnova baze

Potrebni su instalirani PostgreSQL i njegovi naredbeni alati. Iz mape s datotekama
pokrenuti u PowerShellu, uz pretpostavku da baza `travian_db` još ne postoji:

```powershell
createdb -U postgres -W travian_db
psql -U postgres -W -v ON_ERROR_STOP=1 -d travian_db -f baza/travian_db.sql
```

Dump je izrađen za PostgreSQL 18. Naredbe `createdb`, `psql` i `pg_dump`
moraju biti dostupne u varijabli `PATH` ili pokrenute punom putanjom.

## Pokretanje web prikaza

```powershell
python -m pip install "psycopg[binary]"
$env:PGHOST = "127.0.0.1"
$env:PGUSER = "postgres"
$env:PGDATABASE = "travian_db"
$env:PGPASSWORD = Read-Host "PostgreSQL lozinka" -MaskInput
python backend/server.py
```

Otvori [lokalnu početnu stranicu](http://127.0.0.1:8765/). Poveznice za potpuni skup
poslužuju spremljene datoteke. Tablica dohvaća zapise iz baze asinkrono. Filtar traži po
svim stupcima ili jednom odabranom stupcu. Prazan unos ili gumb **Poništi** vraća sve
zapise. Izvoz iz tablice koristi isti filtar kao prikaz.

Nakon zaustavljanja poslužitelja ukloni lozinku iz terminala naredbom `Remove-Item Env:PGPASSWORD`.

## Licencija i navođenje

Podaci i dokumentacija objavljuju se pod licencijom
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
