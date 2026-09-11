# -*- coding: utf-8 -*-
"""Saca la GLOSA de cada entrada de la Parte II y la cruza con la lista de
Miguel y con el lexicón."""
import io, os, re, sys, json, yaml, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))

E = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "parte2.json"), encoding="utf-8"))

# la glosa va entre paréntesis al final de la entrada
PAREN = re.compile(r"\(([^)]{3,400})\)")
# …pero el OCR se come el paréntesis de CIERRE a veces, y ahí se perdían glosas:
# CARACUBANA «cerro poblado de caracara» y BOROJÓ «es chibcha» caían fuera.
# Medido 2026-09-10: seis entradas más al admitir el paréntesis huérfano.
HUERFANO = re.compile(r"\(([^)]{3,240})$")

def base(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s)
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C").replace("c", "k").replace("z", "s").replace("v", "b")
    s = re.sub(r"[^a-zC]", "", s)
    return re.sub(r"(.)\1+", r"\1", s)

con_glosa = {}
for n, e in E.items():
    _c = re.sub(r"\s+", " ", e["cuerpo"])
    m = PAREN.search(_c) or HUERFANO.search(_c)
    if m:
        g = " ".join(m.group(1).split())
        # descartar los paréntesis que sólo son advertencias del autor
        if not g.lower().startswith(("advertencia", "véase", "vease", "ver ")):
            con_glosa[n] = {**e, "glosa": g}

print(f"entradas de la Parte II: {len(E)} | CON GLOSA entre paréntesis: {len(con_glosa)}")

# ── ¿qué filiación declara Esteves? ──
FIL = collections.Counter()
for e in con_glosa.values():
    g = base(e["glosa"])
    for lengua in ("caquet", "taina", "taino", "caribe", "cumanagot", "jirajar",
                   "ayaman", "gayon", "arawak", "arahuac", "guajir", "chaima"):
        if lengua in g:
            FIL[lengua] += 1
print("filiaciones que Esteves declara en las glosas:", dict(FIL.most_common()))

# ── cruce con la lista de Miguel ──
d = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "toponimia_paraguana_miguel.yaml"),
                           encoding="utf-8"))
L = d["lista_dictada_2026-09-10"]
lista = sorted(set(L["ya_en_canon"]["formas"]) | set(L["en_el_barrido_osm_sin_procesar"]["formas"])
               | set(L["nuevos_para_el_repo"]["formas"]))
idx = {fon(n): n for n in con_glosa}

aciertos = []
for n in lista:
    k = fon(n)
    if k in idx:
        aciertos.append((n, idx[k], con_glosa[idx[k]]))
print(f"\nDE LA LISTA DE MIGUEL, con glosa de Esteves: {len(aciertos)} de {len(lista)}")
for orig, esteves, e in sorted(aciertos):
    print(f"  {orig:<14} [{e['municipio']}/{e['distrito']}] {e['glosa'][:105]}")

# ── cruce con el lexicón ──
from curiana_lexicon import VOCABULARIO_BASE as V
lex = {fon(k): (k, e.get("sig") or e.get("es"), e.get("fuente")) for k, e in V.items()}
print("\n── entradas de la Parte II cuya FORMA ya está en el lexicón ──")
n = 0
for nom, e in con_glosa.items():
    hit = lex.get(fon(nom))
    if hit and n < 30:
        print(f"  {nom:<16} ~ {hit[0]:<14} '{str(hit[1])[:40]}' | Esteves: {e['glosa'][:60]}")
        n += 1

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parte2_glosas.json")
json.dump(con_glosa, io.open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito:", dest)
