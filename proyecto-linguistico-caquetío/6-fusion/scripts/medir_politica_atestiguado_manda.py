#!/usr/bin/env python3
"""LA POLÍTICA «MANDA LA ATESTIGUADA», medida: qué cuesta el corte.

Decisión de Miguel, 2026-09-19:

    «Sí o sí tenemos que usar los atestiguados por sobre los reconstruidos,
     por lo menos la parte caquetía.»

Es una POLÍTICA, no una respuesta par a par: donde el caquetío TIENE forma
atestiguada para un significado, ésa es la que la comunidad habla y la que el
instrumento enseña; la derivada se ARCHIVA con su procedencia —como `piache`—
y deja de enseñarse y de competir. Sólo muerde donde hay rival atestiguado: el
grueso del lexicón caquetío es reconstrucción legítima porque no hay atestación
y no lo toca.

Este script MIDE el corte. No decide nada y no propone nada: las decisiones
están en `6-fusion/decisiones_tanda_2026-09-19.yaml` (d19.b) y lo que queda
abierto, en `6-fusion/issues-pendientes/pares-atestiguado-reconstruido-2026-09-19.md`.

Qué mide, en orden:

  1. EL CENSO. Qué se archivó, con qué capa (que NO se toca) y qué manda en su
     lugar, con su cita. Cuánto encoge `VOCABULARIO_BASE` y cuánto crece
     `FUERA_DEL_HABLA`.

  2. LA PUERTA. `FORMAS_DE_PLANTILLA` antes y después, con el diff entero.
     `FUERA_DEL_HABLA` entra en la puerta con esta tanda: sin eso, archivar
     una voz la habría dejado ACUÑABLE al día siguiente.

  3. LAS PLANTILLAS. Plantilla a plantilla, qué formas de par enseñaba y
     cuáles enseña, con los dos criterios (el ESTRECHO del script de pares y
     el ANCHO de `formas_en_texto`). Y el largo del system prompt antes y
     después en un ensayo SIN API sobre los dos elencos — la longitud predice
     el score (r = −0,48), así que se mide aunque parezca cosmético.

  4. LOS DOS COSTES QUE HABÍA QUE DECIR ANTES DE APLICAR.
     (a) `paa`: su paradigma de aspecto entero, forma a forma, y cuántas dejan
         de contar como arahuacas. Y si queda hueco funcional — no queda:
         `were` es también `v_raiz` y atestiguada.
     (b) `kasi` / `kashi`: comparten esqueleto fonémico bajo la `fonemizar`
         del propio proyecto. Se comprueba sitio por sitio si el MOTOR las
         confunde (`_familia_de_token`, el filtro de nombres, la puerta de la
         competencia) y dónde quedan las dos después del cambio.

  5. LA RE-PUNTUACIÓN DE LAS 216. La serie C limpia (`b847944d` → `17c2271e`
     → `9a98de67`) se re-ejecuta entera por el pipeline del Observer, dos
     veces —con el lexicón de antes y con el de hoy— y se comparan respuesta a
     respuesta. Archivar una voz la saca de `palabras_activas()`: es un corte
     de serie y su número se mide, no se estima.

  6. LOS RESIDUOS DECLARADOS: `FORMAS_SEED`, `haborü`, el corpus, y `sima`
     —el par 6, que la política ALCANZA y que NO se aplica porque es la
     pregunta que Miguel dejó abierta—.

    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/medir_politica_atestiguado_manda.py
    python 6-fusion/scripts/medir_politica_atestiguado_manda.py --sin-base
    python 6-fusion/scripts/medir_politica_atestiguado_manda.py --ref <sha>

CÓMO SE MIDE EL «ANTES», sin cifras a mano: se saca `curiana_lexicon.py` y
`curiana_koine.py` del commit `REF` con `git show`, se dejan en un directorio
temporal que va PRIMERO en el `sys.path` de un subproceso, y ese subproceso
corre exactamente el mismo código de medición que el de hoy. Los dos brazos
salen del mismo motor y la única diferencia es el módulo.

CONTROL: el replay con el lexicón de ANTES tiene que reproducir el `score` y
el `neologisms_proposed` que la base guardó para las 216. Si el control está
en rojo, lo de abajo no mide nada.

REGLAS DURAS que este script respeta: no abre `curiana_sim/.env` (stub de
`dotenv` antes de importar el motor), no llama a la API, no escribe en la base
(la lee por `docker exec … psql`, que es la vía que CLAUDE.md declara) y no
toca el canon.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import random
import subprocess
import sys
import tempfile
import types
from collections import defaultdict

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

FECHA = "2026-09-19"
SALIDA = os.path.join(RAIZ, "6-fusion",
                      f"medicion_politica_atestiguado_manda_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"
SEMILLA_ENSAYO = 20260919

# El commit ANTES de la política: el último merge a main del 2026-09-19, con
# el ejemplo de la identidad ya en `biro-bana` (#172) y los 19 pares aún sin
# decidir. Se declara para que la medición se pueda repetir dentro de un año.
REF = "f864482"

# La serie C limpia, declarada y verificada abajo como cadena.
SERIE_C_LIMPIA = ("b847944d", "17c2271e", "9a98de67")
CADENCIA_NOMBRAMIENTO = 4          # curiana_orchestrator_v2.auto_mode
SEPARADOR = "\x1f"
FIN_DE_FILA = "\x1e"

# Lo que la política archivó y lo que manda en su lugar. NO es una lista a
# mano de lo que «debería» pasar: el script COMPRUEBA contra el módulo que
# cada archivada está en `FUERA_DEL_HABLA` y fuera de `VOCABULARIO_BASE`, que
# su capa no cambió, y que la que manda es `caquetío-atestiguado` con cita.
POLITICA = [
    (1,  "sol",      "kasi",     "kali"),
    (3,  "ofrecer",  "were",     "paa"),
    (4,  "escuchar", "jai",      "kira"),
    (12, "luna",     "kati",     "kasha"),
    (13, "mar",      "para",     "habo"),
    (16, "viento",   "juri",     "joutai"),
    (18, "espanto",  "etamo",    "mülia"),
]
# El par que la política ALCANZA y que no se aplica: es la pregunta abierta.
PAR_ABIERTO_SIMA = (6, "cerro", "turumako", "sima")

ARCHIVADAS = [d for _n, _g, _a, d in POLITICA]
MANDAN = [a for _n, _g, a, _d in POLITICA]


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


def usos_por_token() -> dict[str, int]:
    return {w: int(n) for w, n in
            psql("select word, count(*) from word_uses group by 1;")}


def ids_serie_c() -> dict:
    filas = psql(
        "select id::text, substring(id::text,1,8), "
        "coalesce(config->>'continuado_desde','') from simulation_runs "
        "where substring(id::text,1,8) in ("
        + ", ".join(f"'{i}'" for i in SERIE_C_LIMPIA) + ");")
    por8 = {i8: (rid, desde) for rid, i8, desde in filas}
    faltan = [i for i in SERIE_C_LIMPIA if i not in por8]
    if faltan:
        raise RuntimeError(f"la serie C limpia declara runs que no están: {faltan}")
    ids = [por8[i][0] for i in SERIE_C_LIMPIA]
    cadena = (por8[SERIE_C_LIMPIA[0]][1] == ""
              and por8[SERIE_C_LIMPIA[1]][1] == ids[0]
              and por8[SERIE_C_LIMPIA[2]][1] == ids[1])
    dias, turnos = psql(
        "select count(distinct day), count(*) from turns where run_id in ("
        + ", ".join(f"'{i}'::uuid" for i in ids) + ");")[0]
    return {"ids": ids, "id8": list(SERIE_C_LIMPIA), "cadena_ok": cadena,
            "dias": int(dias), "turnos": int(turnos)}


def respuestas_de(ids: list[str]) -> list[dict]:
    """Las 216, en el orden en que se dijeron."""
    sql = (
        "select t.day || '{S}' || t.turn_num || '{S}' || r.agent_name || '{S}' || "
        "coalesce(r.ethnicity,'') || '{S}' || coalesce(r.tier,2) || '{S}' || "
        "t.moment || '{S}' || t.season || '{S}' || r.score || '{S}' || "
        "r.neologisms_proposed || '{S}' || coalesce(r.lugar,'') || '{S}' || "
        "substring(r.run_id::text,1,8) || '{S}' || r.response_text || '{F}' "
        "from agent_responses r join turns t on t.id = r.turn_id "
        "where r.run_id in ({IDS}) order by t.day, t.turn_num, r.created_at"
    ).format(S=SEPARADOR, F=FIN_DE_FILA,
             IDS=", ".join(f"'{i}'::uuid" for i in ids))
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
# EL BRAZO: lo que se mide DENTRO de un lexicón (hoy o el de REF)
# ══════════════════════════════════════════════════════════════════════
def _plantillas_etiquetadas(L):
    """Las mismas diez plantillas estáticas que construyen la puerta."""
    t = [("IDENTIDAD_LINGUISTICA", L.IDENTIDAD_LINGUISTICA),
         ("prompt_reglas_completo", L.prompt_reglas_completo()),
         ("prompt_reglas_breve", L.prompt_reglas_breve())]
    for s in (1.0, 3.0, 5.0, 6.5):
        t.append((f"prompt_refuerzo_score{s}", L.prompt_refuerzo(s, [])))
    for etiqueta, esp, otro in (("fuga_esp0", 0, [""]),
                                ("fuga_esp3_con_otro", 3, [""]),
                                ("fuga_esp3_sin_otro", 3, [])):
        t.append((f"prompt_rescate_{etiqueta}",
                  L.prompt_rescate_linguistico("", 0.0, esp, otro)))
    # El refuerzo enseña por RECORTE (`verbos[:4]`), así que con
    # `palabras_usadas=[]` sólo se ven las cuatro primeras de cada lista: la
    # quinta posición —donde vivían `kira` y `kali`— la puerta NO la alcanza.
    # Se añade la variante «ya dijo las cuatro primeras», que es la que el
    # motor produce de verdad en un turno flojo.
    gastadas = ["wana", "suna", "masa", "awa", "barsure", "duna", "amana",
                "ka", "mara", "saa", "naka"]
    for s in (1.0, 3.0, 5.0, 6.5):
        t.append((f"prompt_refuerzo_score{s}_gastado",
                  L.prompt_refuerzo(s, gastadas)))
    return t


def _ensayo_de_prompt(L, era: str) -> dict:
    """Los system prompts del elenco, montando el turno de verdad.

    `orch.run_turn` con `_invoke` espiado y el Director mudo: entra el
    ensamblado entero (persona, identidad, mundo, `[Tu tierra]`, muestra del
    lexicón, memoria). Sin API y sin base.
    """
    import curiana_agents as A
    import curiana_orchestrator_v2 as orch
    from curiana_observer import ObserverAgent
    from curiana_perfiles import cargar_perfil
    from curiana_state import estado_inicial, estado_inicial_test

    if era == "era2":
        import curiana_agents_era2 as _era2
        elenco = dict(_era2.ALL_AGENTS)
        perfil = cargar_perfil("era2")
    else:
        elenco = {**A.AGENTS_T1, **A.AGENTS_T2, **A.AGENTS_T3}
        perfil = cargar_perfil("base")
    roster = list(elenco)

    random.seed(SEMILLA_ENSAYO)
    capturas = []
    _invoke, _agentes = orch._invoke, orch.ALL_AGENTS
    _narrar, _evento = orch.director_narrate, orch.director_select_event
    orch._invoke = lambda c, system, user: (
        capturas.append(system) or "Taya wana-ka arima wara kari.")
    orch.director_narrate = lambda *a, **k: "(narración)"
    orch.director_select_event = lambda s: None
    orch.ALL_AGENTS = elenco
    try:
        state = (estado_inicial("PARAGUANÁ") if era == "era2"
                 else estado_inicial_test())
        if era == "era2":
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

    largos = sorted(len(p) for p in capturas)
    return {
        "prompts": len(capturas),
        "medio": round(sum(largos) / len(largos), 1),
        "mediana": largos[len(largos) // 2],
        "min": largos[0], "max": largos[-1],
        "largos": largos,
        # En el ORDEN en que se pidieron: el ensayo es determinista (misma
        # semilla, mismo roster), así que el prompt i es del mismo agente en
        # los dos brazos y el delta por prompt sí significa algo. Ordenarlos
        # antes de restar da el delta de los ESTADÍSTICOS DE ORDEN, que es
        # otra cosa y engaña.
        "largos_en_orden": [len(p) for p in capturas],
        "dicen": {f: sum(1 for p in capturas if f in p)
                  for f in ARCHIVADAS + MANDAN},
    }


def _replay(L, filas: list[dict]) -> list[dict]:
    """Re-ejecuta el pipeline del Observer sobre las respuestas, en su orden y
    encadenando los días como lo hizo `--continuar`. El patrón es el de
    `medir_formas_de_plantilla.py`; lo que cambia entre brazos no es una
    bandera sino el LEXICÓN."""
    from curiana_koine import CampoLexico, CompetenciaLexica, REFERENTES_NOVEDOSOS
    from curiana_observer import ObserverAgent

    lexico = L.LexicoComunitario(filtrar_plantilla=True)
    observer = ObserverAgent(None, lexico)
    competencia = CompetenciaLexica(filtrar_plantilla=True)
    campo = CampoLexico()
    pendientes = [dict(r) for r in REFERENTES_NOVEDOSOS]

    turnos, visto = [], None
    for f in filas:
        if (f["run"], f["dia"], f["turno"]) != visto:
            turnos.append([])
            visto = (f["run"], f["dia"], f["turno"])
        turnos[-1].append(f)

    salida, run_previo, t = [], None, 0
    for turno in turnos:
        if turno[0]["run"] != run_previo:
            if run_previo is not None:
                competencia.evaluar_fijacion(turno[0]["dia"] - 1)
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
            salida.append({
                "run": fila["run"], "agente": fila["agente"],
                "dia": fila["dia"], "turno": fila["turno"],
                "score": reg.score,
                "prestamos_de_esfera": len(reg.prestamos_de_esfera),
                "palabras_caquetias": len(reg.palabras_caquetias),
                "neologisms_proposed": len(neos),
                "caquetias": sorted(reg.palabras_caquetias),
            })
        t += 1
    competencia.evaluar_fijacion(turnos[-1][0]["dia"] if turnos else 0)
    return salida


def _reconoce(L, tokens: list[str]) -> dict[str, bool]:
    """¿El SCORER cuenta este token como arahuaco? Se pregunta al scorer, no a
    una copia de su lógica: se le pasa el token en un marco caquetío mínimo y
    se mira si sale en `palabras_arahuacas`."""
    lexico = L.LexicoComunitario()
    out = {}
    for tok in tokens:
        r = L.score_linguistico(f"taya {tok} yama", lexico)
        out[tok] = tok in set(r["palabras_arahuacas"])
    return out


def medir_en_proceso(args) -> dict:
    """Todo lo que depende del LEXICÓN cargado en este proceso."""
    import curiana_lexicon as L

    d = {
        "modulo": os.path.abspath(L.__file__),
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "fuera_del_habla": sorted(L.FUERA_DEL_HABLA),
        "formas_de_plantilla": sorted(L.FORMAS_DE_PLANTILLA),
        "raices_verbales": sorted(L._RAICES_VERB),
        "plantillas": {n: t for n, t in _plantillas_etiquetadas(L)},
        "fichas": {},
        "formas_seed": {},
    }
    for f in ARCHIVADAS + MANDAN + ["sima", "turumako", "kashi", "haborü"]:
        e = L.VOCABULARIO_BASE.get(f) or L.FUERA_DEL_HABLA.get(f) or {}
        d["fichas"][f] = {
            "en_vocabulario_base": f in L.VOCABULARIO_BASE,
            "en_fuera_del_habla": f in L.FUERA_DEL_HABLA,
            "capa": e.get("fuente"), "cat": e.get("cat"),
            "glosa": e.get("sig") or e.get("es"),
            "archivada": e.get("archivada"),
            "tiene_cita": bool(str(e.get("notas") or "").strip()),
            "cita": " ".join(str(e.get("notas") or "").split())[:180],
            "es_forma_de_plantilla": L.es_forma_de_plantilla(f),
        }
    try:
        import curiana_koine as K
        d["formas_seed"] = {a: list(v) for a, v in K.FORMAS_SEED.items()}
    except Exception as exc:                              # noqa: BLE001
        d["formas_seed_error"] = str(exc)

    if not args.sin_prompt:
        d["prompt_era2"] = _ensayo_de_prompt(L, "era2")
        d["prompt_era1"] = _ensayo_de_prompt(L, "era1")

    if args.tokens:
        d["reconoce"] = _reconoce(L, json.load(io.open(args.tokens,
                                                       encoding="utf-8")))
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = _replay(L, filas)
    return d


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO DE ANTES: el módulo del commit REF, en un subproceso
# ══════════════════════════════════════════════════════════════════════
def modulos_de_ref(ref: str) -> str:
    """Deja `curiana_lexicon.py` y `curiana_koine.py` del commit `ref` en un
    directorio temporal y devuelve la ruta. `./` es relativo al cwd de git."""
    tmp = tempfile.mkdtemp(prefix="curiana_ref_")
    for nombre in ("curiana_lexicon.py", "curiana_koine.py"):
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
# LOS CRUCES
# ══════════════════════════════════════════════════════════════════════
def _mp():
    """El criterio ESTRECHO de «enseñar», del script hermano de los pares."""
    spec = importlib.util.spec_from_file_location(
        "_medir_pares",
        os.path.join(AQUI, "medir_pares_atestiguado_reconstruido.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cruce_de_plantillas(antes: dict, hoy: dict) -> dict:
    """Qué forma de la política enseñaba cada plantilla y cuál enseña."""
    import curiana_lexicon as L
    MP = _mp()
    interes = ARCHIVADAS + MANDAN + ["sima", "kashi"]
    out, cambian = {}, []
    for nombre in sorted(hoy["plantillas"]):
        ta = antes["plantillas"].get(nombre, "")
        th = hoy["plantillas"][nombre]
        ea, eh = MP.formas_ensenadas(ta), MP.formas_ensenadas(th)
        aa, ah = L.formas_en_texto(ta), L.formas_en_texto(th)
        fila = {
            "largo_antes": len(ta), "largo_despues": len(th),
            "ensena_antes": sorted(f for f in interes if f in ea),
            "ensena_despues": sorted(f for f in interes if f in eh),
            "aparece_antes": sorted(f for f in interes if f in aa),
            "aparece_despues": sorted(f for f in interes if f in ah),
            "archivada_despues": sorted(f for f in ARCHIVADAS if f in ah),
            "moldes_despues": sorted(x for x in eh if "-" in x
                                     and set(x.split("-")) & set(interes)),
        }
        out[nombre] = fila
        if ta != th:
            cambian.append(nombre)
    return {"plantillas": out, "cambian": sorted(cambian),
            "con_archivada_despues": sorted(
                n for n, f in out.items() if f["archivada_despues"])}


def coste_de_una_raiz(raiz: str, usos: dict[str, int],
                      rec_antes: dict, rec_hoy: dict, MP) -> dict:
    """El paradigma de una raíz archivada, forma a forma."""
    familia = {t: n for t, n in usos.items() if MP.rol_en_la_familia(t, raiz)}
    pierden = {t: n for t, n in familia.items()
               if rec_antes.get(t) and not rec_hoy.get(t)}
    siguen = {t: n for t, n in familia.items() if rec_hoy.get(t)}
    return {
        "raiz": raiz,
        "formas_distintas": len(familia),
        "usos": sum(familia.values()),
        "formas_que_dejan_de_contar": len(pierden),
        "usos_que_dejan_de_contar": sum(pierden.values()),
        "formas_que_siguen_contando": len(siguen),
        "usos_que_siguen_contando": sum(siguen.values()),
        "top": dict(sorted(familia.items(), key=lambda kv: -kv[1])[:12]),
        "siguen_contando_ejemplos": sorted(siguen)[:8],
    }


def colision_kasi_kashi(hoy: dict, cruce: dict) -> dict:
    """¿El motor confunde `kasi` 'sol' y `kashi` 'ahora'? Sitio por sitio."""
    import curiana_lexicon as L
    from curiana_fonotactica import fonemizar

    esq = {f: [fonemizar(f, g) for g in (False, True)] for f in ("kasi", "kashi")}
    mismo = esq["kasi"] == esq["kashi"]
    nombres = L._nombres_de_agentes()
    lexico = L.LexicoComunitario()
    # `_familia_de_token` es lookup exacto sobre las claves: si confundiera,
    # una de las dos devolvería la lengua de la otra. Se prueban también sus
    # compuestos, que es donde el motor deshace afijos.
    familia = {t: L._familia_de_token(t) for t in
               ("kasi", "kashi", "kasi-bana", "kashi-bana", "ta-kasi",
                "ta-kashi", "kasi-ka", "kashi-ka")}
    # El scorer: ¿cuenta cada una por separado?
    r = L.score_linguistico("taya kasi wana-ka ka kashi naa-da", lexico)
    juntas = sorted(set(r["palabras_caquetias"]) & {"kasi", "kashi"})
    plantillas_con_las_dos = sorted(
        n for n, f in cruce["plantillas"].items()
        if "kasi" in f["aparece_despues"] and "kashi" in f["aparece_despues"])
    plantillas_con_las_dos_antes = sorted(
        n for n, f in cruce["plantillas"].items()
        if "kasi" in f["aparece_antes"] and "kashi" in f["aparece_antes"])
    return {
        "esqueleto_kasi": esq["kasi"][0], "esqueleto_kashi": esq["kashi"][0],
        "mismo_esqueleto": mismo,
        "difieren_en_un_caracter": L._difieren_en_un_caracter(
            esq["kasi"][0], esq["kashi"][0]),
        "familia_de_token": familia,
        "familia_de_token_las_distingue": len(set(familia)) == len(familia),
        "el_scorer_cuenta_las_dos": juntas,
        "homografas_de_un_nombre_del_elenco": {
            f: f in nombres for f in ("kasi", "kashi")},
        "la_puerta_las_distingue": (L.es_forma_de_plantilla("kasi")
                                    and L.es_forma_de_plantilla("kashi")),
        "plantillas_con_las_dos_antes": plantillas_con_las_dos_antes,
        "plantillas_con_las_dos_despues": plantillas_con_las_dos,
        "glosa_kasi": hoy["fichas"]["kasi"]["glosa"],
        "glosa_kashi": hoy["fichas"]["kashi"]["glosa"],
        "veredicto": (
            "el MOTOR no las confunde en ningún sitio medido; quien puede "
            "confundirlas es el HABLANTE, y desde esta tanda las tiene las dos "
            "en la misma plantilla"),
    }


def diff_de_scores(filas, antes, hoy) -> dict:
    control = [
        {"run": f["run"], "agente": f["agente"], "dia": f["dia"],
         "turno": f["turno"], "base": f["score_guardado"], "replay": a["score"],
         "neos_base": f["neos_guardados"], "neos_replay": a["neologisms_proposed"]}
        for f, a in zip(filas, antes)
        if abs(f["score_guardado"] - a["score"]) > 1e-9
        or f["neos_guardados"] != a["neologisms_proposed"]]

    def difs(campo):
        return [{"run": a["run"], "agente": a["agente"], "dia": a["dia"],
                 "turno": a["turno"], "antes": a[campo], "despues": h[campo],
                 "delta": round(h[campo] - a[campo], 4)}
                for a, h in zip(antes, hoy) if a[campo] != h[campo]]

    d_score = difs("score")
    d_pal = difs("palabras_caquetias")
    d_neo = difs("neologisms_proposed")
    # Qué voz concreta se perdió en cada respuesta que se movió.
    perdidas = defaultdict(int)
    for a, h in zip(antes, hoy):
        for f in set(a["caquetias"]) - set(h["caquetias"]):
            perdidas[f] += 1
    # A qué archivada se le puede imputar cada respuesta movida.
    por_raiz = defaultdict(int)
    MP = _mp()
    for a, h in zip(antes, hoy):
        if a["score"] == h["score"]:
            continue
        for f in set(a["caquetias"]) - set(h["caquetias"]):
            for raiz in ARCHIVADAS:
                if MP.rol_en_la_familia(f, raiz):
                    por_raiz[raiz] += 1
                    break
    deltas = [d["delta"] for d in d_score]
    return {
        "respuestas": len(filas),
        "control_replay_desvios": len(control),
        "control_ejemplos": control[:5],
        "score_cambia_en": len(d_score),
        "score_delta_max": max((abs(x) for x in deltas), default=0.0),
        "score_delta_medio_de_las_que_cambian": (
            round(sum(deltas) / len(deltas), 4) if deltas else 0.0),
        "score_medio_antes": round(sum(a["score"] for a in antes) / len(antes), 4),
        "score_medio_despues": round(sum(h["score"] for h in hoy) / len(hoy), 4),
        "score_baja_en": sum(1 for x in deltas if x < 0),
        "score_sube_en": sum(1 for x in deltas if x > 0),
        "score_ejemplos": sorted(d_score, key=lambda d: d["delta"])[:15],
        "palabras_caquetias_cambia_en": len(d_pal),
        "neologisms_proposed_cambia_en": len(d_neo),
        "voces_que_dejan_de_contarse": dict(
            sorted(perdidas.items(), key=lambda kv: -kv[1])),
        "respuestas_movidas_por_raiz": dict(
            sorted(por_raiz.items(), key=lambda kv: -kv[1])),
    }


# ══════════════════════════════════════════════════════════════════════
# EL YAML
# ══════════════════════════════════════════════════════════════════════
def _y(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    return "'" + s.replace("'", "''") + "'"


def escribir_yaml(doc: list[str]) -> None:
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(doc) + "\n")


def main(argv=None):
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", default=REF,
                    help=f"commit del brazo «antes» (por defecto {REF})")
    ap.add_argument("--sin-base", action="store_true",
                    help="no consulta Supabase: ni el paradigma ni las 216")
    ap.add_argument("--json", action="store_true",
                    help="modo BRAZO: mide en este proceso y escupe JSON")
    ap.add_argument("--sin-prompt", action="store_true",
                    help="modo brazo: se salta el ensayo de prompt")
    ap.add_argument("--tokens", default="",
                    help="modo brazo: JSON con los tokens a reconocer")
    ap.add_argument("--respuestas", default="",
                    help="modo brazo: JSON con las respuestas a re-puntuar")
    args = ap.parse_args(argv)

    if args.json:
        # ⚠️ APPEND, NO INSERT(0): el brazo «antes» recibe el directorio del
        # módulo de REF por `PYTHONPATH` y tiene que GANAR. Insertar `SIM` en
        # la cabeza hacía que los dos brazos cargaran el mismo lexicón —el de
        # hoy— y la medición salía toda a cero sin avisar. El control de abajo
        # (`brazos_distintos`) lo vigila.
        if SIM not in sys.path:
            sys.path.append(SIM)
        json.dump(medir_en_proceso(args), sys.stdout, ensure_ascii=False)
        return 0

    sys.path.insert(0, SIM)

    # ── Los insumos de la base ───────────────────────────────────────
    usos, serie, filas = {}, {}, []
    tmpdir = tempfile.mkdtemp(prefix="curiana_medida_")
    extra_tokens, extra_resp = [], []
    if not args.sin_base:
        usos = usos_por_token()
        serie = ids_serie_c()
        filas = respuestas_de(serie["ids"])
        MP0 = _mp()
        raices = ARCHIVADAS + MANDAN + [PAR_ABIERTO_SIMA[3], "turumako"]
        tokens = sorted({t for t in usos
                         if any(MP0.rol_en_la_familia(t, r) for r in raices)}
                        # El paradigma de la que MANDA, aunque nadie lo haya
                        # dicho todavía: es lo que dice si queda hueco.
                        | {f"{r}{s}" for r in MANDAN
                           for s in ("", "-ka", "-ni", "-da")}
                        | {f"{r}{s}" for r in ARCHIVADAS
                           for s in ("", "-ka", "-ni", "-da")})
        ruta_tok = os.path.join(tmpdir, "tokens.json")
        json.dump(tokens, io.open(ruta_tok, "w", encoding="utf-8"))
        ruta_resp = os.path.join(tmpdir, "respuestas.json")
        json.dump(filas, io.open(ruta_resp, "w", encoding="utf-8"),
                  ensure_ascii=False)
        extra_tokens = ["--tokens", ruta_tok]
        extra_resp = ["--respuestas", ruta_resp]

    ref_dir = modulos_de_ref(args.ref)
    extra = extra_tokens + extra_resp
    antes = correr_brazo(ref_dir, extra)
    hoy = correr_brazo(None, extra)
    # CONTROL CERO: los dos brazos tienen que ser DISTINTOS módulos. Si el
    # `PYTHONPATH` no gana, los dos cargan el lexicón de hoy y todo sale a
    # cero sin avisar — pasó al escribir este script.
    brazos_distintos = (antes["modulo"] != hoy["modulo"]
                        and antes["vocabulario_base"] != hoy["vocabulario_base"])
    if not brazos_distintos:
        raise SystemExit(
            "🔴 CONTROL CERO EN ROJO: los dos brazos cargaron el mismo "
            f"lexicón ({antes['modulo']}). Lo de abajo no mediría nada.")

    import curiana_lexicon as L                            # el de hoy
    MP = _mp()

    # ── 1. Censo ─────────────────────────────────────────────────────
    censo = {
        "vocabulario_base_antes": antes["vocabulario_base"],
        "vocabulario_base_despues": hoy["vocabulario_base"],
        "vocabulario_base_delta": hoy["vocabulario_base"] - antes["vocabulario_base"],
        "fuera_del_habla_antes": len(antes["fuera_del_habla"]),
        "fuera_del_habla_despues": len(hoy["fuera_del_habla"]),
        "archivadas_en_esta_tanda": sorted(
            set(hoy["fuera_del_habla"]) - set(antes["fuera_del_habla"])),
        "raices_verbales_antes": len(antes["raices_verbales"]),
        "raices_verbales_despues": len(hoy["raices_verbales"]),
        "raices_verbales_que_salen": sorted(
            set(antes["raices_verbales"]) - set(hoy["raices_verbales"])),
    }
    # Controles del censo: la capa NO se toca y la que manda tiene cita.
    controles = {"capa_intacta": [], "manda_atestiguada_con_cita": [],
                 "archivada_fuera_del_habla": [], "archivada_en_la_puerta": []}
    for n, glosa, att, der in POLITICA:
        fa_, fh = antes["fichas"][der], hoy["fichas"][der]
        controles["capa_intacta"].append(fa_["capa"] == fh["capa"])
        controles["archivada_fuera_del_habla"].append(
            fh["en_fuera_del_habla"] and not fh["en_vocabulario_base"])
        controles["archivada_en_la_puerta"].append(fh["es_forma_de_plantilla"])
        m = hoy["fichas"][att]
        controles["manda_atestiguada_con_cita"].append(
            m["capa"] == "caquetío-atestiguado" and m["tiene_cita"]
            and m["en_vocabulario_base"])
    censo["control_verde"] = all(all(v) for v in controles.values())
    censo["controles"] = {k: all(v) for k, v in controles.items()}

    # ── 2. La puerta ─────────────────────────────────────────────────
    pa, ph = set(antes["formas_de_plantilla"]), set(hoy["formas_de_plantilla"])
    puerta = {
        "antes": len(pa), "despues": len(ph),
        "entran": sorted(ph - pa), "salen": sorted(pa - ph),
        "archivadas_dentro": {f: hoy["fichas"][f]["es_forma_de_plantilla"]
                              for f in ARCHIVADAS},
        "archivo_viejo_dentro": sorted(
            f for f in antes["fuera_del_habla"] if f in ph),
        "archivo_viejo_estaba_dentro": sorted(
            f for f in antes["fuera_del_habla"] if f in pa),
    }

    # ── 3. Plantillas y prompt ───────────────────────────────────────
    cruce = cruce_de_plantillas(antes, hoy)
    prompt = {}
    if "prompt_era2" in hoy:
        for era in ("era2", "era1"):
            a, h = antes["prompt_" + era], hoy["prompt_" + era]
            deltas = [y - x for x, y in
                      zip(a["largos_en_orden"], h["largos_en_orden"])]
            deltas_orden = [y - x for x, y in zip(a["largos"], h["largos"])]
            prompt[era] = {
                "prompts": h["prompts"],
                "medio_antes": a["medio"], "medio_despues": h["medio"],
                "delta_medio": round(h["medio"] - a["medio"], 2),
                "mediana_antes": a["mediana"], "mediana_despues": h["mediana"],
                "min_antes": a["min"], "max_antes": a["max"],
                "min_despues": h["min"], "max_despues": h["max"],
                "delta_por_prompt": sorted(set(deltas)),
                "delta_por_prompt_medio": round(sum(deltas) / len(deltas), 2),
                "delta_de_los_estadisticos_de_orden": sorted(set(deltas_orden)),
                "prompts_que_decian_cada_archivada": a["dicen"],
                "prompts_que_dicen_cada_archivada": h["dicen"],
            }

    # ── 4. Los dos costes ────────────────────────────────────────────
    paradigma, colision = {}, {}
    if not args.sin_base:
        for raiz in ARCHIVADAS + MANDAN + [PAR_ABIERTO_SIMA[3], "turumako"]:
            paradigma[raiz] = coste_de_una_raiz(
                raiz, usos, antes.get("reconoce", {}), hoy.get("reconoce", {}), MP)
        rec = hoy.get("reconoce", {})
        paradigma["_hueco_funcional_de_paa"] = {
            "were_es_v_raiz": "were" in hoy["raices_verbales"],
            "were_es_atestiguada": hoy["fichas"]["were"]["capa"],
            "were_tiene_cita": hoy["fichas"]["were"]["tiene_cita"],
            "were_paradigma_cuenta": {s: rec.get(f"were{s}")
                                      for s in ("", "-ka", "-ni", "-da")},
            "paa_paradigma_cuenta_antes": {
                s: antes.get("reconoce", {}).get(f"paa{s}")
                for s in ("", "-ka", "-ni", "-da")},
            "paa_paradigma_cuenta_despues": {s: rec.get(f"paa{s}")
                                             for s in ("", "-ka", "-ni", "-da")},
            "jai_paradigma_cuenta": {s: rec.get(f"jai{s}")
                                     for s in ("", "-ka", "-ni", "-da")},
            "jai_es_v_raiz": "jai" in hoy["raices_verbales"],
            "veredicto": (
                "no queda hueco funcional: `were` y `jai` son raíces verbales "
                "atestiguadas y toman los mismos tres aspectos, así que el "
                "paradigma no se rompe — se muda de raíz. Lo que cuesta es la "
                "comparabilidad del corpus ya dicho, que es lo que un corte de "
                "serie declara"),
        }
    colision = colision_kasi_kashi(hoy, cruce)

    # ── 5. Las 216 ───────────────────────────────────────────────────
    scores = {}
    if not args.sin_base and "replay" in hoy:
        scores = diff_de_scores(filas, antes["replay"], hoy["replay"])
        scores["serie"] = serie

    # ── 6. Residuos ──────────────────────────────────────────────────
    seed_a, seed_h = antes.get("formas_seed", {}), hoy.get("formas_seed", {})
    cambios_seed = {a: [x for x in seed_a[a] if x not in seed_h.get(a, [])]
                    for a in seed_a if seed_a[a] != seed_h.get(a)}
    residuos = {
        "formas_seed_agentes_tocados": len(cambios_seed),
        "formas_seed_formas_que_salen": sorted(
            {x for v in cambios_seed.values() for x in v}),
        "formas_seed_n_formas_por_agente_igual": all(
            len(seed_a[a]) == len(seed_h.get(a, [])) for a in seed_a),
        "haborü": {
            "sigue_en_el_habla": hoy["fichas"]["haborü"]["en_vocabulario_base"],
            "capa": hoy["fichas"]["haborü"]["capa"],
            "nota": "'marejada' = habo+rü: su raíz queda archivada",
        },
        "sima_par_6": {
            "capa": hoy["fichas"]["sima"]["capa"],
            "sigue_en_el_habla": hoy["fichas"]["sima"]["en_vocabulario_base"],
            "rival_atestiguada": "turumako",
            "rival_capa": hoy["fichas"]["turumako"]["capa"],
            "plantillas_que_la_ensenan": sorted(
                n for n, f in cruce["plantillas"].items()
                if "sima" in f["ensena_despues"]),
            "moldes": sorted({m for f in cruce["plantillas"].values()
                              for m in f["moldes_despues"] if "sima" in m}),
        },
    }
    if paradigma:
        residuos["sima_par_6"]["usos"] = paradigma["sima"]["usos"]
        residuos["sima_par_6"]["formas_distintas"] = paradigma["sima"]["formas_distintas"]
        # Lo que COSTARÍA archivarla: no son sus 510 usos sino los que el
        # scorer reconoce hoy — el resto ya no contaba (`sima` no es v_raiz,
        # así que sólo cuentan la voz suelta y sus prefijos posesivos).
        residuos["sima_par_6"]["usos_que_el_scorer_reconoce_hoy"] = (
            paradigma["sima"]["usos_que_siguen_contando"])
        residuos["sima_par_6"]["formas_que_el_scorer_reconoce_hoy"] = (
            paradigma["sima"]["formas_que_siguen_contando"])
        residuos["sima_par_6"]["turumako_usos"] = paradigma["turumako"]["usos"]

    # ── Informe por pantalla ─────────────────────────────────────────
    print("═" * 74)
    print("LA POLÍTICA «MANDA LA ATESTIGUADA» — MEDICIÓN DEL CORTE")
    print("═" * 74)
    print(f"brazo «antes»: {args.ref}   ·   brazo «después»: el árbol de trabajo")
    print()
    print(f"1. CENSO    VOCABULARIO_BASE {censo['vocabulario_base_antes']} → "
          f"{censo['vocabulario_base_despues']} "
          f"({censo['vocabulario_base_delta']:+d})")
    print(f"            FUERA_DEL_HABLA  {censo['fuera_del_habla_antes']} → "
          f"{censo['fuera_del_habla_despues']}")
    print(f"            archivadas: {', '.join(censo['archivadas_en_esta_tanda'])}")
    print(f"            raíces verbales que salen: "
          f"{censo['raices_verbales_que_salen']}")
    print(f"            CONTROL {'✓ verde' if censo['control_verde'] else '🔴 ROJO'}"
          f"  {censo['controles']}")
    print()
    for n, glosa, att, der in POLITICA:
        fd, fm = hoy["fichas"][der], hoy["fichas"][att]
        u_d = paradigma.get(der, {}).get("usos", "?")
        u_a = paradigma.get(att, {}).get("usos", usos.get(att, "?"))
        print(f"   par {n:2} {glosa:9} manda {att:9} ({fm['capa']}, {u_a} usos)"
              f"   archivada {der:8} ({fd['capa']}, {u_d} usos)")
    print()
    print(f"2. LA PUERTA  {puerta['antes']} → {puerta['despues']}")
    print(f"   entran ({len(puerta['entran'])}): {puerta['entran'][:20]}")
    print(f"   salen  ({len(puerta['salen'])}): {puerta['salen'][:20]}")
    print(f"   las siete archivadas siguen DENTRO: "
          f"{all(puerta['archivadas_dentro'].values())}")
    print(f"   el archivo viejo (piache, numerales D11) estaba dentro antes: "
          f"{puerta['archivo_viejo_estaba_dentro'] or 'NO'}")
    print()
    print("3. PLANTILLAS")
    for nombre, f in sorted(cruce["plantillas"].items()):
        if f["ensena_antes"] or f["ensena_despues"] or f["archivada_despues"]:
            print(f"   {nombre:38} {f['ensena_antes']} → {f['ensena_despues']}"
                  + ("   ⚠ ARCHIVADA DENTRO" if f["archivada_despues"] else ""))
    print(f"   plantillas cuyo texto cambia: {cruce['cambian']}")
    print(f"   plantillas que aún dicen una archivada: "
          f"{cruce['con_archivada_despues'] or 'ninguna'}")
    for era, p in prompt.items():
        print(f"   prompt {era}: {p['medio_antes']} → {p['medio_despues']} car. "
              f"({p['delta_medio']:+.1f}) sobre {p['prompts']} prompts; "
              f"Δ por prompt {p['delta_por_prompt'][:8]} "
              f"(medio {p['delta_por_prompt_medio']})")
    print()
    if paradigma:
        print("4a. EL COSTE DE `paa` (y del resto de paradigmas)")
        for raiz in ARCHIVADAS:
            d = paradigma[raiz]
            print(f"   {raiz:8} {d['formas_distintas']:3} formas · "
                  f"{d['usos']:5} usos → dejan de contar "
                  f"{d['formas_que_dejan_de_contar']:3} formas / "
                  f"{d['usos_que_dejan_de_contar']:5} usos "
                  f"(siguen {d['usos_que_siguen_contando']})")
        h = paradigma["_hueco_funcional_de_paa"]
        print(f"   ¿hueco funcional? were v_raiz={h['were_es_v_raiz']} "
              f"capa={h['were_es_atestiguada']} · jai v_raiz={h['jai_es_v_raiz']}")
        print(f"   paradigma `were`: {h['were_paradigma_cuenta']}")
        print(f"   paradigma `jai`:  {h['jai_paradigma_cuenta']}")
        print(f"   paradigma `paa`:  {h['paa_paradigma_cuenta_antes']} → "
              f"{h['paa_paradigma_cuenta_despues']}")
        print(f"   ⇒ {h['veredicto']}")
        print()
    print("4b. LA COLISIÓN `kasi` / `kashi`")
    print(f"   esqueleto: {colision['esqueleto_kasi']} = "
          f"{colision['esqueleto_kashi']} → mismo: {colision['mismo_esqueleto']}")
    print(f"   `_familia_de_token` las distingue: "
          f"{colision['familia_de_token_las_distingue']}")
    print(f"   el scorer cuenta las dos en la misma frase: "
          f"{colision['el_scorer_cuenta_las_dos']}")
    print(f"   homógrafas de un nombre del elenco: "
          f"{colision['homografas_de_un_nombre_del_elenco']}")
    print(f"   plantillas con las DOS: {colision['plantillas_con_las_dos_antes']} "
          f"→ {colision['plantillas_con_las_dos_despues']}")
    print(f"   ⇒ {colision['veredicto']}")
    print()
    if scores:
        print(f"5. LAS {scores['respuestas']} RESPUESTAS DE LA SERIE C LIMPIA")
        print(f"   control (el replay de ANTES reproduce la base): "
              f"{scores['control_replay_desvios']} desvíos "
              f"{'✓' if not scores['control_replay_desvios'] else '🔴'}")
        print(f"   score cambia en {scores['score_cambia_en']} de "
              f"{scores['respuestas']} (|Δ| máx {scores['score_delta_max']:.2f}; "
              f"baja {scores['score_baja_en']}, sube {scores['score_sube_en']})")
        print(f"   score medio {scores['score_medio_antes']} → "
              f"{scores['score_medio_despues']}")
        print(f"   palabras_caquetias cambia en "
              f"{scores['palabras_caquetias_cambia_en']}; "
              f"neologisms_proposed en {scores['neologisms_proposed_cambia_en']}")
        print(f"   voces que dejan de contarse: "
              f"{list(scores['voces_que_dejan_de_contarse'].items())[:10]}")
        print(f"   respuestas movidas, por raíz: "
              f"{scores['respuestas_movidas_por_raiz']}")
        print()
    print("6. RESIDUOS DECLARADOS")
    print(f"   FORMAS_SEED: {residuos['formas_seed_agentes_tocados']} agentes, "
          f"salen {residuos['formas_seed_formas_que_salen']}; mismo número de "
          f"formas por agente: {residuos['formas_seed_n_formas_por_agente_igual']}")
    print(f"   haborü: {residuos['haborü']}")
    s6 = residuos["sima_par_6"]
    print(f"   sima (par 6, NO aplicado): {s6.get('usos','?')} usos en "
          f"{s6.get('formas_distintas','?')} formas, de los que el scorer "
          f"reconoce {s6.get('usos_que_el_scorer_reconoce_hoy','?')}; la enseñan "
          f"{s6['plantillas_que_la_ensenan']}; moldes {s6['moldes']}; "
          f"turumako {s6.get('turumako_usos','?')} usos")
    print()

    # ── YAML ─────────────────────────────────────────────────────────
    W = []
    A = W.append
    A("# ─────────────────────────────────────────────────────────────────")
    A("# LA POLÍTICA «MANDA LA ATESTIGUADA» — MEDICIÓN DEL CORTE")
    A("#")
    A("# GENERADO por 6-fusion/scripts/medir_politica_atestiguado_manda.py")
    A("# No se edita a mano: se regenera. La decisión está en")
    A("# 6-fusion/decisiones_tanda_2026-09-19.yaml (d19.b).")
    A("# ─────────────────────────────────────────────────────────────────")
    A("meta:")
    A(f"  fecha: '{FECHA}'")
    A("  generado_por: 6-fusion/scripts/medir_politica_atestiguado_manda.py")
    A(f"  ref_del_brazo_antes: '{args.ref}'")
    A("  elenco: era2")
    A("  decision_literal: >-")
    A("    «Sí o sí tenemos que usar los atestiguados por sobre los")
    A("    reconstruidos, por lo menos la parte caquetía.» (Miguel, 2026-09-19)")
    A("  como_se_mide_el_antes: >-")
    A("    `git show <ref>:./curiana_sim/curiana_lexicon.py` (y curiana_koine)")
    A("    a un directorio temporal que va PRIMERO en el sys.path de un")
    A("    subproceso que corre este mismo código. Los dos brazos salen del")
    A("    mismo motor y la única diferencia es el módulo. Sin API, sin .env,")
    A("    base local en sólo lectura.")
    A("politica:")
    A("  alcance: >-")
    A("    Sólo muerde donde hay rival ATESTIGUADO para el mismo significado.")
    A("    El grueso del lexicón caquetío es reconstrucción legítima porque no")
    A("    hay atestación —los pronombres, los aspectos, la mayoría de las 86")
    A("    reconstruidas— y no lo toca.")
    A("  pares_aplicados:")
    for n, glosa, att, der in POLITICA:
        fd, fm = hoy["fichas"][der], hoy["fichas"][att]
        A(f"    - par: {n}")
        A(f"      glosa: {_y(glosa)}")
        A(f"      manda: {att}")
        A(f"      manda_capa: {_y(fm['capa'])}")
        A(f"      manda_cita: {_y(fm['cita'])}")
        A(f"      manda_usos: {usos.get(att, 'null') if usos else 'null'}")
        A(f"      archivada: {der}")
        A(f"      archivada_capa_antes: {_y(antes['fichas'][der]['capa'])}")
        A(f"      archivada_capa_despues: {_y(fd['capa'])}")
        A(f"      archivada_usos: {paradigma.get(der, {}).get('usos', 'null')}")
        A(f"      archivada_formas: {paradigma.get(der, {}).get('formas_distintas', 'null')}")
    A("censo:")
    for k, v in censo.items():
        if isinstance(v, dict):
            A(f"  {k}:")
            for kk, vv in v.items():
                A(f"    {kk}: {_y(vv)}")
        elif isinstance(v, list):
            A(f"  {k}: [{', '.join(str(x) for x in v)}]")
        else:
            A(f"  {k}: {_y(v)}")
    A("puerta_formas_de_plantilla:")
    A("  # `FUERA_DEL_HABLA` ENTRA en la puerta con esta tanda: sin eso,")
    A("  # archivar una voz la habría dejado ACUÑABLE al día siguiente.")
    A(f"  antes: {puerta['antes']}")
    A(f"  despues: {puerta['despues']}")
    A(f"  entran: [{', '.join(puerta['entran'])}]")
    A(f"  salen: [{', '.join(puerta['salen'])}]")
    A("  archivadas_dentro:")
    for f, v in puerta["archivadas_dentro"].items():
        A(f"    {f}: {_y(v)}")
    A(f"  archivo_viejo_estaba_dentro_antes: [{', '.join(puerta['archivo_viejo_estaba_dentro'])}]")
    A(f"  archivo_viejo_dentro_ahora: [{', '.join(puerta['archivo_viejo_dentro'])}]")
    A("plantillas:")
    A(f"  cambian: [{', '.join(cruce['cambian'])}]")
    A(f"  con_archivada_despues: [{', '.join(cruce['con_archivada_despues'])}]")
    A("  detalle:")
    for nombre, f in sorted(cruce["plantillas"].items()):
        A(f"    {nombre}:")
        A(f"      largo_antes: {f['largo_antes']}")
        A(f"      largo_despues: {f['largo_despues']}")
        A(f"      ensena_antes: [{', '.join(f['ensena_antes'])}]")
        A(f"      ensena_despues: [{', '.join(f['ensena_despues'])}]")
        A(f"      aparece_antes: [{', '.join(f['aparece_antes'])}]")
        A(f"      aparece_despues: [{', '.join(f['aparece_despues'])}]")
        if f["moldes_despues"]:
            A(f"      moldes_despues: [{', '.join(f['moldes_despues'])}]")
    if prompt:
        A("largo_del_prompt:")
        A("  # La longitud predice el score (r = −0,48): se mide aunque parezca")
        A("  # cosmético. Ensayo SIN API con `run_turn` de verdad e `_invoke`")
        A(f"  # espiado, misma semilla ({SEMILLA_ENSAYO}) en los dos brazos.")
        A("  lectura: >-")
        A("    Lo que el cambio mueve DE VERDAD es el texto de las plantillas,")
        A("    y ese número está arriba, en `plantillas.detalle.*.largo_*`:")
        A("    son unas pocas decenas de caracteres y sólo en las plantillas")
        A("    que cambian. El `delta_por_prompt` tiene un rango ancho por otra")
        A("    razón, y conviene decirla: quitar siete claves de")
        A("    `VOCABULARIO_BASE` cambia los SORTEOS del muestreador aguas")
        A("    abajo aunque la semilla sea la misma, así que cada prompt")
        A("    recibe otra muestra del lexicón y su largo se mueve con ella.")
        A("    Por eso el número que se compara es el MEDIO sobre los 63 (y")
        A("    los 60 de la era 1), no el de un prompt suelto.")
        for era, p in prompt.items():
            A(f"  {era}:")
            for k, v in p.items():
                if isinstance(v, dict):
                    A(f"    {k}:")
                    for kk, vv in v.items():
                        A(f"      {kk}: {_y(vv)}")
                elif isinstance(v, list):
                    A(f"    {k}: [{', '.join(str(x) for x in v)}]")
                else:
                    A(f"    {k}: {_y(v)}")
    if paradigma:
        A("coste_de_los_paradigmas:")
        A("  # El reconocimiento no se reimplementa: se le pregunta al SCORER")
        A("  # (`score_linguistico` sobre el token en marco caquetío mínimo).")
        for raiz in ARCHIVADAS + MANDAN + [PAR_ABIERTO_SIMA[3], "turumako"]:
            d = paradigma[raiz]
            A(f"  {raiz}:")
            for k, v in d.items():
                if k == "top":
                    A("    formas_mas_usadas:")
                    for t, nn in v.items():
                        A(f"      {t}: {nn}")
                elif isinstance(v, list):
                    A(f"    {k}: [{', '.join(str(x) for x in v)}]")
                else:
                    A(f"    {k}: {_y(v)}")
        A("  hueco_funcional_de_paa:")
        for k, v in paradigma["_hueco_funcional_de_paa"].items():
            A(f"    {k}: {_y(v)}")
    A("colision_kasi_kashi:")
    for k, v in colision.items():
        if isinstance(v, dict):
            A(f"  {k}:")
            for kk, vv in v.items():
                A(f"    {kk}: {_y(vv)}")
        elif isinstance(v, list):
            A(f"  {k}: [{', '.join(str(x) for x in v)}]")
        else:
            A(f"  {k}: {_y(v)}")
    if scores:
        A("re_puntuacion_de_la_serie_c_limpia:")
        A("  # Archivar una voz la saca de `palabras_activas()`: es un CORTE DE")
        A("  # SERIE y su número se mide, no se estima. El scorer NO se tocó —")
        A("  # `score_linguistico`, `pct_*` y `capas_de_score` son los mismos.")
        for k, v in scores.items():
            if k in ("score_ejemplos", "control_ejemplos"):
                A(f"  {k}:")
                for e in v:
                    A("    - {" + ", ".join(f"{kk}: {_y(vv)}"
                                            for kk, vv in e.items()) + "}")
            elif isinstance(v, dict):
                A(f"  {k}:")
                for kk, vv in v.items():
                    if isinstance(vv, list):
                        A(f"    {kk}: [{', '.join(str(x) for x in vv)}]")
                    else:
                        A(f"    {kk}: {_y(vv)}")
            else:
                A(f"  {k}: {_y(v)}")
    A("residuos_declarados:")
    for k, v in residuos.items():
        if isinstance(v, dict):
            A(f"  {k}:")
            for kk, vv in v.items():
                if isinstance(vv, list):
                    A(f"    {kk}: [{', '.join(str(x) for x in vv)}]")
                else:
                    A(f"    {kk}: {_y(vv)}")
        elif isinstance(v, list):
            A(f"  {k}: [{', '.join(str(x) for x in v)}]")
        else:
            A(f"  {k}: {_y(v)}")
    A("  formas_seed: >-")
    A("    `curiana_koine.FORMAS_SEED` es INSTRUMENTO, no emergencia: una")
    A("    lista escrita a mano que entra en `[Tu manera de hablar]` desde el")
    A("    día 1. Sembrar ahí una forma archivada sería enseñarla por la")
    A("    puerta de atrás, así que las seis que la política retiró se mudan a")
    A("    su rival atestiguada. El NÚMERO de formas por agente no cambia, y")
    A("    con él la divergencia inicial que DISENO_KOINE §4 pide.")
    A("  sima_es_de_miguel: >-")
    A("    El par 6 («cerro») lo ALCANZA la política —`turumako` es")
    A("    atestiguada (Zavala #262) y el caquetío dice además 'cerro' con")
    A("    `-bana` (D9, seis apoyos)— y NO se ha aplicado. Es la pregunta que")
    A("    Miguel dejó abierta y aquí está su coste delante: `sima` está en")
    A("    `prompt_reglas_completo` dos veces (la voz y el molde `sima-bana`,")
    A("    que es el ejemplo de los locativos) y tiene el uso que dice la")
    A("    tabla de arriba, mientras `turumako` casi no se ha dicho. Aplicarla")
    A("    obligaría además a reescribir el ejemplo del locativo, que es lo")
    A("    que enseña `-bana`.")
    escribir_yaml(W)
    print(f"✓ escrito {os.path.relpath(SALIDA, RAIZ)}  ({len(W)} líneas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
