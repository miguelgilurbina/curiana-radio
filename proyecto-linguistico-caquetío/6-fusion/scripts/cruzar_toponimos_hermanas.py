# -*- coding: utf-8 -*-
"""
Cruce de los topónimos caquetíos sin lectura con las hermanas y las primas
(2026-10-10). El pase que Miguel aprobó ese día y que nunca se había hecho.

Tres partes, las tres PROPUESTA (regla 5): no toca 2-lengua/, curiana_sim/,
3-mundo/ ni ningún YAML generado.

  Parte 1 — `-ana`. Qué hace -ana (o -na tras raíz en -a) en los nombres de
            las hermanas y las primas CON GLOSA DE FUENTE. Las lecturas se
            hicieron a mano sobre la capa de texto (página localizada, cita
            corta) y van declaradas abajo en `ANA`; el script MIDE lo que es
            contable (cuántas voces en -ana tiene cada lengua del lexicón y
            cuántas mencionan un lugar en la glosa; cuántas -ana tiene el
            manuscrito achagua y qué notas de topónimo dejó su escriba; cómo
            escribe cada obra «Guayana» y en cuántas hay algo con aire de
            etimología) para que ninguna cifra vaya a mano (regla 1).

  Parte 2 — el cruce general. Para cada topónimo del canon en nivel C o
            `descartado`: se quitan las terminaciones de lugar ya declaradas,
            la raíz que queda se busca en el lexicón caquetío, en las
            hermanas (lokono, taíno, kalinago), en las primas (achagua,
            wayuu, paraujano) y en las voces vivas de Medina, y un par SOLO
            cuenta si la glosa de la voz cae en el mismo campo que el
            referente del lugar (filtro de significado, skill `minar-fuente`
            §2: sin él, 5 de 7 «aciertos» eran falsos con el achagua). Dos
            controles de azar con las mismas raíces y los mismos umbrales:
              (a) PERMUTACIÓN DE GLOSAS dentro de cada lengua: la forma queda
                  donde está y su glosa se baraja; mide cuántos pares da el
                  parecido de forma con un significado cualquiera;
              (b) PERMUTACIÓN DE REFERENTES entre topónimos: cada lugar
                  recibe el referente de otro; mide cuántos pares da el
                  filtro con un lugar cualquiera.
            Se reporta, por lengua, observados frente a la media y el p95 del
            azar, y la fracción de réplicas que igualan o superan lo observado.
            Y una sensibilidad: (c) UNA VOZ POR FAMILIA (misma lengua, mismos
            cuatro primeros fonemas del radical), porque una lengua con muchas
            entradas sobre una raíz (el achagua) gana pares que no son cognados.
            El kalinago de Goeje se parte en dos: lo que él marca K (kalina,
            caribe) es una VECINA; lo arahuaco y el habla de mujeres, la hermana.

  Fauna y flora en -re: para cada voz caquetía en -re que nombra un animal o
            una planta, la voz de las hermanas y primas con LA MISMA glosa, y
            cuánto se parece.

Salida: 6-fusion/cruce_toponimos_hermanas_2026-10-10.yaml

    python 6-fusion/scripts/cruzar_toponimos_hermanas.py
"""
import collections
import difflib
import io
import os
import random
import re
import statistics
import sys
import unicodedata

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL  # noqa: E402
from curiana_fonotactica import fonemizar, forma_comparable  # noqa: E402
from lexicon_perea import COMPARANDA_LOKONO  # noqa: E402

FECHA = "2026-10-10"
SALIDA = os.path.join(R, "6-fusion", "cruce_toponimos_hermanas_2026-10-10.yaml")
F = lambda *p: os.path.join(R, *p)  # noqa: E731

# ── parámetros declarados ANTES de mirar resultados ──────────────────────
UMBRAL_PARECIDO = 0.62      # el de cruzar_jahn_guajiro.py y cruzar_achagua_caquetio.py
UMBRAL_COGNADO = 0.75
MIN_FONEMAS = 3             # dos letras no son evidencia
REPLICAS = 300
SEMILLA = 20261010
GU_ES_W = False             # defecto de curiana_fonotactica
NIVELES = ("C", "descartado")

LINEA = {   # 3-mundo/hermanas/README.md §2 (Miguel, 2026-10-09)
    "lokono": "hermana (lokonoide)", "taíno": "hermana (lokonoide)",
    "kalinago": "hermana (lokonoide, por el sustrato iñeri)",
    "kalinago-caribe": "vecina (el estrato kalina —caribe— del caribe insular: Goeje lo marca K)",
    "achagua": "prima (orinoco-llanos)", "wayunaiki": "prima (guajiro-paraujana)",
    "paraujano": "prima (guajiro-paraujana)",
    "caquetío": "la propia lengua", "medina": "voz viva (Medina Colina, s. XX)",
}
HERMANAS = ("lokono", "taíno", "kalinago")
PRIMAS = ("achagua", "wayunaiki", "paraujano")

# ═════════════════════════════════════════════════════════════════════════
# Terminaciones de lugar ya declaradas (paso 1). Cada una dice de dónde sale.
# ═════════════════════════════════════════════════════════════════════════
SUFIJOS = [  # (forma fonemizada, de dónde)
    ("ubana", "REGLAS_ZAVALA -ubana"), ("bana", "-bana, D9/#38"),
    ("bakoa", "morfema-001 / REGLAS_TOPONIMICAS"), ("akoa", "-bacoa con haplología (quibacoas)"),
    ("koa", "Oliver 1989 cap. 2 p. 148 (-coa)"), ("oa", "Oliver 1989 cap. 2 p. 149 / TODAS_LAS_REGLAS"),
    ("kiba", "kiba 'piedra' (lexicón; Jadacaquiva, Tiquiba)"), ("kiwa", "quigua (kiwa) 'concha'"),
    ("ebo", "ebo 'camino' (lexicón)"), ("bo", "Oliver 1989 p. 148 (e)-bo"),
    ("are", "morfema-002"), ("ure", "ure 'raíz' (Esteves) / censo -re"),
    ("ire", "censo -re"), ("ore", "censo -re"), ("re", "censo -re"),
    ("iana", "-iana (Chamuriana, Curiana)"), ("ana", "morfema-011"), ("na", "-ná (Paraguaná)"),
    ("gua", "-wa / -gua (Oliver p. 148)"), ("wa", "-wa (TODAS_LAS_REGLAS)"),
    ("aima", "REGLAS_ZAVALA"), ("ima", "REGLAS_ZAVALA"), ("iro", "REGLAS_ESTEVES"),
    ("uko", "REGLAS_ESTEVES -uco"), ("uto", "-uto, variante de -uco"),
    ("uru", "REGLAS_ZAVALA"), ("dito", "-dito colectivo (Esteves)"), ("dite", "-dite (Cocodite)"),
    ("si", "-shi/-chi (morfema-007, fonemizado)"), ("ri", "-ari/-ri (morfema-008)"),
    ("kuri", "morfema-009"), ("bari", "morfema-010"),
    ("al", "colectivo castellano -al"), ("ito", "diminutivo castellano"),
    ("itos", "diminutivo castellano"), ("s", "plural castellano"),
]
PREFIJOS = [("a", "prótesis (adaure)"), ("gua", "wa- (morfema-006)"), ("wa", "wa- (morfema-006)"),
            ("ka", "ka- atributivo"), ("ma", "ma- privativo")]
VOCALES = set("aeiou")

# ═════════════════════════════════════════════════════════════════════════
# Campos de significado (paso 3). Escritos uno por uno y auditables; las
# palabras van en castellano, inglés y francés porque las glosas de Goeje y de
# la lista taína vienen así. Ningún campo es «lugar» o «pueblo»: todos los
# topónimos lo son y casarían con todo.
# ═════════════════════════════════════════════════════════════════════════
CAMPOS = {
    # paisaje
    "cerro": ("cerro loma lomas colina colinas serrania sierra montana morro penon cumbre cuesta cerros",
              "cerro loma colina montana sierra pena cumbre hill mountain montagne morne"),
    "agua_dulce": ("laguna lagunas estanque jaguey pozo manantial aguada represa charca cienaga pantano agua",
                   "laguna lago charca pozo manantial fuente agua cienaga pantano lake pond spring water swamp eau etang source marais"),
    "rio": ("rio quebrada cano arroyo riachuelo cauce vertiente desagua quebrajon",
            "rio quebrada arroyo cano cauce river creek stream riviere ruisseau"),
    "mar_costa": ("punta cabo ensenada bahia playa costa costeno puerto golfete golfo mar orilla litoral isla islote cayo",
                  "mar playa orilla costa punta cabo bahia isla sea beach shore coast island mer plage cote ile isle"),
    "salina": ("salina salinas salineta sal", "sal salina salado salt sel sale"),
    "llano": ("sabana sabanas llano llanura llanos planicie vega", "sabana llano llanura vega savanna plain plaine savane"),
    "monte": ("monte bosque boscoso frondoso arboleda", "bosque monte selva arboleda forest wood woods foret bois"),
    "piedra": ("piedra piedras roca rocas rocoso pedregal pedruzco cristales cuarzo cueva caverna cavernosas cavernoso",
               "piedra roca pedregal cueva caverna stone rock cave pierre roche caverne grotte"),
    "arena": ("arena arenas arenal arenales arenoso medano medanos duna", "arena arenal medano sand sable"),
    "barro": ("barro arcilla greda lodo", "barro arcilla lodo clay mud argile boue"),
    "viento": ("viento ventoso ventarron brisa", "viento ventarron wind vent"),
    "camino": ("camino paso sendero vereda", "camino senda sendero path road chemin"),
    # lo vivo
    "arbol": ("arbol arboles arbusto arbustos planta palma palmera cardon cardonal cactus cardo yabo cuji guayacan",
              "arbol arbusto planta palma palmera cactus cardon cardo tree shrub plant palm arbre arbuste plante palmier"),
    "ave": ("ave aves pajaro paloma palomas palomita garza zamuro zamuros loro loros cotorra alcaravan flamenco tortola gavilan lechuza",
            "ave pajaro paloma garza zamuro loro cotorra gavilan lechuza buho bird dove pigeon parrot owl hawk oiseau ramier perroquet tourterelle hibou"),
    "pez_marisco": ("pez peces pescado cangrejo cangrejos almeja almejas molusco moluscos concha conchas caracol tortuga langosta pesquera",
                    "pez pescado cangrejo almeja molusco concha caracol tortuga fish crab clam shell turtle poisson crabe coquille tortue"),
    "reptil": ("culebra serpiente lagarto lagartija iguana caiman vibora", "culebra serpiente lagarto lagartija iguana caiman vibora snake serpent lizard couleuvre lezard"),
    "mamifero": ("venado cervido conejo zorro tigre mono baquiro cachicamo murcielago",
                 "venado ciervo conejo zorro tigre jaguar mono deer rabbit fox monkey cerf lapin singe"),
    "insecto": ("mosquito mosquitos abeja abejas avispa hormiga", "mosquito abeja avispa hormiga bee wasp ant mouche abeille guepe fourmi"),
    "cultivo": ("conuco labranza cultivo siembra maizal maizales sembradio sementera",
                "conuco cultivo siembra sembrar maiz field garden jardin champ"),
}
PAISAJE = {"cerro", "agua_dulce", "rio", "mar_costa", "salina", "llano", "monte", "piedra",
           "arena", "barro", "viento", "camino"}
# Palabras que nunca son especie: administración, censo, la propia campaña
STOP_ESPECIE = set("""municipio distrito aldea caserio lugar sitio fundo pecuario censo casas vecinos nombre
segun esteves fuente glosa topónimo toponimo canon campana nivel forma formas grafia mapa vivo antiguo antigua
municipios linderos lindero cerca norte oeste este sur hacia entre donde tiene tenia registra pueblo poblado
poblacion paraguana falcon nuestro nuestra indigena indigenas voz voces significa quiere decir llaman llama
palabra alteracion etimologia informante informantes nombre nombres hacienda tierras tierra region zona parte
cercano cercana cuyo cuya hasta desde sobre bajo otro otra otros otras puede podria aunque tambien mismo misma
alguna algunos dicen dice""".split())


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                   if unicodedata.category(c) != "Mn").lower()


def tokens(s):
    return re.findall(r"[a-zñ]+", sin_tildes(s).replace("ñ", "n"))


CAMPO_REF = {c: set(v[0].split()) for c, v in CAMPOS.items()}
CAMPO_GLO = {c: set(v[1].split()) for c, v in CAMPOS.items()}
TODAS_CAMPO = set().union(*CAMPO_REF.values(), *CAMPO_GLO.values())


def _plural(w):
    out = {w}
    if len(w) > 4 and w.endswith("es"):
        out.add(w[:-2])
    if len(w) > 3 and w.endswith("s"):
        out.add(w[:-1])
    return out


def campos_de(texto, tabla):
    ts = set()
    for t in tokens(texto):
        ts |= _plural(t)
    return {c for c, ws in tabla.items() if ts & ws}


def especies_de(texto):
    """Palabras de contenido (≥5 letras) que podrían nombrar una especie."""
    return {t for t in tokens(texto) if len(t) >= 5 and t not in STOP_ESPECIE and t not in TODAS_CAMPO}


# ═════════════════════════════════════════════════════════════════════════
# Formas
# ═════════════════════════════════════════════════════════════════════════
def fon(forma, orto="colonial"):
    f = sin_tildes(forma).replace("ü", "u") if orto != "colonial" else str(forma).lower()
    if orto == "frances":     # Breton y Goeje escriben a la francesa
        f = f.replace("ou", "u").replace("ch", "sh").replace("gn", "ñ")
    if orto in ("linguistica", "frances"):
        f = re.sub(r"(?<![cstkp])h", "j", f)
    f = re.sub(r"[^a-zñüáéíóúàâèêëïîôûç]", "", f)
    f = fonemizar(f, gu_es_w=GU_ES_W).replace("ü", "u")
    f = sin_tildes(f)
    return re.sub(r"(.)\1+", r"\1", f)


AFIJOS_LENGUA = {  # (prefijos, sufijos) sobre la forma ya fonemizada (cruzar_achagua_caquetio.py)
    "achagua": (("nu", "ri", "ru", "gua", "wa", "ji", "na"), ("si",)),
    "lokono": (("da", "wa", "li", "to", "bu", "na"), ("n",)),
    "wayunaiki": (("a",), ()),
    "paraujano": (("ta", "a"), ()),
    "kalinago": (("n", "l", "t", "i"), ()),
}


def radicales(f, lengua):
    pref, suf = AFIJOS_LENGUA.get(lengua, ((), ()))
    out = {f}
    for p in pref:
        if f.startswith(p) and len(f) - len(p) >= MIN_FONEMAS and (len(p) > 1 or f[len(p)] not in VOCALES):
            out.add(f[len(p):])
    for g in list(out):
        for s in suf:
            if g.endswith(s) and len(g) - len(s) >= MIN_FONEMAS:
                out.add(g[: -len(s)])
    return {x for x in out if len(x) >= MIN_FONEMAS}


def raices_de(forma):
    """Las raíces candidatas de un topónimo: entero, sin un sufijo declarado,
    sin un prefijo declarado, y sin los dos. Cada una dice qué se le quitó."""
    f = fon(forma)
    out = {f: "entero"}
    bases = [(f, "")]
    for s, de in SUFIJOS:
        if f.endswith(s) and len(f) - len(s) >= MIN_FONEMAS:
            r = f[: -len(s)]
            out.setdefault(r, f"-{s} ({de})")
            bases.append((r, f"-{s}"))
    for base, quitado in bases:
        for p, de in PREFIJOS:
            if base.startswith(p) and len(base) - len(p) >= MIN_FONEMAS:
                r = base[len(p):]
                out.setdefault(r, f"{p}- ({de})" + (f" y {quitado}" if quitado else ""))
    return out


def parecido(a, b):
    sm = difflib.SequenceMatcher(None, a, b)
    if sm.real_quick_ratio() < UMBRAL_PARECIDO or sm.quick_ratio() < UMBRAL_PARECIDO:
        return 0.0
    return sm.ratio()


# ═════════════════════════════════════════════════════════════════════════
# Carga: topónimos
# ═════════════════════════════════════════════════════════════════════════
def limpiar_forma(f):
    f = re.split(r"\s*[→←]\s*", str(f))[0]
    f = re.sub(r"\(.*?\)|'.*?'", "", f)
    return f.strip()


# las palabras de anotación que la `segmentacion` del canon trae entre corchetes
# (ya fonemizadas): no son piezas del nombre
NO_ES_PIEZA = set("""sin fitonimo komponer despejar segun kon kastelano estebes komposision sobre alterado forma por
sonimo reduplikasion sinkopa kolektibo reduplikado epentesis plural metatesis del atestiguada glosa desde komo las los
una ke protesis aferesis apokope aplologia kopia konjetura bariante formas antiguas primitiba antropónimo antroponimo
lengua andina guarauna kumanagota kaketio sinkope ipotetika ipotetiko entero kon""".split())


def cargar_toponimos():
    Y = yaml.safe_load(io.open(F("2-lengua", "toponimos.yaml"), encoding="utf-8"))
    out = []
    for t in Y["toponimos"]:
        if t["nivel"] not in NIVELES:
            continue
        forma = limpiar_forma(t["forma"])
        if not forma or " " in forma.strip():      # «la cuiba», «golfete de coro», «villa real»: castellano dentro
            sin_art = re.sub(r"^(la|el|los|las)\s+", "", forma.strip())
            if " " in sin_art:
                continue
            forma = sin_art
        # el referente es lo que el lugar ES: `referente` y `glosa_fuente` (que en
        # los descartados es la nota de trabajo con el referente); la
        # `observacion` sólo si no hay ninguna de las dos, porque arrastra mapa,
        # OSM y discusión
        ref = " ".join(str(t.get(k) or "") for k in ("referente", "glosa_fuente"))
        if not ref.strip():
            ref = str(t.get("observacion") or "")
        out.append({
            "id": t["id"], "forma": forma, "nivel": t["nivel"],
            "referente_texto": ref,
            "campos": campos_de(ref, CAMPO_REF),
            "especies": especies_de(ref),
            "raices": raices_de(forma),
            "procedencia": (t.get("procedencia") or {}).get("obra"),
            # lo que el canon ya lee en el nombre: sirve de CONTROL POSITIVO (si
            # el cruce encuentra esa pieza, el método ve lo que tiene que ver)
            "ya_leido": [fon(p) for p in re.split(r"[^\wñáéíóúü]+", " ".join(
                [str(t.get("segmentacion") or "")] + list((t.get("morfemas") or {}).keys())))
                if len(fon(p)) >= MIN_FONEMAS and fon(p) not in NO_ES_PIEZA],
        })
    return out


# ═════════════════════════════════════════════════════════════════════════
# Carga: las voces
# ═════════════════════════════════════════════════════════════════════════
# una glosa que nombra un lugar o una persona es un NOMBRE, no una palabra: no
# entra al cruce de palabras y se cuenta aparte, como eco onomástico
ONOMASTICO = re.compile(r"^\s*(lugar|r[ií]o|pueblo|cacique|barrio|provincia|sitio|isla|islas|monte|sierra|puerto|cabo|"
                        r"punta|nombre|regi[oó]n|comarca|hacienda|municipio|valle|arroyo|quebrada|laguna|"
                        r"ranch|cacicazgo|personaje|indio|india|territorio|caser[ií]o|costas? de|uno de los|"
                        r"una de las|la isla|la bah[ií]a|bah[ií]a|el actual|la actual|a native name|monta[ñn]a|"
                        r"pen[ií]nsula|ensenada|cayo de|antiguo nombre|nombre que)\b", re.I)


def entrada(lengua, forma, glosa, ficha, orto="linguistica", formas_extra=()):
    fs = set()
    for fm in [forma, *formas_extra]:
        if not fm:
            continue
        fb = fon(fm, orto)
        if len(fb) >= MIN_FONEMAS:
            fs |= radicales(fb, lengua)
    if not fs:
        return None
    # una glosa larga (las citas verbatim de la lista taína) cae en todos los
    # campos: sólo cuentan los segmentos de diez palabras o menos
    segs = [g for g in re.split(r"\s*##\s*|[;«»]", str(glosa or "")) if 0 < len(tokens(g)) <= 10]
    return {"lengua": lengua, "forma": str(forma), "glosa": str(glosa or "").strip(),
            "formas_fon": sorted(fs), "campos": set().union(*[campos_de(g, CAMPO_GLO) for g in segs]) if segs else set(),
            "especies": especies_de(glosa), "onomastico": bool(ONOMASTICO.match(str(glosa or ""))),
            "ficha": ficha}


def cargar_voces():
    vs = []
    medida = collections.Counter()
    VB = CL.VOCABULARIO_BASE
    FH = getattr(CL, "FUERA_DEL_HABLA", {})
    for origen, tabla in (("VOCABULARIO_BASE", VB), ("FUERA_DEL_HABLA", FH)):
        for k, v in tabla.items():
            fu = str(v.get("fuente") or "")
            if fu.startswith("caquetío"):
                lengua = "medina" if fu == "caquetío-retroabstraido" else "caquetío"
            elif fu in ("lokono", "kalinago", "achagua", "wayunaiki", "paraujano"):
                lengua = fu
            elif fu.startswith("taíno"):
                lengua = "taíno"
            else:
                continue
            base = re.sub(r"-(lokono|achagua|kalinago|wayuu|wayunaiki|paraujano|taíno|\d+)$", "", k)
            extra = [v["forma_fuente"]] if v.get("forma_fuente") else []
            if lengua == "lokono":
                try:
                    extra.append(forma_comparable(base, v))
                except Exception:
                    pass
            orto = "colonial" if lengua in ("caquetío", "medina", "achagua", "taíno") else "linguistica"
            e = entrada(lengua, base, v.get("sig"),
                        {"clave": k, "capa": fu, "origen": origen,
                         "notas": (str(v.get("notas") or "")[:160] or None)}, orto, extra)
            if e:
                vs.append(e)
                medida[lengua] += 1
    # lokono de Perea (Schultz 1802), las acepciones con página
    for raiz, d in COMPARANDA_LOKONO.items():
        for a in d.get("acepciones", [])[:3]:
            e = entrada("lokono", raiz, a.get("glosa"), {"obra": "perea-alonso-1942", "pagina": a.get("pagina")})
            if e:
                vs.append(e)
                medida["lokono (Perea, COMPARANDA_LOKONO)"] += 1
    # taíno: la lista maestra (T10), todas las clases, con su clase declarada
    LM = yaml.safe_load(io.open(F("6-fusion", "taino_lista_maestra_2026-09-22.yaml"), encoding="utf-8"))
    for x in LM["voces"]:
        glosas = [str(g) for g in (x.get("glosas_verbatim") or [])]
        if not glosas:
            continue
        formas = [str(f) for f in (x.get("formas_atestiguadas") or []) if isinstance(f, str)][:3]
        e = entrada("taíno", formas[0] if formas else x["lema"], " ## ".join(glosas[:3]),
                    {"lema": x["lema"], "clase": x.get("clase"),
                     "cronistas": x.get("cronistas_independientes") or []},
                    "colonial", formas[1:])
        if e:
            vs.append(e)
            medida["taíno (lista maestra T10)"] += 1
    # kalinago: Goeje 1939 (hombres/mujeres) y el habla de mujeres
    KG = yaml.safe_load(io.open(F("6-fusion", "kalinago_goeje_1939.yaml"), encoding="utf-8"))
    for x in KG["vocabulario"]:
        # Goeje marca K (kalina = caribe) frente a A/f/T (arahuaco, habla de
        # mujeres, taíno). Lo kalina es de una VECINA, no de la hermana.
        lk = "kalinago-caribe" if x.get("origen_segun_goeje") == "kalina" else "kalinago"
        e = entrada(lk, x.get("forma_fuente"), x.get("glosa_fuente"),
                    {"obra": "goeje-1939", "pagina": x.get("pagina_impresa"), "registro": x.get("registro"),
                     "origen_segun_goeje": x.get("origen_segun_goeje")}, "frances")
        if e:
            vs.append(e)
            medida[f"{lk} (Goeje 1939)"] += 1
    KM = yaml.safe_load(io.open(F("6-fusion", "kalinago_mujeres_goeje_2026-09-24.yaml"), encoding="utf-8"))
    for x in KM["voces"]:
        e = entrada("kalinago", x.get("forma_mujeres"), x.get("glosa_fr"),
                    {"obra": "goeje-1939", "pagina": x.get("pagina_impresa"), "registro": "f"}, "frances")
        if e:
            vs.append(e)
            medida["kalinago (habla de mujeres, Goeje)"] += 1
    return vs, dict(medida)


# ═════════════════════════════════════════════════════════════════════════
# El cruce
# ═════════════════════════════════════════════════════════════════════════
def similares(tops, voces):
    """Todos los (topónimo, voz) con parecido de forma ≥ umbral: NO depende de
    la glosa ni del referente, así que se calcula una vez y los controles lo
    reutilizan."""
    por_fon = collections.defaultdict(list)
    for i, v in enumerate(voces):
        for f in v["formas_fon"]:
            por_fon[f].append(i)
    formas = list(por_fon)
    largos = {f: len(f) for f in formas}
    pares = {}  # (t_idx, v_idx) -> (sim, raiz, que_se_quito, forma_fon)
    for ti, t in enumerate(tops):
        for r, quitado in t["raices"].items():
            lr = len(r)
            sm = difflib.SequenceMatcher(None, "", r)
            for f in formas:
                lf = largos[f]
                if 2.0 * min(lr, lf) / (lr + lf) < UMBRAL_PARECIDO:
                    continue
                sm.set_seq1(f)
                if sm.real_quick_ratio() < UMBRAL_PARECIDO or sm.quick_ratio() < UMBRAL_PARECIDO:
                    continue
                s = sm.ratio()
                if s < UMBRAL_PARECIDO:
                    continue
                for vi in por_fon[f]:
                    k = (ti, vi)
                    if k not in pares or s > pares[k][0]:
                        pares[k] = (s, r, quitado, f)
    return pares


def filtro(t_campos, t_especies, v_campos, v_especies):
    """Qué hace pasar el par: un campo de paisaje compartido, o un campo vivo.

    La «especie compartida» (una palabra de contenido igual en el referente y en
    la glosa) se probó en la primera corrida y se RETIRÓ: casaba `hacha`,
    `libro`, `gente`, `origen` o `entonces` porque el texto del referente trae
    la discusión etimológica de Esteves, no sólo lo que el lugar es. Se deja
    escrito para que nadie la vuelva a poner sin otra cosa que la filtre."""
    c = t_campos & v_campos
    if c & PAISAJE:
        return "paisaje", sorted(c & PAISAJE)
    if c:
        return "clase-viva", sorted(c)
    return None, []


def contar(pares, tops, voces, glosa_de=None, ref_de=None):
    """Pares (topónimo, lengua) que pasan el filtro. glosa_de/ref_de permiten
    que los controles barajen sin recalcular el parecido."""
    por_lengua = collections.defaultdict(set)
    por_tipo = collections.Counter()
    for (ti, vi), _ in pares.items():
        v = voces[vi]
        if v["onomastico"]:
            continue
        vc, ve = (voces[glosa_de[vi]]["campos"], voces[glosa_de[vi]]["especies"]) if glosa_de else (v["campos"], v["especies"])
        tc, te = (tops[ref_de[ti]]["campos"], tops[ref_de[ti]]["especies"]) if ref_de else (tops[ti]["campos"], tops[ti]["especies"])
        tipo, _ = filtro(tc, te, vc, ve)
        if tipo:
            por_lengua[v["lengua"]].add(ti)
            por_tipo[(v["lengua"], tipo)] += 1
    return {l: len(s) for l, s in por_lengua.items()}, por_tipo


def familias(voces):
    """Una voz por familia: misma lengua y mismos cuatro primeros fonemas del
    radical más corto. El achagua trae muchas entradas de una raíz (`numa`
    'boca' → `numacoa` 'margen del agua', `rinumacoa` 'orilla', `vní numāna`
    'boca del río'…) y la permutación de glosas las dispersa: esta
    sensibilidad dice si el exceso sobre el azar es de pares o de familias."""
    vistas, keep = set(), set()
    for i, v in enumerate(voces):
        if v["onomastico"]:
            continue
        k = (v["lengua"], min(v["formas_fon"], key=len)[:4])
        if k not in vistas:
            vistas.add(k)
            keep.add(i)
    return keep


def controles(pares, tops, voces, lenguas, solo=None):
    rnd = random.Random(SEMILLA)
    idx_por_lengua = collections.defaultdict(list)
    for i, v in enumerate(voces):
        if not v["onomastico"] and (solo is None or i in solo):
            idx_por_lengua[v["lengua"]].append(i)
    glos = {l: [] for l in lenguas}
    refs = {l: [] for l in lenguas}
    for _ in range(REPLICAS):
        perm = {}
        for l, idx in idx_por_lengua.items():
            sh = idx[:]
            rnd.shuffle(sh)
            perm.update(dict(zip(idx, sh)))
        obs, _ = contar(pares, tops, voces, glosa_de=perm)
        for l in lenguas:
            glos[l].append(obs.get(l, 0))
        orden = list(range(len(tops)))
        rnd.shuffle(orden)
        obs2, _ = contar(pares, tops, voces, ref_de=dict(enumerate(orden)))
        for l in lenguas:
            refs[l].append(obs2.get(l, 0))
    return glos, refs


def resumen_azar(vals, observado):
    s = sorted(vals)
    return {"media": round(statistics.mean(vals), 2), "p95": s[int(0.95 * (len(s) - 1))],
            "max": s[-1], "replicas_que_igualan_o_superan": round(sum(1 for x in vals if x >= observado) / len(vals), 3)}


# ═════════════════════════════════════════════════════════════════════════
# Parte 1 — -ana: lo contable
# ═════════════════════════════════════════════════════════════════════════
LUGAR_GLOSA = re.compile(r"\b(lugar|sitio|r[ií]o|cerro|isla|pueblo|tierra|regi[oó]n|provincia|laguna|costa|"
                         r"playa|punta|monte|sabana|llano|campi[ñn]a|vega|valle|lieu|place|village|river|island)\b", re.I)


def medir_ana(voces):
    out = {}
    for lengua in ("lokono", "taíno", "kalinago", "kalinago-caribe", "achagua", "wayunaiki", "paraujano", "caquetío", "medina"):
        vs = [v for v in voces if v["lengua"] == lengua]
        ana = [v for v in vs if re.search(r"an+[aá]$", sin_tildes(v["forma"]))]
        lugar = [v for v in ana if LUGAR_GLOSA.search(v["glosa"])]
        out[lengua] = {
            "voces": len(vs), "en_ana": len(ana), "con_glosa_de_lugar": len(lugar),
            "ejemplos_de_lugar": [f"{v['forma']} '{v['glosa'][:70]}'" for v in lugar[:8]],
        }
    return out


def medir_achagua_ana():
    Y = yaml.safe_load(io.open(F("6-fusion", "achagua_neira_ribero_1762.yaml"), encoding="utf-8"))
    voc = Y["vocabulario"]
    ana = [v for v in voc if re.search(r"an+[aā]\b", str(v.get("achagua", "")), re.I)]
    topo = [v for v in voc if "TOPONIMO" in str(v.get("nota", "")).upper() or "toponimo" in str(v.get("nota", ""))]
    return {
        "entradas_del_vocabulario": len(voc),
        "formas_con_ana": len(ana),
        "notas_de_toponimo_del_escriba": [f"{v['castellano']} = {v['achagua']} (pliego {v.get('pliego')}): {str(v.get('nota'))[:90]}" for v in topo],
        "boca": [f"{v['castellano']} = {v['achagua']} (pliego {v.get('pliego')})" for v in voc
                 if re.match(r"(Boca|Voca)\b", str(v.get("castellano", "")))],
        "lugar": [f"{v['castellano']} = {v['achagua']} (pliego {v.get('pliego')})" for v in voc
                  if re.match(r"(Lugar|Espacio)", str(v.get("castellano", "")))],
    }


GRAFIAS_GUAYANA = ("Guayana", "Guiana", "Guyana", "Guyane", "Goyana", "Wayana", "Guajana", "Oayana", "Ouajana")
ETIMOLOGIA_GUAYANA = re.compile(r"(many waters|land of water|tierra de (muchas )?aguas|pays des eaux|"
                                r"gu[iy]ana[^.]{0,80}(signif|means|meaning|quiere decir|veut dire)|"
                                r"(nom|nombre|voz|name)[^.]{0,40}gu[iy]an[ae]|leur nom au pays)", re.I)


def medir_guayana():
    """Regla 6 antes de contar: cómo escribe cada obra el nombre, y en cuántas
    hay algo que se parezca a una etimología (la regex de arriba, ancha a
    propósito; cada acierto se leyó)."""
    out = {}
    for f in sorted(os.listdir(F("fuentes_caquetios"))):
        if not f.endswith(".txt"):
            continue
        t = io.open(F("fuentes_caquetios", f), encoding="utf-8", errors="replace").read()
        t1 = re.sub(r"\s+", " ", t)
        n = {g: len(re.findall(rf"\b{g}s?\b", t1)) for g in GRAFIAS_GUAYANA}
        n = {g: x for g, x in n.items() if x}
        if n:
            out[f] = {"grafias": n, "pasajes_con_aire_de_etimologia": len(ETIMOLOGIA_GUAYANA.findall(t1))}
    return out


# ═════════════════════════════════════════════════════════════════════════
# Fauna y flora en -re
# ═════════════════════════════════════════════════════════════════════════
FAUNA_RE = {  # clave caquetía -> (lo que es, cabezas de glosa que lo nombran en otras lenguas)
    "bisure": ("lagartija", "lagartija lagarto lizard lezard anolis"),
    "chaure": ("lechuza", "lechuza buho mochuelo owl hibou chouette"),
    "chiriware": ("gavilán", "gavilan halcon hawk epervier aguila"),
    "kerekere": ("ave pequeña", "querequere"),
    "bayure": ("abeja", "abeja bee abeille"),
    "yakure": ("acacia, cují", "acacia cuji yacure"),
    "naure": ("planta bejucosa", "bejuco liana enredadera vine liane"),
    "chipare": ("matapalo", "matapalo higueron ficus"),
    "susukure": ("cardón", "cardon cactus cardo"),
    "watakare": ("árbol de fruto no comestible", "guatacare"),
    "yacare": ("caimán (y 'pueblo', morfema-005)", "caiman cocodrilo babo yacare alligator caiman"),
    "asubure": ("sesuvio, vidrio (planta)", "sesuvio verdolaga vidrio"),
    "camuare": ("árbol de madera blanda (Camunare)", "camuare"),
    "chamanare": ("—", "iguana"),   # control: la voz achagua en -are para un reptil
}
FORMA_DE = {"yacare": "yacare", "asubure": "asubure", "camuare": "camuare", "chamanare": "chamanare"}


def cruzar_fauna(voces):
    out = []
    for clave, (que, cabezas) in FAUNA_RE.items():
        cab = set(cabezas.split())
        forma = fon(FORMA_DE.get(clave, clave))
        hall = collections.defaultdict(list)
        for v in voces:
            if v["lengua"] in ("caquetío", "medina") or v["onomastico"]:
                continue
            ts = set(tokens(v["glosa"]))
            if not (ts & cab):
                continue
            s = max(difflib.SequenceMatcher(None, forma, f).ratio() for f in v["formas_fon"])
            hall[v["lengua"]].append((round(s, 2), v["forma"], v["glosa"][:60]))
        fila = {"voz": clave, "que_es": que, "forma_fonemica": forma, "por_lengua": {}}
        for l, xs in sorted(hall.items()):
            xs.sort(reverse=True)
            fila["por_lengua"][l] = {"mejor": f"{xs[0][1]} '{xs[0][2]}' ({xs[0][0]})",
                                     "voces_con_esa_glosa": len(xs),
                                     "pasa_umbral": xs[0][0] >= UMBRAL_PARECIDO}
        out.append(fila)
    return out


# ═════════════════════════════════════════════════════════════════════════
# Lo leído a mano. Cada fila dice obra (clave de 4-fuentes/bibliografia.yaml),
# página, si se vio en imagen o sólo en la capa de texto, y la cita corta.
# Lo contable de estas mismas obras lo mide el script (arriba).
# ═════════════════════════════════════════════════════════════════════════
META = {
    "pregunta": (
        "Miguel, 2026-10-10: cruzar los topónimos caquetíos que no tienen lectura con las lenguas "
        "hermanas para sacar candidatos a palabra o cognado; y ver qué hace -ana en los nombres de "
        "las hermanas —Guayana en el lokono, los nombres taínos— para saber si se le puede devolver "
        "una glosa al -ana caquetío («hasta el día de hoy está solamente en Chamuriana, Jayana, "
        "Curiana, Cujicana»)."),
    "estado": "PROPUESTA (regla 5): no toca 2-lengua/, curiana_sim/, 3-mundo/ ni ningún YAML generado",
    "obra": "varias (ver fuentes_leidas)",
    "quien": "minero del cruce (Claude Opus 5.5), rama vault/cruce-toponimos",
    "fuentes_leidas": {
        "las-casas-apologetica": "cap. VII p. 19 (Maguana); capa de texto, desfase constante pdf − 14",
        "las-casas-1875": "lib. I caps. XLIV (Cubanacan) y LVI (çabanas); citado por capítulo, el PDF es un ebook",
        "oviedo-y-valdes-1851": "vol. 1, Maguana como villa (sin glosa); capa de texto extraída al vuelo",
        "goeje-1939": "pp. 5 (los Guayana), 13 (magua / magüana, xagueye), 57 (habla de mujeres: šiba, šauai, balaua); impresa = pdf − 1",
        "breton-1665": "p. 416, entrada Ouâitoucoubouli (gentilicio -ri / -na); capa de texto",
        "breton-1665 (Grammaire 1667)": "del género de los nombres, hoja signada G iij: «Les pluriers terminez en a»; capa de texto",
        "brett-1880": "pp. 178-179, notas (Ebesoana, Demaréna, Korobohána); ya vistas en imagen por la minería 2 (hermanas_lokono, lokono-parentesco-002)",
        "brett-1868": "p. 98 (familias lokonas), p. 485 (anakabo 'in the midst' frente a nacan)",
        "perea-alonso-1942": "p. 561 (-coa-na), p. 647 (a-nnakù-di 'estar en medio'); Guayana sin etimología",
        "bachiller-morales-1883": "pp. 120-121 (Del Monte: -ana agrícola), p. 114 (Habana 'pradera'), p. 205 (nacan / anaca), p. 277 s.v. Guainía (Guayana); impresa = pdf − 4",
        "coll-y-toste-1897": "pp. 166-167 (Sibana, Sibanacán), 169 y 227 (Habana), 240 (Maguana) — vía 6-fusion/taino3_coll_y_toste_1897.yaml",
        "zayas-1931": "t. I s.v. Abayagua (Maguana 'vega menor'); t. I p. 34 s.v. Ana (contra Del Monte y Bachiller)",
        "gumilla-1791": "t. I, la Nación Guayana (sin etimología)",
        "neira-ribero-1762": "vocabulario entero, por 6-fusion/achagua_neira_ribero_1762.yaml (pliegos 42, 61, 69, 73, 80, 98)",
        "fabo-1911": "p. 101 (-are llanero; mánare 'morir')",
        "alvarado-1921": "pp. 199-200 s.v. MANARE (y avispa, culebra-sapa), p. 205 s.v. MAPANARE / MAPANARÍ",
        "carvajal-1892": "«cataures y manaures muy labrados» (la relación de 1647); capa de texto",
        "oliver-1989-cap2": "pp. 148-150 (los sufijos toponímicos caquetíos)",
        "roth-1915": "barrido de nombres en -ana; ninguno de lugar con glosa",
    },
    "sondas": {
        "ana": "voces y nombres terminados en -ana, -anna, -aná, -āna en cada fuente y en el lexicón; -na tras raíz en -a se cuenta con ellas",
        "guayana": "Guayana, Guiana, Guyana, Guyane, Goyana, Wayana, Guajana, Oayana, Ouajana — y una regex ancha de etimología (medida abajo)",
        "cruce": "250 nombres de una palabra en nivel C o descartado (los de varias palabras con castellano dentro quedan fuera)",
    },
    "controles": [
        "permutación de glosas dentro de cada lengua (la forma queda, el significado se baraja)",
        "permutación de referentes entre topónimos (cada lugar recibe lo que es otro)",
        "una voz por familia (misma lengua, mismos cuatro primeros fonemas del radical): el exceso, ¿es de pares o de familias?",
        "control positivo: el cruce tiene que encontrar lo que el canon ya lee (para 'mar' en Paraguaná, kiba 'piedra' en Cuiba y Tiquiba, kumarawa en Cumaraguas…)",
    ],
    "no_leido": [
        "Oviedo 1851-1855 sólo se barrió por Maguana y sabana: un -ana glosado en sus otros libros no se buscó",
        "Gilij (maipure) no se leyó para -ana: la prima maipure queda sin medir",
        "el capítulo de lenguas de Gumilla donde Goeje dice que el guayana es «apparentée au Kalina»: no se localizó en t. I ni t. II",
        "Breton 1666 (françois-caraïbe): la entrada «habitant» se vio en la capa de texto, sin página",
        "las páginas de Breton 1665 y 1667 no se vieron en imagen",
        "el wayuu sólo como comparanda medida en el lexicón; Jahn 1927 no se leyó para topónimos en -ana",
        "Las Casas, Historia, vols. 2-5: no están en el repo",
    ],
    "fuentes_a_buscar": [
        "J. Williams 1923, «The name “Guiana”», Journal de la Société des Américanistes XV (Goeje 1939 p. 5 la cita: es la discusión de la etimología)",
        "C. H. de Goeje, «Guayana and Carib tribal names», Proceedings del XXI Congreso Internacional de Americanistas (citado en Goeje 1939 p. 5)",
        "W. Hilhouse 1832/1834, Journal of the Royal Geographical Society: las 27 familias lokonas que Brett resume (p. 98) — ¿cuántas en -ana y con qué glosa?",
        "C. H. de Goeje 1928, The Arawak Language of Guiana, y W. Pet 1987: la fuente de lokono kabadaro 'jaguar' que el lexicón cita",
        "D. Taylor 1977, Languages of the West Indies: el gentilicio -ri / -na del caribe insular, con su estrato",
        "A. Del Monte 1853, Historia de Santo Domingo, p. 370 (sólo se tiene por Bachiller)",
        "un diccionario de venezolanismos con etimología para mapanare (Alvarado 1921 no la da)",
    ],
    "descargas": "ninguna (lo decide Miguel)",
}

ANA = {
    "estado_en_el_canon": (
        "morfema-011: forma atestiguada SIN glosa desde #109 (Miguel, 2026-09-07, opción B) y en el prompt sin "
        "glosa desde d21.6. Casos caquetíos: Paraguaná, Curiana, Chamuriana, Cujicana, Jayana, Coria-na (La "
        "Ramada, Castellanos p. 264 vía Oliver cap. 3 p. 211); en el canon también Cariguariana, Maracapana y "
        "Capana, con el -ana dentro de la raíz."),
    "por_lengua": {
        "taíno": {
            "linea": "hermana (lokonoide)",
            "con_glosa": [
                {"nombre": "Maguana", "lugar": "provincia y vega de la Española (la de Caonabó)",
                 "glosa": "«Llamaban los indios á la Vega grande Magua […] y á esta provincia decían con adición Maguana, cuasi la Vega menor»",
                 "procedencia": {"obra": "las-casas-apologetica", "pagina": "19 (cap. VII)", "visto": "capa de texto"},
                 "que_hace_el_ana": "la -na añadida a Magua 'la vega grande' da 'la vega menor': valor de MENOR / la otra, más pequeña",
                 "separable": "sí: magua 'vega grande' lo glosa el mismo Las Casas",
                 "atestaciones": "un cronista; Goeje 1939 p. 13 («la petite plaine»), Coll y Toste 1897 p. 240 y Zayas 1931 (s.v. Abayagua) lo copian: no son independientes",
                 "nota": "la lista maestra taína (T10) tenía maguana como ii-solo-secundaria por no haber visto el pasaje: esta es su primaria"},
                {"nombre": "çabana / sabana", "glosa": "«campiñas llanas y rasas que […] ellos llaman en su lengua çabanas»",
                 "procedencia": {"obra": "las-casas-1875", "pagina": "lib. I cap. LVI"},
                 "que_hace_el_ana": "nada que se pueda aislar: no hay *çab- ni *sab- con glosa; es la palabra entera",
                 "separable": "no"},
                {"nombre": "Habana", "glosa": "«Sitio grande»; «Lo grande; ha, por gua, he aquí, lo; baña, grande»",
                 "procedencia": {"obra": "coll-y-toste-1897", "pagina": "169 y 227"},
                 "que_hace_el_ana": "para su autor es -bana 'grande', no -ana; sin cronista detrás (lista maestra: ii)",
                 "separable": "conjetura de compilador"},
                {"nombre": "Sibana / Sibanacán", "glosa": "'pedregoso' / 'piedras muchas'",
                 "procedencia": {"obra": "coll-y-toste-1897", "pagina": "166-167 (su vocabulario inverso)"},
                 "que_hace_el_ana": "siba 'piedra' + -na 'abundante en'?; Sibanacán es topónimo cubano",
                 "separable": "conjetura de compilador, sin cronista"},
            ],
            "contra": [
                "Del Monte 1853 (vía bachiller-morales-1883 pp. 120-121): «las terminaciones en ana son aplicables á la agricultura, plantas, frutos y sus poseedores»; Bachiller la da por equivocada y Zayas 1931 t. I p. 34 la llama arbitraria",
                "Cubanacan no es -ana: es Cuba + nacan 'medio, en medio' (las-casas-1875 lib. I cap. XLIV). Va a Paraguaná, abajo",
            ],
            "sin_glosa": "Bayaguana, Yaguana, Caguana, Guatapaná, Bucaná, Jácana: nombres con referente (Coll y Toste) y sin significado",
        },
        "lokono": {
            "linea": "hermana (lokonoide)",
            "con_glosa": [
                {"nombre": "Ebesoana, Demaréna (y Korobohána)",
                 "glosa": "«From the "
                          "“Ebesotu” (changed or transformed), heroine of the above legend, the Ebesoana (Arawak family) take their name»",
                 "procedencia": {"obra": "brett-1880", "pagina": "178-179, notas", "visto": "imagen (minería 2, lokono-parentesco-002)"},
                 "que_hace_el_ana": "hace del nombre de la antepasada el nombre del LINAJE matrilineal: Ebesō-tu → Ebeso-ana, Demare-du → Demaré-na: 'los de X, la gente que viene de X'",
                 "separable": "sí en los dos primeros (la antepasada está nombrada en la misma nota)"},
                {"nombre": "-coa-na (no topónimo)", "glosa": "nombres de lugar e instrumento sobre verbo: a-ha-cuba-coa-na 'lugar de reposo', lu-yaccada-coa-na 'su cama'",
                 "procedencia": {"obra": "perea-alonso-1942", "pagina": "561"},
                 "que_hace_el_ana": "nominalizador verbal; ya en 2-lengua/morfologia.md §8. No forma nombres de lugar sobre nombres"},
            ],
            "guayana": {
                "lo_que_dicen_las_fuentes_del_repo": [
                    {"obra": "goeje-1939", "pagina": "5",
                     "dice": "el nombre del país viene de un PUEBLO, los Guayana, que vivían junto a la desembocadura del Caroní en el Orinoco; Gumilla dice que su lengua es pariente del kalina, y el vocabulario de Raleigh (1595) y Keymis (1596) «confirme que c'était une langue de la famille caribe»"},
                    {"obra": "bachiller-morales-1883", "pagina": "277 (s.v. Guainía)",
                     "dice": "Guainía «es palabra también de los indios de Costa Firme de que han derivado los españoles la voz Guiana ó Guayana», tras Dauxion Lavaysse: tercera mano"},
                    {"obra": "gumilla-1791", "pagina": "t. I (la Nación Guayana)", "dice": "nombra a la nación Guayana, «de genio duro y belicoso», sin etimología"},
                ],
                "tierra_de_muchas_aguas": "no aparece en ninguna fuente del repo (medido abajo, ana.medido.guayana): es etimología que circula fuera",
                "veredicto": "en el repo, Guayana es un ETNÓNIMO pasado al país, y de un pueblo de lengua caribe: no es un -ana lokono ni dice nada del -ana arahuaco",
            },
            "sin_glosa": "los nombres en -ana de Brett 1868/1880, Roth 1915, Brinton 1871 y Perea 1942 son etnónimos (Wapisiana, Ojana, Layana), personajes (Kororomana, Marerewana, Amanna) o -banna 'hoja' (Yuri-banna 'hoja de tabaco', nombre de persona): ningún nombre de lugar en -ana con glosa",
        },
        "kalinago": {
            "linea": "hermana (lokonoide, por el sustrato iñeri)",
            "con_glosa": [
                {"nombre": "Ouâitoucoubouli-ri / Ouâitoucoubouli-na; caloucaera-ri / caloucaera-na; Liamaïga-ri / Liamaïga-na; Kaérabou-ri / Kaéra-bona; balaourcou-ri / balaourcou-na; aichi-na",
                 "glosa": "«vn sauuage ou habitant de la Dominique, les habitans de la Dominique. On forme des mots pareillement sur le nom des autres Isles»",
                 "procedencia": {"obra": "breton-1665", "pagina": "416 (s.v. Ouâitoucoubouli) y Grammaire 1667, hoja G iij («Les pluriers terminez en a, sont du commun»)", "visto": "capa de texto"},
                 "que_hace_el_ana": "GENTILICIO: isla + -ri 'un habitante' (masculino), isla + -na 'los habitantes' (plural común)",
                 "separable": "sí: el nombre de la isla queda entero (Ouâitoucoubouli 'Dominica', Caloucaera 'Guadalupe', Liamaïga 'San Cristóbal')",
                 "sustrato": "sin-decidir: Breton da la regla sin marcar registro de hombres o de mujeres"},
            ],
            "sin_glosa": "balanna 'mar' (Breton, femenino; Goeje f balaua) es palabra entera; ningún nombre de isla en -ana",
        },
        "achagua": {
            "linea": "prima (orinoco-llanos): comparanda, no reconstruye sola",
            "con_glosa": [
                {"nombre": "Casanare Numana 'Boca de Casanare' (pliego 42); Vní numāna 'Voca del Rio' (pliego 98)",
                 "que_hace_el_ana": "numa 'boca' (Numasí, pliego 42) + -na relacional: 'la boca (de)'. Abaca Numa 'Boca del monte' va sin -na. La nota del escriba de la transcripción («toponimo del Meta/Casanare con el locativo -ana») no se sostiene: el -na es del sustantivo 'boca', no del topónimo",
                 "separable": "sí, pero no es locativo"},
                {"nombre": "Jarrun 'Lugar, sitio' (pliego 73) ~ Jarruna 'Espacio, sitio' (pliego 61)",
                 "que_hace_el_ana": "-na optativo sobre 'lugar': la misma -na relacional"},
            ],
            "fabo_1911": "p. 101: el -are hidronímico llanero; del -ana no dice nada",
        },
        "wayuu": {"linea": "prima (guajiro-paraujana): sólo comparanda",
                  "medido": "ver ana.medido.lexicon_por_lengua.wayunaiki: ninguna voz en -ana con glosa de lugar"},
        "caquetio_mismo": {
            "oliver_1989_cap2": "pp. 148-149: los sufijos toponímicos caquetíos que lista son -bana, -coa, -oa, -kiva, -(e)bo y -wa; -ana no está entre ellos",
            "oliver_1989_cap3": "p. 211: «Coria-na» y «Paragua-nil», «suspiciously Caquetío», en La Ramada",
        },
    },
    "paraguana_en_medio": {
        "por_que_aqui": "Esteves p. 56 recoge «conuco en medio del mar» y al canon le falta el morfema de 'en medio'",
        "lo_que_hay": [
            "taíno nacan 'medio, en medio': «Cubanacan […] porque nacan quiere decir, en la lengua destas islas, medio ó en medio» (las-casas-1875 lib. I cap. XLIV)",
            "lokono annakan 'centro, punto medio' (lexicón, Brinton 1871) y a-nnakù-di 'estar en medio, entre' (perea-alonso-1942 p. 647, Schumann 1755); brett-1868 p. 485: «anakabo n signifying “in the midst”» frente a nacan",
        ],
        "lectura": "paragua 'mar' + -ná como resto de *naka(n) 'en medio' daría 'en medio del mar', la tradición de Esteves",
        "veredicto": "DÉBIL: exige perder -kan sin un solo paralelo de ese recorte, y Paraguaná se imprime con -ná tónica, no con -naka. Se deja como hipótesis",
    },
    "veredicto": {
        "lugar_de": "ninguna línea —hermana ni prima— glosa un -ana como 'lugar de'. La retirada de #109 se confirma desde fuera",
        "lo_que_recurre": (
            "-(a)na como COLECTIVO DE GENTE, en dos hermanas lokonoides y con glosa de fuente primaria y separable: "
            "el linaje matrilineal lokono (Brett 1880) y el gentilicio plural kalinago (Breton 1665 y 1667). "
            "Guayana, el caso que trae Miguel, es lo mismo visto desde fuera —un pueblo cuyo nombre pasó al país, "
            "Goeje p. 5—, pero ese pueblo hablaba caribe."),
        "lo_que_no_recurre": "el taíno da un caso, Maguana 'la vega menor' (Las Casas): -na sobre un nombre de lugar con valor de 'menor'. Uno solo, y otra función",
        "candidato": (
            "-ana 'los de X, la gente de X' (colectivo de gente, gentilicio): el topónimo sería el nombre de una gente "
            "pasado al lugar, como Guayana. Encaja con Curiana, que nombra «el pueblo» y «la costa» a la vez (Arcaya "
            "p. 169), y con Coria-na y Paragua-nil como nombres de aldea en La Ramada (Castellanos p. 264)."),
        "linea": "hermana: lokono + kalinago (dos tradiciones lokonoides). El achagua no lo apoya (su -na es relacional); el taíno lo contradice en su único caso",
        "capa_propuesta": "hipotético, no reconstruido: el lado caquetío no tiene un solo -ana glosado y el paso de gentilicio a topónimo es inferencia nuestra (regla 2: en duda, degradar)",
        "lo_que_lo_subiria": "un -ana caquetío usado por una fuente como nombre de GENTE (no de lugar), o una de las 27 familias de Hilhouse en -ana con su epónimo",
        "decide": "Miguel (ver el borrador de issue): dejar sin glosa, adoptar el candidato como hipotético, o esperar a Hilhouse y a Williams 1923",
    },
}

LECTURAS_PROPUESTAS = [
    {"toponimo": "toponimo-239", "forma": "manare",
     "lecturas": [
         {"tipo": "testimonio-residente",
          "lectura": "Manare sería una culebra de ojos amarillos, «como de gemas»; y muchos nombres propios y de animales terminan en -re (mapanare, Manaure)",
          "quien": "Miguel Gil Urbina", "fecha": FECHA, "eje": "significado"},
         {"tipo": "glosa-fuente",
          "lectura": "«CULEBRA-SAPA manare. Pequeña serpiente que suele hallarse a orillas de las vertientes y arroyos hecha un rollo […] Es mui ponzoñosa» (E. Portuguesa); y «Avispa MANARE», amarilla, nombrada por su nido «a modo de manare»",
          "quien": "Alvarado 1921", "fecha": FECHA, "eje": "significado",
          "procedencia": {"obra": "alvarado-1921", "pagina": 200},
          "veredicto": ("sin decidir. Da a la lectura de Miguel un referente documentado —hay una culebra llamada "
                        "manare—, pero en los Llanos y sin los ojos amarillos. El patrón de la entrada es nombrar por "
                        "la forma del cedazo: la avispa por su nido en disco; la culebra, por enroscarse en rollo, es "
                        "inferencia nuestra (Alvarado no lo dice)")},
     ],
     "contexto": [
         "la glosa del canon es «cesto de fibra», voz cumanagota según Esteves p. 50; Alvarado p. 199 s.v. MANARE: harnero, «Voz car., ch. y cum. que existe asimismo en cal., gal., etc. En aruaco, mánali» — el cedazo tiene forma lokona (mánali)",
         "Alvarado p. 199: «Carvajal escribe incorrectamente manaure»; y en Carvajal (relación de 1647) se lee «cataures y manaures muy labrados»: ahí manaure es el objeto tejido, no el título. Para la campaña de Manaure (rama vault/manaure-colombia)",
         "en el achagua (Neira y Ribero 1762) chamanare es la iguana (pliego 69) y manari- da 'calamidad, perderse, arruinar' (pliegos 31, 47, 82); Fabo 1911 p. 101 trae mánare 'morir' y un río Manare entre los hidrónimos llaneros en -are",
     ]},
]

MAPANARE = {
    "pregunta": "¿alguna fuente del repo da el origen de «mapanare»?",
    "respuesta": "no",
    "lo_que_hay": [
        "alvarado-1921 p. 205 s.v. MAPANARE: la serpiente («Color amarillo o rosado en el lomo con una serie de manchas pardas romboidales», y la especie más común «de un amarillo que degenera sensiblemente en blanco» por debajo), la variante mapanarí (s.v. RABO-FRITO) y la frase «ser una mapanare»; NINGUNA etimología, cuando la entrada vecina MAPÍRE sí la lleva («Del ch. mapiri») y MANARE dice «Voz car., ch. y cum.»",
        "neira-ribero-1762, pliego 80: «Palma = Cusí, guerrarí, mapanarí, gigirrí» — en achagua mapanarí es una PALMA, no la culebra: mismo nombre, otra cosa (el filtro de significado lo separa)",
        "el resto del repo nombra la mapanare como fauna de Falcón (corpus de ecología, sin voz caquetía: hueco declarado en 3-mundo/corpus/ecologia_lexicon_map.md)",
    ],
    "maparari": "toponimo-172 sigue igual: la variante mapanarí de Alvarado acerca la forma pero el salto n~r interior sigue sin permutación documentada; no se propone",
    "a_buscar": "un diccionario de venezolanismos con etimología (fuentes_a_buscar)",
}

MEJORES = [  # elegidos a mano DE LA LISTA que el script emite; cada uno con su par medido
    {"toponimo": "toponimo-016", "forma": "capadare", "nivel": "C",
     "par": "lokono kabadaro 'jaguar, yaguareté'",
     "referente": "la glosa de fuente es «Diente de tigre» (Zavala; la atribución a Alvarado no se pudo verificar, censo_terminacion_re.yaml)",
     "lectura": "capadare podría ser la palabra entera para el jaguar (kabadaro ~ capadare: p~b, -o~-e) y «diente de tigre» una relectura de -dare como dare 'diente'; conserva el 'tigre' que la segmentación capa- + dare dejaba sin morfema",
     "linea": "hermana (lokono), con reserva: las notas del lexicón dicen que kabadaro es préstamo del caribe insular en el lokono (Goeje 1928, Pet 1987; no están en el repo). Si viene del estrato caribe, la línea es VECINA",
     "por_que_es_debil": "una sola lengua, y préstamo; el canon decía «el lexicón no tiene ninguna palabra para felino» y sí la tenía, como comparanda lokona"},
    {"toponimo": "toponimo-285", "forma": "siraba", "nivel": "descartado",
     "par": "taíno ciba 'piedra' (Pané, Las Casas: lista maestra, i-primaria) · lokono siba 'piedra, roca' · kalinago (habla de mujeres) šiba 'pierre' (Goeje p. 57)",
     "referente": "cerro cónico de unos 500 m unido al de Santa Ana, con los petroglifos «Las Piedras del Almanaque» (Esteves p. 60)",
     "lectura": "si(ra)ba: la piedra en las tres hermanas, en un cerro de piedras grabadas; el caquetío atestigua kiba/quiva 'piedra' y van Buurt da siba en Aruba (Casibari)",
     "linea": "hermana, en las tres",
     "por_que_es_debil": "queda un -ra- sin explicar; el parecido (0,8) lo hace la secuencia s-i-b-a, no un cognado limpio"},
    {"toponimo": "toponimo-298", "forma": "cimiro", "nivel": "descartado",
     "par": "caquetío (reconstruido) sima 'cerro, elevación del terreno' + -iro diminutivo (REGLAS_ESTEVES)",
     "referente": "cerro, lindero en Moruy (Esteves p. 30)",
     "lectura": "sim(a)-iro 'cerrito'; Esteves escribió «No parece voz indígena»",
     "linea": "la propia lengua: no sale de una hermana (sima se declara por cognado lokono y por Barquisimeto, y ese cognado no está en el lexicón)",
     "por_que_es_debil": "las dos piezas son de capa baja (sima reconstruido, -iro leído en topónimos) y contradice a la fuente"},
    {"toponimo": "toponimo-090", "forma": "amuay", "nivel": "C",
     "par": "kalinago (habla de mujeres) šauai 'côte rocheuse, falaise, caverne' (Goeje p. 57; grotte šauai-roku)",
     "referente": "Esteves p. 16: «la voz da la idea de cavidad subterránea, haitón, cueva grande», y en las cercanías hay cuevas naturales",
     "lectura": "la cueva / el acantilado rocoso de la hermana para un sitio con cuevas",
     "linea": "hermana (kalinago, estrato arahuaco de las mujeres)",
     "por_que_es_debil": "m- frente a š- en el arranque no es correspondencia de nadie; y Amuay es ya C por el ETNÓNIMO (Oliver cap. 3 pp. 275-276)"},
    {"toponimo": "toponimo-264", "forma": "bajarigua", "nivel": "descartado",
     "par": "taíno bagua 'mar' (Oviedo; lista maestra i-primaria) · kalinago (mujeres) balaua 'la mer' (Goeje p. 55)",
     "referente": "fundo y salina al norte de El Vínculo, en una depresión bajo el nivel del mar (Esteves p. 19)",
     "lectura": "el mar de las hermanas en un salar costero; el caquetío ya tiene para/parawa 'mar' (atestiguado)",
     "linea": "hermana (taíno y kalinago)",
     "por_que_es_debil": "el parecido lo hacen b-a…g-u-a con un -jari- en medio sin explicar, y el campo 'mar' es el que más pares da por azar"},
]

LEIDO_AL_PASAR = [  # fuera del filtro del script: se dicen y no se cuentan
    {"toponimo": "toponimo-234", "forma": "jagüe",
     "nota": ("Goeje p. 13 junta taíno xagueye 'citerne naturelle' con kalinago šauai 'côte rocheuse, cavernes et "
              "grottes'; jagüey es voz de la esfera (taíno por el castellano) y el lugar tiene «una cueva grande». "
              "El canon lo lee como el árbol andino jagüe (Alvarado p. 178). No pasa el filtro (cueva ≠ agua) y no se "
              "cuenta; se deja para que la campaña lo mire")},
]

PARA_LA_CAMPANA_FIJAS = [
    {"toponimo": "toponimo-239", "forma": "manare", "nivel_actual": "C", "nivel_propuesto": "C",
     "que": "colgar las dos lecturas de lecturas_propuestas (Miguel y Alvarado p. 200); no cambia el nivel"},
    {"toponimo": "toponimo-016", "forma": "capadare", "nivel_actual": "C", "nivel_propuesto": "C",
     "que": "lectura tipo hipotesis (quien: proyecto): ~ lokono kabadaro 'jaguar' (ver cruce.mejores); y corregir en la razón «el lexicón no tiene ninguna palabra para felino»: la tiene como comparanda lokona"},
    {"toponimo": "toponimo-285", "forma": "siraba", "nivel_actual": "descartado", "nivel_propuesto": "C si Miguel acepta media ecuación por el referente; si no, descartado con la lectura colgada",
     "que": "lectura tipo hipotesis: si(ra)ba 'piedra' de las tres hermanas, en el cerro de los petroglifos"},
    {"toponimo": "toponimo-298", "forma": "cimiro", "nivel_actual": "descartado", "nivel_propuesto": "C (cierra con dos piezas de capa baja; contra Esteves)",
     "que": "lectura tipo etimologia-analitica (quien: proyecto): sim(a) 'cerro' + -iro 'diminutivo' = 'cerrito'"},
    {"toponimo": "toponimo-090", "forma": "amuay", "nivel_actual": "C", "nivel_propuesto": "C",
     "que": "lectura tipo hipotesis: kalinago šauai 'acantilado, caverne' (débil, ver cruce.mejores)"},
    {"toponimo": "toponimo-264", "forma": "bajarigua", "nivel_actual": "descartado", "nivel_propuesto": "descartado",
     "que": "lectura tipo hipotesis: bagua/balaua 'mar' (débil)"},
    {"toponimo": "toponimo-018", "forma": "paraguaná", "nivel_actual": "C", "nivel_propuesto": "C",
     "que": "lectura tipo hipotesis: -ná como resto de *naka(n) 'en medio' (taíno nacan, Las Casas; lokono annakan): la tradición de Esteves «en medio del mar» con morfema; DÉBIL (ana.paraguana_en_medio)"},
    {"toponimos": ["toponimo-111 curiana", "toponimo-109 chamuriana", "toponimo-110 jayana", "toponimo-268 cujicana", "toponimo-018 paraguaná"],
     "que": "SÓLO si Miguel adopta el candidato de -ana: lectura tipo hipotesis 'los de X' en cada uno (Curiana 'los de Curi/Coro', Paraguaná 'los del mar'). Sin la decisión, no se cuelga nada"},
]

PARA_EL_LEXICON = [
    {"forma": "-ana", "glosa_propuesta": "los de X, la gente de X (colectivo de gente; gentilicio)",
     "capa_propuesta": "hipotético", "linea": "hermana: lokono (linaje, Brett 1880 pp. 178-179) + kalinago (gentilicio, Breton 1665 p. 416 y 1667)",
     "contra": "taíno Maguana 'la vega menor' (otra función); achagua -na relacional (no apoya)",
     "nota": "es la glosa del morfema-011 en 2-lengua/morfemas.yaml y la del prompt (d21.6): cambiarla mueve canon y motor, decisión de Miguel"},
    {"forma": "nakan", "glosa_propuesta": "en medio, centro",
     "capa_propuesta": "reconstruido (regla de la tanda de las hermanas: dos hermanas = reconstruida)",
     "linea": "hermana: taíno nacan 'medio, en medio' (Las Casas, Historia lib. I cap. XLIV) + lokono annakan 'centro' (Brinton 1871) / a-nnakù-di 'estar en medio' (Perea p. 647)",
     "nota": ("hueco del caquetío (no hay voz para 'en medio'); no sale de un topónimo glosado —sólo la apoya "
              "débilmente la tradición de Paraguaná— y la forma caquetía es nuestra (el segmento común), no de nadie")},
    {"forma": "(jaguar)", "glosa_propuesta": "—", "capa_propuesta": "no se propone",
     "nota": "capadare ~ kabadaro es una sola lengua y un préstamo: se queda como lectura del topónimo, no como palabra"},
]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    tops = cargar_toponimos()
    voces, medida_voces = cargar_voces()
    lenguas = sorted({v["lengua"] for v in voces})
    print(f"topónimos C+descartado con forma de una palabra: {len(tops)}; con algún campo de referente: "
          f"{sum(1 for t in tops if t['campos'])}")
    print("voces cargadas:", medida_voces)
    pares = similares(tops, voces)
    print(f"pares con parecido de forma ≥ {UMBRAL_PARECIDO}: {len(pares)}")
    obs, por_tipo = contar(pares, tops, voces)
    glos, refs = controles(pares, tops, voces, lenguas)
    # sensibilidad: una voz por familia (mismas réplicas, misma semilla)
    keep = familias(voces)
    pares_f = {k: x for k, x in pares.items() if k[1] in keep}
    obs_f, _ = contar(pares_f, tops, voces)
    glos_f, _ = controles(pares_f, tops, voces, lenguas, solo=keep)
    azar = {}
    for l in lenguas:
        azar[l] = {"linea": LINEA.get(l, "?"), "observados": obs.get(l, 0),
                   "azar_permutando_glosas": resumen_azar(glos[l], obs.get(l, 0)),
                   "azar_permutando_referentes": resumen_azar(refs[l], obs.get(l, 0)),
                   "una_voz_por_familia": {"voces": sum(1 for i in keep if voces[i]["lengua"] == l),
                                           "observados": obs_f.get(l, 0),
                                           "azar_permutando_glosas": resumen_azar(glos_f[l], obs_f.get(l, 0))},
                   "por_filtro": {tp: n for (ll, tp), n in por_tipo.items() if ll == l}}
        print(l, azar[l]["observados"], azar[l]["azar_permutando_glosas"], azar[l]["azar_permutando_referentes"],
              "| familias:", azar[l]["una_voz_por_familia"])

    # los candidatos: un par por (topónimo, voz), con todo lo necesario para juzgarlo
    cands = []
    for (ti, vi), (s, r, quitado, f) in pares.items():
        t, v = tops[ti], voces[vi]
        if v["onomastico"]:
            continue
        tipo, por = filtro(t["campos"], t["especies"], v["campos"], v["especies"])
        if not tipo:
            continue
        # control positivo: una voz del propio lexicón que el canon ya leía en
        # ese nombre. Sólo en caquetío y Medina: en una hermana, el mismo
        # parecido no garantiza el mismo significado (carey 'tortuga' ~ kari)
        positivo = v["lengua"] in ("caquetío", "medina") and any(
            difflib.SequenceMatcher(None, p, f).ratio() >= UMBRAL_COGNADO for p in t["ya_leido"])
        cands.append({
            "toponimo": t["id"], "forma": t["forma"], "nivel": t["nivel"],
            "raiz": r, "se_quito": quitado, "lengua": v["lengua"], "linea": LINEA.get(v["lengua"]),
            "voz": v["forma"], "glosa": v["glosa"][:140], "forma_comparada": f, "similitud": round(s, 3),
            "filtro": tipo, "por": por, "control_positivo": positivo,
            "referente": re.sub(r"\s+", " ", t["referente_texto"])[:220],
            "ficha": {k: x for k, x in v["ficha"].items() if x},
        })
    cands.sort(key=lambda c: (-{"paisaje": 2, "clase-viva": 1}[c["filtro"]], -c["similitud"]))
    ecos = []
    for (ti, vi), (s, r, quitado, f) in pares.items():
        v = voces[vi]
        if v["onomastico"] and s >= UMBRAL_COGNADO and v["lengua"] in HERMANAS + PRIMAS:
            ecos.append({"toponimo": tops[ti]["id"], "forma": tops[ti]["forma"], "lengua": v["lengua"],
                         "nombre": v["forma"], "glosa": v["glosa"][:110], "similitud": round(s, 3)})
    ecos.sort(key=lambda e: -e["similitud"])

    # ── lo que se publica ────────────────────────────────────────────────
    def por_lengua(cs, ls):
        return {l: sorted({c["toponimo"] for c in cs if c["lengua"] == l}) for l in ls}

    fuertes = [c for c in cands if c["similitud"] >= UMBRAL_COGNADO]
    hermanas_fuertes = [c for c in fuertes if c["lengua"] in HERMANAS]
    positivos = [c for c in cands if c["control_positivo"]]
    mejores = []
    for m in MEJORES:
        medidos = [c for c in cands if c["toponimo"] == m["toponimo"]]
        medidos.sort(key=lambda c: -c["similitud"])
        mejores.append(dict(m, medido=[f"{c['raiz']} ~ {c['voz']} ({c['lengua']}) '{c['glosa'][:60]}' "
                                        f"{c['similitud']} [{c['filtro']}: {', '.join(c['por'])}]" for c in medidos[:5]]))
    ana_medido = {"lexicon_por_lengua": medir_ana(voces), "achagua_neira_ribero": medir_achagua_ana(),
                  "guayana": medir_guayana()}
    sin_eti = sum(1 for x in ana_medido["guayana"].values() if not x["pasajes_con_aire_de_etimologia"])

    def exceso(l):
        a = azar.get(l)
        if not a:
            return "sin voces"
        g, fam = a["azar_permutando_glosas"], a["una_voz_por_familia"]
        return (f"{a['observados']} topónimos con par frente a {g['media']} por azar (p95 {g['p95']}; réplicas que "
                f"igualan o superan: {g['replicas_que_igualan_o_superan']}); con una voz por familia, "
                f"{fam['observados']} frente a {fam['azar_permutando_glosas']['media']} (réplicas que igualan o "
                f"superan: {fam['azar_permutando_glosas']['replicas_que_igualan_o_superan']})")

    veredicto = {
        "ana": ANA["veredicto"]["candidato"] + " Capa propuesta: " + ANA["veredicto"]["capa_propuesta"] + ".",
        "guayana": (ANA["por_lengua"]["lokono"]["guayana"]["veredicto"]
                    + f". De las {len(ana_medido['guayana'])} obras del repo que escriben el nombre, {sin_eti} no "
                      "traen nada con aire de etimología; los pasajes de las demás se leyeron uno a uno y sólo Goeje "
                      "(p. 5) y Bachiller (p. 277) dicen de dónde viene."),
        "cruce": {
            "hermanas": {l: exceso(l) for l in HERMANAS},
            "primas": {l: exceso(l) for l in PRIMAS},
            "vecina_caribe": exceso("kalinago-caribe"),
            "propia_lengua_y_medina": {l: exceso(l) for l in ("caquetío", "medina")},
            "lectura": (
                "Ninguna hermana pasa del azar de forma limpia. El lokono y el taíno dan lo que da el azar. El "
                "kalinago sale por encima con todas las voces y en el borde con una por familia, y lo que lo empuja "
                "son dos cognados que el canon YA TIENE: la piedra (šiba ~ kiba) y el mar (balaua, barana ~ para). "
                "El achagua sale muy por encima con todas las voces y vuelve al azar con una por familia: lo que se "
                "replica es que el achagua escribe muchas entradas sobre una misma raíz del agua (numa 'boca', uni "
                "'agua'), no un cognado. El caquetío y las voces de Medina salen por encima en las dos cuentas, y son "
                "el control positivo: los topónimos se nombran con las voces que el propio canon sacó de ellos."),
            "candidatos": (f"{len(cands)} pares (topónimo, voz) pasan el filtro de significado; {len(fuertes)} con "
                           f"parecido ≥ {UMBRAL_COGNADO}, {len(hermanas_fuertes)} de ellos en una hermana; "
                           f"{len(positivos)} son control positivo (el canon ya leía esa pieza)"),
        },
        "fauna_re": ("ninguna voz caquetía en -re de animal o planta tiene en una hermana o prima una voz con el "
                     "mismo animal y la misma raíz: todas quedan bajo el umbral (fauna_re)"),
        "mapanare": ("ninguna fuente del repo da su origen; Alvarado la describe y no la etimologiza; en achagua "
                     "mapanarí es una palma. Sí hay una culebra llamada manare (Alvarado p. 200, Portuguesa)"),
        "lo_mejor_del_pase": ("de -ana, que dos hermanas glosan un -na de GENTE y ninguna un -na de lugar, y la "
                              "primaria de Maguana; del cruce, cinco candidatos débiles, ninguno por encima de C"),
    }

    salida = {
        "meta": dict(META, fecha=FECHA, script="6-fusion/scripts/cruzar_toponimos_hermanas.py",
                     parametros={"umbral_parecido": UMBRAL_PARECIDO, "umbral_cognado": UMBRAL_COGNADO,
                                 "min_fonemas": MIN_FONEMAS, "replicas": REPLICAS, "semilla": SEMILLA,
                                 "gu_es_w": GU_ES_W, "niveles": list(NIVELES),
                                 "sufijos_quitados": [f"-{x}: {d}" for x, d in SUFIJOS],
                                 "prefijos_quitados": [f"{x}-: {d}" for x, d in PREFIJOS],
                                 "campos": {c: {"referente": v[0], "glosa": v[1]} for c, v in CAMPOS.items()}},
                     medido={"toponimos_cruzados": len(tops),
                             "toponimos_con_referente_util": sum(1 for t in tops if t["campos"]),
                             "voces": medida_voces, "pares_de_forma": len(pares)}),
        "ana": dict(ANA, medido=ana_medido),
        "cruce": {
            "azar_por_lengua": azar,
            "mejores": mejores,
            "leido_al_pasar": LEIDO_AL_PASAR,
            "control_positivo": [f"{c['forma']} ({c['toponimo']}): {c['raiz']} ~ {c['voz']} ({c['lengua']}) "
                                 f"'{c['glosa'][:50]}' {c['similitud']}" for c in positivos],
            "candidatos_hermanas_y_primas": [c for c in cands if c["lengua"] in HERMANAS + PRIMAS + ("kalinago-caribe",)
                                             and c["similitud"] >= UMBRAL_COGNADO],
            "toponimos_con_par_por_lengua": por_lengua(cands, HERMANAS + PRIMAS + ("kalinago-caribe", "caquetío", "medina")),
            "ecos_onomasticos": {"que_son": "el mismo nombre en un lugar de la hermana o la prima (≥ 0,75): no son palabras y no se cuentan",
                                 "lista": ecos[:40]},
        },
        "fauna_re": cruzar_fauna(voces),
        "lecturas_propuestas": LECTURAS_PROPUESTAS,
        "mapanare": MAPANARE,
        "para_la_campana": PARA_LA_CAMPANA_FIJAS,
        "para_el_lexicon": PARA_EL_LEXICON,
        "veredicto": veredicto,
    }
    tmp = os.environ.get("CRUCE_TMP") or SALIDA
    with io.open(tmp, "w", encoding="utf-8") as fh:
        fh.write("# Generado por 6-fusion/scripts/cruzar_toponimos_hermanas.py — PROPUESTA (regla 5).\n"
                 "# Lo leído a mano va en las constantes del script; lo contado lo cuenta el script.\n")
        yaml.safe_dump(salida, fh, allow_unicode=True, sort_keys=False, width=110)
    print("candidatos:", len(cands), "· fuertes:", len(fuertes), "· hermanas fuertes:", len(hermanas_fuertes),
          "· control positivo:", len(positivos), "· ecos:", len(ecos), "→", os.path.relpath(tmp, R))


if __name__ == "__main__":
    main()
