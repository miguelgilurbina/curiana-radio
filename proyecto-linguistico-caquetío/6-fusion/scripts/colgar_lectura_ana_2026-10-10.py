"""Segunda mitad de t10.3 (6-fusion/decisiones_tanda_2026-10-10.yaml): la
glosa hipotética de `-ana` se cuelga como LECTURA en los topónimos del canon
que la llevan.

Decisión literal de Miguel (2026-10-10): «Yo también voy por hipotética.» Es
la opción B de la D1 del borrador
6-fusion/issues-pendientes/cruce-toponimos-hermanas-2026-10-10.md, que dice:
«se cuelga como lectura en los cinco nombres y en `morfema-011`». La mitad de
`morfema-011` la aplicó aplicar_ana_hipotetica_2026-10-10.py.

Los cinco nombres de `morfema-011`, todos en el canon de topónimos:
- paraguaná (toponimo-018), curiana (toponimo-111) y chamuriana
  (toponimo-109): entradas completas con su lista `lecturas`;
- cujicana (toponimo-268) y jayana (toponimo-110): descartados dentro de un
  lote de DESCARTES, que lleva `lecturas` {forma: [lecturas]} (migrar_toponimos
  lo admite desde dp.2.08 de #222).

⚠️ La primera pasada (commit 70f9467) saltó Paraguaná creyendo que no tenía
entrada: la buscó con un patrón que no reconoció la «á». Está, y es el único
de los cinco con glosa de fuente («Rodeada del mar»), así que su lectura dice
la tensión en vez de taparla. Por eso el script es idempotente POR ENTRADA:
una segunda pasada salta las que ya tienen la lectura y añade las que falten.

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
    "paraguaná": "si la -aná de Paraguaná fuera este formante, se leería 'los "
                 "del mar', con X = para(gua) 'mar', que el canon ya despeja; "
                 "pero la fuente glosa «Rodeada del mar» y la -aná es tónica, "
                 "que #109 §3 da como el dato que separaría este sufijo del "
                 "-ana de Curiana",
    "curiana": "X = curi-/cori-, sin glosa acordada (avispa, lagartija, espina o "
               "cardón: ver las otras lecturas); y Curiana nombra a la vez el "
               "pueblo y la costa (Arcaya p. 169)",
    "chamuriana": "X = chamur-, sin glosa (el canon segmenta chamur- + -iana)",
    "cujicana": "X = cujic-, sin glosa",
    "jayana": "X = jay-, sin glosa",
}
VEREDICTO = {
    "paraguaná": "HIPOTÉTICA (Miguel, 2026-10-10: «Yo también voy por "
                 "hipotética.») y EN TENSIÓN con la glosa de fuente, que no "
                 "desplaza; no cambia el nivel. El 'lugar de' sigue retirado (#109)",
}
VEREDICTO_GENERAL = ("HIPOTÉTICA (Miguel, 2026-10-10: «Yo también voy por "
                     "hipotética.»); no cambia el nivel. El 'lugar de' sigue "
                     "retirado (#109)")


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
        f'{s} "veredicto": "{VEREDICTO.get(forma, VEREDICTO_GENERAL)}"}}'
    )


def rango_de_entrada(lineas, clave):
    """(inicio, fin) de la entrada de nivel 4 `"clave": {` hasta su `    },`."""
    ini = next(i for i, l in enumerate(lineas) if l.startswith(f'    "{clave}": {{'))
    fin = next(i for i in range(ini + 1, len(lineas)) if lineas[i].rstrip() in ("    },", "    }"))
    return ini, fin


def rango_de_lote(lineas, k):
    ini = max(i for i in range(k) if lineas[i].startswith('    "'))
    fin = next(i for i in range(k, len(lineas)) if lineas[i].rstrip() in ("    },", "    }"))
    return ini, fin


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    seco = "--dry-run" in (argv if argv is not None else sys.argv[1:])
    raw = io.open(MODULO, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    L = raw.replace("\r\n", "\n").split("\n")
    cambios = 0

    # 1-3. entradas completas: primera lectura de su lista
    for clave in ("paraguaná", "curiana", "chamuriana"):
        ini, fin = rango_de_entrada(L, clave)
        if any(MARCA in L[i] for i in range(ini, fin)):
            print(f"  = {clave}: ya tiene la lectura")
            continue
        k = next((i for i in range(ini, fin) if L[i].strip() == '"lecturas": ['), None)
        if k is None:
            print(f"✗ {clave}: sin lista `lecturas` en su entrada; no se escribe")
            return 1
        L.insert(k + 1, lectura(clave, 12) + ",")
        cambios += 1
        print(f"  + {clave}: lectura hipotética, primera de su lista")

    # 4. cujicana: lote con `lecturas` {forma: [...]}
    k_ids = next(i for i, l in enumerate(L) if l.startswith('        "ids": {') and '"cujicana": "toponimo-268"' in l)
    ini, fin = rango_de_lote(L, k_ids)
    k = next((i for i in range(ini, fin) if L[i].startswith('        "lecturas": {')), None)
    if any(MARCA in L[i] and "cujic-" in L[i] for i in range(ini, fin)):
        print("  = cujicana: ya tiene la lectura")
    elif k is None:
        print("✗ cujicana: el lote no tiene `lecturas`; no se escribe")
        return 1
    else:
        L[k] = L[k].replace('        "lecturas": {', '        "lecturas": {"cujicana": [\n'
                            + lectura("cujicana", 12) + '], ', 1)
        cambios += 1
        print("  + cujicana: lectura hipotética en el `lecturas` de su lote")

    # 5. jayana: lote que no tenía `lecturas`; se añade la clave
    k_fv = next(i for i, l in enumerate(L) if l.startswith('        "formas_vivas": {') and '"jayana"' in l)
    ini, fin = rango_de_lote(L, k_fv)
    if any(MARCA in L[i] and "jay-" in L[i] for i in range(ini, fin)):
        print("  = jayana: ya tiene la lectura")
    elif any(L[i].startswith('        "lecturas": {') for i in range(ini, fin)):
        print("✗ jayana: el lote ya tiene `lecturas` sin la de -ana; revisar a mano")
        return 1
    else:
        L.insert(k_fv, '        "lecturas": {"jayana": [\n' + lectura("jayana", 12) + ']},')
        cambios += 1
        print("  + jayana: clave `lecturas` nueva en su lote, con la lectura hipotética")

    if not cambios:
        print("ya aplicado; nada que hacer")
        return 0
    nuevo = "\n".join(L)
    ast.parse(nuevo)  # que siga siendo Python válido
    if seco:
        print(f"(--dry-run: {cambios} cambio(s); no se escribió nada; el módulo resultante parsea)")
        return 0
    if crlf:
        nuevo = nuevo.replace("\n", "\r\n")
    io.open(MODULO, "w", encoding="utf-8", newline="").write(nuevo)
    print(f"✓ escrito {os.path.relpath(MODULO, R)} ({cambios} cambio(s)); ahora: python curiana_sim/migrar_toponimos.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
