# -*- coding: utf-8 -*-
"""Balance nombre por nombre de la lista de Miguel: qué se revisó y qué falta."""
import io, os, re, sys, glob, json, yaml, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s); s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C").replace("c", "k").replace("z", "s").replace("v", "b")
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zC]", "", s))

# ── la lista ──
d = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "toponimia_paraguana_miguel.yaml"), encoding="utf-8"))
L = d["lista_dictada_2026-09-10"]
lista = sorted(set(L["ya_en_canon"]["formas"]) | set(L["en_el_barrido_osm_sin_procesar"]["formas"])
               | set(L["nuevos_para_el_repo"]["formas"]))

# ── A. glosa por Esteves (Parte I o II) ──
G2 = json.load(io.open(os.path.join(S, "parte2_glosas.json"), encoding="utf-8"))
glosa_esteves = {fon(n) for n in G2}

# ── B. lo mirado a mano en la web (los ficheros de barrido) ──
b1 = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "barrido_web_medina_2026-09-09.yaml"), encoding="utf-8"))
bt = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "barrido_toponimos_web_2026-09-10.yaml"), encoding="utf-8"))
web = set()
for sec in ("nombres", "sin_hallazgo_util", "otros_del_segundo_tramo"):
    for x in (bt.get(sec) or []):
        if isinstance(x, dict) and x.get("forma"): web.add(fon(x["forma"]))
for x in (bt.get("ecuaciones_que_cierran", {}).get("casos") or []):
    if x.get("forma"): web.add(fon(x["forma"]))
for x in (bt.get("de_la_lista_de_miguel") or []):
    if isinstance(x, dict) and x.get("forma"): web.add(fon(x["forma"]))
tm = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "toponimia_paraguana_miguel.yaml"), encoding="utf-8"))
for x in (tm["cola_de_etimologia_coloquial"].get("nombres") or []):
    web.add(fon(x["forma"]))
# los que busqué a mano en tandas agrupadas
web |= {fon(x) for x in ["Coro","Chichiriviche","Tucacas","Cuare","Jadacaquiva","Yabuquiva",
  "Buchivacoa","Tocuyo","Yaracal","Mirimire","Macolla","Buchuaco","Baraived","Cabure",
  "Curimagua","Pecaya","Taratara","Mitare","Hueque","Cumaragua","Cayerúa","Machuruca",
  "Jacuque","Jacura","Quitaire","Purureche","Taparoy","Tupure","Guacuira","Cocodite",
  "Maitiruma","Acurigua","Cuajaracume","Sacuragua","Tumatey","Maquigue","Yaima","Codore",
  "Aguide","Camare","Guaranao","Borojó","Adícora","Tacuato","Capatárida","Zazárida",
  "Miraca","Matícora","Judibana","Amuay","Jayana","Adaro"]}

# ── C. presencia en Esteves aunque sin glosa ──
p1 = "".join(io.open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(R, "fuentes_caquetios", "Esteves_1989_*_[123].ocr.txt"))))
p2 = "".join(io.open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(R, "fuentes_caquetios", "Esteves_1989_*_[456].ocr.txt"))))
tb = base(" ".join((p1 + p2).split()))
def en_esteves(n):
    b = base(n)
    return bool(re.search(r"\b" + re.escape(b) + r"\w{0,3}\b", tb))

filas = collections.defaultdict(list)
for n in lista:
    k = fon(n)
    tiene_glosa = k in glosa_esteves
    mirado_web = k in web
    esta = en_esteves(n)
    if tiene_glosa and mirado_web: filas["glosa de Esteves + mirado en web"].append(n)
    elif tiene_glosa:              filas["glosa de Esteves, sin mirar en web"].append(n)
    elif mirado_web:               filas["mirado en web, sin glosa de Esteves"].append(n)
    elif esta:                     filas["en Esteves SIN glosa, y sin mirar en web"].append(n)
    else:                          filas["SIN TOCAR: ni glosa, ni web, ni en Esteves"].append(n)

print(f"LISTA DE MIGUEL: {len(lista)} nombres únicos\n")
orden = ["glosa de Esteves + mirado en web", "glosa de Esteves, sin mirar en web",
         "mirado en web, sin glosa de Esteves", "en Esteves SIN glosa, y sin mirar en web",
         "SIN TOCAR: ni glosa, ni web, ni en Esteves"]
for k in orden:
    v = filas[k]
    print(f"── {k}: {len(v)}")
    if v: print("   " + ", ".join(sorted(v)))
    print()
rev = len(lista) - len(filas[orden[3]]) - len(filas[orden[4]])
print(f"=> con ALGO en firme (glosa o revisión propia): {rev}")
print(f"=> falta trabajo real en: {len(filas[orden[3]]) + len(filas[orden[4]])}")
