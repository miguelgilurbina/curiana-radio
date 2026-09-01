# -*- coding: utf-8 -*-
"""Tests de D11 (#39): la columna añú/paraujano y el refuerzo lokono.

Lo que protegen: que la columna del pariente costero más cercano EXISTA
(estuvo en cero hasta el 2026-08-31), que el import de comparación jamás
pise una clave existente, y que la categoría `paraujano` sea canónica.
"""

from curiana_database import normalize_source_language
from curiana_lexicon import VOCABULARIO_BASE
from lexicon_a2 import COLISIONES_A2, LOKONO_A2, PARAUJANO_A2


def test_la_columna_anu_existe_y_no_esta_vacia():
    """El cero se midió el 2026-08-31; si vuelve, que se vea."""
    assert len(PARAUJANO_A2) >= 30
    n = sum(1 for e in VOCABULARIO_BASE.values()
            if normalize_source_language(e.get("fuente", "")) == "paraujano")
    assert n >= 30, "la columna añú volvió a vaciarse en VOCABULARIO_BASE"


def test_paraujano_es_categoria_canonica():
    assert normalize_source_language("paraujano") == "paraujano"
    assert normalize_source_language("añú") == "paraujano"


def test_el_import_a2_no_pisa_claves():
    """setdefault + colisiones declaradas: cada clave A2 del lexicón fusionado
    debe ser la entrada A2 (si otra capa la tuviera, es colisión, no pisado)."""
    for forma, e in {**PARAUJANO_A2, **LOKONO_A2}.items():
        assert VOCABULARIO_BASE[forma] is e or \
            VOCABULARIO_BASE[forma].get("notas") == e.get("notas"), forma
    formas_a2 = set(PARAUJANO_A2) | set(LOKONO_A2)
    for _, _, _, forma in COLISIONES_A2:
        assert forma not in formas_a2, (
            f"{forma} está a la vez importada y en COLISIONES_A2")


def test_el_import_es_comparacion_no_habla():
    """Ninguna clave A2 puede capturar el habla de los agentes: ni semillas
    ni raíces verbales. Si esto falla, una palabra que los agentes usan
    pasaría a contarse como fuga a otra lengua."""
    from curiana_koine import FORMAS_SEED
    from curiana_lexicon import _RAICES_VERB
    nuevas = set(PARAUJANO_A2) | set(LOKONO_A2)
    semillas = set()
    for formas in FORMAS_SEED.values():
        for f in formas:
            semillas.add(f)
            if "-" in f:
                semillas.add(f.split("-")[0])
    assert not (nuevas & semillas), sorted(nuevas & semillas)
    assert not (nuevas & set(_RAICES_VERB)), sorted(nuevas & set(_RAICES_VERB))
