#!/usr/bin/env python3
"""LA TABLA DE MORFEMAS de `2-lengua/morfologia.md`, emitida desde la medición.

POR QUÉ EXISTE. La nota de morfología tiene que decir, por morfema, cuatro
cosas: **capa epistémica, cita, si el motor lo enseña y si el scorer lo
reconoce**. Esas cuatro columnas son las que hacen legibles las cuatro
patologías del issue `morfologia-revision-2026-09-20.md` §2 sin tener que
creerse ninguna prosa:

  (a) lo ENSEÑA y el canon no lo declara  →  capa `canon-simulación` + enseñado
  (b) el canon lo DECLARA y el scorer no lo ve  →  la segunda tabla
  (c) apoyo SÓLO en el andamio D11  →  capa `reconstruido-andamio-d11`
  (d) lo enseña y no hay clave foránea  →  enseñado + `sin-procedencia`

Y son cuatro columnas que **nadie debe escribir a mano** (regla 1): salen de
`6-fusion/medicion_morfologia_2026-09-20.yaml`, que genera
`6-fusion/scripts/auditar_morfologia.py` leyendo el motor y la base.

Este script NO mide nada: relee la medición y la imprime en markdown. Si la
medición se vuelve a correr, la tabla se vuelve a emitir y se pega en la nota.

    python 6-fusion/scripts/tabla_morfemas.py            # las dos tablas
    python 6-fusion/scripts/tabla_morfemas.py --check    # ¿cuadran los totales?
    python 6-fusion/scripts/tabla_morfemas.py --medicion <ruta.yaml>
"""

from __future__ import annotations

import argparse
import os
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
FUSION = os.path.dirname(AQUI)
MEDICION = os.path.join(FUSION, "medicion_morfologia_2026-09-20.yaml")

# Cómo se dice en la tabla cada puerta del motor. La clave es el prefijo de lo
# que escribe el auditor en `reconocido_en`; el valor, la etiqueta corta.
PUERTAS = [
    ("_PREFIJOS_CAQ", "desafija"),
    ("_SUFIJOS_CAQ", "desafija"),
    ("_AFIJOS_SUELTOS", "suelto"),
    ("_aspectos_morfologicos", "**aspecto (2/10 pts)**"),
    ("score_linguistico.es_arahuaco", "**es_arahuaco**"),
]

CAPA_CORTA = {
    "reconstruido-andamio-d11": "reconstruido · andamio D11",
    "canon-simulación": "canon-simulación",
    "atestiguado": "**atestiguado**",
    "reconstruido": "reconstruido",
    "retirada": "retirada",
}


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8", errors="replace")


def cargar(ruta: str) -> dict:
    with open(ruta, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _cita(m: dict) -> str:
    citas = m.get("citas") or []
    if citas:
        return " · ".join(f"[[{c}]]" for c in citas)
    if m.get("deuda"):
        return f"⚠️ `deuda: {m['deuda']}`"
    return "—"


def _ensena(m: dict) -> str:
    plantillas = m.get("ensenado_en") or []
    if not plantillas:
        return "no"
    return f"sí ({len(plantillas)})"


def _reconoce(m: dict) -> str:
    crudo = m.get("reconocido_en") or []
    etiquetas: list[str] = []
    for linea in crudo:
        for prefijo, etiqueta in PUERTAS:
            if linea.startswith(prefijo) and etiqueta not in etiquetas:
                etiquetas.append(etiqueta)
    return " · ".join(etiquetas) if etiquetas else "no"


def tabla_del_motor(med: dict) -> list[str]:
    """Los 21 morfemas del motor: capa, cita, enseña, reconoce, uso."""
    detalle = med["inventario"]["detalle"]
    usos = {u["forma"]: u["usos"] for u in med["uso"]["por_morfema"]}
    # Un morfema declarado que nadie usó no es «sin dato»: es un CERO medido, y
    # el cero es el argumento de d21.9. Los retirados sí quedan fuera del censo.
    for forma in med["uso"].get("morfemas_declarados_que_nadie_usa") or []:
        usos.setdefault(forma, 0)

    filas = sorted(
        detalle,
        key=lambda m: (-usos.get(m["forma"], -1), m["forma"]),
    )

    out = [
        "| Morfema | Clase | Capa | Cita (clave foránea) | ¿Lo enseña? | ¿Lo reconoce el scorer? | Usos |",
        "|---|---|---|---|---|---|---:|",
    ]
    for m in filas:
        u = usos.get(m["forma"])
        if u is None:
            n = "fuera del censo"
        elif u == 0:
            n = "**0**"
        else:
            n = f"{u:,}".replace(",", ".")
        out.append(
            "| `{forma}` | {clase} | {capa} | {cita} | {ensena} | {reconoce} | {n} |".format(
                forma=m["forma"],
                clase=m["clase"],
                capa=CAPA_CORTA.get(m["capa"], m["capa"]),
                cita=_cita(m),
                ensena=_ensena(m),
                reconoce=_reconoce(m),
                n=n,
            )
        )
    return out


def tabla_del_canon(med: dict) -> list[str]:
    """Patología (b): lo que el canon de datos declara y el scorer no ve."""
    det = med["patologias"]["b_el_canon_declara_lo_que_el_motor_no_reconoce"]["detalle"]
    out = [
        "| Morfema | Glosa | Dónde está declarado | Recurrencia | ¿Lo reconoce el scorer? |",
        "|---|---|---|---:|---|",
    ]
    for m in det:
        glosa = m.get("glosa") or "**sin glosar**"
        rec = m.get("recurrencia")
        rec = "—" if rec is None else str(rec)
        visto = "sí" if m.get("reconocido_por_el_scorer") else "**no**"
        out.append(
            f"| `{m['forma']}` | {glosa} | {m['donde']} | {rec} | {visto} |"
        )
    return out


def check(med: dict) -> int:
    """Los totales que la nota cita en prosa, recontados desde la medición."""
    inv = med["inventario"]
    detalle = inv["detalle"]
    problemas: list[str] = []

    if len(detalle) != inv["morfemas_en_el_motor"]:
        problemas.append(
            f"detalle tiene {len(detalle)} filas y el inventario dice "
            f"{inv['morfemas_en_el_motor']}"
        )

    con_cita = sum(1 for m in detalle if m.get("citas"))
    if con_cita != inv["con_cita_valida"]:
        problemas.append(
            f"con cita válida: {con_cita} contado / {inv['con_cita_valida']} declarado"
        )

    sin_proc = sorted(m["forma"] for m in detalle if m.get("deuda"))
    if sin_proc != sorted(inv["sin_procedencia"]):
        problemas.append("la lista de sin-procedencia no coincide")

    # (d): lo que el motor enseña y no tiene clave foránea.
    d = sorted(
        m["forma"] for m in detalle if m.get("deuda") and (m.get("ensenado_en") or [])
    )

    print(f"morfemas en el motor .......... {len(detalle)}")
    print(f"con clave foránea válida ...... {con_cita}")
    print(f"con deuda: sin-procedencia .... {len(sin_proc)}  ({' · '.join(sin_proc)})")
    print(f"(a) capa canon-simulación y enseñado .. "
          f"{med['patologias']['a_el_motor_ensena_lo_que_el_canon_no_declara']['n']}")
    print(f"(b) canon declara / scorer no ve ...... "
          f"{med['patologias']['b_el_canon_declara_lo_que_el_motor_no_reconoce']['n']}")
    print(f"(c) apoyo sólo en el andamio D11 ...... "
          f"{med['patologias']['c_apoyo_solo_en_el_andamio_d11']['n']}")
    print(f"(d) enseñado y sin clave foránea ...... {len(d)}  ({' · '.join(d)})")

    if problemas:
        for p in problemas:
            print(f"  ✗ {p}")
        return 1
    print("\n  ✓ la medición cuadra consigo misma")
    return 0


def main(argv=None) -> int:
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--medicion", default=MEDICION)
    ap.add_argument("--check", action="store_true",
                    help="recuenta los totales en vez de imprimir la tabla")
    args = ap.parse_args(argv)

    med = cargar(args.medicion)
    if args.check:
        return check(med)

    print("### Los 21 morfemas del motor\n")
    print("\n".join(tabla_del_motor(med)))
    print("\n### Lo que el canon de datos declara y el scorer no ve\n")
    print("\n".join(tabla_del_canon(med)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
