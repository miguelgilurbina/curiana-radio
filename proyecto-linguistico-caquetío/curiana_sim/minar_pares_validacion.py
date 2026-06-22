"""
CURIANA — Minería de pares de validación reales para el método comparativo
=============================================================================
PARES_VALIDACION en arahuaco_comparative.py tenía solo 14 pares elegidos a
mano. Este script busca pares OBJETIVOS en nuestro propio corpus: conceptos
donde existe una forma caquetío-ATESTIGUADA (dato histórico real, no
reconstruido) Y una forma conocida en otra lengua arahuaca (wayunaiki,
lokono, taíno) para el MISMO significado.

Esos son los únicos pares que sirven como prueba honesta del método: si
transducir(otra_lengua, "CQ") predice la forma caquetía REAL atestiguada,
la regla fonológica es buena evidencia, no circular.

No modifica nada automáticamente — reporta aciertos/fallos para revisión,
y deja un archivo de pares nuevos listos para sumar a PARES_VALIDACION
tras revisión humana.

Uso:
    python minar_pares_validacion.py
"""

import json
from collections import defaultdict

from curiana_lexicon import VOCABULARIO_BASE
from curiana_database import normalize_source_language
from arahuaco_comparative import transducir

OUT_FILE = "pares_validacion_minados.json"

# normalize_source_language() -> código de lengua usado por transducir()
FAMILIA_A_CODIGO = {
    "wayunaiki": "WY",
    "lokono": "LK",
    "taíno": "TN",
}


def agrupar_por_significado() -> dict[str, dict[str, list[tuple[str, str]]]]:
    """
    {sig: {familia: [(palabra, fuente_original), ...]}}
    Solo agrupa por familias relevantes: caquetío-atestiguado y las 3
    lenguas con reglas de transducción directas a CQ.
    """
    grupos: dict[str, dict[str, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for palabra, datos in VOCABULARIO_BASE.items():
        sig = (datos.get("sig") or "").strip().lower()
        if not sig:
            continue
        fuente = datos.get("fuente", "")
        fam = normalize_source_language(fuente)

        if fam == "caquetío" and "atestiguad" in fuente.lower():
            grupos[sig]["CQ_atestiguado"].append((palabra, fuente))
        elif fam in FAMILIA_A_CODIGO:
            grupos[sig][FAMILIA_A_CODIGO[fam]].append((palabra, fuente))
    return grupos


def distancia_simple(a: str, b: str) -> int:
    """Distancia de Levenshtein simple, sin dependencias externas."""
    a, b = a.lower(), b.lower()
    if a == b:
        return 0
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            cur = dp[j]
            dp[j] = prev if a[i - 1] == b[j - 1] else 1 + min(prev, dp[j - 1], dp[j])
            prev = cur
    return dp[n]


def main():
    grupos = agrupar_por_significado()

    pares_probados = []
    for sig, por_familia in grupos.items():
        atestiguadas = por_familia.get("CQ_atestiguado")
        if not atestiguadas:
            continue
        forma_real, fuente_cq = atestiguadas[0]

        for codigo in ("WY", "LK", "TN"):
            for forma_origen, fuente_origen in por_familia.get(codigo, []):
                predicha = transducir(forma_origen, codigo, "CQ", asterisk=False)
                if not predicha:
                    continue
                dist = distancia_simple(predicha, forma_real)
                pares_probados.append({
                    "glosa": sig,
                    "origen_codigo": codigo,
                    "forma_origen": forma_origen,
                    "fuente_origen": fuente_origen,
                    "forma_cq_real": forma_real,
                    "fuente_cq": fuente_cq,
                    "forma_predicha": predicha,
                    "distancia": dist,
                    "exacto": dist == 0,
                })

    if not pares_probados:
        print("No se encontraron pares objetivos (¿cambió el esquema de fuentes?).")
        return

    exactos = [p for p in pares_probados if p["exacto"]]
    cercanos = [p for p in pares_probados if 0 < p["distancia"] <= 2]
    lejanos = [p for p in pares_probados if p["distancia"] > 2]

    print("=== MINERÍA DE PARES DE VALIDACIÓN (datos reales, no elegidos a mano) ===\n")
    print(f"Pares objetivos encontrados: {len(pares_probados)}")
    print(f"  Exactos (distancia 0):        {len(exactos)}  ({len(exactos)/len(pares_probados)*100:.0f}%)")
    print(f"  Cercanos (distancia 1-2):     {len(cercanos)}  ({len(cercanos)/len(pares_probados)*100:.0f}%)")
    print(f"  Lejanos (distancia >2):       {len(lejanos)}  ({len(lejanos)/len(pares_probados)*100:.0f}%)")
    print()

    if exactos:
        print("Muestra de aciertos exactos:")
        for p in exactos[:10]:
            print(f"  {p['origen_codigo']} {p['forma_origen']:<15} -> {p['forma_predicha']:<15} "
                  f"= CQ real '{p['forma_cq_real']}' ({p['glosa']})")
        print()

    if lejanos:
        print("Casos lejanos (revisar regla de correspondencia o el dato mismo):")
        for p in lejanos[:10]:
            print(f"  {p['origen_codigo']} {p['forma_origen']:<15} -> predijo '{p['forma_predicha']}' "
                  f"pero CQ real es '{p['forma_cq_real']}' ({p['glosa']}, dist={p['distancia']})")
        print()

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(pares_probados, f, ensure_ascii=False, indent=2)
    print(f"Detalle completo guardado en: {OUT_FILE}")
    print("Revisa los 'lejanos' para refinar arahuaco_comparative.py;")
    print("los 'exactos' son candidatos honestos para sumar a PARES_VALIDACION.")


if __name__ == "__main__":
    main()
