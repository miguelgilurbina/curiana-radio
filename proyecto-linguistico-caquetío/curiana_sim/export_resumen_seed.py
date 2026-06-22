"""
Exporta los seeds curados de Resumen y Neologismos para /simulador en
Curiana Radio -- mismo espiritu evergreen que export_personajes_seed.py
(sin realtime, sin conexion en produccion).

Cruza neologisms con las citas ya curadas en content/simulador/personajes.json
para marcar como "destacado" cualquier neologismo cuya forma aparezca en una
frase de alto impacto -- en vez de inventar una nota editorial aparte.

Uso:
    python export_resumen_seed.py [run_id]
    (sin argumento usa el run mas reciente con perfiles)
"""
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import CurianaDB

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "content", "simulador")
PERSONAJES_PATH = os.path.join(CONTENT_DIR, "personajes.json")
UMBRAL_DESTACADO = 8.5  # impacto_score minimo de una cita para "prender" un neologismo


def cruzar_con_citas(neos: list[dict]) -> list[dict]:
    try:
        with open(PERSONAJES_PATH, encoding="utf-8") as f:
            personajes = json.load(f)["personajes"]
    except FileNotFoundError:
        personajes = []

    citas = [
        (q["quote"], q.get("traduccion", ""), q.get("impacto_score") or 0, p["nombre"], p["slug"])
        for p in personajes
        for q in p["quotes"]
    ]

    for n in neos:
        forma = n["form"].lower()
        mejor = None
        for quote, traduccion, score, nombre, slug in citas:
            # coincidencia de la forma COMPLETA del neologismo, no de su raíz --
            # una raíz suelta (ej. "ma", "kali") aparece en casi cualquier frase
            # y no significa que ESE neologismo en particular haya resurgido.
            if forma in quote.lower() and score >= UMBRAL_DESTACADO:
                if not mejor or score > mejor["impacto_score"]:
                    mejor = {
                        "quote": quote, "traduccion": traduccion,
                        "impacto_score": score, "agente": nombre, "agente_slug": slug,
                    }
        n["destacado"] = mejor
    return neos


def main():
    run_id = sys.argv[1] if len(sys.argv) > 1 else None
    db = CurianaDB()

    if not run_id:
        latest = (
            db.client.table("agent_profiles").select("run_id")
            .order("created_at", desc=True).limit(1).execute().data
        )
        if not latest:
            print("No hay agent_profiles en Supabase.")
            sys.exit(1)
        run_id = latest[0]["run_id"]

    run = db.client.table("simulation_runs").select("*").eq("id", run_id).execute().data[0]

    drift = (
        db.client.table("language_drift_by_turn").select("*")
        .eq("run_id", run_id).order("day").order("turn_num").execute().data
    )

    neos = db.client.table("neologisms").select("*").eq("run_id", run_id).execute().data
    neos = cruzar_con_citas(neos)

    adoptados = [n for n in neos if n["status"] == "adoptado"]
    avg_score = round(sum(d["avg_score"] for d in drift) / len(drift), 2) if drift else None
    pct_caquetio_final = drift[-1]["avg_caquetio"] if drift else None

    resumen = {
        "run_id": run_id,
        "started_at": run["started_at"],
        "ended_at": run.get("ended_at"),
        "total_days": run.get("total_days"),
        "total_turns": run.get("total_turns"),
        "model": run.get("model"),
        "avg_score": avg_score,
        "pct_caquetio_final": pct_caquetio_final,
        "total_neologismos": len(neos),
        "total_adoptados": len(adoptados),
        "drift": drift,
    }

    os.makedirs(CONTENT_DIR, exist_ok=True)
    with open(os.path.join(CONTENT_DIR, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    with open(os.path.join(CONTENT_DIR, "neologismos.json"), "w", encoding="utf-8") as f:
        json.dump({"run_id": run_id, "neologismos": neos}, f, ensure_ascii=False, indent=2)

    n_destacados = len([n for n in neos if n["destacado"]])
    print(f"resumen.json escrito ({len(drift)} filas de deriva)")
    print(f"neologismos.json escrito ({len(neos)} neologismos, {n_destacados} destacados)")


if __name__ == "__main__":
    main()
