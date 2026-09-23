"""La tanda del 2026-09-21: las catorce decisiones, fijadas una a una.

`6-fusion/decisiones_tanda_2026-09-21.yaml` responde las catorce preguntas de
la auditoría de morfología (`6-fusion/issues-pendientes/
morfologia-revision-2026-09-20.md` §6) más las dos que salieron de la
conversación. Las que son código se aplicaron en UN SOLO corte de serie, con
UNA SOLA medición (`6-fusion/medicion_tanda_21_2026-09-21.yaml`).

Cada test de aquí fija UNA decisión, con su letra y su cita. Lo que vigilan:

  d21.1 C   el comodín de longitud del detector de aspecto está muerto: el
            aspecto cuenta sobre el ÚLTIMO segmento verbal y no sobre «tres
            letras y un guion». `ta-hamaka-chaa-ni` sigue contando por `chaa`,
            que es el caso bueno que el comodín cubría a ciegas.
  d21.2 A   `_RAICES_VERB` mezcla las cinco lenguas y las DOS puertas que
            deciden densidad y aspecto miran sólo la caquetía.
  d21.4 B   la clase estativa está declarada en la `cat` y llega al prompt, y
            un estativo sigue tomando aspecto: etiquetar no es podar.
  d21.5 C   `ka-` es atributivo, vive en su tabla y el prompt dice «hay sal».
            La reagrupación NO mueve el desafijador.
  d21.6 B   `-ana` se enseña sin glosa, con la fórmula de `-ubana`/`-uru`.
  d21.8 A   `-kana` baja a reconstruido y deja de enseñar a pluralizar wayuu.
  d21.9 A   `-naiki` está retirado.
  d21.10 A  `kudanga` y `kuté` se enseñan como REGISTRO FORMAL.
  d21.13 B  el no-poseído `u-` existe, se enseña Y se reconoce.
  d21.14    `-bakoa` es el lema fonémico de D5, `-uto` está declarado como
            variante y ninguna regla presenta un derivado que el lexicón no
            tenga.
  d21.15    `coro` es 'espina' con la fuente de González Batista.
  d21.16    las cinco glosas.

Lo que NO se fija aquí porque no es código: d21.3 (la trampa de la saturación,
que va a la tabla de CLAUDE.md), d21.7 (la campaña de `-gua`), d21.11 C y
d21.12 (que se declaran en `2-lengua/morfologia.md`).
"""
import curiana_lexicon as lx
from curiana_lexicon import (
    AFIJOS_ATESTIGUADOS,
    CATS_VERBALES,
    FUERA_DEL_HABLA,
    LexicoComunitario,
    REGLAS_ATRIBUTIVAS,
    REGLAS_NUMERO,
    REGLAS_POSESIVAS,
    REGLAS_RETIRADAS,
    TODAS_LAS_REGLAS,
    VOCABULARIO_BASE,
    nucleo_de_token,
    prompt_reglas_breve,
    prompt_reglas_completo,
    score_linguistico,
)

# Los cinco derivados que las reglas presentaban y el lexicón no tiene
# (auditoría §2, «deuda documental de las tablas»).
DERIVADOS_FANTASMA = ("Judibana", "Corogua", "adabacoa", "yacarebacoa",
                      "wayuukana")


def _plantillas() -> list[str]:
    return [lx.IDENTIDAD_LINGUISTICA, prompt_reglas_completo(),
            prompt_reglas_breve()]


def _aspectos(texto: str) -> list:
    limpio = lx._normalizar(texto)
    return lx._aspectos_morfologicos(lx._tokenizar(limpio))


def _score(texto: str) -> dict:
    return score_linguistico(texto, LexicoComunitario())


# ══════════════════════════════════════════════════════════════════════
# d21.1 — el comodín de longitud («Si vamos con C»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_1_el_aspecto_exige_verbo_debajo():
    """20.165 de 62.347 detecciones entraban sin verbo ninguno."""
    assert _aspectos("naa-ka") == ["completivo"]
    assert _aspectos("chaa-ni") == ["continuativo"]
    # Sustantivo + sufijo de aspecto: tres letras y un guion, cero verbo.
    assert _aspectos("hamaka-ni") == []
    assert _aspectos("barsure-da") == []
    assert _aspectos("baro-ni") == []


def test_d21_1_el_compuesto_con_verbo_dentro_sigue_contando():
    """El caso legítimo que el comodín cubría a ciegas: la opción C lo
    conserva y la A lo habría tirado."""
    assert _aspectos("ta-hamaka-chaa-ni") == ["continuativo"]
    assert _aspectos("kali-barsure-masa-ka") == ["completivo"]


def test_d21_1_el_aspecto_apilado_solo_cuenta_una_vez():
    """Consecuencia declarada: en `chaa-ni-da` el segundo sufijo va sobre el
    primero, no sobre un verbo. El apilamiento es gramática emergente (d21.12)
    y se describe en morfologia.md; no se premia en el score."""
    assert _aspectos("chaa-ni-da") == []
    assert _aspectos("chaa-ni chaa-da") == ["continuativo", "prospectivo"]


# ══════════════════════════════════════════════════════════════════════
# d21.2 — `_RAICES_VERB` mezcla las cinco lenguas («Si, A»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_2_la_tabla_entera_sigue_mezclando_lenguas():
    """No se toca `_RAICES_VERB`: es también quien resuelve
    `word_uses.source_language` y una clave lokono tiene que seguir
    devolviendo lokono. Lo que cambia es QUIÉN la mira."""
    from curiana_database import normalize_source_language as N
    lenguas = {N(VOCABULARIO_BASE[k].get("fuente", "")) for k in lx._RAICES_VERB}
    assert len(lenguas) > 1, "la tabla entera debería seguir teniendo comparanda"
    assert "caquetío" in lenguas


def test_d21_2_la_puerta_del_aspecto_y_la_densidad_solo_miran_la_caquetia():
    from curiana_database import normalize_source_language as N
    caq = lx.raices_verbales_caquetias()
    assert caq, "no puede quedar vacía"
    assert caq <= set(lx._RAICES_VERB)
    assert len(caq) < len(lx._RAICES_VERB), (
        "si fueran iguales, el filtro de d21.2 no estaría puesto")
    for k in caq:
        assert N(VOCABULARIO_BASE[k].get("fuente", "")) == "caquetío", k


def test_d21_2_una_raiz_verbal_ajena_ya_no_da_densidad_ni_aspecto():
    """`es_arahuaco()` devolvía True para cualquier token cuyo primer segmento
    estuviera en la tabla entera: el andamio de la reconstrucción daba
    densidad arahuaca."""
    ajenas = sorted(set(lx._RAICES_VERB) - set(lx.raices_verbales_caquetias()))
    assert ajenas, "hacen falta raíces verbales de la comparanda para el test"
    raiz = ajenas[0]
    assert _aspectos(f"{raiz}-ni") == []
    r = _score(f"taya {raiz}-ni yama")
    assert f"{raiz}-ni" not in r["palabras_caquetias"]


# ══════════════════════════════════════════════════════════════════════
# d21.4 — la clase estativa («Vale vamos con la B entonces»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_4_las_diez_estativas_llevan_su_etiqueta():
    from lexicon_zavala import CLASES_DE_RAIZ_ZAVALA
    estativas = [f for f, fila in CLASES_DE_RAIZ_ZAVALA.items()
                 if fila["clase"] == "estativo"]
    assert len(estativas) == 10, estativas
    for f in estativas:
        assert VOCABULARIO_BASE[f]["cat"] == "v_estativo", f


def test_d21_4_etiquetar_no_es_podar():
    """`v_estativo` cuenta como verbal: las diez siguen en `_RAICES_VERB` y
    toman los mismos tres aspectos. Si esto se rompe, declarar la clase habría
    vaciado diez raíces del paradigma, que es lo contrario de la decisión."""
    assert "v_estativo" in CATS_VERBALES and "v_raiz" in CATS_VERBALES
    for forma in ("usera", "waranao", "wasima", "apo"):
        assert forma in lx._RAICES_VERB, forma
        assert forma in lx.raices_verbales_caquetias(), forma
        assert _aspectos(f"{forma}-ni") == ["continuativo"], forma
        assert _aspectos(f"{forma}-ka") == ["completivo"], forma


def test_d21_4_la_etiqueta_llega_al_prompt():
    """«La etiqueta LLEGA AL PROMPT» es media decisión."""
    completo, breve = prompt_reglas_completo(), prompt_reglas_breve()
    assert "ESTADO" in completo or "ESTADO" in breve
    for p in (completo, breve):
        assert "estado" in p.lower()
    assert "UN ESTADO ES UN VERBO" in completo
    # Sin pronombre pospuesto: la opción C (el alineamiento lokono) quedó
    # descartada por no tener ni un dato caquetío detrás.
    for p in (completo, breve):
        assert "pospuesto" not in p.lower()


# ══════════════════════════════════════════════════════════════════════
# d21.5 — `ka-` es atributivo («Vamos con la C»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_5_ka_y_ma_viven_en_su_propia_tabla():
    assert set(REGLAS_ATRIBUTIVAS) == {"ka-", "ma-"}
    assert "ka-" not in REGLAS_POSESIVAS and "ma-" not in REGLAS_POSESIVAS
    assert "atributivo" in REGLAS_ATRIBUTIVAS["ka-"]["nombre"]
    assert "privativo" in REGLAS_ATRIBUTIVAS["ma-"]["nombre"]
    # Regla 8: la afirmación nueva viene con su cita.
    assert "van Buurt" in REGLAS_ATRIBUTIVAS["ka-"]["atestiguado"]
    assert "Perea" in REGLAS_ATRIBUTIVAS["ma-"]["atestiguado"]


def test_d21_5_cambia_la_agrupacion_no_las_claves():
    """«Cambia la AGRUPACIÓN, no las claves, así que el desafijador no se
    mueve». Los dos afijos siguen en la tabla maestra y en los prefijos."""
    assert "ka-" in TODAS_LAS_REGLAS and "ma-" in TODAS_LAS_REGLAS
    assert "ka-" in lx._PREFIJOS_CAQ and "ma-" in lx._PREFIJOS_CAQ
    for tok, nucleo in (("ka-biro", ["biro"]), ("ma-barsure", ["barsure"]),
                        ("ka-biro-ana", ["biro"]), ("ma-arua-bana", ["arua"])):
        assert nucleo_de_token(tok) == nucleo, tok


def test_d21_5_el_prompt_deja_de_decir_el_salinero():
    """`ka-biro` se enseñaba como 'el salinero' —una persona— cuando en van
    Buurt §8 sería 'hay sal'."""
    completo = prompt_reglas_completo()
    assert "salinero" not in completo
    assert "hay sal" in completo
    assert "el/la del" not in completo
    assert "el-la del" not in prompt_reglas_breve()


# ══════════════════════════════════════════════════════════════════════
# d21.6 — `-ana` sin glosa («Me parece🫡 la B»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_6_ninguna_plantilla_dice_ya_que_ana_es_lugar_de():
    """#109 retiró la glosa el 2026-09-07 y las dos plantillas siguieron
    enseñándola dos semanas: el patrón exacto de `kali-bana`."""
    for p in (prompt_reglas_completo(), prompt_reglas_breve()):
        assert "-ana (lugar de)" not in p
        assert "-ana = lugar de" not in p
    assert "-ana" in prompt_reglas_completo()
    assert "-ana" in prompt_reglas_breve()


def test_d21_6_se_ensena_con_la_formula_de_las_desinencias_sin_valor():
    completo = prompt_reglas_completo()
    # Desde la tanda de la base (dc.2 C) `-wa` comparte la línea con `-ana`.
    assert "-wa y -ana = desinencias atestiguadas cuyo valor nadie anotó" in completo
    assert "propones su valor entre corchetes" in completo
    assert "no precisado" in lx.REGLAS_LOCATIVAS["-ana"]["nombre"]


# ══════════════════════════════════════════════════════════════════════
# d21.8 — `-kana` no es cognado directo («Por lo que me parece. A.»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_8_la_regla_deja_de_afirmar_el_cognado_directo():
    kana = REGLAS_NUMERO["-kana"]
    assert "COGNADO DIRECTO" not in kana["wayunaiki"]
    assert "RECONSTRUIDO DESDE EL WAYUNAIKI" in kana["wayunaiki"]
    assert "sin-procedencia" in kana["deuda"]
    assert "D11" in kana["deuda"]


def test_d21_8_los_ejemplos_pluralizan_en_caquetio():
    """La regla enseñaba a formar el plural de una palabra WAYUU y de una
    forma ARCHIVADA, con la lengua que la identidad declara «tan ajena para ti
    como el español»."""
    ejemplos = " ".join(REGLAS_NUMERO["-kana"]["ejemplos"])
    assert "wayuu" not in ejemplos.lower()
    assert "piache" not in ejemplos.lower()
    for raiz in ("barsure", "wanü", "boratio"):
        assert raiz in ejemplos, raiz
        assert raiz in VOCABULARIO_BASE, raiz


# ══════════════════════════════════════════════════════════════════════
# d21.9 — `-naiki` se retira («Si, A.»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_9_naiki_esta_retirado():
    assert "-naiki" in REGLAS_RETIRADAS
    assert "-naiki" not in TODAS_LAS_REGLAS
    assert "-naiki" not in REGLAS_NUMERO
    assert "-naiki" not in lx._SUFIJOS_CAQ
    assert REGLAS_RETIRADAS["-naiki"]["retirada"].startswith("2026-09-21")
    for p in _plantillas():
        assert "-naiki" not in p


# ══════════════════════════════════════════════════════════════════════
# d21.10 — `kudanga` y `kuté` («Vamos con tu propuesta»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_10_los_dos_pronombres_atestiguados_se_ensenan():
    completo = prompt_reglas_completo()
    for forma in ("kudanga", "kuté"):
        assert forma in completo, forma
        assert VOCABULARIO_BASE[forma]["fuente"] == "caquetío-atestiguado"
        assert "Zavala" in VOCABULARIO_BASE[forma]["notas"]
    assert "FORMAL" in completo
    # `pia` no compite con `kudanga`: se reparten registros. El caso barato de
    # la política d19.b — aquí no se archiva nada.
    assert "pia (tú)" in completo
    assert "pia" not in FUERA_DEL_HABLA and "kudanga" not in FUERA_DEL_HABLA


# ══════════════════════════════════════════════════════════════════════
# d21.13 — el no-poseído («Vale, B»)
# ══════════════════════════════════════════════════════════════════════
def test_d21_13_el_no_poseido_es_una_regla_declarada_con_su_cita():
    u = REGLAS_POSESIVAS["u-"]
    assert "no-poseído" in u["nombre"]
    assert "Perea y Alonso 1942 p. 587" in u["atestiguado"]
    assert "u-si-kua-hù" in u["atestiguado"]
    assert "lokono" in u["capa"]
    assert "u-" in lx._PREFIJOS_CAQ


def test_d21_13_se_ensena_y_TAMBIEN_se_reconoce():
    """La patología de `-uto` es enseñar lo que el motor no cuenta. El
    no-poseído entra por las dos puertas o no entra."""
    assert "u- = la cosa SIN DUEÑO" in prompt_reglas_completo()
    assert "u- (la cosa sin dueño)" in prompt_reglas_breve()
    assert nucleo_de_token("u-biro") == ["biro"]
    r = _score("taya wana-ka u-biro yama")
    assert "u-biro" in r["palabras_arahuacas"]


def test_d21_13_el_genero_y_el_numero_de_los_irracionales_NO_se_importan():
    """«El género es lo que la regla 4 prohíbe importar sin marcarlo, y el
    proyecto acaba de pasar por eso con -ko/-sha»."""
    texto = " ".join(
        str(r.get("nombre", "")) + str(r.get("desc", ""))
        for r in TODAS_LAS_REGLAS.values()).lower()
    assert "varonil" not in texto
    for p in _plantillas():
        assert "varonil" not in p.lower()


# ══════════════════════════════════════════════════════════════════════
# d21.14 — D5 en la morfología («Vale, B..» + A en el mismo corte)
# ══════════════════════════════════════════════════════════════════════
def test_d21_14_la_clave_es_el_lema_fonemico():
    """D5 (2026-08-31): la grafía española es grafía, el lema fonémico es la
    palabra. `bakoa` es voz atestiguada del lexicón; `bacoa` no existía."""
    assert "-bakoa" in TODAS_LAS_REGLAS and "-bacoa" not in TODAS_LAS_REGLAS
    assert "-bakoa" in lx._SUFIJOS_CAQ and "-bacoa" not in lx._SUFIJOS_CAQ
    assert "bakoa" in VOCABULARIO_BASE
    assert lx.REGLAS_TOPONIMICAS["-bakoa"]["forma_fuente"] == "-bacoa"
    assert set(AFIJOS_ATESTIGUADOS) == set(lx.REGLAS_ZAVALA) | {"-bakoa"}
    assert nucleo_de_token("kuru-bakoa") == ["kuru"]


def test_d21_14_uto_esta_declarado_como_variante():
    # `-uco` vivía en REGLAS_ZAVALA; desde el 2026-09-23 (cc.4 / tf.0, 4-a)
    # está en REGLAS_ESTEVES —su única fuente es la (E) de Zavala, que es
    # Esteves— con las mismas claves, la misma variante y el mismo residuo.
    assert "-uco" not in lx.REGLAS_ZAVALA
    uco = lx.REGLAS_ESTEVES["-uco"]
    assert uco["variantes"] == ["-uto"]
    assert "no es clave" in uco["variantes_nota"].lower()
    # Residuo declarado: se sigue enseñando y sigue sin reconocerse.
    assert "-uto" in prompt_reglas_completo()
    assert "-uto" not in TODAS_LAS_REGLAS


def test_d21_14_ninguna_regla_presenta_un_derivado_que_el_lexicon_no_tiene():
    ejemplos = " ".join(
        " ".join(r.get("ejemplos") or []) + str(r.get("uso", ""))
        + str(r.get("instruccion_agente", ""))
        for r in TODAS_LAS_REGLAS.values())
    for fantasma in DERIVADOS_FANTASMA:
        assert fantasma not in ejemplos, fantasma
    for p in _plantillas():
        for fantasma in DERIVADOS_FANTASMA:
            assert fantasma not in p, fantasma


# ══════════════════════════════════════════════════════════════════════
# d21.15 — `coro` es 'espina'
# ══════════════════════════════════════════════════════════════════════
def test_d21_15_coro_cambia_la_glosa_inventada_por_la_que_tiene_fuente():
    coro = VOCABULARIO_BASE["coro"]
    assert coro["sig"] == "espina"
    assert "cardón grande, cactus columnar" not in coro["sig"]
    assert "González Batista" in coro["notas"]
    assert "gonzalez-batista-nombre-de-coro" in coro["notas"]
    # «Cardón» queda como lo que la propia fuente dice que es: una
    # consecuencia INDIRECTA, no la glosa.
    assert "INDIRECTAMENTE" in coro["notas"]
    # Lectura en disputa, declarada con su rival.
    assert "Arcaya" in coro["lectura_en_disputa"]
    # Hasta el 2026-09-23 la disputa tenía TRES lecturas y la tercera era
    # 'viento' (Castellanos 1589). cc.6 / tf.6 la DESCARTÓ: es el juego culto
    # de Castellanos sobre el latín cōrus/caurus, no una glosa indígena
    # (BAE p. 185; Arcaya 1920 p. 170). Sale de `lectura_en_disputa` y queda
    # archivada en `notas` con su porqué — archivar no es borrar.
    assert "Castellanos" not in coro["lectura_en_disputa"]
    assert "'viento'" not in coro["lectura_en_disputa"]
    assert "DESCARTADA 2026-09-23" in coro["notas"]


def test_d21_15_kadushi_no_se_toca():
    assert "kadushi" in VOCABULARIO_BASE
    assert "cactus" in VOCABULARIO_BASE["kadushi"]["sig"].lower() or \
           "cardón" in VOCABULARIO_BASE["kadushi"]["sig"].lower()


# ══════════════════════════════════════════════════════════════════════
# d21.16 — las cinco glosas
# ══════════════════════════════════════════════════════════════════════
def test_d21_16_chaa_pierde_crear():
    """Emparejaba con `eroa` «empezar, crear, originar», que es atestiguada, y
    no son lo mismo: uno construye, el otro origina."""
    assert VOCABULARIO_BASE["chaa"]["sig"] == "hacer, construir"
    assert "crear" not in VOCABULARIO_BASE["chaa"]["sig"]


def test_d21_16_apana_es_una_medida_de_tiempo_y_no_un_mes():
    """«Llamarlo mes proyectaría el calendario europeo» (regla 3)."""
    apana = VOCABULARIO_BASE["apana"]
    assert apana["sig"].startswith("medida de tiempo")
    assert "luna" in apana["sig"]
    assert "mes" not in apana["sig"].lower()


def test_d21_16_bara_y_kuru_declaran_su_convivencia():
    for clave, gemela in (("bara", "kuru"), ("kuru", "bara")):
        notas = VOCABULARIO_BASE[clave]["notas"]
        assert "CONVIVENCIA DECLARADA" in notas, clave
        assert gemela in notas, clave
    assert VOCABULARIO_BASE["bara"]["sig"] != VOCABULARIO_BASE["kuru"]["sig"]


def test_d21_16_sima_y_turumako_dejan_de_emparejar():
    sima, turu = VOCABULARIO_BASE["sima"], VOCABULARIO_BASE["turumako"]
    assert "CONVIVENCIA DECLARADA" in sima["notas"]
    assert "turumako" in sima["notas"]
    assert sima["sig"] != turu["sig"]
    assert "montaña" not in sima["sig"]
    assert "cima plana" in turu["sig"]
    # La glosa de la FUENTE no se toca jamás.
    assert turu["glosa_fuente"].startswith("Cerro, meseta")


# ══════════════════════════════════════════════════════════════════════
# LA LÍNEA ROJA DE TODA LA TANDA
# ══════════════════════════════════════════════════════════════════════
def test_la_linea_roja_capas_de_score_sigue_fija():
    """«El scorer se toca aquí a propósito y con medición […] pero
    `capas_de_score` sigue fijo y `curiana_observer` no se modifica»."""
    from curiana_perfiles import cargar_perfil, nombres
    capas = {n: tuple(sorted(cargar_perfil(n).capas_de_score))
             for n in nombres()}
    assert len(capas) > 1 and len(set(capas.values())) == 1, capas
