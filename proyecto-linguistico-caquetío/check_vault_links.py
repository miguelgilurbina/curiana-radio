#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — verificador de enlaces del vault
==========================================

Comprueba que todo `[[wikilink]]` del vault resuelva a un archivo existente, y
reporta notas de `3-mundo/`, `2-lengua/` o `4-fuentes/` sin ningún enlace
entrante.

Es el guardián del eje VAULT, en el mismo espíritu con que `tests/` guarda el
motor: un vault con enlaces rotos deja de ser un grafo y vuelve a ser markdown
suelto — exactamente lo que el plan quiere evitar (ver PLAN_MAESTRO.md §2).

Uso:
    python check_vault_links.py          # informe
    python check_vault_links.py --strict # exit 1 si hay roto

Reglas que aplica:
  - Un wikilink resuelve por BASENAME en todo el vault (como Obsidian).
  - Los wikilinks dentro de código (``` o `inline`) no cuentan: son ejemplos.
  - Se ignoran .obsidian/, .trash/, __pycache__/, node_modules/ y data/.
"""

import argparse
import collections
import os
import re
import sys

VAULT = os.path.dirname(os.path.abspath(__file__))

# `.claude/` incluye worktrees de git, que duplican el repo entero y hacen que
# todo basename aparezca como ambiguo. Un worktree es una copia de trabajo, no
# contenido del vault.
IGNORAR_DIRS = {"__pycache__", ".obsidian", ".trash", "node_modules", "data",
                ".git", ".claude", ".next", ".pytest_cache"}
EXT_ENLAZABLES = {".md", ".canvas", ".pdf", ".yaml", ".yml", ".py", ".txt"}

# [[destino]] · [[destino|alias]] · [[destino#seccion]]
LINK = re.compile(r"\[\[([^\]\|#]+)(?:[#\|][^\]]*)?\]\]")


def _caminar():
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIRS]
        for f in files:
            yield root, f


def indexar():
    """basename (sin extensión) -> [rutas relativas]

    Se indexa también por `carpeta/basename` (y por la ruta completa sin
    extensión), como hace Obsidian: es la única forma de enlazar sin
    ambigüedad un basename repetido — p. ej. los dos `README.md`.

    Devuelve (idx, claves_por_ruta): `idx` resuelve cualquier clave; el segundo
    mapea cada ruta a todas sus claves, para el informe de huérfanas.
    """
    idx = collections.defaultdict(list)
    claves_por_ruta = {}
    for root, f in _caminar():
        stem, ext = os.path.splitext(f)
        if ext.lower() not in EXT_ENLAZABLES:
            continue
        rel = os.path.relpath(os.path.join(root, f), VAULT)
        partes = rel.replace("\\", "/").split("/")
        sin_ext = "/".join(partes)[: -len(ext)]
        claves = {stem}
        for i in range(1, len(partes)):
            claves.add("/".join(sin_ext.split("/")[i - 1:]))
        for k in claves:
            idx[k].append(rel)
        claves_por_ruta[rel] = claves
    return idx, claves_por_ruta


def sin_codigo(txt):
    txt = re.sub(r"```.*?```", "", txt, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", txt)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="salir con código 1 si hay enlaces rotos")
    args = ap.parse_args()

    idx, claves_por_ruta = indexar()
    rotos = collections.defaultdict(set)
    entrantes = collections.Counter()
    total = 0

    for root, f in _caminar():
        if not f.endswith(".md"):
            continue
        path = os.path.join(root, f)
        with open(path, encoding="utf-8", errors="replace") as fh:
            txt = sin_codigo(fh.read())
        for m in LINK.finditer(txt):
            destino = m.group(1).strip()
            total += 1
            entrantes[destino] += 1
            if destino not in idx:
                rotos[destino].add(os.path.relpath(path, VAULT))

    print("wikilinks: %d   destinos distintos: %d   notas indexadas: %d"
          % (total, len(entrantes), len(claves_por_ruta)))

    if rotos:
        print("\nROTOS (%d):" % len(rotos))
        for destino, origenes in sorted(rotos.items()):
            print("  [[%s]]  <-  %s" % (destino, ", ".join(sorted(origenes))))
    else:
        print("\nOK: todos los wikilinks resuelven")

    ambiguos = {k: v for k, v in idx.items() if len(v) > 1 and k in entrantes}
    if ambiguos:
        print("\nAMBIGUOS (mismo basename en varias rutas, enlazados):")
        for k, v in sorted(ambiguos.items()):
            print("  %s -> %s" % (k, ", ".join(v)))

    vigilados = tuple(os.path.join(d, "") for d in ("2-lengua", "3-mundo", "4-fuentes"))
    huerfanas = sorted(
        r for r, claves in claves_por_ruta.items()
        if r.endswith(".md") and r.startswith(vigilados)
        and not any(k in entrantes for k in claves)
    )
    if huerfanas:
        print("\nSIN ENLACES ENTRANTES: %s" % ", ".join(huerfanas))

    if args.strict and rotos:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
