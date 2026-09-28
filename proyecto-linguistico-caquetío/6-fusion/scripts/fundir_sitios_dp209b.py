# -*- coding: utf-8 -*-
"""dp.2.09 P3 B de #222: lo que Miguel reconoce sobre el terreno (2026-09-27).

Las cuatro identificaciones del mapa vivo que M6 (#216) dejó «a revisar» y que
P3 A escribió como lecturas `hipotesis`. Miguel:
  · La Miraba = Niraba (Esteves p. 54, toponimo-278)            → SE FUNDEN
  · Tabe = Jabe / San José de Tarbes (Esteves p. 44, toponimo-272) → SE FUNDEN
  · Coduto = el caduto del dictado (toponimo-176 → toponimo-219)   → SE FUNDEN
  · «Cumairebo y Curaidebo son dos lugares distintos en Paraguaná» → NO

Fundir: la forma viva (con su coordenada) y la lectura pasan a la entrada de
Esteves; la hipótesis gana su `validacion` y una lectura
`testimonio-residente` de Miguel; y el descartado (138 La Miraba, 135 Tabe,
176 caduto) se retira como `reubicados`, sin mover el contador: un reubicado
con id explícito no gasta turno (migrar_toponimos.py).
Cumairebo se queda como está, con la hipótesis REFUTADA y su testimonio.
Idempotente; `--dry-run` no escribe. Después: migrar_toponimos.py.
"""
import argparse
import ast
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = os.path.join(R, "curiana_sim", "lexicon_toponimos.py")
ap = argparse.ArgumentParser()
ap.add_argument("--dry-run", action="store_true")
ARGS = ap.parse_args()

src = open(P, "rb").read().decode("utf-8")
EOL = "\r\n" if "\r\n" in src else "\n"
t = src.replace(EOL, "\n")
MARCA = "dp.2.09 P3 B de #222"
if MARCA in t:
    print("ya aplicado; nada que hacer")
    sys.exit(0)

FECHA = "2026-09-27"
HUELLA = f"{MARCA}, {FECHA}"
J = lambda v: json.dumps(v, ensure_ascii=False)  # noqa: E731


def rep(a, c):
    global t
    assert t.count(a) == 1, (a[:70], t.count(a))
    t = t.replace(a, c)


def linea(prefijo):
    """La única línea que empieza por `prefijo`; devuelve (línea, valor)."""
    ls = [l for l in t.split("\n") if l.startswith(prefijo)]
    assert len(ls) == 1, (prefijo, len(ls))
    l = ls[0]
    cuerpo = l.split(": ", 1)[1].rstrip().rstrip(",")
    return l, ast.literal_eval(cuerpo)


def testimonio(texto):
    return {"tipo": "testimonio-residente", "lectura": texto, "quien": "Miguel",
            "fecha": FECHA, "eje": "referente"}


def validar(lecturas, veredicto, validacion):
    out = []
    for x in lecturas:
        x = dict(x)
        if x.get("tipo") == "hipotesis":
            x["veredicto"] = veredicto
            x["validacion"] = validacion
        out.append(x)
    return out


# ── 1. el grupo del mapa vivo (OSM) ─────────────────────────────────────
l_cum, lec_cum = linea('            "cumairebo": ')
l_mir, lec_mir = linea('            "la miraba": ')
l_tab, lec_tab = linea('            "tabe": ')
rep(l_cum, '            "cumairebo": ' + J(
    validar(lec_cum, "refutada: son dos lugares distintos",
            f"refutada sobre el terreno por Miguel ({HUELLA})")
    + [testimonio("«Cumairebo y Curaidebo son dos lugares distintos en Paraguaná»")]) + ",")
rep(l_mir + "\n", "")
rep(l_tab + "\n", "")
l_fv, fv = linea('        "formas_vivas": {"cumairebo"')
fv_mir, fv_tab = fv.pop("la miraba"), fv.pop("tabe")
rep(l_fv, '        "formas_vivas": ' + J(fv) + ",")
rep('        "ids": {"cumairebo": "toponimo-132",',
    f'        # {HUELLA}: La Miraba y Tabe se funden en Niraba y Jabe (Esteves);\n'
    '        # siguen en `formas` para que nada se mueva y no se emiten desde aquí.\n'
    '        "reubicados": ["la miraba", "tabe"],\n'
    '        "ids": {"cumairebo": "toponimo-132",')

# ── 2. el grupo del dictado: caduto se funde en Coduto ──────────────────
l_cad, lec_cad = linea('            "caduto": ')
rep("        \"lecturas\": {\n" + l_cad + "\n        },\n", "")
rep('        "ids": {"siburua": "toponimo-165",',
    f'        # {HUELLA}: caduto se funde en Coduto (toponimo-219); sigue en\n'
    '        # `formas` para que nada se mueva y no se emite desde aquí.\n'
    '        "reubicados": ["caduto"],\n'
    '        "ids": {"siburua": "toponimo-165",')

# ── 3. Niraba y Jabe (lote de la cola de Esteves) ───────────────────────
l_lec, lec = linea('        "lecturas": {"tacuato"')
lec["niraba"] = validar(lec_mir, "confirmada", f"confirmada sobre el terreno por Miguel ({HUELLA})") + [
    testimonio("La Miraba (el poblado y el Cerro La Miraba, municipio Moruy) es la Niraba de Esteves")]
lec["jabe"] = validar(lec_tab, "confirmada", f"confirmada sobre el terreno por Miguel ({HUELLA})") + [
    testimonio("Tabe, a unos dos kilómetros de Jadacaquiva, es la Jabe o San José de Tarbes de Esteves")]
rep(l_lec, '        "lecturas": ' + J(lec) + ",\n"
    '        "formas_vivas": ' + J({"niraba": fv_mir, "jabe": fv_tab}) + ",")

# ── 4. Coduto (NIVEL_C, toponimo-219) ───────────────────────────────────
ini = t.index('    "coduto": {\n        "id": "toponimo-219",')
fin = t.index("\n    },\n", ini)
bloque = t[ini:fin]
nuevo = bloque.replace(
    'sin fundirlas.",',
    f'sin fundirlas. FUNDIDAS el {FECHA} ({MARCA}): Miguel reconoce el caduto del dictado '
    '(toponimo-176, que queda reubicado aquí) como este Coduto. Lo que decía aquella entrada: '
    'municipio Carirubana, Paraguaná; Arcaya lista CODUTO y CURARADUTO entre los nombres «de lugares '
    'en las regiones ocupadas por los caquetíos», y Miguel dictó además CODORE: el formante `-duto` '
    'merece censo.",')
assert nuevo != bloque
nuevo = nuevo.replace(
    '        "verificado": "imagen",',
    '        "lecturas": ' + J(
        validar(lec_cad, "confirmada", f"confirmada sobre el terreno por Miguel ({HUELLA})")
        + [testimonio("Coduto (al este de Los Taques) y Coduto / Punta Coduto en Médanos son el «caduto» "
                      "que dictó el 2026-09-10")]) + ",\n"
    '        "forma_viva": ' + J([{"forma": "Coduto", "tipo": "lugar", "lat": 11.817, "lon": -70.213,
                                  "fuente": "osm-kaketiana"}]) + ",\n"
    '        "verificado": "imagen",')
t = t[:ini] + nuevo + t[fin:]

# ── 5. la nota de Curaidebo ─────────────────────────────────────────────
rep('Candidato a ser el mismo nombre (r~m, que NO está entre las permutaciones documentadas): ver §mapa_vivo.",',
    'Candidato a ser el mismo nombre (r~m, que NO está entre las permutaciones documentadas): ver §mapa_vivo. '
    f'NO LO ES ({HUELLA}): «Cumairebo y Curaidebo son dos lugares distintos en Paraguaná» (Miguel).",')

ast.parse(t)
if ARGS.dry_run:
    print("--dry-run: no se escribe")
    sys.exit(0)
open(P, "wb").write(t.replace("\n", EOL).encode("utf-8"))
print("✓ curiana_sim/lexicon_toponimos.py — ahora: python curiana_sim/migrar_toponimos.py")
