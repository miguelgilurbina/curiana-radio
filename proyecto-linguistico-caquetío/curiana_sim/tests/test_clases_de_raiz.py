"""La clase de la raíz (corte de serie del 2026-09-20).

En `minar_zavala_glosario.py` la parte de la oración de todo el vocabulario
activo salía de una línea —`_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}`, con el
comentario «heurística de POS; el resto, sust»— y T4 es el **cajón de resto**
del minador. De ahí salían **49** entradas con `cat: v_raiz`, y de ahí sale
`curiana_lexicon._RAICES_VERB`, que hace que `score_linguistico()` cuente como
arahuaco cualquier token cuyo primer segmento sea una de ellas: `juri-ni`,
`popoi-ka`, `dichiba-ni`.

⚠️ Y **no es que cuarenta no sean verbos** (corrección de Miguel el mismo día).
En arahuaco mucho de lo que el castellano llama adjetivo es un **verbo
estativo** — Perea y Alonso 1942 pp. 634-639: la 4ª conjugación lokono es «la
clase de los estativos: colores, tamaños, sabores, estados» (`cule-n` 'ser
rojo', `hebbe-n` 'ser viejo'). Diez de las 49 son de esa clase y **siguen
conjugándose**; lo que cambia es que ahora está declarado.

⚠️ ACTUALIZADO POR LA TANDA DEL 2026-09-21 (d21.4, «Vale vamos con la B
entonces»): las diez estativas dejan de emitirse con `cat: v_raiz` y pasan a
`cat: v_estativo`. NO es una poda: `curiana_lexicon.CATS_VERBALES` las cuenta
como verbales igual, así que toman los mismos tres aspectos y `_RAICES_VERB`
no pierde ni gana una raíz. Lo que se gana es que la clase está DECLARADA y
llega al prompt. Sin alineamiento pospuesto (opción C, descartada: cero dato
caquetío).

Lo que vigilan, en orden:

  (a) NADA SE DECIDE YA POR HEURÍSTICA. Toda entrada del glosario que salga
      `v_raiz` tiene fila declarada, y `SIN_CLASE_DECLARADA` está vacía.
  (b) EL REPARTO ES EL QUE SE MIDIÓ, y cada fila lleva su razón con cita
      (regla 8) o declara su deuda.
  (c) LOS ESTATIVOS Y LAS ACCIONES SIGUEN CONJUGÁNDOSE. `apo-ni`, `usera-ka`
      cuentan como arahuacas; es la mitad que importa.
  (d) LOS NOMBRES DEJAN DE CONJUGARSE Y PASAN A PREDICARSE CON `ka-`/`ma-`
      (van Buurt 2014 §8). `juri-ni` ya no cuenta, `ka-juri` y `ma-juri` sí —
      el corte cierra la puerta mala y deja abierta la buena.
  (e) LO QUE NO SE TOCÓ. `glosa_fuente` es verbatim de la fuente y ninguna
      entrada la perdió; la capa epistémica de las 30 sigue intacta; el
      vocabulario no encoge ni crece.
  (f) LA REGENERACIÓN NO DESTRUYE. Los homógrafos formales con la comparanda
      achagua y lokono están declarados y sus entradas siguen en el módulo.

Medición del corte: `6-fusion/medicion_clases_de_raiz_2026-09-20.yaml`
(`6-fusion/scripts/medir_clases_de_raiz.py`). Lo que queda propuesto y sin
aplicar: `6-fusion/clases_de_raiz_zavala_2026-09-20.yaml`.
"""
import pytest

import curiana_lexicon as lx
import minar_zavala_glosario as M
from curiana_lexicon import LexicoComunitario, VOCABULARIO_BASE, score_linguistico
from lexicon_zavala import (
    CLASES_DE_RAIZ_ZAVALA,
    GLOSARIO_ZAVALA,
    REPARTO_DE_CLASES,
    SIN_CLASE_DECLARADA,
)

CLASES_VERBALES = {"estativo", "accion"}
CLASES_NOMINALES = {"nombre", "adverbio"}
CAT_DE_CLASE = {"estativo": "v_estativo", "accion": "v_raiz",
                "nombre": "sust", "adverbio": "part"}


def _reconoce(tok: str) -> bool:
    """¿El scorer cuenta este token como arahuaco? Se le pregunta a él."""
    lexico = LexicoComunitario()
    r = score_linguistico(f"taya {tok} yama", lexico)
    return tok in set(r["palabras_arahuacas"])


# ── (a) nada se decide ya por heurística ──────────────────────────────
def test_ninguna_entrada_sale_v_raiz_sin_declararlo():
    assert SIN_CLASE_DECLARADA == [], (
        "el cajón de resto volvió a decidir solo: estas entradas salen "
        f"`v_raiz` por heurística de tier — {SIN_CLASE_DECLARADA}")


def test_toda_v_raiz_del_glosario_tiene_clase_verbal_declarada():
    for forma, e in GLOSARIO_ZAVALA.items():
        if e.get("cat") not in lx.CATS_VERBALES:
            continue
        fila = CLASES_DE_RAIZ_ZAVALA.get(forma)
        assert fila, f"`{forma}` es v_raiz y no tiene clase declarada"
        assert fila["clase"] in CLASES_VERBALES, (
            f"`{forma}` es v_raiz pero se declaró «{fila['clase']}»")


def test_la_cat_emitida_es_la_que_la_clase_manda():
    for forma, fila in CLASES_DE_RAIZ_ZAVALA.items():
        assert fila["cat"] == CAT_DE_CLASE[fila["clase"]], forma
        assert GLOSARIO_ZAVALA[forma]["cat"] == fila["cat"], (
            f"`{forma}` se declaró {fila['cat']} y el módulo emite "
            f"{GLOSARIO_ZAVALA[forma]['cat']}")


# ── (b) el reparto, y su razón ────────────────────────────────────────
def test_el_reparto_es_el_medido():
    assert REPARTO_DE_CLASES == {"estativo": 10, "accion": 9,
                                 "nombre": 29, "adverbio": 1}
    assert sum(REPARTO_DE_CLASES.values()) == 49


def test_cada_fila_declara_su_apoyo_o_su_deuda():
    for forma, fila in CLASES_DE_RAIZ_ZAVALA.items():
        por = str(fila.get("por") or "")
        assert len(por) > 40, f"`{forma}` no dice por qué"
        # Regla 8: o cita una obra de 4-fuentes/bibliografia.yaml, o declara
        # el hueco. Callarlo no vale.
        cita = any(o in por for o in (
            "perea-alonso-1942", "neira-ribero-1762", "van-buurt-2014",
            "zavala-reyes-2015", "oliver-1989", "gatschet-1885",
            "medina-colina-sxx", "velasco-2015-resistencia", "morfologia.md"))
        assert cita or "deuda: sin-procedencia" in por, (
            f"`{forma}` no cita obra ni declara deuda")


def test_las_tres_que_el_lexicon_ya_glosaba_en_forma_verbal_son_estativas():
    """El apoyo más limpio: el propio lexicón ya decía «ser entero», «ser
    salado», «estar seco» de las voces hermanas. El proyecto ya sabía que el
    concepto es un verbo; sólo no lo había dicho del caquetío."""
    for forma in ("waidima", "waranao", "usera", "wasima"):
        assert CLASES_DE_RAIZ_ZAVALA[forma]["clase"] == "estativo", forma


def test_popoi_es_adverbio_porque_lo_dice_la_fuente():
    e = GLOSARIO_ZAVALA["popoi"]
    assert "Adverbio de lugar" in e["glosa_fuente"]
    assert e["cat"] == "part", (
        "`popoi` es la clase de `yama` 'aquí' y `kana-pa` 'allá'")
    # Tanda final (tf.5): `yama` se archivó —reconstruida desde el wayuu— y
    # `popoi` ocupa su sitio en la plantilla. El precedente de la clase sigue
    # en el archivo, con su `cat` intacta.
    from curiana_lexicon import FUERA_DEL_HABLA
    assert FUERA_DEL_HABLA["yama"]["cat"] == "part", (
        "el precedente de la clase se movió: revisar `popoi`")


# ── (c) los verbos siguen conjugándose ────────────────────────────────
@pytest.mark.parametrize("tok", ["apo-ni", "usera-ka", "waidima-da",
                                 "kachipo-ni", "badamaro-ka", "gide-ni"])
def test_el_estativo_y_la_accion_siguen_contando_conjugados(tok):
    assert _reconoce(tok), f"`{tok}` dejó de contar y no debía"


def test_los_diecinueve_verbos_siguen_en_raices_verb():
    verbales = {f for f, c in CLASES_DE_RAIZ_ZAVALA.items()
                if c["clase"] in CLASES_VERBALES}
    assert verbales <= lx._RAICES_VERB
    assert len(verbales) == 19


# ── (d) los nombres se predican con ka-/ma-, no con aspecto ───────────
def test_el_nombre_deja_de_tomar_aspecto():
    for tok in ("juri-ni", "juri-ka", "juri-da", "popoi-ni", "dichiba-ni"):
        assert not _reconoce(tok), (
            f"`{tok}` sigue contando: la puerta mala no se cerró")


def test_la_via_arahuaca_sigue_abierta():
    """van Buurt 2014 §8: `ka-` atributivo/existencial («hay, existe(n)») y
    `ma-` privativo. `es_arahuaco()` ya los acepta sobre cualquier forma
    activa — el corte no toca esto, y por eso hay que fijarlo."""
    for tok in ("ka-juri", "ma-juri", "ta-juri", "wa-juri"):
        assert _reconoce(tok), f"`{tok}` debería seguir contando"


def test_juri_a_secas_sigue_siendo_caquetio():
    e = VOCABULARIO_BASE["juri"]
    # Era `caquetío-atestiguado` hasta el 2026-09-23: la (E) de Zavala #178 es
    # Esteves 1989, que saca 'viento' de partir tres topónimos (cc.4 / tf.0,
    # opción B → hipotética). Lo que este test vigila no se mueve: `juri` a
    # secas sigue siendo CAQUETÍO (la capa no es la lengua) y sigue contando.
    assert e["fuente"] == "caquetío-hipotético"
    assert lx.capa_epistemica(e["fuente"]) is not None
    assert _reconoce("juri")
    assert lx._familia_de_token("juri-ni") == "caquetío", (
        "la raíz SÍ es caquetía: lo que está mal es el molde, no la lengua")


def test_el_nombre_se_comporta_como_cualquier_otro_nombre_del_lexicon():
    """El corte no le pone a `juri` una penalización nueva: le quita un
    privilegio que ningún otro nombre del lexicón tenía. `biro` y `kasi` son
    atestiguados y nunca contaron con sufijo."""
    for nombre in ("biro", "kasi", "juri", "popoi"):
        assert _reconoce(nombre), nombre
        assert not _reconoce(f"{nombre}-bana"), nombre


# ── (e) lo que no se tocó ─────────────────────────────────────────────
def test_la_glosa_verbatim_de_la_fuente_sigue_entera():
    for forma, fila in CLASES_DE_RAIZ_ZAVALA.items():
        e = GLOSARIO_ZAVALA[forma]
        assert e.get("glosa_fuente"), f"`{forma}` perdió su glosa_fuente"
        assert f"#{fila['num']}" in e["glosa_fuente"], forma
        # `sig` se deriva de la glosa verbatim y tampoco se tocó en esta tanda.
        # Salvo excepción DECLARADA en SIG_CURADO, con su razón: `komoho`
        # (T2 de la tanda de las hermanas, 2026-09-24) precisa 'higo' como el
        # higo de tuna por Oviedo p. 313; la glosa verbatim sigue en glosa_fuente.
        if fila["forma_zavala"] in M.SIG_CURADO:
            assert e["sig"] == M.SIG_CURADO[fila["forma_zavala"]]["sig"], forma
            continue
        assert e["sig"].lower().startswith(
            e["glosa_fuente"].split(" [Zavala")[0][:12].lower()), forma


def test_la_capa_epistemica_no_se_movio():
    """La corrección de `cat` no movió ninguna capa. Desde el 2026-09-23 la
    capa SÍ se mueve en algunas de estas raíces, pero por otra decisión y por
    otra puerta: `M.FUENTE_CURADA` (tf.0, los pemenos de `baperon`/`raporon`;
    cc.4, la sigla (E) de Zavala es Esteves). Lo que este test sigue vigilando
    es que ninguna capa cambie SIN fila declarada en esa tabla."""
    for forma, fila in CLASES_DE_RAIZ_ZAVALA.items():
        curada = M.FUENTE_CURADA.get(fila["forma_zavala"])
        esperada = curada["fuente"] if curada else "caquetío-atestiguado"
        assert GLOSARIO_ZAVALA[forma]["fuente"] == esperada, (
            f"`{forma}` cambió de capa sin fila en FUENTE_CURADA: esto era una "
            "corrección de `cat`")


def test_las_49_siguen_en_el_vocabulario_activo():
    """Reclasificar no es archivar: nada sale del habla."""
    for forma in CLASES_DE_RAIZ_ZAVALA:
        assert forma in VOCABULARIO_BASE, forma
        assert forma not in lx.FUERA_DEL_HABLA, forma


# ── (f) la regeneración no destruye ───────────────────────────────────
def test_los_homografos_de_la_comparanda_estan_declarados_y_sus_voces_vivas():
    """El cruce del minador contra `VOCABULARIO_BASE` incluye las 3.569
    entradas achagua desde el 2026-09-13, así que una coincidencia de grafía
    entre dos lenguas se leía como «ya está» y la regeneración borraba la voz
    caquetía. `NO_ES_LA_MISMA_VOZ` lo impide, fila a fila y con su razón."""
    import lexicon_zavala as Z
    # `aburi` (2026-09-24): el topónimo de Zavala contra la voz reconstruida
    # 'tener vergüenza' de la tanda de las hermanas.
    assert set(M.NO_ES_LA_MISMA_VOZ) == {
        "cana", "carama", "cuna", "turupia", "ima", "coa", "aburi"}
    assert "aburi" in Z.TOPONIMOS_ZAVALA, "el topónimo aburi se perdió al regenerar"
    for razon in M.NO_ES_LA_MISMA_VOZ.values():
        assert len(razon) > 40
    # Las cuatro voces y los dos afijos que se perdían.
    for forma in ("kana", "karama", "kuna", "turupia"):
        assert forma in GLOSARIO_ZAVALA, (
            f"`{forma}` desapareció del generado: la deriva volvió")
    for afijo in ("-ima", "-aima"):
        assert afijo in Z.AFIJOS_ZAVALA, (
            f"`{afijo}` desapareció: son «el hallazgo de mayor valor» "
            "según la cabecera del propio minador")
    assert len(Z.AFIJOS_ZAVALA) == 8
