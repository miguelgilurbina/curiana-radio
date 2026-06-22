"""
One-off: regenera las frases curadas (agent_quotes) del run ya corrido para
agregarles `translation`, sin recalcular nada que ya estaba correcto
(neologismos_adoptados viene de la replicacion de adopciones durante el run
real, no es reconstruible desde response_text solo -- se preserva tal cual).

Reconstruye el historial de RegistroInteraccion desde Supabase (agent_responses
+ turns), corre analizar_agente_curado() por agente con el prompt actualizado
(que ahora pide "traduccion" ademas de "quote"/"justificacion"), y persiste
solo perfil + quotes -- preservando neologismos_adoptados de la fila existente.

Uso: python regenerar_quotes_traduccion.py [run_id]
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import CurianaDB, get_anthropic_client
from curiana_lexicon import LexicoComunitario, extraer_neologismos_del_texto
from curiana_observer import ObserverAgent, RegistroInteraccion


def main():
    run_id = sys.argv[1] if len(sys.argv) > 1 else "2e729f3f-ebf4-4d23-8142-c4c65b06e27b"

    db = CurianaDB()
    client = get_anthropic_client()

    turns = db.client.table("turns").select("id, day, turn_num, moment, season").eq("run_id", run_id).execute().data
    turn_meta = {t["id"]: t for t in turns}

    responses = (
        db.client.table("agent_responses")
        .select("id, turn_id, agent_name, ethnicity, tier, response_text, score")
        .eq("run_id", run_id)
        .execute()
        .data
    )

    lexico = LexicoComunitario()
    observer = ObserverAgent(client, lexico)
    for r in responses:
        tm = turn_meta.get(r["turn_id"], {})
        dia = tm.get("day", 0)
        turno = tm.get("turn_num", 0)
        neos = extraer_neologismos_del_texto(r["response_text"], r["agent_name"], dia, turno)
        observer._historial.append(RegistroInteraccion(
            dia=dia, turno=turno,
            momento=tm.get("moment", ""), estacion=tm.get("season", ""),
            agente=r["agent_name"], etnia=r["ethnicity"], tier=r["tier"],
            texto=r["response_text"], score=r["score"],
            neologismos_extraidos=neos, response_id=r["id"],
        ))

    perfiles_existentes = {
        p["agent_name"]: p
        for p in db.client.table("agent_profiles").select("*").eq("run_id", run_id).execute().data
    }

    ok = 0
    for agente, perfil in perfiles_existentes.items():
        analisis = observer.analizar_agente_curado(agente)
        if not analisis:
            print(f"  x {agente}: sin historial reconstruido, se omite")
            continue

        profile_id = db.save_agent_profile(
            run_id=run_id,
            agent_name=agente,
            tier=perfil.get("tier", 0),
            rol_comunidad=analisis.get("rol_comunidad", perfil.get("rol_comunidad", "")),
            resumen_arco=analisis.get("resumen_arco", perfil.get("resumen_arco", "")),
            total_respuestas=analisis["total_respuestas"],
            avg_score=analisis["avg_score"],
            neologismos_propuestos=analisis["neologismos_propuestos"],
            neologismos_adoptados=perfil.get("neologismos_adoptados", 0),  # preservado
        )
        db.clear_agent_quotes(profile_id)
        for q in analisis.get("quotes", []):
            db.save_agent_quote(
                profile_id=profile_id,
                run_id=run_id,
                agent_name=agente,
                quote=q.get("quote", ""),
                justificacion=q.get("justificacion", ""),
                impacto_score=q.get("impacto_score", 0),
                translation=q.get("traduccion", ""),
                response_id=q.get("response_id"),
                day=q.get("dia"),
                turn_num=q.get("turno"),
            )
        print(f"  OK {agente}: {len(analisis.get('quotes', []))} frases regeneradas con traduccion")
        ok += 1

    print(f"\n{ok}/{len(perfiles_existentes)} perfiles regenerados.")


if __name__ == "__main__":
    main()
