# -*- coding: utf-8 -*-
"""Mide qué cubre la parcela T2 de la campaña del taíno.

Regla 1: ninguna cifra a mano. Todo lo que el informe o los YAML digan en
números sale de aquí.

Cruza las tres propuestas de `6-fusion/` con las entradas taínas de
`curiana_lexicon.VOCABULARIO_BASE` y dice cuántas quedan con cita, separando
la atestación PRIMARIA (el cuerpo de una crónica: Las Casas, Pané) de la
SECUNDARIA (Brinton, que recopila a otros — skill §8).

    python 6-fusion/scripts/medir_taino_t2.py
"""
import os
import re
import sys
import unicodedata

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIM = os.path.join(RAIZ, "curiana_sim")
FUSION = os.path.join(RAIZ, "6-fusion")

PROPUESTAS = {
    "las-casas-1875": ("taino_las_casas_1875.yaml", "primaria"),
    "pane-c1498": ("taino_pane_c1498.yaml", "primaria"),
    "brinton-1871": ("taino_brinton_1871.yaml", "secundaria"),
}


def _forzar_utf8():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def entradas_tainas():
    sys.path.insert(0, SIM)
    import curiana_lexicon as lex
    fuera = {}
    for clave, valor in lex.VOCABULARIO_BASE.items():
        if not isinstance(valor, dict):
            continue
        fuente = str(valor.get("fuente") or "")
        if fuente.startswith("taíno"):
            proc = valor.get("procedencia") or {}
            fuera[clave] = {"fuente": fuente, "obra": proc.get("obra")}
    return fuera


def _tokens(texto):
    return set(re.findall(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñç]+", texto))


def _recorrer(nodo, claves, hallados):
    """Busca todo campo `en_el_lexicon` y saca de él claves conocidas."""
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k == "en_el_lexicon" and v not in (None, False):
                for t in _tokens(str(v)):
                    if t in claves:
                        hallados.add(t)
            else:
                _recorrer(v, claves, hallados)
    elif isinstance(nodo, list):
        for v in nodo:
            _recorrer(v, claves, hallados)


def cobertura(claves):
    fuera = {}
    for obra, (fichero, tipo) in PROPUESTAS.items():
        ruta = os.path.join(FUSION, fichero)
        datos = yaml.safe_load(open(ruta, encoding="utf-8"))
        hallados = set()
        _recorrer(datos, claves, hallados)
        fuera[obra] = {"tipo": tipo, "claves": hallados, "fichero": fichero,
                       "bloques": _contar_bloques(datos)}
    return fuera


def _contar_bloques(datos):
    n = {}
    for k in ("voces", "metalinguistico", "onomastica", "teonimos_y_rito",
              "vocabulario_antillano", "correspondencias_para_T4"):
        v = datos.get(k)
        if isinstance(v, list):
            n[k] = len(v)
        elif isinstance(v, dict):
            for sk, sv in v.items():
                if isinstance(sv, list):
                    n[f"{k}.{sk}"] = len(sv)
    return n


def main():
    _forzar_utf8()
    tainas = entradas_tainas()
    claves = set(tainas)
    con_obra = [k for k, v in tainas.items() if v["obra"]]

    print("=" * 66)
    print("CAMPAÑA DEL TAÍNO — parcela T2 (Las Casas · Pané · Brinton)")
    print("=" * 66)
    print(f"entradas taínas en VOCABULARIO_BASE : {len(tainas)}")
    for etiqueta in sorted({v['fuente'] for v in tainas.values()}):
        n = sum(1 for v in tainas.values() if v["fuente"] == etiqueta)
        print(f"   {etiqueta:<24}{n}")
    print(f"con procedencia.obra HOY            : {len(con_obra)}")

    cob = cobertura(claves)
    print("\n--- lo que cada propuesta atestigua ---")
    for obra, d in cob.items():
        print(f"{obra:<16}({d['tipo']:<10}) {len(d['claves']):>2} entradas  "
              f"{sorted(d['claves'])}")
        for k, v in sorted(d["bloques"].items()):
            print(f"                  {k}: {v}")

    prim = set().union(*[d["claves"] for d in cob.values()
                         if d["tipo"] == "primaria"])
    sec = set().union(*[d["claves"] for d in cob.values()
                        if d["tipo"] == "secundaria"])
    union = prim | sec
    print("\n--- resumen ---")
    print(f"con cita PRIMARIA (Las Casas o Pané)          : "
          f"{len(prim)} de {len(tainas)}")
    print(f"sólo por vía SECUNDARIA (Brinton)             : "
          f"{len(sec - prim)} de {len(tainas)}")
    print(f"TOTAL que deja de estar sin procedencia       : "
          f"{len(union)} de {len(tainas)}")
    print(f"siguen sin ninguna cita en esta parcela       : "
          f"{len(claves - union)}")
    print(f"   {sorted(claves - union)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
