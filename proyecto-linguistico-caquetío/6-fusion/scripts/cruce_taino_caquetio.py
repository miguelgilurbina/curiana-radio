# -*- coding: utf-8 -*-
"""
Cruce TAÍNO <-> CAQUETÍO ATESTIGUADO — campaña del taíno, T4 (2026-09-21).

LA PREGUNTA
-----------
¿Qué comparten de verdad el taíno y el caquetío ATESTIGUADO —en léxico, en
morfología y en onomástica—, y qué de eso es herencia arahuaca común, qué es
préstamo por contacto en la esfera, y qué es casualidad?

POR QUÉ SÓLO CONTRA EL CAQUETÍO ATESTIGUADO
-------------------------------------------
Las capas `caquetío-reconstruido` y `caquetío-hipotético` se fabricaron
mirando al wayuu y al lokono (`arahuaco_comparative.REGLAS_*`, las 441
candidatas). Cruzarlas con el taíno mediría **el andamio**, no el caquetío:
el parecido que saliera sería el que nosotros pusimos. Se miden igual y se
emiten aparte, marcadas `circular`, para que el número exista y no para que
decida nada. El resumen de filiación usa **sólo** la capa atestiguada.

Y por la misma razón queda fuera `taíno-reconstruido` (9 entradas): son
formas que `reconstruir_taino()` generó desde el lokono y sus propias `notas`
lo dicen —«no cuenta como dato taíno en cruces»—. Cruzarlas contra el
caquetío mediría dos veces el mismo lokono.

EL MÉTODO, con las tres lecciones de la skill `minar-fuente` en código
----------------------------------------------------------------------
1. FILTRO DE SIGNIFICADO (§2). Se empareja por la glosa castellana, nunca por
   parecido de forma suelto. Medido el 2026-09-10 en el achagua: de 11
   «aciertos» de forma, sólo 2 aguantaron al mirar la glosa.
2. MIRAR LA CAPA (§8). La entrada cuya forma se derivó de otra lengua es
   circular con esa lengua. Y la entrada taína cuyas `notas` se escribieron
   mirando al caquetío («cognado caquetío probable *kali») lleva aviso: la
   forma es real, la nota no es independiente.
3. DESCONFIAR DE LA PROPIA REGLA (§2, §8). Tres controles:
   - MODELO NULO por permutación: para cada concepto se sortean tantas
     entradas al azar de la misma lengua como emparejaron por glosa. Es la
     versión sin sesgo de «barajar las glosas», y además corrige que el
     achagua (3.568 entradas) ofrezca muchos más candidatos que el taíno (43);
   - CONTROL NO ARAHUACO: la misma medida contra el jirajara/ayomán de Jahn
     1927 (`6-fusion/control_jirajarano_jahn_1927.yaml`), que no es pariente;
   - PRUEBA DE PREDICCIÓN dejando fuera: una correspondencia vista en un par
     predice sobre los demás conceptos. Una que sale una vez no es nada.

SALIDA (PROPUESTA, regla 5)
---------------------------
    6-fusion/cruce_taino_caquetio_2026-09-21.yaml

No toca `curiana_lexicon.py`, ni `lexicon_*.py`, ni `2-lengua/*`, ni
`3-mundo/corpus/`. Ningún cognado entra a `cognados.yaml` por este script.

    python 6-fusion/scripts/cruce_taino_caquetio.py
    python 6-fusion/scripts/cruce_taino_caquetio.py --check   # ¿está al día?
"""
import argparse
import collections
import difflib
import io
import os
import random
import re
import sys
import time
import unicodedata

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL  # noqa: E402
from curiana_fonotactica import fonemizar, forma_comparable  # noqa: E402

SALIDA = os.path.join(R, "6-fusion", "cruce_taino_caquetio_2026-09-21.yaml")
YAML_CONTROL = os.path.join(R, "6-fusion", "control_jirajarano_jahn_1927.yaml")
YAML_TOPONIMOS = os.path.join(R, "2-lengua", "toponimos.yaml")
YAML_COGNADOS = os.path.join(R, "2-lengua", "cognados.yaml")
YAML_ANTROPONIMOS = os.path.join(R, "6-fusion", "antroponimos_caquetios.yaml")
JSON_TAINO_HIP = os.path.join(R, "curiana_sim", "taino_hipotetico.json")
TXT_BRINTON = os.path.join(R, "fuentes_caquetios", "Brinton_1871_texto.txt")
TXT_PANE = os.path.join(R, "fuentes_caquetios",
                        "Pane_c1498_Relacion_Antiguedades_Indios_wikisource.txt")
FECHA = "2026-09-21"

# ── parámetros declarados ANTES de mirar resultados ──────────────────────
UMBRAL_PARECIDO = 0.62      # el de cruzar_jahn_guajiro.py y del cruce achagua
UMBRAL_COGNADO = 0.75
UMBRAL_FORMA = 0.75         # el paso SIN filtro de glosa: listón más alto a propósito
MIN_FONEMAS_FORMA = 4       # y forma más larga, porque ahí no hay glosa que sujete
MIN_FONEMAS = 3             # dos letras no son evidencia (el 80 % de las 441)
REPLICAS = 300
SEMILLA = 1492
GU_ES_W = False             # defecto de curiana_fonotactica; True = sensibilidad
ATESTIGUADO = "caquetío-atestiguado"

LENGUAS = ("taíno", "lokono", "wayunaiki", "achagua")   # las que deciden
INFORMATIVAS = ("kalinago", "paraujano")                # columna extra
CONTROL = "jirajarano"                                  # NO arahuaco
TODAS = LENGUAS + INFORMATIVAS + (CONTROL,)
TOPES = {"taíno": 3, "lokono": 3, "wayunaiki": 2, "achagua": 3,
         "kalinago": 2, "paraujano": 2, "jirajarano": 2}

AFIJOS = {  # (prefijos, sufijos) sobre la forma YA fonemizada
    "taíno": (("wa", "gua", "da", "ma", "ka", "ni"), ()),
    "lokono": (("da", "wa", "li", "to", "bu", "na"), ("n",)),
    "wayunaiki": (("a",), ()),
    "achagua": (("nu", "ri", "ru", "gua", "wa", "ji", "na"), ("si",)),
    "paraujano": (("ta", "a"), ()),
    "kalinago": (("a", "i"), ()),
    "jirajarano": (("a", "i"), ()),
}

SINONIMOS_CRUDOS = {  # declarados: la glosa colonial y la moderna para lo mismo
    "pescado": "pez", "pájaro": "ave", "varón": "hombre", "culebra": "serpiente",
    "demonio": "diablo", "anciano": "viejo", "escuchar": "oír", "jefe": "cacique",
    "maíz": "maiz", "cazabe": "casabe", "jutía": "hutia",
}

# El DOMINIO decide la clase de una pareja, y es la tabla de la skill
# `minar-fuente` §3, que viene de la corrección de Miguel del 2026-09-10:
# «hay palabras que pueden compartirse entre etnias». Lo que decide no es SI
# se comparte, sino QUÉ.
DOMINIO_POR_CATEGORIA = {
    # viajan entre lenguas sin parentesco: préstamo areal, dato de comercio
    "flora": "viajero", "fauna": "viajero", "alimentacion": "viajero",
    "alimentos": "viajero", "comercio": "viajero", "utiles": "viajero",
    "ritual": "viajero", "arquitectura": "viajero", "navegacion": "viajero",
    "jerarquia": "viajero", "materiales": "viajero", "cosmos": "viajero",
    "agricultura": "viajero", "tecnologia": "viajero", "vestimenta": "viajero",
    # casi nunca viajan: si coinciden, es dato de FILIACIÓN
    "cuerpo": "filiacion", "parentesco": "filiacion", "gramatica": "filiacion",
    "pronombres": "filiacion", "numeros": "filiacion",
    # ni lo uno ni lo otro sin mirar el caso
    "geografia": "mixto", "clima": "mixto", "tiempo": "mixto",
    "naturaleza": "mixto", "etnonimia": "mixto",
}
CATS_DE_FILIACION = frozenset({"pron", "num", "interr"})

VOCALES = set("aeiou")

# Sondas de formante: (nombre, patrón sobre la forma en minúsculas).
# Los prefijos se prueban con la grafía colonial Y la fonémica, porque el
# taíno del repo está en grafía castellana y el caquetío en lema fonémico.
SONDAS_PREFIJO = [
    ("ma- privativo", r"^ma"),
    ("ka-/ca- atributivo", r"^(ka|ca)"),
    ("da- 1ª sg.", r"^da"),
    ("gua-/wa-", r"^(gua|wa|hua|gu)"),
    ("ni-", r"^ni"),
]
SONDAS_SUFIJO = [
    ("-bana", r"bana$"),
    ("-coa/-koa/-cua", r"(coa|koa|cua|kua|qua)$"),
    ("-bacoa/-bakoa", r"(bacoa|bakoa|vacoa)$"),
    ("-oa", r"oa$"),
    ("-bo/-abo", r"bo$"),
    ("-ey/-ay", r"([eé]y|[aá]y|g[uü]ey)$"),
    ("-ana", r"ana$"),
    ("-gua", r"gua$"),
    ("-ni/-na", r"(ni|na)$"),
    ("-ío/-yo (gentilicio)", r"([ií]o|yo)$"),
    ("-(h)o nominalizador", r"(ho|o)$"),
    ("-ex final (antropónimo)", r"e[xj]$"),
    ("-el final (antropónimo)", r"[eaoi]l$"),
    # Oliver cap. 2 p. 148 lista -kiva entre los sufijos toponímicos caquetíos
    # y el canon no lo tiene. Se sonda para que el cero (o el no-cero) sea medido.
    ("-kiva/-quiva", r"(kiva|quiva|kiba|quiba)$"),
]

# Castellano y onomástica cristiana que NO debe contar como forma indígena en
# la sonda sobre Pané. Lista DECLARADA: la sonda emite su inventario entero
# para que se pueda auditar.
BLOQUEO_PANE = {
    "dios", "cristo", "jesús", "jesus", "santa", "santo", "san", "juan", "pedro",
    "antonio", "ramón", "ramon", "cristóbal", "cristobal", "colón", "colon",
    "almirante", "virrey", "gobernador", "rey", "reina", "fernando", "isabel",
    "indias", "española", "españa", "castilla", "italia", "magdalena", "isabela",
    "concepción", "concepcion", "ave", "maría", "maria", "credo", "padrenuestro",
    "pater", "noster", "fray", "señor", "señora", "verdad", "ahora", "así", "asi",
    "creo", "dicen", "dice", "entonces", "estando", "todos", "todo", "acabado",
    "pero", "por", "para", "como", "cuando", "esto", "este", "esta", "estos",
    "diremos", "hallándome", "hallandome", "verdaderamente", "capítulo", "capitulo",
    "relación", "relacion", "libro", "primero", "segundo", "tercero", "cuarto",
    "quinto", "sexto", "hombres", "mujeres", "tierra", "cielo", "islas", "isla",
    "los", "las", "una", "uno", "que", "con", "del", "les", "muy", "más", "mas",
    "ayala", "arteaga", "martín", "martin", "ayuno", "fortaleza", "provincia",
    # añadidos DESPUÉS de leer el inventario de la primera pasada (regla 6: el
    # cero y el ruido se auditan mirando la lista, no confiando en el filtro)
    "algunas", "canta", "cómo", "como", "dime", "francisco", "guárdala", "guardala",
    "jerónimo", "jeronimo", "mateo", "mirobalanos", "orden", "pané", "pane", "pues",
    "señoría", "senoria", "subpáginas", "subpaginas", "trae", "vete", "vuestra",
    "wikisource", "borgoña", "borgona", "haití", "haiti",
}


# ═════════════════════════════════════════════════════════════════════════
# Glosas castellanas  (el filtro de significado)
# ═════════════════════════════════════════════════════════════════════════
def sin_diacriticos(s, conservar=True):
    out = []
    for ch in unicodedata.normalize("NFD", str(s or "")):
        if unicodedata.category(ch) == "Mn":
            if conservar and ch == "̈" and out and out[-1] in "uU":
                out.append(ch)
            elif conservar and ch == "̃" and out and out[-1] in "nN":
                out.append(ch)
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


def _norm_es(w):
    """Una palabra castellana, colonial o moderna, a una clave comparable."""
    w = re.sub(r"[^a-zñ]", "", sin_diacriticos(w, False).lower()).replace("ñ", "n")
    if not w:
        return ""
    w = re.sub(r"^h", "", w)
    w = re.sub(r"qu(?=[ao])", "cu", w)
    w = re.sub(r"g(?=[ei])", "j", w)              # muger -> mujer
    w = re.sub(r"c(?=[ei])", "s", w)
    w = w.replace("z", "s").replace("v", "b").replace("x", "j").replace("ll", "y")
    w = re.sub(r"y$", "i", w)
    if len(w) > 4 and w.endswith("es") and w[-3] not in VOCALES:
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and w[-2] in VOCALES:
        w = w[:-1]
    return w


SINONIMOS = {_norm_es(a): _norm_es(b) for a, b in SINONIMOS_CRUDOS.items()}
ARTICULOS = {_norm_es(x) for x in "el la los las lo un una unos unas ser estar".split()}
INDEFINIDOS = {_norm_es(x) for x in "un una unos unas".split()}
# Homonimia castellana que el filtro no puede resolver (medida en el cruce achagua).
HOMONIMOS_DE_GLOSA = {_norm_es("este")}


def es_palabra(w):
    n = _norm_es(w)
    return SINONIMOS.get(n, n)


def conceptos(glosa):
    """[(cabeza, exacto, segmento)] de una glosa. `exacto` = una sola palabra."""
    g = str(glosa or "")
    g = re.sub(r"\([^)]*\)", " ", g)
    g = re.sub(r"\([^)]*$", " ", g)
    g = re.sub(r"[,;]\s*-\w+", " ", g)
    g = re.sub(r"«[^»]*»", " ", g)
    g = re.sub(r"\[[^\]]*\]", " ", g)
    g = re.sub(r"\bv\.\s*g\..*$", " ", g, flags=re.I)
    g = re.sub(r"&\s*c\.?", " ", g)
    out = []
    for p in re.split(r"[,;:./¿?¡!=]|\s+(?:o|ó|u|vel)\s+", g):
        ws = [es_palabra(w) for w in p.split()]
        ws = [w for w in ws if w]
        clase = bool(ws) and ws[0] in INDEFINIDOS
        while ws and ws[0] in ARTICULOS:
            ws.pop(0)
        if ws and not (len(ws) == 1 and len(ws[0]) < 2):
            exacto = len(ws) == 1 and not clase and ws[0] not in HOMONIMOS_DE_GLOSA
            out.append((ws[0], exacto, " ".join(ws)))
    return out


# ═════════════════════════════════════════════════════════════════════════
# Formas
# ═════════════════════════════════════════════════════════════════════════
def fon(forma, orto, gu):
    f = sin_diacriticos(forma).lower()
    if orto == "linguistica":
        f = re.sub(r"(?<![cstkp])h", "j", f)
    f = fonemizar(f, gu_es_w=gu).replace("ü", "u")
    return re.sub(r"(.)\1+", r"\1", f)


def radicales(f, lengua):
    """La forma entera primero y luego sus radicales, en orden ESTABLE.

    ⚠️ Devolver un `set` aquí haría el script irreproducible: el hash de las
    cadenas se aleatoriza por proceso, el orden de los candidatos cambiaría
    entre corridas y los empates de `mejor()` se resolverían distinto. Con
    `--check` eso sería ruido puro. Sale lista ordenada, y la forma completa
    siempre en la posición 0.
    """
    pref, suf = AFIJOS.get(lengua, ((), ()))
    otros = set()
    for p in pref:
        if (f.startswith(p) and len(f) - len(p) >= MIN_FONEMAS
                and (len(p) > 1 or f[len(p)] not in VOCALES)):
            otros.add(f[len(p):])
    for g in list(otros) + [f]:
        for s in suf:
            if g.endswith(s) and len(g) - len(s) >= MIN_FONEMAS:
                otros.add(g[: -len(s)])
    otros.discard(f)
    return [f] + sorted(otros)


def dominio_de(v):
    if v.get("cat") in CATS_DE_FILIACION:
        return "filiacion"
    return DOMINIO_POR_CATEGORIA.get(v.get("categoria") or "", "sin-declarar")


# ═════════════════════════════════════════════════════════════════════════
# Carga
# ═════════════════════════════════════════════════════════════════════════
def _estrato(lengua, v):
    n = v.get("notas") or ""
    if lengua == "taíno":
        if "Brinton" in n:
            return "Brinton 1871 (sin `procedencia.obra`)"
        return "sin estrato declarado — 0 de 52 taínas del lexicón tienen procedencia"
    if lengua == "lokono":
        if "Perea" in n:
            return "Perea 1942"
        for m, et in (("Oliver", "Oliver 1989 A-2"), ("Pet 1987", "Pet 1987"),
                      ("Goeje", "Goeje 1928"), ("Brinton", "Brinton 1871")):
            if m in n:
                return et
    if lengua == "paraujano":
        return "Wilbert 1958-59 vía Oliver 1989 A-2"
    if lengua == "achagua" and "Neira" in n:
        return "Neira y Ribero 1762"
    return "sin estrato declarado"


def cargar_comparanda(lengua, gu):
    """Las entradas del lexicón de una lengua hermana o de contacto."""
    entradas = []
    gemelas = set(CL.FORMA_DE_LA_ESFERA)          # clave castellana con gemela indígena
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != lengua:
            continue
        if lengua == "taíno" and k in gemelas:
            continue    # `maíz` y `maisi` son la MISMA voz: entra la indígena
        base = re.sub(r"-(lokono|achagua|kalinago|wayuu|wayunaiki|paraujano|caribe|\d+)$", "", k)
        formas = [base] + ([v["forma_fuente"]] if v.get("forma_fuente") else [])
        orto = "linguistica" if lengua in ("wayunaiki", "lokono") else "colonial"
        cands = []
        for fm in dict.fromkeys(formas):
            fm2 = forma_comparable(fm, v) if lengua == "lokono" else fm
            fb = fon(fm2, orto, gu)
            if len(fb) < MIN_FONEMAS:
                continue
            for r in radicales(fb, lengua):
                cands.append((r, fm, r != fb))
        ficha = {"forma": base, "glosa": v.get("sig"), "estrato": _estrato(lengua, v)}
        notas = v.get("notas") or ""
        # SESGO INVERSO: la nota se escribió mirando al caquetío.
        mirando_caq = bool(re.search(r"caquet", notas, re.I))
        if mirando_caq:
            ficha["aviso"] = ("la `notas` de esta entrada se escribió comparándola con el caquetío: "
                              "la FORMA es de la fuente, la comparación no es independiente")
        if lengua == "taíno":
            ficha["marca_castellana"] = k in (set(CL.SIN_FORMA_DE_LA_ESFERA)
                                              | set(CL.CASTELLANO_CORRIENTE))
            ficha["dice_paso_al_espanol"] = "español" in notas
        entradas.append({"lengua": lengua, "forma": base, "glosa": v.get("sig"),
                         "clave": k, "cands": cands, "conceptos": conceptos(v.get("sig")),
                         "fon_base": cands[0][0] if cands else "",
                         "ficha": ficha, "dominio": dominio_de(v),
                         "nota_mira_al_caquetio": mirando_caq})
    return entradas


def medir_jirajaroide_frontera():
    """Por qué el control que el encargo sugería no sirve — medido, no dicho."""
    import json
    d = json.load(io.open(os.path.join(R, "curiana_sim", "jirajaroide_frontera_lexicon.json"),
                          encoding="utf-8"))
    v = d["vocabulario"]
    vacias = [e for e in v if str(e.get("forma")).strip() == "?"]
    reales = [e for e in v if e not in vacias]
    caq = [e for e in reales if "caquetio" in str(e.get("lengua", ""))]
    declaradas = (d.get("_estadisticas") or {}).get("pendientes_verificacion")
    out = {
        "archivo": "curiana_sim/jirajaroide_frontera_lexicon.json",
        "por_que_se_miro": "el encargo lo sugería como lista de control no arahuaca",
        "entradas": len(v),
        "ranuras_vacias_con_la_forma_literal_?": len(vacias),
        "entradas_con_forma": len(reales),
        "de_esas_caquetias": len(caq),
        "lenguas_de_las_que_quedan": sorted({str(e.get("lengua")) for e in reales
                                             if "caquetio" not in str(e.get("lengua", ""))}),
        "conceptos_cruzables": 0,
        "veredicto": ("NO SIRVE: lo que queda son topónimos y etnónimos sin glosa léxica, así que "
                      "no hay ni un concepto que cruzar. El control se sacó del vocabulario "
                      "jirajara/ayomán de Jahn 1927, que sí tiene formas con glosa castellana."),
    }
    if declaradas is not None and declaradas != len(vacias):
        out["⚠️_su_propia_estadistica_no_cuadra"] = (
            f"`_estadisticas.pendientes_verificacion` dice {declaradas} y las ranuras con forma «?» "
            f"son {len(vacias)}. Es una cifra escrita a mano dentro del propio archivo (regla 1).")
    return out


def cargar_control(gu):
    """El jirajara/ayomán de Jahn 1927: lengua NO arahuaca."""
    Y = yaml.safe_load(io.open(YAML_CONTROL, encoding="utf-8"))
    entradas = []
    for f in Y["vocabulario"]:
        formas = [x for x in (f.get("jirajara"), f.get("ayoman")) if x]
        cands = []
        for fm in formas:
            for tok in re.split(r"[\s,;]+", str(fm)):
                fb = fon(tok.strip("-!¡?¿"), "colonial", gu)
                if len(fb) < MIN_FONEMAS:
                    continue
                for r in radicales(fb, CONTROL):
                    cands.append((r, tok, r != fb))
        if not cands:
            continue
        entradas.append({"lengua": CONTROL, "forma": formas[0], "glosa": f["castellano"],
                         "clave": f["castellano"], "cands": cands,
                         "conceptos": conceptos(f["castellano"]),
                         "fon_base": cands[0][0],
                         "ficha": {"forma": formas[0], "glosa": f["castellano"],
                                   "estrato": "Jahn 1927 pp. 388-391 (CONTROL, no comparanda)"},
                         "dominio": "sin-declarar", "nota_mira_al_caquetio": False})
    return entradas, Y["meta"]


def derivada_de(v, capa):
    """De qué lengua dicen las `notas` que se sacó la FORMA caquetía."""
    if capa == ATESTIGUADO:
        return []
    n = f"{v.get('notas') or ''} || {v.get('sig') or ''}"
    crudas = set()
    for t in re.findall(r"cognado en ([^\s—;,.]+)", n) + re.findall(r"etiquetada `([^`]+)`", n):
        crudas.update(t.lower().split("/"))
    if re.search(r"desde el WAYUU|<[^)]*Wayunaiki", n) or n.startswith("Way. "):
        crudas.add("wayunaiki")
    if n.startswith("Lok. "):
        crudas.add("lokono")
    out = set()
    for f in crudas:
        f = f.replace("-cogn", "").strip("`() ")
        if f.startswith("wayu"):
            out.add("wayunaiki")
        elif f.startswith("lokono"):
            out.add("lokono")
        elif f.startswith("proto"):
            out.add("proto-arahuaco")
        elif f.startswith("ta"):
            out.add("taíno")
        elif f:
            out.add(f)
    return sorted(out)


def cargar_caquetio(gu):
    out = []
    for k, v in CL.VOCABULARIO_BASE.items():
        capa = CL.capa_epistemica(v.get("fuente"))
        if not capa:
            continue
        base = re.sub(r"-\d+$", "", k)
        orto = "linguistica" if ("reconstru" in capa or "hipot" in capa) else "colonial"
        cands = [(fon(base, orto, gu), base)]
        if v.get("forma_fuente"):
            cands.append((fon(v["forma_fuente"], "colonial", gu), v["forma_fuente"]))
        cands = list({c[0]: c for c in cands if c[0]}.values())
        out.append({"clave": k, "capa": capa, "sig": v.get("sig"), "cat": v.get("cat"),
                    "categoria": v.get("categoria"), "forma_fuente": v.get("forma_fuente"),
                    "notas": v.get("notas") or "", "cands": cands,
                    "conceptos": conceptos(v.get("sig")), "dominio": dominio_de(v),
                    "derivada_de": derivada_de(v, capa)})
    return out


# ═════════════════════════════════════════════════════════════════════════
# Medida
# ═════════════════════════════════════════════════════════════════════════
def indexar(entradas):
    exacto, cualquiera = collections.defaultdict(list), collections.defaultdict(list)
    for e in entradas:
        for cab, ex, _seg in e["conceptos"]:
            if ex:
                exacto[cab].append(e)
            cualquiera[cab].append(e)
    return exacto, cualquiera


def mejor(caq_cands, entradas):
    best = (-1.0, None, None, None)
    for fa, ma in caq_cands:
        sm = difflib.SequenceMatcher(None, autojunk=False)
        sm.set_seq2(fa)
        for e in entradas:
            for fb, mb, rad in e["cands"]:
                sm.set_seq1(fb)
                r = sm.ratio()
                if r > best[0]:
                    best = (r, e, (fb, mb, rad), (fa, ma))
    return best


def emparejar(c, idx_exacto, idx_cualquiera):
    exactas_cabezas = {cab for cab, ex, _ in c["conceptos"] if ex}
    todas_cabezas = {cab for cab, _, _ in c["conceptos"]}
    vistos, exactas, cortas = set(), [], 0
    for cab in sorted(exactas_cabezas):
        for e in idx_exacto.get(cab, []):
            if id(e) not in vistos:
                vistos.add(id(e))
                if e["cands"]:
                    exactas.append(e)
                else:
                    cortas += 1
    cercanas = {id(e) for cab in todas_cabezas for e in idx_cualquiera.get(cab, [])} - vistos
    return exactas, len(cercanas), cortas


def veredicto(sim, n_exactas, n_cercanas, corto, circ, n_cortas=0):
    if corto:
        return "no-comparable", "la forma caquetía tiene menos de tres fonemas"
    if n_exactas == 0:
        if n_cortas:
            return "no-comparable", "la glosa está, pero su forma tiene menos de tres fonemas"
        return "no-comparable", ("solo glosa cercana (hiperónimo o frase)" if n_cercanas
                                 else "el concepto no está en esta lengua")
    if sim >= UMBRAL_PARECIDO and circ:
        return "circular", ("la forma caquetía se derivó de esta lengua (o del proto-arahuaco): "
                            "el parecido es de construcción")
    if sim >= UMBRAL_COGNADO:
        return "cognado-probable", ""
    if sim >= UMBRAL_PARECIDO:
        return "parecido-debil", ""
    return "sin-parecido", ""


def medir(gu, con_nulo=True):
    t0 = time.time()
    lengs = {L: cargar_comparanda(L, gu) for L in LENGUAS + INFORMATIVAS}
    lengs[CONTROL], meta_control = cargar_control(gu)
    idx = {L: indexar(es) for L, es in lengs.items()}
    caq = cargar_caquetio(gu)

    res = []
    for c in caq:
        corto = max((len(fa) for fa, _ in c["cands"]), default=0) < MIN_FONEMAS
        por = {}
        for L in TODAS:
            exactas, n_cerc, n_cortas = emparejar(c, *idx[L])
            ranking = []
            if not corto:
                for e in exactas:
                    s, _, cb, ca = mejor(c["cands"], [e])
                    ranking.append((s, e, cb, ca))
                ranking.sort(key=lambda x: (-x[0], x[1]["clave"]))
            sim = ranking[0][0] if ranking else 0.0
            circ = L in c["derivada_de"] or "proto-arahuaco" in c["derivada_de"]
            ver, porque = veredicto(sim, len(exactas), n_cerc, corto, circ, n_cortas)
            por[L] = {"exactas": exactas, "n_cercanas": n_cerc, "n_cortas": n_cortas,
                      "ranking": ranking, "sim": sim, "veredicto": ver, "porque": porque}
        res.append({"c": c, "corto": corto, "por": por})

    # ── modelo nulo sobre la capa atestiguada ──
    rng = random.Random(SEMILLA)
    pool = {L: sorted([e for e in lengs[L] if e["cands"]], key=lambda e: str(e["clave"]))
            for L in TODAS}
    if con_nulo:
        for r in res:
            if r["c"]["capa"] != ATESTIGUADO or r["corto"]:
                continue
            r["nulo"] = {}
            for L in TODAS:
                n = len(r["por"][L]["exactas"])
                if not n or len(pool[L]) <= n:
                    continue
                excl = {id(e) for e in r["por"][L]["exactas"]}
                sims = []
                for _ in range(REPLICAS):
                    muestra, ids = [], set()
                    intentos = 0
                    while len(muestra) < n and intentos < 500:
                        intentos += 1
                        e = pool[L][rng.randrange(len(pool[L]))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    sims.append(max(0.0, mejor(r["c"]["cands"], muestra)[0]) if muestra else 0.0)
                r["nulo"][L] = sims
    return {"res": res, "lengs": lengs, "idx": idx, "pool": pool,
            "meta_control": meta_control, "segundos": round(time.time() - t0, 1)}


# ═════════════════════════════════════════════════════════════════════════
# Clase de cada pareja: herencia / préstamo / casualidad / indecidible
# ═════════════════════════════════════════════════════════════════════════
def clase_de_pareja(r, p_nulo):
    """La clase NO la decide el parecido: el parecido sólo abre la candidatura.

    La decide (a) el DOMINIO —la tabla de `minar-fuente` §3: lo que viaja
    entre lenguas sin parentesco y lo que casi nunca viaja— y (b) si el mismo
    concepto se parece también en las hermanas, que es lo que distingue una
    herencia arahuaca común de un encuentro sólo taíno-caquetío.
    """
    c, por = r["c"], r["por"]
    sim = por["taíno"]["sim"]
    if por["taíno"]["veredicto"] in ("no-comparable", "sin-parecido"):
        return None, ""
    if por["taíno"]["veredicto"] == "circular":
        return "circular", "la forma caquetía se derivó del taíno: el parecido es de construcción"
    par = por["taíno"]["ranking"][0]
    corta = min(len(par[2][0]), len(par[3][0])) <= MIN_FONEMAS
    if corta:
        return "casualidad", f"parecido sobre {MIN_FONEMAS} fonemas o menos: barato por construcción"
    if p_nulo is not None and p_nulo > 0.10:
        return "casualidad", (f"el modelo nulo alcanza este parecido en el {p_nulo:.0%} de las "
                              f"réplicas: no hace falta parentesco para producirlo")
    hermanas = [L for L in ("lokono", "wayunaiki", "achagua")
                if por[L]["exactas"] and por[L]["sim"] >= UMBRAL_PARECIDO]
    dominio = c["dominio"]
    if dominio == "viajero":
        return "préstamo-probable", (
            "el dominio es de los que viajan entre lenguas sin parentesco (cultígeno, bicho, "
            "mercancía, utensilio, rito): compartirlo es dato de comercio y vecindad, no de filiación"
            + (f"; y se parece además en {', '.join(hermanas)}" if hermanas else ""))
    if dominio == "filiacion" and len(hermanas) >= 2:
        return "herencia-probable", (
            "vocabulario que casi nunca viaja y el mismo concepto se parece también en "
            + ", ".join(hermanas) + ": arahuaco común, no un lazo taíno-caquetío particular")
    if dominio == "filiacion":
        return "indecidible", (
            "vocabulario de filiación, pero el parecido no se repite en las hermanas: con una sola "
            "pareja no se decide si es innovación compartida o casualidad")
    if len(hermanas) >= 2:
        return "herencia-probable", (
            "el mismo concepto se parece también en " + ", ".join(hermanas)
            + ": patrimonio arahuaco antes que lazo taíno-caquetío")
    return "indecidible", ("dominio sin declarar o ambiguo y sin apoyo en las hermanas: "
                           "la pareja queda abierta")


# ═════════════════════════════════════════════════════════════════════════
# Resumen de la capa atestiguada
# ═════════════════════════════════════════════════════════════════════════
def resumir(M):
    ates = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO]
    utiles = [r for r in ates if not r["corto"]]
    por_lengua = {}
    for L in TODAS:
        comp = [r for r in utiles if r["por"][L]["exactas"]]
        obs_p = sum(r["por"][L]["sim"] >= UMBRAL_PARECIDO for r in comp)
        obs_c = sum(r["por"][L]["sim"] >= UMBRAL_COGNADO for r in comp)
        d = {"entradas_de_la_lengua": len(M["lengs"][L]),
             "conceptos_comparables": len(comp),
             "parecidos_ge_umbral": obs_p,
             "cognado_probable_ge_umbral_cognado": obs_c,
             "tasa_parecido": round(obs_p / len(comp), 3) if comp else None,
             "similitud_media": round(sum(r["por"][L]["sim"] for r in comp) / len(comp), 3) if comp else None,
             "candidatos_por_concepto_media": round(
                 sum(len(r["por"][L]["exactas"]) for r in comp) / len(comp), 2) if comp else None}
        con_nulo = [r for r in comp if "nulo" in r and L in r["nulo"]]
        if con_nulo:
            tot_p = [sum(r["nulo"][L][i] >= UMBRAL_PARECIDO for r in con_nulo) for i in range(REPLICAS)]
            tot_c = [sum(r["nulo"][L][i] >= UMBRAL_COGNADO for r in con_nulo) for i in range(REPLICAS)]
            media_nula = sum(sum(r["nulo"][L]) / REPLICAS for r in con_nulo) / len(con_nulo)
            obs_p_n = sum(r["por"][L]["sim"] >= UMBRAL_PARECIDO for r in con_nulo)
            obs_c_n = sum(r["por"][L]["sim"] >= UMBRAL_COGNADO for r in con_nulo)
            d["azar"] = {
                "conceptos_con_modelo_nulo": len(con_nulo),
                "parecidos_observados_en_esos": obs_p_n,
                "parecidos_esperados": round(sum(tot_p) / REPLICAS, 2),
                "cognados_observados_en_esos": obs_c_n,
                "cognados_esperados": round(sum(tot_c) / REPLICAS, 2),
                "similitud_media_esperada": round(media_nula, 3),
                "p_parecidos_ge_observado": round(sum(t >= obs_p_n for t in tot_p) / REPLICAS, 3),
                "p_cognados_ge_observado": round(sum(t >= obs_c_n for t in tot_c) / REPLICAS, 3),
            }
            d["exceso_de_parecidos_sobre_el_azar"] = round(obs_p_n - sum(tot_p) / REPLICAS, 2)
        por_lengua[L] = d
    return {
        "entradas_caquetio_atestiguado": len(ates),
        "formas_de_menos_de_tres_fonemas": len(ates) - len(utiles),
        "con_concepto_en_alguna_de_las_cuatro": len(
            [r for r in utiles if any(r["por"][L]["exactas"] for L in LENGUAS)]),
        "con_concepto_en_las_cuatro": len(
            [r for r in utiles if all(r["por"][L]["exactas"] for L in LENGUAS)]),
        "por_lengua": por_lengua,
    }


def p_nulo_de(r, L):
    if "nulo" not in r or L not in r["nulo"]:
        return None
    s = r["por"][L]["sim"]
    return sum(x >= s for x in r["nulo"][L]) / REPLICAS


# ═════════════════════════════════════════════════════════════════════════
# Correspondencias: una sale una vez y no es nada; tres veces es una regla
# ═════════════════════════════════════════════════════════════════════════
def alinear(a, b):
    m = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("equal", "replace"):
            for d in range(i2 - i1):
                m[i1 + d] = b[j1 + d] if j1 + d < j2 else "∅"
        elif tag == "delete":
            for i in range(i1, i2):
                m[i] = "∅"
    return m


def reglas_de(a, b):
    m = alinear(a, b)
    out = []
    for i, x in enumerate(a):
        if x in VOCALES:
            continue
        y = m.get(i, "∅")
        if y != x:
            out.append((x, y, False))
            if i == 0:
                out.append((x, y, True))
    return out


def nombre_regla(x, y, inicial, lengua="taíno"):
    return f"caq {'#' if inicial else ''}{x} ~ {lengua[:3]} {y}"


def juicio_regla(apoyos, aplicables, tasa, tasa_azar):
    if apoyos < 3:
        return (f"NO es una regla: {apoyos} apoyo(s). Una correspondencia que sale una o dos "
                "veces no es nada (hacen falta tres)")
    if aplicables < 5:
        return "sin casos suficientes para ponerla a predecir (menos de 5 aplicables)"
    if tasa is not None and tasa_azar is not None and tasa >= 0.5 and tasa >= 2 * tasa_azar:
        return "predice por encima del azar"
    return "NO predice: falla o no supera al azar"


def aplica(a, b, x, y, inicial):
    pos = [i for i, c in enumerate(a) if c == x and (not inicial or i == 0)]
    if not pos:
        return None
    m = alinear(a, b)
    return any(m.get(i) == y for i in pos)


def mejor_forma(a, entradas):
    _s, _e, cb, _ca = mejor([(a, a)], entradas)
    return cb[0] if cb else None


def prueba_dejando_fuera(M, lenguas):
    rng = random.Random(SEMILLA + 2)
    out = {"diseño": (
        "Para cada lengua se alinean los pares atestiguados que se parecen (cognado-probable o "
        "parecido-debil) y se anotan sus correspondencias consonánticas no idénticas. Cada una "
        "predice sobre TODOS los demás conceptos atestiguados con glosa exacta en esa lengua "
        "(fuera los que la sugirieron). La tasa por azar repite la prueba con entradas al azar de "
        f"la misma lengua ({REPLICAS} réplicas). Juicio: hacen falta 3 apoyos para llamarla regla, "
        "y 5 casos aplicables para ponerla a predecir.")}
    for L in lenguas:
        base = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO and not r["corto"]
                and r["por"][L]["exactas"]]
        base.sort(key=lambda r: r["c"]["clave"])
        pool = M["pool"][L]
        cnt, apoyos, pares = collections.Counter(), collections.defaultdict(list), 0
        for r in base:
            p = r["por"][L]
            if p["veredicto"] not in ("cognado-probable", "parecido-debil"):
                continue
            pares += 1
            _s, _e, cb, ca = p["ranking"][0]
            for regla in set(reglas_de(ca[0], cb[0])):
                cnt[regla] += 1
                apoyos[regla].append((r["c"]["clave"], f"{ca[1]} ~ {cb[1]}"))
        reglas = []
        for regla, n in sorted(cnt.items(), key=lambda kv: (-kv[1], nombre_regla(*kv[0]))):
            x, y, ini = regla
            fuera = {k for k, _ in apoyos[regla]}
            aplicables = aciertos = az_ap = az_ac = 0
            casos = []
            for r in base:
                if r["c"]["clave"] in fuera:
                    continue
                a = r["c"]["cands"][0][0]
                b = mejor_forma(a, r["por"][L]["exactas"])
                h = aplica(a, b, x, y, ini) if b else None
                if h is None:
                    continue
                aplicables += 1
                aciertos += int(h)
                casos.append(f"{r['c']['clave']} ~ {b}: {'acierta' if h else 'falla'}")
                k = len(r["por"][L]["exactas"])
                if len(pool) <= k:
                    continue
                excl = {id(e) for e in r["por"][L]["exactas"]}
                for _ in range(REPLICAS):
                    muestra, ids, intentos = [], set(), 0
                    while len(muestra) < k and intentos < 500:
                        intentos += 1
                        e = pool[rng.randrange(len(pool))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    bz = mejor_forma(a, muestra) if muestra else None
                    hz = aplica(a, bz, x, y, ini) if bz else None
                    if hz is not None:
                        az_ap += 1
                        az_ac += int(hz)
            tasa = round(aciertos / aplicables, 3) if aplicables else None
            tasa_azar = round(az_ac / az_ap, 3) if az_ap else None
            reglas.append({"regla": nombre_regla(x, y, ini, L), "apoyos": n,
                           "visto_en": [f"{k}: {par}" for k, par in apoyos[regla]],
                           "aplicables": aplicables, "aciertos": aciertos,
                           "fallos": aplicables - aciertos, "tasa_de_acierto": tasa,
                           "tasa_por_azar": tasa_azar,
                           "juicio": juicio_regla(n, aplicables, tasa, tasa_azar),
                           "casos": casos[:15]})
        out[L] = {"pares_parecidos": pares, "conceptos_con_glosa_exacta": len(base),
                  "correspondencias_distintas": len(reglas),
                  "con_tres_apoyos_o_mas": sum(1 for x in reglas if x["apoyos"] >= 3),
                  "reglas": reglas[:12]}
    return out


# ═════════════════════════════════════════════════════════════════════════
# Auditar el cero: qué se perdió, y qué dice el canon que ya existe
# ═════════════════════════════════════════════════════════════════════════
def bloque_los_comparables(M):
    """Con un denominador de cuatro, los casos SON el resultado: van uno a uno."""
    out = []
    for r in M["res"]:
        if r["c"]["capa"] != ATESTIGUADO or not r["por"]["taíno"]["exactas"]:
            continue
        s, e, cb, ca = r["por"]["taíno"]["ranking"][0]
        out.append({
            "concepto": sorted({cab for cab, ex, _ in r["c"]["conceptos"] if ex}),
            "caquetio": r["c"]["clave"], "glosa_caquetia": r["c"]["sig"],
            "cita_caquetia": (r["c"]["notas"] or "sin nota")[:150],
            "taino": e["forma"], "glosa_taina": e["glosa"],
            "cita_taina": e["ficha"]["estrato"],
            "otros_candidatos_taino": [f"{e2['forma']} ({s2:.2f})"
                                       for s2, e2, _c, _a in r["por"]["taíno"]["ranking"][1:4]],
            "comparado": f"{ca[0]} ~ {cb[0]}", "similitud": round(s, 3),
            "dominio": r["c"]["dominio"],
            "lectura": "sin parecido: las dos lenguas usan palabras distintas para esto",
        })
    out.sort(key=lambda d: -d["similitud"])
    return out


def bloque_glosa_cercana(M):
    """Lo que el filtro de significado descartó, para que el cero sea auditable."""
    out = []
    for r in M["res"]:
        if r["c"]["capa"] != ATESTIGUADO:
            continue
        p = r["por"]["taíno"]
        if not p["exactas"] and p["n_cercanas"]:
            out.append({"caquetio": r["c"]["clave"], "glosa": r["c"]["sig"],
                        "entradas_taínas_con_glosa_cercana": p["n_cercanas"]})
    out.sort(key=lambda d: d["caquetio"])
    return out


ETNONIMOS = frozenset({"caquetio", "kaketio", "taino", "caribe", "karibna", "kalinago"})


def buscar_en_el_lexicon(forma, gu):
    """La forma tal cual, por `forma_fuente`, o por lema fonémico.

    Hace falta por D5: `cognados.yaml` escribe `quiva` y el lexicón lematizó a
    `kiba` con `forma_fuente: quiva`. Buscar sólo por la clave daría un «no
    está» falso, y un cero falso es peor que ninguno.
    """
    if forma in CL.VOCABULARIO_BASE:
        return forma, CL.VOCABULARIO_BASE[forma].get("fuente"), "clave directa"
    if forma in CL.FUERA_DEL_HABLA:
        return forma, CL.FUERA_DEL_HABLA[forma].get("fuente"), "⚠️ en FUERA_DEL_HABLA (archivada)"
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("forma_fuente") and str(v["forma_fuente"]).lower() == forma.lower():
            return k, v.get("fuente"), f"por forma_fuente «{v['forma_fuente']}»"
    lema = fon(forma, "colonial", gu)
    if lema:
        for k, v in CL.VOCABULARIO_BASE.items():
            if fon(k, "colonial", gu) == lema:
                return k, v.get("fuente"), f"por lema fonémico «{lema}»"
    return None, None, "no está"


def bloque_cognados_ya_declarados(gu):
    """Los sets de `2-lengua/cognados.yaml` que ya emparejan caquetío con taíno.

    Es lo primero que había que mirar y no estaba mirado: el canon de datos de
    lengua YA tiene parejas CQ~TN. Aquí se auditan una a una, con las tres
    preguntas de la regla 8 y de la skill §8: ¿cita a alguien?, ¿la forma
    caquetía existe en el lexicón?, ¿no serán las dos la misma palabra
    castellana escrita dos veces?
    """
    Y = yaml.safe_load(io.open(YAML_COGNADOS, encoding="utf-8"))
    filas, resumen = [], collections.Counter()
    for c in Y["cognados"]:
        f = c.get("formas") or {}
        if "CQ" not in f or "TN" not in f:
            continue
        cq, tn = str(f["CQ"]), str(f["TN"])
        prim_tn = re.split(r"\s*/\s*", tn)[0].strip()
        a, b = fon(cq, "colonial", gu), fon(prim_tn, "colonial", gu)
        sim = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0.0
        proc = c.get("procedencia") or {}
        clave_cq, capa_cq, como = buscar_en_el_lexicon(cq, gu)
        identicas = _norm_es(cq) == _norm_es(prim_tn) and bool(_norm_es(cq))
        etnonimo = _norm_es(cq) in {_norm_es(x) for x in ETNONIMOS} or \
                   _norm_es(prim_tn) in {_norm_es(x) for x in ETNONIMOS}
        lado_cq_no_es_caquetio = bool(capa_cq) and not str(capa_cq).startswith("caquetío")
        if proc.get("obra") and c.get("fuente") == "atestiguado":
            ver = "ATESTIGUADO CON CITA"
            porque = f"cita {proc['obra']} p. {proc.get('pagina')}"
        elif lado_cq_no_es_caquetio:
            ver = "EL LADO CAQUETÍO NO ES CAQUETÍO"
            porque = (f"la forma de la columna CQ está en el lexicón etiquetada `{capa_cq}`. "
                      "Un set que empareja una voz taína con otra voz taína no dice nada del "
                      "caquetío")
        elif etnonimo:
            ver = "CIRCULAR: es un etnónimo"
            porque = ("emparejar el nombre de un pueblo con el nombre de otro no es un cognado "
                      "léxico; y `taino` como autónimo ya lo desmiente Brinton p. impresa 14")
        elif identicas:
            ver = "NO ES UN COGNADO: la misma palabra escrita dos veces"
            porque = ("las dos formas son idénticas y el set no cita a nadie. Es el préstamo que el "
                      "castellano tomó del taíno y devolvió a todas partes: lo que prueba es que "
                      "nosotros escribimos la palabra igual en las dos columnas")
        elif not proc.get("obra"):
            ver = "SIN PROCEDENCIA"
            porque = ("regla 8: no hay clave foránea que citar. Se declara `deuda: sin-procedencia`; "
                      "el hueco se admite, callarlo no")
        else:
            ver = "CON CITA, capa reconstruida"
            porque = f"cita {proc['obra']}"
        resumen[ver] += 1
        filas.append({
            "id": c["id"], "glosa": c["glosa"], "cq": cq, "tn": tn,
            "similitud_fonemica": round(sim, 3),
            "capa_declarada": c.get("fuente"), "confianza": c.get("confianza"),
            "procedencia": (f"{proc.get('obra')} p. {proc.get('pagina')}" if proc.get("obra")
                            else None),
            "forma_caquetia_en_el_lexicon": (f"{clave_cq} · {capa_cq} ({como})" if clave_cq
                                             else "NO ESTÁ"),
            "veredicto": ver, "por_que": porque,
        })
    filas.sort(key=lambda d: (d["veredicto"], d["id"]))
    return {
        "que_es": ("los sets de 2-lengua/cognados.yaml que ya emparejan una forma CQ con una TN. "
                   "Existían antes de esta campaña y nadie los había auditado como grupo."),
        "sets_con_CQ_y_TN": len(filas),
        "reparto": dict(sorted(resumen.items())),
        "formas_caquetias_que_no_estan_en_el_lexicon": sorted(
            d["cq"] for d in filas if d["forma_caquetia_en_el_lexicon"] == "NO ESTÁ"),
        "filas": filas,
    }


def bloque_hallazgos_de_etiqueta(gu):
    """Formas taínas que el repo tiene pero NO bajo la etiqueta `taíno`.

    El cero del cruce por glosa no mide las dos lenguas: mide las dos listas.
    Esto cuenta cuánto de ese cero es un problema de etiqueta.
    """
    import json
    hip = json.load(io.open(JSON_TAINO_HIP, encoding="utf-8"))
    declaradas = {k: v for k, v in hip.items()
                  if str(v.get("notas", "")).startswith("Taíno atestiguado")}
    fuera = []
    for k, v in sorted(declaradas.items()):
        ent = CL.VOCABULARIO_BASE.get(k)
        fuente = ent.get("fuente") if ent else None
        if fuente == "taíno":
            continue
        fuera.append({"forma": k, "glosa_en_el_json": v.get("es"),
                      "etiqueta_en_el_lexicon": fuente or "no está en VOCABULARIO_BASE",
                      "lo_que_dice_el_json": str(v.get("notas"))[:120]})
    # ¿hay una voz caquetía atestiguada con la misma glosa normalizada?
    por_glosa = collections.defaultdict(list)
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != ATESTIGUADO:
            continue
        for cab, ex, _ in conceptos(v.get("sig")):
            if ex:
                por_glosa[cab].append(k)
    for d in fuera:
        for cab, ex, _ in conceptos(d["glosa_en_el_json"]):
            if ex and por_glosa.get(cab):
                cqs = por_glosa[cab]
                a = fon(d["forma"], "colonial", gu)
                mejor_cq, mejor_s = None, 0.0
                for cq in cqs:
                    b = fon(cq, "colonial", gu)
                    s = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
                    if s > mejor_s:
                        mejor_cq, mejor_s = cq, s
                d["pareja_caquetia_que_el_cruce_se_pierde"] = {
                    "caquetio": mejor_cq, "concepto": cab, "similitud": round(mejor_s, 3)}
    return {
        "que_es": ("curiana_sim/taino_hipotetico.json declara 14 formas «Taíno atestiguado». "
                   "Esto mira cuántas de ellas NO llevan la etiqueta `taíno` en el lexicón, y si "
                   "alguna tenía pareja caquetía que el cruce por glosa se pierde por eso."),
        "declaradas_atestiguadas_en_el_json": len(declaradas),
        "de_esas_sin_la_etiqueta_taino_en_el_lexicon": len(fuera),
        "casos": fuera,
        "lo_que_falta_del_todo": {
            "que_es": ("voces taínas que las propias fuentes del repo imprimen, que tienen pareja "
                       "caquetía atestiguada declarada en cognados.yaml, y que NO están en el "
                       "lexicón bajo ninguna etiqueta. Se listan como propuesta para T1/T2; este "
                       "script no las añade (regla 5)."),
            "casos": [
                {"taino": "bagua / bara-wa 'mar'",
                 "donde_esta_en_el_repo": ("2-lengua/cognados.yaml cognado-016 (con cita: "
                                           "oliver-1989-cap2 p. 150) y cognado-019; "
                                           "brinton-1871 p. impresa 11 s.v. Bagua «the sea»"),
                 "pareja_caquetia": "para / parawa 'mar', caquetío-atestiguado",
                 "por_que_importa": ("es la pareja CQ~TN mejor citada que hay, y el lexicón no tiene "
                                     "ninguna entrada taína para 'mar': por eso el cruce por glosa "
                                     "no la ve")},
                {"taino": "siba 'piedra'",
                 "donde_esta_en_el_repo": ("el lexicón la tiene, pero etiquetada `lokono`; "
                                           "taino_hipotetico.json la declara «Taíno atestiguado»; "
                                           "brinton-1871 p. impresa 14 «Siba, a stone»"),
                 "pareja_caquetia": "kiba 'piedra' (forma_fuente `quiva`), caquetío-atestiguado",
                 "por_que_importa": ("el cruce la puntúa 0,75 contra el LOKONO y 0 contra el taíno, "
                                     "y es la misma forma. Es el ejemplo más claro de que el cero "
                                     "mide la etiqueta y no la lengua")},
            ],
        },
    }


def paso_por_forma(M, gu):
    """Cruce por ESQUELETO FONÉMICO, sin filtro de significado.

    El encargo lo pide y hay que hacerlo, pero existe sobre todo para poder
    DESCARTARLO con número: medido el 2026-09-10 sobre el achagua, 7 de 11
    «aciertos» de forma se caen al mirar la glosa. Aquí el listón sube a
    0,75 y se exigen 4 fonemas, y cada pareja dice si las glosas coinciden.
    """
    caq = [r["c"] for r in M["res"] if r["c"]["capa"] == ATESTIGUADO
           and r["c"]["cands"] and len(r["c"]["cands"][0][0]) >= MIN_FONEMAS_FORMA]
    cab_caq = {c["clave"]: {x for x, ex, _ in c["conceptos"] if ex} for c in caq}
    out, por_lengua = [], {}
    for L in TODAS:
        pool = [e for e in M["lengs"][L] if len(e.get("fon_base") or "") >= MIN_FONEMAS_FORMA]
        hits, con_glosa = [], 0
        for c in caq:
            a = c["cands"][0][0]
            sm = difflib.SequenceMatcher(None, autojunk=False)
            sm.set_seq2(a)
            mejor_s, empatadas = 0.0, []
            for e in pool:
                sm.set_seq1(e["fon_base"])
                s = sm.ratio()
                if s > mejor_s + 1e-9:
                    mejor_s, empatadas = s, [e]
                elif abs(s - mejor_s) <= 1e-9:
                    empatadas.append(e)
            # Desempate POR GLOSA, y es importante: el lokono tiene `catti`
            # 'mes' y `kathi` 'luna' con la misma forma fonemizada, y quedarse
            # con la primera daría «las glosas no coinciden» sobre un empate.
            mejor_e = next((e for e in empatadas
                            if cab_caq[c["clave"]] & {x for x, ex, _ in e["conceptos"] if ex}),
                           empatadas[0] if empatadas else None)
            if mejor_s >= UMBRAL_FORMA and mejor_e is not None:
                cab_e = {x for x, ex, _ in mejor_e["conceptos"] if ex}
                coincide = bool(cab_caq[c["clave"]] & cab_e)
                con_glosa += int(coincide)
                hits.append({"lengua": L, "caquetio": c["clave"], "glosa_caquetia": c["sig"],
                             "comparanda": mejor_e["forma"], "glosa_comparanda": mejor_e["glosa"],
                             "similitud": round(mejor_s, 3),
                             "las_glosas_coinciden": coincide})
        por_lengua[L] = {"formas_caquetias_probadas": len(caq), "entradas_de_la_lengua": len(pool),
                         "parejas_de_forma_ge_umbral": len(hits),
                         "de_esas_con_la_glosa_tambien": con_glosa,
                         "ruido": len(hits) - con_glosa}
        if L in ("taíno", CONTROL):
            out.extend(hits)
    out.sort(key=lambda d: (d["lengua"], -d["similitud"]))
    return {
        "diseño": (f"cada forma caquetía atestiguada de {MIN_FONEMAS_FORMA}+ fonemas contra todas "
                   f"las de cada lengua; se listan las de similitud >= {UMBRAL_FORMA}. La columna "
                   "`de_esas_con_la_glosa_tambien` es la que importa: lo demás es ruido, y el "
                   "número dice cuánto."),
        "por_lengua": por_lengua,
        "parejas_taino_y_control": out,
    }


# ═════════════════════════════════════════════════════════════════════════
# Morfología
# ═════════════════════════════════════════════════════════════════════════
def _sondar(formas, sondas):
    out = {}
    for nombre, patron in sondas:
        hits = sorted({f for f in formas if re.search(patron, f)})
        out[nombre] = {"n": len(hits), "formas": hits[:14]}
    return out


def headwords_brinton():
    """Los lemas de la «Vocabulary of the Ancient Language of the Great Antilles».

    SONDA, no censo. El censo de las fuentes taínas es de otro escriba; aquí
    sólo se cuentan formantes sobre la lista que Brinton 1871 pp. 11-14 imprime.
    """
    txt = io.open(TXT_BRINTON, encoding="utf-8", errors="replace").read()
    i = txt.find("Vocabulary  of  the  Ancient  Language")
    j = txt.find("The  following  numerals  are  given")
    if i < 0 or j < 0:
        return [], "no localizada"
    cuerpo = txt[i:j]
    out = []
    for ln in cuerpo.split("\n"):
        m = re.match(r"^([A-Z][A-Za-zá-úñ]{2,})(?:\s+or\s+([a-zá-úñ]+))?\s*[,.]", ln)
        if m:
            out.append(m.group(1).lower())
            if m.group(2):
                out.append(m.group(2).lower())
    return sorted(set(out)), "Brinton 1871 pp. impresas 11-14"


def onomastica_pane():
    """SONDA de formantes sobre las formas indígenas de Pané.

    Regla declarada y auditable: tokens capitalizados de 4+ letras que no
    estén en BLOQUEO_PANE y que no abran oración tras punto. El inventario
    entero se emite para que se pueda revisar a mano.
    ⚠️ El texto es la retraducción castellana de la versión italiana de Ulloa:
    cada nombre pasó por dos copistas. Sirve para contar formantes, no para
    citar una forma como exacta.
    """
    txt = io.open(TXT_PANE, encoding="utf-8", errors="replace").read()
    txt = re.sub(r"[.!?:;]\s+", " ␞ ", txt)     # marca de inicio de oración
    out = collections.Counter()
    for m in re.finditer(r"(␞\s+)?\b([A-ZÁÉÍÓÚÑ][a-zá-úñ]{3,})\b", txt):
        if m.group(1):
            continue
        w = m.group(2).lower()
        if w in BLOQUEO_PANE:
            continue
        out[w] += 1
    return out


def bloque_morfologia(M, caq_ates, taino_ates):
    """La tabla morfema a morfema. Los apoyos son DECLARADOS con su cita; lo
    que el script mide es cuántas formas del repo los exhiben de verdad."""
    f_caq = sorted({c["clave"] for c in caq_ates} |
                   {c["forma_fuente"] for c in caq_ates if c.get("forma_fuente")})
    f_tno = sorted({e["forma"] for e in taino_ates})
    brinton, cita_brinton = headwords_brinton()
    medido = {
        "caquetio_atestiguado": {"n": len(f_caq), **_sondar(f_caq, SONDAS_PREFIJO + SONDAS_SUFIJO)},
        "taino_atestiguado_del_lexicon": {"n": len(f_tno),
                                          **_sondar(f_tno, SONDAS_PREFIJO + SONDAS_SUFIJO)},
        "taino_lemas_de_brinton": {"n": len(brinton), "cita": cita_brinton,
                                   **_sondar(brinton, SONDAS_PREFIJO + SONDAS_SUFIJO)},
    }

    filas = [
        {
            "morfema_caquetio": "ma- privativo",
            "capa_y_cita_caquetia": ("atestiguado en la nota (2-lengua/morfologia.md §6): van Buurt "
                                     "2014 §8 y el par mínimo lokono de Perea 1942 p. 555. La entrada "
                                     "del motor sigue con `deuda: sin-procedencia`"),
            "candidato_taino": "ma- en mahite 'sin dientes'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 13: mahite «you have lost a tooth»; y "
                                     "compara el arahuaco «marikata, you have no teeth (ma negative, "
                                     "ari tooth)». Oliver 1989 cap. 2 p. 147 n. 43 lo generaliza: el "
                                     "privativo /mV-/ es común a las lenguas maipures"),
            "veredicto": "MISMO MORFEMA, y el paralelo no es taíno-caquetío: es arahuaco común",
            "por_que": ("Brinton segmenta ma- + ari 'diente' y Oliver lo declara maipure general. "
                        "Sirve para confirmar que el caquetío tiene lo que la familia tiene; NO "
                        "acerca el taíno al caquetío más que a cualquier otra hermana."),
        },
        {
            "morfema_caquetio": "ma- privativo",
            "capa_y_cita_caquetia": "igual que la fila de arriba",
            "candidato_taino": "manicato 'fuerte, valiente'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 13, citando a Oviedo. Brinton lo "
                                     "relaciona con un arahuaco «manikade» glosado «I am unhurt, I am "
                                     "unconquered», pero NO lo segmenta"),
            "veredicto": "INDECIDIBLE — el sentido es negativo y encaja, pero nadie lo segmenta",
            "por_que": ("El OCR de la etimología de Brinton («from indn, manin») no es legible y hay "
                        "que verla en imagen antes de citarla. Sin segmentación explícita, contar "
                        "manicato como apoyo de ma- sería la trampa que el proyecto se tragó dos "
                        "veces hoy mismo: macana no sostenía -kana, y el -po de apopo era "
                        "reduplicación. Comparte sílaba; el morfema está sin probar."),
        },
        {
            "morfema_caquetio": "ka- atributivo / existencial",
            "capa_y_cita_caquetia": ("atestiguado en la nota: van Buurt 2014 §8 (Casibari «hay rocas "
                                     "duras») y el par mínimo k-ere-u-ti / m-ere-u-ti de Perea 1942 "
                                     "p. 555. d21.5 → C, 2026-09-21"),
            "candidato_taino": "ka-/ca- inicial (caney, cacique, casabe, caona, caiman…)",
            "que_fuente_lo_afirma": ("NADIE en el repo. Brinton no segmenta ningún ca- taíno como "
                                     "prefijo; Oliver cap. 2 p. 148 da el atributivo /k-/, /kV-/ "
                                     "entre los afijos ARAHUACOS generales, sin ejemplo taíno"),
            "veredicto": "SIN APOYO — la sílaba está, el morfema no está afirmado por ninguna fuente",
            "por_que": ("`caiman` Brinton lo glosa «lit. to be strong» sobre el arahuaco k-aiman, que "
                        "sí sería el atributivo; pero es su lectura del ARAHUACO de Guayana, no del "
                        "taíno, y una sola lectura no hace regla. Queda como pregunta para el minado "
                        "de T1/T2, no como corroboración."),
        },
        {
            "morfema_caquetio": "da- / d- de 1ª persona singular",
            "capa_y_cita_caquetia": ("el motor NO lo tiene como regla: `ta-` (wayuu) es su posesivo de "
                                     "1ª sg. El /dA-/ caquetío es dato de oliver-1989-cap2 pp. 146-147 "
                                     "en diao, dare, dato, datihao — y es el pilar de que el caquetío "
                                     "salga del mismo fondo que el lokono"),
            "candidato_taino": "daca 'yo' (Pané); da- en da(i)tia-o; m-a(h)i-te que sería da-ai",
            "que_fuente_lo_afirma": ("pane-c1498 cap. XXV: «Dios naboria daca» glosado «yo soy siervo "
                                     "de Dios»; oliver-1989-cap2 p. 147: «/da-/ in da(i)tia-o is first "
                                     "person singular marker», y p. 136 sitúa /dA-/ en lokono, taíno y "
                                     "«perhaps Caquetío»"),
            "veredicto": "MISMO MORFEMA — y es el paralelo mejor sostenido de los tres",
            "por_que": ("Es el único de la lista con atestación taína dentro del repo (Pané) y con la "
                        "afirmación explícita de Oliver. ⚠️ Pero es exactamente el argumento de "
                        "filiación que ya sostiene D11, y NO es exclusivo taíno-caquetío: el lokono "
                        "lo tiene igual. Acerca al caquetío al par lokono-taíno frente al "
                        "guajiro-paraujano (/tA-/), no al taíno en particular."),
            "alerta": ("⚠️ CHOQUE CON EL LEXICÓN, y hay que mirarlo: el repo tiene `daca` como "
                       "`taíno-reconstruido` con la glosa 'mano' (desde el lokono daka). La forma que "
                       "Pané atestigua es `daca` 'yo'. No se toca nada aquí —esto propone—, pero el "
                       "par homógrafo tiene que decidirlo Miguel."),
        },
        {
            "morfema_caquetio": "-gua (locativo, 'región')",
            "capa_y_cita_caquetia": ("reconstruido, `deuda: sin-procedencia` (d21.7 → B, 2026-09-21). "
                                     "Su único apoyo escrito es «Topónimos venezolanos de Falcón y "
                                     "Sucre»; el canon lo sostiene con paragua = para 'mar' + -gua"),
            "candidato_taino": "gua- prefijo de nombres propios; y el -wa de bara-wa 'mar'",
            "que_fuente_lo_afirma": ("brinton-1871 p. impresa 12, s.v. Gua: «a very frequent prefix», "
                                     "citando a Pedro Mártir (Decad. p. 285) sobre que casi ningún "
                                     "nombre de rey empieza sin él; oliver-1989-cap2 p. 147: «/wa- "
                                     "[gua-]/ is a third person plural marker». Y p. 150 da el taíno "
                                     "bara-wa 'mar' junto al caquetío para-"),
            "veredicto": ("DOS MORFEMAS DISTINTOS con la misma sílaba — pero el bara-wa taíno es el "
                          "mejor cabo suelto que tiene la campaña de -gua"),
            "por_que": ("El gua- taíno que documentan Brinton y Oliver es un PREFIJO (3ª plural / "
                        "formante de nombres propios); el -gua caquetío del canon es un SUFIJO "
                        "locativo. Misma sílaba, posición contraria, función contraria: contar el uno "
                        "como apoyo del otro sería la trampa de -kana. Lo que SÍ es paralelo real es "
                        "otra cosa: taíno bara-wa 'mar' y caquetío para-gua tienen la misma raíz "
                        "'mar' y el mismo elemento detrás. Eso no prueba la glosa 'región', pero es "
                        "la primera pista independiente que la campaña d21.7 tiene."),
        },
        {
            "morfema_caquetio": "-bana (locativo, 'cerro, sitio alto')",
            "capa_y_cita_caquetia": ("ATESTIGUADO, D9 resuelta con seis apoyos: zavala-reyes-2015 #26, "
                                     "gonzalez-batista-nombre-de-coro, velasco-2015-resistencia"),
            "candidato_taino": "Agüey-bana (antropónimo) y pana-pe(n) 'fruto del pan'",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 148: «Taíno, for example, has pana-pe(n) for "
                                     "'breadfruit' and Agüey-bana as an anthroponym»"),
            "veredicto": "MISMO FORMANTE, GLOSA DISTINTA — y la distinta es la nuestra",
            "por_que": ("Oliver pone el -bana caquetío, el -bana/-pana taíno, el a-pana guajiro 'hoja' "
                        "y el -bana lokono 'techo' bajo una misma glosa: 'rodear, cubrir, extensión'. "
                        "El canon del proyecto le dio a -bana 'cerro, sitio alto' (D9) con apoyo "
                        "caquetío propio. Las dos cosas pueden convivir —la nota ya deja viva la "
                        "lectura 'ancho/llano' de van Buurt para kabana, darubana y guacaubana— pero "
                        "el paralelo taíno NO corrobora D9: empuja al otro lado."),
        },
        {
            "morfema_caquetio": "-coa / -bakoa (postposición toponímica)",
            "capa_y_cita_caquetia": ("-bacoa ATESTIGUADO (morfemas.yaml morfema-001: cinco topónimos "
                                     "glosados de Esteves 1989 + alvarado-1921 vía van-buurt-2014 §10); "
                                     "migra a -bakoa con el corte, d21.14 A"),
            "candidato_taino": "coa 'palo cavador'; barbacoa",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 149: «Taíno has the noun coa for the digging "
                                     "stick»; brinton-1871 p. impresa 11 s.v. Barbacoa: «a loft for "
                                     "drying maize», del arahuaco burrabakoa «a place for storing "
                                     "provisions»"),
            "veredicto": "NO ES EL MISMO MORFEMA — el coa taíno es un NOMBRE, no una postposición",
            "por_que": ("Oliver trae el coa taíno como apoyo SEMÁNTICO de que la postposición arahuaca "
                        "-coa se aplica a lo puntiagudo, no como paralelo morfológico: un palo cavador "
                        "es un sustantivo. Y barbacoa lo avisa el propio Oliver p. 151: «one must be "
                        "careful about some terms (e.g. barbacoa) offered by the Spanish as 'native' "
                        "Caquetío». Es tainismo llegado con el castellano, no herencia compartida."),
        },
        {
            "morfema_caquetio": "-(h)o nominalizador solemne · gentilicio -ío",
            "capa_y_cita_caquetia": ("NO está en TODAS_LAS_REGLAS: el motor no lo tiene. Es dato de "
                                     "oliver-1989-cap2 pp. 146-148, que lo ve en diao, datihao, "
                                     "boratio y en el propio kaket-ío"),
            "candidato_taino": "-hu/-o taíno-lokono; y los gentilicios Luca-yo, Cigüa-yo",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 147: el sufijo nominalizador solemne /-(h)o/ "
                                     "«characteristic of both Taíno and Lokono»; y la n. 44 p. 148 "
                                     "atribuye la serie -ío/-yo a Gary Vescelius, **comunicación "
                                     "personal de 1982**: «Luca-yo, Cigüa-yo, Kaket-ío»"),
            "veredicto": "PLAUSIBLE PARA -(h)o · NO CITABLE PARA -ío/-yo",
            "por_que": ("El nominalizador lo afirma Oliver en su propio texto y con ejemplos de las "
                        "dos lenguas. La serie de gentilicios, en cambio, es una comunicación personal "
                        "en nota al pie: no hay dato publicado detrás, no hay lista, y Lucayo y "
                        "Ciguayo son exónimos coloniales. Es sugerente y NO es evidencia; escribirlo "
                        "como apoyo sería inventar una clave foránea."),
        },
        {
            "morfema_caquetio": "-(i)tiao / -ati de parentesco y alianza",
            "capa_y_cita_caquetia": ("`datihao` está en el lexicón como caquetío-atestiguado; también "
                                     "`boratio` 'chamán' y `dato` 'fruto del cardón'"),
            "candidato_taino": "guatiao / waitiao / watiao 'amigo, aliado'",
            "que_fuente_lo_afirma": ("oliver-1989-cap2 p. 147, citando a Las Casas [1552] 1929 II:291 "
                                     "sobre el trueque de nombres entre Ponce de León y el cacique "
                                     "Agueybana; brinton-1871 p. impresa 12 s.v. Guatiao «friend, "
                                     "companion», del arahuaco ahati"),
            "veredicto": ("MISMO MORFEMA según Oliver — pero es EL caso que la skill §8 manda tratar "
                          "con cuidado"),
            "por_que": ("Oliver escribe «This Taíno term is cognate to Caquetio daitiao». Y en la n. 42 "
                        "de la p. 146 DUDA de que datihao sea caquetío: Oviedo hablaba de «los indios "
                        "de la Provincia de Venezuela» en general y su larga residencia en La Española "
                        "pudo hacerle usar taíno; concluye que probablemente fuera «equally shared by "
                        "both Taíno and Caquetío». O sea: la voz más taína del caquetío puede ser "
                        "taína a secas. Y Jahn, que parecía corroborarla, cita el mismo apéndice de "
                        "Oviedo. El lexicón sigue teniéndola como caquetío-atestiguado sin la reserva."),
        },
        {
            "morfema_caquetio": "ni- / nitaíno (prefijo pronominal)",
            "capa_y_cita_caquetia": "el caquetío no declara ningún ni-",
            "candidato_taino": "nitaíno 'noble, principal'",
            "que_fuente_lo_afirma": "nadie: brinton-1871 p. impresa 14 lo DESMIENTE",
            "veredicto": "🔴 FALSO — la fuente del repo rechaza expresamente el análisis",
            "por_que": ("Brinton, sobre nitainos: «There is not the slightest authority for this, nor "
                        "for supposing, with Von Martius, that the first syllable is a pronominal "
                        "prefix». Lo deriva del arahuaco nuddan 'estar firme, hacer algo bien'. El "
                        "análisis ni- + taíno ya estaba descartado en 1871 por la misma obra de donde "
                        "el lexicón sacó sus voces taínas."),
        },
        {
            "morfema_caquetio": "-bo / -abo (formante toponímico)",
            "capa_y_cita_caquetia": ("Oliver cap. 2 p. 148 lo lista como «(e)-bo» entre los sufijos más "
                                     "comunes de la toponimia caquetía; el canon del proyecto NO lo "
                                     "tiene ni en morfemas.yaml ni en TODAS_LAS_REGLAS"),
            "candidato_taino": "—",
            "que_fuente_lo_afirma": ("nadie lo afirma del taíno en el repo. La sonda sobre los lemas de "
                                     "Brinton dice cuántos acaban en -bo (ver `medido`)"),
            "veredicto": "SIN PAREJA — y además es un hueco del propio canon caquetío",
            "por_que": ("Oliver lo declara para el caquetío y el proyecto nunca lo recogió; el taíno "
                        "no tiene quien lo afirme. La fila existe para que el hueco quede escrito "
                        "(regla 8: el hueco se admite, callarlo no)."),
        },
    ]
    return {"medido": medido, "filas": filas}


# ═════════════════════════════════════════════════════════════════════════
# Onomástica
# ═════════════════════════════════════════════════════════════════════════
def bloque_onomastica():
    T = yaml.safe_load(io.open(YAML_TOPONIMOS, encoding="utf-8"))
    A = yaml.safe_load(io.open(YAML_ANTROPONIMOS, encoding="utf-8"))
    vivos = [t for t in T["toponimos"] if t.get("nivel") != "descartado"]
    descartados = [t for t in T["toponimos"] if t.get("nivel") == "descartado"]
    f_vivos = sorted({str(t["forma"]).lower() for t in vivos})
    f_todos = sorted({str(t["forma"]).lower() for t in T["toponimos"]})
    f_antrop = sorted({str(a["forma"]).lower() for a in A["antroponimos"] if a.get("forma")})
    pane = onomastica_pane()
    f_pane = sorted(pane)

    # el contraste lado a lado, que es lo que contesta la pregunta onomástica
    corpus = [("topónimos caquetíos sin descartar", f_vivos),
              ("antropónimos caquetíos propuestos", f_antrop),
              ("onomástica taína de Pané (sonda)", f_pane)]
    contraste = {}
    for nombre, patron in SONDAS_PREFIJO + SONDAS_SUFIJO:
        fila = {}
        for etiqueta, formas in corpus:
            n = sum(1 for f in formas if re.search(patron, f))
            fila[etiqueta] = (f"{n}/{len(formas)}"
                              + (f" ({n / len(formas):.0%})" if formas else ""))
        contraste[nombre] = fila

    # los topónimos que Esteves atribuye a taíno / «caribe insular»
    atribuidos = sorted({str(t["forma"]) for t in T["toponimos"]
                         if re.search(r"ta[ií]n|caribe insular", str(t.get("clase", "")) +
                                      str(t.get("razon", "")) + str(t.get("observacion", "")), re.I)})
    return {
        "insumos": {
            "toponimos_en_canon": len(T["toponimos"]),
            "toponimos_sin_descartar": len(vivos),
            "toponimos_descartados": len(descartados),
            "antroponimos_propuestos": len(f_antrop),
            "formantes_antroponimicos_declarados": [f["formante"] for f in A["formantes"]],
            "onomastica_de_pane_tokens": len(f_pane),
        },
        "contraste_de_formantes": {
            "que_es": ("la misma sonda sobre los tres corpus onomásticos, lado a lado. Es lo que "
                       "contesta la pregunta: no si un formante existe en los dos sitios —con "
                       "listas de fonología parecida casi todo existe en los dos sitios— sino si "
                       "aparece en la misma proporción."),
            "como_leerlo": ("una proporción parecida no prueba nada por sí sola; una MUY distinta, "
                            "o un cero limpio contra un 20 %, sí dice algo. Y ningún número de aquí "
                            "es un morfema: una sonda cuenta sílabas en posición, y la tabla de "
                            "`morfologia` es la que dice si detrás hay morfema."),
            "⚠️_el_sesgo_que_hay_que_descontar": (
                "los tres corpus no son del mismo género. El caquetío sin descartar es sobre todo "
                "TOPONIMIA (nombres de sitio de Falcón y Paraguaná) y la sonda de Pané es sobre todo "
                "ANTROPONIMIA y nombres de mito de La Española. Parte de la diferencia es de género, "
                "no de lengua: que -bana y -coa —que son formantes de LUGAR— den cero en Pané puede "
                "medir que Pané casi no nombra lugares. La columna de antropónimos caquetíos es la "
                "que sí compara género con género, y es la que da los ceros más limpios: 0 de 48 en "
                "-ex y 0 de 48 en -el contra 6 % y 21 % en Pané."),
            "tabla": contraste,
        },
        "formantes_en_la_toponimia_caquetia": {
            "sin_descartar": _sondar(f_vivos, SONDAS_SUFIJO + SONDAS_PREFIJO),
            "canon_entero_incluidos_descartados": _sondar(f_todos, SONDAS_SUFIJO + SONDAS_PREFIJO),
        },
        "formantes_en_los_antroponimos_caquetios": _sondar(f_antrop, SONDAS_SUFIJO + SONDAS_PREFIJO),
        "sonda_onomastica_taina_sobre_pane": {
            "que_es": ("SONDA de formantes, no censo — el censo de las fuentes taínas es de otro "
                       "escriba. Regla: token capitalizado de 4+ letras que no abra oración y no esté "
                       "en la lista de bloqueo declarada."),
            "advertencia": ("el texto es la retraducción castellana de la versión italiana de Ulloa "
                            "(1571): cada nombre pasó por dos copistas y una imprenta veneciana. Vale "
                            "para contar formantes, no para citar una forma como exacta."),
            "tokens": len(f_pane),
            "los_mas_frecuentes": [f"{w} ×{n}" for w, n in pane.most_common(25)],
            "formantes": _sondar(f_pane, SONDAS_SUFIJO + SONDAS_PREFIJO),
        },
        "el_estrato_taino_de_esteves": {
            "topónimos_del_canon_con_la_atribución": atribuidos,
            "lo_que_ya_dice_el_repo": (
                "4-fuentes/esteves-1989.md §6: la atribución de Amuay, Elegüey, Maragüey, Jamaica y "
                "Maitiruma al «caribe insular»/taíno es de Esteves y sale de PARECIDO DE SONIDO sin "
                "documento — «por su fonética la voz pertenece al caribe insular, como batey, mamey, "
                "caney, carey» (p. 14), y esas cuatro son voces taínas del español general."),
            "lo_que_este_cruce_añade": (
                "la serie -ey de Esteves es del castellano que llegó con los españoles vía La "
                "Española, no de un contacto taíno-caquetío precolonial: batey, mamey, caney y carey "
                "entran en el castellano antillano antes de que nadie escriba un topónimo de "
                "Paraguaná. Es el mismo aviso que Oliver da para maraca, cacique y barbacoa (p. 151). "
                "Un -ey en Paraguaná mide la boca del cronista, no la lengua del sitio."),
            "y_la_etiqueta_esta_mal_puesta": (
                "el caribe insular de Breton es una lengua ARAHUACA (iñeri) con préstamos caribes en "
                "el habla de los hombres, hermana del taíno y del caquetío — ya está escrito en "
                "4-fuentes/esteves-1989.md. Una coincidencia con él es parentesco de familia."),
        },
        "los_gentilicios_en_-io_-yo": {
            "la_afirmacion": "Luca-yo, Cigüa-yo, Kaket-ío comparten un formante de etnónimo",
            "de_donde_sale": ("oliver-1989-cap2 n. 44 p. 148, y Oliver la atribuye a Gary Vescelius, "
                              "**comunicación personal de 1982**"),
            "veredicto": ("NO CITABLE como evidencia. No hay dato publicado detrás, no hay lista, y "
                          "Lucayo y Ciguayo son exónimos coloniales recogidos por cronistas. Que "
                          "`kaketío` sea `kake-` + `-(h)o` sí lo argumenta Oliver aparte, con el "
                          "lokono kakïtho (p. 148) — ese es el apoyo bueno, y no necesita a Vescelius."),
        },
    }


# ═════════════════════════════════════════════════════════════════════════
# La pregunta de clasificación
# ═════════════════════════════════════════════════════════════════════════
def bloque_clasificacion():
    return {
        "advertencia_de_entrada": (
            "El caquetío atestiguado son ~228 entradas de lexicón y ~78 topónimos sin descartar, "
            "casi todo fitonimia y zoonimia de Paraguaná y Coro recogida por Zavala. Del taíno el "
            "repo tiene 43 voces atestiguadas y **ninguna con `procedencia.obra`**. Eso NO da para "
            "una clasificación y este cruce no la intenta. Oliver, que tenía más, llama «tentative» "
            "a la suya y dice que del caquetío no hay medición porque no existe lista de 100 palabras."),
        "posiciones": [
            {"quien": "Oliver 1989 (cap. 2, pp. 150-155)",
             "que_dice": ("el caquetío sale del mismo fondo que el lokono, no de una ascendencia "
                          "guajiro-paraujana; y hace salir a lokono, island carib, taíno y caquetío "
                          "del mismo nodo"),
             "cita": "«strongest affinities with Lokono» (p. 155)",
             "en_que_se_apoya": ("DATOS: el prefijo /dA-/ de 1ª sg. (sólo lokono y taíno lo tienen), "
                                 "la innovación léxica auri 'perro', kaketío = lokono kakïtho, y "
                                 "-bana frente a -pana"),
             "y_en_que_no": ("en GEOGRAFÍA cuando descarta al guajiro: «a preliminary examination of "
                             "selected Guajira-Falcón toponyms» (p. 150) — preliminar, y sin lista"),
             "lo_llama": "«tentative» él mismo"},
            {"quien": "Noble 1965 (vía Oliver p. 97 y Rouse)",
             "que_dice": "el taíno es un vástago directo del proto-arahuaco, aislado",
             "cita": "—",
             "en_que_se_apoya": ("porcentajes de cognados sin lista publicada. Oliver: «Noble does not "
                                 "provide the actual word list(s) for Taíno, a major drawback»"),
             "y_en_que_no": "—",
             "lo_llama": "Oliver lo llama «misleading and ambiguous at the very best»"},
            {"quien": "Taylor 1977 (vía Oliver p. 97)",
             "que_dice": "el taíno deriva del proto-maipure, con 60 palabras comparadas",
             "cita": ("«Taíno appears to have [share] more lexical cognates with Island Carib than "
                      "Arawak [Lokono]», pero «borrowing cannot be excluded»"),
             "en_que_se_apoya": "DATOS, aunque pocos: una lista corta de 60 ítems",
             "y_en_que_no": "—",
             "lo_llama": "el propio Taylor deja abierto el préstamo"},
            {"quien": "Rouse 1986 (citado por Oliver p. 97)",
             "que_dice": "el taíno evolucionó del proto-norteño, como las demás del grupo",
             "cita": "«So little is known about the Taíno language that there is room for disagreement»",
             "en_que_se_apoya": "la opinión de Arróm y la escasez reconocida del dato",
             "y_en_que_no": "—",
             "lo_llama": "él mismo admite el desacuerdo"},
            {"quien": "Vescelius (comunicación personal 1982, en Oliver n. 44 p. 148)",
             "que_dice": "los etnónimos en -ío/-yo (Luca-yo, Cigüa-yo, Kaket-ío) van juntos",
             "cita": "—",
             "en_que_se_apoya": "NADA publicado: es una nota al pie de una conversación",
             "y_en_que_no": "—",
             "lo_llama": "«curious relationship»"},
        ],
        "que_puede_aportar_nuestro_material": [
            "confirmar o no que una voz caquetía atestiguada tiene pareja taína con la MISMA glosa, "
            "y de qué dominio es esa voz (que es lo que decide si el dato vale para filiación o para "
            "comercio);",
            "medir cuántas de esas parejas salen también por azar, que es lo que ninguna de las "
            "posiciones de arriba hizo;",
            "poner sobre la mesa los formantes que Oliver declara para el caquetío y que el canon del "
            "proyecto nunca recogió (-bo, -oa, -kiva), que son hueco propio antes que pregunta taína.",
        ],
        "que_NO_puede": [
            "medir distancia lexicoestadística: no hay lista de 100 palabras ni del caquetío ni del "
            "taíno, y Oliver lo dice de las dos;",
            "decidir dónde cae el caquetío en el árbol. Con 43 voces taínas sin procedencia, cualquier "
            "número que salga de aquí mide nuestras dos listas, no las dos lenguas;",
            "usar el taíno como prueba a favor o en contra de D11: el prefijo /dA-/ que comparten "
            "taíno y caquetío lo comparte también el lokono, y por eso el argumento ya está contado "
            "en D11. Contarlo otra vez por la vía taína sería contar dos veces el mismo dato.",
        ],
    }


# ═════════════════════════════════════════════════════════════════════════
# Salida
# ═════════════════════════════════════════════════════════════════════════
def ficha_de(e, cb, sim):
    d = dict(e["ficha"])
    d["comparado_como"] = cb[0] + (" (radical)" if cb[2] else "")
    d["similitud"] = round(sim, 3)
    return d


def registro(r):
    c, por = r["c"], r["por"]
    p_nulo = p_nulo_de(r, "taíno")
    clase, porque_clase = clase_de_pareja(r, p_nulo)
    reg = {"caquetio": {"forma": c["clave"],
                        **({"forma_fuente": c["forma_fuente"]} if c["forma_fuente"] else {}),
                        "capa": c["capa"], "cat": c["cat"], "categoria": c["categoria"],
                        "dominio": c["dominio"], "glosa": c["sig"],
                        "fonemizada": " / ".join(fa for fa, _ in c["cands"])},
           "conceptos_exactos": sorted({cab for cab, ex, _ in c["conceptos"] if ex})}
    if c["derivada_de"]:
        reg["caquetio"]["forma_derivada_de"] = c["derivada_de"]
    for L in TODAS:
        p = por[L]
        if p["ranking"]:
            reg[L] = [ficha_de(e, cb, s) for s, e, cb, _ca in p["ranking"][: TOPES[L]]]
            if len(p["exactas"]) > TOPES[L]:
                reg[L].append({"mas_entradas_con_la_misma_glosa": len(p["exactas"]) - TOPES[L]})
    reg["similitud"] = {L: (round(por[L]["sim"], 3) if por[L]["ranking"] else None) for L in TODAS}
    reg["veredictos"] = {L: por[L]["veredicto"] for L in TODAS}
    reg["veredicto"] = por["taíno"]["veredicto"]
    if clase:
        reg["clase"] = clase
        reg["por_que_esa_clase"] = porque_clase
    if p_nulo is not None:
        reg["p_por_azar_taino"] = round(p_nulo, 3)
    candidatas = [(por[L]["sim"], L) for L in LENGUAS
                  if por[L]["veredicto"] in ("cognado-probable", "parecido-debil")]
    reg["se_parece_mas_a"] = max(candidatas)[1] if candidatas else "ninguna"
    trozos = []
    for L in TODAS:
        p = por[L]
        if p["ranking"]:
            s, e, cb, ca = p["ranking"][0]
            barato = (" (3 fonemas: parecido barato)"
                      if s >= UMBRAL_PARECIDO and min(len(cb[0]), len(ca[0])) <= MIN_FONEMAS else "")
            trozos.append(f"{L} {cb[1]} «{str(e['glosa'])[:36]}» {s:.2f}{barato}")
        elif p["porque"] and L == "taíno":
            trozos.append(f"{L}: {p['porque']}")
    extra = [f"{L}: {por[L]['porque']}" for L in TODAS if por[L]["veredicto"] == "circular"]
    if any(e["nota_mira_al_caquetio"] for _s, e, _cb, _ca in por["taíno"]["ranking"][:1]):
        extra.append("⚠️ la `notas` de la entrada taína se escribió mirando al caquetío: "
                     "la forma es de la fuente, la comparación no es independiente")
    reg["por_que"] = ("forma caquetía de menos de tres fonemas: no cuenta como evidencia"
                      if r["corto"] else " · ".join(trozos + extra))
    return reg


def construir(M, M2):
    resumen = resumir(M)
    resumen_sens = resumir(M2)
    res = M["res"]
    ates = [r for r in res if r["c"]["capa"] == ATESTIGUADO]

    clases = collections.Counter()
    parejas = []
    for r in ates:
        p_nulo = p_nulo_de(r, "taíno")
        clase, porque = clase_de_pareja(r, p_nulo)
        if not clase:
            continue
        clases[clase] += 1
        s, e, cb, ca = r["por"]["taíno"]["ranking"][0]
        parejas.append({
            "caquetio": r["c"]["clave"], "glosa_caquetia": r["c"]["sig"],
            "taino": e["forma"], "glosa_taina": e["glosa"],
            "fuente_caquetia": (r["c"]["notas"] or "")[:160] or "sin nota",
            "fuente_taina": e["ficha"]["estrato"],
            "comparado": f"{ca[0]} ~ {cb[0]}",
            "similitud": round(s, 3), "clase": clase, "por_que": porque,
            "dominio": r["c"]["dominio"],
            "p_por_azar": round(p_nulo, 3) if p_nulo is not None else None,
            "tambien_se_parece_en": [L for L in ("lokono", "wayunaiki", "achagua", "kalinago",
                                                 "paraujano", "jirajarano")
                                     if r["por"][L]["exactas"] and r["por"][L]["sim"] >= UMBRAL_PARECIDO],
        })
    parejas.sort(key=lambda p: (p["clase"], -p["similitud"], p["caquetio"]))

    # las circulares (capas reconstruidas): existen y no deciden
    circulares = []
    for r in res:
        for L in TODAS:
            if r["por"][L]["veredicto"] == "circular":
                s, e, cb, _ca = r["por"][L]["ranking"][0]
                circulares.append({"caquetio": r["c"]["clave"], "capa": r["c"]["capa"],
                                   "lengua": L, "comparanda": cb[1], "similitud": round(s, 3),
                                   "forma_derivada_de": r["c"]["derivada_de"]})
    circulares.sort(key=lambda d: (d["lengua"], -d["similitud"], d["caquetio"]))

    por_capa = collections.defaultdict(collections.Counter)
    for r in res:
        if r["por"]["taíno"]["exactas"]:
            por_capa[r["c"]["capa"]][r["por"]["taíno"]["veredicto"]] += 1

    taino_ates = M["lengs"]["taíno"]
    caq_ates = [r["c"] for r in ates]
    n_caq = collections.Counter(r["c"]["capa"] for r in res)
    comparables = [r for r in res if any(r["por"][L]["exactas"] for L in TODAS)]

    meta = {
        "campana": "la campaña del taíno — parcela T4: el cruce con el caquetío",
        "medido": FECHA,
        "script": "6-fusion/scripts/cruce_taino_caquetio.py",
        "estado": ("PROPUESTA (regla 5). No toca el lexicón, ni lexicon_*.py, ni 2-lengua/, ni "
                   "3-mundo/corpus/. Ningún cognado entra a cognados.yaml por este archivo. "
                   "Toda cifra de `meta` la emite el script (regla 1)."),
        "pregunta": ("¿Qué comparten de verdad el taíno y el caquetío ATESTIGUADO —léxico, "
                     "morfología, onomástica—, y qué de eso es herencia arahuaca común, qué "
                     "préstamo por contacto en la esfera, y qué casualidad?"),
        "el_limite_duro": {
            "que_es": ("las 52 entradas taínas del lexicón tienen 0 `procedencia.obra`. Las 43 "
                       "atestiguadas dicen «Brinton 1871» en `notas` y eso NO es una clave foránea "
                       "(regla 8): el validador no lo comprueba."),
            "taino_con_procedencia_obra": sum(
                1 for k, v in CL.VOCABULARIO_BASE.items()
                if str(v.get("fuente", "")).startswith("taíno") and v.get("procedencia")),
            "consecuencia": ("este cruce mide lo que el repo tiene HOY. Cuando entren las "
                             "transcripciones de Oviedo, Las Casas, Pané y Brinton se vuelve a "
                             "correr el script y las cifras cambian. Por eso es un script y no una "
                             "tabla."),
        },
        "por_que_solo_la_capa_atestiguada": (
            "las capas caquetío-reconstruido e -hipotético se fabricaron desde el wayuu y el lokono "
            "(arahuaco_comparative.REGLAS_*, las 441 candidatas con ~80 % de fallo). Cruzarlas con el "
            "taíno mediría el ANDAMIO, no el caquetío. Se miden y se emiten en `circulares`, y no "
            "entran en ningún resumen de filiación. Por la misma razón queda fuera `taíno-reconstruido`: "
            "9 formas que reconstruir_taino() generó desde el lokono, y cuyas propias notas dicen «no "
            "cuenta como dato taíno en cruces»."),
        "insumos": {
            "caquetio_por_capa": dict(sorted(n_caq.items())),
            "taino_atestiguado_usado": len(taino_ates),
            "taino_reconstruido_excluido": sum(
                1 for v in CL.VOCABULARIO_BASE.values() if v.get("fuente") == "taíno-reconstruido"),
            "taino_gemelas_castellanas_fusionadas": sorted(CL.FORMA_DE_LA_ESFERA),
            "taino_con_nota_escrita_mirando_al_caquetio": sorted(
                e["forma"] for e in taino_ates if e["nota_mira_al_caquetio"]),
            "taino_con_marca_castellana_declarada": sorted(
                e["forma"] for e in taino_ates if e["ficha"].get("marca_castellana")),
            **{f"{L}_entradas": len(M["lengs"][L]) for L in LENGUAS[1:] + INFORMATIVAS},
            "control_jirajarano": dict(M["meta_control"],
                                       filas_con_forma_comparable=len(M["lengs"][CONTROL])),
            "lo_que_NO_sirvio_de_control": medir_jirajaroide_frontera(),
        },
        "parametros": {
            "umbral_parecido": UMBRAL_PARECIDO, "umbral_cognado": UMBRAL_COGNADO,
            "min_fonemas": MIN_FONEMAS, "replicas_del_modelo_nulo": REPLICAS, "semilla": SEMILLA,
            "gu_es_w": GU_ES_W,
            "similitud": "difflib.SequenceMatcher.ratio() sobre la forma fonemizada",
            "afijos_probados": {L: {"prefijos": list(p), "sufijos": list(s)}
                                for L, (p, s) in sorted(AFIJOS.items())},
            "sinonimos_de_glosa": SINONIMOS_CRUDOS,
            "dominio_por_categoria": DOMINIO_POR_CATEGORIA,
            "de_donde_sale_la_tabla_de_dominios": (
                "skill minar-fuente §3, que viene de la corrección de Miguel del 2026-09-10: «hay "
                "palabras que pueden compartirse entre etnias». Lo que decide no es SI se comparte, "
                "sino QUÉ: plantas, bichos, mercancías y utensilios viajan entre lenguas sin "
                "parentesco (préstamo areal); pronombres, numerales y morfemas gramaticales casi "
                "nunca (dato de filiación)."),
        },
        "metodo": [
            "FILTRO DE SIGNIFICADO: se empareja por glosa castellana EXACTA (el segmento es una sola "
            "palabra en los dos lados, tras normalizar la ortografía colonial). Un parecido de forma "
            "sin filtro de significado es casi todo ruido: medido 5 falsos de 7 en el achagua.",
            "MIRAR LA CAPA: sólo la capa caquetío-atestiguado decide; las reconstruidas se emiten "
            "aparte como circulares. Y las entradas taínas cuya `notas` se escribió comparándolas con "
            "el caquetío llevan aviso — la forma es de la fuente, la comparación no es independiente.",
            "LA CLASE NO LA DECIDE EL PARECIDO: el parecido sólo abre la candidatura. La clase la "
            "deciden el DOMINIO de la voz y si el mismo concepto se parece también en las hermanas.",
            "DESCONFIAR: modelo nulo por permutación, control no arahuaco (jirajara/ayomán) y prueba "
            "de predicción dejando fuera. Una correspondencia con 1 o 2 apoyos no es una regla.",
        ],
        "capas_de_medicion": [
            "diacríticos fuera salvo ü y ñ (sin esto fonemizar borraba ū, ẽ, ë enteras)",
            "ortografía lingüística (lokono, wayuu, reconstruido): la h suelta pasa a j, porque "
            "fonemizar borra la h castellana",
            "curiana_fonotactica.fonemizar(); OJO: lleva <ch> a k y <sh> a s en todas por igual",
            "forma_comparable() colapsa las geminadas de Perea; se colapsan las repeticiones y ü -> u",
            "las cuatro claves castellanas con gemela indígena (casabe/cazabi, maíz/maisi, "
            "cacique/cacike, bohío/bohio) entran UNA vez, por la indígena: FORMA_DE_LA_ESFERA",
        ],
        "advertencias": [
            "Un parecido de forma con glosa exacta es un CANDIDATO a cognado, no un cognado. Ninguna "
            "de estas parejas ha pasado por correspondencias regulares verificadas.",
            "Las listas son cortas y muy distintas de dominio: el caquetío atestiguado es fitonimia y "
            "zoonimia de Paraguaná y Coro, y la lista taína de Brinton excluye a propósito «nearly "
            "all names of plants and animals» (p. impresa 11). El hueco mide las listas, no las lenguas.",
            "Los tainismos son préstamos panamericanos que llegaron con el castellano vía La Española. "
            "Oliver lo avisa para maraca, cacique y barbacoa (p. 151): «one must be careful about some "
            "terms offered by the Spanish as 'native' Caquetío».",
            "El caquetío atestiguado y el taíno de Brinton están los dos en ortografía castellana "
            "colonial: parte del parecido que salga es del transcriptor español, no de las lenguas. "
            "fonemizar() normaliza lo que puede y no lo resuelve.",
        ],
        "resumen_atestiguado": resumen,
        "reparto_por_clase": dict(sorted(clases.items())) or {
            "sin_parejas": ("ninguna voz caquetía atestiguada alcanza el umbral con una voz taína "
                            "de la misma glosa: no hay nada que clasificar. Ver "
                            "`auditoria_del_cero`, que es donde está el resultado.")},
        "auditoria_del_cero": {
            "por_que_este_bloque": (
                "regla 6: un cero mide la consulta hasta que se verifica. Con cuatro conceptos "
                "comparables, los cuatro casos SON el resultado y van uno a uno; y hay que decir "
                "qué descartó el filtro y qué tiene el canon que el cruce no ve."),
            "los_conceptos_comparables_uno_a_uno": bloque_los_comparables(M),
            "descartados_por_glosa_solo_cercana": bloque_glosa_cercana(M),
            "cognados_CQ_TN_ya_declarados_en_el_canon": bloque_cognados_ya_declarados(GU_ES_W),
            "hallazgos_de_etiqueta": bloque_hallazgos_de_etiqueta(GU_ES_W),
            "paso_por_forma_sin_filtro_de_glosa": paso_por_forma(M, GU_ES_W),
        },
        "sensibilidad_gu_es_w_true": {
            L: {k: resumen_sens["por_lengua"][L].get(k)
                for k in ("conceptos_comparables", "parecidos_ge_umbral",
                          "cognado_probable_ge_umbral_cognado")}
            | {"parecidos_esperados": resumen_sens["por_lengua"][L].get("azar", {}).get("parecidos_esperados")}
            for L in TODAS},
        "veredicto_taino_por_capa": {k: dict(sorted(v.items())) for k, v in sorted(por_capa.items())},
        "morfologia": bloque_morfologia(M, caq_ates, taino_ates),
        "onomastica": bloque_onomastica(),
        "clasificacion": bloque_clasificacion(),
        "prueba_de_prediccion": prueba_dejando_fuera(M, ("taíno", "lokono", "wayunaiki", "achagua")),
        "circulares": circulares,
        "registros": {
            "conceptos_con_glosa_exacta_en_alguna_lengua": len(comparables),
            "sin_concepto_en_ninguna_comparanda": len(res) - len(comparables),
        },
    }
    rango = {"cognado-probable": 0, "parecido-debil": 1, "circular": 2,
             "sin-parecido": 3, "no-comparable": 4}
    comparables.sort(key=lambda r: (r["c"]["capa"] != ATESTIGUADO, r["c"]["capa"],
                                    rango[r["por"]["taíno"]["veredicto"]],
                                    -r["por"]["taíno"]["sim"], r["c"]["clave"]))
    return {"meta": meta, "parejas": parejas, "conceptos": [registro(r) for r in comparables]}


CABECERA = (
    "# ══════════════════════════════════════════════════════════════════════\n"
    "# CRUCE TAÍNO <-> CAQUETÍO ATESTIGUADO — campaña del taíno, parcela T4\n"
    "# PROPUESTA (regla 5). Generado por 6-fusion/scripts/cruce_taino_caquetio.py:\n"
    "# no se edita a mano; se corrige el script o sus insumos y se regenera.\n"
    "# Toda cifra de `meta` la emite el script (regla 1).\n"
    "# Re-ejecutable: cuando entren las transcripciones de Oviedo, Las Casas,\n"
    "# Pané y Brinton con su `procedencia.obra`, se vuelve a correr.\n"
    "# ══════════════════════════════════════════════════════════════════════\n"
)


def texto_yaml(salida):
    buf = io.StringIO()
    buf.write(CABECERA)
    yaml.safe_dump(salida, buf, allow_unicode=True, sort_keys=False, width=110)
    return buf.getvalue()


def consola(salida):
    m = salida["meta"]
    print("\n═══ RESUMEN, capa caquetío-atestiguado ═══")
    for L, d in m["resumen_atestiguado"]["por_lengua"].items():
        az = d.get("azar", {})
        print(f"  {L:<12} entradas {d['entradas_de_la_lengua']:>5} · comparables {d['conceptos_comparables']:>3}"
              f" · parecidos {d['parecidos_ge_umbral']:>2} (azar {az.get('parecidos_esperados')},"
              f" p={az.get('p_parecidos_ge_observado')}) · cognado-probable {d['cognado_probable_ge_umbral_cognado']}"
              f" · sim media {d['similitud_media']} (azar {az.get('similitud_media_esperada')})")
    print(f"\n  reparto por clase: {list(m['reparto_por_clase'])}")
    print("\n═══ PAREJAS TAÍNO ~ CAQUETÍO ATESTIGUADO ═══")
    for p in salida["parejas"]:
        print(f"  [{p['clase']:<18}] {p['caquetio']:<12} «{str(p['glosa_caquetia'])[:26]:<26}» ~ "
              f"{p['taino']:<12} {p['similitud']:.2f}  azar p={p['p_por_azar']}  "
              f"también: {','.join(p['tambien_se_parece_en']) or '—'}")
    aud = m["auditoria_del_cero"]
    print("\n═══ AUDITORÍA DEL CERO ═══")
    for d in aud["los_conceptos_comparables_uno_a_uno"]:
        print(f"  {d['concepto']} · caq {d['caquetio']:<10} ~ tno {d['taino']:<10} {d['similitud']:.2f}")
    print(f"  descartados por glosa sólo cercana: {len(aud['descartados_por_glosa_solo_cercana'])}")
    cg = aud["cognados_CQ_TN_ya_declarados_en_el_canon"]
    print(f"  cognados.yaml ya empareja CQ~TN en {cg['sets_con_CQ_y_TN']} sets: {cg['reparto']}")
    he = aud["hallazgos_de_etiqueta"]
    print(f"  «Taíno atestiguado» en taino_hipotetico.json sin la etiqueta taíno en el lexicón: "
          f"{he['de_esas_sin_la_etiqueta_taino_en_el_lexicon']} de "
          f"{he['declaradas_atestiguadas_en_el_json']}")
    print("  paso por forma (sin filtro de glosa):")
    for L, d in aud["paso_por_forma_sin_filtro_de_glosa"]["por_lengua"].items():
        print(f"    {L:<12} parejas {d['parejas_de_forma_ge_umbral']:>3} · con glosa "
              f"{d['de_esas_con_la_glosa_tambien']:>2} · ruido {d['ruido']:>3}")
    print("\n═══ MORFOLOGÍA ═══")
    for f in m["morfologia"]["filas"]:
        print(f"  {f['morfema_caquetio']:<44} {f['veredicto']}")
    print("\n═══ PREDICCIÓN (dejando fuera) ═══")
    for L in ("taíno", "lokono", "wayunaiki", "achagua"):
        b = m["prueba_de_prediccion"][L]
        print(f"  [{L}] {b['pares_parecidos']} pares parecidos · {b['correspondencias_distintas']} "
              f"correspondencias · {b['con_tres_apoyos_o_mas']} con 3 apoyos o más")
        for rg in b["reglas"][:4]:
            print(f"    {rg['regla']:<18} apoyos {rg['apoyos']} · {rg['aciertos']}/{rg['aplicables']}"
                  f" (tasa {rg['tasa_de_acierto']}, azar {rg['tasa_por_azar']}) · {rg['juicio'][:60]}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--check", action="store_true",
                    help="no escribe: dice si el YAML del repo está al día")
    args = ap.parse_args(argv)

    print("midiendo (gu_es_w=False) ...")
    M = medir(GU_ES_W)
    print(f"  {M['segundos']} s")
    print("midiendo la sensibilidad (gu_es_w=True) ...")
    M2 = medir(not GU_ES_W)
    print(f"  {M2['segundos']} s")

    salida = construir(M, M2)
    nuevo = texto_yaml(salida)

    if args.check:
        viejo = io.open(SALIDA, encoding="utf-8").read() if os.path.exists(SALIDA) else ""
        if viejo == nuevo:
            print(f"\n✓ {os.path.relpath(SALIDA, R)} está al día")
            return 0
        print(f"\n✗ {os.path.relpath(SALIDA, R)} DESFASADO: re-ejecuta el script sin --check")
        return 1

    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(nuevo)
    consola(salida)
    print(f"\n✓ {os.path.relpath(SALIDA, R)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
