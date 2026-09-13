# -*- coding: utf-8 -*-
"""
Cruce achagua <-> caquetio POR CONCEPTO (D11 fase 2, #121) - 2026-09-13.

La pregunta: ¿que voces caquetias tienen cognado plausible en achagua (Neira y
Ribero 1762), y el caquetio ATESTIGUADO se parece mas al achagua, al lokono o
al wayuu?

El metodo es el de cruzar_achagua_jahn.py y cruzar_jahn_guajiro.py, con sus
tres lecciones convertidas en codigo:

1. FILTRO DE SIGNIFICADO. Se empareja por la glosa castellana, nunca por
   parecido de forma suelto («ishay» 'fuego' casaba con «kasha» 'luna'). Una
   pareja cuenta solo si la glosa coincide EXACTA: la cabeza del segmento de
   glosa es la misma palabra en los dos lados y ninguno de los dos lleva
   modificador («arbol» ~ «Arbol» si; «arbol de madera dura» ~ «Arbol» no: eso
   es glosa cercana, se registra y no se cuenta).
2. MIRAR LA CAPA. Si la entrada caquetia es reconstruida/hipotetica y sus
   `notas` dicen que la forma sale del lokono o del wayuu, un parecido con ESA
   lengua es `circular`. La filiacion se decide solo sobre la capa atestiguada.
3. DESCONFIAR DE LA PROPIA REGLA. Dos controles:
   - un MODELO NULO por permutacion: para cada concepto se toman tantas
     entradas AL AZAR de la misma lengua como entradas emparejaron por glosa,
     y se mide cuanto parecido sale sin significado. Corrige que el achagua
     (4.276 entradas) ofrezca mas candidatos que el wayuu o el lokono;
   - una PRUEBA DE PREDICCION a dos pliegues: las correspondencias foneticas
     se ven en una mitad de los conceptos y se ponen a predecir en la otra,
     contra la tasa de acierto por azar.

Capas de medicion (se aplican igual a todas las lenguas; NO deciden D5):
  - diacriticos fuera salvo ü y ñ (sin esto `fonemizar` borra ū, ẽ, ë enteras);
  - regla del copista achagua: V/J iniciales ante consonante = u/i;
  - en ortografia linguistica (lokono, wayuu, reconstruido) la h suelta es
    /h/ y pasa a j antes de fonemizar, porque `fonemizar` borra la h (muda en
    castellano);
  - `curiana_fonotactica.fonemizar()` (gu_es_w=False, su defecto; la otra
    opcion se mide como sensibilidad) y `forma_comparable()` para Perea;
  - ü -> u y geminadas colapsadas (como cruzar_jahn_guajiro.py);
  - radicales: se prueba tambien la forma sin un prefijo posesivo/personal y
    sin el sufijo absolutivo declarados en AFIJOS. El modelo nulo usa los
    mismos radicales, asi que el azar paga el mismo precio.

Salida: 6-fusion/cruce_achagua_caquetio_2026-09-13.yaml (PROPUESTA, regla 5).
No toca curiana_lexicon.py, lexicon_*.py ni 3-mundo/corpus/.

    python 6-fusion/scripts/cruzar_achagua_caquetio.py
"""
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
from lexicon_achagua import COMPARANDA_ACHAGUA  # noqa: E402

YAML_ACHAGUA = os.path.join(R, "6-fusion", "achagua_neira_ribero_1762.yaml")
SALIDA = os.path.join(R, "6-fusion", "cruce_achagua_caquetio_2026-09-13.yaml")
FECHA = "2026-09-13"

# ── parametros declarados ANTES de mirar resultados ──────────────────────
UMBRAL_PARECIDO = 0.62      # el de cruzar_jahn_guajiro.py
UMBRAL_COGNADO = 0.75
MIN_FONEMAS = 3             # dos letras no son evidencia (el 80 % de las 441)
REPLICAS = 300
SEMILLA = 1762
GU_ES_W = False             # defecto de curiana_fonotactica; True = sensibilidad
LENGUAS = ("achagua", "lokono", "wayunaiki")     # las que deciden la pregunta
INFORMATIVAS = ("paraujano",)                    # columna extra, no decide
EXCLUIR_CAT = frozenset({"pron", "num"})         # los trabaja otro escriba
ATESTIGUADO = "caquetío-atestiguado"
VOCALES = set("aeiou")

AFIJOS = {  # (prefijos, sufijos) sobre la forma YA fonemizada
    "achagua": (("nu", "ri", "ru", "gua", "wa", "ji", "na"), ("si",)),
    "lokono": (("da", "wa", "li", "to", "bu", "na"), ("n",)),
    "wayunaiki": (("a",), ()),
    "paraujano": (("ta", "a"), ()),
}

SINONIMOS_CRUDOS = {  # declarados: la glosa colonial y la moderna para lo mismo
    "pescado": "pez", "pájaro": "ave", "varón": "hombre", "culebra": "serpiente",
    "demonio": "diablo", "anciano": "viejo", "escuchar": "oír",
}
# Añadidos DESPUÉS de la primera corrida, al auditar los ceros (regla 6): el
# lema achagua existía con otra flexión del mismo sustantivo. Se declaran aparte
# porque se añadieron viendo el vocabulario: `mona` trae `Rrabata` (pl. 76 izq.),
# que se parece a `arata` — ese par nace de esta línea y el informe lo dice.
SINONIMOS_TRAS_AUDITAR_CEROS = {"mona": "mono", "palmera": "palma"}
SINONIMOS_CRUDOS.update(SINONIMOS_TRAS_AUDITAR_CEROS)


# ═════════════════════════════════════════════════════════════════════════
# Glosas castellanas
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
# «Cachama, un pescado»: el segmento que abre con indefinido es una clase, no el
# mismo concepto (medido: `arima` 'pez' casaba con `Carama` 'cachama').
INDEFINIDOS = {_norm_es(x) for x in "un una unos unas".split()}
# Homonimia castellana que el filtro no puede resolver: «este» punto cardinal y
# «Este, q.do no es racional» (demostrativo). Medido en la auditoría de lemas.
HOMONIMOS_DE_GLOSA = {_norm_es("este")}


def es_palabra(w):
    n = _norm_es(w)
    return SINONIMOS.get(n, n)


def conceptos(glosa):
    """[(cabeza, exacto, segmento)] de una glosa. `exacto` = una sola palabra."""
    g = str(glosa or "")
    g = re.sub(r"\([^)]*\)", " ", g)
    g = re.sub(r"\([^)]*$", " ", g)          # paréntesis sin cerrar: «botar (un grupo o montón»
    g = re.sub(r"[,;]\s*-\w+", " ", g)       # «novio, -via»: desinencia del diccionario wayuu, no glosa
    g = re.sub(r"«[^»]*»", " ", g)
    g = re.sub(r"\[[^\]]*\]", " ", g)
    # «Pequeñito, v.g. Padre»: lo que sigue a v.g. es un EJEMPLO, no una glosa
    # (medido: `tata` 'padre' casaba con esa entrada). Igual «&c».
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


def copista(token):
    t = token.strip().lower()
    t = re.sub(r"^v(?=[^aeiouáéíóúy])", "u", t)
    t = re.sub(r"^j(?=[^aeiouáéíóú])", "i", t)
    return t


def radicales(f, lengua):
    pref, suf = AFIJOS.get(lengua, ((), ()))
    out = {f}
    for p in pref:
        if (f.startswith(p) and len(f) - len(p) >= MIN_FONEMAS
                and (len(p) > 1 or f[len(p)] not in VOCALES)):
            out.add(f[len(p):])
    for g in list(out):
        for s in suf:
            if g.endswith(s) and len(g) - len(s) >= MIN_FONEMAS:
                out.add(g[: -len(s)])
    return out


def clave_achagua(principal):
    """La clave que le dio generar_lexicon_achagua.py, si esta en el modulo."""
    f = re.sub(r"[\[\]]", "", principal).strip().strip(".;:,").lower()
    f = re.sub(r"\s+", " ", f)
    f = re.sub(r"^v(?=[^aeiouáéíóúy\s])", "u", f)
    f = re.sub(r"^j(?=[^aeiouáéíóú\s])", "i", f)
    for k in (f, f + "-achagua"):
        if k in COMPARANDA_ACHAGUA:
            return k
    return None


def estrato_lokono(notas):
    n = notas or ""
    if "Perea" in n:
        if "Schumann" in n and "Schultz" not in n:
            return "Schumann 1755 vía Perea 1942"
        if "Schumann" in n:
            return "Schumann 1755 / Schultz 1802 vía Perea 1942"
        return "Schultz 1802 vía Perea 1942"
    marcas = [("Oliver", "Oliver 1989 A-2"), ("Pet 1987", "Pet 1987"),
              ("Goeje", "Goeje 1928"), ("Brinton", "Brinton 1871"), ("Schultz", "Schultz 1800")]
    hallado = [et for m, et in marcas if m in n]
    return " + ".join(hallado) if hallado else "sin estrato declarado"


# ═════════════════════════════════════════════════════════════════════════
# Carga
# ═════════════════════════════════════════════════════════════════════════
def cargar_achagua(gu):
    Y = yaml.safe_load(io.open(YAML_ACHAGUA, encoding="utf-8"))
    filas = [dict(f, _origen="vocabulario") for f in Y["vocabulario"]]

    def walk(n):
        if isinstance(n, dict):
            if "castellano" in n and "achagua" in n:
                filas.append(dict(n, _origen="arte"))
                return
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(Y["arte"]["verbos"])

    entradas = []
    for f in filas:
        texto, cast = f.get("achagua"), f.get("castellano")
        if not texto or not cast:
            continue
        palabras_es = {es_palabra(w) for w in str(cast).split()} | {"dio"}
        variantes = [p.strip() for p in re.split(r"\s*,\s*|\s+vel\s+|\s*;\s*|\s+ó\s+|\s+o\s+", str(texto))
                     if p and p.strip()]
        cands = []
        for var in variantes:
            for t in re.sub(r"[\[\]().+]", " ", var).split():
                if es_palabra(t) in palabras_es:
                    continue                      # «Dios», «Mesa»: castellano dentro
                fb = fon(copista(t), "colonial", gu)
                if len(fb) < MIN_FONEMAS:
                    continue
                for r in radicales(fb, "achagua"):
                    cands.append((r, t.strip(".,;"), r != fb))
        entradas.append({
            "lengua": "achagua", "forma": str(texto).strip(), "glosa": str(cast).strip(),
            "cands": cands, "conceptos": conceptos(cast),
            "ficha": {"forma": str(texto).strip(), "castellano": str(cast).strip(),
                      "pliego": f.get("pliego"), "lado": f.get("lado"),
                      **({"seccion": "arte"} if f["_origen"] == "arte" else {}),
                      "clave_lexicon": clave_achagua(variantes[0]) if variantes else None},
        })
    return entradas, len(Y["vocabulario"])


def cargar_lexicon(lengua, gu):
    entradas = []
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") != lengua or v.get("cat") in EXCLUIR_CAT:
            continue
        base = re.sub(r"-(lokono|achagua|kalinago|wayuu|wayunaiki|paraujano|\d+)$", "", k)
        formas = [base] + ([v["forma_fuente"]] if v.get("forma_fuente") else [])
        cands = []
        for fm in dict.fromkeys(formas):
            fm2 = forma_comparable(fm, v) if lengua == "lokono" else fm
            fb = fon(fm2, "linguistica", gu)
            if len(fb) < MIN_FONEMAS:
                continue
            for r in radicales(fb, lengua):
                cands.append((r, fm, r != fb))
        ficha = {"forma": base, "glosa": v.get("sig")}
        if lengua == "lokono":
            ficha["estrato"] = estrato_lokono(v.get("notas"))
        elif "Captain" in (v.get("notas") or ""):
            ficha["estrato"] = "Captain & Captain 2005"
        elif lengua == "paraujano":
            ficha["estrato"] = "Wilbert 1958-59 vía Oliver 1989 A-2"
        sin_fuente = ficha.get("estrato", "sin estrato declarado") == "sin estrato declarado"
        sesgada = sin_fuente and bool(re.search(r"cognad[oa] (de|con) [^;]*caquet", v.get("notas") or "", re.I))
        if sesgada:
            ficha["aviso"] = "sin fuente y escrita como cognado de una voz caquetía: excluida del cruce"
        entradas.append({"lengua": lengua, "forma": base, "glosa": v.get("sig"), "cands": cands,
                         "conceptos": conceptos(v.get("sig")), "ficha": ficha, "sesgada": sesgada})
    return entradas


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
        elif f.startswith("garif"):
            out.add("garífuna")
        elif f:
            out.add(f)
    return sorted(out)


def cargar_caquetio(gu):
    out = []
    for k, v in CL.VOCABULARIO_BASE.items():
        capa = CL.capa_epistemica(v.get("fuente"))
        if not capa or v.get("cat") in EXCLUIR_CAT:
            continue
        base = re.sub(r"-\d+$", "", k)
        orto = "linguistica" if ("reconstru" in capa or "hipot" in capa) else "colonial"
        cands = [(fon(base, orto, gu), base)]
        if v.get("forma_fuente"):
            cands.append((fon(v["forma_fuente"], "colonial", gu), v["forma_fuente"]))
        cands = list({c[0]: c for c in cands if c[0]}.values())
        out.append({"clave": k, "capa": capa, "sig": v.get("sig"), "cat": v.get("cat"),
                    "forma_fuente": v.get("forma_fuente"), "cands": cands,
                    "conceptos": conceptos(v.get("sig")), "derivada_de": derivada_de(v, capa)})
    return out


# ═════════════════════════════════════════════════════════════════════════
# Medida
# ═════════════════════════════════════════════════════════════════════════
def indexar(entradas):
    exacto, cualquiera = collections.defaultdict(list), collections.defaultdict(list)
    for e in entradas:
        if e.get("sesgada"):
            continue
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
    for cab in exactas_cabezas:
        for e in idx_exacto.get(cab, []):
            if id(e) not in vistos:
                vistos.add(id(e))
                if e["cands"]:
                    exactas.append(e)
                else:                     # glosa exacta pero ninguna forma de 3+ fonemas
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
        return "circular", "la forma caquetía se derivó de esta lengua (o del proto-arahuaco): el parecido es de construcción"
    if sim >= UMBRAL_COGNADO:
        return "cognado-probable", ""
    if sim >= UMBRAL_PARECIDO:
        return "parecido-debil", ""
    return "sin-parecido", ""


def medir(gu, con_nulo=True):
    t0 = time.time()
    ach, n_voc = cargar_achagua(gu)
    lengs = {"achagua": ach}
    for L in LENGUAS[1:] + INFORMATIVAS:
        lengs[L] = cargar_lexicon(L, gu)
    idx = {L: indexar(es) for L, es in lengs.items()}
    caq = cargar_caquetio(gu)

    res = []
    for c in caq:
        corto = max((len(fa) for fa, _ in c["cands"]), default=0) < MIN_FONEMAS
        por = {}
        for L in LENGUAS + INFORMATIVAS:
            exactas, n_cerc, n_cortas = emparejar(c, *idx[L])
            ranking = []
            if not corto:
                for e in exactas:
                    s, _, cb, ca = mejor(c["cands"], [e])
                    ranking.append((s, e, cb, ca))
                ranking.sort(key=lambda x: -x[0])
            sim = ranking[0][0] if ranking else 0.0
            circ = L in c["derivada_de"] or "proto-arahuaco" in c["derivada_de"]
            ver, porque = veredicto(sim, len(exactas), n_cerc, corto, circ, n_cortas)
            por[L] = {"exactas": exactas, "n_cercanas": n_cerc, "n_cortas": n_cortas, "ranking": ranking,
                      "sim": sim, "veredicto": ver, "porque": porque}
        res.append({"c": c, "corto": corto, "por": por})

    # ── modelo nulo sobre la capa atestiguada ──
    rng = random.Random(SEMILLA)
    pool = {L: [e for e in lengs[L] if e["cands"] and not e.get("sesgada")] for L in LENGUAS}
    if con_nulo:
        for r in res:
            if r["c"]["capa"] != ATESTIGUADO or r["corto"]:
                continue
            r["nulo"] = {}
            for L in LENGUAS:
                n = len(r["por"][L]["exactas"])
                if not n:
                    continue
                excl = {id(e) for e in r["por"][L]["exactas"]}
                sims = []
                for _ in range(REPLICAS):
                    muestra, ids = [], set()
                    while len(muestra) < n:
                        e = pool[L][rng.randrange(len(pool[L]))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    sims.append(max(0.0, mejor(r["c"]["cands"], muestra)[0]))
                r["nulo"][L] = sims
    return {"res": res, "lengs": lengs, "idx": idx, "n_voc": n_voc, "pool": pool,
            "segundos": round(time.time() - t0, 1)}


# ═════════════════════════════════════════════════════════════════════════
# Resumen de la capa atestiguada
# ═════════════════════════════════════════════════════════════════════════
def _categoria(conjunto):
    if not conjunto:
        return "ninguna"
    if len(conjunto) > 1:
        return "varias"
    return "solo-" + next(iter(conjunto))


def resumir(M):
    ates = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO]
    utiles = [r for r in ates if not r["corto"]]
    por_lengua = {}
    for L in LENGUAS:
        comp = [r for r in utiles if r["por"][L]["exactas"]]
        obs_p = sum(r["por"][L]["sim"] >= UMBRAL_PARECIDO for r in comp)
        obs_c = sum(r["por"][L]["sim"] >= UMBRAL_COGNADO for r in comp)
        d = {"conceptos_comparables": len(comp),
             "parecidos_ge_umbral": obs_p, "cognado_probable_ge_umbral_cognado": obs_c,
             "tasa_parecido": round(obs_p / len(comp), 3) if comp else None,
             "similitud_media": round(sum(r["por"][L]["sim"] for r in comp) / len(comp), 3) if comp else None,
             "candidatos_por_concepto_media": round(sum(len(r["por"][L]["exactas"]) for r in comp) / len(comp), 2) if comp else None}
        if comp and all("nulo" in r and L in r["nulo"] for r in comp):
            tot_p = [sum(r["nulo"][L][i] >= UMBRAL_PARECIDO for r in comp) for i in range(REPLICAS)]
            tot_c = [sum(r["nulo"][L][i] >= UMBRAL_COGNADO for r in comp) for i in range(REPLICAS)]
            media_nula = sum(sum(r["nulo"][L]) / REPLICAS for r in comp) / len(comp)
            d["azar"] = {
                "parecidos_esperados": round(sum(tot_p) / REPLICAS, 2),
                "cognados_esperados": round(sum(tot_c) / REPLICAS, 2),
                "similitud_media_esperada": round(media_nula, 3),
                "p_parecidos_ge_observado": round(sum(t >= obs_p for t in tot_p) / REPLICAS, 3),
                "p_cognados_ge_observado": round(sum(t >= obs_c for t in tot_c) / REPLICAS, 3),
            }
            d["exceso_de_parecidos_sobre_el_azar"] = round(obs_p - sum(tot_p) / REPLICAS, 2)
        por_lengua[L] = d

    def reparto(filas, usar_nulo_idx=None):
        cnt = collections.Counter()
        for r in filas:
            alcanzan = set()
            for L in LENGUAS:
                if not r["por"][L]["exactas"]:
                    continue
                s = r["nulo"][L][usar_nulo_idx] if usar_nulo_idx is not None else r["por"][L]["sim"]
                if s >= UMBRAL_PARECIDO:
                    alcanzan.add(L)
            cnt[_categoria(alcanzan)] += 1
        return cnt

    claves = ["solo-achagua", "solo-lokono", "solo-wayunaiki", "varias", "ninguna"]
    comparables_alguna = [r for r in utiles if any(r["por"][L]["exactas"] for L in LENGUAS)]
    en_las_tres = [r for r in utiles if all(r["por"][L]["exactas"] for L in LENGUAS)]
    out = {"entradas_atestiguadas_sin_pron_num": len(ates),
           "formas_de_menos_de_tres_fonemas": len(ates) - len(utiles),
           "con_concepto_en_alguna_de_las_tres": len(comparables_alguna),
           "con_concepto_en_las_tres": len(en_las_tres),
           "por_lengua": por_lengua}
    for nombre, filas in (("reparto_conceptos_en_alguna", comparables_alguna),
                          ("reparto_conceptos_en_las_tres", en_las_tres)):
        obs = reparto(filas)
        bloque = {"observado": {k: obs.get(k, 0) for k in claves}}
        if filas and all("nulo" in r for r in filas):
            acum = collections.Counter()
            for i in range(REPLICAS):
                acum.update(reparto(filas, i))
            bloque["esperado_por_azar"] = {k: round(acum.get(k, 0) / REPLICAS, 2) for k in claves}
        varias = collections.Counter()
        for r in filas:
            al = tuple(L for L in LENGUAS if r["por"][L]["exactas"] and r["por"][L]["sim"] >= UMBRAL_PARECIDO)
            if len(al) > 1:
                varias[" + ".join(al)] += 1
        if varias:
            bloque["desglose_de_varias"] = dict(varias)
        out[nombre] = bloque
    return out


# ═════════════════════════════════════════════════════════════════════════
# Prueba de prediccion (regla 3)
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


def nombre_regla(x, y, inicial, lengua="achagua"):
    return f"caq {'#' if inicial else ''}{x} ~ {lengua[:3]} {y}"


def juicio_regla(aplicables, tasa, tasa_azar):
    if aplicables < 5:
        return "sin casos suficientes (menos de 5 aplicables)"
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
    s, _e, cb, _ca = mejor([(a, a)], entradas)
    return cb[0] if cb else None


def prueba_prediccion(M):
    base = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO and not r["corto"]
            and r["por"]["achagua"]["exactas"]]
    base.sort(key=lambda r: r["c"]["clave"])
    pliegues = {"A": base[0::2], "B": base[1::2]}
    rng = random.Random(SEMILLA + 1)
    pool = M["pool"]["achagua"]
    salida = {"diseño": ("Los conceptos atestiguados con glosa exacta en achagua se ordenan por clave y se "
                         "reparten alternos en dos pliegues. En el pliegue de DESCUBRIMIENTO se alinean los pares "
                         f"que ya se parecen (sim >= {UMBRAL_PARECIDO}) y se cuentan las correspondencias "
                         "consonánticas no idénticas; las que tienen 2 apoyos o más se proponen. En el otro pliegue, "
                         "sobre TODOS sus conceptos (se parezcan o no), cada regla predice que donde el caquetío "
                         "tiene X la mejor forma achagua del mismo concepto tiene Y en la posición alineada. La tasa "
                         f"por azar sale de repetir la prueba con entradas achagua al azar ({REPLICAS} réplicas)."),
              "conceptos_en_la_prueba": len(base), "pliegues": {}}
    for nombre, desc in (("A", "B"), ("B", "A")):
        descubrir, probar = pliegues[nombre], pliegues[desc]
        cnt, ejemplos = collections.Counter(), collections.defaultdict(list)
        pares = 0
        for r in descubrir:
            p = r["por"]["achagua"]
            if p["sim"] < UMBRAL_PARECIDO:
                continue
            pares += 1
            s, e, cb, ca = p["ranking"][0]
            for regla in set(reglas_de(ca[0], cb[0])):
                cnt[regla] += 1
                ejemplos[regla].append(f"{ca[1]} ~ {cb[1]}")
        propuestas = [(rg, n) for rg, n in cnt.most_common() if n >= 2][:6]
        bloque = {"descubrimiento_en": nombre, "prueba_en": desc,
                  "pares_parecidos_para_descubrir": pares,
                  "reglas_propuestas": len(propuestas), "reglas": []}
        if not propuestas:
            bloque["nota"] = "ninguna correspondencia consonántica no idéntica con 2 apoyos en este pliegue"
        for (x, y, ini), n in propuestas:
            aplicables = aciertos = 0
            azar_aciertos = azar_aplicables = 0
            for r in probar:
                a = r["c"]["cands"][0][0]
                b = mejor_forma(a, r["por"]["achagua"]["exactas"])
                if b is None:
                    continue
                h = aplica(a, b, x, y, ini)
                if h is None:
                    continue
                aplicables += 1
                aciertos += int(h)
                k = len(r["por"]["achagua"]["exactas"])
                excl = {id(e) for e in r["por"]["achagua"]["exactas"]}
                for _ in range(REPLICAS):
                    muestra = []
                    while len(muestra) < k:
                        e = pool[rng.randrange(len(pool))]
                        if id(e) not in excl and e not in muestra:
                            muestra.append(e)
                    bz = mejor_forma(a, muestra)
                    if bz is None:
                        continue
                    hz = aplica(a, bz, x, y, ini)
                    if hz is not None:
                        azar_aplicables += 1
                        azar_aciertos += int(hz)
            tasa = round(aciertos / aplicables, 3) if aplicables else None
            tasa_azar = round(azar_aciertos / azar_aplicables, 3) if azar_aplicables else None
            juicio = juicio_regla(aplicables, tasa, tasa_azar)
            bloque["reglas"].append({
                "regla": nombre_regla(x, y, ini), "apoyos_al_descubrir": n,
                "ejemplos_al_descubrir": ejemplos[(x, y, ini)][:4],
                "aplicables_en_prueba": aplicables, "aciertos": aciertos, "fallos": aplicables - aciertos,
                "tasa_de_acierto": tasa, "tasa_por_azar": tasa_azar, "juicio": juicio})
        salida["pliegues"][nombre] = bloque
    return salida


# ═════════════════════════════════════════════════════════════════════════
# Salida
# ═════════════════════════════════════════════════════════════════════════
def prueba_dejando_fuera(M):
    """Cada correspondencia vista en un par parecido predice sobre los DEMÁS conceptos."""
    rng = random.Random(SEMILLA + 2)
    out = {"diseño": ("Para cada lengua se alinean los pares atestiguados que se parecen (cognado-probable o "
                      "parecido-debil) y se anotan sus correspondencias consonánticas no idénticas, aunque tengan un "
                      "solo apoyo. Cada una predice sobre TODOS los demás conceptos atestiguados con glosa exacta en "
                      "esa lengua (fuera los que la sugirieron): donde el caquetío tiene X, la forma más parecida de "
                      "la comparanda con el mismo concepto tiene Y en la posición alineada. La tasa por azar repite la "
                      f"prueba con entradas al azar de la misma lengua ({REPLICAS} réplicas). Juicio: con 5 casos "
                      "aplicables o más, predice si acierta al menos la mitad y al menos el doble que el azar.")}
    for L in LENGUAS:
        base = [r for r in M["res"] if r["c"]["capa"] == ATESTIGUADO and not r["corto"] and r["por"][L]["exactas"]]
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
                excl = {id(e) for e in r["por"][L]["exactas"]}
                for _ in range(REPLICAS):
                    muestra, ids = [], set()
                    while len(muestra) < k:
                        e = pool[rng.randrange(len(pool))]
                        if id(e) in excl or id(e) in ids:
                            continue
                        ids.add(id(e))
                        muestra.append(e)
                    bz = mejor_forma(a, muestra)
                    hz = aplica(a, bz, x, y, ini) if bz else None
                    if hz is not None:
                        az_ap += 1
                        az_ac += int(hz)
            tasa = round(aciertos / aplicables, 3) if aplicables else None
            tasa_azar = round(az_ac / az_ap, 3) if az_ap else None
            reglas.append({"regla": nombre_regla(x, y, ini, L), "apoyos": n,
                           "visto_en": [f"{k}: {par}" for k, par in apoyos[regla]],
                           "aplicables": aplicables, "aciertos": aciertos, "fallos": aplicables - aciertos,
                           "tasa_de_acierto": tasa, "tasa_por_azar": tasa_azar,
                           "juicio": juicio_regla(aplicables, tasa, tasa_azar), "casos": casos[:20]})
        out[L] = {"pares_parecidos": pares, "conceptos_con_glosa_exacta": len(base), "reglas": reglas}
    return out


def ficha_de(e, cb, sim):
    d = dict(e["ficha"])
    d["comparado_como"] = cb[0] + (" (radical)" if cb[2] else "")
    d["similitud"] = round(sim, 3)
    return d


def registro(r):
    c, por = r["c"], r["por"]
    reg = {"caquetio": {"forma": c["clave"], **({"forma_fuente": c["forma_fuente"]} if c["forma_fuente"] else {}),
                        "capa": c["capa"], "cat": c["cat"], "glosa": c["sig"],
                        "fonemizada": " / ".join(fa for fa, _ in c["cands"])},
           "conceptos_exactos": sorted({cab for cab, ex, _ in c["conceptos"] if ex})}
    if c["derivada_de"]:
        reg["caquetio"]["forma_derivada_de"] = c["derivada_de"]
    topes = {"achagua": 3, "lokono": 3, "wayunaiki": 2, "paraujano": 2}
    for L in LENGUAS + INFORMATIVAS:
        p = por[L]
        if p["ranking"]:
            reg[L] = [ficha_de(e, cb, s) for s, e, cb, _ca in p["ranking"][: topes[L]]]
            if len(p["exactas"]) > topes[L]:
                reg[L].append({"mas_entradas_con_la_misma_glosa": len(p["exactas"]) - topes[L]})
    reg["similitud"] = {L: (round(por[L]["sim"], 3) if por[L]["ranking"] else None) for L in LENGUAS + INFORMATIVAS}
    reg["veredictos"] = {L: por[L]["veredicto"] for L in LENGUAS + INFORMATIVAS}
    reg["veredicto"] = por["achagua"]["veredicto"]
    candidatas = [(por[L]["sim"], L) for L in LENGUAS
                  if por[L]["veredicto"] in ("cognado-probable", "parecido-debil")]
    reg["se_parece_mas_a"] = max(candidatas)[1] if candidatas else "ninguna"
    # la linea de por que
    trozos = []
    for L in LENGUAS:
        p = por[L]
        if p["ranking"]:
            s, e, cb, ca = p["ranking"][0]
            barato = (" (3 fonemas: parecido barato)"
                      if s >= UMBRAL_PARECIDO and min(len(cb[0]), len(ca[0])) <= MIN_FONEMAS else "")
            trozos.append(f"{L} {cb[1]} «{e['glosa'][:40]}» {s:.2f}{barato}")
        elif p["porque"]:
            trozos.append(f"{L}: {p['porque']}")
    extra = [f"{L}: {por[L]['porque']}" for L in LENGUAS if por[L]["veredicto"] == "circular"]
    if "taíno" in c["derivada_de"]:
        extra.append("la forma caquetía sale del taíno: un parecido puede ser préstamo panamericano y no decide filiación")
    if r["corto"]:
        reg["por_que"] = "forma caquetía de menos de tres fonemas: no cuenta como evidencia"
    else:
        reg["por_que"] = " · ".join(trozos + extra)
    return reg


def main():
    print("midiendo (gu_es_w=False) ...")
    M = medir(GU_ES_W)
    print(f"  {M['segundos']} s")
    print("midiendo la sensibilidad (gu_es_w=True) ...")
    M2 = medir(not GU_ES_W)
    print(f"  {M2['segundos']} s")

    resumen = resumir(M)
    resumen_sens = resumir(M2)
    prueba = {"dos_pliegues": prueba_prediccion(M), "dejando_fuera": prueba_dejando_fuera(M)}

    res = M["res"]
    comparables = [r for r in res if any(r["por"][L]["exactas"] or r["por"][L]["n_cortas"]
                                         for L in LENGUAS + INFORMATIVAS)]
    solo_cercana = [r for r in res if r not in comparables
                    and any(r["por"][L]["n_cercanas"] for L in LENGUAS + INFORMATIVAS)]
    rango = {"cognado-probable": 0, "parecido-debil": 1, "circular": 2, "sin-parecido": 3, "no-comparable": 4}
    comparables.sort(key=lambda r: (r["c"]["capa"] != ATESTIGUADO, r["c"]["capa"],
                                    rango[r["por"]["achagua"]["veredicto"]], -r["por"]["achagua"]["sim"]))
    registros = [registro(r) for r in comparables]

    # top 10 atestiguados con el achagua
    ates_ach = [r for r in res if r["c"]["capa"] == ATESTIGUADO
                and r["por"]["achagua"]["veredicto"] in ("cognado-probable", "parecido-debil")]
    ates_ach.sort(key=lambda r: -r["por"]["achagua"]["sim"])
    top = []
    for r in ates_ach[:10]:
        s, e, cb, ca = r["por"]["achagua"]["ranking"][0]
        top.append({"caquetio": r["c"]["clave"], "glosa": r["c"]["sig"], "achagua": cb[1],
                    "achagua_entrada": e["ficha"]["forma"], "castellano": e["ficha"]["castellano"],
                    "pliego": f"{e['ficha']['pliego']} {e['ficha']['lado']}", "similitud": round(s, 3),
                    "veredicto": r["por"]["achagua"]["veredicto"],
                    "lokono": round(r["por"]["lokono"]["sim"], 3) if r["por"]["lokono"]["ranking"] else None,
                    "wayunaiki": round(r["por"]["wayunaiki"]["sim"], 3) if r["por"]["wayunaiki"]["ranking"] else None})

    circulares = []
    for r in res:
        for L in LENGUAS + INFORMATIVAS:
            if r["por"][L]["veredicto"] == "circular":
                s, e, cb, ca = r["por"][L]["ranking"][0]
                circulares.append({"caquetio": r["c"]["clave"], "capa": r["c"]["capa"], "lengua": L,
                                   "comparanda": cb[1], "similitud": round(s, 3),
                                   "forma_derivada_de": r["c"]["derivada_de"]})

    por_capa = collections.defaultdict(collections.Counter)
    for r in res:
        if any(r["por"][L]["exactas"] for L in LENGUAS):
            por_capa[r["c"]["capa"]][r["por"]["achagua"]["veredicto"]] += 1

    # control: la trampa de Jahn/Fabo (agua = mena)
    idx_ex = M["idx"]["achagua"][0]
    control = {k: sorted({e["ficha"]["forma"] for e in idx_ex.get(es_palabra(k), [])}) for k in ("agua", "mar")}
    mena = sorted({e["ficha"]["castellano"] for e in M["lengs"]["achagua"]
                   if any(cb[0] == "mena" for cb in e["cands"])})

    n_caq = collections.Counter(r["c"]["capa"] for r in res)
    meta = {
        "obra": "neira-ribero-1762",
        "medido": FECHA,
        "script": "6-fusion/scripts/cruzar_achagua_caquetio.py",
        "issue": "#121 (D11 fase 2)",
        "estado": "PROPUESTA (regla 5). No toca el lexicón ni el corpus. Cifras emitidas por el script.",
        "pregunta": ("¿Qué voces caquetías tienen cognado plausible en achagua (Neira y Ribero 1762), y el caquetío "
                     "ATESTIGUADO se parece más al achagua, al lokono o al wayuu?"),
        "insumos": {
            "achagua_filas_con_forma": len(M["lengs"]["achagua"]),
            "achagua_entradas_del_vocabulario": M["n_voc"],
            "achagua_origen": "6-fusion/achagua_neira_ribero_1762.yaml (vocabulario + arte.verbos; sin pronombres ni numerales del arte)",
            "lokono_entradas": len(M["lengs"]["lokono"]),
            "wayunaiki_entradas": len(M["lengs"]["wayunaiki"]),
            "paraujano_entradas": len(M["lengs"]["paraujano"]),
            "caquetio_por_capa_sin_pron_num": dict(n_caq),
            "excluidas_por_categoria": sorted(EXCLUIR_CAT),
        },
        "parametros": {
            "umbral_parecido": UMBRAL_PARECIDO, "umbral_cognado": UMBRAL_COGNADO,
            "min_fonemas": MIN_FONEMAS, "replicas_del_modelo_nulo": REPLICAS, "semilla": SEMILLA,
            "gu_es_w": GU_ES_W, "similitud": "difflib.SequenceMatcher.ratio() sobre la forma fonemizada",
            "afijos_probados": {L: {"prefijos": list(p), "sufijos": list(s)} for L, (p, s) in AFIJOS.items()},
            "sinonimos_de_glosa": SINONIMOS_CRUDOS,
            "sinonimos_añadidos_tras_auditar_ceros": {
                **SINONIMOS_TRAS_AUDITAR_CEROS,
                "porque": ("añadidos después de la primera corrida, al verificar los ceros: el achagua tenía «Mona» "
                           "y «Palma» y el filtro no los veía. Se añadieron VIENDO el vocabulario; el par arata ~ "
                           "Rrabata sale de aquí y no debe contarse como hallazgo a ciegas"),
            },
        },
        "metodo": [
            "FILTRO DE SIGNIFICADO: cada glosa se parte en segmentos (coma, punto y coma, barra, «o», «vel»; nunca «y», "
            "para que «maíz tostado y miel» no case con «miel»). Cuenta solo la glosa EXACTA: el segmento es una sola "
            "palabra en los dos lados, tras normalizar la ortografía castellana colonial (muger=mujer, v=b, z=s, plural). "
            "Lo que sigue a «v.g.» es ejemplo y se descarta; el segmento que abre con indefinido («Cachama, un pescado») "
            "es una clase y no cuenta como exacto.",
            "MIRAR LA CAPA: la entrada caquetía reconstruida o hipotética cuya `notas` dice de qué lengua sale la forma "
            "(«cognado en lokono», «desde el WAYUU», «etiquetada `lokono/garifuna`», «< ... Wayunaiki») es CIRCULAR con "
            "esa lengua. Si sale del proto-arahuaco, es circular con todas. El resumen de filiación usa solo la capa atestiguada.",
            "SESGO INVERSO: se excluyen las entradas comparanda sin fuente cuya `notas` dice que se escribieron como "
            "cognado de una voz caquetía («Lokono katsi; cognado de cati caquetío»): compararlas mediría la mano que "
            "las escribió, no la lengua.",
            "DESCONFIAR: modelo nulo por permutación (mismo número de entradas al azar de la misma lengua, mismos "
            "radicales) y prueba de predicción a dos pliegues para las correspondencias.",
        ],
        "capas_de_medicion": [
            "diacríticos fuera salvo ü y ñ (fonemizar borraba ū, ẽ, ë enteras)",
            "copista achagua: V/J iniciales ante consonante = u/i, en cada palabra de la forma",
            "ortografía lingüística (lokono, wayuu, reconstruido): la h suelta pasa a j, porque fonemizar borra la h",
            "curiana_fonotactica.fonemizar(); OJO: lleva <ch> a k y <sh> a s en todas las lenguas por igual",
            "forma_comparable() colapsa las geminadas de Perea; además se colapsan todas las repeticiones y ü -> u",
            "en las formas achagua se descartan las palabras que son castellano de la propia glosa («Dios», «Mesa»)",
        ],
        "control_trampa_jahn": {
            "achagua_con_glosa_exacta_agua": control["agua"],
            "achagua_con_glosa_exacta_mar": control["mar"],
            "entradas_de_neira_con_forma_mena": mena,
            "lectura": "Jahn/Fabo es control, no comparanda: aquí solo entra Neira y Ribero.",
        },
        "comparanda_excluida_por_sesgo_inverso": sorted(
            f"{e['lengua']} {e['forma']} «{e['glosa']}»" for L in M["lengs"] for e in M["lengs"][L] if e.get("sesgada")),
        "resumen_atestiguado": resumen,
        "sensibilidad_gu_es_w_true": {
            L: {k: resumen_sens["por_lengua"][L].get(k) for k in ("conceptos_comparables", "parecidos_ge_umbral",
                                                              "cognado_probable_ge_umbral_cognado")}
            | {"parecidos_esperados": resumen_sens["por_lengua"][L].get("azar", {}).get("parecidos_esperados")}
            for L in LENGUAS
        } | {"reparto_conceptos_en_las_tres": resumen_sens["reparto_conceptos_en_las_tres"]},
        "veredicto_achagua_por_capa": {k: dict(v) for k, v in sorted(por_capa.items())},
        "top10_atestiguado_achagua": top,
        "circulares": circulares,
        "prueba_de_prediccion": prueba,
        "registros": {
            "conceptos_con_glosa_exacta_en_alguna_lengua": len(registros),
            "solo_glosa_cercana_no_listados": len(solo_cercana),
            "solo_glosa_cercana_claves": sorted(r["c"]["clave"] for r in solo_cercana),
            "sin_concepto_en_ninguna_comparanda": len(res) - len(registros) - len(solo_cercana),
        },
        "advertencias": [
            "Las formas achagua son TRANSCRIPCIÓN POR VISIÓN (dos pasadas, 2026-09-12): verificar el pliego en imagen "
            "antes de citar cualquier forma de este cruce como exacta.",
            "Un parecido de forma con glosa exacta es un CANDIDATO a cognado, no un cognado: ninguno de estos pares ha "
            "pasado por correspondencias regulares verificadas (la prueba de predicción dice cuánto aguantan).",
            "Glosa exacta no es significado idéntico: el castellano del jesuita de 1762 y el de Zavala 2015 no recortan "
            "igual el mundo. Y los préstamos panamericanos (tainismos) pueden dar parecido sin filiación.",
            "El filtro no ve la aposición sin artículo («Pajaro, Dios te de», «Raya, pescado»): esos lemas entran "
            "como glosa exacta de su hiperónimo. Se auditaron a mano los emparejamientos de lema con varios "
            "segmentos: los que quedan así dan sin-parecido y solo engordan el número de candidatos, que el modelo "
            "nulo ya cobra.",
            "La capa atestiguada es mayoritariamente fitonimia y zoonimia de Paraguaná y Coro (Zavala): conceptos "
            "que un vocabulario de los Llanos rara vez nombra con la misma glosa. El hueco mide la lista, no la lengua.",
        ],
    }
    salida = {"meta": meta, "conceptos": registros}

    cab = (
        "# ══════════════════════════════════════════════════════════════════════\n"
        "# CRUCE ACHAGUA <-> CAQUETIO POR CONCEPTO — D11 fase 2 (#121)\n"
        "# PROPUESTA (regla 5). Generado por 6-fusion/scripts/cruzar_achagua_caquetio.py:\n"
        "# no se edita a mano; se corrige el script o sus insumos y se regenera.\n"
        "# Toda cifra de `meta` la emite el script (regla 1).\n"
        "# ══════════════════════════════════════════════════════════════════════\n"
    )
    with io.open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(cab)
        yaml.safe_dump(salida, fh, allow_unicode=True, sort_keys=False, width=110)

    # ── consola ──
    print(f"\nconceptos comparables (alguna lengua, todas las capas): {len(registros)}")
    print("\n═══ RESUMEN, capa atestiguada ═══")
    for L, d in resumen["por_lengua"].items():
        az = d.get("azar", {})
        print(f"  {L:<10} comparables {d['conceptos_comparables']:>3} · parecidos {d['parecidos_ge_umbral']:>3} "
              f"(azar {az.get('parecidos_esperados')}, p={az.get('p_parecidos_ge_observado')}) · "
              f"cognado-probable {d['cognado_probable_ge_umbral_cognado']} (azar {az.get('cognados_esperados')}) · "
              f"sim media {d['similitud_media']} (azar {az.get('similitud_media_esperada')})")
    for k in ("reparto_conceptos_en_alguna", "reparto_conceptos_en_las_tres"):
        print(f"  {k}: {resumen[k]}")
    print("\n═══ TOP 10 atestiguado ~ achagua ═══")
    for t in top:
        print(f"  {t['caquetio']:<12} «{t['glosa'][:28]}»  ~ {t['achagua']:<14} ({t['castellano'][:22]}, pl. {t['pliego']})"
              f"  {t['similitud']}  {t['veredicto']}   lok {t['lokono']} way {t['wayunaiki']}")
    print(f"\n═══ CIRCULARES: {len(circulares)} ═══")
    for c in circulares:
        print(f"  {c['caquetio']:<10} {c['capa']:<24} {c['lengua']:<10} {c['comparanda']:<14} {c['similitud']}  <- {c['forma_derivada_de']}")
    print("\n═══ PRUEBA DE PREDICCIÓN ═══")
    for L in LENGUAS:
        b = prueba["dejando_fuera"][L]
        print(f"  [{L}] dejando fuera: {b['pares_parecidos']} pares parecidos, {len(b['reglas'])} reglas")
        for rg in b["reglas"]:
            print(f"    {rg['regla']:<16} apoyos {rg['apoyos']} · {rg['aciertos']}/{rg['aplicables']}"
                  f" (tasa {rg['tasa_de_acierto']}, azar {rg['tasa_por_azar']}) · {rg['juicio']}")
    for nombre, b in prueba["dos_pliegues"]["pliegues"].items():
        print(f"  pliegue {nombre}->{b['prueba_en']}: {b['pares_parecidos_para_descubrir']} pares, {b['reglas_propuestas']} reglas")
        for rg in b["reglas"]:
            print(f"    {rg['regla']:<18} apoyos {rg['apoyos_al_descubrir']} · {rg['aciertos']}/{rg['aplicables_en_prueba']}"
                  f" (tasa {rg['tasa_de_acierto']}, azar {rg['tasa_por_azar']}) · {rg['juicio']}")
    print(f"\n✓ {os.path.relpath(SALIDA, R)}")


if __name__ == "__main__":
    main()
