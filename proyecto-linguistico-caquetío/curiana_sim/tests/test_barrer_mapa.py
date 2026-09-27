"""Tests del barrido del mapa vivo (barrer_mapa.py) — la forma viva del canon.

Lo que protegen (dp.2.09 de #222, P4, 2026-09-24): que un nombre del mapa que
es la forma viva de un topónimo del canon se reconozca como tal y no salga
«nuevo, en ninguna fuente». Antes de que el canon guardara `forma_viva`, el
informe decía que Paraguaná tenía ocho nombres nuevos que estaban en el canon
desde el lote 7 con la forma de Esteves.
"""

import barrer_mapa as B


def test_la_forma_viva_del_canon_se_indexa():
    vivas = B.cargar_formas_vivas()
    # Cividual es la forma viva de Sibidigual; Bajo Aroa, la de Bajabaroa
    assert vivas[B.clave("Cividual")][1] == "sibidigual"
    assert vivas[B.clave("Bajo Aroa")][1] == "bajabaroa"
    # los descartes también la llevan (Nueva Jayama → jayana)
    assert vivas[B.clave("Nueva Jayama")][1] == "jayana"


def test_el_generico_no_estorba():
    """«Cerro Capuana» se indexa también sin el genérico: antes caía, como
    aproximado, en `capana` (Parte II) en vez de en Capuhana."""
    vivas = B.cargar_formas_vivas()
    assert vivas[B.clave("Capuana")][1] == "capuhana"


def test_toda_forma_viva_lleva_coordenada_y_fuente():
    import yaml
    with open(B.CANON, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    for r in doc["toponimos"]:
        for f in r.get("forma_viva") or []:
            assert isinstance(f.get("lat"), float) and isinstance(f.get("lon"), float), r["id"]
            assert f.get("fuente") == "osm-kaketiana", r["id"]
