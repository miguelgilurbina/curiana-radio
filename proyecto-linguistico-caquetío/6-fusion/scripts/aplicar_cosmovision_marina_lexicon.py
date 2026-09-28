# -*- coding: utf-8 -*-
"""La parte del LEXICÓN de la campaña de la cosmovisión marina (cc.10).

Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea pendiente»; se
aplica lo recomendado en 6-fusion/issues-pendientes/cosmovision-marina-2026-09-24.md:
  · (e) A — `barana`: la nota se corrige (no la glosa); Goeje p. 55 la da como
    forma de HOMBRES, caribe/tupí.
  · (e) B — `sawaka`: sólo se anota; degradarla movería el nombre del boratio
    Sawaka del elenco.
  · (g) A — `huracan` y `cobo`: se anota lo que dicen las primarias, sin tocar
    la glosa (D7).
Idempotente; `--dry-run` imprime y no escribe.
"""
import argparse
import ast
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
MARCA = "cc.10 (e) A, cosmovisión marina"
ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()
src = open(P, "rb").read().decode("utf-8")
if MARCA in src:
    print("ya aplicado; nada que hacer")
    sys.exit(0)
EOL = "\r\n" if "\r\n" in src else "\n"
t = src.replace(EOL, "\n")
FUENTE = "6-fusion/cosmovision_marina_2026-09-24.yaml"


def q(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, str) else repr(v)


def tocar(clave, notas):
    """`notas` es una función: notas_viejas -> notas_nuevas."""
    global t
    ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
    fin = t.index("\n}\n", ini)
    ms = [m for m in re.finditer(r'^    "' + re.escape(clave) + r'":\s*\{.*\},\s*$', t, re.M)
          if ini < m.start() < fin]
    assert len(ms) == 1, clave
    m = ms[0]
    linea = m.group(0)
    _, e = next(iter(ast.literal_eval("{" + linea.strip().rstrip(",") + "}").items()))
    e = dict(e)
    e["notas"] = notas(e.get("notas", ""))
    cabeza = linea[:linea.index("{")]
    t = t[:m.start()] + cabeza + "{" + ", ".join(f'"{c}": {q(v)}' for c, v in e.items()) + "}," + t[m.end():]
    print("  ·", clave)


tocar("barana", lambda n: (
    "Garifuna barana = gran cuerpo de agua · CORREGIDO el 2026-09-24 (" + MARCA + ", «Ok a "
    "todo»): la nota decía «cognado de CQ para, LK bara, PA *para», y Goeje 1939 p. 55 da "
    "`barana` como la forma de HOMBRES, de origen caribe/tupí (parana); la del lado arahuaco, "
    "la que va con el caquetío `para` y el lokono `bara`, es la de MUJERES: balaua (Goeje p. 55), "
    "«la mer, balànna, f bálaoüa» (Breton 1666 p. 242, en imagen). " + FUENTE))
tocar("sawaka", lambda n: n + (
    " · cc.10 (e) B, cosmovisión marina (2026-09-24, «Ok a todo»): SÓLO SE ANOTA. Es una voz "
    "de papiamento que van Buurt atribuye al caquetío «with a subjective element»; por la regla "
    "2 sería `reconstruido`, pero es la raíz del nombre del boratio mayor del elenco (Sawaka) y "
    "degradarla mueve el elenco: queda escrito, sin decidir en esta tanda. Y es la tierra de los "
    "muertos ABAJO, no mar adentro (" + FUENTE + ")"))
tocar("huracan", lambda n: n + (
    " · cc.10 (g) A (2026-09-24): sin procedencia. Oviedo, Las Casas y Anglería glosan "
    "huracán como TORMENTA; la tormenta de Pané es el cemí Guabancex. Lo de «espíritu del "
    "viento destructor» no lo dice ninguna primaria del repo. La glosa no se toca (D7): se "
    "anota (" + FUENTE + ")"))
tocar("cobo", lambda n: n + (
    " · cc.10 (g) A (2026-09-24): Pané dice «el cobo es el caracol de mar»; no hay trompeta "
    "de caracol taína en el repo (los caracoles de Anglería y de Paria son sonajas). La glosa "
    "no se toca (D7): se anota (" + FUENTE + ")"))
ast.parse(t)
if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
open(P, "wb").write(t.replace("\n", EOL).encode("utf-8"))
print("✓ curiana_sim/curiana_lexicon.py")
