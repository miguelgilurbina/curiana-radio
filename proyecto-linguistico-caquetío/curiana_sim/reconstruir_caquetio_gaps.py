"""
CURIANA — Detección de huecos + reconstrucción comparativa del caquetío
=========================================================================
No es un agente LLM: aplica las reglas fonológicas ya validadas de
arahuaco_comparative.py (transducir / reconstruir_caquetio) sobre los
conceptos del lexicón que tienen forma en wayunaiki/lokono/taíno pero
NO tienen forma caquetío atestiguada ni reconstruida todavía.

No escribe nada en curiana_lexicon.py. Genera un archivo de revisión
(caquetio_reconstruido_candidatos.json) para que un humano apruebe qué
candidatos entran al lexicón vía aplicar_reconstruccion.py.

Uso:
    python reconstruir_caquetio_gaps.py
"""

import json
from collections import defaultdict

from curiana_lexicon import VOCABULARIO_BASE
from curiana_database import normalize_source_language
from arahuaco_comparative import reconstruir_caquetio

OUT_FILE = "caquetio_reconstruido_candidatos.json"

# Categorías de uso frecuente en la simulación: lo que los agentes realmente
# necesitan decir turno a turno. Fuera quedan flora/fauna exótica, etnonimia,
# vestimenta puntual, etc. — gaps reales pero de bajo impacto en el habla.
CATEGORIAS_PRIORITARIAS = {
    "verbos", "parentesco", "cuerpo", "numerales", "gramatica",
    "cosmos", "geografia",
}


def agrupar_por_significado() -> dict[str, dict[str, list[str]]]:
    """
    Agrupa palabras del lexicón por su glosa ("sig"), separadas por
    familia canónica. Ej: {"luna": {"wayunaiki": ["kashi"], "lokono": ["katsi"]}}
    """
    grupos: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for palabra, datos in VOCABULARIO_BASE.items():
        sig = (datos.get("sig") or "").strip().lower()
        if not sig:
            continue
        fam = normalize_source_language(datos.get("fuente", ""))
        grupos[sig][fam].append(palabra)
    return grupos


def categoria_representativa(sig: str) -> str:
    """Busca la 'categoria' (dominio semántico) de cualquier entrada con esta glosa."""
    for datos in VOCABULARIO_BASE.values():
        if (datos.get("sig") or "").strip().lower() == sig and datos.get("categoria"):
            return datos["categoria"]
    return ""


def es_pass_through(resultado: dict) -> bool:
    """
    True si la forma 'reconstruida' es literalmente idéntica a alguna de las
    palabras fuente usadas — significa que transducir() no tenía reglas para
    ese par de sonidos y devolvió la palabra de entrada sin cambios. No es
    una reconstrucción real, es la palabra wayunaiki/lokono/taíno disfrazada
    con un asterisco.
    """
    forma = resultado["proto_caquetio"].lstrip("*").lower()
    fuentes = resultado.get("fuentes_usadas", {})
    return any(
        fuente and fuente.lower() == forma
        for fuente in fuentes.values()
    )


def glosa_sospechosa(glosa: str) -> bool:
    """
    True si la glosa muestra señales de corrupción del diccionario fuente:
    múltiples cláusulas separadas por ';' o '-da', muy larga, o con palabras
    españolas sueltas que no deberían estar en una glosa ya en español
    (señal de que se concatenaron dos entradas del diccionario crudo).
    """
    g = glosa.strip()
    if ";" in g:
        return True
    if len(g) > 40:
        return True
    if g.count("(") != g.count(")"):
        return True  # paréntesis sin cerrar: fragmento de entrada concatenada
    return False


def detectar_huecos(grupos: dict, solo_prioritarias: bool = True) -> list[dict]:
    """
    Para cada significado sin forma caquetío (atestiguada o ya reconstruida),
    pero con al menos una forma en wayunaiki/lokono/taíno, corre la
    reconstrucción comparativa. Si solo_prioritarias=True, descarta
    significados fuera de CATEGORIAS_PRIORITARIAS (flora/fauna/etc.).
    """
    candidatos = []
    for sig, por_familia in grupos.items():
        tiene_caquetio = bool(por_familia.get("caquetío"))
        if tiene_caquetio:
            continue

        categoria = categoria_representativa(sig)
        if solo_prioritarias and categoria not in CATEGORIAS_PRIORITARIAS:
            continue

        if glosa_sospechosa(sig):
            continue

        lokono_word    = por_familia.get("lokono", [None])[0]
        wayunaiki_word = por_familia.get("wayunaiki", [None])[0]
        taino_word     = por_familia.get("taíno", [None])[0]

        if not (lokono_word or wayunaiki_word or taino_word):
            continue  # solo proto-arahuaco/kalinago/jirajaroide, sin base de transducción

        resultado = reconstruir_caquetio(
            lokono_word=lokono_word,
            wayunaiki_word=wayunaiki_word,
            taino_word=taino_word,
            glosa_es=sig,
        )
        resultado["categoria"] = categoria or "sin_categoria"
        resultado["fuentes_usadas"] = {
            "lokono": lokono_word,
            "wayunaiki": wayunaiki_word,
            "taíno": taino_word,
        }

        if es_pass_through(resultado):
            continue

        candidatos.append(resultado)

    return candidatos


def main():
    grupos = agrupar_por_significado()
    candidatos = detectar_huecos(grupos, solo_prioritarias=True)

    # Solo nos interesan los que SÍ produjeron una forma (no "*?")
    con_forma = [c for c in candidatos if c["proto_caquetio"] != "*?"]
    sin_forma = len(candidatos) - len(con_forma)

    con_forma.sort(key=lambda c: {"alta": 0, "media": 1, "ninguna": 2}.get(c["confianza"], 3))

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(con_forma, f, ensure_ascii=False, indent=2)

    print(f"=== RECONSTRUCCIÓN COMPARATIVA DEL CAQUETÍO ===")
    print(f"(filtrado a categorías prioritarias: {', '.join(sorted(CATEGORIAS_PRIORITARIAS))})")
    print(f"Significados sin forma caquetía con al menos 1 cognado: {len(candidatos)}")
    print(f"  Con forma reconstruida : {len(con_forma)}")
    print(f"  Sin forma (transducción falló): {sin_forma}")
    print()

    por_confianza = defaultdict(int)
    for c in con_forma:
        por_confianza[c["confianza"]] += 1
    for nivel in ("alta", "media", "ninguna"):
        if por_confianza[nivel]:
            print(f"  Confianza {nivel:<8}: {por_confianza[nivel]}")

    print()
    print(f"Candidatos guardados en: {OUT_FILE}")
    print("Revísalos y usa aplicar_reconstruccion.py para sumar los aprobados al lexicón.")
    print()
    print("Muestra (confianza alta, primeras 10):")
    for c in [c for c in con_forma if c["confianza"] == "alta"][:10]:
        print(f"  {c['proto_caquetio']:<20} = {c['glosa']:<30} ({c['nota']})")


if __name__ == "__main__":
    main()
