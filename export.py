
import csv
import json
import os
import psycopg

conn = psycopg.connect(
    dbname="travian_db", user="postgres",
    password=os.environ["TRAVIAN_DB_PASSWORD"]
)

cur = conn.cursor()
cur.execute("""
    SELECT p.naziv AS pleme, v.*
    FROM vojne_jedinice v
    JOIN plemena p ON p.id_plemena = v.id_plemena
    ORDER BY p.id_plemena, v.id_jedinice
""")

columns = [col.name for col in cur.description]
data = [dict(zip(columns, row)) for row in cur.fetchall()]

with open("travian_troops.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data)

for unit in data:
    unit["pleme"] = {
        "id_plemena": unit.pop("id_plemena"),
        "naziv": unit["pleme"]
    }

with open("travian_troops.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

conn.close()
print("CSV i JSON generirani")
