"""
CURIANA — El cargador de mundo de la era 2: [Tu tierra].

Lee el canon de sitios y de clima de la campaña del 2026-09-14
(6-fusion/sitios_era2.yaml y 6-fusion/clima_era2.yaml) y arma, para un agente
en un sitio, un período y un momento del día, un bloque de prosa corta con
tope duro: lo que hay donde está, en qué momento del año, y qué se hace hoy
aquí. Decisiones de Miguel del 2026-09-15/16 (decisiones_tanda_2026-09-15.yaml):

  p1  tres períodos: viento / seca larga / siembra (50/40/30)
  p2  sin nombre caquetío del período — que lo acuñen
  p5  Caseto: conuco principal, pesca de visita
  p7  presupuesto ≤ 320 caracteres, truncado por línea entera, con test
  p4/p8  los hechos y la laguna entran con fuente antes del primer run

Y del 2026-09-17 (golfete-en-paraguana-2026-09-17.md §4a, opción A2):

  {tu agua}  la frase de la tarde del viento nombraba el Golfete para los
             siete sitios; ahora cada quien oye la orilla de SU zona de pesca
             y el Director, que no está en ningún sitio, oye «el agua»

Lo que NO hace, a propósito:
  - no muestra voces hipotéticas (el perfil era2 las esconde: se pasa `capas`);
  - no inyecta testimonios sin procedencia ni datos etiquetados hipotéticos;
  - sí inyecta los huecos léxicos, pero como COSA sin palabra: es el cebo de
    la acuñación;
  - no toca capas_de_score.

Los YAML se leen una vez por proceso. La campaña sugería un módulo generado
(como curiana_agents_era2.py); se lee el YAML directamente porque son dos
ficheros y un test vigila que parseen y que las 126 combinaciones quepan.
"""

from __future__ import annotations

import hashlib
import os
import re
from functools import lru_cache
from typing import Optional

try:
    import yaml
except ImportError:                                   # pragma: no cover
    yaml = None

_AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_SITIOS = os.path.join(_AQUI, "..", "6-fusion", "sitios_era2.yaml")
RUTA_CLIMA = os.path.join(_AQUI, "..", "6-fusion", "clima_era2.yaml")
RUTA_CORPUS_ECOLOGIA = os.path.join(_AQUI, "..", "3-mundo", "corpus", "ecologia.yaml")

PRESUPUESTO = 320
# El bloque del Director es más corto que el del agente: dos frases y una línea.
PRESUPUESTO_DIRECTOR = 400
MOMENTOS = ("amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche")

# ── {tu agua}: cada quien oye su propia orilla (2026-09-17) ────────────
# La frase de la tarde del Tiempo de Viento decía «el Golfete» y entraba igual
# en los siete sitios, incluidos los dos de AMUAY, cuya agua es el Golfo de
# Venezuela (run 3973d317: los 12 agentes del turno de la tarde oyeron que su
# agua era el Golfete, y ninguno de los que la tienen habló en ese turno).
# Decisión de Miguel del 2026-09-17, opción A2 «por zona»
# (6-fusion/issues-pendientes/golfete-en-paraguana-2026-09-17.md §4a): la frase
# lleva el marcador `{tu agua}` y se resuelve con la zona de pesca del SITIO.
#
# La palabra NO se filtra (§4c): el Golfete es canon y es la orilla de GUARANAO.
# Lo que se arregla es el destinatario, no el vocabulario.
#
# La tabla se declara aquí y se lee del YAML (clima_era2.yaml
# `aguas_del_cargador`), que es donde vive la redacción de las frases; esto es
# el respaldo si el canon no la trae. No se usan los nombres largos de las
# zonas (estructura_social_era2.yaml §zonas): son el caladero —«la orilla del
# Golfete de Coro, de Matacán a Tacuato y el Bajo de Supí»— y no caben en una
# frase de momento.
MARCA_TU_AGUA = "{tu agua}"
# Quien no tiene zona (Moruy, el Capubana: la casa del Manaure no tiene playa)
# y el Director, que no está en ningún sitio, oyen la forma neutra. ZG1 —la
# laguna de Guaranao, de fondo— tampoco tiene nombre propio: la laguna nace en
# 1985 (Aular Leal 2014, decisión p8) y su orilla precontacto es la ensenada.
AGUA_NEUTRA = "el agua"
AGUA_POR_ZONA = {
    "ZG2": "el Golfete",
    "ZA1": "la costa del oeste",
}

# Lo que el Director no puede inventar en Paraguaná (2026-09-16: en el día 2 de
# la era 2 narró «la sombra del ceibo»). Escrito a mano y citado entrada por
# entrada: al construir la línea se comprueba que cada id exista en el corpus
# —una restricción sin sus entradas no se dice— y test_director vigila que las
# palabras clave estén en el contenido citado.
#   ecologia-032  cedro, caoba y ceiba NO son árboles del cardonal; el monte
#                 espinoso da cují, yabo, dividivi y cardón
#   ecologia-018  la flora xerófila del matorral: cardón, dividivi, cují…
#   ecologia-007  cauces efímeros; no hay un gran río perenne
#   ecologia-026  el Golfete de Coro: laguna somera, corrientes que arrecian
#                 por la tarde. Es UNA de las dos aguas, y la medición del
#                 viento de la tarde es SUYA, no de la otra orilla
#   ecologia-080  la costa oeste, con las dos atalayas de cardúmenes de Punta
#                 Cardón, a menos de 10 km de Carirubana
#
# La tercera restricción se añade el 2026-09-17: el Director cerró el día 1 de
# la serie B (run 3973d317) con «las canoas volverán al Golfete» para toda la
# gente del día, y 2 de 72 respuestas dijeron «Golfete» —una de ellas la de un
# agente de AMUAY, cuya agua es el Golfo de Venezuela—. El Golfete es canon de
# Paraguaná y es la orilla de GUARANAO (sitios_era2.yaml: Tacuato y El Cayude
# son «la orilla del Golfete», zona ZG2), pero NO es la de AMUAY (ZA1, «la
# costa oeste, de Punta Cardón a Los Taques»). Lo que faltaba no era prohibir
# la palabra —es canon— sino que el Director supiera que hay OTRA agua.
#
# ⚠ La línea no dice «Golfete» a propósito: la restricción entra en los 18
# bloques y nombrarla ahí multiplicaría por nueve la exposición del Director a
# la palabra que sobra. Qué agua es de qué nodo lo dice el canon de la era 2 y
# decirlo aquí es redacción que decide Miguel
# (6-fusion/issues-pendientes/golfete-en-paraguana-2026-09-17.md).
RESTRICCIONES_DEL_DIRECTOR = (
    ("El monte es cardonal: cují, yabo, dividivi, cardón",
     ("ecologia-018", "ecologia-032"), ("cují", "yabo", "dividivi", "cardón")),
    ("no hay ríos ni ceibas",
     ("ecologia-007", "ecologia-032"), ("río", "ceiba")),
    ("son dos aguas y no una: la orilla del este, con su marea, y la costa oeste de Punta Cardón",
     ("ecologia-026", "ecologia-080"), ("marea", "costa oeste", "punta cardón")),
)

# El campo `estacion` del canon, traducido a los períodos del estado.
_ESTACION_A_PERIODOS = {
    "todo el año": {"viento", "seca_larga", "siembra"},
    "seca":        {"viento", "seca_larga"},
    "seca larga":  {"seca_larga"},
    "lluvias":     {"siembra"},
}

# Lo que no llega al agente.
_ETIQUETAS_FUERA = {"hipotetico", "testimonio-miguel"}
_CAPAS_SIN_VOZ_POR_DEFECTO = {"caquetío-hipotético"}

# El dominio prioritario por sitio cuando no hay nada abierto (criterio c del
# diseño): la zona manda, salvo Caseto (p5) y Moruy (sin playa), que son de tierra.
_DOMINIO_DE_TIERRA = {"Caseto", "Moruy", "Capubana"}


@lru_cache(maxsize=None)
def _cargar(ruta: str) -> dict:
    if yaml is None:
        return {}
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def sitios() -> dict:
    """{nombre del sitio: bloque del canon}."""
    d = _cargar(RUTA_SITIOS)
    return {s.get("sitio"): s for s in (d.get("sitios") or []) if s.get("sitio")}


def clima() -> dict:
    return _cargar(RUTA_CLIMA)


def periodos() -> dict:
    """{id del período del estado: bloque del canon} — P1 → viento, etc."""
    ids = {"P1": "viento", "P2": "seca_larga", "P3": "siembra"}
    return {ids[p["id"]]: p for p in (clima().get("periodos") or []) if p.get("id") in ids}


# ── El agua de cada quien ──────────────────────────────────────────────

def aguas_por_zona() -> dict:
    """{id de zona: el nombre del agua} + la neutra bajo la clave "".

    Del canon (clima_era2.yaml `aguas_del_cargador`) si está; si no, la tabla
    declarada arriba. El canon manda, pero nunca deja al marcador sin resolver.
    """
    d = clima().get("aguas_del_cargador") or {}
    tabla = dict(AGUA_POR_ZONA)
    tabla.update({str(k): str(v) for k, v in (d.get("por_zona") or {}).items() if v})
    tabla[""] = str(d.get("neutra") or AGUA_NEUTRA)
    return tabla


def agua_del_sitio(sitio: str) -> str:
    """Cómo se llama el agua del que está en `sitio`.

    La zona la da `sitios()[sitio]['zona_de_pesca']` (sitios_era2.yaml la
    escribe pelada: ZG2, ZA1, ZG1 o null; el elenco la escribe con glosa entre
    paréntesis, así que se toma el primer token). Sin zona, o con una zona sin
    nombre declarado, la forma neutra.
    """
    tabla = aguas_por_zona()
    zona = str((sitios().get(sitio) or {}).get("zona_de_pesca") or "").split("(")[0].split()
    return tabla.get(zona[0], tabla[""]) if zona else tabla[""]


def _con_agua(linea: str, agua: str) -> str:
    """Resuelve `{tu agua}` antes de medir el largo: el presupuesto se cobra
    sobre lo que el agente lee, no sobre la plantilla."""
    return linea.replace(MARCA_TU_AGUA, agua) if MARCA_TU_AGUA in linea else linea


# ── Filtros ────────────────────────────────────────────────────────────

def _estacion_y_momento(linea: dict) -> tuple[set, Optional[str]]:
    """'seca — anochecer' → ({viento, seca_larga}, 'anochecer')."""
    txt = str(linea.get("estacion") or "todo el año")
    base, _, mom = txt.partition("—")
    base = base.strip()
    mom = mom.strip() or None
    if mom and " y " in mom:                       # 'anochecer y noche'
        mom = mom.split(" y ")[0].strip()
    return _ESTACION_A_PERIODOS.get(base, _ESTACION_A_PERIODOS["todo el año"]), mom


def _entra(linea: dict, periodo: str, momento: str) -> bool:
    if linea.get("etiqueta") in _ETIQUETAS_FUERA:
        return False
    # Una línea atestiguada del sitio de HOY que no vale para el s. XV (la
    # laguna de Guaranao y su manglar son de 1985: Aular Leal 2014) se declara
    # `proyectable: false` en el canon y no llega al agente.
    if linea.get("proyectable") is False:
        return False
    if linea.get("deuda") == "sin-procedencia" and linea.get("etiqueta") == "testimonio-miguel":
        return False
    per, mom = _estacion_y_momento(linea)
    if periodo not in per:
        return False
    if mom and mom != momento:
        return False
    return True


def _voz_visible(linea: dict, capas: Optional[frozenset]) -> Optional[str]:
    voz = linea.get("voz_caquetia") or {}
    clave, capa = voz.get("clave"), voz.get("capa")
    if not clave:
        return None
    if capas is not None:
        return clave if capa in capas else None
    return None if capa in _CAPAS_SIN_VOZ_POR_DEFECTO else clave


# ── Render ─────────────────────────────────────────────────────────────

_CIERRE = re.compile(r"[.;]\s")
_CITA = re.compile(r"«([^»]{25,})»")
_ARRANQUE = re.compile(r"^(⭐\s*|Y\s+(al lado\s+|la\s+)?|Lo que hay en el agua:\s*|ABRE[^—]*—\s*|NO CIERRA NUNCA[^—]*—\s*|CIERRA[^—]*—\s*)", re.I)


def _rematar(t: str) -> str:
    """Mayúscula inicial y un cierre: la línea es prosa, no una nota."""
    t = t.strip()
    if not t:
        return t
    t = t[0].upper() + t[1:]
    return t if t.endswith(("…", ".", "!", "?")) else t.rstrip(",;:") + "."


def _primera_frase(texto: str, tope: int = 110) -> str:
    """Lo que se le dice al agente de una línea del canon.

    Primero la cita literal de la fuente, si la hay y cabe («Ningún río, ni
    siquiera un arroyo, riega a Paraguaná»): son las palabras del que lo vio.
    Si no, la primera frase del `dato` sin sus marcas de escriba (⭐, «Y al
    lado…», «ABRE en P1 —»), cortada en punto o punto y coma —nunca en dos
    puntos, que suelen abrir lo que importa— y, si aún no cabe, en el último
    espacio antes del tope, con «…»."""
    crudo = " ".join(str(texto).split())
    m = _CITA.search(crudo)
    if m and len(m.group(1)) <= tope:
        return _rematar(m.group(1).rstrip(".;:, "))
    t = crudo.replace("«", "").replace("»", "")
    t = _ARRANQUE.sub("", t).strip()
    m = _CIERRE.search(t)
    if m and m.end() - 1 <= tope:
        t = t[: m.start()]
    if len(t) > tope:
        corte = t.rfind(" ", 0, tope - 1)
        t = (t[:corte] if corte > 40 else t[: tope - 1]).rstrip(",;:") + "…"
    return _rematar(t)


def _frase_de(linea: dict, capas: Optional[frozenset]) -> str:
    if linea.get("hueco_lexico"):
        # La cosa sin palabra, dicha como cosa: es el cebo de la acuñación.
        concepto = str(linea.get("concepto") or "").split("—")[0].split("(")[0].strip()
        concepto = concepto.replace(" / ", ", ").rstrip(".,;: ")
        if concepto:
            return _rematar(f"sin nombre todavía: {concepto}")
    frase = _rematar(linea["frase"]) if linea.get("frase") else _primera_frase(linea.get("dato") or "")
    voz = _voz_visible(linea, capas)
    if voz and len(voz) > 2 and voz.lower() not in frase.lower():
        frase = f"{frase} Lo decís {voz}."
    return frase


def _indice(agente: str, dia: int, n: int) -> int:
    """Rotación determinista: el mismo agente no ve la misma línea todos los
    días, y el run se repite igual con la misma semilla porque no usa el RNG."""
    if n <= 1:
        return 0
    h = hashlib.sha1(f"{agente}|{dia}".encode("utf-8")).hexdigest()
    return int(h[:8], 16) % n


def _candidatas(sitio: dict, periodo: str, momento: str) -> list:
    """Las líneas del sitio que valen hoy, en orden de prioridad:
    (a) lo que abre_y_cierra abre en este período; (b) el agua; (c) el
    dominio de la zona (o la tierra); (d) el resto."""
    nombre = sitio.get("sitio")
    abre = [l for l in (clima().get("abre_y_cierra") or {}).get(nombre) or []
            if _entra(l, periodo, momento) and not str(l.get("dato", "")).startswith("CIERRA")]
    dom = sitio.get("dominios") or {}
    agua = [l for l in dom.get("agua") or [] if _entra(l, periodo, momento)]
    if nombre in _DOMINIO_DE_TIERRA or not sitio.get("zona_de_pesca"):
        principal = "tierra"
    else:
        principal = "mar_y_pesca"
    zona = [l for l in dom.get(principal) or [] if _entra(l, periodo, momento)]
    resto = [l for k, v in dom.items() if k not in ("agua", principal)
             for l in v or [] if _entra(l, periodo, momento)]
    return [abre, agua, zona, resto]


def bloque_tu_tierra(sitio: str, periodo: str, momento: str, *, agente: str = "",
                     dia: int = 1, capas: Optional[frozenset] = None,
                     presupuesto: int = PRESUPUESTO) -> str:
    """El bloque [Tu tierra] para `sitio` en `periodo` y `momento`, ≤ presupuesto.

    Líneas, en orden: el sitio en una frase; el período; el momento; una
    línea del sitio (rotando por agente y día); si cabe, otra. Se trunca por
    línea entera. Devuelve "" si el sitio no está en el canon o el período no
    es de la era 2.

    `{tu agua}` se resuelve con la zona de pesca de ESTE sitio (decisión A2 del
    2026-09-17): el de Tacuato oye «el Golfete», el de Carirubana «la costa del
    oeste» y el que no tiene playa, «el agua».
    """
    s = sitios().get(sitio)
    frases = (clima().get("frases_del_cargador") or {}).get(periodo)
    if not s or not frases:
        return ""
    cabeza = "[Tu tierra] "
    lineas = []
    una = str(s.get("en_una_frase") or "").strip()
    if len(una) > 90:
        # Se corta en la última coma antes del tope; si no la hay, en los dos
        # puntos; y si tampoco, en el último espacio, con «…».
        corte = una.rfind(",", 0, 90)
        if corte < 30:
            corte = una.find(":") if 30 < una.find(":") < 90 else -1
        una = una[:corte] if corte > 0 else una[:88].rsplit(" ", 1)[0] + "…"
    lineas.append(_rematar(f"{sitio}, {una}") if una else f"{sitio}.")
    lineas.append(str(frases.get("periodo") or "").strip())
    mom = (frases.get("momentos") or {}).get(momento)
    if mom:
        lineas.append(str(mom).strip())

    # Las líneas del sitio: una por prioridad, rotando.
    for grupo in _candidatas(s, periodo, momento):
        if not grupo:
            continue
        linea = grupo[_indice(agente, dia, len(grupo))]
        lineas.append(_frase_de(linea, capas))

    # Cada quien oye su propia orilla, y se resuelve ANTES de medir.
    agua = agua_del_sitio(sitio)
    lineas = [_con_agua(l, agua) for l in lineas]

    # Tope duro por línea entera: el sitio, el período y el momento se recortan
    # si hace falta (son el mínimo); una línea del sitio que no cabe se salta y
    # se prueba la siguiente, para que un dato largo no deje al agente sin tierra.
    salida = cabeza
    for i, l in enumerate(lineas):
        candidato = salida + ("" if i == 0 else " ") + l
        if len(candidato) > presupuesto:
            if i < 3:
                l = l[: max(0, presupuesto - len(salida) - 2)].rsplit(" ", 1)[0] + "…"
                candidato = salida + ("" if i == 0 else " ") + l
                if len(candidato) > presupuesto:
                    break
            else:
                continue
        salida = candidato
    return salida if len(salida) > len(cabeza) else ""


def combinaciones() -> list:
    """Las 126 (7 sitios × 3 períodos × 6 momentos), para el test del tope."""
    return [(s, p, m) for s in sitios() for p in ("viento", "seca_larga", "siembra") for m in MOMENTOS]


# ── El mundo para el Director ──────────────────────────────────────────

def hechos_del_corpus(ruta: str = RUTA_CORPUS_ECOLOGIA) -> dict:
    """{id: entrada} de un YAML del corpus. ecologia.yaml es un dict de listas
    (entradas, huecos_lexicos); se aplanan todas las secciones que son lista."""
    try:
        d = _cargar(ruta)
    except OSError:
        return {}
    secciones = d.values() if isinstance(d, dict) else [d]
    return {h["id"]: h for s in secciones if isinstance(s, list)
            for h in s if isinstance(h, dict) and h.get("id")}


def restricciones_del_director() -> str:
    """La línea de restricciones, sólo con las que el corpus sostiene por id."""
    hechos = hechos_del_corpus()
    partes = [frase for frase, ids, _ in RESTRICCIONES_DEL_DIRECTOR
              if all(i in hechos for i in ids)]
    return f"[{'; '.join(partes)}]" if partes else ""


def resumen_del_mundo(state, *, estacion: Optional[str] = None, momento: Optional[str] = None,
                      presupuesto: int = PRESUPUESTO_DIRECTOR) -> str:
    """El mundo para el Director (no para un agente): la frase del período y
    la del momento (clima_era2.yaml, frases_del_cargador) más la línea de
    restricciones del corpus. ≤ presupuesto, truncado por línea entera.
    Devuelve "" si el período no es de la era 2 (la Curiana no tiene canon).

    El Director no está en ningún sitio: `{tu agua}` le llega en la forma
    NEUTRA («el agua»). Decirle «el Golfete» en los 18 bloques es lo que le hizo
    cerrar el día 1 de la serie B con «las canoas volverán al Golfete» para
    toda la gente del día (run 3973d317). Qué agua es de qué nodo se lo dice la
    tercera restricción, que no nombra ninguna."""
    estacion = estacion or getattr(state, "estacion", None)
    momento = momento or getattr(state, "momento", None)
    frases = (clima().get("frases_del_cargador") or {}).get(estacion)
    if not frases:
        return ""
    neutra = aguas_por_zona()[""]
    lineas = [_con_agua(str(frases.get("periodo") or "").strip(), neutra)]
    mom = (frases.get("momentos") or {}).get(momento)
    if mom:
        lineas.append(_con_agua(str(mom).strip(), neutra))
    restricciones = restricciones_del_director()
    if restricciones:
        lineas.append(restricciones)
    cabeza = "[El mundo]"
    salida = cabeza
    for l in lineas:
        if not l:
            continue
        candidato = f"{salida} {l}"
        if len(candidato) > presupuesto:
            continue
        salida = candidato
    return salida if salida != cabeza else ""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for s, p, m in combinaciones():
        b = bloque_tu_tierra(s, p, m, agente="demo", dia=1)
        print(f"{len(b):3}  {b}")
