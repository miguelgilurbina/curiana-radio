#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — el cero antillano en la arqueología del Golfete, medido
=================================================================

Segunda campaña del taíno, parcela T8 (2026-09-22). Emite las cifras del lado
del REPO que citan `6-fusion/taino2_evidencia_material_contacto.yaml` y su
issue. **Ninguna cifra de esos documentos está escrita a mano** (regla 1):
las de este lado salen de aquí; las del otro lado son citas de fuentes
externas y llevan su página.

Mide tres cosas, y las tres son lecturas — no escribe nada:

1. **El cero de las series antillanas en el registro arqueológico del
   Golfete.** ¿Aparece alguna vez «ostionoide», «chicoide», «meillacoide»,
   «guanín», «jadeíta», «Antillas Mayores» en las obras de arqueología de
   Falcón y las ABC que el repo tiene? Regla 6: un `grep` a cero mide tu
   consulta, así que se barre con raíz corta, sin acentos, en español y en
   inglés, y se imprime también lo que SÍ sale (dabajuroide, Strombus), que
   es el control de que el barrido funciona.

2. **Los archivos de 0 bytes**, que son el motivo de que el cero de arriba
   sea un negativo sobre lo que el repo tiene y no sobre el registro
   arqueológico caribeño.

3. **El taíno en `3-mundo/`**, sólo como recordatorio de dónde vive hoy: lo
   mide en detalle `medir_taino_en_la_esfera.py` (campaña anterior) y aquí
   sólo se cuenta el nodo de Curazao, que es el que esta parcela toca.

Necesita `pdftotext` en el PATH (ver la trampa de CLAUDE.md: `pypdf` y
`pdftotext` no dan el mismo texto). Si no está, lo dice y sale sin fingir
un cero.

Uso:
    python 6-fusion/scripts/medir_taino2_evidencia_material.py
    python 6-fusion/scripts/medir_taino2_evidencia_material.py --json
"""

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(_AQUI))

# Las obras de ARQUEOLOGÍA del área que el repo tiene con capa de texto. No se
# barren aquí las crónicas ni los vocabularios: la pregunta es de cultura
# material.
OBRAS = [
    ("urbina-jimenez-2011",
     "fuentes_caquetios/Urbina_2011_Archaeological_Survey_Coastal_Falcon_UCL.pdf",
     "prospección de 192 yacimientos agroalfareros de Falcón costero (UCL)"),
    ("zavala-reyes-2018",
     "fuentes_caquetios/ZavalaReyes_et_al_2018_Arqueologia_Medanos_Coro.pdf",
     "Médanos de Coro: dos áreas de recolección caquetías, s. XIV-XVIII"),
    ("antczak-2015-las-aves",
     "fuentes_caquetios/Antczak_Antczak_2015_Las_Aves_Arqueologia.pdf",
     "Las Aves: el borde ORIENTAL del mar caquetío"),
    ("antczak-2017-cariban",
     "fuentes_caquetios/Antczak_et_al_2017_Cariban_Migration_Orinoco.pdf",
     "la migración caribana al centro-norte, con Los Roques dentro"),
    ("schroeder-2018",
     "fuentes_caquetios/Schroeder_et_al_2018_PNAS_Caribbean_Taino.pdf",
     "el genoma lucayo (control: aquí el taíno SÍ tiene que salir)"),
    ("moron-2012-petroglifos",
     "fuentes_caquetios/Moron_2012_Petroglifos_Falcon.pdf",
     "petroglifos de Falcón — la única afirmación positiva que existía"),
]

# Sondas de CULTURA MATERIAL antillana. Raíz corta y sin acentos (skill §2).
SONDAS_ANTILLANAS = [
    "ostionoid", "chicoid", "meillacoid", "elenoid", "palmetto",
    "guanin", "tumbaga", "jadeit", "jadeita", "cemi", "zemi",
    "guaiza", "duho", "dujo", "trigonolito", "tres puntas",
    "antillas mayores", "greater antilles", "hispaniol", "espanola",
    "taino", "lucayo", "lucayan", "boriqu",
]

# Control positivo: si estas dan cero, el barrido está roto, no la fuente.
SONDAS_CONTROL = [
    "dabajuro", "caquet", "strombus", "lobatus", "concha", "sherd", "ceramic",
]

VACIOS = [
    "fuentes_caquetios/Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf",
    "fuentes_caquetios/Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf",
    "fuentes_caquetios/Brinton_1871_Arawack_Language_Guiana.pdf",
    "fuentes_caquetios/Ramos_Perez_1978_resenia_Persee.pdf",
]


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def plano(texto):
    """Minúsculas y sin diacríticos: así `Caquet´ıo` y `Caquetío` casan."""
    desc = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in desc if unicodedata.category(c) != "Mn")


def texto_de(pdf, cache):
    """pdftotext del PDF, cacheado. Devuelve None si el archivo no sirve."""
    ruta = os.path.join(REPO, pdf)
    if not os.path.exists(ruta) or os.path.getsize(ruta) == 0:
        return None
    destino = os.path.join(cache, os.path.basename(pdf) + ".txt")
    if not os.path.exists(destino):
        subprocess.run(["pdftotext", "-enc", "UTF-8", ruta, destino],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    with open(destino, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not shutil.which("pdftotext"):
        print("🔴 pdftotext no está en el PATH. No se mide nada: un cero sin "
              "extractor no es un cero de la fuente (regla 6).")
        return 1

    salida = {"obras": {}, "vacios": {}, "sondas_antillanas": SONDAS_ANTILLANAS}
    cache = tempfile.mkdtemp(prefix="curiana_taino2_")
    try:
        for clave, pdf, que_es in OBRAS:
            bruto = texto_de(pdf, cache)
            if bruto is None:
                salida["obras"][clave] = {"estado": "sin-texto", "que_es": que_es}
                continue
            s = plano(bruto)
            reg = {
                "que_es": que_es,
                "caracteres": len(bruto),
                "antillanas": {t: len(re.findall(re.escape(plano(t)), s))
                               for t in SONDAS_ANTILLANAS},
                "control": {t: len(re.findall(re.escape(plano(t)), s))
                            for t in SONDAS_CONTROL},
            }
            reg["total_antillano"] = sum(reg["antillanas"].values())
            reg["total_control"] = sum(reg["control"].values())
            salida["obras"][clave] = reg

        for pdf in VACIOS:
            ruta = os.path.join(REPO, pdf)
            tam = os.path.getsize(ruta) if os.path.exists(ruta) else None
            salida["vacios"][os.path.basename(pdf)] = tam
    finally:
        shutil.rmtree(cache, ignore_errors=True)

    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
        return 0

    print("=" * 72)
    print("EL CERO ANTILLANO EN LA ARQUEOLOGÍA DEL ÁREA — medido hoy")
    print("=" * 72)
    for clave, reg in salida["obras"].items():
        if reg.get("estado") == "sin-texto":
            print(f"\n🔴 {clave}: SIN TEXTO (archivo ausente o de 0 bytes) — "
                  f"{reg['que_es']}")
            continue
        print(f"\n▸ {clave} — {reg['que_es']}")
        print(f"  {reg['caracteres']:,} caracteres extraídos")
        aciertos = {t: n for t, n in reg["antillanas"].items() if n}
        if aciertos:
            print("  cultura material antillana: " +
                  ", ".join(f"{t}={n}" for t, n in sorted(aciertos.items())))
        else:
            print("  cultura material antillana: CERO en las "
                  f"{len(SONDAS_ANTILLANAS)} sondas")
        ctrl = {t: n for t, n in reg["control"].items() if n}
        print("  control (el barrido funciona): " +
              (", ".join(f"{t}={n}" for t, n in sorted(ctrl.items()))
               if ctrl else "🔴 TAMBIÉN A CERO — el barrido está roto"))

    print("\n" + "=" * 72)
    print("ARCHIVOS DE 0 BYTES (por qué el cero es del repo, no del registro)")
    print("=" * 72)
    for nombre, tam in salida["vacios"].items():
        marca = "🔴 0 bytes" if tam == 0 else (
            f"{tam:,} bytes" if tam else "ausente")
        print(f"  {marca:>14}  {nombre}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
