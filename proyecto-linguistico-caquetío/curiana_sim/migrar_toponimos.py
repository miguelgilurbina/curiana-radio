#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — desarmar `lexicon_toponimos.py` en datos consultables
===============================================================

El módulo tenía **doce contenedores de nivel superior** para lo que en realidad
son tres entidades distintas más un puñado de prosa:

    NIVEL_A / NIVEL_B / NIVEL_C / DESCARTES      → topónimos analizados
    MORFEMAS_DESPEJADOS / FORMATIVOS_SIN_GLOSA   → formantes extraídos
    CORROBORACIONES_LEXICON                      → enlaces lexicón ↔ topónimo
    REDUPLICACION / CONFLICTOS / ANTROPONIMOS    → prosa editorial
    TOTALES / FUENTES                            → metadatos

Tres problemas concretos que eso produjo:

1. **El nivel de confianza era un campo disfrazado de tres contenedores.** Para
   preguntar "todos los topónimos" había que unir tres dicts, y añadir un nivel
   significaba crear un contenedor.
2. **`TOTALES` declara `nivel_D: 47` y `NIVEL_D` no existe en el módulo.** Una
   cifra a mano apuntando a nada — justo lo que la regla 1 prohíbe.
3. **`ANTROPONIMOS` no contiene antropónimos**: contiene `total`,
   `con_glosa_descriptiva`, `resueltos`, un `detalle` anidado con los datos, y
   dos campos de prosa (`veredicto`, `consecuencia`). Dato, recuento y opinión
   en la misma estructura.

Y nadie importaba el módulo: 739 líneas de análisis curado que ningún consumidor
leía.

QUÉ EMITE
---------
    2-lengua/toponimos.yaml   los topónimos, con `nivel` como campo
    2-lengua/morfemas.yaml    los formantes, con su estatus

La prosa (`REDUPLICACION`, `CONFLICTOS`, el veredicto de los antropónimos) **no
se migra**: se queda para `2-lengua/toponimia.md`, que es donde vive el
argumento. Un YAML no es sitio para un veredicto.

Uso:
    python migrar_toponimos.py
    python migrar_toponimos.py --stdout
"""

import argparse
import io
import os
import re
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DIR_LENGUA = os.path.join(REPO, "2-lengua")

# La obra que sostiene cada análisis, por el valor del campo `fuente` que traía
# el módulo. Es la clave foránea a 4-fuentes/bibliografia.yaml.
OBRA_POR_FUENTE = {
    "zavala-reyes-2015": "zavala-reyes-2015",
    "van-buurt-2014": "van-buurt-2014",
    "gatschet-1885": "gatschet-1885",
    "esteves-1989": "esteves-1989",
}


def _procedencia(e):
    """`fuente` → clave foránea; `pagina`, si la entrada la trae, viaja dentro."""
    obra = OBRA_POR_FUENTE.get(e.get("fuente"))
    if not obra:
        return None
    proc = {"obra": obra}
    if e.get("pagina") is not None:
        proc["pagina"] = e["pagina"]
    return proc


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def _limpio(d: dict, saltar=()) -> dict:
    return {k: v for k, v in d.items() if k not in saltar and v not in (None, "", [], {})}


def toponimos(T):
    """NIVEL_A/B/C + DESCARTES → una lista con `nivel` como campo."""
    # Los ids son claves que citan otros archivos (índice de Esteves, dictado,
    # lecturas, asentamientos): tienen que ser ESTABLES. Los 74 originales se
    # numeran por orden, como siempre; toda entrada nueva trae su `id`
    # explícito (toponimo-075 en adelante) y no mueve el contador.
    registros = []
    n = 0
    for nivel, contenedor in (("A", T.NIVEL_A), ("B", T.NIVEL_B), ("C", T.NIVEL_C)):
        for forma, e in contenedor.items():
            if e.get("id"):
                rid = e["id"]
            else:
                n += 1
                rid = f"toponimo-{n:03d}"
            reg = {
                "id": rid,
                "forma": forma,
                "nivel": nivel,
                "clase": e.get("clase", "topónimo"),
            }
            reg.update(_limpio(e, saltar=("id", "clase", "fuente", "pagina")))
            reg["procedencia"] = _procedencia(e)
            if not reg["procedencia"]:
                reg["deuda"] = "sin-procedencia"
            registros.append(reg)

    # DESCARTES viene indexado por RAZÓN, con una lista de formas dentro. Se
    # expande a un registro por forma: la unidad es el topónimo, no el motivo.
    # La glosa viene DENTRO de la forma, «dabajuro (Población de Falcón)»: se
    # separa a `glosa_fuente` (el bug de forma, arreglado el 2026-08-30 sobre
    # el YAML y aquí desde el 2026-09-06 para que regenerar no lo deshaga).
    # Las flechas («cemirucos → 'Semerucos'») no son glosa y se quedan.
    # Un grupo de DESCARTES puede traer `fuente` y `paginas` {forma: página}
    # (los de Esteves) y `ids` {forma: id} para no mover el contador.
    for razon, e in T.DESCARTES.items():
        ids = e.get("ids", {})
        paginas = e.get("paginas", {})
        for forma in e.get("formas", []):
            m = re.match(r"^(.+?)\s+\((.+)\)$", forma)
            base = m.group(1) if m else forma
            if base in ids:
                rid = ids[base]
            else:
                n += 1
                rid = f"toponimo-{n:03d}"
            reg = {
                "id": rid,
                "forma": base,
                "nivel": "descartado",
                "clase": "topónimo",
            }
            if m:
                reg["glosa_fuente"] = m.group(2)
            reg["razon"] = e.get("razon") or razon
            reg["procedencia"] = _procedencia({"fuente": e.get("fuente"),
                                               "pagina": paginas.get(base)})
            if not reg["procedencia"]:
                reg["deuda"] = "sin-procedencia"
            registros.append(reg)
    return registros


def morfemas(T):
    """MORFEMAS_DESPEJADOS + FORMATIVOS_SIN_GLOSA → una lista con `estatus`."""
    registros = []
    n = 0
    for forma, e in T.MORFEMAS_DESPEJADOS.items():
        n += 1
        reg = {"id": f"morfema-{n:03d}", "forma": forma, "glosado": True}
        reg.update(_limpio(e))
        registros.append(reg)
    for forma, e in T.FORMATIVOS_SIN_GLOSA.items():
        n += 1
        reg = {"id": f"morfema-{n:03d}", "forma": forma, "glosado": False}
        reg.update(_limpio(e))
        registros.append(reg)
    return registros


def corroboraciones(T):
    """Palabras del lexicón que un topónimo respalda de forma independiente."""
    salida = []
    for palabra, e in T.CORROBORACIONES_LEXICON.items():
        reg = {"palabra": palabra}
        reg.update(_limpio(e))
        salida.append(reg)
    return salida


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args(argv)

    sys.path.insert(0, AQUI)
    import lexicon_toponimos as T

    tops = toponimos(T)
    morfs = morfemas(T)
    corrs = corroboraciones(T)

    por_nivel = {}
    for r in tops:
        por_nivel[r["nivel"]] = por_nivel.get(r["nivel"], 0) + 1

    doc_top = {
        "meta": {
            "generado_por": "curiana_sim/migrar_toponimos.py",
            "toponimos": len(tops),
            "por_nivel": por_nivel,
            "con_procedencia": sum(1 for r in tops if r.get("procedencia")),
            # La tercera voz (2026-09-05): lecturas que cuelgan del topónimo sin
            # pisar glosa_fuente ni segmentacion. Ver datos-de-lengua.md.
            "con_lecturas": sum(1 for r in tops if r.get("lecturas")),
            "lecturas": sum(len(r.get("lecturas") or []) for r in tops),
            "con_definicion_aceptada": sum(1 for r in tops if r.get("definicion_aceptada_simulacion")),
            "corroboraciones_del_lexicon": len(corrs),
            "nota": ("El nivel de confianza es un CAMPO, no un contenedor: "
                     "antes eran NIVEL_A/B/C separados y para listar todos los "
                     "topónimos había que unir tres dicts. La prosa (reduplicación, "
                     "conflictos, veredicto sobre antropónimos) vive en "
                     "2-lengua/toponimia.md, no aquí."),
        },
        "toponimos": tops,
        "corroboraciones_lexicon": corrs,
    }
    doc_mor = {
        "meta": {
            "generado_por": "curiana_sim/migrar_toponimos.py",
            "morfemas": len(morfs),
            "glosados": sum(1 for m in morfs if m["glosado"]),
            "sin_glosa": sum(1 for m in morfs if not m["glosado"]),
        },
        "morfemas": morfs,
    }

    if args.stdout:
        print(yaml.safe_dump(doc_top, allow_unicode=True, sort_keys=False,
                             default_flow_style=False, width=100))
        return 0

    os.makedirs(DIR_LENGUA, exist_ok=True)
    for nombre, doc in (("toponimos.yaml", doc_top), ("morfemas.yaml", doc_mor)):
        ruta = os.path.join(DIR_LENGUA, nombre)
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                                    default_flow_style=False, width=100))
        print(f"  → {os.path.relpath(ruta, REPO)}")

    print(f"\n  topónimos: {len(tops)}  {por_nivel}")
    print(f"  con procedencia: {doc_top['meta']['con_procedencia']}/{len(tops)}")
    print(f"  con lecturas: {doc_top['meta']['con_lecturas']} "
          f"({doc_top['meta']['lecturas']} lecturas; "
          f"{doc_top['meta']['con_definicion_aceptada']} con definición aceptada)")
    print(f"  morfemas: {len(morfs)}  ({doc_mor['meta']['glosados']} glosados)")
    print(f"  corroboraciones del lexicón: {len(corrs)}")
    print("\n  ⚠ La prosa NO se migró (reduplicación, conflictos, veredicto de")
    print("    antropónimos). Va a 2-lengua/toponimia.md.")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
