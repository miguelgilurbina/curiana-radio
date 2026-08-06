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
    """En la costa el jefe es además gran chamán; en Barquisimeto no, y su
    boratio vive apartado. Las dos tienen boratio: la diferencia está en el
    jefe, no en si el oficio existe."""
    dif = contrastar("costera", "barquisimeto")
    assert "religion" in dif
    costera, barq = dif["religion"]
    assert "gran chamán" in costera.valor
    assert "cada pueblo principal hay un boratio" in costera.valor
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

def test_el_canon_es_coherente_con_la_polity_costera():
    """Manaure es "gobernante Y piache en uno", que es exactamente el modelo
    costero de Oliver (p. 279). No debe saltar el aviso de barquisimeto.

    Que existan además piaches especialistas (Shaboro) NO es un problema: la
    costa también tenía boratio "en cada pueblo principal" (Oviedo y Valdés
    t. II p.298, en Arcaya 1920 pp. 97-100). Lo que separa a las dos polities
    es si el JEFE es además gran chamán, no si el oficio existe."""
    avisos = coherencia_del_canon()
    assert not any("barquisimeto" in a for a in avisos), (
        f"el canon costero no debería disparar el aviso; avisos={avisos}")


def test_coherencia_avisa_si_el_cacique_pierde_el_don(monkeypatch):
    """La comprobación tiene que servir de algo: si el cacique deja de ser
    chamán, el aviso debe aparecer."""
    import curiana_agents
    falso = {
        "Manaure": {"ubicacion_default": "casa_cacique",
                    "descripcion": "Solo gobierna, reparte sal y juzga.",
                    "system_prompt": "Eres el señor. Administras el buco.",
                    "etnia": "caquetío"},
    }
    monkeypatch.setattr(curiana_agents, "ALL_AGENTS", falso)
    avisos = coherencia_del_canon()
    assert any("barquisimeto" in a for a in avisos)


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
