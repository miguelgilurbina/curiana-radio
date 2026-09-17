"""El Director con mundo y su reflexión del día (2026-09-16).

  - DIRECTOR_SYSTEM dice «de Paraguaná» cuando el elenco es el de la era 2, y
    en la era 1 es el texto de siempre.
  - director_narrate() lleva, sólo en la era 2, el bloque [El mundo] (≤ 400)
    con la frase del período, la del momento y las restricciones del corpus
    (ecologia-007/018/032: cardonal, sin ríos ni ceibas — el día 2 de la era 2
    el Director inventó «la sombra del ceibo»).
  - reflexion_del_dia(): una llamada por día con --reflexion, con cliente mock.

Y lo que el cierre del día 3 (run 0193873d) dejó abierto:

  - la cabecera: la reflexión del día 3 se tituló «Cierre Día 4, Turno 1»
    porque el prompt le pasaba state.to_context_string(), que al cerrar ya
    apunta al amanecer siguiente. Ahora la línea de estado es la del día
    cerrado (estado_del_dia_cerrado) y el encargo fija el día.
  - el residuo: con los eventos ya traducidos (#138), el Director escribió
    «Los Caquetíos y Guaycarí se juntan…». Venía de su propia nota del día 2
    (state.notas_orquestador), que nadie filtraba. Ahora el estado, los
    cierres, las intervenciones y las notas pasan por
    curiana_eventos.decir_para_el_mundo(), el sistema de Paraguaná dice qué
    pueblos NO hay y el Director recibe el elenco en escena.

La era 1 no cambia ni un byte: decir_para_el_mundo("CURIANA") es la identidad,
y hay un test que lo comprueba con un texto lleno de nombres viejos.

Sin LLM ni Supabase: el cliente es un mock que graba lo que se le pide.
"""
import json
from types import SimpleNamespace

import curiana_orchestrator_v2 as orch
from curiana_director import (
    cargar_reflexiones,
    director_system,
    estado_del_dia_cerrado,
    guardar_reflexion,
    reflexion_del_dia,
)
from curiana_lexicon import LexicoComunitario
from curiana_mundo import (
    MOMENTOS,
    PRESUPUESTO_DIRECTOR,
    RESTRICCIONES_DEL_DIRECTOR,
    hechos_del_corpus,
    restricciones_del_director,
    resumen_del_mundo,
)
from curiana_observer import ObserverAgent
from curiana_state import ComunidadState, estado_inicial_test

REFLEXION = "Hoy cambió el viento. Prendió «kuru-bacoa» en boca de Kasebo. Mañana queda el agua."
SISTEMA_ERA1 = """Eres el Director de la simulación comunitaria de la Curiana.
Estilo: conciso, sensorial, presente. Crónica oral caquetía.
No uses lenguaje romántico ni exótico. Describe lo que un habitante vería y sentiría."""


class _ClienteMock:
    """Graba cada messages.create(...) y devuelve siempre la misma reflexión."""
    def __init__(self):
        self.llamadas = []
        self.messages = self

    def create(self, **kw):
        self.llamadas.append(kw)
        return SimpleNamespace(content=[SimpleNamespace(text=f"  {REFLEXION}  ")])


def _paraguana(**kw):
    s = ComunidadState(**kw)
    s.fijar_mundo("PARAGUANÁ")
    return s


# ── el sistema del Director por mundo ─────────────────────────────────

def test_el_director_de_la_era_1_es_el_de_siempre():
    assert director_system("CURIANA") == SISTEMA_ERA1
    assert orch.DIRECTOR_SYSTEM == director_system(orch.MUNDO)


def test_el_director_de_paraguana_se_llama_asi_y_se_ata_al_mundo():
    s = director_system("PARAGUANÁ")
    assert s.startswith("Eres el Director de la simulación comunitaria de Paraguaná.")
    assert "Curiana" not in s and "[El mundo]" in s


def test_el_sistema_de_paraguana_dice_que_pueblos_no_hay_y_de_donde_sale_la_gente():
    """La regla explícita: la era 2 dejó fuera a los foráneos (2026-09-14) y el
    Director del día 3 seguía juntando «Caquetíos y Guaycarí» en la orilla."""
    s = director_system("PARAGUANÁ")
    assert "[La gente que hay hoy]" in s
    for pueblo in ("guaycaríes", "jirajaras", "gayones"):
        assert pueblo in s, pueblo
    assert "una sola gente" in s
    # el caribe NO se niega: llega por mar y no reside (etnia-008)
    assert "caribe" not in s.lower()


# ── las restricciones salen del corpus, por id ────────────────────────

def test_las_restricciones_citan_entradas_que_existen_y_dicen_lo_que_dicen():
    hechos = hechos_del_corpus()
    assert {"ecologia-007", "ecologia-018", "ecologia-026",
            "ecologia-032", "ecologia-080"} <= set(hechos)
    for frase, ids, claves in RESTRICCIONES_DEL_DIRECTOR:
        assert all(i in hechos for i in ids), ids
        contenido = " ".join(str(hechos[i].get("contenido", "")) for i in ids).lower()
        for c in claves:
            assert c in contenido, (c, ids)          # la línea no dice más que el corpus
            assert c in frase.lower(), (c, frase)
    assert restricciones_del_director() == (
        "[El monte es cardonal: cují, yabo, dividivi, cardón; no hay ríos ni ceibas; "
        "son dos aguas y no una: la orilla del este, con su marea, y la costa oeste "
        "de Punta Cardón]")


def test_el_director_sabe_que_las_aguas_son_dos(monkeypatch):
    """2026-09-17, run 3973d317: el Director cerró el día 1 de la serie B con
    «las canoas volverán al Golfete» para toda la gente del día, y un agente de
    AMUAY —cuya orilla es la costa oeste (ZA1), no el Golfete— repitió la
    palabra en el turno de la tarde. El Golfete es canon de GUARANAO (ZG2:
    Tacuato y El Cayude son «la orilla del Golfete»), así que no se puede
    borrar: lo que faltaba era que el Director supiera que hay OTRA agua.

    Dos condiciones: la línea sale del corpus por id, como las otras dos (si un
    id desaparece, la restricción no se dice — no se inventa), y NO nombra el
    Golfete: la restricción va en los 18 bloques y nombrarlo ahí sería repetirle
    al Director nueve veces más la palabra que sobra."""
    import curiana_mundo as M

    for periodo in ("viento", "seca_larga", "siembra"):
        for m in MOMENTOS:
            r = resumen_del_mundo(_paraguana(dia=1, estacion=periodo, momento=m))
            assert "son dos aguas y no una" in r and "costa oeste" in r, (periodo, m)
    assert "Golfete" not in restricciones_del_director()
    # el único [El mundo] que dice «Golfete» sigue siendo el de la tarde del
    # viento, y eso es la frase del momento (clima_era2.yaml), no la restricción
    con_golfete = [(p, m) for p in ("viento", "seca_larga", "siembra") for m in MOMENTOS
                   if "Golfete" in resumen_del_mundo(_paraguana(dia=1, estacion=p, momento=m))]
    assert con_golfete == [("viento", "tarde")], con_golfete

    # sin la entrada del corpus, la restricción se cae entera y el resto queda
    hechos = {k: v for k, v in hechos_del_corpus().items() if k != "ecologia-080"}
    monkeypatch.setattr(M, "hechos_del_corpus", lambda *a, **k: hechos)
    linea = M.restricciones_del_director()
    assert "costa oeste" not in linea and "cardonal" in linea


def test_el_resumen_del_mundo_cabe_en_400_y_solo_existe_en_la_era_2():
    assert PRESUPUESTO_DIRECTOR == 400
    for periodo in ("viento", "seca_larga", "siembra"):
        for m in MOMENTOS:
            r = resumen_del_mundo(_paraguana(dia=1, estacion=periodo, momento=m))
            assert r.startswith("[El mundo] ") and len(r) <= PRESUPUESTO_DIRECTOR, (periodo, m, len(r))
            assert "cardonal" in r and "ni ceibas" in r, (periodo, m)
    assert resumen_del_mundo(estado_inicial_test()) == ""      # la seca de la era 1: sin canon
    # se puede pedir otro período y momento que los del estado (la reflexión mira el día cerrado)
    r = resumen_del_mundo(_paraguana(dia=51, estacion="seca_larga", momento="amanecer"),
                          estacion="viento", momento="noche")
    assert "Tiempo de Viento" in r and "jachos" in r


# ── director_narrate: el mundo sólo en Paraguaná, y deja el cierre ────

def test_director_narrate_lleva_el_mundo_en_paraguana_y_deja_el_cierre():
    cliente = _ClienteMock()
    s = _paraguana(dia=3, estacion="viento", momento="tarde", turnos_por_dia=6)
    s.notas_orquestador = "Ayer prendió kuru-bacoa."
    texto = orch.director_narrate(cliente, s, [{"agent": "Kasebo", "response": "Taya wana-ka."}])
    assert texto == REFLEXION
    kw = cliente.llamadas[0]
    prompt = kw["messages"][0]["content"]
    assert "[El mundo]" in prompt and "cardonal" in prompt and "Ayer prendió" in prompt
    assert "Kasebo" in prompt and "cierre narrativo del turno" in prompt
    assert kw["system"] == director_system("PARAGUANÁ")
    assert s.cierres_del_dia == [texto]


def test_director_narrate_en_la_era_1_no_lleva_mundo():
    cliente = _ClienteMock()
    orch.director_narrate(cliente, estado_inicial_test(), [{"agent": "Manaure", "response": "x"}])
    kw = cliente.llamadas[0]
    assert "[El mundo]" not in kw["messages"][0]["content"]
    assert kw["system"] == orch.DIRECTOR_SYSTEM


RESIDUO = ("Los Caquetíos y Guaycarí se juntan en la orilla. "
           "Biro-ko subió la sal al cerro. Nadie durmió bien.")


def test_director_narrate_filtra_el_residuo_y_pasa_la_gente_en_escena():
    """Lo que el día 3 delató: la nota del día anterior traía «los Guaycarí» y
    el Director la copió. Ahora la frase con el marco se cae, el nombre viejo
    se traduce y el Director sabe a quién puede nombrar."""
    cliente = _ClienteMock()
    s = _paraguana(dia=3, estacion="viento", momento="tarde", turnos_por_dia=6)
    s.notas_orquestador = RESIDUO
    orch.director_narrate(cliente, s, [{"agent": "Kasebo", "response": "Taya wana-ka."},
                                       {"agent": "Birokoa", "response": RESIDUO}])
    prompt = cliente.llamadas[0]["messages"][0]["content"]
    assert "Guaycarí" not in prompt and "Caquetíos" not in prompt and "Biro-ko" not in prompt
    assert "Birokoa subió la sal al cerro." in prompt      # traducido, no perdido
    assert "Nadie durmió bien." in prompt                  # la frase limpia se queda
    assert "[La gente que hay hoy]: Kasebo, Birokoa." in prompt


def test_director_narrate_en_la_era_1_deja_el_texto_byte_a_byte():
    """La era 1 no pasa por el traductor: su Director sí vive con guaycaríes."""
    cliente = _ClienteMock()
    s = estado_inicial_test()
    s.notas_orquestador = RESIDUO
    orch.director_narrate(cliente, s, [{"agent": "Biro-ko", "response": RESIDUO}])
    prompt = cliente.llamadas[0]["messages"][0]["content"]
    assert RESIDUO in prompt and "- Biro-ko: " + RESIDUO[:100] in prompt
    assert "[La gente que hay hoy]" not in prompt
    # y el estado semilla conserva sus nombres
    assert "Shaboro salió de su choza" in prompt


def test_los_cierres_del_dia_no_pasan_de_un_dia():
    cliente = _ClienteMock()
    s = _paraguana(dia=1, turnos_por_dia=2)
    for _ in range(3):
        orch.director_narrate(cliente, s, [{"agent": "Manaure", "response": "x"}])
    assert len(s.cierres_del_dia) == 2
    # un estado guardado por la era 1 no trae el campo y carga igual
    d = estado_inicial_test().to_dict()
    d.pop("cierres_del_dia")
    assert ComunidadState.from_dict(d).cierres_del_dia == []


# ── la reflexión del día ──────────────────────────────────────────────

def test_reflexion_del_dia_es_una_llamada_con_cierres_reporte_y_mundo():
    cliente = _ClienteMock()
    # el estado ya apunta al amanecer del día 2: se reflexiona el 1
    s = _paraguana(dia=2, turno=1, estacion="viento", momento="amanecer", turnos_por_dia=6)
    s.notas_orquestador = "Anoche quedó abierta el agua."
    texto = reflexion_del_dia(cliente, s, "  REPORTE LINGÜÍSTICO — DÍA 1\n  Score 7.1",
                              ["cierre uno", " ", "cierre seis"])
    assert texto == REFLEXION and len(cliente.llamadas) == 1
    kw = cliente.llamadas[0]
    prompt = kw["messages"][0]["content"]
    assert "Se cierra el día 1." in prompt
    assert "- cierre uno" in prompt and "- cierre seis" in prompt and "- (hoy" not in prompt
    assert "REPORTE LINGÜÍSTICO" in prompt and "Anoche quedó abierta" in prompt
    assert "[El mundo]" in prompt and "jachos" in prompt        # el viento, de noche
    assert "4-6 oraciones" in prompt and "qué queda abierto para mañana" in prompt
    assert kw["system"] == director_system("PARAGUANÁ") and kw["max_tokens"] >= 600
    # sin cierres se dice, y el día se puede fijar
    cliente2 = _ClienteMock()
    reflexion_del_dia(cliente2, s, "", [], dia=7)
    p2 = cliente2.llamadas[0]["messages"][0]["content"]
    assert "Se cierra el día 7." in p2 and "(hoy no hubo cierres narrativos)" in p2


def test_la_reflexion_fija_el_dia_cerrado_y_no_nombra_el_amanecer_siguiente():
    """La deuda del día 3: «# REFLEXIÓN DEL DIRECTOR — Cierre Día 4, Turno 1»
    sobre el día 3, porque el estado al cerrar ya apunta al día siguiente."""
    s = _paraguana(dia=4, turno=1, estacion="viento", momento="amanecer", turnos_por_dia=6)
    linea = estado_del_dia_cerrado(s, 3)
    assert "Día 3, Turno 6 (noche)" in linea and "Día 4" not in linea
    assert s.dia == 4 and s.turno == 1 and s.momento == "amanecer"   # no muta el estado

    cliente = _ClienteMock()
    reflexion_del_dia(cliente, s, "  REPORTE LINGÜÍSTICO — DÍA 3", ["cierre del turno 6"])
    prompt = cliente.llamadas[0]["messages"][0]["content"]
    assert "Se cierra el día 3." in prompt and "Día 3, Turno 6 (noche)" in prompt
    assert "Día 4" not in prompt and "Turno 1" not in prompt
    assert "sobre el día 3 y sólo sobre él" in prompt and "«Día 3»" in prompt


def test_la_reflexion_no_le_pasa_al_director_marcos_ni_nombres_de_la_era_1():
    cliente = _ClienteMock()
    s = _paraguana(dia=4, turno=1, estacion="viento", momento="amanecer", turnos_por_dia=6)
    s.notas_orquestador = RESIDUO
    reflexion_del_dia(cliente, s, "", [RESIDUO, "El viento no aflojó."],
                      dia=3, gente_en_escena=["Kasebo", "Birokoa", "Kasebo"])
    prompt = cliente.llamadas[0]["messages"][0]["content"]
    assert "Guaycarí" not in prompt and "Caquetíos" not in prompt and "Biro-ko" not in prompt
    assert "Birokoa subió la sal al cerro." in prompt and "El viento no aflojó." in prompt
    assert "[La gente que hay hoy]: Kasebo, Birokoa." in prompt       # sin repetidos
    assert "No nombres a nadie que no esté en esta lista." in prompt


def test_la_reflexion_de_la_era_1_conserva_su_texto():
    cliente = _ClienteMock()
    s = ComunidadState(dia=3, turno=1, turnos_por_dia=2)
    s.notas_orquestador = RESIDUO
    reflexion_del_dia(cliente, s, "", [RESIDUO], dia=2)
    prompt = cliente.llamadas[0]["messages"][0]["content"]
    assert prompt.count(RESIDUO) == 2 and "[El mundo]" not in prompt
    assert "Día 2, Turno 2 (noche)" in prompt


def test_las_reflexiones_se_guardan_en_curiana_director_json(tmp_path):
    ruta = str(tmp_path / "curiana_director.json")
    assert cargar_reflexiones(ruta) == []
    guardar_reflexion(1, "uno", "run-x", path=ruta, nuevo=True)
    guardar_reflexion(2, "dos", "run-y", path=ruta)
    r = cargar_reflexiones(ruta)
    assert [x["dia"] for x in r] == [1, 2] and r[0]["run_id"] == "run-x" and r[1]["texto"] == "dos"
    with open(ruta, encoding="utf-8") as f:
        assert set(json.load(f)) == {"reflexiones"}
    guardar_reflexion(3, "tres", path=ruta, nuevo=True)        # un run nuevo empieza de cero
    assert [x["dia"] for x in cargar_reflexiones(ruta)] == [3]


class _DBQueGraba:
    def create_run(self, *a, **k):
        return "run-de-prueba"

    def end_run(self, run_id, total_turns, total_days):
        pass

    def __getattr__(self, nombre):
        return lambda *a, **k: "id"


def _auto(monkeypatch, tmp_path, **kw):
    """auto_mode sin LLM ni DB: 6 turnos de 3 por día = 2 días cerrados."""
    monkeypatch.chdir(tmp_path)
    cliente = _ClienteMock()
    lexico = LexicoComunitario()
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: "Taya wana-ka arima wara kari.")
    monkeypatch.setattr(orch, "director_narrate", lambda c, state, inter: "(narración)")
    monkeypatch.setattr(orch, "get_db", lambda: _DBQueGraba())
    monkeypatch.setattr(orch, "get_client", lambda run_id=None: cliente)
    monkeypatch.setattr(orch, "huella_de_base", lambda semilla=None: {"motor_sucio": False, "semilla": semilla})
    llamadas = []

    def espia(client, state, reporte, cierres, **k):
        llamadas.append((k.get("dia"), reporte, list(cierres), state.mundo))
        return f"reflexión del día {k.get('dia')}"
    monkeypatch.setattr(orch, "reflexion_del_dia", espia)
    from curiana_perfiles import cargar_perfil
    orch.auto_mode(cliente, 6, verbose=False, perfil=cargar_perfil("base"),
                   agentes_por_turno=4, roster_nombre="todos", turnos_por_dia=3, semilla=7, **kw)
    return llamadas


def test_auto_mode_reflexiona_una_vez_por_dia_solo_con_la_bandera(monkeypatch, tmp_path):
    llamadas = _auto(monkeypatch, tmp_path, reflexion=True)
    assert [d for d, *_ in llamadas] == [1, 2]
    assert all("REPORTE LINGÜÍSTICO" in rep for _, rep, _, _ in llamadas)
    estado = ComunidadState.load(str(tmp_path / "curiana_state.json"))
    assert estado.notas_orquestador == "reflexión del día 2"
    assert estado.cierres_del_dia == []
    guardadas = cargar_reflexiones(str(tmp_path / "curiana_director.json"))
    assert [g["dia"] for g in guardadas] == [1, 2] and guardadas[0]["run_id"] == "run-de-prueba"


def test_sin_la_bandera_no_hay_reflexion_ni_archivo(monkeypatch, tmp_path):
    assert _auto(monkeypatch, tmp_path) == []
    assert not (tmp_path / "curiana_director.json").exists()
    assert ComunidadState.load(str(tmp_path / "curiana_state.json")).notas_orquestador == ""
