# -*- coding: utf-8 -*-
"""El bloque JIRAJARA | AYOMAN de Jahn (pdf 468-471), parseado y cruzado.

Encuadre corregido por Miguel el 2026-09-10: una coincidencia con el jirajara
NO descalifica la voz. Prueba CONTACTO. Lo que decide es QUE se comparte —
las palabras de cultura material y comercio viajan entre etnias; los
pronombres y los numerales casi nunca.
"""
import io, os, re, sys, json, unicodedata, difflib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

T = io.open(os.path.join(S, "jahn_layout.txt"), encoding="utf-8",
            errors="replace").read().split("\f")

filas = []
for n in range(465, 474):
    pg = T[n]
    m = re.search(r"^\s*ESPA[NÑ]OL\s+JIRAJARA", pg, re.M)
    if not m: continue
    mp = re.search(r"^\s*(\d{3})\s+LOS ABOR|DEL OCCIDENTE DE VENEZUELA\s+(\d{3})", pg, re.M)
    imp = (mp.group(1) or mp.group(2)) if mp else "?"
    for ln in pg[pg.index("\n", m.start()) + 1:].split("\n"):
        if not ln.strip() or len(ln) < 6: continue
        if re.match(r"\s*(ESPA|\d{3}\s|DEL OCC|LOS ABOR)", ln): continue
        c = [x for x in re.split(r"\s{2,}", ln.strip()) if x]
        if len(c) < 2: continue
        esp, jir = c[0].strip(" ."), c[1].strip()
        ayo = c[2].strip() if len(c) > 2 else ""
        if not esp or len(esp) > 34: continue
        if not re.search(r"[a-záéíóúñ]", esp.lower()): continue
        filas.append({"esp": esp, "jirajara": jir, "ayoman": ayo, "impresa": imp})

print(f"filas jirajara/ayomán: {len(filas)}\n")
for f in filas[:12]:
    print(f"  {f['esp']:<22} {f['jirajara']:<18} {f['ayoman']}")
print("  ...\n")
json.dump(filas, io.open(os.path.join(S, "jahn_jirajara.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s); s = re.sub(r"qu(?=[ei])", "k", s)
    s = s.replace("tsch", "C").replace("sch", "C").replace("ch", "C")
    s = s.replace("sh", "C").replace("c", "k").replace("z", "s")
    s = s.replace("v", "b").replace("j", "h").replace("y", "i")
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zC]", "", s))

# los dominios: que se presta facil y que no
NUCLEO = ("pronombre", "persona singular", "persona plural", "numeral",
          "posesivo", "aspecto", "deíctico", "deictico")
CULTURA = ("planta", "árbol", "arbol", "fruto", "pez", "ave", "animal",
           "raíz", "raiz", "bebida", "casabe", "sal", "tabaco", "algodón",
           "algodon", "hamaca", "canoa", "vasija", "olla", "cesta", "flecha",
           "arco", "maíz", "maiz", "yuca")

CAQ = {k: v for k, v in CL.VOCABULARIO_BASE.items()
       if str(v.get("fuente", "")).startswith("caquetío")}
print("═══ VOCES QUE EL CAQUETÍO COMPARTE CON JIRAJARA O AYOMÁN ═══")
print("   (concepto Y forma; el filtro de significado es obligatorio)\n")
hits = []
for f in filas:
    concepto = base(re.sub(r"\(.*?\)", "", f["esp"])).strip()
    if len(concepto) < 3: continue
    for k, v in CAQ.items():
        if not re.search(r"\b" + re.escape(concepto.split()[0]) + r"\w{0,3}\b",
                         base(v.get("sig", ""))): continue
        for lengua in ("jirajara", "ayoman"):
            w = f[lengua]
            if not w or len(w) < 3: continue
            r = difflib.SequenceMatcher(None, fon(w), fon(k)).ratio()
            if r >= .60:
                sig = base(v["sig"]) + " " + base(v.get("cat", ""))
                dom = ("🔴 NÚCLEO" if any(x in sig for x in NUCLEO)
                       else "🟢 cultura material / natural"
                       if any(x in sig for x in CULTURA) else "· otro")
                hits.append((f["esp"], lengua, w, k, v["sig"], r, dom, f["impresa"]))
hits.sort(key=lambda x: -x[5])
vistos = set()
for esp, lg, w, k, sig, r, dom, pag in hits:
    if (base(esp), k) in vistos: continue
    vistos.add((base(esp), k))
    print(f"  {esp:<18} {lg[:3].upper()} {w:<14} ~ CAQ {k:<11} «{sig[:30]:<30}» {r:.2f}  {dom}  p.{pag}")
print(f"\n  => {len(vistos)} coincidencias")
