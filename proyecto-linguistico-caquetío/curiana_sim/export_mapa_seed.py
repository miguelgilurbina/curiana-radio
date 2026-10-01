# -*- coding: utf-8 -*-
"""
Exporta el MAPA de la portada de Kaketiana: los topónimos del canon que tienen
lugar en el mapa vivo.

Por qué existe
--------------
El manual de Kaketiana (design_handoff_kaketiana, portada) pone un mapa al lado
del hero: el territorio del wiki. Miguel eligió el 2026-09-30 que muestre los
**topónimos del canon** (`2-lengua/toponimos.yaml`), ubicados con el mapa vivo
(`6-fusion/toponimos_mapa_kaketiana.yaml`, generado por `barrer_mapa.py` desde
OpenStreetMap). Este exportador cruza los dos y escribe un JSON estático; la
página no lee ni el canon ni OSM.

Qué entra
---------
* Un punto por rasgo del mapa vivo cuyo cruce apunta a un topónimo del canon
  (`cruce.en_canon`) que **no** esté descartado.
* Fuera los cruces `aproximado` que el barrido dejó marcados para revisar
  (`revisar: true`): son candidatos, no lugares. Entran `exacto`,
  `forma-viva` y `parcial`.
* El **nivel** es el del canon y mide la LECTURA del nombre —A: la ecuación
  cierra con morfemas atestiguados · B: exige un morfema despejado · C:
  plausible—, no si el nombre existe: el nombre está en una fuente y en el
  mapa de hoy. La página lo dibuja con la gramática del trazo del manual.

Nada se escribe a mano: el resumen (cuántos topónimos del canon tienen lugar,
por nivel y por región) se mide aquí.

Uso:
    python export_mapa_seed.py
"""
from __future__ import annotations

import io
import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional

import yaml

PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(PROYECTO)
CANON = os.path.join(PROYECTO, "2-lengua", "toponimos.yaml")
MAPA_VIVO = os.path.join(PROYECTO, "6-fusion", "toponimos_mapa_kaketiana.yaml")
SALIDA = os.path.join(REPO, "content", "wiki", "mapa.json")

VERSION = 1
CRUCES_QUE_ENTRAN = ("exacto", "forma-viva", "parcial")
NIVELES = ("A", "B", "C")


def tipo_de_cruce(como: Optional[str]) -> str:
    """`aproximado:borobo` → `aproximado`."""
    return (como or "").split(":", 1)[0]


def id_en_canon(en_canon: Optional[str]) -> Optional[str]:
    """`toponimo-151 · nivel C` → `toponimo-151`."""
    if not en_canon:
        return None
    return str(en_canon).split("·", 1)[0].strip() or None


def glosa_de(t: dict) -> Optional[str]:
    """La glosa que la página muestra: la impresa si la hay, si no la nuestra."""
    for clave in ("glosa_fuente", "glosa_reconstruida"):
        v = t.get(clave)
        if v:
            return str(v).strip()
    return None


def construir_puntos(entradas: list[dict], canon: dict[str, dict]) -> tuple[list[dict], list[str]]:
    puntos, avisos, vistos = [], [], set()
    for e in entradas:
        cruce = e.get("cruce") or {}
        tid = id_en_canon(cruce.get("en_canon"))
        if not tid:
            continue
        t = canon.get(tid)
        if t is None:
            avisos.append(f"{e.get('forma')}: apunta a {tid}, que no está en el canon")
            continue
        if t.get("nivel") not in NIVELES:
            continue
        como = tipo_de_cruce(cruce.get("como"))
        if como not in CRUCES_QUE_ENTRAN or e.get("revisar"):
            continue
        lat, lon = round(float(e["lat"]), 5), round(float(e["lon"]), 5)
        clave = (tid, e.get("forma"), round(lat, 3), round(lon, 3))
        if clave in vistos:
            continue
        vistos.add(clave)
        proc = t.get("procedencia") or {}
        puntos.append({
            "id": tid,
            "forma": t.get("forma"),
            "nombre_en_el_mapa": e.get("forma"),
            "tipo": e.get("tipo"),
            "lat": lat,
            "lon": lon,
            "region": e.get("region"),
            "nivel": t["nivel"],
            "cruce": como,
            "glosa": glosa_de(t),
            "obra": proc.get("obra") if isinstance(proc, dict) else None,
        })
    puntos.sort(key=lambda p: (NIVELES.index(p["nivel"]), p["forma"] or "", p["nombre_en_el_mapa"] or ""))
    return puntos, avisos


def resumir(puntos: list[dict], canon: dict[str, dict]) -> dict:
    ids = {p["id"] for p in puntos}
    vigentes = [t for t in canon.values() if t.get("nivel") in NIVELES]
    por_nivel = {n: len({p["id"] for p in puntos if p["nivel"] == n}) for n in NIVELES}
    por_region: dict[str, int] = {}
    for p in puntos:
        por_region[p["region"]] = por_region.get(p["region"], 0) + 1
    return {
        "puntos": len(puntos),
        "toponimos_con_lugar": len(ids),
        "toponimos_vigentes": len(vigentes),
        "por_nivel": por_nivel,
        "puntos_por_region": dict(sorted(por_region.items(), key=lambda kv: -kv[1])),
    }


def construir_seed(mapa: dict, canon_yaml: dict) -> dict:
    canon = {t["id"]: t for t in canon_yaml.get("toponimos") or []}
    puntos, avisos = construir_puntos(mapa.get("entradas") or [], canon)
    meta = mapa.get("meta") or {}
    return {
        "version": VERSION,
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fuente_mapa": meta.get("fuente_mapa"),
        "licencia": meta.get("licencia"),
        "mapa_vivo_generado": meta.get("generado"),
        "resumen": resumir(puntos, canon),
        "puntos": puntos,
        "avisos": avisos,
    }


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def main() -> int:
    with open(MAPA_VIVO, encoding="utf-8") as f:
        mapa = yaml.safe_load(f)
    with open(CANON, encoding="utf-8") as f:
        canon_yaml = yaml.safe_load(f)
    seed = construir_seed(mapa, canon_yaml)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
        f.write("\n")
    r = seed["resumen"]
    print(f"  ✓ {r['puntos']} puntos · {r['toponimos_con_lugar']} de {r['toponimos_vigentes']} "
          f"topónimos vigentes con lugar · por nivel {r['por_nivel']}")
    print(f"  ✓ por región {r['puntos_por_region']}")
    for a in seed["avisos"]:
        print(f"  ⚠  {a}")
    print(f"\n{os.path.relpath(SALIDA, REPO)} escrito")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
