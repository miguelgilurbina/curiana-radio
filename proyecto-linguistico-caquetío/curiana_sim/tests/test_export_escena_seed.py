"""Tests del exportador de la ESCENA — el seed del visor de repetición.

PR 10 «escena: el mapa» (decisión 10 de Miguel, 2026-09-17). Lo que hay que
vigilar aquí es que el JSON que come la web diga la verdad:

  - que el catálogo de lugares sea **el de la tabla DECIDIDA** —la que corrió:
    28 lugares, 8 con punto propio, 16 heredando el de su aldea, 2 áreas y 2
    caminos— y no una resolución nueva inventada aquí, ni la PROPUESTA de la
    que la tabla salió (leerla es leer otro mapa: allí el camino de la alianza
    son dos entradas y en la decidida es una, y por eso el primer run con
    gente lo dibujó «sin coordenada, aparte»);
  - que el nodo de un lugar y su marca de compartido sean los que la tabla
    decidida declara (el Capubana, su fuente y el camino Moruy–Caseto);
  - que sin filas el seed salga **vacío y válido**, con el mapa entero y sin
    nadie encima: es lo que escribe `--sin-base` y lo que la web enseña
    mientras no haya un seed con gente;
  - que el texto se recorte al tope DECLARADO y que el JSON lo diga;
  - que el lugar de una respuesta lo mande `presencias` y que una discrepancia
    con `agent_responses.lugar` se AVISE en vez de elegirse en silencio.

Sin red y sin base: el mock guarda la escena en memoria (con las MISMAS filas
que `CurianaDB`, porque comparten `filas_de_presencias`) y el resto entra como
un fixture de dos turnos.
"""

import json

import pytest

import export_escena_seed as ees
from curiana_database import CurianaDBMock

RUN = "0193873d-1111-2222-3333-444444444444"
RUN_PADRE = "3973d317-1111-2222-3333-444444444444"

# Las claves que consume `lib/escena.ts` en la web. Si cambian, la página rompe.
CLAVES_SEED = {"version", "generado", "vacio", "tope_texto", "run", "lugares",
               "turnos", "avisos"}
CLAVES_RUN = {"id8", "run_id", "cadena", "started_at", "serie", "brazo",
              "dias", "n_turnos", "n_agentes", "n_presencias"}
CLAVES_LUGAR = {"id", "nombre", "sitio", "locacion", "nodo", "tipo", "lat",
                "lon", "puntos", "compartido", "por_que"}
CLAVES_TURNO = {"i", "run", "dia", "turno", "momento", "n_presencias", "escenas"}
CLAVES_ESCENA = {"lugar", "n", "por_nodo", "contacto", "presentes", "dichos"}


@pytest.fixture(scope="module")
def catalogo():
    return ees.catalogo_de_lugares(ees.cargar_tabla())


# ══════════════════════════════════════════════════════════════════════
# El catálogo: se LEE de la tabla DECIDIDA, no se recalcula
# ══════════════════════════════════════════════════════════════════════

def test_los_28_lugares_con_la_resolucion_que_la_tabla_ya_hizo(catalogo):
    """8 propios, 16 heredados, 2 zonas, 2 caminos, 0 sin nada: en la tabla
    decidida ningún lugar se queda sin punto (§5b)."""
    assert len(catalogo) == 28
    tipos = {}
    for l in catalogo:
        tipos[l["tipo"]] = tipos.get(l["tipo"], 0) + 1
    assert tipos == {"propio": 8, "heredado": 16, "zona": 2, "camino": 2}
    assert all(l["lat"] is not None and l["lon"] is not None for l in catalogo)


def test_el_catalogo_es_el_que_corrio_y_no_la_propuesta(catalogo):
    """La puerta es `curiana_escena.lugares()`: el catálogo del seed y la
    tabla con la que el motor repartió a los 63 son la MISMA."""
    import curiana_escena
    por_id = {l["id"]: l for l in catalogo}
    assert set(por_id) == set(curiana_escena.lugares())
    # el camino de la alianza existe SÓLO en la decidida, y con su coordenada
    assert por_id["camino:Moruy-Caseto"]["lat"] is not None
    assert "camino:Moruy" not in por_id and "camino:Caseto" not in por_id
    # y el nombre es la glosa del canon, no una etiqueta armada aquí
    assert por_id["Tacuato:orilla"]["nombre"] == "la orilla de Tacuato"


def test_cada_lugar_trae_las_claves_que_la_web_espera(catalogo):
    for l in catalogo:
        assert set(l) == CLAVES_LUGAR


def test_el_nodo_de_un_lugar_es_el_que_la_tabla_declara(catalogo):
    """No hay frontera programada: el nodo de un lugar es el de quien lo
    trabaja y la tabla decidida ya lo midió (§0.2 del diseño). Se dice como lo
    dice la web: `compartido` en minúscula, que es el tipo `NodoEscena`."""
    por_id = {l["id"]: l for l in catalogo}
    assert por_id["Tacuato:salinar"]["nodo"] == "GUARANAO"
    assert por_id["Carirubana:orilla"]["nodo"] == "AMUAY"
    assert por_id["ZG2"]["nodo"] == "GUARANAO"
    assert por_id["ZA1"]["nodo"] == "AMUAY"
    # El cerro no es de nadie. Leyendo la propuesta salía GUARANAO.
    assert por_id["Capubana"]["nodo"] == "compartido"
    assert all(l["nodo"] in ("GUARANAO", "AMUAY", "compartido") for l in catalogo)


def test_los_compartidos_son_los_declarados_y_nadie_mas(catalogo):
    """El Capubana (con su fuente) y el camino Moruy–Caseto: decisión p2 «B»."""
    compartidos = {l["id"] for l in catalogo if l["compartido"]}
    assert compartidos == {"Capubana", "Capubana:fuente", "camino:Moruy-Caseto"}
    assert all(l["por_que"] for l in catalogo if l["compartido"])


def test_el_camino_de_la_alianza_tiene_sus_dos_extremos(catalogo):
    """Moruy–Caseto es el único par que el canon nombra; a los demás caminos no
    se les inventa destino."""
    por_id = {l["id"]: l for l in catalogo}
    alianza = por_id["camino:Moruy-Caseto"]
    assert alianza["puntos"] == [[11.822, -69.983], [11.762, -70.017]]
    assert alianza["sitio"] == "Moruy" and alianza["compartido"] is True
    assert por_id["camino:El Cayude"]["puntos"] is None


def test_una_zona_lleva_sus_puntos_y_no_solo_uno(catalogo):
    por_id = {l["id"]: l for l in catalogo}
    assert len(por_id["ZG2"]["puntos"]) == 5
    assert len(por_id["ZA1"]["puntos"]) == 7


# ══════════════════════════════════════════════════════════════════════
# El recorte del texto
# ══════════════════════════════════════════════════════════════════════

def test_lo_que_cabe_no_se_toca():
    texto, cortado = ees.recortar("taya naa-ka biro-ana", tope=220)
    assert (texto, cortado) == ("taya naa-ka biro-ana", False)


def test_lo_que_no_cabe_se_corta_en_una_palabra_y_se_marca():
    largo = "wa-kari duna-rua-ana " * 40
    texto, cortado = ees.recortar(largo, tope=60)
    assert cortado is True
    assert len(texto) <= 61          # el tope + la elipsis
    assert texto.endswith("…")
    assert not texto[:-1].endswith(" ")


def test_el_tope_va_escrito_en_el_json(catalogo):
    seed = ees.construir_seed(run_meta={}, presencias=[], respuestas=[],
                              turnos=[], lugares=catalogo, tope=280)
    assert seed["tope_texto"] == 280


# ══════════════════════════════════════════════════════════════════════
# Sin filas: vacío y válido
# ══════════════════════════════════════════════════════════════════════

def test_sin_filas_el_seed_es_vacio_valido_y_con_el_mapa_entero():
    seed = ees.seed_vacio()
    assert set(seed) == CLAVES_SEED
    assert set(seed["run"]) == CLAVES_RUN
    assert seed["vacio"] is True
    assert seed["turnos"] == []
    assert len(seed["lugares"]) == 28        # el mapa se dibuja igual
    assert json.loads(json.dumps(seed, ensure_ascii=False))["version"] == 2


# ══════════════════════════════════════════════════════════════════════
# Con el mock: la escena que el motor escribiría
# ══════════════════════════════════════════════════════════════════════

MOMENTOS = ["amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche"]

# 63 agentes, como el elenco de la era 2, repartidos en dos lugares de nodos
# distintos. Los nombres son sintéticos: lo que se mide es la aritmética de la
# escena, no el casting (igual que en tests/test_presencias.py).
ESCENA_63 = {f"agente{i:02d}": ("Moruy" if i % 2 else "Carirubana:orilla")
             for i in range(1, 64)}


def _turno_id(n: int) -> str:
    return f"22222222-2222-2222-2222-{n:012d}"


def _seed_del_mock(db, run_ids, catalogo, **kw):
    """El seed a partir de lo que el mock guardó. `respuestas`/`turnos` van
    vacíos a propósito: el mock guarda la escena, no el texto de las
    respuestas, y ésa es la frontera de lo que un test sin base puede decir."""
    return ees.construir_seed(
        run_meta={"id8": run_ids[-1][:8], "run_id": run_ids[-1],
                  "run_ids": run_ids, "cadena": [r[:8] for r in run_ids]},
        presencias=db.presencias_de_cadena(run_ids),
        respuestas=kw.get("respuestas", []), turnos=kw.get("turnos", []),
        lugares=catalogo)


def test_el_mock_escribe_dos_turnos_y_el_seed_los_lee(catalogo):
    db = CurianaDBMock()
    for i, momento in enumerate(MOMENTOS[:2], start=1):
        db.save_presencias(RUN, _turno_id(i), 1, i, momento, ESCENA_63)

    seed = _seed_del_mock(db, [RUN], catalogo)

    assert seed["vacio"] is False
    assert seed["run"]["n_turnos"] == 2
    assert seed["run"]["n_agentes"] == 63
    assert seed["run"]["n_presencias"] == 126
    assert seed["run"]["dias"] == [1]
    assert [t["momento"] for t in seed["turnos"]] == MOMENTOS[:2]
    assert [t["i"] for t in seed["turnos"]] == [0, 1]

    # Dos lugares, y la gente repartida: 32 impares en Moruy, 31 en la orilla.
    primero = seed["turnos"][0]
    assert {e["lugar"] for e in primero["escenas"]} == {"Moruy", "Carirubana:orilla"}
    assert sum(e["n"] for e in primero["escenas"]) == 63
    for e in primero["escenas"]:
        assert set(e) == CLAVES_ESCENA
        assert e["dichos"] == []              # el mock no guarda texto
        assert all(p["hablo"] is False for p in e["presentes"])
    assert set(primero) == CLAVES_TURNO


def test_un_run_sin_escena_no_deja_nada_en_el_mapa(catalogo):
    """La era 1 (o `--sin-escena`) pasa `{}`: ni una fila, ni un punto."""
    db = CurianaDBMock()
    db.save_presencias(RUN, _turno_id(1), 1, 1, "amanecer", {})
    seed = _seed_del_mock(db, [RUN], catalogo)
    assert seed["vacio"] is True
    assert seed["turnos"] == []
    assert len(seed["lugares"]) == 28


def test_la_cadena_ordena_por_run_y_no_por_numero_de_dia(catalogo):
    """En la era 2 un run es UN día y la numeración puede repetirse: el orden
    del deslizador lo manda la posición del run en la cadena."""
    db = CurianaDBMock()
    db.save_presencias(RUN_PADRE, _turno_id(1), 1, 1, "amanecer", ESCENA_63)
    db.save_presencias(RUN, _turno_id(2), 1, 1, "amanecer", ESCENA_63)
    seed = _seed_del_mock(db, [RUN_PADRE, RUN], catalogo)
    assert [t["run"] for t in seed["turnos"]] == ["3973d317", "0193873d"]
    assert seed["run"]["cadena"] == ["3973d317", "0193873d"]


# ══════════════════════════════════════════════════════════════════════
# Fixture de dos turnos: la escena con voz
# ══════════════════════════════════════════════════════════════════════

T1, T2 = _turno_id(1), _turno_id(2)

# Dos turnos de un día, cinco agentes, tres lugares. Capubana lo tocan los dos
# nodos en el turno 2: es la única escena de contacto del fixture.
PRESENCIAS_FIXTURE = [
    # turno 1 — cada nodo en lo suyo
    {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1, "momento": "amanecer",
     "agent_name": "Birokoa", "lugar": "Tacuato:salinar", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1, "momento": "amanecer",
     "agent_name": "Chakamba", "lugar": "Tacuato:salinar", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1, "momento": "amanecer",
     "agent_name": "Bajari", "lugar": "Caseto", "nodo": "AMUAY"},
    {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1, "momento": "amanecer",
     "agent_name": "Sawaka", "lugar": "Capubana", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1, "momento": "amanecer",
     "agent_name": "Waranaro", "lugar": "Caseto", "nodo": "AMUAY"},
    # turno 2 — Bajari sube al cerro: los dos nodos en el mismo lugar
    {"run_id": RUN, "turn_id": T2, "day": 1, "turn_num": 2, "momento": "mañana",
     "agent_name": "Birokoa", "lugar": "Tacuato:salinar", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T2, "day": 1, "turn_num": 2, "momento": "mañana",
     "agent_name": "Chakamba", "lugar": "Tacuato", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T2, "day": 1, "turn_num": 2, "momento": "mañana",
     "agent_name": "Bajari", "lugar": "Capubana", "nodo": "AMUAY"},
    {"run_id": RUN, "turn_id": T2, "day": 1, "turn_num": 2, "momento": "mañana",
     "agent_name": "Sawaka", "lugar": "Capubana", "nodo": "GUARANAO"},
    {"run_id": RUN, "turn_id": T2, "day": 1, "turn_num": 2, "momento": "mañana",
     "agent_name": "Waranaro", "lugar": "Caseto", "nodo": "AMUAY"},
]

TURNOS_FIXTURE = [
    {"id": T1, "run_id": RUN, "day": 1, "turn_num": 1, "moment": "amanecer"},
    {"id": T2, "run_id": RUN, "day": 1, "turn_num": 2, "moment": "mañana"},
]

LARGO = "taya naa-ka biro-ana pia chaa-da-ma wa-kari duna-rua-ana " * 8

RESPUESTAS_FIXTURE = [
    {"id": 1, "run_id": RUN, "turn_id": T1, "agent_name": "Birokoa",
     "response_text": "taya naa-ka biro-ana", "lugar": "Tacuato:salinar"},
    {"id": 2, "run_id": RUN, "turn_id": T1, "agent_name": "Chakamba",
     "response_text": LARGO, "lugar": "Tacuato:salinar"},
    # Sin la columna desnormalizada: el lugar lo pone `presencias`.
    {"id": 3, "run_id": RUN, "turn_id": T2, "agent_name": "Bajari",
     "response_text": "wa-kari kashi-kasuta-iro", "lugar": None},
    # Con la columna en desacuerdo: manda `presencias` y se avisa.
    {"id": 4, "run_id": RUN, "turn_id": T2, "agent_name": "Sawaka",
     "response_text": "nüma chaa-ni", "lugar": "Moruy"},
    # Sin turno conocido y sin presencia: huérfana, se avisa y no entra.
    {"id": 5, "run_id": RUN, "turn_id": "99999999-9999-9999-9999-999999999999",
     "agent_name": "Fantasma", "response_text": "nadie estaba aquí", "lugar": None},
]


@pytest.fixture
def seed(catalogo):
    return ees.construir_seed(
        run_meta={"id8": RUN[:8], "run_id": RUN, "run_ids": [RUN],
                  "cadena": [RUN[:8]], "started_at": "2026-09-17T00:00:00Z"},
        presencias=PRESENCIAS_FIXTURE, respuestas=RESPUESTAS_FIXTURE,
        turnos=TURNOS_FIXTURE, lugares=catalogo, tope=60,
        generado="2026-09-17T00:00:00+00:00")


def test_el_fixture_arma_dos_turnos_con_su_momento(seed):
    assert set(seed) == CLAVES_SEED
    assert seed["vacio"] is False
    assert [(t["dia"], t["turno"], t["momento"]) for t in seed["turnos"]] == [
        (1, 1, "amanecer"), (1, 2, "mañana")]
    assert seed["run"]["n_presencias"] == 10
    assert seed["run"]["n_agentes"] == 5


def test_el_tamano_del_punto_es_cuanta_gente_hay(seed):
    t1 = {e["lugar"]: e for e in seed["turnos"][0]["escenas"]}
    assert t1["Tacuato:salinar"]["n"] == 2
    assert t1["Caseto"]["n"] == 2
    assert t1["Capubana"]["n"] == 1
    assert t1["Tacuato:salinar"]["por_nodo"] == {"GUARANAO": 2}


def test_una_escena_con_los_dos_nodos_queda_marcada(seed):
    t2 = {e["lugar"]: e for e in seed["turnos"][1]["escenas"]}
    assert t2["Capubana"]["contacto"] is True
    assert t2["Capubana"]["por_nodo"] == {"AMUAY": 1, "GUARANAO": 1}
    assert t2["Tacuato:salinar"]["contacto"] is False


def test_lo_que_se_dijo_va_donde_se_dijo_y_recortado(seed):
    t1 = {e["lugar"]: e for e in seed["turnos"][0]["escenas"]}
    dichos = {d["agente"]: d for d in t1["Tacuato:salinar"]["dichos"]}
    assert set(dichos) == {"Birokoa", "Chakamba"}
    assert dichos["Birokoa"]["recortado"] is False
    assert dichos["Birokoa"]["texto"] == "taya naa-ka biro-ana"
    assert dichos["Birokoa"]["nodo"] == "GUARANAO"
    assert dichos["Chakamba"]["recortado"] is True
    assert len(dichos["Chakamba"]["texto"]) <= 61
    # Y quien habló queda marcado entre los presentes.
    hablaron = {p["agente"] for p in t1["Tacuato:salinar"]["presentes"] if p["hablo"]}
    assert hablaron == {"Birokoa", "Chakamba"}
    assert t1["Caseto"]["dichos"] == []


def test_el_lugar_lo_manda_presencias_y_la_discrepancia_se_avisa(seed):
    """Sawaka dijo lo suyo en el Capubana; `agent_responses.lugar` decía Moruy."""
    t2 = {e["lugar"]: e for e in seed["turnos"][1]["escenas"]}
    assert {d["agente"] for d in t2["Capubana"]["dichos"]} == {"Bajari", "Sawaka"}
    assert "Moruy" not in {e["lugar"] for e in seed["turnos"][1]["escenas"]}
    assert any("distinto" in a for a in seed["avisos"])


def test_una_respuesta_sin_lugar_ni_presencia_no_se_cuela(seed):
    agentes = {d["agente"] for t in seed["turnos"]
               for e in t["escenas"] for d in e["dichos"]}
    assert "Fantasma" not in agentes
    assert any("sin lugar ni presencia" in a for a in seed["avisos"])


def test_un_lugar_que_la_tabla_no_conoce_se_dibuja_aparte_y_se_avisa(catalogo):
    inventado = dict(PRESENCIAS_FIXTURE[0], lugar="Golfete:orilla")
    seed = ees.construir_seed(
        run_meta={"id8": RUN[:8], "run_id": RUN, "run_ids": [RUN]},
        presencias=[inventado], respuestas=[], turnos=[], lugares=catalogo)
    fuera = [l for l in seed["lugares"] if l["id"] == "Golfete:orilla"]
    assert fuera and fuera[0]["tipo"] == "sin-coordenada" and fuera[0]["lat"] is None
    assert any("y no en la tabla decidida" in a for a in seed["avisos"])


def test_todo_lugar_de_presencias_tiene_punto_o_sale_en_los_avisos(catalogo):
    """EL INVARIANTE DEL VISOR, y la razón de leer la tabla decidida: un lugar
    donde la escena puso gente o se dibuja en su sitio o se dice que no se
    pudo. Lo que no puede pasar —y pasó con `camino:Moruy-Caseto` el
    2026-09-18— es que un lugar del canon caiga en el saco de los avisos por
    estar leyendo otra tabla.

    Se prueba con LOS 28 lugares que la escena reparte, que son exactamente
    los que `presencias` escribe, más uno inventado."""
    import curiana_escena
    de_la_tabla = sorted(curiana_escena.lugares())
    usados = de_la_tabla + ["Golfete:orilla"]
    presencias = [
        {"run_id": RUN, "turn_id": T1, "day": 1, "turn_num": 1,
         "momento": "amanecer", "agent_name": f"agente{i:02d}",
         "lugar": lugar, "nodo": "GUARANAO"}
        for i, lugar in enumerate(usados)
    ]
    seed = ees.construir_seed(
        run_meta={"id8": RUN[:8], "run_id": RUN, "run_ids": [RUN]},
        presencias=presencias, respuestas=[], turnos=TURNOS_FIXTURE,
        lugares=catalogo)

    por_id = {l["id"]: l for l in seed["lugares"]}
    for lugar in usados:
        assert lugar in por_id, lugar
        avisado = any(f"«{lugar}»" in a for a in seed["avisos"])
        assert por_id[lugar]["lat"] is not None or avisado, lugar
    # y el único avisado es el inventado: los 28 del canon tienen su punto
    sin_punto = [l["id"] for l in seed["lugares"] if l["lat"] is None]
    assert sin_punto == ["Golfete:orilla"]
    assert all(por_id[l]["lat"] is not None for l in de_la_tabla)


def test_el_seed_del_fixture_serializa_a_json(seed):
    texto = json.dumps(seed, ensure_ascii=False, indent=2)
    assert json.loads(texto) == seed
