"""
CURIANA — Descomposición del corpus toponímico y antroponímico  (tarea F11)
===========================================================================

**La idea.** El proyecto venía archivando los topónimos como *canon inerte*:
`minar_zavala_glosario.py`, `minar_gatschet.py` y `minar_van_buurt.py` los
apartan del habla activa ("fuera del habla por diseño"). La exclusión del habla
es correcta —un agente no debería decir *Bariquisimeto*— pero tuvo un efecto
colateral que nadie vio:

    Los topónimos vienen con su traducción.
    Son ECUACIONES BILINGÜES de las que se puede despejar el morfema.

El caso que lo destapó:

    juri        = 'viento, ventarrón'   ← ya en el lexicón, caquetío-atestiguado
    ebo         = 'camino, paso, senda' ← ya en el lexicón, caquetío-atestiguado
    jurijurebo  = 'Paso de los vientos' ← estaba en TOPONIMOS_ZAVALA, fuera del
                                          habla, marcado "glosa incierta"

El topónimo descompone limpio en dos morfemas ya atestiguados **y su glosa lo
confirma**. Y `juri~juri` es reduplicación — un proceso que Gatschet 1885
documenta explícitamente para el arubano y que **no está en `REGLAS_ZAVALA`**.
Un solo topónimo confirma dos palabras y sugiere una regla morfológica.

**El método** es criptoanálisis con texto plano conocido: se tiene la forma y se
tiene el significado; se despejan las partes.

    1. SEGMENTAR contra el inventario de morfemas ya conocido.
    2. ALINEAR los segmentos con las partes de la glosa española.
    3. DESPEJAR el morfema desconocido cuando los demás encajan.
    4. VALIDAR POR RECURRENCIA: un morfema en un solo topónimo es conjetura;
       en tres o cuatro con glosa consistente es un hallazgo.

**Regla cero, no negociable.** Una segmentación que "suena bien" no es
evidencia. El proyecto ya pagó ese precio: 441 formas transducidas sin verificar
cognación, ~80% de fallo medido, hoy aisladas en `lexicon_candidatos.py`.
Segmentar topónimos tiene la misma tentación —cortar donde convenga hasta que
cuadre—, así que aquí rigen tres defensas:

    · La GLOSA MANDA sobre la forma. Si la segmentación no reconstruye la
      traducción que da la fuente, es falsa aunque suene perfecta.
    · RECURRENCIA MÍNIMA ≥2 topónimos independientes para promover un morfema
      nuevo, y hay que decir cuáles.
    · Los topónimos COLONIALES/MODERNOS y las glosas MERAMENTE REFERENCIALES
      ("Nombre propio", "Cacique de…") no rinden ecuación: se apartan.

Fuentes de material (ninguna se modifica; se leen):

    lexicon_zavala.TOPONIMOS_ZAVALA        45  CON GLOSA DESCRIPTIVA ESPAÑOLA
    lexicon_zavala.ANTROPONIMOS_ZAVALA     14  ídem
    lexicon_zavala.AFIJOS_ZAVALA            8  afijos atestiguados
    lexicon_gatschet.GATSCHET_TOPONIMOS    31  Aruba 1885, SIN glosa
    lexicon_van_buurt.TOPONIMOS_VAN_BUURT 176  §7 ABC, SIN glosa
    lexicon_van_buurt.ETIMOLOGIAS_TOPONIMOS 15  §8-10, comentario etimológico
    lexicon_van_buurt.MORFEMAS_VAN_BUURT   19  morfemas con autoridad y glosa
    curiana_lexicon.VOCABULARIO_BASE          formas de familia caquetía

Los 207 topónimos insulares SIN glosa no rinden ecuación: solo sirven como
**control de recurrencia** de los morfemas despejados en los que sí la tienen.
Es una asimetría importante y el informe la reporta como tal.

Uso:
    python minar_toponimos.py                 # informe completo
    python minar_toponimos.py --json out.json
    python minar_toponimos.py --generar-modulo   # volcado crudo para auditar

⚠ `lexicon_toponimos.py` NO se genera desde aquí: es la propuesta **curada a
mano** sobre estos candidatos. En un método que consiste en cortar palabras
hasta que cuadren, dejar decidir al algoritmo *es* el error. Este script
produce candidatos y cuentas de recurrencia; el veredicto A/B/C/D con su razón
lo pone una persona.

NO modifica curiana_lexicon.py ni ningún lexicon_*.py de las minerías previas:
emite una PROPUESTA para revisión humana, en la misma disciplina que
minar_zavala_glosario.py y minar_pares_validacion.py.
"""

import argparse
import io
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _forzar_utf8() -> None:
    """La consola de Windows usa cp1252 y el informe imprime "─", "→", "í"…"""
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


# ───────────────────────────────────────────────────────────────────────────
# 0. Normalización
# ───────────────────────────────────────────────────────────────────────────

FAMILIA_CAQUETIA = {
    "caquetío-atestiguado", "caquetío-reconstruido",
    "caquetío", "caquetío/topónimo",
}

# Correspondencias grafémicas entre las tres tradiciones ortográficas del
# corpus: Zavala (castellanizante), Gatschet 1885 (anglo-alemana) y van Buurt
# (papiamentu/neerlandesa). Sin esto, `quiba` y `kiba` o `guaca` y `waka` no se
# reconocen como la misma forma y la recurrencia sale artificialmente baja.
# El orden importa: cada regla se aplica sobre el resultado de la anterior.
_EQUIV = [
    (r"[çz]", "s"),
    (r"c(?=[ei])", "s"),      # ⚠ español: `barici` = /barisi/, NO /bariki/.
    (r"qu(?=[ei])", "k"),     # `quiba` = /kiba/
    (r"c", "k"),
    (r"qu", "k"),
    (r"[gh]u(?=[aeiouáéíóú])", "w"),   # gua-, hue- = glide /w/  (guacaubana, huay)
    (r"g(?=[uü][aeiou])", "w"),
    (r"[jx]", "h"),           # /x/ ~ /h/: juri (Zavala) ≡ hudi (van Buurt)
    (r"y", "i"),
    (r"v", "b"),
    (r"ñ", "n"),
    (r"ü", "u"),
]


def sin_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def clave(forma: str) -> str:
    """Forma canónica para comparar entre las tres ortografías del corpus.

    Zavala escribe a la española, Gatschet 1885 a la anglo-alemana y van Buurt
    a la papiamentu/neerlandesa. Sin normalizar, `quibacoa` ≠ `kibakoa`,
    `Guadirikiri` ≠ `Wadirikiri` y `barici` ≠ `barisi` — y la recurrencia, que
    es el control de calidad de todo el método, sale artificialmente baja.
    """
    s = sin_acentos(forma).lower()
    s = re.sub(r"[^a-zñü]", "", s)
    for pat, rep in _EQUIV:
        s = re.sub(pat, rep, s)
    s = re.sub(r"(.)\1+", r"\1", s)      # geminadas: Kassibari → kasibari
    return s


def _distancia(a, b):
    """Levenshtein simple, para detectar glosas circulares castellanizadas."""
    if abs(len(a) - len(b)) > 3:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


# ───────────────────────────────────────────────────────────────────────────
# 1. Glosas españolas: comparación por raíz truncada
# ───────────────────────────────────────────────────────────────────────────

_VACIAS = {
    "de", "del", "la", "el", "los", "las", "un", "una", "unos", "unas", "y",
    "o", "en", "para", "por", "con", "que", "se", "su", "sus", "al", "a",
    "muy", "mas", "es", "son", "lo", "designar", "puede", "ser", "tambien",
    "especie", "cerca", "aspecto", "originalmente", "the", "of", "is",
    "escrito", "todo", "toda", "nombre", "propio", "indigena", "indigenas",
    # genéricos de topónimo: aparecen en casi toda glosa y en casi toda glosa
    # de morfema, así que alinean con cualquier cosa. No son evidencia.
    "sitio", "lugar", "punto", "paraje", "place", "site", "parte",
}

# ── Campos semánticos ───────────────────────────────────────────────────────
# El paso más delicado del método. Sin esto, `adabacoa` = "Todo arboleda" no
# alinea con `bacoa` = 'bosque, lugar, paraje': el stemmer no sabe que
# *arboleda* y *bosque* son lo mismo. Con esto sí — pero cada equivalencia es
# una decisión, así que van EXPLÍCITAS y auditables, no en un embedding opaco.
# Criterio de admisión: solo sinonimia de diccionario en el campo del paisaje.
# NO se meten equivalencias "de conveniencia" para hacer cuadrar un topónimo
# concreto (eso sería exactamente la trampa que la Regla Cero prohíbe).
CAMPOS_SEMANTICOS = {
    "vegetación": ["bosque", "bosques", "arboleda", "arbol", "arboles", "monte",
                   "matorral", "espesura", "arbolado", "selva", "arbustos",
                   "thicket"],
    "agua": ["agua", "aguas", "rio", "quebrada", "arroyo", "riachuelo",
             "laguna", "humedad", "humedo", "mojado", "wet", "humid", "water",
             "manantial", "pozo"],
    "tierra": ["tierra", "tierras", "suelo", "region", "terreno", "comarca",
               "land", "campo"],
    "mar": ["mar", "marino", "costa", "orilla", "playa", "sea", "shore",
            "coast", "ribera"],
    "poblado": ["pueblo", "poblado", "caserio", "aldea", "comunidad", "gente",
                "asiento", "village", "poblacion"],
    "piedra": ["piedra", "piedras", "roca", "rocas", "pedregoso", "pedregosos",
               "rocoso", "stone", "rock", "peñasco"],
    "cultivo": ["cultivo", "conuco", "heredad", "sembrado", "maizal",
                "maizales", "hato", "labranza", "sementera", "cultivos"],
    "viento": ["viento", "vientos", "ventarron", "wind", "windy", "brisa"],
    "camino": ["camino", "paso", "senda", "vereda", "trocha", "path"],
    "relieve": ["cerro", "serrania", "montaña", "loma", "colina", "sierra",
                "hill", "cordillera", "altura"],
    "arena": ["arena", "arenoso", "arenal", "sand"],
    "cardón": ["cardon", "cactus", "cactaceo", "cactacea", "cacti"],
    "abundancia": ["abundancia", "abunda", "muchos", "muchas", "lleno",
                   "numeroso", "numerosos", "many", "much", "pluralidad"],
    "llano": ["llano", "llanura", "plano", "plain", "wide", "ancho", "sabana"],
    "escondido": ["escondido", "oculto", "subterraneo", "underground",
                  "soterrado"],
    "barro": ["barro", "arcilla", "loza", "greda", "clay"],
}

_A_CAMPO = {}
for _campo, _palabras in CAMPOS_SEMANTICOS.items():
    for _p in _palabras:
        _A_CAMPO[sin_acentos(_p)[:4]] = "@" + _campo


def raices(texto: str) -> set:
    """Conjunto de conceptos de una glosa española.

    Trunca a 4 caracteres —así `bosques`/`bosque`, `aguas`/`agua`,
    `arboleda`/`árbol`, `vientos`/`viento` colapsan— y luego proyecta al campo
    semántico cuando lo hay. Es un stemmer pobre, pero el error que importa
    evitar aquí es el falso NEGATIVO (perder una alineación real por una `-s`),
    no el falso positivo: toda alineación positiva se revisa después contra la
    recurrencia.
    """
    out = set()
    for p in re.split(r"[^\wáéíóúüñ]+", sin_acentos(texto).lower()):
        if not p or p in _VACIAS or len(p) < 3:
            continue
        r = p[:4] if len(p) >= 4 else p
        out.add(_A_CAMPO.get(r, r))
    return out


def palabras_de(texto: str) -> list:
    """Las palabras de contenido de una glosa, sin truncar (para informes)."""
    return [p for p in re.split(r"[^\wáéíóúüñ]+", sin_acentos(texto).lower())
            if p and p not in _VACIAS and len(p) >= 3]


# ───────────────────────────────────────────────────────────────────────────
# 2. Inventario de morfemas conocidos
# ───────────────────────────────────────────────────────────────────────────

def inventario_morfemas():
    """{clave: {'forma','glosa','origen','tipo'}} — todo lo ya atestiguado."""
    import curiana_lexicon as L
    import lexicon_zavala as Z
    import lexicon_van_buurt as VB

    inv = {}

    def add(forma, glosa, origen, tipo):
        k = clave(forma)
        if len(k) < 2:
            return
        if k in inv:
            # glosas acumulativas: un morfema puede estar en dos fuentes
            if glosa and glosa not in inv[k]["glosa"]:
                inv[k]["glosa"] += " / " + glosa
            if origen not in inv[k]["origen"]:
                inv[k]["origen"] += " + " + origen
            return
        inv[k] = {"forma": forma, "glosa": glosa, "origen": origen, "tipo": tipo}

    for w, d in L.VOCABULARIO_BASE.items():
        if d.get("fuente") in FAMILIA_CAQUETIA and d.get("sig"):
            add(w, d["sig"], f"lexicón ({d['fuente']})", "palabra")

    for a, d in Z.AFIJOS_ZAVALA.items():
        add(a.strip("-"), d["glosa"], "AFIJOS_ZAVALA", "afijo")

    for a, d in VB.MORFEMAS_VAN_BUURT.items():
        add(a.strip("-"), d["glosa"], "MORFEMAS_VAN_BUURT", "morfema")
        if d.get("forma_alt"):
            for alt in re.split(r"[,/]", d["forma_alt"]):
                alt = alt.strip().strip("-")
                if alt:
                    add(alt, d["glosa"], "MORFEMAS_VAN_BUURT (var.)", "morfema")

    # Afijos de trabajo del proyecto que `REGLAS_ZAVALA`/el prompt ya usan y
    # que no viven en VOCABULARIO_BASE como entradas independientes.
    for a, g in [("bana", "orilla, borde; llano"), ("ana", "lugar de"),
                 ("ko", "interior de")]:
        add(a, g, "reglas morfológicas del proyecto", "afijo")

    return inv


# Morfemas de 2 caracteres que la segmentación puede usar. Cualquier bigrama
# libre trocea cualquier palabra: sin esta lista blanca el segmentador produce
# "análisis" por fuerza bruta y la Regla Cero se viola de inmediato.
BIGRAMAS_PERMITIDOS = {"ko", "wa", "ka", "ri", "bi"}


# ───────────────────────────────────────────────────────────────────────────
# 3. Corpus toponímico
# ───────────────────────────────────────────────────────────────────────────

# Glosas que solo IDENTIFICAN el referente (quién/dónde) sin describirlo. No
# rinden ecuación bilingüe: no hay significado que despejar.
_RE_REFERENCIAL = re.compile(
    r"^(nombre propio|apellido|poblaci[oó]n de|poblaci[oó]n$|caci(que|ca) de|"
    r"indio |ind[ií]gena d|asiento ind[ií]gena|comunidad ind[ií]gena|"
    r"nombre de caci|nombre ind[ií]gena|escrito originalmente)", re.I)


def parte_descriptiva(glosa: str) -> str:
    """Quita de la glosa las cláusulas que solo IDENTIFICAN al referente.

    `chunare` = *"Apellido. Mazorca tierna"* es media glosa referencial y media
    descripción: descartarlo entero por empezar con "Apellido" perdía el único
    antropónimo del corpus que sí rinde ecuación. Se evalúa cláusula a
    cláusula.
    """
    partes = [p.strip() for p in re.split(r"[.;]", glosa) if p.strip()]
    utiles = [p for p in partes if not _RE_REFERENCIAL.match(p)]
    return ". ".join(utiles)


def corpus():
    """Devuelve (glosados, sin_glosa).

    glosados: [{'forma','glosa','clase','fuente'}]  — rinden ecuación
    sin_glosa: [{'forma','fuente'}]                 — solo control de recurrencia
    """
    import lexicon_zavala as Z
    import lexicon_gatschet as G
    import lexicon_van_buurt as VB

    glosados, sin_glosa = [], []

    for f, g in Z.TOPONIMOS_ZAVALA.items():
        glosados.append({"forma": f, "glosa": g, "clase": "topónimo",
                         "fuente": "zavala-reyes-2015"})
    for f, g in Z.ANTROPONIMOS_ZAVALA.items():
        glosados.append({"forma": f, "glosa": g, "clase": "antropónimo",
                         "fuente": "zavala-reyes-2015"})
    for f, txt in VB.ETIMOLOGIAS_TOPONIMOS.items():
        base = re.split(r"[,(]", f)[0].strip()
        glosados.append({"forma": base, "glosa": txt, "clase": "topónimo",
                         "fuente": "van-buurt-2014 §8-10", "glosa_en_ingles": True})

    for f in G.GATSCHET_TOPONIMOS:
        sin_glosa.append({"forma": re.split(r"[ (]", f)[0],
                          "fuente": "gatschet-1885"})
    for isla, lst in VB.TOPONIMOS_VAN_BUURT.items():
        for e in lst:
            for var in re.split(r"[,/]", e["toponimo"]):
                var = var.strip().replace(" ", "")
                if var:
                    sin_glosa.append({"forma": var,
                                      "fuente": f"van-buurt-2014 §7 ({isla})"})
    return glosados, sin_glosa


# ───────────────────────────────────────────────────────────────────────────
# 4. Segmentación
# ───────────────────────────────────────────────────────────────────────────

def _colapsar_reduplicacion(k, inv):
    """Reduce `hurihurebo` → `hurebo` marcando la unidad reduplicada.

    Devuelve (clave_reducida, unidad|None). Solo colapsa si la unidad
    reduplicada es un morfema CONOCIDO: colapsar cualquier repetición sería
    fabricar la evidencia que se quiere medir.

    Cubre también la haplología (`juri-jur-ebo`), en que la segunda copia
    pierde su vocal final — el patrón real de `jurijurebo`.
    """
    n = len(k)
    for tam in range(n // 2, 2, -1):
        for i in range(0, n - 2 * tam + 1):
            a, b = k[i:i + tam], k[i + tam:i + 2 * tam]
            if a == b and a in inv:
                return k[:i + tam] + k[i + 2 * tam:], a
        # haplología: la segunda copia truncada en una vocal
        for i in range(0, n - (2 * tam - 1) + 1):
            a, b = k[i:i + tam], k[i + tam:i + 2 * tam - 1]
            if a in inv and a[:-1] == b:
                return k[:i + tam] + k[i + 2 * tam - 1:], a
    return k, None


def _quitar_plural_castellano(k):
    """`kibakoas` → `kibakoa`.

    Zavala transcribe algunos topónimos ya pluralizados en español
    (*Quibacoas* 'Bosques pedregosos', *Cemirucos*). La `-s` es castellana, no
    caquetía, y si no se quita bloquea toda la segmentación.
    """
    return k[:-1] if len(k) > 4 and k.endswith("s") else k


TOPE_SEGMENTACIONES = 600


def segmentaciones(forma, inv, max_residuos=1, clave_dada=None, sandhi=True):
    """TODAS las segmentaciones razonables de `forma` contra `inv`.

    Devuelve una lista de listas [(segmento, clave|None)]; `None` marca residuo
    desconocido. **Deliberadamente no elige**: la elección la hace la glosa en
    `analizar()`.

    Este cambio de diseño es la Regla Cero hecha código. Una primera versión
    elegía la segmentación óptima *por la forma* (máxima cobertura, mínimos
    segmentos) y luego miraba la glosa. Resultado: `Casibari` salía `kasi+bari`
    —dos palabras del lexicón, cobertura perfecta, cero residuos— en vez del
    `ka-siba-rí` 'hay rocas duras' que van Buurt documenta. Ambas cubren los
    ocho caracteres; solo la segunda reconstruye la traducción. Si la forma
    decide primero, el método se convierte en la trampa que dice evitar.

    `sandhi=True` admite que dos morfemas compartan un carácter en la frontera
    (`quiba`+`bacoa` → *quibacoa*). Es haplología real y frecuente en el
    corpus, pero afloja la segmentación, así que se marca en la salida con
    "·" y se pondera peor en el desempate.
    """
    k = clave_dada if clave_dada is not None else clave(forma)
    n = len(k)
    salida = []

    def rec(i, residuos, acc):
        if len(salida) >= TOPE_SEGMENTACIONES:
            return
        if i >= n:
            if i == n:
                salida.append(list(acc))
            return
        for j in range(n, i + 1, -1):
            sub = k[i:j]
            if sub not in inv:
                continue
            if len(sub) == 2 and sub not in BIGRAMAS_PERMITIDOS:
                continue
            acc.append((sub, sub))
            rec(j, residuos, acc)
            acc.pop()
            # haplología: el morfema siguiente reutiliza el último carácter o
            # la última sílaba. `quiba`+`bacoa` → *quibacoa* (comparten "ba");
            # `wa`+`ada`+`bacoa` → *guadabacoa* (comparten "a").
            if sandhi and j < n:
                for ov in (1, 2):
                    if len(sub) >= ov + 2 and j - ov > i:
                        acc.append((sub + "·" * ov, sub))
                        rec(j - ov, residuos, acc)
                        acc.pop()
        if residuos < max_residuos:
            for j in range(n, i + 1, -1):
                acc.append((k[i:j], None))
                rec(j, residuos + 1, acc)
                acc.pop()

    rec(0, 0, [])
    return salida


# ───────────────────────────────────────────────────────────────────────────
# 5. Alineación con la glosa
# ───────────────────────────────────────────────────────────────────────────

# Glosas que no dicen nada: un afijo glosado "desinencia" no puede alinear con
# ninguna traducción, así que contarlo como "no alineado" penalizaría injusta-
# mente la segmentación correcta. Se trata como NEUTRO.
_RE_GLOSA_VACIA = re.compile(
    r"^(desinencia|sufijo|prefijo|ra[ií]z|part[ií]cula|marca)\b", re.I)


def alinear(seg, glosa, inv):
    """¿Cada morfema conocido de la segmentación aporta a la glosa?

    Devuelve (alineados, no_alineados, cobertura_glosa, sin_explicar) donde los
    dos primeros son listas de claves, el tercero es la fracción de conceptos
    de la glosa que algún morfema explica, y el cuarto son los conceptos que
    NINGÚN morfema conocido explica — es decir, **lo que el residuo tiene que
    significar**. Ese conjunto es el despeje.
    """
    rg = raices(glosa)
    alineados, no_alineados, explicadas = [], [], set()
    for sub, m in seg:
        if not m:
            continue
        gm = inv[m]["glosa"]
        rm = raices(gm)
        comun = rm & rg
        if comun:
            alineados.append(m)
            explicadas |= comun
        elif not _RE_GLOSA_VACIA.match(gm.strip()):
            no_alineados.append(m)
    cobertura = len(explicadas) / len(rg) if rg else 0.0
    return alineados, no_alineados, cobertura, rg - explicadas


def elegir_segmentacion(cands, glosa, inv):
    """De todas las segmentaciones posibles, la que MEJOR RECONSTRUYE LA GLOSA.

    Orden de preferencia, en este orden y no en otro:
      1. más conceptos de la glosa explicados      ← la glosa manda
      2. más morfemas que alinean
      3. menos morfemas conocidos que NO alinean   ← castiga el corte oportunista
      4. menos residuos desconocidos
      5. menos haplologías supuestas
      6. menos segmentos (navaja de Occam, la última palabra, no la primera)
    """
    mejor, mejor_clave, mejor_datos = None, None, None
    for seg in cands:
        alin, no_alin, cob, falta = alinear(seg, glosa, inv)
        c = (-cob, -len(alin), len(no_alin),
             sum(1 for _, m in seg if not m),
             sum(s.count("·") for s, _ in seg),
             len(seg))
        if mejor_clave is None or c < mejor_clave:
            mejor, mejor_clave, mejor_datos = seg, c, (alin, no_alin, cob, falta)
    return mejor, mejor_datos


# ───────────────────────────────────────────────────────────────────────────
# 6. Recurrencia
# ───────────────────────────────────────────────────────────────────────────

def indice_recurrencia(glosados, sin_glosa):
    """{substring: [formas que lo contienen]} sobre TODO el corpus toponímico.

    Se calcula sobre las claves normalizadas, de modo que la recurrencia cruza
    las tres ortografías.
    """
    formas = [(e["forma"], clave(e["forma"]), "glosado") for e in glosados]
    formas += [(e["forma"], clave(e["forma"]), "sin_glosa") for e in sin_glosa]
    idx = defaultdict(list)
    for orig, k, tipo in formas:
        vistos = set()
        for i in range(len(k)):
            for j in range(i + 2, min(len(k), i + 9) + 1):
                sub = k[i:j]
                if sub not in vistos:
                    vistos.add(sub)
                    idx[sub].append((orig, tipo))
    return idx


# ───────────────────────────────────────────────────────────────────────────
# 7. Reduplicación
# ───────────────────────────────────────────────────────────────────────────

def reduplicacion(forma, min_unidad=2):
    """Detecta X-X (exacta) y X-X' (parcial, 1 fonema de diferencia).

    Gatschet 1885 sobre los topónimos de Aruba: varios se forman por
    duplicación de la raíz disílaba, proceso usado para onomatopeya, para
    diminutivos, o para objetos que existen en gran número.
    """
    k = clave(forma)
    n = len(k)
    hallazgos = []
    for tam in range(n // 2, min_unidad - 1, -1):
        for i in range(0, n - 2 * tam + 1):
            a, b = k[i:i + tam], k[i + tam:i + 2 * tam]
            if a == b:
                hallazgos.append({"tipo": "exacta", "unidad": a, "pos": i})
            elif tam >= 3 and sum(x != y for x, y in zip(a, b)) == 1:
                hallazgos.append({"tipo": "parcial", "unidad": f"{a}~{b}", "pos": i})
    # nos quedamos con la unidad más larga: es la menos casual
    return hallazgos[:1]


# ───────────────────────────────────────────────────────────────────────────
# 8. Veredicto
# ───────────────────────────────────────────────────────────────────────────

def analizar(entrada, inv, idx):
    """Analiza un topónimo/antropónimo glosado y emite nivel A/B/C/D."""
    forma, glosa = entrada["forma"], entrada["glosa"]
    res = dict(entrada)
    res["clave"] = clave(forma)
    res["reduplicacion"] = reduplicacion(forma)

    # Un topónimo nunca se explica a sí mismo: se retiran del inventario las
    # entradas que salieron de este mismo topónimo (bootstrap o despeje). Las
    # entradas del LEXICÓN con la misma clave sí se conservan: ahí no hay
    # tautología sino corroboración, y la rama de "identidad" la registra.
    inv = {kk: vv for kk, vv in inv.items()
           if not (kk == clave(forma)
                   and vv["tipo"] in ("topónimo-morfema", "despejado"))}

    glosa = parte_descriptiva(glosa)
    res["glosa_util"] = glosa
    if not glosa:
        res.update(nivel="D", razon="glosa meramente referencial: identifica al "
                                    "referente sin describirlo, no hay ecuación "
                                    "bilingüe que resolver",
                   segmentacion=[], alineados=[], no_alineados=[], residuos=[])
        return res

    # glosa circular: la "traducción" es el propio nombre castellanizado
    # (`cemirucos` → "Semerucos"). No aporta ningún significado nuevo.
    kf = clave(forma)
    pal = palabras_de(glosa)
    if len(pal) <= 2 and any(_distancia(clave(p), kf) <= 2 for p in pal):
        res.update(nivel="D", razon="glosa circular: la 'traducción' es el propio "
                                    "topónimo castellanizado",
                   segmentacion=[], alineados=[], no_alineados=[], residuos=[])
        return res

    # identidad: el topónimo ES una palabra del lexicón, sin composición.
    # No hay nada que segmentar, pero sí una corroboración que registrar.
    if kf in inv and raices(inv[kf]["glosa"]) & raices(glosa):
        res.update(nivel="A", razon=f"identidad: el topónimo es la palabra "
                                    f"'{inv[kf]['forma']}' del lexicón y la glosa "
                                    f"coincide — corrobora, no descompone",
                   segmentacion=[{"seg": kf, "morfema": kf,
                                  "glosa": inv[kf]["glosa"]}],
                   alineados=[kf], no_alineados=[], residuos=[],
                   cobertura_glosa=1.0, glosa_por_despejar=[],
                   recurrencia_residuos={})
        return res

    k = _quitar_plural_castellano(clave(forma))
    k, unidad_red = _colapsar_reduplicacion(k, inv)
    res["reduplicacion_de_morfema"] = unidad_red

    cands = segmentaciones(forma, inv, clave_dada=k)
    if cands:
        seg, (alin, no_alin, cob, sin_explicar) = elegir_segmentacion(cands, glosa, inv)
    else:
        seg = [(k, None)]
        alin, no_alin, cob, sin_explicar = [], [], 0.0, raices(glosa)
    if unidad_red:
        seg = [((s + "×2") if s == unidad_red else s, m) for s, m in seg]
    res["segmentacion"] = [{"seg": s, "morfema": m,
                            "glosa": inv[m]["glosa"] if m else None} for s, m in seg]
    residuos = [s for s, m in seg if not m]
    res["alineados"] = alin
    res["no_alineados"] = no_alin
    res["residuos"] = residuos
    res["cobertura_glosa"] = round(cob, 2)
    # lo que la glosa dice y ningún morfema conocido explica: el DESPEJE
    res["glosa_por_despejar"] = sorted(c.lstrip("@") for c in sin_explicar)

    # recurrencia de los residuos (candidatos a morfema nuevo)
    res["recurrencia_residuos"] = {
        r: sorted({f for f, _ in idx.get(r, []) if clave(f) != clave(forma)})
        for r in residuos}

    conocidos = [m for _, m in seg if m]
    if (len(conocidos) >= 2 and not residuos and alin and not no_alin
            and cob >= 0.5):
        res["nivel"] = "A"
        res["razon"] = ("todos los morfemas ya atestiguados y la glosa se "
                        "reconstruye con ellos")
    elif (len(residuos) == 1 and alin and not no_alin and cob >= 0.34
            and len(residuos[0]) >= 3
            and len(res["recurrencia_residuos"][residuos[0]]) >= 1):
        # residuo de <3 caracteres: cualquier bigrama recurre en medio corpus.
        # No es un morfema despejado, es ruido con estadística.
        res["nivel"] = "B"
        res["razon"] = (f"un morfema por despejar ({residuos[0]}) con recurrencia "
                        f"≥2 y el resto alineado con la glosa")
    elif alin or (conocidos and cob > 0):
        res["nivel"] = "C"
        res["razon"] = "segmentación plausible sin recurrencia suficiente"
    else:
        res["nivel"] = "D"
        res["razon"] = "ningún morfema conocido alinea con la glosa"
    return res


def bootstrap(analisis, inv, idx, glosados):
    """Segunda pasada: los propios topónimos glosados son morfemas.

    `yacare` está en `TOPONIMOS_ZAVALA` glosado *"Pueblo. Caimán"*. Es a la vez
    un topónimo y la clave de otro: `yacarebacoa` = *"Pueblo del bosque"*. Si
    no se realimenta, el segundo se queda en residuo opaco.

    Solo se promueven a morfema los topónimos glosados que (a) tienen glosa
    descriptiva, (b) recurren dentro de otro topónimo del corpus. Es el bucle
    criptoanalítico: cada ecuación resuelta da texto plano para la siguiente.
    """
    nuevos = {}
    for e in glosados:
        k = clave(e["forma"])
        g = parte_descriptiva(e["glosa"])
        if len(k) < 4 or not g or k in inv:
            continue
        otros = {f for f, _ in idx.get(k, []) if clave(f) != k}
        if otros:
            nuevos[k] = {"forma": e["forma"], "glosa": g,
                         "origen": f"topónimo glosado ({e['fuente']})",
                         "tipo": "topónimo-morfema", "aparece_en": sorted(otros)}
    inv2 = dict(inv)
    inv2.update(nuevos)
    return inv2, nuevos


def despejar(analisis, inv, idx, glosados):
    """Promueve los residuos de nivel B a morfemas, y devuelve el inventario
    ampliado para una segunda pasada.

    Ejemplo real: `adabacoa` = *"Todo arboleda"* deja el residuo `ada` con
    `bacoa` = 'bosque' ya explicado; el residuo tiene que valer 'árbol'. Con
    `ada` en el inventario, `guadabacoa` = *"Arboleda"* pasa de residuo opaco
    `wada` a `wa-ada-bacoa` — y esa segunda aparición es justamente la
    recurrencia que valida el despeje. El bucle criptoanalítico se cierra.

    Condición para promover: nivel B, residuo ≥3 caracteres, y la glosa deja
    conceptos SIN explicar (si no los deja, el residuo no tiene contenido que
    despejar y sería inventarlo).
    """
    nuevos = {}
    glosa_de = {clave(e["forma"]): e["glosa"] for e in glosados}
    for a in analisis:
        if a["nivel"] != "B" or len(a["residuos"]) != 1:
            continue
        r = a["residuos"][0]
        if len(r) < 3 or r in inv or not a["glosa_por_despejar"]:
            continue
        apoyos = a["recurrencia_residuos"][r]
        cand = nuevos.setdefault(r, {
            "forma": r, "glosa": ", ".join(a["glosa_por_despejar"]),
            "origen": "DESPEJADO por ecuación toponímica",
            "tipo": "despejado", "despejado_en": [], "aparece_en": apoyos})
        cand["despejado_en"].append(a["forma"])
    inv2 = dict(inv)
    inv2.update(nuevos)
    return inv2, nuevos


# ───────────────────────────────────────────────────────────────────────────
# 9. Corroboración del lexicón
# ───────────────────────────────────────────────────────────────────────────

def corroboraciones(analisis, inv):
    """Palabras del lexicón que un topónimo glosado CONFIRMA.

    Confirmar = la forma aparece dentro del topónimo Y su glosa comparte raíz
    con la glosa del topónimo. Es corroboración independiente y barata: alimenta
    el eje FIDELIDAD sin minar una fuente nueva.
    """
    out = defaultdict(list)
    for a in analisis:
        if a["nivel"] == "D":
            continue
        for m in a["alineados"]:
            if inv[m]["tipo"] == "palabra":
                out[m].append(a["forma"])
    return {m: sorted(set(v)) for m, v in sorted(out.items())}


# ───────────────────────────────────────────────────────────────────────────
# 10. Informe
# ───────────────────────────────────────────────────────────────────────────

def informe(analisis, glosados, sin_glosa, inv, idx):
    L = print
    L("=" * 78)
    L("  F11 — DESCOMPOSICIÓN DEL CORPUS TOPONÍMICO Y ANTROPONÍMICO")
    L("=" * 78)
    L(f"\n  Inventario de morfemas conocidos: {len(inv)}")
    L(f"  Topónimos/antropónimos CON glosa (rinden ecuación): {len(glosados)}")
    L(f"  Topónimos SIN glosa (solo control de recurrencia):  {len(sin_glosa)}")

    por_nivel = defaultdict(list)
    for a in analisis:
        por_nivel[a["nivel"]].append(a)
    L("\n  Desglose por nivel:")
    for n in "ABCD":
        L(f"    {n}: {len(por_nivel[n]):3}")

    for n in "ABC":
        if not por_nivel[n]:
            continue
        L("\n" + "─" * 78)
        L(f"  NIVEL {n}")
        L("─" * 78)
        for a in sorted(por_nivel[n], key=lambda x: x["forma"]):
            partes = " + ".join(
                f"{p['seg']}" + (f"({p['glosa'][:24]})" if p["glosa"] else "(?)")
                for p in a["segmentacion"])
            L(f"\n  {a['forma']}  [{a['clase']}, {a['fuente']}]")
            L(f"    glosa : {a['glosa'][:96]}")
            L(f"    segm  : {partes}")
            if a["residuos"]:
                for r in a["residuos"]:
                    rec = a["recurrencia_residuos"][r]
                    L(f"    residuo '{r}' → recurre en {len(rec)}: {', '.join(rec[:6])}")
            if a["reduplicacion"]:
                L(f"    redup : {a['reduplicacion'][0]}")

    L("\n" + "─" * 78)
    L("  NIVEL D (descartes razonados)")
    L("─" * 78)
    for a in sorted(por_nivel["D"], key=lambda x: x["forma"]):
        L(f"  {a['forma']:16} — {a['razon']}")

    corr = corroboraciones(analisis, inv)
    L("\n" + "─" * 78)
    L(f"  CORROBORACIÓN DEL LEXICÓN: {len(corr)} palabras confirmadas por topónimo")
    L("─" * 78)
    for m, tops in corr.items():
        L(f"  {inv[m]['forma']:14} '{inv[m]['glosa'][:38]:40}' ← {', '.join(tops)}")

    L("\n" + "─" * 78)
    L("  MORFEMAS RECURRENTES en los topónimos glosados (≥2 apariciones)")
    L("─" * 78)
    rec = defaultdict(list)
    for a in analisis:
        for p in a.get("segmentacion", []):
            if p["morfema"]:
                rec[p["morfema"]].append(a["forma"])
    for m, fs in sorted(rec.items(), key=lambda kv: -len(kv[1])):
        if len(set(fs)) >= 2:
            L(f"  {inv[m]['forma']:12} '{inv[m]['glosa'][:34]:36}' ×{len(set(fs))}: "
              f"{', '.join(sorted(set(fs)))}")

    L("\n" + "─" * 78)
    L("  REDUPLICACIÓN en todo el corpus (unidad ≥3 caracteres)")
    L("─" * 78)
    todos = sorted({e["forma"] for e in glosados} | {e["forma"] for e in sin_glosa})
    reds = [(f, reduplicacion(f, min_unidad=3)[0])
            for f in todos if reduplicacion(f, min_unidad=3)]
    L(f"  {len(reds)} de {len(todos)} formas ({100*len(reds)//max(1,len(todos))}%)")
    L("  Unidades de <3 caracteres se excluyen: una sílaba repetida en una "
      "palabra\n  de 6 letras es estadística, no morfología.")
    for f, r in reds:
        L(f"    {f:20} {r['tipo']:8} {r['unidad']}")


# ───────────────────────────────────────────────────────────────────────────
# 11. Emisión del módulo de propuesta
# ───────────────────────────────────────────────────────────────────────────

def generar_modulo(analisis, inv, ruta):
    """Escribe el volcado CRUDO del análisis automático.

    ⚠ `lexicon_toponimos.py` es la propuesta CURADA A MANO y no se genera desde
    aquí: el automatismo produce candidatos, no veredictos. Este volcado sirve
    para reproducir y auditar la curación, no para reemplazarla.
    """
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(analisis, f, ensure_ascii=False, indent=2)
    print(f"\n  → volcado crudo: {ruta}")


def main():
    ap = argparse.ArgumentParser(description="F11 — descomposición toponímica")
    ap.add_argument("--json", metavar="RUTA", help="volcar el análisis a JSON")
    ap.add_argument("--generar-modulo", nargs="?", const="toponimos_crudo.json",
                    metavar="RUTA", help="volcado crudo del análisis automático")
    args = ap.parse_args()

    inv = inventario_morfemas()
    glosados, sin_glosa = corpus()
    idx = indice_recurrencia(glosados, sin_glosa)
    inv, promovidos = bootstrap([], inv, idx, glosados)
    analisis = [analizar(e, inv, idx) for e in glosados]
    # 2.ª pasada: los morfemas despejados en la 1.ª entran al inventario
    inv, despejados = despejar(analisis, inv, idx, glosados)
    analisis = [analizar(e, inv, idx) for e in glosados]

    informe(analisis, glosados, sin_glosa, inv, idx)
    print("\n" + "─" * 78)
    print(f"  BOOTSTRAP: {len(promovidos)} topónimos glosados promovidos a morfema")
    print("─" * 78)
    for k, d in sorted(promovidos.items()):
        print(f"  {d['forma']:14} '{d['glosa'][:40]:42}' → {', '.join(d['aparece_en'][:5])}")
    print("\n" + "─" * 78)
    print(f"  MORFEMAS DESPEJADOS en la 1.ª pasada: {len(despejados)}")
    print("─" * 78)
    for k, d in sorted(despejados.items()):
        print(f"  {k:12} ≈ '{d['glosa'][:34]:36}' despejado en "
              f"{', '.join(d['despejado_en'])} · recurre en {', '.join(d['aparece_en'][:6])}")

    if args.generar_modulo:
        ruta = args.generar_modulo
        if not os.path.isabs(ruta):
            ruta = os.path.join(os.path.dirname(__file__), ruta)
        generar_modulo(analisis, inv, ruta)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(analisis, f, ensure_ascii=False, indent=2)
        print(f"\n  → JSON: {args.json}")


if __name__ == "__main__":
    _forzar_utf8()
    main()
