# -*- coding: utf-8 -*-
"""Las Casas 1875 vol. I — mapa capítulo → (página impresa 1875, página pdf).

POR QUÉ EXISTE ESTE SCRIPT
--------------------------
`fuentes_caquetios/Las_Casas_1875_Historia_Indias_vol1.pdf` **no es un facsímil
de la edición de 1875**: es el ebook de Project Gutenberg #49298 llevado a PDF.
Su pie de página es un contador propio —la página pdf 43 dice «43»— y coincide
con el índice del pdf en 609 de sus 613 páginas. La paginación de 1875 NO
está en el cuerpo del texto.

Pero el **índice original de 1875 sobrevive** (páginas pdf 572-596) con sus
números de página impresa. De ahí sale el ancla: para cada capítulo, la página
impresa donde arranca y la página pdf donde arranca. El desfase NO es constante
(va de +8 en el cap. I a +69 en el LXXXII), así que una cita se ancla por
CAPÍTULO y, dentro de él, por interpolación declarada como estimada.

Uso:
    python 6-fusion/scripts/mapa_capitulos_las_casas.py [ruta_del_txt_layout]

Si no se le pasa ruta, extrae el texto él mismo con `pdftotext -layout`.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROM = r"(?:M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3}))"
ROMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
        "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII",
        "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX", "XXXI",
        "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX",
        "XL", "XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII", "XLVIII",
        "XLIX", "L", "LI", "LII", "LIII", "LIV", "LV", "LVI", "LVII", "LVIII",
        "LIX", "LX", "LXI", "LXII", "LXIII", "LXIV", "LXV", "LXVI", "LXVII",
        "LXVIII", "LXIX", "LXX", "LXXI", "LXXII", "LXXIII", "LXXIV", "LXXV",
        "LXXVI", "LXXVII", "LXXVIII", "LXXIX", "LXXX", "LXXXI", "LXXXII"]
PDF = "fuentes_caquetios/Las_Casas_1875_Historia_Indias_vol1.pdf"
INDICE_PDF = (572, 597)  # rango [inicio, fin) de páginas pdf del índice de 1875


def _forzar_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sin_pie(pagina, i):
    """Quita la línea-pie que es el contador del ebook (i es 1-based)."""
    ls = pagina.split("\n")
    while ls and not ls[-1].strip():
        ls.pop()
    if ls and ls[-1].strip() == str(i):
        ls.pop()
    return "\n".join(ls)


def cargar_paginas(ruta_txt=None):
    if ruta_txt and os.path.exists(ruta_txt):
        texto = open(ruta_txt, encoding="utf-8", errors="replace").read()
    else:
        tmp = os.path.join(tempfile.mkdtemp(), "lascasas_layout.txt")
        subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", PDF, tmp],
                       check=True)
        texto = open(tmp, encoding="utf-8", errors="replace").read()
    return texto.split("\f")


def paginas_impresas(paginas):
    """Del índice original de 1875: capítulo → página impresa de arranque."""
    idx = "\n".join(sin_pie(paginas[i - 1], i)
                    for i in range(*INDICE_PDF) if i - 1 < len(paginas))
    marcas = [(m.start(), m.group(1))
              for m in re.finditer(r"Cap(?:\.|[ií]tulo)\s+(" + ROM + r")\.?(?![A-Za-z])", idx)
              if m.group(1)]
    fuera = {}
    for k, (pos, cap) in enumerate(marcas):
        fin = marcas[k + 1][0] if k + 1 < len(marcas) else len(idx)
        bloque = idx[pos:fin]
        nums = re.findall(r"(?<![\d.,])(\d{1,3})\s*$", bloque, re.MULTILINE)
        if nums and cap not in fuera:
            fuera[cap] = int(nums[-1])
    return fuera


def paginas_pdf(paginas):
    """Dónde arranca cada capítulo dentro del pdf."""
    fuera = {}
    for i, p in enumerate(paginas, start=1):
        cuerpo = sin_pie(p, i)
        for m in re.finditer(r"CAP[IÍ]TULO\s+(PRIMERO|" + ROM + r")\.?(?:\[\d+\])?\s*$",
                             cuerpo, re.MULTILINE):
            cap = "I" if m.group(1) == "PRIMERO" else m.group(1)
            if cap and cap not in fuera:
                fuera[cap] = i
    return fuera


def construir(ruta_txt=None):
    paginas = cargar_paginas(ruta_txt)
    impresas, pdfs = paginas_impresas(paginas), paginas_pdf(paginas)
    mapa = {}
    for k, cap in enumerate(ROMS):
        sig = ROMS[k + 1] if k + 1 < len(ROMS) else None
        hasta = (impresas.get(sig) - 1) if sig and impresas.get(sig) else None
        mapa[cap] = {"pagina_impresa": impresas.get(cap),
                     "pagina_pdf": pdfs.get(cap),
                     "hasta_impresa": hasta}
    return mapa, len(paginas)


if __name__ == "__main__":
    _forzar_utf8()
    mapa, n = construir(sys.argv[1] if len(sys.argv) > 1 else None)
    completos = [c for c in ROMS
                 if mapa[c]["pagina_impresa"] and mapa[c]["pagina_pdf"]]
    offs = [mapa[c]["pagina_pdf"] - mapa[c]["pagina_impresa"] for c in completos]
    monotono = all(mapa[completos[i]]["pagina_impresa"]
                   < mapa[completos[i + 1]]["pagina_impresa"]
                   for i in range(len(completos) - 1))
    print(f"páginas pdf: {n}")
    print(f"capítulos con las dos anclas: {len(completos)} de {len(ROMS)}")
    print(f"desfase pdf-impresa: min {min(offs)} · max {max(offs)} (deriva)")
    print(f"páginas impresas monótonas: {monotono}")
    print(json.dumps(mapa, ensure_ascii=False, indent=1))
