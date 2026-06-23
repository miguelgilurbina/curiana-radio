"""
Exporta el lexicon completo (1703 palabras) a un seed estatico para
/simulador/lexicon en Curiana Radio -- mismo espiritu evergreen que el
resto de la seccion: sin Supabase en el navegador.

Pagina con .range() porque PostgREST trunca a max_rows (1000) -- ver la
nota en CLAUDE.md. Sin esto se repite el mismo bug que tenia la pagina
vieja (que ademas apuntaba al proyecto cloud equivocado).

Uso: python export_lexicon_seed.py
"""
import json
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from curiana_database import CurianaDB

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "content", "simulador", "lexicon.json"
)


def main():
    db = CurianaDB()
    desde = 0
    todas = []
    while True:
        page = (
            db.client.table("lexicon")
            .select("id, word, meaning, category, source_language, attested, source_ref")
            .order("word")
            .range(desde, desde + 999)
            .execute()
            .data
        )
        todas.extend(page)
        if len(page) < 1000:
            break
        desde += 1000

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"palabras": todas}, f, ensure_ascii=False, indent=2)

    print(f"{len(todas)} palabras exportadas -> {os.path.abspath(OUT_PATH)}")


if __name__ == "__main__":
    main()
