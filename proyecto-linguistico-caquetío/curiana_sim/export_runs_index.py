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

TURNOS Y DÍAS SE MIDEN, NO SE LEEN DE LA FILA (issue #42)
--------------------------------------------------------
`simulation_runs.total_turns` / `total_days` los escribe SOLO
`CurianaDB.end_run()`, y el orquestador lo llama después del bucle, sin
`try/finally`. Un run cortado antes de terminar (`20091e1f`: el teardown lo
paró en el turno 57) se queda con el `DEFAULT 0` del esquema y `ended_at` NULL,
aunque sus turnos y respuestas estén en la base. Por eso aquí:

    total_turnos = filas de `turns` del run   (turn_num solo vale 1 o 2)
    total_dias   = max(turns.day)             (= state.dia - 1 en un run completo)

Si la fila dice otra cosa, se AVISA por consola: la discrepancia es un dato
sobre el run (interrumpido, turnos sin guardar), no algo que el índice deba
tapar. La forma del JSON no cambia.

Toda query pasa por `todas_las_filas()`: PostgREST corta en max_rows (1000) EN
SILENCIO, y un run de 60 turnos ya tiene ~300 respuestas.

Uso:
    python export_runs_index.py
    (sin argumentos; la selección vive en MANIFIESTO abajo)
"""
import io
import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import CurianaDB

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "content", "simulador")
RUNS_DIR = os.path.join(CONTENT_DIR, "runs")

# Filas pedidas por página. El max_rows del PostgREST local es 1000; si alguien
# lo baja, `todas_las_filas` sigue juntando todo (avanza por lo que llegó).
PAGINA = 1000

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


def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 y este script imprime ⚠ ✓ ·."""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def todas_las_filas(construir, pagina: int = PAGINA) -> list[dict]:
    """Trae TODAS las filas de una query de PostgREST, página a página.

    `construir` es una función sin argumentos que devuelve la query sin ejecutar
    (tabla + select + filtros). Se reconstruye en cada página porque el
    `.range()` de postgrest-py AÑADE `offset`/`limit` a los parámetros en vez de
    reemplazarlos: reutilizar el mismo builder apila rangos. Se ordena por `id`
    (todas las tablas lo tienen) para que las páginas no se solapen ni salten.

    Para con la primera página VACÍA, no con la primera corta: si el servidor
    tuviera un max_rows menor que `pagina`, parar en la página corta volvería a
    truncar en silencio, que es justo lo que esto evita. Cuesta una petición más.
    """
    filas: list[dict] = []
    desde = 0
    while True:
        lote = (
            construir().order("id").range(desde, desde + pagina - 1).execute().data
            or []
        )
        if not lote:
            return filas
        filas.extend(lote)
        desde += len(lote)


def medir_turnos(db: CurianaDB, run_id: str) -> tuple[int, int]:
    """(turnos, días) del run medidos sobre `turns`, no sobre `simulation_runs`.

    Turnos = filas, porque `turn_num` guarda `state.turno` (1 o 2), no un
    contador global. Días = el mayor `day` registrado; en un run cortado a mitad
    de día cuenta ese día empezado (el 57/29 de BITACORA_RUNS para `20091e1f`).
    """
    turnos = todas_las_filas(
        lambda: db.client.table("turns").select("id,day").eq("run_id", run_id)
    )
    return len(turnos), max((t["day"] for t in turnos), default=0)


def avisos_de_medicion(run: dict, total_turnos: int, total_dias: int,
                       n_resp: int) -> list[str]:
    """Lo que la fila de `simulation_runs` dice y la medición no confirma."""
    avisos = []
    for columna, medido in (("total_turns", total_turnos), ("total_days", total_dias)):
        en_fila = run.get(columna)
        if en_fila != medido:
            avisos.append(f"{columna}: la fila dice {en_fila}, medido {medido}")
    if run.get("ended_at") is None:
        avisos.append("ended_at es NULL: el run no pasó por end_run() (¿interrumpido?)")
    if n_resp and not total_turnos:
        avisos.append(f"{n_resp} respuestas y ningún turno en `turns` (¿falló save_turn?)")
    return avisos


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


def resumir_run(db: CurianaDB, entrada: dict, runs: list[dict] | None = None,
                avisos: list[str] | None = None) -> dict | None:
    """Una fila del índice. `runs` evita releer `simulation_runs` por cada run;
    `avisos` acumula las discrepancias fila↔medición para el resumen final."""
    id8 = entrada["id8"]
    if runs is None:
        runs = todas_las_filas(lambda: db.client.table("simulation_runs").select("*"))
    run = next((r for r in runs if r["id"].startswith(id8)), None)
    if not run:
        print(f"  ⚠  {id8}: no está en simulation_runs, se omite")
        return None
    run_id = run["id"]

    resp = todas_las_filas(
        lambda: db.client.table("agent_responses")
        .select("id,score,pct_caquetio,agent_name")
        .eq("run_id", run_id)
    )
    n_resp = len(resp)
    agentes = len({r["agent_name"] for r in resp})
    avg_score = round(sum(r["score"] for r in resp) / n_resp, 2) if n_resp else None
    pct_caq = round(sum(r["pct_caquetio"] for r in resp) / n_resp, 3) if n_resp else None

    total_turnos, total_dias = medir_turnos(db, run_id)
    for aviso in avisos_de_medicion(run, total_turnos, total_dias, n_resp):
        print(f"  ⚠  {id8}: {aviso}")
        if avisos is not None:
            avisos.append(f"{id8}: {aviso}")

    neos = todas_las_filas(
        lambda: db.client.table("neologisms").select("id,status").eq("run_id", run_id)
    )
    adoptados = len([n for n in neos if n["status"] == "adoptado"])

    metrics = todas_las_filas(
        lambda: db.client.table("koine_metrics").select("*").eq("run_id", run_id)
    )
    fijadas = todas_las_filas(
        lambda: db.client.table("koine_lexicon").select("*").eq("run_id", run_id)
    )

    return {
        "id8": id8,
        "seed_run_id": run_id,
        "categoria": entrada["categoria"],
        "rol": entrada.get("rol"),
        "pareja": entrada.get("pareja"),
        "hito": entrada["hito"],
        "started_at": run["started_at"],
        "total_dias": total_dias,
        "total_turnos": total_turnos,
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
                    {"concepto": f["concepto_id"], "descripcion": f.get("descripcion"),
                     "form": f["form"],
                     "fijada_dia": f.get("fijada_dia"), "n_variantes": f.get("n_variantes")}
                    for f in fijadas
                ),
                key=lambda x: x["fijada_dia"] or 999,
            ),
        } if fijadas else None,
    }


def main():
    db = CurianaDB()
    runs = todas_las_filas(lambda: db.client.table("simulation_runs").select("*"))
    filas = []
    avisos: list[str] = []
    for entrada in MANIFIESTO:
        fila = resumir_run(db, entrada, runs=runs, avisos=avisos)
        if fila:
            filas.append(fila)
            conv = fila["convergencia"]
            conv_txt = (
                f"{conv['lectura']} {conv['delta_pct']:+}%" if conv else "sin métrica"
            )
            print(f"  ✓ {fila['id8']} · {fila['categoria']:11} · "
                  f"{fila['total_turnos']}T/{fila['total_dias']}d · "
                  f"caq {fila['pct_caquetio']} · {conv_txt}")

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

    if avisos:
        print(f"\n⚠  {len(avisos)} aviso(s): la fila de simulation_runs no coincide con lo "
              "medido. El índice lleva lo MEDIDO; lo que hay que revisar es el run:")
        for aviso in avisos:
            print(f"   - {aviso}")


if __name__ == "__main__":
    _forzar_utf8()
    main()
