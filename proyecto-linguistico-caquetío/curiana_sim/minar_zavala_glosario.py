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
# NO ES LA MISMA VOZ — homógrafos formales con la comparanda de OTRA lengua
# ══════════════════════════════════════════════════════════════════════
# El cruce contra `VOCABULARIO_BASE` pregunta «¿esta voz de Zavala ya está?»
# y lo pregunta sobre el lexicón ENTERO, que desde el 2026-09-13 lleva las
# 3.569 entradas de la comparanda achagua (Neira y Ribero 1762) además del
# wayuu, el lokono y el taíno. Con eso, una coincidencia de GRAFÍA entre dos
# lenguas hermanas dejó de ser rara y pasó a leerse como «ya está»:
#
#     Cana   #57  'demonio'          vs. achagua `cana-achagua` 'maíz'
#     Carama #64  'ramazón'          vs. achagua `carama` 'cachama, un pescado'
#     Cuna   #95  'pez del golfete'  vs. achagua `cuna-achagua` 'barbasco de raíz'
#     Turupía #263 'árbol espinoso'  vs. achagua `turupia-achagua` 'toche'
#     Ima    #165 AFIJO 'humedad'    vs. lokono  `ima` 'enemigo'
#     Coa    #6   variante del AFIJO `-aima` vs. caquetío `koa` (forma_fuente «coa»)
#
# Medido el 2026-09-20: sin esta tabla, `--generar-modulo` borra del módulo
# generado cuatro voces atestiguadas (`kana`, `karama`, `kuna`, `turupia`) y
# DOS de los ocho afijos (`-ima`, `-aima`) — el hallazgo de mayor valor de
# toda la minería, según la cabecera de este mismo archivo. El módulo
# commiteado es de antes de la fusión achagua y por eso aún las tiene: la
# deriva estaba latente, no aplicada.
#
# ⚠️ Esto NO es el arreglo de fondo. El arreglo de fondo es que `lex_idx` se
# construya sólo con la familia caquetía —un comparandum de otra lengua no
# es «la misma voz» nunca— y eso cambia qué entra en `VOCABULARIO_BASE` (p.
# ej. `ture`, hoy caribe-continental, volvería a emitirse como caquetía) y
# por tanto mueve el score. Es decisión de Miguel: propuesta en
# 6-fusion/clases_de_raiz_zavala_2026-09-20.yaml §homografos_de_la_comparanda.
NO_ES_LA_MISMA_VOZ: dict[str, str] = {
    "cana":    "#57 (HB) 'demonio'. El homógrafo es `cana-achagua` 'maíz' (Neira y Ribero 1762): otra lengua, otro referente.",
    "carama":  "#64 (E) 'ramazón'. El homógrafo es el achagua `carama` 'cachama, un pescado'.",
    "cuna":    "#95 (E) 'pez del golfete de Coro'. El homógrafo es `cuna-achagua` 'barbasco de raíz'.",
    "turupia": "#263 (AM+A) 'árbol espinoso. Sitio en Cumarebo'. El homógrafo es `turupia-achagua` 'toche'.",
    "ima":     "#165 (E+PMA) AFIJO 'humedad, quebrada'. El homógrafo es el lokono `ima` 'enemigo'; un afijo no es una clave del léxico.",
    "coa":     "#6 (AM+PMA) variante del AFIJO `-aima` 'abundancia'. El homógrafo es `koa` (forma_fuente «coa»), el palo de siembra: misma grafía colonial, distinto morfema.",
}


# ══════════════════════════════════════════════════════════════════════
# LA CLASE DE LA RAÍZ — declarada por fila, no heredada del tier
# ══════════════════════════════════════════════════════════════════════
# ANTES (hasta el 2026-09-20) toda la clasificación de parte de la oración
# era una línea:
#
#     _CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS
#
# El tier T4 es el CAJÓN DE RESTO: lo que el regex `re_concreto` no reconoció
# como cosa. De ahí salían **49** entradas con `cat: "v_raiz"`, y de
# `cat: "v_raiz"` sale `_RAICES_VERB` (curiana_lexicon.py), que hace que
# `score_linguistico()` cuente como arahuaco **cualquier token cuyo primer
# segmento sea una raíz verbal** y que `_familia_de_token()` le dé lengua
# propia. Sobre esas 49 raíces la base tiene 123 formas raíz+aspecto y 1.071
# usos (`juri-*` 227, `waidima-*` 97, `dichiba-*` 63, `popoi-*` 59…).
#
# PERO NO es que «40 no sean verbos» (Miguel, 2026-09-20). En arahuaco mucho
# de lo que el castellano llama adjetivo **es un verbo estativo**: Perea y
# Alonso 1942 (obra `perea-alonso-1942`) describe la 4ª conjugación lokono
# —infinitivo en `-en`, pronombre POSPUESTO (`de, bù, i, n, u, hù, ye`)— como
# «la clase de los ESTATIVOS: colores, tamaños, sabores, estados»
# (pp. 634-639: `cule-n` 'ser rojo', `ibe-n` 'estar lleno', `hebbe-n` 'ser
# viejo'), y en pp. 598-599/608 da la regla que los fabrica: «cualquier
# nombre, adjetivo o partícula se hace verbo anteponiendo a- o c-». Buscar
# «adjetivos» sueltos es buscar en la categoría equivocada.
#
# Así que las 49 se clasifican UNA POR UNA contra la glosa verbatim de la
# fuente (`glosa_fuente`, que NO se toca) y contra la comparanda que el
# proyecto ya tiene, en tres clases:
#
#   estativo → concepto adjetival que en arahuaco es verbo   → cat v_estativo
#   accion   → verbo pleno                                   → cat v_raiz
#   nombre   → sustantivo concreto o abstracto               → cat sust
#   adverbio → deíctico de lugar (la clase de `yama`)        → cat part
#
# Las dos primeras son VERBALES las dos: lo que cambia no es que se conjuguen
# sino que ahora está declarado con su razón. La tercera y la cuarta son las
# que estaban mal.
#
# ⚠️ `v_estativo` es de la TANDA DEL 2026-09-21 (d21.4, «Vale vamos con la B
# entonces»). Hasta entonces las diez estativas se emitían con `cat: v_raiz` y
# la clase sólo vivía en `CLASES_DE_RAIZ_ZAVALA`, o sea en la documentación.
# Desde la tanda la clase se DECLARA en la categoría —y llega al prompt— sin
# importar el alineamiento del lokono (opción C, descartada: no hay ni un dato
# caquetío detrás). `curiana_lexicon.CATS_VERBALES` las cuenta como verbales
# igual que a `v_raiz`, así que `_RAICES_VERB`, el detector de aspecto y la
# derivación de semillas de `curiana_koine` no pierden ni una raíz.
#
# ⚠️ Lo que se corrige es `cat` —que es NUESTRO—. `glosa_fuente` es verbatim
# de Zavala y no se toca jamás; `sig` tampoco se toca aquí (mueve lo que el
# agente lee): las glosas que piden curación van propuestas, sin aplicar, en
# 6-fusion/clases_de_raiz_zavala_2026-09-20.yaml §curacion_de_sig.
#
# La clave es la GRAFÍA DE ZAVALA (el primer lema normalizado), como en
# HOMOGRAFOS_ES y IDENTIFICACION_MODERNA, para que la fila sobreviva a
# cualquier re-migración de lema fonémico. Cada fila lleva:
#   cat    — lo que se emite
#   clase  — estativo | accion | nombre | adverbio
#   por    — el apoyo comparativo CON CITA (regla 8: id de
#            4-fuentes/bibliografia.yaml) o `deuda: sin-procedencia`
CLASE_DE_LA_RAIZ: dict[str, dict] = {

    # ── ESTATIVOS: el castellano dice adjetivo, el arahuaco dice verbo ──
    "apo": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Grande' es tamaño, y los tamaños son la 4ª conjugación estativa "
               "del lokono (perea-alonso-1942, pp. 634-639). El propio lexicón ya "
               "trae el lokono `ipi-lli-be` 'ser grande' como v_raiz. La achagua "
               "verbaliza y nominaliza la misma raíz: `numanudau` 'engrandecer', "
               "`manucaicasi` 'grandeza' (neira-ribero-1762)."},
    "bachure": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Maneto, patituerto' es defecto corporal, y el lokono lo dice con "
               "verbo estativo: `hiccu-li` 'ser cojo' (perea-alonso-1942), ya en el "
               "lexicón como v_raiz."},
    "cachipo": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Enojado, colérico' es estado. La achagua lo conjuga sobre una raíz "
               "`cabare-` con el atributivo ca-/ka-: `cabareuno` 'enojarse', "
               "`cabarecayi` 'colérico', `cabareumí` 'es bravo' (neira-ribero-1762). "
               "Wayuu `aashichijawaa` 'enojarse'."},
    "etamo": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Feroz, feo' son cualidades (4ª conj. lokono, perea-alonso-1942 "
               "p. 634); 'espanto' es su nombre de acción, que el lokono forma con "
               "-hi/-hù sobre el mismo verbo (p. 612). La achagua hace el mismo par "
               "sobre una raíz: `carruicay` 'espanto' / `carrunatacayi` 'espantoso' "
               "(neira-ribero-1762). DUDOSO declarado: glosa mixta cualidad+nombre; "
               "se mantiene verbal porque dos de las tres acepciones lo son, y "
               "porque `etamo` es la voz que MANDA en el par 18 de la política "
               "atestiguado-manda (archivó `mülia`)."},
    "guaidima": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Integro' = 'entero'. El lexicón ya trae el wayuu `waneepiaa` "
               "'ser entero, -ra; ser' — la glosa misma lo declara verbo. Achagua "
               "`jaubearuba` 'cabal, entero' (neira-ribero-1762)."},
    "guaranao": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Salado, ácido' son sabores, y los sabores son 4ª conjugación "
               "estativa en lokono (perea-alonso-1942 p. 634). El lexicón ya trae el "
               "wayuu `palawaa` 'ser salado, -da'."},
    "guasima": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Viejo, anciano'. El apoyo es literal: `hebbe-n` 'ser viejo' es UNO "
               "de los tres ejemplos con que Perea define la 4ª conjugación estativa "
               "(perea-alonso-1942 p. 634), y `hebbe` ya está en el lexicón como "
               "v_raiz 'ser viejo, anciano'. DUDOSO declarado: 'anciano' también "
               "puede leerse como nombre de edad (cf. `wanü` 'anciano, mayor', sust); "
               "manda el apoyo literal, que es de la misma glosa."},
    "patapati": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Anegadizo' es propiedad del terreno, y los estados son 4ª "
               "conjugación lokono (perea-alonso-1942 p. 634). La forma es además "
               "reduplicada, y la reduplicación caquetía es productiva y medida "
               "(morfologia.md §4, gatschet-1885). deuda: sin-procedencia para el "
               "cognado — ninguna hermana da 'anegadizo' con glosa idéntica."},
    "singuanguso": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Insolente' es cualidad de carácter; entra por la regla general de "
               "Perea (perea-alonso-1942 pp. 598-599/608: nombre, adjetivo o "
               "partícula se hacen verbo). deuda: sin-procedencia — ninguna hermana "
               "da 'insolente' con glosa idéntica."},
    "usera": {
        "cat": "v_estativo", "clase": "estativo",
        "por": "'Seco, arenoso'. El lexicón ya trae el wayuu `josoo` 'estar seco, "
               "-ca' con la glosa en forma verbal. Paraujano `jaradu` 'seco' "
               "(oliver-1989-apendice-a, tabla A-2). Y la achagua lo predica con el "
               "privativo ma-: `macarray` 'seco', `macarracataní` 'seco, estando "
               "seco' (neira-ribero-1762), que es el mecanismo de van Buurt §8 "
               "(van-buurt-2014)."},

    # ── ACCIONES: verbo pleno, la glosa de la fuente es un infinitivo ──
    "badamaro": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Extraer, sacar', dos infinitivos transitivos. Lokono `lluccu-waria` "
               "'sacar' (perea-alonso-1942). La achagua los marca con el pronombre "
               "PREFIJADO nu-, que es la marca del transitivo (perea-alonso-1942 "
               "p. 635): `numunuayu` 'sacar una espina', `nusiguiayu` 'sacar "
               "estrujando' (neira-ribero-1762)."},
    "beceremicore": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Dominar, triunfar, victoria': dos infinitivos y su nombre de "
               "acción, que el lokono forma con -hù/-hi sobre el verbo "
               "(perea-alonso-1942 p. 612). Achagua `nunisau` 'vencer, concluir' "
               "(neira-ribero-1762). DUDOSO declarado por la glosa mixta."},
    "domaria": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Enredarse, atormentar'. El primero es reflexivo/medio, que en "
               "lokono es una conjugación entera —la 3ª, en -n-nua "
               "(perea-alonso-1942 p. 629)—, y sólo un verbo puede tener voz media."},
    "durigua": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Hacer trabajos cortos': la glosa ES una perífrasis verbal. Lokono "
               "`k-eme-kebbù` 'trabajar' (perea-alonso-1942 p. 648, keme-kebbu-n "
               "'estar atareado'), ya en el lexicón como v_raiz."},
    "guide": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Arreglar, acomodar'. Achagua `nuchuniu` 'acomodar, componer' con "
               "nu- prefijado, o sea transitivo (neira-ribero-1762; "
               "perea-alonso-1942 p. 635)."},
    "jabal": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Adquirir', infinitivo transitivo. deuda: sin-procedencia — ninguna "
               "hermana del repo da 'adquirir' con glosa idéntica; el apoyo es la "
               "glosa de la fuente (zavala-reyes-2015 #168)."},
    "jadarayte": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Recoger', infinitivo. El wayuu del lexicón lo dice en infinitivo "
               "dos veces —`aja'itaa` 'recoger agua', `asukaa` 'recoger leña'— "
               "aunque estén etiquetadas `sust` por el aplanamiento de la "
               "comparanda: se cita la GLOSA, no su cat. deuda: sin-procedencia — "
               "ese wayuu viene de Captain & Captain 2005, que NO es obra de "
               "4-fuentes/bibliografia.yaml, así que no es clave foránea (regla 8)."},
    "quiboata": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Engañar'. Lokono `muli-da` 'engañar' (perea-alonso-1942), ya v_raiz "
               "en el lexicón; achagua `nucharisuedau` 'embaucar, engañar' y "
               "`nuchanisuedau` 'burlar, engañar', con nu- prefijado "
               "(neira-ribero-1762)."},
    "quidiboata": {
        "cat": "v_raiz", "clase": "accion",
        "por": "'Engañar, engañado': verbo y participio de la misma raíz, que es la "
               "prueba interna de que la base es verbal — el lokono forma el "
               "participio pasivo con -sia sobre el verbo (perea-alonso-1942 "
               "p. 612). Comparte raíz con #206 `quiboata`."},

    # ── NOMBRES: sustantivo concreto o abstracto; la cat estaba mal ──
    "aca": {
        "cat": "sust", "clase": "nombre",
        "por": "'Bejuco' es una planta. El propio lexicón ya trae `yaro` 'bejuco. "
               "Planta venenosa' y `naure` 'planta bejucosa' como sust, las dos de "
               "zavala-reyes-2015; achagua `acua` 'sarmiento, bejuco' "
               "(neira-ribero-1762)."},
    "baharuco": {
        "cat": "sust", "clase": "nombre",
        "por": "'Abuelo, viejo': término de parentesco, y el parentesco arahuaco es "
               "nombre poseído — achagua `abi` 'abuelo' (neira-ribero-1762), wayuu "
               "`atuushi` 'abuelo' y `taata` 'papá, abuelo'. DUDOSO declarado: la "
               "segunda acepción ('viejo') sí es estativa, y el par con `guasima` "
               "#145 lo enseña; manda la primera, y en duda se degrada (regla 2)."},
    "baperon": {
        "cat": "sust", "clase": "nombre",
        "por": "'Calabaza con cal': el recipiente del chimó, un objeto. Achagua "
               "`cuirro` 'calabaza, uyama' (neira-ribero-1762); wayuu `aliita` "
               "'totuma', `wüirü` 'auyama'. Gemela de #220 `raporon`."},
    "barbache": {
        "cat": "sust", "clase": "nombre",
        "por": "'Iguana', zoónimo. El lexicón ya trae `iwana` y `higuana` (taíno, "
               "vía brinton-1871) e `iwana-kalinago`, las tres como sust. deuda: "
               "sin-procedencia para el lado caquetío — `barbache` no tiene cognado "
               "hermano; el apoyo es la glosa (zavala-reyes-2015 #33)."},
    "cana": {
        "cat": "sust", "clase": "nombre",
        "por": "'Demonio', ser sobrenatural. Achagua `tanasimi` 'demonio, diablo' "
               "(neira-ribero-1762); wayuu `yolujaa` 'diablo, demonio'."},
    "capo": {
        "cat": "sust", "clase": "nombre",
        "por": "'Duende, ente sobrenatural'. Achagua `guabaimi` 'duende' "
               "(neira-ribero-1762). Y el apoyo interno es fuerte: el compuesto "
               "ATESTIGUADO `capubana` 'duende del cerro' (zavala-reyes-2015 #61) ya "
               "es `sust` en el lexicón, y D9 lo usó como uno de los seis apoyos de "
               "`-bana` 'cerro'. La base de un compuesto nominal atestiguado no es "
               "raíz verbal."},
    "capu": {
        "cat": "sust", "clase": "nombre",
        "por": "'Demonio'. Misma familia que #59 `capo` y misma base de `capubana` "
               "(zavala-reyes-2015 #60/#61; D9, morfologia.md §3). El lazo "
               "referencial del cerro de Santa Ana, que se llamó Cerro de Capú "
               "(velasco-2015-resistencia), es de un NOMBRE, no de un verbo."},
    "carama": {
        "cat": "sust", "clase": "nombre",
        "por": "'Ramazón', colectivo de ramas. Achagua `rinacay` 'rama' "
               "(neira-ribero-1762)."},
    "chuchube": {
        "cat": "sust", "clase": "nombre",
        "por": "'Paraulata', ornitónimo. Es una de las nueve reduplicaciones léxicas "
               "que F11 midió, y 5 de ellas son aves (morfologia.md §4, "
               "gatschet-1885): formación léxica de zoónimo, no morfología viva. Su "
               "gemela `chuchubi` ya es `sust` en el lexicón."},
    "comoho": {
        "cat": "sust", "clase": "nombre",
        "por": "'Higo': el fruto, un nombre. deuda: sin-procedencia para el cognado "
               "— el apoyo es la glosa de la fuente (zavala-reyes-2015 #88)."},
    "despopo": {
        "cat": "sust", "clase": "nombre",
        "por": "'Fuerza', nombre abstracto. En las tres comparandas del lexicón el "
               "concepto es nombre: wayuu `atsüin` 'fuerza', lokono `ansi` 'fuerza "
               "vital', y el propio caquetío `barsure` 'alma, esencia vital, fuerza "
               "interior' (sust, atestiguado: Angulo Molina vía "
               "zavala-reyes-2015). DUDOSO declarado: el wayuu tiene "
               "además `matsüinwaa` 'estar sin fuerza', que es el privativo ma- "
               "sobre la misma raíz y prueba que la raíz SE PREDICA; pero lo que "
               "Zavala glosa es el nombre, y en duda se degrada (regla 2)."},
    "dichiva": {
        "cat": "sust", "clase": "nombre",
        "por": "'Límite, línea'. La achagua distingue las dos cosas: el lindero es "
               "NOMBRE —`rijubana` 'linde', `ypubana` 'coto, lindero'— y para "
               "predicarlo usa otro verbo, `nuyedau rijubanã` 'terminar, poner "
               "lindero' (neira-ribero-1762). 63 usos raíz+aspecto en la base."},
    "guamipa": {
        "cat": "sust", "clase": "nombre",
        "por": "'Hueco, profundidad': la segunda acepción es nombre abstracto y la "
               "primera es nombre de objeto en la achagua, `caricuibai` 'hueco' "
               "(neira-ribero-1762). DUDOSO declarado: 'hueco' admite lectura "
               "adjetival; en duda se degrada (regla 2)."},
    "guaracaro": {
        "cat": "sust", "clase": "nombre",
        "por": "'Tapirama silvestre', fitónimo. El lexicón ya trae `tapirama` "
               "'frijol de grano grande' como sust (retroabstraído de "
               "medina-colina-sxx)."},
    "guica": {
        "cat": "sust", "clase": "nombre",
        "por": "'Yabo', fitónimo (el árbol del cardonal). deuda: sin-procedencia "
               "para el cognado; el apoyo es la glosa (zavala-reyes-2015 #150)."},
    "hueque": {
        "cat": "sust", "clase": "nombre",
        "por": "'Sitio de trabajo': la glosa de la fuente es «sitio de X», un nombre "
               "de lugar. DUDOSO declarado: podría ser la nominalización de un verbo "
               "'trabajar' (el lokono la forma con -hù, perea-alonso-1942 p. 612), "
               "pero lo que la fuente da es el nombre y en duda se degrada."},
    "icoroata": {
        "cat": "sust", "clase": "nombre",
        "por": "'Caraota', fitónimo. El propio minador ya lo declara en "
               "DESMARCADAS_F7: «es la voz caquetía; 'caraota' es su glosa». Cero "
               "usos raíz+aspecto en la base. deuda: sin-procedencia para el "
               "cognado; el apoyo es la glosa (zavala-reyes-2015 #162)."},
    "juri": {
        "cat": "sust", "clase": "nombre",
        "por": "'Viento, ventarrón' — EL CASO CENTRAL, 227 usos raíz+aspecto. En las "
               "tres hermanas 'viento' es nombre y el soplar es verbo aparte: lokono "
               "`wadu-lli` 'viento'; wayuu `wawai` 'viento (de tempestad)' frente a "
               "`waawataa` 'soplar (el viento)'; achagua `nususube` 'viento mío' —un "
               "nombre POSEÍDO con nu-— frente a `risuayu` 'correr viento' y "
               "`guanamatau` 'echarse el viento' (neira-ribero-1762). van Buurt lo "
               "da como RAÍZ nominal `hudi`/`juri` 'viento' en Hudishibana 'llano "
               "ventoso' (van-buurt-2014 §5). Y el propio repo lo lee como nombre: "
               "`jurijurebo` 'Paso de los vientos' es la reduplicación de plural "
               "sobre `juri` (morfologia.md §4)."},
    "laguari": {
        "cat": "sust", "clase": "nombre",
        "por": "'Acacia Espinoza, acacia. Lauadrí', fitónimo. deuda: sin-procedencia "
               "para el cognado; el apoyo es la glosa (zavala-reyes-2015 #182)."},
    "orumo": {
        "cat": "sust", "clase": "nombre",
        "por": "'Urumu. Apamate', fitónimo (Tabebuia). deuda: sin-procedencia para "
               "el cognado; el apoyo es la glosa (zavala-reyes-2015 #187)."},
    "quibaquibi": {
        "cat": "sust", "clase": "nombre",
        "por": "'Baquiano, conocedor': las dos acepciones son nombres de AGENTE en "
               "castellano («un baquiano», «un conocedor»), no adjetivos de estado — "
               "que es lo que la separa de `guasima` 'viejo'. El agentivo arahuaco se "
               "forma sobre el verbo (lokono -ha-li-n 'andador', perea-alonso-1942 "
               "p. 612), pero lo atestiguado aquí es la forma entera. DUDOSO "
               "declarado: si se leyera 'conocedor' como cualidad sería estativo; en "
               "duda se degrada (regla 2)."},
    "quiguagua": {
        "cat": "sust", "clase": "nombre",
        "por": "'Especie de haba grande y blanca', fitónimo. deuda: sin-procedencia "
               "para el cognado; el apoyo es la glosa (zavala-reyes-2015 #215)."},
    "quiricias": {
        "cat": "sust", "clase": "nombre",
        "por": "'Sangre, sangrado'. 'Sangre' es nombre en las tres hermanas —lokono "
               "`ttenna` e `ithihi`, wayuu, achagua `yrraí` (neira-ribero-1762)— y el "
               "lokono tiene ADEMÁS el estativo aparte, `ùttùa` 'ser sangriento, "
               "estar ensangrentado' (perea-alonso-1942 p. 639): la lengua distingue "
               "el nombre del estado, y la glosa de Zavala empieza por el nombre."},
    "raporon": {
        "cat": "sust", "clase": "nombre",
        "por": "'Calabaza con cal'. Gemela de #27 `baperon`, mismo referente y misma "
               "clase; achagua `cuirro` 'calabaza, uyama' (neira-ribero-1762)."},
    "surupa": {
        "cat": "sust", "clase": "nombre",
        "por": "'Blatta orientalis. Cucaracha', zoónimo. Achagua `baderrea` "
               "'cucaracha' (neira-ribero-1762)."},
    "tuba": {
        "cat": "sust", "clase": "nombre",
        "por": "'Aglomeración, montón'. La achagua tiene las DOS voces por separado "
               "—`bambasí` 'montón' (nombre) y `nuetaidau` 'amontonar' (verbo con nu- "
               "prefijado)— y la glosa de Zavala es la del nombre "
               "(neira-ribero-1762). 35 usos raíz+aspecto."},
    "ubeda": {
        "cat": "sust", "clase": "nombre",
        "por": "'Acacia fétida. Mapurite, cují hediondo', fitónimo. deuda: "
               "sin-procedencia para el cognado; el apoyo es la glosa "
               "(zavala-reyes-2015 #266)."},
    "uray": {
        "cat": "sust", "clase": "nombre",
        "por": "'Envoltura o vaina de las cerbatanas': un objeto manufacturado. "
               "deuda: sin-procedencia para el cognado; el apoyo es la glosa "
               "(zavala-reyes-2015 #271)."},
    "ure": {
        "cat": "sust", "clase": "nombre",
        "por": "'Raíz'. Nombre en las tres hermanas: lokono `iikirahi`, wayuu "
               "`ourala`, achagua `baririba` (neira-ribero-1762). Y van Buurt lo "
               "registra como raíz nominal `-ure`/`-huri` 'raíz' (van-buurt-2014 §5, "
               "MORFEMAS_VAN_BUURT). ⚠️ homógrafo del formante toponímico `-ure`, en "
               "disputa con el `-are` 'sitio de' (morfologia.md §5)."},

    # ── ADVERBIO: lo dice la propia fuente ──
    "popoi": {
        "cat": "part", "clase": "adverbio",
        "por": "La glosa de Zavala es «Ahí. **Adverbio de lugar**»: la fuente declara "
               "la parte de la oración. El lexicón ya tiene esa clase y la llama "
               "`part` — `yama` 'aquí, en este lugar (deíctico proximal)' y `kana-pa` "
               "'allá'. Apoyo: lokono `jon` 'allá, allí (adverbio demostrativo "
               "distal)' y `yu-mùn` 'allí' (perea-alonso-1942); achagua `neenì` "
               "'allí' (neira-ribero-1762). 59 usos raíz+aspecto en la base — "
               "«ahí-completivo», que es lo que la heurística permitía decir."},
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
        #
        # …y tampoco casa el homógrafo declarado de OTRA lengua: ver
        # NO_ES_LA_MISMA_VOZ. Sin esa tabla la regeneración BORRA seis
        # entradas atestiguadas del módulo generado.
        hit = next(((l, *lex_idx[norm(l)]) for l in e["lemas"]
                    if norm(l) in lex_idx and norm(l) not in NO_ES_LA_MISMA_VOZ), None)
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
    # La clase de la raíz: qué se declaró y qué sigue en la heurística.
    por_clase: dict[str, list[str]] = {}
    sin_declarar = []
    for t in ("T2_nombres_agente", "T3_concreto", "T4_abstracto"):
        for e in tiers[t]:
            origen = norm(e["lemas"][0])
            forma = e.get("lema_final", origen)
            fila = CLASE_DE_LA_RAIZ.get(origen)
            if fila:
                por_clase.setdefault(fila["clase"], []).append(forma)
            elif _CAT_POR_TIER.get(t) == "v_raiz":
                sin_declarar.append(forma)
    print(f"\n  CLASE DE LA RAÍZ — {sum(len(v) for v in por_clase.values())} declaradas:")
    for clase, formas in sorted(por_clase.items()):
        print(f"     {clase:9} {len(formas):3}  {', '.join(sorted(formas))[:110]}")
    print(f"     sin declarar que salen v_raiz por heurística: "
          f"{sorted(sin_declarar) or 'ninguna'}")
    print(f"     homógrafos de la comparanda que NO son la misma voz: "
          f"{sorted(NO_ES_LA_MISMA_VOZ)}")

    if tiers["MAL_ETIQUETADO"]:
        print(f"\n  ⚠ presentes pero NO etiquetadas 'caquetío' ({len(tiers['MAL_ETIQUETADO'])}):")
        for e in tiers["MAL_ETIQUETADO"]:
            print(f"     {e['lemas'][0]:18} lexicón='{e['forma_lexicon']}' = {e['fuente_actual']}"
                  f"  | Zavala: {e['definicion'][:40]}")


# FALLBACK, no clasificación: la heurística de POS del tier, que se conserva
# para lo que no tenga fila en CLASE_DE_LA_RAIZ. Las 49 entradas que hoy caen
# en T4 la tienen todas, así que hoy este mapa no decide ninguna; si mañana
# el parseo saca una entrada nueva a T4, saldrá `v_raiz` sin declarar y
# `clases_sin_declarar` la delatará en el informe y en el módulo generado.
_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS; el resto, sust


def clase_de(origen: str, tier: str) -> tuple[str, str, str]:
    """(cat, clase, razón) de una entrada, por su grafía de Zavala.

    La fila declarada manda; si no la hay, cae en la heurística del tier y la
    clase queda vacía — que es justamente lo que hay que poder contar.
    """
    fila = CLASE_DE_LA_RAIZ.get(origen)
    if fila:
        return fila["cat"], fila["clase"], fila["por"]
    return _CAT_POR_TIER.get(tier, "sust"), "", ""


# ── GLOSAS CURADAS (`sig`), una a una y con su razón ─────────────────
# `sig` es NUESTRA glosa —la que el agente lee y con la que se buscan pares—,
# distinta de `glosa_fuente`, que es verbatim de Zavala y NO se toca jamás.
# Por defecto `sig` se recorta de la definición literal, que es lo bueno; esta
# tabla es la excepción declarada, para cuando el recorte produce una glosa
# que empareja con otra entrada y hace que el proyecto se invente una
# sinonimia que la lengua no tiene.
#
# La clave es la GRAFÍA DE ZAVALA, como en CLASE_DE_LA_RAIZ.
SIG_CURADO: dict[str, dict] = {
    "turumaco": {
        "sig": "cerro de cima plana, meseta",
        "por": "d21.16 (2026-09-21), punto 5: «cerro, meseta» emparejaba con "
               "`sima` 'cerro, montaña, elevación' y las dos se leían como la "
               "misma palabra. Por el criterio de la propia política d19.b NO "
               "son par —solapamiento parcial, no glosa idéntica— y Miguel: «me "
               "parece bien que convivan sima y turumako […] al final no pasa "
               "nada si hay símiles». Se afinan las dos para que dejen de "
               "emparejar: `turumako` es el cerro de cima plana, que es lo que "
               "'meseta' añade en la propia fuente (zavala-reyes-2015 #262 AM), "
               "y `sima` la elevación a secas. La glosa de la fuente queda "
               "intacta en `glosa_fuente`",
    },
}


# ── LA CAPA CURADA (`fuente`), una a una y con su razón ──────────────
# Hasta el 2026-09-23 toda entrada del vocabulario activo salía
# `caquetío-atestiguado` por el solo hecho de estar en el glosario. Pero
# Zavala es una COMPILACIÓN de nueve autores (ver el CAVEAT DE MÉTODO del
# módulo), y lo que atestigua cada entrada es lo que atestigua su fuente, no
# el glosario. Esta tabla es la excepción declarada: la capa (o la lengua)
# que la entrada lleva cuando su fuente, leída, no la sostiene como caquetía
# atestiguada. `glosa_fuente` y `sig` no se tocan: cambia sólo `fuente`, y
# la razón viaja en `notas`.
#
# La clave es la GRAFÍA DE ZAVALA, como en CLASE_DE_LA_RAIZ y SIG_CURADO.
# Cada fila: `fuente` (un valor de curiana_lexicon.FUENTES_CANONICAS),
# `decision` (quién y cuándo) y `por` (qué dice la fuente, con página); y
# `num`, opcional, cuando dos entradas del glosario dan la misma grafía y la
# fila es sólo de una (el caso de `naure`).
#
# cc.4 (2026-09-23), opción B del issue
# 6-fusion/issues-pendientes/sigla-E-zavala-canon-2026-09-23.md, aceptada con
# el paquete (tf.0, «Vale, vale, vale, vale, vale, vamos.»).
DECISION_SIGLA_E = ("cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves "
                    "1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)")


FUENTE_CURADA: dict[str, dict] = {
    # ── tf.0 (2026-09-23): los pemenos, no los caquetíos ──
    # La trampa de `datihao` (db.2) otra vez: la marca «(Lengua de
    # Venezuela.)» es del glosario que el editor añadió al t. IV de Oviedo, y
    # en el CUERPO (t. II pp. 286 y 294, verificado en imagen) el calabazo de
    # la cal es de los PEMENOS del sur de la laguna de Maracaibo. La etiqueta
    # es `caribe-pemeno`: la lengua de los pemenos, que el canon da como
    # caribe (3-mundo/etnias.yaml etnia-006, con su aviso: la filiación es
    # inferencia de Oliver 1989 pp. 226-228 por los topónimos en -goto y
    # porque «hablan como los bubures»). `normalize_source_language` la
    # resuelve a `caribe-continental`, que es esfera de contacto («los del
    # lago»): préstamo medido aparte, sin penalizar. Una etiqueta sin
    # «caribe» caería en el `return "proto-arahuaco"` por defecto y la
    # declararía arahuaca, que es justo lo que no se sabe.
    "baperon": {
        "fuente": "caribe-pemeno",
        "decision": "tf.0, 2026-09-23 (6-fusion/decisiones_tanda_final_2026-09-23.yaml)",
        "por": "Oviedo y Valdés t. II lib. XXV caps. V y VI (Francisco Martín, "
               "el soldado de Alfínger que vivió como indio; verificado en "
               "imagen). p. 286: «la boca llena de hayo […] é su baperon: este "
               "es un calabaço en que traen los indios çierta manera de cal; "
               "para quitar la hambre, chupándola»; p. 294: «toda aquella "
               "tierra es poblada de indios pemenos». La marca «(Lengua de Venezuela.)» es del "
               "glosario del editor (t. IV, «Baperon y Baperoni»), no de Oviedo: "
               "la trampa de `datihao` (db.2). Es la fuente del BAPÓRON de "
               "Alvarado 1921 p. 20. Pemeno = caribe según el canon "
               "(3-mundo/etnias.yaml etnia-006, filiación inferida por Oliver "
               "1989 pp. 226-228). Detalle en "
               "6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml "
               "§poporo.pasajes.pp-7 y §visto_de_paso.vp-baperon",
    },
    "raporon": {
        "fuente": "caribe-pemeno",
        "decision": "tf.0, 2026-09-23 (6-fusion/decisiones_tanda_final_2026-09-23.yaml)",
        "por": "Oviedo y Valdés t. II lib. XXV caps. V y VI, p. 294 (verificado "
               "en imagen), entre los pemenos del sur de la laguna de Maracaibo: "
               "«salió con sus armas de indio, que eran el arco y las flechas é "
               "dardos é su raporon é hayo […] y el baporon es el calabaço de "
               "la cal para quitar la hambre». Gemela de `baperon` en la misma "
               "página; el glosario del editor del t. IV la remite allí "
               "(«Rapürün [Raporon]: Vide Baperon») con la marca «(Lengua de "
               "Venezuela.)», que no es de Oviedo: la trampa de `datihao` "
               "(db.2). Pemeno = caribe según el canon (3-mundo/etnias.yaml "
               "etnia-006). Detalle en "
               "6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml "
               "§poporo.pasajes.pp-7 y §visto_de_paso.vp-baperon",
    },

    # ── cc.4 (2026-09-23): la sigla (E) de Zavala es Esteves 1989 ──
    # Zavala Reyes 2015 p. 64: «Juan Esteves (E)». Una voz cuya ÚNICA sigla
    # es (E) cita a Esteves copiado por Zavala, no a una fuente más
    # (minar-fuente §8), y la ficha de Esteves ya decía cómo se usa: una
    # etimología suya sin cita es hipotética, sube a reconstruida si corrobora
    # algo que ya teníamos, y sólo es atestiguada si se persigue el documento.
    # Opción B: la capa según lo que Esteves HACE con cada voz —etimología de
    # topónimo, «en caquetío X es Y» o glosa que no está → hipotética; nombre
    # vivo de la península → retroabstraída (precedente chiriware y tukeke,
    # 2026-09-10); etimología que corrobora otra fuente → reconstruida—. Son 40
    # voces: estas 34 viven en este módulo y las otras seis (`bara`, `kari`,
    # `rao`, `saruro`, `siwa`, `wanepe`) en el núcleo de curiana_lexicon.py.
    # `jachos` NO sigue la B: la 6-a, verificada en el DLE, la reasigna a
    # español como `caraota` en D10. La lectura voz por voz, con página, es
    # 6-fusion/sigla_E_zavala_lectura_2026-09-23.yaml; `por` copia su
    # `esteves.lo_que_dice`.
    "aca": {   # → `aka`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#3 Aca (E): Bejuco» la (E) es Esteves 1989, y es su única "
               "fuente: es la etimología de un topónimo, análisis suyo, y ninguna "
               "otra obra la corrobora: hipotética, la regla que la ficha de "
               "Esteves ya tenía. Esteves pp. 83, 105 (verificado: imagen): Sólo "
               "en la Parte II: Acaca, Acarite y Acatuto (p. 83: «Aca: bejuco; "
               "uto: quebrada»). En la p. 105 da «aca: par, casal, pareja»: la "
               "misma forma con dos glosas.",
    },
    "chipare": {   # → `chipare`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#82 Chipare (E): Matapalo» la (E) es Esteves 1989, y es "
               "su única fuente: Esteves nombra una voz VIVA de la península: la "
               "palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves pp. 108, 117 (verificado: "
               "ocr): Ipare (p. 117): «aféresis de chipare, matapalo». En Chipare "
               "(p. 108) no glosa.",
    },
    "dividive": {   # → `dibidibe`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#112 Dividive (E): Árbol cuyo fruto es una baya que da "
               "tinta» la (E) es Esteves 1989, y es su única fuente: Esteves "
               "nombra una voz VIVA de la península: la palabra existe (un nombre "
               "vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves pp. 23, 76, 110 (verificado: ocr): Bibidure (p. 23): "
               "dividive, árbol leguminoso tintóreo; Dividive (p. 110), la glosa "
               "de Zavala entera.",
    },
    "ebo": {   # → `ebo`
        "fuente": "caquetío-reconstruido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#117 Ebo (E): Camino, paso, senda» la (E) es Esteves "
               "1989, y es su única fuente: es etimología suya, pero corrobora una "
               "forma que trae otra fuente y que partimos nosotros: reconstruida. "
               "Esteves pp. 35, 38, 39, 47, 105 (verificado: imagen): Curaidebo "
               "«el paso del Curarí… Ebo: camino, paso, senda» (p. 35), Gisebo (p. "
               "38), Guacurebo «por el sufijo ebo» (p. 39), Jurijurebo «paso, "
               "ruta, valle estrecho, cañón» (p. 47) y Cumarebo (p. 105). "
               "Corrobora: zavala-reyes-2015 p. 66: #75 Cazebo (GC) «Poniente» = "
               "cazi (GC) «sol» + -ebo: «el camino del sol» es partición NUESTRA "
               "(campaña del nominalizador, 2026-09-21)",
    },
    "guica": {   # → `gika`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#150 Güica (E): Yabo» la (E) es Esteves 1989, y es su "
               "única fuente: Esteves nombra una voz VIVA de la península: la "
               "palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves p. 43 (verificado: imagen "
               "(lote del 2026-09-22)): Güica (p. 43): «otro nombre indígena» del "
               "árbol que llaman yabo.",
    },
    "huaymujo": {   # → `huaymujo`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#158 Huaymujo (E): Pequeño cangrejo» la (E) es Esteves "
               "1989, y es su única fuente: Esteves nombra una voz VIVA de la "
               "península: la palabra existe (un nombre vivo es dato); lo que es "
               "suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. "
               "43 (verificado: ocr): Imujo (p. 43): aféresis de huaymujo, pequeño "
               "cangrejo.",
    },
    "jachos": {   # → `jachos`
        "fuente": "español-colonial",
        "decision": DECISION_SIGLA_E,
        "por": "6-a: «jacho» es el castellano «hacho» con la h aspirada. DLE "
               "(dle.rae.es, consultado el 2026-09-23), s.v. hacho¹, de hacha¹ "
               "'vela': 'manojo de paja o esparto encendido para alumbrar' y 'leño "
               "resinoso […] usado para alumbrar'. Reasignada a español como "
               "`caraota` en D10. Esteves p. 33 (verificado: imagen): Cunacho, p. "
               "33: del cunaro «extraían manteca para untar los 'jachos', teas de "
               "madera… para encandilar en labores de pesca nocturna». La palabra "
               "va ENTRE COMILLAS y Esteves no la da por indígena. Con 1-B habría "
               "quedado hipotética; la 6-a, verificada, la saca del caquetío",
    },
    "judereque": {   # → `judereke`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#177 Judereque (E): Árbol ramoso, parecido al chiguare» "
               "la (E) es Esteves 1989, y es su única fuente: Esteves nombra una "
               "voz VIVA de la península: la palabra existe (un nombre vivo es "
               "dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves p. 47 (verificado: imagen): Juderecal (p. 47): colectivo "
               "de judereque, árbol ramoso parecido al chiguare.",
    },
    "juri": {   # → `juri`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#178 Juri (E): Viento, ventarrón» la (E) es Esteves 1989, "
               "y es su única fuente: es la etimología de un topónimo, análisis "
               "suyo, y ninguna otra obra la corrobora: hipotética, la regla que "
               "la ficha de Esteves ya tenía. Esteves pp. 47, 66 (verificado: "
               "imagen): Tres veces y las tres partiendo un topónimo: Judibana "
               "(«Judi, juri: viento. Bana: sitio alto», p. 47), Jurijurebo "
               "(«Juri: viento; Ebo: paso…», p. 47) y Tura, que en el censo de "
               "1881 fue «Hato de Jura» («Jura, juri: ventarrón», p. 66). No cita "
               "a nadie.",
    },
    "carama": {   # → `karama`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#64 Carama (E): Ramazón» la (E) es Esteves 1989, y es su "
               "única fuente: Esteves nombra una voz VIVA de la península: la "
               "palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves p. 98 (verificado: ocr): "
               "Caramabure (p. 98): raíz de las caramas, «raíz de la ramazón».",
    },
    "carapa": {   # → `karapa`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#65 Carapa (E): Árbol resinoso» la (E) es Esteves 1989, y "
               "es su única fuente: Esteves nombra una voz VIVA de la península: "
               "la palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves pp. 27, 98 (verificado: "
               "ocr): Cararapa (p. 27), «forma epentética de carapa, árbol "
               "resinoso»; Carapa (p. 98).",
    },
    "caruca": {   # → `karuka`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#67 Caruca (E): Paja, da consistencia al barro que se "
               "aplica a paredes y techos» la (E) es Esteves 1989, y es su única "
               "fuente: Esteves nombra una voz VIVA de la península: la palabra "
               "existe (un nombre vivo es dato); lo que es suyo, y de Zavala al "
               "copiarlo, es que sea caquetía. Retroabstraída, como chiriware y "
               "tukeke (2026-09-10). Esteves pp. 28, 49 (verificado: imagen): "
               "Caruca (p. 28): hierba áspera para la torta de barro de los "
               "techos; Machuruca (p. 49).",
    },
    "caseto": {   # → `kaseto`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#68 Caseto (E): Planta herbácea» la (E) es Esteves 1989, "
               "y es su única fuente: Esteves nombra una voz VIVA de la península: "
               "la palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves p. 30 (verificado: ocr): "
               "Caseto (p. 30): planta herbácea de las malvas espigadas, "
               "Malvastrum spicatum.",
    },
    "caujaro": {   # → `kaujaro`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#72 Caujaro (E): Árbol de madera blanda, fruta "
               "mucilaginosa, del género cordia» la (E) es Esteves 1989, y es su "
               "única fuente: Esteves nombra una voz VIVA de la península: la "
               "palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves pp. 30, 100 (verificado: "
               "ocr): Caujarito (p. 30), diminutivo de caujaro, Cordia; Caujaro "
               "(p. 100), la glosa de Zavala palabra por palabra.",
    },
    "cayude": {   # → `kayude`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#73 Cayude (E): Árbol frutal, guanábano silvestre, "
               "turagua» la (E) es Esteves 1989, y es su única fuente: Esteves "
               "nombra una voz VIVA de la península: la palabra existe (un nombre "
               "vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves pp. 30, 100 (verificado: imagen (p. 30 en "
               "esteves_paginas_releidas_2026-09-16.yaml)): Cayude (pp. 30 y 100): "
               "árbol anonáceo, turagua.",
    },
    "cuna": {   # → `kuna`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#95 Cuna (E): Pez del golfete de Coro» la (E) es Esteves "
               "1989, y es su única fuente: Esteves nombra una voz VIVA de la "
               "península: la palabra existe (un nombre vivo es dato); lo que es "
               "suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. "
               "33, 44 (verificado: imagen): Cunacho (p. 33): cuna, cunaro, pez "
               "lábrido que abunda en el Golfete; Iticuna (p. 44).",
    },
    "cunaro": {   # → `kunaro`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#96 Cunaro (E): Pez del golfete de Coro. Promicops Guasa» "
               "la (E) es Esteves 1989, y es su única fuente: Esteves nombra una "
               "voz VIVA de la península: la palabra existe (un nombre vivo es "
               "dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves p. 33 (verificado: imagen): Cunacho, p. 33, junto a cuna.",
    },
    "curari": {   # → `kurari`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#97 Curarí (E): Árbol de roble, tecoma» la (E) es Esteves "
               "1989, y es su única fuente: Esteves nombra una voz VIVA de la "
               "península: la palabra existe (un nombre vivo es dato); lo que es "
               "suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. "
               "33, 35, 106 (verificado: imagen): Curaidebo (p. 35): «Curarí: "
               "árbol maderable, tecoma»; la madera de los jachos (p. 33).",
    },
    # ⚠️ DOS entradas del glosario dan la misma grafía normalizada: #185 Naure
    # 'jojoto' y #186 Ñaure 'planta bejucosa'. El módulo generado las emite
    # las dos con la clave `naure` y el dict se queda con la ÚLTIMA (#186),
    # que es la que la medición cuenta. `num` restringe la fila a esa: #185
    # tiene además un testigo fuera de Esteves (Alvarado 1921 p. 226, náura)
    # y su capa no es lo que decidió la 1-B. La colisión es curación de glosas
    # pendiente (issue de la sigla E, §9), no de esta tabla.
    "naure": {   # → `naure`
        "num": 186,
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#186 Ñaure (E): Planta bejucosa» la (E) es Esteves 1989, "
               "y es su única fuente: es un «en caquetío X es Y» que no dice de "
               "dónde sale, y ninguna otra obra lo corrobora: hipotética, la regla "
               "que la ficha de Esteves ya tenía. Esteves p. 37 (verificado: "
               "imagen): Chunaure, p. 37: Chunaure es apellido; «en lengua "
               "caquetía 'ñaure' es planta bejucosa, y 'naure', es jojoto».",
    },
    "taque": {   # → `take`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#236 Taque (E): Árbol nucífero» la (E) es Esteves 1989, y "
               "es su única fuente: Esteves nombra una voz VIVA de la península: "
               "la palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves pp. 61, 132 (verificado: "
               "ocr): Tacal y Tacaduto (p. 61): taque, árbol nucífero.",
    },
    "tauta": {   # → `tauta`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#244 Tauta (E): Pequeña paloma de hábitos ictiófagos» la "
               "(E) es Esteves 1989, y es su única fuente: Esteves nombra una voz "
               "VIVA de la península: la palabra existe (un nombre vivo es dato); "
               "lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. "
               "62 (verificado: ocr): Tausabana (p. 62): tauta, palomita de "
               "hábitos ictiófagos que baja en bandadas a las albuferas.",
    },
    "tigui": {   # → `tigi`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#247 Tigüí (E): Pequeña paloma que se alimenta de peces» "
               "la (E) es Esteves 1989, y es su única fuente: Esteves nombra una "
               "voz VIVA de la península: la palabra existe (un nombre vivo es "
               "dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves p. 63 (verificado: ocr): Ticuí (p. 63): «Tigüí y no Ticuí» "
               "es una palomita que se alimenta de peces.",
    },
    "tijua": {   # → `tijua`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#248 Tijúa (E): Paloma de canto onomatopéyico» la (E) es "
               "Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de "
               "la península: la palabra existe (un nombre vivo es dato); lo que "
               "es suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. "
               "38, 63 (verificado: ocr): Tijuro (p. 63): «se nos ha informado» "
               "que viene de tijua, paloma de canto onomatopéyico, con una copla.",
    },
    "tigua": {   # → `tiwa`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#246 Tigua (E): Árbol rutáceo» la (E) es Esteves 1989, y "
               "es su única fuente: Esteves nombra una voz VIVA de la península: "
               "la palabra existe (un nombre vivo es dato); lo que es suyo, y de "
               "Zavala al copiarlo, es que sea caquetía. Retroabstraída, como "
               "chiriware y tukeke (2026-09-10). Esteves pp. 63, 134 (verificado: "
               "ocr): Tiguadare (p. 63): tigua, árbol rutáceo.",
    },
    "tuba": {   # → `tuba`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#253 Tuba (E): Aglomeración, montón» la (E) es Esteves "
               "1989, y es su única fuente: es la etimología de un topónimo, "
               "análisis suyo, y ninguna otra obra la corrobora: hipotética, la "
               "regla que la ficha de Esteves ya tenía. Esteves pp. 64, 73 "
               "(verificado: imagen): p. 64: Todariquiba no significaría nada, "
               "pero «Tubariquiba» —la forma que él propone en lugar de la de "
               "Castellanos— sería 'pedregal': «Tuba: aglomeración. Quiba: "
               "pedruzco»; y Tubarao, «Tuba: montón». p. 73 (apéndice): el «cuar» "
               "cumanagoto de Caulín «tiene el mismo significado del tuba de los "
               "caquetíos».",
    },
    "tubarao": {   # → `tubarao`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#254 Tubarao (E): Arenales» la (E) es Esteves 1989, y es "
               "su única fuente: es la etimología de un topónimo, análisis suyo, y "
               "ninguna otra obra la corrobora: hipotética, la regla que la ficha "
               "de Esteves ya tenía. Esteves p. 64 (verificado: imagen): Tubarao, "
               "p. 64: «significa arenales. Tuba: montón. Rao: arena».",
    },
    "tuturutos": {   # → `tuturutos`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#264 Tuturutos (E): Hierba de propiedades eméticas. Usado "
               "para cuajar quesos» la (E) es Esteves 1989, y es su única fuente: "
               "Esteves nombra una voz VIVA de la península: la palabra existe (un "
               "nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es "
               "que sea caquetía. Retroabstraída, como chiriware y tukeke "
               "(2026-09-10). Esteves p. 66 (verificado: imagen): Tutubacoa (p. "
               "66): «hemos obtenido dos informaciones»; tuturutos, hierba de "
               "savia emética que cuaja el queso.",
    },
    "ure": {   # → `ure`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#272 Ure (E): Raíz» la (E) es Esteves 1989, y es su única "
               "fuente: es la etimología de un topónimo, análisis suyo, y ninguna "
               "otra obra la corrobora: hipotética, la regla que la ficha de "
               "Esteves ya tenía. Esteves pp. 11, 18, 22 (verificado: ocr): "
               "Abudure (p. 11: «ure… quiere decir: raíz en nuestra primitiva "
               "lengua», y que está en muchos topónimos de Paraguaná) y Babahuro "
               "(p. 18, 'el caño de las raíces'). En la p. 22, a propósito de "
               "Baraivere, trae el único paralelo que da en todo el libro: el "
               "pueblo GUARANÍ «Uretebere» de Cabeza de Vaca, «Ure: raíz; Bere: "
               "amargo». En Parte II lo repite en Camurujure (p. 94) y Guaimure "
               "(p. 112).",
    },
    "guaco": {   # → `wako`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#126 Guaco (E): Planta herbácea de la familia de las "
               "portulacea» la (E) es Esteves 1989, y es su única fuente: Esteves "
               "nombra una voz VIVA de la península: la palabra existe (un nombre "
               "vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea "
               "caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). "
               "Esteves pp. 14, 38 (verificado: ocr): Aguaque (p. 14): viene de "
               "guaco, portulácea, pasto codiciado por las cabras.",
    },
    "guaracaro": {   # → `warakaro`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#138 Guaracaro (E): Tapirama silvestre» la (E) es Esteves "
               "1989, y es su única fuente: Esteves nombra una voz VIVA de la "
               "península: la palabra existe (un nombre vivo es dato); lo que es "
               "suyo, y de Zavala al copiarlo, es que sea caquetía. "
               "Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. "
               "114 (verificado: ocr): Guaracaro (p. 114): planta anual de grano "
               "alimenticio, tapirama silvestre.",
    },
    "guaranao": {   # → `waranao`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#140 Guaranao (E): Salado, ácido» la (E) es Esteves 1989, "
               "y es su única fuente: la glosa de Zavala NO está en la página de "
               "Esteves que la origina, y ninguna otra obra la da: hipotética. "
               "Esteves p. 41 (verificado: imagen): La entrada GUARANAO (p. 41) "
               "describe la salina de Punta Cardón, la fama de su sal para los "
               "ojos (citando a Hill Peña) y la Zona Franca. NO glosa la voz: no "
               "dice «salado» ni «ácido». La búsqueda en las dos partes del OCR da "
               "la voz sólo en esta página.",
    },
    "guarataro": {   # → `warataro`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#141 Guarataro (E): Barro de loza, para la fábrica de "
               "budares y ollas» la (E) es Esteves 1989, y es su única fuente: "
               "Esteves nombra una voz VIVA de la península: la palabra existe (un "
               "nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es "
               "que sea caquetía. Retroabstraída, como chiriware y tukeke "
               "(2026-09-10). Esteves p. 41 (verificado: imagen): Guarataro (p. "
               "41): barro de loza gomoso para budares y ollas; abunda en el "
               "lugar.",
    },
    "guariana": {   # → `wariana`
        "fuente": "caquetío-retroabstraido",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#142 Guariana (E): Arbusto halófilo, frailejón de la "
               "playa. Tabaco pescador» la (E) es Esteves 1989, y es su única "
               "fuente: Esteves nombra una voz VIVA de la península: la palabra "
               "existe (un nombre vivo es dato); lo que es suyo, y de Zavala al "
               "copiarlo, es que sea caquetía. Retroabstraída, como chiriware y "
               "tukeke (2026-09-10). Esteves p. 28 (verificado: imagen): "
               "Cariguariana (p. 28): guariana, arbusto halófilo, «tabaco "
               "pescador».",
    },
    "guaru": {   # → `waru`
        "fuente": "caquetío-hipotético",
        "decision": DECISION_SIGLA_E,
        "por": "1-B. En «#143 Guaru (E): Volturido, cataneja. Ave mayor que el "
               "zamuro» la (E) es Esteves 1989, y es su única fuente: es un «en "
               "caquetío X es Y» que no dice de dónde sale, y ninguna otra obra lo "
               "corrobora: hipotética, la regla que la ficha de Esteves ya tenía. "
               "Esteves p. 42 (verificado: imagen "
               "(esteves_paginas_releidas_2026-09-16.yaml; la p. 42 está escaneada "
               "boca abajo)): Guaruguaja, p. 42: «Guar[a], en caquetío, es el "
               "voltúrido que llamamos cunareja, ave mayor que el zamuro». La saca "
               "del topónimo, que él lee como plural por duplicación (guaraguara).",
    },
}


def _entrada_py(e: dict, tier: str, indent: str = "    ") -> str:
    origen = norm(e["lemas"][0])
    forma = e.get("lema_final", origen)      # Fase 2 de D5: lema fonémico
    verbatim = e["definicion"].replace('"', "'").replace("\\", "")
    sig = verbatim[:78]
    sig = (sig[0].lower() + sig[1:]) if sig else sig
    curado = SIG_CURADO.get(origen)
    if curado:
        sig = curado["sig"]
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
    if curado:
        nota += ("; GLOSA CURADA (`sig`, no `glosa_fuente`): "
                 + " ".join(str(curado["por"]).split()))
    # La capa: `caquetío-atestiguado` salvo excepción declarada en FUENTE_CURADA.
    capa = FUENTE_CURADA.get(origen)
    if capa and capa.get("num") not in (None, e["num"]):
        capa = None                     # la fila es de la otra entrada homógrafa
    fuente = capa["fuente"] if capa else "caquetío-atestiguado"
    if capa:
        por = " ".join(str(capa["por"]).split()).replace('"', "'")
        nota += (f"; CAPA CURADA [{capa['decision']}]: era `caquetío-atestiguado`, "
                 f"pasa a `{fuente}`. {por}")
    cat, _clase, _por = clase_de(origen, tier)
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
            f'"fuente": "{fuente}",{extra} "notas": "{nota}"}},')


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
    L.append("LA CLASE DE LA RAÍZ (2026-09-20): la parte de la oración ya no sale de una")
    L.append("heurística de tier. Cada entrada del vocabulario activo que caía en el cajón")
    L.append("de resto lleva su clase declarada —estativo / acción / nombre / adverbio—")
    L.append("con su apoyo comparativo y su cita, en CLASES_DE_RAIZ_ZAVALA. Importa porque")
    L.append("`cat` verbal alimenta `curiana_lexicon._RAICES_VERB` y con ella")
    L.append("`score_linguistico()`. Ver CLASE_DE_LA_RAIZ en el minador.")
    L.append("")
    L.append("LA CLASE ESTATIVA (2026-09-21, d21.4): las diez raíces estativas se emiten")
    L.append("con `cat: v_estativo` y no con `v_raiz`. Es una etiqueta, no una morfología")
    L.append("nueva: `curiana_lexicon.CATS_VERBALES` la cuenta como verbal, así que toman")
    L.append("los mismos tres aspectos y no sale ni entra ninguna raíz de _RAICES_VERB.")
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

    # ── la clase de la raíz ──
    _todas = [(e, t) for t, _, _ in bloques for e in tiers[t]]
    _clasificadas = [(e, t) for e, t in _todas if norm(e["lemas"][0]) in CLASE_DE_LA_RAIZ]
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# LA CLASE DE LA RAÍZ — por qué cada `cat` es la que es")
    L.append("# ══════════════════════════════════════════════════════════════════")
    L.append("# Hasta el 2026-09-20 la parte de la oración salía de UNA heurística de")
    L.append("# tier (`_CAT_POR_TIER = {\"T4_abstracto\": \"v_raiz\"}`), y el T4 es el")
    L.append("# cajón de resto del minador: de ahí salieron 49 `cat: v_raiz`, que es")
    L.append("# de donde `curiana_lexicon._RAICES_VERB` deja que `score_linguistico()`")
    L.append("# cuente como arahuaco cualquier token cuyo primer segmento sea una de")
    L.append("# ellas. Ahora cada una lleva su clase declarada con su apoyo y su cita")
    L.append("# (regla 8), y las que no tienen cognado lo dicen: `deuda: sin-procedencia`.")
    L.append("#")
    L.append("# Las clases son tres y media:")
    L.append("#   estativo → concepto adjetival que en arahuaco es VERBO (4ª conj.")
    L.append("#              lokono, Perea y Alonso 1942 pp. 634-639) → cat v_estativo")
    L.append("#   accion   → verbo pleno                              → cat v_raiz")
    L.append("#   nombre   → sustantivo concreto o abstracto          → cat sust")
    L.append("#   adverbio → deíctico de lugar (la clase de `yama`)   → cat part")
    L.append("#")
    L.append("# `v_estativo` es de la tanda del 2026-09-21 (d21.4): la clase se declara")
    L.append("# en la CATEGORÍA y llega al prompt, sin importar el alineamiento pospuesto")
    L.append("# del lokono. `curiana_lexicon.CATS_VERBALES` la cuenta como verbal, igual")
    L.append("# que `v_raiz`: un estado se predica con aspecto como una acción.")
    L.append("#")
    L.append("# La declaración de qué es un estativo EN ESTE PROYECTO está propuesta")
    L.append("# en 6-fusion/clases_de_raiz_zavala_2026-09-20.yaml, para 2-lengua/")
    L.append("# morfologia.md. Aquí sólo vive el reparto.")
    L.append("CLASES_DE_RAIZ_ZAVALA: dict[str, dict] = {")
    for e, _t in sorted(_clasificadas, key=lambda x: norm(x[0]["lemas"][0])):
        origen = norm(e["lemas"][0])
        forma = e.get("lema_final", origen)
        fila = CLASE_DE_LA_RAIZ[origen]
        por = " ".join(str(fila["por"]).split()).replace('"', "'")
        L.append(f'    "{forma}": {{"clase": "{fila["clase"]}", "cat": "{fila["cat"]}", '
                 f'"num": {e["num"]}, "forma_zavala": "{origen}",')
        L.append(f'        "por": "{por}"}},')
    L.append("}")
    L.append("")
    L.append("")
    L.append("# Reparto medido, no contado a mano.")
    _por_clase: dict[str, int] = {}
    for e, _t in _clasificadas:
        c = CLASE_DE_LA_RAIZ[norm(e["lemas"][0])]["clase"]
        _por_clase[c] = _por_clase.get(c, 0) + 1
    L.append("REPARTO_DE_CLASES: dict[str, int] = {")
    for c, n in sorted(_por_clase.items()):
        L.append(f'    "{c}": {n},')
    L.append("}")
    L.append("")
    L.append("")
    L.append("# Entradas del vocabulario activo SIN clase declarada: caen en la")
    L.append("# heurística de tier. Si esta lista deja de estar vacía para una que")
    L.append("# salga `v_raiz`, es que el cajón de resto volvió a decidir solo.")
    _sin = sorted({e.get("lema_final", norm(e["lemas"][0]))
                   for e, t in _todas
                   if norm(e["lemas"][0]) not in CLASE_DE_LA_RAIZ
                   and _CAT_POR_TIER.get(t) == "v_raiz"})
    L.append("SIN_CLASE_DECLARADA: list[str] = [")
    for f in _sin:
        L.append(f'    "{f}",')
    L.append("]")
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
    L.append(f'    "clases_declaradas": {len(_clasificadas)},')
    L.append(f'    "clases_sin_declarar": {len(_sin)},')
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
