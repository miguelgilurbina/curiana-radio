#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — la costa occidental en las crónicas del primer contacto: el barrido medido
===================================================================================

Tercera campaña de minería, parcela **M2** (2026-09-22). Emite las cifras que
citan `6-fusion/cronicas_contacto_costa_occidental_2026-09-22.yaml` y su issue.
**Ninguna cifra de esos documentos está escrita a mano** (regla 1): salen de
aquí. No escribe nada en el repo: sólo lee las cinco obras y cuenta.

LA PREGUNTA
-----------
¿Qué cuentan Anglería, Navarrete (t. I y t. III) y Hernando Colón de la COSTA
DE TIERRA FIRME occidental —Coquibacoa, el cabo de San Román, Coro, Curiana,
las islas de los Gigantes— y de su gente? La campaña del taíno (T7) los leyó
sólo para el contacto con las Antillas; esto mide la otra pregunta.

QUÉ MIDE
--------
1. **La ortografía, ANTES de contar** (skill `minar-fuente` §2). Cada diana es
   una raíz corta sobre el texto NORMALIZADO (sin marcas, minúsculas, mismo
   largo que el original, para poder citar el crudo). Y se declaran los
   positivos de control (`isla`, `oro`, `indio`, `rescat`): un cero se lee
   junto a ellos (regla 6). Las consultas de varias palabras van con `\\s+`,
   porque el OCR de archive.org separa con DOS espacios (trampa de T7).

2. **Las grafías de Coquibacoa**, todas: el OCR las destroza
   (`Qoiquevacoa`, `Caquevacoa`, `Coywvaeoa`) y cada una es un dato para el
   topónimo (`toponimo-034`, D5). Se listan con su folio, no se corrigen.

3. **Las dos Curianas.** Cada acierto de `curiana` en Navarrete t. III, con el
   TRAMO en que cae: la de Niño y Guerra (1499, costa centro-oriental) y la de
   Hojeda 1502 («que los indios llamaban Curiana y él nombró Valfermoso»).
   Separarlas es el encargo.

4. **Dónde cae cada acierto.** En Anglería, la página impresa sale de los
   marcadores del `.txt` (vol. 1: impresa = pdf − 64). En los `.txt` de
   archive.org el folio impreso va en la cabecera de cada página y el OCR lo
   estropea a veces (`303` por `203`): el medidor se queda con la cadena de
   cabeceras que crece a ritmo de página verosímil, y entre dos cabeceras no
   consecutivas interpola y lo marca con «≈». Es una GUÍA para ir al pasaje;
   la página que cita el YAML se leyó a mano en la cabecera del propio texto.

Uso:
    python 6-fusion/scripts/medir_cronicas_costa_occidental.py
    python 6-fusion/scripts/medir_cronicas_costa_occidental.py --json
    python 6-fusion/scripts/medir_cronicas_costa_occidental.py --contexto curiana
    python 6-fusion/scripts/medir_cronicas_costa_occidental.py --contexto fauna --obra navarrete-t3
"""

import argparse
import io
import json
import os
import re
import sys
import unicodedata

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(_AQUI))
FUENTES = os.path.join(REPO, "fuentes_caquetios")

# ── Las obras ────────────────────────────────────────────────────────────
# `paginacion`:
#   marcadores  el .txt lleva «=== pdf N · impresa M ===» (lo escribió esta
#               parcela con pdftotext; ver la ficha de Anglería)
#   cabeceras   .txt de archive.org: el folio impreso va en la cabecera
OBRAS = {
    "angleria-v1": {
        "archivo": "Angleria_1892_Fuentes_Historicas_Colon_America_vol1.txt",
        "obra": "angleria-1892 vol. 1",
        "paginacion": "marcadores",
        # Libros de la Década I (impresa). El VIII es el viaje de Niño y Guerra.
        "tramos_impresa": {
            "introducción y cartas (hasta la Década I)": (-63, 96),
            "Década I, libros I-VII (islas, Paria)": (97, 300),
            "Década I, libro VIII (Niño y Guerra: Curiana, Cauchieto)": (301, 318),
            "Década I, libros IX-X y apéndice": (319, 396),
        },
    },
    "angleria-v4": {
        "archivo": "Angleria_1892_Fuentes_Historicas_Colon_America_vol4.txt",
        "obra": "angleria-1892 vol. 4",
        "paginacion": "marcadores",
        "tramos_impresa": {},
    },
    "navarrete-t3": {
        "archivo": "Navarrete_1829_Coleccion_Viages_t3_Viages_Menores_Vespucio.txt",
        "obra": "navarrete-1829-viages-menores",
        "paginacion": "cabeceras",
        # Tramos por ANCLAS de texto (se buscan sobre el texto normalizado,
        # con `\s+`). Si un ancla no aparece, el medidor falla en voz alta: no
        # finge un tramo vacío.
        "anclas": [
            ("Sección 1.ª: Hojeda-La Cosa-Vespucio 1499",
             r"fue el primero en aprestarse alonso de hojeda"),
            ("Sección 1.ª: Niño y Guerra 1499-1500 (Curiana, Cauchieto)",
             r"los hechos de hojeda y cosa hicieron menos"),
            ("Sección 1.ª: Pinzón, Lepe, Vélez, Guerra 1501",
             r"entonces mismo extendio considerablemente"),
            ("Sección 1.ª: Bastidas 1500-1502",
             r"mas conocido y famoso es el viage de rodrigo"),
            ("Sección 1.ª: Hojeda 1502 (Valfermoso, Curazao, Coquibacoa, Santa Cruz)",
             r"casi en todo fue semejante la segunda expedi"),
            ("Sección 1.ª: resto (Pinzón 1501, Caboto, Solís, Grijalva…)",
             r"semejante designio debio de motivar"),
            ("Documentos de la Sección 1.ª (núms. I-XLVI)",
             r"carta de i a reina catolica al obispo de badajoz"),
            ("Sección 2.ª: Vespucio (Lettera y cartas)",
             r"seccion segunda\.\s+vi ages\s+de americo vespucio"),
            ("Vespucio, 1.ª navegación: el poblado sobre el agua",
             r"colocada sobre las aguas , como venecia"),
            ("Vespucio, 1.ª navegación: 80 leguas más allá (otra lengua)",
             r"encontramos otra gente del todo diversa"),
            ("Vespucio, 1.ª navegación: resto",
             r"muchos fueron los ritos y costumbres que vi"),
            ("Vespucio, 2.ª navegación hasta la isla de las hierbas",
             r"de secundariae navigationis cursu|de secundarias navigationis cursu"),
            ("Vespucio, 2.ª navegación: isla de las hierbas e isla de los Gigantes",
             r"avistamos una isla distante 1 ?5 leguas"),
            ("Vespucio, 2.ª navegación: de la ensenada de las perlas a Cádiz",
             r"aliviarnos en nuestros trabajos"),
            ("Vespucio, 3.ª navegación en adelante y documentos de Vespucio",
             r"navegacion tercera"),
            ("Sección 3.ª y suplemento (Darién, pleitos…)",
             r"seccion tercera"),
            ("Pleitos colombinos: preguntas 4.ª-5.ª (Niño-Guerra, Hojeda)",
             r"si saben que los dichos cristobal guerra"),
            ("Pleitos colombinos: pregunta 6.ª en adelante",
             r"6\.a item: si saben que despues"),
            ("Índices y erratas",
             r"sumario e indice"),
        ],
    },
    "navarrete-t1": {
        "archivo": "Navarrete_1859_Coleccion_Viages_t1_Viages_de_Colon.txt",
        "obra": "navarrete-1859-viages-colon",
        "paginacion": "cabeceras",
        "anclas": [],
    },
    "hernando": {
        "archivo": "Colon_Hernando_1892_Historia_del_Almirante_vol2.txt",
        "obra": "colon-hernando-1892 vol. 2",
        "paginacion": "cabeceras",
        "anclas": [],
    },
}

# ── Las dianas (raíces cortas sobre el texto normalizado) ────────────────
LUGARES = {
    "coquibacoa (todas las grafías)": r"[a-z]{2,9}[bvh]acoa\b|coywvaeoa|conqu[a-z]{0,3}boca",
    "curiana": r"curian|cutian|citrian|\bcorian",
    "cauchieto": r"cauchiet|carichat|cahuyet",
    "gigante(s)": r"gigant",
    "curazao": r"curaz|curac[,.]?ao",
    "san roman": r"s\.\s*roman|san\s+roman",
    "venecia / venezuela": r"venecia|vcnecia|venezuel|venetia",
    "valfermoso": r"val\s*-?\s*fermos|valfer",
    "puerto flechado": r"flechad|prechad",
    "coro": r"\bcoro\b",
    "chichiriviche": r"chichiriv|chidiinv",
    "cabo de la vela": r"cabo\s+de\s+la\s+vela",
    "maracaibo": r"maraca[iy]bo|maraciibo|maracáibo",
    "paraguana": r"paraguan|paragoan|paraguay?an",
    "aruba": r"\baruba|\boruba",
    "bonaire": r"bonair|buinar|bonay",
    "caquetio": r"caquet|caiquet|caquit|caketi",
    "manaure": r"manaur",
}
LENGUA = {
    "interprete": r"interpret",
    "lengua": r"\blengua",
    "por senas": r"por\s+se[nñ]as|con\s+gestos",
    "isabel (la india)": r"por\s+amor\s+de\s+isabel|mirad\s+mucho\s+por\s+isabel|con\s+isabel\s+que|la\s+india\s+isabel",
    "llamaban / llaman (nombres indigenas)": r"los\s+indios\s+(le\s+)?llamaban|que\s+llaman|los\s+indigenas\s+llaman|que\s+se\s+dicen",
}
FAUNA = {
    "conejo": r"conejo",
    "ciervo / venado": r"ciervo|venado",
    "jabali / puerco": r"jabali|puerco",
    "tigre": r"tigre",
    "mono / cercopiteco": r"cercopitec|\bmonos?\b",
    "papagayo / loro": r"papagay|\bloros?\b",
    "tortuga": r"tortug|turtur",
    "pez / pesca": r"\bpeces\b|\bpescad|\bpescar",
    "ostra / ostion / concha": r"\bostra|ostion|ostial|conchas?\b",
    "serpiente (iguana en Vespucio)": r"serpient",
    "ave(s) / pajaro(s)": r"\baves\b|pajaro",
    "pavo / faisan / paloma / tortola / pato": r"\bpavo|faisan|paloma|tortola|\bpato|anade",
}
CONTROLES = {
    "isla": r"\bisla",
    "oro": r"\boro\b",
    "indio": r"\bindi[oa]s?\b",
    "rescat": r"rescat",
}
FAMILIAS = {"lugares": LUGARES, "lengua": LENGUA, "fauna": FAUNA, "controles": CONTROLES}


# ── Normalización que conserva el largo ──────────────────────────────────
def _c(ch):
    d = unicodedata.normalize("NFD", ch)
    base = d[0] if d else ch
    low = base.lower()
    return low if len(low) == 1 else base


def normalizar(texto):
    return "".join(_c(ch) for ch in texto)


def patron(diana):
    """Cada espacio literal de una diana pasa a `\\s+` (el OCR usa dos)."""
    return re.compile(re.sub(r"(?<!\\) ", r"\\s+", diana))


# ── Paginación ───────────────────────────────────────────────────────────
_MARCA = re.compile(r"^=== pdf (\d+) · impresa (-?\d+) ===$", re.M)
_CAB_NUM_DELANTE = re.compile(r"^\s*(\d{1,3})\s+[A-ZÁÉÍÓÚ][A-ZÁÉÍÓÚa-z .,]{3,}$")
_CAB_NUM_DETRAS = re.compile(r"^\s*[A-ZÁÉÍÓÚ][A-ZÁÉÍÓÚ .,]{5,}\.?\s+(\d{1,3})\s*$")


def marcadores(crudo):
    """[(posición, impresa)] a partir de los marcadores del .txt."""
    return [(m.start(), int(m.group(2))) for m in _MARCA.finditer(crudo)]


# Caracteres por página admisibles entre dos cabeceras encadenadas. Medido
# sobre las cabeceras limpias de Navarrete t. III (pp. 7→8→9: unos 3.100-3.400)
# y de Hernando (unos 1.600); el margen es ancho a propósito: sólo sirve para
# rechazar el `303` que el OCR escribe por `203`.
_CPP_MIN, _CPP_MAX = 700, 7000


def cabeceras(crudo):
    """[(posición, folio)] de las cabeceras FIABLES.

    El OCR estropea dígitos (`303` por `203`, `91` por `21`, `ío I` por `201`) y
    confunde con cabeceras las notas que empiezan por número. Se queda la
    cadena MÁS LARGA de candidatas que crecen en número y en posición a un
    ritmo de página verosímil (subsecuencia creciente más larga, con la
    restricción de caracteres por página). Las que no entran en la cadena se
    descartan en vez de mover la paginación."""
    cands = []
    pos = 0
    for linea in crudo.split("\n"):
        m = _CAB_NUM_DELANTE.match(linea) or _CAB_NUM_DETRAS.match(linea)
        if m:
            cands.append((pos, int(m.group(1))))
        pos += len(linea) + 1
    n = len(cands)
    if not n:
        return []
    mejor = [1] * n
    previo = [-1] * n
    for i in range(n):
        pi, ni = cands[i]
        for j in range(i):
            pj, nj = cands[j]
            if ni <= nj:
                continue
            cpp = (pi - pj) / (ni - nj)
            if _CPP_MIN <= cpp <= _CPP_MAX and mejor[j] + 1 > mejor[i]:
                mejor[i] = mejor[j] + 1
                previo[i] = j
    k = max(range(n), key=lambda i: mejor[i])
    cadena = []
    while k != -1:
        cadena.append(cands[k])
        k = previo[k]
    return cadena[::-1]


def folio_de(paginas, pos, modo):
    """La página impresa de una posición. Con marcadores, exacta. Con
    cabeceras: exacta si las cabeceras que la rodean son consecutivas; si no,
    interpolada y marcada con «≈» (es una guía para ir al pasaje, no una
    cita)."""
    if not paginas:
        return None
    antes = [x for x in paginas if x[0] <= pos]
    despues = [x for x in paginas if x[0] > pos]
    if modo == "marcadores":
        return antes[-1][1] if antes else None
    if not antes:
        return f"<{despues[0][1]}" if despues else None
    pa, na = antes[-1]
    if not despues:
        return f"≥{na}"
    pb, nb = despues[0]
    if nb - na == 1:
        return na
    cpp = (pb - pa) / (nb - na)
    return f"≈{na + int((pos - pa) / cpp)}"


def tramos_de(clave, ficha, norm, paginas):
    """[(inicio, nombre)] ordenados. Anglería: por página impresa; Navarrete
    t. III: por anclas de texto."""
    if ficha["paginacion"] == "marcadores" and ficha.get("tramos_impresa"):
        out = []
        for nombre, (ini, _fin) in ficha["tramos_impresa"].items():
            pos = next((p for p, n in paginas if n >= ini), None)
            if pos is not None:
                out.append((pos, nombre))
        return sorted(out)
    out = []
    for nombre, ancla in ficha.get("anclas", []):
        m = patron(ancla).search(norm)
        if not m:
            raise SystemExit(f"✗ {clave}: el ancla del tramo «{nombre}» no aparece "
                             f"({ancla!r}). No se finge un tramo vacío: revisar el ancla.")
        out.append((m.start(), nombre))
    return sorted(out)


def tramo_de(tramos, pos):
    nombre = "(antes del primer tramo)"
    for ini, n in tramos:
        if ini <= pos:
            nombre = n
    return nombre if tramos else "(obra entera)"


# ── Medir ────────────────────────────────────────────────────────────────
def cargar(clave):
    ficha = OBRAS[clave]
    ruta = os.path.join(FUENTES, ficha["archivo"])
    if not os.path.exists(ruta):
        return None
    crudo = io.open(ruta, encoding="utf-8").read()
    norm = normalizar(crudo)
    assert len(norm) == len(crudo)
    if ficha["paginacion"] == "marcadores":
        paginas = marcadores(crudo)
    else:
        paginas = cabeceras(crudo)
    tramos = tramos_de(clave, ficha, norm, paginas)
    unido, mapa = unir_guiones(norm)
    return {"ficha": ficha, "crudo": crudo, "norm": norm, "paginas": paginas,
            "tramos": tramos, "unido": unido, "mapa": mapa}


# El guion de fin de línea parte palabras (`ti-` + salto + `gres`, `Co-` +
# salto + `quibacoa`):
# medido aquí, «tigre» daba 0 en Hernando donde el texto dice «garras de
# ti- gres». Se busca sobre una copia con esos guiones cosidos y cada acierto
# se devuelve en posiciones del texto ORIGINAL, para poder citarlo.
_GUION = re.compile(r"(?<=[a-z])-[ \t]*\n\s*(?=[a-z])")


def unir_guiones(norm):
    partes, mapa, prev = [], [], 0
    for m in _GUION.finditer(norm):
        partes.append(norm[prev:m.start()])
        mapa.extend(range(prev, m.start()))
        prev = m.end()
    partes.append(norm[prev:])
    mapa.extend(range(prev, len(norm)))
    mapa.append(len(norm))
    return "".join(partes), mapa


class _Acierto:
    __slots__ = ("_s", "_e")

    def __init__(self, s, e):
        self._s, self._e = s, e

    def start(self):
        return self._s

    def end(self):
        return self._e


def aciertos(obra, diana):
    mapa = obra["mapa"]
    return [_Acierto(mapa[m.start()], mapa[m.end() - 1] + 1)
            for m in patron(diana).finditer(obra["unido"])]


# Cuál Curiana es cuál. Por defecto, la del TRAMO; y el contexto manda cuando
# nombra algo que sólo es de una de las dos. Las reglas se declaran aquí, no
# se deciden acierto por acierto.
_CURIANA_POR_TRAMO = {
    "Sección 1.ª: Hojeda-La Cosa-Vespucio 1499": "oriental",
    "Sección 1.ª: Niño y Guerra 1499-1500 (Curiana, Cauchieto)": "oriental",
    "Sección 1.ª: Hojeda 1502 (Valfermoso, Curazao, Coquibacoa, Santa Cruz)": "occidental",
    "Documentos de la Sección 1.ª (núms. I-XLVI)": "oriental",
    "Índices y erratas": "índice",
}
_CURIANA_OCCIDENTAL = re.compile(r"valfer|jamaica|saltea|salteo|por el en curiana|cutian|\bcoro\b")
_CURIANA_ORIENTAL = re.compile(r"farall|frailes|cumana|golfo de las perlas")


def cual_curiana(tramo, contexto):
    ctx = normalizar(contexto)
    if tramo == "Índices y erratas":
        return "índice"
    if _CURIANA_OCCIDENTAL.search(ctx):
        return "occidental"
    if _CURIANA_ORIENTAL.search(ctx):
        return "oriental"
    return _CURIANA_POR_TRAMO.get(tramo, "sin decidir")


def limpio(texto):
    """Un tramo del texto crudo para mostrarlo: guiones de fin de línea
    cosidos y espacios colapsados."""
    return re.sub(r"\s+", " ", re.sub(r"-[ \t]*\n\s*", "", texto)).strip()


def medir(solo=None):
    res = {}
    for clave, ficha in OBRAS.items():
        if solo and clave != solo:
            continue
        obra = cargar(clave)
        if obra is None:
            res[clave] = {"obra": ficha["obra"], "falta": ficha["archivo"]}
            continue
        r = {"obra": ficha["obra"], "caracteres": len(obra["crudo"]),
             "cabeceras_aceptadas": len(obra["paginas"]), "familias": {}}
        for fam, dianas in FAMILIAS.items():
            r["familias"][fam] = {}
            for nombre, diana in dianas.items():
                ms = aciertos(obra, diana)
                por_tramo = {}
                folios = []
                for m in ms:
                    t = tramo_de(obra["tramos"], m.start())
                    por_tramo[t] = por_tramo.get(t, 0) + 1
                    folios.append(folio_de(obra["paginas"], m.start(), ficha["paginacion"]))
                r["familias"][fam][nombre] = {"n": len(ms), "por_tramo": por_tramo,
                                              "folios": folios}
        # Las grafías de Coquibacoa, forma por forma
        formas = {}
        for m in aciertos(obra, LUGARES["coquibacoa (todas las grafías)"]):
            crudo = limpio(obra["crudo"][m.start():m.end()])
            f = folio_de(obra["paginas"], m.start(), ficha["paginacion"])
            formas.setdefault(crudo, []).append(
                {"folio": f, "tramo": tramo_de(obra["tramos"], m.start())})
        r["grafias_coquibacoa"] = formas
        # Las dos Curianas: cada acierto con su tramo y un contexto corto
        cur = []
        for m in aciertos(obra, LUGARES["curiana"]):
            s, e = max(0, m.start() - 90), min(len(obra["crudo"]), m.end() + 90)
            t = tramo_de(obra["tramos"], m.start())
            ctx = limpio(obra["crudo"][s:e])
            cur.append({"folio": folio_de(obra["paginas"], m.start(), ficha["paginacion"]),
                        "tramo": t, "cual": cual_curiana(t, ctx), "contexto": ctx})
        r["curiana"] = cur
        r["curiana_resumen"] = {}
        for c in cur:
            r["curiana_resumen"][c["cual"]] = r["curiana_resumen"].get(c["cual"], 0) + 1
        res[clave] = r
    return res


def contextos(familia, solo=None, antes=160, despues=260):
    dianas = {}
    for fam, d in FAMILIAS.items():
        for nombre, diana in d.items():
            if familia in (fam, nombre) or familia in nombre:
                dianas[nombre] = diana
    if not dianas:
        raise SystemExit(f"✗ no hay diana ni familia que se llame {familia!r}")
    for clave in OBRAS:
        if solo and clave != solo:
            continue
        obra = cargar(clave)
        if obra is None:
            continue
        for nombre, diana in dianas.items():
            for m in aciertos(obra, diana):
                s, e = max(0, m.start() - antes), min(len(obra["crudo"]), m.end() + despues)
                f = folio_de(obra["paginas"], m.start(), obra["ficha"]["paginacion"])
                print(f"── {clave} · {nombre} · folio {f} · {tramo_de(obra['tramos'], m.start())}")
                print("   " + limpio(obra["crudo"][s:e]))
                print()


def _forzar_utf8():
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8")


def informe(res):
    for clave, r in res.items():
        print(f"\n══ {clave} — {r['obra']}")
        if "falta" in r:
            print(f"   ✗ falta el texto: fuentes_caquetios/{r['falta']} — no se finge un cero")
            continue
        print(f"   {r['caracteres']} caracteres · cabeceras/marcadores aceptados: "
              f"{r['cabeceras_aceptadas']}")
        for fam, dianas in r["familias"].items():
            print(f"   ── {fam}")
            for nombre, d in dianas.items():
                linea = f"      {nombre:<42} {d['n']:>5}"
                if d["n"] and len(d["por_tramo"]) > 1:
                    linea += "   " + " · ".join(f"{t}: {n}" for t, n in d["por_tramo"].items())
                elif d["n"]:
                    linea += "   " + next(iter(d["por_tramo"]))
                print(linea)
        if r["grafias_coquibacoa"]:
            print("   ── grafías de Coquibacoa (tal como las da el texto; el OCR NO se corrige)")
            for forma, lst in r["grafias_coquibacoa"].items():
                fol = ", ".join(str(x["folio"]) for x in lst)
                print(f"      {forma!r:<22} ×{len(lst)}   folio(s): {fol}")
        if r["curiana"]:
            print("   ── las Curianas, acierto por acierto — resumen: "
                  + " · ".join(f"{k} {v}" for k, v in r["curiana_resumen"].items()))
            for c in r["curiana"]:
                print(f"      [{c['cual']}] folio {c['folio']} · {c['tramo']}")
                print(f"         …{c['contexto']}…")


def main(argv=None):
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--obra", choices=list(OBRAS))
    ap.add_argument("--contexto", metavar="FAMILIA_O_DIANA",
                    help="imprime el contexto de cada acierto (p. ej. curiana, fauna, lengua)")
    args = ap.parse_args(argv)
    if args.contexto:
        contextos(args.contexto, args.obra)
        return 0
    res = medir(args.obra)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        informe(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
