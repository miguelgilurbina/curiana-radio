#!/usr/bin/env python3
"""LA RAÍZ DE NINGUNA PARTE, medida: cuánto castellano entró vestido de lengua propia.

EL DEFECTO (destapado el 2026-09-20 por el brazo de control de la serie C,
runs `0345840d` → `45618069` → `e98227eb`):

    `curiana_lexicon._familia_de_token()` termina con
    `return "caquetío"  # neologismo comunitario`.

Esa línea es correcta para una acuñación hecha con morfemas del canon
(`biro-ana`, `kasi-nii-bana`) y es un agujero para cualquier otra cosa: una
raíz que NO está en ninguna tabla del lexicón, con afijos caquetíos pegados,
sale «caquetío». Así `lumina-bana-iro` —del latín/castellano *lumina*, que el
propio agente declaró en su glosa «del español, pero transformada en
caquetío»— llegó a ser la segunda forma más fuerte de su disputa, y
`lumina-bana-uco` **fijó** el cometa en el diccionario koiné del brazo de
control.

Este script MIDE el agujero. No decide nada: el arreglo va aparte y su corte,
si lo hay, se declara en el punto 11 del «Cambio de instrumento» de
`5-experimento/BITACORA_RUNS.md`.

Qué mide, en orden:

  1. EL CENSO POR CLASES sobre TODA la base (`word_uses` con
     `source_language='caquetío'`), por era, serie y run. Cuatro clases, y las
     tres primeras son falsos positivos que se DICEN y no se cuentan:

       raiz_conocida    algún segmento del núcleo es voz del lexicón de HOY
                        (`VOCABULARIO_BASE`, `FUERA_DEL_HABLA`, `_RAICES_VERB`,
                        o la clave con su desambiguador de lengua). Es el caso
                        normal y absorbe el compuesto que el desafijador no
                        supo partir.
       canon_retirado   ningún segmento es voz de HOY pero alguno SÍ lo era el
                        día del run. `chacamba`, `corie`, `canoa`, `hamaca`
                        eran claves del canon en junio y hoy no están: la
                        deriva del lexicón no es un agujero del clasificador.
                        Se reconstruye el `VOCABULARIO_BASE` histórico
                        importando el módulo del commit que corresponde.
       acunada          raíz de ninguna parte que el propio run (o uno
                        anterior de su cadena) DECLARÓ en `neologisms`.
       ninguna_parte    raíz de ninguna parte y nadie la declaró.

     Las dos últimas son la clase que importa. Se cuentan aparte porque la
     etiqueta que se propone para `word_uses.source_language` es distinta.

  2. LAS RAÍCES, UNA A UNA. Las raíces distintas de la clase que importa, con
     su frecuencia, dónde se dijeron y si son reconocibles: castellano o latín
     (`lumina`, `tension`, `suave`), nombre del elenco, o ruido del modelo. Y
     la GLOSA con que el agente la presentó, que a veces lo dice todo.

  3. HASTA DÓNDE LLEGARON. Cuántas se adoptaron (`neologisms.status`), cuántas
     entraron en una competencia y cuántas FIJARON una entrada de
     `koine_lexicon`. La competencia no vive en la base: se reconstruye con el
     mismo replay del punto 4.

  4. ¿MUEVE EL SCORE? Los 6 runs de la serie C —los tres del brazo con escena
     (`f2741e89` → `fcdfa07a` → `0313d830`) y los tres del control
     (`0345840d` → `45618069` → `e98227eb`), 216 + 216 respuestas— se
     re-ejecutan enteros por el pipeline del Observer, dos veces: con el
     lexicón de `--ref` (el de antes del arreglo) y con el del árbol de
     trabajo. Se comparan respuesta a respuesta `score`, `palabras_caquetias`
     y `neologisms_proposed`, y run a run las competencias y las entradas de
     koiné fijadas.

     CONTROL: el brazo «antes» tiene que reproducir el `score` y el
     `neologisms_proposed` que la base guardó. Si el control está en rojo, lo
     de arriba no mide nada.

  5. LA ERA 1. Las 2.071 respuestas del elenco viejo, re-puntuadas igual, para
     decir si el arreglo la mueve y cuánto. (`--sin-era1` la salta.)

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/medir_raices_de_ninguna_parte.py
    python 6-fusion/scripts/medir_raices_de_ninguna_parte.py --sin-era1
    python 6-fusion/scripts/medir_raices_de_ninguna_parte.py --ref <sha>

CÓMO SE MIDE EL «ANTES», sin cifras a mano: se saca `curiana_lexicon.py` y
`curiana_koine.py` del commit `REF` con `git show`, se dejan en un directorio
temporal que va PRIMERO en el `sys.path` de un subproceso, y ese subproceso
corre exactamente el mismo código de medición que el de hoy. Es el patrón de
`medir_politica_atestiguado_manda.py`.

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
import tarfile
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

FECHA = "2026-09-20"
SALIDA = os.path.join(RAIZ, "6-fusion",
                      f"medicion_raices_de_ninguna_parte_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"

# El commit ANTES del arreglo: el último merge a main del 2026-09-20, con los
# dos brazos de la serie C ya en la bitácora y el agujero todavía abierto.
REF = "b8c85ca"

# Los dos brazos de la serie C, en el orden de su cadena. Se verifica abajo
# contra `continuado_desde` que son cadenas y no una lista a mano.
BRAZOS = {
    "con_escena": ("f2741e89", "fcdfa07a", "0313d830"),
    "control":    ("0345840d", "45618069", "e98227eb"),
}
CADENCIA_NOMBRAMIENTO = 4          # curiana_orchestrator_v2.auto_mode
SEPARADOR = "\x1f"
FIN_DE_FILA = "\x1e"


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


def usos_caquetios() -> list[dict]:
    """Todo `word_uses` marcado «caquetío», agrupado por forma y run."""
    filas = psql(
        "select w.word, substring(w.run_id::text,1,8), "
        "coalesce(s.config->>'elenco','era1'), "
        "coalesce(s.config->>'serie','-'), "
        "coalesce(substring(s.config->>'motor_commit',1,40),''), "
        "to_char(s.started_at,'YYYY-MM-DD\"T\"HH24:MI:SS'), count(*) "
        "from word_uses w join simulation_runs s on s.id = w.run_id "
        "where w.source_language = 'caquetío' "
        "group by 1,2,3,4,5,6;")
    return [{"forma": f[0], "run": f[1], "era": f[2], "serie": f[3],
             "commit": f[4], "fecha": f[5], "usos": int(f[6])}
            for f in filas if f[0]]


def neologismos() -> list[dict]:
    filas = psql(
        "select substring(run_id::text,1,8), form, coalesce(components,''), "
        "coalesce(meaning,''), coalesce(status,''), coalesce(proposed_by,'') "
        "from neologisms;")
    return [{"run": f[0], "forma": f[1], "componentes": f[2],
             "significado": f[3], "estado": f[4], "autor": f[5]}
            for f in filas if len(f) >= 6 and f[1]]


def koine_fijadas() -> list[dict]:
    filas = psql("select substring(run_id::text,1,8), concepto_id, form, "
                 "fijada_dia, soporte, n_variantes from koine_lexicon;")
    return [{"run": f[0], "concepto": f[1], "forma": f[2], "dia": f[3],
             "soporte": f[4], "n_variantes": f[5]} for f in filas]


def emergente_de_la_base(id8: tuple) -> list[list]:
    """La serie emergente que el MOTOR guardó para esos runs, día a día.
    Es el control de la reconstrucción: si el brazo «antes» no la reproduce,
    la serie reconstruida no dice nada del veredicto."""
    filas = psql(
        "select m.day, m.distance_emergente from koine_metrics m "
        "where substring(m.run_id::text,1,8) in ("
        + ", ".join(f"'{i}'" for i in id8) + ") order by m.day;")
    return [[int(d), float(v)] for d, v in filas if v not in ("", None)]


def cadenas() -> dict[str, list[str]]:
    """Para cada run, la lista de runs anteriores de su cadena (id8)."""
    filas = psql("select id::text, substring(id::text,1,8), "
                 "coalesce(config->>'continuado_desde','') "
                 "from simulation_runs;")
    por_id = {f[0]: f[1] for f in filas}
    desde = {f[1]: f[2] for f in filas}
    salida: dict[str, list[str]] = {}
    for _id, i8 in por_id.items():
        cadena, cur, vistos = [], desde.get(i8, ""), set()
        while cur and cur not in vistos:
            vistos.add(cur)
            prev8 = por_id.get(cur)
            if not prev8:
                break
            cadena.append(prev8)
            cur = desde.get(prev8, "")
        salida[i8] = cadena
    return salida


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


# ══════════════════════════════════════════════════════════════════════
# EL LEXICÓN HISTÓRICO: qué era canon el día del run
# ══════════════════════════════════════════════════════════════════════
def _commit_del_lexicon(fecha: str) -> str:
    """El último commit que tocó `curiana_lexicon.py` antes de esa fecha.
    Es lo que se usa para los runs viejos, que no sellaron su huella."""
    out = subprocess.run(
        ["git", "-C", RAIZ, "rev-list", "-1", f"--before={fecha}", "HEAD",
         "--", "curiana_sim/curiana_lexicon.py"],
        capture_output=True, text=True, encoding="utf-8")
    return (out.stdout or "").strip()


def claves_historicas(commit: str) -> frozenset:
    """`VOCABULARIO_BASE` tal como era en ese commit.

    No vale un regex: sólo 1.496 de las 5.507 claves están escritas en el
    módulo; el resto entran de los `lexicon_*.py` generados al importarlo. Así
    que se extrae el árbol entero de `curiana_sim/` a un temporal y se importa
    de verdad, en un subproceso, con el `dotenv` stubbeado."""
    if not commit:
        return frozenset()
    tmp = tempfile.mkdtemp(prefix="curiana_hist_")
    tar = os.path.join(tmp, "arbol.tar")
    out = subprocess.run(["git", "-C", RAIZ, "archive", "-o", tar, commit,
                          "curiana_sim"], capture_output=True, text=True)
    if out.returncode != 0:
        return frozenset()
    with tarfile.open(tar) as t:
        t.extractall(tmp)                                 # noqa: S202
    sim = os.path.join(tmp, "curiana_sim")
    guion = (
        "import sys, types, json\n"
        "_s = types.ModuleType('dotenv')\n"
        "_s.load_dotenv = lambda *a, **k: None\n"
        "_s.dotenv_values = lambda *a, **k: {}\n"
        "sys.modules['dotenv'] = _s\n"
        "sys.argv = ['x']\n"
        "import curiana_lexicon as L\n"
        "claves = set(L.VOCABULARIO_BASE)\n"
        "claves |= set(getattr(L, 'FUERA_DEL_HABLA', {}))\n"
        "sys.stdout.write(json.dumps(sorted(claves)))\n")
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("CURIANA_ELENCO", None)          # el elenco no cambia el lexicón
    r = subprocess.run([sys.executable, "-c", guion], capture_output=True,
                       text=True, encoding="utf-8", cwd=sim, env=env)
    if r.returncode != 0:
        return frozenset()
    try:
        return frozenset(json.loads(r.stdout))
    except Exception:                                     # noqa: BLE001
        return frozenset()


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO: lo que se mide DENTRO de un lexicón (hoy o el de REF)
# ══════════════════════════════════════════════════════════════════════
def _replay(L, filas: list[dict]) -> dict:
    """Re-ejecuta el pipeline del Observer sobre las respuestas, en su orden y
    encadenando los días como lo hizo `--continuar`. Lo que cambia entre
    brazos no es una bandera: es el LEXICÓN. Patrón de
    `medir_politica_atestiguado_manda.py::_replay`."""
    from curiana_koine import (CampoLexico, CompetenciaLexica, IdiolectoAgente,
                               REFERENTES_NOVEDOSOS, distancia_idiolectal,
                               emocionar_de)
    from curiana_observer import ObserverAgent

    lexico = L.LexicoComunitario(filtrar_plantilla=True)
    observer = ObserverAgent(None, lexico)
    competencia = CompetenciaLexica(filtrar_plantilla=True)
    campo = CampoLexico()
    pendientes = [dict(r) for r in REFERENTES_NOVEDOSOS]
    # Los idiolectos, como los arma `auto_mode`: uno por agente del elenco
    # ACTIVO, pre-cargado con su emocionar. Es lo que hace falta para
    # reproducir `distance_emergente`, que es la lectura del veredicto.
    try:
        from curiana_agents import ALL_AGENTS
        idiolectos = {nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia")))
                      for nm, a in ALL_AGENTS.items()}
    except Exception:                                     # noqa: BLE001
        idiolectos = {}
    excluidas = getattr(L, "PUERTA_DEL_RECUENTO", L.FORMAS_DE_PLANTILLA)
    serie_emergente: list[list] = []

    turnos, visto = [], None
    for f in filas:
        if (f["run"], f["dia"], f["turno"]) != visto:
            turnos.append([])
            visto = (f["run"], f["dia"], f["turno"])
        turnos[-1].append(f)

    def cerrar_dia(dia: int, participantes: set) -> None:
        """Lo que `auto_mode` hace al cerrar un día: fijación y la distancia
        emergente sobre quienes hablaron. `min_formas=3` y `ventana=True` son
        los valores con los que el motor la llama — no se eligen aquí."""
        for cid, forma in competencia.evaluar_fijacion(dia):
            fijadas.append({"run": run_previo, "concepto": cid, "forma": forma})
        if idiolectos and participantes:
            d = distancia_idiolectal(idiolectos, solo=participantes,
                                     ventana=True, excluir=excluidas,
                                     min_formas=3)
            serie_emergente.append([dia, None if d is None else round(d, 4)])

    salida, fijadas, run_previo, t = [], [], None, 0
    participantes: set = set()
    for turno in turnos:
        if turno[0]["run"] != run_previo:
            if run_previo is not None:
                cerrar_dia(turno[0]["dia"] - 1, participantes)
                participantes = set()
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
                participantes.add(fila["agente"])
            salida.append({
                "run": fila["run"], "agente": fila["agente"],
                "dia": fila["dia"], "turno": fila["turno"],
                "score": reg.score,
                "palabras_caquetias": len(reg.palabras_caquetias),
                "neologisms_proposed": len(neos),
                "caquetias": sorted(reg.palabras_caquetias),
            })
        t += 1
    cerrar_dia(turnos[-1][0]["dia"] if turnos else 0, participantes)

    variantes = {cid: sorted(ref["variantes"].items(), key=lambda x: -x[1])
                 for cid, ref in competencia.referentes.items()
                 if ref["variantes"]}
    return {
        "respuestas": salida,
        "fijadas": fijadas,
        "serie_emergente": serie_emergente,
        "competencias": {cid: [[f, round(p, 2)] for f, p in v[:8]]
                         for cid, v in variantes.items()},
        "en_competencia": sorted({f for v in variantes.values() for f, _ in v}),
        "adoptadas": sorted({n.forma for n in lexico.neologismos_adoptados()}),
        "registradas": sorted({n.forma for n in lexico._neologismos}),
        "rechazos_de_plantilla": [list(r) for r in lexico.rechazos_de_plantilla],
        "rechazos_de_raiz": [list(r) for r in
                             getattr(lexico, "rechazos_de_raiz", [])],
    }


def medir_en_proceso(args) -> dict:
    """Todo lo que depende del LEXICÓN cargado en este proceso."""
    import curiana_lexicon as L

    d = {
        "modulo": os.path.abspath(L.__file__),
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "fuera_del_habla": len(L.FUERA_DEL_HABLA),
        "formas_de_plantilla": len(L.FORMAS_DE_PLANTILLA),
        "tiene_gate_de_raiz": hasattr(L, "es_raiz_de_ninguna_parte"),
    }
    if args.sondas:
        sondas = json.load(io.open(args.sondas, encoding="utf-8"))
        d["familia"] = {t: L._familia_de_token(t) for t in sondas}
        d["neologismo_valido"] = {t: L.neologismo_valido(t) for t in sondas}
        if hasattr(L, "es_raiz_de_ninguna_parte"):
            d["ninguna_parte"] = {t: L.es_raiz_de_ninguna_parte(t)
                                  for t in sondas}
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = _replay(L, filas)
    return d


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO DE ANTES: el módulo del commit REF, en un subproceso
# ══════════════════════════════════════════════════════════════════════
def modulos_de_ref(ref: str) -> str:
    tmp = tempfile.mkdtemp(prefix="curiana_ref_")
    for nombre in ("curiana_lexicon.py", "curiana_koine.py",
                   "curiana_database.py"):
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


def correr_brazo(lexicon_dir: str | None, extra: list[str],
                 elenco: str = "era2") -> dict:
    """Este mismo script, en un subproceso, con el lexicón que se le diga."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["CURIANA_ELENCO"] = elenco
    if elenco == "era1":
        env.pop("CURIANA_ELENCO")
    rutas = ([lexicon_dir] if lexicon_dir else []) + [SIM]
    env["PYTHONPATH"] = os.pathsep.join(rutas)
    out = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--json"] + extra,
        capture_output=True, encoding="utf-8", env=env, cwd=SIM)
    if out.returncode != 0:
        raise RuntimeError("el brazo falló:\n" + (out.stderr or "")[-3000:])
    return json.loads(out.stdout)


# ══════════════════════════════════════════════════════════════════════
# EL CLASIFICADOR (la misma regla que el arreglo, sin depender de él)
# ══════════════════════════════════════════════════════════════════════
class Clasificador:
    """Dice si la raíz de una forma está en alguna tabla del lexicón.

    Se construye con el módulo de HOY. La regla es la del arreglo:
    se quitan de los BORDES los afijos que el proyecto DECLARA caquetíos
    (`TODAS_LAS_REGLAS`) y lo que queda es el NÚCLEO; si ningún segmento del
    núcleo es voz conocida, la raíz no es de ninguna parte.

    Lo que se cuenta como voz conocida: `VOCABULARIO_BASE`, `FUERA_DEL_HABLA`,
    `_RAICES_VERB`, y la clave sin su desambiguador de lengua (`casa-lokono`
    hace conocida a `casa`).
    """

    def __init__(self, L):
        self.L = L
        self.prefijos = frozenset(L._PREFIJOS_CAQ)
        self.sufijos = frozenset(L._SUFIJOS_CAQ)
        conocidas = set(L.VOCABULARIO_BASE) | set(L.FUERA_DEL_HABLA)
        for k in list(conocidas):
            if "-" in k and k.rsplit("-", 1)[-1] in L._SUFIJOS_DE_LENGUA:
                conocidas.add(k.rsplit("-", 1)[0])
        self.conocidas = frozenset(conocidas | set(L._RAICES_VERB))

    def nucleo(self, tok: str) -> list[str]:
        partes = (tok or "").lower().split("-")
        while len(partes) > 1 and partes[0] + "-" in self.prefijos:
            partes = partes[1:]
        while len(partes) > 1 and "-" + partes[-1] in self.sufijos:
            partes = partes[:-1]
        return partes

    def raiz(self, tok: str) -> str:
        return "-".join(self.nucleo(tok))

    def candidatos(self, tok: str) -> list[str]:
        """Los mismos candidatos que prueba `_familia_de_token()` hoy."""
        tok = (tok or "").lower()
        out = [tok]
        if "-" in tok:
            partes = tok.split("-")
            nuc = partes
            if len(nuc) > 1 and nuc[0] + "-" in self.prefijos:
                nuc = nuc[1:]
                out.append("-".join(nuc))
            while len(nuc) > 1 and "-" + nuc[-1] in self.sufijos:
                nuc = nuc[:-1]
                out.append("-".join(nuc))
            if partes[0] in self.L._RAICES_VERB:
                out.append(partes[0])
            out.append(tok.split("-", 1)[1])
            out.append(partes[0])
        return out

    def resuelve_hoy(self, tok: str) -> bool:
        """¿`_familia_de_token()` encuentra entrada, o cae en el `return
        "caquetío"` del final?"""
        return any(c in self.L.VOCABULARIO_BASE for c in self.candidatos(tok))

    def de_ninguna_parte(self, tok: str, extra: frozenset = frozenset()) -> bool:
        seg = self.nucleo(tok)
        return not any(s in self.conocidas or s in extra for s in seg)


def reconocible(L, raiz: str, nombres: frozenset) -> str:
    """¿De qué se parece esta raíz de ninguna parte?"""
    r = raiz.lower()
    partes = [p for p in r.split("-") if p]
    if any(p in nombres for p in partes):
        return "nombre-del-elenco"
    if any(p in L.RAICES_ESPANOLAS or p in L.ES_STOPWORDS
           or p in L.CASTELLANO_CORRIENTE for p in partes):
        return "castellano"
    if any(L._MARCADORES_ES.search(p) for p in partes):
        return "castellano-por-ortografía"
    if any(L._componente_espanol(p) for p in partes):
        return "castellano-por-fonotáctica"
    return "sin-identificar"


# ══════════════════════════════════════════════════════════════════════
# LOS CRUCES
# ══════════════════════════════════════════════════════════════════════
def diff_de_scores(filas, antes, hoy) -> dict:
    """Respuesta a respuesta: control contra la base y delta entre brazos."""
    a = antes["replay"]["respuestas"]
    h = hoy["replay"]["respuestas"]
    if len(a) != len(h) or len(a) != len(filas):
        raise RuntimeError(f"replays desalineados: {len(filas)}/{len(a)}/{len(h)}")
    control = [i for i, (f, r) in enumerate(zip(filas, a))
               if abs(f["score_guardado"] - r["score"]) > 1e-9
               or f["neos_guardados"] != r["neologisms_proposed"]]
    cambian, deltas, por_run = [], [], collections.defaultdict(list)
    for f, ra, rh in zip(filas, a, h):
        d = round(rh["score"] - ra["score"], 4)
        por_run[f["run"]].append((ra["score"], rh["score"]))
        if abs(d) > 1e-9:
            deltas.append(d)
            perdidas = sorted(set(ra["caquetias"]) - set(rh["caquetias"]))
            cambian.append({"run": f["run"], "dia": f["dia"],
                            "turno": f["turno"], "agente": f["agente"],
                            "antes": ra["score"], "hoy": rh["score"],
                            "delta": d, "formas_que_dejan_de_contar": perdidas})
    n = len(a) or 1
    return {
        "n": len(a),
        "control_desvios": len(control),
        "cambian": len(cambian),
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
        "por_run": {r: {"antes": round(sum(x for x, _ in v) / len(v), 4),
                        "hoy": round(sum(y for _, y in v) / len(v), 4)}
                    for r, v in por_run.items()},
        "detalle": cambian[:60],
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
    ap.add_argument("--sondas", help="JSON con tokens a sondear (uso interno)")
    ap.add_argument("--respuestas", help="JSON con respuestas a re-puntuar")
    ap.add_argument("--ref", default=REF, help="commit del lexicón de ANTES")
    ap.add_argument("--sin-era1", action="store_true",
                    help="salta la re-puntuación de las 2.071 de la era 1")
    ap.add_argument("--sin-base", action="store_true",
                    help="sin Supabase: sólo el censo del lexicón")
    ap.add_argument("--solo-censo", action="store_true",
                    help="los puntos 1-3 y nada de re-puntuación")
    args = ap.parse_args(argv)

    if args.json:
        sys.stdout.write(json.dumps(medir_en_proceso(args), ensure_ascii=False))
        return 0

    sys.path.insert(0, SIM)
    import curiana_lexicon as L                            # noqa: E402
    clf = Clasificador(L)
    nombres = L._nombres_de_agentes()

    doc: dict = {
        "medicion": "raices-de-ninguna-parte",
        "fecha": FECHA,
        "ref_de_antes": args.ref,
        "regla": ("núcleo = el token sin los afijos que TODAS_LAS_REGLAS "
                  "declara caquetíos, quitados por los bordes; raíz de "
                  "ninguna parte = ningún segmento del núcleo es voz de "
                  "VOCABULARIO_BASE, FUERA_DEL_HABLA ni _RAICES_VERB"),
        "lexicon": {"vocabulario_base": len(L.VOCABULARIO_BASE),
                    "fuera_del_habla": len(L.FUERA_DEL_HABLA),
                    "raices_conocidas": len(clf.conocidas)},
    }

    if args.sin_base:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        return 0

    # ── 1. El censo por clases ───────────────────────────────────────
    print("· leyendo word_uses…", file=sys.stderr)
    usos = usos_caquetios()
    neos = neologismos()
    fijadas = koine_fijadas()
    cad = cadenas()

    neos_por_run: dict[str, set] = collections.defaultdict(set)
    glosa_de: dict[str, list] = collections.defaultdict(list)
    for n in neos:
        neos_por_run[n["run"]].add(n["forma"].lower())
        glosa_de[n["forma"].lower()].append(n)

    def declarada(forma: str, run: str) -> bool:
        f = forma.lower()
        if f in neos_por_run.get(run, ()):
            return True
        return any(f in neos_por_run.get(prev, ()) for prev in cad.get(run, ()))

    # El lexicón histórico, uno por commit distinto (16 de la era auditada y
    # uno por fecha para los runs viejos, que no sellaron su huella).
    commits: dict[str, str] = {}
    for u in usos:
        clave = u["commit"] or f"fecha:{u['fecha']}"
        if clave not in commits:
            commits[clave] = u["commit"] or _commit_del_lexicon(u["fecha"])
    por_sha: dict[str, frozenset] = {}
    print(f"· reconstruyendo {len(set(commits.values()))} lexicones históricos…",
          file=sys.stderr)
    historico: dict[str, frozenset] = {}
    for clave, sha in commits.items():
        if sha not in por_sha:
            por_sha[sha] = claves_historicas(sha)
        historico[clave] = por_sha[sha]
    doc["lexicones_historicos"] = {
        "pedidos": len(commits),
        "reconstruidos": sum(1 for v in historico.values() if v),
        "tamanos": {k: len(v) for k, v in sorted(historico.items())},
        "sin_reconstruir": sorted(k for k, v in historico.items() if not v),
    }

    clases = collections.Counter()
    usos_por_clase = collections.Counter()
    por_grupo: dict = collections.defaultdict(
        lambda: {"formas": 0, "usos": 0, "ninguna_formas": 0, "ninguna_usos": 0,
                 "acunada_formas": 0, "acunada_usos": 0,
                 "retirado_formas": 0, "retirado_usos": 0})
    raices = collections.Counter()
    raices_formas: dict[str, set] = collections.defaultdict(set)
    raices_runs: dict[str, set] = collections.defaultdict(set)
    formas_c: dict[str, dict] = {}

    for u in usos:
        clave = u["commit"] or f"fecha:{u['fecha']}"
        g = por_grupo[(u["era"], u["serie"])]
        g["formas"] += 1
        g["usos"] += u["usos"]
        if not clf.de_ninguna_parte(u["forma"]):
            # (a) El compuesto que el desafijador de `_familia_de_token` NO
            # supo partir y que la regla por segmentos sí resuelve. Es un
            # falso positivo del clasificador viejo: se dice y no se cuenta.
            cl = ("raiz_conocida" if clf.resuelve_hoy(u["forma"])
                  else "compuesto_no_partido")
            clases[cl] += 1
            usos_por_clase[cl] += u["usos"]
            continue
        viejas = historico.get(clave, frozenset())
        if not clf.de_ninguna_parte(u["forma"], extra=viejas):
            clases["canon_retirado"] += 1
            usos_por_clase["canon_retirado"] += u["usos"]
            g["retirado_formas"] += 1
            g["retirado_usos"] += u["usos"]
            continue
        cl = "acunada" if declarada(u["forma"], u["run"]) else "ninguna_parte"
        clases[cl] += 1
        usos_por_clase[cl] += u["usos"]
        g[("acunada_formas" if cl == "acunada" else "ninguna_formas")] += 1
        g[("acunada_usos" if cl == "acunada" else "ninguna_usos")] += u["usos"]
        r = clf.raiz(u["forma"])
        raices[r] += u["usos"]
        raices_formas[r].add(u["forma"])
        raices_runs[r].add(f"{u['era']}/{u['serie']}")
        formas_c[u["forma"]] = {"run": u["run"], "clase": cl, "usos": u["usos"],
                                "raiz": r}

    doc["censo"] = {
        "formas_marcadas_caquetio": len(usos),
        "usos_marcados_caquetio": sum(u["usos"] for u in usos),
        "por_clase_formas": dict(clases.most_common()),
        "por_clase_usos": dict(usos_por_clase.most_common()),
        "por_era_y_serie": {
            f"{era}/{serie}": v for (era, serie), v in sorted(por_grupo.items())},
    }

    # ── 2. Las raíces, una a una ─────────────────────────────────────
    detalle_raices = []
    for r, n in raices.most_common():
        glosas = []
        for forma in sorted(raices_formas[r]):
            for g in glosa_de.get(forma.lower(), [])[:1]:
                glosas.append(f"{forma} = {g['componentes']} → {g['significado']}")
        detalle_raices.append({
            "raiz": r, "usos": n,
            "formas": sorted(raices_formas[r]),
            "donde": sorted(raices_runs[r]),
            "parece": reconocible(L, r, nombres),
            "glosa_del_agente": glosas[:2],
        })
    doc["raices_de_ninguna_parte"] = {
        "distintas": len(raices),
        "usos": sum(raices.values()),
        "por_parecido": dict(collections.Counter(
            d["parece"] for d in detalle_raices).most_common()),
        "detalle": detalle_raices[:80],
    }

    # ── 3. Hasta dónde llegaron ──────────────────────────────────────
    adoptadas = {n["forma"].lower() for n in neos if n["estado"] == "adoptado"}
    fijadas_c = [f for f in fijadas if f["forma"] in formas_c]
    doc["hasta_donde_llegaron"] = {
        "adoptadas": sorted(f for f in formas_c if f.lower() in adoptadas),
        "fijaron_koine": fijadas_c,
        "koine_lexicon_total": len(fijadas),
    }

    # EL COSTE DE LA PUERTA, dicho sobre lo que un agente PROPONE, que es otra
    # población que `word_uses`: cuántas de las acuñaciones distintas de una
    # cadena llevan raíz de ninguna parte. Es el número que convierte el
    # arreglo en una decisión de diseño («¿un pueblo no puede inventar una
    # raíz nueva?») y por eso se mide, no se estima.
    por_run_neos: dict[str, set] = collections.defaultdict(set)
    for n in neos:
        por_run_neos[n["run"]].add(n["forma"])
    coste = {}
    for nombre_cadena, id8 in list(BRAZOS.items()) + [
            ("serie_c_limpia", ("b847944d", "17c2271e", "9a98de67"))]:
        todas = set().union(*[por_run_neos[r] for r in id8] or [set()])
        malas = {f for f in todas if clf.de_ninguna_parte(f)}
        coste[nombre_cadena] = {
            "acunaciones_distintas": len(todas),
            "de_ninguna_parte": len(malas),
            "de_ellas_adoptadas": len([f for f in malas
                                       if f.lower() in adoptadas]),
            "lista": sorted(malas),
        }
    todas_neos = {n["forma"] for n in neos}
    coste["toda_la_base"] = {
        "acunaciones_distintas": len(todas_neos),
        "de_ninguna_parte": len([f for f in todas_neos
                                 if clf.de_ninguna_parte(f)]),
    }
    doc["coste_de_la_puerta"] = coste

    # ── 4. ¿Mueve el score? Los dos brazos de la serie C ─────────────
    if not args.solo_censo:
        ids = [i for b in BRAZOS.values() for i in b]
        filas = respuestas_de(ids)
        orden = {i: k for k, i in enumerate(ids)}
        filas.sort(key=lambda f: (orden[f["run"]], f["dia"], f["turno"]))
        print(f"· re-puntuando {len(filas)} respuestas de la serie C…",
              file=sys.stderr)

        tmpref = modulos_de_ref(args.ref)
        sondas = ["lumina-bana-iro", "lumina-bana-uco", "lumina",
                  "kasi-nii-bana", "biro-ana", "kasuta-ico-kana", "juri-ima",
                  "ka-to", "ta-bohío", "kali", "kali-mara-bana", "piache",
                  "chacamba"]
        f_sondas = os.path.join(tempfile.mkdtemp(), "sondas.json")
        with io.open(f_sondas, "w", encoding="utf-8") as fh:
            json.dump(sondas, fh, ensure_ascii=False)

        resultado_brazos = {}
        for nombre_brazo, id8 in BRAZOS.items():
            sub = [f for f in filas if f["run"] in id8]
            f_resp = os.path.join(tempfile.mkdtemp(), "resp.json")
            with io.open(f_resp, "w", encoding="utf-8") as fh:
                json.dump(sub, fh, ensure_ascii=False)
            extra = ["--respuestas", f_resp, "--sondas", f_sondas]
            antes = correr_brazo(tmpref, extra)
            hoy = correr_brazo(None, extra)
            d = diff_de_scores(sub, antes, hoy)
            d["sondas_antes"] = antes.get("familia", {})
            d["sondas_hoy"] = hoy.get("familia", {})
            d["ninguna_parte_hoy"] = hoy.get("ninguna_parte", {})
            d["fijadas_antes"] = antes["replay"]["fijadas"]
            d["fijadas_hoy"] = hoy["replay"]["fijadas"]
            d["competencias_antes"] = antes["replay"]["competencias"]
            d["competencias_hoy"] = hoy["replay"]["competencias"]
            d["rechazos_de_raiz"] = hoy["replay"].get("rechazos_de_raiz", [])
            d["adoptadas_antes"] = antes["replay"]["adoptadas"]
            d["adoptadas_hoy"] = hoy["replay"]["adoptadas"]
            # EL VEREDICTO, que es la pregunta que importa. La serie emergente
            # se reconstruye con los mismos idiolectos, la misma ventana y el
            # mismo `min_formas` con que la calcula `auto_mode`, y se juzga con
            # el mismo `veredicto_convergencia`. El CONTROL es la serie que el
            # motor guardó en `koine_metrics`: si el brazo «antes» no la
            # reproduce, este veredicto no mide nada.
            sys.path.insert(0, SIM)
            from curiana_koine import veredicto_convergencia  # noqa: E402
            base = emergente_de_la_base(id8)
            sa = [[x, y] for x, y in antes["replay"].get("serie_emergente", [])
                  if y is not None]
            sh = [[x, y] for x, y in hoy["replay"].get("serie_emergente", [])
                  if y is not None]
            d["emergente_de_la_base"] = base
            d["emergente_antes"] = sa
            d["emergente_hoy"] = sh
            d["control_emergente"] = (
                len(base) == len(sa)
                and all(abs(a[1] - b[1]) <= 0.0005 for a, b in zip(base, sa)))
            d["veredicto_antes"] = list(veredicto_convergencia(
                [(int(x), float(y)) for x, y in sa]))
            d["veredicto_hoy"] = list(veredicto_convergencia(
                [(int(x), float(y)) for x, y in sh]))
            d["veredicto_se_sostiene"] = (
                d["veredicto_antes"][0] == d["veredicto_hoy"][0])

            def _caida(serie):
                if len(serie) < 2 or not serie[0][1]:
                    return None
                return round(100.0 * (serie[-1][1] - serie[0][1]) / serie[0][1], 2)
            d["caida_pct_antes"] = _caida(sa)
            d["caida_pct_hoy"] = _caida(sh)
            resultado_brazos[nombre_brazo] = d
        doc["serie_c"] = resultado_brazos

    # ── 5. La era 1 ──────────────────────────────────────────────────
    if not args.sin_era1 and not args.solo_censo:
        id1 = [f[0] for f in psql(
            "select substring(id::text,1,8) from simulation_runs "
            "where coalesce(config->>'elenco','era1') <> 'era2' "
            "order by started_at;")]
        filas1 = respuestas_de(id1)
        print(f"· re-puntuando {len(filas1)} respuestas de la era 1…",
              file=sys.stderr)
        f_resp = os.path.join(tempfile.mkdtemp(), "era1.json")
        with io.open(f_resp, "w", encoding="utf-8") as fh:
            json.dump(filas1, fh, ensure_ascii=False)
        extra = ["--respuestas", f_resp]
        a1 = correr_brazo(tmpref, extra, elenco="era1")
        h1 = correr_brazo(None, extra, elenco="era1")
        doc["era1"] = diff_de_scores(filas1, a1, h1)
        doc["era1"].pop("detalle", None)
        # El CONTROL de la era 1 sale en rojo y no es por el arreglo: el
        # lexicón de junio tenía 1.262-1.703 claves y el de hoy 5.507, así que
        # re-puntuar respuestas de hace tres meses con el lexicón de hoy nunca
        # reproduce el score guardado. Lo que sí mide el A/B es el DELTA entre
        # los dos brazos de hoy. Y de ese delta hay que descontar lo que es
        # deriva del canon: una forma que la puerta rechaza hoy porque su raíz
        # ya no está en el lexicón, pero que el día del run SÍ lo estaba, no
        # habría sido rechazada entonces.
        viejas_era1 = frozenset().union(
            *[historico[k] for k in historico
              if k.startswith("fecha:")] or [frozenset()])
        rechazadas = sorted({f for f, *_ in h1["replay"].get("rechazos_de_raiz", [])})
        eran_canon = [f for f in rechazadas
                      if not clf.de_ninguna_parte(f, extra=viejas_era1)]
        doc["era1"]["rechazos_de_raiz"] = {
            "formas_distintas": len(rechazadas),
            "eran_canon_entonces": len(eran_canon),
            "lista_eran_canon": eran_canon[:40],
            "lista_nunca_fueron": [f for f in rechazadas if f not in eran_canon][:40],
        }

    # ── Informe por pantalla ─────────────────────────────────────────
    c = doc["censo"]
    print("\n" + "═" * 70)
    print("EL AGUJERO, POR CLASES")
    print("═" * 70)
    print(f"  word_uses marcados «caquetío»: {c['formas_marcadas_caquetio']} "
          f"formas · {c['usos_marcados_caquetio']} usos")
    for cl, n in c["por_clase_formas"].items():
        print(f"    {cl:<16} {n:>6} formas · "
              f"{c['por_clase_usos'].get(cl, 0):>6} usos")
    print("\n  por era y serie (formas / usos · de ninguna parte):")
    for k, v in c["por_era_y_serie"].items():
        print(f"    {k:<14} {v['formas']:>5} / {v['usos']:>6}   "
              f"ninguna {v['ninguna_formas']}+{v['acunada_formas']} formas, "
              f"{v['ninguna_usos'] + v['acunada_usos']} usos   "
              f"(retiradas del canon: {v['retirado_formas']})")

    print("\n" + "═" * 70)
    print("LAS RAÍCES DE NINGUNA PARTE")
    print("═" * 70)
    r = doc["raices_de_ninguna_parte"]
    print(f"  {r['distintas']} raíces distintas, {r['usos']} usos")
    print(f"  parecidos: {r['por_parecido']}")
    for d in r["detalle"][:20]:
        print(f"    {d['raiz']:<18} {d['usos']:>4} usos  [{d['parece']}] "
              f"{', '.join(d['formas'][:3])}")
        for g in d["glosa_del_agente"][:1]:
            print(f"        glosa: {g[:130]}")

    print("\n" + "═" * 70)
    print("HASTA DÓNDE LLEGARON")
    print("═" * 70)
    h = doc["hasta_donde_llegaron"]
    print(f"  adoptadas: {len(h['adoptadas'])} → {h['adoptadas'][:12]}")
    print(f"  fijaron una entrada de koiné: {h['fijaron_koine']}")
    print("\n  EL COSTE DE LA PUERTA — acuñaciones que deja fuera:")
    for nombre_cadena, v in doc["coste_de_la_puerta"].items():
        pct = (100.0 * v["de_ninguna_parte"] / v["acunaciones_distintas"]
               if v["acunaciones_distintas"] else 0.0)
        extra = (f" · {v['de_ellas_adoptadas']} de ellas adoptadas"
                 if "de_ellas_adoptadas" in v else "")
        print(f"    {nombre_cadena:<16} {v['de_ninguna_parte']:>3} de "
              f"{v['acunaciones_distintas']:>3} ({pct:.1f} %){extra}")

    print("\n" + "═" * 70)
    print("¿MUEVE EL SCORE? — la serie C, los dos brazos")
    print("═" * 70)
    for nombre_brazo, d in doc.get("serie_c", {}).items():
        estado = "VERDE" if d["control_desvios"] == 0 else "ROJO"
        print(f"\n  [{nombre_brazo}] control: {estado} "
              f"({d['control_desvios']} desvíos de {d['n']})")
        print(f"    score cambia en {d['cambian']} de {d['n']} · "
              f"|Δ| máx {d['delta_max_abs']} · "
              f"Δ medio de las que cambian {d['delta_medio_de_las_que_cambian']}")
        print(f"    score medio {d['score_medio_antes']} → {d['score_medio_hoy']}")
        print(f"    palabras_caquetias cambian en {d['caquetias_cambian']} · "
              f"neologisms_proposed en {d['neos_cambian']}")
        print(f"    koiné fijada antes: {[f['forma'] for f in d['fijadas_antes']]}")
        print(f"    koiné fijada hoy:   {[f['forma'] for f in d['fijadas_hoy']]}")
        print(f"    emergente del motor (koine_metrics): "
              f"{[v for _, v in d.get('emergente_de_la_base', [])]}")
        print(f"    emergente reconstruida antes:        "
              f"{[v for _, v in d.get('emergente_antes', [])]}  "
              f"control {'VERDE' if d.get('control_emergente') else 'ROJO'}")
        print(f"    emergente reconstruida hoy:          "
              f"{[v for _, v in d.get('emergente_hoy', [])]}")
        print(f"    caída antes {d.get('caida_pct_antes')} % · "
              f"hoy {d.get('caida_pct_hoy')} %")
        print(f"    veredicto antes: {d.get('veredicto_antes', ['?', ''])[1]}")
        print(f"    veredicto hoy:   {d.get('veredicto_hoy', ['?', ''])[1]}")
        print("    → EL VEREDICTO SE SOSTIENE" if d.get("veredicto_se_sostiene")
              else "    → ⚠ EL VEREDICTO CAMBIA")
        if d["rechazos_de_raiz"]:
            cuenta = collections.Counter(x[0] for x in d["rechazos_de_raiz"])
            print(f"    la puerta rechazó: {dict(cuenta.most_common(8))}")
    if "era1" in doc:
        d = doc["era1"]
        print(f"\n  [era 1] control: "
              f"{'VERDE' if d['control_desvios'] == 0 else 'ROJO'} "
              f"({d['control_desvios']} desvíos de {d['n']}) · "
              f"score cambia en {d['cambian']} · "
              f"medio {d['score_medio_antes']} → {d['score_medio_hoy']}")
        rr = d.get("rechazos_de_raiz", {})
        if rr:
            print(f"    el control ROJO es la deriva del lexicón —el de junio "
                  f"tenía ~1.700 claves y el de hoy 5.507—, no el arreglo: "
                  f"re-puntuar la era 1 con el lexicón de hoy nunca reproduce "
                  f"su score. Lo que sí mide el A/B es el delta.")
            print(f"    la puerta rechaza {rr['formas_distintas']} formas "
                  f"distintas en la era 1; {rr['eran_canon_entonces']} de "
                  f"ellas tenían la raíz en el canon el día del run")

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# GENERADO por 6-fusion/scripts/medir_raices_de_ninguna_parte.py\n")
        fh.write("# No se edita a mano. Ninguna cifra de aquí se escribe dos veces.\n")
        fh.write("\n".join(volcar(doc)) + "\n")
    print(f"\n→ {os.path.relpath(SALIDA, RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
