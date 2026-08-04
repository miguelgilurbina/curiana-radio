"""Tests del modelo de polities caquetías (curiana_polities.py).

Lo que estos tests protegen no es un cálculo, es una **disciplina**: que ningún
rasgo entre al módulo sin la fuente que lo sostiene, que los huecos sigan
visibles en vez de rellenarse por simetría, y que la separación entre `etnia`
(qué pueblo) y `polity` (qué formación política) no se difumine.

El contraste costera↔barquisimeto se testea explícitamente porque es el que
motivó el módulo: es donde el canon del proyecto tomó prestado sin marcarlo.
"""

import pytest

from curiana_polities import (
    POLITIES,
    POLITY_SIMULADA,
    Polity,
    Rasgo,
    coherencia_del_canon,
    contrastar,
    la_simulada,
    polity,
    prompt_polity,
    validar,
)


# ── el dato ───────────────────────────────────────────────────────────

def test_el_modulo_valida():
    problemas = validar()
    assert not problemas, "problemas de dato:\n" + "\n".join(problemas)


def test_las_cuatro_polities_atestiguadas_estan():
    assert set(POLITIES) == {"costera", "barquisimeto", "yaracuy", "llanos"}


@pytest.mark.parametrize("pid", sorted(POLITIES))
def test_todo_rasgo_lleva_fuente(pid):
    """Un rasgo sin cita es exactamente lo que este proyecto no hace."""
    for eje, rasgo in polity(pid).rasgos().items():
        assert rasgo.fuente.strip(), f"{pid}.{eje} sin fuente"
        assert rasgo.epoca.strip(), f"{pid}.{eje} sin época"


@pytest.mark.parametrize("pid", sorted(POLITIES))
def test_toda_polity_tiene_territorio(pid):
    assert polity(pid).territorio is not None


def test_la_simulada_es_la_costera():
    """Si esto cambia, cambia lo que el motor entero está modelando."""
    assert POLITY_SIMULADA == "costera"
    assert la_simulada().id == "costera"


def test_polity_desconocida_falla_claro():
    with pytest.raises(KeyError, match="conocidas"):
        polity("tierra-media")


# ── los huecos se ven ─────────────────────────────────────────────────

def test_los_huecos_no_se_rellenan():
    """Oliver no describe la religión del Yaracuy. Inventarla sería el error
    que este módulo existe para no cometer."""
    assert "religion" in polity("yaracuy").huecos()
    assert polity("yaracuy").religion is None


def test_rasgos_omite_los_huecos():
    y = polity("yaracuy")
    assert "religion" not in y.rasgos()
    assert len(y.rasgos()) + len(y.huecos()) == len(Polity.EJES)


# ── el contraste ──────────────────────────────────────────────────────

def test_costera_y_barquisimeto_diferen_en_liderazgo():
    dif = contrastar("costera", "barquisimeto")
    assert "liderazgo" in dif
    costera, barq = dif["liderazgo"]
    assert "paramount" in costera.valor
    assert "Jefe de Paz" in barq.valor


def test_el_contraste_marca_el_eje_religioso():
    """La costera funde poder sagrado y secular; Barquisimeto los separa.
    Es el hallazgo del que sale la advertencia sobre Shaboro."""
    dif = contrastar("costera", "barquisimeto")
    assert "religion" in dif
    costera, barq = dif["religion"]
    assert "gran chamán" in costera.valor
    assert "apartado" in barq.valor


def test_contrastar_conserva_los_huecos_como_None():
    """Un eje que solo una documenta aparece, con None en el lado que falta:
    el hueco es información, no algo que ocultar."""
    dif = contrastar("costera", "yaracuy")
    assert "religion" in dif
    costera, yaracuy = dif["religion"]
    assert costera is not None and yaracuy is None


def test_contrastar_consigo_misma_no_da_diferencias():
    assert contrastar("costera", "costera") == {}


def test_contrastar_es_simetrico_en_los_ejes():
    a = contrastar("costera", "llanos")
    b = contrastar("llanos", "costera")
    assert set(a) == set(b)


# ── el prompt ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("pid", sorted(POLITIES))
def test_prompt_polity_menciona_el_nombre(pid):
    p = prompt_polity(pid)
    assert p.startswith("[") and p.endswith("]")
    assert POLITIES[pid].nombre in p


# ── la coherencia del canon ───────────────────────────────────────────

def test_coherencia_detecta_el_piache_separado():
    """El caso que motivó el módulo: el elenco tiene piaches (choza_piache) y
    caciques (casa_cacique) que no se solapan, y eso es el patrón de
    Barquisimeto, no el costero que la simulación dice modelar.

    Si este test empieza a fallar, es que alguien resolvió la decisión de canon
    — y entonces hay que actualizar la nota, no borrar el test."""
    avisos = coherencia_del_canon()
    assert any("barquisimeto" in a for a in avisos), (
        "esperábamos el aviso sobre poder sagrado/secular separado; "
        f"avisos={avisos}")


def test_coherencia_detecta_el_etnia_partido_por_genero():
    avisos = coherencia_del_canon()
    assert any("caquetía" in a and "etnia" in a for a in avisos)


def test_coherencia_no_revienta_sin_motor(monkeypatch):
    """Debe degradar a un aviso, no a una excepción."""
    import builtins
    real = builtins.__import__

    def falla(nombre, *a, **k):
        if nombre == "curiana_agents":
            raise ImportError("simulado")
        return real(nombre, *a, **k)

    monkeypatch.setattr(builtins, "__import__", falla)
    avisos = coherencia_del_canon()
    assert any("no se pudo leer" in a for a in avisos)


# ── el tipo Rasgo ─────────────────────────────────────────────────────

def test_rasgo_es_inmutable():
    """Los rasgos son dato citado, no estado que alguien deba poder mutar."""
    r = Rasgo("x", "fuente y")
    with pytest.raises(Exception):
        r.valor = "otro"


def test_rasgo_se_imprime_como_su_valor():
    assert str(Rasgo("el valor", "la fuente")) == "el valor"
