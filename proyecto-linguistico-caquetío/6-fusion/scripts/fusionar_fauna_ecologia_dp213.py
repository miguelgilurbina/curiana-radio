# -*- coding: utf-8 -*-
"""dp.2.13 de #222: las propuestas de las tres parcelas de fauna entran a
3-mundo/corpus/ecologia.yaml.

Miguel, 2026-09-24: «Ok a todo, que no quede ninguna tarea pendiente. Lo único
pendiente es lo que tenga que ver con docker». La recomendación (D1 para las
tres parcelas; FA3 (c) A) está en 6-fusion/decisiones_pendientes_2026-09-23.yaml
§dp.2.13 y el registro en 6-fusion/decisiones_222_mundo_2026-09-24.yaml.

  · FA1 tierra (#211): las 7 de `propuestas_ecologia`.
  · FA2 aves (#205): las 5 de `propuestas_ecologia.entradas`.
  · FA3 mar (#208): los 7 `hecho-nuevo` de `propuestas_ecologia`, llevados al
    esquema del corpus (sin `tipo`; `referencia` desde la procedencia; el
    `apoyo` va a `nota`), y pe-7 (re-etiqueta): la identificación del cunaro de
    ecologia-015 queda EN DISPUTA, sin fijar (FA3 (c) A).

Los id provisionales se sustituyen por los siguientes libres; cada entrada
lleva en `nota` de qué propuesta sale. La capa y la procedencia no se tocan.
La única corrección de forma: `locacion: salina` no es una locación del motor
(`curiana_state.LOCACIONES`) y pasa a `salinar`.
Idempotente (si ya están, no hace nada); `--dry-run` no escribe.
"""
import argparse
import os
import sys

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ECO = os.path.join(R, "3-mundo", "corpus", "ecologia.yaml")
F = os.path.join(R, "6-fusion")
HUELLA = "dp.2.13 de #222 («Ok a todo», Miguel, 2026-09-24)"
ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()


def cargar(nombre):
    return yaml.safe_load(open(os.path.join(F, nombre), encoding="utf-8"))["propuestas_ecologia"]


def referencia(p):
    pag = p.get("pagina")
    return f"{p['obra']}" + (f", p. {pag}" if pag not in (None, "") else "")


def cita(a):
    return "; ".join(referencia(x) for x in (a if isinstance(a, list) else [a]))


DOMINIOS_MAR = {"pe-3": ["ecologia", "fauna"], "pe-4": ["ecologia", "fauna"],
                "pe-5": ["ecologia", "fauna"], "pe-6": ["ecologia", "fauna", "sonido"]}
ORDEN = ["id", "voz", "contenido", "fuente", "referencia", "procedencia", "dominios",
         "agentes_relacionados", "palabra_lexicon", "locacion", "identificacion", "lectura",
         "limite", "implicacion_simulacion", "nota"]

nuevas = []
for e in cargar("fauna_paraguana_tierra_2026-09-22.yaml"):
    e = dict(e)
    e["nota"] = f"Fusionada de 6-fusion/fauna_paraguana_tierra_2026-09-22.yaml `{e['id']}` (FA1, #211) por {HUELLA}"
    nuevas.append(e)
for e in cargar("fauna_paraguana_aves_2026-09-22.yaml")["entradas"]:
    e = dict(e)
    if e.get("locacion") == "salina":
        e["locacion"] = "salinar"
    e["nota"] = f"Fusionada de 6-fusion/fauna_paraguana_aves_2026-09-22.yaml `{e['id']}` (FA2, #205) por {HUELLA}"
    nuevas.append(e)
disputa = None
for e in cargar("fauna_paraguana_mar_2026-09-22.yaml"):
    if e["tipo"] == "re-etiqueta":
        assert e["id"] == "pe-7" and e["objetivo"] == "ecologia-015"
        disputa = e
        continue
    assert e["tipo"] == "hecho-nuevo", e["id"]
    n = {k: v for k, v in e.items() if k not in ("tipo", "apoyo")}
    n["referencia"] = cita(e["procedencia"])
    n["dominios"] = DOMINIOS_MAR.get(e["id"], ["ecologia", "pesca"])
    n["agentes_relacionados"] = []
    n["palabra_lexicon"] = None
    n["nota"] = (f"Fusionada de 6-fusion/fauna_paraguana_mar_2026-09-22.yaml `{e['id']}` (FA3, #208) por {HUELLA}"
                 + (f". Apoyo: {cita(e['apoyo'])}" if e.get("apoyo") else ""))
    nuevas.append(n)

src = open(ECO, "rb").read().decode("utf-8")
EOL = "\r\n" if "\r\n" in src else "\n"
t = src.replace(EOL, "\n")
if HUELLA in t:
    print("ya aplicado; nada que hacer")
    sys.exit(0)
d = yaml.safe_load(t)
libre = max(int(h["id"].split("-")[1]) for h in d["entradas"]) + 1
bloques = []
for i, e in enumerate(nuevas):
    e["id"] = f"ecologia-{libre + i:03d}"
    if e.get("locacion") is None:
        e.pop("locacion", None)
    e = {k: e[k] for k in ORDEN if k in e} | {k: v for k, v in e.items() if k not in ORDEN}
    s = yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=110, default_flow_style=False)
    ls = s.rstrip("\n").split("\n")
    bloques.append("\n".join(["  - " + ls[0]] + ["    " + x for x in ls[1:]]))
    print(f"  + {e['id']}  ({e['fuente']})  {e['contenido'][:70]}…")

# la identificación del cunaro, en disputa (FA3 (c) A)
ini = t.index("\n  - id: ecologia-015\n")
fin = t.index("\n  - id: ", ini + 5)
linea = ("    identificacion: " + yaml.safe_dump(
    f"EN DISPUTA ({HUELLA}, FA3 (c) A; 6-fusion/fauna_paraguana_mar_2026-09-22.yaml pe-7): "
    + disputa["contenido"] + f" ({cita(disputa['procedencia'])}). No se fija ninguna de las dos: "
    "el `contenido` sigue diciendo lo que decía, y esto dice que la especie del cunaro no está resuelta",
    allow_unicode=True, width=10**6).rstrip("\n").removesuffix("\n...").strip())
t = t[:fin] + "\n" + linea + t[fin:]
print("  · ecologia-015: identificación del cunaro EN DISPUTA")

corte = t.index("\nhuecos_lexicos:")
t = t[:corte].rstrip("\n") + "\n" + "\n".join(bloques) + "\n" + t[corte:]
d2 = yaml.safe_load(t)
assert len(d2["entradas"]) == len(d["entradas"]) + len(nuevas)
print(f"{len(nuevas)} entradas nuevas: ecologia-{libre:03d} a ecologia-{libre + len(nuevas) - 1:03d}")
if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
open(ECO, "wb").write(t.replace("\n", EOL).encode("utf-8"))
print("✓ 3-mundo/corpus/ecologia.yaml")
