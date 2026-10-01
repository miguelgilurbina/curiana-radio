"""Tests del exportador del mapa de la portada de Kaketiana.

Qué entra al mapa decide qué se publica como territorio del wiki: un topónimo
descartado o un cruce aproximado sin revisar no pueden aparecer como lugares.
"""

import export_mapa_seed as ems

CANON = {"toponimos": [
    {"id": "toponimo-1", "forma": "tacal", "nivel": "C", "glosa_reconstruida": "x",
     "procedencia": {"obra": "esteves-1989"}},
    {"id": "toponimo-2", "forma": "bisure", "nivel": "A", "glosa_fuente": "lagarto común"},
    {"id": "toponimo-3", "forma": "cauca", "nivel": "descartado"},
]}


def entrada(forma, en_canon, como="exacto", lat=11.5, lon=-70.0, **extra):
    return {"forma": forma, "tipo": "río", "lat": lat, "lon": lon, "region": "paraguana",
            "cruce": {"con": forma.lower(), "como": como, "en_canon": en_canon}, **extra}


def test_el_id_del_canon_se_lee_sin_el_nivel():
    assert ems.id_en_canon("toponimo-151 · nivel C") == "toponimo-151"
    assert ems.id_en_canon(None) is None


def test_entra_lo_vigente_y_no_lo_descartado():
    mapa = {"entradas": [
        entrada("Río Tacal", "toponimo-1 · nivel C"),
        entrada("Cauca", "toponimo-3 · nivel descartado"),
        {"forma": "El 22", "lat": 11.0, "lon": -70.2, "region": "x"},  # sin cruce
    ]}
    seed = ems.construir_seed(mapa, CANON)
    assert [p["forma"] for p in seed["puntos"]] == ["tacal"]
    assert seed["resumen"]["toponimos_vigentes"] == 2
    assert seed["resumen"]["toponimos_con_lugar"] == 1


def test_un_cruce_aproximado_por_revisar_no_es_un_lugar():
    mapa = {"entradas": [
        entrada("Quebrada Los Bisures", "toponimo-2 · nivel A", como="aproximado:bisure", revisar=True),
        entrada("Bisure", "toponimo-2 · nivel A", como="forma-viva", lat=11.6),
    ]}
    seed = ems.construir_seed(mapa, CANON)
    assert [p["nombre_en_el_mapa"] for p in seed["puntos"]] == ["Bisure"]
    assert seed["puntos"][0]["glosa"] == "lagarto común"  # la impresa manda


def test_el_mismo_rasgo_dos_veces_es_un_punto():
    mapa = {"entradas": [entrada("Río Tacal", "toponimo-1"), entrada("Río Tacal", "toponimo-1", lat=11.50001)]}
    assert len(ems.construir_seed(mapa, CANON)["puntos"]) == 1


def test_un_id_que_no_esta_en_el_canon_se_avisa():
    seed = ems.construir_seed({"entradas": [entrada("Fantasma", "toponimo-99")]}, CANON)
    assert seed["puntos"] == [] and "toponimo-99" in seed["avisos"][0]


def test_los_puntos_van_de_la_lectura_mas_firme_a_la_mas_debil():
    mapa = {"entradas": [entrada("Río Tacal", "toponimo-1"), entrada("Bisure", "toponimo-2", lat=12.0)]}
    assert [p["nivel"] for p in ems.construir_seed(mapa, CANON)["puntos"]] == ["A", "C"]
