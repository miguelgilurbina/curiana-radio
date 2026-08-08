#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la huella de la base: contra qué corrió cada run
===========================================================

Hoy, mirando un run en la base, **no se puede saber sobre qué lexicón corrió**.
Hubo que reconstruirlo de git para poder analizar los seis primeros, y por eso
[[LINEA_DE_TIEMPO]] existe: para saber qué resultados siguen valiendo.

Esto sella esa información **en el momento de arrancar**, en la propia fila del
run. Es la precondición de todo lo demás: sin ella, dos runs no son comparables
y ningún resultado es citable.

QUÉ SELLA
---------
    lexicon_hash   SHA-256 de VOCABULARIO_BASE serializado y ordenado
    lexicon_n      cuántas entradas tenía
    corpus_hash    hash de los YAML de 3-mundo/corpus/
    corpus_n       cuántos hechos
    agentes_hash   hash del elenco (importa: el prompt de cada agente
                   predice su score, r=-0.48)
    agentes_n      cuántos agentes
    motor_commit   el SHA del HEAD al arrancar
    motor_sucio    si había cambios sin commitear
    polity         qué formación política modela el motor
    semilla        para poder repetir

POR QUÉ `motor_sucio` IMPORTA MÁS DE LO QUE PARECE
--------------------------------------------------
**Un run con el árbol sucio no es citable.** El commit dice una cosa y el código
que corrió decía otra, y no hay forma de recuperar cuál. No se impide correrlo
—hay motivos legítimos para probar algo sin commitear— pero queda marcado, y el
análisis puede excluirlo.

POR QUÉ `agentes_hash` NO ESTABA EN EL ISSUE Y SÍ DEBERÍA
---------------------------------------------------------
El issue #68 pedía lexicón, corpus y motor. Falta el elenco, y es el que más
sesga: medido sobre los 23 runs, **la longitud del `system_prompt` de un agente
predice su score con r = -0.48**. Si alguien reescribe una ficha entre dos runs,
los scores cambian sin que nada más haya cambiado. Sin este hash, ese cambio es
invisible.

Uso:
    python huella_de_base.py            # la huella de ahora mismo
    python huella_de_base.py --json
"""

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def _sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def _hash_dict(d: dict) -> str:
    """Hash estable de un dict: ordenado y con separadores fijos.

    Sin `sort_keys` el hash cambiaría según el orden de inserción, que en
    Python depende del orden del archivo fuente — y entonces mover una entrada
    de sitio parecería un cambio de contenido.
    """
    return _sha(json.dumps(d, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"), default=str))


def _git(*args):
    try:
        out = subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                             text=True, encoding="utf-8", timeout=15)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:                                        # noqa: BLE001
        return None


def huella(semilla=None) -> dict:
    """La huella de la base tal como está en este momento."""
    sys.path.insert(0, AQUI)
    datos = {}

    # ── lexicón ────────────────────────────────────────────────────────
    try:
        from curiana_lexicon import VOCABULARIO_BASE
        datos["lexicon_hash"] = _hash_dict(VOCABULARIO_BASE)
        datos["lexicon_n"] = len(VOCABULARIO_BASE)
    except Exception as e:                                   # noqa: BLE001
        datos["lexicon_hash"] = None
        datos["lexicon_error"] = str(e)[:120]

    # ── corpus ─────────────────────────────────────────────────────────
    try:
        from compilar_corpus import compilar
        hechos, _, _ = compilar()
        limpio = [{k: v for k, v in h.items() if not k.startswith("_")}
                  for h in hechos]
        datos["corpus_hash"] = _hash_dict({"hechos": limpio})
        datos["corpus_n"] = len(hechos)
    except Exception as e:                                   # noqa: BLE001
        datos["corpus_hash"] = None
        datos["corpus_error"] = str(e)[:120]

    # ── elenco ─────────────────────────────────────────────────────────
    try:
        from curiana_agents import ALL_AGENTS
        datos["agentes_hash"] = _hash_dict(ALL_AGENTS)
        datos["agentes_n"] = len(ALL_AGENTS)
        # La longitud total de los prompts, porque es la variable que más
        # sesga el score y conviene tenerla a la vista sin recalcularla.
        datos["prompt_chars"] = sum(
            len(a.get("system_prompt") or "") for a in ALL_AGENTS.values())
    except Exception as e:                                   # noqa: BLE001
        datos["agentes_hash"] = None
        datos["agentes_error"] = str(e)[:120]

    # ── polity ─────────────────────────────────────────────────────────
    try:
        from curiana_polities import POLITY_SIMULADA
        datos["polity"] = POLITY_SIMULADA
    except Exception:                                        # noqa: BLE001
        datos["polity"] = None

    # ── motor ──────────────────────────────────────────────────────────
    datos["motor_commit"] = _git("rev-parse", "HEAD")
    estado = _git("status", "--porcelain")
    datos["motor_sucio"] = bool(estado) if estado is not None else None
    datos["motor_rama"] = _git("rev-parse", "--abbrev-ref", "HEAD")

    if semilla is not None:
        datos["semilla"] = semilla
    return datos


def resumen(h: dict) -> str:
    """Una línea legible para el log del run."""
    sucio = " ⚠ ÁRBOL SUCIO" if h.get("motor_sucio") else ""
    commit = (h.get("motor_commit") or "?")[:8]
    return (f"lexicón {h.get('lexicon_n', '?')} ({(h.get('lexicon_hash') or '?')[:8]}) · "
            f"corpus {h.get('corpus_n', '?')} · "
            f"elenco {h.get('agentes_n', '?')} · "
            f"polity {h.get('polity', '?')} · "
            f"{commit}{sucio}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    h = huella()
    if args.json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
        return 0

    print("\n── Huella de la base ──\n")
    for k, v in h.items():
        print(f"  {k:16} {v}")
    print(f"\n  {resumen(h)}")
    if h.get("motor_sucio"):
        print("\n  ⚠ El árbol tiene cambios sin commitear. Un run lanzado así")
        print("    NO es citable: el commit dice una cosa y el código que corre")
        print("    dice otra, y no hay forma de recuperar cuál.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
