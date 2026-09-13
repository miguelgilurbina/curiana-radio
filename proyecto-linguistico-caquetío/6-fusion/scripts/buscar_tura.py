# -*- coding: utf-8 -*-
"""La tesis de Miguel sobre `tura`: baile y mazorca a la vez, por el comercio
de maiz jirajara con Coro que Oliver documenta."""
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

print("═══ 1. ¿OLIVER dice que los jirajaras comerciaban MAÍZ con Coro? ═══")
for n in ("oliver_cap3.txt", "oliver2.txt", "oliver_cap2.txt", "oliver_324.txt",
          "oliver_200_260.txt"):
    f = os.path.join(S, n)
    if not os.path.exists(f): continue
    T = carga(f)
    for m in re.finditer(r"\b(maize|maiz)\b", T):
        ctx = T[max(0, m.start()-300): m.end()+320]
        if re.search(r"jirajar|coro|trade|exchang|comerci", ctx):
            print(f"  [{n}] ...{ctx}...\n")
            break

print("\n═══ 2. ¿Qué dice JAHN del baile llamado TURA? ═══")
for n in ("jahn.txt", "jahn_layout.txt"):
    f = os.path.join(S, n)
    if not os.path.exists(f): continue
    T = carga(f)
    for m in list(re.finditer(r"\btura\b", T))[:6]:
        print(f"  [{n}] ...{T[max(0,m.start()-260):m.end()+300]}...\n")
    break

print("\n═══ 3. `tura` en las fuentes y en mis registros ═══")
F = (glob.glob(os.path.join(R, "fuentes_caquetios", "*.txt"))
     + glob.glob(os.path.join(R, "6-fusion", "*.yaml"))
     + glob.glob(os.path.join(R, "3-mundo", "corpus", "*.yaml")))
for f in sorted(F):
    T = carga(f)
    ms = [m for m in re.finditer(r"\btura\b", T)]
    if not ms: continue
    print(f"  ── {os.path.basename(f)[:34]}  ({len(ms)})")
    print(f"       ...{T[max(0,ms[0].start()-180):ms[0].end()+220]}...\n")
