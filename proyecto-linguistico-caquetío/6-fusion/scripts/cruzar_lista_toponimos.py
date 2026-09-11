# -*- coding: utf-8 -*-
"""Cruza la lista de topónimos dictada por Miguel (2026-09-10) contra todo lo
que el repo ya tiene: canon, índice de Esteves, barrido OSM y el lexicón."""
import io, os, re, sys, yaml, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))

PARAGUANA = """Jacuque, Sabaneta, Cumajacoa, Guaranao, Yabuquiva, Quitaire, Sarinao,
Carirubana, Cujicana, Cayude, Tacuato, Caduto, Guasare, Botucare, Guica, Machuruca,
Miraca, Maicara, Maquigue, Charaima, Adicora, Guacuira, Sacuragua, Adaure, Guacurebo,
Abudure, Cocodite, Guayacanal, Acaboa, Macolla, Tumatey, Cumaragua, Yaima, Tiraya,
Buchuaco, Baraived, Caseto, Davaduvare, Azaro, Cumairebo, Aguaque, Cayerúa"""

FALCON = """Botucare, Turamaco, Mitare, Codore, Cauca, Cuajaracume, Zazárida, Cocuy,
Caracubana, Borobo, Capana, Guaruguaro, Quisiro, Bariro, Jadagua, Guaguana, Tomoporo,
Camare, Matícora, Casigua, Tarica, Omomo, Copey, Borojó, Buchivacoa, Pure, Chiriguare,
Coroquidiro, Sividigua, Capatárida, Tarama, Corubo, Bariro, Tupure, Purureche, Taparoy,
Churuguara, Mapararí, Tapatapa, Samaria, Carora, Caracara, Aroa, Tucacas, Tuque, Sanare,
Chichiriviche, Tibana, Tocuyo, Yaracal, Araurima, Araure, Tucurere, Camachima, Capadare,
Guacharaca, Mirimire, Caidie, Jacure, Cueparo, Petare, Tacamire, Bucaral, Duvisí,
Mapararí, Araguan, Aguide, Curarí, Guay, Piritú, Hueque, Guanabano, Acurigua, Taratara,
Aracua, Cabure, Curimagua, Macuare, Pecaya, Carazao, Caujarao, Siburúa, Muaco, Dividive,
Cumarebo, Bariquis, Chipare, Taguaqui, Viana, Sauca, Caidie, Jacura, Cueparo, Origuasa,
Murucusa, Guate, Urucure, Usera, Cururupare"""

def lista(s):
    return [x.strip() for x in s.replace("\n", " ").split(",") if x.strip()]

def base(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    """Lema fonémico D5 + la permutación laxa de la campaña."""
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s)
    s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C").replace("c", "k").replace("z", "s").replace("v", "b")
    s = re.sub(r"[^a-zC]", "", s)
    return re.sub(r"(.)\1+", r"\1", s)

def laxa(k):
    """j~s~u~h inicial, b~v~p, según la regla de permutación de la campaña."""
    k = k.replace("p", "b")
    if k[:1] in ("h", "s", "u", "j"):
        k = "j" + k[1:]
    return k

def lev(a, b):
    m, n = len(a), len(b)
    f = list(range(n + 1))
    for i in range(1, m + 1):
        prev, f[0] = f[0], i
        for j in range(1, n + 1):
            prev, f[j] = f[j], min(f[j] + 1, f[j - 1] + 1, prev + (a[i-1] != b[j-1]))
    return f[n]

# ── lo que el repo ya tiene ─────────────────────────────────────────────
canon = {}
d = yaml.safe_load(io.open(os.path.join(R, "2-lengua", "toponimos.yaml"), encoding="utf-8"))
for t in (d.get("toponimos") or d):
    canon[fon(str(t.get("forma", "")))] = (t.get("forma"), t.get("id"), t.get("nivel"))

esteves = set()
fe = os.path.join(R, "6-fusion", "toponimos_esteves_indice.yaml")
if os.path.exists(fe):
    de = yaml.safe_load(io.open(fe, encoding="utf-8"))
    for x in (de.get("toponimos") or de.get("indice") or []):
        f = x.get("forma") if isinstance(x, dict) else x
        if f:
            esteves.add(fon(str(f)))

osm = set()
fo = os.path.join(R, "6-fusion", "toponimos_mapa_kaketiana.yaml")
if os.path.exists(fo):
    do = yaml.safe_load(io.open(fo, encoding="utf-8"))
    def recoge(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("nombre", "forma", "name") and isinstance(v, str):
                    osm.add(fon(v))
                else:
                    recoge(v)
        elif isinstance(o, list):
            for v in o:
                recoge(v)
    recoge(do)

from curiana_lexicon import VOCABULARIO_BASE as V
lexico = {fon(k): (k, e.get("sig") or e.get("es"), e.get("fuente")) for k, e in V.items()}

# ── el cruce ────────────────────────────────────────────────────────────
todos = [(n, "paraguaná") for n in lista(PARAGUANA)] + [(n, "falcón") for n in lista(FALCON)]
vistos, unicos, dups = set(), [], []
for n, zona in todos:
    k = fon(n)
    if k in vistos:
        dups.append(n)
        continue
    vistos.add(k)
    unicos.append((n, zona, k))

print(f"dictados: {len(todos)} | únicos: {len(unicos)} | repetidos: {len(dups)} -> {sorted(set(dups))}")

buckets = collections.defaultdict(list)
detalle = []
for n, zona, k in unicos:
    en_canon = canon.get(k)
    if not en_canon:                       # cruce laxo
        lk = laxa(k)
        for ck, cv in canon.items():
            if laxa(ck) == lk or (len(k) >= 6 and lev(laxa(ck), lk) <= 1):
                en_canon = cv + ("(laxo)",)
                break
    en_lex = lexico.get(k)
    if not en_lex:
        lk = laxa(k)
        for xk, xv in lexico.items():
            if len(k) >= 5 and laxa(xk) == lk:
                en_lex = xv + ("(laxo)",)
                break
    est = k in esteves or laxa(k) in {laxa(x) for x in esteves}
    en_osm = k in osm or laxa(k) in {laxa(x) for x in osm}

    if en_canon:
        buckets["ya en canon"].append(n)
    elif est:
        buckets["en el índice de Esteves, sin procesar"].append(n)
    elif en_osm:
        buckets["en el barrido OSM, sin procesar"].append(n)
    else:
        buckets["NUEVO — no está en ningún sitio"].append(n)
    detalle.append((n, zona, en_canon, en_lex, est, en_osm))

print()
for b in ("ya en canon", "en el índice de Esteves, sin procesar",
          "en el barrido OSM, sin procesar", "NUEVO — no está en ningún sitio"):
    v = buckets[b]
    print(f"── {b}: {len(v)}")
    print("   " + ", ".join(sorted(v)))
    print()

print("── los que casan con una VOZ del lexicón (topónimo + palabra) ──")
for n, zona, c, l, e, o in detalle:
    if l:
        print(f"   {n:<14} ~ {l[0]:<14} '{str(l[1])[:44]}' [{l[2]}]")

json_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cruce_lista.yaml")
io.open(json_out, "w", encoding="utf-8", newline="\n").write(yaml.safe_dump(
    {b: sorted(v) for b, v in buckets.items()}, allow_unicode=True))
print("\nescrito:", json_out)
