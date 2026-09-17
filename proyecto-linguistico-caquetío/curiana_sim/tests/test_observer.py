"""Tests del Observer: análisis local y detección de adopciones con
frontera de palabra (curiana_observer.py). Sin llamadas LLM."""

from curiana_lexicon import LexicoComunitario, extraer_neologismos_del_texto
from curiana_observer import ObserverAgent, RegistroInteraccion


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


def test_el_registro_conserva_los_prestamos_de_esfera_y_sobrevive_al_json(tmp_path):
    """Run c6837386 (2026-09-16): el préstamo de esfera se medía y se perdía.
    El registro lo conserva aparte de `palabras_caquetias`, y el modo JSON
    (sin Supabase) lo escribe, lo vuelve a leer, y carga igual un JSON viejo
    que no traiga el campo.

    ⚠ 2026-09-17: el ejemplo era `caiman`, castellano corriente y desde hoy
    `HISPANISMOS_DE_ESFERA`. Se usa `watapana`, que el castellano no dice
    —dice dividivi—: un préstamo de verdad. El test fija lo mismo."""
    obs, lex = _observer()
    r = obs.analizar("Manaure", "caquetío", 1, "Taya wana-ka watapana wara.",
                     dia=2, turno=1, momento="amanecer", estacion="seca")
    assert r.prestamos_de_esfera == ["watapana"]
    assert "watapana" not in r.palabras_caquetias
    assert r.to_csv_row()["prestamos_esfera"] == "watapana"

    ruta = str(tmp_path / "observer.json")
    obs.save(ruta)
    cargado = ObserverAgent.load(None, lex, ruta)
    assert cargado._historial[0].prestamos_de_esfera == ["watapana"]

    viejo = {k: v for k, v in r.to_dict().items()
             if k not in ("prestamos_de_esfera", "neologismos_extraidos")}
    assert RegistroInteraccion(**viejo).prestamos_de_esfera == []
    assert len(obs._historial) == 1
