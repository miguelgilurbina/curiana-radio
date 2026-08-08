#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — rellenar `word_uses.source_language` en los runs ya corridos
======================================================================

`word_source_language()` era un lookup pelado contra `VOCABULARIO_BASE`, así
que toda forma flexionada se guardó con `source_language = NULL`. Medido sobre
la base local el 2026-08-06:

    27.641 de 54.936 usos (50,3%) sin lengua
    y el 100% de ellos, formas morfológicamente complejas
      18.752 con sufijo de aspecto (-ka/-ni/-da)
       5.049 otros compuestos con guion
       3.840 con prefijo posesivo (ta-/pi-/nü-)

O sea: **justo los usos que prueban que los agentes manejan la morfología**
quedaron fuera de cualquier análisis por lengua. La función ya está arreglada
(usa `_familia_de_token`), pero los 23 runs históricos siguen con el hueco.

Este script lo rellena **sin volver a correr nada**: recalcula la lengua de
cada forma distinta y actualiza solo las filas con NULL.

⚠️ Es una migración de datos. Por defecto **no escribe**: enseña qué haría.
Para aplicarla de verdad hay que pasar `--aplicar`, y conviene tener el
`supabase db dump` del día antes.

Uso:
    python backfill_word_uses.py              # simulacro, no toca nada
    python backfill_word_uses.py --aplicar
    python backfill_word_uses.py --verificar  # cuenta cuánto queda en NULL
"""

import argparse
import io
import subprocess
import sys

CONTENEDOR = "supabase_db_curiana_sim"


def psql(sql: str, csv: bool = True) -> str:
    cmd = ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres"]
    if csv:
        cmd.append("--csv")
    cmd += ["-c", sql]
    out = subprocess.run(cmd, capture_output=True, text=True,
                         encoding="utf-8", timeout=300)
    if out.returncode != 0:
        raise RuntimeError(f"psql falló: {out.stderr.strip()[:400]}")
    return out.stdout


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def formas_sin_lengua() -> list:
    salida = psql("SELECT DISTINCT word FROM word_uses WHERE source_language IS NULL;")
    lineas = [l.strip() for l in salida.splitlines()[1:] if l.strip()]
    return lineas


def resolver(formas: list) -> dict:
    sys.path.insert(0, __import__("os").path.dirname(__file__))
    from curiana_database import word_source_language
    mapa = {}
    for f in formas:
        lang = word_source_language(f)
        if lang:
            mapa[f] = lang
    return mapa


def _sql_escape(s: str) -> str:
    return s.replace("'", "''")


def construir_update(mapa: dict) -> str:
    """Un solo UPDATE ... FROM (VALUES ...), que es mucho más rápido que 1016."""
    vals = ",\n  ".join(
        f"('{_sql_escape(w)}', '{_sql_escape(l)}')" for w, l in sorted(mapa.items()))
    return (
        "UPDATE word_uses AS u SET source_language = v.lang\n"
        "FROM (VALUES\n  " + vals + "\n) AS v(word, lang)\n"
        "WHERE u.word = v.word AND u.source_language IS NULL;")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aplicar", action="store_true",
                    help="escribe de verdad (por defecto es simulacro)")
    ap.add_argument("--verificar", action="store_true",
                    help="solo cuenta cuántos usos siguen sin lengua")
    args = ap.parse_args(argv)

    if args.verificar:
        print(psql("""
            SELECT count(*) FILTER (WHERE source_language IS NULL) AS sin_lengua,
                   count(*) AS total,
                   round(100.0*count(*) FILTER (WHERE source_language IS NULL)
                         / nullif(count(*),0), 2) AS pct_null
            FROM word_uses;"""))
        return 0

    formas = formas_sin_lengua()
    print(f"\n  formas distintas sin lengua: {len(formas)}")
    if not formas:
        print("  nada que hacer.")
        return 0

    mapa = resolver(formas)
    irresolubles = [f for f in formas if f not in mapa]
    print(f"  se resuelven: {len(mapa)}")
    print(f"  siguen sin resolver: {len(irresolubles)}"
          + (f"  (ej.: {irresolubles[:8]})" if irresolubles else ""))

    from collections import Counter
    reparto = Counter(mapa.values())
    print("\n  a qué lengua irían:")
    for lang, n in reparto.most_common():
        print(f"     {lang:26} {n:5d} formas")

    filas = psql(
        "SELECT count(*) FROM word_uses WHERE source_language IS NULL;"
    ).splitlines()[1].strip()
    print(f"\n  filas afectadas (usos, no formas): hasta {filas}")

    if not args.aplicar:
        print("\n  ── SIMULACRO ── no se ha escrito nada.")
        print("     Para aplicarlo: python backfill_word_uses.py --aplicar")
        print("     Antes conviene: cd curiana_sim && supabase db dump -f respaldo.sql")
        return 0

    print("\n  aplicando…")
    psql(construir_update(mapa), csv=False)
    print(psql("""
        SELECT count(*) FILTER (WHERE source_language IS NULL) AS sin_lengua,
               count(*) AS total
        FROM word_uses;"""))
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
