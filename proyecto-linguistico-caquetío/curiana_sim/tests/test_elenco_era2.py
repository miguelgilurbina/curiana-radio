"""El elenco de la era 2 en el motor (Miguel, 2026-09-14: «hacemos la generación
de agentes para la era 2»).

  - curiana_agents_era2.py es GENERADO: tiene que ser lo que emite
    6-fusion/scripts/generar_agentes_era2.py desde 6-fusion/elenco_era2.yaml.
  - 63 agentes con nodo, casa y sitio; ninguno dice «Curiana»; los tier 3
    traen su prompt.
  - CURIANA_ELENCO=era2 hace que curiana_agents exponga ese elenco.
  - El prompt de un agente de la era 2 nombra su nodo y su sitio; el estímulo
    del turno nombra su sitio.
  - El tier 3 ya ve una muestra de vocabulario.
"""
import importlib.util
import io
import os
import subprocess
import sys

import pytest
import yaml

import curiana_orchestrator_v2 as orch
import curiana_agents_era2 as era2
from curiana_lexicon import LexicoComunitario, vocabulario_para_agente
from curiana_observer import ObserverAgent
from curiana_state import estado_inicial_test

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(SIM)
GENERADOR = os.path.join(RAIZ, "6-fusion", "scripts", "generar_agentes_era2.py")
YAML = os.path.join(RAIZ, "6-fusion", "elenco_era2.yaml")
MODULO = os.path.join(SIM, "curiana_agents_era2.py")


def _cargar_generador():
    spec = importlib.util.spec_from_file_location("generar_agentes_era2", GENERADOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_el_modulo_generado_es_lo_que_emite_el_script():
    """Regla del proyecto para los generados (cf. toponimos.yaml): se corrige
    el YAML y se regenera; nadie edita el módulo a mano."""
    gen = _cargar_generador()
    elenco = yaml.safe_load(io.open(YAML, encoding="utf-8"))
    assert io.open(MODULO, encoding="utf-8").read() == gen.emitir(elenco)


def test_el_elenco_era2_tiene_sus_63_con_nodo_casa_y_sitio():
    assert len(era2.ALL_AGENTS) == era2.MEDIDO["total_agentes"] == 63
    for nombre, a in era2.ALL_AGENTS.items():
        assert a["nodo"] in ("GUARANAO", "AMUAY"), nombre
        assert a["casa"] and a["sitio"] in era2.SITIOS, nombre
        assert a["tier"] in (1, 2, 3) and a["etnia"] in ("caquetío", "caquetía"), nombre
        assert a["system_prompt"] and "Curiana" not in a["system_prompt"], nombre
        assert a["dossier"].get("hechos") or a["dossier"].get("obras"), nombre
    assert era2.MUNDO == "PARAGUANÁ"
    assert len(era2.ROSTER_NUCLEO) == era2.MEDIDO["en_roster"] == 24


def test_los_tier_3_de_la_era2_traen_prompt_con_su_nodo():
    t3 = [a for a in era2.ALL_AGENTS.values() if a["tier"] == 3]
    assert t3
    for a in t3:
        assert a["nodo"] in a["system_prompt"] and a["sitio"] in a["system_prompt"]


def test_el_conmutador_carga_el_elenco_de_la_era2():
    """Se prueba en un subproceso: el elenco se decide al importar."""
    codigo = "import curiana_agents as c; print(len(c.ALL_AGENTS), c.MUNDO, c.ELENCO)"
    for env, esperado in (({}, "60 CURIANA era1"), ({"CURIANA_ELENCO": "era2"}, "63 PARAGUANÁ era2")):
        r = subprocess.run([sys.executable, "-c", codigo], cwd=SIM, capture_output=True,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8", **env})
        assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
        assert r.stdout.decode("utf-8").strip() == esperado


def test_el_roster_todos_bajo_era2_son_los_63_y_nucleo_los_24(monkeypatch):
    monkeypatch.setattr(orch, "ALL_AGENTS", era2.ALL_AGENTS)
    monkeypatch.setattr(orch, "ROSTER_NUCLEO", era2.ROSTER_NUCLEO)
    todos = orch.roster_de_habla("todos")
    assert len(todos) == 63 and set(todos) == set(era2.ALL_AGENTS)
    assert orch.roster_de_habla("nucleo") == era2.ROSTER_NUCLEO


def test_el_prompt_de_un_agente_de_la_era2_nombra_su_nodo_y_su_sitio(monkeypatch):
    capturado = {}

    def invoke_falso(client, system, user_message):
        capturado["system"], capturado["user"] = system, user_message
        return "Taya wana-ka arima."
    monkeypatch.setattr(orch, "ALL_AGENTS", era2.ALL_AGENTS)
    monkeypatch.setattr(orch, "_invoke", invoke_falso)
    lexico = LexicoComunitario()
    state = estado_inicial_test()
    state.mundo = era2.MUNDO
    orch.call_agent(object(), "Kunaro-bana", state, lexico, ObserverAgent(object(), lexico),
                    orch.MOMENTOS_ESTIMULO["amanecer"])
    s = capturado["system"]
    assert "[Tu gente]: tu nodo es GUARANAO" in s and "Tacuato" in s
    assert "la orilla del Golfete" in s
    assert "[PARAGUANÁ — " in s and "[CURIANA" not in s
    assert capturado["user"].startswith("Amanece en Tacuato.")
    assert "{lugar}" not in capturado["user"]


def test_un_agente_de_la_era1_no_recibe_bloque_de_gente(monkeypatch):
    capturado = {}
    monkeypatch.setattr(orch, "_invoke", lambda c, s, u: capturado.update(system=s, user=u) or "x")
    lexico = LexicoComunitario()
    orch.call_agent(object(), "Manaure", estado_inicial_test(), lexico,
                    ObserverAgent(object(), lexico), orch.MOMENTOS_ESTIMULO["amanecer"])
    assert "[Tu gente]" not in capturado["system"]
    assert capturado["user"].startswith("Amanece en la Curiana.")


def test_el_tier_3_ve_reglas_y_una_muestra():
    bloque = vocabulario_para_agente(3, LexicoComunitario())
    assert "[LENGUA CAQUETÍA" in bloque and "[VOCABULARIO CAQUETÍO ADICIONAL" in bloque
    t1 = vocabulario_para_agente(1, LexicoComunitario())
    assert len(bloque) < len(t1)
