#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mide el lote de Esteves del 2026-09-22 (parcela M6, tercera campaña).

Lee la propuesta curada a mano (`6-fusion/toponimos_esteves_lote_2026-09-22.yaml`,
que NO lleva cifras: regla 1) y escribe la medición en
`6-fusion/medicion_lote_esteves_2026-09-22.yaml` (GENERADO):

  1. COBERTURA: que cada nombre de la cola del índice (por_procesar) esté
     tratado —entrada, descarte o corrección— y cuáles de la cola ya estaban en
     el canon sin que el índice lo supiera.
  2. RECUENTOS: por nivel, por grupo de descarte, por filiación declarada,
     por cómo se verificó, fauna y flora.
  3. FORMANTES: cuántos nombres muestran cada formante de la consigna y en
     cuántos lo glosa la fuente (nivel A/B/C) frente a los descartados.
  4. EL LEXICÓN, voz por voz: dónde está cada voz que el lote usa, con qué
     capa y con qué siglas de Zavala. Una voz cuya única cita es Zavala (E) NO
     es atestación independiente de Esteves: (E) ES Esteves (Zavala p. 64).
     Se mide también cuántas voces caquetías ATESTIGUADAS de todo el lexicón
     están en ese caso.
  5. EL MAPA VIVO: cada nombre contra `toponimos_mapa_kaketiana.yaml`, exacto
     o aproximado (la permutación laxa de barrer_mapa.py), con coordenadas.

Uso:
    python 6-fusion/scripts/medir_lote_esteves_2026-09-22.py
    python 6-fusion/scripts/medir_lote_esteves_2026-09-22.py --check
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))

PROPUESTA = os.path.join(RAIZ, "6-fusion", "toponimos_esteves_lote_2026-09-22.yaml")
SALIDA = os.path.join(RAIZ, "6-fusion", "medicion_lote_esteves_2026-09-22.yaml")
INDICE = os.path.join(RAIZ, "6-fusion", "toponimos_esteves_indice.yaml")
CANON = os.path.join(RAIZ, "2-lengua", "toponimos.yaml")
MAPA = os.path.join(RAIZ, "6-fusion", "toponimos_mapa_kaketiana.yaml")

# Obras que, citadas en `notas` de una voz, la hacen independiente de Esteves.
OTRAS_OBRAS = ("alvarado", "medina", "van buurt", "gatschet", "oliver", "arcaya",
               "oviedo", "jahn", "angulo")


def _forzar_utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def plano(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def leer(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ── 1-2. cobertura y recuentos ─────────────────────────────────────────────

def nombres_tratados(p):
    ent = {plano(e["forma"]): e for e in p["entradas"]}
    desc = {}
    for grupo, g in p["descartes"].items():
        for f in g["formas"]:
            desc[plano(f["forma"])] = (grupo, f)
    return ent, desc


def cobertura(p, idx, canon):
    ent, desc = nombres_tratados(p)
    alias = {plano(k): plano(v) for k, v in (p["meta"].get("indice_vs_cabecera") or {}).items()}
    corr = {plano(x) for x in p["meta"].get("cubiertas_en_correcciones") or []}
    canon_formas = {plano(t["forma"]): t["id"] for t in canon}
    cola = [x["forma"] for x in idx["por_procesar"]]
    sin_tratar, ya_en_canon, por_cabecera = [], [], []
    for f in cola:
        k = plano(f)
        k2 = alias.get(k, k)
        if k2 != k:
            por_cabecera.append(f"{f} → {k2}")
        if k in canon_formas:
            ya_en_canon.append(f"{f} ({canon_formas[k]})")
        if k2 not in ent and k2 not in desc and k not in corr:
            sin_tratar.append(f)
    return {
        "cola_del_indice": len(cola),
        "tratadas": len(cola) - len(sin_tratar),
        "sin_tratar": sin_tratar,
        "ya_en_canon_segun_la_forma": ya_en_canon,
        "cabecera_distinta_del_indice": por_cabecera,
    }


def recuentos(p):
    ent, desc = nombres_tratados(p)
    niveles = collections.Counter(e["nivel"] for e in p["entradas"])
    niveles["descartado"] = len(desc)
    nuevas = [e for e in p["entradas"] if not e.get("ya_en_canon") and not e.get("posible_canon")]
    fil = collections.Counter(e.get("filiacion_declarada") or "ninguna (caquetío por omisión)" for e in p["entradas"])
    for grupo, g in p["descartes"].items():
        for f in g["formas"]:
            if f.get("estrato"):
                fil[f["estrato"]] += 1
            elif f.get("clase"):
                fil[f"no indígena según Esteves: {f['clase']}"] += 1
    ver = collections.Counter()
    for e in p["entradas"]:
        ver["imagen" if str(e.get("verificado", "")).startswith("imagen") else "ocr"] += 1
    return {
        "por_nivel": dict(sorted(niveles.items())),
        "entradas_glosadas": len(p["entradas"]),
        "de_ellas_cambio_sobre_una_entrada_del_canon": len(p["entradas"]) - len(nuevas),
        "descartes_por_grupo": {g: len(v["formas"]) for g, v in p["descartes"].items()},
        "por_filiacion_declarada": dict(fil.most_common()),
        "entradas_glosadas_por_verificacion": dict(ver),
        "fauna": len(p.get("fauna") or []),
        "fauna_con_sonido": sum(1 for f in p.get("fauna") or [] if f.get("sonido")),
        "fauna_con_especie": sum(1 for f in p.get("fauna") or [] if f.get("especie_probable")),
        "flora": len(p.get("flora") or []),
        "correcciones": len(p.get("correcciones") or []),
    }


# ── 3. formantes ───────────────────────────────────────────────────────────

def formantes(p):
    c = collections.defaultdict(lambda: {"glosado_por_la_fuente_o_cierra": [], "en_descartes": []})
    for e in p["entradas"]:
        for f in e.get("formantes") or []:
            c[f]["glosado_por_la_fuente_o_cierra"].append(e["forma"])
    # en los descartes el formante no está anotado: se mide por la forma
    patrones = {"gua": r"gua$|gua[^a-z]", "bana": r"ban[ao]$", "bakoa": r"b?acoa$", "ebo": r"ebo$",
                "uco": r"[uú][ct]o$", "ure": r"ure$", "are": r"are$", "ey-ay": r"[ae][yií]$",
                "kiva": r"qui[bv]a", "ima": r"i?ma$", "ana": r"ana$", "aco": r"aco$", "uru": r"[uú]r[ou]$"}
    for grupo, g in p["descartes"].items():
        for f in g["formas"]:
            k = plano(f["forma"])
            for nom, pat in patrones.items():
                if re.search(pat, k):
                    c[nom]["en_descartes"].append(f["forma"])
    out = {}
    for nom in sorted(c):
        v = c[nom]
        out[nom] = {"en_entradas": len(v["glosado_por_la_fuente_o_cierra"]),
                    "en_descartes": len(v["en_descartes"]),
                    "entradas": v["glosado_por_la_fuente_o_cierra"],
                    "descartes": v["en_descartes"]}
    return out


# ── 4. el lexicón ──────────────────────────────────────────────────────────

def indice_lexicon():
    import curiana_lexicon as L
    V = L.VOCABULARIO_BASE
    idx = collections.defaultdict(list)
    for k, v in V.items():
        if not isinstance(v, dict):
            continue
        for f in {k, v.get("forma_fuente") or k}:
            idx[plano(f)].append((k, v))
    return V, idx


def siglas(notas: str):
    return re.findall(r"#\s?\d+[^()]{0,40}\(([A-Z+ ]{1,20})\)", notas or "")


def sigla_no_e(notas: str) -> bool:
    """¿Alguna cita de Zavala con sigla distinta de E? (criterio ESTRICTO)"""
    return any(s.strip() != "E" for grupo in siglas(notas) for s in grupo.split("+"))


def obras_en_notas(notas: str) -> list:
    """Otras obras NOMBRADAS en la nota. Nombrar no es apoyar: la nota de
    `saruro` nombra a Oliver para decir que NO lo tiene, y la de `kari` a van
    Buurt citando a Esteves. Por eso esto se lista aparte y no decide."""
    n = plano(notas or "")
    return [o for o in OTRAS_OBRAS if o in n]


def independiente(notas: str) -> bool:
    return sigla_no_e(notas)


def lexicon(p):
    V, idx = indice_lexicon()
    voces = collections.OrderedDict()
    for e in p["entradas"]:
        for v in e.get("voces") or []:
            voces.setdefault(v, []).append(e["forma"])
    filas = []
    for v, formas in voces.items():
        hits = [(k, d) for k, d in idx.get(plano(v), []) if str(d.get("fuente", "")).startswith("caquet")]
        if not hits:
            filas.append({"voz": v, "en": formas, "lexicon": None})
            continue
        k, d = hits[0]
        notas = str(d.get("notas", ""))
        sg = siglas(notas)
        filas.append({"voz": v, "en": formas, "lexicon": k, "capa": d.get("fuente"),
                      "siglas_zavala": ["+".join(x.split()) for x in sg] or None,
                      "zavala_con_sigla_no_E": sigla_no_e(notas),
                      "otras_obras_nombradas_en_la_nota": obras_en_notas(notas) or None})
    # magnitud en todo el lexicón: voces atestiguadas cuya(s) cita(s) de
    # Zavala son todas (E). Dos cortes: sin mirar la nota, y quitando las que
    # nombran otra obra (que puede ser apoyo o no: se revisa a mano).
    atest = [(k, d) for k, d in V.items() if isinstance(d, dict) and d.get("fuente") == "caquetío-atestiguado"]
    solo_e = [k for k, d in atest if siglas(str(d.get("notas", ""))) and not sigla_no_e(str(d.get("notas", "")))]
    solo_e_sin_otra = [k for k in solo_e if not obras_en_notas(str(V[k].get("notas", "")))]
    en_lex = [f for f in filas if f["lexicon"]]
    con_sigla = [f for f in en_lex if f["siglas_zavala"]]
    return {
        "voces_del_lote": len(filas),
        "en_el_lexicon_caquetio": len(en_lex),
        "con_cita_de_zavala": len(con_sigla),
        "de_ellas_solo_sigla_E": sum(1 for f in con_sigla if not f["zavala_con_sigla_no_E"]),
        "de_ellas_solo_sigla_E_y_sin_otra_obra_en_la_nota": sum(
            1 for f in con_sigla if not f["zavala_con_sigla_no_E"] and not f["otras_obras_nombradas_en_la_nota"]),
        "fuera_del_lexicon": [f["voz"] for f in filas if not f["lexicon"]],
        "todo_el_lexicon": {
            "caquetio_atestiguado": len(atest),
            "cuyas_citas_de_zavala_son_todas_E": len(solo_e),
            "y_sin_otra_obra_nombrada_en_la_nota": len(solo_e_sin_otra),
            "nota": ("sigla (E) = Juan Esteves (Zavala p. 64): para un topónimo de Esteves es control de "
                     "transmisión, no segunda atestación. Nombrar otra obra en la nota no es apoyo por sí "
                     "solo (saruro nombra a Oliver para decir que no lo tiene)."),
        },
        "por_voz": filas,
    }


# ── 5. el mapa vivo ────────────────────────────────────────────────────────

def mapa(p):
    import barrer_mapa as B
    E = leer(MAPA)["entradas"]
    pal = []
    for e in E:
        prop = B.nombre_propio(e["forma"])
        pal.append((e, [B.clave(w) for w in B.palabras(prop)] + [B.clave(prop)]))
    ent, desc = nombres_tratados(p)
    filas, exactos, aprox, cero = [], 0, 0, []
    for k0, src in list(ent.items()) + list(desc.items()):
        forma = src["forma"] if isinstance(src, dict) else src[1]["forma"]
        k, kl = B.clave(forma), B.laxa(B.clave(forma))
        hits = []
        for e, ws in pal:
            como = None
            if k in ws:
                como = "exacto"
            elif len(k) >= 5:
                mx = 1 if len(k) < 8 else 2
                for w in ws:
                    if len(w) >= 5 and B._lev(kl, B.laxa(w), mx) <= mx:
                        como = f"aproximado:{w}"
                        break
            if como:
                hits.append({"osm": e["forma"], "tipo": e["tipo"], "region": e["region"],
                             "lat": round(e["lat"], 4), "lon": round(e["lon"], 4), "como": como})
        if any(h["como"] == "exacto" for h in hits):
            exactos += 1
        elif hits:
            aprox += 1
        else:
            cero.append(forma)
        filas.append({"forma": forma, "osm": hits or None})
    return {"nombres": len(filas), "con_exacto": exactos, "solo_aproximado": aprox,
            "sin_nada_en_osm_2026": len(cero), "ceros": cero,
            "nota": "un cero en OSM no es un cero en el terreno (regla 6): depende de quién mapeó",
            "por_nombre": filas}


# ── salida ─────────────────────────────────────────────────────────────────

def medir():
    p, idx, canon = leer(PROPUESTA), leer(INDICE), leer(CANON)["toponimos"]
    return {
        "meta": {
            "generado_por": "6-fusion/scripts/medir_lote_esteves_2026-09-22.py",
            "editar_a_mano": "no — se edita la propuesta o el script y se regenera",
            "propuesta": "6-fusion/toponimos_esteves_lote_2026-09-22.yaml",
        },
        "cobertura": cobertura(p, idx, canon),
        "recuentos": recuentos(p),
        "formantes": formantes(p),
        "lexicon": lexicon(p),
        "mapa_vivo": mapa(p),
    }


def volcar(d) -> str:
    cab = ("# GENERADO por 6-fusion/scripts/medir_lote_esteves_2026-09-22.py — no editar a mano.\n"
           "# La medición del lote de Esteves del 2026-09-22; la propuesta es\n"
           "# 6-fusion/toponimos_esteves_lote_2026-09-22.yaml.\n")
    return cab + yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110)


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="¿la medición escrita está al día?")
    a = ap.parse_args(argv)
    texto = volcar(medir())
    if a.check:
        with open(SALIDA, encoding="utf-8") as fh:
            ok = fh.read() == texto
        print("✓ al día" if ok else "✗ desfasada: regenerar")
        return 0 if ok else 1
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    d = yaml.safe_load(texto)
    print(f"✓ {os.path.relpath(SALIDA, RAIZ)}")
    print("  cobertura:", {k: v for k, v in d["cobertura"].items() if not isinstance(v, list)},
          "sin tratar:", d["cobertura"]["sin_tratar"])
    print("  niveles:", d["recuentos"]["por_nivel"], "descartes:", d["recuentos"]["descartes_por_grupo"])
    lx = d["lexicon"]
    print("  lexicón:", {k: v for k, v in lx.items() if not isinstance(v, (list, dict))}, lx["todo_el_lexicon"])
    mv = d["mapa_vivo"]
    print("  mapa:", {k: v for k, v in mv.items() if not isinstance(v, (list, str))})
    return 0


if __name__ == "__main__":
    sys.exit(main())
