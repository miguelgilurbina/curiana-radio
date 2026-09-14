"""Tests del motor para la era 2 (decisiones de Miguel, 2026-09-14).

  - «que todos los agentes hablen»: roster `todos` sin foráneos, tier 3
    incluidos, con una ventana de 10-12 por turno.
  - «hay que arreglar el muestreo»: reparto proporcional por cubo, sin que el
    cubo `sust` (216 voces) reciba 3 lugares por prompt.
  - «sí o sí todos los afijos atestiguados se enseñan»: REGLAS_ZAVALA y
    `-bacoa` en las dos plantillas.
  - «un día con muchos más turnos»: turnos_por_dia en el estado.
  - «que los agentes puedan acordarse de lo que hicieron»: memoria del día y
    persistencia de la koiné para --continuar.
  - Lo que las plantillas enseñan no cuenta como koiné (bitácora db946685).

Sin LLM ni Supabase: call_agent y director_narrate se sustituyen.
"""
from collections import Counter

import pytest

import curiana_orchestrator_v2 as orch
from curiana_koine import CampoLexico, IdiolectoAgente, cargar_koine, guardar_koine
from curiana_lexicon import (
    AFIJOS_ATESTIGUADOS,
    LexicoComunitario,
    REGLAS_ZAVALA,
    formas_en_texto,
    muestra_caquetio_dinamica,
    prompt_reglas_breve,
    prompt_reglas_completo,
    repartir_cuotas,
)
from curiana_observer import ObserverAgent
from curiana_state import (
    MOMENTOS_DIA,
    ComunidadState,
    estado_inicial_test,
    momento_de_turno,
)

RESPUESTA = "Taya wana-ka arima wara kari. [kuru-bacoa: kuru+-bacoa = la arboleda]."


class _FakeClient:
    pass


@pytest.fixture
def sim(monkeypatch):
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: RESPUESTA)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    monkeypatch.setattr(orch, "director_select_event", lambda state: None)
    lexico = LexicoComunitario()
    return {
        "client": _FakeClient(),
        "state": estado_inicial_test(),
        "memory": orch.AgentMemory(),
        "lexico": lexico,
        "observer": ObserverAgent(_FakeClient(), lexico),
    }


def _correr(sim, turnos, **kw):
    hablaron = Counter()
    por_turno = []
    for _ in range(turnos):
        inter = orch.run_turn(
            sim["client"], sim["state"], sim["memory"], sim["lexico"],
            sim["observer"], verbose=False, db=None, run_id=None, **kw,
        )
        por_turno.append(len(inter))
        for i in inter:
            hablaron[i["agent"]] += 1
    return hablaron, por_turno


# ── el calendario: turnos por día ─────────────────────────────────────

def test_dos_turnos_por_dia_siguen_siendo_amanecer_y_tarde():
    """Regresión: la era 1 corrió con amanecer/tarde y así se queda por defecto."""
    s = estado_inicial_test()
    assert s.turnos_por_dia == 2 and s.momento == "amanecer"
    s.avanzar_turno()
    assert (s.dia, s.turno, s.momento) == (1, 2, "tarde")
    s.avanzar_turno()
    assert (s.dia, s.turno, s.momento) == (2, 1, "amanecer")


def test_seis_turnos_recorren_los_seis_momentos_y_cierran_el_dia():
    s = ComunidadState(turnos_por_dia=6)
    vistos = [s.momento]
    for _ in range(5):
        s.avanzar_turno()
        vistos.append(s.momento)
    assert vistos == MOMENTOS_DIA and s.dia == 1
    s.avanzar_turno()
    assert (s.dia, s.turno, s.momento) == (2, 1, "amanecer")


def test_momento_de_turno_reparte_a_espacios_iguales():
    assert [momento_de_turno(t, 2) for t in (1, 2)] == ["amanecer", "tarde"]
    assert [momento_de_turno(t, 3) for t in (1, 2, 3)] == ["amanecer", "mediodia", "anochecer"]
    assert [momento_de_turno(t, 6) for t in range(1, 7)] == MOMENTOS_DIA


def test_un_estado_guardado_sin_turnos_por_dia_carga_con_dos():
    """Los JSON de la era 1 no traen el campo: no pueden romper --continuar."""
    d = estado_inicial_test().to_dict()
    d.pop("turnos_por_dia"); d.pop("run_anterior")
    s = ComunidadState.from_dict(d)
    assert s.turnos_por_dia == 2 and s.run_anterior is None


# ── el roster: todos hablan, los foráneos no ──────────────────────────

def test_el_roster_todos_deja_fuera_a_los_foraneos_y_mete_a_los_tier_3():
    todos = orch.roster_de_habla("todos")
    etnias = {orch.ALL_AGENTS[a].get("etnia", "caquetío") for a in todos}
    assert not (etnias & orch.ETNIAS_FORANEAS), etnias & orch.ETNIAS_FORANEAS
    tier3 = [a for a in todos if orch.ALL_AGENTS[a].get("tier") == 3]
    assert tier3, "los tier 3 tienen que hablar"
    # Los caquetíos de Aruba y los mestizos son caquetíos: se quedan.
    assert "Kadushi" in todos and "Wata-ni" in todos
    assert "Marokoto-ni" not in todos and "Tariwa" not in todos


def test_el_roster_koine_es_el_de_la_era_1():
    assert orch.roster_de_habla("koine") == [a for a in orch.PARTICIPANTES_KOINE if a in orch.ALL_AGENTS]
    with pytest.raises(ValueError):
        orch.roster_de_habla("otro")


def test_con_doce_por_turno_hablan_doce_y_todos_hablan(sim):
    sim["state"].turnos_por_dia = 6
    roster = orch.roster_de_habla("todos")
    hablaron, por_turno = _correr(sim, turnos=6, agentes_por_turno=12, roster=roster)
    assert set(por_turno) == {12}, por_turno
    mudos = [a for a in roster if a not in hablaron]
    assert not mudos, f"en un día de 6 turnos × 12 quedaron mudos: {mudos}"
    # Un día de 72 voces sobre un roster menor: nadie habla más de dos veces.
    assert max(hablaron.values()) <= 2


def test_un_evento_completa_la_ventana_y_filtra_foraneos(sim, monkeypatch):
    evento = {
        "id": "prueba", "descripcion": "llegan visitantes",
        "agentes_involucrados": ["Manaure", "Marokoto-ni", "Tariwa"],
        "efecto": {},
    }
    monkeypatch.setattr(orch, "director_select_event", lambda state: evento)
    roster = orch.roster_de_habla("todos")
    hablaron, por_turno = _correr(sim, turnos=1, agentes_por_turno=10, roster=roster)
    assert por_turno == [10]
    assert "Manaure" in hablaron
    assert "Marokoto-ni" not in hablaron and "Tariwa" not in hablaron


def test_la_ventana_por_defecto_sigue_siendo_seis_sobre_koine(sim):
    hablaron, por_turno = _correr(sim, turnos=2)
    assert set(por_turno) == {6}
    assert set(hablaron) <= set(orch.roster_de_habla("koine"))


# ── el muestreo ───────────────────────────────────────────────────────

def test_repartir_cuotas_es_proporcional_con_minimo_y_tope():
    cuotas = repartir_cuotas({"sust": 216, "v_raiz": 75, "chico": 2, "uno": 1}, 50)
    assert sum(cuotas.values()) == 50
    assert cuotas["uno"] == 1 and cuotas["chico"] <= 2
    assert cuotas["sust"] > cuotas["v_raiz"] > cuotas["chico"]
    assert cuotas["sust"] >= 20


def test_repartir_cuotas_favorece_lo_relevante_y_no_pide_mas_de_lo_que_hay():
    sin = repartir_cuotas({"a": 50, "b": 50}, 20)
    con = repartir_cuotas({"a": 50, "b": 50}, 20, relevantes={"a"})
    assert con["a"] > sin["a"]
    corto = repartir_cuotas({"a": 3, "b": 3}, 50)
    assert corto == {"a": 3, "b": 3}


def _cuenta_por_cubo(muestra: str) -> Counter:
    c = Counter()
    for linea in muestra.splitlines()[1:]:
        cubo, _, resto = linea.strip().partition(":")
        c[cubo.strip().lower()] = len([x for x in resto.split(" · ") if x.strip()])
    return c


def test_la_muestra_respeta_el_presupuesto_y_saca_a_los_sustantivos_del_goteo():
    capas = frozenset({"caquetío-atestiguado", "caquetío-reconstruido", "caquetío-hipotético"})
    c = _cuenta_por_cubo(muestra_caquetio_dinamica(n_por_categoria=20, contexto="orilla pesca",
                                                   capas=capas, n_total=50))
    assert sum(c.values()) == 50
    # Antes: 3 de 216. Ahora el cubo grande pesa lo que mide.
    assert c["sust"] >= 10, c
    assert c["v_raiz"] >= 5, c


def test_toda_voz_visible_puede_salir_en_la_muestra():
    """Regresión: un modelo sobre 154 prompts estimaba 33 voces que no salían
    nunca. Con el reparto nuevo, en 200 muestras aparecen todas."""
    from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica
    capas = frozenset({"caquetío-atestiguado", "caquetío-reconstruido", "caquetío-hipotético"})
    visibles = {k for k, e in VOCABULARIO_BASE.items()
                if capa_epistemica(e.get("fuente", "")) in capas and (e.get("sig") or e.get("es"))}
    vistas = set()
    for _ in range(200):
        m = muestra_caquetio_dinamica(n_por_categoria=20, capas=capas, n_total=50)
        for linea in m.splitlines()[1:]:
            for item in linea.partition(":")[2].split(" · "):
                vistas.add(item.split(" (")[0].strip())
    faltan = visibles - vistas
    assert len(faltan) <= len(visibles) // 50, sorted(faltan)[:20]


# ── los afijos atestiguados ───────────────────────────────────────────

def test_todos_los_afijos_atestiguados_se_ensenan_en_las_dos_plantillas():
    completo, breve = prompt_reglas_completo(), prompt_reglas_breve()
    for afijo in list(REGLAS_ZAVALA) + ["-bacoa"]:
        assert afijo in completo, afijo
        assert afijo in breve, afijo
    assert set(AFIJOS_ATESTIGUADOS) == set(REGLAS_ZAVALA) | {"-bacoa"}


def test_las_desinencias_sin_valor_se_ensenan_como_tales():
    assert "cuyo valor nadie anotó" in prompt_reglas_completo()


def test_la_plantilla_tier_1_usa_las_formas_del_canon():
    """Auditoría 2026-09-14: buco, corie «choza», canoa, hamaca, conuco y piache
    no estaban en el lexicón con esa grafía o glosa; el scorer no las contaba."""
    p = prompt_reglas_completo()
    for vieja in ("buco (represa)", "corie (choza)", "piache (chamán)", "canoa (canoa)",
                  "hamaca (hamaca)", "conuco (huerto)", "ta-corie", "wa-buco", "buco-ana"):
        assert vieja not in p, vieja
    for nueva in ("buko (represa)", "korie (armadillo)", "boratio", "kanoa (canoa)",
                  "hamaka (hamaca)", "konuko (huerto)", "buko-ana"):
        assert nueva in p, nueva


# ── lo que la plantilla enseña no cuenta como koiné ───────────────────

def test_las_formas_de_las_plantillas_quedan_fuera_de_lo_emergente():
    for forma in ("ta-barsure", "wana-ka", "naba-ni", "kaa-ni", "naa-da", "sima-bana", "buko-ana"):
        assert forma in orch._FORMAS_EXCLUIDAS, forma
    assert "taya" in orch._FORMAS_EXCLUIDAS          # vocabulario base
    assert "kuru-bacoa" not in orch._FORMAS_EXCLUIDAS  # una acuñación de agente sí cuenta


def test_formas_en_texto_extrae_compuestos_y_minusculas():
    assert formas_en_texto("Taya wana-ka [sima-bana: sima+-bana = cumbre]") >= {"taya", "wana-ka", "sima-bana", "bana"}


def test_el_campo_lexico_puede_excluir_lo_heredado():
    campo = CampoLexico()
    campo.registrar(["taya", "taya", "kuru-bacoa"])
    assert campo.top(5) [0][0] == "taya"
    assert [f for f, _ in campo.top(5, excluir={"taya"})] == ["kuru-bacoa"]


# ── memoria del día y días encadenados ────────────────────────────────

def test_la_memoria_guarda_cinco_notas():
    m = orch.AgentMemory()
    for i in range(7):
        m.add("X", f"nota {i}")
    assert m.get("X").startswith("nota 2") and m.get("X").endswith("nota 6")


def test_la_koine_sobrevive_al_disco(tmp_path):
    idio = IdiolectoAgente("Manaure", {"aspecto": "completivo"})
    idio.registrar(["kali", "kali", "arima"], neologismos=["kuru-bacoa"], adoptadas=["biro-pana"])
    campo = CampoLexico(decaimiento=0.9)
    campo.registrar(["kali", "kuru-bacoa"])
    ruta = str(tmp_path / "koine.json")
    guardar_koine({"Manaure": idio}, campo, path=ruta)

    idiolectos, campo2 = cargar_koine(path=ruta)
    i2 = idiolectos["Manaure"]
    assert i2.frecuencias == idio.frecuencias
    assert i2.acunaciones == {"kuru-bacoa"} and i2.adopciones == {"biro-pana"}
    assert i2.vector_reciente() == idio.vector_reciente()
    assert campo2.pesos == campo.pesos and campo2.decaimiento == 0.9


def test_cargar_koine_falla_a_la_vista_si_no_hay_nada(tmp_path):
    with pytest.raises(FileNotFoundError):
        cargar_koine(path=str(tmp_path / "no-existe.json"))


def test_auto_mode_cierra_el_dia_con_una_nota_por_agente_y_guarda_la_koine(sim, monkeypatch, tmp_path):
    """Un día de 3 turnos × 4 agentes: cada uno recibe su nota «D1: hablé al…»
    y la koiné queda en disco para --continuar."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(orch, "get_db", lambda: _DBQueGraba())
    monkeypatch.setattr(orch, "get_client", lambda run_id=None: sim["client"])
    monkeypatch.setattr(orch, "huella_de_base", lambda semilla=None: {"motor_sucio": False, "semilla": semilla})
    memorias = {}
    real_add = orch.AgentMemory.add

    def add_espia(self, agent, note):
        memorias.setdefault(agent, []).append(note)
        real_add(self, agent, note)
    monkeypatch.setattr(orch.AgentMemory, "add", add_espia)

    from curiana_perfiles import cargar_perfil
    orch.auto_mode(sim["client"], 3, verbose=False, perfil=cargar_perfil("base"),
                   agentes_por_turno=4, roster_nombre="todos", turnos_por_dia=3, semilla=7)

    notas_dia = {a: [n for n in ns if n.startswith("D1: hablé al ")] for a, ns in memorias.items()}
    assert notas_dia and all(len(v) == 1 for v in notas_dia.values()), notas_dia
    assert any("acuñé kuru-bacoa" in v[0] for v in notas_dia.values())
    assert (tmp_path / "curiana_koine.json").exists()
    assert (tmp_path / "curiana_state.json").exists()


class _DBQueGraba:
    def __init__(self):
        self.config = None
    def create_run(self, *a, **k):
        self.config = k.get("config")
        return "run-de-prueba"
    def end_run(self, run_id, total_turns, total_days):
        pass
    def __getattr__(self, nombre):
        return lambda *a, **k: "id"
