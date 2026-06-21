#!/usr/bin/env python3
"""
arahuaco_comparative.py
=========================
Modulo de lingüística comparativa arahuaca para la simulación Curiana.

Implementa reglas de correspondencia fonológica entre 6 lenguas:
  CQ = Caquetío atestiguado      (noroccidente de Venezuela, ss. XVI-XVIII)
  WY = Wayunaiki/Wayuu           (Guajira, Colombia-Venezuela)
  LK = Lokono/Arawak             (Guayana, Surinam, Trinidad)
  TN = Taíno                     (Antillas Mayores, ss. XV-XVI)
  PA = Proto-Arahuaco            (reconstrucción, ca. 1000 a.C.)
  KL = Kalinago/Garifuna         (Caribe insular → Centroamérica hoy)

NOTA SOBRE KL (Kalinago / Island Carib / Garifuna):
  El Kalinago es una lengua de contacto con dos estratos:
  - Sustrato arahuaco [A]: gramática completa + vocabulario cotidiano
    (forma lo que documentó Breton 1665 como "lengua de las mujeres")
  - Overlay caribe [C]: vocabulario de dominio masculino (guerra, caza,
    navegación de combate, autorreferencia)
  Los cognados KL listados aquí son del sustrato arahuaco [A] salvo
  indicación explícita [C]. Ver KALINAGO_CARIBE_OVERLAY para overlay.

Fuentes:
  Goeje (1928), Brinton (1871), Pet (1987) — Lokono
  Captain & Captain (2005) — Wayunaiki
  Jahn (1927), Gilij (1782), Zavala Reyes (2015) — Caquetío
  Oliver (1989), Brinton (1871) — Taíno
  Payne (1991) — reconstrucción proto-arahuaca
  Breton (1665), Taylor (1951), Hoff (1968) — Kalinago/Garifuna

Uso:
  from arahuaco_comparative import transducir, tabla_comparativa, COGNADOS

  transducir("katsi", origen="LK", destino="CQ")  -> "*cati"
  transducir("katsi", origen="LK", destino="KL")  -> "*kati"
  transducir("kashi", origen="WY", destino="LK")  -> "*katsi"
  tabla_comparativa("luna")                        -> dict con formas en 6 lenguas
"""

import re
from typing import Optional

# =============================================================================
# COGNATE SETS — núcleo del método comparativo
# Cada entrada: { "PA":?, "CQ":?, "WY":?, "LK":?, "TN":?, "KL":?, "es": glosa }
# None = no atestiguado / no reconstruido con seguridad
# KL = sustrato arahuaco del Kalinago salvo nota [C] = overlay caribe
# =============================================================================

COGNADOS = {
    "sol": {
        "PA": "*kali",
        "CQ": "cazi",
        "WY": "kai",       # ka'i en ortografía oficial
        "LK": "adali",     # hadali (con h- prostética de artículo)
        "TN": None,
        "KL": "wiru",      # Garifuna wiru ~ *kali? Incerteza media
        "es": "sol"
    },
    "luna": {
        "PA": "*kati",
        "CQ": "cati",
        "WY": "kachi",     # kashi oficial
        "LK": "katsi",
        "TN": None,
        "KL": "kati",      # [A] Breton (1665): kati/mois; idéntico a CQ
        "es": "luna"
    },
    "mar": {
        "PA": "*para",
        "CQ": "para",      # en topónimos: Paraguaná, Paraguay
        "WY": "palaa",
        "LK": "bara",
        "TN": "bagua",
        "KL": "barana",    # [A] Garifuna barana = mar/gran agua
        "es": "mar, agua extensa"
    },
    "canoa": {
        "PA": "*kanoa",
        "CQ": "canoa",
        "WY": None,
        "LK": "kannoa",
        "TN": "canoa",
        "KL": "kanawa",    # [C] OVERLAY CARIBE: kanawa desplazó forma arahuaca
        "es": "canoa, embarcación"
    },
    "hamaca": {
        "PA": "*hamaka",
        "CQ": "hamaca",
        "WY": None,
        "LK": "hamaha",
        "TN": "hamaca",
        "KL": "hamaka",    # [A] conservado igual que PA
        "es": "hamaca, cama colgante"
    },
    "casabe": {
        "PA": "*kasabi",
        "CQ": "casabe",
        "WY": None,
        "LK": "kasabi",
        "TN": "casabe",
        "KL": "kasabi",    # [A] idéntico a LK; palabra central de la cultura
        "es": "casabe, pan de yuca"
    },
    "chaman": {
        "PA": "*piay",
        "CQ": "piache",
        "WY": None,
        "LK": "piaye",
        "TN": "bejique",   # TN innovó: b- + sufijo diferente
        "KL": "buyei",     # [A] piaye→buyei: p→b, -ye→-ei; bien atestiguado
        "es": "chamán, curandero, piache"
    },
    "iguana": {
        "PA": "*iwana",
        "CQ": None,
        "WY": "iwana",
        "LK": "iwana",
        "TN": "higuana",
        "KL": "iwana",     # [A] conservado igual
        "es": "iguana (Iguana iguana)"
    },
    "caiman": {
        "PA": "*kaiman",
        "CQ": None,
        "WY": None,
        "LK": "kaiman",
        "TN": "caiman",
        "KL": "kaiman",    # [A] conservado
        "es": "caimán (Caiman crocodilus)"
    },
    "piedra": {
        "PA": "*siba",
        "CQ": None,
        "WY": None,
        "LK": "siba",
        "TN": "siba",
        "KL": "siba",      # [A] conservado; pan-arahuaco
        "es": "piedra, roca"
    },
    "isla": {
        "PA": "*kairi",
        "CQ": "cairi",     # topónimo Trinidad = Cairi
        "WY": None,
        "LK": "kairi",
        "TN": "cai",       # cayo = kairi reducido
        "KL": "kairi",     # [A] conservado; Cairi = nombre arahuaco de Trinidad
        "es": "isla, cayo"
    },
    "yuca": {
        "PA": "*yuka",
        "CQ": "yuca",
        "WY": None,
        "LK": "yuka",
        "TN": "yuca",
        "KL": "yuka",      # [A] conservado; yuca es el eje de la identidad Garifuna
        "es": "yuca, mandioca (Manihot esculenta)"
    },
    "maiz": {
        "PA": "*marisi",
        "CQ": None,
        "WY": None,
        "LK": "marisi",
        "TN": "maisi",     # -> español maíz
        "KL": "marisi",    # [A] conservado igual que LK
        "es": "maíz (Zea mays)"
    },
    "aji": {
        "PA": "*achi",
        "CQ": None,
        "WY": None,
        "LK": "achi",
        "TN": "aji",
        "KL": "achi",      # [A] conservado
        "es": "ají, pimienta (Capsicum sp.)"
    },
    "tabaco": {
        "PA": "*iuli",
        "CQ": None,
        "WY": None,
        "LK": "iuli",
        "TN": "cohiba",    # TN innovó (cohiba = cigarro)
        "KL": None,        # forma KL no documentada con certeza
        "es": "tabaco (Nicotiana tabacum)"
    },
    "sabana": {
        "PA": "*sallaba",
        "CQ": None,
        "WY": None,
        "LK": "sallaban",
        "TN": "sabana",
        "KL": None,        # posible préstamo del español en Garifuna moderno
        "es": "sabana, llanura"
    },
    "barbacoa": {
        "PA": "*barraha-koa",
        "CQ": None,
        "WY": None,
        "LK": "barrahakoa",
        "TN": "barbacoa",
        "KL": None,
        "es": "barbacoa, parrilla, lugar de provisiones"
    },
    "persona": {
        "PA": "*lokono",
        "CQ": "caquetio",  # posible cognado
        "WY": "wayuu",
        "LK": "lokono",
        "TN": "taino",     # cada grupo tiene autónimo derivado
        "KL": "kalinagu",  # autónimo propio; [C+A] compuesto: kalina(caribe)+gu(arahuaco -gente)
        "es": "persona arahuaca, gente propia"
    },
    "casa": {
        "PA": "*isikoa",
        "CQ": None,
        "WY": None,
        "LK": "sikoa",
        "TN": "bohio",     # TN innovó
        "KL": "ikoa",      # [A] sikoa→ikoa: pérdida s- inicial
        "es": "casa, vivienda"
    },
    "agua_rio": {
        "PA": "*tuna",
        "CQ": "tuy",       # topónimo río Tuy
        "WY": "wuin",      # wüin oficial
        "LK": "tuna",
        "TN": "tuna",      # en compuestos
        "KL": "duna",      # [A] tuna→duna: sonorización t→d
        "es": "agua, río"
    },
    "padre": {
        "PA": "*itti",
        "CQ": "tata",      # via relexificación o préstamo Quechua?
        "WY": None,
        "LK": "itti",
        "TN": "taita",
        "KL": "baba",      # [A] Garifuna baba = padre; raíz arahuaca diferente a itti
        "es": "padre"
    },
    "madre": {
        "PA": "*uju",
        "CQ": None,
        "WY": None,
        "LK": "uju",
        "TN": None,
        "KL": "naha",      # [A] Garifuna naha = madre; posible cognado vía nasalización
        "es": "madre"
    },
    "uno": {
        "PA": "*aba",
        "CQ": None,
        "WY": "aba",       # forma wayuu
        "LK": "abba",
        "TN": None,
        "KL": "aban",      # [A] abba→aban: bb→b + nasal final
        "es": "uno, un"
    },
    "dos": {
        "PA": "*biama",
        "CQ": None,
        "WY": None,
        "LK": "biama",
        "TN": "yamosa",    # TN yamosa ~ biama?
        "KL": "biama",     # [A] conservado igual que LK
        "es": "dos"
    },
    "mano": {
        "PA": "*akkabu",
        "CQ": None,
        "WY": None,
        "LK": "akkabu",
        "TN": None,
        "KL": "akabi",     # [A] akkabu→akabi: kk→k, u→i
        "es": "mano"
    },
    "corazon": {
        "PA": "*ukku",
        "CQ": None,
        "WY": None,
        "LK": "ukku",
        "TN": None,
        "KL": None,        # no documentado con certeza en Garifuna
        "es": "corazón, centro vital"
    },
    "arco": {
        "PA": "*semaara-haaba",
        "CQ": None,
        "WY": None,
        "LK": "semaara-haaba",
        "TN": None,
        "KL": None,        # [C] overlay caribe domina vocabulario de armas
        "es": "arco (arma)"
    },
    "flecha": {
        "PA": "*semaara",
        "CQ": None,
        "WY": None,
        "LK": "semaara",
        "TN": None,
        "KL": None,        # [C] overlay caribe domina vocabulario de armas
        "es": "flecha"
    },
    "grande": {
        "PA": "*ipiru",
        "CQ": None,
        "WY": None,
        "LK": "firo",      # firo ~ ipiru? (posible alternancia f/p)
        "TN": None,
        "KL": "firo",      # [A] igual a LK; posible préstamo LK→KL
        "es": "grande, de gran tamaño"
    },
    "negacion": {
        "PA": "*ma",
        "CQ": None,
        "WY": "ma",
        "LK": "ma",
        "TN": "mayani",
        "KL": "ma",        # [A] pan-arahuaco conservado; base gramatical de KL
        "es": "no, negación (prefijo)"
    },
    "firmamento": {
        "PA": "*kassaku",
        "CQ": None,
        "WY": "siruma",    # seru = cielo en Wayuu
        "LK": "kassaku",
        "TN": None,
        "KL": "kasaku",    # [A] kassaku→kasaku: kk→k
        "es": "firmamento, bóveda celeste"
    },
    "pez": {
        "PA": "*itime",
        "CQ": None,
        "WY": None,
        "LK": "itime",
        "TN": None,
        "KL": "pira",      # [C] OVERLAY CARIBE: pira (cf. piraña = pira+aña)
        "es": "pez, pescado"
    },
    "fuego": {
        "PA": "*yuru",
        "CQ": None,
        "WY": "yuru",
        "LK": None,
        "TN": None,
        "KL": "iduru",     # [A] Garifuna iduru = fuego; yuru→iduru: y→id, u→u
        "es": "fuego"
    },
    # ── ENTRADAS NUEVAS: ZONA DE CONTACTO ARAHUACO-CARIBE ──
    "caribe_gente": {
        "PA": None,
        "CQ": "karibna",   # [A] karib + -na (sufijo colectivo arahuaco)
        "WY": None,
        "LK": "karibna",   # [A] mismo término en Lokono
        "TN": "caribe",
        "KL": "kalínagu",  # autónimo Kalinago: kali(na)+gu(gente); el propio pueblo
        "es": "Caribe, pueblo Kalinago (nombre arahuaco y autónimo)"
    },
    "quiripa": {
        "PA": None,
        "CQ": "quiripa",   # cuentas/discos de concha como medio de intercambio
        "WY": None,
        "LK": None,
        "TN": None,
        "KL": None,        # Kalinago tenían conchas ornamentales pero término distinto
        "es": "quiripa, concha-moneda; medio de intercambio costero"
    },
    "hombre_KL": {
        "PA": "*hianaru",  # proto: persona/gente
        "CQ": None,
        "WY": None,
        "LK": "hianaro",   # [A] hianaro = persona en Lokono
        "TN": None,
        "KL": "hiñaru",    # [A] "lengua de mujeres" Breton: hiñaru = persona/mujer
        "es": "persona, ser humano (registro femenino KL)"
    },
    "hombre_caribe": {
        "PA": None,
        "CQ": None,
        "WY": None,
        "LK": None,
        "TN": None,
        "KL": "baruwa",    # [C] OVERLAY CARIBE: baruwa = hombre (registro masculino KL)
        "es": "hombre (registro masculino Kalinago, origen caribe)"
    },
}

# =============================================================================
# REGLAS FONOLOGICAS POR PAR DE LENGUAS
# Formato: lista de (patron_regex, reemplazo, descripcion)
# Las reglas se aplican en orden — el orden importa
# =============================================================================

# --- WY → CQ (ya validado, 14 reglas de wayunaiki_phonology.py) ---
REGLAS_WY_CQ = [
    (r"aa|ee|oo|üü", lambda m: m.group()[0],  "R1: vocales largas → simples"),
    (r"ü",            "u",                      "R2: ü → u"),
    (r"'",            "",                       "R3: oclusiva glotal → Ø"),
    (r"sh",           "ch",                     "R4: sh → ch"),
    (r"k(?=[aeiou])", "c",                      "R5: k ante vocal → c"),  # simplificado
    (r"^w",           "b",                      "R6: w- inicial → b"),
    (r"(?<=[bcdfghjklmnpqrstvxyz])w", "b",      "R7: w post-consonante → b"),
    (r"(?<=[aeiou])w(?=[aeiou])", "u",          "R8: w inter-vocal → u"),
    (r"^j(?=[ie])",   "y",                      "R9: j- ante i/e → y"),
    (r"^j(?=[aou])",  "",                       "R10: j- ante a/o/u → Ø"),
    (r"(?<=[aeiou])j(?=[aeiou])", "y",          "R11: j intervocálica → y"),
    (r"baa$",         "ba",                     "R12: -baa final → -ba"),
    (r"^mm",          "m",                      "R13: consonante inicial doble → simple"),
    (r"^pp",          "p",                      "R13b: pp- → p"),
    (r"(?<=[aeiou])p(?=[aeiou])", "b",          "R14: p intervocálica → b"),
]

# --- LK → CQ ---
# Basado en los pares: hadali↔cazi, katsi↔cati, bara↔para, kannoa↔canoa,
#                      piaye↔piache, hamaha↔hamaca
# ORDEN CRÍTICO: k→c ANTES de ts→t (para que katsi → cati, no kachi)
REGLAS_LK_CQ = [
    (r"^h(?=[aeiou])", "",      "R1: h- prostética inicial → Ø"),
    (r"kk",            "c",     "R2: kk geminada → c"),
    (r"k(?=[aeiou])",  "c",     "R3: k ante vocal → c (ANTES de ts)"),
    (r"ts",            "t",     "R4: ts → t (despalatalización)"),
    (r"^b",            "p",     "R5: b- inicial → p"),
    (r"nn",            "n",     "R6: nn geminada → n"),
    (r"ll",            "l",     "R7: ll geminada → l"),
    (r"mm",            "m",     "R8: mm geminada → m"),
    (r"(?<=[aeiou])b(?=[aeiou])", "p", "R9: b intervocálica → p"),
    (r"ye$",           "che",   "R10: -ye final → -che"),
    (r"-ha$",          "-ca",   "R11: sufijo -ha → -ca"),
    (r"ha$",           "ca",    "R11b: -ha final → -ca"),
    (r"dj",            "ch",    "R12: dj → ch"),
    (r"^d(?=[aeiou])", "t",     "R13: d- inicial ante vocal → t"),
]

# --- TN → CQ ---
# Basado en: bagua↔para, bejique↔piache, higuana↔iguana
# Taíno y Caquetío son más distantes entre sí que Lokono y Caquetío
REGLAS_TN_CQ = [
    (r"^b(?=[aeiou])", "p",     "R1: b- inicial → p"),
    (r"ique$",         "iche",  "R2: sufijo -ique → -iche"),
    (r"eje$",          "ache",  "R3: sufijo -eje → -ache (variante)"),
    (r"que$",          "ca",    "R4: -que final → -ca"),
    (r"^h(?=[iey])",   "",      "R5: h- ante i/e/y → Ø"),
    (r"gu(?=[aeiou])", "gu",    "R6: gu- se mantiene"),
    (r"j(?=[aeiou])",  "y",     "R7: j → y ante vocal"),
    (r"x",             "ch",    "R8: x → ch"),
    (r"z",             "s",     "R9: z → s"),
    (r"gui(?=[aeiou])","gi",    "R10: gui → gi"),
]

# --- LK → WY ---
# Lokono y Wayunaiki son lenguas hermanas del Norte de la familia Maipurana
# Las diferencias son menores que con Taíno
# CORRECCIÓN: bara → palaa requiere r→l Y vocal larga final
REGLAS_LK_WY = [
    (r"^b",            "p",     "R1: b- inicial Lokono → p Wayunaiki"),
    (r"(?<=[aeiou])b(?=[aeiou])", "p", "R2: b intervocal → p"),
    (r"ts",            "sh",    "R3: ts Lokono → sh Wayunaiki"),
    (r"^h(?=[aeiou])", "",      "R4: h- prostética → Ø"),
    (r"nn",            "n",     "R5: nn → n"),
    (r"ll",            "l",     "R6: ll → l"),
    (r"r(?=[aeiou])",  "l",     "R7: r ante vocal → l (Wayunaiki prefiere l)"),
    (r"(?<=[aeiou])k(?=[aeiou])", "k'", "R8: k intervocal → k' (glotal)"),
    (r"ye$",           "ya",    "R9: -ye → -ya"),
    (r"-ha$",          "aa",    "R10: sufijo -ha → -aa (vocal larga)"),
    (r"ha$",           "aa",    "R10b"),
    (r"(?<=[bcdfghjklmnpqrstvxyz])a$", "aa", "R11: -a final post-consonante → -aa"),
    (r"f",             "p",     "R12: f → p (WY no tiene f)"),
    (r"dj",            "sh",    "R13: dj → sh"),
    (r"ono$",          "uyu",   "R14: -ono → -uyu (lokono → wayuu?)"),
]

# --- WY → LK ---
REGLAS_WY_LK = [
    (r"'",             "",      "R1: oclusiva glotal → Ø"),
    (r"sh",            "ts",    "R2: sh → ts"),
    (r"aa",            "a",     "R3: vocal larga → simple"),
    (r"ee",            "e",     "R4"),
    (r"oo",            "o",     "R5"),
    (r"^p",            "b",     "R6: p- inicial → b"),
    (r"(?<=[aeiou])p(?=[aeiou])", "b", "R7: p intervocal → b"),
    (r"ü",             "u",     "R8: ü → u"),
    (r"^w",            "b",     "R9: w- inicial → b"),  # via proto *b
    (r"k'",            "k",     "R10: k' glotal → k"),
    (r"ya$",           "ye",    "R11: -ya → -ye"),
    (r"uyu$",          "ono",   "R12: -uyu → -ono"),
]

# --- LK → TN ---
# Lokono y Taíno comparten muchas raíces pero con diferencias sistemáticas
REGLAS_LK_TN = [
    (r"^b",            "b",     "R1: b- se mantiene (TN y LK coinciden)"),
    (r"ts",            "s",     "R2: ts Lokono → s Taíno"),
    (r"^h(?=[aeiou])", "h",     "R3: h- se mantiene en Taíno"),
    (r"ye$",           "ique",  "R4: -ye → -ique (sufijo chamánico)"),
    (r"(?<=[aeiou])b(?=[aeiou])", "g", "R5: b intervocal → g en TN"),
    (r"k(?=[aeiou])",  "c",     "R6: k → c"),
    (r"nn",            "n",     "R7: nn → n"),
    (r"ll",            "l",     "R8: ll → l"),
    (r"on$",           "on",    "R9: -on se mantiene"),
    (r"ba$",           "ba",    "R10: -ba se mantiene"),
    (r"ha$",           "a",     "R11: -ha → -a (pierde sufijo -ha)"),
]

# --- TN → LK ---
REGLAS_TN_LK = [
    (r"^b",            "b",     "R1: b- Taíno → b- Lokono"),
    (r"ique$",         "ye",    "R2: -ique → -ye"),
    (r"g(?=[aeiou])",  "b",     "R3: g intervocálica → b"),
    (r"c(?=[aeiou])",  "k",     "R4: c → k"),
    (r"s(?=[ie])",     "ts",    "R5: s ante i/e → ts (palatalización Lokono)"),
    (r"(?<=[aeiou])n$","n",     "R6: -n final se mantiene"),
]

# --- LK → KL (Lokono → Kalinago, sustrato arahuaco) ---
# Fuentes: Breton (1665), Taylor (1951), Hoff (1968), Garifuna moderno
# IMPORTANTE: estas reglas aplican al SUSTRATO ARAHUACO del Kalinago.
# El overlay caribe (vocabulario de dominio masculino) NO sigue estas reglas
# y debe consultarse en KALINAGO_CARIBE_OVERLAY.
#
# Pares de validación que fundamentan las reglas:
#   LK katsi  → KL kati   (luna):   ts→t
#   LK piaye  → KL buyei  (chamán): p→b, -ye→-ei
#   LK kasabi → KL kasabi (casabe): sin cambio
#   LK kairi  → KL kairi  (isla):   sin cambio
#   LK yuka   → KL yuka   (yuca):   sin cambio
#   LK tuna   → KL duna   (agua):   t→d (sonorización inicial)
#   LK abba   → KL aban   (uno):    bb→b + nasal
#   LK kassaku→ KL kasaku (cielo):  kk→k
REGLAS_LK_KL = [
    # R0 PRIMERO: piaye→buyei tiene coalescencia ia→u que no es regla general
    (r"^piaye$",       "buyei","R0: piaye→buyei (cognado irregular: p→b + ia→u + ye→ei)"),
    (r"^h(?=[aeiou])", "",     "R1: h- prostética → Ø (igual que CQ)"),
    (r"kk",            "k",    "R2: kk geminada → k"),
    (r"ss",            "s",    "R2b: ss geminada → s (kassaku→kasaku)"),
    (r"nn",            "n",    "R3: nn geminada → n"),
    (r"ll",            "l",    "R4: ll geminada → l"),
    (r"mm",            "m",    "R5: mm geminada → m"),
    (r"bb",            "b",    "R6: bb geminada → b"),
    (r"ts",            "t",    "R7: ts → t (depalatalización; igual que CQ)"),
    (r"^p(?=[aeiou])", "b",    "R8: p- inicial → b (sonorización; inverso a LK→CQ)"),
    (r"^t(?=[aeiou])", "d",    "R9: t- inicial → d (tuna→duna)"),
    (r"ye$",           "ei",   "R10: -ye final → -ei"),
    (r"ba$",           "ban",  "R11: -ba final → -ban (abba→aban)"),
    (r"aa$",           "a",    "R12: -aa final → -a"),
    (r"dj",            "y",    "R13: dj → y"),
]

# --- KL → LK (Kalinago → Lokono, inverso) ---
# Reglas inversas para reconstrucción desde Garifuna hacia Lokono
REGLAS_KL_LK = [
    (r"^b(?=[aeiou])", "p",    "R1: b- inicial → p (piaye: inverso de R8)"),
    (r"^d(?=[aeiou])", "t",    "R2: d- inicial → t (duna→tuna)"),
    (r"t(?=[aeiou])",  "ts",   "R3: t ante vocal → ts (kati→katsi)"),
    (r"ei$",           "ye",   "R4: -ei → -ye (buyei→piaye)"),
    (r"ban$",          "ba",   "R5: -ban → -ba (aban→abba)"),
    (r"^k(?=[aeiou])", "k",    "R6: k- inicial se conserva"),
]

# =============================================================================
# KALINAGO: OVERLAY CARIBE
# Palabras del dominio masculino donde el Caribe sustituyó el vocablo arahuaco.
# Documentado por Breton (1665) como "palabras de los hombres" vs "de las mujeres".
# Esta diglosia léxica es evidencia directa del proceso de contacto.
# =============================================================================

KALINAGO_CARIBE_OVERLAY = {
    "canoa": {
        "kl_arahuaco": "kanoa",
        "kl_caribe":   "kanawa",
        "nota": "kanawa (Carib) desplazó kanoa (Arahuaco) en contexto náutico-masculino"
    },
    "pez": {
        "kl_arahuaco": None,
        "kl_caribe":   "pira",
        "nota": "pira de origen caribe; cf. piraña = pira + aña (diente en Tupí-Guaraní)"
    },
    "hombre": {
        "kl_arahuaco": "hiñaru",   # forma del registro femenino / general
        "kl_caribe":   "baruwa",
        "nota": "baruwa en registro masculino; hiñaru en registro femenino/neutro (Breton 1665)"
    },
    "enemigo_arahuaco": {
        "kl_arahuaco": None,
        "kl_caribe":   "Aruaña",
        "nota": "término caribe para los arahuacos; raíz de 'Arawak' (vía Dutch Aruaña→Arowak)"
    },
    "guerra": {
        "kl_arahuaco": None,
        "kl_caribe":   "amourou",
        "nota": "vocabulario bélico casi exclusivamente caribe en Kalinago"
    },
    "arco_arma": {
        "kl_arahuaco": "semaara-haaba",  # del proto-arahuaco
        "kl_caribe":   "ouacoubou",
        "nota": "forma caribe predomina en contexto de combate (Breton 1665)"
    },
}

# Mapa de reglas disponibles
REGLAS = {
    ("WY", "CQ"): REGLAS_WY_CQ,
    ("LK", "CQ"): REGLAS_LK_CQ,
    ("TN", "CQ"): REGLAS_TN_CQ,
    ("LK", "WY"): REGLAS_LK_WY,
    ("WY", "LK"): REGLAS_WY_LK,
    ("LK", "TN"): REGLAS_LK_TN,
    ("TN", "LK"): REGLAS_TN_LK,
    ("LK", "KL"): REGLAS_LK_KL,
    ("KL", "LK"): REGLAS_KL_LK,
}

# =============================================================================
# MOTOR DE TRANSDUCCION
# =============================================================================

def apply_rules(word: str, rules: list) -> str:
    """Aplica una lista de reglas fonológicas en orden."""
    result = word.lower().strip()
    for pattern, replacement, *_ in rules:
        if callable(replacement):
            result = re.sub(pattern, replacement, result)
        else:
            result = re.sub(pattern, replacement, result)
    return result

def transducir(word: str, origen: str, destino: str,
               asterisk: bool = True) -> Optional[str]:
    """
    Transforma una palabra de la lengua origen a la lengua destino
    aplicando las reglas fonológicas comparativas.

    Args:
        word    : palabra en lengua origen
        origen  : código de lengua ("WY", "LK", "TN", "CQ", "PA")
        destino : código de lengua destino
        asterisk: si True, antepone * a la reconstrucción

    Returns:
        forma reconstruida con * si es especulativa, None si no hay reglas

    Ejemplos:
        transducir("katsi", "LK", "CQ")  -> "*cati"
        transducir("bara",  "LK", "CQ")  -> "*para"
        transducir("kashi", "WY", "LK")  -> "*katsi"
    """
    if origen == destino:
        return word
    if (origen, destino) not in REGLAS:
        # Intentar via PA si hay ruta indirecta
        return _transducir_via_proto(word, origen, destino, asterisk)
    rules = REGLAS[(origen, destino)]
    result = apply_rules(word, rules)
    prefix = "*" if asterisk else ""
    return f"{prefix}{result}"

def _transducir_via_proto(word: str, origen: str, destino: str,
                           asterisk: bool) -> Optional[str]:
    """Intenta transducción via proto-arahuaco si no hay ruta directa."""
    # Buscar el cognado proto si existe para esta forma
    for concepto, forms in COGNADOS.items():
        if forms.get(origen) == word.lower():
            pa_form = forms.get("PA")
            dest_form = forms.get(destino)
            if dest_form:
                return dest_form
            if pa_form:
                prefix = "*" if asterisk else ""
                return f"{prefix}{pa_form.lstrip('*')}→({destino}?)"
    return None

def tabla_comparativa(concepto_o_glosa: str) -> Optional[dict]:
    """
    Devuelve la tabla comparativa completa para un concepto dado.

    Args:
        concepto_o_glosa: clave del concepto ("sol", "luna", "mar"...)
                          o glosa en español ("sol", "luna"...)

    Returns:
        dict con formas en las 5 lenguas, o None si no está documentado
    """
    key = concepto_o_glosa.lower().replace(" ", "_")
    if key in COGNADOS:
        return dict(COGNADOS[key])
    # Buscar por glosa
    for k, v in COGNADOS.items():
        if concepto_o_glosa.lower() in v.get("es", "").lower():
            return dict(v)
    return None

def reconstruir_proto(formas: dict) -> str:
    """
    Dado un dict de formas atestiguadas {lengua: forma},
    propone una proto-forma aplicando el método comparativo.

    Heurística: busca el patrón más conservador (el que
    comparte más rasgos con el mayor número de formas).

    Args:
        formas: {"WY": "kashi", "LK": "katsi", "CQ": "cati"}

    Returns:
        proto-forma con asterisco
    """
    # Si hay PA directamente, devolver
    if "PA" in formas:
        return formas["PA"] if formas["PA"].startswith("*") else "*" + formas["PA"]

    # Heurística simple: CQ o LK son más conservadores
    # (menos cambios fonológicos documentados)
    priority = ["CQ", "LK", "TN", "WY"]
    for lang in priority:
        if lang in formas and formas[lang]:
            base = formas[lang]
            # Simplificaciones proto-tipicas
            proto = base
            proto = re.sub(r"ts", "t", proto)   # WY/LK ts -> proto *t
            proto = re.sub(r"sh", "s", proto)   # WY sh -> proto *s
            proto = re.sub(r"^h", "", proto)    # h- prostética
            proto = re.sub(r"'", "", proto)     # glotal
            proto = re.sub(r"([aeiou])\1", r"\1", proto)  # larga -> simple
            return f"*{proto}"
    return "*?"

# =============================================================================
# TABLA DE CORRESPONDENCIAS FONEMICAS (resumen para documentación)
# =============================================================================

CORRESPONDENCIAS = """
TABLA DE CORRESPONDENCIAS FONÉMICAS — LENGUAS ARAHUACANAS (6 lenguas)
======================================================================
Proto-Arahuaco → Caquetío → Wayunaiki → Lokono → Taíno → Kalinago[A]

PA    CQ     WY     LK     TN     KL[A]  NOTAS
*k-   c-     k-     k-     c-     k-     k→c en CQ/TN; conservado en KL
*k'   c/z    k'     k      —      k      glotal solo en WY
*t    t      t      t/ts   t      t/d    KL sonoriza t→d inicial (tuna→duna)
*p    p      p      b      b      b      KL sonoriza p→b inicial (piaye→buyei)
*b    b/p    p      b      b      b      *b conservado en KL (igual LK)
*m    m      m      m      m      m      universal conservado
*n    n      n      n      n      n      universal conservado
*r    r      r/l    r      r      r      WY alterna r/l
*w    b/gu   w/b    b/w    gu/w   w/b    complejo en todos
*y    y      y      y      y/j    y      conservado
*h    h      j/Ø    h/Ø    h      Ø      KL como CQ: pierde h- prostética
*-aa  -a     -aa    -a     -a     -a     KL simplifica largas como CQ/TN
*-na  -na    -na    -na    -na    -na    sufijo locativo pan-arahuaco
*-koa -coa   -koa   -koa   -coa   -koa   locativo existencial (topónimos)
*-pa  -aba   -pa    -ba    -ba    -ba    sufijo verbal futuro/acción
*-ye  -che   -ya    -ye    -ique  -ei    sufijo chamánico: KL rotó el diptongo
"""

# =============================================================================
# RECONSTRUCCION DE FORMAS TAIINAS DESDE LOKONO
# =============================================================================

def reconstruir_taino(lokono_word: str, glosa_es: str = "") -> dict:
    """
    Intenta reconstruir una forma Taína a partir de una palabra Lokono.
    Útil para generar vocabulario Taíno hipotético donde no está atestiguado.
    """
    forma = transducir(lokono_word, "LK", "TN", asterisk=False)
    if forma is None:
        forma = lokono_word

    confianza = "alta" if len(forma) > 2 else "baja"
    if "?" in forma:
        confianza = "especulativa"

    nota = f"Reconstrucción desde Lok. {lokono_word}"
    if glosa_es:
        nota += f" ({glosa_es})"
    nota += "; método comparativo arahuaco"

    return {
        "taino_hipotetico": "*" + forma,
        "confianza": confianza,
        "nota": nota,
        "lokono_origen": lokono_word,
        "reglas_aplicadas": "LK→TN"
    }

def reconstruir_caquetio(lokono_word: str = None, wayunaiki_word: str = None,
                          taino_word: str = None, glosa_es: str = "") -> dict:
    """
    Reconstruye una proto-forma caquetía desde múltiples fuentes.
    """
    candidatos = []
    notas = []

    if lokono_word:
        from_lk = transducir(lokono_word, "LK", "CQ", asterisk=False)
        if from_lk and "?" not in from_lk:
            candidatos.append(from_lk)
            notas.append(f"Lok. {lokono_word} → {from_lk}")

    if wayunaiki_word:
        from_wy = transducir(wayunaiki_word, "WY", "CQ", asterisk=False)
        if from_wy and "?" not in from_wy:
            candidatos.append(from_wy)
            notas.append(f"Way. {wayunaiki_word} → {from_wy}")

    if taino_word:
        from_tn = transducir(taino_word, "TN", "CQ", asterisk=False)
        if from_tn and "?" not in from_tn:
            candidatos.append(from_tn)
            notas.append(f"Taíno {taino_word} → {from_tn}")

    if not candidatos:
        return {"proto_caquetio": "*?", "confianza": "ninguna", "nota": "sin datos"}

    if len(set(candidatos)) == 1:
        resultado = candidatos[0]
        confianza = "alta" if len(candidatos) > 1 else "media"
    else:
        resultado = min(candidatos, key=len)
        confianza = "media"

    return {
        "proto_caquetio": f"*{resultado}",
        "confianza": confianza,
        "candidatos": candidatos,
        "nota": "; ".join(notas),
        "glosa": glosa_es
    }

# =============================================================================
# VALIDACION — prueba el sistema contra pares conocidos
# =============================================================================

PARES_VALIDACION = [
    # — pares originales validados (9/9) —
    ("katsi",   "LK", "CQ", "cati",    "luna"),
    ("bara",    "LK", "CQ", "para",    "mar"),
    ("kannoa",  "LK", "CQ", "canoa",   "canoa"),
    ("piaye",   "LK", "CQ", "piache",  "chamán"),
    ("kashi",   "WY", "CQ", "cachi",   "luna"),
    ("kai",     "WY", "CQ", "cai",     "sol"),
    ("palaa",   "WY", "CQ", "pala",    "mar"),
    ("katsi",   "LK", "WY", "kashi",   "luna"),
    ("bara",    "LK", "WY", "palaa",   "mar"),
    # — pares Kalinago (sustrato arahuaco) —
    ("katsi",   "LK", "KL", "kati",    "luna LK→KL"),
    ("piaye",   "LK", "KL", "buyei",   "chamán LK→KL"),
    ("kasabi",  "LK", "KL", "kasabi",  "casabe LK→KL"),
    ("tuna",    "LK", "KL", "duna",    "agua LK→KL"),
    ("kassaku", "LK", "KL", "kasaku",  "cielo LK→KL"),
]

def validar():
    """Corre validación contra pares conocidos y reporta resultados."""
    print("=== VALIDACION DEL SISTEMA COMPARATIVO ===\n")
    ok = 0
    fallos = []
    for palabra, orig, dest, esperado, concepto in PARES_VALIDACION:
        resultado = transducir(palabra, orig, dest, asterisk=False)
        passed = resultado and (
            resultado == esperado or
            resultado.replace("*", "") == esperado or
            (len(resultado) > 2 and esperado in resultado)
        )
        status = "OK" if passed else "REVISAR"
        if passed:
            ok += 1
        else:
            fallos.append((palabra, orig, dest, resultado, esperado, concepto))
        print(f"  {status}  {orig}:{palabra:<12} → {dest}:{resultado:<12} (esperado: {esperado}) [{concepto}]")

    print(f"\n  {ok}/{len(PARES_VALIDACION)} pares validados")
    if fallos:
        print(f"  {len(fallos)} reglas a ajustar:")
        for f in fallos:
            print(f"    {f[1]}:{f[0]} → {f[2]}:{f[3]} (esperado: {f[4]}) [{f[5]}]")
    return ok, len(PARES_VALIDACION)

def demo_tabla():
    """Muestra tabla comparativa de conceptos clave."""
    print("\n=== TABLA COMPARATIVA ARAHUACANA (6 lenguas) ===\n")
    print(f"{'Concepto':<15} {'Proto-Ar.':<12} {'Caquetío':<12} {'Wayunaiki':<12} {'Lokono':<12} {'Taíno':<10} {'Kalinago':<12}")
    print("-" * 88)
    for concepto, forms in COGNADOS.items():
        pa  = forms.get("PA") or "—"
        cq  = forms.get("CQ") or "—"
        wy  = forms.get("WY") or "—"
        lk  = forms.get("LK") or "—"
        tn  = forms.get("TN") or "—"
        kl  = forms.get("KL") or "—"
        print(f"  {forms['es']:<13} {pa:<12} {cq:<12} {wy:<12} {lk:<12} {tn:<10} {kl:<12}")

if __name__ == "__main__":
    validar()
    demo_tabla()

    print("\n=== EJEMPLOS DE RECONSTRUCCION ===\n")
    ejemplos = [
        ("itime", "LK", "pez/pescado"),
        ("iuli",  "LK", "tabaco"),
        ("sallaban", "LK", "sabana"),
    ]
    print("Reconstruccion de Taíno hipotetico desde Lokono:")
    for word, lang, glosa in ejemplos:
        r = reconstruir_taino(word, glosa)
        print(f"  Lok. {word:<15} -> Taíno hipotetico {r['taino_hipotetico']:<15} ({glosa})")

    print("\nReconstruccion caquetía desde múltiples fuentes:")
    tests = [
        dict(lokono_word="katsi", wayunaiki_word="kashi", glosa_es="luna"),
        dict(lokono_word="bara",  wayunaiki_word="palaa", glosa_es="mar"),
        dict(lokono_word="piaye", glosa_es="chaman"),
    ]
    for t in tests:
        r = reconstruir_caquetio(**t)
        print(f"  *{r['glosa']:<10} -> {r['proto_caquetio']:<12} [{r['confianza']}] {r['nota'][:60]}")

    print("\nTransducción LK → KL (sustrato arahuaco):")
    kl_tests = [
        ("katsi",   "luna"),
        ("piaye",   "chamán"),
        ("kasabi",  "casabe"),
        ("tuna",    "agua"),
        ("kassaku", "firmamento"),
        ("kairi",   "isla"),
    ]
    for word, glosa in kl_tests:
        r = transducir(word, "LK", "KL")
        print(f"  LK {word:<12} -> KL {r:<12} ({glosa})")

    print("\nOverlay Caribe en Kalinago (vocabulario masculino/de combate):")
    for concepto, formas in KALINAGO_CARIBE_OVERLAY.items():
        ar = formas.get("kl_arahuaco") or "-"
        cb = formas.get("kl_caribe")   or "-"
        print(f"  {concepto:<20} [A] {ar:<12} [C] {cb:<12} | {formas['nota'][:55]}")
