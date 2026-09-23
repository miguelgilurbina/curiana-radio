#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La cronología dabajuroide contra la ventana simulada (s. XIV-XV), medida.

Campaña cc.5 (2026-09-23). Lee:
  - 6-fusion/guaiqueries_manaure_dabajuroide_2026-09-23.yaml §pregunta_3.fases
    (los complejos con su esquema, su obra y su página: Oliver 1989, Casale
    2024, Arvelo y López 2004 vía Urbina 2007);
  - 6-fusion/tabla15_c14_oliver.yaml (las 23 dataciones de la Tabla 15 de
    Oliver, recalibradas por él).

y dice, sin cifras escritas a mano (regla 1):
  1. qué complejos tocan la ventana, con qué solape SEGURO (el tramo que el
     complejo ocupa en cualquier lectura de sus «a/b») y POSIBLE (el que ocupa
     en la lectura más ancha);
  2. por cuartos de siglo, qué complejos de la costa de Falcón, Paraguaná y las
     islas conviven según cada esquema — la pregunta de #203 M8 D1;
  3. qué dataciones de la Tabla 15 tocan la ventana, por región. La región sale
     del NOMBRE del sitio en la tabla (declarado aquí, no inventado): lo que
     dice «Paraguaná» es Paraguaná; lo que dice Aruba o Curazao, las islas; el
     resto, tierra firme de Falcón.

    python 6-fusion/scripts/medir_cronologia_dabajuroide.py
    python 6-fusion/scripts/medir_cronologia_dabajuroide.py --check   # claves y rangos
"""
import os
import sys

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROPUESTA = os.path.join(RAIZ, "6-fusion", "guaiqueries_manaure_dabajuroide_2026-09-23.yaml")
TABLA15 = os.path.join(RAIZ, "6-fusion", "tabla15_c14_oliver.yaml")
BIBLIO = os.path.join(RAIZ, "4-fuentes", "bibliografia.yaml")

# Las regiones que cuentan para la pregunta «qué había en las manos de los
# agentes»: la costa de Falcón, Paraguaná y las ABC. Una fase entra si su
# `region` nombra alguna de éstas.
REGIONES_DE_LA_KAKETIANA = ("Falcón", "Paraguaná", "ABC", "Aruba")


def _forzar_utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def rango(valor):
    """«a/b» se guarda como [a, b]: devuelve (el más temprano, el más tardío)."""
    if isinstance(valor, list):
        return min(valor), max(valor)
    return valor, valor


def tramos(fase):
    """(seguro_desde, seguro_hasta), (posible_desde, posible_hasta)."""
    d_min, d_max = rango(fase["desde"])
    h_min, h_max = rango(fase["hasta"])
    return (d_max, h_min), (d_min, h_max)


def solape(a, b, ventana):
    ini, fin = max(a, ventana[0]), min(b, ventana[1])
    return max(0, fin - ini)


def region_de_sitio(sitio):
    if "Paraguan" in sitio:
        return "Paraguaná"
    if "Aruba" in sitio or "Curazao" in sitio:
        return "islas ABC"
    return "tierra firme de Falcón"


def check(datos, biblio):
    ids = {o["id"] for o in biblio["obras"]}
    problemas = []
    for f in datos["pregunta_3"]["fases"]:
        if f["obra"] not in ids:
            problemas.append(f"obra sin clave: {f['obra']} ({f['complejo']})")
        (s0, s1), (p0, p1) = tramos(f)
        if p0 > p1:
            problemas.append(f"rango invertido: {f['complejo']}")
    return problemas


def main():
    _forzar_utf8()
    datos = _cargar(PROPUESTA)
    tabla = _cargar(TABLA15)
    biblio = _cargar(BIBLIO)
    ventana = tuple(datos["meta"]["ventana_simulada"])
    fases = datos["pregunta_3"]["fases"]

    problemas = check(datos, biblio)
    if "--check" in sys.argv:
        for p in problemas:
            print("✗", p)
        print("✓ claves y rangos en orden" if not problemas else f"{len(problemas)} problemas")
        return 1 if problemas else 0

    print(f"Ventana simulada: {ventana[0]}-{ventana[1]} d.C.\n")

    # 1. Cada complejo contra la ventana
    print("1. LOS COMPLEJOS CONTRA LA VENTANA (años de solape)")
    print(f"   {'esquema':18} {'complejo':38} {'seguro':>7} {'posible':>8}  región · obra p.")
    for f in fases:
        (s0, s1), (p0, p1) = tramos(f)
        seguro = solape(s0, s1, ventana) if s0 <= s1 else 0
        posible = solape(p0, p1, ventana)
        if posible == 0:
            continue
        print(f"   {f['esquema']:18} {str(f['complejo'])[:38]:38} {seguro:>7} {posible:>8}  "
              f"{f['region']} · {f['obra']} p. {f['pagina']}")
    fuera = [f["complejo"] for f in fases if solape(*tramos(f)[1], ventana) == 0]
    print(f"   fuera de la ventana: {', '.join(map(str, fuera))}\n")

    # 2. Por cuartos de siglo, en la Kaketiana
    print("2. QUÉ CONVIVE EN LA KAKETIANA, POR CUARTOS DE SIGLO (lectura posible)")
    kake = [f for f in fases if any(r in f["region"] for r in REGIONES_DE_LA_KAKETIANA)]
    esquemas = sorted({f["esquema"] for f in kake})
    for ini in range(ventana[0], ventana[1], 25):
        fin = ini + 25
        partes = []
        for e in esquemas:
            vivos = [str(f["complejo"]) for f in kake if f["esquema"] == e
                     and solape(*tramos(f)[1], (ini, fin)) > 0]
            partes.append(f"{e}: {' + '.join(vivos) if vivos else '—'}")
        print(f"   {ini}-{fin}  " + "  |  ".join(partes))
    print()

    # 3. La Tabla 15
    print("3. LAS DATACIONES DE LA TABLA 15 QUE TOCAN LA VENTANA (cal. 1 sigma, Oliver)")
    por_region = {}
    for d in tabla["dataciones"]:
        c0, cc, c1 = d["cal"]
        if solape(c0, c1, ventana) == 0:
            continue
        reg = region_de_sitio(d["sitio"])
        central_dentro = ventana[0] <= cc <= ventana[1]
        por_region.setdefault(reg, []).append((d, central_dentro))
    total = sum(len(v) for v in por_region.values())
    print(f"   {total} de {len(tabla['dataciones'])} tocan la ventana con su rango")
    for reg in sorted(por_region):
        filas = por_region[reg]
        n_central = sum(1 for _, c in filas if c)
        print(f"   · {reg}: {len(filas)} (con la fecha central dentro: {n_central})")
        for d, c in filas:
            c0, cc, c1 = d["cal"]
            print(f"       {d['lab']:10} {d['sitio']:26} cal. {c0}-[{cc}]-{c1}"
                  f"{'' if c else '  (central fuera)'}")
    if problemas:
        print("\n⚠️ " + "; ".join(problemas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
