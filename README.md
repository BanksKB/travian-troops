# Travian – vojne jedinice

Skup podataka opisuje 10 vojnih jedinica iz pet plemena igre Travian: Romans,
Teutons, Gauls, Egyptians i Huns. Za svako pleme uključene su dvije jedinice.
Skup je pripremljen za prvu laboratorijsku vježbu iz kolegija Otvoreno računarstvo na FER-u.

## Metapodaci

| Metapodatak | Vrijednost |
| --- | --- |
| Naziv skupa | Travian – vojne jedinice |
| Autor | Karlo Boras |
| JMBAG | 0036520030 |
| Verzija skupa | 1.0 |
| Jezik | Hrvatski nazivi atributa; engleski nazivi plemena, jedinica i tipova |
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
| `travian_troops.csv` | Tablični prikaz, 10 redaka podataka i 16 stupaca |
| `travian_troops.json` | Niz od 10 objekata jedinica, svaki s 15 glavnih polja i ugniježđenim plemenom |
| `travian_db.sql` | Struktura baze, podaci, ključevi i ograničenja |
| `export.py` | Automatizirani izvoz iz baze u CSV i JSON |
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

## Model baze

Podaci su podijeljeni u dvije povezane tablice:

- `plemena`: `id_plemena` (primarni ključ), `naziv` (jedinstven) i `opis`.
- `vojne_jedinice`: `id_jedinice` (primarni ključ), `id_plemena` (strani ključ)
  te naziv i statistike jedinice.

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
psql -U postgres -W -v ON_ERROR_STOP=1 -d travian_db -f travian_db.sql
```

Dump je izrađen za PostgreSQL 18. Naredbe `createdb`, `psql` i `pg_dump`
moraju biti dostupne u varijabli `PATH` ili pokrenute punom putanjom.

## Automatizirani izvoz

Potrebni su Python 3, biblioteka `psycopg` i dostupna baza `travian_db`.
Iz mape koja sadrži `export.py` pokrenuti:

```powershell
python -m pip install "psycopg[binary]"
$env:TRAVIAN_DB_PASSWORD = Read-Host "PostgreSQL lozinka"
python export.py
Remove-Item Env:TRAVIAN_DB_PASSWORD
```

Skripta koristi korisnika `postgres` i lozinku iz varijable okruženja.
SQL upit povezuje tablice preko `id_plemena` i
sortira podatke po ID-ju plemena i jedinice. Skripta prvo zapisuje ravni CSV,
a zatim podatke o plemenu pretvara u ugniježđeni objekt za JSON.
Izlazne datoteke nastaju u trenutačnoj radnoj mapi i prepisuju postojeće izvoze.

Dump baze može se ponovno izraditi naredbom:

```powershell
pg_dump -U postgres -W -d travian_db -f travian_db.sql
```

## Licencija i navođenje

Podaci i dokumentacija objavljuju se pod licencijom
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

