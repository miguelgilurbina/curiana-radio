"""Tests del validador de datos de lengua (compilar_lengua.py).

Lo que estos tests protegen es **la integridad referencial de las citas**. Hasta
que existió `bibliografia.yaml`, una cita era texto libre: nadie comprobaba que
la obra citada existiera. Ahora `procedencia.obra` es una clave foránea, y si
esa comprobación se rompe volvemos al régimen anterior sin enterarnos.

Como en `test_compilar_corpus.py`, la mitad son negativos: un validador que
nunca falla y uno que no valida nada se ven igual desde fuera.
"""

import pytest

from compilar_lengua import (
    LENGUAS_NUCLEO,
    NIVELES_TOPONIMO,
    compilar,
    obras_conocidas,
    validar_cognados,
    validar_procedencia,
    validar_toponimos,
)


def _codigos(problemas, nivel=None):
    return {p.codigo for p in problemas if nivel is None or p.nivel == nivel}


def _cognado(**kw):
    base = {
        "id": "cognado-001",
        "glosa": "luna",
        "formas": {"CQ": "cati", "LK": "katsi"},
        "procedencia": {"obra": "oliver-1989-cap2", "pagina": 142},
    }
    base.update(kw)
    return base


# ══════════════════════════════════════════════════════════════════════
# Los datos reales
# ══════════════════════════════════════════════════════════════════════

def test_los_datos_de_lengua_validan():
    _, problemas = compilar()
    errores = [p for p in problemas if p.nivel == "error"]
    assert not errores, "errores en los datos de lengua:\n" + "\n".join(
        f"  {p}" for p in errores)


def test_la_bibliografia_existe_y_tiene_obras():
    """Sin ella no hay integridad referencial: toda cita vuelve a ser prosa."""
    obras = obras_conocidas()
    assert obras, "4-fuentes/bibliografia.yaml no existe o está vacía"
    assert "oliver-1989-cap2" in obras
    assert "zavala-reyes-2015" in obras


def test_todo_cognado_declara_su_situacion_de_fuente():
    """O cita una obra, o dice explícitamente que no la tiene. Lo que no vale
    es callar: un hueco declarado es dato, un hueco callado es una cita que no
    existe."""
    datos, _ = compilar()
    for r in datos["cognados"]["cognados"]:
        tiene = r.get("procedencia") is not None
        declara = r.get("deuda") == "sin-procedencia"
        assert tiene or declara, f"{r['id']} no declara su situación de fuente"


# ══════════════════════════════════════════════════════════════════════
# La integridad referencial
# ══════════════════════════════════════════════════════════════════════

def test_detecta_obra_que_no_existe():
    """El punto entero de la bibliografía."""
    r = _cognado(procedencia={"obra": "borges-1941-tlon", "pagina": 1})
    problemas = validar_procedencia([r], {"oliver-1989-cap2"}, "cognados")
    assert "obra-fantasma" in _codigos(problemas)


def test_acepta_obra_que_si_existe():
    r = _cognado()
    assert not validar_procedencia([r], {"oliver-1989-cap2"}, "cognados")


def test_detecta_procedencia_callada():
    r = _cognado(procedencia=None)
    assert "procedencia-callada" in _codigos(validar_procedencia([r], set(), "cognados"))


def test_la_deuda_declarada_es_legal():
    r = _cognado(procedencia=None, deuda="sin-procedencia")
    assert not validar_procedencia([r], set(), "cognados")


def test_detecta_procedencia_sin_obra():
    r = _cognado(procedencia={"pagina": 42})
    assert "procedencia-sin-obra" in _codigos(validar_procedencia([r], set(), "cognados"))


# ══════════════════════════════════════════════════════════════════════
# Lo que es un cognado y lo que no
# ══════════════════════════════════════════════════════════════════════

def test_un_cognado_de_una_sola_lengua_no_es_un_cognado():
    doc = {"cognados": [_cognado(formas={"CQ": "quiripa"})]}
    assert "no-es-un-cognado" in _codigos(validar_cognados(doc, {"oliver-1989-cap2"}))


def test_codigo_del_nucleo_inventado_es_error():
    """Los códigos en mayúscula los usa `transducir()`: uno inventado rompería
    la transducción en silencio."""
    doc = {"cognados": [_cognado(formas={"CQ": "cati", "XX": "algo"})]}
    assert "codigo-de-lengua-desconocido" in _codigos(
        validar_cognados(doc, {"oliver-1989-cap2"}))


@pytest.mark.parametrize("lengua", ["maipure", "baré", "wapishana", "tariana"])
def test_la_comparanda_en_minuscula_es_libre(lengua):
    """Las ~24 lenguas arahuacas que cita Oliver son comparanda, no maquinaria.
    Cerrar esa lista obligaría a tocar el esquema cada vez que una fuente cita
    una lengua nueva."""
    doc = {"cognados": [_cognado(formas={"CQ": "cati", lengua: "kethi"})]}
    assert "codigo-de-lengua-desconocido" not in _codigos(
        validar_cognados(doc, {"oliver-1989-cap2"}))


def test_avisa_de_forma_repetida_entre_cognados():
    """`para` estaba en los dos almacenes. No se fusiona sola —decidir que dos
    entradas son la misma es criterio— pero no puede pasar desapercibido."""
    doc = {"cognados": [
        _cognado(id="cognado-001", formas={"CQ": "para", "LK": "bara"}),
        _cognado(id="cognado-002", formas={"CQ": "para", "TN": "bagua"}),
    ]}
    assert "forma-repetida" in _codigos(validar_cognados(doc, {"oliver-1989-cap2"}), "aviso")


def test_cognado_sin_glosa_es_error():
    doc = {"cognados": [_cognado(glosa=None)]}
    assert "sin-glosa" in _codigos(validar_cognados(doc, {"oliver-1989-cap2"}))


# ══════════════════════════════════════════════════════════════════════
# Topónimos
# ══════════════════════════════════════════════════════════════════════

def test_nivel_de_toponimo_ilegal():
    doc = {"toponimos": [{"id": "toponimo-001", "forma": "x", "nivel": "Z",
                          "procedencia": None, "deuda": "sin-procedencia"}]}
    assert "nivel-ilegal" in _codigos(validar_toponimos(doc, set(), None, set()))


@pytest.mark.parametrize("nivel", NIVELES_TOPONIMO)
def test_los_cuatro_niveles_son_legales(nivel):
    """El nivel es un CAMPO. Antes eran tres contenedores separados, y para
    listar todos los topónimos había que unir tres dicts."""
    doc = {"toponimos": [{"id": "toponimo-001", "forma": "x", "nivel": nivel,
                          "procedencia": None, "deuda": "sin-procedencia"}]}
    assert "nivel-ilegal" not in _codigos(validar_toponimos(doc, set(), None, set()))


def test_toponimos_reales_conservan_los_totales_del_modulo_viejo():
    """`lexicon_toponimos.TOTALES` declaraba 74 procesados y 6/8/13/47 por
    nivel. Si la migración fuera infiel, esto lo cazaría."""
    datos, _ = compilar()
    por_nivel = datos["toponimos"]["meta"]["por_nivel"]
    assert datos["toponimos"]["meta"]["toponimos"] == 74
    assert por_nivel == {"A": 6, "B": 8, "C": 13, "descartado": 47}


# ══════════════════════════════════════════════════════════════════════
# Ids
# ══════════════════════════════════════════════════════════════════════

def test_ids_unicos_en_los_datos_reales():
    datos, _ = compilar()
    for clave, seccion in (("cognados", "cognados"), ("toponimos", "toponimos"),
                           ("morfemas", "morfemas")):
        regs = datos[clave][seccion]
        ids = [r["id"] for r in regs]
        assert len(ids) == len(set(ids)), f"ids repetidos en {clave}"


def test_el_id_no_es_la_glosa_espanola():
    """La clave era la glosa, y por eso existía `rojo_almagre`: un desempate
    inventado para no chocar con `rojo`."""
    datos, _ = compilar()
    for r in datos["cognados"]["cognados"]:
        assert r["id"].startswith("cognado-")
        assert r["id"] != r.get("glosa")
