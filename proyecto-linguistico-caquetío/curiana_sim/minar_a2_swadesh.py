# -*- coding: utf-8 -*-
"""
CURIANA — Minería de la Tabla A-2 de Oliver: la columna añú y el refuerzo lokono
================================================================================

Implementa el rumbo de D11 (#39, fijado el 2026-08-31): "sí o sí rebalancear
importando más lokono" + abrir la columna añú/paraujano, que tenía CERO
entradas del pariente costero más cercano. Registro de la decisión:
6-fusion/decisiones_tanda_2026-08-30.yaml §d11_rumbo.

Fuente: 6-fusion/tabla_a2_transcripcion.yaml — el Swadesh-100 comparado de
Oliver 1989 (Apéndice A, pp. impresas 561-565), transcrito A OJO el
2026-08-31 con OCR de contraste. La columna paraujano ES el material de campo
de Wilbert 1958-59 (Sinamaica); la columna arawak/lokono, la compilación de
Oliver.

    python minar_a2_swadesh.py                    # informe
    python minar_a2_swadesh.py --generar-modulo   # reescribe lexicon_a2.py

CURACIÓN (qué entra al lexicón y qué queda de referencia)
---------------------------------------------------------
ENTRA una forma solo si es LIBRE y LIMPIA: sin guion de ligadura (ni t-ein ni
kore-), sin asterisco (las *formas son reconstrucciones/atestaciones viejas
de Oliver), sin paréntesis internos de segmento opcional (kho(ro)), sin
espacios, y de una celda sin «(?)» ni marca de préstamo (SPANISH/CARIB/...).
Todo lo demás NO se pierde: queda en REFERENCIA_A2 con su motivo — las
formas ligadas y las reconstrucciones son datos comparativos de primera,
solo que no son entradas de lexicón.

Si la forma ya existe como clave del lexicón (pia, kai...), NO se pisa: la
colisión se registra en COLISIONES_A2 — y es dato en sí misma (el paraujano
compartiendo forma con el núcleo reconstruido es la señal areal).

⚠️ CAVEAT: la transcripción está pendiente de la segunda pasada de Miguel
contra la imagen (meta de tabla_a2_transcripcion.yaml). Cada entrada lo
declara en notas. Son vocabulario de COMPARACIÓN (detección de fugas en
score_linguistico y columnas del filtro fonotáctico), no habla de agentes.
"""

import argparse
import io
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TABLA = os.path.join(RAIZ, "6-fusion", "tabla_a2_transcripcion.yaml")
MODULO = os.path.join(AQUI, "lexicon_a2.py")

MARCAS = ("SPANISH", "CARIB", "KARIB", "AFRICANISM", "SPECIES")

# Glosa española y categoría por ítem del Swadesh (la glosa inglesa es la de
# Oliver; la española es la glosa activa `es` de la entrada).
GLOSAS: dict[str, tuple[str, str]] = {
    "I": ("yo", "gramatica"), "thou": ("tú", "gramatica"),
    "we": ("nosotros", "gramatica"), "this": ("este, esta", "gramatica"),
    "that": ("ese, esa", "gramatica"), "who": ("quién", "gramatica"),
    "what": ("qué", "gramatica"), "not": ("no, negación", "gramatica"),
    "all": ("todo, todos", "gramatica"), "many": ("muchos", "gramatica"),
    "one": ("uno", "numerales"), "two": ("dos", "numerales"),
    "big": ("grande", "cualidades"), "long": ("largo", "cualidades"),
    "small": ("pequeño", "cualidades"), "woman": ("mujer", "parentesco"),
    "man": ("hombre", "parentesco"), "person": ("persona, gente", "parentesco"),
    "fish": ("pez", "fauna"), "bird": ("pájaro, ave", "fauna"),
    "dog": ("perro", "fauna"), "louse": ("piojo", "fauna"),
    "tree": ("árbol", "flora"), "seed": ("semilla", "flora"),
    "leaf": ("hoja", "flora"), "root": ("raíz", "flora"),
    "bark": ("corteza", "flora"), "skin": ("piel, cuero", "cuerpo"),
    "flesh": ("carne", "cuerpo"), "blood": ("sangre", "cuerpo"),
    "bone": ("hueso", "cuerpo"), "fat": ("grasa", "cuerpo"),
    "egg": ("huevo", "fauna"), "horn": ("cuerno", "fauna"),
    "tail": ("cola, rabo", "fauna"), "feather": ("pluma", "fauna"),
    "hair": ("pelo, cabello", "cuerpo"), "head": ("cabeza", "cuerpo"),
    "ear": ("oreja", "cuerpo"), "eye": ("ojo", "cuerpo"),
    "nose": ("nariz", "cuerpo"), "mouth": ("boca", "cuerpo"),
    "tooth": ("diente", "cuerpo"), "tongue": ("lengua", "cuerpo"),
    "claw": ("garra, uña", "cuerpo"), "foot": ("pie", "cuerpo"),
    "knee": ("rodilla", "cuerpo"), "hand": ("mano", "cuerpo"),
    "belly": ("vientre, barriga", "cuerpo"), "neck": ("cuello", "cuerpo"),
    "breast": ("pecho, seno", "cuerpo"), "heart": ("corazón", "cuerpo"),
    "liver": ("hígado", "cuerpo"), "drink": ("beber", "acciones"),
    "eat": ("comer", "acciones"), "bite": ("morder", "acciones"),
    "see": ("ver", "acciones"), "hear": ("oír", "acciones"),
    "know": ("saber, conocer", "acciones"), "sleep": ("dormir", "acciones"),
    "die": ("morir", "acciones"), "kill": ("matar", "acciones"),
    "swim": ("nadar", "acciones"), "fly": ("volar", "acciones"),
    "walk": ("caminar", "acciones"), "come": ("venir", "acciones"),
    "lie": ("estar acostado", "acciones"), "sit": ("estar sentado", "acciones"),
    "stand": ("estar de pie", "acciones"), "give": ("dar", "acciones"),
    "say": ("decir", "acciones"), "sun": ("sol", "cosmos"),
    "moon": ("luna", "cosmos"), "star": ("estrella", "cosmos"),
    "water": ("agua", "geografia"), "rain": ("lluvia", "cosmos"),
    "stone": ("piedra", "geografia"), "sand": ("arena", "geografia"),
    "earth": ("tierra", "geografia"), "cloud": ("nube", "cosmos"),
    "sky": ("cielo", "cosmos"), "smoke": ("humo", "utiles"),
    "fire": ("fuego", "utiles"), "ash": ("ceniza", "utiles"),
    "burn": ("arder, quemar", "acciones"), "path": ("camino, senda", "geografia"),
    "mountain": ("cerro, montaña", "geografia"), "red": ("rojo", "cualidades"),
    "green": ("verde", "cualidades"), "yellow": ("amarillo", "cualidades"),
    "white": ("blanco", "cualidades"), "black": ("negro", "cualidades"),
    "night": ("noche", "cosmos"), "hot": ("caliente", "cualidades"),
    "cold": ("frío", "cualidades"), "full": ("lleno", "cualidades"),
    "new": ("nuevo", "cualidades"), "good": ("bueno", "cualidades"),
    "round": ("redondo", "cualidades"), "dry": ("seco", "cualidades"),
    "name": ("nombre", "gramatica"),
}

_ANOTACION_FINAL = re.compile(r"\s*\((=[^)]*|vid\.[^)]*|masc\.|fem\.|[a-z ]*\.\.+[a-z ]*)\)\s*$")
_FORMA_LIMPIA = re.compile(r"^[a-záéíóúüñgh'’]+$", re.IGNORECASE)


def _forzar_utf8():
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


def parsear_celda(celda: str):
    """(importables, referencia) de una celda. importables: [(forma, nota)];
    referencia: [(fragmento, motivo)]."""
    if not celda or celda.strip() in ("---", ""):
        return [], []
    if "(?)" in celda:
        return [], [(celda, "transcripción dudosa «(?)» — verificar contra la imagen")]
    if any(m in celda for m in MARCAS):
        return [], [(celda, "préstamo o marca de Oliver, no forma nativa")]
    importables, referencia = [], []
    for seg in celda.split("·"):
        for cand in seg.split("/"):
            cand = cand.strip()
            if not cand:
                continue
            nota = None
            m = _ANOTACION_FINAL.search(cand)
            if m:
                nota = m.group(1).strip()
                cand = cand[:m.start()].strip()
            if not cand:
                continue
            if "*" in cand:
                referencia.append((cand, "reconstrucción/atestación vieja de Oliver (*)"))
            elif cand.startswith("-") or cand.endswith("-") or "-" in cand:
                referencia.append((cand, "forma ligada (guion): morfología, no lema"))
            elif "(" in cand or ")" in cand:
                referencia.append((cand, "segmento opcional entre paréntesis"))
            elif " " in cand:
                referencia.append((cand, "forma compuesta/multi-palabra"))
            elif not _FORMA_LIMPIA.match(cand):
                referencia.append((cand, "caracteres fuera del patrón de forma"))
            elif len(cand) < 2:
                referencia.append((cand, "demasiado corta"))
            else:
                importables.append((cand.lower(), nota))
    return importables, referencia


def minar():
    import yaml
    with io.open(TABLA, encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    # IDEMPOTENCIA: como con lexicon_zavala — medir contra el lexicón PREVIO,
    # excluyendo lo que este propio módulo ya haya fusionado.
    sys.path.insert(0, AQUI)
    try:
        from lexicon_a2 import PARAUJANO_A2 as _P, LOKONO_A2 as _L
        propias = set(_P) | set(_L)
    except ImportError:
        propias = set()
    from curiana_lexicon import VOCABULARIO_BASE
    existentes = {w for w in VOCABULARIO_BASE if w not in propias}

    out = {"paraujano": {}, "lokono": {}}
    referencia = {"paraujano": [], "lokono": []}
    colisiones = []

    for col, fuente in (("paraujano", "paraujano"), ("lokono", "lokono")):
        vistos = out[col]
        for item in doc["items"]:
            n, gloss = item["n"], item["gloss"]
            celda = item.get(col) or ""
            imp, ref = parsear_celda(celda)
            referencia[col].extend(
                (n, gloss, frag, motivo) for frag, motivo in ref)
            if not imp:
                continue
            es, categoria = GLOSAS[gloss]
            forma, nota_forma = imp[0]
            variantes = [f for f, _ in imp[1:]]
            if forma in existentes:
                colisiones.append((col, n, gloss, forma))
                continue
            if forma in vistos:
                vistos[forma]["filas"].append((n, gloss))
                continue
            vistos[forma] = {
                "es": es, "fuente": fuente, "categoria": categoria,
                "filas": [(n, gloss)], "variantes": variantes,
                "nota_celda": nota_forma, "celda": celda,
            }
    return out, referencia, colisiones


def _nota(e, col):
    filas = "; ".join(f"fila {n} '{g}'" for n, g in e["filas"])
    quien = ("Wilbert 1958-59 (Sinamaica) vía Oliver 1989, Apéndice A, Tabla A-2"
             if col == "paraujano"
             else "Oliver 1989, Apéndice A, Tabla A-2, columna arawak/lokono")
    nota = f"{quien}, {filas}"
    if e["variantes"]:
        nota += f"; variantes: {', '.join(e['variantes'])}"
    if e["nota_celda"]:
        nota += f"; nota de la celda: {e['nota_celda']}"
    nota += (". Transcripción a ojo del 2026-08-31, pendiente de verificación "
             "contra la imagen (D11 #39). Vocabulario de comparación, no habla de agentes")
    return nota


def generar_modulo(out, referencia, colisiones):
    L = ['"""']
    L.append("CURIANA — Tabla A-2 de Oliver: la columna añú y el refuerzo lokono (D11)")
    L.append("=" * 72)
    L.append("")
    L.append("GENERADO por `minar_a2_swadesh.py` — no editar a mano; la fuente es")
    L.append("6-fusion/tabla_a2_transcripcion.yaml (transcripción a ojo, 2026-08-31,")
    L.append("pendiente de segunda pasada de Miguel contra la imagen).")
    L.append("")
    L.append("Implementa el rumbo de D11 (#39): rebalancear con lokono y abrir la")
    L.append("columna añú/paraujano (tenía CERO entradas del pariente costero más")
    L.append("cercano). Es vocabulario de COMPARACIÓN: alimenta la detección de fugas")
    L.append("de score_linguistico y las columnas del filtro fonotáctico. NO es habla")
    L.append("de agentes y no redefine el núcleo reconstruido (sesgo declarado del")
    L.append("cómputo de D11 — decisiones_tanda_2026-08-30.yaml §d11_rumbo).")
    L.append('"""')
    L.append("")
    for col, nombre in (("paraujano", "PARAUJANO_A2"), ("lokono", "LOKONO_A2")):
        L.append("")
        L.append(f"{nombre}: dict[str, dict] = {{")
        for forma, e in sorted(out[col].items()):
            L.append(f'    "{forma}": {{"es": "{e["es"]}", "fuente": "{e["fuente"]}", '
                     f'"categoria": "{e["categoria"]}", "notas": "{_nota(e, col)}"}},')
        L.append("}")
        L.append("")
    L.append("")
    L.append("# Lo que NO entró, con su motivo — formas ligadas, reconstrucciones (*),")
    L.append("# segmentos opcionales, dudosas y marcas de préstamo. Es material")
    L.append("# comparativo de primera; solo que no son lemas de lexicón.")
    L.append("REFERENCIA_A2: dict[str, list] = {")
    for col in ("paraujano", "lokono"):
        L.append(f'    "{col}": [')
        for n, gloss, frag, motivo in referencia[col]:
            frag_l = frag.replace('"', "'")
            L.append(f'        ("{n}", "{gloss}", "{frag_l}", "{motivo}"),')
        L.append("    ],")
    L.append("}")
    L.append("")
    L.append("")
    L.append("# Formas de la A-2 que YA son clave del lexicón: no se pisan, y la")
    L.append("# coincidencia es dato areal (el paraujano compartiendo forma con el")
    L.append("# núcleo es exactamente la señal que el hallazgo 1 de la transcripción")
    L.append("# describe para el guajiro).")
    L.append("COLISIONES_A2: list[tuple] = [")
    for col, n, gloss, forma in colisiones:
        L.append(f'    ("{col}", "{n}", "{gloss}", "{forma}"),')
    L.append("]")
    L.append("")
    L.append("TOTALES_A2 = {")
    L.append(f'    "paraujano": {len(out["paraujano"])},')
    L.append(f'    "lokono": {len(out["lokono"])},')
    L.append(f'    "referencia": {sum(len(v) for v in referencia.values())},')
    L.append(f'    "colisiones": {len(colisiones)},')
    L.append("}")
    L.append("")
    io.open(MODULO, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print(f"  → módulo generado: {MODULO}")


def informe(out, referencia, colisiones):
    print("=" * 78)
    print("  TABLA A-2 → LEXICÓN — la columna añú y el refuerzo lokono (D11)")
    print("=" * 78)
    for col in ("paraujano", "lokono"):
        print(f"\n── {col}: {len(out[col])} entradas nuevas")
        for forma, e in sorted(out[col].items()):
            filas = ",".join(str(n) for n, _ in e["filas"])
            print(f"    {forma:16} {e['es']:24} (fila {filas})")
    print(f"\n── referencia (no entran): paraujano "
          f"{len(referencia['paraujano'])} · lokono {len(referencia['lokono'])}")
    print(f"── colisiones con claves existentes ({len(colisiones)}):")
    for col, n, gloss, forma in colisiones:
        print(f"    {col:10} fila {n:>3} '{gloss}': {forma}")


if __name__ == "__main__":
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--generar-modulo", action="store_true")
    args = ap.parse_args()
    out, referencia, colisiones = minar()
    if args.generar_modulo:
        generar_modulo(out, referencia, colisiones)
    else:
        informe(out, referencia, colisiones)
