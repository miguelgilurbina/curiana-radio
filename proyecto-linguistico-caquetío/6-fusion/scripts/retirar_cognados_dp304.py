#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Retirar los ocho sets malos de `2-lengua/cognados.yaml` (dp.3.04 de #222).

DECISIÓN
    Miguel, 2026-09-24, a la lista entera de #222: «Ok a todo, que no quede
    ninguna tarea pendiente. Lo único pendiente es lo que tenga que ver con
    docker». Para dp.3.04 la recomendación era «T11 A; T4 G: retirarlos (no
    dicen nada y hoy inflan el recuento)». Registro:
    6-fusion/decisiones_222_documentacion_2026-09-24.yaml.

QUÉ SE RETIRA (T4, #192: 6-fusion/cruce_taino_caquetio_2026-09-21.yaml y
6-fusion/issues-pendientes/taino-caquetio-similitudes-2026-09-21.md §2.4)
    - «el lado caquetío no es caquetío» (4): cognado-022 casabe~casabe,
      cognado-023 piache~bejique, cognado-027 cairi~cai, cognado-028 yuca~yuca;
    - circulares, etnónimos (2): cognado-034 caquetio~taino, cognado-050
      karibna~caribe;
    - «la misma palabra escrita dos veces» (2): cognado-020 canoa~canoa,
      cognado-021 hamaca~hamaca.

CÓMO
    Retirar NO es borrar: cada set pasa ENTERO de `cognados` a
    `no_son_cognados` (la sección que ya guardaba lo que no es un cognado),
    con un `diagnostico` y la huella `retirado`. El `meta` se recuenta aquí
    con el mismo criterio que `curiana_sim/migrar_cognados.py::documento()`
    (regla 1), sin tocar la `nota`.

QUÉ NO CAMBIA
    El motor no lee este YAML: `transducir()` y `reconstruir_caquetio()` leen
    `arahuaco_comparative.COGNADOS`. El score no se mueve. Sí cambia lo que
    miden `compilar_lengua.py`, `medir_sostiene.py`, `cruzar_voz.py` y el
    cruce taíno (6-fusion/scripts/cruce_taino_caquetio.py) la próxima vez que
    se corran (dp.3.09: no se re-corre ahora).

Uso:
    python 6-fusion/scripts/retirar_cognados_dp304.py --dry-run
    python 6-fusion/scripts/retirar_cognados_dp304.py
Idempotente: si los ocho ya están en `no_son_cognados`, no hace nada.
"""
import argparse
import io
import os
import sys

import yaml

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
YAML = os.path.join(R, "2-lengua", "cognados.yaml")

HUELLA = ("dp.3.04 (T4 G) de #222, «Ok a todo», Miguel, 2026-09-24 — "
          "6-fusion/decisiones_222_documentacion_2026-09-24.yaml")

T4 = "T4, #192: 6-fusion/cruce_taino_caquetio_2026-09-21.yaml"
RETIRAR = {
    "cognado-020": ("NO ES UN COGNADO: la misma palabra escrita dos veces (canoa ~ canoa), sin cita. "
                    "Es el préstamo que el castellano tomó del taíno y devolvió a todas partes; "
                    f"prueba que escribimos igual las dos columnas ({T4})"),
    "cognado-021": ("NO ES UN COGNADO: la misma palabra escrita dos veces (hamaca ~ hamaca), sin cita. "
                    f"Mismo caso que cognado-020 ({T4})"),
    "cognado-022": ("EL LADO CAQUETÍO NO ES CAQUETÍO: la forma de la columna CQ, `casabe`, está en el "
                    "lexicón etiquetada `taíno`; el set empareja una voz taína consigo misma y no dice "
                    f"nada del caquetío ({T4})"),
    "cognado-023": ("EL LADO CAQUETÍO NO ES CAQUETÍO: la forma de la columna CQ, `piache`, está en el "
                    "lexicón como `caribe-cháima` y archivada (D10: su lugar lo ocupa `boratio`); "
                    f"piache ~ bejique no dice nada del caquetío ({T4})"),
    "cognado-027": ("EL LADO CAQUETÍO NO ES CAQUETÍO: la forma de la columna CQ, `cairi`, es en el "
                    f"lexicón `kairi`, lokono; cairi ~ cai no dice nada del caquetío ({T4})"),
    "cognado-028": ("EL LADO CAQUETÍO NO ES CAQUETÍO: la forma de la columna CQ, `yuca`, está en el "
                    "lexicón etiquetada `taíno`; el set empareja una voz taína consigo misma "
                    f"({T4})"),
    "cognado-034": ("CIRCULAR: es un etnónimo (caquetio ~ taino). Emparejar el nombre de un pueblo con "
                    "el de otro no es un cognado léxico; y `taíno` ni siquiera es autónimo: es el "
                    f"truncamiento de un título, nitayno (Brinton 1871 p. 13) ({T4})"),
    "cognado-050": ("CIRCULAR: es un etnónimo (karibna ~ caribe). Emparejar el nombre de un pueblo con "
                    f"el de otro no es un cognado léxico ({T4})"),
}


def q(s: str) -> str:
    """Escalar YAML en comillas simples."""
    return "'" + s.replace("'", "''") + "'"


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dry-run", action="store_true", help="imprime y no escribe")
    a = ap.parse_args(argv)

    texto = io.open(YAML, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in texto else "\n"
    antes = yaml.safe_load(texto)

    ya = {r["id"] for r in antes.get("no_son_cognados", [])} & set(RETIRAR)
    if ya == set(RETIRAR):
        print("ya aplicado; nada que hacer")
        return 0
    if ya:
        print(f"⚠ aplicado a medias ({sorted(ya)}): no se toca nada, revisar a mano")
        return 1

    lineas = texto.split(nl)
    ini = lineas.index("cognados:")
    fin = lineas.index("no_son_cognados:")
    assert ini < fin, "se esperaba `cognados:` antes de `no_son_cognados:`"

    # Bloques del tramo `cognados:`: de un «- id:» al siguiente.
    bloques, actual = [], None
    for i in range(ini + 1, fin):
        if lineas[i].startswith("- id: "):
            if actual:
                bloques.append(actual)
            actual = [i, i + 1]
        elif actual:
            actual[1] = i + 1
    if actual:
        bloques.append(actual)

    quitar = {}
    for b_ini, b_fin in bloques:
        rid = lineas[b_ini][len("- id: "):].strip()
        if rid in RETIRAR:
            # sin las líneas en blanco del final del bloque
            while b_fin > b_ini and not lineas[b_fin - 1].strip():
                b_fin -= 1
            quitar[rid] = (b_ini, b_fin)
    faltan = set(RETIRAR) - set(quitar)
    assert not faltan, f"no están en `cognados`: {sorted(faltan)}"

    movidos = []
    for rid in sorted(quitar):
        b_ini, b_fin = quitar[rid]
        bloque = lineas[b_ini:b_fin]
        bloque += ["  diagnostico: " + q(RETIRAR[rid]), "  retirado: " + q(HUELLA)]
        movidos.append(bloque)
        print(f"  retira {rid}: {bloque[1].strip()}")

    borrar = set()
    for b_ini, b_fin in quitar.values():
        borrar.update(range(b_ini, b_fin))
    nuevas = [l for i, l in enumerate(lineas) if i not in borrar]

    # Al final de `no_son_cognados:` (es la última sección del archivo).
    while nuevas and not nuevas[-1].strip():
        nuevas.pop()
    for bloque in movidos:
        nuevas += bloque
    nuevas.append("")

    # meta, recontado como migrar_cognados.documento()
    d = yaml.safe_load(nl.join(nuevas))
    regs, sueltos = d["cognados"], d["no_son_cognados"]
    con = sum(1 for r in regs if r.get("procedencia"))
    lenguas = sorted({l for r in regs for l in r["formas"]})
    nucleo = sorted(l for l in lenguas if l.isupper())
    nuevo_meta = {
        "cognados": len(regs),
        "con_procedencia": con,
        "sin_procedencia": len(regs) - con,
        "lenguas_comparanda": len(lenguas) - len(nucleo),
        "no_son_cognados": len(sueltos),
    }
    assert nucleo == antes["meta"]["lenguas_nucleo"], "cambia el núcleo: revisar a mano"
    m_fin = nuevas.index("cognados:")
    for i in range(m_fin):
        for k, v in nuevo_meta.items():
            if nuevas[i].startswith(f"  {k}: "):
                viejo = nuevas[i]
                nuevas[i] = f"  {k}: {v}"
                if viejo != nuevas[i]:
                    print(f"  meta {k}: {viejo.split(': ', 1)[1]} → {v}")
    salida = nl.join(nuevas)

    # comprobación: las mismas entradas, sólo cambiadas de sección
    d2 = yaml.safe_load(salida)
    ids_antes = {r["id"] for r in antes["cognados"]} | {r["id"] for r in antes["no_son_cognados"]}
    ids_despues = {r["id"] for r in d2["cognados"]} | {r["id"] for r in d2["no_son_cognados"]}
    assert ids_antes == ids_despues, "se perdió o duplicó alguna entrada"
    assert set(RETIRAR) <= {r["id"] for r in d2["no_son_cognados"]}
    assert not set(RETIRAR) & {r["id"] for r in d2["cognados"]}
    for k, v in nuevo_meta.items():
        assert d2["meta"][k] == v, k
    for r in d2["no_son_cognados"]:
        if r["id"] in RETIRAR:
            viejo = next(x for x in antes["cognados"] if x["id"] == r["id"])
            assert {k: r[k] for k in viejo} == viejo, f"{r['id']} cambió de contenido"

    if a.dry_run:
        print("--dry-run: no se escribió nada")
        return 0
    io.open(YAML, "w", encoding="utf-8", newline="").write(salida)
    print(f"escrito {os.path.relpath(YAML, R)}: {len(movidos)} sets a no_son_cognados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
