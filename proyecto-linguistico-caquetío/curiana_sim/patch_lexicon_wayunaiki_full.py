"""
patch_lexicon_wayunaiki_full.py
================================
Adds ALL 770 Wayunaiki entries from Captain & Captain (2005) to VOCABULARIO_BASE.
Source: Captain & Captain (2005) Diccionario Basico Ilustrado Wayuunaiki-Espanol.
        1,071 raw entries extracted. After filtering:
          - 187 cross-references (see_es) skipped
          - 25  Spanish loanwords skipped
          - 89  already in patch_lexicon_wayunaiki_captain2005.py
          = 770 new entries to add

Each entry includes a proto-caquetio phonological reconstruction in 'notas',
computed by the Wayunaiki->Proto-Caquetio transducer (wayunaiki_phonology.py).

Categories:
  verbos       326   comunicacion  43   gramatica  43
  cuerpo        58   fauna         43   utiles     51
  parentesco    34   tiempo        38   flora      26
  geografia     22   cosmos        16   ritual     11
  adjetivos     10   alimentos      9   otros      28
  sentimientos   7   jerarquia      5

Run from curiana_sim/ directory:
    python patch_lexicon_wayunaiki_full.py

Requires:
    wayunaiki_full_lexicon.json  (in same directory as this script)
"""

import re, sys, os, json
from collections import defaultdict

SOURCE = "Captain & Captain (2005) Diccionario Basico Ilustrado Wayuunaiki-Espanol"
LEXICON_PATH = "curiana_lexicon.py"
JSON_PATH = os.path.join(os.path.dirname(__file__), "wayunaiki_full_lexicon.json")


def load_new_entries():
    if not os.path.exists(JSON_PATH):
        # Try same directory as script
        alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wayunaiki_full_lexicon.json")
        if os.path.exists(alt):
            json_path = alt
        else:
            print("ERROR: wayunaiki_full_lexicon.json not found.")
            print("  Expected at: " + JSON_PATH)
            sys.exit(1)
    else:
        json_path = JSON_PATH

    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def format_entry(word, data):
    es    = data["es"].replace('"', "'")
    notas = data["notas"].replace('"', "'")
    return (
        '    "' + word + '": {\n'
        '        "es": "' + es + '",\n'
        '        "fuente": "wayunaiki",\n'
        '        "notas": "' + notas + '",\n'
        '        "categoria": "' + data["categoria"] + '",\n'
        '    },\n'
    )


def patch():
    # Load curiana_lexicon.py
    try:
        with open(LEXICON_PATH, encoding="utf-8") as f:
            original = f.read()
    except FileNotFoundError:
        print("ERROR: " + LEXICON_PATH + " not found. Run from curiana_sim/ directory.")
        sys.exit(1)

    # Load the 770 entries from JSON
    all_new = load_new_entries()

    # Find existing keys in lexicon
    existing_keys = set(re.findall(r'"([^"]+)"\s*:\s*\{', original))
    new_entries = {k: v for k, v in all_new.items() if k not in existing_keys}
    skipped = len(all_new) - len(new_entries)

    if not new_entries:
        print("All entries already present in curiana_lexicon.py.")
        return

    # Stats by category
    by_cat = defaultdict(list)
    for word, data in new_entries.items():
        by_cat[data["categoria"]].append(word)

    print("Source: " + SOURCE)
    print("Wayunaiki entries to add: " + str(len(new_entries))
          + "  (skipped as duplicates: " + str(skipped) + ")")
    print()
    print("By category:")
    for cat, words in sorted(by_cat.items(), key=lambda x: -len(x[1])):
        print("  [" + cat + "] " + str(len(words)))
    print()

    answer = input("Proceed? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        return

    # Find insertion point
    marker = "\n# -- FIN VOCABULARIO_BASE --"
    if marker in original:
        block_end = original.index(marker)
    else:
        # Try alternate markers
        for alt in ["\n# ── FIN VOCABULARIO_BASE ──", "\n}"]:
            if alt in original:
                block_end = original.rindex(alt)
                break
        else:
            block_end = original.rfind("\n}")

    # Build block organized by category
    new_block = "\n    # -- WAYUNAIKI COMPLETO (Captain & Captain 2005) -- 770 entradas --\n"
    for cat in sorted(by_cat.keys()):
        words_in_cat = by_cat[cat]
        new_block += "\n    # [" + cat + "]\n"
        for word in sorted(words_in_cat):
            new_block += format_entry(word, new_entries[word])

    patched = original[:block_end] + new_block + original[block_end:]

    with open(LEXICON_PATH, "w", encoding="utf-8") as f:
        f.write(patched)

    current_way = original.count('"fuente": "wayunaiki"')
    print()
    print("Done! Wayunaiki entries: " + str(current_way) + " -> " + str(current_way + len(new_entries)))
    print("Total lexicon entries now: ~" + str(original.count('"fuente":') + len(new_entries)))
    print()
    print("Next steps:")
    print("  1. Verify: python -c \"from curiana_lexicon import VOCABULARIO_BASE; print(len(VOCABULARIO_BASE))\"")
    print("  2. Seed:   python -c \"from curiana_database import get_db; db=get_db(); print(db.seed_lexicon())\"")
    print("  3. Deploy: npx vercel --prod")


if __name__ == "__main__":
    patch()
