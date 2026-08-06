"""
CURIANA — Minería de van Buurt (2014), *Caquetío words in the Papiamentu language*
==================================================================================

Extrae y clasifica el material léxico de:

    van Buurt, Gerard (2014). "Caquetío Indians on Curaçao during colonial times
    and Caquetío words in the Papiamentu language — Some names of Animals and
    Plants in Papiamentu". Edición propia, Curaçao. ISBN 978-99904-2-348-8.
    Base: van Buurt & Joubert, *Stemmen uit het Verleden* (1997).
    → fuentes_caquetios/VanBuurt_2014_CaquetioWords_Papiamentu.txt

POR QUÉ ESTA FUENTE SE MINA DISTINTO
------------------------------------
Van Buurt **ya construyó la escala epistémica** que este proyecto tuvo que
inventarse: separa la §6 ("words likely to be of Caquetío origin") de la §11
("words with less certain links to Caquetío"). Su §12 explica por qué:

    "Stemmen uit het Verleden did not explicitly state which Amerindian words
    [...] are likely to be original Caquetío words and which ones are likely to
    have been imported via Spanish, Taïno or Guajiro. Since this is to some
    extent a subjective judgment, it was felt that it would be best to present
    the available evidence and let readers draw their own conclusions.
    **This has turned out to be a major mistake, leaving room for totally
    erroneous interpretations.**"

Es decir: la ambigüedad no marcada no es neutral — se lee como afirmación.
**Aplanar §6 y §11 en una sola etiqueta sería repetir el error que el propio
autor confiesa.** Este minador las mantiene separadas de punta a punta.

Y el propio autor advierte de la §6: *"the following listing has a subjective
element"*. Esa subjetividad viaja con el dato: va en `notas` de cada entrada.

POLÍTICA D7 (decidida 2026-08-03)
---------------------------------
Cuando la glosa histórica y la identificación moderna difieren, se registran las
DOS, en campos separados, y ninguna gana:
  · `glosa_fuente`            — lo que dice van Buurt, verbatim, con sección e isla.
  · `identificacion_moderna`  — el taxón actual, si lo da y difiere.
La **marca de isla** (A=Aruba, B=Bonaire, C=Curaçao) se conserva siempre: es
distribución geográfica, y la distribución restringida es criterio positivo del
protocolo `investigacion/disenos/02_protocolo_habla_paraguanera.md` §4.2.

Uso:
    python minar_van_buurt.py                     # informe
    python minar_van_buurt.py --82                # cobertura de las 82 sin cita
    python minar_van_buurt.py --gatschet          # cruce con Gatschet 1885/Pinart 1882
    python minar_van_buurt.py --json out.json
    python minar_van_buurt.py --generar-modulo    # escribe lexicon_van_buurt.py

NO modifica curiana_lexicon.py: emite una propuesta para revisión humana, en la
misma disciplina que minar_zavala_glosario.py y retag_nucleo_fundacional.py.
"""

import argparse
import io
import json
import os
import re
import sys
import unicodedata

# La consola de Windows es cp1252: sin esto el script revienta al imprimir
# "Curaçao", "Taïno" o "chògògò" (es el bug que tiene minar_zavala_glosario.py).
if (hasattr(sys.stdout, "buffer")
        and (getattr(sys.stdout, "encoding", "") or "").lower().replace("-", "") != "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_AQUI = os.path.dirname(os.path.abspath(__file__))
TXT_PATH = os.path.join(
    _AQUI, "..", "fuentes_caquetios", "VanBuurt_2014_CaquetioWords_Papiamentu.txt")
GATSCHET_PATHS = [
    os.path.join(_AQUI, "..", "fuentes_caquetios", "Gatschet_1885_Aruba_texto.txt"),
    os.path.join(_AQUI, "..", "fuentes_caquetios", "Gatschet_1885_biostor_texto.txt"),
]

# ══════════════════════════════════════════════════════════════════════
# Las 82 entradas de familia caquetía del lexicón SIN nota ni cita.
# Auditarlas es la tarea F1 del backlog; este minado es su primer pago.
# ══════════════════════════════════════════════════════════════════════
OCHENTA_Y_DOS = """
amaca apana ateri auyama bajarí barici bariki borojo buco buiamati buko bureche
buriche cachicamo caduchi caraota cari catarí cati cazebo cazi cazicure cazá
chacamba chiriguare chogogo chuchubi corie coro cudan cudanga cumaragua curiana
cuté dare datihao duraboa eroa garabal gua guaitiao guanepe gudamuen güere
güique humocaro iero jacuque jacura jaguey jai kadushi kama koke kukuisa kunuku
maure mazato mene na pariri paro pauji piache poporo quidi rao sabuenen saruro
sawaka tabri tara tarica tata tebe tuqueque ture ucibo urapa wabarsure warawara
watapana
""".split()

# Lemas de más de una palabra: no se parten por espacios al despiezar el lema.
MULTIPALABRA = {
    "kadushi pushi", "kiwa karate", "kiwa karati", "dori maco", "kasha kutu",
    "yaga dabaruida", "breba di pushi",
}

# ══════════════════════════════════════════════════════════════════════
# RESERVAS DEL PROPIO AUTOR — el techo del veredicto baja a C
# ══════════════════════════════════════════════════════════════════════
# Van Buurt pone estas tres en la §6 pero, dentro de la propia entrada,
# desmonta su atribución caquetía. Respetar la sección e ignorar el cuerpo
# sería quedarse con la etiqueta y tirar el argumento.
RESERVAS_DEL_AUTOR = {
    "wayaca": "el propio autor: «makes one suspect that wayaká could be an "
              "imported Taíno word»; cierra la entrada diciendo que ilustra la "
              "dificultad de decidir",
    "wimpiri": "el propio autor: «it thus seems less likely that the form Wimpiri "
               "is of Caquetío origin» — lo deriva de Karina mapili / mapiri",
    "shirishiri": "el propio autor: «There is no proof this is an Indian word. It "
                  "has been suggested it came from Africa»",
}

# Entradas de la §6 que son remisiones cruzadas, no entradas independientes.
_RE_REMISION = re.compile(r"^\s*see\b", re.IGNORECASE)

# Atestación colonial o recolección decimonónica independiente dentro de la
# entrada. Deliberadamente NO incluye a Taylor (1958/1977) ni a Versteeg &
# Rostain (1997): el primero es comparatismo del s. XX y el segundo es
# arqueología de fauna. Ninguno de los dos atestigua la PALABRA.
_RE_ATESTACION = re.compile(
    r"Relaci[óo]n de Nueva Segovia|\b1579\b|Oviedo|Las Casas|Federmann|Barbudo|"
    r"cronistas|Teenstra|van Koolwijk|Pinart|\b1880\b|\b1890\b",
    re.IGNORECASE)

# Lenguas hermanas / de contacto citadas: se registran como paralelo comparativo.
_LENGUAS = {
    "Guajiro": r"Guajiro|Wayúu|Wayu\b",
    "Taíno": r"Ta[íï]no",
    "Lokono": r"Lokono",
    "Island Carib (Kalinago)": r"Island Carib|Kallinago|Kalinago",
    "Shebayo": r"Shebayo",
    "Paraujano (Añú)": r"Paraujano",
    "Cumanagoto": r"Cumanagoto",
    "Chaima": r"Chaima",
    "Karina": r"Karina",
}

# Filtro 4 del protocolo: forma también corriente en tierra firme / español.
_RE_DISTRIB_AMPLIA = re.compile(
    r"in Venezuela it is called|found in Venezuela|also used in Spanish|"
    r"on the Spanish mainland|found in Spanish|also found in Cuba|"
    r"mainland form|in Paraguan[áa] it is called", re.IGNORECASE)

# ── Nombre científico (política D7: campo separado de la glosa) ──
# Casi toda la §6 lo da entre paréntesis: ese caso es de alta precisión.
_BINOMIO = (r"[A-Z][a-z]{2,}\s+(?:spp\.|[a-z][a-z-]{2,})"
            r"(?:\s+(?:syn\.|subsp\.)\s+[A-Z]?[a-z]+(?:\s+[a-z]+)?|\s+[a-z][a-z-]{2,})?")
_RE_TAXON_PAR = re.compile(rf"\(\s*({_BINOMIO})\s*\)")
_RE_TAXON_LIBRE = re.compile(rf"\b({_BINOMIO})")
# El fallback sin paréntesis confunde inicio de frase con género ("Along the",
# "These are"). Se filtra por la primera palabra.
_NO_ES_GENERO = {
    "the", "this", "these", "those", "in", "it", "along", "since", "nowadays",
    "compare", "see", "melon", "turk", "sea", "general", "small", "large",
    "aruba", "curacao", "bonaire", "venezuela", "guajiro", "lokono", "taino",
    "spanish", "papiamentu", "papiamento", "indian", "west", "another",
    "colombian", "there", "such", "during", "from", "many", "some", "when",
    "originally", "here", "according", "although", "unlike", "nor", "and",
    "abou", "banda", "obviously", "every", "its", "at", "on", "one", "he",
    "arawak", "waka", "young", "venezuelan", "colombia", "nerita", "anolis",
    "drosophila",
}
# El epíteto tiene que parecer latín: si es una palabra inglesa, el "binomio"
# era en realidad un género suelto seguido de prosa ("Anolis lizard").
_NO_ES_EPITETO = {
    "lizard", "lizards", "snail", "snails", "language", "languages", "plaga",
    "underground", "recorded", "fish", "fishes", "flies", "fly", "means",
    "tree", "trees", "cactus", "area", "shell", "shells", "word", "words",
    "name", "names", "grouper", "frog", "bird", "birds", "plant", "plants",
    "region", "salted", "sea", "and", "the", "this", "that", "with", "was",
}
# Un taxón que aparece muy metido en la entrada suele ser una comparación, no
# la identificación del lema (p. ej. el algodón silvestre citado bajo `waíki`).
_TAXON_MAX_POS = 160

_RE_ISLAS = re.compile(r"\(\s*([ABC](?:\s*,\s*[ABC])*)\s*\)")
_RE_FOTO = re.compile(r"\(\s*(P\d+(?:\+\d+)?)\s*\)")


def norm(s: str) -> str:
    """minúsculas sin acentos ni diacríticos, para comparar formas."""
    s = (s or "").lower().strip()
    s = s.replace("ç", "c").replace("ñ", "n")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _limpiar(t: str) -> str:
    return " ".join(t.replace("’", "'").split()).strip()


# ══════════════════════════════════════════════════════════════════════
# Parseo
# ══════════════════════════════════════════════════════════════════════

def leer(path: str = TXT_PATH) -> list[str]:
    if not os.path.exists(path):
        sys.exit(f"No encuentro la fuente: {path}\n"
                 "Debe estar en la RAÍZ del proyecto (pendiente de higiene: "
                 "moverla a fuentes_caquetios/).")
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def secciones(lineas: list[str]) -> dict[int, tuple[int, int]]:
    """Localiza las 12 secciones numeradas. Devuelve {num: (ini, fin)}."""
    marcas = []
    for i, l in enumerate(lineas):
        m = re.match(r"^\s*([0-9]{1,2})\. [A-Z]", l)
        if m:
            n = int(m.group(1))
            if not marcas or n == marcas[-1][0] + 1:      # secuencia estricta
                marcas.append((n, i))
    out = {}
    for k, (n, i) in enumerate(marcas):
        fin = marcas[k + 1][1] if k + 1 < len(marcas) else len(lineas)
        out[n] = (i, fin)
    return out


def _bloques(lineas: list[str], ini: int, fin: int) -> list[list[str]]:
    """Agrupa cada entrada con sus líneas de continuación (indentadas).

    Tres entradas (`dori`, `kadushi`, `yuchi`) llevan intercalado un bloque a
    columna 0 que NO es una entrada: la rima de Aruba, la cita de la Relación de
    Nueva Segovia (1579) y el párrafo de cierre de la sección. Al toparse con
    prosa se CIERRA la entrada en curso en vez de descartarla, y las líneas
    indentadas que vengan después se reenganchan a ella (es su cola).
    """
    bloques, actual, ultimo = [], None, None
    for l in lineas[ini:fin]:
        if l.startswith("Opmaak") or re.match(r"^\s*\d{1,3}\s*$", l):
            continue                                     # pie de página / folio
        if l[:1] not in (" ", ""):                       # línea a columna 0
            m = re.match(r"^(.{1,90}?)\s+[-–]\s+(.+)$", l)
            if m and l[:1].islower():
                if actual:
                    bloques.append(actual)
                actual = ultimo = [l]
                continue
            if actual:                                   # prosa: cierra, no descarta
                bloques.append(actual)
                ultimo = actual
            actual = None
        elif actual is not None:
            actual.append(l)
        elif ultimo is not None:
            ultimo.append(l)                             # cola tras la prosa
    if actual:
        bloques.append(actual)
    return bloques


def _taxon(definicion: str) -> str | None:
    """Identificación moderna (política D7). Paréntesis primero: alta precisión."""
    def _ok(m):
        if m.start() > _TAXON_MAX_POS:
            return None
        pal = _limpiar(m.group(1)).split()
        while pal and pal[-1].lower().rstrip(".") in ("and", "syn", "or", "the"):
            pal.pop()
        if len(pal) < 2 or pal[0].lower() in _NO_ES_GENERO:
            return None
        if pal[1].lower() in _NO_ES_EPITETO:
            return None
        return " ".join(pal)

    for rx in (_RE_TAXON_PAR, _RE_TAXON_LIBRE):
        for m in rx.finditer(definicion):
            t = _ok(m)
            if t:
                return t
    return None


def _despiezar_lema(head: str) -> list[str]:
    """'karawara (C), carawara, cawara (A) koahara, koahari (B)' → 6 formas."""
    h = re.sub(r"\((?:[^()]*)\)", " ", head)             # fuera islas y (Pn)
    formas = []
    for trozo in re.split(r"[,;]", h):
        trozo = trozo.strip()
        if not trozo:
            continue
        # 'wayaca [wayacá]' → dos formas; la NO abreviada va primero (es el lema)
        entre_corchetes = [_limpiar(b) for b in re.findall(r"\[([^\]]+)\]", trozo)]
        trozo = _limpiar(re.sub(r"\[[^\]]*\]", " ", trozo))
        if trozo:
            if trozo.lower() in MULTIPALABRA or " " not in trozo:
                formas.append(trozo)
            else:                                        # coma que falta en el original
                formas.extend(p for p in trozo.split() if len(p) > 1)
        formas.extend(entre_corchetes)
    vistas, out = set(), []
    for f in formas:
        if norm(f) not in vistas and len(f) > 1:
            vistas.add(norm(f))
            out.append(f)
    return out


def extraer_glosario(lineas: list[str], ini: int, fin: int, seccion: int) -> list[dict]:
    entradas = []
    for bloque in _bloques(lineas, ini, fin):
        crudo = _limpiar(" ".join(bloque))
        m = re.match(r"^(.{1,90}?)\s+[-–]\s+(.+)$", crudo)
        if not m:
            continue
        head, definicion = m.group(1), _limpiar(m.group(2))
        # 'totèki - (C,B) Anolis lizard': la marca de isla va tras el guion.
        islas = sorted({c for g in _RE_ISLAS.findall(head + " " + definicion[:14])
                        for c in re.findall(r"[ABC]", g)})
        foto = (_RE_FOTO.search(head) or [None])
        foto = foto.group(1) if hasattr(foto, "group") else None
        formas = _despiezar_lema(head)
        if not formas:
            continue
        taxon = _taxon(definicion)
        entradas.append({
            "seccion": seccion,
            "formas": formas,
            "lema": formas[0],
            "islas": islas,
            "foto": foto,
            "glosa_fuente": definicion,
            "identificacion_moderna": taxon,
            "remision": bool(_RE_REMISION.match(definicion)),
        })
    return entradas


def extraer_toponimos(lineas: list[str], ini: int, fin: int) -> dict[str, list[dict]]:
    """§7: tres bloques (Aruba / Curaçao / Bonaire), un topónimo por línea."""
    isla, out = None, {"Aruba": [], "Curaçao": [], "Bonaire": []}
    for l in lineas[ini:fin]:
        s = l.strip()
        if s in ("Aruba", "Curaçao", "Bonaire"):
            isla = s
            continue
        if isla is None or not s or s.startswith("Opmaak") or re.match(r"^\d{1,3}$", s):
            continue
        if len(s) > 46 or s[:1].islower():               # prosa introductoria
            continue
        generico = re.findall(r"\(([^)]*)\)", s)
        dudoso = s.endswith("?")
        nombre = _limpiar(re.sub(r"\([^)]*\)", " ", s).rstrip("?"))
        if not nombre or not re.match(r"^[A-Z]", nombre):
            continue
        out[isla].append({
            "toponimo": nombre,
            "variantes": [_limpiar(v) for v in nombre.split(",")][1:],
            "generico": ", ".join(generico) or None,     # Seru, Rooi, Boca, Cueba…
            "dudoso": dudoso,
        })
    return out


def extraer_comentarios(lineas: list[str], secs: dict) -> dict[str, str]:
    """§8-10: etimología comentada de topónimos concretos."""
    out = {}
    for n in (8, 9, 10):
        if n not in secs:
            continue
        for bloque in _bloques_toponimo(lineas, *secs[n]):
            crudo = _limpiar(" ".join(bloque))
            m = re.match(r"^(.{1,60}?)\s+[-–]\s+(.+)$", crudo)
            if m:
                out[_limpiar(m.group(1))] = _limpiar(m.group(2))
    return out


def _bloques_toponimo(lineas, ini, fin):
    """Como _bloques pero los lemas de §8-10 empiezan en MAYÚSCULA."""
    bloques, actual = [], None
    for l in lineas[ini:fin]:
        if l.startswith("Opmaak") or re.match(r"^\s*\d{1,3}\s*$", l):
            continue
        if l[:1] not in (" ", ""):
            m = re.match(r"^([A-ZÁÉÍÓÚ].{0,60}?)\s+[-–]\s+(.+)$", l)
            if m:
                if actual:
                    bloques.append(actual)
                actual = [l]
                continue
            actual = None
        elif actual is not None:
            actual.append(l)
    if actual:
        bloques.append(actual)
    return bloques


# ══════════════════════════════════════════════════════════════════════
# MORFEMAS — el otro pago de esta fuente
# ══════════════════════════════════════════════════════════════════════
# Van Buurt hace análisis morfológico explícito en §5 y §8-10. Estos morfemas
# NO se extraen por regex (van en prosa argumentada): se transcriben a mano con
# la glosa y la autoridad que él cita, para que sean auditables uno por uno.
# `-ima` confirma de forma INDEPENDIENTE el afijo homónimo de REGLAS_ZAVALA.
MORFEMAS_VAN_BUURT: dict[str, dict] = {
    "-ima": {"glosa": "húmedo, mojado", "forma_alt": "nima",
             "autoridad": "Cruz Esteves 1989, vía van Buurt §10 (topónimo Onima, Bonaire)",
             "nota": "confirma de forma independiente el afijo -ima de REGLAS_ZAVALA "
                     "(Zavala 2015: 'humedad, quebrada')"},
    "-ure": {"glosa": "raíz", "forma_alt": "-huri, -uri",
             "autoridad": "Cruz Esteves 1989, vía van Buurt §5",
             "nota": "van Buurt: papiamento -huri/-uri equivale al -ure caquetío de "
                     "tierra firme; hurihuri, karishuri, marihuri tienen raíz usada"},
    "-bana": {"glosa": "ancho, llano; también 'cubierto'", "forma_alt": "bana",
              "autoridad": "van Buurt §8 (Hudishibana) y §6 (sawaka/wakubana, vía Oliver)",
              "nota": "el lexicón ya usa -bana como locativo 'orilla/borde': van Buurt "
                      "documenta 'llano' y 'cubierto'. Discrepancia a resolver."},
    "-apana": {"glosa": "hoja, estructura plana como una hoja", "forma_alt": "-pana",
               "autoridad": "van Buurt §5 y §6 (watapana), de Goeje 1928",
               "nota": "watapana ≈ 'tiene muchas hojas (pequeñas)'"},
    "-bi": {"glosa": "pequeño (diminutivo)", "forma_alt": "-bí",
            "autoridad": "van Buurt §6 (gobí, gogorobí, kokorobí, lobi, makambí)",
            "nota": "segundo diminutivo documentado, junto al -iro de REGLAS_ZAVALA"},
    "wa-": {"glosa": "prefijo de pluralidad y de posesión ('tener')", "forma_alt": "wu-",
            "autoridad": "de Goeje 1928, vía van Buurt §6 (watapana, wampanaria)",
            "nota": None},
    "ka-": {"glosa": "localizador: 'hay', 'existe(n)'", "forma_alt": "ca-",
            "autoridad": "van Buurt §8 (Casibari)", "nota": None},
    "-ato": {"glosa": "indica relación de parentesco", "forma_alt": None,
             "autoridad": "Oliver 1989, vía van Buurt §6 (dato = 'hija del yato')",
             "nota": None},
    "-baca": {"glosa": "grupo, matorral, espesura", "forma_alt": "-bacu",
              "autoridad": "Alvarado 1921, vía van Buurt §10 (Yatu Bacu)",
              "nota": "enlaza con la hoja de fuente alvarado-1921"},
    "-utu": {"glosa": "pez (raíz común a muchas lenguas arahuacas)", "forma_alt": None,
             "autoridad": "van Buurt §6 (gutu, kasha kutu; topónimo Manparia Cutu)",
             "nota": "van Buurt: la alternancia k/g es frecuente"},
    "bara": {"glosa": "árbol", "forma_alt": "bari, -bari",
             "autoridad": "van Buurt §5; cf. Lokono balli",
             "nota": "explica kalabari, mashibari, stanibari, tarabara"},
    "bala": {"glosa": "el mar", "forma_alt": None,
             "autoridad": "van Buurt §8 (Balashi, Aruba)", "nota": None},
    "cari": {"glosa": "costa, orilla", "forma_alt": "kari",
             "autoridad": "Cruz Esteves 1989, vía van Buurt §9 (Cariatávo)",
             "nota": "⚠ el lexicón tiene 'cari' sin cita: ver cobertura de las 82"},
    "abo": {"glosa": "lugar", "forma_alt": None,
            "autoridad": "van Buurt §9 (Cariatávo)", "nota": None},
    "tabo": {"glosa": "bifurcación de árbol o de río; confluencia", "forma_alt": None,
             "autoridad": "van Buurt §9 (Cariatávo)", "nota": None},
    "siba": {"glosa": "piedra, roca", "forma_alt": "quiba",
             "autoridad": "van Buurt §8 (Casibari; y el nombre de la isla de Saba)",
             "nota": None},
    "rí": {"glosa": "fuerte, duro, durable", "forma_alt": "-ri",
           "autoridad": "van Buurt §8 (Casibari = 'hay rocas duras')", "nota": None},
    "hudi": {"glosa": "viento", "forma_alt": "juri, judi",
             "autoridad": "Cruz Esteves 1989, vía van Buurt §8 (Hudishibana = 'llano ventoso')",
             "nota": None},
    "waka": {"glosa": "subterráneo, bajo tierra", "forma_alt": "guaca",
             "autoridad": "van Buurt §6 (sawaka, wakaubana vía Oliver 1989)",
             "nota": "sostiene 'sawaka' = inframundo, una de las 82 sin cita"},
}


# ══════════════════════════════════════════════════════════════════════
# Clasificación
# ══════════════════════════════════════════════════════════════════════

def _tokens_gatschet() -> tuple[set[str], dict[str, str]]:
    """Vocabulario de Gatschet 1885 (material de Pinart 1882), para candidatos."""
    toks, evid = set(), {}
    for p in GATSCHET_PATHS:
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as f:
            for linea in f:
                for t in re.findall(r"[A-Za-zÀ-ÿ]{3,}", linea):
                    n = norm(t)
                    toks.add(n)
                    evid.setdefault(n, _limpiar(linea)[:150])
    return toks, evid


def _clave_orto(x: str) -> str:
    """Normaliza las diferencias ortográficas entre Pinart 1882 y el papiamento
    moderno: c/k/qu, ch/sh/sj/sk, z/s, y vocal final inestable."""
    x = norm(x)
    for a, b in (("sj", "sh"), ("ch", "sh"), ("sk", "sh"), ("qu", "k"),
                 ("c", "k"), ("q", "k"), ("z", "s")):
        x = x.replace(a, b)
    return re.sub(r"[aeiou]$", "", x)


def candidatos_gatschet(entradas: list[dict], toks: set[str]) -> list[tuple]:
    """Genera candidatos van Buurt × Gatschet por clave ortográfica + similitud.

    Es un GENERADOR DE HIPÓTESIS, no un resultado: produce falsos positivos
    (`kiberi`~«quiere», `shoco`~«Choco» —una región de Colombia—). La tabla que
    vale es COINCIDENCIAS_GATSCHET, curada a mano leyendo el texto de Gatschet.
    """
    import difflib
    idx: dict[str, set[str]] = {}
    for t in toks:
        if len(t) >= 5:
            idx.setdefault(_clave_orto(t), set()).add(t)
    out = []
    for e in entradas:
        for f in e["formas"]:
            k = _clave_orto(f)
            if len(k) < 4:
                continue
            if k in idx:
                out += [(e["lema"], f, g, "exacta") for g in sorted(idx[k])]
            else:
                for k2, gs in idx.items():
                    if k2[:2] == k[:2] and difflib.SequenceMatcher(None, k, k2).ratio() >= 0.84:
                        out += [(e["lema"], f, g, "aprox") for g in sorted(gs)]
    return out


# ══════════════════════════════════════════════════════════════════════
# CRUCE CON GATSCHET 1885 (material recogido por Pinart en Aruba, 1882)
# ══════════════════════════════════════════════════════════════════════
# Dos recolecciones INDEPENDIENTES separadas por 130 años. Donde coinciden, la
# confianza sube mucho: no es una fuente citando a la otra.
#
# Tabla curada a mano a partir de `--gatschet-candidatos` + lectura del texto de
# Gatschet (pp. 302-303 del artículo: listas de árboles, plantas, peces, aves e
# «insects and other animals»). Cada glosa es la de Gatschet, verbatim, con su
# OCR: hay erratas evidentes («Oereus» = Cereus, «Oathartes» = Cathartes).
COINCIDENCIAS_GATSCHET: dict[str, dict] = {
    "dividivi":   {"gatschet": "dividivi",  "tipo": "exacta",
                   "glosa_gatschet": "fruit of Sapindus coriaria"},
    "kadushi":    {"gatschet": "kaduski",   "tipo": "variante ortográfica",
                   "glosa_gatschet": "Oereus laniginosus [= Cereus lanuginosus]",
                   "nota": "⚠ D7: el taxón de Gatschet (Cereus lanuginosus) es el que "
                           "van Buurt asigna al kadushi PUSHI (Pilosocereus lanuginosus), "
                           "no al kadushi (Cereus repandus). Discrepancia de identificación."},
    "makurá":     {"gatschet": "makura",    "tipo": "exacta",
                   "glosa_gatschet": "Abrus precatorius",
                   "nota": "mismo taxón en las dos fuentes"},
    "shimarucu":  {"gatschet": "shimaruko", "tipo": "variante ortográfica",
                   "glosa_gatschet": "Malpighia glabra",
                   "nota": "Malpighia glabra ~ M. emarginata (sinonimia histórica)"},
    "watapana":   {"gatschet": "watapana",  "tipo": "exacta",
                   "glosa_gatschet": "Sapindus coriaria [= Caesalpinia coriaria]"},
    "dabaruida":  {"gatschet": "dabaraida", "tipo": "variante ortográfica",
                   "glosa_gatschet": "(en «Names of Aruban trees»)",
                   "nota": "el propio van Buurt cita esta coincidencia: «The Pinart "
                           "wordlist from 1890 gives dabaraida»"},
    "hubada":     {"gatschet": "hubada",    "tipo": "exacta",
                   "glosa_gatschet": "(en «Names of Aruban trees»)"},
    "tarabara":   {"gatschet": "tarabada",  "tipo": "variante ortográfica (probable)",
                   "glosa_gatschet": "(en «Names of Aruban trees»)",
                   "nota": "d/r es alternancia frecuente en el OCR y en la transcripción "
                           "de Pinart; ojo con no confundirlo con el monte Tarabana"},
    "warawara":   {"gatschet": "warawara",  "tipo": "exacta",
                   "glosa_gatschet": "Oathartes curasoica [= Cathartes curasoica]",
                   "nota": "⚠ D7: Gatschet lo identifica como zamuro (Cathartes); van "
                           "Buurt, como caracara (Caracara cheriway). El lexicón trae "
                           "hoy la lectura de Gatschet, sin saberlo"},
    "chuchubi":   {"gatschet": "shushubi",  "tipo": "variante ortográfica",
                   "glosa_gatschet": "Orpheus amerieanus [= Mimus, sinsonte]"},
    "dori":       {"gatschet": "dori",      "tipo": "exacta",
                   "glosa_gatschet": "Rana ( — ?)"},
    "palúli":     {"gatschet": "paluli",    "tipo": "exacta",
                   "glosa_gatschet": "Mytilus edulis",
                   "nota": "mejillón en las dos fuentes; van Buurt precisa "
                           "Brachidontes exustus"},
    "waltaca":    {"gatschet": "waltaka",   "tipo": "variante ortográfica",
                   "glosa_gatschet": "lizard"},
    "koubati":    {"gatschet": "Kausheati", "tipo": "variante ortográfica",
                   "glosa_gatschet": "(en «Names of Aruban places»)",
                   "nota": "coincidencia a nivel de TOPÓNIMO: van Buurt trae caushati/"
                           "coushati como variantes arubanas del árbol y Caushati (Sero) "
                           "como topónimo"},
    # ── las dos que caen en la §11 (tier degradado) ──
    "purunchi":   {"gatschet": "puruntsi",  "tipo": "variante ortográfica",
                   "glosa_gatschet": "Serranus variolosus [un mero]",
                   "nota": "el propio van Buurt la cita («Pinart (1890) mentions the name "
                           "purantsi») Y es justo el sitio donde dice que esa lista "
                           "«contains several words which are definitely not Indian»"},
    "kinikini":   {"gatschet": "kinikini",  "tipo": "exacta",
                   "glosa_gatschet": "Cymindes illigeri [un falcónido]"},
}

# Candidatos generados por `--gatschet-candidatos` y DESCARTADOS al leer el
# texto. Documentar el descarte evita que alguien los re-descubra en seis meses.
DESCARTES_GATSCHET: dict[str, str] = {
    "shoco ~ Choco": "«Choco» aparece solo en «Prayer to Christ in the Sambu dialect "
                     "of Choco, Columbian States»: es una región de Colombia, no una "
                     "palabra arubana",
    "kiberi ~ quiere": "«quiere» es castellano, de la parte del artículo sobre el "
                       "papiamento",
    "katana ~ catjan": "«catjan» es el epíteto latino de Cytisus catjan, la planta que "
                       "Gatschet llama nandu",
    "makuaku ~ macacu": "«mono macacu» está en la lista de papiamento de Gatschet, no "
                        "en el vocabulario arubano",
    "warwarú ~ warawara": "warawara ya cruza consigo mismo; el parecido con warwarú es "
                          "casual",
}


def clasificar(entradas: list[dict], toponimos: dict) -> list[dict]:
    """Añade veredicto y señales del protocolo a cada entrada."""
    from curiana_lexicon import VOCABULARIO_BASE
    from curiana_database import normalize_source_language

    lex = {norm(w): (w, normalize_source_language(e.get("fuente", "")), e.get("sig", ""))
           for w, e in VOCABULARIO_BASE.items()}
    topo = {norm(t["toponimo"].split(",")[0]) for isla in toponimos.values() for t in isla}

    for e in entradas:
        n = [norm(f) for f in e["formas"]]
        txt = e["glosa_fuente"]

        e["paralelos"] = [k for k, rx in _LENGUAS.items() if re.search(rx, txt)]
        e["atestacion_colonial"] = bool(_RE_ATESTACION.search(txt))
        e["distribucion_amplia"] = bool(_RE_DISTRIB_AMPLIA.search(txt))
        e["gatschet"] = COINCIDENCIAS_GATSCHET.get(e["lema"])
        e["en_gatschet"] = [e["gatschet"]["gatschet"]] if e["gatschet"] else []
        # respaldo toponímico: la forma es o contiene un topónimo de §7
        # Criterio positivo 5 del protocolo (los topónimos son el reservorio más
        # fiable de sustrato). Coincidencia exacta o de RAÍZ INICIAL entre formas
        # de ≥5 letras: la inclusión libre daba falsos positivos (`ishiri` dentro
        # de `shirishiri`, `bushi` dentro de `Tibushi`).
        # La /w-/ protética alterna con vocal inicial en esta lengua: van Buurt
        # argumenta en §8 que el topónimo Arashi es el singular de warashi.
        def _empareja(t: str, x: str) -> bool:
            if t == x or "w" + t == x or t == "w" + x:
                return True
            return (len(t) >= 5 and len(x) >= 5
                    and (t.startswith(x) or x.startswith(t)))

        e["respaldo_toponimico"] = sorted(
            {t for t in topo for x in n if _empareja(t, x)})
        hit = next(((f, *lex[x]) for f, x in zip(e["formas"], n) if x in lex), None)
        e["en_lexicon"] = None
        if hit:
            e["en_lexicon"] = {"forma_van_buurt": hit[0], "forma_lexicon": hit[1],
                               "fuente_actual": hit[2], "sig_lexicon": hit[3]}
        e["reserva_autor"] = next((RESERVAS_DEL_AUTOR[x] for x in n
                                   if x in RESERVAS_DEL_AUTOR), None)

        # ── veredicto (escala del protocolo §5) ──
        if e["remision"]:
            e["veredicto"], e["razon"] = "REMISION", "remisión cruzada, no entrada propia"
        elif e["reserva_autor"]:
            e["veredicto"] = "C_plausible"
            e["razon"] = "en §6, pero el autor desmonta la atribución en la propia entrada"
        elif e["seccion"] == 11:
            e["veredicto"] = "C_plausible"
            e["razon"] = "§11 — «words with less certain links to Caquetío» (van Buurt)"
        elif e["atestacion_colonial"] or e["en_gatschet"] or e["respaldo_toponimico"]:
            e["veredicto"] = "A_atestiguado"
            e["razon"] = "§6 + " + " + ".join(filter(None, [
                "atestación colonial/decimonónica" if e["atestacion_colonial"] else "",
                f"coincide con Gatschet 1885/Pinart 1882 ({e['en_gatschet'][0]})" if e["en_gatschet"] else "",
                f"respaldo toponímico (§7: {', '.join(e['respaldo_toponimico'])})" if e["respaldo_toponimico"] else "",
            ]))
        else:
            e["veredicto"] = "B_fuerte"
            e["razon"] = "§6 — «likely to be of Caquetío origin», sin respaldo externo adicional"
        if e["distribucion_amplia"] and e["veredicto"] == "A_atestiguado":
            e["razon"] += " ⚠ pero forma también corriente en tierra firme (filtro 4 del protocolo)"

    # Formas que van Buurt lista en LAS DOS secciones: se contradice a sí mismo.
    por_seccion = {}
    for e in entradas:
        for f in e["formas"]:
            por_seccion.setdefault(norm(f), set()).add(e["seccion"])
    for e in entradas:
        e["duplicada_en_ambas_secciones"] = any(
            len(por_seccion[norm(f)]) > 1 for f in e["formas"])
    return entradas


def cobertura_82(entradas: list[dict], toponimos: dict, lineas: list[str]) -> list[dict]:
    """¿Qué de las 82 entradas sin cita aparece en van Buurt, y con qué estatus?"""
    por_forma = {}
    for e in entradas:
        for f in e["formas"]:
            por_forma.setdefault(norm(f), e)
    topo = {}
    for isla, items in toponimos.items():
        for t in items:
            topo.setdefault(norm(t["toponimo"].split(",")[0]), (t["toponimo"], isla))
    plano = [(i, _limpiar(l)) for i, l in enumerate(lineas) if l.strip()]

    out = []
    for w in OCHENTA_Y_DOS:
        nw = norm(w)
        reg = {"palabra": w, "donde": "no", "cita": None, "veredicto": None}
        if nw in por_forma:
            e = por_forma[nw]
            reg["donde"] = f"§{e['seccion']} entrada"
            reg["cita"] = (f"van Buurt 2014 §{e['seccion']} s.v. {e['lema']}"
                           f"{' (' + ','.join(e['islas']) + ')' if e['islas'] else ''}: "
                           f"{e['glosa_fuente'][:90]}")
            reg["seccion"] = e["seccion"]
            reg["veredicto"] = ("CITA DISPONIBLE — §6 «likely Caquetío»" if e["seccion"] == 6
                                else "⚠ RECLASIFICADA HACIA ABAJO — van Buurt la pone en §11 "
                                     "(«less certain links to Caquetío»)")
        elif nw in topo:
            reg["donde"] = "§7 topónimo"
            reg["cita"] = f"van Buurt 2014 §7, topónimo {topo[nw][0]} ({topo[nw][1]})"
            reg["veredicto"] = "respaldo toponímico, no entrada léxica"
        else:
            rx = re.compile(rf"\b{re.escape(nw)}\b", re.IGNORECASE)
            ev = [l for _, l in plano if rx.search(norm(l))][:2]
            if ev:
                reg["donde"] = "mención en prosa"
                reg["cita"] = " / ".join(x[:110] for x in ev)
                reg["veredicto"] = "mención en prosa — revisar si es respaldo léxico"
            else:
                reg["veredicto"] = "sin rastro en van Buurt 2014"
        out.append(reg)
    return out


# ══════════════════════════════════════════════════════════════════════
# Salidas
# ══════════════════════════════════════════════════════════════════════

def informe(entradas, toponimos, comentarios, cobertura):
    s6 = [e for e in entradas if e["seccion"] == 6]
    s11 = [e for e in entradas if e["seccion"] == 11]
    print("=" * 78)
    print("  VAN BUURT 2014 — auditoría de importación (F6)")
    print("=" * 78)
    print(f"  §6  palabras «likely of Caquetío origin»: {len(s6)}")
    print(f"  §11 palabras «with less certain links»  : {len(s11)}")
    print(f"  §7  topónimos: {sum(len(v) for v in toponimos.values())}"
          f"  (A={len(toponimos['Aruba'])} C={len(toponimos['Curaçao'])} "
          f"B={len(toponimos['Bonaire'])})")
    print(f"  §8-10 topónimos con etimología comentada: {len(comentarios)}")
    print(f"  morfemas transcritos a mano de §5/§8-10: {len(MORFEMAS_VAN_BUURT)}")
    print()
    for v in ("A_atestiguado", "B_fuerte", "C_plausible", "REMISION"):
        items = [e for e in entradas if e["veredicto"] == v]
        print(f"── {v}: {len(items)}")
        for e in items[:8]:
            isl = ",".join(e["islas"]) or "-"
            print(f"     {e['lema']:16} ({isl:5}) §{e['seccion']}  "
                  f"{(e['identificacion_moderna'] or e['glosa_fuente'])[:46]}")
        if len(items) > 8:
            print(f"     … y {len(items)-8} más")
        print()

    ya = [e for e in entradas if e["en_lexicon"]]
    print(f"  ya en VOCABULARIO_BASE: {len(ya)}")
    degradadas = [e for e in ya if e["seccion"] == 11 or e["reserva_autor"]]
    if degradadas:
        print(f"\n  ⚠ EN EL LEXICÓN, pero van Buurt las degrada ({len(degradadas)}):")
        for e in degradadas:
            print(f"     {e['lema']:14} lexicón='{e['en_lexicon']['forma_lexicon']}' "
                  f"({e['en_lexicon']['fuente_actual']}) → §{e['seccion']} "
                  f"{'· reserva del autor' if e['reserva_autor'] else ''}")
    dup = sorted({e["lema"] for e in entradas if e["duplicada_en_ambas_secciones"]})
    if dup:
        print(f"\n  ⚠ listadas por van Buurt en §6 Y en §11 ({len(dup)}): {', '.join(dup)}")
    g = [e for e in entradas if e["en_gatschet"]]
    print(f"\n  coincidencias con Gatschet 1885 / Pinart 1882: {len(g)}")
    print("     " + ", ".join(e["lema"] for e in g))
    res = {}
    for r in cobertura:
        res[r["donde"]] = res.get(r["donde"], 0) + 1
    print(f"\n  cobertura de las 82 sin cita: " +
          ", ".join(f"{k}={v}" for k, v in sorted(res.items())))


def informe_82(cobertura):
    print("=" * 78)
    print("  COBERTURA DE LAS 82 ENTRADAS SIN CITA")
    print("=" * 78)
    for r in cobertura:
        print(f"{r['palabra']:14} {r['donde']:18} {r['veredicto'] or ''}")
        if r["cita"]:
            print(f"               ↳ {r['cita'][:150]}")


def informe_gatschet(entradas):
    print("=" * 78)
    print("  CRUCE VAN BUURT 2014 × GATSCHET 1885 (material de Pinart, 1882)")
    print("=" * 78)
    print("  Dos recolecciones INDEPENDIENTES separadas por 130 años.")
    print()
    for e in entradas:
        g = e.get("gatschet")
        if not g:
            continue
        print(f"  {e['lema']:12} §{e['seccion']:<2} ({','.join(e['islas']) or '-':5}) "
              f"↔ Gatschet «{g['gatschet']}» [{g['tipo']}]")
        print(f"      van Buurt: {(e['identificacion_moderna'] or e['glosa_fuente'])[:62]}")
        print(f"      Gatschet : {g['glosa_gatschet'][:62]}")
        if g.get("nota"):
            print(f"      ⚠ {g['nota'][:150]}")
        print()
    print(f"  coincidencias verificadas: {len(COINCIDENCIAS_GATSCHET)}"
          f"  (§6: {sum(1 for e in entradas if e.get('gatschet') and e['seccion'] == 6)}"
          f" · §11: {sum(1 for e in entradas if e.get('gatschet') and e['seccion'] == 11)})")
    print(f"\n  descartados tras leer el texto de Gatschet ({len(DESCARTES_GATSCHET)}):")
    for k, v in DESCARTES_GATSCHET.items():
        print(f"    {k:22} {v[:110]}")


def generar_modulo(entradas, toponimos, comentarios, cobertura, ruta):
    """Escribe lexicon_van_buurt.py — PROPUESTA, no lexicón activo."""
    L = []
    A = L.append
    A('"""')
    A("CURIANA — van Buurt 2014, propuesta de importación (F6)")
    A("=" * 62)
    A("")
    A("GENERADO por `minar_van_buurt.py` — no editar a mano: reejecutar el script.")
    A("")
    A("    van Buurt, Gerard (2014). Caquetío Indians on Curaçao during colonial")
    A("    times and Caquetío words in the Papiamentu language. Curaçao, edición")
    A("    propia. ISBN 978-99904-2-348-8.")
    A("")
    A("ESTE MÓDULO NO SE IMPORTA EN curiana_lexicon.py. Es una propuesta a")
    A("revisión humana. Ninguna forma entra a VOCABULARIO_BASE por este camino")
    A("sin decisión explícita (protocolo 02, §5, regla de oro 1).")
    A("")
    A("LA SEPARACIÓN §6 / §11 ES EL DATO, NO UN DETALLE DE FORMATO.")
    A("van Buurt confiesa en §12 que la edición de 1997 presentó la evidencia sin")
    A("decidir, «leaving room for totally erroneous interpretations». Fusionar")
    A("VAN_BUURT_S6 con VAN_BUURT_S11 repetiría ese error exacto.")
    A("")
    A("Y él mismo advierte de la §6: «the following listing has a subjective")
    A("element». Esa subjetividad viaja en `notas` de cada entrada.")
    A("")
    A("POLÍTICA D7: `glosa_fuente` (verbatim de van Buurt, con sección e isla) e")
    A("`identificacion_moderna` (taxón actual) son campos SEPARADOS. Ninguno gana.")
    A("La marca de isla (A=Aruba, B=Bonaire, C=Curaçao) es distribución")
    A("geográfica: criterio positivo 2 del protocolo.")
    A('"""')
    A("")
    A("")

    def bloque(nombre, items, cabecera):
        A("# " + "═" * 66)
        for l in cabecera:
            A(f"# {l}")
        A("# " + "═" * 66)
        A(f"{nombre}: dict[str, dict] = {{")
        for e in sorted(items, key=lambda x: norm(x["lema"])):
            forma = e["lema"]
            g = e["glosa_fuente"].replace('"', "'").replace("\\", "")[:200]
            notas = [f"van Buurt 2014 §{e['seccion']}"]
            if e["islas"]:
                notas.append("islas: " + "/".join(e["islas"]))
            if e["foto"]:
                notas.append(f"foto {e['foto']}")
            if len(e["formas"]) > 1:
                notas.append("variantes: " + ", ".join(e["formas"][1:]))
            if e["paralelos"]:
                notas.append("paralelos: " + ", ".join(e["paralelos"]))
            if e["gatschet"]:
                notas.append(f"también en Gatschet 1885/Pinart 1882 como "
                             f"«{e['gatschet']['gatschet']}» ({e['gatschet']['glosa_gatschet']})")
            if e["duplicada_en_ambas_secciones"]:
                notas.append("⚠ van Buurt la lista en §6 Y en §11")
            if e["respaldo_toponimico"]:
                notas.append("respaldo toponímico §7: " + ", ".join(e["respaldo_toponimico"]))
            if e["distribucion_amplia"]:
                notas.append("⚠ forma también corriente en tierra firme (filtro 4)")
            if e["reserva_autor"]:
                notas.append("RESERVA DEL AUTOR: " + e["reserva_autor"])
            if e["seccion"] == 6:
                notas.append("el autor advierte que la lista de §6 «has a subjective element»")
            nota = "; ".join(notas).replace('"', "'")
            A(f'    "{forma}": {{')
            A(f'        "glosa_fuente": "{g}",')
            ident = e["identificacion_moderna"]
            A(f'        "identificacion_moderna": ' + (f'"{ident}",' if ident else "None,"))
            A(f'        "islas": {e["islas"]!r},')
            A(f'        "formas": {e["formas"]!r},')
            A(f'        "veredicto": "{e["veredicto"]}",')
            A(f'        "razon": "{e["razon"].replace(chr(34), chr(39))}",')
            A(f'        "fuente_propuesta": "{("caquetío-atestiguado" if e["veredicto"] == "A_atestiguado" else "caquetío-reconstruido" if e["veredicto"] == "B_fuerte" else "hipotético-no-verificado")}",')
            A(f'        "notas": "{nota}",')
            A("    },")
        A("}")
        A("")
        A("")

    s6 = [e for e in entradas if e["seccion"] == 6 and not e["remision"]]
    s11 = [e for e in entradas if e["seccion"] == 11 and not e["remision"]]
    bloque("VAN_BUURT_S6", s6, [
        "§6 — «Words in Papiamentu likely to be of Caquetío Origin»",
        "",
        "Candidatas a `caquetío-atestiguado`. El veredicto A/B/C está en cada",
        "entrada: A = §6 + atestación colonial, coincidencia con Gatschet 1882 o",
        "respaldo toponímico de §7. B = §6 sin respaldo externo adicional.",
        "C dentro de §6 = el autor desmonta la atribución en la propia entrada",
        "(wayaká, wimpiri, shirishiri): la sección dice una cosa y el cuerpo otra.",
    ])
    bloque("VAN_BUURT_S11", s11, [
        "§11 — «Words with less certain links to Caquetío»",
        "",
        "TIER DEGRADADO. van Buurt: «Some of these must surely be of Caquetío",
        "origin, but a different origin cannot be excluded.»",
        "NO son candidatas al léxico activo. Destino: corpus, marcadas.",
        "⚠ `tata` y `kinikini` YA ESTÁN en el lexicón del proyecto como caquetío:",
        "esta sección es evidencia para reclasificarlas hacia abajo, no para",
        "confirmarlas.",
    ])

    remisiones = [e for e in entradas if e["remision"]]
    A("# " + "═" * 66)
    A("# REMISIONES CRUZADAS — no son entradas independientes")
    A("# " + "═" * 66)
    A("REMISIONES_VAN_BUURT: dict[str, str] = {")
    for e in sorted(remisiones, key=lambda x: norm(x["lema"])):
        A(f'    "{e["lema"]}": "{e["glosa_fuente"][:70]}",')
    A("}")
    A("")
    A("")

    A("# " + "═" * 66)
    A("# MORFEMAS documentados por van Buurt (§5 y §8-10)")
    A("# " + "═" * 66)
    A("# Transcritos A MANO desde prosa argumentada, no extraídos por regex.")
    A("# `-ima` confirma DE FORMA INDEPENDIENTE el afijo homónimo de REGLAS_ZAVALA.")
    A("# `-bana` DISCREPA del uso actual del lexicón ('orilla/borde'): resolver.")
    A("")
    A("MORFEMAS_VAN_BUURT: dict[str, dict] = {")
    for k, v in MORFEMAS_VAN_BUURT.items():
        A(f'    "{k}": {{"glosa": "{v["glosa"]}", "forma_alt": '
          + (f'"{v["forma_alt"]}"' if v["forma_alt"] else "None")
          + f', "autoridad": "{v["autoridad"]}", "nota": '
          + (f'"{v["nota"]}"' if v["nota"] else "None") + "},")
    A("}")
    A("")
    A("")

    A("# " + "═" * 66)
    A("# §7 — TOPÓNIMOS (referencia de canon, FUERA del habla)")
    A("# " + "═" * 66)
    A("# Un agente no dice 'Yamanota' para decir nada. Se conservan porque los")
    A("# topónimos son el reservorio más fiable de sustrato (criterio 5 del")
    A("# protocolo) y porque validan morfología: -bana, -bari, -kuri, -ima, wa-.")
    A("")
    A("TOPONIMOS_VAN_BUURT: dict[str, list[dict]] = {")
    for isla, items in toponimos.items():
        A(f'    "{isla}": [')
        for t in items:
            A(f'        {{"toponimo": "{t["toponimo"]}", "generico": '
              + (f'"{t["generico"]}"' if t["generico"] else "None")
              + f', "dudoso": {t["dudoso"]}}},')
        A("    ],")
    A("}")
    A("")
    A("")
    A("# Etimologías comentadas por el autor (§8-10)")
    A("ETIMOLOGIAS_TOPONIMOS: dict[str, str] = {")
    for k, v in sorted(comentarios.items()):
        A(f'    "{k}": "{v.replace(chr(34), chr(39))[:220]}",')
    A("}")
    A("")
    A("")

    A("# " + "═" * 66)
    A("# CRUCE CON GATSCHET 1885 / PINART 1882 — verificado a mano")
    A("# " + "═" * 66)
    A("# Dos recolecciones independientes separadas por 130 años. Donde coinciden,")
    A("# la confianza sube mucho: ninguna cita a la otra.")
    A("")
    A("COINCIDENCIAS_GATSCHET: dict[str, dict] = {")
    for k, v in COINCIDENCIAS_GATSCHET.items():
        A(f'    "{k}": {v!r},')
    A("}")
    A("")
    A("# Candidatos del cruce automático DESCARTADOS al leer el texto de Gatschet.")
    A("DESCARTES_GATSCHET: dict[str, str] = {")
    for k, v in DESCARTES_GATSCHET.items():
        A(f'    "{k}": "{v}",')
    A("}")
    A("")
    A("")
    A("# " + "═" * 66)
    A("# COBERTURA DE LAS 82 ENTRADAS SIN CITA (tarea F1)")
    A("# " + "═" * 66)
    A("COBERTURA_82: dict[str, dict] = {")
    for r in cobertura:
        A(f'    "{r["palabra"]}": {{"donde": "{r["donde"]}", "veredicto": '
          f'"{(r["veredicto"] or "").replace(chr(34), chr(39))}", "cita": '
          + (f'"{r["cita"].replace(chr(34), chr(39))[:170]}"' if r["cita"] else "None")
          + "},")
    A("}")
    A("")
    A("")
    n6 = len(s6)
    n11 = len(s11)
    A("TOTALES = {")
    A(f'    "s6": {n6},')
    A(f'    "s11": {n11},')
    A(f'    "remisiones": {len(remisiones)},')
    A(f'    "toponimos": {sum(len(v) for v in toponimos.values())},')
    A(f'    "morfemas": {len(MORFEMAS_VAN_BUURT)},')
    A(f'    "A_atestiguado": {sum(1 for e in entradas if e["veredicto"] == "A_atestiguado")},')
    A(f'    "B_fuerte": {sum(1 for e in entradas if e["veredicto"] == "B_fuerte")},')
    A(f'    "C_plausible": {sum(1 for e in entradas if e["veredicto"] == "C_plausible")},')
    A("}")
    A("")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"  → módulo generado: {ruta}")
    print(f"     §6={n6}  §11={n11}  topónimos={sum(len(v) for v in toponimos.values())}"
          f"  morfemas={len(MORFEMAS_VAN_BUURT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="RUTA", help="volcar todo a JSON")
    ap.add_argument("--82", dest="ochenta2", action="store_true",
                    help="tabla de cobertura de las 82 entradas sin cita")
    ap.add_argument("--gatschet", action="store_true",
                    help="tabla verificada de coincidencias con Gatschet 1885 / Pinart 1882")
    ap.add_argument("--gatschet-candidatos", action="store_true",
                    help="regenera los candidatos crudos del cruce (con falsos positivos)")
    ap.add_argument("--generar-modulo", nargs="?", const="lexicon_van_buurt.py",
                    metavar="RUTA", help="escribir lexicon_van_buurt.py")
    args = ap.parse_args()

    lineas = leer()
    secs = secciones(lineas)
    for n in (6, 7, 11):
        if n not in secs:
            sys.exit(f"No localizo la sección {n}: ¿cambió el .txt?")

    entradas = (extraer_glosario(lineas, *secs[6], 6)
                + extraer_glosario(lineas, *secs[11], 11))
    toponimos = extraer_toponimos(lineas, *secs[7])
    comentarios = extraer_comentarios(lineas, secs)
    entradas = clasificar(entradas, toponimos)
    cobertura = cobertura_82(entradas, toponimos, lineas)

    if args.gatschet_candidatos:
        toks, evid = _tokens_gatschet()
        print("  CANDIDATOS CRUDOS (incluyen falsos positivos: verificar a mano)")
        for lema, forma, g, tipo in candidatos_gatschet(entradas, toks):
            marca = "✓" if lema in COINCIDENCIAS_GATSCHET else ("✗" if any(
                k.startswith(lema + " ~") for k in DESCARTES_GATSCHET) else "?")
            print(f"  {marca} {lema:14} ({forma:12}) ~ {g:14} [{tipo}]")
            print(f"      {evid.get(norm(g), '')[:100]}")
        return

    if args.generar_modulo:
        ruta = args.generar_modulo
        if not os.path.isabs(ruta):
            ruta = os.path.join(_AQUI, ruta)
        generar_modulo(entradas, toponimos, comentarios, cobertura, ruta)
    elif args.ochenta2:
        informe_82(cobertura)
    elif args.gatschet:
        informe_gatschet(entradas)
    else:
        informe(entradas, toponimos, comentarios, cobertura)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"entradas": entradas, "toponimos": toponimos,
                       "etimologias": comentarios, "morfemas": MORFEMAS_VAN_BUURT,
                       "cobertura_82": cobertura,
                       "gatschet": COINCIDENCIAS_GATSCHET,
                       "descartes_gatschet": DESCARTES_GATSCHET}, f,
                      ensure_ascii=False, indent=2)
        print(f"\n  → JSON: {args.json}")


if __name__ == "__main__":
    main()
