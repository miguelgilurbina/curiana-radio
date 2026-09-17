"""Tests de difusión léxica y variación dialectal (curiana_social.py).

Y, desde el 2026-09-17, de las dos puertas del grafo social: `prestigio_de()` y
`vinculos_de()`. `PRESTIGIO` y `VINCULOS` están indexados por los nombres de la
ERA 1 y la campaña de antropónimos renombró a 60 de 63 agentes: de 63 sólo una
clave estaba viva (Manaure) y los tres destinos de sus vínculos no existían en
el elenco. Mismo agujero que DISENO_KOINE §4 cerró para `FORMAS_SEED`.

La era 1 tiene que quedar BYTE A BYTE: aquí se recalcula con la fórmula vieja
(`_prestigio_como_antes`, `_vecinos_como_antes`) y se compara la tabla entera.
La era 2 se mide en un subproceso, como en test_koine.py: el elenco se decide
al importar curiana_agents, desde CURIANA_ELENCO.
"""

import json
import os
import subprocess
import sys

import pytest

from curiana_agents import ALL_AGENTS, agents_at_location, get_agent
from curiana_social import (
    DifusionLexica,
    PESO_COUBICACION,
    PRESTIGIO,
    VINCULOS,
    _PRESTIGIO_ETNIA_FORANEA,
    _PRESTIGIO_TIER,
    _limpiar_cache,
    normalizar_por_dialecto,
    prestigio_de,
    prestigio_derivado,
    vecinos,
    vinculos_de,
    vinculos_derivados,
)


def test_prestigio_explicito_y_derivado():
    assert prestigio_de("Manaure") == 1.0
    assert 0.0 < prestigio_de("Marokoto-ni") < prestigio_de("Manaure")


def test_contagio_prestigioso_cruza_umbral_en_un_uso():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")   # prestigio 1.0, vínculo 0.95 con Buio-sha
    assert d.exposicion_de("Buio-sha", "sima-bana") >= d.umbral
    assert any(f == "sima-bana" for f, _ in d.sugerencias_para("Buio-sha"))


def test_no_se_sugiere_lo_ya_usado():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")
    d.propagar_uso("sima-bana", "Buio-sha")  # Buio-sha ya la usó
    assert d.sugerencias_para("Buio-sha") == []


def test_periferico_sin_vinculo_no_adopta():
    d = DifusionLexica()
    d.propagar_uso("sima-bana", "Shaboro")
    assert d.sugerencias_para("Marokoto-ni") == []


def test_normalizacion_dialectal_favorece_l2():
    assert normalizar_por_dialecto(4.5, "caribe") > normalizar_por_dialecto(4.5, "caquetío")
    assert normalizar_por_dialecto(9.9, "caribe") <= 10.0   # acotado


# ══════════════════════════════════════════════════════════════════════
# LA ERA 1, BYTE A BYTE
# ══════════════════════════════════════════════════════════════════════
# La fórmula de antes del 2026-09-17, recalculada aquí para comparar la tabla
# ENTERA. Si alguna de las dos puertas mueve un solo valor en la era 1, estos
# tests lo cazan: `score`, `pct_*` y la comparabilidad con los runs publicados
# cuelgan del contagio, y el contagio cuelga de aquí.

def _prestigio_como_antes(agente: str) -> float:
    if agente in PRESTIGIO:
        return PRESTIGIO[agente]
    info = get_agent(agente)
    etnia = info.get("etnia")
    if etnia in _PRESTIGIO_ETNIA_FORANEA:
        return _PRESTIGIO_ETNIA_FORANEA[etnia]
    return _PRESTIGIO_TIER.get(info.get("tier"), 0.2)


def _vecinos_como_antes(agente: str, state=None) -> dict:
    red = dict(VINCULOS.get(agente, {}))
    for otro, destinos in VINCULOS.items():
        if agente in destinos:
            red[otro] = max(red.get(otro, 0.0), destinos[agente])
    info = get_agent(agente)
    ubic = None
    if state is not None:
        ubic = getattr(state, "ubicaciones_override", {}).get(agente)
    if ubic is None:
        ubic = info.get("ubicacion_default")
    if ubic:
        presentes = set(agents_at_location(ubic))
        if state is not None:
            for ag, ub in getattr(state, "ubicaciones_override", {}).items():
                if ub == ubic:
                    presentes.add(ag)
                else:
                    presentes.discard(ag)
        for otro in sorted(presentes):
            if otro != agente:
                red[otro] = max(red.get(otro, 0.0), PESO_COUBICACION)
    return red


class _EstadoFalso:
    def __init__(self, overrides):
        self.ubicaciones_override = overrides


def test_la_era_1_no_cambia_byte_a_byte():
    """El alias y la derivación no tocan la era 1: allí `ALIAS_ERA1` está vacío
    (resolver es la identidad) y la derivación exige `rol_en_la_casa`, campo que
    sólo trae el módulo generado de la era 2."""
    import curiana_agents as A

    assert A.ELENCO == "era1" and A.ALIAS_ERA1 == {} and A.SITIOS == {}
    _limpiar_cache()      # el grafo se compara recién construido, no cacheado
    for agente in ALL_AGENTS:
        assert prestigio_de(agente) == _prestigio_como_antes(agente), agente
        assert prestigio_derivado(agente) is None, agente
        assert vinculos_derivados(agente) == {}, agente
        assert vinculos_de(agente) == dict(VINCULOS.get(agente, {})), agente
        assert vecinos(agente) == _vecinos_como_antes(agente), agente


def test_la_era_1_no_cambia_tampoco_con_el_estado_moviendo_gente():
    """La co-ubicación dinámica es la otra mitad de `vecinos()`: se comprueba
    con un estado que mueve a medio elenco a una sola ubicación."""
    destinos = sorted({(a.get("ubicacion_default") or "") for a in ALL_AGENTS.values()} - {""})
    overrides = {nombre: destinos[i % len(destinos)]
                 for i, nombre in enumerate(sorted(ALL_AGENTS))}
    estado = _EstadoFalso(overrides)
    for agente in ALL_AGENTS:
        assert vecinos(agente, estado) == _vecinos_como_antes(agente, estado), agente


# ══════════════════════════════════════════════════════════════════════
# LA ERA 2 (2026-09-17)
# ══════════════════════════════════════════════════════════════════════

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_CODIGO_ERA2 = """
import json
import curiana_agents as A
import curiana_social as S

nodo_de_sitio = {s: d.get('nodo') for s, d in A.SITIOS.items()}
salida = S.medicion()
salida['por_agente'] = {
    n: {'prestigio': S.prestigio_de(n),
        'derivado': S.prestigio_derivado(n),
        'papel': (S.papel_de(n) or (None, None, None))[1],
        'tier': a.get('tier'),
        'nodo': a.get('nodo'),
        'en_roster': bool(a.get('en_roster')),
        'origen': S.sitio_de_origen(n),
        'nodo_de_origen': nodo_de_sitio.get(S.sitio_de_origen(n)),
        'vinculos': S.vinculos_de(n),
        'vecinos': S.vecinos(n)}
    for n, a in A.ALL_AGENTS.items()}
salida['nodo_de_agente'] = {n: a.get('nodo') for n, a in A.ALL_AGENTS.items()}
salida['nodo_de_sitio'] = nodo_de_sitio
salida['alias'] = {n: (S.nombre_era1(n) or n) for n in A.ALL_AGENTS}
print(json.dumps(salida, ensure_ascii=False, default=str))
"""


def _medir_era2() -> dict:
    env = dict(os.environ, CURIANA_ELENCO="era2", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-c", _CODIGO_ERA2], cwd=SIM, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.fixture(scope="module")
def era2():
    return _medir_era2()


def test_los_63_tienen_prestigio_propio_y_no_es_el_tier_con_otro_nombre(era2):
    """Antes: `1.0 ×1 · 0.5 ×16 · 0.4 ×36 · 0.2 ×10` — tres valores que son los
    tres tiers, más Manaure. Ahora cada agente lo saca de SU ficha y ningún
    agente cae al default por tier."""
    assert era2["mundo"] == "PARAGUANÁ" and era2["agentes"] == 63
    assert era2["prestigio_por_tier_solo"] == []
    assert len(era2["prestigio_derivado"]) == 63
    for nombre, d in era2["por_agente"].items():
        assert d["papel"], f"{nombre} no casa ningún papel declarado"
        assert 0.0 < d["prestigio"] <= 1.0, nombre

    dist = era2["prestigio_distribucion"]
    assert len(dist) >= 8, dist
    # y dentro de un mismo tier hay varios valores (si fuera el tier, sería uno)
    por_tier = era2["prestigio_valores_por_tier"]
    assert all(len(v) > 1 for v in por_tier.values()), por_tier


def test_las_seis_entradas_escritas_que_sobreviven_valen_lo_mismo_que_en_la_era_1(era2):
    """Manaure conserva su nombre; los otros cinco recuperan su valor por
    `ALIAS_ERA1` (Shaboro → Sawaka, Nubiri-sha → Karebe, Paugis-sha → Paugis,
    Buio-sha → Hayo, Bana-mana → Turicha). Lo escrito manda sobre lo derivado."""
    assert era2["prestigio_claves_vivas"] == 1
    por_alias = era2["prestigio_por_alias"]
    assert len(por_alias) == 5, por_alias
    assert era2["por_agente"]["Manaure"]["prestigio"] == PRESTIGIO["Manaure"]
    for nuevo in por_alias:
        viejo = era2["alias"][nuevo]
        assert era2["por_agente"][nuevo]["prestigio"] == PRESTIGIO[viejo], nuevo


def test_ningun_vinculo_apunta_ya_a_un_agente_que_no_existe(era2):
    """Antes: 3 aristas a fantasmas (los tres destinos de Manaure) y un agente
    —Sawaka, solo en el Capubana— sin ninguna arista."""
    assert era2["aristas_a_inexistentes"] == 0
    assert era2["agentes_sin_aristas"] == []
    vivos = set(era2["por_agente"])
    for nombre, d in era2["por_agente"].items():
        assert set(d["vinculos"]) <= vivos, nombre
        assert nombre not in d["vinculos"] and nombre not in d["vecinos"], nombre


def test_las_aristas_intra_y_entre_nodos_estan_medidas(era2):
    """Antes: intra 708 · entre 0 · fantasmas 3. El grafo social era la única
    frontera del motor y estaba cerrada al 100 % por accidente
    (6-fusion/issues-pendientes/frontera-entre-nodos-2026-09-17.md §1.2)."""
    intra, entre = era2["aristas_intra_nodo"], era2["aristas_entre_nodos"]
    assert intra > 0 and entre > 0, (intra, entre)
    # recontado desde el detalle, no desde el resumen
    nodo = era2["nodo_de_agente"]
    recuento = [0, 0]
    for nombre, d in era2["por_agente"].items():
        for otro in d["vecinos"]:
            recuento[nodo[nombre] != nodo[otro]] += 1
    assert recuento == [intra, entre]


def test_los_que_cruzaron_tienen_vinculo_con_su_nodo_de_origen(era2):
    """El elenco declara 18 agentes traídos de otro sitio; 10 de ellos cruzaron
    la frontera entre nodos y 6 están en el roster. El canon les escribió el
    vínculo con su casa de origen: aquí tiene que existir."""
    assert len(era2["con_sitio_de_origen"]) == 18
    assert len(era2["cruzan_de_nodo"]) == 10
    assert len(era2["cruzan_de_nodo_en_roster"]) == 6
    nodo = era2["nodo_de_agente"]
    for nombre in era2["cruzan_de_nodo"]:
        d = era2["por_agente"][nombre]
        origen = d["nodo_de_origen"]
        assert origen and origen != d["nodo"]
        alla = [o for o in d["vinculos"] if nodo[o] == origen]
        assert alla, f"{nombre} no tiene ningún vínculo en {origen}"


def test_wamipa_tiene_a_su_tio_materno_en_caseto(era2):
    """Wamipa no fue traído de ninguna parte —nació en la casa del Manaure—
    pero su linaje es el de su madre Karebe, que vino de Caseto: el eje
    matrilineal le da un vínculo en AMUAY que ningún otro dato le daría."""
    d = era2["por_agente"]["Wamipa"]
    assert d["origen"] is None and d["nodo"] == "GUARANAO"
    nodo = era2["nodo_de_agente"]
    fuera = [o for o in d["vinculos"] if nodo[o] != d["nodo"]]
    assert fuera, "Wamipa se quedó sin el tío materno de Caseto"
    assert all(era2["por_agente"][o]["nodo"] == "AMUAY" for o in fuera)


def test_el_grafo_de_la_era_2_es_determinista_entre_procesos():
    """No hay `hash()` (salado por proceso con PYTHONHASHSEED) ni RNG global:
    todo sale de la ficha y de un orden declarado. Dos procesos, la misma tabla."""
    a, b = _medir_era2(), _medir_era2()
    assert a["por_agente"] == b["por_agente"]
    assert a["prestigio_distribucion"] == b["prestigio_distribucion"]


def test_la_fijacion_de_la_koine_lee_el_prestigio_por_la_puerta():
    """`CompetenciaLexica` pondera la fijación con el prestigio del proponente
    (`curiana_koine.py`). Si algún día dejara de entrar por `prestigio_de()`,
    la era 2 volvería a fijar formas por el tier."""
    from curiana_koine import CompetenciaLexica

    comp = CompetenciaLexica()
    for agente in ("Manaure", "Shaboro", "Kori", "Marokoto-ni"):
        assert comp._prestigio(agente) == prestigio_de(agente), agente
