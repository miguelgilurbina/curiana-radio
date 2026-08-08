#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — fusionar los dos almacenes de cognados en `2-lengua/cognados.yaml`
============================================================================

Había dos, con esquemas distintos, y ninguno de los dos sabía del otro:

| | `COGNADOS` (arahuaco_comparative) | `COGNADOS_OLIVER` |
|---|---|---|
| entradas | 37 | 16 |
| lenguas | CQ WY LK TN PA **KL** | CQ WY LK TN PA **PJ CAIC** |
| procedencia | **ninguna, 0 de 37** | página, ancla, confianza, duda del autor |
| lo usa el motor | sí (`transducir`, `reconstruir_caquetio`) | no |

Lo de la procedencia es lo grave: el set que alimenta la reconstrucción no cita
nada, y el que sí cita —con la página de Oliver y hasta un campo para las dudas
del propio Oliver— solo lo lee su minador.

QUÉ HACE ESTA MIGRACIÓN
-----------------------
Un solo archivo, con la forma que un cognado **es**: una relación entre lenguas
con procedencia.

- **Las lenguas son un mapa abierto**, no casillas fijas. Así `KL`, `PJ`,
  `CAIC` y el escape hatch `otros` dejan de ser tres soluciones al mismo
  problema: si mañana aparece achagua, entra sin tocar el esquema.
- **El id es estable y no es la glosa española.** Antes la clave era la glosa,
  y por eso existía `rojo_almagre`: un desempate inventado para no chocar con
  `rojo`. Ahora `cognado-NNN` y la glosa es un campo.
- **A las 37 sin procedencia NO se les inventa una.** Van con
  `procedencia: null` y `deuda: sin-procedencia`, para que el validador las
  cuente y la deuda se vea en el tablero en lugar de esconderse en el código.

⚠️ `arahuaco_comparative.COGNADOS` alimenta `transducir()` y
`reconstruir_caquetio()`. Esta migración **no lo borra**: solo emite el YAML.
Cambiar el consumidor es un paso aparte, y antes hay que congelar la salida
actual con un test (ver `tests/test_cognados.py`).

Uso:
    python migrar_cognados.py            # escribe 2-lengua/cognados.yaml
    python migrar_cognados.py --stdout
"""

import argparse
import io
import os
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
SALIDA = os.path.join(REPO, "2-lengua", "cognados.yaml")

# Códigos de lengua → el id de la lengua tal como lo usa el resto del proyecto.
# Se deja el código corto como clave porque es el que usan las reglas de
# transducción (REGLAS_WY_CQ, etc.) y cambiarlo sería un refactor aparte.
LENGUAS = {
    "PA": "proto-arahuaco",
    "CQ": "caquetío",
    "WY": "wayunaiki",
    "LK": "lokono",
    "TN": "taíno",
    "KL": "kalinago",
    "PJ": "paraujano",
    "CAIC": "caicetío",
}


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def _formas(entrada: dict) -> dict:
    """Las formas por lengua, saltando los nulos y el escape hatch."""
    salida = {}
    for codigo in LENGUAS:
        valor = entrada.get(codigo)
        if valor:
            salida[codigo] = valor
    # `otros` era la vía de escape para lenguas sin casilla. Ahora que el mapa
    # es abierto, sus claves entran como cualquier otra.
    for lengua, forma in (entrada.get("otros") or {}).items():
        if forma:
            salida[lengua] = forma
    return salida


def construir():
    sys.path.insert(0, AQUI)
    import arahuaco_comparative as A
    import cognados_oliver as O

    registros = []
    n = 0

    # ── Los 16 de Oliver primero: son los que traen procedencia ────────
    for clave, e in O.COGNADOS_OLIVER.items():
        n += 1
        reg = {
            "id": f"cognado-{n:03d}",
            "glosa": e.get("es") or clave,
            "formas": _formas(e),
            "fuente": "atestiguado",
            "procedencia": {
                "obra": "oliver-1989-cap2",
                "pagina": e.get("pagina"),
                "ancla": e.get("ancla"),
            },
            "confianza": e.get("confianza"),
            "clave_origen": clave,
        }
        if e.get("oliver_duda"):
            reg["duda_del_autor"] = e["oliver_duda"]
        if e.get("no_cognado"):
            reg["no_cognado"] = e["no_cognado"]
        if e.get("nota"):
            reg["nota"] = e["nota"]
        registros.append(reg)

    # ── Los 37 del set curado: sin procedencia, y se dice ──────────────
    for clave, e in A.COGNADOS.items():
        n += 1
        registros.append({
            "id": f"cognado-{n:03d}",
            "glosa": e.get("es") or clave,
            "formas": _formas(e),
            "fuente": "reconstruido",
            "procedencia": None,
            "deuda": "sin-procedencia",
            "clave_origen": clave,
        })

    return registros


def separar_no_cognados(registros):
    """Aparta las entradas con una sola lengua.

    Un cognado es una relación **entre** lenguas: una entrada con una sola
    forma es una palabra suelta que acabó en el sitio equivocado. Hay dos en el
    set curado, y no son el mismo caso:

    - `baruwa` (KL, 'hombre') **ya está en `VOCABULARIO_BASE`** con la misma
      glosa, así que aquí sobra.
    - `quiripa` (CQ, concha-moneda) **no está en ninguna otra parte**: este
      registro es su única constancia en el repo. Borrarlo perdería el dato.

    Por eso no se borran ni se emiten como cognados: van a una sección propia
    con el diagnóstico, y qué hacer con cada uno es decisión aparte.
    """
    sys.path.insert(0, AQUI)
    try:
        from curiana_lexicon import VOCABULARIO_BASE
        lexico = set(VOCABULARIO_BASE)
    except Exception:                                        # noqa: BLE001
        lexico = set()

    cognados, sueltos = [], []
    for r in registros:
        if len(r.get("formas") or {}) >= 2:
            cognados.append(r)
            continue
        forma = next(iter(r["formas"].values()), None)
        r["diagnostico"] = (
            "ya existe en VOCABULARIO_BASE — este registro sobra"
            if forma in lexico else
            "NO está en VOCABULARIO_BASE — este registro es su única "
            "constancia; moverlo al lexicón antes de retirarlo de aquí")
        sueltos.append(r)
    return cognados, sueltos


def duplicados(registros):
    """Mismo par (lengua, forma) en dos cognados distintos.

    `para` ('mar') estaba en los dos almacenes con la misma glosa. No se fusiona
    automáticamente —decidir que dos entradas son la misma es criterio, no
    script— pero sí se reporta.
    """
    vistos = {}
    choques = []
    for r in registros:
        for lengua, forma in r["formas"].items():
            clave = (lengua, str(forma).lower())
            if clave in vistos:
                choques.append((lengua, forma, vistos[clave], r["id"]))
            else:
                vistos[clave] = r["id"]
    return choques


def documento(registros, sueltos):
    con = sum(1 for r in registros if r.get("procedencia"))
    lenguas = sorted({l for r in registros for l in r["formas"]})
    nucleo = sorted(l for l in lenguas if l.isupper())
    return {
        "meta": {
            "generado_por": "curiana_sim/migrar_cognados.py",
            "cognados": len(registros),
            "con_procedencia": con,
            "sin_procedencia": len(registros) - con,
            "lenguas_nucleo": nucleo,
            "lenguas_comparanda": len(lenguas) - len(nucleo),
            "no_son_cognados": len(sueltos),
            "nota": ("Fusión de arahuaco_comparative.COGNADOS (37, sin procedencia) "
                     "y cognados_oliver.COGNADOS_OLIVER (16, con página y ancla). "
                     "Las formas van en un mapa abierto: los códigos en mayúscula "
                     "son el núcleo con reglas de transducción; los nombres en "
                     "minúscula son comparanda citada, y son abiertos a propósito."),
        },
        "cognados": registros,
        "no_son_cognados": sueltos,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    registros, sueltos = separar_no_cognados(construir())
    choques = duplicados(registros)

    texto = yaml.safe_dump(documento(registros, sueltos), allow_unicode=True,
                           sort_keys=False, default_flow_style=False, width=100)
    if args.stdout:
        print(texto)
        return 0

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as fh:
        fh.write(texto)

    con = sum(1 for r in registros if r.get("procedencia"))
    print(f"  → {os.path.relpath(SALIDA, REPO)}: {len(registros)} cognados")
    print(f"     con procedencia: {con}   sin procedencia: {len(registros) - con}")
    if sueltos:
        print(f"\n  ⚠ {len(sueltos)} entrada(s) apartada(s) por tener una sola lengua:")
        for r in sueltos:
            print(f"     {r['id']}  {list(r['formas'].items())}")
            print(f"        {r['diagnostico']}")
    if choques:
        print(f"\n  ⚠ {len(choques)} forma(s) repetida(s) entre cognados distintos:")
        for lengua, forma, a, b in choques:
            print(f"     {lengua} «{forma}»  en {a} y en {b}")
        print("     No se fusionan solas: decidir que dos entradas son la misma")
        print("     es criterio humano. Quedan reportadas.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
