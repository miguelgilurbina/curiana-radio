"""La tabla de la escena de la era 2, en datos (PR 1 del diseño del 2026-09-17).

  - `curiana_escena_era2.py` es GENERADO: tiene que ser lo que emite
    6-fusion/scripts/generar_escena_era2.py desde 6-fusion/escena_era2.yaml,
    que a su vez es lo que emite el derivador con --canon desde el elenco.
  - Cobertura 63/63 en los seis momentos de los tres períodos.
  - Toda plantilla resuelve: ningún lugar se queda con `{sitio}` dentro.
  - Ningún lugar sin sitio ni coordenada (es lo que el visor del PR 10 pide).
  - Las decisiones de Miguel: 1 → A (por momento con excepciones fechadas) y
    2 → B (compartidos: el Capubana y el camino Moruy–Caseto).
  - Cada clase de oficio lleva su etiqueta epistémica y su fuente.
"""
import importlib.util
import io
import os

import pytest
import yaml

import curiana_escena_era2 as escena

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(SIM)
GENERADOR = os.path.join(RAIZ, "6-fusion", "scripts", "generar_escena_era2.py")
DERIVADOR = os.path.join(RAIZ, "6-fusion", "scripts", "derivar_escena_por_lugar.py")
TABLA = os.path.join(RAIZ, "6-fusion", "escena_era2.yaml")
MODULO = os.path.join(SIM, "curiana_escena_era2.py")


def _cargar(ruta: str, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def tabla() -> dict:
    return yaml.safe_load(io.open(TABLA, encoding="utf-8"))


# ── el módulo es generado ─────────────────────────────────────────────

def test_el_modulo_generado_es_lo_que_emite_el_script(tabla):
    """Regla del proyecto para los generados: se corrige la tabla del
    derivador, se regenera el YAML y se regenera el módulo. Nadie lo edita."""
    gen = _cargar(GENERADOR, "generar_escena_era2")
    assert io.open(MODULO, encoding="utf-8").read() == gen.emitir(tabla)


def test_la_tabla_es_lo_que_deriva_del_elenco(tabla):
    """El YAML tampoco se escribe a mano: sale del elenco por las reglas de
    clase y las plantillas. Si el casting cambia, la tabla cambia sola."""
    der = _cargar(DERIVADOR, "derivar_escena_por_lugar")
    ag = der.elenco()
    esperado = {
        a["nombre"]: {p: [der.lugar_de(a, m, p, True) for m in der.MOMENTOS]
                      for p in der.PERIODOS}
        for a in ag
    }
    real = {n: {p: list(f[p]) for p in der.PERIODOS}
            for n, f in tabla["escena_por_agente"].items()}
    assert real == esperado
    assert tabla["clase_por_agente"] == {a["nombre"]: a["_clase"] for a in ag}


# ── cobertura: los 63 en los 6 momentos de los 3 períodos ─────────────

def test_cobertura_63_por_6_por_3(tabla):
    assert len(escena.ESCENA) == len(tabla["escena_por_agente"]) == 63
    assert len(escena.MOMENTOS) == 6 and len(escena.PERIODOS) == 3
    for nombre, fila in escena.ESCENA.items():
        assert set(fila) == set(escena.PERIODOS), nombre
        for p in escena.PERIODOS:
            assert len(fila[p]) == 6, (nombre, p)
            assert all(l for l in fila[p]), (nombre, p, fila[p])
    for p, d in tabla["cobertura"].items():
        assert d["con_lugar_en_los_seis"] == d["de"] == 63, p
    # 63 × 6 × 3 escenas, y la puerta de lectura devuelve todas
    total = [escena.lugar_de(n, p, m) for n in escena.ESCENA
             for p in escena.PERIODOS for m in escena.MOMENTOS]
    assert len(total) == 63 * 3 * 6 and all(total)


def test_toda_plantilla_resuelve(tabla):
    """Ningún lugar se queda con un marcador dentro: `{sitio}`, `{zona}` y
    `{jaguey}` se resuelven al derivar, no en el motor."""
    for nombre, fila in escena.ESCENA.items():
        for p in escena.PERIODOS:
            for l in fila[p]:
                assert "{" not in l and "}" not in l, (nombre, p, l)
                assert l in escena.LUGARES, (nombre, p, l)


def test_ningun_lugar_sin_sitio_ni_coordenada():
    """Un mapa con lugares sin punto no es un mapa (diseño §5b)."""
    usados = {l for f in escena.ESCENA.values() for p in escena.PERIODOS for l in f[p]}
    assert usados == set(escena.LUGARES)
    for lug, d in escena.LUGARES.items():
        assert d["lat"] is not None and d["lon"] is not None, lug
        assert d["nodo"] in ("GUARANAO", "AMUAY", "COMPARTIDO"), (lug, d["nodo"])
        assert d["glosa"] and "{" not in d["glosa"], lug
        if d["tipo"] in ("aldea", "locacion"):
            assert d["sitio"], lug
        else:
            assert d["tipo"] in ("zona", "camino"), (lug, d["tipo"])


# ── las decisiones de Miguel (2026-09-17) ─────────────────────────────

def test_decision_2_b_los_compartidos_son_el_cerro_y_el_camino():
    """«Capubana + el camino Moruy–Caseto, que el elenco llama la alianza»."""
    assert set(escena.COMPARTIDOS) == {"Capubana", "Capubana:fuente",
                                       "camino:Moruy-Caseto"}
    for lug, razon in escena.COMPARTIDOS.items():
        assert razon and escena.LUGARES[lug]["nodo"] == "COMPARTIDO", lug


def test_el_camino_compartido_junta_a_los_dos_nodos():
    """El primer contacto EMERGENTE de toda la tabla, y no está escrito: sale
    de los destinos que la ficha de cada mensajero nombra."""
    encuentros = set()
    for p in escena.PERIODOS:
        for i, m in enumerate(escena.MOMENTOS):
            nodos = {escena.NODO_DE[n] for n, f in escena.ESCENA.items()
                     if f[p][i] == "camino:Moruy-Caseto"}
            if len(nodos) > 1:
                encuentros.add((p, m))
    assert encuentros, "el camino de la alianza no junta a nadie"
    assert {m for _, m in encuentros} == {"mañana", "mediodia", "tarde"}
    # uno de cada nodo, y son los dos mensajeros de los extremos
    quienes = {n for n, f in escena.ESCENA.items() if "camino:Moruy-Caseto" in f["viento"]}
    assert {escena.NODO_DE[n] for n in quienes} == {"GUARANAO", "AMUAY"}
    assert all(escena.CLASE_DE[n] == "mensajeria" for n in quienes), quienes


def test_la_travesia_de_la_alianza_es_la_esposa_principal(tabla):
    """El canon dice «la esposa principal viene por él». Quién es no se
    escribe: es el cruzado por matrimonio cuyos dos sitios son los extremos."""
    fila = escena.TRAVESIA["filas"][0]
    assert fila["lugar"] == "camino:Moruy-Caseto"
    assert fila["agentes"] == ["Karebe"]
    assert fila["momentos"] == ["mañana", "mediodia", "tarde"]
    assert fila["cuando"] == "vispera_de_capubana"
    assert "canon-simulacion" in fila["etiqueta"] and fila["fuente"]
    # Wamipa encaja en la geografía y no en la frase: es hijo, no cónyuge
    assert fila["encajan_en_la_geografia_pero_no_en_la_frase"] == ["Wamipa"]


def test_decision_1_a_las_excepciones_son_las_que_el_canon_fecha(tabla):
    """Por momento, con excepciones donde el canon fecha la hora: la pesca de
    noche con jachos en el viento, el conuco que espera en la seca larga, el
    agua que sube a la fuente del cerro, el salinar parado en la siembra."""
    t = tabla["tabla"]
    assert t["pesca"]["excepciones_por_periodo"]["viento"]["noche"] == "{zona}"
    assert t["conuco"]["excepciones_por_periodo"]["seca_larga"]["mañana"] == "{sitio}"
    assert t["agua_dulce"]["excepciones_por_periodo"]["seca_larga"]["amanecer"] == "Capubana:fuente"
    assert t["sal"]["excepciones_por_periodo"]["siembra"]["mañana"] == "{sitio}:conuco"
    # Y el efecto en la escena resuelta: en la seca larga sube a la fuente del
    # cerro MÁS gente del agua que en el viento (la casa del Manaure bebe del
    # cerro todo el año; los demás sólo cuando el jagüey baja).
    def en_la_fuente(p):
        return {n for n, f in escena.ESCENA.items() if f[p][0] == "Capubana:fuente"}
    assert all(escena.CLASE_DE[n] == "agua_dulce" for n in en_la_fuente("seca_larga"))
    assert en_la_fuente("viento") < en_la_fuente("seca_larga")


def test_cada_clase_lleva_etiqueta_y_fuente():
    """Etiqueta epistémica en todo (regla 2 del proyecto). La etiqueta vive en
    el YAML y en el módulo; nunca entra al prompt."""
    assert set(escena.ETIQUETAS) == set(escena.CLASE_DE.values())
    for clase, d in escena.ETIQUETAS.items():
        assert d["etiqueta"] and d["fuente"], clase
        assert any(p in d["etiqueta"] for p in
                   ("atestiguado", "canon-simulacion", "reconstruido", "hipotetico")), clase


def test_el_capubana_declara_su_cadencia_y_su_dia():
    assert escena.CAPUBANA["lugar"] == "Capubana"
    assert "--capubana-cada" in escena.CAPUBANA["cadencia"]
    assert "seis momentos" in escena.CAPUBANA["que_pasa_ese_dia"]
    assert escena.CAPUBANA["fuente"]
