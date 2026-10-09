"""compilar_hermanas.py — las esferas de los pueblos hermanos, validadas y cruzadas.

Valida el esquema de `3-mundo/hermanas/README.md` sobre dos sitios a la vez:

  3-mundo/hermanas/<pueblo>/<esfera>.yaml    el canon (tras fusión)
  6-fusion/hermanas_<pueblo>_<fecha>.yaml     las propuestas (mismo esquema)

y, con `--matriz`, cruza tema × pueblo para ver de un vistazo qué sabemos del
segundo entierro, de la jefatura o del espíritu tutelar en cada hermana, con
el caquetío al lado (los hechos del corpus que cada tema toca).

Qué comprueba:

1. **Estructura** — campos obligatorios; `id` con la forma
   `<pueblo>-<esfera>-NNN[a-z]?`, único en todo el conjunto, y coherente con
   `pueblo` y `esfera` del propio hecho.
2. **Vocabularios cerrados** — `pueblo`, `esfera`, `tema` (por esfera),
   `etiqueta`, `testigo`, `sustrato`, `proyeccion.capa`, los valores de
   `via_a`. Lo que no cabe va a `dominios` (libre) o se propone en
   `meta.temas_propuestos` (aviso, no error).
3. **Regla 2 de la hermana** — `testigo: tercera-mano` obliga a
   `etiqueta: hipotetico`; `atestiguado` exige `procedencia.pagina`.
4. **Regla 8** — `procedencia.obra` y `procedencia_extra[].obra` son claves
   foráneas de `4-fuentes/bibliografia.yaml`.
5. **Regla C (Miguel, 2026-10-09)** — `proyeccion.capa: reconstruido` exige al
   menos una hermana de OTRO pueblo en `hermanas` (el hecho es la primera
   tradición; la segunda tiene que ser independiente, y eso lo declara
   `procedencia_extra[].independiente` o la propia hermana).
6. **Cruces** — `caquetio[]` y las claves de `via_a` resuelven a ids del
   corpus caquetío; `hermanas[].id` resuelve a un hecho cargado (aviso si no,
   porque la propuesta del otro pueblo puede no estar fusionada todavía).
7. **Canon** — un archivo de `3-mundo/hermanas/<pueblo>/` sólo lleva hechos de
   su esfera y de su pueblo, y `meta.estado: canon`.

Uso:

    python curiana_sim/compilar_hermanas.py [rutas extra...]   # informe
    python curiana_sim/compilar_hermanas.py --check            # exit 1 si hay errores
    python curiana_sim/compilar_hermanas.py --matriz           # tema × pueblo
    python curiana_sim/compilar_hermanas.py --matriz --escribir   # reescribe COMPARADA.md
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from collections import Counter, defaultdict

import yaml

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_AQUI)
HERMANAS_DIR = os.path.join(REPO, "3-mundo", "hermanas")
FUSION_DIR = os.path.join(REPO, "6-fusion")
CORPUS_DIR = os.path.join(REPO, "3-mundo", "corpus")
BIBLIOGRAFIA = os.path.join(REPO, "4-fuentes", "bibliografia.yaml")
COMPARADA = os.path.join(HERMANAS_DIR, "COMPARADA.md")

# ── vocabularios cerrados (README §2-§4) ───────────────────────────────────
PUEBLOS = ("taino", "lokono", "kalinago", "achagua", "maipure", "wayuu", "paraujano")
ORDEN_PUEBLOS = ("caquetio",) + PUEBLOS
ESFERAS = ("parentesco", "creencia", "ecologia", "transmision", "geografia_politica")
TEMAS = {
    "parentesco": (
        "descendencia", "residencia", "matrimonio", "sucesion-herencia", "linaje-clan",
        "roles-de-genero", "infancia-nombre", "sociedades-masculinas", "hogar-casa",
    ),
    "geografia_politica": (
        "jefatura", "jerarquia-rango", "sucesion-politica", "territorio-asentamiento",
        "escala-poblacion", "guerra", "alianza-intercambio", "tributo-trabajo",
        "cautivos-esclavitud", "justicia-norma",
    ),
    "creencia": (
        "espiritu-tutelar", "alma", "muerte-entierro", "segundo-entierro", "especialista",
        "iniciacion-especialista", "enfermedad-cura", "cosmos-origen", "tiempo-calendario",
        "ofrenda-fiesta", "tabu", "sueno-vision", "lugar-sagrado",
    ),
    "ecologia": (
        "medio-fisico", "cultivo", "pesca", "caza-recoleccion", "vivienda",
        "tecnologia-objetos", "comida-bebida", "comercio-rutas", "navegacion",
    ),
    "transmision": (
        "curriculo-edad", "especialista-formacion", "saber-restringido", "narracion-mito",
        "lengua-registro", "canto-baile", "escritura-marca", "nombre-propio",
    ),
}
ETIQUETAS = ("atestiguado", "hipotetico")
TESTIGOS = ("vio", "oyo", "lexico", "tercera-mano")
SUSTRATOS = ("arahuaco", "caribe", "colonial", "sin-decidir")
CAPAS = ("reconstruido", "hipotetico", "lectura", "comparanda-esfera", "no-proyecta")
VIA_A = ("corrobora", "corrobora-en-parte", "contradice", "matiza", "no-toca")
ESTADOS = ("sin-fusionar", "fusionada", "canon")
OBLIGATORIOS = ("id", "esfera", "tema", "contenido", "pueblo", "epoca", "etiqueta",
                "testigo", "procedencia", "proyeccion")

RE_ID = re.compile(r"^([a-z]+)-([a-z_]+)-(\d{3})([a-z]?)$")
RE_CORPUS = re.compile(r"^[a-z][a-z_]*(?:-[a-z]+)*-\d{3}[a-z]?$")


def _forzar_utf8() -> None:
    """La consola de Windows usa cp1252 y este informe imprime «─», «✓», «í»…"""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, __import__("io").TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


class Problema:
    __slots__ = ("nivel", "codigo", "donde", "mensaje")

    def __init__(self, nivel, codigo, donde, mensaje):
        self.nivel, self.codigo, self.donde, self.mensaje = nivel, codigo, donde, mensaje

    def __str__(self):
        marca = "✗" if self.nivel == "error" else "⚠"
        return f"  {marca} [{self.codigo}] {self.donde}: {self.mensaje}"


def _error(codigo, donde, mensaje):
    return Problema("error", codigo, donde, mensaje)


def _aviso(codigo, donde, mensaje):
    return Problema("aviso", codigo, donde, mensaje)


# ── carga ──────────────────────────────────────────────────────────────────

def _rel(ruta: str) -> str:
    return os.path.relpath(ruta, REPO).replace("\\", "/")


def archivos_canon():
    patron = os.path.join(HERMANAS_DIR, "*", "*.yaml")
    return sorted(glob.glob(patron))


def archivos_propuestas():
    patron = os.path.join(FUSION_DIR, "hermanas_*.yaml")
    return sorted(glob.glob(patron))


def cargar(rutas_extra=()):
    """Lee canon + propuestas (+ rutas extra). Devuelve (archivos, problemas).

    Cada archivo es un dict: ruta, canon (bool), meta, hechos (lista).
    """
    archivos, problemas = [], []
    pendientes = [(r, True) for r in archivos_canon()]
    pendientes += [(r, False) for r in archivos_propuestas()]
    pendientes += [(os.path.abspath(r), False) for r in rutas_extra]
    for ruta, canon in pendientes:
        rel = _rel(ruta)
        try:
            with open(ruta, encoding="utf-8") as fh:
                datos = yaml.safe_load(fh)
        except (OSError, yaml.YAMLError) as e:
            problemas.append(_error("yaml-invalido", rel, f"no se puede leer: {e}"))
            continue
        if isinstance(datos, list):
            meta, hechos = {}, datos
        elif isinstance(datos, dict):
            meta = datos.get("meta") or {}
            hechos = datos.get("hechos")
            if hechos is None:
                problemas.append(_error("sin-hechos", rel, "no hay clave `hechos`"))
                hechos = []
        else:
            problemas.append(_error("raiz-inesperada", rel,
                                    f"la raíz es {type(datos).__name__}, se esperaba dict"))
            continue
        if not isinstance(hechos, list):
            problemas.append(_error("hechos-no-lista", rel,
                                    f"`hechos` es {type(hechos).__name__}"))
            hechos = []
        for h in hechos:
            if isinstance(h, dict):
                h["_archivo"] = rel
        archivos.append({"ruta": ruta, "rel": rel, "canon": canon,
                         "meta": meta if isinstance(meta, dict) else {},
                         "hechos": [h for h in hechos if isinstance(h, dict)]})
        malos = sum(1 for h in hechos if not isinstance(h, dict))
        if malos:
            problemas.append(_error("hecho-no-dict", rel, f"{malos} entrada(s) que no son dict"))
    return archivos, problemas


def _obras_de_la_bibliografia():
    if not os.path.exists(BIBLIOGRAFIA):
        return None
    with open(BIBLIOGRAFIA, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    return {o["id"] for o in doc.get("obras", []) if isinstance(o, dict) and o.get("id")}


def _ids_del_corpus():
    """Los ids de hecho del corpus caquetío (`3-mundo/corpus/*.yaml`), o None."""
    if not os.path.isdir(CORPUS_DIR):
        return None
    ids = set()
    for nombre in os.listdir(CORPUS_DIR):
        if not nombre.endswith(".yaml") or nombre == "genealogia.yaml":
            continue
        try:
            with open(os.path.join(CORPUS_DIR, nombre), encoding="utf-8") as fh:
                datos = yaml.safe_load(fh)
        except (OSError, yaml.YAMLError):
            continue
        secciones = datos if isinstance(datos, list) else (
            [v for v in datos.values() if isinstance(v, list)] if isinstance(datos, dict) else [])
        if isinstance(datos, list):
            secciones = [datos]
        for lista in secciones:
            for h in lista:
                if isinstance(h, dict) and isinstance(h.get("id"), str):
                    ids.add(h["id"])
    return ids


# ── validación ─────────────────────────────────────────────────────────────

def _donde(hecho: dict) -> str:
    return f"{hecho.get('_archivo', '?')} · {hecho.get('id', '(sin id)')}"


def validar_meta(archivo: dict) -> list:
    p, meta, rel = [], archivo["meta"], archivo["rel"]
    if not meta:
        p.append(_error("sin-meta", rel, "falta `meta` (pueblo, recogido, estado, quien)"))
        return p
    for campo in ("pueblo", "recogido", "estado"):
        if not meta.get(campo):
            p.append(_error("meta-incompleta", rel, f"falta `meta.{campo}`"))
    if meta.get("pueblo") and meta["pueblo"] not in PUEBLOS:
        p.append(_error("pueblo-ilegal", rel, f"meta.pueblo `{meta['pueblo']}`; vale {PUEBLOS}"))
    if meta.get("estado") and meta["estado"] not in ESTADOS:
        p.append(_error("estado-ilegal", rel, f"meta.estado `{meta['estado']}`; vale {ESTADOS}"))
    if archivo["canon"]:
        if meta.get("estado") != "canon":
            p.append(_error("canon-sin-estado", rel, "un archivo de 3-mundo/hermanas/ lleva `meta.estado: canon`"))
        esfera_archivo = os.path.splitext(os.path.basename(archivo["ruta"]))[0]
        pueblo_archivo = os.path.basename(os.path.dirname(archivo["ruta"]))
        if esfera_archivo not in ESFERAS:
            p.append(_error("archivo-canon-ilegal", rel, f"el nombre no es una esfera: {ESFERAS}"))
        if pueblo_archivo not in PUEBLOS:
            p.append(_error("directorio-canon-ilegal", rel, f"el directorio no es un pueblo: {PUEBLOS}"))
        for h in archivo["hechos"]:
            if h.get("esfera") != esfera_archivo:
                p.append(_error("esfera-fuera-de-archivo", _donde(h),
                                f"esfera `{h.get('esfera')}` en el archivo de `{esfera_archivo}`"))
            if h.get("pueblo") != pueblo_archivo:
                p.append(_error("pueblo-fuera-de-directorio", _donde(h),
                                f"pueblo `{h.get('pueblo')}` en el directorio de `{pueblo_archivo}`"))
    temas_propuestos = meta.get("temas_propuestos") or {}
    if temas_propuestos and not isinstance(temas_propuestos, dict):
        p.append(_error("temas-propuestos-mal-formados", rel,
                        "`meta.temas_propuestos` es {esfera: [tema, ...]}"))
    return p


def _temas_propuestos(meta: dict) -> set:
    tp = meta.get("temas_propuestos") or {}
    if not isinstance(tp, dict):
        return set()
    return {(e, t) for e, lista in tp.items() if isinstance(lista, list) for t in lista}


def validar_hechos(archivos: list, obras, ids_corpus) -> list:
    p = []
    vistos = {}
    todos = {h["id"]: h for a in archivos for h in a["hechos"] if isinstance(h.get("id"), str)}

    for archivo in archivos:
        propuestos = _temas_propuestos(archivo["meta"])
        for h in archivo["hechos"]:
            d = _donde(h)
            # 1. estructura
            faltan = [c for c in OBLIGATORIOS if h.get(c) in (None, "", [], {})]
            if faltan:
                p.append(_error("campo-obligatorio", d, "faltan: " + ", ".join(faltan)))
            hid = h.get("id")
            if isinstance(hid, str):
                if hid in vistos:
                    p.append(_error("id-duplicado", d, f"ya está en {vistos[hid]}"))
                vistos[hid] = archivo["rel"]
                m = RE_ID.match(hid)
                if not m:
                    p.append(_error("id-mal-formado", d, "la forma es <pueblo>-<esfera>-NNN[a-z]?"))
                else:
                    pueblo_id, esfera_id = m.group(1), m.group(2)
                    if pueblo_id not in PUEBLOS:
                        p.append(_error("id-pueblo-ilegal", d, f"`{pueblo_id}` no es un pueblo"))
                    if h.get("pueblo") and h["pueblo"] != pueblo_id:
                        p.append(_error("id-pueblo-incoherente", d,
                                        f"el id dice `{pueblo_id}` y `pueblo:` dice `{h['pueblo']}`"))
                    if h.get("esfera") and h["esfera"] != esfera_id:
                        p.append(_error("id-esfera-incoherente", d,
                                        f"el id dice `{esfera_id}` y `esfera:` dice `{h['esfera']}`"))
            # 2. vocabularios
            if h.get("pueblo") and h["pueblo"] not in PUEBLOS:
                p.append(_error("pueblo-ilegal", d, f"`{h['pueblo']}`; vale {PUEBLOS}"))
            esfera = h.get("esfera")
            if esfera and esfera not in ESFERAS:
                p.append(_error("esfera-ilegal", d, f"`{esfera}`; vale {ESFERAS}"))
            tema = h.get("tema")
            if esfera in TEMAS and tema:
                if tema not in TEMAS[esfera]:
                    if (esfera, tema) in propuestos:
                        p.append(_aviso("tema-propuesto", d,
                                        f"`{tema}` no es tema de `{esfera}`; propuesto en meta — lo decide Miguel"))
                    else:
                        p.append(_error("tema-ilegal", d,
                                        f"`{tema}` no es tema de `{esfera}` (README §4); "
                                        "o usa uno cerrado o proponlo en meta.temas_propuestos"))
            if h.get("etiqueta") and h["etiqueta"] not in ETIQUETAS:
                p.append(_error("etiqueta-ilegal", d, f"`{h['etiqueta']}`; vale {ETIQUETAS} "
                                "(reconstruido no existe DENTRO de una hermana: va en proyeccion)"))
            if h.get("testigo") and h["testigo"] not in TESTIGOS:
                p.append(_error("testigo-ilegal", d, f"`{h['testigo']}`; vale {TESTIGOS}"))
            if h.get("sustrato") and h["sustrato"] not in SUSTRATOS:
                p.append(_error("sustrato-ilegal", d, f"`{h['sustrato']}`; vale {SUSTRATOS}"))
            if not isinstance(h.get("epoca"), str) or not h.get("epoca", "").strip():
                p.append(_error("epoca-ausente", d, "`epoca` dice de cuándo es el testimonio (regla 3)"))
            # 3. regla 2 de la hermana
            if h.get("testigo") == "tercera-mano" and h.get("etiqueta") == "atestiguado":
                p.append(_error("tercera-mano-atestiguada", d,
                                "tercera mano obliga a `hipotetico`: un compilador no atestigua"))
            # 4. procedencia
            proc = h.get("procedencia")
            if proc is not None:
                if not isinstance(proc, dict):
                    p.append(_error("procedencia-mal-formada", d, "es {obra, pagina[, via]}"))
                else:
                    obra = proc.get("obra")
                    if not obra:
                        p.append(_error("procedencia-sin-obra", d, "falta `procedencia.obra`"))
                    elif obras is not None and obra not in obras:
                        p.append(_error("obra-desconocida", d,
                                        f"`{obra}` no está en bibliografia.yaml (regla 8)"))
                    if h.get("etiqueta") == "atestiguado" and not proc.get("pagina"):
                        p.append(_error("atestiguado-sin-pagina", d,
                                        "`atestiguado` exige `procedencia.pagina`"))
                    via = proc.get("via")
                    if via and obras is not None and via not in obras:
                        p.append(_error("via-desconocida", d, f"`{via}` no está en bibliografia.yaml"))
            extra = h.get("procedencia_extra") or []
            if not isinstance(extra, list):
                p.append(_error("procedencia-extra-mal-formada", d, "es una lista de {obra, pagina, independiente}"))
                extra = []
            for i, e in enumerate(extra):
                if not isinstance(e, dict) or not e.get("obra"):
                    p.append(_error("procedencia-extra-sin-obra", d, f"entrada {i}"))
                    continue
                if obras is not None and e["obra"] not in obras:
                    p.append(_error("obra-desconocida", d, f"procedencia_extra[{i}] `{e['obra']}`"))
                if "independiente" not in e:
                    p.append(_aviso("independencia-sin-declarar", d,
                                    f"procedencia_extra[{i}] no dice si es testigo independiente"))
            # 5. proyección y regla C
            proy = h.get("proyeccion")
            if proy is not None:
                if not isinstance(proy, dict) or not proy.get("capa"):
                    p.append(_error("proyeccion-mal-formada", d, "es {capa, nota}"))
                else:
                    capa = proy["capa"]
                    if capa not in CAPAS:
                        p.append(_error("capa-ilegal", d, f"`{capa}`; vale {CAPAS}"))
                    hermanas = h.get("hermanas") or []
                    if capa == "reconstruido":
                        otras = {x.get("pueblo") for x in hermanas
                                 if isinstance(x, dict) and x.get("pueblo") and x.get("pueblo") != h.get("pueblo")}
                        if not otras:
                            p.append(_error("reconstruido-sin-segunda-tradicion", d,
                                            "regla C: `reconstruido` exige en `hermanas` al menos un "
                                            "pueblo distinto (dos tradiciones arahuacas independientes)"))
                        if not proy.get("nota"):
                            p.append(_aviso("proyeccion-sin-nota", d, "`reconstruido` sin `proyeccion.nota`"))
            # 6. cruces
            hermanas = h.get("hermanas") or []
            if not isinstance(hermanas, list):
                p.append(_error("hermanas-mal-formadas", d, "es una lista"))
                hermanas = []
            for i, x in enumerate(hermanas):
                if not isinstance(x, dict) or not x.get("pueblo"):
                    p.append(_error("hermana-sin-pueblo", d, f"hermanas[{i}]"))
                    continue
                if x["pueblo"] not in PUEBLOS and x["pueblo"] != "caquetio":
                    p.append(_error("hermana-pueblo-ilegal", d, f"hermanas[{i}] `{x['pueblo']}`"))
                if x.get("id"):
                    if x["id"] not in todos:
                        p.append(_aviso("hermana-no-resuelve", d,
                                        f"hermanas[{i}] `{x['id']}` no está cargado (¿propuesta sin fusionar?)"))
                elif not (x.get("obra") and x.get("que")):
                    p.append(_error("hermana-sin-ancla", d,
                                    f"hermanas[{i}]: o `id` de un hecho, o {{obra, pagina, que}}"))
                elif obras is not None and x["obra"] not in obras:
                    p.append(_error("obra-desconocida", d, f"hermanas[{i}] `{x['obra']}`"))
            caq = h.get("caquetio") or []
            if not isinstance(caq, list):
                p.append(_error("caquetio-mal-formado", d, "`caquetio` es una lista de ids del corpus"))
                caq = []
            for cid in caq:
                if not isinstance(cid, str) or not RE_CORPUS.match(cid):
                    p.append(_error("caquetio-id-mal-formado", d, f"`{cid}`"))
                elif ids_corpus is not None and cid not in ids_corpus:
                    p.append(_error("caquetio-no-resuelve", d, f"`{cid}` no está en 3-mundo/corpus/"))
            via_a = h.get("via_a") or {}
            if not isinstance(via_a, dict):
                p.append(_error("via-a-mal-formada", d, "`via_a` es {id-del-corpus: veredicto}"))
                via_a = {}
            for cid, veredicto in via_a.items():
                if ids_corpus is not None and cid not in ids_corpus:
                    p.append(_error("via-a-no-resuelve", d, f"`{cid}` no está en 3-mundo/corpus/"))
                if veredicto not in VIA_A:
                    p.append(_error("via-a-veredicto-ilegal", d, f"`{veredicto}`; vale {VIA_A}"))
    return p


def compilar(rutas_extra=()):
    archivos, problemas = cargar(rutas_extra)
    obras = _obras_de_la_bibliografia()
    ids_corpus = _ids_del_corpus()
    if obras is None:
        problemas.append(_aviso("sin-bibliografia", _rel(BIBLIOGRAFIA),
                                "no existe: las citas no se pueden comprobar"))
    if ids_corpus is None:
        problemas.append(_aviso("sin-corpus", _rel(CORPUS_DIR), "no existe: `caquetio` y `via_a` no se comprueban"))
    for a in archivos:
        problemas += validar_meta(a)
    problemas += validar_hechos(archivos, obras, ids_corpus)
    return archivos, problemas


# ── informe y matriz ───────────────────────────────────────────────────────

def _hechos(archivos):
    return [h for a in archivos for h in a["hechos"]]


def informe(archivos, problemas) -> None:
    hechos = _hechos(archivos)
    print("─" * 72)
    print("ESFERAS DE LAS HERMANAS")
    print("─" * 72)
    canon = [a for a in archivos if a["canon"]]
    props = [a for a in archivos if not a["canon"]]
    print(f"  canon: {len(canon)} archivo(s), {sum(len(a['hechos']) for a in canon)} hecho(s)")
    print(f"  propuestas: {len(props)} archivo(s), {sum(len(a['hechos']) for a in props)} hecho(s)")
    por_pueblo = Counter(h.get("pueblo") for h in hechos)
    for pueblo in ORDEN_PUEBLOS:
        if por_pueblo.get(pueblo):
            sub = [h for h in hechos if h.get("pueblo") == pueblo]
            etiq = Counter(h.get("etiqueta") for h in sub)
            capas = Counter((h.get("proyeccion") or {}).get("capa") if isinstance(h.get("proyeccion"), dict) else None for h in sub)
            esf = Counter(h.get("esfera") for h in sub)
            print(f"  · {pueblo}: {len(sub)} — "
                  + ", ".join(f"{e} {n}" for e, n in sorted(esf.items()))
                  + " | " + ", ".join(f"{k} {v}" for k, v in sorted(etiq.items(), key=lambda kv: str(kv[0])))
                  + " | proyección: " + ", ".join(f"{k} {v}" for k, v in sorted(capas.items(), key=lambda kv: str(kv[0]))))
    errores = [p for p in problemas if p.nivel == "error"]
    avisos = [p for p in problemas if p.nivel == "aviso"]
    if problemas:
        print()
        for p in problemas:
            print(p)
    print()
    if errores:
        print(f"✗ {len(errores)} error(es), {len(avisos)} aviso(s)")
    else:
        print(f"✓ esferas de las hermanas válidas — {len(hechos)} hecho(s), {len(avisos)} aviso(s)")


def _corto(hid: str) -> str:
    m = RE_ID.match(hid or "")
    return (m.group(3) + m.group(4)) if m else (hid or "?")


def matriz(archivos) -> str:
    """Tema × pueblo por esfera, en markdown. El caquetío es la columna de los
    hechos del corpus que los hechos de ese tema tocan (`caquetio[]`)."""
    hechos = _hechos(archivos)
    pueblos = [p for p in ORDEN_PUEBLOS if p != "caquetio" and any(h.get("pueblo") == p for h in hechos)]
    lineas = [
        "---",
        "tipo: vista",
        "generado_por: curiana_sim/compilar_hermanas.py --matriz --escribir",
        "ambito: tema × pueblo, las cinco esferas de las hermanas con el caquetío al lado",
        "nota: generado — no se edita a mano",
        "---",
        "",
        "# Las hermanas, tema a tema",
        "",
        "> Cada celda: cuántos hechos tiene ese pueblo sobre ese tema (ids cortos).",
        "> La columna **caquetío** lista los hechos del corpus caquetío que esos",
        "> hechos tocan (`caquetio[]`): no es un censo del corpus, es el diálogo.",
        "> Fuente: canon de `3-mundo/hermanas/` + propuestas `6-fusion/hermanas_*.yaml`.",
        "",
    ]
    for esfera in ESFERAS:
        sub = [h for h in hechos if h.get("esfera") == esfera]
        if not sub:
            continue
        lineas.append(f"## {esfera}")
        lineas.append("")
        lineas.append("| tema | caquetío (tocado) | " + " | ".join(pueblos) + " |")
        lineas.append("|---|---|" + "|".join("---" for _ in pueblos) + "|")
        temas = list(TEMAS[esfera]) + sorted({h.get("tema") for h in sub if h.get("tema") not in TEMAS[esfera]})
        for tema in temas:
            fila = [h for h in sub if h.get("tema") == tema]
            if not fila:
                continue
            tocados = sorted({c for h in fila for c in (h.get("caquetio") or []) if isinstance(c, str)})
            celdas = []
            for pueblo in pueblos:
                mios = [h for h in fila if h.get("pueblo") == pueblo]
                celdas.append(f"{len(mios)} ({', '.join(_corto(h.get('id')) for h in mios)})" if mios else "—")
            lineas.append(f"| {tema} | {', '.join(tocados) if tocados else '—'} | " + " | ".join(celdas) + " |")
        lineas.append("")
    # resumen de proyección
    lineas.append("## Lo que cada hermana autoriza a decir del caquetío (`proyeccion.capa`)")
    lineas.append("")
    lineas.append("| pueblo | " + " | ".join(CAPAS) + " |")
    lineas.append("|---|" + "|".join("---" for _ in CAPAS) + "|")
    for pueblo in pueblos:
        mios = [h for h in hechos if h.get("pueblo") == pueblo]
        c = Counter((h.get("proyeccion") or {}).get("capa") for h in mios if isinstance(h.get("proyeccion"), dict))
        lineas.append(f"| {pueblo} | " + " | ".join(str(c.get(k, 0)) for k in CAPAS) + " |")
    lineas.append("")
    return "\n".join(lineas) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rutas", nargs="*", help="YAML extra a validar junto al canon y las propuestas")
    ap.add_argument("--check", action="store_true", help="exit 1 si hay errores")
    ap.add_argument("--matriz", action="store_true", help="imprime tema × pueblo")
    ap.add_argument("--escribir", action="store_true", help="con --matriz: reescribe COMPARADA.md")
    args = ap.parse_args(argv)

    archivos, problemas = compilar(args.rutas)
    errores = [p for p in problemas if p.nivel == "error"]
    if args.matriz:
        texto = matriz(archivos)
        if args.escribir:
            os.makedirs(HERMANAS_DIR, exist_ok=True)
            with open(COMPARADA, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(texto)
            print(f"  → {_rel(COMPARADA)} reescrito ({len(_hechos(archivos))} hechos)")
        else:
            print(texto)
        if errores:
            print(f"⚠ la matriz se calculó con {len(errores)} error(es) de validación:")
            for p in errores:
                print(p)
        return 1 if (args.check and errores) else 0

    informe(archivos, problemas)
    return 1 if (args.check and errores) else 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
