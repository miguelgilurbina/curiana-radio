"""Tests del registro de nodos.

Lo que protegen: que no se pueda afirmar que un asentamiento existía en el
siglo XV sin decir por qué, y que un documento colonial no cuele como evidencia
precontacto. Todo el registro se apoya en cartas de 1538-1550 y la simulación
es del XIV-XV; sin estas dos reglas, "atestiguado" se desliza a "precontacto"
sin que nadie lo note.
"""

import compilar_asentamientos as CA


def _nodo(**kw):
    base = dict(id="nodo-001", forma="x", tipo="asentamiento", region="r",
                etiqueta="atestiguado", atestacion="colonial",
                precontacto="desconocido", rol="algo",
                procedencia={"obra": "oliver-1989-cap3"},
                etimologia="sin-resolver")
    base.update(kw)
    return base


# ── la regla que justifica el módulo ──────────────────────────────────

def test_precontacto_si_exige_razon():
    p = CA.validar_precontacto([_nodo(precontacto="si", atestacion="arqueologica")])
    assert any(x["codigo"] == "precontacto-sin-razon" for x in p)


def test_precontacto_si_con_razon_pasa():
    p = CA.validar_precontacto([_nodo(precontacto="si", atestacion="arqueologica",
                                      precontacto_razon="dabajuroide ~900 d.C.")])
    assert not [x for x in p if x["nivel"] == "error"]


def test_un_documento_colonial_no_prueba_precontacto():
    """Una carta de 1538 no dice nada de 1450. Regla 3 de CLAUDE.md."""
    p = CA.validar_precontacto([_nodo(precontacto="si", atestacion="colonial",
                                      precontacto_razon="lo dice Bastidas")])
    assert any(x["codigo"] == "precontacto-por-documento-colonial" for x in p)


def test_razon_sin_afirmacion_es_solo_aviso():
    p = CA.validar_precontacto([_nodo(precontacto="desconocido",
                                      precontacto_razon="sobra")])
    assert [x["nivel"] for x in p] == ["aviso"]


# ── vocabularios cerrados ─────────────────────────────────────────────

def test_los_campos_cerrados_rechazan_valores_nuevos():
    """Un campo con valores libres deja de poder agruparse — es el bug
    `taíno`/`taino` del lexicón (#93), y aquí no se repite."""
    p = CA.validar_vocabularios([_nodo(etiqueta="mas o menos")])
    assert any(x["codigo"] == "etiqueta-ilegal" for x in p)


def test_atestacion_arqueologica_es_legal():
    assert not CA.validar_vocabularios([_nodo(atestacion="arqueologica")])


# ── integridad referencial ────────────────────────────────────────────

def test_la_obra_citada_tiene_que_existir():
    p = CA.validar_procedencia([_nodo(procedencia={"obra": "inventada-1999"})],
                               {"oliver-1989-cap3"})
    assert any(x["codigo"] == "obra-fantasma" for x in p)


def test_el_hecho_del_corpus_citado_tiene_que_existir():
    p = CA.validar_corpus([_nodo(corpus=["geografia_politica-999"])],
                          {"geografia_politica-003"})
    assert any(x["codigo"] == "hecho-fantasma" for x in p)


def test_id_duplicado_es_error():
    p = CA.validar_estructura([_nodo(), _nodo()])
    assert any(x["codigo"] == "id-duplicado" for x in p)


# ── el registro real ──────────────────────────────────────────────────

def test_el_registro_real_valida():
    nodos, _, problemas = CA.compilar()
    errores = [p for p in problemas if p["nivel"] == "error"]
    assert not errores, errores
    assert len(nodos) >= 13


def test_quienes_sostienen_precontacto():
    """Cable-trampa sobre la afirmación más fuerte del registro.

    Hasta el 2026-08-24 este test decía `== {"curazao", "aruba", "bonaire"}` y
    su docstring afirmaba que solo las islas sostenían precontacto. Saltó al
    fusionar los 17 sitios del Apéndice E de Oliver (#92) — que es justo para
    lo que estaba puesto: "si esto cambia, es que entró evidencia nueva y hay
    que mirarla".

    La evidencia nueva son tres nodos CONTINENTALES con datación propia:
    la-maternidad (Tamers IVIC-626, A.D. 1450, sin material europeo según
    Cruxent), jose-gregorio-hernandez (ISGS-1253/1423, dos fechas en ventana) y
    santa-ana-el-cerro (IVIC-14/16/18, tres fechas, todas precontacto).

    La trampa sigue armada: si esta lista vuelve a cambiar, hay que mirar por
    qué. Y el invariante de abajo NO se toca — es la regla 3 en código."""
    nodos, _, _ = CA.compilar()
    con_pre = {n["forma"] for n in nodos if n.get("precontacto") == "si"}
    assert con_pre == {
        "curazao", "aruba", "bonaire",
        "la-maternidad", "jose-gregorio-hernandez", "santa-ana-el-cerro",
    }
    for n in nodos:
        if n.get("precontacto") == "si":
            assert n["atestacion"] == "arqueologica", (
                f"{n['forma']}: precontacto 'si' exige atestación arqueológica; "
                "un documento colonial no prueba existencia precontacto")
