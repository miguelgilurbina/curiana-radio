"""Las cifras de la minería del ARTE achagua (Neira y Ribero 1762, pliegos 7-23).

Tercera campaña de minería, parcela M4 (2026-09-22). La lectura del arte es por
visión y vive en `6-fusion/achagua_arte_neira_ribero_2026-09-22.yaml`; este
script mide lo que esa lectura deja preguntar al CANON caquetío, para que
ninguna cifra del YAML ni del issue se escriba a mano (regla 1):

1. `ka-`/`ma-`: ¿hay en la capa caquetío-atestiguada formas que empiecen así,
   y qué dicen sus glosas verbatim? (pregunta 4)
2. Las formas de los nominalizadores que el arte describe —agentivo `-erri`,
   relativo de paciente `-nicay`, nombre abstracto en `-si`— ¿aparecen al
   final de formas caquetías atestiguadas, y con qué glosa? (pregunta 5)
3. La trampa `-cana`: el arte llama «nombres verbalizados q.e tienen el cana» a
   `Cagicunacana` 'yo pecador' (ca- + nombre + -ca + -na 1sg). Cuántas formas
   achagua fonemizadas acaban en `kana`, que es la cadena del plural `-kana`
   del proyecto. (pregunta 6)
4. `gudamuen` 'dos' contra el `juchama-` achagua (la raíz que queda al quitar
   el clasificador, arte pliego 56-57) y contra las otras hermanas, con un
   modelo nulo: la misma medida contra TODAS las formas achagua. (pregunta 7)

Uso:
    python 6-fusion/scripts/medir_arte_achagua.py            # escribe el YAML
    python 6-fusion/scripts/medir_arte_achagua.py --check    # mide sin escribir

No toca `curiana_lexicon.py`, `lexicon_achagua.py` ni su YAML: sólo los lee.
"""

import argparse
import difflib
import io
import os
import re
import sys
import unicodedata

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
SIM = os.path.join(RAIZ, "curiana_sim")
sys.path.insert(0, SIM)

import curiana_lexicon as CL  # noqa: E402
from curiana_fonotactica import fonemizar  # noqa: E402
from lexicon_achagua import COMPARANDA_ACHAGUA  # noqa: E402
from lexicon_zavala import GLOSARIO_ZAVALA  # noqa: E402

SALIDA = os.path.join(RAIZ, "6-fusion", "medicion_arte_achagua_2026-09-22.yaml")
CAPA = "caquetío-atestiguado"


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def copista(token):
    """V/J iniciales ante consonante = u/i (clave del copista, meta del YAML de 09-12)."""
    t = token.strip().lower()
    t = re.sub(r"^v(?=[^aeiouáéíóúy])", "u", t)
    t = re.sub(r"^j(?=[^aeiouáéíóú])", "i", t)
    return t


def fon(forma, achagua=False):
    f = copista(forma) if achagua else forma
    f = fonemizar(f).replace("ü", "u")
    return re.sub(r"(.)\1+", r"\1", f)


def ratio(a, b):
    return round(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 3)


# ── la capa atestiguada, con su glosa verbatim ──────────────────────────────
def atestiguadas():
    """[(clave, glosa)] de la capa caquetío-atestiguado. Si la entrada tiene
    `glosa_fuente` (Zavala), ésa es la glosa: es la verbatim; si no, `sig`."""
    out = {}
    for k, v in CL.VOCABULARIO_BASE.items():
        if v.get("fuente") == CAPA:
            out[k] = v.get("glosa_fuente") or v.get("sig") or ""
    for k, v in GLOSARIO_ZAVALA.items():
        if v.get("fuente") == CAPA and k not in out:
            out[k] = v.get("glosa_fuente") or v.get("sig") or ""
    return sorted(out.items())


MARCAS_ATRIB = re.compile(r"\b(sin|no|hay|tiene|tener|con|lleno|llena|abundan\w*|mucho\w*)\b", re.I)
MARCAS_AGENTE = re.compile(r"\b(el que|la que|que \w+|\w+dor|\w+dora|\w+ero|\w+era|conocedor|jefe)\b", re.I)


def sonda_ka_ma(capa):
    filas = []
    for k, g in capa:
        f = fon(k)
        if f.startswith(("ka", "ma")) and len(f) >= 4:
            filas.append({
                "forma": k, "fonemica": f, "prefijo_aparente": f[:2] + "-",
                "glosa_verbatim": g,
                "marca_en_la_glosa": sorted({m.lower() for m in MARCAS_ATRIB.findall(g)}) or None,
            })
    return filas


FINALES_NOMINALIZADOR = {
    "-eri / -iri / -ari (agentivo achagua -erri, arte p. 4-6, 9, 19)": ("eri", "iri", "ari"),
    "-nikai / -kai (relativo de paciente -nicay, arte p. 4-5, 8-9)": ("nikai", "kai"),
    "-si (nombre abstracto y absoluto -si, arte p. 2, 11, 13, 32)": ("si",),
}


def sonda_nominalizadores(capa):
    out = {}
    for rotulo, finales in FINALES_NOMINALIZADOR.items():
        filas = []
        for k, g in capa:
            f = fon(k)
            fin = next((x for x in finales if f.endswith(x) and len(f) > len(x) + 2), None)
            if fin:
                filas.append({
                    "forma": k, "fonemica": f, "final": "-" + fin, "glosa_verbatim": g,
                    "glosa_de_agente_o_de_accion": bool(MARCAS_AGENTE.search(g)),
                })
        out[rotulo] = {"formas": len(filas),
                       "con_glosa_de_agente_o_de_accion": sum(r["glosa_de_agente_o_de_accion"] for r in filas),
                       "detalle": filas}
    return out


def trampa_kana():
    filas = []
    for k, v in COMPARANDA_ACHAGUA.items():
        ff = v.get("forma_fuente") or k
        for tok in re.split(r"[\s,]+", ff):
            if tok and fon(tok, achagua=True).endswith("kana"):
                filas.append({"forma": tok, "glosa": v.get("sig", "")})
                break
    plurales = [r for r in filas if re.search(r"\b(plural|muchos|muchas|los|las)\b", r["glosa"], re.I)]
    return {
        "entradas_achagua": len(COMPARANDA_ACHAGUA),
        "formas_que_acaban_en_kana_fonemizadas": len(filas),
        "de_ellas_con_glosa_plural_o_colectiva": len(plurales),
        "muestra": filas[:25],
        "muestra_de_las_de_glosa_plural": plurales[:10],
    }


def numerales():
    gud = fon("gudamuen")
    dianas = {
        "achagua juchama- (raíz de 'dos' sin clasificador; arte/vocab. pliego 56-57)": ("juchama", True),
        "achagua Juchamata ('dos' general, pliego 56 der.)": ("Juchamata", True),
        "achagua Juchamana ('dos' hombres, pliego 56 der.)": ("Juchamana", True),
        "lokono bian (Pet 1987, lexicón)": ("bian", False),
        "lokono biama (Brinton 1871, lexicón)": ("biama", False),
        "wayuu piama (el que enseñaba el canon; D11)": ("piama", False),
    }
    medidas = {r: ratio(gud, fon(f, a)) for r, (f, a) in dianas.items()}

    # modelo nulo: gudamuen contra TODAS las formas achagua (tokens sueltos, >= 4 fonemas)
    tokens = set()
    for k, v in COMPARANDA_ACHAGUA.items():
        for tok in re.split(r"[\s,]+", v.get("forma_fuente") or k):
            f = fon(tok, achagua=True)
            if len(f) >= 4:
                tokens.add(f)
    nulo = sorted(ratio(gud, t) for t in tokens)
    juch = medidas["achagua juchama- (raíz de 'dos' sin clasificador; arte/vocab. pliego 56-57)"]
    iguales_o_mas = sum(1 for x in nulo if x >= juch)

    # la sílaba compartida: ¿cuán barato es tener «am»?
    def tasa_am(formas):
        formas = [f for f in formas if len(f) >= 4]
        return round(100 * sum("am" in f for f in formas) / len(formas), 1) if formas else None

    capa = [fon(k) for k, _ in atestiguadas()]
    return {
        "gudamuen_fonemica": gud,
        "similitud_difflib": medidas,
        "modelo_nulo": {
            "que_mide": "similitud de gudamuen contra cada forma achagua distinta (tokens de >= 4 fonemas, "
                        "fonemizados con la clave del copista), para saber si el parecido con juchama- es raro",
            "formas_achagua": len(nulo),
            "mediana": nulo[len(nulo) // 2],
            "percentil_95": nulo[int(0.95 * (len(nulo) - 1))],
            "maximo": nulo[-1],
            "formas_achagua_tan_o_mas_parecidas_que_juchama": iguales_o_mas,
            "proporcion": round(iguales_o_mas / len(nulo), 4),
        },
        "silaba_am": {
            "que_mide": "porcentaje de formas (>= 4 fonemas) que contienen «am»: el elemento que 'dos' comparte "
                        "en achagua (juchAMa), lokono (biAMa), wayuu (piAMa) y caquetío (gudAMuen)",
            "caquetio_atestiguado_pct": tasa_am(capa),
            "achagua_pct": tasa_am(list(tokens)),
        },
    }


GILIJ_OCR = os.path.join(RAIZ, "fuentes_caquetios", "Gilij_1782_Saggio_Storia_Americana_vol3.ocr.txt")
# Patrones SIN tildes (el texto se compara sin marcas diacríticas) y con la ſ larga
# que el OCR lee como f. «Acciàgua» es como Gilij escribe achagua; «Arnuàca» es como
# el OCR leyó su «Aruàca» (p. 205): por eso la n opcional.
PATRONES_GILIJ = {
    "achagua (Acciagua)": r"acc?h?[ij]?agu",
    "aruaca / lokono (Aruaca)": r"ar[n]?[uv]ac",
    "maipure": r"maip[uv]r",
    "caquetio (caquet-, cachet-, cacchet-, caiquet-)": r"ca[iy]?c?[cq]u?h?e[tf]",
    "Coro": r"\bcoro\b",
    "Curiana / Coriana": r"c[ou]rian",
    "Paraguana": r"paraguan",
    "Barquisimeto": r"barqui[fs]",
    "guajiro / goajiro": r"g[uo]a[jg]ir",
}


def gilij():
    if not os.path.exists(GILIJ_OCR):
        return {"aviso": "no está el OCR del tomo III"}
    t = open(GILIJ_OCR, encoding="utf-8").read()
    t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    paginas = len(re.findall(r"^=== pdf ", t, re.M))
    cuerpos = re.split(r"^=== pdf \d+[^\n]*\n", t, flags=re.M)[1:]
    vacias = sum(1 for c in cuerpos if len(c.strip()) < 300)
    out = {"archivo": os.path.relpath(GILIJ_OCR, RAIZ).replace("\\", "/"), "paginas_ocr": paginas,
           "paginas_casi_vacias_menos_de_300_caracteres": vacias,
           "aviso": "OCR = pista. Cada acierto se mira en la imagen antes de citarlo; un cero mide este OCR",
           "patrones": {}}
    for rot, pat in PATRONES_GILIJ.items():
        hits = []
        for m in re.finditer(pat, t, re.I):
            pdf = re.findall(r"^=== pdf (\d+)", t[: m.start()], re.M)
            hits.append(int(pdf[-1]) if pdf else None)
        out["patrones"][rot] = {"regex": pat, "aciertos": len(hits), "pdf": sorted(set(hits))}
    return out


def medir():
    capa = atestiguadas()
    return {
        "meta": {
            "que_es": "Cifras de la parcela M4 (arte achagua de Neira y Ribero 1762). Las emite "
                      "6-fusion/scripts/medir_arte_achagua.py; no se editan a mano (regla 1).",
            "fecha": "2026-09-22",
            "capa_caquetia_leida": CAPA,
            "entradas_de_la_capa": len(capa),
            "normalizacion": "curiana_fonotactica.fonemizar (la del cruce de 2026-09-13), geminadas colapsadas; "
                             "en achagua, antes, la clave del copista (V/J iniciales ante consonante = u/i)",
            "aviso": "una forma que empieza por ka-/ma- o acaba en -eri/-si NO es un morfema: es la pregunta. "
                     "El juicio, forma a forma y con la glosa verbatim, está en el YAML de la parcela",
        },
        "sonda_ka_ma": sonda_ka_ma(capa),
        "sonda_nominalizadores": sonda_nominalizadores(capa),
        "trampa_kana": trampa_kana(),
        "numerales": numerales(),
        "gilij_tomo_iii": gilij(),
    }


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="mide e imprime sin escribir")
    a = ap.parse_args()
    m = medir()
    print(f"capa {CAPA}: {m['meta']['entradas_de_la_capa']} entradas")
    print(f"sonda ka-/ma-: {len(m['sonda_ka_ma'])} formas")
    for r, d in m["sonda_nominalizadores"].items():
        print(f"final {r}: {d['formas']} formas, {d['con_glosa_de_agente_o_de_accion']} con glosa de agente/acción")
    t = m["trampa_kana"]
    print(f"trampa -kana: {t['formas_que_acaban_en_kana_fonemizadas']} formas achagua acaban en kana; "
          f"{t['de_ellas_con_glosa_plural_o_colectiva']} con glosa plural")
    n = m["numerales"]
    print("numerales:", n["similitud_difflib"])
    print("nulo:", n["modelo_nulo"])
    print("am:", n["silaba_am"])
    g = m["gilij_tomo_iii"]
    for r, d in g.get("patrones", {}).items():
        print(f"gilij {r}: {d['aciertos']} (pdf {d['pdf']})")
    if not a.check:
        with open(SALIDA, "w", encoding="utf-8") as fh:
            fh.write("# GENERADO por 6-fusion/scripts/medir_arte_achagua.py — no editar a mano\n")
            yaml.safe_dump(m, fh, allow_unicode=True, sort_keys=False, width=110)
        with open(SALIDA, encoding="utf-8") as fh:
            assert yaml.safe_load(fh)["meta"]["entradas_de_la_capa"] == m["meta"]["entradas_de_la_capa"]
        print("escrito:", os.path.relpath(SALIDA, RAIZ))


if __name__ == "__main__":
    main()
