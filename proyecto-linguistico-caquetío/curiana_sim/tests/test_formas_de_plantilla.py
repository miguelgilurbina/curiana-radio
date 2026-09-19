"""La puerta de las formas de plantilla (corte de serie del 2026-09-18).

Miguel: «dale pues con A». Una forma que el prompt YA ENSEÑA —el vocabulario
base o un ejemplo de las plantillas— no es una acuñación: no se registra, no
compite, no puede adoptarse y no sale en el diccionario de cierre. El rechazo
se CUENTA y se dice al cerrar el run.

Lo que vigilan estos tests, en orden:

  (a) la lista sale de las PLANTILLAS, no de una copia a mano, y es UNA:
      el orquestador y `analizar_nodos` miran la misma.
  (b) una forma del vocabulario base no se registra; el ejemplo de la
      plantilla tampoco; una acuñación legítima sí.
  (c) el contador de rechazos sale en el cierre del run (de punta a punta,
      por `auto_mode`), y la forma de plantilla no entra en competencia.
  (d) LOS PROMPTS NO SE MUEVEN con habla legítima: la era 1 y la era 2 sin
      `--escena`, tres turnos, byte a byte con la puerta puesta y quitada
      (patrón de `tests/test_escena_motor.py`). Lo que SÍ se mueve —y es el
      corte de serie declarado— es el prompt de quien copia la plantilla:
      ahí la forma deja de aparecer en las vías comunitarias.
  (e) EL EJEMPLO DE LA IDENTIDAD SE MUEVE CON LA PUERTA (corte del
      2026-09-19, Miguel: «Vale»): el ejemplo pasó de `kali-bana` a
      `biro-bana`, así que ninguna plantilla puede enseñar ya `kali-bana` y
      `biro-bana` tiene que estar en la lista. La lista se construye
      llamando a las plantillas: si alguien vuelve a escribirla a mano, esto
      se cae.
"""
import json
import random

import pytest

import curiana_agents_era2 as era2
import curiana_koine as koine
import curiana_lexicon as lx
import curiana_orchestrator_v2 as orch
from curiana_lexicon import (
    FORMAS_DE_PLANTILLA,
    IDENTIDAD_LINGUISTICA,
    LexicoComunitario,
    Neologismo,
    es_forma_de_plantilla,
)
from curiana_observer import ObserverAgent
from curiana_perfiles import cargar_perfil
from curiana_state import estado_inicial, estado_inicial_test

# `biro-bana` es el ejemplo LITERAL de la plantilla de identidad desde el corte
# del 2026-09-19 (antes lo era `kali-bana`) y `naa-ni` el del bloque de
# morfología; `warawara` está en el vocabulario base; `wana-ni` lo enseña el
# refuerzo y `cati` el rescate. `kuru-bacoa` no la enseña nadie.
EJEMPLO_DE_LA_IDENTIDAD = "biro-bana"
EJEMPLO_RETIRADO = "kali-bana"          # el de antes del 2026-09-19
DE_PLANTILLA = (EJEMPLO_DE_LA_IDENTIDAD, "naa-ni", "warawara", "wana-ni",
                "ma-arua", "cati")
LEGITIMA = "kuru-bacoa"
RESPUESTA = f"Taya wana-ka arima wara kari. [{LEGITIMA}: kuru+-bacoa = la arboleda]."
RESPUESTA_COPIA = ("Taya wana-ka arima wara kari. "
                   "[biro-bana: biro+-bana = cerro de la sal].")
_CALL_AGENT = orch.call_agent


class _Cliente:
    pass


def _neo(forma, autor="Manaure", dia=1, turno=1):
    return Neologismo(turno=turno, dia=dia, autor=autor, forma=forma,
                      componentes="x + y", significado="algo",
                      contexto="", regla_aplicada="")


# ══════════════════════════════════════════════════════════════════════
# (a) la lista sale de las plantillas, y es UNA
# ══════════════════════════════════════════════════════════════════════

def test_a_la_lista_se_construye_desde_las_plantillas():
    """No es una copia a mano: cada forma que la puerta declara está en el
    vocabulario base o en el texto de alguna plantilla."""
    de_los_textos = set()
    for texto in lx._textos_de_plantilla():
        de_los_textos |= lx.formas_en_texto(texto)
    assert FORMAS_DE_PLANTILLA == frozenset(lx.VOCABULARIO_BASE) | de_los_textos
    # y el ejemplo de la identidad está dentro porque la identidad lo dice
    assert EJEMPLO_DE_LA_IDENTIDAD in lx.formas_en_texto(IDENTIDAD_LINGUISTICA)


def test_a_es_una_puerta_y_no_dos():
    """El orquestador y `analizar_nodos` miran la MISMA lista. Eran dos, y una
    de las dos no se respetaba: de ahí el corte."""
    import analizar_nodos

    assert orch._FORMAS_EXCLUIDAS is FORMAS_DE_PLANTILLA
    assert analizar_nodos.formas_excluidas() == frozenset(FORMAS_DE_PLANTILLA)
    assert orch._IDENTIDAD_LINGUISTICA == IDENTIDAD_LINGUISTICA


def test_a_la_puerta_incluye_el_refuerzo_y_el_rescate():
    """Las dos plantillas que `_FORMAS_EXCLUIDAS` no miraba y sí enseñan
    formas: el refuerzo dice «Taya wana-ni …» y «ta-barsure, wa-duna, ma-arua»,
    el rescate «katsi→cati, bara→para»."""
    for forma in ("wana-ni", "wa-duna", "ma-arua", "cati"):
        assert es_forma_de_plantilla(forma), forma


def test_a_las_otras_plantillas_no_ensenan_formas_fuera_de_la_puerta():
    """Verificar el cero: `[Voces de fuera]` enseña claves del vocabulario
    base (ya dentro) y `[Tu tierra]` no enseña ninguna forma caquetía."""
    import curiana_mundo as mundo

    for _clave, forma, _glosa, _fam in lx.voces_de_fuera_posibles():
        assert es_forma_de_plantilla(forma), forma
    formas_del_mundo = set()
    for sitio in mundo.sitios():
        for periodo in (mundo.clima().get("frases_del_cargador") or {}):
            formas_del_mundo |= lx.formas_en_texto(
                mundo.bloque_tu_tierra(sitio, periodo, "mañana"))
    fuera = formas_del_mundo - FORMAS_DE_PLANTILLA
    assert not [f for f in fuera if "-" in f or f in lx.VOCABULARIO_BASE], sorted(fuera)


# ══════════════════════════════════════════════════════════════════════
# (b) qué se registra y qué no
# ══════════════════════════════════════════════════════════════════════

def test_b_una_forma_del_vocabulario_base_no_se_registra():
    lexico = LexicoComunitario()
    assert lexico.registrar_neologismo(_neo("warawara")) is False
    assert lexico._neologismos == []
    assert lexico.rechazos_de_plantilla == [("warawara", "Manaure", 1, 1)]


def test_b_el_ejemplo_de_la_plantilla_no_se_registra():
    lexico = LexicoComunitario()
    for forma in DE_PLANTILLA:
        assert lexico.registrar_neologismo(_neo(forma)) is False, forma
    assert lexico._neologismos == []
    assert len(lexico.rechazos_de_plantilla) == len(DE_PLANTILLA)


def test_b_una_acunacion_legitima_si_se_registra():
    lexico = LexicoComunitario()
    assert lexico.registrar_neologismo(_neo(LEGITIMA)) is True
    assert [n.forma for n in lexico._neologismos] == [LEGITIMA]
    assert lexico.rechazos_de_plantilla == []


def test_b_lo_rechazado_no_puede_adoptarse_ni_entra_en_palabras_activas():
    """Es la cadena entera: sin registro no hay propuesta pendiente, sin
    propuesta no hay adopción, y sin adopción no entra en `palabras_activas()`
    —que es lo que el scorer reconoce— ni en el diccionario de cierre."""
    lexico = LexicoComunitario()
    lexico.registrar_neologismo(_neo(EJEMPLO_DE_LA_IDENTIDAD, autor="Simaure"))
    assert lexico.neologismos_pendientes() == []
    assert lexico.adoptar(EJEMPLO_DE_LA_IDENTIDAD, "Dakawa", turno=2) is None
    assert lexico.adoptar(EJEMPLO_DE_LA_IDENTIDAD, "Chuchubi", turno=3) is None
    assert EJEMPLO_DE_LA_IDENTIDAD not in lexico.palabras_activas()
    assert lexico.adoptados_en_dos_ambitos() == []


def test_b_el_observer_no_registra_la_copia_pero_sigue_contandola_como_propuesta():
    """`neologisms_proposed` NO se mueve: sale de
    `extraer_neologismos_del_texto()`, que es anterior al registro. Lo que se
    mueve es lo que queda registrado."""
    lexico = LexicoComunitario()
    observer = ObserverAgent(None, lexico)
    registro = observer.analizar(agente="Simaure", etnia="caquetío", tier=1,
                                 texto=RESPUESTA_COPIA, dia=1, turno=1,
                                 momento="amanecer", estacion="seca")
    assert [n.forma for n in registro.neologismos_extraidos] == [EJEMPLO_DE_LA_IDENTIDAD]
    assert lexico._neologismos == []
    assert len(lexico.rechazos_de_plantilla) == 1


def test_b_un_lexico_viejo_no_cuela_la_forma_por_la_puerta_de_atras(tmp_path):
    """`--continuar` carga el léxico del día anterior. Si ese JSON es de antes
    del corte y trae una forma de plantilla ya registrada, la puerta también
    la para aquí — y la cuenta."""
    ruta = tmp_path / "curiana_lexico.json"
    ruta.write_text(json.dumps({
        "lexico": {EJEMPLO_DE_LA_IDENTIDAD: {"significado": "cerro de la sal",
                                             "autor": "x", "dia": 1}},
        "neologismos": [_neo(EJEMPLO_DE_LA_IDENTIDAD).to_dict(),
                        _neo(LEGITIMA).to_dict()],
    }, ensure_ascii=False), encoding="utf-8")
    lexico = LexicoComunitario.load(str(ruta))
    assert [n.forma for n in lexico._neologismos] == [LEGITIMA]
    assert EJEMPLO_DE_LA_IDENTIDAD not in lexico.palabras_activas()
    assert len(lexico.rechazos_de_plantilla) == 1
    # y el control: apagando la puerta se carga como antes del corte
    viejo = LexicoComunitario.load(str(ruta), filtrar_plantilla=False)
    assert len(viejo._neologismos) == 2


def test_b_la_copia_no_entra_en_competencia():
    """El día 2 de la serie C `kali-bana` iba GANANDO «las cuentas» 15,8 contra
    3,1 y 2,9: el ejemplo del prompt compitiendo contra las formas de verdad."""
    comp = koine.CompetenciaLexica()
    comp.activar("cuentas_vidrio", "unas cuentas brillantes")
    comp.proponer("cuentas_vidrio", EJEMPLO_DE_LA_IDENTIDAD, "Chirwa")
    comp.proponer("cuentas_vidrio", "brilu-uco", "Hayo")
    comp.registrar_uso(EJEMPLO_DE_LA_IDENTIDAD, "Uria")
    assert list(comp.referentes["cuentas_vidrio"]["variantes"]) == ["brilu-uco"]
    # control: sin la puerta, compite (es el motor de antes del corte)
    antes = koine.CompetenciaLexica(filtrar_plantilla=False)
    antes.activar("cuentas_vidrio", "unas cuentas brillantes")
    antes.proponer("cuentas_vidrio", EJEMPLO_DE_LA_IDENTIDAD, "Chirwa")
    assert EJEMPLO_DE_LA_IDENTIDAD in antes.referentes["cuentas_vidrio"]["variantes"]


# ══════════════════════════════════════════════════════════════════════
# (c) el cierre lo dice — de punta a punta, por auto_mode
# ══════════════════════════════════════════════════════════════════════

class _DBMuda:
    def create_run(self, *a, **k):
        return "run-de-prueba"

    def save_turn(self, **k):
        return "turn-de-prueba"

    def end_run(self, *a, **k):
        pass

    def get_run(self, run_id):
        return {"config": {"escena": False, "capubana_cada": 0}}

    def runs_de_cadena(self, *a, **k):
        return []

    def __getattr__(self, nombre):
        return lambda *a, **k: "id"


def _correr(monkeypatch, tmp_path, respuesta, turnos=5):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(orch, "call_agent", lambda *a, **k: respuesta)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "get_db", lambda: _DBMuda())
    monkeypatch.setattr(orch, "get_client", lambda run_id=None: _Cliente())
    monkeypatch.setattr(orch, "huella_de_base",
                        lambda semilla=None: {"motor_sucio": False, "semilla": semilla})
    orch.auto_mode(_Cliente(), turnos, verbose=False, perfil=cargar_perfil("base"),
                   agentes_por_turno=4, roster_nombre="todos",
                   turnos_por_dia=turnos, semilla=11)


def test_c_el_cierre_dice_cuantas_acunaciones_rechazo(monkeypatch, tmp_path, capsys):
    """«N acuñaciones rechazadas por estar en el prompt: …». No se silencia:
    es la cifra que avisa de que la plantilla se está copiando."""
    _correr(monkeypatch, tmp_path, RESPUESTA_COPIA)
    salida = capsys.readouterr().out
    assert ("acuñaciones rechazadas por estar en el prompt: "
            f"{EJEMPLO_DE_LA_IDENTIDAD}") in salida
    # y la disputa del día no tiene al ejemplo del prompt entre sus variantes
    with open(tmp_path / "curiana_koine.json", encoding="utf-8") as f:
        koine_json = json.load(f)
    variantes = [v for ref in koine_json["competencia"]["referentes"].values()
                 for v in ref["variantes"]]
    assert EJEMPLO_DE_LA_IDENTIDAD not in variantes


def test_c_sin_copias_el_cierre_no_dice_nada(monkeypatch, tmp_path, capsys):
    _correr(monkeypatch, tmp_path, RESPUESTA)
    salida = capsys.readouterr().out
    assert "rechazadas por estar en el prompt" not in salida
    assert LEGITIMA in salida          # la acuñación legítima sí llega al cierre


# ══════════════════════════════════════════════════════════════════════
# (d) los prompts: byte a byte con habla legítima
# ══════════════════════════════════════════════════════════════════════

def _prompts(monkeypatch, state, *, roster, respuesta, filtrar, turnos=3,
             era=None):
    """Los prompts de `turnos` turnos con cliente falso (patrón de
    test_escena_motor): uno por llamada a `call_agent`, el de la 1ª pasada.

    `filtrar=False` es el motor de ANTES del corte."""
    random.seed(20260918)      # la muestra del lexicón se sortea con el RNG global
    if era is not None:
        monkeypatch.setattr(orch, "ALL_AGENTS", era)
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    capturas, actual = [], [None]
    monkeypatch.setattr(orch, "_invoke",
                        lambda c, system, user: capturas.append(
                            {"agente": actual[0], "system": system, "user": user}
                        ) or respuesta)
    primeros = []

    def espia(client, agent_name, *a, **k):
        actual[0] = agent_name
        antes = len(capturas)
        salida = _CALL_AGENT(client, agent_name, *a, **k)
        primeros.append(capturas[antes])
        return salida
    monkeypatch.setattr(orch, "call_agent", espia)

    lexico = LexicoComunitario(filtrar_plantilla=filtrar)
    observer = ObserverAgent(_Cliente(), lexico)
    memoria = orch.AgentMemory()
    for _ in range(turnos):
        orch.run_turn(_Cliente(), state, memoria, lexico, observer, verbose=False,
                      agentes_por_turno=len(roster), roster=list(roster))
    return primeros


def _estado_era2():
    s = estado_inicial("PARAGUANÁ")
    s.turnos_por_dia = 6
    s.escena = False
    s.capubana_cada = 0
    s.evento_del_turno = None
    return s


@pytest.mark.parametrize("era", ["era1", "era2"])
def test_d_los_prompts_no_se_mueven_con_habla_legitima(monkeypatch, era):
    """La era 1 siempre, y la era 2 sin `--escena`: con habla que no copia la
    plantilla, poner la puerta no mueve un carácter de lo que se ENVÍA."""
    if era == "era1":
        roster, elenco, estado = orch.roster_de_habla("koine")[:6], None, estado_inicial_test
    else:
        roster, elenco, estado = list(era2.ALL_AGENTS)[:6], era2.ALL_AGENTS, _estado_era2
    con = _prompts(monkeypatch, estado(), roster=roster, respuesta=RESPUESTA,
                   filtrar=True, era=elenco)
    sin = _prompts(monkeypatch, estado(), roster=roster, respuesta=RESPUESTA,
                   filtrar=False, era=elenco)
    assert [c["agente"] for c in con] == [c["agente"] for c in sin]
    for c, s in zip(con, sin):
        assert c["system"] == s["system"], c["agente"]
        assert c["user"] == s["user"], c["agente"]
    # y el control de que el montaje mide algo: la acuñación legítima llegó a
    # circular por las vías comunitarias del prompt
    assert any(LEGITIMA in c["system"] for c in con)


def test_d_lo_que_si_se_mueve_es_el_prompt_de_quien_copia(monkeypatch):
    """El corte de serie, visto en el prompt: con la puerta, la forma que el
    prompt ya enseña deja de volver por las vías comunitarias (V1/V2). Sin
    ella, el motor se la leía a todo el mundo como si fuera nueva."""
    roster = list(era2.ALL_AGENTS)[:6]
    con = _prompts(monkeypatch, _estado_era2(), roster=roster,
                   respuesta=RESPUESTA_COPIA, filtrar=True, era=era2.ALL_AGENTS)
    sin = _prompts(monkeypatch, _estado_era2(), roster=roster,
                   respuesta=RESPUESTA_COPIA, filtrar=False, era=era2.ALL_AGENTS)
    vias = ("[Palabras nuevas de la comunidad]", "[Palabras propuestas en evaluación")

    def lineas_de_via(prompts):
        return [l for p in prompts for l in p["system"].splitlines()
                if l.startswith(vias)]
    assert any(EJEMPLO_DE_LA_IDENTIDAD in l for l in lineas_de_via(sin))
    assert not any(EJEMPLO_DE_LA_IDENTIDAD in l for l in lineas_de_via(con))


# ══════════════════════════════════════════════════════════════════════
# (e) el ejemplo de la identidad se mueve CON la puerta
# ══════════════════════════════════════════════════════════════════════

def test_e_la_puerta_se_movio_con_el_ejemplo():
    """Corte del 2026-09-19 (Miguel: «Vale»). El ejemplo pasó de `kali-bana`
    a `biro-bana` y la lista —que se construye LLAMANDO a las plantillas— se
    movió sola: la vieja salió y la nueva entró.

    `kali` y `biro` siguen los dos dentro por ser claves del lexicón: la
    puerta incluye `VOCABULARIO_BASE` entero. Lo que cambia es el COMPUESTO.
    """
    assert es_forma_de_plantilla("biro-bana")
    assert not es_forma_de_plantilla(EJEMPLO_RETIRADO)
    assert "biro-bana" in FORMAS_DE_PLANTILLA
    assert EJEMPLO_RETIRADO not in FORMAS_DE_PLANTILLA
    # y las dos raíces siguen dentro, que es otra cosa
    assert es_forma_de_plantilla("kali") and es_forma_de_plantilla("biro")


def test_e_ninguna_plantilla_ensena_ya_la_forma_retirada():
    """Ninguno de los diez textos estáticos dice `kali-bana`, ni siquiera de
    pasada: si alguien la reintroduce en una plantilla, vuelve a la puerta sin
    que nadie lo decida y esto lo caza.

    Se mira el texto ENTERO de cada plantilla, no sólo la lista de formas:
    `formas_en_texto()` es el criterio ancho y aun así un `kali-bana` escrito
    dentro de una glosa castellana pasaría — aquí no.
    """
    for texto in lx._textos_de_plantilla():
        assert EJEMPLO_RETIRADO not in texto
        assert EJEMPLO_RETIRADO not in lx.formas_en_texto(texto)
    # el control de que el test mide algo: la forma NUEVA sí está, y en una
    assert sum(1 for t in lx._textos_de_plantilla()
               if "biro-bana" in lx.formas_en_texto(t)) == 1


def test_e_la_forma_retirada_vuelve_a_poder_acunarse():
    """Consecuencia declarada del corte: al salir de la puerta, `kali-bana`
    deja de estar vetada y se registra como cualquier acuñación.

    No es un descuido: vetarla por haber sido ejemplo histórico sería una
    decisión de Miguel, y no está tomada. El test fija la conducta de HOY para
    que el día que se decida, se vea cambiar.
    """
    lexico = LexicoComunitario()
    assert lexico.registrar_neologismo(_neo(EJEMPLO_RETIRADO)) is True
    assert [n.forma for n in lexico._neologismos] == [EJEMPLO_RETIRADO]
    assert lexico.rechazos_de_plantilla == []


def test_e_el_ejemplo_es_morfologicamente_correcto_y_del_mundo():
    """Las piezas del ejemplo nuevo, contra el canon: `biro` es una entrada
    ATESTIGUADA del lexicón y `-bana` un sufijo de las reglas del motor (D9,
    'cerro, sitio alto'). El compuesto no es clave de nadie: es una acuñación
    de manual, que es justo lo que el ejemplo enseña a hacer.
    """
    biro = lx.VOCABULARIO_BASE["biro"]
    assert biro["fuente"] == "caquetío-atestiguado"
    assert biro["sig"] == "sal"
    assert "-bana" in {a.lower() for a in lx.TODAS_LAS_REGLAS}
    assert "biro-bana" not in lx.VOCABULARIO_BASE
    # y el ejemplo se lee en la plantilla tal cual, con su molde
    assert ("[biro-bana: biro+-bana = cerro de la sal]"
            in IDENTIDAD_LINGUISTICA)


def test_e_la_era_1_tambien_cambia():
    """`IDENTIDAD_LINGUISTICA` es UNA constante y la leen los dos mundos: el
    corte toca también la Curiana, que deja de ser byte a byte con sus runs
    viejos. Está declarado en la bitácora (punto 9 del cambio de instrumento)
    y aquí se fija que no hay una segunda plantilla por era escondida.
    """
    assert orch._IDENTIDAD_LINGUISTICA is IDENTIDAD_LINGUISTICA
    assert lx._textos_de_plantilla()[0] is IDENTIDAD_LINGUISTICA
