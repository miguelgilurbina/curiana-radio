# -*- coding: utf-8 -*-
"""Censo de la terminacion -re: en el lexicon, en el canon de toponimos y en
el gazetteer de Esteves. Observacion de Miguel, 2026-09-10."""
import io, os, re, sys, glob, json, yaml, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\migue\OneDrive\Documents\Desarrollo\Curiana Radio\proyecto-linguistico-caquetío"
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

def base(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

VOCAL = re.compile(r"([aeiou])re$")

# ── 1. el lexicón caquetío ──
CAQ = {k: v for k, v in CL.VOCABULARIO_BASE.items()
       if str(v.get("fuente", "")).startswith("caquetío")}
lex = collections.defaultdict(list)
for k, v in CAQ.items():
    m = VOCAL.search(base(k))
    if m: lex[m.group(1) + "re"].append((k, v["sig"][:40], v["fuente"].split("-")[-1]))

print(f"═══ 1. EL LEXICÓN CAQUETÍO ({len(CAQ)} voces) ═══")
tot = sum(len(v) for v in lex.values())
print(f"  terminadas en -re: {tot}  ({100*tot//len(CAQ)}%)\n")
for suf in sorted(lex, key=lambda s: -len(lex[s])):
    print(f"  ── -{suf}: {len(lex[suf])}")
    for k, s, cap in sorted(lex[suf]):
        print(f"       {k:<14} «{s:<40}» {cap}")

# ── 2. el canon de topónimos ──
d = yaml.safe_load(io.open(os.path.join(R, "2-lengua", "toponimos.yaml"), encoding="utf-8"))
tops = [t for t in d["toponimos"] if VOCAL.search(base(t.get("forma", "")))]
print(f"\n═══ 2. EL CANON DE TOPÓNIMOS ({len(d['toponimos'])}) ═══")
print(f"  terminados en -re: {len(tops)}  ({100*len(tops)//len(d['toponimos'])}%)")
por = collections.Counter(VOCAL.search(base(t["forma"])).group(1) + "re" for t in tops)
for s, n in por.most_common(): print(f"   -{s}: {n}")
print("  " + ", ".join(sorted(t["forma"] for t in tops)))

# ── 3. el gazetteer entero de Esteves ──
E = json.load(io.open(os.path.join(R, "6-fusion", "scripts", "parte2.json"), encoding="utf-8"))
ges = [k for k in E if VOCAL.search(base(k))]
print(f"\n═══ 3. EL GAZETTEER DE ESTEVES, PARTE II ({len(E)} entradas) ═══")
print(f"  terminados en -re: {len(ges)}  ({100*len(ges)//len(E)}%)")
pe = collections.Counter(VOCAL.search(base(k)).group(1) + "re" for k in ges)
for s, n in pe.most_common(): print(f"   -{s}: {n}")
print("  " + ", ".join(sorted(ges)))

# ── 4. control: ¿es -re especial, o todo acaba en vocal? ──
print("\n═══ 4. CONTROL — las otras finales del gazetteer ═══")
fin = collections.Counter()
for k in E:
    b = base(k)
    if len(b) > 2: fin[b[-2:]] += 1
for s, n in fin.most_common(12):
    print(f"   -{s}: {n}")
