"""sondas_hermanas_taino.py — los ceros de la minería 2 taína (regla 6), medidos.

Mide cada sonda de `meta.ceros` de 6-fusion/hermanas_taino_2026-10-09.yaml
sobre los tramos que esa minería leyó:

  Oviedo t. I (copia íntegra)   pdf 240-399  (lib. V-VII)
  Las Casas, Apologética        impresas 320-325, 444-448, 514-540 (pdf + 14)
  Pané (Wikisource)             entero
  Colón 1892 vol. 1             desde el cap. LXI (relato del Almirante + Pané I-XVII)

Imprime, por sonda y por tramo, cuántas coincidencias hay y las primeras con
contexto: un cero aquí es un cero de ESTOS tramos con ESTAS grafías, no de la
obra (minar-fuente §2). Las coincidencias que no son taínas (Plinio, los
egipcios, «linaje humano») se leen a mano en el contexto.

Uso:  python 6-fusion/scripts/sondas_hermanas_taino.py [--contexto N]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys

import pymupdf

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = os.path.join(REPO, "fuentes_caquetios")

SONDAS = {
    "residencia": r"suegr|casa de (su|sus) padres|se iban? a vivir|moraba con|vivia con|viv[ií]an con|resid[ií]a",
    "linaje-clan": r"linaje|parcialidad|casta\b|generaci[oó]n de",
    "sociedades-masculinas": r"mancebos|solteros|casa de los hombres",
    "iniciacion/formacion": r"aprend|enseñ|maestr|disc[ií]pul|novici",
    "tributo": r"tribut",
    "calendario": r"\bluna\b|estaci[oó]n",
}


def _limpia(t: str) -> str:
    t = re.sub(r"-\s*\n\s*", "", t)
    return re.sub(r"\s+", " ", t)


def tramos() -> dict:
    ov = pymupdf.open(os.path.join(F, "Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf"))
    lc = pymupdf.open(os.path.join(F, "LasCasas_Apologetica_NBAE13_Serrano_1909.pdf"))
    pags_lc = list(range(320, 326)) + list(range(444, 449)) + list(range(514, 541))
    with io.open(os.path.join(F, "Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt"), encoding="utf-8") as fh:
        pane = fh.read()
    with io.open(os.path.join(F, "Colon_Hernando_1892_Historia_del_Almirante_vol1.txt"), encoding="utf-8") as fh:
        colon = fh.read()
    i = colon.find("De  algunas  cosas  que  se  vieron")
    return {
        "Oviedo t. I pdf 240-399": _limpia(" ".join(ov[p - 1].get_text() for p in range(240, 400))),
        "Las Casas 320-325/444-448/514-540": _limpia(" ".join(lc[p + 14 - 1].get_text() for p in pags_lc)),
        "Pané (Wikisource)": _limpia(pane),
        "Colón 1892 v1 cap. LXI + Pané I-XVII": _limpia(colon[i:] if i >= 0 else colon),
    }


def main() -> None:
    for nombre in ("stdout",):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer"):
            setattr(sys, nombre, io.TextIOWrapper(flujo.buffer, encoding="utf-8", errors="replace"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--contexto", type=int, default=3, help="coincidencias que se muestran por tramo")
    a = ap.parse_args()
    ts = tramos()
    for tema, patron in SONDAS.items():
        print(f"\n## {tema}  /{patron}/")
        for nombre, texto in ts.items():
            ms = list(re.finditer(patron, texto, flags=re.I))
            print(f"  {nombre}: {len(ms)}")
            for m in ms[: a.contexto]:
                print("     …" + texto[max(0, m.start() - 60):m.end() + 60] + "…")


if __name__ == "__main__":
    main()
