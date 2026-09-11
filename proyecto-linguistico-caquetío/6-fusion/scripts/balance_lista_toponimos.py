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

def cosechar(nodo, saco):
    """Toda clave `forma` del arbol, este donde este: asi un tramo nuevo
    entra en el balance sin tener que tocar este script."""
    if isinstance(nodo, dict):
        f = nodo.get("forma")
        if isinstance(f, str): saco.add(fon(f))
        for v in nodo.values(): cosechar(v, saco)
    elif isinstance(nodo, list):
        for v in nodo: cosechar(v, saco)

cosechar(bt, web)
cosechar(b1, web)
# las listas de nombres pelados que declaran «buscado y sin hallazgo»
for k in ("sin_hallazgo_en_este_tramo", "sin_hallazgo_util", "buscados_sin_resultado"):
    def recoger(n):
        if isinstance(n, dict):
            v = n.get(k)
            if isinstance(v, list):
                for x in v:
                    if isinstance(x, str): web.add(fon(x))
            for vv in n.values(): recoger(vv)
        elif isinstance(n, list):
            for vv in n: recoger(vv)
    recoger(bt)

# los que busqué a mano en tandas agrupadas
web |= {fon(x) for x in ["Coro","Chichiriviche","Tucacas","Cuare","Jadacaquiva","Yabuquiva",
  "Buchivacoa","Tocuyo","Yaracal","Mirimire","Macolla","Buchuaco","Baraived","Cabure",
  "Curimagua","Pecaya","Taratara","Mitare","Hueque","Cumaragua","Cayerúa","Machuruca",
  "Jacuque","Jacura","Quitaire","Purureche","Taparoy","Tupure","Guacuira","Cocodite",
  "Maitiruma","Acurigua","Cuajaracume","Sacuragua","Tumatey","Maquigue","Yaima","Codore",
  "Aguide","Camare","Guaranao","Borojó","Adícora","Tacuato","Capatárida","Zazárida",
  "Miraca","Matícora","Judibana","Amuay","Jayana","Adaro"]}

# ── B bis. lo hallado en fuentes DEL REPO (Alvarado 1921, Arcaya 1920) ──
aa = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "pendientes_en_alvarado_y_arcaya.yaml"), encoding="utf-8"))
repo_fuentes = set()
cosechar(aa, repo_fuentes)

# ── B ter. los que YA están en el canon de topónimos, con glosa ──
_c = yaml.safe_load(io.open(os.path.join(R, "2-lengua", "toponimos.yaml"), encoding="utf-8"))
_c = _c.get("toponimos", _c) if isinstance(_c, dict) else _c
# el campo NO se llama `glosa`: son `glosa_fuente` y `glosa_reconstruida`
canon_con_glosa = {fon(x["forma"]) for x in _c
                   if isinstance(x, dict) and x.get("forma")
                   and (x.get("glosa_fuente") or x.get("glosa_reconstruida"))}

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
    en_fuente_repo = k in repo_fuentes
    en_canon = k in canon_con_glosa
    esta = en_esteves(n)
    if en_canon and not (tiene_glosa or mirado_web or en_fuente_repo):
        filas["ya en el canon de topónimos, con glosa"].append(n); continue
    if en_fuente_repo and not (tiene_glosa or mirado_web):
        filas["resuelto en fuente del repo (Alvarado/Arcaya)"].append(n); continue
    if tiene_glosa and mirado_web: filas["glosa de Esteves + mirado en web"].append(n)
    elif tiene_glosa:              filas["glosa de Esteves, sin mirar en web"].append(n)
    elif mirado_web:               filas["mirado en web, sin glosa de Esteves"].append(n)
    elif en_fuente_repo:           filas["resuelto en fuente del repo (Alvarado/Arcaya)"].append(n)
    elif esta:                     filas["en Esteves SIN glosa, y sin mirar en web"].append(n)
    else:                          filas["SIN TOCAR: ni glosa, ni web, ni en Esteves"].append(n)

print(f"LISTA DE MIGUEL: {len(lista)} nombres únicos\n")
orden = ["glosa de Esteves + mirado en web", "glosa de Esteves, sin mirar en web",
         "mirado en web, sin glosa de Esteves",
         "resuelto en fuente del repo (Alvarado/Arcaya)",
         "ya en el canon de topónimos, con glosa",
         "en Esteves SIN glosa, y sin mirar en web",
         "SIN TOCAR: ni glosa, ni web, ni en Esteves"]
for k in orden:
    v = filas[k]
    print(f"── {k}: {len(v)}")
    if v: print("   " + ", ".join(sorted(v)))
    print()
rev = len(lista) - len(filas[orden[5]]) - len(filas[orden[6]])
print(f"=> con ALGO en firme (glosa o revisión propia): {rev}")
print(f"=> falta trabajo real en: {len(filas[orden[5]]) + len(filas[orden[6]])}")
