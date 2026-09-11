"""Tests del registro de vecinos.

Lo que protegen: que no se pueda atribuir un pueblo a la polity costera —la
que simula el motor— sin una fuente que lo documente o sin declararlo
canon-simulación. Casi todo el contacto documentado es de los Llanos, de
Maracaibo o de Yaracuy; sin esta regla, un vecino de Barquisimeto se desliza
al Golfete sin que nadie lo note (regla 4 de CLAUDE.md).
"""

import compilar_etnias as CE
import curiana_polities as CP


def _etnia(**kw):
    base = dict(id="etnia-001", nombre="x", etiqueta="atestiguado",
                familia_linguistica="caribe", donde="por ahí",
                polity_caquetia="occidental", tipo_de_contacto="mercado",
                intensidad="media",
                procedencia={"obra": "oliver-1989-cap3-vecinos"})
    base.update(kw)
    return base


# ── la regla que justifica el módulo ──────────────────────────────────

def test_la_costera_sin_fuente_ni_decision_es_error():
    """Un vecino de la Curiana sin fuente ni etiqueta de simulación es
    fanfiction que pasa por dato."""
    p = CE.validar_polity([_etnia(polity_caquetia="costera", procedencia=None,
                                  deuda="sin-procedencia")])
    assert any(x["codigo"] == "costera-sin-decision" for x in p)


def test_la_costera_con_fuente_pasa():
    p = CE.validar_polity([_etnia(polity_caquetia="costera")])
    assert not [x for x in p if x["nivel"] == "error"]


def test_la_costera_como_canon_simulacion_pasa_si_declara_la_deuda():
    p = CE.validar_polity([_etnia(polity_caquetia="costera", procedencia=None,
                                  etiqueta="canon-simulacion",
                                  deuda="sin-procedencia")])
    assert not [x for x in p if x["nivel"] == "error"]


def test_canon_simulacion_sin_deuda_es_error():
    """Lo inventado se declara inventado (regla 8)."""
    p = CE.validar_polity([_etnia(etiqueta="canon-simulacion", procedencia=None)])
    assert any(x["codigo"] == "canon-simulacion-sin-deuda" for x in p)


def test_o_cita_o_debe_no_las_dos():
    p = CE.validar_polity([_etnia(deuda="sin-procedencia")])
    assert any(x["codigo"] == "deuda-con-fuente" for x in p)


def test_sin_fuente_hay_que_declarar_la_deuda():
    p = CE.validar_polity([_etnia(procedencia=None)])
    assert any(x["codigo"] == "sin-procedencia-ni-deuda" for x in p)


def test_una_polity_no_costera_con_fuente_no_necesita_decision():
    p = CE.validar_polity([_etnia(polity_caquetia="llanos")])
    assert not p


# ── vocabularios cerrados ─────────────────────────────────────────────

def test_los_campos_cerrados_rechazan_valores_nuevos():
    """Un campo con valores libres deja de poder agruparse — es el bug
    `taíno`/`taino` del lexicón (#93), y aquí no se repite."""
    p = CE.validar_vocabularios([_etnia(polity_caquetia="llanos (NO la costera)")])
    assert any(x["codigo"] == "polity_caquetia-ilegal" for x in p)
    p = CE.validar_vocabularios([_etnia(familia_linguistica="caribe (Perijá)")])
    assert any(x["codigo"] == "familia_linguistica-ilegal" for x in p)


def test_las_polities_del_motor_son_el_vocabulario():
    """`curiana_polities.py` es el canon de las polities; si aparece una
    sexta allí, este validador tiene que saberlo, y al revés. `occidental`
    entró a las dos el 2026-09-07 (esfera futura, decisión de Miguel)."""
    assert set(CP.POLITIES) == set(CE.POLITIES)
    assert CE.POLITY_SIMULADA == CP.POLITY_SIMULADA
    assert CP.polity("occidental").estado == "futura"


# ── integridad referencial ────────────────────────────────────────────

def test_la_obra_citada_tiene_que_existir():
    p = CE.validar_procedencia([_etnia(procedencia={"obra": "inventada-1999"})],
                               {"oliver-1989-cap3-vecinos"})
    assert any(x["codigo"] == "obra-fantasma" for x in p)


def test_la_via_citada_tiene_que_existir():
    p = CE.validar_procedencia(
        [_etnia(procedencia={"obra": "federmann-1916", "via": "nadie-2000"})],
        {"federmann-1916"})
    assert any(x["codigo"] == "via-fantasma" for x in p)


def test_el_hecho_del_corpus_citado_tiene_que_existir():
    p = CE.validar_referencias([_etnia(ver_tambien=["geografia_politica-999"])],
                               {"geografia_politica-013"})
    assert any(x["codigo"] == "hecho-fantasma" for x in p)


def test_el_archivo_citado_tiene_que_existir(tmp_path):
    (tmp_path / "existe.yaml").write_text("a: 1", encoding="utf-8")
    p = CE.validar_referencias(
        [_etnia(ver_tambien=["existe.yaml#prop-007", "existe.yaml (§5)",
                             "no-existe.yaml"])],
        set(), repo=str(tmp_path))
    assert [x["codigo"] for x in p] == ["archivo-fantasma"]
    assert "no-existe.yaml" in p[0]["mensaje"]


def test_id_y_nombre_duplicados_son_error():
    p = CE.validar_estructura([_etnia(), _etnia()])
    codigos = {x["codigo"] for x in p}
    assert {"id-duplicado", "nombre-duplicado"} <= codigos


# ── el registro real ──────────────────────────────────────────────────

def test_el_registro_real_valida():
    etnias, meta, problemas = CE.compilar()
    errores = [p for p in problemas if p["nivel"] == "error"]
    assert not errores, errores
    assert meta.get("estado") == "canon"
    assert len(etnias) >= 8


def test_quienes_tocan_la_costera():
    """Cable-trampa sobre la afirmación que la simulación consume.

    Al cerrar B.6 (2026-09-07) ningún pueblo DOCUMENTADO toca la polity
    costera: los caribes están al sur y oeste de Maracaibo, los cuibas en los
    Llanos, los ciparicotos en Yaracuy. El único que la toca es el caribe del
    elenco, y es canon-simulación. Si esta lista cambia, es que entró evidencia
    nueva (un vecino documentado en el Golfete) y hay que mirarla; el
    invariante de abajo no se toca — es la regla 4 en código."""
    etnias, _, _ = CE.compilar()
    costera = {e["nombre"] for e in etnias if e["polity_caquetia"] == "costera"}
    assert costera == {"caribe del elenco"}
    for e in etnias:
        if e["polity_caquetia"] == "costera":
            assert e["etiqueta"] == "canon-simulacion" or e["procedencia"]["obra"], (
                f"{e['nombre']}: toca la costera sin fuente ni decisión")
