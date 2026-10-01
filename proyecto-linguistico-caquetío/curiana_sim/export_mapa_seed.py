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
  (`cruce.en_canon`), **también los de lectura descartada**: en el canon
  «descartado» es la LECTURA, no el lugar. Jayana es descartado por no tener
  glosa, y existe (Nueva Jayama, junto a Amuaicito). Miguel, 2026-10-01: que
  entren todos; los castellanos y los que Esteves atribuye a otra lengua
  también, porque esa atribución es lectura suya, no dato, y la esfera es
  multilingüe. Van como `sin` (sin lectura) con el `motivo` del canon.
* Fuera los cruces `aproximado` que el barrido dejó marcados para revisar
  (`revisar: true`): son candidatos, no lugares. Entran `exacto`,
  `forma-viva` y `parcial`.
* El **nivel** es el del canon y mide la LECTURA del nombre —A: la ecuación
  cierra con morfemas atestiguados · B: exige un morfema despejado · C:
  plausible · sin: no hay lectura—, no si el nombre existe: el nombre está en
  una fuente y en el mapa de hoy. La página lo dibuja con la gramática del
  trazo del manual.

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
# El nivel del canon «descartado» se publica como `sin` (sin lectura).
SIN_LECTURA = "sin"
ORDEN = NIVELES + (SIN_LECTURA,)


def motivo_sin_lectura(razon: Optional[str]) -> str:
    """Por qué un topónimo no tiene lectura, en una línea, desde la `razon` del
    canon (sus descartes se escriben con un puñado de fórmulas). Lo que no
    encaja en ninguna dice lo mínimo: que la fuente no da glosa."""
    r = (razon or "").lower()
    if "no es indígena" in r:
        return "Esteves lo da por no indígena"
    if "otra lengua" in r:
        return "Esteves lo atribuye a otra lengua (lectura suya)"
    if "transparente en castellano" in r or "colectivo castellano" in r or "formación española" in r:
        return "nombre castellano"
    if "vivo en el mapa" in r:
        return "vivo en el mapa; ninguna fuente impresa lo trae"
    if "ninguna segmentación" in r:
        return "la fuente lo glosa, pero no se segmenta"
    return "la fuente no da glosa"


def tipo_de_cruce(como: Optional[str]) -> str:
    """`aproximado:borobo` → `aproximado`."""
    return (como or "").split(":", 1)[0]


def id_en_canon(en_canon: Optional[str]) -> Optional[str]:
    """`toponimo-151 · nivel C` → `toponimo-151`."""
    if not en_canon:
        return None
    return str(en_canon).split("·", 1)[0].strip() or None


TOPE_GLOSA = 120


def recortar(texto: str, tope: int = TOPE_GLOSA) -> str:
    """Corta en la última palabra entera antes del tope; una cita que se corta
    sigue cerrando sus comillas."""
    texto = " ".join(texto.split())
    if len(texto) <= tope:
        return texto
    corte = texto[:tope].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"
    if corte.startswith("«") and "»" not in corte:
        corte += "»"
    return corte


def glosa_de(t: dict, nivel: str) -> Optional[str]:
    """La glosa que muestra el mapa, corta: nuestra lectura si la hay (es la
    que el nivel mide); si no, la de la fuente, recortada.

    Sin lectura no hay glosa: en los descartados `glosa_fuente` es la nota de
    trabajo de la campaña (referente, censo, rutas de archivos de 6-fusion/),
    no una glosa, y no se publica. El porqué va en `motivo`."""
    if nivel == SIN_LECTURA:
        return None
    for clave in ("glosa_reconstruida", "glosa_fuente"):
        v = t.get(clave)
        if v:
            return recortar(str(v))
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
        nivel = t.get("nivel")
        if nivel == "descartado":
            nivel = SIN_LECTURA
        elif nivel not in NIVELES:
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
            "nivel": nivel,
            "motivo": motivo_sin_lectura(t.get("razon")) if nivel == SIN_LECTURA else None,
            "cruce": como,
            "glosa": glosa_de(t, nivel),
            "obra": proc.get("obra") if isinstance(proc, dict) else None,
        })
    puntos.sort(key=lambda p: (ORDEN.index(p["nivel"]), p["forma"] or "", p["nombre_en_el_mapa"] or ""))
    return puntos, avisos


def resumir(puntos: list[dict], canon: dict[str, dict]) -> dict:
    ids = {p["id"] for p in puntos}
    por_nivel = {n: len({p["id"] for p in puntos if p["nivel"] == n}) for n in ORDEN}
    por_region: dict[str, int] = {}
    for p in puntos:
        por_region[p["region"]] = por_region.get(p["region"], 0) + 1
    return {
        "puntos": len(puntos),
        "toponimos_con_lugar": len(ids),
        "toponimos_canon": len(canon),
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
    print(f"  ✓ {r['puntos']} puntos · {r['toponimos_con_lugar']} de {r['toponimos_canon']} "
          f"topónimos del canon con lugar · por nivel {r['por_nivel']}")
    print(f"  ✓ por región {r['puntos_por_region']}")
    for a in seed["avisos"]:
        print(f"  ⚠  {a}")
    print(f"\n{os.path.relpath(SALIDA, REPO)} escrito")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
