#!/usr/bin/env python3
"""LA CLASE DE LA RAÍZ, medida: qué cuesta declararla.

Hallazgo del 2026-09-20. En `curiana_sim/minar_zavala_glosario.py` la parte de
la oración de todo el vocabulario activo salía de UNA línea:

    _CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS

El tier T4 es el CAJÓN DE RESTO del minador —lo que el regex `re_concreto` no
reconoció como cosa—, así que de él salían **49** entradas con `cat: v_raiz`.
Y de `cat: v_raiz` sale `curiana_lexicon._RAICES_VERB`, que hace que
`score_linguistico()` cuente como arahuaco **cualquier token cuyo primer
segmento sea una raíz verbal** y que `_familia_de_token()` le dé lengua propia.

PERO no es que «40 no sean verbos» (corrección de Miguel el mismo día): en
arahuaco mucho de lo que el castellano llama adjetivo es un VERBO ESTATIVO, y
el repo lo tiene documentado (2-lengua/morfologia.md §2, sobre Perea y Alonso
1942: el lokono tiene dos juegos de pronombre sujeto, prefijado en transitivos
y **pospuesto en estativos**). Así que las 49 se reparten en tres clases y
media —estativo, acción, nombre, adverbio— y sólo las dos últimas cambian de
`cat`. El reparto vive declarado, fila a fila y con su cita, en
`CLASE_DE_LA_RAIZ` (minador) y sale al módulo generado como
`CLASES_DE_RAIZ_ZAVALA`.

Este script MIDE el corte. No decide nada:

  1. EL CENSO. `_RAICES_VERB` antes y después, cuáles salen y con qué clase.
     `VOCABULARIO_BASE` no se mueve: no se archiva ni se añade nada.

  2. EL PARADIGMA EN LA BASE. Sobre las 49 raíces, cuántas formas
     raíz+aspecto hay y cuántos usos, y cuáles **dejan de contar** como
     arahuacas al re-puntuar. Se le pregunta AL SCORER, no a una copia de su
     lógica.

  3. LA RE-PUNTUACIÓN DE LOS DOS BRAZOS. La serie C limpia y su control se
     re-ejecutan enteros por el pipeline del Observer, dos veces —con el
     `lexicon_zavala.py` de REF y con el de hoy— y se comparan respuesta a
     respuesta. CONTROL: el brazo «antes» tiene que reproducir el `score` y el
     `neologisms_proposed` que la base guardó. Si el control está en rojo, lo
     demás no mide nada.

  4. `juri` Y LOS NOMBRES: cuánto pesa hoy la vía mala (nombre + aspecto)
     contra la vía arahuaca (`ka-` atributivo/existencial de van Buurt 2014
     §8, `ma-` privativo). Es el insumo de la propuesta, que NO se aplica.

  5. LA DERIVA DEL GENERADO: seis entradas atestiguadas que la regeneración
     borraba en silencio por homografía con la comparanda achagua y lokono.

    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \
        python 6-fusion/scripts/medir_clases_de_raiz.py
    python 6-fusion/scripts/medir_clases_de_raiz.py --sin-base

CÓMO SE MIDE EL «ANTES», sin cifras a mano: se saca `lexicon_zavala.py` del
commit REF con `git show`, se deja en un directorio temporal que va PRIMERO en
el `sys.path` de un subproceso, y ese subproceso corre exactamente el mismo
código de medición. Los dos brazos salen del mismo motor y lo único que
cambia es el módulo GENERADO — `curiana_lexicon.py` no se toca en esta tanda.

REGLAS DURAS que respeta: no abre `curiana_sim/.env` (stub de `dotenv` antes
de importar el motor), no llama a la API, no escribe en la base (la lee por
`docker exec … psql`) y no toca el canon ni `curiana_observer`.
"""
from __future__ import annotations

import argparse
import io
import json
import os
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

FECHA = "2026-09-20"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_clases_de_raiz_{FECHA}.yaml")
CONTENEDOR = "supabase_db_curiana_sim"

# El commit ANTES de declarar la clase: el merge de «la raíz de ninguna
# parte», que es el corte inmediatamente anterior.
REF = "1efcb24"

# ⚠️ EL CONTROL NO PUEDE SER CONTRA `REF`, y hay que decir por qué. Los seis
# runs de abajo se corrieron el 2026-09-20 a las 01:09-02:04 (−0300) y el fix
# de la raíz de ninguna parte se mergeó a las 03:12: la base guardó sus
# `score` con el motor de ANTES de ese corte. Un replay a `REF` se desvía de
# la base en exactamente las 8 (con escena) y 43 (control) respuestas que el
# punto 11 de la bitácora ya declaró — no es un fallo, es el corte anterior.
#
# Así que el control verde se hace contra `REF_BASE`, el último merge ANTERIOR
# al fix, con `curiana_lexicon.py` Y `lexicon_zavala.py` del mismo commit: ese
# brazo tiene que reproducir la base en 216 de 216. Y la diferencia
# REF_BASE → REF tiene que ser exactamente el corte ya declarado.
REF_BASE = "b8c85ca"
DESVIOS_DECLARADOS_PUNTO_11 = {"con_escena": 8, "control": 43}

# Los dos brazos de la serie C, declarados. Cada uno es una cadena de tres
# días encadenados por `continuado_desde`; el script lo COMPRUEBA.
BRAZOS = {
    "con_escena": ("f2741e89", "fcdfa07a", "0313d830"),
    "control":    ("0345840d", "45618069", "e98227eb"),
}
CADENCIA_NOMBRAMIENTO = 4          # curiana_orchestrator_v2.auto_mode
SEPARADOR = "\x1f"
FIN_DE_FILA = "\x1e"
ASPECTOS = ("-ka", "-ni", "-da")


def _forzar_utf8():
    if sys.platform.startswith("win"):
        for nombre in ("stdout", "stderr"):
            try:
                getattr(sys, nombre).reconfigure(encoding="utf-8")
            except Exception:                             # noqa: BLE001
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


def ids_de(id8: tuple) -> dict:
    filas = psql(
        "select id::text, substring(id::text,1,8), "
        "coalesce(config->>'continuado_desde',''), coalesce(config->>'serie','') "
        "from simulation_runs where substring(id::text,1,8) in ("
        + ", ".join(f"'{i}'" for i in id8) + ");")
    por8 = {i: (rid, desde, serie) for rid, i, desde, serie in filas}
    faltan = [i for i in id8 if i not in por8]
    if faltan:
        raise RuntimeError(f"runs declarados que no están en la base: {faltan}")
    ids = [por8[i][0] for i in id8]
    cadena = (por8[id8[0]][1] == "" and por8[id8[1]][1] == ids[0]
              and por8[id8[2]][1] == ids[1])
    dias, turnos = psql(
        "select count(distinct day), count(*) from turns where run_id in ("
        + ", ".join(f"'{i}'::uuid" for i in ids) + ");")[0]
    return {"ids": ids, "id8": list(id8), "cadena_ok": cadena,
            "serie": por8[id8[0]][2], "dias": int(dias), "turnos": int(turnos)}


def respuestas_de(ids: list[str]) -> list[dict]:
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


def predicacion_ka_ma(raices: list[str]) -> dict:
    """La vía arahuaca (`ka-`/`ma-`) contra la vía del aspecto, en la base."""
    def cuenta(patron: str) -> tuple[int, int]:
        f, u = psql("select count(distinct word), count(*) from word_uses "
                    f"where word like '{patron}';")[0]
        return int(f), int(u)
    ka_f, ka_u = cuenta("ka-%")
    ma_f, ma_u = cuenta("ma-%")
    top_ka = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where word like 'ka-%' "
        "group by 1 order by 2 desc limit 12;")}
    top_ma = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where word like 'ma-%' "
        "group by 1 order by 2 desc limit 12;")}
    en_lista = ", ".join(f"'{r}'" for r in raices)
    via_aspecto = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where word in ("
        + ", ".join(f"'{r}{s}'" for r in raices for s in ASPECTOS)
        + ") group by 1 order by 2 desc;")}
    via_ka = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where word in ("
        + ", ".join(f"'ka-{r}'" for r in raices)
        + ") group by 1 order by 2 desc;")}
    via_ma = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where word in ("
        + ", ".join(f"'ma-{r}'" for r in raices)
        + ") group by 1 order by 2 desc;")}
    fam = {w: int(n) for w, n in psql(
        "select word, count(*) from word_uses where " + " or ".join(
            f"word like '{r}-%'" for r in raices) + " group by 1;")}
    return {
        "ka_prefijo_formas": ka_f, "ka_prefijo_usos": ka_u, "ka_top": top_ka,
        "ma_prefijo_formas": ma_f, "ma_prefijo_usos": ma_u, "ma_top": top_ma,
        "nombres_en_juego": raices,
        "via_aspecto_formas": len(via_aspecto),
        "via_aspecto_usos": sum(via_aspecto.values()),
        "via_aspecto_detalle": via_aspecto,
        "via_ka_formas": len(via_ka), "via_ka_usos": sum(via_ka.values()),
        "via_ka_detalle": via_ka,
        "via_ma_formas": len(via_ma), "via_ma_usos": sum(via_ma.values()),
        "via_ma_detalle": via_ma,
        "familia_entera_formas": len(fam),
        "familia_entera_usos": sum(fam.values()),
        "_sql_en_lista": en_lista[:0],   # se deja la forma, no el volcado
    }


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO: lo que se mide DENTRO de un lexicón (hoy o el de REF)
# ══════════════════════════════════════════════════════════════════════
def _replay(L, filas: list[dict]) -> list[dict]:
    """Re-ejecuta el pipeline del Observer sobre las respuestas, en su orden y
    encadenando los días como lo hizo `--continuar`. Patrón de
    `medir_politica_atestiguado_manda.py::_replay`; lo que cambia entre brazos
    no es una bandera sino el módulo GENERADO que el lexicón importa."""
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
                "palabras_caquetias": len(reg.palabras_caquetias),
                "neologisms_proposed": len(neos),
                "caquetias": sorted(reg.palabras_caquetias),
            })
        t += 1
    competencia.evaluar_fijacion(turnos[-1][0]["dia"] if turnos else 0)
    return salida


def _reconoce(L, tokens: list[str]) -> dict[str, bool]:
    """¿El SCORER cuenta este token como arahuaco? Se le pregunta a él, en un
    marco caquetío mínimo, no a una copia de su lógica."""
    lexico = L.LexicoComunitario()
    out = {}
    for tok in tokens:
        r = L.score_linguistico(f"taya {tok} yama", lexico)
        out[tok] = tok in set(r["palabras_arahuacas"])
    return out


def _familias(L, tokens: list[str]) -> dict[str, str]:
    return {t: L._familia_de_token(t) for t in tokens}


def medir_en_proceso(args) -> dict:
    import curiana_lexicon as L
    import lexicon_zavala as Z

    glos = Z.GLOSARIO_ZAVALA
    d = {
        "modulo_lexicon": os.path.abspath(L.__file__),
        "modulo_zavala": os.path.abspath(Z.__file__),
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "raices_verbales": sorted(L._RAICES_VERB),
        "zavala_entradas": len(glos),
        "zavala_v_raiz": sorted(k for k, v in glos.items()
                                if v.get("cat") == "v_raiz"),
        "zavala_cats": {k: v.get("cat") for k, v in glos.items()},
        "clases": {k: v["clase"] for k, v in
                   getattr(Z, "CLASES_DE_RAIZ_ZAVALA", {}).items()},
        "reparto": dict(getattr(Z, "REPARTO_DE_CLASES", {})),
        "sin_clase_declarada": list(getattr(Z, "SIN_CLASE_DECLARADA", [])),
        "afijos": sorted(Z.AFIJOS_ZAVALA),
        "toponimos": len(Z.TOPONIMOS_ZAVALA),
        "antroponimos": len(Z.ANTROPONIMOS_ZAVALA),
        # Las glosas verbatim, para el control de que NO se tocaron.
        "glosa_fuente": {k: v.get("glosa_fuente") for k, v in glos.items()},
        "sig": {k: v.get("sig") for k, v in glos.items()},
        "fuente": {k: v.get("fuente") for k, v in glos.items()},
        "notas": {k: v.get("notas") for k, v in glos.items()},
    }
    if args.tokens:
        toks = json.load(io.open(args.tokens, encoding="utf-8"))
        d["reconoce"] = _reconoce(L, toks)
        d["familia"] = _familias(L, toks)
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = _replay(L, filas)
    return d


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO DE ANTES: el módulo GENERADO del commit REF, en un subproceso
# ══════════════════════════════════════════════════════════════════════
def modulo_de_ref(ref: str, nombres=("lexicon_zavala.py",)) -> str:
    tmp = tempfile.mkdtemp(prefix="curiana_ref_zavala_")
    for nombre in nombres:
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


def correr_brazo(zavala_dir: str | None, extra: list[str]) -> dict:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["CURIANA_ELENCO"] = "era2"
    rutas = ([zavala_dir] if zavala_dir else []) + [SIM]
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
    perdidas: dict = defaultdict(int)
    for a, h in zip(antes, hoy):
        for f in set(a["caquetias"]) - set(h["caquetias"]):
            perdidas[f] += 1
    ganadas: dict = defaultdict(int)
    for a, h in zip(antes, hoy):
        for f in set(h["caquetias"]) - set(a["caquetias"]):
            ganadas[f] += 1
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
        "palabras_caquetias_cambia_en": len(difs("palabras_caquetias")),
        "neologisms_proposed_cambia_en": len(difs("neologisms_proposed")),
        "voces_que_dejan_de_contarse": dict(
            sorted(perdidas.items(), key=lambda kv: -kv[1])),
        "voces_que_empiezan_a_contarse": dict(
            sorted(ganadas.items(), key=lambda kv: -kv[1])),
    }


def paradigma_de(raices: dict, usos: dict, rec_a: dict, rec_h: dict,
                 fam_a: dict, fam_h: dict) -> dict:
    """Forma a forma, qué deja de contar y qué cambia de lengua."""
    out = {}
    for raiz, clase in sorted(raices.items()):
        familia = {t: n for t, n in usos.items()
                   if t == raiz or t.startswith(raiz + "-")}
        pierden = {t: n for t, n in familia.items()
                   if rec_a.get(t) and not rec_h.get(t)}
        cambian_lengua = {t: (fam_a.get(t), fam_h.get(t)) for t in familia
                          if fam_a.get(t) != fam_h.get(t)}
        aspecto = {f"{raiz}{s}": usos.get(f"{raiz}{s}", 0) for s in ASPECTOS}
        out[raiz] = {
            "clase": clase,
            "formas": len(familia), "usos": sum(familia.values()),
            "formas_aspecto": sum(1 for v in aspecto.values() if v),
            "usos_aspecto": sum(aspecto.values()),
            "formas_que_dejan_de_contar": len(pierden),
            "usos_que_dejan_de_contar": sum(pierden.values()),
            "formas_que_cambian_de_lengua": len(cambian_lengua),
            "top": dict(sorted(familia.items(), key=lambda kv: -kv[1])[:8]),
        }
    return out


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
    return "'" + str(v).replace("'", "''") + "'"


def _bloque(W, nombre: str, datos: dict, sangria: str = "  "):
    W.append(f"{nombre}:")
    for k, v in datos.items():
        if isinstance(v, dict):
            W.append(f"{sangria}{k}:")
            for k2, v2 in v.items():
                if isinstance(v2, (dict, list)):
                    W.append(f"{sangria}  {_y(k2)}: {json.dumps(v2, ensure_ascii=False)}")
                else:
                    W.append(f"{sangria}  {_y(k2)}: {_y(v2)}")
        elif isinstance(v, list):
            W.append(f"{sangria}{k}: {json.dumps(v, ensure_ascii=False)}")
        else:
            W.append(f"{sangria}{k}: {_y(v)}")


def main(argv=None):
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ref", default=REF)
    ap.add_argument("--ref-base", default=REF_BASE,
                    help="commit del CONTROL: el motor con el que se corrieron "
                         f"los runs (por defecto {REF_BASE})")
    ap.add_argument("--sin-base", action="store_true")
    ap.add_argument("--json", action="store_true",
                    help="modo BRAZO: mide en este proceso y escupe JSON")
    ap.add_argument("--tokens", default="")
    ap.add_argument("--respuestas", default="")
    args = ap.parse_args(argv)

    if args.json:
        # APPEND, no insert(0): el brazo «antes» recibe el directorio del
        # módulo de REF por PYTHONPATH y tiene que GANAR.
        if SIM not in sys.path:
            sys.path.append(SIM)
        json.dump(medir_en_proceso(args), sys.stdout, ensure_ascii=False)
        return 0

    sys.path.insert(0, SIM)

    tmpdir = tempfile.mkdtemp(prefix="curiana_medida_clases_")
    usos: dict = {}
    series: dict = {}
    filas_por_brazo: dict = {}
    extra: list[str] = []

    # Las 49 y su clase salen del MÓDULO, no de una lista a mano.
    import lexicon_zavala as Z
    clases = {k: v["clase"] for k, v in Z.CLASES_DE_RAIZ_ZAVALA.items()}
    nombres = sorted(k for k, c in clases.items() if c in ("nombre", "adverbio"))

    if not args.sin_base:
        usos = usos_por_token()
        tokens = sorted({t for t in usos
                         if any(t == r or t.startswith(r + "-") for r in clases)}
                        | {f"{r}{s}" for r in clases for s in ("",) + ASPECTOS}
                        | {f"ka-{r}" for r in nombres}
                        | {f"ma-{r}" for r in nombres})
        ruta_tok = os.path.join(tmpdir, "tokens.json")
        json.dump(tokens, io.open(ruta_tok, "w", encoding="utf-8"))
        extra += ["--tokens", ruta_tok]
        for brazo, id8 in BRAZOS.items():
            series[brazo] = ids_de(id8)
            filas_por_brazo[brazo] = respuestas_de(series[brazo]["ids"])

    ref_dir = modulo_de_ref(args.ref)
    # El brazo del CONTROL lleva el motor entero del commit con el que se
    # corrieron los runs, no sólo el módulo generado.
    base_dir = modulo_de_ref(args.ref_base,
                             ("curiana_lexicon.py", "curiana_koine.py",
                              "curiana_observer.py", "lexicon_zavala.py"))

    resultados = {}
    for brazo in (list(BRAZOS) if not args.sin_base else ["_sin_base"]):
        e = list(extra)
        con_replay = brazo in filas_por_brazo
        if con_replay:
            ruta = os.path.join(tmpdir, f"resp_{brazo}.json")
            json.dump(filas_por_brazo[brazo], io.open(ruta, "w", encoding="utf-8"),
                      ensure_ascii=False)
            e += ["--respuestas", ruta]
        resultados[brazo] = {"antes": correr_brazo(ref_dir, e),
                             "hoy": correr_brazo(None, e)}
        if con_replay:
            resultados[brazo]["base_ref"] = correr_brazo(base_dir, e)

    primero = next(iter(resultados.values()))
    antes, hoy = primero["antes"], primero["hoy"]

    # ── CONTROL CERO: los dos brazos tienen que ser módulos DISTINTOS ──
    distintos = (antes["modulo_zavala"] != hoy["modulo_zavala"]
                 and antes["zavala_v_raiz"] != hoy["zavala_v_raiz"])
    if not distintos:
        raise SystemExit(
            "🔴 CONTROL CERO EN ROJO: los dos brazos cargaron el mismo "
            f"lexicon_zavala ({antes['modulo_zavala']}).")

    # ── 1. Censo ─────────────────────────────────────────────────────
    ra, rh = set(antes["raices_verbales"]), set(hoy["raices_verbales"])
    cambian_cat = sorted(k for k in hoy["zavala_cats"]
                         if antes["zavala_cats"].get(k) != hoy["zavala_cats"][k])
    censo = {
        "zavala_entradas_antes": antes["zavala_entradas"],
        "zavala_entradas_despues": hoy["zavala_entradas"],
        "zavala_claves_iguales": (sorted(antes["zavala_cats"])
                                  == sorted(hoy["zavala_cats"])),
        "zavala_v_raiz_antes": len(antes["zavala_v_raiz"]),
        "zavala_v_raiz_despues": len(hoy["zavala_v_raiz"]),
        "entradas_que_cambian_de_cat": len(cambian_cat),
        "transiciones": {k: f"{antes['zavala_cats'][k]} → {hoy['zavala_cats'][k]}"
                         for k in cambian_cat},
        "vocabulario_base_antes": antes["vocabulario_base"],
        "vocabulario_base_despues": hoy["vocabulario_base"],
        "raices_verbales_antes": len(ra), "raices_verbales_despues": len(rh),
        "raices_verbales_que_salen": sorted(ra - rh),
        "raices_verbales_que_entran": sorted(rh - ra),
        "afijos_iguales": antes["afijos"] == hoy["afijos"],
        "toponimos_iguales": antes["toponimos"] == hoy["toponimos"],
        "antroponimos_iguales": antes["antroponimos"] == hoy["antroponimos"],
        "reparto": hoy["reparto"],
        "sin_clase_declarada": hoy["sin_clase_declarada"],
    }
    # CONTROL DURO: la glosa verbatim de la fuente NO se toca jamás, ni `sig`,
    # ni la capa, ni las notas. Lo único que se mueve es `cat`.
    censo["glosa_fuente_intacta"] = antes["glosa_fuente"] == hoy["glosa_fuente"]
    censo["sig_intacto"] = antes["sig"] == hoy["sig"]
    censo["fuente_intacta"] = antes["fuente"] == hoy["fuente"]
    censo["notas_intactas"] = antes["notas"] == hoy["notas"]
    censo["control_verde"] = all([
        censo["zavala_claves_iguales"], censo["glosa_fuente_intacta"],
        censo["sig_intacto"], censo["fuente_intacta"], censo["notas_intactas"],
        censo["afijos_iguales"], censo["toponimos_iguales"],
        censo["antroponimos_iguales"], not censo["sin_clase_declarada"],
        censo["vocabulario_base_antes"] == censo["vocabulario_base_despues"],
    ])

    # ── 2. El paradigma en la base ───────────────────────────────────
    paradigma, ka_ma = {}, {}
    if not args.sin_base:
        paradigma = paradigma_de(
            clases, usos, antes.get("reconoce", {}), hoy.get("reconoce", {}),
            antes.get("familia", {}), hoy.get("familia", {}))
        ka_ma = predicacion_ka_ma(nombres)

    # ── 3. Las 216 + 216 ─────────────────────────────────────────────
    scores = {}
    for brazo, r in resultados.items():
        if "replay" not in r["hoy"]:
            continue
        scores[brazo] = diff_de_scores(
            filas_por_brazo[brazo], r["antes"]["replay"], r["hoy"]["replay"])
        scores[brazo]["serie"] = series[brazo]
        # EL CONTROL DE VERDAD: el motor del commit con el que se corrieron
        # los runs tiene que reproducir lo que la base guardó, 216 de 216.
        ctrl = diff_de_scores(filas_por_brazo[brazo], r["base_ref"]["replay"],
                              r["hoy"]["replay"])
        scores[brazo]["control_ref_base"] = args.ref_base
        scores[brazo]["control_base_ref_desvios"] = ctrl["control_replay_desvios"]
        scores[brazo]["control_base_ref_ejemplos"] = ctrl["control_ejemplos"]
        scores[brazo]["control_verde"] = ctrl["control_replay_desvios"] == 0
        # Y la diferencia REF_BASE → REF tiene que ser el corte YA declarado
        # (punto 11 de la bitácora), ni una respuesta más.
        corte_anterior = diff_de_scores(
            filas_por_brazo[brazo], r["base_ref"]["replay"], r["antes"]["replay"])
        scores[brazo]["corte_anterior_score_cambia_en"] = (
            corte_anterior["score_cambia_en"])
        scores[brazo]["corte_anterior_declarado_en_el_punto_11"] = (
            DESVIOS_DECLARADOS_PUNTO_11.get(brazo))
        scores[brazo]["corte_anterior_coincide"] = (
            corte_anterior["score_cambia_en"]
            == DESVIOS_DECLARADOS_PUNTO_11.get(brazo))

    # ── Informe por pantalla ─────────────────────────────────────────
    print("═" * 74)
    print("LA CLASE DE LA RAÍZ — MEDICIÓN DEL CORTE")
    print("═" * 74)
    print(f"brazo «antes»: {args.ref} (lexicon_zavala.py)   ·   «después»: el árbol")
    print()
    print(f"1. CENSO   entradas del glosario {censo['zavala_entradas_antes']} → "
          f"{censo['zavala_entradas_despues']} (mismas claves: "
          f"{censo['zavala_claves_iguales']})")
    print(f"           cat v_raiz en el glosario {censo['zavala_v_raiz_antes']} → "
          f"{censo['zavala_v_raiz_despues']}")
    print(f"           _RAICES_VERB {censo['raices_verbales_antes']} → "
          f"{censo['raices_verbales_despues']}  "
          f"(salen {len(censo['raices_verbales_que_salen'])}, "
          f"entran {len(censo['raices_verbales_que_entran'])})")
    print(f"           VOCABULARIO_BASE {censo['vocabulario_base_antes']} → "
          f"{censo['vocabulario_base_despues']}  (no se archiva ni se añade nada)")
    print(f"           reparto: {censo['reparto']}")
    print(f"           CONTROL {'✓ verde' if censo['control_verde'] else '🔴 ROJO'} "
          f"— glosa_fuente intacta: {censo['glosa_fuente_intacta']}, "
          f"sig intacto: {censo['sig_intacto']}, capa intacta: "
          f"{censo['fuente_intacta']}, notas intactas: {censo['notas_intactas']}")
    print()
    if paradigma:
        print("2. EL PARADIGMA EN LA BASE (las 49 raíces)")
        tot = {"formas": 0, "usos": 0, "fa": 0, "ua": 0, "pf": 0, "pu": 0}
        por_clase: dict = defaultdict(lambda: [0, 0, 0, 0])
        for raiz, d in paradigma.items():
            tot["formas"] += d["formas"]; tot["usos"] += d["usos"]
            tot["fa"] += d["formas_aspecto"]; tot["ua"] += d["usos_aspecto"]
            tot["pf"] += d["formas_que_dejan_de_contar"]
            tot["pu"] += d["usos_que_dejan_de_contar"]
            c = por_clase[d["clase"]]
            c[0] += d["formas"]; c[1] += d["usos"]
            c[2] += d["formas_que_dejan_de_contar"]
            c[3] += d["usos_que_dejan_de_contar"]
        print(f"   familia entera: {tot['formas']} formas · {tot['usos']} usos")
        print(f"   raíz+aspecto:   {tot['fa']} formas · {tot['ua']} usos")
        print(f"   dejan de contar como arahuacas: {tot['pf']} formas · "
              f"{tot['pu']} usos")
        for c, v in sorted(por_clase.items()):
            print(f"     {c:9} {v[0]:4} formas / {v[1]:5} usos → dejan de contar "
                  f"{v[2]:4} / {v[3]:5}")
        top = sorted(paradigma.items(),
                     key=lambda kv: -kv[1]["usos_que_dejan_de_contar"])[:10]
        for raiz, d in top:
            print(f"     {raiz:12} {d['clase']:9} {d['usos']:5} usos → "
                  f"pierden {d['usos_que_dejan_de_contar']:5} "
                  f"({d['formas_que_dejan_de_contar']} formas)")
        print()
    for brazo, s in scores.items():
        print(f"3. {brazo.upper()}  ({'/'.join(s['serie']['id8'])}, cadena "
              f"{'✓' if s['serie']['cadena_ok'] else '🔴'}, "
              f"{s['respuestas']} respuestas)")
        print(f"   CONTROL: el motor de {s['control_ref_base']} (el commit con "
              f"el que se corrieron) reproduce la base en "
              f"{s['respuestas'] - s['control_base_ref_desvios']} de "
              f"{s['respuestas']}  "
              f"{'✓ verde' if s['control_verde'] else '🔴 ROJO'}")
        print(f"   corte ANTERIOR (raíz de ninguna parte, punto 11): mueve "
              f"{s['corte_anterior_score_cambia_en']} respuestas; declarado "
              f"{s['corte_anterior_declarado_en_el_punto_11']}  "
              f"{'✓' if s['corte_anterior_coincide'] else '🔴'}")
        print(f"   score cambia en {s['score_cambia_en']} de {s['respuestas']} "
              f"(|Δ| máx {s['score_delta_max']:.2f}; baja {s['score_baja_en']}, "
              f"sube {s['score_sube_en']})")
        print(f"   score medio {s['score_medio_antes']} → {s['score_medio_despues']}"
              f"   (Δ medio de las que cambian "
              f"{s['score_delta_medio_de_las_que_cambian']})")
        print(f"   palabras_caquetias cambia en {s['palabras_caquetias_cambia_en']}; "
              f"neologisms_proposed en {s['neologisms_proposed_cambia_en']}")
        print(f"   voces que dejan de contarse: "
              f"{list(s['voces_que_dejan_de_contarse'].items())[:10]}")
        print()
    if ka_ma:
        print("4. `juri` Y LOS NOMBRES — la vía del aspecto contra `ka-`/`ma-`")
        print(f"   los {len(nombres)} nombres/adverbios re-clasificados suman "
              f"{ka_ma['familia_entera_usos']} usos en "
              f"{ka_ma['familia_entera_formas']} formas")
        print(f"   vía ASPECTO (nombre+-ka/-ni/-da): {ka_ma['via_aspecto_formas']} "
              f"formas · {ka_ma['via_aspecto_usos']} usos")
        print(f"   vía `ka-` sobre esos nombres:     {ka_ma['via_ka_formas']} "
              f"formas · {ka_ma['via_ka_usos']} usos   {ka_ma['via_ka_detalle']}")
        print(f"   vía `ma-` sobre esos nombres:     {ka_ma['via_ma_formas']} "
              f"formas · {ka_ma['via_ma_usos']} usos   {ka_ma['via_ma_detalle']}")
        print(f"   `ka-` en toda la base: {ka_ma['ka_prefijo_formas']} formas / "
              f"{ka_ma['ka_prefijo_usos']} usos; `ma-`: "
              f"{ka_ma['ma_prefijo_formas']} / {ka_ma['ma_prefijo_usos']}")
        print()

    # ── YAML ─────────────────────────────────────────────────────────
    W: list[str] = []
    A = W.append
    A("# ─────────────────────────────────────────────────────────────────")
    A("# LA CLASE DE LA RAÍZ — MEDICIÓN DEL CORTE")
    A("#")
    A("# GENERADO por 6-fusion/scripts/medir_clases_de_raiz.py")
    A("# No se edita a mano: se regenera. La clasificación fila a fila está en")
    A("# curiana_sim/minar_zavala_glosario.py::CLASE_DE_LA_RAIZ y sale al")
    A("# módulo generado como CLASES_DE_RAIZ_ZAVALA.")
    A("# ─────────────────────────────────────────────────────────────────")
    A("meta:")
    A(f"  fecha: '{FECHA}'")
    A(f"  ref_antes: '{args.ref}'")
    A(f"  modulo_antes: {_y(antes['modulo_zavala'])}")
    A(f"  modulo_despues: {_y(hoy['modulo_zavala'])}")
    A("  que_cambia: 'sólo `cat`, y sólo en el módulo GENERADO. curiana_lexicon.py")
    A("    no se toca; score_linguistico() no se toca; glosa_fuente no se toca.'")
    A("")
    _bloque(W, "censo", censo)
    A("")
    A("clases:")
    for k in sorted(hoy["clases"]):
        A(f"  {k}: {_y(hoy['clases'][k])}")
    A("")
    if paradigma:
        A("paradigma_en_la_base:")
        for raiz, d in sorted(paradigma.items(),
                              key=lambda kv: -kv[1]["usos"]):
            A(f"  {raiz}:")
            for k, v in d.items():
                if isinstance(v, dict):
                    A(f"    {k}: {json.dumps(v, ensure_ascii=False)}")
                else:
                    A(f"    {k}: {_y(v)}")
        A("")
    for brazo, s in scores.items():
        s2 = {k: v for k, v in s.items() if k != "serie"}
        _bloque(W, f"repuntuacion_{brazo}", s2)
        A(f"  serie: {json.dumps(s['serie'], ensure_ascii=False)}")
        A("")
    if ka_ma:
        _bloque(W, "juri_y_los_nombres", ka_ma)
        A("")
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(W) + "\n")
    print(f"→ {SALIDA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
