"""¿Qué entradas del lexicón descansan en material de OTRA polity o en la
etiqueta colonial "caribe"? (regla 4 · Oliver §3.8 y §3.2.4)

El corpus ya se auditó así (ver 6-fusion/issues-pendientes/issue-polity-en-el-
corpus.md). El lexicón tiene el mismo hueco y es cinco veces más grande: `fuente`
dice de QUÉ LENGUA es la palabra, nunca DE QUÉ POLITY es la fuente que la
atestigua.

    python auditar_polity_lexicon.py
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


# Topónimos que Oliver §3.7-3.8 asigna FUERA de la polity costera.
OTRA_POLITY = re.compile(
    r"barquisimeto|nueva segovia|yaracuy|turbio|nirgua|el tocuyo|carora|"
    r"qu[ií]bor|\bllanos\b|apure|acarigua|araure|siquisique|baragua", re.I)

# La etiqueta colonial: "caribe" en las crónicas es categoría de conquista,
# no filiación lingüística (§3.2.4). Solo cuenta cuando la fuente ES la crónica.
ETIQUETA_CARIBE = re.compile(r"\bcaribe\b|\bcaríbe\b|\bcanibal|\bcaníbal", re.I)


def main():
    V = L.VOCABULARIO_BASE
    otra, caribe = [], []
    for forma, d in V.items():
        if not isinstance(d, dict):
            continue
        blob = " ".join(str(d.get(k, "")) for k in
                        ("notas", "glosa_fuente", "sig", "es"))
        fuente = d.get("fuente", "?")
        m = OTRA_POLITY.findall(blob)
        if m:
            otra.append((forma, fuente, sorted({w.lower() for w in m}), blob))
        if ETIQUETA_CARIBE.search(blob):
            caribe.append((forma, fuente, blob))

    print(f"lexicón: {len(V)} entradas\n")

    print(f"── A · Atestiguadas por fuente de OTRA POLITY: {len(otra)}")
    porf = Counter(f for _, f, _, _ in otra)
    for f, n in porf.most_common():
        print(f"     {n:3}  fuente={f}")
    print()
    graves = [x for x in otra if "caquet" in str(x[1]).lower()]
    print(f"   🔴 de esas, {len(graves)} están marcadas como CAQUETÍO:")
    for forma, f, ws, blob in graves:
        print(f"     {forma:<14} [{f}]  {','.join(ws)}")
        print(f"        {blob[:110]}")

    print(f"\n── B · Mencionan la etiqueta colonial 'caribe': {len(caribe)}")
    porf2 = Counter(f for _, f, _ in caribe)
    for f, n in porf2.most_common(10):
        print(f"     {n:3}  fuente={f}")

    print("\n── C · Reparto de `fuente` (para dimensionar)")
    for f, n in Counter(d.get("fuente", "?") for d in V.values()
                        if isinstance(d, dict)).most_common(12):
        print(f"     {n:5}  {f}")


if __name__ == "__main__":
    _forzar_utf8()
    main()
