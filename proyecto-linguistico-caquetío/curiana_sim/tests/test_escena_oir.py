"""La escena en el motor: OÍR (PR 4 del diseño del 2026-09-17).

El lugar pasa a ser el ÁMBITO de lo que un agente ve. Lo que estos tests
vigilan, en el orden de la tarea:

  (a) LA ERA 1 BYTE A BYTE y LA ERA 2 SIN `--escena` BYTE A BYTE. Tres turnos
      con cliente falso y el RNG fijado, comparados contra el mismo motor con
      la escena desenchufada. La escena es un brazo, no un parche.
  (b) CON `--escena`, en seis turnos sin día de Capubana, ningún prompt lleva
      en V1 / V2 / V3 una forma cuyo proponente o adoptante estaba en OTRO
      ÁMBITO — el ámbito, no el nodo: Humohumo (GUARANAO) y Bajari (AMUAY)
      comparten el camino Moruy–Caseto y ahí sí se oyen. Y en el día de
      Capubana, donde los 63 están en el cerro, se oye todo.
  (c) `[Lo que se dijo aquí]` trae sólo voces del MOMENTO ANTERIOR del mismo
      lugar, ≤ 3, ≤ 280 caracteres, y no aparece en el primer turno de un run.
  (d) Un `curiana_lexico.json` escrito antes de la escena carga.
  (e) El campo léxico por ámbito suma al global.

Sin LLM y sin Supabase: se sustituye `_invoke` por un doble que acuña una
forma por agente.
"""
import json
import os
import random
import subprocess
import sys

import pytest

import curiana_agents_era2 as era2
import curiana_escena as esc
import curiana_escena_era2 as tabla
import curiana_koine as koine
import curiana_lexicon as lx
import curiana_orchestrator_v2 as orch
from curiana_koine import CampoLexico, CompetenciaLexica
from curiana_lexicon import (
    LexicoComunitario,
    Neologismo,
    prompt_lexico_activo,
    prompt_pendientes_evaluacion,
)
from curiana_observer import ObserverAgent
from curiana_state import estado_inicial, estado_inicial_test

SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CALL_AGENT = orch.call_agent

class _Cliente:
    pass



# Tanda de la base (2026-09-23): `kali` está ARCHIVADA desde el 2026-09-19 y
# una raíz archivada ya no avala una acuñación (db.1, el agujero de `kira`).
# Las formas de ejemplo de este archivo acuñan sobre `kasi`, la atestiguada.

def _raices_del_canon(n: int) -> list[str]:
    """`n` raíces DEL LEXICÓN, distintas, que no enseñe ninguna plantilla y
    que pasen la compuerta fonotáctica.

    Antes el doble se inventaba la raíz del nombre del agente
    (`agente.lower()[:6]`). Desde el corte del 2026-09-20 una raíz que no está
    en el lexicón no se registra ni compite —`lumina-bana-iro`—, así que el
    doble tiene que acuñar como acuñaría un agente de verdad: con morfemas
    propios. Se toman en orden alfabético para que sea determinista.
    """
    import curiana_lexicon as _lx
    salida = []
    for clave in sorted(_lx.VOCABULARIO_BASE):
        forma = f"{clave}-ana"
        if (clave.isalpha() and clave.islower() and 3 <= len(clave) <= 8
                and _lx.neologismo_valido(forma)
                and not _lx.es_forma_de_plantilla(forma)
                and not _lx.es_raiz_de_ninguna_parte(forma)):
            salida.append(clave)
            if len(salida) >= n + 1:
                break
    return salida


# El mapa cubre los DOS elencos: `test_a1` corre con el roster de la era 1.
_NOMBRES = sorted(set(era2.ALL_AGENTS) | set(orch.ALL_AGENTS)
                  | set(orch.roster_de_habla("koine")))
_RAICES = _raices_del_canon(len(_NOMBRES))
_POR_AGENTE = {a: r for a, r in zip(_NOMBRES, _RAICES)}

# La forma que TODOS usan sin haberla acuñado: es la que se adopta y la que
# hace medible la vía «adoptada en dos ámbitos». También sale del canon.
SEMBRADA = f"{_RAICES[-1]}-ana"


def _raiz(agente: str) -> str:
    """Las 63 raíces son distintas entre sí (comprobado abajo) y todas están
    en `VOCABULARIO_BASE`."""
    return _POR_AGENTE[agente]


def _respuesta_de(agente: str) -> str:
    """Cada agente acuña SU forma y usa la sembrada: así hay propuestas en
    todos los lugares y adopciones en unos cuantos."""
    r = _raiz(agente)
    return (f"Taya naa-ka {SEMBRADA} wara kari. "
            f"[{r}-ana: {r} + -ana = lo de {r}].")


def test_las_63_raices_del_doble_son_distintas():
    import curiana_lexicon as _lx
    assert len({_raiz(a) for a in era2.ALL_AGENTS}) == len(era2.ALL_AGENTS)
    # Y son raíces DE VERDAD: si el doble acuñara sobre raíz inventada, la
    # puerta del 2026-09-20 le rechazaría todas las acuñaciones y este archivo
    # mediría el vacío.
    for a in era2.ALL_AGENTS:
        assert not _lx.es_raiz_de_ninguna_parte(f"{_raiz(a)}-ana"), a
    assert not _lx.es_raiz_de_ninguna_parte(SEMBRADA)


# ══════════════════════════════════════════════════════════════════════
# utilidades
# ══════════════════════════════════════════════════════════════════════

def _capturar(monkeypatch, state, *, roster, agentes_por_turno, turnos,
              con_modulo=True, era=None, sembrar=False, nombrar=False):
    """Corre `turnos` turnos con cliente falso y devuelve
    (prompts, lexico, competencia, campo, escenas).

    `con_modulo=False` deja el orquestador como si curiana_escena no existiera:
    es el control del test de byte a byte. El RNG global se fija antes de cada
    corrida porque la muestra del lexicón se sortea con él."""
    random.seed(20260917)
    if era is not None:
        monkeypatch.setattr(orch, "ALL_AGENTS", era)
    monkeypatch.setattr(orch, "director_select_event", lambda s: None)
    monkeypatch.setattr(orch, "director_narrate", lambda *a, **k: "(narración)")
    if not con_modulo:
        monkeypatch.setattr(orch, "escena_de", lambda s: {})
        monkeypatch.setattr(orch, "ambito_de", lambda a, s: None)
        monkeypatch.setattr(orch, "ambito_visible_de", lambda a, s: None)
        monkeypatch.setattr(orch, "bloque_aqui_estas", lambda a, s, **k: "")
        monkeypatch.setattr(orch, "bloque_lo_que_se_dijo_aqui", lambda a, s, **k: "")
        monkeypatch.setattr(orch, "dichos_del_turno", lambda *a, **k: [])
        monkeypatch.setattr(orch, "volcado_de_escena", lambda s, e=None: "")
        monkeypatch.setattr(orch, "es_dia_de_capubana", lambda s, c=None: False)

    capturas, actual = [], [None]
    monkeypatch.setattr(orch, "_invoke",
                        lambda c, system, user: capturas.append(
                            {"agente": actual[0], "system": system, "user": user}
                        ) or _respuesta_de(actual[0]))
    primeros = []

    def espia(client, agent_name, *a, **k):
        actual[0] = agent_name
        antes = len(capturas)
        salida = _CALL_AGENT(client, agent_name, *a, **k)
        primeros.append(capturas[antes])
        return salida
    monkeypatch.setattr(orch, "call_agent", espia)

    lexico = LexicoComunitario()
    if sembrar:
        # Una propuesta que nadie del elenco firmó y que todos usan: se adopta
        # en el lugar donde esté quien la diga, no en «la comunidad».
        lexico.registrar_neologismo(Neologismo(
            turno=0, dia=0, autor="ElQueVino", forma=SEMBRADA,
            componentes="komo + -ana", significado="la cosa traída",
            contexto="", regla_aplicada="-ana"))
    observer = ObserverAgent(_Cliente(), lexico)
    memoria = orch.AgentMemory()
    competencia = CompetenciaLexica()
    campo = CampoLexico()
    escenas = []
    for t in range(turnos):
        escenas.append((state.dia, state.momento, orch.escena_de(state)))
        # El evento de nombramiento NO cambia en este PR (sigue yendo a los 12
        # del turno, decisión p8 = C es la capa 3): se dispara en el turno 1
        # para que haya competencias abiertas que V3 pueda filtrar después.
        referente = (orch.REFERENTES_NOVEDOSOS[0]
                     if (nombrar and t == 0) else None)
        orch.run_turn(_Cliente(), state, memoria, lexico, observer,
                      verbose=False, agentes_por_turno=agentes_por_turno,
                      roster=list(roster), competencia=competencia, campo=campo,
                      naming_referente=referente)
    return primeros, lexico, competencia, campo, escenas


def _estado_era2(escena=False, cada=0, dia=1):
    s = estado_inicial("PARAGUANÁ")
    s.turnos_por_dia = 6
    s.dia = dia
    s.escena = escena
    s.capubana_cada = cada
    s.evento_del_turno = None
    return s


def _linea(system: str, cabeza: str) -> str:
    return next((l for l in system.splitlines() if l.startswith(cabeza)), "")


# ══════════════════════════════════════════════════════════════════════
# (a) byte a byte
# ══════════════════════════════════════════════════════════════════════

def test_a1_la_era_1_es_byte_a_byte_con_ambito(monkeypatch):
    """En CURIANA `ambito_de` devuelve None y las cuatro vías siguen globales:
    tres turnos de prompts, carácter a carácter."""
    roster = orch.roster_de_habla("koine")[:6]
    con, *_ = _capturar(monkeypatch, estado_inicial_test(), roster=roster,
                        agentes_por_turno=6, turnos=3, con_modulo=True,
                        sembrar=True)
    sin, *_ = _capturar(monkeypatch, estado_inicial_test(), roster=roster,
                        agentes_por_turno=6, turnos=3, con_modulo=False,
                        sembrar=True)
    assert [c["agente"] for c in con] == [c["agente"] for c in sin]
    for c, s in zip(con, sin):
        assert c["system"] == s["system"], c["agente"]
        assert c["user"] == s["user"], c["agente"]
    # y hubo algo que comparar: las dos vías comunitarias salieron en el prompt
    assert any("[Palabras propuestas en evaluación" in c["system"] for c in con)
    assert any("[Palabras nuevas de la comunidad]" in c["system"] for c in con)
    assert not any("[Lo que se dijo aquí" in c["system"] for c in con)


def test_a2_la_era_2_sin_escena_es_byte_a_byte(monkeypatch):
    roster = list(era2.ALL_AGENTS)[:8]
    con, *_ = _capturar(monkeypatch, _estado_era2(escena=False), roster=roster,
                        agentes_por_turno=8, turnos=3, era=era2.ALL_AGENTS,
                        con_modulo=True, sembrar=True)
    sin, *_ = _capturar(monkeypatch, _estado_era2(escena=False), roster=roster,
                        agentes_por_turno=8, turnos=3, era=era2.ALL_AGENTS,
                        con_modulo=False, sembrar=True)
    assert [c["agente"] for c in con] == [c["agente"] for c in sin]
    for c, s in zip(con, sin):
        assert c["system"] == s["system"], c["agente"]
    assert any("[Palabras propuestas en evaluación" in c["system"] for c in con)
    assert not any("[Lo que se dijo aquí" in c["system"] for c in con)


def test_a3_sin_escena_el_estado_no_guarda_dichos(monkeypatch):
    state = _estado_era2(escena=False)
    _capturar(monkeypatch, state, roster=list(era2.ALL_AGENTS)[:6],
              agentes_por_turno=6, turnos=2, era=era2.ALL_AGENTS)
    assert state.dichos_del_turno_anterior == []


# ══════════════════════════════════════════════════════════════════════
# (b) con --escena: nadie oye a quien estaba en otro ámbito
# ══════════════════════════════════════════════════════════════════════

def _formas_de_v1(system: str) -> list[str]:
    linea = _linea(system, "[Palabras propuestas en evaluación")
    if not linea:
        return []
    return [t.split("'")[1] for t in linea.split("; ") if "'" in t]


def _formas_de_v2(system: str) -> list[str]:
    linea = _linea(system, "[Palabras nuevas de la comunidad]")
    if not linea:
        return []
    cuerpo = linea.split("]: ", 1)[1]
    return [p.split(" = ")[0].strip() for p in cuerpo.split("; ")]


def _formas_de_v3(system: str) -> list[str]:
    """Las formas rivales del bloque de competencias, y sólo de ése: el bloque
    de léxico también lleva flechas."""
    formas, dentro = [], False
    for linea in system.splitlines():
        if linea.startswith("[La comunidad aún busca nombre"):
            dentro = True
            continue
        if dentro:
            if not linea.startswith("  ") or " → " not in linea:
                break
            formas += [f.strip() for f in linea.split(" → ", 1)[1].split(",")]
    return formas


def _correr_con_escena(monkeypatch, *, turnos=6, cada=0, dia=1, nombrar=True):
    state = _estado_era2(escena=True, cada=cada, dia=dia)
    roster = list(era2.ALL_AGENTS)
    monkeypatch.setattr(orch, "ROSTER_NUCLEO", era2.ROSTER_NUCLEO)
    return state, _capturar(monkeypatch, state, roster=roster,
                            agentes_por_turno=12, turnos=turnos,
                            era=era2.ALL_AGENTS, sembrar=True, nombrar=nombrar)


def test_b_ninguna_via_cruza_de_ambito(monkeypatch):
    """Seis turnos sin Capubana: cada prompt sólo trae formas de SU lugar."""
    _, (prompts, lexico, competencia, _campo, escenas) = _correr_con_escena(
        monkeypatch, turnos=6)
    assert len(prompts) == 72, len(prompts)
    por_forma = {n.forma: n for n in lexico._neologismos}
    v1_vistos = v2_vistos = v3_vistos = 0

    for i, p in enumerate(prompts):
        escena = escenas[i // 12][2]
        aqui = escena[p["agente"]]
        for forma in _formas_de_v1(p["system"]):
            v1_vistos += 1
            neo = por_forma[forma]
            assert neo.ambito == aqui, (p["agente"], forma, neo.ambito, aqui)
        for forma in _formas_de_v2(p["system"]):
            v2_vistos += 1
            neo = por_forma[forma]
            assert aqui in neo.adoptado_en, (p["agente"], forma, neo.adoptado_en)
        for forma in _formas_de_v3(p["system"]):
            v3_vistos += 1
            assert aqui in competencia.ambitos_de_forma(forma), (forma, aqui)

    # Y hubo material: si no saliera ninguna forma, el test no mediría nada.
    assert v1_vistos > 20, v1_vistos
    assert v2_vistos > 0, v2_vistos
    assert v3_vistos > 0, v3_vistos
    # La sembrada se adoptó en algún lugar y su vía quedó declarada.
    sembrada = por_forma[SEMBRADA]
    assert sembrada.estado == "adoptado"
    assert sembrada.via in ("un-ambito", "dos-ambitos")
    assert all(a for a in sembrada.adoptado_en)


def test_b_el_ambito_es_el_lugar_y_no_el_nodo(monkeypatch):
    """Humohumo es de GUARANAO y Bajari de AMUAY, y los dos andan el camino
    Moruy–Caseto: comparten ámbito y se oyen. Una frontera por NODO los habría
    separado; el mapa dice que ese camino es el par más cercano de todos."""
    st = esc.EstadoDeEnsayo(dia=1, momento="mañana", estacion="viento")
    assert esc.ambito_de("Humohumo", st) == esc.ambito_de("Bajari", st)
    assert esc.ambito_de("Humohumo", st) == "camino:Moruy-Caseto"
    assert esc.nodo_de("Moruy") != esc.nodo_de("Caseto")


def test_b_en_el_dia_de_capubana_se_oye_todo(monkeypatch):
    """Ese día los 63 están en el cerro: un solo ámbito, y las vías vuelven a
    ser de toda la comunidad —que es lo que la convergencia significa."""
    _, (prompts, lexico, _c, _campo, escenas) = _correr_con_escena(
        monkeypatch, turnos=6, cada=3, dia=3)
    assert all(set(e.values()) == {"Capubana"} for _d, _m, e in escenas)
    por_forma = {n.forma: n for n in lexico._neologismos}
    # en el último turno del día ya hay propuestas de otros doce agentes
    formas = _formas_de_v1(prompts[-1]["system"])
    assert formas
    autores = {por_forma[f].autor for f in formas}
    assert len(autores) >= 2
    assert all(por_forma[f].ambito == "Capubana" for f in formas)


# ── El Capubana junta ÁMBITOS, no sólo cuerpos (2026-09-18) ──────────
# El día 1 de la serie C midió el fallo: con `--capubana-cada 3`, el día 3
# `ambito_de` devolvía "Capubana" para los 63 y eso era UN LUGAR MÁS, cuyo
# léxico era el de sus dos ocupantes del día 1 (71 formas): V2 vacía y las tres
# rivales de «las cuentas» a 0. El diseño (§4, decisión p7) dice que ese día
# TODOS ven TODO.

def test_b_el_dia_de_capubana_sirve_la_union_de_los_ambitos(monkeypatch):
    """Día 2 (víspera, repartidos) + día 3 (el cerro) + día 4 (repartidos).

    El día 3, V1/V2/V3 tienen que traer exactamente lo mismo que el mismo run
    SIN escena —la comunidad entera— y no lo del lugar «Capubana»; y el día 4
    vuelve el filtro por lugar."""
    _st, (con, lexico, _comp, _campo, escenas) = _correr_con_escena(
        monkeypatch, turnos=18, cada=3, dia=2)
    assert len(con) == 216
    # el control: los mismos turnos sin el brazo (la ventana y las respuestas
    # del doble son las mismas, así que el léxico evoluciona igual)
    sin, *_ = _capturar(monkeypatch, _estado_era2(escena=False, cada=0, dia=2),
                        roster=list(era2.ALL_AGENTS), agentes_por_turno=12,
                        turnos=12, era=era2.ALL_AGENTS, sembrar=True, nombrar=True)

    dia3 = range(72, 144)                       # turnos 7-12 = el día 3
    assert all(set(escenas[i][2].values()) == {"Capubana"} for i in range(6, 12))
    assert all(escenas[i][0] == 3 for i in range(6, 12))

    # (1) el conteo —y el contenido— iguala al del run sin escena
    for i in dia3:
        assert _formas_de_v1(con[i]["system"]) == _formas_de_v1(sin[i]["system"]), i
        assert _formas_de_v2(con[i]["system"]) == _formas_de_v2(sin[i]["system"]), i
        assert _formas_de_v3(con[i]["system"]) == _formas_de_v3(sin[i]["system"]), i

    # (2) y hubo unión de verdad: el cerro sirve formas propuestas en OTROS
    #     lugares el día anterior, que es lo que antes no pasaba.
    #     Ojo: un agente que vuelve a hablar vuelve a acuñar su forma, así que
    #     una misma forma puede tener varias entradas y varios ámbitos.
    ambitos_de = {}
    ambitos_antes = {}
    for n in lexico._neologismos:
        ambitos_de.setdefault(n.forma, set()).add(n.ambito)
        if n.dia < 3:
            ambitos_antes.setdefault(n.forma, set()).add(n.ambito)
    # En el PRIMER momento del día 3 todavía no se ha acuñado nada en el cerro:
    # lo que V1 sirve ahí viene entero de la víspera, y no del cerro.
    de_fuera = 0
    for i in range(72, 84):
        for forma in _formas_de_v1(con[i]["system"]):
            if "Capubana" not in ambitos_antes.get(forma, set()):
                de_fuera += 1
    assert de_fuera > 0, "el día de Capubana no trajo nada de fuera del cerro"

    # (3) y lo que se propone ESE día se registra en "Capubana", para que
    #     `adoptados_en_dos_ambitos` y el mapa lo vean
    del_dia3 = [n for n in lexico._neologismos if n.dia == 3]
    assert del_dia3 and all(n.ambito == "Capubana" for n in del_dia3)

    # (4) el día 4 vuelve el filtro por lugar
    dia4 = range(144, 216)
    assert all(escenas[i][0] == 4 for i in range(12, 18))
    assert any(set(escenas[i][2].values()) != {"Capubana"} for i in range(12, 18))
    v1_dia4 = 0
    for i in dia4:
        aqui = escenas[i // 12][2][con[i]["agente"]]
        for forma in _formas_de_v1(con[i]["system"]):
            v1_dia4 += 1
            assert aqui in ambitos_de[forma], (con[i]["agente"], forma, aqui)
    assert v1_dia4 > 0, "el día 4 no midió nada"


def test_b_el_dia_de_capubana_se_oye_a_cualquiera_del_momento_anterior(monkeypatch):
    """El primer momento del día del cerro oye lo que se dijo la noche antes
    repartido por los sitios: es la gente que acaba de subir."""
    _st, (con, *_r) = _correr_con_escena(monkeypatch, turnos=7, cada=3, dia=2)
    ultimo_del_dia2 = dict(esc._escena(2, "noche", "viento", 3))
    de_fuera = 0
    for p in con[72:]:                                    # el turno 1 del día 3
        for linea in p["system"].splitlines():
            if not linea.startswith("— "):
                continue
            quien = linea[2:].split(":", 1)[0]
            if ultimo_del_dia2.get(quien) not in (None, "Capubana"):
                de_fuera += 1
    assert de_fuera > 0, "el cerro no oyó a nadie de fuera del cerro"


def test_b_las_dos_puertas_dicen_cosas_distintas_solo_en_el_capubana():
    """`ambito_de` = dónde ESTÁ · `ambito_visible_de` = qué VE."""
    normal = esc.EstadoDeEnsayo(dia=2, momento="mañana", estacion="viento",
                                capubana_cada=3)
    cerro = esc.EstadoDeEnsayo(dia=3, momento="mañana", estacion="viento",
                               capubana_cada=3)
    sin = esc.EstadoDeEnsayo(dia=3, momento="mañana", estacion="viento",
                             escena=False, capubana_cada=3)
    for agente in ("Manaure", "Bajari", "Sawaka"):
        assert esc.ambito_visible_de(agente, normal) == esc.ambito_de(agente, normal)
        assert esc.ambito_de(agente, cerro) == "Capubana"
        assert esc.ambito_visible_de(agente, cerro) is None
        assert esc.ambito_visible_de(agente, sin) is None
    assert esc.sin_frontera(cerro) and not esc.sin_frontera(normal)
    assert not esc.sin_frontera(sin)
    # sin cadencia declarada no hay día de Capubana y no hay nada que abrir
    nunca = esc.EstadoDeEnsayo(dia=3, momento="mañana", estacion="viento",
                               capubana_cada=0)
    assert not esc.sin_frontera(nunca)
    assert esc.ambito_visible_de("Manaure", nunca) == esc.ambito_de("Manaure", nunca)


def test_b_sin_escena_la_misma_corrida_ve_formas_de_todas_partes(monkeypatch):
    """El contraste que hace del test de arriba una medición: sin el brazo,
    los mismos seis turnos ponen en el prompt formas de cualquier lugar."""
    state = _estado_era2(escena=False)
    prompts, lexico, *_ = _capturar(
        monkeypatch, state, roster=list(era2.ALL_AGENTS), agentes_por_turno=12,
        turnos=6, era=era2.ALL_AGENTS, sembrar=True)
    con_escena = esc.escena_de(_estado_era2(escena=True))
    por_forma = {n.forma: n for n in lexico._neologismos}
    cruces = 0
    for p in prompts:
        aqui = con_escena[p["agente"]]
        for forma in _formas_de_v1(p["system"]):
            autor = por_forma[forma].autor
            if autor in con_escena and con_escena[autor] != aqui:
                cruces += 1
    assert cruces > 0, "sin escena tendría que haber formas de otros lugares"


# ══════════════════════════════════════════════════════════════════════
# (c) [Lo que se dijo aquí]
# ══════════════════════════════════════════════════════════════════════

def test_c_el_bloque_no_aparece_en_el_primer_turno(monkeypatch):
    _, (prompts, *_rest) = _correr_con_escena(monkeypatch, turnos=1)
    assert len(prompts) == 12
    assert not any("[Lo que se dijo aquí" in p["system"] for p in prompts)


def test_c_el_bloque_trae_el_momento_anterior_del_mismo_lugar(monkeypatch):
    state, (prompts, _lex, _comp, _campo, escenas) = _correr_con_escena(
        monkeypatch, turnos=6)
    con_bloque = 0
    for i, p in enumerate(prompts):
        bloque = ""
        for trozo in p["system"].split("\n["):
            if trozo.startswith("Lo que se dijo aquí"):
                bloque = "[" + trozo.split("\n[", 1)[0]
        if not bloque:
            continue
        con_bloque += 1
        assert len(bloque) <= esc.PRESUPUESTO_OIR, len(bloque)
        voces = [l for l in bloque.splitlines() if l.startswith("— ")]
        assert 1 <= len(voces) <= esc.MAX_DICHOS, len(voces)
        # quien habla en el bloque estuvo en este lugar en el turno ANTERIOR,
        # y nunca es el propio agente ni alguien de este mismo turno
        aqui = escenas[i // 12][2][p["agente"]]
        antes = escenas[i // 12 - 1][2]
        for voz in voces:
            quien = voz[2:].split(":", 1)[0]
            assert quien != p["agente"]
            assert antes[quien] == aqui, (p["agente"], quien, aqui)
    # los turnos 2..6 tienen de qué hablar
    assert con_bloque > 10, con_bloque


def test_c_nunca_trae_lo_del_mismo_turno(monkeypatch):
    """Si el bloque trajera lo del mismo turno, el orden de habla volvería a
    ser destino: es el mecanismo de V1 que produjo los tres cruces de
    Δturnos = 0 del día 1 de la serie B."""
    state, (prompts, *_r) = _correr_con_escena(monkeypatch, turnos=2)
    segundos = prompts[12:]
    dichos_del_primer_turno = {_raiz(p["agente"]) for p in prompts[:12]}
    for p in segundos:
        if "[Lo que se dijo aquí" not in p["system"]:
            continue
        # las voces del bloque son del turno 1 y nunca de alguien del turno 2
        # que hable después: se comprueba por el nombre, que va en la línea
        for linea in p["system"].splitlines():
            if linea.startswith("— "):
                quien = linea[2:].split(":", 1)[0]
                assert _raiz(quien) in dichos_del_primer_turno


def test_c_frase_dicha_recorta_la_glosa_y_no_el_caquetio():
    texto = ("Taya naa-ka biro-ana wara kari (he raspado la costra de sal). "
             "[biro-ana: biro + -ana = la costra].")
    assert esc.frase_dicha(texto) == "Taya naa-ka biro-ana wara kari"
    # elige la oración caquetía aunque venga después de una castellana
    mixto = "Miro el agua y pienso. Nüma maa-ni ta-barsure."
    assert esc.frase_dicha(mixto) == "Nüma maa-ni ta-barsure"
    # recorta con puntos suspensivos y respeta el tope
    largo = "taya " + "naa-ka " * 40
    assert len(esc.frase_dicha(largo)) <= esc.TOPE_FRASE + 1
    assert esc.frase_dicha("(sólo glosa)") == ""


def test_c_el_tope_de_280_se_respeta_con_frases_largas():
    """Tres voces de 70 caracteres más la cabecera pasan de 280: el bloque
    recorta voces, no las parte."""
    frase = "taya naa-ka " + "wara-kari " * 6
    dichos = [{"agente": f"Agente{i}", "lugar": "Moruy",
               "frase": esc.frase_dicha(frase)} for i in range(5)]
    st = esc.EstadoDeEnsayo(dia=1, momento="mediodia",
                            dichos_del_turno_anterior=dichos)
    bloque = esc.bloque_lo_que_se_dijo_aqui("Manaure", st)
    assert 0 < len(bloque) <= esc.PRESUPUESTO_OIR
    assert bloque.count("\n— ") <= esc.MAX_DICHOS


def test_c_continuar_hereda_los_dichos():
    from curiana_state import ComunidadState
    s = ComunidadState(escena=True)
    s.dichos_del_turno_anterior = [{"agente": "Karebe", "lugar": "Moruy",
                                    "frase": "taya naa-ka"}]
    d = s.to_dict()
    assert ComunidadState.from_dict(d).dichos_del_turno_anterior == \
        s.dichos_del_turno_anterior
    d.pop("dichos_del_turno_anterior")
    assert ComunidadState.from_dict(d).dichos_del_turno_anterior == []


def test_c_el_ensayo_de_oir_imprime_los_largos():
    r = subprocess.run([sys.executable, "curiana_escena.py", "--oir"], cwd=SIM,
                       capture_output=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    salida = r.stdout.decode("utf-8")
    assert "[Lo que se dijo aquí" in salida
    assert f"tope {esc.PRESUPUESTO_OIR}" in salida
    assert f"tope {esc.MAX_DICHOS}" in salida
    assert "escenas traen bloque" in salida


# ══════════════════════════════════════════════════════════════════════
# (d) el JSON viejo del léxico
# ══════════════════════════════════════════════════════════════════════

def test_d_un_lexico_json_anterior_a_la_escena_carga(tmp_path):
    """Los campos del ámbito nacen con valor por defecto: un run guardado
    antes del 2026-09-17 no los trae y tiene que cargar igual."""
    viejo = {
        "lexico": {"biro-ana": {"significado": "la costra", "autor": "Birokoa",
                                "dia": 1}},
        "neologismos": [{
            "turno": 1, "dia": 1, "autor": "Birokoa", "forma": "biro-ana",
            "componentes": "biro + -ana", "significado": "la costra",
            "contexto": "…", "regla_aplicada": "-ana", "estado": "adoptado",
            "adoptado_por": ["Kasebo", "Waranaro"], "rechazado_por": [],
            "turno_resolucion": 2, "dia_resolucion": 1,
        }],
    }
    ruta = tmp_path / "curiana_lexico.json"
    ruta.write_text(json.dumps(viejo, ensure_ascii=False), encoding="utf-8")
    lex = LexicoComunitario.load(str(ruta))
    neo = lex._neologismos[0]
    assert neo.forma == "biro-ana" and neo.estado == "adoptado"
    assert neo.ambito is None and neo.adoptado_en == [] and neo.via is None
    assert lex.ambitos_vistos() == []
    # y sigue saliendo en el prompt global, como siempre
    assert "biro-ana" in prompt_lexico_activo(lex)
    # con ámbito no sale: nadie lo adoptó aquí, porque no había «aquí»
    assert prompt_lexico_activo(lex, "Moruy") == ""
    # y se puede volver a guardar y releer sin perder nada
    lex.save(str(ruta))
    assert LexicoComunitario.load(str(ruta))._neologismos[0].adoptado_en == []


def test_d_la_oficializacion_por_ambito_y_la_via_de_dos_ambitos():
    lex = LexicoComunitario()
    lex.situar("Birokoa", "Tacuato:salinar")
    lex.registrar_neologismo(Neologismo(
        turno=1, dia=1, autor="Birokoa", forma="biro-ana",
        componentes="biro + -ana", significado="la costra", contexto="",
        regla_aplicada="-ana"))
    assert lex._neologismos[0].ambito == "Tacuato:salinar"
    # V1: sólo lo ve quien está en el salinar
    assert "biro-ana" in prompt_pendientes_evaluacion(lex, "Tacuato:salinar")
    assert prompt_pendientes_evaluacion(lex, "Moruy") == ""
    assert "biro-ana" in prompt_pendientes_evaluacion(lex)      # global: igual

    lex.situar("Kasebo", "Tacuato:salinar")
    assert lex.adoptar("biro-ana", "Kasebo", turno=2) is None
    lex.situar("Waranaro", "Moruy")
    oficial = lex.adoptar("biro-ana", "Waranaro", turno=3, dia=1)
    assert oficial is not None
    assert oficial.via == "dos-ambitos"
    assert oficial.oficial_en == ["Tacuato:salinar", "Moruy"]
    assert lex.adoptados_en_dos_ambitos() == [oficial]
    # V2: la ven los dos lugares donde se adoptó, y nadie más
    assert "biro-ana" in prompt_lexico_activo(lex, "Tacuato:salinar")
    assert "biro-ana" in prompt_lexico_activo(lex, "Moruy")
    assert prompt_lexico_activo(lex, "Caseto") == ""
    # y el diccionario de cierre lo dice
    assert "adoptadas en DOS ámbitos: 1" in lex.reporte_linguistico()


def test_d_un_solo_ambito_no_es_la_via_de_dos():
    lex = LexicoComunitario()
    for quien in ("Birokoa", "Kasebo", "Ebokoa"):
        lex.situar(quien, "Tacuato:orilla")
    lex.registrar_neologismo(Neologismo(
        turno=1, dia=1, autor="Birokoa", forma="hime-ana", componentes="hime + -ana",
        significado="x", contexto="", regla_aplicada="-ana"))
    lex.adoptar("hime-ana", "Kasebo", turno=2)
    oficial = lex.adoptar("hime-ana", "Ebokoa", turno=2, dia=1)
    assert oficial.via == "un-ambito" and oficial.oficial_en == ["Tacuato:orilla"]
    assert lex.adoptados_en_dos_ambitos() == []


def test_d_sin_ambito_el_reporte_no_menciona_ambitos():
    """La era 1: el diccionario de cierre es el de siempre."""
    lex = LexicoComunitario()
    lex.registrar_neologismo(Neologismo(
        turno=1, dia=1, autor="Shaboro", forma="kasi-ni", componentes="kasi + -ni",
        significado="x", contexto="", regla_aplicada="-ni"))
    lex.adoptar("kasi-ni", "Tawaka", turno=2)
    neo = lex.adoptar("kasi-ni", "Manaure", turno=2, dia=1)
    assert neo.via is None and neo.oficial_en == []
    assert "ámbito" not in lex.reporte_linguistico()


def test_d_las_competencias_filtran_por_donde_se_propuso():
    comp = CompetenciaLexica()
    comp.activar("cometa", "una estrella con cola")
    # `kashi` se archivó en la tanda final (tf.5): una raíz archivada ya no
    # compite. El ejemplo pasa a `danu`, su sustituta.
    comp.proponer("cometa", "danu-iro", "Birokoa", ambito="Tacuato:orilla")
    # `wara` → `unia` como raíz de la rival: `wara` se archivó (tanda de las
    # hermanas, 2026-09-24) y una raíz archivada ya no compite.
    comp.proponer("cometa", "unia-bana", "Bajari", ambito="Caseto")
    entero = comp.prompt_competencias()
    assert "danu-iro" in entero and "unia-bana" in entero
    solo_tacuato = comp.prompt_competencias(ambito="Tacuato:orilla")
    assert "danu-iro" in solo_tacuato and "unia-bana" not in solo_tacuato
    assert comp.prompt_competencias(ambito="Moruy") == ""
    # la fijación NO se parte: el soporte suma venga del ámbito que venga
    assert set(comp.referentes["cometa"]["variantes"]) == {"danu-iro", "unia-bana"}


# ══════════════════════════════════════════════════════════════════════
# (e) el campo por ámbito suma al global
# ══════════════════════════════════════════════════════════════════════

def test_e_el_campo_por_ambito_suma_al_global():
    campo = CampoLexico()
    campo.registrar(["kari", "wara"], ambito="Moruy")
    campo.registrar(["kari"], ambito="Caseto")
    assert campo.pesos_de("Moruy") == {"kari": 1.0, "wara": 1.0}
    assert campo.pesos_de("Caseto") == {"kari": 1.0}
    assert campo.pesos == {"kari": 2.0, "wara": 1.0}
    assert campo.peso("kari") == 2.0 and campo.peso("kari", "Caseto") == 1.0
    assert sorted(a for a in campo.ambitos() if a) == ["Caseto", "Moruy"]
    # sin ámbito se ve el global, no «el ámbito nulo»
    assert campo.pesos_de(None) == campo.pesos
    assert campo.top(1) == [("kari", 2.0)]


def test_e_sin_ambito_el_campo_es_el_de_siempre():
    campo = CampoLexico(decaimiento=0.5)
    campo.registrar(["kari", "wara"])
    campo.registrar(["kari"])
    assert campo.pesos == {"kari": 2.0, "wara": 1.0}
    assert campo.pesos_de(None) is campo.por_ambito[None]   # el mismo objeto
    campo.decaer()
    assert campo.pesos == {"kari": 1.0, "wara": 0.5}
    for _ in range(4):                 # wara cae por debajo de 0.05 y muere
        campo.decaer()
    assert "wara" not in campo.pesos and "kari" in campo.pesos


def test_e_el_campo_por_ambito_sobrevive_a_continuar(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    campo = CampoLexico()
    campo.registrar(["kari"], ambito="Moruy")
    campo.registrar(["wara"], ambito="Caseto")
    koine.guardar_koine({}, campo)
    _idio, vuelto, _comp = koine.cargar_koine()
    assert vuelto.pesos_de("Moruy") == {"kari": 1.0}
    assert vuelto.pesos_de("Caseto") == {"wara": 1.0}
    assert vuelto.pesos == campo.pesos
    # un JSON anterior a la escena (sólo el global) entra en el ámbito nulo
    datos = json.loads((tmp_path / koine.KOINE_PATH).read_text(encoding="utf-8"))
    datos["campo"].pop("por_ambito")
    (tmp_path / koine.KOINE_PATH).write_text(json.dumps(datos), encoding="utf-8")
    _i2, viejo, _c2 = koine.cargar_koine()
    assert viejo.por_ambito == {None: {"kari": 1.0, "wara": 1.0}}


def test_e_run_turn_registra_en_el_campo_del_hablante(monkeypatch):
    _st, (prompts, _lex, _comp, campo, escenas) = _correr_con_escena(
        monkeypatch, turnos=2)
    ambitos = [a for a in campo.ambitos() if a]
    assert len(ambitos) > 1, ambitos
    assert None not in campo.ambitos()
    # con 12 voces por turno sobre un roster de 63, nadie repite en dos turnos:
    # cada forma acuñada pesa en el lugar donde se dijo, y en ningún otro
    hablaron = [p["agente"] for p in prompts]
    assert len(set(hablaron)) == len(hablaron)
    for i, p in enumerate(prompts):
        agente = p["agente"]
        forma, aqui = _raiz(agente) + "-ana", escenas[i // 12][2][agente]
        assert campo.peso(forma, aqui) > 0, (agente, forma, aqui)
        fuera = [a for a in ambitos if a != aqui and campo.peso(forma, a) > 0]
        assert not fuera, (agente, forma, fuera)
    # y el global sigue siendo la suma
    total = {}
    for a in campo.ambitos():
        for f, peso in campo.pesos_de(a).items():
            total[f] = total.get(f, 0.0) + peso
    assert campo.pesos == total
