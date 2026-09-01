# -*- coding: utf-8 -*-
"""Tests de D3 (#34, decidida 2026-09-01): el rescate intra-turno con
justicia dialectal, y su apagado en ablación.

Lo que protegen: que el umbral del reintento se evalúe sobre el score
NORMALIZADO por etnia (el caribe no reintenta por obedecer su propio
prompt), que la fuga a otra lengua siga rescatando a cualquiera, y que en
el brazo de control (--ablacion) NO haya rescate — es una inyección que
empuja convergencia y el control corre sin ella.
"""

from curiana_social import necesita_rescate


def _metr(score, otro=0, pct=1.0):
    return {"score": score, "otro_arahuaco": otro,
            "pct_caquetio_especifico": pct}


def test_el_caribe_no_reintenta_por_obedecer_su_prompt():
    """3.0 crudo: bajo la vara nativa reintentaría; normalizado por la
    densidad caribe (0.25) es 7.8 — hizo exactamente su papel."""
    assert not necesita_rescate(_metr(3.0), "caribe")
    assert necesita_rescate(_metr(3.0), "caquetío")


def test_el_caribe_realmente_bajo_si_reintenta():
    """1.5 crudo → 3.9 normalizado: sigue bajo el umbral. La justicia
    dialectal no es un pase libre."""
    assert necesita_rescate(_metr(1.5), "caribe")


def test_la_fuga_a_otra_lengua_rescata_a_cualquiera():
    """Hablar wayunaiki en vez de caquetío es fuga sea quien sea: la
    normalización no la tapa."""
    m = _metr(8.0, otro=3, pct=0.2)
    assert necesita_rescate(m, "caquetío")
    assert necesita_rescate(m, "caribe")


def test_en_ablacion_no_hay_rescate_para_nadie():
    """El brazo de control corre sin la inyección — aunque el score sea
    pésimo y la fuga total."""
    m = _metr(1.0, otro=5, pct=0.0)
    assert not necesita_rescate(m, "caquetío", ablacion=True)
    assert not necesita_rescate(m, "caribe", ablacion=True)


def test_etnia_desconocida_usa_la_vara_nativa():
    """Un tier 3 sin etnia declarada se mide como nativo (perfil por
    defecto) — nadie queda sin vara."""
    assert necesita_rescate(_metr(3.0), None)
    assert not necesita_rescate(_metr(6.0), None)