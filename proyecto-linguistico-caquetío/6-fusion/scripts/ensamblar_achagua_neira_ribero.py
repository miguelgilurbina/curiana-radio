# -*- coding: utf-8 -*-
"""Recalcula las cifras de `6-fusion/achagua_neira_ribero_1762.yaml`.

Regla 1 del proyecto: ninguna cifra a mano. Todo lo que vive en
`meta.cobertura` y en `meta.censo_de_terminaciones` se mide aqui, contando
sobre el propio YAML, y se reescribe en su sitio.

    python 6-fusion/scripts/ensamblar_achagua_neira_ribero.py
    python 6-fusion/scripts/ensamblar_achagua_neira_ribero.py --check   # no escribe

No toca `vocabulario`, `arte`, `calibracion_jahn` ni `dudas`: solo mide.
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

YAML = Path(__file__).resolve().parents[2] / "6-fusion" / "achagua_neira_ribero_1762.yaml"

CABECERA = """\
# ══════════════════════════════════════════════════════════════════════
# ACHAGUA — Neira y Ribero 1762 (copia de 1788, Real Biblioteca II/2910)
# PROPUESTA (regla 5). Comparanda, NO caquetio. Transcripcion por vision.
# Generado por 6-fusion/scripts/ensamblar_achagua_neira_ribero.py — las cifras
# de `cobertura` se miden (regla 1).
# ══════════════════════════════════════════════════════════════════════
"""

# El vocabulario castellano→achagua ocupa del pliego 28 (dcha.) al 98 (izq.).
PRIMER_PLIEGO, ULTIMO_PLIEGO = 28, 98

# Las mismas terminaciones que conto la primera pasada, para que las dos
# medidas se puedan comparar. La pregunta de fondo es la `-are`/`-re` que Fabo
# declara «propia y exclusiva» del achagua.
TERMINACIONES = ["si", "ba", "ri", "yi", "cayi", "na", "mi",
                 "are", "ure", "re", "ere", "ire"]
ARE_RE = ["are", "ure", "re", "ere", "ire"]

# Separadores dentro de la columna achagua de una entrada.
CORTE = re.compile(r",|\bvel\b|\bv\.\s*", re.IGNORECASE)


def _forzar_utf8() -> None:
    """La consola de Windows es cp1252 (trampa medida del proyecto)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:  # pragma: no cover
        pass


def cargar() -> dict:
    with io.open(YAML, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def guardar(d: dict) -> None:
    with io.open(YAML, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(CABECERA)
        yaml.safe_dump(d, fh, allow_unicode=True, sort_keys=False, width=110)


def sin_tildes(s: str) -> str:
    """El copista acentua a bulto (`Guabasí`, `Cuitaminarí`): el acento no es
    parte de la terminacion, asi que se descarta antes de contar."""
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def formas_sueltas(entradas) -> list[str]:
    """Parte la columna achagua de cada entrada en formas independientes."""
    formas = []
    for e in entradas:
        crudo = str(e.get("achagua") or "")
        for trozo in CORTE.split(crudo):
            forma = trozo.strip().strip(".:;=[]()").strip()
            if forma and " " not in forma:
                formas.append(sin_tildes(forma.lower()))
    return formas


def medir(d: dict) -> tuple[dict, dict]:
    voc = d["vocabulario"]

    pliegos = sorted({e["pliego"] for e in voc if isinstance(e.get("pliego"), int)})
    esperados = set(range(PRIMER_PLIEGO, ULTIMO_PLIEGO + 1))
    huecos = sorted(esperados - set(pliegos))

    por_letra = Counter(e.get("letra") for e in voc if e.get("letra"))
    letras = sorted(por_letra)

    verbos = d.get("arte", {}).get("verbos", {}).get("entradas", [])
    pliegos_arte = sorted({e["pliego"] for e in verbos if isinstance(e.get("pliego"), int)})

    cal = d.get("calibracion_jahn", [])
    veredictos = Counter(c.get("veredicto") for c in cal)

    dudas = d.get("dudas", [])
    resueltas = [x for x in dudas if str(x.get("resuelta", "")).startswith("resuelta: sí")]
    parciales = [x for x in dudas if str(x.get("resuelta", "")).startswith("resuelta: parcialmente")]

    cobertura = {
        "pliegos_leidos": pliegos,
        "pliegos_del_vocabulario": f"{PRIMER_PLIEGO}-{ULTIMO_PLIEGO}",
        "huecos_en_el_vocabulario": huecos or "ninguno: el vocabulario esta leido de punta a punta",
        "letras_vistas": letras,
        "letras_completas": (
            letras
            if not huecos
            else ["medir: quedan pliegos sin leer, ver `huecos_en_el_vocabulario`"]
        ),
        "entradas_por_letra": {k: por_letra[k] for k in letras},
        "entradas": len(voc),
        "entradas_del_arte_verbos": len(verbos),
        "pliegos_del_arte_minados": pliegos_arte,
        "dudas": len(dudas),
        "dudas_resueltas": len(resueltas),
        "dudas_resueltas_en_parte": len(parciales),
        "voces_jahn_calibradas": len(cal),
        "coinciden": veredictos.get("coincide", 0),
        "difieren": veredictos.get("difiere", 0),
        "no_estan": veredictos.get("no-esta", 0),
    }

    formas = formas_sueltas(voc)
    cuenta = {t: sum(1 for f in formas if f.endswith(t)) for t in TERMINACIONES}
    # `re` incluiria a `are`/`ure`/`ere`/`ire`; se descuentan para no contar dos veces.
    cuenta["re"] -= sum(cuenta[t] for t in ("are", "ure", "ere", "ire"))
    cuenta["ri"] -= cuenta["cayi"] * 0  # (no se solapan; se deja explicito)
    cuenta["yi"] -= cuenta["cayi"]

    censo = {
        "que_mide": ("sobre las formas achagua sueltas de `vocabulario` (separadas por coma, `vel` o "
                     "`v.`), cuantas acaban en cada terminacion. Medido por "
                     "6-fusion/scripts/ensamblar_achagua_neira_ribero.py, no contado a mano. "
                     "`-yi` excluye `-cayi` y `-re` excluye `-are/-ure/-ere/-ire`, para no contar dos veces"),
        "formas_contadas": len(formas),
        "por_terminacion": dict(sorted(cuenta.items(), key=lambda kv: -kv[1])),
        "are_re_total": sum(cuenta[t] for t in ARE_RE),
        "are_re_porcentaje": round(100 * sum(cuenta[t] for t in ARE_RE) / max(len(formas), 1), 2),
        "lectura": ("Fabo declara `-are`/`-re` «propia y exclusiva» del achagua. Medido sobre el "
                    "vocabulario entero, la terminacion dominante NO es -are sino -si (el absoluto de "
                    "no-poseido, que cae en cuanto el nombre se posee) y -yi/-cayi (adjetival). La -re "
                    "existe y es real, pero es minoritaria."),
    }
    return cobertura, censo


def main() -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="mide y enseña, pero no escribe")
    args = ap.parse_args()

    d = cargar()
    antes = len(d["vocabulario"])
    cobertura, censo = medir(d)

    print(f"pliegos leidos del vocabulario : {len(cobertura['pliegos_leidos'])} "
          f"de {ULTIMO_PLIEGO - PRIMER_PLIEGO + 1}")
    print(f"huecos                         : {cobertura['huecos_en_el_vocabulario']}")
    print(f"letras vistas                  : {' '.join(cobertura['letras_vistas'])}")
    print(f"entradas del vocabulario       : {cobertura['entradas']}")
    print(f"entradas de arte.verbos        : {cobertura['entradas_del_arte_verbos']}")
    print(f"dudas                          : {cobertura['dudas']} "
          f"({cobertura['dudas_resueltas']} resueltas, "
          f"{cobertura['dudas_resueltas_en_parte']} en parte)")
    print(f"calibracion con Jahn           : {cobertura['coinciden']} coinciden / "
          f"{cobertura['difieren']} difieren / {cobertura['no_estan']} no estan")
    print(f"formas achagua contadas        : {censo['formas_contadas']}")
    print(f"  -are/-re                     : {censo['are_re_total']} "
          f"({censo['are_re_porcentaje']} %)")
    print("  las cinco mas frecuentes     : " +
          ", ".join(f"-{k} {v}" for k, v in list(censo["por_terminacion"].items())[:5]))

    if args.check:
        print("\n--check: no se escribio nada")
        return 0

    d["meta"]["cobertura"] = cobertura
    d["meta"]["censo_de_terminaciones"] = censo
    guardar(d)

    d2 = cargar()
    assert len(d2["vocabulario"]) == antes, "el YAML perdio entradas al guardar"
    assert d2["meta"]["cobertura"]["entradas"] == antes
    print(f"\nescrito en {YAML.name}; el fichero reparsea y conserva sus {antes} entradas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
