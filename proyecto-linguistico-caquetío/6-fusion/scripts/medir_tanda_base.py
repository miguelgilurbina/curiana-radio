#!/usr/bin/env python3
"""LA TANDA DE LA BASE (2026-09-23), medida: UN SOLO CORTE, UNA SOLA MEDICIÓN.

Lo que cambia el prompt antes de congelar la base entró junto —db.1 C y el
agujero de `kira`, db.2, db.3, db.4, db.6 (`decisiones_base_2026-09-22.yaml`)
y dc.2 C+E, dc.3 B (`decisiones_campanas_2026-09-21.yaml`)— y se mide aquí de
una vez, contra `main` antes de la tanda.

Qué mide, en orden:

  1. EL INSTRUMENTO. Tamaños (`VOCABULARIO_BASE`, `FUERA_DEL_HABLA`,
     `FORMAS_DE_PLANTILLA`), las claves de `TODAS_LAS_REGLAS` (dc.2 mueve
     `-gua` → `-wa`) y el catálogo de `[Voces de fuera]`.

  2. LA RAÍZ, sobre TODAS las formas de la base (`word_uses` + `neologisms`):
       a. dc.2 aislado — cuántas formas se segmentan distinto con `-wa` en
          lugar de `-gua` (segmentador local, controlado contra el motor).
       b. el corte entero, antes → hoy: `es_raiz_de_ninguna_parte()` (el
          clasificador), la PUERTA (`archivadas_avalan=False`, sólo hoy) y
          `_familia_de_token()`.
       c. la casi-raíz (db.1 C) según el largo mínimo, de 3 a 7: lo que se
          perdonaría con cada uno. Es de donde sale el 6.

  3. EL PROMPT. Las plantillas estáticas carácter a carácter, el system
     prompt ENTERO de los 63 (el `run_turn` de verdad con `_invoke` espiado,
     misma semilla en los dos brazos) y los quince mensajes de nombramiento
     de la era 2. La longitud predice el score (r = −0,48).

  4. ¿MUEVE EL SCORE? Los seis runs de la serie C repetida (2026-09-21) se
     re-ejecutan enteros por el Observer con tres motores: el del RUN
     (control: tiene que reproducir lo que la base guardó), `main` antes de
     la tanda y hoy. Respuesta a respuesta.

  5. LA SEMILLA DE LA PERSONA (db.3.1). Cuántos de los 63 leen otro
     `[Tu emocionar]` el día 2 y el 3 de una cadena con la semilla del DÍA
     (antes) — hoy el motor la fija con la de la cadena y es 0 por
     construcción; el test lo vigila.

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \\
        python 6-fusion/scripts/medir_tanda_base.py

CÓMO SE MIDE EL «ANTES»: los módulos que la tanda tocó se sacan del commit con
`git show` a un directorio temporal que va PRIMERO en el `sys.path` de un
subproceso, y ese subproceso corre este mismo script. Patrón de
`medir_tanda_21.py`, del que se importan las piezas comunes.

REGLAS DURAS: no abre `curiana_sim/.env`, no llama a la API, no escribe en la
base (la lee por `docker exec … psql`) y no toca el canon.
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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import medir_tanda_21 as M21                                   # noqa: E402

RAIZ = M21.RAIZ
SIM = M21.SIM
FECHA = "2026-09-23"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_tanda_base_{FECHA}.yaml")

# `main` antes de la tanda (el merge de #200): las decisiones escritas, ninguna
# aplicada. Es contra éste que se mide el corte.
REF = "797bace"
# Y el motor CON EL QUE CORRIÓ la serie C repetida (config.motor_commit de los
# seis runs). Entre éste y REF entró #193, que tocó el lexicón: por eso el
# control se pide contra éste y no contra REF.
REF_RUN = "114c991"
BRAZOS = {
    "con_escena": ("ce7cd2a9", "591d12d8", "59aad1c3"),
    "control":    ("4e3eef64", "fafdce5b", "104673f6"),
}
# Los módulos que la tanda tocó (y el de Zavala, que el lexicón importa).
MODULOS = ("curiana_lexicon.py", "curiana_koine.py", "curiana_database.py",
           "curiana_orchestrator_v2.py", "lexicon_zavala.py")
SEMILLAS_DE_LA_SERIE = (21, 22, 23)


# ══════════════════════════════════════════════════════════════════════
# EL BRAZO
# ══════════════════════════════════════════════════════════════════════
def _casi_raiz_por_largo(L, formas: dict) -> dict:
    """db.1 C con largos mínimos de 3 a 7, sobre las formas que el
    clasificador de HOY da por «de ninguna parte» sin el perdón. Se calcula en
    el brazo de hoy: necesita las raíces caquetías VIVAS del lexicón nuevo."""
    por_largo_raices = L._vivas_caquetias_por_largo()

    def casi(seg, minimo):
        s = seg.lower()
        if len(s) < minimo:
            return None
        for n in (len(s), len(s) - 1, len(s) + 1):
            for r in por_largo_raices.get(n, ()):
                if r != s and L._difieren_en_un_caracter(s, r):
                    return r
        return None

    conocidas = L._raices_conocidas()
    sin_perdon = [f for f in formas
                  if f.lower() not in conocidas
                  and not any(s in conocidas for s in L.nucleo_de_token(f))]
    salida = {"formas_sin_raiz_conocida": len(sin_perdon),
              "usos": sum(formas[f] for f in sin_perdon)}
    for minimo in (3, 4, 5, 6, 7):
        rec = {}
        for f in sin_perdon:
            for seg in L.nucleo_de_token(f):
                r = casi(seg, minimo)
                if r:
                    rec[f] = (seg, r)
                    break
        orden = sorted(rec.items(), key=lambda kv: -formas[kv[0]])
        salida[f"largo_{minimo}"] = {
            "formas": len(rec),
            "usos": sum(formas[f] for f in rec),
            "ejemplos": [f"{f} ({s} → {r}, {formas[f]} usos)"
                         for f, (s, r) in orden[:14]],
        }
    salida["elegido"] = L.LARGO_MINIMO_CASI_RAIZ
    return salida


def _mensajes_de_nombramiento(K) -> dict:
    refs = getattr(K, "REFERENTES_ERA2", None)
    if refs is None:
        return {}
    salida = []
    for r in refs:
        e = K.estimulo_de_referente(r, "PARAGUANÁ")
        salida.append({"id": r["id"], "tipo": r["tipo"], "animal": r["animal"],
                       "caracteres": len(e),
                       "lo_que_se_oye": "[Lo que se oye]" in e,
                       "invita_por_la_voz": "por cómo suena" in e})
    return {"n": len(salida), "animales": sum(x["animal"] for x in salida),
            "detalle": salida}


def _emocionar_por_semilla(K) -> dict:
    """Con la semilla del DÍA (el motor de antes): qué agentes leen otro
    `[Tu emocionar]` en los días 2 y 3 de una cadena 21 → 22 → 23."""
    from curiana_agents import ALL_AGENTS
    bloques = {}
    for s in SEMILLAS_DE_LA_SERIE:
        K.fijar_semilla(s)
        bloques[s] = {n: K.prompt_emocionar(n, a.get("etnia"))
                      for n, a in ALL_AGENTS.items()}
    K.fijar_semilla(None)
    primero = SEMILLAS_DE_LA_SERIE[0]
    cambian = {s: sorted(n for n in bloques[s] if bloques[s][n] != bloques[primero][n])
               for s in SEMILLAS_DE_LA_SERIE[1:]}
    return {"agentes": len(bloques[primero]),
            "con_la_semilla_del_dia": {f"{primero}_a_{s}": len(v)
                                       for s, v in cambian.items()},
            "quienes": sorted({n for v in cambian.values() for n in v}),
            "con_la_semilla_de_la_cadena": 0}


def medir_en_proceso(args) -> dict:
    import curiana_koine as K
    import curiana_lexicon as L

    plantillas = M21._plantillas(L)
    d = {
        "modulo": os.path.abspath(L.__file__),
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "fuera_del_habla": len(L.FUERA_DEL_HABLA),
        "formas_de_plantilla": len(L.FORMAS_DE_PLANTILLA),
        "formas_de_plantilla_lista": sorted(L.FORMAS_DE_PLANTILLA),
        "claves_de_todas_las_reglas": sorted(L.TODAS_LAS_REGLAS),
        "prefijos": sorted(L._PREFIJOS_CAQ),
        "sufijos": sorted(L._SUFIJOS_CAQ),
        "voces_de_fuera": sorted(f for _p, f, _g, _fam in L.voces_de_fuera_posibles()),
        "plantillas": {k: {"caracteres": len(v), "texto": v}
                       for k, v in plantillas.items()},
        "tiene_puerta_de_archivo": "archivadas_avalan"
                                   in L.es_raiz_de_ninguna_parte.__code__.co_varnames,
    }
    if args.formas:
        formas = json.load(io.open(args.formas, encoding="utf-8"))
        d["nucleos"] = {f: L.nucleo_de_token(f) for f in formas}
        d["ninguna_parte"] = {f: L.es_raiz_de_ninguna_parte(f) for f in formas}
        d["familia"] = {f: L._familia_de_token(f) for f in formas}
        if d["tiene_puerta_de_archivo"]:
            d["puerta"] = {f: L.es_raiz_de_ninguna_parte(f, archivadas_avalan=False)
                           for f in formas}
            # sólo de los segmentos que NINGUNA tabla conoce: es lo único que
            # C perdona (`hamaka` es clave; que `amaka` diste una letra no
            # perdona nada)
            conocidas = L._raices_conocidas()
            d["casi_raiz"] = {f: [L.casi_raiz_de(s) for s in L.nucleo_de_token(f)
                                  if s not in conocidas]
                              for f in formas}
            cuenta = json.load(io.open(args.formas_usos, encoding="utf-8"))
            d["casi_raiz_por_largo"] = _casi_raiz_por_largo(L, cuenta)
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = M21._replay(L, filas)
    if args.ensayo:
        d["ensayo_prompt"] = M21._ensayo_de_prompt(L)
        d["nombramiento"] = _mensajes_de_nombramiento(K)
        d["emocionar"] = _emocionar_por_semilla(K)
    return d


def modulos_de_ref(ref: str) -> str:
    tmp = tempfile.mkdtemp(prefix=f"curiana_ref_{ref}_")
    for nombre in MODULOS:
        out = subprocess.run(
            ["git", "-C", RAIZ, "show", f"{ref}:./curiana_sim/{nombre}"],
            capture_output=True, encoding="utf-8")
        if out.returncode != 0:
            raise RuntimeError(f"git show {ref}:{nombre} falló: {out.stderr[:300]}")
        with io.open(os.path.join(tmp, nombre), "w", encoding="utf-8",
                     newline="\n") as f:
            f.write(out.stdout)
    return tmp


def correr_brazo(lexicon_dir: str | None, extra: list[str]) -> dict:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["CURIANA_ELENCO"] = "era2"
    env["PYTHONPATH"] = os.pathsep.join(([lexicon_dir] if lexicon_dir else []) + [SIM])
    out = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--json"] + extra,
        capture_output=True, encoding="utf-8", env=env, cwd=SIM)
    if out.returncode != 0:
        raise RuntimeError("el brazo falló:\n" + (out.stderr or "")[-3000:])
    return json.loads(out.stdout)


# ══════════════════════════════════════════════════════════════════════
def main(argv=None):
    M21._forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--formas")
    ap.add_argument("--formas-usos", dest="formas_usos")
    ap.add_argument("--respuestas")
    ap.add_argument("--ensayo", action="store_true")
    args = ap.parse_args(argv)
    if args.json:
        sys.stdout.write(json.dumps(medir_en_proceso(args), ensure_ascii=False))
        return 0

    tmp = tempfile.mkdtemp(prefix="curiana_tanda_base_")
    ref_antes, ref_run = modulos_de_ref(REF), modulos_de_ref(REF_RUN)

    # ── las formas de la base ─────────────────────────────────────────
    formas = M21.formas_de_la_base()
    f_formas = os.path.join(tmp, "formas.json")
    f_usos = os.path.join(tmp, "usos.json")
    json.dump(sorted(formas), io.open(f_formas, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(formas, io.open(f_usos, "w", encoding="utf-8"), ensure_ascii=False)

    # ── las respuestas de la serie C repetida ─────────────────────────
    # ⚠️ `M21.respuestas_de()` ordena por `run_id` —un UUID— y no por día: la
    # cadena `4e3eef64 → fafdce5b → 104673f6` salía como día 3, 1, 2, y el
    # replay procesaba el día 3 sin el léxico de los dos anteriores. El primer
    # control de esta medición salió en ROJO por eso (72 y 51 de 216), no por
    # el motor. Aquí se reordena por día y turno, que es el orden de la
    # cadena; el script del 21 queda como está (su control salió verde porque
    # su brazo sin escena caía en orden por casualidad).
    filas_por_brazo = {}
    for b, ids in BRAZOS.items():
        orden_de_cadena = {run: i for i, run in enumerate(ids)}
        filas = M21.respuestas_de(list(ids))
        filas_por_brazo[b] = [f for _i, f in sorted(
            enumerate(filas),
            key=lambda x: (orden_de_cadena[x[1]["run"]], x[1]["dia"],
                           x[1]["turno"], x[0]))]
    ficheros = {}
    for b, filas in filas_por_brazo.items():
        ficheros[b] = os.path.join(tmp, f"resp_{b}.json")
        json.dump(filas, io.open(ficheros[b], "w", encoding="utf-8"), ensure_ascii=False)

    base = ["--formas", f_formas, "--formas-usos", f_usos, "--ensayo"]
    antes = correr_brazo(ref_antes, base)
    hoy = correr_brazo(None, base)
    replays = {}
    for b, f in ficheros.items():
        extra = ["--respuestas", f]
        replays[b] = {"run": correr_brazo(ref_run, extra),
                      "antes": correr_brazo(ref_antes, extra),
                      "hoy": correr_brazo(None, extra)}

    doc: dict = {
        "medicion": "tanda-de-la-base-un-corte-una-medicion",
        "fecha": FECHA,
        "ref_de_antes": REF,
        "ref_del_run": REF_RUN,
        "decide": ["6-fusion/decisiones_base_2026-09-22.yaml",
                   "6-fusion/decisiones_campanas_2026-09-21.yaml §dc.2 §dc.3"],
        "que_se_aplico": [
            "db.1 C — la casi-raíz de largo ≥ 6 se perdona (raíces caquetías vivas)",
            "db.1 — el agujero de kira: una raíz archivada no avala en la puerta",
            "db.2 — datihao pasa a taíno (commit 2f898ec, antes de esta medición)",
            "db.3.1 — la semilla de la persona es la de la cadena",
            "db.3.2 — las 8 taíno-reconstruido al archivo; daca es taíno 'yo'",
            "db.3.3 — mayani, caney, batey, tabako y siba según su cronista",
            "db.4 — el catálogo de la era 2, novedad/hueco, uno cada dos días",
            "db.6 — la puerta onomatopéyica en la competencia de un animal",
            "dc.2 C+E — -gua 'región' pasa a -wa, sin glosa",
            "dc.3 B — la derivación cero se enseña (jusual)",
            "d21.6, lo que faltaba — el ejemplo ideal ya no glosa buko-ana",
        ],
    }

    # ── 1. el instrumento ─────────────────────────────────────────────
    doc["instrumento"] = {
        k: {"antes": antes[k], "hoy": hoy[k]}
        for k in ("vocabulario_base", "fuera_del_habla", "formas_de_plantilla")
    }
    doc["instrumento"]["sufijos"] = {
        "salen": sorted(set(antes["sufijos"]) - set(hoy["sufijos"])),
        "entran": sorted(set(hoy["sufijos"]) - set(antes["sufijos"]))}
    fp_a, fp_h = set(antes["formas_de_plantilla_lista"]), set(hoy["formas_de_plantilla_lista"])
    doc["instrumento"]["formas_de_plantilla_salen"] = sorted(fp_a - fp_h)[:40]
    doc["instrumento"]["formas_de_plantilla_entran"] = sorted(fp_h - fp_a)[:40]
    doc["instrumento"]["voces_de_fuera"] = {
        "antes": len(antes["voces_de_fuera"]), "hoy": len(hoy["voces_de_fuera"]),
        "salen": sorted(set(antes["voces_de_fuera"]) - set(hoy["voces_de_fuera"])),
        "entran": sorted(set(hoy["voces_de_fuera"]) - set(antes["voces_de_fuera"]))}

    # ── 2. la raíz ────────────────────────────────────────────────────
    pre_a, suf_a = frozenset(antes["prefijos"]), frozenset(antes["sufijos"])
    pre_h, suf_h = frozenset(hoy["prefijos"]), frozenset(hoy["sufijos"])
    control_seg = [f for f in formas
                   if M21.nucleo_con(pre_h, suf_h, f) != hoy["nucleos"][f]]
    dc2 = M21.diff_de_nucleos(formas, pre_a, suf_a, pre_h, suf_h)
    dc2["control_del_segmentador"] = {"desvios": len(control_seg), "verde": not control_seg}
    # ¿alguna de las formas que dc.2 re-segmenta cambia de clase? El núcleo
    # sólo importa por sus dos consumidores (patrón de d21.14 en el 21).
    re_seg = {f for f in formas
              if M21.nucleo_con(pre_a, suf_a, f) != M21.nucleo_con(pre_h, suf_h, f)}
    dc2["de_ellas_cambian_ninguna_parte"] = sorted(
        f for f in re_seg if antes["ninguna_parte"][f] != hoy["ninguna_parte"][f])
    dc2["de_ellas_cambian_familia"] = sorted(
        f for f in re_seg if antes["familia"][f] != hoy["familia"][f])

    def cambia(clave):
        c = [f for f in formas if antes[clave][f] != hoy[clave][f]]
        c.sort(key=lambda f: -formas[f])
        return {"formas": len(c), "usos": sum(formas[f] for f in c),
                "detalle": [f"{f}: {antes[clave][f]} → {hoy[clave][f]} ({formas[f]} usos)"
                            for f in c[:30]]}

    puerta_cierra = [f for f in formas if hoy["puerta"][f] and not hoy["ninguna_parte"][f]]
    puerta_cierra.sort(key=lambda f: -formas[f])
    perdonadas = [f for f in formas if any(hoy["casi_raiz"][f])]
    perdonadas.sort(key=lambda f: -formas[f])
    doc["raiz"] = {
        "formas_de_la_base": len(formas),
        "usos": sum(formas.values()),
        "dc2_desafijador": dc2,
        "clasificador_ninguna_parte": cambia("ninguna_parte"),
        "familia": cambia("familia"),
        "puerta_archivo_cierra": {
            "que_es": ("formas cuya ÚNICA raíz conocida es una ARCHIVADA: el "
                       "clasificador las sigue leyendo, la puerta ya no las deja "
                       "registrarse ni competir (el agujero de kira)"),
            "formas": len(puerta_cierra),
            "usos": sum(formas[f] for f in puerta_cierra),
            "detalle": [f"{f} ({formas[f]} usos)" for f in puerta_cierra[:30]]},
        "casi_raiz_perdonadas_hoy": {
            "formas": len(perdonadas),
            "usos": sum(formas[f] for f in perdonadas),
            "detalle": [f"{f} → {[r for r in hoy['casi_raiz'][f] if r]} ({formas[f]} usos)"
                        for f in perdonadas[:30]]},
        "casi_raiz_por_largo": hoy["casi_raiz_por_largo"],
    }

    # ── 3. el prompt ──────────────────────────────────────────────────
    doc["prompt"] = {
        "plantillas": {
            k: {"antes": antes["plantillas"][k]["caracteres"],
                "hoy": hoy["plantillas"][k]["caracteres"],
                "cambia": antes["plantillas"][k]["texto"] != hoy["plantillas"][k]["texto"]}
            for k in hoy["plantillas"]},
        "system_prompt_de_los_63": {
            k: {"antes": antes["ensayo_prompt"][k], "hoy": hoy["ensayo_prompt"][k]}
            for k in ("prompts", "medio", "mediana", "min", "max")},
        "nombramiento_era2": hoy["nombramiento"],
    }
    la, lh = antes["ensayo_prompt"]["largos"], hoy["ensayo_prompt"]["largos"]
    doc["prompt"]["system_prompt_de_los_63"]["cambio_medio_pct"] = round(
        100 * (sum(lh) / len(lh) - sum(la) / len(la)) / (sum(la) / len(la)), 2)

    # ── 4. el score ───────────────────────────────────────────────────
    doc["score"] = {}
    for b, r in replays.items():
        filas = filas_por_brazo[b]
        doc["score"][b] = {
            "runs": list(BRAZOS[b]),
            "control": M21.control_del_replay(filas, r["run"]),
            "del_run_a_antes": {k: v for k, v in
                                M21.diff_de_scores(filas, r["run"], r["antes"]).items()
                                if k != "detalle"},
            "antes_a_hoy": M21.diff_de_scores(filas, r["antes"], r["hoy"]),
            "adoptadas": {"antes": r["antes"]["replay"]["adoptadas"],
                          "hoy": r["hoy"]["replay"]["adoptadas"]},
            "rechazos_de_raiz": {"antes": len(r["antes"]["replay"]["rechazos_de_raiz"]),
                                 "hoy": len(r["hoy"]["replay"]["rechazos_de_raiz"])},
            "fijadas": {"antes": r["antes"]["replay"]["fijadas"],
                        "hoy": r["hoy"]["replay"]["fijadas"]},
        }
        doc["score"][b]["antes_a_hoy"]["detalle"] = \
            doc["score"][b]["antes_a_hoy"]["detalle"][:20]

    # ── 5. la semilla ─────────────────────────────────────────────────
    doc["semilla_de_la_persona"] = hoy["emocionar"]

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por 6-fusion/scripts/medir_tanda_base.py — NO editar a mano.\n")
        f.write("\n".join(M21.volcar(doc)) + "\n")

    # ── resumen ───────────────────────────────────────────────────────
    print(f"→ {os.path.relpath(SALIDA, RAIZ)}")
    i = doc["instrumento"]
    print(f"  vocabulario {i['vocabulario_base']['antes']} → {i['vocabulario_base']['hoy']} · "
          f"archivo {i['fuera_del_habla']['antes']} → {i['fuera_del_habla']['hoy']} · "
          f"[Voces de fuera] {i['voces_de_fuera']['antes']} → {i['voces_de_fuera']['hoy']}")
    print(f"  sufijos: salen {i['sufijos']['salen']} · entran {i['sufijos']['entran']}")
    rz = doc["raiz"]
    print(f"  dc.2: {rz['dc2_desafijador']['formas']} formas se segmentan distinto "
          f"({rz['dc2_desafijador']['usos']} usos), de ellas cambian de clase "
          f"{len(rz['dc2_desafijador']['de_ellas_cambian_ninguna_parte'])}/"
          f"{len(rz['dc2_desafijador']['de_ellas_cambian_familia'])}; control del segmentador "
          f"{'verde' if rz['dc2_desafijador']['control_del_segmentador']['verde'] else 'ROJO'}")
    print(f"  clasificador: {rz['clasificador_ninguna_parte']['formas']} formas cambian "
          f"«de ninguna parte» ({rz['clasificador_ninguna_parte']['usos']} usos); "
          f"familia: {rz['familia']['formas']}")
    print(f"  casi-raíz perdonada: {rz['casi_raiz_perdonadas_hoy']['formas']} formas · "
          f"la puerta del archivo cierra {rz['puerta_archivo_cierra']['formas']}")
    p = doc["prompt"]["system_prompt_de_los_63"]
    print(f"  system prompt medio {p['medio']['antes']} → {p['medio']['hoy']} "
          f"({p['cambio_medio_pct']:+} %)")
    for b, s in doc["score"].items():
        c, d = s["control"], s["antes_a_hoy"]
        print(f"  [{b}] control {'verde' if c['verde'] else 'ROJO'} ({c['desvios']} de {c['n']}) · "
              f"cambian {d['cambian']} de {d['n']} (↓{d['a_la_baja']} ↑{d['al_alza']}, "
              f"|Δ| máx {d['delta_max_abs']}) · score medio {d['score_medio_antes']} → "
              f"{d['score_medio_hoy']}")
    e = doc["semilla_de_la_persona"]
    print(f"  [Tu emocionar] con la semilla del día: {e['con_la_semilla_del_dia']} de "
          f"{e['agentes']}; con la de la cadena: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
