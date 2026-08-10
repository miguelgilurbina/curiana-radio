"""Tests de la fonotáctica.

Lo que protegen: que el filtro se entrene solo con lo atestiguado, que la
normalización ortográfica no dependa de cómo escribió el transcriptor, y —
sobre todo— **que el resultado negativo siga a la vista**. Si alguien mejora
el filtro y el wayunaiki empieza a pasar al 99%, el filtro dejó de medir algo.
"""

import curiana_fonotactica as F


# ── normalización ─────────────────────────────────────────────────────

def test_dos_grafias_de_la_misma_palabra_convergen():
    """El caquetío atestiguado se escribió a la castellana y el reconstruido
    a la moderna. Si no convergen, se mide al transcriptor."""
    assert F.fonemizar("caquetio") == F.fonemizar("kaketio")
    assert F.fonemizar("quiba") == F.fonemizar("kiba")


def test_el_seseo_y_el_betacismo_no_contrastan():
    assert F.fonemizar("zazarida") == F.fonemizar("sasarida")
    assert F.fonemizar("vaca") == F.fonemizar("baka")


def test_la_h_castellana_es_muda():
    assert F.fonemizar("harifuche") == F.fonemizar("arifuche")


def test_las_tildes_no_crean_fonemas():
    assert F.fonemizar("Zazárida") == F.fonemizar("zazarida")


def test_la_regla_gu_es_w_no_se_aplica_sola():
    """Es una cuestión abierta: activarla por defecto sería decidir D5 por la
    puerta de atrás."""
    assert F.fonemizar("gua") != F.fonemizar("wa")
    assert F.fonemizar("gua", gu_es_w=True) == F.fonemizar("wa")


# ── el filtro ─────────────────────────────────────────────────────────

def test_el_filtro_acepta_todo_lo_que_lo_entrena():
    """Trivial pero necesario: si el propio conjunto base fallara, el filtro
    estaría mal construido."""
    fono, paso = F.medir()
    assert paso["caquetío atestiguado"] == 1.0


def test_valida_devuelve_motivos_no_un_bool():
    fono, _ = F.medir()
    ok, motivos = fono.valida("transporte")
    assert not ok
    assert motivos and all(isinstance(m, str) for m in motivos)


def test_una_forma_caquetia_pasa():
    fono, _ = F.medir()
    assert fono.valida("barsure")[0]


def test_la_tasa_de_violacion_es_una_fraccion():
    fono, _ = F.medir()
    t = fono.tasa_de_violacion(["barsure", "transporte", "kashi"])
    assert 0.0 <= t <= 1.0
    assert F.Fonotactica(["kasa"]).tasa_de_violacion([]) == 0.0


# ── el resultado negativo, protegido ──────────────────────────────────

def test_el_filtro_discrimina_el_castellano():
    """Lo único que el filtro sí hace: el castellano tiene que caer bastante
    por debajo de las lenguas arahuacas."""
    _, paso = F.medir()
    assert paso["castellano (control)"] < 0.60
    assert paso["castellano (control)"] < paso["wayunaiki"] - 0.20


def test_el_filtro_NO_discrimina_el_wayunaiki():
    """**El resultado negativo de #91.** El wayunaiki pasa casi entero porque
    ya satisface la fonotáctica caquetía: ambas son abrumadoramente CV.

    Si este test empieza a fallar porque el wayunaiki bajó, no es una mejora
    automática — hay que mirar si el filtro se volvió más estricto por buenas
    razones o si el lexicón cambió debajo."""
    _, paso = F.medir()
    assert paso["wayunaiki"] > 0.80, (
        "el wayunaiki dejó de pasar mayoritariamente: revisar si el filtro "
        "cambió o si cambió el lexicón")


def test_la_regla_gu_cambia_la_discriminacion_a_lo_grande():
    """Una sola decisión ortográfica (D5, #36) mueve el poder discriminante
    del filtro contra el wayunaiki por un factor grande. Es la razón de que
    D5 no sea cosmética."""
    _, sin_regla = F.medir(gu_es_w=False)
    _, con_regla = F.medir(gu_es_w=True)
    assert sin_regla["wayunaiki"] - con_regla["wayunaiki"] > 0.15
