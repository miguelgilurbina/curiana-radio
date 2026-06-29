"""
CURIANA — Capa de Base de Datos
================================
Supabase (PostgreSQL) + LangSmith tracing.

Uso:
    from curiana_database import CurianaDB, get_anthropic_client

    db = CurianaDB()          # conecta a Supabase
    client = get_anthropic_client()  # Anthropic + LangSmith wrapper

Variables de entorno necesarias:
    ANTHROPIC_API_KEY    — siempre requerida
    SUPABASE_URL         — URL del proyecto Supabase
    SUPABASE_SERVICE_KEY — service_role key (bypassa RLS para escritura)
    LANGSMITH_API_KEY    — opcional, activa tracing automático
    LANGSMITH_PROJECT    — nombre del proyecto en LangSmith (default: curiana)
"""

import os
import json
from typing import Optional
from datetime import datetime, timezone

# Carga curiana_sim/.env para que las credenciales (Supabase, Anthropic,
# LangSmith) estén disponibles al invocar este módulo directamente
# (p.ej. `python curiana_database.py seed`), no solo vía el orquestador.
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

import anthropic

# ── Supabase ──────────────────────────────────────────────────────────
try:
    from supabase import create_client, Client as SupabaseClient
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠  supabase-py no instalado. Ejecuta: pip install supabase")

# ── LangSmith ─────────────────────────────────────────────────────────
try:
    from langsmith.wrappers import wrap_anthropic
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    print("⚠  langsmith no instalado. Ejecuta: pip install langsmith")


# ══════════════════════════════════════════════════════════════════════
# NORMALIZACIÓN DE LENGUA FUENTE
# ══════════════════════════════════════════════════════════════════════

# Mapeo de los valores de "fuente" en VOCABULARIO_BASE a 5 categorías canónicas.
# Estas mismas categorías se usan en las columnas pct_* de agent_responses.
LANG_CATEGORIES = ("caquetío", "wayunaiki", "lokono", "taíno", "proto-arahuaco",
                    "kalinago", "kalinago-caribe-overlay", "jirajaroide-contacto",
                    "hipotético-no-verificado")

def normalize_source_language(fuente: str) -> str:
    """
    Convierte el campo 'fuente' del lexicón a una de las 9 categorías canónicas.

    caquetío / caquetío-atestiguado / caquetío/topónimo → "caquetío"
    wayunaiki / wayunaiki-cogn                          → "wayunaiki"
    lokono / garifuna / lokono/garifuna                 → "lokono"
    taíno / taíno/caribe                                → "taíno"
    arahuaco / proto-arawakan / proto-arahuaco / ...    → "proto-arahuaco"
    kalinago-caribe-overlay                             → "kalinago-caribe-overlay"
    kalinago                                            → "kalinago"
    jirajaroide-contacto                                → "jirajaroide-contacto"
    hipotético-no-verificado                            → "hipotético-no-verificado"
        (transducción fonológica sin verificar cognación real contra COGNADOS;
         ver minar_pares_validacion.py — no cuenta como caquetío para scoring)
    """
    f = fuente.lower()
    if "no-verificado" in f or "no verificado" in f:
        return "hipotético-no-verificado"
    if "caquetio" in f or "caquetío" in f:
        return "caquetío"
    if "wayunaiki" in f or "wayuu" in f:
        return "wayunaiki"
    if "taino" in f or "taíno" in f:
        return "taíno"
    if "lokono" in f or "garifuna" in f:
        return "lokono"
    if "jirajaroide" in f:
        return "jirajaroide-contacto"
    if "kalinago-caribe-overlay" in f:
        return "kalinago-caribe-overlay"
    if "kalinago" in f:
        return "kalinago"
    # proto-arawakan, proto-arahuaco, reconstructed
    return "proto-arahuaco"


def language_composition(words_used: list[str]) -> dict[str, float]:
    """
    Dado el listado de palabras caquetías usadas en una respuesta,
    devuelve la composición por lengua fuente como proporciones (suman 1.0).

    Ejemplo:
        {"caquetío": 0.42, "wayunaiki": 0.33, "lokono": 0.15,
         "taíno": 0.06, "proto-arahuaco": 0.04}
    """
    from curiana_lexicon import VOCABULARIO_BASE

    counts: dict[str, int] = {lang: 0 for lang in LANG_CATEGORIES}
    for word in words_used:
        if word in VOCABULARIO_BASE:
            lang = normalize_source_language(VOCABULARIO_BASE[word]["fuente"])
            counts[lang] = counts.get(lang, 0) + 1

    total = sum(counts.values()) or 1
    return {lang: round(counts[lang] / total, 4) for lang in LANG_CATEGORIES}


def word_source_language(word: str) -> Optional[str]:
    """Devuelve la categoría canónica de lengua para una palabra individual."""
    from curiana_lexicon import VOCABULARIO_BASE
    if word in VOCABULARIO_BASE:
        return normalize_source_language(VOCABULARIO_BASE[word]["fuente"])
    return None


# ══════════════════════════════════════════════════════════════════════
# CLIENTE ANTHROPIC (con LangSmith si disponible)
# ══════════════════════════════════════════════════════════════════════

def get_anthropic_client(run_id: Optional[str] = None) -> anthropic.Anthropic:
    """
    Devuelve un cliente Anthropic.
    Si LANGSMITH_API_KEY está en el entorno, lo wrappea automáticamente
    para registrar todas las llamadas en LangSmith.

    El run_id de la simulación se usa como nombre del proyecto LangSmith
    para poder filtrar todas las trazas de un run específico.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("Falta ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(api_key=api_key)

    ls_key = os.environ.get("LANGSMITH_API_KEY", "")
    if ls_key and LANGSMITH_AVAILABLE:
        # Nombre del proyecto: "curiana-{run_id[:8]}" para filtrar por run
        project = os.environ.get(
            "LANGSMITH_PROJECT",
            f"curiana-{run_id[:8]}" if run_id else "curiana"
        )
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = ls_key
        os.environ["LANGCHAIN_PROJECT"] = project
        client = wrap_anthropic(client)
        print(f"  ✓ LangSmith activo → proyecto: {project}")
    else:
        if not ls_key:
            print("  ℹ  LangSmith desactivado (sin LANGSMITH_API_KEY)")

    return client


# ══════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL: CurianaDB
# ══════════════════════════════════════════════════════════════════════

class CurianaDB:
    """
    Interfaz de alto nivel para todas las operaciones de base de datos.
    Usa la service_role key para bypasear RLS (escritura desde el backend Python).
    """

    def __init__(self):
        if not SUPABASE_AVAILABLE:
            raise RuntimeError("supabase-py no disponible. pip install supabase")

        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_SERVICE_KEY", "")

        if not url or not key:
            raise ValueError(
                "Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY.\n"
                "Agrégalos a tu .env o exporta las variables antes de correr."
            )

        self.client: SupabaseClient = create_client(url, key)
        self._run_id: Optional[str] = None
        print("  ✓ Supabase conectado")

    # ── Seed del léxico ───────────────────────────────────────────────

    def seed_lexicon(self, overwrite: bool = False) -> int:
        """
        Inserta todas las entradas de VOCABULARIO_BASE en la tabla lexicon.
        Si overwrite=False, usa upsert con conflict en 'word' (no duplica).
        Retorna cuántas filas se insertaron/actualizaron.
        """
        from curiana_lexicon import VOCABULARIO_BASE

        rows = []
        for word, data in VOCABULARIO_BASE.items():
            fuente = data.get("fuente", "desconocido")
            rows.append({
                "word": word,
                # Tras la canonicalización en curiana_lexicon, "sig" y "cat"
                # están siempre presentes. "categoria" es el dominio semántico
                # opcional (eje distinto a "cat", la categoría gramatical).
                "meaning": data.get("sig", ""),
                "category": data.get("cat", ""),
                "semantic_domain": data.get("categoria"),
                "source_language": normalize_source_language(fuente),
                "attested": "atestiguado" in fuente or fuente == "caquetío-atestiguado",
                "source_ref": fuente,
            })

        result = (
            self.client.table("lexicon")
            .upsert(rows, on_conflict="word")
            .execute()
        )
        count = len(result.data) if result.data else 0
        print(f"  ✓ Léxico sembrado: {count} palabras en Supabase")
        return count

    # ── Simulation run ────────────────────────────────────────────────

    def create_run(self, model: str = "claude-haiku-4-5-20251001",
                   config: Optional[dict] = None) -> str:
        """Crea un nuevo simulation run y retorna su UUID."""
        row = {
            "model": model,
            "config": json.dumps(config or {}),
        }
        result = self.client.table("simulation_runs").insert(row).execute()
        run_id: str = result.data[0]["id"]
        self._run_id = run_id
        print(f"  ✓ Run creado: {run_id[:8]}...")

        # Actualizar el proyecto LangSmith con el run_id real
        ls_project = f"curiana-{run_id[:8]}"
        os.environ["LANGCHAIN_PROJECT"] = ls_project
        result2 = (
            self.client.table("simulation_runs")
            .update({"langsmith_project": ls_project})
            .eq("id", run_id)
            .execute()
        )

        return run_id

    def end_run(self, run_id: str, total_turns: int, total_days: int):
        """Marca el run como terminado."""
        self.client.table("simulation_runs").update({
            "ended_at": datetime.now(timezone.utc).isoformat(),
            "total_turns": total_turns,
            "total_days": total_days,
        }).eq("id", run_id).execute()

    # ── Turns ─────────────────────────────────────────────────────────

    def save_turn(
        self,
        run_id: str,
        day: int,
        turn_num: int,
        moment: str,
        season: str,
        event_description: Optional[str] = None,
    ) -> str:
        """Crea un registro de turno. Retorna turn_id."""
        row = {
            "run_id": run_id,
            "day": day,
            "turn_num": turn_num,
            "moment": moment,
            "season": season,
            "event_description": event_description,
        }
        result = self.client.table("turns").insert(row).execute()
        return result.data[0]["id"]

    # ── Agent responses ───────────────────────────────────────────────

    def save_agent_response(
        self,
        turn_id: str,
        run_id: str,
        agent_name: str,
        ethnicity: str,
        tier: int,
        response_text: str,
        score: float,
        words_used: list[str],
        aspects_used: list[str],
        neologisms_proposed: int = 0,
        langsmith_trace_url: Optional[str] = None,
    ) -> str:
        """
        Guarda la respuesta de un agente con análisis lingüístico completo.
        Calcula automáticamente la composición por lengua.
        Retorna response_id.
        """
        comp = language_composition(words_used)

        row = {
            "turn_id": turn_id,
            "run_id": run_id,
            "agent_name": agent_name,
            "ethnicity": ethnicity,
            "tier": tier,
            "response_text": response_text,
            "score": score,
            "pct_caquetio":   comp.get("caquetío",   0.0),
            "pct_wayunaiki":  comp.get("wayunaiki",  0.0),
            "pct_lokono":     comp.get("lokono",      0.0),
            "pct_taino":      comp.get("taíno",       0.0),
            "pct_proto_arahuaco": comp.get("proto-arahuaco", 0.0),
            "aspects_used":   aspects_used,
            "words_used":     words_used,
            "neologisms_proposed": neologisms_proposed,
            "langsmith_trace_url": langsmith_trace_url,
        }
        result = self.client.table("agent_responses").insert(row).execute()
        response_id: str = result.data[0]["id"]

        # Insertar word_uses granulares
        if words_used:
            wu_rows = [
                {
                    "response_id": response_id,
                    "run_id": run_id,
                    "turn_id": turn_id,
                    "word": w,
                    "source_language": word_source_language(w),
                    "agent_name": agent_name,
                    "day": None,   # se rellena con join en la vista
                    "turn_num": None,
                }
                for w in words_used
            ]
            self.client.table("word_uses").insert(wu_rows).execute()

        return response_id

    # ── Neologisms ────────────────────────────────────────────────────

    def save_neologism(
        self,
        run_id: str,
        turn_id: str,
        proposed_by: str,
        proposed_day: int,
        form: str,
        components: str,
        meaning: str,
        morphological_rule: str = "desconocida",
    ) -> str:
        """Registra una nueva palabra propuesta. Retorna su id."""
        row = {
            "run_id": run_id,
            "proposed_turn_id": turn_id,
            "proposed_by": proposed_by,
            "proposed_day": proposed_day,
            "form": form,
            "components": components,
            "meaning": meaning,
            "morphological_rule": morphological_rule,
            "status": "propuesto",
        }
        result = self.client.table("neologisms").insert(row).execute()
        return result.data[0]["id"]

    def update_neologism_status(
        self,
        form: str,
        run_id: str,
        status: str,                           # adoptado | rechazado | ignorado
        adopted_by: Optional[list[str]] = None,
        adopted_turn_id: Optional[str] = None,
    ):
        """Actualiza el estado de una palabra propuesta."""
        update = {"status": status}
        if adopted_by:
            update["adopted_by"] = adopted_by
        if adopted_turn_id:
            update["adopted_turn_id"] = adopted_turn_id

        self.client.table("neologisms").update(update).eq(
            "form", form
        ).eq("run_id", run_id).execute()

    # ── Koiné metrics ─────────────────────────────────────────────────

    def save_koine_metric(self, run_id: str, day: int, distance: float, n_agents: int):
        """Persiste la distancia idiolectal media de un día (métrica de
        convergencia). Upsert por (run_id, day) para ser idempotente."""
        self.client.table("koine_metrics").upsert(
            {"run_id": run_id, "day": day, "distance": distance, "n_agents": n_agents},
            on_conflict="run_id,day",
        ).execute()

    def save_koine_lexicon(self, run_id: str, concepto_id: str, descripcion: str,
                           form: str, fijada_dia: int,
                           soporte: Optional[float] = None, n_variantes: Optional[int] = None):
        """Persiste una entrada del diccionario koiné (forma fijada por
        competencia para un referente nuevo). Upsert por (run_id, concepto_id)."""
        self.client.table("koine_lexicon").upsert(
            {"run_id": run_id, "concepto_id": concepto_id, "descripcion": descripcion,
             "form": form, "fijada_dia": fijada_dia, "soporte": soporte,
             "n_variantes": n_variantes},
            on_conflict="run_id,concepto_id",
        ).execute()

    # ── Phrase etymologies ────────────────────────────────────────────

    def save_phrase_etymology(
        self,
        response_id: str,
        phrase: str,
        word_breakdown: list[dict],            # [{word, source_language, meaning, is_neologism}]
        lang_composition: dict,
        etymological_note: Optional[str] = None,
        is_notable: bool = False,
    ):
        """Guarda un análisis etimológico detallado de una frase."""
        row = {
            "response_id": response_id,
            "phrase": phrase,
            "word_breakdown": json.dumps(word_breakdown),
            "lang_composition": json.dumps(lang_composition),
            "etymological_note": etymological_note,
            "curated_by": "auto",
            "is_notable": is_notable,
        }
        self.client.table("phrase_etymologies").insert(row).execute()

    # ── Queries de utilidad ───────────────────────────────────────────

    def latest_run(self) -> Optional[dict]:
        """Devuelve el run más reciente."""
        result = (
            self.client.table("simulation_runs")
            .select("*")
            .order("started_at", desc=True)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def language_drift(self, run_id: str) -> list[dict]:
        """
        Retorna la vista language_drift_by_turn para un run.
        Útil para el chart principal del dashboard.
        """
        result = (
            self.client.table("language_drift_by_turn")
            .select("*")
            .eq("run_id", run_id)
            .order("day")
            .execute()
        )
        return result.data or []

    def adopted_neologisms(self, run_id: str) -> list[dict]:
        result = (
            self.client.table("neologisms")
            .select("*")
            .eq("run_id", run_id)
            .eq("status", "adoptado")
            .order("proposed_day")
            .execute()
        )
        return result.data or []

    # ── Perfiles de agentes ───────────────────────────────────────────

    def get_agent_responses(self, run_id: str, agent_name: str) -> list[dict]:
        """Todas las respuestas de un agente en un run, ordenadas cronológicamente."""
        result = (
            self.client.table("agent_responses")
            .select("id, response_text, score, words_used, neologisms_proposed, turn_id")
            .eq("run_id", run_id)
            .eq("agent_name", agent_name)
            .order("created_at")
            .execute()
        )
        return result.data or []

    def save_agent_profile(
        self,
        run_id: str,
        agent_name: str,
        tier: int,
        rol_comunidad: str,
        resumen_arco: str,
        total_respuestas: int,
        avg_score: Optional[float],
        neologismos_propuestos: int,
        neologismos_adoptados: int,
    ) -> str:
        """Crea o actualiza el perfil narrativo de un agente para un run. Retorna profile_id."""
        row = {
            "run_id": run_id,
            "agent_name": agent_name,
            "tier": tier,
            "rol_comunidad": rol_comunidad,
            "resumen_arco": resumen_arco,
            "total_respuestas": total_respuestas,
            "avg_score": avg_score,
            "neologismos_propuestos": neologismos_propuestos,
            "neologismos_adoptados": neologismos_adoptados,
        }
        result = (
            self.client.table("agent_profiles")
            .upsert(row, on_conflict="run_id,agent_name")
            .execute()
        )
        return result.data[0]["id"]

    def clear_agent_quotes(self, profile_id: str):
        """Borra las frases previas de un perfil antes de regenerarlas."""
        self.client.table("agent_quotes").delete().eq("profile_id", profile_id).execute()

    def save_agent_quote(
        self,
        profile_id: str,
        run_id: str,
        agent_name: str,
        quote: str,
        justificacion: str,
        impacto_score: float,
        translation: Optional[str] = None,
        response_id: Optional[str] = None,
        day: Optional[int] = None,
        turn_num: Optional[int] = None,
    ) -> str:
        """Guarda una frase célebre curada por el agente analista."""
        row = {
            "profile_id": profile_id,
            "run_id": run_id,
            "agent_name": agent_name,
            "quote": quote,
            "justificacion": justificacion,
            "impacto_score": impacto_score,
            "translation": translation,
            "response_id": response_id,
            "day": day,
            "turn_num": turn_num,
        }
        result = self.client.table("agent_quotes").insert(row).execute()
        return result.data[0]["id"]


# ══════════════════════════════════════════════════════════════════════
# MODO DEGRADADO (sin Supabase)
# ══════════════════════════════════════════════════════════════════════

class CurianaDBMock:
    """
    Drop-in replacement cuando Supabase no está configurado.
    Todos los métodos son no-ops que no rompen la simulación.
    """
    def seed_lexicon(self, **kw): return 0
    def create_run(self, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def end_run(self, *a, **kw): pass
    def save_turn(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def save_agent_response(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def save_neologism(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def update_neologism_status(self, *a, **kw): pass
    def save_koine_metric(self, *a, **kw): pass
    def save_koine_lexicon(self, *a, **kw): pass
    def save_phrase_etymology(self, *a, **kw): pass
    def latest_run(self): return None
    def language_drift(self, *a): return []
    def adopted_neologisms(self, *a): return []
    def get_agent_responses(self, *a, **kw): return []
    def save_agent_profile(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def clear_agent_quotes(self, *a, **kw): pass
    def save_agent_quote(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())


def get_db() -> "CurianaDB | CurianaDBMock":
    """
    Factory: devuelve CurianaDB si Supabase está configurado,
    CurianaDBMock si no (la simulación sigue funcionando sin DB).
    """
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if url and key and SUPABASE_AVAILABLE:
        try:
            return CurianaDB()
        except Exception as e:
            print(f"  ⚠  Supabase no disponible ({e}). Corriendo sin DB.")
    else:
        print("  ℹ  Sin Supabase configurado. Corriendo en modo local (JSON).")
    return CurianaDBMock()


# ══════════════════════════════════════════════════════════════════════
# CLI de utilidad
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"

    if cmd == "seed":
        db = CurianaDB()
        db.seed_lexicon()
        print("Léxico sembrado en Supabase.")

    elif cmd == "test":
        print("── Test de composición de lengua ──")
        test_words = ["taya", "barsure", "arima", "hamaca", "duna", "wana", "ka", "mara"]
        comp = language_composition(test_words)
        for lang, pct in comp.items():
            bar = "█" * int(pct * 20)
            print(f"  {lang:12} {bar:<20} {pct:.1%}")

    elif cmd == "check":
        db = get_db()
        run = db.latest_run()
        if run:
            print(f"Último run: {run['id'][:8]}... ({run['started_at']})")
        else:
            print("Sin runs registrados.")
