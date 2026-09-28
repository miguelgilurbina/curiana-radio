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
  - Campaña de antropónimos (Miguel, 2026-09-14: «Sí o sí hay que sacar eso
    de -ko y -sha. Si es inventado, tanto de la gramática como de los
    nombres»): ningún nombre lleva -ko ni -sha, y ALIAS_ERA1 resuelve del
    nombre viejo al nuevo para los 63.
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


def test_ningun_nombre_de_la_era2_lleva_ko_ni_sha():
    """Los sufijos -ko «hombre de» y -sha «mujer de» eran convención de la era 1
    sin campo de evidencia. Miguel los retiró el 2026-09-14 de los nombres y de
    la gramática; aquí se vigila la mitad de los nombres.

    `conservados` son los tres que el sistema de nombres declara intactos
    (6-fusion/sistema_de_nombres_era2.yaml regla g): ninguno lleva -ko ni -sha,
    así que la lista existe para que el test siga siendo verdad si algún día se
    declara una excepción, no para tapar una.
    """
    sistema = yaml.safe_load(io.open(
        os.path.join(RAIZ, "6-fusion", "sistema_de_nombres_era2.yaml"), encoding="utf-8"))
    reglas = {r["id"]: r for r in sistema["reglas"]}
    conservados = {c["nombre"] for c in reglas["g"]["conservados"]}
    assert conservados == {"Manaure", "Kunaro-bana", "Dara-bana"}

    con_sufijo = [n for n in era2.ALL_AGENTS
                  if n.endswith(("-ko", "-sha")) and n not in conservados]
    assert con_sufijo == []
    # y tampoco los otros formantes inventados del casting
    assert [n for n in era2.ALL_AGENTS
            if n.endswith(("-ni", "-nu", "-mana")) and n not in conservados] == []


def test_alias_era1_resuelve_para_los_63():
    """El puente con la era 1: el corpus, la genealogía y las bitácoras de los
    runs de prueba nombran a la gente como se llamaba antes."""
    assert len(era2.ALIAS_ERA1) == len(era2.ALL_AGENTS) == 63
    # todo alias apunta a un agente que existe
    for viejo, nuevo in era2.ALIAS_ERA1.items():
        assert nuevo in era2.ALL_AGENTS, viejo
        assert era2.ALL_AGENTS[nuevo]["alias_era1"] == viejo
    # los tres conservados se apuntan a sí mismos
    for n in ("Manaure", "Kunaro-bana", "Dara-bana"):
        assert era2.resolver_alias(n) == n
    # y los renombrados resuelven
    assert era2.resolver_alias("Shaboro") == "Sawaka"
    assert era2.resolver_alias("Biro-ko") == "Birokoa"
    assert era2.resolver_alias("Paugis-sha") == "Paugis"
    # un nombre que no es de nadie se devuelve tal cual
    assert era2.resolver_alias("Tariwa") == "Tariwa"


def test_las_raices_de_los_nombres_son_caquetio_del_lexicon():
    """Regla a del sistema de nombres: raíz atestiguada (preferida) o
    reconstruida, nunca hipotética ni comparanda."""
    from curiana_lexicon import VOCABULARIO_BASE
    mapa = yaml.safe_load(io.open(
        os.path.join(RAIZ, "6-fusion", "mapa_nombres_era2.yaml"), encoding="utf-8"))
    # La regla a se aplicó el día de NOMBRAR (2026-09-14), con la capa de ese
    # día. El 2026-09-23 (cc.4 / tf.0, opción B) la sigla (E) de Zavala resultó
    # ser Esteves 1989 y 40 voces bajaron de capa; doce de ellas son raíz de un
    # nombre del elenco (Kunaro-bana, Naure, Akaure, Jachos, Wanepe, Tijua,
    # Karama, Saruro, Siwa, Tauta, Waru, Tigi). «El agente no cambia, la voz
    # sí» (issue sigla-E-zavala-canon-2026-09-23.md §7): el nombre se queda, y
    # lo que se exige de esas doce es que la bajada sea LA DECIDIDA, leída de
    # la medición, y no cualquier otra.
    medicion = yaml.safe_load(io.open(
        os.path.join(RAIZ, "6-fusion", "medicion_sigla_E_zavala_2026-09-23.yaml"),
        encoding="utf-8"))
    capa_b = dict(medicion["por_opcion"]["B"]["voces"])
    capa_b["jachos"] = "español-colonial"          # la 6-a, verificada en el DLE
    # La tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»)
    # archivó cuatro voces que son raíz de un nombre: Dunakoa (duna), Ruata
    # (rua), Simaure (sima) y Talata (talata). Mismo criterio: el nombre se
    # queda y la voz sale del habla; lo que se exige es que esté ARCHIVADA por
    # esa tanda —en FUERA_DEL_HABLA, con su capa—, no desaparecida.
    from curiana_lexicon import FUERA_DEL_HABLA
    archivadas_hermanas = {"duna", "rua", "sima", "talata"}
    assert len(mapa["nombres"]) == 63
    for fila in mapa["nombres"]:
        if fila["raiz"] in archivadas_hermanas:
            arch = FUERA_DEL_HABLA.get(fila["raiz"])
            assert arch and "tanda de las hermanas" in arch["archivada"], fila
            assert fila["raiz"] not in VOCABULARIO_BASE, fila
            continue
        entrada = VOCABULARIO_BASE.get(fila["raiz"])
        assert entrada is not None, fila["raiz"]
        if fila["raiz"] in capa_b:
            assert entrada["fuente"] == capa_b[fila["raiz"]], fila
            continue
        assert entrada["fuente"] in ("caquetío-atestiguado", "caquetío-reconstruido"), fila
        esperado = fila.get("nombre") if fila["nombre_nuevo"] == "se conserva" else fila["nombre_nuevo"]
        assert esperado in era2.ALL_AGENTS, esperado


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
    # Birokoa es el de la sal en Tacuato; en la era 1 se llamaba Biro-ko y el
    # nombre se rehizo el 2026-09-14 (biro «sal» + -koa, el formante de Uriacoa).
    orch.call_agent(object(), "Birokoa", state, lexico, ObserverAgent(object(), lexico),
                    orch.MOMENTOS_ESTIMULO["amanecer"])
    s = capturado["system"]
    assert "Eres Birokoa" in s and "Biro-ko" not in s
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
