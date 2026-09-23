# -*- coding: utf-8 -*-
"""
COLL Y TOSTE, *Prehistoria de Puerto Rico* — los dos vocabularios, entrada a entrada.
Tercera campaña de minería, parcela M5 (los vocabularios antillanos). 2026-09-22.

LA PREGUNTA
-----------
La ficha `4-fuentes/coll-y-toste-1897.md` dejaba dos preguntas: (1) ¿cita Coll y Toste
POR ENTRADA de qué cronista sale cada voz?, y (2) ¿qué dice de las voces que otras fuentes
SACAN del taíno? Este script transcribe los dos vocabularios del libro para que las dos
preguntas se contesten con números y no con impresiones:

  · el cap. XII, «Vocabulario indo-antillano», que según su propio título apoya cada voz
    «con la cita oportuna del cronista que ha conservado la palabra indígena»;
  · el cap. X, «Vocabulario español-boriqueño», que va AL REVÉS (glosa castellana → voz) y
    compara cada voz con el caribe insular (`Ci.`), el caribe continental (`Cn.`), el
    aruaca (`Ar.`), el galibi (`Gl.`)… — es la única lista del repo con glosa castellana de
    UNA palabra para cada voz, que es lo que el cruce con el caquetío necesita.

EL TEXTO QUE SE LEE, Y SU ESTATUTO
----------------------------------
`fuentes_caquetios/CollYToste_1897_Prehistoria_Puerto_Rico.ocr.txt` = el OCR del propio
ítem de archive.org (no es nuestro). ⚠️ **No es la edición de 1897**: la portada del
escaneo es la SEGUNDA edición (Isabel Cuchí Coll, Bilbao, Editorial Vasco Americana, s. f.,
«Todos los derechos reservados»), con un apéndice fotográfico del Instituto de Cultura
Puertorriqueña (fundado en 1955); y el texto cita obras de 1907. 1897 es la fecha del premio
de la Sociedad Económica, no la del texto. Las páginas son las de ESA edición.

El OCR es una pista, no una cita (skill `leer-fuente` §2). Aquí se transcribe
automáticamente, se dice que es automático, y se revisa a mano lo que decide algo (ver
`REVISADO_A_MANO`).

LO QUE ESTE SCRIPT NO HACE
--------------------------
No fusiona nada ni toca el canon. Lee el lexicón de SÓLO LECTURA para marcar qué voces
coinciden con una clave taína por FORMA — y eso es una pista, no una igualdad: la glosa se
revisa (la trampa de `macana`).

USO
---
    python 6-fusion/scripts/transcribir_coll_y_toste.py
    python 6-fusion/scripts/transcribir_coll_y_toste.py --check

SALIDA (PROPUESTA, regla 5): 6-fusion/taino3_coll_y_toste_1897.yaml
"""
import argparse
import bisect
import collections
import io
import os
import re
import sys
import unicodedata

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL          # noqa: E402  (sólo lectura)

FUENTE = os.path.join(R, "fuentes_caquetios", "CollYToste_1897_Prehistoria_Puerto_Rico.ocr.txt")
SALIDA = os.path.join(R, "6-fusion", "taino3_coll_y_toste_1897.yaml")
OBRA = "coll-y-toste-1897"
TOPE_TEXTO = 700

# ═════════════════════════════════════════════════════════════════════════
# Autoridades — quién es cronista (s. XV-XVI o documento de época) y quién no
# ═════════════════════════════════════════════════════════════════════════
CRONISTAS = collections.OrderedDict([
    ("Las Casas", r"Las\s*Casas|Obispo\s+de\s+Chiapa|obispo\s+de\s+Chiapas|el\s+obispo\b"),
    ("Oviedo", r"Oviedo"),
    ("Pedro Mártir", r"M[áa]rtir|Angler[íi]a|D[ée]c(ada)?\.?\s*[IVX\d]"),
    ("Colón", r"\bCol[óo]n\b|Almirante|Diario\s+del"),
    ("Chanca", r"Chanca"),
    ("Pané", r"\bPan[ée]\b|Rom[áa]n\s+Pan|fray\s+Rom[áa]n"),
    ("Gómara", r"G[óo]mara"),
    ("Herrera", r"Herrera"),
    ("Enciso", r"Enciso"),
    ("Echagoian", r"Echagoi?an"),
    ("Benzoni", r"Benzoni"),
    ("Juan de la Cosa", r"Juan\s+de\s+la\s+Cosa"),
    ("Documento de época", r"Repartimiento|Informe\s+(dado\s+)?al\s+Rey|Memoria\s+de\s+Melgarejo|"
                           r"Documentos\s+in[ée]ditos|Archivo\s+de\s+Indias|c[ée]dula|"
                           r"Santa\s+Clara"),
])
OTRAS = collections.OrderedDict([
    ("Pichardo", r"Pichardo"), ("Bachiller y Morales", r"Bachiller\s+y\s+Morales"),
    ("García", r"\bGarc[íi]a\b"), ("Brinton", r"Brinton"), ("Breton (1665)", r"Bret[óo]n"),
    ("Iñigo Abbad (1788)", r"[ÍI][ñn]igo|Abbad"), ("Gundlach", r"Gundla"),
    ("Stahl", r"Stahl"), ("Armas", r"\bArmas\b"), ("Tapia", r"\bTapia\b"),
    ("Poey", r"\bPoey\b"), ("Crévaux", r"Cr[ée]vaux"), ("Humboldt", r"Humboldt"),
    ("Rochefort", r"Rochefort"), ("Castellanos", r"Castellanos"), ("Guridi", r"Guridi"),
    ("Asensio", r"Asensio"), ("Navarrete", r"Navarrete"), ("Zayas", r"Zayas"),
])

# El autor saca la voz del indo-antillano (la manda a otra lengua o la llama error). Estricto:
# que el texto MENCIONE a los mexicanos o el árabe no basta (en `coa` y `maní` los nombra para
# comparar); tiene que decir que la voz VIENE de ahí, o que no es indo-antillana.
SACADA = re.compile(
    r"(vocablo|palabra|voz)\s+(es\s+)?de\s+origen\s+(mejicano|mexicano|azteca|africano|quech\w*|"
    r"guaran[íi]|tup[íi]|[áa]rabe|portugu[ée]s|brasile\w+|caribe)|"
    r"^\s*(Palabra|Vocablo|Voz)\s+(de\s+origen\s+)?(mejicana|mexicana|azteca|africana|[áa]rabe|"
    r"espa[ñn]ola|portuguesa|quech\w*)|"
    r"de\s+origen\s+(mejicano|mexicano|azteca|africano|quech\w*)|"
    r"del\s+(mexicano|mejicano|[áa]rabe)\s|viene\s+del\s+(árabe|arabe|mexicano|mejicano|latín|"
    r"espa[ñn]ol|griego)|procede\s+de\s+la\s+mejicana|es\s+del\s+Brasil|el\s+vocablo\s+es\s+de\s+guaran|"
    r"no\s+es\s+(vocablo\s+|de\s+origen\s+)?indo-?\s*antillan|no\s+es\s+ind[íi]gena|"
    r"(han\s+)?comet\w+\s+el\s+error\s+de\s+(creer|suponer)|^\s*Del\s+mexicano|"
    r"Vocablo\s+espa[ñn]ol", re.I)
# El autor analiza, traduce o reconstruye: su etimología es conjetura, no dato.
CONJETURA = re.compile(
    r"[Rr]adical\s+indo|[Rr]adical\b|creemos|opinamos|nuestra\s+interpretaci[óo]n|"
    r"traducimos|significa|polisintetismo|aglutinaci|reducido|reducida|"
    r"por\s+polisint|es\s+f[áa]cil\s+que|parece|quiz[áa]|acaso|probablemente|dudamos", re.I)

ISLAS = collections.OrderedDict([
    ("La Española", r"Hay\s*t[íi]|haytian|Santo\s+Domingo|La\s+Espa[ñn]ola|Xaragua|Higüey|Higiiey|Maguana|Marien|Magua\b"),
    ("Boriquén", r"Borinqu[ée]n|Boriqu[ée]n|boriqueñ|Puerto\s+Rico|boriquen"),
    ("Cuba", r"\bCuba\b|cuban[oa]"),
    ("Jamaica", r"Jamaica"),
    ("Lucayas", r"Lucay|Yucay"),
    ("Tierra Firme", r"Tierra\s+Firme|Costa-?\s*Firme|Venezuela|Cuman[áa]|Paria"),
])

CAMPOS = [
    ("toponimo", r"^(R[íi]o|Lugar|Pueblo|Isla|Islilla|Isleta|La\s+islilla|Laguna|Lago|Monte|Montaña|"
                 r"Sierra|Valle|Provincia|Cacicazgo|Puerto|Barrio|Cabo|Ensenada|Regi[óo]n|Cayo|"
                 r"Nombre\s+boriqueño\s+del\s+r[íi]o|Nombre\s+ind[íi]gena\s+de|Nombre\s+de\s+(la|una|un)\s+"
                 r"(isla|regi|provinc|lugar|monta|sierra|r[íi]o|pueblo)|Punta|Bah[íi]a|Caser[íi]o|Arroyo|"
                 r"Quebrada|Llanura|Llano|Playa|Sitio|Costa|Tierra|Territorio|Yucayeque|Pa[íi]s)"),
    ("antroponimo", r"^(Cacique|Cacica|Nombre\s+del\s+cacique|Nombre\s+de\s+(un|una|la)\s+cacica?|"
                    r"Indio|India|Nitayno|Nitaino|Régulo|Guerrero|Un\s+cacique|Una\s+cacica|"
                    r"El\s+cacique|La\s+cacica|Hermano|Hermana|Hija|Hijo\s+del|Mujer\s+del|Madre|Padre)"),
    ("creencia", r"zem[íi]|cem[íi]|\bdios|diosa|esp[íi]ritu|[íi]dolo|areyto|behique|bohique|"
                 r"\bculto|religi|ceremonia|sacerdote|m[ée]dico\b|ultratumba|difunto|cohoba|cojoba"),
    ("fauna", r"^(Pez|Pececillo|Peces|Ave|Aves|Pájaro|Pajarillo|Insecto|Insectillo|Culebra|Culebr[óo]n|"
              r"Serpiente|Lagarto|Lagartija|Lagartijo|Cangrej|Caracol|Molusco|Mamífero|Cuadrúpedo|"
              r"Hormiga|Mosca|Mosquito|Tortuga|Iguana|Conejo|Perro|Murci[ée]lago|Mariposa|Gusano|"
              r"Araña|Cocuyo|Luciérnaga|Loro|Cotorra|Paloma|Garza|Rat[óo]n|Rata|Animal|Almeja|Ostra|"
              r"Marisco|Cienpi[ée]s|Ciempi[ée]s|Avispa|Abeja|Piojo|Pulga|Nigua|Sapo|Rana|Jaiba|"
              r"Especie\s+de\s+(pez|ave|culebra|lagart|cangrej|caracol|insect|mono|loro|papagayo)|"
              r"Variedad\s+de\s+(pez|ave|cangrej|caracol|lagart|tortuga)|Vaca\s+marina|"
              r"Manat[íi]|Tibur[óo]n|Caim[áa]n|Cocodrilo|Buho|Búho|Lechuza|Gavil[áa]n|Halc[óo]n|"
              r"Pelícano|Alcatraz|Guacamayo|Papagayo|Periquito|Cotorrita|Zorzal|Carpintero|Colibr[íi]|"
              r"Tórtola|Pato|Chivo|Cerdo|Jutía|Hut[íi]a|Quemi|Mono|Erizo|Langost|Camar[óo]n|Pulpo|"
              r"Sardina|Lisa|Anguila|Morena|Raya|Guabina|Gusanillo|Larva|Oruga|Chinche|Cucaracha)"),
    ("flora", r"^(Á|A)rbol|^Arbusto|^Planta|^Fruta|^Fruto|^Bejuco|^Palma|^Palmera|^Hierba|^Yerba|"
              r"^Vegetal|^Enredadera|^Flor\b|^Ra[íi]z|^Tub[ée]rculo|^Variedad\s+de\s+(batata|yuca|"
              r"palm|pi[ñn]a|ají|aji|maíz|maiz|ñame|aje|frijol|calabaza)|^Una\s+variedad\s+de\s+"
              r"(batata|yuca|palm|pi[ñn]a|ají|maíz)|^Madera|^Le[ñn]o|^Caña|^Helecho|^Hongo|^Alga|"
              r"^Grama|^Gram[íi]nea|^Cacto|^Cactus|^Tabaco|^La\s+planta|^El\s+tub|^El\s+[áa]rbol|"
              r"^La\s+fruta|^El\s+fruto|^Almid[óo]n|^Semilla"),
    ("gramatica", r"^(Radical|Part[íi]cula|Prefijo|Sufijo|Pronombre|Adverbio|Interjecci|Exclamaci|"
                  r"Negaci|Verbo|Palabra\s+de\s+distinci|Terminaci)"),
]

# Revisión a mano: lo que la regla no decide bien, leído en el texto. Cada fila dice por qué.
REVISADO_A_MANO = {
}


def sin_diacriticos(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                   if unicodedata.category(c) != "Mn")


def _lema(f):
    """Mismo agrupador que `consolidar_taino._lema1` (se duplica aquí para no importar su
    módulo, que carga el lexicón entero otra vez)."""
    f = sin_diacriticos(f).lower()
    f = re.sub(r"\([^)]*\)", " ", f)
    f = re.sub(r"[^a-zñ\- ]", "", f)
    f = f.replace("-", "").replace(" ", "")
    if not f:
        return ""
    f = re.sub(r"^h", "", f)
    f = f.replace("qu", "k").replace("c", "k").replace("z", "s")
    f = f.replace("x", "s").replace("j", "s").replace("g", "k")
    f = f.replace("v", "b").replace("w", "u").replace("y", "i")
    return re.sub(r"(.)\1+", r"\1", f)


# ═════════════════════════════════════════════════════════════════════════
# Páginas: las cabeceras corridas del libro, con su número
# ═════════════════════════════════════════════════════════════════════════
CABECERA = re.compile(r"(?mi)^[^\n]{0,10}(PREHISTORIA\s+D[\w.]{1,2}\s+P[^\n]{0,14}|"
                      r"[^\n]{0,16}\b[CO.]{0,2}[LE][LE]-?\s+Y\s+TOST\w?)[^\n]{0,10}$")
NUMERO = re.compile(r"(?m)^[ 	]*((?:[0-9QOoIlSÍ()>¿][ 	]?){2,4})[ 	]*$")
OCR_DIGITOS = str.maketrans({"Q": "9", "O": "0", "o": "0", "I": "1", "l": "1", "S": "5",
                             "Í": "2", "(": "", ")": "", ">": "", "¿": "", " ": ""})


def paginas(t):
    """[(offset_de_la_cabecera, pagina)] — una cabecera por página, numerada.

    El número impreso va encima (páginas pares) o debajo (impares) de la cabecera, y el OCR
    lo lee mal a veces (`2(>0`, `238` por 258, `Í00`). Se toma el número más cercano que
    encaja en la serie y los huecos se rellenan contando cabeceras: una cabecera = una página.
    """
    nums = []
    for m in NUMERO.finditer(t):
        s = m.group(1).replace("(>", "6").translate(OCR_DIGITOS)
        if s.isdigit() and 1 <= int(s) <= 300:
            nums.append((m.start(), int(s)))
    # marcas de página: los números sueltos y las cabeceras que no tienen número al lado
    marcas = [(o, n) for o, n in nums]
    for m in CABECERA.finditer(t):
        if not any(abs(o - m.start()) < 90 for o, _ in nums):
            marcas.append((m.start(), None))
    marcas.sort()
    fusion = []
    for o, n in marcas:
        if fusion and o - fusion[-1][0] < 90:
            if fusion[-1][1] is None:
                fusion[-1] = (fusion[-1][0], n)
            continue
        fusion.append((o, n))
    cabs = [o for o, _ in fusion]
    leidos = [n for _, n in fusion]
    # la serie más larga de lecturas coherentes: crecen, y entre dos cabeceras hay al menos
    # una página y como mucho tres más (las primeras páginas de capítulo no llevan cabecera)
    idx = [i for i, n in enumerate(leidos) if n is not None]
    mejor = {}
    for a, i in enumerate(idx):
        mejor[i] = (1, None)
        for j in idx[:a]:
            d = leidos[i] - leidos[j]
            if (i - j) <= d <= (i - j) + 3 and mejor[j][0] + 1 > mejor[i][0]:
                mejor[i] = (mejor[j][0] + 1, j)
    fin = max(mejor, key=lambda k: (mejor[k][0], -k)) if mejor else None
    anclas = {}
    while fin is not None:
        anclas[fin] = leidos[fin]
        fin = mejor[fin][1]
    fijados = [None] * len(cabs)
    orden = sorted(anclas)
    for i in range(len(cabs)):
        if i in anclas:
            fijados[i] = anclas[i]
            continue
        prev = max((j for j in orden if j < i), default=None)
        nxt = min((j for j in orden if j > i), default=None)
        if prev is not None:
            v = anclas[prev] + (i - prev)
            if nxt is None or v < anclas[nxt]:
                fijados[i] = v
        elif nxt is not None:
            fijados[i] = anclas[nxt] - (nxt - i)
    return list(zip(cabs, fijados))


def pagina_de(offset, pags, inicio_capitulo=None):
    """La página de un offset. La primera página de un capítulo no lleva cabecera ni número:
    lo que cae entre el título del capítulo y la primera marca es de (esa marca − 1)."""
    offs = [o for o, _ in pags]
    i = bisect.bisect_right(offs, offset) - 1
    if inicio_capitulo is not None and (i < 0 or offs[i] < inicio_capitulo):
        if i + 1 < len(pags) and pags[i + 1][1] is not None:
            return pags[i + 1][1] - 1
    if i < 0:
        return None
    return pags[i][1]


def quitar_cabeceras(bloque):
    bloque = CABECERA.sub("\n", bloque)
    bloque = re.sub(r"(?m)^\s*PREHISTORIA\s*[.—-]+\s*\S{1,4}\s*$", "\n", bloque)  # firma de pliego
    bloque = NUMERO.sub(lambda m: "\n" if m.group(1).translate(OCR_DIGITOS).isdigit() else m.group(0),
                        bloque)
    return bloque


# ═════════════════════════════════════════════════════════════════════════
# Parsers
# ═════════════════════════════════════════════════════════════════════════
INICIO_XII = re.compile(r"(?m)^\s*CAPITULO\s+XII\s*$")
FIN_XII = re.compile(r"(?m)^\s*APENDICE\s+FOTOGRAFICO")
INICIO_X = re.compile(r"(?m)^\s*CAPITULO\s+X\s*$")
FIN_X = re.compile(r"(?m)^\s*CAPITULO\s+XI\s*$")
LETRA = re.compile(r"^\s*[A-ZÑ]{1,2}\s*$|^\s*[a-zñ]\s*$")
# Cabeza de entrada: palabra(s) con mayúscula + separador (« . — », «.—», « —», «. »)
CABEZA = re.compile(
    r"^\s*(?P<cab>[A-ZÁÉÍÓÚÑ](?:[\wáéíóúüñÁÉÍÓÚÑ’'\-]|\s(?=[a-záéíóúñ]{1,}\b)|"
    r"\s(?=[A-ZÁÉÍÓÚÑ][a-záéíóúñ]))*?)\s*(?P<sep>[.,]?\s*[—–-]{1,3}|\.)\s+(?P<resto>.+)$", re.S)


def _en_blanco(bloque):
    """Borra cabeceras corridas, números de página y firmas de pliego SIN mover los offsets:
    se sustituyen por espacios del mismo largo (los saltos de línea se conservan)."""
    def blanco(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    bloque = CABECERA.sub(blanco, bloque)
    bloque = re.sub(r"(?m)^\s*(PREHISTORIA|RKÍ-\.\s*HISTORIA)\s*[.—-]+\s*\S{1,4}\s*$", blanco, bloque)
    bloque = re.sub(r"(?m)^\s*DR\.?\s*$", blanco, bloque)
    bloque = NUMERO.sub(lambda m: blanco(m)
                        if m.group(1).replace("(>", "6").translate(OCR_DIGITOS).isdigit()
                        else m.group(0), bloque)
    return bloque


# Dentro de un párrafo, otra entrada empieza tras un cierre de frase con «Cabeza. — » o «Cabeza.—».
CORTE_INTERNO = re.compile(
    r"(?<=[.”\"»)\]])\s+(?=[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{1,20}(?:\s[a-záéíóúñ]{1,12})?\s?[.,]\s?[—–]{1,2}\s)")


def _parrafos(bloque, base, pags):
    """Párrafos con su offset (para la página); un párrafo con entradas pegadas se parte."""
    out = []
    for m in re.finditer(r"(?:[^\n]|\n(?!\s*\n))+", bloque):
        trozo = m.group(0)
        s = " ".join(trozo.split())
        if not s:
            continue
        piezas = CORTE_INTERNO.split(s)
        if len(piezas) == 1:
            out.append((base + m.start(), s))
            continue
        pos = 0
        for pz in piezas:
            k = s.find(pz, pos)
            pos = k + len(pz)
            frac = k / max(1, len(s))
            out.append((base + m.start() + int(frac * len(trozo)), pz))
    return out


def _normaliza_cabeza(c):
    c = c.strip(" ,.;")
    # «Y uca» → «Yuca», «Ar amaná» → «Aramaná», «G u ay ama» → «Guayama»
    c = re.sub(r"\b([A-ZÁÉÍÓÚÑ])\s(?=[a-záéíóúñ])", r"\1", c)
    c = re.sub(r"(?<=[a-záéíóúñ])\s(?=[a-záéíóúñ]{1,2}\b)", "", c)
    return c


def autoridades(texto):
    cr = [n for n, rx in CRONISTAS.items() if re.search(rx, texto)]
    ot = [n for n, rx in OTRAS.items() if re.search(rx, texto)]
    return cr, ot


def islas(texto):
    return [n for n, rx in ISLAS.items() if re.search(rx, texto)]


def campo_de(glosa, texto):
    for nombre, rx in CAMPOS:
        if nombre in ("creencia",):
            if re.search(rx, glosa, re.I):
                return nombre
            continue
        if re.search(rx, glosa.strip()):
            return nombre
    return "otro"


def primera_frase(resto):
    """La glosa: la primera oración (hasta el primer punto que cierra), sin citas largas."""
    m = re.match(r"(.+?[^A-Z\s][\.!?])(\s|$)", resto)
    g = m.group(1) if m else resto
    return g.strip()[:180]


def binomio(texto):
    for m in re.finditer(r"\(\s*([A-Z][a-zé]+)\s+([a-zé]+)\s*\.?\s*\)", texto):
        return "%s %s" % (m.group(1), m.group(2))
    return None


SONIDO = re.compile(r"[^.]{0,120}\b(canto|canta|cantan|grito|grita|chilla|silba|silbido|"
                    r"onomatop|sonido|ruido|croa|zumba|zumbido|graznido|voz\s+de|mugido|"
                    r"aúlla|ladra|ladrido)\b[^.]{0,120}\.", re.I)


def transcribir_xii(t, pags):
    a = INICIO_XII.search(t, 300000)
    b = FIN_XII.search(t, a.end())
    bloque = _en_blanco(t[a.end():b.start()])
    base = a.end()
    parr = _parrafos(bloque, base, pags)
    entradas = []
    actual = None
    empezado = False
    letra = "A"
    for off, s in parr:
        s_limpio = s.strip()
        if not empezado:          # el sumario del capítulo llega hasta la letra «A»
            empezado = bool(re.match(r"^A$", s_limpio))
            continue
        if not s_limpio:
            continue
        if LETRA.match(s_limpio):
            letra = s_limpio.strip().upper()[:1]
            continue
        if re.fullmatch(r"[\]\}¡|\\]", s_limpio):      # la letra de sección leída como símbolo
            letra = chr(ord(letra) + 1) if letra else None
            continue
        # basura del margen interior antes de la cabeza («“ l5 lguanamá», «12 '^ímotonex») y la
        # mayúscula que el OCR lee `]`, `}`, `¡` o `\`: en la sección I es I y en la J es J
        # («]na bón» = Inabón, «] ácana» = Jácana), así que se repone la letra de la sección
        s_limpio = re.sub(r"^[^\w\]\}¡\\]{0,6}\d{0,3}[^\w\]\}¡\\]{0,4}(?=[\w\]\}¡\\])", "", s_limpio)
        if letra:
            s_limpio = re.sub(r"^[\]\}¡\\l]\s?(?=[a-záéíóúñA-Z])",
                              lambda _m: letra if letra in "IJ" else _m.group(0), s_limpio)
        m = CABEZA.match(s_limpio)
        es_cabeza = bool(m) and len(m.group("cab")) <= 45 and not re.match(
            r"^(El|La|Los|Las|En|De|Dice|Según|Pedro|Oviedo|Colón|Nosotros|Hay|Así|Este|Esta|"
            r"Por|Como|Cuando|Pero|Si|No|Se|Y|Todavía|Tenía|Fue|Era|Véase)\b", m.group("cab"))
        if es_cabeza and actual is not None and actual["texto"].rstrip().endswith("-"):
            es_cabeza = False
        if es_cabeza:
            actual = {"off": off, "cab": m.group("cab"), "texto": m.group("resto"), "cap": base}
            entradas.append(actual)
        elif actual is not None:
            unido = actual["texto"].rstrip()
            if unido.endswith("-"):
                actual["texto"] = unido[:-1] + s_limpio
            else:
                actual["texto"] = unido + " " + s_limpio
    return entradas


def transcribir_x(t, pags):
    a = INICIO_X.search(t, 290000)
    b = FIN_X.search(t, a.end())
    bloque = _en_blanco(t[a.end():b.start()])
    base = a.end()
    # en el cap. X cada entrada es «Glosa. — Voz; Ci. x; Cn. y…» y ocupa uno o dos renglones
    parr = _parrafos(bloque, base, pags)
    entradas = []
    actual = None
    empezado = False
    for off, s in parr:
        if not s:
            continue
        if not empezado:
            if re.match(r"^A\s*$", s):
                empezado = True
            continue
        if LETRA.match(s) or s.startswith("("):
            continue
        # un párrafo puede traer varias entradas pegadas (el OCR junta renglones)
        for pieza in re.split(r"(?<=[.])\s+(?=[A-ZÁÉÍÓÚÑ][^.;]{1,60}?\.\s*[—–-])", s):
            m = re.match(r"^\s*(?P<gl>[A-ZÁÉÍÓÚÑ¡!][^—–]{0,90}?)\s*[.,]?\s*[—–-]{1,3}\s*(?P<resto>.+)$", pieza)
            if m and not pieza[:1].islower():
                actual = {"off": off, "glosa": m.group("gl").strip(" .,"), "resto": m.group("resto"),
                          "cap": base}
                entradas.append(actual)
            elif actual is not None:
                actual["resto"] = actual["resto"].rstrip("- ") + " " + pieza
    return entradas


ABREV_X = collections.OrderedDict([
    ("Ci", "caribe insular"), ("Cn", "caribe continental"), ("Ar", "aruaca"),
    ("Gl", "galibi"), ("Ru", "rucuyano"), ("Gní", "guaraní"), ("Gn", "guaraní"),
    ("Kg", "koggaba"), ("Chb", "chibcha"), ("My", "maya"), ("Ntl", "náhuatl"),
    ("Qé", "quiché"), ("Qchú", "quichua"), ("Dk", "dakota"), ("DD", "dené-dindjié"),
])


def partir_x(resto):
    """«Bija; Ci. rocú; Cn. urukú…» → (voz, {lengua: forma}, cola)."""
    trozos = [x.strip() for x in re.split(r";", resto)]
    voz = trozos[0]
    cola = ""
    m = re.match(r"^(.+?)[.]\s+(.+)$", voz)
    if m and len(trozos) == 1:
        voz, cola = m.group(1), m.group(2)
    comp = collections.OrderedDict()
    for tr in trozos[1:]:
        mm = re.match(r"^([A-Z][A-Za-zíéú]{0,3})[.,]\s*(.+)$", tr)
        if mm and mm.group(1) in ABREV_X:
            comp.setdefault(ABREV_X[mm.group(1)], mm.group(2).strip(" ."))
        else:
            cola = (cola + " " + tr).strip()
    return voz.strip(" ."), comp, cola


# ═════════════════════════════════════════════════════════════════════════
# El lexicón, de sólo lectura
# ═════════════════════════════════════════════════════════════════════════
def claves_tainas():
    ks = {}
    for k, v in CL.VOCABULARIO_BASE.items():
        if str(v.get("fuente") or "").startswith("taíno"):
            ks.setdefault(_lema(k), []).append(k)
    for cast, ind in (getattr(CL, "FORMA_DE_LA_ESFERA", {}) or {}).items():
        if ind in CL.VOCABULARIO_BASE and str(CL.VOCABULARIO_BASE[ind].get("fuente") or "").startswith("taíno"):
            ks.setdefault(_lema(cast), []).append(ind)
    return ks


def construir():
    t = io.open(FUENTE, encoding="utf-8").read()
    pags = paginas(t)
    lex = claves_tainas()

    voces = []
    fauna = []
    por_tipo = collections.Counter()
    for e in transcribir_xii(t, pags):
        cab = _normaliza_cabeza(e["cab"])
        texto = e["texto"].strip()
        glosa = primera_frase(texto)
        cr, ot = autoridades(texto)
        sacada = SACADA.search(texto)
        conj = CONJETURA.search(texto)
        if sacada:
            tipo = "sacada-por-el-autor"
        elif cr:
            tipo = "documentada"
        elif conj:
            tipo = "conjetura-del-autor"
        elif ot:
            tipo = "secundaria"
        else:
            tipo = "afirmada-sin-fuente"
        clave = REVISADO_A_MANO.get(cab, {})
        tipo = clave.get("tipo_de_apoyo", tipo)
        por_tipo[tipo] += 1
        pag = pagina_de(e["off"], pags, e["cap"])
        camp = clave.get("campo") or campo_de(glosa, texto)
        entrada = collections.OrderedDict([
            ("forma_fuente", cab),
            ("glosa_fuente", glosa),
            ("texto", texto if len(texto) <= TOPE_TEXTO else texto[:TOPE_TEXTO].rstrip() + " […]"),
            ("pagina_impresa", pag),
            ("capitulo", "XII"),
            ("fuente_que_declara_el_autor", "; ".join(cr + ot) or "no-declarada"),
            ("cronistas_nombrados", cr or None),
            ("otras_autoridades", ot or None),
            ("tipo_de_apoyo", tipo),
            ("marca", (sacada.group(0) if sacada else (conj.group(0) if conj and not cr else None))),
            ("variedad_o_isla", islas(texto) or "no-declarada"),
            ("campo", camp),
            ("en_el_lexicon", ", ".join(sorted(set(lex.get(_lema(cab), [])))) or None),
            ("ocr", "automatico"),
        ])
        if clave.get("nota"):
            entrada["nota_de_revision"] = clave["nota"]
        voces.append(entrada)
        if camp == "fauna":
            s = SONIDO.search(texto)
            fauna.append(collections.OrderedDict([
                ("nombre_en_fuente", cab),
                ("especie_probable", binomio(texto)),
                ("texto", texto[:400] + (" […]" if len(texto) > 400 else "")),
                ("obra", OBRA),
                ("pagina_impresa", pag),
                ("lugar", ", ".join(islas(texto)) or "Antillas (no declarado)"),
                ("epoca", "contacto-temprano" if cr else "moderno"),
                ("sonido", s.group(0).strip() if s else None),
            ]))

    inversas = []
    kalinago_en_coll = []
    for e in transcribir_x(t, pags):
        voz, comp, cola = partir_x(e["resto"])
        pag = pagina_de(e["off"], pags, e["cap"])
        inversas.append(collections.OrderedDict([
            ("glosa_fuente", e["glosa"]),
            ("forma_fuente", voz),
            ("comparanda", dict(comp) or None),
            ("resto", cola or None),
            ("pagina_impresa", pag),
            ("capitulo", "X"),
            ("en_el_lexicon", ", ".join(sorted(set(lex.get(_lema(voz), [])))) or None),
            ("ocr", "automatico"),
        ]))
        if "caribe insular" in comp:
            kalinago_en_coll.append({"glosa": e["glosa"], "boriqueño": voz,
                                     "caribe_insular": comp["caribe insular"],
                                     "caribe_continental": comp.get("caribe continental"),
                                     "aruaca": comp.get("aruaca"), "pagina_impresa": pag})

    salida = collections.OrderedDict()
    salida["meta"] = collections.OrderedDict([
        ("obra_id", OBRA),
        ("autor", "Coll y Toste, Cayetano"),
        ("titulo", "Prehistoria de Puerto Rico"),
        ("campana", "tercera campaña de minería — parcela M5 (vocabularios antillanos)"),
        ("medido", "2026-09-22"),
        ("script", "6-fusion/scripts/transcribir_coll_y_toste.py"),
        ("estado", "PROPUESTA (regla 5). Transcripción AUTOMÁTICA sobre OCR ajeno; lo que decide "
                   "algo se revisó a mano (`REVISADO_A_MANO` en el script)."),
        ("edicion_que_se_lee", (
            "🔴 NO es la de 1897. La portada del escaneo es la SEGUNDA edición: Isabel Cuchí Coll "
            "(ed.), Bilbao, Editorial Vasco Americana, s. f., «Todos los derechos reservados»; "
            "lleva un apéndice fotográfico del Instituto de Cultura Puertorriqueña (fundado en "
            "1955) y el texto cita obras de 1907 (Segarra y Juliá). 1897 es la fecha del premio de "
            "la Sociedad Económica de Amigos del País. Las páginas son las de esta edición.")),
        ("derechos", (
            "el texto de Coll y Toste (†1930) es de dominio público; el prólogo de la editora y el "
            "apéndice fotográfico no. Aquí sólo se transcribe el texto del autor.")),
        ("fuente", "fuentes_caquetios/CollYToste_1897_Prehistoria_Puerto_Rico.ocr.txt (OCR de archive.org)"),
        ("tope_de_texto", "cada `texto` se recorta a %d caracteres; el entero está en el .ocr.txt" % TOPE_TEXTO),
        ("clases_de_apoyo", collections.OrderedDict([
            ("documentada", "nombra al menos un cronista del XV-XVI o un documento de época"),
            ("secundaria", "sólo nombra autoridades del XVII-XIX (Pichardo, Bachiller, García, Breton…)"),
            ("afirmada-sin-fuente", "el autor la da por indígena y no dice de dónde"),
            ("conjetura-del-autor", "sin cronista, y el autor analiza, traduce o reconstruye "
                                    "(«radical», «significa», «creemos», «polisintetismo») → clase iii"),
            ("sacada-por-el-autor", "el propio autor la manda a otra lengua o la llama error"),
        ])),
    ])
    salida["resumen"] = collections.OrderedDict([
        ("entradas_cap_XII", len(voces)),
        ("por_tipo_de_apoyo", dict(sorted(por_tipo.items()))),
        ("por_campo", dict(sorted(collections.Counter(v["campo"] for v in voces).items()))),
        ("con_isla_declarada", sum(1 for v in voces if v["variedad_o_isla"] != "no-declarada")),
        ("tocan_una_clave_taina_del_lexicon_por_forma", sum(1 for v in voces if v["en_el_lexicon"])),
        ("entradas_cap_X", len(inversas)),
        ("cap_X_con_forma_de_caribe_insular", len(kalinago_en_coll)),
        ("animales", len(fauna)),
        ("paginas_cap_XII", "%s-%s" % (voces[0]["pagina_impresa"], voces[-1]["pagina_impresa"])),
        ("paginas_cap_X", "%s-%s" % (inversas[0]["pagina_impresa"], inversas[-1]["pagina_impresa"])),
    ])
    salida["voces"] = voces
    salida["vocabulario_espanol_boriqueno"] = inversas
    salida["caribe_insular_segun_coll"] = kalinago_en_coll
    salida["fauna"] = fauna
    return salida


def texto_yaml(d):
    def rep(dumper, data):
        return dumper.represent_dict(data.items())
    yaml.add_representer(collections.OrderedDict, rep, Dumper=yaml.SafeDumper)
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=100)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    s = construir()
    nuevo = texto_yaml(s)
    if a.check:
        viejo = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        ok = viejo == nuevo
        print(("✓ %s está al día" if ok else "✗ %s DESFASADO") % os.path.relpath(SALIDA, R))
        return 0 if ok else 1
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(nuevo)
    for k, v in s["resumen"].items():
        print("  %-45s %s" % (k, v))
    print("✓", os.path.relpath(SALIDA, R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
