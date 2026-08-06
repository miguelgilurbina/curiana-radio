"""Tests del motor de koiné: idiolectos, métricas de convergencia,
competencia léxica y campo léxico (curiana_koine.py)."""

from curiana_koine import (
    IdiolectoAgente,
    CampoLexico,
    CompetenciaLexica,
    distancia_idiolectal,
    emocionar_de,
    veredicto_convergencia,
)

# Series de convergencia emergente reales (koine_metrics) de los dos brazos del
# experimento 2026-07-06 — la evidencia de que el veredicto binario engañaba.
SERIE_NORMAL_038 = [
    0.6997, 0.6253, 0.6069, 0.5634, 0.533, 0.5161, 0.509, 0.5047, 0.5413, 0.5363,
    0.5346, 0.5721, 0.5682, 0.5858, 0.6321, 0.6392, 0.6404, 0.6216, 0.6195, 0.5934,
    0.5907, 0.5917, 0.5835, 0.5791, 0.5763, 0.5792, 0.5842, 0.5823, 0.5714, 0.5746,
]
SERIE_ABLACION_BDC = [
    0.6957, 0.6758, 0.7118, 0.6715, 0.6521, 0.6349, 0.6258, 0.6404, 0.6217, 0.6807,
    0.6729, 0.6984, 0.6933, 0.6855, 0.6696, 0.6514, 0.6491, 0.649, 0.6461, 0.6456,
    0.6423, 0.6413, 0.6407, 0.6427, 0.6423, 0.6432, 0.642, 0.6443, 0.6528, 0.6499,
]


def _idios(nombres):
    return {nm: IdiolectoAgente(nm, emocionar_de(nm)) for nm in nombres}


# ── Métrica acumulada (compatibilidad histórica) ──────────────────────

def test_distancia_acumulada_converge_con_uso_comun():
    idios = _idios(["Manaure", "Shaboro", "Dara-ko"])
    d0 = distancia_idiolectal(idios)
    comunes = ["taya", "wana-ka", "biro", "kali", "naa-da"]
    for _ in range(30):
        for idio in idios.values():
            idio.registrar(comunes)
    d1 = distancia_idiolectal(idios)
    assert d0 is not None and d1 is not None
    assert d1 < d0


def test_distancia_none_con_datos_insuficientes():
    idios = _idios(["Manaure"])  # un solo agente: no hay pares
    assert distancia_idiolectal(idios) is None
    # ventana sin habla registrada: nadie tiene vector reciente
    idios2 = _idios(["Manaure", "Shaboro"])
    assert distancia_idiolectal(idios2, ventana=True) is None


# ── Veredicto de convergencia: plateau ≠ convergencia sostenida ──────

def _puntos(serie):
    return [(i + 1, v) for i, v in enumerate(serie)]


def test_veredicto_normal_converge_sostenido():
    """El run normal baja en total Y sigue bajando en el último tercio."""
    codigo, _ = veredicto_convergencia(_puntos(SERIE_NORMAL_038))
    assert codigo == "converge"


def test_veredicto_ablacion_es_plateau_no_converge():
    """El run de ablación baja al inicio y se estanca — el binario decía
    'CONVERGE' porque fin < inicio; el nuevo veredicto lo llama plateau."""
    codigo, _ = veredicto_convergencia(_puntos(SERIE_ABLACION_BDC))
    assert codigo == "plateau"
    # sanity: el binario viejo (fin < inicio) SÍ daba positivo — por eso engañaba
    assert SERIE_ABLACION_BDC[-1] < SERIE_ABLACION_BDC[0]


def test_veredicto_diverge_si_sube():
    codigo, _ = veredicto_convergencia([(1, 0.4), (2, 0.5), (3, 0.6)])
    assert codigo == "diverge"


def test_veredicto_insuficiente_con_un_punto():
    codigo, _ = veredicto_convergencia([(1, 0.5)])
    assert codigo == "insuficiente"


# ── Métrica por ventana: mide el habla RECIENTE, no el acumulado ─────

def test_ventana_ignora_semillas():
    """Las formas-semilla pre-cargadas no cuentan en el vector reciente."""
    idio = IdiolectoAgente("Manaure", emocionar_de("Manaure"))
    assert len(idio.vector()) > 0          # semillas presentes en acumulado
    assert len(idio.vector_reciente()) == 0  # pero no en la ventana


def test_ventana_refleja_habla_actual_no_historia():
    """Dos agentes con historia distinta pero habla reciente idéntica deben
    verse CERCA en ventana aunque el acumulado los separe."""
    a = IdiolectoAgente("A", peso_semilla=0)
    b = IdiolectoAgente("B", peso_semilla=0)
    # Historia divergente (más larga que la ventana)
    for _ in range(IdiolectoAgente.VENTANA_TURNOS + 5):
        a.registrar(["kali", "kasha", "urari", "piache", "barsure"])
        b.registrar(["biro", "habo", "canoa", "arima", "bara"])
    # Habla reciente idéntica (llena la ventana completa)
    comunes = ["taya", "naa-ka", "wana-ni", "duna", "kuru"]
    for _ in range(IdiolectoAgente.VENTANA_TURNOS):
        a.registrar(comunes)
        b.registrar(comunes)
    idios = {"A": a, "B": b}
    d_ventana = distancia_idiolectal(idios, ventana=True)
    d_acum = distancia_idiolectal(idios)
    assert d_ventana == 0.0                 # habla actual idéntica
    assert d_acum > d_ventana               # el acumulado aún arrastra la historia


def test_excluir_deja_solo_formas_emergentes():
    base = {"taya", "naa-ka", "wana-ni", "duna", "kuru"}
    a = IdiolectoAgente("A", peso_semilla=0)
    b = IdiolectoAgente("B", peso_semilla=0)
    for _ in range(5):
        # comparten TODO el vocabulario base, difieren solo en neologismos
        a.registrar(list(base) + ["kali-dusha", "sima-bana", "buco-rua"])
        b.registrar(list(base) + ["suka-wana", "habo-kata", "dali-nu"])
    idios = {"A": a, "B": b}
    d_total = distancia_idiolectal(idios, ventana=True)
    d_emergente = distancia_idiolectal(idios, ventana=True, excluir=base, min_formas=3)
    # sobre formas emergentes los agentes son totalmente disjuntos;
    # el vocabulario base compartido enmascara esa divergencia en la total
    assert d_emergente == 1.0
    assert d_total < d_emergente


def test_ventana_expira_formas_viejas():
    idio = IdiolectoAgente("A", peso_semilla=0)
    idio.registrar(["forma-vieja"])
    for _ in range(IdiolectoAgente.VENTANA_TURNOS):
        idio.registrar(["forma-nueva"])
    reciente = idio.vector_reciente()
    assert "forma-vieja" not in reciente
    assert reciente["forma-nueva"] == IdiolectoAgente.VENTANA_TURNOS
    # el acumulado sí la conserva (entrenchment no expira)
    assert idio.vector()["forma-vieja"] == 1


# ── Competencia léxica (fijación por concepto) ────────────────────────

def test_competencia_fija_la_variante_dominante():
    comp = CompetenciaLexica(soporte_minimo=2.0)
    comp.activar("cometa", "estrella con cola")
    comp.proponer("cometa", "kali-dusha", "Manaure")
    comp.proponer("cometa", "suka-wana", "Tariwa")
    for _ in range(4):
        comp.registrar_uso("kali-dusha", "Shaboro")
    fijadas = comp.evaluar_fijacion(dia=5)
    assert ("cometa", "kali-dusha") in fijadas
    assert comp.diccionario_koine()["cometa"]["forma"] == "kali-dusha"


def test_competencia_no_fija_sin_rivales():
    """Con una sola variante no hay competencia que resolver."""
    comp = CompetenciaLexica(soporte_minimo=1.0)
    comp.activar("eclipse", "el sol se oscurece")
    comp.proponer("eclipse", "kali-suka", "Manaure")
    for _ in range(10):
        comp.registrar_uso("kali-suka", "Shaboro")
    assert comp.evaluar_fijacion(dia=3) == []


def test_competencia_ignora_uso_tras_fijacion():
    comp = CompetenciaLexica(soporte_minimo=1.0, umbral_fijacion=0.5)
    comp.activar("c", "algo")
    comp.proponer("c", "forma-a", "Manaure")
    comp.proponer("c", "forma-b", "Tariwa")
    comp.registrar_uso("forma-a", "Shaboro")
    assert comp.evaluar_fijacion(dia=1)
    soporte_antes = comp.referentes["c"]["variantes"]["forma-b"]
    comp.registrar_uso("forma-b", "Shaboro")   # ya fijada: no debe sumar
    assert comp.referentes["c"]["variantes"]["forma-b"] == soporte_antes


# ── Campo léxico (rich-get-richer + decaimiento) ──────────────────────

def test_campo_decae_y_descarta():
    campo = CampoLexico(decaimiento=0.5)
    campo.registrar(["biro"], incremento=1.0)
    campo.registrar(["kali"], incremento=0.08)
    campo.decaer()
    assert campo.peso("biro") == 0.5
    assert campo.peso("kali") == 0.0   # 0.04 < umbral 0.05: la forma muere


# ── El motor no puede sembrar palabras que ya salieron del habla ──────

def test_formas_seed_solo_usa_palabras_del_lexicon():
    """`FORMAS_SEED` siembra el idiolecto de cada agente desde el día 1. Si
    siembra una forma que no está en `VOCABULARIO_BASE`, el motor le está
    enseñando a los agentes una palabra que el proyecto ya descartó — y
    `score_linguistico()` ni siquiera se la va a contar.

    Es lo que pasó con `piache`: D10 la sacó del habla por ser voz caribe
    (Alvarado p.248, corroborado por Jahn 1927 n.28), y `FORMAS_SEED` siguió
    sembrándosela a Shaboro y Buio-sha. La reemplaza `boratio`, que es la forma
    caquetía atestiguada del mismo oficio.
    """
    import re

    from curiana_koine import FORMAS_SEED
    from curiana_lexicon import VOCABULARIO_BASE

    huerfanas = {}
    for agente, formas in FORMAS_SEED.items():
        for forma in formas:
            # Las formas con aspecto (`wana-ka`) se validan por su raíz.
            raiz = re.split(r"-", forma)[0]
            if forma not in VOCABULARIO_BASE and raiz not in VOCABULARIO_BASE:
                huerfanas.setdefault(forma, []).append(agente)

    assert not huerfanas, (
        "FORMAS_SEED siembra formas que no están en VOCABULARIO_BASE: "
        + "; ".join(f"{f} ({', '.join(a)})" for f, a in sorted(huerfanas.items())))


def test_ningun_referente_novedoso_menciona_piache():
    """Los `desc` de REFERENTES_NOVEDOSOS entran al prompt vía
    `competencia.activar()`, así que ponen sus palabras delante de los agentes.
    `piache` salió del habla: tampoco puede colarse por ahí."""
    from curiana_koine import REFERENTES_NOVEDOSOS

    con_piache = [r["id"] for r in REFERENTES_NOVEDOSOS if "piache" in r["desc"]]
    assert not con_piache, f"referentes que aún dicen 'piache': {con_piache}"
