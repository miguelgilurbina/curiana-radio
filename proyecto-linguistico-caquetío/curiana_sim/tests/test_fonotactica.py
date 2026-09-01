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


def test_el_filtro_discrimina_el_wayunaiki_tras_d5c():
    """**El estado decidido.** Hasta la tanda del 2026-08-30 este test
    protegía el resultado negativo de #91 (el wayunaiki pasaba >80% porque la
    grafía colonial disfrazaba las /w/ de <gu>). D5c se decidió (gu→w
    uniforme) y la Fase 2 la horneó en los LEMAS (aplicar_fase2_d5.py), así
    que la discriminación ya no depende del flag: vive en la base.

    Lo que se protege ahora: el wayunaiki pasa MINORITARIAMENTE, y el orden
    lokono > wayunaiki — la señal estructural del cómputo de D11
    (6-fusion/computo_d11_2026-08-31.yaml). Si esto falla, o el lexicón
    cambió debajo o alguien deshizo la migración."""
    _, paso = F.medir()
    assert paso["wayunaiki"] < 0.75, (
        "el wayunaiki volvió a pasar mayoritariamente: ¿se deshizo la "
        "migración de lemas de la Fase 2 de D5?")
    assert paso["lokono"] > paso["wayunaiki"], (
        "el orden lokono > wayunaiki del cómputo D11 se invirtió: revisar "
        "qué cambió en la base atestiguada")


def test_la_regla_gu_ya_esta_horneada_en_los_lemas():
    """Antes de la tanda, activar gu_es_w movía el pase del wayunaiki >15
    puntos — la prueba de que D5 no era cosmética. Tras la Fase 2, los lemas
    ya llevan la /w/ escrita y el flag es casi nulo SOBRE LA BASE. Este test
    documenta que la decisión está aplicada: si el flag vuelve a mover mucho,
    hay lemas sin migrar entrando a la base (p. ej. una regeneración de
    lexicon_zavala sin el paso de normalización — ver
    6-fusion/migracion_lemas_fase2.yaml)."""
    _, sin_regla = F.medir(gu_es_w=False)
    _, con_regla = F.medir(gu_es_w=True)
    assert abs(sin_regla["wayunaiki"] - con_regla["wayunaiki"]) < 0.05
