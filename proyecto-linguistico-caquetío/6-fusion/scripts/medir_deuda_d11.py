# -*- coding: utf-8 -*-
"""Las 23 entradas reconstruidas desde el wayuu, contra el lokono y el achagua
— que es lo que D11 puso en su lugar."""
import io, os, re, sys, json, unicodedata, difflib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

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

V = CL.VOCABULARIO_BASE
DEUDA = [k for k, v in V.items()
         if v.get("fuente") == "caquetío-reconstruido"
         and re.search(r"wayu|guajiro", str(v.get("notas", "")), re.I)]
LOK = {k: v for k, v in V.items() if str(v.get("fuente", "")).startswith("lokono")}
ACH = {e["es"]: e["achagua"] for e in
       __import__("yaml").safe_load(io.open(os.path.join(R, "6-fusion",
       "comparandas_jahn_1927.yaml"), encoding="utf-8"))["achagua"]["voces"]}

print(f"deuda D11: {len(DEUDA)} entradas | lokono en el lexicón: {len(LOK)}\n")
apoya = contradice = mudo = 0
for k in sorted(DEUDA):
    v = V[k]
    sig = base(v["sig"])
    # que dice el lokono para ese mismo concepto
    lok = [(lk, lv["sig"]) for lk, lv in LOK.items()
           if difflib.SequenceMatcher(None, sig[:22], base(lv.get("sig", ""))[:22]).ratio() > .62]
    # y el achagua
    ach = [(ae, aw) for ae, aw in ACH.items()
           if difflib.SequenceMatcher(None, base(ae), sig[:len(ae) + 4]).ratio() > .72]
    linea = f"── {k:<9} «{v['sig'][:30]:<30}»"
    if lok:
        lk, lsig = max(lok, key=lambda x: difflib.SequenceMatcher(None, fon(k), fon(x[0])).ratio())
        r = difflib.SequenceMatcher(None, fon(k), fon(lk)).ratio()
        veredicto = "✅ APOYA" if r >= .55 else "🔴 DISCREPA"
        apoya += r >= .55; contradice += r < .55
        linea += f"  LOK {lk:<10} «{lsig[:24]:<24}» sim {r:.2f}  {veredicto}"
    else:
        mudo += 1
        linea += "  LOK —  (el lokono del lexicón no cubre ese concepto)"
    if ach:
        linea += f"   | ACH {ach[0][1]}"
    print(linea)
print(f"\n  apoya {apoya} · discrepa {contradice} · el lokono no cubre {mudo}")
