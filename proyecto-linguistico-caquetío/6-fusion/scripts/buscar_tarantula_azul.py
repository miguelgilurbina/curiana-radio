# -*- coding: utf-8 -*-
"""¿Dice ALGO de la tarántula (o de las arañas) alguna fuente del repo?

Miguel, 2026-09-22: la tarántula azul «sí o sí tuvo que ser una especie muy
importante». Este script mide si hay rastro de una relación humana —nombre,
uso, creencia— en el material que el proyecto ya tiene. Regla 6: un cero mide
la consulta, así que se buscan varias raíces (araña, tarántula, arácnido,
spider, «pollera», la «araña mona» del habla venezolana) y se imprime el
contexto de cada acierto para leerlo, no para contarlo.

Los PDF se leen con pymupdf (capa de texto; el OCR de Esteves ya está en .txt).

Uso:  python 6-fusion/scripts/buscar_tarantula_azul.py [--contexto]
"""
import glob
import io
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
F = os.path.join(R, "fuentes_caquetios")

# «arana» sin eñe sólo en minúscula: en mayúscula es el capitán Arana de Castellanos, y
# dentro de palabra es Guaranao. Por eso va con límite de palabra y sin re.I en esa rama.
PATRON = re.compile(r"\b(?:[Aa]raña|arana)s?\b|(?i:tar[aá]ntul|\bar[aá]cn|arachn|\bspiders?\b|\bpollera\b)")

TEXTOS = sorted(glob.glob(os.path.join(F, "Esteves_1989_*.ocr.txt"))) + [
    os.path.join(F, "VanBuurt_2014_CaquetioWords_Papiamentu.txt"),
    os.path.join(F, "Castellanos_1857_Elegias_partes_I-II_texto.txt"),
    os.path.join(F, "Gatschet_1885_Aruba_texto.txt"),
    os.path.join(F, "Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt"),
    os.path.join(R, "6-fusion", "medina_colina_dictado.yaml"),
    os.path.join(R, "6-fusion", "sitios_era2.yaml"),
    os.path.join(R, "6-fusion", "capubana_agua_y_microclima.yaml"),
    os.path.join(R, "3-mundo", "corpus", "creencia.yaml"),
    os.path.join(R, "3-mundo", "corpus", "ecologia.yaml"),
    os.path.join(R, "3-mundo", "corpus", "transmision.yaml"),
]
PDFS = [
    os.path.join(F, "Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf"),
    os.path.join(F, "Arcaya_1920_Historia_Estado_Falcon.pdf"),
    os.path.join(F, "Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf"),
    os.path.join(F, "Antolinez_1946_Hacia_el_indio_y_su_mundo.pdf"),
    os.path.join(F, "Jahn_1927_Aborigenes_Occidente_Venezuela.pdf"),
]


def _texto_pdf(ruta):
    import pymupdf
    doc = pymupdf.open(ruta)
    return "\n".join(f"\f[pdf {i + 1}]\n" + p.get_text() for i, p in enumerate(doc))


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = argv or sys.argv[1:]
    ver = "--contexto" in argv
    fuentes = [(p, lambda p=p: io.open(p, encoding="utf-8", errors="replace").read()) for p in TEXTOS if os.path.exists(p)]
    fuentes += [(p, lambda p=p: _texto_pdf(p)) for p in PDFS if os.path.exists(p)]
    for ruta, leer in fuentes:
        t = leer()
        ms = list(PATRON.finditer(t))
        formas = sorted({m.group(0).lower() for m in ms})
        print(f"{os.path.relpath(ruta, R):75s} {len(ms):3d}  {formas}")
        if ver:
            for m in ms:
                pdf = t.rfind("[pdf ", 0, m.start())
                pag = t[pdf:pdf + 12].split("]")[0] + "]" if pdf >= 0 else ""
                print("   ", pag, re.sub(r"\s+", " ", t[max(0, m.start() - 160): m.end() + 200]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
