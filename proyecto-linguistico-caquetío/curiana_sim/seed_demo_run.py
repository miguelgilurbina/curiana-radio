"""
CURIANA — Generador de datos demo (sin LLM)
===========================================

Crea un `simulation_run` completo en Supabase a partir de respuestas de agentes
PRE-ESCRITAS (no llama a Claude). Las pasa por el MISMO flujo de producción
(`observer.analizar` → `score_linguistico` → `db.save_*`), de modo que prueba
end-to-end el pipeline de persistencia — incluyendo el fix del BUG 3
(`aspects_used`, `regla_aplicada`) — y deja al dashboard datos reales que mostrar.

Requiere Supabase configurado (SUPABASE_URL + SUPABASE_SERVICE_KEY en el entorno
o en curiana_sim/.env). Si no, cae a CurianaDBMock y solo valida el código.

Uso:
    PYTHONUTF8=1 python seed_demo_run.py
"""

import os

# Cargar curiana_sim/.env si python-dotenv está disponible
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except Exception:
    pass

from curiana_database import get_db
from curiana_observer import ObserverAgent
from curiana_lexicon import LexicoComunitario


# ── Guion demo: 3 días, respuestas que SUBEN en densidad caquetía ──────
# Cada entrada: (dia, turno, momento, estacion, evento, [(agente, etnia, tier, texto)])
# La deriva: el español inicial cede paso a caquetío denso + neologismos adoptados.

GUION = [
    (1, 1, "amanecer", "seca", "La Curiana despierta tras la tormenta.", [
        ("Manaure", "caquetío", 1,
         "Taya naa-ka habo-bana. Wa-buco kira-ni. Biro rua-da taya Curiana-ana."),
        ("Tawaka", "caquetío", 1,
         "Estoy en la orilla mirando el mar, voy a preparar las canoas para hoy."),
        ("Marokoto-ni", "caribe", 1,
         "Yo mira el agua. Taya kira arima. Mucho pez viene con la marea."),
    ]),
    (1, 2, "mañana", "seca", None, [
        ("Shaboro", "caquetío", 1,
         "Nüma suna-ni choza-ko. Taya raka-da maa wara. "
         "[sima-bana: sima+-bana = orilla de los sueños]"),
        ("Nubiri-sha", "caquetía", 1,
         "Wa-amana masa-ni. Taya paa-ka kashi pia. Ta-barsure wana-ka."),
        ("Dara-ko", "caquetío", 1,
         "Taya naba-ni wa-buco. Kira-da taya duna wara. Ka biro suka-ka."),
    ]),
    (2, 3, "mañana", "seca", "Llega Kadushi desde las islas con noticias.", [
        ("Kadushi", "caquetío_aruba", 1,
         "Taya naa-ka maure-gua. Watapana kira-ni. "
         "[kuru-bana: kuru+-bana = ribera arbolada]"),
        ("Buio-sha", "caquetía", 1,
         "Taya suna-ka sima-bana. Nüma maa-ni wara. Wa-barsure raka-da."),
        ("Chiriguare", "caquetío", 1,
         "Taya panaa-ka perimetro-ana. Naya wana-ni. Ka mara taya kira-da."),
    ]),
    (2, 4, "tarde", "seca", None, [
        ("Manaure", "caquetío", 1,
         "Taya maa-ka naya. Wa-Curiana kira-ni wara. Biro paa-da taya pia-kana. "
         "[managua-ana: managua+-ana = lugar del señorío]"),
        ("Corie-ko", "caquetío", 1,
         "Taya kono-ni conuco-ko. Arima wana-ka. Ta-duna suka-da kashi."),
        ("Buio-sha", "caquetía", 1,
         "Taya naba-ka sima-bana. Kuru-bana kira-ni. Nüma raka-da wa-barsure."),
    ]),
    (3, 5, "amanecer", "lluvias", "Empiezan las lluvias sobre el Golfete.", [
        ("Shaboro", "caquetío", 1,
         "Naya suna-ni. Taya maa-ka tüshi wara. Sima-bana kira-da naya-kana."),
        ("Nubiri-sha", "caquetía", 1,
         "Wa-amana wana-ka. Taya masa-ni kashi. Kuru-bana paa-da taya."),
        ("Tawaka", "caquetío", 1,
         "Taya kira-ka wa-buco. Naa-da taya habo-bana. Ka biro rua-ni wara."),
    ]),
]

# Neologismos que "se adoptan" durante el run (2+ agentes los usan)
ADOPTADOS = ["sima-bana", "kuru-bana"]


def main():
    db = get_db()
    es_real = type(db).__name__ == "CurianaDB"
    print(f"  Backend: {type(db).__name__}  ({'Supabase REAL' if es_real else 'mock'})")

    observer = ObserverAgent(client=None, lexico=LexicoComunitario())

    run_id = db.create_run(
        model="demo-seed (sin LLM)",
        config={"mode": "demo", "fuente": "seed_demo_run.py"},
    )

    total_resp = total_neo = 0
    max_dia = max_turno = 0

    for dia, turno, momento, estacion, evento, agentes in GUION:
        turn_id = db.save_turn(run_id, dia, turno, momento, estacion, evento)
        max_dia, max_turno = max(max_dia, dia), max(max_turno, turno)

        for agente, etnia, tier, texto in agentes:
            reg = observer.analizar(
                agente=agente, etnia=etnia, tier=tier, texto=texto,
                dia=dia, turno=turno, momento=momento, estacion=estacion,
            )
            db.save_agent_response(
                turn_id=turn_id, run_id=run_id, agent_name=agente,
                ethnicity=etnia, tier=tier, response_text=texto,
                score=reg.score,
                words_used=list(reg.palabras_caquetias),
                aspects_used=list(reg.aspectos_usados),
                neologisms_proposed=len(reg.neologismos_extraidos),
            )
            total_resp += 1

            for neo in reg.neologismos_extraidos:
                db.save_neologism(
                    run_id=run_id, turn_id=turn_id, proposed_by=agente,
                    proposed_day=dia, form=neo.forma, components=neo.componentes,
                    meaning=neo.significado, morphological_rule=neo.regla_aplicada,
                )
                total_neo += 1

            barra = "●" * int(reg.score) + "○" * (10 - int(reg.score))
            print(f"  D{dia}T{turno} {agente:13} {barra} {reg.score:>4}/10  "
                  f"{etnia}")

    # Marcar neologismos como adoptados (para la vista 'adoptado' del dashboard)
    for forma in ADOPTADOS:
        try:
            db.update_neologism_status(
                form=forma, run_id=run_id, status="adoptado",
                adopted_by=["Buio-sha", "Shaboro"],
            )
        except Exception:
            pass

    db.end_run(run_id, total_turns=max_turno, total_days=max_dia)

    print(f"\n  ✓ Run demo creado: {run_id}")
    print(f"    {total_resp} respuestas · {total_neo} neologismos · "
          f"{len(ADOPTADOS)} adoptados · {max_dia} días")
    if es_real:
        print(f"    Dashboard: el run aparecerá en la lista. run_id={run_id[:8]}…")
    else:
        print("    (mock: no se persistió; configura Supabase para datos reales)")


if __name__ == "__main__":
    main()
