#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — análisis POR NODO de la era 2
=======================================

La era 2 corre dos nodos —GUARANAO (39 agentes: los Tacuatos, los Cayudes y la
casa del Manaure en Moruy) y AMUAY (24: los Guasicures de Caseto y los Corubos
de Carirubana)— que sólo se juntan en el Capubana y por los que se casaron
cruzando. La pregunta del diseño (`5-experimento/DISENO_ERA2.md` §7) no es si
cada nodo converge consigo mismo —eso ya pasaba en la era 1— sino **si las
formas cruzan la frontera y si la distancia ENTRE nodos se contrae**.

Este módulo responde eso y nada más. `analizar_runs.py` sigue siendo el análisis
general de los runs; aquí sólo vive lo que necesita saber de qué lado de la
península se dijo cada cosa.

LO QUE MIDE
-----------
1. `--formas`  Para cada forma emergente, por día y por nodo: usos, hablantes
               distintos y la TASA por hablante posible del nodo. Los nodos
               tienen 39 y 24 agentes: comparar conteos crudos entre ellos dice
               más del censo que de la lengua. Clasifica cada forma en
               compartida / inclinada / exclusiva con un umbral declarado, y
               dice quién la acuñó y cuándo cruzó al otro nodo.
2. `--distancia`  La distancia idiolectal (1 − coseno, la misma de
               `curiana_koine.distancia_idiolectal`) partida en pares INTRA-nodo
               y pares ENTRE nodos, por día. La lectura que se busca: ¿la de
               entre nodos baja más rápido, igual o más lento que la intra?
3. `--lugar`   La ESCENA (tabla `presencias`, desde el 2026-09-17): ocupación
               por lugar y momento, cuántas escenas tuvieron más de un hablante
               y el cruce de las formas por LUGAR además de por nodo — incluido
               si pasaron por un lugar que tocan los dos nodos (el Capubana, el
               camino Moruy–Caseto). Es la lectura que el mapa aguanta y la
               frontera binaria no: Moruy–Caseto son 7,6 km y son de nodos
               distintos; Tacuato–El Cayude son 12,7 y son del mismo. Sobre un
               run anterior a la escena avisa y sigue.

EL MÉTODO, Y SU LÍMITE
----------------------
Los idiolectos (`curiana_koine.IdiolectoAgente`) **no se guardan por día en la
base**: sólo quedan, enteros y al cierre, en `curiana_koine.json`. Así que aquí
los vectores se RECONSTRUYEN desde `word_uses` × `turns`: el vector de un agente
en un día es el `Counter` de las formas caquetías que ese día dijo. Eso equivale
a la lectura de **ventana** del motor (habla real, sin las formas-semilla
pre-cargadas), con la ventana fijada al día en vez de a los últimos
`VENTANA_TURNOS`; no reproduce la lectura acumulada ni tiene por qué coincidir
con `koine_metrics.distance_ventana`, y el informe imprime las dos al lado para
que la diferencia se vea. La lectura **emergente** es la misma quitando de los
vectores lo que el motor tampoco cuenta (`curiana_lexicon.PUERTA_DEL_RECUENTO`,
la misma puerta con la que el motor rechaza en la registración: el vocabulario
base más lo que las plantillas enseñan, y —desde el corte del 2026-09-20— toda
forma con la RAÍZ fuera del lexicón).

LA RAÍZ DE NINGUNA PARTE
------------------------
Los runs ya corridos NO se reescriben: `lumina-bana-iro` sigue en `word_uses`
con `source_language='caquetío'`, que es lo que la base guardó. La cabecera del
informe la vuelve a clasificar AL LEER, dice cuántas formas y cuántos usos de
la cadena tienen la raíz fuera del lexicón, y compara la lectura emergente con
y sin ellas — para poder decir si el veredicto de esa cadena aguanta. ⚠️ Esa
serie se RECONSTRUYE de `word_uses` y no es `koine_metrics.distance_emergente`:
sólo vale para comparar consigo misma. La cifra del motor, con su veredicto, la
mide `6-fusion/scripts/medir_raices_de_ninguna_parte.py`.

⚠️ `word_uses.day` y `word_uses.turn_num` vienen NULL en los runs de la era 2:
el día se saca por join con `turns`, nunca de esas columnas.

LA CADENA DE RUNS
-----------------
Un run de la era 2 es UN día; los días se encadenan con `--continuar`, y el hijo
guarda a su padre en `config.continuado_desde`. Aquí se sube por esa columna
hasta la raíz con una implementación mínima y propia (`cadena_de_runs`), porque
sólo necesita la rama hacia atrás, que es única. La función general —bajar,
ramificar, listar campañas— la está escribiendo `analizar_runs.py`; cuando esté,
esto debería llamarla a ella.

CONEXIÓN
--------
Igual que `analizar_runs.py`: no psycopg2, sino `docker exec` + CSV. El
contenedor va por nombre porque en la misma máquina corre otro Supabase
(fintech) en los puertos 54321/54322; el de este proyecto está en 64321/64322.
Se lee con `csv`, no con pandas, a propósito: pandas convertiría una forma
llamada `na`, `nan` o `null` en un valor nulo.

Uso:
    python analizar_nodos.py --run 0193873d              # esa cadena, todo
    python analizar_nodos.py --run 0193873d --formas     # sólo las formas
    python analizar_nodos.py --run 0193873d --lugar      # sólo la escena
    python analizar_nodos.py --todo                      # las cadenas de la era 2
    python analizar_nodos.py --run 0193873d --json       # a stdout, para el informe
"""

import argparse
import csv
import io
import json
import math
import os
import subprocess
import sys
from collections import Counter, defaultdict
from textwrap import dedent
from typing import Iterable, Optional

CONTENEDOR = "supabase_db_curiana_sim"

# Los dos nodos de la era 2. El orden es el del diseño (GUARANAO primero: es el
# del Manaure y el del Capubana), no el alfabético.
NODOS = ("GUARANAO", "AMUAY")

# ── Los umbrales de clasificación, declarados aquí y no escondidos en el código ──
#
# `UMBRAL_INCLINACION`: cuántas veces más prevalente tiene que ser una forma en
# un nodo que en el otro —ya normalizada por hablantes posibles— para llamarla
# «inclinada». 2.0 = el doble. La razón de que sea 2 y no 1.3: con 39 y 24
# hablantes posibles y formas que llegan a un puñado de bocas, una diferencia
# menor cabe entera dentro de a quién le tocó hablar ese día (el roster rota 12
# agentes por turno). Es un umbral grueso a propósito; la tabla imprime siempre
# la razón cruda para que el lector aplique el suyo.
UMBRAL_INCLINACION = 2.0

# Por debajo de esto una forma no se clasifica: se dice `poco-atestiguada`. Con
# uno o dos hablantes, «exclusiva de AMUAY» y «la dijo un señor» son la misma
# frase.
MIN_HABLANTES = 3


# ══════════════════════════════════════════════════════════════════════
# 0. PLOMERÍA — consola, base de datos
# ══════════════════════════════════════════════════════════════════════

def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 y este módulo imprime ─, ✓ y acentos."""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def q(sql: str) -> list[dict]:
    """Corre SQL en el Postgres del contenedor y devuelve filas como dicts."""
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "--csv", "-c", dedent(sql)],
        capture_output=True, text=True, encoding="utf-8", timeout=180)
    if out.returncode != 0:
        raise RuntimeError(f"psql falló:\n{out.stderr.strip()[:500]}")
    return list(csv.DictReader(io.StringIO(out.stdout)))


def titulo(t: str) -> None:
    print(f"\n{'═' * 78}\n  {t}\n{'═' * 78}")


def sub(t: str) -> None:
    print(f"\n── {t} ──")


# ══════════════════════════════════════════════════════════════════════
# I. EL ELENCO — quién es de qué nodo
# ══════════════════════════════════════════════════════════════════════

def elenco_por_nodo() -> tuple[dict[str, str], dict[str, str], dict[str, int]]:
    """(nodo_de_agente, casa_de_agente, hablantes_posibles_por_nodo).

    Se lee `curiana_agents_era2` directo, sin pasar por `CURIANA_ELENCO`: aquí
    no se corre el motor, se analiza un run que YA declaró `elenco: era2` en su
    config, y forzar la variable de entorno cambiaría el elenco de cualquier
    otro módulo que el intérprete importe después.
    """
    import curiana_agents_era2 as era2
    nodo = {nm: a["nodo"] for nm, a in era2.ALL_AGENTS.items()}
    casa = {nm: a.get("casa") for nm, a in era2.ALL_AGENTS.items()}
    posibles = Counter(nodo.values())
    return nodo, casa, dict(posibles)


def divergencia_sembrada() -> dict:
    """¿Arrancan los dos nodos con habla distinta? Medido, no supuesto.

    `DISENO_ERA2.md` §1 dice «sembrar divergencia para medir convergencia», y
    `DISENO_KOINE.md` §4 lo pone más fuerte: «sin esta pre-carga, todos arrancan
    iguales y "convergencia" no significa nada». La pre-carga es
    `curiana_koine.formas_semilla()`. Esto cuenta cuántos vectores-semilla
    DISTINTOS hay entre los agentes del elenco activo y cuántos son propios del
    agente (`FORMAS_SEED`) en vez del núcleo compartido de reserva.

    Es la precondición de todo lo demás: si sale un vector para todos, la
    distancia entre nodos no puede contraerse porque nunca estuvo abierta.
    """
    import curiana_agents_era2 as era2
    from curiana_koine import EMOCIONAR_SEED, FORMAS_SEED, emocionar_de, formas_semilla
    nombres = set(era2.ALL_AGENTS)
    vectores = Counter()
    por_nodo: dict[str, set] = defaultdict(set)
    for nm in nombres:
        a = era2.ALL_AGENTS[nm]
        v = tuple(formas_semilla(nm, emocionar_de(nm, a.get("etnia"))))
        vectores[v] += 1
        por_nodo[a["nodo"]].add(v)
    mas_comun = vectores.most_common(1)[0] if vectores else ((), 0)
    return {
        "agentes": len(nombres),
        "con_formas_seed_propia": sorted(nombres & set(FORMAS_SEED)),
        "con_emocionar_seed_propio": sorted(nombres & set(EMOCIONAR_SEED)),
        "vectores_semilla_distintos": len(vectores),
        "agentes_con_el_vector_mas_comun": mas_comun[1],
        "vectores_por_nodo": {n: len(v) for n, v in sorted(por_nodo.items())},
        # Si los dos nodos comparten todos sus vectores-semilla, no hay
        # divergencia POR NODO aunque la hubiera por agente.
        "nodos_con_semilla_propia": sorted(
            n for n, v in por_nodo.items()
            if v - set().union(*(w for m, w in por_nodo.items() if m != n))),
    }


def formas_de_plantilla_solas() -> frozenset:
    """Sólo la mitad enumerable de la puerta: el vocabulario base y lo que las
    plantillas enseñan. Es la lectura de ANTES del corte del 2026-09-20, y
    existe para poder comparar con ella (`veredicto_sin_raiz_ajena`)."""
    from curiana_lexicon import FORMAS_DE_PLANTILLA
    return frozenset(FORMAS_DE_PLANTILLA)


def formas_excluidas():
    """Lo que NO puede contar como forma emergente.

    Es el mismo conjunto con el que el motor mide su distancia emergente y su
    diccionario koiné, y —desde el corte de serie del 2026-09-18— el mismo con
    el que RECHAZA en la registración: la puerta es una sola y vive en
    `curiana_lexicon.FORMAS_DE_PLANTILLA`. El vocabulario base MÁS lo que las
    plantillas del prompt enseñan. La segunda mitad importa: `ta-barsure` y
    `naba-ni` salen del ejemplo de la plantilla, no están en
    `VOCABULARIO_BASE` y aparecen en decenas de respuestas (run db946685,
    bitácora del 2026-09-14). Contarlas como koiné sería medir la plantilla.

    Desde el corte del 2026-09-20 es además LA RAÍZ DE NINGUNA PARTE, y por
    eso esto ya no es un `frozenset` sino un objeto que responde a `in`
    (`curiana_lexicon.PUERTA_DEL_RECUENTO`): las formas de plantilla se pueden
    enumerar y las raíces posibles no. Sigue siendo EL MISMO objeto que usa el
    motor (`curiana_orchestrator_v2._FORMAS_EXCLUIDAS`): la puerta es una.
    Quien necesite la lista de antes, `formas_de_plantilla_solas()`.

    Se importa del lexicón —no del orquestador, que arrastraba el bucle y su
    `load_dotenv`— para que no se puedan desincronizar; la importación es de
    sólo lectura.
    """
    from curiana_lexicon import PUERTA_DEL_RECUENTO
    return PUERTA_DEL_RECUENTO


# ══════════════════════════════════════════════════════════════════════
# II. LA CADENA DE RUNS
# ══════════════════════════════════════════════════════════════════════

def resolver_run(prefijo: str) -> str:
    """De un id8 (o un uuid entero) al uuid completo. Falla si es ambiguo."""
    filas = q(f"select id::text from simulation_runs where id::text like '{prefijo}%'")
    ids = [f["id"] for f in filas]
    if not ids:
        raise SystemExit(f"No hay run que empiece por {prefijo!r}")
    if len(ids) > 1:
        raise SystemExit(f"{prefijo!r} es ambiguo: {', '.join(i[:8] for i in ids)}")
    return ids[0]


def cadena_de_runs(run_id: str) -> list[dict]:
    """Sube por `config.continuado_desde` hasta la raíz. Devuelve raíz→hoja.

    Implementación MÍNIMA y propia: sólo la rama hacia atrás, que es única
    (un run tiene un padre o ninguno). La función general —bajar por los hijos,
    que sí ramifican: 89fc1744 tiene dos, el día 3 bueno y un arranque abortado—
    la está escribiendo `analizar_runs.py`. Cuando exista, llamarla a ella.
    """
    cadena: list[dict] = []
    vistos: set[str] = set()
    actual: Optional[str] = run_id
    while actual:
        if actual in vistos:
            raise SystemExit(f"Ciclo en continuado_desde alrededor de {actual[:8]}")
        vistos.add(actual)
        filas = q(f"""
            select id::text as id,
                   coalesce(total_days, 0) as total_days,
                   started_at::text as started_at,
                   coalesce(config->>'continuado_desde', '') as padre,
                   coalesce(config->>'elenco', '') as elenco,
                   coalesce(config->>'perfil', '') as perfil,
                   coalesce(config->>'semilla', '') as semilla,
                   coalesce(config->>'turnos_por_dia', '6') as turnos_por_dia,
                   coalesce(config->>'serie', '') as serie,
                   coalesce(config->>'escena', '') as escena,
                   coalesce(config->>'capubana_cada', '') as capubana_cada,
                   coalesce(config->>'motor_commit', '') as motor_commit
            from simulation_runs where id = '{actual}'
        """)
        if not filas:
            raise SystemExit(f"El run {actual[:8]} no está en la base")
        fila = filas[0]
        cadena.append(fila)
        actual = fila["padre"] or None
    cadena.reverse()
    return cadena


def cadenas_era2() -> list[list[dict]]:
    """Las cadenas de la era 2: una por cada hoja (run sin hijos)."""
    filas = q("""
        select id::text as id, coalesce(config->>'continuado_desde','') as padre
        from simulation_runs where config->>'elenco' = 'era2'
    """)
    ids = {f["id"] for f in filas}
    con_hijo = {f["padre"] for f in filas if f["padre"]}
    hojas = sorted(ids - con_hijo)
    return [cadena_de_runs(h) for h in hojas]


# ══════════════════════════════════════════════════════════════════════
# III. LOS DATOS DE LA CADENA
# ══════════════════════════════════════════════════════════════════════

def _lista_sql(ids: Iterable[str]) -> str:
    return ", ".join(f"'{i}'" for i in ids)


def cargar_usos(run_ids: list[str]) -> list[dict]:
    """(dia, turno, agente, forma, usos). El día sale de `turns`, no de
    `word_uses.day`, que viene NULL en la era 2."""
    filas = q(f"""
        select t.day as dia, t.turn_num as turno, w.agent_name as agente,
               w.word as forma, count(*) as usos
        from word_uses w join turns t on t.id = w.turn_id
        where w.run_id in ({_lista_sql(run_ids)})
        group by 1, 2, 3, 4
        order by 1, 2, 3
    """)
    for f in filas:
        f["dia"] = int(f["dia"])
        f["turno"] = int(f["turno"])
        f["usos"] = int(f["usos"])
    return filas


def cargar_neologismos(run_ids: list[str]) -> list[dict]:
    """El turno se saca por join con `turns` (proposed_turn_id): sin él, el
    cruce sólo se podría fechar por días, y un día trae seis turnos."""
    filas = q(f"""
        select n.form as forma, coalesce(n.meaning,'') as glosa,
               n.proposed_by as acunador,
               coalesce(n.proposed_day, coalesce(t.day, 0)) as dia,
               coalesce(t.turn_num, 0) as turno,
               coalesce(n.status,'') as estado
        from neologisms n left join turns t on t.id = n.proposed_turn_id
        where n.run_id in ({_lista_sql(run_ids)})
        order by 3, 4, 1
    """)
    for f in filas:
        f["dia"] = int(f["dia"])
        f["turno"] = int(f["turno"])
    return filas


def cargar_koine_lexicon(run_ids: list[str]) -> list[dict]:
    filas = q(f"""
        select concepto_id, coalesce(descripcion,'') as descripcion, form as forma,
               coalesce(fijada_dia, 0) as dia
        from koine_lexicon where run_id in ({_lista_sql(run_ids)})
    """)
    for f in filas:
        f["dia"] = int(f["dia"])
    return filas


def acunacion_sin_uso_registrado(run_ids: list[str]) -> dict:
    """Cuántas acuñaciones NO dejan su forma en `word_uses` en la misma
    respuesta que la acuña.

    No es una curiosidad: es el sesgo que hay que descontar antes de leer
    cualquier ruta de contagio. Al acuñar, la forma todavía no está en el
    léxico comunitario, así que `palabras_caquetias` no la reconoce y
    `words_used` no la recoge; el primer uso que SÍ queda en la base es el del
    que la adoptó, que puede ser del otro nodo. Medido, no supuesto: si sale
    0, esta reserva se cae y hay que borrarla.
    """
    filas = q(f"""
        with acu as (
          select n.form, n.proposed_by as agente, n.proposed_turn_id as turno
          from neologisms n where n.run_id in ({_lista_sql(run_ids)})
            and n.proposed_turn_id is not null
        )
        select count(*) as total,
               count(*) filter (where w.word is null) as sin_uso
        from acu left join word_uses w
          on w.turn_id = acu.turno and w.agent_name = acu.agente
         and w.word = acu.form
    """)
    f = filas[0] if filas else {"total": 0, "sin_uso": 0}
    total, sin_uso = int(f["total"]), int(f["sin_uso"])
    return {"acunaciones_con_turno": total, "sin_uso_registrado": sin_uso,
            "pct": round(100 * sin_uso / total, 1) if total else None}


def cargar_metricas_koine(run_ids: list[str]) -> list[dict]:
    return q(f"""
        select day as dia, distance, distance_ventana, distance_emergente, n_agents
        from koine_metrics where run_id in ({_lista_sql(run_ids)}) order by day
    """)


# ══════════════════════════════════════════════════════════════════════
# IV. CLASIFICACIÓN DE UNA FORMA — la pieza pura, la que testean los tests
# ══════════════════════════════════════════════════════════════════════

def tasas_por_nodo(hablantes: dict[str, int], posibles: dict[str, int]) -> dict[str, float]:
    """Hablantes distintos / hablantes posibles del nodo. La normalización sin
    la que 21 GUARANAO y 6 AMUAY parecen decir algo sobre la lengua."""
    return {n: (hablantes.get(n, 0) / posibles[n] if posibles.get(n) else 0.0)
            for n in posibles}


def clasificar_forma(hablantes: dict[str, int], posibles: dict[str, int],
                     umbral: float = UMBRAL_INCLINACION,
                     min_hablantes: int = MIN_HABLANTES) -> dict:
    """Clasifica una forma por su reparto entre nodos, YA normalizado.

    Devuelve `clase` ∈ {compartida, inclinada, exclusiva, poco-atestiguada,
    sin-usos} y, cuando aplica, el `nodo` al que se inclina o del que es
    exclusiva, más la `razon` de tasas (la mayor sobre la menor).

      exclusiva          — la tasa del otro nodo es 0.
      inclinada          — razón de tasas ≥ `umbral` (por defecto 2.0: el doble
                           de prevalencia normalizada).
      compartida         — razón < umbral en los dos sentidos.
      poco-atestiguada   — menos de `min_hablantes` bocas en total: no se
                           clasifica, porque con dos hablantes «exclusiva» y
                           «casualidad» son indistinguibles.

    La razón se calcula sobre TASAS (hablantes / hablantes posibles del nodo),
    nunca sobre conteos: GUARANAO tiene 39 agentes y AMUAY 24, y el nodo grande
    ganaría siempre.
    """
    total = sum(hablantes.get(n, 0) for n in posibles)
    tasas = tasas_por_nodo(hablantes, posibles)
    orden = sorted(posibles, key=lambda n: (-tasas[n], n))
    alto, bajo = orden[0], orden[-1]
    base = {
        "hablantes": {n: hablantes.get(n, 0) for n in posibles},
        "tasas": {n: round(tasas[n], 4) for n in posibles},
        "total_hablantes": total,
        "nodo_alto": alto,
    }
    if total == 0:
        return {**base, "clase": "sin-usos", "nodo": None, "razon": None}
    if total < min_hablantes:
        return {**base, "clase": "poco-atestiguada", "nodo": None,
                "razon": None}
    if tasas[bajo] == 0:
        return {**base, "clase": "exclusiva", "nodo": alto, "razon": math.inf}
    razon = tasas[alto] / tasas[bajo]
    if razon >= umbral:
        return {**base, "clase": "inclinada", "nodo": alto, "razon": round(razon, 2)}
    return {**base, "clase": "compartida", "nodo": None, "razon": round(razon, 2)}


# ══════════════════════════════════════════════════════════════════════
# V. LAS FORMAS EMERGENTES POR NODO Y POR DÍA
# ══════════════════════════════════════════════════════════════════════

def formas_emergentes(usos: list[dict], neologismos: list[dict],
                      koine: list[dict], excluidas: frozenset) -> set[str]:
    """Qué cuenta como forma emergente.

    Todo lo dicho en la cadena que no esté en `excluidas` (vocabulario base +
    lo que las plantillas enseñan), MÁS toda forma registrada como neologismo
    —adoptado o propuesto— y toda forma fijada en `koine_lexicon`, aunque no
    aparezca en `word_uses`.
    """
    emergentes = {f["forma"] for f in usos if f["forma"] not in excluidas}
    emergentes |= {n["forma"] for n in neologismos}
    emergentes |= {k["forma"] for k in koine}
    return emergentes


def perfil_de_forma(forma: str, usos_de_la_forma: list[dict], nodo_de: dict[str, str],
                    posibles: dict[str, int], dias: list[int],
                    neos: list[dict], en_koine: Optional[dict],
                    umbral: float, min_hablantes: int,
                    turnos_por_dia: int = 6) -> dict:
    """El renglón completo de una forma: por día y por nodo, su clasificación,
    quién la acuñó y cuándo cruzó."""
    por_dia: dict[int, dict[str, dict]] = {
        d: {n: {"usos": 0, "hablantes": set()} for n in posibles} for d in dias}
    total: dict[str, dict] = {n: {"usos": 0, "hablantes": set()} for n in posibles}
    primer_uso: Optional[tuple[int, int, str]] = None

    for u in usos_de_la_forma:
        nodo = nodo_de.get(u["agente"])
        if nodo is None:
            continue   # agente que no es del elenco era2: no se le inventa nodo
        d = u["dia"]
        if d in por_dia:
            por_dia[d][nodo]["usos"] += u["usos"]
            por_dia[d][nodo]["hablantes"].add(u["agente"])
        total[nodo]["usos"] += u["usos"]
        total[nodo]["hablantes"].add(u["agente"])
        clave = (u["dia"], u["turno"], u["agente"])
        if primer_uso is None or clave < primer_uso:
            primer_uso = clave

    # ── quién la acuñó ──
    # `neologisms` es la fuente buena: dice el agente que la propuso. Cuando la
    # forma no está registrada como neologismo (la mayoría: son formas nuevas
    # que nunca pasaron por el parser de neologismos) se usa el PRIMER USO de
    # la cadena como aproximación, y se declara como tal en `origen_acunacion`
    # — no es lo mismo acuñar que ser el primero al que se le oyó.
    #
    # ⚠️ La acuñación es PLURAL, y eso no es un detalle de implementación: los
    # eventos de nombramiento (`REFERENTES_NOVEDOSOS`, DISENO_KOINE §6) enseñan
    # el mismo referente a TODOS los agentes activos del turno, así que varios
    # acuñan a la vez — y a veces de los dos nodos. Cuando eso pasa, la forma
    # NACIÓ en los dos lados y «cruzó» no significa nada: se marca
    # `acunacion_multinodo` y el cruce queda en None con esa razón declarada.
    if neos:
        clave = min((n["dia"], n.get("turno") or 0) for n in neos)
        acunadores = sorted({n["acunador"] for n in neos
                             if (n["dia"], n.get("turno") or 0) == clave
                             and n.get("acunador")})
        dia_acu, turno_acu = clave
        origen = "neologisms"
    elif primer_uso:
        dia_acu, turno_acu, _ = primer_uso
        acunadores = sorted({u["agente"] for u in usos_de_la_forma
                             if (u["dia"], u["turno"]) == (dia_acu, turno_acu)})
        origen = "primer-uso"
    else:
        acunadores, dia_acu, turno_acu, origen = [], None, None, "sin-rastro"
    nodos_acu = sorted({nodo_de[a] for a in acunadores if a in nodo_de})
    multinodo = len(nodos_acu) > 1

    # ── cuándo cruzó: primer (día, turno) con uso en un nodo que NO acuñó. Con
    # turno y no sólo con día: un día son seis turnos y casi todo cruza «el
    # mismo día», que a esa resolución no dice nada.
    cruce = None
    if nodos_acu and not multinodo:
        ajenos = [(u["dia"], u["turno"]) for u in usos_de_la_forma
                  if nodo_de.get(u["agente"]) not in (None, *nodos_acu)]
        if ajenos:
            cruce = min(ajenos)
    dia_cruce, turno_cruce = cruce if cruce else (None, None)

    clasif = clasificar_forma({n: len(total[n]["hablantes"]) for n in posibles},
                              posibles, umbral, min_hablantes)

    glosas = [n["glosa"] for n in neos if n.get("glosa")]
    estados = sorted({n["estado"] for n in neos if n.get("estado")})
    return {
        "forma": forma,
        "glosa": glosas[0] if glosas else "",
        "es_neologismo": bool(neos),
        "n_registros_neologismo": len(neos),
        "estado_neologismo": "/".join(estados),
        "fijada_en_koine": bool(en_koine),
        "concepto_koine": (en_koine or {}).get("concepto_id", ""),
        "usos_totales": sum(total[n]["usos"] for n in posibles),
        "por_nodo": {n: {"usos": total[n]["usos"],
                         "hablantes": len(total[n]["hablantes"]),
                         "posibles": posibles[n],
                         "tasa": round(len(total[n]["hablantes"]) / posibles[n], 4),
                         "usos_por_posible": round(total[n]["usos"] / posibles[n], 3)}
                     for n in posibles},
        "por_dia": {str(d): {n: {"usos": por_dia[d][n]["usos"],
                                 "hablantes": len(por_dia[d][n]["hablantes"]),
                                 "tasa": round(len(por_dia[d][n]["hablantes"]) / posibles[n], 4)}
                             for n in posibles}
                    for d in sorted(dias)},
        "clase": clasif["clase"],
        "nodo_de_la_clase": clasif["nodo"],
        "razon_de_tasas": (None if clasif["razon"] in (None, math.inf)
                           else clasif["razon"]),
        "razon_infinita": clasif["razon"] is math.inf,
        "acunadores": acunadores,
        "nodos_acunadores": nodos_acu,
        "acunacion_multinodo": multinodo,
        "dia_acunacion": dia_acu,
        "turno_acunacion": turno_acu,
        "origen_acunacion": origen,
        "dia_cruce": dia_cruce,
        "turno_cruce": turno_cruce,
        "dias_hasta_cruzar": (None if (dia_cruce is None or dia_acu is None)
                              else dia_cruce - dia_acu),
        "turnos_hasta_cruzar": (
            None if (cruce is None or dia_acu is None) else
            (dia_cruce - dia_acu) * turnos_por_dia + (turno_cruce - (turno_acu or 0))),
        "cruzo": cruce is not None,
        "cruce_no_aplica": multinodo,
    }


def analizar_formas(usos: list[dict], neologismos: list[dict], koine: list[dict],
                    nodo_de: dict[str, str], posibles: dict[str, int],
                    excluidas: frozenset, umbral: float = UMBRAL_INCLINACION,
                    min_hablantes: int = MIN_HABLANTES,
                    turnos_por_dia: int = 6) -> list[dict]:
    """Todas las formas emergentes de la cadena, ordenadas por usos."""
    emergentes = formas_emergentes(usos, neologismos, koine, excluidas)
    dias = sorted({u["dia"] for u in usos})
    por_forma: dict[str, list[dict]] = defaultdict(list)
    for u in usos:
        if u["forma"] in emergentes:
            por_forma[u["forma"]].append(u)
    # TODOS los registros de neologismo de cada forma, no sólo uno: la misma
    # forma la proponen varios agentes en el mismo turno de nombramiento y
    # quedarse con uno inventaría un acuñador único donde hubo cinco.
    neo_de: dict[str, list[dict]] = defaultdict(list)
    for n in neologismos:
        neo_de[n["forma"]].append(n)
    koine_de = {k["forma"]: k for k in koine}

    filas = [perfil_de_forma(f, por_forma.get(f, []), nodo_de, posibles, dias,
                             neo_de.get(f, []), koine_de.get(f), umbral,
                             min_hablantes, turnos_por_dia)
             for f in sorted(emergentes)]
    filas.sort(key=lambda r: (-r["usos_totales"], r["forma"]))
    return filas


# ══════════════════════════════════════════════════════════════════════
# VI. DISTANCIA IDIOLECTAL INTRA-NODO Y ENTRE NODOS
# ══════════════════════════════════════════════════════════════════════

def _coseno(a: Counter, b: Counter) -> float:
    """El coseno de `curiana_koine`. Se importa de allí y sólo se copia la
    firma si el motor no está disponible (no debería pasar)."""
    from curiana_koine import _coseno as coseno_motor
    return coseno_motor(a, b)


def distancias_intra_entre(vectores: dict[str, Counter], nodo_de: dict[str, str],
                           min_formas: int = 5) -> dict:
    """Distancia media (1 − coseno) partida en pares intra-nodo y pares cruzados.

    `vectores`: agente → Counter de formas. Se descartan los agentes con menos
    de `min_formas` formas distintas, igual que `distancia_idiolectal`: un
    vector de dos palabras no mide una manera de hablar.

    Devuelve `intra` por nodo, `intra_global` (todos los pares del mismo nodo,
    sean del que sean), `entre` (pares cruzados) y `brecha` = entre − intra
    global. Un valor es None cuando no hay pares que lo sostengan: sin datos no
    es lo mismo que distancia cero.
    """
    activos = {nm: v for nm, v in vectores.items()
               if len(v) >= min_formas and nm in nodo_de}
    nombres = sorted(activos)
    intra: dict[str, list[float]] = defaultdict(list)
    entre: list[float] = []
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            a, b = nombres[i], nombres[j]
            d = 1.0 - _coseno(activos[a], activos[b])
            if nodo_de[a] == nodo_de[b]:
                intra[nodo_de[a]].append(d)
            else:
                entre.append(d)

    def media(xs: list[float]) -> Optional[float]:
        return round(sum(xs) / len(xs), 4) if xs else None

    todos_intra = [d for xs in intra.values() for d in xs]
    res = {
        "n_agentes": len(activos),
        "agentes_por_nodo": dict(Counter(nodo_de[nm] for nm in activos)),
        "intra": {n: media(xs) for n, xs in sorted(intra.items())},
        "pares_intra": {n: len(xs) for n, xs in sorted(intra.items())},
        "intra_global": media(todos_intra),
        "pares_intra_global": len(todos_intra),
        "entre": media(entre),
        "pares_entre": len(entre),
    }
    res["brecha"] = (None if res["entre"] is None or res["intra_global"] is None
                     else round(res["entre"] - res["intra_global"], 4))
    return res


def vectores_por_dia(usos: list[dict], excluir: Optional[frozenset] = None,
                     acumulado: bool = False) -> dict[int, dict[str, Counter]]:
    """Reconstruye el vector de formas de cada agente desde `word_uses`.

    Por defecto, un vector por agente y día (la lectura de VENTANA, con la
    ventana fijada al día). Con `acumulado`, el vector del día d incluye todo lo
    dicho del día 1 al d: es la lectura que menos sufre de que un agente hable
    poco en un día suelto, a cambio de converger sola por acumulación —el
    artefacto que `DISENO_KOINE.md` §7 documenta—, así que se lee como control,
    no como veredicto. Con `excluir` queda la lectura EMERGENTE.
    """
    salida: dict[int, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    dias = sorted({u["dia"] for u in usos})
    for u in usos:
        if excluir and u["forma"] in excluir:
            continue
        destinos = [d for d in dias if d >= u["dia"]] if acumulado else [u["dia"]]
        for d in destinos:
            salida[d][u["agente"]][u["forma"]] += u["usos"]
    return {d: dict(ag) for d, ag in salida.items()}


# Las tres lecturas que los datos de la base permiten. `min_formas` copia los
# valores con los que el motor llama a `distancia_idiolectal` (5 normal, 3 en la
# emergente, donde los vectores son mucho más cortos).
LECTURAS = ("ventana", "emergente", "acumulada_emergente")


def analizar_distancia(usos: list[dict], nodo_de: dict[str, str],
                       excluidas: frozenset) -> list[dict]:
    """Por día, la distancia intra/entre en las tres lecturas."""
    vect = {
        "ventana": (vectores_por_dia(usos), 5),
        "emergente": (vectores_por_dia(usos, excluir=excluidas), 3),
        "acumulada_emergente": (
            vectores_por_dia(usos, excluir=excluidas, acumulado=True), 3),
    }
    filas = []
    for dia in sorted({u["dia"] for u in usos}):
        fila = {"dia": dia}
        for nombre, (v, min_f) in vect.items():
            fila[nombre] = distancias_intra_entre(v.get(dia, {}), nodo_de,
                                                  min_formas=min_f)
        filas.append(fila)
    return filas


def raices_de_ninguna_parte(usos: list[dict]) -> dict:
    """Lo que la base guardó como «caquetío» con la RAÍZ fuera del lexicón.

    El corte del 2026-09-20 se lo cierra al motor, pero los runs ya corridos NO
    se reescriben: `lumina-bana-iro` sigue en `word_uses` con
    `source_language='caquetío'`. Esto lo vuelve a clasificar AL LEER, para que
    los seis runs de la serie C se puedan leer con el dato.

    ⚠ Falso positivo declarado: el lexicón se mueve. Una forma cuya raíz era
    canon el día del run y hoy no lo es sale aquí sin serlo entonces —pasa en
    la era 1 (`chacamba`, `canoa`)—. Para la era 2 no hay ninguna, y la
    reconstrucción commit a commit la hace
    `6-fusion/scripts/medir_raices_de_ninguna_parte.py`.
    """
    from curiana_lexicon import es_raiz_de_ninguna_parte, nucleo_de_token
    formas = {u["forma"] for u in usos}
    ajenas = {f for f in formas if es_raiz_de_ninguna_parte(f)}
    usos_ajenos = sum(u["usos"] for u in usos if u["forma"] in ajenas)
    por_raiz: Counter = Counter()
    for u in usos:
        if u["forma"] in ajenas:
            por_raiz["-".join(nucleo_de_token(u["forma"]))] += u["usos"]
    return {
        "formas": len(ajenas),
        "de_formas_totales": len(formas),
        "usos": usos_ajenos,
        "de_usos_totales": sum(u["usos"] for u in usos),
        "raices": dict(por_raiz.most_common()),
        "lista": sorted(ajenas),
        "set": frozenset(ajenas),          # se quita antes de volcar el JSON
    }


def _distancia_global(d: dict) -> Optional[float]:
    """La distancia media sobre TODOS los pares, de la partición intra/entre.

    `distancias_intra_entre` devuelve las dos mitades y sus tamaños; la media
    global es la ponderada. Es la lectura que el veredicto juzga (el motor la
    calcula con `distancia_idiolectal`, sobre sus propios vectores; aquí se
    reconstruye de `word_uses`, así que **sólo se compara consigo misma** —con
    y sin las raíces ajenas—, nunca con la cifra del motor.
    """
    n_i, n_e = d.get("pares_intra_global") or 0, d.get("pares_entre") or 0
    if not (n_i + n_e):
        return None
    suma = ((d["intra_global"] or 0.0) * n_i) + ((d["entre"] or 0.0) * n_e)
    return round(suma / (n_i + n_e), 4)


def veredicto_sin_raiz_ajena(usos: list[dict], nodo_de: dict[str, str],
                             solo_plantilla: frozenset,
                             ajenas: frozenset) -> dict:
    """El veredicto de convergencia con y sin las raíces de ninguna parte.

    La pregunta que el defecto obliga a hacer: `lumina-bana-uco` fijó el cometa
    en el brazo de control y pesaba en la métrica emergente. ¿Se sostiene el
    CONVERGE al descontar las formas de raíz ajena? Se reconstruye la serie
    emergente día a día de las dos maneras y se pasa por el MISMO criterio que
    el motor (`curiana_koine.veredicto_convergencia`), para que no se juzguen
    con varas distintas.
    """
    from curiana_koine import veredicto_convergencia
    salida = {}
    for nombre, excluir in (("con_raiz_ajena", solo_plantilla),
                            ("sin_raiz_ajena", solo_plantilla | ajenas)):
        vect = vectores_por_dia(usos, excluir=excluir)
        serie = []
        for dia in sorted(vect):
            d = distancias_intra_entre(vect[dia], nodo_de, min_formas=3)
            g = _distancia_global(d)
            if g is not None:
                serie.append((dia, g))
        codigo, mensaje = veredicto_convergencia(serie)
        salida[nombre] = {"serie": [[d, v] for d, v in serie],
                          "codigo": codigo, "mensaje": mensaje}
    salida["se_sostiene"] = (
        salida["con_raiz_ajena"]["codigo"] == salida["sin_raiz_ajena"]["codigo"])
    return salida


def tendencia(filas: list[dict], lectura: str) -> dict:
    """¿Bajó más rápido la de entre nodos o la intra? Compara el primer día con
    el último en puntos absolutos y en porcentaje del valor inicial."""
    puntos = [(f["dia"], f[lectura]["intra_global"], f[lectura]["entre"])
              for f in filas
              if f[lectura]["intra_global"] is not None and f[lectura]["entre"] is not None]
    if len(puntos) < 2:
        return {"veredicto": "insuficiente", "puntos": len(puntos)}
    (d0, i0, e0), (dn, i_n, e_n) = puntos[0], puntos[-1]
    d_intra, d_entre = i_n - i0, e_n - e0
    rel_intra = d_intra / i0 if i0 else 0.0
    rel_entre = d_entre / e0 if e0 else 0.0
    # Umbral de 2 puntos porcentuales de caída relativa para llamar «más
    # rápido» a una de las dos: por debajo de eso, con tres días, la diferencia
    # no se distingue del ruido de quién habló.
    margen = 0.02
    if rel_entre < rel_intra - margen:
        veredicto = "entre-nodos-baja-mas-rapido"
    elif rel_intra < rel_entre - margen:
        veredicto = "intra-nodo-baja-mas-rapido"
    else:
        veredicto = "bajan-igual"
    return {
        "veredicto": veredicto, "dia_inicial": d0, "dia_final": dn,
        "intra": [round(i0, 4), round(i_n, 4)], "entre": [round(e0, 4), round(e_n, 4)],
        "delta_intra": round(d_intra, 4), "delta_entre": round(d_entre, 4),
        "delta_rel_intra": round(rel_intra, 4), "delta_rel_entre": round(rel_entre, 4),
        "brecha": [round(e0 - i0, 4), round(e_n - i_n, 4)],
        "margen": margen, "puntos": len(puntos),
    }


# ══════════════════════════════════════════════════════════════════════
# VII. VOLUMEN DE HABLA POR NODO — la reserva obligatoria
# ══════════════════════════════════════════════════════════════════════

def cobertura_del_elenco(usos: list[dict], nodo_de: dict[str, str]) -> dict:
    """Cuánto de lo hablado en la cadena se puede asignar a un nodo.

    Hace falta porque `config.elenco = era2` no garantiza que los nombres sean
    los del elenco de hoy: el run aafc5c32 (2026-09-14) declara era2 y habla con
    los nombres de la era 1, de antes de la campaña de antropónimos. Sin un nodo
    por agente, todo lo de este módulo es aire — así que se mide y se avisa,
    en vez de producir una tabla que parezca llena.
    """
    agentes = {u["agente"] for u in usos}
    conocidos = {a for a in agentes if a in nodo_de}
    usos_tot = sum(u["usos"] for u in usos) or 1
    usos_conocidos = sum(u["usos"] for u in usos if u["agente"] in nodo_de)
    return {
        "agentes_en_la_base": len(agentes),
        "agentes_con_nodo": len(conocidos),
        "agentes_sin_nodo": sorted(agentes - conocidos)[:20],
        "n_agentes_sin_nodo": len(agentes - conocidos),
        "pct_usos_con_nodo": round(100 * usos_conocidos / usos_tot, 1),
    }


def habla_por_nodo(usos: list[dict], nodo_de: dict[str, str],
                   posibles: dict[str, int]) -> list[dict]:
    """Cuánto habló cada nodo cada día. Sin esto no se puede leer nada de lo de
    arriba: GUARANAO tiene 39 agentes de 63 y si habla más, todo conteo crudo
    se le inclina por censo."""
    filas = []
    dias = sorted({u["dia"] for u in usos})
    for dia in dias:
        del_dia = [u for u in usos if u["dia"] == dia]
        fila = {"dia": dia, "nodos": {}}
        tot_usos = sum(u["usos"] for u in del_dia) or 1
        for n in posibles:
            ds = [u for u in del_dia if nodo_de.get(u["agente"]) == n]
            us = sum(u["usos"] for u in ds)
            fila["nodos"][n] = {
                "usos": us,
                "cuota_de_usos": round(us / tot_usos, 4),
                "agentes_activos": len({u["agente"] for u in ds}),
                "posibles": posibles[n],
                "cuota_del_censo": round(posibles[n] / sum(posibles.values()), 4),
                "formas_distintas": len({u["forma"] for u in ds}),
            }
        filas.append(fila)
    return filas


# ══════════════════════════════════════════════════════════════════════
# VII-bis. LA ESCENA — dónde estuvo cada quien, y dónde se dijo cada cosa
# ══════════════════════════════════════════════════════════════════════
#
# Todo esto sale de `presencias` (migración 20260917000000), que guarda a los 63
# agentes en cada uno de los seis momentos del día y no sólo a los 12 que
# hablan. Antes de ella no había columna de lugar en ninguna tabla: el único
# modo de saber dónde estaba alguien era su `ubicacion_default`, que no cambia
# nunca. Un run anterior —o corrido con `--sin-escena`— no tiene filas aquí, y
# esta sección lo dice y sigue en vez de imprimir una tabla vacía que parezca
# llena.

def hay_tabla_presencias() -> bool:
    """¿Está la migración aplicada en ESTA base? Se pregunta antes de leer
    porque una base sin migrar hace fallar la consulta entera, y el resto del
    informe (formas, distancia) no depende de la escena."""
    filas = q("""
        select count(*) as n from information_schema.tables
        where table_schema = 'public' and table_name = 'presencias'
    """)
    return bool(filas) and int(filas[0]["n"]) > 0


def cargar_presencias(run_ids: list[str]) -> list[dict]:
    """(dia, turno, momento, agente, lugar, nodo, run). El nodo se lee de la
    FILA y no del elenco de hoy: el módulo del elenco es generado y se
    regenera, y lo que hay que saber es de qué lado estaba la gente el día del
    run."""
    filas = q(f"""
        select p.day as dia, p.turn_num as turno,
               coalesce(p.momento, '') as momento,
               p.agent_name as agente, p.lugar as lugar,
               coalesce(p.nodo, '') as nodo, p.run_id::text as run
        from presencias p
        where p.run_id in ({_lista_sql(run_ids)}) and p.lugar is not null
        order by 1, 2, 5, 4
    """)
    for f in filas:
        f["dia"] = int(f["dia"])
        f["turno"] = int(f["turno"])
    return filas


def cargar_hablantes(run_ids: list[str]) -> list[dict]:
    """Quién habló en cada turno, con el lugar DESNORMALIZADO de
    `agent_responses.lugar` (vacío si el run no lo escribió). Una fila por
    respuesta: es la que decide si una escena tuvo una voz o varias."""
    filas = q(f"""
        select t.day as dia, t.turn_num as turno, r.agent_name as agente,
               coalesce(r.lugar, '') as lugar
        from agent_responses r join turns t on t.id = r.turn_id
        where r.run_id in ({_lista_sql(run_ids)})
        order by 1, 2, 3
    """)
    for f in filas:
        f["dia"] = int(f["dia"])
        f["turno"] = int(f["turno"])
    return filas


def orden_de_momentos(presencias: list[dict]) -> list[str]:
    """Los momentos del día, en el orden en que ocurren. MEDIDO del turno en el
    que aparece cada uno, no escrito: si un día corre con otro número de
    momentos, la tabla sigue saliendo bien."""
    primero: dict[str, int] = {}
    for p in presencias:
        m = p["momento"] or f"turno {p['turno']}"
        primero[m] = min(primero.get(m, p["turno"]), p["turno"])
    return sorted(primero, key=lambda m: (primero[m], m))


def ocupacion_por_lugar(presencias: list[dict]) -> list[dict]:
    """Cuánta gente hubo en cada lugar, por momento.

    La cifra que se imprime es la MEDIA POR DÍA (presencias del par
    lugar×momento / días en que ese momento se corrió), no el total: una cadena
    de tres días triplicaría los conteos y parecería que el mundo se llenó.
    """
    dias_del_momento: dict[str, set] = defaultdict(set)
    for p in presencias:
        dias_del_momento[p["momento"]].add(p["dia"])

    por_lugar: dict[str, dict[str, set]] = defaultdict(lambda: defaultdict(set))
    agentes: dict[str, set] = defaultdict(set)
    nodos: dict[str, set] = defaultdict(set)
    for p in presencias:
        por_lugar[p["lugar"]][p["momento"]].add((p["dia"], p["agente"]))
        agentes[p["lugar"]].add(p["agente"])
        if p["nodo"]:
            nodos[p["lugar"]].add(p["nodo"])

    filas = []
    for lugar, momentos in por_lugar.items():
        celdas = {}
        for m, pares in momentos.items():
            dias = len(dias_del_momento[m]) or 1
            celdas[m] = {"presencias": len(pares),
                         "media_por_dia": round(len(pares) / dias, 2)}
        filas.append({
            "lugar": lugar,
            "presencias": sum(c["presencias"] for c in celdas.values()),
            "agentes_distintos": len(agentes[lugar]),
            "nodos": sorted(nodos[lugar]),
            "por_momento": celdas,
        })
    filas.sort(key=lambda f: (-f["presencias"], f["lugar"]))
    return filas


def lugares_compartidos(presencias: list[dict]) -> dict:
    """Qué lugares tocan los DOS nodos — y si los tocan a la vez.

    La distinción es la de §3.4 del diseño: un lugar «compartido» donde los dos
    nodos nunca coinciden en el mismo turno no produce contacto, sólo
    coincidencia en el plano. La escena derivada daba CERO simultáneos sobre el
    papel; aquí se mide sobre lo que el run guardó de verdad.
    """
    nodos_de: dict[str, set] = defaultdict(set)
    por_turno: dict[tuple, set] = defaultdict(set)
    for p in presencias:
        if not p["nodo"]:
            continue
        nodos_de[p["lugar"]].add(p["nodo"])
        por_turno[(p["dia"], p["turno"], p["lugar"])].add(p["nodo"])

    simultaneos = {clave[2] for clave, ns in por_turno.items() if len(ns) > 1}
    filas = [{"lugar": lugar, "nodos": sorted(ns), "compartido": len(ns) > 1,
              "simultaneo": lugar in simultaneos}
             for lugar, ns in sorted(nodos_de.items())]
    return {
        "lugares": filas,
        "n_lugares": len(filas),
        "compartidos": sorted(f["lugar"] for f in filas if f["compartido"]),
        "compartidos_simultaneos": sorted(simultaneos),
        "turnos_con_dos_nodos": sum(1 for ns in por_turno.values() if len(ns) > 1),
    }


def escenas_del_turno(presencias: list[dict], hablantes: list[dict]) -> dict:
    """Una ESCENA es (día, turno, lugar) con alguien dentro. ¿Cuántas tuvieron
    más de una voz?

    Es la medición que decide si la capa 2 (oír por lugar) tiene material: una
    escena de una sola voz es un ámbito vacío — el dato, no el fallo, pero nadie
    oye a nadie allí. Se cuenta también por HABLANTE, que es la cifra que
    importa: qué porcentaje de las intervenciones cae en un lugar donde ese
    mismo turno habla alguien más.
    """
    lugar_de = {(p["dia"], p["turno"], p["agente"]): p["lugar"] for p in presencias}
    presentes: dict[tuple, set] = defaultdict(set)
    for p in presencias:
        presentes[(p["dia"], p["turno"], p["lugar"])].add(p["agente"])

    voces: dict[tuple, set] = defaultdict(set)
    sin_presencia = []
    declarado_discrepa = 0
    con_lugar_declarado = 0
    for h in hablantes:
        lugar = lugar_de.get((h["dia"], h["turno"], h["agente"]))
        if h["lugar"]:
            con_lugar_declarado += 1
            if lugar is not None and h["lugar"] != lugar:
                declarado_discrepa += 1
        if lugar is None:
            sin_presencia.append(h["agente"])
            continue
        voces[(h["dia"], h["turno"], lugar)].add(h["agente"])

    escenas = sorted(presentes)
    n_voces = {e: len(voces.get(e, ())) for e in escenas}
    con_compania = sum(len(voces[e]) for e in voces if len(voces[e]) >= 2)
    intervenciones = sum(len(v) for v in voces.values())
    return {
        "escenas": len(escenas),
        "escenas_con_voz": sum(1 for e in escenas if n_voces[e] >= 1),
        "escenas_con_dos_o_mas_voces": sum(1 for e in escenas if n_voces[e] >= 2),
        "voces_max_en_una_escena": max(n_voces.values(), default=0),
        "intervenciones_ubicadas": intervenciones,
        "intervenciones_con_compania": con_compania,
        "pct_con_compania": (round(100 * con_compania / intervenciones, 1)
                             if intervenciones else None),
        "hablantes_sin_presencia": len(sin_presencia),
        "respuestas_con_lugar_declarado": con_lugar_declarado,
        "respuestas_totales": len(hablantes),
        "lugar_declarado_discrepa": declarado_discrepa,
        "presencias_por_turno": (round(len(presencias) /
                                       len({(p["dia"], p["turno"]) for p in presencias}), 1)
                                 if presencias else None),
    }


def cruce_por_lugar(usos: list[dict], presencias: list[dict],
                    excluidas: frozenset, neologismos: list[dict],
                    koine: list[dict], compartidos: set,
                    turnos_por_dia: int = 6) -> list[dict]:
    """El cruce de una forma, pero por LUGAR en vez de por nodo.

    La lectura que el mapa aguanta y la frontera binaria no (§5.2 del diseño):
    Moruy–Caseto son 7,6 km y son de nodos distintos; Tacuato–El Cayude son 12,7
    y son del mismo. Por cada forma emergente: dónde se dijo primero, en cuántos
    lugares se dijo, cuándo salió del suyo, y si pasó por un lugar que tocan los
    dos nodos —el Capubana, el camino— que es por donde el diseño espera que
    salga.

    Una forma cuyos usos no se pueden ubicar (el agente no tiene presencia ese
    turno) queda `ubicable: False` y no entra en los resúmenes: es preferible
    contar menos que fechar un viaje que no se vio.
    """
    lugar_de = {(p["dia"], p["turno"], p["agente"]): p["lugar"] for p in presencias}
    emergentes = formas_emergentes(usos, neologismos, koine, excluidas)

    por_forma: dict[str, list[dict]] = defaultdict(list)
    for u in usos:
        if u["forma"] in emergentes:
            por_forma[u["forma"]].append(u)

    filas = []
    for forma in sorted(por_forma):
        ubicados = []
        sin_ubicar = 0
        for u in por_forma[forma]:
            lugar = lugar_de.get((u["dia"], u["turno"], u["agente"]))
            if lugar is None:
                sin_ubicar += 1
            else:
                ubicados.append((u["dia"], u["turno"], lugar, u["agente"]))
        if not ubicados:
            filas.append({"forma": forma, "ubicable": False, "usos_sin_ubicar": sin_ubicar})
            continue
        ubicados.sort()
        d0, t0, lugar0, _ = ubicados[0]
        # El lugar de nacimiento es plural si en ese mismo (día, turno) la forma
        # sonó en dos sitios: entonces no nació en ninguno y «salir» no
        # significa nada, igual que `acunacion_multinodo` con los nodos.
        natales = sorted({l for d, t, l, _ in ubicados if (d, t) == (d0, t0)})
        fuera = [(d, t, l) for d, t, l, _ in ubicados if l not in natales]
        salida = min(fuera) if fuera else None
        lugares = sorted({l for _, _, l, _ in ubicados})
        en_compartido = sorted(set(lugares) & compartidos)
        filas.append({
            "forma": forma,
            "ubicable": True,
            "usos_ubicados": len(ubicados),
            "usos_sin_ubicar": sin_ubicar,
            "lugares": lugares,
            "n_lugares": len(lugares),
            "lugares_natales": natales,
            "nacimiento_multilugar": len(natales) > 1,
            "dia_nacimiento": d0,
            "turno_nacimiento": t0,
            "dia_salida": salida[0] if salida else None,
            "turno_salida": salida[1] if salida else None,
            "lugar_salida": salida[2] if salida else None,
            "turnos_hasta_salir": (None if salida is None else
                                   (salida[0] - d0) * turnos_por_dia + (salida[1] - t0)),
            "murio_en_su_lugar": salida is None and len(natales) == 1,
            "lugares_compartidos_tocados": en_compartido,
            "paso_por_compartido": bool(en_compartido),
        })
    filas.sort(key=lambda f: (-f.get("usos_ubicados", 0), f["forma"]))
    return filas


def resumen_cruce_por_lugar(filas: list[dict]) -> dict:
    """Las cifras del cruce por lugar, todas contadas de `cruce_por_lugar`."""
    ubicables = [f for f in filas if f["ubicable"]]
    salieron = [f for f in ubicables if f["turnos_hasta_salir"] is not None]
    dts = sorted(f["turnos_hasta_salir"] for f in salieron)
    return {
        "formas": len(filas),
        "ubicables": len(ubicables),
        "sin_ubicar": len(filas) - len(ubicables),
        "murieron_en_su_lugar": sum(1 for f in ubicables if f["murio_en_su_lugar"]),
        "nacieron_en_varios_lugares": sum(1 for f in ubicables
                                          if f["nacimiento_multilugar"]),
        "salieron_de_su_lugar": len(salieron),
        "turnos_hasta_salir_mediana": dts[len(dts) // 2] if dts else None,
        "turnos_hasta_salir_min": dts[0] if dts else None,
        "turnos_hasta_salir_max": dts[-1] if dts else None,
        "mismo_turno": sum(1 for d in dts if d == 0),
        "pasaron_por_compartido": sum(1 for f in ubicables if f["paso_por_compartido"]),
        "lugares_distintos_mediana": (
            sorted(f["n_lugares"] for f in ubicables)[len(ubicables) // 2]
            if ubicables else None),
    }


def analizar_lugar(run_ids: list[str], usos: list[dict], neologismos: list[dict],
                   koine: list[dict], excluidas: frozenset,
                   turnos_por_dia: int = 6) -> dict:
    """La sección `--lugar` entera. Devuelve `disponible: False` con su motivo
    —y nada más— cuando la base o el run no tienen escena: un run viejo se avisa
    y se sigue, no se rompe."""
    if not hay_tabla_presencias():
        return {"disponible": False,
                "motivo": "esta base no tiene la tabla `presencias` (migración "
                          "20260917000000 sin aplicar)"}
    presencias = cargar_presencias(run_ids)
    hablantes = cargar_hablantes(run_ids)
    if not presencias:
        return {"disponible": False, "respuestas": len(hablantes),
                "motivo": "esta cadena corrió SIN escena: 0 filas en `presencias`"}
    comp = lugares_compartidos(presencias)
    cruce = cruce_por_lugar(usos, presencias, excluidas, neologismos, koine,
                            set(comp["compartidos"]), turnos_por_dia)
    por_run = Counter(p["run"] for p in presencias)
    return {
        "disponible": True,
        "presencias": len(presencias),
        "por_run": {r[:8]: por_run[r] for r in run_ids if r in por_run},
        "dias": sorted({p["dia"] for p in presencias}),
        "momentos": orden_de_momentos(presencias),
        "agentes_en_escena": len({p["agente"] for p in presencias}),
        "ocupacion": ocupacion_por_lugar(presencias),
        "compartidos": comp,
        "escenas": escenas_del_turno(presencias, hablantes),
        "cruce": cruce,
        "resumen_cruce": resumen_cruce_por_lugar(cruce),
    }


# ══════════════════════════════════════════════════════════════════════
# VIII. INFORME
# ══════════════════════════════════════════════════════════════════════

def brazo_de_la_cadena(cadena: list[dict]) -> dict:
    """Con qué brazo corrió la cadena, leído de `simulation_runs.config`.

    La escena es un BRAZO, no un parche: la evidencia es la diferencia entre
    dos cadenas completas con la misma semilla (diseño §5.4), así que el
    informe tiene que decir cuál está leyendo. `mezcla` avisa de la cadena que
    cambió de brazo a la mitad —el motor ya no deja hacerla, pero la base
    viene de antes que esa comprobación."""
    brazos = {((r.get("escena") or "").lower() == "true",
               int(r.get("capubana_cada") or 0)) for r in cadena}
    escena = any(e for e, _ in brazos)
    cadencias = sorted({c for e, c in brazos if e and c})
    return {
        "escena": escena,
        "capubana_cada": cadencias[0] if len(cadencias) == 1 else None,
        "mezcla": len(brazos) > 1,
        "brazos": sorted(f"{'con' if e else 'sin'} escena"
                         + (f", Capubana cada {c}" if e and c else "")
                         for e, c in brazos),
    }


def admitir_raices_de_la_cadena(run_ids: list[str]) -> list[str]:
    """Las raíces que la puerta onomatopéyica admitió en esta cadena (db.6).

    El motor las guarda en `neologisms.morphological_rule` como
    `onomatopeya:<raíz>` (tanda final, 2026-09-23), porque la lista viva está
    en el `curiana_lexico.json` del run, que aquí no se lee. Se admiten ANTES
    de clasificar nada: sin esto, `tororo-bana` saldría «de ninguna parte» y el
    análisis dejaría fuera justo los nombres de animales que queremos ver
    cruzar de un nodo a otro."""
    from curiana_lexicon import admitir_raiz_onomatopeyica
    filas = q(f"""
        select distinct substring(morphological_rule from 13) as raiz
        from neologisms
        where run_id in ({_lista_sql(run_ids)})
          and morphological_rule like 'onomatopeya:%'
    """)
    raices = sorted(f["raiz"] for f in filas if f.get("raiz"))
    for r in raices:
        admitir_raiz_onomatopeyica(r)
    return raices


def analizar_cadena(cadena: list[dict], umbral: float = UMBRAL_INCLINACION,
                    min_hablantes: int = MIN_HABLANTES,
                    con_lugar: bool = False) -> dict:
    run_ids = [r["id"] for r in cadena]
    admitir_raices_de_la_cadena(run_ids)
    nodo_de, casa_de, posibles = elenco_por_nodo()
    excluidas = formas_excluidas()
    usos = cargar_usos(run_ids)
    neologismos = cargar_neologismos(run_ids)
    koine = cargar_koine_lexicon(run_ids)
    raices = raices_de_ninguna_parte(usos)
    tpd = max(int(r["turnos_por_dia"] or 6) for r in cadena)
    # La escena se consulta SÓLO si se pidió: son dos consultas más y la
    # mayoría de las cadenas de la base corrieron antes de que existiera.
    lugar = (analizar_lugar(run_ids, usos, neologismos, koine, excluidas, tpd)
             if con_lugar else None)
    return {
        "cadena": [{"run": r["id"][:8], "run_id": r["id"], "dias": int(r["total_days"]),
                    "perfil": r["perfil"], "semilla": r["semilla"],
                    "turnos_por_dia": int(r["turnos_por_dia"] or 6),
                    "serie": r.get("serie") or None,
                    # El BRAZO, leído de la config (no deducido de `presencias`):
                    # un run anterior a la escena no trae la clave y entonces
                    # corrió sin escena, que es un hecho — antes del 2026-09-17
                    # la escena no existía.
                    "escena": (r.get("escena") or "").lower() == "true",
                    "capubana_cada": int(r.get("capubana_cada") or 0),
                    "motor_commit": r["motor_commit"][:8], "started_at": r["started_at"]}
                   for r in cadena],
        "brazo": brazo_de_la_cadena(cadena),
        "elenco": {"total": len(nodo_de), "por_nodo": posibles,
                   "por_casa": dict(Counter(f"{nodo_de[a]}/{casa_de[a]}" for a in nodo_de))},
        "umbrales": {"inclinacion": umbral, "min_hablantes": min_hablantes,
                     "formas_excluidas": len(formas_de_plantilla_solas()),
                     "mas_la_raiz_de_ninguna_parte": True},
        "divergencia_sembrada": divergencia_sembrada(),
        "cobertura": cobertura_del_elenco(usos, nodo_de),
        "habla_por_nodo": habla_por_nodo(usos, nodo_de, posibles),
        "formas": analizar_formas(usos, neologismos, koine, nodo_de, posibles,
                                  excluidas, umbral, min_hablantes, tpd),
        "distancia": analizar_distancia(usos, nodo_de, excluidas),
        # El corte del 2026-09-20: cuántas formas de la cadena tienen la raíz
        # fuera del lexicón, y si el veredicto aguanta al descontarlas.
        "raiz_de_ninguna_parte": {k: v for k, v in raices.items() if k != "set"},
        "veredicto_raiz": veredicto_sin_raiz_ajena(
            usos, nodo_de, formas_de_plantilla_solas(), raices["set"]),
        "acunacion_sin_uso_registrado": acunacion_sin_uso_registrado(run_ids),
        "koine_metrics_del_motor": cargar_metricas_koine(run_ids),
        # Sólo con `--lugar`: sin la bandera la clave no existe y el JSON es el
        # de siempre.
        **({"lugar": lugar} if lugar is not None else {}),
    }


def _fmt(x, n=3) -> str:
    return "—" if x is None else f"{x:.{n}f}"


def _imprimir_raices(res: dict) -> None:
    """Las formas con la raíz fuera del lexicón, y si el veredicto aguanta.

    Los runs no se reescriben: esto es una RELECTURA de `word_uses` con la
    regla del corte del 2026-09-20."""
    r = res.get("raiz_de_ninguna_parte")
    if not r:
        return
    pct = (100.0 * r["usos"] / r["de_usos_totales"]) if r["de_usos_totales"] else 0.0
    print(f"  Raíz de ninguna parte (relectura, la base no se reescribe): "
          f"{r['formas']} de {r['de_formas_totales']} formas · "
          f"{r['usos']} de {r['de_usos_totales']} usos ({pct:.2f}%)")
    if r["raices"]:
        top = list(r["raices"].items())[:6]
        print("    raíces: " + " · ".join(f"{k} ×{n}" for k, n in top))
    v = res.get("veredicto_raiz") or {}
    if v:
        con, sin = v["con_raiz_ajena"], v["sin_raiz_ajena"]
        print("    ¿aguanta la lectura emergente al descontarlas? "
              "(serie RECONSTRUIDA de `word_uses`: no es `distance_emergente`,")
        print("     que el motor calcula sobre sus idiolectos — sólo vale para "
              "comparar con y sin. La cifra del motor,")
        print("     con el mismo veredicto, la mide "
              "`6-fusion/scripts/medir_raices_de_ninguna_parte.py`)")
        for etiqueta, d in (("con raíz ajena", con), ("sin raíz ajena", sin)):
            serie = d["serie"]
            caida = ((serie[-1][1] - serie[0][1]) / serie[0][1] * 100.0
                     if len(serie) >= 2 and serie[0][1] else 0.0)
            print(f"      {etiqueta:<15} "
                  f"{' → '.join(f'{x}' for _, x in serie)}  "
                  f"({caida:+.1f} %, {d['codigo']})")
        print("      → la lectura NO cambia de signo al descontarlas"
              if v["se_sostiene"] else
              "      → ⚠ LA LECTURA CAMBIA DE SIGNO al descontarlas")


def imprimir_lugar(res: dict, top: int) -> None:
    """La sección de la escena. Si no hay escena, dice por qué y vuelve."""
    lug = res.get("lugar")
    if lug is None:
        return
    sub("La escena — dónde estuvo cada quien (tabla `presencias`)")
    if not lug["disponible"]:
        print(f"  ⚠ Sin escena: {lug['motivo']}.")
        print("    Los runs anteriores al 2026-09-17 corrieron sin capa 1: el "
              "lugar de un agente era su `ubicacion_default`, que no cambia "
              "nunca. Lo de arriba (formas, distancia) no depende de esto.")
        return

    esc = lug["escenas"]
    print(f"  {lug['presencias']} presencias · {lug['agentes_en_escena']} agentes · "
          f"días {', '.join(str(d) for d in lug['dias'])} · "
          f"{esc['presencias_por_turno']} presencias por turno de media")
    print("  Por run: " + " · ".join(f"{r} {n}" for r, n in lug["por_run"].items()))

    momentos = lug["momentos"]
    sub(f"Ocupación por lugar y momento (media por día) — las {top} más pobladas")
    cab = f"  {'lugar':<26}" + "".join(f"{m[:9]:>10}" for m in momentos) + f"{'nodos':>16}"
    print(cab)
    print("  " + "─" * (len(cab) - 2))
    for f in lug["ocupacion"][:top]:
        celdas = ""
        for m in momentos:
            c = f["por_momento"].get(m)
            celdas += f"{c['media_por_dia']:>10.1f}" if c else f"{'·':>10}"
        print(f"  {f['lugar']:<26}{celdas}{'+'.join(n[:3] for n in f['nodos']) or '—':>16}")

    comp = lug["compartidos"]
    sub("Lugares que tocan los dos nodos")
    print(f"  {comp['n_lugares']} lugares con nodo · compartidos: "
          f"{', '.join(comp['compartidos']) or 'ninguno'}")
    print(f"  Compartidos EN EL MISMO TURNO (contacto de verdad): "
          f"{', '.join(comp['compartidos_simultaneos']) or 'ninguno'} · "
          f"{comp['turnos_con_dos_nodos']} turno(s) con los dos nodos en un lugar")
    if not comp["compartidos_simultaneos"]:
        print("  ⚠ Ningún lugar junta a los dos nodos en el mismo turno. Es el "
              "resultado que la escena derivada anticipaba (§3.4: cero lugares "
              "compartidos emergentes): el mundo no produce contacto solo, hay "
              "que declararlo o hacerlo viajar.")

    sub("Escenas y voces (una escena = día × turno × lugar con alguien dentro)")
    print(f"  {esc['escenas']} escenas · {esc['escenas_con_voz']} con alguna voz · "
          f"{esc['escenas_con_dos_o_mas_voces']} con dos o más "
          f"(máximo {esc['voces_max_en_una_escena']} voces en una)")
    print(f"  Intervenciones ubicadas: {esc['intervenciones_ubicadas']} de "
          f"{esc['respuestas_totales']} · con compañía en su lugar: "
          f"{esc['intervenciones_con_compania']} ({esc['pct_con_compania']}%)")
    if esc["hablantes_sin_presencia"]:
        print(f"  ⚠ {esc['hablantes_sin_presencia']} respuesta(s) de agentes sin "
              f"fila en `presencias` ese turno: habló alguien que no estaba en "
              f"la escena. Es el guardián barato del §5b, en texto.")
    print(f"  `agent_responses.lugar` escrito en {esc['respuestas_con_lugar_declarado']} "
          f"de {esc['respuestas_totales']} respuestas · discrepan de `presencias`: "
          f"{esc['lugar_declarado_discrepa']}")

    rc = lug["resumen_cruce"]
    sub(f"Cruce de formas POR LUGAR — las {top} más usadas")
    cab = (f"  {'forma':<22}{'usos':>6}{'lugares':>8}  {'nació en':<22}"
           f"{'salió':>7}{'Δturnos':>9}  {'compartido':<20}")
    print(cab)
    print("  " + "─" * (len(cab) - 2))
    for f in lug["cruce"][:top]:
        if not f["ubicable"]:
            print(f"  {f['forma']:<22}{'—':>6}{'—':>8}  {'(sin ubicar)':<22}")
            continue
        natal = "+".join(f["lugares_natales"])
        salida = (f"d{f['dia_salida']}t{f['turno_salida']}"
                  if f["turnos_hasta_salir"] is not None else
                  ("n/a" if f["nacimiento_multilugar"] else "no"))
        dt = ("—" if f["turnos_hasta_salir"] is None
              else str(f["turnos_hasta_salir"]))
        print(f"  {f['forma']:<22}{f['usos_ubicados']:>6}{f['n_lugares']:>8}  "
              f"{natal[:22]:<22}{salida:>7}{dt:>9}  "
              f"{','.join(f['lugares_compartidos_tocados'])[:20]:<20}")
    print("\n  (Δturnos = turnos desde el primer uso hasta el primero fuera del "
          "lugar donde nació · n/a = sonó en dos lugares a la vez, así que no "
          "hay lugar del que salir)")
    print(f"  De {rc['formas']} formas emergentes, {rc['ubicables']} se pueden "
          f"ubicar y {rc['sin_ubicar']} no (su hablante no tiene presencia ese turno).")
    print(f"  {rc['salieron_de_su_lugar']} salieron de su lugar, "
          f"{rc['murieron_en_su_lugar']} murieron en él, "
          f"{rc['nacieron_en_varios_lugares']} nacieron en varios a la vez.")
    if rc["turnos_hasta_salir_mediana"] is not None:
        print(f"  Turnos hasta salir del lugar: mediana "
              f"{rc['turnos_hasta_salir_mediana']}, mínimo {rc['turnos_hasta_salir_min']}, "
              f"máximo {rc['turnos_hasta_salir_max']} · mismo turno: {rc['mismo_turno']}")
    print(f"  Pasaron por un lugar compartido: {rc['pasaron_por_compartido']} · "
          f"mediana de lugares distintos por forma: {rc['lugares_distintos_mediana']}")


def imprimir(res: dict, top: int, con_formas: bool, con_distancia: bool) -> None:
    c = res["cadena"]
    titulo(f"NODOS — cadena {' → '.join(r['run'] for r in c)}")
    # El BRAZO primero: sin saber si la cadena corrió con escena, ninguna cifra
    # de abajo significa lo mismo (la brecha intra/entre se lee CONTRA el otro
    # brazo, no contra un umbral).
    brazo = res.get("brazo") or {}
    series = sorted({r.get("serie") for r in c if r.get("serie")})
    etiqueta = ("con escena" + (f", Capubana cada {brazo['capubana_cada']}"
                                if brazo.get("capubana_cada") else "")
                if brazo.get("escena") else "sin escena (brazo de control)")
    print(f"  Brazo: {etiqueta}"
          + (f" · serie {', '.join(series)}" if series else ""))
    if brazo.get("mezcla"):
        print(f"  ⚠ ESTA CADENA MEZCLA BRAZOS ({' | '.join(brazo['brazos'])}): "
              f"una escena no puede entrar ni salir a mitad de cadena "
              f"(diseño §5.4). Lo de abajo promedia días que no son "
              f"comparables entre sí.")
    print(f"  Elenco: {res['elenco']['total']} agentes — " +
          ", ".join(f"{n} {k}" for n, k in res["elenco"]["por_nodo"].items()))
    print(f"  Umbral de inclinación: razón de tasas ≥ {res['umbrales']['inclinacion']}"
          f" · mínimo {res['umbrales']['min_hablantes']} hablantes para clasificar")
    print(f"  Formas excluidas del recuento emergente: {res['umbrales']['formas_excluidas']}"
          f" (vocabulario base + lo que enseñan las plantillas)"
          f" + toda forma con la raíz fuera del lexicón")
    _imprimir_raices(res)
    ds = res["divergencia_sembrada"]
    print(f"  Divergencia sembrada: {ds['vectores_semilla_distintos']} vector(es)-"
          f"semilla distinto(s) entre {ds['agentes']} agentes · "
          f"{ds['agentes_con_el_vector_mas_comun']} comparten el mismo · "
          f"nodos con semilla propia: {', '.join(ds['nodos_con_semilla_propia']) or 'ninguno'}")
    if ds["vectores_semilla_distintos"] <= 2 or not ds["nodos_con_semilla_propia"]:
        print(f"  ⚠ NO HAY DIVERGENCIA SEMBRADA POR NODO. `FORMAS_SEED` y "
              f"`EMOCIONAR_SEED` (curiana_koine) están indexados por los nombres "
              f"de la era 1 y sólo "
              f"{len(ds['con_formas_seed_propia'])} agente(s) del elenco actual "
              f"los reciben ({', '.join(ds['con_formas_seed_propia']) or '—'}): la "
              f"campaña de antropónimos renombró al resto y nadie resuelve "
              f"ALIAS_ERA1 al sembrar. DISENO_KOINE §4: «sin esta pre-carga, "
              f"todos arrancan iguales y convergencia no significa nada».")
    cob = res["cobertura"]
    print(f"  Cobertura: {cob['agentes_con_nodo']} de {cob['agentes_en_la_base']} "
          f"agentes de la base tienen nodo · {cob['pct_usos_con_nodo']}% de los usos")
    if cob["pct_usos_con_nodo"] < 90:
        print(f"  ⚠ ESTA CADENA NO SE PUEDE LEER POR NODO: {cob['n_agentes_sin_nodo']} "
              f"agentes no están en curiana_agents_era2 "
              f"({', '.join(cob['agentes_sin_nodo'][:6])}…). El run declara "
              f"`elenco: era2` pero habla con otros nombres — pasó con aafc5c32, "
              f"anterior a la campaña de antropónimos. Todo lo de abajo mide "
              f"sólo la fracción reconocida.")

    sub("Cuánto habló cada nodo (la reserva: GUARANAO es 39 de 63 = 61,9% del censo)")
    print(f"  {'día':<5}{'nodo':<11}{'usos':>7}{'cuota':>9}{'censo':>9}"
          f"{'activos':>9}{'formas':>8}")
    for f in res["habla_por_nodo"]:
        for n, d in f["nodos"].items():
            print(f"  {f['dia']:<5}{n:<11}{d['usos']:>7}{d['cuota_de_usos']*100:>8.1f}%"
                  f"{d['cuota_del_censo']*100:>8.1f}%{d['agentes_activos']:>9}"
                  f"{d['formas_distintas']:>8}")

    if con_formas:
        sub(f"Formas emergentes — las {top} más usadas (tasa = hablantes / hablantes posibles del nodo)")
        nodos = list(res["elenco"]["por_nodo"])
        cab = (f"  {'':2}{'forma':<22}{'usos':>6}" +
               "".join(f"{n[:3]+' habl':>10}{n[:3]+' tasa':>10}" for n in nodos) +
               f"{'razón':>8}  {'clase':<18}{'acuñó':<12}{'cruce':>7}{'Δturnos':>9}")
        print(cab)
        print("  " + "─" * (len(cab) - 2))
        for r in res["formas"][:top]:
            celdas = ""
            for n in nodos:
                pn = r["por_nodo"][n]
                celdas += f"{pn['hablantes']:>10}{pn['tasa']:>10.3f}"
            razon = "∞" if r["razon_infinita"] else _fmt(r["razon_de_tasas"], 2)
            clase = r["clase"] + (f"→{r['nodo_de_la_clase'][:3]}"
                                  if r["nodo_de_la_clase"] else "")
            nodos_acu = ("+".join(n[:3] for n in r["nodos_acunadores"])
                         or "?")
            # «~» = no hay registro en `neologisms`: el acuñador es una
            # aproximación por primer uso, y en el turno 1 del día 1 hablan doce
            # agentes a la vez, así que ahí no dice casi nada.
            aprox = "~" if r["origen_acunacion"] == "primer-uso" else ""
            acu = (f"{aprox}{nodos_acu} d{r['dia_acunacion'] or '?'}"
                   f"t{r['turno_acunacion'] or '?'}")
            cruce = (f"d{r['dia_cruce']}t{r['turno_cruce']}" if r["cruzo"]
                     else ("n/a" if r["cruce_no_aplica"] else "no"))
            dturnos = ("—" if r["turnos_hasta_cruzar"] is None
                       else str(r["turnos_hasta_cruzar"]))
            marca = "*" if r["fijada_en_koine"] else (
                "n" if r["es_neologismo"] else " ")
            print(f"  {marca:<2}{r['forma']:<22}{r['usos_totales']:>6}{celdas}"
                  f"{razon:>8}  {clase:<18}{acu:<12}{cruce:>7}{dturnos:>9}")
        print("\n  (* fijada en koine_lexicon · n registrada como neologismo · "
              "acuñó/cruce en díaNturnoN · ~ = acuñador aproximado por primer "
              "uso, sin registro en neologisms · Δturnos = turnos hasta el primer "
              "uso fuera del nodo que acuñó · n/a = la acuñaron los DOS nodos a "
              "la vez, así que no hay frontera que cruzar)")

        clases = Counter(r["clase"] for r in res["formas"])
        print("\n  Reparto de clases: " +
              " · ".join(f"{k} {v}" for k, v in clases.most_common()))
        clasificables = [r for r in res["formas"]
                         if r["clase"] not in ("poco-atestiguada", "sin-usos")]
        multinodo = [r for r in clasificables if r["acunacion_multinodo"]]
        cruzaron = [r for r in clasificables if r["cruzo"]]
        nunca = [r for r in clasificables
                 if not r["cruzo"] and not r["acunacion_multinodo"]]
        print(f"  De {len(clasificables)} formas clasificables: {len(cruzaron)} "
              f"cruzaron de nodo, {len(nunca)} no cruzaron, {len(multinodo)} "
              f"nacieron en los dos nodos a la vez (evento de nombramiento simultáneo)")
        con_registro = [r for r in clasificables
                        if r["origen_acunacion"] == "neologisms"]
        print(f"  Con acuñador registrado en `neologisms`: {len(con_registro)}; "
              f"el resto lleva acuñador aproximado por primer uso (marcado ~)")
        a = res["acunacion_sin_uso_registrado"]
        if a["acunaciones_con_turno"]:
            print(f"  ⚠ Acuñaciones cuya forma NO queda en word_uses en la misma "
                  f"respuesta: {a['sin_uso_registrado']} de "
                  f"{a['acunaciones_con_turno']} ({a['pct']}%). Al acuñar, la forma "
                  f"aún no está en el léxico comunitario y `words_used` no la "
                  f"recoge: el primer uso registrado es el del que la ADOPTÓ, que "
                  f"puede ser del otro nodo. Descontar esto antes de leer rutas.")
        # El mismo corte pero sólo sobre las que SÍ tienen acuñador registrado:
        # es la lectura fiable de la ruta, y es mucho más pequeña.
        if con_registro:
            print("  Sólo con acuñador registrado → " +
                  f"{sum(1 for r in con_registro if r['cruzo'])} cruzaron, " +
                  f"{sum(1 for r in con_registro if not r['cruzo'] and not r['acunacion_multinodo'])} no, " +
                  f"{sum(1 for r in con_registro if r['acunacion_multinodo'])} multinodo")
        dts = sorted(r["turnos_hasta_cruzar"] for r in cruzaron
                     if r["turnos_hasta_cruzar"] is not None)
        if dts:
            mediana = dts[len(dts) // 2]
            print(f"  Turnos hasta cruzar (las que cruzaron): mediana {mediana}, "
                  f"mínimo {dts[0]}, máximo {dts[-1]} · mismo turno: "
                  f"{sum(1 for d in dts if d == 0)}")

    if con_distancia:
        sub("Distancia idiolectal (1 − coseno) — vectores reconstruidos de word_uses por día")
        print(f"  {'día':<5}{'lectura':<22}{'n':>4}{'intra GUA':>11}{'intra AMU':>11}"
              f"{'intra':>9}{'entre':>9}{'brecha':>9}")
        for f in res["distancia"]:
            for lect in LECTURAS:
                d = f[lect]
                print(f"  {f['dia']:<5}{lect:<22}{d['n_agentes']:>4}"
                      f"{_fmt(d['intra'].get('GUARANAO'), 4):>11}"
                      f"{_fmt(d['intra'].get('AMUAY'), 4):>11}"
                      f"{_fmt(d['intra_global'], 4):>9}{_fmt(d['entre'], 4):>9}"
                      f"{_fmt(d['brecha'], 4):>9}")
        for lect in LECTURAS:
            t = tendencia(res["distancia"], lect)
            if t["veredicto"] == "insuficiente":
                print(f"\n  {lect}: datos insuficientes ({t['puntos']} días comparables)")
                continue
            print(f"\n  {lect}: día {t['dia_inicial']} → {t['dia_final']} · "
                  f"intra {t['intra'][0]:.4f}→{t['intra'][1]:.4f} "
                  f"({t['delta_rel_intra']*100:+.1f}%) · "
                  f"entre {t['entre'][0]:.4f}→{t['entre'][1]:.4f} "
                  f"({t['delta_rel_entre']*100:+.1f}%) · "
                  f"brecha {t['brecha'][0]:+.4f}→{t['brecha'][1]:+.4f}")
            print(f"     veredicto: {t['veredicto']} (margen {t['margen']*100:.0f}%)")

        if res["koine_metrics_del_motor"]:
            print("\n  Contraste con lo que el motor guardó en koine_metrics "
                  "(ventana de 10 turnos de habla, no del día; sin partir por nodo):")
            for m in res["koine_metrics_del_motor"]:
                print(f"    día {m['dia']}: acumulada {m['distance']} · "
                      f"ventana {m['distance_ventana']} · emergente {m['distance_emergente']} "
                      f"· n {m['n_agents']}")


# ══════════════════════════════════════════════════════════════════════
# IX. CLI
# ══════════════════════════════════════════════════════════════════════

def main() -> int:
    _forzar_utf8()
    p = argparse.ArgumentParser(
        description="Análisis por nodo (GUARANAO / AMUAY) de la era 2.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""\
            Ejemplos:
              python analizar_nodos.py --run 0193873d
              python analizar_nodos.py --todo --formas
              python analizar_nodos.py --run 0193873d --lugar
              python analizar_nodos.py --run 0193873d --json > nodos.json
        """))
    p.add_argument("--run", metavar="ID8",
                   help="run del que sube la cadena por continuado_desde")
    p.add_argument("--todo", action="store_true",
                   help="todas las cadenas de la era 2")
    p.add_argument("--formas", action="store_true", help="sólo la tabla de formas")
    p.add_argument("--distancia", action="store_true", help="sólo la distancia intra/entre")
    p.add_argument("--lugar", action="store_true",
                   help="la escena: ocupación por lugar y momento, escenas con "
                        "más de un hablante y cruce de formas por lugar "
                        "compartido (tabla `presencias`)")
    p.add_argument("--top", type=int, default=25, help="formas a imprimir (def. 25)")
    p.add_argument("--umbral", type=float, default=UMBRAL_INCLINACION,
                   help=f"razón de tasas para llamar «inclinada» (def. {UMBRAL_INCLINACION})")
    p.add_argument("--min-hablantes", type=int, default=MIN_HABLANTES,
                   help=f"hablantes mínimos para clasificar (def. {MIN_HABLANTES})")
    p.add_argument("--json", action="store_true", help="volcado JSON a stdout")
    args = p.parse_args()

    if not args.run and not args.todo:
        p.error("hace falta --run <id8> o --todo")

    cadenas = [cadena_de_runs(resolver_run(args.run))] if args.run else cadenas_era2()
    if not cadenas:
        print("No hay cadenas de la era 2 en la base.")
        return 1

    resultados = [analizar_cadena(c, args.umbral, args.min_hablantes, args.lugar)
                  for c in cadenas]

    if args.json:
        print(json.dumps(resultados if len(resultados) > 1 else resultados[0],
                         ensure_ascii=False, indent=2))
        return 0

    # Sin banderas de sección: formas y distancia, como siempre. `--lugar` es
    # una sección más y sólo sale si se pide: la escena no existe en los runs
    # anteriores al 2026-09-17 y el informe de siempre no tiene por qué cambiar.
    pedidas = (args.formas, args.distancia, args.lugar)
    con_formas = args.formas or not any(pedidas)
    con_dist = args.distancia or not any(pedidas)
    for r in resultados:
        imprimir(r, args.top, con_formas, con_dist)
        if args.lugar:
            imprimir_lugar(r, args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
