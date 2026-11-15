"""Zajednički upit i formati izvoza za Travian katalog."""

import csv
import io
import json

import psycopg
from psycopg.rows import dict_row

FIELDS = {
    "naziv": "Jedinica", "pleme": "Pleme", "zgrada": "Zgrada",
    "tip_jedinice": "Tip jedinice",
    "napad": "Napad", "obrana_pjesadija": "Obrana od pješaštva",
    "obrana_konjica": "Obrana od konjice", "brzina": "Brzina (polja/h)",
    "nosivost": "Nosivost", "drvo": "Drvo", "glina": "Glina",
    "zeljezo": "Željezo", "zito": "Žito", "potrosnja_zita": "Potrošnja žita (po satu)",
    "vrijeme_treniranja": "Vrijeme treninga (s)",
    "id_jedinice": "ID jedinice", "id_plemena": "ID plemena",
}

QUERY = """
SELECT p.naziv AS pleme, v.*, z.naziv AS zgrada
FROM public.vojne_jedinice v
JOIN public.plemena p USING (id_plemena)
JOIN public.zgrade_za_trening z USING (tip_jedinice)
ORDER BY p.id_plemena, v.id_jedinice
"""


def get_units(query="", field="all"):
    with psycopg.connect(row_factory=dict_row) as connection:
        units = connection.execute(QUERY).fetchall()
    needle = query.strip().casefold()
    if not needle:
        return units
    keys = FIELDS if field == "all" else (field,)
    return [
        unit for unit in units
        if any(unit[key] is not None and needle in str(unit[key]).casefold() for key in keys)
    ]


def get_training_levels():
    with psycopg.connect(row_factory=dict_row) as connection:
        return connection.execute("""
            SELECT z.naziv AS zgrada, r.razina,
                   (r.faktor_vremena * 100)::double precision AS trajanje,
                   ((1 - r.faktor_vremena) * 100)::double precision AS smanjenje
            FROM public.razine_treninga r
            JOIN public.zgrade_za_trening z USING (tip_jedinice)
            ORDER BY z.naziv, r.razina
        """).fetchall()


def json_units(units):
    records = []
    for unit in units:
        record = dict(unit)
        record["pleme"] = {"id_plemena": record.pop("id_plemena"), "naziv": record["pleme"]}
        records.append(record)
    return json.dumps(records, ensure_ascii=False, indent=2) + "\n"


def csv_units(units):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(units)
    return output.getvalue()
