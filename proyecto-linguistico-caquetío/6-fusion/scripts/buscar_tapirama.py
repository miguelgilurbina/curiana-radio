# -*- coding: utf-8 -*-
"""tapirama (Miguel la anade) y cadare (Miguel la conoce de primera mano)."""
import io, os, re, sys, glob, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def carga(f):
    return re.sub(r"\s+", " ", base(re.sub(r"-\s*\n\s*", "",
        io.open(f, encoding="utf-8", errors="replace").read())))

F = (glob.glob(os.path.join(R, "fuentes_caquetios", "*.txt"))
     + glob.glob(os.path.join(S, "*.txt"))
     + glob.glob(os.path.join(R, "6-fusion", "*.yaml")))

for voz, pat in (("TAPIRAMA", r"\btapiram\w*\b"),
                 ("TAPIRUCUSU / afines", r"\btapiru\w*\b"),
                 ("CADARE", r"\bcadare\w*\b")):
    print(f"═══ {voz} ═══")
    visto = 0
    for f in sorted(set(F)):
        T = carga(f)
        ms = list(re.finditer(pat, T))
        if not ms: continue
        visto += len(ms)
        print(f"  ── {os.path.basename(f)[:34]} ({len(ms)})")
        for m in ms[:2]:
            print(f"       ...{T[max(0,m.start()-230):m.end()+270]}...\n")
    if not visto:
        print("  🔴 cero\n")

# el lexicon
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL
print("═══ ¿estan en el lexicon? ═══")
for k in ("tapirama", "cadare", "urubana", "guaracaro"):
    v = CL.VOCABULARIO_BASE.get(k)
    print(f"  {k:<11} {'🔴 no' if not v else v['fuente'] + ' «' + v['sig'][:40] + '»'}")
