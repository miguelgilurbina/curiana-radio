#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — semilla del wiki caquetío, generada desde el vault
=============================================================

Emite `content/wiki/**/*.json` en el repo de Curiana Radio (carpeta hermana
de esta): el **marco teórico** de la simulación, publicado como una wiki
sobre el pueblo caquetío y las sociedades del Golfete de Coro.

EL EJE: RESULTADOS, NO PROCESO
-------------------------------
Decisión de Miguel, 2026-08-24. La primera versión de este exportador
publicaba las 40 notas de `4-fuentes/` como artículos — y esas notas son la
**bitácora del minado**: "qué es · estado técnico · qué ha dado". Eso es
cómo llegamos, no qué sabemos.

El eje ahora es el objeto, no la procedencia:

    pueblo   los ensayos — el argumento con su evidencia
    lengua   cómo es el caquetío reconstruido
    biblio   las obras, como referencia, no como artículo

Los `mapa-*.md` **no se publican**: son índices de navegación del vault
(ver INDICE.md, "un mapa navega, un ensayo argumenta"), y en una wiki con su
propia navegación duplicarían el menú. Su contenido de valor ya está en los
ensayos a los que apuntan.

QUÉ NO INCLUYE — a propósito
-----------------------------
`1-plan/` (roadmap interno), `5-experimento/` (tiene su propia superficie en
/simulador/experimento), `4-fuentes/sesiones/` (bitácora), `6-fusion/` (cola
de trabajo), los `*.yaml` de datos crudos, y las notas de fontanería del
vault (`datos-de-lengua`, `mapa-lengua`).

Uso:
    python export_wiki_seed.py
    python export_wiki_seed.py --dry-run     # no escribe, solo reporta
"""

import argparse
import datetime
import io
import json
import os
import re
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)                    # proyecto-linguistico-caquetío/
CURIANA_RADIO = os.path.dirname(REPO)            # Curiana Radio/
SALIDA = os.path.join(CURIANA_RADIO, "content", "wiki")

_FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.M)
_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
_MD_STRIP = re.compile(r"[`*_>#]|\[\[|\]\]|\[([^\]]*)\]\([^)]*\)")
_MD_EMFASIS = re.compile(r"[*_`]")
_URL = re.compile(r"https?://\S+")

# ── El orden es editorial, y el slug es público ───────────────────────
# Una wiki se lee en un orden pensado, y sus URLs las lee gente. Los
# nombres de archivo del vault (`01_familia_caquetia`, `CULTURA_CAQUETIA`)
# sirven para ordenar carpetas, no para una barra de direcciones: aquí se
# renombran. El orden es el de la lista.
#
#   (ruta en el vault, slug público, título — None = el H1 de la nota)
PUEBLO = [
    ("3-mundo/CULTURA_CAQUETIA.md",         "vida-cotidiana",     "La vida en La Curiana"),
    ("3-mundo/ensayos/01_familia_caquetia.md",   "familia",       None),
    ("3-mundo/ensayos/02_ecologia_golfete.md",   "ecologia",      None),
    ("3-mundo/ensayos/03_creencia_caquetia.md",  "creencia",      None),
    ("3-mundo/ensayos/04_transmision_saber.md",  "transmision",   "¿Cómo sabía el caquetío lo que sabía?"),
    ("3-mundo/ensayos/05_geografia_politica_y_sucesion.md", "geografia-politica", None),
    ("3-mundo/polities-caquetias.md",       "polities",           None),
    ("3-mundo/esfera-de-interaccion.md",    "esfera-de-interaccion", None),
    ("3-mundo/horizonte-de-contacto.md",    "horizonte-de-contacto", None),
    ("3-mundo/cronista.md",                 "cronista",           None),
]

LENGUA = [
    ("2-lengua/lexicon.md",            "lexico",             None),
    ("2-lengua/morfologia.md",         "morfologia",         None),
    ("2-lengua/toponimia.md",          "toponimia",          None),
    ("2-lengua/metodo-comparativo.md", "metodo-comparativo", None),
    ("2-lengua/fonotactica.md",        "fonotactica",        None),
]

ARTICULOS = [("pueblo", PUEBLO), ("lengua", LENGUA)]

# La bibliografía se recolecta entera de 4-fuentes/, sin lista a mano: son 40
# y crecen. Estas quedan fuera por no ser obras.
BIBLIO_DIR = "4-fuentes"
BIBLIO_EXCLUIR = {"INDICE_FUENTES.md"}


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def frontmatter_y_cuerpo(path):
    with open(path, encoding="utf-8") as fh:
        texto = fh.read()
    m = _FM.match(texto)
    if not m:
        return {}, texto
    datos = yaml.safe_load(m.group(1))
    return (datos if isinstance(datos, dict) else {}), texto[m.end():]


def _json_seguro(valor):
    """Recursivo: fechas YAML (datetime.date) → isoformat, para json.dumps."""
    if isinstance(valor, (datetime.date, datetime.datetime)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {k: _json_seguro(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [_json_seguro(v) for v in valor]
    return valor


def _limpiar(texto):
    """Quita marcado de énfasis — el título se pinta como texto, no como MDX."""
    return re.sub(r"\s+", " ", _MD_EMFASIS.sub("", str(texto))).strip()


def extraer_titulo(cuerpo, fm, slug, override=None):
    m = _H1.search(cuerpo)
    cuerpo_sin_h1 = _H1.sub("", cuerpo, count=1).lstrip("\n") if m else cuerpo
    if override:
        return _limpiar(override), cuerpo_sin_h1
    if m:
        return _limpiar(m.group(1)), cuerpo_sin_h1
    return _limpiar(fm.get("obra") or fm.get("titulo") or slug), cuerpo


_SEPARADOR = re.compile(r"^---\s*$", re.M)

# El sitio renderiza estos cuerpos con MDX, y MDX no es Markdown: `<` abre
# JSX y `{` abre una expresión. El vault es Markdown puro escrito por humanos,
# así que tarde o temprano aparece un `<https://…>` o un `{` en prosa y el
# build revienta a las 800 páginas. Se neutraliza aquí, en el origen.
_CODIGO = re.compile(r"```.*?```|`[^`\n]*`", re.S)   # vallas y código en línea
_AUTOLINK = re.compile(r"<(https?://[^>\s]+)>")


def escapar_para_mdx(md):
    """Neutraliza `<` y `{` fuera de código. Los autolinks Markdown
    (`<https://…>`) se convierten en enlaces normales en vez de escaparse,
    que si no se verían como texto con picos."""
    def limpiar(fragmento):
        fragmento = _AUTOLINK.sub(r"[\1](\1)", fragmento)
        return fragmento.replace("<", "&lt;").replace("{", "&#123;")

    salida, pos = [], 0
    for m in _CODIGO.finditer(md):
        salida.append(limpiar(md[pos:m.start()]))
        salida.append(m.group(0))       # el código se deja intacto
        pos = m.end()
    salida.append(limpiar(md[pos:]))
    return "".join(salida)


def separar_preambulo(cuerpo):
    """→ (cuerpo_sin_preambulo, [slugs de obras citadas])

    Los ensayos abren con un bloque dirigido al equipo, no al lector:

        *Sesión 1/4 del programa "corpus cultural" …*
        > **Mapa** · [[mapa-familia]] — [[01_familia|hoja de fuentes]] …
        > **Fuentes** · [[oliver-1989-cap3]] · [[jahn-1927]] …
        ---

    Eso es proceso de minado. Se quita del cuerpo — **pero la lista de obras
    no se tira**: se devuelve aparte para que la ficha del artículo la
    muestre como «sobre qué se sostiene esto», que sí le importa a quien lee.

    Conservador a propósito: solo recorta si lo que hay antes del primer
    `---` es exclusivamente itálicas, cita en bloque y blancos. Si hay prosa
    real ahí, no toca nada.
    """
    m = _SEPARADOR.search(cuerpo)
    if not m:
        return cuerpo, []
    cabeza, resto = cuerpo[:m.start()], cuerpo[m.end():]

    for linea in cabeza.strip().splitlines():
        l = linea.strip()
        if l and not (l.startswith(">") or (l.startswith("*") and l.endswith("*"))):
            return cuerpo, []   # hay prosa: no es preámbulo

    citadas = [t.strip() for t, _ in _WIKILINK.findall(cabeza)]
    return resto.lstrip("\n"), citadas


def texto_plano(md, limite=220):
    """Resumen sin marcado, para las tarjetas — no intenta ser perfecto."""
    t = _MD_STRIP.sub(lambda m: m.group(1) or "", md)
    t = re.sub(r"\|", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:limite].rsplit(" ", 1)[0] + "…") if len(t) > limite else t


def que_aporta(cuerpo, limite=200):
    """La primera prosa bajo «## Qué es» de una nota de fuente, para la ficha
    bibliográfica. Sin eso, el primer párrafo que haya."""
    m = re.search(r"^##\s+Qué es\s*$(.*?)(?=^##\s|\Z)", cuerpo, re.M | re.S)
    fragmento = m.group(1) if m else cuerpo
    for parrafo in fragmento.strip().split("\n\n"):
        p = parrafo.strip()
        if p and not p.startswith(("|", ">", "#", "-", "```")):
            return texto_plano(p, limite)
    return texto_plano(fragmento, limite)


def primera_url(texto):
    """Primer enlace en un campo `acceso` en prosa — para «leer la fuente».
    `acceso` es prosa a propósito: no siempre hay un solo link limpio."""
    if not isinstance(texto, str):
        return None
    m = _URL.search(texto)
    return m.group(0).rstrip(".,;:)»") if m else None


def recolectar():
    """→ (id_map, articulos, biblio). id_map resuelve los [[wikilinks]]."""
    id_map = {}
    articulos = []
    biblio = []

    for seccion, lista in ARTICULOS:
        for orden, (rel, slug, override) in enumerate(lista):
            path = os.path.join(REPO, rel)
            if not os.path.isfile(path):
                print(f"  ⚠️  no existe, se omite: {rel}")
                continue
            fm, cuerpo = frontmatter_y_cuerpo(path)
            titulo, cuerpo = extraer_titulo(cuerpo, fm, slug, override)
            cuerpo, citadas = separar_preambulo(cuerpo)
            articulos.append({
                "slug": slug, "seccion": seccion, "orden": orden,
                "titulo": titulo, "fm": fm, "cuerpo": cuerpo, "citadas": citadas,
            })
            # Los [[wikilinks]] del vault citan el NOMBRE DE ARCHIVO, no el
            # slug público: el mapa se indexa por el basename original.
            id_map[os.path.basename(rel)[:-3]] = (seccion, slug, titulo)

    ruta_biblio = os.path.join(REPO, BIBLIO_DIR)
    for nombre in sorted(os.listdir(ruta_biblio)):
        if not nombre.endswith(".md") or nombre in BIBLIO_EXCLUIR:
            continue
        path = os.path.join(ruta_biblio, nombre)
        fm, cuerpo = frontmatter_y_cuerpo(path)
        if fm.get("tipo") != "fuente":
            continue
        slug = nombre[:-3]
        titulo, cuerpo = extraer_titulo(cuerpo, fm, slug)
        biblio.append({
            "slug": slug,
            "titulo": titulo,
            "obra": _limpiar(fm.get("obra") or titulo),
            "autor": fm.get("autor"),
            "anio": str(fm.get("anio")) if fm.get("anio") is not None else None,
            "publicacion": fm.get("publicacion"),
            "genero": fm.get("genero"),
            "aporta": que_aporta(cuerpo),
            "acceso": fm.get("acceso"),
            "lectura_url": primera_url(fm.get("acceso")),
        })
        # La bibliografía no tiene página propia: los [[wikilinks]] a una obra
        # apuntan al ancla de esa obra dentro de la lista.
        id_map[slug] = ("bibliografia", slug, titulo)

    return id_map, articulos, biblio


def resolver_wikilinks(cuerpo, id_map, no_resueltos, origen):
    def sub(m):
        objetivo, alias = m.group(1).strip(), m.group(2)
        info = id_map.get(objetivo)
        if info is None:
            no_resueltos.append((origen, objetivo))
            return alias or objetivo
        seccion, slug, titulo = info
        texto = alias or titulo
        destino = (f"/kaketiana/bibliografia#{slug}" if seccion == "bibliografia"
                   else f"/kaketiana/{seccion}/{slug}")
        return f"[{texto}]({destino})"

    return _WIKILINK.sub(sub, cuerpo)


def emitir(dry_run=False):
    id_map, articulos, biblio = recolectar()
    no_resueltos = []
    indice = []
    por_seccion = {}

    for art in articulos:
        cuerpo = resolver_wikilinks(
            art["cuerpo"], id_map, no_resueltos, f"{art['seccion']}/{art['slug']}")
        # De lo citado en el preámbulo, solo sobreviven las obras: los enlaces
        # a mapas, hojas de sesión y decisiones de GitHub son navegación
        # interna del vault y no significan nada fuera de él.
        fuentes = [{"slug": s, "titulo": id_map[s][2]} for s in art["citadas"]
                   if s in id_map and id_map[s][0] == "bibliografia"]

        pagina = {
            "slug": art["slug"],
            "seccion": art["seccion"],
            "orden": art["orden"],
            "tipo": art["fm"].get("tipo") or "articulo",
            "titulo": art["titulo"],
            "frontmatter": _json_seguro(art["fm"]),
            "cuerpo": escapar_para_mdx(cuerpo.strip()),
            "resumen": texto_plano(cuerpo),
            "fuentes": fuentes,
        }
        indice.append({k: pagina[k] for k in
                       ("slug", "seccion", "orden", "tipo", "titulo", "resumen")})
        por_seccion.setdefault(art["seccion"], []).append(pagina)

    # La bibliografía va entera en un solo archivo: son fichas cortas, y una
    # petición por obra para pintar una lista sería absurdo.
    for b in biblio:
        b["aporta"] = resolver_wikilinks(
            b["aporta"], id_map, no_resueltos, f"bibliografia/{b['slug']}")

    if not dry_run:
        os.makedirs(SALIDA, exist_ok=True)
        for seccion, pags in por_seccion.items():
            dir_seccion = os.path.join(SALIDA, seccion)
            os.makedirs(dir_seccion, exist_ok=True)
            for pagina in pags:
                with open(os.path.join(dir_seccion, f"{pagina['slug']}.json"),
                          "w", encoding="utf-8") as fh:
                    json.dump(pagina, fh, ensure_ascii=False, indent=2)
                    fh.write("\n")

        with open(os.path.join(SALIDA, "bibliografia.json"), "w", encoding="utf-8") as fh:
            json.dump({"n": len(biblio), "obras": biblio}, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

        manifest = {
            "generado": datetime.date.today().isoformat(),
            "n": len(indice),
            "n_biblio": len(biblio),
            "paginas": sorted(indice, key=lambda p: (p["seccion"], p["orden"])),
        }
        with open(os.path.join(SALIDA, "index.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    con_lectura = sum(1 for b in biblio if b["lectura_url"])
    print(f"{len(indice)} artículos · "
          f"{len(por_seccion.get('pueblo', []))} pueblo · "
          f"{len(por_seccion.get('lengua', []))} lengua")
    print(f"{len(biblio)} obras en bibliografía · {con_lectura} con enlace de lectura")
    if no_resueltos:
        unicos = sorted({o for _, o in no_resueltos})
        print(f"\n{len(no_resueltos)} wikilinks sin resolver "
              f"({len(unicos)} destinos distintos, fuera del subconjunto público):")
        for objetivo in unicos:
            print(f"  [[{objetivo}]]")
    print("\n(dry-run: no se escribió nada)" if dry_run else f"\nEscrito en {SALIDA}")


if __name__ == "__main__":
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    emitir(dry_run=args.dry_run)
