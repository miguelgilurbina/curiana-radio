# -*- coding: utf-8 -*-
"""
CURIANA — colisiones de la Fase 2 de D5, y los nombres de agente
=================================================================

Decisión de Miguel del 2026-08-31 (registrada en
6-fusion/decisiones_colisiones_d5_2026-08-31.yaml): la grafía española es
GRAFÍA (va a forma_fuente); el lema fonémico es LA PALABRA y vive una sola
vez en el lexicón. Palabras distintas que colapsan en el mismo lema son
homónimos y se declaran (patrón D9). Atestación directa gana la etiqueta
(precedente de `para`). Y los 10 nombres de agente en grafía colonial se
renombran: las primeras tandas de simulación no se reutilizan.

    python aplicar_colisiones_d5.py --dry-run   # qué haría, sin escribir
    python aplicar_colisiones_d5.py             # aplica

QUÉ HACE
--------
1. curiana_lexicon.py — las fusiones del literal:
   cati+kati → kati (atestiguada) · canoa+kanoa → kanoa (reconstruida) ·
   hamaca+hamaka → hamaka (reconstruida) · quiba+quiva → kiba (nueva,
   homónimos declarados) · sigua+siwa → siwa (atestiguada, homónimos).
2. Renombra los 10 agentes (Buco→Buko, Chiriguare→Chiriware, Sha-corie→
   Sha-korie...) en todo el código del motor, y las palabras sueltas de sus
   prompts (cunaro, guaranaro, buco, corie, chiriguare).
3. FORMAS_SEED: canoa→kanoa (6 semillas).
4. 2-lengua/cognados.yaml: CQ y clave_origen al lema fonémico.
5. curiana_database.py: test_words hamaca→hamaka.

QUÉ NO TOCA
-----------
- Los IDs de locación ("buco", "conuco"): etiquetas de registro, no léxico
  que puntúe. Decisión aparte si se quiere.
- naure #185/#186: no es colisión de grafías; sigue en COLISIONES_D5.
- lexicon_zavala.py: es GENERADO — la salida de quiba/quiva/sigua la hace
  el miner vía FUSIONADAS_EN_LITERAL, no este script.

Idempotente: cada operación se salta si su texto viejo ya no está y el
nuevo sí. Si no está ninguno de los dos, avisa (el archivo derivó).
"""

import argparse
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


MARCA = "Decisión colisiones D5 (2026-08-31)"

# ── 1. Las fusiones del literal (reemplazos exactos) ──────────────────

L_HAMACA = '    "hamaca":     {"sig": "red colgante para dormir",                       "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido"},\n'
L_CANOA = '    "canoa":      {"sig": "embarcación excavada en tronco",                 "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido"},\n'
L_SIWA_VIEJA = '    "siwa":       {"sig": "sal de comercio (< proto-arawakan *siwa)",       "cat": "sust",  "fuente": "proto-arawakan/lokono"},'
L_SIWA_NUEVA = '    "siwa":       {"sig": "blando",                                        "cat": "v_raiz","fuente": "caquetío-atestiguado", "forma_fuente": "sigua", "notas": "' + MARCA + ' — HOMÓNIMOS DECLARADOS: siwa-1 blando, caquetío-ATESTIGUADO (Zavala Reyes 2015 #227 «Sigua» (E); su homógrafo con el español era de la grafía y se disolvió con ella) y siwa-2 sal de comercio (< proto-arawakan *siwa, la entrada anterior de esta clave, capa lokono). La atestación directa gana la etiqueta — precedente de para (2026-07-20)"},'
L_CATI = '    "cati":       {"sig": "luna",                                           "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #71 (CGB): «Luna [catire: persona de tez blanca]»"},'
L_KIBA = '    "kiba":       {"sig": "piedra",                                        "cat": "sust",  "fuente": "caquetío-atestiguado", "forma_fuente": "quiva", "notas": "' + MARCA + ' — HOMÓNIMOS DECLARADOS bajo el mismo lema: kiba-1 piedra (Zavala Reyes 2015 #218 «Quiva» (E); y #92 «Cuiva. Kiba» (PMA) piedra — Arcaya registró la grafía k: el lema fonémico está impreso en la fuente) y kiba-2 ayuda (Zavala #203 «Quiba» (AM), cat v_raiz). La grafía b~v es betacismo colonial: mismo lema fonémico. El sentido piedra lleva el sig activo por la capa toponímica (van Buurt §8 siba/quiba piedra-roca; quibacoa, Todariquiba). Ambas salen del generado: FUSIONADAS_EN_LITERAL del miner"},'

B_KATI_VIEJO = '''    "kati": {
        "es": "luna",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *kati; atestiguada en 3 lenguas: CQ: cati, WY: kachi, LK: katsi; Payne (1991), Brinton (1871)",
        "categoria": "cosmos"
    },'''
B_KATI_NUEVO = '''    "kati": {
        "es": "luna",
        "fuente": "caquetío-atestiguado",
        "forma_fuente": "cati",
        "notas": "''' + MARCA + ''' — FUSIONADA con cati: la grafía c es colonial y el lema fonémico es la palabra. Atestiguada: Zavala Reyes 2015, glosario #71 (CGB): «Luna [catire: persona de tez blanca]». Cognados: proto-arahuaco *kati, WY kachi, LK katsi (Payne 1991, Brinton 1871); en el Swadesh de Oliver (Tabla A-2, fila moon) el lokono trae kathi — similitud 1.00, la fila bandera del cómputo de D11. RE-ETIQUETADA de proto-arahuaco a caquetío-atestiguado por atestación directa (precedente de para, 2026-07-20)",
        "categoria": "cosmos"
    },'''

B_KANOA_VIEJO = '''    "kanoa": {
        "es": "canoa, embarcación",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *kanoa; atestiguada en 3 lenguas: CQ: canoa, LK: kannoa, TN: canoa; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },'''
B_KANOA_NUEVO = '''    "kanoa": {
        "es": "canoa, embarcación excavada en tronco",
        "fuente": "caquetío-reconstruido",
        "forma_fuente": "canoa",
        "notas": "''' + MARCA + ''' — FUSIONADA con canoa (núcleo fundacional, forma justificada por cognado en taíno): grafía española del mismo lema. Cognados: proto-arahuaco *kanoa, LK kannoa, TN canoa (Payne 1991, Brinton 1871). Se queda RECONSTRUIDA: el CQ canoa de la serie comparativa no es atestación independiente — canoa es préstamo taíno del propio español, riesgo de circularidad",
        "categoria": "utiles"
    },'''

B_HAMAKA_VIEJO = '''    "hamaka": {
        "es": "hamaca, cama colgante",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *hamaka; atestiguada en 3 lenguas: CQ: hamaca, LK: hamaha, TN: hamaca; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },'''
B_HAMAKA_NUEVO = '''    "hamaka": {
        "es": "hamaca, red colgante para dormir",
        "fuente": "caquetío-reconstruido",
        "forma_fuente": "hamaca",
        "notas": "''' + MARCA + ''' — FUSIONADA con hamaca (núcleo fundacional, forma justificada por cognado en taíno). Cognados: proto-arahuaco *hamaka, LK hamaha, TN hamaca (Payne 1991, Brinton 1871). Se queda RECONSTRUIDA (mismo motivo que kanoa: hamaca es préstamo taíno del propio español). OJO: amaka sitio-de-moler-maíz (Zavala #9, forma_fuente amaca) es palabra DISTINTA, y h→∅ sigue disputada en D5 — no se fusionan",
        "categoria": "utiles"
    },'''

OPS_LEXICON = [
    ("borrar `hamaca` (absorbida por hamaka)", L_HAMACA, ""),
    ("borrar `canoa` (absorbida por kanoa)", L_CANOA, ""),
    ("cati → nueva entrada `kiba` (quiba+quiva)", L_CATI, L_KIBA),
    ("fusionar `kati`", B_KATI_VIEJO, B_KATI_NUEVO),
    ("fusionar `kanoa`", B_KANOA_VIEJO, B_KANOA_NUEVO),
    ("fusionar `hamaka`", B_HAMAKA_VIEJO, B_HAMAKA_NUEVO),
    ("fusionar `siwa` (homónimos)", L_SIWA_VIEJA, L_SIWA_NUEVA),
    ("composición de nombres: corie", '"corie + ko = Corie-ko', '"korie + ko = Korie-ko'),
    ("composición de nombres: buco", '"buco + ko = Buco-ko', '"buko + ko = Buko-ko'),
]

# ── 2. Los nombres de agente (los -ko/-ni/-sha antes que el simple) ───

NOMBRES = [
    ("Buco-ko", "Buko-ko"), ("Buco-ni", "Buko-ni"),
    ("Cahu-sha", "Kahu-sha"), ("Chiriguare", "Chiriware"),
    ("Corie-ko", "Korie-ko"), ("Cunaro-bana", "Kunaro-bana"),
    ("Guama-ko", "Wama-ko"), ("Guaranaro-sha", "Waranaro-sha"),
    ("Sha-corie", "Sha-korie"),
]
RE_BUCO_SOLO = re.compile(r"\bBuco\b(?!-)")   # el niño Buko, tras los -ko/-ni

ARCHIVOS_NOMBRES = [
    "curiana_agents.py", "curiana_state.py", "curiana_koine.py",
    "curiana_social.py", "curiana_orchestrator_v2.py", "curiana_lexicon.py",
    "aplicar_d10.py", "seed_demo_run.py",
]

# El canon del vault que describe a la POBLACIÓN (el validador del corpus
# cruza los nombres contra ALL_AGENTS). Los análisis de runs históricos
# (5-experimento/analisis/, BITACORA_RUNS) y los comentarios ya publicados
# (issues-pendientes/publicados/) NO se tocan: documentan lo que pasó con
# los nombres que entonces había.
ARCHIVOS_NOMBRES_VAULT = [
    os.path.join("3-mundo", "corpus", "creencia.yaml"),
    os.path.join("3-mundo", "corpus", "ecologia.yaml"),
    os.path.join("3-mundo", "corpus", "genealogia.yaml"),
    os.path.join("3-mundo", "corpus", "geografia_politica.yaml"),
    os.path.join("3-mundo", "corpus", "parentesco.yaml"),
    os.path.join("3-mundo", "corpus", "transmision.yaml"),
    os.path.join("3-mundo", "corpus", "ecologia_lexicon_map.md"),
    os.path.join("3-mundo", "ensayos", "01_familia_caquetia.md"),
    os.path.join("3-mundo", "ensayos", "02_ecologia_golfete.md"),
    os.path.join("3-mundo", "ensayos", "04_transmision_saber.md"),
    os.path.join("3-mundo", "ensayos", "05_geografia_politica_y_sucesion.md"),
    os.path.join("3-mundo", "CULTURA_CAQUETIA.md"),
    os.path.join("3-mundo", "mapa-geografia-politica.md"),
    os.path.join("2-lengua", "lexicon.md"),
    os.path.join("5-experimento", "CANON_TIERRA.md"),
    os.path.join("5-experimento", "DINAMICA_DE_RUNS.md"),
    os.path.join("1-plan", "PLAN_MAESTRO.md"),
    os.path.join("1-plan", "SIGUIENTE_TANDA.md"),
]

# ── 3. Palabras sueltas en prompts y escenas ──────────────────────────

OPS_PROSA = [
    ("curiana_agents.py", "barsure, buco, biro, chiriguare, Curiana",
     "barsure, buko, biro, chiriware, Curiana"),
    ("curiana_agents.py", "cunaro, guaranaro, bagre", "kunaro, waranaro, bagre"),
    ("curiana_agents.py", "Usas corie (armadillo)", "Usas korie (armadillo)"),
]
# "el/del buco" en prosa — NO toca los IDs de locación ("buco" entre comillas)
RE_BUCO_PROSA = re.compile(r"\b(el|El|del|Del|al|un) buco\b")

# ── 4. Datos de lengua y misceláneos ──────────────────────────────────

OPS_OTROS = [
    (os.path.join("2-lengua", "cognados.yaml"), "CQ: cati",
     "CQ: kati  # forma_fuente cati (colisiones D5 2026-08-31)"),
    (os.path.join("2-lengua", "cognados.yaml"), "CQ: canoa",
     "CQ: kanoa  # forma_fuente canoa (colisiones D5 2026-08-31)"),
    (os.path.join("2-lengua", "cognados.yaml"), "CQ: hamaca",
     "CQ: hamaka  # forma_fuente hamaca (colisiones D5 2026-08-31)"),
    (os.path.join("2-lengua", "cognados.yaml"), "clave_origen: canoa",
     "clave_origen: kanoa"),
    (os.path.join("2-lengua", "cognados.yaml"), "clave_origen: hamaca",
     "clave_origen: hamaka"),
    (os.path.join("curiana_sim", "curiana_database.py"), '"hamaca"', '"hamaka"'),
]


def _aplicar_exactas(ruta, ops, dry, hechas, avisos):
    txt = io.open(ruta, encoding="utf-8").read()
    for etiqueta, viejo, nuevo in ops:
        if viejo in txt:
            txt = txt.replace(viejo, nuevo)
            hechas.append(etiqueta)
        elif not nuevo or nuevo in txt:
            pass  # ya aplicada (los borrados: viejo ausente = hecho)
        else:
            avisos.append(f"{os.path.basename(ruta)}: no encuentro ni viejo ni nuevo — {etiqueta}")
    if not dry:
        io.open(ruta, "w", encoding="utf-8", newline="").write(txt)
    return txt


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    _forzar_utf8()
    dry = args.dry_run
    hechas, avisos = [], []

    print("=" * 78)
    print("  COLISIONES D5 + NOMBRES DE AGENTE — decisión del 2026-08-31")
    print("=" * 78)

    # 1. lexicón
    _aplicar_exactas(os.path.join(AQUI, "curiana_lexicon.py"),
                     [(e, v, n) for e, v, n in OPS_LEXICON], dry, hechas, avisos)

    # 2+3. nombres y prosa en el motor
    for nombre in ARCHIVOS_NOMBRES:
        ruta = os.path.join(AQUI, nombre)
        txt = io.open(ruta, encoding="utf-8").read()
        n_total = 0
        for viejo, nuevo in NOMBRES:
            txt, k = re.subn(re.escape(viejo), nuevo, txt)
            n_total += k
        txt, k = RE_BUCO_SOLO.subn("Buko", txt)
        n_total += k
        if nombre in ("curiana_agents.py", "curiana_state.py"):
            txt, k = RE_BUCO_PROSA.subn(r"\1 buko", txt)
            n_total += k
        if n_total:
            hechas.append(f"{nombre}: {n_total} renombre(s)")
            if not dry:
                io.open(ruta, "w", encoding="utf-8", newline="").write(txt)
    for rel in ARCHIVOS_NOMBRES_VAULT:
        ruta = os.path.join(RAIZ, rel)
        if not os.path.exists(ruta):
            avisos.append(f"no existe: {rel}")
            continue
        txt = io.open(ruta, encoding="utf-8").read()
        n_total = 0
        for viejo, nuevo in NOMBRES:
            txt, k = re.subn(re.escape(viejo), nuevo, txt)
            n_total += k
        txt, k = RE_BUCO_SOLO.subn("Buko", txt)
        n_total += k
        if n_total:
            hechas.append(f"{rel}: {n_total} renombre(s)")
            if not dry:
                io.open(ruta, "w", encoding="utf-8", newline="").write(txt)

    for ruta_rel, viejo, nuevo in OPS_PROSA:
        _aplicar_exactas(os.path.join(AQUI, ruta_rel),
                         [(f"prosa: {viejo[:40]}", viejo, nuevo)], dry, hechas, avisos)

    # 4. datos de lengua y misceláneos
    for ruta_rel, viejo, nuevo in OPS_OTROS:
        _aplicar_exactas(os.path.join(RAIZ, ruta_rel),
                         [(f"{ruta_rel}: {viejo}", viejo, nuevo)], dry, hechas, avisos)

    # FORMAS_SEED: canoa → kanoa (solo dentro del bloque, como el propagador)
    ruta_koine = os.path.join(AQUI, "curiana_koine.py")
    txt = io.open(ruta_koine, encoding="utf-8").read()
    m = re.search(r"FORMAS_SEED[^=]*=\s*\{", txt)
    if m:
        fin = txt.find("\n}", m.end())
        bloque, k = re.subn(r'"canoa"', '"kanoa"', txt[m.end():fin])
        if k:
            hechas.append(f"FORMAS_SEED: canoa → kanoa ({k})")
            if not dry:
                io.open(ruta_koine, "w", encoding="utf-8", newline="").write(
                    txt[:m.end()] + bloque + txt[fin:])

    print()
    for h in hechas:
        print(f"  ✓ {h}")
    if not hechas:
        print("  (nada que hacer: todo aplicado ya)")
    for a in avisos:
        print(f"  ⚠ {a}")
    if dry:
        print("\n  --dry-run: nada se escribió.")
    return 1 if avisos else 0


if __name__ == "__main__":
    sys.exit(main())
