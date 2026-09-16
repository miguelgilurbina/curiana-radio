"""
CURIANA — Los eventos del mundo, dichos para el elenco activo.

EVENTOS_COTIDIANOS y EVENTOS_ESTACIONALES (curiana_state.py) se escribieron
para la era 1: nombran a los agentes por su nombre viejo (Biro-ko, Shaboro,
Tina-sha…) y traen el marco étnico de la Curiana —guaycaríes y caquetíos en la
misma orilla, el Jirajara de la sierra, el comerciante serrano—. En la era 2
(el elenco de Paraguaná, curiana_agents_era2.py) 60 de los 63 nombres cambiaron
y los foráneos no están en escena (Miguel, 2026-09-14: «los foráneos no
deberían entrar de momento»). Nadie traducía: run_turn filtra
`agentes_involucrados` con `a in ALL_AGENTS` y nunca llamó a resolver_alias(),
así que un evento de la era 2 sólo traía a Manaure o a Dara-bana, y el Director
narró «Biro-ko» y «los Guaycarí» en Paraguaná (runs c6837386 y 89fc1744,
2026-09-16). Las cifras se miden con `python curiana_eventos.py` (medir()).

Lo que hace evento_para_elenco():
  1. era 1: devuelve el evento tal cual (el mismo objeto).
  2. era 2: si el evento está en EVENTOS_SOLO_CON_FORANEOS, None.
  3. reescribe las frases de REESCRITURAS_ERA2 (tabla declarada, exacta,
     escrita en nombres de la era 1: se aplica ANTES del alias para que se lea);
  4. traduce los nombres por ALIAS_ERA1 respetando guiones y mayúsculas
     («Biro-ko» → «Birokoa»; «Sha» no toca «Sha-korie» ni «Shaboro»);
  5. en `agentes_involucrados` traduce los que tienen alias, conserva los
     pseudo-nombres (toda_la_comunidad, guerreros) y quita a los foráneos y a
     los que no tienen equivalente;
  6. si aún queda un nombre de la era 1 en `descripcion` o `nombre`, None:
     mejor un evento menos que un nombre de otra era en boca del Director.

El catálogo no era la única puerta. El texto LIBRE que se le pasa al Director
—lo que él mismo dejó anotado al cerrar el día anterior (`notas_orquestador`),
los cierres del día y la línea de estado— venía sin traducir: en el día 3 (run
0193873d, con los eventos ya traducidos) el Director escribió «Los Caquetíos y
Guaycarí se juntan…» porque su propia nota del día 2 decía «los Guaycarí culpan
el calor, los Caquetíos el rezo faltante». Para eso está texto_para_elenco():
mismas reescrituras y mismo alias que el catálogo, y las FRASES que aún llevan
un nombre sin traducción o un marco que la era 2 no tiene se caen —frase a
frase, no el texto entero, que una reflexión son seis oraciones y no un evento
de dos—. decir_para_el_mundo() es la puerta que usa el Director.

Decisiones declaradas (2026-09-16):
  - llegada_nabaraka CAE: el evento es el foráneo (jirajara, fuera de escena).
  - trueque_visitantes_plaza SE QUEDA sin el marco étnico: el intercambio es
    actividad del Tiempo de Viento y de la seca larga (PERIODOS_ERA2), y los
    visitantes son escena, no voces.
  - rumor_raid_caribe y vigilancia_perimetro_amanecer SE QUEDAN: el caribe
    llega por mar y no reside (etnia-008). Chiriware, que en la era 2 es un
    linaje y no un guerrero vivo, sale de la frase.
  - canoa_islas_llega y watapana_parte_islas SE QUEDAN sin Kadushi ni
    Watapana (sin equivalente en la era 2): la travesía a las islas es del
    Tiempo de Viento (clima_era2.yaml).
  - crecida_buco SE QUEDA sin Buko-ko (sin equivalente): «los del buko».

El catálogo de la era 1 no se toca: cada evento adaptado es una copia.
"""

from __future__ import annotations

import copy
import re
from functools import lru_cache
from typing import Iterable, Optional

from curiana_state import EVENTOS_COTIDIANOS, EVENTOS_ESTACIONALES

# Nombres que no son agentes y run_turn ya descarta; se conservan tal cual.
PSEUDO_AGENTES = frozenset({"toda_la_comunidad", "guerreros"})

# Eventos que sólo tienen sentido con foráneos en escena: en la era 2 no caen.
EVENTOS_SOLO_CON_FORANEOS = {
    "llegada_nabaraka": "el evento ES Nabaraka el Jirajara (foráneo, fuera de escena "
                        "desde 2026-09-14); sin él no queda nada que contar",
}

# Frases de la era 1 que no valen en la era 2. Se reescribe exactamente esto y
# nada más; están en nombres de la era 1 porque se aplican antes del alias.
REESCRITURAS_ERA2 = {
    # pesca_mala — dos etnias en la misma orilla es el marco de la Curiana
    "Los Guaycarí culpan al calor; los Caquetíos al mal ritual.":
        "Unos culpan al calor; otros, al mal ritual.",
    # trueque_visitantes_plaza — el Jirajara de la sierra no está en escena; el trueque sí
    "el Jirajara muestra ocre y carne seca de la sierra, el caquetío ofrece biro y cerámica":
        "los de fuera muestran ocre y carne seca; los de aquí ofrecen biro y cerámica",
    # canoa_islas_llega — Kadushi no tiene equivalente en la era 2; la canoa de Aruba sí
    "La canoa de Kadushi llega desde Aruba": "Una canoa llega desde Aruba",
    # vigilancia_perimetro_amanecer / rumor_raid_caribe — Chiriware es linaje, no guerrero vivo
    "Chiriware reparte los puestos de guardia": "se reparten los puestos de guardia",
    "Chiriware activa el perímetro.": "Se activa el perímetro.",
    # crecida_buco — Buko-ko no tiene equivalente
    "Korie-ko y Buko-ko caminan las represas": "Korie-ko y los del buko caminan las represas",
    # watapana_parte_islas — sólo el nombre del evento lo nombra
    "Watapana parte a las islas": "Una expedición parte a las islas",
}

# Los marcos de la era 1 que no valen en texto libre: los etnónimos de los
# pueblos que la era 2 no tiene en la orilla y el nombre del mundo de la era 1
# usado como lugar. El CARIBE no está en la lista a propósito: llega por mar y
# no reside (etnia-008), y sus eventos se quedan (decisión 2026-09-16). Los
# guaycaríes, jirajaras y gayones son los foráneos que la era 2 dejó fuera
# (decisión 2026-09-14) y en Paraguaná no hay dos pueblos en la misma orilla.
MARCOS_FUERA_ERA2 = (
    re.compile(r"[Gg]uaycar[íi](?:es)?\b"),
    re.compile(r"[Jj]irajaras?\b"),
    re.compile(r"[Gg]ay(?:ón|ones)\b"),
    re.compile(r"\bCuriana\b"),
)

# Fin de frase y fin de línea: el texto libre se filtra frase a frase dentro de
# cada línea, para no romper un bloque con estructura (la línea de estado) ni
# tirar seis oraciones por una.
_FIN_DE_FRASE = re.compile(r"(?<=[.!?…])\s+")


# ── Nombres en texto ───────────────────────────────────────────────────

@lru_cache(maxsize=None)
def _patron_cacheado(nombres: tuple) -> Optional[re.Pattern]:
    if not nombres:
        return None
    # Ni letra ni guion a los lados: «Sha» no casa en «Sha-korie» ni en «Shaboro»,
    # y «Kori» no casa en «Korie-ko». Los largos van primero.
    return re.compile(r"(?<![\w-])(?:" + "|".join(map(re.escape, nombres)) + r")(?![\w-])")


def _patron(nombres: Iterable[str]) -> Optional[re.Pattern]:
    return _patron_cacheado(tuple(sorted(set(nombres), key=lambda n: (-len(n), n))))


def sustituir_nombres(texto: str, alias: dict) -> str:
    """Cambia cada nombre de `alias` por su valor, entero y con su caso."""
    cambian = {k: v for k, v in alias.items() if k != v}
    p = _patron(cambian)
    return p.sub(lambda m: cambian[m.group(0)], texto) if p else texto


def nombres_de_la_era_1(texto: str, nombres: Iterable[str]) -> list[str]:
    """Los nombres de `nombres` que aparecen enteros en `texto`."""
    p = _patron(nombres)
    return p.findall(texto) if p else []


# ── El evento para el elenco ───────────────────────────────────────────

def evento_para_elenco(evento: dict, elenco: str, alias: dict, foraneos,
                       *, sin_equivalente=frozenset()) -> Optional[dict]:
    """El evento dicho para `elenco`.

    era 1 → el mismo objeto. era 2 → una copia con `nombre`, `descripcion` y
    `agentes_involucrados` traducidos por `alias` (nombre viejo → nuevo), sin
    `foraneos` ni nombres sin equivalente; o None si el evento sólo tiene
    sentido con foráneos o si un nombre de la era 1 no se pudo traducir.
    `sin_equivalente` son los nombres de la era 1 que la era 2 dejó fuera sin
    ser foráneos (Kadushi, Watapana, Chiriware, Buko-ko…): sirven para
    detectar el residuo.
    """
    if elenco != "era2":
        return evento
    if evento.get("id") in EVENTOS_SOLO_CON_FORANEOS:
        return None
    e = copy.deepcopy(evento)
    for campo in ("nombre", "descripcion"):
        t = str(e.get(campo) or "")
        for viejo, nuevo in REESCRITURAS_ERA2.items():
            t = t.replace(viejo, nuevo)
        e[campo] = sustituir_nombres(t, alias)
    foraneos = set(foraneos or ())
    e["agentes_involucrados"] = [
        alias.get(a, a) for a in evento.get("agentes_involucrados", [])
        if (a in alias or a in PSEUDO_AGENTES) and a not in foraneos
    ]
    viejos = {k for k, v in alias.items() if k != v} | foraneos | set(sin_equivalente)
    for campo in ("nombre", "descripcion"):
        if nombres_de_la_era_1(e[campo], viejos):
            return None
    return e


def catalogo_para_elenco(elenco: str, alias: dict, foraneos,
                         sin_equivalente=frozenset()) -> tuple[list, list]:
    """(cotidianos, estacionales) para `elenco`: la era 1 tal cual; la era 2
    adaptada, sin los eventos que caen."""
    if elenco != "era2":
        return list(EVENTOS_COTIDIANOS), list(EVENTOS_ESTACIONALES)

    def _adaptar(eventos):
        salida = []
        for ev in eventos:
            a = evento_para_elenco(ev, elenco, alias, foraneos, sin_equivalente=sin_equivalente)
            if a is not None:
                salida.append(a)
        return salida

    return _adaptar(EVENTOS_COTIDIANOS), _adaptar(EVENTOS_ESTACIONALES)


# ── El texto libre para el elenco ──────────────────────────────────────

def residuos_de_la_era_1(texto: str, viejos: Iterable[str]) -> list[str]:
    """Lo que la era 2 no tiene y quedó en `texto`: nombres de la era 1 sin
    traducción (`viejos`) y marcos étnicos o de lugar de la Curiana."""
    t = texto or ""
    return (nombres_de_la_era_1(t, viejos)
            + [m.group(0) for p in MARCOS_FUERA_ERA2 for m in p.finditer(t)])


def texto_para_elenco(texto: str, alias: dict, viejos: Iterable[str]) -> str:
    """Texto libre (las notas del Director, un cierre, la línea de estado)
    dicho para el elenco de la era 2.

    Reescribe las frases de REESCRITURAS_ERA2, traduce los nombres por `alias`
    y quita, frase a frase y línea a línea, las que aún llevan un nombre sin
    traducción o un marco que la era 2 no tiene. Devuelve "" si no sobrevive
    nada: el Director prefiere no leer a leer de otro mundo."""
    t = texto or ""
    for viejo, nuevo in REESCRITURAS_ERA2.items():
        t = t.replace(viejo, nuevo)
    t = sustituir_nombres(t, alias)
    viejos = set(viejos)
    lineas = []
    for linea in t.split("\n"):
        vivas = [f for f in _FIN_DE_FRASE.split(linea)
                 if f.strip() and not residuos_de_la_era_1(f, viejos)]
        if vivas:
            lineas.append(" ".join(f.strip() for f in vivas))
    return "\n".join(lineas).strip()


@lru_cache(maxsize=None)
def _alias_y_viejos(elenco: str) -> tuple:
    """(alias, nombres de la era 1 que la era 2 no puede decir) para `elenco`.
    Los «viejos» son los que cambiaron de nombre más los que se quedaron fuera
    (foráneos incluidos: un nombre fuera del elenco no tiene alias)."""
    alias = alias_del_elenco(elenco)
    if not alias:
        return {}, frozenset()
    era1 = set(elenco_era1())
    viejos = {k for k, v in alias.items() if k != v} | (era1 - set(alias))
    return alias, frozenset(viejos)


def decir_para_el_mundo(texto: str, mundo: Optional[str]) -> str:
    """La puerta del Director: el texto libre que se le pasa, dicho para el
    mundo del estado. CURIANA devuelve el texto tal cual —la era 1 no cambia
    ni un byte—; PARAGUANÁ pasa por texto_para_elenco()."""
    if (mundo or "").upper() != "PARAGUANÁ":
        return texto or ""
    alias, viejos = _alias_y_viejos("era2")
    return texto_para_elenco(texto, alias, viejos)


# ── Lo que el elenco activo aporta ─────────────────────────────────────

def alias_del_elenco(elenco: str) -> dict:
    """ALIAS_ERA1 (nombre de la era 1 → de la era 2) si el elenco es la era 2;
    vacío en la era 1. Se importa aquí para no cargar el módulo generado sin
    necesidad."""
    if elenco != "era2":
        return {}
    from curiana_agents_era2 import ALIAS_ERA1
    return dict(ALIAS_ERA1)


def elenco_era1() -> dict:
    """Los agentes de la era 1 con su ficha, sea cual sea el elenco activo:
    curiana_agents.py sólo reemplaza ALL_AGENTS, los tiers quedan."""
    from curiana_agents import AGENTS_T1, AGENTS_T2, AGENTS_T3
    return {**AGENTS_T1, **AGENTS_T2, **AGENTS_T3}


# ── Medición ───────────────────────────────────────────────────────────

def medir(alias: dict, foraneos, sin_equivalente=frozenset()) -> dict:
    """Cuánto nombra el catálogo a la era 1: es la cifra del commit que abre
    este módulo y se vuelve a medir aquí, no a mano."""
    eventos = EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES
    foraneos = set(foraneos or ())
    viejos = {k for k, v in alias.items() if k != v} | foraneos | set(sin_equivalente)
    m = {"eventos": len(eventos), "involucrados": 0, "con_alias": 0, "foraneos": 0,
         "sin_equivalente": 0, "pseudo": 0, "menciones_en_texto": 0,
         "eventos_con_mencion_en_texto": 0, "marco_etnico": []}
    etnico = re.compile(r"Guaycar|Caquetíos|Jirajara|serrano")
    for e in eventos:
        inv = e.get("agentes_involucrados", [])
        m["involucrados"] += len(inv)
        m["con_alias"] += sum(1 for a in inv if a in alias)
        m["foraneos"] += sum(1 for a in inv if a in foraneos)
        m["sin_equivalente"] += sum(1 for a in inv if a in sin_equivalente)
        m["pseudo"] += sum(1 for a in inv if a in PSEUDO_AGENTES)
        n = len(nombres_de_la_era_1(e["descripcion"], viejos | set(alias))) \
            + len(nombres_de_la_era_1(e["nombre"], viejos | set(alias)))
        m["menciones_en_texto"] += n
        m["eventos_con_mencion_en_texto"] += bool(n)
        if etnico.search(e["descripcion"] + " " + e["nombre"]):
            m["marco_etnico"].append(e["id"])
    return m


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    alias = alias_del_elenco("era2")
    era1 = elenco_era1()
    foraneas = {"caribe", "gayón", "guaycarí", "jirajara"}       # = orquestador.ETNIAS_FORANEAS
    foraneos = {n for n, a in era1.items() if (a.get("etnia") or "caquetío").lower() in foraneas}
    sin_eq = set(era1) - set(alias) - foraneos
    m = medir(alias, foraneos, sin_eq)
    print("El catálogo de la era 1, medido:")
    for k, v in m.items():
        print(f"  {k}: {v}")
    print(f"  foráneos de la era 1: {sorted(foraneos)}")
    print(f"  sin equivalente en la era 2: {sorted(sin_eq)}")
    print("\nEl catálogo dicho para la era 2:")
    cot, est = catalogo_para_elenco("era2", alias, foraneos, sin_eq)
    vivos = {e["id"] for e in cot + est}
    for e in EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES:
        if e["id"] in vivos:
            a = next(x for x in cot + est if x["id"] == e["id"])
            print(f"  ✓ {e['id']:32} {a['agentes_involucrados']}")
        else:
            print(f"  ✗ {e['id']:32} cae: {EVENTOS_SOLO_CON_FORANEOS.get(e['id'], 'nombre sin traducción')}")

    print("\nEl texto libre del Director, dicho para la era 2:")
    muestra = (
        "El alisio no aflojó y los peces tampoco vinieron. Lo que cambió fue el miedo, "
        "y eso dividió las explicaciones: los Guaycarí culpan el calor, los Caquetíos "
        "el rezo faltante. La palabra que prendió fue tüshi-juri, viento frío del este. "
        "Biro-ko subió la sal al cerro antes de que cayera la noche."
    )
    for etiqueta, mundo in (("CURIANA", "CURIANA"), ("PARAGUANÁ", "PARAGUANÁ")):
        salida = decir_para_el_mundo(muestra, mundo)
        print(f"  [{etiqueta}] {len(salida)} caracteres de {len(muestra)}")
        print(f"      {salida}")
    _, viejos = _alias_y_viejos("era2")
    print(f"  residuos que detecta en el original: {residuos_de_la_era_1(muestra, viejos)}")
