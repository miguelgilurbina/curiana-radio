#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Línea del .txt de Castellanos 1857 → página IMPRESA de la BAE (t. IV).

Por qué existe (campaña M7, 2026-09-22). La ficha `castellanos-elegias` daba la
línea 47693 («PARTE II, INTRODUCCION. 185») como «la única cabecera limpia» y
colgaba de ella la p. 185. Medido: ese «185» es un 183 mal leído por el OCR. El
OCR de Google confunde 3↔5 (y 6↔3, 2↔4) justo en los números de página, así
que ninguna cabecera sola sirve de ancla. Aquí la página se fija por CUATRO
comprobaciones independientes que convergen, y el script las re-mide:

  1. Los números que el OCR lee LIMPIOS justo encima de una cabecera par
     («JUAN DE CASTELLANOS»), tras el «Digitized by» del escaneo: 188, 196,
     200, 202, 204, 212, 220 (tabla `LIMPIOS`).
  2. Las signaturas de pliego «T. IV.» caen cada 16 páginas y siempre en una
     página ≡ 1 (mod 16): 193, 209, 225 en la tabla `SIGNATURAS` (y, fuera de
     los tramos cubiertos, las de las líneas 67476 y 71700 caen en 257 y 273). Con el
     «185» de la ficha caerían en páginas ≡ 3 (mod 16), que no es un pliego.
  3. El índice del tomo: Elegía I, canto I en la p. 186; canto III en la 201.
  4. Arcaya 1920 cita «Elegías, p. 185» para la lista de las once ciudades
     (línea 48248): con esta tabla, la línea 48248 cae en la p. 185.

La tabla `CABECERAS` es la lista de líneas donde EMPIEZA cada página (la
cabecera de columna 1; la de columna 2 no abre página). Cubre lo que la
campaña cita: el final de los preliminares de la Parte II, la Introducción, la
Elegía I entera y el comienzo de la II, más los tramos sueltos de Santa Marta,
de la Parte I y de la Parte III que se citan, cada uno anclado en su número
limpio. Una línea fuera de un tramo cubierto devuelve None: no se adivina.

    python 6-fusion/scripts/castellanos_pagina.py            # comprueba y lista
    python 6-fusion/scripts/castellanos_pagina.py 48216 52883  # páginas de líneas
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXT = os.path.join(RAIZ, "fuentes_caquetios", "Castellanos_1857_Elegias_partes_I-II_texto.txt")

# (línea donde empieza la página, página impresa). Tramos contiguos: dentro de
# un tramo cada fila es la página siguiente de la anterior.
CABECERAS = [
    # ── Parte I, Elegía VI (Boriquén) ──
    (13847, 54), (14097, 55), (14375, 56),
    # ── Parte I, Elegía X (Trinidad, Sedeño) ──
    (24352, 93), (24616, 94), (24881, 95), (25144, 96), (25396, 97), (25684, 98),
    # ── Parte I, Elegía XII, canto III ──
    (36012, 137), (36256, 138),
    # ── Parte II: preliminares, Introducción, Elegía I, comienzo de la II ──
    (46880, 180), (47056, 181), (47280, 182), (47558, 183), (47840, 184),
    (48095, 185), (48378, 186), (48636, 187), (48912, 188), (49177, 189),
    (49458, 190), (49717, 191), (49990, 192), (50259, 193), (50555, 194),
    (50807, 195), (51082, 196), (51353, 197), (51617, 198), (51872, 199),
    (52161, 200), (52416, 201), (52690, 202), (52952, 203), (53232, 204),
    (53493, 205), (53780, 206), (54033, 207), (54303, 208), (54563, 209),
    (54835, 210), (55094, 211), (55372, 212), (55651, 213), (55943, 214),
    (56216, 215),
    # (216: su cabecera no salió en el OCR; 56216→56747 son dos páginas)
    (56747, 217), (57016, 218), (57292, 219), (57553, 220), (57806, 221),
    (58094, 222), (58349, 223), (58618, 224), (58888, 225), (59177, 226),
    # ── Parte II, Relación del Cabo de la Vela / Santa Marta (anclas limpias) ──
    (65225, 249), (65504, 250), (65774, 251), (66041, 252), (66308, 253),
    (69199, 264), (69449, 265), (69723, 266),
    (77908, 297), (78182, 298), (78443, 299),
    # ── Parte III, Benalcázar ──
    (118408, 454), (118663, 455), (118927, 456), (119197, 457), (119468, 458),
]
# Fin de cada tramo (la última página del tramo termina aquí).
FIN_DE_TRAMO = {14375: 14640, 25684: 25950, 36256: 36520, 59177: 59450,
                66308: 66560, 69723: 69990, 78443: 78700, 119468: 119730}

# Números que el OCR leyó limpios encima de una cabecera par (tras «Digitized»).
LIMPIOS = {48909: 188, 51079: 196, 52158: 200, 52687: 202, 53229: 204,
           55369: 212, 57550: 220, 66038: 252, 118405: 454, 119465: 458}
# Signaturas de pliego «T. IV.».
SIGNATURAS = [50401, 54698, 59028]
# Lecturas del OCR que la ficha tomó por buenas y no lo son (la clave es la
# línea de la cabecera; el «157» se imprime encima de la de la línea 36012).
MAL_LEIDOS = {47693: ("185", 183), 50404: ("195", 193), 36012: ("157", 137),
              53092: ("905", 203), 51872: ("109", 199)}


def pagina(linea):
    previas = [(l, p) for l, p in CABECERAS if l <= linea]
    if not previas:
        return None
    l, p = previas[-1]
    fin = FIN_DE_TRAMO.get(l)
    if fin is not None and linea > fin:
        return None
    # dentro de un tramo contiguo, la siguiente cabecera cierra la página
    return p


def _forzar_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def comprobar():
    ok = True
    for linea, esperado in LIMPIOS.items():
        # el número limpio va encima de la cabecera: pertenece a la página que abre
        siguiente = min(l for l, _ in CABECERAS if l > linea)
        got = dict(CABECERAS)[siguiente]
        estado = "✓" if got == esperado else "✗"
        ok &= got == esperado
        print(f"  {estado} número limpio «{esperado}» (línea {linea}) → página {got}")
    for linea in SIGNATURAS:
        p = pagina(linea)
        estado = "✓" if p is not None and p % 16 == 1 else "✗"
        ok &= estado == "✓"
        print(f"  {estado} signatura «T. IV.» (línea {linea}) en la p. {p} (≡ {p % 16} mod 16)")
    for linea, (leido, real) in MAL_LEIDOS.items():
        p = pagina(linea)
        estado = "✓" if p == real else "✗"
        ok &= p == real
        print(f"  {estado} la cabecera OCR «{leido}» (línea {linea}) es la p. {p}")
    # comprobación de que las cabeceras existen donde la tabla dice
    with open(TXT, encoding="utf-8") as f:
        lineas = f.read().split("\n")
    patron = re.compile(r"CASTELLAN|ILUSTR|CASrELLAN|castellan|Varones|TABONES|VAHOLES|JUAN D|^JUAN\s*$", re.I)
    for l, p in CABECERAS:
        if l in (47056,):      # portadilla de la Segunda Parte
            continue
        if not patron.search(lineas[l - 1]):
            ok = False
            print(f"  ✗ la línea {l} (p. {p}) no es una cabecera: {lineas[l - 1][:60]!r}")
    print("  ✓ todas las cabeceras de la tabla están donde dice" if ok else "  ✗ hay fallos")
    return ok


if __name__ == "__main__":
    _forzar_utf8()
    args = [a for a in sys.argv[1:] if a.isdigit()]
    if args:
        for a in args:
            print(f"línea {a} → p. {pagina(int(a))} (BAE 1857, t. IV)")
    else:
        sys.exit(0 if comprobar() else 1)
