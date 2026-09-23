#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
La CAJA MARINA de la campaña de fauna del mar (FA3, 2026-09-22): qué especies
tienen registro de ocurrencia en las dos aguas de la era 2, según OBIS (el
sistema de información de biodiversidad oceánica) y GBIF.

Regla 1: ninguna cifra a mano. Las cifras de registros que cita
`6-fusion/fauna_paraguana_mar_2026-09-22.yaml` salen de aquí, y este script
las escribe en `6-fusion/fauna_mar_caja_obis_gbif_2026-09-22.yaml`.

Las tres cajas (lon/lat, WGS84):
  - paraguana_dos_aguas: la península entera con sus dos costas, el Golfete
    de Coro y la orilla este del Golfo de Venezuela (no llega a Aruba, 12.5 N)
  - golfete_de_coro: la bahía somera del este (GUARANAO: Tacuato, El Cayude)
  - costa_oeste: Carirubana, Punta Cardón, Amuay, Los Taques (AMUAY)

⚠️ Lo que NO mide: un registro moderno no es presencia en el s. XV (regla 3),
y un cero de OBIS/GBIF mide el esfuerzo de muestreo, no la fauna (regla 6).
Los datos de OBIS y GBIF son CC0 / CC-BY por conjunto de datos: se citan por
la API y la fecha de consulta.

Usa red (api.obis.org, api.gbif.org). No lee curiana_sim/.env, no toca la base.

    python 6-fusion/scripts/caja_marina_obis_gbif.py            # consulta y escribe
    python 6-fusion/scripts/caja_marina_obis_gbif.py --resumen  # sólo imprime
"""

import argparse
import datetime
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SALIDA = os.path.join(RAIZ, "6-fusion", "fauna_mar_caja_obis_gbif_2026-09-22.yaml")

CAJAS = {
    "paraguana_dos_aguas": (-70.40, 11.35, -69.50, 12.30),
    "golfete_de_coro": (-69.95, 11.40, -69.55, 11.75),
    "costa_oeste": (-70.35, 11.55, -70.05, 11.95),
}

# Los grupos que son parcela del mar (FA3). Aves: FA2. Tierra: FA1.
CLASES_MAR = {
    "Teleostei": "peces óseos",
    "Actinopteri": "peces óseos",
    "Actinopterygii": "peces óseos",
    "Elasmobranchii": "tiburones y rayas",
    "Mammalia": "mamíferos marinos",
    "Reptilia": "reptiles (tortugas marinas)",
    "Testudines": "reptiles (tortugas marinas)",
    "Gastropoda": "caracoles",
    "Bivalvia": "almejas, ostras, mejillones",
    "Cephalopoda": "pulpos y calamares",
    "Malacostraca": "cangrejos, camarones, langostas",
    "Echinoidea": "erizos",
    "Asteroidea": "estrellas de mar",
    "Holothuroidea": "pepinos de mar",
    "Anthozoa": "corales y gorgonias",
    "Hexacorallia": "corales y anémonas",
    "Octocorallia": "gorgonias (abanicos de mar)",
    "Scyphozoa": "medusas",
    "Demospongiae": "esponjas",
    "Polyplacophora": "quitones",
}

# Las especies cuya presencia la campaña discute una por una.
CLAVE = [
    "Chelonia mydas", "Eretmochelys imbricata", "Caretta caretta",
    "Dermochelys coriacea", "Lepidochelys olivacea",
    "Tursiops truncatus", "Sotalia guianensis", "Stenella frontalis",
    "Stenella attenuata", "Delphinus delphis", "Megaptera novaeangliae",
    "Balaenoptera edeni", "Physeter macrocephalus", "Trichechus manatus",
    "Neomonachus tropicalis", "Pristis pectinata", "Pristis pristis",
    "Epinephelus itajara", "Rhomboplites aurorubens", "Mugil curema",
    "Mugil incilis", "Mugil liza", "Chaetodipterus faber", "Orthopristis rubra",
    "Orthopristis ruber", "Bagre marinus", "Centropomus undecimalis", "Conodon nobilis",
    "Bairdiella ronchus", "Porichthys plectrodon", "Gorgonia ventalina", "Gorgonia flabellum",
    "Peprilus paru", "Paranthias furcifer", "Mycteroperca tigris", "Chelonoidis carbonarius",
    "Micropogonias furnieri", "Cynoscion jamaicensis", "Sardinella aurita",
    "Albula vulpes", "Elops saurus", "Megalops atlanticus",
    "Rhincodon typus", "Ginglymostoma cirratum", "Hypanus americanus",
    "Aetobatus narinari", "Mobula birostris",
    "Aliger gigas", "Lobatus gigas", "Cittarium pica", "Crassostrea rhizophorae",
    "Pinctada imbricata", "Arca zebra", "Donax striatus", "Tivela mactroides",
    "Melongena melongena", "Brachidontes exustus", "Callinectes sapidus",
    "Cardisoma guanhumi", "Panulirus argus", "Octopus vulgaris",
    "Octopus insularis", "Diadema antillarum", "Echinometra lucunter",
    "Grapsus grapsus", "Coenobita clypeatus", "Alpheus heterochaelis",
]

UA = {"User-Agent": "curiana-caquetio-investigacion/1.0 (campaña fauna del mar)"}


def _forzar_utf8():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def _get(url, reintentos=3):
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # red inestable: se reintenta y se dice
            if i == reintentos - 1:
                raise
            print(f"  (reintento {i + 1}: {e})", file=sys.stderr)
            time.sleep(3)


def wkt(caja):
    x0, y0, x1, y1 = caja
    return f"POLYGON(({x0} {y0},{x1} {y0},{x1} {y1},{x0} {y1},{x0} {y0}))"


def obis_checklist(caja):
    q = urllib.parse.urlencode({"geometry": wkt(caja), "size": 5000})
    url = f"https://api.obis.org/v3/checklist?{q}"
    d = _get(url)
    return url, d.get("total"), d.get("results", [])


def gbif_cuenta(nombre, caja):
    q = urllib.parse.urlencode({"scientificName": nombre, "geometry": wkt(caja),
                                "limit": 0, "facet": "year", "facetLimit": 300})
    url = f"https://api.gbif.org/v1/occurrence/search?{q}"
    d = _get(url)
    anios = []
    for f in d.get("facets", []):
        if f.get("field") == "YEAR":
            anios = sorted(int(c["name"]) for c in f.get("counts", []))
    return url, d.get("count", 0), (min(anios) if anios else None), (max(anios) if anios else None)


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--resumen", action="store_true", help="imprime y no escribe")
    args = ap.parse_args()

    hoy = datetime.date.today().isoformat()
    salida = {
        "meta": {
            "que_es": "Registros de ocurrencia de OBIS y GBIF en las dos aguas de la era 2, "
                      "filtrados a la parcela del mar (sin aves, sin fauna de tierra).",
            "generado_por": "6-fusion/scripts/caja_marina_obis_gbif.py",
            "consultado": hoy,
            "cajas_lon_lat": {k: list(v) for k, v in CAJAS.items()},
            "licencia": "OBIS y GBIF: CC0 o CC-BY según el conjunto de datos; se cita la API y la fecha",
            "regla_3": "un registro moderno NO es presencia en el s. XV: dice qué hay (o se vio) hoy",
            "regla_6": "un cero de OBIS/GBIF mide el muestreo, no la fauna",
        },
        "obis": {},
        "clave": {},
    }

    nombres_por_caja = {}
    for nombre_caja, caja in CAJAS.items():
        url, total, res = obis_checklist(caja)
        grupos = {}
        nombres = {}
        for r in res:
            if r.get("taxonRank") != "Species":
                continue
            cl = r.get("class") or r.get("order")
            if r.get("order") == "Testudines":
                cl = "Testudines"
            if cl not in CLASES_MAR:
                continue
            if cl == "Mammalia" and r.get("order") not in ("Cetacea", "Sirenia", "Carnivora"):
                continue
            if cl == "Reptilia" and r.get("order") != "Testudines":
                continue
            g = CLASES_MAR[cl]
            grupos.setdefault(g, []).append({
                "especie": r.get("scientificName"),
                "familia": r.get("family"),
                "registros": r.get("records"),
            })
            nombres[r.get("scientificName")] = r.get("records")
        for g in grupos:
            grupos[g].sort(key=lambda e: -(e["registros"] or 0))
        nombres_por_caja[nombre_caja] = nombres
        salida["obis"][nombre_caja] = {
            "url": url,
            "taxones_totales_obis": total,
            "especies_de_la_parcela": sum(len(v) for v in grupos.values()),
            "por_grupo_n": {g: len(v) for g, v in sorted(grupos.items())},
            "por_grupo": dict(sorted(grupos.items())),
        }
        print(f"OBIS {nombre_caja}: {total} taxones; parcela del mar: "
              f"{salida['obis'][nombre_caja]['especies_de_la_parcela']} especies")
        time.sleep(1)

    caja = CAJAS["paraguana_dos_aguas"]
    for nombre in CLAVE:
        try:
            url, n, a0, a1 = gbif_cuenta(nombre, caja)
        except Exception as e:
            url, n, a0, a1 = f"(error: {e})", None, None, None
        salida["clave"][nombre] = {
            "obis_registros": {k: v.get(nombre, 0) for k, v in nombres_por_caja.items()},
            "gbif_registros_caja": n,
            "gbif_primer_anio": a0,
            "gbif_ultimo_anio": a1,
        }
        print(f"  {nombre:28s} OBIS={salida['clave'][nombre]['obis_registros']} "
              f"GBIF={n} ({a0}-{a1})")
        time.sleep(0.4)

    if args.resumen:
        return
    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write("# GENERADO por 6-fusion/scripts/caja_marina_obis_gbif.py — no editar a mano.\n")
        yaml.safe_dump(salida, fh, allow_unicode=True, sort_keys=False, width=100)
    print(f"escrito: {os.path.relpath(SALIDA, RAIZ)}")


if __name__ == "__main__":
    main()
