"""Tests del compilador/validador del corpus cultural (compilar_corpus.py).

Dos mitades, y la segunda es la que importa:

1. **El corpus real valida.** Se corre sobre `3-mundo/corpus/` y se exige cero
   errores. Es la condición 4 del gate: si alguien rompe un `id`, mueve una
   locación o cita un hecho que no existe, esta prueba lo dice.

2. **El validador detecta cada rotura.** Un validador que nunca falla y un
   validador que no valida nada se ven exactamente igual desde fuera. Así que
   por cada regla hay un corpus mínimo, construido a mano, con la rotura
   metida a propósito — y se exige que salga el código de error correcto.
"""

import os

import pytest
import yaml

from compilar_corpus import (
    ETIQUETAS_FUENTE,
    cargar,
    compilar,
    fusionar,
    validar_agentes,
    validar_enganche_motor,
    validar_estructura,
    validar_etiquetas,
    validar_genealogia,
    validar_referencias_cruzadas,
    validar_rutas,
)

CORPUS_REAL = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", "3-mundo", "corpus",
)


def _hecho(**kw):
    """Un hecho válido mínimo, al que cada test le mete su rotura."""
    base = {
        "id": "parentesco-001",
        "contenido": "Un hecho cualquiera.",
        "fuente": "atestiguado",
        "referencia": "Oliver 1989, cap. 3, p. 255",
        "dominios": ["parentesco"],
        "agentes_relacionados": [],
        "_archivo": "parentesco.yaml",
        "_seccion": None,
    }
    base.update(kw)
    return base


def _codigos(problemas, nivel=None):
    return {p.codigo for p in problemas if nivel is None or p.nivel == nivel}


# ══════════════════════════════════════════════════════════════════════
# 1. El corpus real
# ══════════════════════════════════════════════════════════════════════

def test_corpus_real_valida_sin_errores():
    """La condición 4 del gate: 161 hechos y cero errores."""
    hechos, genealogia, problemas = compilar(CORPUS_REAL)
    errores = [p for p in problemas if p.nivel == "error"]
    assert not errores, "el corpus real tiene errores:\n" + "\n".join(
        f"  {p}" for p in errores)
    assert len(hechos) > 150, f"solo se cargaron {len(hechos)} hechos"
    assert genealogia is not None


def test_corpus_real_solo_usa_etiquetas_legales():
    hechos, _, _ = compilar(CORPUS_REAL)
    usadas = {h["fuente"] for h in hechos}
    assert usadas <= set(ETIQUETAS_FUENTE), f"etiquetas ilegales: {usadas - set(ETIQUETAS_FUENTE)}"


def test_corpus_real_ids_unicos():
    hechos, _, _ = compilar(CORPUS_REAL)
    ids = [h["id"] for h in hechos]
    assert len(ids) == len(set(ids)), "hay ids repetidos en el corpus"


def test_cargar_registra_origen_de_cada_hecho():
    """Sin `_archivo` el informe no puede señalar dónde está el problema."""
    hechos, _, problemas = cargar(CORPUS_REAL)
    assert not problemas
    assert all(h.get("_archivo") for h in hechos)
    # ecologia.yaml es el único con secciones; sus huecos deben traerla.
    huecos = [h for h in hechos if h.get("_seccion") == "huecos_lexicos"]
    assert huecos, "no se cargó la sección huecos_lexicos de ecologia.yaml"


def test_fusionado_es_yaml_reparseable_y_lleva_censo():
    hechos, genealogia, problemas = compilar(CORPUS_REAL)
    doc = fusionar(hechos, genealogia, problemas)
    vuelta = yaml.safe_load(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False))
    assert vuelta["meta"]["hechos"] == len(hechos)
    assert sum(vuelta["meta"]["por_etiqueta"].values()) == len(hechos)
    assert vuelta["meta"]["errores"] == 0
    # Los campos internos no se filtran al documento publicado.
    assert all(not k.startswith("_") for h in vuelta["hechos"] for k in h)
    assert all(h.get("archivo") for h in vuelta["hechos"])


# ══════════════════════════════════════════════════════════════════════
# 2. Cada regla detecta su rotura
# ══════════════════════════════════════════════════════════════════════

def test_detecta_campo_obligatorio_ausente():
    h = _hecho()
    del h["referencia"]
    assert "campo-falta" in _codigos(validar_estructura([h]))


def test_detecta_campo_obligatorio_vacio():
    assert "campo-vacio" in _codigos(validar_estructura([_hecho(contenido="   ")]))


def test_agentes_relacionados_vacio_es_legal():
    """Hay hechos sin persona concreta detrás; no es un hueco que llenar."""
    assert not validar_estructura([_hecho(agentes_relacionados=[])])


def test_detecta_id_malformado():
    assert "id-malformado" in _codigos(validar_estructura([_hecho(id="parentesco-1")]))


def test_acepta_id_con_sufijo_de_letra():
    """`creencia-010b` es la convención para intercalar sin renumerar."""
    h = _hecho(id="parentesco-010b")
    assert "id-malformado" not in _codigos(validar_estructura([h]))


def test_acepta_namespace_declarado():
    """`hueco-lex-001` vive en ecologia.yaml a propósito."""
    h = _hecho(id="hueco-lex-001", _archivo="ecologia.yaml", dominios=["ecologia"])
    assert not _codigos(validar_estructura([h]))


def test_detecta_namespace_no_declarado():
    h = _hecho(id="inventado-001", _archivo="ecologia.yaml")
    assert "id-dominio-cruzado" in _codigos(validar_estructura([h]))


def test_detecta_id_en_archivo_equivocado():
    h = _hecho(id="creencia-001", _archivo="parentesco.yaml")
    assert "id-dominio-cruzado" in _codigos(validar_estructura([h]))


def test_detecta_id_duplicado():
    a = _hecho(id="parentesco-007")
    b = _hecho(id="parentesco-007", _archivo="creencia.yaml")
    assert "id-duplicado" in _codigos(validar_estructura([a, b]))


@pytest.mark.parametrize("etiqueta", ETIQUETAS_FUENTE)
def test_acepta_las_cinco_etiquetas(etiqueta):
    assert not validar_etiquetas([_hecho(fuente=etiqueta)])


@pytest.mark.parametrize("ilegal", ["atestiguada", "ATESTIGUADO", "inventado",
                                    "retro_abstraido", "canon simulacion"])
def test_detecta_etiqueta_ilegal(ilegal):
    """Una variante de escritura no es la etiqueta: si `retro-abstraido` se
    cuela como `reconstruido`, el corpus miente sin que nadie lo note."""
    assert "etiqueta-ilegal" in _codigos(validar_etiquetas([_hecho(fuente=ilegal)]))


def test_detecta_agente_fantasma():
    problemas = validar_agentes([_hecho(agentes_relacionados=["Nadie-ko"])],
                                agentes={"Manaure"}, fondo=set())
    assert "agente-fantasma" in _codigos(problemas, "error")


def test_persona_de_fondo_es_aviso_no_error():
    """Las personas propuestas y sin veto de Miguel se citan a sabiendas."""
    problemas = validar_agentes([_hecho(agentes_relacionados=["Waimo-ko"])],
                                agentes={"Manaure"}, fondo={"Waimo-ko"})
    assert _codigos(problemas, "aviso") == {"agente-de-fondo"}
    assert not _codigos(problemas, "error")


def test_agente_real_no_produce_nada():
    assert not validar_agentes([_hecho(agentes_relacionados=["Manaure"])],
                               agentes={"Manaure"}, fondo=set())


def test_detecta_agentes_relacionados_como_cadena():
    problemas = validar_agentes([_hecho(agentes_relacionados="Manaure")],
                                agentes={"Manaure"}, fondo=set())
    assert "agentes-no-lista" in _codigos(problemas)


def test_detecta_referencia_cruzada_rota():
    h = _hecho(implicacion_simulacion="Ver parentesco-999 para el detalle.")
    assert "referencia-rota" in _codigos(validar_referencias_cruzadas([h]))


def test_referencia_cruzada_valida_no_produce_nada():
    a = _hecho(id="parentesco-001")
    b = _hecho(id="parentesco-002", contenido="Como dice parentesco-001, …")
    assert not validar_referencias_cruzadas([a, b])


def test_no_confunde_rangos_de_pagina_con_referencias():
    """`pp. 255-256` no es un id, y tratarlo como tal haría el chequeo inútil."""
    h = _hecho(referencia="Oliver 1989, cap. 3, pp. 255-256; Martí 1969")
    assert not validar_referencias_cruzadas([h])


def test_no_exige_resolver_dominios_ajenos_al_corpus():
    """`covid-019` o cualquier token de otro dominio no es asunto del corpus."""
    h = _hecho(contenido="Referencia externa tipo informe-001.")
    assert not validar_referencias_cruzadas([h])


def test_detecta_ruta_anterior_al_refactor():
    """`curiana_sim/cultura/` dejó de existir con el refactor del vault."""
    h = _hecho(referencia="cf. curiana_sim/cultura/creencia.yaml")
    assert "ruta-muerta" in _codigos(validar_rutas([h]))


def test_detecta_locacion_desconocida():
    problemas = validar_enganche_motor([_hecho(locacion="tabernaculo")],
                                       locaciones={"orilla"}, lexico={"bara"})
    assert "locacion-desconocida" in _codigos(problemas)


def test_detecta_palabra_fuera_del_lexicon():
    problemas = validar_enganche_motor([_hecho(palabra_lexicon="xyzzy")],
                                       locaciones={"orilla"}, lexico={"bara"})
    assert "palabra-desconocida" in _codigos(problemas)


def test_hueco_lexico_con_palabra_es_aviso():
    """Un hueco es, por definición, un fenómeno sin palabra caquetía."""
    problemas = validar_enganche_motor(
        [_hecho(hueco_lexico=True, palabra_lexicon="bara")],
        locaciones={"orilla"}, lexico={"bara"})
    assert _codigos(problemas, "aviso") == {"hueco-con-palabra"}


def test_enganche_valido_no_produce_nada():
    problemas = validar_enganche_motor([_hecho(locacion="orilla", palabra_lexicon="bara")],
                                       locaciones={"orilla"}, lexico={"bara"})
    assert not problemas


# ── genealogía ────────────────────────────────────────────────────────

def _genealogia(**kw):
    base = {
        "linajes": {"Kaira": {}},
        "agentes": {"Manaure": {"linaje": "Kaira", "conyuge": "Nubiri-sha"}},
        "personas_de_fondo": {"Nubiri-sha": {"linaje": "Kaira"}},
    }
    base.update(kw)
    return base


def test_genealogia_valida_no_produce_errores():
    problemas = validar_genealogia(_genealogia(), agentes={"Manaure"})
    assert not _codigos(problemas, "error")


def test_detecta_linaje_no_declarado():
    g = _genealogia(agentes={"Manaure": {"linaje": "Inexistente"}})
    assert "linaje-desconocido" in _codigos(validar_genealogia(g, agentes={"Manaure"}))


def test_linaje_en_prosa_no_es_error():
    """La mitad de los registros explican en prosa que el dato NO está, y esa
    honestidad es deliberada — no una laguna que el validador deba perseguir."""
    g = _genealogia(agentes={"Manaure": {"linaje": "no asignado"}})
    assert "linaje-desconocido" not in _codigos(validar_genealogia(g, agentes={"Manaure"}))


def test_detecta_pariente_que_no_resuelve():
    g = _genealogia(agentes={"Manaure": {"linaje": "Kaira", "conyuge": "Fantasma"}})
    assert "pariente-desconocido" in _codigos(validar_genealogia(g, agentes={"Manaure"}), "aviso")


def test_detecta_ruta_muerta_en_genealogia():
    g = _genealogia(agentes={"Manaure": {"titulo": "ver curiana_sim/cultura/parentesco.yaml"}})
    assert "ruta-muerta" in _codigos(validar_genealogia(g, agentes={"Manaure"}))


def test_agente_sin_ficha_es_aviso():
    problemas = validar_genealogia(_genealogia(), agentes={"Manaure", "Shaboro"})
    assert "agente-sin-ficha" in _codigos(problemas, "aviso")


# ── carga defensiva ───────────────────────────────────────────────────

def test_corpus_inexistente_no_revienta(tmp_path):
    hechos, genealogia, problemas = cargar(str(tmp_path / "no-existe"))
    assert hechos == [] and genealogia is None
    assert "corpus-ausente" in _codigos(problemas)


def test_yaml_invalido_se_reporta_sin_reventar(tmp_path):
    (tmp_path / "roto.yaml").write_text("- id: x\n  mal: [sin cerrar\n", encoding="utf-8")
    _, _, problemas = cargar(str(tmp_path))
    assert "yaml-invalido" in _codigos(problemas)


def test_raiz_inesperada_se_reporta(tmp_path):
    (tmp_path / "raro.yaml").write_text("solo una cadena\n", encoding="utf-8")
    _, _, problemas = cargar(str(tmp_path))
    assert "raiz-inesperada" in _codigos(problemas)
