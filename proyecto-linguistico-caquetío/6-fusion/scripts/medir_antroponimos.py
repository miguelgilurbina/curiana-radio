#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mide la campaña de antropónimos: 6-fusion/antroponimos_caquetios.yaml.

Regla 1 del proyecto: ninguna cifra a mano. Lo que el YAML declara en
`formantes[].recurrencia` lo vuelve a contar este script sobre el corpus de
formas del propio YAML; si no coinciden, es un bug del YAML.

Qué mide:
  · cuántos antropónimos hay, por tipo, por época y por etiqueta
  · cuántos llevan marca de regla 3 y de regla 4
  · la recurrencia de cada formante = cuántas FORMAS DISTINTAS del corpus
    (forma + variantes de una sola palabra) terminan en él, comparadas con
    curiana_fonotactica.fonemizar para que la ortografía colonial y la
    lingüística cuenten juntas (Uriacoa/uriakoa, Bonyata/Boniata)
  · si cada `ejemplos` del formante está de verdad en el corpus
  · cuántas formas del corpus coinciden con un topónimo del canon

No llama a ninguna API, no lee curiana_sim/.env y no toca Supabase.

    python 6-fusion/scripts/medir_antroponimos.py
    python 6-fusion/scripts/medir_antroponimos.py --check   # 0 si cuadra
"""

import argparse
import collections
import io
import os
import re
import sys

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))

ANTROPONIMOS = os.path.join(RAIZ, "6-fusion", "antroponimos_caquetios.yaml")
TOPONIMOS = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")

# Partículas de tratamiento colonial: no son parte del nombre indígena.
TRATAMIENTOS = {"don", "dona", "doña", "de", "el", "la", "y"}


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def cargar(path):
    with io.open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def formas_de(entrada):
    """Las formas de una sola palabra de una entrada: `forma` + `variantes`.

    De «Don Sancho Uriacoa» se queda con `Uriacoa`: el tratamiento colonial no
    es parte del nombre. De «Gorybacoa ~ Goyabaco ~ Guaibacoa (el pueblo…)» se
    queda con las tres formas y tira el paréntesis.
    """
    crudas = [entrada.get("forma")] + list(entrada.get("variantes") or [])
    fuera = []
    for c in crudas:
        if not c:
            continue
        c = re.sub(r"\(.*?\)", " ", str(c))
        for pieza in re.split(r"[~,/]| ", c):
            pieza = pieza.strip()
            if pieza and pieza.lower() not in TRATAMIENTOS:
                fuera.append(pieza)
    return fuera


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="no imprime el informe largo; 0 si todo cuadra")
    args = ap.parse_args(argv)

    from curiana_fonotactica import fonemizar

    datos = cargar(ANTROPONIMOS)
    entradas = datos["antroponimos"]
    formantes = datos["formantes"]

    biblio = cargar(BIBLIO)["obras"]
    obras_validas = set(biblio) if isinstance(biblio, dict) else {
        o["id"] for o in biblio if isinstance(o, dict) and o.get("id")}
    toponimos = {fonemizar(t["forma"]) for t in cargar(TOPONIMOS)["toponimos"]}

    fallos = []

    # ── el corpus de formas ──────────────────────────────────────────
    corpus = {}          # forma tal cual -> fonemizada
    for e in entradas:
        for f in formas_de(e):
            corpus.setdefault(f, fonemizar(f))
    fonemizadas = sorted(set(corpus.values()))

    # ── procedencia: clave foránea a bibliografia.yaml (regla 8) ─────
    sin_procedencia = []
    for e in entradas:
        p = e.get("procedencia")
        obra = (p or {}).get("obra") if isinstance(p, dict) else None
        if obra and obra not in obras_validas:
            fallos.append(f"{e['forma']}: procedencia.obra «{obra}» no existe en bibliografia.yaml")
        if not obra:
            sin_procedencia.append(e["forma"])
            if not e.get("deuda"):
                fallos.append(f"{e['forma']}: sin procedencia y sin `deuda: sin-procedencia`")
        for a in e.get("apoyos") or []:
            o = a.get("obra")
            if o and o not in obras_validas:
                fallos.append(f"{e['forma']}: apoyo con obra «{o}» que no existe en bibliografia.yaml")

    # ── recurrencia medida de cada formante ──────────────────────────
    medido_formantes = {}
    for f in formantes:
        cola = fonemizar(f["formante"].lstrip("-"))
        llevan = sorted({c for c in fonemizadas if c.endswith(cola) and c != cola})
        medido_formantes[f["formante"]] = llevan
        if f.get("recurrencia") != len(llevan):
            fallos.append(
                f"formante {f['formante']}: declara recurrencia {f.get('recurrencia')} "
                f"y se miden {len(llevan)} ({', '.join(llevan)})")
        for ej in f.get("ejemplos") or []:
            if fonemizar(re.sub(r"\(.*?\)", " ", str(ej)).split("~")[0]) not in fonemizadas:
                fallos.append(f"formante {f['formante']}: el ejemplo «{ej}» no está en el corpus de antropónimos")

    # ── conteos ──────────────────────────────────────────────────────
    conteos = {
        "entradas": len(entradas),
        "formas_distintas": len(corpus),
        "formas_fonemizadas_distintas": len(fonemizadas),
        "por_tipo": dict(collections.Counter(e.get("tipo") for e in entradas)),
        "por_etiqueta": dict(collections.Counter(
            str(e.get("etiqueta", "")).split(" ")[0] for e in entradas)),
        "por_epoca": dict(collections.Counter(
            str(e.get("epoca", "")).split(" ")[0].split("/")[0] for e in entradas)),
        "con_regla_3": sum(1 for e in entradas if e.get("regla_3")),
        "con_regla_4": sum(1 for e in entradas if e.get("regla_4")),
        "sin_procedencia": len(sin_procedencia),
        "formantes_productivos": sum(1 for f in formantes if f.get("productivo_en_la_era_2")),
        "formas_que_son_toponimo_del_canon": sorted(
            f for f, fon in corpus.items() if fon in toponimos),
    }

    print("── CONTEOS ──")
    for k, v in conteos.items():
        print(f"  {k}: {v}")

    if not args.check:
        print("\n── FORMANTES (recurrencia medida) ──")
        for f in formantes:
            llevan = medido_formantes[f["formante"]]
            marca = "productivo" if f.get("productivo_en_la_era_2") else "no productivo"
            print(f"  {f['formante']:8} {len(llevan):2}  [{marca}]  {', '.join(llevan)}")

        print("\n── SIN PROCEDENCIA (deuda declarada) ──")
        print(f"  {', '.join(sin_procedencia) or '(ninguno)'}")

    print("\n── RESULTADO ──")
    if fallos:
        for m in fallos:
            print(f"  FALLO: {m}")
        print(f"\n  {len(fallos)} fallo(s).")
        return 1
    print("  todo en verde.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
