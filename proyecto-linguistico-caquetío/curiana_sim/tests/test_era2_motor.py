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


# ── -ko y -sha fuera de la gramática (Miguel, 2026-09-14) ─────────────

def test_ko_y_sha_no_se_ensenan_ni_cuentan_como_regla():
    """«Sí o sí hay que sacar eso de -ko y -sha, si es inventado, tanto de la
    gramática como de los nombres». Se archivan en REGLAS_RETIRADAS."""
    from curiana_lexicon import REGLAS_RETIRADAS, TODAS_LAS_REGLAS
    for plantilla in (prompt_reglas_completo(), prompt_reglas_breve()):
        assert "hombre de" not in plantilla and "mujer de" not in plantilla
        assert "-ko (" not in plantilla and "-sha (" not in plantilla
        assert "-kana" in plantilla          # el plural se queda
    assert "-ko" not in TODAS_LAS_REGLAS and "-sha" not in TODAS_LAS_REGLAS
    assert set(REGLAS_RETIRADAS) == {"-ko", "-sha"}
    assert all("retirada" in r for r in REGLAS_RETIRADAS.values())


# ── los nombres de los agentes no son vocabulario ─────────────────────

def test_los_nombres_de_los_agentes_no_cuentan_como_palabras(monkeypatch):
    """Campaña de antropónimos: 49 de 63 nombres de la era 2 son homógrafos de
    una clave del lexicón. Nombrar a Karebe no es usar la palabra karebe."""
    import curiana_lexicon as L
    from curiana_lexicon import score_linguistico
    lex = LexicoComunitario()
    # era 1: el nombre con sufijo tampoco suma su raíz
    r = score_linguistico("Biro-ko maa-ka: biro wara.", lex)
    assert "biro-ko" not in r["palabras_arahuacas"] and "biro" in r["palabras_caquetias"]
    # era 2: un nombre que es clave del lexicón se descarta si es nombre del elenco
    monkeypatch.setattr(L, "_NOMBRES_AGENTES", frozenset({"karebe"}))
    r2 = score_linguistico("Karebe maa-ka: biro wara.", lex)
    assert "karebe" not in r2["palabras_caquetias"] and "biro" in r2["palabras_caquetias"]
    assert "karebe" in L.VOCABULARIO_BASE   # la homografía es real


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


# ── el perfil de la era 2 ─────────────────────────────────────────────

def test_el_perfil_era2_esconde_las_hipoteticas_y_puntua_igual():
    """Miguel, 2026-09-14: «escondemos las 38 hipotéticas». Cambia lo que el
    agente VE, nunca contra qué se le puntúa."""
    from curiana_perfiles import cargar_perfil
    era2, base = cargar_perfil("era2"), cargar_perfil("base")
    # Desde el 2026-09-14 (matacán) la era 2 ve también la capa retroabstraída:
    # voces vivas documentadas, no acuñaciones.
    assert era2.capas == {"caquetío-atestiguado", "caquetío-reconstruido",
                          "caquetío-retroabstraido"}
    assert "caquetío-hipotético" not in era2.capas
    assert era2.capas_de_score == base.capas_de_score
    assert not era2.ablacion


def test_la_muestra_del_perfil_era2_no_trae_ninguna_hipotetica():
    from curiana_lexicon import VOCABULARIO_BASE
    from curiana_perfiles import cargar_perfil
    hip = {k for k, e in VOCABULARIO_BASE.items() if e.get("fuente") == "caquetío-hipotético"}
    capas = cargar_perfil("era2").capas
    for _ in range(30):
        m = muestra_caquetio_dinamica(n_por_categoria=20, capas=capas, n_total=50)
        vistas = {item.split(" (")[0].strip() for linea in m.splitlines()[1:]
                  for item in linea.partition(":")[2].split(" · ")}
        assert not (vistas & hip), vistas & hip


def test_el_venado_entra_retroabstraido_y_la_era_2_lo_ve():
    """Miguel, 2026-09-14: «sí o sí lo tenemos que utilizar». El matacán de
    Esteves (p. 51) entra como voz viva con el sustrato en duda —la capa que
    #124 definió— y el perfil era2 pasa a enseñar esa capa. No es
    reconstruido (no tiene cognado) ni hipotético (la forma no es inventada);
    y las hipotéticas siguen escondidas."""
    from curiana_lexicon import VOCABULARIO_BASE, capa_epistemica
    from curiana_database import normalize_source_language
    from curiana_perfiles import cargar_perfil
    e = VOCABULARIO_BASE["matakán"]
    assert e["fuente"] == "caquetío-retroabstraido"
    assert e.get("forma_fuente") == "matacán" and e.get("categoria") == "fauna"
    capas = cargar_perfil("era2").capas
    pool = {k for k, d in VOCABULARIO_BASE.items()
            if normalize_source_language(d.get("fuente", "")) == "caquetío"
            and capa_epistemica(d.get("fuente", "")) in capas}
    assert "matakán" in pool
    hip = {k for k, d in VOCABULARIO_BASE.items() if d.get("fuente") == "caquetío-hipotético"}
    assert not (pool & hip)


# ── la esfera de contacto (2026-09-15) ────────────────────────────────

def test_la_mayuscula_decide_si_es_nombre_o_palabra(monkeypatch):
    """Corrección del 2026-09-16. El filtro en minúsculas se comía 52 voces
    del canon homógrafas de un nombre. Ahora `Karebe` es la persona y
    `karebe` el cucharón.

    Los tests corren con el elenco de la era 1, donde «Karebe» no existe: se
    inyecta el nombre como en test_los_nombres_de_los_agentes_no_cuentan."""
    import curiana_lexicon as L
    from curiana_lexicon import LexicoComunitario, score_linguistico
    monkeypatch.setattr(L, "_NOMBRES_AGENTES", frozenset({"karebe", "biro-ko"}))
    lex = LexicoComunitario()
    r = score_linguistico("Karebe maa-ka: el karebe está en el buko.", lex)
    # la palabra en minúscula cuenta una vez; la mención en mayúscula, ninguna
    assert "karebe" in r["palabras_caquetias"] and "buko" in r["palabras_caquetias"]
    solo_nombre = score_linguistico("Karebe maa-ka.", lex)
    assert "karebe" not in solo_nombre["palabras_caquetias"]
    # un nombre que NO es voz del lexicón se descarta siempre
    assert "biro-ko" not in score_linguistico("Biro-ko naa-ka", lex)["palabras_arahuacas"]


def test_el_prestamo_de_esfera_se_mide_aparte_y_no_penaliza():
    """Decisión de Miguel 2026-09-15: «el set de cinco es razonable; se debe
    medir aparte». Una voz de las islas es préstamo, no fuga; una voz wayuu
    —la lengua con la que reconstruimos— sigue penalizando."""
    from curiana_lexicon import (ESFERA_DE_CONTACTO, LexicoComunitario,
                                 VOCABULARIO_BASE, score_linguistico)
    from curiana_database import normalize_source_language
    lex = LexicoComunitario()
    assert "wayunaiki" not in ESFERA_DE_CONTACTO and "lokono" not in ESFERA_DE_CONTACTO
    base = score_linguistico("taya buko", lex)
    con_prestamo = score_linguistico("taya buko caiman", lex)
    assert con_prestamo["prestamos_de_esfera"] == ["caiman"]
    assert con_prestamo["otro_arahuaco"] == 0
    assert con_prestamo["score"] >= base["score"]          # no penaliza
    wayu = next(k for k, e in VOCABULARIO_BASE.items()
                if normalize_source_language(e.get("fuente", "")) == "wayunaiki" and "-" not in k)
    fuga = score_linguistico(f"taya buko {wayu}", lex)
    assert fuga["otro_arahuaco"] == 1 and fuga["score"] < base["score"]


def test_las_voces_de_fuera_son_solo_del_tier_1_y_nunca_caquetias():
    """«Los de tier 1 no sólo conocían su lenguaje sino el de su esfera de
    influencia» (Miguel, 2026-09-15). Van marcadas como ajenas, y el tier 2
    y el 3 no las ven."""
    from curiana_lexicon import (ESFERA_DE_CONTACTO, LexicoComunitario,
                                 VOCABULARIO_BASE, prompt_voces_de_fuera,
                                 vocabulario_para_agente)
    from curiana_database import normalize_source_language
    lex = LexicoComunitario()
    assert "Voces de fuera" in vocabulario_para_agente(1, lex, "canoa islas trueque")
    for tier in (2, 3):
        assert "Voces de fuera" not in vocabulario_para_agente(tier, lex, "canoa islas trueque")
    for _ in range(30):
        bloque = prompt_voces_de_fuera("trueque canoa islas")
        assert bloque.startswith("[Voces de fuera")
        for item in bloque.split("]: ", 1)[1].split("; "):
            forma = item.split(" = ")[0].strip()
            entrada = VOCABULARIO_BASE.get(forma) or VOCABULARIO_BASE.get(f"{forma}-kalinago")
            if entrada is None:
                continue
            fam = normalize_source_language(entrada.get("fuente", ""))
            assert fam in ESFERA_DE_CONTACTO, f"{forma} no es de la esfera: {fam}"
            # la glosa no repite la forma («cobo = cobo» no enseña nada)
            assert item.split(" = ")[1].split(" (")[0].strip().lower() != forma.lower()


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
