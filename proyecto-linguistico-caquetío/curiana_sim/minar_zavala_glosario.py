"""
CURIANA — Minería del glosario de Zavala Reyes (2015)
=====================================================

Extrae las 288 entradas numeradas del glosario de:

    Zavala Reyes, Miguel Enrique (2015). "Palabras vivas de una lengua muerta:
    legado arawak-caquetío". Boletín Antropológico, año 33, n.º 89, pp. 58-76.
    Universidad de Los Andes, Mérida.
    → fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf

y las clasifica en TIERS de importación al lexicón, cruzándolas con
`VOCABULARIO_BASE` para detectar cuáles ya están y cuáles faltan.

MOTIVO (auditoría 2026-07-20): el proyecto tenía solo ~62 de las 288 entradas
del glosario, es decir ~22% de su fuente atestiguada central. Faltaban incluso
palabras que dan nombre a agentes de la simulación (buio, bagre, cunaro,
guaranaro, dara, naure) y ocho AFIJOS atestiguados ausentes de las reglas
morfológicas.

Uso:
    python minar_zavala_glosario.py              # informe por tiers
    python minar_zavala_glosario.py --json out.json
    python minar_zavala_glosario.py --python     # emite entradas listas para pegar

NO modifica curiana_lexicon.py: emite una propuesta para revisión humana, en la
misma disciplina que retag_nucleo_fundacional.py y minar_pares_validacion.py.
"""

import argparse
import json
import os
import re
import sys
import unicodedata

PDF_PATH = os.path.join(
    os.path.dirname(__file__), "..", "fuentes_caquetios",
    "Palabras Vivas de una Lengua Muerta.pdf",
)

# Pie de página que se repite en cada plana y rompe el parseo de la definición.
_FOOTER = re.compile(
    r"Bolet[íi]n Antropol[óo]gico.*?(?:Investigaciones\.|pp\. 58-76\.|- \d+|\d+ -)",
    re.IGNORECASE | re.DOTALL,
)

# "12. Apopo (AM): jefe de parcialidad" · "146.- Guata (AM): Planta" · "191- Paragua (GC): Mar"
# Las siglas del compilador son opcionales (p. ej. "256. Tupure: Siembra de cacao").
_ENTRADA = re.compile(
    r"(?<!\d)(\d{1,3})\s*[.\-]+\s*"                    # número
    r"([A-ZÁÉÍÓÚÑÜ][^:()\d]{0,45}?)\s*"                # lema(s)
    r"((?:\([A-Za-z]{1,4}\)\s*)*)"                     # siglas del compilador (opcional)
    r":\s*"
    r"(.{0,180}?)"                                     # definición
    r"(?=\s*(?<!\d)\d{1,3}\s*[.\-]+\s*[A-ZÁÉÍÓÚÑÜ]|$)"
)

# Compiladores citados por Zavala (p. 64).
SIGLAS = {
    "PMA": "Pedro Manuel Arcaya", "HB": "Adrián Hernández Baño",
    "E": "Juan Esteves", "AM": "Angulo Molina", "A": "Lisandro Alvarado",
    "GC": "Galeotto Cey", "CGB": "Carlos González Batista",
    "AAM": "Antonio Arellano Moreno", "HP": "Aníbal Hill Peña",
}


# ══════════════════════════════════════════════════════════════════════
# Clasificación en tiers
# ══════════════════════════════════════════════════════════════════════

# T1 — AFIJOS atestiguados. El hallazgo de mayor valor: amplían lo que los
# agentes pueden CONSTRUIR, no solo lo que pueden nombrar.
AFIJOS = {
    "aima": ("-aima", "desinencia de abundancia"),
    "coa": ("-coa", "desinencia de abundancia"),
    "dito": ("dito", "distintivo de nombres colectivos de abundancia"),
    "ima": ("-ima", "desinencia: humedad, quebrada"),
    "iro": ("-iro", "desinencia de diminutivo"),
    "toda": ("toda", "desinencia"),
    "ubana": ("-ubana", "desinencia"),
    "uru": ("-uru", "desinencia"),
    "uco": ("-uco", "sufijo: quebrada, cauce"),
    "uto": ("-uto", "sufijo: quebrada, cauce"),
}

# T2 — palabras que el proyecto YA USA (nombres de agente) sin tenerlas en el
# lexicón: el scorer no las cuenta como caquetío hoy.
NOMBRES_DE_AGENTE = {
    "buio", "bagre", "cunaro", "guaranaro", "dara", "naure", "moruy",
    "cuna", "paugis", "corie", "chiriguare", "watapana", "kadushi",
    "saruro", "maure", "tari", "piru", "kori", "taku", "suba",
}

# T5 — antropónimos y gentilicios: valiosos para el canon, NO para el habla.
# Se detectan por la propia definición de Zavala.
_RE_ANTROPONIMO = re.compile(
    r"nombre propio|apellido|cacique|nombre de cacique|ind[íi]gena de|"
    r"indio caquet[íi]o|poblaci[óo]n ind[íi]gena", re.IGNORECASE)

# T5b — topónimos: lugar, sitio, población, río con nombre.
_RE_TOPONIMO = re.compile(
    r"^\s*(poblaci[óo]n|pueblo|sitio del estado|asiento ind[íi]gena|"
    r"serran[íi]a de coro|caser[íi]o)", re.IGNORECASE)

# T6 — Zavala (o sus compiladores) marcan la voz como de OTRA lengua.
_RE_OTRA_LENGUA = re.compile(
    r"cumanagota|caribe\b|chaima|es voz (?:de|del)", re.IGNORECASE)

# FLAG — homógrafos con español corriente: si entran al léxico activo, un texto
# en español que los use puntuaría como caquetío. Se importan marcados para que
# el scoring los resuelva POR CONTEXTO (mismo mecanismo que ya usa "para").
HOMOGRAFOS_ES = {
    "bagre", "sabana", "cabana", "cana", "enea", "guaca", "coca", "hay",
    "dato", "apo", "tuba", "ruba", "supi", "quiba", "quiva", "guama",
    "caraota", "icoroata", "samuro", "taque", "taques", "cocuy", "yaro",
    "sigua", "carama", "guata", "guay", "koro", "ure", "aca", "capo",
}

# EXCLUIR — curación a mano tras revisar las listas heurísticas (2026-07-20).
# El tier automático acierta en la mayoría, pero deja pasar topónimos modernos
# de Falcón/Lara cuya "definición" es la etimología del lugar, no una palabra de
# uso corriente. Entran al corpus como topónimos, NO al vocabulario del habla:
# un agente no dice "Bariquisimeto" para decir "río turbio".
EXCLUIR_DEL_HABLA = {
    # topónimos modernos documentados (Falcón, Lara, Yaracuy, islas)
    "bariquisimeto", "paraguana", "dabajuro", "cabudare", "bobare", "doaca",
    "cumarebo", "acatute", "poapao", "yacare", "yacarebacoa", "yaracuy",
    "adicora", "jadicuar", "aruba", "curiana", "coro", "moruy", "misoa",
    "sazaribacoa", "guacaubana", "alaurima", "barisi", "pachacuare",
    "quibacoas", "siguruba", "dabudare", "guacurebo", "guadabacoa",
    "guamabatriba", "adabacoa", "alcaboa", "aburi", "aricula", "taratarare",
    "turijerebo", "jurijurebo", "capadare", "guasare", "cemirucos",
    # gentilicios y etnónimos (canon, no habla)
    "caquetio", "yaruca", "iboa", "parotaima", "tabicure", "todarahuato",
    "xirahara", "chorota",
    # glosa demasiado incierta para usarse en una frase
    "coroque",      # "Árbol de ¿?" — la propia fuente no sabe
    "tarai",        # "Garipial o caripial" — glosa circular
    "guanajio",     # variante ortográfica de guanajo
}


def norm(s: str) -> str:
    """minúsculas sin acentos, para comparar formas."""
    s = (s or "").lower().strip()
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def extraer(pdf_path: str = PDF_PATH) -> list[dict]:
    """Parsea el glosario del PDF. Devuelve [{num, lemas, siglas, definicion}]."""
    try:
        import pypdf
    except ImportError:
        sys.exit("Falta pypdf: pip install pypdf")

    r = pypdf.PdfReader(pdf_path)
    texto = "\n".join((p.extract_text() or "") for p in r.pages)
    plano = re.sub(r"-\n", "", texto)           # une palabras cortadas por guion
    plano = re.sub(r"\s*\n\s*", " ", plano)
    plano = _FOOTER.sub(" ", plano)             # quita pies de página repetidos

    vistos: dict[int, dict] = {}
    for m in _ENTRADA.finditer(plano):
        num = int(m.group(1))
        if num in vistos or not (1 <= num <= 288):
            continue
        lemas_raw = m.group(2).strip().rstrip(".,;")
        siglas = re.findall(r"\(([A-Za-z]{1,4})\)", m.group(3) or "")
        definicion = " ".join(m.group(4).split()).strip(" .;")
        # "Aco. Aca" / "Baja, baba" / "Cuiva. Kiba" → varias formas del mismo lema
        lemas = [l.strip() for l in re.split(r"[.,]|\bo\b", lemas_raw) if l.strip()]
        lemas = [l for l in lemas if len(l) > 1]
        if not lemas or not definicion:
            continue
        vistos[num] = {
            "num": num, "lemas": lemas, "siglas": siglas,
            "definicion": definicion[:160],
        }
    return [vistos[k] for k in sorted(vistos)]


def clasificar(entradas: list[dict]) -> dict:
    """Cruza con VOCABULARIO_BASE y reparte en tiers."""
    from curiana_lexicon import VOCABULARIO_BASE
    from curiana_database import normalize_source_language

    # IDEMPOTENCIA: curiana_lexicon.py fusiona GLOSARIO_ZAVALA en VOCABULARIO_BASE.
    # Si comparásemos contra el resultado de esa fusión, en la segunda ejecución
    # el script vería sus propias palabras como "ya presentes" y generaría un
    # módulo vacío. Se excluyen para medir siempre contra el lexicón PREVIO.
    try:
        from lexicon_zavala import GLOSARIO_ZAVALA as _YA_IMPORTADO
    except ImportError:
        _YA_IMPORTADO = {}

    lex_idx = {}
    for w, e in VOCABULARIO_BASE.items():
        if w in _YA_IMPORTADO:
            continue
        lex_idx.setdefault(norm(w), (w, normalize_source_language(e.get("fuente", ""))))

    tiers = {
        "T1_afijos": [], "T2_nombres_agente": [], "T3_concreto": [],
        "T4_abstracto": [], "T5_toponimo": [], "T5b_antroponimo": [],
        "T6_descartado": [], "YA_EN_LEXICON": [], "MAL_ETIQUETADO": [],
    }

    # Heurística T3/T4: definición con marca de cosa concreta vs. acción/cualidad
    re_concreto = re.compile(
        r"[áa]rbol|planta|arbusto|hierba|yerba|palmera|cact|fruto|semilla|"
        r"ave|p[áa]jaro|pez|peces|animal|insecto|hormiga|avispa|abeja|"
        r"serpiente|lagart|molusco|concha|caracol|cangrejo|zorro|mono|"
        r"murci[ée]lago|paloma|cotorra|lechuza|r[íi]o|quebrada|cerro|"
        r"sierra|serran[íi]a|monte|sabana|llano|arena|arenal|piedra|"
        r"barro|salina|mar\b|agua|camino|senda|casa|olla|tinaja|budare|"
        r"fibra|madera|palo|ma[íi]z|comida|licor|vino|sal\b|conuco|siembra|"
        r"tierra|bosque|arboleda|punta|playa|cueva|hoguera|tea", re.IGNORECASE)

    for e in entradas:
        lemas_n = [norm(l) for l in e["lemas"]]
        d = e["definicion"]

        hit = next(((l, *lex_idx[norm(l)]) for l in e["lemas"] if norm(l) in lex_idx), None)
        if hit:
            lema, forma_lex, fuente = hit
            reg = {**e, "forma_lexicon": forma_lex, "fuente_actual": fuente}
            tiers["YA_EN_LEXICON"].append(reg)
            if fuente != "caquetío":
                tiers["MAL_ETIQUETADO"].append(reg)
            continue

        e = {**e, "homografo_es": any(l in HOMOGRAFOS_ES for l in lemas_n)}

        if any(l in EXCLUIR_DEL_HABLA for l in lemas_n):
            tiers["T5_toponimo"].append({**e, "motivo": "curación manual: topónimo/etnónimo o glosa incierta"})
        elif any(l in AFIJOS for l in lemas_n):
            afijo = next(AFIJOS[l] for l in lemas_n if l in AFIJOS)
            tiers["T1_afijos"].append({**e, "afijo": afijo[0], "glosa_afijo": afijo[1]})
        elif _RE_OTRA_LENGUA.search(d):
            tiers["T6_descartado"].append({**e, "motivo": "Zavala/compilador la marca de otra lengua"})
        elif any(l in NOMBRES_DE_AGENTE for l in lemas_n):
            tiers["T2_nombres_agente"].append(e)
        elif _RE_ANTROPONIMO.search(d):
            tiers["T5b_antroponimo"].append(e)
        elif _RE_TOPONIMO.search(d):
            tiers["T5_toponimo"].append(e)
        elif re_concreto.search(d):
            tiers["T3_concreto"].append(e)
        else:
            tiers["T4_abstracto"].append(e)

    return tiers


def informe(tiers: dict, entradas: list[dict]):
    total = len(entradas)
    ya = len(tiers["YA_EN_LEXICON"])
    print("=" * 78)
    print("  GLOSARIO ZAVALA REYES 2015 — auditoría de importación")
    print("=" * 78)
    print(f"  entradas parseadas del PDF: {total}")
    print(f"  ya presentes en VOCABULARIO_BASE: {ya}  ({100*ya//max(total,1)}%)")
    print(f"  ausentes: {total - ya}")
    print()
    orden = ["T1_afijos", "T2_nombres_agente", "T3_concreto", "T4_abstracto",
             "T5_toponimo", "T5b_antroponimo", "T6_descartado"]
    etiquetas = {
        "T1_afijos": "AFIJOS atestiguados (→ reglas morfológicas + léxico)",
        "T2_nombres_agente": "Palabras que YA usa el proyecto (nombres de agente)",
        "T3_concreto": "Sustantivos concretos (fauna, flora, paisaje, técnica)",
        "T4_abstracto": "Verbos, cualidades y abstractos",
        "T5_toponimo": "Topónimos (→ caquetío/topónimo, fuera del habla)",
        "T5b_antroponimo": "Antropónimos y gentilicios (canon, NO léxico activo)",
        "T6_descartado": "Descartados (otra lengua según la propia fuente)",
    }
    for t in orden:
        items = tiers[t]
        print(f"── {t}: {len(items):3}  {etiquetas[t]}")
        for e in items[:6]:
            marca = " ⚠es" if e.get("homografo_es") else ""
            print(f"     {'/'.join(e['lemas']):22}{marca:5} {e['definicion'][:52]}")
        if len(items) > 6:
            print(f"     … y {len(items)-6} más")
        print()
    n_hom = sum(1 for t in orden for e in tiers[t] if e.get("homografo_es"))
    print(f"  ⚠ homógrafos con español (importar con nota): {n_hom}")
    if tiers["MAL_ETIQUETADO"]:
        print(f"\n  ⚠ presentes pero NO etiquetadas 'caquetío' ({len(tiers['MAL_ETIQUETADO'])}):")
        for e in tiers["MAL_ETIQUETADO"]:
            print(f"     {e['lemas'][0]:18} lexicón='{e['forma_lexicon']}' = {e['fuente_actual']}"
                  f"  | Zavala: {e['definicion'][:40]}")


_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS; el resto, sust


def _entrada_py(e: dict, tier: str, indent: str = "    ") -> str:
    forma = norm(e["lemas"][0])
    sig = e["definicion"].replace('"', "'").replace("\\", "")[:78]
    sig = (sig[0].lower() + sig[1:]) if sig else sig
    siglas = "+".join(e["siglas"]) or "s/sigla"
    nota = f"Zavala Reyes 2015 #{e['num']} ({siglas})"
    if e.get("homografo_es"):
        nota += "; homógrafo con español — resuelto por contexto en score_linguistico"
    variantes = [norm(l) for l in e["lemas"][1:]]
    if variantes:
        nota += f"; variantes: {', '.join(variantes)}"
    cat = _CAT_POR_TIER.get(tier, "sust")
    pad = " " * max(1, 14 - len(forma))
    return (f'{indent}"{forma}":{pad}{{"sig": "{sig}", "cat": "{cat}", '
            f'"fuente": "caquetío-atestiguado", "notas": "{nota}"}},')


def generar_modulo(tiers: dict, ruta: str):
    """Escribe lexicon_zavala.py con la propuesta de importación por tiers."""
    L = []
    L.append('"""')
    L.append("CURIANA — Glosario de Zavala Reyes (2015), importado por tiers")
    L.append("=" * 62)
    L.append("")
    L.append("GENERADO por `minar_zavala_glosario.py` — no editar a mano: reejecutar el")
    L.append("script si cambia la curación. Fuente:")
    L.append("")
    L.append('    Zavala Reyes, Miguel Enrique (2015). "Palabras vivas de una lengua')
    L.append('    muerta: legado arawak-caquetío". Boletín Antropológico 33(89), pp. 58-76.')
    L.append("    Universidad de Los Andes. → fuentes_caquetios/")
    L.append("")
    L.append("MOTIVO (auditoría 2026-07-20): el lexicón contenía solo ~66 de las 286")
    L.append("entradas del glosario (23%). Faltaban palabras que el propio proyecto usa")
    L.append("como nombre de agente (buio, bagre, cunaro, guaranaro, dara, naure) — que")
    L.append("por tanto NO puntuaban como caquetío — y ocho afijos atestiguados ausentes")
    L.append("de las reglas morfológicas.")
    L.append("")
    L.append("CAVEAT DE MÉTODO: el glosario de Zavala es una compilación de nueve autores")
    L.append("(Arcaya, Hernández Baño, Esteves, Angulo Molina, Alvarado, Galeotto Cey,")
    L.append("González Batista, Arellano Moreno, Hill Peña). Algunos fitónimos y zoónimos")
    L.append("son voces indígenas de circulación pan-venezolana cuya atribución")
    L.append("*específicamente caquetía* es más débil que la de un `diao` o un `barsure`.")
    L.append("Cada entrada lleva en `notas` el número de glosario y las siglas del")
    L.append("compilador para que esa procedencia quede siempre auditable.")
    L.append("")
    L.append("EXCLUIDOS del habla (ver EXCLUIR_DEL_HABLA en el minador): topónimos")
    L.append("modernos, antropónimos, etnónimos y glosas circulares. Están abajo en")
    L.append("TOPONIMOS_ZAVALA / ANTROPONIMOS_ZAVALA como referencia de canon, y NO se")
    L.append("mezclan con el vocabulario activo.")
    L.append('"""')
    L.append("")
    L.append("")

    # ── afijos ──
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# T1 — AFIJOS ATESTIGUADOS (el hallazgo de mayor valor)")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# Amplían lo que los agentes pueden CONSTRUIR, no solo nombrar. Se")
    L.append("# integran a las reglas morfológicas en curiana_lexicon.py.")
    L.append("")
    L.append("AFIJOS_ZAVALA: dict[str, dict] = {")
    for e in sorted(tiers["T1_afijos"], key=lambda x: x["num"]):
        forma = norm(e["lemas"][0])
        afijo = e.get("afijo", forma)
        glosa = e.get("glosa_afijo", e["definicion"])[:70]
        siglas = "+".join(e["siglas"]) or "s/sigla"
        L.append(f'    "{afijo}": {{"glosa": "{glosa}", '
                 f'"forma_glosario": "{forma}", "notas": "Zavala Reyes 2015 #{e["num"]} ({siglas})"}},')
    L.append("}")
    L.append("")
    L.append("")

    # ── vocabulario ──
    bloques = [
        ("T2_nombres_agente", "T2 — palabras que el proyecto YA USA como nombre de agente",
         "Sin estas entradas, cuando Bagre-ko decía 'bagre' o Buio-sha decía 'buio',\n"
         "# score_linguistico NO lo contaba como caquetío: la métrica sub-contaba."),
        ("T3_concreto", "T3 — sustantivos concretos: fauna, flora, paisaje, técnica",
         "Varios cierran 'huecos léxicos' que ecologia_lexicon_map.md daba por vacíos\n"
         "# (taques=salina, bisure=lagartija, chaguanco=zorro, jachos=teas de pesca)."),
        ("T4_abstracto", "T4 — verbos, cualidades y abstractos",
         "El lexicón activo es pobre en verbos y cualidades; este tier lo compensa."),
    ]
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# T2-T4 — VOCABULARIO ACTIVO")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("")
    L.append("GLOSARIO_ZAVALA: dict[str, dict] = {")
    for tier, titulo, nota in bloques:
        L.append("")
        L.append(f"    # ── {titulo} ──")
        for linea_nota in nota.split("\n"):
            L.append(f"    # {linea_nota.lstrip('# ')}")
        for e in sorted(tiers[tier], key=lambda x: norm(x["lemas"][0])):
            L.append(_entrada_py(e, tier))
    L.append("}")
    L.append("")
    L.append("")

    # ── homógrafos ──
    homs = sorted({norm(e["lemas"][0]) for t in ("T2_nombres_agente", "T3_concreto", "T4_abstracto")
                   for e in tiers[t] if e.get("homografo_es")})
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# HOMÓGRAFOS CON ESPAÑOL — se resuelven POR CONTEXTO")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# Son caquetío atestiguado, pero su forma coincide con una palabra")
    L.append("# española corriente. Sin tratamiento, un texto en español que diga")
    L.append('# "el bagre" puntuaría como caquetío. score_linguistico los cuenta solo')
    L.append("# si un vecino inmediato es arahuaco (mismo mecanismo que ya usa 'para').")
    L.append("")
    L.append("HOMOGRAFOS_ZAVALA: frozenset = frozenset({")
    for h in homs:
        L.append(f'    "{h}",')
    L.append("})")
    L.append("")
    L.append("")

    # ── referencia de canon ──
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# REFERENCIA DE CANON — fuera del vocabulario activo")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# Un agente no dice 'Bariquisimeto' para decir 'río turbio'. Se conservan")
    L.append("# por su valor etnohistórico y morfológico (muestran cómo compone la")
    L.append("# lengua), pero NO entran a VOCABULARIO_BASE ni puntúan.")
    L.append("")
    for nombre, tier in (("TOPONIMOS_ZAVALA", "T5_toponimo"),
                         ("ANTROPONIMOS_ZAVALA", "T5b_antroponimo"),
                         ("DESCARTADOS_ZAVALA", "T6_descartado")):
        L.append(f"{nombre}: dict[str, str] = {{")
        for e in sorted(tiers[tier], key=lambda x: norm(x["lemas"][0])):
            forma = norm(e["lemas"][0])
            d = e["definicion"].replace('"', "'")[:74]
            motivo = e.get("motivo", "")
            suf = f"   # {motivo}" if motivo else ""
            L.append(f'    "{forma}": "{d}",{suf}')
        L.append("}")
        L.append("")

    L.append("")
    L.append("TOTALES = {")
    L.append(f'    "afijos": {len(tiers["T1_afijos"])},')
    L.append(f'    "vocabulario_activo": {sum(len(tiers[t]) for t, _, _ in bloques)},')
    L.append(f'    "homografos": {len(homs)},')
    L.append(f'    "toponimos": {len(tiers["T5_toponimo"])},')
    L.append(f'    "antroponimos": {len(tiers["T5b_antroponimo"])},')
    L.append("}")
    L.append("")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"  → módulo generado: {ruta}")
    print(f"     afijos={len(tiers['T1_afijos'])}  "
          f"vocabulario={sum(len(tiers[t]) for t, _, _ in bloques)}  "
          f"homógrafos={len(homs)}  topónimos={len(tiers['T5_toponimo'])}  "
          f"antropónimos={len(tiers['T5b_antroponimo'])}")


def emitir_python(tiers: dict, incluir=("T2_nombres_agente", "T3_concreto", "T4_abstracto")):
    """Emite entradas sueltas por stdout (inspección rápida)."""
    for t in incluir:
        for e in sorted(tiers[t], key=lambda x: norm(x["lemas"][0])):
            print(_entrada_py(e, t, indent=""))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", metavar="RUTA", help="volcar la clasificación a JSON")
    ap.add_argument("--python", action="store_true", help="emitir entradas para VOCABULARIO_BASE")
    ap.add_argument("--generar-modulo", nargs="?", const="lexicon_zavala.py",
                    metavar="RUTA", help="escribir lexicon_zavala.py con la propuesta")
    args = ap.parse_args()

    entradas = extraer()
    tiers = clasificar(entradas)

    if args.generar_modulo:
        ruta = args.generar_modulo
        if not os.path.isabs(ruta):
            ruta = os.path.join(os.path.dirname(__file__), ruta)
        generar_modulo(tiers, ruta)
    elif args.python:
        emitir_python(tiers)
    else:
        informe(tiers, entradas)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"total": len(entradas), "tiers": tiers}, f,
                      ensure_ascii=False, indent=2)
        print(f"\n  → JSON: {args.json}")
