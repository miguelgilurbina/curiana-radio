"""Tests de la huella de la base.

Lo que protegen: que dos runs sobre la misma base den la misma huella, y que
cualquier cambio en lexicón, corpus o elenco la mueva. Si la huella no
discrimina, no sirve para nada — y su único trabajo es decir *contra qué corrió
este run*.
"""

from huella_de_base import _hash_dict, huella, resumen


def test_la_huella_trae_las_cuatro_esferas():
    h = huella()
    for campo in ("lexicon_hash", "corpus_hash", "agentes_hash", "motor_commit"):
        assert campo in h, f"falta {campo}"
    for campo in ("lexicon_n", "corpus_n", "agentes_n"):
        assert isinstance(h[campo], int) and h[campo] > 0


def test_es_estable_entre_llamadas():
    """Dos runs sobre la misma base tienen que dar la misma huella, o no se
    pueden comparar."""
    a, b = huella(), huella()
    for campo in ("lexicon_hash", "corpus_hash", "agentes_hash"):
        assert a[campo] == b[campo], f"{campo} cambia entre llamadas"


def test_el_hash_no_depende_del_orden_de_insercion():
    """Sin `sort_keys`, mover una entrada de sitio en el archivo fuente
    parecería un cambio de contenido."""
    assert _hash_dict({"a": 1, "b": 2}) == _hash_dict({"b": 2, "a": 1})


def test_el_hash_si_cambia_con_el_contenido():
    """Lo contrario del test anterior: si no discrimina, no sirve."""
    assert _hash_dict({"a": 1}) != _hash_dict({"a": 2})


def test_registra_la_polity_simulada():
    """Un run de la costera y uno de Barquisimeto no son comparables, y hoy
    eso no se vería en ningún sitio."""
    assert huella()["polity"] == "costera"


def test_registra_el_tamano_de_los_prompts():
    """La longitud del prompt predice el score (r=-0.48). Si alguien reescribe
    una ficha entre dos runs, los scores cambian sin que nada más cambie."""
    h = huella()
    assert isinstance(h["prompt_chars"], int) and h["prompt_chars"] > 0


def test_la_semilla_solo_aparece_si_se_pasa():
    assert "semilla" not in huella()
    assert huella(semilla=42)["semilla"] == 42


def test_el_resumen_es_una_linea_legible():
    r = resumen(huella())
    assert "\n" not in r
    assert "lexicón" in r and "polity" in r


def test_el_resumen_avisa_del_arbol_sucio():
    sucio = resumen({"motor_sucio": True, "motor_commit": "abc123456"})
    limpio = resumen({"motor_sucio": False, "motor_commit": "abc123456"})
    assert "SUCIO" in sucio
    assert "SUCIO" not in limpio
