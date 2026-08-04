#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — cruce de las adjudicaciones del censo de citas (insumo de F1)
=======================================================================

Las entradas de familia caquetía de `VOCABULARIO_BASE` **sin `notas`** son la
deuda que el eje FIDELIDAD persigue: palabras marcadas como caquetío sin una
sola cita detrás (PLAN_MAESTRO.md §1, tarea F1). Eran 82 al abrir el vault.

Este script **no las arregla**: cruza lo que cada minería dijo sobre ellas y
emite un veredicto sugerido por palabra, para que F1 adjudique con evidencia en
vez de degradar por defecto. Lee cuatro propuestas:

    lexicon_alvarado.AUDITORIA_82      (F3)
    lexicon_gatschet.COBERTURA_82      (F4)
    lexicon_van_buurt.COBERTURA_82     (F6)
    investigacion/fuentes/zavala-reyes-2015.md, secciones A-E   (F7)

La lista de palabras **se recalcula** desde el lexicón en cada corrida, no está
cableada: a medida que F1 aplique citas, el censo se encoge solo.

Uso:
    python auditar_82.py                # informe completo
    python auditar_82.py --resumen      # solo los totales
    python auditar_82.py --pendientes   # solo lo que ninguna fuente resuelve
"""

import argparse
import collections
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
NOTA_ZAVALA = os.path.join(REPO, "investigacion", "fuentes", "zavala-reyes-2015.md")

# Clases de veredicto, de mejor a peor para el lexicón.
CONFIRMA = "CONFIRMA"          # hay cita y sostiene la etiqueta caquetía
REVISAR = "REVISAR"            # la fuente la roza (prosa, mención) — no es cita léxica
RECLASIFICA = "RECLASIFICA"    # la fuente dice que es de OTRA lengua
CONFLICTO = "CONFLICTO_GLOSA"  # la fuente la tiene, pero con otro significado
SIN_RASTRO = "SIN_RASTRO"      # ninguna de las cuatro la encuentra

# Marcas de que la fuente NO dice nada útil. Se buscan en cualquier posición:
# van Buurt escribe "sin rastro en van Buurt 2014", no "sin rastro" a secas.
_NEGATIVO = re.compile(
    r"(?i)(no[ -](resuelta|concluyente)|no en |sin rastro|falso positivo|no aparece)"
)
# Marcas de que la roza pero no la cita: hay que mirarlo a mano.
_TIBIO = re.compile(r"(?i)(menci[oó]n en prosa|revisar si|abierto|ambigu)")


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con § o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def censo_actual():
    """Entradas de familia caquetía sin `notas`, recalculadas del lexicón."""
    sys.path.insert(0, AQUI)
    import curiana_lexicon as L
    voc = L.VOCABULARIO_BASE
    familia = [k for k, v in voc.items()
               if "caquet" in str(v.get("fuente", "")).lower()]
    return sorted(k for k in familia if not voc[k].get("notas")), voc


def _texto_veredicto(valor):
    if isinstance(valor, dict):
        for clave in ("veredicto", "resultado", "estado"):
            if clave in valor:
                return str(valor[clave])
        return "; ".join("%s=%s" % (k, v) for k, v in list(valor.items())[:3])
    return str(valor)


def _clasificar(texto):
    bajo = texto.lower()
    # Lo que contradice o matiza se evalúa ANTES de descartar por negativo:
    # "no resuelta como caquetío, es cumanagoto" sí dice algo.
    if "reclasific" in bajo or "hacia abajo" in bajo or "falso amigo" in bajo:
        return RECLASIFICA
    if "conflicto" in bajo:
        return CONFLICTO
    if _NEGATIVO.search(texto):
        return None
    if _TIBIO.search(texto):
        return REVISAR
    return CONFIRMA


def leer_propuestas():
    """{palabra: [(sigla_fuente, clase, texto), ...]}"""
    sys.path.insert(0, AQUI)
    dichos = collections.defaultdict(list)

    modulos = [("A", "lexicon_alvarado", "AUDITORIA_82"),
               ("G", "lexicon_gatschet", "COBERTURA_82"),
               ("V", "lexicon_van_buurt", "COBERTURA_82")]
    for sigla, nombre, atributo in modulos:
        try:
            mod = __import__(nombre)
        except ImportError:
            print("  (aviso: falta %s.py — esa minería no se cruza)" % nombre,
                  file=sys.stderr)
            continue
        for palabra, valor in getattr(mod, atributo, {}).items():
            texto = _texto_veredicto(valor)
            clase = _clasificar(texto)
            if clase:
                dichos[palabra].append((sigla, clase, texto))

    for palabra, clase, texto in _leer_zavala():
        dichos[palabra].append(("Z", clase, texto))
    return dichos


def _leer_zavala():
    """La adjudicación de F7 vive en markdown, por secciones A-E."""
    if not os.path.exists(NOTA_ZAVALA):
        return
    with open(NOTA_ZAVALA, encoding="utf-8") as fh:
        lineas = fh.read().split("\n")

    seccion = None
    dentro = False
    for linea in lineas:
        if linea.startswith("## Cobertura de las 82"):
            dentro = True
            continue
        if dentro and linea.startswith("## "):
            break
        if not dentro:
            continue
        m = re.match(r"### ([A-E])\.", linea)
        if m:
            seccion = m.group(1)
            continue
        if seccion in ("A", "B", "C"):
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if len(celdas) >= 3 and celdas[0].startswith("`"):
                palabra = celdas[0].strip("`")
                # La última columna («fuerza») es la que marca los conflictos de
                # glosa; leer solo nº y siglas los perdía.
                texto = " · ".join(c for c in celdas[1:] if c)
                yield palabra, _clasificar(texto) or CONFIRMA, texto[:110]
        elif seccion == "D":
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if len(celdas) >= 2 and celdas[0].startswith("`"):
                yield celdas[0].strip("`"), RECLASIFICA, "falso amigo: %s" % celdas[1][:70]
        elif seccion == "E":
            for palabra in re.findall(r"`([^`]+)`", linea):
                yield palabra, "__nada__", ""


def veredicto(dichos_de_una):
    """Prioridad: reclasificar y los conflictos mandan sobre confirmar."""
    clases = [c for _, c, _ in dichos_de_una if c != "__nada__"]
    if RECLASIFICA in clases:
        return RECLASIFICA
    if CONFLICTO in clases:
        return CONFLICTO
    if CONFIRMA in clases:
        return CONFIRMA
    if REVISAR in clases:
        return REVISAR
    return SIN_RASTRO


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resumen", action="store_true", help="solo los totales")
    ap.add_argument("--pendientes", action="store_true",
                    help="solo lo que ninguna fuente resuelve")
    args = ap.parse_args()
    _forzar_utf8()

    palabras, voc = censo_actual()
    dichos = leer_propuestas()

    filas = []
    for palabra in palabras:
        de_esta = dichos.get(palabra, [])
        filas.append((palabra, veredicto(de_esta), de_esta))

    por_clase = collections.Counter(v for _, v, _ in filas)

    if not args.resumen:
        for clase, titulo in ((RECLASIFICA, "RECLASIFICAN — la fuente contradice la etiqueta caquetía"),
                              (CONFLICTO, "CONFLICTO DE GLOSA — la fuente la tiene con otro significado"),
                              (CONFIRMA, "CONFIRMAN — hay cita que sostiene la entrada"),
                              (REVISAR, "A REVISAR A MANO — la fuente la roza, pero no es cita léxica"),
                              (SIN_RASTRO, "SIN RASTRO — ninguna de las cuatro minerías la encuentra")):
            if args.pendientes and clase != SIN_RASTRO:
                continue
            del_grupo = [f for f in filas if f[1] == clase]
            if not del_grupo:
                continue
            print("\n" + "=" * 78)
            print("  %s  (%d)" % (titulo, len(del_grupo)))
            print("=" * 78)
            for palabra, _, de_esta in del_grupo:
                siglas = "".join(sorted({s for s, c, _ in de_esta if c != "__nada__"})) or "—"
                detalle = next((t for _, c, t in de_esta if c != "__nada__"), "")
                print("  %-12s [%-4s] %-42s %s"
                      % (palabra, siglas, voc[palabra]["sig"][:42], detalle[:52]))

    total = len(filas)
    adjudicadas = total - por_clase[SIN_RASTRO]
    print("\n" + "=" * 78)
    print("  CENSO: %d entradas de familia caquetía sin cita" % total)
    print("  %d confirman · %d reclasifican · %d conflicto de glosa · %d a revisar · %d sin rastro"
          % (por_clase[CONFIRMA], por_clase[RECLASIFICA], por_clase[CONFLICTO],
             por_clase[REVISAR], por_clase[SIN_RASTRO]))
    print("  F1 puede adjudicar con evidencia: %d de %d (%.0f%%)"
          % (adjudicadas, total, 100.0 * adjudicadas / max(total, 1)))
    print("=" * 78)
    print("  Fuentes: A=Alvarado(F3) · G=Gatschet(F4) · V=van Buurt(F6) · Z=Zavala(F7)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
