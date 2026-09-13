# -*- coding: utf-8 -*-
"""Decisión de Miguel, 2026-09-12: «si están como taíno en otra fuente y son
panhispánicas, y el mismo diccionario del habla paraguanera los recoge,
entonces deben clasificar como caquetío. Ya hemos visto que el caquetío y el
taíno compartían muchas cosas».

Cómo se aplica sin romper la regla 2:
  - La capa es `caquetío-reconstruido`, no atestiguada. Es el precedente que
    el propio canon ya tiene: kanoa, hamaca y konuko son «forma justificada
    por cognado en taíno» y se quedaron RECONSTRUIDAS (D5 colisiones,
    2026-08-31) porque la voz pudo llegar a Paraguaná por el español y no por
    el caquetío — riesgo de circularidad. Reconstruido dice exactamente eso:
    cognado hermano citado, sin atestación caquetía colonial.
  - Sólo entran las que cumplen las TRES cosas: origen taíno declarado por una
    fuente (DRAE / Alvarado, en el `cruce` del dictado), panhispánicas, y
    recogidas por Medina Colina en el habla paraguanera.

Dos salidas:
  1. Las que YA están en el lexicón como taíno y Medina recoge → se re-etiquetan
     aquí mismo (iguana, macana, nagua…). `tuna` se excluye: la de Medina es el
     cactus, la del lexicón 'agua, río' — homónimos.
  2. Las que NO están en el lexicón → propuesta en
     6-fusion/tainismos_en_medina.yaml, para que Miguel diga cuáles entran
     como entradas nuevas (regla 5: esto sí es fusión de voces nuevas).
Idempotente.
"""
import io, os, re, sys, unicodedata, yaml
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL

V = CL.VOCABULARIO_BASE
D = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "medina_colina_dictado.yaml"), encoding="utf-8"))
voces = {}
def rec(n):
    if isinstance(n, dict):
        if "voz" in n and "glosa_libro" in n: voces[n["voz"]] = n
        for v in n.values(): rec(v)
    elif isinstance(n, list):
        for v in n: rec(v)
rec(D)

def pel(s): return "".join(c for c in unicodedata.normalize("NFD", (s or "").lower()) if unicodedata.category(c) != "Mn")
medina = {pel(v): v for v in voces}
HOMONIMOS = {"tuna"}          # Medina: el cactus; lexicón: 'agua, río'

def etimologia_taina(d):
    blob = " ".join(str(d.get(k, "")) for k in ("cruce", "razon", "filtros"))
    m = re.search(r"(DRAE[^'}\]]{0,80}del ta[ií]no[^'}\]]{0,60}|de origen ta[ií]no[^'}\]]{0,60}|origen antillano \(ta[ií]no\)[^'}\]]{0,40})", blob, re.I)
    return " ".join(m.group(1).split()) if m else None

# ── 1. las que ya están en el lexicón ──
p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
cambiadas = []
for k, e in list(V.items()):
    f = e.get("fuente") or ""
    if not f.startswith("taíno") or f == "taíno-reconstruido": continue
    formas = {pel(k), pel(e.get("forma_fuente", ""))} - {""}
    hit = [medina[x] for x in formas if x in medina and x not in HOMONIMOS]
    if not hit: continue
    d = voces[hit[0]]; eti = etimologia_taina(d) or "origen taíno según el cruce del dictado"
    pag = d.get("pagina") or "página no dictada"
    huella = (f"Decisión de Miguel 2026-09-12: tainismo panhispánico que Medina Colina recoge en el habla "
              f"paraguanera (s.v. {hit[0]}, {pag}) → `caquetío-reconstruido`, forma justificada por cognado "
              f"en taíno, como kanoa/hamaca/konuko; NO atestiguada porque la vía pudo ser el español. Etimología: {eti}. "
              f"Etiqueta anterior: `{f}`")
    m = re.search(r'^(\s*"%s":\s*\{)' % re.escape(k), t, re.M); assert m, k
    ini = m.end(); fin = t.index("},", ini)
    seg = t[ini:fin]
    seg2 = re.sub(r'"fuente":\s*"%s"' % re.escape(f), '"fuente": "caquetío-reconstruido"', seg, count=1)
    if '"notas":' in seg2:
        seg2 = re.sub(r'("notas":\s*")', lambda n: n.group(1) + huella + " · ", seg2, count=1)
    else:
        seg2 = seg2.rstrip() + f', "notas": "{huella}"'
    t = t[:ini] + seg2 + t[fin:]
    cambiadas.append((k, f, hit[0], pag))
if cambiadas:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
for k, f, voz, pag in cambiadas:
    print(f"  {k:10} {f:14} → caquetío-reconstruido   (Medina s.v. {voz}, {pag})")
print(f"re-etiquetadas en el lexicón: {len(cambiadas)}")

# ── 2. las que Medina recoge con origen taíno y NO están en el lexicón ──
en_lex = {pel(k) for k in V} | {pel(e.get("forma_fuente", "")) for e in V.values()}
prop = []
for voz, d in sorted(voces.items()):
    eti = etimologia_taina(d)
    if not eti or pel(voz) in en_lex or voz in HOMONIMOS: continue
    prop.append({"voz": voz, "glosa_libro": " ".join(str(d.get("glosa_libro", "")).split()), "pagina": d.get("pagina"),
                 "veredicto_protocolo": d.get("veredicto"), "etimologia": eti,
                 "propuesta": "caquetío-reconstruido (cognado taíno + repertorio paraguanero s. XX), como kanoa/hamaca/konuko",
                 "clave_sugerida": pel(voz).replace("ü", "u")})
out = {"meta": {"obra": "medina-colina-sxx", "generado_por": "6-fusion/scripts/tainismos_medina_a_caquetio.py", "fecha": "2026-09-12",
                "regla_de_miguel": ("«si están como taíno en otra fuente y son panhispánicas, y el mismo diccionario del habla "
                                    "paraguanera los recoge, deben clasificar como caquetío»"),
                "capa": "caquetío-reconstruido — el precedente es kanoa/hamaca/konuko (D5 colisiones 2026-08-31): cognado taíno citado, sin atestación caquetía colonial",
                "que_es_esto": ("las voces del dictado con etimología taína declarada (DRAE/Alvarado en el cruce) que el protocolo descartó "
                                "como panhispánicas (veredicto D) y que NO están en el lexicón. Regla 5: entrarían como entradas NUEVAS, "
                                "y eso lo fusiona Miguel voz a voz"),
                "ya_aplicado_en_el_lexicon": [f"{k} ({f} → caquetío-reconstruido)" for k, f, _, _ in cambiadas],
                "n": len(prop)},
       "voces": prop}
dest = os.path.join(R, "6-fusion", "tainismos_en_medina.yaml")
io.open(dest, "w", encoding="utf-8", newline="\n").write(yaml.safe_dump(out, allow_unicode=True, sort_keys=False, width=110))
print(f"propuestas nuevas en {os.path.relpath(dest, R)}: {len(prop)} → " + ", ".join(x["voz"] for x in prop))
