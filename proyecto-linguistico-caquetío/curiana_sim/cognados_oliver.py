"""
CURIANA — PROPUESTA: cognados y correspondencias fonológicas de Oliver 1989, cap. 2
====================================================================================

Fuente:
    Oliver, José R. (1989). "Chapter 2: Arawakan Historical Linguistics", en
    *The Archaeological, Linguistic and Ethnohistorical Evidence for the
    Expansion of Arawakan into Northwestern Venezuela and Northeastern
    Colombia*. Tesis doctoral, University of Illinois at Urbana-Champaign.
    → fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf (109 pp.)

Este módulo es **una propuesta cerrada**, no código del motor. NO se importa
desde la simulación y NO modifica `arahuaco_comparative.py` ni
`curiana_lexicon.py`. La fusión la decide un humano, entrada por entrada.
Misma disciplina que `lexicon_zavala.py` / `minar_zavala_glosario.py`.

`minar_oliver_cap2.py` verifica cada `ancla` de este archivo contra el texto
extraído del PDF y comprueba que la página declarada coincida con la del
marcador de pie de página. Ninguna entrada de aquí es una cita de memoria.

REGLA CERO DEL PROYECTO
    Un parecido no es un cognado. Cuando Oliver duda, la duda viaja al dato:
    el campo `oliver_duda` reproduce su reserva textual y NO debe limpiarse al
    importar.

ABREVIATURAS DE LENGUA
    CQ caquetío · LK lokono (Arawak de Guayana) · WY wayuunaiki (guajiro, "Gu"
    en Oliver) · PJ paraujano/añú ("Pa") · TN taíno · CAIC Island Carib
    centroamericano · PA proto-arahuaco · PM proto-maipurano
"""

from __future__ import annotations

FUENTE = {
    "obra": "Oliver 1989, cap. 2: Arawakan Historical Linguistics",
    "pdf": "fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf",
    "paginas_pdf": 109,
    "paginacion": "numeración de la tesis (pp. 52-160), tomada del pie de página",
    "minado": "2026-08-03 (F5)",
    "seccion_nuclear": "§2.8 The Caquetío Language, pp. 142-151",
}

# =============================================================================
# 1. SETS DE COGNADOS CON CAQUETÍO ATESTIGUADO
# =============================================================================
# Formato por entrada:
#   CQ/WY/PJ/LK/TN/CAIC/PA : formas (None = no dado por Oliver)
#   otros    : {lengua: forma} — lenguas fuera del set de 6 del proyecto
#   no_cognado: {lengua: forma} — formas que Oliver excluye EXPLÍCITAMENTE
#   es       : glosa
#   pagina   : página de la tesis
#   ancla    : subcadena literal del PDF que sostiene la entrada (verificable)
#   confianza: alta | media | baja
#   oliver_duda: reserva textual del autor, o None
#
# CONFIANZA — criterio aplicado:
#   alta  = Oliver afirma la cognación sin reserva Y da ≥2 formas hermanas
#   media = Oliver usa "probably/appears to/it seems", o da 1 sola hermana
#   baja  = Oliver registra un parecido y él mismo lo problematiza
# =============================================================================

COGNADOS_OLIVER: dict[str, dict] = {

    "ceniza": {
        "CQ": "barisi",       # bari-si; en el topónimo bari-si-ki-meto
        "WY": "palíi",        # también palí'i (Oliver p.119, vía Taylor)
        "PJ": None,
        "LK": "bálisi",
        "TN": None,
        "CAIC": None,
        "PA": "*p-/b-ali-",   # "stem p-/b-ali-", pan-arahuaco (item #83 Apéndice A)
        "otros": {},
        "no_cognado": {},
        "es": "ceniza (y, por extensión colonial, pólvora)",
        "pagina": 142,
        "ancla": "the toponym bari-si-ki-meto",
        "confianza": "alta",
        "oliver_duda": None,
        "nota": (
            "El documento de 1579 glosa barisi como 'agua turbia/lodosa' del río "
            "(Río Turbio > Barquisimeto). Oliver separa dos morfemas sobre la misma "
            "raíz: bari-si 'ceniza' y bari-ki 'rojizo'. El par CQ barisi : LK bálisi : "
            "WY palíi es la evidencia más limpia del capítulo de que el caquetío "
            "conserva /b-/ como el lokono, frente al /p-/ guajiro (ver C3)."
        ),
    },

    "rojo_almagre": {
        "CQ": "bariki",
        "WY": None,
        "PJ": None,
        "LK": None,
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {"achagua": "ki-rrayi", "piapoco": "ki-reri", "otras": "ki-lali"},
        "no_cognado": {},
        "es": "almagre, óxido férrico rojo usado como pintura corporal",
        "pagina": 142,
        "ancla": "some painted [their bodies] with bariki which is like",
        "confianza": "baja",
        "oliver_duda": (
            "\"The etymology, however, is not too clear since the dependent segmental "
            "morpheme for 'red' is -ira- or -ila- rather than ki-\" (n. 40, p. 143). "
            "Oliver propone leer ki- como el prefijo atributivo /kV-/ ('que tiene la "
            "cualidad de'), no como el lexema 'rojo'."
        ),
        "nota": "Ya en el lexicón como `bariki`/`barique` vía Zavala 2015 #35.",
    },

    "tapir": {
        "CQ": "kama",         # "cama"/"çama" en el documento de 1579
        "WY": "ama'",         # 'caballo'; irra'ma 'venado'
        "PJ": None,
        "LK": None,
        "TN": None,
        "CAIC": None,
        "PA": "*-ama / *-Vma-",   # Noble 1965:81
        "otros": {
            "karro": "hema", "maipure": "kiema", "baré": "dehema",
            "achagua": "emayenesi", "yavitero": "kema", "baniva": "ema",
            "cauyarí": "?e.ma", "piro": "xema", "amarakaeri": "keme",
        },
        "no_cognado": {},
        "es": "danta, tapir (Tapirus terrestris)",
        "pagina": 143,
        "ancla": "is defined as danta (Spanish) or tapir",
        "confianza": "alta",
        "oliver_duda": None,
        "nota": (
            "El set más ancho del capítulo: 9 lenguas arahuacas más dos preandinas. "
            "Oliver observa que la raíz se reaplicó al ganado europeo donde no había "
            "referente americano (WY ama' 'caballo')."
        ),
    },

    "arbol": {
        "CQ": "-ada-",        # en el topónimo (h)adabacoa 'valle de muchos árboles'
        "WY": "ata'",         # 'palo brasil'; también 'piel', 'corteza'
        "PJ": None,
        "LK": "ada",          # adada 'corteza', ida 'piel', ado-bana 'hoja'
        "TN": None,
        "CAIC": None,
        "PA": "*at-/-ada-",   # Oliver: "at the very least, a Proto-Maipuran stem"
        "otros": {
            "baniva": "aáta-pi", "manao": "ata", "baré": "adda",
            "wapishana": "ata-man", "maipure": "aá",
            "terena": "m-oto-ru", "kinikinao": "m-oto-ke", "campa": "ota-ki",
            "machiguenga": "ota-kyi", "piro": "m-ta", "ipuriná": "m-ata",
        },
        "no_cognado": {},
        "es": "árbol, madera, corteza, piel (la parte por el todo)",
        "pagina": 144,
        "ancla": "The Caquetío stem -ada- is characteristic of Maipuran languages",
        "confianza": "alta",
        "oliver_duda": (
            "Sobre el par LK ada : WY ata' 'árbol' (p. 120): \"It is not clear if this "
            "is a shift in meaning or whether the recorder was given a term for the "
            "part (bark for tree) and interpreted for the whole... For now, I do not "
            "count the pair of terms for 'tree' as cognates.\" La cognación de la RAÍZ "
            "no está en duda; lo que está en duda es contarlos como el mismo ítem "
            "léxico en la lexicoestadística."
        ),
        "nota": (
            "CLAVE: \"having the phoneme /d/ rather than /t/ appears to make it closer "
            "to Lokono than to Paraujano or Guajiro\" (p. 144). Es uno de los tres "
            "pilares de la filiación caquetío-lokono. Ver ANCLA_ARCO_NORTENO."
        ),
    },

    "calabaza": {
        "CQ": "auyama",
        "WY": None,
        "PJ": None,
        "LK": None,
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {
            "achagua": "uyama", "guarequena": "uiiayama", "baniva": "ui-iama",
            "yavitero": "oyama", "maipure": "aviama", "baria": "ui-iama",
            "mandauaca": "ui-iama",
        },
        "no_cognado": {
            "LK": "hihuida",           # "which is not cognate to auyama"
            "WY": "kala'pua / wuirru",  # wuirru es cognado de PJ wüir y TN wíro
            "PJ": "wüir",
            "TN": "wíro",
            "piapoco": "ayi",
        },
        "es": "auyama, calabaza de botella / calabacín",
        "pagina": 145,   # la sección «d) Auyama» abre en la p. 144
        "ancla": "Achagua has the term uyama as cognate of Caquetio's auyama",
        "confianza": "alta",
        "oliver_duda": (
            "\"has been thoroughly incorporated to modern Venezuelan Spanish\" (p. 144) "
            "— la forma que conocemos pasó por el español, no la recogió un lingüista."
        ),
        "nota": (
            "Set NEGATIVO valioso: el caquetío se alinea con achagua/alto Negro y NO "
            "con lokono ni con el par guajiro-paraujano-taíno (wuirru/wüir/wíro). "
            "Contradice parcialmente la tesis lokonoide del propio Oliver: él no lo "
            "comenta."
        ),
    },

    "espiritu_maligno": {
        "CQ": "capú",         # kapú; 'el diablo' y 'los españoles' según doc. 1579
        "WY": None,
        "PJ": None,
        "LK": None,
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {
            "wapishana": "capishi",   # 'el espíritu de las estrellas' (Brett 1868:108)
            "baré": "capuyo carlene",  # 'chamán'
        },
        "no_cognado": {},
        "es": "espíritu, diablo, duende (topónimo Capubana, Paraguaná)",
        "pagina": 145,
        "ancla": "Capú is the Caquetío term which, according to a 1579 document",
        "confianza": "baja",
        "oliver_duda": (
            "\"There is one caution, however. The Carib speaking Tamanaco have the "
            "term capu, /kapu/, for 'sky'; therefore, the possibility of borrowing from "
            "Tamanaco (Carib) to Caquetío (Arawak) or vice-versa cannot be discounted\" "
            "(p. 145)."
        ),
        "nota": (
            "Oliver apoya la lectura arahuaca en el topónimo Capubana y en una leyenda "
            "moderna de duende que él mismo oyó cerca de Santa Ana (Paraguaná) — "
            "evidencia etnográfica del s. XX, no filológica del XVI."
        ),
    },

    "bachaco": {
        "CQ": "koke",         # "coque", hormiga roja que destruye los árboles
        "WY": None,
        "PJ": None,
        "LK": "kuse",         # "cusse", Anonymous [1765] 1928
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {"yavitero": "hoke", "maipure": "kuki"},
        "no_cognado": {},
        "es": "bachaco, hormiga roja grande (Atta sp.)",
        "pagina": 145,
        "ancla": "The term coque or /koke/ is defined as",
        "confianza": "media",
        "oliver_duda": (
            "El segundo set (mandauaca ko-oue, karru kabirri, baria kute, piapoco "
            "kahue, baniva ()uehe) queda fuera: \"the second /k/ is not found as in the "
            "former set, and the sound change can not be explained (e.g. kabirri : "
            "koke)\" (p. 146). Y advierte parecidos NO arahuacos: ye'kuana chauke, "
            "karina kumako, yaruro kohi."
        ),
        "nota": "koke : hoke : kuki : kuse es el único subconjunto que Oliver sostiene.",
    },

    "senor_diao": {
        "CQ": "diao",         # /d-ia(o)/ — Oviedo y Valdés
        "WY": None,
        "PJ": None,
        "LK": "dai-yana-ho",  # 'príncipe'; dia 'palabra', daiya '(mi) lengua'
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {},
        "no_cognado": {},
        "es": "señor o cacique principal, al que otros caciques están sujetos",
        "pagina": 146,
        "ancla": "DIAO: Lord or cacique of the zaquitios territory",
        "confianza": "media",
        "oliver_duda": (
            "\"From the above I could suggest that Caquetío /d-ia(o)/ is cognate to the "
            "stem /d-ai-/ of Lokono\" — formulación condicional, no afirmación."
        ),
        "nota": (
            "Análisis de Oliver: /d-/ 1sg + raíz 'palabra/lengua' (LK dia 'palabra', "
            "adian 'lengua', wa-(a)dia-ni-wa 'nuestra lengua') + /-(h)o/ nominalizador "
            "solemne. ES UNA ETIMOLOGÍA DISTINTA de la de daitiao. Ver NUDO_DAITIAO."
        ),
    },

    "pariente_aliado": {
        "CQ": "daitiao",      # var. datihao (Oviedo); da- 1sg + -(i)tiao
        "WY": None,
        "PJ": None,
        "LK": "da-tti / da-iti",   # statu constructo: dahati, wahati
        "TN": "daitia-o / waitiao / watiao",   # > esp. "guaitiao"
        "CAIC": None,
        "PA": "*-atti-",      # raíz de parentesco: 'tío', 'padre', 'hija'
        "otros": {},
        "no_cognado": {},
        "es": "pariente o aliado ritual; el que presta su nombre (intercambio de nombres)",
        "pagina": 147,
        "ancla": "This Taíno term is cognate to Caquetio daitiao",
        "confianza": "alta",
        "oliver_duda": (
            "Sobre datihao (n. 42, p. 146): \"I have no absolute certainty that it "
            "belongs to a Caquetío language since Oviedo only speaks --at that specific "
            "juncture-- of the Indians of Province of Venezuela in general... He could "
            "very well have used Taíno to express the relationship\". Concluye: "
            "\"makes me suspect that datihao was equally shared by both Taíno and "
            "Caquetío\"."
        ),
        "nota": (
            "Morfología explícita: /wa- [gua-]/ = 3.ª persona plural; /da-/ = 1.ª "
            "persona singular. Las Casas [1552] 1929 II:291 documenta el rito de "
            "intercambio de nombres entre Juan Ponce de León y el cacique Agüeybaná "
            "('se hicieron guaitiaos')."
        ),
    },

    "diente": {
        "CQ": "dare",         # todavía en uso entre pocos individuos en Paraguaná
        "WY": "t-ali",        # '(mi) diente'
        "PJ": "t-a()i",
        "LK": "d-ari",        # 'mi diente'
        "TN": "m-a(h)i-te",   # 'desdentado' (Las Casas, vía Perea y Perea 1941:15-16)
        "CAIC": None,
        "PA": "*/a(r/l)i/",   # proto-maipurano (item #43 Apéndice A)
        "otros": {},
        "no_cognado": {},
        "es": "diente",
        "pagina": 147,
        "ancla": "in coastal Falcón we find the term dare for tooth",
        "confianza": "alta",
        "oliver_duda": (
            "\"although it is known to just a few individuals in Paraguaná\" — dato "
            "etnográfico del s. XX recogido por el propio Oliver, no de crónica."
        ),
        "nota": (
            "EL PAR MÁS PRODUCTIVO DEL CAPÍTULO. Cuatro lenguas con la misma raíz y el "
            "prefijo de 1sg contrastando: CQ d- = LK d- ≠ WY t- = PJ t-. Sostiene C1 y "
            "falsifica la regla `^d → t` de REGLAS_LK_CQ. El lexicón ya tiene `dare` "
            "vía Zavala #103; lo que faltaba era el par."
        ),
    },

    "fruto_cardon": {
        "CQ": "dato",
        "WY": None,
        "PJ": None,
        "LK": "-atti-",       # raíz de parentesco
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {},
        "no_cognado": {},
        "es": "fruto del cardón (pitahaya); lit. 'la hija del cardón'",
        "pagina": 147,
        "ancla": "The other fruit is called in their Indian language as dato",
        "confianza": "media",
        "oliver_duda": (
            "\"Here it seems quite probable that, etymologically...\" y \"-ato probably "
            "relating to Lokono -atti-\". Oliver mismo lo llama \"to put it tritely\"."
        ),
        "nota": (
            "El otro fruto del mismo cardón, caduchi ('breva'), queda SIN etimología "
            "en Oliver. Ambos están ya en el lexicón vía Zavala (#105, #55)."
        ),
    },

    "chaman_boratio": {
        "CQ": "boratio",
        "WY": None,
        "PJ": None,
        "LK": "-atti- + -hu",
        "TN": "-atti- + -hu",
        "CAIC": None,
        "PA": None,
        "otros": {},
        "no_cognado": {},
        "es": "chamán, piache",
        "pagina": 147,
        "ancla": "The term boratio for 'shaman' again includes the ubiquitous stem",
        "confianza": "media",
        "oliver_duda": None,
        "nota": (
            "Descomposición: bor- + /-ati/ (parentesco) + /-(h)o/ nominalizador solemne "
            "(/-hu/ en taíno-lokono). El primer segmento queda sin analizar. Distinto "
            "de `piache` (< PA *piay), que el proyecto ya tiene en COGNADOS."
        ),
    },

    "persona_ser_vivo": {
        "CQ": "kaketío",      # el propio etnónimo
        "WY": None,
        "PJ": None,
        "LK": "kakïtho",      # 'living creature' (Taylor 1977:82)
        "TN": None,
        "CAIC": None,
        "PA": "*/kake/i/-thi/-o/",   # reconstrucción explícita de Oliver
        "otros": {"piro": "kaxiti", "ipuriná": "kakiti"},
        "no_cognado": {"LK_alt": "loko / loko-no"},   # 'miembros de una tribu'
        "es": "ser vivo, criatura viviente (NO 'gente propia')",
        "pagina": 148,
        "ancla": "It is obvious that Lokono kakïtho is cognate of the Caquetío term",
        "confianza": "alta",
        "oliver_duda": None,
        "nota": (
            "CORRIGE COGNADOS['persona'] del proyecto, que empareja CQ 'caquetio' con "
            "LK 'lokono', WY 'wayuu' y TN 'taino' como autónimos paralelos con la glosa "
            "'persona arahuaca, gente propia'. Oliver dice tres cosas incompatibles con "
            "eso: (1) el cognado de kaketío es kakïtho, no lokono; (2) kakïtho glosa "
            "'ser vivo' e incluye MÁS que loko; (3) loko-no y kaketío no son cognados "
            "entre sí. Correspondencia derivada: CQ /t/ : LK /th/ (ver C4b)."
        ),
    },

    "canal_buco": {
        "CQ": "buko",
        "WY": None,
        "PJ": None,
        "LK": "wáburúkku / wáboróko",   # 'sendero angosto'; cf. -roko, ukuburuku, ullúku, aku
        "TN": None,
        "CAIC": None,
        "PA": None,
        "otros": {},
        "no_cognado": {},
        "es": "canal excavado para riego; presa",
        "pagina": 148,
        "ancla": "defined the Caquetío term buco /buko/as a channel dug into the earth",
        "confianza": "media",
        "oliver_duda": (
            "\"These terms are probably cognate to Caquetío buko\" — y el argumento es "
            "semántico ('sendero angosto' ≈ 'canal'), no fonológico."
        ),
        "nota": (
            "Ballesteros [1550] vía Bécker 1950a. En el lexicón `buco` está etiquetado "
            "`caquetío` (no -atestiguado) con la reserva de Alvarado 1921, que lo cree "
            "romance. Oliver aporta el lado arahuaco de la disputa: NO la cierra."
        ),
    },

    "perro": {
        "CQ": "auri",
        "WY": None,
        "PJ": "-y-eri",
        "LK": None,
        "TN": None,
        "CAIC": "auri / auli",
        "PA": "*Africada-/i/-nV",   # la forma ANTIGUA, desplazada en el norte
        "otros": {
            "maipure": "auri", "achagua": "auri", "piapoco": "auri",
            "wapishana": "a()ri-merak", "cauyarí": "cha-aw()i",
            "guarequena": "chi-nu/o", "mandauaca": "chi-nu/o",
            "baniva": "tsinu", "werekena": "tsinu", "tariana": "tsíinu",
            "baré": "shino", "campa": "o-chi-tu", "matsigüenga": "o-tsi-ti",
            "amuesha": "oo-che-k",
        },
        "no_cognado": {},
        "es": "perro",
        "pagina": 151,
        "ancla": "The term for 'dog' in Caquetío is auri",
        "confianza": "alta",
        "oliver_duda": (
            "El término lo halló en una lista de vocabulario CUYÓN, no caquetía: "
            "\"there is little doubt that the Cuyón borrowed the term from the "
            "neighboring Caquetío of Barquisimeto\" — inferencia por distribución "
            "geográfica, no atestación directa en boca caquetía."
        ),
        "nota": (
            "INNOVACIÓN proto-norteña: auri/auli sustituye a la forma proto-arahuaca "
            "*Africada-i-nV, que sobrevive en el Alto Río Negro. Es uno de los tres "
            "pilares de la filiación lokonoide del caquetío. El lexicón NO tiene "
            "ninguna palabra caquetía para 'perro' (solo el wayunaiki erü)."
        ),
    },

    "mar": {
        "CQ": "para",
        "WY": "palaa'",
        "PJ": None,
        "LK": None,
        "TN": "bara-wa",
        "CAIC": None,
        "PA": "*para",
        "otros": {},
        "no_cognado": {},
        "es": "mar",
        "pagina": 150,
        "ancla": "para- for 'sea' [Guajiro: /palaa'/, Taíno: /bara-wa/]",
        "confianza": "alta",
        "oliver_duda": None,
        "nota": (
            "Ya está en COGNADOS del proyecto (con LK bara, TN bagua). Oliver aporta "
            "TN bara-wa, más cercano a bara que bagua. **Es la excepción a C3**: aquí "
            "el caquetío tiene /p/ donde el taíno tiene /b/. Oliver no lo comenta."
        ),
    },
}


# =============================================================================
# 2. CORRESPONDENCIAS FONOLÓGICAS REGULARES
# =============================================================================
# Esto es lo que las 441 formas `hipotético-no-verificado` nunca tuvieron.
# `implicacion_motor` dice qué regla de arahuaco_comparative.py toca.
# =============================================================================

CORRESPONDENCIAS_OLIVER: list[dict] = [

    {
        "id": "C1",
        "titulo": "Prefijo de 1.ª persona singular: */nV-/ → /dA-/ → /tA-/",
        "cadena": "PA */n(V)-/  >  /dA-/ (LK, TN, y probablemente CQ)  >  /tA-/ (WY, PJ)",
        "pagina": 136,
        "ancla": "*/nV-/---> /dA-/",
        "confianza": "alta para LK/TN; media-alta para CQ",
        "evidencia_cq": ["diao /d-ia(o)/", "datihao / daitiao /da-/", "dare 'diente'", "dato 'fruto'"],
        "evidencia_otras": [
            "LK dái 'yo' : WY tayá 'yo'",
            "LK d-ari 'mi diente' : WY t-ali : PJ t-a()i",
            "LK d-ike 'mi oreja' : WY t-achée (< *t-ati-, Taylor 1978)",
        ],
        "oliver_duda": (
            "\"Taíno, Lokono, and PERHAPS Caquetío (section 2.8) experienced the shift\" "
            "(p. 136, énfasis añadido). Y: \"Even if I am wrong about the direction of "
            "sound change (especially /d/--->/t/) the distribution pattern does not "
            "change with regards to the language nodes.\""
        ),
        "implicacion_motor": (
            "FALSIFICA REGLAS_LK_CQ R13 (`^d(?=[aeiou]) → t`, «d- inicial ante vocal → "
            "t»). El caquetío CONSERVA /d-/. La regla actual convierte cada palabra "
            "lokona con d- inicial en una forma caquetía con t- inicial, que es "
            "exactamente la innovación GUAJIRA. Propuesta: eliminar R13 y añadir a "
            "REGLAS_WY_CQ la regla inversa `^t(?=a) → d` para el prefijo de 1sg."
        ),
    },

    {
        "id": "C2",
        "titulo": "Lokono /d/ : Guajiro /t/ — «very regular and systematic»",
        "cadena": "PA */d/  >  /t/ en guajiro; lokono no experimentó el cambio",
        "pagina": 119,
        "ancla": "Two very regular and systematic sound changes between Lokono and Guajiro",
        "confianza": "alta",
        "evidencia_cq": [],
        "evidencia_otras": [
            "WY tayá : LK dái 'yo' (ítem #1)",
            "WY atúnká : LK donkon 'dormir' (pre-lokono *-addaumka)",
            "ítems #1, 17, 27, 28, 45, 61, 66 del Apéndice A",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "REGLAS_WY_LK ya tiene el eje p/b pero NO tiene t→d. Falta "
            "`^t(?=[aeiou]) → d` en WY→LK. Y por C1, la misma regla debería valer "
            "WY→CQ al menos para el prefijo personal."
        ),
    },

    {
        "id": "C3",
        "titulo": "Lokono /b/ : Guajiro /p/ — «very regular and systematic»",
        "cadena": "PA */b/  >  /p/ en guajiro; lokono (y caquetío) conservan /b/",
        "pagina": 119,
        "ancla": "(Lo) /b/ : (Gu) /p/",
        "confianza": "alta (para LK:WY); media para el lado caquetío",
        "evidencia_cq": [
            "CQ barisi 'ceniza' : LK bálisi : WY palíi  —  el CQ va con el LK",
            "CQ -bana (sufijo topónimo) y NO -pana: «many appear to be closer to "
            "Lokono (e.g. -bana instead of -pana)» (p. 150)",
            "CQ buko, bariki, boratio: /b-/ inicial conservada",
        ],
        "evidencia_otras": [
            "WY pia' 'tú' : LK bïí",
            "ítems #12, 25, 31, 45, 48, 53, 57, 77, 83, 85 del Apéndice A",
        ],
        "oliver_duda": (
            "CONTRAEJEMPLO dentro del propio Oliver: CQ *para* 'mar' frente a TN "
            "bara-wa y LK bara (p. 150). Ahí el caquetío tiene /p/ donde el lokono "
            "tiene /b/. Oliver no lo explica ni lo menciona como problema. La "
            "correspondencia b/p en caquetío NO es, por tanto, regular en el sentido "
            "estricto: hay al menos un contraejemplo atestiguado."
        ),
        "implicacion_motor": (
            "PROBLEMATIZA REGLAS_LK_CQ R5 (`^b → p`) y R9 (`b intervocálica → p`). Con "
            "el dato de Oliver, esas reglas producen la forma GUAJIRA, no la caquetía, "
            "salvo en 'mar'. Propuesta: NO eliminarlas (para 'mar' las necesita) sino "
            "degradarlas de regla a alternancia no resuelta, y no usarlas para generar "
            "vocabulario nuevo."
        ),
    },

    {
        "id": "C4",
        "titulo": "Lokono /th/ : Guajiro /s/ ~ /sh/ (Taylor 1977:38, 43)",
        "cadena": "LK /th/  ↔  WY /s/, /sh/  ↔  CAIC /t/",
        "pagina": 119,
        "ancla": "asá (a)than áta 'to drink'",   # fila 1 de la tabla de Taylor
        "confianza": "alta con caveat",
        "evidencia_cq": [],
        "evidencia_otras": [
            "WY asá : LK (a)than : CAIC áta 'beber'",
            "WY kashí : LK káthi : CAIC hati 'luna'",
            "WY nisha : LK lithina : CAIC líta 'su sangre'",
            "WY tashíi : LK dáthi 'mi padre'",
            "WY sï?uli : LK thokóti : CAIC tugúdi 'su pie'",
            "WY ahï : LK -íkhï : CAIC -oho 'savia, pus'",
        ],
        "oliver_duda": (
            "Taylor advierte: \"there appears to be considerable dialectal confusion in "
            "Guajiro between these latter phonemes and /h/\" — WY pisíchi : LK bíhiri "
            "'murciélago'; WY asíkaa : LK ihíka 'futuro'; WY asápï : LK áhabo 'espalda'."
        ),
        "implicacion_motor": (
            "El proyecto NO tiene ninguna regla para /th/ lokono. REGLAS_LK_CQ y "
            "REGLAS_LK_WY lo dejan pasar intacto. Seis pares listos para "
            "PARES_VALIDACION (LK→WY). Nótese que la tabla de Taylor da el par "
            "'luna' WY kashí : LK káthi, mientras el proyecto usa LK 'katsi': "
            "revisar cuál es la forma buena."
        ),
    },

    {
        "id": "C4b",
        "titulo": "Caquetío /t/ : Lokono /th/",
        "cadena": "CQ /t/  ↔  LK /th/  (y, por C4, WY /s ~ sh/)",
        "pagina": 148,
        "ancla": "kakïtho is cognate of the Caquetío term kaketío (/t/--->/th/)",
        "confianza": "media",
        "evidencia_cq": ["CQ kaketío : LK kakïtho : piro kaxiti : ipuriná kakiti"],
        "evidencia_otras": ["Oliver reconstruye */kake/i/-thi/-o/"],
        "oliver_duda": (
            "Un solo par. Oliver escribe la flecha como (/t/--->/th/), es decir, del "
            "caquetío hacia el lokono, lo que contradice su propia dirección "
            "reconstructiva (*-thi > -t- sería lo esperable). Puede ser notación de "
            "correspondencia, no de cambio."
        ),
        "implicacion_motor": (
            "Junto con C4 da la cadena completa CQ /t/ : LK /th/ : WY /s, sh/. Eso "
            "SÍ es un puente nuevo y falsifica de paso REGLAS_WY_CQ R4 (`sh → ch`): "
            "por C5 el /sh/ guajiro es innovación reciente, y su correspondencia "
            "caquetía debería ser /t/ o /s/, no /ch/."
        ),
    },

    {
        "id": "C5",
        "titulo": "Las palatales guajiras /ch/, /ñ/, /sh/ son innovaciones RECIENTES",
        "cadena": "*/t/ o */l/  >  /ch/, /ñ/, /sh/ en guajiro (Taylor 1978); "
                  "además */d/ > /t/ y */s/ > /sh, ch/",
        "pagina": 119,
        "ancla": 'arose as phonemes',
        "confianza": "alta",
        "evidencia_cq": [],
        "evidencia_otras": [
            "WY chi', chirra 'este/ese' : LK tho(h)o, lira(h)a (Oliver los cuenta "
            "como cognados DUDOSOS)",
            "LK tiene tres oclusivas apicales /d/, /t/, /th/; el guajiro solo /t/",
        ],
        "oliver_duda": (
            "Oliver cuenta los pares afectados como cognados DUDOSOS (?), no "
            "definitivos."
        ),
        "implicacion_motor": (
            "MUNICIÓN PRINCIPAL CONTRA LAS 441. Toda reconstrucción caquetía derivada "
            "de una forma wayunaiki que contenga /ch/, /sh/ o /ñ/ está proyectando al "
            "s. XV un fonema que, según Taylor, el guajiro adquirió \"not very long "
            "ago\". REGLAS_WY_CQ R4 (`sh → ch`) conserva la innovación en vez de "
            "deshacerla."
        ),
    },

    {
        "id": "C6",
        "titulo": "Guajiro /w/ : Lokono /o/",
        "cadena": "WY /wA-/  :  LK /oA-/",
        "pagina": 118,
        "ancla": "wayá', whereas in Lokono it is oái",
        "confianza": "alta",
        "evidencia_cq": [],
        "evidencia_otras": [
            "WY wayá' : LK oái 'nosotros'",
            "El lokono moderno carece de /w/ (tiene /o/) y de /y/ (tiene /i/, /ï/)",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "REGLAS_WY_LK R9 hace `^w → b` («via proto *b»), sin fuente. Oliver da la "
            "correspondencia real: `^w → o`. R9 debería revisarse."
        ),
    },

    {
        "id": "C7",
        "titulo": "Prefijo atributivo fosilizado /k-/, /kV-/ con alternancia cero",
        "cadena": "/k-/ ~ Ø, en ambas direcciones (Matteson 1972:164; Noble 1965:28)",
        "pagina": 120,
        "ancla": "suggests that /k-/ is a fossilized prefix of some sort",
        "confianza": "media",
        "evidencia_cq": [
            "El sufijo CQ -coa frente al pre-lokono *-kua/-koa 'cuerno' entra por aquí"
        ],
        "evidencia_otras": [
            "'nadar': WY katüná : LK (-)athímïn",
            "'caminar': WY (-)ouná : LK kúuna",
            "'cuerno':  WY (-)ouá  : pre-LK *-kua/-koa",
            "'luna':    WY kashi'  : LK káthi   (k : k, sin pérdida)",
        ],
        "oliver_duda": (
            "Oliver clasifica el grupo entero como cognados DUDOSOS: «there is a group "
            "which seem to show an IRREGULAR alternation»."
        ),
        "implicacion_motor": (
            "Explica por qué transducciones que solo difieren en una /k/ inicial "
            "pueden ser cognados reales — pero también por qué NO se puede predecir "
            "la presencia de esa /k/. Ninguna regla del motor debe añadir o quitar "
            "/k-/ inicial."
        ),
    },

    {
        "id": "C8",
        "titulo": "LÍMITE: /r/ ~ /l/ es indecidible en todo el corpus",
        "cadena": "r ↔ l ↔ rr ↔ lr, no discriminados por los transcriptores",
        "pagina": 105,
        "ancla": "The discrimination of l, r, rr and lr is rarely consistent",
        "confianza": "alta (como límite, no como regla)",
        "evidencia_cq": [
            "n. 47, p. 150: en los topónimos caquetíos la /r/ de -Vr-oa «could have "
            "been either /l/, /lr/, or /r/ phoneme[s] in Caquetío»"
        ],
        "evidencia_otras": [
            "Oliver excluye m, l, r y ly de su Tabla 3 de reflejos fonémicos",
            "Nota de trabajo del propio Oliver en Barquisimeto: bari- (/r/=/l/)",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "REGLAS_LK_WY R7 (`r ante vocal → l`) es indefendible como regla de cambio "
            "de sonido: es una diferencia de TRANSCRIPCIÓN, no un cambio fonológico "
            "documentado. Igual para cualquier scoring que distinga r de l."
        ),
    },

    {
        "id": "C9",
        "titulo": "LÍMITE: las vocales quedan fuera del método comparativo de Oliver",
        "cadena": "—",
        "pagina": 105,
        "ancla": "vowels are excluded from this table",
        "confianza": "alta (como límite)",
        "evidencia_cq": [],
        "evidencia_otras": [
            "«many of the languages here discussed were not recorded in phonetic "
            "transcription by trained linguistic observers»",
            "Solo se incluyen consonantes y semivocales en las Tablas 3-7",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "Las reglas del motor que operan sobre vocales (REGLAS_WY_CQ R1 «vocales "
            "largas → simples», R12 `-baa$ → -ba`; REGLAS_LK_WY R10/R11 sobre `-aa`; "
            "REGLAS_LK_KL R12) NO tienen respaldo en Oliver, ni a favor ni en contra. "
            "Son convenciones del proyecto y deben documentarse como tales."
        ),
    },

    {
        "id": "C10",
        "titulo": "Léxico diagnóstico 'pez': PM *-imV con fricativa vs. innovación *kupa-(l)i",
        "cadena": "PA/PM */-imV/ precedido de /s/, /sh/, /h/, /x/",
        "pagina": 136,
        "ancla": "The reconstructed */-imV/ stem is contained in Guajiro j-ime",
        "confianza": "alta",
        "evidencia_cq": [],
        "evidencia_otras": [
            "WY j-ime · LK h-ime · yavitero zimazi/simasi · baniva sr-ime · "
            "werekena sh-ime · bauré h-im (pre-bauré *iman) · maipure t-ima-ki · "
            "campa/matsigüenga/nomatsigüenga sh-ima",
            "INNOVACIÓN del Alto Negro: achagua kupai, piapoco ku'bai, "
            "guarequena/tariana/wakuenai kuphe",
            "PJ oïh corresponde a terena hyoe, kinikinao hyoi (metátesis)",
        ],
        "oliver_duda": (
            "n. 38: \"I suspect that oïh is the name of a specific fish species, but "
            "which Jahn interpreted as a generic Paraujano term for 'fish'.\""
        ),
        "implicacion_motor": (
            "No hay forma caquetía atestiguada para 'pez'. Oliver sitúa al caquetío en "
            "la rama SIN la innovación kupa-, lo que PREDICE una forma tipo *(h)ime. "
            "Es una predicción, no un dato: si se importa, va como reconstruida y "
            "marcada. El COGNADOS del proyecto tiene PA *itime / LK itime — compatible."
        ),
    },

    {
        "id": "C11",
        "titulo": "Sufijo /-bana/ ~ /-pana/ 'hoja, cubierta, entorno, casa'",
        "cadena": "PM *-bana / *-pana (pani-, bani- en Noble 1965:101)",
        "pagina": 148,
        "ancla": "In Lokono I found the same suffix,with the meaning of 'sorrounding'",
        "confianza": "alta",
        "evidencia_cq": [
            "Topónimos: ti-bana, caracu-bana, cua-bana, judi-bana, cariru-bana, "
            "tausa-bana (Paraguaná), yara-bana (Baragua), Capu-bana",
            "Aruba: wata-pana (Sapindus coriaria)",
        ],
        "evidencia_otras": [
            "LK -bana 'techo, cubierta'; ado-bana 'hoja'",
            "WY a-pana 'hoja'",
            "TN pana-pe(n) 'fruto del pan'; antropónimo Agüey-bana",
            "piapoco a-ban() 'hoja'; uainambeu aá-pana 'bosque'; "
            "baniwa de Içana aá-pana-pe",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "El proyecto ya usa -bana como locativo ('orilla, borde'). Oliver da una "
            "glosa distinta y mejor fundada: 'entorno, cubierta, techo'. Y usa la "
            "b/p de este sufijo como argumento de filiación (ver C3)."
        ),
    },

    {
        "id": "C12",
        "titulo": "Postposición /-coa/ (/-koa/, /-kua/, /-kwa/)",
        "cadena": "LK -aku + -oa  >  -akoa  >  CQ -coa (síncopa)",
        "pagina": 149,
        "ancla": "This seems to be a syncope of /-oa/ and /-aku/ seen for Lokono",
        "confianza": "media",
        "evidencia_cq": [
            "Topónimos: cumaja-coa, toda-coa, pipia-coa, uria-coa, ri-coa, Túcua "
            "(sitio FAL-60 cerca de Dabajuro)",
            "Con el morfema intermedio -ba-/-va-: a-ba-coa, ura-ba-coa, guai-ba-coa, "
            "qui-ba-coa, buchi-ba-coa, guaida-ba-coa, bar(a)-ba-coa, gua-ba-coa, "
            "chi-va-coa, di-va-coa",
            "En -oa solo: ar-oa, botor-oa, er-oa, maur-oa (patrón -Vr-oa)",
        ],
        "evidencia_otras": [
            "LK -aku = enfático/recíproco; -oa (< -oaia, Taylor 1970b:32,35) = reflexivo",
            "Perea y Perea 1948:87: -coa = «superlativo de la preposición en/sobre»",
            "TN coa 'coa, palo de sembrar'; LK ukoa (tucua) 'cuerno'; "
            "piapoco idnakua 'cuerno', idakoa 'proa', yanakoa 'filo/punta'",
            "Siuçí: los nombres de ángulos y puntas de roca ribereña llevan -coa "
            "(p. ej. mami-coa, mami- 'perdiz')",
        ],
        "oliver_duda": (
            "El morfema intermedio -ba-/-va- queda con \"meaning as yet undetermined\". "
            "Y sobre la coa taína (n. 46) discute si es préstamo, herencia proto-amerindia "
            "o convergencia paralela con el náhuatl, inclinándose por la convergencia."
        ),
        "implicacion_motor": (
            "El proyecto ya tiene -coa como «locativo existencial (topónimos)» en la "
            "tabla CORRESPONDENCIAS. Oliver da el análisis morfológico completo "
            "(-aku + -oa) y un valor semántico añadido: 'punta, pico, proa'. "
            "El patrón -Vr-oa (n. 47) es un molde generativo real para topónimos."
        ),
    },

    {
        "id": "C13",
        "titulo": "Sufijos nominalizadores /-si/ y /-(h)o/",
        "cadena": "PA *-tsi / *-si (Matteson 1972:164); nominalizador solemne /-(h)o/, "
                  "/-hu/ en taíno-lokono",
        "pagina": 143,
        "ancla": "The suffix -si is a nominalizing suffix, of Proto-Arawakan origin",
        "confianza": "alta",
        "evidencia_cq": [
            "-si: bari-si 'ceniza'",
            "-(h)o: dia-o, daitia-o, borati-o, kaket-ío",
        ],
        "evidencia_otras": [
            "Matteson: la clase se usa para «abstract shapes, body parts, tools, kin, "
            "and intimately possessed objects»; *tsi en proto-piro-apuriná y "
            "proto-asheninka, *-si en proto-newiki",
            "Vescelius (com. pers. 1982, n. 44): Luca-yo, Cigüa-yo, Kaket-ío — "
            "los etnónimos antillanos y norsudamericanos en -ío/-yo",
        ],
        "oliver_duda": None,
        "implicacion_motor": (
            "Dos afijos productivos ausentes de REGLAS_ZAVALA. `-si` da nombres de "
            "cosas poseídas/partes; `-(h)o` da títulos y etnónimos. Con `-si` los "
            "agentes podrían derivar nombres abstractos de forma atestiguada."
        ),
    },
]


# =============================================================================
# 3. PARES DE VALIDACIÓN NUEVOS — listos para PARES_VALIDACION
# =============================================================================
# (palabra, origen, destino, esperado, concepto)
# Todos con fuente EXTERNA (Oliver 1989 / Taylor 1977-78), no del propio corpus.
# El campo `pasa_hoy` lo calcula minar_oliver_cap2.py; aquí no se predice.
# =============================================================================

PARES_VALIDACION_OLIVER = [
    # — eje /d/ : /t/ (C1, C2), pp. 119, 136, 147 —
    ("dari",   "LK", "WY", "tali",   "diente LK→WY (Oliver 1989, p.147)"),
    ("dai",    "LK", "WY", "tai",    "yo LK→WY (Oliver 1989, p.119: dái : tayá)"),
    # — eje /b/ : /p/ (C3), p. 119 —
    ("balisi", "LK", "WY", "palisi", "ceniza LK→WY (Oliver 1989, p.119: bálisi : palíi)"),
    ("bii",    "LK", "WY", "pii",    "tú LK→WY (Oliver 1989, p.119: bïí : pia')"),
    # — eje /th/ : /s, sh/ (C4), p. 119, tabla de Taylor 1977:38 —
    ("athan",  "LK", "WY", "asa",    "beber LK→WY (Taylor 1977:38 en Oliver p.119)"),
    ("kathi",  "LK", "WY", "kashi",  "luna LK→WY (Taylor 1977:38 en Oliver p.119)"),
    ("dathi",  "LK", "WY", "tashi",  "mi padre LK→WY (Taylor 1977:38 en Oliver p.119)"),
    # — caquetío atestiguado contra su hermana (los únicos honestos para →CQ) —
    ("dari",   "LK", "CQ", "dare",   "diente LK→CQ (Oliver 1989, p.147)"),
    ("balisi", "LK", "CQ", "barisi", "ceniza LK→CQ (Oliver 1989, p.142 y 119)"),
    ("ada",    "LK", "CQ", "ada",    "árbol LK→CQ (Oliver 1989, p.144, sin cambio)"),
]

# Los cuatro últimos son los que valen: predicen una forma caquetía ATESTIGUADA
# desde una hermana. Los primeros seis prueban el eje LK↔WY, que el motor usa
# como puente. Ninguno se elige por conveniencia: los seis de Taylor son la
# tabla completa que Oliver reproduce, sin descartar filas.


# =============================================================================
# 4. REVISIONES PROPUESTAS A arahuaco_comparative.py
# =============================================================================
# NO se aplican aquí. Cada una nombra la regla, qué dato la toca y qué hacer.
# =============================================================================

REVISIONES_REGLAS: list[dict] = [
    {
        "regla": "REGLAS_LK_CQ R13  `^d(?=[aeiou]) → t`",
        "veredicto": "FALSIFICADA",
        "dato": "CQ dare : LK d-ari (p.147); CQ diao, datihao, dato (pp.146-147); "
                "Oliver sitúa /dA-/ 1sg en LK, TN y probablemente CQ (p.136)",
        "accion": "Eliminar. El caquetío conserva /d-/; el paso a /t-/ es la "
                  "innovación guajiro-paraujana.",
        "impacto_441": "clave A1",
    },
    {
        "regla": "REGLAS_LK_CQ R5 `^b → p` y R9 `b intervocálica → p`",
        "veredicto": "DEGRADADA (no regular)",
        "dato": "A favor de conservar /b/: CQ barisi : LK bálisi : WY palíi (pp.142,119); "
                "CQ -bana y no -pana (p.150); buko, bariki, boratio. "
                "En contra: CQ para 'mar' : LK bara : TN bara-wa (p.150).",
        "accion": "No eliminar (hace falta para 'mar'), pero dejar de usarla para "
                  "GENERAR vocabulario: produce la forma guajira en todos los demás casos.",
        "impacto_441": "clave A2",
    },
    {
        "regla": "REGLAS_WY_CQ R4 `sh → ch`",
        "veredicto": "SOSPECHOSA",
        "dato": "Taylor 1978 en Oliver p.119: /ch/, /ñ/, /sh/ guajiros «arose as "
                "phonemes not very long ago» de la palatalización de /t/ o /l/.",
        "accion": "La correspondencia conservadora del /sh/ guajiro es /t/ o /s/ "
                  "(C4, C4b), no /ch/. Revisar antes de reconstruir cualquier forma "
                  "caquetía desde una palabra wayunaiki con sh/ch/ñ.",
        "impacto_441": "clave A3",
    },
    {
        "regla": "REGLAS_LK_WY R7 `r ante vocal → l`",
        "veredicto": "SIN FUNDAMENTO FONOLÓGICO",
        "dato": "Oliver excluye l, r, rr, lr de la Tabla 3 porque «rarely consistent» "
                "en las transcripciones (p.105); n.47 p.150 admite que la /r/ de los "
                "topónimos caquetíos pudo ser /l/, /lr/ o /r/.",
        "accion": "Documentar como convención de transcripción, no como cambio de "
                  "sonido. No usarla como evidencia de nada.",
        "impacto_441": "—",
    },
    {
        "regla": "REGLAS_WY_LK R9 `^w → b` («via proto *b»)",
        "veredicto": "CORREGIBLE",
        "dato": "WY wayá' : LK oái 'nosotros' [/wA-/ : /oA-/]; el lokono moderno "
                "carece de /w/ y tiene /o/ (p.118).",
        "accion": "Cambiar a `^w → o`.",
        "impacto_441": "—",
    },
    {
        "regla": "COGNADOS['persona']",
        "veredicto": "MAL EMPAREJADO",
        "dato": "CQ kaketío es cognado de LK kakïtho 'ser vivo' (p.148), de piro "
                "kaxiti e ipuriná kakiti — NO de LK loko-no. Reconstrucción de Oliver: "
                "*/kake/i/-thi/-o/.",
        "accion": "Separar en dos entradas: 'ser_vivo' (CQ kaketío : LK kakïtho : "
                  "piro kaxiti : ipuriná kakiti) y 'autonimo' (los autónimos, que no "
                  "son cognados entre sí).",
        "impacto_441": "—",
    },
    {
        "regla": "COGNADOS['mar'] — forma taína",
        "veredicto": "AMPLIABLE",
        "dato": "Oliver p.150 da TN bara-wa junto a WY palaa' y CQ para. El proyecto "
                "tiene TN bagua.",
        "accion": "Registrar bara-wa como variante; bagua y bara-wa pueden ser la "
                  "misma palabra con distinta transcripción colonial.",
        "impacto_441": "—",
    },
    {
        "regla": "COGNADOS['luna'] — forma lokona",
        "veredicto": "A VERIFICAR",
        "dato": "Taylor 1977:38 (en Oliver p.119) da LK káthi, no katsi. El proyecto "
                "usa katsi y sobre él construye REGLAS_LK_CQ R4 (`ts → t`) y "
                "REGLAS_LK_KL R7.",
        "accion": "No tocar sin más: katsi puede venir de otra fuente (Goeje/Pet). "
                  "Pero si la forma buena es káthi, la regla `ts → t` pierde su par "
                  "fundacional y lo que hay es /th/ → /t/ (C4b).",
        "impacto_441": "—",
    },
]


# =============================================================================
# 5. ENTRADAS CAQUETÍAS ATESTIGUADAS AUSENTES DEL LEXICÓN
# =============================================================================

NUEVAS_ENTRADAS_CAQUETIO: dict[str, dict] = {
    "auri": {
        "sig": "perro",
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "glosa_fuente": "dog [Oliver 1989 cap.2, p.151]",
        "notas": (
            "Oliver 1989 cap. 2, p. 151: hallado en una lista de vocabulario CUYÓN y "
            "atribuido al caquetío por préstamo desde el caquetío de Barquisimeto "
            "(«it is eminently clear that the term is not of Cuyón-Jirajaran "
            "affiliation»). Innovación proto-norteña frente al proto-arahuaco "
            "*Africada-i-nV; cognados: island carib, maipure, achagua y piapoco auri/auli, "
            "wapishana a()ri-merak, paraujano -y-eri. ATESTACIÓN INDIRECTA: no está en "
            "boca caquetía en ninguna crónica, se infiere por distribución geográfica."
        ),
        "categoria": "fauna",
    },
    "barisi": {
        "sig": "ceniza; agua turbia, lodosa",
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "glosa_fuente": (
            "«...the water [of the river] comes muddy, hence the Indians call it barisi» "
            "[Relación de Barquisimeto 1579, en Arellano Moreno 1964:178, vía "
            "Oliver 1989 cap.2, p.142]"
        ),
        "notas": (
            "Oliver 1989 cap. 2, p. 142. Base del topónimo bari-si-ki-meto "
            "(Barquisimeto) y de los hidrónimos falconianos bari-si-gua (Borojó) y "
            "bari-si-gu()-ita (Bariro). Raíz pan-arahuaca p-/b-ali- 'ceniza'; cognados "
            "LK bálisi, WY palíi (Oliver p.119). D7: la glosa de la fuente es 'agua "
            "turbia'; la identificación morfológica de Oliver es bari- 'ceniza' + -si "
            "nominalizador."
        ),
        "categoria": "materia",
    },
    "ada": {
        "sig": "árbol, madera (raíz; también 'corteza', 'piel' por parte/todo)",
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "glosa_fuente": (
            "«the valley of hadabacoa [...], which means in Spanish language 'all trees'» "
            "[Relación 1579, en Arellano Moreno 1964, vía Oliver 1989 cap.2, p.144]"
        ),
        "notas": (
            "Oliver 1989 cap. 2, p. 144. Atestiguada solo dentro del topónimo "
            "(h)adabacoa (valle de Yaracuy) y de los fitónimos arubeños dabaraida, "
            "hubada, tarabada. Cognados: LK ada 'árbol', adada 'corteza', ida 'piel', "
            "ado-bana 'hoja'; WY ata'; baré adda; manao ata; maipure aá. Oliver la usa "
            "como argumento de filiación: el /d/ (no /t/) acerca el caquetío al lokono."
        ),
        "categoria": "flora",
    },
    "adabacoa": {
        "sig": "valle arbolado, valle lleno de árboles (topónimo, valle de Yaracuy)",
        "cat": "topónimo",
        "fuente": "caquetío-atestiguado",
        "glosa_fuente": "«adabacoa, which means a valley 'full of trees'» [Relación 1579, "
                        "vía Oliver 1989 cap.2, p.144]",
        "notas": (
            "Oliver 1989 cap. 2, p. 144. Var. hadabacoa. Morfología: ada- 'árbol' + "
            "-ba- (valor indeterminado) + -coa (postposición locativa superlativa). "
            "TOPÓNIMO: fuera del habla de los agentes, como referencia de canon."
        ),
        "categoria": "geografia",
    },
    "daitiao": {
        "sig": "pariente o aliado ritual (forma de 1.ª persona: 'mi aliado')",
        "cat": "sust",
        "fuente": "caquetío-atestiguado",
        "glosa_fuente": "DATIHAO: «lord: the one that loans his name to the slave» "
                        "[Oviedo y Valdés (1535-1557) 1944:41, vía Oliver 1989 cap.2, p.146]",
        "notas": (
            "Oliver 1989 cap. 2, pp. 146-147. VARIANTE de la forma `datihao` que el "
            "lexicón ya tiene: mismo lexema, /da-/ 1sg + raíz de parentesco /-(a)tti-/ + "
            "/-(h)o/ nominalizador. La 3pl es /wa-[gua-]/ → taíno waitiao/watiao > "
            "español guaitiao. Oliver DUDA de que datihao sea caquetío (n.42): sospecha "
            "que Oviedo pudo usar taíno, y concluye que quizá fuera «equally shared by "
            "both Taíno and Caquetío». Ver NUDO_DAITIAO."
        ),
        "categoria": "parentesco",
    },
}

AFIJOS_OLIVER: dict[str, dict] = {
    "-si": {
        "valor": "sufijo nominalizador (formas abstractas, partes del cuerpo, "
                 "herramientas, parentesco, objetos íntimamente poseídos)",
        "origen": "proto-arahuaco *-tsi / *-si (Matteson 1972:164)",
        "ejemplo_cq": "bari-si 'ceniza'",
        "pagina": 143,
        "confianza": "alta",
    },
    "-(h)o": {
        "valor": "sufijo nominalizador solemne; forma títulos y etnónimos",
        "origen": "taíno-lokono /-hu/",
        "ejemplo_cq": "dia-o, daitia-o, borati-o, kaket-ío",
        "pagina": 146,
        "confianza": "alta",
    },
    "-bana": {
        "valor": "'entorno, alrededor, extensión'; en lokono 'techo, cubierta'",
        "origen": "PM *-bana / *-pana (Noble 1965:101)",
        "ejemplo_cq": "ti-bana, judi-bana, cariru-bana, tausa-bana, yara-bana, Capu-bana",
        "pagina": 148,
        "confianza": "alta",
        "nota_proyecto": "El proyecto lo glosa 'orilla, borde'. Oliver da "
                         "'entorno, cubierta' — glosa mejor fundada.",
    },
    "-coa": {
        "valor": "postposición locativa superlativa ('en', 'sobre'); también "
                 "'punta, pico, proa'",
        "origen": "LK -aku (enfático/recíproco) + -oa (reflexivo, < -oaia) → -akoa",
        "ejemplo_cq": "uria-coa, toda-coa, pipia-coa, ri-coa, Túcua; con -ba-: a-ba-coa…",
        "pagina": 149,
        "confianza": "media",
    },
    "-oa": {
        "valor": "reflexivo, 'sí mismo'; en topónimos aparece como -Vr-oa",
        "origen": "LK -oa < -oaia (Taylor 1970b:32,35)",
        "ejemplo_cq": "ar-oa, botor-oa, er-oa, maur-oa",
        "pagina": 149,
        "confianza": "media",
    },
    "-ba- / -va-": {
        "valor": "INDETERMINADO — Oliver: «whose meaning is as yet undetermined»",
        "origen": None,
        "ejemplo_cq": "a-ba-coa, ura-ba-coa, guai-ba-coa, chi-va-coa, di-va-coa",
        "pagina": 149,
        "confianza": "ninguna",
    },
    "k- / kV-": {
        "valor": "prefijo atributivo ('que tiene', 'que pertenece a la clase de'); "
                 "alterna con cero de forma irregular",
        "origen": "Matteson 1972:164; Noble 1965:28",
        "ejemplo_cq": "bari-KI-si leído como 'que tiene la cualidad de rojo' (n.40)",
        "pagina": 120,
        "confianza": "media",
    },
    "mV-": {
        "valor": "prefijo/sufijo privativo ('sin')",
        "origen": "común a las lenguas maipuranas (n.43, p.147; n.40, p.143)",
        "ejemplo_cq": None,   # atestiguado en taíno m-a(h)i-te 'desdentado', no en CQ
        "pagina": 147,
        "confianza": "alta para maipurano; sin atestación caquetía",
    },
}


# =============================================================================
# 6. EL NUDO daitiao / datihao / diao — CERRADO
# =============================================================================

NUDO_DAITIAO = {
    "pregunta": "¿daitiao, datihao y diao son una palabra, dos o tres?",
    "veredicto": "DOS lexemas. daitiao = datihao (mismo lexema). diao es OTRA palabra.",
    "paginas": [146, 147],
    "evidencia": [
        ("Oviedo y Valdés registra DOS entradas separadas: «DATIHAO: lord: the one "
         "that loans his name to the slave» y «DIAO: Lord or cacique of the zaquitios "
         "territory» (p. 146). No son variantes de copia: son dos lemas del mismo "
         "diccionario."),
        ("Oliver les da DOS ETIMOLOGÍAS DISTINTAS. diao = /d-ia(o)/, sobre la raíz "
         "lokona /d-ai-/ de 'palabra/lengua' (dia 'palabra', daiya '(mi) lengua', "
         "adian 'lengua', dai-yana-ho 'príncipe'). datihao/daitiao = /da-/ + /-(i)tiao/, "
         "sobre la raíz de parentesco lokona /atti/ ('tío', 'padre', 'hija'), statu "
         "constructo dahati/wahati 'mi/nuestro pariente, aliado'."),
        ("Oliver llama a daitiao explícitamente «the variant term for 'lord' of "
         "daitiao» al introducir el pasaje de Las Casas — es decir, daitiao y datihao "
         "son la misma palabra en dos grafías coloniales."),
        ("La morfología de persona la da el propio Oliver, no es inferencia: «The "
         "prefix /wa- [gua-]/ is a third person plural marker, and /da-/ in da(i)tia-o "
         "is first person singular marker» (p. 147). Taíno waitiao/watiao 3pl > "
         "español «guaitiao» 'amigo, aliado'."),
    ],
    "confirma_a_zavala": (
        "SÍ. La minería de Zavala (F7) concluyó que daitiao/waitiao/guaitiao son un "
        "solo lexema con distinto prefijo de persona sobre la raíz /-atti-/, y que "
        "diao (Zavala #106) es otra palabra. Oliver, con el texto delante, dice "
        "exactamente eso — y además da los prefijos con su valor gramatical."
    ),
    "matiz_que_hay_que_conservar": (
        "Oliver escribe que «diao is, in many ways, closely related to datihao» "
        "(n. 42). Eso NO es una identificación: son parientes por compartir el "
        "prefijo /d-/ de 1sg y el sufijo /-(h)o/ solemne, no por compartir raíz. La "
        "frase se ha leído mal antes; con el texto completo el sentido es "
        "'formados con el mismo molde', no 'la misma palabra'."
    ),
    "duda_que_viaja": (
        "Oliver NO da datihao por caquetío con seguridad (n. 42, p. 146): Oviedo "
        "hablaba de «los indios de la Provincia de Venezuela» en general, y su larga "
        "residencia en La Española pudo hacerle usar taíno. Descarta el guajiro-"
        "paraujano («it does not exist in these languages today») y concluye que "
        "probablemente fuera «equally shared by both Taíno and Caquetío». Esa reserva "
        "debe quedar en la nota del lexicón. El proyecto tiene la entrada `datihao` "
        "etiquetada `caquetío-atestiguado` sin ella."
    ),
    "accion_lexicon": (
        "1) Añadir `daitiao` como variante de `datihao` (ver NUEVAS_ENTRADAS_CAQUETIO). "
        "2) Corregir la glosa de `datihao`: la de Oviedo es 'señor, el que presta su "
        "nombre al esclavo'; la del lexicón dice 'padrino de cautivo', que es "
        "interpretación, no glosa de fuente (D7: separar glosa_fuente de "
        "identificacion_moderna). "
        "3) Trasladar la reserva de la n.42 a `notas`. "
        "4) `guaitiao` ya está en el lexicón como caquetío-atestiguado: es taíno "
        "según Oliver (3pl waitiao > préstamo español). Revisar la etiqueta."
    ),
}


# =============================================================================
# 7. EL ANCLA DEL «ARCO NORTEÑO» — VERIFICADA, Y NO DICE LO QUE SE LE ATRIBUYE
# =============================================================================

ANCLA_ARCO_NORTENO = {
    "afirmacion_atribuida": (
        "«Confirmación de que las dos hermanas más cercanas del caquetío son el "
        "wayuunaiki y el paraujano» — nota de fuente `oliver-1989-cap2.md`, "
        "«Qué ha dado», y ancla de [[01_familia_caquetia]] §2."
    ),
    "veredicto": "OLIVER DICE LO CONTRARIO.",
    "citas": [
        (150, "it seems reasonable, for the moment, to regard Caquetío as emerging "
              "from a similar background to that of Lokono rather than from a "
              "Guajiro-Paraujano ancestry"),
        (150, "a preliminary examination of selected Guajira-Falcón toponyms show far "
              "more differences in sound sequences than similarities"),
        (150, "I have tentatively placed Caquetío in the tree diagram model (Fig. 22) "
              "as more closely related to Lokono than to either Achagua-Piapoco or "
              "Guajiro-Paraujano"),
        (155, "Caquetío, which I have shown to have the strongest affinities with "
              "Lokono, probably diverged at a minimum point in time no later than 1.8 "
              "millennia and closer to 2.6 millennia"),
    ],
    "los_tres_pilares_de_oliver": [
        "El prefijo /dA-/ de 1.ª persona singular: solo lokono y taíno lo tienen "
        "(el guajiro-paraujano innovó /tA-/). Evidencia caquetía: diao, datihao, "
        "dare, dato.",
        "La innovación léxica auri 'perro', de distribución norteña.",
        "kaketío 'ser vivo' = lokono kakïtho.",
        "Y un cuarto, menor: el sufijo caquetío es -bana, no -pana, como el lokono.",
    ],
    "lo_que_si_dice_sobre_wayuu_y_paraujano": (
        "Guajiro y paraujano son entre SÍ las dos lenguas arahuacas más próximas que "
        "se conocen: 64.2% de vocabulario básico compartido, separación mínima de 1.0 "
        "milenio (ca. A.D. 900-1200), «No other known Arawakan language has as close "
        "affinities to Guajiro as Paraujano» (p. 115). Eso es una afirmación sobre "
        "ELLAS DOS, no sobre el caquetío. Oliver también refuta a Swadesh, que las "
        "daba separadas por 2.0 milenios."
    ),
    "distancias_medidas_por_oliver": {
        "guajiro–paraujano": "64.2% cognados · 1.0 milenio",
        "lokono–guajiro": "31.3% cognados · 2.6 milenios",
        "lokono–baniva": "28.7% · 2.7 milenios",
        "lokono–piapoco": "25% · —",
        "lokono–achagua": "18% · 3.8 milenios",
        "guajiro–achagua": "13% · 4.6 milenios (3.6 con dudosos)",
        "lokono–island carib": "43.7-52.5% · 1.4-1.8 milenios",
        "caquetío": "SIN MEDIR — no hay lista de 100 palabras. La posición de Oliver "
                    "es cualitativa y explícitamente «tentative».",
    },
    "matiz_honesto": (
        "Oliver hace salir al lokono, al island carib, al taíno y al caquetío del "
        "MISMO NODO del que salió el conjunto guajiro-paraujano (p. 155). Es decir: "
        "el caquetío es PRIMO del wayuunaiki, no hermano. El «arco norteño» sigue "
        "existiendo como hecho geográfico y de contacto — el Golfete linda con la "
        "Guajira — pero eso es contacto, no filiación, y Oliver no lo confunde. "
        "Registrar ambas cosas por separado (misma lógica que D7)."
    ),
    "consecuencia_para_el_proyecto": (
        "El lexicón tiene 781 entradas wayunaiki y 228 lokono: 3.4 a 1 a favor de la "
        "hermana que Oliver considera MÁS lejana. Si se sigue a Oliver, la lengua "
        "donante prioritaria para reconstruir huecos caquetíos debería ser el lokono. "
        "Esto NO es una tarea de esta sesión: es una decisión (candidata a D9)."
    ),
}


# =============================================================================
# 8. ADJUDICACIÓN DE LAS 441 FORMAS `hipotético-no-verificado`
# =============================================================================
# Las claves son criterios OPERATIVOS; minar_oliver_cap2.py las aplica al
# contenido real de lexicon_candidatos.py y cuenta. Aquí solo se definen.
# =============================================================================

CLAVES_ADJUDICACION = {
    "A1": {
        "nombre": "d- lokona convertida en t- caquetía",
        "criterio": "el candidato se generó de una forma lokona con /d-/ inicial y "
                    "la reconstrucción tiene /t-/ inicial (REGLAS_LK_CQ R13)",
        "veredicto": "DEGRADAR + CORREGIR",
        "fundamento": "C1 (Oliver pp. 136, 147): el caquetío conserva /d-/. "
                      "La /t-/ es la innovación guajiro-paraujana.",
        "que_hacer": "la forma correcta es la lokona con d- conservada; la "
                     "reconstrucción actual es reparable, no descartable",
    },
    "A2": {
        "nombre": "b- lokona convertida en p- caquetía",
        "criterio": "el candidato se generó de una forma lokona con /b-/ inicial y "
                    "la reconstrucción tiene /p-/ inicial (REGLAS_LK_CQ R5)",
        "veredicto": "DEGRADAR",
        "fundamento": "C3 (Oliver pp. 119, 142, 150): CQ barisi : LK bálisi : WY palíi; "
                      "CQ -bana y no -pana. Contraejemplo conocido: CQ para 'mar'.",
        "que_hacer": "marcar la inicial como indecidible; no usar la forma con p- "
                     "como si fuera reconstrucción",
    },
    "A3": {
        "nombre": "palatal guajira proyectada al s. XV",
        "criterio": "el candidato se generó de una forma wayunaiki que contiene "
                    "/ch/, /sh/ o /ñ/",
        "veredicto": "DEGRADAR",
        "fundamento": "C5 (Taylor 1978 en Oliver p. 119): esos tres fonemas «arose as "
                      "phonemes not very long ago» en guajiro, por palatalización de "
                      "/t/ o /l/. Proyectarlos al caquetío precontacto es un anacronismo.",
        "que_hacer": "la correspondencia conservadora es /t/ o /s/, no /ch/",
    },
    "A4": {
        "nombre": "hueco ya cubierto por caquetío atestiguado en Oliver",
        "criterio": "la glosa del candidato coincide con un concepto para el que "
                    "Oliver da forma caquetía atestiguada",
        "veredicto": "SUSTITUIR",
        "fundamento": "COGNADOS_OLIVER + NUEVAS_ENTRADAS_CAQUETIO",
        "que_hacer": "borrar el candidato y usar la forma atestiguada",
    },
    "A5": {
        "nombre": "regla vocálica sin respaldo",
        "criterio": "el candidato difiere de su fuente SOLO en vocales",
        "veredicto": "SIN VEREDICTO",
        "fundamento": "C9 (Oliver p. 105): las vocales quedan fuera del método "
                      "comparativo por falta de transcripción fonética fiable.",
        "que_hacer": "Oliver no puede adjudicarlos, ni a favor ni en contra. "
                     "Declararlo, no fingir que se resolvieron.",
    },
}


# =============================================================================
# 9. LO QUE ESTE CAPÍTULO **NO** DA (para que no se vuelva a buscar)
# =============================================================================

NO_DISPONIBLE = {
    "tablas_comparativas": (
        "NINGUNA de las tablas de vocabulario comparativo del capítulo tiene capa de "
        "texto. Tabla 3 (Arawakan Phoneme Reflexes, p.104) y Tabla 8 (Comparative "
        "Lexicostatistical Data, p.130) son páginas-imagen con solo el pie. Las Tablas "
        "4, 5, 6 y 7 (fonemas proto-arahuacos, achagua, piapoco, guajiro, paraujano, "
        "lokono) están embebidas como imagen dentro de páginas con prosa: ni siquiera "
        "el pie aparece en el texto. 24 páginas del PDF son solo pie de figura. "
        "Recuperarlas exige OCR sobre el render, no extracción de texto."
    ),
    "apendice_A": (
        "Las listas de 100 palabras de Swadesh para 31 lenguas arahuacas viven en el "
        "**Apéndice A**, que NO está en este PDF: el capítulo lo cita 5 veces "
        "(«Appendix A: Table A1, A2, A8, A9», «item #43, #53, #83, #87 Appendix A») "
        "pero no lo contiene. Ese apéndice es el que tiene la lista completa de "
        "términos caquetíos (Tabla 8) y los vocabularios cuyón. **Es la pieza que "
        "falta y la que más rendiría.**"
    ),
    "lo_que_si_hay_como_texto": (
        "Cuatro tablas pequeñas SÍ salieron como texto y se recuperaron: (a) los 6 "
        "pares de Taylor 1977:38 guajiro/lokono/island carib (p.119); (b) los 5 "
        "cognados dudosos guajiro-paraujano con sus correspondencias (p.114); (c) los "
        "8 cognados dudosos lokono-achagua (p.122); (d) las Tablas 9 y 10 de milenios "
        "de separación (pp.130-131). Todos están volcados en este módulo."
    ),
}


# =============================================================================
# 10. COGNADOS DUDOSOS QUE OLIVER TABULA (no caquetíos, pero son datos duros)
# =============================================================================

DUDOSOS_TABULADOS = {
    "guajiro_paraujano": {
        "pagina": 114,
        "filas": [
            # (item, glosa, guajiro, paraujano, relación de sonidos según Oliver)
            (23, "árbol",  "mojuhi",  "jínghi / jáki",   "/j/ : /j/; /h/ : /k, [gh]/"),
            (30, "sangre", "sha'",    "-ayá",            "/sh/ : /y/"),
            (33, "huevo",  "ashu'kú", "chüyúk / hüyúk",  "/sh/ : /ch/; /-u'kú/ : /úk()/"),
            (44, "lengua", "ayéuá",   "-ebeñe / -weña",  "metátesis ayé : eña; /y/ : /ñ/"),
            (56, "morder", "ojóttá",  "oródi",           "/t/ : [d], pero /x/ ≠ /r/"),
        ],
        "correspondencias_seguras": [
            "Gu /ch/ : Pa /ch/ y alófonos [y], [ty] — 'este' chia' : chi/tyi (#4)",
            "Gu /ch/ : Pa [y] — 'nariz' eichi : eiyi (#41); Wilbert: ta-idyi 'mi nariz'",
            "Gu /y/ : Pa /ñ, ny/ — 'persona' wayú : añú/anyú (#18)",
            "Gu /k/ : Pa /k/ y alófonos [g, gh, ky] — 'fuego' siki : chighe (#82); "
            "'boca' anuku : -unaga (#42)",
            "Gu /ch/ : Pa /sh/ — 'ese' chia' : shira (#5)",
        ],
        "alofonos_paraujano": "/p/=[p,pw,b] · /t/=[d,ty] · /k/=[k,g,g',ky] · "
                              "/ch/=[ch,ty,y] · /m/=[m,mw] · /w/=[w,m] · /n/=[n,~v,~n] "
                              "(Patte 1978:59)",
        "nota": (
            "Etimología del propio nombre «paraujano» (n. 27, p. 110): /palaá/ 'mar' "
            "+ /añú/ 'gente' > palaáuhañú 'gente del mar' — término guajiro y "
            "DESPECTIVO ('animales que comen pescado apestoso'). El autónimo es Añú/Añún."
        ),
    },
    "lokono_achagua": {
        "pagina": 122,
        "filas": [
            (2,  "tú",      "b-íi",          "j-ïa, j-ía",   "/b/ : /h, x/ ['j']"),
            (12, "dos",     "bíama",         "juchamata",    "/m/ : /m/"),
            (36, "pluma",   "(o)-bára",      "baí-si",       "/b-/ : /b-/ pero r ≠ ()"),
            (38, "cabeza",  "*d-a-sí, -isíi", "bí-ta-sí",    "*/d/ : /t/"),
            (49, "vientre", "-dibeio",       "yabai-sí",     "/-b-/ : /-b-/"),
            (57, "ver",     "dïkhï-",        "nukabáu",      "/kh/ : /k/"),
            (91, "negro",   "khareme",       "kachajureyí",  "/kh/ : /k/"),
            (97, "bueno",   "*u-sa, sa-",    "saíka-",       "/s-/ : /s-/"),
        ],
        "nota": "«*» = pre-lokono (ss. XVI-XVIII). Oliver los cuenta como DUDOSOS.",
    },
    "part_whole": {
        "pagina": [120, 122],
        "casos": [
            "'árbol': LK ada vs. WY ata' 'corteza/piel' — Oliver NO los cuenta como "
            "cognados en la lexicoestadística, aunque la raíz sí lo sea",
            "'flor' WY así vs. 'semilla' LK isíi — no contados",
            "'cielo'/'nube': achagua kasarianayi 'nube' ~ lokono kasako 'cielo'; "
            "LK oraro 'nube', achagua erri 'cielo' — significados intercambiados",
            "'palo': WY wunnú / (w)unú?u : LK kunnuku — comparar con TN konuko 'conuco'",
            "'hoja': WY apána : LK adobona — cognados",
        ],
        "leccion": (
            "En arahuaco, «árbol», «corteza», «piel», «hoja», «madera» y «bosque» "
            "rotan sobre la misma raíz. Emparejar por glosa española es exactamente "
            "el error que produjo las 441."
        ),
    },
}


__all__ = [
    "FUENTE", "COGNADOS_OLIVER", "CORRESPONDENCIAS_OLIVER",
    "PARES_VALIDACION_OLIVER", "REVISIONES_REGLAS",
    "NUEVAS_ENTRADAS_CAQUETIO", "AFIJOS_OLIVER",
    "NUDO_DAITIAO", "ANCLA_ARCO_NORTENO", "CLAVES_ADJUDICACION",
    "NO_DISPONIBLE", "DUDOSOS_TABULADOS",
]
