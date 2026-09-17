#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deriva del elenco de la era 2 la tabla «oficio × momento del día → lugar», y
mide qué sale de ella: cobertura, ocupación de cada lugar por momento, qué
lugares comparten los dos nodos y quiénes cruzaron por matrimonio.

    6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md
    6-fusion/escena_por_lugar_propuesta_2026-09-17.yaml   (--yaml lo reescribe)

Regla 1: ninguna cifra de ese borrador está escrita a mano. Las imprime este
script. No llama a ninguna API, no lee `curiana_sim/.env` y no toca Supabase.

QUÉ ES LA TABLA. Hoy la ubicación de un agente es su `ubicacion_default` y no
se mueve nunca: nadie escribe `state.ubicaciones_override` (medido abajo con
--motor). La tabla dice, para cada CLASE DE OFICIO —derivada de la ficha por
palabras clave, no escrita agente a agente— dónde está esa gente en cada uno
de los seis momentos del día. El lugar se escribe como PLANTILLA
(`{sitio}:orilla`, `{zona}`, `Capubana`) y se resuelve con la ficha de cada
agente, así que el nodo de un lugar no se programa: sale del mapa.

    python 6-fusion/scripts/derivar_escena_por_lugar.py
    python 6-fusion/scripts/derivar_escena_por_lugar.py --yaml
    python 6-fusion/scripts/derivar_escena_por_lugar.py --motor   # + el motor de hoy
"""

import argparse
import collections
import math
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:                                     # pragma: no cover
    yaml = None

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RAIZ = os.path.normpath(os.path.join(_AQUI, "..", ".."))
_FUSION = os.path.join(_RAIZ, "6-fusion")
_SIM = os.path.join(_RAIZ, "curiana_sim")

RUTA_ELENCO = os.path.join(_FUSION, "elenco_era2.yaml")
RUTA_SITIOS = os.path.join(_FUSION, "sitios_era2.yaml")
RUTA_CLIMA = os.path.join(_FUSION, "clima_era2.yaml")
RUTA_ESTRUCTURA = os.path.join(_FUSION, "estructura_social_era2.yaml")
RUTA_SALIDA = os.path.join(_FUSION, "escena_por_lugar_propuesta_2026-09-17.yaml")

MOMENTOS = ["amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche"]
PERIODOS = ["viento", "seca_larga", "siembra"]


def _forzar_utf8():
    """La consola de Windows es cp1252 (CLAUDE.md, trampas)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                   # pragma: no cover
        pass


def norm(t) -> str:
    """Minúsculas y sin acentos: las reglas de clasificación se leen mejor."""
    t = str(t or "").lower()
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn")


# ══════════════════════════════════════════════════════════════════════
# 1. LAS CLASES DE OFICIO — derivadas de la ficha, en este orden
# ══════════════════════════════════════════════════════════════════════
# Cada clase es (id, regex sobre `oficio` normalizado, glosa). La PRIMERA que
# casa gana: por eso el orden es parte de la propuesta y no un detalle. Antes
# de las regex corre una regla sobre `rol_en_la_casa` (los niños y la
# encerrada), porque su día lo manda la casa y no lo que ya saben hacer.

PRE_ROL = [
    (r"\bnin[oa]\b|\(nin[oa]\)|en encierro|encerrada", "ninez"),
]

CLASES = [
    ("mensajeria", r"recado|aviso|llamamiento|corre los avisos",
     "el que lleva la palabra de una casa a otra"),
    ("mando", r"gobernar|redistribu|presidir|acompana al manaure",
     "el Manaure, la que reparte y el sobrino que aprende estando cerca"),
    ("oraculo", r"oraculo|lee suenos|urari|buhio del cerro|\bayuna\b",
     "el boratio mayor y su ayunante: el cerro y el encierro"),
    ("curacion", r"boratia|cura por pasos|parturienta|adivina para",
     "la boratia de pueblo: cura, adivina, recibe"),
    ("huesos", r"huesos del diao|fuego sin llama|hamaca del diao|muelen los huesos",
     "las que muelen los huesos y el que sostiene el fuego"),
    ("cantor", r"cantor|recita a los ancestros|canta de noche lo que hizo",
     "el cantor de hazañas (of-08)"),
    ("arbitraje", r"buena vara|linderos",
     "el de la buena vara: linderos de conuco y de playa (of-13)"),
    ("merejuy", r"merejuy|chicha|fermento",
     "la maestra del merejuy (of-07)"),
    ("sal", r"\bel biro\b|cosecha la sal|sal de las charcas",
     "el biro: raspar la sal de las charcas"),
    ("agua_dulce", r"jaguey|charca|fuente intermitente|lee la tierra y el agua|cuando se abre el agua",
     "los que guardan el agua: el jagüey y la fuente del cerro (of-06)"),
    ("vigia", r"\bvigia\b|vigiar|cardumen|sube a la punta",
     "el que sube a la punta y ve primero"),
    ("marisqueo", r"junta la concha|concha y el caracol|junta el botuto|botuto|marea baja",
     "la concha y el caracol de la orilla, a marea baja"),
    ("casa", r"cocina|budare|fogon|ahuma|seca el pescado|sala y seca|casabe|cuida a los ninos|lleva la casa",
     "la casa y el fogón: cocinar, ahumar, criar"),
    ("fibra", r"cordelera|cocuiza|cabuya|\bhila\b|teje|totuma|hamacas de maure",
     "la fibra: cordel, algodón, hamaca, totuma"),
    ("pesca", r"pesca|pescador|nasas|se zambulle|arpon|de red\b",
     "la pesca: de orilla, de red, nocturna y de mar grueso"),
    ("canoa", r"canoa|calafate|resina|brea|corrientes de la costa",
     "el taller de canoas y la brea"),
    ("conuco", r"conuco|siembra|semilla|cultivos|roza y fuego|desmontado",
     "el conuco: sembrar, cosechar, abrir tierra"),
    ("monte", r"matorral|recolectora|herbolaria|recoge el fruto|lo del monte|del monte\b",
     "el matorral: la planta que cura y lo que el conuco no da"),
    ("alfareria", r"alfarer|vasija|barro|modela",
     "el barro: la vasija que es memoria"),
    ("vision", r"vidente|frases que se cumplen",
     "la que dice lo que se cumple dos días después"),
    ("memoria_de_casa", r"matriarca|guarda la memoria|autoriza los matrimonios|cuentas|guarda lo de la casa|guarda los disenos",
     "la matriarca: la cuenta del don y lo que se guarda"),
]

# La ficha de un agente puede declarar ella misma que su oficio cambia con el
# año. Sólo se lee lo que está escrito; no se infiere.
CLASE_POR_PERIODO = [
    (r"conuco en las lluvias", "siembra", "conuco"),
]


def clase_en(agente: dict, periodo: str) -> str:
    """La clase del agente en ese período: la suya, salvo que su ficha declare
    el cambio (Kunaro-bana, «pesca el cunaro en la seca y trabaja el conuco en
    las lluvias»)."""
    texto = norm(agente.get("oficio"))
    for patron, per, clase in CLASE_POR_PERIODO:
        if per == periodo and re.search(patron, texto):
            return clase
    return agente["_clase"]


def clase_de(agente: dict) -> str:
    rol = norm(agente.get("rol_en_la_casa"))
    for patron, clase in PRE_ROL:
        if re.search(patron, rol):
            return clase
    texto = norm(agente.get("oficio"))
    for clase, patron, _ in CLASES:
        if re.search(patron, texto):
            return clase
    return "sin_clasificar"


# ══════════════════════════════════════════════════════════════════════
# 2. LA TABLA — clase × momento → plantilla de lugar
# ══════════════════════════════════════════════════════════════════════
# Plantillas: {sitio} la aldea del agente · {sitio}:X una locación suya ·
# {zona} el agua de su nodo (ZG2 o ZA1) · Capubana el cerro ·
# {jaguey} el agua dulce que le toca (su jagüey, o la fuente del cerro en la
# seca larga) · camino:{sitio}>{destino} el camino.
#
# `etiqueta` y `fuente` son de la FILA, no de la celda: dicen con qué se
# sostiene el día de ese oficio. Las celdas que el canon fecha de verdad
# (la pesca con jachos de noche, el biro de la seca, el mediodía sin trabajo)
# van en `excepciones`, que manda sobre la fila en ese período.

T = "{sitio}"
ESCENA = {
    "pesca": {
        "dia": {"amanecer": "{zona}", "mañana": "{zona}", "mediodia": T,
                "tarde": "{sitio}:orilla", "anochecer": "{sitio}:orilla", "noche": T},
        "excepciones": {
            # ecologia-078 + clima P1: la pesca nocturna del cunaro con jachos
            # untados de su propia manteca es del Tiempo de Viento.
            "viento": {"noche": "{zona}"},
            # clima P3: «el salinar está parado» y el chubasco cierra el agua.
            "siembra": {"tarde": T, "anochecer": T},
        },
        "etiqueta": "canon-simulacion",
        "fuente": ["ecologia-015", "ecologia-026", "ecologia-036", "ecologia-078",
                   "clima_era2.yaml frases_del_cargador"],
    },
    "marisqueo": {
        "dia": {"amanecer": "{sitio}:orilla", "mañana": "{sitio}:orilla", "mediodia": T,
                "tarde": "{sitio}:orilla", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["ecologia-012", "ecologia-044", "ecologia-061", "ecologia-081"],
    },
    "vigia": {
        "dia": {"amanecer": "{sitio}:punta", "mañana": "{sitio}:punta", "mediodia": T,
                "tarde": "{sitio}:punta", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (la atalaya); canon-simulacion (el día)",
        "fuente": ["ecologia-080", "hueco-lex-002", "sitios_era2.yaml Carirubana.mar_y_pesca"],
    },
    "sal": {
        "dia": {"amanecer": "{sitio}:salinar", "mañana": "{sitio}:salinar", "mediodia": T,
                "tarde": "{sitio}:salinar", "anochecer": T, "noche": T},
        "excepciones": {
            # clima P3 noche: «el salinar está parado». El biro es de la seca.
            "siembra": {"amanecer": T, "mañana": "{sitio}:conuco",
                        "tarde": "{sitio}:conuco", "noche": T},
        },
        "etiqueta": "atestiguado (el ciclo); canon-simulacion (el día)",
        "fuente": ["ecologia-009", "ecologia-010", "hueco-lex-005",
                   "clima_era2.yaml abre_y_cierra.Tacuato"],
    },
    "conuco": {
        "dia": {"amanecer": "{sitio}:conuco", "mañana": "{sitio}:conuco", "mediodia": T,
                "tarde": "{sitio}:conuco", "anochecer": T, "noche": T},
        "excepciones": {
            # clima P2: «el conuco espera, seco».
            "seca_larga": {"mañana": T, "tarde": T},
        },
        "etiqueta": "atestiguado (el conuco); canon-simulacion (el día)",
        "fuente": ["ecologia-029", "ecologia-030", "ecologia-083",
                   "sitios_era2.yaml Caseto.tierra"],
    },
    "agua_dulce": {
        "dia": {"amanecer": "{jaguey}", "mañana": "{jaguey}", "mediodia": T,
                "tarde": "{jaguey}", "anochecer": T, "noche": T},
        "excepciones": {
            # clima P2 amanecer: «se va al jagüey, O A LA FUENTE DEL CERRO».
            # En la seca larga el jagüey baja y el cerro no cierra nunca.
            "seca_larga": {"amanecer": "Capubana:fuente", "mañana": "Capubana:fuente",
                           "tarde": "Capubana:fuente"},
        },
        "etiqueta": "atestiguado (la fuente del cerro); canon-simulacion (el oficio)",
        "fuente": ["ecologia-008", "ecologia-028", "arcaya-1920 p. 22",
                   "estructura_social_era2.yaml of-06",
                   "clima_era2.yaml abre_y_cierra.Capubana"],
    },
    "monte": {
        "dia": {"amanecer": T, "mañana": "{sitio}:matorral", "mediodia": T,
                "tarde": "{sitio}:matorral", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["ecologia-018", "ecologia-019", "ecologia-077", "ecologia-082",
                   "creencia-020"],
    },
    "alfareria": {
        "dia": {"amanecer": T, "mañana": "{sitio}:taller", "mediodia": T,
                "tarde": "{sitio}:taller", "anochecer": T, "noche": T},
        "excepciones": {
            # clima abre_y_cierra.Moruy: la lluvia descubre el barro de Abudure.
            "siembra": {"mañana": "{sitio}:barrial"},
        },
        "etiqueta": "atestiguado (la cadena técnica); canon-simulacion (el día)",
        "fuente": ["ecologia-013", "ecologia-014", "ecologia-025", "transmision-003"],
    },
    "fibra": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": "{sitio}:taller", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["ecologia-023", "ecologia-024", "sitios_era2.yaml *.materiales"],
    },
    "canoa": {
        "dia": {"amanecer": "{sitio}:orilla", "mañana": "{sitio}:taller_canoas", "mediodia": T,
                "tarde": "{sitio}:taller_canoas", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (la canoa); canon-simulacion (el día)",
        "fuente": ["ecologia-031", "ecologia-032", "hueco-lex-008", "transmision-002"],
    },
    "casa": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["transmision-007", "ecologia-081", "estructura_social_era2.yaml niveles"],
    },
    "mando": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (el diao que redistribuye); canon-simulacion (el día)",
        "fuente": ["creencia-001b", "creencia-013", "parentesco-037",
                   "estructura_social_era2.yaml of-01"],
    },
    "mensajeria": {
        # El único oficio cuyo lugar no lo manda la hora del sol sino el
        # recado. Sale de su sitio, anda, llega a una casa a la hora de comer
        # y de hablar, y vuelve. A qué casa llega es LO ÚNICO que la escena
        # sortea (ver §4b y la pregunta 6).
        "dia": {"amanecer": T, "mañana": "camino", "mediodia": "camino",
                "tarde": "camino", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "reconstruido (of-12); canon-simulacion (el recorrido)",
        "fuente": ["estructura_social_era2.yaml of-12", "creencia-010",
                   "elenco_era2.yaml agentes[Humohumo|Chuchubi|Bajari].oficio"],
    },
    "oraculo": {
        "dia": {"amanecer": "Capubana", "mañana": "Capubana", "mediodia": "Capubana",
                "tarde": "Capubana", "anochecer": "Capubana", "noche": "Capubana"},
        "excepciones": {},
        "etiqueta": "atestiguado (el encierro de 1-3 días); canon-simulacion (que viva en el cerro)",
        "fuente": ["creencia-002", "creencia-004", "arcaya-1920 pp. 97-100",
                   "estructura_social_era2.yaml of-02, of-04"],
    },
    "curacion": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (un boratio por pueblo principal)",
        "fuente": ["creencia-001", "creencia-007", "arcaya-1920 pp. 97-100",
                   "estructura_social_era2.yaml of-03"],
    },
    "huesos": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (el rito); reconstruido (quién lo hace)",
        "fuente": ["creencia-010b", "creencia-010c", "creencia-011",
                   "estructura_social_era2.yaml of-09"],
    },
    "cantor": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "atestiguado (el canto de noche)",
        "fuente": ["creencia-010", "transmision-006", "transmision-018",
                   "estructura_social_era2.yaml of-08"],
    },
    "arbitraje": {
        "dia": {"amanecer": T, "mañana": "{sitio}:conuco", "mediodia": T,
                "tarde": "{sitio}:orilla", "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "hipotetico (of-13)",
        "fuente": ["estructura_social_era2.yaml of-13", "oliver-1989-cap3 p. 275"],
    },
    "merejuy": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "hipotetico (of-07)",
        "fuente": ["estructura_social_era2.yaml of-07",
                   "clima_era2.yaml abre_y_cierra.Moruy"],
    },
    "memoria_de_casa": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "reconstruido (la matriarca)",
        "fuente": ["parentesco-005", "parentesco-022", "transmision-008"],
    },
    "vision": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["transmision-014", "creencia-005"],
    },
    "ninez": {
        "dia": {"amanecer": T, "mañana": T, "mediodia": T,
                "tarde": T, "anochecer": T, "noche": T},
        "excepciones": {},
        "etiqueta": "canon-simulacion",
        "fuente": ["transmision-025", "transmision-027", "transmision-029"],
    },
}

# Los sitios sin playa propia y el agua que les toca: la decisión p5 del
# 2026-09-16 dice que Caseto está a ~22 km de ZA1 («a un día de ida») y la
# casa del Manaure (Moruy) no tiene playa por construcción.
SIN_PLAYA = {"Moruy", "Capubana"}
PLAYA_LEJOS = {"Caseto"}
# El barro de loza tiene sitio y fuente: las vetas de Abudure, junto a Moruy,
# «pueden verse en los cangilones labrados por la lluvia» (Esteves p. 11).
# En los demás sitios la alfarera trabaja en el taller de su casa.
BARRIAL_EN = {"Moruy"}
# El agua dulce que le toca a cada sitio.
JAGUEY_DE = {
    "Tacuato": "Tacuato:jaguey",       # los jagüeyes de Tacuato (P2 decisión)
    "El Cayude": "El Cayude:jaguey",
    "Moruy": "Capubana:fuente",        # la casa del cerro bebe del cerro
    "Capubana": "Capubana:fuente",
    "Caseto": "Caseto:jaguey",
    "Carirubana": "Carirubana:jaguey",
}


def resolver(plantilla: str, agente: dict) -> str:
    """La plantilla, con el sitio, la zona y el agua del agente."""
    sitio = agente.get("ubicacion_default") or "?"
    zona = agente.get("zona_de_pesca")
    if plantilla == "{zona}":
        if not zona:
            return sitio
        return zona
    if plantilla == "{jaguey}":
        return JAGUEY_DE.get(sitio, f"{sitio}:jaguey")
    if plantilla == "camino":
        return f"camino:{sitio}"
    out = plantilla.replace("{sitio}", sitio)
    if out.endswith(":barrial") and sitio not in BARRIAL_EN:
        return f"{sitio}:taller"
    # Un sitio sin playa no tiene orilla ni punta ni salinar propios: su gente
    # se queda en la aldea. No se inventa geografía.
    if sitio in SIN_PLAYA and out.split(":")[-1] in ("orilla", "punta", "salinar",
                                                     "taller_canoas"):
        return sitio
    return out


def lugar_de(agente: dict, momento: str, periodo: str) -> str:
    fila = ESCENA.get(clase_en(agente, periodo))
    if not fila:
        return agente.get("ubicacion_default") or "?"
    plantilla = fila["excepciones"].get(periodo, {}).get(momento) or fila["dia"][momento]
    return resolver(plantilla, agente)


# ── el alcance de la mensajería, leído de la ficha ──────────────────────
def destinos_de(agente: dict, sitios_todos: list, casas_sitio: list) -> list:
    """A qué sitios puede llegar un mensajero, según lo que SU FICHA dice.
    No hay lista escrita a mano: se leen los sitios nombrados en el oficio, y
    las dos fórmulas que el elenco usa («las cuatro casas», «de casa en casa
    cuando el cerro convoca»)."""
    texto = norm(agente.get("oficio"))
    propio = agente.get("ubicacion_default")
    dest = [s for s in sitios_todos if norm(s) in texto and s != propio]
    if "cuatro casas" in texto:
        dest = [s for s in casas_sitio if s != propio]
    if "de casa en casa" in texto:
        dest = [s for s in casas_sitio if s != propio]
        if "cerro" in texto:
            dest.append("Capubana")
    return sorted(dict.fromkeys(dest))


# ══════════════════════════════════════════════════════════════════════
# 3. DE QUÉ NODO ES CADA LUGAR
# ══════════════════════════════════════════════════════════════════════
# No se declara por lugar: se lee del mapa. El nodo de `Tacuato:orilla` es el
# de Tacuato; el de ZG2, el de quien la pesca. Sólo dos lugares se declaran
# COMPARTIDOS, y los dos por decisión citada.
COMPARTIDOS_DECLARADOS = {
    # decision_creativa_2026-09-14.capubana: «centro compartido que congrega y
    # centraliza lo espiritual… no necesariamente como institución sino a
    # nivel energético».
    "Capubana": "estructura_social_era2.yaml decision_creativa_2026-09-14.capubana",
    "Capubana:fuente": "clima_era2.yaml abre_y_cierra.Capubana (NO CIERRA NUNCA)",
}


def nodo_de_lugar(lugar: str, nodos_presentes: set) -> str:
    if lugar in COMPARTIDOS_DECLARADOS:
        return "COMPARTIDO"
    if len(nodos_presentes) > 1:
        return "COMPARTIDO"
    return next(iter(nodos_presentes)) if nodos_presentes else "?"


# ══════════════════════════════════════════════════════════════════════
# 4. CARGA Y MEDICIÓN
# ══════════════════════════════════════════════════════════════════════

def cargar(ruta: str) -> dict:
    if yaml is None:
        raise SystemExit("hace falta pyyaml")
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def haversine(a, b) -> float:
    (la1, lo1), (la2, lo2) = a, b
    r = 6371.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(lo2 - lo1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def elenco() -> list:
    d = cargar(RUTA_ELENCO)
    ag = list(d.get("agentes") or [])
    for a in ag:
        a["_clase"] = clase_de(a)
    return ag


def coordenadas() -> dict:
    """{sitio: (lat, lon)} del canon de sitios de la era 2."""
    d = cargar(RUTA_SITIOS)
    return {s["sitio"]: (s["lat"], s["lon"]) for s in (d.get("sitios") or [])
            if s.get("lat") is not None and s.get("lon") is not None}


# ── los puntos que el canon ya tiene, para que la escena se pueda VER ──
RUTA_TOPONIMOS = os.path.join(_RAIZ, "2-lengua", "toponimos.yaml")
_COORD = re.compile(r"(-?\d{1,2}\.\d{2,6})\s+(-?\d{1,3}\.\d{2,6})")

# El lugar de la tabla que NO es una aldea pero SÍ tiene punto en el canon,
# con el nombre bajo el que está registrado. Lo que no esté aquí ni sea una
# aldea se cuenta como SIN COORDENADA — que es el dato que interesa.
ALIAS_DE_PUNTO = {
    "El Cayude:punta": "Punta Cuara",
    "Carirubana:punta": "Sarabón",                  # Esteves p. 58, sin punto OSM
    "Carirubana:salinar": "Laguna de Guaranao",
    "Caseto:salinar": "Punta Salinas",
    "Moruy:barrial": "abudure",                     # mapa vivo, toponimos.yaml
    "Capubana:fuente": "Cerro Santa Ana (el Capubana, Cerro de Capú)",
}


def puntos_del_canon() -> dict:
    """{nombre: (lat, lon)} de todo lo que el canon de la era 2 ya sitúa:
    sitios, zonas pesqueras, lugares del Kapubana, y el mapa vivo de
    2-lengua/toponimos.yaml (`mapa_vivo`, que trae el par de OSM en prosa)."""
    pts = {}

    def poner(nombre, lat, lon):
        if nombre and lat is not None and lon is not None:
            pts.setdefault(str(nombre), (float(lat), float(lon)))

    for s in (cargar(RUTA_SITIOS).get("sitios") or []):
        poner(s.get("sitio"), s.get("lat"), s.get("lon"))
    el = cargar(RUTA_ELENCO)
    for c in (el.get("casas") or []):
        sit = c.get("sitio") or {}
        poner(sit.get("nombre"), sit.get("lat"), sit.get("lon"))
    for s in (el.get("sitios_sin_casa") or []):
        poner(s.get("nombre"), s.get("lat"), s.get("lon"))
    est = cargar(RUTA_ESTRUCTURA)
    for grupo in ("GUARANAO", "AMUAY", "zona_en_disputa"):
        for z in (est.get("zonas_pesqueras") or {}).get(grupo) or []:
            for l in z.get("lugares") or []:
                poner(l.get("nombre"), l.get("lat"), l.get("lon"))
    for l in (est.get("institucion_kapubana") or {}).get("lugares") or []:
        co = l.get("coordenadas") or {}
        poner(l.get("nombre"), co.get("lat"), co.get("lon"))
    for t in (cargar(RUTA_TOPONIMOS).get("toponimos") or []):
        m = _COORD.search(str(t.get("mapa_vivo") or ""))
        if m:
            poner(t.get("forma"), m.group(1), m.group(2))
    return pts


def punto_de_lugar(lugar: str, pts: dict, zonas: dict) -> tuple:
    """(clase de punto, dato). Clases: `propio` (el canon lo sitúa),
    `heredado` (hereda el de su aldea), `zona` (polilínea de sus lugares),
    `arista` (un camino entre dos puntos), `sin-coordenada`."""
    if lugar in pts:
        return "propio", pts[lugar]
    alias = ALIAS_DE_PUNTO.get(lugar)
    if alias and alias in pts:
        return "propio", pts[alias]
    if alias:
        return "sin-coordenada", f"«{alias}» está en el canon sin lat/lon"
    if lugar in zonas:
        return "zona", zonas[lugar]
    if lugar.startswith("camino:"):
        origen = lugar.split(":", 1)[1]
        return ("arista", origen) if origen in pts else ("sin-coordenada", lugar)
    aldea = lugar.split(":")[0]
    if aldea in pts:
        return "heredado", pts[aldea]
    return "sin-coordenada", lugar


def zonas_de_pesca_puntos() -> dict:
    """{ZG2|ZA1: [puntos]} — una zona no es un punto: es el conjunto de sus
    lugares, que es lo que un visor dibujaría como área."""
    est = cargar(RUTA_ESTRUCTURA)
    out = {}
    for grupo in ("GUARANAO", "AMUAY"):
        for z in (est.get("zonas_pesqueras") or {}).get(grupo) or []:
            pts = [(l["nombre"], l["lat"], l["lon"]) for l in z.get("lugares") or []
                   if l.get("lat") is not None]
            if pts:
                out[z["id"]] = pts
    return out


def cruzados(ag: list) -> list:
    """Los que viven en un nodo y son de linaje del otro: el canal que el canon
    escribió (elenco_era2.yaml §como_se_enlazan_las_casas). Se deriva del
    linaje del agente contra el linaje declarado de su casa, no de una lista."""
    d = cargar(RUTA_ELENCO)
    linaje_de_casa = {c["casa"]: c.get("linaje_d1") for c in (d.get("casas") or [])}
    nodo_de_casa = {c["casa"]: c.get("nodo") for c in (d.get("casas") or [])}
    nodo_de_linaje = {}
    for c in (d.get("casas") or []):
        if c.get("linaje_d1"):
            nodo_de_linaje.setdefault(c["linaje_d1"], c.get("nodo"))
    out = []
    for a in ag:
        linaje = str(a.get("linaje") or "").split(" (")[0].strip()
        casa = a.get("casa")
        if not linaje or linaje not in nodo_de_linaje:
            continue
        if nodo_de_linaje[linaje] != nodo_de_casa.get(casa):
            out.append({
                "nombre": a["nombre"], "vive_en": a.get("ubicacion_default"),
                "nodo": a.get("nodo"), "linaje": linaje,
                "origen": nodo_de_linaje[linaje],
                "rol": a.get("rol_en_la_casa"),
                "en_roster": bool(a.get("en_roster")),
                "clase": a["_clase"],
            })
    return out


def ocupacion(ag: list, periodo: str) -> dict:
    """{(lugar, momento): Counter{nodo: n}}"""
    out = collections.defaultdict(collections.Counter)
    for a in ag:
        for m in MOMENTOS:
            out[(lugar_de(a, m, periodo), m)][a.get("nodo")] += 1
    return out


# ══════════════════════════════════════════════════════════════════════
# 5. LO QUE HAY HOY EN EL MOTOR (opcional, --motor)
# ══════════════════════════════════════════════════════════════════════

def medir_motor() -> list:
    """Cuántas veces el motor ESCRIBE una ubicación, y cuántas la lee."""
    lineas = []
    escrituras = re.compile(r"ubicaciones_override\s*\[|ubicaciones_override\s*=|"
                            r"ubicaciones_override\.update|ubicaciones_override\.setdefault")
    lecturas = re.compile(r"ubicaciones_override")
    n_esc = n_lec = 0
    for base, _, ficheros in os.walk(_SIM):
        if "tests" in base or "__pycache__" in base:
            continue
        for f in ficheros:
            if not f.endswith(".py"):
                continue
            ruta = os.path.join(base, f)
            with open(ruta, encoding="utf-8", errors="replace") as fh:
                for i, l in enumerate(fh, 1):
                    if "ubicaciones_override" not in l:
                        continue
                    if l.lstrip().startswith("#"):
                        continue
                    n_lec += 1
                    if escrituras.search(l) and "field(" not in l:
                        n_esc += 1
                        lineas.append(f"    escritura: {os.path.relpath(ruta, _RAIZ)}:{i}")
    lineas.insert(0, f"  usos de `ubicaciones_override` fuera de tests: {n_lec} "
                     f"(escrituras reales: {n_esc})")
    return lineas


# ══════════════════════════════════════════════════════════════════════
# 6. SALIDA
# ══════════════════════════════════════════════════════════════════════

def informe(ag: list, con_motor: bool = False):
    print("=" * 72)
    print("  ESCENA POR LUGAR — derivada de 6-fusion/elenco_era2.yaml")
    print("=" * 72)

    # ── clases ────────────────────────────────────────────────────────
    por_clase = collections.defaultdict(list)
    for a in ag:
        por_clase[a["_clase"]].append(a["nombre"])
    sin = por_clase.get("sin_clasificar", [])
    print(f"\n[1] CLASES DE OFICIO — {len(ag)} agentes en "
          f"{len([c for c in por_clase if c != 'sin_clasificar'])} clases; "
          f"sin clasificar: {len(sin)}")
    orden = [c for c, _, _ in CLASES] + ["ninez", "sin_clasificar"]
    for c in orden:
        if c not in por_clase:
            continue
        nombres = sorted(por_clase[c])
        print(f"  {c:<16} {len(nombres):>2}  {', '.join(nombres)}")

    # ── cobertura ─────────────────────────────────────────────────────
    print("\n[2] COBERTURA — ¿tiene cada agente un lugar en cada momento?")
    for p in PERIODOS:
        completos = sum(1 for a in ag
                        if all(lugar_de(a, m, p) not in (None, "", "?") for m in MOMENTOS))
        print(f"  {p:<11} {completos} de {len(ag)} con lugar en los 6 momentos")
    lugares = sorted({lugar_de(a, m, p) for a in ag for m in MOMENTOS for p in PERIODOS})
    print(f"  lugares distintos en los tres períodos: {len(lugares)}")
    print("   ", ", ".join(lugares))

    # ── ocupación ─────────────────────────────────────────────────────
    for p in PERIODOS:
        occ = ocupacion(ag, p)
        print(f"\n[3] OCUPACIÓN — período {p}")
        print(f"  {'lugar':<24}" + "".join(f"{m[:5]:>9}" for m in MOMENTOS))
        for lug in sorted({l for l, _ in occ}):
            fila = []
            for m in MOMENTOS:
                c = occ.get((lug, m))
                fila.append(f"{sum(c.values()):>9}" if c else f"{'·':>9}")
            print(f"  {lug:<24}" + "".join(fila))
        # escenas por momento
        print("  escenas (lugares con alguien) por momento: "
              + ", ".join(f"{m}={len({l for (l, mm) in occ if mm == m})}" for m in MOMENTOS))

    # ── compartidos ───────────────────────────────────────────────────
    print("\n[4] LUGARES COMPARTIDOS — dónde coinciden de hecho GUARANAO y AMUAY")
    emergentes = []
    for p in PERIODOS:
        occ = ocupacion(ag, p)
        for (lug, m), c in sorted(occ.items()):
            nodos = {n for n, v in c.items() if v}
            if len(nodos) > 1:
                emergentes.append((p, m, lug,
                                   " + ".join(f"{n} {v}" for n, v in sorted(c.items()))))
    print(f"  (a) EMERGENTES — los dos nodos en el mismo lugar el mismo momento: "
          f"{len(emergentes)}")
    for p, m, lug, reparto in emergentes:
        print(f"      {p:<11} {m:<10} {lug:<20} {reparto}")
    if not emergentes:
        print("      ninguno. La escena derivada del elenco NO produce contacto por")
        print("      sí sola: cada oficio trabaja en lugares de su nodo los 6 momentos")
        print("      de los 3 períodos. El contacto hay que declararlo o hacerlo viajar.")
    print(f"  (b) DECLARADOS compartidos por decisión: "
          f"{', '.join(sorted(COMPARTIDOS_DECLARADOS))}")
    for lug, razon in sorted(COMPARTIDOS_DECLARADOS.items()):
        quien = collections.Counter()
        for p in PERIODOS:
            for (l, m), c in ocupacion(ag, p).items():
                if l == lug:
                    quien.update(c)
        reparto = " + ".join(f"{n}" for n in sorted(quien)) or "nadie"
        print(f"      {lug:<20} lo ocupa: {reparto}   ← {razon}")

    # ── alcance de la mensajería ──────────────────────────────────────
    d_el = cargar(RUTA_ELENCO)
    casas_sitio = [c["sitio"]["nombre"] for c in (d_el.get("casas") or [])]
    nodo_sitio = {c["sitio"]["nombre"]: c["nodo"] for c in (d_el.get("casas") or [])}
    nodo_sitio["Capubana"] = "COMPARTIDO"
    sitios_todos = casas_sitio + [s["nombre"] for s in (d_el.get("sitios_sin_casa") or [])]
    print("\n[4b] ALCANCE DE LA MENSAJERÍA — el único oficio que cruza por sí solo")
    total_cruza = 0
    for a in ag:
        if a["_clase"] != "mensajeria":
            continue
        dest = destinos_de(a, sitios_todos, casas_sitio)
        fuera = [d for d in dest if nodo_sitio.get(d) not in (a["nodo"], None)]
        total_cruza += len(fuera)
        print(f"  {a['nombre']:<10} {a['nodo']:<9} desde {a['ubicacion_default']:<11} "
              f"→ {', '.join(dest) or '(ninguno nombrado)'}")
        print(f"  {'':<10} de esos, del OTRO nodo o compartidos: "
              f"{', '.join(fuera) or 'ninguno'}")
    print(f"  destinos fuera del propio nodo, sumados los tres mensajeros: {total_cruza}")

    # ── cruzados ──────────────────────────────────────────────────────
    cr = cruzados(ag)
    print(f"\n[5] CRUZADOS POR MATRIMONIO — {len(cr)} viven en el nodo del cónyuge "
          f"({sum(1 for c in cr if c['en_roster'])} en el roster)")
    for c in sorted(cr, key=lambda x: (x["nodo"], x["nombre"])):
        r = "roster" if c["en_roster"] else "      "
        print(f"  {c['nombre']:<11} {c['origen']:<9} → {c['nodo']:<9} "
              f"{c['vive_en']:<11} {c['clase']:<14} {r}  {c['rol']}")

    # ── distancias ────────────────────────────────────────────────────
    coords = coordenadas()
    print(f"\n[6] DISTANCIAS ENTRE SITIOS (km, de las coordenadas del canon)")
    nodos_sitio = {}
    d = cargar(RUTA_SITIOS)
    for s in (d.get("sitios") or []):
        nodos_sitio[s["sitio"]] = s.get("nodo")
    pares = []
    ns = [s for s in coords if nodos_sitio.get(s)]
    for i, a in enumerate(ns):
        for b in ns[i + 1:]:
            pares.append((haversine(coords[a], coords[b]), a, b,
                          "intra" if nodos_sitio[a] == nodos_sitio[b] else "ENTRE"))
    for km, a, b, tipo in sorted(pares)[:8]:
        print(f"  {km:6.1f}  {a} – {b}   ({tipo})")
    intra = [k for k, _, _, t in pares if t == "intra"]
    entre = [k for k, _, _, t in pares if t == "ENTRE"]
    print(f"  media intra {sum(intra)/len(intra):.1f} km · "
          f"media entre {sum(entre)/len(entre):.1f} km")

    # ── coordenadas: ¿se puede VER esta escena sobre el mapa? ──────────
    pts = puntos_del_canon()
    zonas = zonas_de_pesca_puntos()
    print(f"\n[7] COORDENADAS — {len(pts)} puntos con lat/lon en el canon de la era 2")
    clases_pt = collections.Counter()
    detalle = collections.defaultdict(list)
    for lug in lugares:
        clase_pt, dato = punto_de_lugar(lug, pts, zonas)
        clases_pt[clase_pt] += 1
        detalle[clase_pt].append(lug)
    glosa = {
        "propio": "el canon los sitúa con lat/lon propios",
        "heredado": "se dibujarían ENCIMA de su aldea: no tienen punto propio",
        "zona": "no son un punto: son el área de sus lugares (polilínea)",
        "arista": "no son un punto: son un camino entre dos aldeas",
        "sin-coordenada": "ni punto, ni aldea, ni área",
    }
    for k in ("propio", "heredado", "zona", "arista", "sin-coordenada"):
        n = clases_pt.get(k, 0)
        print(f"  {k:<16} {n:>2} de {len(lugares)} — {glosa[k]}")
        if n:
            print(f"    {', '.join(detalle[k])}")

    # ── el corpus ya está indexado por locación ───────────────────────
    print("\n[8] EL CORPUS POR LOCACIÓN — lo que ya se puede decir en cada tipo de lugar")
    cuenta = collections.Counter()
    for ruta in ("3-mundo/corpus/ecologia.yaml", "3-mundo/corpus/transmision.yaml",
                 "3-mundo/corpus/creencia.yaml"):
        d = cargar(os.path.join(_RAIZ, ruta))
        secs = d.values() if isinstance(d, dict) else [d]
        for s in secs:
            if not isinstance(s, list):
                continue
            for h in s:
                if isinstance(h, dict) and h.get("id"):
                    cuenta[h.get("locacion") or "(sin locación)"] += 1
    total = sum(cuenta.values())
    con = total - cuenta.get("(sin locación)", 0)
    print(f"  {con} de {total} hechos del corpus (ecología, transmisión, creencia) "
          f"traen `locacion`")
    for loc, n in cuenta.most_common():
        print(f"    {loc:<16} {n:>3}")

    if con_motor:
        print("\n[9] EL MOTOR DE HOY")
        for l in medir_motor():
            print(l)


def escribir_yaml(ag: list):
    """La tabla y lo medido, como propuesta (regla 5: propone, no fusiona)."""
    por_clase = collections.defaultdict(list)
    for a in ag:
        por_clase[a["_clase"]].append(a["nombre"])

    def bloque_ocupacion(p):
        occ = ocupacion(ag, p)
        out = {}
        for (lug, m), c in occ.items():
            out.setdefault(lug, {})[m] = {
                "n": sum(c.values()),
                "por_nodo": {k: v for k, v in sorted(c.items())},
                "nodo": nodo_de_lugar(lug, {n for n, v in c.items() if v}),
            }
        return out

    doc = {
        "meta": {
            "fecha": "2026-09-17",
            "estado": "sin-fusionar. PROPONE (regla 5). No toca el motor, ni el "
                      "elenco generado, ni el corpus.",
            "obra": "varias",
            "quien": "escriba (Claude), a pedido de Miguel",
            "pregunta": "¿Dónde está cada uno de los 63 en cada uno de los seis "
                        "momentos del día, y qué lugares acaban compartiendo los "
                        "dos nodos?",
            "lee": "6-fusion/issues-pendientes/existir-en-el-mundo-escena-por-lugar-2026-09-17.md",
            "medido_por": "python 6-fusion/scripts/derivar_escena_por_lugar.py --yaml",
            "derivado_de": ["6-fusion/elenco_era2.yaml", "6-fusion/sitios_era2.yaml",
                            "6-fusion/clima_era2.yaml",
                            "6-fusion/estructura_social_era2.yaml"],
            "aviso": "Ninguna fila se escribió agente a agente: la clase de oficio "
                     "sale de `oficio` y `rol_en_la_casa` por palabras clave "
                     "declaradas (§reglas_de_clase) y el lugar sale de una "
                     "plantilla resuelta con la ficha. Cambiar el elenco cambia "
                     "esta tabla sin tocarla.",
        },
        "reglas_de_clase": {
            "orden": "la primera regla que casa gana; antes corre la de rol",
            "por_rol": [{"patron": p, "clase": c} for p, c in PRE_ROL],
            "por_oficio": [{"clase": c, "patron": p, "glosa": g} for c, p, g in CLASES],
        },
        "plantillas": {
            "{sitio}": "la aldea del agente (su ubicacion_default de hoy)",
            "{sitio}:X": "una locación suya: orilla, conuco, matorral, salinar, "
                         "jaguey, punta, taller, taller_canoas, barrial",
            "{zona}": "el agua de su nodo: ZG2 (GUARANAO) o ZA1 (AMUAY)",
            "{jaguey}": "el agua dulce que le toca; en Moruy y en el cerro es la fuente",
            "Capubana": "el cerro, centro declarado compartido",
            "camino:{sitio}": "el camino que sale de su sitio",
            "sin_playa": sorted(SIN_PLAYA),
            "playa_a_un_dia": sorted(PLAYA_LEJOS),
        },
        "tabla": {
            clase: {
                "glosa": next((g for c, _, g in CLASES if c == clase), ""),
                "agentes": sorted(por_clase.get(clase, [])),
                "n": len(por_clase.get(clase, [])),
                "etiqueta": fila["etiqueta"],
                "fuente": fila["fuente"],
                "dia": dict(fila["dia"]),
                "excepciones_por_periodo": fila["excepciones"] or None,
            }
            for clase, fila in ESCENA.items()
        },
        "cobertura": {
            p: {
                "con_lugar_en_los_seis": sum(
                    1 for a in ag if all(lugar_de(a, m, p) for m in MOMENTOS)),
                "de": len(ag),
            } for p in PERIODOS
        },
        "ocupacion": {p: bloque_ocupacion(p) for p in PERIODOS},
        "escena_por_agente": {
            a["nombre"]: {
                "nodo": a.get("nodo"), "sitio": a.get("ubicacion_default"),
                "clase": a["_clase"],
                **{p: [lugar_de(a, m, p) for m in MOMENTOS] for p in PERIODOS},
            } for a in sorted(ag, key=lambda x: (x.get("nodo"), x["nombre"]))
        },
        "puntos": {
            "para_que": "para poder VER la escena sobre el mapa real: cada lugar con "
                        "el punto que el canon ya le da, o el de su aldea si no tiene "
                        "uno propio.",
            "fuentes": ["6-fusion/sitios_era2.yaml", "6-fusion/elenco_era2.yaml",
                        "6-fusion/estructura_social_era2.yaml zonas_pesqueras + "
                        "institucion_kapubana.lugares",
                        "2-lengua/toponimos.yaml (campo mapa_vivo, OSM)"],
            "lugares": {
                lug: {"tipo": punto_de_lugar(lug, puntos_del_canon(),
                                             zonas_de_pesca_puntos())[0],
                      "dato": punto_de_lugar(lug, puntos_del_canon(),
                                             zonas_de_pesca_puntos())[1]}
                for lug in sorted({lugar_de(a, m, p) for a in ag
                                   for m in MOMENTOS for p in PERIODOS})
            },
        },
        "compartidos_declarados": COMPARTIDOS_DECLARADOS,
        "cruzados_por_matrimonio": cruzados(ag),
        "sin_clasificar": sorted(por_clase.get("sin_clasificar", [])),
    }
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        f.write("# ─────────────────────────────────────────────────────────────\n"
                "# GENERADO por 6-fusion/scripts/derivar_escena_por_lugar.py\n"
                "# No se edita a mano: se edita el script (la tabla ESCENA) y se\n"
                "# regenera con --yaml.\n"
                "# ─────────────────────────────────────────────────────────────\n")
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=88)
    print(f"\n✓ escrito {os.path.relpath(RUTA_SALIDA, _RAIZ)}")


def main():
    _forzar_utf8()
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yaml", action="store_true",
                    help="reescribe 6-fusion/escena_por_lugar_propuesta_2026-09-17.yaml")
    ap.add_argument("--motor", action="store_true",
                    help="mide también lo que el motor hace hoy con la ubicación")
    args = ap.parse_args()
    ag = elenco()
    informe(ag, con_motor=args.motor)
    if args.yaml:
        escribir_yaml(ag)


if __name__ == "__main__":
    main()
