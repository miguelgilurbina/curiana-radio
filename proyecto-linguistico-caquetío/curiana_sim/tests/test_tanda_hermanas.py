# -*- coding: utf-8 -*-
"""Tests de la TANDA DE LAS HERMANAS (2026-09-24).

«Acepto todo lo recomendado» (Miguel): el núcleo fundacional rehecho desde el
lokono y el habla de mujeres kalinago, las ocho voces que seguían saliendo del
wayuu, alaain/japü, y las notas de la esfera taína. Decisiones en
6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml.

Lo que fijan: que cada voz vieja está ARCHIVADA con su capa intacta (archivar
no es degradar), que la nueva lleva la etiqueta que N1 le da (dos hermanas =
reconstruida, una = hipotética) y su cita, que ninguna plantilla enseña lo
archivado, y que lo hipotético llega a los 63 por la plantilla breve, porque
el perfil era2 no lo muestrea.
"""
import re

import pytest

import curiana_lexicon as L
from curiana_lexicon import (FUERA_DEL_HABLA, IDENTIDAD_LINGUISTICA,
                             VOCABULARIO_BASE, prompt_reglas_breve,
                             prompt_reglas_completo)

# vieja -> nueva (None = manda una atestiguada que ya estaba)
NUCLEO = {
    "kono": None, "sima": None, "nomi": None, "wari": None, "arua": None, "buri": None,
    "chaa": "ani", "masa": "aeke", "awa": "ati", "suna": "dunku", "panaa": "aita",
    "kabo": "isi", "nii": "akusi", "wara": "kibe", "kuru": "ada", "duna": "uni",
    "kaya": "unia", "taa": "butu",
    "naa": "kunu", "waa": "sile", "raka": "hiti", "rua": "kudu", "amana": "hikihi",
    "arima": "hime", "dali": "wunabu", "baba": "iti", "ka": "badia", "mara": "ika",
    "saa": "bena", "naka": "kia",
}
MANDA_LA_ATESTIGUADA = {"kono": "jusual", "sima": "kidi", "nomi": "ateri",
                        "wari": "iero", "arua": "ako", "buri": "dare"}
D2 = {"anasa": "saika", "mütsia": "uli", "kasuta": "halira", "sünatü": "kule",
      "outa": "huda", "kataa": "kake", "talata": "halikebe", "jashichi": "aiima"}
RECONSTRUIDAS = {"ani", "aeke", "ati", "dunku", "aita", "isi", "akusi", "kibe",
                 "ada", "uni", "unia", "butu", "huda", "kake", "aburi",
                 "diki", "marisi", "bui", "lihi", "tuhu"}
HIPOTETICAS = {"kunu", "sile", "hiti", "kudu", "hikihi", "hime", "wunabu", "iti",
               "badia", "ika", "bena", "kia", "saika", "uli", "halira", "kule",
               "halikebe", "aiima", "kaa", "maa", "suka", "ama", "bari", "puna"}
ARCHIVADAS = set(NUCLEO) | set(D2) | {"alaain", "japü"}


def _plantillas() -> str:
    return "\n".join([
        IDENTIDAD_LINGUISTICA, prompt_reglas_breve(), prompt_reglas_completo(),
        *(L.prompt_refuerzo(s, []) for s in (1.0, 3.0, 5.0, 6.5)),
        L.prompt_rescate_linguistico("x", 1.0),
    ])


def _ensena(forma: str, texto: str) -> bool:
    return bool(re.search(r"(?<![\w-])" + re.escape(forma) + r"(?![\w])", texto))


@pytest.mark.parametrize("vieja", sorted(ARCHIVADAS))
def test_la_vieja_esta_archivada_con_su_capa(vieja):
    assert vieja not in VOCABULARIO_BASE
    e = FUERA_DEL_HABLA[vieja]
    assert "tanda de las hermanas" in e["archivada"]
    assert "ARCHIVADA DEL HABLA 2026-09-24" in e["notas"]
    # archivar no es degradar: las del núcleo eran reconstruidas y lo siguen
    # siendo en el archivo; alaain y japü eran hipotéticas
    assert e["fuente"] in ("caquetío-reconstruido", "caquetío-hipotético")


@pytest.mark.parametrize("vieja,nueva", sorted({**NUCLEO, **D2}.items()))
def test_la_nueva_esta_en_el_habla_con_su_cita(vieja, nueva):
    if nueva is None:
        manda = MANDA_LA_ATESTIGUADA[vieja]
        assert VOCABULARIO_BASE[manda]["fuente"] == "caquetío-atestiguado", manda
        return
    e = VOCABULARIO_BASE[nueva]
    assert "Tanda de las hermanas" in e["notas"], nueva
    assert f"Sustituye a `{vieja}`" in e["notas"], nueva
    assert re.search(r"Goeje|Adam|Perea|Neira|Oliver", e["notas"]), nueva


@pytest.mark.parametrize("forma", sorted(RECONSTRUIDAS))
def test_dos_hermanas_es_reconstruida(forma):
    assert VOCABULARIO_BASE[forma]["fuente"] == "caquetío-reconstruido", forma


@pytest.mark.parametrize("forma", sorted(HIPOTETICAS))
def test_una_hermana_es_hipotetica(forma):
    assert VOCABULARIO_BASE[forma]["fuente"] == "caquetío-hipotético", forma


def test_las_claves_de_comparanda_que_chocaban():
    for k in ("huda-lokono", "kia-lokono", "wunabu-lokono"):
        assert VOCABULARIO_BASE[k]["fuente"] == "lokono", k
        assert "CLAVE CAMBIADA 2026-09-24" in VOCABULARIO_BASE[k]["notas"], k
    for k in ("uni-achagua", "unia-achagua"):
        assert VOCABULARIO_BASE[k]["fuente"] == "achagua", k
    from lexicon_a2 import COLISIONES_A2, LOKONO_A2
    formas = {c[3] for c in COLISIONES_A2 if c[0] == "lokono"}
    assert {"ada", "hime"} <= formas
    assert "ada" not in LOKONO_A2 and "hime" not in LOKONO_A2


def test_ninguna_plantilla_ensena_lo_archivado():
    todo = _plantillas()
    for forma in ARCHIVADAS - {"ka"}:      # `ka-` es el prefijo atributivo, y se enseña
        assert not _ensena(forma, todo), forma
    assert not re.search(r"(?<![\w-])ka(?![\w-])", todo), "`ka` suelto 'y'"


def test_la_breve_lleva_lo_hipotetico_a_los_63():
    """El perfil era2 no muestrea la capa hipotética: los conectores y las
    seis voces de D2 sólo llegan a los tiers 2 y 3 por la breve."""
    breve = prompt_reglas_breve()
    for forma in ("badia", "ika", "bena", "kia", "kibe",
                  "saika", "uli", "halira", "kule", "halikebe", "aiima"):
        assert _ensena(forma, breve), forma


def test_la_identidad_y_la_completa_ensenan_el_nucleo_nuevo():
    assert "Dai diki-kuba hime kibe para." in IDENTIDAD_LINGUISTICA
    completa = prompt_reglas_completo()
    for forma in ("kunu", "sile", "ani", "aeke", "ati", "dunku", "aita", "butu",
                  "jusual", "hiti", "kudu", "uni", "hikihi", "unia", "ada", "hime",
                  "wunabu", "kidi", "iti", "dare", "ateri", "iero", "ako", "isi",
                  "akusi", "huda", "kake"):
        assert _ensena(forma, completa), forma


def test_komoho_tiene_dos_fuentes_y_la_glosa_de_oviedo():
    e = VOCABULARIO_BASE["komoho"]
    assert e["sig"] == "fruto del cardón de las tunas (higo de tuna)"
    assert e["glosa_fuente"].startswith("Higo")          # la de Zavala, intacta
    assert "Oviedo" in e["notas"] and "313" in e["notas"]


def test_aburi_es_voz_y_el_toponimo_de_zavala_sigue():
    import lexicon_zavala as Z
    assert "HOMÓGRAFO DECLARADO" in VOCABULARIO_BASE["aburi"]["notas"]
    assert "aburi" in Z.TOPONIMOS_ZAVALA


def test_baja_cano_entra_hipotetica_y_marcada():
    """Archivar `baba` destapaba la entrada #23 de Zavala («Baja (baba)»
    'caño', sigla E), que el minador daba por «ya está» por un homógrafo
    falso. Miguel decidió que entre (2026-09-24, «Ok a todo»): hipotética por
    cc.4 (su única fuente es Esteves p. 19) y marcada como homógrafo del
    castellano 'baja', para que el score la trate neutra."""
    e = VOCABULARIO_BASE["baja"]
    assert e["fuente"] == "caquetío-hipotético" and e["cat"] == "sust"
    assert "Esteves p. 19" in e["notas"]
    assert "baja" in L.HOMOGRAFOS_ZAVALA
    r = L.score_linguistico("La marea baja por la tarde.", L.LexicoComunitario())
    assert "baja" not in r["palabras_caquetias"]


@pytest.mark.parametrize("forma", ["kiba", "waitiao", "jagey", "warawara",
                                   "kabana", "bajareke", "wako", "kiwa"])
def test_t4_la_pareja_taina_esta_anotada_sin_tocar_capa(forma):
    e = VOCABULARIO_BASE[forma]
    assert "T4 de la tanda de las hermanas" in e["notas"], forma
    assert e["fuente"].startswith("caquetío-"), forma
