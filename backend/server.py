from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json

import psycopg

from data import FIELDS, csv_units, get_training_levels, get_units, json_units

ROOT = Path(__file__).resolve().parent.parent
STATIC = {
    "/": ("index.html", "text/html"),
    "/index.html": ("index.html", "text/html"),
    "/datatable.html": ("datatable.html", "text/html"),
    "/frontend/style.css": ("frontend/style.css", "text/css"),
    "/frontend/table.js": ("frontend/table.js", "text/javascript"),
    "/podaci/schema.json": ("podaci/schema.json", "application/schema+json"),
    "/podaci/travian_troops.csv": ("podaci/travian_troops.csv", "text/csv"),
    "/podaci/travian_troops.json": ("podaci/travian_troops.json", "application/json"),
}


class Handler(BaseHTTPRequestHandler):
    def database_error(self, error):
        self.log_error("PostgreSQL: %s", error)
        if isinstance(error, psycopg.errors.UndefinedTable):
            message = "U bazi nedostaje tablica. Provjeri naziv baze i pokreni migracije prema README-u."
        elif "no password supplied" in str(error):
            message = "PostgreSQL traži lozinku. Postavi PGPASSWORD u terminalu u kojem pokrećeš server.py."
        elif isinstance(error, psycopg.OperationalError):
            message = "Veza s PostgreSQL-om nije uspjela. Provjeri postavke i grešku u terminalu."
        else:
            message = "Upit prema bazi nije uspio. Provjeri grešku u terminalu."
        self.respond(json.dumps({"error": message}, ensure_ascii=False), "application/json", 503)

    def respond(self, content, mime, status=200, filename=None):
        body = content.encode("utf-8") if isinstance(content, str) else content
        self.send_response(status)
        self.send_header("Content-Type", f"{mime}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path in STATIC:
            filename, mime = STATIC[url.path]
            self.respond((ROOT / filename).read_bytes(), mime)
            return
        if url.path == "/api/training-levels":
            try:
                self.respond(json.dumps(get_training_levels()), "application/json")
            except psycopg.Error as error:
                self.database_error(error)
            return
        if url.path != "/api/units":
            self.send_error(404)
            return

        query = parse_qs(url.query)
        field = query.get("field", ["all"])[0]
        format_name = query.get("format", ["table"])[0]
        if (field != "all" and field not in FIELDS) or format_name not in {"table", "csv", "json"}:
            self.send_error(400)
            return
        try:
            units = get_units(query.get("q", [""])[0], field)
        except psycopg.Error as error:
            self.database_error(error)
            return
        if format_name == "csv":
            self.respond(csv_units(units), "text/csv", filename="travian_filtrirano.csv")
        elif format_name == "json":
            self.respond(json_units(units), "application/json", filename="travian_filtrirano.json")
        else:
            self.respond(json.dumps({"fields": FIELDS, "units": units}), "application/json")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), Handler) as server:
        print(f"http://127.0.0.1:{server.server_port}", flush=True)
        server.serve_forever()
