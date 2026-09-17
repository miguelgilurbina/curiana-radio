"""Los eventos del catálogo, dichos para el elenco de la era 2 (2026-09-16).

Medido antes del arreglo (python curiana_eventos.py): el catálogo nombraba a la
era 1 en `descripcion`/`nombre` de la mayoría de los eventos, casi todos los
`agentes_involucrados` tenían nombre viejo o foráneo, y run_turn conservaba
sólo a los tres que no cambiaron de nombre (Manaure, Kunaro-bana, Dara-bana)
porque filtraba con `a in ALL_AGENTS` sin resolver el alias.

Los tests corren con el elenco de la era 1 (CURIANA_ELENCO no está puesta): el
alias se importa de curiana_agents_era2 directamente y la era 2 real se
comprueba en un subproceso con la variable puesta.
"""
import copy
import os
import subprocess
import sys

import curiana_agents_era2 as era2
import curiana_orchestrator_v2 as orch
from curiana_eventos import (
    EVENTOS_SOLO_CON_FORANEOS,
    MARCOS_FUERA_ERA2,
    PSEUDO_AGENTES,
    REESCRITURAS_ERA2,
    alias_del_elenco,
    catalogo_para_elenco,
    decir_para_el_mundo,
    elenco_era1,
    evento_para_elenco,
    medir,
    nombres_de_la_era_1,
    residuos_de_la_era_1,
    sustituir_nombres,
)
from curiana_state import (
    EVENTOS_COTIDIANOS,
    EVENTOS_ESTACIONALES,
    PERIODOS_ERA2,
    TENSIONES_ERA2,
    ComunidadState,
    estado_inicial,
    estado_inicial_paraguana,
    estado_inicial_test,
)

ALIAS = era2.ALIAS_ERA1
ERA1 = elenco_era1()
FORANEOS = frozenset(n for n, a in ERA1.items() if orch.es_foraneo(a))
SIN_EQUIV = frozenset(set(ERA1) - set(ALIAS) - FORANEOS)
VIEJOS = frozenset(k for k, v in ALIAS.items() if k != v) | FORANEOS | SIN_EQUIV
TODOS = EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES
SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _evento(id_):
    return next(e for e in TODOS if e["id"] == id_)


def _era2(ev):
    return evento_para_elenco(ev, "era2", ALIAS, FORANEOS, sin_equivalente=SIN_EQUIV)


# ── la era 1 no se toca ───────────────────────────────────────────────

def test_la_era_1_devuelve_el_evento_intacto():
    for ev in TODOS:
        assert evento_para_elenco(ev, "era1", ALIAS, FORANEOS) is ev
    cot, est = catalogo_para_elenco("era1", ALIAS, FORANEOS)
    assert [e["id"] for e in cot] == [e["id"] for e in EVENTOS_COTIDIANOS]
    assert [e["id"] for e in est] == [e["id"] for e in EVENTOS_ESTACIONALES]
    assert alias_del_elenco("era1") == {} and alias_del_elenco("era2") == ALIAS


def test_adaptar_no_muta_el_catalogo():
    antes = copy.deepcopy(TODOS)
    catalogo_para_elenco("era2", ALIAS, FORANEOS, SIN_EQUIV)
    assert TODOS == antes


# ── la era 2: ni nombres viejos, ni foráneos, ni marco étnico ─────────

def test_ningun_evento_de_la_era_2_nombra_a_la_era_1_ni_a_los_foraneos():
    cot, est = catalogo_para_elenco("era2", ALIAS, FORANEOS, SIN_EQUIV)
    assert cot and est
    for e in cot + est:
        for campo in ("nombre", "descripcion"):
            assert not nombres_de_la_era_1(e[campo], VIEJOS), (e["id"], campo, e[campo])
            for marca in ("Guaycar", "Jirajara", "serrano", "Caquetíos"):
                assert marca not in e[campo], (e["id"], marca)
        assert e["agentes_involucrados"], e["id"]      # ningún evento se queda sin nadie
        for a in e["agentes_involucrados"]:
            assert a in era2.ALL_AGENTS or a in PSEUDO_AGENTES, (e["id"], a)
            assert a not in FORANEOS and a not in SIN_EQUIV
    m = medir(ALIAS, FORANEOS, SIN_EQUIV)
    assert m["eventos"] == len(TODOS) and m["menciones_en_texto"] > 0 and m["foraneos"] > 0


def test_los_nombres_se_traducen_respetando_guiones_y_mayusculas():
    assert sustituir_nombres("Biro-ko y los suyos; el biro brilla.", ALIAS) == "Birokoa y los suyos; el biro brilla."
    assert sustituir_nombres("Sha-korie, Shaboro y Sha.", ALIAS) == "Amaka, Sawaka y Jaiata."
    assert sustituir_nombres("Korie-ko y Kori; Piri-sha y Piri.", ALIAS) == "Patapati y Chakamba; Uria y Ucibo."
    assert sustituir_nombres("Manaure decide.", ALIAS) == "Manaure decide."
    assert nombres_de_la_era_1("Nubiri-sha y Nubi", {"Nubi", "Nubiri-sha"}) == ["Nubiri-sha", "Nubi"]


def test_raspado_salinar_lo_hace_birokoa():
    ev = _era2(_evento("raspado_salinar"))
    assert "Birokoa y los suyos" in ev["descripcion"] and "Biro-ko" not in ev["descripcion"]
    assert ev["agentes_involucrados"] == ["Birokoa", "Buriche", "Urari", "Karama"]
    assert ev["efecto"] == {"nivel_sal": "abundante"}
    assert ev["nombre"] == "Raspado de la sal en el salinar"


def test_pesca_mala_pierde_el_marco_etnico_y_al_foraneo():
    ev = _era2(_evento("pesca_mala"))
    assert ev["descripcion"] == "Poco pescado. Unos culpan al calor; otros, al mal ritual."
    assert ev["agentes_involucrados"] == ["Jachos", "Sawaka"]        # Tariwa, foráneo, fuera


def test_llegada_nabaraka_cae_y_el_trueque_se_queda():
    assert "llegada_nabaraka" in EVENTOS_SOLO_CON_FORANEOS
    assert _era2(_evento("llegada_nabaraka")) is None
    trueque = _era2(_evento("trueque_visitantes_plaza"))
    assert trueque is not None and "Jirajara" not in trueque["descripcion"]
    assert "los de fuera muestran ocre" in trueque["descripcion"] and "Karebe vigila" in trueque["descripcion"]
    assert trueque["agentes_involucrados"] == ["Birokoa", "Karebe"]
    cot, est = catalogo_para_elenco("era2", ALIAS, FORANEOS, SIN_EQUIV)
    ids = {e["id"] for e in cot + est}
    assert ids == {e["id"] for e in TODOS} - {"llegada_nabaraka"}


def test_el_caribe_llega_por_mar_y_chiriware_sale_de_la_frase():
    """etnia-008: el caribe llega por mar, no reside. Chiriware es linaje en la era 2."""
    raid = _era2(_evento("rumor_raid_caribe"))
    assert raid["descripcion"] == "Dara-bana vio canoas extrañas al este. Se activa el perímetro."
    assert raid["agentes_involucrados"] == ["Dara-bana", "Manaure", "Kasebo", "guerreros"]
    guardia = _era2(_evento("vigilancia_perimetro_amanecer"))
    assert guardia["descripcion"].startswith("Antes de que aclare, se reparten los puestos de guardia")
    assert "los Caribes" in guardia["descripcion"] and "Chiriware" not in guardia["descripcion"]
    assert guardia["agentes_involucrados"] == ["Ruata", "Bajari", "Dara-bana"]


def test_las_islas_se_quedan_sin_kadushi_ni_watapana():
    canoa = _era2(_evento("canoa_islas_llega"))
    assert canoa["descripcion"] == "Una canoa llega desde Aruba con bienes y noticias."
    assert canoa["agentes_involucrados"] == ["Manaure"]
    salida = _era2(_evento("watapana_parte_islas"))
    assert salida["nombre"] == "Una expedición parte a las islas"
    assert salida["agentes_involucrados"] == ["Isiro", "Manaure"]
    crecida = _era2(_evento("crecida_buco"))
    assert "Patapati y los del buko caminan" in crecida["descripcion"]
    assert crecida["agentes_involucrados"] == ["Patapati", "Tebekoa", "Dunakoa"]


def test_un_nombre_sin_traduccion_tumba_el_evento():
    ev = {"id": "x", "nombre": "Prueba", "descripcion": "Buko-ko riega el conuco.",
          "agentes_involucrados": ["Manaure"], "efecto": {}}
    assert _era2(ev) is None
    ev2 = dict(ev, descripcion="Tariwa pesca solo.")
    assert _era2(ev2) is None


def test_cada_reescritura_declarada_se_usa():
    textos = " ".join(e["descripcion"] + " " + e["nombre"] for e in TODOS)
    for viejo in REESCRITURAS_ERA2:
        assert viejo in textos, viejo


# ── el texto libre: lo que llega al Director ──────────────────────────
# El catálogo no era la única puerta. En el día 3 (run 0193873d), con los
# eventos ya traducidos (#138), el Director escribió «Los Caquetíos y Guaycarí
# se juntan…» porque su propia nota del día 2 —texto libre, sin traducir— lo
# decía. Es la reflexión real de aquel día, recortada.

NOTA_DEL_DIA_2 = (
    "El alisio no aflojó y los peces tampoco vinieron. Lo que cambió fue el miedo, "
    "y eso dividió las explicaciones: los Guaycarí culpan el calor, los Caquetíos "
    "el rezo faltante. La palabra que prendió fue tüshi-juri, viento frío del este. "
    "Biro-ko subió la sal al cerro antes de que cayera la noche."
)


def test_la_era_1_no_toca_el_texto_libre():
    for mundo in ("CURIANA", None, ""):
        assert decir_para_el_mundo(NOTA_DEL_DIA_2, mundo) == NOTA_DEL_DIA_2


def test_en_paraguana_se_traduce_el_nombre_y_se_cae_la_frase_con_el_marco():
    dicho = decir_para_el_mundo(NOTA_DEL_DIA_2, "PARAGUANÁ")
    assert not residuos_de_la_era_1(dicho, VIEJOS), dicho
    assert "Guaycarí" not in dicho and "Caquetíos" not in dicho
    assert "Birokoa subió la sal al cerro" in dicho          # el alias traduce, no borra
    assert "El alisio no aflojó" in dicho                    # lo limpio se queda entero
    assert "tüshi-juri" in dicho                             # y la palabra del día también
    # sólo se cae la frase que lleva el marco: 1 de 4
    assert len(dicho) < len(NOTA_DEL_DIA_2) and dicho.count(".") == 3


def test_los_marcos_declarados_son_los_de_la_decision_y_el_caribe_no_esta():
    """Guaycarí, jirajara y gayón salieron de la era 2 (2026-09-14); el caribe
    se queda porque llega por mar y no reside (etnia-008)."""
    fuera = [p.pattern for p in MARCOS_FUERA_ERA2]
    assert len(fuera) == 4 and not any("arib" in p for p in fuera)
    for texto, esperado in (
        ("Los guaycaríes llegaron.", ["guaycaríes"]),
        ("Un jirajara de la sierra.", ["jirajara"]),
        ("Los gayones bajaron.", ["gayones"]),
        ("Vienen de la Curiana.", ["Curiana"]),
        ("Una canoa caribe por el norte.", []),
        ("Nadie durmió bien.", []),
    ):
        assert residuos_de_la_era_1(texto, VIEJOS) == esperado, texto


def test_el_texto_se_filtra_frase_a_frase_y_linea_a_linea():
    """Una reflexión son seis oraciones: no se tira entera por una. Y la línea
    de estado tiene estructura: se filtra dentro de cada línea."""
    texto = "[PARAGUANÁ — Tiempo de Viento]\nDía 3, Turno 6 (noche). Biro-ko raspa.\nLos Guaycarí."
    dicho = decir_para_el_mundo(texto, "PARAGUANÁ")
    assert dicho.splitlines() == ["[PARAGUANÁ — Tiempo de Viento]",
                                  "Día 3, Turno 6 (noche). Birokoa raspa."]
    assert decir_para_el_mundo("Los Guaycarí pescan.", "PARAGUANÁ") == ""


def test_el_estado_semilla_no_lleva_nombres_de_la_era_1_a_paraguana():
    """estado_inicial_test() abre TODO run que no continúa con «Shaboro salió
    de su choza… Buio-sha lo vio desde lejos» en evento_del_turno: dos nombres
    de la era 1 que llegaban a los 63 agentes y al Director el día 1."""
    s = estado_inicial_test()
    s.fijar_mundo("PARAGUANÁ")
    crudo = s.to_context_string()
    assert sorted(set(nombres_de_la_era_1(crudo, VIEJOS))) == ["Buio-sha", "Shaboro"]
    dicho = decir_para_el_mundo(crudo, "PARAGUANÁ")
    assert not residuos_de_la_era_1(dicho, VIEJOS)
    assert "Día 1, Turno 1 (amanecer)" in dicho and "Tiempo de Viento" in dicho
    # la era 1 sigue viendo su estado entero
    assert decir_para_el_mundo(estado_inicial_test().to_context_string(), "CURIANA") \
        == estado_inicial_test().to_context_string()


def test_call_agent_no_le_pasa_al_agente_el_mundo_de_la_era_1(monkeypatch):
    """El bloque del mundo del prompt del agente también pasa por el traductor:
    en Paraguaná ningún agente lee «Shaboro salió de su choza»."""
    from curiana_lexicon import LexicoComunitario
    from curiana_observer import ObserverAgent

    sistemas = []
    monkeypatch.setattr(orch, "_invoke",
                        lambda client, system, msg: sistemas.append(system) or "Taya wana-ka.")
    lexico = LexicoComunitario()
    observer = ObserverAgent(object(), lexico)
    for mundo, debe_estar in (("CURIANA", True), ("PARAGUANÁ", False)):
        st = estado_inicial_test()
        st.fijar_mundo(mundo)
        sistemas.clear()
        orch.call_agent(object(), "Manaure", st, lexico, observer, "¿Qué haces?")
        assert ("Shaboro salió de su choza" in sistemas[0]) is debe_estar, mundo


# ── la otra puerta: el MENSAJE del agente (2026-09-17) ────────────────
# El bloque del mundo iba traducido desde #143, pero el user_message no: el
# estímulo de un turno con evento es «[Situación]: {evento}» y se mandaba
# crudo. Medido en el run b06f57ea (serie B, era 2): 23 de 72 respuestas del
# día 1 dicen «Shaboro» y 16 «Buio-sha» —12 de 12 en el turno 2— mientras el
# Director decía «Sawaka».

def _espiar_prompts(monkeypatch) -> list:
    """Cada (system, mensaje) que sale hacia el cliente."""
    prompts = []
    monkeypatch.setattr(
        orch, "_invoke",
        lambda client, system, msg: prompts.append((system, msg)) or "Taya wana-ka.")
    return prompts


def test_el_mensaje_del_agente_tambien_pasa_por_el_traductor(monkeypatch):
    from curiana_lexicon import LexicoComunitario
    from curiana_observer import ObserverAgent

    prompts = _espiar_prompts(monkeypatch)
    lexico = LexicoComunitario()
    observer = ObserverAgent(object(), lexico)
    situacion = f"[Situación]: {estado_inicial_test().evento_del_turno}. ¿Cómo reaccionas?"
    for mundo, debe_estar in (("CURIANA", True), ("PARAGUANÁ", False)):
        st = estado_inicial_test()
        st.fijar_mundo(mundo)
        prompts.clear()
        orch.call_agent(object(), "Manaure", st, lexico, observer, situacion)
        mensaje = prompts[0][1]
        assert ("Shaboro" in mensaje) is debe_estar, (mundo, mensaje)
        assert ("Buio-sha" in mensaje) is debe_estar, (mundo, mensaje)
    # el alias traduce, no borra: la situación sigue llegando, dicha de la era 2
    assert "Sawaka salió de su choza" in prompts[0][1]


def test_un_mensaje_que_no_sobrevive_entero_cae_en_el_momento_del_dia(monkeypatch):
    """Un estímulo que es todo marco de la era 1 se queda en nada: el agente
    recibe el momento del día antes que un mensaje vacío (la API lo rechaza)."""
    from curiana_lexicon import LexicoComunitario
    from curiana_observer import ObserverAgent

    prompts = _espiar_prompts(monkeypatch)
    lexico = LexicoComunitario()
    observer = ObserverAgent(object(), lexico)
    st = estado_inicial_test()
    st.fijar_mundo("PARAGUANÁ")
    orch.call_agent(object(), "Manaure", st, lexico, observer, "Los Guaycarí pescan.")
    assert prompts[0][1] == orch.MOMENTOS_ESTIMULO[st.momento].replace("{lugar}", "la Curiana")


_TURNO_ERA2 = """
import json
import curiana_orchestrator_v2 as orch
from curiana_lexicon import LexicoComunitario
from curiana_observer import ObserverAgent
from curiana_state import estado_inicial, estado_inicial_test

prompts = []
orch._invoke = lambda client, system, msg: prompts.append([system, msg]) or "Taya wana-ka."
orch.director_narrate = lambda *a, **k: "(narración)"
orch.director_select_event = lambda state: None
lexico = LexicoComunitario()


class _DB:                      # como _DBQueGraba en test_era2_motor.py
    turnos = []
    def save_turn(self, **k):
        _DB.turnos.append(k)
        return "turn-1"
    def __getattr__(self, n):
        return lambda *a, **k: "id"


def turno(state):
    prompts.clear()
    orch.run_turn(object(), state, orch.AgentMemory(), lexico,
                  ObserverAgent(object(), lexico), verbose=False,
                  db=_DB(), run_id="run-1", agentes_por_turno=4,
                  roster=orch.roster_de_habla("todos"))
    return list(prompts)


# (a) el estado de la ERA 1 con el mundo de la 2: lo que corrió hasta el
#     2026-09-17 y lo que puede traer un estado continuado de antes.
viejo = estado_inicial_test()
viejo.fijar_mundo(orch.MUNDO)
# (b) el estado que escribe ahora estado_inicial(MUNDO).
nuevo = estado_inicial(orch.MUNDO)
print(json.dumps({
    "mundo": orch.MUNDO,
    "elenco": orch.ELENCO,
    "desde_la_era_1": turno(viejo),
    "desde_paraguana": turno(nuevo),
    "turnos": _DB.turnos,
}))
"""


def test_un_turno_con_el_elenco_era2_no_manda_ningun_nombre_de_la_era_1():
    """La garantía de punta a punta, con la era 2 REAL (subproceso con
    CURIANA_ELENCO=era2): ni el system prompt ni el mensaje de ningún agente
    llevan «Shaboro» o «Buio-sha», ni arrancando del estado nuevo ni
    arrancando del de la era 1. Y `turns.event_description` tampoco.

    Con el elenco de la era 1 este turno no se puede medir: la persona de
    Manaure nombra a Shaboro en su propio system_prompt, que es suyo y no es
    texto del mundo."""
    env = dict(os.environ, CURIANA_ELENCO="era2", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-c", _TURNO_ERA2], cwd=SIM, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    import json
    salida = json.loads(r.stdout.strip().splitlines()[-1])
    assert salida["mundo"] == "PARAGUANÁ" and salida["elenco"] == "era2"
    for arranque in ("desde_la_era_1", "desde_paraguana"):
        prompts = salida[arranque]
        assert prompts, arranque
        texto = " ".join(t for p in prompts for t in p)
        for marca in ("Shaboro", "Buio-sha", "Biro-ko", "Guaycar", "la Curiana"):
            assert marca not in texto, (arranque, marca)
    # el evento semilla de Paraguaná sí llega, entero y dicho de su mundo
    mensajes = " ".join(p[1] for p in salida["desde_paraguana"])
    assert "Tiempo de Viento" in mensajes and "el Capubana" in mensajes
    # y lo que se graba en `turns` es lo mismo, sin nombres viejos
    grabados = [t["event_description"] for t in salida["turnos"]]
    assert grabados and all(g is None or "Shaboro" not in g for g in grabados), grabados


# ── el estado inicial por mundo (2026-09-17) ──────────────────────────

def test_la_era_1_arranca_byte_a_byte_como_siempre():
    assert estado_inicial("CURIANA").to_dict() == estado_inicial_test().to_dict()
    assert estado_inicial().to_dict() == estado_inicial_test().to_dict()
    assert estado_inicial("un mundo que no existe").to_dict() == estado_inicial_test().to_dict()


def test_paraguana_arranca_sin_nada_de_la_era_1():
    """Ni en el evento, ni en la escena, ni en las tensiones, ni en el clima."""
    s = estado_inicial_paraguana()
    assert s is not estado_inicial_paraguana()          # no comparte estado mutable
    assert (s.mundo, s.dia, s.turno, s.estacion, s.momento) == \
        ("PARAGUANÁ", 1, 1, "viento", "amanecer")
    assert s.clima == PERIODOS_ERA2["viento"]["clima_base"]
    todo = " ".join([s.evento_del_turno or "", *s.agentes_en_escena,
                     *s.tensiones_activas, *(t["causa"] for t in s.tensiones_activas.values())])
    assert not residuos_de_la_era_1(todo, VIEJOS), todo
    for nombre in s.agentes_en_escena:
        assert nombre in era2.ALL_AGENTS, nombre
    # el estado entero, tal como lo lee el agente, ya está dicho para la era 2
    crudo = s.to_context_string()
    assert decir_para_el_mundo(crudo, "PARAGUANÁ") == crudo


def test_la_escena_del_dia_1_es_el_manaure_y_un_apopo_por_casa():
    """Sale del módulo GENERADO, no de una lista a mano: las cinco casas del
    casting tienen voz el primer amanecer y los dos nodos están en escena."""
    s = estado_inicial_paraguana()
    fichas = era2.ALL_AGENTS
    casas = {fichas[n]["casa"] for n in s.agentes_en_escena}
    assert casas == {a["casa"] for a in fichas.values() if a.get("casa")}
    assert {fichas[n]["nodo"] for n in s.agentes_en_escena} == {"GUARANAO", "AMUAY"}
    roles = [fichas[n]["rol_en_la_casa"] for n in s.agentes_en_escena]
    assert roles[0].startswith("Manaure") and set(roles[1:]) == {"apopo"}


def test_las_tensiones_de_la_era_2_son_las_que_el_canon_declara():
    """Sólo pares de gente que existe, y cada una con la línea de 6-fusion/
    que la sostiene. El `nivel` es canon-simulación y va declarado."""
    s = estado_inicial_paraguana()
    assert s.tensiones_activas == TENSIONES_ERA2 and TENSIONES_ERA2
    for par, t in TENSIONES_ERA2.items():
        assert t["fuente"].startswith("6-fusion/"), par
        assert t["nivel"] in ("bajo", "medio", "alto"), par
    # el par se escribe con los nombres de la era 2, que están en el elenco
    for nombres in (("Sawaka", "Paugis"), ("Manaure", "Kiwakoa"),
                    ("Kunaro-bana", "Jachos"), ("Bajari", "Kasebo")):
        assert "-".join(nombres) in TENSIONES_ERA2
        for n in nombres:
            assert n in era2.ALL_AGENTS, n


def test_el_evento_semilla_de_paraguana_cita_el_canon():
    """Ninguna frase a mano: la del amanecer es LITERAL de clima_era2.yaml y
    los sitios son los del canon (sitios_era2.yaml), no inventados."""
    from curiana_mundo import clima, sitios
    evento = estado_inicial_paraguana().evento_del_turno
    assert clima()["frases_del_cargador"]["viento"]["momentos"]["amanecer"] in evento
    for sitio in ("Tacuato", "Carirubana", "Moruy", "Capubana"):
        assert sitio in sitios() and sitio in evento, sitio
    assert "Curiana" not in evento and "salinar" not in evento


# ── el orquestador pasa por el elenco ─────────────────────────────────

def test_director_select_event_en_la_era_1_es_el_pool_de_siempre(monkeypatch):
    monkeypatch.setattr(orch.random, "random", lambda: 0.0)
    ids = {orch.director_select_event(ComunidadState(estacion="seca"))["id"] for _ in range(600)}
    assert "llegada_nabaraka" in ids and "raspado_salinar" in ids


def test_director_select_event_con_la_era_2_no_nombra_a_la_era_1(monkeypatch):
    monkeypatch.setattr(orch.random, "random", lambda: 0.0)
    monkeypatch.setattr(orch, "_eventos_del_elenco",
                        lambda: catalogo_para_elenco("era2", ALIAS, FORANEOS, SIN_EQUIV))
    st = ComunidadState(dia=1)
    st.fijar_mundo("PARAGUANÁ")
    vistos = {}
    for _ in range(600):
        e = orch.director_select_event(st)
        vistos[e["id"]] = e
    assert "llegada_nabaraka" not in vistos and "gran_cosecha_sal" in vistos
    for e in vistos.values():
        assert not nombres_de_la_era_1(e["descripcion"], VIEJOS), e["id"]


def test_con_curiana_elenco_era2_el_orquestador_traduce_de_verdad():
    """La era 2 real, en un subproceso con la variable puesta: el catálogo del
    elenco no nombra a la era 1 y todos los involucrados están en ALL_AGENTS."""
    codigo = (
        "import curiana_orchestrator_v2 as o, curiana_agents_era2 as e, json\n"
        "from curiana_eventos import nombres_de_la_era_1, elenco_era1\n"
        "cot, est = o._eventos_del_elenco()\n"
        "era1 = elenco_era1(); alias = e.ALIAS_ERA1\n"
        "viejos = {k for k, v in alias.items() if k != v} | (set(era1) - set(alias))\n"
        "malos = [x['id'] for x in cot + est if nombres_de_la_era_1(x['descripcion'], viejos)]\n"
        "fuera = [(x['id'], a) for x in cot + est for a in x['agentes_involucrados']\n"
        "         if a not in o.ALL_AGENTS and a not in ('toda_la_comunidad', 'guerreros')]\n"
        "print(json.dumps({'n': len(cot) + len(est), 'malos': malos, 'fuera': fuera,\n"
        "                  'mundo': o.MUNDO, 'system': o.DIRECTOR_SYSTEM}))\n"
    )
    env = dict(os.environ, CURIANA_ELENCO="era2", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-c", codigo], cwd=SIM, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert r.returncode == 0, r.stderr[-2000:]
    import json
    salida = json.loads(r.stdout.strip().splitlines()[-1])
    assert salida["n"] == len(TODOS) - len(EVENTOS_SOLO_CON_FORANEOS)
    assert salida["malos"] == [] and salida["fuera"] == []
    assert salida["mundo"] == "PARAGUANÁ" and "de Paraguaná" in salida["system"]
