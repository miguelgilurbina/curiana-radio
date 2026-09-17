"""La competencia léxica sigue su secuencia de referentes de un día al
siguiente (--continuar). Hasta el 2026-09-17 cada run empezaba
REFERENTES_NOVEDOSOS de cero y un día de seis turnos sólo llegaba al
primero: los tres días de la serie A nombraron «las cuentas brillantes»."""
import json

from curiana_koine import REFERENTES_NOVEDOSOS
from curiana_orchestrator_v2 import referentes_pendientes_de
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
