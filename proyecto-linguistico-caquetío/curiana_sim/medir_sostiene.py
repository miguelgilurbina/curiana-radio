#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — qué sostiene de verdad cada obra, medido
==================================================

El frontmatter de las 30 notas de fuente lleva un campo `sostiene`
(`{hechos_corpus: 15, entradas_lexicon: 2}`) que **se mantiene a mano**. Como
toda cifra a mano en este proyecto, deriva: se mina una fuente, se olvida
actualizar el número, y el tablero informa de un estado que ya no es.

Esto lo cuenta contra el dato, en las **cuatro esferas** donde una obra puede
dejar rastro:

    lexicón     entradas de VOCABULARIO_BASE que la citan en `notas`
    corpus      hechos de 3-mundo/corpus/ que la citan en `referencia`
    cognados    2-lengua/cognados.yaml, vía `procedencia.obra`
    topónimos   2-lengua/toponimos.yaml, vía `procedencia.obra`

POR QUÉ IMPORTA MÁS DE LO QUE PARECE
------------------------------------
Una minería no debería alimentar solo el lexicón. Oliver cap. 3 dio geografía
política, guerra, economía y religión; Jahn dio parentesco y un mapa de
polities. Si la única cuenta que llevamos es «entradas del lexicón», el trabajo
que va a las otras esferas **no se ve**, y lo que no se ve no se prioriza.

Este informe hace visible esa asimetría: qué obras alimentan varias esferas y
cuáles solo una.

⚠️ **Dos calidades de medida, y conviene no confundirlas.**

Cognados y topónimos se miden por **clave foránea** (`procedencia.obra`): es
exacto. Lexicón y corpus se miden por **coincidencia del apellido del autor**
sobre campos de texto libre, y eso falla en las dos direcciones:

- **por defecto**, si la cita está escrita de otra forma («vía Zavala p.60» sí,
  pero «Boletín Antropológico 89» no);
- **por exceso**, si el apellido aparece en prosa sin ser una cita.

O sea: los números de esas dos columnas son una **estimación**, no una cuenta.
Sirven para ver desfases grandes y para ordenar por magnitud, no para escribir
«esta obra sostiene exactamente N entradas».

Esa ambigüedad es precisamente el argumento para migrar corpus y lexicón a
`procedencia.obra`, como ya están cognados y topónimos: entonces la cuenta sería
exacta en las cuatro esferas.

Uso:
    python medir_sostiene.py             # tabla por obra
    python medir_sostiene.py --esferas   # qué esfera alimenta cada obra
    python medir_sostiene.py --desfase   # frontmatter declarado vs. medido
"""

import argparse
import io
import os
import re
import sys
from collections import defaultdict

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
FUENTES = os.path.join(REPO, "4-fuentes")

_FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def cargar_yaml(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def obras():
    """id → {patrones de búsqueda, declarado}. Los patrones salen de la propia
    nota (`autor` + `aliases`), no de una lista cableada."""
    doc = cargar_yaml(os.path.join(FUENTES, "bibliografia.yaml"))
    if not doc:
        raise RuntimeError("falta 4-fuentes/bibliografia.yaml — genérala primero")

    salida = {}
    for o in doc["obras"]:
        claves = set()
        apellido = str(o.get("autor", "")).split(",")[0].strip()
        if len(apellido) >= 4 and apellido.lower() != "varios":
            claves.add(apellido)
        for alias in o.get("aliases") or []:
            if len(str(alias).strip()) >= 5:
                claves.add(str(alias).strip())
        salida[o["id"]] = {"claves": claves, "obra": o.get("obra", "")}

    # El `sostiene` declarado, para poder medir el desfase.
    for nombre in os.listdir(FUENTES):
        if not nombre.endswith(".md"):
            continue
        with open(os.path.join(FUENTES, nombre), encoding="utf-8") as fh:
            m = _FM.match(fh.read())
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        if fm.get("tipo") == "fuente" and nombre[:-3] in salida:
            salida[nombre[:-3]]["declarado"] = fm.get("sostiene") or {}
    return salida


def _cita(texto: str, claves) -> bool:
    return any(k.lower() in texto.lower() for k in claves)


def medir():
    datos = obras()
    cuenta = {oid: defaultdict(int) for oid in datos}

    # ── lexicón (texto libre: cota inferior) ───────────────────────────
    sys.path.insert(0, AQUI)
    try:
        from curiana_lexicon import VOCABULARIO_BASE
        for entrada in VOCABULARIO_BASE.values():
            notas = str(entrada.get("notas", "")) + str(entrada.get("glosa_fuente", ""))
            if not notas.strip():
                continue
            for oid, d in datos.items():
                if d["claves"] and _cita(notas, d["claves"]):
                    cuenta[oid]["lexicon"] += 1
    except Exception as e:                                   # noqa: BLE001
        print(f"  ⚠ no se pudo leer el lexicón: {e}")

    # ── corpus ─────────────────────────────────────────────────────────
    # Mixto a propósito: si el hecho ya tiene `procedencia.obra`, se usa esa
    # (exacta) y no se adivina por apellido. Los 58 migrados cuentan bien; los
    # 103 que aún citan en prosa siguen siendo estimación. Conforme avance la
    # migración, esta columna se vuelve exacta sola.
    exactos = 0
    try:
        from compilar_corpus import compilar as compilar_corpus
        hechos, _, _ = compilar_corpus()
        for h in hechos:
            obra = (h.get("procedencia") or {}).get("obra")
            if obra:
                if obra in cuenta:
                    cuenta[obra]["corpus"] += 1
                    exactos += 1
                continue
            texto = " ".join(str(h.get(c, "")) for c in
                             ("referencia", "contenido", "implicacion_simulacion"))
            for oid, d in datos.items():
                if d["claves"] and _cita(texto, d["claves"]):
                    cuenta[oid]["corpus"] += 1
        if hechos:
            print(f"  ({exactos}/{len(hechos)} hechos del corpus se cuentan por "
                  f"clave foránea; el resto, por apellido)")
    except Exception as e:                                   # noqa: BLE001
        print(f"  ⚠ no se pudo leer el corpus: {e}")

    # ── cognados y topónimos (clave foránea: exacto) ───────────────────
    for archivo, seccion, esfera in (
            ("cognados.yaml", "cognados", "cognados"),
            ("toponimos.yaml", "toponimos", "toponimos")):
        doc = cargar_yaml(os.path.join(REPO, "2-lengua", archivo))
        for r in (doc or {}).get(seccion, []):
            obra = (r.get("procedencia") or {}).get("obra")
            if obra in cuenta:
                cuenta[obra][esfera] += 1

    return datos, cuenta


ESFERAS = ("lexicon", "corpus", "cognados", "toponimos")


def informe(datos, cuenta):
    print("\n── Qué sostiene cada obra, medido ──")
    print(f"  {'obra':28} {'lex':>5} {'corp':>5} {'cogn':>5} {'topo':>5}  esferas")
    filas = sorted(datos, key=lambda o: -sum(cuenta[o].values()))
    for oid in filas:
        c = cuenta[oid]
        total = sum(c.values())
        if not total:
            continue
        n_esf = sum(1 for e in ESFERAS if c[e])
        print(f"  {oid:28} {c['lexicon']:>5} {c['corpus']:>5} "
              f"{c['cognados']:>5} {c['toponimos']:>5}  {'●' * n_esf}")

    mudas = [o for o in datos if not sum(cuenta[o].values())]
    if mudas:
        print(f"\n  sin rastro medible ({len(mudas)}): {', '.join(sorted(mudas))}")
        print("  (puede ser que no se haya minado, o que su cita esté escrita")
        print("   de una forma que la búsqueda por apellido no atrapa)")


def informe_esferas(datos, cuenta):
    print("\n── Cuántas esferas alimenta cada obra ──")
    print("  Una minería que solo toca el lexicón está desaprovechando la fuente.\n")
    por_n = defaultdict(list)
    for oid in datos:
        n = sum(1 for e in ESFERAS if cuenta[oid][e])
        por_n[n].append(oid)
    for n in sorted(por_n, reverse=True):
        etiqueta = {0: "ninguna", 1: "una sola", 2: "dos", 3: "tres", 4: "las cuatro"}[n]
        print(f"  {etiqueta:12} ({len(por_n[n]):2d}): {', '.join(sorted(por_n[n])[:6])}"
              + (" …" if len(por_n[n]) > 6 else ""))


def informe_desfase(datos, cuenta):
    print("\n── Declarado en el frontmatter vs. medido ──")
    print("  `sostiene` se mantiene a mano; esto enseña cuánto ha derivado.\n")
    hay = False
    for oid, d in sorted(datos.items()):
        dec = d.get("declarado") or {}
        dl = dec.get("hechos_corpus")
        dx = dec.get("entradas_lexicon")
        ml, mx = cuenta[oid]["corpus"], cuenta[oid]["lexicon"]
        if dl is None and dx is None:
            continue
        if (dl is not None and dl != ml) or (dx is not None and dx != mx):
            hay = True
            print(f"  {oid:28} corpus dec={dl} med={ml}   lexicón dec={dx} med={mx}")
    if not hay:
        print("  sin desfases detectables.")
    print("\n  ⚠ Lexicón y corpus se miden por coincidencia del apellido sobre")
    print("    texto libre, y eso falla en las DOS direcciones: por defecto si")
    print("    la cita está escrita de otra forma, y por exceso si el apellido")
    print("    aparece en prosa sin ser cita. Son estimación, no cuenta.")
    print("    Cognados y topónimos sí son exactos: van por clave foránea.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--esferas", action="store_true")
    ap.add_argument("--desfase", action="store_true")
    args = ap.parse_args(argv)

    datos, cuenta = medir()
    if args.esferas:
        informe_esferas(datos, cuenta)
    elif args.desfase:
        informe_desfase(datos, cuenta)
    else:
        informe(datos, cuenta)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
