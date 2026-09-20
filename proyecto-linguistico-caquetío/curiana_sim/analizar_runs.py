#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — análisis de los runs almacenados
==========================================

Lee la base local (Supabase/Postgres en Docker) y responde las tres preguntas
que el proyecto se hace sobre sus propios datos:

    --koine     ¿Hubo koineización? El contraste normal vs. ablación, con
                estadística y no solo con medias; + la vista por CADENA (los
                días encadenados con `--continuar`: un run de la era 2 es un
                día y su serie sola nunca tiene dos puntos).
    --lengua    ¿Qué le pasó a la lengua? Composición, deriva, neologismos,
                distribución del léxico.
    --agentes   ¿Cómo se comportaron? Prestigio, adopción, diferencias por
                tier y etnia.
    --narrativa ¿Qué historias salieron? Citas, arcos, eventos.
    --prestamos ¿Qué voces de la esfera de contacto se usaron, y bajaron del
                tier 1 al 2 y al 3? Lee `loanword_uses` (migración 20260916).
    --raices    ¿Cuánto de lo que la base guardó como «caquetío» tiene la RAÍZ
                fuera del lexicón? Re-clasifica `word_uses` AL LEER con la
                regla del corte del 2026-09-20 (`lumina-bana-iro`); la base no
                se reescribe.

POR QUÉ ESTE MÓDULO EXISTE
--------------------------
El análisis se venía haciendo con consultas sueltas cuyo resultado acababa en
un markdown y no se podía reproducir. Aquí las consultas **son el código**: si
alguien duda de una cifra del informe, corre el comando y la vuelve a medir.
Es la misma disciplina de `generar_tablero.py`.

CONEXIÓN
--------
No usa psycopg2 (no está instalado): habla con Postgres por `docker exec` y lee
CSV. Es más lento y da igual — son consultas de análisis, no de un bucle.
El contenedor por defecto es el de este proyecto; ojo que en la misma máquina
corre otro Supabase (fintech), por eso el nombre va explícito y no por puerto.

Uso:
    python analizar_runs.py --koine
    python analizar_runs.py --lengua --neologismos
    python analizar_runs.py --todo
"""

import argparse
import io
import subprocess
import sys
from textwrap import dedent

import numpy as np
import pandas as pd

from curiana_cadena import (
    LectorSQL,
    cadenas_en_la_base,
    corto,
    es_interrumpido,
    id_de,
    lineas_de_serie,
    resumen_de_cadena,
    serie_koine_de_cadena,
    texto_veredicto,
)

CONTENEDOR = "supabase_db_curiana_sim"

# Los dos brazos del experimento de koiné del 2026-07-06. Van fijos porque el
# contraste solo tiene sentido entre estos dos: mismo día, misma configuración,
# misma semilla de elenco, y la única diferencia es `--ablacion`.
RUN_NORMAL = "038d7b9d-3335-4b96-971d-8a3132c0319d"
RUN_ABLACION = "bdc54134-9bb5-4308-a71b-135e99900f67"


def q(sql: str) -> pd.DataFrame:
    """Corre SQL en el Postgres del contenedor y devuelve un DataFrame."""
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "--csv", "-c", dedent(sql)],
        capture_output=True, text=True, encoding="utf-8", timeout=180)
    if out.returncode != 0:
        raise RuntimeError(f"psql falló:\n{out.stderr.strip()[:500]}")
    return pd.read_csv(io.StringIO(out.stdout))


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def titulo(t: str) -> None:
    print(f"\n{'═' * 72}\n  {t}\n{'═' * 72}")


def sub(t: str) -> None:
    print(f"\n── {t} ──")


# ══════════════════════════════════════════════════════════════════════
# KOINÉ — el contraste normal vs. ablación
# ══════════════════════════════════════════════════════════════════════

def analizar_koine() -> dict:
    titulo("KOINÉ — ¿convergieron, y fue por el motor?")

    df = q(f"""
        SELECT r.config->>'ablacion' AS brazo, k.day,
               k.distance AS acumulada,
               k.distance_ventana AS ventana,
               k.distance_emergente AS emergente
        FROM koine_metrics k JOIN simulation_runs r ON r.id = k.run_id
        WHERE k.run_id IN ('{RUN_NORMAL}', '{RUN_ABLACION}')
        ORDER BY brazo, k.day
    """)
    # Ojo: `config->>'ablacion'` sale como texto 'true'/'false' de psql, y pandas
    # lo lee como **bool** al parsear el CSV. Mapear por la cadena devuelve NaN
    # para todo y deja el pareo vacío sin decir por qué. Se normaliza a texto.
    df["brazo"] = df["brazo"].astype(str).str.lower().map(
        {"false": "normal", "true": "ablacion"})
    if df["brazo"].isna().any():
        raise RuntimeError("no se pudo identificar el brazo de cada run")

    n = df[df.brazo == "normal"].set_index("day")
    a = df[df.brazo == "ablacion"].set_index("day")
    dias = sorted(set(n.index) & set(a.index))
    print(f"\n  días pareados: {len(dias)}")

    from scipy import stats

    resultados = {}
    for lectura in ("acumulada", "ventana", "emergente"):
        vn = n.loc[dias, lectura].astype(float).values
        va = a.loc[dias, lectura].astype(float).values
        dif = va - vn                      # positivo = la ablación converge MENOS

        # Pareado por día: los dos brazos comparten el calendario de eventos.
        t, p_t = stats.ttest_rel(vn, va)
        try:
            _, p_w = stats.wilcoxon(vn, va)
        except ValueError:
            p_w = float("nan")
        d = dif.mean() / dif.std(ddof=1) if dif.std(ddof=1) else float("nan")

        # ¿Se separan con el tiempo? Pendiente de la diferencia contra el día.
        pend, inter, r, p_pend, se = stats.linregress(dias, dif)

        resultados[lectura] = dict(
            normal=vn.mean(), ablacion=va.mean(), delta=dif.mean(),
            p_t=p_t, p_w=p_w, d=d, pend=pend, p_pend=p_pend,
            gana_normal=int((dif > 0).sum()), n=len(dias))

        sub(f"lectura «{lectura}»")
        print(f"    normal   {vn.mean():.4f}      ablación {va.mean():.4f}")
        print(f"    Δ (abl−nor) = {dif.mean():+.4f}   "
              f"(mayor = la ablación converge menos, que es lo esperado)")
        print(f"    t pareada  p = {p_t:.2e}    Wilcoxon p = {p_w:.2e}")
        print(f"    d de Cohen (pareada) = {d:.2f}")
        print(f"    días en que el normal converge más: "
              f"{int((dif > 0).sum())}/{len(dias)}")
        if p_pend >= 0.05:
            lectura_tend = "— plana: el efecto no crece ni se apaga"
        elif pend > 0:
            lectura_tend = "— la brecha SE ABRE con el tiempo"
        else:
            lectura_tend = "— la brecha SE CIERRA con el tiempo"
        print(f"    tendencia de la brecha: {pend:+.5f}/día (p={p_pend:.3f}) "
              f"{lectura_tend}")

    sub("veredicto")
    em = resultados["emergente"]
    print("    La lectura emergente es la más exigente y la que más separa los")
    print(f"    brazos: Δ = {em['delta']:+.4f}, p = {em['p_t']:.1e}, d = {em['d']:.2f}.")
    print(f"    El normal converge más que la ablación en {em['gana_normal']} de")
    print(f"    {em['n']} días. La diferencia NO es de medias apenas distintas:")
    print("    es sistemática día a día.")

    sub("⚠️ lo que estos p-valores NO dicen")
    print(dedent("""\
        1. **n = 1 run por brazo.** Los 30 días son pseudo-réplicas: los días de
           un mismo run comparten agentes, semilla y trayectoria, así que NO son
           independientes. Los p-valores de arriba miden «¿difieren estas dos
           series?», no «¿difieren estas dos condiciones?». Para lo segundo hace
           falta repetir el par de runs varias veces y tratar el RUN como unidad.
           Con lo que hay, el resultado es una señal fuerte, no una prueba.

        2. **La brecha no crece.** En las tres lecturas la tendencia es plana o
           ligeramente decreciente. O sea: el motor de convergencia produce un
           desplazamiento **inmediato y sostenido**, no un efecto acumulativo.
           Si la hipótesis era «la koiné se va formando», el dato dice más bien
           «el contagio fija una diferencia desde el principio y la mantiene».

        3. **30 días simulados es poco** para hablar de koineización histórica;
           es una prueba del mecanismo, no del fenómeno."""))
    return resultados


# ══════════════════════════════════════════════════════════════════════
# CADENAS — los días encadenados con `--continuar`
# ══════════════════════════════════════════════════════════════════════

def analizar_cadenas() -> list[list[dict]]:
    """La serie de koiné y el veredicto de cada CADENA de runs.

    En la era 2 un run es un día: su serie tiene un punto y el veredicto del
    motor dice siempre «datos insuficientes». La evidencia vive en la cadena
    `continuado_desde`, que hasta el 2026-09-16 había que juntar a mano (ver
    5-experimento/BITACORA_RUNS.md). El criterio del veredicto es el MISMO del
    orquestador: `curiana_cadena.veredicto`."""
    titulo("CADENAS — los días encadenados con --continuar")

    lector = LectorSQL(CONTENEDOR)
    cadenas = cadenas_en_la_base(lector)
    if not cadenas:
        print("\n    (ninguna cadena: ningún run continúa de otro)")
        return []

    for cadena in cadenas:
        hoja = id_de(cadena[-1])
        avisos: list[str] = []
        serie = serie_koine_de_cadena(lector, hoja, avisos=avisos, cadena=cadena)
        sub(f"cadena {resumen_de_cadena(cadena)} · {len(cadena)} runs")
        for aviso in avisos:
            print(f"    ⚠ {aviso}")
        if not serie:
            print("    (sin días medidos)")
            continue
        print(f"    días: {len(serie)}")
        for linea in lineas_de_serie(serie):
            print(f"    {linea}")
        print(f"    {texto_veredicto(serie)}")
    print("\n    Un run interrumpido (sin ended_at o 0 turnos) sigue EN la cadena")
    print("    —hay que poder subir a través de él— pero sus métricas no entran:")
    print("    la unidad de la serie es el día cerrado.")
    return cadenas


# ══════════════════════════════════════════════════════════════════════
# LENGUA
# ══════════════════════════════════════════════════════════════════════

def analizar_lengua() -> None:
    titulo("LENGUA — composición, deriva y léxico")

    sub("composición por brazo (media de las respuestas)")
    comp = q(f"""
        SELECT r.config->>'ablacion' AS brazo,
               round(avg(a.pct_caquetio)::numeric, 4) AS caquetio,
               round(avg(a.pct_wayunaiki)::numeric, 4) AS wayunaiki,
               round(avg(a.pct_lokono)::numeric, 4) AS lokono,
               round(avg(a.pct_taino)::numeric, 4) AS taino,
               round(avg(a.score)::numeric, 3) AS score,
               round(stddev(a.pct_caquetio)::numeric, 4) AS sd_caquetio,
               round(stddev(a.score)::numeric, 4) AS sd_score,
               count(*) AS n
        FROM agent_responses a JOIN simulation_runs r ON r.id = a.run_id
        WHERE a.run_id IN ('{RUN_NORMAL}', '{RUN_ABLACION}')
        GROUP BY brazo ORDER BY brazo
    """)
    print(comp.to_string(index=False))

    print("\n  ⚠️ Mirar `sd_caquetio` y `sd_score`: si son casi cero, las métricas")
    print("     están saturadas y no distinguen nada (es el issue #69).")

    sub("¿está saturada pct_caquetio? distribución en los dos runs de 60 turnos")
    dist = q(f"""
        SELECT width_bucket(pct_caquetio, 0, 1, 10) AS decil,
               count(*) AS n
        FROM agent_responses
        WHERE run_id IN ('{RUN_NORMAL}', '{RUN_ABLACION}')
        GROUP BY decil ORDER BY decil
    """)
    total = dist["n"].sum()
    for _, r in dist.iterrows():
        pct = 100.0 * r["n"] / total
        barra = "█" * int(pct / 2)
        lo = (r["decil"] - 1) * 10
        print(f"    {lo:3d}-{lo+10:3d}%  {r['n']:5d}  {pct:5.1f}%  {barra}")

    sub("las 25 palabras más usadas, y de qué lengua son")
    top = q("""
        SELECT word, source_language, count(*) AS usos,
               count(DISTINCT agent_name) AS agentes,
               count(DISTINCT run_id) AS runs
        FROM word_uses GROUP BY word, source_language
        ORDER BY usos DESC LIMIT 25
    """)
    print(top.to_string(index=False))

    sub("reparto de usos por lengua (todos los runs)")
    lang = q("""
        SELECT source_language, count(*) AS usos,
               count(DISTINCT word) AS formas
        FROM word_uses GROUP BY source_language ORDER BY usos DESC
    """)
    lang["pct"] = (100.0 * lang["usos"] / lang["usos"].sum()).round(1)
    print(lang.to_string(index=False))

    sub("¿ley de Zipf? concentración del léxico")
    z = q("""
        SELECT word, count(*) AS usos FROM word_uses
        GROUP BY word ORDER BY usos DESC
    """)
    usos = z["usos"].values
    acum = np.cumsum(usos) / usos.sum()
    for k in (10, 25, 50, 100):
        if len(acum) >= k:
            print(f"    las {k:3d} palabras más usadas concentran "
                  f"{100 * acum[k - 1]:5.1f}% de los usos")
    print(f"    formas distintas: {len(z)}   usos totales: {usos.sum()}")


def analizar_neologismos() -> None:
    titulo("NEOLOGISMOS — qué inventaron y qué cuajó")

    sub("por estado")
    est = q("""
        SELECT status, count(*) AS n,
               round(avg(coalesce(array_length(adopted_by,1),0))::numeric,2) AS adoptantes_medios
        FROM neologisms GROUP BY status ORDER BY n DESC
    """)
    print(est.to_string(index=False))

    sub("regla morfológica usada")
    reglas = q("""
        SELECT coalesce(nullif(trim(morphological_rule),''),'(sin regla)') AS regla,
               count(*) AS n
        FROM neologisms GROUP BY regla ORDER BY n DESC LIMIT 15
    """)
    print(reglas.to_string(index=False))

    sub("quién propone (top 15) y con qué éxito")
    quien = q("""
        SELECT proposed_by AS agente, count(*) AS propuestos,
               sum(coalesce(array_length(adopted_by,1),0)) AS adopciones,
               round(avg(coalesce(array_length(adopted_by,1),0))::numeric,2) AS media
        FROM neologisms GROUP BY proposed_by
        ORDER BY propuestos DESC LIMIT 15
    """)
    print(quien.to_string(index=False))

    sub("los que más se adoptaron")
    top = q("""
        SELECT form, meaning, proposed_by,
               coalesce(array_length(adopted_by,1),0) AS adoptantes, status
        FROM neologisms
        WHERE coalesce(array_length(adopted_by,1),0) > 0
        ORDER BY adoptantes DESC LIMIT 20
    """)
    print(top.to_string(index=False) if len(top) else "    (ninguno con adoptantes)")

    sub("koiné: formas que se FIJARON")
    fij = q("""
        SELECT concepto_id, form, fijada_dia, soporte, n_variantes
        FROM koine_lexicon ORDER BY fijada_dia
    """)
    print(fij.to_string(index=False) if len(fij) else "    (ninguna)")


# ══════════════════════════════════════════════════════════════════════
# AGENTES
# ══════════════════════════════════════════════════════════════════════

def analizar_agentes() -> None:
    titulo("AGENTES — prestigio, tier y comportamiento")

    sub("por tier (todos los runs)")
    tier = q("""
        SELECT tier, count(DISTINCT agent_name) AS agentes, count(*) AS respuestas,
               round(avg(score)::numeric,3) AS score,
               round(avg(pct_caquetio)::numeric,4) AS caquetio,
               round(avg(neologisms_proposed)::numeric,3) AS neo_por_resp
        FROM agent_responses WHERE tier IS NOT NULL
        GROUP BY tier ORDER BY tier
    """)
    print(tier.to_string(index=False))

    sub("por etnia")
    etnia = q("""
        SELECT ethnicity AS etnia, count(DISTINCT agent_name) AS agentes,
               count(*) AS respuestas,
               round(avg(score)::numeric,3) AS score,
               round(avg(pct_caquetio)::numeric,4) AS caquetio
        FROM agent_responses WHERE ethnicity IS NOT NULL
        GROUP BY ethnicity ORDER BY respuestas DESC
    """)
    print(etnia.to_string(index=False))
    print("\n  ⚠️ Si aparecen 'caquetío' y 'caquetía' como filas distintas, es el")
    print("     bug del campo `etnia` que detecta curiana_polities.py.")

    sub("los 20 agentes más activos")
    act = q("""
        SELECT agent_name AS agente, tier, count(*) AS resp,
               round(avg(score)::numeric,3) AS score,
               round(avg(pct_caquetio)::numeric,4) AS caquetio,
               sum(neologisms_proposed) AS neo
        FROM agent_responses GROUP BY agent_name, tier
        ORDER BY resp DESC LIMIT 20
    """)
    print(act.to_string(index=False))

    sub("perfiles curados: rol en la comunidad")
    perf = q("""
        SELECT rol_comunidad, count(*) AS n
        FROM agent_profiles WHERE rol_comunidad IS NOT NULL
        GROUP BY rol_comunidad ORDER BY n DESC LIMIT 20
    """)
    print(perf.to_string(index=False) if len(perf) else "    (sin perfiles)")


# ══════════════════════════════════════════════════════════════════════
# NARRATIVA
# ══════════════════════════════════════════════════════════════════════

def analizar_narrativa() -> None:
    titulo("NARRATIVA — citas, arcos y eventos")

    sub("las 15 citas de mayor impacto")
    citas = q("""
        SELECT agent_name AS agente, day AS dia, round(impacto_score::numeric,2) AS impacto,
               left(quote, 90) AS cita
        FROM agent_quotes ORDER BY impacto_score DESC NULLS LAST LIMIT 15
    """)
    for _, r in citas.iterrows():
        print(f"\n    [{r['impacto']}] {r['agente']} (día {r['dia']})")
        print(f"      «{r['cita']}»")

    sub("agentes con más citas seleccionadas")
    top = q("""
        SELECT agent_name AS agente, count(*) AS citas,
               round(avg(impacto_score)::numeric,2) AS impacto_medio
        FROM agent_quotes GROUP BY agent_name
        ORDER BY citas DESC LIMIT 15
    """)
    print(top.to_string(index=False))

    sub("eventos del mundo más frecuentes")
    ev = q("""
        SELECT left(event_description, 70) AS evento, count(*) AS veces
        FROM turns WHERE event_description IS NOT NULL AND event_description <> ''
        GROUP BY evento ORDER BY veces DESC LIMIT 15
    """)
    print(ev.to_string(index=False) if len(ev) else "    (sin eventos)")

    sub("arcos narrativos (muestra)")
    arcos = q("""
        SELECT agent_name AS agente, tier, left(resumen_arco, 150) AS arco
        FROM agent_profiles
        WHERE resumen_arco IS NOT NULL AND resumen_arco <> ''
        ORDER BY total_respuestas DESC NULLS LAST LIMIT 8
    """)
    for _, r in arcos.iterrows():
        print(f"\n    {r['agente']} (tier {r['tier']})")
        print(f"      {r['arco']}")


# ══════════════════════════════════════════════════════════════════════
# PRÉSTAMOS — la esfera de contacto y su difusión por tier
# ══════════════════════════════════════════════════════════════════════

def _voz_sql(col: str = "word") -> str:
    """SQL que normaliza una columna a la FORMA DE LA ESFERA.

    La tabla está declarada UNA vez, en `curiana_lexicon.FORMA_DE_LA_ESFERA`
    («la etiqueta manda», Miguel 2026-09-18), y el CASE se genera de ella: si
    mañana entra un par nuevo, esta vista lo hereda sin tocarse.

    Hace falta al LEER porque los runs viejos no se reescriben: sus filas
    guardan la grafía castellana en `word` y no tienen `forma_dicha`. Una fila
    de `loanword_uses` es un hecho observado (principio del 2026-09-17).
    """
    from curiana_lexicon import FORMA_DE_LA_ESFERA
    ramas = " ".join(f"WHEN {col} = '{k}' THEN '{v}'"
                     for k, v in FORMA_DE_LA_ESFERA.items())
    return f"(CASE {ramas} ELSE {col} END)"


def _dicha_sql() -> str:
    """Lo que el agente escribió. NULL en las filas anteriores al 2026-09-18,
    donde `word` ES la forma dicha."""
    return "coalesce(forma_dicha, word)"


def _con_dicha(voz: str, dichas) -> str:
    """«cazabi (casabe)» — la forma de la esfera y, entre paréntesis, la dicha
    cuando difiere. Sin paréntesis cuando el agente ya la escribió así."""
    otras = sorted({d for d in (dichas or "").split("|") if d and d != voz})
    return f"{voz} ({', '.join(otras)})" if otras else voz


def analizar_prestamos() -> None:
    """Lectura mínima de `loanword_uses`: qué voces de la esfera de contacto
    (taíno, kalinago, paraujano, caribe continental, jirajaroide) se usaron,
    por qué tier, y si bajaron del tier 1 —el único que ve el bloque [Voces de
    fuera]— al 2 y al 3. Hasta el 2026-09-16 esto se medía re-puntuando
    `response_text` a mano (bitácora del run c6837386).

    Desde el 2026-09-18 la voz se agrupa por su FORMA DE LA ESFERA y la forma
    dicha va entre paréntesis cuando difiere: `casabe` y `cazabi` son la misma
    voz y su difusión es una sola serie, pero que el agente escribiera «casabe»
    no se pierde."""
    titulo("PRÉSTAMOS — la esfera de contacto, medida aparte")

    try:
        q("SELECT forma_dicha FROM loanword_uses LIMIT 1")
    except RuntimeError:
        print("\n    (sin tabla loanword_uses o sin la columna forma_dicha: "
              "aplicar supabase/migrations/20260916000000_loanword_uses.sql y "
              "20260918000000_loanword_forma_dicha.sql — ver CLAUDE.md)")
        return

    voz, dicha = _voz_sql(), _dicha_sql()

    normalizadas = q(f"""
        SELECT count(*) AS filas
        FROM loanword_uses WHERE {voz} <> {dicha}
    """)
    n_norm = int(normalizadas["filas"].iloc[0]) if len(normalizadas) else 0
    if n_norm:
        print(f"\n    ({n_norm} filas se leen con la forma de la esfera: la "
              f"dicha va entre paréntesis. Los runs viejos no se reescriben.)")

    sub("usos por lengua y tier (todos los runs)")
    por_tier = q(f"""
        SELECT source_language AS lengua, tier, count(*) AS usos,
               count(DISTINCT {voz}) AS formas,
               count(DISTINCT agent_name) AS agentes,
               count(DISTINCT run_id) AS runs
        FROM loanword_uses GROUP BY source_language, tier
        ORDER BY source_language, tier
    """)
    if not len(por_tier):
        print("    (ningún préstamo registrado todavía)")
        return
    print(por_tier.to_string(index=False))

    sub("difusión: primer día por tier de cada voz (¿bajó del tier 1?)")
    dif = q(f"""
        SELECT run_id, {voz} AS voz, string_agg(DISTINCT {dicha}, '|') AS dichas,
               source_language AS lengua,
               min(day) FILTER (WHERE tier = 1) AS d_t1,
               min(day) FILTER (WHERE tier = 2) AS d_t2,
               min(day) FILTER (WHERE tier = 3) AS d_t3,
               count(DISTINCT agent_name) FILTER (WHERE tier = 1) AS ag_t1,
               count(DISTINCT agent_name) FILTER (WHERE tier > 1) AS ag_t23,
               count(*) AS usos
        FROM loanword_uses GROUP BY run_id, {voz}, source_language
        ORDER BY usos DESC LIMIT 30
    """)
    dif.insert(0, "run", dif["run_id"].astype(str).str[:8])
    dif["voz"] = [_con_dicha(v, d) for v, d in zip(dif["voz"], dif["dichas"])]
    print(dif.drop(columns=["run_id", "dichas"]).to_string(index=False))
    print(f"\n    voces que llegaron al tier 2/3: {int((dif['ag_t23'] > 0).sum())} "
          f"de {len(dif)} (las 30 más usadas)")

    sub("por día y tier (¿la difusión crece con los días?)")
    dia = q(f"""
        SELECT run_id, day,
               count(*) FILTER (WHERE tier = 1) AS t1,
               count(*) FILTER (WHERE tier = 2) AS t2,
               count(*) FILTER (WHERE tier = 3) AS t3,
               count(DISTINCT {voz}) AS formas
        FROM loanword_uses GROUP BY run_id, day ORDER BY run_id, day
    """)
    dia.insert(0, "run", dia["run_id"].astype(str).str[:8])
    print(dia.drop(columns="run_id").to_string(index=False))

    _prestamos_por_cadena()


def _prestamos_por_cadena() -> None:
    """Los mismos usos, sumados por CADENA: en la era 2 un run es un día y la
    difusión de una voz de la esfera se juzga a lo largo de los días, no dentro
    de uno.

    A diferencia de la serie de koiné, aquí NO se saltan los runs
    interrumpidos, sólo se marcan: un uso registrado es un hecho observado, no
    una métrica de día cerrado. (Y hoy los únicos préstamos de la base son de
    uno interrumpido — saltarlo dejaría la vista vacía sin decir por qué.)"""
    lector = LectorSQL(CONTENEDOR)
    cadenas = cadenas_en_la_base(lector)
    if not cadenas:
        return
    sub("por cadena (los días encadenados con --continuar)")
    for cadena in cadenas:
        ids = [id_de(r) for r in cadena]
        filas = lector.prestamos(ids)
        cortados = {corto(id_de(r)) for r in cadena if es_interrumpido(r)}
        print(f"\n    {resumen_de_cadena(cadena)}")
        if not filas:
            print("      (ningún préstamo registrado en la cadena)")
            continue
        from curiana_lexicon import forma_de_la_esfera
        df = pd.DataFrame(filas)
        df["day"] = df["day"].astype(int)
        df["tier"] = df["tier"].astype(int)
        df["run"] = df["run_id"].astype(str).str[:8]
        # La voz se agrupa por su forma de la esfera; los runs viejos guardan
        # la castellana en `word` y no se reescriben.
        df["voz"] = [forma_de_la_esfera(w) for w in df["word"]]
        tabla = (df.groupby(["day", "tier"])
                   .agg(usos=("voz", "size"), formas=("voz", "nunique"),
                        agentes=("agent_name", "nunique"),
                        runs=("run", lambda s: ", ".join(sorted(set(s)))))
                   .reset_index())
        tabla["nota"] = ["⚠ interrumpido" if set(r.split(", ")) & cortados else ""
                         for r in tabla["runs"]]
        print("\n".join("      " + l
                        for l in tabla.to_string(index=False).splitlines()))
        voces = sorted({_con_dicha(v, "|".join(sorted(set(g["forma_dicha"]))))
                        for v, g in df.groupby("voz")})
        print(f"      voces distintas en la cadena: {df['voz'].nunique()} · "
              f"tier 2/3: {int((df['tier'] > 1).sum())} de {len(df)} usos")
        print(f"      {' · '.join(voces)}")


# ══════════════════════════════════════════════════════════════════════
# RAÍCES — lo que se dijo en caquetío sin serlo
# ══════════════════════════════════════════════════════════════════════

def analizar_raices() -> None:
    """Cuántas formas de cada run tienen la RAÍZ fuera del lexicón.

    Los runs ya corridos NO se reescriben: `word_uses.source_language` sigue
    diciendo «caquetío» para `lumina-bana-iro`, que es lo que la base guardó.
    Esto lo vuelve a clasificar al LEER, con la regla de hoy
    (`curiana_lexicon.es_raiz_de_ninguna_parte`), para que los seis runs de la
    serie C se puedan leer con el dato.

    ⚠ Un falso positivo declarado, y es grande en la era 1: el lexicón se
    mueve. `chacamba`, `corie`, `canoa` o `hamaca` eran claves del canon en
    junio y hoy no están, así que salen aquí como raíz de ninguna parte sin
    serlo el día en que se dijeron. La columna `era` deja separarlo a ojo; la
    reconstrucción del lexicón histórico, commit a commit, la hace
    `6-fusion/scripts/medir_raices_de_ninguna_parte.py`, que es la medición
    buena.
    """
    from curiana_lexicon import es_raiz_de_ninguna_parte, nucleo_de_token

    titulo("RAÍCES DE NINGUNA PARTE — morfología caquetía sobre raíz ajena")

    df = q("""
        SELECT substring(w.run_id::text, 1, 8) AS run,
               coalesce(s.config->>'elenco', 'era1') AS era,
               coalesce(s.config->>'serie', '-') AS serie,
               w.word, count(*) AS usos,
               count(DISTINCT w.agent_name) AS agentes
        FROM word_uses w JOIN simulation_runs s ON s.id = w.run_id
        WHERE w.source_language = 'caquetío'
        GROUP BY 1, 2, 3, 4
    """)
    if df.empty:
        print("    (no hay word_uses marcados «caquetío»)")
        return
    df["word"] = df["word"].astype(str)
    df["ninguna"] = [es_raiz_de_ninguna_parte(w) for w in df["word"]]
    df["raiz"] = ["-".join(nucleo_de_token(w)) for w in df["word"]]

    sub("por era y serie")
    por = (df.groupby(["era", "serie"])
             .agg(formas=("word", "size"), usos=("usos", "sum"))
             .reset_index())
    mal = (df[df["ninguna"]].groupby(["era", "serie"])
             .agg(formas_raiz=("word", "size"), usos_raiz=("usos", "sum"),
                  raices=("raiz", "nunique")).reset_index())
    tabla = por.merge(mal, on=["era", "serie"], how="left").fillna(0)
    for c in ("formas_raiz", "usos_raiz", "raices"):
        tabla[c] = tabla[c].astype(int)
    tabla["pct_usos"] = (100.0 * tabla["usos_raiz"] / tabla["usos"]).round(2)
    print(tabla.to_string(index=False))

    sub("por run (sólo los que tienen alguna)")
    por_run = (df[df["ninguna"]].groupby(["run", "era", "serie"])
                 .agg(formas=("word", "size"), usos=("usos", "sum"),
                      raices=("raiz", "nunique")).reset_index()
                 .sort_values("usos", ascending=False))
    if por_run.empty:
        print("    (ninguna)")
    else:
        print(por_run.to_string(index=False))

    sub("las 25 raíces de ninguna parte más dichas")
    top = (df[df["ninguna"]].groupby("raiz")
             .agg(usos=("usos", "sum"), formas=("word", "nunique"),
                  eras=("era", lambda s: ", ".join(sorted(set(s)))))
             .reset_index().sort_values("usos", ascending=False).head(25))
    print(top.to_string(index=False))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Análisis de los runs de Curiana")
    ap.add_argument("--koine", action="store_true")
    ap.add_argument("--lengua", action="store_true")
    ap.add_argument("--neologismos", action="store_true")
    ap.add_argument("--agentes", action="store_true")
    ap.add_argument("--narrativa", action="store_true")
    ap.add_argument("--prestamos", action="store_true")
    ap.add_argument("--raices", action="store_true")
    ap.add_argument("--todo", action="store_true")
    a = ap.parse_args(argv)

    if a.todo or not any(vars(a).values()):
        a.koine = a.lengua = a.neologismos = a.agentes = a.narrativa = True
        a.prestamos = a.raices = True

    if a.koine:
        analizar_koine()
        analizar_cadenas()
    if a.lengua:
        analizar_lengua()
    if a.neologismos:
        analizar_neologismos()
    if a.agentes:
        analizar_agentes()
    if a.narrativa:
        analizar_narrativa()
    if a.prestamos:
        analizar_prestamos()
    if a.raices:
        analizar_raices()
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
