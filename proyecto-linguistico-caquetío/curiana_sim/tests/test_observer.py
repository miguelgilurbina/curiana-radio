"""Tests del Observer: análisis local y detección de adopciones con
frontera de palabra (curiana_observer.py). Sin llamadas LLM."""

from curiana_lexicon import LexicoComunitario, extraer_neologismos_del_texto
from curiana_observer import ObserverAgent


def _observer():
    """ObserverAgent sin cliente Anthropic (solo análisis local)."""
    lex = LexicoComunitario()
    obs = ObserverAgent.__new__(ObserverAgent)
    obs.client = None
    obs.lexico = lex
    obs._historial = []
    obs._scores_por_agente = {}
    return obs, lex


def _proponer(lex, forma, autor="Manaure"):
    neos = extraer_neologismos_del_texto(
        f"[{forma}: kali+ni = luz continua]", autor, dia=1, turno=1)
    assert neos, f"el neologismo de test '{forma}' no pasó la compuerta"
    lex.registrar_neologismo(neos[0])


def test_adopcion_exige_frontera_de_palabra():
    """'kali-ni' NO debe adoptarse desde 'kali-nima' (bug de substring)."""
    obs, lex = _observer()
    _proponer(lex, "kali-ni")
    obs.procesar_adopciones("Taya wana-ka kali-nima wara.", "Shaboro", turno=1, dia=2)
    obs.procesar_adopciones("Nüma maa-ni kali-nima.", "Tawaka", turno=2, dia=2)
    assert lex.neologismos_adoptados() == []


def test_adopcion_con_uso_exacto():
    obs, lex = _observer()
    _proponer(lex, "kali-ni")
    assert obs.procesar_adopciones("Taya wana-ka kali-ni.", "Shaboro", turno=1, dia=2) == []
    oficializados = obs.procesar_adopciones(
        "Kali-ni wara, naa-da yama.", "Tawaka", turno=2, dia=3)
    assert len(oficializados) == 1
    assert oficializados[0].forma == "kali-ni"
    assert oficializados[0].dia_resolucion == 3


def test_autor_no_se_adopta_a_si_mismo():
    obs, lex = _observer()
    _proponer(lex, "kali-ni", autor="Manaure")
    obs.procesar_adopciones("Kali-ni wara.", "Manaure", turno=1, dia=2)
    neo = lex.neologismos_pendientes()[0]
    assert neo.adoptado_por == []


def test_analizar_alimenta_historial_y_scores():
    obs, _ = _observer()
    r = obs.analizar("Shaboro", "caquetío", 1,
                     "Taya wana-ka arima wara bara-bana. Ta-barsure naba-ni.",
                     dia=1, turno=1, momento="amanecer", estacion="seca")
    assert r.score > 0
    assert obs.score_promedio("Shaboro") == r.score
    assert len(obs._historial) == 1
