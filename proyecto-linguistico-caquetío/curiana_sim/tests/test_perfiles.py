"""Tests de los perfiles de run (curiana_perfiles.py + el filtro de capa).

Diseño: 5-experimento/disenos/05_perfiles_de_run.md
"""

import pytest

from curiana_perfiles import cargar_perfil, nombres, PERFIL_POR_DEFECTO
from curiana_lexicon import (VOCABULARIO_BASE, capa_epistemica,
                             muestra_caquetio_dinamica)


def test_los_perfiles_del_fichero_cargan_todos():
    for n in nombres():
        p = cargar_perfil(n)
        assert p.capas, f"el perfil {n} no declara ninguna capa"
        assert p.andamiaje in ("completo", "ninguno")


def test_el_perfil_por_defecto_es_como_se_corrio_la_era_1():
    """`base` no debe ver lo retro-abstraído: es la línea de comparación con
    todo lo ya publicado."""
    p = cargar_perfil(PERFIL_POR_DEFECTO)
    assert "caquetío-retroabstraido" not in p.capas
    assert p.andamiaje == "completo"


def test_las_capas_de_score_son_iguales_en_todos_los_perfiles():
    """🔴 El cable trampa que sostiene el experimento entero.

    Si el score se midiera con las capas de cada perfil, la diferencia entre
    brazos sería un artefacto del instrumento y no del habla — la lección de
    la fase 1. Puntuar igual en todos es lo que hace que la caída del brazo
    `suelto` SEA el dato.
    """
    referencia = cargar_perfil(PERFIL_POR_DEFECTO).capas_de_score
    for n in nombres():
        assert cargar_perfil(n).capas_de_score == referencia, (
            f"el perfil {n} cambia las capas de score; eso rompe la "
            f"comparabilidad entre brazos")


def test_capa_epistemica_solo_clasifica_caquetio():
    assert capa_epistemica("caquetío-atestiguado") == "caquetío-atestiguado"
    assert capa_epistemica("caquetío-reconstruido") == "caquetío-reconstruido"
    assert capa_epistemica("caquetío-retroabstraido") == "caquetío-retroabstraido"
    # `caquetío` a secas se trata como atestiguado, no se degrada por su cuenta
    assert capa_epistemica("caquetío") == "caquetío-atestiguado"
    # lo que no es caquetío no tiene capa: es comparanda
    assert capa_epistemica("wayunaiki") is None
    assert capa_epistemica("lokono") is None
    assert capa_epistemica("") is None


def test_el_brazo_atestiguado_ve_menos_lengua_que_el_base():
    base = cargar_perfil("base")
    duro = cargar_perfil("atestiguado")

    def disponibles(perfil):
        return sum(1 for e in VOCABULARIO_BASE.values()
                   if capa_epistemica(e.get("fuente", "")) in perfil.capas
                   and (e.get("sig") or e.get("es")))

    assert disponibles(duro) < disponibles(base), (
        "el brazo duro debería ver estrictamente menos vocabulario")


def test_la_muestra_del_prompt_respeta_las_capas():
    """Sin `capas` entra todo el caquetío (era 1); con `capas` sólo lo suyo."""
    duro = cargar_perfil("atestiguado")
    sin_filtro = muestra_caquetio_dinamica(n_por_categoria=40)
    con_filtro = muestra_caquetio_dinamica(n_por_categoria=40, capas=duro.capas)
    assert sin_filtro and con_filtro
    assert len(con_filtro) < len(sin_filtro)


def test_el_perfil_resuelto_va_entero_a_config():
    """Lo que se guarda es el perfil resuelto, no su nombre: un run de hace
    seis meses tiene que seguir diciendo con qué se corrió."""
    c = cargar_perfil("suelto").como_config()
    assert c["perfil"] == "suelto"
    assert c["ablacion"] is False
    assert "caquetío-retroabstraido" in c["capas_lexicas"]
    assert c["capas_lexicas"] == sorted(c["capas_lexicas"]), "orden estable"
    assert c["capas_de_score"], "sin capas de score el run no es comparable"


def test_control_es_la_ablacion():
    assert cargar_perfil("control").ablacion is True
    assert cargar_perfil("base").ablacion is False


def test_un_perfil_inexistente_falla_claro():
    with pytest.raises(KeyError):
        cargar_perfil("no-existe")
