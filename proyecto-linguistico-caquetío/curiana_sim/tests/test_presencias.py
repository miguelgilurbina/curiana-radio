"""Tests de la ESCENA en la base — `presencias` y `agent_responses.lugar`.

La capa 1 de «existir en el mundo» (decisión de Miguel 2026-09-17) pone a los
**63** agentes en un lugar cada momento del día, no sólo a los 12 que hablan. Lo
que hay que vigilar aquí es exactamente eso y tres cosas más:

  - que un turno escriba 63 presencias y un día 378 (6 momentos), y que se
    puedan LEER de vuelta;
  - que un run sin escena no escriba **nada** —ni una fila, ni un viaje a la
    base—, que es lo que mantiene la era 1 byte a byte;
  - que las 63 filas salgan en **una** inserción y no en 63 llamadas;
  - que `save_agent_response` escriba la columna `lugar` cuando viene y no la
    mencione siquiera cuando no, para que la fila de un run sin escena sea la de
    antes de la migración.

Sin Supabase y sin red: el mock guarda en memoria (con las MISMAS filas, porque
comparte `filas_de_presencias` con `CurianaDB`), y para lo que sólo existe en
`CurianaDB` —la forma del insert— hay un cliente falso de quince líneas, como
`tests/test_cadena.py` sustituye el lector de la base.
"""

from types import SimpleNamespace

import pytest

import curiana_database as cdb
from curiana_database import CurianaDB, CurianaDBMock, filas_de_presencias

RUN = "11111111-1111-1111-1111-111111111111"
MOMENTOS = ["amanecer", "mañana", "mediodía", "tarde", "anochecer", "noche"]

# 63 agentes, como el elenco de la era 2. Los nombres son sintéticos a
# propósito: lo que se mide es la aritmética de la escena, no el casting.
ESCENA_63 = {f"agente{i:02d}": ("Moruy" if i % 2 else "Tacuato:orilla")
             for i in range(1, 64)}


def _turno(n: int) -> str:
    return f"22222222-2222-2222-2222-{n:012d}"


# ══════════════════════════════════════════════════════════════════════
# Las filas: la pieza pura que comparten la base y el mock
# ══════════════════════════════════════════════════════════════════════

def test_una_fila_por_agente_con_su_lugar_y_su_momento():
    filas = filas_de_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)
    assert len(filas) == 63
    primera = filas[0]
    assert primera["run_id"] == RUN and primera["turn_id"] == _turno(1)
    assert (primera["day"], primera["turn_num"]) == (1, 1)
    assert primera["momento"] == "amanecer"
    assert {f["agent_name"] for f in filas} == set(ESCENA_63)
    assert {f["lugar"] for f in filas} == {"Moruy", "Tacuato:orilla"}


def test_un_agente_sin_lugar_no_escribe_fila():
    """La escena puede no ubicar a alguien; inventarle un lugar sería peor."""
    escena = {"Sawaka": "Capubana", "Hayo": "", "Bajari": None}
    filas = filas_de_presencias(RUN, _turno(1), 1, 1, "noche", escena)
    assert [f["agent_name"] for f in filas] == ["Sawaka"]


def test_el_nodo_sale_del_elenco_activo(monkeypatch):
    """El nodo se congela con la fila y se resuelve del elenco ACTIVO, no de una
    tabla propia: el módulo del elenco es generado y se regenera."""
    import curiana_agents
    monkeypatch.setitem(curiana_agents.ALL_AGENTS, "Fulanito", {"nodo": "AMUAY"})
    filas = filas_de_presencias(RUN, _turno(1), 1, 1, "tarde",
                                {"Fulanito": "Caseto", "NoExiste": "Moruy"})
    nodos = {f["agent_name"]: f["nodo"] for f in filas}
    assert nodos["Fulanito"] == "AMUAY"
    # Quien no está en el elenco activo —toda la era 1— no tiene nodo, y eso se
    # guarda como None en vez de adivinarse.
    assert nodos["NoExiste"] is None


# ══════════════════════════════════════════════════════════════════════
# El mock: escribir y leer un turno, y un día entero
# ══════════════════════════════════════════════════════════════════════

def test_el_mock_escribe_y_lee_63_presencias_por_turno():
    db = CurianaDBMock()
    escritas = db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)
    assert escritas == 63
    leidas = db.presencias_de(RUN)
    assert len(leidas) == 63
    assert {f["agent_name"] for f in leidas} == set(ESCENA_63)
    assert all(f["momento"] == "amanecer" for f in leidas)


def test_un_dia_son_378_presencias():
    """63 agentes × 6 momentos. Es la cifra del diseño (§2 capa 1) y la razón de
    que la tabla exista: con los 12 que hablan no hay mundo que dibujar."""
    db = CurianaDBMock()
    total = sum(db.save_presencias(RUN, _turno(t), 1, t, momento, ESCENA_63)
                for t, momento in enumerate(MOMENTOS, start=1))
    assert total == 378
    assert len(db.presencias_de(RUN)) == 378
    # y los seis momentos están, cada uno con los 63
    por_momento = {}
    for f in db.presencias_de(RUN):
        por_momento.setdefault(f["momento"], set()).add(f["agent_name"])
    assert sorted(por_momento) == sorted(MOMENTOS)
    assert all(len(a) == 63 for a in por_momento.values())


def test_la_lectura_por_cadena_junta_los_runs_y_solo_esos():
    """En la era 2 un run es UN día: lo que se mira es la cadena."""
    otro = "33333333-3333-3333-3333-333333333333"
    ajeno = "44444444-4444-4444-4444-444444444444"
    db = CurianaDBMock()
    db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)
    db.save_presencias(otro, _turno(2), 2, 1, "amanecer", ESCENA_63)
    db.save_presencias(ajeno, _turno(3), 1, 1, "amanecer", ESCENA_63)
    cadena = db.presencias_de_cadena([RUN, otro])
    assert len(cadena) == 126
    assert {f["run_id"] for f in cadena} == {RUN, otro}


def test_un_run_sin_escena_no_escribe_nada():
    """La era 1, o un run con `--sin-escena`: `escena_de()` devuelve {} y esto
    no deja rastro. Es la garantía de que la escena no cambia lo que ya había."""
    db = CurianaDBMock()
    assert db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", {}) == 0
    assert db.presencias_de(RUN) == []
    assert db.presencias_de_cadena([RUN]) == []


# ══════════════════════════════════════════════════════════════════════
# `save_agent_response` con y sin lugar
# ══════════════════════════════════════════════════════════════════════

RESPUESTA = dict(
    turn_id=_turno(1), run_id=RUN, agent_name="Birokoa", ethnicity="caquetío",
    tier=1, response_text="taya naa-ka biro-ana", score=7.0,
    words_used=["taya"], aspects_used=["completivo"],
)


def test_el_mock_guarda_el_lugar_de_la_respuesta_cuando_viene():
    db = CurianaDBMock()
    db.save_agent_response(**RESPUESTA, lugar="Tacuato:salinar")
    db.save_agent_response(**RESPUESTA)
    assert [r["lugar"] for r in db.respuestas] == ["Tacuato:salinar", None]


class _Tabla:
    def __init__(self, registro, nombre):
        self.registro, self.nombre = registro, nombre

    def insert(self, filas):
        self.registro.setdefault(self.nombre, []).append(filas)
        return self

    def execute(self):
        return SimpleNamespace(data=[{"id": "55555555-5555-5555-5555-555555555555"}])


class _ClienteFalso:
    """Lo mínimo de supabase-py que tocan estas dos escrituras."""
    def __init__(self):
        self.inserciones: dict[str, list] = {}

    def table(self, nombre):
        return _Tabla(self.inserciones, nombre)


def _db_falsa() -> tuple[CurianaDB, _ClienteFalso]:
    """Una `CurianaDB` sin Supabase: `__init__` exige credenciales y aquí lo que
    se mira es la FORMA del insert, no la conexión."""
    db = CurianaDB.__new__(CurianaDB)
    cliente = _ClienteFalso()
    db.client = cliente
    db._run_id = None
    return db, cliente


def test_sin_lugar_la_fila_es_la_de_antes_de_la_migracion():
    db, cliente = _db_falsa()
    db.save_agent_response(**RESPUESTA)
    fila = cliente.inserciones["agent_responses"][0]
    assert "lugar" not in fila, "un run sin escena no debe mencionar la columna"


def test_lugar_none_es_lo_mismo_que_no_pasarlo():
    """Desde el arreglo de b7bc51dc el orquestador pasa SIEMPRE
    `lugar=ambito_de(...)`, que sin escena —la era 1, o la era 2 sin el flag—
    es None. La fila que sale hacia PostgREST tiene que ser la misma que
    antes, carácter a carácter: si `None` escribiera la columna, la era 1
    dejaría de ser byte a byte en la base."""
    db, cliente = _db_falsa()
    db.save_agent_response(**RESPUESTA)
    db.save_agent_response(**RESPUESTA, lugar=None)
    sin_pasarlo, con_none = cliente.inserciones["agent_responses"]
    assert sin_pasarlo == con_none
    assert "lugar" not in con_none


def test_con_lugar_la_columna_se_escribe():
    db, cliente = _db_falsa()
    db.save_agent_response(**RESPUESTA, lugar="Tacuato:salinar")
    assert cliente.inserciones["agent_responses"][0]["lugar"] == "Tacuato:salinar"


# ══════════════════════════════════════════════════════════════════════
# Una inserción por lote, no 63 llamadas
# ══════════════════════════════════════════════════════════════════════

def test_las_63_presencias_van_en_una_sola_insercion():
    """Un día son 378 filas; a llamada por agente serían 378 viajes a
    PostgREST."""
    db, cliente = _db_falsa()
    assert db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63) == 63
    lotes = cliente.inserciones["presencias"]
    assert len(lotes) == 1
    assert len(lotes[0]) == 63


def test_sin_escena_la_base_ni_se_toca():
    db, cliente = _db_falsa()
    assert db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", {}) == 0
    assert cliente.inserciones == {}


def test_el_fallo_de_escritura_se_propaga_para_que_lo_cuente_el_llamador():
    """Como `save_loanword_uses`: el `Counter` por tabla vive en el orquestador
    (`db_fallos["presencias"]`), y perder escrituras en silencio corrompe el
    análisis — 62 presencias en vez de 63 siguen pareciendo un mundo."""
    db, _ = _db_falsa()

    class _Rota(_ClienteFalso):
        def table(self, nombre):
            raise RuntimeError("PostgREST caído")

    db.client = _Rota()
    with pytest.raises(RuntimeError):
        db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)


def test_el_mock_construye_las_mismas_filas_que_la_base():
    """Si el mock y `CurianaDB` divergieran, estos tests dejarían de decir nada
    de lo que se guarda de verdad."""
    db, cliente = _db_falsa()
    db.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)
    mock = CurianaDBMock()
    mock.save_presencias(RUN, _turno(1), 1, 1, "amanecer", ESCENA_63)
    assert cliente.inserciones["presencias"][0] == mock.presencias


def test_el_lector_de_la_base_pagina():
    """PostgREST corta en `max_rows`=1000 y una consulta sin `.range()` se
    trunca EN SILENCIO (la trampa que ya se comió a `lexicon`). Tres días de
    escena son 1.134 filas."""
    assert cdb.PAGINA_POSTGREST == 1000

    class _Paginador:
        """Devuelve 1.134 filas en dos páginas, como PostgREST."""
        def __init__(self):
            self.rangos = []

        def table(self, nombre):
            return self

        def select(self, *a, **kw):
            return self

        def in_(self, *a, **kw):
            return self

        def order(self, *a, **kw):
            return self

        def range(self, desde, hasta):
            self.rangos.append((desde, hasta))
            self._lote = [{"agent_name": f"a{i}"} for i in range(desde, min(hasta + 1, 1134))]
            return self

        def execute(self):
            return SimpleNamespace(data=self._lote)

    db = CurianaDB.__new__(CurianaDB)
    db.client = paginador = _Paginador()
    filas = db.presencias_de(RUN)
    assert len(filas) == 1134
    assert paginador.rangos == [(0, 999), (1000, 1999)]


def test_sin_runs_no_se_consulta():
    db = CurianaDB.__new__(CurianaDB)
    db.client = None          # si consultara, reventaría aquí
    assert db.presencias_de_cadena([]) == []
