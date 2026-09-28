# -*- coding: utf-8 -*-
"""Aplica las ediciones del lexicón del grupo 3 de #222 (el «frente del lexicón»).

Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea pendiente. Lo único
pendiente es lo que tenga que ver con docker». La rama docs/222-grupo3 dejó
escritas, sin tocar el lexicón, las ediciones exactas en
6-fusion/para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml. Este script las
aplica tal cual:

  · dp.3.03 / dp.3.15 / dp.3.08 / dp.3.10 — cada `edicion` del YAML (archivo
    curiana_lexicon.py, dict VOCABULARIO_BASE, campo `notas`): se añade al
    final de `notas` precedido de « · », o se crea `notas`. Nunca cambia forma,
    `sig`, `cat` ni `fuente`.
  · dp.3.08 k5 — `kalínagu` se funde en `kalinagu`: pasa entera a
    FUERA_DEL_HABLA con la huella; `kalinagu` gana la nota de la variante. Se
    queda la de sin tilde: Goeje imprime «Kalinago» (p. 43).
  · dp.3.07 P2 — las voces de Gumilla van a `nota` de sus entradas en
    6-fusion/achagua_neira_ribero_1762.yaml (hay que regenerar después
    curiana_sim/lexicon_achagua.py con generar_lexicon_achagua.py).

Idempotente (cada texto se busca antes de añadirlo); `--dry-run` no escribe.
"""
import argparse
import ast
import json
import os
import re
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEX = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
ACH = os.path.join(R, "6-fusion", "achagua_neira_ribero_1762.yaml")
PROP = os.path.join(R, "6-fusion", "para_el_frente_del_lexicon_222_grupo3_2026-09-24.yaml")
ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()

P = yaml.safe_load(open(PROP, encoding="utf-8"))


def ediciones(x):
    if isinstance(x, dict):
        if x.get("archivo") == "curiana_sim/curiana_lexicon.py" and "texto" in x:
            yield x
            return
        for v in x.values():
            yield from ediciones(v)
    elif isinstance(x, list):
        for v in x:
            yield from ediciones(v)


# ── el lexicón ──────────────────────────────────────────────────────────
src = open(LEX, "rb").read().decode("utf-8")
EOL = "\r\n" if "\r\n" in src else "\n"
t = src.replace(EOL, "\n")


def q(v):
    return json.dumps(v, ensure_ascii=False) if isinstance(v, str) else repr(v)


def _fuera():
    ini = t.index("FUERA_DEL_HABLA: dict[str, dict] = {")
    return ini, t.index("\n}\n", ini)


def _linea(clave):
    """La línea de una entrada activa (fuera de FUERA_DEL_HABLA)."""
    f_ini, f_fin = _fuera()
    ms = [m for m in re.finditer(r'^ +"' + re.escape(clave) + r'":\s*\{.*\},\s*$', t, re.M)
          if not (f_ini < m.start() < f_fin)]
    if not ms:   # entrada escrita en varias líneas: «"clave": {» … «},»
        ms = [m for m in re.finditer(r'^( +)"' + re.escape(clave) + r'":\s*\{\n(?:\1 .*\n)*?\1\},?$', t, re.M)
              if not (f_ini < m.start() < f_fin)]
        assert len(ms) == 1, (clave, len(ms))
        m = ms[0]
        return m, m.group(0), dict(ast.literal_eval("{" + m.group(0).strip().rstrip(",") + "}")[clave])
    assert len(ms) == 1, (clave, len(ms))
    m = ms[0]
    linea = m.group(0)
    _, e = next(iter(ast.literal_eval("{" + linea.strip().rstrip(",") + "}").items()))
    return m, linea, dict(e)


def _escribir(m, linea, e):
    global t
    if "\n" in linea:           # se conserva el formato de varias líneas
        sang = linea[:len(linea) - len(linea.lstrip())]
        cuerpo = ",\n".join(f'{sang}    "{c}": {q(v)}' for c, v in e.items())
        t = t[:m.start()] + linea[:linea.index("{") + 1] + "\n" + cuerpo + "\n" + sang + "}" + \
            ("," if linea.rstrip().endswith(",") else "") + t[m.end():]
        return
    cabeza = linea[:linea.index("{")]
    t = t[:m.start()] + cabeza + "{" + ", ".join(f'"{c}": {q(v)}' for c, v in e.items()) + "}," + t[m.end():]


def anadir_nota(clave, texto):
    m, linea, e = _linea(clave)
    viejas = e.get("notas", "")
    if texto in viejas:
        return False
    e["notas"] = (viejas + " · " + texto) if viejas else texto
    _escribir(m, linea, e)
    return True


n_lex = 0
for ed in ediciones(P):
    assert ed["dict"] == "VOCABULARIO_BASE" and ed["campo"] == "notas", ed
    if anadir_nota(ed["clave"], ed["texto"]):
        n_lex += 1
        print("  · notas", ed["clave"])

# dp.3.08 k5: fundir kalínagu en kalinagu
HUELLA_K5 = "Fundida en `kalinagu` (dp.3.08 de #222, 2026-09-24): la misma voz de Goeje 1939 p. 43."
f_ini, f_fin = _fuera()
if '"kalínagu":' not in t[f_ini:f_fin]:
    m, linea, e = _linea("kalínagu")
    glosa = e.get("es") or e.get("sig")
    t = t[:m.start()] + t[m.end() + 1:]          # la línea y su salto
    e = {**{k: v for k, v in e.items() if k != "notas"},
         "archivada": "2026-09-24 · dp.3.08 k5 de #222 · fundida en `kalinagu`",
         "notas": HUELLA_K5 + " " + e.get("notas", "")}
    f_ini, f_fin = _fuera()
    t = t[:f_fin] + "\n    " + json.dumps("kalínagu", ensure_ascii=False) + ": {" + \
        ", ".join(f'"{c}": {q(v)}' for c, v in e.items()) + "}," + t[f_fin:]
    anadir_nota("kalinagu", f"Variante con tilde `kalínagu` archivada (dp.3.08); su glosa decía '{glosa}'.")
    n_lex += 1
    print("  · kalínagu → FUERA_DEL_HABLA; nota en kalinagu")
ast.parse(t)

# ── el achagua de Neira y Ribero (dp.3.07 P2) ───────────────────────────
a_src = open(ACH, "rb").read().decode("utf-8")
A_EOL = "\r\n" if "\r\n" in a_src else "\n"
lineas = a_src.split(A_EOL)
n_ach = 0
for ed in P["dp.3.07_P2_gumilla_en_neira"]["ediciones"]:
    ent, texto = ed["entrada"], ed["texto"]
    hallados = []
    for i, l in enumerate(lineas):
        if l == f"- castellano: {ent['castellano']}" or l == f"- castellano: '{ent['castellano']}'":
            j = i + 1
            while j < len(lineas) and lineas[j].startswith("  "):
                j += 1
            d = yaml.safe_load("\n".join(lineas[i:j]))[0]
            if d.get("pliego") == ent["pliego"] and d.get("lado") == ent["lado"]:
                hallados.append((i, j, d))
    assert len(hallados) == 1, (ent, len(hallados))
    i, j, d = hallados[0]
    vieja = d.get("nota") or ""
    if texto in vieja:
        continue
    nueva = (vieja + " · " + texto) if vieja else texto
    k = next((x for x in range(i, j) if lineas[x].startswith("  nota:")), None)
    if k is None:
        lineas.insert(j, "  nota: " + json.dumps(nueva, ensure_ascii=False))
    else:
        fin = k + 1
        while fin < j and lineas[fin].startswith("    "):
            fin += 1
        lineas[k:fin] = ["  nota: " + json.dumps(nueva, ensure_ascii=False)]
    n_ach += 1
    print("  · achagua", ent["castellano"], ent["pliego"], ent["lado"])
a_out = A_EOL.join(lineas)
yaml.safe_load(a_out)

print(f"lexicón: {n_lex} ediciones · achagua: {n_ach} notas")
if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
open(LEX, "wb").write(t.replace("\n", EOL).encode("utf-8"))
open(ACH, "wb").write(a_out.encode("utf-8"))
print("✓ escrito")
