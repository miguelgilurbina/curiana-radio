#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mide y valida la campaña de fauna del MAR (FA3, 2026-09-22):

    6-fusion/fauna_paraguana_mar_2026-09-22.yaml

Regla 1: las cifras de `meta.medido` las calcula este script. Regla 8: toda
`obra` citada existe en 4-fuentes/bibliografia.yaml.

Comprueba:
  1. ids únicos (especies y candidatos a referente)
  2. topes de largo: descripcion_visual ≤ 220, desc_referente ≤ 180, se_oye ≤ 80
  3. presencia_s_xv ∈ {segura, probable, dudosa, excluida}
  4. toda clave `obra` (a cualquier profundidad) existe en la bibliografía
  5. todo `hueco_canon` existe en 3-mundo/corpus/ecologia.yaml
  6. toda voz caquetía citada (`nombres.caquetio.clave`) existe en
     curiana_lexicon.VOCABULARIO_BASE y su `capa` es la del lexicón
  7. los `silabeo_propuesto` van etiquetados `hipotetico`, y avisa si una
     forma propuesta coincide con una clave del lexicón (homónimo)
  8. los candidatos a referente apuntan a especies que existen

No llama a ninguna API, no lee curiana_sim/.env, no toca la base.

    python 6-fusion/scripts/medir_fauna_mar.py            # valida y compara con meta.medido
    python 6-fusion/scripts/medir_fauna_mar.py --conteos  # sólo imprime el bloque medido
"""

import argparse
import collections
import io
import os
import re
import sys

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
YAML_FA3 = os.path.join(RAIZ, "6-fusion", "fauna_paraguana_mar_2026-09-22.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")
ECOLOGIA = os.path.join(RAIZ, "3-mundo", "corpus", "ecologia.yaml")
sys.path.insert(0, os.path.join(RAIZ, "curiana_sim"))

PRESENCIAS = ("segura", "probable", "dudosa", "excluida")
TOPES = {"descripcion_visual": 220, "desc_referente": 180, "se_oye": 80}


def _forzar_utf8():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def _obras(nodo, acc):
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k == "obra" and isinstance(v, str):
                acc.append(v)
            else:
                _obras(v, acc)
    elif isinstance(nodo, list):
        for v in nodo:
            _obras(v, acc)
    return acc


def medir(d):
    esp = d.get("especies") or []
    m = collections.OrderedDict()
    m["especies"] = len(esp)
    m["por_grupo"] = dict(sorted(collections.Counter(e["grupo"] for e in esp).items()))
    m["por_presencia"] = dict(sorted(collections.Counter(e["presencia_s_xv"] for e in esp).items()))
    m["es_hueco"] = sum(1 for e in esp if e.get("es_hueco"))
    m["con_nombre_caquetio"] = sum(
        1 for e in esp if isinstance((e.get("nombres") or {}).get("caquetio"), dict)
        and (e["nombres"]["caquetio"] or {}).get("clave"))
    m["con_sonido_documentado"] = sum(
        1 for e in esp if isinstance((e.get("sonido") or {}).get("onomatopeya_documentada"), dict))
    m["candidatos_referente"] = len(d.get("candidatos_referente") or [])
    m["propuestas_ecologia"] = len(d.get("propuestas_ecologia") or [])
    m["obras_citadas"] = len(set(_obras(d, [])))
    return m


def validar(d):
    errores, avisos = [], []
    biblio = yaml.safe_load(open(BIBLIO, encoding="utf-8"))
    ids_biblio = {o["id"] for o in biblio["obras"]}
    eco = yaml.safe_load(open(ECOLOGIA, encoding="utf-8"))
    ids_eco = {h["id"] for sec in ("entradas", "huecos_lexicos") for h in (eco.get(sec) or [])}
    try:
        from curiana_lexicon import VOCABULARIO_BASE
    except Exception as e:  # el lexicón no carga: se avisa y se sigue
        VOCABULARIO_BASE = {}
        avisos.append(f"no se pudo importar curiana_lexicon ({e}): sin chequeo 6")

    esp = d.get("especies") or []
    vistos = collections.Counter(e["id"] for e in esp)
    errores += [f"id repetido: {i}" for i, n in vistos.items() if n > 1]
    ids_esp = set(vistos)

    for e in esp:
        i = e["id"]
        if e.get("presencia_s_xv") not in PRESENCIAS:
            errores.append(f"{i}: presencia_s_xv inválida ({e.get('presencia_s_xv')})")
        dv = e.get("descripcion_visual")
        if dv and len(dv) > TOPES["descripcion_visual"]:
            errores.append(f"{i}: descripcion_visual de {len(dv)} > 220")
        if dv is None and e.get("presencia_s_xv") != "excluida":
            avisos.append(f"{i}: sin descripcion_visual")
        hc = e.get("hueco_canon")
        if hc and hc not in ids_eco:
            errores.append(f"{i}: hueco_canon {hc} no está en ecologia.yaml")
        caq = (e.get("nombres") or {}).get("caquetio")
        if isinstance(caq, dict) and caq.get("clave") and VOCABULARIO_BASE:
            v = VOCABULARIO_BASE.get(caq["clave"])
            if v is None:
                errores.append(f"{i}: la voz caquetía `{caq['clave']}` no está en VOCABULARIO_BASE")
            elif caq.get("capa") and v.get("fuente") != caq["capa"]:
                errores.append(f"{i}: `{caq['clave']}` es {v.get('fuente')} en el lexicón, aquí dice {caq['capa']}")
        sil = (e.get("sonido") or {}).get("silabeo_propuesto")
        if isinstance(sil, dict):
            if sil.get("etiqueta") != "hipotetico":
                errores.append(f"{i}: silabeo_propuesto sin etiqueta hipotetico")
            for tok in re.findall(r"[a-záéíóúüñ]+", (sil.get("forma") or "").lower()):
                if tok in VOCABULARIO_BASE:
                    avisos.append(f"{i}: el silabeo «{tok}» es homónimo de una clave del lexicón "
                                  f"({VOCABULARIO_BASE[tok].get('sig', '')[:40]})")

    cand = d.get("candidatos_referente") or []
    vc = collections.Counter(c["id"] for c in cand)
    errores += [f"candidato repetido: {i}" for i, n in vc.items() if n > 1]
    for c in cand:
        for k in ("desc_referente", "se_oye"):
            t = c.get(k)
            if t and len(t) > TOPES[k]:
                errores.append(f"candidato {c['id']}: {k} de {len(t)} > {TOPES[k]}")
        for e in c.get("especie") or []:
            if e not in ids_esp:
                errores.append(f"candidato {c['id']}: especie {e} no existe")
        hc = c.get("hueco_canon")
        if hc and hc not in ids_eco:
            errores.append(f"candidato {c['id']}: hueco_canon {hc} no está en ecologia.yaml")

    for o in sorted(set(_obras(d, []))):
        if o not in ids_biblio:
            errores.append(f"obra sin ficha en la bibliografía: {o}")
    return errores, avisos


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--conteos", action="store_true")
    a = ap.parse_args()
    d = yaml.safe_load(open(YAML_FA3, encoding="utf-8"))
    m = medir(d)
    if a.conteos:
        print(yaml.safe_dump({"medido": dict(m)}, allow_unicode=True, sort_keys=False, width=100))
        return 0
    errores, avisos = validar(d)
    declarado = (d.get("meta") or {}).get("medido") or {}
    for k, v in m.items():
        if declarado.get(k) != v:
            errores.append(f"meta.medido.{k}: declarado {declarado.get(k)} ≠ medido {v}")
    for a_ in avisos:
        print("aviso:", a_)
    for e in errores:
        print("ERROR:", e)
    print(f"{len(errores)} errores, {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
