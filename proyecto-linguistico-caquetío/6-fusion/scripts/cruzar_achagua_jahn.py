# -*- coding: utf-8 -*-
"""El vocabulario achagua de Jahn (VERIFICADO EN IMAGEN) contra el caquetio."""
import io, os, re, sys, unicodedata, difflib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

# leido de la IMAGEN de las pp. impresas 377-378 (pdf 457-458)
ACHAGUA = [
 ("lengua","nuiname"), ("diente","nier"), ("nariz","nutako"), ("ojo","nutoi"),
 ("oreja","nubila"), ("cabeza","nurita"), ("barba","nuchianoma"), ("mano","nukaje"),
 ("pie","nuipa"), ("agua","mena"), ("rio","unibe"), ("fuego","ishay"),
 ("lena","ichaba"), ("sol","erre"), ("luna","kerre"), ("estrella","ivisai"),
 ("piedra","iba"), ("flecha","kapauje"), ("casa","banisi"), ("arena","gaina"),
 ("mujer","inagetua"), ("esposa","nuino"), ("tabaco","sema"), ("tigre","echave"),
 ("leon","mirrianare"), ("danta","ema"), ("pez","kupai"), ("canoa","ida"),
 ("cazabe","berri"), ("hermano","nimerre"), ("sepultura","nirri"),
 ("barbasco","kuna"), ("oir","numike"), ("beber","irago"),
]

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def fon(s):
    s = base(s)
    s = re.sub(r"gu(?=[aeio])", "w", s); s = re.sub(r"qu(?=[ei])", "k", s)
    s = re.sub(r"c(?=[ei])", "s", s)
    s = s.replace("ch", "C").replace("c", "k").replace("z", "s").replace("v", "b")
    s = s.replace("sh", "C").replace("j", "h")
    return re.sub(r"(.)\1+", r"\1", re.sub(r"[^a-zC]", "", s))

# el caquetio atestiguado, solo
CAQ = {k: v for k, v in CL.VOCABULARIO_BASE.items()
       if str(v.get("fuente", "")).startswith("caquetío")}
print(f"caquetío en el lexicón: {len(CAQ)}  |  achagua de Jahn: {len(ACHAGUA)}\n")

print("═══ A. MISMO CONCEPTO: ¿qué dice el caquetío donde el achagua dice X? ═══")
for glosa, ach in ACHAGUA:
    hits = [(k, v["sig"]) for k, v in CAQ.items()
            if re.search(r"\b" + re.escape(glosa) + r"\w{0,3}\b", base(v.get("sig", "")))]
    if not hits: continue
    for k, sig in hits[:3]:
        r = difflib.SequenceMatcher(None, fon(ach), fon(k)).ratio()
        marca = "  ⭐ PARECIDAS" if r >= .55 else ""
        print(f"  {glosa:<10} ACH {ach:<12} CAQ {k:<12} «{sig[:44]}»  sim {r:.2f}{marca}")

print("\n═══ B. MISMA FORMA: ¿hay caquetío que se parezca, diga lo que diga? ═══")
for glosa, ach in ACHAGUA:
    fa = fon(ach)
    if len(fa) < 3: continue
    for k, v in CAQ.items():
        fk = fon(k)
        if len(fk) < 3: continue
        r = difflib.SequenceMatcher(None, fa, fk).ratio()
        if r >= .78:
            print(f"  ACH {ach:<12} '{glosa}'   ~   CAQ {k:<12} «{v['sig'][:42]}»  sim {r:.2f}")

print("\n═══ C. los conceptos que el caquetío NO tiene ═══")
faltan = []
for glosa, ach in ACHAGUA:
    if not any(re.search(r"\b" + re.escape(glosa) + r"\w{0,3}\b", base(v.get("sig", "")))
               for v in CAQ.values()):
        faltan.append(f"{glosa} (ach. {ach})")
print("  " + "; ".join(faltan))
print(f"\n  => {len(faltan)} de {len(ACHAGUA)} conceptos sin palabra caquetía atestiguada")
