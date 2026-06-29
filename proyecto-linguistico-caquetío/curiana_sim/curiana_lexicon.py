"""
CURIANA — Motor Léxico y Morfológico
=====================================
Motor de reglas morfológicas arahuacas para la simulación de
emergencia lingüística en la comunidad caquetía de Curiana.

Basado en:
  - Vocabulario caquetío atestiguado (Zavala Reyes 2015, Jahn 1927, Alvarado 1921)
  - Morfología Wayunaiki (Álvarez 2017; Goulet & Jusayú 1978; Mansen & Mansen 1984)
  - Cognados arahuacos: Lokono, Taíno, Garifuna
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
    "barsure":    {"sig": "alma, esencia vital, fuerza interior",          "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Angulo Molina; Zavala Reyes 2015", "categoria": "cosmos"},
    "buco":       {"sig": "represa, presa de agua, reservorio",             "cat": "sust",  "fuente": "caquetío"},
    "biro":       {"sig": "sal",                                            "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 (Angulo Molina); recurso estratégico Coro", "categoria": "comercio"},
    "chiriguare": {"sig": "gavilán, ave rapaz grande",                      "cat": "sust",  "fuente": "caquetío"},
    "maure":      {"sig": "fibra de algodón, hilo para tejer",              "cat": "sust",  "fuente": "caquetío"},
    "urari":      {"sig": "veneno/medicina vegetal (curare)",               "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 (AM); artículo de comercio", "categoria": "comercio"},
    "corie":      {"sig": "choza, habitación, espacio propio",              "cat": "sust",  "fuente": "caquetío"},
    "saruro":     {"sig": "árbol saruro (frutos pequeños)",                 "cat": "sust",  "fuente": "caquetío"},
    "tuqueque":   {"sig": "lagartija pequeña, gecko",                       "cat": "sust",  "fuente": "caquetío"},
    "coro":       {"sig": "cardón grande, cactus columnar",                 "cat": "sust",  "fuente": "caquetío/topónimo"},
    "piache":     {"sig": "chamán, curandero, intermediario espiritual",    "cat": "sust",  "fuente": "caquetío"},
    "caraota":    {"sig": "frijol negro, legumbre",                         "cat": "sust",  "fuente": "caquetío"},
    "pauji":      {"sig": "pavo de monte, ave grande",                      "cat": "sust",  "fuente": "caquetío"},
    "manaure":    {"sig": "título laudatorio del señor principal",          "cat": "título","fuente": "caquetío"},
    "curiana":    {"sig": "territorio de los caquetíos / lugar del cardón", "cat": "topón", "fuente": "caquetío"},

    # ── Arahuaco compartido (cognados en Wayunaiki, Lokono, Taíno) ──
    "wayuu":      {"sig": "persona, gente, ser humano",                     "cat": "sust",  "fuente": "wayunaiki"},
    "anüiki":     {"sig": "habla, palabra, lengua",                         "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "anasa":      {"sig": "bueno, bien, bello (< anasü Wayunaiki)",         "cat": "adj",   "fuente": "wayunaiki-cogn"},
    "taya":       {"sig": "yo (1ra persona singular)",                      "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "waya":       {"sig": "nosotros (1ra persona plural)",                  "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "pia":        {"sig": "tú (2da persona singular)",                      "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "nüma":       {"sig": "él/ella (pronombre 3ra persona)",                "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "naya":       {"sig": "ellos, ellas (3ra persona plural)",              "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "wanee":      {"sig": "uno (numeral)",                                  "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "piama":      {"sig": "dos (numeral)",                                  "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "apünüin":    {"sig": "tres (numeral)",                                 "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "pienchi":    {"sig": "cuatro (numeral)",                               "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "jarai":      {"sig": "cinco (numeral)",                                "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},

    # ── Taíno (familia arahuaca, préstamos a todas las lenguas caribeñas) ──
    "hamaca":     {"sig": "red colgante para dormir",                       "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido"},
    "canoa":      {"sig": "embarcación excavada en tronco",                 "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido"},
    "cacique":    {"sig": "jefe, señor principal de la comunidad",          "cat": "sust",  "fuente": "taíno"},
    "maíz":       {"sig": "planta de maíz, grano principal",               "cat": "sust",  "fuente": "taíno"},
    "yuca":       {"sig": "tubérculo, mandioca amarga o dulce",             "cat": "sust",  "fuente": "taíno", "notas": "Tno. yuca; cognado Lokono mariti", "categoria": "flora"},
    "batata":     {"sig": "camote, tubérculo dulce",                        "cat": "sust",  "fuente": "taíno", "notas": "Tno. batata; arahuaco del área caribeña", "categoria": "flora"},
    "bohío":      {"sig": "casa comunal, choza redonda con techo cónico",   "cat": "sust",  "fuente": "taíno"},
    "conuco":     {"sig": "huerto familiar, parcela cultivada",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido"},
    "iguana":     {"sig": "lagarto grande, iguana",                         "cat": "sust",  "fuente": "taíno/caribe"},

    # ── Raíces verbales arahuacas (reconstruidas por comparación) ────
    "naa":        {"sig": "ir, moverse hacia",                              "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "waa":        {"sig": "venir, aproximarse",                             "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "kaa":        {"sig": "estar, existir, ser (cópula)",                   "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "paa":        {"sig": "dar, ofrecer, transferir",                       "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "maa":        {"sig": "decir, hablar, comunicar",                       "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "taa":        {"sig": "tomar, coger, recibir",                          "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "chaa":       {"sig": "hacer, construir, crear",                        "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},

    # ── Única frase Caquetía atestiguada ──────────────────────────────
    # "Chacamba cudanga" = ¿Cómo está usted? (saludo)
    # "Cudan de cuté"    = Para servirle a usted
    "chacamba":   {"sig": "¿cómo? (pregunta de estado)",                    "cat": "interr","fuente": "caquetío-atestiguado"},
    "cudanga":    {"sig": "usted, vos (2da persona formal)",                "cat": "pron",  "fuente": "caquetío-atestiguado"},
    "cudan":      {"sig": "servir, estar al servicio de",                   "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "cuté":       {"sig": "a usted, para usted (dativo formal)",            "cat": "pron",  "fuente": "caquetío-atestiguado"},

    # ── Verbos arahuacos (cognados Lokono / Wayunaiki / Garifuna) ────
    "wana":       {"sig": "ver, observar, mirar",                           "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/wayunaiki", "fuente": "caquetío-reconstruido"},
    "suna":       {"sig": "dormir, reposar, descansar",                     "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "masa":       {"sig": "comer, alimentarse",                             "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "awa":        {"sig": "beber, tomar líquido",                           "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    "kira":       {"sig": "escuchar, oír, atender",                         "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en wayunaiki/lokono", "fuente": "caquetío-reconstruido"},
    "panaa":      {"sig": "saber, conocer, entender",                       "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "naba":       {"sig": "pensar, reflexionar, meditar",                   "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/wayunaiki", "fuente": "caquetío-reconstruido"},
    "kono":       {"sig": "sembrar, plantar, cultivar",                     "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/taíno", "fuente": "caquetío-reconstruido"},
    "raka":       {"sig": "querer, desear, necesitar",                      "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "rua":        {"sig": "cargar, transportar, llevar",                    "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},

    # ── Naturaleza (cognados arahuacos) ─────────────────────────────
    "duna":       {"sig": "agua (corriente, bebible)",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en garifuna/lokono", "fuente": "caquetío-reconstruido"},
    "amana":      {"sig": "fuego, lumbre, brasa",                           "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    "kali":       {"sig": "sol",                                            "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "kasha":      {"sig": "luna",                                           "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki/lokono", "fuente": "caquetío-reconstruido"},
    "kaya":       {"sig": "lluvia, agua del cielo",                         "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono (juya-cogn)", "fuente": "caquetío-reconstruido"},
    "kuru":       {"sig": "árbol, madera, tronco",                          "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "arima":      {"sig": "pez, pescado",                                   "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "habo":       {"sig": "mar, océano, aguas grandes",                     "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "dali":       {"sig": "tierra, suelo, polvo",                           "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en garifuna/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "suka":       {"sig": "noche, oscuridad",                               "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "bara":       {"sig": "río, corriente fluvial",                         "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan/topónimo", "fuente": "caquetío-reconstruido"},
    "sima":       {"sig": "cerro, montaña, elevación",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/topónimo (Barquisimeto)", "fuente": "caquetío-reconstruido"},

    # ── Personas y parentesco ──────────────────────────────────────────
    "ama":        {"sig": "madre, mujer que nutre y da origen",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan universal", "fuente": "caquetío-reconstruido"},
    "baba":       {"sig": "padre, hombre que protege",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "buri":       {"sig": "hijo, hija, criatura, descendiente",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "nomi":       {"sig": "hombre adulto (no título)",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "wari":       {"sig": "mujer adulta (no título)",                       "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "wanü":       {"sig": "anciano, mayor, persona de saber acumulado",     "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "pütchi":     {"sig": "mensaje, palabra sagrada, voz del espíritu",     "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},

    # ── Cuerpo ──────────────────────────────────────────────────────────
    "kabo":       {"sig": "cabeza, mente, lo alto de",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "nii":        {"sig": "ojo, mirada, visión",                            "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono-cogn", "fuente": "caquetío-reconstruido"},
    "bari":       {"sig": "vientre, barriga, interior del cuerpo",          "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "arua":       {"sig": "alimento, comida, sustento (raíz de 'arawak')",  "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "kapua":      {"sig": "amanecer, alba, primera luz del día",            "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "tüshi":      {"sig": "frío, temperatura baja",                         "cat": "adj",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},

    # ── Partículas y conectores ────────────────────────────────────────
    # (permiten construir frases más complejas sin recurrir al español)
    "ka":         {"sig": "y, también, además, con (conector aditivo)",     "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    "mara":       {"sig": "pero, sin embargo, aunque (contraste)",          "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "saa":        {"sig": "si, cuando, al momento de (condicional/temp.)",  "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "naka":       {"sig": "después, luego, más tarde (temporal posterior)", "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "puna":       {"sig": "antes, ya, primero (temporal anterior)",         "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "kashi":      {"sig": "ahora, en este momento (temporal presente)",     "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
    "wara":       {"sig": "muy, mucho, bastante (intensificador)",          "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "sulu":       {"sig": "adentro, dentro de, en el interior de",         "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido"},
    "yama":       {"sig": "aquí, en este lugar (deíctico proximal)",        "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn", "fuente": "caquetío-reconstruido"},
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

    # ── Intercambio y comercio (raíces y cognados arahuacos) ─────────
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

    # ── Flora local (cognados arahuacos y atestiguado) ───────────────
    "mankaba":    {"sig": "manglar, bosque de raíces en agua salobre",      "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "marawa":     {"sig": "palma, palmera de cogollo y fibra",              "cat": "sust",  "fuente": "lokono/garifuna"},
    "kasiripa":   {"sig": "yuca brava, mandioca para casabe",               "cat": "sust",  "fuente": "lokono/garifuna"},
    "marisi":     {"sig": "maíz en mazorca, grano de cosecha",              "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "yuri":       {"sig": "tabaco, hoja sagrada del piache",                "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "kukuisa":    {"sig": "cocuiza, agave de fibra para cuerda",            "cat": "sust",  "fuente": "caquetío/topónimo"},

    # ── Fauna (cognados arahuacos) ───────────────────────────────────
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

    # ── Tiempo y clima (cognados arahuacos y derivados locales) ──────
    "joutai":     {"sig": "viento, corriente de aire (< joutai Wayunaiki)", "cat": "sust",  "fuente": "wayunaiki-cogn"},
    "kayawara":   {"sig": "tormenta, lluvia con viento fuerte (kaya+wara)", "cat": "sust",  "fuente": "lokono/proto-arawakan"},
    "haborü":     {"sig": "marejada, oleaje grande del mar (habo+rü)",      "cat": "sust",  "fuente": "lokono/garifuna"},
    "madunaka":   {"sig": "sequía, tiempo sin agua (ma+duna)",              "cat": "sust",  "fuente": "proto-arawakan"},
    "habobrisa":  {"sig": "brisa del golfete, viento suave del mar",        "cat": "sust",  "fuente": "lokono/garifuna"},
    # (fin de entradas nuevas — expansión a 146 palabras)

    # ── Expansión atestiguada — fuentes coloniales (Galeotto Cey, Oviedo y Valdés,
    #    Las Casas, Arellano Moreno, Zavala Reyes 2015, Van Buurt 2014, Gatschet 1885) ──
    "ateri":      {"sig": "hombre, varón",                                  "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "iero":       {"sig": "mujer",                                          "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "humocaro":   {"sig": "mujer bella, hermosa",                           "cat": "adj",   "fuente": "caquetío-atestiguado"},
    "cazi":       {"sig": "sol",                                            "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cati":       {"sig": "luna",                                           "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "apana":      {"sig": "una luna (unidad de tiempo ~30 días)",           "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "buiamati":   {"sig": "dos lunas (unidad de tiempo ~60 días)",          "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cazebo":     {"sig": "poniente, oeste",                                "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cazicure":   {"sig": "levante, este",                                  "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "diao":       {"sig": "señor, jefe de segundo orden",                   "cat": "título","fuente": "caquetío-atestiguado"},
    "guaitiao":   {"sig": "amigo ritual, aliado de alianza",                "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "datihao":    {"sig": "padrino de cautivo, el que presta su nombre al esclavo", "cat": "sust", "fuente": "caquetío-atestiguado"},
    "uriacoa":    {"sig": "título del cacique mayor de Curiana/Coro",       "cat": "título","fuente": "caquetío-atestiguado"},
    "tata":       {"sig": "padre, papá",                                   "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "dare":       {"sig": "diente; hijo (extensión metafórica)",            "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "sawaka":     {"sig": "inframundo, reino de los muertos",               "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "paro":       {"sig": "río, cauce simple",                              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cari":       {"sig": "orilla del mar, costa",                         "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "rao":        {"sig": "arena, arenal costero",                         "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "barici":     {"sig": "agua turbia, tierras coloradas rojizas",         "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "pariri":     {"sig": "pantano, ciénaga",                              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "tarica":     {"sig": "laguna, espejo de agua interior",               "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "güique":     {"sig": "río navegable, cauce ancho",                    "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "quidi":      {"sig": "sierra, serranía, cerro largo",                 "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "borojo":     {"sig": "salina, lago salado de Coro",                   "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "ucibo":      {"sig": "cuenta de piedra, chaquira",                    "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "buriche":    {"sig": "licor fermentado, chicha de maíz",              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "buko":       {"sig": "canal de riego, acequia, presa",                "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "gua":        {"sig": "conuco, heredad, terreno cercado cultivado",    "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "duraboa":    {"sig": "conuco sembrado, parcela en producción",        "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "tabri":      {"sig": "siembra, plantación en proceso",                "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "tebe":       {"sig": "lugar de cultivo, campo agrícola",              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "amaca":      {"sig": "sitio de moler maíz, área de procesamiento",    "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "urapa":      {"sig": "sitio de cría de animales, corral",             "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "garabal":    {"sig": "tierra de crianza, pastizal",                   "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "kunuku":     {"sig": "parcela de cultivo, conuco insular (ABC)",      "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cazá":       {"sig": "puche de maíz, atole",                         "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "mazato":     {"sig": "bebida de harinas fermentada",                  "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cumaragua":  {"sig": "ciruela, espuma rosada (Spondias mombin)",      "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "auyama":     {"sig": "auyama, calabaza (Cucurbita maxima)",           "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "bajarí":     {"sig": "recorrer, caminar",                             "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "bureche":    {"sig": "hacer, realizar, fabricar",                     "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "eroa":       {"sig": "empezar, crear, originar",                      "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "güere":      {"sig": "dar, entregar, ofrecer",                        "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "jacura":     {"sig": "guardar, conservar, custodiar",                 "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "jai":        {"sig": "oír, escuchar",                                 "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "jaguey":     {"sig": "estancar, represar, crear charco artificial",   "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "jacuque":    {"sig": "regar, irrigar",                                "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "pana":       {"sig": "uno",                                           "cat": "num",   "fuente": "caquetío-atestiguado", "notas": "Pedro Manuel Arcaya; Zavala Reyes 2015", "categoria": "numerales"},
    "gudamuen":   {"sig": "dos",                                           "cat": "num",   "fuente": "caquetío-atestiguado"},
    "sabuenen":   {"sig": "tres",                                          "cat": "num",   "fuente": "caquetío-atestiguado"},
    "catarí":     {"sig": "cuatro",                                        "cat": "num",   "fuente": "caquetío-atestiguado"},
    "kama":       {"sig": "tapir, danta (Tapirus terrestris)",             "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "koke":       {"sig": "bachaco, hormiga grande (Atta spp.)",           "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "cachicamo":  {"sig": "armadillo (Dasypus novemcinctus)",              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "caduchi":    {"sig": "fruto del cardón (Cereus spp.)",                "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "kadushi":    {"sig": "cactus columnar (Cereus hexagonus)",            "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "tara":       {"sig": "venado, ciervo (Odocoileus virginianus)",       "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "warawara":   {"sig": "buitre, zamuro (Cathartes curasoica)",          "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "watapana":   {"sig": "árbol dividivi (Caesalpinia coriaria)",         "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "chogogo":    {"sig": "flamingo rosado (Phoenicopterus ruber)",        "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "chuchubi":   {"sig": "sinsonte tropical (Mimus gilvus)",              "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "bariki":     {"sig": "tierra colorada, pigmento encarnado, pintura corporal", "cat": "sust", "fuente": "caquetío-atestiguado"},
    "mene":       {"sig": "sustancia que brota de la tierra (petróleo, resina)",   "cat": "sust", "fuente": "caquetío-atestiguado"},
    "poporo":     {"sig": "maza-porra, arma de combate ceremonial",        "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "ture":       {"sig": "vasija, utensilio de barro",                    "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "guanepe":    {"sig": "cesto para cargar niños",                       "cat": "sust",  "fuente": "caquetío-atestiguado"},
    "na":         {"sig": "como, semejante a (partícula comparativa)",     "cat": "part",  "fuente": "caquetío-atestiguado"},

    # ── Expansión taíno (préstamos arahuacos del área caribeña) ──────
    "maisi":      {"es": "maíz (Zea mays)", "fuente": "taíno", "notas": "Tno. maisi → español maíz; cognado Lokono mariti", "categoria": "flora"},
    "aji":        {"es": "ají, chile (Capsicum spp.)", "fuente": "taíno", "notas": "Tno. ají → español ají; venezolanismo activo", "categoria": "flora"},
    "papaya":     {"es": "papaya, lechosa (Carica papaya)", "fuente": "taíno", "notas": "Tno. papaya → español papaya", "categoria": "flora"},
    "guayaba":    {"es": "guayaba (Psidium guajava)", "fuente": "taíno", "notas": "Tno. guayaba → español guayaba", "categoria": "flora"},
    "tabako":     {"es": "tabaco (Nicotiana tabacum), pipa ceremonial", "fuente": "taíno", "notas": "Tno. tabaco; ritual chamánico arahuaco", "categoria": "ritual"},
    "cazabi":     {"es": "cazabe, pan de yuca, torta de mandioca", "fuente": "taíno", "notas": "Tno. cazabi → español cazabe; alimento base arahuaco", "categoria": "alimentacion"},
    "bohio":      {"es": "bohío, casa redonda de varas y palma", "fuente": "taíno", "notas": "Tno. bohío; cognado caquetío probable *kali", "categoria": "arquitectura"},
    "caney":      {"es": "caney, bohío rectangular del cacique", "fuente": "taíno", "notas": "Tno. caney; vivienda del jefe diferenciada", "categoria": "arquitectura"},
    "batey":      {"es": "batey, plaza central del poblado, cancha de juego ritual", "fuente": "taíno", "notas": "Tno. batey; espacio ritual comunitario", "categoria": "arquitectura"},
    "nagua":      {"es": "nagua, falda de algodón de mujer", "fuente": "taíno", "notas": "Tno. nagua → español enagua; Lokono annaka", "categoria": "vestimenta"},
    "piragua":    {"es": "piragua, canoa grande de un palo", "fuente": "taíno", "notas": "Tno. piragua → español piragua", "categoria": "navegacion"},
    "iwana":      {"es": "iguana (Iguana iguana)", "fuente": "taíno", "notas": "Tno. higuana → español iguana; Lokono iwana", "categoria": "fauna"},
    "manati":     {"es": "manatí (Trichechus manatus), vaca marina", "fuente": "taíno", "notas": "Tno. manatí; animal del Golfete de Coro", "categoria": "fauna"},
    "hutia":      {"es": "jutía, roedor grande (Capromys spp.)", "fuente": "taíno", "notas": "Tno. hutía; fuente proteica arahuaca del Caribe", "categoria": "fauna"},
    "guabina":    {"es": "guabina, pez de agua dulce (Hoplias malabaricus)", "fuente": "taíno", "notas": "Tno. guabina; pez de ríos y lagunas costeras", "categoria": "fauna"},
    "cobo":       {"es": "cobo, caracol marino gigante (Strombus gigas), trompeta ritual", "fuente": "taíno", "notas": "Tno. cobo; objeto de intercambio arahuaco", "categoria": "fauna"},
    "cemi":       {"es": "cemí, ídolo sagrado, espíritu materializado", "fuente": "taíno", "notas": "Tno. cemí; objeto ritual de poder arahuaco", "categoria": "cosmos"},
    "areito":     {"es": "areíto, danza ritual narrativa, celebración colectiva", "fuente": "taíno", "notas": "Tno. areíto; práctica arahuaca de memoria oral danzada", "categoria": "ritual"},
    "bejique":    {"es": "bejique, chamán taíno, mediador ritual", "fuente": "taíno", "notas": "Tno. bejique; cognado de piache (Lokono piaye)", "categoria": "cosmos"},
    "huracan":    {"es": "huracán, espíritu del viento destructor, ciclón", "fuente": "taíno", "notas": "Tno. hurakán → español huracán; ser sobrenatural arahuaco", "categoria": "cosmos"},
    "maboya":     {"es": "maboya, espíritu maligno nocturno", "fuente": "taíno", "notas": "Tno. maboya; equivalente al buio en cosmología caquetía", "categoria": "cosmos"},
    "guanin":     {"es": "guanín, aleación de oro y cobre, metal sagrado", "fuente": "taíno", "notas": "Tno. guanín; metal de alto prestigio en redes arahuacas", "categoria": "comercio"},
    "cacike":     {"es": "cacique, jefe político-ritual del grupo", "fuente": "taíno", "notas": "Tno. cacique → español cacique; equivalente al manaure caquetío", "categoria": "jerarquia"},
    "naboria":    {"es": "naboría, servidor permanente, trabajador dependiente del cacique", "fuente": "taíno", "notas": "Tno. naboría; clase social arahuaca", "categoria": "jerarquia"},
    "nitaino":    {"es": "nitaíno, noble, principal, hombre de rango", "fuente": "taíno", "notas": "Tno. nitaíno; clase intermedia entre cacique y naboría", "categoria": "jerarquia"},
    "dujo":       {"es": "dujo, asiento de madera tallado del cacique", "fuente": "taíno", "notas": "Tno. dujo; trono ritual arahuaco", "categoria": "utiles"},
    "macana":     {"es": "macana, garrote de madera dura, arma de combate", "fuente": "taíno", "notas": "Tno. macana; arma arahuaca; análoga al poporo caquetío", "categoria": "armas"},
    "cayo":       {"es": "cayo, islote bajo y arenoso, escollo costero", "fuente": "taíno", "notas": "Tno. cayo → español cayo; rasgos costeros del Golfete", "categoria": "geografia"},
    "manigua":    {"es": "manigua, matorral denso, monte bajo", "fuente": "taíno", "notas": "Tno. manigua; vegetación de transición sabana-bosque", "categoria": "geografia"},
    "bixa":       {"es": "bija, onoto, achiote (Bixa orellana), pigmento corporal rojo", "fuente": "taíno", "notas": "Tno. bixa/bija; pigmento ritual rojo; análogo al bariki caquetío", "categoria": "materiales"},
    "hayo":       {"es": "hayo, coca (Erythroxylum coca), hoja masticada ritual", "fuente": "taíno", "notas": "Tno. hayo; estimulante de uso ritual; documentado en Oviedo", "categoria": "ritual"},

    # ── Expansión lokono ─────────────────────────────────────────────────
    "hadalli":    {"es": "sol (forma Lokono)", "fuente": "lokono", "notas": "Lokono hadalli; cognado de cazi caquetío; raíz proto-arahuaca *kadali", "categoria": "cosmos"},
    "katsi":      {"es": "luna (forma Lokono)", "fuente": "lokono", "notas": "Lokono katsi; cognado de cati caquetío", "categoria": "cosmos"},
    "piaye":      {"es": "chamán, curandero (forma Lokono)", "fuente": "lokono", "notas": "Lokono piaye; cognado de piache (caquetío vía Rivero 1728)", "categoria": "cosmos"},
    # Nota de desambiguación: "bara" ya existe en VOCABULARIO_BASE con el sentido
    # "río, corriente fluvial" (carga semántica usada en tests y prompts de ejemplo:
    # test_quick.py, test_pipeline.py, curiana_orchestrator_v2.py). El cognado Lokono
    # de "mar" se registra bajo "baraha" para no romper esas dependencias.
    "baraha":     {"es": "mar, agua extensa (forma Lokono)", "fuente": "lokono", "notas": "Lokono bara (mar); cognado de para- caquetío. Distinto de 'bara' (río) ya presente en el lexicon", "categoria": "geografia"},
    "koïa":       {"es": "tierra, suelo (forma Lokono)", "fuente": "lokono", "notas": "Lokono koïa; cognado de cúa/kuya caquetío", "categoria": "geografia"},
    "balli":      {"es": "árbol, madera (forma Lokono)", "fuente": "lokono", "notas": "Lokono balli; raíz dendrológica arahuaca", "categoria": "flora"},
    "kannoa":     {"es": "canoa (forma Lokono con -n final nominal)", "fuente": "lokono", "notas": "Lokono kannoa; Lokono añade -n final a sustantivos vs. canoa taíno", "categoria": "navegacion"},
    "annaka":     {"es": "nagua, falda (forma Lokono)", "fuente": "lokono", "notas": "Lokono annaka; cognado de Tno. nagua", "categoria": "vestimenta"},
    "hamaha":     {"es": "hamaca (forma Lokono)", "fuente": "lokono", "notas": "Lokono hamaha; cognado de maure caquetío y Tno. hamaca", "categoria": "utiles"},
    "kaiman":     {"es": "caimán (Caiman crocodilus)", "fuente": "lokono", "notas": "Lokono kaiman → español caimán; arahuaco universal", "categoria": "fauna"},
    "adda":       {"es": "árbol específico (raíz Lokono)", "fuente": "lokono", "notas": "Lokono adda; cognado del morfema ada- en topónimo caquetío Adabacoa", "categoria": "flora"},
    "tutu":       {"es": "río, corriente de agua (forma Lokono)", "fuente": "lokono", "notas": "Lokono tutu; cognado posible del topónimo Tuy", "categoria": "geografia"},
    "wayü":       {"es": "gente libre, pueblo propio (wa- nuestro + -yú gente)", "fuente": "lokono", "notas": "Raíz pan-arahuaca; base del autónimo Wayunaiki", "categoria": "parentesco"},
    "alijuna":    {"es": "forastero, ajeno, no-arahuaco", "fuente": "lokono", "notas": "Jahn 1927; Way. moderno alijúna; frontera identitaria del grupo", "categoria": "parentesco"},
    # -- LOKONO COMPLETO (Goeje 1928; Brinton 1871; Pet 1987) -- 185 entradas --

    # [ADJETIVOS]
    "firo": {
        "es": "grande, de gran tamaño",
        "fuente": "lokono",
        "notas": "Lok. firo; 'grande'; firo-ka no 'es grande'; firo-bero 'cosa grande = tapir'; Pet 1987",
        "categoria": "adjetivos"
    },
    "hehen": {
        "es": "amarillo",
        "fuente": "lokono",
        "notas": "Lok. hehen; 'amarillo'; hehe-thi 'el amarillo' (nominalización); Pet 1987",
        "categoria": "adjetivos"
    },
    "joho": {
        "es": "muchos, numeroso",
        "fuente": "lokono",
        "notas": "Lok. joho; 'muchos/numeroso'; cuantificador indefinido; Pet 1987",
        "categoria": "adjetivos"
    },
    "mahoro": {
        "es": "blanco, claro",
        "fuente": "lokono",
        "notas": "Lok. mahoro; 'blanco/claro'; raíz *mahoro arahuacana; Goeje 1928",
        "categoria": "adjetivos"
    },
    "maran": {
        "es": "ser pequeño, ser pobre (adjetivo-verbo estativo)",
        "fuente": "lokono",
        "notas": "Lok. maran; 'ser pequeño/pobre'; aparece en topónimos: Marien (Cuba); Brinton 1871",
        "categoria": "adjetivos"
    },
    "nohin": {
        "es": "rojo (forma alternativa)",
        "fuente": "lokono",
        "notas": "Lok. nohin; 'rojo'; cognado Taíno hobin (metal rojizo = oro?); cf. Brinton 1871 = tinte rojo ritual",
        "categoria": "adjetivos"
    },
    "roodi": {
        "es": "rojo, colorado",
        "fuente": "lokono",
        "notas": "Lok. roodi; 'rojo'; raíz arahuacana; Goeje 1928",
        "categoria": "adjetivos"
    },
    "siri": {
        "es": "pequeño, de tamaño reducido",
        "fuente": "lokono",
        "notas": "Lok. siri; 'pequeño'; cf. Wayuu -chi (diminutivo); antónimo de firo; Goeje 1928",
        "categoria": "adjetivos"
    },
    "siwi": {
        "es": "negro, oscuro",
        "fuente": "lokono",
        "notas": "Lok. siwi; 'negro/oscuro'; raíz arahuacana; Goeje 1928",
        "categoria": "adjetivos"
    },
    "wakaijaru": {
        "es": "sin valor, sucio, inútil",
        "fuente": "lokono",
        "notas": "Lok. wakaijaru; 'sin valor/sucio'; cf. Taíno guaoxeri (clase sin rango); Brinton 1871",
        "categoria": "adjetivos"
    },

    # [ALIMENTOS]
    "kasabi": {
        "es": "casabe, pan de yuca",
        "fuente": "lokono",
        "notas": "Lok. kasabi; 'casabe/pan de yuca'; cognado de casabe (caquetío, taíno); raíz *kasabi pan-arahuacana; Goeje 1928",
        "categoria": "alimentos"
    },
    "kasiri": {
        "es": "chicha, bebida fermentada de yuca",
        "fuente": "lokono",
        "notas": "Lok. kasiri; 'chicha/bebida fermentada'; raíz *kasiri pan-arahuacana; cognado en Wayuu kasira; Goeje 1928",
        "categoria": "alimentos"
    },
    "khesia": {
        "es": "comida (nominalización de comer)",
        "fuente": "lokono",
        "notas": "Lok. khesia; 'comida'; nominalización de khin 'comer' con -sia (WH.OBJ); Pet 1987",
        "categoria": "alimentos"
    },
    "khotaha": {
        "es": "carne, presa de caza",
        "fuente": "lokono",
        "notas": "Lok. khotaha; 'carne/presa'; cf. Caq. registro de términos de caza; Pet 1987",
        "categoria": "alimentos"
    },
    "ythysia": {
        "es": "bebida (nominalización de beber)",
        "fuente": "lokono",
        "notas": "Lok. ythysia; 'bebida'; nominalización de ythyn 'beber' con -sia; kathysia 'tener bebida'; Pet 1987",
        "categoria": "alimentos"
    },

    # [COSMOS]
    "adali": {
        "es": "sol (forma alternativa, sin h- prostética)",
        "fuente": "lokono",
        "notas": "Lok. adali; variante de hadali; artículo li [+masc]; cognado de cazi/cali caquetío; *kali (proto-arahuaco); Goeje 1928",
        "categoria": "cosmos"
    },
    "buru": {
        "es": "cielo, firmamento",
        "fuente": "lokono",
        "notas": "Lok. buru; 'cielo/firmamento'; cf. Wayuu seru (cielo); raíz arahuacana *buri; Goeje 1928",
        "categoria": "cosmos"
    },
    "kassahubehu": {
        "es": "el cielo, el día (literalmente: casa del firmamento)",
        "fuente": "lokono",
        "notas": "Lok. kassahu behu; 'el cielo/el día'; kassahu (firmamento) + behu (casa); Brinton 1871",
        "categoria": "cosmos"
    },
    "kassaku": {
        "es": "firmamento, bóveda celeste",
        "fuente": "lokono",
        "notas": "Lok. kassaku; 'firmamento'; de kassan (estar embarazada) — el cielo como vientre cósmico; Brinton 1871",
        "categoria": "cosmos"
    },
    "kolokon": {
        "es": "en el fuego, en la luz (postposición)",
        "fuente": "lokono",
        "notas": "Lok. kolokon; postposición locativa 'en fuego o luz'; hadali kolokon 'en el sol'; Pet 1987",
        "categoria": "cosmos"
    },
    "oni": {
        "es": "lluvia",
        "fuente": "lokono",
        "notas": "Lok. oni; 'lluvia'; raíz *uni arahuacana; cf. oniabo (agua); Goeje 1928",
        "categoria": "cosmos"
    },

    # [CUERPO]
    "akkabu": {
        "es": "mano (forma alternativa, usada en numerales)",
        "fuente": "lokono",
        "notas": "Lok. akkabu; 'mano'; base de abbatekkabe (cinco = una mano); cf. khabo (Pet 1987); Brinton 1871",
        "categoria": "cuerpo"
    },
    "bana": {
        "es": "hígado",
        "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido",
        "notas": "Lok. bana; 'hígado'; bana-ha (forma generalizada); Pet 1987",
        "categoria": "cuerpo"
    },
    "dakuty": {
        "es": "pies, patas",
        "fuente": "lokono",
        "notas": "Lok. dakuty; 'pies'; da- posesivo + kuty; cf. Pet 1987 kothi (pie en compuesto bithi-ka-kothi-bero); Brinton 1871",
        "categoria": "cuerpo"
    },
    "daliroko": {
        "es": "boca",
        "fuente": "lokono",
        "notas": "Lok. daliroko; 'boca'; da- posesivo + liroko; cf. da-eretho (esposa) — da- posesivo 1sg; Brinton 1871",
        "categoria": "cuerpo"
    },
    "dari": {
        "es": "dientes",
        "fuente": "lokono",
        "notas": "Lok. dari; 'dientes'; forma plural inherente; cognado Taíno dari (idéntico); Brinton 1871",
        "categoria": "cuerpo"
    },
    "dyna": {
        "es": "brazo",
        "fuente": "lokono",
        "notas": "Lok. dyna; 'brazo'; da-dyna 'mi brazo'; ada dyna 'rama de árbol (brazo del árbol)'; Pet 1987",
        "categoria": "cuerpo"
    },
    "khabo": {
        "es": "mano",
        "fuente": "lokono",
        "notas": "Lok. khabo; 'mano'; da-khabo 'mi mano'; khabo-ho (forma generalizada); Pet 1987",
        "categoria": "cuerpo"
    },
    "ukku": {
        "es": "corazón, centro vital",
        "fuente": "lokono",
        "notas": "Lok. ukku; 'corazón'; base de ukkurahu (familia) e iikuahu (persona); Brinton 1871",
        "categoria": "cuerpo"
    },
    "ukkurahu2": {
        "es": "pus (secreción del cuerpo enfermo)",
        "fuente": "lokono",
        "notas": "Lok. ukkurahu; segunda acepción: 'pus'; homónimo de 'familia'; raíz ukku (corazón/centro) aplicada al cuerpo enfermo; Brinton 1871",
        "categoria": "cuerpo"
    },
    "wadihy": {
        "es": "oído, oreja",
        "fuente": "lokono",
        "notas": "Lok. wadihy; 'oído/oreja'; wa- posesivo + dihy; Schultz 1800; Brinton 1871",
        "categoria": "cuerpo"
    },
    "wakusi": {
        "es": "ojo",
        "fuente": "lokono",
        "notas": "Lok. wakusi; 'ojo'; wa- posesivo + kusi; Schultz 1800; Brinton 1871",
        "categoria": "cuerpo"
    },
    "waseye": {
        "es": "cabeza",
        "fuente": "lokono",
        "notas": "Lok. waseye; 'cabeza'; wa- = prefijo 'nuestro/mi' + seye; Schultz 1800; Brinton 1871",
        "categoria": "cuerpo"
    },
    "wasiri": {
        "es": "nariz",
        "fuente": "lokono",
        "notas": "Lok. wasiri; 'nariz'; wa- posesivo + siri; Schultz 1800; Brinton 1871",
        "categoria": "cuerpo"
    },
    "yda": {
        "es": "piel, corteza (de árbol)",
        "fuente": "lokono",
        "notas": "Lok. yda; 'piel/corteza'; ada yda 'corteza del árbol'; metáfora piel=corteza pan-arahuacana; Pet 1987",
        "categoria": "cuerpo"
    },

    # [FAUNA]
    "bimiti": {
        "es": "colibrí, picaflor (Trochilidae)",
        "fuente": "lokono",
        "notas": "Lok. bimiti; 'colibrí/picaflor'; contraste con el perezoso trogón en fábula arahuacana; Goeje 1928",
        "categoria": "fauna"
    },
    "bokolawro": {
        "es": "trogón, pájaro sagrado (Trogon viridis)",
        "fuente": "lokono",
        "notas": "Lok. bokolawro; 'trogón' — pájaro sagrado; se sienta de espaldas al comer (tabú); Goeje 1928",
        "categoria": "fauna"
    },
    "firobero": {
        "es": "tapir, danta (literalmente: la cosa grande)",
        "fuente": "lokono",
        "notas": "Lok. firo-bero; 'tapir' (lit. 'cosa grande'); derivado de firo + -bero nominalizador NH; Pet 1987",
        "categoria": "fauna"
    },
    "foro": {
        "es": "pájaro, ave (forma alternativa)",
        "fuente": "lokono",
        "notas": "Lok. foro; 'pájaro/ave'; forma alternativa de kodibio en dialectos del Demerara; Brinton 1871; Goeje 1928",
        "categoria": "fauna"
    },
    "hikolhi": {
        "es": "tortuga (animal de buen augurio)",
        "fuente": "lokono",
        "notas": "Lok. hikolhi; 'tortuga'; tratado como [+masc] por ser animal apreciado; Goeje 1928; Pet 1987",
        "categoria": "fauna"
    },
    "itime": {
        "es": "pez, pescado",
        "fuente": "lokono",
        "notas": "Lok. itime; 'pez/pescado'; singular y plural idénticos; raíz arahuacana; Brinton 1871",
        "categoria": "fauna"
    },
    "jawade": {
        "es": "zarigüeya, zorro chucha (Didelphis marsupialis)",
        "fuente": "lokono",
        "notas": "Lok. jawade; 'zarigüeya/opossum'; protagonista de fábula 'La tortuga y la zarigüeya'; Goeje 1928",
        "categoria": "fauna"
    },
    "kabadaro": {
        "es": "jaguar, yaguareté",
        "fuente": "lokono",
        "notas": "Lok. kabadaro; 'jaguar'; artículo li [+masc fuerte]; préstamo del caribe insular en Lokono; Goeje 1928; Pet 1987",
        "categoria": "fauna"
    },
    "kodibio": {
        "es": "pájaro (forma genérica)",
        "fuente": "lokono",
        "notas": "Lok. kodibio; 'pájaro'; to kodibio; to kodibio-be 'los pájaros'; Pet 1987",
        "categoria": "fauna"
    },
    "mabberie": {
        "es": "mosca, moscas de carroña",
        "fuente": "lokono",
        "notas": "Lok. mabberie; 'mosca/moscas'; mabberie-ron 'solo moscas'; plural inherente; Goeje 1928",
        "categoria": "fauna"
    },
    "makowa": {
        "es": "animal (genérico)",
        "fuente": "lokono",
        "notas": "Lok. makowa; 'animal (genérico)'; makowa-ron 'animales (con postposición)'; Goeje 1928",
        "categoria": "fauna"
    },

    # [FLORA]
    "achi": {
        "es": "ají, pimienta (Capsicum sp.)",
        "fuente": "lokono",
        "notas": "Lok. achi; 'ají/pimienta'; raíz *achi arahuacana universal; venezolanismo ají del mismo origen; Brinton 1871",
        "categoria": "flora"
    },
    "baikya": {
        "es": "fruta, fruto maduro",
        "fuente": "lokono",
        "notas": "Lok. baikya; 'fruta/fruto'; baikya-da 'fruta caída'; contexto alimenticio arahuacano; Goeje 1928",
        "categoria": "flora"
    },
    "hobo": {
        "es": "jobillo, ciruela de huesito (Spondias lutea)",
        "fuente": "lokono",
        "notas": "Lok. hobo; 'Spondias lutea' (ciruela tropical); árbol del cuento 'La tortuga y la zarigüeya'; Goeje 1928",
        "categoria": "flora"
    },
    "iuli": {
        "es": "tabaco (Nicotiana tabacum)",
        "fuente": "lokono",
        "notas": "Lok. iuli; 'tabaco'; planta ritual arahuacana; venezolanismo 'tabaco' via Taíno/arahuacano; Brinton 1871",
        "categoria": "flora"
    },
    "karowa": {
        "es": "maguey, cabuya, agave (Agave sp.)",
        "fuente": "lokono",
        "notas": "Lok. karowa; 'agave/maguey'; planta de fibra; en texto 'karowa otoro' = pie/base del agave; Goeje 1928",
        "categoria": "flora"
    },
    "malhisi": {
        "es": "maíz (forma alternativa Surinam)",
        "fuente": "lokono",
        "notas": "Lok. malhisi; 'maíz' (dialectal Surinam/Guyana); cf. mariti; Pet 1987",
        "categoria": "flora"
    },
    "mariti": {
        "es": "maíz (Zea mays)",
        "fuente": "lokono",
        "notas": "Lok. mariti; 'maíz'; cf. mazato (chicha de maíz, Caq.); raíz *maiti arahuacana; Brinton 1871",
        "categoria": "flora"
    },
    "yuka": {
        "es": "yuca, mandioca (Manihot esculenta)",
        "fuente": "lokono",
        "notas": "Lok. yuka; 'yuca/mandioca'; raíz *yuka pan-arahuacana; venezolanismo 'yuca' de este origen; Goeje 1928",
        "categoria": "flora"
    },

    # [GEOGRAFIA]
    "boro": {
        "es": "aldea, pueblo, asentamiento",
        "fuente": "lokono",
        "notas": "Lok. boro; 'aldea/asentamiento arahuacano'; cf. topónimos Venezuela con -boro/-buro; Goeje 1928",
        "categoria": "geografia"
    },
    "erne": {
        "es": "desembocadura de río, frente de costa",
        "fuente": "lokono",
        "notas": "Lok. erne / uime; 'desembocadura de río/frente de costa'; cognado Taíno cimu/simu; Brinton 1871",
        "categoria": "geografia"
    },
    "kabojan": {
        "es": "conuco, milpa, terreno de cultivo",
        "fuente": "lokono",
        "notas": "Lok. kabojan; 'conuco/terreno de cultivo'; ly-kabojan 'su conuco'; cognado del caquetío 'conuco' (del arahuacano); Pet 1987",
        "categoria": "geografia"
    },
    "kairi": {
        "es": "isla, territorio insular",
        "fuente": "lokono",
        "notas": "Lok. kairi; 'isla'; raíz *kairi pan-arahuacana; topónimo Trinidad (Cairi caquetío); Brinton 1871",
        "categoria": "geografia"
    },
    "oniabo": {
        "es": "agua, cuerpo de agua",
        "fuente": "lokono",
        "notas": "Lok. oniabo; artículo to [NH]; forma compleja oni+abo; cf. Lok. tuna (río); Brinton 1871; Goeje 1928",
        "categoria": "geografia"
    },
    "ori": {
        "es": "cerro, colina, montaña",
        "fuente": "lokono",
        "notas": "Lok. ori; 'cerro/colina'; raíz arahuacana *ari montaña; cf. Oriente en topónimos; Goeje 1928",
        "categoria": "geografia"
    },
    "sallaban": {
        "es": "sabana, llanura (terreno plano y liso)",
        "fuente": "lokono",
        "notas": "Lok. sallaban; 'llano/sabana'; cognado Taíno sabana; origen del venezolanismo/americanismo 'sabana'; Brinton 1871",
        "categoria": "geografia"
    },
    "siba": {
        "es": "piedra, roca",
        "fuente": "lokono",
        "notas": "Lok. siba; artículo to [NH]; siba-be 'piedras'; cognado con iba/kiba (Carib.); Brinton 1871; Goeje 1928",
        "categoria": "geografia"
    },

    # [GRAMATICA]
    "aba": {
        "es": "uno, un (numeral y artículo indefinido)",
        "fuente": "lokono",
        "notas": "Lok. aba; 'uno/un'; aba sikoa 'una casa'; aba-li 'un hombre'; cognado *aba pan-arahuacano; Pet 1987",
        "categoria": "gramatica"
    },
    "abbalukku": {
        "es": "veinte (literalmente: un hombre = manos y pies)",
        "fuente": "lokono",
        "notas": "Lok. abba lukku; 'veinte'; abba (uno) + lukku (hombre = 20 dedos); numeral vigesimal arahuacano; Brinton 1871",
        "categoria": "gramatica"
    },
    "abbatekkabe": {
        "es": "cinco (literalmente: una mano = abba + akkabu)",
        "fuente": "lokono",
        "notas": "Lok. abbatekkabe; 'cinco'; compuesto de abba (uno) + akkabu (mano); sistema vigesimal arahuacano; Brinton 1871",
        "categoria": "gramatica"
    },
    "abon": {
        "es": "debajo de, bajo (postposición locativa inferior)",
        "fuente": "lokono",
        "notas": "Lok. abon; 'debajo de/bajo'; hobo abon 'bajo el árbol de jobillo'; postposición espacial inferior; Goeje 1928",
        "categoria": "gramatica"
    },
    "aijumun": {
        "es": "arriba, en lo alto (adverbio espacial vertical)",
        "fuente": "lokono",
        "notas": "Lok. aijumun; 'arriba/en lo alto'; cognado Taíno huilio (altura); base de Adajali 'Dios' (ajomyn-thi); Brinton 1871",
        "categoria": "gramatica"
    },
    "alikan": {
        "es": "quién (interrogativo)",
        "fuente": "lokono",
        "notas": "Lok. alikan; 'quién'; interrogativo de persona [+humano]; Pet 1987",
        "categoria": "gramatica"
    },
    "annakan": {
        "es": "centro, punto medio (concepto espacial)",
        "fuente": "lokono",
        "notas": "Lok. annakan; 'centro/punto medio'; cognado Taíno nacan; Cubanacan = kuba+annakan (centro del pasado); Brinton 1871",
        "categoria": "gramatica"
    },
    "be": {
        "es": "sufijo plural general (-be)",
        "fuente": "lokono",
        "notas": "Lok. -be; sufijo plural [+/-humano]; siba-be 'piedras'; wadili-be 'hombres (grupo)'; Pet 1987",
        "categoria": "gramatica"
    },
    "bi": {
        "es": "tú (pronombre libre 2sg)",
        "fuente": "lokono",
        "notas": "Lok. bi; '2SG pronombre libre'; by- como prefijo verbal/posesivo; Pet 1987",
        "categoria": "gramatica"
    },
    "biama": {
        "es": "dos (forma Brinton 1871, variante de bian)",
        "fuente": "lokono",
        "notas": "Lok. biama; 'dos'; biamannu 'dos (plural)'; cf. bian (Pet 1987); Brinton 1871",
        "categoria": "gramatica"
    },
    "biamantekabbe": {
        "es": "diez (literalmente: dos manos = biama + akkabu)",
        "fuente": "lokono",
        "notas": "Lok. biamantekabbe; 'diez'; compuesto de biama (dos) + akkabu (manos); base del sistema vigesimal; Brinton 1871",
        "categoria": "gramatica"
    },
    "bian": {
        "es": "dos (numeral)",
        "fuente": "lokono",
        "notas": "Lok. bian; 'dos'; bian sikoa 'dos casas'; bian-ninon 'dos personas'; Pet 1987",
        "categoria": "gramatica"
    },
    "bibiti": {
        "es": "cuatro (forma Brinton 1871, variante de bithi)",
        "fuente": "lokono",
        "notas": "Lok. bibiti; 'cuatro'; bibitinu 'cuatro (plural)'; cf. bithi (Pet 1987); Brinton 1871",
        "categoria": "gramatica"
    },
    "biinasufix": {
        "es": "sufijo de pasado próximo (-biina: ayer)",
        "fuente": "lokono",
        "notas": "Lok. -biina; sufijo verbal de pasado próximo (ayer); dayahaddibiina 'caminé ayer'; Brinton 1871",
        "categoria": "gramatica"
    },
    "bisufix": {
        "es": "sufijo de pasado reciente (-bi: hoy)",
        "fuente": "lokono",
        "notas": "Lok. -bi; sufijo verbal de pasado reciente (hoy); dayahaddibi 'caminé hoy'; Brinton 1871",
        "categoria": "gramatica"
    },
    "bithi": {
        "es": "cuatro (numeral)",
        "fuente": "lokono",
        "notas": "Lok. bithi; 'cuatro'; bithi hiaro-non 'cuatro mujeres'; bithi-ka-kothi-bero 'cuadrúpedo = auto'; Pet 1987",
        "categoria": "gramatica"
    },
    "bo": {
        "es": "sufijo continuativo / presente progresivo (-bo)",
        "fuente": "lokono",
        "notas": "Lok. -bo; 'continuativo/progresivo'; li wadili dalhida-bo 'el hombre está corriendo'; Pet 1987",
        "categoria": "gramatica"
    },
    "bute": {
        "es": "ahora (marcador de presente inmediato)",
        "fuente": "lokono",
        "notas": "Lok. bute; 'ahora'; marcador de tiempo presente en Actos 14:11 (texto Lokono de 1799); Brinton 1871",
        "categoria": "gramatica"
    },
    "dduria": {
        "es": "que, más que (partícula comparativa)",
        "fuente": "lokono",
        "notas": "Lok. dduria; 'que/más que'; Bokkia ussó dduria = 'tú eres mejor que yo'; Brinton 1871",
        "categoria": "gramatica"
    },
    "de": {
        "es": "yo (pronombre libre 1sg)",
        "fuente": "lokono",
        "notas": "Lok. de; '1SG pronombre libre'; da- como prefijo verbal/posesivo; de bode 'mi anzuelo'; Pet 1987",
        "categoria": "gramatica"
    },
    "diako": {
        "es": "encima de, sobre (postposición de superficie superior)",
        "fuente": "lokono",
        "notas": "Lok. diako; 'encima de/sobre'; postposición que requiere referente con superficie; Pet 1987",
        "categoria": "gramatica"
    },
    "doma": {
        "es": "porque, a causa de (postposición causal)",
        "fuente": "lokono",
        "notas": "Lok. doma; 'porque/a causa de'; li doma da-fatadoa 'a causa de él me golpearon'; Pet 1987",
        "categoria": "gramatica"
    },
    "fa": {
        "es": "sufijo de futuro (-fa/-ha)",
        "fuente": "lokono",
        "notas": "Lok. -fa/-ha; 'futuro'; l-osy-fa 'él irá'; da-siki-fa 'yo daré'; Pet 1987",
        "categoria": "gramatica"
    },
    "hibin": {
        "es": "ya, de ya (aspecto completivo)",
        "fuente": "lokono",
        "notas": "Lok. hibin; 'ya'; marcador de completitud/aspecto; Pet 1987",
        "categoria": "gramatica"
    },
    "jon": {
        "es": "allá, allí (adverbio demostrativo distal)",
        "fuente": "lokono",
        "notas": "Lok. jon; 'allá/allí'; marcador deíctico de lugar distal; Pet 1987",
        "categoria": "gramatica"
    },
    "kabbuhin": {
        "es": "tres (forma Brinton 1871, variante de kabyn)",
        "fuente": "lokono",
        "notas": "Lok. kabbuhin; 'tres'; kabbuhinihnu 'tres (plural)'; cf. kabyn (Pet 1987); Brinton 1871",
        "categoria": "gramatica"
    },
    "kabyn": {
        "es": "tres (numeral)",
        "fuente": "lokono",
        "notas": "Lok. kabyn; 'tres'; kabyn wadili-non 'tres hombres'; Pet 1987",
        "categoria": "gramatica"
    },
    "ken": {
        "es": "y (conjunción copulativa)",
        "fuente": "lokono",
        "notas": "Lok. ken; 'y'; conjunción coordinante; Pet 1987",
        "categoria": "gramatica"
    },
    "kho": {
        "es": "no, negación (partícula negativa)",
        "fuente": "lokono",
        "notas": "Lok. kho; 'no/negación'; partícula negativa verbal; Pet 1987",
        "categoria": "gramatica"
    },
    "khonan": {
        "es": "sobre, acerca de, de (postposición temática)",
        "fuente": "lokono",
        "notas": "Lok. khonan; 'sobre/acerca de/de'; na-mithada-fa da-khonan 'se burlarán de mí'; Pet 1987",
        "categoria": "gramatica"
    },
    "kijadoma": {
        "es": "por eso, por tanto, por esa razón",
        "fuente": "lokono",
        "notas": "Lok. kijadoma; 'por eso/por tanto'; conector causal discursivo; cf. doma (postposición causal); Goeje 1928",
        "categoria": "gramatica"
    },
    "koana": {
        "es": "sufijo nominalizador instrumental: cosa que hace X (-koana)",
        "fuente": "lokono",
        "notas": "Lok. -koana; nominalizador instrumental 'cosa que hace X'; dalhidi-koana 'vehículo'; da-dalhidi-koana 'mi auto'; Pet 1987",
        "categoria": "gramatica"
    },
    "kuba": {
        "es": "signo de tiempo pasado (prefijo/sufijo temporal)",
        "fuente": "lokono",
        "notas": "Lok. kuba-/-kuba; 'tiempo pasado indefinido'; dayahaddakuba 'yo caminé (hace tiempo)'; Brinton 1871",
        "categoria": "gramatica"
    },
    "lhin": {
        "es": "sufijo de agente habitual / profesión (-lhin)",
        "fuente": "lokono",
        "notas": "Lok. -lhin; nominalizador agentivo habitual; borata-lhin 'el que salva'; jokara-lhin 'vendedor'; Pet 1987",
        "categoria": "gramatica"
    },
    "li": {
        "es": "artículo masculino humano (3sg masc)",
        "fuente": "lokono",
        "notas": "Lok. li; artículo [+masc +humano]; li wadili 'el hombre'; ly- como prefijo verbal; Pet 1987",
        "categoria": "gramatica"
    },
    "liko": {
        "es": "nuestro (posesivo 1pl, poseído)",
        "fuente": "lokono",
        "notas": "Lok. liko- / wa-; '1PL posesivo'; wa-karobo 'nuestro plato'; wa-kali 'nuestra casa'; Pet 1987",
        "categoria": "gramatica"
    },
    "loko": {
        "es": "dentro de (postposición interior para objetos huecos/sólidos)",
        "fuente": "lokono",
        "notas": "Lok. loko; 'dentro de'; postposición de clase espacial: hueco/sólido; Pet 1987",
        "categoria": "gramatica"
    },
    "ma": {
        "es": "prefijo privativo: sin, carente de (ma-)",
        "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido",
        "notas": "Lok. ma-; prefijo privativo 'sin/carente'; ma-bolheidi-n 'no tirar'; antónimo de ka-; Pet 1987",
        "categoria": "gramatica"
    },
    "myn": {
        "es": "a, para (postposición benefactiva/direccional)",
        "fuente": "lokono",
        "notas": "Lok. myn; 'a/para'; da-siki-fa no thy-myn 'yo se lo daré a ella'; ly-myn 'a él'; Pet 1987",
        "categoria": "gramatica"
    },
    "non": {
        "es": "sufijo plural humano (-non)",
        "fuente": "lokono",
        "notas": "Lok. -non; sufijo plural [+humano]; kakythi-non 'hombres'; ibili-non 'niños'; Pet 1987",
        "categoria": "gramatica"
    },
    "nro": {
        "es": "hacia (sufijo direccional -nro)",
        "fuente": "lokono",
        "notas": "Lok. -nro; 'hacia'; da-sika-fa no bahy-nro 'la llevaré hacia casa'; Pet 1987",
        "categoria": "gramatica"
    },
    "oma": {
        "es": "con (postposición comitativa: en compañía de)",
        "fuente": "lokono",
        "notas": "Lok. oma; 'con (acompañamiento)'; li fara-fa to kabadaro oma 'él peleará con el jaguar'; Pet 1987",
        "categoria": "gramatica"
    },
    "sia": {
        "es": "sufijo relativizador de objeto (-sia)",
        "fuente": "lokono",
        "notas": "Lok. -sia; WH.OBJ relativizador; khin→khesia 'comida'; ythyn→ythysia 'bebida'; Pet 1987",
        "categoria": "gramatica"
    },
    "thi": {
        "es": "sufijo relativizador de sujeto masculino (-thi)",
        "fuente": "lokono",
        "notas": "Lok. -thi; WH.SUBJ relativizador [+masc]; li wadili dykha-thi 'el hombre que vio'; kaky-thi 'el que vive = hombre'; Pet 1987",
        "categoria": "gramatica"
    },
    "to": {
        "es": "artículo no-masculino / no-humano (3sg NM/NH)",
        "fuente": "lokono",
        "notas": "Lok. to; artículo [NM/NH]; to hiaro 'la mujer'; to oniabo 'el agua'; thy- como prefijo verbal; Pet 1987",
        "categoria": "gramatica"
    },
    "waja": {
        "es": "solo, por sí mismo (sufijo reflexivo -waja)",
        "fuente": "lokono",
        "notas": "Lok. -waja; 'reflexivo/solo'; ly-soka ly-waja 'él se cortó solo'; influencia holandés/sranan tongo en Surinam; Pet 1987",
        "categoria": "gramatica"
    },
    "we": {
        "es": "nosotros (pronombre libre 1pl)",
        "fuente": "lokono",
        "notas": "Lok. we; '1PL pronombre libre'; wa- como prefijo verbal/posesivo; wa-karobo-n 'nuestro plato'; Pet 1987",
        "categoria": "gramatica"
    },

    # [JERARQUIA]
    "diakothi": {
        "es": "jefe, el que está encima (título)",
        "fuente": "lokono",
        "notas": "Lok. diakothi; 'jefe' (lit. 'el que está encima'); diako (encima) + -thi (agent masc); cf. Caq. cacique; Goeje 1928",
        "categoria": "jerarquia"
    },
    "kasikoali": {
        "es": "dueño, propietario (literalmente: el que tiene casa)",
        "fuente": "lokono",
        "notas": "Lok. kasikoali; 'dueño/propietario'; de kasikoa (ka- + sikoa) + -li [+masc agentivo]; Pet 1987",
        "categoria": "jerarquia"
    },
    "kassiquan": {
        "es": "ser dueño de casa; de donde viene 'cacique'",
        "fuente": "lokono",
        "notas": "Lok. kassiquan; 'ser dueño de casa'; de ussequa/iissiqua (casa); origen del Taíno casique → español cacique; Brinton 1871",
        "categoria": "jerarquia"
    },

    # [PARENTESCO]
    "ahati": {
        "es": "compañero, aliado, amigo ceremonial",
        "fuente": "lokono",
        "notas": "Lok. ahati; 'compañero/aliado'; cf. guaitiao (ritual de amistad interétnica caquetío); Brinton 1871",
        "categoria": "parentesco"
    },
    "aithi": {
        "es": "hijo (término de parentesco inalienable)",
        "fuente": "lokono",
        "notas": "Lok. aithi; 'hijo'; l-aithi 'su hijo'; inalienable — siempre posesivo; Pet 1987",
        "categoria": "parentesco"
    },
    "bokithi": {
        "es": "hermano mayor (visto por el menor)",
        "fuente": "lokono",
        "notas": "Lok. bokithi; 'hermano mayor'; da-bokithi 'mi hermano mayor'; Pet 1987",
        "categoria": "parentesco"
    },
    "dalli": {
        "es": "padre (mi padre, forma poseída)",
        "fuente": "lokono",
        "notas": "Lok. dalli; 'mi padre'; da-thi (forma morfológica); cf. Brinton 1871 ilta/dalli; cognado con tata (Caq.); Brinton 1871",
        "categoria": "parentesco"
    },
    "eretho": {
        "es": "esposa (término inalienable)",
        "fuente": "lokono",
        "notas": "Lok. eretho; 'esposa'; da-eretho 'mi esposa'; inalienable, siempre posesivo; Pet 1987",
        "categoria": "parentesco"
    },
    "eyeri": {
        "es": "hombres arahuacanos isleños (etnónimo caribeño)",
        "fuente": "lokono",
        "notas": "Lok. eyeri; 'hombres arahuacanos isleños'; base de Siboneyes (siba+eyeri = 'hombres de las rocas'); Brinton 1871",
        "categoria": "parentesco"
    },
    "falhetho": {
        "es": "forastero blanco, europeo (literalmente: hombre de otro tipo)",
        "fuente": "lokono",
        "notas": "Lok. falhetho; 'hombre blanco/europeo'; [+masc -humano=arahuacano]; cf. alijuna (Wayuu para no-arahuacano); Pet 1987",
        "categoria": "parentesco"
    },
    "hiaro": {
        "es": "mujer, hembra (forma genérica de sexo femenino)",
        "fuente": "lokono",
        "notas": "Lok. hiaro; 'mujer/hembra'; to hiaro 'la mujer'; [NM]; también para animales hembras; Pet 1987",
        "categoria": "parentesco"
    },
    "ibili": {
        "es": "niño, infante (sin distinción de género)",
        "fuente": "lokono",
        "notas": "Lok. ibili; 'niño/infante'; ibili-non 'niños'; tratado como [+human] independiente del grupo; Pet 1987",
        "categoria": "parentesco"
    },
    "iikuahu": {
        "es": "persona (literalmente: aquel cuyo corazón late)",
        "fuente": "lokono",
        "notas": "Lok. iikuahu; 'persona'; de ukku (corazón); lit. 'one whose heart beats'; concepto arahuacano de persona; Brinton 1871",
        "categoria": "parentesco"
    },
    "itti": {
        "es": "padre (forma atestiguada 1800, Schultz)",
        "fuente": "lokono",
        "notas": "Lok. itti; 'padre'; datti 'mi padre'; cf. pilplii (De Laet 1598); cognado Taíno taita; Brinton 1871",
        "categoria": "parentesco"
    },
    "kakythi": {
        "es": "hombre adulto arahuacano",
        "fuente": "lokono",
        "notas": "Lok. kakythi; 'hombre adulto' [+masc +human]; kakythi-non 'los hombres'; base de kakythinon 'pueblo'; Taylor 1977; Pet 1987",
        "categoria": "parentesco"
    },
    "kakythinon": {
        "es": "pueblo, gente arahuacana",
        "fuente": "lokono",
        "notas": "Lok. kakythinon; 'pueblo/gente'; na kakythinon 'la gente'; plural de kakythi; cognado posible con 'caquetío'; Pet 1987",
        "categoria": "parentesco"
    },
    "kubakanan": {
        "es": "antepasados, ancestros",
        "fuente": "lokono",
        "notas": "Lok. kubakanan; 'antepasados/ancestros'; kuba- (tiempo pasado) + annakan (centro); lit. 'los del centro pasado'; Brinton 1871",
        "categoria": "parentesco"
    },
    "lokono": {
        "es": "persona arahuaca, miembro del pueblo Lokono",
        "fuente": "lokono",
        "notas": "Lok. lokono; autónimo arahuacano 'persona/gente nuestra'; base del étnico Lokono/Arawak; cognado con kakythi; Goeje 1928",
        "categoria": "parentesco"
    },
    "lukku": {
        "es": "hombre, persona arahuacana (autónimo masculino)",
        "fuente": "lokono",
        "notas": "Lok. lukku; 'hombre/persona'; lukkunu 'el pueblo Lokono'; Lucayos = lukku+kairi 'hombres de las islas'; Brinton 1871",
        "categoria": "parentesco"
    },
    "lukkunu": {
        "es": "el pueblo Lokono (autónimo colectivo)",
        "fuente": "lokono",
        "notas": "Lok. lukkunu; autónimo colectivo 'nosotros los hombres'; cf. lokono; Brinton 1871: 'They call themselves simply lukkunu, men'",
        "categoria": "parentesco"
    },
    "okithi": {
        "es": "hermano menor (visto por el mayor)",
        "fuente": "lokono",
        "notas": "Lok. okithi; 'hermano menor' [+masc]; d-okithi 'mi hermano menor'; Pet 1987",
        "categoria": "parentesco"
    },
    "okitho": {
        "es": "hermana menor (vista por la mayor)",
        "fuente": "lokono",
        "notas": "Lok. okitho; 'hermana menor' [NM]; d-okitho 'mi hermana menor'; Pet 1987",
        "categoria": "parentesco"
    },
    "pilplii": {
        "es": "padre (forma arcaica, De Laet 1598)",
        "fuente": "lokono",
        "notas": "Lok. pilplii; 'padre' (forma más antigua, De Laet ca.1598); cf. itti (Schultz 1800); Brinton 1871",
        "categoria": "parentesco"
    },
    "rethi": {
        "es": "esposo (término inalienable)",
        "fuente": "lokono",
        "notas": "Lok. rethi; 'esposo'; da-rethi 'mi esposo'; inalienable, siempre posesivo; Pet 1987",
        "categoria": "parentesco"
    },
    "uju": {
        "es": "madre",
        "fuente": "lokono",
        "notas": "Lok. uju; 'madre'; daiju 'mi madre'; waijunattu 'nuestra madre'; Brinton 1871; cf. De Laet saeckee (1598)",
        "categoria": "parentesco"
    },
    "ukkurahu": {
        "es": "familia, tribu, grupo de origen común",
        "fuente": "lokono",
        "notas": "Lok. ukkurahu; 'familia/tribu'; de ukku (corazón) + rahu (sufijo colectivo?); Brinton 1871",
        "categoria": "parentesco"
    },
    "wadili": {
        "es": "hombre, varón (forma genérica de sexo masculino)",
        "fuente": "lokono",
        "notas": "Lok. wadili; 'hombre/varón'; li wadili 'el hombre'; [+masc]; también para animales machos; Pet 1987",
        "categoria": "parentesco"
    },
    "wakili": {
        "es": "persona, ser humano (forma arcaica de lokono)",
        "fuente": "lokono",
        "notas": "Lok. wakili; 'persona/ser humano'; wakili-be 'personas'; forma arcaica en cuentos; cf. lokono (autónimo moderno); Goeje 1928",
        "categoria": "parentesco"
    },

    # [RITUAL]
    "Adajali": {
        "es": "Dios, ser supremo (literalmente: el que vive arriba)",
        "fuente": "lokono",
        "notas": "Lok. Adajali; 'Dios/ser supremo'; de ajomyn-thi 'el que es alto'; Adajali boko = 'libro de Dios/Biblia'; Pet 1987",
        "categoria": "ritual"
    },
    "akkicyaha": {
        "es": "espíritu del ser vivo (alma vital)",
        "fuente": "lokono",
        "notas": "Lok. akkicyaha; 'espíritu del ser vivo'; cognado Taíno goeiz (espíritu personal); concepto arahuacano del alma; Brinton 1871",
        "categoria": "ritual"
    },
    "akkuyaha": {
        "es": "seres vivos; máscaras rituales que los representan",
        "fuente": "lokono",
        "notas": "Lok. akkuyaha; 'seres vivos / máscaras rituales'; cognado Taíno guayzas; Brinton 1871",
        "categoria": "ritual"
    },
    "alla": {
        "es": "banco, asiento ceremonial (símbolo de autoridad)",
        "fuente": "lokono",
        "notas": "Lok. alla; 'banco/asiento ceremonial'; d-alla-nnijawa 'mi propio banco'; signo de distinción social arahuacano; Goeje 1928",
        "categoria": "ritual"
    },
    "ansi": {
        "es": "fuerza vital, energía de vida",
        "fuente": "lokono",
        "notas": "Lok. ansi; 'fuerza vital/energía'; tata-ansi 'recuperar fuerza'; cf. concepto arahuacano de anima; Goeje 1928",
        "categoria": "ritual"
    },
    "dulluhu": {
        "es": "asiento bajo ceremonial (hahlah)",
        "fuente": "lokono",
        "notas": "Lok. dulluhu/durruhu; 'asiento bajo ceremonial'; cognado Taíno duhos; usado por piaye/piai en rituales; Brinton 1871",
        "categoria": "ritual"
    },
    "haikahu": {
        "es": "muerte, lo que pasa",
        "fuente": "lokono",
        "notas": "Lok. haikahu; 'muerte'; de haikaikan 'pasar/transcurrir'; auhakit 'matrimonio' (la muchacha ha pasado); Brinton 1871",
        "categoria": "ritual"
    },
    "piayeman": {
        "es": "curandero aprendiz, asistente del chamán",
        "fuente": "lokono",
        "notas": "Lok. piayeman; derivado de piaye (chamán); forma con sufijo de agente -man; Goeje 1928",
        "categoria": "ritual"
    },
    "semett": {
        "es": "sacerdote, adivino, hechicero (espiritu ritual)",
        "fuente": "lokono",
        "notas": "Lok. semett; 'sacerdote/adivino/hechicero'; cognado Taíno semi (divinidades/espíritus); Brinton 1871",
        "categoria": "ritual"
    },
    "una": {
        "es": "tinte negro (de una planta específica)",
        "fuente": "lokono",
        "notas": "Lok. una; 'tinte negro'; de donde laimatun 'teñir de negro'; uso ritual en pintura corporal arahuacana; Brinton 1871",
        "categoria": "ritual"
    },

    # [SENTIMIENTOS]
    "hammusia": {
        "es": "hambre, estado de inanición",
        "fuente": "lokono",
        "notas": "Lok. hammusia; 'hambre'; cf. Pet 1987 fonasia 'to be hungry'; Goeje 1928",
        "categoria": "sentimientos"
    },

    # [TIEMPO]
    "kasakabo": {
        "es": "día (unidad de tiempo)",
        "fuente": "lokono",
        "notas": "Lok. kasakabo; 'día'; kasakabo-be 'días' (plural NH); joho kasakabo 'muchos días'; Goeje 1928",
        "categoria": "tiempo"
    },
    "mothi": {
        "es": "mañana (tiempo futuro próximo)",
        "fuente": "lokono",
        "notas": "Lok. mothi; 'mañana'; adverbio temporal; Pet 1987",
        "categoria": "tiempo"
    },

    # [UTILES]
    "anikho": {
        "es": "pertenencias, bienes personales",
        "fuente": "lokono",
        "notas": "Lok. anikho; 'pertenencias/bienes'; d-anikho 'mis pertenencias'; inalienable; Pet 1987",
        "categoria": "utiles"
    },
    "barrahakoa": {
        "es": "barbacoa, lugar de almacenamiento de provisiones",
        "fuente": "lokono",
        "notas": "Lok. barrahakoa; lit. 'lugar donde se guarda comida'; origen del venezolanismo/americanismo 'barbacoa'; Brinton 1871",
        "categoria": "utiles"
    },
    "bode": {
        "es": "anzuelo de pesca",
        "fuente": "lokono",
        "notas": "Lok. bode; 'anzuelo'; bode-he (forma generalizada); de bode 'mi anzuelo'; da-bode-da-bo 'estoy pescando'; Pet 1987",
        "categoria": "utiles"
    },
    "habba": {
        "es": "cesta, canasto, cestería",
        "fuente": "lokono",
        "notas": "Lok. habba; 'cesta/canasto'; cognado Taíno haba; artesanía arahuacana de fibra vegetal; Brinton 1871",
        "categoria": "utiles"
    },
    "kaly": {
        "es": "casa (forma poseída: nu-kali = mi casa)",
        "fuente": "lokono",
        "notas": "Lok. kaly/kali; 'casa (poseída)'; nu-kali 'mi casa'; forma poseída de sikoa; Goeje 1928; Brinton 1871",
        "categoria": "utiles"
    },
    "semaara": {
        "es": "flecha",
        "fuente": "lokono",
        "notas": "Lok. semaara; 'flecha'; cf. Caq. saeta/flecha (registros coloniales); Brinton 1871",
        "categoria": "utiles"
    },

    # [VERBOS]
    "adija": {
        "es": "hablar, decir; palabra, discurso",
        "fuente": "lokono",
        "notas": "Lok. adija; 'hablar/decir'; adija-kien 'habló de nuevo'; cf. dian (otra raíz para hablar); Goeje 1928",
        "categoria": "verbos"
    },
    "andyn": {
        "es": "llegar, arribar",
        "fuente": "lokono",
        "notas": "Lok. andyn; 'llegar/arribar'; andyn vs. andan 'tocar/sentir' (par básico/a-stem); Pet 1987",
        "categoria": "verbos"
    },
    "aparrun": {
        "es": "matar (forma alternativa)",
        "fuente": "lokono",
        "notas": "Lok. aparrun; 'matar'; apparahun 'muerto'; cognado Taíno operito (muerto); cf. faryn (Pet 1987); Brinton 1871",
        "categoria": "verbos"
    },
    "aririn": {
        "es": "nombrar, recitar; cantar ritualmente",
        "fuente": "lokono",
        "notas": "Lok. aririn; 'nombrar/recitar/cantar'; cognado Taíno areito (canto ritual ceremonial); Brinton 1871",
        "categoria": "verbos"
    },
    "awothiki": {
        "es": "encontrar, hallar",
        "fuente": "lokono",
        "notas": "Lok. awothiki; 'encontrar/hallar'; awothiki-ren baikya 'encontró fruto'; Goeje 1928",
        "categoria": "verbos"
    },
    "ayahaddin": {
        "es": "caminar, andar",
        "fuente": "lokono",
        "notas": "Lok. ayahaddin; 'caminar/andar'; paradigma verbal completo en Brinton 1871; cf. osyn (ir); Brinton 1871",
        "categoria": "verbos"
    },
    "baleta": {
        "es": "querer sentarse, desear (verbo desiderativo)",
        "fuente": "lokono",
        "notas": "Lok. baleta; 'querer sentarse/desear'; baleta-ti-rro 'solo quiero sentarme'; sufijo desiderativo -ti; Goeje 1928",
        "categoria": "verbos"
    },
    "bokon": {
        "es": "cocinar, hervir",
        "fuente": "lokono",
        "notas": "Lok. bokon; 'cocinar/hervir'; bokonoa 'ser cocinado/hervirse' (pasivo/reflexivo); Pet 1987",
        "categoria": "verbos"
    },
    "boratyn": {
        "es": "ayudar, salvar",
        "fuente": "lokono",
        "notas": "Lok. boratyn; 'ayudar/salvar'; borata-lhin 'el que ayuda/salvado'; sufijo habitual -lhin; Pet 1987",
        "categoria": "verbos"
    },
    "dian": {
        "es": "hablar, decir",
        "fuente": "lokono",
        "notas": "Lok. dian; 'hablar/decir'; dia-thi 'hablante' (agent nominalizer -thi); Lokono Dian = 'habla Lokono'; Pet 1987",
        "categoria": "verbos"
    },
    "dykhyn": {
        "es": "ver, percibir visualmente",
        "fuente": "lokono",
        "notas": "Lok. dykhyn; 'ver'; li wadili dykha siba-be 'el hombre vio las piedras'; Pet 1987",
        "categoria": "verbos"
    },
    "faryn": {
        "es": "matar, dar muerte",
        "fuente": "lokono",
        "notas": "Lok. faryn; 'matar'; li fary-fa aba kabadaro 'él matará un jaguar'; intransitiviza en a-stem: fara 'pelear'; Pet 1987",
        "categoria": "verbos"
    },
    "fatadyn": {
        "es": "golpear, pegar",
        "fuente": "lokono",
        "notas": "Lok. fatadyn; 'golpear/pegar'; fatada-n (a-stem): 'andar golpeando'; thy-fatady-fa to kalhina 'ella golpeará la gallina'; Pet 1987",
        "categoria": "verbos"
    },
    "haikaikan": {
        "es": "pasar, transcurrir, morir (verbo de paso)",
        "fuente": "lokono",
        "notas": "Lok. haikaikan; 'pasar/transcurrir'; base de haikahu (muerte) y auhakit (matrimonio: 'la que ha pasado'); Brinton 1871",
        "categoria": "verbos"
    },
    "kanabyn": {
        "es": "oír, escuchar",
        "fuente": "lokono",
        "notas": "Lok. kanabyn; 'oír/escuchar'; to hiaro kanaba-fa to kodibio-be khonan 'la mujer escuchará a los pájaros'; Pet 1987",
        "categoria": "verbos"
    },
    "kassan": {
        "es": "estar embarazada",
        "fuente": "lokono",
        "notas": "Lok. kassan; 'estar embarazada'; base de kassaku (firmamento = 'la que está preñada'); metáfora cosmológica; Brinton 1871",
        "categoria": "verbos"
    },
    "keretin": {
        "es": "casarse (forma del punto de vista femenino)",
        "fuente": "lokono",
        "notas": "Lok. keretin; 'casarse (forma fem.)'; kerejun 'casarse (forma masc.)'; distinción de género en verbo matrimonial; Brinton 1871",
        "categoria": "verbos"
    },
    "khin": {
        "es": "comer",
        "fuente": "lokono",
        "notas": "Lok. khin; 'comer'; khesia 'comida' (nominalización WH.OBJ); raíz arahuacana universal; Pet 1987",
        "categoria": "verbos"
    },
    "malhitan": {
        "es": "crear, hacer (algo nuevo)",
        "fuente": "lokono",
        "notas": "Lok. malhitan; 'crear/hacer'; malhita-thi 'el creador'; usado en contexto cosmogónico; Pet 1987",
        "categoria": "verbos"
    },
    "manin": {
        "es": "estar ileso, ser invicto, no haber sido tocado",
        "fuente": "lokono",
        "notas": "Lok. manin; 'estar ileso/invicto'; manikade 'estoy ileso'; cognado Taíno manicato (invicto); Brinton 1871",
        "categoria": "verbos"
    },
    "mithadan": {
        "es": "ridiculizar, burlarse",
        "fuente": "lokono",
        "notas": "Lok. mithadan; 'ridiculizar/burlarse'; na-mithada-fa da-khonan 'ellos se burlarán de mí'; Pet 1987",
        "categoria": "verbos"
    },
    "nuddan": {
        "es": "verse bien, estar firme (verbo de buen aspecto)",
        "fuente": "lokono",
        "notas": "Lok. nuddan; 'verse bien/estar firme'; cognado Taíno nitainos (pequeños jefes: 'los de buen aspecto'); Brinton 1871",
        "categoria": "verbos"
    },
    "osyn": {
        "es": "ir, caminar, desplazarse",
        "fuente": "lokono",
        "notas": "Lok. osyn; 'ir/caminar'; l-osy-fa 'él irá'; osy-n (forma citación); Pet 1987",
        "categoria": "verbos"
    },
    "sikin": {
        "es": "dar, poner",
        "fuente": "lokono",
        "notas": "Lok. sikin; 'dar/poner'; da-siki-fa no thy-myn 'yo se lo daré a ella'; ditransitivo; Pet 1987",
        "categoria": "verbos"
    },
    "simakyn": {
        "es": "llamar (a alguien)",
        "fuente": "lokono",
        "notas": "Lok. simakyn; 'llamar'; da-simaka-bo 'estoy llamando'; simakan 'gritar, clamar'; Pet 1987",
        "categoria": "verbos"
    },
    "sokon": {
        "es": "cortar (con machete o hacha)",
        "fuente": "lokono",
        "notas": "Lok. sokon; 'cortar'; da-sokoa 'me cortaron / me corté'; oa-stem = pasivo/reflexivo; Pet 1987",
        "categoria": "verbos"
    },
    "thimin": {
        "es": "nadar, cruzar a nado",
        "fuente": "lokono",
        "notas": "Lok. thimin; 'nadar'; thiman 'cruzar (a nado/río)'; par básico/a-stem; Pet 1987",
        "categoria": "verbos"
    },
    "wadan": {
        "es": "buscar, procurar",
        "fuente": "lokono",
        "notas": "Lok. wadan; 'buscar'; cf. Wayuu wada (caminar buscando); raíz arahuacana; Pet 1987",
        "categoria": "verbos"
    },
    "ythyn": {
        "es": "beber",
        "fuente": "lokono",
        "notas": "Lok. ythyn; 'beber'; ythysia 'bebida' (nominalización); kathysia 'tener bebida'; Pet 1987",
        "categoria": "verbos"
    },

    # -- WAYUNAIKI COMPLETO (Captain & Captain 2005) -- 770 entradas --

    # [adjetivos]
    "chi": {
        "es": "este",
        "fuente": "wayunaiki",
        "notas": "Way. chi; *chi (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "irolu": {
        "es": "verde (no seco)",
        "fuente": "wayunaiki",
        "notas": "Way. irolu; *irolu (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "ja'apü": {
        "es": "mediano, -na",
        "fuente": "wayunaiki",
        "notas": "Way. ja'apü; *aabu (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "laülaa": {
        "es": "viejo, -ja; anciano, -na",
        "fuente": "wayunaiki",
        "notas": "Way. laülaa; *laula (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "mütsiiya": {
        "es": "negro, -gra",
        "fuente": "wayunaiki",
        "notas": "Way. mütsiiya; *mutsiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "nala": {
        "es": "esos",
        "fuente": "wayunaiki",
        "notas": "Way. nala; *nala (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "ouktasiro'ulu": {
        "es": "mortal (que causa",
        "fuente": "wayunaiki",
        "notas": "Way. ouktasiro'ulu; *ouktasiroulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "shiimüin": {
        "es": "verdadero, shokulaa, shukulaa v",
        "fuente": "wayunaiki",
        "notas": "Way. shiimüin; *chimuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "tü": {
        "es": "esta",
        "fuente": "wayunaiki",
        "notas": "Way. tü; *tu (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },
    "tüsa": {
        "es": "aquella",
        "fuente": "wayunaiki",
        "notas": "Way. tüsa; *tusa (proto-caquetio); Captain & Captain 2005",
        "categoria": "adjetivos",
    },

    # [alimentos]
    "ashuku": {
        "es": "huevo",
        "fuente": "wayunaiki",
        "notas": "Way. ashuku; *achuku (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "e'ejü": {
        "es": "sabor",
        "fuente": "wayunaiki",
        "notas": "Way. e'ejü; *eeyu (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "eküülü": {
        "es": "comida, alimento",
        "fuente": "wayunaiki",
        "notas": "Way. eküülü; *ekuulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "ichii": {
        "es": "sal",
        "fuente": "wayunaiki",
        "notas": "Way. ichii; *ichi (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "jamü": {
        "es": "hambre, escasez de alimento",
        "fuente": "wayunaiki",
        "notas": "Way. jamü; *amu (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "juriicha": {
        "es": "comida frita",
        "fuente": "wayunaiki",
        "notas": "Way. juriicha; *uricha (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "manteeka": {
        "es": "aceite comestible",
        "fuente": "wayunaiki",
        "notas": "Way. manteeka; *manteca (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "seepü": {
        "es": "grasa, sebo",
        "fuente": "wayunaiki",
        "notas": "Way. seepü; *sebu (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },
    "yajaaushi": {
        "es": "mazamorra con leche",
        "fuente": "wayunaiki",
        "notas": "Way. yajaaushi; *yayauchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "alimentos",
    },

    # [comunicacion]
    "aa'inmajaa": {
        "es": "cuidar",
        "fuente": "wayunaiki",
        "notas": "Way. aa'inmajaa; *ainmaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "achekajaa": {
        "es": "cobrar deuda",
        "fuente": "wayunaiki",
        "notas": "Way. achekajaa; *achecaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "achiawaa": {
        "es": "amonestar, aconsejar",
        "fuente": "wayunaiki",
        "notas": "Way. achiawaa; *achiaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "achikanain": {
        "es": "huella",
        "fuente": "wayunaiki",
        "notas": "Way. achikanain; *achicanain (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ajütaa": {
        "es": "enviar, mandar",
        "fuente": "wayunaiki",
        "notas": "Way. ajütaa; *ayuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "akaaliijaa": {
        "es": "ayudar",
        "fuente": "wayunaiki",
        "notas": "Way. akaaliijaa; *acaliya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "akua": {
        "es": "viaje",
        "fuente": "wayunaiki",
        "notas": "Way. akua; *akua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "akuaippa": {
        "es": "forma, naturaleza",
        "fuente": "wayunaiki",
        "notas": "Way. akuaippa; *akuaippa (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "aküjaa": {
        "es": "contar",
        "fuente": "wayunaiki",
        "notas": "Way. aküjaa; *akuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "alijunaiki": {
        "es": "español (idioma)",
        "fuente": "wayunaiki",
        "notas": "Way. alijunaiki; *aliyunaiki (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "amaünajaa": {
        "es": "cobrar por daño a",
        "fuente": "wayunaiki",
        "notas": "Way. amaünajaa; *amaunaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ana": {
        "es": "diseño",
        "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki", "fuente": "caquetío-reconstruido",
        "notas": "Way. ana; *ana (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "anaajawaa": {
        "es": "guardar",
        "fuente": "wayunaiki",
        "notas": "Way. anaajawaa; *anayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "anaatawaa": {
        "es": "acomodarse",
        "fuente": "wayunaiki",
        "notas": "Way. anaatawaa; *anataua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "anülia": {
        "es": "nombre",
        "fuente": "wayunaiki",
        "notas": "Way. anülia; *anulia (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "anüliee": {
        "es": "lista de nombres",
        "fuente": "wayunaiki",
        "notas": "Way. anüliee; *anulie (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "apalapajaa": {
        "es": "hacer rodar",
        "fuente": "wayunaiki",
        "notas": "Way. apalapajaa; *abalabaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "apalapajawaa": {
        "es": "rodar",
        "fuente": "wayunaiki",
        "notas": "Way. apalapajawaa; *abalabayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ashapajawaa": {
        "es": "darse prisa, tener",
        "fuente": "wayunaiki",
        "notas": "Way. ashapajawaa; *achabayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ashoujaa": {
        "es": "estornudar",
        "fuente": "wayunaiki",
        "notas": "Way. ashoujaa; *achouya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ashuunajaa": {
        "es": "nadar",
        "fuente": "wayunaiki",
        "notas": "Way. ashuunajaa; *achunaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "asiraa": {
        "es": "dar de beber",
        "fuente": "wayunaiki",
        "notas": "Way. asiraa; *asira (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "awalaajaa": {
        "es": "pagar",
        "fuente": "wayunaiki",
        "notas": "Way. awalaajaa; *aualaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ayaakua": {
        "es": "imagen, fotografía",
        "fuente": "wayunaiki",
        "notas": "Way. ayaakua; *ayakua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ayaawajaa": {
        "es": "contar, medir",
        "fuente": "wayunaiki",
        "notas": "Way. ayaawajaa; *ayauaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ayaawase": {
        "es": "señal, símbolo",
        "fuente": "wayunaiki",
        "notas": "Way. ayaawase; *ayauase (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ayalajaa": {
        "es": "comprar",
        "fuente": "wayunaiki",
        "notas": "Way. ayalajaa; *ayalaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "eisalajaa": {
        "es": "cuidar, asear",
        "fuente": "wayunaiki",
        "notas": "Way. eisalajaa; *eisalaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "epijana": {
        "es": "ruido de",
        "fuente": "wayunaiki",
        "notas": "Way. epijana; *ebiyana (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "kasachiki": {
        "es": "noticia",
        "fuente": "wayunaiki",
        "notas": "Way. kasachiki; *casachiki (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "makataa": {
        "es": "quedarse",
        "fuente": "wayunaiki",
        "notas": "Way. makataa; *macata (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "o'onowaa": {
        "es": "mudarse",
        "fuente": "wayunaiki",
        "notas": "Way. o'onowaa; *oonoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "o'tchejaa": {
        "es": "fallar (no dar en el",
        "fuente": "wayunaiki",
        "notas": "Way. o'tchejaa; *otcheya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "o'ulejaa": {
        "es": "maldecir",
        "fuente": "wayunaiki",
        "notas": "Way. o'ulejaa; *ouleya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "okolojowaa": {
        "es": "mudarse",
        "fuente": "wayunaiki",
        "notas": "Way. okolojowaa; *ocoloyoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "ounekaa": {
        "es": "recobrar el conocimiento, ounekaa",
        "fuente": "wayunaiki",
        "notas": "Way. ounekaa; *ouneca (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "outkajaa": {
        "es": "reunir, juntar",
        "fuente": "wayunaiki",
        "notas": "Way. outkajaa; *outcaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "outkajawaa": {
        "es": "reunirse",
        "fuente": "wayunaiki",
        "notas": "Way. outkajawaa; *outcayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "perulaa": {
        "es": "chisme",
        "fuente": "wayunaiki",
        "notas": "Way. perulaa; *perula (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "siimaraalü": {
        "es": "marca",
        "fuente": "wayunaiki",
        "notas": "Way. siimaraalü; *simaralu (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "sütaa": {
        "es": "dar comezón",
        "fuente": "wayunaiki",
        "notas": "Way. sütaa; *suta (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },
    "wayuunaiki": {
        "es": "idioma de los wayuu",
        "fuente": "wayunaiki",
        "notas": "Way. wayuunaiki; *bayunaiki (proto-caquetio); Captain & Captain 2005",
        "categoria": "comunicacion",
    },

    # [cosmos]
    "aa'ayula": {
        "es": "calor, temperatura",
        "fuente": "wayunaiki",
        "notas": "Way. aa'ayula; *aayula (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "amuuyuu": {
        "es": "cementerio",
        "fuente": "wayunaiki",
        "notas": "Way. amuuyuu; *amuyu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "amüsain": {
        "es": "humo",
        "fuente": "wayunaiki",
        "notas": "Way. amüsain; *amusain (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "atürüla": {
        "es": "trueno, paso",
        "fuente": "wayunaiki",
        "notas": "Way. atürüla; *aturula (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "awarala": {
        "es": "luz",
        "fuente": "wayunaiki",
        "notas": "Way. awarala; *auarala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "ayaa": {
        "es": "relámpago",
        "fuente": "wayunaiki",
        "notas": "Way. ayaa; *aya (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "eemioushi": {
        "es": "sombra",
        "fuente": "wayunaiki",
        "notas": "Way. eemioushi; *emiouchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "jolotsü": {
        "es": "estrella",
        "fuente": "wayunaiki",
        "notas": "Way. jolotsü; *olotsu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "kaspolüin": {
        "es": "arco iris",
        "fuente": "wayunaiki",
        "notas": "Way. kaspolüin; *caspoluin (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "katkousü": {
        "es": "arma de fuego",
        "fuente": "wayunaiki",
        "notas": "Way. katkousü; *catcousu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "luusa": {
        "es": "luz",
        "fuente": "wayunaiki",
        "notas": "Way. luusa; *lusa (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "pali'i": {
        "es": "ceniza",
        "fuente": "wayunaiki",
        "notas": "Way. pali'i; *palii (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "piyuushi": {
        "es": "oscuridad",
        "fuente": "wayunaiki",
        "notas": "Way. piyuushi; *piyuchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "walatshi": {
        "es": "calor atmosférico",
        "fuente": "wayunaiki",
        "notas": "Way. walatshi; *balatchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },
    "wawai": {
        "es": "viento (de tempestad)",
        "fuente": "wayunaiki",
        "notas": "Way. wawai; *bauai (proto-caquetio); Captain & Captain 2005",
        "categoria": "cosmos",
    },

    # [cuerpo]
    "a'wala": {
        "es": "cabello",
        "fuente": "wayunaiki",
        "notas": "Way. a'wala; *auala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "a'wiira": {
        "es": "lágrima",
        "fuente": "wayunaiki",
        "notas": "Way. a'wiira; *auira (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "aaluwain": {
        "es": "tobillo",
        "fuente": "wayunaiki",
        "notas": "Way. aaluwain; *aluuain (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "aanükü": {
        "es": "boca",
        "fuente": "wayunaiki",
        "notas": "Way. aanükü; *anuku (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "acha'a": {
        "es": "excremento",
        "fuente": "wayunaiki",
        "notas": "Way. acha'a; *achaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ache'e": {
        "es": "oreja, oído",
        "fuente": "wayunaiki",
        "notas": "Way. ache'e; *achee (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "achepü": {
        "es": "pintura para la cara",
        "fuente": "wayunaiki",
        "notas": "Way. achepü; *achebu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "achira": {
        "es": "seno",
        "fuente": "wayunaiki",
        "notas": "Way. achira; *achira (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "aja'apüin": {
        "es": "tamaño (por altura, ajutalaa",
        "fuente": "wayunaiki",
        "notas": "Way. aja'apüin; *ayaabuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ajapkii": {
        "es": "muñeca",
        "fuente": "wayunaiki",
        "notas": "Way. ajapkii; *ayapki (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "aliina": {
        "es": "muela",
        "fuente": "wayunaiki",
        "notas": "Way. aliina; *alina (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "aluuwain": {
        "es": "pecho",
        "fuente": "wayunaiki",
        "notas": "Way. aluuwain; *aluuain (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "amülira": {
        "es": "vello",
        "fuente": "wayunaiki",
        "notas": "Way. amülira; *amulira (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ano'u": {
        "es": "diseño",
        "fuente": "wayunaiki",
        "notas": "Way. ano'u; *anou (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "apachera": {
        "es": "dedo (del pie)",
        "fuente": "wayunaiki",
        "notas": "Way. apachera; *abachera (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "apato'u": {
        "es": "uña, garra, pezuña",
        "fuente": "wayunaiki",
        "notas": "Way. apato'u; *abatou (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "apü'ü": {
        "es": "muslo",
        "fuente": "wayunaiki",
        "notas": "Way. apü'ü; *abuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "asapü": {
        "es": "espalda, columna",
        "fuente": "wayunaiki",
        "notas": "Way. asapü; *asabu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "asatala": {
        "es": "codo",
        "fuente": "wayunaiki",
        "notas": "Way. asatala; *asatala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ase'eru'u": {
        "es": "mitad, cintura",
        "fuente": "wayunaiki",
        "notas": "Way. ase'eru'u; *aseeruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "asi": {
        "es": "cola",
        "fuente": "wayunaiki",
        "notas": "Way. asi; *asi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "asipala": {
        "es": "cicatriz",
        "fuente": "wayunaiki",
        "notas": "Way. asipala; *asibala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "atouta": {
        "es": "piel entera, superficie",
        "fuente": "wayunaiki",
        "notas": "Way. atouta; *atouta (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "atüna": {
        "es": "brazo, ala",
        "fuente": "wayunaiki",
        "notas": "Way. atüna; *atuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "awaa": {
        "es": "saliva",
        "fuente": "wayunaiki",
        "notas": "Way. awaa; *aua (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "awala": {
        "es": "hermano, -na",
        "fuente": "wayunaiki",
        "notas": "Way. awala; *auala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "awalainse": {
        "es": "mandíbula, quijada",
        "fuente": "wayunaiki",
        "notas": "Way. awalainse; *aualainse (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "awalapa'a": {
        "es": "mejilla",
        "fuente": "wayunaiki",
        "notas": "Way. awalapa'a; *aualabaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ayee": {
        "es": "lengua",
        "fuente": "wayunaiki",
        "notas": "Way. ayee; *aye (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ayülain": {
        "es": "intestino, tripa",
        "fuente": "wayunaiki",
        "notas": "Way. ayülain; *ayulain (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "chirinchi": {
        "es": "aguardiente",
        "fuente": "wayunaiki",
        "notas": "Way. chirinchi; *chirinchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "e'ichi": {
        "es": "nariz",
        "fuente": "wayunaiki",
        "notas": "Way. e'ichi; *eichi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "e'iima": {
        "es": "barba",
        "fuente": "wayunaiki",
        "notas": "Way. e'iima; *eima (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "e'iru'u": {
        "es": "punta",
        "fuente": "wayunaiki",
        "notas": "Way. e'iru'u; *eiruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "e'iyeise": {
        "es": "barbilla",
        "fuente": "wayunaiki",
        "notas": "Way. e'iyeise; *eiyeise (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "eejuu": {
        "es": "olor",
        "fuente": "wayunaiki",
        "notas": "Way. eejuu; *eyu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "eipüse": {
        "es": "hueso",
        "fuente": "wayunaiki",
        "notas": "Way. eipüse; *eibuse (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ekia": {
        "es": "mano derecha",
        "fuente": "wayunaiki",
        "notas": "Way. ekia; *ekia (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ekiisholoin": {
        "es": "cerebro, seso",
        "fuente": "wayunaiki",
        "notas": "Way. ekiisholoin; *ekicholoin (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "epe'e": {
        "es": "mano izquierda",
        "fuente": "wayunaiki",
        "notas": "Way. epe'e; *ebee (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ewein": {
        "es": "lunar",
        "fuente": "wayunaiki",
        "notas": "Way. ewein; *euein (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "iita": {
        "es": "recipiente para comida o",
        "fuente": "wayunaiki",
        "notas": "Way. iita; *ita (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "jiipü": {
        "es": "hueso",
        "fuente": "wayunaiki",
        "notas": "Way. jiipü; *yibu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "ka'lapücho'u": {
        "es": "ave cucarachero",
        "fuente": "wayunaiki",
        "notas": "Way. ka'lapücho'u; *calabuchou (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "kaarai": {
        "es": "alcaraván (dara)",
        "fuente": "wayunaiki",
        "notas": "Way. kaarai; *carai (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "kalekale": {
        "es": "perico (cara sucia)",
        "fuente": "wayunaiki",
        "notas": "Way. kalekale; *calecale (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "kasipa": {
        "es": "ciempiés",
        "fuente": "wayunaiki",
        "notas": "Way. kasipa; *casiba (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "majayülü": {
        "es": "señorita, joven (mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. majayülü; *mayayulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "mapüi": {
        "es": "piojo",
        "fuente": "wayunaiki",
        "notas": "Way. mapüi; *mabui (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "o'uluku": {
        "es": "miembro",
        "fuente": "wayunaiki",
        "notas": "Way. o'uluku; *ouluku (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "o'upünaa": {
        "es": "cara, rostro",
        "fuente": "wayunaiki",
        "notas": "Way. o'upünaa; *oubuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "o'utala": {
        "es": "cáscara",
        "fuente": "wayunaiki",
        "notas": "Way. o'utala; *outala (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "oi": {
        "es": "vello",
        "fuente": "wayunaiki",
        "notas": "Way. oi; *oi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "omokoin": {
        "es": "espuma",
        "fuente": "wayunaiki",
        "notas": "Way. omokoin; *omocoin (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "teitei": {
        "es": "alcaraván",
        "fuente": "wayunaiki",
        "notas": "Way. teitei; *teitei (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "walashi": {
        "es": "pelo",
        "fuente": "wayunaiki",
        "notas": "Way. walashi; *balachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "wayunkeera": {
        "es": "muñeca (figura de",
        "fuente": "wayunaiki",
        "notas": "Way. wayunkeera; *bayuncera (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },
    "yooi": {
        "es": "llaga, infección",
        "fuente": "wayunaiki",
        "notas": "Way. yooi; *yoi (proto-caquetio); Captain & Captain 2005",
        "categoria": "cuerpo",
    },

    # [fauna]
    "asirü": {
        "es": "presa",
        "fuente": "wayunaiki",
        "notas": "Way. asirü; *asiru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "chünü'ü": {
        "es": "colibrí",
        "fuente": "wayunaiki",
        "notas": "Way. chünü'ü; *chunuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "e'e": {
        "es": "plaga, parásito",
        "fuente": "wayunaiki",
        "notas": "Way. e'e; *ee (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "e'ejena": {
        "es": "cabalgadura",
        "fuente": "wayunaiki",
        "notas": "Way. e'ejena; *eeyena (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "eperü'üi": {
        "es": "sapo",
        "fuente": "wayunaiki",
        "notas": "Way. eperü'üi; *eberuui (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "erü": {
        "es": "perro, -rra",
        "fuente": "wayunaiki",
        "notas": "Way. erü; *eru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "iisho": {
        "es": "ave cardenal coriano",
        "fuente": "wayunaiki",
        "notas": "Way. iisho; *icho (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ja'yumulerü": {
        "es": "mosca",
        "fuente": "wayunaiki",
        "notas": "Way. ja'yumulerü; *ayumuleru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "jayapa": {
        "es": "pulga",
        "fuente": "wayunaiki",
        "notas": "Way. jayapa; *ayaba (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ji'rupu": {
        "es": "mosquito",
        "fuente": "wayunaiki",
        "notas": "Way. ji'rupu; *yirubu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "jokoma": {
        "es": "gusano",
        "fuente": "wayunaiki",
        "notas": "Way. jokoma; *ocoma (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ju'i": {
        "es": "grillo",
        "fuente": "wayunaiki",
        "notas": "Way. ju'i; *ui (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "julirü": {
        "es": "mariposa",
        "fuente": "wayunaiki",
        "notas": "Way. julirü; *uliru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "kaashapü": {
        "es": "langosta (insecto)",
        "fuente": "wayunaiki",
        "notas": "Way. kaashapü; *cachabu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "katipirüin": {
        "es": "ave atrapamoscas",
        "fuente": "wayunaiki",
        "notas": "Way. katipirüin; *catibiruin (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ko'oi": {
        "es": "avispa",
        "fuente": "wayunaiki",
        "notas": "Way. ko'oi; *cooi (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "kookooche'erü": {
        "es": "ratón, rata",
        "fuente": "wayunaiki",
        "notas": "Way. kookooche'erü; *cococheeru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "mashale'e": {
        "es": "ave caricare",
        "fuente": "wayunaiki",
        "notas": "Way. mashale'e; *machalee (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "mo'uwa": {
        "es": "paloma (silvestre)",
        "fuente": "wayunaiki",
        "notas": "Way. mo'uwa; *mouua (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "monkulonseerü": {
        "es": "búho",
        "fuente": "wayunaiki",
        "notas": "Way. monkulonseerü; *monkulonseru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "mürülü": {
        "es": "animal doméstico",
        "fuente": "wayunaiki",
        "notas": "Way. mürülü; *murulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "peerü": {
        "es": "perdiz",
        "fuente": "wayunaiki",
        "notas": "Way. peerü; *peru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "potshonoi": {
        "es": "libélula",
        "fuente": "wayunaiki",
        "notas": "Way. potshonoi; *potchonoi (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "püsichi": {
        "es": "murciélago",
        "fuente": "wayunaiki",
        "notas": "Way. püsichi; *pusichi (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ruluma": {
        "es": "comején (termes)",
        "fuente": "wayunaiki",
        "notas": "Way. ruluma; *ruluma (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "sa'wainrü": {
        "es": "tortuga de",
        "fuente": "wayunaiki",
        "notas": "Way. sa'wainrü; *sauainru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "samulu": {
        "es": "buitre, zamuro",
        "fuente": "wayunaiki",
        "notas": "Way. samulu; *samulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "sarulu": {
        "es": "boa",
        "fuente": "wayunaiki",
        "notas": "Way. sarulu; *sarulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "seruma": {
        "es": "ave chirito",
        "fuente": "wayunaiki",
        "notas": "Way. seruma; *seruma (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "si'ya": {
        "es": "gonzalito, toche",
        "fuente": "wayunaiki",
        "notas": "Way. si'ya; *siya (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "taataai": {
        "es": "rana",
        "fuente": "wayunaiki",
        "notas": "Way. taataai; *tatai (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "toolü": {
        "es": "ave aguaitacamino, ave",
        "fuente": "wayunaiki",
        "notas": "Way. toolü; *tolu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "toomasü": {
        "es": "paloma (doméstica)",
        "fuente": "wayunaiki",
        "notas": "Way. toomasü; *tomasu (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ulee": {
        "es": "estar limpio, -pia",
        "fuente": "wayunaiki",
        "notas": "Way. ulee; *ule (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "ului": {
        "es": "ave turpial común",
        "fuente": "wayunaiki",
        "notas": "Way. ului; *ului (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "wainpirai": {
        "es": "ave paraulata llanera",
        "fuente": "wayunaiki",
        "notas": "Way. wainpirai; *bainpirai (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "walekerü": {
        "es": "araña",
        "fuente": "wayunaiki",
        "notas": "Way. walekerü; *baleceru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "walirü": {
        "es": "zorro, -rra",
        "fuente": "wayunaiki",
        "notas": "Way. walirü; *baliru (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "wuchii": {
        "es": "pájaro",
        "fuente": "wayunaiki",
        "notas": "Way. wuchii; *buchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "wuliyuuna": {
        "es": "lombriz",
        "fuente": "wayunaiki",
        "notas": "Way. wuliyuuna; *buliyuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "wüi": {
        "es": "culebra",
        "fuente": "wayunaiki",
        "notas": "Way. wüi; *bui (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },
    "yaawe": {
        "es": "llave",
        "fuente": "wayunaiki",
        "notas": "Way. yaawe; *yaue (proto-caquetio); Captain & Captain 2005",
        "categoria": "fauna",
    },

    # [flora]
    "a'ttia": {
        "es": "cosecha, cultivo",
        "fuente": "wayunaiki",
        "notas": "Way. a'ttia; *attia (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "a'ü": {
        "es": "semilla",
        "fuente": "wayunaiki",
        "notas": "Way. a'ü; *au (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "adoptivo": {
        "es": "árbol trupillo, cují",
        "fuente": "wayunaiki",
        "notas": "Way. adoptivo; *adoptivo (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "ajü": {
        "es": "savia, resina",
        "fuente": "wayunaiki",
        "notas": "Way. ajü; *ayu (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "alama": {
        "es": "pasto",
        "fuente": "wayunaiki",
        "notas": "Way. alama; *alama (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "aliita": {
        "es": "totuma (especie de calabaza)",
        "fuente": "wayunaiki",
        "notas": "Way. aliita; *alita (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "ase": {
        "es": "fibra, pulpa, borra",
        "fuente": "wayunaiki",
        "notas": "Way. ase; *ase (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "asema": {
        "es": "leña",
        "fuente": "wayunaiki",
        "notas": "Way. asema; *asema (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "asii": {
        "es": "flor",
        "fuente": "wayunaiki",
        "notas": "Way. asii; *asi (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "epi": {
        "es": "cabo, mango (de un",
        "fuente": "wayunaiki",
        "notas": "Way. epi; *ebi (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "era": {
        "es": "jugo, savia",
        "fuente": "wayunaiki",
        "notas": "Way. era; *era (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "jamüche'e": {
        "es": "tuna",
        "fuente": "wayunaiki",
        "notas": "Way. jamüche'e; *amuchee (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "maawüi": {
        "es": "algodón",
        "fuente": "wayunaiki",
        "notas": "Way. maawüi; *mauui (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "meruuna": {
        "es": "melón",
        "fuente": "wayunaiki",
        "notas": "Way. meruuna; *meruna (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "monku": {
        "es": "mango (fruta)",
        "fuente": "wayunaiki",
        "notas": "Way. monku; *monku (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "oo'ulia": {
        "es": "mata",
        "fuente": "wayunaiki",
        "notas": "Way. oo'ulia; *oulia (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "ourala": {
        "es": "raíz",
        "fuente": "wayunaiki",
        "notas": "Way. ourala; *ourala (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "pünajüt": {
        "es": "lo sembrado, cultivo",
        "fuente": "wayunaiki",
        "notas": "Way. pünajüt; *punayut (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "rülipi": {
        "es": "sábila, áloe",
        "fuente": "wayunaiki",
        "notas": "Way. rülipi; *rulibi (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "türiiya": {
        "es": "junco",
        "fuente": "wayunaiki",
        "notas": "Way. türiiya; *turiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "waana": {
        "es": "millo, mijo",
        "fuente": "wayunaiki",
        "notas": "Way. waana; *bana (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "wala'ayuu": {
        "es": "pelusa de la tuna",
        "fuente": "wayunaiki",
        "notas": "Way. wala'ayuu; *balaayu (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "wüirü": {
        "es": "auyama, calabaza",
        "fuente": "wayunaiki",
        "notas": "Way. wüirü; *buiru (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "wüitshii": {
        "es": "hierba",
        "fuente": "wayunaiki",
        "notas": "Way. wüitshii; *buitchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },
    "yüi": {
        "es": "tabaco",
        "fuente": "wayunaiki",
        "notas": "Way. yüi; *yui (proto-caquetio); Captain & Captain 2005",
        "categoria": "flora",
    },

    # [geografia]
    "aajuna": {
        "es": "cubierta, techo",
        "fuente": "wayunaiki",
        "notas": "Way. aajuna; *ayuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "anooi": {
        "es": "terreno despejado",
        "fuente": "wayunaiki",
        "notas": "Way. anooi; *anoi (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "apülee": {
        "es": "lugar, sitio, puesto",
        "fuente": "wayunaiki",
        "notas": "Way. apülee; *abule (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "apüna": {
        "es": "camino, sendero",
        "fuente": "wayunaiki",
        "notas": "Way. apüna; *abuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "asepü": {
        "es": "pared",
        "fuente": "wayunaiki",
        "notas": "Way. asepü; *asebu (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "atu'u": {
        "es": "superficie interior",
        "fuente": "wayunaiki",
        "notas": "Way. atu'u; *atuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "ipa": {
        "es": "piedra",
        "fuente": "wayunaiki",
        "notas": "Way. ipa; *iba (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "kulaala": {
        "es": "corral",
        "fuente": "wayunaiki",
        "notas": "Way. kulaala; *kulala (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "laa": {
        "es": "jagüey",
        "fuente": "wayunaiki",
        "notas": "Way. laa; *la (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "lamuuna": {
        "es": "lago",
        "fuente": "wayunaiki",
        "notas": "Way. lamuuna; *lamuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "luma": {
        "es": "enramada (estructura abierta",
        "fuente": "wayunaiki",
        "notas": "Way. luma; *luma (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "luwopu": {
        "es": "arroyo",
        "fuente": "wayunaiki",
        "notas": "Way. luwopu; *luuobu (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "maraaja": {
        "es": "vidrio",
        "fuente": "wayunaiki",
        "notas": "Way. maraaja; *maraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "miichi": {
        "es": "casa, malo, -la",
        "fuente": "wayunaiki",
        "notas": "Way. miichi; *michi (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "miicho'u": {
        "es": "puerta (la",
        "fuente": "wayunaiki",
        "notas": "Way. miicho'u; *michou (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "miiroku": {
        "es": "sitio donde hay",
        "fuente": "wayunaiki",
        "notas": "Way. miiroku; *miroku (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "mojuui": {
        "es": "monte (vegetación)",
        "fuente": "wayunaiki",
        "notas": "Way. mojuui; *moyui (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "namüna": {
        "es": "loma, cerro",
        "fuente": "wayunaiki",
        "notas": "Way. namüna; *namuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "puatto'u": {
        "es": "puerta",
        "fuente": "wayunaiki",
        "notas": "Way. puatto'u; *puattou (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "uraichi": {
        "es": "especie de árbol que florece de amarillo en la",
        "fuente": "wayunaiki",
        "notas": "Way. uraichi; *uraichi (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "wo'olu": {
        "es": "mochila para el cinturón bosque, monte",
        "fuente": "wayunaiki",
        "notas": "Way. wo'olu; *boolu (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },
    "wüin": {
        "es": "agua",
        "fuente": "wayunaiki",
        "notas": "Way. wüin; *buin (proto-caquetio); Captain & Captain 2005",
        "categoria": "geografia",
    },

    # [gramatica]
    "a'aka": {
        "es": "entre",
        "fuente": "wayunaiki",
        "notas": "Way. a'aka; *aaca (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "a'ato'u": {
        "es": "al lado de",
        "fuente": "wayunaiki",
        "notas": "Way. a'ato'u; *aatou (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "a'ütpa'a": {
        "es": "al lado de, junto a",
        "fuente": "wayunaiki",
        "notas": "Way. a'ütpa'a; *autpaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "aa'u": {
        "es": "en",
        "fuente": "wayunaiki",
        "notas": "Way. aa'u; *au (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "aashin": {
        "es": "según",
        "fuente": "wayunaiki",
        "notas": "Way. aashin; *achin (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "achiirua": {
        "es": "detrás de",
        "fuente": "wayunaiki",
        "notas": "Way. achiirua; *achirua (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "achikijee": {
        "es": "después de",
        "fuente": "wayunaiki",
        "notas": "Way. achikijee; *achikiye (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "achikiru'u": {
        "es": "después de la salida aikkaa",
        "fuente": "wayunaiki",
        "notas": "Way. achikiru'u; *achikiruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "airu'u": {
        "es": "en la horqueta de, entre",
        "fuente": "wayunaiki",
        "notas": "Way. airu'u; *airuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "akaisa'a": {
        "es": "pero, sin embargo",
        "fuente": "wayunaiki",
        "notas": "Way. akaisa'a; *acaisaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "ale'eru'u": {
        "es": "en el vientre de",
        "fuente": "wayunaiki",
        "notas": "Way. ale'eru'u; *aleeruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "alu'u": {
        "es": "dentro de, en",
        "fuente": "wayunaiki",
        "notas": "Way. alu'u; *aluu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "alu'ujasa'a": {
        "es": "pero",
        "fuente": "wayunaiki",
        "notas": "Way. alu'ujasa'a; *aluuyasaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "ama'ichiki": {
        "es": "antes",
        "fuente": "wayunaiki",
        "notas": "Way. ama'ichiki; *amaichiki (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "ama'inru'u": {
        "es": "mientras",
        "fuente": "wayunaiki",
        "notas": "Way. ama'inru'u; *amainruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "amüin": {
        "es": "a, para",
        "fuente": "wayunaiki",
        "notas": "Way. amüin; *amuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "anain": {
        "es": "en, a",
        "fuente": "wayunaiki",
        "notas": "Way. anain; *anain (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "anainjee": {
        "es": "de, por",
        "fuente": "wayunaiki",
        "notas": "Way. anainjee; *anainye (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "anainmüin": {
        "es": "a, hacia",
        "fuente": "wayunaiki",
        "notas": "Way. anainmüin; *anainmuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "anii": {
        "es": "aquí está, estoy",
        "fuente": "wayunaiki",
        "notas": "Way. anii; *ani (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "apücho'u": {
        "es": "detrás de",
        "fuente": "wayunaiki",
        "notas": "Way. apücho'u; *abuchou (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "apülapünaa": {
        "es": "antes de",
        "fuente": "wayunaiki",
        "notas": "Way. apülapünaa; *abulabuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "apüleerua": {
        "es": "delante de",
        "fuente": "wayunaiki",
        "notas": "Way. apüleerua; *abulerua (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "asala": {
        "es": "a causa de, por",
        "fuente": "wayunaiki",
        "notas": "Way. asala; *asala (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "atak": {
        "es": "¡caramba! atükaa pootshi embarrar",
        "fuente": "wayunaiki",
        "notas": "Way. atak; *atak (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "atüma": {
        "es": "por",
        "fuente": "wayunaiki",
        "notas": "Way. atüma; *atuma (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "e'ipajee": {
        "es": "en respuesta a",
        "fuente": "wayunaiki",
        "notas": "Way. e'ipajee; *eibaye (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "einalu'u": {
        "es": "en el fondo de, en el ekiisa",
        "fuente": "wayunaiki",
        "notas": "Way. einalu'u; *einaluu (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "eroku": {
        "es": "en (un líquido)",
        "fuente": "wayunaiki",
        "notas": "Way. eroku; *eroku (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "jalia": {
        "es": "¡cuidado!",
        "fuente": "wayunaiki",
        "notas": "Way. jalia; *alia (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "jia": {
        "es": "ustedes; los, las",
        "fuente": "wayunaiki",
        "notas": "Way. jia; *yia (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "joo'uya": {
        "es": "vámonos",
        "fuente": "wayunaiki",
        "notas": "Way. joo'uya; *ouya (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "kaatei": {
        "es": "¡oiga! ka'i",
        "fuente": "wayunaiki",
        "notas": "Way. kaatei; *catei (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "nia": {
        "es": "él, lo",
        "fuente": "wayunaiki",
        "notas": "Way. nia; *nia (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "o'upala": {
        "es": "delante de (a la vista",
        "fuente": "wayunaiki",
        "notas": "Way. o'upala; *oubala (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "o'utpünaa": {
        "es": "durante",
        "fuente": "wayunaiki",
        "notas": "Way. o'utpünaa; *outpuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "ojuuna": {
        "es": "a escondidas",
        "fuente": "wayunaiki",
        "notas": "Way. ojuuna; *oyuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "oo'opünaa": {
        "es": "por",
        "fuente": "wayunaiki",
        "notas": "Way. oo'opünaa; *oobuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "oulia": {
        "es": "de, más que, en vez de, 2",
        "fuente": "wayunaiki",
        "notas": "Way. oulia; *oulia (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "oupünaa": {
        "es": "debajo de",
        "fuente": "wayunaiki",
        "notas": "Way. oupünaa; *oubuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "shiale": {
        "es": "o ella",
        "fuente": "wayunaiki",
        "notas": "Way. shiale; *chiale (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },
    "wane'ere'eya": {
        "es": "no hasta que",
        "fuente": "wayunaiki",
        "notas": "Way. wane'ere'eya; *baneereeya (proto-caquetio); Captain & Captain 2005",
        "categoria": "gramatica",
    },

    # [jerarquia]
    "aapiee": {
        "es": "mensajero, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. aapiee; *abie (proto-caquetio); Captain & Captain 2005",
        "categoria": "jerarquia",
    },
    "achepchia": {
        "es": "sirviente, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. achepchia; *achepchia (proto-caquetio); Captain & Captain 2005",
        "categoria": "jerarquia",
    },
    "apü'üya": {
        "es": "pastor, -tora; guardián, -diana; cuidador, -dora",
        "fuente": "wayunaiki",
        "notas": "Way. apü'üya; *abuuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "jerarquia",
    },
    "ee'iraka": {
        "es": "sustituto, -ta; suplente",
        "fuente": "wayunaiki",
        "notas": "Way. ee'iraka; *eiraca (proto-caquetio); Captain & Captain 2005",
        "categoria": "jerarquia",
    },
    "piuuna": {
        "es": "sirviente, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. piuuna; *piuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "jerarquia",
    },

    # [otros]
    "kaasü": {
        "es": "petróleo (para lámpara)",
        "fuente": "wayunaiki",
        "notas": "Way. kaasü; *casu (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kaatset": {
        "es": "cárcel",
        "fuente": "wayunaiki",
        "notas": "Way. kaatset; *catset (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kalapaasü": {
        "es": "patilla (especie de",
        "fuente": "wayunaiki",
        "notas": "Way. kalapaasü; *calabasu (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kane'ewa": {
        "es": "mamón (fruta)",
        "fuente": "wayunaiki",
        "notas": "Way. kane'ewa; *caneeua (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "karateera": {
        "es": "carretera",
        "fuente": "wayunaiki",
        "notas": "Way. karateera; *caratera (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "karatiiya": {
        "es": "carretilla",
        "fuente": "wayunaiki",
        "notas": "Way. karatiiya; *caratiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kochiina": {
        "es": "cochino, -na",
        "fuente": "wayunaiki",
        "notas": "Way. kochiina; *cochina (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kosinapia": {
        "es": "cocina",
        "fuente": "wayunaiki",
        "notas": "Way. kosinapia; *cosinabia (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "kousüla": {
        "es": "bala",
        "fuente": "wayunaiki",
        "notas": "Way. kousüla; *cousula (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "laapi": {
        "es": "lápiz",
        "fuente": "wayunaiki",
        "notas": "Way. laapi; *labi (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "müliashii": {
        "es": "difunto, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. müliashii; *muliachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "o'use": {
        "es": "gafas",
        "fuente": "wayunaiki",
        "notas": "Way. o'use; *ouse (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "o'uta": {
        "es": "pestaña",
        "fuente": "wayunaiki",
        "notas": "Way. o'uta; *outa (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "o'uwa": {
        "es": "cuerno",
        "fuente": "wayunaiki",
        "notas": "Way. o'uwa; *ouua (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "o'uyaajana": {
        "es": "acompañante",
        "fuente": "wayunaiki",
        "notas": "Way. o'uyaajana; *ouyayana (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "olu": {
        "es": "borde",
        "fuente": "wayunaiki",
        "notas": "Way. olu; *olu (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "oora": {
        "es": "hora",
        "fuente": "wayunaiki",
        "notas": "Way. oora; *ora (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "paarü": {
        "es": "pala",
        "fuente": "wayunaiki",
        "notas": "Way. paarü; *paru (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "pirijirü": {
        "es": "periquito",
        "fuente": "wayunaiki",
        "notas": "Way. pirijirü; *piriyiru (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "pülaasa": {
        "es": "plaza",
        "fuente": "wayunaiki",
        "notas": "Way. pülaasa; *pulasa (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "shaakuma": {
        "es": "cabestro",
        "fuente": "wayunaiki",
        "notas": "Way. shaakuma; *chakuma (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "si'warai": {
        "es": "caldero",
        "fuente": "wayunaiki",
        "notas": "Way. si'warai; *siuarai (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "tottoolu": {
        "es": "médico, -ca",
        "fuente": "wayunaiki",
        "notas": "Way. tottoolu; *tottolu (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "tüitüi": {
        "es": "halcón",
        "fuente": "wayunaiki",
        "notas": "Way. tüitüi; *tuitui (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "walaashi": {
        "es": "pago",
        "fuente": "wayunaiki",
        "notas": "Way. walaashi; *balachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "wawaachi": {
        "es": "tortolita",
        "fuente": "wayunaiki",
        "notas": "Way. wawaachi; *bauachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },
    "woowira": {
        "es": "bóveda",
        "fuente": "wayunaiki",
        "notas": "Way. woowira; *bouira (proto-caquetio); Captain & Captain 2005",
        "categoria": "otros",
    },

    # [parentesco]
    "a'wayuuse": {
        "es": "esposo, -a",
        "fuente": "wayunaiki",
        "notas": "Way. a'wayuuse; *auayuse (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "a'üi": {
        "es": "suegro (de mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. a'üi; *aui (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "a'ülü": {
        "es": "suegra (de mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. a'ülü; *aulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "a'ünüü": {
        "es": "enemigo, -ga",
        "fuente": "wayunaiki",
        "notas": "Way. a'ünüü; *aunuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "aa'irü": {
        "es": "tía (materna)",
        "fuente": "wayunaiki",
        "notas": "Way. aa'irü; *airu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "achon": {
        "es": "hijo, -ja",
        "fuente": "wayunaiki",
        "notas": "Way. achon; *achon (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "achon'irü": {
        "es": "sobrino, -na",
        "fuente": "wayunaiki",
        "notas": "Way. achon'irü; *achoniru (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "aleshi": {
        "es": "cuñado (de mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. aleshi; *alechi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "alüin": {
        "es": "nieto, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. alüin; *aluin (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "alüinyuu": {
        "es": "cuñada (de varón)",
        "fuente": "wayunaiki",
        "notas": "Way. alüinyuu; *aluinyu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "amüraajüin": {
        "es": "novio, -via",
        "fuente": "wayunaiki",
        "notas": "Way. amüraajüin; *amurayuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "apüshi": {
        "es": "familia, pariente",
        "fuente": "wayunaiki",
        "notas": "Way. apüshi; *abuchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "ashi": {
        "es": "padre",
        "fuente": "wayunaiki",
        "notas": "Way. ashi; *achi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "ashimia": {
        "es": "suegro (de varón)",
        "fuente": "wayunaiki",
        "notas": "Way. ashimia; *achimia (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "ashiyaashi": {
        "es": "padrastro",
        "fuente": "wayunaiki",
        "notas": "Way. ashiyaashi; *achiyachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "ashunuu": {
        "es": "hermana menor (de varón)",
        "fuente": "wayunaiki",
        "notas": "Way. ashunuu; *achunu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "asiipü": {
        "es": "sobrino, -na (materno de",
        "fuente": "wayunaiki",
        "notas": "Way. asiipü; *asibu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "atuushi": {
        "es": "abuelo",
        "fuente": "wayunaiki",
        "notas": "Way. atuushi; *atuchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "atünajutü": {
        "es": "amigo, -ga",
        "fuente": "wayunaiki",
        "notas": "Way. atünajutü; *atunayutu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "awala'ata": {
        "es": "compañero, -ra;",
        "fuente": "wayunaiki",
        "notas": "Way. awala'ata; *aualaata (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "e'erü": {
        "es": "cuñada (de mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. e'erü; *eeru (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "e'iruma": {
        "es": "primogénito, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. e'iruma; *eiruma (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "e'iyou": {
        "es": "visita; huésped, -da",
        "fuente": "wayunaiki",
        "notas": "Way. e'iyou; *eiyou (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "eerüin": {
        "es": "esposa",
        "fuente": "wayunaiki",
        "notas": "Way. eerüin; *eruin (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "ei": {
        "es": "madre",
        "fuente": "wayunaiki",
        "notas": "Way. ei; *ei (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "eiyaasü": {
        "es": "madrastra",
        "fuente": "wayunaiki",
        "notas": "Way. eiyaasü; *eiyasu (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "emeshi": {
        "es": "suegra (de varón)",
        "fuente": "wayunaiki",
        "notas": "Way. emeshi; *emechi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "jierü": {
        "es": "mujer",
        "fuente": "wayunaiki",
        "notas": "Way. jierü; *yieru (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "maachon": {
        "es": "mamá, abuela",
        "fuente": "wayunaiki",
        "notas": "Way. maachon; *machon (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "oo'uliwo'u": {
        "es": "descendiente",
        "fuente": "wayunaiki",
        "notas": "Way. oo'uliwo'u; *ouliuou (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "shale": {
        "es": "último hijo, última hija",
        "fuente": "wayunaiki",
        "notas": "Way. shale; *chale (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "taata": {
        "es": "papá, abuelo",
        "fuente": "wayunaiki",
        "notas": "Way. taata; *tata (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },
    "tepichi": {
        "es": "muchacho, -cha; niño, -ña",
        "fuente": "wayunaiki",
        "notas": "Way. tepichi; *tebichi (proto-caquetio); Captain & Captain 2005",
        "categoria": "parentesco",
    },

    # [ritual]
    "aainjala": {
        "es": "acción mala",
        "fuente": "wayunaiki",
        "notas": "Way. aainjala; *ainyala (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "aleiwa": {
        "es": "Dios",
        "fuente": "wayunaiki",
        "notas": "Way. aleiwa; *aleiua (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "anoula": {
        "es": "fe",
        "fuente": "wayunaiki",
        "notas": "Way. anoula; *anoula (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "apülain": {
        "es": "poder",
        "fuente": "wayunaiki",
        "notas": "Way. apülain; *abulain (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "aseyuu": {
        "es": "espíritu de la piache",
        "fuente": "wayunaiki",
        "notas": "Way. aseyuu; *aseyu (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "ee'irain": {
        "es": "canción",
        "fuente": "wayunaiki",
        "notas": "Way. ee'irain; *eirain (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "eewain": {
        "es": "víctima",
        "fuente": "wayunaiki",
        "notas": "Way. eewain; *euain (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "lania": {
        "es": "amuleto, contra",
        "fuente": "wayunaiki",
        "notas": "Way. lania; *lania (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "maüna": {
        "es": "cobro por daño a una",
        "fuente": "wayunaiki",
        "notas": "Way. maüna; *mauna (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "mi'iraa": {
        "es": "fiesta",
        "fuente": "wayunaiki",
        "notas": "Way. mi'iraa; *miira (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },
    "yolujaa": {
        "es": "diablo, demonio",
        "fuente": "wayunaiki",
        "notas": "Way. yolujaa; *yoluya (proto-caquetio); Captain & Captain 2005",
        "categoria": "ritual",
    },

    # [sentimientos]
    "a'alain": {
        "es": "mentira",
        "fuente": "wayunaiki",
        "notas": "Way. a'alain; *aalain (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "amanee": {
        "es": "bondad, cariño",
        "fuente": "wayunaiki",
        "notas": "Way. amanee; *amane (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "amüliala": {
        "es": "sufrimiento",
        "fuente": "wayunaiki",
        "notas": "Way. amüliala; *amuliala (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "asira": {
        "es": "risa",
        "fuente": "wayunaiki",
        "notas": "Way. asira; *asira (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "atsüin": {
        "es": "fuerza",
        "fuente": "wayunaiki",
        "notas": "Way. atsüin; *atsuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "eema": {
        "es": "miedo a",
        "fuente": "wayunaiki",
        "notas": "Way. eema; *ema (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },
    "mee'era": {
        "es": "broma",
        "fuente": "wayunaiki",
        "notas": "Way. mee'era; *meera (proto-caquetio); Captain & Captain 2005",
        "categoria": "sentimientos",
    },

    # [tiempo]
    "achukua'a": {
        "es": "otra",
        "fuente": "wayunaiki",
        "notas": "Way. achukua'a; *achukuba (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "aipa'a": {
        "es": "de noche",
        "fuente": "wayunaiki",
        "notas": "Way. aipa'a; *aibaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "aipa'inka": {
        "es": "anoche",
        "fuente": "wayunaiki",
        "notas": "Way. aipa'inka; *aibainca (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "aliika": {
        "es": "por la tarde",
        "fuente": "wayunaiki",
        "notas": "Way. aliika; *alica (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "aliikainka": {
        "es": "ayer",
        "fuente": "wayunaiki",
        "notas": "Way. aliikainka; *alicainca (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "anooipa'a": {
        "es": "afuera",
        "fuente": "wayunaiki",
        "notas": "Way. anooipa'a; *anoibaa (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "cha'aya": {
        "es": "allá (lejos)",
        "fuente": "wayunaiki",
        "notas": "Way. cha'aya; *chaaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "iipünaa": {
        "es": "arriba",
        "fuente": "wayunaiki",
        "notas": "Way. iipünaa; *ibuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "iiwa": {
        "es": "primavera (tiempo de lluvias",
        "fuente": "wayunaiki",
        "notas": "Way. iiwa; *iua (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "kale'u": {
        "es": "a mediodía",
        "fuente": "wayunaiki",
        "notas": "Way. kale'u; *caleu (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "ma'i": {
        "es": "muy, mucho",
        "fuente": "wayunaiki",
        "notas": "Way. ma'i; *mai (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "maalü": {
        "es": "ya",
        "fuente": "wayunaiki",
        "notas": "Way. maalü; *malu (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "mmolu'u": {
        "es": "en el suelo, abajo",
        "fuente": "wayunaiki",
        "notas": "Way. mmolu'u; *moluu (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "motso'o": {
        "es": "por poco tiempo",
        "fuente": "wayunaiki",
        "notas": "Way. motso'o; *motsoo (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "ne'e": {
        "es": "justamente, solamente",
        "fuente": "wayunaiki",
        "notas": "Way. ne'e; *nee (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "nnojo": {
        "es": "no",
        "fuente": "wayunaiki",
        "notas": "Way. nnojo; *noyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "ouyase": {
        "es": "edad (años)",
        "fuente": "wayunaiki",
        "notas": "Way. ouyase; *ouyase (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "palaapünaa": {
        "es": "por el norte",
        "fuente": "wayunaiki",
        "notas": "Way. palaapünaa; *palabuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "palajana": {
        "es": "primero",
        "fuente": "wayunaiki",
        "notas": "Way. palajana; *palayana (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "peesü'ülü": {
        "es": "detrás de una casa",
        "fuente": "wayunaiki",
        "notas": "Way. peesü'ülü; *pesuulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "piantua": {
        "es": "dos veces",
        "fuente": "wayunaiki",
        "notas": "Way. piantua; *piantua (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "sa'aya": {
        "es": "allá",
        "fuente": "wayunaiki",
        "notas": "Way. sa'aya; *saaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "sa'wai": {
        "es": "de noche",
        "fuente": "wayunaiki",
        "notas": "Way. sa'wai; *sauai (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "unapümüin": {
        "es": "hacia abajo",
        "fuente": "wayunaiki",
        "notas": "Way. unapümüin; *unabumuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "uuchipünaa": {
        "es": "por el sur",
        "fuente": "wayunaiki",
        "notas": "Way. uuchipünaa; *uchibuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "uwatua": {
        "es": "una vez",
        "fuente": "wayunaiki",
        "notas": "Way. uwatua; *uuatua (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "waapünaa": {
        "es": "por el occidente",
        "fuente": "wayunaiki",
        "notas": "Way. waapünaa; *babuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "waneepia": {
        "es": "siempre (continuamente), continuamente",
        "fuente": "wayunaiki",
        "notas": "Way. waneepia; *banebia (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "watta'apa": {
        "es": "esta mañana (ya",
        "fuente": "wayunaiki",
        "notas": "Way. watta'apa; *battaaba (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "wattapia": {
        "es": "pasado mañana",
        "fuente": "wayunaiki",
        "notas": "Way. wattapia; *battabia (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "wiinnaa": {
        "es": "por el oriente",
        "fuente": "wayunaiki",
        "notas": "Way. wiinnaa; *binna (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "wuna'ainküin": {
        "es": "wweeinntsahaina",
        "fuente": "wayunaiki",
        "notas": "Way. wuna'ainküin; *bunaainkuin (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yaa": {
        "es": "hoy en día, en este",
        "fuente": "wayunaiki",
        "notas": "Way. yaa; *ya (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yaajeeru'u": {
        "es": "en este lado",
        "fuente": "wayunaiki",
        "notas": "Way. yaajeeru'u; *yayeruu (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yaaulerü": {
        "es": "un rato",
        "fuente": "wayunaiki",
        "notas": "Way. yaaulerü; *yauleru (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yaawala": {
        "es": "al instante",
        "fuente": "wayunaiki",
        "notas": "Way. yaawala; *yauala (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yaaya": {
        "es": "aquí",
        "fuente": "wayunaiki",
        "notas": "Way. yaaya; *yaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },
    "yala": {
        "es": "allí",
        "fuente": "wayunaiki",
        "notas": "Way. yala; *yala (proto-caquetio); Captain & Captain 2005",
        "categoria": "tiempo",
    },

    # [utiles]
    "a'apüla": {
        "es": "4. vida. arma",
        "fuente": "wayunaiki",
        "notas": "Way. a'apüla; *aabula (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "aanala": {
        "es": "cobija",
        "fuente": "wayunaiki",
        "notas": "Way. aanala; *anala (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "aawain": {
        "es": "peso",
        "fuente": "wayunaiki",
        "notas": "Way. aawain; *auain (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "achisa": {
        "es": "carga",
        "fuente": "wayunaiki",
        "notas": "Way. achisa; *achisa (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "ajapüna": {
        "es": "pulsera",
        "fuente": "wayunaiki",
        "notas": "Way. ajapüna; *ayabuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "ajutu": {
        "es": "valor",
        "fuente": "wayunaiki",
        "notas": "Way. ajutu; *ayutu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "ajuyaala": {
        "es": "deuda",
        "fuente": "wayunaiki",
        "notas": "Way. ajuyaala; *ayuyala (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "akanain": {
        "es": "sueldo, ganancia",
        "fuente": "wayunaiki",
        "notas": "Way. akanain; *acanain (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "alia": {
        "es": "precio, valor",
        "fuente": "wayunaiki",
        "notas": "Way. alia; *alia (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "amüchi": {
        "es": "múcura (vasija de barro",
        "fuente": "wayunaiki",
        "notas": "Way. amüchi; *amuchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "anülü": {
        "es": "telar",
        "fuente": "wayunaiki",
        "notas": "Way. anülü; *anulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "apü": {
        "es": "atadura, cabestro, cuerda",
        "fuente": "wayunaiki",
        "notas": "Way. apü; *abu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "ashe'in": {
        "es": "ropa",
        "fuente": "wayunaiki",
        "notas": "Way. ashe'in; *achein (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "atujuna": {
        "es": "viga",
        "fuente": "wayunaiki",
        "notas": "Way. atujuna; *atuyuna (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "awashirüin": {
        "es": "riqueza",
        "fuente": "wayunaiki",
        "notas": "Way. awashirüin; *auachiruin (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "aüliijana": {
        "es": "collar",
        "fuente": "wayunaiki",
        "notas": "Way. aüliijana; *auliyana (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "chajaruuta": {
        "es": "machete",
        "fuente": "wayunaiki",
        "notas": "Way. chajaruuta; *chayaruta (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "che'esaa": {
        "es": "arete",
        "fuente": "wayunaiki",
        "notas": "Way. che'esaa; *cheesa (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "chocho": {
        "es": "trompo",
        "fuente": "wayunaiki",
        "notas": "Way. chocho; *chocho (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "e'ipa": {
        "es": "pedazo, parte",
        "fuente": "wayunaiki",
        "notas": "Way. e'ipa; *eiba (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "e'ipolo": {
        "es": "tapa",
        "fuente": "wayunaiki",
        "notas": "Way. e'ipolo; *eibolo (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "einase": {
        "es": "asiento",
        "fuente": "wayunaiki",
        "notas": "Way. einase; *einase (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "erouse": {
        "es": "tapa, tapón",
        "fuente": "wayunaiki",
        "notas": "Way. erouse; *erouse (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "isira": {
        "es": "maraca",
        "fuente": "wayunaiki",
        "notas": "Way. isira; *isira (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "jaarü": {
        "es": "pocillo, jarra, jarro",
        "fuente": "wayunaiki",
        "notas": "Way. jaarü; *aru (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "jatü": {
        "es": "flecha",
        "fuente": "wayunaiki",
        "notas": "Way. jatü; *atu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "jiirü": {
        "es": "hilo",
        "fuente": "wayunaiki",
        "notas": "Way. jiirü; *yiru (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "jiitpai": {
        "es": "hilaza",
        "fuente": "wayunaiki",
        "notas": "Way. jiitpai; *yitpai (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "jooki": {
        "es": "linterna",
        "fuente": "wayunaiki",
        "notas": "Way. jooki; *oki (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "korolo": {
        "es": "cosa (pertenencia de",
        "fuente": "wayunaiki",
        "notas": "Way. korolo; *corolo (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "maasü": {
        "es": "flauta",
        "fuente": "wayunaiki",
        "notas": "Way. maasü; *masu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "mapase": {
        "es": "cera de abeja",
        "fuente": "wayunaiki",
        "notas": "Way. mapase; *mabase (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "metkaalü": {
        "es": "mercado",
        "fuente": "wayunaiki",
        "notas": "Way. metkaalü; *metcalu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "o'ula": {
        "es": "lecho, hamaca",
        "fuente": "wayunaiki",
        "notas": "Way. o'ula; *oula (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "ooro": {
        "es": "oro",
        "fuente": "wayunaiki",
        "notas": "Way. ooro; *oro (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "otse": {
        "es": "olla",
        "fuente": "wayunaiki",
        "notas": "Way. otse; *otse (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "paa'ata": {
        "es": "cuero",
        "fuente": "wayunaiki",
        "notas": "Way. paa'ata; *paata (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "pisaalü": {
        "es": "bozal",
        "fuente": "wayunaiki",
        "notas": "Way. pisaalü; *pisalu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "piyulu": {
        "es": "bolsa de malla",
        "fuente": "wayunaiki",
        "notas": "Way. piyulu; *piyulu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "polu": {
        "es": "hacha",
        "fuente": "wayunaiki",
        "notas": "Way. polu; *polu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "pootshi": {
        "es": "barro",
        "fuente": "wayunaiki",
        "notas": "Way. pootshi; *potchi (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "rüi": {
        "es": "cuchillo",
        "fuente": "wayunaiki",
        "notas": "Way. rüi; *rui (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "si'ira": {
        "es": "cinturón (del varón)",
        "fuente": "wayunaiki",
        "notas": "Way. si'ira; *siira (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "sirapü": {
        "es": "cinturón (de la mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. sirapü; *sirabu (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "süi": {
        "es": "chinchorro, hamaca",
        "fuente": "wayunaiki",
        "notas": "Way. süi; *sui (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "taapüla": {
        "es": "tabla",
        "fuente": "wayunaiki",
        "notas": "Way. taapüla; *tabula (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "toleeka": {
        "es": "saco, costal",
        "fuente": "wayunaiki",
        "notas": "Way. toleeka; *toleca (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "tu'uma": {
        "es": "piedra preciosa",
        "fuente": "wayunaiki",
        "notas": "Way. tu'uma; *tuuma (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "uwon": {
        "es": "sombrero",
        "fuente": "wayunaiki",
        "notas": "Way. uwon; *uuon (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "wayeeta": {
        "es": "olla",
        "fuente": "wayunaiki",
        "notas": "Way. wayeeta; *bayeta (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },
    "wutia": {
        "es": "aguja",
        "fuente": "wayunaiki",
        "notas": "Way. wutia; *butia (proto-caquetio); Captain & Captain 2005",
        "categoria": "utiles",
    },

    # [verbos]
    "a'ajaa": {
        "es": "quemar",
        "fuente": "wayunaiki",
        "notas": "Way. a'ajaa; *aaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'alijawaa": {
        "es": "estar de parto",
        "fuente": "wayunaiki",
        "notas": "Way. a'alijawaa; *aaliyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'anaa": {
        "es": "armar",
        "fuente": "wayunaiki",
        "notas": "Way. a'anaa; *aana (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'anawaa": {
        "es": "aakkuuaaippa",
        "fuente": "wayunaiki",
        "notas": "Way. a'anawaa; *aanaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'ataa": {
        "es": "a'anawaa",
        "fuente": "wayunaiki",
        "notas": "Way. a'ataa; *aata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'atapajaa": {
        "es": "esperar",
        "fuente": "wayunaiki",
        "notas": "Way. a'atapajaa; *aatabaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'chükütaa": {
        "es": "pisar",
        "fuente": "wayunaiki",
        "notas": "Way. a'chükütaa; *achukuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'ktütajawaa": {
        "es": "sufrir un ataque",
        "fuente": "wayunaiki",
        "notas": "Way. a'ktütajawaa; *aktutayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'waajaa": {
        "es": "alabar",
        "fuente": "wayunaiki",
        "notas": "Way. a'waajaa; *auaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'waataa": {
        "es": "gritar",
        "fuente": "wayunaiki",
        "notas": "Way. a'waataa; *auata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'waatawaa": {
        "es": "jactarse",
        "fuente": "wayunaiki",
        "notas": "Way. a'waatawaa; *auataua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'walakajaa": {
        "es": "dispersar, esparcir",
        "fuente": "wayunaiki",
        "notas": "Way. a'walakajaa; *aualacaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'wanajawaa": {
        "es": "cambiar",
        "fuente": "wayunaiki",
        "notas": "Way. a'wanajawaa; *auanayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'yaataa": {
        "es": "pegar",
        "fuente": "wayunaiki",
        "notas": "Way. a'yaataa; *ayata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'yalajaa": {
        "es": "llorar",
        "fuente": "wayunaiki",
        "notas": "Way. a'yalajaa; *ayalaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'yalajiraa": {
        "es": "tocar (música o",
        "fuente": "wayunaiki",
        "notas": "Way. a'yalajiraa; *ayalayira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'yapüjaa": {
        "es": "coser",
        "fuente": "wayunaiki",
        "notas": "Way. a'yapüjaa; *ayabuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'ülüjaa": {
        "es": "regañar",
        "fuente": "wayunaiki",
        "notas": "Way. a'ülüjaa; *auluya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'ülüjirawaa": {
        "es": "discutir",
        "fuente": "wayunaiki",
        "notas": "Way. a'ülüjirawaa; *auluyiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "a'ürülawaa": {
        "es": "odiar",
        "fuente": "wayunaiki",
        "notas": "Way. a'ürülawaa; *aurulaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aa'ayajirawaa": {
        "es": "discutir",
        "fuente": "wayunaiki",
        "notas": "Way. aa'ayajirawaa; *aayayiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aa'inraa": {
        "es": "hacer",
        "fuente": "wayunaiki",
        "notas": "Way. aa'inraa; *ainra (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aa'inyajaa": {
        "es": "colgar una hamaca",
        "fuente": "wayunaiki",
        "notas": "Way. aa'inyajaa; *ainyaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aakataa": {
        "es": "quitar",
        "fuente": "wayunaiki",
        "notas": "Way. aakataa; *acata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aamüjaa": {
        "es": "ayunar",
        "fuente": "wayunaiki",
        "notas": "Way. aamüjaa; *amuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aapawaa": {
        "es": "tomar, coger",
        "fuente": "wayunaiki",
        "notas": "Way. aapawaa; *abaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aashichijawaa": {
        "es": "enojarse",
        "fuente": "wayunaiki",
        "notas": "Way. aashichijawaa; *achichiyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aawalaa": {
        "es": "aflojar",
        "fuente": "wayunaiki",
        "notas": "Way. aawalaa; *auala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aawalawaa": {
        "es": "aliviarse, mejorarse (fuego)",
        "fuente": "wayunaiki",
        "notas": "Way. aawalawaa; *aualaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achajawaa": {
        "es": "buscar",
        "fuente": "wayunaiki",
        "notas": "Way. achajawaa; *achayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achecheraa": {
        "es": "apretar",
        "fuente": "wayunaiki",
        "notas": "Way. achecheraa; *achechera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achijiraa": {
        "es": "despertar",
        "fuente": "wayunaiki",
        "notas": "Way. achijiraa; *achiyira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achijirawaa": {
        "es": "despertarse",
        "fuente": "wayunaiki",
        "notas": "Way. achijirawaa; *achiyiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achikü": {
        "es": "soltar",
        "fuente": "wayunaiki",
        "notas": "Way. achikü; *achiku (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achitaa": {
        "es": "martillar",
        "fuente": "wayunaiki",
        "notas": "Way. achitaa; *achita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achu'laa": {
        "es": "besar",
        "fuente": "wayunaiki",
        "notas": "Way. achu'laa; *achula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achumajaa": {
        "es": "estar aiwaa",
        "fuente": "wayunaiki",
        "notas": "Way. achumajaa; *achumaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "achuntaa": {
        "es": "pedir",
        "fuente": "wayunaiki",
        "notas": "Way. achuntaa; *achunta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aikkalawaa": {
        "es": "sentarse",
        "fuente": "wayunaiki",
        "notas": "Way. aikkalawaa; *aikcalaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aja'itaa": {
        "es": "recoger agua",
        "fuente": "wayunaiki",
        "notas": "Way. aja'itaa; *ayaita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aja'lajawaa": {
        "es": "terminarse, agotarse",
        "fuente": "wayunaiki",
        "notas": "Way. aja'lajawaa; *ayalayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aja'laje'eraa": {
        "es": "agotar",
        "fuente": "wayunaiki",
        "notas": "Way. aja'laje'eraa; *ayalayeera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aja'ttaa": {
        "es": "terminarse, acabarse",
        "fuente": "wayunaiki",
        "notas": "Way. aja'ttaa; *ayatta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajapulu'uwaa": {
        "es": "estar a cargo de",
        "fuente": "wayunaiki",
        "notas": "Way. ajapulu'uwaa; *ayabuluuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajaraittaa": {
        "es": "halar",
        "fuente": "wayunaiki",
        "notas": "Way. ajaraittaa; *ayaraitta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajataa": {
        "es": "golpear, pegar",
        "fuente": "wayunaiki",
        "notas": "Way. ajataa; *ayata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajuittaa": {
        "es": "salir",
        "fuente": "wayunaiki",
        "notas": "Way. ajuittaa; *ayuitta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajuittiraa": {
        "es": "sacar",
        "fuente": "wayunaiki",
        "notas": "Way. ajuittiraa; *ayuittira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajujawaa": {
        "es": "bostezar",
        "fuente": "wayunaiki",
        "notas": "Way. ajujawaa; *ayuyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajurulajaa": {
        "es": "revolver",
        "fuente": "wayunaiki",
        "notas": "Way. ajurulajaa; *ayurulaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajutaa": {
        "es": "tirar, lanzar",
        "fuente": "wayunaiki",
        "notas": "Way. ajutaa; *ayuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajutuwaa": {
        "es": "caerse",
        "fuente": "wayunaiki",
        "notas": "Way. ajutuwaa; *ayutuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ajuyaajaa": {
        "es": "pedir",
        "fuente": "wayunaiki",
        "notas": "Way. ajuyaajaa; *ayuyaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akacheraa": {
        "es": "colgar",
        "fuente": "wayunaiki",
        "notas": "Way. akacheraa; *acachera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akaijaa": {
        "es": "fumar",
        "fuente": "wayunaiki",
        "notas": "Way. akaijaa; *acaiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akalu'ujaa": {
        "es": "llenar",
        "fuente": "wayunaiki",
        "notas": "Way. akalu'ujaa; *acaluuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akanajaa": {
        "es": "ganar",
        "fuente": "wayunaiki",
        "notas": "Way. akanajaa; *acanaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akatalaa": {
        "es": "separar, apartar",
        "fuente": "wayunaiki",
        "notas": "Way. akatalaa; *acatala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akatalawaa": {
        "es": "apartarse",
        "fuente": "wayunaiki",
        "notas": "Way. akatalawaa; *acatalaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akotchajaa": {
        "es": "ajurulajaa",
        "fuente": "wayunaiki",
        "notas": "Way. akotchajaa; *acotchaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akurulaa": {
        "es": "tener frío",
        "fuente": "wayunaiki",
        "notas": "Way. akurulaa; *akurula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akutkujawaa": {
        "es": "temblar",
        "fuente": "wayunaiki",
        "notas": "Way. akutkujawaa; *akutkuyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "akünülaa": {
        "es": "masticar",
        "fuente": "wayunaiki",
        "notas": "Way. akünülaa; *akunula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alapajaa": {
        "es": "lamentar la muerte de",
        "fuente": "wayunaiki",
        "notas": "Way. alapajaa; *alabaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aleewaa": {
        "es": "tener amistad",
        "fuente": "wayunaiki",
        "notas": "Way. aleewaa; *aleua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alerajaa": {
        "es": "sentir asco por",
        "fuente": "wayunaiki",
        "notas": "Way. alerajaa; *aleraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aliichajaa": {
        "es": "ordeñar",
        "fuente": "wayunaiki",
        "notas": "Way. aliichajaa; *alichaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aliikajawaa": {
        "es": "subir, subirse",
        "fuente": "wayunaiki",
        "notas": "Way. aliikajawaa; *alicayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alumajaa": {
        "es": "amansar (caballo, mula",
        "fuente": "wayunaiki",
        "notas": "Way. alumajaa; *alumaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alü'üjaa": {
        "es": "llevar, cargar, traer",
        "fuente": "wayunaiki",
        "notas": "Way. alü'üjaa; *aluuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alü'ülaa": {
        "es": "acercarse (en el tiempo; a amülaa",
        "fuente": "wayunaiki",
        "notas": "Way. alü'ülaa; *aluula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "alüjaa": {
        "es": "rastrear",
        "fuente": "wayunaiki",
        "notas": "Way. alüjaa; *aluya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amaa": {
        "es": "equivocarse",
        "fuente": "wayunaiki",
        "notas": "Way. amaa; *ama (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amaüsijaa": {
        "es": "domar, amansar",
        "fuente": "wayunaiki",
        "notas": "Way. amaüsijaa; *amausiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amojujaa": {
        "es": "dañar, perjudicar",
        "fuente": "wayunaiki",
        "notas": "Way. amojujaa; *amoyuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amüliajaa": {
        "es": "compadecerse de",
        "fuente": "wayunaiki",
        "notas": "Way. amüliajaa; *amuliaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amüloulii": {
        "es": "perderse",
        "fuente": "wayunaiki",
        "notas": "Way. amüloulii; *amulouli (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "amüschejaa": {
        "es": "atragantarse",
        "fuente": "wayunaiki",
        "notas": "Way. amüschejaa; *amuscheya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anaa": {
        "es": "ser bueno, -na; estar bien",
        "fuente": "wayunaiki",
        "notas": "Way. anaa; *ana (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anachonwaa": {
        "es": "ser bonito, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. anachonwaa; *anachonba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anajaa": {
        "es": "mirar, observar",
        "fuente": "wayunaiki",
        "notas": "Way. anajaa; *anaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anakaa": {
        "es": "alumbrar",
        "fuente": "wayunaiki",
        "notas": "Way. anakaa; *anaca (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "analawaa": {
        "es": "averiguar qué es",
        "fuente": "wayunaiki",
        "notas": "Way. analawaa; *analaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "analüü": {
        "es": "estar mejor de salud",
        "fuente": "wayunaiki",
        "notas": "Way. analüü; *analuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anamiaa": {
        "es": "ser bueno, -na; ser justo, -ta; ser bondadoso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. anamiaa; *anamia (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aneekaa": {
        "es": "escoger",
        "fuente": "wayunaiki",
        "notas": "Way. aneekaa; *aneca (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "anouktaa": {
        "es": "corregir, arreglar",
        "fuente": "wayunaiki",
        "notas": "Way. anouktaa; *anoukta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "antiraa": {
        "es": "traer",
        "fuente": "wayunaiki",
        "notas": "Way. antiraa; *antira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apaajirawaa": {
        "es": "separarse (cada uno",
        "fuente": "wayunaiki",
        "notas": "Way. apaajirawaa; *abayiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apalaalajaa": {
        "es": "ir de compras",
        "fuente": "wayunaiki",
        "notas": "Way. apalaalajaa; *abalalaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apalanajawaa": {
        "es": "fluir",
        "fuente": "wayunaiki",
        "notas": "Way. apalanajawaa; *abalanayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apalirajaa": {
        "es": "mezclar",
        "fuente": "wayunaiki",
        "notas": "Way. apalirajaa; *abaliraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apanapajaa": {
        "es": "encontrarse con una",
        "fuente": "wayunaiki",
        "notas": "Way. apanapajaa; *abanabaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apantajawaa": {
        "es": "irse corriendo",
        "fuente": "wayunaiki",
        "notas": "Way. apantajawaa; *abantayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apasiajawaa": {
        "es": "hacer una visita",
        "fuente": "wayunaiki",
        "notas": "Way. apasiajawaa; *abasiayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apüla": {
        "es": "ser",
        "fuente": "wayunaiki",
        "notas": "Way. apüla; *abula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apülajaa": {
        "es": "prohibir",
        "fuente": "wayunaiki",
        "notas": "Way. apülajaa; *abulaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apünajaa": {
        "es": "sembrar",
        "fuente": "wayunaiki",
        "notas": "Way. apünajaa; *abunaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apütaa": {
        "es": "dejar",
        "fuente": "wayunaiki",
        "notas": "Way. apütaa; *abuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apütawaa": {
        "es": "ser dejado, -da;",
        "fuente": "wayunaiki",
        "notas": "Way. apütawaa; *abutaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "apüttaa": {
        "es": "romperse (algo como",
        "fuente": "wayunaiki",
        "notas": "Way. apüttaa; *abutta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aralajaa": {
        "es": "dejar en remojo",
        "fuente": "wayunaiki",
        "notas": "Way. aralajaa; *aralaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asalajaa": {
        "es": "afilar",
        "fuente": "wayunaiki",
        "notas": "Way. asalajaa; *asalaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asha'walawaa": {
        "es": "ponerse de pie",
        "fuente": "wayunaiki",
        "notas": "Way. asha'walawaa; *achaualaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashaittaa": {
        "es": "jugar",
        "fuente": "wayunaiki",
        "notas": "Way. ashaittaa; *achaitta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashantajaa": {
        "es": "adivinar (por",
        "fuente": "wayunaiki",
        "notas": "Way. ashantajaa; *achantaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashapatawaa": {
        "es": "preocuparse",
        "fuente": "wayunaiki",
        "notas": "Way. ashapatawaa; *achabataua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashataa": {
        "es": "sanar (una herida)",
        "fuente": "wayunaiki",
        "notas": "Way. ashataa; *achata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashe'ejirawaa": {
        "es": "pelear con puños",
        "fuente": "wayunaiki",
        "notas": "Way. ashe'ejirawaa; *acheeyiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashe'etaa": {
        "es": "golpear, patear",
        "fuente": "wayunaiki",
        "notas": "Way. ashe'etaa; *acheeta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashiitaa": {
        "es": "orinar",
        "fuente": "wayunaiki",
        "notas": "Way. ashiitaa; *achita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashijawaa": {
        "es": "lavar (ropa)",
        "fuente": "wayunaiki",
        "notas": "Way. ashijawaa; *achiyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashottaa": {
        "es": "cortar (con ataralawaa",
        "fuente": "wayunaiki",
        "notas": "Way. ashottaa; *achotta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ashutaa": {
        "es": "meterse, entrar a la",
        "fuente": "wayunaiki",
        "notas": "Way. ashutaa; *achuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asiiyajawaa": {
        "es": "ensillar",
        "fuente": "wayunaiki",
        "notas": "Way. asiiyajawaa; *asiyayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asijaa": {
        "es": "asar",
        "fuente": "wayunaiki",
        "notas": "Way. asijaa; *asiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asirajaa": {
        "es": "reirse",
        "fuente": "wayunaiki",
        "notas": "Way. asirajaa; *asiraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asiranajawaa": {
        "es": "resbalarse",
        "fuente": "wayunaiki",
        "notas": "Way. asiranajawaa; *asiranayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asiwataa": {
        "es": "desatar",
        "fuente": "wayunaiki",
        "notas": "Way. asiwataa; *asiuata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asouktaa": {
        "es": "responder",
        "fuente": "wayunaiki",
        "notas": "Way. asouktaa; *asoukta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asukaa": {
        "es": "recoger leña",
        "fuente": "wayunaiki",
        "notas": "Way. asukaa; *asuca (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asü'ütaa": {
        "es": "arrancar",
        "fuente": "wayunaiki",
        "notas": "Way. asü'ütaa; *asuuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "asüküitaa": {
        "es": "rasgarse",
        "fuente": "wayunaiki",
        "notas": "Way. asüküitaa; *asukuita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ataa": {
        "es": "atragantarse",
        "fuente": "wayunaiki",
        "notas": "Way. ataa; *ata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atamawaa": {
        "es": "levantarse",
        "fuente": "wayunaiki",
        "notas": "Way. atamawaa; *atamaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ataüjawaa": {
        "es": "violar (a una mujer)",
        "fuente": "wayunaiki",
        "notas": "Way. ataüjawaa; *atauyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atkawaa": {
        "es": "pelear",
        "fuente": "wayunaiki",
        "notas": "Way. atkawaa; *atcaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atpajaa": {
        "es": "recolectar (alimento)",
        "fuente": "wayunaiki",
        "notas": "Way. atpajaa; *atpaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atüjaa": {
        "es": "saber",
        "fuente": "wayunaiki",
        "notas": "Way. atüjaa; *atuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atükawaa": {
        "es": "atascarse",
        "fuente": "wayunaiki",
        "notas": "Way. atükawaa; *atucaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "atütüjaa": {
        "es": "animar, ayolojo",
        "fuente": "wayunaiki",
        "notas": "Way. atütüjaa; *atutuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "awajawaa": {
        "es": "rajarse, partirse",
        "fuente": "wayunaiki",
        "notas": "Way. awajawaa; *auayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "awareejaa": {
        "es": "barrer",
        "fuente": "wayunaiki",
        "notas": "Way. awareejaa; *auareya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "awatawaa": {
        "es": "correr",
        "fuente": "wayunaiki",
        "notas": "Way. awatawaa; *auataua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ayaawataa": {
        "es": "reconocer",
        "fuente": "wayunaiki",
        "notas": "Way. ayaawataa; *ayauata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ayaleraa": {
        "es": "levantar, alzar",
        "fuente": "wayunaiki",
        "notas": "Way. ayaleraa; *ayalera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ayoujirawaa": {
        "es": "competir",
        "fuente": "wayunaiki",
        "notas": "Way. ayoujirawaa; *ayouyiraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ayounjaa": {
        "es": "azotar",
        "fuente": "wayunaiki",
        "notas": "Way. ayounjaa; *ayounya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ayüüjawaa": {
        "es": "moler",
        "fuente": "wayunaiki",
        "notas": "Way. ayüüjawaa; *ayuuyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aüjaa": {
        "es": "cortar (el pelo), afeitar",
        "fuente": "wayunaiki",
        "notas": "Way. aüjaa; *auya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aüjawaa": {
        "es": "matar (ganado)",
        "fuente": "wayunaiki",
        "notas": "Way. aüjawaa; *auyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "aürülaa": {
        "es": "estar flaco, -ca",
        "fuente": "wayunaiki",
        "notas": "Way. aürülaa; *aurula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "chuwataa": {
        "es": "estar encendido, -da;",
        "fuente": "wayunaiki",
        "notas": "Way. chuwataa; *chuuata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'iijaa": {
        "es": "tener diarrea",
        "fuente": "wayunaiki",
        "notas": "Way. e'iijaa; *eiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'iitaa": {
        "es": "defecar",
        "fuente": "wayunaiki",
        "notas": "Way. e'iitaa; *eita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'ikaa": {
        "es": "enseñar, instruir",
        "fuente": "wayunaiki",
        "notas": "Way. e'ikaa; *eica (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'ikajawaa": {
        "es": "llevar y dejar",
        "fuente": "wayunaiki",
        "notas": "Way. e'ikajawaa; *eicayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'ikawaa": {
        "es": "estar herido, -da",
        "fuente": "wayunaiki",
        "notas": "Way. e'ikawaa; *eicaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'inaa": {
        "es": "tejer con aguja",
        "fuente": "wayunaiki",
        "notas": "Way. e'inaa; *eina (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'ipünawaa": {
        "es": "llevar y dejar de",
        "fuente": "wayunaiki",
        "notas": "Way. e'ipünawaa; *eibunaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'itaa": {
        "es": "aportar",
        "fuente": "wayunaiki",
        "notas": "Way. e'itaa; *eita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'itawaa": {
        "es": "poner, meter",
        "fuente": "wayunaiki",
        "notas": "Way. e'itawaa; *eitaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'raajaa": {
        "es": "conocer",
        "fuente": "wayunaiki",
        "notas": "Way. e'raajaa; *eraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'rajaa": {
        "es": "mirar",
        "fuente": "wayunaiki",
        "notas": "Way. e'rajaa; *eraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "e'rajawaa": {
        "es": "mirar, observar",
        "fuente": "wayunaiki",
        "notas": "Way. e'rajawaa; *erayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ee'iranajawaa": {
        "es": "cambiar",
        "fuente": "wayunaiki",
        "notas": "Way. ee'iranajawaa; *eiranayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ee'irataa": {
        "es": "cambiar",
        "fuente": "wayunaiki",
        "notas": "Way. ee'irataa; *eirata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ee'iratawaa": {
        "es": "cambiar de esposo, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. ee'iratawaa; *eirataua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eewaa": {
        "es": "haber, existir",
        "fuente": "wayunaiki",
        "notas": "Way. eewaa; *eua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eewawaa": {
        "es": "accidentarse",
        "fuente": "wayunaiki",
        "notas": "Way. eewawaa; *euawa (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eimalawaa": {
        "es": "ekiipala n",
        "fuente": "wayunaiki",
        "notas": "Way. eimalawaa; *eimalaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eipiraa": {
        "es": "perseguir",
        "fuente": "wayunaiki",
        "notas": "Way. eipiraa; *eibira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eirakawaa": {
        "es": "mirar",
        "fuente": "wayunaiki",
        "notas": "Way. eirakawaa; *eiracaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eisalawaa": {
        "es": "acostarse",
        "fuente": "wayunaiki",
        "notas": "Way. eisalawaa; *eisalaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eitajaa": {
        "es": "repartir",
        "fuente": "wayunaiki",
        "notas": "Way. eitajaa; *eitaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eite'eraa": {
        "es": "devolver",
        "fuente": "wayunaiki",
        "notas": "Way. eite'eraa; *eiteera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eiyajaa": {
        "es": "curar",
        "fuente": "wayunaiki",
        "notas": "Way. eiyajaa; *eiyaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ejejerawaa": {
        "es": "cuchichear, secretear",
        "fuente": "wayunaiki",
        "notas": "Way. ejejerawaa; *eyeyeraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ejemplo": {
        "es": "estar cerrado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. ejemplo; *eyemplo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ejetaa": {
        "es": "escupir",
        "fuente": "wayunaiki",
        "notas": "Way. ejetaa; *eyeta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ejitaa": {
        "es": "verter (polvos o granos)",
        "fuente": "wayunaiki",
        "notas": "Way. ejitaa; *eyita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ejittawaa": {
        "es": "atar",
        "fuente": "wayunaiki",
        "notas": "Way. ejittawaa; *eyittaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ekerojiraa": {
        "es": "meter",
        "fuente": "wayunaiki",
        "notas": "Way. ekerojiraa; *eceroyira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ekii": {
        "es": "dolerle la cabeza",
        "fuente": "wayunaiki",
        "notas": "Way. ekii; *eki (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ekirajaa": {
        "es": "enseñar",
        "fuente": "wayunaiki",
        "notas": "Way. ekirajaa; *ekiraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eme'erajawaa": {
        "es": "bromear",
        "fuente": "wayunaiki",
        "notas": "Way. eme'erajawaa; *emeerayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "epejawaa": {
        "es": "prender, encender",
        "fuente": "wayunaiki",
        "notas": "Way. epejawaa; *ebeyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "epettaa": {
        "es": "tocar",
        "fuente": "wayunaiki",
        "notas": "Way. epettaa; *ebetta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "epirajaa": {
        "es": "llenar, inflar",
        "fuente": "wayunaiki",
        "notas": "Way. epirajaa; *ebiraya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "epitanajaa": {
        "es": "barrer",
        "fuente": "wayunaiki",
        "notas": "Way. epitanajaa; *ebitanaya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "eweetaa": {
        "es": "salir a la vista, aparecer",
        "fuente": "wayunaiki",
        "notas": "Way. eweetaa; *eueta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ewiijaa": {
        "es": "silbar",
        "fuente": "wayunaiki",
        "notas": "Way. ewiijaa; *euiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ichee": {
        "es": "estar tenso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. ichee; *iche (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "iraa": {
        "es": "ser insípido, -da; tener poco unaquemadura",
        "fuente": "wayunaiki",
        "notas": "Way. iraa; *ira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ishaa": {
        "es": "sufrir una quemadura",
        "fuente": "wayunaiki",
        "notas": "Way. ishaa; *icha (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "itaa": {
        "es": "secarse",
        "fuente": "wayunaiki",
        "notas": "Way. itaa; *ita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "iwaa": {
        "es": "ser prostituta",
        "fuente": "wayunaiki",
        "notas": "Way. iwaa; *iua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ja'ijawaa": {
        "es": "faltar",
        "fuente": "wayunaiki",
        "notas": "Way. ja'ijawaa; *aiyaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ja'iwaa": {
        "es": "estar caliente",
        "fuente": "wayunaiki",
        "notas": "Way. ja'iwaa; *aiua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ja'yaa": {
        "es": "aparecer",
        "fuente": "wayunaiki",
        "notas": "Way. ja'yaa; *aya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ja'yumuu": {
        "es": "estar bien",
        "fuente": "wayunaiki",
        "notas": "Way. ja'yumuu; *ayumu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jalaa": {
        "es": "dónde estar",
        "fuente": "wayunaiki",
        "notas": "Way. jalaa; *ala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jamaamaa": {
        "es": "ser liviano, -na",
        "fuente": "wayunaiki",
        "notas": "Way. jamaamaa; *amama (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "japülii": {
        "es": "tener vergüenza",
        "fuente": "wayunaiki",
        "notas": "Way. japülii; *abuli (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jashü'üwaa": {
        "es": "ser agrio, -a",
        "fuente": "wayunaiki",
        "notas": "Way. jashü'üwaa; *achuuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jawa'awaa": {
        "es": "estar flojo, -ja",
        "fuente": "wayunaiki",
        "notas": "Way. jawa'awaa; *auaaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jawataa": {
        "es": "ser pesado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. jawataa; *auata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jayaa": {
        "es": "ser barato, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. jayaa; *aya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "je'wee": {
        "es": "estar maduro, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. je'wee; *yeue (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jemetaa": {
        "es": "ser sabroso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. jemetaa; *yemeta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jera": {
        "es": "cuánto ser",
        "fuente": "wayunaiki",
        "notas": "Way. jera; *yera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jerottaa": {
        "es": "ser brillante; ser claro, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. jerottaa; *yerotta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jerulaa": {
        "es": "ser ancho, -cha",
        "fuente": "wayunaiki",
        "notas": "Way. jerulaa; *yerula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jimataa": {
        "es": "estar quieto, -ta; estar",
        "fuente": "wayunaiki",
        "notas": "Way. jimataa; *yimata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jolotoo": {
        "es": "tener ampolla",
        "fuente": "wayunaiki",
        "notas": "Way. jolotoo; *oloto (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "josoo": {
        "es": "estar seco, -ca",
        "fuente": "wayunaiki",
        "notas": "Way. josoo; *oso (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jotaa": {
        "es": "arder",
        "fuente": "wayunaiki",
        "notas": "Way. jotaa; *ota (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "joulaa": {
        "es": "ser mucho, -cha; ser",
        "fuente": "wayunaiki",
        "notas": "Way. joulaa; *oula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "joyotoo": {
        "es": "estar sentado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. joyotoo; *oyoto (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jutataa": {
        "es": "estar abierto, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. jutataa; *utata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "jüüjüwaa": {
        "es": "ser obediente; ser",
        "fuente": "wayunaiki",
        "notas": "Way. jüüjüwaa; *uuyuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ka'lee": {
        "es": "ser grueso, -sa (de objetos",
        "fuente": "wayunaiki",
        "notas": "Way. ka'lee; *cale (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ka'wayuusee": {
        "es": "tener esposo, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. ka'wayuusee; *cauayuse (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ka'yataa": {
        "es": "estar un poco retirado",
        "fuente": "wayunaiki",
        "notas": "Way. ka'yataa; *cayata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kaa'inwaa": {
        "es": "ser arisco, -ca; ser",
        "fuente": "wayunaiki",
        "notas": "Way. kaa'inwaa; *cainba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kaainjalaa": {
        "es": "causar daño, pecar",
        "fuente": "wayunaiki",
        "notas": "Way. kaainjalaa; *cainyala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kachetaa": {
        "es": "estar colgado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. kachetaa; *cacheta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kakaliaa": {
        "es": "llevar; ser juicioso, -sa; ser prudente",
        "fuente": "wayunaiki",
        "notas": "Way. kakaliaa; *cacalia (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kakuaa": {
        "es": "ser veloz (andando)",
        "fuente": "wayunaiki",
        "notas": "Way. kakuaa; *cakua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kalu'uwaa": {
        "es": "contener",
        "fuente": "wayunaiki",
        "notas": "Way. kalu'uwaa; *caluuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kamanewaa": {
        "es": "ser amable; ser katsüinwaa, katsinwaa",
        "fuente": "wayunaiki",
        "notas": "Way. kamanewaa; *camaneua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kanüliaa": {
        "es": "ser llamado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. kanüliaa; *canulia (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kapüü": {
        "es": "estar atado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. kapüü; *cabuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kasaa": {
        "es": "tener filo",
        "fuente": "wayunaiki",
        "notas": "Way. kasaa; *casa (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kasewaa": {
        "es": "ser ruidoso, -sa; ser sabio, -bia",
        "fuente": "wayunaiki",
        "notas": "Way. kasewaa; *caseua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kashüülaa": {
        "es": "ser feo, fea; ser",
        "fuente": "wayunaiki",
        "notas": "Way. kashüülaa; *cachuula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "katchinwaa": {
        "es": "ser fuerte",
        "fuente": "wayunaiki",
        "notas": "Way. katchinwaa; *catchinba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "keemaa": {
        "es": "ser",
        "fuente": "wayunaiki",
        "notas": "Way. keemaa; *cema (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "keenaa": {
        "es": "derramarse",
        "fuente": "wayunaiki",
        "notas": "Way. keenaa; *cena (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kekiiwaa": {
        "es": "ser inteligente; ser",
        "fuente": "wayunaiki",
        "notas": "Way. kekiiwaa; *cekiua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kerawaa": {
        "es": "estar terminado, -da; objeto)",
        "fuente": "wayunaiki",
        "notas": "Way. kerawaa; *ceraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kettawaa": {
        "es": "estar terminado, -da;",
        "fuente": "wayunaiki",
        "notas": "Way. kettawaa; *cettaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kisaawaa": {
        "es": "estar guisado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. kisaawaa; *kisaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ko'oyowaa": {
        "es": "ser redondo, -da",
        "fuente": "wayunaiki",
        "notas": "Way. ko'oyowaa; *cooyoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ko'utaa": {
        "es": "estar callado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. ko'utaa; *couta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kojoo": {
        "es": "ser espeso, -sa; ser denso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. kojoo; *coyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kojutaa": {
        "es": "ser caro, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. kojutaa; *coyuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "kojuyaa": {
        "es": "ser varios, -rias; haber ku'lupucho'u, ku'lupüchü'i",
        "fuente": "wayunaiki",
        "notas": "Way. kojuyaa; *coyuya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "koojaa": {
        "es": "pincharse",
        "fuente": "wayunaiki",
        "notas": "Way. koojaa; *coya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "la'walawaa": {
        "es": "ser flexible",
        "fuente": "wayunaiki",
        "notas": "Way. la'walawaa; *laualaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "lakayawaa": {
        "es": "ser redondo, -da",
        "fuente": "wayunaiki",
        "notas": "Way. lakayawaa; *lacayaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "laüktaa": {
        "es": "ser grueso, -sa (de luma",
        "fuente": "wayunaiki",
        "notas": "Way. laüktaa; *laukta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "lemtaa": {
        "es": "arrastrarse",
        "fuente": "wayunaiki",
        "notas": "Way. lemtaa; *lemta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "lotaa": {
        "es": "ser recto, -ta",
        "fuente": "wayunaiki",
        "notas": "Way. lotaa; *lota (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "maa'inwaa": {
        "es": "ser necio, -cia",
        "fuente": "wayunaiki",
        "notas": "Way. maa'inwaa; *mainba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mache'ewaa": {
        "es": "ser sordo, -da",
        "fuente": "wayunaiki",
        "notas": "Way. mache'ewaa; *macheeua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "maittaa": {
        "es": "estar en calma el tiempo",
        "fuente": "wayunaiki",
        "notas": "Way. maittaa; *maitta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "malaa": {
        "es": "ser tonto, -ta; ser bobo, -ba",
        "fuente": "wayunaiki",
        "notas": "Way. malaa; *mala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mamainnaa": {
        "es": "ser loco, -ca",
        "fuente": "wayunaiki",
        "notas": "Way. mamainnaa; *mamainna (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mapülewaa": {
        "es": "ser fácil",
        "fuente": "wayunaiki",
        "notas": "Way. mapülewaa; *mabuleua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "maralüü": {
        "es": "ser estéril",
        "fuente": "wayunaiki",
        "notas": "Way. maralüü; *maraluu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mariiyaa": {
        "es": "ser amarillo, -lla",
        "fuente": "wayunaiki",
        "notas": "Way. mariiyaa; *mariya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "matsüinwaa": {
        "es": "estar sin fuerza",
        "fuente": "wayunaiki",
        "notas": "Way. matsüinwaa; *matsuinba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mayeinwaa": {
        "es": "estar grave (de",
        "fuente": "wayunaiki",
        "notas": "Way. mayeinwaa; *mayeinba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "miyaasüü": {
        "es": "tener sed",
        "fuente": "wayunaiki",
        "notas": "Way. miyaasüü; *miyasuu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mmoluu": {
        "es": "tener 2",
        "fuente": "wayunaiki",
        "notas": "Way. mmoluu; *molu (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mo'uu": {
        "es": "ser ciego, -ga",
        "fuente": "wayunaiki",
        "notas": "Way. mo'uu; *mou (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mojulawaa": {
        "es": "ser malo, -la (de mujuu",
        "fuente": "wayunaiki",
        "notas": "Way. mojulawaa; *moyulaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "moulii": {
        "es": "ser angosto, -ta; ser",
        "fuente": "wayunaiki",
        "notas": "Way. moulii; *mouli (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "mütsiiyaa": {
        "es": "ser negro, -gra",
        "fuente": "wayunaiki",
        "notas": "Way. mütsiiyaa; *mutsiya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "naataa": {
        "es": "ser ajeno, -na; ser nneerü",
        "fuente": "wayunaiki",
        "notas": "Way. naataa; *nata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'otojowaa": {
        "es": "sacudir",
        "fuente": "wayunaiki",
        "notas": "Way. o'otojowaa; *ootoyoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'otowaa": {
        "es": "montar",
        "fuente": "wayunaiki",
        "notas": "Way. o'otowaa; *ootoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'ttaa": {
        "es": "aterrizar",
        "fuente": "wayunaiki",
        "notas": "Way. o'ttaa; *otta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'tte'eraa": {
        "es": "hacer pasar",
        "fuente": "wayunaiki",
        "notas": "Way. o'tte'eraa; *otteera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'ulijaa": {
        "es": "cargar (a un niño)",
        "fuente": "wayunaiki",
        "notas": "Way. o'ulijaa; *ouliya (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'uniraa": {
        "es": "llevar",
        "fuente": "wayunaiki",
        "notas": "Way. o'uniraa; *ounira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'utaa": {
        "es": "ser",
        "fuente": "wayunaiki",
        "notas": "Way. o'utaa; *outa (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'yotoo": {
        "es": "verter (un líquido)",
        "fuente": "wayunaiki",
        "notas": "Way. o'yotoo; *oyoto (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "o'yotowaa": {
        "es": "cortar (con cuchillo, abdomen)",
        "fuente": "wayunaiki",
        "notas": "Way. o'yotowaa; *oyotoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojoitaa": {
        "es": "enterrar",
        "fuente": "wayunaiki",
        "notas": "Way. ojoitaa; *oyoita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojotaa": {
        "es": "botar (un grupo o montón",
        "fuente": "wayunaiki",
        "notas": "Way. ojotaa; *oyota (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojottaa": {
        "es": "morder",
        "fuente": "wayunaiki",
        "notas": "Way. ojottaa; *oyotta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojununtawaa": {
        "es": "o'ktaa",
        "fuente": "wayunaiki",
        "notas": "Way. ojununtawaa; *oyununtaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojuttaa": {
        "es": "caer",
        "fuente": "wayunaiki",
        "notas": "Way. ojuttaa; *oyutta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ojuttiraa": {
        "es": "derribar, 2",
        "fuente": "wayunaiki",
        "notas": "Way. ojuttiraa; *oyuttira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oko'oloo": {
        "es": "envolver",
        "fuente": "wayunaiki",
        "notas": "Way. oko'oloo; *ocoolo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "okolojoo": {
        "es": "llevar regalo",
        "fuente": "wayunaiki",
        "notas": "Way. okolojoo; *ocoloyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oo'ui": {
        "es": "tropezar",
        "fuente": "wayunaiki",
        "notas": "Way. oo'ui; *oui (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oo'ulawaa": {
        "es": "dejar",
        "fuente": "wayunaiki",
        "notas": "Way. oo'ulawaa; *oulaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oojoo": {
        "es": "raspar",
        "fuente": "wayunaiki",
        "notas": "Way. oojoo; *oyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oonojoo": {
        "es": "toser",
        "fuente": "wayunaiki",
        "notas": "Way. oonojoo; *onoyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ooroloo": {
        "es": "estar hinchado (el",
        "fuente": "wayunaiki",
        "notas": "Way. ooroloo; *orolo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oosojowaa": {
        "es": "secarse",
        "fuente": "wayunaiki",
        "notas": "Way. oosojowaa; *osoyoua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ootojoo": {
        "es": "perforar",
        "fuente": "wayunaiki",
        "notas": "Way. ootojoo; *otoyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "opoolojoo": {
        "es": "hervir",
        "fuente": "wayunaiki",
        "notas": "Way. opoolojoo; *oboloyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "opootaa": {
        "es": "atascarse (en el barro o conocimiento, desmayarse",
        "fuente": "wayunaiki",
        "notas": "Way. opootaa; *obota (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oshojoo": {
        "es": "desollar, pelar, curandero, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. oshojoo; *ochoyo (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ounjulaa": {
        "es": "esconder",
        "fuente": "wayunaiki",
        "notas": "Way. ounjulaa; *ounyula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ounjulawaa": {
        "es": "esconderse",
        "fuente": "wayunaiki",
        "notas": "Way. ounjulawaa; *ounyulaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ountaa": {
        "es": "poder",
        "fuente": "wayunaiki",
        "notas": "Way. ountaa; *ounta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ourulaa": {
        "es": "estar hinchado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. ourulaa; *ourula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ousaa": {
        "es": "deshierbar, arar, rozar (un",
        "fuente": "wayunaiki",
        "notas": "Way. ousaa; *ousa (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "oushuwaa": {
        "es": "tener fiebre",
        "fuente": "wayunaiki",
        "notas": "Way. oushuwaa; *ouchuua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "ouyantaa": {
        "es": "volver",
        "fuente": "wayunaiki",
        "notas": "Way. ouyantaa; *ouyanta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "paa'inwaa": {
        "es": "estar de acuerdo",
        "fuente": "wayunaiki",
        "notas": "Way. paa'inwaa; *painba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "palastaa": {
        "es": "estar acostado, -da; estar pentaana, wentaana ventana",
        "fuente": "wayunaiki",
        "notas": "Way. palastaa; *palasta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "palawaa": {
        "es": "ser salado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. palawaa; *palaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "palirawaa": {
        "es": "estar mezclado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. palirawaa; *paliraua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "pansawaa": {
        "es": "estar derecho, -cha",
        "fuente": "wayunaiki",
        "notas": "Way. pansawaa; *pansaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "pejee": {
        "es": "estar cerca",
        "fuente": "wayunaiki",
        "notas": "Way. pejee; *peye (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "peraa": {
        "es": "ser mocho, -cha",
        "fuente": "wayunaiki",
        "notas": "Way. peraa; *pera (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "pülaa": {
        "es": "ser poderoso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. pülaa; *pula (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "püreesaa": {
        "es": "estar preso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. püreesaa; *puresa (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "saamataa": {
        "es": "estar frío, fría; estar seita",
        "fuente": "wayunaiki",
        "notas": "Way. saamataa; *samata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "sha'wataa": {
        "es": "estar parado, -da; estar",
        "fuente": "wayunaiki",
        "notas": "Way. sha'wataa; *chauata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "shitaa": {
        "es": "estar hinchado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. shitaa; *chita (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "shokotaa": {
        "es": "ser curvo, -va",
        "fuente": "wayunaiki",
        "notas": "Way. shokotaa; *chocota (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "shottaa": {
        "es": "gotear",
        "fuente": "wayunaiki",
        "notas": "Way. shottaa; *chotta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "sirasiraa": {
        "es": "ser liso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. sirasiraa; *sirasira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "sirataa": {
        "es": "ser liso, -sa",
        "fuente": "wayunaiki",
        "notas": "Way. sirataa; *sirata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "taashii": {
        "es": "estar libre; estar suelto, -ta; estar disponible",
        "fuente": "wayunaiki",
        "notas": "Way. taashii; *tachi (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "talataa": {
        "es": "estar alegre; estar chotacabras",
        "fuente": "wayunaiki",
        "notas": "Way. talataa; *talata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "tuttaa": {
        "es": "tener fiebre",
        "fuente": "wayunaiki",
        "notas": "Way. tuttaa; *tutta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "tütaa": {
        "es": "ser trabajador, -dora; ser",
        "fuente": "wayunaiki",
        "notas": "Way. tütaa; *tuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "waawataa": {
        "es": "soplar (el viento)",
        "fuente": "wayunaiki",
        "notas": "Way. waawataa; *bauata (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "walawaa": {
        "es": "estar pagado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. walawaa; *balaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "wanaawaa": {
        "es": "ser lo mismo, ser",
        "fuente": "wayunaiki",
        "notas": "Way. wanaawaa; *banaua (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "waneepiaa": {
        "es": "ser entero, -ra; ser",
        "fuente": "wayunaiki",
        "notas": "Way. waneepiaa; *banebia (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "wotoo": {
        "es": "estar lleno, -na (de",
        "fuente": "wayunaiki",
        "notas": "Way. wotoo; *boto (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "wüinsiraa": {
        "es": "ahogarse (en agua)",
        "fuente": "wayunaiki",
        "notas": "Way. wüinsiraa; *buinsira (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "wüittaa": {
        "es": "ser azul, ser verde",
        "fuente": "wayunaiki",
        "notas": "Way. wüittaa; *buitta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "yalayalaa": {
        "es": "ser áspero, -ra",
        "fuente": "wayunaiki",
        "notas": "Way. yalayalaa; *yalayala (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "yapaa": {
        "es": "estar listo, -ta; estar",
        "fuente": "wayunaiki",
        "notas": "Way. yapaa; *yaba (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "yarüttaa": {
        "es": "estar sucio",
        "fuente": "wayunaiki",
        "notas": "Way. yarüttaa; *yarutta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },
    "yokutaa": {
        "es": "estar apagado, -da",
        "fuente": "wayunaiki",
        "notas": "Way. yokutaa; *yokuta (proto-caquetio); Captain & Captain 2005",
        "categoria": "verbos",
    },


    # --- Taíno hipotético (arahuaco_comparative.py) ---
    "abba": {
        "es": "uno",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. abba; método comparativo arahuacano; Reconstrucción desde Lok. abba (uno); método comparativo arahuaco; confianza: alta",
        "categoria": "gramatica"
    },
    "acoa": {
        "es": "pie",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. akoa; método comparativo arahuacano; Reconstrucción desde Lok. akoa (pie); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "aduri": {
        "es": "nariz",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. aduri; método comparativo arahuacano; Reconstrucción desde Lok. aduri (nariz); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "agari": {
        "es": "cabeza",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. abari; método comparativo arahuacano; Reconstrucción desde Lok. abari (cabeza); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "akcicyaa": {
        "es": "espíritu vital",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. akkicyaha; método comparativo arahuacano; Reconstrucción desde Lok. akkicyaha (espíritu vital); método comparativo arahuaco; confianza: alta",
        "categoria": "ritual"
    },
    "cai": {
        "es": "isla",
        "fuente": "taino",
        "notas": "Taíno atestiguado: cai; cognado Lok. kairi; Brinton 1871",
        "categoria": "geografia"
    },
    "caiman": {
        "es": "caimán",
        "fuente": "taino",
        "notas": "Taíno atestiguado: caiman; cognado Lok. kaiman; Brinton 1871",
        "categoria": "fauna"
    },
    "casabe": {
        "es": "casabe",
        "fuente": "taino",
        "notas": "Taíno atestiguado: casabe; cognado Lok. kasabi; Brinton 1871",
        "categoria": "alimentos"
    },
    "cohiba": {
        "es": "tabaco",
        "fuente": "taino",
        "notas": "Taíno atestiguado: cohiba; cognado Lok. iuli; Brinton 1871",
        "categoria": "ritual"
    },
    "daca": {
        "es": "mano",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. daka; método comparativo arahuacano; Reconstrucción desde Lok. daka (mano); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "higuana": {
        "es": "iguana",
        "fuente": "taino",
        "notas": "Taíno atestiguado: higuana; cognado Lok. iwana; Brinton 1871",
        "categoria": "fauna"
    },
    "mayani": {
        "es": "no, negación",
        "fuente": "taino",
        "notas": "Taíno atestiguado: mayani; cognado Lok. ma; Brinton 1871",
        "categoria": "gramatica"
    },
    "taita": {
        "es": "padre",
        "fuente": "taino",
        "notas": "Taíno atestiguado: taita; cognado Lok. itti; Brinton 1871",
        "categoria": "parentesco"
    },
    "thigisi": {
        "es": "diente",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. thibisi; método comparativo arahuacano; Reconstrucción desde Lok. thibisi (diente); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "tuna": {
        "es": "agua, río",
        "fuente": "taino",
        "notas": "Taíno atestiguado: tuna; cognado Lok. tuna; Brinton 1871",
        "categoria": "geografia"
    },
    "wacusi": {
        "es": "ojo",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. wakusi; método comparativo arahuacano; Reconstrucción desde Lok. wakusi (ojo); método comparativo arahuaco; confianza: alta",
        "categoria": "cuerpo"
    },
    "wagulo": {
        "es": "tortuga",
        "fuente": "taino",
        "notas": "Reconstrucción hipotética Taíno desde Lok. wabulo; método comparativo arahuacano; Reconstrucción desde Lok. wabulo (tortuga); método comparativo arahuaco; confianza: alta",
        "categoria": "fauna"
    },
    "yamosa": {
        "es": "dos",
        "fuente": "taino",
        "notas": "Taíno atestiguado: yamosa; cognado Lok. biama; Brinton 1871",
        "categoria": "gramatica"
    },

    # --- Proto-arahuaco reconstruido (arahuaco_comparative.py) ---
    "hamaka": {
        "es": "hamaca, cama colgante",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *hamaka; atestiguada en 3 lenguas: CQ: hamaca, LK: hamaha, TN: hamaca; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },
    "isikoa": {
        "es": "casa, vivienda",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *isikoa; atestiguada en 2 lenguas: LK: sikoa, TN: bohio; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },
    "kanoa": {
        "es": "canoa, embarcación",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *kanoa; atestiguada en 3 lenguas: CQ: canoa, LK: kannoa, TN: canoa; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },
    "kati": {
        "es": "luna",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *kati; atestiguada en 3 lenguas: CQ: cati, WY: kachi, LK: katsi; Payne (1991), Brinton (1871)",
        "categoria": "cosmos"
    },
    "para": {
        "es": "mar, agua extensa",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *para; atestiguada en 4 lenguas: CQ: para, WY: palaa, LK: bara, TN: bagua; Payne (1991), Brinton (1871)",
        "categoria": "geografia"
    },
    "piay": {
        "es": "chamán, curandero, piache",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *piay; atestiguada en 3 lenguas: CQ: piache, LK: piaye, TN: bejique; Payne (1991), Brinton (1871)",
        "categoria": "ritual"
    },
    "sallaba": {
        "es": "sabana, llanura",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *sallaba; atestiguada en 2 lenguas: LK: sallaban, TN: sabana; Payne (1991), Brinton (1871)",
        "categoria": "geografia"
    },

    # ── KALINAGO — SUSTRATO ARAHUACO (Breton 1665; Taylor 1951; Hoff 1968) ──
    "kati-kalinago":     {"es": "luna, mes", "fuente": "kalinago", "notas": "Breton (1665) kati/mois; cognado directo de CQ cati, LK katsi, PA *kati. Sufijo -kalinago: colisión con entrada caquetío 'kati' (cati) ya existente bajo otra forma", "categoria": "cosmos"},
    "barana":   {"es": "mar, agua extensa", "fuente": "kalinago", "notas": "Garifuna barana = gran cuerpo de agua; cognado de CQ para, LK bara, PA *para", "categoria": "geografia"},
    "kasabi-kalinago":   {"es": "casabe, pan de yuca", "fuente": "kalinago", "notas": "Kalinago kasabi; idéntico a LK kasabi, CQ casabe; término central de la identidad cultural. Sufijo -kalinago: colisión de clave con entrada lokono 'kasabi' preexistente", "categoria": "alimentos"},
    "buyei":    {"es": "chamán, curandero ritual", "fuente": "kalinago", "notas": "Breton (1665) buyei; cognado irregular de LK piaye (p→b, ia→u, ye→ei); figura ritual paralela al piache caquetío", "categoria": "cosmos"},
    "iwana-kalinago":    {"es": "iguana (Iguana iguana)", "fuente": "kalinago", "notas": "Garifuna iwana; conservado igual que LK iwana, WY iwana, PA *iwana. Sufijo -kalinago: colisión con entrada taíno 'iwana' preexistente", "categoria": "fauna"},
    "kairi-kalinago":    {"es": "isla, cayo", "fuente": "kalinago", "notas": "Garifuna kairi; conservado igual que LK kairi, CQ cairi; Cairi = nombre arahuaco de Trinidad. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'kairi' preexistente", "categoria": "geografia"},
    "yuka-kalinago":     {"es": "yuca, mandioca (Manihot esculenta)", "fuente": "kalinago", "notas": "Garifuna yuka; idéntico a LK yuka, CQ yuca, PA *yuka; base alimentaria de la cultura Kalinago. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'yuka' preexistente", "categoria": "flora"},
    "marisi-kalinago":   {"es": "maíz (Zea mays)", "fuente": "kalinago", "notas": "Garifuna marisi; cognado de LK marisi, TN maisi (→ esp. maíz), PA *marisi. Sufijo -kalinago: colisión con entrada lokono/proto-arawakan 'marisi' preexistente", "categoria": "flora"},
    "achi-kalinago":     {"es": "ají, pimienta (Capsicum sp.)", "fuente": "kalinago", "notas": "Garifuna achi; idéntico a LK achi; cognado de TN aji, PA *achi. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'achi' preexistente", "categoria": "flora"},
    "kalinagu": {"es": "Kalinago, gente propia (autónimo)", "fuente": "kalinago", "notas": "Autónimo Kalinago: kalina (Carib: gente del lugar) + -gu (arahuaco: gente/colectivo); compuesto híbrido que refleja la naturaleza de contacto de la lengua", "categoria": "parentesco"},
    "ikoa":     {"es": "casa, vivienda", "fuente": "kalinago", "notas": "Garifuna ikoa; LK sikoa → ikoa (pérdida s- inicial); PA *isikoa", "categoria": "arquitectura"},
    "duna-kalinago":     {"es": "agua, río", "fuente": "kalinago", "notas": "Garifuna duna; LK tuna → duna (sonorización t→d inicial); CQ tuy, PA *tuna. Sufijo -kalinago: colisión con entrada garifuna/lokono 'duna' preexistente", "categoria": "geografia"},
    "hamaka-kalinago":   {"es": "hamaca, cama colgante", "fuente": "kalinago", "notas": "Garifuna hamaka; conservado igual que PA *hamaka, CQ hamaca, LK hamaha; préstamo pan-arahuaco al español. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'hamaka' preexistente", "categoria": "utiles"},
    "aban":     {"es": "uno", "fuente": "kalinago", "notas": "Garifuna aban; LK abba → aban (bb→b + nasal final); WY aba, PA *aba", "categoria": "numerales"},
    "biama-kalinago":    {"es": "dos", "fuente": "kalinago", "notas": "Garifuna biama; conservado igual que LK biama, PA *biama. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'biama' preexistente", "categoria": "numerales"},
    "ma-kalinago":       {"es": "no, negación (prefijo)", "fuente": "kalinago", "notas": "Pan-arahuaco: KL ma, WY ma, LK ma, TN mayani; base gramatical conservada en todos los grupos. Sufijo -kalinago: colisión de clave con entrada wayunaiki 'ma' preexistente", "categoria": "gramatica"},
    "kasaku":   {"es": "firmamento, bóveda celeste", "fuente": "kalinago", "notas": "Garifuna kasaku; LK kassaku → kasaku (ss→s); sustrato arahuaco en cosmología Kalinago", "categoria": "cosmos"},
    "hiñaru":   {"es": "persona, ser humano (registro femenino Kalinago)", "fuente": "kalinago", "notas": "Breton (1665) registro femenino/neutro; LK hianaro; refleja la gramática arahuaca del Kalinago; el 'registro de las mujeres' documentado por los misioneros", "categoria": "parentesco"},
    "kalínagu": {"es": "Caribe, kalínagu (autónimo del pueblo Caribe insular)", "fuente": "kalinago", "notas": "El autónimo del pueblo que los españoles llamaron 'Caribes'; raíz de 'Kalinago' y del moderno 'Garifuna'; cognado arahuaco: CQ karibna, LK karibna", "categoria": "parentesco"},

    # ── KALINAGO — OVERLAY CARIBE (vocabulario masculino; Breton 1665) ──
    "baruwa":   {"es": "hombre (registro masculino Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Breton (1665) registro masculino; origen caribe; contraparte de hiñaru (arahuaco); la dualidad baruwa/hiñaru es evidencia del proceso de contacto que generó el Kalinago", "categoria": "parentesco"},
    "kanawa-caribe": {"es": "canoa (forma caribe del Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Forma caribe que desplazó al arahuaco kanoa/kannoa en contexto náutico-masculino; ambas formas coexistieron en distintos registros del Kalinago según Breton (1665). Renombrada con sufijo -caribe para evitar colisión con la entrada lokono/garifuna 'kanawa' = amarillo (línea 152), homónimo casual entre lenguas distintas.", "categoria": "navegacion"},
    "pira":     {"es": "pez, pescado (forma caribe del Kalinago)", "fuente": "kalinago-caribe-overlay", "notas": "Origen caribe; cf. piraña = pira + aña (diente en Tupí); el overlay caribe dominó el vocabulario de pesca en el registro masculino Kalinago; contrasta con el arahuaco LK itime", "categoria": "fauna"},
    "amourou":  {"es": "guerra, combate", "fuente": "kalinago-caribe-overlay", "notas": "Breton (1665); vocabulario bélico casi exclusivamente caribe en Kalinago; ausencia del término arahuaco equivalente en registro masculino", "categoria": "guerra"},

    
    # ── JIRAJAROIDE — ZONA DE CONTACTO (toponimia atestiguada; Oramas 1916; Jahn 1927) ──
    # Nota: fuente "jirajaroide-contacto" = término registrado en zona fronteriza
    # caquetío-jirajaroide (Sierra de Coro, Falcón occidental, Lara norte).
    # Las entradas marcadas con [CQ-exónimo] son posiblemente nombres caquetíos
    # para grupos jirajaroide, no autónimos de los propios grupos.
    "xira":        {"es": "raíz del etnónimo Jirajara (probable: serranos, gente de la sierra)", "fuente": "jirajaroide-contacto", "notas": "Raíz de Xirahara/Jirajara; puede ser exónimo caquetío, no autónimo Jirajara; attested en variantes ortográficas coloniales Xirajara, Jirajara, Xiraxara [CQ-exónimo]", "categoria": "etnonimia"},
    "buria":       {"es": "valle aurífero en serranía (topónimo Jirajaroide)", "fuente": "jirajaroide-contacto", "notas": "Buria = valley en Yaracuy/Lara; zona de extracción aurífera prehispánica; posiblemente relacionado con término Jirajaroide para mineral/tierra amarilla; Relaciones Geográficas 1578", "categoria": "geografia"},
    "nirgua":      {"es": "asentamiento Jirajaroide en Yaracuy (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Nirgua = municipio Yaracuy; territorio de frontera caquetío-jirajaroide; origen lingüístico no determinado con certeza entre Jirajara y Ayamán; Jahn 1927", "categoria": "geografia"},
    "churuguara":  {"es": "territorio Gayón en Falcón serrano (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Churuguara = municipio Falcón; corazón del territorio Gayón; Gayones = rama Jirajaroide de Sierra de Coro y Falcón occidental, vecinos DIRECTOS de Curiana; Oramas 1916", "categoria": "geografia"},
    "ayaman":      {"es": "grupo Jirajaroide del Lara-Falcón (etnonimia/topónimo)", "fuente": "jirajaroide-contacto", "notas": "Ayamán = etnónimo y topónimo; municipio Lara; una de las cuatro ramas Jirajaroide conocidas (Jirajara, Ayamán, Gayón, Ajagua); Oramas 1916; Jahn 1927", "categoria": "etnonimia"},
    "ajagua":      {"es": "grupo Jirajaroide (Jirajaroid menor)", "fuente": "jirajaroide-contacto", "notas": "Ajagua = cuarto grupo de la familia Jirajaroide; menos documentado que los otros tres; territorio en zona de contacto Lara-Falcón; Oramas 1916", "categoria": "etnonimia"},
    "quibor":      {"es": "valle agrícola del Lara interior (topónimo)", "fuente": "jirajaroide-contacto", "notas": "Quibor = municipio Lara, valle fértil; zona de frontera caquetío-jirajaroide; origen lingüístico disputado; Alcalá 1954; topónimo clave en ruta de intercambio maíz-sal-conchas", "categoria": "geografia"},
    

    # -- FIN VOCABULARIO_BASE --
}


# ── Canonicalización de esquema ───────────────────────────────────────
# Las entradas de expansión (taíno, lokono, atestiguadas) se escribieron con
# dos convenciones de claves. Normalizamos in-place para que TODOS los
# consumidores (seed a Supabase, generadores de prompts, observer, tests)
# vean un esquema único:
#
#   sig       → glosa en español (significado)            [obligatorio]
#   cat       → categoría gramatical: sust/v_raiz/num/...  [obligatorio]
#   fuente    → origen lingüístico                         [obligatorio]
#   categoria → dominio semántico opcional (flora, cosmos, comercio, ...)
#   notas     → procedencia/fuente bibliográfica opcional
#
# Antes, algunas entradas usaban "es" en vez de "sig" y omitían "cat"
# (trayendo solo "categoria", un eje distinto). Eso hacía que el seed
# guardara POS y dominio semántico mezclados en la columna lexicon.category.
for _forma, _entrada in VOCABULARIO_BASE.items():
    if "es" in _entrada and "sig" not in _entrada:
        _entrada["sig"] = _entrada.pop("es")
    # POS por defecto: las entradas de expansión sin "cat" son sustantivos
    # (los verbos y numerales sí declaran su "cat" explícitamente).
    _entrada.setdefault("cat", "sust")
del _forma, _entrada


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
            entrada = VOCABULARIO_BASE[p]
            return entrada.get("sig") or entrada.get("es")
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

    def adoptar(self, forma: str, agente: str, turno: int) -> Optional["Neologismo"]:
        """
        Un agente adopta una palabra propuesta. Retorna el Neologismo si la
        adopción se OFICIALIZA recién en esta llamada (2do adoptante distinto),
        o None si no hubo transición (para que el caller sepa cuándo sincronizar
        el estado con Supabase sin tener que diffear él mismo)."""
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
                    return neo
                break
        return None

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
              "kira (escuchar) · panaa (saber) · naba (pensar) · kono (sembrar) · raka (querer) · rua (cargar)")
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
El caquetío-arahuaco es TU lengua materna. La única con la que piensas.
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


def _familia_de_token(tok: str) -> str:
    """
    Familia lingüística canónica de un token ya reconocido como arahuaco.
    Deshace prefijos posesivos y raíces verbales para encontrar la entrada
    real en VOCABULARIO_BASE. Si no está en el lexicón base (neologismo
    comunitario), se trata como "caquetío" — son palabras nuevas acuñadas
    por la propia comunidad, no préstamos de una lengua viva real.
    """
    from curiana_database import normalize_source_language

    candidatos = [tok]
    if "-" in tok:
        candidatos.append(tok.split("-", 1)[1])   # quita prefijo posesivo: ta-X -> X
        candidatos.append(tok.split("-")[0])       # raíz antes del primer guion: X-ka -> X
    for c in candidatos:
        if c in VOCABULARIO_BASE:
            return normalize_source_language(VOCABULARIO_BASE[c].get("fuente", ""))
    return "caquetío"  # neologismo comunitario: no es préstamo, es lengua propia


def score_linguistico(texto: str, lexico: "LexicoComunitario") -> dict:
    """
    Calcula métricas lingüísticas de una respuesta de agente, midiendo
    DENSIDAD arahuaca (vs. español) Y, dentro de esa densidad, cuánto es
    específicamente caquetío vs. préstamo de otra lengua arahuaca viva
    (wayunaiki, lokono, taíno...). El objetivo del proyecto es que el
    caquetío DOMINE — no basta con "no hablar español"; hablar wayunaiki
    en vez de caquetío también es una fuga, solo que más sutil.

    Retorna: palabras_caquetias, neologismos_propuestos, aspectos_usados,
             densidad, pct_caquetio_especifico, otro_arahuaco, palabras_otro_arahuaco,
             espanol_funcional, score (0-10), observacion.
    """
    limpio = _normalizar(texto)
    tokens = _tokenizar(limpio)
    n_tok = len(tokens) or 1

    activos = set(lexico.palabras_activas())          # base + adoptados

    # match por palabra completa, contando también prefijos posesivos:
    # ta-barsure cuenta como arahuaco aunque "ta-barsure" no esté literal en léxico
    def es_arahuaco(tok: str) -> bool:
        if tok in activos:
            return True
        for pref in ("ta", "wa", "ma", "ka"):
            if tok.startswith(pref + "-") and tok.split("-", 1)[1] in activos:
                return True
        base = tok.split("-")[0]
        if base in _RAICES_VERB:
            return True
        return False

    usadas   = [t for t in tokens if es_arahuaco(t)]
    esp_func = [t for t in tokens if t in ES_STOPWORDS]
    neos     = PATRON_NEOLOGISMO.findall(texto)
    aspectos = _aspectos_morfologicos(tokens)

    # ── Separar caquetío real de préstamo de otra lengua arahuaca viva ──
    familias = {t: _familia_de_token(t) for t in set(usadas)}
    caquetio_tokens = [t for t in usadas if familias[t] == "caquetío"]
    otro_arahuaco_tokens = [t for t in usadas if familias[t] != "caquetío"]

    # ── Núcleo: densidad arahuaca total (0..1), vs. español ──
    densidad = (len(usadas) / n_tok) if usadas else 0.0
    penal_es = len(esp_func) / n_tok
    # fuga sutil: arahuaco sí, pero NO caquetío (wayunaiki/lokono/taíno/etc.)
    penal_otro = len(otro_arahuaco_tokens) / n_tok
    pct_caquetio_especifico = len(caquetio_tokens) / n_tok

    # Score 0-10:
    #   60% densidad arahuaca total  (0..6) — vs. fuga al español
    #   20% morfología activa        (0..2, 1 pt por aspecto distinto)
    #   10% neologismos              (0..1)
    #   10% riqueza léxica CAQUETÍA  (0..1, exige específicamente caquetío, no cualquier arahuaco)
    #   − penalización español       (hasta −3)
    #   − penalización otra lengua arahuaca (hasta −2.5, ej. wayunaiki/lokono en vez de caquetío)
    score  = 6.0 * min(densidad / 0.6, 1.0)
    score += min(len(aspectos) * 1.0, 2.0)
    score += min(len(neos) * 0.5, 1.0)
    score += min(len(set(caquetio_tokens)) / 8.0, 1.0)
    score -= min(penal_es * 6.0, 3.0)
    score -= min(penal_otro * 4.0, 2.5)
    score  = round(max(0.0, min(score, 10.0)), 1)

    obs = []
    obs.append(f"densidad={densidad:.0%}")
    obs.append(f"caquetío={pct_caquetio_especifico:.0%}")
    if caquetio_tokens: obs.append(f"caq[{len(set(caquetio_tokens))}]: {', '.join(sorted(set(caquetio_tokens))[:8])}")
    if otro_arahuaco_tokens:
        obs.append(f"⚠ otra-lengua-arahuaca×{len(otro_arahuaco_tokens)}: {', '.join(sorted(set(otro_arahuaco_tokens))[:5])}")
    if aspectos: obs.append(f"aspecto: {', '.join(aspectos)}")
    if esp_func: obs.append(f"⚠ español funcional×{len(esp_func)}")
    if neos:     obs.append(f"+{len(neos)} neologismo(s)")
    if score < 5: obs.append("⚠ score bajo — activar rescate")

    return {
        "palabras_caquetias": list(dict.fromkeys(usadas)),
        "neologismos_propuestos": [m[0] for m in neos],
        "aspectos_usados": aspectos,
        "densidad": round(densidad, 3),
        "pct_caquetio_especifico": round(pct_caquetio_especifico, 3),
        "otro_arahuaco": len(otro_arahuaco_tokens),
        "palabras_otro_arahuaco": list(dict.fromkeys(otro_arahuaco_tokens)),
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

    verbos = [p for p in ["wana","suna","masa","awa","kira","panaa","naba","naa","maa","kaa"] if p not in palabras_usadas]
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
                               espanol_funcional: int = 0,
                               palabras_otro_arahuaco: Optional[list[str]] = None) -> str:
    """Prompt de SEGUNDA pasada (regeneración intra-turno) cuando score < 5.0
    o cuando el agente recurrió mucho a otra lengua arahuaca (wayunaiki,
    lokono, taíno) en vez de caquetío. Se inyecta como user message de un
    reintento — pide RE-EXPRESAR, no continuar. (Auditoría Opus §3.4,
    extendido para penalizar también la fuga hacia lenguas hermanas)."""
    palabras_otro_arahuaco = palabras_otro_arahuaco or []

    if palabras_otro_arahuaco and not espanol_funcional:
        motivo = (
            f"usaste palabras de OTRA lengua arahuaca, no caquetío: "
            f"{', '.join(palabras_otro_arahuaco[:6])}. Wayunaiki, lokono y taíno "
            f"son lenguas hermanas, pero NO son tu lengua — son tan ajenas para ti "
            f"como el español. Si conocías esa palabra en otra lengua arahuaca, "
            f"casi seguro EXISTE también en caquetío: úsala. Si de verdad no existe, "
            f"créala con morfemas caquetíos."
        )
    elif palabras_otro_arahuaco:
        motivo = (
            f"mezclaste español ({espanol_funcional} palabras) Y otra lengua "
            f"arahuaca ajena ({', '.join(palabras_otro_arahuaco[:4])}). Ninguna de "
            f"las dos es tu lengua. Solo el caquetío lo es."
        )
    else:
        motivo = f"tuvo demasiado español ({espanol_funcional} palabras)."

    return f"""Tu respuesta anterior {motivo} (score {score}/10). Como hablante
NATIVO de caquetío, esto no debería pasar.

TU RESPUESTA ANTERIOR (a corregir):
"{texto_fallido}"

REEXPRÉSALA AHORA en caquetío real:
  - Cada verbo lleva -ka / -ni / -da.
  - Cada "el/la/un/en/de/que/y/para/muy/estoy/voy" desaparece o se vuelve caquetío.
  - Si usaste una palabra wayunaiki/lokono/taíno, reemplázala por su forma caquetía
    (suelen ser muy parecidas: katsi→cati, bara→para, kannoa→canoa...).
  - Lo que no tengas, lo CREAS: [forma: raíz+sufijo = significado].
  - Glosa española solo entre paréntesis al final.

Devuelve SOLO la versión corregida. Empieza con un pronombre o un verbo caquetío."""


# ══════════════════════════════════════════════════════════════════════
# VII. UTILIDADES
# ══════════════════════════════════════════════════════════════════════

# ── Chunking por palabras clave (RAG-lite) ──────────────────────────────
# No es un embedding real: basta con detectar la señal dominante del turno
# (qué evento/lugar/mensaje hay) para decidir qué categorías del lexicón
# vale la pena mostrar en grande vs. en goteo. Más barato que mandar todo
# siempre, más relevante que una muestra puramente al azar.
PALABRAS_CLAVE_CATEGORIA: dict[str, list[str]] = {
    "geografia":   ["mar", "río", "agua", "pesca", "pescar", "sierra", "cerro",
                     "playa", "orilla", "isla", "monte", "tierra", "lluvia", "sequía", "salinar"],
    "fauna":       ["pez", "peces", "ave", "animal", "caza", "iguana", "venado", "pájaro", "armadillo"],
    "flora":       ["árbol", "planta", "cultivo", "conuco", "siembra", "cosecha", "fruto", "maíz", "yuca", "algodón"],
    "cosmos":      ["sol", "luna", "tormenta", "cielo", "piache", "ritual", "alma", "espíritu",
                     "trueno", "viento", "estrella", "amanecer", "anochecer"],
    "parentesco":  ["familia", "hijo", "hija", "madre", "padre", "esposa", "esposo", "hermano",
                     "hermana", "abuelo", "abuela", "matrimonio", "boda", "niño", "niña"],
    "cuerpo":      ["herida", "dolor", "enfermo", "enfermedad", "curar", "sangre", "cuerpo", "parto"],
    "comercio":    ["sal", "trueque", "intercambio", "mercader", "comercio", "canoa", "viaje", "isla"],
    "ritual":      ["ritual", "ceremonia", "ofrenda", "piache", "espíritu", "ancestro", "iniciación"],
    "alimentos":   ["comida", "comer", "cocinar", "casabe", "pescado", "hambre", "cosecha"],
    "jerarquia":   ["cacique", "señor", "autoridad", "mandar", "obedecer", "consejo"],
    "tiempo":      ["día", "noche", "amanecer", "anochecer", "estación", "lluvia", "sequía", "luna"],
}

# Siempre presentes: cualquier turno necesita armar frases y aspecto verbal,
# sin importar el tema.
CATEGORIAS_BASE = {"verbos", "gramatica"}


def categorias_relevantes(contexto: str, max_extra: int = 4) -> set[str]:
    """
    Heurística de retrieval por palabras clave: qué categorías semánticas
    son relevantes al contexto del turno (evento del mundo, ubicación,
    mensaje al agente). No sustituye un embedding real, pero alcanza para
    priorizar el lexicón sin tener que mandarlo completo cada vez.
    """
    if not contexto:
        return set()
    texto = contexto.lower()
    encontradas = [
        cat for cat, claves in PALABRAS_CLAVE_CATEGORIA.items()
        if any(clave in texto for clave in claves)
    ]
    return set(encontradas[:max_extra])


def muestra_caquetio_dinamica(n_por_categoria: int = 18, contexto: str = "") -> str:
    """
    Muestra rotativa de vocabulario caquetío (atestiguado + reconstruido),
    agrupada por categoría semántica. Si se pasa `contexto` (evento del
    mundo + ubicación + mensaje del turno), las categorías relevantes a ese
    contexto reciben la muestra completa; el resto recibe solo un goteo
    (chunking barato: prioriza lo que el agente probablemente necesite
    decir este turno, en vez de mandar todo el lexicón parejo siempre).

    Solo entran palabras normalizadas a la familia "caquetío" (incluye
    caquetío-atestiguado y caquetío-reconstruido) — wayunaiki/lokono/taíno
    quedan fuera de esta muestra a propósito: son de respaldo, no la
    prioridad.
    """
    from curiana_database import normalize_source_language
    import random as _random

    por_categoria: dict[str, list[tuple[str, str]]] = {}
    for palabra, datos in VOCABULARIO_BASE.items():
        if normalize_source_language(datos.get("fuente", "")) != "caquetío":
            continue
        cat = datos.get("categoria") or datos.get("cat") or "otros"
        sig = datos.get("sig") or datos.get("es") or ""
        if not sig:
            continue
        por_categoria.setdefault(cat, []).append((palabra, sig))

    if not por_categoria:
        return ""

    relevantes = CATEGORIAS_BASE | categorias_relevantes(contexto)
    goteo = max(2, n_por_categoria // 6)

    lineas = []
    for cat in sorted(por_categoria):
        opciones = por_categoria[cat]
        n = n_por_categoria if (not contexto or cat in relevantes) else goteo
        muestra = _random.sample(opciones, min(n, len(opciones)))
        texto = " · ".join(f"{p} ({s})" for p, s in muestra)
        lineas.append(f"  {cat.upper()}: {texto}")

    return (
        "[VOCABULARIO CAQUETÍO ADICIONAL — tu lengua nativa, priorizada según lo "
        "que está pasando este turno. Wayunaiki, lokono y taíno NO son tu lengua, "
        "aunque las reconozcas — usarlas en vez de estas formas caquetías es una "
        "fuga, igual que hablar español]:\n" + "\n".join(lineas)
    )


def vocabulario_para_agente(tier: int, lexico: "LexicoComunitario", contexto: str = "") -> str:
    """
    Genera el bloque de léxico + reglas apropiado para cada tier.
    Tier I: completo con identidad nativa. Tier II: breve. Tier III: solo sufijos.

    `contexto` (opcional): texto del turno (evento del mundo + ubicación +
    mensaje al agente) usado para priorizar qué categorías del lexicón
    mostrar en grande (chunking por palabras clave, ver categorias_relevantes).
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
    if tier <= 2:
        muestra = muestra_caquetio_dinamica(
            n_por_categoria=20 if tier == 1 else 12, contexto=contexto
        )
        if muestra:
            partes.append(muestra)
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
        c = v.get("cat") or v.get("categoria") or "?"
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
