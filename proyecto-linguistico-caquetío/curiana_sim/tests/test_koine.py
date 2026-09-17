"""Tests del motor de koiné: idiolectos, métricas de convergencia,
competencia léxica y campo léxico (curiana_koine.py)."""

import json
import os
import subprocess
import sys

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
        b.registrar(["biro", "habo", "kanoa", "arima", "bara"])
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


# ══════════════════════════════════════════════════════════════════════
# LA PRE-CARGA DE IDIOLECTOS (2026-09-16)
# ══════════════════════════════════════════════════════════════════════
# Medido por analizar_nodos.py al cerrar el día 3 de la era 2: `FORMAS_SEED` y
# `EMOCIONAR_SEED` están indexados por los nombres de la ERA 1 y la campaña de
# antropónimos renombró a 60 de 63 agentes, así que sólo Manaure encontraba su
# semilla y 62 de 63 arrancaban con el MISMO vector. DISENO_KOINE §4: «sin esta
# pre-carga, todos arrancan iguales y convergencia no significa nada».
#
# La era 2 se comprueba en un subproceso, como en test_eventos_era2.py: el
# elenco se decide al importar curiana_agents, desde CURIANA_ELENCO.

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _medir_era2(semilla=None, codigo_extra=""):
    """Mide las semillas de idiolecto del elenco de la era 2, en su elenco."""
    codigo = (
        "import json\n"
        "import curiana_agents as A\n"
        "from curiana_koine import (emocionar_de, fijar_semilla, formas_seed_de,\n"
        "                           formas_semilla, nombre_era1)\n"
        f"fijar_semilla({semilla!r})\n"
        "sem = {}\n"
        "escritas = []\n"
        "for n, a in A.ALL_AGENTS.items():\n"
        "    sem[n] = formas_semilla(n, emocionar_de(n, a.get('etnia')))\n"
        "    if formas_seed_de(n):\n"
        "        escritas.append(n)\n"
        "salida = {'total': len(A.ALL_AGENTS), 'semillas': sem,\n"
        "          'escritas': sorted(escritas), 'mundo': A.MUNDO,\n"
        "          'viejo_de': {n: nombre_era1(n) for n in A.ALL_AGENTS}}\n"
        + codigo_extra +
        "print(json.dumps(salida, ensure_ascii=False))\n"
    )
    env = dict(os.environ, CURIANA_ELENCO="era2", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-c", codigo], cwd=SIM, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_la_era_2_arranca_con_63_semillas_distintas_por_pares():
    """La precondición de que «convergencia» signifique algo: dos agentes
    distintos no pueden arrancar con el mismo vector. Medido ANTES del
    arreglo: 2 vectores distintos de 63 (62 compartían `_NUCLEO_FALLBACK`)."""
    d = _medir_era2()
    assert d["mundo"] == "PARAGUANÁ" and d["total"] == 63
    vectores = {n: tuple(sorted(v)) for n, v in d["semillas"].items()}
    repetidos = {}
    for n, v in vectores.items():
        repetidos.setdefault(v, []).append(n)
    choques = {v: ns for v, ns in repetidos.items() if len(ns) > 1}
    assert not choques, f"agentes que arrancan iguales: {list(choques.values())}"
    assert len(set(vectores.values())) == 63
    # Y ninguno arranca vacío ni con una sola forma.
    assert all(len(v) >= 5 for v in d["semillas"].values())


def test_la_semilla_de_manaure_es_la_de_siempre_y_diez_mas_llegan_por_alias():
    """Manaure conserva su nombre, así que su semilla no puede moverse. Los
    otros diez que tenían una escrita en la era 1 la recuperan por
    `ALIAS_ERA1` (Nubiri-sha → Karebe, Shaboro → Sawaka, Korie-ko →
    Patapati…): son 11 de 63."""
    from curiana_koine import FORMAS_SEED

    d = _medir_era2()
    assert d["semillas"]["Manaure"] == list(dict.fromkeys(FORMAS_SEED["Manaure"]))
    assert len(d["escritas"]) == 11, d["escritas"]
    for nuevo in d["escritas"]:
        viejo = d["viejo_de"][nuevo] or nuevo
        assert d["semillas"][nuevo] == list(dict.fromkeys(FORMAS_SEED[viejo])), nuevo


def test_la_semilla_derivada_es_determinista_entre_procesos():
    """El sorteo va con blake2b sobre (semilla del run, nombre), no con
    `hash()` —salado por proceso con PYTHONHASHSEED— ni con el RNG global,
    que el motor comparte con eventos y muestreo. Dos procesos con la misma
    semilla tienen que dar la misma pre-carga; con otra semilla, no."""
    a = _medir_era2(semilla=1)
    b = _medir_era2(semilla=1)
    c = _medir_era2(semilla=2)
    assert a["semillas"] == b["semillas"]
    distintas = [n for n in a["semillas"] if a["semillas"][n] != c["semillas"][n]]
    # Las 11 escritas no dependen de la semilla; las 52 derivadas sí.
    assert len(distintas) >= 40, f"la semilla del run casi no mueve nada: {len(distintas)}"
    assert not (set(distintas) & set(a["escritas"])), "una semilla ESCRITA se movió"


def test_la_semilla_derivada_no_siembra_nombres_del_elenco():
    """49 de los 63 nombres de la era 2 son homógrafos de una clave del
    lexicón (`karebe` cucharón / Karebe la esposa principal). El bloque
    «sueles decir: …» del prompt sale de aquí: sembrar uno le diría al agente
    que suele decir el nombre de un vecino."""
    d = _medir_era2()
    escritas = set(d["escritas"])
    nombres = {n.lower() for n in d["semillas"]} | {
        (v or "").lower() for v in d["viejo_de"].values() if v}
    for agente, formas in d["semillas"].items():
        if agente in escritas:
            continue          # las escritas son canon de la era 1, no se tocan
        malas = [f for f in formas if f.split("-")[0].lower() in nombres]
        assert not malas, f"{agente} arranca diciendo nombres: {malas}"


def test_la_semilla_derivada_no_toca_la_capa_hipotetica():
    """35 de las 38 voces hipotéticas son formas que el proyecto acuñó para la
    simulación, y el perfil `era2` las esconde a propósito. Sembrarlas
    adelantaría justo lo que la era 2 quiere ver acuñar."""
    d = _medir_era2()
    from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica

    escritas = set(d["escritas"])
    for agente, formas in d["semillas"].items():
        if agente in escritas:
            continue
        for f in formas:
            datos = VOCABULARIO_BASE.get(f) or VOCABULARIO_BASE.get(f.split("-")[0])
            if datos is None:
                continue
            assert capa_epistemica(datos.get("fuente", "")) != "caquetío-hipotético", \
                f"{agente} arranca con la hipotética {f}"


def test_la_era_1_no_cambia_byte_a_byte():
    """El arreglo del alias y la derivación no tocan la era 1: `ALIAS_ERA1`
    está vacío allí (resolver es la identidad) y la derivación pide `oficio`,
    campo que sólo trae el módulo generado de la era 2. Las 20 semillas
    escritas salen tal cual, y los 40 agentes sin ella siguen en el núcleo
    compartido — que es por lo que la era 1 sólo tiene 21 vectores de 60."""
    import curiana_agents as A
    from curiana_koine import (
        _ASPECTO_SUFIJO, _NUCLEO_FALLBACK, FORMAS_SEED, formas_semilla,
        nombre_era1,
    )

    assert A.ELENCO == "era1" and A.ALIAS_ERA1 == {}
    for agente, formas in FORMAS_SEED.items():
        assert nombre_era1(agente) is None
        assert formas_semilla(agente, emocionar_de(agente)) == \
            list(dict.fromkeys(formas)), agente

    sin_semilla = [n for n in A.ALL_AGENTS if n not in FORMAS_SEED]
    assert len(sin_semilla) == 40
    for agente in sin_semilla:
        emo = emocionar_de(agente, A.ALL_AGENTS[agente].get("etnia"))
        suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", "continuativo"), "-ni")
        assert formas_semilla(agente, emo) == \
            _NUCLEO_FALLBACK + [f"naa{suf}", f"wana{suf}"], agente

    vectores = {tuple(sorted(formas_semilla(n, emocionar_de(n, a.get("etnia")))))
                for n, a in A.ALL_AGENTS.items()}
    assert len(vectores) == 21


def test_continuar_no_recupera_una_pre_carga_que_nunca_hubo():
    """`cargar_koine` reconstruye con `peso_semilla=0` a propósito (las
    frecuencias guardadas ya traen la semilla), así que una cadena que arrancó
    sin pre-carga no la gana por seguir encadenando. El motor lo mide y lo
    dice; la salida es re-correr desde el día 1."""
    from curiana_koine import agentes_sin_precarga

    agentes = {"Manaure": {"etnia": "caquetío"}, "Shaboro": {"etnia": "caquetío"}}
    # Como quedaba una cadena vieja: el núcleo compartido y lo que habló.
    viejos = {}
    for nm in agentes:
        idio = IdiolectoAgente(nm, {}, peso_semilla=0)
        idio.frecuencias.update(["taya", "pia", "nüma", "arima"])
        viejos[nm] = idio
    assert sorted(agentes_sin_precarga(viejos, agentes)) == ["Manaure", "Shaboro"]

    nuevos = {nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia")))
              for nm, a in agentes.items()}
    assert agentes_sin_precarga(nuevos, agentes) == []
