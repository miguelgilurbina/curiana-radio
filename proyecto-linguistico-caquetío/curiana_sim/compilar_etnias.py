#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — validador del registro de vecinos
===========================================

Valida `3-mundo/etnias.yaml`: qué pueblos están documentados en contacto con
los caquetíos, de qué familia lingüística, con qué tipo de contacto, con qué
polity caquetía y con qué fuente. Es el hermano de `compilar_asentamientos.py`:
aquel dice **dónde** estaba la esfera; este dice **con quién**.

POR QUÉ NO VIVE EN `compilar_corpus.py`
---------------------------------------
Una etnia no es un hecho del corpus: no tiene `contenido` ni etiqueta sobre una
afirmación, sino una ficha de un pueblo (familia, lugar, contacto). Cada vez que
una fuente documenta a los caquetíos conviviendo, comerciando o guerreando con
otro pueblo, ese pueblo entra aquí con su ficha, y el hecho del corpus lo cita.

LA VALIDACIÓN QUE JUSTIFICA EL MÓDULO
-------------------------------------
**Regla 4 de CLAUDE.md, en código.** Casi todo el contacto documentado es de
polities NO costeras: los cuibas en los Llanos, los bubures en Maracaibo, los
ciparicotos en Yaracuy. La simulación modela la polity **costera**. Sin una
regla, un vecino de Barquisimeto se desliza al Golfete sin que nadie lo note,
que es exactamente el error que Oliver denuncia.

1. `polity_caquetia` es obligatorio y de vocabulario cerrado.
2. `polity_caquetia: costera` **exige decisión explícita**: o una
   `procedencia.obra` que documente el contacto con la polity costera, o
   `etiqueta: canon-simulacion` (es del elenco, no un dato). Sin una de las
   dos, un vecino de la Curiana es fanfiction que pasa por dato.
3. `etiqueta: canon-simulacion` exige `deuda: sin-procedencia`: lo inventado
   se declara inventado (regla 8: el hueco se admite, callarlo no).

Y la de siempre: `procedencia.obra` es clave foránea contra la bibliografía, y
`ver_tambien` solo puede apuntar a hechos del corpus o archivos que existan.

Uso:
    python compilar_etnias.py            # informe
    python compilar_etnias.py --check    # exit 1 si hay errores (CI)
    python compilar_etnias.py --json     # el informe en JSON

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
REPO = os.path.dirname(_AQUI)
REGISTRO = os.path.join(REPO, "3-mundo", "etnias.yaml")
BIBLIOGRAFIA = os.path.join(REPO, "4-fuentes", "bibliografia.yaml")
CORPUS_DIR = os.path.join(REPO, "3-mundo", "corpus")

RE_ID = re.compile(r"^etnia-\d{3}$")
RE_HECHO = re.compile(r"^[a-z][a-z_]*-\d{3}[a-z]?$")

# Vocabularios cerrados. Un campo con valores libres deja de poder agruparse:
# es el bug de `taíno`/`taino` en el lexicón (issue #93), y no se repite aquí.
# Lo que no cabe en el valor cerrado va al campo `*_nota` de al lado.
ETIQUETAS = ("atestiguado", "reconstruido", "hipotetico", "canon-simulacion")
FAMILIAS = ("arahuaca", "caribe", "guahibo", "chibcha", "jirajara", "desconocida")
# Las cuatro de `curiana_polities.py` + `occidental` (Maracaibo, Juruara,
# Perijá): la esfera que Oliver §3.2.4 documenta y que el corpus ya usa como
# `polity: occidental` (geografia_politica-009..013). No está modelada en
# `curiana_polities.py`; añadirla allí es canon y decisión humana.
POLITIES = ("costera", "barquisimeto", "yaracuy", "llanos", "occidental")
POLITY_SIMULADA = "costera"
CONTACTOS = ("corresidencia", "vecindad", "mercado", "guerra", "visita", "ninguno")
INTENSIDADES = ("maxima", "alta", "media", "baja", "ninguna", "desconocida")

OBLIGATORIOS = ("id", "nombre", "etiqueta", "familia_linguistica", "donde",
                "polity_caquetia", "tipo_de_contacto", "intensidad")


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
    """Devuelve `(etnias, meta, problemas)`."""
    if not os.path.exists(ruta):
        return [], {}, [_error("registro-ausente", ruta,
                               "3-mundo/etnias.yaml no existe")]
    try:
        with open(ruta, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
    except yaml.YAMLError as e:
        return [], {}, [_error("yaml-invalido", ruta, f"no parsea: {e}")]

    if not isinstance(doc, dict):
        return [], {}, [_error("raiz-inesperada", ruta,
                               f"la raíz es {type(doc).__name__}, se esperaba dict")]

    etnias = doc.get("etnias") or []
    meta = doc.get("meta") or {}
    problemas = []
    if not isinstance(etnias, list):
        problemas.append(_error("etnias-inesperado", ruta,
                                f"`etnias` es {type(etnias).__name__}, se esperaba lista"))
        etnias = []
    return [e for e in etnias if isinstance(e, dict)], meta, problemas


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

def validar_estructura(etnias: list) -> list:
    problemas, vistos, nombres = [], set(), set()
    for i, etnia in enumerate(etnias):
        eid = etnia.get("id")
        donde = eid or f"etnias[{i}]"

        for campo in OBLIGATORIOS:
            valor = etnia.get(campo)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                problemas.append(_error("campo-ausente", donde,
                                        f"falta el campo obligatorio `{campo}`"))

        if eid and not RE_ID.match(str(eid)):
            problemas.append(_error("id-mal-formado", donde,
                                    f"`{eid}` no tiene la forma `etnia-NNN`"))
        if eid in vistos:
            problemas.append(_error("id-duplicado", donde, f"`{eid}` está repetido"))
        vistos.add(eid)

        nombre = etnia.get("nombre")
        if nombre in nombres:
            problemas.append(_error("nombre-duplicado", donde,
                                    f"`{nombre}` ya tiene ficha: es la misma etnia "
                                    "o falta decir por qué son dos"))
        nombres.add(nombre)

        variantes = etnia.get("variantes")
        if variantes is not None and not isinstance(variantes, list):
            problemas.append(_error("variantes-mal-formadas", donde,
                                    "`variantes` tiene que ser una lista"))
    return problemas


def validar_vocabularios(etnias: list) -> list:
    """Cada campo cerrado, con su lista cerrada. Sin esto no se puede agrupar."""
    cerrados = (("etiqueta", ETIQUETAS), ("familia_linguistica", FAMILIAS),
                ("polity_caquetia", POLITIES), ("tipo_de_contacto", CONTACTOS),
                ("intensidad", INTENSIDADES))
    problemas = []
    for etnia in etnias:
        donde = etnia.get("id", "(sin id)")
        for campo, legales in cerrados:
            valor = etnia.get(campo)
            if valor is not None and valor not in legales:
                problemas.append(_error(
                    f"{campo}-ilegal", donde,
                    f"`{campo}: {valor}` no es legal — solo {', '.join(legales)}. "
                    f"El matiz va en `{_nota_de(campo)}`"))
    return problemas


def _nota_de(campo: str) -> str:
    return {"familia_linguistica": "aviso_familia",
            "polity_caquetia": "polity_nota",
            "tipo_de_contacto": "contacto_nota",
            "intensidad": "intensidad_nota",
            "etiqueta": "aviso"}[campo]


def _tiene_obra(etnia: dict) -> bool:
    proc = etnia.get("procedencia")
    return isinstance(proc, dict) and bool(proc.get("obra"))


def validar_polity(etnias: list) -> list:
    """**La regla que justifica este módulo.** Regla 4 de CLAUDE.md.

    La simulación modela la polity costera. Un vecino que se le atribuye es la
    afirmación que la simulación consume de verdad, y no se hace de gratis:

    1. `polity_caquetia: costera` exige `procedencia.obra` (una fuente que
       documente el contacto con ESA polity) o `etiqueta: canon-simulacion`
       (es del elenco: se declara inventado).
    2. `etiqueta: canon-simulacion` exige `deuda: sin-procedencia`. Lo que no
       viene de una fuente lo dice (regla 8).
    3. Y al revés: `deuda: sin-procedencia` junto a una `procedencia.obra` es
       contradicción — o cita o debe, no las dos.
    """
    problemas = []
    for etnia in etnias:
        donde = etnia.get("id", "(sin id)")
        polity = etnia.get("polity_caquetia")
        etiqueta = etnia.get("etiqueta")
        deuda = etnia.get("deuda")

        if polity == POLITY_SIMULADA and not (_tiene_obra(etnia)
                                              or etiqueta == "canon-simulacion"):
            problemas.append(_error(
                "costera-sin-decision", donde,
                "se atribuye a la polity costera (la simulada) sin fuente que "
                "lo documente ni `etiqueta: canon-simulacion`. Nada entra al "
                "Golfete sin decisión explícita (regla 4 de CLAUDE.md)"))

        if etiqueta == "canon-simulacion" and deuda != "sin-procedencia":
            problemas.append(_error(
                "canon-simulacion-sin-deuda", donde,
                "es canon-simulación y no declara `deuda: sin-procedencia`: "
                "lo inventado se declara inventado (regla 8)"))

        if deuda == "sin-procedencia" and _tiene_obra(etnia):
            problemas.append(_error(
                "deuda-con-fuente", donde,
                "declara `deuda: sin-procedencia` y a la vez cita una obra: "
                "o cita o debe, no las dos"))

        if not _tiene_obra(etnia) and deuda != "sin-procedencia":
            problemas.append(_error(
                "sin-procedencia-ni-deuda", donde,
                "no cita obra ni declara `deuda: sin-procedencia` (regla 8: "
                "el hueco se admite, callarlo no)"))
    return problemas


def validar_procedencia(etnias: list, obras) -> list:
    """`procedencia.obra` (y `procedencia.via`) son claves foráneas contra la
    bibliografía."""
    if obras is None:
        return [_aviso("sin-bibliografia", "4-fuentes/bibliografia.yaml",
                       "no existe: las citas no se pueden comprobar. Genérala "
                       "con `python curiana_sim/generar_bibliografia.py`")]
    problemas = []
    for etnia in etnias:
        donde = etnia.get("id", "(sin id)")
        proc = etnia.get("procedencia")
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
        via = proc.get("via")
        if via and via not in obras:
            problemas.append(_error("via-fantasma", donde,
                                    f"cita `via: {via}`, que no está en la bibliografía"))
    return problemas


def _destino(referencia: str) -> str:
    """De `6-fusion/x.yaml#prop-007` o `6-fusion/x.yaml (§5)` saca la ruta."""
    return re.split(r"[#\s(]", str(referencia).strip(), maxsplit=1)[0]


def validar_referencias(etnias: list, ids, repo: str = REPO) -> list:
    """`ver_tambien` es una lista; cada ítem apunta a un hecho del corpus
    (`<dominio>-NNN`) o a un archivo del repo, y tienen que existir."""
    problemas = []
    for etnia in etnias:
        donde = etnia.get("id", "(sin id)")
        refs = etnia.get("ver_tambien")
        if refs is None:
            continue
        if not isinstance(refs, list):
            problemas.append(_error("ver-tambien-mal-formado", donde,
                                    "`ver_tambien` tiene que ser una lista"))
            continue
        for ref in refs:
            ref = str(ref)
            if RE_HECHO.match(ref):
                if ids is None:
                    problemas.append(_aviso("sin-corpus", donde,
                                            f"no se pudo comprobar `{ref}`"))
                elif ref not in ids:
                    problemas.append(_error("hecho-fantasma", donde,
                                            f"cita `{ref}`, que no está en el corpus"))
            else:
                ruta = _destino(ref)
                if not ruta or not os.path.exists(os.path.join(repo, ruta)):
                    problemas.append(_error("archivo-fantasma", donde,
                                            f"cita `{ref}` y `{ruta}` no existe en el repo"))
    return problemas


def compilar(ruta: str = REGISTRO):
    """Carga, valida y devuelve `(etnias, meta, problemas)`."""
    etnias, meta, problemas = cargar(ruta)
    problemas += validar_estructura(etnias)
    problemas += validar_vocabularios(etnias)
    problemas += validar_polity(etnias)
    problemas += validar_procedencia(etnias, _obras_de_la_bibliografia())
    problemas += validar_referencias(etnias, _ids_del_corpus())
    return etnias, meta, problemas


# ══════════════════════════════════════════════════════════════════════
# INFORME
# ══════════════════════════════════════════════════════════════════════

def informe(etnias, meta, problemas) -> None:
    errores = [p for p in problemas if p["nivel"] == "error"]
    avisos = [p for p in problemas if p["nivel"] == "aviso"]

    print(f"\n── registro de vecinos ── {len(etnias)} etnias"
          f" (estado: {meta.get('estado', '?')})\n")

    print("  por polity caquetía (regla 4):")
    por_polity = Counter(e.get("polity_caquetia") for e in etnias)
    for valor in POLITIES:
        if por_polity.get(valor):
            marca = "  ← la simulada" if valor == POLITY_SIMULADA else ""
            print(f"    {valor:14} {por_polity[valor]}{marca}")

    print("\n  por familia lingüística:")
    por_familia = Counter(e.get("familia_linguistica") for e in etnias)
    for valor in FAMILIAS:
        if por_familia.get(valor):
            print(f"    {valor:14} {por_familia[valor]}")

    print("\n  por tipo de contacto:")
    por_contacto = Counter(e.get("tipo_de_contacto") for e in etnias)
    for valor in CONTACTOS:
        if por_contacto.get(valor):
            print(f"    {valor:14} {por_contacto[valor]}")

    costera = [e for e in etnias if e.get("polity_caquetia") == POLITY_SIMULADA]
    if costera:
        print("\n  Tocan la polity costera:")
        for e in costera:
            como = ("canon-simulación" if e.get("etiqueta") == "canon-simulacion"
                    else f"documentado en {e.get('procedencia', {}).get('obra')}")
            print(f"    {e.get('nombre'):22} {como}")
    else:
        print("\n  ⚠ NINGÚN vecino documentado toca la polity costera.")

    if errores:
        print(f"\n  ✗ {len(errores)} error(es):")
        for p in errores:
            print(f"      [{p['codigo']}] {p['donde']}: {p['mensaje']}")
    if avisos:
        print(f"\n  ⚠ {len(avisos)} aviso(s):")
        for p in avisos:
            print(f"      [{p['codigo']}] {p['donde']}: {p['mensaje']}")
    if not errores:
        print(f"\n  ✓ registro válido — {len(etnias)} etnias, {len(avisos)} aviso(s)\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 si hay errores")
    ap.add_argument("--json", action="store_true", help="el informe en JSON")
    args = ap.parse_args(argv)

    etnias, meta, problemas = compilar()
    errores = [p for p in problemas if p["nivel"] == "error"]

    if args.json:
        print(json.dumps({"etnias": len(etnias), "problemas": problemas},
                         ensure_ascii=False, indent=2))
    elif args.check:
        if errores:
            print(f"✗ {len(errores)} error(es) en el registro de vecinos")
            for p in errores:
                print(f"    [{p['codigo']}] {p['donde']}: {p['mensaje']}")
        else:
            avisos = len(problemas) - len(errores)
            print(f"✓ registro de vecinos válido — {len(etnias)} etnias, {avisos} aviso(s)")
    else:
        informe(etnias, meta, problemas)

    return 1 if (args.check and errores) else 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
