# -*- coding: utf-8 -*-
"""
CURIANA — Fase 2 de D5: la migración de lemas a grafía fonémica
================================================================

D5 quedó decidida entera en la tanda del 2026-08-30 (F2/#36): lema fonémico
con `forma_fuente` obligatorio, y `gu`→/w/ uniforme. La tanda aplicó lo
puntual; esto aplica la migración masiva sobre la familia caquetía.

    python aplicar_fase2_d5.py --dry-run   # el plan de renombres, no escribe
    python aplicar_fase2_d5.py             # aplica lexicón + referencias

QUÉ HACE
--------
1. Recorre las entradas de familia caquetía (fuente caquetío*) del literal de
   `curiana_lexicon.py` y calcula el lema fonémico con las REGLAS APROBADAS:
       gü+vocal → w        gua/guo → w        (D5c, uniforme)
       gu+e/i   → g        (dígrafo castellano: /g/ dura, NO es [gw])
       qu+e/i   → k        c → k (salvo ch y salvo ce/ci)      q → k
       z → s               v → b
   NO aplica (disputadas en D5): h→∅ · ce/ci→s · x→sh. Tildes y ü se
   conservan (la tilde puede ser acento real; la ü del núcleo es fonema).
2. Renombra la clave, añade `forma_fuente` con la grafía anterior, y anota
   el renombre en `notas` solo si la entrada no tenía forma_fuente ya.
3. Propaga los renombres a las referencias vivas:
   `3-mundo/corpus/*.yaml` (palabra_lexicon) y el bloque FORMAS_SEED de
   `curiana_koine.py`.
4. Escribe el mapa completo en `6-fusion/migracion_lemas_fase2.yaml`.

QUÉ NO TOCA
-----------
- `coro` (D5b: el par coro/koro quedó «no tocar» — colisionaría con koro
  'cotorra') y `curiana` (topónimo y nombre de la polity/proyecto: por D5a
  los topónimos quedan del lado fuente hasta su propia migración).
- Entradas de familia caquetía que viven en `lexicon_zavala.py` (GENERADO):
  se reportan como pendientes de la regeneración, no se editan a mano.
- Colisiones: si el lema nuevo ya existe como clave, se reporta y NO se
  renombra (cada colisión es una decisión, no un accidente).

Idempotente: una entrada ya fonémica no cambia; correrlo dos veces es no-op.
"""

import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LEXICON_FILE = os.path.join(AQUI, "curiana_lexicon.py")
KOINE_FILE = os.path.join(AQUI, "curiana_koine.py")
RAIZ = os.path.dirname(AQUI)
CORPUS_DIR = os.path.join(RAIZ, "3-mundo", "corpus")
MAPA_FILE = os.path.join(RAIZ, "6-fusion", "migracion_lemas_fase2.yaml")

EXCLUIDAS = {
    "coro": "D5b: par coro/koro decidido «no tocar» (colisión con koro 'cotorra')",
    "curiana": "topónimo y nombre de la polity: queda del lado fuente (D5a) hasta la migración de toponimos.yaml",
}


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def lema_fonemico(forma):
    """Las reglas de D5 aprobadas, en orden. Conserva tildes, ü, h, ce/ci, x."""
    f = forma
    f = re.sub(r"g[üu](?=[aáoó])", "w", f)      # gua/guo/güa → wa/wo
    f = re.sub(r"gü(?=[eéií])", "w", f)         # güe/güi → we/wi
    f = re.sub(r"gu(?=[eéií])", "g", f)         # gue/gui → ge/gi (dígrafo /g/)
    f = re.sub(r"qu(?=[eéií])", "k", f)         # que/qui → ke/ki
    f = f.replace("ch", "\x01")                  # proteger el fonema ch
    f = re.sub(r"c(?=[eéií])", "\x02", f)       # proteger ce/ci (disputada)
    f = f.replace("c", "k")
    f = f.replace("\x01", "ch").replace("\x02", "c")
    f = re.sub(r"q(?![uü])", "k", f)
    f = f.replace("z", "s").replace("v", "b")
    return f


def entradas_literales(contenido):
    """(clave, fuente) de cada entrada del dict literal del lexicón."""
    out = []
    for m in re.finditer(r'^\s*"([^"]+)":\s*\{([^}]*?)\}', contenido, re.MULTILINE):
        fm = re.search(r'"fuente":\s*"([^"]*)"', m.group(2))
        out.append((m.group(1), fm.group(1) if fm else ""))
    return out


def plan_renombres(contenido):
    import importlib, sys as _s
    _s.path.insert(0, AQUI)
    V = importlib.import_module("curiana_lexicon").VOCABULARIO_BASE
    literales = dict(entradas_literales(contenido))
    claves_todas = set(V.keys()) | set(literales.keys())

    renombres, colisiones, en_generado, excluidas = [], [], [], []
    for clave, d in sorted(V.items()):
        fuente = str(d.get("fuente", ""))
        if not fuente.startswith("caquetío"):
            continue
        if clave in EXCLUIDAS:
            excluidas.append((clave, EXCLUIDAS[clave]))
            continue
        nuevo = lema_fonemico(clave)
        if nuevo == clave:
            continue
        if clave not in literales:
            en_generado.append((clave, nuevo))
            continue
        if nuevo in claves_todas:
            colisiones.append((clave, nuevo))
            continue
        renombres.append((clave, nuevo))
    return renombres, colisiones, en_generado, excluidas


def aplicar_lexicon(contenido, renombres):
    hechos = []
    for viejo, nuevo in renombres:
        m = re.search(r'^(\s*)"%s":\s*\{([^}]*?)(\})' % re.escape(viejo),
                      contenido, re.MULTILINE)
        if not m:
            continue
        cuerpo = m.group(2)
        if '"forma_fuente"' not in cuerpo:
            c = cuerpo.rstrip()
            if not c.endswith(","):
                c += ","
            cuerpo = c + ' "forma_fuente": "%s"' % viejo
        bloque = '%s"%s": {%s%s' % (m.group(1), nuevo, cuerpo, m.group(3))
        contenido = contenido[:m.start()] + bloque + contenido[m.end():]
        hechos.append((viejo, nuevo))
    return contenido, hechos


def propagar(renombres, dry):
    """palabra_lexicon en el corpus + FORMAS_SEED en koine."""
    mapa = dict(renombres)
    tocados = []
    for nombre in sorted(os.listdir(CORPUS_DIR)):
        if not nombre.endswith(".yaml"):
            continue
        ruta = os.path.join(CORPUS_DIR, nombre)
        txt = io.open(ruta, encoding="utf-8").read()
        nuevo_txt, n = txt, 0
        for viejo, nuevo in mapa.items():
            nuevo_txt, k = re.subn(r"(palabra_lexicon:\s*)%s\b" % re.escape(viejo),
                                   r"\g<1>%s" % nuevo, nuevo_txt)
            n += k
        if n:
            tocados.append(("corpus/" + nombre, n))
            if not dry:
                io.open(ruta, "w", encoding="utf-8", newline="").write(nuevo_txt)

    txt = io.open(KOINE_FILE, encoding="utf-8").read()
    m = re.search(r"FORMAS_SEED[^=]*=\s*\{", txt)
    if m:
        fin = txt.find("\n}", m.end())
        bloque = txt[m.end():fin]
        nuevo_bloque, n = bloque, 0
        for viejo, nuevo in mapa.items():
            nuevo_bloque, k = re.subn(r'"%s"' % re.escape(viejo),
                                      '"%s"' % nuevo, nuevo_bloque)
            n += k
        if n:
            tocados.append(("curiana_koine.py (FORMAS_SEED)", n))
            if not dry:
                io.open(KOINE_FILE, "w", encoding="utf-8", newline="").write(
                    txt[:m.end()] + nuevo_bloque + txt[fin:])
    return tocados


def renombres_del_generado():
    """(forma_fuente, lema) de lexicon_zavala.py — los renombres que ejecutó
    el propio generador (minar_zavala_glosario.py) al regenerar con D5."""
    try:
        from lexicon_zavala import GLOSARIO_ZAVALA
    except ImportError:
        return []
    return sorted((e["forma_fuente"], k) for k, e in GLOSARIO_ZAVALA.items()
                  if e.get("forma_fuente"))


def escribir_mapa(renombres, colisiones, en_generado, excluidas,
                  generado_hechos=()):
    lineas = [
        "# ─────────────────────────────────────────────────────────────",
        "# MAPA — migración de lemas de la Fase 2 de D5 (generado por",
        "# aplicar_fase2_d5.py; la fecha es la del commit que lo trae).",
        "# forma_fuente conserva la grafía anterior en cada entrada.",
        "# ─────────────────────────────────────────────────────────────",
        "renombres:",
    ]
    for v, n in renombres:
        lineas.append("  - {de: %s, a: %s}" % (v, n))
    lineas.append("excluidas_por_decision:")
    for v, razon in excluidas:
        lineas.append('  - {forma: %s, razon: "%s"}' % (v, razon))
    lineas.append("colisiones_no_renombradas:  # cada una es una decisión pendiente")
    for v, n in colisiones:
        lineas.append("  - {forma: %s, chocaria_con: %s}" % (v, n))
    lineas.append("renombres_en_generado:  # ejecutados por minar_zavala_glosario.py; forma_fuente en cada entrada")
    for v, n in generado_hechos:
        lineas.append("  - {de: %s, a: %s}" % (v, n))
    lineas.append("en_lexicon_zavala_pendientes:  # colisiones del generado — cada una es una decisión")
    for v, n in en_generado:
        lineas.append("  - {forma: %s, lema_fonemico: %s}" % (v, n))
    io.open(MAPA_FILE, "w", encoding="utf-8", newline="\n").write("\n".join(lineas) + "\n")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    _forzar_utf8()

    contenido = io.open(LEXICON_FILE, encoding="utf-8").read()
    renombres, colisiones, en_generado, excluidas = plan_renombres(contenido)

    print("=" * 78)
    print("  FASE 2 DE D5 — migración de lemas a grafía fonémica")
    print("=" * 78)
    print("\n  RENOMBRES (%d):" % len(renombres))
    for v, n in renombres:
        print("    %-16s → %s" % (v, n))
    if excluidas:
        print("\n  EXCLUIDAS POR DECISIÓN (%d): %s" % (
            len(excluidas), ", ".join(v for v, _ in excluidas)))
    if colisiones:
        print("\n  ⚠ COLISIONES — NO se renombran (%d):" % len(colisiones))
        for v, n in colisiones:
            print("    %-16s chocaría con %s" % (v, n))
    if en_generado:
        print("\n  EN lexicon_zavala (GENERADO) — pendientes de regeneración (%d): %s" % (
            len(en_generado), ", ".join(v for v, _ in en_generado)))

    if args.dry_run:
        print("\n  --dry-run: nada se escribió.")
        return 0

    contenido, hechos = aplicar_lexicon(contenido, renombres)
    io.open(LEXICON_FILE, "w", encoding="utf-8", newline="").write(contenido)
    print("\n  ✓ lexicón: %d entradas renombradas (forma_fuente añadida)." % len(hechos))

    # Se propagan también los renombres que ya ejecutó el GENERADOR: las
    # referencias vivas (corpus, FORMAS_SEED) no distinguen de qué módulo
    # viene la palabra. Fue lo que atrapó test_formas_seed: la semilla de
    # Dara-ko decía cunaro y el generado ya decía kunaro.
    generado_hechos = renombres_del_generado()
    tocados = propagar(hechos + generado_hechos, dry=False)
    for donde, n in tocados:
        print("  ✓ %s: %d referencia(s) actualizadas." % (donde, n))

    escribir_mapa(hechos, colisiones, en_generado, excluidas, generado_hechos)
    print("  ✓ mapa escrito: 6-fusion/migracion_lemas_fase2.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
