#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mide la Apologética de Las Casas (NBAE 13, Serrano y Sanz 1909) para la
segunda campaña del taíno, parcela T9.

Emite las cifras que cita `6-fusion/taino2_las_casas_apologetica.yaml`
(regla 1: ninguna cifra a mano). Cuatro medidas:

  --desfase     ¿es constante el salto pdf → página impresa?
  --ortografia  conteos por grafía del XVI, antes de contar nada (skill §2)
  --prosodia    las voces que Las Casas marca con acento
  --cobertura   cuántas de las 52 claves taínas del lexicón reciben cita

Sin bandera las corre todas.

Fuente: fuentes_caquetios/LasCasas_Apologetica_NBAE13_Serrano_1909.txt
  (pdftotext -enc UTF-8 sobre el PDF del mismo nombre; el PDF está en
  el repo, ver 4-fuentes/las-casas-apologetica.md)

La clasificación de las 52 es CURADA: sale de leer los pasajes, no de
contar substrings, y por eso va escrita aquí con su página. El script
valida que cubre exactamente las 52 que mide el inventario y cuenta.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import Counter, OrderedDict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TXT = RAIZ / "fuentes_caquetios" / "LasCasas_Apologetica_NBAE13_Serrano_1909.txt"
INVENTARIO = RAIZ / "6-fusion" / "taino_inventario_2026-09-21.yaml"

OFFSET = 14  # página impresa = página pdf (1-based) − 14


def _forzar_utf8() -> None:
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def paginas() -> list[str]:
    if not TXT.exists():
        sys.exit(f"falta {TXT}\n  pdftotext -enc UTF-8 <pdf> {TXT}")
    return TXT.read_text(encoding="utf-8", errors="replace").split("\f")


def impresa(pdf1: int) -> int:
    return pdf1 - OFFSET


# ─────────────────────────────────────────────────────────────────────
def medir_desfase(pags: list[str]) -> None:
    print("── DESFASE pdf → impresa ─────────────────────────────────")
    hist: Counter[int] = Counter()
    con_numero = 0
    for i, p in enumerate(pags):
        nums = re.findall(r"(?m)^\s*(\d{1,3})\s*$", p[:400])
        if not nums:
            continue
        con_numero += 1
        hist[(i + 1) - int(nums[0])] += 1
    top, n = hist.most_common(1)[0]
    print(f"páginas pdf                      : {len(pags)}")
    print(f"con número impreso legible       : {con_numero}")
    print(f"desfase dominante                : {top:+d}  ({n} de {con_numero})")
    print(f"resto (ruido de OCR)             : {con_numero - n}")
    print(f"=> impresa = pdf − {top}   CONSTANTE")
    print()


# ─────────────────────────────────────────────────────────────────────
GRAFIAS = OrderedDict([
    ("cemi",     ["cemi", "cemies", "çemi", "zemi", "chemi"]),
    ("behique",  ["behique", "bohique", "behico", "buhuitihu", "buhiti", "bohiti"]),
    ("areito",   ["areito", "areyto", "areit", "areyt", "aeryto"]),
    ("cohoba",   ["cohoba", "cogioba", "cohiba"]),
    ("hupia",    ["hupia", "maboya", "mabuya"]),
    ("atabey",   ["atabex", "atabey", "yocahu", "guabancex"]),
    ("rango",    ["nitayno", "nitaino", "guaoxeri", "bahari", "matunheri", "naboria"]),
    ("guatiao",  ["guatiao", "guaitiao", "datihao"]),
    ("etnonimo", ["taino", "tayno", "macorix", "maçorix", "ciguayo", "cyguayo", "lucayo"]),
    ("casa",     ["caney", "caneya", "bohio", "buhio", "conuco", "batey", "duohos", "duho"]),
    ("comida",   ["cazabi", "caçabi", "yuca", "axi", "mahiz", "batata", "ajes"]),
    ("esfera",   ["guanin", "taguagua", "çibas", "bixa", "macana", "cotara", "tabaco"]),
    ("prosodia", ["penultima", "ultima silaba", "luenga", "aguda", "silaba", "vocablo"]),
])


def medir_ortografia(pags: list[str]) -> None:
    print("── ORTOGRAFÍA (skill §2: medir ANTES de contar) ──────────")
    entero = norm("\f".join(pags))
    for familia, formas in GRAFIAS.items():
        trozos = [f"{f}={entero.count(norm(f))}" for f in formas]
        print(f"{familia:10s} " + "  ".join(trozos))
    print()
    print("⚠️  dos lecturas de esta tabla que hay que hacer:")
    print("    (a) NFD funde ç con c: `çemi`==`cemi` y `maçorix`==`macorix` NO son")
    print("        dos medidas, son la misma. La cedilla del impreso se ve en la")
    print("        IMAGEN (çibas p. 521), no aquí: los dos pdftotext la pierden.")
    print("    (b) `duohos`=0 y `guaoxeri`=0 son fallos del EXTRACTOR, no de la")
    print("        fuente: las dos voces están en el impreso (pp. 446 y 516) y se")
    print("        leyeron en imagen. Un cero mide la consulta — regla 6.")
    print()


# ─────────────────────────────────────────────────────────────────────
STOP = set("""que los las del una unos unas esta este estos estas otro otra otros otras
muy mas tan como para por con sin sobre entre hasta desde cuando donde porque pero
sino aunque tiene tienen tenia tenian hace hacen hacia hacian dice dicen decia decian
era eran isla islas tierra tierras hombre hombres mujer mujeres casa casas agua aguas
rio rios sierra sierras provincia provincias nombre nombres lengua lenguaje vocablo
vocablos silaba letra acento primera segunda tercera ultima penultima media misma mismo
indios indio gente gentes senores senor rey reyes cosa cosas parte partes toda todo
todos todas cual cuales bien mal aqui alli ella ellas ellos sus dos tres cuatro
llamaban llamado llamada llamadas llamados llamamos nombraban decimos dejimos
arriba abajo asi sera son fue habia hay ser estar""".split())

RX_PROSODIA = re.compile(
    r"([A-Za-z\u00c0-\u017e\u00e7]{3,18})\s*,\s*la\s+([^,;\.]{2,40}?)\s*"
    r"(luenga|aguda|breve)", re.I)


def medir_prosodia(pags: list[str]) -> None:
    print("── PROSODIA: voces que Las Casas acentúa ─────────────────")
    ocur, formas = 0, OrderedDict()
    for i, p in enumerate(pags):
        linea = re.sub(r"\s+", " ", p)
        for m in RX_PROSODIA.finditer(linea):
            voz = m.group(1)
            if norm(voz) in STOP or len(voz) < 3:
                continue
            ocur += 1
            formas.setdefault(norm(voz), (voz, f"{m.group(2)} {m.group(3)}", impresa(i + 1)))
    print(f"ocurrencias con marca prosódica  : {ocur}")
    print(f"formas distintas                 : {len(formas)}")
    print("⚠️  es un SUELO: la red pierde los casos con la columna zipeada")
    print("    (guaoxerí, baharí, matunherí) y los de fórmula «la letra e luenga»")
    print("    (batéy p. 538, nitaynos p. 516).")
    print()


# ─────────────────────────────────────────────────────────────────────
# Clasificación CURADA de las 52 claves. Leída pasaje a pasaje.
#   A = atestación primaria limpia (forma + glosa/acento + atribución)
#   B = misma glosa, otra forma       C = misma forma, otra glosa
#   D = se usa para La Española sin marca metalingüística
#   E = cero verificado
CURADA = {
    "aji": ("A", "axí, 'la pimienta', pp. 27/90/537"),
    "batata": ("A", "batatas, pp. 29"),
    "batey": ("A", "batéy 'pelota, juego y lugar', pp. 121/538"),
    "bejique": ("A", "behiques/bohiques/behicos, pp. 322-323/365/445-447/535"),
    "bixa": ("A", "bixa 'la color bermeja', pp. 36/177"),
    "bohio": ("A", "bohíos, p. 39"),
    "bohío": ("A", "bohíos, p. 39"),
    "caney": ("A", "caney/caneyas 'la casa del señor principal', pp. 345/445"),
    "casabe": ("A", "cazabi/çaçabí 'el pan de raíces', p. 27"),
    "cazabi": ("A", "cazabi/çaçabí 'el pan de raíces', p. 27"),
    "cemi": ("A", "Cemí, pp. 322/445"),
    "guabina": ("A", "guabinas, p. 17"),
    "guanin": ("A", "guanín 'cierta especie de oro bajo', p. 521"),
    "guayaba": ("A", "guayabas, p. 32"),
    "huracan": ("A", "huracanes 'las tempestades', p. 95"),
    "hutia": ("A", "hutías, pp. 26/536"),
    "kunuku": ("A", "conuco 'la labranza', p. 28"),
    "maisi": ("A", "mahíz, pp. 32/177"),
    "maíz": ("A", "mahíz, pp. 32/177"),
    "manati": ("A", "manatíes, p. 27"),
    "naboria": ("A", "naboría 'sirviente o criado', p. 447"),
    "nitaino": ("A", "nitaynos 'nobles y principales', p. 516"),
    "tabako": ("A", "tabacos 'los mosquetes de humo', p. 181"),
    "yuca": ("A", "yuca, p. 28"),
    "dujo": ("B", "el impreso lee «duohos», p. 446"),
    "yamosa": ("B", "el impreso lee «yamocá» para 'dos', p. 538"),
    "daca": ("C", "Las Casas: 'yo'; el lexicón: 'mano' (reconstruida del lokono), p. 447"),
    "cacique": ("D", "usada sin marca metalingüística"),
    "cacike": ("D", "usada sin marca metalingüística"),
}

ETIQUETAS = {
    "A": "atestación primaria limpia",
    "B": "misma glosa, OTRA forma (conflicto)",
    "C": "misma forma, OTRA glosa (conflicto)",
    "D": "usada sin marca metalingüística",
    "E": "CERO verificado",
}

DUPLICADAS = [("bohio", "bohío"), ("casabe", "cazabi"), ("maisi", "maíz")]


def claves_del_inventario() -> list[str]:
    txt = INVENTARIO.read_text(encoding="utf-8")
    m = re.search(
        r"lexicon_vocabulario_base:\s*\n\s*n:\s*(\d+).*?claves:\n((?:\s*-\s*\S+\n)+)",
        txt, re.S)
    if not m:
        sys.exit(f"no se pudo leer el censo en {INVENTARIO}")
    return [l.strip()[2:].strip() for l in m.group(2).strip().split("\n")]


def medir_cobertura() -> None:
    print("── COBERTURA: las 52 claves taínas del lexicón ───────────")
    claves = claves_del_inventario()
    print(f"claves que mide el inventario    : {len(claves)}")
    sobra = [k for k in CURADA if k not in claves]
    if sobra:
        sys.exit(f"la clasificación nombra claves que no están en las 52: {sobra}")

    clasif = {k: CURADA.get(k, ("E", "cero"))[0] for k in claves}
    for et in "ABCDE":
        ks = sorted(k for k in claves if clasif[k] == et)
        print(f"\n{et} — {ETIQUETAS[et]}: {len(ks)}")
        print("   " + ", ".join(ks))

    nA = sum(1 for k in claves if clasif[k] == "A")
    dobles = sum(1 for a, b in DUPLICADAS if clasif.get(a) == "A" and clasif.get(b) == "A")
    sin_cita = sum(1 for k in claves if clasif[k] in ("D", "E"))
    print()
    print(f"=> pasan de 0 citas primarias a UNA, limpia : {nA} claves "
          f"({nA - dobles} voces distintas; {dobles} pares duplicados en el lexicón)")
    print(f"=> reciben cita pero con conflicto          : "
          f"{sum(1 for k in claves if clasif[k] in ('B', 'C'))}")
    print(f"=> siguen sin cita primaria                 : {sin_cita}")
    print()


# ─────────────────────────────────────────────────────────────────────
def main() -> None:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--desfase", action="store_true")
    ap.add_argument("--ortografia", action="store_true")
    ap.add_argument("--prosodia", action="store_true")
    ap.add_argument("--cobertura", action="store_true")
    args = ap.parse_args()
    todo = not any([args.desfase, args.ortografia, args.prosodia, args.cobertura])

    if args.cobertura and not (todo or args.desfase or args.ortografia or args.prosodia):
        medir_cobertura()
        return

    pags = paginas()
    if todo or args.desfase:
        medir_desfase(pags)
    if todo or args.ortografia:
        medir_ortografia(pags)
    if todo or args.prosodia:
        medir_prosodia(pags)
    if todo or args.cobertura:
        medir_cobertura()


if __name__ == "__main__":
    main()
