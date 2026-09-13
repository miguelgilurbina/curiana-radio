# -*- coding: utf-8 -*-
"""Fase 1b de D11: el vocabulario verbal de Schumann (1755) vía Perea 1942
entra al lexicón como comparanda lokono.

Lee 6-fusion/lokono_verbos_perea_1942.yaml (generado por minar_perea_verbos.py)
y escribe las voces NUEVAS en VOCABULARIO_BASE, en un bloque propio a
continuación del de la fase 1. Miguel autorizó el 2026-09-12 «incorporar la
mayor cantidad de voces lokono y achagua posibles».

Reglas que se respetan:
- Ninguna clave pisa una existente. Si la clave ya está (sea lokono o no), la
  voz entra como `<clave>-lokono` — el precedente es `kati-kalinago` y los 4
  homógrafos de la fase 1. Las 26 que ya estaban CON LA MISMA CLAVE se saltan:
  son corroboración, y están listadas en el YAML.
- 🔴 Homógrafos del ESPAÑOL también van con `-lokono`: `score_linguistico()`
  cuenta como arahuaco cualquier token igual a una clave y no filtra por
  fuente, así que `casa`, `carta` o `manta` como claves desnudas contaminarían
  la métrica. Se detectan con RAICES_ESPANOLAS del propio lexicón más una lista
  corta de lo que ese conjunto no cubre, y toda clave de dos letras o menos.
- `cat`: los verbos son `v_raiz` (Perea los da como verbos, estativos
  incluidos); las voces sueltas llevan la suya. No se inventa más gramática.
- Las dos glosas alemanas ilegibles (Al: berbekutten, bogairen) NO entran: una
  entrada sin glosa legible no sirve para comparar nada.
- Cada entrada lleva página impresa, forma de Perea, conjugación y marcas.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import yaml
import curiana_lexicon as CL

V = CL.VOCABULARIO_BASE
Y = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "lokono_verbos_perea_1942.yaml"),
                           encoding="utf-8"))

# Homógrafos del español que RAICES_ESPANOLAS no lista (medido sobre esta lista).
ESPANOL_EXTRA = {"casa", "carta", "manta", "ca", "sa", "ide", "pere", "tere", "case",
                 "cari", "usa", "poi", "make", "sina", "cai", "boa", "ere", "cure", "cu",
                 "su", "ri", "man", "mor", "sur", "tun", "cui", "sia", "uca", "ollasa"}
ES = {r.lower() for r in CL.RAICES_ESPANOLAS} | ESPANOL_EXTRA


def limpio(s):
    return str(s).replace('"', "'").replace("\\", "").strip()


def clave_segura(cl):
    base = cl.replace("!", "").replace(" ", "-")
    pelada = base.replace("c-a-", "").replace("k-", "").replace("m-", "")
    if base in V or len(pelada) <= 2 or pelada in ES or base in ES:
        return base + "-lokono", True
    return base, False


filas, saltadas = [], []
for f in Y["verbos"]:
    if "ya_en_lexicon" in f:
        saltadas.append((f["clave"], f"ya en el lexicón como `{f['ya_en_lexicon']}` — corroboración, ver YAML"))
        continue
    marcas = f.get("marcas") or []
    if "Al" in marcas and "ilegible" in f["glosa"]:
        saltadas.append((f["clave"], "glosa alemana ilegible en la fuente"))
        continue
    clave, desamb = clave_segura(f["clave"])
    if clave in V:
        saltadas.append((f["clave"], f"la clave {clave} ya existe")); continue
    sig = limpio(f["glosa"])
    notas = (f"Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, "
             f"p. {f['pagina']}. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior "
             f"al Fraseario de Schultz 1802. Forma de Perea: `{f['forma']}`, conjugación {f['conjugacion']}.")
    if marcas:
        notas += " Marcas de la fuente o del OCR: " + ", ".join(marcas) + "."
    if f.get("forma_parecida_en_lexicon"):
        cf = "; ".join(f"`{k}` «{limpio(v)[:40]}»" for k, v in f["forma_parecida_en_lexicon"].items())
        notas += f" Cf. del Fraseario: {cf} — misma raíz o pariente, aislada con otra geminada o glosa."
    if desamb:
        notas += (f" Clave desambiguada como `{clave}` porque `{f['clave']}` colisiona con una clave "
                  f"existente o con una palabra española (score_linguistico no filtra por fuente).")
    notas += " Fusión fase 1b de D11, 2026-09-12."
    filas.append((clave, sig, "v_raiz", notas))

for f in Y["sueltas"]:
    if "ya_en_lexicon" in f:
        saltadas.append((f["clave"], f"ya en el lexicón")); continue
    clave, desamb = clave_segura(f["clave"])
    if clave in V:
        saltadas.append((f["clave"], f"la clave {clave} ya existe")); continue
    notas = (f"Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. {f['pagina']}. Voz que sale "
             f"de paso en los ejemplos de Schumann/Schultz.")
    if f.get("marcas"):
        notas += " Marcas: " + ", ".join(f["marcas"]) + "."
    if desamb:
        notas += f" Clave desambiguada como `{clave}` (homógrafo)."
    notas += " Fusión fase 1b de D11, 2026-09-12."
    filas.append((clave, limpio(f["glosa"]), f["cat"], notas))

print(f"a fusionar: {len(filas)}   saltadas: {len(saltadas)}")
for r, por in saltadas:
    print(f"   · {r}: {por}")

# ── escribir, al final de VOCABULARIO_BASE (después del bloque de la fase 1) ──
p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
assert "D11 FASE 1b" not in t, "la fase 1b ya está fusionada"
ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
fin = t.index("REGLAS_ASPECTO", ini)
region = t[ini:fin]
ancla = None
for m in re.finditer(r'^\s*"[^"]+":\s*\{.*\},\s*$', region, re.M):
    ancla = m
assert ancla, "no encuentro la última entrada de VOCABULARIO_BASE"
corte = ini + ancla.end()

bloque = ["\n", "    # ══════════════════════════════════════════════════════\n",
          "    # D11 FASE 1b (2026-09-12) — el vocabulario verbal de Schumann\n",
          "    # (ms. 1755) vía Perea 1942, pp. 609-684. Comparanda lokono.\n",
          "    # ══════════════════════════════════════════════════════\n"]
for clave, sig, cat, notas in filas:
    bloque.append(f'    "{clave}": {{"sig": "{sig}", "cat": "{cat}", '
                  f'"fuente": "lokono", "notas": "{notas}"}},\n')
t = t[:corte] + "".join(bloque) + t[corte:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"\nescritas {len(filas)} entradas lokono (fase 1b)")
