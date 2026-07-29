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
