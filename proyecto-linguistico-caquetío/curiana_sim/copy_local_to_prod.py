"""
One-off: copia el lexicon completo + el run curado (2e729f3f) de Supabase
LOCAL a Supabase de PRODUCCION (curiana-produccion), preservando los ids
existentes para que las foreign keys entre tablas sigan siendo validas.

No toca .env.local del sitio (el sitio no consulta produccion en runtime,
solo el pipeline de Python lo hace).

La credencial de produccion (service_role) se obtiene en el momento via el
CLI de Supabase (ya logueado) -- nunca se escribe a disco ni se tipea en
ningun comando, evitando que quede en texto plano en esta carpeta
(sincronizada con OneDrive) o en el historial de shell.

Uso: python copy_local_to_prod.py
"""
import json
import os
import subprocess

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from supabase import create_client

LOCAL_URL = os.environ["SUPABASE_URL"]
LOCAL_KEY = os.environ["SUPABASE_SERVICE_KEY"]

PROD_REF = "edygyxlcvvgnvdsqxnsm"
PROD_URL = f"https://{PROD_REF}.supabase.co"
_keys = json.loads(
    subprocess.run(
        f"supabase projects api-keys --project-ref {PROD_REF}",
        shell=True, capture_output=True, text=True, check=True,
    ).stdout
)["keys"]
_service_keys = [k["api_key"] for k in _keys if k["id"] == "service_role"]
if not _service_keys:
    raise RuntimeError(
        f"No se encontro una llave 'service_role' para el proyecto {PROD_REF}. "
        "Revisa `supabase projects api-keys --project-ref ...` -- puede que la "
        "API haya cambiado el formato o el proyecto no tenga esa llave provisionada."
    )
PROD_KEY = _service_keys[0]

RUN_ID = "2e729f3f-ebf4-4d23-8142-c4c65b06e27b"

local = create_client(LOCAL_URL, LOCAL_KEY)
prod = create_client(PROD_URL, PROD_KEY)


def fetch_all(client, table, filt=None, in_filt=None):
    desde = 0
    todas = []
    while True:
        q = client.table(table).select("*")
        if filt:
            q = q.eq(*filt)
        if in_filt:
            q = q.in_(*in_filt)
        page = q.range(desde, desde + 999).execute().data
        todas.extend(page)
        if len(page) < 1000:
            break
        desde += 1000
    return todas


def copy_table(table, rows, label=None):
    label = label or table
    if not rows:
        print(f"  {label}: 0 filas (omitido)")
        return
    # upsert (no insert): el script debe poder re-correrse sobre un proyecto
    # ya poblado (ej. tras promover un run anterior) sin romper por llave
    # duplicada -- se preservan los ids originales a proposito (ver docstring).
    for i in range(0, len(rows), 500):
        prod.table(table).upsert(rows[i:i + 500], on_conflict="id").execute()
    print(f"  {label}: {len(rows)} filas copiadas")


def main():
    print("Lexicon completo...")
    lexicon_rows = fetch_all(local, "lexicon")
    copy_table("lexicon", lexicon_rows)

    print(f"\nRun curado {RUN_ID}...")
    copy_table("simulation_runs", fetch_all(local, "simulation_runs", ("id", RUN_ID)))
    copy_table("turns", fetch_all(local, "turns", ("run_id", RUN_ID)))
    responses = fetch_all(local, "agent_responses", ("run_id", RUN_ID))
    copy_table("agent_responses", responses)
    copy_table("word_uses", fetch_all(local, "word_uses", ("run_id", RUN_ID)))
    copy_table("neologisms", fetch_all(local, "neologisms", ("run_id", RUN_ID)))
    # phrase_etymologies no tiene run_id propio (solo response_id) -- se
    # escopea via los ids de agent_responses que ya filtramos por RUN_ID,
    # para no copiar etimologias de otros runs cuyo agent_response no existe
    # en produccion (rompe la foreign key al insertar).
    response_ids = [r["id"] for r in responses]
    etymologies = (
        fetch_all(local, "phrase_etymologies", in_filt=("response_id", response_ids))
        if response_ids else []
    )
    copy_table("phrase_etymologies", etymologies)
    profiles = fetch_all(local, "agent_profiles", ("run_id", RUN_ID))
    copy_table("agent_profiles", profiles)
    copy_table("agent_quotes", fetch_all(local, "agent_quotes", ("run_id", RUN_ID)))

    print("\nListo.")


if __name__ == "__main__":
    main()
