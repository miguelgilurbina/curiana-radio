"""
CURIANA — Contagio lingüístico sociolingüístico
================================================

Modelo de difusión léxica entre los 60 agentes (auditoría Opus §5).

El "contagio" del sistema base solo marca una palabra como adoptada cuando
2 agentes distintos la usan, sin propagación dirigida. Este módulo añade:

  1. Un GRAFO SOCIAL (prestigio + vínculos fuertes + co-ubicación dinámica).
  2. DifusionLexica: rastrea la "presión de exposición" de cada neologismo
     sobre cada agente y emite sugerencias léxicas cuando cruza un umbral.
  3. Perfiles DIALECTALES por etnia, con normalización del score (justicia L2):
     un hablante de segunda lengua no se mide al rasero del nativo caquetío.

Integración (en curiana_orchestrator_v2.py):

    from curiana_social import DifusionLexica, prestigio_de, normalizar_por_dialecto

    difusion = DifusionLexica()            # una sola instancia por simulación

    # — al construir el prompt del agente —
    for forma, sig in difusion.sugerencias_para(agent_name, lexico=lexico):
        system_parts.append(
            f"[Has oído '{forma}' (={sig}) en boca de gente que respetas; "
            f"empléala si encaja].")

    # — tras analizar la respuesta del agente —
    for forma in registro.palabras_caquetias:
        difusion.propagar_uso(forma, agent_name, state)
    for neo in registro.neologismos_extraidos:
        difusion.propagar_uso(neo.forma, agent_name, state)

D3 (#34) DECIDIDA el 2026-09-01 — opción A: `normalizar_por_dialecto()` se
cablea en el UMBRAL DEL RESCATE intra-turno (ver `necesita_rescate()` y el
orquestador), y SOLO ahí. El score que se ALMACENA sigue siendo el crudo: la
métrica insignia y la comparabilidad con los runs publicados no cambian. La
"justicia L2" opera donde el score tiene efecto dentro del run (el reintento),
no en el dato — la lección de fase 1 ("el instrumento medía en parte a sus
autores") prohíbe hornear estas constantes en lo almacenado.

Y en ABLACIÓN no hay rescate: es una inyección que empuja convergencia y el
brazo de control corre sin ella. Reserva declarada: las densidades objetivo
siguen siendo constantes de diseño sin base empírica; calibrarlas desde los
runs queda como mejora anotada (6-fusion/decisiones_tanda_2026-09-01.yaml).

⚠ `PRESTIGIO` y `VINCULOS` están escritos con los nombres de la ERA 1 y NO se
reescriben (el canon nombra a la gente así). Se leen por sus dos puertas —
`prestigio_de()` y `vinculos_de()`—, que resuelven `ALIAS_ERA1` y, para quien
no tiene entrada escrita, derivan una de la ficha. Ver § I-b. Nadie debe leer
las tablas directo: en la era 2 sólo UNA de sus 63 claves está viva.
"""

from __future__ import annotations

import re
from typing import Optional

import curiana_agents as _agentes
from curiana_agents import ALL_AGENTS, agents_at_location, get_agent


# ══════════════════════════════════════════════════════════════════════
# I. PRESTIGIO LINGÜÍSTICO — quién marca la norma
# ══════════════════════════════════════════════════════════════════════

# Overrides explícitos para los formadores de norma (cacique, piaches, esposa
# del cacique, mensajero insular...). El resto se deriva por papel (§ I-b) y,
# en último término, por tier/etnia. Indexado por los nombres de la ERA 1: se
# lee con `prestigio_de()`, nunca directo.
PRESTIGIO: dict[str, float] = {
    "Manaure": 1.0,      # Señor de la Curiana, teocrático
    "Shaboro": 1.0,      # piache anciano
    "Nubiri-sha": 0.9,   # esposa del cacique
    "Paugis-sha": 0.85,  # autoridad femenina, conocimiento de plantas
    "Buio-sha": 0.7,     # piache aprendiz
    "Bana-mana": 0.7,
    "Chiriware": 0.65,  # jefe guerrero
    "Watapana": 0.6,
    "Kadushi": 0.55,     # mensajero insular (caquetío_aruba), contacto léxico
}

# Defaults por tier cuando el agente no aparece en PRESTIGIO.
_PRESTIGIO_TIER = {1: 0.5, 2: 0.4, 3: 0.2}

# Etnias foráneas: su norma se propaga poco (L2, baja autoridad lingüística).
_PRESTIGIO_ETNIA_FORANEA = {
    "caribe": 0.15,
    "jirajara": 0.15,
    "gayón": 0.2,
    "guaycarí": 0.25,
    "guaycarí_caquetío": 0.3,
}


# ══════════════════════════════════════════════════════════════════════
# I-b. EL ALIAS Y LA FICHA — de dónde sale el prestigio de quien no tiene
#      entrada escrita
# ══════════════════════════════════════════════════════════════════════
# Mismo agujero que DISENO_KOINE §4 cerró para `FORMAS_SEED`, medido aquí el
# 2026-09-17 (`6-fusion/medicion_prestigio_vinculos_era2_2026-09-17.yaml`):
#
#   `PRESTIGIO` y `VINCULOS` están indexados por los nombres de la ERA 1 y la
#   campaña de antropónimos (2026-09-14) renombró a 60 de 63 agentes, así que
#   de 63 sólo **una clave estaba viva** (Manaure) y los tres destinos de sus
#   vínculos no existían en el elenco: el agente de más prestigio propagaba su
#   habla a tres fantasmas. El prestigio medido en la era 2 era
#   `1.0 ×1 · 0.5 ×16 · 0.4 ×36 · 0.2 ×10` — el TIER con otro nombre — y es el
#   que pondera la fijación de la koiné (`curiana_koine.CompetenciaLexica.
#   _prestigio`, que ya entra por `prestigio_de()`: esa puerta no se duplica).
#
# Se cierra en dos escalones, como `formas_seed_de()`/`emocionar_de()`:
#
#   1. POR ALIAS. El nombre activo se traduce al de la era 1 con `ALIAS_ERA1`
#      (`curiana_agents` es el único que sabe qué elenco corre). Así vuelven
#      las entradas escritas de quien sólo cambió de nombre.
#   2. DERIVADA DE LA FICHA para quien no tiene ninguna. No es una escala
#      nueva: son los valores que la era 1 YA escribió, y cada papel de la era
#      2 se coloca en la banda de su equivalente de la era 1 (el díao en la del
#      cacique, el boratio mayor en la del piache anciano, la esposa principal
#      en la de la esposa del cacique, el ayunante en la del piache aprendiz,
#      el cantor en la de Bana-mana…). Los huecos entre anclas interpolan.
#
# LA ERA 1 NO CAMBIA: allí `ALIAS_ERA1` está vacío (resolver es la identidad) y
# la derivación exige `rol_en_la_casa`, campo que sólo trae el módulo generado
# de la era 2. `test_social.py` compara la tabla ENTERA antes/después.

# El papel que forma norma, con el valor de su equivalente en la era 1. Cada
# fila dice QUÉ CAMPO lee: leer `rol_en_la_casa` y `oficio` como un solo texto
# haría que «cuida a los niños de la casa entera» puntuara como niño.
# ⚠ El orden es la regla: gana la PRIMERA fila que case, así que lo específico
# va antes que lo general («esposa del apopo» antes que «apopo», «hermana de la
# matriarca» antes que «matriarca», «niño» antes que «hijo del Manaure», y
# «ayunante» antes que «boratio mayor», que su propio papel nombra).
# `python curiana_social.py` imprime qué banda le sale a cada agente del elenco
# activo; con `CURIANA_ELENCO=era2`, los 63.
_PRESTIGIO_PAPEL: tuple[tuple[str, str, float], ...] = (
    # ── los oficios que forman norma (se leen en `oficio`) ──
    ("rol",    "ayunante",                   0.70),  # ancla: Buio-sha, piache aprendiz
    ("oficio", "boratia",                    0.85),  # ancla: Paugis-sha, autoridad femenina
    ("oficio", "boratio",                    0.85),
    ("oficio", "vidente",                    0.70),  # el don sin el título
    ("oficio", "cantor",                     0.70),  # ancla: Bana-mana (tier 2 por encima de su tier)
    # ── la cúspide de la polity ──
    ("rol",    "diao paramount",             1.00),  # ancla: Manaure, señor teocrático
    ("rol",    "boratio mayor",              1.00),  # ancla: Shaboro, piache anciano
    ("rol",    "esposa principal",           0.90),  # ancla: Nubiri-sha, esposa del cacique
    # ── la casa del señor ──
    ("rol",    "hermana mayor del manaure",  0.80),  # matriarca del linaje del señor
    ("rol",    "hermana menor del manaure",  0.55),
    ("rol",    "esposa del manaure",         0.50),
    ("rol",    "sobrino candidato",          0.60),  # ancla: Watapana, el que trata y se prepara
    # ── la casa ──
    ("rol",    "esposa del apopo",           0.45),  # el matrimonio, no el cargo
    ("rol",    "esposo entrante",            0.45),
    ("rol",    "hermana de la matriarca",    0.65),
    ("rol",    "hermano mayor de la matriarca", 0.65),
    ("rol",    "matriarca",                  0.75),
    ("rol",    "apopo",                      0.70),
    ("rol",    "anciano con oficio",         0.65),
    ("rol",    "anciana",                    0.65),
    ("rol",    "maestra",                    0.55),  # ancla: Kadushi, el titular de un oficio
    ("rol",    "maestro",                    0.55),
    ("oficio", "maestra",                    0.55),
    ("oficio", "maestro",                    0.55),
    ("rol",    "hermana con hijos",          0.40),
    ("rol",    "hermano adulto",             0.40),
    ("rol",    "hermana",                    0.40),
    ("rol",    "hermano",                    0.40),
    ("rol",    "joven",                      0.30),
    ("rol",    "niña",                       0.20),
    ("rol",    "niño",                       0.20),
    ("rol",    "hijo del manaure",           0.35),  # después de «niño»: Dato tiene 7 años
)

# Un oficio en la convergencia del cerro (`papel_kapubana`) se dice delante de
# los DOS nodos: quien lo tiene habla para más gente que su casa. Es el único
# modificador y va acotado a 1.0.
PESO_KAPUBANA = 0.05

_CAMPO_DEL_PAPEL = {"rol": "rol_en_la_casa", "oficio": "oficio"}


def _ficha(agente: str) -> dict:
    return _agentes.ALL_AGENTS.get(agente) or {}


_inverso_alias: Optional[dict] = None


def nombre_era1(agente: str) -> Optional[str]:
    """Cómo se llamaba en la era 1 quien hoy se llama `agente`, o None.

    En la era 1 `ALIAS_ERA1` está vacío: devuelve None y todo sigue igual.
    (Lo mismo que hace `curiana_koine.nombre_era1` sobre la misma puerta,
    `curiana_agents.ALIAS_ERA1`.)
    """
    global _inverso_alias
    if _inverso_alias is None:
        inverso: dict = {}
        for viejo, nuevo in getattr(_agentes, "ALIAS_ERA1", {}).items():
            inverso.setdefault(nuevo, viejo)
        _inverso_alias = inverso
    viejo = _inverso_alias.get(agente)
    return viejo if viejo and viejo != agente else None


def papel_de(agente: str) -> Optional[tuple[str, str, float]]:
    """La fila de `_PRESTIGIO_PAPEL` que le toca al agente, o None si su ficha
    no dice qué papel tiene (toda la era 1) o ningún papel declarado casa."""
    ficha = _ficha(agente)
    if not ficha.get("rol_en_la_casa"):
        return None
    # `oficio` EMPIEZA por el título cuando lo hay («boratia de pueblo de
    # AMUAY», «cantor de hazañas», «maestra alfarera mayor»), así que se
    # compara por el principio: buscar por dentro haría boratia a Jaiata, la
    # niña que «escucha desde el umbral… en la casa del boratio». En
    # `rol_en_la_casa` sí se busca por dentro: la clave es el papel y el resto
    # del campo es la aclaración («esposa del apopo (del otro nodo)»).
    for fila in _PRESTIGIO_PAPEL:
        campo, clave, _ = fila
        texto = str(ficha.get(_CAMPO_DEL_PAPEL[campo]) or "").lower().lstrip()
        encaja = texto.startswith(clave) if campo == "oficio" else clave in texto
        if encaja:
            return fila
    return None


def prestigio_derivado(agente: str) -> Optional[float]:
    """Prestigio leído de la ficha del agente, o None si no hay de qué.

    None en la era 1 a propósito: sus fichas no traen `rol_en_la_casa`, así que
    su prestigio queda como estaba (explícito > etnia foránea > tier).
    """
    fila = papel_de(agente)
    if fila is None:
        return None
    valor = fila[2]
    if _ficha(agente).get("papel_kapubana"):
        valor += PESO_KAPUBANA
    return round(min(valor, 1.0), 4)


def prestigio_de(agente: str) -> float:
    """Prestigio lingüístico ∈ [0,1] de un agente: explícito > el de su nombre
    de la era 1 > etnia foránea > derivado de su ficha > tier.

    UNA puerta: el contagio (`DifusionLexica.propagar_uso`) y la fijación de la
    koiné (`curiana_koine.CompetenciaLexica._prestigio`) entran por aquí; nadie
    lee `PRESTIGIO[...]` directo.
    """
    if agente in PRESTIGIO:
        return PRESTIGIO[agente]
    viejo = nombre_era1(agente)
    if viejo and viejo in PRESTIGIO:
        return PRESTIGIO[viejo]
    info = get_agent(agente)
    etnia = info.get("etnia")
    if etnia in _PRESTIGIO_ETNIA_FORANEA:
        return _PRESTIGIO_ETNIA_FORANEA[etnia]
    derivado = prestigio_derivado(agente)
    if derivado is not None:
        return derivado
    return _PRESTIGIO_TIER.get(info.get("tier"), 0.2)


# ══════════════════════════════════════════════════════════════════════
# II. GRAFO SOCIAL — vínculos fuertes (mentoría, parentesco, trabajo)
# ══════════════════════════════════════════════════════════════════════

# peso ∈ [0,1] = frecuencia/intensidad del contacto lingüístico. Aristas
# dirigidas: VINCULOS[A][B] = cuánto escucha B a A. Se simetriza en vecinos().
# Indexado por los nombres de la ERA 1, claves Y destinos: se lee con
# `vinculos_de()`, que traduce las dos puntas al elenco activo.
VINCULOS: dict[str, dict[str, float]] = {
    "Shaboro":   {"Buio-sha": 0.95, "Manaure": 0.7, "Bana-mana": 0.5},
    "Manaure":   {"Nubiri-sha": 0.95, "Shaboro": 0.7, "Chiriware": 0.6},
    "Nubiri-sha": {"Manaure": 0.95, "Saruro-sha": 0.5},
    "Paugis-sha": {"Suba-ko": 0.7, "Saruro-sha": 0.5},
    "Chiriware": {"Tawaka": 0.6, "Pari-nu": 0.7},
    "Dara-ko":   {"Dare-nu": 0.9, "Tari-ko": 0.6, "Bagre-ko": 0.5},
    "Korie-ko":  {"Tawaka": 0.5, "Ita-ko": 0.7, "Buko-ko": 0.6},
    "Kadushi":   {"Watapana": 0.5, "Marokoto-ni": 0.4},
    "Watapana":  {"Biro-ko": 0.6, "Bagre-ko": 0.5},
}

# Arista por defecto entre agentes que comparten ubicación en un turno dado.
PESO_COUBICACION = 0.3

# ── Los vínculos que la ficha declara (§ I-b, escalón 2) ──────────────
# Pesos tomados de la tabla escrita, no inventados: 0.6 es su banda de trabajo
# y autoridad dentro de la casa (Manaure→Chiriware, Chiriware→Tawaka), 0.5 la
# del parentesco que cruza de casa (Nubiri-sha→Saruro-sha, Paugis-sha→
# Saruro-sha) y 0.4 su suelo, el trato que se mantiene a distancia
# (Kadushi→Marokoto-ni).
PESO_CASA = 0.6      # la cabeza de tu casa: el apopo y la matriarca
PESO_LINAJE = 0.5    # la mayor de tu linaje que vive en otra casa
PESO_ORIGEN = 0.4    # la casa del sitio del que te trajeron

# Los papeles que responden por una casa. `rol_en_la_casa` empieza por el
# cargo, así que se compara por el principio: «esposa del apopo» NO es el apopo.
_CABEZAS_DE_CASA = ("apopo", "matriarca")


def _es_cabeza(ficha: dict) -> bool:
    rol = str(ficha.get("rol_en_la_casa") or "").strip().lower()
    return rol.startswith(_CABEZAS_DE_CASA) or "diao paramount" in rol


_cache_estructura: dict = {}


def _estructura() -> dict:
    """Lo que el elenco activo declara de sí mismo: los nombres de linaje, las
    cabezas por casa y por sitio. Ninguna lista a mano — se lee del elenco.

    Un nombre de linaje es un valor de `linaje` que es SÓLO el nombre
    ('Corie'); quien vive fuera de su casa lo trae con coletilla ('Corie (el
    suyo, de Tacuato); vive en la casa Buio de los Cayudes').
    """
    if _cache_estructura:
        return _cache_estructura
    agentes = _agentes.ALL_AGENTS
    linajes = {v.strip() for v in
               (str(a.get("linaje") or "") for a in agentes.values())
               if v.strip() and " " not in v.strip()}
    por_casa: dict[str, list[str]] = {}
    por_sitio: dict[str, list[str]] = {}
    for nombre, ficha in sorted(agentes.items()):
        if not _es_cabeza(ficha):
            continue
        if ficha.get("casa"):
            por_casa.setdefault(ficha["casa"], []).append(nombre)
        if ficha.get("sitio"):
            por_sitio.setdefault(ficha["sitio"], []).append(nombre)
    _cache_estructura.update({
        "linajes": frozenset(linajes),
        "cabezas_por_casa": por_casa,
        "cabezas_por_sitio": por_sitio,
    })
    return _cache_estructura


def linaje_de(agente: str) -> Optional[str]:
    """El nombre del linaje (matrilineal) del agente, o None si no tiene uno
    del canon ('propio, sin nombre', 'el de su madre Saruro', None)."""
    crudo = str(_ficha(agente).get("linaje") or "").strip()
    if not crudo:
        return None
    nombre = crudo.split(" ")[0].strip()
    return nombre if nombre in _estructura()["linajes"] else None


def sitio_de_origen(agente: str) -> Optional[str]:
    """El sitio del que lo trajeron, cuando el elenco lo declara y no es el
    suyo. Se lee del tramo de `linaje` ANTERIOR al ';' —el que dice «el suyo,
    de X»—: después del ';' va la casa donde vive, y «los Tacuatos» contiene
    «Tacuato». Por eso también se compara con frontera de palabra.
    """
    ficha = _ficha(agente)
    trozo = str(ficha.get("linaje") or "").split(";")[0]
    if not trozo:
        return None
    propio = ficha.get("sitio")
    for sitio in getattr(_agentes, "SITIOS", {}):
        if sitio != propio and re.search(r"\b%s\b" % re.escape(sitio), trozo):
            return sitio
    return None


def mayor_del_linaje_fuera_de_su_casa(agente: str) -> Optional[str]:
    """La mayor (o el mayor) de su linaje que vive en OTRA casa: el eje de la
    transmisión matrilineal, que en este elenco cruza de casa y de nodo (la
    tía Paugis de Urari, el tío materno de Wamipa en Caseto). Determinista:
    gana la mayor edad y, si empatan, el nombre.
    """
    linaje = linaje_de(agente)
    if not linaje:
        return None
    casa = _ficha(agente).get("casa")
    candidatos = sorted(
        ((-(a.get("edad") or 0), n) for n, a in _agentes.ALL_AGENTS.items()
         if n != agente and a.get("casa") != casa and linaje_de(n) == linaje))
    return candidatos[0][1] if candidatos else None


def vinculos_derivados(agente: str) -> dict[str, float]:
    """Los vínculos que la ficha del agente declara, o {} si no hay de qué.

    Vacía en la era 1 a propósito: sus fichas no traen `rol_en_la_casa`, así
    que allí `vecinos()` queda byte a byte como estaba.
    """
    ficha = _ficha(agente)
    if not ficha.get("rol_en_la_casa"):
        return {}
    est = _estructura()
    red: dict[str, float] = {}

    def _poner(otro, peso):
        if otro and otro != agente:
            red[otro] = max(red.get(otro, 0.0), peso)

    for cabeza in est["cabezas_por_casa"].get(ficha.get("casa"), ()):
        _poner(cabeza, PESO_CASA)
    _poner(mayor_del_linaje_fuera_de_su_casa(agente), PESO_LINAJE)
    for cabeza in est["cabezas_por_sitio"].get(sitio_de_origen(agente), ()):
        _poner(cabeza, PESO_ORIGEN)
    return red


_cache_vinculos: dict = {}


def vinculos_de(agente: str) -> dict[str, float]:
    """Los vínculos fuertes que salen de `agente`, con los nombres del elenco
    ACTIVO: los suyos escritos, los de su nombre de la era 1 (destinos
    traducidos con `resolver_alias` y sin los que el elenco no tiene) y los que
    su ficha declara. UNA puerta: `vecinos()` es su único consumidor y nadie
    lee `VINCULOS[...]` directo.
    """
    if agente in _cache_vinculos:
        return dict(_cache_vinculos[agente])
    escritos = VINCULOS.get(agente)
    if escritos is None:
        viejo = nombre_era1(agente)
        escritos = VINCULOS.get(viejo) if viejo else None
    red = vinculos_derivados(agente)
    for destino, peso in (escritos or {}).items():
        nuevo = _agentes.resolver_alias(destino)
        if nuevo == agente or nuevo not in _agentes.ALL_AGENTS:
            continue          # FUERA_DEL_ELENCO: resolver nunca inventa
        red[nuevo] = max(red.get(nuevo, 0.0), peso)
    _cache_vinculos[agente] = red
    return dict(red)


_cache_grafo: Optional[tuple] = None


def _grafo() -> tuple:
    """(directo, inverso) del grafo resuelto del elenco activo, construido una
    sola vez: `vecinos()` se llama por hablante y por forma de cada turno."""
    global _cache_grafo
    if _cache_grafo is None:
        directo: dict[str, dict[str, float]] = {}
        inverso: dict[str, dict[str, float]] = {}
        for ag in _agentes.ALL_AGENTS:
            red = vinculos_de(ag)
            if not red:
                continue
            directo[ag] = red
            for otro, peso in red.items():
                destino = inverso.setdefault(otro, {})
                destino[ag] = max(destino.get(ag, 0.0), peso)
        _cache_grafo = (directo, inverso)
    return _cache_grafo


def _limpiar_cache() -> None:
    """Olvida el grafo resuelto (para tests que tocan las tablas escritas)."""
    global _cache_grafo, _inverso_alias
    _cache_grafo = None
    _inverso_alias = None
    _cache_vinculos.clear()
    _cache_estructura.clear()


def vecinos(agente: str, state=None) -> dict[str, float]:
    """Red de escucha de un agente: vínculos resueltos (simetrizados) +
    co-ubicación dinámica del turno actual.

    Devuelve {otro_agente: peso} donde peso ∈ [0,1] aproxima cuánta exposición
    léxica recibe ese vecino cuando `agente` habla.
    """
    directo, inverso = _grafo()
    red: dict[str, float] = dict(directo.get(agente, {}))
    # simetría: si otro tiene a `agente` como destino, también lo oye de vuelta
    for otro, peso in inverso.get(agente, {}).items():
        red[otro] = max(red.get(otro, 0.0), peso)

    # co-ubicación: ubicación actual (override) o la por defecto
    info = get_agent(agente)
    ubic = None
    if state is not None:
        ubic = getattr(state, "ubicaciones_override", {}).get(agente)
    if ubic is None:
        ubic = info.get("ubicacion_default")

    if ubic:
        for otro in _agentes_en(ubic, state):
            if otro != agente:
                red[otro] = max(red.get(otro, 0.0), PESO_COUBICACION)
    return red


def _agentes_en(ubicacion: str, state=None) -> list[str]:
    """Agentes presentes en una ubicación, respetando overrides del estado."""
    presentes = set(agents_at_location(ubicacion))
    if state is not None:
        overrides = getattr(state, "ubicaciones_override", {})
        for ag, ub in overrides.items():
            if ub == ubicacion:
                presentes.add(ag)
            else:
                presentes.discard(ag)  # se movió a otra parte
    return sorted(presentes)


# ══════════════════════════════════════════════════════════════════════
# III. DIFUSIÓN LÉXICA — presión de exposición por neologismo
# ══════════════════════════════════════════════════════════════════════

class DifusionLexica:
    """Rastrea la 'presión de exposición' de cada forma léxica emergente sobre
    cada agente. Cuando un agente acumula exposición ≥ umbral, está listo para
    adoptar la palabra y se le sugiere en el prompt."""

    def __init__(self, umbral_adopcion: float = 0.6):
        # forma -> {agente -> exposicion acumulada [0..∞)}
        self.exposicion: dict[str, dict[str, float]] = {}
        # formas que el agente ya ha empleado (no re-sugerir)
        self.usadas_por: dict[str, set[str]] = {}
        self.umbral = umbral_adopcion

    def propagar_uso(self, forma: str, hablante: str, state=None) -> None:
        """Cuando `hablante` usa `forma`, sube la exposición de sus vecinos en
        proporción a (prestigio del hablante × fuerza del vínculo)."""
        if not forma:
            return
        forma = forma.lower().strip()
        self.usadas_por.setdefault(hablante, set()).add(forma)

        pres = prestigio_de(hablante)
        red = vecinos(hablante, state)
        mapa = self.exposicion.setdefault(forma, {})
        for vecino, peso in red.items():
            mapa[vecino] = mapa.get(vecino, 0.0) + pres * peso

    def sugerencias_para(self, agente: str, lexico=None, top: int = 3) -> list[tuple[str, str]]:
        """Formas que `agente` está listo para adoptar (exposición ≥ umbral),
        excluyendo las que ya usó. Ordenadas por exposición descendente."""
        ya = self.usadas_por.get(agente, set())
        candidatas = []
        for forma, mapa in self.exposicion.items():
            if forma in ya:
                continue
            exp = mapa.get(agente, 0.0)
            if exp >= self.umbral:
                sig = ""
                if lexico is not None and hasattr(lexico, "significado"):
                    sig = lexico.significado(forma) or ""
                candidatas.append((forma, sig, exp))
        candidatas.sort(key=lambda x: x[2], reverse=True)
        return [(f, s) for f, s, _ in candidatas[:top]]

    def exposicion_de(self, agente: str, forma: str) -> float:
        """Exposición acumulada de un agente a una forma (para inspección/tests)."""
        return self.exposicion.get(forma.lower().strip(), {}).get(agente, 0.0)


# ══════════════════════════════════════════════════════════════════════
# IV. VARIACIÓN DIALECTAL — sesgos por etnia y normalización del score
# ══════════════════════════════════════════════════════════════════════

# La variación es por ETNIA/ROL (sociolingüística real), no por tier (artefacto
# de coste). densidad_objetivo = cuánto caquetío se espera de ese grupo.
DIALECTOS: dict[str, dict] = {
    "caquetío":         {"densidad_objetivo": 0.65, "rasgos": []},
    "caquetía":         {"densidad_objetivo": 0.65, "rasgos": []},
    "caquetío_aruba":   {"densidad_objetivo": 0.60,
                         "rasgos": ["lenición -k- > -g-", "léxico marino insular"]},
    "guaycarí":         {"densidad_objetivo": 0.45,
                         "rasgos": ["sintaxis SVO ocasional", "errores de prefijo"]},
    "guaycarí_caquetío": {"densidad_objetivo": 0.50,
                          "rasgos": ["mezcla guaycarí-caquetía"]},
    "gayón":            {"densidad_objetivo": 0.40,
                         "rasgos": ["orden de palabras alterado"]},
    "jirajara":         {"densidad_objetivo": 0.35,
                         "rasgos": ["orden de palabras alterado", "prefijos mal aplicados"]},
    "caribe":           {"densidad_objetivo": 0.25,
                         "rasgos": ["SVO estricto", "léxico caquetío mínimo"]},
}

# Densidad de referencia (la del nativo caquetío). El score se normaliza contra ella.
_DENSIDAD_REF = DIALECTOS["caquetío"]["densidad_objetivo"]


def perfil_dialectal(etnia: str | None) -> dict:
    """Perfil dialectal de una etnia (caquetío nativo por defecto / T3 sin etnia)."""
    return DIALECTOS.get(etnia or "caquetío", DIALECTOS["caquetío"])


def rasgos_dialectales(etnia: str | None) -> list[str]:
    """Rasgos de estilo a inyectar en el prompt del agente según su etnia."""
    return perfil_dialectal(etnia).get("rasgos", [])


def normalizar_por_dialecto(score_crudo: float, etnia: str | None) -> float:
    """Normaliza el score por la densidad objetivo del dialecto (justicia L2):
    un guaycarí no debe penalizarse al rasero del nativo. Acotado a [0,10]."""
    objetivo = perfil_dialectal(etnia)["densidad_objetivo"] or _DENSIDAD_REF
    return round(min(score_crudo * (_DENSIDAD_REF / objetivo), 10.0), 1)


def necesita_rescate(metr: dict, etnia: str | None, ablacion: bool = False) -> bool:
    """D3 (#34, decidida 2026-09-01): ¿la respuesta amerita el reintento
    intra-turno? El umbral se evalúa sobre el score NORMALIZADO por dialecto
    (justicia L2: el caribe no reintenta por obedecer su propio prompt); lo
    que se almacena sigue siendo el score crudo. En ABLACIÓN no hay rescate:
    es una inyección que empuja convergencia y el control corre sin ella."""
    if ablacion:
        return False
    fuga_otra_lengua = (metr.get("otro_arahuaco", 0) >= 3
                        and metr.get("pct_caquetio_especifico", 1) < 0.3)
    return normalizar_por_dialecto(metr["score"], etnia) < 5.0 or fuga_otra_lengua


def prompt_rasgos_dialectales(etnia: str | None) -> str:
    """Fragmento de prompt con la orientación de estilo dialectal (o "" si nativo)."""
    rasgos = rasgos_dialectales(etnia)
    if not rasgos:
        return ""
    return ("[Tu habla, por tu origen, tiene estos rasgos: "
            + "; ".join(rasgos) + ". Es característico, no un error.]")


# ══════════════════════════════════════════════════════════════════════
# V. LA MEDICIÓN — el grafo del elenco activo, para no escribir cifras a mano
# ══════════════════════════════════════════════════════════════════════

def medicion() -> dict:
    """Prestigio y vínculos del elenco ACTIVO, medidos. Es de aquí de donde
    salen las cifras de `6-fusion/medicion_prestigio_vinculos_era2_*.yaml`:
    `python curiana_social.py` (era 1) y `CURIANA_ELENCO=era2 python
    curiana_social.py` (era 2)."""
    agentes = _agentes.ALL_AGENTS
    vivos = set(agentes)
    destinos = {d for orig in VINCULOS.values() for d in orig}

    nodo = {n: (a.get("nodo") or "") for n, a in agentes.items()}
    intra = entre = fantasma = 0
    sin_aristas = []
    for ag in sorted(vivos):
        red = vecinos(ag)
        if not red:
            sin_aristas.append(ag)
        for otro in red:
            if otro not in vivos:
                fantasma += 1
            elif nodo[ag] and nodo[otro] and nodo[ag] != nodo[otro]:
                entre += 1
            else:
                intra += 1

    pres = {n: prestigio_de(n) for n in sorted(vivos)}
    dist: dict[float, int] = {}
    for v in pres.values():
        dist[v] = dist.get(v, 0) + 1
    por_tier: dict = {}
    for n, a in agentes.items():
        por_tier.setdefault(a.get("tier"), set()).add(pres[n])

    cruzados = sorted(n for n in vivos if sitio_de_origen(n))
    cruzan_nodo = sorted(
        n for n in cruzados
        if nodo[n] and nodo[n] != (getattr(_agentes, "SITIOS", {})
                                   .get(sitio_de_origen(n), {}).get("nodo")))
    return {
        "elenco": _agentes.ELENCO, "mundo": _agentes.MUNDO, "agentes": len(vivos),
        "prestigio_claves_vivas": sum(1 for k in PRESTIGIO if k in vivos),
        "prestigio_por_alias": sorted(
            n for n in vivos if n not in PRESTIGIO
            and (nombre_era1(n) or "") in PRESTIGIO),
        "prestigio_derivado": sorted(n for n in vivos
                                     if prestigio_derivado(n) is not None),
        "prestigio_por_tier_solo": sorted(
            n for n in vivos if n not in PRESTIGIO
            and (nombre_era1(n) or "") not in PRESTIGIO
            and prestigio_derivado(n) is None),
        "prestigio_distribucion": dict(sorted(dist.items(), reverse=True)),
        "prestigio_valores_por_tier": {t: sorted(v) for t, v in sorted(
            por_tier.items(), key=lambda kv: (kv[0] is None, kv[0]))},
        "vinculos_claves_vivas": sum(1 for k in VINCULOS if k in vivos),
        "vinculos_claves_por_alias": sorted(
            n for n in vivos if n not in VINCULOS
            and (nombre_era1(n) or "") in VINCULOS),
        "vinculos_destinos_escritos": len(destinos),
        "vinculos_destinos_sin_elenco": sorted(
            d for d in destinos if _agentes.resolver_alias(d) not in vivos),
        "vinculos_derivados": sorted(n for n in vivos if vinculos_derivados(n)),
        "aristas_intra_nodo": intra,
        "aristas_entre_nodos": entre,
        "aristas_a_inexistentes": fantasma,
        "agentes_sin_aristas": sin_aristas,
        "con_sitio_de_origen": cruzados,
        "cruzan_de_nodo": cruzan_nodo,
        "cruzan_de_nodo_en_roster": sorted(
            n for n in cruzan_nodo if agentes[n].get("en_roster")),
    }


# ══════════════════════════════════════════════════════════════════════
# Smoke test
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json
    import sys

    if sys.platform == "win32":                 # la consola de Windows es cp1252
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:                       # noqa: BLE001
            pass

    if "--json" in sys.argv:                    # la medición, sin adornos
        print(json.dumps(medicion(), ensure_ascii=False, default=str))
        raise SystemExit(0)

    print("── curiana_social: smoke test ──")

    if _agentes.ELENCO == "era1":
        d = DifusionLexica()

        # Shaboro (prestigio 1.0) acuña [sima-bana]; su aprendiz Buio-sha (vínculo 0.95)
        # debería cruzar el umbral 0.6 en un solo turno.
        d.propagar_uso("sima-bana", "Shaboro")
        exp_buio = d.exposicion_de("Buio-sha", "sima-bana")
        print(f"  exposición Buio-sha a 'sima-bana' tras 1 uso de Shaboro: {exp_buio:.2f}")
        assert exp_buio >= 0.6, "el aprendiz debería estar listo para adoptar"
        sugs = d.sugerencias_para("Buio-sha")
        print(f"  sugerencias para Buio-sha: {sugs}")
        assert any(f == "sima-bana" for f, _ in sugs)

        # Un periférico (Marokoto-ni, caribe, sin vínculo con Shaboro) no debería adoptar.
        sugs_lejos = d.sugerencias_para("Marokoto-ni")
        print(f"  sugerencias para Marokoto-ni (periférico): {sugs_lejos}")

        # Normalización dialectal: el mismo score crudo vale más para un L2.
        print(f"  score 4.5 caquetío → {normalizar_por_dialecto(4.5, 'caquetío')}")
        print(f"  score 4.5 caribe   → {normalizar_por_dialecto(4.5, 'caribe')}")
        assert normalizar_por_dialecto(4.5, "caribe") > normalizar_por_dialecto(4.5, "caquetío")

        print(f"  prestigio Manaure={prestigio_de('Manaure')}  "
              f"Marokoto-ni={prestigio_de('Marokoto-ni')}  Kori(T3)={prestigio_de('Kori')}")
        print("  ✓ todos los asserts OK")

    # ── la medición del elenco activo (no se escribe ninguna cifra a mano) ──
    m = medicion()
    print(f"\n── el grafo de {m['mundo']} ({m['elenco']}, {m['agentes']} agentes) ──")
    print(f"  PRESTIGIO: {m['prestigio_claves_vivas']} clave(s) viva(s) · "
          f"{len(m['prestigio_por_alias'])} por alias · "
          f"{len(m['prestigio_derivado'])} derivado(s) de la ficha · "
          f"{len(m['prestigio_por_tier_solo'])} sólo por tier")
    print(f"  distribución: {m['prestigio_distribucion']}")
    print(f"  valores por tier: {m['prestigio_valores_por_tier']}")
    print(f"  VINCULOS: {m['vinculos_claves_vivas']} clave(s) viva(s) · "
          f"{len(m['vinculos_claves_por_alias'])} por alias · "
          f"{len(m['vinculos_destinos_sin_elenco'])} de {m['vinculos_destinos_escritos']} "
          f"destinos sin equivalente · {len(m['vinculos_derivados'])} derivados")
    print(f"  aristas de vecinos(): intra-nodo {m['aristas_intra_nodo']} · "
          f"entre nodos {m['aristas_entre_nodos']} · "
          f"a agentes inexistentes {m['aristas_a_inexistentes']}")
    print(f"  sin ninguna arista: {m['agentes_sin_aristas'] or '(nadie)'}")
    print(f"  con sitio de origen declarado: {len(m['con_sitio_de_origen'])} · "
          f"de otro nodo {len(m['cruzan_de_nodo'])} "
          f"({len(m['cruzan_de_nodo_en_roster'])} en el roster)")
