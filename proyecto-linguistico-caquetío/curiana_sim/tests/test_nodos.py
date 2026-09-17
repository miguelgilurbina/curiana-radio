"""Tests de `analizar_nodos.py` — la lectura por nodo de la era 2.

Todo con datos SINTÉTICOS: dos nodos de tamaños distintos (como GUARANAO 39 y
AMUAY 24), formas compartidas y formas exclusivas. Ni base de datos ni elenco
real, porque lo que hay que vigilar es la aritmética:

  - que la clasificación NORMALICE por hablantes posibles del nodo — si no,
    el nodo grande se lleva todas las formas por censo y no por lengua;
  - que la distancia sepa distinguir pares intra-nodo de pares cruzados, y que
    dé None donde no hay pares en vez de dar cero;
  - que el cruce se feche por (día, turno) y que una forma acuñada a la vez en
    los dos nodos NO se cuente como cruzada.

Las funciones de base (`q`, `cargar_*`) no se testean aquí: son SQL, y su
guardián es que el comando corra.
"""
from collections import Counter

import pytest

import analizar_nodos as an

# Dos nodos deliberadamente desiguales: el punto entero del módulo.
POSIBLES = {"GRANDE": 39, "CHICO": 24}
NODO_DE = ({f"g{i}": "GRANDE" for i in range(39)} |
           {f"c{i}": "CHICO" for i in range(24)})


# ══════════════════════════════════════════════════════════════════════
# Clasificación — la normalización es el test
# ══════════════════════════════════════════════════════════════════════

def test_tasa_es_hablantes_sobre_posibles_del_nodo():
    tasas = an.tasas_por_nodo({"GRANDE": 39, "CHICO": 12}, POSIBLES)
    assert tasas["GRANDE"] == pytest.approx(1.0)
    assert tasas["CHICO"] == pytest.approx(0.5)


def test_mismo_conteo_crudo_en_nodos_desiguales_inclina_al_chico():
    """12 y 12 parecen empate; normalizado son 0.31 y 0.50 en favor del chico.
    Con el umbral por defecto (2.0) la razón 1.63 no alcanza para llamarla
    inclinada, pero el nodo de mayor prevalencia ya es el CHICO, no el que
    tiene más bocas."""
    r = an.clasificar_forma({"GRANDE": 12, "CHICO": 12}, POSIBLES)
    assert r["nodo_alto"] == "CHICO"
    assert r["razon"] == pytest.approx(39 / 24, abs=0.01)
    assert r["clase"] == "compartida"
    # y con un umbral más fino la misma cifra se declara inclinada al chico
    assert an.clasificar_forma({"GRANDE": 12, "CHICO": 12}, POSIBLES,
                               umbral=1.5)["nodo"] == "CHICO"


def test_conteos_muy_desiguales_que_normalizan_igual_son_compartida():
    """26 de 39 y 16 de 24 son la misma proporción: dos tercios cada uno."""
    r = an.clasificar_forma({"GRANDE": 26, "CHICO": 16}, POSIBLES)
    assert r["clase"] == "compartida"
    assert r["razon"] == pytest.approx(1.0, abs=0.01)


def test_inclinada_cuando_la_tasa_dobla_a_la_del_otro():
    # 0.5128 vs 0.2083 → razón 2.46
    r = an.clasificar_forma({"GRANDE": 20, "CHICO": 5}, POSIBLES)
    assert r["clase"] == "inclinada"
    assert r["nodo"] == "GRANDE"
    assert r["razon"] >= an.UMBRAL_INCLINACION


def test_justo_por_debajo_del_umbral_sigue_siendo_compartida():
    # 0.3846 vs 0.2083 → razón 1.85
    r = an.clasificar_forma({"GRANDE": 15, "CHICO": 5}, POSIBLES)
    assert r["clase"] == "compartida"
    assert r["razon"] < an.UMBRAL_INCLINACION


def test_el_umbral_es_un_parametro_y_mueve_el_veredicto():
    h = {"GRANDE": 15, "CHICO": 5}
    assert an.clasificar_forma(h, POSIBLES, umbral=2.0)["clase"] == "compartida"
    assert an.clasificar_forma(h, POSIBLES, umbral=1.5)["clase"] == "inclinada"


def test_exclusiva_cuando_el_otro_nodo_no_la_dice():
    r = an.clasificar_forma({"GRANDE": 0, "CHICO": 7}, POSIBLES)
    assert r["clase"] == "exclusiva"
    assert r["nodo"] == "CHICO"
    assert r["razon"] == float("inf")


def test_pocos_hablantes_no_se_clasifica():
    """Con dos bocas, «exclusiva» y «casualidad» son la misma frase."""
    r = an.clasificar_forma({"GRANDE": 0, "CHICO": 2}, POSIBLES)
    assert r["clase"] == "poco-atestiguada"
    assert r["nodo"] is None


def test_sin_usos_no_es_lo_mismo_que_poco_atestiguada():
    r = an.clasificar_forma({"GRANDE": 0, "CHICO": 0}, POSIBLES)
    assert r["clase"] == "sin-usos"


# ══════════════════════════════════════════════════════════════════════
# Distancia intra-nodo vs. entre nodos
# ══════════════════════════════════════════════════════════════════════

def _vec(**kw) -> Counter:
    return Counter(kw)


def test_formas_exclusivas_por_nodo_separan_los_nodos():
    """Cada nodo con su forma propia: la distancia entre nodos es máxima (los
    vectores no comparten nada) y la intra es cero."""
    vect = {
        "g0": _vec(a=3, b=2, c=1, d=1, e=1),
        "g1": _vec(a=3, b=2, c=1, d=1, e=1),
        "c0": _vec(p=3, q=2, r=1, s=1, t=1),
        "c1": _vec(p=3, q=2, r=1, s=1, t=1),
    }
    d = an.distancias_intra_entre(vect, NODO_DE)
    assert d["intra"]["GRANDE"] == pytest.approx(0.0)
    assert d["intra"]["CHICO"] == pytest.approx(0.0)
    assert d["entre"] == pytest.approx(1.0)
    assert d["brecha"] == pytest.approx(1.0)
    assert d["pares_intra_global"] == 2 and d["pares_entre"] == 4


def test_habla_identica_borra_la_brecha_entre_nodos():
    igual = _vec(a=2, b=2, c=2, d=2, e=2)
    vect = {"g0": Counter(igual), "g1": Counter(igual),
            "c0": Counter(igual), "c1": Counter(igual)}
    d = an.distancias_intra_entre(vect, NODO_DE)
    assert d["entre"] == pytest.approx(0.0)
    assert d["brecha"] == pytest.approx(0.0)


def test_una_forma_compartida_acerca_los_nodos_sin_juntarlos():
    """Con una forma en común la distancia entre nodos baja de 1, y sigue por
    encima de la intra: es el caso que el run real tiene que distinguir."""
    vect = {
        "g0": _vec(comun=5, a=1, b=1, c=1, d=1),
        "g1": _vec(comun=5, a=1, b=1, c=1, d=1),
        "c0": _vec(comun=5, p=1, q=1, r=1, s=1),
        "c1": _vec(comun=5, p=1, q=1, r=1, s=1),
    }
    d = an.distancias_intra_entre(vect, NODO_DE)
    assert 0.0 < d["entre"] < 1.0
    assert d["entre"] > d["intra_global"]


def test_min_formas_descarta_a_los_que_apenas_hablaron():
    vect = {"g0": _vec(a=1, b=1, c=1, d=1, e=1),
            "g1": _vec(a=1, b=1, c=1, d=1, e=1),
            "c0": _vec(a=1, b=1)}          # 2 formas: fuera con min_formas=5
    d = an.distancias_intra_entre(vect, NODO_DE, min_formas=5)
    assert d["n_agentes"] == 2
    assert d["entre"] is None              # no quedan pares cruzados
    assert d["intra"]["GRANDE"] == pytest.approx(0.0)


def test_sin_pares_cruzados_devuelve_None_y_no_cero():
    """Sin datos no es convergencia perfecta: el None tiene que sobrevivir."""
    vect = {"g0": _vec(a=1, b=1, c=1, d=1, e=1),
            "g1": _vec(a=1, b=1, c=1, d=1, e=1)}
    d = an.distancias_intra_entre(vect, NODO_DE)
    assert d["entre"] is None and d["brecha"] is None


def test_agente_sin_nodo_no_entra_en_ningun_par():
    vect = {"g0": _vec(a=1, b=1, c=1, d=1, e=1),
            "c0": _vec(a=1, b=1, c=1, d=1, e=1),
            "forastero": _vec(z=9, y=9, x=9, w=9, v=9)}
    d = an.distancias_intra_entre(vect, NODO_DE)
    assert d["n_agentes"] == 2
    assert d["pares_entre"] == 1


# ══════════════════════════════════════════════════════════════════════
# Vectores reconstruidos desde word_uses
# ══════════════════════════════════════════════════════════════════════

USOS = [
    {"dia": 1, "turno": 1, "agente": "g0", "forma": "taya", "usos": 2},
    {"dia": 1, "turno": 1, "agente": "g0", "forma": "nueva", "usos": 1},
    {"dia": 2, "turno": 1, "agente": "g0", "forma": "otra", "usos": 3},
]


def test_vectores_por_dia_separan_los_dias():
    v = an.vectores_por_dia(USOS)
    assert v[1]["g0"] == Counter(taya=2, nueva=1)
    assert v[2]["g0"] == Counter(otra=3)


def test_excluir_deja_solo_lo_emergente():
    v = an.vectores_por_dia(USOS, excluir=frozenset({"taya"}))
    assert v[1]["g0"] == Counter(nueva=1)


def test_acumulado_arrastra_los_dias_anteriores():
    v = an.vectores_por_dia(USOS, acumulado=True)
    assert v[1]["g0"] == Counter(taya=2, nueva=1)
    assert v[2]["g0"] == Counter(taya=2, nueva=1, otra=3)


# ══════════════════════════════════════════════════════════════════════
# Qué cuenta como forma emergente
# ══════════════════════════════════════════════════════════════════════

def test_lo_que_ensenan_las_plantillas_no_es_emergente():
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "ta-barsure", "usos": 9},
            {"dia": 1, "turno": 1, "agente": "g0", "forma": "kali-iro-pabu", "usos": 1}]
    em = an.formas_emergentes(usos, [], [], frozenset({"ta-barsure"}))
    assert em == {"kali-iro-pabu"}


def test_un_neologismo_que_nadie_reuso_sigue_siendo_forma_emergente():
    em = an.formas_emergentes([], [{"forma": "sima-naa"}], [], frozenset())
    assert "sima-naa" in em


def test_una_forma_fijada_en_koine_entra_aunque_este_en_el_vocabulario_base():
    em = an.formas_emergentes([], [], [{"forma": "kali-pica"}],
                              frozenset({"kali-pica"}))
    assert "kali-pica" in em


# ══════════════════════════════════════════════════════════════════════
# El perfil de una forma: acuñación y cruce
# ══════════════════════════════════════════════════════════════════════

def _perfil(usos, neos=(), **kw):
    return an.perfil_de_forma("x", list(usos), NODO_DE, POSIBLES,
                              sorted({u["dia"] for u in usos}) or [1],
                              list(neos), None,
                              kw.get("umbral", an.UMBRAL_INCLINACION),
                              kw.get("min_hablantes", an.MIN_HABLANTES),
                              kw.get("turnos_por_dia", 6))


def test_cruce_se_fecha_por_dia_y_turno():
    usos = [{"dia": 1, "turno": 2, "agente": "g0", "forma": "x", "usos": 1},
            {"dia": 1, "turno": 5, "agente": "g1", "forma": "x", "usos": 1},
            {"dia": 2, "turno": 3, "agente": "c0", "forma": "x", "usos": 1}]
    neos = [{"forma": "x", "acunador": "g0", "dia": 1, "turno": 2,
             "glosa": "", "estado": "adoptado"}]
    r = _perfil(usos, neos)
    assert r["nodos_acunadores"] == ["GRANDE"]
    assert r["origen_acunacion"] == "neologisms"
    assert (r["dia_cruce"], r["turno_cruce"]) == (2, 3)
    # (2−1)·6 + (3−2) = 7 turnos
    assert r["turnos_hasta_cruzar"] == 7
    assert r["cruzo"] is True


def test_forma_que_nunca_sale_de_su_nodo():
    usos = [{"dia": d, "turno": 1, "agente": f"g{i}", "forma": "x", "usos": 1}
            for d in (1, 2) for i in range(4)]
    r = _perfil(usos)
    assert r["cruzo"] is False
    assert r["clase"] == "exclusiva" and r["nodo_de_la_clase"] == "GRANDE"


def test_acunacion_simultanea_en_los_dos_nodos_no_es_un_cruce():
    """El evento de nombramiento enseña el referente a todos los activos del
    turno: si acuñan de los dos lados, la forma nació en los dos y no hay
    frontera que cruzar."""
    usos = [{"dia": 1, "turno": 5, "agente": "g0", "forma": "x", "usos": 1},
            {"dia": 1, "turno": 5, "agente": "c0", "forma": "x", "usos": 1}]
    neos = [{"forma": "x", "acunador": "g0", "dia": 1, "turno": 5,
             "glosa": "", "estado": "adoptado"},
            {"forma": "x", "acunador": "c0", "dia": 1, "turno": 5,
             "glosa": "", "estado": "adoptado"}]
    r = _perfil(usos, neos)
    assert r["acunacion_multinodo"] is True
    assert sorted(r["nodos_acunadores"]) == ["CHICO", "GRANDE"]
    assert r["cruzo"] is False and r["cruce_no_aplica"] is True
    assert r["turnos_hasta_cruzar"] is None


def test_sin_registro_de_neologismo_el_acunador_es_aproximado():
    usos = [{"dia": 1, "turno": 3, "agente": "c0", "forma": "x", "usos": 1},
            {"dia": 1, "turno": 4, "agente": "g0", "forma": "x", "usos": 1}]
    r = _perfil(usos)
    assert r["origen_acunacion"] == "primer-uso"
    assert r["nodos_acunadores"] == ["CHICO"]
    assert r["turnos_hasta_cruzar"] == 1


def test_el_desglose_por_dia_cuenta_hablantes_distintos_no_usos():
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "x", "usos": 5},
            {"dia": 1, "turno": 4, "agente": "g0", "forma": "x", "usos": 4},
            {"dia": 1, "turno": 4, "agente": "g1", "forma": "x", "usos": 1}]
    r = _perfil(usos)
    assert r["por_dia"]["1"]["GRANDE"] == {"usos": 10, "hablantes": 2,
                                           "tasa": pytest.approx(2 / 39, abs=1e-4)}
    assert r["usos_totales"] == 10


# ══════════════════════════════════════════════════════════════════════
# El barrido completo, con datos sintéticos de dos nodos
# ══════════════════════════════════════════════════════════════════════

def test_analizar_formas_separa_compartida_de_exclusiva():
    usos = []
    # `compartida`: la mitad de cada nodo, en los dos días
    for d in (1, 2):
        for i in range(20):
            usos.append({"dia": d, "turno": 1, "agente": f"g{i}",
                         "forma": "compartida", "usos": 1})
        for i in range(12):
            usos.append({"dia": d, "turno": 2, "agente": f"c{i}",
                         "forma": "compartida", "usos": 1})
    # `del_grande`: sólo en el nodo grande
    for i in range(10):
        usos.append({"dia": 1, "turno": 1, "agente": f"g{i}",
                     "forma": "del_grande", "usos": 1})
    # `ta-barsure`: de la plantilla, no debe salir en absoluto
    usos.append({"dia": 1, "turno": 1, "agente": "g0",
                 "forma": "ta-barsure", "usos": 30})

    filas = an.analizar_formas(usos, [], [], NODO_DE, POSIBLES,
                               frozenset({"ta-barsure"}))
    por_forma = {f["forma"]: f for f in filas}
    assert "ta-barsure" not in por_forma
    assert por_forma["compartida"]["clase"] == "compartida"
    assert por_forma["del_grande"]["clase"] == "exclusiva"
    assert por_forma["del_grande"]["nodo_de_la_clase"] == "GRANDE"
    # ordenadas por usos totales
    assert filas[0]["forma"] == "compartida"


def test_habla_por_nodo_mide_la_cuota_contra_el_censo():
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "a", "usos": 90},
            {"dia": 1, "turno": 1, "agente": "c0", "forma": "a", "usos": 10}]
    fila = an.habla_por_nodo(usos, NODO_DE, POSIBLES)[0]
    assert fila["nodos"]["GRANDE"]["cuota_de_usos"] == pytest.approx(0.9)
    assert fila["nodos"]["GRANDE"]["cuota_del_censo"] == pytest.approx(39 / 63, abs=1e-4)
    assert fila["nodos"]["CHICO"]["agentes_activos"] == 1


def test_cobertura_avisa_cuando_los_nombres_no_son_del_elenco():
    usos = [{"dia": 1, "turno": 1, "agente": "Biro-ko", "forma": "a", "usos": 9},
            {"dia": 1, "turno": 1, "agente": "g0", "forma": "a", "usos": 1}]
    cob = an.cobertura_del_elenco(usos, NODO_DE)
    assert cob["n_agentes_sin_nodo"] == 1
    assert cob["pct_usos_con_nodo"] == pytest.approx(10.0)


# ══════════════════════════════════════════════════════════════════════
# La divergencia sembrada (sí toca el elenco real: es lo que mide)
# ══════════════════════════════════════════════════════════════════════

def test_divergencia_sembrada_es_coherente_consigo_misma():
    """No fija el valor —que es un hallazgo y puede arreglarse— sino que la
    medición cuadre: los agentes con semilla propia son del elenco, el vector
    más común no puede tener más agentes que el elenco, y un nodo no puede
    tener más vectores distintos que agentes."""
    d = an.divergencia_sembrada()
    assert d["agentes"] == 63
    assert 1 <= d["vectores_semilla_distintos"] <= d["agentes"]
    assert d["agentes_con_el_vector_mas_comun"] <= d["agentes"]
    assert set(d["vectores_por_nodo"]) == {"GUARANAO", "AMUAY"}
    assert d["vectores_por_nodo"]["GUARANAO"] <= 39
    assert d["vectores_por_nodo"]["AMUAY"] <= 24
    assert set(d["nodos_con_semilla_propia"]) <= {"GUARANAO", "AMUAY"}
    assert set(d["con_emocionar_seed_propio"]) <= set(
        __import__("curiana_agents_era2").ALL_AGENTS)


# ══════════════════════════════════════════════════════════════════════
# Tendencia: ¿quién baja más rápido?
# ══════════════════════════════════════════════════════════════════════

def _serie(intra, entre):
    return [{"dia": i + 1,
             "ventana": {"intra_global": a, "entre": b, "intra": {},
                         "n_agentes": 10, "brecha": None}}
            for i, (a, b) in enumerate(zip(intra, entre))]


def test_entre_nodos_bajando_mas_rapido_se_detecta():
    t = an.tendencia(_serie([0.60, 0.59, 0.58], [0.70, 0.55, 0.40]), "ventana")
    assert t["veredicto"] == "entre-nodos-baja-mas-rapido"


def test_intra_bajando_mas_rapido_se_detecta():
    t = an.tendencia(_serie([0.60, 0.45, 0.30], [0.62, 0.61, 0.60]), "ventana")
    assert t["veredicto"] == "intra-nodo-baja-mas-rapido"


def test_bajar_a_la_par_no_es_koineizacion_entre_nodos():
    t = an.tendencia(_serie([0.60, 0.50, 0.40], [0.61, 0.51, 0.41]), "ventana")
    assert t["veredicto"] == "bajan-igual"


def test_un_solo_dia_no_da_tendencia():
    t = an.tendencia(_serie([0.60], [0.61]), "ventana")
    assert t["veredicto"] == "insuficiente"


def test_los_dias_sin_pares_cruzados_no_cuentan_como_puntos():
    serie = _serie([0.60, 0.50], [0.61, 0.51])
    serie[0]["ventana"]["entre"] = None
    assert an.tendencia(serie, "ventana")["veredicto"] == "insuficiente"


# ══════════════════════════════════════════════════════════════════════
# La cadena hacia atrás (sin base: se sustituye `q`)
# ══════════════════════════════════════════════════════════════════════

def test_cadena_de_runs_sube_hasta_la_raiz(monkeypatch):
    base = {
        "ccc": {"id": "ccc", "padre": "bbb"},
        "bbb": {"id": "bbb", "padre": "aaa"},
        "aaa": {"id": "aaa", "padre": ""},
    }

    def falso_q(sql):
        rid = sql.split("where id = '")[1].split("'")[0]
        fila = dict(base[rid])
        fila.update(total_days="1", started_at="", elenco="era2", perfil="era2",
                    semilla="1", turnos_por_dia="6", motor_commit="deadbeef")
        return [fila]

    monkeypatch.setattr(an, "q", falso_q)
    assert [r["id"] for r in an.cadena_de_runs("ccc")] == ["aaa", "bbb", "ccc"]


def test_un_ciclo_en_continuado_desde_falla_a_la_vista(monkeypatch):
    def falso_q(sql):
        rid = sql.split("where id = '")[1].split("'")[0]
        return [{"id": rid, "padre": "aaa" if rid == "bbb" else "bbb",
                 "total_days": "1", "started_at": "", "elenco": "era2",
                 "perfil": "era2", "semilla": "1", "turnos_por_dia": "6",
                 "motor_commit": ""}]

    monkeypatch.setattr(an, "q", falso_q)
    with pytest.raises(SystemExit):
        an.cadena_de_runs("aaa")


# ══════════════════════════════════════════════════════════════════════
# La escena (`--lugar`): ocupación, escenas con voz y cruce por LUGAR
# ══════════════════════════════════════════════════════════════════════
#
# Datos sintéticos otra vez, y por la misma razón: lo que hay que vigilar es la
# aritmética. Dos aldeas de nodos distintos y un cerro que tocan las dos —el
# Capubana del canon—, dos días de dos momentos cada uno.

def _p(dia, turno, momento, agente, lugar, nodo):
    return {"dia": dia, "turno": turno, "momento": momento, "agente": agente,
            "lugar": lugar, "nodo": nodo, "run": "r1"}


PRESENCIAS = [
    # día 1, amanecer: cada nodo en lo suyo
    _p(1, 1, "amanecer", "g0", "Moruy", "GRANDE"),
    _p(1, 1, "amanecer", "g1", "Moruy", "GRANDE"),
    _p(1, 1, "amanecer", "c0", "Caseto", "CHICO"),
    # día 1, mediodía: los dos nodos en el cerro, el mismo turno
    _p(1, 2, "mediodía", "g0", "Capubana", "GRANDE"),
    _p(1, 2, "mediodía", "g1", "Moruy", "GRANDE"),
    _p(1, 2, "mediodía", "c0", "Capubana", "CHICO"),
    # día 2
    _p(2, 1, "amanecer", "g0", "Moruy", "GRANDE"),
    _p(2, 1, "amanecer", "g1", "Moruy", "GRANDE"),
    _p(2, 1, "amanecer", "c0", "Caseto", "CHICO"),
    _p(2, 2, "mediodía", "c0", "Caseto", "CHICO"),
]


def test_los_momentos_salen_del_turno_en_que_ocurren():
    assert an.orden_de_momentos(PRESENCIAS) == ["amanecer", "mediodía"]


def test_la_ocupacion_es_media_por_dia_y_no_total_de_la_cadena():
    """Dos días de cadena doblarían los conteos crudos y parecería que el mundo
    se llenó: Moruy tiene 2 personas al amanecer, no 4."""
    ocup = {f["lugar"]: f for f in an.ocupacion_por_lugar(PRESENCIAS)}
    assert ocup["Moruy"]["por_momento"]["amanecer"]["presencias"] == 4
    assert ocup["Moruy"]["por_momento"]["amanecer"]["media_por_dia"] == 2.0
    assert ocup["Caseto"]["por_momento"]["amanecer"]["media_por_dia"] == 1.0
    assert ocup["Capubana"]["nodos"] == ["CHICO", "GRANDE"]
    assert ocup["Moruy"]["agentes_distintos"] == 2


def test_compartido_es_el_lugar_que_tocan_los_dos_nodos_a_la_vez():
    """La distinción de §3.4: un lugar que los dos nodos pisan en turnos
    distintos no produce contacto, sólo coincidencia en el plano."""
    comp = an.lugares_compartidos(PRESENCIAS)
    assert comp["compartidos"] == ["Capubana"]
    assert comp["compartidos_simultaneos"] == ["Capubana"]
    assert comp["turnos_con_dos_nodos"] == 1

    # el mismo cerro, pero cada nodo en un turno: compartido, NO simultáneo
    en_turnos_distintos = [
        _p(1, 1, "amanecer", "g0", "Capubana", "GRANDE"),
        _p(1, 2, "mediodía", "c0", "Capubana", "CHICO"),
    ]
    comp2 = an.lugares_compartidos(en_turnos_distintos)
    assert comp2["compartidos"] == ["Capubana"]
    assert comp2["compartidos_simultaneos"] == []
    assert comp2["turnos_con_dos_nodos"] == 0


def test_una_escena_con_una_sola_voz_no_es_conversacion():
    """Una escena es (día, turno, lugar) con alguien dentro. La cifra que
    importa es por HABLANTE: cuántas intervenciones caen donde ese turno habla
    alguien más."""
    hablantes = [
        {"dia": 1, "turno": 1, "agente": "g0", "lugar": ""},
        {"dia": 1, "turno": 1, "agente": "g1", "lugar": ""},   # los dos en Moruy
        {"dia": 1, "turno": 1, "agente": "c0", "lugar": ""},   # solo, en Caseto
    ]
    esc = an.escenas_del_turno(PRESENCIAS, hablantes)
    # d1t1: Moruy, Caseto · d1t2: Capubana, Moruy · d2t1: Moruy, Caseto · d2t2: Caseto
    assert esc["escenas"] == 7
    assert esc["escenas_con_voz"] == 2
    assert esc["escenas_con_dos_o_mas_voces"] == 1
    assert esc["voces_max_en_una_escena"] == 2
    assert esc["intervenciones_ubicadas"] == 3
    assert esc["intervenciones_con_compania"] == 2
    assert esc["pct_con_compania"] == pytest.approx(66.7, abs=0.1)


def test_un_hablante_sin_presencia_se_cuenta_y_no_se_ubica():
    """El guardián barato: si habló alguien que no estaba en la escena, se ve."""
    hablantes = [{"dia": 1, "turno": 1, "agente": "fantasma", "lugar": ""}]
    esc = an.escenas_del_turno(PRESENCIAS, hablantes)
    assert esc["hablantes_sin_presencia"] == 1
    assert esc["intervenciones_ubicadas"] == 0


def test_el_lugar_declarado_que_discrepa_de_la_presencia_se_cuenta():
    hablantes = [{"dia": 1, "turno": 1, "agente": "g0", "lugar": "Caseto"},
                 {"dia": 1, "turno": 1, "agente": "g1", "lugar": "Moruy"}]
    esc = an.escenas_del_turno(PRESENCIAS, hablantes)
    assert esc["respuestas_con_lugar_declarado"] == 2
    assert esc["lugar_declarado_discrepa"] == 1


def _cruce(usos, compartidos=("Capubana",)):
    return an.cruce_por_lugar(list(usos), PRESENCIAS, frozenset(), [], [],
                              set(compartidos), turnos_por_dia=2)


def test_una_forma_que_no_sale_de_su_lugar_muere_en_el():
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "x", "usos": 1},
            {"dia": 2, "turno": 1, "agente": "g1", "forma": "x", "usos": 1}]
    r = _cruce(usos)[0]
    assert r["lugares_natales"] == ["Moruy"] and r["n_lugares"] == 1
    assert r["murio_en_su_lugar"] is True
    assert r["turnos_hasta_salir"] is None
    assert r["paso_por_compartido"] is False


def test_la_salida_del_lugar_se_fecha_en_turnos():
    """g0 la dice en Moruy al amanecer del día 1 y en el Capubana al mediodía:
    (1−1)·2 + (2−1) = 1 turno hasta salir, y el lugar de salida es compartido."""
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "x", "usos": 1},
            {"dia": 1, "turno": 2, "agente": "g0", "forma": "x", "usos": 1}]
    r = _cruce(usos)[0]
    assert r["lugares_natales"] == ["Moruy"]
    assert (r["dia_salida"], r["turno_salida"], r["lugar_salida"]) == (1, 2, "Capubana")
    assert r["turnos_hasta_salir"] == 1
    assert r["lugares_compartidos_tocados"] == ["Capubana"]


def test_nacer_en_dos_lugares_a_la_vez_no_es_salir_de_ninguno():
    """El análogo por lugar de `acunacion_multinodo`: si la forma sonó en dos
    sitios en el mismo turno, no nació en ninguno y «salir» no significa nada."""
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "x", "usos": 1},
            {"dia": 1, "turno": 1, "agente": "c0", "forma": "x", "usos": 1}]
    r = _cruce(usos)[0]
    assert r["nacimiento_multilugar"] is True
    assert sorted(r["lugares_natales"]) == ["Caseto", "Moruy"]
    assert r["turnos_hasta_salir"] is None
    assert r["murio_en_su_lugar"] is False


def test_un_uso_sin_presencia_no_se_ubica_y_no_se_inventa():
    usos = [{"dia": 9, "turno": 9, "agente": "g0", "forma": "x", "usos": 1}]
    r = _cruce(usos)[0]
    assert r["ubicable"] is False
    resumen = an.resumen_cruce_por_lugar([r])
    assert resumen["sin_ubicar"] == 1 and resumen["ubicables"] == 0


def test_el_resumen_cuenta_lo_que_la_tabla_dice():
    usos = [{"dia": 1, "turno": 1, "agente": "g0", "forma": "viaja", "usos": 1},
            {"dia": 1, "turno": 2, "agente": "g0", "forma": "viaja", "usos": 1},
            {"dia": 1, "turno": 1, "agente": "c0", "forma": "quieta", "usos": 1},
            {"dia": 2, "turno": 2, "agente": "c0", "forma": "quieta", "usos": 1}]
    resumen = an.resumen_cruce_por_lugar(_cruce(usos))
    assert resumen["formas"] == 2 and resumen["ubicables"] == 2
    assert resumen["salieron_de_su_lugar"] == 1
    assert resumen["murieron_en_su_lugar"] == 1
    assert resumen["pasaron_por_compartido"] == 1
    assert resumen["turnos_hasta_salir_mediana"] == 1
