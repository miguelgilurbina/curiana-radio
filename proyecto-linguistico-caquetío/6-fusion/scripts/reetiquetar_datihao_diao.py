#!/usr/bin/env python3
"""`datihao` pasa a taíno; `diao` y `boratio` reciben su cita primaria.

DECISIÓN (Miguel, 2026-09-22, db.2 de `6-fusion/decisiones_base_2026-09-22.yaml`):
«vale, dale con el punto 2» — el punto 2 era «`datihao` a taíno-atestiguado, con
`diao` como la voz caquetía».

QUÉ SE APLICA
  · `datihao`: `fuente` caquetío-atestiguado → `taíno` (la etiqueta del lexicón
    para la voz taína atestiguada; «taíno-atestiguado» no es un valor de
    FUENTES_CANONICAS). Huella al principio de `notas`. NO se toca `sig` ni la
    forma: la glosa que hoy tiene es la del EDITOR de 1855, y la de Oviedo en el
    pasaje es otra — se escribe, y cambiarla es otra decisión.
  · `diao` y `boratio`: la cita primaria de Oviedo t. II al final de `notas`, sin
    mover etiqueta ni glosa.
  · `3-mundo/corpus/creencia.yaml` creencia-001: la `referencia` apunta a la
    fuente primaria de `boratio`, no sólo al glosario del editor vía Jahn.

QUÉ SE MIDIÓ (campaña del taíno 2, T6, PR #195, `6-fusion/taino2_oviedo_venezuela.yaml`,
y verificado por el escriba sobre el PDF con pymupdf):
  · `datihao` en el CUERPO de los cuatro tomos: 1 (t. I p. 473, San Juan). La
    «(Lengua de Venezuela)» es del glosario del editor, t. IV impresa 598.
  · `diao`: t. II impresa 299, «en algunas partes desta gobernación de Venezuela
    el señor principal… llámanle diao».
  · `boratio`: t. II pp. 298-299, con una t.

QUÉ NO SE APLICA (saltado, y llevado a Miguel): `waitiao` (`guaitiao`) tiene el
mismo problema — 0 en Oviedo t. II y en la Apologética, sólo secundarias —; la
`lectura` de `gatiao` en ecologia.yaml que usa `datihao` como ejemplo; la glosa.

ES CORTE DE SERIE: `datihao` sale de la muestra caquetía del prompt. Va en la
tanda de la base, que se mide entera una vez.

Uso:  python 6-fusion/scripts/reetiquetar_datihao_diao.py [--dry-run]
"""
import argparse
import io
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LEX = os.path.join(R, "curiana_sim", "curiana_lexicon.py")
CREENCIA = os.path.join(R, "3-mundo", "corpus", "creencia.yaml")
MARCA = "Decisión de Miguel 2026-09-22 (db.2"

HUELLA_DATIHAO = (
    "Decisión de Miguel 2026-09-22 (db.2, «dale con el punto 2»): re-etiquetada de "
    "`caquetío-atestiguado` a `taíno`. En el CUERPO de los cuatro tomos de Oviedo y Valdés "
    "(ed. Amador de los Ríos, 1851-1855) aparece UNA vez: t. I p. 473, en San Juan, en boca "
    "de Agüeybana — «á mi dalihao (que quiere deçir mi señor, ó el que, como yo, se nombra)» "
    "[la capa de texto da `dalihao`; la l/t no está verificada en imagen]. La marca «(Lengua de "
    "Venezuela)» es del GLOSARIO DEL EDITOR (t. IV impresa 598), y de ahí sale también esta `sig` "
    "(«el que presta su nombre al esclavo»): no es la glosa de Oviedo, que dice «mi señor, ó el "
    "que, como yo, se nombra». Oliver, Jahn y Arcaya heredaron la etiqueta del editor. Campaña del "
    "taíno 2, T6 (#195). Etiqueta anterior: `caquetío-atestiguado`"
)
CITA_DIAO = (
    " · Cita primaria (campaña del taíno 2, T6, 2026-09-22; db.2): Oviedo y Valdés, Historia "
    "general, t. II (1852) impresa 299, Libro XXV: «en algunas partes desta gobernación de "
    "Venezuela el señor principal, que tiene muchos indios y le son subjetos otros caciques, "
    "llámanle diao», con sus exequias, «otra manera de obsequias de la que se dixo de suso». "
    "Alcance que Oviedo declara: la gobernación de Venezuela, no sólo Coro (regla 4). No cuelga "
    "de `datihao` (taíno): otra raíz en Oliver, /d-ia(o)/"
)
CITA_BORATIO = (
    " · Cita primaria (campaña del taíno 2, T6, 2026-09-22; db.2): Oviedo y Valdés, Historia "
    "general, t. II (1852) pp. 298-299, `boratio` con UNA t: «afirman los boratios que le ven y "
    "hablan muchas veces [al diablo]… Estos boratios son como sacerdotes suyos», de los indios "
    "de la gobernación de Venezuela. La doble t de `borattio` es de la cadena Jahn/Arcaya. El "
    "glosario del editor (t. IV impresa 595) la da como «(Lengua de Venezuela)»"
)
REF_VIEJA = 'referencia: "Oviedo y Valdés, Historia general, apéndice t. IV (en Jahn 1927:213 n.29); Arcaya 1920:116"'
REF_NUEVA = ('referencia: "Oviedo y Valdés, Historia general, t. II (1852) pp. 298-299 (el cuerpo: '
             '`boratio`, con una t, de los indios de la gobernación de Venezuela) y glosario del editor '
             't. IV p. 595; Jahn 1927:213 n.29; Arcaya 1920:116"')


def _linea_de(texto, clave):
    """La línea de la entrada `clave` DENTRO de VOCABULARIO_BASE (no en FUERA_DEL_HABLA)."""
    ini = texto.index("VOCABULARIO_BASE: dict[str, dict] = {")
    fin = texto.index("REGLAS_ASPECTO", ini)
    region = texto[ini:fin]
    ms = list(re.finditer(rf'^    "{re.escape(clave)}":\s*\{{.*\}},\s*$', region, re.M))
    assert len(ms) == 1, (clave, len(ms))
    return ini + ms[0].start(), ini + ms[0].end()


def _cambiar_notas(linea, huella_delante=None, cola=None):
    m = re.search(r'"notas":\s*"((?:[^"\\]|\\.)*)"', linea)
    assert m, linea[:80]
    notas = m.group(1)
    nuevas = (huella_delante + " · " if huella_delante else "") + notas + (cola or "")
    nuevas = nuevas.replace('"', "'")
    return linea[:m.start(1)] + nuevas + linea[m.end(1):]


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    lex = io.open(LEX, encoding="utf-8").read()
    if MARCA in lex:
        print("ya aplicado; nada que hacer")
        return 0

    cambios = []
    # datihao: fuente + huella
    a, b = _linea_de(lex, "datihao")
    linea = lex[a:b]
    assert '"fuente": "caquetío-atestiguado"' in linea, linea[:120]
    nueva = linea.replace('"fuente": "caquetío-atestiguado"', '"fuente": "taíno"', 1)
    nueva = _cambiar_notas(nueva, huella_delante=HUELLA_DATIHAO)
    cambios.append(("datihao", a, b, nueva, "fuente caquetío-atestiguado → taíno; huella en notas"))
    # diao, boratio: cita al final de notas
    for clave, cita in (("diao", CITA_DIAO), ("boratio", CITA_BORATIO)):
        a, b = _linea_de(lex, clave)
        cambios.append((clave, a, b, _cambiar_notas(lex[a:b], cola=cita), "cita primaria al final de notas"))

    cre = io.open(CREENCIA, encoding="utf-8").read()
    assert cre.count(REF_VIEJA) == 1, cre.count(REF_VIEJA)

    for clave, _, _, _, que in cambios:
        print(f"  {clave:8} {que}")
    print("  creencia-001  referencia → fuente primaria de `boratio`")
    print("  SALTADO: waitiao (mismo caso que datihao, sin decisión) · lectura de `gatiao` · la glosa de datihao")
    if args.dry_run:
        print("\n--dry-run: no se escribe nada")
        return 0

    for _, a, b, nueva, _ in sorted(cambios, key=lambda c: -c[1]):
        lex = lex[:a] + nueva + lex[b:]
    io.open(LEX, "w", encoding="utf-8", newline="\n").write(lex)
    io.open(CREENCIA, "w", encoding="utf-8", newline="\n").write(cre.replace(REF_VIEJA, REF_NUEVA))
    print("\nescrito")
    return 0


if __name__ == "__main__":
    sys.exit(main())
