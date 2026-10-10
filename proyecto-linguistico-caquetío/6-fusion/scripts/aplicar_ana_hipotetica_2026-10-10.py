"""Aplica t10.3 (6-fusion/decisiones_tanda_2026-10-10.yaml): la glosa candidata
de `-ana`, 'los de X, la gente de X', con capa HIPOTÉTICA.

Decisión literal de Miguel (2026-10-10), sobre la D1 del borrador
6-fusion/issues-pendientes/cruce-toponimos-hermanas-2026-10-10.md:

    «Yo también voy por hipotética.»

Qué hace: edita la entrada "-ana" de FORMATIVOS_SIN_GLOSA en
curiana_sim/lexicon_toponimos.py —la fuente de 2-lengua/morfemas.yaml, que es
GENERADO por curiana_sim/migrar_toponimos.py— y nada más:

- añade `glosa_hipotetica`, `capa_de_la_glosa`, `apoyo_comparado` y `decision`;
- corrige la frase de `nota` que había quedado vieja («El motor conserva -ana
  'lugar de'…»): desde d21.6 (2026-09-21) el prompt la enseña SIN glosa.

Qué NO hace (regla 5 y el alcance de lo autorizado): no mueve `-ana` a
MORFEMAS_DESPEJADOS (sigue sin glosa de fuente caquetía), no toca el motor
(curiana_lexicon.py y las plantillas), ni el nivel o la segmentación de ningún
topónimo.

Medido antes de escribir: regenerar con migrar_toponimos.py daba un árbol
idéntico (git status vacío en 2-lengua/). Después, el único cambio en
2-lengua/morfemas.yaml tiene que ser morfema-011.

Uso:
    python 6-fusion/scripts/aplicar_ana_hipotetica_2026-10-10.py --dry-run
    python 6-fusion/scripts/aplicar_ana_hipotetica_2026-10-10.py
    python curiana_sim/migrar_toponimos.py
"""
import io
import os
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODULO = os.path.join(R, "curiana_sim", "lexicon_toponimos.py")
MARCA = "t10.3 (2026-10-10)"

VIEJA = (
    '                "(guariana, maracapana). El motor conserva -ana \'lugar de\' "\n'
    '                "como convención de la simulación (canon-simulación), no "\n'
    '                "como dato.",\n'
    '    },\n'
)
NUEVA = (
    '                "(guariana, maracapana). Desde d21.6 (2026-09-21) el motor "\n'
    '                "la enseña SIN glosa, como -ubana y -uru.",\n'
    '        # t10.3 (2026-10-10), decisión de Miguel: «Yo también voy por\n'
    '        # hipotética.» La glosa de abajo es CANDIDATA y comparada; la forma\n'
    '        # sigue sin glosa de fuente caquetía (por eso no pasa a\n'
    '        # MORFEMAS_DESPEJADOS). Ver 6-fusion/decisiones_tanda_2026-10-10.yaml.\n'
    '        "glosa_hipotetica": "los de X, la gente de X (colectivo de gente; en "\n'
    '                            "el topónimo, el nombre de una gente pasado al "\n'
    '                            "lugar, como Guayana)",\n'
    '        "capa_de_la_glosa": "hipotetico",\n'
    '        "apoyo_comparado": [\n'
    '            "lokono (hermana): el linaje matrilineal toma el nombre de la "\n'
    '            "antepasada, Ebesō-tu → Ebeso-ana, Demare-du → Demaré-na "\n'
    '            "(Brett 1880, pp. 178-179); el sufijo se separa",\n'
    '            "kalinago (hermana, sustrato iñeri): gentilicio plural isla + "\n'
    '            "-na, Ouâitoucoubouli-na \'los de Dominica\' (Breton 1665 p. 416 "\n'
    '            "y Grammaire 1667, hoja G iij); leído en la capa de texto, "\n'
    '            "falta verlo en imagen",\n'
    '            "Guayana: el país toma el nombre de los Guayana, un pueblo de "\n'
    '            "lengua caribe (Goeje 1939 p. 5); la «tierra de muchas aguas» "\n'
    '            "no tiene fuente en el repo",\n'
    '        ],\n'
    '        "no_la_apoyan": [\n'
    '            "achagua (prima): el «locativo -ana» de la transcripción es el "\n'
    '            "-na relacional de numa \'boca\' (Numana \'boca de Casanare\')",\n'
    '            "taíno: su único caso, Maguana \'cuasi la Vega menor\' (Las "\n'
    '            "Casas, Apologética cap. VII p. 19), es otra función",\n'
    '        ],\n'
    '        "decision": "t10.3 (2026-10-10), opción B de la D1 de "\n'
    '                    "6-fusion/issues-pendientes/cruce-toponimos-hermanas-"\n'
    '                    "2026-10-10.md; propuesta en "\n'
    '                    "6-fusion/cruce_toponimos_hermanas_2026-10-10.yaml §ana",\n'
    '    },\n'
)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    seco = "--dry-run" in (argv if argv is not None else sys.argv[1:])
    raw = io.open(MODULO, encoding="utf-8", newline="").read()
    crlf = "\r\n" in raw
    t = raw.replace("\r\n", "\n")
    if MARCA in t:
        print("ya aplicado; nada que hacer")
        return 0
    n = t.count(VIEJA)
    if n != 1:
        print(f"✗ la entrada '-ana' no tiene la forma esperada ({n} coincidencias): no se escribe")
        return 1
    nuevo = t.replace(VIEJA, NUEVA)
    print("-ana (FORMATIVOS_SIN_GLOSA):")
    print("  + glosa_hipotetica: 'los de X, la gente de X'  (capa: hipotetico)")
    print("  + apoyo_comparado: lokono (Brett 1880), kalinago (Breton 1665), Guayana (Goeje 1939)")
    print("  + no_la_apoyan: achagua (prima, -na relacional), taíno (Maguana)")
    print("  ~ nota: el motor la enseña SIN glosa desde d21.6 (corrige la frase vieja)")
    if seco:
        print("(--dry-run: no se escribió nada)")
        return 0
    if crlf:
        nuevo = nuevo.replace("\n", "\r\n")
    io.open(MODULO, "w", encoding="utf-8", newline="").write(nuevo)
    print(f"✓ escrito {os.path.relpath(MODULO, R)}; ahora: python curiana_sim/migrar_toponimos.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
