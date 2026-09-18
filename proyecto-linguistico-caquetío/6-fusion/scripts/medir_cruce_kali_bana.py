#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
¿`kali-bana` viajó de Moruy a Carirubana, o se re-acuñó allí?

Mide el día 1 de la serie C (run `b7bc51dc`, brazo `--escena --capubana-cada 3`,
semilla 21), el primer día en que el ámbito de lo que un agente VE es el LUGAR.

    6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md
    §2 capa 2 (OÍR) · §5 (medición)

Contesta tres preguntas y NO toca el motor:

  1. `kali-bana` — quién la dijo, en qué lugar y en qué orden dentro del turno;
     qué vía podía haberla llevado hasta cada usuario (V1 propuestas, V2
     adoptadas, V3 competencias y V4 el campo, las cuatro POR ÁMBITO; el bloque
     `[Lo que se dijo aquí]`; el contagio léxico, que NO está partido por
     ámbito; y `procesar_adopciones`, que ve todas las pendientes) y si el
     compuesto es re-acuñable de forma independiente.
  2. La disputa de «las cuentas brillantes»: las tres formas rivales, quién las
     dijo, dónde, con qué soporte de competencia reconstruido y con qué peso
     por lugar en `CampoLexico` (`curiana_koine.json` → `campo.por_ambito`).
  3. Las formas que nacieron en VARIOS lugares a la vez: cuántas son del evento
     de nombramiento, cuántas son formas que el propio prompt enseña y cuántas
     quedan sin explicar.

REGLAS DE LA CASA QUE ESTE SCRIPT RESPETA
  · No llama a la API de Anthropic ni lee `curiana_sim/.env`. No importa
    `curiana_orchestrator_v2` —importarlo arrastra `curiana_database` y su
    `load_dotenv()`—: la única constante suya que hace falta
    (`_IDENTIDAD_LINGUISTICA`) se saca del fichero con `ast`, sin ejecutarlo.
    Es el mismo patrón que `medir_presupuesto_escena.py`.
  · La base se consulta con `docker exec supabase_db_curiana_sim psql`, en
    sólo lectura, como manda CLAUDE.md (puertos 64321/64322; la CLI no).
  · Ninguna cifra se escribe a mano: todo lo que sale por pantalla se cuenta
    aquí.

USO
    python 6-fusion/scripts/medir_cruce_kali_bana.py
    python 6-fusion/scripts/medir_cruce_kali_bana.py --run b7bc51dc
    python 6-fusion/scripts/medir_cruce_kali_bana.py --forma kali-bana
    python 6-fusion/scripts/medir_cruce_kali_bana.py --json

Los `curiana_*.json` del cierre (léxico, koiné, estado) son el residuo del run
en el checkout donde se corrió y están gitignorados: no viven en un worktree.
Con `--estado-dir` se le dice dónde están; por defecto, `curiana_sim/` del
propio repo.
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.normpath(os.path.join(_AQUI, "..", ".."))
_SIM = os.path.join(_RAIZ, "curiana_sim")

# El elenco se decide ANTES de importar curiana_agents (CLAUDE.md, trampas).
os.environ.setdefault("CURIANA_ELENCO", "era2")
sys.path.insert(0, _SIM)

CONTENEDOR = "supabase_db_curiana_sim"
RUN_POR_DEFECTO = "b7bc51dc"
FORMA_POR_DEFECTO = "kali-bana"
CADENCIA_NOMBRAMIENTO = 4          # curiana_orchestrator_v2.py:1521
UMBRAL_CONTAGIO = 0.6              # curiana_social.DifusionLexica(umbral_adopcion)


def _forzar_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                   # pragma: no cover
        pass


# ══════════════════════════════════════════════════════════════════════
# 0. La base, en sólo lectura y por psql
# ══════════════════════════════════════════════════════════════════════

def consulta(sql: str):
    """Una consulta a la Supabase LOCAL, devuelta como lista de dicts.

    Va por `docker exec … psql` a propósito: es la puerta que CLAUDE.md
    declara y la única que no necesita credenciales del `.env`."""
    envoltorio = f"select coalesce(json_agg(t), '[]'::json) from ({sql}) t"
    proc = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d", "postgres",
         "-Atc", envoltorio],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit("psql falló:\n" + proc.stderr.decode("utf-8", "replace"))
    return json.loads(proc.stdout.decode("utf-8"))


def run_completo(prefijo: str) -> dict:
    filas = consulta(
        "select id::text as id, started_at::text as started_at, total_turns, "
        "total_days, model, config from simulation_runs "
        f"where id::text like '{prefijo}%' order by started_at desc limit 1")
    if not filas:
        raise SystemExit(f"no hay run que empiece por {prefijo} en la base local")
    return filas[0]


# ══════════════════════════════════════════════════════════════════════
# 1. Lo que el prompt ENSEÑA — sin importar el orquestador
# ══════════════════════════════════════════════════════════════════════

def constante_del_orquestador(nombre: str):
    """Una constante de curiana_orchestrator_v2, leída con `ast` y sin
    ejecutar el módulo: importarlo arrastra curiana_database → load_dotenv."""
    ruta = os.path.join(_SIM, "curiana_orchestrator_v2.py")
    with open(ruta, encoding="utf-8") as f:
        arbol = ast.parse(f.read())
    for n in arbol.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == nombre:
            return ast.literal_eval(n.value)
    raise SystemExit(f"no encuentro {nombre} en curiana_orchestrator_v2.py")


def formas_excluidas():
    """`_FORMAS_EXCLUIDAS` del orquestador, reconstruida pieza a pieza.

    Es el conjunto que el propio motor declara como «lo que las plantillas
    ENSEÑAN»: vocabulario base + identidad lingüística + las dos plantillas de
    reglas. Una forma de aquí NO es koiné: es copia del prompt."""
    from curiana_lexicon import (VOCABULARIO_BASE, formas_en_texto,
                                 prompt_reglas_completo, prompt_reglas_breve)
    ident = constante_del_orquestador("_IDENTIDAD_LINGUISTICA")
    return (frozenset(VOCABULARIO_BASE)
            | formas_en_texto(ident)
            | formas_en_texto(prompt_reglas_completo())
            | formas_en_texto(prompt_reglas_breve())), ident


def transparencia(forma: str, componentes: str) -> dict:
    """¿Es un compuesto que CUALQUIER agente podría armar solo?

    Transparente = todos sus componentes son (a) voz del vocabulario base que
    el muestreador puede enseñar, o (b) un afijo que la identidad lingüística
    o las reglas nombran. Si lo es, verla en dos lugares a la vez no prueba
    que haya viajado: prueba que los dos lugares tienen los mismos ladrillos."""
    from curiana_lexicon import VOCABULARIO_BASE, prompt_reglas_completo
    ident = constante_del_orquestador("_IDENTIDAD_LINGUISTICA")
    ensenado = (ident + "\n" + prompt_reglas_completo()).lower()
    piezas = [p.strip().strip("-").lower()
              for p in re.split(r"[+\s]+", componentes or "") if p.strip(" +-")]
    if not piezas:
        piezas = [p for p in forma.lower().split("-") if p]
    detalle = []
    for p in piezas:
        en_base = p in VOCABULARIO_BASE
        en_plantilla = bool(re.search(r"(?<![\w-])-?" + re.escape(p) + r"(?![\w])",
                                      ensenado))
        detalle.append({"pieza": p, "en_vocabulario_base": en_base,
                        "en_plantilla": en_plantilla})
    return {"piezas": detalle,
            "transparente": all(d["en_vocabulario_base"] or d["en_plantilla"]
                                for d in detalle)}


# ══════════════════════════════════════════════════════════════════════
# 2. El run, reconstruido: quién habló, dónde y en qué orden
# ══════════════════════════════════════════════════════════════════════

def cargar_run(run_id: str) -> dict:
    turnos = consulta(
        "select id::text as id, day, turn_num, moment, event_description "
        f"from turns where run_id='{run_id}' order by day, turn_num")
    respuestas = consulta(
        "select ar.id::text as id, t.day, t.turn_num, t.moment, ar.agent_name, "
        "ar.tier, ar.response_text, ar.lugar, ar.created_at::text as created_at "
        "from agent_responses ar join turns t on t.id=ar.turn_id "
        f"where ar.run_id='{run_id}' order by t.day, t.turn_num, ar.created_at")
    presencias = consulta(
        "select p.day, p.turn_num, p.momento, p.agent_name, p.lugar, p.nodo "
        f"from presencias p where p.run_id='{run_id}' order by p.turn_num, p.agent_name")
    usos = consulta(
        "select t.day, t.turn_num, wu.agent_name, wu.word, wu.response_id::text "
        "as response_id from word_uses wu join turns t on t.id=wu.turn_id "
        f"where wu.run_id='{run_id}' order by t.day, t.turn_num")
    neos_db = consulta(
        "select form, components, meaning, proposed_by, proposed_day, status, "
        f"adopted_by from neologisms where run_id='{run_id}' order by form")
    koine = consulta("select concepto_id, form, fijada_dia, soporte, n_variantes "
                     f"from koine_lexicon where run_id='{run_id}'")
    return {"turnos": turnos, "respuestas": respuestas, "presencias": presencias,
            "usos": usos, "neologismos_db": neos_db, "koine_lexicon": koine}


def indice_de_lugar(presencias):
    return {(p["day"], p["turn_num"], p["agent_name"]): p["lugar"] for p in presencias}


def indice_de_nodo(presencias):
    return {p["agent_name"]: p["nodo"] for p in presencias}


def nodo_de_lugar(presencias):
    """Qué nodo(s) ocupan cada lugar. Un lugar con los dos es contacto."""
    m = defaultdict(set)
    for p in presencias:
        if p["lugar"] and p["nodo"]:
            m[p["lugar"]].add(p["nodo"])
    return {lug: sorted(nod) for lug, nod in m.items()}


# ══════════════════════════════════════════════════════════════════════
# 3. Las vías, reconstruidas por ámbito
# ══════════════════════════════════════════════════════════════════════

def neologismos_del_cierre(estado_dir: str) -> list:
    """Los neologismos con su ámbito, tal y como quedaron en `curiana_lexico.json`.

    La base (`neologisms`) NO guarda el ámbito: `ambito`, `adoptado_en`,
    `oficial_en` y `via` sólo viven en el JSON del cierre."""
    ruta = os.path.join(estado_dir, "curiana_lexico.json")
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8") as f:
        return json.load(f).get("neologismos") or []


def campo_por_ambito(estado_dir: str) -> dict:
    """`CampoLexico.pesos_de(ambito)` del cierre (`curiana_koine.json`)."""
    ruta = os.path.join(estado_dir, "curiana_koine.json")
    if not os.path.exists(ruta):
        return {}
    with open(ruta, encoding="utf-8") as f:
        campo = json.load(f).get("campo") or {}
    return {"global": campo.get("pesos") or {},
            "por_ambito": campo.get("por_ambito") or {}}


def v1_en(neos, ambito, dia, turno, top=5):
    """`prompt_pendientes_evaluacion(lexico, ambito)` reconstruida.

    Pendiente en (día, turno) = propuesta ANTES y todavía sin resolver
    entonces. Se filtra por dónde se PROPUSO (`Neologismo.ambito`) y se
    muestran las 5 últimas, como el motor."""
    vivas = []
    for n in neos:
        if n.get("ambito") != ambito:
            continue
        if (n["dia"], n["turno"]) >= (dia, turno):
            continue
        tr, dr = n.get("turno_resolucion"), n.get("dia_resolucion")
        if tr is not None and dr is not None and (dr, tr) < (dia, turno):
            continue
        vivas.append(n["forma"])
    return vivas[-top:]


def v2_en(neos, ambito, dia, turno, top=15):
    """`prompt_lexico_activo(lexico, ambito)`: las adoptadas AQUÍ (V2)."""
    vivas = []
    for n in neos:
        if ambito not in (n.get("adoptado_en") or ()):
            continue
        tr, dr = n.get("turno_resolucion"), n.get("dia_resolucion")
        if tr is None or dr is None or (dr, tr) >= (dia, turno):
            continue
        vivas.append(n["forma"])
    return vivas[-top:]


def dichos_por_turno(respuestas, lugar_de):
    """`state.dichos_del_turno_anterior` reconstruido turno a turno.

    Usa las mismas funciones del motor (`curiana_escena.frase_dicha`) y la
    misma puerta de texto libre (`curiana_eventos.decir_para_el_mundo`)."""
    from curiana_escena import frase_dicha
    from curiana_eventos import decir_para_el_mundo
    decir = lambda t: decir_para_el_mundo(t, "PARAGUANÁ")
    salida = defaultdict(list)
    for r in respuestas:
        lugar = lugar_de.get((r["day"], r["turn_num"], r["agent_name"]))
        if not lugar:
            continue
        frase = frase_dicha(decir(r["response_text"] or ""))
        if frase:
            salida[(r["day"], r["turn_num"])].append(
                {"agente": r["agent_name"], "lugar": lugar, "frase": frase})
    return salida


def bloque_oir(agente, lugar, dichos_previos, maximo=3):
    from curiana_escena import dichos_aqui
    return dichos_aqui(agente, lugar, dichos_previos, maximo)


def exposicion_de_contagio(respuestas, neos, usos, lugar_de, formas_base,
                           hasta, forma):
    """La QUINTA vía, la que el diseño no contó: `DifusionLexica`.

    El bloque «[Has oído estas palabras nuevas en boca de gente que respetas]»
    no está partido por ámbito: viaja por `curiana_social.vecinos()` = vínculos
    resueltos + co-ubicación. Se reconstruye igual que el motor: cada uso de
    una forma emergente y cada acuñación suben la exposición de los vecinos del
    hablante en `prestigio_de(hablante) × peso_del_vinculo`.

    Devuelve {agente: exposición acumulada a `forma`} hasta (día, turno)
    excluidos."""
    from curiana_social import vecinos, prestigio_de, PESO_COUBICACION  # noqa: F401
    usos_por_respuesta = defaultdict(list)
    for u in usos:
        usos_por_respuesta[u["response_id"]].append(u["word"])
    neos_por_autor_turno = defaultdict(list)
    for n in neos:
        neos_por_autor_turno[(n["dia"], n["turno"], n["autor"])].append(n["forma"])

    exposicion = Counter()
    for r in respuestas:
        if (r["day"], r["turn_num"]) >= hasta:
            break
        dichas = set(usos_por_respuesta.get(r["id"], []))
        dichas -= formas_base
        dichas |= set(neos_por_autor_turno.get(
            (r["day"], r["turn_num"], r["agent_name"]), []))
        if forma not in dichas:
            continue
        # `vecinos()` sin state: los vínculos resueltos + la co-ubicación por
        # `ubicacion_default`. La co-ubicación REAL del turno la escribe
        # `ubicaciones_override`, que aquí se sustituye por `presencias`.
        red = vecinos(r["agent_name"])
        lugar = lugar_de.get((r["day"], r["turn_num"], r["agent_name"]))
        if lugar:
            for otro, l2 in lugar_de.items():
                if l2 == lugar and otro[2] != r["agent_name"] and otro[:2] == (
                        r["day"], r["turn_num"]):
                    red[otro[2]] = max(red.get(otro[2], 0.0), PESO_COUBICACION)
        p = prestigio_de(r["agent_name"])
        for vecino, peso in red.items():
            exposicion[vecino] += p * peso
    return exposicion


# ══════════════════════════════════════════════════════════════════════
# 4. La competencia léxica, reconstruida
# ══════════════════════════════════════════════════════════════════════

def reconstruir_competencia(respuestas, neos, usos, turno_nombramiento):
    """`CompetenciaLexica` del día, re-ejecutada sobre lo que la base guardó.

    Hace falta reconstruirla porque **no se persiste**: `guardar_koine()`
    escribe idiolectos y campo, nada más. El modelo es el del motor:
      proponer      +1.0 + prestigio(agente)   (sólo en el turno de nombramiento)
      registrar_uso +0.5 + prestigio(agente)   (reuso de una forma ya en liza)
    `registrar_uso` se alimenta de `palabras_caquetias`, que NO es lo mismo que
    `word_uses`: la tabla guarda además lo que esa respuesta ACUÑA
    (`save_agent_response(..., coined_words=…)`). Una forma recién acuñada no
    es una `palabra_activa` (CLAUDE.md), así que en el motor su autor NO la
    re-puntúa en el mismo turno: aquí se descuenta explícitamente."""
    from curiana_social import prestigio_de
    usos_por_respuesta = defaultdict(list)
    for u in usos:
        usos_por_respuesta[u["response_id"]].append(u["word"])
    neos_por_autor_turno = defaultdict(list)
    for n in neos:
        neos_por_autor_turno[(n["dia"], n["turno"], n["autor"])].append(n["forma"])

    soporte = Counter()
    forma2concepto = {}
    propuestas = defaultdict(list)
    reusos = defaultdict(list)
    for r in respuestas:
        p = prestigio_de(r["agent_name"])
        propias = set(neos_por_autor_turno.get(
            (r["day"], r["turn_num"], r["agent_name"]), []))
        if r["turn_num"] == turno_nombramiento:
            for forma in neos_por_autor_turno.get(
                    (r["day"], r["turn_num"], r["agent_name"]), []):
                soporte[forma] += 1.0 + p
                forma2concepto[forma.lower()] = True
                propuestas[forma].append(r["agent_name"])
        for forma in usos_por_respuesta.get(r["id"], []):
            if forma in propias:
                continue                     # lo que acuñó no es `palabra_activa`
            if forma.lower() in forma2concepto:
                soporte[forma] += 0.5 + p
                reusos[forma].append(r["agent_name"])
    return soporte, propuestas, reusos


# ══════════════════════════════════════════════════════════════════════
# 5. Las formas emergentes y dónde nacieron
# ══════════════════════════════════════════════════════════════════════

def cruce_por_lugar(usos, neos_db, koine, excluidas, lugar_de, turnos_por_dia=6):
    """Igual que `analizar_nodos.cruce_por_lugar`, para poder cruzarlo con el
    origen de cada forma (plantilla / nombramiento / resto)."""
    emergentes = {u["word"] for u in usos if u["word"] not in excluidas}
    emergentes |= {n["form"] for n in neos_db}
    emergentes |= {k["form"] for k in koine}
    por_forma = defaultdict(list)
    for u in usos:
        if u["word"] in emergentes:
            lugar = lugar_de.get((u["day"], u["turn_num"], u["agent_name"]))
            if lugar:
                por_forma[u["word"]].append(
                    (u["day"], u["turn_num"], lugar, u["agent_name"]))
    filas = []
    for forma, ubic in sorted(por_forma.items()):
        ubic.sort()
        d0, t0, _, _ = ubic[0]
        natales = sorted({l for d, t, l, _ in ubic if (d, t) == (d0, t0)})
        fuera = [(d, t, l) for d, t, l, _ in ubic if l not in natales]
        filas.append({
            "forma": forma, "usos": len(ubic),
            "lugares": sorted({l for _, _, l, _ in ubic}),
            "natales": natales, "multilugar": len(natales) > 1,
            "dia": d0, "turno": t0,
            "salida": min(fuera) if fuera else None,
            "murio_en_su_lugar": not fuera and len(natales) == 1,
            "hablantes_natales": sorted({a for d, t, _, a in ubic if (d, t) == (d0, t0)}),
        })
    return filas, emergentes


# ══════════════════════════════════════════════════════════════════════
# 6. Informe
# ══════════════════════════════════════════════════════════════════════

def tit(txt):
    print("\n" + "─" * 78)
    print(f"  {txt}")
    print("─" * 78)


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default=RUN_POR_DEFECTO, help="prefijo del run (id8)")
    ap.add_argument("--forma", default=FORMA_POR_DEFECTO, help="la forma a rastrear")
    ap.add_argument("--estado-dir", default=_SIM,
                    help="dónde están los curiana_*.json del cierre")
    ap.add_argument("--json", action="store_true", help="volcado en JSON")
    args = ap.parse_args()

    run = run_completo(args.run)
    cfg = run["config"] or {}
    datos = cargar_run(run["id"])
    lugar_de = indice_de_lugar(datos["presencias"])
    nodo_de = indice_de_nodo(datos["presencias"])
    nodos_del_lugar = nodo_de_lugar(datos["presencias"])
    excluidas, ident = formas_excluidas()
    neos = neologismos_del_cierre(args.estado_dir)
    campo = campo_por_ambito(args.estado_dir)
    if not neos or not campo:
        print(f"\n  ⚠ no encuentro los `curiana_*.json` del cierre en "
              f"{args.estado_dir}.")
        print("    Están gitignorados y viven en el CHECKOUT donde se corrió el "
              "run, no en un worktree.")
        print("    Sin ellos no hay ámbito por neologismo (`ambito`, "
              "`adoptado_en`, `via`) ni `CampoLexico.por_ambito`, y las "
              "secciones 2, 4 y 7 saldrían en cero.")
        print("    Pásalo con --estado-dir <ruta>/curiana_sim.")
        raise SystemExit(2)
    turnos_por_dia = int(cfg.get("turnos_por_dia") or 6)
    # El nombramiento cae en el turno `t % 4 == 0` del bucle 0-based → turno 5.
    turno_nombramiento = CADENCIA_NOMBRAMIENTO + 1
    forma = args.forma.lower()
    patron = re.compile(r"(?<![\w\-])" + re.escape(forma) + r"(?![\w\-])")

    salida = {"run": run["id"], "config": cfg}

    # ── 0. El run ──────────────────────────────────────────────────────
    tit(f"EL RUN — {run['id'][:8]} · {run['started_at'][:16]}")
    print(f"  serie {cfg.get('serie')} · elenco {cfg.get('elenco')} · perfil "
          f"{cfg.get('perfil')} · semilla {cfg.get('semilla')}")
    print(f"  escena {cfg.get('escena')} · capubana_cada {cfg.get('capubana_cada')} "
          f"· roster {cfg.get('roster')} ({cfg.get('roster_n')}) · "
          f"{cfg.get('agentes_por_turno')} agentes/turno · "
          f"{turnos_por_dia} turnos/día · continuado_desde "
          f"{cfg.get('continuado_desde')}")
    print(f"  motor {str(cfg.get('motor_commit'))[:8]} · sucio "
          f"{cfg.get('motor_sucio')}")
    print(f"  respuestas {len(datos['respuestas'])} · presencias "
          f"{len(datos['presencias'])} · word_uses {len(datos['usos'])} · "
          f"neologismos(db) {len(datos['neologismos_db'])} · "
          f"neologismos(cierre con ámbito) {len(neos)} · "
          f"koine_lexicon {len(datos['koine_lexicon'])}")
    con_lugar = sum(1 for r in datos["respuestas"] if r["lugar"])
    discrepan = sum(1 for r in datos["respuestas"]
                    if r["lugar"] and lugar_de.get(
                        (r["day"], r["turn_num"], r["agent_name"])) != r["lugar"])
    print(f"  `agent_responses.lugar` escrito en {con_lugar} de "
          f"{len(datos['respuestas'])} respuestas · discrepan de `presencias`: "
          f"{discrepan} (todo lo de abajo se ubica por `presencias`, que es la "
          f"capa 1 y cubre a los 63, no sólo a los 12 que hablan)")
    compartidos = [l for l, n in nodos_del_lugar.items() if len(n) > 1]
    print(f"  lugares con nodo: {len(nodos_del_lugar)} · compartidos por los dos: "
          f"{', '.join(compartidos) or 'ninguno'}")

    # ── 1. La forma ────────────────────────────────────────────────────
    tit(f"1 · «{forma}» — QUIÉN LA DIJO, DÓNDE Y EN QUÉ ORDEN")
    print(f"  ¿está en lo que las plantillas del prompt ENSEÑAN "
          f"(_FORMAS_EXCLUIDAS, {len(excluidas)} formas)?  "
          f"{'SÍ' if forma in excluidas else 'no'}")
    for linea in ident.splitlines():
        if patron.search(linea.lower()):
            print(f"    _IDENTIDAD_LINGUISTICA, línea literal que la enseña:")
            print(f"      {linea.strip()}")
    orden = defaultdict(int)
    dichos = dichos_por_turno(datos["respuestas"], lugar_de)
    apariciones = []
    for r in datos["respuestas"]:
        clave = (r["day"], r["turn_num"])
        orden[clave] += 1
        if not patron.search((r["response_text"] or "").lower()):
            continue
        lugar = lugar_de.get((r["day"], r["turn_num"], r["agent_name"]))
        apariciones.append({
            "dia": r["day"], "turno": r["turn_num"], "momento": r["moment"],
            "orden_en_el_turno": orden[clave], "agente": r["agent_name"],
            "lugar": lugar, "nodo": nodo_de.get(r["agent_name"]),
            "veces": len(patron.findall((r["response_text"] or "").lower())),
        })
    en_word_uses = {(u["day"], u["turn_num"], u["agent_name"])
                    for u in datos["usos"] if u["word"] == forma}
    print(f"\n  {'d/t':<5} {'orden':<6} {'agente':<13} {'lugar':<26} {'nodo':<9} "
          f"{'veces':<6} en word_uses")
    for a in apariciones:
        marca = "sí" if (a["dia"], a["turno"], a["agente"]) in en_word_uses else "NO"
        print(f"  d{a['dia']}t{a['turno']:<3} {a['orden_en_el_turno']:<6} "
              f"{a['agente']:<13} {str(a['lugar']):<26} {str(a['nodo']):<9} "
              f"{a['veces']:<6} {marca}")
    lugares = sorted({a["lugar"] for a in apariciones if a["lugar"]})
    primer = min((a["dia"], a["turno"]) for a in apariciones) if apariciones else None
    natales = sorted({a["lugar"] for a in apariciones
                      if (a["dia"], a["turno"]) == primer})
    print(f"\n  dicha por {len({a['agente'] for a in apariciones})} agentes en "
          f"{len(lugares)} lugares: {', '.join(lugares)}")
    print(f"  en el PRIMER turno en que suena (d{primer[0]}t{primer[1]}) ya suena en "
          f"{len(natales)} lugar(es): {', '.join(natales)}")
    print(f"  usos que quedaron en `word_uses`: {len(en_word_uses)} de "
          f"{len(apariciones)} apariciones en el texto")
    salida["apariciones"] = apariciones

    # ── 2. Las vías, una por una ───────────────────────────────────────
    tit(f"2 · LAS VÍAS — qué podía haber llevado «{forma}» hasta cada usuario")
    reg = {n["forma"]: n for n in neos}
    ficha = reg.get(forma)
    if ficha:
        print(f"  registrada como neologismo: autor {ficha['autor']} · "
              f"ámbito {ficha['ambito']} · d{ficha['dia']}t{ficha['turno']} · "
              f"estado {ficha['estado']}")
        print(f"  adoptado_por {ficha['adoptado_por']} · adoptado_en "
              f"{ficha['adoptado_en']} · oficial_en {ficha['oficial_en']} · "
              f"vía {ficha['via']} · resuelto en "
              f"d{ficha['dia_resolucion']}t{ficha['turno_resolucion']}")
    filas_via = []
    for a in apariciones:
        clave_ant = (a["dia"], a["turno"] - 1) if a["turno"] > 1 else None
        previos = dichos.get(clave_ant, []) if clave_ant else []
        oidos = bloque_oir(a["agente"], a["lugar"], previos)
        oye_forma = any(patron.search(d["frase"].lower()) for d in oidos)
        v1 = v1_en(neos, a["lugar"], a["dia"], a["turno"])
        v2 = v2_en(neos, a["lugar"], a["dia"], a["turno"])
        pesos_lugar = (campo.get("por_ambito") or {}).get(a["lugar"], {})
        filas_via.append({
            "agente": a["agente"], "dia": a["dia"], "turno": a["turno"],
            "lugar": a["lugar"],
            "v1_tiene_la_forma": forma in v1, "v1": v1,
            "v2_tiene_la_forma": forma in v2, "v2": v2,
            "v4_peso_en_su_lugar": round(pesos_lugar.get(forma, 0.0), 4),
            "oyo_aqui": len(oidos), "oyo_la_forma": oye_forma,
        })
    print(f"\n  {'d/t':<5} {'agente':<13} {'lugar':<26} {'V1':<4} {'V2':<4} "
          f"{'V4 peso':<9} {'oyó aquí':<9} ¿la oyó?")
    for f in filas_via:
        print(f"  d{f['dia']}t{f['turno']:<3} {f['agente']:<13} {f['lugar']:<26} "
              f"{'sí' if f['v1_tiene_la_forma'] else '·':<4} "
              f"{'sí' if f['v2_tiene_la_forma'] else '·':<4} "
              f"{f['v4_peso_en_su_lugar']:<9} {f['oyo_aqui']:<9} "
              f"{'SÍ' if f['oyo_la_forma'] else 'no'}")
    salida["vias"] = filas_via

    # La quinta vía: el contagio, que NO va por ámbito.
    tit("2b · LA QUINTA VÍA — el contagio léxico, que el diseño no contó")
    print("  `DifusionLexica` inyecta «[Has oído estas palabras nuevas en boca de")
    print("  gente que respetas]» y NO recibe ámbito: viaja por")
    print("  `curiana_social.vecinos()` = vínculos resueltos + co-ubicación.")
    formas_base = set(excluidas)
    for a in apariciones[1:]:
        exp = exposicion_de_contagio(datos["respuestas"], neos, datos["usos"],
                                     lugar_de, formas_base,
                                     (a["dia"], a["turno"]), forma)
        e = exp.get(a["agente"], 0.0)
        print(f"  d{a['dia']}t{a['turno']} {a['agente']:<13} exposición acumulada a "
              f"«{forma}» antes de hablar: {e:.3f}  "
              f"(umbral {UMBRAL_CONTAGIO} → "
              f"{'SE LE SUGIERE' if e >= UMBRAL_CONTAGIO else 'no se le sugiere'})")

    # La sexta puerta: procesar_adopciones ve TODAS las pendientes.
    tit("2c · `procesar_adopciones` — el detector NO está partido por ámbito")
    print("  `curiana_observer.procesar_adopciones` recorre")
    print("  `lexico.neologismos_pendientes()` SIN ámbito (curiana_lexicon.py:7418):")
    print("  lo que el lugar filtra es lo que el agente VE (V1), no lo que puede")
    print("  adoptar. Una forma dicha por cualquier motivo —incluida la copia de la")
    print("  plantilla— cuenta como adopción de la propuesta de otro lugar.")
    if ficha:
        for i, quien in enumerate(ficha["adoptado_por"]):
            donde = (ficha["adoptado_en"] or [None] * (i + 1))[i]
            print(f"    adoptante {i+1}: {quien} en {donde}")

    # ── 3. Transparencia del compuesto ─────────────────────────────────
    tit("3 · ¿ES RE-ACUÑABLE? — transparencia del compuesto")
    tr = transparencia(forma, (ficha or {}).get("componentes", ""))
    for d in tr["piezas"]:
        print(f"  {d['pieza']:<12} en VOCABULARIO_BASE: "
              f"{'sí' if d['en_vocabulario_base'] else 'no':<3} · "
              f"la enseña una plantilla del prompt: "
              f"{'sí' if d['en_plantilla'] else 'no'}")
    print(f"  → compuesto transparente para CUALQUIER agente: "
          f"{'SÍ' if tr['transparente'] else 'no'}")
    salida["transparencia"] = tr

    # ── 4. La disputa de las cuentas ───────────────────────────────────
    tit("4 · LA DISPUTA — «las cuentas brillantes» (concepto `cuentas_vidrio`)")
    soporte, propuestas, reusos = reconstruir_competencia(
        datos["respuestas"], neos, datos["usos"], turno_nombramiento)
    print(f"  turno de nombramiento: t{turno_nombramiento} "
          f"(cadencia {CADENCIA_NOMBRAMIENTO})")
    print(f"  fijada en `koine_lexicon`: "
          f"{datos['koine_lexicon'] or 'NO — ninguna variante llegó al umbral'}")
    print(f"\n  {'forma rival':<22} {'soporte':<9} {'propuso':<24} {'reusó':<20} "
          f"{'lugares':<26} nodos")
    for forma_r, sup in soporte.most_common():
        dichos_r = [(r["turn_num"], r["agent_name"],
                     lugar_de.get((r["day"], r["turn_num"], r["agent_name"])))
                    for r in datos["respuestas"]
                    if re.search(r"(?<![\w\-])" + re.escape(forma_r) + r"(?![\w\-])",
                                 (r["response_text"] or "").lower())]
        lugs = sorted({l for _, _, l in dichos_r if l})
        nods = sorted({nodo_de.get(a) for _, a, _ in dichos_r if nodo_de.get(a)})
        pesos = {l: round((campo.get("por_ambito") or {}).get(l, {}).get(forma_r, 0), 4)
                 for l in lugs}
        print(f"  {forma_r:<22} {sup:<9.2f} {', '.join(propuestas[forma_r]):<24} "
              f"{', '.join(reusos[forma_r]) or '·':<20} {', '.join(lugs):<26} "
              f"{', '.join(nods)}")
        print(f"    peso en CampoLexico por lugar: {pesos} · "
              f"global {round((campo.get('global') or {}).get(forma_r, 0), 4)}")
        print(f"    lo dijeron: " + "; ".join(f"t{t} {a}" for t, a, _ in dichos_r))
    total = sum(soporte.values())
    if total:
        lider, sup = soporte.most_common(1)[0]
        print(f"\n  total {total:.2f} · líder {lider} {sup:.2f} = "
              f"{sup/total:.1%} (umbral de fijación 55 %, soporte mínimo 3.0)")
    print("\n  ⚠ `CompetenciaLexica` NO se persiste: `guardar_koine()` escribe")
    print("    idiolectos y campo, nada más, y `auto_mode` crea una")
    print("    `CompetenciaLexica()` nueva aunque se continúe. Con")
    print("    `referentes_introducidos` heredado, el referente tampoco se")
    print("    vuelve a presentar: la disputa no puede resolverse mañana.")
    salida["disputa"] = {f: round(s, 4) for f, s in soporte.items()}

    # ── 5. Las nacidas en varios lugares a la vez ──────────────────────
    tit("5 · LAS QUE NACIERON EN VARIOS LUGARES A LA VEZ")
    filas, emergentes = cruce_por_lugar(
        datos["usos"], datos["neologismos_db"], datos["koine_lexicon"],
        excluidas, lugar_de, turnos_por_dia)
    multi = [f for f in filas if f["multilugar"]]
    murieron = [f for f in filas if f["murio_en_su_lugar"]]
    salieron = [f for f in filas if f["salida"]]
    print(f"  formas emergentes ubicables: {len(filas)} · nacieron en varios "
          f"lugares: {len(multi)} · murieron en el suyo: {len(murieron)} · "
          f"salieron: {len(salieron)}")
    del_nombramiento = [f for f in multi if f["turno"] == turno_nombramiento]
    plantilla = [f for f in multi if f["forma"] in excluidas]
    resto = [f for f in multi
             if f["turno"] != turno_nombramiento and f["forma"] not in excluidas]
    print(f"\n  del evento de nombramiento (nacieron en t{turno_nombramiento}): "
          f"{len(del_nombramiento)}")
    for f in del_nombramiento:
        print(f"    {f['forma']:<24} {', '.join(f['natales'])}")
    print(f"\n  formas que el propio prompt ENSEÑA (están en _FORMAS_EXCLUIDAS y "
          f"vuelven a contar por ser neologismo registrado o koiné): {len(plantilla)}")
    for f in plantilla:
        print(f"    {f['forma']:<24} d{f['dia']}t{f['turno']} "
              f"{', '.join(f['natales'])}")
    print(f"\n  el resto: {len(resto)}")
    print(f"  {'forma':<22} {'d/t':<5} {'n lug':<6} {'transp':<7} lugares natales")
    for f in sorted(resto, key=lambda x: (-x["usos"], x["forma"])):
        comp = reg.get(f["forma"], {}).get("componentes", "")
        t = transparencia(f["forma"], comp)
        print(f"  {f['forma']:<22} d{f['dia']}t{f['turno']:<3} "
              f"{len(f['natales']):<6} {'sí' if t['transparente'] else 'NO':<7} "
              f"{', '.join(f['natales'])}")
    transp = sum(1 for f in resto
                 if transparencia(f["forma"],
                                  reg.get(f["forma"], {}).get("componentes", ""))
                 ["transparente"])
    print(f"\n  de las {len(resto)} del resto, {transp} son compuestos "
          f"transparentes (todas sus piezas se enseñan a los 63) y "
          f"{len(resto) - transp} no lo son")
    por_turno = Counter((f["dia"], f["turno"]) for f in multi)
    print("  nacimiento de las multilugar, por turno: " +
          " · ".join(f"d{d}t{t} {c}" for (d, t), c in sorted(por_turno.items())))

    # Lo mismo por NODO, para poder contrastar con `analizar_nodos.py` (que
    # glosa su cifra como «evento de nombramiento simultáneo»).
    nodo_por_forma = defaultdict(lambda: defaultdict(set))
    primero = {}
    for u in datos["usos"]:
        if u["word"] not in emergentes:
            continue
        n = nodo_de.get(u["agent_name"])
        if not n:
            continue
        clave = (u["day"], u["turn_num"])
        primero[u["word"]] = min(primero.get(u["word"], clave), clave)
        nodo_por_forma[u["word"]][clave].add(n)
    multinodo = {f: primero[f] for f in primero
                 if len(nodo_por_forma[f][primero[f]]) > 1}
    print(f"\n  por NODO: {len(multinodo)} formas nacieron en los DOS nodos a la "
          f"vez · turno de ese nacimiento: " +
          " · ".join(f"d{d}t{t} {c}" for (d, t), c in
                     sorted(Counter(multinodo.values()).items())))
    print(f"  de ellas, nacidas en el turno de nombramiento "
          f"(t{turno_nombramiento}): "
          f"{sum(1 for k in multinodo.values() if k[1] == turno_nombramiento)}")
    salida["multilugar"] = {
        "total": len(multi), "del_nombramiento": len(del_nombramiento),
        "de_plantilla": len(plantilla), "resto": len(resto),
        "resto_transparentes": transp,
    }

    # ── 6. Lo que el instrumento no ve ────────────────────────────────
    tit("6 · LO QUE EL INSTRUMENTO NO VE")
    de_plantilla = [n for n in datos["neologismos_db"] if n["form"] in excluidas]
    print(f"  neologismos registrados cuya forma YA la enseña el prompt "
          f"(está en _FORMAS_EXCLUIDAS): {len(de_plantilla)} de "
          f"{len(datos['neologismos_db'])}")
    for n in de_plantilla:
        print(f"    {n['form']:<24} propuesta por {n['proposed_by']} · "
              f"estado {n['status']} · adoptada por {n['adopted_by']}")
    print("    `formas_emergentes()` (analizar_nodos.py:449-452) las devuelve al")
    print("    conjunto emergente por ser neologismo registrado, aunque el propio")
    print("    motor las había excluido: `registrar_neologismo()` no comprueba")
    print("    _FORMAS_EXCLUIDAS (curiana_lexicon.py:7346).")

    # Apariciones en el texto que no dejan fila en `word_uses`.
    par_uso = {(u["response_id"], u["word"]) for u in datos["usos"]}
    huecos = Counter()
    for r in datos["respuestas"]:
        texto = (r["response_text"] or "").lower()
        for n in datos["neologismos_db"]:
            f = n["form"].lower()
            if not re.search(r"(?<![\w\-])" + re.escape(f) + r"(?![\w\-])", texto):
                continue
            if (r["id"], f) not in par_uso:
                huecos[f] += 1
    print(f"\n  apariciones de un neologismo en el TEXTO que no dejan fila en "
          f"`word_uses`: {sum(huecos.values())} sobre {len(huecos)} formas")
    for f, c in huecos.most_common(12):
        print(f"    {f:<24} {c}")
    print("    Es la trampa de CLAUDE.md «una forma recién acuñada no es una")
    print("    palabra_activa»: mientras está en `propuesto` no entra en")
    print("    `palabras_caquetias`, y todo el cruce por lugar se mide sobre")
    print("    `word_uses`. Un uso invisible es un viaje que no se fecha.")
    salida["huecos_word_uses"] = dict(huecos)

    # ── 7. Lo que verán el día 2 y el día 3 ───────────────────────────
    tit("7 · EL DÍA 2 (VÍSPERA) Y EL DÍA 3 (CAPUBANA) — la predicción, medida")
    from curiana_escena import (EstadoDeEnsayo, escena_de, es_dia_de_capubana,
                                es_vispera_de_capubana)
    cada = int(cfg.get("capubana_cada") or 0)
    momentos = [t["moment"] for t in datos["turnos"]]
    for dia in (2, 3):
        st = EstadoDeEnsayo(dia=dia, estacion="viento", escena=True,
                            capubana_cada=cada)
        print(f"\n  día {dia}: capubana {es_dia_de_capubana(st)} · víspera "
              f"{es_vispera_de_capubana(st)}")
        ambitos_del_dia = defaultdict(set)
        for m in momentos:
            st.momento = m
            for agente, lugar in escena_de(st).items():
                ambitos_del_dia[lugar].add(agente)
        print(f"    lugares ocupados en el día: {len(ambitos_del_dia)}")
        compart = [l for l, gente in ambitos_del_dia.items()
                   if len({nodo_de.get(a) for a in gente} - {None}) > 1]
        for l in sorted(compart):
            gente = sorted(ambitos_del_dia[l])
            print(f"    lugar con los DOS nodos: {l} — {len(gente)} agentes: "
                  f"{', '.join(gente[:8])}{'…' if len(gente) > 8 else ''}")
            # Lo que esa gente lleva encima: su idiolecto NO va por ámbito.
            for a in gente[:8]:
                acu = sorted({n["forma"] for n in neos if n["autor"] == a})
                if acu:
                    print(f"      {a} carga en `[Tu manera de hablar]` "
                          f"«acuñaste: {', '.join(acu[:4])}»")
    # Lo que el ámbito Capubana tendrá para ofrecer el día 3.
    pesos_cerro = (campo.get("por_ambito") or {}).get("Capubana", {})
    v1_cerro = [n["forma"] for n in neos if n.get("ambito") == "Capubana"
                and n["estado"] == "propuesto"]
    v2_cerro = [n["forma"] for n in neos
                if "Capubana" in (n.get("adoptado_en") or ())]
    print(f"\n  el día 3 los 63 comparten ámbito «Capubana». Heredado del día 1:")
    print(f"    V4 · `pesos_de('Capubana')`: {len(pesos_cerro)} formas "
          f"(el campo del cerro es el de sus DOS ocupantes del día 1)")
    print(f"    V1 · propuestas hechas en «Capubana» y aún pendientes: "
          f"{v1_cerro or 'ninguna'}")
    print(f"    V2 · adoptadas en «Capubana»: {v2_cerro or 'ninguna'}")
    rivales = [f for f, _ in soporte.most_common(3)]
    print(f"    las tres rivales en el campo del cerro: "
          f"{ {r: round(pesos_cerro.get(r, 0), 4) for r in rivales} }")
    otros_cerro = sorted(a for a in (campo.get("por_ambito") or {})
                         if a.startswith("Capubana"))
    print(f"    ⚠ el cerro no es un solo ámbito: {otros_cerro} son cadenas "
          f"distintas y no se ven entre sí")
    salida["dia3"] = {"v1_capubana": v1_cerro, "v2_capubana": v2_cerro,
                      "formas_en_el_campo_del_cerro": len(pesos_cerro),
                      "rivales_en_el_cerro": {r: pesos_cerro.get(r, 0)
                                              for r in rivales}}

    if args.json:
        print("\n" + json.dumps(salida, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
