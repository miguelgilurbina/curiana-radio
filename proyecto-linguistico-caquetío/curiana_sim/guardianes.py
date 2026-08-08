#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — los guardianes, en un solo comando
============================================

El proyecto tiene ocho comprobaciones que miden **contra el dato** y no contra
la documentación. Estaban sueltas, y correrlas dependía de que alguien se
acordara de todas:

    1. tests del motor            pytest curiana_sim/tests/
    2. la suite rápida            python curiana_sim/test_quick.py
    3. el grafo del vault         python check_vault_links.py --strict
    4. el corpus cultural         python curiana_sim/compilar_corpus.py --check
    5. las polities               python curiana_sim/curiana_polities.py --check
    6. la bibliografía al día     python curiana_sim/generar_bibliografia.py --check
    7. los datos de lengua        python curiana_sim/compilar_lengua.py --check
    8. el registro de nodos       python curiana_sim/compilar_asentamientos.py --check

Acordarse de ocho cosas no es un método: es suerte. Esto las corre todas,
informa en una tabla y sale con código ≠ 0 si alguna falla, para que se pueda
colgar de un hook o de CI.

Deliberadamente **no** incluye `generar_tablero.py --check`: el tablero se queda
viejo cada vez que cambia una cifra medida, que es constantemente, y bloquear
por eso sería ruido. Se regenera, no se vigila.

Uso:
    python guardianes.py            # los ocho, informe en tabla
    python guardianes.py --rapido   # salta los tests (los más lentos)
    python guardianes.py --silencio # solo el veredicto, para hooks
"""

import argparse
import io
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
PY = sys.executable

# (nombre, comando, cwd, es_lento)
GUARDIANES = [
    ("tests del motor",
     [PY, "-m", "pytest", os.path.join(AQUI, "tests"), "-q", "--no-header"],
     REPO, True),
    ("suite rápida (8/8)",
     [PY, os.path.join(AQUI, "test_quick.py")],
     AQUI, True),
    ("grafo del vault",
     [PY, os.path.join(REPO, "check_vault_links.py"), "--strict"],
     REPO, False),
    ("corpus cultural",
     [PY, os.path.join(AQUI, "compilar_corpus.py"), "--check"],
     REPO, False),
    ("polities",
     [PY, os.path.join(AQUI, "curiana_polities.py"), "--check"],
     REPO, False),
    ("bibliografía al día",
     [PY, os.path.join(AQUI, "generar_bibliografia.py"), "--check"],
     REPO, False),
    ("datos de lengua",
     [PY, os.path.join(AQUI, "compilar_lengua.py"), "--check"],
     REPO, False),
    ("registro de nodos",
     [PY, os.path.join(AQUI, "compilar_asentamientos.py"), "--check"],
     REPO, False),
]


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def correr(nombre, cmd, cwd):
    """Corre un guardián. Devuelve (ok, segundos, última línea útil)."""
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    t0 = time.time()
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                             encoding="utf-8", errors="replace",
                             timeout=600, env=entorno)
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, "se pasó de 600 s"
    except FileNotFoundError as e:
        return False, time.time() - t0, f"no se pudo ejecutar: {e}"

    texto = (out.stdout or "") + (out.stderr or "")
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    resumen = ""
    for l in reversed(lineas):
        if any(m in l for m in ("passed", "failed", "OK", "✓", "✗", "error",
                                "ERROR", "ROTOS", "válido", "módulos")):
            resumen = l
            break
    if not resumen and lineas:
        resumen = lineas[-1]
    return out.returncode == 0, time.time() - t0, resumen[:78]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rapido", action="store_true", help="salta los lentos")
    ap.add_argument("--silencio", action="store_true", help="solo el veredicto")
    args = ap.parse_args(argv)

    tareas = [g for g in GUARDIANES if not (args.rapido and g[3])]
    if not args.silencio:
        print(f"\n── guardianes ({len(tareas)}) ──\n")

    fallos = []
    for nombre, cmd, cwd, _ in tareas:
        ok, seg, resumen = correr(nombre, cmd, cwd)
        if not ok:
            fallos.append((nombre, resumen))
        if not args.silencio:
            print(f"  {'✓' if ok else '✗'}  {nombre:22} {seg:5.1f}s  {resumen}")

    if fallos:
        print(f"\n  ✗ {len(fallos)} guardián(es) en rojo:")
        for nombre, resumen in fallos:
            print(f"      {nombre}: {resumen}")
        return 1

    if not args.silencio:
        print(f"\n  ✓ los {len(tareas)} en verde\n")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
