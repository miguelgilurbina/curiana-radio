"""
CURIANA — Orquestador Principal
El Director Agent que gestiona la simulación comunitaria.

Modelo usado: claude-haiku-4-5-20251001 (para todos los agentes)
Requiere: anthropic Python SDK  →  pip install anthropic

Uso:
    python curiana_orchestrator.py                  # test run interactivo
    python curiana_orchestrator.py --auto 10        # 10 turnos automáticos
"""

import os
import sys
import json
import random
import argparse
from typing import Optional

import anthropic

from curiana_agents import ALL_AGENTS, AGENTS_T1, AGENTS_T2, AGENTS_T3
from curiana_state import (
    ComunidadState,
    estado_inicial_test,
    EVENTOS_COTIDIANOS,
    EVENTOS_ESTACIONALES,
    MOMENTOS_DIA,
    LOCACIONES,
)

# ── Configuración ─────────────────────────────────────────────────────────────

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_AGENT = 400      # Respuesta por agente (Haiku es conciso)
MAX_TOKENS_DIRECTOR = 600   # Respuesta del director/narrador

# ── Cliente Anthropic ─────────────────────────────────────────────────────────

def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "Falta ANTHROPIC_API_KEY en las variables de entorno.\n"
            "Ejecuta: export ANTHROPIC_API_KEY='tu-clave'"
        )
    return anthropic.Anthropic(api_key=api_key)


# ── Llamada a un agente individual ────────────────────────────────────────────

def call_agent(
    client: anthropic.Anthropic,
    agent_name: str,
    state: ComunidadState,
    user_message: str,
    agent_memory: Optional[str] = None,
) -> str:
    """
    Llama a un agente individual con su system prompt + contexto dinámico.

    El contexto dinámico se construye en cada turno:
    - Estado actual del mundo (día, clima, eventos)
    - Ubicación actual del agente
    - Memoria reciente del agente (últimas 3 interacciones relevantes)
    """
    agent = ALL_AGENTS.get(agent_name)
    if not agent:
        return f"[Agente '{agent_name}' no encontrado]"

    tier = agent.get("tier", 2)

    # System prompt base
    if tier == 3:
        # Tier III: prompt mínimo generado desde la descripción
        base_prompt = (
            f"Eres {agent_name} de la Curiana, comunidad caquetía del Golfete de Coro. "
            f"{agent.get('descripcion', '')} "
            f"Responde brevemente en español, en personaje."
        )
    else:
        base_prompt = agent.get("system_prompt", f"Eres {agent_name} de la Curiana.")

    # Contexto dinámico del mundo
    world_context = state.to_context_string()

    # Ubicación actual
    ubicacion = state.ubicaciones_override.get(agent_name, agent.get("ubicacion_default", "plaza"))

    # Ensamblado final del system prompt
    system = f"""{base_prompt}

---
{world_context}
[Tu ubicación ahora]: {ubicacion}
"""

    if agent_memory:
        system += f"[Tu memoria reciente]: {agent_memory}\n"

    # Llamada a Haiku
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_AGENT,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text.strip()


# ── Director / Narrador ───────────────────────────────────────────────────────

DIRECTOR_SYSTEM = """Eres el Director de la simulación comunitaria de la Curiana.
La Curiana es un asentamiento caquetío en el Golfete de Coro, Venezuela, siglo XIV-XV, pre-contacto europeo.

Tu función es triple:
1. NARRAR: Describir el estado del mundo en cada turno (2-3 frases vívidas del ambiente).
2. DECIDIR: Qué agentes están activos este turno y qué evento ocurre (si alguno).
3. RESUMIR: Al final de cada turno, qué cambió en el estado comunitario.

Estilo narrativo: conciso, sensorial, presente. Como una crónica oral caquetía.
No uses lenguaje romántico ni exótico. Describe lo que un habitante de la Curiana vería y sentiría.
"""

def director_narrate(
    client: anthropic.Anthropic,
    state: ComunidadState,
    interactions: list[dict],
) -> str:
    """Genera la narración del Director al final de un turno."""

    interaction_summary = "\n".join(
        f"- {i['agent']}: {i['response'][:120]}..."
        for i in interactions
    )

    prompt = f"""Estado actual: {state.to_context_string()}

Interacciones de este turno:
{interaction_summary}

Escribe la narración del cierre de este turno (3-4 oraciones).
Luego sugiere en JSON: {{"siguiente_evento": "...", "agentes_proximos": ["..."], "cambio_estado": {{}}}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_DIRECTOR,
        system=DIRECTOR_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def director_select_event(
    client: anthropic.Anthropic,
    state: ComunidadState,
) -> Optional[dict]:
    """El director decide si ocurre un evento este turno."""

    # Probabilidad simple basada en el estado
    prob = 0.3  # 30% base
    if state.nivel_tension == "alto":
        prob += 0.2
    if state.nivel_alimentos == "escaso":
        prob += 0.15
    if state.dia % 3 == 0:  # Cada 3 días algo pasa
        prob += 0.3

    if random.random() > prob:
        return None  # Sin evento especial este turno

    # Seleccionar evento
    pool = EVENTOS_COTIDIANOS.copy()
    if state.estacion == "seca":
        pool += EVENTOS_ESTACIONALES[:3]  # Los primeros 3 son de seca
    else:
        pool += EVENTOS_ESTACIONALES[3:]  # Los últimos son de lluvias

    return random.choice(pool)


# ── Memoria de agentes ────────────────────────────────────────────────────────

class AgentMemory:
    """Memoria ligera por agente: guarda las últimas 3 interacciones relevantes."""

    def __init__(self):
        self._memory: dict[str, list[str]] = {}

    def add(self, agent_name: str, note: str):
        if agent_name not in self._memory:
            self._memory[agent_name] = []
        self._memory[agent_name].append(note)
        # Mantener solo las últimas 3
        self._memory[agent_name] = self._memory[agent_name][-3:]

    def get(self, agent_name: str) -> Optional[str]:
        notes = self._memory.get(agent_name, [])
        if not notes:
            return None
        return " | ".join(notes)

    def save(self, path: str = "curiana_memory.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._memory, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str = "curiana_memory.json") -> "AgentMemory":
        m = cls()
        try:
            with open(path, encoding="utf-8") as f:
                m._memory = json.load(f)
        except FileNotFoundError:
            pass
        return m


# ── Bucle principal de simulación ─────────────────────────────────────────────

def run_turn(
    client: anthropic.Anthropic,
    state: ComunidadState,
    memory: AgentMemory,
    user_input: Optional[str] = None,
    verbose: bool = True,
) -> list[dict]:
    """
    Ejecuta un turno completo de la simulación.

    Retorna lista de interacciones del turno.
    """
    interactions = []

    # ── 1. Director decide evento ──────────────────────────────────────────
    evento = director_select_event(client, state)
    if evento:
        state.evento_del_turno = evento["descripcion"]
        state.eventos_activos = [evento["id"]]
        agentes_activos = evento.get("agentes_involucrados", state.agentes_en_escena)
        # Resolver "toda_la_comunidad" → top 5 de T1
        agentes_activos = [
            a for a in agentes_activos
            if a in ALL_AGENTS and a != "toda_la_comunidad" and a != "guerreros"
        ]
        if not agentes_activos:
            agentes_activos = state.agentes_en_escena[:5]
    else:
        agentes_activos = state.agentes_en_escena

    if verbose:
        print(f"\n{'='*60}")
        print(f"  DÍA {state.dia} | TURNO {state.turno} | {state.momento.upper()}")
        print(f"  {state.estacion.upper()} — {state.clima}")
        if state.evento_del_turno:
            print(f"  📍 {state.evento_del_turno}")
        print(f"{'='*60}\n")

    # ── 2. Activar agentes en escena ───────────────────────────────────────
    # La entrada del usuario (o el evento) es el estímulo
    if user_input:
        stimulus = user_input
    elif state.evento_del_turno:
        stimulus = f"[Situación]: {state.evento_del_turno}. ¿Cómo reaccionas o qué haces?"
    else:
        # Turno cotidiano: estímulo de actividad rutinaria
        momento_acts = {
            "amanecer": "Amanece en la Curiana. ¿Qué estás haciendo al comenzar el día?",
            "mañana": "La mañana avanza en la Curiana. ¿En qué estás trabajando?",
            "mediodia": "Es mediodía. El calor obliga al descanso. ¿Dónde estás y con qué en mente?",
            "tarde": "La tarde en la Curiana. ¿Qué haces o con quién hablas?",
            "anochecer": "El sol cae sobre el Golfete. ¿Cómo terminas tu día?",
            "noche": "La noche cae. ¿Qué pensamientos tienes antes de dormir?",
        }
        stimulus = momento_acts.get(state.momento, "¿Qué haces ahora?")

    # Llamar a cada agente activo
    for agent_name in agentes_activos[:6]:  # Máximo 6 por turno para no disparar costos
        if agent_name not in ALL_AGENTS:
            continue

        agent = ALL_AGENTS[agent_name]
        tier = agent.get("tier", 2)

        # Solo Tier I y II hablan (T3 es fondo)
        if tier == 3:
            continue

        mem = memory.get(agent_name)
        response = call_agent(client, agent_name, state, stimulus, mem)

        interactions.append({
            "agent": agent_name,
            "tier": tier,
            "etnia": agent.get("etnia", "caquetío"),
            "response": response,
        })

        # Guardar en memoria
        memory.add(agent_name, f"Día {state.dia}T{state.turno}: {response[:80]}")

        if verbose:
            etnia_label = agent.get("etnia", "caquetío").upper()
            print(f"  [{agent_name} — {etnia_label}]")
            print(f"  {response}")
            print()

    # ── 3. Narración del director ──────────────────────────────────────────
    if interactions and verbose:
        narration = director_narrate(client, state, interactions)
        print(f"\n  ── Narrador ──")
        print(f"  {narration}")
        print()

    # ── 4. Avanzar estado ─────────────────────────────────────────────────
    state.avanzar_turno()

    return interactions


# ── Modo interactivo ───────────────────────────────────────────────────────────

def interactive_mode(client: anthropic.Anthropic):
    """
    Simulación interactiva: el usuario puede hablar con agentes o dejar correr el tiempo.

    Comandos:
        [Enter]              → Avanzar turno automáticamente
        habla <nombre>       → Hablar directamente con un agente
        estado               → Ver estado actual
        evento <id>          → Forzar un evento específico
        salir                → Terminar
    """
    print("\n" + "="*60)
    print("  CURIANA — Simulación Comunitaria")
    print("  Golfete de Coro · Falcón · Siglo XIV-XV")
    print("  Pre-contacto europeo puro")
    print("="*60)

    # Inicializar estado y memoria
    try:
        state = ComunidadState.load()
        print("  → Estado cargado desde archivo.")
    except Exception:
        state = estado_inicial_test()
        print("  → Iniciando nuevo test run.")

    memory = AgentMemory.load()

    print(f"\n  Situación inicial:")
    print(f"  {state.evento_del_turno or 'La Curiana despierta con el viento del noreste.'}\n")

    while True:
        try:
            user_input = input("  [CURIANA]> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Guardando estado...")
            break

        if not user_input:
            # Avance automático de turno
            run_turn(client, state, memory)
        elif user_input.lower() == "salir":
            break
        elif user_input.lower() == "estado":
            print(f"\n{state.to_context_string()}\n")
        elif user_input.lower().startswith("habla "):
            agent_name = user_input[6:].strip()
            if agent_name not in ALL_AGENTS:
                print(f"  Agente '{agent_name}' no encontrado.")
                print(f"  Agentes disponibles: {', '.join(list(AGENTS_T1.keys())[:10])}...")
            else:
                try:
                    msg = input(f"  ¿Qué le dices a {agent_name}? > ").strip()
                    response = call_agent(client, agent_name, state, msg, memory.get(agent_name))
                    print(f"\n  [{agent_name}]: {response}\n")
                    memory.add(agent_name, f"Día {state.dia}: conversación directa")
                except (EOFError, KeyboardInterrupt):
                    break
        elif user_input.lower().startswith("evento "):
            evento_id = user_input[7:].strip()
            todos_eventos = EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES
            evento = next((e for e in todos_eventos if e["id"] == evento_id), None)
            if evento:
                state.evento_del_turno = evento["descripcion"]
                state.eventos_activos = [evento_id]
                print(f"  Evento '{evento['nombre']}' activado.")
            else:
                ids = [e["id"] for e in todos_eventos]
                print(f"  Evento no encontrado. IDs disponibles: {ids}")
        else:
            # Input libre: se pasa como estímulo al siguiente turno
            run_turn(client, state, memory, user_input=user_input)

    # Guardar antes de salir
    state.save()
    memory.save()
    print("  Estado guardado. ¡Hasta la próxima jornada en la Curiana!")


# ── Modo automático ────────────────────────────────────────────────────────────

def auto_mode(client: anthropic.Anthropic, turnos: int):
    """Corre N turnos automáticos sin input del usuario. Útil para generar historia."""
    state = estado_inicial_test()
    memory = AgentMemory()

    print(f"\nCURIANA — Modo Automático ({turnos} turnos)\n")

    for _ in range(turnos):
        run_turn(client, state, memory)

    state.save()
    memory.save()
    print(f"\nSimulación completada. {turnos} turnos = {state.dia - 1} días en la Curiana.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Curiana — Simulación comunitaria caquetía")
    parser.add_argument("--auto", type=int, default=0,
                        help="Correr N turnos automáticos (0 = modo interactivo)")
    args = parser.parse_args()

    client = get_client()

    if args.auto > 0:
        auto_mode(client, args.auto)
    else:
        interactive_mode(client)
