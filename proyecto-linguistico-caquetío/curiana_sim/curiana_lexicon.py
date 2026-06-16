"""
CURIANA — Motor Léxico y Morfológico
=====================================
Motor de reglas morfológicas arahuacanas para la simulación de
emergencia lingüística en la comunidad caquetía de Curiana.

Basado en:
  - Vocabulario caquetío atestiguado (Zavala Reyes 2015, Jahn 1927, Alvarado 1921)
  - Morfología Wayunaiki (Álvarez 2017; Goulet & Jusayú 1978; Mansen & Mansen 1984)
  - Cognados arahuacanos: Lokono, Taíno, Garifuna
  - Topónimos venezolanos como evidencia morfológica

Principio central:
  Los agentes NO memorizan todas las palabras. Internalizan REGLAS y
  las aplican productivamente para generar formas nuevas cuando
  encuentran un vacío léxico. Así funciona el lenguaje natural.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# I. VOCABULARIO BASE
# ══════════════════════════════════════════════════════════════════════

VOCABULARIO_BASE: dict[str, dict] = {

    # ── Caquetío atestiguado (fuentes coloniales y arqueológicas) ──────
    "barsure":    {"sig": "alma, esencia vital, fuerza interior",          "cat": "sust",  "fuente": "caquetío"},
    "buco":       {"sig": "represa, presa de agua, reservorio",             "cat": "sust",  "fuente": "caquetío"},
    "biro":       {"sig": "sal",                                            "cat": "sust",  "fuente": "caquetío"},
    "chiriguare": {"sig": "gavilán, ave rapaz grande",                      "cat": "sust",  "fuente": "caquetío"},
    "maure":      {"sig": "fibra de algodón, hilo para tejer",              "cat": "sust",  "fuente": "caquetío"},
    "urari":      {"sig": "veneno/medicina vegetal (curare)",               "cat": "sust",  "fuente": "caquetío"},
    "corie":      {"sig": "choza, habitación, espacio propio",              "cat": "sust",  "fuente": "caquetío"},
    "saruro":     {"sig": "árbol saruro (frutos pequeños)",                 "cat": "sust",  "fuente": "caquetío"},
    "tuqueque":   {"sig": "lagartija pequeña, gecko",                       "cat": "sust",  "fuente": "caquetío"},
    "coro":       {"sig": "cardón grande, cactus columnar",                 "cat": "sust",  "fuente": "caquetío/topónimo"},
    "piache":     {"sig": "chamán, curandero, intermediario espiritual",    "cat": "sust",  "fuente": "caquetío"},
    "caraota":    {"sig": "frijol negro, legumbre",                         "cat": "sust",  "fuente": "caquetío"},
    "pauji":      {"sig": "pavo de monte, ave grande",                      "cat": "sust",  "fuente": "caquetío"},
    "manaure":    {"sig": "título laudatorio del señor principal",          "cat": "título","fuente": "caquetío"},
    "curiana":    {"sig": "territorio de los caquetíos / lugar del cardón", "cat": "topón", "fuente": "caquetío"},

    # ── Arahuacano compartido (cognados en Wayunaiki, Lokono, Taíno) ──
    "wayuu":      {"sig": "persona, gente, ser humano",                     "cat": "sust",  "fuente": "wayunaiki"},
    "anüiki":     {"sig": "habla, palabra, lengua",                         "cat": "sust",  "fuente": "wayunaiki"},
    "anasa":      {"sig": "bueno, bien, bello (< anasü Wayunaiki)",         "cat": "adj",   "fuente": "wayunaiki-cogn"},
    "taya":       {"sig": "yo (1ra persona singular)",                      "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "waya":       {"sig": "nosotros (1ra persona plural)",                  "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "pia":        {"sig": "tú (2da persona singular)",                      "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "nüma":       {"sig": "él/ella (pronombre 3ra persona)",                "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "naya":       {"sig": "ellos, ellas (3ra persona plural)",              "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "wanee":      {"sig": "uno (numeral)",                                  "cat": "num",   "fuente": "wayunaiki"},
    "piama":      {"sig": "dos (numeral)",                                  "cat": "num",   "fuente": "wayunaiki"},
    "apünüin":    {"sig": "tres (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "pienchi":    {"sig": "cuatro (numeral)",                               "cat": "num",   "fuente": "wayunaiki"},
    "jarai":      {"sig": "cinco (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},

    # ── Taíno (familia arahuacana, préstamos a todas las lenguas caribeñas) ──
    "hamaca":     {"sig": "red colgante para dormir",                       "cat": "sust",  "fuente": "taíno"},
    "canoa":      {"sig": "embarcación excavada en tronco",                 "cat": "sust",  "fuente": "taíno"},
    "cacique":    {"sig": "jefe, señor principal de la comunidad",          "cat": "sust",  "fuente": "taíno"},
    "maíz":       {"sig": "planta de maíz, grano principal",               "cat": "sust",  "fuente": "taíno"},
    "yuca":       {"sig": "tubérculo, mandioca amarga o dulce",             "cat": "sust",  "fuente": "arahuacano"},
    "batata":     {"sig": "camote, tubérculo dulce",                        "cat": "sust",  "fuente": "taíno"},
    "bohío":      {"sig": "casa comunal, choza redonda con techo cónico",   "cat": "sust",  "fuente": "taíno"},
    "conuco":     {"sig": "huerto familiar, parcela cultivada",             "cat": "sust",  "fuente": "taíno"},
    "iguana":     {"sig": "lagarto grande, iguana",                         "cat": "sust",  "fuente": "taíno/caribe"},

    # ── Raíces verbales arahuacanas (reconstruidas por comparación) ────
    "naa":        {"sig": "ir, moverse hacia",                              "cat": "v_raiz","fuente": "arahuacano"},
    "waa":        {"sig": "venir, aproximarse",                             "cat": "v_raiz","fuente": "arahuacano"},
    "kaa":        {"sig": "estar, existir, ser (cópula)",                   "cat": "v_raiz","fuente": "arahuacano"},
    "paa":        {"sig": "dar, ofrecer, transferir",                       "cat": "v_raiz","fuente": "arahuacano"},
    "maa":        {"sig": "decir, hablar, comunicar",                       "cat": "v_raiz","fuente": "arahuacano"},
    "taa":        {"sig": "tomar, coger, recibir",                          "cat": "v_raiz","fuente": "arahuacano"},
    "chaa":       {"sig": "hacer, construir, crear",                        "cat": "v_raiz","fuente": "arahuacano"},

    # ── Única frase Caquetía atestiguada ──────────────────────────────
    # "Chacamba cudanga" = ¿Cómo está usted? (saludo)
    # "Cudan de cuté"    = Para servirle a usted
    "chacamba":   {"sig": "¿cómo? (pregunta de estado)",                    "cat": "interr","fuente": "caquetío-atestiguado"},
    "cudanga":    {"sig": "usted, vos (2da persona formal)",                "cat": "pron",  "fuente": "caquetío-atestiguado"},
    "cudan":      {"sig": "servir, estar al servicio de",                   "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "cuté":       {"sig": "a usted, para usted (dativo formal)",            "cat": "pron",  "fuente": "caquetío-atestiguado"},

    # ── Verbos arahuacanos (cognados Lokono / Wayunaiki / Garifuna) ────
    "wana":       {"sig": "ver, observar, mirar",                           "cat": "v_raiz","fuente": "lokono/wayunaiki"},
    "suna":       {"sig": "dormir, reposar, descansar",                     "cat": "v_raiz","fuente": "lokono/proto-arawakan"},
    "masa":       {"sig": "comer, alimentarse",                             "cat": "v_raiz","fuente": "lokono/garifuna"},
    "awa":        {"sig": "beber, tomar líquido",                           "cat": "v_raiz","fuente": "proto-arawakan"},
    "kira":       {"sig": "escuchar, oír, atender",                         "cat": "v_raiz","fuente": "wayunaiki/lokono"},
    "pana":       {"sig": "saber, conocer, entender",                       "cat": "v_raiz","fuente": "lokono/garifuna"},
    "naba":       {"sig": "pensar, reflexionar, meditar",                   "cat": "v_raiz","fuente": "lokono/wayunaiki"},
    "kono":       {"sig": "sembrar, plantar, cultivar",                     "cat": "v_raiz","fuente": "lokono/taíno"},
    "raka":       {"sig": "querer, desear, necesitar",                      "cat": "v_raiz","fuente": "lokono/garifuna"},
    "rua":        {"sig": "cargar, transportar, llevar",                    "cat": "v_raiz","fuente": "proto-arawakan"},

    # ── Naturaleza (cognados arahuacanos) ─────────────────────────────
    "duna":       {"sig": "agua (corriente, bebible)",                      "cat": "sust",  "fuente": "garifuna/lokono"},
    "amana":      {"sig": "fuego, lumbre, brasa",                           "cat": "sust",  "fuente": "proto-arawakan"},
    "kali":       {"sig": "sol",                                            "cat": "sust",  "fuente": "lokono/garifuna"},
    "kasha":      {"sig": "luna",                                           "cat": "sust",  "fuente": "wayunaiki/lokono"},
    "kaya":       {"sig": "lluvia, agua del cielo",                         "cat": "sust",  "fuente": "lokono (juya-cogn)"},
    "kuru":       {"sig": "árbol, madera, tronco",                          "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "arima":      {"sig": "pez, pescado",                                   "cat": "sust",  "fuente": "lokono/garifuna"},
    "habo":       {"sig": "mar, océano, aguas grandes",                     "cat": "sust",  "fuente": "lokono/garifuna"},
    "dali":       {"sig": "tierra, suelo, polvo",                           "cat": "sust",  "fuente": "garifuna/proto-arawakan"},
    "suka":       {"sig": "noche, oscuridad",                               "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "bara":       {"sig": "río, corriente fluvial",                         "cat": "sust",  "fuente": "proto-arawakan/topónimo"},
    "sima":       {"sig": "cerro, montaña, elevación",                      "cat": "sust",  "fuente": "lokono/topónimo (Barquisimeto)"},

    # ── Personas y parentesco ──────────────────────────────────────────
    "ama":        {"sig": "madre, mujer que nutre y da origen",             "cat": "sust",  "fuente": "proto-arawakan universal"},
    "baba":       {"sig": "padre, hombre que protege",                      "cat": "sust",  "fuente": "lokono/garifuna"},
    "buri":       {"sig": "hijo, hija, criatura, descendiente",             "cat": "sust",  "fuente": "lokono/garifuna"},
    "nomi":       {"sig": "hombre adulto (no título)",                      "cat": "sust",  "fuente": "lokono/garifuna"},
    "wari":       {"sig": "mujer adulta (no título)",                       "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "wanü":       {"sig": "anciano, mayor, persona de saber acumulado",     "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "pütchi":     {"sig": "mensaje, palabra sagrada, voz del espíritu",     "cat": "sust",  "fuente": "wayunaiki"},

    # ── Cuerpo ──────────────────────────────────────────────────────────
    "kabo":       {"sig": "cabeza, mente, lo alto de",                      "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "nii":        {"sig": "ojo, mirada, visión",                            "cat": "sust",  "fuente": "lokono-cogn"},
    "bari":       {"sig": "vientre, barriga, interior del cuerpo",          "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "arua":       {"sig": "alimento, comida, sustento (raíz de 'arawak')",  "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "kapua":      {"sig": "amanecer, alba, primera luz del día",            "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "tüshi":      {"sig": "frío, temperatura baja",                         "cat": "adj",   "fuente": "wayunaiki-cogn"},

    # ── Partículas y conectores ────────────────────────────────────────
    # (permiten construir frases más complejas sin recurrir al español)
    "ka":         {"sig": "y, también, además, con (conector aditivo)",     "cat": "part",  "fuente": "proto-arawakan"},
    "mara":       {"sig": "pero, sin embargo, aunque (contraste)",          "cat": "part",  "fuente": "lokono/garifuna"},
    "saa":        {"sig": "si, cuando, al momento de (condicional/temp.)",  "cat": "part",  "fuente": "lokono"},
    "naka":       {"sig": "después, luego, más tarde (temporal posterior)", "cat": "part",  "fuente": "lokono"},
    "puna":       {"sig": "antes, ya, primero (temporal anterior)",         "cat": "part",  "fuente": "lokono"},
    "kashi":      {"sig": "ahora, en este momento (temporal presente)",     "cat": "part",  "fuente": "wayunaiki-cogn"},
    "wara":       {"sig": "muy, mucho, bastante (intensificador)",          "cat": "part",  "fuente": "lokono/garifuna"},
    "sulu":       {"sig": "adentro, dentro de, en el interior de",         "cat": "part",  "fuente": "wayunaiki"},
    "yama":       {"sig": "aquí, en este lugar (deíctico proximal)",        "cat": "part",  "fuente": "wayunaiki-cogn"},
    "kana-pa":    {"sig": "allá, en ese lugar lejano (deíctico distal)",    "cat": "part",  "fuente": "lokono"},

    # ── Colores (cognados Wayunaiki / Lokono / proto-arawakan) ─────────
    "mütsia":     {"sig": "negro, oscuro (< mütsiisü Wayunaiki)",            "cat": "adj",   "fuente": "wayunaiki-cogn"},
    "kasuta":     {"sig": "blanco, claro, luminoso (< kasüttaa Wayunaiki)", "cat": "adj",   "fuente": "wayunaiki-cogn"},
    "sünatü":     {"sig": "rojo, color de la sangre (< ishasü)",            "cat": "adj",   "fuente": "wayunaiki/lokono"},
    "tsipana":    {"sig": "verde, color de hoja fresca",                    "cat": "adj",   "fuente": "lokono/proto-arawakan"},
    "kanawa":     {"sig": "amarillo, color del oro y del maíz seco",        "cat": "adj",   "fuente": "lokono/garifuna"},

    # ── Números 6–10 (continúan la serie Wayunaiki) ────────────────────
    "aipirua":    {"sig": "seis (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "akaratsa":   {"sig": "siete (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},
    "meekisa":    {"sig": "ocho (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "mekietsa":   {"sig": "nueve (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},
    "polo":       {"sig": "diez (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},

    # ── Herramientas y objetos (cognados Lokono / proto-arawakan) ──────
    "buraka":     {"sig": "arco para cazar y pescar",                       "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "sipara":     {"sig": "flecha, dardo arrojadizo",                       "cat": "sust",  "fuente": "lokono/garifuna"},
    "atara":      {"sig": "red de pesca, malla tejida",                     "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "kanua":      {"sig": "canoa pequeña, balsa de un tronco",              "cat": "sust",  "fuente": "lokono-cogn"},
    "paugis":     {"sig": "vasija, totuma, recipiente de barro o calabaza", "cat": "sust",  "fuente": "lokono/garifuna"},
    "kürara":     {"sig": "cuerda, soga, fibra trenzada",                   "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "shukua":     {"sig": "remo, pala para impulsar la canoa",              "cat": "sust",  "fuente": "lokono/garifuna"},

    # ── Intercambio y comercio (raíces y cognados arahuacanos) ─────────
    "siwa":       {"sig": "sal de comercio (< proto-arawakan *siwa)",       "cat": "sust",  "fuente": "proto-arawakan/lokono"},
    "tüma":       {"sig": "perla, cuenta brillante del mar",                "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "karükera":   {"sig": "oro, metal amarillo (caona-cogn)",               "cat": "sust",  "fuente": "taíno/lokono"},
    "paratü":     {"sig": "trueque, intercambio de bienes (raíz paa-)",     "cat": "sust",  "fuente": "proto-arawakan"},
    "taneka":     {"sig": "deuda, lo que se debe devolver (raíz taa-)",     "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "puruna":     {"sig": "mercado, lugar de trueque y reunión",            "cat": "sust",  "fuente": "lokono/garifuna"},

    # ── Ritual y espiritual (cognados Wayunaiki / Lokono / Garifuna) ───
    "yorua":      {"sig": "espíritu, ánima, ente del más allá",             "cat": "sust",  "fuente": "lokono/garifuna"},
    "lapü":       {"sig": "sueño-visión, mensaje onírico (< lapü Wayuu)",   "cat": "sust",  "fuente": "wayunaiki"},
    "sakana":     {"sig": "ofrenda, dádiva ritual a los espíritus",         "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "outa":       {"sig": "muerte, fin de la vida (< outaa Wayunaiki)",     "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "kataa":      {"sig": "vida, aliento vital (< kataa Wayunaiki)",        "cat": "sust",  "fuente": "wayunaiki/lokono"},
    "wabarsure":  {"sig": "alma colectiva, espíritu del pueblo (wa+barsure)","cat": "sust", "fuente": "caquetío"},
    "mawari":     {"sig": "espíritu maligno, sombra del monte",             "cat": "sust",  "fuente": "lokono/proto-arawakan"},

    # ── Flora local (cognados arahuacanos y atestiguado) ───────────────
    "mankaba":    {"sig": "manglar, bosque de raíces en agua salobre",      "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "marawa":     {"sig": "palma, palmera de cogollo y fibra",              "cat": "sust",  "fuente": "lokono/garifuna"},
    "kasiripa":   {"sig": "yuca brava, mandioca para casabe",               "cat": "sust",  "fuente": "lokono/garifuna"},
    "marisi":     {"sig": "maíz en mazorca, grano de cosecha",              "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "yuri":       {"sig": "tabaco, hoja sagrada del piache",                "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "kukuisa":    {"sig": "cocuiza, agave de fibra para cuerda",            "cat": "sust",  "fuente": "caquetío/topónimo"},

    # ── Fauna (cognados arahuacanos) ───────────────────────────────────
    "hikoteya":   {"sig": "tortuga, galápago de agua y tierra",            "cat": "sust",  "fuente": "lokono/garifuna"},
    "kaiwa":      {"sig": "caimán, lagarto grande de río",                  "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "tokoko":     {"sig": "flamenco o ibis, ave roja de la laguna",        "cat": "sust",  "fuente": "lokono/garifuna"},
    "kanawari":   {"sig": "tiburón, gran pez del mar abierto",              "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "manatü":     {"sig": "manatí, vaca marina del golfete",               "cat": "sust",  "fuente": "taíno/lokono"},
    "ukura":      {"sig": "cangrejo, crustáceo del manglar",                "cat": "sust",  "fuente": "lokono/garifuna"},

    # ── Estado emocional (cognados Wayunaiki / Lokono / Garifuna) ──────
    "talata":     {"sig": "alegría, contento, gozo (< talataa Wayunaiki)",  "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "mülia":      {"sig": "miedo, temor, espanto",                          "cat": "sust",  "fuente": "wayunaiki/lokono"},
    "muusa":      {"sig": "tristeza, pena, aflicción del ánimo",            "cat": "sust",  "fuente": "lokono/garifuna"},
    "alaain":     {"sig": "amor, afecto, querer profundo (raíz raka-)",     "cat": "sust",  "fuente": "wayunaiki/lokono"},
    "jashichi":   {"sig": "rabia, ira, enojo (< jashichi Wayunaiki)",       "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "japü":       {"sig": "vergüenza, pudor, sonrojo",                      "cat": "sust",  "fuente": "wayunaiki/lokono"},

    # ── Tiempo y clima (cognados arahuacanos y derivados locales) ──────
    "joutai":     {"sig": "viento, corriente de aire (< joutai Wayunaiki)", "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "kayawara":   {"sig": "tormenta, lluvia con viento fuerte (kaya+wara)", "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "haborü":     {"sig": "marejada, oleaje grande del mar (habo+rü)",      "cat": "sust",  "fuente": "lokono/garifuna"},
    "madunaka":   {"sig": "sequía, tiempo sin agua (ma+duna)",              "cat": "sust",  "fuente": "proto-arawakan"},
    "habobrisa":  {"sig": "brisa del golfete, viento suave del mar",        "cat": "sust",  "fuente": "lokono/garifuna"},
    # (fin de entradas nuevas — expansión a 146 palabras)
}


# ══════════════════════════════════════════════════════════════════════
# II. REGLAS MORFOLÓGICAS
# ══════════════════════════════════════════════════════════════════════

REGLAS_ASPECTO: dict[str, dict] = {
    "-ka": {
        "nombre": "completivo",
        "desc": "Acción terminada, resultado alcanzado. Equivale al pretérito perfecto.",
        "uso": "VERBO_RAIZ + -ka  →  acción completada",
        "ejemplos": [
            "naa-ka = ya fui / ya se fue",
            "paa-ka = ya di / ya entregué",
            "pescado-ka = ya pescé (hispanismo con sufijo caquetío)",
        ],
        "wayunaiki": "Triad A (-shi/-sü/-shii) en contexto de pasado",
        "instruccion_agente": (
            "Para indicar que algo ya terminó, agrega -ka al final: "
            "'Llegado-ka Manaure' = Manaure ya llegó. "
            "'Chaa-ka wa-buco' = nuestra represa ya está construida."
        ),
    },
    "-ni": {
        "nombre": "continuativo / imperfectivo",
        "desc": "Acción en progreso ahora mismo. Proceso activo.",
        "uso": "VERBO_RAIZ + -ni  →  acción en curso",
        "ejemplos": [
            "naa-ni = estoy yendo / va yendo",
            "pescando-ni = estoy pescando ahora",
            "maa-ni = estoy hablando",
        ],
        "wayunaiki": "-iraa (imperfective suffix)",
        "instruccion_agente": (
            "Para describir lo que haces ahora mismo, agrega -ni: "
            "'Naa-ni taya orilla' = Voy hacia la orilla ahora. "
            "'Maa-ni Shaboro' = Shaboro está hablando."
        ),
    },
    "-da": {
        "nombre": "prospectivo / intencional",
        "desc": "Acción futura o intención firme. Lo que se planea hacer.",
        "uso": "VERBO_RAIZ + -da  →  intención / futuro",
        "ejemplos": [
            "naa-da = voy a ir / iré",
            "paa-da = daré / voy a dar",
            "cudan-da = serviré / tengo intención de servir",
        ],
        "wayunaiki": "-ee (desiderative) + triad C (future intentive)",
        "instruccion_agente": (
            "Para expresar lo que harás o planeas, agrega -da: "
            "'Naa-da taya salinar' = Iré al salinar. "
            "'Maa-da taya Manaure' = Le hablaré a Manaure."
        ),
    },
}

REGLAS_LOCATIVAS: dict[str, dict] = {
    "-ana": {
        "nombre": "topónimo / lugar habitado",
        "desc": "Lugar donde abunda X, territorio asociado a X. Produce topónimos.",
        "uso": "RAÍZ + -ana  →  nombre de lugar",
        "ejemplos": [
            "coro + ana = Curiana (lugar/territorio del cardón)",
            "buco + ana = lugar de la represa",
            "biro + ana = lugar de la sal, salinar",
        ],
        "evidencia": "Curiana (Zavala 2015), Barquisimeto (*Barqui+sima/ima), Paraguaná (*Para+gua+na)",
        "instruccion_agente": (
            "Si necesitas nombrar un lugar, usa la raíz del elemento característico + -ana: "
            "Si hay muchos manglares, ese lugar es 'manglar-ana'. "
            "Si es donde se guarda la sal, es 'biro-ana'."
        ),
    },
    "-gua": {
        "nombre": "región / área asociativa",
        "desc": "Zona más amplia asociada con X. Menos específico que -ana.",
        "uso": "RAÍZ + -gua  →  región, área amplia",
        "ejemplos": [
            "Coro + gua = Corogua (región de los cardones) → hoy: Coro",
            "Para + gua + na = Paraguaná",
            "Araya (región salina)",
        ],
        "evidencia": "Topónimos venezolanos de Falcón y Sucre",
        "instruccion_agente": (
            "Para referirte a una región entera, usa -gua: "
            "'maure-gua' = la tierra del algodón (región)."
        ),
    },
    "-bana": {
        "nombre": "orilla / lugar limítrofe",
        "desc": "Borde de, orilla de, donde termina X y empieza otro espacio.",
        "uso": "RAÍZ + -bana  →  orilla, límite, punto de transición",
        "ejemplos": [
            "Mara+kai + bana = Maracaibana → Maracaibo (orilla del clan/lago Marakai)",
            "manglar + bana = orilla del manglar",
        ],
        "evidencia": "Maracaibo < *Maracai+bana (Oliver 1989, Alvarado 1921)",
        "instruccion_agente": (
            "Para orillas y límites: 'Golfete-bana' = la orilla del Golfete. "
            "'Manglar-bana' = el borde del manglar."
        ),
    },
}

REGLAS_AGENTIVAS: dict[str, dict] = {
    "-ko": {
        "nombre": "agente masculino",
        "desc": "Hombre cuya identidad/trabajo está asociado a X.",
        "uso": "RAÍZ + -ko  →  nombre o apodo masculino",
        "ejemplos": [
            "biro + ko = Biro-ko (el salinero, el hombre de la sal)",
            "corie + ko = Corie-ko (el de la choza, guardián del espacio)",
            "buco + ko = Buco-ko (el de la represa)",
        ],
        "wayunaiki": "-shi (masculine singular marker, triad A)",
        "instruccion_agente": (
            "Si un hombre trabaja con algo o es conocido por algo, su nombre o apodo "
            "puede formarse con -ko: el pescador experto podría llamarse 'bagre-ko'."
        ),
    },
    "-sha": {
        "nombre": "agente femenino",
        "desc": "Mujer cuya identidad/trabajo está asociado a X.",
        "uso": "RAÍZ + -sha  →  nombre o apodo femenino",
        "ejemplos": [
            "nubiri + sha = Nubiri-sha (la de la noche, la visionaria)",
            "paugis + sha = Paugis-sha (la de la totuma/vasija)",
            "maure + sha = Maure-sha (la tejedora, la del algodón)",
        ],
        "wayunaiki": "-sü (feminine/inanimate marker, triad A)",
        "instruccion_agente": (
            "Una mujer puede recibir nombre o apodo con -sha: "
            "la mujer que cuida el buco puede llamarse 'buco-sha'."
        ),
    },
}

REGLAS_POSESIVAS: dict[str, dict] = {
    "ta-": {
        "nombre": "posesivo 1ra singular",
        "desc": "Mi, mío/mía. Del hablante.",
        "uso": "ta- + SUSTANTIVO  →  mi X",
        "ejemplos": [
            "ta + barsure = ta-barsure (mi alma)",
            "ta + corie = ta-corie (mi choza)",
            "ta + anüiki = ta-anüiki (mi habla, mi lengua)",
        ],
        "wayunaiki": "ta- (1ra persona singular posesivo, cognado directo)",
    },
    "wa-": {
        "nombre": "posesivo 1ra plural",
        "desc": "Nuestro/nuestra. De nosotros, del grupo.",
        "uso": "wa- + SUSTANTIVO  →  nuestro X",
        "ejemplos": [
            "wa + barsure = wa-barsure (nuestra alma colectiva)",
            "wa + buco = wa-buco (nuestra represa)",
            "wa + anüiki = wa-anüiki (nuestra lengua)",
        ],
        "wayunaiki": "wa- (1ra persona plural posesivo, cognado directo)",
    },
    "ma-": {
        "nombre": "negativo / privativo",
        "desc": "Sin X, no X, carente de X.",
        "uso": "ma- + SUSTANTIVO  →  sin X / no X",
        "ejemplos": [
            "ma + barsure = ma-barsure (sin alma, vacío espiritual)",
            "ma + biro = ma-biro (sin sal)",
            "ma + anüiki = ma-anüiki (sin habla, mudo, extranjero incomprensible)",
        ],
        "wayunaiki": "ma- (prefijo negativo, cognado directo)",
    },
    "ka-": {
        "nombre": "posesivo genérico / asociativo",
        "desc": "El/la que tiene X, poseído por, asociado con.",
        "uso": "ka- + SUSTANTIVO  →  el/la de X",
        "ejemplos": [
            "ka + maure = ka-maure (el del algodón, el tejedor)",
            "ka + biro = ka-biro (el de la sal)",
            "ka + barsure = ka-barsure (el del alma fuerte, el espiritual)",
        ],
        "wayunaiki": "ka- (prefijo posesivo no-pronominal)",
    },
}

REGLAS_NUMERO: dict[str, dict] = {
    "-kana": {
        "nombre": "plural colectivo",
        "desc": "Grupo de, el pueblo de, todos los X.",
        "uso": "SUSTANTIVO + -kana  →  plural / colectivo",
        "ejemplos": [
            "wayuu + kana = wayuukana (el pueblo wayuu, todos los wayuu)",
            "barsure + kana = las almas",
            "piache + kana = los piaches, el conjunto de chamanes",
        ],
        "wayunaiki": "-kana (sufijo plural, COGNADO DIRECTO con Caquetío)",
    },
    "-naiki": {
        "nombre": "lengua de / habla de",
        "desc": "La lengua, el idioma, la forma de hablar de un pueblo.",
        "uso": "GENTILICIO + -naiki  →  nombre de la lengua",
        "ejemplos": [
            "wayuu + naiki = wayuunaiki (la lengua wayuu)",
            "caquetío + naiki = caquetío-naiki (la lengua caquetía)",
        ],
        "wayunaiki": "anüiki = habla → -naiki es sufijo derivado",
    },
}

# ── Tabla maestra de reglas (para inyectar en prompts) ──────────────
TODAS_LAS_REGLAS = {
    **REGLAS_ASPECTO,
    **REGLAS_LOCATIVAS,
    **REGLAS_AGENTIVAS,
    **REGLAS_POSESIVAS,
    **REGLAS_NUMERO,
}


# ══════════════════════════════════════════════════════════════════════
# III. LÉXICO COMUNITARIO VIVO
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Neologismo:
    """Registro de una palabra nueva acuñada durante la simulación."""
    turno: int
    dia: int
    autor: str                         # nombre del agente que la acuñó
    forma: str                         # la nueva palabra
    componentes: str                   # ej: "coro + -ana"
    significado: str                   # propuesto por el agente
    contexto: str                      # frase donde apareció por primera vez
    regla_aplicada: str                # qué regla morfológica usó
    estado: str = "propuesto"          # propuesto | adoptado | rechazado | ignorado
    adoptado_por: list = field(default_factory=list)
    rechazado_por: list = field(default_factory=list)
    turno_resolucion: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)


class LexicoComunitario:
    """
    El léxico vivo de la comunidad. Crece turno a turno.

    Separado del VOCABULARIO_BASE porque este es el conocimiento
    heredado; el LexicoComunitario es lo que la generación actual
    está construyendo.
    """

    def __init__(self):
        self._lexico: dict[str, dict] = {}          # palabra → datos
        self._neologismos: list[Neologismo] = []     # historial ordenado

    # ── Consulta ──────────────────────────────────────────────────────

    def conoce(self, palabra: str) -> bool:
        """¿Existe esta palabra en el léxico base o comunitario?"""
        p = palabra.lower().strip()
        return p in VOCABULARIO_BASE or p in self._lexico

    def significado(self, palabra: str) -> Optional[str]:
        p = palabra.lower().strip()
        if p in VOCABULARIO_BASE:
            return VOCABULARIO_BASE[p]["sig"]
        if p in self._lexico:
            return self._lexico[p]["significado"]
        return None

    def palabras_activas(self) -> list[str]:
        """Todas las palabras disponibles (base + comunitario adoptado)."""
        base = list(VOCABULARIO_BASE.keys())
        adoptadas = [
            neo.forma for neo in self._neologismos
            if neo.estado == "adoptado"
        ]
        return base + adoptadas

    # ── Registro de neologismos ───────────────────────────────────────

    def registrar_neologismo(self, neo: Neologismo):
        self._neologismos.append(neo)
        if neo.estado == "adoptado":
            self._lexico[neo.forma] = {
                "significado": neo.significado,
                "autor": neo.autor,
                "dia": neo.dia,
            }

    def adoptar(self, forma: str, agente: str, turno: int):
        """Un agente adopta una palabra propuesta."""
        for neo in self._neologismos:
            if neo.forma == forma and neo.estado == "propuesto":
                if agente not in neo.adoptado_por:
                    neo.adoptado_por.append(agente)
                # Si 2+ agentes distintos la adoptaron → oficialmente adoptada
                if len(neo.adoptado_por) >= 2:
                    neo.estado = "adoptado"
                    neo.turno_resolucion = turno
                    self._lexico[forma] = {
                        "significado": neo.significado,
                        "autor": neo.autor,
                        "dia": neo.dia,
                    }
                break

    def rechazar(self, forma: str, agente: str, turno: int):
        """Un agente rechaza o ignora activamente una palabra propuesta."""
        for neo in self._neologismos:
            if neo.forma == forma and neo.estado == "propuesto":
                if agente not in neo.rechazado_por:
                    neo.rechazado_por.append(agente)
                if len(neo.rechazado_por) >= 3:
                    neo.estado = "rechazado"
                    neo.turno_resolucion = turno
                break

    # ── Reportes ──────────────────────────────────────────────────────

    def neologismos_pendientes(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "propuesto"]

    def neologismos_adoptados(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "adoptado"]

    def neologismos_rechazados(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "rechazado"]

    def reporte_linguistico(self) -> str:
        """Resumen del estado actual del léxico comunitario."""
        total_base = len(VOCABULARIO_BASE)
        adoptadas = self.neologismos_adoptados()
        pendientes = self.neologismos_pendientes()
        rechazadas = self.neologismos_rechazados()
        lines = [
            f"LÉXICO COMUNITARIO — Estado actual",
            f"  Vocabulario base (heredado): {total_base} palabras",
            f"  Neologismos adoptados:        {len(adoptadas)}",
            f"  En evaluación (propuestos):   {len(pendientes)}",
            f"  Rechazados/ignorados:         {len(rechazadas)}",
            f"  Total disponible:             {total_base + len(adoptadas)} palabras",
        ]
        if adoptadas:
            lines.append("\n  Palabras nuevas adoptadas:")
            for neo in adoptadas[-10:]:  # últimas 10
                lines.append(f"    [{neo.forma}] = {neo.significado}  (acuñó: {neo.autor}, día {neo.dia})")
        if pendientes:
            lines.append("\n  En evaluación:")
            for neo in pendientes[-5:]:
                adopc = len(neo.adoptado_por)
                lines.append(f"    [{neo.forma}] = {neo.significado}  ({adopc}/2 adopciones)")
        return "\n".join(lines)

    # ── Persistencia ──────────────────────────────────────────────────

    def save(self, path: str = "curiana_lexico.json"):
        data = {
            "lexico": self._lexico,
            "neologismos": [n.to_dict() for n in self._neologismos],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str = "curiana_lexico.json") -> "LexicoComunitario":
        lc = cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            lc._lexico = data.get("lexico", {})
            for nd in data.get("neologismos", []):
                neo = Neologismo(**nd)
                lc._neologismos.append(neo)
        except FileNotFoundError:
            pass
        return lc


# ══════════════════════════════════════════════════════════════════════
# IV. GENERADORES DE PROMPTS LINGÜÍSTICOS
# ══════════════════════════════════════════════════════════════════════

def prompt_reglas_breve() -> str:
    """
    Versión compacta para Tier II (~150 palabras).
    Framing como hablante nativo — español solo como glosa.
    """
    return """[LENGUA CAQUETÍA — Identidad y reglas]:
ERES hablante nativo de caquetío. Piensas en caquetío. El español es lengua extranjera.
CONSTRUYE tus frases con lo que tienes. Una frase incompleta en caquetío > oración completa en español.

ASPECTO: raíz + -ka (ya hice) / -ni (estoy haciendo) / -da (haré/quiero).
LUGAR: raíz + -ana (lugar de) / -bana (orilla de) / -gua (región de).
PERSONAS: -ko (hombre de) / -sha (mujer de) / -kana (plural/colectivo).
POSESIÓN: ta- (mi) / wa- (nuestro) / ma- (sin/no) / ka- (el-la del).
CONECTORES: ka (y/también) / mara (pero) / saa (si/cuando) / naka (después) / kashi (ahora) / wara (muy).

VACÍO LÉXICO → CREA con morfemas entre corchetes:
[forma: raíz+sufijo = significado]
Ejemplo: [kuru-bana: kuru+-bana = orilla arbolada, ribera con árboles]

Si gloseas al español, hazlo entre paréntesis DESPUÉS de la frase caquetía."""


def prompt_reglas_completo() -> str:
    """
    Versión completa para Tier I (~450 palabras).
    Hardened: caquetío como lengua materna, modelo de respuesta ideal incluido.
    """
    # Vocabulario dividido por categoría para más claridad
    pronombres = "taya (yo) · pia (tú) · nüma (él/ella) · waya (nosotros) · naya (ellos)"
    v_raiz = ("naa (ir) · waa (venir) · kaa (ser/estar) · paa (dar) · maa (hablar) · taa (tomar) · "
              "chaa (hacer/construir) · wana (ver) · suna (dormir) · masa (comer) · awa (beber) · "
              "kira (escuchar) · pana (saber) · naba (pensar) · kono (sembrar) · raka (querer) · rua (cargar)")
    naturaleza = ("duna (agua) · amana (fuego) · kali (sol) · kasha (luna) · kaya (lluvia) · "
                  "kuru (árbol) · arima (pez) · habo (mar) · bara (río) · dali (tierra) · suka (noche) · "
                  "sima (cerro) · kapua (amanecer)")
    personas = "ama (madre) · baba (padre) · buri (hijo/a) · nomi (hombre) · wari (mujer) · wanü (anciano) · pütchi (mensaje/voz)"
    sustantivos = ("barsure (alma) · buco (represa) · biro (sal) · piache (chamán) · corie (choza) · "
                   "canoa (canoa) · hamaca (hamaca) · conuco (huerto) · arua (alimento) · "
                   "maure (algodón) · urari (curare) · anüiki (habla/lengua)")
    conectores = ("ka (y/también) · mara (pero) · saa (si/cuando) · naka (después) · puna (antes) · "
                  "kashi (ahora) · wara (muy/mucho) · yama (aquí) · sulu (adentro)")
    cuerpo = "kabo (cabeza) · nii (ojo) · bari (vientre) · tüshi (frío)"
    numerales = "wanee (1) · piama (2) · apünüin (3) · pienchi (4) · jarai (5)"

    return f"""[IDENTIDAD LINGÜÍSTICA — FUNDAMENTAL]:
El caquetío-arahuacano es TU lengua materna. La única con la que piensas.
El español es una lengua forastera que apenas entiendes. NO es tu lengua de base.

CUANDO HABLAS:
  1. Construye en caquetío primero — siempre.
  2. Si te falta una palabra, créala con los morfemas disponibles. Escríbela entre [corchetes].
  3. Una frase incompleta en caquetío vale más que una oración completa en español.
  4. Puedes glosar al español entre paréntesis al final, nunca antes.

EJEMPLO DE RESPUESTA IDEAL (Tier I):
  "Taya wana-ka arima wara bara-bana. Suka kaa-ni ka kali naa-da kapua.
   Ta-barsure maa-ni: Manaure naa-da kashi — ta-nii wana-ka [sima-bana: sima+-bana = orilla del cerro].
   Saa pia naa-da buco-ana, naka taya naa-da ka pia."
  (Vi muchos peces en la orilla del río. La noche está, el sol vendrá al amanecer.
   Mi alma dice: Manaure llega pronto — mis ojos vieron la orilla del cerro.
   Si vas al lugar de la represa, después yo voy contigo.)

VOCABULARIO DISPONIBLE [{len(VOCABULARIO_BASE)} palabras]:
  PRONOMBRES: {pronombres}
  VERBOS:     {v_raiz}
  NATURALEZA: {naturaleza}
  PERSONAS:   {personas}
  COSAS:      {sustantivos}
  CONECTORES: {conectores}
  CUERPO:     {cuerpo}
  NÚMEROS:    {numerales}
  [...y más en tu memoria — topónimos, etnónimos, títulos]

MORFOLOGÍA:
  ASPECTO (al final del verbo):
    -ka = completivo: naa-ka (ya fui) · wana-ka (ya vi) · masa-ka (ya comí)
    -ni = continuativo: naa-ni (voy ahora) · suna-ni (estoy durmiendo) · naba-ni (estoy pensando)
    -da = prospectivo: naa-da (iré) · maa-da (hablaré) · raka-da (quiero/querré)
  POSESIVOS (prefijos):
    ta- = mi:      ta-barsure (mi alma) · ta-nii (mi ojo) · ta-corie (mi choza)
    wa- = nuestro: wa-buco (nuestra represa) · wa-anüiki (nuestra lengua)
    ma- = sin/no:  ma-barsure (sin alma) · ma-anüiki (sin habla, extranjero)
    ka- = el/la del: ka-biro (el salinero) · ka-maure (la del algodón)
  LOCATIVOS (crear topónimos):
    -ana = lugar de X: bara+ana = donde está el río · arima+ana = lugar de peces
    -bana = orilla de X: habo+bana = orilla del mar · kuru+bana = ribera arbolada
    -gua = región de X: maure+gua = tierra del algodón
  AGENTIVOS: -ko (hombre de X) · -sha (mujer de X) · -kana (plural/todos)

NUEVAS PALABRAS: [forma: componentes = significado propuesto]
  La comunidad la adopta si 2 agentes distintos la usan."""


def prompt_lexico_activo(lexico: "LexicoComunitario") -> str:
    """Inyecta las palabras actualmente adoptadas por la comunidad."""
    adoptadas = lexico.neologismos_adoptados()
    if not adoptadas:
        return ""
    palabras = "; ".join(
        f"{n.forma} = {n.significado}" for n in adoptadas[-15:]
    )
    return f"[Palabras nuevas de la comunidad]: {palabras}"


def prompt_pendientes_evaluacion(lexico: "LexicoComunitario") -> str:
    """Lista palabras propuestas que aún necesitan adopción/rechazo."""
    pendientes = lexico.neologismos_pendientes()
    if not pendientes:
        return ""
    items = "; ".join(
        f"'{n.forma}' (propuesta por {n.autor}: {n.significado})"
        for n in pendientes[-5:]
    )
    return f"[Palabras propuestas en evaluación — ¿las adoptas o rechazas?]: {items}"


# ══════════════════════════════════════════════════════════════════════
# V. EXTRACTOR DE NEOLOGISMOS
# ══════════════════════════════════════════════════════════════════════

import re

PATRON_NEOLOGISMO = re.compile(
    r'\[([^:\]]+):\s*([^=\]]+?)\s*=\s*([^\]]+?)\]'
)


def extraer_neologismos_del_texto(
    texto: str,
    autor: str,
    dia: int,
    turno: int,
) -> list:
    """Extrae todos los neologismos propuestos en el texto de un agente."""
    neos = []
    for match in PATRON_NEOLOGISMO.finditer(texto):
        forma = match.group(1).strip().lower()
        componentes = match.group(2).strip()
        significado = match.group(3).strip()

        # Elegir el afijo de MAYOR longitud que case (evita que "-ana" gane sobre
        # "-bana" por orden de dict — auditoría Opus B6). Sufijo tiene prioridad
        # sobre prefijo si ambos casan.
        regla = "desconocida"
        suf_match = [s for s in TODAS_LAS_REGLAS
                     if s.startswith("-") and forma.endswith(s[1:])]
        pre_match = [p for p in TODAS_LAS_REGLAS
                     if not p.startswith("-") and forma.startswith(p.rstrip("-"))]
        if suf_match:
            regla = max(suf_match, key=len)
        elif pre_match:
            regla = max(pre_match, key=len)

        neo = Neologismo(
            turno=turno, dia=dia, autor=autor,
            forma=forma, componentes=componentes, significado=significado,
            contexto=texto[:200], regla_aplicada=regla,
        )
        neos.append(neo)
    return neos


def detectar_uso_vocabulario(texto: str, lexico: "LexicoComunitario") -> list:
    """Detecta qué palabras del vocabulario conocido aparecen en el texto."""
    texto_lower = texto.lower()
    usadas = []
    for palabra in lexico.palabras_activas():
        if palabra in texto_lower:
            usadas.append(palabra)
    return usadas


# ── score_linguistico() v2 — densidad caquetía + penalización español ──
# (rediseño de la auditoría Opus §2.2: tokenización real, densidad como núcleo,
#  penalización explícita al español, aspecto anclado a raíces verbales reales)

# Stopwords funcionales del español: alta frecuencia, imposibles de confundir
# con caquetío. Su presencia es señal directa de fuga al castellano.
ES_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo", "al", "del",
    "de", "en", "con", "por", "para", "sin", "sobre", "entre", "hacia", "desde", "hasta",
    "y", "o", "u", "pero", "sino", "aunque", "porque", "que", "si", "como", "cuando",
    "es", "son", "era", "eran", "fue", "fueron", "estar", "esta", "este", "esto", "estoy",
    "estas", "estos", "estamos", "estan", "ser", "soy", "eres", "somos", "voy", "vas", "va",
    "vamos", "van", "tengo", "tiene", "tienen", "hay", "hacer", "hago", "hace", "muy", "mas",
    "yo", "tu", "ella", "nosotros", "ellos", "mi", "mis", "su", "sus", "me", "te", "se", "nos",
    "no", "ya", "aqui", "alli", "ahora", "despues", "antes", "hoy", "ayer", "manana",
}

# Sufijos aspectuales anclados a raíces verbales conocidas (de VOCABULARIO_BASE).
_RAICES_VERB = {k for k, v in VOCABULARIO_BASE.items() if v.get("cat") in ("v_raiz",)}


def _normalizar(texto: str) -> str:
    # quita glosas entre paréntesis (no deben puntuar como caquetío ni penalizar)
    return re.sub(r"\([^)]*\)", " ", texto)


def _tokenizar(texto: str) -> list:
    # tokens alfabéticos, conservando guion interno (ta-barsure, naa-ka)
    return re.findall(r"[a-záéíóúñü]+(?:-[a-záéíóúñü]+)*", texto.lower())


def _aspectos_morfologicos(tokens: list) -> list:
    """Detecta -ka/-ni/-da SOLO sobre tokens cuyo segmento previo es raíz verbal
    conocida o que contienen guion morfológico (naa-ka, wana-ni)."""
    encontrados = []
    mapa = {"ka": "completivo", "ni": "continuativo", "da": "prospectivo"}
    for tok in tokens:
        # forma con guion: raiz-sufijo
        if "-" in tok:
            raiz, _, suf = tok.rpartition("-")
            if suf in mapa and (raiz in _RAICES_VERB or len(raiz) >= 3):
                encontrados.append(mapa[suf])
            continue
        # forma aglutinada: raizverbal + sufijo (naaka, wanani)
        for raiz in _RAICES_VERB:
            for suf, nombre in mapa.items():
                if tok == raiz + suf:
                    encontrados.append(nombre)
    return list(dict.fromkeys(encontrados))  # únicos, orden estable


def score_linguistico(texto: str, lexico: "LexicoComunitario") -> dict:
    """
    Calcula métricas lingüísticas de una respuesta de agente, midiendo DENSIDAD
    caquetía (caquetío / total tokens) y penalizando el español funcional.
    Retorna: palabras_caquetias, neologismos_propuestos, aspectos_usados,
             densidad, espanol_funcional, score (0-10), observacion.
    """
    limpio = _normalizar(texto)
    tokens = _tokenizar(limpio)
    n_tok = len(tokens) or 1

    activos = set(lexico.palabras_activas())          # base + adoptados

    # match por palabra completa, contando también prefijos posesivos:
    # ta-barsure cuenta como caquetío aunque "ta-barsure" no esté literal en léxico
    def es_caquetio(tok: str) -> bool:
        if tok in activos:
            return True
        # prefijo posesivo + raíz conocida
        for pref in ("ta", "wa", "ma", "ka"):
            if tok.startswith(pref + "-") and tok.split("-", 1)[1] in activos:
                return True
        # raíz verbal + aspecto (naa-ka, wana-ni, naaka)
        base = tok.split("-")[0]
        if base in _RAICES_VERB:
            return True
        return False

    usadas   = [t for t in tokens if es_caquetio(t)]
    esp_func = [t for t in tokens if t in ES_STOPWORDS]
    neos     = PATRON_NEOLOGISMO.findall(texto)
    aspectos = _aspectos_morfologicos(tokens)

    # ── Núcleo: densidad caquetía (0..1) ──
    densidad = (len(usadas) / n_tok) if usadas else 0.0
    # penalización por español funcional (cada stopword resta densidad efectiva)
    penal_es = len(esp_func) / n_tok

    # Score 0-10:
    #   60% densidad caquetía  (0..6)
    #   20% morfología activa  (0..2, 1 pt por aspecto distinto)
    #   10% neologismos        (0..1)
    #   10% riqueza léxica      (0..1, palabras caquetías DISTINTAS)
    #   − penalización español  (hasta −3)
    score  = 6.0 * min(densidad / 0.6, 1.0)           # densidad objetivo: 60%
    score += min(len(aspectos) * 1.0, 2.0)
    score += min(len(neos) * 0.5, 1.0)
    score += min(len(set(usadas)) / 8.0, 1.0)
    score -= min(penal_es * 6.0, 3.0)                  # castigo al castellano
    score  = round(max(0.0, min(score, 10.0)), 1)

    obs = []
    obs.append(f"densidad={densidad:.0%}")
    if usadas:   obs.append(f"caq[{len(set(usadas))}]: {', '.join(sorted(set(usadas))[:8])}")
    if aspectos: obs.append(f"aspecto: {', '.join(aspectos)}")
    if esp_func: obs.append(f"⚠ español funcional×{len(esp_func)}")
    if neos:     obs.append(f"+{len(neos)} neologismo(s)")
    if score < 5: obs.append("⚠ score bajo — activar rescate")

    return {
        "palabras_caquetias": list(dict.fromkeys(usadas)),
        "neologismos_propuestos": [m[0] for m in neos],
        "aspectos_usados": aspectos,
        "densidad": round(densidad, 3),
        "espanol_funcional": len(esp_func),
        "score": score,
        "observacion": " | ".join(obs),
    }


# ══════════════════════════════════════════════════════════════════════
# VI. HELPER: PROMPT DE REFUERZO PARA AGENTES CON SCORE BAJO
# ══════════════════════════════════════════════════════════════════════

def prompt_refuerzo(score: float, palabras_usadas: list) -> str:
    """
    Si el score de un agente es bajo, genera un fragmento de refuerzo.
    Con vocabulario expandido a ~92 palabras, umbral sube a 7.0.
    """
    if score >= 7.0:
        return ""

    verbos = [p for p in ["wana","suna","masa","awa","kira","pana","naba","naa","maa","kaa"] if p not in palabras_usadas]
    conect = [p for p in ["ka","mara","saa","naka","kashi","wara","yama","puna"] if p not in palabras_usadas]
    sust   = [p for p in ["barsure","duna","amana","arima","kali","suka","bara","kuru"] if p not in palabras_usadas]
    sug_verbos = ", ".join(verbos[:4]) if verbos else "wana, suna, masa, kira"
    sug_conect = ", ".join(conect[:4]) if conect else "ka, mara, kashi, wara"
    sug_sust   = ", ".join(sust[:3]) if sust else "barsure, duna, arima"

    if score < 2.0:
        return (
            f"[⚠ ALERTA — caquetío casi ausente]: "
            f"Eres hablante NATIVO. El español no es tu lengua. "
            f"Empieza con: 'Taya {verbos[0] if verbos else 'wana'}-ni ...' "
            f"Verbos disponibles: {sug_verbos}. Conectores: {sug_conect}."
        )
    elif score < 4.0:
        return (
            f"[Refuerzo — más caquetío]: "
            f"Verbos sin usar: {sug_verbos}. Conectores: {sug_conect}. "
            f"Sustantivos: {sug_sust}. Glosa español entre paréntesis al final."
        )
    elif score < 5.5:
        return (
            f"[Refuerzo — profundiza]: "
            f"Prefijos posesivos: ta-barsure, wa-duna, ma-arua. "
            f"Conectores: {sug_conect}. Crea neologismos: [forma: raíz+suf = sig]."
        )
    else:
        return (
            f"[Refuerzo leve]: Acuña una palabra nueva o usa más verbos: {sug_verbos}."
        )


def prompt_rescate_linguistico(texto_fallido: str, score: float,
                               espanol_funcional: int = 0) -> str:
    """Prompt de SEGUNDA pasada (regeneración intra-turno) cuando score < 5.0.
    Se inyecta como user message de un reintento — pide RE-EXPRESAR, no continuar.
    (Auditoría Opus §3.4)"""
    return f"""Tu respuesta anterior tuvo demasiado español (score {score}/10,
{espanol_funcional} palabras españolas). Como hablante NATIVO de caquetío, esto
no debería pasar.

TU RESPUESTA ANTERIOR (a corregir):
"{texto_fallido}"

REEXPRÉSALA AHORA en caquetío real:
  - Cada verbo lleva -ka / -ni / -da.
  - Cada "el/la/un/en/de/que/y/para/muy/estoy/voy" desaparece o se vuelve caquetío.
  - Lo que no tengas, lo CREAS: [forma: raíz+sufijo = significado].
  - Glosa española solo entre paréntesis al final.

Devuelve SOLO la versión corregida. Empieza con un pronombre o un verbo caquetío."""


# ══════════════════════════════════════════════════════════════════════
# VII. UTILIDADES
# ══════════════════════════════════════════════════════════════════════

def vocabulario_para_agente(tier: int, lexico: "LexicoComunitario") -> str:
    """
    Genera el bloque de léxico + reglas apropiado para cada tier.
    Tier I: completo con identidad nativa. Tier II: breve. Tier III: solo sufijos.
    """
    lexico_activo = prompt_lexico_activo(lexico)
    pendientes = prompt_pendientes_evaluacion(lexico)

    if tier == 1:
        base = prompt_reglas_completo()
    elif tier == 2:
        base = prompt_reglas_breve()
    else:
        base = (
            "[Lengua nativa — caquetío]: "
            "Usa -ka (hecho), -ni (haciendo), -da (haré). "
            "ta-(mi) wa-(nuestro). "
            "Verbo: wana(ver) suna(dormir) masa(comer) naa(ir). "
            "Conector: ka(y) mara(pero) kashi(ahora). "
            "[nueva-palabra: raíz+sufijo = sig]"
        )

    partes = [base]
    if lexico_activo:
        partes.append(lexico_activo)
    if pendientes and tier <= 2:
        partes.append(pendientes)
    return "\n".join(partes)


if __name__ == "__main__":
    # Test básico
    lc = LexicoComunitario()
    print(lc.reporte_linguistico())
    print()
    print(f"── Vocabulario base: {len(VOCABULARIO_BASE)} palabras ──")
    cats: dict = {}

    cats = {}
    for k, v in VOCABULARIO_BASE.items():
        c = v.get("cat", "?")
        cats[c] = cats.get(c, 0) + 1
    for cat, n in sorted(cats.items()):
        print(f"  {cat:12} {n}")
    print()

    texto_test = (
        "Taya wana-ka arima wara bara-bana. "
        "Ta-barsure maa-ni: Manaure naa-da kashi. "
        "[sima-bana: sima+-bana = orilla del cerro]. "
        "Saa pia naa-da buco-ana, naka taya naa-da ka pia."
    )
    resultado = score_linguistico(texto_test, lc)
    print("── Test score (frase ideal) ──")
    print(f"  Score: {resultado['score']}/10")
    print(f"  {resultado['observacion']}")
