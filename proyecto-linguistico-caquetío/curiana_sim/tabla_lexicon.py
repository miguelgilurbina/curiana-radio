#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""LAS CIFRAS DE `2-lengua/lexicon.md`, medidas y escritas en su sitio.

POR QUÉ EXISTE. La nota del lexicón se escribió el 2026-08-04 con las cifras
de ese día («1413 entradas», «781 wayunaiki», «226 atestiguadas») y la wiki
pública la publica tal cual: el 2026-09-24 el lexicón tenía 5.488 entradas y
la nota seguía diciendo 1.413. Regla 1: ninguna cifra a mano. Este script
mide con las MISMAS funciones que el tablero (`generar_tablero.medir_lexicon`
y `medir_quien_sostiene`), para que no haya dos maneras de contar, y reescribe
en la nota sólo lo que va entre marcas:

    <!-- GENERADO por curiana_sim/tabla_lexicon.py: <bloque> -->
    …
    <!-- /GENERADO -->

y las claves `total`, `familia_caquetia`, `sin_cita` y `medido` del
frontmatter. La prosa y la historia fechada de la nota no se tocan.

`generar_tablero.py` lo llama al final, así que se pone al día en cada cierre.

    python curiana_sim/tabla_lexicon.py            # reescribe la nota
    python curiana_sim/tabla_lexicon.py --check    # exit 1 si está vieja
"""
import argparse
import collections
import datetime
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
NOTA = os.path.join(REPO, "2-lengua", "lexicon.md")
MARCA = re.compile(r"(<!-- GENERADO por curiana_sim/tabla_lexicon\.py: (\w+) -->\n)(.*?)(<!-- /GENERADO -->)",
                   re.S)


def _pct(n, total):
    return f"{100 * n / total:.1f}".replace(".", ",") + " %" if total else "—"


def _miles(n):
    return f"{n:,}".replace(",", ".")


def medir():
    if AQUI not in sys.path:
        sys.path.insert(0, AQUI)
    import generar_tablero as T

    lex = T.medir_lexicon()
    familia = lex["familia"]
    total = lex["total"]
    capas = collections.Counter(str(v.get("fuente")) for v in familia.values())
    sin_notas = sorted(k for k, v in familia.items() if not v.get("notas"))
    atest = {k: familia[k] for k in lex["atestiguado"]}
    cuenta, con_notas, huerfanas = T.medir_quien_sostiene({"familia": atest})
    return {"total": total, "normal": lex["normal"], "familia": len(familia),
            "capas": capas, "sin_notas": sin_notas, "atestiguadas": len(atest),
            "sostiene": cuenta, "huerfanas_atest": huerfanas,
            "fuera": len(lex["fuera_del_habla"])}


def bloques(m):
    b = {}
    b["tamano"] = (
        f"**{_miles(m['total'])} entradas activas** en `VOCABULARIO_BASE`, y "
        f"**{_miles(m['fuera'])}** archivadas en `FUERA_DEL_HABLA` (fuera del habla, "
        "con su capa intacta).\n")
    filas = ["| Categoría normalizada | Entradas | % |", "|---|---:|---:|"]
    for cat, n in m["normal"].most_common():
        nombre = f"**{cat}**" if cat == "caquetío" else cat
        filas.append(f"| {nombre} | {_miles(n)} | {_pct(n, m['total'])} |")
    no_caq = m["total"] - m["normal"].get("caquetío", 0)
    b["lenguas"] = ("\n".join(filas) + "\n\n"
                    f"> **{_pct(no_caq, m['total'])} del lexicón no es caquetío**: son "
                    "comparanda, están ahí para reconstruir y medir, no para hablar.\n")
    filas = ["| Etiqueta | n |", "|---|---:|"]
    for capa, n in sorted(m["capas"].items(), key=lambda kv: -kv[1]):
        filas.append(f"| `{capa}` | {n} |")
    b["capas"] = (f"De las **{m['familia']}** entradas de familia caquetía:\n\n" + "\n".join(filas) + "\n\n"
                  f"**{len(m['sin_notas'])} sin `notas`** (sin cita)"
                  + (f": {', '.join('`' + k + '`' for k in m['sin_notas'])}." if m["sin_notas"] else ".") + "\n")
    filas = ["| Obra | Entradas que la citan |", "|---|---:|"]
    for slug, n in m["sostiene"].most_common():
        filas.append(f"| [[{slug}]] | {n} |")
    filas.append(f"| *sin obra reconocida en `notas`* | {len(m['huerfanas_atest'])} |")
    b["sostiene"] = (f"De las **{m['atestiguadas']}** entradas `caquetío-atestiguado`, cuántas "
                     "citan a cada obra en su campo `notas` (una entrada puede citar varias; "
                     "los patrones salen del `autor` y los `aliases` de cada nota de "
                     "`4-fuentes/`, como en el tablero):\n\n" + "\n".join(filas) + "\n")
    return b


def componer(texto, m):
    nuevo_por = bloques(m)

    def sub(mt):
        nombre = mt.group(2)
        if nombre not in nuevo_por:
            raise SystemExit(f"bloque desconocido en la nota: {nombre}")
        return mt.group(1) + nuevo_por[nombre] + mt.group(4)

    cuerpo = MARCA.sub(sub, texto)
    for clave, valor in (("total", m["total"]), ("familia_caquetia", m["familia"]),
                         ("sin_cita", len(m["sin_notas"]))):
        cuerpo = re.sub(rf"^{clave}: .*$", f"{clave}: {valor}", cuerpo, count=1, flags=re.M)
    return cuerpo


def sin_fecha(t):
    return re.sub(r"^medido: .*$", "medido: X", t, count=1, flags=re.M)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    crudo = open(NOTA, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in crudo else "\n"
    texto = crudo.replace(eol, "\n")
    if not MARCA.search(texto):
        print("la nota no tiene bloques GENERADO")
        return 1
    nuevo = componer(texto, medir())
    if args.check:
        if sin_fecha(nuevo) != sin_fecha(texto):
            print("2-lengua/lexicon.md está DESACTUALIZADA: python curiana_sim/tabla_lexicon.py")
            return 1
        print("2-lengua/lexicon.md al día.")
        return 0
    if sin_fecha(nuevo) != sin_fecha(texto):
        nuevo = re.sub(r"^medido: .*$", f"medido: {datetime.date.today().isoformat()}",
                       nuevo, count=1, flags=re.M)
        open(NOTA, "wb").write(nuevo.replace("\n", eol).encode("utf-8"))
        print("escrito: 2-lengua/lexicon.md")
    else:
        print("2-lengua/lexicon.md ya estaba al día.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
