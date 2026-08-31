# -*- coding: utf-8 -*-
"""Cómputo D11 — primera medición: lo atestiguado contra la Tabla A-2.

A. Swadesh curado: ~24 formas caquetío-atestiguadas de concepto directo,
   fonemizadas con las reglas aprobadas de D5, contra las cinco columnas.
B. Fonotáctico: pases del filtro (se corre aparte, se reporta).
C. Colisiones forma+glosa contra las entradas wayuu y lokono del lexicón.
"""
import sys, io, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío\curiana_sim")
from curiana_lexicon import VOCABULARIO_BASE as V

# ── fonemización D5 (reglas aprobadas; h se conserva: quedó disputada) ──
def fonemizar(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z]", "", s)          # fuera apóstrofos, guiones, espacios
    s = re.sub(r"gu(?=[aeio])", "w", s)   # D5c uniforme
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)      # seseo SOLO para comparar (disputada en lemas)
    s = s.replace("ch", "C")              # proteger ch como fonema propio
    s = s.replace("c", "k").replace("C", "ch")
    s = s.replace("z", "s").replace("v", "b")
    s = s.replace("kh", "k").replace("th", "t").replace("dh", "d")
    return s

def variantes(celda):
    """Parte una celda de la A-2 en formas comparables, limpias de prefijos."""
    if not celda or celda.startswith(("---", "SPANISH", "CARIB", "KARIB", "AFRICANISM", "vid")):
        return []
    celda = re.sub(r"\([^)]*\)", "", celda)          # glosas entre paréntesis
    out = []
    for trozo in re.split(r"[/·]", celda):
        t = trozo.strip().strip("*").strip("-")
        t = re.sub(r"^(nu|n|hu|ua|wa|p|t)-", "", t)  # posesivos/persona prefijados
        t = t.replace("'", "").replace("^", "")
        t = fonemizar(t)
        if len(t) >= 2:
            out.append(t)
    return out

def lev(a, b):
    m, n = len(a), len(b)
    fila = list(range(n + 1))
    for i in range(1, m + 1):
        prev, fila[0] = fila[0], i
        for j in range(1, n + 1):
            prev, fila[j] = fila[j], min(fila[j] + 1, fila[j - 1] + 1,
                                         prev + (a[i - 1] != b[j - 1]))
    return fila[n]

def sim(a, b):
    if not a or not b:
        return 0.0
    return 1.0 - lev(a, b) / max(len(a), len(b))

# ── A. la lista curada: (forma_cq, concepto, celdas A-2 por lengua) ──
A2 = {
 "moon":     {"guajiro": "kashi'", "paraujano": "keichare", "lokono": "kathi", "ic": "hati", "maipure": "keyapi"},
 "sun":      {"guajiro": "kai'", "paraujano": "kai/kei", "lokono": "hadali", "ic": "CARIB", "maipure": "kie"},
 "stone":    {"guajiro": "ipa", "paraujano": "ipah", "lokono": "siba/-siban", "ic": "CARIB", "maipure": "kipa"},
 "sand":     {"guajiro": "jasai/wule'shi/muaku", "paraujano": "mo", "lokono": "mothoko", "ic": "CARIB", "maipure": "kaina"},
 "woman":    {"guajiro": "erruni/jie'rru/eiyetse", "paraujano": "hniere/ñerika/añukar", "lokono": "hiaro", "ic": "hiaru", "maipure": "---"},
 "man":      {"guajiro": "tolo/achini/t-echin", "paraujano": "eichire", "lokono": "oadili", "ic": "eieri/*iñeri", "maipure": "kayarrikini"},
 "tooth":    {"guajiro": "aiua/ali", "paraujano": "tai", "lokono": "arii/-ari/*dari", "ic": "-ari", "maipure": "n-ati"},
 "path":     {"guajiro": "wopu'/apu'na", "paraujano": "wobu", "lokono": "oaboroko/abonaha", "ic": "CARIB", "maipure": "anepu"},
 "one":      {"guajiro": "wane", "paraujano": "manei", "lokono": "aba-", "ic": "abana", "maipure": "piau/pakiata"},
 "two":      {"guajiro": "piama", "paraujano": "pimu/pimi", "lokono": "biama/bian", "ic": "biama", "maipure": "pina"},
 "root":     {"guajiro": "ourrala", "paraujano": "---", "lokono": "iikirahi/-ikira", "ic": "-ilagola", "maipure": "---"},
 "hear":     {"guajiro": "apa", "paraujano": "---", "lokono": "kanabon/*kanabun", "ic": "agaba", "maipure": "---"},
 "blood":    {"guajiro": "asha/isha'", "paraujano": "---", "lokono": "ithihi/-china", "ic": "hitao/-ita", "maipure": "---"},
 "big":      {"guajiro": "muleu", "paraujano": "youghe", "lokono": "firo/fili-", "ic": "uairi", "maipure": "---"},
 "mountain": {"guajiro": "uchi/kochooshi/kamu'nashi", "paraujano": "utschi", "lokono": "hororo", "ic": "CARIB", "maipure": "yapa"},
 "water":    {"guajiro": "wuin", "paraujano": "win/winkari", "lokono": "oniabo/-nia", "ic": "CARIB", "maipure": "ueni"},
 "tree":     {"guajiro": "ouulia/mojui/wunuu", "paraujano": "jinghi/jiki", "lokono": "ada/kunnuku", "ic": "---", "maipure": "aa/aama"},
 "thou":     {"guajiro": "pia'", "paraujano": "pia", "lokono": "bii", "ic": "hu-guia", "maipure": "p-ia"},
}

CURADAS = [
 ("cati",      "luna",            "moon"),
 ("cazi",      "sol",             "sun"),
 ("quiva",     "piedra",          "stone"),
 ("cuiva",     "piedra",          "stone"),
 ("rao",       "arena",           "sand"),
 ("jajato",    "lugar de arena",  "sand"),
 ("iero",      "mujer",           "woman"),
 ("ateri",     "hombre",          "man"),
 ("dare",      "diente",          "tooth"),
 ("ebo",       "camino",          "path"),
 ("darubana",  "camino (comp.)",  "path"),
 ("pana",      "uno",             "one"),
 ("gudamuen",  "dos",             "two"),
 ("buiamati",  "dos lunas",       "two"),
 ("ure",       "raíz",            "root"),
 ("jai",       "oír",             "hear"),
 ("quiricias", "sangre",          "blood"),
 ("apo",       "grande",          "big"),
 ("quidi",     "cerro",           "mountain"),
 ("bana",      "cerro (morfema)", "mountain"),
 ("para",      "mar/agua grande", "water"),
 ("bara",      "árbol",           "tree"),
 ("cudanga",   "usted (2ª)",      "thou"),
 ("apana",     "una luna",        "moon"),
]

LENGUAS = ["guajiro", "paraujano", "lokono", "ic", "maipure"]
print("=" * 96)
print("  A · SWADESH CURADO — similitud fonémica (D5) contra la Tabla A-2")
print("=" * 96)
tally = {l: 0 for l in LENGUAS}
tally["ninguna"] = 0
filas = []
for forma, glosa, concepto in CURADAS:
    fq = fonemizar(forma)
    mejores = {}
    for l in LENGUAS:
        vs = variantes(A2[concepto][l])
        mejores[l] = max((sim(fq, v) for v in vs), default=0.0)
    orden = sorted(mejores.items(), key=lambda kv: -kv[1])
    ganadora, score = orden[0]
    margen = score - orden[1][1]
    if score < 0.50:
        veredicto = "ninguna"
    elif margen < 0.10:
        veredicto = "%s~%s (empate)" % (ganadora, orden[1][0])
    else:
        veredicto = ganadora
    clave = ganadora if score >= 0.50 and margen >= 0.10 else ("ninguna" if score < 0.50 else ganadora)
    tally[clave] = tally.get(clave, 0) + 1
    filas.append((forma, glosa, fq, mejores, veredicto, score))
    det = "  ".join("%s %.2f" % (l[:4], mejores[l]) for l in LENGUAS)
    print("  %-10s %-16s → %-24s | %s" % (forma, glosa, veredicto, det))

print("\n  TALLY (gana con sim≥0.50 y margen≥0.10):")
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
    if v:
        print("    %-22s %d" % (k, v))

# ── C. colisiones forma+glosa contra wayuu y lokono del lexicón ──
print()
print("=" * 96)
print("  C · COLISIONES contra las entradas wayuu/lokono importadas (sim≥0.80 + glosa compatible)")
print("=" * 96)
def palabras_glosa(sig):
    stop = {"de","del","la","el","los","las","que","con","por","para","una","uno","en","y","o","al","su","se"}
    return {w for w in re.findall(r"[a-záéíóúüñ]+", str(sig).lower()) if len(w) > 3 and w not in stop}

at = [(p, d) for p, d in V.items() if d.get("fuente") == "caquetío-atestiguado"]
way = [(p, d) for p, d in V.items() if str(d.get("fuente", "")).startswith("wayunaiki")]
lok = [(p, d) for p, d in V.items() if str(d.get("fuente", "")).startswith("lokono")]
print("  atestiguadas %d · wayuu %d · lokono %d" % (len(at), len(way), len(lok)))

def colisiones(candidatas, etiqueta):
    n = 0
    for p, d in at:
        fq, gp = fonemizar(p), palabras_glosa(d.get("sig", ""))
        for q, e in candidatas:
            if sim(fq, fonemizar(q)) >= 0.80 and gp & palabras_glosa(e.get("sig", "")):
                print("    %-12s ~ %-14s [%s] %s | %s" % (
                    p, q, etiqueta, str(d.get("sig"))[:34], str(e.get("sig"))[:34]))
                n += 1
                break
    return n

nw = colisiones(way, "wayuu")
nl = colisiones(lok, "lokono")
print("\n  TALLY C: wayuu %d · lokono %d  (sobre %d atestiguadas)" % (nw, nl, len(at)))
