"""Tests del exportador de una serie de la era 2 (dos brazos, una cadena cada uno).

Sin base: se prueban las piezas puras que deciden qué cifra llega a la página —
los días de Capubana, el placebo, la brecha que se cita y la competencia leída
del estado—. La parte que consulta la base es plomería de `analizar_nodos` y
`curiana_cadena`, que tienen sus propios tests.
"""

import export_serie_seed as ess


def test_dias_de_capubana_es_la_regla_del_motor():
    # curiana_escena.es_dia_de_capubana: dia % cada == 0
    assert ess.dias_de_capubana(list(range(1, 31)), 3) == [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
    assert ess.dias_de_capubana(list(range(1, 31)), 0) == []


def test_el_placebo_usa_los_mismos_dias_en_el_brazo_sin_escena():
    serie = [{"dia": d, "emergente": 0.5 if d % 3 == 0 else 0.9} for d in range(1, 7)]
    r = ess.partir_por_capubana(serie, "emergente", [3, 6])
    assert r == {"capubana": 0.5, "resto": 0.9, "n_capubana": 2}


def test_una_lectura_sin_dato_no_cuenta_como_cero():
    serie = [{"dia": 3, "brecha": None}, {"dia": 1, "brecha": 0.02}]
    r = ess.partir_por_capubana(serie, "brecha", [3])
    assert r["capubana"] is None and r["n_capubana"] == 0
    assert r["resto"] == 0.02


def test_la_brecha_publicada_es_la_acumulada_emergente():
    koine = [(1, 0.73, 0.6, 0.92), (2, 0.6, 0.4, 0.88)]
    distancia = [
        {"dia": 1, "ventana": {"brecha": 0.9}, "emergente": {"brecha": 0.8},
         "acumulada_emergente": {"brecha": 0.0028}},
        {"dia": 2, "ventana": {"brecha": 0.9}, "emergente": {"brecha": 0.8},
         "acumulada_emergente": {"brecha": 0.01}},
    ]
    serie = ess.unir_serie(koine, distancia)
    assert serie[0]["brecha"] == 0.0028 and serie[1]["brecha"] == 0.01
    assert serie[0]["emergente"] == 0.92
    # la brecha de un solo día es la de la lectura emergente del día
    assert serie[0]["brecha_dia"] == 0.8


def test_la_emergente_del_dia_es_la_media_de_todos_los_pares():
    del_dia = {"intra_global": 0.8, "pares_intra_global": 3, "entre": 0.9,
               "pares_entre": 1, "brecha": 0.1}
    serie = ess.unir_serie([(1, None, None, None)], [{"dia": 1, "emergente": del_dia}])
    assert serie[0]["emergente_dia"] == 0.825
    assert serie[0]["brecha"] is None


def test_dias_de_capubana_que_bajan_respecto_del_anterior():
    serie = [{"dia": d, "x": v} for d, v in [(2, 0.9), (3, 0.8), (5, 0.7), (6, 0.75)]]
    assert ess.dias_que_bajan(serie, "x", [3, 6, 9]) == {"bajan": 1, "de": 2}


def test_el_minimo_desempata_por_el_primer_dia():
    serie = [{"dia": 1, "e": 0.9}, {"dia": 2, "e": 0.5}, {"dia": 3, "e": 0.5},
             {"dia": 4, "e": None}]
    assert ess.minimo(serie, "e") == {"dia": 2, "valor": 0.5}
    assert ess.minimo([], "e") is None


def test_formas_que_no_cruzaron_no_cuentan_las_nacidas_en_los_dos_pueblos():
    formas = [
        {"clase": "exclusiva", "cruzo": False, "acunacion_multinodo": False},
        {"clase": "compartida", "cruzo": True, "acunacion_multinodo": False},
        {"clase": "compartida", "cruzo": False, "acunacion_multinodo": True},
        {"clase": "poco-atestiguada", "cruzo": False, "acunacion_multinodo": False},
    ]
    assert ess.resumen_de_formas(formas) == {
        "emergentes": 4, "clasificables": 3, "cruzaron": 1, "no_cruzaron": 1,
        "nacidas_en_los_dos": 1}


def test_la_competencia_guarda_el_dato_tal_cual_y_en_orden_de_llegada():
    koine = {"competencia": {"umbral": 0.55, "referentes": {
        "guacharaca": {"desc": "ave", "variantes": {"taka": 106.4},
                       "fijada": None, "fijada_dia": None},
        "tarantula_azul": {"desc": "araña", "variantes": {
            "oto-biro-oto": 31.0, "kule-biro-iro": 31.95, "**ula-kibe-bakoa**": 1.45,
            "hamaka-imo": 1.45}, "fijada": None, "fijada_dia": None},
        "delfin": {"desc": "delfín", "variantes": {"punu-dunku": 20.0, "x": 1.0},
                   "fijada": "punu-dunku", "fijada_dia": 5},
    }}}
    c = ess.competencia_del_estado(koine, ["tarantula_azul", "guacharaca", "delfin"])
    assert c["referentes"] == 3 and c["fijados"] == 1 and c["umbral"] == 0.55
    assert [a["concepto"] for a in c["lista"]] == ["tarantula_azul", "guacharaca", "delfin"]
    assert c["lista"][2]["fijada"] == "punu-dunku" and c["lista"][2]["fijada_dia"] == 5
    abiertos = [a for a in c["lista"] if not a["fijada"]]
    tar = abiertos[0]
    assert tar["n_variantes"] == 4
    assert [r["forma"] for r in tar["rivales"]] == [
        "kule-biro-iro", "oto-biro-oto", "**ula-kibe-bakoa**"]
    # Un nombre unánime queda abierto: es el defecto de evaluar_fijacion, y se
    # publica como está para que la página lo diga.
    assert abiertos[1]["n_variantes"] == 1


def test_sin_estado_no_hay_competencia():
    avisos = []
    assert ess.leer_estado(None, "x", "escena", avisos) is None
    assert avisos == []


def test_un_estado_de_otro_brazo_no_se_publica(tmp_path):
    import json
    (tmp_path / "curiana_state.json").write_text(
        json.dumps({"run_anterior": "otro-run", "referentes_introducidos": []}),
        encoding="utf-8")
    (tmp_path / "curiana_koine.json").write_text(
        json.dumps({"competencia": {"referentes": {}}}), encoding="utf-8")
    avisos = []
    assert ess.leer_estado(str(tmp_path), "hoja-de-la-cadena", "control", avisos) is None
    assert len(avisos) == 1 and "NO se publica" in avisos[0]
