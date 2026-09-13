# -*- coding: utf-8 -*-
"""Miguel, 2026-09-12: «en cuanto a lo de Medina, todas entran como voces nuevas».

Fusiona al lexicón las voces de 6-fusion/tainismos_en_medina.yaml como
`caquetío-reconstruido` — el precedente de kanoa/hamaca/konuko: cognado taíno
citado (DRAE/Alvarado), sin atestación caquetía colonial, recogidas por Medina
Colina en el habla paraguanera. La vía pudo ser el español: por eso
reconstruido y no atestiguado.

Clave = lema fonémico de D5 (aplicar_fase2_d5.lema_fonemico): gua→wa, gue→ge,
c→k salvo ce/ci, z→s, v→b; la forma castellana va en `forma_fuente`, como en
konuko/conuco. `naguas` no es nueva: el lexicón ya tenía `nagua` (taíno) →
se re-etiqueta. `hicotea` entra como `hikotea` y se anota que convive con la
acuñación `hikoteya` (hipotético): retirar la acuñación es decisión aparte.
Idempotente.
"""
import io, os, re, sys, yaml
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(R, "curiana_sim"))
import curiana_lexicon as CL
from aplicar_fase2_d5 import lema_fonemico

V = CL.VOCABULARIO_BASE
Y = yaml.safe_load(io.open(os.path.join(R, "6-fusion", "tainismos_en_medina.yaml"), encoding="utf-8"))
por_voz = {v["voz"]: v for v in Y["voces"]}

# (voz de Medina, sig corto, cat, categoria)
FICHAS = [
 ("coa",      "coa: palo de madera aguzado con que se abre el hueco de la siembra y se deposita la semilla", "sust", "agricultura"),
 ("comején",  "comején, termita que se come la madera por dentro", "sust", "fauna"),
 ("guayacán", "guayacán, árbol de madera durísima y mucho follaje; hoy casi extinto en la península", "sust", "flora"),
 ("hico",     "hico: cada cuerda de la hamaca; por extensión, toda cuerda o soga", "sust", "casa"),
 ("hicotea",  "hicotea, tortuga de agua dulce comestible (morrocoy en el resto del país)", "sust", "fauna"),
 ("jaiba",    "jaiba: cangrejo de mar; también broma o chanza molesta", "sust", "fauna"),
 ("jején",    "jején, mosquito diminuto de picada muy molesta", "sust", "fauna"),
 ("maguey",   "maguey: la vara larga de la inflorescencia del cocuy o sisal", "sust", "flora"),
 ("nigua",    "nigua, pulga que anida bajo la piel y cría en ella (Tunga penetrans); hoy desaparecida", "sust", "fauna"),
 ("siguato",  "siguato: desganado, apático, triste (oriente de la península); pescado que empieza a descomponerse (occidente, entre pescadores)", "adj", "estado"),
 ("yaguaza",  "yaguaza, ave comestible de aguas cenagosas; hoy extinguida en la península", "sust", "fauna"),
]
RELABEL = {"naguas": "nagua"}          # ya estaba en el lexicón como taíno

def limpio(s): return str(s).replace('"', "'").replace("\\", "").strip()

p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()
if "TAINISMOS DE MEDINA" in t:
    print("ya fusionado"); sys.exit(0)

filas = []
for voz, sig, cat, categoria in FICHAS:
    d = por_voz[voz]
    clave = lema_fonemico(voz)
    assert clave not in V, f"colisión: {clave}"
    pag = f"p. {d['pagina']}" if d.get("pagina") else "página no dictada (⚠️ pendiente)"
    notas = (f"Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». "
             f"Medina Colina, Del Habla Paraguanera, {pag}: «{limpio(d['glosa_libro'])[:220]}». "
             f"Etimología: {limpio(d['etimologia'])[:120]}. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel "
             f"revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, "
             f"sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «{voz}».")
    if voz == "hicotea":
        notas += " ⚠️ Convive con `hikoteya` 'tortuga', acuñación de la simulación (caquetío-hipotético desde F8): retirar la acuñación es decisión aparte."
    if voz == "siguato":
        notas += " Es la isoglosa intrapeninsular mc-mundo-027 del dictado (oriente/occidente, y por oficio)."
    filas.append((clave, sig, cat, categoria, voz, notas))

ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
fin = t.index("REGLAS_ASPECTO", ini)
region = t[ini:fin]
ancla = None
for m in re.finditer(r'^\s*"[^"]+":\s*\{.*\},\s*$', region, re.M):
    ancla = m
corte = ini + ancla.end()
bloque = ["\n", "    # ══════════════════════════════════════════════════════\n",
          "    # TAINISMOS DE MEDINA (2026-09-12) — decisión de Miguel: voces de origen\n",
          "    # taíno, panhispánicas, recogidas en el habla paraguanera. Reconstruidas,\n",
          "    # no atestiguadas (precedente kanoa/hamaca/konuko).\n",
          "    # ══════════════════════════════════════════════════════\n"]
for clave, sig, cat, categoria, voz, notas in filas:
    bloque.append(f'    "{clave}": {{"sig": "{limpio(sig)}", "cat": "{cat}", "fuente": "caquetío-reconstruido", '
                  f'"forma_fuente": "{voz}", "categoria": "{categoria}", "notas": "{notas}"}},\n')
t = t[:corte] + "".join(bloque) + t[corte:]

# nagua: re-etiquetar
d = por_voz["naguas"]
m = re.search(r'^(\s*"nagua":\s*\{)', t, re.M); assert m
i0 = m.end(); i1 = t.index("},", i0); seg = t[i0:i1]
assert '"fuente": "taíno"' in seg
huella = (f"Decisión de Miguel 2026-09-12 (tainismos de Medina): Medina Colina p. {d['pagina']} s.v. naguas «{limpio(d['glosa_libro'])[:120]}» "
          f"→ caquetío-reconstruido como kanoa/hamaca/konuko; etiqueta anterior `taíno`")
seg = seg.replace('"fuente": "taíno"', '"fuente": "caquetío-reconstruido"', 1)
seg = re.sub(r'("notas":\s*")', lambda n: n.group(1) + huella + " · ", seg, count=1) if '"notas":' in seg else seg.rstrip() + f', "notas": "{huella}"'
t = t[:i0] + seg + t[i1:]
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
for clave, sig, cat, categoria, voz, _ in filas:
    print(f"  + {clave:10} ← {voz:10} {cat:4} {categoria}")
print("  ~ nagua      taíno → caquetío-reconstruido")
print(f"fusionadas {len(filas)} nuevas + 1 re-etiquetada")

# dejar dicho en la propuesta
yp = os.path.join(R, "6-fusion", "tainismos_en_medina.yaml")
Y["meta"]["fusionado"] = "2026-09-12 — Miguel: «todas entran como voces nuevas». Aplicado por 6-fusion/scripts/fusionar_tainismos_medina.py; nagua re-etiquetada, las otras 11 nuevas con clave = lema fonémico D5"
io.open(yp, "w", encoding="utf-8", newline="\n").write(yaml.safe_dump(Y, allow_unicode=True, sort_keys=False, width=110))
