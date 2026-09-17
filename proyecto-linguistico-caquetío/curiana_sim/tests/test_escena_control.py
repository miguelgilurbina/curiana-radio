"""La escena: EL CONTROL (PR 5 del diseño del 2026-09-17).

La escena es un BRAZO y la evidencia es la DIFERENCIA entre dos cadenas
completas con la misma semilla (§5.4). Eso pide tres cosas, y son éstas:

  (a) `curiana_cadena` NO MEZCLA BRAZOS. Una cadena con escena y otra sin ella
      no se unen; si una cadena cambió de brazo a la mitad —el motor ya no
      deja hacerla, pero la base viene de antes que esa comprobación— el
      veredicto avisa y deja fuera los días del otro brazo.
  (b) `--dry-run` imprime la config resuelta y sale SIN LLAMAR A NADA: ni a la
      API, ni a la base, ni a git.
  (c) `analizar_nodos.py` etiqueta el informe con el brazo leído de la config,
      no deducido de `presencias`.
"""
import os
import subprocess
import sys

import pytest

import analizar_nodos as an
import curiana_orchestrator_v2 as orch
from curiana_cadena import (
    brazo_de,
    brazos_de_cadena,
    linea_de_brazo,
    serie_koine_de_cadena,
    texto_de_brazo,
)
from curiana_perfiles import cargar_perfil

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

A = "aaaaaaaa-0000-0000-0000-000000000001"
B = "bbbbbbbb-0000-0000-0000-000000000002"
C = "cccccccc-0000-0000-0000-000000000003"


def _run(rid, dia, padre, **cfg):
    return {"id": rid, "ended_at": "2026-09-18T00:00:00Z", "total_turns": 6,
            "config": {"dia_inicial": dia, "continuado_desde": padre,
                       "elenco": "era2", **cfg}}


def _metrica(dia, d):
    return {"day": dia, "distance": d, "distance_ventana": d,
            "distance_emergente": d, "n_agents": 12}


class _Lector:
    def __init__(self, runs, metricas):
        self.runs = {r["id"]: r for r in runs}
        self.metricas = metricas

    def get_run(self, run_id):
        return self.runs.get(run_id)

    def runs_encadenados(self):
        return list(self.runs.values())

    def koine_metrics(self, run_id):
        return list(self.metricas.get(run_id, []))


# ══════════════════════════════════════════════════════════════════════
# (a) la cadena no mezcla brazos
# ══════════════════════════════════════════════════════════════════════

def test_a_un_run_anterior_a_la_escena_es_sin_escena():
    """La clave no existía antes del 2026-09-17: que no esté es un hecho, no
    un desconocido — entonces aquel run corrió sin escena."""
    assert brazo_de(_run(A, 1, None)) == (False, 0)
    assert brazo_de(_run(A, 1, None, escena=False, capubana_cada=None)) == (False, 0)
    assert brazo_de(_run(A, 1, None, escena=True, capubana_cada=3)) == (True, 3)
    # sin escena, la cadencia no significa nada y no se lee
    assert brazo_de(_run(A, 1, None, escena=False, capubana_cada=3)) == (False, 0)
    assert texto_de_brazo((True, 3)) == "con escena, Capubana cada 3"
    assert texto_de_brazo((True, 0)) == "con escena, sin Capubana"
    assert texto_de_brazo((False, 0)) == "sin escena"


def test_a_una_cadena_de_un_solo_brazo_se_une_entera():
    runs = [_run(A, 1, None, escena=True, capubana_cada=3),
            _run(B, 2, A, escena=True, capubana_cada=3)]
    db = _Lector(runs, {A: [_metrica(1, 0.9)], B: [_metrica(2, 0.7)]})
    avisos = []
    serie = serie_koine_de_cadena(db, B, avisos=avisos)
    assert [p[0] for p in serie] == [1, 2]
    assert avisos == []
    assert linea_de_brazo(runs) == "brazo: con escena, Capubana cada 3"


def test_a_una_cadena_que_cambia_de_brazo_no_se_mezcla():
    """El día 1 corrió sin escena y el 2 con ella: el veredicto avisa y se
    queda sólo con los días del brazo de la HOJA."""
    runs = [_run(A, 1, None),                              # sin escena
            _run(B, 2, A, escena=True, capubana_cada=3)]   # con escena
    db = _Lector(runs, {A: [_metrica(1, 0.9)], B: [_metrica(2, 0.7)]})
    avisos = []
    serie = serie_koine_de_cadena(db, B, avisos=avisos)
    assert [p[0] for p in serie] == [2]
    assert len(avisos) == 1 and "NO se mezclan" in avisos[0]
    assert "sin escena" in avisos[0] and "con escena" in avisos[0]
    linea = linea_de_brazo(runs)
    assert linea.startswith("⚠ ESTA CADENA MEZCLA 2 BRAZOS")
    assert brazos_de_cadena(runs) == {(False, 0): [A], (True, 3): [B]}


def test_a_dos_cadencias_distintas_tampoco_se_mezclan():
    """`--capubana-cada` es parte del brazo: cambiar la cadencia a mitad de
    cadena cambia el mundo tanto como quitar la escena."""
    runs = [_run(A, 1, None, escena=True, capubana_cada=3),
            _run(B, 2, A, escena=True, capubana_cada=4)]
    db = _Lector(runs, {A: [_metrica(1, 0.9)], B: [_metrica(2, 0.7)]})
    avisos = []
    assert [p[0] for p in serie_koine_de_cadena(db, B, avisos=avisos)] == [2]
    assert avisos and "Capubana cada 3" in avisos[0]


def test_a_las_cadenas_viejas_de_la_base_no_se_rompen():
    """Ninguna cadena anterior a hoy declara `escena`: todas son del mismo
    brazo (sin escena) y se siguen uniendo enteras."""
    runs = [_run(A, 1, None), _run(B, 2, A), _run(C, 3, B)]
    db = _Lector(runs, {A: [_metrica(1, 0.9)], B: [_metrica(2, 0.8)],
                        C: [_metrica(3, 0.7)]})
    avisos = []
    assert [p[0] for p in serie_koine_de_cadena(db, C, avisos=avisos)] == [1, 2, 3]
    assert avisos == []
    assert linea_de_brazo(runs) == "brazo: sin escena"


# ══════════════════════════════════════════════════════════════════════
# (b) --dry-run
# ══════════════════════════════════════════════════════════════════════

def test_b_la_config_resuelta_dice_el_brazo():
    cfg = orch.config_resuelta(6, cargar_perfil("base"), agentes_por_turno=12,
                               roster_nombre="todos", turnos_por_dia=6,
                               semilla=1, serie="era2-c", escena=True,
                               capubana_cada=3)
    assert cfg["escena"] is True and cfg["capubana_cada"] == 3
    assert cfg["serie"] == "era2-c" and cfg["semilla"] == 1
    assert cfg["continuado_desde"] is None and cfg["continuar"] is False
    assert cfg["perfil"] == "base" and cfg["turnos"] == 6
    # sin escena la cadencia no se sella: la config no sugiere lo que no pasó
    sin = orch.config_resuelta(6, cargar_perfil("base"), capubana_cada=3)
    assert sin["escena"] is False and sin["capubana_cada"] is None


def test_b_continuado_desde_sale_del_estado_en_disco(tmp_path, monkeypatch):
    from curiana_state import ComunidadState
    monkeypatch.chdir(tmp_path)
    ComunidadState(run_anterior="abcdef12-0000-0000-0000-000000000000").save()
    cfg = orch.config_resuelta(6, cargar_perfil("base"), continuar=True)
    assert cfg["continuado_desde"].startswith("abcdef12")
    # y sin estado en disco no revienta: avisa el impresor
    os.remove(tmp_path / "curiana_state.json")
    assert orch.config_resuelta(6, cargar_perfil("base"),
                                continuar=True)["continuado_desde"] is None


def test_b_el_dry_run_no_llama_a_nada(tmp_path, monkeypatch):
    """Se corre el CLI entero en un subproceso SIN clave de API y con la base
    apagada: si tocara cualquiera de las dos, no saldría con 0."""
    entorno = {**os.environ, "PYTHONIOENCODING": "utf-8",
               "CURIANA_ELENCO": "era2", "ANTHROPIC_API_KEY": "",
               "SUPABASE_URL": "", "SUPABASE_SERVICE_KEY": ""}
    r = subprocess.run(
        [sys.executable, "curiana_orchestrator_v2.py", "--elenco", "era2",
         "--auto", "6", "--turnos-por-dia", "6", "--agentes-por-turno", "12",
         "--roster", "todos", "--semilla", "1", "--serie", "era2-c",
         "--escena", "--capubana-cada", "3", "--dry-run"],
        cwd=SIM, capture_output=True, env=entorno, timeout=180)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    salida = r.stdout.decode("utf-8")
    for clave in ("perfil", "serie", "escena", "capubana_cada", "semilla",
                  "continuado_desde"):
        assert clave in salida, clave
    assert "era2-c" in salida and "Capubana cada 3" in salida
    assert "Run ID" not in salida and "SIMULACIÓN COMPLETADA" not in salida


def test_b_el_dry_run_sin_escena_dice_que_es_el_de_control(tmp_path, capsys):
    orch.imprimir_dry_run(orch.config_resuelta(6, cargar_perfil("base")))
    salida = capsys.readouterr().out
    assert "brazo: sin escena (el de control" in salida
    assert "capubana_cada        —" in salida


# ══════════════════════════════════════════════════════════════════════
# (c) analizar_nodos etiqueta el informe con el brazo
# ══════════════════════════════════════════════════════════════════════

def test_c_el_brazo_de_la_cadena_sale_de_la_config():
    con = [{"escena": "true", "capubana_cada": "3"},
           {"escena": "true", "capubana_cada": "3"}]
    assert an.brazo_de_la_cadena(con) == {
        "escena": True, "capubana_cada": 3, "mezcla": False,
        "brazos": ["con escena, Capubana cada 3"]}
    sin = [{"escena": "", "capubana_cada": ""}]
    assert an.brazo_de_la_cadena(sin)["escena"] is False
    assert an.brazo_de_la_cadena(sin)["mezcla"] is False
    mezcla = an.brazo_de_la_cadena(con + sin)
    assert mezcla["mezcla"] is True and len(mezcla["brazos"]) == 2


def test_c_el_informe_dice_el_brazo(capsys):
    res = {
        "cadena": [{"run": "abcdef12", "serie": "era2-c", "escena": "true",
                    "capubana_cada": "3"}],
        "brazo": an.brazo_de_la_cadena([{"escena": "true", "capubana_cada": "3"}]),
        "elenco": {"total": 63, "por_nodo": {"GUARANAO": 39, "AMUAY": 24}},
        "umbrales": {"inclinacion": 3.0, "min_hablantes": 2, "formas_excluidas": 0},
        "divergencia_sembrada": {"vectores_semilla_distintos": 15, "agentes": 63,
                                 "agentes_con_el_vector_mas_comun": 3,
                                 "nodos_con_semilla_propia": ["GUARANAO"],
                                 "con_formas_seed_propia": ["Manaure"]},
        "cobertura": {"agentes_con_nodo": 63, "agentes_en_la_base": 63,
                      "pct_usos_con_nodo": 100.0, "n_agentes_sin_nodo": 0,
                      "agentes_sin_nodo": []},
        "habla_por_nodo": [],
    }
    an.imprimir(res, top=0, con_formas=False, con_distancia=False)
    salida = capsys.readouterr().out
    assert "Brazo: con escena, Capubana cada 3 · serie era2-c" in salida
    assert "MEZCLA BRAZOS" not in salida

    res["brazo"] = an.brazo_de_la_cadena(
        [{"escena": "true", "capubana_cada": "3"}, {"escena": "", "capubana_cada": ""}])
    an.imprimir(res, top=0, con_formas=False, con_distancia=False)
    assert "ESTA CADENA MEZCLA BRAZOS" in capsys.readouterr().out
