#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — análisis de los runs almacenados
==========================================

Lee la base local (Supabase/Postgres en Docker) y responde las tres preguntas
que el proyecto se hace sobre sus propios datos:

    --koine     ¿Hubo koineización? El contraste normal vs. ablación, con
                estadística y no solo con medias.
    --lengua    ¿Qué le pasó a la lengua? Composición, deriva, neologismos,
                distribución del léxico.
    --agentes   ¿Cómo se comportaron? Prestigio, adopción, diferencias por
                tier y etnia.
    --narrativa ¿Qué historias salieron? Citas, arcos, eventos.

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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Análisis de los runs de Curiana")
    ap.add_argument("--koine", action="store_true")
    ap.add_argument("--lengua", action="store_true")
    ap.add_argument("--neologismos", action="store_true")
    ap.add_argument("--agentes", action="store_true")
    ap.add_argument("--narrativa", action="store_true")
    ap.add_argument("--todo", action="store_true")
    a = ap.parse_args(argv)

    if a.todo or not any(vars(a).values()):
        a.koine = a.lengua = a.neologismos = a.agentes = a.narrativa = True

    if a.koine:
        analizar_koine()
    if a.lengua:
        analizar_lengua()
    if a.neologismos:
        analizar_neologismos()
    if a.agentes:
        analizar_agentes()
    if a.narrativa:
        analizar_narrativa()
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
