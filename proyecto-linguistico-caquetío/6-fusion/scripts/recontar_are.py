# -*- coding: utf-8 -*-
"""morfema-002 mide «apariciones en posicion final CON GLOSA DESCRIPTIVA».
Eran 5 de 7 cuando se escribio. Se recuenta con el canon de hoy."""
import io, os, re, sys, json, yaml, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

LUGAR = ("sitio", "lugar", "paraje", "cerro", "quebrada", "rio", "río",
         "valle", "sabana", "cauce", "playa", "salina", "monte", "llano",
         "conuco", "cultivo", "pueblo", "aldea", "caserio", "punta", "cuesta")

d = yaml.safe_load(io.open(os.path.join(R, "2-lengua", "toponimos.yaml"),
                           encoding="utf-8"))
final = re.compile(r"are$")
con_glosa, sin_glosa = [], []
for t in d["toponimos"]:
    f = base(t.get("forma", ""))
    if not final.search(f): continue
    g = (t.get("glosa_fuente") or t.get("glosa_reconstruida") or "")
    if g:
        denota = any(x in base(g) for x in LUGAR)
        con_glosa.append((t["forma"], g[:58], denota))
    else:
        sin_glosa.append(t["forma"])

print(f"topónimos del canon terminados en -are: {len(con_glosa)+len(sin_glosa)}")
print(f"  CON glosa: {len(con_glosa)}   ·   sin glosa: {len(sin_glosa)}\n")
den = sum(1 for _, _, x in con_glosa if x)
for forma, g, x in sorted(con_glosa):
    print(f"  {'✔ LUGAR' if x else '· otro '}  {forma:<16} «{g}»")
print(f"\n  >> denotan LUGAR: {den} de {len(con_glosa)} con glosa")
print(f"  (morfema-002 declara 5 de 7, de cuando se escribió)")
print(f"\n  sin glosa, que son los candidatos por examinar: {', '.join(sorted(sin_glosa))}")
