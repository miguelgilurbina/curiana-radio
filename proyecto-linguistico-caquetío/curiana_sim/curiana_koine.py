"""
CURIANA — Motor de koiné emergente
===================================
Implementa el arco "diverso → converge" del diseño (ver DISENO_KOINE.md):

  1. EMOCIONAR sembrado por agente — semilla de idiolecto (Maturana: la emoción
     como disposición que abre el dominio de lo decible). Extraído del emocionar
     ya latente en los system_prompt, vuelto dato.
  2. IdiolectoAgente — perfil de frecuencia de formas por agente (entrenchment).
     Memoria larga que NO expira (= el "segundo compartimento" de CANON_TIERRA).
     Se pre-carga con las formas-semilla del emocionar → divergencia el día 1.
     La semilla se busca por el nombre de la ERA 1 (ALIAS_ERA1) y, si no hay
     escrita, se DERIVA de la ficha del agente (§ I-b). Ver DISENO_KOINE §4.
  3. CampoLexico — frecuencia comunitaria con decaimiento (rich-get-richer +
     recambio) para muestreo ponderado.
  4. distancia_idiolectal — la métrica que prueba (o refuta) la koineización:
     debe CONTRAERSE en el tiempo.

No hace llamadas LLM: se alimenta de lo que el Observer ya extrae cada turno.
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter, deque
from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# I. EMOCIONAR — semilla de idiolecto por agente
# ══════════════════════════════════════════════════════════════════════
# Estructura: {disposicion, sesgo_lexico (dominios semánticos preferidos),
#              aspecto (sufijo favorito), registro (frase, metafora)}
# Los dominios de sesgo_lexico son las "categoria" de VOCABULARIO_BASE
# (geografia, fauna, flora, cosmos, parentesco, cuerpo, comercio, ritual,
#  alimentos, jerarquia, tiempo).

EMOCIONAR_SEED: dict[str, dict] = {
    # ── Tier I caquetío/caquetía ──
    "Manaure":    {"disposicion": "contención vigilante — la carga del que sostiene el cielo",
                   "sesgo_lexico": ["jerarquia", "cosmos", "comercio"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Shaboro":    {"disposicion": "ternura no nombrada e ironía grave",
                   "sesgo_lexico": ["ritual", "cosmos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "alta"}},
    "Nubiri-sha": {"disposicion": "cálculo afectuoso — la red de deudas y cuidados",
                   "sesgo_lexico": ["parentesco", "comercio", "jerarquia"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "baja"}},
    "Watapana":   {"disposicion": "avidez curiosa — el placer del trato y la novedad",
                   "sesgo_lexico": ["comercio", "geografia", "fauna"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "media"}},
    "Dara-ko":    {"disposicion": "duelo callado volcado en el oficio",
                   "sesgo_lexico": ["geografia", "fauna", "flora"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Paugis-sha": {"disposicion": "franqueza cálida — memoria viva de la comunidad",
                   "sesgo_lexico": ["cuerpo", "flora", "parentesco"],
                   "aspecto": "completivo", "registro": {"frase": "media", "metafora": "media"}},
    "Biro-ko":    {"disposicion": "orgullo terco del oficio de la sal",
                   "sesgo_lexico": ["comercio", "geografia", "alimentos"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Tawaka":     {"disposicion": "ambición tensa, apenas contenida",
                   "sesgo_lexico": ["jerarquia", "cuerpo", "fauna"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Saruro-sha": {"disposicion": "paciencia del hacer — el cuidado de la materia",
                   "sesgo_lexico": ["flora", "alimentos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Chiriware": {"disposicion": "vigilancia dura — el deber de la defensa",
                   "sesgo_lexico": ["jerarquia", "geografia", "cuerpo"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Buio-sha":   {"disposicion": "visión naciente, asombro reverente",
                   "sesgo_lexico": ["ritual", "cosmos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "alta"}},
    "Korie-ko":   {"disposicion": "paciencia de la tierra — la reciprocidad del conuco",
                   "sesgo_lexico": ["flora", "geografia", "tiempo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Dare-nu":    {"disposicion": "apertura ávida — las ganas de pertenecer y aprender",
                   "sesgo_lexico": ["geografia", "fauna", "alimentos"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    # ── Tier I de contacto (insular / caribe) ──
    "Kadushi":    {"disposicion": "asombro del que va y vuelve por el agua abierta",
                   "sesgo_lexico": ["geografia", "comercio", "cosmos"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Marokoto-ni":{"disposicion": "cautela del extraño que mide antes de hablar",
                   "sesgo_lexico": ["comercio", "geografia"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    # ── Tier II foráneos (aportantes de la mezcla koiné) ──
    "Tariwa":     {"disposicion": "respeto mutuo del mar — dos pueblos que se entienden pescando",
                   "sesgo_lexico": ["geografia", "fauna", "comercio"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Kawa-ni":    {"disposicion": "esfuerzo de quien aprende la lengua de prestigio",
                   "sesgo_lexico": ["geografia", "fauna"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Piru-sha":   {"disposicion": "gratitud cautelosa de la recién integrada",
                   "sesgo_lexico": ["parentesco", "alimentos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "baja"}},
    "Nabaraka":   {"disposicion": "astucia del mercader de sierra",
                   "sesgo_lexico": ["comercio", "flora", "geografia"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "baja"}},
    "Raka-bi":    {"disposicion": "esfuerzo de quien aprende la lengua de prestigio",
                   "sesgo_lexico": ["comercio", "geografia"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
}

# Disposición de respaldo por etnia (para agentes sin seed explícita).
_DISPOSICION_ETNIA = {
    "caquetío":  "arraigo sereno en la lengua propia",
    "caquetía":  "arraigo sereno en la lengua propia",
    "caquetío_aruba": "memoria marina del que cruza el agua",
    "guaycarí":  "esfuerzo de quien aprende la lengua de prestigio",
    "guaycarí_caquetío": "vaivén entre dos hablas",
    "jirajara":  "pragmatismo del comerciante de frontera",
    "gayón":     "cautela del vecino serrano",
    "caribe":    "distancia del extraño que mide antes de hablar",
}

_ASPECTO_SUFIJO = {"completivo": "-ka", "continuativo": "-ni", "prospectivo": "-da"}

# Formas-firma por agente: vocabulario caquetío característico que ancla su
# idiolecto desde el día 1 (varias provienen de la línea "Vocabulario que usas"
# de su system_prompt). El `categoria` semántico está vacío en casi todo el
# caquetío activo, así que el sesgo se siembra con estas listas explícitas, no
# por muestreo de dominio. Distintas entre agentes → divergencia inicial.
FORMAS_SEED: dict[str, list[str]] = {
    "Manaure":    ["biro", "barsure", "kali", "kasha", "chiriware", "maa-ka", "naa-ka"],
    "Shaboro":    ["urari", "barsure", "boratio", "saruro", "kasha", "suna-ni", "naba-ni"],
    "Nubiri-sha": ["ama", "buri", "arua", "biro", "konuko", "paa-da", "raka-da"],
    "Watapana":   ["biro", "maure", "kanoa", "habo", "arima", "naa-da", "wana-da"],
    "Dara-ko":    ["kuru", "kanoa", "bara", "arima", "kunaro", "bagre", "wana-ni"],
    "Paugis-sha": ["urari", "arua", "buri", "ama", "kabo", "kono-ka", "wana-ka"],
    "Biro-ko":    ["biro", "habo", "dali", "sima", "naa-ka", "paa-ka"],
    "Tawaka":     ["chiriware", "kabo", "arima", "habo", "wana-da", "naa-da"],
    "Saruro-sha": ["maure", "arua", "naure", "kuru", "kono-ni", "chaa-ni"],
    "Chiriware": ["chiriware", "sima", "habo", "kabo", "wana-ka", "naa-ka"],
    "Buio-sha":   ["barsure", "boratio", "kasha", "suka", "urari", "naba-ni"],
    "Korie-ko":   ["konuko", "buko", "kuru", "dali", "kaya", "kono-ni"],  # buco→buko: fusión D5b, tanda 2026-08-30
    "Dare-nu":    ["kanoa", "arima", "bara", "kuru", "naa-da", "wana-da"],
    "Kadushi":    ["habo", "kanoa", "biro", "kali", "maure", "naa-ni"],
    "Marokoto-ni":["biro", "habo", "kanoa", "arima", "naa-da"],
    "Tariwa":     ["arima", "habo", "bara", "biro", "kanoa", "wana-ni"],
    "Kawa-ni":    ["arima", "habo", "bara", "masa-ni", "naa-ni"],
    "Piru-sha":   ["ama", "buri", "arua", "konuko", "masa-ni"],
    "Nabaraka":   ["maure", "naure", "sima", "biro", "kuru", "paa-da"],
    "Raka-bi":    ["biro", "sima", "habo", "naa-ni", "paa-ni"],
}

# Núcleo caquetío compartido (último recurso, para quien no tiene formas-firma
# NI ficha de la que derivarlas): pronombres y verbos base que cualquiera usa.
# Se combina con el aspecto del emocionar. Es lo que corrió la era 1 en 40 de
# sus 60 agentes (medido 2026-09-16) y por eso allí sólo había 21 vectores-
# semilla distintos de 60.
_NUCLEO_FALLBACK = ["taya", "pia", "nüma", "naa", "wana", "maa", "ka", "mara"]


# ══════════════════════════════════════════════════════════════════════
# I-b. LA SEMILLA POR ALIAS Y LA SEMILLA DERIVADA
# ══════════════════════════════════════════════════════════════════════
# Dos agujeros medidos el 2026-09-16 (analizar_nodos.py, día 3 de la era 2):
#
#   1. `FORMAS_SEED`/`EMOCIONAR_SEED` están indexados por los nombres de la
#      ERA 1, y la campaña de antropónimos (2026-09-14) renombró a 60 de 63
#      agentes. El orquestador siembra con el nombre NUEVO, así que de los 63
#      sólo Manaure encontraba su semilla: 62 de 63 arrancaban con el MISMO
#      vector (`_NUCLEO_FALLBACK` + `-ni`). DISENO_KOINE §4: «sin esta
#      pre-carga, todos arrancan iguales y convergencia no significa nada».
#      → se resuelve el nombre por `ALIAS_ERA1` (curiana_agents es el único
#        que sabe qué elenco está activo). 11 de 63 recuperan así su semilla.
#
#   2. Aun con el alias, 52 de 63 no tienen semilla escrita — ni la tenían en
#      la era 1, donde `FORMAS_SEED` cubre 20 de 60. Para ésos se DERIVA una,
#      de lo que el agente ya trae en su ficha (el módulo generado de la era 2
#      lleva `oficio`, `rol_en_la_casa`, `casa`/`nodo`, `linaje`, `dossier`).
#
# EL PRINCIPIO DE LA SEMILLA DERIVADA (declarado, no inventado por agente):
#
#   (a) Primero, lo que su propia ficha YA dice: las voces caquetías que
#       aparecen literalmente en su `system_prompt`, su `oficio` y su
#       `descripcion`. Es el mismo principio con que se escribió `FORMAS_SEED`
#       («varias provienen de la línea "Vocabulario que usas" de su
#       system_prompt») y es lo más anclado que tiene el agente.
#   (b) Luego, el CAMPO SEMÁNTICO DE SU OFICIO. No se inventa una tabla nueva:
#       se reusa `curiana_lexicon.categorias_relevantes()` —la heurística de
#       palabras clave que ya prioriza el lexicón del prompt por el contexto
#       del turno— aplicada DOS veces: sobre el oficio del agente (qué hace) y
#       sobre la glosa de cada voz del lexicón (qué significa). La semilla sale
#       de la intersección: pesca → voces de mar y orilla; alfarería → barro y
#       vasija; boratio → cosmos y ritual. Medido: 62 de 63 agentes de la era 2
#       disparan al menos una categoría.
#   (c) Y el aspecto del emocionar sobre dos raíces verbales suyas, que es la
#       firma morfológica que las semillas escritas también llevan (`naa-ka`,
#       `wana-ni`…).
#
#   El sorteo dentro del campo es DETERMINISTA: blake2b sobre
#   (semilla del run, nombre del agente, etiqueta), nunca el RNG global —el
#   motor lo comparte con eventos y muestreo— ni `hash()`, que va salado por
#   proceso (PYTHONHASHSEED) y no repetiría un run.
#
#   La capa hipotética NO entra: 35 de sus 38 voces son formas que el proyecto
#   acuñó para la simulación, y sembrarlas adelantaría justo lo que la era 2
#   quiere ver acuñar (perfil `era2`). Las otras tres sí, que es de donde salen
#   las semillas escritas (medido: 88 reconstruido, 31 atestiguado, 3
#   retroabstraído; hipotéticas, cero).
#
#   LA ERA 1 NO CAMBIA: la derivación sólo actúa sobre una ficha que traiga
#   `oficio` —campo que sólo existe en el módulo generado de la era 2—, y en la
#   era 1 `ALIAS_ERA1` está vacío, así que resolver es la identidad.

# Las capas epistémicas de las que puede salir una semilla derivada.
CAPAS_DE_SEMILLA = frozenset({
    "caquetío-atestiguado", "caquetío-reconstruido", "caquetío-retroabstraido",
})

# Los campos de la ficha que dicen QUÉ HACE el agente (el contexto sobre el que
# se pregunta por sus categorías semánticas). Medido sobre la era 2: con
# `oficio` solo, 15 agentes no disparan ninguna; con estos cuatro, 1.
CAMPOS_DEL_OFICIO = ("oficio", "actividades", "rol_en_la_casa", "descripcion")

# Los campos donde se buscan las voces caquetías que el agente YA dice.
CAMPOS_DE_LA_VOZ = ("system_prompt", "oficio", "descripcion")

# Cuántas formas lleva una semilla derivada: 5 del campo + 2 verbos con su
# aspecto = 7, el tamaño de las semillas escritas (6-7 formas cada una).
N_FORMAS_DE_CAMPO = 5
N_VERBOS_DE_ASPECTO = 2

# La semilla del run (`--semilla N`). Cambia el sorteo de las derivadas sin
# tocar las escritas: dos runs con la misma semilla arrancan igual.
SEMILLA_RUN: int = 0

_cache_derivadas: dict = {}


def fijar_semilla(semilla: Optional[int]) -> None:
    """Fija la semilla del sorteo de las semillas derivadas (y limpia la caché).

    La llama el orquestador junto a `random.seed()`. No usa el RNG global a
    propósito: el motor lo comparte con los eventos, el muestreo del prompt y
    los nombramientos, y la pre-carga de idiolectos tiene que ser reproducible
    aunque cambie el orden en que se consume el azar.
    """
    global SEMILLA_RUN
    SEMILLA_RUN = int(semilla) if semilla is not None else 0
    _cache_derivadas.clear()
    _cache_emocionar.clear()      # el aspecto de respaldo sale del mismo dado


def _dado(*partes) -> int:
    """Entero estable a partir de texto. blake2b, no `hash()`: el hash de las
    cadenas va salado por proceso y no repetiría un run."""
    crudo = "|".join(str(p) for p in (SEMILLA_RUN, *partes)).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(crudo, digest_size=8).digest(), "big")


def _sortear(pool, n: int, *clave) -> list:
    """`n` elementos distintos de `pool`, elegidos de forma determinista."""
    opciones = sorted(set(pool))
    if not opciones or n <= 0:
        return []
    elegidas: list = []
    usados: set = set()
    for i in range(min(n, len(opciones))):
        j = _dado(*clave, i) % len(opciones)
        while j in usados:
            j = (j + 1) % len(opciones)
        usados.add(j)
        elegidas.append(opciones[j])
    return elegidas


# ── El elenco activo: quién es quién y cómo se llamaba en la era 1 ──

def _elenco():
    """(ALL_AGENTS, era2→era1) del elenco activo, o ({}, {}) si no se puede.

    Import perezoso: `curiana_agents` decide el elenco al cargarse desde
    CURIANA_ELENCO y este módulo no debe forzar ese momento.
    """
    try:
        import curiana_agents as _ag
    except Exception:                                        # noqa: BLE001
        return {}, {}
    inverso: dict = {}
    for viejo, nuevo in getattr(_ag, "ALIAS_ERA1", {}).items():
        inverso.setdefault(nuevo, viejo)
    return getattr(_ag, "ALL_AGENTS", {}), inverso


def nombre_era1(agente: str) -> Optional[str]:
    """Cómo se llamaba en la era 1 quien hoy se llama `agente`, o None.

    En la era 1 `ALIAS_ERA1` está vacío: devuelve None y todo sigue igual.
    """
    _, inverso = _elenco()
    viejo = inverso.get(agente)
    return viejo if viejo and viejo != agente else None


def _ficha(agente: str) -> dict:
    agentes, _ = _elenco()
    return agentes.get(agente) or {}


def _texto_de(ficha: dict, campos) -> str:
    trozos = []
    for c in campos:
        v = ficha.get(c)
        if isinstance(v, (list, tuple)):
            trozos.extend(str(x) for x in v)
        elif v:
            trozos.append(str(v))
    return " ".join(trozos)


# ── El vocabulario del que sale una semilla derivada, por campo semántico ──

_vocabulario_cache: Optional[tuple] = None


def _nombres_del_elenco() -> set:
    """Los nombres del elenco activo y los de la era 1, en minúsculas.

    49 de los 63 nombres de la era 2 son homógrafos de una clave del lexicón
    (`karebe` cucharón / Karebe la esposa principal). Una voz así puede
    aprenderse jugando —el scorer la cuenta cuando va en minúscula—, pero
    SEMBRARLA es otra cosa: el bloque «sueles decir: …» del prompt le diría al
    agente que suele decir el nombre de un vecino. No entran al pool derivado.
    """
    agentes, _ = _elenco()
    nombres = {n.lower() for n in agentes}
    try:
        import curiana_agents as _ag
        nombres |= {n.lower() for n in getattr(_ag, "AGENTES_ERA1", ())}
        nombres |= {n.lower() for n in getattr(_ag, "ALIAS_ERA1", {})}
    except Exception:                                        # noqa: BLE001
        pass
    return nombres


def _vocabulario_de_semilla() -> tuple:
    """(voces_por_categoria, raices_verbales, todas) del caquetío sembrable.

    La categoría de una voz se resuelve con la MISMA tabla de palabras clave
    que prioriza el lexicón del prompt (`PALABRAS_CLAVE_CATEGORIA`), aplicada a
    su glosa, más su `categoria` declarada cuando la tiene (sólo 28 de 401 la
    traen — por eso no basta con ella, que es lo que ya decía el comentario de
    `FORMAS_SEED`).
    """
    global _vocabulario_cache
    if _vocabulario_cache is not None:
        return _vocabulario_cache
    try:
        from curiana_lexicon import (
            PALABRAS_CLAVE_CATEGORIA, VOCABULARIO_BASE, capa_epistemica,
            categorias_relevantes,
        )
    except Exception:                                        # noqa: BLE001
        _vocabulario_cache = ({}, [], [])
        return _vocabulario_cache

    nombres = _nombres_del_elenco()
    por_categoria: dict[str, list[str]] = {}
    verbos: list[str] = []
    todas: list[str] = []
    for palabra, datos in VOCABULARIO_BASE.items():
        fuente = str(datos.get("fuente") or "")
        if capa_epistemica(fuente) not in CAPAS_DE_SEMILLA:
            continue
        if palabra.lower() in nombres:
            continue
        sig = str(datos.get("sig") or datos.get("es") or "")
        if not sig:
            continue
        todas.append(palabra)
        if datos.get("cat") == "v_raiz":
            verbos.append(palabra)
        cats = set(categorias_relevantes(sig, max_extra=99))
        declarada = str(datos.get("categoria") or "").strip()
        if declarada in PALABRAS_CLAVE_CATEGORIA:
            cats.add(declarada)
        for c in cats:
            por_categoria.setdefault(c, []).append(palabra)
    _vocabulario_cache = (por_categoria, verbos, todas)
    return _vocabulario_cache


_cache_campos: dict = {}


def campos_del_oficio(agente: str) -> list[str]:
    """Las categorías semánticas que dispara el oficio del agente.

    Es `sesgo_lexico` del emocionar (DISENO_KOINE §4: «dominios que alcanza
    primero»), derivado en vez de escrito a mano.
    """
    if agente in _cache_campos:
        return list(_cache_campos[agente])
    ficha = _ficha(agente)
    if not ficha:
        return []
    try:
        from curiana_lexicon import categorias_relevantes
    except Exception:                                        # noqa: BLE001
        return []
    por_categoria, _, _ = _vocabulario_de_semilla()
    contexto = _texto_de(ficha, CAMPOS_DEL_OFICIO)
    campos = sorted(c for c in categorias_relevantes(contexto, max_extra=99)
                    if por_categoria.get(c))
    _cache_campos[agente] = campos
    return list(campos)


def voces_de_la_ficha(agente: str) -> list[str]:
    """Las voces caquetías que la propia ficha del agente ya dice.

    Se descartan los nombres del elenco: `Saruro` la alfarera no siembra
    `saruro` la planta (misma trampa que el filtro de nombres del scorer).
    """
    ficha = _ficha(agente)
    if not ficha:
        return []
    try:
        from curiana_lexicon import formas_en_texto
    except Exception:                                        # noqa: BLE001
        return []
    _, _, todas = _vocabulario_de_semilla()
    sembrables = set(todas)      # ya sin los homógrafos de nombres del elenco
    texto = _texto_de(ficha, CAMPOS_DE_LA_VOZ)
    return sorted(t for t in formas_en_texto(texto) if t in sembrables)


def formas_derivadas(agente: str, emo: dict) -> list[str]:
    """La semilla derivada de la ficha del agente, o [] si no hay de qué.

    Vacía en la era 1 a propósito: sus fichas no traen `oficio`, así que sus
    semillas quedan byte a byte como estaban.
    """
    ficha = _ficha(agente)
    if not ficha.get("oficio"):
        return []
    clave = (agente, emo.get("aspecto", ""))
    if clave in _cache_derivadas:
        return list(_cache_derivadas[clave])

    por_categoria, verbos, todas = _vocabulario_de_semilla()
    formas: list[str] = list(voces_de_la_ficha(agente))[:3]

    campos = campos_del_oficio(agente)
    faltan = N_FORMAS_DE_CAMPO - len(formas)
    if faltan > 0:
        if campos:
            # Una por campo, dando la vuelta: un agente de cinco campos no se
            # queda con cinco voces del primero.
            vuelta = 0
            while faltan > 0 and vuelta < 8:
                for c in campos:
                    if faltan <= 0:
                        break
                    pool = [p for p in por_categoria.get(c, []) if p not in formas]
                    elegida = _sortear(pool, 1, agente, c, vuelta)
                    if elegida:
                        formas.append(elegida[0])
                        faltan -= 1
                vuelta += 1
        else:
            # Residuo declarado: el oficio de 1 de los 63 (Chirwa, «aprendiza
            # de alfarería con Dabuda») no dispara ninguna categoría. Su
            # semilla sale del caquetío sembrable entero, y sigue siendo suya.
            pool = [p for p in todas if p not in formas]
            formas.extend(_sortear(pool, faltan, agente, "sin-campo"))

    suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", "continuativo"), "-ni")
    raices = _sortear(verbos, N_VERBOS_DE_ASPECTO, agente, "verbos")
    formas.extend(f"{r}{suf}" for r in raices)

    salida = list(dict.fromkeys(formas))
    _cache_derivadas[clave] = salida
    return list(salida)


# ── Disposición, aspecto y registro derivados del papel en la casa ──
# Cuando no hay `EMOCIONAR_SEED` escrito (ni propio ni por alias). Se lee sobre
# `rol_en_la_casa` + `oficio`, en este orden: gana la primera clave que case.
# ⚠ El orden es la regla: gana la PRIMERA clave que case, así que lo específico
# va antes que lo general («esposa del apopo» antes que «apopo», «hermano mayor
# de la matriarca» antes que «matriarca»). `python curiana_koine.py` imprime
# qué disposición sale para cada papel del elenco activo.
_DISPOSICION_ROL = (
    ("diao paramount",  "contención vigilante — la carga del que sostiene el cielo de dos nodos"),
    ("esposa principal", "cálculo afectuoso — la red de deudas y cuidados"),
    ("esposa del manaure", "discreción de la que sirve en la casa del señor y sabe"),
    ("esposa del apopo", "vaivén de la que llegó de otra casa y ya manda en ésta"),
    ("esposo entrante", "comedimiento del que llegó del otro nodo y compara en voz baja"),
    ("sobrino candidato", "ambición tensa, apenas contenida"),
    ("hijo del manaure", "dignidad del que sirve sin heredar"),
    ("hermano mayor de la matriarca", "peso del mayor de la casa, que responde sin mandar"),
    ("hermana mayor del manaure", "autoridad callada de la que guarda la casa y su memoria"),
    ("hermana menor del manaure", "lealtad vigilante con lo de su casa"),
    ("ayunante",        "hambre lúcida del que aprende a ver"),
    ("boratio",         "gravedad del que pregunta al cerro y espera respuesta"),
    ("boratia",         "gravedad de la que pregunta y espera respuesta"),
    ("apopo",           "orgullo terco del que responde por su casa"),
    ("matriarca",       "autoridad callada de la que guarda la casa y su memoria"),
    ("anciano",         "paciencia del que ya vio esto antes"),
    ("anciana",         "paciencia de la que ya vio esto antes"),
    ("cantor",          "memoria en voz alta — lo que se canta no se pierde"),
    ("maestra",         "paciencia del hacer — el cuidado de la materia"),
    ("maestro",         "paciencia del hacer — el cuidado de la materia"),
    ("hermana con hijos", "franqueza cálida — el trabajo que no se interrumpe"),
    ("hermana",         "lealtad vigilante con lo de su casa"),
    ("hermano",         "orgullo del oficio bien hecho"),
    ("joven",           "apertura ávida — las ganas de pertenecer y aprender"),
    ("niña",            "curiosidad sin freno, todavía sin vergüenza"),
    ("niño",            "curiosidad sin freno, todavía sin vergüenza"),
)

# Quien decide cierra la frase (completivo); quien aprende o anuncia mira
# adelante (prospectivo); el oficio que no termina se dice continuativo.
_ASPECTO_ROL = (
    ("diao paramount", "completivo"),
    ("esposa del apopo", "continuativo"),
    ("esposa del manaure", "continuativo"),
    ("esposo entrante", "continuativo"),
    ("hermano mayor de la matriarca", "completivo"),
    ("sobrino candidato", "prospectivo"),
    ("ayunante", "prospectivo"),
    ("apopo", "completivo"),
    ("matriarca", "completivo"),
    ("anciano", "completivo"), ("anciana", "completivo"),
    ("joven", "prospectivo"), ("niña", "prospectivo"), ("niño", "prospectivo"),
    ("boratio", "continuativo"), ("boratia", "continuativo"),
)

_REGISTRO_ROL = (
    ("esposa del apopo", {"frase": "media", "metafora": "media"}),
    ("esposa del manaure", {"frase": "media", "metafora": "baja"}),
    ("ayunante", {"frase": "media", "metafora": "alta"}),
    ("boratio", {"frase": "media", "metafora": "alta"}),
    ("boratia", {"frase": "media", "metafora": "alta"}),
    ("cantor", {"frase": "media", "metafora": "alta"}),
    ("vidente", {"frase": "media", "metafora": "alta"}),
    ("diao paramount", {"frase": "corta", "metafora": "baja"}),
    ("apopo", {"frase": "corta", "metafora": "baja"}),
    ("matriarca", {"frase": "corta", "metafora": "baja"}),
    ("anciano", {"frase": "corta", "metafora": "baja"}),
    ("anciana", {"frase": "corta", "metafora": "baja"}),
    ("joven", {"frase": "corta", "metafora": "media"}),
    ("niña", {"frase": "corta", "metafora": "media"}),
    ("niño", {"frase": "corta", "metafora": "media"}),
)

_ASPECTOS = ("completivo", "continuativo", "prospectivo")


def _primera_clave(texto: str, tabla):
    for clave, valor in tabla:
        if clave in texto:
            return valor
    return None


_cache_emocionar: dict = {}


def emocionar_derivado(agente: str) -> Optional[dict]:
    """Emocionar derivado del papel y el oficio del agente, o None si su ficha
    no trae `oficio` (la era 1, donde nada de esto cambia)."""
    if agente in _cache_emocionar:
        return _cache_emocionar[agente]
    ficha = _ficha(agente)
    if not ficha.get("oficio"):
        _cache_emocionar[agente] = None
        return None
    texto = f"{ficha.get('rol_en_la_casa') or ''} {ficha.get('oficio') or ''}".lower()
    campos = campos_del_oficio(agente)
    aspecto = _primera_clave(texto, _ASPECTO_ROL)
    if aspecto is None:
        aspecto = _ASPECTOS[_dado(agente, "aspecto") % len(_ASPECTOS)]
    emo = {
        "disposicion": (_primera_clave(texto, _DISPOSICION_ROL)
                        or _DISPOSICION_ETNIA.get(ficha.get("etnia") or "caquetío",
                                                  "arraigo en la lengua propia")),
        "sesgo_lexico": campos[:3] or ["geografia", "fauna", "alimentos"],
        "aspecto": aspecto,
        "registro": (_primera_clave(texto, _REGISTRO_ROL)
                     or {"frase": "media", "metafora": "media"}),
        "derivado": True,
    }
    _cache_emocionar[agente] = emo
    return emo


def emocionar_de(agente: str, etnia: Optional[str] = None) -> dict:
    """Emocionar sembrado de un agente: el suyo, el de su nombre de la era 1,
    el derivado de su papel y su oficio, o uno de respaldo por etnia."""
    if agente in EMOCIONAR_SEED:
        return EMOCIONAR_SEED[agente]
    viejo = nombre_era1(agente)
    if viejo and viejo in EMOCIONAR_SEED:
        return EMOCIONAR_SEED[viejo]
    derivado = emocionar_derivado(agente)
    if derivado is not None:
        return derivado
    return {
        "disposicion": _DISPOSICION_ETNIA.get(etnia or "caquetío", "arraigo en la lengua propia"),
        "sesgo_lexico": ["geografia", "fauna", "alimentos"],
        "aspecto": "continuativo",
        "registro": {"frase": "media", "metafora": "baja"},
    }


# ── Formas-semilla: vocabulario caquetío característico del agente ──
# Se usa para pre-cargar el idiolecto (divergencia día 1) y para el prompt.

def formas_seed_de(agente: str) -> Optional[list[str]]:
    """La semilla ESCRITA del agente: la suya, o la de su nombre de la era 1.

    None si no tiene ninguna. `FORMAS_SEED` está indexado por los nombres de la
    era 1 y la era 2 renombró a 60 de 63 agentes: sin resolver el alias, 62 de
    63 arrancaban con el mismo vector.
    """
    if agente in FORMAS_SEED:
        return list(dict.fromkeys(FORMAS_SEED[agente]))
    viejo = nombre_era1(agente)
    if viejo and viejo in FORMAS_SEED:
        return list(dict.fromkeys(FORMAS_SEED[viejo]))
    return None


def formas_semilla(agente: str, emo: dict) -> list[str]:
    """Formas-firma del agente, en tres escalones: la escrita (propia o por
    alias), la derivada de su ficha, y —si no hay ficha de la que derivar— el
    núcleo compartido marcado con el aspecto del emocionar."""
    escritas = formas_seed_de(agente)
    if escritas:
        return escritas
    derivadas = formas_derivadas(agente, emo)
    if derivadas:
        return derivadas
    suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", "continuativo"), "-ni")
    base = list(_NUCLEO_FALLBACK)
    base += [f"naa{suf}", f"wana{suf}"]   # verbos base con su aspecto
    return list(dict.fromkeys(base))


# ══════════════════════════════════════════════════════════════════════
# II. IDIOLECTO POR AGENTE — entrenchment + memoria larga
# ══════════════════════════════════════════════════════════════════════

class IdiolectoAgente:
    """Perfil de frecuencia de formas de un agente. No expira en el run."""

    # Turnos de habla que abarca la ventana reciente (~5 días si el agente
    # habla cada turno; más días reales con la rotación de roster).
    VENTANA_TURNOS = 10

    def __init__(self, agente: str, emocionar: Optional[dict] = None, peso_semilla: int = 2):
        self.agente = agente
        self.emocionar = emocionar or {}
        self.frecuencias: Counter[str] = Counter()
        self.acunaciones: set[str] = set()
        self.adopciones: set[str] = set()
        # Ventana de USO REAL (solo lo que el agente dijo, sin semillas):
        # base de la métrica de convergencia por ventana, inmune tanto al
        # sesgo acumulativo como al artefacto de las formas-semilla.
        self.recientes: deque[list[str]] = deque(maxlen=self.VENTANA_TURNOS)
        # Pre-carga: las formas-semilla entran con peso, para que el día 1 ya
        # haya divergencia entre agentes (precondición de la convergencia).
        # Con peso_semilla=0 no se siembra NADA: `Counter[f] += 0` crea la
        # clave con valor cero, y un idiolecto reconstruido (`--continuar`)
        # aparecería con formas que nunca dijo — `len(vector())` las cuenta.
        if peso_semilla:
            for f in formas_semilla(agente, self.emocionar):
                self.frecuencias[f] += peso_semilla

    def registrar(self, formas, neologismos=None, adoptadas=None):
        turno_formas: list[str] = []
        for f in formas or []:
            self.frecuencias[f] += 1
            turno_formas.append(f)
        for neo in neologismos or []:
            forma = getattr(neo, "forma", neo)
            self.acunaciones.add(forma)
            self.frecuencias[forma] += 1
            turno_formas.append(forma)
        for f in adoptadas or []:
            self.adopciones.add(f)
        if turno_formas:
            self.recientes.append(turno_formas)

    def top_formas(self, n: int = 6) -> list[str]:
        return [f for f, _ in self.frecuencias.most_common(n)]

    def vector(self) -> Counter:
        return self.frecuencias

    def vector_reciente(self) -> Counter:
        """Frecuencias SOLO de la ventana de turnos recientes (uso real,
        sin las formas-semilla pre-cargadas)."""
        c: Counter[str] = Counter()
        for turno in self.recientes:
            c.update(turno)
        return c


# ══════════════════════════════════════════════════════════════════════
# III. CAMPO LÉXICO COMUNITARIO — frecuencia + decaimiento
# ══════════════════════════════════════════════════════════════════════

class CampoLexico:
    """Frecuencia comunitaria de formas, con decaimiento por turno (recambio).

    Desde el 2026-09-17 (capa 2 de la escena, PR 4) el campo está partido POR
    ÁMBITO: `{lugar: {forma: peso}}`, y el campo global es la SUMA de los
    lugares. Es la vía 4 del diseño —el muestreo rich-get-richer del prompt—,
    que hasta hoy ponderaba con la frecuencia de los 63 aunque el agente
    estuviera solo en el agua.

    Sin escena hay un único ámbito, el nulo (`None`), y entonces el global ES
    ese diccionario: `pesos` devuelve el mismo objeto de siempre y el muestreo
    sortea exactamente lo mismo. La era 1 no se mueve un byte.
    """

    def __init__(self, decaimiento: float = 0.97):
        self.por_ambito: dict[Optional[str], dict[str, float]] = {}
        self.decaimiento = decaimiento

    # ── El campo global: la suma de los ámbitos ───────────────────────

    @property
    def pesos(self) -> dict[str, float]:
        """El campo de TODA la comunidad. Con un solo ámbito —la era 1— es
        literalmente su diccionario, sin copiar ni sumar nada."""
        if len(self.por_ambito) == 1:
            return next(iter(self.por_ambito.values()))
        total: dict[str, float] = {}
        for pesos in self.por_ambito.values():
            for f, p in pesos.items():
                total[f] = total.get(f, 0.0) + p
        return total

    @pesos.setter
    def pesos(self, valor: dict) -> None:
        """Poner el global sin decir de qué lugar viene lo deja todo en el
        ámbito nulo: es lo que hace `cargar_koine` con un JSON anterior a la
        escena, y es la lectura correcta (aquel run no tenía lugares)."""
        self.por_ambito = {None: dict(valor or {})}

    def pesos_de(self, ambito: Optional[str] = None) -> dict[str, float]:
        """El campo que ve quien está en `ambito`. Sin ámbito, el global.

        Ojo: sin ámbito NO es «el ámbito nulo», es TODO — para que la era 1 y
        la era 2 sin escena vean lo de siempre."""
        if ambito is None:
            return self.pesos
        return self.por_ambito.setdefault(ambito, {})

    def ambitos(self) -> list:
        return list(self.por_ambito)

    # ── Escritura ─────────────────────────────────────────────────────

    def registrar(self, formas, incremento: float = 1.0,
                  ambito: Optional[str] = None):
        """Suma uso en el campo del LUGAR donde se dijo (None = la comunidad
        entera, que es el único lugar que hay sin escena)."""
        pesos = self.por_ambito.setdefault(ambito, {})
        for f in formas or []:
            pesos[f] = pesos.get(f, 0.0) + incremento

    def decaer(self):
        """Aplica decaimiento; descarta lo despreciable (formas que mueren)."""
        self.por_ambito = {
            ambito: {f: p * self.decaimiento
                     for f, p in pesos.items()
                     if p * self.decaimiento > 0.05}
            for ambito, pesos in self.por_ambito.items()
        }

    def peso(self, forma: str, ambito: Optional[str] = None) -> float:
        return self.pesos_de(ambito).get(forma, 0.0)

    def top(self, n: int = 20, excluir: Optional[set] = None,
            ambito: Optional[str] = None) -> list[tuple[str, float]]:
        """Las formas de más peso. `excluir` deja fuera el vocabulario heredado
        (base y plantillas) cuando lo que se quiere ver es lo emergente."""
        items = self.pesos_de(ambito).items()
        if excluir:
            items = [(f, p) for f, p in items if f not in excluir]
        return sorted(items, key=lambda x: x[1], reverse=True)[:n]


# ══════════════════════════════════════════════════════════════════════
# III-b. PERSISTENCIA — para encadenar días (--continuar)
# ══════════════════════════════════════════════════════════════════════
# Miguel, 2026-09-14: «que cada uno de los turnos que equivalen a un día puedan
# irse sumando uno tras de otro, es decir, que los agentes puedan aprender y
# acordarse de lo que hicieron en el turno pasado». El estado, la memoria, el
# lexicón y el observer ya se guardaban en JSON al cerrar un run; lo que no se
# guardaba era la koiné: el idiolecto de cada agente (su manera de hablar
# acumulada) y el campo léxico comunitario. Sin eso, un día encadenado
# arrancaba con la lengua en blanco.

KOINE_PATH = "curiana_koine.json"


def _idiolecto_a_dict(idio: "IdiolectoAgente") -> dict:
    return {
        "agente": idio.agente,
        "emocionar": idio.emocionar,
        "frecuencias": dict(idio.frecuencias),
        "acunaciones": sorted(idio.acunaciones),
        "adopciones": sorted(idio.adopciones),
        "recientes": [list(t) for t in idio.recientes],
    }


def _idiolecto_de_dict(d: dict) -> "IdiolectoAgente":
    # peso_semilla=0: las frecuencias guardadas ya traen las semillas del
    # primer día; volver a sembrarlas las contaría dos veces.
    idio = IdiolectoAgente(d["agente"], d.get("emocionar") or {}, peso_semilla=0)
    idio.frecuencias = Counter(d.get("frecuencias") or {})
    idio.acunaciones = set(d.get("acunaciones") or [])
    idio.adopciones = set(d.get("adopciones") or [])
    for turno in d.get("recientes") or []:
        idio.recientes.append(list(turno))
    return idio


def agentes_sin_precarga(idiolectos: dict, agentes) -> list[str]:
    """Los agentes cuyo idiolecto HEREDADO no trae ni una de sus formas-semilla.

    `cargar_koine` reconstruye con `peso_semilla=0` a propósito —las
    frecuencias guardadas ya traen la semilla del día 1—, así que una cadena
    que arrancó SIN pre-carga (todo run de la era 2 anterior al 2026-09-16) no
    la recupera por seguir encadenando: hay que re-correr desde el día 1. Esto
    lo mide para que el run lo diga en voz alta en vez de callarlo.
    """
    faltan = []
    for nombre, ficha in (agentes or {}).items():
        idio = idiolectos.get(nombre)
        if idio is None or not idio.frecuencias:
            continue
        semilla = set(formas_semilla(nombre, emocionar_de(nombre, ficha.get("etnia"))))
        if semilla and not (semilla & set(idio.frecuencias)):
            faltan.append(nombre)
    return faltan


# En el JSON, el ámbito nulo (la comunidad entera, que es lo único que hay sin
# escena) se escribe con esta llave: JSON no tiene claves `null` en un objeto.
AMBITO_NULO = ""


def guardar_koine(idiolectos: dict, campo: "CampoLexico", path: str = KOINE_PATH) -> None:
    import json
    datos = {
        "idiolectos": {nm: _idiolecto_a_dict(i) for nm, i in idiolectos.items()},
        # `pesos` sigue siendo el GLOBAL: lo leen tests y tooling anteriores a
        # la escena, y es la suma de `por_ambito` por construcción.
        # `por_ambito` es lo que una cadena `--continuar` con escena necesita
        # para no fundir los lugares el día 2.
        "campo": {"pesos": dict(campo.pesos), "decaimiento": campo.decaimiento,
                  "por_ambito": {(a if a is not None else AMBITO_NULO): dict(p)
                                 for a, p in campo.por_ambito.items()}},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)


def cargar_koine(path: str = KOINE_PATH) -> tuple[dict, "CampoLexico"]:
    """Devuelve (idiolectos, campo) tal como quedaron al cerrar el run anterior.
    Lanza FileNotFoundError si no hay nada guardado: continuar sin koiné previa
    no es continuar, y conviene que falle a la vista."""
    import json
    with open(path, encoding="utf-8") as f:
        datos = json.load(f)
    idiolectos = {nm: _idiolecto_de_dict(d) for nm, d in datos.get("idiolectos", {}).items()}
    c = datos.get("campo") or {}
    campo = CampoLexico(decaimiento=float(c.get("decaimiento", 0.97)))
    # Un JSON anterior a la escena sólo trae el global: entra entero al ámbito
    # nulo, que es la lectura correcta —aquel run no tenía lugares.
    campo.pesos = {f: float(p) for f, p in (c.get("pesos") or {}).items()}
    por_ambito = c.get("por_ambito")
    if por_ambito:
        campo.por_ambito = {
            (a or None): {f: float(p) for f, p in (pesos or {}).items()}
            for a, pesos in por_ambito.items()
        }
    return idiolectos, campo


# ══════════════════════════════════════════════════════════════════════
# IV. MÉTRICA DE CONVERGENCIA — distancia idiolectal
# ══════════════════════════════════════════════════════════════════════

def _coseno(a: Counter, b: Counter) -> float:
    comunes = set(a) & set(b)
    if not comunes:
        return 0.0
    num = sum(a[k] * b[k] for k in comunes)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na and nb else 0.0


def distancia_idiolectal(idiolectos: dict[str, "IdiolectoAgente"], min_formas: int = 5,
                         solo: Optional[set] = None, ventana: bool = False,
                         excluir: Optional[set] = None) -> Optional[float]:
    """Distancia idiolectal media (1 - coseno) entre pares de agentes activos.

    Es la firma de la koineización: DEBE CONTRAERSE en el tiempo. Solo se
    consideran agentes con vocabulario suficiente (min_formas).

    `solo`: si se pasa un conjunto de nombres, restringe la medición a esos
    agentes (los que REALMENTE hablaron) — clave porque los idiolectos se
    pre-cargan con formas-semilla para los 60 agentes, y medir sobre todos
    diluiría la señal con vectores estáticos de quienes nunca participaron.

    `ventana`: mide sobre los últimos VENTANA_TURNOS de habla real (sin
    semillas) en vez del acumulado. El acumulado converge en coseno por mera
    acumulación del vocabulario base compartido (artefacto matemático); la
    ventana mide si el habla ACTUAL de los agentes se parece.

    `excluir`: formas a ignorar en los vectores (típicamente el vocabulario
    base heredado). Con ventana+excluir la métrica queda solo sobre formas
    EMERGENTES (neologismos y adopciones), que es donde la koiné se juega.

    Retorna None si menos de 2 agentes tienen vocabulario suficiente bajo
    estos filtros (sin datos ≠ convergencia perfecta).
    """
    vectores = []
    for nombre, idio in idiolectos.items():
        if solo is not None and nombre not in solo:
            continue
        vec = idio.vector_reciente() if ventana else idio.vector()
        if excluir:
            vec = Counter({f: n for f, n in vec.items() if f not in excluir})
        if len(vec) >= min_formas:
            vectores.append(vec)
    if len(vectores) < 2:
        return None
    distancias = []
    for i in range(len(vectores)):
        for j in range(i + 1, len(vectores)):
            distancias.append(1.0 - _coseno(vectores[i], vectores[j]))
    return round(sum(distancias) / len(distancias), 4) if distancias else None


def veredicto_convergencia(
    puntos: list[tuple[int, float]],
    umbral_total: float = 0.05,
    umbral_reciente: float = 0.02,
) -> tuple[str, str]:
    """Clasifica la trayectoria de la distancia idiolectal en el tiempo.

    Un veredicto binario (fin < inicio) marca "converge" aunque la curva haya
    bajado solo al principio y luego se ESTANCARA — el caso típico de un run de
    ablación (baja los primeros días por el mundo compartido, se aplana después
    sin andamiaje). Aquí se mira también la pendiente del último tercio para
    separar convergencia SOSTENIDA de un plateau.

    puntos: lista de (día, distancia) con valores no nulos. Se ordena por día.
    Retorna (codigo, mensaje); codigo ∈ {converge, plateau, diverge, insuficiente}.

      converge     — bajó en total (> umbral_total) y el último tercio sigue
                     bajando (> umbral_reciente).
      plateau      — bajó en total pero el último tercio se estancó o subió.
      diverge      — no bajó en total (se mantuvo o subió).
      insuficiente — menos de 2 puntos comparables.

    Umbrales en cambio RELATIVO (la distancia vive en ~0.4–0.7): total 5%,
    reciente 2%.
    """
    if len(puntos) < 2:
        return ("insuficiente", "datos insuficientes (ningún par de días comparable)")
    pts = sorted(puntos)
    d_ini, d_fin = pts[0][1], pts[-1][1]
    if not d_ini:
        return ("insuficiente", "distancia inicial nula")
    delta_total = (d_fin - d_ini) / d_ini

    # Tramo reciente: desde el inicio del último tercio hasta el final. Con
    # pocos puntos cae a una ventana de 2 (penúltimo → último).
    corte = min(len(pts) - 2, (2 * len(pts)) // 3)
    d_rec_ini = pts[corte][1]
    delta_reciente = (d_fin - d_rec_ini) / d_rec_ini if d_rec_ini else 0.0

    if delta_total <= -umbral_total:
        if delta_reciente <= -umbral_reciente:
            return ("converge", "CONVERGE ✓ (koineización sostenida)")
        return ("plateau", "SE ESTABILIZA ~ (bajó y se estancó — sin convergencia sostenida)")
    return ("diverge", "NO converge ✗ (sin koineización)")


# ══════════════════════════════════════════════════════════════════════
# V. INYECCIÓN EN EL PROMPT
# ══════════════════════════════════════════════════════════════════════

def prompt_emocionar(agente: str, etnia: Optional[str] = None) -> str:
    """Línea de emocionar (Maturana): disposición + firma morfológica.
    Moldea CÓMO lenguajea; el agente nunca habla DE su emoción."""
    emo = emocionar_de(agente, etnia)
    suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", ""), "")
    extra = f" Tu aspecto natural es {suf}." if suf else ""
    return f"[Tu emocionar — moldea cómo hablas, no lo menciones]: {emo['disposicion']}.{extra}"


def prompt_idiolecto(idio: "IdiolectoAgente") -> str:
    """Bloque 'tu manera de hablar' derivado del perfil acumulado (entrenchment).
    Reemplaza los snippets de texto crudo de AgentMemory."""
    top = idio.top_formas(6)
    if not top:
        return ""
    partes = [f"sueles decir: {', '.join(top)}"]
    if idio.acunaciones:
        partes.append(f"acuñaste: {', '.join(sorted(idio.acunaciones)[:4])}")
    return f"[Tu manera de hablar]: {'; '.join(partes)}."


# ══════════════════════════════════════════════════════════════════════
# VI. FIJACIÓN POR COMPETENCIA — la koiné selecciona un nombre por concepto
# ══════════════════════════════════════════════════════════════════════
# Hallazgo (run 9bb920eb): la competencia NO ocurre sola — cada agente acuña
# para un concepto distinto, así que no hay variantes rivales que fijar. Una
# koiné, en cambio, nace de una NECESIDAD REFERENCIAL COMPARTIDA: aparece algo
# nuevo que VARIOS deben nombrar, cada uno propone, y la comunidad fija una
# forma. Por eso la fijación viene en dos piezas: (a) inducir la competencia con
# "eventos de nombramiento" (REFERENTES_NOVEDOSOS), y (b) resolverla aquí.

# Referentes sin palabra caquetía: cosas nuevas (contacto, novedad natural) que
# la comunidad necesita nombrar. Cada uno dispara una competencia.
REFERENTES_NOVEDOSOS: list[dict] = [
    {"id": "cuentas_vidrio", "desc": "unas cuentas brillantes y duras que un mercader trajo de tierras lejanas, nunca vistas aquí"},
    {"id": "cometa",         "desc": "una estrella con cola que cruza el cielo varias noches seguidas"},
    {"id": "eclipse",        "desc": "el sol se oscurece en pleno día y luego vuelve, como si algo lo cubriera"},
    {"id": "fiebre_manchas", "desc": "una fiebre nueva que llena la piel de manchas, que ningún boratio había visto"},
    {"id": "metal_amarillo", "desc": "un trozo de metal amarillo y pesado, distinto del oro conocido, llegado por trueque"},
    {"id": "bestia_orilla",  "desc": "un animal enorme nunca visto, varado y muerto en la orilla del golfete"},
    {"id": "marea_roja",     "desc": "el agua del golfete se tiñe de rojo durante días y mata a los peces"},
    {"id": "tambor_caribe",  "desc": "un tambor de los caribe con un sonido grave y distinto a los nuestros"},
    {"id": "planta_quema",   "desc": "una planta nueva que cura la herida pero quema la boca al probarla"},
    {"id": "cuenta_insular", "desc": "una forma de contar el valor del trueque que enseñó el mensajero de las islas"},
]


class CompetenciaLexica:
    """Acumula soporte (frecuencia × prestigio) de las formas rivales que
    compiten por un MISMO concepto nuevo, y fija una como entrada koiné cuando
    domina su concepto por encima de un umbral."""

    def __init__(self, umbral_fijacion: float = 0.55, soporte_minimo: float = 3.0):
        # concepto_id -> {desc, variantes: Counter(forma->soporte), fijada, fijada_dia}
        self.referentes: dict[str, dict] = {}
        self._forma2concepto: dict[str, str] = {}
        # forma (minúscula) -> los ÁMBITOS donde alguien la PROPUSO (capa 2 de
        # la escena). Vacío sin escena, y entonces el bloque no se filtra.
        self._ambitos_de_forma: dict[str, list] = {}
        self.umbral = umbral_fijacion
        self.soporte_min = soporte_minimo

    def _prestigio(self, agente: str) -> float:
        try:
            from curiana_social import prestigio_de
            return prestigio_de(agente)
        except Exception:
            return 0.3

    def activar(self, concepto_id: str, desc: str):
        self.referentes.setdefault(concepto_id, {
            "desc": desc, "variantes": Counter(), "fijada": None, "fijada_dia": None})

    def proponer(self, concepto_id: str, forma: str, agente: str,
                 ambito: Optional[str] = None):
        """Un agente acuña `forma` para `concepto_id` en un evento de nombramiento.

        `ambito` (capa 2 de la escena): el LUGAR donde estaba al acuñarla. Es
        lo que `prompt_competencias()` filtra: en un lugar sólo circulan las
        formas rivales que se propusieron allí. Sin escena es None, no se
        guarda nada y el bloque sale entero, como siempre."""
        ref = self.referentes.get(concepto_id)
        if ref is None or ref["fijada"] or not forma:
            return
        ref["variantes"][forma] += 1.0 + self._prestigio(agente)
        self._forma2concepto[forma.lower()] = concepto_id
        if ambito:
            lugares = self._ambitos_de_forma.setdefault(forma.lower(), [])
            if ambito not in lugares:
                lugares.append(ambito)

    def ambitos_de_forma(self, forma: str) -> list:
        """Dónde se propuso esa forma rival. [] sin escena."""
        return list(self._ambitos_de_forma.get((forma or "").lower(), ()))

    def registrar_uso(self, forma: str, agente: str):
        """Reuso posterior de una forma en competencia → suma soporte (más leve
        que proponer). Es lo que hace que una variante gane sobre las otras."""
        cid = self._forma2concepto.get((forma or "").lower())
        if not cid:
            return
        ref = self.referentes[cid]
        if ref["fijada"]:
            return
        ref["variantes"][forma] += 0.5 + self._prestigio(agente)

    def evaluar_fijacion(self, dia: int) -> list[tuple[str, str]]:
        """Fija las competencias donde una variante domina. Devuelve las recién
        fijadas [(concepto_id, forma)]."""
        nuevas = []
        for cid, ref in self.referentes.items():
            if ref["fijada"] or len(ref["variantes"]) < 2:
                continue
            total = sum(ref["variantes"].values())
            forma, sup = ref["variantes"].most_common(1)[0]
            if total >= self.soporte_min and sup / total >= self.umbral:
                ref["fijada"] = forma
                ref["fijada_dia"] = dia
                nuevas.append((cid, forma))
        return nuevas

    def activas(self) -> dict[str, dict]:
        return {cid: ref for cid, ref in self.referentes.items()
                if not ref["fijada"] and ref["variantes"]}

    def prompt_competencias(self, top: int = 4,
                            ambito: Optional[str] = None) -> str:
        """Surface las competencias abiertas para que los agentes REUSEN una
        forma rival en vez de inventar otra — así una se impone.

        `ambito` (V3 de la capa 2): sólo las formas rivales que se propusieron
        EN ESTE LUGAR. Un referente cuyas variantes nacieron todas en otra
        parte no sale: aquí no circula ninguna, y el agente no puede «elegir
        una de las que ya circulan» sin haberlas oído. Con `ambito=None` el
        bloque es el de siempre, byte a byte.

        La FIJACIÓN no se parte: sigue siendo comunitaria (el soporte de una
        forma suma venga de donde venga). Lo que el ámbito filtra es lo que se
        VE, no con qué se mide — la misma regla que gobierna los perfiles."""
        lineas = []
        for ref in self.activas().values():
            if ambito is None:
                # La rama de siempre, intacta: `most_common(top)` ordena los
                # empates como `nlargest`, no como `sorted`, y filtrar después
                # no es lo mismo que pedir los N de golpe.
                formas = [f for f, _ in ref["variantes"].most_common(top)]
            else:
                formas = [f for f, _ in ref["variantes"].most_common()
                          if ambito in self.ambitos_de_forma(f)][:top]
            if formas:
                lineas.append(f"{ref['desc']} → {', '.join(formas)}")
        if not lineas:
            return ""
        return ("[La comunidad aún busca nombre para cosas nuevas. Si hablas de "
                "alguna, ELIGE una de las formas que ya circulan, no inventes otra]:\n  "
                + "\n  ".join(lineas))

    def diccionario_koine(self) -> dict[str, dict]:
        """{concepto_id: {desc, forma, dia, soporte, n_variantes}} de las fijadas."""
        out = {}
        for cid, ref in self.referentes.items():
            if ref["fijada"]:
                out[cid] = {
                    "desc": ref["desc"], "forma": ref["fijada"],
                    "dia": ref["fijada_dia"],
                    "soporte": round(ref["variantes"][ref["fijada"]], 2),
                    "n_variantes": len(ref["variantes"]),
                }
        return out

    def reporte(self) -> str:
        lines = ["\n  ── KOINÉ — fijación por competencia ──"]
        fijadas = self.diccionario_koine()
        lines.append(f"  Conceptos nombrados: {len(self.referentes)} | "
                     f"fijados: {len(fijadas)} | en disputa: {len(self.activas())}")
        for cid, d in fijadas.items():
            lines.append(f"    ✓ {d['desc'][:42]:42} → {d['forma']}  "
                         f"(de {d['n_variantes']} variantes, día {d['dia']})")
        for cid, ref in self.activas().items():
            top = ref["variantes"].most_common(3)
            comp = ", ".join(f"{f}({s:.1f})" for f, s in top)
            lines.append(f"    … {ref['desc'][:42]:42} ⚔ {comp}")
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# Smoke test
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("── curiana_koine: smoke test ──")
    idios = {}
    for nm in ("Manaure", "Shaboro", "Dara-ko", "Korie-ko", "Tariwa"):
        emo = emocionar_de(nm)
        idio = IdiolectoAgente(nm, emo)
        idios[nm] = idio
        print(f"  {nm:12} emocionar='{emo['disposicion'][:40]}...'")
        print(f"               semilla: {idio.top_formas(6)}")
        print(f"               {prompt_emocionar(nm)}")

    d0 = distancia_idiolectal(idios)
    print(f"\n  distancia idiolectal inicial (debe ser ALTA): {d0}")

    # Simular convergencia: todos empiezan a usar las mismas formas
    comunes = ["taya", "wana-ka", "para", "biro", "kali", "naa-da", "ka", "mara"]
    for _ in range(30):
        for idio in idios.values():
            idio.registrar(comunes)
    d1 = distancia_idiolectal(idios)
    print(f"  distancia tras 30 turnos de uso común (debe BAJAR): {d1}")
    assert d1 < d0, "la convergencia debería reducir la distancia idiolectal"

    campo = CampoLexico()
    campo.registrar(comunes)
    campo.registrar(["taya", "para"])
    print(f"\n  campo léxico top: {campo.top(4)}")

    # ── competencia: 3 agentes acuñan rivales para un concepto; uno gana ──
    comp = CompetenciaLexica(soporte_minimo=2.0)
    comp.activar("cometa", "estrella con cola")
    comp.proponer("cometa", "kali-dusha", "Manaure")   # cacique, prestigio alto
    comp.proponer("cometa", "suka-wana", "Tariwa")      # foráneo, prestigio bajo
    comp.proponer("cometa", "kali-rua", "Kawa-ni")
    # reuso: la forma del prestigioso se propaga
    for _ in range(4):
        comp.registrar_uso("kali-dusha", "Shaboro")
    fij = comp.evaluar_fijacion(dia=5)
    print(f"  competencia 'cometa' fijada: {fij}")
    assert any(f == "kali-dusha" for _, f in fij), "debería ganar la forma del prestigioso reusada"
    print(f"  diccionario koiné: {comp.diccionario_koine()}")

    # ── la pre-carga de idiolectos del elenco ACTIVO, medida ──────────
    # `CURIANA_ELENCO=era2 python curiana_koine.py` mide la era 2.
    try:
        import curiana_agents as _A
    except Exception:                                        # noqa: BLE001
        _A = None
    if _A is not None and _A.ALL_AGENTS:
        print(f"\n  ── pre-carga de idiolectos · elenco {_A.ELENCO} "
              f"({len(_A.ALL_AGENTS)} agentes) ──")
        vectores, escritas, alias, derivadas, nucleo = {}, 0, 0, 0, 0
        for _nm, _a in _A.ALL_AGENTS.items():
            _emo = emocionar_de(_nm, _a.get("etnia"))
            _formas = formas_semilla(_nm, _emo)
            vectores[_nm] = tuple(sorted(_formas))
            if _nm in FORMAS_SEED:
                escritas += 1
            elif formas_seed_de(_nm):
                alias += 1
            elif formas_derivadas(_nm, _emo):
                derivadas += 1
            else:
                nucleo += 1
        _distintos = len(set(vectores.values()))
        print(f"  semilla escrita propia: {escritas} · por alias: {alias} · "
              f"derivada de la ficha: {derivadas} · núcleo compartido: {nucleo}")
        print(f"  vectores-semilla DISTINTOS: {_distintos} de {len(vectores)}")
        _repes: dict = {}
        for _nm, _v in vectores.items():
            _repes.setdefault(_v, []).append(_nm)
        for _v, _quienes in sorted(_repes.items(), key=lambda kv: -len(kv[1]))[:3]:
            if len(_quienes) > 1:
                print(f"    x{len(_quienes)} iguales: {_quienes[:6]}")
        for _nm in list(_A.ALL_AGENTS)[:4]:
            print(f"    {_nm:14} {formas_semilla(_nm, emocionar_de(_nm))}")

    print("  ✓ smoke test OK")
