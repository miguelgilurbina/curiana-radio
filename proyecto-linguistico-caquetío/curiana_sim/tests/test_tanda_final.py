"""La tanda final (2026-09-23): D11 fase 3 y las voces reconstruidas desde el wayuu.

Cada bloque es una decisión de `6-fusion/decisiones_tanda_final_2026-09-23.yaml`
(tf.1-tf.5), con su cita. Las etiquetas del lexicón (fuentes, Zayas, sigla E)
tienen sus tests en `test_tanda_final_lexicon.py`; el canon del mundo, en
`test_etnias.py`, `test_asentamientos.py` y `test_lengua.py`. La medición del
corte entero está en `6-fusion/medicion_tanda_final_2026-09-23.yaml`.
"""

import re

import pytest

import curiana_koine as K
import curiana_lexicon as L
from curiana_lexicon import (
    FUERA_DEL_HABLA,
    IDENTIDAD_LINGUISTICA,
    VOCABULARIO_BASE,
    prompt_reglas_breve,
    prompt_reglas_completo,
    score_linguistico,
)


def _todas_las_plantillas() -> str:
    return (IDENTIDAD_LINGUISTICA + prompt_reglas_breve() + prompt_reglas_completo()
            + "".join(L.prompt_refuerzo(s, []) for s in (1.0, 3.0, 5.0, 6.5))
            + L.prompt_rescate_linguistico("x", 1.0, 3, []))


def _ensena(forma: str, texto: str) -> bool:
    return bool(re.search(r"(?<![\w-])" + re.escape(forma) + r"(?![\w])", texto))


# ══════════════════════════════════════════════════════════════════════
# tf.1 — los pronombres de las hermanas
# ══════════════════════════════════════════════════════════════════════
PRONOMBRES = {"dai": "caquetío-reconstruido", "bui": "caquetío-hipotético",
              "lihi": "caquetío-hipotético", "tuhu": "caquetío-hipotético",
              "waya": "caquetío-reconstruido", "naya": "caquetío-reconstruido"}


@pytest.mark.parametrize("forma,capa", sorted(PRONOMBRES.items()))
def test_tf1_el_pronombre_esta_con_su_capa_y_su_cita(forma, capa):
    e = VOCABULARIO_BASE[forma]
    assert e["cat"] == "pron" and e["fuente"] == capa
    assert "tf.1" in e["notas"] and "wayuu" in e["notas"]
    assert "Perea" in e["notas"] or "Neira" in e["notas"]


@pytest.mark.parametrize("forma", ["taya", "pia", "nüma"])
def test_tf1_el_pronombre_del_wayuu_al_archivo_con_su_capa(forma):
    assert forma not in VOCABULARIO_BASE
    e = FUERA_DEL_HABLA[forma]
    assert e["fuente"] == "caquetío-reconstruido", "archivar no es degradar"
    assert "ARCHIVADA DEL HABLA 2026-09-23" in e["notas"]


def test_tf1_las_claves_lokono_que_chocaban_llevan_su_etiqueta():
    assert VOCABULARIO_BASE["tuhu-lokono"]["fuente"] == "lokono"
    assert VOCABULARIO_BASE["kuba-lokono"]["fuente"] == "lokono"
    assert VOCABULARIO_BASE["tuhu"]["fuente"] == "caquetío-hipotético"


def test_tf1_el_formal_no_se_toca():
    for forma in ("kudanga", "kuté"):
        assert VOCABULARIO_BASE[forma]["fuente"] == "caquetío-atestiguado"
    assert "bui (tú)" in prompt_reglas_completo()


# ══════════════════════════════════════════════════════════════════════
# tf.2 — el aspecto: presente sin marca, -kuba, -ba
# ══════════════════════════════════════════════════════════════════════

def test_tf2_las_reglas_son_kuba_y_ba_y_los_viejos_solo_se_pelan():
    assert set(L.REGLAS_ASPECTO) == {"-kuba", "-ba"}
    assert set(L.REGLAS_EN_DESUSO) == {"-ka", "-ni", "-da", "ta-"}
    for afijo in ("-kuba", "-ba", "-ka", "-ni", "-da"):
        assert afijo in L._SUFIJOS_CAQ, afijo
    assert "-ka" not in L.REGLAS_RETIRADAS, "no es lo mismo que -ko/-sha"


def test_tf2_el_detector_se_sustituye_no_se_une():
    tok = ["naa-kuba", "diki-ba", "naa-ka", "naa-ni", "naa-da", "naa"]
    assert L._aspectos_morfologicos(tok) == ["completivo", "prospectivo"]
    assert L._aspectos_morfologicos(["naa"]) == [], "el presente no se marca"


def test_tf2_el_desafijador_sigue_pelando_lo_viejo():
    assert L.nucleo_de_token("ta-kasi-ni") == ["kasi"]
    assert L.nucleo_de_token("da-kasi-kuba") == ["kasi"]


def test_tf2_el_emocionar_dice_el_paradigma_nuevo():
    assert K._ASPECTO_SUFIJO == {"completivo": "-kuba", "continuativo": "",
                                 "prospectivo": "-ba"}
    for agente, emo in K.EMOCIONAR_SEED.items():
        linea = K.prompt_emocionar(agente)
        assert not re.search(r"-(ka|ni|da)\.", linea), linea
        if emo.get("aspecto") == "continuativo":
            assert "el verbo solo" in linea


def test_tf2_las_semillas_escritas_no_llevan_el_aspecto_viejo():
    for agente, formas in K.FORMAS_SEED.items():
        for f in formas:
            assert not re.search(r"-(ka|ni|da)$", f), (agente, f)


# ══════════════════════════════════════════════════════════════════════
# tf.3 — el posesivo da-
# ══════════════════════════════════════════════════════════════════════

def test_tf3_el_posesivo_es_da_y_el_scorer_lo_reconoce():
    assert "da-" in L.REGLAS_POSESIVAS and "ta-" not in L.REGLAS_POSESIVAS
    r = score_linguistico("Dai diki-kuba da-barsure.", L.LexicoComunitario())
    assert "da-barsure" in r["palabras_caquetias"]


# ══════════════════════════════════════════════════════════════════════
# tf.5 — las voces reconstruidas desde el wayuu
# ══════════════════════════════════════════════════════════════════════
SUSTITUTAS = {"kashi": "danu", "yama": "popoi", "sulu": "ruku", "wana": "diki",
              "naba": "kuburuku", "tüshi": "kasalini", "kapua": "mautia",
              "wanü": "wasima"}
SIN_SUSTITUTA = ("anüiki", "pütchi")


@pytest.mark.parametrize("vieja,nueva", sorted(SUSTITUTAS.items()))
def test_tf5_la_vieja_al_archivo_y_la_nueva_en_el_habla(vieja, nueva):
    assert vieja not in VOCABULARIO_BASE and vieja in FUERA_DEL_HABLA
    assert "tf.5" in FUERA_DEL_HABLA[vieja]["notas"]
    assert nueva in VOCABULARIO_BASE


@pytest.mark.parametrize("vieja", SIN_SUSTITUTA)
def test_tf5_las_que_se_archivan_sin_sustituta(vieja):
    assert vieja not in VOCABULARIO_BASE and vieja in FUERA_DEL_HABLA


def test_tf5_las_nuevas_son_hipoteticas_con_cita_y_las_que_mandan_atestiguadas():
    for forma in ("danu", "ruku", "diki", "kuburuku", "kasalini", "mautia"):
        e = VOCABULARIO_BASE[forma]
        assert e["fuente"] == "caquetío-hipotético", forma
        assert "Perea" in e["notas"] or "Neira" in e["notas"], forma
    for forma in ("popoi", "wasima"):
        assert VOCABULARIO_BASE[forma]["fuente"] == "caquetío-atestiguado"
    assert VOCABULARIO_BASE["bana"]["fuente"] == "caquetío-hipotético"
    assert "Goeje 1939 p. 34" in VOCABULARIO_BASE["bana"]["notas"]


def test_tf5_las_raices_verbales_nuevas_toman_aspecto():
    assert {"diki", "kuburuku", "kasalini"} <= L.raices_verbales_caquetias()
    assert L._aspectos_morfologicos(["kuburuku-ba"]) == ["prospectivo"]


# ══════════════════════════════════════════════════════════════════════
# las plantillas: lo que leen los 63
# ══════════════════════════════════════════════════════════════════════
RETIRADAS_DE_LA_PLANTILLA = ("taya", "pia", "nüma", "kashi", "yama", "sulu",
                             "wana", "naba", "tüshi", "kapua", "anüiki",
                             "pütchi", "wanü")


def test_ninguna_plantilla_ensena_lo_retirado():
    todo = _todas_las_plantillas()
    for forma in RETIRADAS_DE_LA_PLANTILLA:
        assert not _ensena(forma, todo), forma
    for suf in ("-ka", "-ni", "-da"):
        assert not re.search(r"\w" + re.escape(suf) + r"(?![\w])", todo), suf
    assert not _ensena("ta-", todo.replace("ta-barsure", ""))


def test_la_identidad_ensena_el_nucleo_nuevo():
    assert "Dai diki-kuba arima wara para." in IDENTIDAD_LINGUISTICA
    assert "Da-barsure kuburuku." in IDENTIDAD_LINGUISTICA
    assert "kari" not in IDENTIDAD_LINGUISTICA, "sigla E: kari es hipotética"


def test_la_breve_lleva_lo_que_la_muestra_del_perfil_era2_no_da():
    """El perfil era2 no muestra la capa hipotética en el muestreador: los
    pronombres y voces nuevas sólo llegan a los tiers 2 y 3 por aquí."""
    breve = prompt_reglas_breve()
    for forma in ("dai", "bui", "lihi", "tuhu", "danu", "ruku", "kasalini", "mautia"):
        assert _ensena(forma, breve), forma
    assert "waranao" not in breve


def test_el_refuerzo_ensena_por_recorte_sin_las_viejas():
    """La plantilla enseña por RECORTE (`[:4]`): se cambian las LISTAS."""
    usadas = ["diki", "suna", "masa", "awa", "ka", "mara", "saa", "naka"]
    texto = L.prompt_refuerzo(3.0, usadas)
    for forma in ("wana", "naba", "kashi", "yama"):
        assert not _ensena(forma, texto), forma
    assert "kuburuku" in texto and "danu" in texto
