# -*- coding: utf-8 -*-
"""Las 390 filas guajiro/paraujano de Jahn contra el caquetio.
Con filtro de SIGNIFICADO obligatorio: la leccion del test k- que se cayo."""
import io, os, re, sys, json, unicodedata, difflib, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

F = json.load(io.open(os.path.join(S, "jahn_guajiro.json"), encoding="utf-8"))

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s); s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("tsch", "C").replace("sch", "C").replace("ch", "C")
    s = s.replace("sh", "C").replace("c", "k").replace("z", "s")
    s = s.replace("v", "b").replace("j", "h").replace("y", "i")
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zC]", "", s))

def desposeer(w):
    """las formas de la tabla llevan el posesivo ta-/te-/to-/t-/wa-/we-:
    el radical es lo que queda, y es lo unico comparable."""
    b = base(w).replace("-", "")
    for pre in ("ta", "te", "ti", "to", "tu", "wa", "we", "sou", "su", "sa"):
        if b.startswith(pre) and len(b) > len(pre) + 2:
            return b[len(pre):]
    return b[1:] if b.startswith("t") and len(b) > 3 else b

CAQ = {k: v for k, v in CL.VOCABULARIO_BASE.items()
       if str(v.get("fuente", "")).startswith("caquetío")}
print(f"filas de Jahn {len(F)}  |  caquetío atestiguado {len(CAQ)}\n")

# ── el cruce, exigiendo concepto Y forma ──
pares, solo_concepto = [], 0
for f in F:
    concepto = base(f["esp"])
    concepto = re.sub(r"\((mi|mío|nuestro|nuestra|tu|su)\)", "", concepto).strip()
    if len(concepto) < 3: continue
    caq_ok = [(k, v["sig"]) for k, v in CAQ.items()
              if re.search(r"\b" + re.escape(concepto.split()[0]) + r"\w{0,3}\b",
                           base(v.get("sig", "")))]
    if not caq_ok: continue
    solo_concepto += 1
    for lengua in ("guajiro", "paraujano"):
        w = f[lengua]
        if not w or len(w) < 3: continue
        rad = fon(desposeer(w))
        if len(rad) < 3: continue
        for k, sig in caq_ok:
            r = difflib.SequenceMatcher(None, rad, fon(k)).ratio()
            if r >= .62:
                pares.append((f["esp"], lengua, w, rad, k, sig, r, f["impresa"]))

pares.sort(key=lambda x: -x[6])
print("═══ PARES QUE CUMPLEN LAS DOS COSAS: mismo concepto Y forma parecida ═══")
vistos = set()
for esp, lg, w, rad, k, sig, r, pag in pares:
    key = (base(esp), k)
    if key in vistos: continue
    vistos.add(key)
    print(f"  {esp:<20} {lg[:3].upper()} {w:<16} (rad. {rad:<9}) ~ CAQ {k:<11} «{sig[:34]}»  {r:.2f}  p.{pag}")
print(f"\n  => {len(vistos)} pares  (de {solo_concepto} filas cuyo concepto SÍ existe en caquetío)")

# ── el hueco ──
conceptos = {re.sub(r"\(.*?\)", "", base(f["esp"])).strip() for f in F}
sin = [c for c in sorted(conceptos)
       if c and not any(re.search(r"\b" + re.escape(c.split()[0]) + r"\w{0,3}\b",
                                  base(v.get("sig", ""))) for v in CAQ.values())]
print(f"\n═══ HUECO: conceptos de la tabla sin palabra caquetía ═══")
print(f"  {len(sin)} de {len(conceptos)} conceptos distintos")
print("  " + "; ".join(sin[:55]) + " …")
