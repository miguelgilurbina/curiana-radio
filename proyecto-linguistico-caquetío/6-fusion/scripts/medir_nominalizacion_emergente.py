#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la nominalización que INVENTARON los agentes
=======================================================

El otro lado de la campaña de **d21.11**. El sistema no tiene ni una regla que
derive un nombre de un verbo (sonda del canon: cero), y la comunidad lo
resolvió sola, con el posesivo sobre la raíz verbal: `ta-chaa` 'mi hacer',
`wa-jai` 'nuestro oír'. Miguel, al decidir:

    «Muy interesante cómo los agentes lo resolvieron. Eso es súper importante
    irlo dejando en nuestros sights, porque es literalmente la idea del
    proyecto: ver el surgimiento del lenguaje, un resurgimiento, una
    reimaginación.»

⚠️ **ESTO NO ES EVIDENCIA DE LO ATESTIGUADO.** Son dos secciones separadas y
no se mezclan: lo que la comunidad inventa mide el motor, no la lengua. La
medición del lado atestiguado va en `medir_nominalizador.py`.

QUÉ MIDE
--------
1. Cuántos usos y cuántas formas, con la MISMA regla que el auditor de
   morfología (`6-fusion/scripts/auditar_morfologia.py`): prefijo posesivo o
   atributivo + raíz que el lexicón declara verbal.
2. Qué prefijo, sobre qué raíces, y con qué glosa se declaró en el texto
   (los corchetes `[forma: componentes = significado]` del propio prompt).
3. Cómo se reparte por NODO (GUARANAO / AMUAY), por casa y por tier, con la
   tasa normalizada por hablantes posibles — que es como lo lee
   `analizar_nodos.py`, porque los nodos no tienen el mismo tamaño.
4. Si alguna se FIJÓ en el diccionario de koiné.

SÓLO LECTURA. `docker exec … psql` con SELECT, y con la base acotada a los
runs anteriores a la fecha de corte para que las cifras sean reproducibles
mientras se escriben runs nuevos.

    python 6-fusion/scripts/medir_nominalizacion_emergente.py
    python 6-fusion/scripts/medir_nominalizacion_emergente.py --yaml RUTA
"""

from __future__ import annotations

import argparse
import collections
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))

CONTENEDOR = "supabase_db_curiana_sim"
CORTE = "2026-09-21"          # runs con started_at < CORTE

# Las mismas tablas y las mismas clases que el auditor de morfología: la
# clase de un afijo la decide el nombre de su tabla en `curiana_lexicon`,
# no este script.
TABLAS = [
    ("REGLAS_ASPECTO",     "aspecto"),
    ("REGLAS_LOCATIVAS",   "locativo"),
    ("REGLAS_POSESIVAS",   "posesivo"),
    ("REGLAS_ATRIBUTIVAS", "atributivo"),
    ("REGLAS_NUMERO",      "número"),
    ("REGLAS_ZAVALA",      "derivativo"),
    ("REGLAS_TOPONIMICAS", "toponímico"),
    ("REGLAS_RETIRADAS",   "agentivo"),
]


def _forzar_utf8() -> None:
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass


def psql(sql: str) -> list[list[str]]:
    out = subprocess.run(
        ["docker", "exec", CONTENEDOR, "psql", "-U", "postgres", "-d",
         "postgres", "-Atc", sql], capture_output=True, text=True,
        encoding="utf-8")
    if out.returncode != 0:
        raise RuntimeError(f"psql falló: {(out.stderr or '').strip()[:400]}")
    return [ln.split("|") for ln in out.stdout.splitlines() if ln.strip()]


def slot_declarado(uso: str) -> str:
    u = (uso or "").lower()
    if "verbo_raiz" in u or "verbo raiz" in u:
        return "v_raiz"
    if "sustantivo" in u:
        return "sust"
    return "sin-declarar"


class Segmentador:
    """`nucleo_de_token()` con la lista de afijos pelados apuntada."""

    def __init__(self, L):
        self.L = L
        self.prefijos = frozenset(L._PREFIJOS_CAQ)
        self.sufijos = frozenset(L._SUFIJOS_CAQ)

    def __call__(self, tok: str):
        partes = (tok or "").strip().lower().split("-")
        pref, suf = [], []
        while len(partes) > 1 and partes[0] + "-" in self.prefijos:
            pref.append(partes[0] + "-")
            partes = partes[1:]
        while len(partes) > 1 and "-" + partes[-1] in self.sufijos:
            suf.insert(0, "-" + partes[-1])
            partes = partes[:-1]
        return pref, partes, suf

    def control(self, formas):
        malas = [f for f in formas if self(f)[1] != self.L.nucleo_de_token(f)]
        return len(malas), malas[:10]


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yaml")
    ap.add_argument("--corte", default=CORTE,
                    help="sólo runs con started_at < esta fecha")
    args = ap.parse_args(argv)

    import curiana_lexicon as L
    seg = Segmentador(L)
    VERBALES = frozenset(getattr(L, "CATS_VERBALES", {"v_raiz"}))

    clase_de, slot_de = {}, {}
    for nombre, clase in TABLAS:
        for afijo, regla in (getattr(L, nombre, {}) or {}).items():
            clase_de[afijo] = clase
            slot_de[afijo] = slot_declarado(regla.get("uso", ""))

    # ── quién es de qué nodo (la era 2) ──
    import curiana_agents_era2 as era2
    nodo_de = {nm: a["nodo"] for nm, a in era2.ALL_AGENTS.items()}
    casa_de = {nm: a.get("casa") for nm, a in era2.ALL_AGENTS.items()}
    tier_de = {nm: a.get("tier") for nm, a in era2.ALL_AGENTS.items()}
    rol_de = {nm: a.get("rol_en_la_casa") for nm, a in era2.ALL_AGENTS.items()}
    posibles = collections.Counter(nodo_de.values())

    corte = args.corte
    filtro = f"s.started_at < '{corte}'"

    # ── los usos, forma a forma ──
    filas = psql(
        "select w.word, coalesce(s.config->>'elenco','era1'), "
        "coalesce(s.config->>'serie','-'), coalesce(w.agent_name,''), "
        "count(*) from word_uses w join simulation_runs s on s.id = w.run_id "
        f"where {filtro} group by 1,2,3,4;")
    usos = [{"forma": f[0], "era": f[1], "serie": f[2], "agente": f[3],
             "n": int(f[4])} for f in filas if f[0]]

    total_usos = sum(u["n"] for u in usos)
    formas_todas = {u["forma"] for u in usos}
    desvios, ejemplos = seg.control(sorted(formas_todas))

    nomin = collections.defaultdict(
        lambda: {"usos": 0, "formas": set(), "raices": set(),
                 "por_era_serie": collections.Counter(),
                 "por_nodo": collections.Counter(),
                 "por_casa": collections.Counter(),
                 "por_tier": collections.Counter(),
                 "por_rol": collections.Counter(),
                 "agentes": set()})
    por_forma = collections.defaultdict(
        lambda: {"usos": 0, "agentes": set(), "nodos": collections.Counter()})
    usos_nom: list[dict] = []
    global_ = {"usos": 0, "formas": set(), "raices": set(),
               "agentes": set(), "por_nodo": collections.Counter(),
               "por_era_serie": collections.Counter(),
               "por_casa": collections.Counter(),
               "por_tier": collections.Counter(),
               "por_rol": collections.Counter()}

    for u in usos:
        pref, nucleo, suf = seg(u["forma"])
        if not pref:
            continue
        cat = "raiz-fuera-del-lexicon"
        for s in nucleo:
            v = L.VOCABULARIO_BASE.get(s)
            if v:
                cat = v.get("cat", "sin-cat")
                break
        if cat not in VERBALES:
            continue
        raiz = "-".join(nucleo)
        nodo = nodo_de.get(u["agente"], "(no era2)")
        for a in pref:
            if slot_de.get(a) != "sust":
                continue
            if clase_de.get(a) not in ("posesivo", "atributivo"):
                continue
            k = f"{clase_de[a]} {a}"
            d = nomin[k]
            d["usos"] += u["n"]
            d["formas"].add(u["forma"])
            d["raices"].add(raiz)
            d["por_era_serie"][f"{u['era']}/{u['serie']}"] += u["n"]
            d["por_nodo"][nodo] += u["n"]
            d["por_casa"][casa_de.get(u["agente"], "(no era2)")] += u["n"]
            d["por_tier"][str(tier_de.get(u["agente"], "-"))] += u["n"]
            d["por_rol"][rol_de.get(u["agente"], "(no era2)")] += u["n"]
            if u["agente"]:
                d["agentes"].add(u["agente"])
            global_["usos"] += u["n"]
            global_["formas"].add(u["forma"])
            global_["raices"].add(raiz)
            global_["por_nodo"][nodo] += u["n"]
            global_["por_era_serie"][f"{u['era']}/{u['serie']}"] += u["n"]
            global_["por_casa"][casa_de.get(u["agente"], "(no era2)")] += u["n"]
            global_["por_tier"][str(tier_de.get(u["agente"], "-"))] += u["n"]
            global_["por_rol"][rol_de.get(u["agente"], "(no era2)")] += u["n"]
            if u["agente"]:
                global_["agentes"].add(u["agente"])
            pf = por_forma[u["forma"]]
            pf["usos"] += u["n"]
            pf["raiz"] = raiz
            pf["prefijos"] = pf.get("prefijos", set()) | {a}
            if u["agente"]:
                pf["agentes"].add(u["agente"])
            pf["nodos"][nodo] += u["n"]
            usos_nom.append({"agente": u["agente"], "n": u["n"],
                             "forma": u["forma"], "prefijo": a})

    # ── conciliación con la cifra escrita en 2-lengua/morfologia.md §11 ──
    # §11 dice 1.107 usos de posesivo + 25 de `ka-` = 1.132. Hoy salen 960
    # sobre los MISMOS runs. La diferencia no es un error de nadie: es que
    # aquella medición corrió ANTES de que #178 repartiera las 49 raíces de
    # Zavala, y 30 de ellas dejaron de ser verbales. Se mide, no se supone.
    import lexicon_zavala as Z
    ya_no_verbales = {k for k, v in Z.CLASES_DE_RAIZ_ZAVALA.items()
                      if v.get("cat") not in VERBALES}
    fuera = getattr(L, "FUERA_DEL_HABLA", {})
    reclas = collections.Counter()
    formas_reclas = set()
    archivadas = collections.Counter()
    for u in usos:
        pref, nucleo, _ = seg(u["forma"])
        if not pref:
            continue
        cat = prim = None
        for s in nucleo:
            v = L.VOCABULARIO_BASE.get(s) or fuera.get(s)
            if v:
                cat, prim = v.get("cat"), s
                break
        for a in pref:
            if slot_de.get(a) != "sust" or clase_de.get(a) not in (
                    "posesivo", "atributivo"):
                continue
            if cat not in VERBALES and prim in ya_no_verbales:
                reclas[a] += u["n"]
                formas_reclas.add(u["forma"])
            elif (prim in fuera and fuera[prim].get("cat") in VERBALES
                  and prim not in L.VOCABULARIO_BASE):
                archivadas[prim] += u["n"]

    conciliacion = {
        "lo_que_dice_morfologia_11": "1.107 usos de ta-/ma-/wa- + 25 de ka- = 1.132",
        "lo_que_sale_hoy": global_["usos"],
        "diferencia": 1132 - global_["usos"],
        "explicada_por_178": {
            "que_es": "#178 (2026-09-20) repartió las 49 raíces de Zavala que "
                      "la heurística de tier había hecho `v_raiz` en bloque",
            "raices_que_dejaron_de_ser_verbales": len(ya_no_verbales),
            "usos_que_ya_no_cuentan": sum(reclas.values()),
            "por_prefijo": dict(reclas.most_common()),
            "formas": len(formas_reclas),
            "muestra": sorted(formas_reclas)[:12],
        },
        "aparte_lo_archivado_por_d19b": {
            "que_es": "`paa` y `kira` salieron a FUERA_DEL_HABLA y sus formas "
                      "no cuentan en ninguna de las dos mediciones",
            "usos": dict(archivadas.most_common()),
        },
        "lectura": "las dos cifras son correctas para SU estado del lexicón. "
                   "La de hoy es la del canon en main, y es la que debe "
                   "escribirse en §11 — con `ka-juri` fuera, que es "
                   "justamente lo que d21.5 quería",
    }

    # ── ¿alguna se fijó en la koiné? ──
    fijadas = psql(
        "select k.form, k.concepto_id, coalesce(k.descripcion,''), "
        "k.fijada_dia, k.soporte, substring(k.run_id::text,1,8) "
        "from koine_lexicon k join simulation_runs s on s.id = k.run_id "
        f"where {filtro};")
    koine = [{"forma": f[0], "concepto": f[1], "descripcion": f[2],
              "dia": f[3], "soporte": f[4], "run": f[5]} for f in fijadas]
    koine_nominal = [k for k in koine if k["forma"] in global_["formas"]]

    # ── ¿qué dijeron que significaban? los corchetes del texto ──
    import re
    glosas = {}
    if global_["formas"]:
        ins = ",".join("'" + f.replace("'", "''") + "'"
                       for f in sorted(global_["formas"]))
        sql = ("select r.response_text from agent_responses r "
               "join simulation_runs s on s.id = r.run_id "
               f"where {filtro} and r.response_text ~* "
               "'\\[[a-zà-ÿ-]+ *:' limit 4000;")
        textos = psql(sql)
        CORCHETE = re.compile(r"\[([a-zà-ÿ\-]+)\s*:\s*([^\]=]*)=\s*([^\]]+)\]",
                              re.I)
        for t in textos:
            for m in CORCHETE.finditer("|".join(t)):
                forma = m.group(1).strip().lower()
                if forma in global_["formas"]:
                    glosas.setdefault(forma, collections.Counter())[
                        m.group(3).strip()[:60]] += 1

    doc = {
        "medicion": "nominalizacion-emergente",
        "fecha": "2026-09-21",
        "responde_a": "6-fusion/decisiones_tanda_2026-09-21.yaml §d21.11",
        "aviso": "lo que la comunidad inventa NO es evidencia de lo "
                 "atestiguado: son dos secciones y no se mezclan",
        "base": {
            "corte": f"simulation_runs.started_at < '{corte}'",
            "por_que": "se están escribiendo runs nuevos mientras se mide; sin "
                       "el corte las cifras no serían reproducibles",
            "usos_en_word_uses": total_usos,
            "formas_distintas": len(formas_todas),
        },
        "control_de_segmentacion": {
            "formas_comprobadas": len(formas_todas),
            "desvios_contra_nucleo_de_token": desvios,
            "ejemplos": ejemplos,
            "verde": desvios == 0,
        },
        "total": {
            "usos": global_["usos"],
            "formas": len(global_["formas"]),
            "raices_verbales_distintas": len(global_["raices"]),
            "agentes_distintos": len(global_["agentes"]),
            "por_era_y_serie": dict(global_["por_era_serie"].most_common()),
            "por_nodo": dict(global_["por_nodo"].most_common()),
            "hablantes_posibles_por_nodo": dict(posibles),
            "tasa_por_hablante_posible": {
                n: round(global_["por_nodo"][n] / posibles[n], 1)
                for n in posibles if posibles[n]},
            "por_tier": dict(global_["por_tier"].most_common()),
            "por_casa": dict(global_["por_casa"].most_common()),
        },
        # ⚠️ El titular de morfologia.md §11 —«la nominalización con el
        # posesivo»— suma cuatro prefijos, y desde d21.5 dos de ellos NO son
        # posesivos: `ka-` es atributivo y `ma-` privativo. Son DOS invenciones
        # distintas y conviene contarlas aparte antes de nombrarlas.
        "dos_patrones": {
            "posesivo_sobre_verbo": {
                "que_es": "`ta-`/`wa-` + raíz verbal: «mi hacer», «nuestro "
                          "oír». ESTO es nominalización: el posesivo exige un "
                          "nombre y lo que hay debajo es un verbo",
                "usos": sum(d["usos"] for k, d in nomin.items()
                            if k.startswith("posesivo")),
                "formas": len({f for k, d in nomin.items()
                               if k.startswith("posesivo") for f in d["formas"]}),
            },
            "atributivo_o_privativo_sobre_verbo": {
                "que_es": "`ma-`/`ka-` + raíz verbal: «ma-panaa» sin saber, "
                          "«ma-awa» sin beber. NO es nominalización: es "
                          "predicación negativa sobre un verbo, y el privativo "
                          "está declarado para NOMBRES (d21.5). Es una segunda "
                          "invención, y nadie la ha nombrado todavía",
                "usos": sum(d["usos"] for k, d in nomin.items()
                            if k.startswith("atributivo")),
                "formas": len({f for k, d in nomin.items()
                               if k.startswith("atributivo") for f in d["formas"]}),
            },
        },
        "por_prefijo": [
            {"prefijo": k, "usos": d["usos"], "formas": len(d["formas"]),
             "raices": len(d["raices"]), "agentes": len(d["agentes"]),
             "por_nodo": dict(d["por_nodo"].most_common()),
             "por_era_y_serie": dict(d["por_era_serie"].most_common()),
             "muestra": sorted(d["formas"])[:12]}
            for k, d in sorted(nomin.items(), key=lambda x: -x[1]["usos"])],
        "formas": [
            {"forma": f, "raiz": d.get("raiz"), "usos": d["usos"],
             "prefijos": sorted(d.get("prefijos", [])),
             "glosa_de_la_raiz": (L.VOCABULARIO_BASE.get(d.get("raiz"), {})
                                  .get("sig")),
             "capa_de_la_raiz": (L.VOCABULARIO_BASE.get(d.get("raiz"), {})
                                 .get("fuente")),
             "cat_de_la_raiz": (L.VOCABULARIO_BASE.get(d.get("raiz"), {})
                                .get("cat")),
             "hablantes": len(d["agentes"]),
             "por_nodo": dict(d["nodos"].most_common()),
             "glosa_declarada_mas_frecuente":
                 (glosas.get(f).most_common(1)[0][0] if glosas.get(f) else None)}
            for f, d in sorted(por_forma.items(), key=lambda x: -x[1]["usos"])],
        "raices_por_capa": dict(collections.Counter(
            (L.VOCABULARIO_BASE.get(r, {}).get("fuente", "?"))
            for r in global_["raices"]).most_common()),
        "conciliacion_con_morfologia_11": conciliacion,
        "roles_que_mas_la_usan": dict(
            collections.Counter(global_["por_rol"]).most_common(12)),
        # Ojo al leer esto: es conteo CRUDO. Quien más turnos habló más dice,
        # y el Manaure habla en todos los turnos en que sale. No es una tasa.
        # Ordenado por usos y, a igualdad, por nombre: un empate resuelto por
        # el orden de iteración de un set hace que el volcado no se reproduzca
        # byte a byte, y un generado que no se reproduce no se puede auditar.
        "agentes_que_mas_la_usan_era2": [
            {"agente": a, "usos": n, "nodo": nodo_de.get(a),
             "rol": rol_de.get(a), "tier": tier_de.get(a)}
            for a, n in sorted(
                ((a, sum(u["n"] for u in usos_nom if u["agente"] == a))
                 for a in sorted({u["agente"] for u in usos_nom} & set(nodo_de))),
                key=lambda x: (-x[1], x[0]))[:10]],
        "koine": {
            "entradas_fijadas_en_la_base": len(koine),
            "de_ellas_nominalizacion_emergente": len(koine_nominal),
            "detalle": koine_nominal,
        },
    }

    print("═" * 70)
    print("NOMINALIZACIÓN EMERGENTE — lo que inventaron los agentes")
    print("═" * 70)
    print(f"base: {total_usos} usos, {len(formas_todas)} formas "
          f"(runs anteriores a {corte})")
    print(f"control de segmentación: {desvios} desvíos → "
          f"{'verde' if desvios == 0 else 'ROJO'}")
    t = doc["total"]
    print(f"\nnominalización emergente: {t['usos']} usos en {t['formas']} formas, "
          f"{t['raices_verbales_distintas']} raíces verbales, "
          f"{t['agentes_distintos']} hablantes")
    print("  por prefijo:")
    for p in doc["por_prefijo"]:
        print(f"    {p['prefijo']:<16} {p['usos']:>5} usos  {p['formas']:>3} formas "
              f" {p['raices']:>3} raíces   {sorted(p['muestra'])[:4]}")
    print(f"  por era y serie: {t['por_era_y_serie']}")
    print(f"  por nodo: {t['por_nodo']}  (hablantes posibles {t['hablantes_posibles_por_nodo']})")
    print(f"  tasa por hablante posible: {t['tasa_por_hablante_posible']}")
    print(f"  por tier: {t['por_tier']}")
    dp = doc["dos_patrones"]
    print(f"\n  DOS patrones, no uno:")
    print(f"    posesivo (ta-/wa-) sobre verbo  → "
          f"{dp['posesivo_sobre_verbo']['usos']} usos, "
          f"{dp['posesivo_sobre_verbo']['formas']} formas  ← esto es nominalización")
    print(f"    atributivo/privativo (ma-/ka-)  → "
          f"{dp['atributivo_o_privativo_sobre_verbo']['usos']} usos, "
          f"{dp['atributivo_o_privativo_sobre_verbo']['formas']} formas  ← esto NO lo es")
    print(f"\n  raíces por capa: {doc['raices_por_capa']}")
    print("\n  las 15 formas más usadas:")
    for f in doc["formas"][:15]:
        g = f["glosa_declarada_mas_frecuente"]
        print(f"    {f['forma']:<22} {f['usos']:>4} usos  {f['hablantes']:>2} hablantes"
              f"  raíz «{(f['glosa_de_la_raiz'] or '?')[:30]}»"
              + (f"  → «{g}»" if g else ""))
    c = doc["conciliacion_con_morfologia_11"]
    print(f"\n  conciliación con morfologia.md §11: dice 1.132, hoy salen "
          f"{c['lo_que_sale_hoy']} (diferencia {c['diferencia']})")
    print(f"    explicada por #178: {c['explicada_por_178']['usos_que_ya_no_cuentan']}"
          f" usos en {c['explicada_por_178']['formas']} formas "
          f"({c['explicada_por_178']['raices_que_dejaron_de_ser_verbales']} raíces)")
    print(f"    muestra: {c['explicada_por_178']['muestra'][:6]}")
    print(f"\n  koiné: {doc['koine']['entradas_fijadas_en_la_base']} entradas "
          f"fijadas en la base; de ellas nominalización emergente: "
          f"{doc['koine']['de_ellas_nominalizacion_emergente']}")
    for k in doc["koine"]["detalle"]:
        print(f"    {k['forma']:<22} {k['concepto']}  día {k['dia']} "
              f"soporte {k['soporte']}  run {k['run']}")

    if args.yaml:
        sys.path.insert(0, AQUI)
        from medir_nominalizador import volcar
        with open(args.yaml, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(volcar(doc)) + "\n")
        print(f"\n→ {args.yaml}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
