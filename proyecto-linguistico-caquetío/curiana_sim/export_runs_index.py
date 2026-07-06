"""
Exporta el ÍNDICE cross-run de evolución para /simulador en Curiana Radio.

A diferencia de los otros export_*_seed.py (que escriben el detalle de UN run),
este produce la espina dorsal comparativa: una fila por run curado con sus
métricas clave, para que la página pueda contar la EVOLUCIÓN entre simulaciones
(8% → 92% → 99% de caquetío, deriva plana → koiné con diccionario → experimento
de control). Ver MIGRACION_RUNS_EVOLUCION.md.

Filosofía evergreen (igual que el resto de exporters): lee de Supabase LOCAL y
escribe JSON estático commiteado; la página en producción nunca toca la base.

La CURACIÓN es explícita: solo se exportan los runs listados en MANIFIESTO, con
su hito editorial y categoría. Los smokes y runs de desarrollo NO se publican —
quedan documentados en BITACORA_RUNS.md, no en la página. Añadir un run nuevo =
una línea en MANIFIESTO.

Uso:
    python export_runs_index.py
    (sin argumentos; la selección vive en MANIFIESTO abajo)
"""
import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import CurianaDB

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "content", "simulador")
RUNS_DIR = os.path.join(CONTENT_DIR, "runs")

# --- Curación editorial ----------------------------------------------------
# Prefijo de 8 chars del run_id → metadatos editoriales. El orden define el
# orden narrativo en la página (cronológico = arco del proyecto). Categorías:
#   insignia    → el run destacado que la página cuenta en detalle
#   koine       → runs de la era koiné (convergencia + fijación)
#   experimento → el par normal/ablación (la evidencia de control)
#   baseline    → hito histórico (primer run calibrado)
# `pareja` enlaza un run de ablación con su control normal (mismo experimento).
MANIFIESTO = [
    {"id8": "2e729f3f", "categoria": "baseline",
     "hito": "Primer run largo calibrado — caquetío al 92%, deriva plana"},
    {"id8": "f8ef263d", "categoria": "koine",
     "hito": "Primer run koiné — convergencia confirmada"},
    {"id8": "9bb920eb", "categoria": "koine",
     "hito": "Run largo (60T) — población constante, métrica persistida"},
    {"id8": "20091e1f", "categoria": "koine",
     "hito": "Fijación por competencia — diccionario koiné de 7 conceptos"},
    {"id8": "038d7b9d", "categoria": "experimento", "rol": "normal", "pareja": "bdc54134",
     "hito": "Experimento de control (normal) — koiné con andamiaje"},
    {"id8": "bdc54134", "categoria": "experimento", "rol": "ablacion", "pareja": "038d7b9d",
     "hito": "Experimento de control (ablación) — sin las 3 inyecciones"},
]


def _first_last(rows: list[dict], col: str):
    """Primer y último valor no-nulo de una columna ordenada por día."""
    vals = [(r["day"], r[col]) for r in rows if r.get(col) is not None]
    if not vals:
        return None, None
    vals.sort()
    return vals[0][1], vals[-1][1]


def convergencia(metrics: list[dict]) -> dict | None:
    """Resume la convergencia con la lectura MÁS EXIGENTE que tenga datos.

    Preferencia: emergente > ventana > acumulada. Los runs anteriores a la
    corrección metodológica del 2026-07-04 solo tienen la acumulada (las otras
    columnas son NULL); se reporta esa y se marca la lectura usada para que la
    página pueda mostrar la reserva (la acumulada infla por acumulación del
    léxico base compartido — ver DISENO_KOINE.md §7).
    """
    if not metrics:
        return None
    metrics = sorted(metrics, key=lambda r: r["day"])
    for col, lectura in (
        ("distance_emergente", "emergente"),
        ("distance_ventana", "ventana"),
        ("distance", "acumulada"),
    ):
        ini, fin = _first_last(metrics, col)
        if ini is not None and fin is not None:
            ini, fin = float(ini), float(fin)
            delta_pct = round((fin - ini) / ini * 100, 1) if ini else None
            return {
                "lectura": lectura,
                "inicio": round(ini, 4),
                "fin": round(fin, 4),
                "delta_pct": delta_pct,
                "dias": len(metrics),
                # Serie completa de la lectura elegida, para un sparkline.
                "serie": [
                    round(float(r[col]), 4) for r in metrics if r.get(col) is not None
                ],
            }
    return None


def resumir_run(db: CurianaDB, entrada: dict) -> dict | None:
    id8 = entrada["id8"]
    runs = db.client.table("simulation_runs").select("*").execute().data
    run = next((r for r in runs if r["id"].startswith(id8)), None)
    if not run:
        print(f"  ⚠  {id8}: no está en simulation_runs, se omite")
        return None
    run_id = run["id"]

    resp = (
        db.client.table("agent_responses")
        .select("score,pct_caquetio,agent_name")
        .eq("run_id", run_id).execute().data
    )
    n_resp = len(resp)
    agentes = len({r["agent_name"] for r in resp})
    avg_score = round(sum(r["score"] for r in resp) / n_resp, 2) if n_resp else None
    pct_caq = round(sum(r["pct_caquetio"] for r in resp) / n_resp, 3) if n_resp else None

    neos = db.client.table("neologisms").select("status").eq("run_id", run_id).execute().data
    adoptados = len([n for n in neos if n["status"] == "adoptado"])

    metrics = db.client.table("koine_metrics").select("*").eq("run_id", run_id).execute().data
    fijadas = db.client.table("koine_lexicon").select("*").eq("run_id", run_id).execute().data

    return {
        "id8": id8,
        "seed_run_id": run_id,
        "categoria": entrada["categoria"],
        "rol": entrada.get("rol"),
        "pareja": entrada.get("pareja"),
        "hito": entrada["hito"],
        "started_at": run["started_at"],
        "total_dias": run.get("total_days"),
        "total_turnos": run.get("total_turns"),
        "agentes": agentes,
        "respuestas": n_resp,
        "avg_score": avg_score,
        "pct_caquetio": pct_caq,
        "neologismos_adoptados": adoptados,
        "convergencia": convergencia(metrics),
        "fijacion": {
            "conceptos_fijados": len(fijadas),
            "formas": sorted(
                (
                    {"concepto": f["concepto_id"], "form": f["form"],
                     "fijada_dia": f.get("fijada_dia"), "n_variantes": f.get("n_variantes")}
                    for f in fijadas
                ),
                key=lambda x: x["fijada_dia"] or 999,
            ),
        } if fijadas else None,
    }


def main():
    db = CurianaDB()
    filas = []
    for entrada in MANIFIESTO:
        fila = resumir_run(db, entrada)
        if fila:
            filas.append(fila)
            conv = fila["convergencia"]
            conv_txt = (
                f"{conv['lectura']} {conv['delta_pct']:+}%" if conv else "sin métrica"
            )
            print(f"  ✓ {fila['id8']} · {fila['categoria']:11} · caq {fila['pct_caquetio']} · {conv_txt}")

    index = {
        "version": 1,
        "generado": datetime.now(timezone.utc).isoformat(),
        "runs": filas,
    }

    os.makedirs(RUNS_DIR, exist_ok=True)
    out = os.path.join(RUNS_DIR, "index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\nruns/index.json escrito ({len(filas)} runs curados)")


if __name__ == "__main__":
    main()
