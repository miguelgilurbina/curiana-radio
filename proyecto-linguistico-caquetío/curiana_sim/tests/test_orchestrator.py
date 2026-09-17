"""Tests del orquestador y del estado del mundo.

Estos módulos (1000+ y 400 líneas) no tenían NINGÚN test: los cuatro bugs de
la auditoría 2026-07-20 vivían ahí y la suite pasaba en verde igualmente.

Cada test de este archivo corresponde a uno de esos bugs y falla si reaparece:

  1. la ventana rotatoria del roster usaba state.turno (solo vale 1 o 2), así
     que de 23 participantes hablaban 12 y los formadores de norma, ninguno.
  2. nadie asignaba state.estacion: los runs transcurrían enteros en "seca".
  3. el pool estacional se partía por índice ([:3]/[3:]) en vez de por la
     clave "estacion", dejando 9 de 25 eventos inalcanzables.
  4. evento["efecto"] no se aplicaba: el mundo quedaba congelado.

No hacen llamadas al LLM ni a Supabase: sustituyen call_agent/director_narrate
y pasan db=None.
"""

import pytest

import curiana_orchestrator_v2 as orch
from curiana_lexicon import LexicoComunitario
from curiana_observer import ObserverAgent
from curiana_state import (
    DIAS_POR_ESTACION,
    ESTACION_DE_DIA,
    EVENTOS_COTIDIANOS,
    EVENTOS_ESTACIONALES,
    ComunidadState,
    estado_inicial_test,
)

RESPUESTA = "Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni."


class _FakeClient:
    """Sustituto del cliente Anthropic: nunca se usa porque call_agent está mockeado."""


@pytest.fixture
def sim(monkeypatch):
    """Entorno de simulación sin LLM ni DB."""
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: RESPUESTA)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    lexico = LexicoComunitario()
    return {
        "client": _FakeClient(),
        "state": estado_inicial_test(),
        "memory": orch.AgentMemory(),
        "lexico": lexico,
        "observer": ObserverAgent(_FakeClient(), lexico),
    }


def _correr(sim, turnos):
    """Corre N turnos y devuelve el Counter de quién habló."""
    from collections import Counter
    hablaron = Counter()
    for _ in range(turnos):
        for i in orch.run_turn(
            sim["client"], sim["state"], sim["memory"], sim["lexico"],
            sim["observer"], verbose=False, db=None, run_id=None,
        ):
            hablaron[i["agent"]] += 1
    return hablaron


# ══════════════════════════════════════════════════════════════════════
# BUG 1 — rotación del roster
# ══════════════════════════════════════════════════════════════════════

def test_la_rotacion_cubre_todo_el_roster(sim, monkeypatch):
    """Sin eventos, la ventana rotatoria debe recorrer el roster completo.

    Regresión: con `state.turno` (1 o 2) la ventana se clavaba en dos
    posiciones y 11 de 23 agentes no hablaban nunca.
    """
    monkeypatch.setattr(orch, "director_select_event", lambda state: None)
    roster = [a for a in orch.PARTICIPANTES_KOINE if a in orch.ALL_AGENTS]

    hablaron = _correr(sim, turnos=2 * len(roster))   # margen de sobra

    mudos = [a for a in roster if a not in hablaron]
    assert not mudos, f"agentes que nunca hablaron: {mudos}"


def test_la_rotacion_incluye_a_los_formadores_de_norma(sim, monkeypatch):
    """Los caquetíos nucleares son el corazón del diseño de koiné: si no
    hablan salvo por evento, la convergencia mide otra cosa."""
    monkeypatch.setattr(orch, "director_select_event", lambda state: None)
    nucleares = {"Manaure", "Shaboro", "Nubiri-sha", "Buio-sha", "Tawaka", "Dare-nu"}

    hablaron = _correr(sim, turnos=12)

    assert nucleares <= set(hablaron), f"faltaron: {nucleares - set(hablaron)}"


# ══════════════════════════════════════════════════════════════════════
# BUG 2 — ciclo estacional
# ══════════════════════════════════════════════════════════════════════

def test_estacion_de_dia_alterna_cada_temporada():
    assert ESTACION_DE_DIA(1) == "seca"
    assert ESTACION_DE_DIA(DIAS_POR_ESTACION) == "seca"
    assert ESTACION_DE_DIA(DIAS_POR_ESTACION + 1) == "lluvias"
    assert ESTACION_DE_DIA(2 * DIAS_POR_ESTACION) == "lluvias"
    assert ESTACION_DE_DIA(2 * DIAS_POR_ESTACION + 1) == "seca"


def test_la_estacion_cambia_al_avanzar_los_dias():
    """Regresión: nadie asignaba `estacion` y todo run era 'seca' perpetua."""
    s = estado_inicial_test()
    vistas = {s.estacion}
    for _ in range(2 * 2 * DIAS_POR_ESTACION + 4):   # algo más de un año
        s.avanzar_turno()
        vistas.add(s.estacion)
    assert vistas == {"seca", "lluvias"}


def test_el_clima_acompana_al_cambio_de_estacion():
    s = ComunidadState(dia=DIAS_POR_ESTACION, turno=2, estacion="seca")
    clima_seca = s.clima
    s.avanzar_turno()          # entra a lluvias
    assert s.estacion == "lluvias"
    assert s.clima != clima_seca


# ══════════════════════════════════════════════════════════════════════
# BUG 3 — filtrado estacional de eventos
# ══════════════════════════════════════════════════════════════════════

def _pool_de(estacion, monkeypatch):
    """Todos los eventos que director_select_event puede devolver en una estación."""
    monkeypatch.setattr(orch.random, "random", lambda: 0.0)   # siempre hay evento
    vistos = set()
    state = ComunidadState(estacion=estacion)
    for _ in range(4000):
        e = orch.director_select_event(state)
        if e:
            vistos.add(e["id"])
    return vistos


def test_los_eventos_de_seca_solo_salen_en_seca(monkeypatch):
    """Regresión: el slicing por índice metía los eventos etiquetados `seca`
    en el pool de lluvias, y viceversa."""
    de_seca = {e["id"] for e in EVENTOS_ESTACIONALES if e.get("estacion") == "seca"}
    assert de_seca <= _pool_de("seca", monkeypatch)
    assert not (de_seca & _pool_de("lluvias", monkeypatch))


def test_los_eventos_de_lluvias_solo_salen_en_lluvias(monkeypatch):
    de_lluvias = {e["id"] for e in EVENTOS_ESTACIONALES if e.get("estacion") == "lluvias"}
    assert de_lluvias <= _pool_de("lluvias", monkeypatch)
    assert not (de_lluvias & _pool_de("seca", monkeypatch))


def test_todos_los_eventos_son_alcanzables_en_algun_momento(monkeypatch):
    """Regresión: 9 de 25 eventos no podían ocurrir en ningún run."""
    definidos = {e["id"] for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES}
    alcanzables = _pool_de("seca", monkeypatch) | _pool_de("lluvias", monkeypatch)
    assert definidos == alcanzables, f"inalcanzables: {sorted(definidos - alcanzables)}"


# ══════════════════════════════════════════════════════════════════════
# BUG 4 — efectos de los eventos sobre el mundo
# ══════════════════════════════════════════════════════════════════════

def test_aplicar_efecto_muta_el_estado():
    s = estado_inicial_test()
    s.aplicar_efecto({"nivel_sal": "abundante", "nivel_tension": "alto"})
    assert s.nivel_sal == "abundante"
    assert s.nivel_tension == "alto"


def test_aplicar_efecto_ignora_claves_desconocidas():
    s = estado_inicial_test()
    s.aplicar_efecto({"no_existe": "x"})
    assert not hasattr(s, "no_existe")


def test_aplicar_efecto_tolera_none_y_vacio():
    s = estado_inicial_test()
    antes = s.nivel_sal
    s.aplicar_efecto(None)
    s.aplicar_efecto({})
    assert s.nivel_sal == antes


def test_un_evento_con_efecto_cambia_el_mundo_en_un_turno(sim, monkeypatch):
    """Regresión: el mundo quedaba congelado en sus valores iniciales y todos
    los agentes recibían el mismo contexto en todos los turnos de todo run."""
    evento = next(e for e in EVENTOS_COTIDIANOS if e["id"] == "raspado_salinar")
    monkeypatch.setattr(orch, "director_select_event", lambda state: evento)
    assert sim["state"].nivel_sal == "bajo"

    _correr(sim, turnos=1)

    assert sim["state"].nivel_sal == "abundante"
    assert "Sal (biro): abundante" in sim["state"].to_context_string()


# ══════════════════════════════════════════════════════════════════════
# El reporte anual (--reporte) depende del calendario
# ══════════════════════════════════════════════════════════════════════

def test_el_cierre_de_anio_coincide_con_un_cambio_de_estacion():
    """El reporte anual se emite en el cambio de estación que cierra el año.

    Regresión: la condición era `state.dia % 120 == 0`, pero las estaciones
    cambian en los días 61, 121, 181… — nunca múltiplos de 120. La bandera
    --reporte no producía nada aunque el calendario funcionara.
    """
    anio_de = lambda dia: (dia - 1) // (2 * DIAS_POR_ESTACION) + 1

    s = estado_inicial_test()
    anterior, anio_visto = s.estacion, anio_de(s.dia)
    cierres = []
    for _ in range(2 * 3 * 2 * DIAS_POR_ESTACION):        # ~3 años
        s.avanzar_turno()
        if s.estacion != anterior:
            anterior = s.estacion
            if anio_de(s.dia) > anio_visto:
                anio_visto = anio_de(s.dia)
                cierres.append(s.dia)

    assert cierres[:3] == [121, 241, 361], f"cierres de año en {cierres[:3]}"


# ══════════════════════════════════════════════════════════════════════
# #42 — un run interrumpido se cierra igual
# ══════════════════════════════════════════════════════════════════════

class _DBQueGraba:
    """Sustituto de CurianaDB que sólo recuerda cómo se cerró el run."""
    def __init__(self):
        self.cierres = []
    def create_run(self, *a, **k):
        return "run-de-prueba"
    def end_run(self, run_id, total_turns, total_days):
        self.cierres.append((run_id, total_turns, total_days))
    def __getattr__(self, nombre):          # save_turn, save_agent_response, …
        return lambda *a, **k: "id"


def test_un_run_interrumpido_se_cierra_igual(sim, monkeypatch):
    """El run 20091e1f se cortó en el turno 57 y quedó con total_turns=0 y
    ended_at NULL porque end_run() iba después del bucle, sin finally. Ahora
    se cierra siempre, con los turnos que de verdad se corrieron."""
    db = _DBQueGraba()
    monkeypatch.setattr(orch, "get_db", lambda: db)
    monkeypatch.setattr(orch, "get_client", lambda *a, **k: _FakeClient())
    monkeypatch.setattr(orch, "huella_de_base", lambda semilla=None: {})
    monkeypatch.setattr(orch, "resumen_huella", lambda h: "")
    monkeypatch.setattr(orch, "guardar_koine", lambda *a, **k: None)
    for cls, metodos in ((ComunidadState, ("save",)), (orch.AgentMemory, ("save",)),
                         (LexicoComunitario, ("save",)),
                         (ObserverAgent, ("save", "exportar_csv", "exportar_neologismos_csv"))):
        for m in metodos:
            monkeypatch.setattr(cls, m, lambda self, *a, **k: None)

    real = orch.run_turn
    llamadas = {"n": 0}
    def run_turn_que_se_corta(*a, **k):
        llamadas["n"] += 1
        if llamadas["n"] == 4:
            raise KeyboardInterrupt
        return real(*a, **k)
    monkeypatch.setattr(orch, "run_turn", run_turn_que_se_corta)

    with pytest.raises(KeyboardInterrupt):
        orch.auto_mode(sim["client"], turnos=10, verbose=False)

    assert len(db.cierres) == 1, "el run interrumpido no se cerró"
    _, total_turns, total_days = db.cierres[0]
    assert total_turns == 3
    assert total_days >= 1


# ══════════════════════════════════════════════════════════════════════
# c6837386 — los préstamos de esfera llegan a la base, aparte
# ══════════════════════════════════════════════════════════════════════

class _DBQueGuardaPrestamos:
    """Sustituto de CurianaDB que recuerda qué se le pidió guardar."""
    def __init__(self):
        self.respuestas = []
        self.prestamos = []
    def save_turn(self, *a, **k):
        return "turno-de-prueba"
    def save_agent_response(self, *a, **k):
        self.respuestas.append(k)
        return "respuesta-de-prueba"
    def save_loanword_uses(self, *a, **k):
        self.prestamos.append(k)
        return len(k.get("words", []))
    def __getattr__(self, nombre):          # save_neologism, update_neologism_status, …
        return lambda *a, **k: "id"


def test_los_prestamos_de_esfera_se_guardan_aparte_y_no_en_words_used(sim, monkeypatch):
    """Run c6837386 (2026-09-16): un préstamo usado por un tier 1 no llegaba a
    la base —`words_used` es `palabras_caquetias`, sólo caquetío— y la difusión
    al tier 2/3 sólo se podía medir re-puntuando `response_text`. Ahora va a
    `loanword_uses` por respuesta, con tier y día, y `words_used` no cambia.

    ⚠ 2026-09-17: el ejemplo era `caiman`, castellano corriente y desde hoy
    `HISPANISMOS_DE_ESFERA`. Se usa `watapana`, que el castellano no dice
    —dice dividivi—: un préstamo de verdad. El test fija lo mismo."""
    from collections import Counter
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: RESPUESTA + " Naya watapana wara.")
    monkeypatch.setattr(orch, "director_select_event", lambda state: None)
    db = _DBQueGuardaPrestamos()
    fallos = Counter()
    dia = sim["state"].dia
    orch.run_turn(sim["client"], sim["state"], sim["memory"], sim["lexico"],
                  sim["observer"], verbose=False, db=db, run_id="run-de-prueba",
                  db_fallos=fallos)
    assert not fallos, dict(fallos)
    assert db.respuestas, "ninguna respuesta se persistió"
    assert len(db.prestamos) == len(db.respuestas), "cada respuesta con préstamo escribe una vez"
    for r, p in zip(db.respuestas, db.prestamos):
        assert "watapana" not in r["words_used"], "el préstamo no contamina words_used"
        assert p["words"] == ["watapana"]
        assert p["response_id"] == "respuesta-de-prueba"
        assert p["turn_id"] == "turno-de-prueba"
        assert p["run_id"] == "run-de-prueba"
        assert p["agent_name"] == r["agent_name"] and p["tier"] == r["tier"]
        assert p["day"] == dia and isinstance(p["turn_num"], int)


class _ClienteQueGraba:
    """Sustituto del cliente supabase: recuerda tabla y filas de cada insert."""
    def __init__(self):
        self.inserts = []
    def table(self, nombre):
        cliente = self
        class _Tabla:
            def insert(self, rows):
                cliente.inserts.append((nombre, rows))
                return self
            def execute(self):
                return None
        return _Tabla()


def test_save_loanword_uses_escribe_la_lengua_real_en_su_tabla():
    """La fila lleva la lengua REAL de la voz (`watapana` es caribe
    continental), y va a `loanword_uses`, nunca a `word_uses`."""
    from curiana_database import CurianaDB
    db = CurianaDB.__new__(CurianaDB)
    db.client = _ClienteQueGraba()
    n = db.save_loanword_uses(response_id="r", run_id="run", turn_id="t",
                              agent_name="Manaure", tier=1, day=3, turn_num=2,
                              words=["watapana"])
    assert n == 1
    (tabla, filas), = db.client.inserts
    assert tabla == "loanword_uses"
    assert (filas[0]["word"] == "watapana"
            and filas[0]["source_language"] == "caribe-continental")
    assert (filas[0]["tier"], filas[0]["day"], filas[0]["turn_num"]) == (1, 3, 2)
    assert db.save_loanword_uses(response_id="r", run_id="run", turn_id="t",
                                 agent_name="Manaure", tier=1, day=3, turn_num=2,
                                 words=[]) == 0
    assert len(db.client.inserts) == 1, "sin préstamos no se escribe nada"


# ══════════════════════════════════════════════════════════════════════
# 2026-09-16 — la forma acuñada queda en boca de quien la acuña
# ══════════════════════════════════════════════════════════════════════
# `score_linguistico()` sólo reconoce `lexico.palabras_activas()` (base +
# adoptados) y una acuñación recién propuesta no está ahí, así que
# `palabras_caquetias` —y con ella `words_used` y `word_uses`— no la traía. El
# primer uso que constaba era el del ADOPTANTE, que puede ser del otro nodo:
# 29 de 40 acuñaciones de la era 2 (72,5%, analizar_nodos.py). Eso invierte las
# rutas de contagio que se leen de `word_uses`.

CON_ACUNACION = RESPUESTA + " [kuru-bacoa: kuru+-bacoa = la arboleda]."


def test_el_acunador_es_el_primer_usuario_registrado_de_su_forma(sim, monkeypatch):
    from collections import Counter

    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: CON_ACUNACION)
    monkeypatch.setattr(orch, "director_select_event", lambda state: None)
    db = _DBQueGuardaPrestamos()
    fallos = Counter()
    inter = orch.run_turn(sim["client"], sim["state"], sim["memory"], sim["lexico"],
                          sim["observer"], verbose=False, db=db, run_id="run-de-prueba",
                          db_fallos=fallos)
    assert not fallos, dict(fallos)
    assert inter and db.respuestas
    primera = db.respuestas[0]
    # El scorer NO la ve (no está en `palabras_activas()`), así que el
    # orquestador la pasa aparte: el merge —y su lengua— los hace la capa de
    # base, que es la que escribe `word_uses`.
    assert "kuru-bacoa" not in primera["words_used"]
    assert primera["coined_words"] == ["kuru-bacoa"], (
        "la forma acuñada no llega a la base en boca de su acuñador")
    assert primera["agent_name"] == inter[0]["agent"]
    # Todos dicen lo mismo (el agente es un mock), así que a partir del
    # segundo la forma YA está adoptada en el léxico y el scorer sí la ve: es
    # exactamente la asimetría que arreglamos. Nunca puede contarse dos veces.
    for r in db.respuestas:
        veces = r["words_used"].count("kuru-bacoa") + r["coined_words"].count("kuru-bacoa")
        assert veces == 1, r["agent_name"]
    adoptantes = [r for r in db.respuestas if "kuru-bacoa" in r["words_used"]]
    assert adoptantes, "sin adopción no hay contraste que medir"


def test_save_agent_response_escribe_la_acunacion_como_caquetio():
    """La fila de `word_uses` de una acuñación lleva `caquetío` declarado:
    no está en el lexicón y `word_source_language()` la dejaría en NULL — el
    agujero que el backfill de 2026-08-06 cerró para las formas flexionadas.
    Y los `pct_*` no se mueven: `language_composition()` sólo cuenta
    VOCABULARIO_BASE."""
    from curiana_database import CurianaDB

    class _ClienteConId(_ClienteQueGraba):
        """Como `_ClienteQueGraba`, pero `execute()` devuelve el id que
        `save_agent_response` necesita para colgar de él los `word_uses`."""
        def table(self, nombre):
            cliente = self

            class _Resultado:
                data = [{"id": "resp-1"}]

            class _Tabla:
                def insert(self, rows):
                    cliente.inserts.append((nombre, rows))
                    return self

                def execute(self):
                    return _Resultado()
            return _Tabla()

    def _guardar(coined):
        db = CurianaDB.__new__(CurianaDB)
        db.client = _ClienteConId()
        db.save_agent_response(
            turn_id="t", run_id="run", agent_name="Manaure", ethnicity="caquetío",
            tier=1, response_text="…", score=7.0, words_used=["biro", "kali"],
            aspects_used=["completivo"], neologisms_proposed=len(coined),
            coined_words=coined)
        return dict(db.client.inserts)

    con = _guardar(["kuru-bacoa"])
    sin = _guardar([])
    fila_resp = con["agent_responses"]
    assert "kuru-bacoa" in fila_resp["words_used"]
    assert fila_resp["pct_caquetio"] == sin["agent_responses"]["pct_caquetio"]

    por_palabra = {f["word"]: f for f in con["word_uses"]}
    assert por_palabra["kuru-bacoa"]["source_language"] == "caquetío"
    assert por_palabra["kuru-bacoa"]["agent_name"] == "Manaure"
    assert "kuru-bacoa" not in {f["word"] for f in sin["word_uses"]}
    # Una sola fila por acuñación, aunque llegue repetida o ya en words_used.
    assert len([f for f in con["word_uses"] if f["word"] == "kuru-bacoa"]) == 1
    repe = _guardar(["kuru-bacoa", "kuru-bacoa", "biro"])
    assert repe["agent_responses"]["words_used"].count("kuru-bacoa") == 1
    assert repe["agent_responses"]["words_used"].count("biro") == 1
