"""Segunda mitad de t10.3 (6-fusion/decisiones_tanda_2026-10-10.yaml): la
glosa hipotética de `-ana` se cuelga como LECTURA en los topónimos del canon
que la llevan.

Decisión literal de Miguel (2026-10-10): «Yo también voy por hipotética.» Es
la opción B de la D1 del borrador
6-fusion/issues-pendientes/cruce-toponimos-hermanas-2026-10-10.md, que dice:
«se cuelga como lectura en los cinco nombres y en `morfema-011`». La mitad de
`morfema-011` la aplicó aplicar_ana_hipotetica_2026-10-10.py.

Los cinco nombres de `morfema-011` son Paraguaná, Curiana, Chamuriana,
Cujicana y Jayana. En el canon de topónimos están los cuatro últimos:
- curiana (toponimo-111) y chamuriana (toponimo-109): entradas completas con
  su lista `lecturas`;
- cujicana (toponimo-268) y jayana (toponimo-110): descartados dentro de un
  lote de DESCARTES, que lleva `lecturas` {forma: [lecturas]} (migrar_toponimos
  lo admite desde dp.2.08 de #222).
**Paraguaná no tiene entrada en el canon de topónimos**: se salta y se le lleva
a Miguel (fusionar-propuesta §0: lo que nadie previó no se resuelve de paso).

No cambia el nivel, la segmentación ni la razón de ninguna entrada: añade una
lectura `tipo: hipotesis`, `eje: significado`.

Uso:
    python 6-fusion/scripts/colgar_lectura_ana_2026-10-10.py --dry-run
    python 6-fusion/scripts/colgar_lectura_ana_2026-10-10.py
    python curiana_sim/migrar_toponimos.py
"""
import ast
import io
import os
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULO = os.path.join(R, "curiana_sim", "lexicon_toponimos.py")
MARCA = "glosa HIPOTÉTICA de morfema-011 (t10.3)"

RAIZ = {
    "curiana": "X = curi-/cori-, sin glosa acordada (avispa, lagartija, espina o "
               "cardón: ver las otras lecturas); y Curiana nombra a la vez el "
               "pueblo y la costa (Arcaya p. 169)",
    "chamuriana": "X = chamur-, sin glosa (el canon segmenta chamur- + -iana)",
    "cujicana": "X = cujic-, sin glosa",
    "jayana": "X = jay-, sin glosa",
}


def lectura(forma, sangria):
    s = " " * sangria
    return (
        f'{s}{{"tipo": "hipotesis",\n'
        f'{s} "lectura": "-ana \'los de X, la gente de X\' ({MARCA}): el nombre '
        f'sería el de una gente pasado al lugar, como Guayana; {RAIZ[forma]}",\n'
        f'{s} "quien": "cruce de topónimos con las hermanas (2026-10-10), adoptada '
        f'como hipotética por Miguel",\n'
        f'{s} "fecha": "2026-10-10", "eje": "significado",\n'
        f'{s} "apoyo": "lokono Ebeso-ana, el linaje con el nombre de la antepasada '
        f'(Brett 1880 pp. 178-179); kalinago isla + -na \'los habitantes\' (Breton '
        f'1665 p. 416, falta verlo en imagen); 6-fusion/cruce_toponimos_hermanas_'
        f'2026-10-10.yaml §ana",\n'
        f'{s} "procedencia": dict(obra="brett-1880", pagina="178-179"),\n'
        f'{s} "veredicto": "HIPOTÉTICA (Miguel, 2026-10-10: «Yo también voy por '
        f'hipotética.»); no cambia el nivel. El \'lugar de\' sigue retirado (#109)"}}'
    )


def rango_de_entrada(lineas, clave):
    """(inicio, fin) de la entrada de nivel 4 `"clave": {` hasta su `    },`."""
    ini = next(i for i, l in enumerate(lineas) if l.startswith(f'    "{clave}": {{'))
    fin = next(i for i in range(ini + 1, len(lineas)) if lineas[i].rstrip() in ("    },", "    }"))
    return ini, fin


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    seco = "--dry-run" in (argv if argv is not None else sys.argv[1:])
    raw = io.open(MODULO, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    if MARCA in t:
        print("ya aplicado; nada que hacer")
        return 0
    L = t.split("\n")

    # 1-2. curiana y chamuriana: primera lectura de su lista
    for clave in ("curiana", "chamuriana"):
        ini, fin = rango_de_entrada(L, clave)
        k = next((i for i in range(ini, fin) if L[i].strip() == '"lecturas": ['), None)
        if k is None:
            print(f"✗ {clave}: sin lista `lecturas` en su entrada; no se escribe")
            return 1
        L.insert(k + 1, lectura(clave, 12) + ",")
        print(f"  + {clave}: lectura hipotética, primera de su lista")

    # 3. cujicana: lote con `lecturas` {forma: [...]} de una línea
    lote_cuj = next(i for i, l in enumerate(L) if l.startswith('        "ids": {') and '"cujicana": "toponimo-268"' in l)
    ini = max(i for i in range(lote_cuj) if L[i].startswith('    "'))
    fin = next(i for i in range(lote_cuj, len(L)) if L[i].rstrip() in ("    },", "    }"))
    k = next((i for i in range(ini, fin) if L[i].startswith('        "lecturas": {')), None)
    if k is None or '"cujicana"' in L[k]:
        print("✗ cujicana: el lote no tiene `lecturas` o ya la tiene; no se escribe")
        return 1
    L[k] = L[k].replace('        "lecturas": {', '        "lecturas": {"cujicana": [\n'
                        + lectura("cujicana", 12) + '], ', 1)
    print("  + cujicana: lectura hipotética en el `lecturas` de su lote")

    # 4. jayana: lote SIN `lecturas`; se añade la clave
    lote_jay = next(i for i, l in enumerate(L) if l.startswith('        "formas_vivas": {') and '"jayana"' in l)
    ini = max(i for i in range(lote_jay) if L[i].startswith('    "'))
    fin = next(i for i in range(lote_jay, len(L)) if L[i].rstrip() in ("    },", "    }"))
    if any(L[i].startswith('        "lecturas": {') for i in range(ini, fin)):
        print("✗ jayana: el lote ya tiene `lecturas`; revisar a mano")
        return 1
    L.insert(lote_jay, '        "lecturas": {"jayana": [\n' + lectura("jayana", 12) + ']},')
    print("  + jayana: clave `lecturas` nueva en su lote, con la lectura hipotética")

    print("  · paraguaná: SALTADO — no tiene entrada en el canon de topónimos (llevarlo a Miguel)")
    nuevo = "\n".join(L)
    ast.parse(nuevo)  # que siga siendo Python válido
    if seco:
        print("(--dry-run: no se escribió nada; el módulo resultante parsea)")
        return 0
    if crlf:
        nuevo = nuevo.replace("\n", "\r\n")
    io.open(MODULO, "w", encoding="utf-8", newline="").write(nuevo)
    print(f"✓ escrito {os.path.relpath(MODULO, R)}; ahora: python curiana_sim/migrar_toponimos.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
