#!/usr/bin/env python3
"""LA ÚLTIMA TANDA ANTES DE LA CORRIDA BASE (2026-09-23): un corte, una medición.

Lo que Miguel aceptó en `6-fusion/decisiones_tanda_final_2026-09-23.yaml`
(tf.0-tf.9) entra junto y se mide aquí de una vez, contra `main`:

  · D11 fase 3 — pronombres (dai, bui, lihi/tuhu; waya/naya se quedan),
    aspecto (presente sin marca, -kuba, -ba), posesivo da-, y las voces
    reconstruidas desde el wayuu que quedaban (tf.5);
  · la tanda de fuentes — poporo, macana, coro, cohoba, las voces de Zayas,
    daca — y baperon/raporon a los pemenos;
  · la sigla (E) de Zavala, opción B, y lo que toca al prompt (los ejemplos de
    kari y waranao, el rótulo de -iro/-uco);
  · el canon del mundo (Manaure A, guaiqueríes A+B+E, cronología C) y los
    topónimos.

Qué mide, en orden:
  1. EL INSTRUMENTO: tamaños, capas del lexicón (entradas por `fuente`),
     claves de `TODAS_LAS_REGLAS`, `[Voces de fuera]`.
  2. EL DESAFIJADOR Y LA RAÍZ sobre todas las formas de la base: núcleo,
     «raíz de ninguna parte» (clasificador y puerta) y familia.
  3. EL PROMPT: plantillas carácter a carácter, el system prompt ENTERO de los
     63 (`run_turn` de verdad, `_invoke` espiado, misma semilla) y el
     `[Tu emocionar]` de cada uno.
  4. ¿MUEVE EL SCORE? La serie C repetida (216 + 216) re-puntuada con tres
     motores: el del run (control), `main` y hoy. Con el aspecto nuevo el
     score TIENE que caer: se dice cuánto y por qué componente.

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \\
        python 6-fusion/scripts/medir_tanda_final.py

No abre `curiana_sim/.env`, no llama a la API, no escribe en la base (la lee
por `docker exec … psql`) y no toca el canon.
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
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_tanda_final_{FECHA}.yaml")

# `main` antes de la tanda final (#230): la base de la tanda anterior ya
# mergeada y las propuestas de cierre en 6-fusion/, ninguna aplicada.
REF = "1a97628"
# El motor con que corrió la serie C repetida (config.motor_commit).
REF_RUN = "114c991"
BRAZOS = {
    "con_escena": ("ce7cd2a9", "591d12d8", "59aad1c3"),
    "control":    ("4e3eef64", "fafdce5b", "104673f6"),
}
MODULOS = ("curiana_lexicon.py", "curiana_koine.py", "curiana_database.py",
           "curiana_orchestrator_v2.py", "curiana_escena.py", "curiana_mundo.py",
           "lexicon_zavala.py", "curiana_agents_era2.py")
SEMILLA = 21


def _capas(L) -> dict:
    return dict(collections.Counter(
        v.get("fuente", "(sin fuente)") for v in L.VOCABULARIO_BASE.values()))


def _emocionar(K) -> dict:
    from curiana_agents import ALL_AGENTS
    K.fijar_semilla(SEMILLA)
    salida = {n: K.prompt_emocionar(n, a.get("etnia")) for n, a in ALL_AGENTS.items()}
    semillas = {n: K.formas_semilla(n, K.emocionar_de(n, a.get("etnia")))
                for n, a in ALL_AGENTS.items()}
    K.fijar_semilla(None)
    return {"bloques": salida, "semillas": semillas}


def medir_en_proceso(args) -> dict:
    import curiana_koine as K
    import curiana_lexicon as L

    plantillas = M21._plantillas(L)
    d = {
        "vocabulario_base": len(L.VOCABULARIO_BASE),
        "fuera_del_habla": len(L.FUERA_DEL_HABLA),
        "formas_de_plantilla": len(L.FORMAS_DE_PLANTILLA),
        "formas_de_plantilla_lista": sorted(L.FORMAS_DE_PLANTILLA),
        "capas": _capas(L),
        "claves_de_todas_las_reglas": sorted(L.TODAS_LAS_REGLAS),
        "prefijos": sorted(L._PREFIJOS_CAQ),
        "sufijos": sorted(L._SUFIJOS_CAQ),
        "voces_de_fuera": sorted(f for _p, f, _g, _fam in L.voces_de_fuera_posibles()),
        "plantillas": {k: {"caracteres": len(v), "texto": v}
                       for k, v in plantillas.items()},
    }
    if args.formas:
        formas = json.load(io.open(args.formas, encoding="utf-8"))
        d["nucleos"] = {f: L.nucleo_de_token(f) for f in formas}
        d["ninguna_parte"] = {f: L.es_raiz_de_ninguna_parte(f) for f in formas}
        d["familia"] = {f: L._familia_de_token(f) for f in formas}
    if args.respuestas:
        filas = json.load(io.open(args.respuestas, encoding="utf-8"))
        d["replay"] = M21._replay(L, filas)
    if args.ensayo:
        d["ensayo_prompt"] = M21._ensayo_de_prompt(L)
        d["emocionar"] = _emocionar(K)
    return d


def modulos_de_ref(ref: str) -> str:
    tmp = tempfile.mkdtemp(prefix=f"curiana_ref_{ref}_")
    for nombre in MODULOS:
        out = subprocess.run(
            ["git", "-C", RAIZ, "show", f"{ref}:./curiana_sim/{nombre}"],
            capture_output=True, encoding="utf-8")
        if out.returncode != 0:
            continue                    # el módulo no existía en ese commit
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


def main(argv=None):
    M21._forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--formas")
    ap.add_argument("--respuestas")
    ap.add_argument("--ensayo", action="store_true")
    args = ap.parse_args(argv)
    if args.json:
        sys.stdout.write(json.dumps(medir_en_proceso(args), ensure_ascii=False))
        return 0

    tmp = tempfile.mkdtemp(prefix="curiana_tanda_final_")
    ref_antes, ref_run = modulos_de_ref(REF), modulos_de_ref(REF_RUN)

    formas = M21.formas_de_la_base()
    f_formas = os.path.join(tmp, "formas.json")
    json.dump(sorted(formas), io.open(f_formas, "w", encoding="utf-8"), ensure_ascii=False)

    filas_por_brazo, ficheros = {}, {}
    for b, ids in BRAZOS.items():
        filas = M21.respuestas_de(list(ids))       # ya ordena por día (arreglado el 09-23)
        filas_por_brazo[b] = filas
        ficheros[b] = os.path.join(tmp, f"resp_{b}.json")
        json.dump(filas, io.open(ficheros[b], "w", encoding="utf-8"), ensure_ascii=False)

    base = ["--formas", f_formas, "--ensayo"]
    antes = correr_brazo(ref_antes, base)
    hoy = correr_brazo(None, base)
    replays = {b: {"run": correr_brazo(ref_run, ["--respuestas", f]),
                   "antes": correr_brazo(ref_antes, ["--respuestas", f]),
                   "hoy": correr_brazo(None, ["--respuestas", f])}
               for b, f in ficheros.items()}

    doc: dict = {
        "medicion": "tanda-final-antes-de-la-base",
        "fecha": FECHA,
        "ref_de_antes": REF,
        "ref_del_run": REF_RUN,
        "decide": "6-fusion/decisiones_tanda_final_2026-09-23.yaml",
    }
    # 1. el instrumento
    doc["instrumento"] = {k: {"antes": antes[k], "hoy": hoy[k]}
                          for k in ("vocabulario_base", "fuera_del_habla", "formas_de_plantilla")}
    capas = sorted(set(antes["capas"]) | set(hoy["capas"]))
    doc["instrumento"]["capas"] = {c: {"antes": antes["capas"].get(c, 0),
                                       "hoy": hoy["capas"].get(c, 0)}
                                   for c in capas if antes["capas"].get(c, 0) != hoy["capas"].get(c, 0)}
    for k in ("claves_de_todas_las_reglas", "prefijos", "sufijos", "voces_de_fuera"):
        doc["instrumento"][k] = {"salen": sorted(set(antes[k]) - set(hoy[k])),
                                 "entran": sorted(set(hoy[k]) - set(antes[k])),
                                 "antes": len(antes[k]), "hoy": len(hoy[k])}
    fp_a, fp_h = set(antes["formas_de_plantilla_lista"]), set(hoy["formas_de_plantilla_lista"])
    doc["instrumento"]["formas_de_plantilla_salen"] = sorted(fp_a - fp_h)[:60]
    doc["instrumento"]["formas_de_plantilla_entran"] = sorted(fp_h - fp_a)[:60]

    # 2. el desafijador y la raíz
    def cambia(clave):
        c = sorted((f for f in formas if antes[clave][f] != hoy[clave][f]),
                   key=lambda f: -formas[f])
        return {"formas": len(c), "usos": sum(formas[f] for f in c),
                "detalle": [f"{f}: {antes[clave][f]} → {hoy[clave][f]} ({formas[f]} usos)"
                            for f in c[:30]]}
    doc["raiz"] = {"formas_de_la_base": len(formas), "usos": sum(formas.values()),
                   "nucleo": cambia("nucleos"), "ninguna_parte": cambia("ninguna_parte"),
                   "familia": cambia("familia")}

    # 3. el prompt
    la, lh = antes["ensayo_prompt"]["largos"], hoy["ensayo_prompt"]["largos"]
    ea, eh = antes["emocionar"], hoy["emocionar"]
    doc["prompt"] = {
        "plantillas": {k: {"antes": antes["plantillas"][k]["caracteres"],
                           "hoy": hoy["plantillas"][k]["caracteres"],
                           "cambia": antes["plantillas"][k]["texto"] != hoy["plantillas"][k]["texto"]}
                       for k in hoy["plantillas"]},
        "system_prompt_de_los_63": {
            **{k: {"antes": antes["ensayo_prompt"][k], "hoy": hoy["ensayo_prompt"][k]}
               for k in ("prompts", "medio", "mediana", "min", "max")},
            "cambio_medio_pct": round(100 * (sum(lh) / len(lh) - sum(la) / len(la))
                                      / (sum(la) / len(la)), 2)},
        "tu_emocionar_cambia_en": sum(1 for n in eh["bloques"]
                                      if ea["bloques"].get(n) != eh["bloques"][n]),
        "semilla_de_idiolecto_cambia_en": sum(1 for n in eh["semillas"]
                                              if ea["semillas"].get(n) != eh["semillas"][n]),
        "agentes": len(eh["bloques"]),
    }

    # 4. el score
    doc["score"] = {}
    for b, r in replays.items():
        filas = filas_por_brazo[b]
        antes_hoy = M21.diff_de_scores(filas, r["antes"], r["hoy"])
        antes_hoy["detalle"] = antes_hoy["detalle"][:20]
        doc["score"][b] = {
            "runs": list(BRAZOS[b]),
            "control": M21.control_del_replay(filas, r["run"]),
            "del_run_a_antes": {k: v for k, v in
                                M21.diff_de_scores(filas, r["run"], r["antes"]).items()
                                if k not in ("detalle", "por_run")},
            "antes_a_hoy": antes_hoy,
            "adoptadas": {"antes": r["antes"]["replay"]["adoptadas"],
                          "hoy": r["hoy"]["replay"]["adoptadas"]},
            "fijadas": {"antes": r["antes"]["replay"]["fijadas"],
                        "hoy": r["hoy"]["replay"]["fijadas"]},
        }

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Generado por 6-fusion/scripts/medir_tanda_final.py — NO editar a mano.\n")
        f.write("\n".join(M21.volcar(doc)) + "\n")

    print(f"→ {os.path.relpath(SALIDA, RAIZ)}")
    i = doc["instrumento"]
    print(f"  vocabulario {i['vocabulario_base']['antes']} → {i['vocabulario_base']['hoy']} · "
          f"archivo {i['fuera_del_habla']['antes']} → {i['fuera_del_habla']['hoy']} · "
          f"[Voces de fuera] {i['voces_de_fuera']['antes']} → {i['voces_de_fuera']['hoy']}")
    print(f"  capas que cambian: {i['capas']}")
    print(f"  reglas: salen {i['claves_de_todas_las_reglas']['salen']} · "
          f"entran {i['claves_de_todas_las_reglas']['entran']}")
    rz = doc["raiz"]
    print(f"  núcleo cambia en {rz['nucleo']['formas']} formas · «ninguna parte» en "
          f"{rz['ninguna_parte']['formas']} · familia en {rz['familia']['formas']}")
    p = doc["prompt"]
    print(f"  system prompt medio {p['system_prompt_de_los_63']['medio']['antes']} → "
          f"{p['system_prompt_de_los_63']['medio']['hoy']} "
          f"({p['system_prompt_de_los_63']['cambio_medio_pct']:+} %) · [Tu emocionar] cambia "
          f"en {p['tu_emocionar_cambia_en']} de {p['agentes']} · semilla en "
          f"{p['semilla_de_idiolecto_cambia_en']}")
    for b, s in doc["score"].items():
        c, d = s["control"], s["antes_a_hoy"]
        print(f"  [{b}] control {'verde' if c['verde'] else 'ROJO'} ({c['desvios']} de {c['n']}) · "
              f"cambian {d['cambian']} de {d['n']} (↓{d['a_la_baja']} ↑{d['al_alza']}) · "
              f"score {d['score_medio_antes']} → {d['score_medio_hoy']} · aspecto "
              f"{d['aspecto_medio_antes']} → {d['aspecto_medio_hoy']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
