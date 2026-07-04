"""Tests del motor de koiné: idiolectos, métricas de convergencia,
competencia léxica y campo léxico (curiana_koine.py)."""

from curiana_koine import (
    IdiolectoAgente,
    CampoLexico,
    CompetenciaLexica,
    distancia_idiolectal,
    emocionar_de,
)


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
