"""
Exporta un seed curado de personajes para la sección evergreen /simulador
de Curiana Radio: une el perfil narrativo + citas generadas por el Observer
(Supabase, por run) con la biografía estática de cada agente (curiana_agents.py).

No se conecta a producción: lee de Supabase LOCAL y escribe un JSON versionado
en el repo de Curiana Radio. Re-correr este script tras cada run curado
(--perfiles) es, por ahora, el "seeding" — la sincronización automática con
una base de producción queda para cuando definamos cómo crece across runs.

Uso:
    python export_personajes_seed.py [run_id]
    (sin argumento usa el run más reciente con perfiles)
"""
import json
import os
import re
import sys
import unicodedata

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_agents import ALL_AGENTS
from curiana_database import CurianaDB

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "content", "simulador", "personajes.json"
)


def slugify(nombre: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9-]+", "", sin_acentos.lower().replace(" ", "-"))


def main():
    db = CurianaDB()

    run_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not run_id:
        latest = (
            db.client.table("agent_profiles")
            .select("run_id")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
            .data
        )
        if not latest:
            print("No hay agent_profiles en Supabase. Corre una simulación con --perfiles primero.")
            sys.exit(1)
        run_id = latest[0]["run_id"]

    run = db.client.table("simulation_runs").select("*").eq("id", run_id).execute().data
    run = run[0] if run else None

    profiles = (
        db.client.table("agent_profiles").select("*").eq("run_id", run_id).execute().data
    )
    quotes = (
        db.client.table("agent_quotes")
        .select("*")
        .eq("run_id", run_id)
        .order("impacto_score", desc=True)
        .execute()
        .data
    )
    quotes_by_agent: dict[str, list[dict]] = {}
    for q in quotes:
        quotes_by_agent.setdefault(q["agent_name"], []).append(q)

    personajes = []
    for p in profiles:
        nombre = p["agent_name"]
        bio = ALL_AGENTS.get(nombre, {})
        personajes.append({
            "slug": slugify(nombre),
            "nombre": nombre,
            "tier": p.get("tier") or bio.get("tier"),
            "genero": bio.get("genero"),
            "edad": bio.get("edad"),
            "etnia": bio.get("etnia", "caquetío"),
            "ubicacion_default": bio.get("ubicacion_default"),
            "descripcion": bio.get("descripcion", ""),
            "rol_comunidad": p.get("rol_comunidad", ""),
            "resumen_arco": p.get("resumen_arco", ""),
            "total_respuestas": p.get("total_respuestas", 0),
            "avg_score": p.get("avg_score"),
            "neologismos_propuestos": p.get("neologismos_propuestos", 0),
            "neologismos_adoptados": p.get("neologismos_adoptados", 0),
            "quotes": [
                {
                    "quote": q["quote"],
                    "traduccion": q.get("translation", ""),
                    "justificacion": q.get("justificacion", ""),
                    "impacto_score": q.get("impacto_score"),
                    "day": q.get("day"),
                    "turn_num": q.get("turn_num"),
                }
                for q in quotes_by_agent.get(nombre, [])
            ],
        })

    personajes.sort(key=lambda x: (x["tier"] or 9, -(x["avg_score"] or 0)))

    seed = {
        "run_id": run_id,
        "run_started_at": run.get("started_at") if run else None,
        "total_days": run.get("total_days") if run else None,
        "total_turns": run.get("total_turns") if run else None,
        "personajes": personajes,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

    print(f"{len(personajes)} personajes exportados -> {os.path.abspath(OUT_PATH)}")


if __name__ == "__main__":
    main()
