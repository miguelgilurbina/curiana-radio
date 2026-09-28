"""«La etiqueta manda» (Miguel, 2026-09-18): las voces de la esfera no
circulan por el motor con la grafía castellana.

La decisión, voz a voz y con su cita, está en
`6-fusion/descastellanizar_esfera_2026-09-18.yaml`; las cifras de aquí salen
de `6-fusion/scripts/medir_descastellanizar_esfera.py`.

Lo que estos tests vigilan:
  · la tabla sólo apunta a claves que existen, con familia de la esfera;
  · [Voces de fuera] no enseña ninguna clave marcada castellana, y lo que
    conserva una marca está DECLARADO `se-queda`;
  · `save_loanword_uses` normaliza `word` y guarda `forma_dicha`;
  · el scorer no se movió: `prestamos_de_esfera` sigue devolviendo la clave
    castellana, y `score`/`pct_*` valen lo de antes del cambio.
"""

import curiana_lexicon as L
from curiana_database import (
    CurianaDB,
    CurianaDBMock,
    normalize_source_language,
)


def _familia(clave):
    return normalize_source_language(L.VOCABULARIO_BASE[clave].get("fuente", ""))


# ── La tabla ──────────────────────────────────────────────────────────

def test_la_tabla_solo_apunta_a_claves_que_existen_y_son_de_la_esfera():
    """Ni una entrada nueva: la fila une dos claves que YA están en el lexicón,
    las dos con `fuente` de la esfera de contacto."""
    assert L.FORMA_DE_LA_ESFERA, "la tabla no puede quedarse vacía sin decidirlo"
    for castellana, indigena in L.FORMA_DE_LA_ESFERA.items():
        assert castellana in L.VOCABULARIO_BASE, castellana
        assert indigena in L.VOCABULARIO_BASE, indigena
        assert castellana != indigena
        assert _familia(castellana) in L.ESFERA_DE_CONTACTO, castellana
        assert _familia(indigena) in L.ESFERA_DE_CONTACTO, indigena


def test_normalizar_no_mueve_la_lengua_de_la_voz():
    """`source_language` se calcula sobre la forma de la esfera: si las dos
    claves del par no compartieran familia, la tabla estaría reescribiendo la
    lengua de un hecho observado."""
    for castellana, indigena in L.FORMA_DE_LA_ESFERA.items():
        assert _familia(castellana) == _familia(indigena), castellana


def test_las_que_esperan_a_miguel_existen_y_no_tienen_gemela_aplicada():
    for clave in L.SIN_FORMA_DE_LA_ESFERA:
        assert clave in L.VOCABULARIO_BASE, clave
        assert clave not in L.FORMA_DE_LA_ESFERA, clave
        assert _familia(clave) in L.ESFERA_DE_CONTACTO, clave


def test_forma_de_la_esfera_respeta_la_morfologia_caquetia():
    """`ta-casabe` es la lengua haciendo algo con la raíz ajena (13 de 13 usos
    con morfología caen dentro de la frase caquetía, medición 2026-09-17): el
    posesivo se conserva y la raíz se normaliza."""
    assert L.forma_de_la_esfera("casabe") == "cazabi"
    assert L.forma_de_la_esfera("ta-casabe") == "ta-cazabi"
    assert L.forma_de_la_esfera("ka-casabe") == "ka-cazabi"
    assert L.forma_de_la_esfera("watapana") == "watapana"
    assert L.forma_de_la_esfera("ta-watapana") == "ta-watapana"


def test_marcas_castellanas_no_confunde_el_digrafo_ni_la_etiqueta_de_lengua():
    """⟨ch⟩ es dígrafo en todas las ortografías del repo, y la etiqueta con que
    el lexicón desambigua homógrafos no es parte de la voz."""
    assert L.marcas_castellanas("maíz") == ["tilde", "z"]
    assert L.marcas_castellanas("cacique") == ["qu", "c"]
    assert L.marcas_castellanas("chighe") == []
    assert L.marcas_castellanas("keichare") == []
    assert L.marcas_castellanas("kanawa-caribe") == []
    assert L.marcas_castellanas("watapana") == []


# ── [Voces de fuera] ──────────────────────────────────────────────────

def test_voces_de_fuera_no_ensena_ninguna_clave_con_grafia_castellana():
    """Las 43 candidatas (50 antes del 2026-09-18): ninguna clave decidida
    castellana sale, y toda forma que conserve una marca está declarada."""
    candidatas = L.voces_de_fuera_posibles()
    formas = [f for _p, f, _g, _fam in candidatas]
    assert len(formas) == len(set(formas)), "una voz no sale dos veces"

    decididas_castellanas = set(L.FORMA_DE_LA_ESFERA) | set(L.SIN_FORMA_DE_LA_ESFERA)
    fuera = sorted(set(formas) & decididas_castellanas)
    assert not fuera, f"[Voces de fuera] enseña grafía castellana: {fuera}"

    sin_declarar = sorted(f for f in formas
                          if L.marcas_castellanas(f)
                          and f not in L.SE_QUEDA_CON_SU_GRAFIA)
    assert not sin_declarar, (
        "voces de la esfera con marca castellana sin decidir: "
        f"{sin_declarar} — decidirlas en 6-fusion/descastellanizar_esfera_2026-09-18.yaml")


def test_las_gemelas_si_se_ensenan_y_el_bloque_las_escribe():
    """El bloque decía «maíz = planta de maíz» y ahora dice «maisi = …»."""
    import random
    formas = {f for _p, f, _g, _fam in L.voces_de_fuera_posibles()}
    # `cacike` dejó de enseñarse el 2026-09-24 (dp.1.04: llegó en boca del
    # español); las gemelas que siguen se enseñan por su forma indígena.
    assert {"maisi", "cazabi", "bohio"} <= formas
    assert "cacike" not in formas

    random.seed(20260918)
    bloque = L.prompt_voces_de_fuera(n=60)
    assert bloque.startswith("[Voces de fuera")
    for castellana in L.FORMA_DE_LA_ESFERA:
        assert f"{castellana} =" not in bloque, castellana
    for castellana in L.SIN_FORMA_DE_LA_ESFERA:
        assert f"{castellana} =" not in bloque, castellana


def test_el_catalogo_no_pierde_voces_por_accidente():
    """Sólo se caen las que la decisión dejó sin gemela: las otras dos claves
    que salen (`bohio`, `cacike`) colapsan con su par y su VOZ sigue estando."""
    formas = {f for _p, f, _g, _fam in L.voces_de_fuera_posibles()}
    # 43 → 44 el 2026-09-22 (db.2): `datihao` pasó de caquetío-atestiguado a
    # `taíno` —en Oviedo sólo aparece en San Juan— y con eso entra en la esfera.
    # Es la consecuencia declarada de la decisión, no una voz perdida o ganada
    # por accidente.
    # 44 → 42 el 2026-09-23 (db.3): las `taíno-reconstruido` se archivaron —eran
    # lokono con otra grafía— y dos de ellas salían en el bloque: `akcicyaa`
    # 'espíritu vital' y `wagulo` 'tortuga'. Las otras siete eran de categorías
    # que no se prestan (cuerpo, gramática). `daca` se queda en el lexicón como
    # taíno 'yo', que tampoco se presta.
    # 42 → 44 el 2026-09-23 (tf.0): `baperon` y `raporon` 'calabaza con cal'
    # pasaron de caquetío-atestiguado a `caribe-pemeno` —en el cuerpo de
    # Oviedo (t. II pp. 286 y 294) son de los pemenos de la laguna, y «(Lengua
    # de Venezuela)» es del editor, como en `datihao`—, y el caribe continental
    # es esfera. El mismo día `cohiba` se archivó y entró `cohoba` (tf.6):
    # una sale y otra entra, el total no se mueve por eso.
    # 44 → 42 el 2026-09-24 (dp.1.04 de #222, «Ok a todo»): `cacike` y
    # `naboria`, las que Oliver nombra como traídas por el español desde La
    # Española, dejan de enseñarse (LLEGARON_CON_EL_ESPANOL). El scorer no se toca.
    assert len(formas) == 42
    assert not {"cacike", "naboria"} & formas
    assert "datihao" in formas
    assert {"baperon", "raporon", "cohoba"} <= formas
    assert "cohiba" not in formas
    assert not {"akcicyaa", "wagulo"} & formas
    for clave in L.SIN_FORMA_DE_LA_ESFERA:
        assert clave not in formas


# ── La base ───────────────────────────────────────────────────────────

class _ClienteQueGraba:
    def __init__(self):
        self.inserts = []

    def table(self, nombre):
        cliente = self

        class _Tabla:
            def insert(self, rows):
                cliente.inserts.append((nombre, rows))
                return self

            def execute(self):
                return None

        return _Tabla()


def test_save_loanword_uses_normaliza_y_guarda_la_forma_dicha():
    """`word` lleva la forma de la esfera y `forma_dicha` lo que el agente
    escribió. Migración 20260918000000."""
    db = CurianaDB.__new__(CurianaDB)
    db.client = _ClienteQueGraba()
    n = db.save_loanword_uses(response_id="r", run_id="run", turn_id="t",
                              agent_name="Manaure", tier=1, day=3, turn_num=2,
                              words=["casabe", "ta-casabe", "watapana"])
    assert n == 3
    (tabla, filas), = db.client.inserts
    assert tabla == "loanword_uses"
    assert [f["word"] for f in filas] == ["cazabi", "ta-cazabi", "watapana"]
    assert [f["forma_dicha"] for f in filas] == ["casabe", "ta-casabe", "watapana"]
    assert [f["source_language"] for f in filas] == ["taíno", "taíno", "caribe-continental"]
    assert all((f["tier"], f["day"], f["turn_num"]) == (1, 3, 2) for f in filas)


def test_el_mock_construye_exactamente_las_mismas_filas():
    """Si el mock divergiera, los tests dejarían de decir nada de lo que se
    guarda de verdad (misma garantía que `filas_de_presencias`)."""
    db = CurianaDB.__new__(CurianaDB)
    db.client = _ClienteQueGraba()
    argumentos = dict(response_id="r", run_id="run", turn_id="t",
                      agent_name="Manaure", tier=2, day=1, turn_num=6,
                      words=["maíz", "yuca"])
    db.save_loanword_uses(**argumentos)
    (_tabla, filas), = db.client.inserts

    mock = CurianaDBMock()
    assert mock.save_loanword_uses(**argumentos) == 2
    assert mock.loanwords == filas
    assert [f["word"] for f in mock.loanwords] == ["maisi", "yuca"]
    assert [f["forma_dicha"] for f in mock.loanwords] == ["maíz", "yuca"]
    assert CurianaDBMock().save_loanword_uses(**{**argumentos, "words": []}) == 0


# ── El scorer no se toca ──────────────────────────────────────────────

# Medido con `HEAD:curiana_sim/curiana_lexicon.py` cargado como módulo aparte,
# frase a frase, por 6-fusion/scripts/medir_descastellanizar_esfera.py: 0 de 8
# frases cambian en score, densidad, pct_caquetio_especifico, otro_arahuaco,
# espanol_funcional, palabras_caquetias, palabras_arahuacas,
# palabras_otro_arahuaco, aspectos_usados ni prestamos_de_esfera. Estas cuatro
# son las del informe; si el número se mueve, el instrumento se movió.
# ⚠️ Tanda final (2026-09-23, D11 fase 3): el instrumento SE MOVIÓ, y a
# propósito — `-ka`/`-ni` dejan de contar como aspecto (el detector se
# sustituyó) y `taya`, `pia` y `wana` se archivaron. Las cuatro frases son las
# mismas; los números, los del scorer de hoy (antes: 7,2 · 6,1 · 8,4 · 8,5).
# Lo que este test vigila sigue igual: `prestamos_de_esfera` devuelve la
# clave castellana y la normalización no mueve el score.
# ⚠️ Tanda de las hermanas (2026-09-24): SE MOVIÓ otra vez, y también a
# propósito — `wara`, `amana` y `naa` se archivaron (el núcleo sale ahora del
# lokono y del habla de mujeres kalinago). Mismas frases; números de hoy
# (antes: 6,2 · 6,1 · 5,1 · 6,4). Los préstamos de la esfera no se movieron.
ANTES = [
    ("Casabe kaa-ni wara amana-ni", 5.1, 0.500, 0.250, ["casabe"]),
    ("Maíz, yuca ta-kana", 6.1, 1.000, 0.333, ["maíz", "yuca"]),
    ("Taya naa-ka casabe wana-ni, ta-casabe para-ko", 3.3, 0.333, 0.000,
     ["casabe", "ta-casabe"]),
    ("Pia naa-ka maisi, cazabi kaa-ni wara", 5.1, 0.500, 0.167,
     ["maisi", "cazabi"]),
]


def test_el_scorer_devuelve_exactamente_lo_de_antes():
    lex = L.LexicoComunitario()
    for frase, score, densidad, pct, prestamos in ANTES:
        r = L.score_linguistico(frase, lex)
        assert r["score"] == score, frase
        assert round(r["densidad"], 3) == densidad, frase
        assert round(r["pct_caquetio_especifico"], 3) == pct, frase
        # La clave CASTELLANA es la que el scorer reconoce y la que devuelve:
        # el agente escribe «casabe» y cuenta. Normalizar es cosa de guardar
        # y de leer, nunca de puntuar.
        assert r["prestamos_de_esfera"] == prestamos, frase


def test_las_capas_de_score_no_se_movieron():
    """Lo que cambia es lo que el agente VE, nunca con qué se le puntúa."""
    lex = L.LexicoComunitario()
    con_castellana = L.score_linguistico("Casabe kaa-ni wara amana-ni", lex)
    con_indigena = L.score_linguistico("Cazabi kaa-ni wara amana-ni", lex)
    assert con_castellana["score"] == con_indigena["score"]
    assert con_castellana["densidad"] == con_indigena["densidad"]
    assert con_castellana["prestamos_de_esfera"] == ["casabe"]
    assert con_indigena["prestamos_de_esfera"] == ["cazabi"]
