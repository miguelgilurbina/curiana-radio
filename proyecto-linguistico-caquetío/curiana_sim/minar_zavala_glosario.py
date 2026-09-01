"""
CURIANA — Minería del glosario de Zavala Reyes (2015)
=====================================================

Extrae las **288** entradas numeradas del glosario de:

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

CIERRE DEL PARSEO (F7, 2026-08-03): la extracción cubría 286 de las 288 entradas
y mutilaba nueve definiciones. Ver `RESCATES_PARSEO` y `_normalizar_plano()` más
abajo: hoy el parseo es **288/288 sin mutilaciones**, y `extraer()` lo verifica.

Uso:
    python minar_zavala_glosario.py              # informe por tiers
    python minar_zavala_glosario.py --json out.json
    python minar_zavala_glosario.py --python     # emite entradas listas para pegar
    python minar_zavala_glosario.py --generar-modulo   # reescribe lexicon_zavala.py

NO modifica curiana_lexicon.py: emite una propuesta para revisión humana, en la
misma disciplina que retag_nucleo_fundacional.py y minar_pares_validacion.py.
"""

import argparse
import io
import json
import os
import re
import sys
import unicodedata

# Las reglas ortográficas de D5 (lema fonémico) viven en el aplicador de la
# Fase 2 y se importan de ahí: una sola fuente de verdad para la migración.
from aplicar_fase2_d5 import lema_fonemico


def _forzar_utf8() -> None:
    """La consola de Windows usa cp1252 y el informe imprime "─", "⚠", "í"…

    Sin esto el script revienta con UnicodeEncodeError al llegar a los tiers.
    Se llama solo al ejecutarlo como script: reasignar sys.stdout al importarlo
    como módulo le rompería el stdout a quien lo importa.
    """
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))

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

TOTAL_ENTRADAS_PDF = 288          # numeración del glosario, pp. 65-72

# Número de página suelto (58-76) que sobrevive a `_FOOTER` y se pega a la
# definición de la última entrada de cada plana ("…cerca del mar.  66 38. Barsure").
_PAG_SUELTA = re.compile(
    r"\s+-?\s*(?:5[89]|6\d|7[0-6])\s*-?\s+(?=\d{1,3}\s*[.\-]\s*[A-ZÁÉÍÓÚÑÜ])")

# pypdf separa la versal inicial de algunas palabras ("V olturido", "V ocero").
# Se excluyen las letras que en español son palabra por sí solas (a, e, o, u, y).
_VERSAL_SUELTA = re.compile(r"\b([BCDFGHJKLMNPQRSTVWXZ]) (?=[a-záéíóúñ])")

# RESCATES DEL PARSEO (F7, 2026-08-03) — las dos entradas que el regex perdía y
# las nueve definiciones que mutilaba. Se documentan aquí, no se parchean a mano:
# `_normalizar_plano()` corrige la causa y el regex las captura como al resto.
RESCATES_PARSEO = {
    31: "Baracoica (HP). Cacique de Curazao — única entrada del glosario que "
        "separa siglas y definición con PUNTO en vez de dos puntos. El regex "
        "exigía ':' y la saltaba entera.",
    104: "Darubana (durabana) (AM): Camino, vía — única entrada cuyo lema lleva "
         "una variante entre paréntesis en minúscula. El grupo del lema excluye "
         "'(' y el de siglas solo acepta 1-4 letras, así que no casaba ninguno.",
    "definiciones_mutiladas":
        "#37, #77, #116, #156, #195, #235, #275 arrastraban el número de página "
        "de la plana ('…cerca del mar. 66'); #143 y #183 traían la versal partida "
        "por pypdf ('V olturido', 'V ocero').",
}


def _normalizar_plano(plano: str) -> str:
    """Repara los tres defectos de extracción documentados en RESCATES_PARSEO.

    Los tres patrones son **únicos** en el glosario (verificado: un solo
    '(SIGLAS).', un solo paréntesis en minúscula), así que la corrección es
    general y no un parche por entrada.
    """
    plano = _PAG_SUELTA.sub(" ", plano)
    plano = _VERSAL_SUELTA.sub(r"\1", plano)
    # "(HP). Cacique de Curazao"  →  "(HP): Cacique de Curazao"
    plano = re.sub(r"(\([A-Z]{1,4}\))\s*\.\s*(?=[A-ZÁÉÍÓÚÑÜ])", r"\1: ", plano)
    # "Darubana (durabana) (AM)"  →  "Darubana, durabana (AM)"
    plano = re.sub(r"\s*\(([a-záéíóúñ]{3,})\)", r", \1", plano)
    return plano


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
#
# REVISIÓN F7 (2026-08-03) — las 28 formas que la marca heurística levantaba se
# revisaron **una por una** contra la entrada de Zavala. La pregunta era: ¿es la
# voz caquetía, o es la palabra ESPAÑOLA con la que Zavala la glosa? Resultado:
#
#   · 14 se quedan marcadas  → colisión real con el español (esta tabla).
#   · 11 pierden la marca    → no son palabras del español (ver DESMARCADAS_F7);
#                              marcarlas hacía que el scorer SUB-contara caquetío.
#   ·  3 salen del habla     → ver DESCARTAR_DEL_HABLA.
#
# Cuatro casos que la revisión aclaró de paso (no son homógrafos, son la GLOSA
# española de otra entrada, y por tanto no deben tratarse como voz caquetía):
# `caraota` glosa a *icoroata* (#162), `paují` glosa a *paugis* (#197),
# `piache` glosa a *boratio* (#43), y `coro` no viene de aquí — Zavala #181 es
# *Koro* 'cotorra', no 'cardón'.
HOMOGRAFOS_ES: dict[str, str] = {
    "aca":    "#3 (E) 'bejuco'. Caquetía. Colisiona con 'acá' si se escribe sin tilde.",
    "bagre":  "#21 (AM) 'pez'. Caquetía según la fuente; el 'bagre' español es a su vez indigenismo. Colisión real.",
    "cana":   "#57 (HB) 'demonio'. Caquetía; colisiona con 'cana'/'caña'.",
    "capo":   "#59 (E) 'duende'. Caquetía (cf. #60 capu 'demonio'); colisión menor con 'capo'.",
    "carama": "#64 (E) 'ramazón'. Caquetía; 'carama' existe en español rural (escarcha).",
    "cocuy":  "#87 'penca; planta que da un vino'. Indigenismo de circulación pan-venezolana: ATRIBUCIÓN DÉBIL además de homógrafo.",
    "dato":   "#105 (HB) 'fruto del cardón'. Caquetía, pero 'dato' es altísima frecuencia en español: la marca es imprescindible.",
    "guaca":  "#123 (E) 'ave, cotorra'. Caquetía; 'guaca' español (quechua, tesoro) es otra cosa.",
    "guay":   "#147 (E)(A) 'árbol parecido a la ceiba'. Caquetía; colisiona con la interjección.",
    "samuro": "#223 (AM) 'punta hacia el mar'. La forma coincide con 'zamuro' (zoónimo venezolano) y la glosa es geográfica: ATRIBUCIÓN DÉBIL.",
    "sigua":  "#227 (E) 'blando'. Caquetía; 'sigua' antillano es otra cosa.",
    "taque":  "#236 (E) 'árbol nucífero'. Caquetía; 'taque' español es regional y raro.",
    "taques": "#237 (AM) 'salina'. Es también el topónimo Los Taques (Paraguaná): la glosa es la etimología del lugar. ATRIBUCIÓN DÉBIL.",
    "tuba":   "#253 (E) 'aglomeración, montón'. Caquetía; colisiona con 'tuba'.",
}

# Formas que la marca heurística levantaba y que NO son palabras del español.
# Se documentan para que nadie las vuelva a marcar "por si acaso": marcarlas
# obliga al scorer a exigir vecino arahuaco y hace perder caquetío legítimo.
DESMARCADAS_F7: dict[str, str] = {
    "aco":      "#4 'comida; par, pareja' — no existe en español.",
    "apo":      "#11 'grande' — en español solo es prefijo culto (apo-).",
    "cabana":   "#51 'sabana' — la palabra española es 'cabaña', con ñ.",
    "icoroata": "#162 'caraota' — NO es homógrafo: es la voz caquetía; 'caraota' es su glosa.",
    "koro":     "#181 'cotorra' — con k no colisiona; 'coro' (canto) es otra forma.",
    "quiba":    "#203 'ayuda' — no existe en español.",
    "quiva":    "#218 'piedra' — no existe en español.",
    "ruba":     "#221 'abeja silvestre negra de Coro' — no existe en español.",
    "supi":     "#230 'sitio a orilla del mar' — no existe en español.",
    "ure":      "#272 'raíz' — no existe en español.",
    "yaro":     "#285 'bejuco, planta venenosa' — no existe en español (sí es topónimo de Falcón).",
}

# FUSIONADAS EN EL LITERAL por la decisión de colisiones D5 (2026-08-31,
# 6-fusion/decisiones_colisiones_d5_2026-08-31.yaml): la grafía española es
# grafía; el lema fonémico es la palabra, y vive UNA vez, en el literal de
# curiana_lexicon.py, con los homónimos declarados (patrón D9). El miner las
# reconoce aquí y no las re-emite. El homógrafo español de sigua se disolvió
# con la grafía (siwa no choca con nada); su veredicto F7 sigue abajo en
# HOMOGRAFOS_ES como documentación.
FUSIONADAS_EN_LITERAL: dict[str, str] = {
    "quiba": "kiba",   # #203 (AM) 'ayuda' — homónimo kiba-2, declarado bajo kiba
    "quiva": "kiba",   # #218 (E) 'piedra' — kiba-1, el sig activo
    "sigua": "siwa",   # #227 (E) 'blando' — siwa-1; 'sal de comercio' queda como siwa-2
}

# DESCARTE del habla activa (nivel D del protocolo de descarte, §5 de
# investigacion/disenos/02_protocolo_habla_paraguanera.md). No son topónimos:
# son formas cuya presencia en el léxico activo hace más daño que bien.
DESCARTAR_DEL_HABLA: dict[str, str] = {
    "hay": "F7: #154 (AM) 'coca'. La forma coincide con el verbo español más "
           "frecuente ('hay'); ninguna resolución por contexto compensa eso. "
           "En su lugar queda `hayo` (#156, 'hierba quita sed'), que es la forma "
           "corriente del mismo referente y no colisiona.",
    "enea": "F7: #118 (A) 'planta ciperácea'. 'Enea' (~anea, Typha) ES la palabra "
            "española del junco; Alvarado está dando el nombre castellano de la "
            "planta, no una voz caquetía.",
    "guata": "F7: #146 (AM) 'Planta'. Glosa vacía —no dice qué planta— y homógrafo "
             "con 'guata'. Mismo criterio que `coroque` ('Árbol de ¿?').",
}

# ══════════════════════════════════════════════════════════════════════
# D7 — glosa histórica vs. identificación científica moderna
# ══════════════════════════════════════════════════════════════════════
# Decisión de Miguel, 2026-08-03: cuando la glosa de la fuente y la
# identificación taxonómica moderna difieren, **se registran las dos, en campos
# separados**, y ninguna gana:
#
#   glosa_fuente           → lo que dice Zavala, verbatim, con nº y siglas.
#                            ES LA QUE EL AGENTE HABLA (`sig` se deriva de ella).
#   identificacion_moderna → el taxón actual, como nota auditable.
#
# Se rellena a mano, caso por caso: nadie infiere taxonomía automáticamente.
IDENTIFICACION_MODERNA: dict[str, str] = {
    "cunaro": "Rhomboplites aurorubens (pargo cunaro, de altura) según SVDB. "
              "Zavala transcribe 'Promicops Guasa' (por Promicrops itajara, hoy "
              "Epinephelus itajara, el mero guasa): dos peces distintos.",
    "guaranaro": "sin resolver; 'lisa' apunta a Mugil spp. (M. curema / M. incilis "
                 "son las del Golfete). La hoja de fuentes 02_ecologia lo daba por "
                 "'sin identificación taxonómica firme' cuando Zavala YA lo glosaba.",
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
    plano = _normalizar_plano(plano)            # ver RESCATES_PARSEO

    vistos: dict[int, dict] = {}
    for m in _ENTRADA.finditer(plano):
        num = int(m.group(1))
        if num in vistos or not (1 <= num <= TOTAL_ENTRADAS_PDF):
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

    # El parseo debe cerrar en 288/288. Si vuelve a abrirse un hueco (otra
    # extracción de PDF, otra versión de pypdf), que se vea, no que se silencie.
    faltan = [n for n in range(1, TOTAL_ENTRADAS_PDF + 1) if n not in vistos]
    if faltan:
        print(f"  AVISO: entradas del PDF no parseadas: {faltan}", file=sys.stderr)

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
        familia = normalize_source_language(e.get("fuente", ""))
        lex_idx.setdefault(norm(w), (w, familia))
        # Fase 2 de D5 (2026-08-31): el literal migró sus lemas a grafía
        # fonémica conservando la anterior en forma_fuente. Sin este alias el
        # miner vería «cari», «coques» o «catarí» como ausentes —ya no casan
        # con la clave migrada— y los re-emitiría duplicados. Es también lo
        # que cierra la fusión del #89: «coques» casa con koke.forma_fuente.
        ff = e.get("forma_fuente")
        if ff:
            lex_idx.setdefault(norm(ff), (w, familia))

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

        # Un lema «ya está» solo si casa POR GRAFÍA (la clave o la
        # forma_fuente del alias). Casar por lema fonémico sería absorber en
        # silencio palabras DISTINTAS que colisionan (quiba 'ayuda' no es el
        # kiba del literal): esas van a COLISIONES_D5, más abajo.
        hit = next(((l, *lex_idx[norm(l)]) for l in e["lemas"] if norm(l) in lex_idx), None)
        if hit:
            lema, forma_lex, fuente = hit
            reg = {**e, "forma_lexicon": forma_lex, "fuente_actual": fuente}
            tiers["YA_EN_LEXICON"].append(reg)
            if fuente != "caquetío":
                tiers["MAL_ETIQUETADO"].append(reg)
            continue

        # Colisiones ya DECIDIDAS (2026-08-31): viven fusionadas en el
        # literal con homónimos declarados; no se re-emiten.
        fus = next((l for l in lemas_n if l in FUSIONADAS_EN_LITERAL), None)
        if fus:
            tiers["YA_EN_LEXICON"].append(
                {**e, "forma_lexicon": FUSIONADAS_EN_LITERAL[fus],
                 "fuente_actual": "caquetío"})
            continue

        # La marca se decide por la forma que REALMENTE entra al léxico (el
        # primer lema), no por cualquier variante: la #4 "Aco. Aca" entra como
        # `aco`, que no es homógrafo, aunque su variante `aca` sí lo sea.
        e = {**e, "homografo_es": lemas_n[0] in HOMOGRAFOS_ES}

        if any(l in DESCARTAR_DEL_HABLA for l in lemas_n):
            motivo = next(DESCARTAR_DEL_HABLA[l] for l in lemas_n if l in DESCARTAR_DEL_HABLA)
            tiers["T6_descartado"].append({**e, "motivo": motivo})
        elif any(l in EXCLUIR_DEL_HABLA for l in lemas_n):
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

    # ── Fase 2 de D5 sobre el generado (decidida 2026-08-30; el literal
    # migró el 2026-08-31 con aplicar_fase2_d5.py — mismo movimiento aquí) ──
    # Cada entrada del vocabulario activo entra con su LEMA FONÉMICO y
    # conserva la grafía de Zavala en forma_fuente. Colisiones NO se
    # renombran: cada una es una decisión, no un accidente. Los topónimos y
    # antropónimos (T5/T5b) quedan en grafía fuente por D5a.
    claves_literal = {w for w in VOCABULARIO_BASE if w not in _YA_IMPORTADO}
    activos = [e for t in ("T2_nombres_agente", "T3_concreto", "T4_abstracto")
               for e in tiers[t]]
    finales: dict[str, int] = {}
    for e in activos:
        e["lema_fonemico"] = lema_fonemico(norm(e["lemas"][0]))
        finales[e["lema_fonemico"]] = finales.get(e["lema_fonemico"], 0) + 1
    tiers["COLISIONES_D5"] = []
    for e in activos:
        origen, nuevo = norm(e["lemas"][0]), e["lema_fonemico"]
        colision = None
        if nuevo in claves_literal:
            colision = f"su lema fonémico «{nuevo}» ya es clave del lexicón literal"
        elif finales[nuevo] > 1:
            colision = f"más de una entrada del glosario da el lema «{nuevo}»"
        # Colisión con forma cambiada → se queda en grafía fuente, pendiente.
        # Colisión con forma intacta (naure/naure) → statu quo, pero visible.
        e["lema_final"] = origen if (colision and nuevo != origen) else nuevo
        if colision:
            tiers["COLISIONES_D5"].append(
                {"forma": origen, "lema_fonemico": nuevo, "num": e["num"],
                 "motivo": colision})
        # El veredicto de homógrafo (F7) es sobre la GRAFÍA: si la migración
        # cambió la forma, la colisión con el español se disuelve con ella.
        e["homografo_disuelto"] = bool(e.get("homografo_es")) and e["lema_final"] != origen
        e["homografo_es"] = bool(e.get("homografo_es")) and e["lema_final"] == origen

    return tiers


def informe(tiers: dict, entradas: list[dict]):
    total = len(entradas)
    ya = len(tiers["YA_EN_LEXICON"])
    print("=" * 78)
    print("  GLOSARIO ZAVALA REYES 2015 — auditoría de importación")
    print("=" * 78)
    print(f"  entradas numeradas del PDF: {TOTAL_ENTRADAS_PDF}")
    print(f"  entradas parseadas:         {total}"
          f"   ({'CIERRA' if total == TOTAL_ENTRADAS_PDF else 'HUECO'})")
    print(f"  ya presentes en VOCABULARIO_BASE: {ya}  ({100*ya//max(total,1)}%)")
    print(f"  ausentes: {total - ya}")
    capturadas = sum(len(tiers[t]) for t in
                     ("T1_afijos", "T2_nombres_agente", "T3_concreto", "T4_abstracto",
                      "T5_toponimo", "T5b_antroponimo", "T6_descartado")) + ya
    print(f"  CAPTURADAS (habla + canon + descartes + ya presentes): {capturadas}"
          f"/{TOTAL_ENTRADAS_PDF}  ({100*capturadas//TOTAL_ENTRADAS_PDF}%)")
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

    activos = [e for t in ("T2_nombres_agente", "T3_concreto", "T4_abstracto")
               for e in tiers[t]]
    renombradas = [e for e in activos
                   if e.get("lema_final", "") != norm(e["lemas"][0])]
    disueltos = [e for e in activos if e.get("homografo_disuelto")]
    print(f"\n  D5 fase 2 — {len(renombradas)} lemas al fonémico, "
          f"{len(disueltos)} homógrafos disueltos, "
          f"{len(tiers.get('COLISIONES_D5', []))} colisiones sin renombrar:")
    for c in tiers.get("COLISIONES_D5", []):
        print(f"     ⚠ {c['forma']:14} → {c['lema_fonemico']:14} {c['motivo']}")
    if tiers["MAL_ETIQUETADO"]:
        print(f"\n  ⚠ presentes pero NO etiquetadas 'caquetío' ({len(tiers['MAL_ETIQUETADO'])}):")
        for e in tiers["MAL_ETIQUETADO"]:
            print(f"     {e['lemas'][0]:18} lexicón='{e['forma_lexicon']}' = {e['fuente_actual']}"
                  f"  | Zavala: {e['definicion'][:40]}")


_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS; el resto, sust


def _entrada_py(e: dict, tier: str, indent: str = "    ") -> str:
    origen = norm(e["lemas"][0])
    forma = e.get("lema_final", origen)      # Fase 2 de D5: lema fonémico
    verbatim = e["definicion"].replace('"', "'").replace("\\", "")
    sig = verbatim[:78]
    sig = (sig[0].lower() + sig[1:]) if sig else sig
    siglas = "+".join(e["siglas"]) or "s/sigla"
    nota = f"Zavala Reyes 2015 #{e['num']} ({siglas})"
    if e.get("homografo_es"):
        nota += "; homógrafo con español — resuelto por contexto en score_linguistico"
    if e.get("homografo_disuelto"):
        nota += (f"; era homógrafo del español en grafía fuente ({origen}) — "
                 "la migración D5 disolvió la colisión")
    if forma == origen != e.get("lema_fonemico", origen):
        nota += (f"; D5 PENDIENTE: su lema fonémico {e['lema_fonemico']} "
                 "colisiona — ver COLISIONES_D5")
    variantes = [norm(l) for l in e["lemas"][1:]]
    if variantes:
        nota += f"; variantes: {', '.join(variantes)}"
    cat = _CAT_POR_TIER.get(tier, "sust")
    pad = " " * max(1, 14 - len(forma))
    # D7: la glosa de la fuente se conserva verbatim y trazable; la
    # identificación moderna se añade aparte, sin desplazarla.
    extra = (f' "glosa_fuente": "{verbatim} [Zavala Reyes 2015 #{e["num"]} ({siglas})]",')
    if forma != origen:
        extra += f' "forma_fuente": "{origen}",'
    moderna = IDENTIFICACION_MODERNA.get(origen)
    if moderna:
        extra += f' "identificacion_moderna": "{moderna.replace(chr(34), chr(39))}",'
    return (f'{indent}"{forma}":{pad}{{"sig": "{sig}", "cat": "{cat}", '
            f'"fuente": "caquetío-atestiguado",{extra} "notas": "{nota}"}},')


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
    L.append("MOTIVO (auditoría 2026-07-20): el lexicón contenía solo ~66 de las 288")
    L.append("entradas del glosario (23%). Faltaban palabras que el propio proyecto usa")
    L.append("como nombre de agente (buio, bagre, cunaro, guaranaro, dara, naure) — que")
    L.append("por tanto NO puntuaban como caquetío — y ocho afijos atestiguados ausentes")
    L.append("de las reglas morfológicas.")
    L.append("")
    L.append("CIERRE DEL PARSEO (F7, 2026-08-03): el glosario tiene 288 entradas numeradas")
    L.append("y hoy se parsean las 288. Antes se perdían la #31 (separa siglas y definición")
    L.append("con punto) y la #104 (variante del lema entre paréntesis), y nueve")
    L.append("definiciones venían mutiladas por el número de página o por versales")
    L.append("partidas por pypdf. Ver RESCATES_PARSEO en el minador.")
    L.append("")
    L.append("D7 — GLOSA HISTÓRICA vs. IDENTIFICACIÓN MODERNA (decidido el 2026-08-03):")
    L.append("cada entrada lleva `glosa_fuente` con el texto VERBATIM de Zavala, su número")
    L.append("y las siglas del compilador. Esa es la glosa que el agente habla. Cuando la")
    L.append("ciencia moderna identifica otra cosa, se añade `identificacion_moderna` como")
    L.append("nota auditable; ninguna de las dos desplaza a la otra.")
    L.append("")
    L.append("D5 FASE 2 — LEMA FONÉMICO (decidida 2026-08-30/F2-#36; aplicada al generado")
    L.append("el 2026-08-31): el vocabulario activo entra con su lema en grafía fonémica")
    L.append("(gua/gü→w, gue/gui→g dura, qu→k, c→k salvo ch y ce/ci, z→s, v→b) y conserva")
    L.append("la grafía de Zavala en `forma_fuente`. Los homógrafos cuya colisión con el")
    L.append("español era de la grafía colonial quedan DISUELTOS (ver")
    L.append("HOMOGRAFOS_DISUELTOS_D5); las colisiones de lema NO se renombran y esperan")
    L.append("decisión (ver COLISIONES_D5). Topónimos y antropónimos siguen en grafía")
    L.append("fuente por D5a. Mapa del literal: 6-fusion/migracion_lemas_fase2.yaml.")
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
    _activos = [e for t in ("T2_nombres_agente", "T3_concreto", "T4_abstracto")
                for e in tiers[t]]
    homs = sorted({e.get("lema_final", norm(e["lemas"][0]))
                   for e in _activos if e.get("homografo_es")})
    disueltos = sorted((e for e in _activos if e.get("homografo_disuelto")),
                       key=lambda e: e["lema_final"])
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# HOMÓGRAFOS CON ESPAÑOL — se resuelven POR CONTEXTO")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# Son caquetío atestiguado, pero su forma coincide con una palabra")
    L.append("# española corriente. Sin tratamiento, un texto en español que diga")
    L.append('# "el bagre" puntuaría como caquetío. score_linguistico los cuenta solo')
    L.append("# si un vecino inmediato es arahuaco (mismo mecanismo que ya usa 'para').")
    L.append("")
    L.append("# Revisión F7 (2026-08-03): las 28 formas que la heurística marcaba se")
    L.append("# revisaron una por una contra su entrada de Zavala. 14 siguen marcadas,")
    L.append("# 11 perdieron la marca por no ser palabras del español (DESMARCADAS_F7 en")
    L.append("# el minador) y 3 salieron del habla (DESCARTADOS_ZAVALA, abajo).")
    L.append("")
    L.append("HOMOGRAFOS_ZAVALA: frozenset = frozenset({")
    for h in homs:
        L.append(f'    "{h}",')
    L.append("})")
    L.append("")
    L.append("")
    L.append("# Veredicto por forma, para que la marca sea auditable y no un acto de fe.")
    L.append("VEREDICTO_HOMOGRAFOS: dict[str, str] = {")
    for h in homs:
        v = HOMOGRAFOS_ES.get(h, "").replace('"', "'")
        L.append(f'    "{h}": "{v}",')
    L.append("}")
    L.append("")
    L.append("")
    L.append("# Homógrafos que la migración D5 DISOLVIÓ: la colisión con el español era")
    L.append("# de la grafía colonial, no del fonema (guaca chocaba con 'guaca'; waka no")
    L.append("# choca con nada). Se conserva el veredicto F7 para que nadie los vuelva a")
    L.append("# marcar «por si acaso» — marcarlos haría sub-contar caquetío legítimo.")
    L.append("HOMOGRAFOS_DISUELTOS_D5: dict[str, str] = {")
    for e in disueltos:
        origen = norm(e["lemas"][0])
        v = HOMOGRAFOS_ES.get(origen, "").replace('"', "'")
        L.append(f'    "{e["lema_final"]}": "grafía fuente «{origen}» — {v}",')
    L.append("}")
    L.append("")
    L.append("")
    L.append("# Colisiones de lema fonémico — NO se renombraron: cada una es una")
    L.append("# decisión pendiente, no un accidente. La entrada sigue en grafía fuente.")
    L.append("COLISIONES_D5: list[dict] = [")
    for c in tiers.get("COLISIONES_D5", []):
        L.append(f'    {{"forma": "{c["forma"]}", "lema_fonemico": "{c["lema_fonemico"]}", '
                 f'"num": {c["num"]}, "motivo": "{c["motivo"]}"}},')
    L.append("]")
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
    _renombradas = sum(1 for e in _activos
                       if e.get("lema_final", "") != norm(e["lemas"][0]))
    L.append("TOTALES = {")
    L.append(f'    "afijos": {len(tiers["T1_afijos"])},')
    L.append(f'    "vocabulario_activo": {sum(len(tiers[t]) for t, _, _ in bloques)},')
    L.append(f'    "renombradas_d5": {_renombradas},')
    L.append(f'    "homografos": {len(homs)},')
    L.append(f'    "homografos_disueltos_d5": {len(disueltos)},')
    L.append(f'    "colisiones_d5": {len(tiers.get("COLISIONES_D5", []))},')
    L.append(f'    "toponimos": {len(tiers["T5_toponimo"])},')
    L.append(f'    "antroponimos": {len(tiers["T5b_antroponimo"])},')
    L.append(f'    "descartados": {len(tiers["T6_descartado"])},')
    L.append(f'    "ya_en_lexicon_antes_del_import": {len(tiers["YA_EN_LEXICON"])},')
    L.append(f'    "entradas_pdf": {TOTAL_ENTRADAS_PDF},')
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
    _forzar_utf8()
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
