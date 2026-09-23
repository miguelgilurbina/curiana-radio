"""La tanda de la base (2026-09-23): lo que cambia el prompt, en un solo corte.

Cada bloque es una decisión de `6-fusion/decisiones_base_2026-09-22.yaml`
(db.1-db.6) o de `6-fusion/decisiones_campanas_2026-09-21.yaml` (dc.2, dc.3),
con su cita. La medición del corte entero está en
`6-fusion/medicion_tanda_base_2026-09-23.yaml`.
"""

import json

import pytest

import curiana_koine as K
import curiana_lexicon as L
from curiana_koine import CompetenciaLexica
from curiana_lexicon import (
    FUERA_DEL_HABLA,
    VOCABULARIO_BASE,
    LexicoComunitario,
    Neologismo,
    es_raiz_de_ninguna_parte,
    prompt_reglas_breve,
    prompt_reglas_completo,
)


@pytest.fixture(autouse=True)
def _sin_raices_admitidas():
    """Las raíces onomatopéyicas son estado del run: cada test empieza sin."""
    L.olvidar_raices_onomatopeyicas()
    yield
    L.olvidar_raices_onomatopeyicas()


def _sig(clave):
    """La glosa: VOCABULARIO_BASE la guarda en `sig` (las entradas escritas con
    `es` se normalizan al fundir las tablas)."""
    e = VOCABULARIO_BASE[clave]
    return e.get("sig") or e.get("es")


def _neo(forma, autor="Manaure", dia=1, turno=1):
    return Neologismo(turno=turno, dia=dia, autor=autor, forma=forma,
                      componentes="x + y", significado="algo",
                      contexto="", regla_aplicada="")


# ══════════════════════════════════════════════════════════════════════
# db.3 (2) — las `taíno-reconstruido`, que eran lokono, al archivo
# ══════════════════════════════════════════════════════════════════════
ARCHIVADAS_DB3 = ["abba", "acoa", "aduri", "agari", "akcicyaa",
                  "thigisi", "wacusi", "wagulo"]


@pytest.mark.parametrize("forma", ARCHIVADAS_DB3)
def test_db3_la_reconstruida_sale_del_habla_con_su_capa(forma):
    assert forma not in VOCABULARIO_BASE
    e = FUERA_DEL_HABLA[forma]
    assert e["fuente"] == "taíno-reconstruido", "archivar no es degradar"
    assert "ARCHIVADA DEL HABLA 2026-09-23" in e["notas"]
    assert "reconstruir_taino()" in e["notas"], "la procedencia se conserva"
    assert e["archivada"].startswith("2026-09-23")


def test_db3_no_queda_ninguna_taino_reconstruido_en_el_habla():
    assert not [k for k, v in VOCABULARIO_BASE.items()
                if v.get("fuente") == "taíno-reconstruido"]


def test_db3_daca_es_yo_con_las_casas_y_guarda_la_reconstruccion_en_notas():
    e = VOCABULARIO_BASE["daca"]
    assert e["fuente"] == "taíno"
    assert _sig("daca") == "yo"
    assert "daca quiere decir yo" in e["notas"]
    assert "CLXVII p. 447" in e["notas"]
    assert "'mano'" in e["notas"], "la reconstrucción no se borra: se dice"
    assert "daca" not in FUERA_DEL_HABLA


# ══════════════════════════════════════════════════════════════════════
# db.3 (3) — las glosas, cada una según su cronista
# ══════════════════════════════════════════════════════════════════════

def test_db3_mayani_es_un_juicio_de_valor_no_la_negacion():
    e = VOCABULARIO_BASE["mayani"]
    assert _sig("mayani").startswith("de ningún valor")
    assert "p. 13" in e["notas"] and "Martyr" in e["notas"]


def test_db3_caney_es_la_casa_redonda_no_la_del_cacique():
    sig = _sig("caney")
    assert "redonda" in sig
    assert "rectangular" not in sig and "del cacique" not in sig


def test_db3_batey_es_el_juego():
    assert _sig("batey").startswith("juego de pelota")


def test_db3_tabako_es_el_canuto_no_la_hierba():
    sig = _sig("tabako")
    # db.3 la dejó en «cañuto con que se toma el humo…». El 2026-09-23 (cc.7 /
    # tf.6) la glosa se AMPLIÓ con lo que Zayas dejaba abierto: Las Casas
    # (Apologética p. 181) llama tabacos a los ROLLOS de hoja encendidos, y
    # Oviedo t. IV p. 96 igual. El cañuto sigue; entra primero el rollo.
    assert sig.startswith("el rollo de hojas")
    assert "cañuto" in sig and "no la hierba" in sig
    assert "Nicotiana" not in sig


def test_db3_siba_taina_y_siba_lokono_son_dos_claves():
    assert VOCABULARIO_BASE["siba"]["fuente"] == "taíno"
    assert "Pané" in VOCABULARIO_BASE["siba"]["notas"]
    assert VOCABULARIO_BASE["siba-lokono"]["fuente"] == "lokono"


def test_db3_voces_de_fuera_pierde_las_dos_que_salian():
    formas = {f for _p, f, _g, _fam in L.voces_de_fuera_posibles()}
    assert not {"akcicyaa", "wagulo"} & formas
    glosas = {f: g for _p, f, g, _fam in L.voces_de_fuera_posibles()}
    assert glosas["batey"].startswith("juego de pelota")
    # «cañuto» hasta el 2026-09-23: cc.7 / tf.6 amplió la glosa y el bloque
    # enseña ahora su primera parte, el rollo de hojas (Las Casas p. 181).
    assert glosas["tabako"].startswith("el rollo de hojas")


# ══════════════════════════════════════════════════════════════════════
# db.3 (1) — la semilla de la persona es la de la cadena
# ══════════════════════════════════════════════════════════════════════

def test_db3_guardar_koine_escribe_la_semilla_y_cargar_la_devuelve(tmp_path):
    ruta = str(tmp_path / "koine.json")
    K.fijar_semilla(21)
    K.guardar_koine({}, K.CampoLexico(), CompetenciaLexica(), path=ruta)
    assert K.semilla_de_precarga_guardada(ruta) == 21
    K.fijar_semilla(None)


def test_db3_un_json_viejo_no_trae_semilla(tmp_path):
    ruta = tmp_path / "viejo.json"
    ruta.write_text(json.dumps({"idiolectos": {}, "campo": {}}), encoding="utf-8")
    assert K.semilla_de_precarga_guardada(str(ruta)) is None
    assert K.semilla_de_precarga_guardada(str(tmp_path / "no-hay.json")) is None


def test_db3_con_la_semilla_de_la_cadena_el_emocionar_no_cambia_de_dia():
    """Uria leía «Tu aspecto natural es -ni» el día 1 y «-ka» los días 2 y 3.
    Con la semilla de la cadena, el día 2 dice lo mismo que el día 1."""
    from curiana_agents import ALL_AGENTS
    K.fijar_semilla(21)
    dia1 = {n: K.prompt_emocionar(n, a.get("etnia")) for n, a in ALL_AGENTS.items()}
    K.fijar_semilla(22)                      # la del día 2
    K.fijar_semilla(21)                      # …y --continuar la re-fija con la de la cadena
    dia2 = {n: K.prompt_emocionar(n, a.get("etnia")) for n, a in ALL_AGENTS.items()}
    assert dia1 == dia2
    K.fijar_semilla(None)


# ══════════════════════════════════════════════════════════════════════
# dc.2 C + E — `-gua` 'región' pasa a `-wa`, sin glosa
# ══════════════════════════════════════════════════════════════════════

def test_dc2_la_clave_es_wa_y_no_tiene_glosa():
    assert "-wa" in L.TODAS_LAS_REGLAS and "-gua" not in L.TODAS_LAS_REGLAS
    r = L.REGLAS_LOCATIVAS["-wa"]
    assert "no precisado" in r["nombre"]
    assert r["forma_fuente"] == "-gua"
    assert "oliver" in r["evidencia"].lower() and "148" in r["evidencia"]
    assert "deuda" not in r, "ya cita a Oliver: deja de ser sin-procedencia"


def test_dc2_las_plantillas_no_ensenan_region():
    for p in (prompt_reglas_breve(), prompt_reglas_completo()):
        assert "-gua" not in p
        assert "región de" not in p
        assert "-wa y -ana" in p


def test_dc2_el_desafijador_quita_wa_y_ya_no_gua():
    assert L.nucleo_de_token("maure-wa") == ["maure"]
    assert L.nucleo_de_token("maure-gua") == ["maure", "gua"]
    # el prefijo `wa-` 'nuestro' sigue siendo prefijo
    assert L.nucleo_de_token("wa-buko") == ["buko"]


# ══════════════════════════════════════════════════════════════════════
# dc.3 B — la derivación cero se enseña; y el `buko-ana` que faltaba
# ══════════════════════════════════════════════════════════════════════

def test_dc3_las_dos_plantillas_ensenan_la_derivacion_cero_con_jusual():
    assert "jusual" in VOCABULARIO_BASE
    assert "jusual es sembrar" in prompt_reglas_breve()
    assert "jusual es sembrar" in prompt_reglas_completo()


def test_d21_6_el_ejemplo_ya_no_glosa_ana_como_lugar():
    p = prompt_reglas_completo()
    assert "buko-ana" not in p and "lugar de la represa" not in p


# ══════════════════════════════════════════════════════════════════════
# db.1 C — la casi-raíz, y el agujero de `kira`
# ══════════════════════════════════════════════════════════════════════

def test_db1_c_perdona_la_casi_raiz_larga():
    assert L.LARGO_MINIMO_CASI_RAIZ == 6
    assert L.casi_raiz_de("pütshi") == "pütchi"
    assert not es_raiz_de_ninguna_parte("pütshi-bana")
    assert LexicoComunitario().registrar_neologismo(_neo("pütshi-bana")) is True


@pytest.mark.parametrize("forma", ["lumina-bana-iro", "duma-bana", "uyama-ni", "karu-bana"])
def test_db1_c_no_perdona_lo_que_es_otra_palabra(forma):
    """Medido sobre la base: con largo 4 se perdonaban `duma`→`duna` y
    `karu`→`kuru`, con 5 `uyama`→`yama`. Con 6, ninguna."""
    assert es_raiz_de_ninguna_parte(forma)
    assert LexicoComunitario().registrar_neologismo(_neo(forma)) is False


def test_db1_la_forma_perdonada_se_guarda_como_la_escribio():
    lex = LexicoComunitario()
    lex.registrar_neologismo(_neo("pütshi-bana"))
    assert [n.forma for n in lex._neologismos] == ["pütshi-bana"]


def test_db1_el_agujero_de_kira_se_cierra_en_la_puerta_y_no_en_el_clasificador():
    """`kira` 'escuchar' está ARCHIVADA; `kira` 'brillo' se inventó el
    2026-09-21 y pasaba por ella. En la puerta no avala; en el clasificador
    sí, porque decir de qué lengua es una palabra no es dejarla competir."""
    assert "kira" in FUERA_DEL_HABLA
    assert es_raiz_de_ninguna_parte("kira-bana", archivadas_avalan=False)
    assert not es_raiz_de_ninguna_parte("kira-bana")
    lex = LexicoComunitario()
    assert lex.registrar_neologismo(_neo("kira-bana")) is False
    assert [r[0] for r in lex.rechazos_de_raiz] == ["kira-bana"]
    comp = CompetenciaLexica()
    comp.activar("cometa", "una estrella con cola")
    comp.proponer("cometa", "kira-bana", "Manaure")
    assert not comp.referentes["cometa"]["variantes"]
    assert "kira-bana" in L.PUERTA_DEL_RECUENTO


def test_db1_una_raiz_archivada_con_una_viva_al_lado_sigue_pasando():
    """No es una poda: `kasi-kira` tiene `kasi`, que se habla."""
    assert not es_raiz_de_ninguna_parte("kasi-kira", archivadas_avalan=False)


# ══════════════════════════════════════════════════════════════════════
# db.4 — el catálogo de la era 2, los dos moldes y la cadencia
# ══════════════════════════════════════════════════════════════════════

def test_db4_el_catalogo_de_la_era_2_es_una_tabla_con_quince():
    refs = K.REFERENTES_ERA2
    assert len(refs) == 15
    assert refs[0]["id"] == "tarantula_azul", "la tarántula azul abre (Miguel)"
    assert sum(r["animal"] for r in refs) == 12
    assert {r["tipo"] for r in refs} == {"hueco", "novedad"}
    assert not {"cuentas_vidrio", "fiebre_manchas"} & {r["id"] for r in refs}


def test_db4_ninguna_descripcion_trae_un_animal_o_una_cosa_de_despues_de_1500():
    europeo = ("gallina", "caballo", "vaca", "cabra", "chivo", "oveja", "cerdo",
               "puerco", "hierro", "vidrio", "trigo", "burro")
    for r in K.REFERENTES_ERA2:
        texto = f"{r['desc']} {r.get('se_oye') or ''}".lower()
        assert not [p for p in europeo if p in texto], r["id"]


def test_db4_el_catalogo_depende_del_mundo():
    assert K.referentes_del_mundo("PARAGUANÁ") is K.REFERENTES_ERA2
    assert K.referentes_del_mundo("CURIANA") is K.REFERENTES_NOVEDOSOS


def test_db4_la_era_1_dice_el_estimulo_de_siempre_caracter_a_caracter():
    ref = K.REFERENTES_NOVEDOSOS[1]
    viejo = (f"[ALGO NUEVO EN LA CURIANA]: {ref['desc']}. "
             f"Esto no tiene nombre en caquetío todavía. Nómbralo TÚ con morfemas "
             f"caquetíos y dilo: [forma: componentes = significado]. Reacciona a la "
             f"cosa nueva y nómbrala.")
    assert K.estimulo_de_referente(ref, "LA CURIANA") == viejo


def test_db4_el_hueco_no_se_presenta_como_algo_nuevo():
    guacharaca = next(r for r in K.REFERENTES_ERA2 if r["id"] == "guacharaca")
    e = K.estimulo_de_referente(guacharaca, "PARAGUANÁ")
    assert e.startswith("[LO QUE VES SIEMPRE, EN PARAGUANÁ]")
    assert "ALGO NUEVO" not in e
    assert "[Lo que se oye]: un grito fuerte" in e
    assert "por cómo suena" in e


def test_db4_sin_sonido_no_hay_linea_ni_invitacion():
    cometa = next(r for r in K.REFERENTES_ERA2 if r["id"] == "cometa")
    e = K.estimulo_de_referente(cometa, "PARAGUANÁ")
    assert "[Lo que se oye]" not in e and "por cómo suena" not in e
    tarantula = K.REFERENTES_ERA2[0]
    e = K.estimulo_de_referente(tarantula, "PARAGUANÁ")
    assert "[Lo que se oye]: nada" in e
    assert "por cómo suena" not in e, "«nada» no invita a nombrar por la voz"


def test_db4_los_quince_sobreviven_al_traductor_de_la_era_2():
    from curiana_eventos import decir_para_el_mundo
    for r in K.REFERENTES_ERA2:
        e = K.estimulo_de_referente(r, "PARAGUANÁ")
        assert decir_para_el_mundo(e, "PARAGUANÁ") == e, r["id"]


def test_db4_la_cadencia_de_la_era_2_es_uno_cada_dos_dias():
    toca = [(d, tu) for d in range(1, 7) for tu in range(1, 7)
            if K.toca_nombrar("PARAGUANÁ", d, tu, t=tu - 1)]
    assert toca == [(1, 5), (3, 5), (5, 5)]


def test_db4_la_cadencia_de_la_era_1_no_cambia():
    assert [t for t in range(12) if K.toca_nombrar("CURIANA", 1, 1, t)] == [4, 8]


# ══════════════════════════════════════════════════════════════════════
# db.6 — la puerta onomatopéyica
# ══════════════════════════════════════════════════════════════════════

def test_db6_cerrada_por_defecto():
    lex = LexicoComunitario()
    assert lex.puerta_onomatopeyica is None
    assert lex.registrar_neologismo(_neo("tororo")) is False


def test_db6_abierta_admite_una_raiz_con_forma_caquetia_y_la_marca():
    lex = LexicoComunitario()
    lex.puerta_onomatopeyica = "guacharaca"
    assert lex.registrar_neologismo(_neo("tororo")) is True
    neo = lex._neologismos[0]
    assert neo.raiz_onomatopeyica == "tororo"
    assert L.RAICES_ONOMATOPEYICAS["tororo"]["referente"] == "guacharaca"
    # y desde ahí es raíz conocida: una forma que la use después cuenta
    assert not es_raiz_de_ninguna_parte("tororo-bana", archivadas_avalan=False)
    assert "♪" in lex.reporte_de_rechazos()


@pytest.mark.parametrize("forma,referente", [
    ("wacharaka", "guacharaca"),    # el nombre castellano respelado
    ("korokoro", "corocoro"),
    ("guacharaca", "guacharaca"),   # con marca castellana
    ("kira-kira", "cardenal"),      # raíz archivada: no vuelve por aquí
    ("suave", "delfin"),            # palabra castellana
    ("krak", "delfin"),             # fuera de la fonotáctica
    ("bururu-lumina", "delfin"),    # dos raíces nuevas
])
def test_db6_lo_que_no_pasa_el_filtro(forma, referente):
    assert L.raiz_onomatopeyica_candidata(forma, referente) is None


def test_db6_la_reduplicacion_es_una_raiz():
    assert L.raiz_onomatopeyica_candidata("tiwi-tiwi", "cardenal") == "tiwi"


def test_db6_la_competencia_sólo_abre_la_puerta_a_un_animal():
    comp = CompetenciaLexica()
    comp.activar("cometa", "una estrella con cola")
    comp.activar("guacharaca", "un ave parda", animal=True)
    comp.proponer("cometa", "tororo", "Manaure")
    comp.proponer("guacharaca", "tororo", "Manaure")
    assert not comp.referentes["cometa"]["variantes"]
    assert "tororo" in comp.referentes["guacharaca"]["variantes"]


def test_db6_la_raiz_admitida_sobrevive_a_continuar(tmp_path):
    ruta = str(tmp_path / "lexico.json")
    lex = LexicoComunitario()
    lex.puerta_onomatopeyica = "guacharaca"
    lex.registrar_neologismo(_neo("tororo"))
    lex.save(ruta)
    L.olvidar_raices_onomatopeyicas()
    assert es_raiz_de_ninguna_parte("tororo")
    vuelta = LexicoComunitario.load(ruta)
    assert "tororo" in L.RAICES_ONOMATOPEYICAS
    assert vuelta._neologismos[0].raiz_onomatopeyica == "tororo"


def test_db6_la_competencia_guarda_que_el_referente_es_animal(tmp_path):
    ruta = str(tmp_path / "koine.json")
    comp = CompetenciaLexica()
    comp.activar("guacharaca", "un ave parda", animal=True)
    K.guardar_koine({}, K.CampoLexico(), comp, path=ruta)
    _i, _c, vuelta = K.cargar_koine(ruta)
    assert vuelta.referentes["guacharaca"]["animal"] is True
