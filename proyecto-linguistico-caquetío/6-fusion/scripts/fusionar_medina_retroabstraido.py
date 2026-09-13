# -*- coding: utf-8 -*-
"""#124, decidido por Miguel el 2026-09-13 («seguiré tu recomendación»): opción A —
las 46 voces de Medina Colina entran al lexicón como `caquetío-retroabstraido`.

  - nivel A que no estaba en el lexicón: arifuque, carebe, chirigua, tuturuto (4)
  - nivel B (10; guarataro ya estaba como atestiguado)
  - nivel C: las 32 que Miguel falló y que están en el corpus como hipotético
    (ecologia-046 … -076 y creencia-019)

La capa `caquetío-retroabstraido` sólo la ven los perfiles `suelto` y
`suelto-control` (5-experimento/perfiles_de_run.yaml); `base` no la ve. Es la
etiqueta que el borrador de #124 propuso y que ya existía con 3 entradas:
lo incierto no es la forma —está documentada en boca viva, con página— sino
que el sustrato sea caquetío.

Clave = lema fonémico de D5 (aplicar_fase2_d5.lema_fonemico); la forma de
Medina va en `forma_fuente`. Colisiones con claves existentes: se saltan y se
imprimen (son decisión aparte). Los 32 hechos del corpus reciben
`palabra_lexicon: <clave>` para que el enganche lexicón↔corpus sea medible.
Idempotente.
"""
import io, os, re, sys, yaml
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL
from aplicar_fase2_d5 import lema_fonemico

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

NIVEL_A = ["arifuque", "carebe", "chirigua", "tuturuto"]
NIVEL_B = [v for v, d in voces.items() if d.get("veredicto") == "B" and v != "guarataro"]
corpus = {}
for f in ("ecologia", "creencia"):
    dd = yaml.safe_load(io.open(os.path.join(R, "3-mundo", "corpus", f"{f}.yaml"), encoding="utf-8"))
    for e in (dd["entradas"] if isinstance(dd, dict) else dd):
        if isinstance(e, dict) and e.get("voz"):
            corpus[e["voz"]] = (f, e["id"])
NIVEL_C = sorted(corpus)
ADJ = {"cadare", "sarutaco", "siguato"}

def limpio(s): return " ".join(str(s or "").replace('"', "'").replace("\\", "").split())

def sig_de(voz, d):
    g = limpio(d.get("glosa_libro"))
    g = re.sub(r"^\[[^\]]*\]\s*", "", g)          # «[por la entrada x] …»
    return g[:150].rstrip(" ,;")

filas, saltadas = [], []
for nivel, lista in (("A", NIVEL_A), ("B", NIVEL_B), ("C", NIVEL_C)):
    for voz in lista:
        d = voces.get(voz)
        if not d:
            saltadas.append((voz, "no está en el dictado")); continue
        clave = lema_fonemico(voz.replace("ü", "ü"))
        if clave in V:
            saltadas.append((voz, f"la clave `{clave}` ya existe ({V[clave].get('fuente')})")); continue
        pag = f"p. {d['pagina']}" if d.get("pagina") else "página no dictada (⚠️ pendiente)"
        cat = "adj" if voz in ADJ else "sust"
        notas = (f"Medina Colina 2013, Del Habla Paraguanera, {pag}, s.v. {voz}: «{limpio(d.get('glosa_libro'))[:200]}». "
                 f"Nivel {nivel} del protocolo del dictado")
        if nivel == "C":
            notas += f"; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho {corpus[voz][1]} en el corpus"
        notas += (". CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del "
                  "s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven "
                  "sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. "
                  "Clave = lema fonémico D5.")
        if d.get("identificacion"):
            notas += f" Identificación: {limpio(d['identificacion'])}."
        filas.append((clave, sig_de(voz, d), cat, voz, nivel, notas))

print(f"a fusionar: {len(filas)}   saltadas: {len(saltadas)}")
for v, por in saltadas: print("   ·", v, ":", por)

p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
if "RETROABSTRAÍDAS DE MEDINA" in t:
    print("ya fusionado"); sys.exit(0)
ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {"); fin = t.index("REGLAS_ASPECTO", ini)
region = t[ini:fin]; ancla = None
for m in re.finditer(r'^\s*"[^"]+":\s*\{.*\},\s*$', region, re.M): ancla = m
corte = ini + ancla.end()
bloque = ["\n", "    # ══════════════════════════════════════════════════════\n",
          "    # RETROABSTRAÍDAS DE MEDINA (2026-09-13, #124 opción A) — las voces\n",
          "    # del habla paraguanera de nivel A/B/C: forma documentada, sustrato\n",
          "    # incierto. Sólo las ven los perfiles `suelto`.\n",
          "    # ══════════════════════════════════════════════════════\n"]
for clave, sig, cat, voz, nivel, notas in filas:
    bloque.append(f'    "{clave}": {{"sig": "{sig}", "cat": "{cat}", "fuente": "caquetío-retroabstraido", '
                  f'"forma_fuente": "{voz}", "nivel_dictado": "{nivel}", "notas": "{notas}"}},\n')
t = t[:corte] + "".join(bloque) + t[corte:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
for clave, sig, cat, voz, nivel, _ in filas:
    print(f"  + {clave:12} ← {voz:12} [{nivel}] {cat:4} {sig[:50]}")

# el enganche: palabra_lexicon en los 32 hechos
claves_c = {voz: clave for clave, _, _, voz, nivel, _ in filas if nivel == "C"}
for f in ("ecologia", "creencia"):
    pc = os.path.join(R, "3-mundo", "corpus", f"{f}.yaml"); tc = io.open(pc, encoding="utf-8").read(); n = 0
    for voz, (ff, hid) in corpus.items():
        if ff != f or voz not in claves_c: continue
        m = re.search(r"(- id: %s\n(?:.*\n)*?\s*palabra_lexicon: )null" % re.escape(hid), tc)
        if m:
            tc = tc[:m.start()] + m.group(1) + claves_c[voz] + tc[m.end():]; n += 1
    io.open(pc, "w", encoding="utf-8", newline="\n").write(tc); print(f"{f}.yaml: palabra_lexicon puesta en {n} hechos")
print("hecho")
