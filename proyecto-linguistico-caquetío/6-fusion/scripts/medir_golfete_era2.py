#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mide por dónde entra «Golfete» al prompt del agente y al del Director en la
era 2, y contra qué canon se puede juzgar cada aparición.

    6-fusion/issues-pendientes/golfete-en-paraguana-2026-09-17.md

Regla 1: ninguna cifra de ese borrador está escrita a mano. Las imprime este
script. No llama a ninguna API, no lee `curiana_sim/.env` y no toca Supabase
(salvo `--base`, que sólo consulta el Postgres local por `docker exec`).

El caso: el día 1 de la serie B (run `3973d317`) el Director cerró con «las
canoas volverán al Golfete» y 2 de 72 respuestas dijeron «Golfete». El Golfete
de Coro ES la orilla de GUARANAO —Tacuato y El Cayude, zona ZG2, `sitios_era2
.yaml`— y NO es la de AMUAY, que pesca la costa oeste (ZA1, de Punta Cardón a
Los Taques). La pregunta medible es por cuántas vías le llega la palabra a
quien no tiene esa agua.

    python 6-fusion/scripts/medir_golfete_era2.py
    python 6-fusion/scripts/medir_golfete_era2.py --base          # + los runs
    python 6-fusion/scripts/medir_golfete_era2.py --run 3973d317  # + ese run
"""

import argparse
import collections
import json
import os
import re
import subprocess
import sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.normpath(os.path.join(_AQUI, "..", ".."))
_SIM = os.path.join(_RAIZ, "curiana_sim")

# El elenco se decide ANTES de importar curiana_agents (CLAUDE.md, trampas).
os.environ.setdefault("CURIANA_ELENCO", "era2")
sys.path.insert(0, _SIM)

TERMINOS = {
    "Golfete": re.compile(r"[Gg]olfete"),
    "Golfo": re.compile(r"[Gg]olfo(?!te)"),
    "costa oeste": re.compile(r"costa (?:oeste|del oeste)"),
    "mar": re.compile(r"(?<![\w-])[Mm]ar(?![\w-])"),
}
GOLFETE = TERMINOS["Golfete"]
CONTENEDOR = "supabase_db_curiana_sim"


def _forzar_utf8():
    """La consola de Windows es cp1252 (CLAUDE.md, trampas)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                   # pragma: no cover
        pass


def contar(textos) -> tuple:
    """(apariciones, textos que la traen) por término."""
    ap, con = collections.Counter(), collections.Counter()
    for t in textos:
        for nombre, patron in TERMINOS.items():
            n = len(patron.findall(t or ""))
            ap[nombre] += n
            con[nombre] += bool(n)
    return ap, con


def _fila(via, textos):
    ap, con = contar(textos)
    vivos = [t for t in textos if t]
    print(f"\n  {via}  ({len(vivos)} textos)")
    for nombre in TERMINOS:
        print(f"      {nombre:14} {ap[nombre]:5} apariciones en {con[nombre]:5} textos")


# ── el canon: qué agua es la de cada sitio ────────────────────────────

def canon_de_sitios():
    from curiana_mundo import sitios
    print("\n── EL CANON (6-fusion/sitios_era2.yaml) ─────────────────────────")
    print("   nodo       sitio                  zona   en una frase")
    for nombre, s in sitios().items():
        print(f"   {str(s.get('nodo') or '—'):10} {nombre:22} {str(s.get('zona_de_pesca')):6} "
              f"{str(s.get('en_una_frase'))[:70]}")
    from curiana_orchestrator_v2 import ZONAS_DE_PESCA
    print(f"\n   ZONAS_DE_PESCA (curiana_orchestrator_v2) = {ZONAS_DE_PESCA}")


# ── las vías del prompt ───────────────────────────────────────────────

def vias_del_prompt():
    from curiana_mundo import (MOMENTOS, bloque_tu_tierra, combinaciones,
                               resumen_del_mundo, restricciones_del_director,
                               sitios)
    from curiana_perfiles import cargar_perfil
    from curiana_state import estado_inicial
    import curiana_agents_era2 as A2
    import curiana_orchestrator_v2 as orch
    from curiana_eventos import (alias_del_elenco, catalogo_para_elenco,
                                 decir_para_el_mundo, elenco_era1)

    capas = cargar_perfil("era2").capas
    print("\n── LAS VÍAS DEL PROMPT (ensayo en seco, sin API) ────────────────")

    # 1. el evento semilla del día 1
    st = estado_inicial("PARAGUANÁ")
    _fila("1. estado_inicial('PARAGUANÁ').evento_del_turno", [st.evento_del_turno])
    print(f"      → {st.evento_del_turno}")

    # 2. [Tu tierra], las 126 combinaciones
    combos = combinaciones()
    bloques = {c: bloque_tu_tierra(c[0], c[1], c[2], agente="demo", dia=1, capas=capas)
               for c in combos}
    _fila(f"2. bloque_tu_tierra — {len(combos)} combinaciones (7 sitios × 3 períodos × 6 momentos)",
          list(bloques.values()))
    por_sitio = collections.Counter()
    por_momento = collections.Counter()
    for (s, p, m), b in bloques.items():
        if GOLFETE.search(b):
            por_sitio[s] += 1
            por_momento[(p, m)] += 1
    nodos = {n: s.get("nodo") for n, s in sitios().items()}
    print("      «Golfete» por sitio (de 18 combinaciones cada uno):")
    for s, n in por_sitio.most_common():
        print(f"         {str(nodos.get(s) or '—'):10} {s:22} {n:2}/18")
    print("      «Golfete» por (período, momento) — de 7 sitios cada uno:")
    for (p, m), n in sorted(por_momento.items(), key=lambda kv: -kv[1])[:4]:
        print(f"         {p}/{m:10} {n}/7")

    # 3. [El mundo] del Director
    class _E:
        def __init__(s_, e, m):
            s_.estacion, s_.momento = e, m

    mundos = {(p, m): resumen_del_mundo(_E(p, m))
              for p in ("viento", "seca_larga", "siembra") for m in MOMENTOS}
    _fila("3. resumen_del_mundo — 3 períodos × 6 momentos ([El mundo])", list(mundos.values()))
    print(f"      largo: min {min(len(b) for b in mundos.values())}, "
          f"máx {max(len(b) for b in mundos.values())} (tope 400)")
    for (p, m), b in mundos.items():
        if GOLFETE.search(b):
            print(f"      «Golfete» en {p}/{m}: {b}")
    print(f"      la línea de restricciones va en los 18 y sale del corpus por id:")
    print(f"         {restricciones_del_director()}")

    # 4. el catálogo de eventos
    era1 = elenco_era1()
    foraneas = {"caribe", "gayón", "guaycarí", "jirajara"}
    foraneos = {n for n, a in era1.items() if (a.get("etnia") or "caquetío").lower() in foraneas}
    alias = alias_del_elenco("era2")
    cot, est = catalogo_para_elenco("era2", alias, foraneos, set(era1) - set(alias) - foraneos)
    _fila(f"4. catalogo_para_elenco('era2') — {len(cot)}+{len(est)} eventos",
          [f"{e['nombre']} {e['descripcion']}" for e in cot + est])
    for e in cot + est:
        if GOLFETE.search(e["descripcion"]):
            print(f"      → {e['id']}")

    # 5. la ficha del agente y [Tu gente]
    fichas = A2.ALL_AGENTS
    _fila(f"5. system_prompt de los {len(fichas)} agentes (curiana_agents_era2, GENERADO)",
          [a.get("system_prompt") or "" for a in fichas.values()])
    por_nodo = collections.Counter(a.get("nodo") for a in fichas.values()
                                   if GOLFETE.search(a.get("system_prompt") or ""))
    print(f"      por nodo: {dict(por_nodo)}")
    _fila("6. prompt_gente() — [Tu gente], los 63", [orch.prompt_gente(a) for a in fichas.values()])

    # 7. ¿el traductor del mundo lo toca?
    frase = "Mañana el juri seguirá fuerte desde el este, las canoas volverán al Golfete."
    print(f"\n  7. decir_para_el_mundo(…, 'PARAGUANÁ') sobre la frase del Director:")
    print(f"      → {decir_para_el_mundo(frase, 'PARAGUANÁ')}")
    print("      («Golfete» NO está en MARCOS_FUERA_ERA2: es canon de Paraguaná)")


# ── el run, reconstruido pieza a pieza ────────────────────────────────

def _psql(sql: str) -> list:
    out = subprocess.run(["docker", "exec", CONTENEDOR, "psql", "-U", "postgres",
                          "-d", "postgres", "-Atc", sql],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        print(f"  ⚠ psql: {out.stderr.strip()[:200]}")
        return []
    return [l.split("|") for l in out.stdout.strip().splitlines() if l.strip()]


def medir_base():
    print("\n── EN LA BASE: los runs de la era 2 ─────────────────────────────")
    filas = _psql(
        "select left(r.id::text,8), coalesce(r.config->>'serie','(sin serie)'), count(*), "
        "count(*) filter (where ar.response_text ilike '%golfete%'), "
        "count(*) filter (where ar.response_text ~* 'golfo(?!te)'), "
        "count(*) filter (where ar.response_text ~* 'costa (oeste|del oeste)') "
        "from agent_responses ar join simulation_runs r on r.id=ar.run_id "
        "where r.config->>'elenco'='era2' group by 1,2 order by 1;")
    print("   run       serie         respuestas  Golfete  Golfo  costa oeste")
    for r in filas:
        print(f"   {r[0]:9} {r[1]:13} {r[2]:>10} {r[3]:>8} {r[4]:>6} {r[5]:>12}")

    import curiana_agents_era2 as A2
    print("\n   cada respuesta con «Golfete», con el nodo de quien la dijo:")
    for run, dia, turno, momento, agente in _psql(
            "select left(r.id::text,8), t.day, t.turn_num, t.moment, ar.agent_name "
            "from agent_responses ar join simulation_runs r on r.id=ar.run_id "
            "join turns t on t.id=ar.turn_id "
            "where r.config->>'elenco'='era2' and ar.response_text ilike '%golfete%' "
            "order by r.started_at, t.day, t.turn_num;"):
        a = A2.ALL_AGENTS.get(agente, {})
        nodo, sitio = a.get("nodo") or "?", a.get("sitio") or "?"
        juicio = "✓ su agua" if nodo == "GUARANAO" and sitio in ("Tacuato", "El Cayude") \
            else ("· su nodo, sin playa" if nodo == "GUARANAO" else "✗ NO es su agua")
        print(f"   {run} d{dia} t{turno} {momento:10} {agente:12} {nodo:9} {sitio:12} {juicio}")

    print("\n   las reflexiones del Director guardadas (curiana_sim/curiana_director.json):")
    try:
        with open(os.path.join(_SIM, "curiana_director.json"), encoding="utf-8") as f:
            for r in json.load(f).get("reflexiones") or []:
                n = len(GOLFETE.findall(r.get("texto") or ""))
                print(f"      día {r['dia']} · run {str(r.get('run_id'))[:8]} · «Golfete» ×{n}")
    except FileNotFoundError:
        print("      (no hay archivo)")


def medir_run(run8: str):
    """Reconstruye las piezas DETERMINISTAS del prompt de cada respuesta de un
    run (la ficha, [Tu gente] y [Tu tierra]) y cuenta por dónde le llegó la
    palabra. No reconstruye el léxico ni la memoria: no hacen falta."""
    from curiana_mundo import bloque_tu_tierra, resumen_del_mundo
    from curiana_perfiles import cargar_perfil
    import curiana_agents_era2 as A2
    import curiana_orchestrator_v2 as orch

    capas = cargar_perfil("era2").capas
    filas = _psql("select t.day, t.turn_num, t.moment, t.season, ar.agent_name "
                  "from agent_responses ar join turns t on t.id=ar.turn_id "
                  "join simulation_runs r on r.id=ar.run_id "
                  f"where left(r.id::text,8)='{run8}' order by t.turn_num, ar.created_at;")
    if not filas:
        print(f"\n  ⚠ sin respuestas para el run {run8}")
        return
    print(f"\n── EL RUN {run8}, PIEZA A PIEZA ({len(filas)} respuestas) ──────────")
    vias = collections.Counter()
    con_golfete = collections.Counter()
    detalle = collections.Counter()

    class _E:
        def __init__(s_, e, m):
            s_.estacion, s_.momento = e, m

    for dia, turno, momento, estacion, nombre in filas:
        a = A2.ALL_AGENTS.get(nombre)
        if not a:
            continue
        piezas = {
            "la ficha del agente (system_prompt)": a.get("system_prompt") or "",
            "[Tu gente] (ZONAS_DE_PESCA)": orch.prompt_gente(a),
            "[Tu tierra] (curiana_mundo)": bloque_tu_tierra(
                a.get("sitio"), estacion, momento, agente=nombre, dia=int(dia), capas=capas),
        }
        tocado = False
        for via, texto in piezas.items():
            if GOLFETE.search(texto):
                vias[via] += 1
                tocado = True
                if via.startswith("[Tu tierra]"):
                    detalle[(a.get("nodo"), a.get("sitio"), momento)] += 1
        if tocado:
            con_golfete[a.get("nodo")] += 1

    n = len(filas)
    print(f"\n   prompts con «Golfete» por vía (una respuesta puede llevar varias):")
    for via, k in vias.most_common():
        print(f"      {k:3}/{n}  {via}")
    print(f"      {sum(con_golfete.values()):3}/{n}  por alguna vía — por nodo: {dict(con_golfete)}")
    print("\n   [Tu tierra] con «Golfete», por (nodo, sitio, momento):")
    for (nodo, sitio, momento), k in sorted(detalle.items()):
        marca = "" if sitio in ("Tacuato", "El Cayude") else "   ← no es la orilla de este sitio"
        print(f"      {str(nodo):10} {sitio:22} {momento:10} {k:2}{marca}")
    print("\n   [El mundo] que vio el Director, turno a turno:")
    for turno, momento, estacion in sorted({(int(f[1]), f[2], f[3]) for f in filas}):
        b = resumen_del_mundo(_E(estacion, momento))
        print(f"      turno {turno} ({momento:10}) "
              f"{'← GOLFETE' if GOLFETE.search(b) else ''}")
        print(f"         {b}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", action="store_true", help="consulta también el Supabase local")
    ap.add_argument("--run", metavar="ID8", help="reconstruye las piezas del prompt de ese run")
    args = ap.parse_args()

    _forzar_utf8()
    canon_de_sitios()
    vias_del_prompt()
    if args.base or args.run:
        medir_base()
    if args.run:
        medir_run(args.run)


if __name__ == "__main__":
    main()
