# -*- coding: utf-8 -*-
"""Que ninguna entrada caquetía caiga en la capa atestiguada por descuido.

`capa_epistemica()` tiene un `return` por defecto: cualquier `fuente` que
contenga «caquetío» y no case con ningún sufijo conocido sale como
ATESTIGUADA. Eso convirtió seis entradas viejas con `fuente: "caquetío"` a
secas en atestiguadas sin que nadie lo decidiera — dos de ellas con un
comentario que decía, con todas las letras, que la atribución era débil
(`chiriware`, `tukeke`: voces zoonímicas panvenezolanas).

Se repartieron el 2026-09-10. Estos tests impiden que vuelva a pasar: un
`fuente` nuevo mal escrito, o una capa nueva sin declarar, falla aquí en vez
de colarse en el brazo estricto del experimento.
"""
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PERFILES = os.path.join(RAIZ, "5-experimento", "perfiles_de_run.yaml")

SUFIJOS_DECLARADOS = ("atestiguado", "reconstruido", "hipotético", "hipotetico",
                      "retroabstraido", "retro-abstraido")


def _caquetias():
    for clave, datos in VOCABULARIO_BASE.items():
        f = str(datos.get("fuente", ""))
        if "caquetío" in f.lower() or "caquetio" in f.lower():
            yield clave, f


def test_ninguna_entrada_cae_en_la_capa_por_defecto():
    """Toda caquetía declara su capa; ninguna llega a atestiguada por descuido."""
    huerfanas = [(c, f) for c, f in _caquetias()
                 if not any(s in f.lower() for s in SUFIJOS_DECLARADOS)]
    assert not huerfanas, (
        "Estas entradas tienen `fuente` caquetío sin sufijo de capa, así que "
        "capa_epistemica() las manda a ATESTIGUADO por defecto — que es "
        "exactamente lo que pasó con las seis de 2026-09-10:\n  " +
        "\n  ".join(f"{c}: {f!r}" for c, f in huerfanas))


def test_toda_capa_del_lexicon_la_ve_algun_perfil():
    """Una capa que ningún perfil lista no llegaría nunca a un agente."""
    with open(PERFILES, encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    perfiles = d.get("perfiles") or d
    vistas = set()
    for p in perfiles.values():
        if isinstance(p, dict):
            vistas.update(p.get("capas_lexicas") or [])
    en_uso = {capa_epistemica(f) for _, f in _caquetias()}
    en_uso.discard(None)
    ciegas = sorted(en_uso - vistas)
    assert not ciegas, (
        f"El lexicón usa capas que NINGÚN perfil incluye en `capas_lexicas`: "
        f"{ciegas}. Esas entradas no llegarían a ningún agente en ningún "
        f"brazo del experimento.")


@pytest.mark.parametrize("clave,capa_esperada", [
    # las dos que el reparto del 2026-09-10 sacó de «atestiguada por defecto»
    ("chiriware", "caquetío-retroabstraido"),
    ("tukeke", "caquetío-retroabstraido"),
    # y las cuatro que sí tenían con qué quedarse arriba
    ("maure", "caquetío-atestiguado"),
    ("korie", "caquetío-atestiguado"),
    ("curiana", "caquetío-atestiguado"),
    ("saruro", "caquetío-atestiguado"),
])
def test_el_reparto_de_las_seis_se_mantiene(clave, capa_esperada):
    """Fija el fallo de Miguel del 2026-09-10, una por una."""
    assert clave in VOCABULARIO_BASE, f"{clave} desapareció del lexicón"
    capa = capa_epistemica(VOCABULARIO_BASE[clave]["fuente"])
    assert capa == capa_esperada, (
        f"{clave} debería estar en {capa_esperada} y está en {capa}. "
        f"Si es un cambio querido, actualiza este test y di por qué.")


def test_la_capa_retroabstraida_no_esta_vacia():
    """Si se vacía, el brazo `suelto` vuelve a ser un clon de `base`."""
    n = sum(1 for _, f in _caquetias()
            if capa_epistemica(f) == "caquetío-retroabstraido")
    assert n > 0, (
        "La capa retro-abstraída está vacía. El perfil `suelto` la lista en "
        "sus capas_lexicas, así que sin entradas produce exactamente lo mismo "
        "que `base` y el brazo laxo del experimento no mide nada.")
