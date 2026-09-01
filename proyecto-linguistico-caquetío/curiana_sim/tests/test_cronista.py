"""Tests del cronista.

Lo que protegen es que la perspectiva sea **comprobable** y no una declaración
de intenciones. Una tabla de sustituciones que nadie verifica es una opinión;
verificada contra el lexicón y la bibliografía, es una afirmación sobre el dato
que se cae sola si alguien cambia el dato.

Y protegen el límite epistémico: el cronista es una lectura, nunca una fuente.
"""

import pytest

from curiana_cronista import (
    DESCOLONIZAR,
    LIMITE,
    glosario_prompt,
    prompt_cronista,
    verificar,
)


def test_la_tabla_se_sostiene_contra_el_dato():
    problemas = verificar()
    assert not problemas, "la tabla de descolonización no cuadra:\n" + "\n".join(
        f"  {p}" for p in problemas)


@pytest.mark.parametrize("fila", DESCOLONIZAR, ids=lambda f: f["ajeno"][:18])
def test_cada_sustitucion_dice_de_donde_viene_y_quien_lo_dice(fila):
    """Sin `de_donde_viene` y `fuente`, la sustitución sería un gusto personal.
    Con ellos es una corrección con cita."""
    assert fila["de_donde_viene"].strip()
    assert fila["fuente"].strip()
    assert fila["nota"].strip()


def test_las_palabras_ajenas_no_se_cuelan_en_el_prompt_como_nuestras():
    """`piache` y `cacique` pueden aparecer en el prompt —hay que nombrarlas
    para rechazarlas— pero solo del lado ajeno de la flecha."""
    glosario = glosario_prompt()
    for ajena in ("piache", "cacique"):
        assert f"«{ajena}»" in glosario, f"{ajena} debería nombrarse para rechazarla"
        assert f"→ **{ajena}**" not in glosario, (
            f"{ajena} aparece como palabra propuesta, y no es caquetía")


def test_el_prompt_usa_las_palabras_propias():
    p = prompt_cronista()
    # kapu, no capu: Fase 2 de D5 (2026-08-31) migró el lema al fonémico.
    for propia in ("boratio", "diao", "apopo", "kapu", "barsure", "biro", "para"):
        assert propia in p, f"el cronista debería nombrar `{propia}`"


def test_el_prompt_prohibe_inventar_datos():
    """La regla que impide que esta voz contamine el corpus."""
    p = prompt_cronista().lower()
    assert "no inventes" in p
    assert "evidencia" in p and "corpus" in p, (
        "el prompt tiene que decir que lo que cuenta no es evidencia ni entra "
        "al corpus")


def test_el_prompt_prohibe_romantizar():
    """Contar desde dentro no es contar bonito: hay hambre y hay raids."""
    assert "no romantices" in prompt_cronista().lower()


def test_el_limite_epistemico_esta_escrito():
    """La honestidad sobre qué es esta voz no puede quedar solo en el commit."""
    assert "construida" in LIMITE
    assert "extinta" in LIMITE
    assert "Paraguaná" in LIMITE


def test_el_limite_no_va_en_el_prompt_del_agente_por_defecto():
    """Un cronista no se explica a sí mismo mientras narra; pero el límite tiene
    que estar disponible para quien lea."""
    assert LIMITE not in prompt_cronista()
    assert LIMITE in prompt_cronista(incluir_limite=True)


def test_no_promete_recuperar_la_voz_caquetia():
    """El proyecto entero se cae si esto se vende como voz recuperada."""
    texto = prompt_cronista(incluir_limite=True).lower()
    assert "no se puede" in texto or "construida" in texto
    assert "fabricando" in texto or "no lo sería" in texto
