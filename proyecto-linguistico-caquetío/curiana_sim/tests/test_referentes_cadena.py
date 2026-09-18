"""La competencia léxica sigue su secuencia de referentes de un día al
siguiente (--continuar). Hasta el 2026-09-17 cada run empezaba
REFERENTES_NOVEDOSOS de cero y un día de seis turnos sólo llegaba al
primero: los tres días de la serie A nombraron «las cuentas brillantes».

Y desde el 2026-09-18, la DISPUTA misma viaja: `auto_mode` recuperaba la
secuencia de referentes pero creaba una `CompetenciaLexica()` nueva, así que
ninguna competencia podía durar más de un día (día 1 de la serie C)."""
import itertools
import json

import pytest

import curiana_orchestrator_v2 as orch
from curiana_koine import REFERENTES_NOVEDOSOS
from curiana_orchestrator_v2 import referentes_pendientes_de
from curiana_perfiles import cargar_perfil
from curiana_state import ComunidadState, estado_inicial


def test_un_run_nuevo_empieza_la_secuencia():
    state = estado_inicial("CURIANA")
    assert state.referentes_introducidos == []
    pendientes = referentes_pendientes_de(state)
    assert [r["id"] for r in pendientes] == [r["id"] for r in REFERENTES_NOVEDOSOS]


def test_un_run_que_continua_sigue_donde_la_dejo_el_dia_anterior():
    state = estado_inicial("CURIANA")
    state.referentes_introducidos = ["cuentas_vidrio"]          # el día 1 ya las nombró
    pendientes = referentes_pendientes_de(state)
    ids = [r["id"] for r in pendientes]
    assert "cuentas_vidrio" not in ids
    assert ids[0] == "cometa"                                    # el día 2 recibe el cometa
    assert len(ids) == len(REFERENTES_NOVEDOSOS) - 1


def test_el_orden_del_catalogo_se_respeta_aunque_falten_varios():
    state = estado_inicial("CURIANA")
    state.referentes_introducidos = ["cuentas_vidrio", "cometa", "eclipse"]
    ids = [r["id"] for r in referentes_pendientes_de(state)]
    assert ids[:2] == ["fiebre_manchas", "metal_amarillo"]


def test_devuelve_copias_y_no_toca_el_catalogo():
    state = estado_inicial("CURIANA")
    pendientes = referentes_pendientes_de(state)
    pendientes[0]["desc"] = "otra cosa"
    pendientes.pop(0)
    assert REFERENTES_NOVEDOSOS[0]["id"] == "cuentas_vidrio"
    assert REFERENTES_NOVEDOSOS[0]["desc"] != "otra cosa"


def test_los_introducidos_viajan_en_el_estado_guardado(tmp_path):
    state = estado_inicial("CURIANA")
    state.referentes_introducidos.append("cuentas_vidrio")
    path = tmp_path / "curiana_state.json"
    state.save(str(path))
    otro = ComunidadState.load(str(path))
    assert otro.referentes_introducidos == ["cuentas_vidrio"]
    assert [r["id"] for r in referentes_pendientes_de(otro)][0] == "cometa"


def test_un_estado_guardado_antes_del_campo_carga_y_empieza_de_cero(tmp_path):
    """Los curiana_state.json de la serie A no traen el campo."""
    d = estado_inicial("CURIANA").to_dict()
    del d["referentes_introducidos"]
    path = tmp_path / "viejo.json"
    path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    viejo = ComunidadState.load(str(path))
    assert viejo.referentes_introducidos == []
    assert referentes_pendientes_de(viejo)[0]["id"] == "cuentas_vidrio"


# ══════════════════════════════════════════════════════════════════════
# La disputa sobrevive la noche — de punta a punta, por `auto_mode`
# ══════════════════════════════════════════════════════════════════════

class _DBMuda:
    def create_run(self, *a, **k):
        return "run-de-prueba"

    def save_turn(self, **k):
        return "turn-de-prueba"

    def end_run(self, *a, **k):
        pass

    def get_run(self, run_id):
        # El brazo del run anterior: sin escena, que es como corren estos días.
        return {"config": {"escena": False, "capubana_cada": 0}}

    def runs_de_cadena(self, *a, **k):
        return []

    def __getattr__(self, nombre):
        return lambda *a, **k: "id"


class _Cliente:
    pass


def _alterna(formas):
    """Un `call_agent` que acuña por turnos una de las formas rivales: en el
    turno de nombramiento salen las dos y la competencia nace con dos
    variantes, como en un día de verdad."""
    ciclo = itertools.cycle(formas)
    return lambda *a, **k: f"Taya wana-ka arima. [{next(ciclo)}: kali + uco = algo]."


# Cuatro rivales, como en el día 1 de la serie C: con el soporte repartido
# ninguna llega al umbral del 55 % y el día cierra en disputa.
RIVALES = ("kali-uco-aima", "ucibo-kali-duruco", "kali-boro", "kali-rua")


def _correr_un_dia(monkeypatch, tmp_path, formas, turnos, continuar):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(orch, "call_agent", _alterna(formas))
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "get_db", lambda: _DBMuda())
    monkeypatch.setattr(orch, "get_client", lambda run_id=None: _Cliente())
    monkeypatch.setattr(orch, "huella_de_base",
                        lambda semilla=None: {"motor_sucio": False, "semilla": semilla})
    orch.auto_mode(_Cliente(), turnos, verbose=False, perfil=cargar_perfil("base"),
                   agentes_por_turno=len(RIVALES), roster_nombre="todos",
                   turnos_por_dia=turnos, semilla=11, continuar=continuar)
    with open(tmp_path / "curiana_koine.json", encoding="utf-8") as f:
        return json.load(f)


def test_la_disputa_de_un_dia_se_resuelve_al_dia_siguiente(monkeypatch, tmp_path):
    """El día 1 abre la competencia con cuatro rivales y no la resuelve; el día
    2 (--continuar) la HEREDA y la fija.

    Antes del 2026-09-18 el día 2 arrancaba con la competencia en blanco y, como
    `referentes_introducidos` impide volver a presentar el referente, la disputa
    moría sin resolverse: por competencia no podía fijarse jamás una entrada de
    koiné en una cadena de runs de un día."""
    # cinco turnos: el nombramiento cae en el 5º (cadencia 4) y ahí nacen las
    # cuatro rivales; el día cierra con la competencia abierta.
    dia1 = _correr_un_dia(monkeypatch, tmp_path, RIVALES, turnos=5, continuar=False)
    ref1 = dia1["competencia"]["referentes"].get("cuentas_vidrio")
    assert ref1, dia1["competencia"]["referentes"]
    assert set(ref1["variantes"]) == set(RIVALES), ref1["variantes"]
    assert ref1["fijada"] is None, "el día 1 no debería resolver la disputa"
    soporte1 = sum(ref1["variantes"].values())

    # El día 2 continúa y todos dicen la misma rival. Cuatro turnos: no hay
    # nombramiento nuevo (cadencia 4), sólo gente reusando una forma.
    dia2 = _correr_un_dia(monkeypatch, tmp_path, RIVALES[:1], turnos=4, continuar=True)
    ref2 = dia2["competencia"]["referentes"].get("cuentas_vidrio")
    assert ref2, "la disputa del día 1 desapareció al continuar"
    assert set(ref2["variantes"]) == set(RIVALES)          # las cuatro siguen ahí
    assert sum(ref2["variantes"].values()) > soporte1      # y el soporte creció
    assert ref2["fijada"] == RIVALES[0]
    assert ref2["fijada_dia"] == 2
    # y el ámbito de cada proponente viaja con ella (vacío sin --escena)
    assert "ambitos_de_forma" in dia2["competencia"]


def test_un_run_que_no_continua_empieza_la_competencia_de_cero(monkeypatch, tmp_path):
    _correr_un_dia(monkeypatch, tmp_path, RIVALES, turnos=5, continuar=False)
    otro = _correr_un_dia(monkeypatch, tmp_path, RIVALES, turnos=5, continuar=False)
    ref = otro["competencia"]["referentes"]["cuentas_vidrio"]
    # el segundo run vuelve a presentar el referente y la disputa nace de nuevo
    assert ref["fijada"] is None
    assert set(otro["competencia"]["referentes"]) == {"cuentas_vidrio"}
