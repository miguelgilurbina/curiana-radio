"""Tests del motor léxico: scoring, compuerta de neologismos, extracción
y ciclo de adopción (curiana_lexicon.py)."""

from curiana_lexicon import (
    LexicoComunitario,
    score_linguistico,
    neologismo_valido,
    extraer_neologismos_del_texto,
)


def _lexico():
    return LexicoComunitario()


# ── score_linguistico ─────────────────────────────────────────────────

def test_score_caquetio_supera_espanol():
    lex = _lexico()
    caq = ("Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni. "
           "Ka biro escaso, mara waya naa-da salinar.")
    esp = ("Hoy fui al río muy temprano por la mañana y vi muchos peces. "
           "Mi alma está pensando, pero debemos ir por sal.")
    assert score_linguistico(caq, lex)["score"] > score_linguistico(esp, lex)["score"]


def test_score_glosas_no_penalizan():
    """Lo que va entre paréntesis es glosa: no puntúa ni penaliza."""
    lex = _lexico()
    con_glosa = "Taya wana-ka arima bara-bana. (Vi peces en la orilla del río.)"
    sin_glosa = "Taya wana-ka arima bara-bana."
    assert (score_linguistico(con_glosa, lex)["espanol_funcional"]
            == score_linguistico(sin_glosa, lex)["espanol_funcional"] == 0)


def test_homografo_para_segun_contexto():
    lex = _lexico()
    # rodeada de caquetío → "para" es el mar (léxico caquetío)
    r_caq = score_linguistico("Taya naa-ni para-bana, wana-ka para wara arima.", lex)
    assert "para" in r_caq["palabras_caquetias"]
    # rodeada de español → es la preposición
    r_esp = score_linguistico("Esto es para que vayas mañana temprano.", lex)
    assert "para" not in r_esp["palabras_caquetias"]
    assert r_esp["espanol_funcional"] > 0


# ── neologismo_valido (compuerta anti-español) ────────────────────────

def test_bloquea_ofensores_observados_en_runs():
    for forma in ("suave-bana-ni", "tension-bana-chi", "boca-pana",
                  "carrera-kata", "guardia-bana", "lanza-sara", "temblor-bana"):
        assert not neologismo_valido(forma), forma


def test_acepta_composiciones_caquetias():
    for forma in ("sima-bana", "kali-dusha", "kuru-bana", "arima-ana", "wa-buco"):
        assert neologismo_valido(forma), forma


# ── extraer_neologismos_del_texto ─────────────────────────────────────

def test_extraccion_y_regla_de_afijo_mas_largo():
    texto = "Taya wana-ka [sima-bana: sima+-bana = orilla del cerro]."
    neos = extraer_neologismos_del_texto(texto, "Shaboro", dia=1, turno=1)
    assert len(neos) == 1
    assert neos[0].forma == "sima-bana"
    # "-bana" debe ganar sobre "-ana" (afijo más largo)
    assert neos[0].regla_aplicada == "-bana"


def test_extraccion_descarta_neologismo_espanol():
    texto = "Naba-ni [guardia-bana: guardia+-bana = puesto de vigilancia]."
    assert extraer_neologismos_del_texto(texto, "Tawaka", dia=1, turno=1) == []


# ── ciclo de adopción en LexicoComunitario ────────────────────────────

def _neo(lex, forma="kali-dusha"):
    neos = extraer_neologismos_del_texto(
        f"[{forma}: kali+dusha = estrella con cola]", "Manaure", dia=3, turno=1)
    lex.registrar_neologismo(neos[0])
    return neos[0]


def test_adopcion_requiere_dos_agentes_y_registra_dia():
    lex = _lexico()
    _neo(lex)
    assert lex.adoptar("kali-dusha", "Shaboro", turno=2, dia=4) is None  # 1er adoptante
    oficial = lex.adoptar("kali-dusha", "Tawaka", turno=1, dia=5)        # 2do → oficializa
    assert oficial is not None and oficial.estado == "adoptado"
    assert oficial.dia_resolucion == 5      # día de ADOPCIÓN, no de propuesta
    assert oficial.dia == 3
    assert "kali-dusha" in lex.palabras_activas()


def test_adopcion_repetida_mismo_agente_no_oficializa():
    lex = _lexico()
    _neo(lex)
    assert lex.adoptar("kali-dusha", "Shaboro", turno=1, dia=4) is None
    assert lex.adoptar("kali-dusha", "Shaboro", turno=2, dia=4) is None


# ── word_source_language debe entender morfología ─────────────────────

def test_word_source_language_resuelve_formas_flexionadas():
    """Lo que se guarda en `word_uses.source_language` tiene que reconocer las
    formas con prefijo posesivo y sufijo de aspecto.

    Antes era un lookup pelado contra VOCABULARIO_BASE, así que `wana-ka` o
    `ta-barsure` se guardaban con NULL. Medido sobre la base local el
    2026-08-06: **27.641 de 54.936 usos (50,3%) sin lengua, y el 100% de ellos
    formas morfológicamente complejas** — justo los usos que prueban que los
    agentes manejan la morfología del proyecto.
    """
    from curiana_database import word_source_language

    for forma in ("wana-ka", "naba-ni", "kaa-ni", "ta-barsure", "pi-barsure"):
        assert word_source_language(forma) is not None, (
            f"{forma} debería resolver a una lengua, no a None")


def test_word_source_language_conserva_la_lengua_hermana():
    """Descomponer no puede convertirlo todo en caquetío: una palabra wayunaiki
    o lokono tiene que seguir siendo suya, que es de lo que vive el scoring.

    Se comprueba sobre TODO el lexicón, no sobre una muestra: si una sola
    entrada cambiara de lengua al pasar por aquí, la composición por lengua de
    los runs quedaría falseada.
    """
    from curiana_database import normalize_source_language, word_source_language
    from curiana_lexicon import VOCABULARIO_BASE

    discrepantes = []
    for palabra, entrada in VOCABULARIO_BASE.items():
        esperada = normalize_source_language(entrada.get("fuente", ""))
        obtenida = word_source_language(palabra)
        if obtenida != esperada:
            discrepantes.append((palabra, esperada, obtenida))

    assert not discrepantes, (
        f"{len(discrepantes)} entradas cambian de lengua al resolverse; "
        f"primeras: {discrepantes[:5]}")


def test_word_source_language_vacio_es_none():
    from curiana_database import word_source_language
    assert word_source_language("") is None
