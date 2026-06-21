"""
CURIANA — Aplica los candidatos de reconstruccion comparativa al lexicón
==========================================================================
Lee caquetio_reconstruido_candidatos.json (generado por
reconstruir_caquetio_gaps.py) e inserta cada candidato en
curiana_lexicon.py con fuente "caquetío-reconstruido".

Maneja colisiones de clave:
  - Si la forma ya existe en el lexicón (de cualquier fuente), se descarta
    el candidato (no se sobrescribe nada existente).
  - Si dos candidatos reconstruidos llegan a la misma forma (homofonía
    esperable del método comparativo), se distinguen con sufijo -2, -3, ...

Uso:
    python aplicar_reconstruccion.py
"""

import json
import re
from collections import Counter

CANDIDATOS_FILE = "caquetio_reconstruido_candidatos.json"
LEXICON_FILE = "curiana_lexicon.py"
MARKER = "# -- FIN VOCABULARIO_BASE --"


def cargar_candidatos() -> list[dict]:
    with open(CANDIDATOS_FILE, encoding="utf-8") as f:
        return json.load(f)


def claves_existentes(contenido: str) -> set[str]:
    return set(re.findall(r'^    "([^"]+)":', contenido, re.MULTILINE))


def formatear_entrada(clave: str, candidato: dict) -> str:
    glosa = candidato["glosa"].replace('"', '\\"')
    nota = candidato["nota"].replace('"', '\\"')
    categoria = candidato.get("categoria", "sin_categoria")
    return (
        f'    "{clave}": {{"es": "{glosa}", "fuente": "caquetío-reconstruido", '
        f'"notas": "{nota}; confianza {candidato["confianza"]}", "categoria": "{categoria}"}},\n'
    )


def main():
    candidatos = cargar_candidatos()

    with open(LEXICON_FILE, encoding="utf-8") as f:
        contenido = f.read()

    if MARKER not in contenido:
        print(f"ERROR: marcador '{MARKER}' no encontrado en {LEXICON_FILE}")
        return

    existentes = claves_existentes(contenido)

    # Resolver colisiones internas entre candidatos (homofonía del método comparativo)
    formas = [c["proto_caquetio"].lstrip("*").lower() for c in candidatos]
    conteo = Counter(formas)

    contador_sufijo: dict[str, int] = {}
    nuevas_lineas = []
    insertadas = 0
    omitidas_existentes = 0

    for candidato, forma_base in zip(candidatos, formas):
        clave = forma_base
        if conteo[forma_base] > 1:
            contador_sufijo[forma_base] = contador_sufijo.get(forma_base, 0) + 1
            if contador_sufijo[forma_base] > 1:
                clave = f"{forma_base}-{contador_sufijo[forma_base]}"

        if clave in existentes:
            omitidas_existentes += 1
            continue

        nuevas_lineas.append(formatear_entrada(clave, candidato))
        existentes.add(clave)
        insertadas += 1

    if not nuevas_lineas:
        print("No hay candidatos nuevos para insertar.")
        return

    bloque = (
        "\n    # ── CAQUETÍO RECONSTRUIDO (método comparativo, ver arahuaco_comparative.py) ──\n"
        + "".join(nuevas_lineas)
    )
    contenido_nuevo = contenido.replace(MARKER, bloque.rstrip() + "\n\n    " + MARKER)

    with open(LEXICON_FILE, "w", encoding="utf-8") as f:
        f.write(contenido_nuevo)

    print(f"=== APLICADO ===")
    print(f"Insertadas: {insertadas}")
    print(f"Omitidas (clave ya existía en el lexicón): {omitidas_existentes}")
    print(f"Fuente asignada: caquetío-reconstruido")


if __name__ == "__main__":
    main()
