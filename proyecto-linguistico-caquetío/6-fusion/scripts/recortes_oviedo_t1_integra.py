#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Recortes de la copia ÍNTEGRA de Oviedo t. I para verificar en imagen las
formas que T1 dejó `ocr-sin-imagen` (dp.3.21 de #222: «la verificación entra
con dp.3.03»).

Por qué hace falta: el PDF viejo del t. I está truncado y perdió la imagen
de las impresas 155-618 (6-fusion/taino_oviedo_valdes_1851.yaml
§meta.estado_del_pdf); T1 leyó esas formas sólo en el OCR. M3 (#206) bajó la
copia íntegra: fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf,
con impresa = pdf − 120 contando desde 1 (M3 escribe «− 119» contando desde
0, como pymupdf).

Qué hace: para cada (forma, página impresa) pedida, busca en la capa de texto
de esa página cualquiera de las grafías que la lista maestra da para la voz
(`formas_atestiguadas`), recorta la línea encontrada con margen y monta los
recortes en láminas PNG numeradas, con el número de página y la grafía
buscada al lado. La lectura la hace quien mira la lámina: este script NO
decide nada (el OCR sólo sirve para localizar; skill leer-fuente §7).

Uso:
    python 6-fusion/scripts/recortes_oviedo_t1_integra.py --salida DIR [--por-lamina 6]
Lee la lista de pares de `dp.3.21_pendientes_de_imagen` de
6-fusion/para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml.
"""
import argparse
import io
import os
import re
import sys
import unicodedata

import pymupdf
import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PDF = os.path.join(R, "fuentes_caquetios", "Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf")
LISTA = os.path.join(R, "6-fusion", "taino_lista_maestra_2026-09-22.yaml")
PROPUESTA = os.path.join(R, "6-fusion", "para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml")
# M3 midió «impresa = pdf − 119» contando las páginas desde 0 (índice de
# pymupdf). Contando desde 1, como el visor de PDF, es pdf − 120. Comprobado
# el 2026-09-24 en las cabeceras de las impresas 143, 265, 471 y 530.
DESFASE = 119   # índice 0 de pymupdf = impresa + 119


def plano(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("ç", "c")


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True)
    ap.add_argument("--por-lamina", type=int, default=6)
    a = ap.parse_args(argv)
    os.makedirs(a.salida, exist_ok=True)

    lm = yaml.safe_load(io.open(LISTA, encoding="utf-8"))
    grafias = {v["lema"]: sorted({str(f) for f in (v.get("formas_atestiguadas") or [])} | {v["lema"]})
               for v in lm["voces"]}
    prop = yaml.safe_load(io.open(PROPUESTA, encoding="utf-8"))
    sec = prop["dp.3.21_pendientes_de_imagen"]
    # las que faltan por mirar y, para poder repetir la lectura, las ya miradas
    pares = sorted({(c["forma"], str(c["pagina"])) for c in (sec.get("citas") or [])}
                   | {(c["forma"], str(c["pagina"])) for c in (sec.get("pares_mirados_en_la_integra") or [])},
                   key=lambda x: (int(x[1]), x[0]))

    doc = pymupdf.open(PDF)
    recortes = []
    for lema, pag in pares:
        pdf_i = int(pag) + DESFASE              # índice 0
        page = doc[pdf_i]
        palabras = page.get_text("words")
        buscadas = [plano(g) for g in grafias.get(lema, [lema])]
        hits = []
        for w in palabras:
            t = plano(re.sub(r"[^\wçÇ]", "", w[4]))
            if len(t) >= 3 and any(t.startswith(b[:max(3, len(b) - 1)]) or b.startswith(t) and len(t) >= len(b) - 1
                                   for b in buscadas):
                hits.append(w)
        if not hits:
            print(f"  p. {pag} ({lema}): SIN LOCALIZAR en la capa de texto — mirar la página entera")
            clip = page.rect
        else:
            w = hits[0]
            clip = pymupdf.Rect(page.rect.x0, max(page.rect.y0, w[1] - 30), page.rect.x1, min(page.rect.y1, w[3] + 30))
        pix = page.get_pixmap(dpi=170, clip=clip)
        recortes.append((lema, pag, pdf_i + 1, len(hits), pix, grafias.get(lema, [lema])))
        print(f"  p. {pag} (pdf {pdf_i + 1}) {lema}: {len(hits)} coincidencia(s) en la capa")

    n = 0
    for i in range(0, len(recortes), a.por_lamina):
        grupo = recortes[i:i + a.por_lamina]
        ancho = max(r[4].width for r in grupo) + 260
        alto = sum(r[4].height + 12 for r in grupo)
        lam = pymupdf.open()
        hoja = lam.new_page(width=ancho, height=alto)
        y = 0
        for lema, pag, pdfn, nh, pix, gr in grupo:
            hoja.insert_text((6, y + 16), f"p.{pag}", fontsize=13)
            hoja.insert_text((6, y + 34), f"pdf {pdfn}", fontsize=9)
            hoja.insert_text((6, y + 50), lema, fontsize=11)
            hoja.insert_text((6, y + 66), "/".join(gr)[:40], fontsize=7)
            hoja.insert_image(pymupdf.Rect(250, y, 250 + pix.width, y + pix.height), pixmap=pix)
            y += pix.height + 12
        n += 1
        out = os.path.join(a.salida, f"lamina_{n:02d}.png")
        lam[0].get_pixmap(dpi=72).save(out)
        print(f"lámina {out}: " + ", ".join(f"p.{r[1]} {r[0]}" for r in grupo))


if __name__ == "__main__":
    main()
