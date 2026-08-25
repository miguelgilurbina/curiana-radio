#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — validador del registro de nodos
=========================================

Valida `3-mundo/asentamientos.yaml`: qué asentamientos existían, cuándo, y con
qué evidencia. Es la pieza que hace posible la **simulación geográficamente
cerrada** de la fase 2 (`3-mundo/esfera-de-interaccion.md` §4).

POR QUÉ NO VIVE EN `compilar_corpus.py`
---------------------------------------
Un nodo no es un hecho del corpus: no tiene `contenido` ni etiqueta epistémica
sobre una afirmación, sino sobre la EXISTENCIA de un lugar y sobre su ÉPOCA.
Meterlo en el corpus obligaría a que `cargar()` supiera de dos esquemas.

Y no vive en `compilar_lengua.py` porque `toponimos.yaml` contesta otra cosa:
"¿qué significa este nombre?". Ahí Adícora, Curaçao y Aruba constan como
`descartado`, que significa "sin etimología despejable" y NO "no existió".

LA VALIDACIÓN QUE JUSTIFICA EL MÓDULO
-------------------------------------
`precontacto: si` **exige** `precontacto_razon`.

Es la única regla que de verdad protege algo. Todo el registro se apoya en
documentos coloniales —la carta de Bastidas es de 1538, once años después del
pacto Ampíes-Manaure— y la simulación es del s. XIV-XV. Sin esta regla,
"atestiguado" se desliza a "precontacto" sin que nadie lo note, que es la
regla 3 de CLAUDE.md incumplida en silencio.

Y su corolario: un nodo con `atestacion: colonial` **no puede** declarar
`precontacto: si`. Un documento de 1538 no prueba nada sobre 1450. Si existe
esa evidencia, será arqueológica, y entonces `atestacion` lo tiene que decir.

Uso:
    python compilar_asentamientos.py            # informe
    python compilar_asentamientos.py --check    # exit 1 si hay errores (CI)
    python compilar_asentamientos.py --json     # el informe en JSON

No modifica el YAML: valida e informa. Misma disciplina que los minadores.
"""

import argparse
import io
import json
import os
import re
import sys
from collections import Counter

import yaml

_AQUI = os.path.dirname(os.path.abspath(__file__))
REGISTRO = os.path.join(_AQUI, "..", "3-mundo", "asentamientos.yaml")
BIBLIOGRAFIA = os.path.join(_AQUI, "..", "4-fuentes", "bibliografia.yaml")
CORPUS_DIR = os.path.join(_AQUI, "..", "3-mundo", "corpus")

RE_ID = re.compile(r"^nodo-\d{3}$")
RE_HECHO = re.compile(r"^[a-z][a-z_]*-\d{3}[a-z]?$")

# Vocabularios cerrados. Un campo con valores libres deja de poder agruparse:
# es el bug de `taíno`/`taino` en el lexicón (issue #93), y no se repite aquí.
ETIQUETAS = ("atestiguado", "reconstruido", "hipotetico")
ATESTACIONES = ("colonial", "precolonial", "arqueologica")
PRECONTACTO = ("si", "probable", "desconocido")
TIPOS = ("asentamiento", "asentamiento-puerto", "asentamiento-palafito",
         "isla", "sitio-arqueologico")
# `sitio-arqueologico` se anadio el 2026-08-24 al fusionar los 17 del
# Apendice E de Oliver (#92). Son sitios de PROSPECCION, no poblados
# nombrados en cronica: llamarlos `asentamiento` afirmaria una funcion
# que el registro arqueologico no da. Cuando la funcion SI se conoce
# (Tara-tara es cementerio, El Manglar son campamentos) vive en `rol`,
# no en `tipo` — el tipo dice que clase de nodo es en la red, el rol
# dice que sabemos de el.
ETIMOLOGIAS = ("resuelto", "sin-resolver", "descartada", "no-aplica")

OBLIGATORIOS = ("id", "forma", "tipo", "region", "etiqueta", "atestacion",
                "precontacto", "rol", "procedencia", "etimologia")


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace",
                line_buffering=True))


def _error(codigo, donde, mensaje):
    return {"nivel": "error", "codigo": codigo, "donde": donde, "mensaje": mensaje}


def _aviso(codigo, donde, mensaje):
    return {"nivel": "aviso", "codigo": codigo, "donde": donde, "mensaje": mensaje}


# ══════════════════════════════════════════════════════════════════════
# CARGA
# ══════════════════════════════════════════════════════════════════════

def cargar(ruta: str = REGISTRO):
    """Devuelve `(nodos, huecos, problemas)`."""
    if not os.path.exists(ruta):
        return [], [], [_error("registro-ausente", ruta,
                               "3-mundo/asentamientos.yaml no existe")]
    try:
        with open(ruta, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
    except yaml.YAMLError as e:
        return [], [], [_error("yaml-invalido", ruta, f"no parsea: {e}")]

    if not isinstance(doc, dict):
        return [], [], [_error("raiz-inesperada", ruta,
                               f"la raíz es {type(doc).__name__}, se esperaba dict")]

    nodos = doc.get("nodos") or []
    huecos = doc.get("huecos") or []
    problemas = []
    if not isinstance(nodos, list):
        problemas.append(_error("nodos-inesperado", ruta,
                                f"`nodos` es {type(nodos).__name__}, se esperaba lista"))
        nodos = []
    return [n for n in nodos if isinstance(n, dict)], huecos, problemas


def _obras_de_la_bibliografia():
    """Los ids de `4-fuentes/bibliografia.yaml`, o None si no existe."""
    if not os.path.exists(BIBLIOGRAFIA):
        return None
    with open(BIBLIOGRAFIA, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    return {o["id"] for o in doc.get("obras", []) if o.get("id")}


def _ids_del_corpus():
    """Los ids de hecho de `3-mundo/corpus/`, o None si no se puede leer."""
    if not os.path.isdir(CORPUS_DIR):
        return None
    ids = set()
    for nombre in sorted(os.listdir(CORPUS_DIR)):
        if not nombre.endswith(".yaml"):
            continue
        try:
            with open(os.path.join(CORPUS_DIR, nombre), encoding="utf-8") as fh:
                datos = yaml.safe_load(fh)
        except yaml.YAMLError:
            continue
        secciones = datos.values() if isinstance(datos, dict) else [datos]
        for entradas in secciones:
            if not isinstance(entradas, list):
                continue
            for e in entradas:
                if isinstance(e, dict) and e.get("id"):
                    ids.add(e["id"])
    return ids


# ══════════════════════════════════════════════════════════════════════
# VALIDACIONES
# ══════════════════════════════════════════════════════════════════════

def validar_estructura(nodos: list) -> list:
    problemas, vistos = [], set()
    for i, nodo in enumerate(nodos):
        nid = nodo.get("id")
        donde = nid or f"nodos[{i}]"

        for campo in OBLIGATORIOS:
            valor = nodo.get(campo)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                problemas.append(_error("campo-ausente", donde,
                                        f"falta el campo obligatorio `{campo}`"))

        if nid and not RE_ID.match(str(nid)):
            problemas.append(_error("id-mal-formado", donde,
                                    f"`{nid}` no tiene la forma `nodo-NNN`"))
        if nid in vistos:
            problemas.append(_error("id-duplicado", donde, f"`{nid}` está repetido"))
        vistos.add(nid)
    return problemas


def validar_vocabularios(nodos: list) -> list:
    """Cada campo cerrado, con su lista cerrada. Sin esto no se puede agrupar."""
    cerrados = (("etiqueta", ETIQUETAS), ("atestacion", ATESTACIONES),
                ("precontacto", PRECONTACTO), ("tipo", TIPOS),
                ("etimologia", ETIMOLOGIAS))
    problemas = []
    for nodo in nodos:
        donde = nodo.get("id", "(sin id)")
        for campo, legales in cerrados:
            valor = nodo.get(campo)
            if valor is not None and valor not in legales:
                problemas.append(_error(
                    f"{campo}-ilegal", donde,
                    f"`{campo}: {valor}` no es legal — solo {', '.join(legales)}"))
    return problemas


def validar_precontacto(nodos: list) -> list:
    """**La regla que justifica este módulo.**

    Afirmar que un asentamiento existía en el s. XIV-XV es la afirmación más
    fuerte del registro y la única que la simulación consume de verdad. No se
    puede hacer de gratis:

    1. `precontacto: si` exige `precontacto_razon`.
    2. `precontacto: si` con `atestacion: colonial` es contradicción: un
       documento de 1538 no dice nada de 1450. Si hay evidencia precontacto,
       será arqueológica, y `atestacion` lo tiene que declarar.
    """
    problemas = []
    for nodo in nodos:
        donde = nodo.get("id", "(sin id)")
        pre = nodo.get("precontacto")
        razon = nodo.get("precontacto_razon")

        if pre == "si" and not (razon and str(razon).strip()):
            problemas.append(_error(
                "precontacto-sin-razon", donde,
                "declara `precontacto: si` sin `precontacto_razon`. La "
                "afirmación más fuerte del registro no se hace de gratis"))

        if pre == "si" and nodo.get("atestacion") == "colonial":
            problemas.append(_error(
                "precontacto-por-documento-colonial", donde,
                "declara `precontacto: si` con `atestacion: colonial`: un "
                "documento colonial no prueba existencia precontacto "
                "(regla 3 de CLAUDE.md)"))

        if pre != "si" and razon:
            problemas.append(_aviso(
                "razon-huerfana", donde,
                f"tiene `precontacto_razon` pero `precontacto: {pre}`"))
    return problemas


def validar_procedencia(nodos: list, obras) -> list:
    """`procedencia.obra` es clave foránea contra la bibliografía."""
    if obras is None:
        return [_aviso("sin-bibliografia", "4-fuentes/bibliografia.yaml",
                       "no existe: las citas no se pueden comprobar. Genérala "
                       "con `python curiana_sim/generar_bibliografia.py`")]
    problemas = []
    for nodo in nodos:
        donde = nodo.get("id", "(sin id)")
        proc = nodo.get("procedencia")
        if proc is None:
            continue
        if not isinstance(proc, dict):
            problemas.append(_error("procedencia-mal-formada", donde,
                                    f"es {type(proc).__name__}, se esperaba dict"))
            continue
        obra = proc.get("obra")
        if not obra:
            problemas.append(_error("procedencia-sin-obra", donde,
                                    "`procedencia` sin campo `obra`"))
        elif obra not in obras:
            problemas.append(_error("obra-fantasma", donde,
                                    f"cita `{obra}`, que no está en la bibliografía"))
    return problemas


def validar_corpus(nodos: list, ids) -> list:
    """Los hechos citados en `corpus:` tienen que existir."""
    if ids is None:
        return [_aviso("sin-corpus", "3-mundo/corpus", "no se pudo leer")]
    problemas = []
    for nodo in nodos:
        donde = nodo.get("id", "(sin id)")
        for hecho in nodo.get("corpus") or []:
            if not RE_HECHO.match(str(hecho)):
                problemas.append(_error("hecho-mal-formado", donde,
                                        f"`{hecho}` no tiene forma `<dominio>-NNN`"))
            elif hecho not in ids:
                problemas.append(_error("hecho-fantasma", donde,
                                        f"cita `{hecho}`, que no está en el corpus"))
    return problemas


def compilar(ruta: str = REGISTRO):
    """Carga, valida y devuelve `(nodos, huecos, problemas)`."""
    nodos, huecos, problemas = cargar(ruta)
    problemas += validar_estructura(nodos)
    problemas += validar_vocabularios(nodos)
    problemas += validar_precontacto(nodos)
    problemas += validar_procedencia(nodos, _obras_de_la_bibliografia())
    problemas += validar_corpus(nodos, _ids_del_corpus())
    return nodos, huecos, problemas


# ══════════════════════════════════════════════════════════════════════
# INFORME
# ══════════════════════════════════════════════════════════════════════

def informe(nodos, huecos, problemas) -> None:
    errores = [p for p in problemas if p["nivel"] == "error"]
    avisos = [p for p in problemas if p["nivel"] == "aviso"]

    print(f"\n── registro de nodos ── {len(nodos)} nodos, {len(huecos)} hueco(s)\n")

    por_region = Counter(n.get("region") for n in nodos)
    for region, n in por_region.most_common():
        print(f"  {region:22} {n}")

    print("\n  por evidencia de precontacto (la que consume la simulación):")
    por_pre = Counter(n.get("precontacto") for n in nodos)
    for valor in PRECONTACTO:
        if por_pre.get(valor):
            print(f"    {valor:14} {por_pre[valor]}")

    utiles = [n.get("forma") for n in nodos if n.get("precontacto") == "si"]
    if utiles:
        print(f"\n  Con precontacto sostenido: {', '.join(utiles)}")
    else:
        print("\n  ⚠ NINGÚN nodo tiene precontacto sostenido.")

    if errores:
        print(f"\n  ✗ {len(errores)} error(es):")
        for p in errores:
            print(f"      [{p['codigo']}] {p['donde']}: {p['mensaje']}")
    if avisos:
        print(f"\n  ⚠ {len(avisos)} aviso(s):")
        for p in avisos:
            print(f"      [{p['codigo']}] {p['donde']}: {p['mensaje']}")
    if not errores:
        print(f"\n  ✓ registro válido — {len(nodos)} nodos, {len(avisos)} aviso(s)\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 si hay errores")
    ap.add_argument("--json", action="store_true", help="el informe en JSON")
    args = ap.parse_args(argv)

    nodos, huecos, problemas = compilar()
    errores = [p for p in problemas if p["nivel"] == "error"]

    if args.json:
        print(json.dumps({"nodos": len(nodos), "huecos": len(huecos),
                          "problemas": problemas}, ensure_ascii=False, indent=2))
    elif args.check:
        if errores:
            print(f"✗ {len(errores)} error(es) en el registro de nodos")
            for p in errores:
                print(f"    [{p['codigo']}] {p['donde']}: {p['mensaje']}")
        else:
            avisos = len(problemas) - len(errores)
            print(f"✓ registro de nodos válido — {len(nodos)} nodos, {avisos} aviso(s)")
    else:
        informe(nodos, huecos, problemas)

    return 1 if (args.check and errores) else 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
