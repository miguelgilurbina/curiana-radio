#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — ¿hay un NOMINALIZADOR retroabstraíble en el caquetío atestiguado?
===========================================================================

Campaña C de la decisión **d21.11** (`6-fusion/decisiones_tanda_2026-09-21.yaml`):

    «Buscar en Zavala, Alvarado y Arcaya nombres de acción que compartan
    terminación con un verbo, a la manera de `matakán`; si sale algo, entra
    atestiguado. NO se importa el nominalizador lokono `-hù`/`-hi`.»

La pregunta, entera: ¿hay en el material caquetío ATESTIGUADO algún nombre de
acción, de agente, de instrumento o de resultado que comparta terminación con
un verbo —o que se deje segmentar como raíz verbal + algo— de manera que se
pueda retroabstraer un nominalizador?

QUÉ HACE ESTE SCRIPT (y qué NO)
-------------------------------
1. **Inventario** de las 288 entradas del glosario de Zavala Reyes 2015 con su
   glosa **VERBATIM**, leída del PDF por el parser del propio proyecto
   (`minar_zavala_glosario.extraer()`), no por la glosa curada del lexicón.
   La clasificación semántica está DECLARADA abajo, entrada por entrada, con
   su glosa al lado: es revisable a ojo y el script comprueba que no falte ni
   sobre ningún número.
2. **Prueba del sufijo**: ¿algún lema es otro lema + algo? Y en particular:
   ¿algún NOMBRE del inventario es un VERBO atestiguado + algo?
3. **Control de azar** (el paso que mata a la mayoría de las terminaciones):
   la frecuencia de cada final de 1, 2 y 3 letras en el subconjunto de nombres
   de acción/agente/instrumento/resultado/lugar-de-acción, contra su
   frecuencia como final de palabra en **las 288**. Con p exacta
   (hipergeométrica), no con impresión.
4. Tres **controles de procedencia** que deciden cuánto vale lo que salga:
   de qué compilador viene cada verbo (regla del §8 de `minar-fuente`: una
   corroboración dentro de la misma lista no es independiente), qué dicen las
   otras fuentes (Oliver A-9, Alvarado 1921, Medina Colina) y qué ofrece la
   comparanda arahuaca.
5. El **subproducto** medido aparte y marcado como tal: `-ebo`, que NO es un
   nominalizador.

NO toca `curiana_lexicon.py`, ni `lexicon_zavala.py` (importarlo no lo
regenera), ni `2-lengua/`, ni el corpus. Escribe un YAML en `6-fusion/`.

    python 6-fusion/scripts/medir_nominalizador.py            # informe a pantalla
    python 6-fusion/scripts/medir_nominalizador.py --yaml RUTA # y el volcado
"""

from __future__ import annotations

import argparse
import collections
import math
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))


def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 (trampa declarada en CLAUDE.md)."""
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════
# LA CLASIFICACIÓN — declarada entrada por entrada, no inferida
# ══════════════════════════════════════════════════════════════════════
# El tipo sale de la GLOSA VERBATIM de Zavala, no de la glosa curada del
# lexicón (que en algún caso es otra: `bureche` #49 es «Hacer, realizar» en
# Zavala y «bebida fermentada de casabe» en el lexicón desde D10).
#
# Tipos:
#   verbo_accion       la glosa es uno o más infinitivos de acción
#   verbo_estativo     la glosa es una propiedad o estado, que el canon
#                      declara verbal desde d21.4 (`cat: v_estativo`)
#   n_accion           nombre de acción o abstracto deverbal
#   n_agente           el que hace / el que es
#   n_instrumento      aquello CON QUE se hace (la glosa declara la función)
#   n_resultado        aquello que RESULTA de hacer
#   n_lugar_accion     lugar definido por una ACCIÓN («sitio de moler maíz»)
#   n_lugar_cosa       lugar definido por una COSA — grupo de control
#   otro               todo lo demás (plantas, bichos, topónimos, afijos…)
#
# `dudoso` marca las que se cuentan pero que otra lectura razonable dejaría
# fuera. El informe da las cifras CON y SIN dudosas: si el resultado cambia
# de signo entre las dos, no hay resultado.
#
# Una entrada puede llevar DOS tipos cuando su glosa da las dos cosas
# («Sembrar, siembra, sembradío») — y ése, ya se verá, es el hallazgo.
CLASIFICACION: dict[int, dict] = {
    4:   {"tipos": ["n_resultado"], "por": "«Comida» es lo que resulta de comer/cocinar"},
    9:   {"tipos": ["n_lugar_accion"], "por": "«Sitio de MOLER maíz»: el lugar lo define la acción"},
    11:  {"tipos": ["verbo_estativo"], "por": "«Grande»; el canon lo declara v_estativo (d21.4)"},
    12:  {"tipos": ["n_agente"], "por": "«Nombre de jefe de parcialidad pequeña»: el que manda"},
    15:  {"tipos": ["n_lugar_cosa"], "por": "«Punto de tierra»"},
    16:  {"tipos": ["n_agente"], "dudoso": True,
          "por": "«Puede ser Oirubae: aquel o aquella que ACOMPAÑA» — pero la "
                 "glosa es una conjetura del compilador («Puede ser») y la forma "
                 "agentiva que propone, Oirubae, no está atestiguada como tal"},
    18:  {"tipos": ["n_lugar_cosa"], "por": "«Bosque, lugar, paraje, sitio fértil»"},
    19:  {"tipos": ["verbo_estativo"], "por": "«Maneto, patituerto»; el canon lo declara v_estativo"},
    20:  {"tipos": ["verbo_accion"], "por": "«Extraer, sacar»"},
    24:  {"tipos": ["n_resultado"], "por": "«Tabico HECHO DE tierra palos y bejuco»"},
    25:  {"tipos": ["verbo_accion"], "por": "«Recorrer, caminar»"},
    26:  {"tipos": ["n_lugar_cosa"], "por": "«Sitio, cerro alto»"},
    37:  {"tipos": ["n_lugar_cosa"], "por": "«Región de tierras coloradas cerca del mar»"},
    39:  {"tipos": ["verbo_accion", "n_accion"],
          "por": "«Dominar, triunfar, VICTORIA»: la MISMA forma glosa dos "
                 "infinitivos y su nombre de acción"},
    42:  {"tipos": ["n_lugar_accion"], "por": "«Sitio de CULTIVO»"},
    43:  {"tipos": ["n_agente"], "por": "«Piache, cacique, jefe, sacerdote, médico»: oficios"},
    44:  {"tipos": ["n_lugar_accion"], "dudoso": True,
          "por": "«Salina de Coro, COMERCIO de la sal»: la segunda mitad es "
                 "acción, pero la cabeza de la glosa es el lugar"},
    46:  {"tipos": ["n_instrumento"], "dudoso": True,
          "por": "«Chorro de agua, PRESA de agua»: artefacto de función declarada"},
    49:  {"tipos": ["verbo_accion"], "por": "«Hacer, realizar»"},
    50:  {"tipos": ["n_resultado"], "por": "«Licor FERMENTADO»"},
    52:  {"tipos": ["n_lugar_accion"], "por": "«sitio de CULTIVO»"},
    53:  {"tipos": ["verbo_estativo"], "por": "«En voz vulgar, enojado, colérico»; v_estativo en el canon"},
    74:  {"tipos": ["n_resultado"], "por": "«Puche de maíz»: alimento preparado"},
    94:  {"tipos": ["n_lugar_cosa"], "por": "«CAMINO del cacique Cumare»"},
    100: {"tipos": ["n_lugar_accion"], "por": "«Sitio de EXTRACCIÓN de barro»"},
    106: {"tipos": ["n_agente"], "dudoso": True,
          "por": "«Señor principal. Jefe mayor»: es un título, no un derivado "
                 "transparente de un verbo"},
    107: {"tipos": ["n_accion"], "por": "«Fuerza»: nombre abstracto"},
    110: {"tipos": ["n_agente"], "dudoso": True,
          "por": "«Insecto, hormiga QUE DAÑA»: la relativa es descripción del "
                 "compilador, no necesariamente morfología caquetía"},
    114: {"tipos": ["verbo_accion"], "por": "«Enredarse, atormentar»"},
    115: {"tipos": ["n_lugar_accion"], "dudoso": True,
          "por": "«Conuco, SEMBRADO»: participio sustantivado en la glosa"},
    116: {"tipos": ["verbo_accion"], "por": "«Hacer trabajos cortos»"},
    117: {"tipos": ["n_lugar_cosa"], "por": "«Camino, paso, senda»"},
    119: {"tipos": ["verbo_accion"], "por": "«Empezar, crear»"},
    120: {"tipos": ["verbo_estativo", "n_accion"],
          "por": "«Feroz, feo, ESPANTO»: dos propiedades y un abstracto, la "
                 "misma forma; el canon lo declara v_estativo"},
    121: {"tipos": ["n_lugar_accion"], "dudoso": True,
          "por": "«Tierra de CRIANZA o tierra de pasto»"},
    131: {"tipos": ["verbo_estativo"], "por": "«Integro»; v_estativo en el canon"},
    133: {"tipos": ["n_lugar_accion"], "dudoso": True,
          "por": "«Muchas tierras de CULTIVO»"},
    137: {"tipos": ["n_instrumento"], "por": "«Cesto PARA CARGAR a los niños»"},
    140: {"tipos": ["verbo_estativo"], "por": "«Salado, ácido»; v_estativo en el canon"},
    145: {"tipos": ["verbo_estativo"], "por": "«Viejo, anciano»; v_estativo en el canon"},
    149: {"tipos": ["verbo_accion"], "por": "«Dar, entregar»"},
    151: {"tipos": ["verbo_accion"], "por": "«Arreglar, acomodar»"},
    153: {"tipos": ["n_resultado"], "por": "«Maíz TOSTADO y miel»"},
    155: {"tipos": ["n_lugar_accion"], "por": "«Sitio de TRABAJO»"},
    160: {"tipos": ["n_agente"], "por": "«EL AVE QUE VUELA»: relativa agentiva"},
    161: {"tipos": ["n_accion"], "dudoso": True,
          "por": "«Comunidad indígena. Enemigo, ENEMISTAD»: glosa triple y dispersa"},
    168: {"tipos": ["verbo_accion"], "por": "«Adquirir»"},
    169: {"tipos": ["n_instrumento"], "por": "«Teas de madera, PARA ENCANDILAR en las labores de pesca nocturna»"},
    170: {"tipos": ["verbo_accion", "n_accion"],
          "por": "«Regar, REGADÍO»: la misma forma, el infinitivo y su nombre"},
    171: {"tipos": ["verbo_accion"], "por": "«Guardar»"},
    172: {"tipos": ["verbo_accion"], "por": "«Recoger»"},
    173: {"tipos": ["n_lugar_cosa"], "por": "«Sitio donde ABUNDA jajato»: lo define una planta"},
    174: {"tipos": ["verbo_accion"], "por": "«Establecer, estancar»"},
    175: {"tipos": ["verbo_accion"], "por": "«Oír, escuchar»"},
    176: {"tipos": ["n_lugar_cosa"], "dudoso": True, "por": "«Lugar de arena»"},
    179: {"tipos": ["n_lugar_cosa"], "por": "«PASO de los vientos»"},
    180: {"tipos": ["verbo_accion", "n_accion", "n_lugar_accion"],
          "por": "«SEMBRAR, SIEMBRA, SEMBRADÍO. Conuco»: infinitivo, nombre de "
                 "acción y nombre de lugar en UNA sola forma"},
    183: {"tipos": ["n_agente"], "por": "«VOCERO antiguo de la tierra, sabio CONOCEDOR de la tierra»"},
    188: {"tipos": ["n_lugar_cosa"], "por": "«Sitio de palmeras»"},
    198: {"tipos": ["verbo_estativo"], "por": "«Anegadizo»; v_estativo en el canon"},
    203: {"tipos": ["n_accion"], "por": "«Ayuda»: nombre de acción"},
    205: {"tipos": ["n_agente"], "por": "«Baquiano, CONOCEDOR»"},
    206: {"tipos": ["verbo_accion"], "por": "«Engañar»"},
    213: {"tipos": ["verbo_accion"], "por": "«Engañar, ENGAÑADO»: infinitivo y participio, misma forma"},
    217: {"tipos": ["n_accion"], "por": "«Sangre, SANGRADO»: el nombre y el nombre de acción, misma forma"},
    227: {"tipos": ["verbo_estativo"], "por": "«Blando»; `siwa` es raíz verbal en el canon"},
    228: {"tipos": ["verbo_accion", "n_lugar_accion"], "dudoso": True,
          "por": "«SALVAR. Caserío, sitio»: infinitivo y lugar en la misma "
                 "forma, pero la segunda mitad de la glosa puede ser un topónimo"},
    229: {"tipos": ["verbo_estativo"], "por": "«Insolente»; v_estativo en el canon"},
    230: {"tipos": ["n_lugar_cosa"], "por": "«Sitio a orilla del mar. Arena»"},
    234: {"tipos": ["n_accion"], "por": "«Conuco, SIEMBRA»"},
    240: {"tipos": ["n_lugar_accion"], "dudoso": True, "por": "«Hato, conuco»"},
    245: {"tipos": ["n_lugar_accion"], "por": "«Lugar de CULTIVO»"},
    253: {"tipos": ["n_accion"], "por": "«AGLOMERACIÓN, montón»"},
    256: {"tipos": ["n_accion"], "por": "«SIEMBRA de cacao»"},
    259: {"tipos": ["n_instrumento"], "por": "«Vasija, UTENSILIO»"},
    260: {"tipos": ["n_agente", "n_instrumento"],
          "por": "«Ave CANTADORA. Flauta»: agentivo y el instrumento que suena"},
    261: {"tipos": ["n_lugar_accion"], "por": "«Lugar de DESCANSO»"},
    269: {"tipos": ["n_lugar_accion"], "por": "«Sitio de CRÍA de animales»"},
    271: {"tipos": ["n_resultado"], "dudoso": True,
          "por": "«ENVOLTURA o vaina de las cerbatanas»"},
    273: {"tipos": ["n_accion"], "por": "«Plantío, SIEMBRA»"},
    275: {"tipos": ["verbo_estativo"], "por": "«Seco, arenoso»; v_estativo en el canon"},
    283: {"tipos": ["n_accion"], "por": "«SIEMBRA, plantío»"},
}

# Las que la criba automática señala y la clasificación deja fuera A PROPÓSITO.
# Cada una costó mirar la glosa verbatim, que es la trampa que la skill
# `minar-fuente` nombra: una glosa castellana que suena a nombre de acción y
# en la fuente es otra cosa.
TRAMPAS_DECLARADAS: dict[int, str] = {
    1:   "«PARA DESIGNAR las aguas de un río lleno de arena»: el infinitivo es "
         "del compilador explicando su propia entrada, no glosa de la voz",
    10:  "«Una luna. MEDICIÓN de tiempo»: «medición» es la etiqueta del "
         "compilador para decir de qué campo es la palabra; no es la glosa",
    47:  "igual que #10: «dos lunas. Medición de tiempo»",
    111: "«Distintivo de los nombres colectivos de abundancia»: es un AFIJO, y "
         "la glosa es metalingüística",
    132: "«Hoguera»: cosa, no nombre de acción",
    159: "«Mujer bella»: la criba la marca porque «mujer» acaba en -er",
    163: "«Mujer»: lo mismo",
    201: "«Ahí. ADVERBIO DE LUGAR»: la palabra «lugar» es la etiqueta "
         "gramatical del compilador",
    267: "«CUENTA de piedras»: es la chaquira, el abalorio — no el acto de "
         "contar. La trampa más limpia del glosario",
    264: "«Hierba de propiedades eméticas. USADO PARA CUAJAR quesos»: el "
         "infinitivo describe el uso que le da el castellano, no la voz",
    156: "«Hierba QUITA SED»: el compuesto es castellano",
    141: "«Barro de loza, PARA LA FÁBRICA de budares y ollas»: es la materia, "
         "no el instrumento",
    83:  "«Tinaja pequeña»: un recipiente sin función declarada en la glosa no "
         "es nombre de instrumento; si se contaran todos los cacharros, el "
         "conjunto se llenaría de ruido",
    27:  "«Calabaza con cal»: igual que #83 (y su gemela #220 `raporon`)",
    75:  "«Poniente»: es un punto cardinal. Se mide aparte, en el bloque -ebo",
}

TIPOS_DIANA = ("n_accion", "n_agente", "n_instrumento", "n_resultado",
               "n_lugar_accion")
TIPOS_VERBO = ("verbo_accion", "verbo_estativo")


# ══════════════════════════════════════════════════════════════════════
# UTILIDADES
# ══════════════════════════════════════════════════════════════════════
def norm(s: str) -> str:
    """minúsculas sin acentos — la misma que usa el minador de Zavala."""
    s = (s or "").lower().strip()
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def hipergeometrica_cola(k: int, n: int, K: int, N: int) -> float:
    """P(X >= k) con X ~ Hipergeométrica(N, K, n). Exacta, con math.comb.

    N = todas las entradas, K = las que tienen el final, n = el tamaño del
    subconjunto, k = las del subconjunto que tienen el final.
    """
    if n == 0 or K == 0:
        return 1.0
    total = math.comb(N, n)
    acumulado = 0
    for i in range(k, min(K, n) + 1):
        acumulado += math.comb(K, i) * math.comb(N - K, n - i)
    return acumulado / total


# ══════════════════════════════════════════════════════════════════════
# 1. EL INVENTARIO
# ══════════════════════════════════════════════════════════════════════
def inventario() -> tuple[list[dict], dict]:
    """Las 288 de Zavala con su glosa verbatim y su tipo declarado."""
    import minar_zavala_glosario as MZ

    ents = MZ.extraer()
    nums = {e["num"] for e in ents}

    # Regla 6: un cero se verifica, y un desajuste de claves también.
    sobran = sorted(set(CLASIFICACION) - nums)
    if sobran:
        raise SystemExit(f"CLASIFICACION apunta a entradas que no existen: {sobran}")
    sobran_t = sorted(set(TRAMPAS_DECLARADAS) - nums)
    if sobran_t:
        raise SystemExit(f"TRAMPAS_DECLARADAS apunta a inexistentes: {sobran_t}")

    filas = []
    for e in ents:
        c = CLASIFICACION.get(e["num"], {})
        filas.append({
            "num": e["num"],
            "lemas": e["lemas"],
            "lema": e["lemas"][0],
            "clave": norm(e["lemas"][0]),
            "siglas": e["siglas"],
            "glosa_verbatim": e["definicion"],
            "tipos": c.get("tipos", ["otro"]),
            "dudoso": bool(c.get("dudoso")),
            "por": c.get("por", ""),
        })
    resumen = collections.Counter()
    for f in filas:
        for t in f["tipos"]:
            resumen[t] += 1
    return filas, dict(resumen.most_common())


# ══════════════════════════════════════════════════════════════════════
# 2. LA PRUEBA DEL SUFIJO
# ══════════════════════════════════════════════════════════════════════
def prueba_del_sufijo(filas: list[dict]) -> dict:
    """¿Algún lema es otro lema + algo? ¿Y alguno de ellos es VERBO + algo?"""
    por_clave: dict[str, dict] = {}
    for f in filas:
        for l in f["lemas"]:
            por_clave.setdefault(norm(l), f)

    pares = []
    for corta, fc in por_clave.items():
        if len(corta) < 3:          # `gua`, `na`, `par` se pegan a todo
            continue
        for larga, fl in por_clave.items():
            if larga == corta or not larga.startswith(corta):
                continue
            pares.append({
                "base": corta, "base_num": fc["num"],
                "base_glosa": fc["glosa_verbatim"],
                "base_tipos": fc["tipos"],
                "resto": larga[len(corta):],
                "derivada": larga, "derivada_num": fl["num"],
                "derivada_glosa": fl["glosa_verbatim"],
                "derivada_tipos": fl["tipos"],
            })

    # El caso que la campaña busca: base VERBAL, derivada NOMBRE de la diana.
    diana = [p for p in pares
             if any(t in TIPOS_VERBO for t in p["base_tipos"])
             and any(t in TIPOS_DIANA for t in p["derivada_tipos"])]
    # Y el inverso, que también dice algo: nombre → verbo.
    inverso = [p for p in pares
               if any(t in TIPOS_DIANA or t == "otro" for t in p["base_tipos"])
               and any(t in TIPOS_VERBO for t in p["derivada_tipos"])]

    return {
        "umbral_de_base": "3 letras — por debajo, `gua`, `par` y `na` "
                          "segmentan medio glosario y el resultado sería ruido",
        "parejas_totales": len(pares),
        "parejas": pares,
        "base_verbal_derivada_nominal": diana,
        "base_nominal_derivada_verbal": inverso,
    }


# ══════════════════════════════════════════════════════════════════════
# 3. EL CONTROL DE AZAR
# ══════════════════════════════════════════════════════════════════════
def control_de_azar(filas: list[dict], largos=(1, 2, 3)) -> dict:
    """La terminación del subconjunto contra la del glosario entero.

    Una terminación que cierra el 8 % de los nombres de acción y el 8 % de
    todo no es nada. Se mide con p hipergeométrica exacta.
    """
    todas = [f["clave"] for f in filas]
    N = len(todas)

    def subconjunto(tipos, con_dudosas=True):
        out = []
        for f in filas:
            if any(t in tipos for t in f["tipos"]):
                if con_dudosas or not f["dudoso"]:
                    out.append(f["clave"])
        return out

    bloques = {}
    for etiqueta, tipos in (("diana", TIPOS_DIANA),
                            ("verbos", TIPOS_VERBO),
                            ("lugar_de_cosa_control", ("n_lugar_cosa",))):
        for con_dud in (True, False):
            sub = subconjunto(tipos, con_dud)
            n = len(sub)
            filas_out = []
            for L in largos:
                cuenta_todo = collections.Counter(c[-L:] for c in todas if len(c) >= L)
                cuenta_sub = collections.Counter(c[-L:] for c in sub if len(c) >= L)
                for fin, k in cuenta_sub.most_common():
                    K = cuenta_todo[fin]
                    if k < 2:
                        continue
                    p = hipergeometrica_cola(k, n, K, N)
                    filas_out.append({
                        "final": f"-{fin}",
                        "en_el_subconjunto": k,
                        "tamano_subconjunto": n,
                        "pct_subconjunto": round(100 * k / n, 1) if n else 0.0,
                        "en_las_288": K,
                        "pct_288": round(100 * K / N, 1),
                        "enriquecimiento": round((k / n) / (K / N), 2) if n and K else 0.0,
                        "p_hipergeometrica": float(f"{p:.4g}"),
                    })
            filas_out.sort(key=lambda r: (r["p_hipergeometrica"],
                                          -r["enriquecimiento"]))
            bloques[f"{etiqueta}{'' if con_dud else '_sin_dudosas'}"] = {
                "n": n, "finales": filas_out,
            }
    bloques["N_glosario"] = N
    bloques["umbral_declarado"] = (
        "se miran los finales con k >= 2 en el subconjunto; el criterio para "
        "llamar candidato a algo es p < 0,05 Y enriquecimiento > 2 Y que la "
        "base que queda al quitarlo exista en el atestiguado. Los tres, no uno"
    )
    return bloques


# ══════════════════════════════════════════════════════════════════════
# 3 bis. LA TERMINACIÓN COMPARTIDA — la pregunta, con sus palabras
# ══════════════════════════════════════════════════════════════════════
def terminaciones_compartidas(filas: list[dict], largos=(2, 3)) -> dict:
    """«¿Hay un nombre de acción que COMPARTA TERMINACIÓN con un verbo?»

    Compartir terminación no basta: para que `-X` sea nominalizador hace falta
    que el NOMBRE lo lleve, el VERBO **no**, y que al quitarlo quede una raíz
    atestiguada. Aquí se mide lo primero, y se dice de cada final si cumple lo
    segundo.
    """
    verbos = [f for f in filas if any(t in TIPOS_VERBO for t in f["tipos"])]
    diana = [f for f in filas if any(t in TIPOS_DIANA for t in f["tipos"])]
    claves = {f["clave"] for f in filas}

    out = []
    for L in largos:
        cv = collections.Counter(f["clave"][-L:] for f in verbos if len(f["clave"]) > L)
        cd = collections.Counter(f["clave"][-L:] for f in diana if len(f["clave"]) > L)
        for fin in sorted(set(cv) & set(cd)):
            nombres = [f for f in diana if f["clave"].endswith(fin)
                       and len(f["clave"]) > L]
            bases = []
            for f in nombres:
                base = f["clave"][:-L]
                bases.append({"nombre": f["clave"], "base_al_quitarlo": base,
                              "base_atestiguada": base in claves})
            out.append({
                "final": f"-{fin}",
                "verbos_que_lo_llevan": sorted(
                    f["clave"] for f in verbos if f["clave"].endswith(fin)
                    and len(f["clave"]) > L),
                "nombres_que_lo_llevan": sorted(f["clave"] for f in nombres),
                "bases_al_quitarlo": bases,
                "bases_atestiguadas": sum(1 for b in bases if b["base_atestiguada"]),
                "descalifica": "el VERBO también lo lleva: si `-X` nominalizara, "
                               "el verbo no podría terminar igual",
            })
    return {
        "criterio": "compartir terminación es condición NECESARIA de un "
                    "parecido, y condición SUFICIENTE de nada. Un final que "
                    "llevan los dos lados no puede ser lo que los distingue",
        "verbos": len(verbos), "nombres_diana": len(diana),
        "finales_compartidos": out,
    }


# ══════════════════════════════════════════════════════════════════════
# 3 ter. LA DERIVACIÓN CERO — lo que el material SÍ muestra
# ══════════════════════════════════════════════════════════════════════
def derivacion_cero(filas: list[dict]) -> dict:
    """Entradas cuya ÚNICA forma glosa a la vez el verbo y su nombre.

    Es el resultado positivo de la campaña: donde el glosario da las dos
    cosas, las da **con la misma forma**. Si hubiera un nominalizador, ahí es
    donde se vería, y no se ve.
    """
    casos = []
    for f in filas:
        tv = [t for t in f["tipos"] if t in TIPOS_VERBO]
        tn = [t for t in f["tipos"] if t in TIPOS_DIANA]
        if tv and tn:
            casos.append({
                "lema": f["lema"], "num": f["num"],
                "siglas": ",".join(f["siglas"]),
                "glosa_verbatim": f["glosa_verbatim"],
                "tipos": f["tipos"], "dudoso": f["dudoso"],
            })
    return {
        "que_mide": "una sola forma glosada como verbo Y como nombre",
        "casos": len(casos),
        "sin_dudosas": sum(1 for c in casos if not c["dudoso"]),
        "detalle": casos,
        "reserva_obligatoria": (
            "una glosa castellana que enumera «sembrar, siembra, sembradío» "
            "puede ser el compilador diciendo DE QUÉ VA la palabra, no una "
            "afirmación sobre las clases de palabra del caquetío. El dato es "
            "el glosario, no la lengua: esto describe lo que la fuente "
            "registra, y la fuente no distingue"),
    }


# ══════════════════════════════════════════════════════════════════════
# 3 quater. LA REDUPLICACIÓN DENTRO DE LA DIANA
# ══════════════════════════════════════════════════════════════════════
def reduplicacion_en_la_diana(filas: list[dict]) -> dict:
    """¿Cómo forma el atestiguado los nombres que sí se dejan segmentar?

    F11 ya midió la reduplicación con control (`REDUPLICACION` en
    `lexicon_toponimos.py`, y §9 de morfologia.md). Aquí sólo se mira cuántos
    de los nombres DIANA son reduplicados y con qué base atestiguada.
    """
    claves = {f["clave"]: f for f in filas}

    def reduplicada(c: str):
        # total exacta: X X
        n = len(c)
        if n >= 6 and n % 2 == 0 and c[:n // 2] == c[n // 2:]:
            return c[:n // 2], "total"
        # total con haplología o cambio de la vocal final: X X'
        for corte in range(3, n - 2):
            a, b = c[:corte], c[corte:]
            if len(b) >= 3 and a[:len(b) - 1] == b[:len(b) - 1]:
                return a, "total con vocal final distinta"
        # parcial: la última sílaba repetida (apo → apopo)
        for k in (2, 3):
            if n > k and c[-k:] == c[-2 * k:-k]:
                return c[:-k], "parcial (sílaba final)"
        return None, None

    diana = [f for f in filas if any(t in TIPOS_DIANA for t in f["tipos"])]
    casos = []
    for f in diana:
        base, tipo = reduplicada(f["clave"])
        if base:
            casos.append({
                "lema": f["lema"], "num": f["num"],
                "glosa_verbatim": f["glosa_verbatim"],
                "tipos": f["tipos"], "base": base, "reduplicacion": tipo,
                "base_atestiguada": base in claves,
                "glosa_de_la_base": claves[base]["glosa_verbatim"] if base in claves else None,
            })
    agentes = [f for f in filas if "n_agente" in f["tipos"]]
    red_agentes = [c for c in casos if "n_agente" in c["tipos"]]
    return {
        "aviso": "el detector de aquí es el de esta campaña, NO el de F11; "
                 "sirve para contar dentro de la diana, no para volver a medir "
                 "la tasa del corpus, que ya está medida con control en "
                 "2-lengua/morfologia.md §9",
        "nombres_diana": len(diana),
        "reduplicados": len(casos),
        "agentes": len(agentes),
        "agentes_reduplicados": len(red_agentes),
        "detalle": casos,
    }


# ══════════════════════════════════════════════════════════════════════
# 4. DE QUIÉN VIENE CADA VERBO (la independencia de la fuente)
# ══════════════════════════════════════════════════════════════════════
SIGLAS = {
    "PMA": "Pedro Manuel Arcaya", "HB": "Adrián Hernández Baño",
    "E": "Juan Esteves", "AM": "Angulo Molina", "A": "Lisandro Alvarado",
    "GC": "Galeotto Cey", "CGB": "Carlos González Batista",
    "AAM": "Antonio Arellano Moreno", "HP": "Aníbal Hill Peña",
}


def de_quien_viene(filas: list[dict]) -> dict:
    """Skill `minar-fuente` §8: una corroboración dentro de la misma lista no
    es independiente. Si todos los verbos salen de un compilador, cualquier
    patrón que se encuentre entre ellos es un patrón de ESA lista."""
    def reparto(tipos):
        c = collections.Counter()
        for f in filas:
            if any(t in tipos for t in f["tipos"]):
                for s in (f["siglas"] or ["(sin sigla)"]):
                    c[s] += 1
        return dict(c.most_common())

    return {
        "verbos_por_compilador": reparto(TIPOS_VERBO),
        "verbos_de_accion_por_compilador": reparto(("verbo_accion",)),
        "diana_por_compilador": reparto(TIPOS_DIANA),
        "todo_el_glosario_por_compilador": dict(collections.Counter(
            s for f in filas for s in (f["siglas"] or ["(sin sigla)"])
        ).most_common()),
        "leyenda": SIGLAS,
    }


# ══════════════════════════════════════════════════════════════════════
# 5. LA SONDA `ja-` — una letra que concentra verbos
# ══════════════════════════════════════════════════════════════════════
def sonda_inicial(filas: list[dict]) -> dict:
    """¿Se reparten los verbos por el abecedario, o se amontonan?"""
    por_inicial: dict[str, dict] = collections.defaultdict(
        lambda: {"entradas": 0, "verbos": 0, "lemas_verbales": []})
    for f in filas:
        ini = f["clave"][:1]
        d = por_inicial[ini]
        d["entradas"] += 1
        if any(t in TIPOS_VERBO for t in f["tipos"]):
            d["verbos"] += 1
            d["lemas_verbales"].append(f"{f['lema']} (#{f['num']}) «{f['glosa_verbatim'][:40]}»")
    N = len(filas)
    K = sum(d["verbos"] for d in por_inicial.values())
    out = []
    for ini, d in sorted(por_inicial.items()):
        if d["verbos"] < 2:
            continue
        p = hipergeometrica_cola(d["verbos"], d["entradas"], K, N)
        out.append({
            "inicial": ini,
            "entradas_con_esa_inicial": d["entradas"],
            "verbos": d["verbos"],
            "pct": round(100 * d["verbos"] / d["entradas"], 1),
            "p_hipergeometrica": float(f"{p:.4g}"),
            "lemas": d["lemas_verbales"],
        })
    out.sort(key=lambda r: r["p_hipergeometrica"])
    return {"verbos_en_el_glosario": K, "entradas": N, "por_inicial": out}


# ══════════════════════════════════════════════════════════════════════
# 6. EL SUBPRODUCTO: `-ebo`. NO es un nominalizador, y se dice.
# ══════════════════════════════════════════════════════════════════════
def bloque_ebo(filas: list[dict]) -> dict:
    """`ebo` #117 «Camino, paso, senda» es voz libre atestiguada y aparece
    como segundo miembro en compuestos cuya glosa dice «camino / paso /
    lugar de X». Es el mismo patrón que resolvió `-bana` en D9 (seis apoyos),
    y es DENOMINAL: no deriva nombres de verbos. Se mide aquí porque salió de
    esta campaña, no porque la conteste."""
    en_ebo = [f for f in filas if f["clave"].endswith("ebo")]
    return {
        "aviso": "`-ebo` NO responde a d21.11: compone sobre NOMBRES, no sobre "
                 "verbos. Se mide y se propone aparte",
        "base_libre": next(
            ({"lema": f["lema"], "num": f["num"], "glosa": f["glosa_verbatim"]}
             for f in filas if f["clave"] == "ebo"), None),
        "compuestos": [
            {"lema": f["lema"], "num": f["num"], "siglas": f["siglas"],
             "glosa": f["glosa_verbatim"]}
            for f in en_ebo if f["clave"] != "ebo"],
        "cuantos": len(en_ebo) - 1,
    }


# ══════════════════════════════════════════════════════════════════════
# 7. LO QUE DICE EL CANON DE HOY
# ══════════════════════════════════════════════════════════════════════
def sonda_canon() -> dict:
    """¿Cuántas raíces verbales ATESTIGUADAS tiene el lexicón, y qué reglas
    derivan nombre de verbo? La sonda es la del auditor de morfología."""
    import curiana_lexicon as L

    verbales = frozenset(getattr(L, "CATS_VERBALES", {"v_raiz"}))
    atest = sorted(k for k, v in L.VOCABULARIO_BASE.items()
                   if v.get("cat") in verbales
                   and v.get("fuente") == "caquetío-atestiguado")
    return {
        "raices_verbales_de_familia_caquetia": len(L.raices_verbales_caquetias()),
        "de_ellas_atestiguadas": len(atest),
        "atestiguadas": atest,
        "reglas_que_derivan_nombre_de_verbo": sorted(
            a for a, r in L.TODAS_LAS_REGLAS.items()
            if "nombre" in ((r.get("desc") or "") + (r.get("nombre") or "")).lower()
            and "verbo" in (r.get("uso") or "").lower()),
        "morfemas_declarados": len(L.TODAS_LAS_REGLAS),
    }


# ══════════════════════════════════════════════════════════════════════
# 8. LAS OTRAS FUENTES — los ceros, verificados (regla 6)
# ══════════════════════════════════════════════════════════════════════
INFINITIVO = re.compile(
    r"^[a-záéíóúñ]+(?:ar|er|ir)(?:se)?(?:[,;.]|\s|$)", re.I)


def otras_fuentes() -> dict:
    """Oliver A-9, Medina Colina y Alvarado 1921: ¿traen verbos caquetíos?"""
    import yaml
    salida = {}

    # ── Oliver 1989, Apéndice A, Tabla A-9 ──
    ruta = os.path.join(RAIZ, "6-fusion", "tabla_a9_oliver.yaml")
    d = yaml.safe_load(open(ruta, encoding="utf-8"))
    ents = d.get("entradas", [])
    glosas = [str(e.get("glosa_es", "")).strip(' "\'') for e in ents]
    verbos = [g for g in glosas if INFINITIVO.match(g)]
    # Regla 6: el uno también se verifica. El único que marca la criba es
    # «ser viviente» (la glosa de `Caquetio`), que es un SUSTANTIVO con el
    # infinitivo dentro — falso positivo, y se dice.
    falsos = [g for g in verbos if re.match(r"^(ser|estar)\s+\w", g, re.I)]
    salida["oliver_a9"] = {
        "que_es": "«Selected Caquetío Vocabulary from the XVIth Century», "
                  "Oliver 1989 Apéndice A, pp. impresas 593-594",
        "entradas_transcritas": len(ents),
        "glosas_que_la_criba_marca": len(verbos),
        "de_ellas_falsos_positivos": len(falsos),
        "los_falsos": falsos,
        "verbos_reales": len(verbos) - len(falsos),
        "ejemplos_de_glosa": glosas[:12],
        "lectura": "el vocabulario caquetío más antiguo del repo es enteramente "
                   "NOMINAL: sin verbo no hay par verbo/nombre que retroabstraer",
    }

    # ── Medina Colina, el dictado (voces vivas) ──
    ruta = os.path.join(RAIZ, "6-fusion", "medina_colina_dictado.yaml")
    d = yaml.safe_load(open(ruta, encoding="utf-8"))
    ents = d.get("entradas", [])
    verbos = [e for e in ents
              if INFINITIVO.match(str(e.get("glosa_libro", "")).strip())]
    salida["medina_colina_dictado"] = {
        "que_es": "«Del Habla Paraguanera», dictado desde 2026-09-01",
        "entradas_dictadas": len(ents),
        "glosas_que_son_infinitivo": len(verbos),
        "lectura": "las voces vivas de Paraguaná son nombres; el dictado es "
                   "parcial por diseño, así que es un cero DEL DICTADO",
    }

    # ── Alvarado 1921 ──
    ruta = os.path.join(RAIZ, "fuentes_caquetios",
                        "Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf")
    salida["alvarado_1921"] = {
        "que_es": "«Glosario de voces indígenas de Venezuela»",
        "receta": "pdftotext -enc UTF-8 (pypdf no vale; trampa declarada)",
        "pdf_presente": os.path.exists(ruta),
        "lectura": "sus entradas con glosa verbal son verbos CASTELLANOS "
                   "derivados de nombres indígenas —cachicamear, cebucanear, "
                   "embijar, enguanepar, chigüirear—, no verbos indígenas. "
                   "Un glosario de lo que el español TOMÓ prestado recoge "
                   "nombres: es lo que se presta entre lenguas",
        "medido_en": "la bitácora de 4-fuentes/alvarado-1921.md",
    }

    # ── Arcaya 1920 — la cita que cierra su lado ──
    ruta = os.path.join(RAIZ, "fuentes_caquetios",
                        "Arcaya_1920_Historia_Estado_Falcon.pdf")
    salida["arcaya_1920"] = {
        "que_es": "«Historia del Estado Falcón», tomo I",
        "pdf_presente": os.path.exists(ruta),
        "pagina_impresa": 75,
        "cita_literal": (
            "«Pensamos, con fundadas razones, que también debe clasificarse en "
            "la familia lingüística nuarhuaca al idioma caquetío. No se "
            "conserva de él, desgraciadamente, vocabulario alguno, ni mucho "
            "menos hay frases que permitan conocer su estructura gramatical, "
            "pero sí quedan los nombres, muy numerosos por cierto, de los "
            "lugares que habitaron […] y nombres propios de personas»"),
        "lo_unico_que_da": "de la Relación de Barquisimeto de 1579: «sabana», "
                           "«Capu» (el demonio), «bariqué», «guadabacoa o "
                           "adobacoa», «quiccide», «mene» y «cumaragua» — siete "
                           "voces, las siete NOMBRES",
        "y_una_frase_que_importa_para_el_otro_lado": (
            "misma página: las lenguas nuarhuacas «conjuga[n] los temas "
            "verbales y nominales, prefijándoles ciertos índices posesivos». "
            "Es lo que los agentes hicieron —y es de la FAMILIA, no del "
            "caquetío: describe conjugación, no derivación de nombres"),
        "aviso_de_extraccion": (
            "la capa de texto de este PDF pierde los acentos (Falc?n, "
            "ling??stica). La cita se transcribe restituyéndolos; el texto "
            "sin acentos es reproducible con `pdftotext -enc UTF-8`"),
    }
    return salida


# ══════════════════════════════════════════════════════════════════════
# VOLCADO
# ══════════════════════════════════════════════════════════════════════
def _y(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if "\n" in s or len(s) > 90 or s[:1] in "&*!%@`>|[{#-?:" or ": " in s:
        return "'" + s.replace("'", "''") + "'"
    return s


def volcar(obj, nivel=0, salida=None) -> list[str]:
    salida = salida if salida is not None else []
    sangria = "  " * nivel
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                salida.append(f"{sangria}{k}:")
                volcar(v, nivel + 1, salida)
            elif isinstance(v, (dict, list)):
                salida.append(f"{sangria}{k}: {'{}' if isinstance(v, dict) else '[]'}")
            else:
                salida.append(f"{sangria}{k}: {_y(v)}")
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, dict):
                salida.append(f"{sangria}-")
                volcar(v, nivel + 1, salida)
            elif isinstance(v, list):
                salida.append(f"{sangria}-")
                volcar(v, nivel + 1, salida)
            else:
                salida.append(f"{sangria}- {_y(v)}")
    return salida


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaml", help="ruta del volcado YAML")
    args = ap.parse_args(argv)

    filas, resumen = inventario()
    doc = {
        "medicion": "nominalizador-retroabstraccion",
        "fecha": "2026-09-21",
        "responde_a": "6-fusion/decisiones_tanda_2026-09-21.yaml §d21.11 (campaña C)",
        "fuente_principal": "zavala-reyes-2015 (glosario de 288 entradas, "
                            "leído del PDF por minar_zavala_glosario.extraer)",
        "glosa_usada": "la VERBATIM del glosario, no la curada del lexicón",
        "inventario": {"entradas": len(filas), "por_tipo": resumen},
        "canon_hoy": sonda_canon(),
        "de_quien_viene": de_quien_viene(filas),
        "prueba_del_sufijo": prueba_del_sufijo(filas),
        "terminaciones_compartidas": terminaciones_compartidas(filas),
        "derivacion_cero": derivacion_cero(filas),
        "reduplicacion_en_la_diana": reduplicacion_en_la_diana(filas),
        "control_de_azar": control_de_azar(filas),
        "sonda_inicial": sonda_inicial(filas),
        "otras_fuentes": otras_fuentes(),
        "subproducto_ebo": bloque_ebo(filas),
        "trampas_declaradas": TRAMPAS_DECLARADAS,
        "detalle": [
            {"num": f["num"], "lema": f["lema"], "siglas": ",".join(f["siglas"]),
             "glosa_verbatim": f["glosa_verbatim"], "tipos": f["tipos"],
             "dudoso": f["dudoso"], "por": f["por"]}
            for f in filas if f["tipos"] != ["otro"]],
    }

    # ── informe corto a pantalla ──
    print("═" * 70)
    print("NOMINALIZADOR — ¿hay algo que retroabstraer?")
    print("═" * 70)
    print(f"glosario de Zavala: {len(filas)} entradas")
    for t, n in resumen.items():
        print(f"  {t:<18} {n}")
    ca = doc["control_de_azar"]
    print(f"\nsubconjunto diana: {ca['diana']['n']} nombres "
          f"({ca['diana_sin_dudosas']['n']} sin las dudosas)")
    print("finales más enriquecidos del subconjunto diana:")
    for r in ca["diana"]["finales"][:8]:
        print(f"  {r['final']:<6} {r['en_el_subconjunto']:>2}/{r['tamano_subconjunto']:<3}"
              f" ({r['pct_subconjunto']:>4}%)  vs {r['en_las_288']:>3}/288"
              f" ({r['pct_288']:>4}%)  x{r['enriquecimiento']:<5} p={r['p_hipergeometrica']}")
    ps = doc["prueba_del_sufijo"]
    print(f"\nparejas base+resto en el glosario: {ps['parejas_totales']}")
    print(f"  de ellas VERBO + resto = NOMBRE de la diana: "
          f"{len(ps['base_verbal_derivada_nominal'])}")
    for p in ps["base_verbal_derivada_nominal"]:
        print(f"    {p['base']} (#{p['base_num']}) «{p['base_glosa'][:30]}»"
              f"  + -{p['resto']}  =  {p['derivada']} (#{p['derivada_num']})"
              f" «{p['derivada_glosa'][:40]}»")
    print(f"  y NOMBRE + resto = VERBO: {len(ps['base_nominal_derivada_verbal'])}")
    for p in ps["base_nominal_derivada_verbal"]:
        print(f"    {p['base']} (#{p['base_num']}) + -{p['resto']} = "
              f"{p['derivada']} (#{p['derivada_num']}) «{p['derivada_glosa'][:36]}»")
    print("\nfinales del subconjunto diana SIN las dudosas:")
    for r in ca["diana_sin_dudosas"]["finales"][:6]:
        print(f"  {r['final']:<6} {r['en_el_subconjunto']:>2}/{r['tamano_subconjunto']:<3}"
              f"  x{r['enriquecimiento']:<5} p={r['p_hipergeometrica']}")
    tc = doc["terminaciones_compartidas"]
    print(f"\nfinales que llevan A LA VEZ verbos y nombres diana: "
          f"{len(tc['finales_compartidos'])}")
    for r in tc["finales_compartidos"]:
        print(f"  {r['final']:<6} verbos={r['verbos_que_lo_llevan']} "
              f"nombres={r['nombres_que_lo_llevan']} "
              f"bases atestiguadas al quitarlo: {r['bases_atestiguadas']}")
    dc = doc["derivacion_cero"]
    print(f"\nUNA forma que glosa verbo Y nombre: {dc['casos']} "
          f"({dc['sin_dudosas']} sin las dudosas)")
    for c in dc["detalle"]:
        print(f"  {c['lema']:<14} (#{c['num']}, {c['siglas']}) «{c['glosa_verbatim']}»")
    rd = doc["reduplicacion_en_la_diana"]
    print(f"\nreduplicados dentro de la diana: {rd['reduplicados']}/{rd['nombres_diana']}"
          f"  (agentes: {rd['agentes_reduplicados']}/{rd['agentes']})")
    for c in rd["detalle"]:
        print(f"  {c['lema']:<14} ← {c['base']:<10} "
              f"[{'base atestiguada' if c['base_atestiguada'] else 'base NO atestiguada'}] "
              f"{c['reduplicacion']}  «{c['glosa_verbatim'][:38]}»")
    print("\nde quién vienen los verbos:",
          doc["de_quien_viene"]["verbos_por_compilador"])
    print("iniciales con verbos amontonados:")
    for r in doc["sonda_inicial"]["por_inicial"][:4]:
        print(f"  {r['inicial']}-  {r['verbos']}/{r['entradas_con_esa_inicial']}"
              f" ({r['pct']}%)  p={r['p_hipergeometrica']}")
    print("\nsubproducto `-ebo`:", doc["subproducto_ebo"]["cuantos"], "compuestos")
    for c in doc["subproducto_ebo"]["compuestos"]:
        print(f"  {c['lema']:<14} (#{c['num']}) «{c['glosa']}»")
    of = doc["otras_fuentes"]
    print(f"\nOliver A-9: {of['oliver_a9']['entradas_transcritas']} entradas, "
          f"{of['oliver_a9']['verbos_reales']} verbos "
          f"({of['oliver_a9']['de_ellas_falsos_positivos']} falso positivo: "
          f"{of['oliver_a9']['los_falsos']})")
    print(f"Medina dictado: {of['medina_colina_dictado']['entradas_dictadas']} "
          f"entradas, {of['medina_colina_dictado']['glosas_que_son_infinitivo']} verbos")

    if args.yaml:
        with open(args.yaml, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(volcar(doc)) + "\n")
        print(f"\n→ {args.yaml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
