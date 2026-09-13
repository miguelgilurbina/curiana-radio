# -*- coding: utf-8 -*-
"""F8, parte taíno: el lexicón tenía dos grafías de `fuente` para el taíno, y
no era una tilde — era una CAPA sin etiqueta.

Medido el 2026-09-12: de las 18 entradas con `fuente: "taino"`,
  - 9 son «Taíno atestiguado: X; cognado Lok. Y; Brinton 1871»
  - 9 son «Reconstrucción hipotética Taíno desde Lok. X; método comparativo»
    — formas GENERADAS por `arahuaco_comparative.reconstruir_taino()`
    aplicando correspondencias LK→TN a una palabra lokono. No son taíno
    atestiguado: son lo que el taíno «debería» tener si la regla acierta.

Contarlas como taíno en un cruce es circular (regla 2 del método: mirar la
capa antes de contar un cognado), y el filtro fonotáctico las dejaba pasar al
94 % porque están construidas a partir de lokono.

Qué hace, y sólo esto:
  - las 9 atestiguadas: `taino` → `taíno`  (grafía canónica; nada más cambia)
  - las 9 reconstruidas: `taino` → `taíno-reconstruido`, el mismo patrón que
    `caquetío-reconstruido`. Ni una forma ni una glosa se toca.
  - deja la huella en `notas`.
Idempotente: si no queda ningún `taino`, no hace nada.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
p = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
t = io.open(p, encoding="utf-8").read()

ENTRADA = re.compile(r'"([^"\n]+)":\s*\{[^{}]*?"fuente":\s*"taino"[^{}]*?\}', re.S)
atest, recon = [], []

def arreglar(m):
    bloque = m.group(0)
    clave = m.group(1)
    if "Reconstrucción hipotética" in bloque:
        nuevo = "taíno-reconstruido"; recon.append(clave)
        huella = ("F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por "
                  "reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces")
    else:
        nuevo = "taíno"; atest.append(clave)
        huella = "F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`"
    bloque = re.sub(r'"fuente":\s*"taino"', f'"fuente": "{nuevo}"', bloque, count=1)
    if '"notas":' in bloque:
        bloque = re.sub(r'("notas":\s*")([^"]*)(")', lambda n: n.group(1) + n.group(2).rstrip() + " · " + huella + n.group(3), bloque, count=1)
    else:
        bloque = bloque[:-1].rstrip().rstrip(",") + f', "notas": "{huella}"}}'
    return bloque

t2 = ENTRADA.sub(arreglar, t)
if t2 == t:
    print("nada que hacer: no queda ningún `taino`"); sys.exit(0)
io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
print(f"atestiguadas → taíno ({len(atest)}): {atest}")
print(f"reconstruidas → taíno-reconstruido ({len(recon)}): {recon}")

# el comparador fonotáctico tiene que conocer la capa nueva, o la pierde
pf = os.path.join(R, "curiana_sim", "curiana_fonotactica.py")
f = io.open(pf, encoding="utf-8").read()
viejo = '''    "taíno": "taíno",
    "taino": "taíno",
'''
nuevo = '''    "taíno": "taíno",
    "taino": "taíno",
    # F8 (2026-09-12): las 9 formas que reconstruir_taino() generó desde el
    # lokono dejan de contarse como taíno. Van aparte, como el caquetío
    # reconstruido: si pasan el filtro al 100 % es porque se hicieron con
    # regla, no porque el taíno se parezca al caquetío.
    "taíno-reconstruido": "taíno reconstruido",
'''
assert viejo in f, "no encuentro FAMILIAS en curiana_fonotactica.py"
io.open(pf, "w", encoding="utf-8", newline="\n").write(f.replace(viejo, nuevo, 1))
print("FAMILIAS actualizado en curiana_fonotactica.py")
