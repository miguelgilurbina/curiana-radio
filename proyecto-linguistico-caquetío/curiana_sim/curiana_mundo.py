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

PRESUPUESTO = 320
MOMENTOS = ("amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche")

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


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for s, p, m in combinaciones():
        b = bloque_tu_tierra(s, p, m, agente="demo", dia=1)
        print(f"{len(b):3}  {b}")
