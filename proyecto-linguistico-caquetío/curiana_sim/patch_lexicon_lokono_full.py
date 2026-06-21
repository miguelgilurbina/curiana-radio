#!/usr/bin/env python3
"""
patch_lexicon_lokono_full.py
Aplica el patch completo de Lokono/Arawak a curiana_lexicon.py.
Fuentes: Goeje (1928), Brinton (1871), Pet (1987/2011), Taylor (1977)
~115 entradas nuevas — fonologia, grammatica, cognados caquetios.
Correr desde curiana_sim/ con lokono_full_lexicon.json en la misma carpeta.
"""

import re, json, os, sys

LEXICON_FILE = "curiana_lexicon.py"
JSON_FILE    = os.path.join(os.path.dirname(__file__), "lokono_full_lexicon.json")

def load_new_entries():
    if not os.path.exists(JSON_FILE):
        print(f"ERROR: No se encuentra {JSON_FILE}")
        print("Copia lokono_full_lexicon.json a curiana_sim/ antes de correr.")
        sys.exit(1)
    with open(JSON_FILE, encoding="utf-8") as f:
        return json.load(f)

def format_entry(word, data):
    es      = data["es"].replace('"', '\\"')
    fuente  = data["fuente"]
    notas   = data["notas"].replace('"', '\\"')
    cat     = data["categoria"]
    return (
        f'    "{word}": {{\n'
        f'        "es": "{es}",\n'
        f'        "fuente": "{fuente}",\n'
        f'        "notas": "{notas}",\n'
        f'        "categoria": "{cat}"\n'
        f'    }},\n'
    )

def patch():
    if not os.path.exists(LEXICON_FILE):
        print(f"ERROR: No se encuentra {LEXICON_FILE} en {os.getcwd()}")
        sys.exit(1)

    with open(LEXICON_FILE, encoding="utf-8") as f:
        original = f.read()

    all_new      = load_new_entries()
    existing_keys = set(re.findall(r'"([^"]+)"\s*:\s*\{', original))
    new_entries  = {k: v for k, v in all_new.items() if k not in existing_keys}

    if not new_entries:
        print("No hay entradas nuevas — todas ya existen en el lexicon.")
        return

    # Agrupar por categoria
    by_cat = {}
    for word, data in new_entries.items():
        cat = data["categoria"]
        by_cat.setdefault(cat, []).append(word)

    # Encontrar punto de insercion
    MARKERS = [
        "\n# -- FIN VOCABULARIO_BASE --",
        "\n# -- FIN VOCABULARIO BASE --",
        "\n# ── FIN VOCABULARIO_BASE ──",
        "\n# ─── FIN ───",
    ]
    block_end = None
    for marker in MARKERS:
        if marker in original:
            block_end = original.index(marker)
            break
    if block_end is None:
        # Ultimo recurso: antes del cierre del dict
        if "\n}" in original:
            block_end = original.rindex("\n}")
        else:
            print("ERROR: No se encontro el marcador de fin en curiana_lexicon.py")
            sys.exit(1)

    # Construir bloque nuevo
    new_block = "\n    # -- LOKONO COMPLETO (Goeje 1928; Brinton 1871; Pet 1987) -- {n} entradas --\n".format(
        n=len(new_entries)
    )

    for cat in sorted(by_cat.keys()):
        words = sorted(by_cat[cat])
        new_block += f"\n    # [{cat.upper()}]\n"
        for word in words:
            new_block += format_entry(word, new_entries[word])

    # Insertar
    updated = original[:block_end] + new_block + original[block_end:]

    # Backup
    with open(LEXICON_FILE + ".bak", "w", encoding="utf-8") as f:
        f.write(original)

    with open(LEXICON_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    total_new = len(new_entries)
    total_skipped = len(all_new) - total_new

    print(f"=== PATCH LOKONO COMPLETO ===")
    print(f"Entradas insertadas : {total_new}")
    print(f"Entradas ya existentes (saltadas): {total_skipped}")
    print(f"Distribucion por categoria:")
    for cat in sorted(by_cat.keys()):
        print(f"  {cat:<20} : {len(by_cat[cat])}")
    print(f"Backup guardado en  : {LEXICON_FILE}.bak")
    print("Exito.")

if __name__ == "__main__":
    patch()
