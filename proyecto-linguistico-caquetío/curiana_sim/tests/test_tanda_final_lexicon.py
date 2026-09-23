"""La última tanda antes de la corrida base (2026-09-23): el canon del LEXICÓN.

Decisiones de Miguel en `6-fusion/decisiones_tanda_final_2026-09-23.yaml`
(tf.0 el paquete entero, tf.6 la tanda de fuentes) y en
`6-fusion/decisiones_cierre_2026-09-23.yaml` (cc.3 poporo, cc.4 la sigla E,
cc.6 coro, cc.7 Zayas). Un test por punto aplicado:

  A · la tanda de fuentes — `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml`
      y la nota de `daca` (medida en
      `6-fusion/issues-pendientes/d11-fase3-pronombres-aspectos-2026-09-23.md`)
  B · `baperon` y `raporon` son de los pemenos (tf.0; el precedente es
      `datihao`, db.2)
  C · la sigla (E) de Zavala es Esteves, opción B — medida en
      `6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml`, recomendación junta
      «1-B, 2-a, 3-a, 4-a, 5-a, 6-a» del issue
      `6-fusion/issues-pendientes/sigla-E-zavala-canon-2026-09-23.md`
      (3-a y 5-a no son de esta parcela).
"""

import curiana_lexicon as L
from curiana_database import normalize_source_language
from curiana_lexicon import (
    FUERA_DEL_HABLA,
    VOCABULARIO_BASE,
    LexicoComunitario,
    es_forma_de_plantilla,
    score_linguistico,
)


def _sig(clave, tabla=VOCABULARIO_BASE):
    e = tabla[clave]
    return e.get("sig") or e.get("es")


# ══════════════════════════════════════════════════════════════════════
# A · la tanda de fuentes (tf.6: cc.3, cc.6, cc.7) y `daca`
# ══════════════════════════════════════════════════════════════════════

def test_a_poporo_sale_del_habla_como_espanol_colonial():
    """cc.3, opción A: ninguna fuente pone el poporo en manos de un caquetío,
    así que la etiqueta era FALSA y se corrige al archivar (no es el archivo
    de d19.b, que deja la capa intacta porque la capa era verdad)."""
    assert "poporo" not in VOCABULARIO_BASE
    e = FUERA_DEL_HABLA["poporo"]
    assert e["fuente"] == "español-colonial"
    assert _sig("poporo", FUERA_DEL_HABLA).startswith("calabacito de la cal")
    assert "chichón" in _sig("poporo", FUERA_DEL_HABLA)
    assert e["archivada"].startswith("2026-09-23")
    # la glosa y la cita viejas se conservan, dichas como lo que fueron
    assert "maza-porra, arma de combate ceremonial" in e["notas"]
    assert "guanebucán" in e["notas"] and "p. 202" in e["notas"]
    # archivada = puerta: no vuelve como acuñación
    assert es_forma_de_plantilla("poporo")
    assert "poporo" not in score_linguistico(
        "taya poporo yama", LexicoComunitario())["palabras_caquetias"]


def test_a_macana_ya_no_dice_que_el_poporo_es_la_voz_caquetia_del_arma():
    """La frase falsa se sustituye y la historia de la etiqueta se marca; la
    etiqueta y la glosa NO se tocan (la decisión de clase de los tainismos
    sigue abierta)."""
    e = VOCABULARIO_BASE["macana"]
    assert e["fuente"] == "caquetío-reconstruido"
    assert _sig("macana").startswith("macana, garrote")
    assert "La voz caquetía ATESTIGUADA para el arma es `poporo`" not in e["notas"]
    assert "CORREGIDO 2026-09-23 (cc.3)" in e["notas"]
    assert "análoga al poporo caquetío [falso: ver 2026-09-23]" in e["notas"]
    assert "Uriorebuí" in e["notas"] and "BAE p. 200" in e["notas"]


def test_a_coro_viento_sale_de_la_disputa_y_queda_descartada_en_notas():
    """cc.6: 'viento' es el latín cōrus/caurus de Castellanos, no una glosa
    caquetía. La glosa enseñada, la capa y la clave no se tocan."""
    e = VOCABULARIO_BASE["coro"]
    assert e["sig"] == "espina"
    assert e["fuente"] == "caquetío-hipotético"
    assert e["lectura_en_disputa"].startswith("dos lecturas compiten")
    assert "viento" not in e["lectura_en_disputa"]
    assert "DESCARTADA 2026-09-23 (cc.6" in e["notas"]
    assert "BAE 1857 p. 185" in e["notas"]
    assert "cōrus/caurus" in e["notas"]
    assert "No es de Oviedo" in e["notas"]


def test_a_cohiba_se_archiva_y_entra_cohoba():
    """cc.7, opción A: «la atestiguada manda». `cohiba` es forma del editor de
    1855 y de Pichardo; la de los cronistas es `cohoba`, el polvo y el rito."""
    assert "cohiba" not in VOCABULARIO_BASE
    viejo = FUERA_DEL_HABLA["cohiba"]
    assert viejo["fuente"] == "taíno", "archivar no cambia la capa"
    assert viejo["archivada"].startswith("2026-09-23")
    assert "Brinton 1871" in viejo["notas"], "la procedencia vieja se conserva"
    assert "t. IV p. 604" in viejo["notas"]

    nuevo = VOCABULARIO_BASE["cohoba"]
    assert nuevo["fuente"] == "taíno"
    assert _sig("cohoba").startswith("polvo que se aspira")
    assert "tabaco" not in _sig("cohoba")
    for cita in ("Pané, cap. XI", "Apologética p. 445", "p. 143", "p. 347"):
        assert cita in nuevo["notas"], cita

    # los conjuntos de la forma de la esfera nombran la clave nueva
    assert "cohoba" in L.SE_QUEDA_CON_SU_GRAFIA
    assert "cohiba" not in L.SE_QUEDA_CON_SU_GRAFIA
    for tabla in (L.FORMA_DE_LA_ESFERA, L.SIN_FORMA_DE_LA_ESFERA):
        assert "cohiba" not in tabla and "cohoba" not in tabla
    formas = {f for _p, f, _g, _fam in L.voces_de_fuera_posibles()}
    assert "cohoba" in formas and "cohiba" not in formas
    # la vieja no vuelve como acuñación; la nueva cuenta como esfera
    assert es_forma_de_plantilla("cohiba")
    r = score_linguistico("taya cohoba wana-ka yama", LexicoComunitario())
    assert r["prestamos_de_esfera"] == ["cohoba"]


def test_a_manati_sigue_taino_con_el_conflicto_declarado():
    e = VOCABULARIO_BASE["manati"]
    assert e["fuente"] == "taíno"
    assert "NBAE 13 p. 27" in e["notas"] and "p. 434" in e["notas"]
    assert "Goeje 1939 p. 14" in e["notas"]


def test_a_tabako_gana_el_rollo_y_cierra_lo_que_zayas_dejaba_abierto():
    e = VOCABULARIO_BASE["tabako"]
    assert e["fuente"] == "taíno"
    assert _sig("tabako") == ("el rollo de hojas encendido que se fuma, el cañuto "
                              "con que se toma el humo, y la ahumada misma (no la hierba)")
    assert "CERRADO 2026-09-23 (cc.7)" in e["notas"]
    assert "Apologética p. 181" in e["notas"] and "t. IV p. 96" in e["notas"]


def test_a_las_voces_de_zayas_sin_clave_no_entran_por_la_puerta_de_atras():
    """`bagua`, `anaki`, `anua` y `manaya` no son claves del lexicón: su
    etiqueta se decide en la lista maestra, y el lexicón no gana entradas que
    nadie mandó fusionar (`bagua` en el habla de la esfera queda para Miguel)."""
    for voz in ("bagua", "anaki", "anua", "aura", "manaya"):
        assert voz not in VOCABULARIO_BASE, voz
        assert voz not in FUERA_DEL_HABLA, voz


def test_a_daca_tiene_un_solo_testigo_de_la_frase():
    """La nota decía «Segunda mano independiente: Pané», y es falso: Las Casas
    copia a Pané en la misma p. 447. La frase es de Pané; la glosa 'yo', de
    Las Casas; la única segunda atestación posible es la frase de Esquivel
    (Goeje 1939 p. 17, cronista sin identificar)."""
    e = VOCABULARIO_BASE["daca"]
    assert e["fuente"] == "taíno" and _sig("daca") == "yo"
    assert "Segunda mano independiente: Pané, cap. XXV, la misma frase —" not in e["notas"]
    assert "UN SOLO TESTIGO" in e["notas"]
    assert "Todo esto refiere fray Ramón" in e["notas"]
    assert "Goeje 1939 p. 17" in e["notas"] and "Esquivel" in e["notas"]
    assert "sin identificar" in e["notas"]


# ══════════════════════════════════════════════════════════════════════
# B · `baperon` y `raporon` → los pemenos (tf.0, como `datihao` en db.2)
# ══════════════════════════════════════════════════════════════════════

def test_b_baperon_y_raporon_son_de_los_pemenos_y_los_aplica_el_generador():
    """El cuerpo de Oviedo (t. II pp. 286 y 294) los pone entre los pemenos
    del sur de la laguna; «(Lengua de Venezuela)» es del editor. La etiqueta
    la escribe el generador (`FUENTE_CURADA`), nunca una mano sobre el módulo
    generado."""
    import lexicon_zavala as Z
    import minar_zavala_glosario as M

    assert "caribe-pemeno" in L.FUENTES_CANONICAS
    for voz in ("baperon", "raporon"):
        assert M.FUENTE_CURADA[voz]["fuente"] == "caribe-pemeno"
        assert Z.GLOSARIO_ZAVALA[voz]["fuente"] == "caribe-pemeno"
        e = VOCABULARIO_BASE[voz]
        assert e["fuente"] == "caribe-pemeno"
        assert _sig(voz) == "calabaza con cal", "la glosa no se toca"
        assert "pemenos" in e["notas"] and "p. 294" in e["notas"]
        assert "datihao" in e["notas"]
        # con «caribe» en el nombre la resuelve el motor sin tocarlo: esfera
        # de contacto (no penaliza, se mide aparte) y NO proto-arahuaco, que
        # es lo que habría dicho el `return` por defecto de una etiqueta nueva
        assert normalize_source_language(e["fuente"]) == "caribe-continental"
        assert normalize_source_language(e["fuente"]) in L.ESFERA_DE_CONTACTO
    assert normalize_source_language("pemeno") == "proto-arahuaco"
    r = score_linguistico("taya baperon wana-ka yama", LexicoComunitario())
    assert r["prestamos_de_esfera"] == ["baperon"]
    assert "baperon" not in r["palabras_caquetias"]
    assert r["otro_arahuaco"] == 0
