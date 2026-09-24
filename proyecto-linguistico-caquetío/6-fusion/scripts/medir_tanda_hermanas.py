#!/usr/bin/env python3
"""LA TANDA DE LAS HERMANAS (2026-09-24): un corte, una medición.

Lo que Miguel aceptó con «Acepto todo lo recomendado»
(`6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml`) entra junto y se mide
aquí contra `main` (6aa43a5, la tanda final ya mergeada):

  · el núcleo fundacional rehecho desde el lokono y el habla de mujeres
    kalinago (th.6 N1, th.7), las ocho voces que seguían saliendo del wayuu
    (th.2), alaain/japü (th.3) y los pronombres de D1 (th.1);
  · las plantillas, la koiné y los generados que eso arrastra.

Qué mide, en orden (es la maquinaria de `medir_tanda_final.py`):
  1. EL INSTRUMENTO: tamaños, capas del lexicón, reglas, `[Voces de fuera]`,
     formas de plantilla que salen y entran.
  2. EL PROMPT: plantillas carácter a carácter, el system prompt ENTERO de los
     63 (`run_turn` de verdad, `_invoke` espiado, misma semilla), el
     `[Tu emocionar]` y la semilla de idiolecto de cada uno.
  Con `--con-base` (necesita Docker y la base local):
  3. EL DESAFIJADOR Y LA RAÍZ sobre todas las formas de la base.
  4. ¿MUEVE EL SCORE? La serie C repetida re-puntuada con el motor del run
     (control), `main` y hoy.

Uso:
    CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 \\
        python 6-fusion/scripts/medir_tanda_hermanas.py [--con-base]

Sin `--con-base` la salida lo dice en `pendiente_con_la_base`: un cero de algo
que no se midió no es un cero. No abre `curiana_sim/.env`, no llama a la API,
no escribe en la base y no toca el canon.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import medir_tanda_21 as M21                                   # noqa: E402
import medir_tanda_final as MF                                 # noqa: E402

RAIZ = M21.RAIZ
FECHA = "2026-09-24"
SALIDA = os.path.join(RAIZ, "6-fusion", f"medicion_tanda_hermanas_{FECHA}.yaml")

# `main` antes de la tanda de las hermanas (#233 mergeado: la tanda final).
REF = "6aa43a5"
# El motor con que corrió la serie C repetida, y sus runs: los mismos que
# midió la tanda final.
REF_RUN = MF.REF_RUN
BRAZOS = MF.BRAZOS
# La respuesta fija del ensayo del prompt, dicha con lo que vale en `main` Y
# hoy. La de las mediciones anteriores («Taya wana-ka arima wara kari…») hoy
# puntúa baja —`arima` y `wara` se archivaron—, dispara la segunda pasada y el
# ensayo contaba 126 prompts contra 63: medido el 2026-09-24.
RESPUESTA_ENSAYO = "Dai diki-kuba para. Da-barsure kuburuku."


def medir_en_proceso(args) -> dict:
    """Lo de `medir_tanda_final.medir_en_proceso`, con la respuesta de arriba."""
    import curiana_koine as K
    import curiana_lexicon as L
    d = MF.medir_en_proceso(argparse.Namespace(
        formas=args.formas, respuestas=args.respuestas, ensayo=False))
    if args.ensayo:
        d["ensayo_prompt"] = M21._ensayo_de_prompt(L, RESPUESTA_ENSAYO)
        d["emocionar"] = MF._emocionar(K)
    return d


def correr_brazo(lexicon_dir: str | None, extra: list[str]) -> dict:
    """Como `medir_tanda_final.correr_brazo`, pero corre ESTE fichero."""
    import subprocess
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["CURIANA_ELENCO"] = "era2"
    env["PYTHONPATH"] = os.pathsep.join(([lexicon_dir] if lexicon_dir else []) + [M21.SIM])
    out = subprocess.run(
        [sys.executable, os.path.abspath(__file__), "--json"] + extra,
        capture_output=True, encoding="utf-8", env=env, cwd=M21.SIM)
    if out.returncode != 0:
        raise RuntimeError("el brazo falló:\n" + (out.stderr or "")[-3000:])
    return json.loads(out.stdout)


def _instrumento(antes: dict, hoy: dict) -> dict:
    d = {k: {"antes": antes[k], "hoy": hoy[k]}
         for k in ("vocabulario_base", "fuera_del_habla", "formas_de_plantilla")}
    capas = sorted(set(antes["capas"]) | set(hoy["capas"]))
    d["capas"] = {c: {"antes": antes["capas"].get(c, 0), "hoy": hoy["capas"].get(c, 0)}
                  for c in capas if antes["capas"].get(c, 0) != hoy["capas"].get(c, 0)}
    for k in ("claves_de_todas_las_reglas", "prefijos", "sufijos", "voces_de_fuera"):
        d[k] = {"salen": sorted(set(antes[k]) - set(hoy[k])),
                "entran": sorted(set(hoy[k]) - set(antes[k])),
                "antes": len(antes[k]), "hoy": len(hoy[k])}
    fp_a, fp_h = set(antes["formas_de_plantilla_lista"]), set(hoy["formas_de_plantilla_lista"])
    d["formas_de_plantilla_salen"] = sorted(fp_a - fp_h)
    d["formas_de_plantilla_entran"] = sorted(fp_h - fp_a)
    return d


def _prompt(antes: dict, hoy: dict) -> dict:
    la, lh = antes["ensayo_prompt"]["largos"], hoy["ensayo_prompt"]["largos"]
    ea, eh = antes["emocionar"], hoy["emocionar"]
    return {
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
        "semilla_mas_corta_hoy": min(len(v) for v in eh["semillas"].values()),
        "agentes": len(eh["bloques"]),
    }


def main(argv=None):
    M21._forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--con-base", action="store_true",
                    help="mide también la raíz y el score sobre la base (Docker)")
    ap.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--formas", help=argparse.SUPPRESS)
    ap.add_argument("--respuestas", help=argparse.SUPPRESS)
    ap.add_argument("--ensayo", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    if args.json:
        sys.stdout.write(json.dumps(medir_en_proceso(args), ensure_ascii=False))
        return 0

    tmp = tempfile.mkdtemp(prefix="curiana_tanda_hermanas_")
    ref_antes = MF.modulos_de_ref(REF)
    ref_run = MF.modulos_de_ref(REF_RUN) if args.con_base else None
    try:
        return _medir(tmp, ref_antes, ref_run, args.con_base)
    finally:
        MF._limpiar_worktrees()


def _medir(tmp: str, ref_antes: str, ref_run: str | None, con_base: bool) -> int:
    base = ["--ensayo"]
    formas = None
    if con_base:
        formas = M21.formas_de_la_base()
        f_formas = os.path.join(tmp, "formas.json")
        json.dump(sorted(formas), io.open(f_formas, "w", encoding="utf-8"), ensure_ascii=False)
        base += ["--formas", f_formas]
    antes = correr_brazo(ref_antes, base)
    hoy = correr_brazo(None, base)

    doc: dict = {
        "medicion": "tanda-de-las-hermanas",
        "fecha": FECHA,
        "ref_de_antes": REF,
        "decide": "6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml",
        "con_la_base": con_base,
    }
    doc["instrumento"] = _instrumento(antes, hoy)
    doc["prompt"] = _prompt(antes, hoy)

    if con_base:
        def cambia(clave):
            c = sorted((f for f in formas if antes[clave][f] != hoy[clave][f]),
                       key=lambda f: -formas[f])
            return {"formas": len(c), "usos": sum(formas[f] for f in c),
                    "detalle": [f"{f}: {antes[clave][f]} → {hoy[clave][f]} ({formas[f]} usos)"
                                for f in c[:40]]}
        doc["raiz"] = {"formas_de_la_base": len(formas), "usos": sum(formas.values()),
                       "nucleo": cambia("nucleos"), "ninguna_parte": cambia("ninguna_parte"),
                       "familia": cambia("familia")}
        doc["score"] = {}
        for b, ids in BRAZOS.items():
            filas = M21.respuestas_de(list(ids))
            f = os.path.join(tmp, f"resp_{b}.json")
            json.dump(filas, io.open(f, "w", encoding="utf-8"), ensure_ascii=False)
            r = {"run": correr_brazo(ref_run, ["--respuestas", f]),
                 "antes": correr_brazo(ref_antes, ["--respuestas", f]),
                 "hoy": correr_brazo(None, ["--respuestas", f])}
            antes_hoy = M21.diff_de_scores(filas, r["antes"], r["hoy"])
            antes_hoy["detalle"] = antes_hoy["detalle"][:20]
            doc["score"][b] = {
                "runs": list(ids),
                "control": M21.control_del_replay(filas, r["run"]),
                "antes_a_hoy": antes_hoy,
                "adoptadas": {"antes": r["antes"]["replay"]["adoptadas"],
                              "hoy": r["hoy"]["replay"]["adoptadas"]},
                "fijadas": {"antes": r["antes"]["replay"]["fijadas"],
                            "hoy": r["hoy"]["replay"]["fijadas"]},
            }
    else:
        doc["pendiente_con_la_base"] = [
            "el control: re-puntuar la serie C repetida con el motor del run tiene que reproducir sus scores",
            "cuánto se mueve el score de esas 216 + 216 respuestas de main a hoy, y por qué componente",
            "el uso histórico de las voces archivadas (usos sueltos y como núcleo que dejan de contar)",
            "que las formas NUEVAS de las plantillas no se hayan dicho nunca en la base "
            "(ada-bana, ada-bakoa, kidi-bana, kunu-kuba, da-akusi, wa-uni, ma-ako…): "
            "la condición de d21.14 para un ejemplo del prompt",
        ]

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Generado por 6-fusion/scripts/medir_tanda_hermanas.py — NO editar a mano.\n")
        fh.write("\n".join(M21.volcar(doc)) + "\n")

    print(f"→ {os.path.relpath(SALIDA, RAIZ)}")
    i, p = doc["instrumento"], doc["prompt"]
    print(f"  vocabulario {i['vocabulario_base']['antes']} → {i['vocabulario_base']['hoy']} · "
          f"archivo {i['fuera_del_habla']['antes']} → {i['fuera_del_habla']['hoy']} · "
          f"formas de plantilla {i['formas_de_plantilla']['antes']} → {i['formas_de_plantilla']['hoy']}")
    print(f"  capas que cambian: {i['capas']}")
    s = p["system_prompt_de_los_63"]
    print(f"  system prompt medio {s['medio']['antes']} → {s['medio']['hoy']} "
          f"({s['cambio_medio_pct']:+} %) · [Tu emocionar] cambia en "
          f"{p['tu_emocionar_cambia_en']} de {p['agentes']} · semilla en "
          f"{p['semilla_de_idiolecto_cambia_en']} (la más corta: {p['semilla_mas_corta_hoy']})")
    for k, v in p["plantillas"].items():
        print(f"    {k:28} {v['antes']:>6} → {v['hoy']:>6}")
    if con_base:
        rz = doc["raiz"]
        print(f"  núcleo cambia en {rz['nucleo']['formas']} formas · «ninguna parte» en "
              f"{rz['ninguna_parte']['formas']} · familia en {rz['familia']['formas']}")
        for b, sc in doc["score"].items():
            c, d = sc["control"], sc["antes_a_hoy"]
            print(f"  [{b}] control {'verde' if c['verde'] else 'ROJO'} ({c['desvios']} de {c['n']}) · "
                  f"cambian {d['cambian']} de {d['n']} (↓{d['a_la_baja']} ↑{d['al_alza']}) · "
                  f"score {d['score_medio_antes']} → {d['score_medio_hoy']}")
    else:
        print("  sin la base: control y score PENDIENTES (se mide con --con-base)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
