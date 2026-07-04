"""Tests de difusión léxica y variación dialectal (curiana_social.py)."""

from curiana_social import (
    DifusionLexica,
    normalizar_por_dialecto,
    prestigio_de,
)


def test_prestigio_explicito_y_derivado():
    assert prestigio_de("Manaure") == 1.0
    assert 0.0 < prestigio_de("Marokoto-ni") < prestigio_de("Manaure")


def test_contagio_prestigioso_cruza_umbral_en_un_uso():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")   # prestigio 1.0, vínculo 0.95 con Buio-sha
    assert d.exposicion_de("Buio-sha", "sima-bana") >= d.umbral
    assert any(f == "sima-bana" for f, _ in d.sugerencias_para("Buio-sha"))


def test_no_se_sugiere_lo_ya_usado():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")
    d.propagar_uso("sima-bana", "Buio-sha")  # Buio-sha ya la usó
    assert d.sugerencias_para("Buio-sha") == []


def test_periferico_sin_vinculo_no_adopta():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")
    assert d.sugerencias_para("Marokoto-ni") == []


def test_normalizacion_dialectal_favorece_l2():
    assert normalizar_por_dialecto(4.5, "caribe") > normalizar_por_dialecto(4.5, "caquetío")
    assert normalizar_por_dialecto(9.9, "caribe") <= 10.0   # acotado
