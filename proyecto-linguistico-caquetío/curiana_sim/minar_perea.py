#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""minar_perea.py — vacía el FRASEARIO de Perea y Alonso 1942 y emite la
propuesta de comparanda lokono en `6-fusion/lokono_perea_1942.yaml`.

QUÉ ES LA FUENTE
    «Filología comparada de las lenguas y dialectos arawak», tomo I, de Sixto
    Perea y Alonso (Montevideo, 1942). Su PRIMERA PARTE es un *fraseario
    analógico* del arawak de las Guayanas —o sea, LOKONO— extractado del texto
    bíblico de Theodor SCHULTZ, 1802: «Act Apostel-nu», los Hechos de los
    Apóstoles. Cada entrada numerada da un concepto en español con sus glosas
    latina, portuguesa, francesa e inglesa, y debajo las frases lokono donde la
    voz aparece, citadas por capítulo-versículo y ya segmentadas en morfemas
    por el propio Perea.

CÓMO SE EXTRAE
    La voz lokono es el token EN MAYÚSCULAS del lado arawak de cada igualdad
    `frase = traducción`. La raíz se obtiene quitando de la segmentación del
    propio Perea los segmentos que su Compendio Gramatical declara afijos
    (paradigma de Schumann, p. impresa 587). No se inventa segmentación.

QUÉ NO ES
    No es un diccionario de la lengua: es la concordancia de UN libro. Su campo
    semántico es el de los Hechos, no el de la costa caribe. Medido: no hay
    ENTRADA para agua, árbol, arena, raíz, pez ni casa — aunque agua y árbol sí
    aparecen en el Compendio Gramatical (parte II), que se minó aparte.

Uso:  python curiana_sim/minar_perea.py [--dry-run]
"""
import io, os, re, sys, json, bisect, subprocess, unicodedata, collections

import yaml

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

RAIZ_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(RAIZ_REPO, "fuentes_caquetios",
                   "Perea_Alonso_1942_Filologia_Comparada_Arawak_TomoI.pdf")
TXT = os.path.join(RAIZ_REPO, "fuentes_caquetios",
                   "Perea_Alonso_1942_Filologia_Comparada_Arawak_TomoI.txt")
DEST = os.path.join(RAIZ_REPO, "6-fusion", "lokono_perea_1942.yaml")

# El Fraseario ocupa las páginas pdf 165-763 (impresas 1-541). El escaneo de
# Michigan repite pliegos, así que el desfase deriva: se lee el número impreso
# de cada página en vez de sumar una constante.
PDF_INI, PDF_FIN = 164, 763

# ─────────────────────────────────────────────────────────────────────────
# 1. texto
# ─────────────────────────────────────────────────────────────────────────
def cargar_texto():
    if not os.path.exists(TXT):
        # pypdf devuelve basura en este escaneo; pdftotext, no (regla del repo)
        subprocess.run(["pdftotext", "-enc", "UTF-8", PDF, TXT], check=True)
    return io.open(TXT, encoding="utf-8").read().split("\f")


def pagina_impresa(txt):
    cab = " ".join(txt.split()[:12])
    m = re.match(r"^(\d{1,3})\s", cab)                       # par:  "10 Arw) ARAWAK…"
    if m:
        return int(m.group(1))
    m = re.match(r"^[A-ZÁÉÍÓÚÑ,. ]{4,45}?\s(\d{1,3})\b", cab)  # impar: "NOMBRES 11"
    if m:
        return int(m.group(1))
    return None


# ─────────────────────────────────────────────────────────────────────────
# 2. entradas numeradas
# ─────────────────────────────────────────────────────────────────────────
MARCA = re.compile(r"[-—–―]\s*(\d{1,4})(\s*bis)?\s*[-—–―]")
# el encabezado va `LEMA ; L : latín, P : …` — y en los pronombres, sin el `;`
CABEZA = re.compile(r"\s*(.{1,130}?)\s*[;,]?\s*L\s*[:.]\s")
# el OCR mete espacios alrededor de los guiones y parte las voces segmentadas
PEGA = re.compile(r"\s*-\s+|\s+-\s*")


def parsear(paginas):
    trozos, mapa, off = [], [], 0
    for idx in range(PDF_INI, min(PDF_FIN, len(paginas))):
        t = " ".join(paginas[idx].split())
        mapa.append((off, pagina_impresa(paginas[idx]), idx + 1))
        trozos.append(t)
        off += len(t) + 1
    stream = " ".join(trozos)
    offs = [o for o, _, _ in mapa]

    def pag_de(p):
        i = max(bisect.bisect_right(offs, p) - 1, 0)
        return mapa[i][1], mapa[i][2]

    ms = list(MARCA.finditer(stream))
    entradas = {}
    for i, m in enumerate(ms):
        num = int(m.group(1))
        if not 1 <= num <= 1100:
            continue
        clave = f"{num}bis" if m.group(2) else str(num)
        if clave in entradas:          # el escaneo repite pliegos: vale la 1ª
            continue
        fin = ms[i + 1].start() if i + 1 < len(ms) else len(stream)
        bloque = stream[m.end():min(fin, m.end() + 2500)]
        mh = CABEZA.match(bloque)
        if not mh:
            continue
        pi, ppdf = pag_de(m.start())
        entradas[clave] = {"n": num, "lema_es": mh.group(1).strip(),
                           "pagina_impresa": pi, "pagina_pdf": ppdf,
                           "cuerpo": PEGA.sub("-", bloque[mh.end():])}
    return entradas


# ─────────────────────────────────────────────────────────────────────────
# 3. la voz lokono: el token en mayúsculas del lado arawak
# ─────────────────────────────────────────────────────────────────────────
LET = "A-ZÀÁÄÈÉËÌÍÏÒÓÖÙÚÜÑÇƔ"
TOKEN = re.compile(rf"\b[{LET}][{LET}]+(?:-[{LET}]+)*\b")
CITA = re.compile(r"(?<![\w-])(\d{1,2}-\d{1,3}|-\d{1,3})(?![\w-])")


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def formas_de(cuerpo):
    formas, ejemplos, cita = collections.Counter(), [], None
    for tr in CITA.split(cuerpo):
        if not tr:
            continue
        if CITA.fullmatch(tr):
            cita = tr
            continue
        partes = tr.split("=")
        if len(partes) < 2:
            continue
        arw, esp = partes[0], "=".join(partes[1:])
        caps = [t for t in TOKEN.findall(arw)
                if len(sin_tildes(t).replace("-", "")) >= 2]
        for c in caps:
            formas[c] += 1
        if caps and len(ejemplos) < 4:
            ejemplos.append({"cita": cita,
                             "arw": " ".join(arw.split())[-70:],
                             "es": " ".join(esp.split())[:70]})
    return formas, ejemplos


# ─────────────────────────────────────────────────────────────────────────
# 4. raíz — afijos declarados por el propio libro (p. impresa 587)
# ─────────────────────────────────────────────────────────────────────────
PREFIJOS = {"d", "da", "b", "bu", "l", "lu", "lù", "li", "t", "tu", "tù", "w",
            "wa", "h", "hu", "hù", "n", "na", "u", "ù", "s", "y", "i",
            "a", "ca", "ka", "ma", "m"}
SUFIJOS = {"ti", "tti", "tu", "ttu", "nu", "nnu", "ni", "nni", "wa", "ua",
           "hu", "hù", "u", "n", "ne", "na", "nna", "sia", "cu", "ccu", "bu",
           "ba", "ca", "cá", "da", "dù", "di", "ddi", "ki", "kitti", "kia",
           "man", "mùn", "ye", "re", "ren", "be", "la", "ru", "rù", "co",
           "cuba", "cubá", "benna", "uria", "abbu", "ma"}


def base(s):
    return sin_tildes(s.lower())


def raiz(forma):
    segs = [s for s in forma.split("-") if s]
    if not segs:
        return None
    i = 0
    while i < len(segs) - 1 and base(segs[i]) in PREFIJOS:
        i += 1
    j = len(segs)
    while j - 1 > i and base(segs[j - 1]) in SUFIJOS:
        j -= 1
    r = "-".join(segs[i:j])
    return r if len(base(r).replace("-", "")) >= 3 else None


# ─────────────────────────────────────────────────────────────────────────
# 5. criba: el propio Perea avisa de los exotismos del traductor moravo
# ─────────────────────────────────────────────────────────────────────────
GERMANISMOS = set("""engel apostel gott tempel prophet satan christus brief karta
carta hundert funfzing tausend kreuz altar krone stunde geist herr kaiser konig
meister schiff stadt taufe teufel wein zeit opfer synagoge psalm jude heide
pharisaer sadducaer centurio hauptmann kammer anker bischof diakon evangelium
heiland himmel kirche pfingsten sabbat segen sunde tisch wunder buch stuhl
krieg richter soldaru coning""".split())
HISPANISMOS = set("""baca kawaiyu cawaiyu sapatu kapitai capitai kabaiyu sibora
kabritu bino asukar kruz sinku mesa kamisa pesu real soldado gobernador
plata oro papel silla libro senor""".split())
CRISTIANO = re.compile(
    r"(jesus|christ|paul|pedro|petrus|juda|israel|jerusal|roma|moises|david|"
    r"abraham|espiritu santo|bautis|circuncid|circuncis|sinagoga|fariseo|"
    r"saduceo|evangelio|apostol|angel|profeta|cristian|salmo|pentecost|"
    r"gentil|idolo|altar|templo|obispo|diacono)", re.I)


# ─────────────────────────────────────────────────────────────────────────
# 6. cruce contra el lexicón — forma Y glosa; la forma sola no es evidencia
# ─────────────────────────────────────────────────────────────────────────
def fon_perea(s):
    """Panfonética de Perea (declarada por él, p. impresa 545-546): c/q = k
    siempre; ù = ü alemana; las geminadas alternan «sin motivo aparente»
    (l/ll, d/dd, t/tt) y se colapsan para comparar."""
    s = s.lower().replace("-", "").replace("ù", "u").replace("ü", "u")
    s = sin_tildes(s).replace("cx", "C").replace("ch", "C").replace("x", "S")
    s = re.sub(r"[^a-zCS]", "", s)
    s = s.replace("qu", "k").replace("q", "k").replace("c", "k")
    s = re.sub(r"(.)\1+", r"\1", s)
    return s.replace("z", "s").replace("v", "b")


def fon_lex(s):
    """La MISMA fonemización de computo_d11.py, para que la medida sea
    comparable con el cómputo del 2026-08-31."""
    s = sin_tildes(s.lower())
    s = re.sub(r"gu(?=[aeio])", "w", s)
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s).replace("ch", "C").replace("c", "k")
    s = s.replace("z", "s").replace("v", "b")
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zCS]", "", s))


def similitud(a, b):
    if not a or not b:
        return 0.0
    m, n = len(a), len(b)
    f = list(range(n + 1))
    for i in range(1, m + 1):
        prev, f[0] = f[0], i
        for j in range(1, n + 1):
            prev, f[j] = f[j], min(f[j] + 1, f[j - 1] + 1,
                                   prev + (a[i - 1] != b[j - 1]))
    return 1.0 - f[n] / max(m, n)


VACIAS = set("""de del la el los las un una unos unas y o a en que se su sus al lo
por para con sin como mas muy ver vease etc tambien ese esa este esta forma
nota cosa""".split())


def palabras(s):
    s = sin_tildes(s.lower())
    s = re.sub(r"\([^)]*\)", " ", s)
    out = set()
    for w in re.findall(r"[a-zñ]{3,}", s):
        if w in VACIAS:
            continue
        for suf in ("ciones", "cion", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                w = w[:-len(suf)]
                break
        out.add(w)
    return out


def columnas_lexicon():
    sys.path.insert(0, os.path.join(RAIZ_REPO, "curiana_sim"))
    from curiana_lexicon import VOCABULARIO_BASE as V
    fuentes = ("lokono", "lokono/proto-arawakan", "lokono/garifuna",
               "wayunaiki/lokono", "taíno/lokono", "proto-arawakan",
               "proto-arahuaco")
    return [(k, fon_lex(k), e.get("sig", ""))
            for k, e in V.items() if e.get("fuente") in fuentes]


# ─────────────────────────────────────────────────────────────────────────
# 7. la auditoría de la columna lokono de la tabla A-2 de Oliver
#    (leída a mano en el texto, fila por fila; no sale del cruce automático)
# ─────────────────────────────────────────────────────────────────────────
AUDITORIA_A2 = yaml.safe_load(io.open(
    os.path.join(RAIZ_REPO, "6-fusion", "auditoria_a2_perea.yaml"),
    encoding="utf-8")) if os.path.exists(
    os.path.join(RAIZ_REPO, "6-fusion", "auditoria_a2_perea.yaml")) else None


def main():
    seco = "--dry-run" in sys.argv
    paginas = cargar_texto()
    entradas = parsear(paginas)
    nums = sorted(e["n"] for e in entradas.values())
    print(f"entradas del Fraseario parseadas: {len(entradas)} "
          f"(numeradas 1-{nums[-1]}; faltan {nums[-1] - len(nums)})")

    lex = columnas_lexicon()
    corrobora, nuevas = [], []
    criba = collections.Counter()
    for clave, e in entradas.items():
        formas, ejemplos = formas_de(e["cuerpo"])
        cands = collections.Counter()
        for f, n in formas.most_common(6):
            r = raiz(f)
            if r:
                cands[r] += n
        if not cands:
            criba["sin raíz aislable"] += 1
            continue
        r, apoyos = cands.most_common(1)[0]
        rb = base(r).replace("-", "")
        if rb in GERMANISMOS:
            criba["germanismo del traductor"] += 1
            continue
        if rb in HISPANISMOS:
            criba["hispanismo"] += 1
            continue
        if CRISTIANO.search(e["lema_es"]):
            criba["voz cristiana sin forma nativa"] += 1
            continue
        criba["se conserva"] += 1

        fila = {"raiz": r.lower(),
                "concepto_es": re.sub(r"\s+", " ", e["lema_es"]).strip(" .,;"),
                "pagina": e["pagina_impresa"], "atestaciones": apoyos,
                "entrada_n": e["n"]}
        ej = next((x for x in ejemplos if x["cita"] and not x["cita"].startswith("-")),
                  ejemplos[0] if ejemplos else None)
        if ej:
            if ej["cita"]:
                fila["cita_hechos"] = ej["cita"]
            fila["ejemplo"] = f"{ej['arw']} = {ej['es']}"

        fp = fon_perea(r)
        mejor, sim = None, 0.0
        for k, fk, sig in lex:
            s = similitud(fp, fk)
            if s > sim:
                mejor, sim = (k, sig), s
        if mejor and sim >= 0.85:
            fila["ya_en_lexicon"] = mejor[0]
            fila["glosa_lexicon"] = mejor[1]
            fila["glosa_coincide"] = bool(palabras(e["lema_es"]) & palabras(mejor[1]))
            corrobora.append(fila)
        else:
            nuevas.append(fila)

    print("criba:", dict(criba))
    corrobora.sort(key=lambda f: -f["atestaciones"])
    nuevas.sort(key=lambda f: (-f["atestaciones"], f["concepto_es"]))
    con_glosa = sum(1 for f in corrobora if f["glosa_coincide"])
    print(f"corroboran una entrada del lexicón: {len(corrobora)} "
          f"(de ellas con la glosa también: {con_glosa})")
    print(f"nuevas: {len(nuevas)} — con 2+ atestaciones: "
          f"{sum(1 for f in nuevas if f['atestaciones'] >= 2)}")

    doc = {
        "meta": {
            "generado_por": "curiana_sim/minar_perea.py",
            "obra": "perea-alonso-1942",
            "que_es": (
                "Fraseario analógico del arawak (LOKONO) de las Guayanas Holandesa e "
                "Inglesa, extractado por Perea del texto bíblico de Theodor Schultz, "
                "1802 — «Act Apostel-nu», los Hechos de los Apóstoles. Cada entrada da "
                "el concepto en español con sus glosas latina, portuguesa, francesa e "
                "inglesa, y debajo las frases lokono donde la voz aparece, citadas por "
                "capítulo-versículo y ya segmentadas en morfemas por el propio Perea."),
            "estrato": (
                "Lokono de 1802, no el moderno. El propio Perea documenta que el arawak "
                "de Brett 1849 ya diverge: «la g sustituye con frecuencia a la k de los "
                "Moravos, y la i, u, t de aquéllos se ha transformado en e, o, cx» "
                "(p. impresa 546). Es un estrato más cercano en el tiempo a los "
                "documentos caquetíos que Goeje 1928, Brinton 1871 o Pet 1987."),
            "cobertura_medida": {
                "entradas_numeradas": 1060,
                "parseadas": len(entradas),
                "raices_conservadas": criba["se conserva"],
                "corroboran_el_lexicon": len(corrobora),
                "de_esas_con_glosa_coincidente": con_glosa,
                "nuevas": len(nuevas),
                "paginas_impresas_ausentes_del_escaneo": 29,
            },
            "desfase": ("el Fraseario ocupa pdf 165-763 = impresas 1-541, pero el "
                        "escaneo repite pliegos: hay que leer el número impreso de "
                        "cada página, no sumar una constante"),
            "etiqueta_propuesta": ("comparanda lokono atestiguada. No entra al canon "
                                   "por sí sola: minar propone, humano fusiona"),
        },
        "advertencias": [
            "El texto es una TRADUCCIÓN DEL ALEMÁN hecha por misioneros moravos. El "
            "propio Perea avisa (p. impresa CVII): «no son de extrañar los abundantes "
            "neologismos, exotismos, supresiones y aditamentos». Se cribaron "
            "germanismos, hispanismos y voces cristianas sin forma nativa.",
            "El campo semántico es el de los Hechos de los Apóstoles, no el de la costa "
            "caribe. Verificado: el Fraseario no tiene ENTRADA propia para agua, árbol, "
            "arena, raíz, pez ni casa. Aviso medido el mismo día: agua (wuni-abu) y "
            "árbol (adda) sí están en el Compendio Gramatical, pp. 556 y 559 — el "
            "índice de lemas no es la obra. Arena y raíz sí faltan de las 926 páginas. "
            "Esta fuente NO equilibra la columna wayuu concepto por concepto: la "
            "equilibra en gramática, partículas, cuerpo, parentesco y vocabulario "
            "abstracto.",
            "La raíz sale de quitar de la segmentación del PROPIO Perea los segmentos "
            "que su Compendio Gramatical declara afijos (p. impresa 587). Donde el OCR "
            "metió un espacio dentro de un guion la raíz podía salir partida; se "
            "corrigió pegando los guiones, pero quedan casos.",
            "Las corroboraciones marcadas `glosa_coincide: false` NO son falsas: casi "
            "todas son polisemia de una misma raíz (abba = uno / otro / alguno / "
            "nadie). Necesitan ojo humano, no descarte automático.",
            "Trampa que el propio Perea nombra (p. impresa 546): la alternancia r/l "
            "hace que la postposición -ruccu ~ -luccu «en, dentro» colisione con luccu "
            "«hombre, persona, indio». El cruce la reencontró sola.",
        ],
        "corroboraciones": corrobora,
        "nuevas_con_dos_o_mas_atestaciones": [f for f in nuevas if f["atestaciones"] >= 2],
        "nuevas_con_una_atestacion": [f for f in nuevas if f["atestaciones"] == 1],
    }
    if AUDITORIA_A2:
        doc["auditoria_columna_lokono_de_la_A2"] = AUDITORIA_A2

    texto = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100)
    yaml.safe_load(texto)          # VALIDAR antes de escribir (trampa 2026-09-08)
    if seco:
        print("--dry-run: no se escribe", DEST)
        return
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(texto)
    print("escrito:", os.path.relpath(DEST, RAIZ_REPO))


if __name__ == "__main__":
    main()
