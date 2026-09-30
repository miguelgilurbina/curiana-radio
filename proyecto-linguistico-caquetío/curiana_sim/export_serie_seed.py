# -*- coding: utf-8 -*-
"""
Exporta una SERIE de la era 2 —dos brazos, una cadena de días cada uno— para
la página del experimento (`/kaketiana/experimento`).

Por qué existe
--------------
`export_runs_index.py` publica runs sueltos de la era 1: una fila por run. En
la era 2 un run es UN día, y el experimento son dos cadenas de treinta días con
las mismas semillas —una con escena y otra sin ella— que sólo significan algo
juntas. Este exportador escribe esa comparación como un JSON estático, con el
mismo molde que el resto: lee la base **local** y la página en producción no la
toca nunca.

Nada se escribe a mano (regla 1 del proyecto). Cada cifra sale de un sitio que
ya existe y que la bitácora usa:

* **la serie y el veredicto** — `curiana_cadena` (las `koine_metrics` de la
  cadena unidas por día, y el mismo veredicto que emite el orquestador);
* **la brecha entre pueblos y las formas que cruzan** — `analizar_nodos`
  (`analizar_cadena`, la lectura acumulada-emergente de `analizar_distancia` y
  la clasificación de formas por nodo);
* **las palabras fijadas** — `koine_lexicon`;
* **las disputas que quedaron abiertas** — el `curiana_koine.json` guardado al
  cerrar cada brazo (`--estado-escena` / `--estado-control`). La competencia no
  vive en la base: si no se pasa el estado, la clave va `null` y la página no
  la dibuja. El estado se comprueba contra la cadena (`run_anterior` tiene que
  ser la hoja) para no publicar la competencia de otro brazo.

Qué cadena es cada brazo
------------------------
Se miran todas las cadenas de la era 2 cuyos runs declaran `serie` = la pedida.
Por brazo (con escena / sin escena) se queda la que más días cerrados tiene. Las
demás se AVISAN: la serie `era2-base` tiene un control cortado en el día 4 por
falta de saldo de la API (`f40e5f34` → `41a5148a`), que se rehízo desde el día 1
y no es parte de la comparación.

Uso
---
    python export_serie_seed.py --serie era2-base \\
        --estado-escena  C:/Users/migue/curiana_estado_backup/era2-base-escena \\
        --estado-control C:/Users/migue/curiana_estado_backup/era2-base-control

Escribe `content/simulador/series/<serie>.json`.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

import analizar_nodos as an
import curiana_cadena as cc

PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(PROYECTO)                            # la raíz del sitio Next
DIR_SALIDA = os.path.join(REPO, "content", "simulador", "series")

VERSION = 1


# ══════════════════════════════════════════════════════════════════════
# I. PIEZAS PURAS (sin base) — lo que prueban los tests
# ══════════════════════════════════════════════════════════════════════

def dias_de_capubana(dias: list[int], cada: int) -> list[int]:
    """Los días de reunión en el cerro: la regla de `curiana_escena.es_dia_de_capubana`."""
    if cada <= 0:
        return []
    return [d for d in dias if d > 0 and d % cada == 0]


def _media(xs: list[float]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def partir_por_capubana(serie: list[dict], clave: str, capubana: list[int]) -> dict:
    """Media de `clave` los días de Capubana y el resto.

    Se aplica también al brazo SIN escena con los días del brazo con escena: es
    el placebo. Allí no hay reunión, así que si los días 3, 6, 9… también bajaran
    el efecto no sería del Capubana."""
    en = set(capubana)
    return {
        "capubana": _media([p[clave] for p in serie if p["dia"] in en]),
        "resto": _media([p[clave] for p in serie if p["dia"] not in en]),
        "n_capubana": sum(1 for p in serie if p["dia"] in en and p[clave] is not None),
    }


def minimo(serie: list[dict], clave: str) -> Optional[dict]:
    puntos = [p for p in serie if p.get(clave) is not None]
    if not puntos:
        return None
    p = min(puntos, key=lambda p: (p[clave], p["dia"]))
    return {"dia": p["dia"], "valor": p[clave]}


def unir_serie(serie_koine: list[tuple], distancia: list[dict]) -> list[dict]:
    """Una fila por día: las tres lecturas del motor y dos de `analizar_nodos`.

    * `brecha` — la acumulada-emergente, la que la bitácora cita para la
      tendencia: distancia media entre pares de pueblos distintos menos la de
      pares del mismo pueblo. Positiva = dentro de cada pueblo se habla más
      parecido que entre ellos.
    * `emergente_dia` y `brecha_dia` — la lectura emergente de SÓLO ese día
      (sin acumular), reconstruida de `word_uses`. Es la que mide el efecto de
      un día suelto, como el de Capubana. Se compara sólo consigo misma
      (`analizar_nodos._distancia_global`), nunca con la cifra del motor.
    """
    por_dia = {}
    for fila in distancia:
        acum = fila.get("acumulada_emergente") or {}
        del_dia = fila.get("emergente") or {}
        por_dia[int(fila["dia"])] = {
            "brecha": acum.get("brecha"),
            "emergente_dia": an._distancia_global(del_dia) if del_dia else None,
            "brecha_dia": del_dia.get("brecha"),
        }
    vacio = {"brecha": None, "emergente_dia": None, "brecha_dia": None}
    return [{"dia": d, "acumulada": a, "ventana": v, "emergente": e,
             **por_dia.get(d, vacio)}
            for (d, a, v, e) in serie_koine]


def dias_que_bajan(serie: list[dict], clave: str, capubana: list[int]) -> dict:
    """De los días de Capubana, cuántos quedan por debajo del día anterior."""
    valor = {p["dia"]: p.get(clave) for p in serie}
    comparables = [d for d in capubana
                   if valor.get(d) is not None and valor.get(d - 1) is not None]
    return {"bajan": sum(1 for d in comparables if valor[d] < valor[d - 1]),
            "de": len(comparables)}


def resumen_de_formas(formas: list[dict]) -> dict:
    """El mismo recuento que imprime `analizar_nodos` bajo la tabla de formas."""
    clasificables = [r for r in formas
                     if r["clase"] not in ("poco-atestiguada", "sin-usos")]
    return {
        "emergentes": len(formas),
        "clasificables": len(clasificables),
        "cruzaron": sum(1 for r in clasificables if r["cruzo"]),
        "no_cruzaron": sum(1 for r in clasificables
                           if not r["cruzo"] and not r["acunacion_multinodo"]),
        "nacidas_en_los_dos": sum(1 for r in clasificables if r["acunacion_multinodo"]),
    }


def competencia_del_estado(koine_estado: dict, orden: list[str]) -> dict:
    """Las disputas del `curiana_koine.json`: fijadas y abiertas, con sus rivales.

    Las formas van TAL CUAL las guardó el motor, asteriscos de markdown incluidos
    (defecto anotado en la bitácora: `**x` y `x` reparten soporte). Quien las
    muestra decide cómo limpiarlas; aquí no se corrige el dato."""
    comp = (koine_estado or {}).get("competencia") or {}
    refs = comp.get("referentes") or {}
    posicion = {c: i for i, c in enumerate(orden)}
    filas = []
    for concepto, r in refs.items():
        variantes = sorted(((f, round(float(s), 2)) for f, s in
                            (r.get("variantes") or {}).items()),
                           key=lambda x: (-x[1], x[0]))
        filas.append({
            "concepto": concepto,
            "orden": posicion.get(concepto),
            "descripcion": r.get("desc") or "",
            "fijada": r.get("fijada"),
            "fijada_dia": r.get("fijada_dia"),
            "n_variantes": len(variantes),
            "rivales": [{"forma": f, "soporte": s} for f, s in variantes[:3]],
        })
    filas.sort(key=lambda f: (f["orden"] is None, f["orden"] or 0, f["concepto"]))
    return {
        "umbral": comp.get("umbral"),
        "soporte_minimo": comp.get("soporte_minimo"),
        "referentes": len(filas),
        "fijados": sum(1 for f in filas if f["fijada"]),
        # Todos, fijados y abiertos, en el orden en que el mundo los presentó.
        "lista": filas,
    }


def clave_de_brazo(escena: bool) -> str:
    return "escena" if escena else "control"


# ══════════════════════════════════════════════════════════════════════
# II. LA BASE
# ══════════════════════════════════════════════════════════════════════

def cadenas_de_la_serie(serie: str) -> tuple[dict[str, list[dict]], list[str]]:
    """{brazo: cadena} con la cadena más larga de cada brazo, y los avisos."""
    avisos: list[str] = []
    por_brazo: dict[str, list[list[dict]]] = {}
    for cadena in an.cadenas_era2():
        if not cadena or any((r.get("serie") or "") != serie for r in cadena):
            continue
        brazo = clave_de_brazo((cadena[-1].get("escena") or "").lower() == "true")
        por_brazo.setdefault(brazo, []).append(cadena)
    elegidas = {}
    for brazo, cadenas in por_brazo.items():
        cadenas.sort(key=lambda c: (-sum(1 for r in c if int(r["total_days"] or 0) > 0),
                                    c[0]["started_at"]))
        elegidas[brazo] = cadenas[0]
        for otra in cadenas[1:]:
            cerrados = sum(1 for r in otra if int(r["total_days"] or 0) > 0)
            avisos.append(
                f"brazo {brazo}: se descarta la cadena {otra[0]['id'][:8]} → "
                f"{otra[-1]['id'][:8]} ({len(otra)} runs, {cerrados} cerrados); "
                f"la comparación usa la más larga")
    return elegidas, avisos


def huella_de_cadena(run_ids: list[str]) -> dict:
    filas = an.q(f"""
        select coalesce(config->>'motor_commit','') as commit,
               coalesce(config->>'motor_sucio','') as sucio,
               coalesce(model,'') as modelo
        from simulation_runs where id in ({an._lista_sql(run_ids)})
    """)
    return {
        "modelos": sorted({f["modelo"] for f in filas if f["modelo"]}),
        "commits": sorted({f["commit"][:8] for f in filas if f["commit"]}),
        "sucios": sum(1 for f in filas if f["sucio"].lower() == "true"),
        "sin_huella": sum(1 for f in filas if f["sucio"] == ""),
    }


def habla_de_cadena(run_ids: list[str]) -> dict:
    f = an.q(f"""
        select count(*) as respuestas, count(distinct agent_name) as agentes
        from agent_responses where run_id in ({an._lista_sql(run_ids)})
    """)[0]
    return {"respuestas": int(f["respuestas"]), "agentes": int(f["agentes"])}


def fijadas_de_cadena(run_ids: list[str]) -> list[dict]:
    filas = an.q(f"""
        select concepto_id, coalesce(descripcion,'') as descripcion, form,
               fijada_dia, n_variantes, soporte
        from koine_lexicon where run_id in ({an._lista_sql(run_ids)})
        order by fijada_dia, concepto_id
    """)
    return [{"concepto": f["concepto_id"], "descripcion": f["descripcion"],
             "forma": f["form"],
             "dia": int(f["fijada_dia"]) if f["fijada_dia"] else None,
             "n_variantes": int(f["n_variantes"]) if f["n_variantes"] else None,
             "soporte": round(float(f["soporte"]), 2) if f["soporte"] else None}
            for f in filas]


def leer_estado(carpeta: Optional[str], hoja: str, brazo: str,
                avisos: list[str]) -> Optional[dict]:
    """El `curiana_koine.json` del brazo, sólo si su estado cierra ESTA cadena."""
    if not carpeta:
        return None
    try:
        with open(os.path.join(carpeta, "curiana_state.json"), encoding="utf-8") as f:
            estado = json.load(f)
        with open(os.path.join(carpeta, "curiana_koine.json"), encoding="utf-8") as f:
            koine = json.load(f)
    except OSError as e:
        avisos.append(f"brazo {brazo}: no se pudo leer el estado ({e}); "
                      f"la competencia va null")
        return None
    if estado.get("run_anterior") != hoja:
        avisos.append(
            f"brazo {brazo}: el estado de {carpeta} cierra el run "
            f"{str(estado.get('run_anterior'))[:8]}, no la hoja {hoja[:8]}: "
            f"su competencia NO se publica")
        return None
    return competencia_del_estado(koine, estado.get("referentes_introducidos") or [])


def brazo_de(cadena: list[dict], estado: Optional[str],
             avisos: list[str]) -> tuple[dict, dict]:
    run_ids = [r["id"] for r in cadena]
    hoja = run_ids[-1]
    escena = (cadena[-1].get("escena") or "").lower() == "true"
    brazo = clave_de_brazo(escena)
    avisos_cadena: list[str] = []
    serie_koine = cc.serie_koine_de_cadena(cc.LectorSQL(), hoja, avisos=avisos_cadena)
    avisos.extend(f"brazo {brazo}: {a}" for a in avisos_cadena)
    etiqueta, codigo, mensaje, d_ini, d_fin = cc.veredicto(serie_koine)

    analisis = an.analizar_cadena(cadena)
    serie = unir_serie(serie_koine, analisis["distancia"])
    return {
        "clave": brazo,
        "escena": escena,
        "capubana_cada": int(cadena[-1].get("capubana_cada") or 0),
        "runs": {"primero": run_ids[0][:8], "ultimo": hoja[:8], "n": len(run_ids)},
        "dias": len(serie),
        "semillas": [cadena[0].get("semilla"), cadena[-1].get("semilla")],
        "motor": huella_de_cadena(run_ids),
        **habla_de_cadena(run_ids),
        "serie": serie,
        "veredicto": {"lectura": etiqueta, "codigo": codigo, "mensaje": mensaje,
                      "inicio": d_ini, "fin": d_fin},
        "emergente_min": minimo(serie, "emergente"),
        "formas": resumen_de_formas(analisis["formas"]),
        "fijadas": fijadas_de_cadena(run_ids),
        "competencia": leer_estado(estado, hoja, brazo, avisos),
    }, analisis["elenco"]


def construir_seed(serie: str, estados: dict[str, Optional[str]]) -> dict:
    cadenas, avisos = cadenas_de_la_serie(serie)
    if not cadenas:
        raise SystemExit(f"No hay cadenas de la serie {serie!r} en la base")
    brazos, elenco = [], None
    for clave in ("escena", "control"):
        if clave not in cadenas:
            avisos.append(f"la serie no tiene brazo {clave}")
            continue
        b, elenco = brazo_de(cadenas[clave], estados.get(clave), avisos)
        brazos.append(b)

    con_escena = next((b for b in brazos if b["escena"]), None)
    cada = con_escena["capubana_cada"] if con_escena else 0
    dias = sorted({p["dia"] for b in brazos for p in b["serie"]})
    capubana = dias_de_capubana(dias, cada)
    commits = sorted({c for b in brazos for c in b["motor"]["commits"]})
    if len(commits) > 1:
        avisos.append(f"los brazos corrieron con motores distintos: {', '.join(commits)}")

    return {
        "version": VERSION,
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "serie": serie,
        "elenco": {"total": elenco["total"], "por_nodo": elenco["por_nodo"]} if elenco else None,
        "motor": commits,
        "brazos": brazos,
        "capubana": {
            "cada": cada,
            "dias": capubana,
            # El placebo: los mismos días, en los dos brazos.
            # Lecturas de un solo día: el Capubana es un día, no una tendencia.
            "emergente_dia": {b["clave"]: partir_por_capubana(b["serie"], "emergente_dia", capubana)
                              for b in brazos},
            "brecha_dia": {b["clave"]: partir_por_capubana(b["serie"], "brecha_dia", capubana)
                           for b in brazos},
            "bajan": {b["clave"]: dias_que_bajan(b["serie"], "emergente_dia", capubana)
                      for b in brazos},
        },
        "avisos": avisos,
    }


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def informe(seed: dict, salida: str) -> None:
    for b in seed["brazos"]:
        v = b["veredicto"]
        comp = b["competencia"]
        print(f"  ✓ {b['clave']:<8} {b['runs']['primero']} → {b['runs']['ultimo']} · "
              f"{b['dias']} días · {b['respuestas']} respuestas · {b['agentes']} agentes · "
              f"motor {', '.join(b['motor']['commits'])} "
              f"({b['motor']['sucios']} sucios)")
        print(f"             [{v['lectura']}] {v['inicio']} → {v['fin']}: {v['mensaje']}")
        print(f"             fijadas {len(b['fijadas'])}"
              + (f" · competencia {comp['fijados']}/{comp['referentes']}" if comp else
                 " · competencia: sin estado")
              + f" · formas que no cruzaron {b['formas']['no_cruzaron']}")
    cap = seed["capubana"]
    for clave, e in cap["emergente_dia"].items():
        b, n = cap["brecha_dia"][clave], cap["bajan"][clave]
        print(f"  ✓ Capubana ({clave}): emergente del día {e['capubana']} vs {e['resto']}; "
              f"brecha del día {b['capubana']} vs {b['resto']}; "
              f"bajan {n['bajan']} de {n['de']}")
    for aviso in seed["avisos"]:
        print(f"  ⚠  {aviso}")
    print(f"\n{os.path.relpath(salida, REPO)} escrito")


def main(argv: Optional[list[str]] = None) -> int:
    # Las cadenas de la era 2 se leen con el elenco de la era 2: sin esto
    # `analizar_nodos` da una falsa alarma de semillas (lo anotó la serie base
    # el 2026-09-28). Va aquí y no al importar el módulo, para que importarlo
    # —los tests lo hacen— no cambie el elenco de nadie más.
    os.environ.setdefault("CURIANA_ELENCO", "era2")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serie", required=True, help="la etiqueta sellada en config.serie")
    ap.add_argument("--estado-escena", metavar="CARPETA",
                    help="estado guardado al cerrar el brazo con escena")
    ap.add_argument("--estado-control", metavar="CARPETA",
                    help="estado guardado al cerrar el brazo de control")
    ap.add_argument("--salida", metavar="RUTA",
                    help=f"por defecto {os.path.relpath(DIR_SALIDA, REPO)}/<serie>.json")
    args = ap.parse_args(argv)

    seed = construir_seed(args.serie, {"escena": args.estado_escena,
                                       "control": args.estado_control})
    salida = args.salida or os.path.join(DIR_SALIDA, f"{args.serie}.json")
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
        f.write("\n")
    informe(seed, salida)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
