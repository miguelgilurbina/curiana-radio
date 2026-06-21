"""
CURIANA — Perfilador de Agentes
================================
Corre DESPUÉS de una simulación. Para cada agente que participó en un run:
  1. Junta todas sus respuestas (agent_responses).
  2. Le pide a Claude que analice su arco narrativo y elija las frases
     más célebres / con más impacto.
  3. Guarda el perfil en `agent_profiles` y las frases en `agent_quotes`.

Uso:
    python curiana_perfilador.py                  # perfila el último run, todos los agentes
    python curiana_perfilador.py --run <uuid>      # perfila un run específico
    python curiana_perfilador.py --agent Manaure   # solo un agente
    python curiana_perfilador.py --min-respuestas 3  # ignora agentes con pocas respuestas
"""

import os
import sys
import json
import argparse

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_agents import ALL_AGENTS, get_agent
from curiana_database import get_db, get_anthropic_client

MODEL = "claude-haiku-4-5-20251001"

PROMPT_TEMPLATE = """Eres un analista literario especializado en la lengua caquetía reconstruida.
Vas a analizar las intervenciones de UN personaje de una simulación multi-agente
ambientada en la Curiana (Golfete de Coro, siglo XIV-XV).

PERSONAJE: {agent_name}
Descripción narrativa: {descripcion}

INTERVENCIONES (día/turno, score de densidad lingüística 0-10, texto):
{respuestas}

Tu tarea:
1. Resume en 2-3 frases el "arco" de este personaje durante la simulación: cómo
   habló, qué lo distingue lingüísticamente, algún momento notable.
2. Define su rol en la comunidad en una frase corta (ej. "Señor de la Curiana y piache").
3. Elige hasta 5 frases célebres (las más originales, reveladoras del personaje,
   con mayor densidad caquetía, o que introdujeron/adoptaron un neologismo).
   Para cada una da una justificación breve (1 frase) y un impacto_score (0-10).

Responde SOLO con JSON válido, sin texto adicional, con esta forma exacta:
{{
  "rol_comunidad": "...",
  "resumen_arco": "...",
  "quotes": [
    {{"day": <int o null>, "turn_num": <int o null>, "quote": "...", "justificacion": "...", "impacto_score": <float 0-10>}}
  ]
}}
"""


def _format_respuestas(respuestas: list[dict], turns_by_id: dict) -> str:
    lines = []
    for r in respuestas:
        info = turns_by_id.get(r.get("turn_id"), {})
        day = info.get("day", "?")
        turn_num = info.get("turn_num", "?")
        score = r.get("score")
        lines.append(f"[día {day}, turno {turn_num}, score {score}] {r['response_text']}")
    return "\n".join(lines)


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def perfilar_agente(db, client, run_id: str, agent_name: str, min_respuestas: int = 1) -> bool:
    agent_def = get_agent(agent_name)
    if not agent_def:
        print(f"  ⚠  Agente desconocido: {agent_name}")
        return False

    respuestas = db.get_agent_responses(run_id, agent_name)
    if len(respuestas) < min_respuestas:
        print(f"  ↪  {agent_name}: solo {len(respuestas)} respuesta(s), se omite.")
        return False

    turns_by_id = {}
    try:
        turn_ids = list({r["turn_id"] for r in respuestas if r.get("turn_id")})
        if turn_ids:
            result = db.client.table("turns").select("id, day, turn_num").in_("id", turn_ids).execute()
            turns_by_id = {t["id"]: t for t in (result.data or [])}
    except Exception:
        pass

    descripcion = agent_def.get("descripcion", "")
    prompt = PROMPT_TEMPLATE.format(
        agent_name=agent_name,
        descripcion=descripcion,
        respuestas=_format_respuestas(respuestas, turns_by_id),
    )

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = "".join(block.text for block in message.content if hasattr(block, "text"))

    try:
        analisis = _parse_json_response(raw_text)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"  ⚠  {agent_name}: no se pudo parsear la respuesta del analista ({e})")
        return False

    total_respuestas = len(respuestas)
    scores = [r["score"] for r in respuestas if r.get("score") is not None]
    avg_score = round(sum(scores) / len(scores), 2) if scores else None
    neologismos_propuestos = sum(r.get("neologisms_proposed", 0) or 0 for r in respuestas)

    neologismos_adoptados = 0
    try:
        result = (
            db.client.table("neologisms")
            .select("id", count="exact")
            .eq("run_id", run_id)
            .eq("proposed_by", agent_name)
            .eq("status", "adoptado")
            .execute()
        )
        neologismos_adoptados = result.count or 0
    except Exception:
        pass

    profile_id = db.save_agent_profile(
        run_id=run_id,
        agent_name=agent_name,
        tier=agent_def.get("tier", 0),
        rol_comunidad=analisis.get("rol_comunidad", ""),
        resumen_arco=analisis.get("resumen_arco", ""),
        total_respuestas=total_respuestas,
        avg_score=avg_score,
        neologismos_propuestos=neologismos_propuestos,
        neologismos_adoptados=neologismos_adoptados,
    )

    db.clear_agent_quotes(profile_id)

    # Mapear (day, turn_num) -> response_id para enlazar la cita con su respuesta original
    response_by_turn = {
        (turns_by_id.get(r["turn_id"], {}).get("day"), turns_by_id.get(r["turn_id"], {}).get("turn_num")): r["id"]
        for r in respuestas
    }

    for q in analisis.get("quotes", []):
        key = (q.get("day"), q.get("turn_num"))
        db.save_agent_quote(
            profile_id=profile_id,
            run_id=run_id,
            agent_name=agent_name,
            quote=q.get("quote", ""),
            justificacion=q.get("justificacion", ""),
            impacto_score=q.get("impacto_score", 0),
            response_id=response_by_turn.get(key),
            day=q.get("day"),
            turn_num=q.get("turn_num"),
        )

    print(f"  ✓ {agent_name}: perfil generado ({total_respuestas} respuestas, {len(analisis.get('quotes', []))} frases)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Perfilador de agentes Curiana")
    parser.add_argument("--run", help="UUID del simulation_run a perfilar (default: el más reciente)")
    parser.add_argument("--agent", help="Perfilar solo este agente (default: todos los que tuvieron respuestas)")
    parser.add_argument("--min-respuestas", type=int, default=1, help="Mínimo de respuestas para generar perfil")
    args = parser.parse_args()

    db = get_db()
    if not hasattr(db, "client"):
        print("✗ Sin Supabase configurado. El perfilador necesita una base de datos real.")
        sys.exit(1)

    run_id = args.run
    if not run_id:
        run = db.latest_run()
        if not run:
            print("✗ No hay simulation_runs registrados.")
            sys.exit(1)
        run_id = run["id"]
        print(f"  ℹ  Usando el run más reciente: {run_id[:8]}...")

    client = get_anthropic_client(run_id=run_id)

    if args.agent:
        nombres = [args.agent]
    else:
        result = (
            db.client.table("agent_responses")
            .select("agent_name")
            .eq("run_id", run_id)
            .execute()
        )
        nombres = sorted({r["agent_name"] for r in (result.data or [])})

    if not nombres:
        print("✗ Ese run no tiene agent_responses.")
        sys.exit(1)

    print(f"── Perfilando {len(nombres)} agente(s) del run {run_id[:8]}... ──")
    ok = 0
    for nombre in nombres:
        if perfilar_agente(db, client, run_id, nombre, min_respuestas=args.min_respuestas):
            ok += 1

    print(f"\n✓ {ok}/{len(nombres)} perfiles generados.")


if __name__ == "__main__":
    main()
