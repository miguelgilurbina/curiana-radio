# -*- coding: utf-8 -*-
"""Donde aparece `chamaco`. Ahora si: fuentes primarias Y registros propios."""
import io, os, re, sys, glob, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# la leccion de hace un rato: TAMBIEN lo que yo mismo he escrito
F = (glob.glob(os.path.join(R, "fuentes_caquetios", "*.txt"))
     + glob.glob(os.path.join(S, "*.txt"))
     + glob.glob(os.path.join(R, "6-fusion", "*.yaml"))
     + glob.glob(os.path.join(R, "6-fusion", "**", "*.md"), recursive=True)
     + glob.glob(os.path.join(R, "2-lengua", "*.yaml"))
     + glob.glob(os.path.join(R, "3-mundo", "corpus", "*.yaml"))
     + glob.glob(os.path.join(R, "4-fuentes", "*.md")))

PAT = re.compile(r"\b[cs]hamac[oa]s?\b")
print(f"buscado en {len(F)} archivos (fuentes + mis propios registros)\n")
visto = 0
for f in sorted(set(F)):
    try:
        T = re.sub(r"\s+", " ", base(io.open(f, encoding="utf-8", errors="replace").read()))
    except Exception:
        continue
    ms = list(PAT.finditer(T))
    if not ms: continue
    visto += 1
    rel = f.replace(R + os.sep, "")
    print(f"── {rel}  ({len(ms)})")
    for m in ms[:2]:
        print(f"     ...{T[max(0,m.start()-220):m.end()+260]}...\n")
if not visto:
    print("  cero")

# y el vecindario en Alvarado, por si el ave tiene otro nombre
print("\n═══ ¿que dice Alvarado del pajaro carpintero? ═══")
a = os.path.join(S, "alvarado.txt")
if os.path.exists(a):
    T = re.sub(r"\s+", " ", base(re.sub(r"-\s*\n\s*", "", io.open(a, encoding="utf-8", errors="replace").read())))
    for m in list(re.finditer(r"carpintero", T))[:4]:
        print(f"  ...{T[max(0,m.start()-230):m.end()+160]}...\n")
