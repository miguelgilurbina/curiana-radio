"""
CURIANA — Orquestador v2: Motor de Emergencia Lingüística
==========================================================
Versión refactorizada con lexicon engine, observer lingüístico,
reportes periódicos y simulación de largo plazo (días/meses/años).

Uso:
    python curiana_orchestrator_v2.py                     # interactivo
    python curiana_orchestrator_v2.py --auto 10           # 10 turnos
    python curiana_orchestrator_v2.py --auto 60 --anio    # 1 año simulado (60 dias = 120 turnos)
    python curiana_orchestrator_v2.py --auto 240 --reporte # 4 años simulados con reporte anual LLM
"""

import os
import sys
import json
import random
import argparse
from typing import Optional

import anthropic

# Cargar variables de entorno desde curiana_sim/.env (Supabase + Anthropic)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

from curiana_database import get_anthropic_client, get_db
from curiana_agents import ALL_AGENTS, AGENTS_T1, AGENTS_T2, AGENTS_T3
from curiana_state import (
    ComunidadState,
    estado_inicial_test,
    EVENTOS_COTIDIANOS,
    EVENTOS_ESTACIONALES,
    MOMENTOS_DIA,
    LOCACIONES,
)
from curiana_lexicon import (
    LexicoComunitario,
    vocabulario_para_agente,
    prompt_lexico_activo,
    score_linguistico,
    prompt_rescate_linguistico,
    VOCABULARIO_BASE,
)
from curiana_observer import ObserverAgent
from curiana_social import (
    DifusionLexica,
    prompt_rasgos_dialectales,
)


# ══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_AGENT = 500      # Espacio para frases en caquetío + glosa + neologismos
MAX_TOKENS_DIRECTOR = 600

# Constante de identidad lingüística — inyectada en TODOS los agentes
# Este es el pivot central: cambia "español con interferencia caquetía"
# a "caquetío como lengua materna, español como glosa opcional"
_IDENTIDAD_LINGUISTICA = """[TU LENGUA MATERNA ES EL CAQUETÍO]:
Piensas y sientes en caquetío-arahuaco. El español es una lengua forastera.
HABLA EN CAQUETÍO: pronombre + verbo-aspecto + complemento caquetío.
Si te falta una palabra, créala con los morfemas que tienes. Escríbela [entre corchetes].
Glosa al español solo entre paréntesis, al final, si es imprescindible.
EJEMPLO: "Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni. [kali-bana: kali+-bana = orilla de luz]."
NO empieces con "Estoy..." ni "El sol..." — empieza con "Taya..." o "Nüma..." o directamente con el verbo."""


# ══════════════════════════════════════════════════════════════════════
# CLIENTE
# ══════════════════════════════════════════════════════════════════════

def get_client(run_id: Optional[str] = None) -> anthropic.Anthropic:
    """
    Devuelve el cliente Anthropic con LangSmith wrapping si está configurado.
    Delega a curiana_database.get_anthropic_client() para unificar setup.
    """
    return get_anthropic_client(run_id=run_id)


# ══════════════════════════════════════════════════════════════════════
# MEMORIA DE AGENTES (rolling, últimas 3 interacciones)
# ══════════════════════════════════════════════════════════════════════

class AgentMemory:
    def __init__(self):
        self._memory: dict[str, list[str]] = {}

    def add(self, agent_name: str, note: str):
        self._memory.setdefault(agent_name, []).append(note)
        self._memory[agent_name] = self._memory[agent_name][-3:]

    def get(self, agent_name: str) -> Optional[str]:
        notes = self._memory.get(agent_name, [])
        return " | ".join(notes) if notes else None

    def save(self, path="curiana_memory.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._memory, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path="curiana_memory.json") -> "AgentMemory":
        m = cls()
        try:
            with open(path, encoding="utf-8") as f:
                m._memory = json.load(f)
        except FileNotFoundError:
            pass
        return m


# ══════════════════════════════════════════════════════════════════════
# LLAMADA A AGENTE (con léxico inyectado)
# ══════════════════════════════════════════════════════════════════════

def _invoke(client: anthropic.Anthropic, system: str, user_message: str) -> str:
    """Una llamada cruda al modelo del agente."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_AGENT,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return resp.content[0].text.strip()


def call_agent(
    client: anthropic.Anthropic,
    agent_name: str,
    state: ComunidadState,
    lexico: LexicoComunitario,
    observer: ObserverAgent,
    user_message: str,
    agent_memory: Optional[str] = None,
    difusion: Optional[DifusionLexica] = None,
) -> str:
    agent = ALL_AGENTS.get(agent_name)
    if not agent:
        return f"[Agente '{agent_name}' no encontrado]"

    tier = agent.get("tier", 2)
    etnia = agent.get("etnia", "caquetío")

    # System prompt base del agente
    if tier == 3:
        base_prompt = (
            f"Eres {agent_name} de la Curiana, comunidad caquetía del Golfete de Coro. "
            f"{agent.get('descripcion', '')} Responde brevemente en personaje."
        )
    else:
        base_prompt = agent.get("system_prompt", f"Eres {agent_name} de la Curiana.")

    # Contexto dinámico del mundo
    world_context = state.to_context_string()

    # Ubicación actual
    ubicacion = state.ubicaciones_override.get(
        agent_name, agent.get("ubicacion_default", "plaza")
    )

    # Léxico + reglas apropiadas para el tier
    bloque_lexico = vocabulario_para_agente(tier, lexico)

    # Feedback lingüístico si el agente tuvo score bajo
    feedback = observer.feedback_para_agente(agent_name)

    # Rasgos dialectales según etnia (L2 con sintaxis propia, insulares, etc.)
    rasgos = prompt_rasgos_dialectales(etnia)

    # Contagio: palabras que el agente "ha oído" de gente que respeta
    sugerencia_contagio = ""
    if difusion is not None:
        sugs = difusion.sugerencias_para(agent_name, lexico=lexico)
        if sugs:
            txt = "; ".join(f"{f} = {s}" if s else f for f, s in sugs)
            sugerencia_contagio = (
                f"[Has oído estas palabras nuevas en boca de gente que respetas; "
                f"empléalas si encajan]: {txt}"
            )

    # Ensamblado del system prompt
    # Orden: persona → identidad lingüística → dialecto → mundo → léxico → contagio → memoria → refuerzo
    system_parts = [base_prompt, "---", _IDENTIDAD_LINGUISTICA]
    if rasgos:
        system_parts.append(rasgos)
    system_parts += ["---", world_context, f"[Tu ubicación]: {ubicacion}"]
    if bloque_lexico:
        system_parts.append(bloque_lexico)
    if sugerencia_contagio:
        system_parts.append(sugerencia_contagio)
    if agent_memory:
        system_parts.append(f"[Tu memoria reciente]: {agent_memory}")
    if feedback:
        system_parts.append(feedback)

    system = "\n".join(system_parts)

    # 1ª pasada
    response = _invoke(client, system, user_message)

    # ── RESCATE INTRA-TURNO (auditoría §3.4): si la densidad es baja, un único
    #    reintento que re-expresa la respuesta fallida en caquetío real ──
    metr = score_linguistico(response, lexico)
    if metr["score"] < 5.0:
        rescate = prompt_rescate_linguistico(
            response, metr["score"], metr.get("espanol_funcional", 0)
        )
        try:
            response2 = _invoke(client, system, user_message + "\n\n" + rescate)
            if score_linguistico(response2, lexico)["score"] > metr["score"]:
                response = response2
        except Exception:
            pass  # ante fallo de red, conserva la 1ª respuesta

    return response


# ══════════════════════════════════════════════════════════════════════
# DIRECTOR / NARRADOR
# ══════════════════════════════════════════════════════════════════════

DIRECTOR_SYSTEM = """Eres el Director de la simulación comunitaria de la Curiana.
Estilo: conciso, sensorial, presente. Crónica oral caquetía.
No uses lenguaje romántico ni exótico. Describe lo que un habitante vería y sentiría."""


def director_narrate(
    client: anthropic.Anthropic,
    state: ComunidadState,
    interactions: list[dict],
) -> str:
    resumen = "\n".join(
        f"- {i['agent']}: {i['response'][:100]}..."
        for i in interactions
    )
    prompt = f"""Estado: {state.to_context_string()}
Interacciones: {resumen}
Escribe el cierre narrativo del turno (2-3 oraciones)."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_DIRECTOR,
        system=DIRECTOR_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def director_select_event(
    client: anthropic.Anthropic,
    state: ComunidadState,
) -> Optional[dict]:
    prob = 0.3
    if state.nivel_tension == "alto":
        prob += 0.2
    if state.nivel_alimentos == "escaso":
        prob += 0.15
    if state.dia % 3 == 0:
        prob += 0.3
    if random.random() > prob:
        return None
    pool = EVENTOS_COTIDIANOS.copy()
    pool += EVENTOS_ESTACIONALES[:3] if state.estacion == "seca" else EVENTOS_ESTACIONALES[3:]
    return random.choice(pool)


# ══════════════════════════════════════════════════════════════════════
# TURNO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

MOMENTOS_ESTIMULO = {
    "amanecer": "Amanece en la Curiana. ¿Qué estás haciendo al comenzar el día?",
    "mañana":   "La mañana avanza. ¿En qué estás trabajando?",
    "mediodia": "Es mediodía. El calor obliga al descanso. ¿Dónde estás y qué piensas?",
    "tarde":    "La tarde en la Curiana. ¿Qué haces o con quién hablas?",
    "anochecer":"El sol cae sobre el Golfete. ¿Cómo terminas tu día?",
    "noche":    "La noche cae. ¿Qué pensamientos tienes?",
}


def run_turn(
    client: anthropic.Anthropic,
    state: ComunidadState,
    memory: AgentMemory,
    lexico: LexicoComunitario,
    observer: ObserverAgent,
    user_input: Optional[str] = None,
    verbose: bool = True,
    db=None,
    run_id: Optional[str] = None,
    difusion: Optional[DifusionLexica] = None,
) -> list[dict]:
    interactions = []

    # 0. Registrar turno en DB
    turn_id: Optional[str] = None
    if db and run_id:
        try:
            turn_id = db.save_turn(
                run_id=run_id,
                day=state.dia,
                turn_num=state.turno,
                moment=state.momento,
                season=state.estacion,
                event_description=state.evento_del_turno or None,
            )
        except Exception as e:
            if verbose:
                print(f"  ⚠ DB turn error: {e}")

    # 1. Director: ¿hay evento?
    evento = director_select_event(client, state)
    if evento:
        state.evento_del_turno = evento["descripcion"]
        state.eventos_activos = [evento["id"]]
        agentes_activos = [
            a for a in evento.get("agentes_involucrados", state.agentes_en_escena)
            if a in ALL_AGENTS and a not in ("toda_la_comunidad", "guerreros")
        ] or state.agentes_en_escena[:5]
    else:
        agentes_activos = state.agentes_en_escena

    if verbose:
        print(f"\n{'='*60}")
        print(f"  DÍA {state.dia} | TURNO {state.turno} | {state.momento.upper()}")
        print(f"  {state.estacion.upper()} — {state.clima}")
        if state.evento_del_turno:
            print(f"  📍 {state.evento_del_turno}")
        print(f"{'='*60}\n")

    # 2. Estímulo del turno
    if user_input:
        stimulus = user_input
    elif state.evento_del_turno:
        stimulus = f"[Situación]: {state.evento_del_turno}. ¿Cómo reaccionas?"
    else:
        stimulus = MOMENTOS_ESTIMULO.get(state.momento, "¿Qué haces ahora?")

    # 3. Activar agentes
    for agent_name in agentes_activos[:6]:
        if agent_name not in ALL_AGENTS:
            continue
        agent = ALL_AGENTS[agent_name]
        tier = agent.get("tier", 2)
        if tier == 3:
            continue

        mem = memory.get(agent_name)
        response = call_agent(
            client, agent_name, state, lexico, observer, stimulus, mem,
            difusion=difusion,
        )

        interactions.append({
            "agent": agent_name,
            "tier": tier,
            "etnia": agent.get("etnia", "caquetío"),
            "response": response,
        })

        # Análisis lingüístico por el Observer
        registro = observer.analizar(
            agente=agent_name,
            etnia=agent.get("etnia", "caquetío"),
            tier=tier,
            texto=response,
            dia=state.dia,
            turno=state.turno,
            momento=state.momento,
            estacion=state.estacion,
        )

        # Detectar adopciones de palabras propuestas por otros
        observer.procesar_adopciones(response, agent_name, state.turno)

        # Contagio: propagar exposición de las palabras emergentes que usó este
        # agente (no las del vocabulario base) a sus vecinos sociales.
        if difusion is not None:
            for forma in getattr(registro, "palabras_caquetias", []):
                if forma not in VOCABULARIO_BASE:
                    difusion.propagar_uso(forma, agent_name, state)
            for neo in getattr(registro, "neologismos_extraidos", []):
                difusion.propagar_uso(neo.forma, agent_name, state)

        # Persistir en Supabase
        if db and run_id and turn_id:
            try:
                # Extraer listas del registro
                words_used = list(getattr(registro, "palabras_caquetias", []))
                aspects_used = list(getattr(registro, "aspectos_usados", []))
                neos = getattr(registro, "neologismos_extraidos", [])
                neo_count = len(neos)

                response_id = db.save_agent_response(
                    turn_id=turn_id,
                    run_id=run_id,
                    agent_name=agent_name,
                    ethnicity=agent.get("etnia", "caquetío"),
                    tier=tier,
                    response_text=response,
                    score=registro.score,
                    words_used=words_used,
                    aspects_used=aspects_used,
                    neologisms_proposed=neo_count,
                )

                # Persistir neologismos propuestos
                for neo in neos:
                    try:
                        db.save_neologism(
                            run_id=run_id,
                            turn_id=turn_id,
                            proposed_by=agent_name,
                            proposed_day=state.dia,
                            form=neo.forma,
                            components=getattr(neo, "componentes", ""),
                            meaning=neo.significado,
                            morphological_rule=getattr(neo, "regla_aplicada", "desconocida"),
                        )
                    except Exception:
                        pass  # No interrumpir por neologismo fallido

            except Exception as e:
                if verbose:
                    print(f"  ⚠ DB agent error ({agent_name}): {e}")

        # Guardar en memoria del agente
        memory.add(agent_name, f"D{state.dia}T{state.turno}: {response[:70]}")

        if verbose:
            print(f"  [{agent_name} — {agent.get('etnia','caquetío').upper()}]")
            print(f"  {response}")
            score_bar = "●" * int(registro.score) + "○" * (10 - int(registro.score))
            print(f"  ╰─ {score_bar} {registro.score}/10")
            for neo in registro.neologismos_extraidos:
                print(f"     ✦ NUEVO: [{neo.forma}] = {neo.significado}")
            print()

    # 4. Narración del director
    if interactions and verbose:
        narration = director_narrate(client, state, interactions)
        print(f"  ── Narrador ──")
        print(f"  {narration}")

    # 5. Reporte Observer del turno
    if verbose:
        print(observer.reporte_turno(state.dia, state.turno))

    # 6. Avanzar estado
    state.avanzar_turno()

    return interactions


# ══════════════════════════════════════════════════════════════════════
# MODO INTERACTIVO
# ══════════════════════════════════════════════════════════════════════

def interactive_mode(client: anthropic.Anthropic):
    print("\n" + "="*60)
    print("  CURIANA — Laboratorio de Emergencia Lingüística v2")
    print("  Golfete de Coro · Falcón · Siglo XIV-XV")
    print("="*60)

    try:
        state = ComunidadState.load()
        print("  → Estado cargado.")
    except Exception:
        state = estado_inicial_test()
        print("  → Nuevo test run.")

    memory = AgentMemory.load()
    lexico = LexicoComunitario.load()
    lexico_anterior = len(lexico.neologismos_adoptados())

    try:
        obs_client = client
        observer = ObserverAgent.load(obs_client, lexico)
    except Exception:
        observer = ObserverAgent(client, lexico)

    # Difusión léxica (contagio sociolingüístico) — persiste durante todo el run
    difusion = DifusionLexica()

    # Inicializar DB (gracefully degraded si no hay Supabase)
    db = get_db()
    run_id = db.create_run(model=MODEL, config={"mode": "interactive"})
    client = get_client(run_id)  # re-crear con run_id para LangSmith

    print(f"\n  Vocabulario disponible: {len(lexico.palabras_activas())} palabras")
    print(f"  Situación: {state.evento_del_turno or 'La Curiana despierta.'}")
    print(f"  Run ID: {run_id[:8]}...\n")

    while True:
        try:
            user_input = input("  [CURIANA]> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            run_turn(client, state, memory, lexico, observer, db=db, run_id=run_id,
                     difusion=difusion)
        elif user_input.lower() == "salir":
            break
        elif user_input.lower() == "estado":
            print(f"\n{state.to_context_string()}\n")
        elif user_input.lower() == "lexico":
            print(f"\n{lexico.reporte_linguistico()}\n")
        elif user_input.lower() == "ranking":
            print("\n  Ranking lingüístico:")
            for agente, score in observer.ranking_linguistico():
                bar = "█" * int(score) + "░" * (10 - int(score))
                print(f"    {agente:15} {bar} {score:.1f}/10")
            print()
        elif user_input.lower().startswith("habla "):
            agent_name = user_input[6:].strip()
            if agent_name not in ALL_AGENTS:
                print(f"  Agente no encontrado. Disponibles: {', '.join(list(AGENTS_T1.keys())[:8])}...")
            else:
                try:
                    msg = input(f"  ¿Qué le dices a {agent_name}? > ").strip()
                    response = call_agent(
                        client, agent_name, state, lexico, observer, msg,
                        memory.get(agent_name), difusion=difusion
                    )
                    print(f"\n  [{agent_name}]: {response}\n")
                    observer.analizar(
                        agent_name,
                        ALL_AGENTS[agent_name].get("etnia", "caquetío"),
                        ALL_AGENTS[agent_name].get("tier", 2),
                        response, state.dia, state.turno, state.momento, state.estacion
                    )
                    memory.add(agent_name, f"D{state.dia}: conversación directa")
                except (EOFError, KeyboardInterrupt):
                    break
        elif user_input.lower().startswith("evento "):
            evento_id = user_input[7:].strip()
            todos = EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES
            ev = next((e for e in todos if e["id"] == evento_id), None)
            if ev:
                state.evento_del_turno = ev["descripcion"]
                state.eventos_activos = [evento_id]
                print(f"  Evento '{ev['nombre']}' activado.")
            else:
                print(f"  IDs disponibles: {[e['id'] for e in todos]}")
        elif user_input.lower() == "reporte dia":
            print(observer.reporte_dia(state.dia - 1))
        elif user_input.lower() == "exportar":
            observer.exportar_csv()
            observer.exportar_neologismos_csv()
        else:
            run_turn(
                client, state, memory, lexico, observer,
                user_input=user_input, db=db, run_id=run_id,
                difusion=difusion,
            )

    # Guardar todo
    state.save()
    memory.save()
    lexico.save()
    observer.save()
    observer.exportar_csv()
    observer.exportar_neologismos_csv()

    # Cerrar run
    db.end_run(run_id, total_turns=state.turno, total_days=state.dia)
    print("  Guardado. ¡Hasta la próxima jornada en la Curiana!")


# ══════════════════════════════════════════════════════════════════════
# MODO AUTOMÁTICO (con reportes periódicos)
# ══════════════════════════════════════════════════════════════════════

def auto_mode(
    client: anthropic.Anthropic,
    turnos: int,
    reporte_anual: bool = False,
    verbose: bool = True,
):
    """
    Corre N turnos automáticamente.
    Genera reportes al final de cada día, estación y año simulado.

    Mapeo temporal:
        1 turno = media jornada
        2 turnos = 1 día
        60 días = 1 estación (seca o lluvias)
        120 días = 1 año (2 estaciones)
        → 240 turnos = 1 año simulado completo
    """
    state = estado_inicial_test()
    memory = AgentMemory()
    lexico = LexicoComunitario.load()
    observer = ObserverAgent(client, lexico)
    difusion = DifusionLexica()

    # Inicializar DB (CurianaDB real o CurianaDBMock si no está configurada)
    db = get_db()
    run_id = db.create_run(
        model=MODEL,
        config={"max_turns": turnos, "mode": "auto"},
    )
    # Re-crear cliente con run_id para que LangSmith use el proyecto correcto
    client = get_client(run_id)

    estacion_anterior = state.estacion
    anio_simulado = 1
    dia_inicio_estacion = 1

    print(f"\n{'='*60}")
    print(f"  CURIANA — Modo Automático: {turnos} turnos")
    print(f"  ({turnos // 2} días simulados · {turnos // 240} año(s) aprox.)")
    print(f"  Run ID: {run_id[:8]}...")
    print(f"{'='*60}\n")

    for t in range(turnos):
        run_turn(
            client, state, memory, lexico, observer,
            verbose=verbose, db=db, run_id=run_id,
            difusion=difusion,
        )

        # Reporte al final de cada día
        if state.turno == 1 and state.dia > 1:  # acaba de cambiar de día
            dia_terminado = state.dia - 1
            if verbose:
                print(observer.reporte_dia(dia_terminado))

        # Detección de cambio de estación
        if state.estacion != estacion_anterior:
            if verbose:
                print(observer.reporte_estacion(estacion_anterior))
            estacion_anterior = state.estacion
            dia_inicio_estacion = state.dia

            # Cada vez que completa un año (2 estaciones), reporte anual
            if reporte_anual and state.dia % 120 == 0:
                print(observer.reporte_anual_llm(anio_simulado))
                anio_simulado += 1

    # Guardar localmente
    state.save()
    memory.save()
    lexico.save()
    observer.save()
    observer.exportar_csv()
    observer.exportar_neologismos_csv()

    # Cerrar run en DB
    db.end_run(run_id, total_turns=turnos, total_days=state.dia - 1)

    # Reporte final
    print(f"\n{'═'*60}")
    print(f"  SIMULACIÓN COMPLETADA: {turnos} turnos = {state.dia - 1} días")
    print(f"{'═'*60}")
    print(lexico.reporte_linguistico())
    print()
    print("  Ranking lingüístico final:")
    for agente, score in observer.ranking_linguistico()[:8]:
        bar = "█" * int(score) + "░" * (10 - int(score))
        print(f"    {agente:15} {bar} {score:.1f}/10")

    if reporte_anual:
        print(observer.reporte_anual_llm(anio_simulado))


# ══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Curiana v2 — Motor de emergencia lingüística caquetía"
    )
    parser.add_argument(
        "--auto", type=int, default=0,
        help="Turnos automáticos (0 = interactivo). 240 = 1 año simulado."
    )
    parser.add_argument(
        "--anio", action="store_true",
        help="Atajos: --auto 240 (1 año). Equivale a --auto 240."
    )
    parser.add_argument(
        "--reporte", action="store_true",
        help="Generar reporte anual LLM al completar cada año simulado."
    )
    parser.add_argument(
        "--silencioso", action="store_true",
        help="Solo mostrar reportes, no cada interacción individual."
    )
    args = parser.parse_args()

    client = get_client()

    if args.anio:
        auto_mode(client, 240, reporte_anual=True, verbose=not args.silencioso)
    elif args.auto > 0:
        auto_mode(
            client, args.auto,
            reporte_anual=args.reporte,
            verbose=not args.silencioso
        )
    else:
        interactive_mode(client)
