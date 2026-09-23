#!/usr/bin/env python3
"""`waitiao` se queda caquetío-atestiguado, con la nota de lo que no se ha verificado.

DECISIÓN (Miguel, 2026-09-22, db.5 de `6-fusion/decisiones_base_2026-09-22.yaml`):
«En cuanto a guaitiao, si no está confirmado que no está en Oviedo y no sabemos si
es taína mantengámosla no más pero con ese foot note.»

QUÉ SE APLICA: una nota al final de `notas`. Ni `fuente`, ni `sig`, ni la forma:
`notas` no llega al prompt, así que esto no es corte (se comprueba con la huella
del pre-vuelo antes y después).

QUÉ SE MIDIÓ (2026-09-22): `guaitiao`/`guatiao`/`waitiao`/`guaytiao` 0 en la capa
de texto de los cuatro tomos de Oviedo (pymupdf, modo reparación) y 0 en la
Apologética de Las Casas; la lista maestra taína (#198) la trae sólo de Brinton
1871 y Goeje 1939, sin cronista.

Uso:  python 6-fusion/scripts/anotar_waitiao.py [--dry-run]
"""
import argparse
import io
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEX = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
MARCA = "(2026-09-22, db.5"
NOTA = (
    " · ⚠ Nota (2026-09-22, db.5, Miguel: «si no está confirmado que no está en Oviedo y no "
    "sabemos si es taína, mantengámosla no más pero con ese foot note»): la cita a Oviedo NO "
    "está verificada. Medido: `guaitiao`/`guatiao`/`waitiao` dan 0 en la capa de texto de los "
    "cuatro tomos de Oviedo (ed. Amador de los Ríos) — pero allí las voces indígenas van en "
    "cursiva y el OCR falla justo en ellas, así que el cero no es una ausencia probada —; 0 en "
    "la Apologética de Las Casas; la lista maestra taína la trae sólo de Brinton 1871 p. 12 y "
    "Goeje 1939 p. 9, sin cronista. Es el caso de `datihao`, que resultó ser de San Juan: si "
    "aparece en Oviedo en un pasaje de las islas, se re-etiqueta"
)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    t = io.open(LEX, encoding="utf-8").read()
    if MARCA in t:
        print("ya aplicado; nada que hacer")
        return 0
    ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
    fin = t.index("REGLAS_ASPECTO", ini)
    ms = list(re.finditer(r'^    "waitiao":\s*\{.*\},\s*$', t[ini:fin], re.M))
    assert len(ms) == 1, len(ms)
    a, b = ini + ms[0].start(), ini + ms[0].end()
    linea = t[a:b]
    assert '"fuente": "caquetío-atestiguado"' in linea
    m = re.search(r'"notas":\s*"((?:[^"\\]|\\.)*)"', linea)
    nueva = linea[:m.end(1)] + NOTA.replace('"', "'") + linea[m.end(1):]
    print("  waitiao  nota al final de `notas` (etiqueta y glosa intactas)")
    if args.dry_run:
        print("--dry-run: no se escribe nada")
        return 0
    io.open(LEX, "w", encoding="utf-8", newline="\n").write(t[:a] + nueva + t[b:])
    print("escrito")
    return 0


if __name__ == "__main__":
    sys.exit(main())
