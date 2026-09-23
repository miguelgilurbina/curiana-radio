"""La política «manda la atestiguada» (corte de serie del 2026-09-19).

Miguel:

    «Sí o sí tenemos que usar los atestiguados por sobre los reconstruidos,
     por lo menos la parte caquetía.»

Donde el caquetío TIENE forma atestiguada para un significado, ésa es la que
la comunidad habla y la que el instrumento enseña; la derivada se ARCHIVA en
`FUERA_DEL_HABLA` con su procedencia —como `piache`— y deja de enseñarse y de
competir. La política sólo muerde donde hay rival atestiguado: el grueso del
lexicón caquetío es reconstrucción legítima porque no hay atestación, y estos
tests comprueban también que ESO no se ha tocado.

Lo que vigilan, en orden:

  (a) EL ARCHIVO ES UN EJE DISTINTO DE LA ETIQUETA. La entrada archivada
      conserva su `fuente` y su `notas`: archivar no es degradar ni borrar.
  (b) UNA FORMA ARCHIVADA NO SE ENSEÑA. Ninguna de las diez plantillas
      estáticas la dice, ni siquiera como token, ni dentro de un compuesto;
      tampoco la siembra `FORMAS_SEED`, que es instrumento y no emergencia.
  (c) UNA FORMA ARCHIVADA NO COMPITE. Ni se registra como acuñación
      (`LexicoComunitario.registrar_neologismo`) ni entra en la competencia
      (`CompetenciaLexica.proponer`), y el rechazo se CUENTA.
  (d) UNA FORMA ARCHIVADA NO PUNTÚA, y LA ATESTIGUADA SÍ — con su paradigma
      de aspecto entero, que es lo que hacía cara la decisión de `paa`.
  (e) LA POLÍTICA NO SE COMIÓ EL NÚCLEO: los pronombres, los aspectos y las
      reconstruidas sin rival atestiguado siguen enteras.

Medición del corte: `6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml`.
"""
import pytest

import curiana_koine as koine
import curiana_lexicon as lx
from curiana_koine import CompetenciaLexica
from curiana_lexicon import (
    FUERA_DEL_HABLA,
    LexicoComunitario,
    Neologismo,
    VOCABULARIO_BASE,
    es_forma_de_plantilla,
    score_linguistico,
)

# Los siete pares que la política cerró: (par, glosa, la que MANDA, la
# ARCHIVADA). No es una copia del YAML medido: es lo que estos tests exigen
# del módulo, y si el módulo cambia sin que nadie lo decida, se caen.
POLITICA = [
    (1,  "sol",      "kasi",  "kali"),
    (3,  "ofrecer",  "were",  "paa"),
    (4,  "escuchar", "jai",   "kira"),
    (12, "luna",     "kati",  "kasha"),
    (13, "mar",      "para",  "habo"),
    (16, "viento",   "juri",  "joutai"),
    (18, "espanto",  "etamo", "mülia"),
]
ARCHIVADAS = [d for _n, _g, _a, d in POLITICA]
MANDAN = [a for _n, _g, a, _d in POLITICA]

# El par 16 «viento» DEJÓ DE SER un caso de la política el 2026-09-23 (cc.4 /
# tf.0, respuestas 1-B y 2-a del issue sigla-E-zavala-canon-2026-09-23.md):
# la (E) de Zavala #178 es Esteves 1989 y `juri` pasó a hipotética, así que ya
# no hay atestiguada que mande. `joutai` SIGUE archivada —no vuelve: es wayuu
# y cc.12 manda no reconstruir desde el wayuu—, con el motivo reescrito. Se
# queda en POLITICA porque todo lo que los tests (b)-(d) exigen de una
# archivada le sigue valiendo; lo que cambia se dice aquí.
YA_NO_MANDA_POR_ATESTIGUADA = {"juri": "caquetío-hipotético"}
MOTIVO_REESCRITO = {"joutai": "2026-09-23 · D11 / cc.12"}

# La capa con la que cada archivada entró al archivo. Archivar NO la cambia.
CAPA_AL_ARCHIVAR = {
    "kali": "caquetío-reconstruido", "paa": "caquetío-reconstruido",
    "kira": "caquetío-reconstruido", "kasha": "caquetío-reconstruido",
    "habo": "caquetío-reconstruido", "joutai": "caquetío-reconstruido",
    "mülia": "caquetío-hipotético",
}

# Reconstruidas del núcleo SIN rival atestiguado: la política no las toca.
# Si alguna apareciera archivada, la política se habría comido el núcleo.
# Tanda final (2026-09-23): `taya`, `pia`, `nüma` y `wana` salieron del habla,
# pero NO por esta política —no tenían rival atestiguado—, sino por D11 fase 3
# (cc.12: nada reconstruido desde el wayuu). Lo que este test fija sigue
# valiendo: la política d19.b no los alcanzaba. Salen de la lista con su nota.
NUCLEO_INTACTO = ("waya", "naya",
                  "naa", "waa", "kaa", "maa", "chaa", "suna",
                  "kuru", "arima", "bara", "sima", "duna", "amana", "dali")


def _neo(forma, autor="Manaure", dia=1, turno=1):
    return Neologismo(turno=turno, dia=dia, autor=autor, forma=forma,
                      componentes="x + y", significado="algo",
                      contexto="", regla_aplicada="")


# ══════════════════════════════════════════════════════════════════════
# (a) archivar no es degradar ni borrar
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("par,glosa,manda,archivada", POLITICA)
def test_a_la_archivada_sale_del_habla_y_conserva_su_procedencia(
        par, glosa, manda, archivada):
    assert archivada not in VOCABULARIO_BASE, (
        f"`{archivada}` (par {par}) sigue en el habla activa")
    assert archivada in FUERA_DEL_HABLA, (
        f"`{archivada}` no está archivada: archivar no es borrar")
    e = FUERA_DEL_HABLA[archivada]
    assert e.get("sig"), "la glosa se conserva"
    assert str(e.get("notas") or "").strip(), (
        "la procedencia se conserva entera — regla 8")
    assert "ARCHIVADA DEL HABLA" in e["notas"], (
        "el archivo se declara en la propia entrada, con su porqué")
    if archivada in MOTIVO_REESCRITO:
        # el motivo nuevo delante, y el del 2026-09-19 conservado detrás
        assert e["archivada"].startswith(MOTIVO_REESCRITO[archivada])
        assert "2026-09-19 · política atestiguado-manda" in e["archivada"]
        assert "MOTIVO DEL ARCHIVO CAMBIADO 2026-09-23" in e["notas"]
        return
    assert e.get("archivada", "").startswith("2026-09-19"), (
        "la marca de archivo lleva su fecha y su par")


@pytest.mark.parametrize("archivada,capa", sorted(CAPA_AL_ARCHIVAR.items()))
def test_a_archivar_no_cambia_la_capa_epistemica(archivada, capa):
    """La etiqueta dice DE DÓNDE VIENE la palabra; el archivo, si la comunidad
    la habla. Son dos ejes y mezclarlos rompería la regla 2."""
    assert FUERA_DEL_HABLA[archivada]["fuente"] == capa


@pytest.mark.parametrize("par,glosa,manda,archivada", POLITICA)
def test_a_la_que_manda_es_atestiguada_y_con_cita(par, glosa, manda, archivada):
    """Regla 8: «atestiguado» es la etiqueta MÁS la cita, no la etiqueta."""
    assert manda in VOCABULARIO_BASE, f"`{manda}` tiene que estar en el habla"
    e = VOCABULARIO_BASE[manda]
    if manda in YA_NO_MANDA_POR_ATESTIGUADA:
        # par 16: la capa es la que decidió la sigla E, y sigue citando
        assert e["fuente"] == YA_NO_MANDA_POR_ATESTIGUADA[manda]
        assert "Esteves" in e["notas"]
        return
    assert e["fuente"] == "caquetío-atestiguado", (
        f"`{manda}` manda por atestiguada: su capa tiene que decirlo")
    assert str(e.get("notas") or "").strip(), (
        f"`{manda}` manda sin cita: eso no es atestiguar")


# ══════════════════════════════════════════════════════════════════════
# (b) una forma archivada no se enseña
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("archivada", ARCHIVADAS)
def test_b_ninguna_plantilla_estatica_dice_una_forma_archivada(archivada):
    """Las plantillas se LLAMAN, no se copian: si alguien vuelve a meter
    `kali` en el refuerzo, esto se cae."""
    dicen = [i for i, texto in enumerate(lx._textos_de_plantilla())
             if archivada in lx.formas_en_texto(texto)]
    assert not dicen, (
        f"`{archivada}` está archivada y la enseñan las plantillas {dicen}")


@pytest.mark.parametrize("archivada", ARCHIVADAS)
def test_b_el_refuerzo_tampoco_la_dice_cuando_recorta_por_el_final(archivada):
    """El refuerzo enseña por RECORTE (`verbos[:4]`), así que con
    `palabras_usadas=[]` sólo se ven las cuatro primeras de cada lista: `kira`
    y `kali` vivían en la quinta posición y la puerta NO las alcanzaba. A un
    agente que ya hubiera dicho las cuatro primeras se las enseñaba."""
    gastadas = ["wana", "suna", "masa", "awa", "barsure", "duna", "amana",
                "ka", "mara", "saa", "naka", "panaa", "naba", "naa", "maa",
                "kaa", "arima", "suka", "bara", "kuru", "kashi", "wara",
                "yama", "puna"]
    for score in (1.0, 3.0, 5.0, 6.5):
        texto = lx.prompt_refuerzo(score, gastadas)
        assert archivada not in lx.formas_en_texto(texto), (
            f"el refuerzo (score {score}) enseña `{archivada}` al agente que "
            "ya gastó las primeras de la lista")


@pytest.mark.parametrize("archivada", ARCHIVADAS)
def test_b_formas_seed_no_siembra_una_archivada(archivada):
    """`FORMAS_SEED` es instrumento, no emergencia: entra en `[Tu manera de
    hablar]` desde el día 1. Sembrar una archivada sería enseñarla por la
    puerta de atrás."""
    culpables = {agente: [f for f in formas
                          if f == archivada or f.split("-")[0] == archivada]
                 for agente, formas in koine.FORMAS_SEED.items()}
    culpables = {a: f for a, f in culpables.items() if f}
    assert not culpables, (
        f"`{archivada}` está archivada y FORMAS_SEED la siembra: {culpables}")


@pytest.mark.parametrize("par,glosa,manda,archivada", POLITICA)
def test_b_la_que_manda_llega_al_hablante(par, glosa, manda, archivada):
    """No basta con retirar: la atestiguada tiene que estar donde estaba la
    otra — en el muestreador (es clave del lexicón) y, las cinco que una
    plantilla enseñaba, también en la plantilla."""
    assert manda in lx.FORMAS_DE_PLANTILLA
    assert manda in VOCABULARIO_BASE
    if manda in ("kasi", "kati", "para", "were", "jai"):
        textos = lx._textos_de_plantilla()
        assert any(manda in lx.formas_en_texto(t) for t in textos), (
            f"`{manda}` ocupa el sitio de `{archivada}` y ninguna plantilla "
            "la dice")


# ══════════════════════════════════════════════════════════════════════
# (c) una forma archivada no compite
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("archivada", ARCHIVADAS)
def test_c_una_forma_archivada_no_se_registra_como_acunacion(archivada):
    """Sin esto, archivar sería una puerta giratoria: la voz sale de
    `VOCABULARIO_BASE`, sale de la puerta, y al día siguiente vuelve como
    «palabra nueva de la comunidad»."""
    assert es_forma_de_plantilla(archivada)
    lex = LexicoComunitario()
    assert lex.registrar_neologismo(_neo(archivada)) is False
    assert lex._neologismos == []
    assert [f for f, *_ in lex.rechazos_de_plantilla] == [archivada]
    assert archivada in lex.reporte_de_rechazos()


@pytest.mark.parametrize("archivada", ARCHIVADAS)
def test_c_una_forma_archivada_no_entra_en_competencia(archivada):
    comp = CompetenciaLexica()
    comp.activar("cuentas", "las cuentas brillantes")
    assert not comp.proponer("cuentas", archivada, "Manaure")
    assert not comp.referentes["cuentas"]["variantes"], (
        f"`{archivada}` está archivada y aun así compite por un referente")
    # y una rival legítima sí entra, para que el test no pase por estar rota
    # la competencia entera
    comp.proponer("cuentas", "kuru-bacoa", "Manaure")
    assert "kuru-bacoa" in comp.referentes["cuentas"]["variantes"]


def test_c_el_archivo_viejo_tambien_quedo_cerrado():
    """`piache` y los cinco numerales de D11 llevaban archivados desde el
    2026-08-03 y el 2026-09-13 y SÍ eran acuñables: entraron en la puerta con
    esta tanda, porque la puerta ahora incluye `FUERA_DEL_HABLA` entero."""
    for forma in ("piache", "wanee", "piama", "apünüin", "pienchi", "jarai"):
        assert es_forma_de_plantilla(forma), forma
        assert LexicoComunitario().registrar_neologismo(_neo(forma)) is False


def test_c_una_acunacion_legitima_sigue_pasando():
    """La puerta no se cerró de más: lo que nadie enseña y nadie archivó sí
    se registra."""
    lex = LexicoComunitario()
    assert lex.registrar_neologismo(_neo("kuru-bacoa")) is True
    assert not lex.rechazos_de_plantilla


# ══════════════════════════════════════════════════════════════════════
# (d) la archivada no puntúa; la atestiguada sí, con su paradigma
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("par,glosa,manda,archivada", POLITICA)
def test_d_la_archivada_sale_de_palabras_activas_y_la_que_manda_no(
        par, glosa, manda, archivada):
    activas = set(LexicoComunitario().palabras_activas())
    assert archivada not in activas, (
        "archivar saca la voz de `palabras_activas()`: eso es el corte de serie")
    assert manda in activas


@pytest.mark.parametrize("par,glosa,manda,archivada", POLITICA)
def test_d_el_scorer_cuenta_la_que_manda_y_no_la_archivada(
        par, glosa, manda, archivada):
    """El scorer NO se tocó —`score_linguistico`, `pct_*` y `capas_de_score`
    son los mismos—: lo que cambió es el lexicón del que lee."""
    lex = LexicoComunitario()
    # Tanda final: el marco era «taya … yama», y las dos voces se archivaron
    # (D11 fase 3). Con vecinos que ya no son arahuacos, `para` se leía como la
    # preposición castellana. El marco pasa a `dai` … `popoi`.
    assert manda in set(score_linguistico(f"dai {manda} popoi", lex)["palabras_caquetias"])
    assert archivada not in set(
        score_linguistico(f"dai {archivada} popoi", lex)["palabras_arahuacas"])


def test_d_no_queda_hueco_funcional_el_paradigma_se_muda_de_raiz():
    """El coste que había que decir antes de aplicar: `paa` era raíz verbal
    del núcleo con todo su paradigma de aspecto. No se rompe — `were` y `jai`
    son también `v_raiz` y atestiguadas, y toman los mismos tres aspectos."""
    lex = LexicoComunitario()
    for raiz in ("were", "jai"):
        assert raiz in lx._RAICES_VERB, f"`{raiz}` tiene que ser raíz verbal"
        for suf in ("", "-ka", "-ni", "-da"):
            tok = raiz + suf
            r = score_linguistico(f"taya {tok} yama", lex)
            assert tok in set(r["palabras_arahuacas"]), tok
    for raiz in ("paa", "kira"):
        assert raiz not in lx._RAICES_VERB
        for suf in ("", "-ka", "-ni", "-da"):
            tok = raiz + suf
            r = score_linguistico(f"taya {tok} yama", lex)
            assert tok not in set(r["palabras_arahuacas"]), tok


def test_d_los_tres_aspectos_siguen_declarados_y_sin_referencia_muerta():
    """`REGLAS_ASPECTO` no llega al prompt, pero es documentación del módulo:
    un ejemplo con una raíz archivada sería una referencia muerta."""
    for afijo, regla in lx.REGLAS_ASPECTO.items():
        for ejemplo in regla.get("ejemplos", []):
            raiz = ejemplo.split("-")[0].split(" ")[0].strip().lower()
            assert raiz not in ARCHIVADAS, (
                f"`{afijo}` se ejemplifica con `{raiz}`, que está archivada")


# ══════════════════════════════════════════════════════════════════════
# (e) la política no se comió el núcleo
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("forma", NUCLEO_INTACTO)
def test_e_la_reconstruccion_sin_rival_atestiguado_no_se_toca(forma):
    """El alcance de la política, fijado: sólo muerde donde EXISTE rival
    atestiguado. Los pronombres, los aspectos y la mayoría de las
    reconstruidas se quedan exactamente como están — convertir esto en una
    poda del núcleo sería otra decisión, y no está tomada."""
    assert forma in VOCABULARIO_BASE, (
        f"`{forma}` no tiene rival atestiguado: la política no la alcanza")
    assert forma not in FUERA_DEL_HABLA


def test_e_sima_sigue_viva_porque_es_pregunta_de_miguel():
    """El par 6 («cerro») lo ALCANZA la política —`turumako` es atestiguada,
    Zavala #262— y NO se ha aplicado: es la pregunta que Miguel dejó abierta
    y su coste está medido. Este test fija la conducta de HOY, para que el
    día que se decida, se vea cambiar."""
    assert "sima" in VOCABULARIO_BASE
    assert "sima" not in FUERA_DEL_HABLA
    assert VOCABULARIO_BASE["sima"]["fuente"] == "caquetío-reconstruido"
    assert "turumako" in VOCABULARIO_BASE
    assert VOCABULARIO_BASE["turumako"]["fuente"] == "caquetío-atestiguado"
    # y la plantilla la sigue enseñando, con su molde
    completo = lx.prompt_reglas_completo()
    assert "sima (cerro)" in completo
    assert "sima-bana" in lx.formas_en_texto(completo)


def test_e_la_colision_kasi_kashi_quedo_resuelta():
    """Tanda final (2026-09-23): `kashi` 'ahora' era reconstruida desde el
    wayuu y se archivó (tf.5); el ahora es `danu`. La colisión que el test de
    abajo declaraba ya no está en la plantilla: se comprueba que no vuelva."""
    completo = lx.prompt_reglas_completo()
    tokens = lx.formas_en_texto(completo)
    assert "kasi" in tokens and "kashi" not in tokens and "danu" in tokens
    assert "kashi" in FUERA_DEL_HABLA


