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
                    "caribe-continental", "español-colonial",
                    "hipotético-no-verificado")

def normalize_source_language(fuente: str) -> str:
    """
    Convierte el campo 'fuente' del lexicón a una de las 12 categorías canónicas.

    caquetío / caquetío-atestiguado / caquetío/topónimo → "caquetío"
    caquetío-hipotético / caquetío-hipotético/topónimo  → "caquetío"
        (D10: la LENGUA no se discute, solo baja la confianza de la entrada —
         por eso comparte categoría con el resto del caquetío y no puntúa peor)
    wayunaiki / wayunaiki-cogn                          → "wayunaiki"
    paraujano / añú                                     → "paraujano"
        (D11 #39, 2026-08-31: el pariente costero más cercano abre columna
         propia — el lexicón tenía CERO entradas añú. Fuente: Wilbert
         1958-59 vía Oliver 1989, Tabla A-2; ver lexicon_a2.py)
    lokono / garifuna / lokono/garifuna                 → "lokono"
    taíno / taíno/caribe                                → "taíno"
    arahuaco / proto-arawakan / proto-arahuaco / ...    → "proto-arahuaco"
    kalinago-caribe-overlay                             → "kalinago-caribe-overlay"
    kalinago                                            → "kalinago"
    caribe-cháima / caribe-cumanagoto / caribe-tamanaco → "caribe-continental"
        (D10, 2026-08-03: caribe de TIERRA FIRME, el que Alvarado 1921 declara
         para piache, ture, pauji, watapana y auyama. Se separa del `kalinago`
         ya existente, que es el caribe INSULAR — de ahí el sufijo)
    español / español-colonial                          → "español-colonial"
        (D10: voces que la fuente declara castellanas frente a un nombre
         indígena distinto — kukuisa/cocuiza vs. caruata, caraota vs. icoroata.
         Necesitan categoría propia: si cayeran en el `return` por defecto se
         contarían como proto-arahuaco, es decir, como arahuacas)
    jirajaroide-contacto                                → "jirajaroide-contacto"
    hipotético-no-verificado                            → "hipotético-no-verificado"
        (transducción fonológica sin verificar cognación real contra COGNADOS;
         ver minar_pares_validacion.py — no cuenta como caquetío para scoring)
    """
    f = fuente.lower()
    if "no-verificado" in f or "no verificado" in f:
        return "hipotético-no-verificado"
    if "espanol" in f or "español" in f:
        return "español-colonial"
    if "caquetio" in f or "caquetío" in f:
        return "caquetío"
    if "wayunaiki" in f or "wayuu" in f:
        return "wayunaiki"
    if "paraujano" in f or "añú" in f or "añu" in f:
        return "paraujano"
    if "taino" in f or "taíno" in f:
        return "taíno"
    if "lokono" in f or "garifuna" in f:
        return "lokono"
    if "jirajaroide" in f:
        return "jirajaroide-contacto"
    # El overlay y el kalinago insular se resuelven ANTES que el caribe
    # continental: "kalinago-caribe-overlay" también contiene "caribe".
    if "kalinago-caribe-overlay" in f:
        return "kalinago-caribe-overlay"
    if "kalinago" in f:
        return "kalinago"
    if "caribe" in f:
        return "caribe-continental"
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
    """Categoría canónica de lengua de una palabra ya reconocida como arahuaca.

    Delega en `_familia_de_token()`, que **deshace prefijos posesivos y sufijos
    de aspecto** antes de buscar en el lexicón. Antes esto era un lookup pelado
    contra `VOCABULARIO_BASE`, y por eso toda forma flexionada se guardaba con
    `source_language = NULL`: `wana-ka`, `ta-barsure`, `naba-ni`…

    Medido sobre la base local (2026-08-06): **27.641 de 54.936 usos (50,3%)
    estaban sin lengua, y el 100% de ellos eran formas morfológicamente
    complejas** — o sea, justo los usos que prueban que los agentes manejan la
    morfología que el proyecto quiere modelar. El motor los reconocía para
    puntuar (`score_linguistico`) y los perdía al persistir.

    Solo se llama con tokens que `score_linguistico()` ya aceptó como arahuacos
    (`words_used` = `palabras_caquetias`), que es la precondición de
    `_familia_de_token`: para un neologismo comunitario devuelve "caquetío",
    que es lo correcto — es lengua propia, no préstamo.

    ⚠ Las formas ACUÑADAS en la propia respuesta (`coined_words`) NO pasan por
    aquí: todavía no están en el lexicón —el scorer no las ve, que es el
    agujero del 2026-09-16— y volverían NULL. `save_agent_response` les declara
    «caquetío» directamente.
    """
    from curiana_lexicon import _familia_de_token
    if not word:
        return None
    return _familia_de_token(word)


# ══════════════════════════════════════════════════════════════════════
# CLIENTE ANTHROPIC (con LangSmith si disponible)
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# LA ESCENA — dónde estaba cada agente
# ══════════════════════════════════════════════════════════════════════

# PostgREST corta en `max_rows`=1000 y una consulta sin `.range()` se trunca en
# SILENCIO (la trampa que ya se comió a `lexicon`, ~1400 palabras). `presencias`
# son 378 filas por día —63 agentes × 6 momentos—, así que una cadena de tres
# días ya pasa del corte. Todo lector de esta tabla pagina.
PAGINA_POSTGREST = 1000


def nodo_del_elenco_activo(agent_name: str) -> Optional[str]:
    """El nodo (GUARANAO / AMUAY) que el elenco ACTIVO le da a un agente.

    La importación va DENTRO a propósito: el elenco se decide antes de importar
    (`CURIANA_ELENCO=era2` hace que `curiana_agents` cargue
    `curiana_agents_era2`), y a este módulo lo importan scripts que no corren el
    motor. En la era 1 las fichas no tienen `nodo` y devuelve None — allí no hay
    escena.
    """
    try:
        from curiana_agents import ALL_AGENTS
    except Exception:                                        # noqa: BLE001
        return None
    return (ALL_AGENTS.get(agent_name) or {}).get("nodo")


def filas_de_presencias(
    run_id: str,
    turn_id: str,
    dia: int,
    turno: int,
    momento: str,
    escena: dict,
) -> list[dict]:
    """Las filas que una escena escribe en `presencias`, sin tocar la base.

    `escena` es `{agente: lugar}` — lo que `curiana_escena.escena_de(state)`
    devuelve. Un agente sin lugar no escribe fila: en la era 1 la escena está
    vacía y esta función devuelve `[]`, que es lo que hace que un run sin escena
    no escriba nada.

    Vive aquí fuera, y no dentro de `CurianaDB`, para que el mock construya
    EXACTAMENTE las mismas filas que la base: si se desincronizan, los tests
    dejan de decir nada de lo que se guarda de verdad.
    """
    return [
        {
            "run_id": run_id,
            "turn_id": turn_id,
            "day": dia,
            "turn_num": turno,
            "momento": momento,
            "agent_name": agente,
            "lugar": lugar,
            # El nodo se congela con la fila: el elenco es un módulo GENERADO
            # que se regenera, y `analizar_nodos` necesita saber de qué lado
            # estaba la gente el día del run, no hoy.
            "nodo": nodo_del_elenco_activo(agente),
        }
        for agente, lugar in sorted(escena.items())
        if lugar
    ]


def filas_de_loanword_uses(
    response_id: str,
    run_id: str,
    turn_id: str,
    agent_name: str,
    tier: int,
    day: int,
    turn_num: int,
    words: list,
) -> list[dict]:
    """Las filas que una respuesta escribe en `loanword_uses`, sin tocar la base.

    `words` es `score_linguistico()["prestamos_de_esfera"]`, que devuelve la
    clave CASTELLANA porque es la que el scorer reconoce. Aquí se normaliza
    («la etiqueta manda», Miguel 2026-09-18): `word` lleva la forma de la
    esfera —la indígena, cuando el lexicón la tiene con clave propia— y
    `forma_dicha`, lo que el agente escribió. Sin decisión para esa voz, las
    dos columnas coinciden.

    Vive aquí fuera, como `filas_de_presencias`, para que el mock construya
    EXACTAMENTE las mismas filas que la base.
    """
    from curiana_lexicon import forma_de_la_esfera
    filas = []
    for dicha in words or []:
        voz = forma_de_la_esfera(dicha)
        filas.append({
            "response_id": response_id,
            "run_id": run_id,
            "turn_id": turn_id,
            "word": voz,
            "forma_dicha": dicha,
            # La lengua es la de la voz de la esfera. Los cuatro pares de
            # `FORMA_DE_LA_ESFERA` comparten familia (las dos claves son
            # taínas), así que normalizar no mueve `source_language`; hay un
            # test que lo vigila.
            "source_language": word_source_language(voz),
            "agent_name": agent_name,
            "tier": tier,
            "day": day,
            "turn_num": turn_num,
        })
    return filas


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
            # dict directo → jsonb OBJETO consultable con config->>'clave'.
            # (json.dumps lo guardaba como string JSON, inconsultable en SQL.)
            "config": config or {},
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
        coined_words: Optional[list[str]] = None,
        lugar: Optional[str] = None,
    ) -> str:
        """
        Guarda la respuesta de un agente con análisis lingüístico completo.
        Calcula automáticamente la composición por lengua.
        Retorna response_id.

        `lugar` — dónde estaba el agente cuando dijo esto (escena, capa 1). Va
        desnormalizado al lado de la respuesta a propósito (decisión de Miguel
        2026-09-17, §2 capa 1 «las dos»): `presencias` sabe de los 63, pero toda
        consulta de lengua sale de `word_uses` × `turns` × `agent_responses` y
        no tiene por qué unir además con una cuarta tabla. Sin escena —la era 1,
        o un run con `--sin-escena`— la columna ni se menciona en el insert: la
        fila queda idéntica a la de antes de esta migración.

        `coined_words` — las formas que esta respuesta ACUÑA. Se suman a
        `words_used` y escriben su fila en `word_uses` con
        `source_language='caquetío'`. Van aparte porque no vienen del scorer:
        `score_linguistico()` sólo reconoce `lexico.palabras_activas()` (base +
        adoptados) y una acuñación recién propuesta no está ahí, así que el
        acuñador no quedaba registrado como usuario de su propia forma y el
        primer uso que constaba era el del ADOPTANTE — 29 de 40 acuñaciones de
        la era 2 (medido el 2026-09-16). `neologisms.proposed_by` sí lo sabía;
        `word_uses`, que es de donde se leen las rutas de contagio, no.

        Su lengua se declara «caquetío» en vez de resolverla: una acuñación
        pasó la compuerta fonotáctica, no está en el lexicón y
        `word_source_language()` la dejaría en NULL — que es justo el agujero
        que el backfill de 2026-08-06 cerró para las formas flexionadas.
        Los `pct_*` NO se mueven: `language_composition()` sólo cuenta lo que
        está en VOCABULARIO_BASE, y una acuñación por definición no lo está.
        """
        # Sin repetir: una respuesta que acuña dos veces la misma forma —o que
        # acuña una que el scorer ya contó— escribe UNA fila, no dos.
        acunadas = [w for w in dict.fromkeys(coined_words or [])
                    if w and w not in words_used]
        comp = language_composition(words_used)
        words_used = list(words_used) + acunadas

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
        if lugar:
            row["lugar"] = lugar
        result = self.client.table("agent_responses").insert(row).execute()
        response_id: str = result.data[0]["id"]

        # Insertar word_uses granulares
        if words_used:
            acunadas_set = set(acunadas)
            wu_rows = [
                {
                    "response_id": response_id,
                    "run_id": run_id,
                    "turn_id": turn_id,
                    "word": w,
                    "source_language": ("caquetío" if w in acunadas_set
                                        else word_source_language(w)),
                    "agent_name": agent_name,
                    "day": None,   # se rellena con join en la vista
                    "turn_num": None,
                }
                for w in words_used
            ]
            self.client.table("word_uses").insert(wu_rows).execute()

        return response_id

    def save_loanword_uses(
        self,
        response_id: str,
        run_id: str,
        turn_id: str,
        agent_name: str,
        tier: int,
        day: int,
        turn_num: int,
        words: list[str],
    ) -> int:
        """Guarda las voces de la ESFERA DE CONTACTO que usó una respuesta
        (`score_linguistico()["prestamos_de_esfera"]`) en `loanword_uses`, con
        su lengua real. Retorna cuántas filas escribió.

        Tabla aparte, y no `word_uses`, a propósito (2026-09-16, run c6837386):
        `word_uses` es la huella de `palabras_caquetias`, que desde el
        2026-09-09 significa SÓLO caquetío, y ninguno de sus lectores
        (`analizar_runs.py`, la vista `top_words_by_agent`) filtra por lengua.
        Y `words_used` alimenta `language_composition()` → `pct_*`: meter ahí
        el préstamo movería `pct_caquetio` a mitad de serie. La decisión de
        Miguel (2026-09-15, §p3b) es literal: «se debe medir aparte». A
        diferencia de `word_uses`, aquí `tier`, `day` y `turn_num` van
        puestos: la pregunta que responde la tabla es si la voz baja del
        tier 1 —el único que ve [Voces de fuera]— al 2 y al 3, y cuándo.

        ⚠ 2026-09-18, «la etiqueta manda»: `word` guarda la FORMA DE LA ESFERA
        —la indígena, si el lexicón la tiene— y `forma_dicha` lo que el agente
        escribió de verdad. Se normaliza AQUÍ, al guardar, y no en el scorer:
        `score_linguistico()` sigue devolviendo la clave castellana, que es la
        que reconoce. Las dos columnas dicen cosas distintas y las dos hacen
        falta: `word` para agrupar la voz (`casabe` y `cazabi` son la misma) y
        `forma_dicha` para no perder que el agente dijo «casabe». Los runs
        viejos NO se reescriben: allí `forma_dicha` queda NULL y `word` lleva
        la grafía de entonces; `analizar_runs.py --prestamos` normaliza al
        leer. Ver `curiana_lexicon.FORMA_DE_LA_ESFERA` y
        6-fusion/descastellanizar_esfera_2026-09-18.yaml.
        """
        rows = filas_de_loanword_uses(response_id, run_id, turn_id, agent_name,
                                      tier, day, turn_num, words)
        if not rows:
            return 0
        self.client.table("loanword_uses").insert(rows).execute()
        return len(rows)

    # ── Presencias: la escena del turno ───────────────────────────────

    def save_presencias(
        self,
        run_id: str,
        turn_id: str,
        dia: int,
        turno: int,
        momento: str,
        escena: dict,
    ) -> int:
        """Guarda dónde estaba CADA agente este turno. Retorna cuántas filas
        escribió.

        `escena` es `{agente: lugar}`, lo que devuelve
        `curiana_escena.escena_de(state)`. Son los 63, no los 12 que hablan
        (decisión de Miguel 2026-09-17): el visor de repetición (§5b) lee de
        aquí y «un mapa con 12 de 63 no es un mundo».

        **Una inserción por lote, no 63 llamadas.** Un día son 6 turnos × 63 =
        378 filas; a llamada por agente serían 378 viajes a PostgREST por día.

        Como `save_loanword_uses`, esta función NO atrapa sus fallos: los
        propaga para que el llamador los cuente en su `Counter` por tabla
        (`db_fallos["presencias"] += 1` en `curiana_orchestrator_v2`). Perder
        escrituras en silencio corrompe el análisis, y la escena es justo la
        tabla donde un agujero no se nota: 62 presencias en vez de 63 siguen
        pareciendo un mundo.

        Un run sin escena (la era 1, o `--sin-escena`) pasa `{}` y esto no
        escribe nada ni viaja a la base.
        """
        filas = filas_de_presencias(run_id, turn_id, dia, turno, momento, escena)
        if not filas:
            return 0
        self.client.table("presencias").insert(filas).execute()
        return len(filas)

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

    def save_koine_metric(self, run_id: str, day: int, distance: float, n_agents: int,
                          distance_ventana: Optional[float] = None,
                          distance_emergente: Optional[float] = None):
        """Persiste la distancia idiolectal media de un día (métrica de
        convergencia). Upsert por (run_id, day) para ser idempotente.

        distance = acumulada (histórica); distance_ventana = sobre los últimos
        turnos de habla real; distance_emergente = ventana sin vocabulario base
        (solo formas emergentes — la señal de koineización menos sesgada).
        Si el esquema no tiene las columnas nuevas (sin migración), reintenta
        con las básicas para no perder la métrica principal."""
        row = {"run_id": run_id, "day": day, "distance": distance, "n_agents": n_agents,
               "distance_ventana": distance_ventana,
               "distance_emergente": distance_emergente}
        try:
            self.client.table("koine_metrics").upsert(
                row, on_conflict="run_id,day").execute()
        except Exception:
            self.client.table("koine_metrics").upsert(
                {"run_id": run_id, "day": day, "distance": distance,
                 "n_agents": n_agents},
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

    def get_run(self, run_id: str) -> Optional[dict]:
        """Un run por id. Lo usa `curiana_cadena` para subir por
        `config->continuado_desde` hasta la raíz de la cadena."""
        result = (
            self.client.table("simulation_runs")
            .select("*")
            .eq("id", run_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def runs_encadenados(self) -> list[dict]:
        """id + started_at + config de todos los runs, para descubrir las
        cadenas (`curiana_cadena.cadenas_en_la_base`). Son decenas de filas, muy
        por debajo del `max_rows`=1000 de PostgREST que trunca al `lexicon`."""
        result = (
            self.client.table("simulation_runs")
            .select("id, started_at, ended_at, total_turns, config")
            .order("started_at")
            .execute()
        )
        return result.data or []

    def _presencias(self, run_ids: list[str]) -> list[dict]:
        """La escena de uno o varios runs, paginada.

        Pagina porque tiene que hacerlo: 378 filas por día contra el
        `max_rows`=1000 de PostgREST, que trunca **en silencio** una consulta
        sin `.range()` — es la trampa que ya se comió a `lexicon`. Una cadena de
        tres días son 1.134 filas y sin esto se leerían 1.000.
        """
        if not run_ids:
            return []
        filas: list[dict] = []
        desde = 0
        while True:
            result = (
                self.client.table("presencias")
                .select("run_id, turn_id, day, turn_num, momento, "
                        "agent_name, lugar, nodo")
                .in_("run_id", list(run_ids))
                .order("day").order("turn_num").order("agent_name")
                .range(desde, desde + PAGINA_POSTGREST - 1)
                .execute()
            )
            lote = result.data or []
            filas.extend(lote)
            if len(lote) < PAGINA_POSTGREST:
                return filas
            desde += PAGINA_POSTGREST

    def presencias_de(self, run_id: str) -> list[dict]:
        """La escena de un run: quién estuvo dónde, turno a turno."""
        return self._presencias([run_id])

    def presencias_de_cadena(self, run_ids: list[str]) -> list[dict]:
        """La escena de una CADENA entera. En la era 2 un run es UN día, así que
        la unidad que se mira casi siempre es la cadena, no el run: los ids
        salen de subir por `config.continuado_desde` (`runs_encadenados` →
        `curiana_cadena.cadena_de_runs`)."""
        return self._presencias(list(run_ids))

    def koine_metrics(self, run_id: str) -> list[dict]:
        """Las métricas de koiné de un run, por día."""
        result = (
            self.client.table("koine_metrics")
            .select("day, distance, distance_ventana, distance_emergente, n_agents")
            .eq("run_id", run_id)
            .order("day")
            .execute()
        )
        return result.data or []

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

    # ── Libro de costos ───────────────────────────────────────────────

    def save_llm_calls(self, run_id: str, filas: list[dict]) -> int:
        """Vuelca las llamadas de un turno a `llm_calls` (ver curiana_costos.py).
        Una fila por llamada al modelo; retorna cuántas escribió."""
        if not filas:
            return 0
        rows = [{"run_id": run_id, **f} for f in filas]
        self.client.table("llm_calls").insert(rows).execute()
        return len(rows)


# ══════════════════════════════════════════════════════════════════════
# MODO DEGRADADO (sin Supabase)
# ══════════════════════════════════════════════════════════════════════

class CurianaDBMock:
    """
    Drop-in replacement cuando Supabase no está configurado.
    Todos los métodos son no-ops que no rompen la simulación.

    Con dos excepciones declaradas: la ESCENA y los PRÉSTAMOS DE ESFERA sí se
    guardan, en memoria. Sin base no habría cómo afirmar en un test que se
    escriben 63 presencias por turno y 378 por día, ni que un run sin escena no
    escribe nada, ni que `word` lleva la forma de la esfera y `forma_dicha` lo
    que el agente escribió (2026-09-18) — y ésas son exactamente las garantías
    que esas dos capas necesitan. Las filas se construyen con
    `filas_de_presencias` y `filas_de_loanword_uses`, las MISMAS funciones que
    usa `CurianaDB`, para que el mock no pueda divergir de lo que se guarda de
    verdad.
    """
    def __init__(self):
        self.presencias: list[dict] = []
        self.respuestas: list[dict] = []
        self.loanwords: list[dict] = []

    def seed_lexicon(self, **kw): return 0
    def create_run(self, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def end_run(self, *a, **kw): pass
    def save_turn(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def save_agent_response(self, *a, **kw) -> str:
        import uuid
        response_id = str(uuid.uuid4())
        self.respuestas.append({
            "response_id": response_id,
            "run_id": kw.get("run_id"),
            "turn_id": kw.get("turn_id"),
            "agent_name": kw.get("agent_name"),
            "lugar": kw.get("lugar"),
        })
        return response_id
    def save_loanword_uses(self, response_id: str = "", run_id: str = "",
                           turn_id: str = "", agent_name: str = "", tier: int = 0,
                           day: int = 0, turn_num: int = 0,
                           words: list | None = None) -> int:
        # Mismas filas que `CurianaDB`, misma función: si el mock divergiera,
        # los tests dejarían de decir nada de lo que se guarda de verdad.
        filas = filas_de_loanword_uses(response_id, run_id, turn_id, agent_name,
                                       tier, day, turn_num, words or [])
        self.loanwords.extend(filas)
        return len(filas)

    def save_presencias(self, run_id: str, turn_id: str, dia: int, turno: int,
                        momento: str, escena: dict) -> int:
        filas = filas_de_presencias(run_id, turn_id, dia, turno, momento, escena)
        self.presencias.extend(filas)
        return len(filas)

    def presencias_de(self, run_id: str) -> list[dict]:
        return [f for f in self.presencias if f["run_id"] == run_id]

    def presencias_de_cadena(self, run_ids: list[str]) -> list[dict]:
        ids = set(run_ids)
        return [f for f in self.presencias if f["run_id"] in ids]
    def save_neologism(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def update_neologism_status(self, *a, **kw): pass
    def save_koine_metric(self, *a, **kw): pass
    def save_koine_lexicon(self, *a, **kw): pass
    def save_phrase_etymology(self, *a, **kw): pass
    def latest_run(self): return None
    # Sin base no hay cadena: el orquestador imprime la serie del run y ya.
    def get_run(self, *a, **kw): return None
    def runs_encadenados(self, *a, **kw): return []
    def koine_metrics(self, *a, **kw): return []
    def language_drift(self, *a): return []
    def adopted_neologisms(self, *a): return []
    def get_agent_responses(self, *a, **kw): return []
    def save_agent_profile(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def clear_agent_quotes(self, *a, **kw): pass
    def save_agent_quote(self, *a, **kw) -> str:
        import uuid; return str(uuid.uuid4())
    def save_llm_calls(self, *a, **kw) -> int: return 0


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
        test_words = ["taya", "barsure", "arima", "hamaka", "duna", "wana", "ka", "mara"]
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
