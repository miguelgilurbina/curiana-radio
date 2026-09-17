# -*- coding: utf-8 -*-
"""
Exporta la ESCENA de un run (o de una cadena) para el visor de repetición.

PR 10 «escena: el mapa» del plan de
`6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md`
(§5b «Verlo», §8 fila 10), decisión 10 de Miguel del 2026-09-17: «Sí, sobre el
mapa real, en /kaketiana, estático, leyendo `presencias`».

Qué es y qué NO es
------------------
Esto **no simula**: lee. La escena ya está decidida y guardada —`presencias`
pone a los 63 en un lugar cada momento del día, no sólo a los 12 que hablan— y
aquí sólo se junta con lo que se dijo en cada sitio y se escribe como JSON
estático. Mismo molde que los otros `export_*_seed.py`: se lee de Supabase
**local** y se commitea el JSON; la página en producción no toca la base nunca
(cero egress, el sitio es 100 % estático).

Y es además un **guardián**: el día que el Director narre que las canoas
volvieron al Golfete y en el mapa no haya nadie en el Golfete, se ve de un
vistazo.

De dónde sale cada cosa
-----------------------
* **Los lugares y sus coordenadas** — de
  `6-fusion/escena_por_lugar_propuesta_2026-09-17.yaml`, que ya resolvió los 29
  lugares de los tres períodos contra `sitios_era2.yaml`, `elenco_era2.yaml`,
  `estructura_social_era2.yaml` y el `mapa_vivo` de `2-lengua/toponimos.yaml`:
  **8 con punto propio, 16 heredando el de su aldea, 2 áreas y 3 caminos**. Esa
  resolución no se rehace aquí, se lee (§5b: «lo que falta para afinarlo son
  puntos de detalle, y ésos no los tiene el canon — no se inventan»).
* **El nodo de cada lugar** — medido del `§ocupacion` de esa misma tabla: un
  lugar es del nodo de quien lo trabaja, y si lo tocan los dos es `compartido`.
  No se programa ninguna frontera.
* **Quién estaba dónde** — de `presencias` (`presencias_de` /
  `presencias_de_cadena`, que paginan: 378 filas por día contra el
  `max_rows`=1000 de PostgREST).
* **Qué dijo ahí** — de `agent_responses`, con el texto **recortado a un tope
  declarado** (`TOPE_TEXTO`, que va escrito en el propio JSON). El lugar de una
  respuesta lo manda `presencias`; `agent_responses.lugar` es el atajo
  desnormalizado y si los dos discrepan se AVISA en vez de elegir en silencio.

Esquema del JSON (versión 1)
----------------------------
```
{
  "version": 1,
  "generado": "2026-09-17T…Z",        # ISO-8601 UTC
  "vacio": false,                      # true si no hay ni una presencia
  "tope_texto": 220,                   # caracteres por intervención
  "run": {
    "id8": "0193873d",                 # el run HOJA (el último de la cadena)
    "run_id": "0193873d-…",
    "cadena": ["a1b2c3d4", "0193873d"],# id8 raíz→hoja; [id8] si no es cadena
    "started_at": "…" | null,
    "dias": [1, 2],
    "n_turnos": 12,
    "n_agentes": 63,
    "n_presencias": 756
  },
  "lugares": [{
    "id": "Tacuato:orilla",            # la clave que usan `presencias.lugar`
    "nombre": "Tacuato · orilla",      # etiqueta mecánica, no prosa nueva
    "sitio": "Tacuato",
    "locacion": "orilla" | null,
    "nodo": "GUARANAO" | "AMUAY" | "compartido" | null,
    "tipo": "propio"|"heredado"|"zona"|"camino"|"sin-coordenada",
    "lat": 11.708, "lon": -69.841,     # null si "sin-coordenada"
    "puntos": [[lat, lon], …] | null,  # zona: los puntos del área
                                       # camino: los dos extremos, si el canon
                                       #         nombra el par
    "compartido": false,               # declarado entre nodos (Capubana, el
                                       # camino Moruy–Caseto)
    "por_que": "…" | null              # qué lo declara compartido
  }],
  "turnos": [{
    "i": 0,                            # índice en el deslizador
    "run": "0193873d",
    "dia": 1, "turno": 1, "momento": "amanecer",
    "n_presencias": 63,
    "escenas": [{
      "lugar": "Tacuato:orilla",
      "n": 5,                          # cuánta gente hay — el tamaño del punto
      "por_nodo": {"GUARANAO": 5},
      "contacto": false,               # los DOS nodos aquí, a la vez
      "presentes": [{"agente": "Birokoa", "nodo": "GUARANAO", "hablo": true}, …],
      "dichos": [{"agente": "Birokoa", "nodo": "GUARANAO",
                  "texto": "…", "recortado": true}]
    }]
  }],
  "avisos": ["…"]                      # lo que no cuadra, dicho y no tapado
}
```

Un JSON **vacío** es el mismo objeto con `vacio: true`, `turnos: []` y el
catálogo de `lugares` completo: el mapa se dibuja igual y la página dice que
todavía no ha corrido ningún run con escena (ningún run lo ha hecho aún — la
tabla existe desde el 2026-09-17 y está sin filas).

Uso
---
```bash
python export_escena_seed.py --run 0193873d            # un run
python export_escena_seed.py --run 0193873d --cadena   # él y sus antecesores
python export_escena_seed.py --sin-base                # sólo el catálogo (seed vacío)
python export_escena_seed.py --run 0193873d --salida ruta/al.json
python export_escena_seed.py --tope 280                # otro recorte del texto
```
"""
import argparse
import io
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Optional

import yaml
from dotenv import load_dotenv

# Cada entrypoint carga su .env: leer os.environ no basta (CLAUDE.md, trampas).
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import get_db  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
PROYECTO = os.path.dirname(AQUI)                 # proyecto-linguistico-caquetío/
REPO = os.path.dirname(PROYECTO)                 # la raíz del sitio Next

RUTA_PROPUESTA = os.path.join(
    PROYECTO, "6-fusion", "escena_por_lugar_propuesta_2026-09-17.yaml")
DIR_SALIDA = os.path.join(REPO, "content", "simulador", "escena")

VERSION = 1

# El recorte de cada intervención, en caracteres. Va DECLARADO aquí y escrito en
# el JSON (`tope_texto`) para que el visor pueda decir que lo que enseña está
# cortado; el texto entero vive en la base, que es su sitio.
TOPE_TEXTO = 220

# Filas por página de PostgREST. `presencias` pasa el max_rows=1000 en tres días
# y `agent_responses` en dos; sus lectores paginan o truncan en silencio.
PAGINA = 1000

# Los caminos cuyos DOS extremos nombra el canon. La decisión de Miguel del
# 2026-09-17 (p2, «B») declara compartido «el camino Moruy–Caseto, que el elenco
# llama la alianza y que el mapa dice que es el par más cercano de todos
# (7,6 km)». Es el único par nombrado: los demás caminos se dibujan en su sitio
# de origen y sin destino, porque inventarles uno sería inventar el mapa.
CAMINOS_CON_PAR: dict[str, tuple[str, str]] = {
    "camino:Moruy": ("Moruy", "Caseto"),
    "camino:Caseto": ("Caseto", "Moruy"),
}
POR_QUE_CAMINO = ("decisión de Miguel 2026-09-17 p2 «B»: el camino Moruy–Caseto, "
                  "«la alianza», compartido entre nodos")


def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 y esto imprime ⚠ ✓ · y acentos."""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


# ══════════════════════════════════════════════════════════════════════
# El catálogo de lugares — se LEE de la tabla derivada, no se recalcula
# ══════════════════════════════════════════════════════════════════════

def cargar_propuesta(ruta: str = RUTA_PROPUESTA) -> dict:
    """La tabla de escena por lugar, tal cual la dejó
    `6-fusion/scripts/derivar_escena_por_lugar.py --yaml`."""
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def nodo_por_lugar(propuesta: dict) -> dict[str, str]:
    """El nodo de cada lugar, MEDIDO de `§ocupacion`: quien lo trabaja.

    Un lugar al que van los dos nodos —en cualquier período y cualquier
    momento— sale como `compartido`. No hay frontera declarada en ninguna
    parte: el nodo de un lugar es un resultado del reparto, no un dato escrito
    (§0.2 del diseño: «los nodos no se programan: salen del mapa»).
    """
    nodos: dict[str, set[str]] = defaultdict(set)
    for por_lugar in (propuesta.get("ocupacion") or {}).values():
        for lugar, momentos in (por_lugar or {}).items():
            for celda in (momentos or {}).values():
                nodos[lugar].update((celda.get("por_nodo") or {}).keys())
    return {
        lugar: (sorted(vistos)[0] if len(vistos) == 1 else "compartido")
        for lugar, vistos in nodos.items() if vistos
    }


def partir_id(lugar: str) -> tuple[str, Optional[str]]:
    """`"Tacuato:orilla"` → `("Tacuato", "orilla")`; `"Moruy"` → `("Moruy", None)`."""
    if ":" not in lugar:
        return lugar, None
    sitio, locacion = lugar.split(":", 1)
    return sitio, locacion


def etiqueta_de(lugar: str, tipo: str) -> str:
    """Una etiqueta legible, derivada del id. No es prosa nueva: el canon no
    escribió nombres en castellano para las locaciones y no se los invento."""
    sitio, locacion = partir_id(lugar)
    if tipo == "camino":
        return f"camino de {locacion or sitio}"
    if tipo == "zona":
        return f"{lugar} · zona de pesca"
    return f"{sitio} · {locacion}" if locacion else sitio


def catalogo_de_lugares(propuesta: dict) -> list[dict]:
    """Los 29 lugares con su punto, su nodo y su marca de compartido.

    `§puntos.lugares` ya trae la resolución: `propio` (8), `heredado` (16, el
    punto de su aldea), `zona` (2, que no son un punto sino un área) y `arista`
    (3, que son un camino). Aquí sólo se le pega el nodo y se normaliza la
    forma; ninguna coordenada se calcula.
    """
    puntos = (propuesta.get("puntos") or {}).get("lugares") or {}
    nodos = nodo_por_lugar(propuesta)
    declarados = propuesta.get("compartidos_declarados") or {}

    catalogo: list[dict] = []
    for lugar, punto in sorted(puntos.items()):
        tipo = punto.get("tipo")
        dato = punto.get("dato")
        lat = lon = None
        lista: Optional[list[list[float]]] = None

        if tipo in ("propio", "heredado") and isinstance(dato, (list, tuple)):
            lat, lon = float(dato[0]), float(dato[1])
        elif tipo == "zona":
            # El área es sus puntos; el marcador va en el centro de ellos.
            lista = [[float(p[1]), float(p[2])] for p in dato or []]
            if lista:
                lat = sum(p[0] for p in lista) / len(lista)
                lon = sum(p[1] for p in lista) / len(lista)
        elif tipo == "arista":
            tipo = "camino"
            origen = puntos.get(str(dato), {})
            if isinstance(origen.get("dato"), (list, tuple)):
                lat, lon = float(origen["dato"][0]), float(origen["dato"][1])
            par = CAMINOS_CON_PAR.get(lugar)
            if par:
                extremos = []
                for sitio in par:
                    p = (puntos.get(sitio) or {}).get("dato")
                    if isinstance(p, (list, tuple)):
                        extremos.append([float(p[0]), float(p[1])])
                if len(extremos) == 2:
                    lista = extremos

        compartido = lugar in declarados or lugar in CAMINOS_CON_PAR
        por_que = declarados.get(lugar) or (POR_QUE_CAMINO if lugar in CAMINOS_CON_PAR else None)
        sitio, locacion = partir_id(lugar)
        if tipo == "camino":
            # `camino:Moruy` es el camino que sale de Moruy: el sitio es el
            # origen, no la palabra «camino».
            sitio, locacion = locacion or sitio, None

        catalogo.append({
            "id": lugar,
            "nombre": etiqueta_de(lugar, tipo or ""),
            "sitio": sitio,
            "locacion": locacion,
            "nodo": nodos.get(lugar),
            "tipo": tipo,
            "lat": round(lat, 5) if lat is not None else None,
            "lon": round(lon, 5) if lon is not None else None,
            "puntos": lista,
            "compartido": compartido,
            "por_que": por_que,
        })
    return catalogo


# ══════════════════════════════════════════════════════════════════════
# El recorte del texto
# ══════════════════════════════════════════════════════════════════════

def recortar(texto: Optional[str], tope: int = TOPE_TEXTO) -> tuple[str, bool]:
    """`(texto, recortado)`. Corta en la última palabra que cabe y cierra con «…».

    Un tope declarado, y dicho en el JSON: el visor enseña un asomo de lo que se
    dijo en un sitio, no el corpus. El texto entero vive en `agent_responses`.
    """
    limpio = " ".join((texto or "").split())
    if len(limpio) <= tope:
        return limpio, False
    corte = limpio[:tope]
    espacio = corte.rfind(" ")
    if espacio > tope * 0.6:
        corte = corte[:espacio]
    return corte.rstrip(" ,;:.—-") + "…", True


# ══════════════════════════════════════════════════════════════════════
# El seed
# ══════════════════════════════════════════════════════════════════════

def _clave_turno(fila: dict) -> tuple:
    return (fila.get("run_id"), fila.get("day"), fila.get("turn_num"))


def construir_seed(
    *,
    run_meta: dict,
    presencias: list[dict],
    respuestas: list[dict],
    turnos: list[dict],
    lugares: list[dict],
    tope: int = TOPE_TEXTO,
    generado: Optional[str] = None,
) -> dict:
    """El JSON entero, sin tocar la base ni el reloj de nadie.

    Es la pieza pura: recibe filas (las de `presencias`, las de
    `agent_responses` y las de `turns`) y devuelve el seed. Así los tests pueden
    afirmar sobre el esquema con un fixture de dos turnos, y el exportador se
    limita a traer las filas.

    `turnos` sólo se usa para ordenar la cadena y para colocar una respuesta
    cuyo turno no tenga presencias; el orden que manda es (run en la cadena,
    día, turno).
    """
    avisos: list[str] = []
    cadena: list[str] = run_meta.get("cadena") or []
    orden_run = {rid: i for i, rid in enumerate(run_meta.get("run_ids") or [])}

    conocidos = {l["id"] for l in lugares}
    lugares = list(lugares)

    # (run, turno) → momento, día, turno. Se toma de `presencias` y se completa
    # con `turns`, para que un turno sin escena aparezca igual en el deslizador.
    meta_turno: dict[tuple, dict] = {}
    for t in turnos:
        clave = (t.get("run_id"), t.get("day"), t.get("turn_num"))
        meta_turno.setdefault(clave, {
            "run_id": t.get("run_id"), "dia": t.get("day"),
            "turno": t.get("turn_num"), "momento": t.get("moment") or "",
        })

    # turn_id → clave de turno, para colocar las respuestas.
    turno_de_id: dict[str, tuple] = {t["id"]: (t.get("run_id"), t.get("day"),
                                               t.get("turn_num"))
                                     for t in turnos if t.get("id")}

    # La escena: (clave de turno) → lugar → [presencias]
    escena: dict[tuple, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    lugar_de: dict[tuple, str] = {}          # (turn_id, agente) → lugar
    nodo_de: dict[str, str] = {}
    agentes: set[str] = set()
    sin_coordenada: set[str] = set()

    for p in presencias:
        clave = _clave_turno(p)
        meta_turno.setdefault(clave, {
            "run_id": p.get("run_id"), "dia": p.get("day"),
            "turno": p.get("turn_num"), "momento": p.get("momento") or "",
        })
        if not meta_turno[clave].get("momento") and p.get("momento"):
            meta_turno[clave]["momento"] = p["momento"]
        lugar = p.get("lugar")
        if not lugar:
            continue
        agente = p.get("agent_name")
        agentes.add(agente)
        if p.get("nodo"):
            nodo_de[agente] = p["nodo"]
        escena[clave][lugar].append(p)
        lugar_de[(p.get("turn_id"), agente)] = lugar
        if lugar not in conocidos:
            sin_coordenada.add(lugar)

    # Un lugar que la escena usó y la tabla derivada no conoce se dibuja igual —
    # sin punto y marcado. Callarlo sería perder al agente en el mapa.
    for lugar in sorted(sin_coordenada):
        sitio, locacion = partir_id(lugar)
        lugares.append({
            "id": lugar, "nombre": etiqueta_de(lugar, ""), "sitio": sitio,
            "locacion": locacion, "nodo": None, "tipo": "sin-coordenada",
            "lat": None, "lon": None, "puntos": None,
            "compartido": False, "por_que": None,
        })
        avisos.append(
            f"«{lugar}» está en `presencias` y no en la tabla derivada: sin "
            f"coordenada, se dibuja aparte")

    # Lo que se dijo, colocado por `presencias` y contrastado con la columna
    # desnormalizada de `agent_responses`.
    dichos: dict[tuple, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    hablaron: set[tuple] = set()
    discrepancias = 0
    huerfanas = 0
    for r in respuestas:
        agente = r.get("agent_name")
        turn_id = r.get("turn_id")
        clave = turno_de_id.get(turn_id)
        lugar = lugar_de.get((turn_id, agente))
        if lugar and r.get("lugar") and r["lugar"] != lugar:
            discrepancias += 1
        lugar = lugar or r.get("lugar")
        if not clave or not lugar:
            huerfanas += 1
            continue
        texto, cortado = recortar(r.get("response_text"), tope)
        dichos[clave][lugar].append({
            "agente": agente,
            "nodo": nodo_de.get(agente),
            "texto": texto,
            "recortado": cortado,
        })
        hablaron.add((turn_id, agente))

    if discrepancias:
        avisos.append(
            f"{discrepancias} respuesta(s) con `agent_responses.lugar` distinto "
            f"del de `presencias`: manda `presencias`")
    if huerfanas:
        avisos.append(
            f"{huerfanas} respuesta(s) sin lugar ni presencia en su turno: no "
            f"entran al mapa (¿run sin escena?)")

    # El deslizador: los turnos en el orden en que ocurrieron.
    claves = sorted(
        meta_turno,
        key=lambda c: (orden_run.get(c[0], 0), c[1] if c[1] is not None else 0,
                       c[2] if c[2] is not None else 0),
    )
    filas_turno: list[dict] = []
    for i, clave in enumerate(claves):
        meta = meta_turno[clave]
        en_lugar = escena.get(clave, {})
        escenas = []
        for lugar in sorted(en_lugar):
            gente = en_lugar[lugar]
            por_nodo: dict[str, int] = defaultdict(int)
            presentes = []
            for p in sorted(gente, key=lambda x: x.get("agent_name") or ""):
                nodo = p.get("nodo")
                if nodo:
                    por_nodo[nodo] += 1
                presentes.append({
                    "agente": p.get("agent_name"),
                    "nodo": nodo,
                    "hablo": (p.get("turn_id"), p.get("agent_name")) in hablaron,
                })
            escenas.append({
                "lugar": lugar,
                "n": len(presentes),
                "por_nodo": dict(sorted(por_nodo.items())),
                "contacto": len(por_nodo) > 1,
                "presentes": presentes,
                "dichos": dichos.get(clave, {}).get(lugar, []),
            })
        filas_turno.append({
            "i": i,
            "run": (clave[0] or "")[:8],
            "dia": meta.get("dia"),
            "turno": meta.get("turno"),
            "momento": meta.get("momento") or "",
            "n_presencias": sum(e["n"] for e in escenas),
            "escenas": escenas,
        })

    # Un turno sin escena en medio de un run que sí la tiene es un agujero: la
    # capa 1 escribe 63 filas por turno o no escribe ninguna.
    con_escena = [t for t in filas_turno if t["n_presencias"]]
    if con_escena and len(con_escena) != len(filas_turno):
        avisos.append(
            f"{len(filas_turno) - len(con_escena)} turno(s) sin ninguna "
            f"presencia, y otros {len(con_escena)} con ella")

    dias = sorted({t["dia"] for t in filas_turno if t["dia"] is not None})
    return {
        "version": VERSION,
        "generado": generado or datetime.now(timezone.utc).isoformat(),
        "vacio": not presencias,
        "tope_texto": tope,
        "run": {
            "id8": run_meta.get("id8"),
            "run_id": run_meta.get("run_id"),
            "cadena": cadena,
            "started_at": run_meta.get("started_at"),
            "dias": dias,
            "n_turnos": len(filas_turno),
            "n_agentes": len(agentes),
            "n_presencias": sum(t["n_presencias"] for t in filas_turno),
        },
        "lugares": sorted(lugares, key=lambda l: l["id"]),
        "turnos": filas_turno,
        "avisos": avisos,
    }


# ══════════════════════════════════════════════════════════════════════
# La base
# ══════════════════════════════════════════════════════════════════════

def todas_las_filas(construir, pagina: int = PAGINA) -> list[dict]:
    """Todas las filas de una query de PostgREST, página a página.

    Igual que en `export_runs_index.py`, y por la misma razón: sin `.range()`
    PostgREST corta en `max_rows` EN SILENCIO. Se reconstruye la query en cada
    página porque `.range()` de postgrest-py AÑADE offset/limit en vez de
    reemplazarlos. Para con la primera página vacía, no con la primera corta.
    """
    filas: list[dict] = []
    desde = 0
    while True:
        lote = (construir().order("id").range(desde, desde + pagina - 1)
                .execute().data or [])
        if not lote:
            return filas
        filas.extend(lote)
        desde += len(lote)


def resolver_run(db: Any, id8: str) -> Optional[dict]:
    """La fila de `simulation_runs` cuyo id empieza por `id8`."""
    runs = db.runs_encadenados() or []
    coincidencias = [r for r in runs if str(r.get("id", "")).startswith(id8)]
    if len(coincidencias) > 1:
        raise SystemExit(f"«{id8}» casa con {len(coincidencias)} runs; da más caracteres")
    return coincidencias[0] if coincidencias else None


def respuestas_y_turnos(db: Any, run_ids: list[str]) -> tuple[list[dict], list[dict]]:
    """Las respuestas (con su lugar y su texto) y los turnos de esos runs.

    Sin `client` —el mock— no hay de dónde: el mock guarda la escena en memoria
    (`presencias`) pero no el texto de las respuestas, y ésa es exactamente la
    frontera de lo que un test sin base puede afirmar.
    """
    if not run_ids or not hasattr(db, "client"):
        return [], []
    respuestas = todas_las_filas(
        lambda: db.client.table("agent_responses")
        .select("id, run_id, turn_id, agent_name, response_text, lugar")
        .in_("run_id", run_ids))
    turnos = todas_las_filas(
        lambda: db.client.table("turns")
        .select("id, run_id, day, turn_num, moment")
        .in_("run_id", run_ids))
    return respuestas, turnos


def seed_de_run(db: Any, id8: str, cadena: bool, tope: int = TOPE_TEXTO) -> dict:
    """Junta las filas del run (o de su cadena) y arma el seed."""
    import curiana_cadena

    run = resolver_run(db, id8)
    if not run:
        raise SystemExit(f"⚠  No hay ningún run que empiece por «{id8}» en la base")
    run_id = str(run["id"])

    run_ids = [run_id]
    if cadena:
        encadenados = curiana_cadena.cadena_de_runs(db, run_id)
        if encadenados:
            run_ids = [str(r["id"]) for r in encadenados]
        else:
            print("  ⚠  --cadena: no se pudo subir por `continuado_desde`; "
                  "se exporta el run solo")

    presencias = db.presencias_de_cadena(run_ids)
    respuestas, turnos = respuestas_y_turnos(db, run_ids)

    return construir_seed(
        run_meta={
            "id8": run_id[:8],
            "run_id": run_id,
            "run_ids": run_ids,
            "cadena": [r[:8] for r in run_ids],
            "started_at": run.get("started_at"),
        },
        presencias=presencias,
        respuestas=respuestas,
        turnos=turnos,
        lugares=catalogo_de_lugares(cargar_propuesta()),
        tope=tope,
    )


def seed_vacio(tope: int = TOPE_TEXTO) -> dict:
    """El seed del catálogo, sin base. El mapa se dibuja; no hay nadie encima."""
    return construir_seed(
        run_meta={"id8": None, "run_id": None, "run_ids": [], "cadena": [],
                  "started_at": None},
        presencias=[], respuestas=[], turnos=[],
        lugares=catalogo_de_lugares(cargar_propuesta()), tope=tope)


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

def escribir(seed: dict, salida: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
        f.write("\n")


def informe(seed: dict, salida: str) -> None:
    run = seed["run"]
    con_punto = len([l for l in seed["lugares"] if l["lat"] is not None])
    print(f"  ✓ {len(seed['lugares'])} lugares ({con_punto} con punto, "
          f"{len([l for l in seed['lugares'] if l['compartido']])} compartidos)")
    if seed["vacio"]:
        print("  ⚠  Ni una fila en `presencias`: el seed va VACÍO (válido). "
              "Ningún run ha corrido con escena todavía.")
    else:
        contactos = sum(1 for t in seed["turnos"] for e in t["escenas"] if e["contacto"])
        dichos = sum(len(e["dichos"]) for t in seed["turnos"] for e in t["escenas"])
        print(f"  ✓ {run['n_turnos']} turnos · días {run['dias']} · "
              f"{run['n_agentes']} agentes · {run['n_presencias']} presencias")
        print(f"  ✓ {dichos} intervenciones situadas · {contactos} escena(s) "
              f"con los dos nodos a la vez")
    for aviso in seed["avisos"]:
        print(f"  ⚠  {aviso}")
    print(f"\n{os.path.relpath(salida, REPO)} escrito")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", metavar="ID8",
                    help="el run a exportar (prefijo de su id)")
    ap.add_argument("--cadena", action="store_true",
                    help="sube por `continuado_desde` y exporta la cadena entera")
    ap.add_argument("--salida", metavar="RUTA",
                    help=f"por defecto {os.path.relpath(DIR_SALIDA, REPO)}/<id8>.json")
    ap.add_argument("--tope", type=int, default=TOPE_TEXTO, metavar="N",
                    help=f"caracteres por intervención (por defecto {TOPE_TEXTO})")
    ap.add_argument("--sin-base", action="store_true",
                    help="no consulta la base: escribe el seed vacío con el "
                         "catálogo de lugares, para que la web construya antes "
                         "del primer run con escena")
    args = ap.parse_args(argv)

    if args.sin_base:
        seed = seed_vacio(args.tope)
        salida = args.salida or os.path.join(DIR_SALIDA, "sin-escena.json")
    else:
        if not args.run:
            ap.error("hace falta --run <id8> (o --sin-base)")
        db = get_db()
        seed = seed_de_run(db, args.run, args.cadena, args.tope)
        salida = args.salida or os.path.join(DIR_SALIDA, f"{seed['run']['id8']}.json")

    escribir(seed, salida)
    informe(seed, salida)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
