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
