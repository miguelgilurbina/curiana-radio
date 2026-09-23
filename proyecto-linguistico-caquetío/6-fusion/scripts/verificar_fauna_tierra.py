# -*- coding: utf-8 -*-
"""Verifica y cuenta `6-fusion/fauna_paraguana_tierra_2026-09-22.yaml` (FA1).

Comprueba lo que el encargo fija y lo que la regla 8 exige:
  - `descripcion_visual` ≤ 220 caracteres; `desc_referente` ≤ 180; `se_oye` ≤ 80;
  - `presencia_s_xv` en {segura, probable, dudosa, excluida};
  - toda clave de obra (`fuentes`, `evidencias[].obra`, `procedencia.obra`)
    existe en `4-fuentes/bibliografia.yaml`;
  - cada candidato a referente apunta a una especie con `es_hueco: true` y
    presencia segura o probable.
Y cuenta (regla 1: las cifras del issue salen de aquí): especies por grupo,
por presencia, huecos, y cuántas llevan sonido con fuente u onomatopeya.

Uso:  python 6-fusion/scripts/verificar_fauna_tierra.py   (sale con 1 si algo falla)
"""
import collections
import io
import os
import sys

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ARCHIVO = os.path.join(R, "6-fusion", "fauna_paraguana_tierra_2026-09-22.yaml")
BIBLIO = os.path.join(R, "4-fuentes", "bibliografia.yaml")
PRESENCIAS = {"segura", "probable", "dudosa", "excluida"}
TOPES = {"descripcion_visual": 220, "desc_referente": 180, "se_oye": 80, "se_oye_sin_silabas": 80}


def _limpio(t):
    return " ".join(str(t).split())


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = yaml.safe_load(io.open(ARCHIVO, encoding="utf-8"))
    bib = yaml.safe_load(io.open(BIBLIO, encoding="utf-8"))
    obras = {o["id"] for o in bib.get("obras") or []}
    errores = []

    def obra(k, donde):
        if k and k not in obras:
            errores.append(f"{donde}: obra '{k}' no está en bibliografia.yaml")

    esp = {e["id"]: e for e in d["especies"]}
    for e in d["especies"]:
        i = e["id"]
        if e.get("presencia_s_xv") not in PRESENCIAS:
            errores.append(f"{i}: presencia '{e.get('presencia_s_xv')}'")
        dv = e.get("descripcion_visual")
        if dv and len(_limpio(dv)) > TOPES["descripcion_visual"]:
            errores.append(f"{i}: descripcion_visual {len(_limpio(dv))} > 220")
        for k in e.get("fuentes") or []:
            obra(k, i)
        for ev in e.get("evidencias") or []:
            obra(ev.get("obra"), i)
    for c in d["candidatos_referente"]:
        if not isinstance(c, dict) or "especie" not in c:
            continue
        e = esp.get(c["especie"])
        if not e:
            errores.append(f"candidato {c.get('orden')}: especie {c['especie']} no existe")
            continue
        if e.get("es_hueco") is not True or e.get("presencia_s_xv") not in ("segura", "probable"):
            errores.append(f"candidato {c['orden']}: {c['especie']} no es hueco con presencia segura/probable")
        for k in ("desc_referente", "se_oye", "se_oye_sin_silabas"):
            if c.get(k) and len(_limpio(c[k])) > TOPES[k]:
                errores.append(f"candidato {c['orden']}: {k} {len(_limpio(c[k]))} > {TOPES[k]}")
    for p in d.get("propuestas_ecologia") or []:
        obra((p.get("procedencia") or {}).get("obra"), p["id"])
    obra((d["tarantula_azul"]["distribucion"]["fuente"] or {}).get("obra"), "tarantula_azul")

    vivas = [e for e in d["especies"] if e["presencia_s_xv"] != "excluida"]
    print(f"entradas: {len(d['especies'])} (de ellas excluidas: {len(d['especies']) - len(vivas)})")
    print("por presencia:", dict(collections.Counter(e["presencia_s_xv"] for e in d["especies"])))
    print("por grupo (sin excluidas):", dict(collections.Counter(e["grupo"] for e in vivas)))
    huecos = [e for e in vivas if e.get("es_hueco") is True]
    print(f"huecos (sin voz caquetía): {len(huecos)} de {len(vivas)}; "
          f"con presencia segura o probable: {sum(e['presencia_s_xv'] in ('segura', 'probable') for e in huecos)}")
    con_fuente = [e for e in vivas if (e.get("sonido") or {}).get("fuente")]
    ono = [e for e in vivas if (e.get("sonido") or {}).get("onomatopeya_fuente")]
    print(f"sonido con fuente: {len(con_fuente)}; onomatopeya de fuente: {len(ono)} ({', '.join(e['nombre_comun'] for e in ono)})")
    print(f"candidatos a referente: {sum(1 for c in d['candidatos_referente'] if isinstance(c, dict) and 'especie' in c)}")
    print(f"propuestas a ecología: {len(d.get('propuestas_ecologia') or [])}")
    if errores:
        print("\nERRORES:")
        for e in errores:
            print("  -", e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
