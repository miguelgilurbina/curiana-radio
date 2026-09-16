"""Tests de la cadena de runs encadenados (`curiana_cadena.py`).

En la era 2 un run ES un día y los días se encadenan con `--continuar`. El
veredicto de convergencia miraba sólo la serie del run en curso —un punto— y
por eso el motor imprimía «datos insuficientes (ningún par de días comparable)»
al cerrar cada día del 2026-09-16, con la cadena `c6837386` → `89fc1744` ya
medida en `koine_metrics`.

Sin red y sin base: un lector falso de diez líneas sirve las dos tablas que el
módulo necesita (`simulation_runs` y `koine_metrics`), igual que
`tests/test_orchestrator.py` sustituye el cliente LLM y pasa `db=None`.

Las cifras son las MEDIDAS en la base local el 2026-09-16 (`koine_metrics`).
"""

import pytest

from curiana_cadena import (
    cadena_de_runs,
    cadenas_en_la_base,
    es_interrumpido,
    serie_koine_de_cadena,
    texto_veredicto,
    veredicto,
)

# ── Los runs reales de la cadena del 2026-09-16 (día 1 → día 2 → día 3 muerto)
D1 = "c6837386-eb81-49cb-8533-373d887158b6"
D2 = "89fc1744-400a-4917-a921-7036ed8d8791"
D3 = "06482296-8232-449e-a2b1-4ef9c4c9f112"      # interrumpido: 0 turnos

# koine_metrics medidas: (day, distance, distance_ventana, distance_emergente)
METRICAS = {
    D1: [{"day": 1, "distance": 0.1993, "distance_ventana": 0.6038,
          "distance_emergente": 0.8995, "n_agents": 60}],
    D2: [{"day": 2, "distance": 0.2295, "distance_ventana": 0.4665,
          "distance_emergente": 0.8203, "n_agents": 62}],
    D3: [],
}

RUNS = {
    D1: {"id": D1, "ended_at": "2026-09-16T16:41:33Z", "total_turns": 6,
         "config": {"dia_inicial": 1, "continuado_desde": None, "elenco": "era2"}},
    D2: {"id": D2, "ended_at": "2026-09-16T18:40:20Z", "total_turns": 6,
         "config": {"dia_inicial": 2, "continuado_desde": D1, "elenco": "era2"}},
    D3: {"id": D3, "ended_at": None, "total_turns": 0,
         "config": {"dia_inicial": 3, "continuado_desde": D2, "elenco": "era2"}},
}


class _LectorFalso:
    """Lo que `curiana_cadena` le pide a una base: tres lecturas y nada más."""

    def __init__(self, runs=None, metricas=None):
        self.runs = dict(RUNS if runs is None else runs)
        self.metricas = dict(METRICAS if metricas is None else metricas)
        self.leidos = []                      # para contar consultas

    def get_run(self, run_id):
        self.leidos.append(run_id)
        return self.runs.get(run_id)

    def runs_encadenados(self):
        return list(self.runs.values())

    def koine_metrics(self, run_id):
        return list(self.metricas.get(run_id, []))


# ══════════════════════════════════════════════════════════════════════
# La cadena se reconstruye
# ══════════════════════════════════════════════════════════════════════

def test_la_cadena_sube_hasta_la_raiz_y_devuelve_raiz_a_hoja():
    cadena = cadena_de_runs(_LectorFalso(), D2)
    assert [r["id"] for r in cadena] == [D1, D2]


def test_la_cadena_pasa_a_traves_del_run_interrumpido():
    """El día 3 murió a los 2 turnos, pero la cadena tiene que poder subir a
    través de él hasta la raíz: saltarlo aquí la partiría por el medio."""
    cadena = cadena_de_runs(_LectorFalso(), D3)
    assert [r["id"] for r in cadena] == [D1, D2, D3]


def test_un_run_suelto_es_una_cadena_de_uno():
    assert [r["id"] for r in cadena_de_runs(_LectorFalso(), D1)] == [D1]


def test_sin_base_no_hay_cadena():
    """Modo JSON (`CurianaDBMock`) o `db=None`: no rompe, devuelve vacío."""
    assert cadena_de_runs(None, D2) == []

    class _Mudo:
        pass
    assert cadena_de_runs(_Mudo(), D2) == []


def test_un_padre_que_no_esta_en_la_base_corta_el_ascenso():
    lector = _LectorFalso(runs={D2: RUNS[D2]})
    assert [r["id"] for r in cadena_de_runs(lector, D2)] == [D2]


def test_un_ciclo_no_cuelga():
    """Una config corrupta que apunte a sí misma no puede colgar el cierre."""
    bucle = {
        D1: {**RUNS[D1], "config": {"continuado_desde": D2, "dia_inicial": 1}},
        D2: RUNS[D2],
    }
    cadena = cadena_de_runs(_LectorFalso(runs=bucle), D2)
    assert [r["id"] for r in cadena] == [D1, D2]


def test_la_config_tambien_se_lee_como_texto_json():
    """psql devuelve `config` como texto; supabase-py como dict. Los dos valen."""
    import json
    como_texto = {rid: {**r, "config": json.dumps(r["config"])}
                  for rid, r in RUNS.items()}
    cadena = cadena_de_runs(_LectorFalso(runs=como_texto), D2)
    assert [r["id"] for r in cadena] == [D1, D2]


def test_la_config_aplanada_por_el_lector_tambien_vale():
    """Un lector que hizo SELECT config->>'continuado_desde' no trae `config`."""
    planos = {
        D1: {"id": D1, "ended_at": "…", "total_turns": 6, "continuado_desde": None},
        D2: {"id": D2, "ended_at": "…", "total_turns": 6, "continuado_desde": D1},
    }
    assert [r["id"] for r in cadena_de_runs(_LectorFalso(runs=planos), D2)] == [D1, D2]


# ══════════════════════════════════════════════════════════════════════
# La serie: sin duplicar días, saltando el interrumpido
# ══════════════════════════════════════════════════════════════════════

def test_la_serie_une_los_dias_de_toda_la_cadena():
    serie = serie_koine_de_cadena(_LectorFalso(), D2)
    assert [p[0] for p in serie] == [1, 2]
    assert serie[0] == (1, 0.1993, 0.6038, 0.8995)
    assert serie[1] == (2, 0.2295, 0.4665, 0.8203)


def test_el_run_interrumpido_se_salta_con_aviso():
    avisos: list[str] = []
    serie = serie_koine_de_cadena(_LectorFalso(), D3, avisos=avisos)
    assert [p[0] for p in serie] == [1, 2]      # el día 3 no llegó a cerrarse
    assert len(avisos) == 1 and D3[:8] in avisos[0]


def test_un_interrumpido_con_metricas_igual_se_salta():
    """Un run cortado puede haber alcanzado a escribir un día antes de morir;
    no entra: la unidad de la serie es el día cerrado, no la fila que exista."""
    metricas = dict(METRICAS)
    metricas[D3] = [{"day": 3, "distance": 0.9, "distance_ventana": 0.9,
                     "distance_emergente": 0.9, "n_agents": 2}]
    serie = serie_koine_de_cadena(_LectorFalso(metricas=metricas), D3)
    assert [p[0] for p in serie] == [1, 2]


def test_los_dias_no_se_duplican_y_gana_el_run_mas_avanzado():
    """Si dos runs de la cadena midieron el mismo día, el más cercano a la hoja
    lo remidió sobre el estado heredado: ése es el que vale."""
    metricas = dict(METRICAS)
    metricas[D1] = METRICAS[D1] + [
        {"day": 2, "distance": 0.99, "distance_ventana": 0.99,
         "distance_emergente": 0.99, "n_agents": 1}]
    serie = serie_koine_de_cadena(_LectorFalso(metricas=metricas), D2)
    assert [p[0] for p in serie] == [1, 2]
    assert serie[1][3] == 0.8203               # el del día 2, no el 0.99 del D1


def test_la_serie_ordena_por_dia_aunque_la_base_no():
    metricas = {D1: METRICAS[D2], D2: METRICAS[D1]}   # al revés a propósito
    serie = serie_koine_de_cadena(_LectorFalso(metricas=metricas), D2)
    assert [p[0] for p in serie] == [1, 2]


def test_las_lecturas_nulas_pasan_como_none():
    """Runs viejos (pre-2026-07-04) no tienen ventana ni emergente."""
    metricas = {
        D1: [{"day": 1, "distance": 0.66, "distance_ventana": None,
              "distance_emergente": None}],
        D2: [{"day": 2, "distance": 0.61, "distance_ventana": "",
              "distance_emergente": float("nan")}],
    }
    serie = serie_koine_de_cadena(_LectorFalso(metricas=metricas), D2)
    assert serie == [(1, 0.66, None, None), (2, 0.61, None, None)]


# ══════════════════════════════════════════════════════════════════════
# El veredicto: el MISMO criterio del orquestador
# ══════════════════════════════════════════════════════════════════════

def test_el_veredicto_de_la_cadena_del_16_es_converge_por_la_emergente():
    """Las cifras medidas de D1→D2: la emergente cae 0.8995 → 0.8203 (−8,8%),
    más que el 5% total y que el 2% del último tercio que exige
    `veredicto_convergencia`. Ojo: la ACUMULADA sube (0.1993 → 0.2295) — por eso
    el criterio se emite sobre la lectura más exigente y no sobre las tres."""
    serie = serie_koine_de_cadena(_LectorFalso(), D2)
    etiqueta, codigo, _mensaje, d_ini, d_fin = veredicto(serie)
    assert etiqueta == "emergente"
    assert codigo == "converge"
    assert (d_ini, d_fin) == (0.8995, 0.8203)
    assert "CONVERGE" in texto_veredicto(serie)


def test_el_veredicto_del_run_solo_es_insuficiente():
    """La deuda que esto cierra: un run de la era 2 es un día y su serie sola
    nunca tiene dos puntos comparables."""
    serie = [(1, 0.1993, 0.6038, 0.8995)]
    etiqueta, codigo, mensaje, _i, _f = veredicto(serie)
    assert etiqueta is None and codigo == "insuficiente"
    assert "insuficientes" in mensaje
    assert texto_veredicto(serie) == f"Veredicto: {mensaje}"


def test_el_veredicto_cae_a_la_ventana_si_no_hay_emergente():
    serie = [(1, 0.40, 0.60, None), (2, 0.39, 0.50, None)]
    etiqueta, codigo, _m, _i, _f = veredicto(serie)
    assert etiqueta == "ventana" and codigo == "converge"


def test_el_veredicto_es_el_mismo_que_usa_el_orquestador():
    """No es «otro» criterio parecido: el orquestador llama a esta función.
    Si alguien la duplicara, este test deja de tener sentido y hay que mirarlo."""
    import inspect

    import curiana_orchestrator_v2 as orch

    fuente = inspect.getsource(orch.auto_mode) + inspect.getsource(orch._imprimir_cadena)
    assert "texto_veredicto(serie_distancia)" in fuente
    assert "texto_veredicto(serie)" in fuente
    assert "veredicto_convergencia(" not in fuente      # ya no se llama a mano


# ══════════════════════════════════════════════════════════════════════
# El cierre del run: lo que imprime el orquestador
# ══════════════════════════════════════════════════════════════════════

def test_al_cerrar_un_run_continuado_se_imprime_la_cadena(capsys):
    import curiana_orchestrator_v2 as orch

    orch._imprimir_cadena(_LectorFalso(), D2)
    salida = capsys.readouterr().out
    assert "CADENA" in salida
    assert "D1:0.8995 → D2:0.8203" in salida
    assert "CONVERGE" in salida


def test_un_run_suelto_no_imprime_cadena(capsys):
    import curiana_orchestrator_v2 as orch

    orch._imprimir_cadena(_LectorFalso(), D1)
    assert capsys.readouterr().out == ""


def test_sin_base_el_cierre_no_rompe(capsys):
    """Modo JSON: `CurianaDBMock` no sabe de runs y el cierre sigue igual."""
    import curiana_orchestrator_v2 as orch
    from curiana_database import CurianaDBMock

    orch._imprimir_cadena(CurianaDBMock(), D2)
    orch._imprimir_cadena(None, D2)
    assert capsys.readouterr().out == ""


def test_una_base_caida_avisa_y_no_tumba_el_cierre(capsys):
    """El bloque corre DESPUÉS de `end_run`: un fallo aquí no puede llevarse por
    delante el reporte de un run ya terminado."""
    import curiana_orchestrator_v2 as orch

    class _Roto:
        def get_run(self, run_id):
            raise RuntimeError("base caída")

    orch._imprimir_cadena(_Roto(), D2)
    assert "no se pudo leer la cadena" in capsys.readouterr().out


# ══════════════════════════════════════════════════════════════════════
# Descubrir las cadenas de la base
# ══════════════════════════════════════════════════════════════════════

def test_se_descubren_las_cadenas_por_su_hoja():
    cadenas = cadenas_en_la_base(_LectorFalso())
    assert len(cadenas) == 1
    assert [r["id"] for r in cadenas[0]] == [D1, D2, D3]


def test_un_run_suelto_no_es_una_cadena():
    suelto = "aafc5c32-48b6-400d-9d13-ee45371f586c"
    lector = _LectorFalso(runs={suelto: {"id": suelto, "ended_at": "…",
                                         "total_turns": 6, "config": {}}})
    assert cadenas_en_la_base(lector) == []


def test_dos_hijos_del_mismo_run_son_dos_cadenas():
    """Pasó el 2026-09-16: dos intentos del día 3 colgando de `89fc1744`."""
    otro = "0193873d-7077-450e-95a0-5673d1d2d2c1"
    runs = dict(RUNS)
    runs[otro] = {"id": otro, "ended_at": None, "total_turns": 0,
                  "config": {"dia_inicial": 3, "continuado_desde": D2}}
    cadenas = cadenas_en_la_base(_LectorFalso(runs=runs))
    assert len(cadenas) == 2
    assert {c[-1]["id"] for c in cadenas} == {D3, otro}


# ══════════════════════════════════════════════════════════════════════
# Lo que cuenta como interrumpido
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("run, esperado", [
    ({"ended_at": "2026-09-16T18:40:20Z", "total_turns": 6}, False),
    ({"ended_at": None, "total_turns": 0}, True),
    ({"ended_at": "", "total_turns": 6}, True),
    ({"ended_at": "2026-09-16T19:40:00Z", "total_turns": 0}, True),
    ({"ended_at": "2026-09-16T19:40:00Z", "total_turns": None}, True),
])
def test_es_interrumpido(run, esperado):
    assert es_interrumpido(run) is esperado
