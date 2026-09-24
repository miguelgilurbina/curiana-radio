#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — las fichas de palabra, generadas desde el lexicón
===========================================================

Emite `content/wiki/fichas.json` en el repo de Curiana Radio: **una ficha por
voz caquetía** del habla (atestiguada, reconstruida, retroabstraída e
hipotética) y, aparte, las voces que el proyecto retiró del habla
(`FUERA_DEL_HABLA`).

EL EJE
------
Decisión de Miguel (cc.9, 2026-09-23, sobre la propuesta del escriba): «no
mostrar la investigación, mostrar la lengua viva, y que la investigación sea
lo que hay debajo de cada palabra». La unidad es la PALABRA: forma, glosa,
etiqueta epistémica, fuente con página y, si es reconstruida o hipotética, de
qué hermana sale. Se lee en diez segundos y se comparte sola.

Y el mismo criterio que `export_wiki_seed.py` (Miguel, 2026-08-24):
**resultados, no proceso**. La nota de cada entrada del lexicón es la
bitácora de cómo se llegó a ella —tandas, decisiones, rutas de 6-fusion/—;
aquí no se publica. De ella se extrae sólo lo que el lector necesita:

    citas      las obras que la nota cita, con su localizador (página, número
               del glosario, pliego…), enlazadas a la bibliografía
    hermanas   las lenguas hermanas que la nota da como EVIDENCIA de la forma
    sustituye  la voz retirada en cuyo lugar entró

QUÉ NO INCLUYE — a propósito
----------------------------
Las comparandas (wayuu, lokono, achagua… el 80 % del lexicón: son el andamio
de la reconstrucción, no la lengua), las 441 candidatas aisladas de
`lexicon_candidatos.py`, y los topónimos (tienen su propio canon).

⚠️ La extracción de citas y hermanas LEE PROSA. Es determinista y está escrita
contra las notas reales (se revisó entrada por entrada con `--revisar`), pero
no es una clave foránea: la regla 8 del proyecto pide migrar el lexicón a
`procedencia.obra`, y el día que exista, este exportador debe leerla en vez de
adivinar. Hasta entonces, lo que no se reconoce no se inventa: sale sin cita.

Sin la base: lee `curiana_lexicon.py` y el vault, nunca Supabase.

Uso:
    python export_fichas_seed.py
    python export_fichas_seed.py --dry-run     # no escribe, solo reporta
    python export_fichas_seed.py --revisar     # imprime citas y hermanas por voz
"""

import argparse
import datetime
import io
import json
import os
import re
import sys
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)                    # proyecto-linguistico-caquetío/
CURIANA_RADIO = os.path.dirname(REPO)            # Curiana Radio/
SALIDA = os.path.join(CURIANA_RADIO, "content", "wiki", "fichas.json")

sys.path.insert(0, AQUI)
import curiana_lexicon as L                                   # noqa: E402
from export_wiki_seed import (                                # noqa: E402
    BIBLIO_DIR, BIBLIO_EXCLUIR, frontmatter_y_cuerpo)


# ── Las cuatro capas: la marca de la casa ────────────────────────────
# Texto editorial, como los títulos de export_wiki_seed.py. La columna «qué es
# incierto» es la de la decisión que abrió la capa retroabstraída
# (6-fusion/issues-pendientes/publicados/decision-era2-retroabstraido.md);
# el criterio de reconstruida/hipotética es N1 de la tanda de las hermanas
# (6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml, th.6).
CAPAS = {
    "atestiguado": {
        "fuente": "caquetío-atestiguado",
        "etiqueta": "atestiguada",
        "que_es": "Una fuente la registra como voz caquetía, con obra y página.",
        "incierto": "Nada de la forma: es dato histórico.",
    },
    "reconstruido": {
        "fuente": "caquetío-reconstruido",
        "etiqueta": "reconstruida",
        "que_es": ("Ninguna fuente la registra en caquetío. La forma sale de las "
                   "lenguas hermanas —dos que la dan igual, o con una "
                   "correspondencia regular declarada— o de una segunda fuente "
                   "que la corrobora."),
        "incierto": "Que el caquetío la dijera así.",
    },
    "retroabstraido": {
        "fuente": "caquetío-retroabstraido",
        "etiqueta": "retroabstraída",
        "que_es": ("La palabra está viva: se documentó en boca de la península, "
                   "hoy. Se proyecta hacia atrás."),
        "incierto": "No la forma, sino el sustrato: si es caquetía.",
    },
    "hipotetico": {
        "fuente": "caquetío-hipotético",
        "etiqueta": "hipotética",
        "que_es": ("Una conjetura declarada: una sola hermana, una sola fuente "
                   "que la saca de partir un topónimo, o una acuñación de "
                   "trabajo del proyecto."),
        "incierto": "La forma misma: se propuso, no se documentó.",
    },
}
CAPA_DE_FUENTE = {v["fuente"]: k for k, v in CAPAS.items()}

CATEGORIAS = {
    "sust": "sustantivo", "v_raiz": "verbo", "v_estativo": "verbo de estado",
    "part": "partícula", "pron": "pronombre", "adj": "adjetivo",
    "título": "título", "num": "numeral", "topón": "topónimo",
    "interr": "interrogativo",
}


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def slugify(forma: str) -> str:
    s = unicodedata.normalize("NFKD", forma).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# ══════════════════════════════════════════════════════════════════════
# 1. LAS OBRAS — de 4-fuentes/bibliografia.yaml, nunca de una lista a mano
# ══════════════════════════════════════════════════════════════════════

_ANIO = re.compile(r"(1[4-9]\d\d|20[0-2]\d)")

# Un apellido compartido por varias obras sólo se resuelve con una regla
# declarada; si no, NO se cita (lo que no se reconoce no se inventa).
#   apellido → obra por defecto cuando el texto no dice cuál
DESEMPATE = {
    "Zavala": "zavala-reyes-2015",      # el glosario; la de 2018 se cita con «et al.»
    "Arcaya": "arcaya-1920",
    "Castellanos": "castellanos-elegias",
}


def _oliver(texto_siguiente: str, loc: str | None) -> str | None:
    """Oliver 1989 son cinco notas en el vault. El capítulo lo dice el propio
    localizador; si sólo hay página, la lingüística es el cap. 2, cuyo §2.8
    son las pp. 142-151 (frontmatter de oliver-1989-cap2.md)."""
    t = (texto_siguiente[:40] + " " + (loc or "")).lower()
    if "tabla a-" in t or "apéndice a" in t or "apendice a" in t:
        return "oliver-1989-apendice-a"
    m = re.search(r"cap\.\s*(\d)", t)
    if m:
        return {"2": "oliver-1989-cap2", "3": "oliver-1989-cap3",
                "4": "oliver-1989-cap4"}.get(m.group(1))
    paginas = [int(p) for p in re.findall(r"\d+", loc or "")]
    if loc and loc.startswith("p") and paginas and max(paginas) <= 151:
        return "oliver-1989-cap2"
    return None


def _es_nombre(palabra: str) -> bool:
    return len(palabra) >= 4 and palabra[0].isupper() and palabra.isalpha()


def cargar_obras():
    """→ (obras: id → ficha, patrones: [(regex, ids, especifico)])

    Tres clases de patrón, de más a menos seguro:
      · un alias con año («Goeje 1939») o «Apellido AÑO» → cita por sí solo
      · un alias sin año que lleva el nombre del autor («Medina Colina»)
        → cita por sí solo
      · un apellido suelto, o un alias que es un título o un lugar («Cerro
        Santa Ana») → sólo es cita si le sigue un localizador (página, #…)
    Un mismo literal que casa con varias obras («Oliver 1989» son cinco notas)
    lleva todas: lo resuelve el localizador o `DESEMPATE`.
    """
    with open(os.path.join(REPO, BIBLIO_DIR, "bibliografia.yaml"), encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)

    # Qué obras tienen ancla en /kaketiana/bibliografia: las mismas que
    # export_wiki_seed.py publica (nota de 4-fuentes/ con tipo: fuente).
    con_ancla = set()
    ruta = os.path.join(REPO, BIBLIO_DIR)
    for nombre in os.listdir(ruta):
        if nombre.endswith(".md") and nombre not in BIBLIO_EXCLUIR:
            fm, _ = frontmatter_y_cuerpo(os.path.join(ruta, nombre))
            if fm.get("tipo") == "fuente":
                con_ancla.add(nombre[:-3])

    obras = {}
    literales: dict[str, list] = {}          # literal → [ids, especifico]

    def anotar(lit: str, oid: str, especifico: bool) -> None:
        entrada = literales.setdefault(lit, [set(), especifico])
        entrada[0].add(oid)
        entrada[1] = entrada[1] and especifico

    for o in doc["obras"]:
        oid = o["id"]
        autor = re.sub(r"\s*\([^)]*\)", "", str(o.get("autor") or ""))
        apellido = (autor.split(",")[0] if "," in autor else autor.split(" ")[-1]).strip()
        # El año sólo si el campo EMPIEZA por uno: «sin confirmar — posterior
        # a 2000» no es de 2000.
        m_anio = re.match(r"\s*(1[4-9]\d\d|20[0-2]\d)", str(o.get("anio") or ""))
        anios = [m_anio.group(1)] if m_anio else _ANIO.findall(oid)
        aliases = [str(a) for a in (o.get("aliases") or [])]
        # El nombre corto: el alias con año que empieza por el apellido
        # («Goeje 1939», no «de Goeje 1939»), si no el más largo con año.
        con_anio = sorted((a for a in aliases if _ANIO.search(a)),
                          key=lambda a: (not a.lower().startswith(apellido.lower()), -len(a)))
        con_nombre = [a for a in aliases if apellido and apellido in a]
        if con_anio:
            corta = con_anio[0]
        elif all(_es_nombre(p) or p in ("y", "de") for p in apellido.split()) and anios:
            corta = f"{apellido} {anios[0]}"
        elif con_nombre:
            corta = max(con_nombre, key=len)
        else:
            corta = str(o.get("obra") or oid)
        obras[oid] = {"id": oid, "corta": corta, "obra": o.get("obra") or oid,
                      "enlace": oid in con_ancla}

        for a in aliases:
            if len(a) < 5:
                continue
            if _ANIO.search(a):
                anotar(a, oid, True)
                primera = a.split(" ")[0]
                if _es_nombre(primera):
                    anotar(primera, oid, False)     # «Goeje p. 86», «Oviedo p. 205»
            elif " " in a:
                anotar(a, oid, bool(apellido) and apellido.split(" ")[0] in a)
        if apellido and anios:
            anotar(f"{apellido} {anios[0]}", oid, True)
            anotar(f"{apellido} ({anios[0]})", oid, True)
        for palabra in {apellido, apellido.split(" ")[0]}:
            if _es_nombre(palabra) and palabra.lower() != "varios":
                anotar(palabra, oid, False)

    patrones = [(re.compile(r"(?<!\w)" + re.escape(lit) + r"(?!\w)"), ids, esp)
                for lit, (ids, esp) in literales.items()]
    # Para desempatar «González Batista, «El nombre de Coro»»: los títulos y
    # alias de cada obra, buscados justo detrás del apellido.
    for o in doc["obras"]:
        obras[o["id"]]["titulos"] = [str(a) for a in (o.get("aliases") or []) if len(str(a)) >= 5]
    return obras, patrones


# ══════════════════════════════════════════════════════════════════════
# 2. LA NOTA — qué parte es evidencia de ESTA forma
# ══════════════════════════════════════════════════════════════════════

# Se quitan antes de leer: la derivación de la voz VIEJA en su glosa, la
# etiqueta que tuvo, la etiqueta vieja de F8 («pedigrí sin cita»), la lista
# de hermanas PERMITIDAS (cc.12, que no es evidencia de nada), y los incisos
# que contrastan con el wayuu o explican por qué NO se eligió otra forma.
_CLAUSULAS_FUERA = [
    re.compile(r"\(<[^)]*\)"),
    re.compile(r"\(era `[^`]*`\)"),
    re.compile(r"etiquetad[ao] `[^`]*`"),
    re.compile(r"[Ee]tiqueta (?:vieja|anterior):? `[^`]*`"),
    re.compile(r"No viene sólo del wayuu:?"),
    re.compile(r"\(cc\.12:[^)]*\)"),
    re.compile(r"las voces que seguían saliendo del wayuu[.:]?"),
    re.compile(r"donde el wayuu[^).;]*"),
    re.compile(r"`\w+` quedaba a una letra de `\w+`[^.;]*"),
    re.compile(r"[\w./§-]+\.(?:md|yaml|py)\b"),       # rutas del vault
]

# Una oración con estas marcas habla de OTRA voz (la que se sustituyó), de la
# historia de la entrada, o de una hermana que NO la apoya. No es evidencia.
_ORACIONES_FUERA = re.compile("|".join([
    r"\b[Ss]ustituye a\b", r"^\s*Antes:", r"\bNO apoya\b", r"\bno la sostiene\b",
    r"\bno comparte\b", r"\b[Uu]na sola hermana \(", r"\bDEUDA D11\b",
    r"\bdesde el WAYUU\b", r"\bdel wayuu\b", r"\bya no desde el wayuu\b",
    r"\bretiró al wayuunaiki\b", r"\bcircular\b", r"^\s*Propuesta:",
    r"\b[Dd]ecisión:", r"pasa a `[^`]+-(?:lokono|achagua)`",
    r"\botra raíz\b", r"\b[Cc]andidat[oa]s?\b", r"\bno está en\b",
    r"\bdistinguen el género\b", r"\bpero\b[^.]*\ba una letra\b",
    r"\b[Ll]ectura descartada\b", r"`\w+` se archivó", r"\bpoporo\b",
    r"\bpalabra distinta\b", r"\bno salía de ninguna fuente\b", r"\bReparos\b",
    r"\bno la tiene\b", r"^\s*Deuda:", r"^\s*Ver\b", r"^`\w+` se queda\b",
]), re.I)

_ABREV = {"p", "pp", "cap", "s.v", "izq", "der", "Lok", "Way", "Tno", "cf",
          "n", "vol", "t", "Sg", "cm", "ed", "trad", "fr", "Ven", "Cast", "Eleg"}


def oraciones(texto: str) -> list[str]:
    """Parte en oraciones sin partir «p. 74», «Lok. ma-» ni lo que hay dentro
    de un paréntesis («(Perea Alonso 1942 p. 573; Adam 1879 p. 278)»)."""
    salida, inicio = [], 0
    for m in re.finditer(r"[.;]\s+(?=[A-ZÁÉÍÓÚÑ«¿`])|\s·\s", texto):
        antes = texto[inicio:m.start()]
        if m.group(0).strip() != "·":
            if antes.count("(") > antes.count(")"):
                continue
            ultima = re.split(r"[\s(]", antes.strip())[-1] if antes.strip() else ""
            if ultima in _ABREV or len(ultima) == 1:
                continue
        salida.append(texto[inicio:m.end()].strip())
        inicio = m.end()
    salida.append(texto[inicio:].strip())
    return [s for s in salida if s]


def evidencia(entrada: dict) -> list[str]:
    """Las oraciones de la nota que hablan de la evidencia de ESTA forma.
    La nota crece por capas separadas por « · »; una capa que empieza por
    «Antes:» o «DESCARTADA» es la historia de la entrada (o una lectura que
    se tiró) y se descarta entera."""
    texto = " · ".join(t for t in (entrada.get("notas"), entrada.get("glosa_fuente")) if t)
    capas = [c for c in texto.split(" · ")
             if not re.match(r"\s*(?:Antes:|DESCARTADA\b)", c)]
    texto = " · ".join(capas)
    for patron in _CLAUSULAS_FUERA:
        texto = patron.sub("", texto)
    return [o for o in oraciones(texto) if not _ORACIONES_FUERA.search(o)]


# ── Localizador: lo que sigue a la obra ──────────────────────────────
_LOC = re.compile(r"""^\s*[,:]?\s*\(?
    (?:\d{4}\)?\s*[,:]?\s*)?                        # el año, si el patrón no lo llevaba
    (?:(?:Del\ Habla\ Paraguanera|arte|glosario|Ap[ée]ndice\ A|nota\ al\ pie)[,]?\s*)?
    (?:cap\.\s*\d+\s*,?\s*)?
    (?P<loc>
        \#\s?\d+(?:\s*\([A-Z]{1,4}(?:\+[A-Z]{1,4})*\))?
      | pp?\.\s?\d+(?:\s*[-–]\s*\d+)?(?:\s*(?:,|y)\s*\d+(?:\s*[-–]\s*\d+)?)*
      | :\s?\d+
      | pliegos?\s+\d+\w*(?:\s+(?:izq|der)\.?)?(?:\s*[-–]\s*\d+\w*)?
      | Tabla\s+A-\d+
      | §\s?\d+(?:\.\d+)*
      | página\s+no\s+dictada
      | nota\ al\ pie\ \(\d+\)
      | \(\d+\)
      | cap\.\s*[\dIVXL]+
    )""", re.X)


def _limpiar_loc(loc: str) -> str:
    loc = re.sub(r"\s+", " ", loc.strip())
    loc = re.sub(r"^(pp?)\.(\d)", r"\1. \2", loc)
    loc = re.sub(r"^#\s", "#", loc)
    if loc.startswith(":"):
        loc = "p. " + loc[1:].strip()
    if re.fullmatch(r"\(\d+\)", loc):
        loc = "nota al pie " + loc
    return loc


# ── Citas genéricas: «Pet 1987», «Captain & Captain 2005» ────────────
# Obras que la nota cita y el vault no tiene: salen sin enlace. El año va
# de 1492 a 2025 para no confundir con las fechas de las decisiones.
_CITA_SUELTA = re.compile(
    r"(?<!\w)([A-ZÁÉÍÓÚ][a-záéíóúñü]+(?:\s(?:y|&)\s[A-ZÁÉÍÓÚ][a-záéíóúñü]+)?)"
    r"\s\(?(1[4-9]\d\d|20[01]\d|202[0-5])\)?(?![\d-])")
_NO_ES_AUTOR = {"Decisión", "Tanda", "Campaña", "Miguel", "Antes", "Fraseario",
                # lugares: «Aruba 1882», «Barquisimeto 1579» fechan un hecho, no una obra
                "Aruba", "Curazao", "Bonaire", "Barquisimeto", "Coro", "Paraguaná",
                "Falcón", "Venezuela", "Cuba", "Maracaibo"}


def citas_de(oraciones_ev: list[str], obras, patrones) -> list[dict]:
    texto = " ".join(oraciones_ev)
    encontrados = []
    for rx, ids, especifico in patrones:
        for m in rx.finditer(texto):
            encontrados.append((m.start(), m.end(), ids, especifico))
    # El más largo gana en cada tramo («Zavala Reyes 2015» sobre «Zavala»).
    encontrados.sort(key=lambda e: (e[0], -(e[1] - e[0])))
    elegidos, hasta = [], -1
    for e in encontrados:
        if e[0] >= hasta:
            elegidos.append(e)
            hasta = e[1]

    por_obra: dict[str, dict] = {}
    orden: list[str] = []
    for ini, fin, ids, especifico in elegidos:
        m = _LOC.match(texto[fin:fin + 90])
        loc = _limpiar_loc(m.group("loc")) if m else None
        # «González Batista, «El nombre de Coro»»: el título detrás del
        # apellido vale como localizador y dice cuál de las obras es.
        detras = texto[fin:fin + 50]
        por_titulo = [i for i in ids
                      if any(t in detras for t in obras.get(i, {}).get("titulos", []))]
        if not especifico and not loc and not por_titulo:
            continue                    # un apellido suelto en prosa no es cita
        oid = None
        if len(ids) == 1:
            oid = next(iter(ids))
        elif all(i.startswith("oliver-") for i in ids):
            oid = _oliver(texto[fin:fin + 60], loc)
        elif len(por_titulo) == 1:
            oid = por_titulo[0]
        else:
            apellido = texto[ini:fin].split(" ")[0]
            oid = DESEMPATE.get(apellido)
            if oid == "zavala-reyes-2015" and re.match(r"\s*(?:Reyes\s)?et al", detras):
                oid = "zavala-reyes-2018"
        if not oid or oid not in obras:
            continue
        if oid not in por_obra:
            por_obra[oid] = {"obra": oid, "titulo": obras[oid]["corta"],
                             "enlace": obras[oid]["enlace"], "localizadores": []}
            orden.append(oid)
        locs = por_obra[oid]["localizadores"]
        if loc and not any(x.startswith(loc) for x in locs):
            # «#227» y «#227 (E)» son el mismo lugar: queda el más completo
            locs[:] = [x for x in locs if not loc.startswith(x)] + [loc]

    ya = {por_obra[o]["titulo"].split(" ")[0] for o in orden}
    sueltas = []
    for m in _CITA_SUELTA.finditer(texto):
        autor, anio = m.group(1), m.group(2)
        if autor in _NO_ES_AUTOR or autor.split(" ")[0] in ya:
            continue
        # ¿La cubre ya una obra del vault? (p. ej. «Zavala Reyes 2015»)
        if any(e[0] <= m.start() < e[1] for e in elegidos):
            continue
        titulo = f"{autor} {anio}"
        if titulo not in sueltas:
            sueltas.append(titulo)

    salida = [por_obra[o] for o in orden]
    for oid in salida:
        oid["localizadores"] = oid["localizadores"][:4]
    salida += [{"obra": None, "titulo": t, "enlace": False, "localizadores": []}
               for t in sueltas]
    return salida[:6]


# ── Hermanas: la lengua que da la forma ──────────────────────────────
HERMANAS = [
    ("lokono", re.compile(r"\blokon[oa]s?\b|\bLok\.|\bLK\b", re.I | re.A)),
    # «lokono X → mujeres Y» es la notación de Adam 1879 (el habla de las
    # mujeres kalinago frente al arahuaco)
    ("kalinago", re.compile(r"\bkalinago\b|\bKL\b|\bmujeres\s*«", re.I)),
    ("achagua", re.compile(r"\bachagua\b", re.I)),
    ("taíno", re.compile(r"\btaín[oa]s?\b|\bTno\.|\bTN\b")),
    ("wayuu", re.compile(r"\bwayuu\b|\bwayu+naiki\b|\bWay\.|\bWY\b|\bguajiro\b", re.I)),
    ("paraujano", re.compile(r"\bparaujano\b|\bPJ\b")),
    ("garífuna", re.compile(r"\bgar[ií]funa\b", re.I)),
    ("proto-arahuaco", re.compile(r"proto-?ara(?:h)?ua(?:k|c)o?\w*|proto-arawak\w*", re.I)),
]
# Lo que una fuente trae de una hermana se reconoce por la obra: Perea es el
# lokono de los moravos, Neira y Ribero el achagua, Goeje y Adam el kalinago.
HERMANA_DE_OBRA = {
    "perea-alonso-1942": "lokono",
    "neira-ribero-1762": "achagua",
}
_SIN_OBRA = re.compile(r"forma justificada por cognado en|sin obra citada|sin cita")


_KALINAGO_DE_MUJERES = re.compile(r"mujeres\s+kalinago|kalinago\s+de\s+mujeres|mujeres\s*«", re.I)


def hermanas_de(oraciones_ev: list[str], obras, patrones) -> list[dict]:
    """Cada lengua hermana que la nota da como evidencia. `citada` = en la
    misma oración hay una obra; si no, es el «cognado en X» sin obra que la
    tanda de las hermanas desacreditó. Ésas sólo se muestran si no hay
    ninguna citada — y entonces se dice que no tienen obra."""
    vistas: dict[str, dict] = {}
    for o in oraciones_ev:
        citas = citas_de([o], obras, patrones)
        sin_obra = bool(_SIN_OBRA.search(o)) and not citas
        encontradas = [h for h, rx in HERMANAS if rx.search(o)]
        for c in citas:
            h = HERMANA_DE_OBRA.get(c["obra"] or "")
            if h and h not in encontradas:
                encontradas.append(h)
        for h in encontradas:
            # «kalinago de mujeres» sólo si la nota lo dice así: el kalinago
            # de los hombres y el común también se citan (ani, uli).
            etiqueta = ("kalinago de mujeres"
                        if h == "kalinago" and _KALINAGO_DE_MUJERES.search(o) else h)
            prev = vistas.get(h)
            if prev is None:
                vistas[h] = {"lengua": etiqueta, "citada": not sin_obra}
            else:
                prev["citada"] = prev["citada"] or not sin_obra
                if etiqueta == "kalinago de mujeres":
                    prev["lengua"] = etiqueta
    todas = list(vistas.values())
    citadas = [h for h in todas if h["citada"]]
    return citadas or todas


_SUSTITUYE = re.compile(r"[Ss]ustituye a `([^`]+)`")
# De dónde sale una voz que no cita forma de nadie: se declara, no se calla
# (regla 8). La acuñación de F8 que después ganó hermanas (marisi) deja de
# serlo: por eso se mira también si hay cita.
_ACUNACION = re.compile(r"acuñación para la simulación sin cita|forma sin cita ni derivación")
_COMPUESTO = re.compile(r"compuesto de trabajo del proyecto")
_SIN_PAREJA = re.compile(r"ninguna hermana")


def glosa_de_fuente(entrada: dict) -> str | None:
    """La glosa tal como la escribe la fuente, si dice algo que la glosa del
    canon no dice ya (a menudo es la misma, con mayúscula)."""
    g = entrada.get("glosa_fuente")
    if not g:
        return None
    g = re.sub(r"\s*\[[^\]]*\]\s*$", "", g).strip()

    def llana(t: str) -> str:
        return re.sub(r"[\W_]+", " ", t).strip().lower()
    return g if g and llana(g) != llana(entrada.get("sig", "")) else None


def siglas_zavala() -> dict[str, str]:
    """Las siglas del glosario de Zavala Reyes 2015 (quién le dio cada voz),
    leídas de su nota en el vault: «PMA = Pedro Manuel Arcaya, HB = …»."""
    ruta = os.path.join(REPO, BIBLIO_DIR, "zavala-reyes-2015.md")
    try:
        with open(ruta, encoding="utf-8") as fh:
            texto = fh.read()
    except FileNotFoundError:
        return {}
    m = re.search(r"identificados por siglas:(.*?)\)", texto, re.S)
    if not m:
        return {}
    pares = re.findall(r"\b([A-Z]{1,4})\s*=\s*([^,]+)", re.sub(r"\s+", " ", m.group(1)))
    return {s: nombre.strip() for s, nombre in pares}


# ══════════════════════════════════════════════════════════════════════
# 3. LAS VOCES RETIRADAS
# ══════════════════════════════════════════════════════════════════════

# El motivo en una frase llana. Se lee primero el campo `archivada` (el
# motivo VIGENTE: `joutai` se archivó por la política y hoy lo está por D11)
# y, si no lo hay, la nota. El orden importa: la primera que casa gana.
MOTIVOS = [
    ("no-caquetia", re.compile(r"no es caquetía|no era caquetía"),
     "No era caquetía: las fuentes que la sostenían hablaban de otro pueblo."),
    ("editor", re.compile(r"forma y glosa del editor"),
     "La forma no era de ningún cronista: la puso un editor del siglo XIX."),
    ("wayuu", re.compile(r"derivada del wayuu|etiquetada wayuu|\bD11\b|reconstruida desde el WAYUU"),
     "Salía del wayuu, que dejó de contar como lengua hermana."),
    ("atestiguada-manda", re.compile(r"atestiguado-manda|manda `|manda la atestiguada|ATESTIGUA\b"),
     "Hay una voz atestiguada para lo mismo, y donde hay atestiguada, manda ella."),
    ("sin-obra", re.compile(r"núcleo fundacional|citaba «cognado»|sin cita"),
     "Citaba un parentesco sin obra ni página; la sustituye una forma de las hermanas."),
]


def _motivo(e: dict) -> tuple[str, str]:
    notas = str(e.get("notas") or "")
    marca = re.search(r"(?:RETIRADA|ARCHIVADA) DEL HABLA", notas)
    for texto in (str(e.get("archivada") or ""), notas[marca.start():] if marca else notas):
        for clave, rx, frase in MOTIVOS:
            if rx.search(texto):
                return clave, frase
    lengua = e.get("fuente")
    if lengua and not L.capa_epistemica(lengua):
        return "no-caquetia", f"No era caquetía: es voz {lengua}."
    return "otra", "Retirada del habla; su nota conserva el porqué."


def retiradas(vivas: dict[str, str]) -> list[dict]:
    salida = []
    for clave, e in L.FUERA_DEL_HABLA.items():
        capa_cruda = L.capa_epistemica(e.get("fuente", ""))
        texto = " ".join(str(e.get(c) or "") for c in ("archivada", "notas"))
        fue_del_habla = capa_cruda or re.search(r"RETIRADA DEL HABLA|ARCHIVADA DEL HABLA", texto)
        otra_lengua_reconstruida = (not capa_cruda
                                    and (e.get("fuente") or "").endswith("-reconstruido"))
        if not fue_del_habla or otra_lengua_reconstruida:
            continue          # reconstrucciones de OTRA lengua (el taíno desde el lokono)
        arch = str(e.get("archivada") or "")
        m = re.match(r"(\d{4}-\d{2}-\d{2})", arch) or re.search(
            r"(?:RETIRADA|ARCHIVADA) DEL HABLA[^0-9]{0,4}(\d{4}-\d{2}-\d{2})", texto)
        fecha = m.group(1) if m else None
        if not fecha:
            m = re.search(r"\((\d{4}-\d{2}-\d{2})\)\s*—\s*RETIRADA", texto)
            fecha = m.group(1) if m else None
        sustitutas = []
        for patron in (r"manda `([^`]+)`", r"la sustituye `([^`]+)`",
                       r"manda (\w+)(?: / (\w+))?", r"su lugar lo ocupa `([^`]+)`"):
            for mm in re.finditer(patron, arch if "lugar" not in patron else texto):
                for g in mm.groups():
                    if g and g not in sustitutas:
                        sustitutas.append(g)
            if sustitutas:
                break
        motivo = _motivo(e)
        salida.append({
            "forma": clave,
            "ancla": "r-" + slugify(clave),
            "glosa": e.get("sig", ""),
            "capa": CAPA_DE_FUENTE.get(capa_cruda or "", None),
            "lengua": None if capa_cruda else e.get("fuente"),
            "fecha": fecha,
            "motivo": motivo[0],
            "motivo_texto": motivo[1],
            "sustitutas": [{"forma": s, "slug": vivas.get(s)} for s in sustitutas],
        })
    salida.sort(key=lambda r: (r["fecha"] or "", r["forma"]), reverse=True)
    return salida


# ══════════════════════════════════════════════════════════════════════
# 4. LA SEMILLA
# ══════════════════════════════════════════════════════════════════════

def construir():
    obras, patrones = cargar_obras()
    vivas = {k: slugify(k) for k, v in L.VOCABULARIO_BASE.items()
             if L.capa_epistemica(v.get("fuente", ""))}
    slugs = list(vivas.values())
    duplicados = {s for s in slugs if slugs.count(s) > 1}
    if duplicados:
        raise SystemExit(f"slugs repetidos: {sorted(duplicados)} — hay que desambiguar")

    retiradas_ = retiradas(vivas)
    retirada_por_forma = {r["forma"]: r for r in retiradas_}

    fichas = []
    for clave, e in sorted(L.VOCABULARIO_BASE.items(), key=lambda kv: slugify(kv[0])):
        capa_cruda = L.capa_epistemica(e.get("fuente", ""))
        if not capa_cruda:
            continue
        capa = CAPA_DE_FUENTE[capa_cruda]
        ev = evidencia(e)
        notas = " ".join(t for t in (e.get("notas"), e.get("glosa_fuente")) if t)
        citas = citas_de(ev, obras, patrones)
        hermanas = []
        if capa in ("reconstruido", "hipotetico"):
            hermanas = hermanas_de(ev, obras, patrones)
        origen = None
        if _COMPUESTO.search(notas):
            origen = "compuesto"          # sus piezas citan; el compuesto es nuestro
        elif _ACUNACION.search(notas) and not citas and not hermanas:
            origen = "acunacion"
        sustituye = []
        for s in _SUSTITUYE.findall(notas):
            r = retirada_por_forma.get(s)
            if s not in [x["forma"] for x in sustituye]:
                sustituye.append({"forma": s, "ancla": r["ancla"] if r else None,
                                  "glosa": r["glosa"] if r else None})
        forma_fuente = e.get("forma_fuente")
        fichas.append({
            "slug": vivas[clave],
            "forma": clave,
            "forma_fuente": forma_fuente if forma_fuente and forma_fuente.lower() != clave else None,
            "glosa": e.get("sig", ""),
            "glosa_fuente": glosa_de_fuente(e),
            "categoria": CATEGORIAS.get(e.get("cat", ""), e.get("cat")),
            "capa": capa,
            "citas": citas,
            "hermanas": hermanas,
            "origen": origen,
            "sin_pareja": bool(capa in ("reconstruido", "hipotetico") and _SIN_PAREJA.search(notas)),
            "sustituye": sustituye,
            # Lo que sólo la corrida base puede decir: quién la dijo primero,
            # cuántas veces, en qué lugar. Hueco declarado, no olvidado.
            "en_la_simulacion": None,
        })

    por_capa = {k: sum(1 for f in fichas if f["capa"] == k) for k in CAPAS}
    return {
        "generado": datetime.date.today().isoformat(),
        "fuente_de_verdad": "proyecto-linguistico-caquetío/curiana_sim/curiana_lexicon.py",
        "n": len(fichas),
        "por_capa": por_capa,
        "con_cita": sum(1 for f in fichas if f["citas"]),
        "capas": CAPAS,
        "siglas_zavala": siglas_zavala(),
        "pendiente_de_la_corrida_base": [
            "quién dijo primero cada palabra y en qué día",
            "cuántas veces se dijo, y en qué lugar del mapa",
            "si entró en la koiné",
        ],
        "fichas": fichas,
        "retiradas": retiradas_,
    }


def revisar(semilla) -> None:
    for f in semilla["fichas"]:
        citas = "; ".join(c["titulo"] + (" " + ", ".join(c["localizadores"]) if c["localizadores"] else "")
                          for c in f["citas"])
        hermanas = ", ".join(h["lengua"] + ("" if h["citada"] else " (sin obra)") for h in f["hermanas"])
        marcas = " ".join(m for m, v in (((f["origen"] or "").upper(), f["origen"]),
                                          ("SIN-PAREJA", f["sin_pareja"])) if v)
        print(f"{f['forma']:14} {f['capa'][:5]:5} | {hermanas:40} | {citas} {marcas}")
    print()
    for r in semilla["retiradas"]:
        sust = ", ".join(s["forma"] for s in r["sustitutas"])
        print(f"  retirada {r['forma']:10} {r['fecha']} {r['motivo']:18} → {sust}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--revisar", action="store_true")
    args = ap.parse_args(argv)

    semilla = construir()
    if args.revisar:
        revisar(semilla)
    if not args.dry_run:
        os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
        with open(SALIDA, "w", encoding="utf-8") as fh:
            json.dump(semilla, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    print(f"{semilla['n']} fichas · " + " · ".join(f"{k} {v}" for k, v in semilla["por_capa"].items()))
    print(f"{semilla['con_cita']} con al menos una cita · {len(semilla['retiradas'])} voces retiradas")
    print("(dry-run: no se escribió nada)" if args.dry_run else f"Escrito en {SALIDA}")
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
