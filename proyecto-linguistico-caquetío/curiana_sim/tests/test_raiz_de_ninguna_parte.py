"""La raíz de ninguna parte (corte de serie del 2026-09-20).

`_familia_de_token()` acababa en `return "caquetío"` para todo lo que no
encontrara en el lexicón. La razón escrita era buena —«es un neologismo
comunitario, lengua propia»— y vale para una acuñación hecha con morfemas del
canon; no vale para una raíz que no está en ninguna tabla. Lo destapó el brazo
de CONTROL de la serie C (`0345840d` → `45618069` → `e98227eb`):
`lumina-bana-iro` fue la segunda forma más fuerte de la disputa de las cuentas
y `lumina-bana-uco` **fijó** el cometa en el diccionario koiné, con `lumina`
latina. Un agente lo escribió en su propia glosa: «lumina: cosa-que-brilla
(del español, pero transformada en caquetío)».

Lo que vigilan, en orden:

  (a) LA REGLA ES DE RAÍZ, NO DE FORMA. `lumina-bana-iro` no es caquetío y
      `kasi-nii-bana` sí, con la misma morfología: lo único que cambia es si
      la raíz está en el lexicón.
  (b) LA ACUÑACIÓN LEGÍTIMA SIGUE FUNCIONANDO. Una forma nueva sobre raíz
      conocida se registra, compite y se adopta como siempre. Esto es la mitad
      que importa: la puerta tiene que dejar pasar lo que el experimento mide.
  (c) LA RAÍZ AJENA NO PASA POR NINGUNA DE LAS TRES PUERTAS — registro,
      competencia y recuento emergente — y el rechazo SE CUENTA aparte del de
      las formas de plantilla, porque son dos defectos distintos.
  (d) `word_uses.source_language` DEJA DE DECIR «caquetío». Se propone
      `desconocida` para lo que sale del scorer y `acuñada` para lo que la
      respuesta declaró como acuñación: la fila se escribe igual —un rechazo
      callado es un dato perdido— pero no vestida de lengua propia.
  (e) LO QUE NO SE TOCÓ. Ninguna clave del lexicón cambia de lengua, el
      scorer no ve raíces ajenas en ningún token que pueda reconocer, y la
      ERA 1 no se mueve en un control de frases fijas.

Medición del corte: `6-fusion/medicion_raices_de_ninguna_parte_2026-09-20.yaml`
(`6-fusion/scripts/medir_raices_de_ninguna_parte.py`).
"""
import pytest

import curiana_koine as koine
import curiana_lexicon as lx
from curiana_koine import CompetenciaLexica
from curiana_lexicon import (
    LexicoComunitario,
    Neologismo,
    VOCABULARIO_BASE,
    es_forma_de_plantilla,
    es_raiz_de_ninguna_parte,
    nucleo_de_token,
    score_linguistico,
)

# Las que el brazo de control fabricó, con su raíz latina. No es una lista
# decorativa: son las formas que se dijeron y que llegaron a la koiné.
DE_NINGUNA_PARTE = ["lumina", "lumina-bana", "lumina-bana-iro",
                    "lumina-bana-uco", "tapa-uco"]

# Acuñaciones con la MISMA morfología sobre raíz del lexicón. `kasi-nii-bana`
# es la que fijó el eclipse en el brazo con escena; `biro-ana` usa el locativo
# sobre la sal de Guaranao.
# `kasuta-bana-iro` (la que ganó «las cuentas» en la serie C limpia) pasa a
# `halira-bana-iro`: `kasuta` se archivó en la tanda de las hermanas
# (2026-09-24) y una raíz archivada ya no avala en la puerta (db.1).
DEL_CANON = ["kasi-nii-bana", "biro-ana", "halira-bana-iro", "juri-ima"]


def _neo(forma: str, autor: str = "Manaure") -> Neologismo:
    return Neologismo(turno=1, dia=1, autor=autor, forma=forma,
                      componentes="x + y", significado="algo",
                      contexto="", regla_aplicada="")


# ══════════════════════════════════════════════════════════════════════
# (a) la regla es de RAÍZ
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("forma", DE_NINGUNA_PARTE)
def test_a_lumina_bana_iro_no_es_caquetio(forma):
    assert es_raiz_de_ninguna_parte(forma), forma
    assert lx._familia_de_token(forma) == "desconocida", forma


@pytest.mark.parametrize("forma", DEL_CANON)
def test_a_kasi_nii_bana_si_es_caquetio(forma):
    assert not es_raiz_de_ninguna_parte(forma), forma
    assert lx._familia_de_token(forma) == "caquetío", forma


def test_a_el_nucleo_es_lo_que_queda_al_quitar_los_afijos_declarados():
    assert nucleo_de_token("lumina-bana-iro") == ["lumina"]
    assert nucleo_de_token("ta-kasi-nii-bana") == ["kasi", "nii"]
    assert nucleo_de_token("biro-ana") == ["biro"]
    # Un token sin guion es su propio núcleo, y uno que es todo afijo no se
    # queda vacío: se para en el último segmento.
    assert nucleo_de_token("lumina") == ["lumina"]
    assert nucleo_de_token("bana") == ["bana"]


def test_a_no_es_lo_mismo_que_la_compuerta_fonotactica():
    """`neologismo_valido()` mira la FORMA y `lumina` pasa sus tres capas: no
    está en la blocklist, no tiene marcadores ortográficos castellanos y sus
    bigramas son corrientes en caquetío. Hacen falta las dos."""
    assert lx.neologismo_valido("lumina-bana-iro")
    assert es_raiz_de_ninguna_parte("lumina-bana-iro")


def test_a_la_raiz_decide_antes_que_el_legado():
    """`_familia_de_token` prueba como último recurso `tok.split('-', 1)[1]`.
    Con una raíz ajena ese legado resolvía por el SUFIJO: `pütshi-bana` habría
    salido caquetío por la clave `bana` 'hígado', que ahí no es la raíz.

    El ejemplo era `pütshi-bana` hasta la tanda de la base (2026-09-23): desde
    db.1 C es una casi-raíz de `pütchi` y se perdona (ver
    test_tanda_base.py). El caso del legado es el mismo con `lumina-bana`."""
    assert "bana" in VOCABULARIO_BASE
    assert es_raiz_de_ninguna_parte("lumina-bana")
    assert lx._familia_de_token("lumina-bana") == "desconocida"
    # y la puerta y el clasificador dicen lo MISMO de la misma forma
    for forma in DE_NINGUNA_PARTE + DEL_CANON + ["pütshi-bana", "lumina-bana", "ka-to"]:
        ajena = es_raiz_de_ninguna_parte(forma)
        assert (lx._familia_de_token(forma) == "desconocida") is ajena, forma


# ══════════════════════════════════════════════════════════════════════
# (b) la acuñación legítima sigue funcionando
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("forma", DEL_CANON)
def test_b_la_acunacion_sobre_raiz_conocida_se_registra(forma):
    lexico = LexicoComunitario()
    assert lexico.registrar_neologismo(_neo(forma)) is True, forma
    assert lexico.rechazos_de_raiz == []
    assert forma in {n.forma for n in lexico._neologismos}


@pytest.mark.parametrize("forma", DEL_CANON)
def test_b_la_acunacion_sobre_raiz_conocida_compite(forma):
    comp = CompetenciaLexica()
    comp.activar("eclipse", "el sol que se apaga")
    comp.proponer("eclipse", forma, "Manaure")
    assert forma in comp.referentes["eclipse"]["variantes"], forma


def test_b_y_se_adopta_y_entonces_puntua():
    """El recorrido entero: acuñar → adoptar → `palabras_activas()` →
    `palabras_caquetias`. Es lo que la puerta NO puede romper."""
    lexico = LexicoComunitario()
    neo = _neo("kasi-nii-bana")
    neo.estado = "adoptado"
    assert lexico.registrar_neologismo(neo) is True
    assert "kasi-nii-bana" in lexico.palabras_activas()
    r = score_linguistico("Taya naa-ka kasi-nii-bana wara.", lexico)
    assert "kasi-nii-bana" in r["palabras_caquetias"]


def test_b_el_recuento_emergente_la_deja_pasar():
    for forma in DEL_CANON:
        assert forma not in lx.PUERTA_DEL_RECUENTO, forma


# ══════════════════════════════════════════════════════════════════════
# (c) la raíz ajena no pasa por ninguna de las tres puertas
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("forma", DE_NINGUNA_PARTE)
def test_c_no_se_registra(forma):
    lexico = LexicoComunitario()
    assert lexico.registrar_neologismo(_neo(forma)) is False, forma
    assert lexico._neologismos == []
    assert [f for f, *_ in lexico.rechazos_de_raiz] == [forma]
    # y el rechazo se DICE al cerrar el run
    assert forma in lexico.reporte_de_rechazos()
    assert "raíz fuera del lexicón" in lexico.reporte_de_rechazos()


@pytest.mark.parametrize("forma", DE_NINGUNA_PARTE)
def test_c_no_compite(forma):
    comp = CompetenciaLexica()
    comp.activar("cometa", "una luz que cruza el cielo")
    comp.proponer("cometa", forma, "Manaure")
    assert forma not in comp.referentes["cometa"]["variantes"], forma


@pytest.mark.parametrize("forma", DE_NINGUNA_PARTE)
def test_c_no_cuenta_como_forma_emergente(forma):
    """La tercera puerta: el orquestador mete en el campo léxico todo lo que
    el agente acuñó sin preguntar si el léxico lo aceptó. Sin esto,
    `lumina-bana-uco` seguiría en el diccionario koiné del cierre."""
    assert forma in lx.PUERTA_DEL_RECUENTO, forma


def test_c_los_dos_rechazos_se_cuentan_aparte():
    """«Estaba en el prompt» y «la raíz no es de aquí» son dos defectos
    distintos: mezclarlos escondería cuál está pasando."""
    lexico = LexicoComunitario()
    plantilla = lx.IDENTIDAD_LINGUISTICA.split("[")[-1].split(":")[0]
    assert es_forma_de_plantilla(plantilla), plantilla
    lexico.registrar_neologismo(_neo(plantilla))
    lexico.registrar_neologismo(_neo("lumina-bana-iro"))
    assert [f for f, *_ in lexico.rechazos_de_plantilla] == [plantilla]
    assert [f for f, *_ in lexico.rechazos_de_raiz] == ["lumina-bana-iro"]
    assert lexico.reporte_de_rechazos().count("acuñaciones rechazadas") == 2


def test_c_sin_filtro_la_puerta_no_existe():
    """`filtrar_plantilla=False` es el motor de ANTES del corte, y es lo que
    usan las mediciones para reproducir la base. Tiene que seguir dejando
    pasar las dos cosas."""
    lexico = LexicoComunitario(filtrar_plantilla=False)
    assert lexico.registrar_neologismo(_neo("lumina-bana-iro")) is True
    comp = CompetenciaLexica(filtrar_plantilla=False)
    comp.activar("cometa", "una luz")
    comp.proponer("cometa", "lumina-bana-iro", "Manaure")
    assert "lumina-bana-iro" in comp.referentes["cometa"]["variantes"]


# ══════════════════════════════════════════════════════════════════════
# (d) la etiqueta de `word_uses.source_language`
# ══════════════════════════════════════════════════════════════════════

def test_d_lo_que_sale_del_scorer_se_guarda_como_desconocida():
    from curiana_database import word_source_language
    assert word_source_language("lumina-bana-iro") == "desconocida"
    assert word_source_language("kasi-nii-bana") == "caquetío"


def test_d_lo_que_la_respuesta_acuna_se_guarda_como_acunada():
    """La fila se escribe igual: es el único rastro que queda de que se dijo,
    porque el motor ya no la registra ni la deja competir."""
    from curiana_database import lengua_de_acunacion
    assert lengua_de_acunacion("lumina-bana-iro") == "acuñada"
    assert lengua_de_acunacion("kasi-nii-bana") == "caquetío"


# ══════════════════════════════════════════════════════════════════════
# (e) lo que NO se tocó
# ══════════════════════════════════════════════════════════════════════

def test_e_ninguna_clave_del_lexicon_cambia_de_lengua():
    """La comprobación cara, sobre las 5.507: si una sola clave saliera
    «desconocida» de su propia entrada, el diccionario quedaría falseado."""
    from curiana_database import normalize_source_language, word_source_language
    malas = [(p, normalize_source_language(d.get("fuente", "")),
              word_source_language(p))
             for p, d in VOCABULARIO_BASE.items()
             if word_source_language(p) != normalize_source_language(
                 d.get("fuente", ""))]
    assert not malas, malas[:5]


def test_e_las_archivadas_siguen_siendo_del_canon():
    """`FUERA_DEL_HABLA` cuenta como raíz conocida: archivar no es borrar, y
    `kali` sigue siendo caquetío aunque la comunidad ya no lo hable."""
    for forma in lx.FUERA_DEL_HABLA:
        assert not es_raiz_de_ninguna_parte(forma), forma
    assert lx._familia_de_token("kali-mara-bana") == "caquetío"


def test_e_el_scorer_no_ve_raices_ajenas():
    """El scorer sólo llama a `_familia_de_token` sobre tokens que ya aceptó
    como arahuacos, y para aceptarlos tienen que estar en `palabras_activas()`
    (que es `VOCABULARIO_BASE` + lo adoptado) o empezar por raíz verbal. Con
    la puerta puesta, nada adoptado puede tener raíz ajena — así que el
    scorer nunca clasifica «desconocida» y ni `score` ni `pct_*` se mueven
    por esta vía. Aquí se comprueba el caso que lo destapó."""
    lexico = LexicoComunitario()
    r = score_linguistico("Taya naa-ka lumina-bana-iro wara kari.", lexico)
    assert "lumina-bana-iro" not in r["palabras_arahuacas"]
    assert "lumina-bana-iro" not in r["palabras_caquetias"]
    assert r["otro_arahuaco"] == 0          # no penaliza: no lo ve


# El control de la ERA 1: frases fijas, con el elenco viejo. El número grande
# —cuánto se mueve la era 1 entera al re-puntuar sus 2.071 respuestas— lo mide
# `6-fusion/scripts/medir_raices_de_ninguna_parte.py`, que las corre con los
# dos lexicones; esto fija que el scorer NO cambió para lo que ya reconocía.
FRASES_ERA1 = [
    "Taya wana-ka arima wara kari. Ta-barsure naba-ni.",
    "Waya naa-da duna-ko. Wa-duna masa-ka.",
    "Nüma jai-ni ta-kasi. Kashi wana-da para-ko.",
    "Ma-arua panaa-ka. Naya were-da biro wara.",
]


@pytest.mark.parametrize("frase", FRASES_ERA1)
def test_e_la_era_1_no_se_mueve(frase):
    """Sobre lo que el scorer YA reconocía, el corte no cambia nada: ninguna
    de estas frases usa una raíz de fuera, así que el camino nuevo ni se
    activa. Se comprueba contra el propio módulo, no contra una cifra a mano:
    todos sus tokens tienen raíz conocida."""
    lexico = LexicoComunitario()
    r = score_linguistico(frase, lexico)
    assert r["palabras_caquetias"]
    for tok in r["palabras_arahuacas"]:
        assert not es_raiz_de_ninguna_parte(tok), tok
        assert lx._familia_de_token(tok) != "desconocida", tok
