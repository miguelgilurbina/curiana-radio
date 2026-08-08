#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — validador de los datos de lengua
==========================================

El hermano de `compilar_corpus.py` para `2-lengua/`: cognados, topónimos y
morfemas. Misma disciplina — valida y emite, nunca modifica.

LO QUE DE VERDAD APORTA: INTEGRIDAD REFERENCIAL
-----------------------------------------------
Hasta ahora una cita era **texto libre**: `"Oliver 1989, cap. 3, p. 255"`. Nadie
comprobaba que esa obra existiera, ni que el id fuera consistente entre dos
hechos que citan lo mismo.

Con `4-fuentes/bibliografia.yaml`, `procedencia.obra` pasa a ser una **clave
foránea**, y este validador la comprueba. La cita deja de ser una promesa.

QUÉ VALIDA
----------
1. **Estructura** — campos obligatorios, `id` con forma `<tipo>-NNN` y único.
2. **Procedencia** — si la hay, su `obra` existe en la bibliografía. Si no la
   hay, la entrada debe declararlo con `deuda: sin-procedencia`: el hueco se
   admite, **pero no en silencio**.
3. **Cognados** — al menos dos lenguas (una relación de una sola lengua no es
   un cognado), códigos de lengua conocidos, y ninguna forma repetida entre dos
   cognados distintos sin marcar.
4. **Topónimos** — `nivel` legal (A/B/C/descartado), y que los morfemas citados
   en `morfemas` existan como entrada del lexicón o como morfema despejado.
5. **Corroboraciones** — la palabra corroborada existe en `VOCABULARIO_BASE`.

Uso:
    python compilar_lengua.py            # informe
    python compilar_lengua.py --check    # exit 1 si hay errores
    python compilar_lengua.py --deuda    # solo el listado de lo que no cita
"""

import argparse
import io
import os
import sys
from collections import Counter, defaultdict

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DIR_LENGUA = os.path.join(REPO, "2-lengua")
BIBLIOGRAFIA = os.path.join(REPO, "4-fuentes", "bibliografia.yaml")

NIVELES_TOPONIMO = ("A", "B", "C", "descartado")

# Dos clases de lengua, y la distinción no es cosmética:
#
# - **Núcleo** (mayúsculas, 2-4 letras): las lenguas sobre las que hay reglas de
#   transducción (`REGLAS_WY_CQ` y compañía). Un código en mayúsculas fuera de
#   este set es un typo, porque el motor va a intentar transducir con él.
# - **Comparanda** (minúsculas, nombre completo): las ~24 lenguas arahuacas que
#   Oliver cita para situar una forma en la familia — maipure, baré, wapishana,
#   tariana… No tienen reglas ni las necesitan: son cita, no maquinaria.
#
# Por eso el mapa de formas es abierto: cerrar la lista de comparanda obligaría
# a tocar el esquema cada vez que una fuente cita una lengua nueva.
LENGUAS_NUCLEO = {"PA", "CQ", "WY", "LK", "TN", "KL", "PJ", "CAIC"}


class Problema:
    def __init__(self, nivel, codigo, donde, mensaje):
        self.nivel, self.codigo, self.donde, self.mensaje = nivel, codigo, donde, mensaje

    def __repr__(self):
        return f"{self.nivel.upper()} [{self.codigo}] {self.donde}: {self.mensaje}"


def _err(c, d, m):
    return Problema("error", c, d, m)


def _avi(c, d, m):
    return Problema("aviso", c, d, m)


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def cargar(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def obras_conocidas():
    """Los ids de la bibliografía. Sin esto no hay integridad referencial."""
    doc = cargar(BIBLIOGRAFIA)
    if not doc:
        return None
    return {o["id"] for o in doc.get("obras", []) if o.get("id")}


# ══════════════════════════════════════════════════════════════════════
# VALIDACIONES
# ══════════════════════════════════════════════════════════════════════

def validar_procedencia(registros, obras, etiqueta):
    """La regla que hace que citar signifique algo."""
    problemas = []
    for r in registros:
        donde = f"{etiqueta}#{r.get('id', '?')}"
        proc = r.get("procedencia")

        if proc is None:
            # Se admite no tener fuente, pero hay que decirlo. Un hueco
            # declarado es dato; un hueco callado es una cita que no existe.
            if r.get("deuda") != "sin-procedencia":
                problemas.append(_err(
                    "procedencia-callada", donde,
                    "sin `procedencia` y sin `deuda: sin-procedencia` — "
                    "el hueco se admite, pero declarado"))
            continue

        if not isinstance(proc, dict):
            problemas.append(_err("procedencia-mal-formada", donde,
                                  f"es {type(proc).__name__}, se esperaba dict"))
            continue

        obra = proc.get("obra")
        if not obra:
            problemas.append(_err("procedencia-sin-obra", donde,
                                  "`procedencia` sin campo `obra`"))
        elif obras is not None and obra not in obras:
            problemas.append(_err(
                "obra-fantasma", donde,
                f"cita la obra `{obra}`, que no está en la bibliografía"))
    return problemas


def validar_ids(registros, prefijo, etiqueta):
    problemas = []
    vistos = Counter()
    import re
    patron = re.compile(rf"^{prefijo}-\d{{3}}$")
    for r in registros:
        rid = r.get("id")
        donde = f"{etiqueta}#{rid or '(sin id)'}"
        if not rid:
            problemas.append(_err("sin-id", etiqueta, "registro sin `id`"))
            continue
        vistos[rid] += 1
        if not patron.match(str(rid)):
            problemas.append(_err("id-malformado", donde,
                                  f"no tiene la forma {prefijo}-NNN"))
    for rid, n in vistos.items():
        if n > 1:
            problemas.append(_err("id-duplicado", f"{etiqueta}#{rid}",
                                  f"aparece {n} veces"))
    return problemas


def validar_cognados(doc, obras):
    problemas = []
    if not doc:
        return [_avi("cognados-ausente", "2-lengua/cognados.yaml", "no existe")]
    regs = doc.get("cognados", [])
    problemas += validar_ids(regs, "cognado", "cognados")
    problemas += validar_procedencia(regs, obras, "cognados")

    formas_vistas = defaultdict(list)
    for r in regs:
        donde = f"cognados#{r.get('id')}"
        formas = r.get("formas") or {}
        if not isinstance(formas, dict):
            problemas.append(_err("formas-mal-formadas", donde, "`formas` no es un mapa"))
            continue
        if len(formas) < 2:
            problemas.append(_err(
                "no-es-un-cognado", donde,
                f"solo {len(formas)} lengua(s) — «{r.get('glosa', '')[:40]}». "
                "Un cognado es una relación entre lenguas; una entrada de una "
                "sola pertenece al lexicón, no aquí"))
        for lengua, forma in formas.items():
            # Solo se vigilan los códigos del núcleo: son los que el motor va a
            # usar para transducir. Los nombres en minúscula son comparanda
            # citada y el mapa es abierto a propósito.
            if lengua.isupper() and lengua not in LENGUAS_NUCLEO:
                problemas.append(_err(
                    "codigo-de-lengua-desconocido", donde,
                    f"`{lengua}` parece código del núcleo pero no lo es "
                    f"(núcleo: {', '.join(sorted(LENGUAS_NUCLEO))})"))
            elif not str(lengua).strip():
                problemas.append(_err("lengua-vacia", donde, "clave de lengua vacía"))
            formas_vistas[(lengua, str(forma).lower())].append(r.get("id"))
        if not r.get("glosa"):
            problemas.append(_err("sin-glosa", donde, "sin `glosa`"))

    for (lengua, forma), ids in formas_vistas.items():
        if len(ids) > 1:
            problemas.append(_avi(
                "forma-repetida", f"cognados#{ids[0]}",
                f"{lengua} «{forma}» aparece también en {', '.join(ids[1:])} — "
                "¿son el mismo cognado?"))
    return problemas


def validar_toponimos(doc, obras, lexico, morfemas_ids):
    problemas = []
    if not doc:
        return [_avi("toponimos-ausente", "2-lengua/toponimos.yaml", "no existe")]
    regs = doc.get("toponimos", [])
    problemas += validar_ids(regs, "toponimo", "toponimos")
    problemas += validar_procedencia(regs, obras, "toponimos")

    for r in regs:
        donde = f"toponimos#{r.get('id')}"
        if not r.get("forma"):
            problemas.append(_err("sin-forma", donde, "sin `forma`"))
        nivel = r.get("nivel")
        if nivel not in NIVELES_TOPONIMO:
            problemas.append(_err(
                "nivel-ilegal", donde,
                f"`nivel: {nivel}` no es legal "
                f"(legales: {', '.join(NIVELES_TOPONIMO)})"))

    if lexico:
        for c in doc.get("corroboraciones_lexicon", []):
            palabra = c.get("palabra")
            if not palabra:
                continue
            # La clave no siempre es un lema suelto: hay pares de variantes
            # («quiva/quiba», «para/paragua») y afijos («ka-», «-ima»). Basta
            # con que UNA de las lecturas resuelva.
            candidatos = {palabra}
            candidatos |= {p.strip() for p in str(palabra).split("/")}
            candidatos |= {p.strip("-") for p in list(candidatos)}
            if not (candidatos & lexico):
                problemas.append(_avi(
                    "corrobora-fuera-del-lexicon", f"corroboraciones#{palabra}",
                    "ninguna lectura resuelve en VOCABULARIO_BASE — puede ser "
                    "un afijo o una forma que salió del habla"))
    return problemas


def validar_morfemas(doc, obras):
    problemas = []
    if not doc:
        return [_avi("morfemas-ausente", "2-lengua/morfemas.yaml", "no existe")]
    regs = doc.get("morfemas", [])
    problemas += validar_ids(regs, "morfema", "morfemas")
    for r in regs:
        if not r.get("forma"):
            problemas.append(_err("sin-forma", f"morfemas#{r.get('id')}", "sin `forma`"))
    return problemas


def compilar():
    obras = obras_conocidas()
    problemas = []
    if obras is None:
        problemas.append(_err(
            "sin-bibliografia", "4-fuentes/bibliografia.yaml",
            "no existe: sin ella no se puede comprobar ninguna cita. "
            "Genérala con `python curiana_sim/generar_bibliografia.py`"))

    try:
        sys.path.insert(0, AQUI)
        from curiana_lexicon import VOCABULARIO_BASE
        lexico = set(VOCABULARIO_BASE)
    except Exception as e:                                   # noqa: BLE001
        problemas.append(_avi("lexicon-no-importable", "curiana_lexicon",
                              f"no se pudo leer ({e})"))
        lexico = None

    cog = cargar(os.path.join(DIR_LENGUA, "cognados.yaml"))
    top = cargar(os.path.join(DIR_LENGUA, "toponimos.yaml"))
    mor = cargar(os.path.join(DIR_LENGUA, "morfemas.yaml"))

    morfemas_ids = {m.get("forma") for m in (mor or {}).get("morfemas", [])}
    problemas += validar_cognados(cog, obras)
    problemas += validar_toponimos(top, obras, lexico, morfemas_ids)
    problemas += validar_morfemas(mor, obras)
    return {"cognados": cog, "toponimos": top, "morfemas": mor}, problemas


def informe(datos, problemas):
    cog, top, mor = datos["cognados"], datos["toponimos"], datos["morfemas"]

    print("\n── Datos de lengua ──")
    if cog:
        m = cog.get("meta", {})
        print(f"  cognados   {m.get('cognados', '?'):>4}   "
              f"con procedencia {m.get('con_procedencia', '?')}  "
              f"sin {m.get('sin_procedencia', '?')}")
    if top:
        m = top.get("meta", {})
        print(f"  topónimos  {m.get('toponimos', '?'):>4}   {m.get('por_nivel', {})}")
    if mor:
        m = mor.get("meta", {})
        print(f"  morfemas   {m.get('morfemas', '?'):>4}   "
              f"glosados {m.get('glosados', '?')}")

    errores = [p for p in problemas if p.nivel == "error"]
    avisos = [p for p in problemas if p.nivel == "aviso"]

    for titulo, lista in (("ERRORES", errores), ("Avisos", avisos)):
        if not lista:
            continue
        print(f"\n── {titulo}: {len(lista)} ──")
        por = defaultdict(list)
        for p in lista:
            por[p.codigo].append(p)
        for codigo, items in sorted(por.items()):
            print(f"  [{codigo}] × {len(items)}")
            for p in items[:6]:
                print(f"     {p.donde}: {p.mensaje}")
            if len(items) > 6:
                print(f"     … y {len(items) - 6} más")

    print("\n" + "=" * 60)
    if errores:
        print(f"  ✗ {len(errores)} error(es), {len(avisos)} aviso(s)")
    else:
        print(f"  ✓ datos de lengua válidos — {len(avisos)} aviso(s)")
    print("=" * 60)


def informe_deuda(datos):
    print("\n── Lo que todavía no cita a nadie ──")
    for etiqueta, doc, clave in (("cognados", datos["cognados"], "cognados"),
                                 ("topónimos", datos["toponimos"], "toponimos")):
        if not doc:
            continue
        sin = [r for r in doc.get(clave, []) if not r.get("procedencia")]
        total = len(doc.get(clave, []))
        print(f"\n  {etiqueta}: {len(sin)}/{total} sin procedencia")
        for r in sin[:10]:
            print(f"     {r.get('id')}  {r.get('glosa') or r.get('forma')}")
        if len(sin) > 10:
            print(f"     … y {len(sin) - 10} más")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--deuda", action="store_true")
    args = ap.parse_args(argv)

    datos, problemas = compilar()
    if args.deuda:
        informe_deuda(datos)
        return 0
    informe(datos, problemas)
    if args.check and any(p.nivel == "error" for p in problemas):
        return 1
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
