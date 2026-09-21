# -*- coding: utf-8 -*-
"""Extrae el CONTROL no arahuaco (jirajara / ayomán de Jahn 1927) a YAML.

Se ejecuta a mano y su salida se commitea:

    python 6-fusion/scripts/_extraer_control_jirajarano.py

Lo usa `cruce_taino_caquetio.py` como lista de control: dos listas cortas de
lenguas con fonología parecida SIEMPRE dan parecidos, y hace falta saber
cuántos da una lengua que NO es pariente.

⚠️ POR QUÉ ESTO ES CONTROL Y NUNCA COMPARANDA. El bloque de Jahn sale de
`pdftotext -layout` sobre un escaneo y, a partir de cierta fila de la p. 389,
las columnas DERIVAN: la glosa de una fila queda al lado de la forma de otra.
Para una comparanda eso es fatal. Para un control es inofensivo —incluso
conservador—, porque una glosa mal pegada a una forma es exactamente lo que
hace un modelo nulo. Este archivo no entra al lexicón ni a cognados.yaml.
"""
import io
import os
import re
import subprocess
import sys
import tempfile

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PDF = os.path.join(R, "fuentes_caquetios", "Jahn_1927_Aborigenes_Occidente_Venezuela.pdf")
SALIDA = os.path.join(R, "6-fusion", "control_jirajarano_jahn_1927.yaml")


def paginas_del_vocabulario(texto):
    """Las planas cuyo encabezado es ESPAÑOL | JIRAJARA | AYOMÁN."""
    out = []
    for pg in texto.split("\f"):
        if re.search(r"ESPA[NÑ]OL\s+JIRAJARA", pg):
            out.append(pg)
    return out


def filas_de(pg):
    """Filas de tres columnas que arrancan en el margen.

    La regla de corte está declarada: se toma la línea sólo si empieza en la
    columna 0 o 1 (la glosa castellana está donde debe) y tiene al menos dos
    celdas separadas por dos espacios o más. Las líneas con la primera celda
    vacía son justo donde empieza la deriva de columnas y se descartan.
    """
    cab = re.search(r"ESPA[NÑ]OL\s+JIRAJARA.*\n", pg)
    cuerpo = pg[cab.end():] if cab else ""
    out = []
    for ln in cuerpo.split("\n"):
        if not ln.strip() or len(ln.rstrip()) < 6:
            continue
        if re.match(r"\s*(\(\d\)|\d{3}\s|DEL OCC|LOS ABOR|ESPA|Vocabulario|[A-Z]\.\s)", ln):
            continue
        if len(ln) - len(ln.lstrip()) > 1:      # primera celda vacía: deriva
            continue
        celdas = [c for c in re.split(r"\s{2,}", ln.strip()) if c]
        if len(celdas) < 2:
            continue
        glosa = celdas[0].strip(" .·")
        if not re.search(r"[a-záéíóúñ]", glosa.lower()) or len(glosa) > 34:
            continue
        out.append({
            "castellano": glosa,
            "jirajara": celdas[1].strip(" .“”"),
            "ayoman": celdas[2].strip(" .“”") if len(celdas) > 2 else None,
        })
    return out


def main():
    with tempfile.TemporaryDirectory() as tmp:
        txt = os.path.join(tmp, "jahn.txt")
        subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", PDF, txt], check=True)
        texto = io.open(txt, encoding="utf-8", errors="replace").read()

    filas, paginas = [], paginas_del_vocabulario(texto)
    for pg in paginas:
        filas.extend(filas_de(pg))
    # el mismo lema dos veces (la tabla repite cabeceras) se queda una
    vistos, unicas = set(), []
    for f in filas:
        k = (f["castellano"].lower(), f["jirajara"])
        if k in vistos:
            continue
        vistos.add(k)
        unicas.append(f)

    salida = {
        "meta": {
            "obra": "jahn-1927",
            "que_es": ("Vocabulario jirajara de Siquisique comparado con el ayomán, "
                       "Jahn 1927 pp. impresas 388-391. Lengua JIRAJAROIDE: no arahuaca "
                       "y sin filiación chibcha sostenida (ver 6-fusion/tabla_a8_jirajarano.yaml)."),
            "para_que": ("CONTROL DE AZAR de 6-fusion/scripts/cruce_taino_caquetio.py. "
                         "Nunca comparanda: no entra al lexicón ni a 2-lengua/cognados.yaml."),
            "generado_por": "6-fusion/scripts/_extraer_control_jirajarano.py",
            "receta": "pdftotext -enc UTF-8 -layout; filas de 3 columnas que arrancan en el margen",
            "advertencia": ("A partir de cierta fila de la p. 389 las columnas DERIVAN en el "
                            "escaneo: una glosa puede quedar junto a la forma de otra fila. Para "
                            "una comparanda sería fatal; para un control es conservador, porque una "
                            "glosa mal pegada a una forma es lo que hace un modelo nulo."),
            "planas_leidas": len(paginas),
            "filas": len(unicas),
        },
        "vocabulario": unicas,
    }
    cab = (
        "# ══════════════════════════════════════════════════════════════════════\n"
        "# CONTROL NO ARAHUACO — jirajara/ayomán (Jahn 1927, pp. 388-391)\n"
        "# GENERADO por 6-fusion/scripts/_extraer_control_jirajarano.py.\n"
        "# Es una LISTA DE CONTROL, no comparanda: ver meta.advertencia.\n"
        "# ══════════════════════════════════════════════════════════════════════\n"
    )
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(cab)
        yaml.safe_dump(salida, fh, allow_unicode=True, sort_keys=False, width=100)
    print(f"planas {len(paginas)} · filas {len(unicas)} -> {os.path.relpath(SALIDA, R)}")
    for f in unicas[:10]:
        print(f"  {f['castellano']:<20} {f['jirajara']:<16} {f['ayoman']}")


if __name__ == "__main__":
    main()
