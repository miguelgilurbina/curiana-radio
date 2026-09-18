"""La escena en el motor: ESTAR (PR 2 del diseño del 2026-09-17).

Lo que estos tests vigilan, en orden:

  (a) LA ERA 1 SIGUE BYTE A BYTE. Se capturan los prompts de un turno con
      cliente falso, con el módulo de escena enchufado y con él apagado, y se
      comparan carácter a carácter.
  (b) LA ERA 2 SIN --escena, también byte a byte. La escena es un BRAZO, no un
      parche: sin el flag, el prompt es el de hoy.
  (c) CON --escena: [Aquí estás] en los 72 prompts de un día de seis turnos,
      ≤ 200 caracteres, sin ningún marcador sin resolver, y los presentes que
      el bloque nombra son exactamente los que escena_de() pone en ese lugar.
  (d) es_dia_de_capubana: cadencia 3 → días 3, 6, 9, y ese día los 63 están en
      el cerro los seis momentos.
  (e) la config del run sella `escena` y `capubana_cada`.
  (f) --continuar con OTRO brazo se niega (no se mezclan cadenas).
  (g) el ensayo sin API imprime las 63 × 6 × 3 escenas con su largo.

Sin LLM y sin Supabase: se sustituye `_invoke` y se usa un doble de base.
"""
import os
import random
import subprocess
import sys

import pytest

import curiana_agents_era2 as era2
import curiana_escena as esc
import curiana_escena_era2 as tabla
import curiana_orchestrator_v2 as orch
from curiana_lexicon import LexicoComunitario
from curiana_observer import ObserverAgent
from curiana_state import ComunidadState, estado_inicial, estado_inicial_test

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPUESTA = "Taya wana-ka arima wara kari. [kuru-bacoa: kuru+-bacoa = la arboleda]."
# El call_agent de verdad, guardado al importar: `_capturar` lo sustituye por
# un espía y un test puede llamarla dos veces, así que no vale releerlo del
# módulo (el espía de la primera llamada envolvería al de la segunda).
_CALL_AGENT = orch.call_agent


class _Cliente:
    pass


class _DB:
    """Doble de base: guarda la config del run y las presencias si se lo piden."""

    def __init__(self, con_presencias=False, config_anterior=None):
        self.config = None
        self.presencias = []
        self.turnos = []
        self.respuestas = []
        self._config_anterior = config_anterior
        if con_presencias:
            self.save_presencias = self._save_presencias

    def _save_presencias(self, **k):
        self.presencias.append(k)

    def save_agent_response(self, **k):
        self.respuestas.append(k)
        return f"resp-{len(self.respuestas)}"

    def create_run(self, *a, **k):
        self.config = k.get("config")
        return "run-de-prueba"

    def save_turn(self, **k):
        self.turnos.append(k)
        return f"turn-{len(self.turnos)}"

    def get_run(self, run_id):
        return {"id": run_id, "config": self._config_anterior} if self._config_anterior else None

    def end_run(self, *a, **k):
        pass

    def __getattr__(self, nombre):
        if nombre.startswith("_") or nombre == "save_presencias":
            raise AttributeError(nombre)
        return lambda *a, **k: "id"


# ══════════════════════════════════════════════════════════════════════
# utilidades: capturar los prompts de un día entero
# ══════════════════════════════════════════════════════════════════════

def _capturar(monkeypatch, state, *, roster, agentes_por_turno, turnos,
              con_modulo=True, era=None, db=None, verbose=False):
    """Corre `turnos` turnos con cliente falso y devuelve un prompt por
    llamada a call_agent (el primero: el de la 1ª pasada, antes del rescate).

    `con_modulo=False` deja el orquestador como si curiana_escena no
    existiera: es el control del test de byte a byte.

    La muestra del lexicón se sortea con el RNG global, así que se fija antes
    de cada corrida: si no, dos capturas del mismo prompt nunca serían
    iguales y el test de byte a byte no mediría nada."""
    random.seed(20260917)
    if era is not None:
        monkeypatch.setattr(orch, "ALL_AGENTS", era)
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    if not con_modulo:
        monkeypatch.setattr(orch, "escena_de", lambda s: {})
        monkeypatch.setattr(orch, "ambito_de", lambda a, s: None)
        monkeypatch.setattr(orch, "bloque_aqui_estas", lambda a, s, **k: "")
        monkeypatch.setattr(orch, "volcado_de_escena", lambda s, e=None: "")
        monkeypatch.setattr(orch, "es_dia_de_capubana", lambda s, c=None: False)

    capturas, actual = [], [None]
    monkeypatch.setattr(orch, "_invoke",
                        lambda c, system, user: capturas.append(
                            {"agente": actual[0], "system": system, "user": user}
                        ) or RESPUESTA)
    primeros = []

    def espia(client, agent_name, *a, **k):
        actual[0] = agent_name
        antes = len(capturas)
        salida = _CALL_AGENT(client, agent_name, *a, **k)
        primeros.append(capturas[antes])
        return salida
    monkeypatch.setattr(orch, "call_agent", espia)

    lexico = LexicoComunitario()
    observer = ObserverAgent(_Cliente(), lexico)
    memoria = orch.AgentMemory()
    for _ in range(turnos):
        orch.run_turn(_Cliente(), state, memoria, lexico, observer,
                      verbose=verbose, db=db, run_id="run-1" if db else None,
                      agentes_por_turno=agentes_por_turno, roster=list(roster))
    return primeros


def _estado_era2(escena=False, cada=0, dia=1):
    s = estado_inicial("PARAGUANÁ")
    s.turnos_por_dia = 6
    s.dia = dia
    s.escena = escena
    s.capubana_cada = cada
    s.evento_del_turno = None          # el semilla habla del día 1 y aquí estorba
    return s


# ══════════════════════════════════════════════════════════════════════
# (a) la era 1, byte a byte
# ══════════════════════════════════════════════════════════════════════

def test_a_la_era_1_es_byte_a_byte_con_y_sin_el_modulo(monkeypatch):
    """En CURIANA no hay escena: `ambito_de` devuelve None, `escena_de` {} y
    ningún bloque nuevo entra al prompt. Importar curiana_escena no puede
    mover un carácter."""
    roster = orch.roster_de_habla("koine")[:6]
    con = _capturar(monkeypatch, estado_inicial_test(), roster=roster,
                    agentes_por_turno=6, turnos=2, con_modulo=True)
    sin = _capturar(monkeypatch, estado_inicial_test(), roster=roster,
                    agentes_por_turno=6, turnos=2, con_modulo=False)
    assert [c["agente"] for c in con] == [c["agente"] for c in sin]
    for c, s in zip(con, sin):
        assert c["system"] == s["system"], c["agente"]
        assert c["user"] == s["user"], c["agente"]
    assert all("[Tu ubicación]: " in c["system"] for c in con)
    assert not any("[Aquí estás]" in c["system"] for c in con)


def test_la_era_1_no_escribe_ubicaciones_override(monkeypatch):
    """Cuatro lectores y cero escrituras: en la era 1 sigue igual."""
    state = estado_inicial_test()
    _capturar(monkeypatch, state, roster=orch.roster_de_habla("koine")[:4],
              agentes_por_turno=4, turnos=2)
    assert state.ubicaciones_override == {} and state.escena_del_turno == {}


def test_ambito_de_devuelve_none_en_curiana():
    s = estado_inicial_test()
    s.escena = True                      # aunque se pida, en CURIANA no hay
    assert esc.ambito_de("Manaure", s) is None
    assert esc.escena_de(s) == {}
    assert esc.bloque_aqui_estas("Manaure", s) == ""
    assert esc.volcado_de_escena(s) == ""


# ══════════════════════════════════════════════════════════════════════
# (b) la era 2 SIN --escena, byte a byte
# ══════════════════════════════════════════════════════════════════════

def test_b_la_era_2_sin_escena_es_byte_a_byte(monkeypatch):
    """La escena es un brazo, no un parche: sin el flag, el prompt de
    Paraguaná es exactamente el de hoy."""
    roster = list(era2.ALL_AGENTS)[:8]
    con = _capturar(monkeypatch, _estado_era2(escena=False), roster=roster,
                    agentes_por_turno=8, turnos=2, era=era2.ALL_AGENTS,
                    con_modulo=True)
    sin = _capturar(monkeypatch, _estado_era2(escena=False), roster=roster,
                    agentes_por_turno=8, turnos=2, era=era2.ALL_AGENTS,
                    con_modulo=False)
    assert [c["agente"] for c in con] == [c["agente"] for c in sin]
    for c, s in zip(con, sin):
        assert c["system"] == s["system"], c["agente"]
    assert all("[Tu ubicación]: " in c["system"] for c in con)
    assert not any("[Aquí estás]" in c["system"] for c in con)


def test_sin_escena_no_se_escribe_la_ubicacion_ni_se_agrupa_al_director(monkeypatch):
    state = _estado_era2(escena=False)
    _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS)[:4],
              agentes_por_turno=4, turnos=1, era=era2.ALL_AGENTS)
    assert state.ubicaciones_override == {} and state.escena_del_turno == {}


# ══════════════════════════════════════════════════════════════════════
# (c) con --escena
# ══════════════════════════════════════════════════════════════════════

def test_c_aqui_estas_en_los_72_prompts_de_un_dia(monkeypatch):
    """Seis turnos × doce voces = 72 prompts, y los 72 traen [Aquí estás]
    dentro de presupuesto, sin marcador sin resolver, y con los presentes que
    la escena pone en ese lugar."""
    state = _estado_era2(escena=True, cada=0)
    roster = orch.roster_de_habla("todos")
    monkeypatch.setattr(orch, "ALL_AGENTS", era2.ALL_AGENTS)
    monkeypatch.setattr(orch, "ROSTER_NUCLEO", era2.ROSTER_NUCLEO)
    roster = [a for a in era2.ALL_AGENTS]
    escenas = []
    real_escena = orch.escena_de
    monkeypatch.setattr(orch, "escena_de",
                        lambda s: escenas.append((s.dia, s.momento, real_escena(s)))
                        or escenas[-1][2])
    prompts = _capturar(monkeypatch, state, roster=roster, agentes_por_turno=12,
                        turnos=6, era=era2.ALL_AGENTS)

    assert len(prompts) == 72, len(prompts)
    por_turno = {(d, m): e for d, m, e in escenas}
    for i, p in enumerate(prompts):
        s = p["system"]
        bloque = next(l for l in s.splitlines() if l.startswith("[Aquí estás]"))
        assert len(bloque) <= esc.PRESUPUESTO, (p["agente"], len(bloque))
        assert "{" not in bloque and "}" not in bloque, bloque
        assert "[Tu ubicación]" not in s
        # el momento del turno al que pertenece este prompt
        dia, momento, escena = escenas[i // 12]
        lugar = escena[p["agente"]]
        assert esc.glosa_de(lugar) in bloque, (p["agente"], lugar, bloque)
        presentes = esc.presentes_en(lugar, escena, sin=p["agente"])
        if not presentes:
            assert "No hay nadie más aquí" in bloque
        elif "Contigo está " in bloque:
            assert bloque.endswith(f"Contigo está {presentes[0]}.") and len(presentes) == 1
        elif "Contigo están" in bloque:
            # lista completa: son exactamente los que la escena pone allí
            dichos = (bloque.split("Contigo están ", 1)[1].rstrip(".")
                      .replace(" y ", ", ").split(", "))
            assert sorted(dichos) == presentes, (p["agente"], lugar)
        else:
            # lista recortada: el número es el real y los nombres son suyos
            assert f"Contigo hay {len(presentes)}" in bloque, bloque
            for n in bloque.split(": ", 2)[-1].rstrip("…").split(", "):
                assert n in presentes, (n, lugar)
    assert len(por_turno) == 6


def test_c_las_72_respuestas_se_guardan_con_su_lugar(monkeypatch):
    """`agent_responses.lugar` existe desde #155 y `save_agent_response` lo
    acepta, pero el orquestador no se lo pasaba: el día 1 de la serie C (run
    b7bc51dc) cerró con **0 de 72** filas con lugar mientras `presencias`
    tenía las 378. Lo que se guarda es el ÁMBITO del hablante —la misma puerta
    `ambito_de` que filtra lo que ve y que ya se le declaró al léxico—, no el
    nodo: Humohumo (GUARANAO) y Bajari (AMUAY) andan el mismo camino."""
    db = _DB()
    state = _estado_era2(escena=True, cada=0)
    monkeypatch.setattr(orch, "ROSTER_NUCLEO", era2.ROSTER_NUCLEO)
    escenas = []
    real_escena = orch.escena_de
    monkeypatch.setattr(orch, "escena_de",
                        lambda s: escenas.append(real_escena(s)) or escenas[-1])
    prompts = _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS),
                        agentes_por_turno=12, turnos=6, era=era2.ALL_AGENTS, db=db)

    assert len(prompts) == 72 and len(db.respuestas) == 72
    assert all(r["lugar"] for r in db.respuestas), "0 de 72 es el bug de b7bc51dc"
    for i, r in enumerate(db.respuestas):
        # el lugar de la escena de SU turno, y un lugar de la tabla decidida
        assert r["lugar"] == escenas[i // 12][r["agent_name"]], r["agent_name"]
        assert r["lugar"] in tabla.LUGARES, r["lugar"]


def test_c_sin_escena_la_respuesta_se_guarda_sin_lugar(monkeypatch):
    """La era 2 sin el flag y la era 1: `lugar=None`. Y `lugar=None` es lo
    mismo que no pasarlo —`save_agent_response` no menciona la columna—, así
    que lo que se le envía a PostgREST es byte a byte la fila de antes de la
    migración (tests/test_presencias.py lo compara)."""
    db = _DB()
    _capturar(monkeypatch, _estado_era2(escena=False), roster=list(era2.ALL_AGENTS)[:6],
              agentes_por_turno=6, turnos=2, era=era2.ALL_AGENTS, db=db)
    assert len(db.respuestas) == 12
    assert all(r["lugar"] is None for r in db.respuestas)

    era1 = _DB()
    _capturar(monkeypatch, estado_inicial_test(),
              roster=orch.roster_de_habla("koine")[:6],
              agentes_por_turno=6, turnos=2, db=era1)
    assert era1.respuestas
    assert all(r["lugar"] is None for r in era1.respuestas)


def test_run_turn_escribe_ubicaciones_override_para_los_63(monkeypatch):
    """El campo que llevaba cuatro lectores y cero escrituras. Y son los 63,
    no los 12 que hablan: un mapa con 12 de 63 no es un mundo."""
    state = _estado_era2(escena=True)
    _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS)[:12],
              agentes_por_turno=12, turnos=1, era=era2.ALL_AGENTS)
    assert len(state.ubicaciones_override) == 63
    assert state.ubicaciones_override == state.escena_del_turno
    assert set(state.ubicaciones_override) == set(era2.ALL_AGENTS)
    assert all(l in tabla.LUGARES for l in state.ubicaciones_override.values())


def test_el_bloque_cabe_en_200_en_las_1134_escenas():
    """63 agentes × 6 momentos × 3 períodos, y el día de Capubana aparte, que
    es el peor caso (62 co-presentes)."""
    combos = esc.combinaciones()
    assert len(combos) == 63 * 6 * 3 == 1134
    for cada, dia in ((0, 1), (3, 3)):
        for agente, momento, periodo in combos:
            st = esc.EstadoDeEnsayo(dia=dia, momento=momento, estacion=periodo,
                                    capubana_cada=cada)
            b = esc.bloque_aqui_estas(agente, st)
            assert b.startswith("[Aquí estás]: "), b
            assert len(b) <= esc.PRESUPUESTO, (agente, momento, periodo, len(b))
            assert "{" not in b and "…" not in b.split("Contigo")[0]


def test_el_director_recibe_las_intervenciones_agrupadas_por_lugar(monkeypatch):
    """Decisión 6 → A: un Director por turno, cero llamadas más, pero con las
    intervenciones agrupadas por lugar."""
    prompts = {}

    class _C:
        class messages:
            @staticmethod
            def create(**k):
                prompts["texto"] = k["messages"][0]["content"]
                return type("R", (), {"content": [type("T", (), {"text": "cierre"})()]})()

    state = _estado_era2(escena=True)
    state.escena_del_turno = esc.escena_de(state)
    inter = [{"agent": a, "response": "taya naa-ka"} for a in ("Birokoa", "Kasebo", "Sawaka")]
    orch.director_narrate(_C(), state, inter)
    texto = prompts["texto"]
    for a in ("Birokoa", "Kasebo", "Sawaka"):
        lugar = state.escena_del_turno[a]
        assert f"[{esc.glosa_de(lugar)}]" in texto, (a, lugar)

    # sin escena, el resumen es el de siempre: una lista plana
    state.escena_del_turno = {}
    orch.director_narrate(_C(), state, inter)
    assert "[" not in prompts["texto"].split("Interacciones:")[1]


def test_save_presencias_se_llama_solo_si_existe(monkeypatch):
    """Interfaz con el PR 3 (el agente de la base): se llama si el método
    está, y no se rompe nada si todavía no."""
    db = _DB(con_presencias=True)
    state = _estado_era2(escena=True)
    _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS)[:4],
              agentes_por_turno=4, turnos=2, era=era2.ALL_AGENTS, db=db)
    assert len(db.presencias) == 2
    p = db.presencias[0]
    assert p["run_id"] == "run-1" and p["dia"] == 1 and p["momento"] == "amanecer"
    assert len(p["escena"]) == 63

    # sin el método: el turno corre igual
    sin = _DB(con_presencias=False)
    _capturar(monkeypatch, _estado_era2(escena=True), roster=list(era2.ALL_AGENTS)[:4],
              agentes_por_turno=4, turnos=1, era=era2.ALL_AGENTS, db=sin)
    assert sin.turnos

    # y sin escena no se escribe ninguna presencia
    db2 = _DB(con_presencias=True)
    _capturar(monkeypatch, _estado_era2(escena=False), roster=list(era2.ALL_AGENTS)[:4],
              agentes_por_turno=4, turnos=1, era=era2.ALL_AGENTS, db=db2)
    assert db2.presencias == []


def test_el_volcado_no_rompe_el_silencioso(monkeypatch, capsys):
    """PR 8: el volcado va dentro del bloque verboso. Con --silencioso
    (verbose=False) no se imprime, y con él sí."""
    state = _estado_era2(escena=True)
    _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS)[:2],
              agentes_por_turno=2, turnos=1, era=era2.ALL_AGENTS, verbose=False)
    assert "escena del turno" not in capsys.readouterr().out

    _capturar(monkeypatch, _estado_era2(escena=True), roster=list(era2.ALL_AGENTS)[:2],
              agentes_por_turno=2, turnos=1, era=era2.ALL_AGENTS, verbose=True)
    salida = capsys.readouterr().out
    assert "escena del turno · amanecer:" in salida
    assert "Tacuato:salinar: Birokoa" in salida       # el del biro, en sus charcas


# ══════════════════════════════════════════════════════════════════════
# (d) el día de Capubana
# ══════════════════════════════════════════════════════════════════════

def test_d_es_dia_de_capubana():
    """Cadencia 3 → días 3, 6, 9. Cadencia 0 → nunca."""
    def dia(n, cada=3):
        return esc.EstadoDeEnsayo(dia=n, capubana_cada=cada)
    assert [n for n in range(1, 13) if esc.es_dia_de_capubana(dia(n))] == [3, 6, 9, 12]
    assert [n for n in range(1, 13) if esc.es_dia_de_capubana(dia(n, 4))] == [4, 8, 12]
    assert not any(esc.es_dia_de_capubana(dia(n, 0)) for n in range(1, 13))
    # el argumento manda sobre el estado
    assert esc.es_dia_de_capubana(dia(4, 3), cada=4)
    assert not esc.es_dia_de_capubana(dia(4, 3), cada=3)
    # la víspera es el día de antes
    assert [n for n in range(1, 13) if esc.es_vispera_de_capubana(dia(n))] == [2, 5, 8, 11]


def test_el_dia_de_capubana_estan_los_63_los_seis_momentos():
    for momento in tabla.MOMENTOS:
        st = esc.EstadoDeEnsayo(dia=3, momento=momento, capubana_cada=3)
        escena = esc.escena_de(st)
        assert len(escena) == 63
        assert set(escena.values()) == {"Capubana"}, momento
    # el día antes y el día después, no
    for d in (2, 4):
        st = esc.EstadoDeEnsayo(dia=d, momento="mediodia", capubana_cada=3)
        assert len(set(esc.escena_de(st).values())) > 1


def test_la_vispera_la_esposa_principal_anda_el_camino_de_la_alianza():
    """«La esposa principal viene por él y el aporte de AMUAY al cerro baja
    por él» — el camino Moruy–Caseto, la víspera de la convergencia."""
    quien = tabla.TRAVESIA["filas"][0]["agentes"][0]
    for momento in ("mañana", "mediodia", "tarde"):
        vispera = esc.escena_de(esc.EstadoDeEnsayo(dia=2, momento=momento, capubana_cada=3))
        normal = esc.escena_de(esc.EstadoDeEnsayo(dia=1, momento=momento, capubana_cada=3))
        assert vispera[quien] == "camino:Moruy-Caseto", momento
        assert normal[quien] != "camino:Moruy-Caseto", momento
    # al amanecer y de noche no anda caminos
    assert esc.escena_de(esc.EstadoDeEnsayo(dia=2, momento="noche",
                                            capubana_cada=3))[quien] == "Moruy"


def test_sin_cadencia_no_hay_capubana_ni_travesia():
    for d in range(1, 10):
        escena = esc.escena_de(esc.EstadoDeEnsayo(dia=d, momento="mediodia",
                                                  capubana_cada=0))
        assert set(escena.values()) != {"Capubana"}


# ══════════════════════════════════════════════════════════════════════
# (e) y (f): la config y la cadena
# ══════════════════════════════════════════════════════════════════════

def _auto(monkeypatch, tmp_path, db, **kw):
    from curiana_perfiles import cargar_perfil
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(orch, "get_db", lambda: db)
    monkeypatch.setattr(orch, "get_client", lambda run_id=None: _Cliente())
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: RESPUESTA)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "huella_de_base",
                        lambda semilla=None: {"motor_sucio": False, "semilla": semilla})
    kw.setdefault("perfil", cargar_perfil("base"))
    kw.setdefault("verbose", False)
    return orch.auto_mode(_Cliente(), kw.pop("turnos", 1), **kw)


def test_e_la_config_sella_escena_y_capubana_cada(monkeypatch, tmp_path):
    db = _DB()
    _auto(monkeypatch, tmp_path, db, turnos=1, agentes_por_turno=2,
          roster_nombre="todos", turnos_por_dia=1, semilla=7,
          escena=True, capubana_cada=4)
    assert db.config["escena"] is True and db.config["capubana_cada"] == 4

    _auto(monkeypatch, tmp_path, db, turnos=1, agentes_por_turno=2,
          roster_nombre="todos", turnos_por_dia=1, semilla=7)
    assert db.config["escena"] is False and db.config["capubana_cada"] is None


def test_f_continuar_con_otro_brazo_se_niega(monkeypatch, tmp_path):
    """Una escena no puede entrar ni salir a mitad de cadena (diseño §5.4)."""
    db = _DB()
    _auto(monkeypatch, tmp_path, db, turnos=1, agentes_por_turno=2,
          roster_nombre="todos", turnos_por_dia=1, semilla=1)   # sin escena
    with pytest.raises(SystemExit) as e:
        _auto(monkeypatch, tmp_path, db, turnos=1, agentes_por_turno=2,
              roster_nombre="todos", turnos_por_dia=1, semilla=1,
              continuar=True, escena=True)
    assert "otro brazo" in str(e.value).lower()
    # y con el mismo brazo, sigue
    _auto(monkeypatch, tmp_path, db, turnos=1, agentes_por_turno=2,
          roster_nombre="todos", turnos_por_dia=1, semilla=1, continuar=True)
    assert db.config["continuado_desde"] == "run-de-prueba"


def test_f_la_config_del_run_anterior_manda_sobre_el_estado():
    """El brazo se lee de la config, que es donde queda sellado; el estado en
    disco es el respaldo."""
    state = ComunidadState(run_anterior="abcdef12", escena=False, capubana_cada=0)
    db = _DB(config_anterior={"escena": True, "capubana_cada": 3})
    with pytest.raises(SystemExit) as e:
        orch.comprobar_brazo_de_escena(db, state, False, 3)
    assert "config del run abcdef12" in str(e.value)
    orch.comprobar_brazo_de_escena(db, state, True, 3)        # el mismo: pasa
    with pytest.raises(SystemExit):                           # otra cadencia: no
        orch.comprobar_brazo_de_escena(db, state, True, 4)


def test_f_sin_base_se_cae_al_estado_en_disco():
    state = ComunidadState(run_anterior="abcdef12", escena=True, capubana_cada=3)
    with pytest.raises(SystemExit) as e:
        orch.comprobar_brazo_de_escena(_DB(), state, False, 0)
    assert "curiana_state.json" in str(e.value)
    orch.comprobar_brazo_de_escena(_DB(), state, True, 3)


# ══════════════════════════════════════════════════════════════════════
# (g) el ensayo sin API
# ══════════════════════════════════════════════════════════════════════

def test_g_el_ensayo_imprime_las_1134_escenas():
    r = subprocess.run([sys.executable, "curiana_escena.py"], cwd=SIM,
                       capture_output=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    salida = r.stdout.decode("utf-8")
    lineas = [l for l in salida.splitlines() if "[Aquí estás]" in l]
    assert len(lineas) == 1134, len(lineas)
    assert "1134 escenas (63 agentes × 6 momentos × 3 períodos)" in salida
    assert f"tope {esc.PRESUPUESTO}" in salida
    assert "escena del turno · mediodia:" in salida


def test_el_estado_lleva_el_brazo_y_lo_hereda_continuar():
    """Los tres campos van en to_dict(), así que --continuar los hereda, y un
    JSON viejo que no los trae carga con el brazo apagado."""
    s = ComunidadState(escena=True, capubana_cada=3)
    s.escena_del_turno = {"Manaure": "Moruy"}
    d = s.to_dict()
    assert d["escena"] is True and d["capubana_cada"] == 3
    assert ComunidadState.from_dict(d).escena_del_turno == {"Manaure": "Moruy"}
    for clave in ("escena", "capubana_cada", "escena_del_turno"):
        d.pop(clave)
    viejo = ComunidadState.from_dict(d)
    assert viejo.escena is False and viejo.capubana_cada == 0
    assert viejo.escena_del_turno == {}
