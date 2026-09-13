# -*- coding: utf-8 -*-
"""El seretón: la forma y el concepto, en todo lo extraido."""
import io, os, re, sys, glob, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

F = glob.glob(os.path.join(R, "fuentes_caquetios", "*.txt")) + glob.glob(os.path.join(S, "*.txt"))
F = [f for f in F if os.path.getsize(f) > 5000]

# la forma, con permutacion laxa s~c~z y una consonante doble opcional
FORMA = re.compile(r"\b[scz]e?r+e?t[oó]n\w{0,3}\b")
# y el concepto, por si la voz no esta pero el mito si
CONCEPTO = re.compile(r"\b(transform\w+ en|convertirse en|hombres? que se|"
                      r"licantrop\w+|brujo\w* que vuel\w+|se vuelve\w? (?:animal|tigre)|"
                      r"hombre[- ]tigre|nahual\w*)\b")

print(f"buscados en {len(F)} textos\n")
print("═══ LA FORMA (seretón / ceretón / cerretón…) ═══")
hay = False
for f in F:
    T = re.sub(r"\s+", " ", base(io.open(f, encoding="utf-8", errors="replace").read()))
    for m in list(FORMA.finditer(T))[:2]:
        hay = True
        print(f"  [{os.path.basename(f)[:28]}] ...{T[max(0,m.start()-170):m.end()+200]}...\n")
if not hay:
    print("  🔴 CERO en todo lo extraído\n")

print("═══ EL CONCEPTO (el mito, aunque la voz no esté) ═══")
hay2 = False
for f in F:
    T = re.sub(r"\s+", " ", base(io.open(f, encoding="utf-8", errors="replace").read()))
    for m in list(CONCEPTO.finditer(T))[:1]:
        hay2 = True
        print(f"  [{os.path.basename(f)[:28]}] ...{T[max(0,m.start()-190):m.end()+230]}...\n")
if not hay2:
    print("  🔴 cero")
