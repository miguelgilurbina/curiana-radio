#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — qué sabían unos de otros en 1492-1500: el barrido medido
==================================================================

Segunda campaña del taíno, parcela **T7** (2026-09-22). Emite las cifras que
citan `6-fusion/taino2_etnohistoria_contacto.yaml` y su issue. **Ninguna cifra
de esos documentos está escrita a mano** (regla 1): salen de aquí.

No escribe nada en el repo: sólo lee las cinco obras y cuenta.

QUÉ MIDE
--------
1. **La ortografía, ANTES de contar** (skill `minar-fuente` §2). Cada diana se
   busca por la raíz corta y sobre el texto NORMALIZADO (NFD sin marcas), no
   por la palabra entera: el escaneo de Anglería parte palabras y pierde
   acentos, y una consulta a cero mediría la consulta, no la fuente (regla 6).
   Se declaran los positivos de control: si `interprete` sale 0 en un texto
   donde `lengua` sale decenas de veces, el cero es de la consulta.

2. **Las cinco preguntas de la parcela**, cada una con su familia de dianas:
   guanín · lo que los isleños decían del sur · lo que la costa decía del
   norte · la lengua y los intérpretes · los caribes y la ruta.

3. **Dónde cae cada acierto**: la página PDF y, cuando el texto la lleva, la
   página impresa. En Anglería el desfase es constante y se declara abajo, no
   se recalcula por acierto.

4. **El negativo que sostiene el veredicto**: en qué TRAMO de cada obra caen
   los aciertos de `intérprete`. Si los once de Anglería vol. 1 caen todos
   antes del libro que narra Paria y Curiana, el cero de ese tramo está medido.

Uso:
    python 6-fusion/scripts/medir_taino2_etnohistoria.py
    python 6-fusion/scripts/medir_taino2_etnohistoria.py --json
    python 6-fusion/scripts/medir_taino2_etnohistoria.py --obra angleria-v1
"""

import argparse
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
FUENTES = os.path.join(REPO, "fuentes_caquetios")

# ── Las obras ────────────────────────────────────────────────────────────
# `desfase` = página impresa − página PDF, medido una vez y fijado aquí
# (skill §3: se calcula una vez, no por acierto). None = el texto no viene
# paginado por saltos de página (los .txt de archive.org llevan el folio
# impreso dentro del flujo).
OBRAS = {
    "angleria-v1": {
        "archivo": "Angleria_1892_Fuentes_Historicas_Colon_America_vol1.pdf",
        "obra": "angleria-1892 vol. 1",
        "desfase": -64,
        "tramos": {"hasta el libro VII (Española y Cuba)": (1, 320),
                   "libros VII-IX (Paria, Curiana, Pinzón)": (321, 460)},
    },
    "angleria-v4": {
        "archivo": "Angleria_1892_Fuentes_Historicas_Colon_America_vol4.pdf",
        "obra": "angleria-1892 vol. 4",
        "desfase": -8,
        "tramos": {"décadas VII-VIII (Lucayas, Chicora)": (1, 200),
                   "resto (Chiribichi, Cumaná)": (201, 492)},
    },
    # ⚠️ Las Casas NO lleva desfase constante: el PDF del repo es el ebook de
    # Project Gutenberg y su pie de página es un contador propio, no el folio
    # de 1875 (lo midió T2 el 2026-09-21). Una cita se ancla por CAPÍTULO con
    # `6-fusion/scripts/mapa_capitulos_las_casas.py`, y la página impresa
    # dentro del capítulo es interpolación declarada. Aquí `desfase: None`
    # para que el medidor no invente un número.
    "las-casas-v1": {
        "archivo": "Las_Casas_1875_Historia_Indias_vol1.pdf",
        "obra": "las-casas-1875 vol. 1",
        "desfase": None,
        "tramos": {"prólogo y libro I hasta el descubrimiento": (1, 330),
                   "el primer viaje (Diario parafraseado)": (331, 500),
                   "aparato y notas": (501, 614)},
    },
    "colon-hernando": {
        "archivo": "Colon_Hernando_1892_Historia_del_Almirante_vol2.txt",
        "obra": "colon-hernando-1892 vol. 2",
        "desfase": None,
        "tramos": {},
    },
    "navarrete-t3": {
        "archivo": "Navarrete_1829_Coleccion_Viages_t3_Viages_Menores_Vespucio.txt",
        "obra": "navarrete-1829-viages-menores",
        "desfase": None,
        "tramos": {},
    },
    "navarrete-t1": {
        "archivo": "Navarrete_1859_Coleccion_Viages_t1_Viages_de_Colon.txt",
        "obra": "navarrete-1859-viages-colon",
        "desfase": None,
        "tramos": {},
    },
}

# ── Las dianas, por pregunta de la parcela ───────────────────────────────
# Cada diana es una RAÍZ corta y sin acentos. El texto se normaliza antes.
PREGUNTAS = {
    "control-de-la-consulta": [
        "isla", "oro", "indio", "cacique", "rescat",
    ],
    "1-guanin": [
        "guanin", "guani", "oro baxo", "oro bajo", "oro muy bajo", "turey",
        "espejo de oro", "aguila de guanin", "alhajas de oro", "oro no puro",
    ],
    "2-lo-que-los-isleños-decian-del-sur": [
        "babeque", "caribana", "caritaba", "bohio", "matinin", "carib",
        "canib", "gran can", "tierra.firme", "tierra firme", "cibao",
        "cyguayo", "cigua", "lucay", "yucay",
    ],
    "3-lo-que-la-costa-decia-del-norte": [
        "paria", "curian", "coquibacoa", "cuchibacoa", "quinquibacoa",
        "cauchie", "cumana", "chiribich", "manacapana", "haraia",
        "san roman", "s. roman", "gigante", "margarita", "perla",
    ],
    "4-lengua-e-interpretes": [
        "interpret", "lengua", "entend", "no los entend", "no se entend",
        "por se.as", "se.alar", "ase.al", "faraute", "trujaman", "truchiman",
        "ladino", "tener lengua",
    ],
    "5-caribes-y-ruta": [
        "canoa", "almad.a", "remo", "piragua", "flecha envenenada",
        "yerba", "armada de canoas", "renclera",
    ],
}


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def normaliza(s):
    """NFD y fuera las marcas: `Caquetío` y `Caquet´ıo` colapsan en lo mismo."""
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def patron(diana):
    """🔴 Un espacio literal en la diana vale CERO en el OCR de archive.org.

    Los `_djvu.txt` separan las palabras con DOS espacios, y los PDF escaneados
    meten saltos de línea dentro de la frase. `no se entendian` devolvía 0 en el
    texto donde está la frase entera (regla 6: el cero medía la consulta). Cada
    espacio de una diana se convierte aquí en `\\s+`, una sola vez y para todas.
    """
    return r"\s+".join(diana.split(" "))


def cargar(clave, cache):
    """Devuelve el texto de la obra. Los PDF pasan por pdftotext (nunca pypdf:
    ver la trampa de CLAUDE.md), y el resultado se cachea en el temporal."""
    ficha = OBRAS[clave]
    origen = os.path.join(FUENTES, ficha["archivo"])
    if not os.path.exists(origen):
        return None, f"no está en el repo: {ficha['archivo']}"
    if origen.lower().endswith(".txt"):
        with open(origen, "rb") as fh:
            crudo = fh.read()
    else:
        if not shutil.which("pdftotext"):
            return None, "pdftotext no está en el PATH"
        destino = os.path.join(cache, clave + ".txt")
        if not os.path.exists(destino):
            subprocess.run(["pdftotext", "-enc", "UTF-8", origen, destino],
                           check=True)
        with open(destino, "rb") as fh:
            crudo = fh.read()
    try:
        return crudo.decode("utf-8"), None
    except UnicodeDecodeError:
        return crudo.decode("latin-1"), None


def paginas_pdf(texto):
    """Límites de cada página PDF (separadas por salto de página)."""
    cortes, pos = [], 0
    for i, trozo in enumerate(texto.split("\f"), start=1):
        cortes.append((pos, pos + len(trozo), i))
        pos += len(trozo) + 1
    return cortes


def pagina_de(cortes, off):
    for ini, fin, i in cortes:
        if ini <= off <= fin:
            return i
    return -1


def medir_obra(clave, cache):
    ficha = OBRAS[clave]
    texto, error = cargar(clave, cache)
    if texto is None:
        return {"obra": ficha["obra"], "error": error}
    plano = normaliza(texto)
    cortes = paginas_pdf(texto)
    paginada = len(cortes) > 1
    salida = {
        "obra": ficha["obra"],
        "archivo": ficha["archivo"],
        "caracteres": len(texto),
        "paginas_pdf": len(cortes) if paginada else None,
        "desfase_impresa_menos_pdf": ficha["desfase"],
        "preguntas": {},
    }
    for pregunta, dianas in PREGUNTAS.items():
        filas = []
        for diana in dianas:
            aciertos = list(re.finditer(patron(diana), plano, re.I))
            fila = {"diana": diana, "n": len(aciertos)}
            if paginada and aciertos:
                pags = sorted({pagina_de(cortes, m.start()) for m in aciertos})
                fila["pdf"] = pags
                if ficha["desfase"] is not None:
                    fila["impresa"] = [p + ficha["desfase"] for p in pags]
            filas.append(fila)
        salida["preguntas"][pregunta] = filas
    # El negativo por tramos: dónde caen los aciertos de intérprete
    if paginada and ficha["tramos"]:
        reparto = {}
        for diana in ("interpret", "curian", "paria", "guanin"):
            aciertos = [pagina_de(cortes, m.start())
                        for m in re.finditer(patron(diana), plano, re.I)]
            reparto[diana] = {
                nombre: sum(1 for p in aciertos if a <= p <= b)
                for nombre, (a, b) in ficha["tramos"].items()
            }
        salida["reparto_por_tramo"] = reparto
    return salida


def imprimir(resultados):
    for r in resultados:
        print("=" * 74)
        print(r["obra"])
        if r.get("error"):
            print("  ⚠️ " + r["error"])
            continue
        print(f"  {r['archivo']}  ·  {r['caracteres']:,} caracteres"
              f"  ·  {r['paginas_pdf'] or '—'} páginas PDF"
              f"  ·  desfase impresa−pdf: {r['desfase_impresa_menos_pdf']}")
        for pregunta, filas in r["preguntas"].items():
            print(f"\n  ── {pregunta} ──")
            for f in filas:
                linea = f"    {f['diana']:<22} {f['n']:>4}"
                if f.get("impresa"):
                    muestra = f["impresa"][:14]
                    cola = " …" if len(f["impresa"]) > 14 else ""
                    linea += f"   impresa: {muestra}{cola}"
                elif f.get("pdf"):
                    muestra = f["pdf"][:14]
                    cola = " …" if len(f["pdf"]) > 14 else ""
                    linea += f"   pdf: {muestra}{cola}"
                print(linea)
        if r.get("reparto_por_tramo"):
            print("\n  ── reparto por tramo (el negativo medido) ──")
            for diana, tramos in r["reparto_por_tramo"].items():
                print(f"    {diana}")
                for nombre, n in tramos.items():
                    print(f"      {nombre:<48} {n:>4}")
        print()


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--obra", choices=sorted(OBRAS), action="append",
                    help="mide sólo esta obra (repetible)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    claves = args.obra or list(OBRAS)
    cache = os.path.join(tempfile.gettempdir(), "curiana_taino2_t7")
    os.makedirs(cache, exist_ok=True)
    resultados = [medir_obra(c, cache) for c in claves]
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        imprimir(resultados)
    return 0


if __name__ == "__main__":
    sys.exit(main())
