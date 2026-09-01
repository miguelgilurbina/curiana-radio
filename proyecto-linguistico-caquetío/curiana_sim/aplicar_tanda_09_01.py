# -*- coding: utf-8 -*-
"""
CURIANA — aplicador de la tanda del 2026-09-01 (D3 + D1)
=========================================================

Registro: 6-fusion/decisiones_tanda_2026-09-01.yaml. Dossiers:
6-fusion/issues-pendientes/comentario-32-dossier-d1.md y
comentario-34-dossier-d3.md.

    python aplicar_tanda_09_01.py --dry-run
    python aplicar_tanda_09_01.py

QUÉ APLICA
----------
D3 (#34, opción A): `normalizar_por_dialecto()` se cablea en el UMBRAL del
rescate intra-turno vía `curiana_social.necesita_rescate()`; el score
almacenado sigue CRUDO. Y el rescate se apaga en --ablacion (el brazo de
control corre sin esa inyección de convergencia).

D1 (#32, opción B): los 6 linajes y las personas de fondo de
genealogia.yaml pasan a canon-simulación; Waimo-ko queda como CANDIDATO
ELEGIBLE (puerta 1 de 3 — parentesco-038 como regla del modelo), no
"sucesor natural"; la pluralidad de candidatos (parentesco-039) es
expansión aprobada sin ejecutar.

Idempotente: cada operación se salta si su texto viejo ya no está y el
nuevo sí. Los tests del rescate viven en tests/test_rescate_d3.py.
"""

import argparse
import io
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


# ── D3: curiana_social.py ─────────────────────────────────────────────

S_DOC_VIEJO = '''⚠ `normalizar_por_dialecto()` NO está cableada al pipeline (auditoría
2026-07-20): se define y se testea aquí, y AUDITORIA_OPUS.md §"metr.score" la
lista como paso del flujo, pero ningún módulo la llama. Es decir, la "justicia
L2" no está activa: los hablantes foráneos se miden con el rasero del nativo.

Se deja deliberadamente sin conectar. Activarla multiplicaría el score de un
caribe por 0.65/0.25 = 2.6 (un 4.5 crudo pasaría a 10/10), lo que cambiaría la
semántica de la métrica insignia del proyecto y rompería la comparabilidad con
todos los runs ya publicados. Es una decisión de diseño pendiente, no un
descuido: o se cablea y se re-corre todo, o se elimina la función.'''

S_DOC_NUEVO = '''D3 (#34) DECIDIDA el 2026-09-01 — opción A: `normalizar_por_dialecto()` se
cablea en el UMBRAL DEL RESCATE intra-turno (ver `necesita_rescate()` y el
orquestador), y SOLO ahí. El score que se ALMACENA sigue siendo el crudo: la
métrica insignia y la comparabilidad con los runs publicados no cambian. La
"justicia L2" opera donde el score tiene efecto dentro del run (el reintento),
no en el dato — la lección de fase 1 ("el instrumento medía en parte a sus
autores") prohíbe hornear estas constantes en lo almacenado.

Y en ABLACIÓN no hay rescate: es una inyección que empuja convergencia y el
brazo de control corre sin ella. Reserva declarada: las densidades objetivo
siguen siendo constantes de diseño sin base empírica; calibrarlas desde los
runs queda como mejora anotada (6-fusion/decisiones_tanda_2026-09-01.yaml).'''

S_FUNC_ANCLA = '''    objetivo = perfil_dialectal(etnia)["densidad_objetivo"] or _DENSIDAD_REF
    return round(min(score_crudo * (_DENSIDAD_REF / objetivo), 10.0), 1)


def prompt_rasgos_dialectales(etnia: str | None) -> str:'''

S_FUNC_NUEVA = '''    objetivo = perfil_dialectal(etnia)["densidad_objetivo"] or _DENSIDAD_REF
    return round(min(score_crudo * (_DENSIDAD_REF / objetivo), 10.0), 1)


def necesita_rescate(metr: dict, etnia: str | None, ablacion: bool = False) -> bool:
    """D3 (#34, decidida 2026-09-01): ¿la respuesta amerita el reintento
    intra-turno? El umbral se evalúa sobre el score NORMALIZADO por dialecto
    (justicia L2: el caribe no reintenta por obedecer su propio prompt); lo
    que se almacena sigue siendo el score crudo. En ABLACIÓN no hay rescate:
    es una inyección que empuja convergencia y el control corre sin ella."""
    if ablacion:
        return False
    fuga_otra_lengua = (metr.get("otro_arahuaco", 0) >= 3
                        and metr.get("pct_caquetio_especifico", 1) < 0.3)
    return normalizar_por_dialecto(metr["score"], etnia) < 5.0 or fuga_otra_lengua


def prompt_rasgos_dialectales(etnia: str | None) -> str:'''

# ── D3: curiana_orchestrator_v2.py ────────────────────────────────────

O_IMPORT_VIEJO = '''from curiana_social import (
    DifusionLexica,
    prompt_rasgos_dialectales,
)'''
O_IMPORT_NUEVO = '''from curiana_social import (
    DifusionLexica,
    necesita_rescate,
    prompt_rasgos_dialectales,
)'''

O_RESCATE_VIEJO = '''    metr = score_linguistico(response, lexico)
    fuga_otra_lengua = metr.get("otro_arahuaco", 0) >= 3 and metr.get("pct_caquetio_especifico", 1) < 0.3
    if metr["score"] < 5.0 or fuga_otra_lengua:'''
O_RESCATE_NUEVO = '''    metr = score_linguistico(response, lexico)
    # D3 (#34, 2026-09-01): el umbral se evalúa sobre el score NORMALIZADO
    # por dialecto, y en ablación no hay rescate — curiana_social.
    # necesita_rescate(). A la base va siempre el score CRUDO.
    if necesita_rescate(metr, etnia, ablacion):'''

# ── D1: genealogia.yaml y parentesco.yaml ─────────────────────────────

G_HEADER_VIEJO = "# curiana_agents.py NO se modifica. Esto es una propuesta en datos, para revisar y vetar."
G_HEADER_NUEVO = '''# curiana_agents.py NO se modifica. Esto es una propuesta en datos, para revisar y vetar.
#
# ✅ D1 DECIDIDA (2026-09-01, opción B — 6-fusion/decisiones_tanda_2026-09-01.yaml):
# los 6 linajes y las personas de fondo son CANON-SIMULACIÓN; Waimo-ko queda como
# CANDIDATO ELEGIBLE (puerta 1 de 3, parentesco-038 como regla del modelo), NO
# "sucesor natural"; la pluralidad de candidatos (parentesco-039) es expansión
# aprobada, sin ejecutar. Tótem y nombre de Kaira y Warana siguen abiertos a Miguel.'''

OPS = [
    ("curiana_sim/curiana_social.py", [
        ("D3: la nota de código muerto pasa a nota de decisión", S_DOC_VIEJO, S_DOC_NUEVO),
        ("D3: necesita_rescate() junto a la normalización", S_FUNC_ANCLA, S_FUNC_NUEVA),
    ]),
    ("curiana_sim/curiana_orchestrator_v2.py", [
        ("D3: import de necesita_rescate", O_IMPORT_VIEJO, O_IMPORT_NUEVO),
        ("D3: el rescate usa umbral normalizado y respeta ablación", O_RESCATE_VIEJO, O_RESCATE_NUEVO),
    ]),
    ("3-mundo/corpus/genealogia.yaml", [
        ("D1: encabezado con la decisión", G_HEADER_VIEJO, G_HEADER_NUEVO),
        ("D1: linaje Kaira — sucesor→candidato",
         "promover a Waimo-ko (el sucesor) e Itana-sha",
         "promover a Waimo-ko (el candidato) e Itana-sha"),
        ("D1: Itana-sha — madre del candidato",
         '"Hermana no nombrada, Itana-sha (fondo), madre del sucesor propuesto"',
         '"Hermana no nombrada, Itana-sha (fondo), madre del candidato propuesto"'),
        ("D1: la línea de Waimo-ko en Manaure",
         '"Sobrino uterino y sucesor natural: Waimo-ko (propuesto, ver abajo',
         '"Sobrino uterino y CANDIDATO ELEGIBLE, puerta 1 de 3 (D1, 2026-09-01): Waimo-ko (propuesto, ver abajo'),
        ("D1: la nota de Manaure cierra con la decisión",
         "pluralidad de sobrinos como patrón más realista, todavía no ejecutada en este archivo.",
         "pluralidad de sobrinos como patrón más realista, todavía no ejecutada en este archivo — expansión APROBADA por D1, sin ejecutar."),
        ("D1: la ficha de fondo de Waimo-ko",
         '''propuesto como su sucesor natural en
      línea matrilineal — no existe como agente hoy.''',
         '''CANDIDATO ELEGIBLE por
      línea matrilineal (D1 2026-09-01: candidato, no sucesor) — no existe como agente hoy.'''),
    ]),
    ("3-mundo/corpus/parentesco.yaml", [
        ("D1: parentesco-038 anota que el modelo la sigue",
         "o si ningún piache valida su capacidad. Ver parentesco-039 para la corrección de heredero único.",
         "o si ningún piache valida su capacidad. Ver parentesco-039 para la corrección de heredero único. DECISIÓN D1 (2026-09-01): las tres puertas son REGLA del modelo de sucesión de la simulación — el hecho sigue siendo hipotetico como reconstrucción histórica; lo decidido es que el diseño la sigue."),
        # Errata medida el 2026-09-01 (verificación a ojo, minería Paraguaná):
        # la impresa 255 es la Figura 40 y la 256 el viaje de Ojeda; la
        # sucesión y la bastardía están en 265-266 (pdf 292-293). Ver
        # 6-fusion/paraguana_dos_clanes.yaml §correccion_de_erratas.
        ("errata: parentesco-001 cita pp. 265-266",
         "cap. 3, pp. 255-256, 268 (",
         "cap. 3, pp. 265-266, 268 ("),
        ("errata: parentesco-003 cita pp. 265-266",
         "cap. 3, pp. 255-256, citando a Martí 1969",
         "cap. 3, pp. 265-266, citando a Martí 1969"),
    ]),
]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    _forzar_utf8()

    print("=" * 78)
    print("  TANDA 2026-09-01 — D3 (rescate justo, crudo a la base) + D1 (candidato)")
    print("=" * 78)
    print()

    avisos = 0
    for ruta_rel, ops in OPS:
        ruta = os.path.join(RAIZ, ruta_rel)
        txt = io.open(ruta, encoding="utf-8").read()
        for etiqueta, viejo, nuevo in ops:
            # El nuevo se comprueba PRIMERO: cuando el nuevo contiene al
            # viejo (encabezados que anexan), chequear al revés re-aplica
            # y duplica en cada corrida.
            if nuevo in txt:
                print(f"  · {etiqueta} (ya aplicada)")
            elif viejo in txt:
                txt = txt.replace(viejo, nuevo)
                print(f"  ✓ {etiqueta}")
            else:
                print(f"  ⚠ {etiqueta}: no encuentro ni viejo ni nuevo — el archivo derivó")
                avisos += 1
        if not args.dry_run:
            io.open(ruta, "w", encoding="utf-8", newline="").write(txt)

    if args.dry_run:
        print("\n  --dry-run: nada se escribió.")
    return 1 if avisos else 0


if __name__ == "__main__":
    sys.exit(main())
