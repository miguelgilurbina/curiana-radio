# -*- coding: utf-8 -*-
"""
CURIANA — tanda de decisiones del 2026-08-30/31: F1 · D5b · D9 · #101
=====================================================================

Miguel resolvió cinco decisiones una por una (registro completo, con la
evidencia de cada una: `6-fusion/decisiones_tanda_2026-08-30.yaml`). Este
script aplica al lexicón las que tocan entradas concretas. Como
`aplicar_d10.py`: idempotente, con --dry-run, y solo `curiana_lexicon.py`.

    python aplicar_tanda_08_30.py --dry-run   # informe, no escribe
    python aplicar_tanda_08_30.py             # aplica

LO QUE APLICA
-------------
F1  · `kama` baja a hipotético (ruta de rehabilitación: fila 'tapir' de la
      Tabla A-7) · `wabarsure` pasa a reconstruido (compuesto de trabajo
      wa- + barsure) · `koke` gana la cita de Zavala #89 vía forma_fuente
      «coques».
D5b · `buko` absorbe a `buco` (bajo D5a el lema fonémico sobrevive y la
      grafía de fuente va a `forma_fuente`), con la cita de Ballesteros 1550
      como reina · `barici`/`bariki` quedan con referencia cruzada, sin
      fusionar · `coro`/`koro` no se tocan.
#101· `bara` pasa a atestiguado 'palo, árbol' (Zavala #29 + Esteves + van
      Buurt + la prueba interna de `barabara`); la lectura 'río' queda
      descartada por D7, registrada.
D9  · `bana` 'hígado' queda como HOMÓNIMO declarado del morfema -bana
      'cerro, sitio alto' (atestiguado). De paso se sanea un bug latente:
      la entrada traía DOS claves "notas" (la segunda pisaba a la primera).

LO QUE NO APLICA (y por qué)
----------------------------
· La migración masiva de lemas de D5a/D5c (fonémico + forma_fuente en toda
  la familia caquetía, gu→w en ~44 lemas) es la FASE 2: obra grande que
  toca exporters, wiki y tests, y va en su propia sesión antes del run 1.
· Las correcciones de documentación (CLAUDE.md, morfologia.md, la nota de
  Zavala) van en el mismo commit pero a mano: son prosa, no campos.
· `coques` vive en `lexicon_zavala.py`, que es GENERADO: no se toca a mano.
  Al regenerarlo hay que fusionar/excluir el #89 — queda anotado en la
  entrada de `koke` y en el YAML de decisiones.
"""

import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LEXICON_FILE = os.path.join(AQUI, "curiana_lexicon.py")

Z = "Zavala Reyes 2015"

# ══════════════════════════════════════════════════════════════════════
# Ediciones de campos (mismo mecanismo que aplicar_d10)
# ══════════════════════════════════════════════════════════════════════
CAMPOS = {
    # ── F1 ──
    "kama": {
        "fuente": "caquetío-hipotético",
        "notas": "Decisión F1 (tanda 2026-08-30) — DEGRADADA: SIN_RASTRO real en las cuatro minerías (auditar_82); el lokono usa otra raíz (firobero). Candidata a reconstruido vía cognado proto-arahuaco *kema. RUTA CORREGIDA 2026-08-31: el Swadesh-100 de Oliver NO trae tapir (medido al minar la serie A-1..A-7); candidatos reales: el vocabulario paraujano completo de Wilbert (Tabla A-1), las voces de fauna de van Buurt, o la comparativa externa (Payne). Ver 6-fusion/tabla_a1_a7_swadesh.yaml",
    },
    "wabarsure": {
        "fuente": "caquetío-reconstruido",
        "notas": "Decisión F1 (tanda 2026-08-30) — compuesto de trabajo del proyecto: wa- (posesivo 1pl, nuestro) + barsure (alma, ATESTIGUADO: Angulo Molina; %s). Nunca buscarla en fuentes como palabra simple: no es palabra perdida sino derivación interna. De paso sale del limbo fuente=caquetío sin capa" % Z,
    },
    "koke": {
        "sig": "hormiga roja; bachaco, hormiga grande (Atta spp.)",
        "forma_fuente": "coques",
        "notas": "Decisión F1/D5b (tanda 2026-08-30) — FUSIONADA con la grafía de fuente «coques»: %s #89 (HB): «Hormiga roja». No estaba SIN_RASTRO: las minerías buscaron la grafía k y no vieron la c (el mismo error de grafía que ocultó a Hurehurebo en Castellanos). Apoyo extra: cognados_oliver.py trae CQ coque, hormiga roja. La -s de coques es plural castellano de Zavala (cf. quibacoas). FUSIÓN CERRADA 2026-08-31: el miner casa ahora por forma_fuente y el #89 queda como YA_EN_LEXICON — coques dejó de ser entrada aparte del generado" % Z,
    },
    # ── D5b: el par que NO se fusiona, con referencia cruzada ──
    "barici": {
        "notas": "%s, glosario #34 (HB): «Agua turbia». Referencia cruzada D5b (tanda 2026-08-30): NO fusionar con bariki (#35 «Barique», arcilla roja) — son entradas distintas de la fuente que solo colisionan al normalizar c/k. Posible raíz común bar- (agua turbia ~ tierra colorada): pregunta etimológica abierta, no duplicado" % Z,
    },
    "bariki": {
        "forma_fuente": "Barique",
        "notas": "%s, glosario #35 «Barique» (AM+HB): «Arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija»; Arcaya la cita también en la Relación de Barquisimeto 1579. Referencia cruzada D5b (tanda 2026-08-30): NO fusionar con barici (#34, agua turbia) — entradas distintas de la fuente" % Z,
    },
    # ── D5b: el superviviente de la fusión buco/buko ──
    "buko": {
        "sig": "presa de agua, represa, canal de riego",
        "forma_fuente": "buco",
        "notas": "Decisión D5b (tanda 2026-08-30) — FUSIONADA con buco: bajo D5a el lema fonémico sobrevive y la grafía de fuente queda aquí. CITA REINA: Ballesteros, Obispo de Coro, 1550: «Los indios antiguamente, una legua del río arriba tenían hecha una presa que ellos llaman buco» (vía Arcaya 1920 p.170, que declara citar de una copia — segunda mano; ver 4-fuentes/ballesteros-1550.md). Además %s #46 «Buco» (AM+CGB): «Chorro de agua, presa de agua». La reserva de Alvarado 1921 p.34 (sugería origen romance, localizaba en Lara) queda superada por la atestación de 1550 en el propio río de Coro; el topónimo vivo El Buco corrobora" % Z,
    },
    # ── #101 ──
    "bara": {
        "sig": "palo, árbol",
        "fuente": "caquetío-atestiguado",
        "forma_fuente": "Bara",
        "notas": "Decisión #101 (tanda 2026-08-30) — GLOSA CORREGIDA a la de las fuentes: %s #29 (E): «Palo, árbol», con Esteves 1989 y van Buurt 2014 diciendo lo mismo, y la prueba interna de barabara (%s #30: «Árbol de madera dura y pesada. Olivo») — la reduplicada de la misma raíz ya estaba atestiguada como árbol. Lectura descartada por D7: río, corriente fluvial (venía de cognado proto-arawakan/topónimo, sin cita) — queda registrada aquí, no se pierde" % (Z, Z),
    },
}

# ── D9: `bana` se reescribe entera (sanea el bug de las dos claves notas) ──
BANA_MARCADOR = "HOMÓNIMOS DECLARADOS"
BANA_NUEVA = (
    '"es": "hígado", "fuente": "caquetío-reconstruido", "categoria": "cuerpo", '
    '"notas": "Decisión D9 (tanda 2026-08-30) — %s: bana-1 cerro, sitio alto es '
    "caquetío-ATESTIGUADO (%s #26 «Bana (E): Sitio, cerro alto»; composición "
    "capu+bana = «duende del cerro» #61; el cerro de Santa Ana se llamaba Cerro "
    "de Capú). Esta entrada es bana-2 hígado, reconstruida por cognado lokono "
    "(Pet 1987: bana, bana-ha) — COGNADO VERIFICADO 2026-08-31 en la serie "
    "Swadesh de Oliver, fila 53 liver: lokono ebana, island-carib *bana, "
    "guajiro apa-na, y la serie panarahuaca *pana entera (nu-pana, nu-shupana, "
    "-upana, apakana...; ver 6-fusion/tabla_a1_a7_swadesh.yaml). El morfema "
    "toponímico -bana vive en morfologia.md y morfemas.yaml. Saneado de paso un "
    "bug latente: la entrada traía dos claves notas y la segunda pisaba a la "
    'primera"'
) % (BANA_MARCADOR, Z)

# ── D5b: `buco` sale (absorbida por `buko`) ──
BUCO_COMENTARIO = (
    '    # "buco" → fusionada con "buko" (D5b, tanda 2026-08-30): el lema '
    "fonémico sobrevive (D5a)\n"
    "    #   y la grafía de fuente viaja en forma_fuente. Cita reina: "
    "Ballesteros 1550. Ver la entrada buko.\n"
)


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def _entrada(contenido, clave):
    patron = re.compile(r'^(\s*"' + re.escape(clave) + r'":\s*\{)([^}]*?)(\})',
                        re.MULTILINE)
    return patron.search(contenido)


def _set_campo(cuerpo, campo, valor):
    if '"' in valor or "}" in valor:
        raise ValueError("valor con comilla o llave: %r" % valor[:40])
    m = re.search(r'"%s":\s*"([^"]*)"' % re.escape(campo), cuerpo)
    if m:
        if m.group(1) == valor:
            return cuerpo, False
        return cuerpo[:m.start(1)] + valor + cuerpo[m.end(1):], True
    nuevo = cuerpo.rstrip()
    if not nuevo.endswith(","):
        nuevo += ","
    return nuevo + ' "%s": "%s"' % (campo, valor), True


def aplicar_campos(contenido, tabla):
    cambiadas, sin_cambio, ausentes = [], [], []
    for clave, campos in sorted(tabla.items()):
        m = _entrada(contenido, clave)
        if not m:
            ausentes.append(clave)
            continue
        cuerpo, toco = m.group(2), False
        for campo, valor in campos.items():
            cuerpo, c = _set_campo(cuerpo, campo, valor)
            toco = toco or c
        if not toco:
            sin_cambio.append(clave)
            continue
        contenido = (contenido[:m.start()] + m.group(1) + cuerpo + m.group(3)
                     + contenido[m.end():])
        cambiadas.append(clave)
    return contenido, cambiadas, sin_cambio, ausentes


def reescribir_bana(contenido):
    """D9: una sola clave `notas`, con la homonimia declarada. Idempotente.

    La marca de "ya hecho" es la ÚLTIMA frase distintiva del texto vigente
    (no el marcador genérico): así una edición posterior de BANA_NUEVA
    —como la verificación del cognado del 08-31— se aplica sobre la versión
    anterior en vez de saltársela."""
    m = _entrada(contenido, "bana")
    if not m:
        return contenido, "⚠ bana NO ENCONTRADA"
    if "COGNADO VERIFICADO" in m.group(2):
        return contenido, "ya estaba"
    nuevo = m.group(1).rstrip("{") + "{\n        " + BANA_NUEVA + "\n    " + m.group(3)
    contenido = contenido[:m.start()] + nuevo + contenido[m.end():]
    return contenido, "reescrita (homónimo declarado, bug de notas dobles saneado)"


def retirar_buco(contenido):
    """D5b: `buco` sale de VOCABULARIO_BASE; queda el comentario que apunta
    a `buko`. Idempotente: si la clave no está, no hay nada que hacer."""
    m = _entrada(contenido, "buco")
    if not m:
        return contenido, "ya estaba fuera"
    inicio = contenido.rfind("\n", 0, m.start()) + 1
    fin = contenido.find("\n", m.end())
    fin = len(contenido) if fin == -1 else fin + 1
    contenido = contenido[:inicio] + BUCO_COMENTARIO + contenido[fin:]
    return contenido, "retirada; comentario en su lugar"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    _forzar_utf8()

    with open(LEXICON_FILE, encoding="utf-8") as fh:
        original = fh.read()
    contenido = original

    print("=" * 78)
    print("  TANDA 2026-08-30 — F1 · D5b · D9 · #101")
    print("=" * 78)

    contenido, cam, igual, aus = aplicar_campos(contenido, CAMPOS)
    print("\n  CAMPOS  (%d entradas)" % len(CAMPOS))
    print("    aplicadas : %s" % (", ".join(cam) or "—"))
    if igual:
        print("    ya estaban: %s" % ", ".join(igual))
    if aus:
        print("    ⚠ NO ENCONTRADAS: %s" % ", ".join(aus))

    contenido, msg = reescribir_bana(contenido)
    print("\n  D9 · bana (homónimo declarado): %s" % msg)

    contenido, msg = retirar_buco(contenido)
    print("  D5b · buco → buko: %s" % msg)

    if args.dry_run:
        print("\n  --dry-run: el lexicón NO se tocó.")
        return 0
    if contenido == original:
        print("\n  Nada que escribir: ya estaba al día.")
        return 0
    with open(LEXICON_FILE, "w", encoding="utf-8", newline="") as fh:
        fh.write(contenido)
    print("\n  ✓ curiana_lexicon.py escrito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
