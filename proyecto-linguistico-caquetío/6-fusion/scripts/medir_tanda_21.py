#!/usr/bin/env python3
"""LA TANDA DEL 2026-09-21, medida: UN SOLO CORTE, UNA SOLA MEDICIÓN.

Las catorce decisiones de `6-fusion/decisiones_tanda_2026-09-21.yaml` que son
código se aplicaron JUNTAS, porque un corte de serie cuesta lo mismo por una
que por ocho y la serie C se repite una sola vez. Esto mide el corte entero.

Qué mide, en orden:

  1. EL INSTRUMENTO. Lo que cambió de tamaño: `VOCABULARIO_BASE`,
     `FUERA_DEL_HABLA`, `FORMAS_DE_PLANTILLA`, `_RAICES_VERB` y —lo nuevo de
     d21.2— las raíces verbales CAQUETÍAS, que son las que el detector de
     aspecto y `es_arahuaco` usan desde hoy. Y las CLAVES de
     `TODAS_LAS_REGLAS`, que son las que mueven el desafijador: entran `u-`
     (d21.13) y `-bakoa` (d21.14 A), sale `-naiki` (d21.9) y `-bacoa` se
     migra al lema fonémico de D5.

  2. EL DESAFIJADOR, DECISIÓN POR DECISIÓN. `nucleo_de_token()` se recalcula
     sobre TODAS las formas de la base (`word_uses` + `neologisms`) con cinco
     juegos de afijos: el de antes, el de hoy, y tres contrafactuales que
     aíslan d21.9, d21.13 y d21.14 A. Es la medición que d21.14 pide «antes»
     y la que d21.5 pide como invariante:

       d21.5   REAGRUPAR `ka-`/`ma-` a REGLAS_ATRIBUTIVAS no toca ninguna
               clave → `nucleo_de_token()` tiene que devolver EXACTAMENTE lo
               mismo, token a token. Si no sale 0, el corte está mal hecho.
       d21.9   sacar `-naiki` sí mueve `_SUFIJOS_CAQ` aunque el uso sea cero.
       d21.13  añadir `u-` mueve `_PREFIJOS_CAQ`.
       d21.14  `-bacoa` → `-bakoa`: cuántas formas dejan de segmentarse
               igual, y de ellas cuántas cambian de verdad algo — o sea
               `es_raiz_de_ninguna_parte()` y `_familia_de_token()`, que son
               los dos únicos consumidores del núcleo. «Limpia» quiere decir
               cero en esos dos, no cero en el núcleo.

     CONTROL: el segmentador local de este script tiene que reproducir
     `nucleo_de_token()` del motor forma a forma. Si no, no mide nada.

  3. EL PROMPT. Es corte de serie, así que hay que comprobar que CAMBIA y en
     cuánto. Dos capas: las diez plantillas estáticas, carácter a carácter, y
     el system prompt ENTERO de los 63 del elenco, montado con el `run_turn`
     de verdad y `_invoke` espiado (el patrón de `medir_ejemplo_identidad.py`),
     con la misma semilla en los dos brazos. La longitud predice el score
     (r = −0,48): se mide aunque parezca cosmético.

  4. ¿MUEVE EL SCORE? Los 6 runs de la serie C —los tres del brazo con escena
     (`f2741e89` → `fcdfa07a` → `0313d830`) y los tres del control
     (`0345840d` → `45618069` → `e98227eb`), 216 + 216 respuestas— se
     re-ejecutan enteros por el pipeline del Observer, dos veces: con el
     lexicón de `--ref` y con el del árbol de trabajo. Se comparan respuesta a
     respuesta `score`, `palabras_caquetias`, `neologisms_proposed` y los
     PUNTOS DE ASPECTO.

     CONTROL: el brazo «antes» tiene que reproducir el `score` y el
     `neologisms_proposed` que la base guardó. Si el control está en rojo, lo
     de arriba no mide nada.

  5. LA SATURACIÓN DEL ASPECTO (d21.3), que es la pregunta abierta. La
     auditoría del 09-20 midió media 1,9982 sobre un máximo de 2,0 — el 20 %
     del score sin separar a nadie— y dijo que tapar el comodín la movería a
     1,9296. Miguel aceptó VOLVER A MEDIRLA después de d21.1 y d21.2, «porque
     al exigir verbo de verdad la saturación puede caerse sola». Se re-mide
     sobre TODAS las respuestas de la base, en los dos brazos, con el mismo
     recuento que hace el score (`min(aspectos_distintos, 2)`).

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/medir_tanda_21.py
    python 6-fusion/scripts/medir_tanda_21.py --sin-ensayo   # salta el punto 3
    python 6-fusion/scripts/medir_tanda_21.py --ref <sha>

CÓMO SE MIDE EL «ANTES», sin cifras a mano: se sacan `curiana_lexicon.py`,
`curiana_koine.py` y `curiana_database.py` del commit `REF` con `git show`, se
dejan en un directorio temporal que va PRIMERO en el `sys.path` de un
subproceso, y ese subproceso corre exactamente el mismo código de medición que
el de hoy. Es el patrón de `medir_politica_atestiguado_manda.py` y
`medir_raices_de_ninguna_parte.py`.

REGLAS DURAS que este script respeta: no abre `curiana_sim/.env` (stub de
`dotenv` antes de importar el motor), no llama a la API, no escribe en la base
(la lee por `docker exec … psql`) y no toca el canon.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import os
import subprocess
import sys
import tempfile
import types

# ── El motor, sin abrir .env ──────────────────────────────────────────────
if "dotenv" not in sys.modules:
    _stub = types.ModuleType("dotenv")
    _stub.load_dotenv = lambda *a, **k: None              # noqa: E731
    _stub.dotenv_values = lambda *a, **k: {}              # noqa: E731
    sys.modules["dotenv"] = _stub

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SIM = os.path.join(RAIZ, "curiana_sim")
os.environ.setdefault("CURIANA_ELENCO", "era2")

FECHA = "2026-09-21"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_tanda_21_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"

# El commit ANTES de la tanda: el último merge a main del 2026-09-21, con las
# catorce decisiones ya escritas en 6-fusion/ y ninguna aplicada. Es contra
# éste contra el que se mide el corte.
REF = "b5733f1"

# ⚠️ Y el commit CON EL QUE CORRIERON los runs, que NO es el mismo: entre
# medias entraron dos cortes ya declarados y medidos —#177 (la raíz de
# ninguna parte, punto 11 de la bitácora) y #178 (la clase de la raíz, 49
# raíces de Zavala)— y los dos movieron el score. Así que el CONTROL del
# replay no se puede pedir contra el módulo de hoy: se pide contra éste, que
# es lo que la base guardó. Con tres brazos cada número dice lo suyo:
#   motor_del_run → control contra `agent_responses.score` (tiene que ser 0)
#   motor_del_run → antes  = lo que ya movieron los cortes del 09-20
#   antes → hoy            = LO QUE MUEVE ESTA TANDA, que es el número del corte
REF_RUN = "b8c85ca"

# Los dos brazos de la serie C, en el orden de su cadena.
BRAZOS = {
    "con_escena": ("f2741e89", "fcdfa07a", "0313d830"),
    "control":    ("0345840d", "45618069", "e98227eb"),
}
CADENCIA_NOMBRAMIENTO = 4          # curiana_orchestrator_v2.auto_mode
SEMILLA_ENSAYO = 20260921
SEPARADOR = "\x1f"
FIN_DE_FILA = "\x1e"

# El tope que el score le pone al componente de aspecto: `min(n * 1.0, 2.0)`.
# No se escribe a mano en ningún otro sitio de este script.
TOPE_ASPECTO = 2.0


def _forzar_utf8():
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:                                 # noqa: BLE001
            pass


# ══════════════════════════════════════════════════════════════════════
# LA BASE (sólo lectura, por docker exec)
# ══════════════════════════════════════════════════════════════════════
def psql(sql: str) -> list[list[str]]:
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql],
        capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise RuntimeError(f"psql falló: {out.stderr.strip()[:400]}")
    return [ln.split("|") for ln in out.stdout.splitlines() if ln.strip()]


def formas_de_la_base() -> dict[str, int]:
    """Toda forma distinta que la base conoce, con sus usos.

    `word_uses` (lo que el scorer reconoció) MÁS `neologisms.form` (lo que un
    agente propuso y el scorer puede no haber visto nunca): el desafijador
    pasa por las dos poblaciones.
    """
    cuenta: dict[str, int] = collections.Counter()
    for f in psql("select word, count(*) from word_uses group by 1;"):
        if f[0]:
            cuenta[f[0]] += int(f[1])
    for f in psql("select form, count(*) from neologisms group by 1;"):
        if f[0]:
            cuenta[f[0]] += int(f[1])
    return dict(cuenta)


def respuestas_de(id8: list[str]) -> list[dict]:
    """Las respuestas de unos runs, en el orden en que se dijeron."""
    sql = (
        "select t.day || '{S}' || t.turn_num || '{S}' || r.agent_name || '{S}' || "
        "coalesce(r.ethnicity,'') || '{S}' || coalesce(r.tier,2) || '{S}' || "
        "t.moment || '{S}' || t.season || '{S}' || r.score || '{S}' || "
        "r.neologisms_proposed || '{S}' || coalesce(r.lugar,'') || '{S}' || "
        "substring(r.run_id::text,1,8) || '{S}' || r.response_text || '{F}' "
        "from agent_responses r join turns t on t.id = r.turn_id "
        "where substring(r.run_id::text,1,8) in ({IDS}) "
        "order by r.run_id, t.day, t.turn_num, r.created_at"
    ).format(S=SEPARADOR, F=FIN_DE_FILA,
             IDS=", ".join(f"'{i}'" for i in id8))
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql], capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace")[:400])
    filas = []
    for bloque in out.stdout.decode("utf-8").split(FIN_DE_FILA):
        if not bloque.strip("\n"):
            continue
        p = bloque.lstrip("\n").split(SEPARADOR)
        if len(p) < 12:
            continue
        filas.append({"dia": int(p[0]), "turno": int(p[1]), "agente": p[2],
                      "etnia": p[3] or "caquetío", "tier": int(p[4]),
                      "momento": p[5], "estacion": p[6],
                      "score_guardado": float(p[7]),
                      "neos_guardados": int(p[8]), "lugar": p[9] or None,
                      "run": p[10], "texto": p[11]})
    return filas


def todas_las_respuestas() -> list[dict]:
    """Toda la base, para la saturación del aspecto (d21.3).

    La auditoría del 09-20 midió la media sobre TODAS las respuestas; para que
    el número nuevo sea comparable con el 1,9982, se mide sobre la misma
    población.
    """
    sql = (
        "select coalesce(s.config->>'elenco','era1') || '{S}' || "
        "coalesce(s.config->>'serie','-') || '{S}' || r.response_text || '{F}' "
        "from agent_responses r join simulation_runs s on s.id = r.run_id"
    ).format(S=SEPARADOR, F=FIN_DE_FILA)
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql], capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace")[:400])
    filas = []
    for bloque in out.stdout.decode("utf-8").split(FIN_DE_FILA):
        if not bloque.strip("\n"):
            continue
        p = bloque.lstrip("\n").split(SEPARADOR)
        if len(p) < 3:
            continue
        filas.append({"era": p[0], "serie": p[1], "texto": p[2]})
    return filas


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO: lo que se mide DENTRO de un lexicón (hoy o el de REF)
# ══════════════════════════════════════════════════════════════════════
def _replay(L, filas: list[dict]) -> dict:
    """Re-ejecuta el pipeline del Observer sobre las respuestas, en su orden y
    encadenando los días como lo hizo `--continuar`. Lo que cambia entre
    brazos no es una bandera: es el LEXICÓN. Patrón de
    `medir_raices_de_ninguna_parte.py::_replay`."""
    from curiana_koine import (CampoLexico, CompetenciaLexica, IdiolectoAgente,
                               REFERENTES_NOVEDOSOS, emocionar_de)
    from curiana_observer import ObserverAgent

    lexico = L.LexicoComunitario(filtrar_plantilla=True)
    observer = ObserverAgent(None, lexico)
    competencia = CompetenciaLexica(filtrar_plantilla=True)
    campo = CampoLexico()
    pendientes = [dict(r) for r in REFERENTES_NOVEDOSOS]
    try:
        from curiana_agents import ALL_AGENTS
        idiolectos = {nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia")))
                      for nm, a in ALL_AGENTS.items()}
    except Exception:                                     # noqa: BLE001
        idiolectos = {}

    turnos, visto = [], None
    for f in filas:
        if (f["run"], f["dia"], f["turno"]) != visto:
            turnos.append([])
            visto = (f["run"], f["dia"], f["turno"])
        turnos[-1].append(f)

    salida, fijadas, run_previo, t = [], [], None, 0
    for turno in turnos:
        if turno[0]["run"] != run_previo:
            if run_previo is not None:
                for cid, forma in competencia.evaluar_fijacion(
                        turno[0]["dia"] - 1):
                    fijadas.append({"run": run_previo, "concepto": cid,
                                    "forma": forma})
            run_previo, t = turno[0]["run"], 0
        naming = None
        if pendientes and t > 0 and t % CADENCIA_NOMBRAMIENTO == 0:
            naming = pendientes.pop(0)
            competencia.activar(naming["id"], naming["desc"])
        for fila in turno:
            lexico.situar(fila["agente"], fila["lugar"])
            reg = observer.analizar(
                agente=fila["agente"], etnia=fila["etnia"], tier=fila["tier"],
                texto=fila["texto"], dia=fila["dia"], turno=fila["turno"],
                momento=fila["momento"], estacion=fila["estacion"])
            observer.procesar_adopciones(fila["texto"], fila["agente"],
                                         fila["turno"], dia=fila["dia"])
            neos = reg.neologismos_extraidos
            for neo in neos:
                if naming:
                    competencia.proponer(naming["id"], neo.forma,
                                         fila["agente"], ambito=fila["lugar"])
                else:
                    competencia.registrar_uso(neo.forma, fila["agente"])
            for forma in reg.palabras_caquetias:
                competencia.registrar_uso(forma, fila["agente"])
            campo.registrar(reg.palabras_caquetias, ambito=fila["lugar"])
            campo.registrar([n.forma for n in neos], ambito=fila["lugar"])
            if fila["agente"] in idiolectos:
                idiolectos[fila["agente"]].registrar(reg.palabras_caquetias, neos)
            salida.append({
                "run": fila["run"], "agente": fila["agente"],
                "dia": fila["dia"], "turno": fila["turno"],
                "score": reg.score,
                "palabras_caquetias": len(reg.palabras_caquetias),
                "neologisms_proposed": len(neos),
                # EL ASPECTO, que es la pregunta de d21.3: no el número de
                # detecciones sino los PUNTOS, que es lo que el score suma.
                "aspectos": list(reg.aspectos_usados),
                "puntos_aspecto": min(len(reg.aspectos_usados) * 1.0,
                                      TOPE_ASPECTO),
                "caquetias": sorted(reg.palabras_caquetias),
            })
        t += 1
    if turnos:
        for cid, forma in competencia.evaluar_fijacion(turnos[-1][0]["dia"]):
            fijadas.append({"run": run_previo, "concepto": cid, "forma": forma})

    variantes = {cid: sorted(ref["variantes"].items(), key=lambda x: -x[1])
                 for cid, ref in competencia.referentes.items()
                 if ref["variantes"]}
    return {
        "respuestas": salida,
        "fijadas": fijadas,
        "competencias": {cid: [[f, round(p, 2)] for f, p in v[:8]]
                         for cid, v in variantes.items()},
        "adoptadas": sorted({n.forma for n in lexico.neologismos_adoptados()}),
        "rechazos_de_plantilla": [list(r) for r in lexico.rechazos_de_plantilla],
        "rechazos_de_raiz": [list(r) for r in
                             getattr(lexico, "rechazos_de_raiz", [])],
    }


def _plantillas(L) -> dict:
    """Las diez plantillas estáticas, cada una con su texto.

    Se LLAMAN, nunca se copian: si mañana una cambia, el diff sale solo. Es la
    misma lista con la que `FORMAS_DE_PLANTILLA` construye la puerta.
    """
    p = {
        "IDENTIDAD_LINGUISTICA": L.IDENTIDAD_LINGUISTICA,
        "prompt_reglas_completo": L.prompt_reglas_completo(),
        "prompt_reglas_breve": L.prompt_reglas_breve(),
        "prompt_afijos_atestiguados": L.prompt_afijos_atestiguados(),
        "prompt_afijos_atestiguados_breve": L.prompt_afijos_atestiguados_breve(),
    }
    for s in (1.0, 3.0, 5.0, 6.5):
        p[f"prompt_refuerzo[{s}]"] = L.prompt_refuerzo(s, [])
    for i, (esp, otro) in enumerate(((0, [""]), (3, [""]), (3, []))):
        p[f"prompt_rescate[{i}]"] = L.prompt_rescate_linguistico("", 0.0, esp, otro)
    return p


def _ensayo_de_prompt(L) -> dict:
    """El system prompt ENTERO de los 63, montado con el `run_turn` de verdad.

    `_invoke` espiado, Director mudo, misma semilla del RNG global en los dos
    brazos (de ahí sale la muestra del lexicón). No llama a la API. Patrón de
    `medir_ejemplo_identidad.py::ensayo_de_prompt`.
    """
    import random

    import curiana_agents_era2 as _era2                   # noqa: F401
    import curiana_orchestrator_v2 as orch
    from curiana_observer import ObserverAgent
    from curiana_perfiles import cargar_perfil
    from curiana_state import estado_inicial

    respuesta = "Taya wana-ka arima wara kari. Ta-barsure naba-ni."
    elenco = dict(_era2.ALL_AGENTS)
    perfil = cargar_perfil("era2")
    roster = list(elenco)

    random.seed(SEMILLA_ENSAYO)
    capturas: list[str] = []
    _invoke, _agentes = orch._invoke, orch.ALL_AGENTS
    _narrar, _evento = orch.director_narrate, orch.director_select_event
    orch._invoke = lambda c, system, user: (capturas.append(system) or respuesta)
    orch.director_narrate = lambda *a, **k: "(narración)"
    orch.director_select_event = lambda s: None
    orch.ALL_AGENTS = elenco
    try:
        state = estado_inicial("PARAGUANÁ")
        state.turnos_por_dia = 6
        state.escena = False
        state.capubana_cada = 0
        state.evento_del_turno = None
        lexico = L.LexicoComunitario()
        observer = ObserverAgent(None, lexico)
        orch.run_turn(None, state, orch.AgentMemory(), lexico, observer,
                      verbose=False, agentes_por_turno=len(roster),
                      roster=list(roster), capas=perfil.capas)
    finally:
        orch._invoke, orch.ALL_AGENTS = _invoke, _agentes
        orch.director_narrate, orch.director_select_event = _narrar, _evento

    largos = sorted(len(c) for c in capturas)
    return {
        "prompts": len(capturas),
        "medio": round(sum(largos) / (len(largos) or 1), 1),
        "mediana": largos[len(largos) // 2] if largos else 0,
        "min": largos[0] if largos else 0,
        "max": largos[-1] if largos else 0,
        "largos": largos,
    }


def medir_en_proceso(args) -> dict:
    """Todo lo que depende del LEXICÓN cargado en este proceso."""
    import curiana_lexicon as L

    plantillas = _plantillas(L)
    d = {
        "modulo": os.path.abspath(L.__file__),
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "fuera_del_habla": len(L.FUERA_DEL_HABLA),
        "formas_de_plantilla": len(L.FORMAS_DE_PLANTILLA),
        "formas_de_plantilla_lista": sorted(L.FORMAS_DE_PLANTILLA),
        "raices_verb": len(L._RAICES_VERB),
        "raices_verb_caquetias": (
            len(L.raices_verbales_caquetias())
            if hasattr(L, "raices_verbales_caquetias") else None),
        "cats_verbales": sorted(getattr(L, "CATS_VERBALES", {"v_raiz"})),
        "claves_de_todas_las_reglas": sorted(L.TODAS_LAS_REGLAS),
        "prefijos": sorted(L._PREFIJOS_CAQ),
        "sufijos": sorted(L._SUFIJOS_CAQ),
        "reglas_retiradas": sorted(L.REGLAS_RETIRADAS),
        "tiene_reglas_atributivas": hasattr(L, "REGLAS_ATRIBUTIVAS"),
        "plantillas": {k: {"caracteres": len(v), "texto": v}
                       for k, v in plantillas.items()},
        "raices_conocidas": None,
    }
    if args.formas:
        formas = json.load(io.open(args.formas, encoding="utf-8"))
        d["nucleos"] = {f: L.nucleo_de_token(f) for f in formas}
        d["ninguna_parte"] = {f: L.es_raiz_de_ninguna_parte(f) for f in formas}
        d["familia"] = {f: L._familia_de_token(f) for f in formas}
        d["raices_conocidas"] = sorted(L._raices_conocidas())
    if args.aspecto:
        textos = json.load(io.open(args.aspecto, encoding="utf-8"))
        puntos = []
        for t in textos:
            limpio = L._normalizar(t)
            tokens = L._filtrar_nombres(limpio, L._tokenizar(limpio))
            asp = L._aspectos_morfologicos(tokens)
            puntos.append(min(len(asp) * 1.0, TOPE_ASPECTO))
        d["puntos_aspecto"] = puntos
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = _replay(L, filas)
    if args.ensayo:
        d["ensayo_prompt"] = _ensayo_de_prompt(L)
    return d


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO DE ANTES: el módulo del commit REF, en un subproceso
# ══════════════════════════════════════════════════════════════════════
def modulos_de_ref(ref: str) -> str:
    tmp = tempfile.mkdtemp(prefix="curiana_ref21_")
    for nombre in ("curiana_lexicon.py", "curiana_koine.py",
                   "curiana_database.py", "lexicon_zavala.py"):
        out = subprocess.run(
            ["git", "-C", RAIZ, "show", f"{ref}:./curiana_sim/{nombre}"],
            capture_output=True, encoding="utf-8")
        if out.returncode != 0:
            raise RuntimeError(
                f"git show {ref}:./curiana_sim/{nombre} falló: "
                + out.stderr.strip()[:300])
        with io.open(os.path.join(tmp, nombre), "w",
                     encoding="utf-8", newline="\n") as f:
            f.write(out.stdout)
    return tmp


def correr_brazo(lexicon_dir: str | None, extra: list[str]) -> dict:
    """Este mismo script, en un subproceso, con el lexicón que se le diga."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["CURIANA_ELENCO"] = "era2"
    rutas = ([lexicon_dir] if lexicon_dir else []) + [SIM]
    env["PYTHONPATH"] = os.pathsep.join(rutas)
    out = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--json"] + extra,
        capture_output=True, encoding="utf-8", env=env, cwd=SIM)
    if out.returncode != 0:
        raise RuntimeError("el brazo falló:\n" + (out.stderr or "")[-3000:])
    return json.loads(out.stdout)


# ══════════════════════════════════════════════════════════════════════
# EL SEGMENTADOR LOCAL — para los contrafactuales de una clave
# ══════════════════════════════════════════════════════════════════════
def nucleo_con(prefijos: frozenset, sufijos: frozenset, tok: str) -> list[str]:
    """`nucleo_de_token()` con los juegos de afijos que se le pasen.

    Es copia literal del motor; el control de abajo lo comprueba forma a
    forma contra `nucleo_de_token()` de verdad.
    """
    partes = (tok or "").strip().lower().split("-")
    while len(partes) > 1 and partes[0] + "-" in prefijos:
        partes = partes[1:]
    while len(partes) > 1 and "-" + partes[-1] in sufijos:
        partes = partes[:-1]
    return partes


def diff_de_nucleos(formas: dict, pre_a, suf_a, pre_b, suf_b) -> dict:
    """Qué formas se segmentan distinto entre dos juegos de afijos."""
    cambian = []
    usos = 0
    for f, n in formas.items():
        a = nucleo_con(pre_a, suf_a, f)
        b = nucleo_con(pre_b, suf_b, f)
        if a != b:
            cambian.append({"forma": f, "usos": n,
                            "antes": "+".join(a), "hoy": "+".join(b)})
            usos += n
    cambian.sort(key=lambda x: -x["usos"])
    return {"formas": len(cambian), "usos": usos, "detalle": cambian[:40]}


# ══════════════════════════════════════════════════════════════════════
# LOS CRUCES
# ══════════════════════════════════════════════════════════════════════
def control_del_replay(filas, base) -> dict:
    """¿El brazo del motor del run reproduce lo que la base guardó?

    Es EL control: si el replay no reproduce `score` y `neologisms_proposed`
    con el módulo del commit con el que el run corrió, ningún delta de abajo
    mide nada.
    """
    b = base["replay"]["respuestas"]
    if len(b) != len(filas):
        raise RuntimeError(f"replay desalineado: {len(filas)}/{len(b)}")
    desvios = [{"run": f["run"], "dia": f["dia"], "turno": f["turno"],
                "agente": f["agente"], "guardado": f["score_guardado"],
                "replay": r["score"], "neos_guardados": f["neos_guardados"],
                "neos_replay": r["neologisms_proposed"]}
               for f, r in zip(filas, b)
               if abs(f["score_guardado"] - r["score"]) > 1e-9
               or f["neos_guardados"] != r["neologisms_proposed"]]
    return {"n": len(b), "desvios": len(desvios), "verde": not desvios,
            "detalle": desvios[:10]}


def diff_de_scores(filas, antes, hoy) -> dict:
    """Respuesta a respuesta: el delta entre dos brazos."""
    a = antes["replay"]["respuestas"]
    h = hoy["replay"]["respuestas"]
    if len(a) != len(h) or len(a) != len(filas):
        raise RuntimeError(f"replays desalineados: {len(filas)}/{len(a)}/{len(h)}")
    cambian, deltas, por_run = [], [], collections.defaultdict(list)
    for f, ra, rh in zip(filas, a, h):
        d = round(rh["score"] - ra["score"], 4)
        por_run[f["run"]].append((ra["score"], rh["score"]))
        if abs(d) > 1e-9:
            deltas.append(d)
            perdidas = sorted(set(ra["caquetias"]) - set(rh["caquetias"]))
            ganadas = sorted(set(rh["caquetias"]) - set(ra["caquetias"]))
            cambian.append({"run": f["run"], "dia": f["dia"],
                            "turno": f["turno"], "agente": f["agente"],
                            "antes": ra["score"], "hoy": rh["score"],
                            "delta": d,
                            "aspecto_antes": ra["puntos_aspecto"],
                            "aspecto_hoy": rh["puntos_aspecto"],
                            "formas_que_dejan_de_contar": perdidas[:8],
                            "formas_que_empiezan_a_contar": ganadas[:8]})
    n = len(a) or 1
    asp_a = sum(r["puntos_aspecto"] for r in a) / n
    asp_h = sum(r["puntos_aspecto"] for r in h) / n
    return {
        "n": len(a),
        "cambian": len(cambian),
        "a_la_baja": sum(1 for d in deltas if d < 0),
        "al_alza": sum(1 for d in deltas if d > 0),
        "delta_max_abs": round(max((abs(d) for d in deltas), default=0.0), 4),
        "delta_medio_de_las_que_cambian":
            round(sum(deltas) / len(deltas), 4) if deltas else 0.0,
        "score_medio_antes": round(sum(r["score"] for r in a) / n, 4),
        "score_medio_hoy": round(sum(r["score"] for r in h) / n, 4),
        "caquetias_cambian": sum(
            1 for ra, rh in zip(a, h)
            if ra["palabras_caquetias"] != rh["palabras_caquetias"]),
        "neos_cambian": sum(
            1 for ra, rh in zip(a, h)
            if ra["neologisms_proposed"] != rh["neologisms_proposed"]),
        "aspecto_medio_antes": round(asp_a, 4),
        "aspecto_medio_hoy": round(asp_h, 4),
        "aspecto_tope": TOPE_ASPECTO,
        "respuestas_con_aspecto_al_tope_antes":
            sum(1 for r in a if r["puntos_aspecto"] >= TOPE_ASPECTO),
        "respuestas_con_aspecto_al_tope_hoy":
            sum(1 for r in h if r["puntos_aspecto"] >= TOPE_ASPECTO),
        "respuestas_sin_aspecto_antes":
            sum(1 for r in a if not r["puntos_aspecto"]),
        "respuestas_sin_aspecto_hoy":
            sum(1 for r in h if not r["puntos_aspecto"]),
        "por_run": {r: {"antes": round(sum(x for x, _ in v) / len(v), 4),
                        "hoy": round(sum(y for _, y in v) / len(v), 4)}
                    for r, v in por_run.items()},
        "detalle": cambian[:50],
    }


# ══════════════════════════════════════════════════════════════════════
# YAML (a mano, como el resto de 6-fusion/)
# ══════════════════════════════════════════════════════════════════════
def _y(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if any(c in s for c in ":#{}[]&*!|>'\"%@`,") or s != s.strip() or not s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def volcar(obj, nivel=0, salida=None) -> list[str]:
    salida = salida if salida is not None else []
    ind = "  " * nivel
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)) and v:
                salida.append(f"{ind}{_y(k)}:")
                volcar(v, nivel + 1, salida)
            elif isinstance(v, (dict, list)):
                salida.append(f"{ind}{_y(k)}: {{}}" if isinstance(v, dict)
                              else f"{ind}{_y(k)}: []")
            else:
                salida.append(f"{ind}{_y(k)}: {_y(v)}")
    elif isinstance(obj, list):
        for v in obj:
            if isinstance(v, (dict, list)) and v:
                salida.append(f"{ind}-")
                volcar(v, nivel + 1, salida)
            else:
                salida.append(f"{ind}- {_y(v)}")
    return salida


# ══════════════════════════════════════════════════════════════════════
def main(argv=None):
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true",
                    help="modo brazo: imprime JSON y sale (uso interno)")
    ap.add_argument("--formas", help="JSON con formas a segmentar (uso interno)")
    ap.add_argument("--aspecto", help="JSON con textos a medir (uso interno)")
    ap.add_argument("--respuestas", help="JSON con respuestas a re-puntuar")
    ap.add_argument("--ensayo", action="store_true",
                    help="monta los 63 system prompts (uso interno)")
    ap.add_argument("--ref", default=REF, help="commit del lexicón de ANTES")
    ap.add_argument("--sin-ensayo", action="store_true",
                    help="salta el ensayo de prompts de los 63")
    ap.add_argument("--sin-saturacion", action="store_true",
                    help="salta la re-medición del aspecto sobre toda la base")
    args = ap.parse_args(argv)

    if args.json:
        sys.stdout.write(json.dumps(medir_en_proceso(args), ensure_ascii=False))
        return 0

    sys.path.insert(0, SIM)
    tmpref = modulos_de_ref(args.ref)
    tmpdir = tempfile.mkdtemp(prefix="curiana_tanda21_")

    doc: dict = {
        "medicion": "tanda-21-un-corte-una-medicion",
        "fecha": FECHA,
        "ref_de_antes": args.ref,
        "decide": "6-fusion/decisiones_tanda_2026-09-21.yaml",
        "responde_a": ("6-fusion/issues-pendientes/"
                       "morfologia-revision-2026-09-20.md §6"),
        "que_se_aplico": [
            "d21.1 C — el aspecto sólo cuenta sobre el ÚLTIMO segmento verbal",
            "d21.2 A — _RAICES_VERB filtrada a familia caquetía en las dos puertas",
            "d21.4 B — cat v_estativo en las 10 estativas + una línea en el prompt",
            "d21.5 C — ka-/ma- a REGLAS_ATRIBUTIVAS; ka-biro = hay sal",
            "d21.6 B — -ana se enseña sin glosa",
            "d21.8 A — -kana baja a reconstruido; ejemplos con voz caquetía",
            "d21.9 A — -naiki a REGLAS_RETIRADAS",
            "d21.10 A — kudanga y kuté al prompt como registro formal",
            "d21.11 A — el posesivo sobre verbo sale de las violaciones de slot",
            "d21.13 B — se importa el no-poseído u-",
            "d21.14 B+A — deuda documental y -bacoa → -bakoa",
            "d21.15 — coro 'espina' con González Batista",
            "d21.16 — las cinco glosas",
        ],
    }

    # ── 1. El instrumento, y las formas de la base ───────────────────
    print("· leyendo las formas de la base…", file=sys.stderr)
    formas = formas_de_la_base()
    f_formas = os.path.join(tmpdir, "formas.json")
    with io.open(f_formas, "w", encoding="utf-8") as fh:
        json.dump(sorted(formas), fh, ensure_ascii=False)

    print("· cargando los dos lexicones…", file=sys.stderr)
    antes = correr_brazo(tmpref, ["--formas", f_formas])
    hoy = correr_brazo(None, ["--formas", f_formas])

    ca, ch = set(antes["claves_de_todas_las_reglas"]), set(hoy["claves_de_todas_las_reglas"])
    doc["instrumento"] = {
        "formas_distintas_en_la_base": len(formas),
        "usos_sumados": sum(formas.values()),
        "vocabulario_base": {"antes": antes["vocabulario_base"],
                             "hoy": hoy["vocabulario_base"]},
        "fuera_del_habla": {"antes": antes["fuera_del_habla"],
                            "hoy": hoy["fuera_del_habla"]},
        "formas_de_plantilla": {"antes": antes["formas_de_plantilla"],
                                "hoy": hoy["formas_de_plantilla"]},
        "puerta_entran": sorted(set(hoy["formas_de_plantilla_lista"])
                                - set(antes["formas_de_plantilla_lista"])),
        "puerta_salen": sorted(set(antes["formas_de_plantilla_lista"])
                               - set(hoy["formas_de_plantilla_lista"])),
        "cats_verbales": {"antes": antes["cats_verbales"],
                          "hoy": hoy["cats_verbales"]},
        "raices_verb": {"antes": antes["raices_verb"], "hoy": hoy["raices_verb"]},
        "raices_verb_caquetias_hoy": hoy["raices_verb_caquetias"],
        "raices_verb_que_el_detector_deja_de_mirar":
            (hoy["raices_verb"] - (hoy["raices_verb_caquetias"] or 0)),
        "reglas_retiradas": {"antes": antes["reglas_retiradas"],
                             "hoy": hoy["reglas_retiradas"]},
        "tiene_reglas_atributivas": {"antes": antes["tiene_reglas_atributivas"],
                                     "hoy": hoy["tiene_reglas_atributivas"]},
        "claves_de_todas_las_reglas": {
            "antes": antes["claves_de_todas_las_reglas"],
            "hoy": hoy["claves_de_todas_las_reglas"],
            "entran": sorted(ch - ca), "salen": sorted(ca - ch)},
    }

    # ── 2. El desafijador, decisión por decisión ─────────────────────
    pre_a = frozenset(antes["prefijos"])
    suf_a = frozenset(antes["sufijos"])
    pre_h = frozenset(hoy["prefijos"])
    suf_h = frozenset(hoy["sufijos"])

    # CONTROL: el segmentador de este script contra el del motor.
    desvios_a = [f for f in formas
                 if nucleo_con(pre_a, suf_a, f) != antes["nucleos"][f]]
    desvios_h = [f for f in formas
                 if nucleo_con(pre_h, suf_h, f) != hoy["nucleos"][f]]

    conocidas_hoy = frozenset(hoy["raices_conocidas"] or ())

    def de_ninguna_parte_con(pre, suf, tok) -> bool:
        t = (tok or "").strip().lower()
        if not t:
            return False
        if t in conocidas_hoy:
            return False
        return not any(s in conocidas_hoy for s in nucleo_con(pre, suf, t))

    # d21.5: la reagrupación no toca ninguna clave → el núcleo es el mismo.
    # Se comprueba con los afijos de ANTES contra los de ANTES sin `-naiki`,
    # sin `u-` y con `-bacoa`, que es exactamente lo que queda si se quitan
    # d21.9, d21.13 y d21.14 A del corte de hoy.
    pre_solo_5 = frozenset(pre_h - {"u-"})
    suf_solo_5 = frozenset((suf_h - {"-bakoa"}) | {"-bacoa", "-naiki"})
    doc["desafijador"] = {
        "control_segmentador_local": {
            "desvios_antes": len(desvios_a), "desvios_hoy": len(desvios_h),
            "verde": not desvios_a and not desvios_h,
            "nota": ("el segmentador de este script tiene que reproducir "
                     "`nucleo_de_token()` del motor forma a forma, en los dos "
                     "brazos. Si no, los contrafactuales de abajo no miden "
                     "nada")},
        "d21_5_reagrupacion_no_mueve_el_nucleo": {
            "claves_iguales": sorted(pre_solo_5 | suf_solo_5) == sorted(pre_a | suf_a),
            "diff": diff_de_nucleos(formas, pre_a, suf_a, pre_solo_5, suf_solo_5),
            "nota": ("d21.5 saca `ka-` y `ma-` de REGLAS_POSESIVAS a "
                     "REGLAS_ATRIBUTIVAS: cambia la AGRUPACIÓN, no las claves. "
                     "Tiene que salir 0 formas y 0 usos")},
        "d21_9_naiki": {
            "diff": diff_de_nucleos(formas, pre_a, suf_a,
                                    pre_a, frozenset(suf_a - {"-naiki"})),
            "formas_de_la_base_con_naiki":
                sorted(f for f in formas if "naiki" in f),
            "nota": ("sacar `-naiki` de TODAS_LAS_REGLAS mueve `_SUFIJOS_CAQ`, "
                     "así que se mide aunque el uso sea cero: d21.9 lo pide "
                     "explícitamente")},
        "d21_13_no_poseido": {
            "diff": diff_de_nucleos(formas, pre_a, suf_a,
                                    frozenset(pre_a | {"u-"}), suf_a),
            "formas_de_la_base_con_u_inicial":
                sorted(f for f in formas if f.lower().startswith("u-")),
            "nota": "añadir `u-` mueve `_PREFIJOS_CAQ`"},
    }

    # d21.14 A: la que hay que medir ANTES de aplicarla.
    suf_bacoa = frozenset((suf_a - {"-naiki"}))            # el de antes, limpio
    suf_bakoa = frozenset((suf_bacoa - {"-bacoa"}) | {"-bakoa"})
    diff14 = diff_de_nucleos(formas, pre_a, suf_bacoa, pre_a, suf_bakoa)
    cambian14 = [f for f in formas
                 if nucleo_con(pre_a, suf_bacoa, f)
                 != nucleo_con(pre_a, suf_bakoa, f)]
    ninguna_cambia = [f for f in cambian14
                      if de_ninguna_parte_con(pre_a, suf_bacoa, f)
                      != de_ninguna_parte_con(pre_a, suf_bakoa, f)]
    familia_cambia = [f for f in cambian14
                      if antes["familia"].get(f) != hoy["familia"].get(f)]
    doc["desafijador"]["d21_14_bakoa"] = {
        "diff": diff14,
        "formas_que_dejan_de_segmentarse_igual": len(cambian14),
        "de_ellas_cambian_es_raiz_de_ninguna_parte": len(ninguna_cambia),
        "lista_ninguna_parte": sorted(ninguna_cambia)[:20],
        "de_ellas_cambian_de_familia_en_el_corte_entero": len(familia_cambia),
        "lista_familia": sorted(familia_cambia)[:20],
        "limpia": not ninguna_cambia and not familia_cambia,
        "nota": ("«limpia» = las formas dejan de desafijarse por el borde pero "
                 "NINGUNA cambia lo que el núcleo decide: ni "
                 "`es_raiz_de_ninguna_parte()` —su raíz sigue siendo un "
                 "segmento del núcleo— ni `_familia_de_token()`, que resuelve "
                 "por el primer segmento igual. Si `limpia` es false, d21.14 A "
                 "no debería haberse aplicado en este corte"),
    }

    # ── 3. El prompt ─────────────────────────────────────────────────
    pa, ph = antes["plantillas"], hoy["plantillas"]
    cambios = {k: {"antes": pa[k]["caracteres"], "hoy": ph[k]["caracteres"],
                   "delta": ph[k]["caracteres"] - pa[k]["caracteres"],
                   "texto_cambia": pa[k]["texto"] != ph[k]["texto"]}
               for k in sorted(set(pa) & set(ph))}
    doc["el_prompt"] = {
        "plantillas": cambios,
        "plantillas_que_cambian": sorted(k for k, v in cambios.items()
                                         if v["texto_cambia"]),
        "plantillas_iguales": sorted(k for k, v in cambios.items()
                                     if not v["texto_cambia"]),
        "el_prompt_cambia": any(v["texto_cambia"] for v in cambios.values()),
        "caracteres_estaticos": {
            "antes": sum(v["antes"] for v in cambios.values()),
            "hoy": sum(v["hoy"] for v in cambios.values())},
    }
    if not args.sin_ensayo:
        print("· montando los 63 system prompts en los dos brazos…",
              file=sys.stderr)
        ea = correr_brazo(tmpref, ["--ensayo"])["ensayo_prompt"]
        eh = correr_brazo(None, ["--ensayo"])["ensayo_prompt"]
        doc["el_prompt"]["ensayo_de_los_63"] = {
            "semilla": SEMILLA_ENSAYO,
            "antes": {k: v for k, v in ea.items() if k != "largos"},
            "hoy": {k: v for k, v in eh.items() if k != "largos"},
            "delta_medio": round(eh["medio"] - ea["medio"], 2),
            "nota": ("`run_turn` de verdad con `_invoke` espiado, Director "
                     "mudo, misma semilla del RNG global (de ahí sale la "
                     "muestra del lexicón) y sin escena. No llama a la API. "
                     "La longitud predice el score, r = −0,48"),
        }

    # ── 4. ¿Mueve el score? Los dos brazos de la serie C ─────────────
    ids = [i for b in BRAZOS.values() for i in b]
    filas = respuestas_de(ids)
    orden = {i: k for k, i in enumerate(ids)}
    filas.sort(key=lambda f: (orden[f["run"]], f["dia"], f["turno"]))
    print(f"· re-puntuando {len(filas)} respuestas de la serie C…",
          file=sys.stderr)

    tmprun = modulos_de_ref(REF_RUN)
    resultado_brazos = {}
    for nombre_brazo, id8 in BRAZOS.items():
        sub = [f for f in filas if f["run"] in id8]
        f_resp = os.path.join(tmpdir, f"resp_{nombre_brazo}.json")
        with io.open(f_resp, "w", encoding="utf-8") as fh:
            json.dump(sub, fh, ensure_ascii=False)
        extra = ["--respuestas", f_resp]
        base = correr_brazo(tmprun, extra)
        a = correr_brazo(tmpref, extra)
        h = correr_brazo(None, extra)
        d = diff_de_scores(sub, a, h)
        d["control_del_replay"] = control_del_replay(sub, base)
        d["control_del_replay"]["commit_del_run"] = REF_RUN
        d["control_verde"] = d["control_del_replay"]["verde"]
        d["control_desvios"] = d["control_del_replay"]["desvios"]
        # Contexto, no corte: lo que ya se movió entre el día del run y hoy,
        # que son los dos cortes del 09-20 (#177 y #178), ya declarados.
        ya_movido = diff_de_scores(sub, base, a)
        d["ya_movido_por_los_cortes_del_09_20"] = {
            "cambian": ya_movido["cambian"],
            "score_medio_el_dia_del_run": ya_movido["score_medio_antes"],
            "score_medio_antes_de_esta_tanda": ya_movido["score_medio_hoy"],
            "aspecto_medio_el_dia_del_run": ya_movido["aspecto_medio_antes"],
        }
        d["fijadas_antes"] = a["replay"]["fijadas"]
        d["fijadas_hoy"] = h["replay"]["fijadas"]
        d["competencias_antes"] = a["replay"]["competencias"]
        d["competencias_hoy"] = h["replay"]["competencias"]
        d["adoptadas_antes"] = a["replay"]["adoptadas"]
        d["adoptadas_hoy"] = h["replay"]["adoptadas"]
        resultado_brazos[nombre_brazo] = d
    doc["serie_c"] = resultado_brazos

    # ── 5. La saturación del aspecto (d21.3) ─────────────────────────
    if not args.sin_saturacion:
        print("· re-midiendo la saturación del aspecto sobre toda la base…",
              file=sys.stderr)
        todas = todas_las_respuestas()
        f_asp = os.path.join(tmpdir, "aspecto.json")
        with io.open(f_asp, "w", encoding="utf-8") as fh:
            json.dump([r["texto"] for r in todas], fh, ensure_ascii=False)
        pa_ = correr_brazo(tmpref, ["--aspecto", f_asp])["puntos_aspecto"]
        ph_ = correr_brazo(None, ["--aspecto", f_asp])["puntos_aspecto"]
        n = len(pa_) or 1
        por_grupo: dict = collections.defaultdict(lambda: [0.0, 0.0, 0])
        for r, x, y in zip(todas, pa_, ph_):
            g = por_grupo[f"{r['era']}/{r['serie']}"]
            g[0] += x
            g[1] += y
            g[2] += 1
        doc["d21_3_saturacion"] = {
            "poblacion": "todas las respuestas de la base",
            "respuestas": len(pa_),
            "tope": TOPE_ASPECTO,
            "media_antes": round(sum(pa_) / n, 4),
            "media_hoy": round(sum(ph_) / n, 4),
            "al_tope_antes": sum(1 for x in pa_ if x >= TOPE_ASPECTO),
            "al_tope_hoy": sum(1 for x in ph_ if x >= TOPE_ASPECTO),
            "pct_al_tope_antes": round(
                100.0 * sum(1 for x in pa_ if x >= TOPE_ASPECTO) / n, 2),
            "pct_al_tope_hoy": round(
                100.0 * sum(1 for x in ph_ if x >= TOPE_ASPECTO) / n, 2),
            "sin_aspecto_antes": sum(1 for x in pa_ if not x),
            "sin_aspecto_hoy": sum(1 for x in ph_ if not x),
            "cambian": sum(1 for x, y in zip(pa_, ph_) if x != y),
            "por_era_y_serie": {
                k: {"respuestas": v[2],
                    "media_antes": round(v[0] / (v[2] or 1), 4),
                    "media_hoy": round(v[1] / (v[2] or 1), 4)}
                for k, v in sorted(por_grupo.items())},
            "nota": ("d21.3 se decidió A —escribir la trampa, no cambiar el "
                     "peso— con el matiz de VOLVER A MEDIR después de d21.1 y "
                     "d21.2: «al exigir verbo de verdad la saturación puede "
                     "caerse sola». Aquí está el número nuevo. Si sigue "
                     "pegado al tope, el rediseño del peso (opción B) queda "
                     "abierto con su propio diseño en 5-experimento/"),
        }

    # ── Informe por pantalla ─────────────────────────────────────────
    ins = doc["instrumento"]
    print("\n" + "═" * 72)
    print("EL INSTRUMENTO")
    print("═" * 72)
    print(f"  VOCABULARIO_BASE   {ins['vocabulario_base']['antes']} → "
          f"{ins['vocabulario_base']['hoy']}")
    print(f"  FORMAS_DE_PLANTILLA {ins['formas_de_plantilla']['antes']} → "
          f"{ins['formas_de_plantilla']['hoy']}  "
          f"(+{len(ins['puerta_entran'])} / −{len(ins['puerta_salen'])})")
    print(f"  _RAICES_VERB       {ins['raices_verb']['antes']} → "
          f"{ins['raices_verb']['hoy']}   ·  caquetías (las que el detector "
          f"mira ahora): {ins['raices_verb_caquetias_hoy']}")
    print(f"  claves de TODAS_LAS_REGLAS: entran {ins['claves_de_todas_las_reglas']['entran']} "
          f"· salen {ins['claves_de_todas_las_reglas']['salen']}")

    print("\n" + "═" * 72)
    print("EL DESAFIJADOR, DECISIÓN POR DECISIÓN")
    print("═" * 72)
    ctrl = doc["desafijador"]["control_segmentador_local"]
    print(f"  control del segmentador: "
          f"{'VERDE' if ctrl['verde'] else 'ROJO'} "
          f"({ctrl['desvios_antes']}/{ctrl['desvios_hoy']} desvíos de "
          f"{len(formas)} formas)")
    d5 = doc["desafijador"]["d21_5_reagrupacion_no_mueve_el_nucleo"]
    print(f"  d21.5  reagrupar ka-/ma-: claves iguales "
          f"{d5['claves_iguales']} · formas que cambian de núcleo "
          f"{d5['diff']['formas']}  "
          f"{'✓ INVARIANTE' if d5['diff']['formas'] == 0 else '⚠ SE MOVIÓ'}")
    for k, etiqueta in (("d21_9_naiki", "d21.9  sacar -naiki"),
                        ("d21_13_no_poseido", "d21.13 añadir u-")):
        v = doc["desafijador"][k]
        print(f"  {etiqueta}: {v['diff']['formas']} formas / "
              f"{v['diff']['usos']} usos cambian de núcleo")
    v = doc["desafijador"]["d21_14_bakoa"]
    print(f"  d21.14 -bacoa → -bakoa: {v['formas_que_dejan_de_segmentarse_igual']} "
          f"formas dejan de segmentarse igual ({v['diff']['usos']} usos); "
          f"de ellas cambian de raíz-de-ninguna-parte "
          f"{v['de_ellas_cambian_es_raiz_de_ninguna_parte']} y de familia "
          f"{v['de_ellas_cambian_de_familia_en_el_corte_entero']} → "
          f"{'LIMPIA' if v['limpia'] else '⚠ NO LIMPIA'}")

    print("\n" + "═" * 72)
    print("EL PROMPT")
    print("═" * 72)
    pr = doc["el_prompt"]
    print(f"  ¿cambia?  {'SÍ' if pr['el_prompt_cambia'] else 'NO'}")
    print(f"  plantillas que cambian: {pr['plantillas_que_cambian']}")
    for k, v in pr["plantillas"].items():
        if v["texto_cambia"]:
            print(f"    {k:<36} {v['antes']:>6} → {v['hoy']:>6}  "
                  f"({v['delta']:+d})")
    print(f"  estáticas en total: {pr['caracteres_estaticos']['antes']} → "
          f"{pr['caracteres_estaticos']['hoy']}")
    if "ensayo_de_los_63" in pr:
        e = pr["ensayo_de_los_63"]
        print(f"  system prompt de los 63: medio {e['antes']['medio']} → "
              f"{e['hoy']['medio']}  ({e['delta_medio']:+})")

    print("\n" + "═" * 72)
    print("¿MUEVE EL SCORE? — la serie C, los dos brazos")
    print("═" * 72)
    for nombre_brazo, d in doc["serie_c"].items():
        ym = d["ya_movido_por_los_cortes_del_09_20"]
        print(f"\n  [{nombre_brazo}] control del replay (módulo {REF_RUN}, el "
              f"del run): {'VERDE' if d['control_verde'] else 'ROJO'} "
              f"({d['control_desvios']} desvíos de {d['n']})")
        print(f"    ya movido por los cortes del 09-20 (#177, #178): "
              f"{ym['cambian']} de {d['n']} · medio "
              f"{ym['score_medio_el_dia_del_run']} → "
              f"{ym['score_medio_antes_de_esta_tanda']}")
        print("    ── esta tanda ──")
        print(f"    score cambia en {d['cambian']} de {d['n']} "
              f"({d['a_la_baja']} a la baja, {d['al_alza']} al alza) · "
              f"|Δ| máx {d['delta_max_abs']} · "
              f"Δ medio de las que cambian {d['delta_medio_de_las_que_cambian']}")
        print(f"    score medio {d['score_medio_antes']} → {d['score_medio_hoy']}")
        print(f"    palabras_caquetias cambian en {d['caquetias_cambian']} · "
              f"neologisms_proposed en {d['neos_cambian']}")
        print(f"    aspecto medio {d['aspecto_medio_antes']} → "
              f"{d['aspecto_medio_hoy']} (tope {TOPE_ASPECTO}) · "
              f"al tope {d['respuestas_con_aspecto_al_tope_antes']} → "
              f"{d['respuestas_con_aspecto_al_tope_hoy']} · "
              f"sin aspecto {d['respuestas_sin_aspecto_antes']} → "
              f"{d['respuestas_sin_aspecto_hoy']}")
        print(f"    koiné fijada antes: {[f['forma'] for f in d['fijadas_antes']]}")
        print(f"    koiné fijada hoy:   {[f['forma'] for f in d['fijadas_hoy']]}")

    if "d21_3_saturacion" in doc:
        s = doc["d21_3_saturacion"]
        print("\n" + "═" * 72)
        print("LA SATURACIÓN DEL ASPECTO (d21.3) — toda la base")
        print("═" * 72)
        print(f"  {s['respuestas']} respuestas · tope {s['tope']}")
        print(f"  media   {s['media_antes']} → {s['media_hoy']}")
        print(f"  al tope {s['al_tope_antes']} ({s['pct_al_tope_antes']} %) → "
              f"{s['al_tope_hoy']} ({s['pct_al_tope_hoy']} %)")
        print(f"  sin aspecto {s['sin_aspecto_antes']} → {s['sin_aspecto_hoy']} "
              f"· cambian {s['cambian']}")

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# GENERADO por 6-fusion/scripts/medir_tanda_21.py\n")
        fh.write("# No se edita a mano. Ninguna cifra de aquí se escribe dos veces.\n")
        fh.write("\n".join(volcar(doc)) + "\n")
    print(f"\n→ {os.path.relpath(SALIDA, RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
