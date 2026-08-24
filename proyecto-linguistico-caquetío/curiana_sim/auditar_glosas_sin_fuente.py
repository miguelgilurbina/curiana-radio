"""¿Cuántas glosas del lexicón no tienen fuente que las sostenga?

Nace de un patrón encontrado el 2026-08-24: `tara` ('venado' contra tres fuentes
que dicen langosta), `corie` ('choza' contra tres que dicen armadillo) y `mene`
('petróleo' contra tres que dicen brea) resultaron ser EL MISMO CASO — una glosa
activa cuya propia nota admite que no tiene fuente localizada, sostenida contra
fuentes que dicen otra cosa.

D10 los llamó "los tres conflictos". Nadie ha contado si son tres o más. Esto
lo cuenta, para saber si la fusión es una tarde o una campaña.

    python auditar_glosas_sin_fuente.py
"""
import io
import re
import sys
from collections import Counter

import curiana_lexicon as L


def _forzar_utf8():
    """La consola de Windows es cp1252 y revienta con « o ü."""
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                      errors="replace")


# Lo que una nota dice cuando el proyecto YA detectó el problema.
CONFESION = [
    (re.compile(r"no tiene fuente localizada|sin fuente localizada", re.I),
     "glosa sin fuente localizada"),
    (re.compile(r"CONFLICTO DE GLOSA ABIERTO", re.I),
     "conflicto de glosa declarado abierto"),
    (re.compile(r"la entrada NO se reescribe|no se toca aquí", re.I),
     "conflicto aplazado a propósito"),
    (re.compile(r"discrepancia a resolver|glosa en disputa|en disputa", re.I),
     "glosa en disputa"),
    (re.compile(r"\bdeuda\b|sin-procedencia|sin procedencia", re.I),
     "deuda de procedencia declarada"),
    (re.compile(r"atribución débil|filiación dudosa|duda del origen", re.I),
     "filiación dudosa"),
    (re.compile(r"pendiente:", re.I),
     "pendiente anotado"),
]

# Entradas SIN notas: no confiesan nada porque no dicen nada.
def main():
    V = L.VOCABULARIO_BASE
    marcadas, motivos = {}, Counter()
    sin_notas = []
    for forma, d in V.items():
        if not isinstance(d, dict):
            continue
        notas = str(d.get("notas") or "")
        glosa_f = str(d.get("glosa_fuente") or "")
        blob = notas + " " + glosa_f
        if not notas.strip():
            sin_notas.append((forma, d.get("fuente", "?")))
            continue
        for pat, etiqueta in CONFESION:
            if pat.search(blob):
                marcadas.setdefault(forma, []).append(etiqueta)
                motivos[etiqueta] += 1

    print(f"lexicón: {len(V)} entradas\n")
    print(f"── A · Entradas cuya nota CONFIESA un problema: {len(marcadas)}")
    for etiqueta, n in motivos.most_common():
        print(f"     {n:4}  {etiqueta}")

    print(f"\n── B · Las más graves: glosa sin fuente localizada O conflicto abierto")
    graves = {f: m for f, m in marcadas.items()
              if any("sin fuente localizada" in x or "conflicto de glosa" in x
                     for x in m)}
    print(f"     {len(graves)} entradas\n")
    for f in sorted(graves):
        d = V[f]
        print(f"     {f:<14} [{d.get('fuente','?'):<22}] {str(d.get('sig') or d.get('es'))[:46]}")

    print(f"\n── C · Entradas SIN campo `notas` (no confiesan porque no dicen nada)")
    print(f"     {len(sin_notas)} de {len(V)}")
    por_fuente = Counter(f for _, f in sin_notas)
    for fu, n in por_fuente.most_common(8):
        print(f"     {n:5}  {fu}")


if __name__ == "__main__":
    _forzar_utf8()
    main()
