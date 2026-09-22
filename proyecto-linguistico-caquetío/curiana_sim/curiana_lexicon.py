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
    # "buco" → fusionada con "buko" (D5b, tanda 2026-08-30): el lema fonémico sobrevive (D5a)
    #   y la grafía de fuente viaja en forma_fuente. Cita reina: Ballesteros 1550. Ver la entrada buko.
    "biro":       {"sig": "sal",                                            "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 (Angulo Molina); recurso estratégico Coro", "categoria": "comercio"},
    "chiriware": {"sig": "gavilán, ave rapaz grande",                      "cat": "sust",  "fuente": "caquetío-retroabstraido", "notas": "Zavala Reyes 2015, glosario #84 (HB): «Gavilán» [atribución débil: voz zoonímica panvenezolana] — REPARTO 2026-09-10 (Miguel: «una por una según lo que digan sus notas»): a RETROABSTRAÍDO porque su propia nota lo pedía — «atribución débil: voz zoonímica panvenezolana». La voz está documentada; lo incierto es que el sustrato sea caquetío y no castellano regional. 🔴 CORRECCIÓN, mismo día: dije que estas 6 eran INVISIBLES para los perfiles. Falso — `capa_epistemica()` manda `caquetío` a secas a `caquetío-atestiguado`, y lo documenta. El defecto era el CONTRARIO y peor: se las promovía en silencio a atestiguadas, esta incluida, cuyo propio comentario decía que la atribución era débil.", "forma_fuente": "chiriguare"},
    "maure":      {"sig": "fibra de algodón, hilo para tejer",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, nota al pie (3): «Maure: fibra de algodón con la que tejían las hamacas»; Alvarado 1921, p.216 s.v. MÁURE (Carvajal 168 y Castellanos la registran como faja o tejido; en Coro vivía en 1921 como pieza de dril)", "notas": "REPARTO 2026-09-10: a ATESTIGUADO. Cuatro apoyos y uno de ellos local: Zavala nota al pie (3), Alvarado 1921 p.216, Carvajal 168 y Castellanos; y Alvarado la registra VIVA EN CORO en 1921. No es voz suelta del área: está anclada en el sitio."},
    "urari":      {"sig": "veneno/medicina vegetal (curare)",               "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 (AM); artículo de comercio", "categoria": "comercio"},
    "korie": {"sig": "armadillo",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "RESUELTO 2026-08-24 (#46). Glosa anterior: 'choza, habitacion, espacio propio', que su propia nota admitia sin fuente localizada (ausente de Alvarado 1921 y de van Buurt 2014). Tres fuentes dicen armadillo: Zavala Reyes 2015 #90 (HB); el CANON del proyecto (genealogia.yaml da 'corie (armadillo)' como totem del linaje Paugis, y la ficha de Buio-sha lo usa como elogio); y Oliver 1989, Apendice A, Tabla A-9 «Selected Caquetio Vocabulary from the XVIth Century», pp. impresas 593-594, leida sobre la imagen por Miguel el 2026-08-24: 'corie | korie | armadillo | armadillo'. La agente Korie-ko conserva su nombre: lo que cambia es que significa — REPARTO 2026-09-10: a ATESTIGUADO. Su nota ya declaraba el marcador 3-0 al resolver #46: Zavala #90 (HB), el canon del propio proyecto (genealogia.yaml, tótem del linaje Paugis) y Oliver 1989 Apéndice A.", "forma_fuente": "corie"},
    "saruro":     {"sig": "boa, serpiente no venenosa",                 "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "RESUELTO 2026-08-24 (#47). Glosa anterior: 'arbol saruro', cuyo unico rastro era una lista de Notion citada en DISENO_KOINE §8 — y alli se usa para confirmar la terminacion -aro/-uro, NO para sostener la glosa. A favor: Zavala Reyes 2015 #224 (E) 'Serpiente no venenosa. Boa constrictora'. AVISO: MARCADOR 1-0, no 3-0 — comprobado que `saruro` NO aparece en la Tabla A-9 de Oliver, asi que no hay tercera fuente; se decide con menos respaldo que #45 y #46 y conviene saberlo. Apoyo lateral: la A-9 da tres palabras en -ure sobre seres vivos (bisure lagartija, chaure buho, maure tejido), asi que la terminacion es compatible con un animal. La agente Saruro-sha conserva su nombre", "notas": "REPARTO 2026-09-10: a ATESTIGUADO, pero CON LA RESERVA QUE SU NOTA YA TRAÍA: marcador 1-0, no 3-0 — `saruro` NO está en la Tabla A-9 de Oliver, así que el único apoyo es Zavala #224 (E). Una sola fuente citada es el listón normal de la capa atestiguada (la mayoría del lexicón es Zavala-solo), y lo que la distingue de chiriware y tukeke es que NO se ha medido como voz panvenezolana. Si apareciera que lo es, baja a retroabstraído."},
    "tukeke": {"sig": "lagartija pequeña, gecko",                       "cat": "sust",  "fuente": "caquetío-retroabstraido", "notas": "Zavala Reyes 2015, glosario #257 (E+A+PMA): «Lagarto casero»; Alvarado 1921, p.300 s.v. TUQUEQUE (geco: Thecadactylus rapicaudus / Gonatodes albogularis); van Buurt 2014 §6 s.v. waltaca deriva el papiamento totèki de «tuqueque, tuteque, an Amerindian word used for geckos in Venezuela» [atribución débil: voz venezolana corriente, ninguna fuente la localiza en Coro] — REPARTO 2026-09-10: a RETROABSTRAÍDO por la misma razón que su nota ya declaraba — «voz venezolana corriente, ninguna fuente la localiza en Coro». Tres fuentes dan la palabra (Zavala #257 E+A+PMA, Alvarado p.300 con dos especies de geco, van Buurt vía el papiamento totèki): lo que falta no es documentación, es la atribución al caquetío. ⭐ Y es una de las tres que Jahn nombra al describir la costumbre de poner a la gente nombres del reino animal («picure, venado, tuqueque»).", "forma_fuente": "tuqueque"},
    "coro":       {"sig": "espina",                                          "cat": "sust",  "fuente": "caquetío-hipotético", "lectura_en_disputa": "tres lecturas compiten y ninguna cierra: 'espina' (González Batista, «El nombre de Coro»), 'avispa o lagartija' (Arcaya 1920 p. 170) y 'viento' (Castellanos 1589). Se enseña la que TIENE FUENTE TRABAJADA en el repo, con la disputa declarada", "notas": "F8 (2026-09-12): etiqueta vieja `caquetío-hipotético/topónimo` · D10 (2026-08-03), grupo 3 — BAJA DE TIER, no cambia de lengua. La glosa «cardón grande, cactus columnar» que esta entrada llevaba hasta el 2026-09-21 NO salía de ninguna fuente localizada, y su propia nota lo declaraba: Zavala Reyes 2015 sección D dice que su #181 es Koro = «Cotorra» (entrada aparte en el lexicón, con su cita), no cardón; en Alvarado 1921 la palabra coro aparece 55 veces y siempre como TOPÓNIMO; van Buurt 2014 solo la menciona como la ciudad · d21.15 (2026-09-21, decisión de Miguel): la curación NO es quitar la glosa sino CAMBIAR LA INVENTADA POR LA QUE SÍ TIENE FUENTE. González Batista, «El nombre de Coro» (4-fuentes/gonzalez-batista-nombre-de-coro.md, trabajada en 6-fusion/toponimia_coro_espina.yaml y ya registrada como lectura en 2-lengua/toponimos.yaml §Coriana, con el veredicto de Miguel del 2026-08-25: «PLAUSIBLE, la línea más prometedora del autor, abierta») da `coro` 'espina' → Coriana 'tierra de las espinas, o la tierra del espinar, de vegetación espinosa, e INDIRECTAMENTE tierra de cardones', con `paragua` + `na` como paralelo. O sea que «cardón» no era la glosa: era la CONSECUENCIA INDIRECTA que la propia fuente declara, y se enseñaba como si fuera el dato. Reparos anotados y no escondidos: la lectura depende de `na` = 'tierra', que ninguna fuente impresa da (Zavala #184: 'como, semejante'), y el ejemplo `corocoro` del autor se refutó con Alvarado 1921 (onomatopeya del canto del ave); la tesis aguanta por `tococoro`/`totocoro` vivos en la arquitectura coriana, por el 'fruto del cardón' de Zavala y por el cardonal de Coro en los linderos. La entrada NO se borra y el canon NO se toca: coro da nombre a la ciudad de Coro y aparece en todo el sitio público. `kadushi` se queda como la atestiguación insular del cactus (van Buurt 2014, islas A/B/C, var. *cadushi* en Aruba; Gatschet 1885 sobre material de Pinart, Aruba 1882, «kaduski»), con el matiz de que van Buurt advierte que su lista es de «words LIKELY to be of Caquetío origin» y «has a subjective element»"},
    "caraota":    {"sig": "frijol negro, legumbre",                         "cat": "sust",  "fuente": "español-colonial", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A ESPAÑOL. Alvarado 1921 p.58 s.v. CARAOTA la describe como el nombre corriente panvenezolano de las judías (Phaseolus, Canavalia, Pachyrrhizus), sin declararle origen indígena. Y Zavala Reyes 2015 sección D la cierra: su glosario #162 glosa el caquetío «icoroata» como 'caraota' — caraota es la GLOSA española, icoroata la voz caquetía"},
    "pauji":      {"sig": "árbol espinoso de fruto pequeño (Bumelia buxifolia)",                      "cat": "sust",  "fuente": "caribe-cháima", "glosa_fuente": "Bumelia buxifolia. Sapotáceas. Árbol espinoso, de hojas elípticas... [Alvarado 1921 p.244 s.v. PAUJÍ; cf. p.175 s.v. IGÜÍ: «Bumelia buxifolia, árbol maderable. Paují, Malarmo. Coro»]", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL Y GLOSA CORREGIDA. En Alvarado 1921 p.244 paují es un ÁRBOL derivado del chaima, no el ave. Y Zavala Reyes 2015 sección D lo confirma por otra vía: su glosario #197 glosa el caquetío «paugis» como 'paují' — es decir, paují es la palabra ESPAÑOLA y paugis la caquetía (la que lleva la agente Paugis-sha). El ave sigue teniendo nombre propio en el lexicón; lo que sale del caquetío es la forma española"},
    "manaure":    {"sig": "título laudatorio del señor principal (var. managuanare, managuarire)", "cat": "título", "fuente": "caquetío-atestiguado", "notas": "González, Carlos (estudio histórico del PLINCODE, p.23), citado en Zavala Reyes 2015 nota al pie (2): 'el cacique caquetío no se llamaba Manaure, pues este era un término laudatorio pero no el único, también recibía los dictados de managuanare, managuarire'. curiana_agents.py ya usaba este dato en el system_prompt de Manaure sin cita"},
    "curiana":    {"sig": "territorio de los caquetíos / lugar del cardón", "cat": "topón", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, nota al pie (4): «Curiana: territorio donde estaban asentados los caquetíos»", "notas": "REPARTO 2026-09-10: a ATESTIGUADO. Zavala nota al pie (4) la glosa como topónimo-etnónimo, y el canon la sostiene por todos lados — es el nombre del proyecto y el del pueblo que Arcaya identifica con Coro."},

    # ── Arahuaco compartido (cognados en Wayunaiki, Lokono, Taíno) ──
    "wayuu":      {"sig": "persona, gente, ser humano",                     "cat": "sust",  "fuente": "wayunaiki"},
    "anüiki":     {"sig": "habla, palabra, lengua",                         "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `adija` 'hablar, decir; palabra' — otra raíz. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "anasa":      {"sig": "bueno, bien, bello (< anasü Wayunaiki)",         "cat": "adj",   "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "taya":       {"sig": "yo (1ra persona singular)",                      "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `de`/`dai` 1sg — en el lexicón y en Perea 1942. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "waya":       {"sig": "nosotros (1ra persona plural)",                  "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `we`/`wai` 1pl — PARECIDA; `wai` sale 231 veces en Perea. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "pia":        {"sig": "tú (2da persona singular)",                      "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `bi`/`bui` 2sg — en el lexicón y en Perea 1942. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "nüma":       {"sig": "él/ella (pronombre 3ra persona)",                "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `li`/`tho` 3sg. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "naya":       {"sig": "ellos, ellas (3ra persona plural)",              "cat": "pron",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `na-` 3pl. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},

    # ── Taíno (familia arahuaca, préstamos a todas las lenguas caribeñas) ──
    "cacique":    {"sig": "jefe, señor principal de la comunidad",          "cat": "sust",  "fuente": "taíno"},
    "maíz":       {"sig": "planta de maíz, grano principal",               "cat": "sust",  "fuente": "taíno"},
    "yuca":       {"sig": "tubérculo, mandioca amarga o dulce",             "cat": "sust",  "fuente": "taíno", "notas": "Tno. yuca; cognado Lokono mariti", "categoria": "flora"},
    "batata":     {"sig": "camote, tubérculo dulce",                        "cat": "sust",  "fuente": "taíno", "notas": "Tno. batata; arahuaco del área caribeña", "categoria": "flora"},
    "bohío":      {"sig": "casa comunal, choza redonda con techo cónico",   "cat": "sust",  "fuente": "taíno"},
    "konuko": {"sig": "huerto familiar, parcela cultivada",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en taíno", "fuente": "caquetío-reconstruido", "forma_fuente": "conuco"},
    "iguana":     {"sig": "lagarto grande, iguana",                         "cat": "sust",  "fuente": "caquetío-reconstruido", "notas": "Decisión de Miguel 2026-09-12: tainismo panhispánico que Medina Colina recoge en el habla paraguanera (s.v. iguana, página no dictada) → `caquetío-reconstruido`, forma justificada por cognado en taíno, como kanoa/hamaca/konuko; NO atestiguada porque la vía pudo ser el español. Etimología: origen taíno según el cruce del dictado. Etiqueta anterior: `taíno` · F8 (2026-09-12): etiqueta vieja `taíno/caribe`: la voz circula también en caribe"},

    # ── Raíces verbales arahuacas (reconstruidas por comparación) ────
    "naa":        {"sig": "ir, moverse hacia",                              "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "waa":        {"sig": "venir, aproximarse",                             "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "kaa":        {"sig": "estar, existir, ser (cópula)",                   "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    # `paa` 'dar, ofrecer, transferir' ARCHIVADA el 2026-09-19 (política
    # «manda la atestiguada»): su rival atestiguada es `were` (Zavala #149).
    # Está en FUERA_DEL_HABLA con su procedencia. Es el archivo más caro de la
    # tanda: 56 formas flexionadas y 1.222 usos en la base.
    "maa":        {"sig": "decir, hablar, comunicar",                     "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "taa":        {"sig": "tomar, coger, recibir",                          "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco", "fuente": "caquetío-reconstruido"},
    "chaa":       {"sig": "hacer, construir",                               "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco · d21.16 (2026-09-21): la glosa decía «hacer, construir, crear» y ese «crear» la emparejaba con `eroa` «empezar, crear, originar», que es ATESTIGUADA — y no son lo mismo: uno construye, el otro origina. Miguel: «efectivamente pasa lo mismo, son símiles pero que tienen significados distintos también». Se quita «crear»; la entrada no se archiva, porque sin el solapamiento no hay par", "fuente": "caquetío-reconstruido"},

    # ── Única frase Caquetía atestiguada ──────────────────────────────
    # "Chacamba cudanga" = ¿Cómo está usted? (saludo)
    # "Cudan de cuté"    = Para servirle a usted
    "chakamba": {"sig": "¿cómo? (pregunta de estado)",                    "cat": "interr","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.73, citando a Arcaya (1995): «fórmula de saludo: chacamba cudanga (¿Cómo está usted?)», recogida a una anciana de Mitare. Es la única frase caquetía conservada", "forma_fuente": "chacamba"},
    "kudanga": {"sig": "usted, vos (2da persona formal)",                "cat": "pron",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.73, citando a Arcaya (1995): «chacamba cudanga (¿Cómo está usted?)»", "forma_fuente": "cudanga"},
    "kudan": {"sig": "servir, estar al servicio de",                   "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.73, citando a Arcaya (1995): «cudan de cuté (para servir a usted)»; variante de 1905: «judan de cuteo»", "forma_fuente": "cudan"},
    "kuté": {"sig": "a usted, para usted (dativo formal)",            "cat": "pron",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.73, citando a Arcaya (1995): «cudan de cuté (para servir a usted)»", "forma_fuente": "cuté"},

    # ── Verbos arahuacos (cognados Lokono / Wayunaiki / Garifuna) ────
    "wana":       {"sig": "ver, observar, mirar",                           "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'ver'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "suna":       {"sig": "dormir, reposar, descansar",                     "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "masa":       {"sig": "comer, alimentarse",                             "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "awa":        {"sig": "beber, tomar líquido",                           "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    # `kira` 'escuchar, oír, atender' ARCHIVADA el 2026-09-19 (política «manda
    # la atestiguada»): su rival atestiguada es `jai` (Zavala #175). En
    # FUERA_DEL_HABLA con su procedencia y su deuda D11 intactas.
    "panaa":    {"sig": "saber, conocer, entender",                       "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "naba":       {"sig": "pensar, reflexionar, meditar",                   "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'pensar'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "kono":       {"sig": "sembrar, plantar, cultivar",                     "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/taíno", "fuente": "caquetío-reconstruido"},
    "raka":       {"sig": "querer, desear, necesitar",                      "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "rua":        {"sig": "cargar, transportar, llevar",                    "cat": "v_raiz","notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},

    # ── Naturaleza (cognados arahuacos) ─────────────────────────────
    "duna":       {"sig": "agua (corriente, bebible)",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en garifuna/lokono", "fuente": "caquetío-reconstruido"},
    "amana":      {"sig": "fuego, lumbre, brasa",                           "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    # `kali` 'sol' y `kasha` 'luna' ARCHIVADAS el 2026-09-19 (política «manda
    # la atestiguada»): sus rivales atestiguadas son `kasi` (Zavala #76) y
    # `kati` (Zavala #71). Están en FUERA_DEL_HABLA con su procedencia.
    "kaya":     {"sig": "lluvia, agua del cielo",                         "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono (juya-cogn)", "fuente": "caquetío-reconstruido"},
    "kuru":       {"sig": "árbol, madera, tronco",                          "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan · d21.16 (2026-09-21), punto 4 — CONVIVENCIA DECLARADA con `bara` 'palo, árbol' (atestiguada, Zavala #29 E). No es un bug de curación ni un par de la política «manda la atestiguada»: es VARIACIÓN REAL, y las dos se quedan. La distinción que las sostiene es la que la propia pareja de glosas enseña — `bara` es el PALO CORTADO (y su reduplicada atestiguada `barabara` es la madera dura, Zavala #30) y `kuru` el ÁRBOL VIVO con su madera y su tronco. Miguel: «al final no pasa nada si hay símiles, en todo lenguaje hay símiles»", "fuente": "caquetío-reconstruido"},
    "arima":      {"sig": "pez, pescado",                                   "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    # `habo` 'mar, océano, aguas grandes' ARCHIVADA el 2026-09-19 (política
    # «manda la atestiguada»): su rival atestiguada es `para` (Zavala #190),
    # que además ya ganaba el uso 311 a 125. En FUERA_DEL_HABLA. ⚠️ `haborü`
    # 'marejada' (habo+rü, hipotética) se queda: su raíz queda archivada y es
    # una de las deudas declaradas de la tanda.
    "dali":     {"sig": "tierra, suelo, polvo",                           "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en garifuna/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "suka":       {"sig": "noche, oscuridad",                               "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "bara":       {"sig": "palo, árbol",                         "cat": "sust",  "notas": "Decisión #101 (tanda 2026-08-30) — GLOSA CORREGIDA a la de las fuentes: Zavala Reyes 2015 #29 (E): «Palo, árbol», con Esteves 1989 y van Buurt 2014 diciendo lo mismo, y la prueba interna de barabara (Zavala Reyes 2015 #30: «Árbol de madera dura y pesada. Olivo») — la reduplicada de la misma raíz ya estaba atestiguada como árbol. Lectura descartada por D7: río, corriente fluvial (venía de cognado proto-arawakan/topónimo, sin cita) — queda registrada aquí, no se pierde · d21.16 (2026-09-21), punto 4 — CONVIVENCIA DECLARADA con `kuru` 'árbol, madera, tronco' (reconstruida). No es un bug de curación ni un par de la política «manda la atestiguada»: es variación real y las dos se quedan. `bara` es el PALO CORTADO —y `barabara`, su reduplicada atestiguada, la madera dura (Zavala #30)—; `kuru`, el árbol vivo", "fuente": "caquetío-atestiguado", "forma_fuente": "Bara"},
    "sima":       {"sig": "cerro, elevación del terreno",                   "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/topónimo (Barquisimeto) · d21.16 (2026-09-21), punto 5 — CONVIVENCIA DECLARADA con `turumako` 'cerro de cima plana, meseta' (atestiguada, Zavala #262 AM). Las dos se quedan y las dos se dicen: por el criterio de la política d19.b NO son par —«cerro, montaña, elevación» contra «cerro, meseta» es solapamiento parcial, no glosa idéntica— y Miguel: «me parece bien que convivan sima y turumako […] al final no pasa nada si hay símiles, en todo lenguaje hay símiles». Se afinan las dos glosas para que dejen de emparejar: aquí la elevación a secas, allí la cima plana. Y el argumento morfológico que cierra la tercera banda de aquel issue: `-bana` es un SUFIJO locativo, no un sustantivo; compone (`kali-bana`, `biro-bana`) pero no nombra, así que «cerro ya se dice con -bana» no se sostiene. El par 6 («sima») deja de estar abierto por esta vía: no se archiva ninguna", "fuente": "caquetío-reconstruido"},

    # ── Personas y parentesco ──────────────────────────────────────────
    "ama":        {"sig": "madre, mujer que nutre y da origen",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan universal", "fuente": "caquetío-reconstruido"},
    "baba":       {"sig": "padre, hombre que protege",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "buri":       {"sig": "hijo, hija, criatura, descendiente",             "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "nomi":       {"sig": "hombre adulto (no título)",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "wari":       {"sig": "mujer adulta (no título)",                       "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "wanü":       {"sig": "anciano, mayor, persona de saber acumulado",     "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'anciano'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "pütchi":     {"sig": "mensaje, palabra sagrada, voz del espíritu",     "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'mensaje'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},

    # ── Cuerpo ──────────────────────────────────────────────────────────
    "kabo":       {"sig": "cabeza, mente, lo alto de",                      "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "nii":        {"sig": "ojo, mirada, visión",                            "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono-cogn", "fuente": "caquetío-reconstruido"},
    "bari":       {"sig": "vientre, barriga, interior del cuerpo",          "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "arua":       {"sig": "alimento, comida, sustento (raíz de 'arawak')",  "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/proto-arawakan", "fuente": "caquetío-reconstruido"},
    "kapua":      {"sig": "amanecer, alba, primera luz del día",            "cat": "sust",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'amanecer'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "tüshi":      {"sig": "frío, temperatura baja",                         "cat": "adj",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'frío'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},

    # ── Partículas y conectores ────────────────────────────────────────
    # (permiten construir frases más complejas sin recurrir al español)
    "ka":         {"sig": "y, también, además, con (conector aditivo)",     "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en proto-arawakan", "fuente": "caquetío-reconstruido"},
    "mara":       {"sig": "pero, sin embargo, aunque (contraste)",          "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "saa":        {"sig": "si, cuando, al momento de (condicional/temp.)",  "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "naka":       {"sig": "después, luego, más tarde (temporal posterior)", "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "puna":       {"sig": "antes, ya, primero (temporal anterior)",         "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono", "fuente": "caquetío-reconstruido"},
    "kashi":      {"sig": "ahora, en este momento (temporal presente)",     "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'ahora'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · ⚠️ COLISIÓN DECLARADA (2026-09-19) con `kasi` 'sol', que la política «manda la atestiguada» acaba de poner en las plantillas: bajo `curiana_fonotactica.fonemizar` las dos dan el mismo esqueleto, `kasi`, y `prompt_reglas_completo` las enseña ahora las dos. `kashi` NO tiene rival atestiguado —la política no la alcanza— y se queda; lo que se declara es el choque. El motor no las confunde en ningún sitio medido: quien puede confundirlas es el hablante. Cambiar esta forma o reescribir el ejemplo de la plantilla para separarlas es decisión de Miguel y no está tomada. Medido en 6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml §colision_kasi_kashi", "fuente": "caquetío-reconstruido"},
    "wara":     {"sig": "muy, mucho, bastante (intensificador)",          "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna", "fuente": "caquetío-reconstruido"},
    "sulu":       {"sig": "adentro, dentro de, en el interior de",         "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'adentro'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "yama":       {"sig": "aquí, en este lugar (deíctico proximal)",        "cat": "part",  "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki-cogn — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'aquí'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md", "fuente": "caquetío-reconstruido"},
    "kana-pa":    {"sig": "allá, en ese lugar lejano (deíctico distal)",    "cat": "part",  "fuente": "lokono"},

    # ── Colores (cognados Wayunaiki / Lokono / proto-arawakan) ─────────
    "mütsia":     {"sig": "negro, oscuro (< mütsiisü Wayunaiki)",            "cat": "adj",   "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "kasuta":     {"sig": "blanco, claro, luminoso (< kasüttaa Wayunaiki)", "cat": "adj",   "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "sünatü":     {"sig": "rojo, color de la sangre (< ishasü)",            "cat": "adj",   "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki/lokono`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "tsipana":    {"sig": "verde, color de hoja fresca",                    "cat": "adj",   "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "kanawa":     {"sig": "amarillo, color del oro y del maíz seco",        "cat": "adj",   "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},

    # ── Números 6–10 (continúan la serie Wayunaiki) ────────────────────
    "aipirua":    {"sig": "seis (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "akaratsa":   {"sig": "siete (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},
    "meekisa":    {"sig": "ocho (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "mekietsa":   {"sig": "nueve (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},
    "polo":       {"sig": "diez (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},

    # ── Herramientas y objetos (cognados Lokono / proto-arawakan) ──────
    "buraka":     {"sig": "arco para cazar y pescar",                       "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "sipara":     {"sig": "flecha, dardo arrojadizo",                       "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "atara":      {"sig": "red de pesca, malla tejida",                     "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "kanua":      {"sig": "canoa pequeña, balsa de un tronco",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono-cogn`"},
    "paugis":     {"sig": "paují, pavón de monte (variante de pauji)",      "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #197 (E+A): 'Paují'. CORREGIDO 2026-07-20: figuraba como 'vasija, totuma' (lokono/garifuna), lo que contradecía a la vez la fuente y la ficha del propio agente Paugis-sha ('tu nombre viene de paugis (paují): el ave que ve desde lejos')"},
    "kürara":     {"sig": "cuerda, soga, fibra trenzada",                   "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "shukua":     {"sig": "remo, pala para impulsar la canoa",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},

    # ── Intercambio y comercio (raíces y cognados arahuacos) ─────────
    "siwa":       {"sig": "blando",                                        "cat": "v_raiz","fuente": "caquetío-atestiguado", "forma_fuente": "sigua", "notas": "Decisión colisiones D5 (2026-08-31) — HOMÓNIMOS DECLARADOS: siwa-1 blando, caquetío-ATESTIGUADO (Zavala Reyes 2015 #227 «Sigua» (E); su homógrafo con el español era de la grafía y se disolvió con ella) y siwa-2 sal de comercio (< proto-arawakan *siwa, la entrada anterior de esta clave, capa lokono). La atestación directa gana la etiqueta — precedente de para (2026-07-20)"},
    "tüma":       {"sig": "perla, cuenta brillante del mar",                "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "karükera":   {"sig": "oro, metal amarillo (caona-cogn)",               "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): forma sin cita ni derivación declarada, etiquetada `taíno/lokono`"},
    "paratü":     {"sig": "trueque, intercambio de bienes (raíz paa-)",     "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `proto-arawakan`"},
    "taneka":     {"sig": "deuda, lo que se debe devolver (raíz taa-)",     "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "puruna":     {"sig": "mercado, lugar de trueque y reunión",            "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},

    # ── Ritual y espiritual (cognados Wayunaiki / Lokono / Garifuna) ───
    "yorua":      {"sig": "espíritu, ánima, ente del más allá",             "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "lapü":       {"sig": "sueño-visión, mensaje onírico (< lapü Wayuu)",   "cat": "sust",  "fuente": "wayunaiki"},
    "sakana":     {"sig": "ofrenda, dádiva ritual a los espíritus",         "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "outa":       {"sig": "muerte, fin de la vida (< outaa Wayunaiki)",     "cat": "sust",  "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "kataa":      {"sig": "vida, aliento vital (< kataa Wayunaiki)",        "cat": "sust",  "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki/lokono`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "wabarsure":  {"sig": "alma colectiva, espíritu del pueblo (wa+barsure)","cat": "sust", "fuente": "caquetío-reconstruido", "notas": "Decisión F1 (tanda 2026-08-30) — compuesto de trabajo del proyecto: wa- (posesivo 1pl, nuestro) + barsure (alma, ATESTIGUADO: Angulo Molina; Zavala Reyes 2015). Nunca buscarla en fuentes como palabra simple: no es palabra perdida sino derivación interna. De paso sale del limbo fuente=caquetío sin capa"},
    "mawari":     {"sig": "espíritu maligno, sombra del monte",             "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},

    # ── Flora local (cognados arahuacos y atestiguado) ───────────────
    "mankaba":    {"sig": "manglar, bosque de raíces en agua salobre",      "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "marawa":     {"sig": "palma, palmera de cogollo y fibra",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "kasiripa":   {"sig": "yuca brava, mandioca para casabe",               "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "marisi":     {"sig": "maíz en mazorca, grano de cosecha",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "yuri":       {"sig": "tabaco, hoja sagrada del piache",                "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "kukuisa":    {"sig": "cocuiza, agave de fibra para cuerda",            "cat": "sust",  "fuente": "español-colonial", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A ESPAÑOL. Alvarado 1921 p.84 s.v. COCUIZA (Furcraea spp.) cita a Caulín I.3: «una especie de pita que los indios llaman CARUATA y los españoles COCUIZA». La fuente separa las dos lenguas en la misma frase: el nombre indígena es caruata (voz cháima; tam. karuatá, cum. karúata) y cocuiza/kukuisa es el castellano. La entrada venía marcada «caquetío/topónimo»: el valor toponímico no se discute y se conserva en esta nota, pero no sostiene la filiación léxica"},

    # ── Fauna (cognados arahuacos) ───────────────────────────────────
    "hikoteya":   {"sig": "tortuga, galápago de agua y tierra",            "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "kaiwa":      {"sig": "caimán, lagarto grande de río",                  "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "tokoko":     {"sig": "flamenco o ibis, ave roja de la laguna",        "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "kanawari":   {"sig": "tiburón, gran pez del mar abierto",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "manatü":     {"sig": "manatí, vaca marina del golfete",               "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): forma sin cita ni derivación declarada, etiquetada `taíno/lokono`"},
    "ukura":      {"sig": "cangrejo, crustáceo del manglar",                "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},

    # ── Estado emocional (cognados Wayunaiki / Lokono / Garifuna) ──────
    "talata":     {"sig": "alegría, contento, gozo (< talataa Wayunaiki)",  "cat": "sust",  "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    # `mülia` 'miedo, temor, espanto' ARCHIVADA el 2026-09-19 (política «manda
    # la atestiguada»): su rival atestiguada es `etamo` (Zavala #120). Era
    # hipotética y con 0 usos en toda la base: el archivo más barato de la
    # tanda. En FUERA_DEL_HABLA con su procedencia.
    "muusa":    {"sig": "tristeza, pena, aflicción del ánimo",            "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "alaain":     {"sig": "amor, afecto, querer profundo (raíz raka-)",     "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): forma sin cita ni derivación declarada, etiquetada `wayunaiki/lokono`"},
    "jashichi":   {"sig": "rabia, ira, enojo (< jashichi Wayunaiki)",       "cat": "sust",  "fuente": "caquetío-reconstruido", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu)"},
    "japü":       {"sig": "vergüenza, pudor, sonrojo",                      "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): forma sin cita ni derivación declarada, etiquetada `wayunaiki/lokono`"},

    # ── Tiempo y clima (cognados arahuacos y derivados locales) ──────
    # `joutai` 'viento' ARCHIVADA el 2026-09-19 (política «manda la
    # atestiguada»): su rival atestiguada es `juri` (Zavala #178), que ya
    # ganaba 544 a 19. Declaraba en su propia glosa que venía del wayuu, que
    # es justo lo que D11 retiró. En FUERA_DEL_HABLA con su procedencia.
    "kayawara": {"sig": "tormenta, lluvia con viento fuerte (kaya+wara)", "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/proto-arawakan`"},
    "haborü":     {"sig": "marejada, oleaje grande del mar (habo+rü)",      "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    "madunaka":   {"sig": "sequía, tiempo sin agua (ma+duna)",              "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `proto-arawakan`"},
    "habobrisa":  {"sig": "brisa del golfete, viento suave del mar",        "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "F8 (2026-09-12): acuñación para la simulación sin cita, etiquetada `lokono/garifuna`"},
    # (fin de entradas nuevas — expansión a 146 palabras)

    # ── Expansión atestiguada — fuentes coloniales (Galeotto Cey, Oviedo y Valdés,
    #    Las Casas, Arellano Moreno, Zavala Reyes 2015, Van Buurt 2014, Gatschet 1885) ──
    "ateri":      {"sig": "hombre, varón",                                  "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #17 (GC): «Hombre»"},
    "iero":       {"sig": "mujer",                                          "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #163 (GC): «Mujer»"},
    "humokaro": {"sig": "mujer bella, hermosa",                           "cat": "adj",   "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #159 (GC): «Mujer bella»", "forma_fuente": "humocaro"},
    "kasi": {"sig": "sol",                                            "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #76 (GC): «Sol» · MANDA desde el 2026-09-19 (política «manda la atestiguada»): ocupa el sitio de `kali`, la forma reconstruida que quedó archivada en FUERA_DEL_HABLA. ⚠️ COLISIÓN DECLARADA con `kashi` 'ahora': bajo `curiana_fonotactica.fonemizar` las dos dan el mismo esqueleto, `kasi`, y desde esta tanda `prompt_reglas_completo` enseña las dos —ésta en NATURALEZA y `kashi` en CONECTORES, y el ejemplo de respuesta ideal las usa a tres líneas de distancia—. El MOTOR no las confunde (lookup exacto en `_familia_de_token`, token literal en el filtro de nombres, pertenencia a un set en la puerta de la competencia; `fonemizar` sólo entra por `_es_casi_autoglosa`, que compara una voz con su propia glosa); quien puede confundirlas es el hablante. Medido en 6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml §colision_kasi_kashi", "forma_fuente": "cazi"},
    "kiba":       {"sig": "piedra",                                        "cat": "sust",  "fuente": "caquetío-atestiguado", "forma_fuente": "quiva", "notas": "Decisión colisiones D5 (2026-08-31) — HOMÓNIMOS DECLARADOS bajo el mismo lema: kiba-1 piedra (Zavala Reyes 2015 #218 «Quiva» (E); y #92 «Cuiva. Kiba» (PMA) piedra — Arcaya registró la grafía k: el lema fonémico está impreso en la fuente) y kiba-2 ayuda (Zavala #203 «Quiba» (AM), cat v_raiz). La grafía b~v es betacismo colonial: mismo lema fonémico. El sentido piedra lleva el sig activo por la capa toponímica (van Buurt §8 siba/quiba piedra-roca; quibacoa, Todariquiba). Ambas salen del generado: FUSIONADAS_EN_LITERAL del miner"},
    "apana":      {"sig": "medida de tiempo: una luna (~30 días)",          "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #10 (GC): «Una luna. Medición de tiempo» · d21.16 (2026-09-21): la CABEZA de la glosa pasa a ser la medida, que es lo que la fuente pone delante; antes era «una luna (unidad de tiempo ~30 días)» y emparejaba con `kati` 'luna'. NO se reglosa a «mes»: la fuente dice «Una luna. Medición de tiempo» y su pareja `buiamati` «dos lunas» (#47), o sea un sistema de CONTAR LUNAS; llamarlo mes proyectaría el calendario europeo (regla 3). Miguel: «¿Entonces es más sobre el ciclo lunar pensando en la agricultura? Pero no sé si sea derechamente un mes, no?» — y lo de la agricultura tampoco lo dice la fuente, así que no se escribe"},
    "buiamati":   {"sig": "dos lunas (unidad de tiempo ~60 días)",          "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #47 (GC): «dos lunas. Medición de tiempo»"},
    "kasebo": {"sig": "poniente, oeste",                                "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #75 (GC): «Poniente»", "forma_fuente": "cazebo"},
    "kasikure": {"sig": "levante, este",                                  "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #77 (GC): «Parte del levante»", "forma_fuente": "cazicure"},
    "diao":       {"sig": "señor principal, jefe mayor",                    "cat": "título","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.67 (\'señor principal, jefe mayor\'); Oliver 1989 cap.3 p.251 llama a Manaure \'the main diao or great cacique\' — corregido de \'segundo orden\' (sin cita) a la glosa atestiguada · Cita primaria (campaña del taíno 2, T6, 2026-09-22; db.2): Oviedo y Valdés, Historia general, t. II (1852) impresa 299, Libro XXV: «en algunas partes desta gobernación de Venezuela el señor principal, que tiene muchos indios y le son subjetos otros caciques, llámanle diao», con sus exequias, «otra manera de obsequias de la que se dixo de suso». Alcance que Oviedo declara: la gobernación de Venezuela, no sólo Coro (regla 4). No cuelga de `datihao` (taíno): otra raíz en Oliver, /d-ia(o)/"},
    "apopo":      {"sig": "jefe de parcialidad pequeña",                    "cat": "título","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.65"},
    "boratio":    {"sig": "piache, cacique, jefe, sacerdote, médico",       "cat": "título","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, p.66; cf. Jahn 1927 p.213 n.29 (\'adivino o sacerdote\', vía Oviedo) · Cita primaria (campaña del taíno 2, T6, 2026-09-22; db.2): Oviedo y Valdés, Historia general, t. II (1852) pp. 298-299, `boratio` con UNA t: «afirman los boratios que le ven y hablan muchas veces [al diablo]… Estos boratios son como sacerdotes suyos», de los indios de la gobernación de Venezuela. La doble t de `borattio` es de la cadena Jahn/Arcaya. El glosario del editor (t. IV impresa 595) la da como «(Lengua de Venezuela)»"},
    "waitiao": {"sig": "amigo ritual, aliado de alianza",                "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Oliver 1989, cap. 2, p.147, sobre Oviedo y Valdés: mismo lexema que datihao sobre la raíz de parentesco /-atti-/, con distinto prefijo de persona; el pacto de guaitiao (intercambio de nombres entre aliados) lo describe Oviedo para el área circuncaribe", "forma_fuente": "guaitiao"},
    "datihao":    {"sig": "padrino de cautivo, el que presta su nombre al esclavo", "cat": "sust", "fuente": "taíno", "notas": "Decisión de Miguel 2026-09-22 (db.2, «dale con el punto 2»): re-etiquetada de `caquetío-atestiguado` a `taíno`. En el CUERPO de los cuatro tomos de Oviedo y Valdés (ed. Amador de los Ríos, 1851-1855) aparece UNA vez: t. I p. 473, en San Juan, en boca de Agüeybana — «á mi dalihao (que quiere deçir mi señor, ó el que, como yo, se nombra)» [la capa de texto da `dalihao`; la l/t no está verificada en imagen]. La marca «(Lengua de Venezuela)» es del GLOSARIO DEL EDITOR (t. IV impresa 598), y de ahí sale también esta `sig` («el que presta su nombre al esclavo»): no es la glosa de Oviedo, que dice «mi señor, ó el que, como yo, se nombra». Oliver, Jahn y Arcaya heredaron la etiqueta del editor. Campaña del taíno 2, T6 (#195). Etiqueta anterior: `caquetío-atestiguado` · Oliver 1989, cap. 2, p.147, sobre Oviedo y Valdés: forma atestiguada «daitiao», cognada del taíno daitia-o y del lokono da-tti / da-iti, sobre la raíz de parentesco /-atti-/, que en lokono cubre tío, padre e hija según el prefijo posesivo [pendiente: la forma del lexicón es datihao y la de Oliver daitiao — ¿metátesis de copia o dos formas?]"},
    "uriakoa": {"sig": "Uriacoa: antropónimo (apellido de un cacique del s. XVI)", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Oliver 1989 cap.3 pp.255-256: 'the Crown recognized Don Sancho Uriacoa as the Caquetío paramount chief'; le sucedió su hijo Don Luis Caguallo. CORREGIDO 2026-07-20: figuraba como 'título del cacique mayor de Curiana/Coro', una inferencia sin fuente a partir de un NOMBRE PROPIO — el mismo error que tenía 'diao'. El título atestiguado del jefe mayor es diao (Zavala Reyes 2015 #106); apopo es el de parcialidad pequeña (#12)", "forma_fuente": "uriacoa"},
    "tata":       {"sig": "padre, papá",                                   "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "D10 (2026-08-03), grupo 3 — BAJA DE TIER, no cambia de lengua. van Buurt 2014 la trae en su §11, «words with less certain links to Caquetío» (islas A/B/C, 'father'), NO en su §6 de voces probablemente caquetías: la propia fuente la coloca en la lista de menor confianza. Zavala Reyes 2015 glosario #243 (AM) «Padre, papá» la marca con fuerza D porque tata es panhispánico infantil, y Alvarado 1921 p.71 solo la registra en 'tata-cuá' (indígenas de Mérida). Ninguna la reasigna a otra lengua; lo que ninguna sostiene es la certeza"},
    "dare":       {"sig": "diente; hijo (extensión metafórica)",            "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #103 (HB): «Diente»; Oliver 1989 la confirma en Paraguaná — 🔴 DEUDA DECLARADA 2026-09-10 (regla 8): la glosa dice 'diente; HIJO (extensión metafórica)' pero las dos fuentes citadas dan solo DIENTE. El 'hijo' entró sin procedencia y no se ha localizado quién lo sostiene. Importa porque de él dependería leer `catire` como 'hijo de la luna' y `capadare` como algo distinto de 'diente de'. Mientras no aparezca la fuente, para componer vale 'diente'.", "deuda": "sin-procedencia (la acepción 'hijo')"},
    "sawaka":     {"sig": "inframundo, reino de los muertos",               "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "van Buurt 2014 §6 «words likely to be of Caquetío origin» (el autor advierte que la lista «has a subjective element»), isla C: «the underworld, the realm of the dead, the beyond»; en papiamento antiguo la expresión baha na sawaka = descender al inframundo, morir; paralelos en taíno y lokono"},
    "paro":       {"sig": "río, cauce simple",                              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #195 (AM): «Río»"},
    "kari": {"sig": "orilla del mar, costa",                         "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #66 (E): «Orilla del mar»; Cruz Esteves 1989 vía van Buurt 2014 §9 (topónimo Cariatávo), cari/kari = costa, orilla", "forma_fuente": "cari"},
    "rao":        {"sig": "arena, arenal costero",                         "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #219 (E): «Arena»"},
    "barici":     {"sig": "agua turbia, tierras coloradas rojizas",         "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #34 (HB): «Agua turbia». Referencia cruzada D5b (tanda 2026-08-30): NO fusionar con bariki (#35 «Barique», arcilla roja) — son entradas distintas de la fuente que solo colisionan al normalizar c/k. Posible raíz común bar- (agua turbia ~ tierra colorada): pregunta etimológica abierta, no duplicado"},
    "pariri":     {"sig": "pantano, ciénaga",                              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #194 (AM): «Pantano, ciénaga»"},
    "tarika": {"sig": "laguna, espejo de agua interior",               "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #242 (AM): «Laguna»", "forma_fuente": "tarica"},
    "wike": {"sig": "río navegable, cauce ancho",                    "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #152 (AM): «Río navegable»", "forma_fuente": "güique"},
    "kidi": {"sig": "sierra, serranía, cerro largo",                 "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #212 (AM): «Cerro, altura»", "forma_fuente": "quidi"},
    "borojo":     {"sig": "salina, lago salado de Coro",                   "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #44 (AM): «Salina de Coro, comercio de la sal» · #123 (Miguel, 2026-09-13, opción 3 — se queda atestiguada con el conflicto a la vista): Esteves 1989 t. 4 p. 90 (verificado en imagen) dice «Borojó es chibcha: un árbol frutal», sin argumento; el único borojó frutal conocido es el del Chocó (Alibertia patinoi), de nombre emberá y de selva húmeda — ni la lengua ni el árbol son de Falcón, así que la atribución parece un falso amigo. A favor de la filiación caquetía del topónimo: la historiografía local (pueblosdebuchivaoa.blogspot, «Conociendo a Borojó») da la fundación del pueblo el 7 de abril de 1715 por el alférez Juan de Ulacia y Albízu «en presencia de 20 indios de la tribu caquetía, su cacique BOROBO que habitaba en la región de Canapo», y piensa que el nombre viene del cacique. Miguel (2026-09-13): buscando Borojó/Borobó en línea sale lo de la salina. DEUDA: el acta de 1715 y el «boro = sal» que circula en la divulgación no tienen fuente primaria citada; AM no dice de dónde saca «salina». Verificar en González Batista o en el archivo de Coro."},
    "ucibo":      {"sig": "cuenta de piedra, chaquira",                    "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #267 (AM): «Cuenta de piedras»"},
    "buriche":    {"sig": "licor fermentado, chicha de maíz",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #50 (AM): «Licor fermentado»"},
    "buko":       {"sig": "presa de agua, represa, canal de riego",                "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Decisión D5b (tanda 2026-08-30) — FUSIONADA con buco: bajo D5a el lema fonémico sobrevive y la grafía de fuente queda aquí. CITA REINA: Ballesteros, Obispo de Coro, 1550: «Los indios antiguamente, una legua del río arriba tenían hecha una presa que ellos llaman buco» (vía Arcaya 1920 p.170, que declara citar de una copia — segunda mano; ver 4-fuentes/ballesteros-1550.md). Además Zavala Reyes 2015 #46 «Buko» (AM+CGB): «Chorro de agua, presa de agua». La reserva de Alvarado 1921 p.34 (sugería origen romance, localizaba en Lara) queda superada por la atestación de 1550 en el propio río de Coro; el topónimo vivo El Buko corrobora", "forma_fuente": "buco"},
    "wa": {"sig": "conuco, heredad, terreno cercado cultivado",    "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #122 (HP): «Conuco, heredad, terreno cercado con algo»", "forma_fuente": "gua"},
    "duraboa":    {"sig": "conuco sembrado, parcela en producción",        "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #115 (AM): «Conuco, sembrado»"},
    "tabri":      {"sig": "siembra, plantación en proceso",                "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #234 (AM): «Conuco, siembra»"},
    "tebe":       {"sig": "lugar de cultivo, campo agrícola",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #245 (AM): «Lugar de cultivo»"},
    "amaka": {"sig": "sitio de moler maíz, área de procesamiento",    "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #9 (AM): «Sitio de moler maíz»", "forma_fuente": "amaca"},
    "urapa":      {"sig": "sitio de cría de animales, corral",             "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #269 (AM): «Sitio de cría de animales»"},
    "garabal":    {"sig": "tierra de crianza, pastizal",                   "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #121 (AM): «Tierra de crianza o tierra de pasto»"},
    "kunuku":     {"sig": "parcela de cultivo, conuco insular (ABC)",      "cat": "sust",  "fuente": "taíno", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A TAÍNO. Alvarado 1921 p.89 s.v. CONUCO: «Voz taina», citando a Las Casas V.307 («esta labranza, en lenguaje de los indios desta isla, se llama conuco»). van Buurt 2014 lo dice igual en prosa: kanoa, komehein, kunuku, maïshi, pita y sabana derivan del taíno. Gatschet la trae, pero por la sección de PAPIAMENTO del artículo (Guía de Curazao 1876), no por la lista arubana: kunuku es la forma papiamenta del conuco taíno, no un caquetío insular"},
    "kasá": {"sig": "puche de maíz, atole",                         "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #74 (HB): «Puche de maíz»", "forma_fuente": "cazá"},
    "masato": {"sig": "bebida de harinas fermentada",                  "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Alvarado 1921, p.217 s.v. MAZATO, citando Oviedo II.297 y 300 («magato… brevaje») [atribución débil de la filiación: la forma es panamericana (masato peruano), la glosa sí está confirmada]", "forma_fuente": "mazato"},
    "kumarawa": {"sig": "caracol de las costas de Paraguaná",      "cat": "sust",  "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de caracol de las costas de Paraguaná [Alvarado 1921 p.102 s.v. CUMARAGUA]", "notas": "D10 (2026-08-03), grupo 2 — GLOSA CORREGIDA, la palabra sigue siendo caquetía. Alvarado 1921 p.102 es la localización más precisa de todo su glosario para una voz de esta lista: costas de Paraguaná. PREMISA CORREGIDA: la glosa anterior NO estaba sin fuente. La lectura que se descarta —Zavala Reyes 2015 glosario #93 (HB+E) «Ciruela, espuma rosada», fuerza F, y Arcaya 1920 sobre la Relación de Barquisimeto 1579 («mene y cumaragua nombre de la ciruela»)— queda registrada aquí íntegra por D7. Las dos son fuentes históricas y ninguna es moderna: el conflicto es real y D10 adjudica por localización", "forma_fuente": "cumaragua"},
    "auyama":     {"sig": "auyama, calabaza (Cucurbita maxima)",           "cat": "sust",  "fuente": "caribe-cumanagoto", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL. Alvarado 1921 p.16 s.v. AUYAMA: «Voz cum. que Ruiz Blanco traslada 'calabaza'», con variantes ayuyáma y huyáma y la cita de Castellanos (Cabo de la Vela). Familia caribe, no arahuaca. Zavala Reyes 2015 no la tiene (su sección E la da por ausente) y Gatschet tampoco: el papiamento usa pampuna, y ahullama aparece solo como voz española del guía de conversación"},
    "bajarí":     {"sig": "recorrer, caminar",                             "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #25 (AM): «Recorrer, caminar»"},
    "bureche":    {"sig": "bebida fermentada de casabe",                     "cat": "sust","fuente": "caquetío-atestiguado", "glosa_fuente": "Bebida fermentada que preparan los indios guayaneses poniendo por cierto tiempo en agua caliente el casabe [Alvarado 1921 p.34 s.v. BURECHE]", "notas": "D10 (2026-08-03), grupo 2 — GLOSA CORREGIDA y `cat` cambiada de v_raiz a sust: una bebida no toma sufijos de aspecto. PREMISA CORREGIDA: la glosa anterior NO estaba sin fuente — Zavala Reyes 2015 glosario #49 (AM) da bureche = «Hacer, realizar» con fuerza F, que es exactamente lo que el lexicón traía; queda registrado aquí por D7. DOS RESERVAS que la sesión reporta y no resuelve: (1) el lexicón ya tiene `buriche` (Zavala Reyes 2015 #50, AM: «Licor fermentado»), de modo que esta corrección crea un cuasi-duplicado y habrá que decidir si bureche y buriche son la misma entrada; (2) Alvarado localiza su bureche en GUAYANA, no en Coro"},
    "eroa":       {"sig": "empezar, crear, originar",                      "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #119 (AM): «Empezar, crear»"},
    "were": {"sig": "dar, entregar, ofrecer",                        "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #149 (AM): «Dar, entregar»", "forma_fuente": "güere"},
    "jakura": {"sig": "guardar, conservar, custodiar",                 "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #171 (AM): «Guardar»", "forma_fuente": "jacura"},
    "jai":        {"sig": "oír, escuchar",                                 "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #175 (AM): «Oír, escuchar»"},
    "jagey": {"sig": "estancar, represar, crear charco artificial",   "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #174 (AM): «Establecer, estancar» [atribución débil: jagüey es panamericano, de origen taíno]", "forma_fuente": "jaguey"},
    "jakuke": {"sig": "regar, irrigar",                                "cat": "v_raiz","fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #170 (AM): «Regar, regadío»", "forma_fuente": "jacuque"},
    "pana":       {"sig": "uno",                                           "cat": "num",   "fuente": "caquetío-atestiguado", "notas": "Pedro Manuel Arcaya; Zavala Reyes 2015", "categoria": "numerales"},
    "gudamuen":   {"sig": "dos",                                           "cat": "num",   "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #148 (PMA): «Numero dos»"},
    "sabuenen":   {"sig": "tres",                                          "cat": "num",   "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #222 (PMA): «Número tres»"},
    "katarí": {"sig": "cuatro",                                        "cat": "num",   "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #70 (PMA): «Número cuatro»", "forma_fuente": "catarí"},
    "kama":       {"sig": "tapir, danta (Tapirus terrestris)",             "cat": "sust",  "fuente": "caquetío-hipotético", "notas": "Decisión F1 (tanda 2026-08-30) — DEGRADADA: SIN_RASTRO real en las cuatro minerías (auditar_82); el lokono usa otra raíz (firobero). Candidata a reconstruido vía cognado proto-arahuaco *kema. RUTA CORREGIDA 2026-08-31: el Swadesh-100 de Oliver NO trae tapir (medido al minar la serie A-1..A-7); candidatos reales: el vocabulario paraujano completo de Wilbert (Tabla A-1), las voces de fauna de van Buurt, o la comparativa externa (Payne). Ver 6-fusion/tabla_a1_a7_swadesh.yaml"},
    "koke":       {"sig": "hormiga roja; bachaco, hormiga grande (Atta spp.)",           "cat": "sust",  "fuente": "caquetío-atestiguado", "forma_fuente": "coques", "notas": "Decisión F1/D5b (tanda 2026-08-30) — FUSIONADA con la grafía de fuente «coques»: Zavala Reyes 2015 #89 (HB): «Hormiga roja». No estaba SIN_RASTRO: las minerías buscaron la grafía k y no vieron la c (el mismo error de grafía que ocultó a Hurehurebo en Castellanos). Apoyo extra: cognados_oliver.py trae CQ coque, hormiga roja. La -s de coques es plural castellano de Zavala (cf. quibacoas). FUSIÓN CERRADA 2026-08-31: el miner casa ahora por forma_fuente y el #89 queda como YA_EN_LEXICON — coques dejó de ser entrada aparte del generado"},
    "kachikamo": {"sig": "armadillo (Dasypus novemcinctus)",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Alvarado 1921, p.41 s.v. CACHICAMO: glosa idéntica (Dasypus) [atribución débil de la filiación: voz de circulación nacional, Alvarado no declara origen ni la localiza en Coro]", "forma_fuente": "cachicamo"},
    "kaduchi": {"sig": "fruto del cardón (Cereus spp.)",                "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #55 (HB): «Higo, breva» [atribución débil: la fuente da la glosa española del fruto, no el referente local (cardón)]", "forma_fuente": "caduchi"},
    "kadushi":    {"sig": "cactus columnar (Cereus hexagonus)",            "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "van Buurt 2014 §6 «words likely to be of Caquetío origin» (el autor advierte que la lista «has a subjective element»), islas A/B/C: «a columnar cactus (Cereus repandus)», var. cadushi (Aruba); Gatschet 1885 (material Pinart, Aruba 1882), sección plantas, «kaduski» = Cereus lanuginosus; respaldo toponímico van Buurt §7 (cadushi) [referente ABIERTO por D7: tres cactus distintos bajo el mismo nombre — Gatschet Pilosocereus lanuginosus, van Buurt Cereus repandus, el lexicón Cereus hexagonus; el nombre es un genérico de cardón, no una especie] AMPLIACION 2026-08-24 (#51): Oliver 1989, Apendice A, Tabla A-9, leida sobre la imagen por Miguel el 2026-08-24 trae `caduchi` 'higo, breva' y `comoho` 'higo, tuna' como entradas DISTINTAS -- confirma que la salida correcta es lexico por especies (kadushi/cactus columnar, caduchi/breva, comoho/tuna, dato/fruto de cactus), no una glosa unica. Ver tambien testimonio retro-abstraido de Miguel: en Punto Fijo el fruto del cactus se llama 'dato'."},
    "tara":       {"sig": "langosta; tambien mariposa, polilla",       "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "RESUELTO 2026-08-24 (#45). Glosa anterior: 'venado, ciervo (Odocoileus virginianus)', que NO tenia fuente localizada. Tres fuentes independientes coinciden en insecto: Zavala Reyes 2015 #238 (HB+PMA+AM) 'Langosta, mariposa'; Alvarado 1921 p.283 (polilla o mariposa; cf. TARITA 'mariposa o tara pequena'); y Oliver 1989, Apendice A, Tabla A-9 «Selected Caquetio Vocabulary from the XVIth Century», pp. impresas 593-594, leida sobre la imagen por Miguel el 2026-08-24: 'tara | tara | langosta | locust'. Marcador 3-0. AVISO: al aplicarlo cae el ejemplo insignia de ecologia.yaml:624 ('el venado hoy ausente'), y la palabra caquetia del VENADO queda huerfana — es hueco lexico declarado, no se rellena a mano"},
    "warawara":   {"sig": "caracara, ave rapaz carroñera (Caracara cheriway)",          "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "van Buurt 2014 §6 «words likely to be of Caquetío origin» (el autor advierte que la lista «has a subjective element»), islas A/B/C: «the crested Caracara (Caracara cheriway syn. Polyborus plancus)»; respaldo toponímico §7 (Sero Warawara, Warawao, Aruba). La glosa anterior del lexicón («buitre, zamuro (Cathartes curasoica)») era, palabra por palabra, la identificación de Gatschet 1885 (material Pinart 1882), heredada sin saber de dónde venía: Cathartes es Cathartidae (zamuros) y Caracara es Falconidae. D7 registra las dos lecturas: la de 1885 queda aquí, la moderna pasa a la glosa activa"},
    "watapana":   {"sig": "árbol dividivi (Caesalpinia coriaria)",         "cat": "sust",  "fuente": "caribe-cumanagoto", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL. Alvarado 1921 p.163 s.v. GUATAPANAR: «Caesalpinia coriaria. Dividive. Del cum. araguatapanár, oreja de araguato, por la forma del fruto»; entre los guayuncomos del Alto Orinoco, arauotá-fanári es nombre propio. CONFLICTO DE FILIACIÓN NO CERRADO, y viaja aquí a propósito: van Buurt 2014 §6 la lista entre las «words likely to be of Caquetío origin» (islas A/B/C) con etimología arahuaca interna (-apana = hojas, wa-/wu- pluralidad), y Gatschet 1885 (material Pinart, Aruba 1882) la registra con taxón. D10 adjudica a Alvarado para la forma continental; la vertiente insular sigue siendo argumento vivo"},
    "chogogo":    {"sig": "flamingo rosado (Phoenicopterus ruber)",        "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "van Buurt 2014 §6 «words likely to be of Caquetío origin» (el autor advierte que la lista «has a subjective element»), islas A/B/C: «the greater flamingo (Phoenicopterus ruber)»"},
    "chuchubi":   {"sig": "sinsonte tropical (Mimus gilvus)",              "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #85 «Chuchube» (HB): «Paraulata»; Gatschet 1885 (material Pinart, Aruba 1882), sección aves, «shushubi» = Orpheus americanus; van Buurt 2014 §6 «chuchubi» (islas A/B/C) = Mimus gilvus. Triple atestación continental-insular-viva; la alternancia sh~ch es la correspondencia que describe van Buurt"},
    "bariki":     {"sig": "tierra colorada, pigmento encarnado, pintura corporal", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #35 «Barique» (AM+HB): «Arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija»; Arcaya la cita también en la Relación de Barquisimeto 1579. Referencia cruzada D5b (tanda 2026-08-30): NO fusionar con barici (#34, agua turbia) — entradas distintas de la fuente", "forma_fuente": "Barique"},
    "mene":       {"sig": "brea, betún natural; rezumadero de asfalto",   "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "RESUELTO 2026-08-24 (#52). Glosa anterior: 'sustancia que brota de la tierra (petroleo, resina)' — 'petroleo' es anacronico: lo que el hablante del s. XV nombraba es el MATERIAL que se ve y se usa (calafateo, impermeabilizacion). Tres fuentes convergen en brea: Oviedo II.301 'betun a manera de brea' via Alvarado 1921 p.218 s.v. MENE (que ademas cita a Codazzi localizando los yacimientos en Coro y Maracaibo); Oliver 1989, Apendice A, Tabla A-9 «Selected Caquetio Vocabulary from the XVIth Century», pp. impresas 593-594, leida sobre la imagen por Miguel el 2026-08-24: 'mene | mene | viruela / pez derretida | smallpox / tar' — 'pez' ahi es LA pez, femenino, no un pescado —; y el uso toponimico vivo (Mene Mauroa, Mene Grande son manaderos de asfalto). AVISO: la acepcion 'VIRUELA' que Oliver tambien recoge queda SIN registrar aqui, es post-contacto por definicion y merece decision aparte. Y Oliver glosa igual `cumaragua`, mientras Arcaya empareja las dos palabras como 'nombre de la CIRUELA' — una letra de diferencia, probable errata; ver #38 y D10"},
    "poporo":     {"sig": "maza-porra, arma de combate ceremonial",        "cat": "sust",  "fuente": "caquetío-atestiguado", "notas": "Alvarado 1921, p.255 s.v. POPORO: la atribuye explícitamente a los antiguos Caquetíos y cita a Castellanos"},
    "ture":       {"sig": "asiento pequeño de madera",                    "cat": "sust",  "fuente": "caribe-cháima", "glosa_fuente": "Asiento pequeño de forma particular. Us. en Cumaná y Margarita. Es lo mismo que el butaque de Occidente. Voz cháima, que Tauste traduce: asiento pequeño de madera [Alvarado 1921 p.301 s.v. TURE]", "notas": "D10 (2026-08-03), grupo 1 — REASIGNADA A CARIBE CONTINENTAL Y GLOSA CORREGIDA. Alvarado 1921 p.301 la da como voz cháima (Tauste), usada en Cumaná y Margarita, y con la glosa de asiento, no de vasija. Doble error: lengua y referente. Lectura que se descarta: Zavala Reyes 2015 glosario #259 (AM) «Vasija, utensilio», fuerza F — queda registrada aquí por D7, no se pierde"},
    "wanepe": {"sig": "cesto para cargar niños",                       "cat": "sust",  "fuente": "caquetío-atestiguado", "glosa_fuente": "Así llaman en Barcelona y Guayana una especie de cabestrillo o charpa en que las madres indígenas llevan sus niños de pecho cuando viajan [Alvarado 1921 p.152 s.v. GUANEPE]", "notas": "D10 (2026-08-03), grupo 2 — LA GLOSA SE CONSERVA: Alvarado 1921 p.152 la CONFIRMA palabra por palabra, y Zavala Reyes 2015 glosario #137 (E) la respalda («Cesto para cargar a los niños», fuerza F). Lo que Alvarado desmiente no es el significado sino la GEOGRAFÍA: la localiza en Barcelona y Guayana, oriente caribe, no en Coro. La reserva es geográfica, no semántica, y por eso la entrada no cambia de etiqueta: queda anotada", "forma_fuente": "guanepe"},
    "na":         {"sig": "como, semejante a (partícula comparativa)",     "cat": "part",  "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015, glosario #184 (HP): «Partícula equivalente a como o semejante»"},

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
    "nagua":      {"es": "nagua, falda de algodón de mujer", "fuente": "caquetío-reconstruido", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): Medina Colina p. 193 s.v. naguas «con esta palabra, producto del pueblo llano, nuestros paraguaneros se refirieron a las enaguas de la mujer; es voz taína» → caquetío-reconstruido como kanoa/hamaca/konuko; etiqueta anterior `taíno` · Tno. nagua → español enagua; Lokono annaka", "categoria": "vestimenta"},
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
    "macana":     {"es": "macana, garrote de madera dura, arma de combate", "fuente": "caquetío-reconstruido", "notas": "Decisión de Miguel 2026-09-12: tainismo panhispánico que Medina Colina recoge en el habla paraguanera (s.v. macana, página no dictada) → `caquetío-reconstruido`, forma justificada por cognado en taíno, como kanoa/hamaca/konuko; NO atestiguada porque la vía pudo ser el español. Etimología: DRAE: macana, del taíno; panamericana; en Venezuela también. Etiqueta anterior: `taíno` · Tno. macana; arma arahuaca; análoga al poporo caquetío · Campaña 2026-09-21 (#184), decisión de Miguel → A («Si voy con tu recomendación»): la etiqueta SE QUEDA, y consta que el achagua NO la sostiene — Neira y Ribero 1762 da `Macana → Guacaba` (pliego 73 der.), y `Macanasi`/`Macanayi`/`Mamacanayisa` glosan «Dormidera», «Mazorca de mais» e «Yndecible». Cero fuentes la dan como caquetía (Zavala, van Buurt, Gatschet, Perea, Pané); Alvarado 1921 p. 189: «voz taína». Medina la recoge como 'algo muy grande o desproporcionado', no como garrote. La voz caquetía ATESTIGUADA para el arma es `poporo` (Alvarado 1921 p. 255: «usada por los antiguos Caquetíos», ref. Castellanos). Volverla a `taíno` (opción C) queda dentro de la decisión de clase sobre los tainismos", "categoria": "armas"},
    "cayo":       {"es": "cayo, islote bajo y arenoso, escollo costero", "fuente": "taíno", "notas": "Tno. cayo → español cayo; rasgos costeros del Golfete", "categoria": "geografia"},
    "manigua":    {"es": "manigua, matorral denso, monte bajo", "fuente": "taíno", "notas": "Tno. manigua; vegetación de transición sabana-bosque", "categoria": "geografia"},
    "bixa":       {"es": "bija, onoto, achiote (Bixa orellana), pigmento corporal rojo", "fuente": "taíno", "notas": "Tno. bixa/bija; pigmento ritual rojo; análogo al bariki caquetío", "categoria": "materiales"},
    "hayo":       {"es": "hayo, coca (Erythroxylum coca), hoja masticada ritual", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #156 (HB): 'hierba quita sed'; cf. #154 hay (E) = coca. Forma taína hayo documentada en Oviedo. RE-ETIQUETADO 2026-07-20: estaba como taíno pese a figurar en el glosario caquetío", "categoria": "ritual"},

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
        "es": "hígado", "fuente": "caquetío-reconstruido", "categoria": "cuerpo", "notas": "Decisión D9 (tanda 2026-08-30) — HOMÓNIMOS DECLARADOS: bana-1 cerro, sitio alto es caquetío-ATESTIGUADO (Zavala Reyes 2015 #26 «Bana (E): Sitio, cerro alto»; composición capu+bana = «duende del cerro» #61; el cerro de Santa Ana se llamaba Cerro de Capú). Esta entrada es bana-2 hígado, reconstruida por cognado lokono (Pet 1987: bana, bana-ha) — COGNADO VERIFICADO 2026-08-31 en la serie Swadesh de Oliver, fila 53 liver: lokono ebana, island-carib *bana, guajiro apa-na, y la serie panarahuaca *pana entera (nu-pana, nu-shupana, -upana, apakana...; ver 6-fusion/tabla_a1_a7_swadesh.yaml). El morfema toponímico -bana vive en morfologia.md y morfemas.yaml. Saneado de paso un bug latente: la entrada traía dos claves notas y la segunda pisaba a la primera", "notas": "⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'hígado'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md"},
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
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. abba; método comparativo arahuacano; Reconstrucción desde Lok. abba (uno); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "gramatica"
    },
    "acoa": {
        "es": "pie",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. akoa; método comparativo arahuacano; Reconstrucción desde Lok. akoa (pie); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "aduri": {
        "es": "nariz",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. aduri; método comparativo arahuacano; Reconstrucción desde Lok. aduri (nariz); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "agari": {
        "es": "cabeza",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. abari; método comparativo arahuacano; Reconstrucción desde Lok. abari (cabeza); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "akcicyaa": {
        "es": "espíritu vital",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. akkicyaha; método comparativo arahuacano; Reconstrucción desde Lok. akkicyaha (espíritu vital); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "ritual"
    },
    "cai": {
        "es": "isla",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: cai; cognado Lok. kairi; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "geografia"
    },
    "caiman": {
        "es": "caimán",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: caiman; cognado Lok. kaiman; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "fauna"
    },
    "casabe": {
        "es": "casabe",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: casabe; cognado Lok. kasabi; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "alimentos"
    },
    "cohiba": {
        "es": "tabaco",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: cohiba; cognado Lok. iuli; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "ritual"
    },
    "daca": {
        "es": "mano",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. daka; método comparativo arahuacano; Reconstrucción desde Lok. daka (mano); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "higuana": {
        "es": "iguana",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: higuana; cognado Lok. iwana; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "fauna"
    },
    "mayani": {
        "es": "no, negación",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: mayani; cognado Lok. ma; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "gramatica"
    },
    "taita": {
        "es": "padre",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: taita; cognado Lok. itti; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "parentesco"
    },
    "thigisi": {
        "es": "diente",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. thibisi; método comparativo arahuacano; Reconstrucción desde Lok. thibisi (diente); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "tuna": {
        "es": "agua, río",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: tuna; cognado Lok. tuna; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "geografia"
    },
    "wacusi": {
        "es": "ojo",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. wakusi; método comparativo arahuacano; Reconstrucción desde Lok. wakusi (ojo); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "cuerpo"
    },
    "wagulo": {
        "es": "tortuga",
        "fuente": "taíno-reconstruido",
        "notas": "Reconstrucción hipotética Taíno desde Lok. wabulo; método comparativo arahuacano; Reconstrucción desde Lok. wabulo (tortuga); método comparativo arahuaco; confianza: alta · F8 (2026-09-12): re-etiquetada de `taino` a `taíno-reconstruido` — forma generada por reconstruir_taino() desde el lokono, no atestiguada; no cuenta como dato taíno en cruces",
        "categoria": "fauna"
    },
    "yamosa": {
        "es": "dos",
        "fuente": "taíno",
        "notas": "Taíno atestiguado: yamosa; cognado Lok. biama; Brinton 1871 · F8 (2026-09-12): grafía de `fuente` unificada, `taino` → `taíno`",
        "categoria": "gramatica"
    },

    # --- Proto-arahuaco reconstruido (arahuaco_comparative.py) ---
    "hamaka": {
        "es": "hamaca, red colgante para dormir",
        "fuente": "caquetío-reconstruido",
        "forma_fuente": "hamaca",
        "notas": "Decisión colisiones D5 (2026-08-31) — FUSIONADA con hamaca (núcleo fundacional, forma justificada por cognado en taíno). Cognados: proto-arahuaco *hamaka, LK hamaha, TN hamaca (Payne 1991, Brinton 1871). Se queda RECONSTRUIDA (mismo motivo que kanoa: hamaca es préstamo taíno del propio español). OJO: amaka sitio-de-moler-maíz (Zavala #9, forma_fuente amaca) es palabra DISTINTA, y h→∅ sigue disputada en D5 — no se fusionan",
        "categoria": "utiles"
    },
    "isikoa": {
        "es": "casa, vivienda",
        "fuente": "proto-arahuaco",
        "notas": "Proto-arahuaco *isikoa; atestiguada en 2 lenguas: LK: sikoa, TN: bohio; Payne (1991), Brinton (1871)",
        "categoria": "utiles"
    },
    "kanoa": {
        "es": "canoa, embarcación excavada en tronco",
        "fuente": "caquetío-reconstruido",
        "forma_fuente": "canoa",
        "notas": "Decisión colisiones D5 (2026-08-31) — FUSIONADA con canoa (núcleo fundacional, forma justificada por cognado en taíno): grafía española del mismo lema. Cognados: proto-arahuaco *kanoa, LK kannoa, TN canoa (Payne 1991, Brinton 1871). Se queda RECONSTRUIDA: el CQ canoa de la serie comparativa no es atestación independiente — canoa es préstamo taíno del propio español, riesgo de circularidad",
        "categoria": "utiles"
    },
    "kati": {
        "es": "luna",
        "fuente": "caquetío-atestiguado",
        "forma_fuente": "cati",
        "notas": "Decisión colisiones D5 (2026-08-31) — FUSIONADA con cati: la grafía c es colonial y el lema fonémico es la palabra. Atestiguada: Zavala Reyes 2015, glosario #71 (CGB): «Luna [catire: persona de tez blanca]». Cognados: proto-arahuaco *kati, WY kachi, LK katsi (Payne 1991, Brinton 1871); en el Swadesh de Oliver (Tabla A-2, fila moon) el lokono trae kathi — similitud 1.00, la fila bandera del cómputo de D11. RE-ETIQUETADA de proto-arahuaco a caquetío-atestiguado por atestación directa (precedente de para, 2026-07-20)",
        "categoria": "cosmos"
    },
    "catire":     {"sig": "persona de tez blanca", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "persona de tez blanca [Zavala Reyes 2015 #71 (CGB)]", "notas": "COSECHADA 2026-09-10, a propuesta de Miguel. Estaba en la fuente y no en el lexicón: Zavala Reyes 2015, glosario #71 (CGB) dice «CATI: Luna [CATIRE: persona de tez blanca]», y el importador la dejó dentro de las notas de `kati` en vez de hacerla entrada. Barridos TODOS los corchetes del glosario, es el único lema sin cosechar. LECTURA DE MIGUEL: «es como decir hijo de la luna, para describir a los españoles por su tez blanca». La conexión con la luna la hace la propia fuente, y `kati` luna es caquetío-atestiguado. ⚠️ La parte de HIJO no se sostiene con lo atestiguado: exigiría `dare` = 'hijo', y la cita de `dare` solo da 'diente'. La lectura que SÍ se sostiene sin añadir nada es la metáfora directa — la luna es lo pálido, 'lunar' → 'de tez clara'. CAPA retro-abstraída y no atestiguada porque `catire` es además voz corriente del castellano venezolano: lo incierto no es la forma, es que el sustrato sea caquetío. Mismo caso que `chiriware` y `tukeke`. Detalle: 6-fusion/censo_terminacion_re.yaml §catire", "forma_fuente": "catire"},
    "para": {
        "es": "mar, agua extensa (dulce o salada en gran cantidad)",
        "fuente": "caquetío-atestiguado",
        "notas": "Zavala Reyes 2015 #190 (E+HP): 'Aguadulce o salada en grandes cantidades'; cf. #191 paragua (GC) = mar. Reflejo del proto-arahuaco *para, atestiguado en 4 lenguas: CQ para, WY palaa, LK bara, TN bagua; Payne (1991), Brinton (1871). RE-ETIQUETADO 2026-07-20: figuraba como proto-arahuaco pese a estar atestiguado directamente en caquetío — por eso _familia_de_token necesitaba un caso especial para contarlo como caquetío",
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
    "baruwa":   {"es": "hombre (registro masculino Kalinago)", "fuente": "kalinago", "notas": "F8 (2026-09-12): etiqueta vieja `kalinago-caribe-overlay`: forma del registro caribe (overlay) del kalinago · Breton (1665) registro masculino; origen caribe; contraparte de hiñaru (arahuaco); la dualidad baruwa/hiñaru es evidencia del proceso de contacto que generó el Kalinago", "categoria": "parentesco"},
    "kanawa-caribe": {"es": "canoa (forma caribe del Kalinago)", "fuente": "kalinago", "notas": "F8 (2026-09-12): etiqueta vieja `kalinago-caribe-overlay`: forma del registro caribe (overlay) del kalinago · Forma caribe que desplazó al arahuaco kanoa/kannoa en contexto náutico-masculino; ambas formas coexistieron en distintos registros del Kalinago según Breton (1665). Renombrada con sufijo -caribe para evitar colisión con la entrada lokono/garifuna 'kanawa' = amarillo (línea 152), homónimo casual entre lenguas distintas.", "categoria": "navegacion"},
    "pira":     {"es": "pez, pescado (forma caribe del Kalinago)", "fuente": "kalinago", "notas": "F8 (2026-09-12): etiqueta vieja `kalinago-caribe-overlay`: forma del registro caribe (overlay) del kalinago · Origen caribe; cf. piraña = pira + aña (diente en Tupí); el overlay caribe dominó el vocabulario de pesca en el registro masculino Kalinago; contrasta con el arahuaco LK itime", "categoria": "fauna"},
    "amourou":  {"es": "guerra, combate", "fuente": "kalinago", "notas": "F8 (2026-09-12): etiqueta vieja `kalinago-caribe-overlay`: forma del registro caribe (overlay) del kalinago · Breton (1665); vocabulario bélico casi exclusivamente caribe en Kalinago; ausencia del término arahuaco equivalente en registro masculino", "categoria": "guerra"},

    
    # ── JIRAJAROIDE — ZONA DE CONTACTO (toponimia atestiguada; Oramas 1916; Jahn 1927) ──
    # Nota: fuente "jirajaroide-contacto" = término registrado en zona fronteriza
    # caquetío-jirajaroide (Sierra de Coro, Falcón occidental, Lara norte).
    # Las entradas marcadas con [CQ-exónimo] son posiblemente nombres caquetíos
    # para grupos jirajaroide, no autónimos de los propios grupos.
    "xira":        {"es": "raíz del etnónimo Jirajara (probable: serranos, gente de la sierra)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Raíz de Xirahara/Jirajara; puede ser exónimo caquetío, no autónimo Jirajara; attested en variantes ortográficas coloniales Xirajara, Jirajara, Xiraxara [CQ-exónimo]", "categoria": "etnonimia"},
    "buria":       {"es": "valle aurífero en serranía (topónimo Jirajaroide)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Buria = valley en Yaracuy/Lara; zona de extracción aurífera prehispánica; posiblemente relacionado con término Jirajaroide para mineral/tierra amarilla; Relaciones Geográficas 1578", "categoria": "geografia"},
    "nirgua":      {"es": "asentamiento Jirajaroide en Yaracuy (topónimo)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Nirgua = municipio Yaracuy; territorio de frontera caquetío-jirajaroide; origen lingüístico no determinado con certeza entre Jirajara y Ayamán; Jahn 1927", "categoria": "geografia"},
    "churuguara":  {"es": "territorio Gayón en Falcón serrano (topónimo)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Churuguara = municipio Falcón; corazón del territorio Gayón; Gayones = rama Jirajaroide de Sierra de Coro y Falcón occidental, vecinos DIRECTOS de Curiana; Oramas 1916", "categoria": "geografia"},
    "ayaman":      {"es": "grupo Jirajaroide del Lara-Falcón (etnonimia/topónimo)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Ayamán = etnónimo y topónimo; municipio Lara; una de las cuatro ramas Jirajaroide conocidas (Jirajara, Ayamán, Gayón, Ajagua); Oramas 1916; Jahn 1927", "categoria": "etnonimia"},
    "ajagua":      {"es": "grupo Jirajaroide (Jirajaroid menor)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Ajagua = cuarto grupo de la familia Jirajaroide; menos documentado que los otros tres; territorio en zona de contacto Lara-Falcón; Oramas 1916", "categoria": "etnonimia"},
    "quibor":      {"es": "valle agrícola del Lara interior (topónimo)", "fuente": "jirajaroide", "notas": "F8 (2026-09-12): etiqueta vieja `jirajaroide-contacto`: voz de contacto con el área jirajaroide · Quibor = municipio Lara, valle fértil; zona de frontera caquetío-jirajaroide; origen lingüístico disputado; Alcalá 1954; topónimo clave en ruta de intercambio maíz-sal-conchas", "categoria": "geografia"},
    


    # ── Dictado de Medina Colina (Miguel, 2026-09) — nivel A ──
    # Las únicas dos voces del dictado que NO estaban ya en el
    # lexicón por su lema fonémico. Ver 6-fusion/medina_colina_dictado.yaml
    "karebe": {"sig": "cuchara, cucharón de media tapara con mango de madera", "cat": "sust", "fuente": "caquetío-atestiguado", "categoria": "casa", "notas": "DOS atestaciones independientes a los dos lados del Golfete y con 128 años entre ellas: Gatschet 1885 la recoge en ARUBA como «karebe spoon» (lista de voces arahuacas de la isla), y Medina Colina 2013 p. 64 la da viva en PARAGUANÁ — «una especie de cucharón que se hacía con media tapara, atravesada por sus bordes por un mango de madera; era utilizado para servir comida» (dictado de Miguel, 2026-09-01). Alvarado 1921 p. 62 describe el mismo objeto («de forma oval, a la que sirve de mango la parte más angosta del óvalo; fabrícala del fruto del totumo y úsala en Occidente») pero le atribuye origen andino (cf. guahibo kariepa) y dice que en Oriente se desconoce — RESERVA DECLARADA: la atestación insular es lo que la hace caquetía, no la etimología, que Alvarado disputa. El objeto es precontacto (la totuma como cucharón es pancaribeña)."},
    "urupagua": {"sig": "arbusto espinoso usado para cercar conucos; y árbol de la serranía coriana de fruto amargo comestible tras larga cocción", "cat": "sust", "fuente": "caquetío-atestiguado", "categoria": "flora", "notas": "TRES fuentes independientes y DOS topónimos. Alvarado 1921 p. 305 URUPÁGUA: «Árbol indeterminado de Coro. Fruto elipsoide, cuando seco, de 1½ pulgada de largo, con cáscara dura y un contenido libre, compacto, harinoso, amarillento» — que la ciencia no supiera darle taxón es señal de voz local no castellanizable. Esteves 1989 da los topónimos URUPAGUADUCO «la quebrada de las urupaguas» (p. 71) y Urupagua. Medina Colina 2013 p. 292 la da viva en Paraguaná y distingue las DOS clases: el arbusto espinoso de las cercas (Paraguaná) y el árbol de la sierra de fruto amargo, con refrán dentro — «tiene más coraje que el que se comió la primera urupagua» (dictado de Miguel, 2026-09-08). Distribución restringida a la Curiana. La etiqueta descansa en la vía toponímica: no hay atestación en boca caquetía, sí convergencia de tres testigos y el topónimo. Deuda: procesar Urupagua y Urupaguaduco en la campaña de topónimos con esta voz como lectura."},

    # Las dos que el filtro automatico salto por tener glosa de UNA letra:
    # no eran ilegibles, son PALABRAS GRAMATICALES — y el lexicon anda
    # pobre justo de eso. Revisadas y entradas a mano.
    "baddia": {"sig": "y (conjuncion copulativa); tambien, asimismo, aun", "cat": "part", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I. Raiz `baddia` con 8 atestaciones; acepcion principal 'y' (p. 538, 4 atestaciones). Otras: aun (p.498); asimismo (p.498); tambien (p.537). NOTA DE METODO: el fusionador automatico de la fase 1 de D11 la salto porque su glosa tiene UNA letra y el filtro exigia dos; no era ilegible, es una conjuncion. Entrada a mano el 2026-09-11."},
    "mun-lokono": {"sig": "a, para, en (relacional)", "cat": "part", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I. Raiz `mun` (Perea escribe `mun` con acento grave) con 8 atestaciones; acepciones: a (3 atestaciones, sin pagina en la fuente); para (p.527, 3); en (p.511, 1); haber (p.339, 1). Clave desambiguada con sufijo de lengua por el acento de la forma original. NOTA DE METODO: saltada por el mismo filtro de una letra; es una preposicion. Entrada a mano el 2026-09-11."},
    # ══════════════════════════════════════════════════════
    # D11 FASE 1 (2026-09-11) — las raíces lokono de Perea 1942.
    # Comparanda, NO caquetío: rebalancea el eje que D11 decidió.
    # ══════════════════════════════════════════════════════
    "abba-waria": {"sig": "extranjero", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `abba-waria` con 4 atestaciones; acepción principal «extranjero» (p. 44, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "abbu": {"sig": "por (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `abbu` con 10 atestaciones; acepción principal «por» (p. 528, 6 atestaciones). Otras acepciones: con (p.501). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "abbu-coa": {"sig": "juntar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `abbu-coa` con 4 atestaciones; acepción principal «juntar» (p. 364, 2 atestaciones). Otras acepciones: unánime (p.130). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "abbu-mùn": {"sig": "debajo (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `abbu-mùn` con 3 atestaciones; acepción principal «debajo» (p. 507, 2 atestaciones). Otras acepciones: bajo (p.499). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "adi": {"sig": "sobre (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `adi` con 10 atestaciones; acepción principal «sobre» (p. 536, 8 atestaciones). Otras acepciones: delante (p.507); sobrepujar (p.463). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "adi-acu": {"sig": "encima", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `adi-acu` con 4 atestaciones; acepción principal «encima» (p. 513, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "awa-lokono": {"sig": "mismo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `awa` con 2 atestaciones; acepción principal «mismo» (p. 118, 2 atestaciones). ⚠️ HOMÓGRAFO: la clave `awa` ya existía en el lexicón como caquetío-reconstruido «beber, tomar líquido», así que esta entra desambiguada como `awa-lokono` y NO la pisa — el precedente es `kati-kalinago`. `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "baha": {"sig": "caso (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `baha` con 10 atestaciones; acepción principal «caso» (p. 491, 9 atestaciones). Otras acepciones: quizás (p.533). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "balla": {"sig": "crucificar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `balla` con 2 atestaciones; acepción principal «crucificar» (p. 276, 1 atestaciones). Otras acepciones: sonda (p.92). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "balti": {"sig": "sentarse", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `balti` con 2 atestaciones; acepción principal «sentarse» (p. 454, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bara-lokono": {"sig": "mar", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bara` con 6 atestaciones; acepción principal «mar» (p. 65, 6 atestaciones). ⚠️ HOMÓGRAFO: la clave `bara` ya existía en el lexicón como caquetío-atestiguado «palo, árbol», así que esta entra desambiguada como `bara-lokono` y NO la pisa — el precedente es `kati-kalinago`. `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bbuku": {"sig": "recibir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bbuku` con 2 atestaciones; acepción principal «recibir» (p. 432, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bbuna": {"sig": "paralítico", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bbuna` con 2 atestaciones; acepción principal «paralítico» (p. 77, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bele": {"sig": "cojo (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bele` con 2 atestaciones; acepción principal «cojo» (p. 23, 1 atestaciones). Otras acepciones: fervor (p.45). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "benna": {"sig": "cuando", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `benna` con 5 atestaciones; acepción principal «cuando» (p. 504, 5 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bia": {"sig": "in (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bia` con 2 atestaciones; acepción principal «in» (p. 515, 1 atestaciones). Otras acepciones: que (p.533). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "biama-cutti-hi": {"sig": "doce", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `biama-cutti-hi` con 4 atestaciones; acepción principal «doce» (p. 112, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "boa": {"sig": "crimen, delito (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `boa` con 7 atestaciones; acepción principal «crimen, delito» (p. 26, 2 atestaciones). Otras acepciones: invocar (p.361); malo (p.117); mal (p.519). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "boa-hù-dda": {"sig": "asolar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `boa-hù-dda` con 2 atestaciones; acepción principal «asolar» (p. 244, 1 atestaciones). Otras acepciones: ruina (p.88). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bulita": {"sig": "scribir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bulita` con 2 atestaciones; acepción principal «scribir» (p. 321, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bulle": {"sig": "echar (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bulle` con 4 atestaciones; acepción principal «echar» (p. 306, 2 atestaciones). Otras acepciones: alijar (p.231); aliviar (p.232). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bura": {"sig": "padre (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bura` con 6 atestaciones; acepción principal «padre» (p. 123, 5 atestaciones). Otras acepciones: patria (p.78). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "bura-mùn": {"sig": "antes", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `bura-mùn` con 2 atestaciones; acepción principal «antes» (p. 496, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cani": {"sig": "partir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cani` con 2 atestaciones; acepción principal «partir» (p. None, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "canna": {"sig": "oír", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `canna` con 3 atestaciones; acepción principal «oír» (p. 399, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "catti": {"sig": "mes (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `catti` con 4 atestaciones; acepción principal «mes» (p. 66, 3 atestaciones). Otras acepciones: luna (p.60). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ccabbu": {"sig": "mano", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ccabbu` con 5 atestaciones; acepción principal «mano» (p. 63, 5 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cubu-ruccu": {"sig": "ánimo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cubu-ruccu` con 2 atestaciones; acepción principal «ánimo» (p. 10, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cubu-ruccu-a-monnua": {"sig": "permitir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cubu-ruccu-a-monnua` con 2 atestaciones; acepción principal «permitir» (p. 414, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cudu-cutta": {"sig": "llevar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cudu-cutta` con 2 atestaciones; acepción principal «llevar» (p. 378, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cui-kitta": {"sig": "arrepentirse", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cui-kitta` con 3 atestaciones; acepción principal «arrepentirse» (p. 241, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cullu-siba-ttoa": {"sig": "rodilla", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cullu-siba-ttoa` con 3 atestaciones; acepción principal «rodilla» (p. 88, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cumu": {"sig": "no (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cumu` con 4 atestaciones; acepción principal «no» (p. 524, 3 atestaciones). Otras acepciones: sin (p.535). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cun": {"sig": "nacer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cun` con 3 atestaciones; acepción principal «nacer» (p. 393, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cun-du": {"sig": "desierto", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cun-du` con 2 atestaciones; acepción principal «desierto» (p. 28, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cun-te": {"sig": "ir", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cun-te` con 4 atestaciones; acepción principal «ir» (p. 362, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cuttu": {"sig": "ayunar (y 3 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cuttu` con 8 atestaciones; acepción principal «ayunar» (p. 247, 4 atestaciones). Otras acepciones: comer (p.258); gustar (p.339); menester (p.386). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cuya": {"sig": "rogar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cuya` con 5 atestaciones; acepción principal «rogar» (p. 442, 3 atestaciones). Otras acepciones: demandar (p.294). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cuya-bua": {"sig": "orar (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cuya-bua` con 5 atestaciones; acepción principal «orar» (p. 404, 3 atestaciones). Otras acepciones: adorar (p.227). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "cuyoa": {"sig": "volver", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `cuyoa` con 3 atestaciones; acepción principal «volver» (p. 486, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "daiya": {"sig": "señor", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `daiya` con 4 atestaciones; acepción principal «señor» (p. 90, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dannu": {"sig": "hoy", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dannu` con 4 atestaciones; acepción principal «hoy» (p. 517, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ddiki": {"sig": "ver (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ddiki` con 7 atestaciones; acepción principal «ver» (p. 479, 4 atestaciones). Otras acepciones: mirar (p.389); postrero, último (p.124). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dia": {"sig": "decir (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dia` con 28 atestaciones; acepción principal «decir» (p. 280, 9 atestaciones). Otras acepciones: palabra (p.75); lengua, idioma (p.57); voz (p.104); conferir (p.262). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dikki": {"sig": "sembrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dikki` con 2 atestaciones; acepción principal «sembrar» (p. 454, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dina": {"sig": "ante (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dina` con 2 atestaciones; acepción principal «ante» (p. 495, 1 atestaciones). Otras acepciones: poner (p.418). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dinamu-kitta": {"sig": "presentar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dinamu-kitta` con 2 atestaciones; acepción principal «presentar» (p. 425, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "disia": {"sig": "acostumbrar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `disia` con 3 atestaciones; acepción principal «acostumbrar» (p. 225, 2 atestaciones). Otras acepciones: soler (p.464). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ditti": {"sig": "hijo (y 4 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ditti` con 16 atestaciones; acepción principal «hijo» (p. 51, 10 atestaciones). Otras acepciones: entender (p.313); afirmar (p.227); concernir (p.260); conocer (p.265). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ditti-kitta": {"sig": "convencer (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ditti-kitta` con 2 atestaciones; acepción principal «convencer» (p. 270, 1 atestaciones). Otras acepciones: suerte (p.92). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "dumma": {"sig": "porque (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `dumma` con 17 atestaciones; acepción principal «porque» (p. 531, 12 atestaciones). Otras acepciones: causar (p.253); fe (p.45); modo (p.322). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ehé": {"sig": "sí", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ehé` con 2 atestaciones; acepción principal «sí» (p. 534, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "emelia": {"sig": "nuevo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `emelia` con 2 atestaciones; acepción principal «nuevo» (p. 121, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "haca": {"sig": "testificar (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `haca` con 22 atestaciones; acepción principal «testificar» (p. 468, 6 atestaciones). Otras acepciones: hablar (p.342); anunciar (p.234); despedazar (p.300); disputar (p.303). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "hada-cuttu": {"sig": "informar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `hada-cuttu` con 3 atestaciones; acepción principal «informar» (p. 359, 2 atestaciones). Otras acepciones: inquirir (p.360). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "halli": {"sig": "cuanto (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `halli` con 2 atestaciones; acepción principal «cuanto» (p. 505, 1 atestaciones). Otras acepciones: término (p.94). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "halli-kebbe": {"sig": "gozar (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `halli-kebbe` con 7 atestaciones; acepción principal «gozar» (p. 336, 3 atestaciones). Otras acepciones: alegrar (p.231); confiar (p.262); consentir (p.266); dichoso (p.112). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "hamma": {"sig": "por qué ? (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `hamma` con 8 atestaciones; acepción principal «por qué ?» (p. 530, 7 atestaciones). Otras acepciones: temer (p.466). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "hamma-talli": {"sig": "cosa", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `hamma-talli` con 4 atestaciones; acepción principal «cosa» (p. 25, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "hidda": {"sig": "así (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `hidda` con 11 atestaciones; acepción principal «así» (p. 497, 9 atestaciones). Otras acepciones: tal (p.128). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "hitte": {"sig": "más (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `hitte` con 7 atestaciones; acepción principal «más» (p. 520, 4 atestaciones). Otras acepciones: mucho (p.322); erseverar (p.415). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "huda": {"sig": "morir (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `huda` con 11 atestaciones; acepción principal «morir» (p. 390, 7 atestaciones). Otras acepciones: resucitar (p.440); espirar (p.325). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "huki": {"sig": "hermano", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `huki` con 3 atestaciones; acepción principal «hermano» (p. 49, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "huyuru": {"sig": "provincia", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `huyuru` con 2 atestaciones; acepción principal «provincia» (p. 83, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ibe": {"sig": "llenar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ibe` con 2 atestaciones; acepción principal «llenar» (p. 378, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ibikiddu-lli-a": {"sig": "mancebo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ibikiddu-lli-a` con 6 atestaciones; acepción principal «mancebo» (p. 63, 6 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ibiti": {"sig": "cerca", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ibiti` con 3 atestaciones; acepción principal «cerca» (p. 500, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "icca": {"sig": "entonces (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `icca` con 3 atestaciones; acepción principal «entonces» (p. 513, 2 atestaciones). Otras acepciones: pero (p.528). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ikira": {"sig": "cercar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ikira` con 2 atestaciones; acepción principal «cercar» (p. 255, 1 atestaciones). Otras acepciones: lágrima (p.56). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ikisi": {"sig": "escoger (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ikisi` con 7 atestaciones; acepción principal «escoger» (p. 321, 3 atestaciones). Otras acepciones: acordar (p.224); contar, enumerar (p.269); determinar (p.301); prometer (p.428). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ikitta": {"sig": "guardar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ikitta` con 3 atestaciones; acepción principal «guardar» (p. 337, 2 atestaciones). Otras acepciones: honrar (p.356). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ima": {"sig": "enemigo (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ima` con 3 atestaciones; acepción principal «enemigo» (p. 39, 2 atestaciones). Otras acepciones: resentir (p.437). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ime": {"sig": "enviar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ime` con 2 atestaciones; acepción principal «enviar» (p. 318, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ipil": {"sig": "príncipe ; [ cf. n : pilli ] (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ipil` con 5 atestaciones; acepción principal «príncipe ; [ cf. n : pilli ]» (p. 82, 4 atestaciones). Otras acepciones: pontífice (p.81). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ipilli": {"sig": "sumo (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ipilli` con 4 atestaciones; acepción principal «sumo» (p. 128, 2 atestaciones). Otras acepciones: alto (p.None); prepósito (p.81). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "irei": {"sig": "mujer, esposa", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `irei` con 4 atestaciones; acepción principal «mujer, esposa» (p. 69, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iri": {"sig": "nombrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iri` con 14 atestaciones; acepción principal «nombrar» (p. 395, 14 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iribe": {"sig": "común (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iribe` con 2 atestaciones; acepción principal «común» (p. 110, 1 atestaciones). Otras acepciones: violar (p.484). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iribé": {"sig": "inmundo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iribé` con 3 atestaciones; acepción principal «inmundo» (p. 117, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "isibu": {"sig": "puerta (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `isibu` con 7 atestaciones; acepción principal «puerta» (p. 85, 3 atestaciones). Otras acepciones: cara, faz, rostro (p.17); rostro (p.88). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iya": {"sig": "espíritu (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iya` con 3 atestaciones; acepción principal «espíritu» (p. 40, 2 atestaciones). Otras acepciones: compungirse (p.260). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyaca-ttoa": {"sig": "encubrir (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyaca-ttoa` con 2 atestaciones; acepción principal «encubrir» (p. 309, 1 atestaciones). Otras acepciones: rincón (p.87). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyaha-dda": {"sig": "conversar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyaha-dda` con 2 atestaciones; acepción principal «conversar» (p. 270, 1 atestaciones). Otras acepciones: pasar (p.410). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyaon": {"sig": "uzgar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyaon` con 2 atestaciones; acepción principal «uzgar» (p. 367, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyucana": {"sig": "vender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyucana` con 3 atestaciones; acepción principal «vender» (p. 474, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyuhu": {"sig": "multitud (y 4 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyuhu` con 16 atestaciones; acepción principal «multitud» (p. 69, 8 atestaciones). Otras acepciones: gente (p.47); número (p.72); conjurar (p.264); aumentar (p.246). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyula": {"sig": "afrentar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyula` con 2 atestaciones; acepción principal «afrentar» (p. 228, 1 atestaciones). Otras acepciones: castigar (p.253). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyumu": {"sig": "persuadir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyumu` con 2 atestaciones; acepción principal «persuadir» (p. 416, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "iyuru": {"sig": "traer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `iyuru` con 3 atestaciones; acepción principal «traer» (p. 471, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "kia": {"sig": "después", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `kia` con 4 atestaciones; acepción principal «después» (p. 508, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "kia-hann": {"sig": "pues", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `kia-hann` con 2 atestaciones; acepción principal «pues» (p. 532, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "kia-hanna": {"sig": "así", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `kia-hanna` con 3 atestaciones; acepción principal «así» (p. 498, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "kkürkùa": {"sig": "linaje (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `kkürkùa` con 5 atestaciones; acepción principal «linaje» (p. 59, 2 atestaciones). Otras acepciones: nación, pueblo, familia (p.70); simiente (p.16); tribu (p.98). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "kusa": {"sig": "ni (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `kusa` con 4 atestaciones; acepción principal «ni» (p. 523, 2 atestaciones). Otras acepciones: o (p.526). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "lesi": {"sig": "leer", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `lesi` con 4 atestaciones; acepción principal «leer» (p. 369, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "lle-ruccu": {"sig": "boca", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `lle-ruccu` con 2 atestaciones; acepción principal «boca» (p. 13, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "llua": {"sig": "corazón (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `llua` con 11 atestaciones; acepción principal «corazón» (p. 23, 9 atestaciones). Otras acepciones: alma; espíritu, ánimo, corazón (p.8). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "lluccu-waria": {"sig": "sacar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `lluccu-waria` con 2 atestaciones; acepción principal «sacar» (p. 446, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "maiyana-ttoa": {"sig": "notorio (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `maiyana-ttoa` con 3 atestaciones; acepción principal «notorio» (p. 120, 2 atestaciones). Otras acepciones: eferir (p.435). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "makua": {"sig": "todo (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `makua` con 22 atestaciones; acepción principal «todo» (p. 215, 16 atestaciones). Otras acepciones: cada uno (p.211); público (p.125); cualquiera (p.218). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "malli": {"sig": "encender (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `malli` con 3 atestaciones; acepción principal «encender» (p. 308, 1 atestaciones). Otras acepciones: imposible (p.116); osar (p.406). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "malli-cutta": {"sig": "enseñar (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `malli-cutta` con 7 atestaciones; acepción principal «enseñar» (p. 311, 4 atestaciones). Otras acepciones: doctrina (p.38); instruír (p.360). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "malli-t-a-coa": {"sig": "ídolo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `malli-t-a-coa` con 2 atestaciones; acepción principal «ídolo» (p. 54, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "manswa": {"sig": "maravilla (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `manswa` con 6 atestaciones; acepción principal «maravilla» (p. 66, 2 atestaciones). Otras acepciones: milagro (p.67); grande (p.114); prodigio (p.83). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "mehli": {"sig": "pan", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `mehli` con 2 atestaciones; acepción principal «pan» (p. 77, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "mei-cuxu": {"sig": "eunuco", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `mei-cuxu` con 2 atestaciones; acepción principal «eunuco» (p. 43, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "meyu": {"sig": "navegar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `meyu` con 4 atestaciones; acepción principal «navegar» (p. 394, 3 atestaciones). Otras acepciones: barco, buque, nave, navío (p.12). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "mmayu-n-ni-hùa": {"sig": "librar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `mmayu-n-ni-hùa` con 2 atestaciones; acepción principal «librar» (p. 272, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "muda": {"sig": "orar (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `muda` con 2 atestaciones; acepción principal «orar» (p. 389, 1 atestaciones). Otras acepciones: subir (p.465). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "mulli": {"sig": "aparentar (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `mulli` con 3 atestaciones; acepción principal «aparentar» (p. 237, 1 atestaciones). Otras acepciones: mentir (p.387); usar (p.474). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "muniru": {"sig": "hasta", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `muniru` con 7 atestaciones; acepción principal «hasta» (p. 516, 7 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "mùn-hitti": {"sig": "limosna", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `mùn-hitti` con 2 atestaciones; acepción principal «limosna» (p. 59, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "nda": {"sig": "sobrevenir (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `nda` con 3 atestaciones; acepción principal «sobrevenir» (p. 464, 2 atestaciones). Otras acepciones: descender, bajar (p.297). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "nnebe-ttoa": {"sig": "esparcir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `nnebe-ttoa` con 2 atestaciones; acepción principal «esparcir» (p. 324, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "nsi": {"sig": "discipulo (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `nsi` con 6 atestaciones; acepción principal «discipulo» (p. 36, 3 atestaciones). Otras acepciones: amar (p.232); amigo (p.8); voluntad (p.102). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "oaya": {"sig": "ahogar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `oaya` con 2 atestaciones; acepción principal «ahogar» (p. 229, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "onaica": {"sig": "tribulación", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `onaica` con 3 atestaciones; acepción principal «tribulación» (p. 98, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "onna": {"sig": "responder (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `onna` con 4 atestaciones; acepción principal «responder» (p. 438, 2 atestaciones). Otras acepciones: tomar (p.470). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "pahia": {"sig": "atónito (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `pahia` con 4 atestaciones; acepción principal «atónito» (p. 108, 2 atestaciones). Otras acepciones: atontar (p.245); entontecerse (p.315). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "platta": {"sig": "dinero (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `platta` con 2 atestaciones; acepción principal «dinero» (p. 32, 1 atestaciones). Otras acepciones: plata, dinero (p.80). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "pucu": {"sig": "diferencia (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `pucu` con 2 atestaciones; acepción principal «diferencia» (p. 32, 1 atestaciones). Otras acepciones: separar (p.455). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "putti": {"sig": "salir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `putti` con 6 atestaciones; acepción principal «salir» (p. 448, 6 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "raiya-ttoa": {"sig": "aparecer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `raiya-ttoa` con 2 atestaciones; acepción principal «aparecer» (p. 236, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "rubu-ùn": {"sig": "sólo, solamente (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `rubu-ùn` con 6 atestaciones; acepción principal «sólo, solamente» (p. 536, 4 atestaciones). Otras acepciones: sino (p.535). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "rule": {"sig": "luz", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `rule` con 2 atestaciones; acepción principal «luz» (p. 61, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sa-kebe": {"sig": "santo", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sa-kebe` con 4 atestaciones; acepción principal «santo» (p. 126, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sa-maria": {"sig": "derecha", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sa-maria` con 3 atestaciones; acepción principal «derecha» (p. 28, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sacca-bbu": {"sig": "día (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sacca-bbu` con 6 atestaciones; acepción principal «día» (p. None, 3 atestaciones). Otras acepciones: tiempo (p.94). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "saturdaca": {"sig": "sábado", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `saturdaca` con 2 atestaciones; acepción principal «sábado» (p. 82, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "seme": {"sig": "mágico, mago (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `seme` con 4 atestaciones; acepción principal «mágico, mago» (p. 62, 2 atestaciones). Otras acepciones: exorcizar (p.332); mosto (p.67). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sica": {"sig": "servir (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sica` con 16 atestaciones; acepción principal «servir» (p. 462, 4 atestaciones). Otras acepciones: obedecer (p.398); pecar (p.411); piadoso, pío (p.123); asentir (p.243). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sica-n-doa": {"sig": "rebelarse (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sica-n-doa` con 2 atestaciones; acepción principal «rebelarse» (p. 432, 1 atestaciones). Otras acepciones: rebelde (p.86). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sica-ni-coa": {"sig": "incredulo (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sica-ni-coa` con 2 atestaciones; acepción principal «incredulo» (p. 55, 1 atestaciones). Otras acepciones: incredulo : (p.116). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "siki": {"sig": "dar (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `siki` con 5 atestaciones; acepción principal «dar» (p. 278, 2 atestaciones). Otras acepciones: entregar (p.317); exponer (p.332). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sikua": {"sig": "casa", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sikua` con 8 atestaciones; acepción principal «casa» (p. 19, 8 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sima-lokono": {"sig": "alaridos (dar (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sima` con 2 atestaciones; acepción principal «alaridos (dar» (p. 230, 1 atestaciones). Otras acepciones: clamar (p.256). ⚠️ HOMÓGRAFO: la clave `sima` ya existía en el lexicón como caquetío-reconstruido «cerro, montaña, elevación», así que esta entra desambiguada como `sima-lokono` y NO la pisa — el precedente es `kati-kalinago`. `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sima-sima": {"sig": "gritar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sima-sima` con 2 atestaciones; acepción principal «gritar» (p. 336, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "statuta": {"sig": "ley (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `statuta` con 4 atestaciones; acepción principal «ley» (p. 58, 2 atestaciones). Otras acepciones: decretar (p.292); ordenar (p.406). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sucusa": {"sig": "bautizar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sucusa` con 4 atestaciones; acepción principal «bautizar» (p. 248, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "sura": {"sig": "sala (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `sura` con 3 atestaciones; acepción principal «sala» (p. 82, 2 atestaciones). Otras acepciones: azotea (p.12). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tatta": {"sig": "mandar (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tatta` con 13 atestaciones; acepción principal «mandar» (p. 381, 2 atestaciones). Otras acepciones: virtud, fuerza, poder (p.102); voto, promesa (p.104); afirmar (p.228); amenazar (p.232). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttene-nnua": {"sig": "primero (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttene-nnua` con 3 atestaciones; acepción principal «primero» (p. 124, 2 atestaciones). Otras acepciones: vez (p.102). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttenna": {"sig": "sangre", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttenna` con 2 atestaciones; acepción principal «sangre» (p. 82, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tti": {"sig": "que (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tti` con 5 atestaciones; acepción principal «que» (p. 199, 4 atestaciones). Otras acepciones: beber (p.250). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttica-ha": {"sig": "dañar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttica-ha` con 2 atestaciones; acepción principal «dañar» (p. 277, 1 atestaciones). Otras acepciones: escapar (p.321). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttiki": {"sig": "concitar (y 2 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttiki` con 3 atestaciones; acepción principal «concitar» (p. 260, 1 atestaciones). Otras acepciones: incitar (p.359); sobornar (p.463). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttu": {"sig": "cual (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttu` con 2 atestaciones; acepción principal «cual» (p. 205, 1 atestaciones). Otras acepciones: hija (p.51). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tturku": {"sig": "desechar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tturku` con 2 atestaciones; acepción principal «desechar» (p. 299, 1 atestaciones). Otras acepciones: rempujar (p.436). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ttùdda": {"sig": "huir", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ttùdda` con 3 atestaciones; acepción principal «huir» (p. 357, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tuhu": {"sig": "aquel, aquella, aquello, aquellos, aquellas (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tuhu` con 5 atestaciones; acepción principal «aquel, aquella, aquello, aquellos, aquellas» (p. 197, 2 atestaciones). Otras acepciones: ello, lo (p.187); éste , ésta, esto, éstos, éstas (p.148). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tullu-du": {"sig": "abrir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tullu-du` con 2 atestaciones; acepción principal «abrir» (p. 220, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "tuyucu": {"sig": "anciano", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `tuyucu` con 4 atestaciones; acepción principal «anciano» (p. 9, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "uma": {"sig": "con (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `uma` con 15 atestaciones; acepción principal «con» (p. 502, 13 atestaciones). Otras acepciones: acompañar (p.222). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "uria-lokono": {"sig": "de (y 3 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `uria` con 12 atestaciones; acepción principal «de» (p. 505, 5 atestaciones). Otras acepciones: apartar (p.238); 'uera (p.515); entre (p.514). ⚠️ HOMÓGRAFO: la clave `uria` ya existía en el lexicón como caquetío-atestiguado «plantío, siembra», así que esta entra desambiguada como `uria-lokono` y NO la pisa — el precedente es `kati-kalinago`. `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "usa": {"sig": "arremeter (y 4 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `usa` con 5 atestaciones; acepción principal «arremeter» (p. 241, 1 atestaciones). Otras acepciones: austro (p.12); comenzar (p.257); completar (p.259); tentar, probar (p.468). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "uttiki": {"sig": "hallar (y 1 acepción/es más)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `uttiki` con 4 atestaciones; acepción principal «hallar» (p. 352, 3 atestaciones). Otras acepciones: evitar (p.331). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wabu-ruccu": {"sig": "camino", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wabu-ruccu` con 7 atestaciones; acepción principal «camino» (p. 16, 7 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wacaiya": {"sig": "maldecir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wacaiya` con 2 atestaciones; acepción principal «maldecir» (p. 380, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wadu-lli": {"sig": "viento", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wadu-lli` con 2 atestaciones; acepción principal «viento» (p. 102, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "waria": {"sig": "desde", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `waria` con 6 atestaciones; acepción principal «desde» (p. 508, 6 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wiyua": {"sig": "año", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wiyua` con 5 atestaciones; acepción principal «año» (p. 10, 5 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wunabu": {"sig": "tierra, ( la, el mundo : (y 2 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wunabu` con 7 atestaciones; acepción principal «tierra, ( la, el mundo :» (p. 95, 4 atestaciones). Otras acepciones: mundo, tierra, siglo, humanidad (p.70); tierra, suelo (p.96). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wurebu": {"sig": "fornicar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wurebu` con 2 atestaciones; acepción principal «fornicar» (p. 333, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "wùseica-da-hitti": {"sig": "paz", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `wùseica-da-hitti` con 2 atestaciones; acepción principal «paz» (p. 78, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ya-luccu": {"sig": "contra", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ya-luccu` con 8 atestaciones; acepción principal «contra» (p. 503, 8 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "yaha": {"sig": "aquí", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `yaha` con 2 atestaciones; acepción principal «aquí» (p. 496, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "yu-mùn": {"sig": "allí", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `yu-mùn` con 4 atestaciones; acepción principal «allí» (p. 493, 4 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "yuhu": {"sig": "generación (y 1 acepción/es más)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `yuhu` con 2 atestaciones; acepción principal «generación» (p. 47, 1 atestaciones). Otras acepciones: pariente : (p.77). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ñaden": {"sig": "gracia", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ñaden` con 3 atestaciones; acepción principal «gracia» (p. 48, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ùsanu-wa-i": {"sig": "alabar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ùsanu-wa-i` con 2 atestaciones; acepción principal «alabar» (p. 229, 2 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},
    "ùsanu-wai": {"sig": "glorificar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I — lokono de 1802 (Schultz), anterior al de Brett 1849 y al de Goeje. Raíz `ùsanu-wai` con 3 atestaciones; acepción principal «glorificar» (p. 335, 3 atestaciones). `cat` INFERIDA de la glosa castellana (infinitivo → v_raiz, resto → sust): la fuente no da categoría gramatical. Fusión fase 1 de D11, 2026-09-11."},

    # ══════════════════════════════════════════════════════
    # D11 FASE 1b (2026-09-12) — el vocabulario verbal de Schumann
    # (ms. 1755) vía Perea 1942, pp. 609-684. Comparanda lokono.
    # ══════════════════════════════════════════════════════
    "iyaha-ddi": {"sig": "andar, caminar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 609. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyaha-ddi-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "a-ù": {"sig": "llorar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ù-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "buli-di": {"sig": "escribir, pintar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-buli-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "idi": {"sig": "ceñir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-idi-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "calleme-tti": {"sig": "encender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-calleme-tti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "m-a-monaica-di": {"sig": "enriquecer (lit. hacer no-pobre: m- privativo sobre a-monaica «pobre»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-m-a-monaica-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "úyi": {"sig": "arrancar, coger", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-úyi-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "iyaon-tti": {"sig": "comprar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyaon-tti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "budi-di": {"sig": "pescar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-budi-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "dumki": {"sig": "dormir, pernoctar, alojarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dumki-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ùki-tti": {"sig": "andar en vehículo", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùki-tti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "man-ti": {"sig": "afilar, aguzar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-man-ti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "puttùki-di": {"sig": "apartarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-puttùki-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "púsi-ti": {"sig": "libertar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-púsi-ti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "diriki": {"sig": "afeitar, aderezar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-diriki-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "uki": {"sig": "montar en vehículo", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-uki-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "cui-di": {"sig": "escupir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cui-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ndi": {"sig": "venir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ndi-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "nniki-di": {"sig": "elevar, alzar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-nniki-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "rdi": {"sig": "morder", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-rdi-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "bule-di": {"sig": "tirar, echar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bule-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "bule-he-di": {"sig": "arrojar, tirar, echar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bule-he-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "yali-di": {"sig": "envenenar con tóxico vegetal", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-yali-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ibitti": {"sig": "quemar, encender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ibitti-n`, conjugación 1-in. Cf. del Fraseario: `ibiti` «cerca» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "llihù-ti": {"sig": "ungir, untar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-llihù-ti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ndi-kitti": {"sig": "hacer venir (causativo de a-ndi-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ndi-kitti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "cohùn-ti": {"sig": "plantar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cohùn-ti-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ri-di": {"sig": "nombrar, apellidar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 614. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ri-di-n`, conjugación 1-in. Fusión fase 1b de D11, 2026-09-12."},
    "ttuba-ddù": {"sig": "zambullir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 615. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ttuba-ddù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "dina-mùn": {"sig": "estar presente", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dina-mùn`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "bacubù": {"sig": "respirar, reposar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bacubù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "canabù": {"sig": "oír", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-canabù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "iyaha-dù": {"sig": "asar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyaha-dù-n`, conjugación 1-ùn. Marcas de la fuente o del OCR: sic. Fusión fase 1b de D11, 2026-09-12."},
    "ccu-dù": {"sig": "arrojar, echar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ccu-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "dalli-dù": {"sig": "saltar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dalli-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "paù": {"sig": "matar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-paù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "cakù-dù": {"sig": "avivar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cakù-dù-n`, conjugación 1-ùn. Marcas de la fuente o del OCR: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "hurke-dù": {"sig": "juntarse, reunirse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-hurke-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "burùkù-dù": {"sig": "golpear, herir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-burùkù-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "ùsa-dù": {"sig": "hacer bien", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùsa-dù-n`, conjugación 1-ùn. Marcas de la fuente o del OCR: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "iyaca-ttù": {"sig": "esconder, ocultar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyaca-ttù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "cai-dù": {"sig": "romper, quebrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 618. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cai-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "bbunnù": {"sig": "plantar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bbunnù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "ccarku-dù": {"sig": "tejer, trenzar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ccarku-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "patta-dù": {"sig": "abofetear", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-patta-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "húla-dù": {"sig": "taladrar, agujerear", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-húla-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "para-dù": {"sig": "cortar madera", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-para-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "cartù": {"sig": "enterrar, sepultar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cartù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "ttù-dù": {"sig": "huir, escaparse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ttù-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "yara-dù": {"sig": "dar zarpazos", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-yara-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "kkùù": {"sig": "atar, ligar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-kkùù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "kùn-dù": {"sig": "lucir, orillar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-kùn-dù-n`, conjugación 1-ùn. Marcas de la fuente o del OCR: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "tia-dù": {"sig": "pasar por, introducir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-tia-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "ibù": {"sig": "dejar, omitir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ibù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "ccabba-tù": {"sig": "salar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ccabba-tù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "iyacu-n-nua-tia-dù": {"sig": "atravesar de parte a parte", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyacu-n-nua-tia-dù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "cula-ttù": {"sig": "golpear, herir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cula-ttù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "cúllekù": {"sig": "esparcir, desparramar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cúllekù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "kùttù": {"sig": "empujar, chocar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-kùttù-n`, conjugación 1-ùn. Fusión fase 1b de D11, 2026-09-12."},
    "sonnucu": {"sig": "verter, derramar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 619. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sonnucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "iyacusu": {"sig": "apagar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyacusu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "ddur-hu": {"sig": "tejer, trenzar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ddur-hu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "iyurucu": {"sig": "llevar, conducir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyurucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "bucu": {"sig": "hervir, cocer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "sucu": {"sig": "cortar, mochar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "cu-du": {"sig": "ablandar con agua", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cu-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "rrusu-ttu": {"sig": "edificar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-rrusu-ttu-n`, conjugación 1-un. Marcas de la fuente o del OCR: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "sucusu": {"sig": "lavar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sucusu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "surcu-du": {"sig": "emparentar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-surcu-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "iyucu": {"sig": "cazar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "tun-du": {"sig": "toser", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-tun-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "bucu-ttu": {"sig": "coger, asir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bucu-ttu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "ruru-tu": {"sig": "hacer barroso", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ruru-tu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "du-cuttu": {"sig": "mostrar, enseñar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-du-cuttu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "cunnu": {"sig": "ir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cunnu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "mor-du": {"sig": "volar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-mor-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "su-du": {"sig": "raspar, raer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-su-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "púyu-ttu": {"sig": "cargar, agravar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-púyu-ttu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "ttucu-du": {"sig": "bajar, descender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ttucu-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "turru-du": {"sig": "acostarse, echarse (Al: niederliegen)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-turru-du-n`, conjugación 1-un. Marcas de la fuente o del OCR: Al, ocr. Fusión fase 1b de D11, 2026-09-12."},
    "sur-tu": {"sig": "besar, chupar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sur-tu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "ttucu": {"sig": "comer chupando", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ttucu-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "hú-du": {"sig": "morir (con u larga acentuada: d-a-hú-da «muero», d-a-hú-du-pa «moriré»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 623. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-hú-du-n`, conjugación 1-un. Fusión fase 1b de D11, 2026-09-12."},
    "iyuca": {"sig": "cazar, perseguir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyuca-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ollasa-lokono": {"sig": "hender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ollasa-n`, conjugación 2-an. Clave desambiguada como `ollasa-lokono` porque `ollasa` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "hùla-da": {"sig": "perforar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-hùla-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "iyucaia": {"sig": "vender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyucaia-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "cai-da": {"sig": "quebrar, romper", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cai-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "suca": {"sig": "cortar, tronchar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-suca-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "onnaba": {"sig": "responder", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-onnaba-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "purisa": {"sig": "raspar la piel", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-purisa-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ùmaha": {"sig": "hostilizar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùmaha-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ca-lokono": {"sig": "lavarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ca-n`, conjugación 2-an. Clave desambiguada como `ca-lokono` porque `ca` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "canaba": {"sig": "oír", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-canaba-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ccu-da": {"sig": "hilar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 628. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ccu-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "carta-lokono": {"sig": "enterrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-carta-n`, conjugación 2-an. Clave desambiguada como `carta-lokono` porque `carta` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "ccura": {"sig": "cocer [¿coser?]", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ccura-n`, conjugación 2-an. Marcas de la fuente o del OCR: ?. Fusión fase 1b de D11, 2026-09-12."},
    "muli-da": {"sig": "engañar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-muli-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ddura": {"sig": "tejer, trenzar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ddura-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ikkia": {"sig": "evacuar el cuerpo", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ikkia-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "sina-lokono": {"sig": "descaminar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sina-n`, conjugación 2-an. Clave desambiguada como `sina-lokono` porque `sina` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "cuyabua": {"sig": "golpear, herir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cuyabua-n`, conjugación 2-an. Cf. del Fraseario: `cuya-bua` «orar (y 1 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "lamma-da": {"sig": "tambalearse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-lamma-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "manta-lokono": {"sig": "afilar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-manta-n`, conjugación 2-an. Clave desambiguada como `manta-lokono` porque `manta` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "nnaca": {"sig": "empuñar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-nnaca-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "tticaha": {"sig": "ahogarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-tticaha-n`, conjugación 2-an. Cf. del Fraseario: `ttica-ha` «dañar (y 1 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "sa-lokono": {"sig": "nombrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sa-n`, conjugación 2-an. Clave desambiguada como `sa-lokono` porque `sa` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "ùca": {"sig": "casarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùca-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "ddaca": {"sig": "soltar agua", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ddaca-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "saca-da": {"sig": "encontrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-saca-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "cuikita": {"sig": "retornar, volver", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cuikita-n`, conjugación 2-an. Cf. del Fraseario: `cui-kitta` «arrepentirse» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "llucu-da": {"sig": "exponer, mostrar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-llucu-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "mali-cutta": {"sig": "enseñar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-mali-cutta-n`, conjugación 2-an. Cf. del Fraseario: `malli-cutta` «enseñar (y 2 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "maroa-da": {"sig": "cazar con flechas de madera", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-maroa-da-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "mali-cuttu-a": {"sig": "aprender", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-mali-cuttu-a-n`, conjugación 2-an. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-bbura": {"sig": "ser amplio, vasto (m-a-bbura-n «ser angosto»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-bbura-n`, conjugación 2-an. Cf. del Fraseario: `bura` «padre (y 1 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "iyuhu-dú": {"sig": "pender, estar colgado (Perea: sólo puede ser «colgarse»; a-iyubu-du-n «colgar, ahorcar» es el transitivo)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 629. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyuhu-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "bucú": {"sig": "cocerse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bucú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "ùbú": {"sig": "cesar, acabar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùbú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "dittú": {"sig": "conocerse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dittú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "pusi-dú": {"sig": "librarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-pusi-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "sikillú": {"sig": "ser envuelto (Al: eingewickelt werden)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sikillú-n-nua`, conjugación 3-n-nua. Marcas de la fuente o del OCR: Al. Fusión fase 1b de D11, 2026-09-12."},
    "huducullú": {"sig": "suicidarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-huducullú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "cu-dú": {"sig": "introducirse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-cu-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "idi-kittú": {"sig": "ser ceñido", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-idi-kittú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "huke-dú": {"sig": "perderse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-huke-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "buli-dú": {"sig": "pintarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-buli-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "ddele-dú": {"sig": "anclarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ddele-dú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "dibaldi-kittú": {"sig": "acostumbrarse a dar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dibaldi-kittú-n-nua`, conjugación 3-n-nua. Marcas de la fuente o del OCR: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "besú": {"sig": "florecerse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `e-besú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "hudú": {"sig": "curvarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-hudú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "huca-dù": {"sig": "estar agujereado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 633. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-huca-dù-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "iyacusú": {"sig": "apagarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyacusú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "uma-ttú": {"sig": "ser malo", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-uma-ttú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "iyucú": {"sig": "cazarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyucú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "ibi-ttú": {"sig": "arder", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ibi-ttú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "iyabu-dù-kittú": {"sig": "asarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyabu-dù-kittú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "iyahacú": {"sig": "atravesar, pasar por entre", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-iyahacú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "sucú": {"sig": "cortarse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sucú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "ùn-ttú": {"sig": "vencer [?]", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ùn-ttú-n-nua`, conjugación 3-n-nua. Marcas de la fuente o del OCR: ?. Fusión fase 1b de D11, 2026-09-12."},
    "rdú": {"sig": "envanecerse", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 634. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-rdú-n-nua`, conjugación 3-n-nua. Fusión fase 1b de D11, 2026-09-12."},
    "catti-kebe": {"sig": "robar (p. 664: c-a-tti-kebe-n «robar, hurtar»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `catti-kebe-n`, conjugación 4-en. Marcas de la fuente o del OCR: sic. Fusión fase 1b de D11, 2026-09-12."},
    "haule": {"sig": "ser ruin", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `haule-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "caii-me": {"sig": "ser negro", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `caii-me-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ereke": {"sig": "desherbar, sacar la hierba", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ereke-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ca-me": {"sig": "oler, ser oloroso, dar olor de sí (p. 664: ca-eme-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ca-me-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "case-lokono": {"sig": "estar agusanado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `case-n`, conjugación 4-en. Clave desambiguada como `case-lokono` porque `case` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "pere-lokono": {"sig": "estar furioso, airado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `pere-n`, conjugación 4-en. Clave desambiguada como `pere-lokono` porque `pere` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "waikille": {"sig": "estar lejos (p. 665: wai-kille-n «ser ancho»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `waikille-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "m-ake": {"sig": "estar desnudo (privativo de c-ake-n «estar vestido»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `m-ake-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "m-yukehe": {"sig": "no estar loco (privativo: *yukehe- «loco»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ma-yukehe-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "hehe": {"sig": "ser pálido", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hehe-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ipi-lli-be": {"sig": "ser grande (vr.; ipi-ru-be-n nv.)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ipi-lli-be-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "c-ake": {"sig": "estar vestido, cubierto", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-ake-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "sipe": {"sig": "ser amargo [?]", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `sipe-n`, conjugación 4-en. Marcas de la fuente o del OCR: ?. Fusión fase 1b de D11, 2026-09-12."},
    "hebbe": {"sig": "ser viejo, anciano", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hebbe-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "calli-me": {"sig": "lucir, brillar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `calli-me-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ide-lokono": {"sig": "estar muy cocido", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ide-n`, conjugación 4-en. Clave desambiguada como `ide-lokono` porque `ide` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "cule": {"sig": "ser rojo, colorado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `cule-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "were-be": {"sig": "estar caliente (p. 665: tere-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `were-be-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "subu-le": {"sig": "ser verde", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `subu-le-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "m-mole": {"sig": "no estar ebrio (p. 664: sommole-n «estar ebrio»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ma-mole-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "m-isi-re": {"sig": "proceder rectamente (pronombre d-a, b-a… pospuesto)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 638. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `m-isi-re-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "yiba-na": {"sig": "retrasarse, quedarse atrás", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `yiba-na-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-monai-ca": {"sig": "ser pobre", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-monai-ca-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-sicoa": {"sig": "habitar, residir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-sicoa-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "casa-lokono": {"sig": "engendrar (p. 664: c-a-sa-n; m-a-sa-n «no tener hijos»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `casa-n`, conjugación 4-en. Clave desambiguada como `casa-lokono` porque `casa` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "c-a-ima": {"sig": "ser malo (p. 664: c-a-ima-ca-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-ima-n`, conjugación 4-en. Cf. del Fraseario: `ima` «enemigo (y 1 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "emelie": {"sig": "ser nuevo, reciente (emelia de «soy nuevo»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `emelie-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-raiyè": {"sig": "aparecer", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 639. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-raiyè-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "yaha-ddi-a": {"sig": "estar cerca (p. 639: vaha-di-è-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `yaha-ddi-a-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ùttùa": {"sig": "ser sangriento, estar ensangrentado (p. 639: yittùè-n)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ùttùa-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "sommole": {"sig": "estar ebrio", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 664. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `sommole-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "k-eme-kebbù": {"sig": "trabajar (p. 648: keme-kebbu-n «estar atareado»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 664. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `k-eme-kebbù-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "tere-lokono": {"sig": "estar caliente", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 664. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `tere-n`, conjugación 4-en. Clave desambiguada como `tere-lokono` porque `tere` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "wuré": {"sig": "guiar (Sl: fornicar)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `wuré-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "mihite": {"sig": "estar cansado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `mihite-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "wasi": {"sig": "ser amplio", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `wasi-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "wai-kille": {"sig": "ser ancho", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `wai-kille-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "ùsa": {"sig": "ser bueno (mù-ùsa-n «no ser bueno»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 665. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ùsa-n`, conjugación 4-en. Cf. del Fraseario: `usa` «arremeter (y 4 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "wadi": {"sig": "ser amplio (wadi-ke n «es muy amplio»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `wadi-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "móa-di": {"sig": "ser corto", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `móa-di-n`, conjugación 4-en. Fusión fase 1b de D11, 2026-09-12."},
    "mùn-ni": {"sig": "estar con, haber, tener (Schumann: c-a-mùn-ni-n «haber, tener»; m-a-mùn-ni-n «carecer»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 640. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-mùn-ni-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-nsi": {"sig": "amar, querer (c-a-nsi-hi «amor, querencia»; c-a-nsi-sia «amado»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 644. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-nsi-n`, conjugación 5-ca. Cf. del Fraseario: `nsi` «discipulo (y 3 acepción/es más)» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "hadubu-tti": {"sig": "sudar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hadubu-tti-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "cakù": {"sig": "vivir (cakù-ca de «vivo»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `cakù-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "hamaru": {"sig": "estar asustado (?) (p. 668: hamma-ru-ca bu «estás con miedo»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hamaru-n`, conjugación 5-ca. Marcas de la fuente o del OCR: ?. Fusión fase 1b de D11, 2026-09-12."},
    "hiccu-li": {"sig": "ser cojo", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hiccu-li-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-lluccu": {"sig": "no estar vacío", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-lluccu-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "daiya-hù": {"sig": "estar despierto (p. 668: a-daiya-hù-ca bu «eres señor, distinguido»; p. 676: Gott a-daiya-coa-coa-na «el reino de Dios»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-daiya-hù-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "nnakù-di": {"sig": "estar en medio, entre", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-nnakù-di-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "bu-luccu-du": {"sig": "estar en punta", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-bu-luccu-du-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "tu-rubu-ddi": {"sig": "estar cansado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 647. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `tu-rubu-ddi-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "haburù": {"sig": "estar avergonzado (haburu-ca de «me avergüenzo»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `haburù-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "k-ere-ti": {"sig": "estar casada (k-ere-u-n «estar casado»; k-ere-ru-ca «tengo mujer»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `k-ere-ti-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-ddibeu": {"sig": "ser grueso", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-ddibeu-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "kebéru": {"sig": "ser disimulado (p. 668: k-ebe-ru-ca de «yo oculto»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `kebéru-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "hammarù": {"sig": "estar acobardado (?)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `hammarù-n`, conjugación 5-ca. Marcas de la fuente o del OCR: ?. Fusión fase 1b de D11, 2026-09-12."},
    "coa-llaba": {"sig": "estar al lado", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `coa-llaba-n`, conjugación 5-ca. Fusión fase 1b de D11, 2026-09-12."},
    "ni-lokono": {"sig": "hacer (I: to do); el auxiliar universal", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 648. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ni-n`, conjugación 5-ca. Clave desambiguada como `ni-lokono` porque `ni` colisiona con una clave existente o con una palabra española (score_linguistico no filtra por fuente). Fusión fase 1b de D11, 2026-09-12."},
    "ebeta": {"sig": "retardar", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 650. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `ebeta-n`, conjugación recíproco. Fusión fase 1b de D11, 2026-09-12."},
    "tteki-da": {"sig": "persuadir", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 650. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-tteki-da-n`, conjugación recíproco. Fusión fase 1b de D11, 2026-09-12."},
    "c-a-cubu-ruccu": {"sig": "acordarse (m-a-cubu-ruccu-ca de «no me acuerdo»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 666. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `c-a-cubu-ruccu-n`, conjugación 5-ca. Cf. del Fraseario: `cubu-ruccu` «ánimo» — misma raíz o pariente, aislada con otra geminada o glosa. Fusión fase 1b de D11, 2026-09-12."},
    "ddica-hitti": {"sig": "desear ver (verbo de deseo con -hitti-)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 671. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-ddica-hitti-n`, conjugación deseo. Fusión fase 1b de D11, 2026-09-12."},
    "tta-hitti": {"sig": "tener sed, gana de beber (m-a-tta-hitti-n «no tener sed»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 672. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-tta-hitti-n`, conjugación deseo. Fusión fase 1b de D11, 2026-09-12."},
    "dum-ca-rubú-ma": {"sig": "sólo dormir (a-dum-ca «dormir» + -rubu- exclusivo)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 672. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dum-ca-rubú-ma-n`, conjugación exclusivo. Fusión fase 1b de D11, 2026-09-12."},
    "sima-ca": {"sig": "gritar, llamar (reduplicado a-sima-sima-ca-n «clamorear», Hechos 19-32)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sima-ca-n`, conjugación reduplicación. Fusión fase 1b de D11, 2026-09-12."},
    "sucu-sucu": {"sig": "bautizar (reduplicación de a-sucusu-n «lavar»)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-sucu-sucu-n`, conjugación reduplicación. Fusión fase 1b de D11, 2026-09-12."},
    "dia-dia": {"sig": "disertar (reduplicación de a-dia-n «hablar», Hechos 24-25)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-dia-dia-n`, conjugación reduplicación. Fusión fase 1b de D11, 2026-09-12."},
    "haca-haca": {"sig": "predicar (reduplicación de a-haca-n «decir», Hechos 10-42)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 679. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `a-haca-haca-n`, conjugación reduplicación. Fusión fase 1b de D11, 2026-09-12."},
    "poi-m-a": {"sig": "decir ¡ah!, asombrarse (verbo elíptico sobre la interjección poi!)", "cat": "v_raiz", "fuente": "lokono", "notas": "Perea Alonso 1942, Filología Comparada Arawak, tomo I, Compendio Gramatical — el verbo, p. 682. VOCABULARIO DE SCHUMANN (ms. 1755) vía Perea: estrato lokono anterior al Fraseario de Schultz 1802. Forma de Perea: `poi! m-a-n`, conjugación elíptico. Fusión fase 1b de D11, 2026-09-12."},
    "calli": {"sig": "yuca (kia calli «esta yuca», da-calle «mi yuca»)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 628. Voz que sale de paso en los ejemplos de Schumann/Schultz. Fusión fase 1b de D11, 2026-09-12."},
    "barba-coa": {"sig": "cañizo, como parrillas, donde se pone habitualmente a secar o ahumar algo (Perea lo da como ejemplo de -coa «estado, permanencia»)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 651. Voz que sale de paso en los ejemplos de Schumann/Schultz. Fusión fase 1b de D11, 2026-09-12."},
    "curru": {"sig": "no (adverbio pospuesto que sustituye a la m- de negación: m-a-nsi d-a = d-a-nsi-ca curru). OCR «cuлu», л = rr", "cat": "part", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 665. Voz que sale de paso en los ejemplos de Schumann/Schultz. Marcas: ocr. Fusión fase 1b de D11, 2026-09-12."},
    "make-lokono": {"sig": "mucho, con vehemencia (adv.; make d-a «hablo con vehemencia»; infijo intensivo -make-)", "cat": "part", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 676. Voz que sale de paso en los ejemplos de Schumann/Schultz. Clave desambiguada como `make-lokono` (homógrafo). Fusión fase 1b de D11, 2026-09-12."},
    "rubu": {"sig": "sólo; poco; apenas (Perea: «sobre rubu habría mucho que hablar»; Hechos 1-5, 12-18)", "cat": "part", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 651. Voz que sale de paso en los ejemplos de Schumann/Schultz. Fusión fase 1b de D11, 2026-09-12."},
    "hitti-ha": {"sig": "gusto, deseo (infijo -hitti- de los verbos de deseo)", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 651. Voz que sale de paso en los ejemplos de Schumann/Schultz. Fusión fase 1b de D11, 2026-09-12."},
    "lu-luccu-mùn-ti": {"sig": "los que están con él [sus amigos] [?]", "cat": "sust", "fuente": "lokono", "notas": "Perea Alonso 1942, tomo I, Compendio Gramatical — el verbo, p. 666. Voz que sale de paso en los ejemplos de Schumann/Schultz. Marcas: ?. Fusión fase 1b de D11, 2026-09-12."},

    # ══════════════════════════════════════════════════════
    # TAINISMOS DE MEDINA (2026-09-12) — decisión de Miguel: voces de origen
    # taíno, panhispánicas, recogidas en el habla paraguanera. Reconstruidas,
    # no atestiguadas (precedente kanoa/hamaca/konuko).
    # ══════════════════════════════════════════════════════
    "koa": {"sig": "coa: palo de madera aguzado con que se abre el hueco de la siembra y se deposita la semilla", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "coa", "categoria": "agricultura", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, p. 77: «es el palo de madera aguzado en la punta con que se abrían huecos en la tierra, y donde se depositaba la semilla de la siembra.». Etimología: origen antillano (taíno); no está en Alvarado 1921 como lema'. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «coa»."},
    "komején": {"sig": "comején, termita que se come la madera por dentro", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "comején", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, p. 78: «así identificó nuestro pueblo a las termitas, pequeños animales que se consumen la parte interna de la madera y le dejan sana la parte exterior. Es palabra académica.». Etimología: de origen taíno (Alvarado, con Las Casas y Castellanos como testigos): la v. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «comején»."},
    "wayakán": {"sig": "guayacán, árbol de madera durísima y mucho follaje; hoy casi extinto en la península", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "guayacán", "categoria": "flora", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «árbol que fue común en nuestros montes; es de lento crecimiento, mucho follaje; su madera es de mucha dureza y apreciada para trabajar con ella. Hoy casi extinto de la península.». Etimología: de origen taíno. Guayacán es un árbol zigofiliáceo de madera recia y hojas. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «guayacán»."},
    "hiko": {"sig": "hico: cada cuerda de la hamaca; por extensión, toda cuerda o soga", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "hico", "categoria": "casa", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «es palabra ingresada al diccionario de la lengua española con el significado de cada una de las cuerdas que sostienen la hamaca [dictado: «la marca»]; por extensión, toda cuerda o soga.». Etimología: DRAE: hico, del taíno; cada una de las cuerdas de la hamaca; Antillas y Venezuela. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «hico»."},
    "hikotea": {"sig": "hicotea, tortuga de agua dulce comestible (morrocoy en el resto del país)", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "hicotea", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «quelonio que fue abundante en nuestro medio, hoy casi desaparecido, de unos 30 cm de largo, y era comestible; conocido en otras partes del país como morrocoy.». Etimología: DRAE: jicotea / hicotea, del taíno; Antillas, Colombia, Venezuela: tortuga de agua dulce. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «hicotea». ⚠️ Convive con `hikoteya` 'tortuga', acuñación de la simulación (caquetío-hipotético desde F8): retirar la acuñación es decisión aparte."},
    "jaiba": {"sig": "jaiba: cangrejo de mar; también broma o chanza molesta", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "jaiba", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «dos connotaciones le dieron nuestros viejos [dictado: «viajeros»] a esta palabra: una, identificar a una especie de cangrejo de mar; y la chanza o broma que resultara molesta: «me echó una jaiba Anacleto».». Etimología: DRAE: jaiba, del taíno; cangrejo; Antillas y Caribe continental. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «jaiba»."},
    "jején": {"sig": "jején, mosquito diminuto de picada muy molesta", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "jején", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «especie de mosquito mucho más pequeño que este y cuya picadura es muy molesta; es palabra de origen haitiano [según el autor]». Etimología: DRAE: jején, del taíno; panamericano. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «jején»."},
    "magey": {"sig": "maguey: la vara larga de la inflorescencia del cocuy o sisal", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "maguey", "categoria": "flora", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, página no dictada (⚠️ pendiente): «la espiga o vara larga a cuyo extremo superior la planta de sisal o cocuy, como le conocemos en Falcón, produce su inflorescencia». Etimología: DRAE: maguey, del taíno; panamericano (agave). Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «maguey»."},
    "niwa": {"sig": "nigua, pulga que anida bajo la piel y cría en ella (Tunga penetrans); hoy desaparecida", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "nigua", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, p. 195: «fue insecto común en Paraguaná, hoy desaparecido; las hembras fecundadas excavaban una galería en la piel de los animales y del hombre, y en la misma criaban su descendencia; causaban gran picazón y úlceras graves. Al qu». Etimología: DRAE: nigua, del taíno (Tunga penetrans); panamericana; niguatero, Ven.. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «nigua»."},
    "siwato": {"sig": "siguato: desganado, apático, triste (oriente de la península); pescado que empieza a descomponerse (occidente, entre pescadores)", "cat": "adj", "fuente": "caquetío-reconstruido", "forma_fuente": "siguato", "categoria": "estado", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, p. 262: «en la parte oriental de la península es estar desganado, apático, cabizbajo, triste; en la parte occidental, entre pescadores, es el pescado que tiene mal olor, que empieza a descomponerse.». Etimología: DRAE; siguato/ciguato en el Caribe es el envenenado por ciguatera (DRAE: ciguato, del taíno cigua): la acepción occident. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «siguato». Es la isoglosa intrapeninsular mc-mundo-027 del dictado (oriente/occidente, y por oficio)."},
    "yawasa": {"sig": "yaguaza, ave comestible de aguas cenagosas; hoy extinguida en la península", "cat": "sust", "fuente": "caquetío-reconstruido", "forma_fuente": "yaguaza", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-12 (tainismos de Medina): «todas entran como voces nuevas». Medina Colina, Del Habla Paraguanera, p. 305: «es ave comestible propia de las aguas cenagosas, hoy extinguida en nuestra península». Etimología: DRAE: yaguasa, del taíno; Antillas y Venezuela. Panhispánica; el protocolo la había descartado (veredicto D) y Miguel revoca el descarte para los tainismos. caquetío-RECONSTRUIDO como kanoa/hamaca/konuko: cognado taíno citado, sin atestación caquetía colonial — la vía pudo ser el español. Clave = lema fonémico D5 de «yaguaza»."},

    # ══════════════════════════════════════════════════════
    # RETROABSTRAÍDA DE ESTEVES (2026-09-14) — decisión de Miguel: el venado
    # de Paraguaná. Forma viva y documentada (Esteves 1989 p. 51); sustrato en
    # disputa (la lexicografía general la da castellana). Entra por decisión,
    # no por cognado. Medición: 6-fusion/matacan_venado_2026-09-14.yaml.
    # ══════════════════════════════════════════════════════
    "matakán": {"sig": "venado matacán: el cérvido pequeño («de poca alzada», Mazama) de los bosques de Paraguaná, caza mayor de la península; hoy extinguido en el llano", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "matacán", "categoria": "fauna", "notas": "Decisión de Miguel 2026-09-14: «sí o sí lo tenemos que utilizar […] matacán siendo el único mamífero de ese tamaño, venado, que además funciona como caza […] si quieres lo ponemos como simulación o como lo que quieras». Esteves 1989, parte 2, p. 51 (imagen verificada), s.v. MATACAN: «cérvido de poca alzada. En tiempos pasados había rebaños de este tipo de venado en los bosques de Paraguaná. Se han extinguido por la cacería incontrolada»; Punta de Matacán, en el Golfete, es hoy aldea de pescadores. El animal está atestiguado en Coro en 1540 (Castellanos: «conejos y venados») y sobrevive en el Cerro Santa Ana. CAPA RETROABSTRAÍDA (#124): la forma está documentada en boca viva; lo incierto es el sustrato — y aquí la duda pesa más que en las voces de Medina: la lexicografía general da «de matar y can» (la liebre que agota a los perros), Alvarado 1921 no la tiene entre las voces indígenas (cero verificado con variantes; sí tiene locho, del quechua) y ningún vocabulario arahuaco o caribe del repo llama así al venado (motilón amúsha/trihunchti, guajiro Uyára, achagua nerraí). NO es caquetío-reconstruido (el precedente wayakán exigía cognado taíno) ni hipotético (la forma no es inventada). Especie: Mazama, distinta del venado caramerudo (Odocoileus). Cierra el hueco léxico de ecologia-037. La ven los perfiles `suelto` y `era2`. Deuda: Alvarado 1929 (Glosario del bajo español) s.v.; Medina Colina físico s.v. Clave = lema fonémico D5 de «matacán»; fonotáctica atestiguada: válida."},

    # ══════════════════════════════════════════════════════
    # RETROABSTRAÍDAS DE MEDINA (2026-09-13, #124 opción A) — las voces
    # del habla paraguanera de nivel A/B/C: forma documentada, sustrato
    # incierto. Las ven los perfiles `suelto` y, desde el 2026-09-14, `era2`.
    # ══════════════════════════════════════════════════════
    "arifuke": {"sig": "harina de maíz a la que se agregaba raspillo [?] de panela y que se servía como parte de la comida de los arrieros. Es muy nutritiva.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "arifuque", "nivel_dictado": "A", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 31, s.v. arifuque: «harina de maíz a la que se agregaba raspillo [?] de panela y que se servía como parte de la comida de los arrieros. Es muy nutritiva.». Nivel A del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "chiriwa": {"sig": "recipiente de barro cocido, pequeño, manual, para contener agua u otro líquido. Es palabra popular.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "chirigua", "nivel_dictado": "A", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 72, s.v. chirigua: «recipiente de barro cocido, pequeño, manual, para contener agua u otro líquido. Es palabra popular.». Nivel A del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "tuturuto": {"sig": "fue una planta venenosa y sin ninguna utilidad para el paraguanero", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "tuturuto", "nivel_dictado": "A", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 288, s.v. tuturuto: «fue una planta venenosa y sin ninguna utilidad para el paraguanero». Nivel A del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "barisiwa": {"sig": "árbol que fue abundante en nuestro medio, hoy muy escaso, de hasta ocho metros de altura, en otras regiones del país conocido como palo de balsa. Su m", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "barisigua", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 43, s.v. barisigua: «árbol que fue abundante en nuestro medio, hoy muy escaso, de hasta ocho metros de altura, en otras regiones del país conocido como palo de balsa. Su madera era muy liviana de peso, de granulación suav». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "bayure": {"sig": "especie de abeja que produce una miel dulce y un poco ácida. También se le llama así a la casa que hace esta abeja, generalmente en palos secos y huec", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "bayure", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 45, s.v. bayure: «especie de abeja que produce una miel dulce y un poco ácida. También se le llama así a la casa que hace esta abeja, generalmente en palos secos y huecos.». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: Abeja sin aguijón (Meliponini), por la miel «dulce y un poco ácida» (la acidez alta es el rasgo de las mieles de meliponinos: Vit et al. 2012 miden 12,7-95,9 meq/kg en la Melipona favosa de Paraguaná) y por el nido en palos huecos. Especie: abierta (¿Melipona favosa? ¿otra?).."},
    "lefaria": {"sig": "cardón cuyo fruto se llamaba breva; su tallo sin espinas se usaba para asentar el agua", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "lefaria", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 49 (y asentar agua), s.v. lefaria: «[no tiene entrada propia hasta ahora] cardón cuyo fruto se llamaba breva; su tallo sin espinas se usaba para asentar el agua». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "budare": {"sig": "palabra aceptada por la Real Academia; plato de barro o hierro para cocer el pan de maíz.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "budare", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. budare: «[según Miguel] palabra aceptada por la Real Academia; plato de barro o hierro para cocer el pan de maíz.». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "chiware": {"sig": "así identificó nuestro pueblo a una planta enredadera que generalmente cubre un árbol para, apoyándose en él, poder desarrollarse. No es parásita, por", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "chiguare", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 71, s.v. chiguare: «así identificó nuestro pueblo a una planta enredadera que generalmente cubre un árbol para, apoyándose en él, poder desarrollarse. No es parásita, por lo que no daña a la que le sirve de apoyo. Sus fr». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "kuawaro": {"sig": "árbol de madera dura que se utilizó para hacer las cercas de los conucos y el armazón de las viviendas. Es palabra popular.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "cuaguaro", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 83, s.v. cuaguaro: «árbol de madera dura que se utilizó para hacer las cercas de los conucos y el armazón de las viviendas. Es palabra popular.». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "watakare": {"sig": "árbol común, y cuyos frutos no eran comestibles por el ser humano", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guatacare", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. guatacare: «árbol común, y cuyos frutos no eran comestibles por el ser humano». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "isikawa": {"sig": "árbol de nuestros montes utilizado en la medicina empírica para tratar hernias", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "isicagua", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. isicagua: «árbol de nuestros montes utilizado en la medicina empírica para tratar hernias». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "maba": {"sig": "son tres denominaciones para identificar al panal de las abejas", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "maba", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. maba: «[con mebi y bayure] son tres denominaciones para identificar al panal de las abejas». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "totokoro": {"sig": "así se denominó la madera de los brazos del cardón seco, o sea, al corazón del mismo, que es la parte sólida de él; se obtenía el cañizo para el techo", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "totocoro", "nivel_dictado": "B", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 281, s.v. totocoro: «así se denominó la madera de los brazos del cardón seco, o sea, al corazón del mismo, que es la parte sólida de él; se obtenía el cañizo para el techo de la vivienda.». Nivel B del protocolo del dictado. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "buchuko": {"sig": "también se conoció como buchuco", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "buchuco", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 179, s.v. buchuco: «[s.v. mapire] también se conoció como buchuco». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-069 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "busuga": {"sig": "árbol de madera liviana que se utilizó para hacer la armazón de las casas de bahareque. Su corteza se usaba para teñir de color amarillo. Se escuchó d", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "busuga", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 52, s.v. busuga: «árbol de madera liviana que se utilizó para hacer la armazón de las casas de bahareque. Su corteza se usaba para teñir de color amarillo. Se escuchó decir «tan amarillo como una busuga». Es palabra po». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-046 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "kachinare": {"sig": "es creada por el pueblo para designar con ella el fruto del cardón que no terminó de desarrollarse, que quedó pequeño o no maduró bien.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "cachinare", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 57, s.v. cachinare: «es creada por el pueblo para designar con ella el fruto del cardón que no terminó de desarrollarse, que quedó pequeño o no maduró bien.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-047 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "kadare": {"sig": "la primera fue creada por el pueblo como sinónimo de la segunda, y ambas significaron una suciedad profunda; conforme a la Academia de la Lengua, la s", "cat": "adj", "fuente": "caquetío-retroabstraido", "forma_fuente": "cadare", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 57, s.v. cadare: «la primera fue creada por el pueblo como sinónimo de la segunda, y ambas significaron una suciedad profunda; conforme a la Academia de la Lengua, la segunda es grasa o suciedad de la lana, vestidos u ». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-070 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "chenga": {"sig": "voz con que el pueblo identificó a la paloma perdiz. Fue abundante en nuestros montes, hoy casi desaparecida.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "chenga", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 70, s.v. chenga: «voz con que el pueblo identificó a la paloma perdiz. Fue abundante en nuestros montes, hoy casi desaparecida.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-059 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: paloma perdiz = Leptotila / Geotrygon (paloma de suelo del monte seco); especie abierta."},
    "chebebe": {"sig": "con este nombre, un tanto extraño, nuestros mayores identificaron a la langosta; otros le llaman saltamontes. Es palabra de pueblo.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "chevebe", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 69-70, s.v. chevebe: «con este nombre, un tanto extraño, nuestros mayores identificaron a la langosta; otros le llaman saltamontes. Es palabra de pueblo.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-060 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "kurubo": {"sig": "caracol marino cuya caparazón utilizaron los alfareros para pulir los envases que fabricaban, y también para hacer cal mediante su cocción a altas tem", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "curubo", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 86, s.v. curubo: «caracol marino cuya caparazón utilizaron los alfareros para pulir los envases que fabricaban, y también para hacer cal mediante su cocción a altas temperaturas.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-061 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: gasterópodo marino de concha gruesa (¿Strombus/Lobatus? ¿Melongena? ¿Cittarium?); especie abierta."},
    "debudeke": {"sig": "símil de la paledonia", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "debudeque", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. debudeque: «símil de la paledonia». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-071 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: Dulce de Falcón: torta hecha con pan viejo y papelón (o panela), que se corta en trozos rectangulares «parecidos a ladrillos de adobe» (recetarios y blogs falconianos, consultados el 2026-09-07). La paledonia con la que Medina la compara es la catalina o cuca: galleta o torta de harina de trigo y melado de papelón con canela, clavo y anís; el nombre paledonia es el del Zulia y los Andes.."},
    "disey": {"sig": "nuestras abuelas cocinaban sobre un fuego producido con leña seca, rodeado de tres topias o piedras de igual tamaño sobre las que descansaban la sarté", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "disey", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 95, s.v. disey: «nuestras abuelas cocinaban sobre un fuego producido con leña seca, rodeado de tres topias o piedras de igual tamaño sobre las que descansaban la sartén, la olla u otro. A dichas topias se les denominó». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-072 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "gatiao": {"sig": "árbol cuyas ramas nuestros mayores utilizaron para espantar moscas.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "gatiao", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 127, s.v. gatiao: «árbol cuyas ramas nuestros mayores utilizaron para espantar moscas.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-048 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "wakukero": {"sig": "así denominaron a una abeja de color amarillento que producía una miel muy dulce y también de color amarillo.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guacuquero", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 130, s.v. guacuquero: «así denominaron a una abeja de color amarillento que producía una miel muy dulce y también de color amarillo.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-062 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: meliponino de color amarillo y miel amarilla (¿Tetragonisca / Scaptotrigona? cf. la «rubita» amarilla de las listas nacionales); especie abierta."},
    "walamo": {"sig": "así le llaman, en las poblaciones de Tacuato y Santa Ana, a un bisure de color amarillo combinado con gris terroso. En el resto de las poblaciones par", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "gualamo", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 130, s.v. gualamo: «así le llaman, en las poblaciones de Tacuato y Santa Ana, a un bisure de color amarillo combinado con gris terroso. En el resto de las poblaciones paraguaneras conserva el nombre de bisure.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-063 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: lagarto amarillo y gris terroso (¿Cnemidophorus / Ameiva?); especie abierta — puede ser un bisure distinto, no solo otro nombre."},
    "wamaro": {"sig": "era un árbol venenoso para los animales. Hoy es escaso en nuestros montes, quizá debido a los continuos veranos.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guamaro", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 130, s.v. guamaro: «era un árbol venenoso para los animales. Hoy es escaso en nuestros montes, quizá debido a los continuos veranos.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-049 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "wanariji": {"sig": "eran las denominaciones de los frutos de determinados cardones. La primera era del cardón de lefaria, la segunda del susucure.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guanariji", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 49, s.v. guanariji: «eran las denominaciones de los frutos de determinados cardones. La primera era del cardón de lefaria, la segunda del susucure.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-050 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "warero": {"sig": "fue planta enredadera, común en nuestros montes, cuyas ramas se utilizaron para amarrar el embarrado [dictado: «embargado»] de las paredes de la vivie", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guarero", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. guarero: «fue planta enredadera, común en nuestros montes, cuyas ramas se utilizaron para amarrar el embarrado [dictado: «embargado»] de las paredes de la vivienda. Las hojas servían de comida para los marranos». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-051 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "warupepe": {"sig": "la auyama madura, cocida, mezclada con leche, que quedara espesa: eso era un guarupepe, comida muy apreciada por nuestra gente.", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "guarupepe", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. guarupepe: «la auyama madura, cocida, mezclada con leche, que quedara espesa: eso era un guarupepe, comida muy apreciada por nuestra gente.». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-073 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "iwira": {"sig": "fue paloma silvestre del tamaño de la casera; abundante en épocas pasadas, hoy en vías de extinción; de carne muy apreciada", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "igüira", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. igüira: «fue paloma silvestre del tamaño de la casera; abundante en épocas pasadas, hoy en vías de extinción; de carne muy apreciada». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-064 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "machire": {"sig": "es producto del ingenio de nuestro pueblo para designar la harina del maíz que presenta en su textura mucha granulación y, por lo tanto, dará una arep", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "machire", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. machire: «es producto del ingenio de nuestro pueblo para designar la harina del maíz que presenta en su textura mucha granulación y, por lo tanto, dará una arepa de baja calidad, por lo que es recomendable volv». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-074 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "marite": {"sig": "así llamaron a la planta acuática que se desarrolla en la superficie del agua depositada en los estanques", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "marite", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 180, s.v. marite: «así llamaron a la planta acuática que se desarrolla en la superficie del agua depositada en los estanques». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-052 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "matejea": {"sig": "así se denominó a la vivienda hecha por las avispas", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "matejea", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 181, s.v. matejea: «así se denominó a la vivienda hecha por las avispas». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-065 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "mebi": {"sig": "son tres denominaciones para identificar al panal de las abejas", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "mebi", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, página no dictada (⚠️ pendiente), s.v. mebi: «[con maba y bayure] son tres denominaciones para identificar al panal de las abejas». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-066 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "memerea": {"sig": "con este nombre se conoció a los panales de las abejas, generalmente localizados en troncos secos", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "memerea", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 183, s.v. memerea: «con este nombre se conoció a los panales de las abejas, generalmente localizados en troncos secos». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-067 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "nawata": {"sig": "se denominó así a la auyama que estaba en pleno proceso de desarrollo", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "naguata", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 193, s.v. naguata: «se denominó así a la auyama que estaba en pleno proceso de desarrollo». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-053 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "kihuawa": {"sig": "una variedad de frijol común en épocas pasadas y muy nutritiva", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "quihuagua", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 237, s.v. quihuagua: «una variedad de frijol común en épocas pasadas y muy nutritiva». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-054 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "sarutako": {"sig": "para los paraguaneros, todo cuanto estuviese en su punto medio de perfección estaba sarutaco: frutas a medio madurar, carne a medio asar o medio cocid", "cat": "adj", "fuente": "caquetío-retroabstraido", "forma_fuente": "sarutaco", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 260, s.v. sarutaco: «para los paraguaneros, todo cuanto estuviese en su punto medio de perfección estaba sarutaco: frutas a medio madurar, carne a medio asar o medio cocida. En el estado Lara le dicen así solo a los cambu». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-075 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "seretón": {"sig": "forma parte del folclor y consistía en que se tenía la certeza de que existían hombres con la facultad de transformarse en animales pequeños y general", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "seretón", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 262, s.v. seretón: «forma parte del folclor y consistía en que se tenía la certeza de que existían hombres con la facultad de transformarse en animales pequeños y generalmente domésticos, pues los mismos tenían pacto dia». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho creencia-019 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "susukure": {"sig": "cardón cuyo fruto se llamaba guanariji", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "susucure", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 49, s.v. susucure: «[sin entrada propia hasta ahora] cardón cuyo fruto se llamaba guanariji». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-055 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "tapirama": {"sig": "frijol de grano grande, de sabor ligeramente amargo, que obliga a cambiar varias veces el agua en que se cuece; altamente nutritiva; las hay de distin", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "tapirama", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 271, s.v. tapirama: «frijol de grano grande, de sabor ligeramente amargo, que obliga a cambiar varias veces el agua en que se cuece; altamente nutritiva; las hay de distintos colores y se les denomina por el mismo: tapira». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-076 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: Phaseolus lunatus, el frijol de Lima (el amargor que se lava es el de los glucósidos cianogénicos de la especie)."},
    "teko": {"sig": "es planta xerófita [dictado: «cerófita»] de hojas lanceoladas, cortas y con espinas por sus bordes, resistente a los veranos, y cuando llueve da unos", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "teco", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 274, s.v. teco: «es planta xerófita [dictado: «cerófita»] de hojas lanceoladas, cortas y con espinas por sus bordes, resistente a los veranos, y cuando llueve da unos frutos muy dulces». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-056 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5. Identificación: por las hojas lanceoladas con espinas marginales y el fruto dulce, una bromelia terrestre (¿Bromelia chrysantha, el 'maya' / 'piñuela'?)."},
    "tobeka": {"sig": "con esta palabra identificaron a la perdiz, también llamada chenga", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "tobeca", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 279, s.v. tobeca: «con esta palabra identificaron a la perdiz, también llamada chenga». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-068 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "tura": {"sig": "cuando la mazorca del maíz tenía pocos granos, nuestros mayores decían que era pura tura", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "tura", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 287, s.v. tura: «cuando la mazorca del maíz tenía pocos granos, nuestros mayores decían que era pura tura». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-057 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},
    "urubana": {"sig": "fue un frijol de color morado, sabor agradable, y que por llegar a Paraguaná desde la isla de Aruba se denominó urubana, sin que eso quiera decir que", "cat": "sust", "fuente": "caquetío-retroabstraido", "forma_fuente": "urubana", "nivel_dictado": "C", "notas": "Medina Colina 2013, Del Habla Paraguanera, p. 291, s.v. urubana: «fue un frijol de color morado, sabor agradable, y que por llegar a Paraguaná desde la isla de Aruba se denominó urubana, sin que eso quiera decir que esa isla es su origen, pues allí solo producen neg». Nivel C del protocolo del dictado; fallo de Miguel 2026-09-11 (fallo-miguel-nivel-C-medina.md); hecho ecologia-058 en el corpus. CAPA RETROABSTRAÍDA (#124, Miguel 2026-09-13, opción A): la forma está documentada en boca viva del s. XX; lo incierto es que el sustrato sea caquetío y no castellano regional, caribe o papiamento. La ven sólo los perfiles `suelto`; `base` no. Regla 4: la fuente es paraguanera, la conclusión es de la esfera. Clave = lema fonémico D5."},

    # -- FIN VOCABULARIO_BASE --
}


# ── Glosario Zavala Reyes 2015 ────────────────────────────────────────
# El lexicón contenía solo ~66 de las 288 entradas del glosario caquetío de
# Zavala (23%) — la fuente atestiguada central del proyecto. Faltaban incluso
# palabras que dan nombre a agentes (buio, bagre, cunaro, guaranaro, dara,
# naure), que por tanto NO puntuaban como caquetío en score_linguistico.
#
# CERRADO el 2026-08-03 (tarea F7): el parseo cubre las 288/288. 225 entran al
# habla activa; 63 quedan fuera POR DISEÑO (45 topónimos + 14 antropónimos + 4
# descartes), no por deuda. Ver investigacion/fuentes/zavala-reyes-2015.md.
#
# `lexicon_zavala.py` lo genera `minar_zavala_glosario.py` desde el PDF, con
# curación por tiers: entra el vocabulario del habla; los topónimos,
# antropónimos y etnónimos quedan aparte como referencia de canon.
#
# Se fusiona SIN pisar entradas existentes: si una forma ya está en
# VOCABULARIO_BASE con otra etiqueta, gana la que ya estaba (la corrección de
# esas colisiones es una decisión aparte, no un efecto colateral del import).
try:
    from lexicon_zavala import GLOSARIO_ZAVALA, HOMOGRAFOS_ZAVALA
except ImportError:      # el módulo generado no está presente
    GLOSARIO_ZAVALA, HOMOGRAFOS_ZAVALA = {}, frozenset()

for _f, _e in GLOSARIO_ZAVALA.items():
    VOCABULARIO_BASE.setdefault(_f, _e)
if GLOSARIO_ZAVALA:
    del _f, _e

# ── D11 (#39): la columna añú/paraujano y el refuerzo lokono ─────────
# `lexicon_a2.py` lo genera `minar_a2_swadesh.py` desde la transcripción de
# la Tabla A-2 de Oliver (6-fusion/tabla_a2_transcripcion.yaml). Vocabulario
# de COMPARACIÓN (detección de fugas, columnas del filtro fonotáctico), no
# habla de agentes. Misma disciplina que el import de Zavala: setdefault —
# jamás pisa una clave existente; las colisiones quedan en COLISIONES_A2.
try:
    from lexicon_a2 import PARAUJANO_A2, LOKONO_A2
except ImportError:      # el módulo generado no está presente
    PARAUJANO_A2, LOKONO_A2 = {}, {}

for _f, _e in list(PARAUJANO_A2.items()) + list(LOKONO_A2.items()):
    VOCABULARIO_BASE.setdefault(_f, _e)
if PARAUJANO_A2 or LOKONO_A2:
    del _f, _e

# ── D11 fase 2 (#121): la comparanda ACHAGUA ──────────────────────────
# `lexicon_achagua.py` lo genera `6-fusion/scripts/generar_lexicon_achagua.py`
# desde la transcripción por visión de Neira y Ribero 1762
# (6-fusion/achagua_neira_ribero_1762.yaml). Vocabulario de COMPARACIÓN, no
# habla de agentes. Misma disciplina que Zavala y la A-2: setdefault, jamás
# pisa una clave existente; los homógrafos vienen ya desambiguados con
# `-achagua`. Miguel, 2026-09-13: «Fusionemos lo que conseguimos achagua».
try:
    from lexicon_achagua import COMPARANDA_ACHAGUA
except ImportError:      # el módulo generado no está presente
    COMPARANDA_ACHAGUA = {}

for _f, _e in COMPARANDA_ACHAGUA.items():
    VOCABULARIO_BASE.setdefault(_f, _e)
if COMPARANDA_ACHAGUA:
    del _f, _e


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
            # `paa-ka` hasta el 2026-09-19: `paa` quedó archivada por la
            # política «manda la atestiguada» y el paradigma se muda a `were`
            # (Zavala #149), que es también `v_raiz`. Este dict NO llega al
            # prompt —`AFIJOS_ATESTIGUADOS` sólo renderiza REGLAS_ZAVALA y
            # REGLAS_TOPONIMICAS—, pero es documentación del módulo y una
            # referencia muerta aquí es deuda igual.
            "were-ka = ya di / ya entregué",
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
            # `paa-da` hasta el 2026-09-19: ver la nota de `-ka`.
            "were-da = daré / voy a dar",
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
    # ⚠️ d21.6 («Me parece🫡 la B», 2026-09-21). #109 retiró la glosa 'lugar de'
    # el 2026-09-07 —el censo de Esteves dio 0 casos y el 'lugar' paraguanero
    # es `-bakoa`— y las dos plantillas siguieron enseñando literalmente
    # «`-ana` = lugar de X» durante dos semanas: el mismo patrón que
    # `kali-bana`, el canon decidiendo una cosa y el prompt diciendo otra.
    # Ahora se enseña SIN GLOSA, como `-ubana` y `-uru`, que es el patrón que
    # el proyecto ya eligió para una desinencia atestiguada sin valor anotado.
    # Ni se quita del prompt (opción A, que tiraría un formante atestiguado)
    # ni se deja el error con permiso (C). Y abre la puerta a que los agentes
    # propongan la glosa, que es para lo que existe la simulación.
    "-ana": {
        "nombre": "desinencia (valor no precisado)",
        "desc": "Desinencia atestiguada de la lengua; nadie anotó su valor. "
                "La glosa 'lugar de' se retiró del canon el 2026-09-07 (#109).",
        "uso": "RAÍZ + -ana",
        "ejemplos": [],
        "evidencia": "ATESTIGUADA COMO FORMA, sin glosa de fuente. #109 (decisión B "
                     "de Miguel, 2026-09-07) retiró la glosa 'lugar de': el censo de "
                     "Esteves dio 0 casos y el 'lugar' paraguanero es -bakoa. Los "
                     "apoyos que tenía eran de FORMA, no de valor: Curiana (Zavala "
                     "2015, sin glosa de fuente), Paraguaná (*Para+gua+na, "
                     "segmentación abierta), Barquisimeto (*Barqui+sima/ima). "
                     "d21.6 (2026-09-21): deja de enseñarse con glosa y pasa al "
                     "patrón de -ubana / -uru",
        "instruccion_agente": (
            "`-ana` es una desinencia que tu lengua tiene y cuyo valor nadie "
            "anotó: puedes usarla si propones tú su valor entre corchetes."
        ),
    },
    "-gua": {
        "nombre": "región / área asociativa",
        "desc": "Zona más amplia asociada con X. Menos específico que -ana.",
        "uso": "RAÍZ + -gua  →  región, área amplia",
        # d21.14 B: `Corogua` era un derivado que el lexicón no tiene. Los tres
        # ejemplos van ahora con formas que el lexicón SÍ tiene (`maure`,
        # `para`) o con el topónimo entero, que no se presenta como derivación.
        "ejemplos": [
            "maure + gua = maure-gua (la tierra del algodón, la región)",
            "para + gua + na = Paraguaná (segmentación abierta)",
            "Araya (región salina)",
        ],
        "evidencia": "Topónimos venezolanos de Falcón y Sucre",
        "deuda": "sin-procedencia (d21.7, «Si me parece, B», 2026-09-21): cero clave "
                 "foránea a 4-fuentes/bibliografia.yaml. Se sigue enseñando mientras "
                 "se le busca fuente en 2-lengua/toponimos.yaml (109 topónimos en "
                 "canon) y en el gazeteer de Esteves ya minado — campaña aparte. "
                 "Apoyo que ya existe en el canon: `paragua` se lee como `para` "
                 "'mar' + `-gua`, y por eso el 2026-09-19 se decidió NO fusionar "
                 "`parawa`/`para`: fusionarlas habría borrado este morfema",
        "instruccion_agente": (
            "Para referirte a una región entera, usa -gua: "
            "'maure-gua' = la tierra del algodón (región)."
        ),
    },
    "-bana": {
        "nombre": "cerro / sitio alto",
        "desc": "El cerro, la loma o el sitio alto asociado a X.",
        "uso": "RAÍZ + -bana  →  cerro de, sitio alto de",
        # d21.14 B: `Judibana` era un derivado que el lexicón no tiene (`judi`
        # no es clave). Se reemplaza por `biro`, que sí lo es y es además el
        # ejemplo que IDENTIDAD_LINGUISTICA enseña desde el 2026-09-19.
        "ejemplos": [
            "kapu + bana = kapubana, el duende del cerro (atestiguado, Zavala #61)",
            "sima + bana = la cumbre del cerro",
            "biro + bana = biro-bana, el cerro de la sal",
        ],
        "evidencia": "D9 (#38), aprobada 2026-08-30: Zavala Reyes 2015 #26 «Bana (E): "
                     "Sitio, cerro alto» + capu/capubana #60-61 + Guadadubana (González "
                     "Batista) + el Cerro de Capú (Velasco 2015) + Judibana. 'Orilla' "
                     "tuvo cero apoyos: la costa atestiguada es kari. Homónimo de bana "
                     "'hígado' (reconstruido). Hasta el 2026-09-13 el motor seguía "
                     "enseñando 'orilla de'",
        "instruccion_agente": (
            "Para un cerro o un sitio alto: 'sima-bana' = la cumbre del cerro; "
            "'kuru-bana' = el cerro arbolado. Para la orilla del mar usa kari."
        ),
    },
}

# ── RETIRADAS (Miguel, 2026-09-14): «Sí o sí hay que sacar eso de -ko y -sha,
# si es inventado, tanto de la gramática como de los nombres». Ninguna fuente
# sostiene -ko «hombre de» ni -sha «mujer de»: eran convención de la era 1
# (el campo `wayunaiki` de cada una es una analogía, no una atestación). Se
# archivan aquí con la misma disciplina que FUERA_DEL_HABLA: no se enseñan,
# no cuentan como regla al clasificar neologismos, y los nombres del elenco de
# la era 2 se rehacen sin ellas (6-fusion/decisiones_tanda_2026-09-14.yaml
# §antroponimos_era2). Los nombres de la era 1 (Biro-ko, Paugis-sha…) se
# conservan tal cual en curiana_agents.py: esa era está cerrada.
REGLAS_RETIRADAS: dict[str, dict] = {
    "-ko": {
        "retirada": "2026-09-14, decisión de Miguel: sin fuente; era convención de la era 1",
        "nombre": "agente masculino",
        "desc": "Hombre cuya identidad/trabajo está asociado a X.",
        "uso": "RAÍZ + -ko  →  nombre o apodo masculino",
        "ejemplos": [
            "biro + ko = Biro-ko (el salinero, el hombre de la sal)",
            "korie + ko = Korie-ko (el de la choza, guardián del espacio)",
            "buko + ko = Buko-ko (el de la represa)",
        ],
        "wayunaiki": "-shi (masculine singular marker, triad A)",
        "instruccion_agente": (
            "Si un hombre trabaja con algo o es conocido por algo, su nombre o apodo "
            "puede formarse con -ko: el pescador experto podría llamarse 'bagre-ko'."
        ),
    },
    "-sha": {
        "retirada": "2026-09-14, decisión de Miguel: sin fuente; era convención de la era 1",
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
    # ── d21.9 («Si, A.», 2026-09-21) ──────────────────────────────────
    # `-naiki` se retira por la MISMA razón que `-ko` y `-sha`: sin fuente, y
    # era convención. Su apoyo era literalmente el NOMBRE DE LA LENGUA ANDAMIO
    # (`wayuunaiki`) y su único ejemplo también, o sea que el argumento era
    # circular. Medido antes de retirarlo: 0 usos en 95.445, ninguna plantilla
    # lo enseñaba, y vivía sólo en el desafijador.
    # ⚠️ Sacarlo de `TODAS_LAS_REGLAS` SÍ mueve `_SUFIJOS_CAQ`, así que se
    # midió aunque el uso fuera cero — ninguna forma de la base se desafija
    # distinto (6-fusion/medicion_tanda_21_2026-09-21.yaml §d21_9_naiki).
    "-naiki": {
        "retirada": "2026-09-21, decisión de Miguel (d21.9): sin fuente; el apoyo "
                    "era el nombre de la lengua andamio y su ejemplo también",
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

REGLAS_POSESIVAS: dict[str, dict] = {
    "ta-": {
        "nombre": "posesivo 1ra singular",
        "desc": "Mi, mío/mía. Del hablante.",
        "uso": "ta- + SUSTANTIVO  →  mi X",
        "ejemplos": [
            "ta + barsure = ta-barsure (mi alma)",
            "ta + korie = ta-korie (mi armadillo)",
            "ta + anüiki = ta-anüiki (mi habla, mi lengua)",
        ],
        "wayunaiki": "ta- (1ra persona singular posesivo, cognado directo)",
        "deuda": "sin-procedencia — el único apoyo escrito es el cognado wayunaiki, "
                 "que es el andamio que D11 retiró como hermana por defecto. "
                 "Auditoría de morfología 2026-09-20 §1 y §2(d)",
    },
    "wa-": {
        "nombre": "posesivo 1ra plural",
        "desc": "Nuestro/nuestra. De nosotros, del grupo.",
        "uso": "wa- + SUSTANTIVO  →  nuestro X",
        "ejemplos": [
            "wa + barsure = wa-barsure (nuestra alma colectiva)",
            "wa + buko = wa-buko (nuestra represa)",
            "wa + anüiki = wa-anüiki (nuestra lengua)",
        ],
        "wayunaiki": "wa- (1ra persona plural posesivo, cognado directo)",
        "atestiguado": "apoyo insular independiente en 2-lengua/morfologia.md §2: "
                       "van Buurt 2014 §6 vía de Goeje 1928",
    },
    # ── EL NO-POSEÍDO (d21.13, «Vale, B», 2026-09-21) ─────────────────
    # De los tres huecos que la auditoría midió —no-poseído, número de los
    # irracionales y género varonil/no varonil— se importa SÓLO éste, que es
    # el que menos cosmovisión arrastra: es pura gramática. Los otros dos se
    # declaran como huecos con su cita en 2-lengua/morfologia.md y se esperan
    # (el género es lo que la regla 4 prohíbe importar sin marcarlo, y el
    # proyecto acaba de pasar por eso con `-ko`/`-sha`).
    #
    # El hueco que tapa está MEDIDO: `ta-` se usa 6.843 veces sobre 258 raíces
    # distintas, y parte de eso son agentes que dicen «mi cerro» porque no
    # tienen forma de decir «el cerro». Hasta hoy el sistema tenía cuatro
    # maneras de decir de quién es algo y ninguna de decir que no es de nadie.
    "u-": {
        "nombre": "no-poseído / absoluto",
        "desc": "La cosa sin dueño: LA casa, EL cerro, no «mi» ni «nuestro».",
        "uso": "u- + SUSTANTIVO  →  el/la X, sin poseedor",
        "ejemplos": [
            "u + korie = u-korie (el armadillo, no el mío)",
            "u + buko = u-buko (la represa, sin decir de quién)",
            "u + biro = u-biro (la sal, la que hay)",
        ],
        "atestiguado": "Perea y Alonso 1942 p. 587: índices personales sobre el "
                       "nombre (`da-si-kua` 'mi casa') frente al índice ABSOLUTO "
                       "`u-`/`ù-` — `u-si-kua-hù` = 'LA casa, sin poseedor'. Es la "
                       "marca de no-poseído, que es como el arahuaco dice lo que "
                       "otras familias dicen con la alienabilidad",
        "capa": "reconstruido desde el lokono (deuda D11 fase 3, como los tres "
                "aspectos y los cuatro prefijos): ninguna fuente caquetía lo "
                "atestigua. Se importa porque es gramática pura y tapa un hueco "
                "medido; el género y el número de los irracionales, que arrastran "
                "cosmovisión, NO se importan",
        "instruccion_agente": (
            "Cuando hablas de una cosa que no es de nadie, no la hagas tuya: "
            "'u-biro' es la sal que hay, 'ta-biro' es mi sal."
        ),
    },
}

# ── ATRIBUTIVO / PRIVATIVO (d21.5, «Vamos con la C», 2026-09-21) ──────
# `ka-` y `ma-` vivían en REGLAS_POSESIVAS, y `ka-` se llamaba «posesivo
# genérico» y se enseñaba como `ka-biro = el salinero` —una persona—. No lo
# es: es el ATRIBUTIVO arahuaco, el par mínimo del privativo `ma-`, y
# predicar un nombre es lo que hace. El `desc` viejo («el/la que TIENE X») ya
# era correcto; lo que estaba mal eran el nombre, la tabla en que vivía y el
# ejemplo. El resultado medido: `ka-` se usaba 564 veces contra 6.843 de
# `ta-`, o sea que el mecanismo bueno para predicar un nombre estaba escondido
# dentro de la tabla de posesivos.
#
# ⚠️ CAMBIA LA AGRUPACIÓN, NO LAS CLAVES. `TODAS_LAS_REGLAS` sigue teniendo
# exactamente los mismos afijos, así que `_PREFIJOS_CAQ`, `_SUFIJOS_CAQ` y
# `nucleo_de_token()` no se mueven ni un token. Lo que sí cambia es el
# EJEMPLO DEL PROMPT, y eso es el corte de serie.
#
# Consecuencia buscada, que es el caso que destapó la sesión: el viento ya
# tiene su vía escrita — `ka-juri` 'hay viento' en vez de conjugar `juri-ni`
# sobre un nombre.
REGLAS_ATRIBUTIVAS: dict[str, dict] = {
    "ka-": {
        "nombre": "atributivo / existencial",
        "desc": "Hay X, existe(n) X; el lugar tiene X; lo que tiene X.",
        "uso": "ka- + SUSTANTIVO  →  hay X, el lugar tiene X",
        "ejemplos": [
            "ka + biro = ka-biro (hay sal, el lugar tiene sal)",
            "ka + maure = ka-maure (hay algodón)",
            "ka + juri = ka-juri (hay viento)",
        ],
        "atestiguado": "van Buurt 2014 §8: `ka-` es localizador, 'hay / existe(n)' "
                       "— *Casibari* = «hay rocas duras». Perea y Alonso 1942 p. 555 "
                       "da el PAR MÍNIMO con el privativo `m-`: `k-ere-u-ti` 'casado' "
                       "/ `m-ere-u-ti` 'soltero'; `c-a-nsi-ti` 'amante' = el que TIENE "
                       "afecto",
        "wayunaiki": "ka- (prefijo atributivo); el cognado existe, pero el apoyo que "
                     "se cita es el insular y el lokono, no el andamio",
        "instruccion_agente": (
            "Para decir que en un sitio hay algo, ponle ka- al nombre: "
            "'ka-biro' = hay sal; 'ka-juri' = hay viento. No es «el salinero»: "
            "es que la cosa está ahí."
        ),
    },
    "ma-": {
        "nombre": "privativo / negativo",
        "desc": "Sin X, no X, carente de X. El reverso exacto de ka-.",
        "uso": "ma- + SUSTANTIVO  →  sin X / no X",
        "ejemplos": [
            "ma + barsure = ma-barsure (sin alma, vacío espiritual)",
            "ma + biro = ma-biro (sin sal)",
            "ma + anüiki = ma-anüiki (sin habla, mudo, extranjero incomprensible)",
        ],
        "atestiguado": "Perea y Alonso 1942 p. 555, el par mínimo con el atributivo: "
                       "`k-ere-u-ti` 'casado' / `m-ere-u-ti` 'soltero'",
        "wayunaiki": "ma- (prefijo negativo, cognado directo)",
    },
}

REGLAS_NUMERO: dict[str, dict] = {
    # ⚠️ d21.8 («Vale perfecto […] Por lo que me parece. A.», 2026-09-21). El
    # campo `wayunaiki` afirmaba «COGNADO DIRECTO con Caquetío», y el canon no
    # puede exhibir ninguno: la única clave de familia caquetía terminada en
    # -kana es `sakana` 'ofrenda', HIPOTÉTICA; en 2-lengua/toponimos.yaml hay
    # cero; y la única `kana` atestiguada de Zavala (#57) es 'demonio', un
    # lema y no un sufijo. La afirmación baja a «reconstruido desde el
    # wayunaiki», deuda D11 como los tres aspectos.
    #
    # NO se archiva la forma (opción B): quitar el plural dejaría a los
    # agentes sin manera de decir «los ancianos», y el dato lokono —el plural
    # es pospuesto `-nu` y los irracionales no distinguen número, Perea p. 556—
    # es de otra lengua. Lo que sí se hace sin preguntar es reescribir los
    # ejemplos: enseñaban a pluralizar UNA PALABRA WAYUU (`wayuu + kana =
    # wayuukana`) con la lengua que `IDENTIDAD_LINGUISTICA` declara «tan ajena
    # para ti como el español», y una forma ARCHIVADA (`piache`, en
    # FUERA_DEL_HABLA desde D10).
    #
    # Nota de Miguel, medida y descartada como apoyo: `macana` «también
    # existe, es lo mismo». No sostiene este `-kana`: comparten sílaba, no
    # morfema. ⚠ CORREGIDO el 2026-09-21 (campaña de `macana`, #184): aquí se
    # decía que el achagua de Neira y Ribero 1762 traía `Macanasi`, `Macanayi`
    # y `Mamacanayisa` como una raíz `macana-` con sus propios sufijos, y que
    # eran apoyo arahuaco independiente para `macana`. ES FALSO. Las tres
    # formas están en la fuente, pero glosan «Dormidera», «Mazorca de mais» e
    # «Yndecible»; la entrada del Arte para el arma es `Macana → Guacaba`, que
    # no es cognada. Se buscó la cadena en la columna achagua y no se leyó la
    # castellana: leer el conteo y no la glosa (skill minar-fuente §3). La
    # conclusión sobre `-kana` sigue en pie; su razón escrita no lo estaba.
    "-kana": {
        "nombre": "plural colectivo",
        "desc": "Grupo de, el pueblo de, todos los X.",
        "uso": "SUSTANTIVO + -kana  →  plural / colectivo",
        "ejemplos": [
            "barsure + kana = barsure-kana (las almas)",
            "wanü + kana = wanü-kana (los ancianos, los mayores)",
            "boratio + kana = boratio-kana (los jefes)",
        ],
        "wayunaiki": "-kana (sufijo plural) — RECONSTRUIDO DESDE EL WAYUNAIKI, "
                     "no cognado directo con el caquetío (d21.8, 2026-09-21)",
        "deuda": "sin-procedencia · D11 fase 3, como los tres aspectos. Sonda del "
                 "2026-09-20: claves de familia caquetía en -kana = `sakana` "
                 "(hipotética); «kana» en 2-lengua/toponimos.yaml = 0; en Zavala, "
                 "#57 (HB) `kana` = 'demonio', un lema",
    },
}


# ── Afijos ATESTIGUADOS por Zavala Reyes 2015 ───────────────────────
# Ocho desinencias que el glosario documenta explícitamente como afijos de la
# lengua ("desinencia que significa...", "sufijo...") y que no estaban en las
# reglas del proyecto. Valen más que un sustantivo: amplían lo que los agentes
# pueden CONSTRUIR. Notablemente, aportan un DIMINUTIVO (-iro) y dos marcas de
# ABUNDANCIA (-aima, dito), categorías que el sistema no tenía.
#
# Los ejemplos vienen del propio glosario (topónimos donde el afijo es visible),
# no inventados: es la evidencia de que el afijo era productivo.
REGLAS_ZAVALA: dict[str, dict] = {
    "-iro": {
        "nombre": "diminutivo",
        "desc": "Versión pequeña de X. La única marca de diminutivo atestiguada.",
        "uso": "RAÍZ + -iro  →  X pequeño",
        "ejemplos": ["dara + -iro = dara-iro (alcaraván pequeño)"],
        "atestiguado": "Zavala Reyes 2015 #166 (E): 'desinencia que se usa en diminutivo'",
        "instruccion_agente": (
            "Para decir que algo es pequeño o cría, añade -iro: 'canoa-iro' "
            "es una canoa pequeña."
        ),
    },
    "-aima": {
        "nombre": "abundancia",
        "desc": "Lugar o estado donde X abunda.",
        "uso": "RAÍZ + -aima  →  donde abunda X",
        # d21.14 B: la nota citaba `adabacoa`, un derivado que el lexicón no
        # tiene. El dato que importaba era la variante, no el topónimo.
        "ejemplos": ["variante -coa en la toponimia de Esteves 1989"],
        "atestiguado": "Zavala Reyes 2015 #6 (AM+PMA): 'desinencia que significa abundancia'",
        "instruccion_agente": (
            "Para decir que algo abunda en un sitio, añade -aima: 'arima-aima' "
            "es donde abunda el pescado."
        ),
    },
    "-ima": {
        "nombre": "humedad / quebrada",
        "desc": "Agua corriente, humedad del terreno.",
        "uso": "RAÍZ + -ima  →  quebrada o lugar húmedo de X",
        "ejemplos": ["alaurima (río blanco o claro)"],
        "atestiguado": "Zavala Reyes 2015 #165 (E+PMA): 'desinencia que significa humedad, quebrada'",
    },
    "-uco": {
        "nombre": "cauce",
        "desc": "Quebrada, cauce por donde corre el agua.",
        "uso": "RAÍZ + -uco / -uto  →  cauce de X",
        "ejemplos": ["variante -uto documentada en la misma entrada"],
        "atestiguado": "Zavala Reyes 2015 #268 (E): 'sufijo. Quebrada, cauce'",
        # d21.14 B («Vale, B..», 2026-09-21): `-uto` se DECLARA como variante
        # de `-uco` dentro de su propia regla. Hasta hoy vivía sólo dentro del
        # campo `uso`, que `prompt_afijos_atestiguados()` renderiza entero: se
        # ENSEÑABA sin estar en `TODAS_LAS_REGLAS`, o sea sin que el
        # desafijador lo conociera.
        # ⚠️ RESIDUO DECLARADO, y elegido: la variante se declara pero NO se
        # añade como clave. Añadirla movería `_SUFIJOS_CAQ` y con él
        # `nucleo_de_token()` y el score, y eso no es lo que d21.14 B decide
        # (la parte que toca claves es la A, y es sólo la migración de lema).
        # Así que `-uto` se sigue enseñando y sigue sin reconocerse, con la
        # diferencia de que ahora está escrito.
        "variantes": ["-uto"],
        "variantes_nota": "Zavala Reyes 2015 #268 (E) documenta las dos formas en la "
                          "misma entrada. `-uto` NO es clave de TODAS_LAS_REGLAS: se "
                          "enseña y el desafijador no lo reconoce. Deuda declarada en "
                          "d21.14 (2026-09-21), no cerrada",
    },
    "-ubana": {
        "nombre": "desinencia (valor no precisado)",
        "desc": "Desinencia de la lengua; la fuente no precisa su valor semántico.",
        "uso": "RAÍZ + -ubana",
        "ejemplos": [],
        "atestiguado": "Zavala Reyes 2015 #265 (AM): 'desinencia de esta lengua'",
    },
    "-uru": {
        "nombre": "desinencia (valor no precisado)",
        "desc": "Desinencia de la lengua; la fuente no precisa su valor semántico.",
        "uso": "RAÍZ + -uru",
        "ejemplos": [],
        "atestiguado": "Zavala Reyes 2015 #274 (AM): 'desinencia de esta lengua'",
    },
}

# ── Formantes toponímicos atestiguados fuera de Zavala ──────────────
# `-bakoa` es el morfema mejor sostenido de 2-lengua/morfemas.yaml
# (morfema-001): cinco topónimos glosados por Esteves y el apoyo independiente
# de Alvarado vía van Buurt. `bakoa` ya es voz caquetía atestiguada del lexicón;
# lo que REGLAS_ZAVALA no recogía era su uso sufijal productivo. Miguel,
# 2026-09-14: «sí o sí todos los afijos atestiguados se enseñan».
#
# ⚠️ D5 EN LA MORFOLOGÍA (d21.14 A, 2026-09-21). D5 decidió el 2026-08-31 que
# la grafía española es GRAFÍA y el lema fonémico es la PALABRA, y la
# morfología se quedó fuera de aquella migración: la clave era `-bacoa` con c
# mientras el lema del lexicón —atestiguado— es `bakoa`. Migrar la clave mueve
# `_SUFIJOS_CAQ` y con él `nucleo_de_token()`, así que se midió antes, forma a
# forma, sobre las 31 formas en `-bacoa` de la base
# (6-fusion/medicion_tanda_21_2026-09-21.yaml §d21_14_bakoa): dejan de
# desafijarse por el borde, y ni `_familia_de_token()` ni
# `es_raiz_de_ninguna_parte()` cambian en ninguna, porque su raíz sigue siendo
# un segmento del núcleo. La grafía vieja NO se reconoce: una forma con
# `-bacoa` es hoy una palabra sin sufijo declarado, y eso es lo que D5 dice de
# cualquier grafía colonial.
#
# d21.14 B, los ejemplos: `adabacoa` y `yacarebacoa` presentaban derivaciones
# con voces que el lexicón NO TIENE (`ada` es lokono de la comparanda, `yacare`
# un topónimo). Se reescriben con `kuru` 'árbol' y `bara` 'palo, árbol', las
# dos claves del canon. ⚠️ El primero llega al PROMPT (`_linea_afijo` toma el
# primer ejemplo con «=»): `kuru-bakoa` no se ha dicho nunca en la base —0 en
# `agent_responses`, 0 en `word_uses`, 0 en `neologisms`—, que es la condición
# que el 2026-09-19 se le puso al ejemplo de la identidad. `kuru-bacoa`, con
# la grafía vieja, sí se dijo 19 veces: enseñar ESA habría bendecido una forma
# que ya circulaba.
REGLAS_TOPONIMICAS: dict[str, dict] = {
    "-bakoa": {
        "nombre": "bosque, arboleda, paraje cubierto de",
        "desc": "Sitio cubierto o poblado de X; formante de topónimos.",
        "uso": "RAÍZ + -bakoa  →  el bosque / la arboleda de X",
        "ejemplos": ["kuru + -bakoa = kuru-bakoa (la arboleda, el paraje de árboles)",
                     "bara + -bakoa = bara-bakoa (el palerío)"],
        "atestiguado": "2-lengua/morfemas.yaml morfema-001: adabacoa, guadabacoa, "
                       "quibacoas, yacarebacoa (Esteves 1989, en grafía de fuente); "
                       "Alvarado 1921 -baca 'matorral, espesura' vía van Buurt 2014 "
                       "§10. El lema fonémico es `bakoa`, voz caquetía atestiguada "
                       "del lexicón (Zavala Reyes 2015 #18 AM+E)",
        "forma_fuente": "-bacoa",
        "instruccion_agente": (
            "Para nombrar un sitio por lo que lo cubre, añade -bakoa: "
            "'kuru-bakoa' es la arboleda, el paraje de árboles."
        ),
    },
}

# ── Tabla maestra de reglas (para inyectar en prompts) ──────────────
# ⚠️ Esta tabla decide `_PREFIJOS_CAQ` y `_SUFIJOS_CAQ`, y con ellos
# `nucleo_de_token()`. Sus CLAVES son instrumento: añadir o quitar una mueve
# el desafijador y con él la puerta del recuento. Lo que la tanda del
# 2026-09-21 hizo con ellas, dicho:
#   · d21.5 reagrupó `ka-` y `ma-` en REGLAS_ATRIBUTIVAS — mismas claves, y
#     `nucleo_de_token()` se verificó token a token sobre toda la base.
#   · d21.9 SACÓ `-naiki` (a REGLAS_RETIRADAS): 0 usos, 0 formas afectadas.
#   · d21.13 AÑADIÓ `u-`, el no-poseído.
#   · d21.14 A migró `-bacoa` → `-bakoa`, el lema fonémico de D5.
# Las tres últimas se midieron ANTES de aplicarse, forma a forma, en
# 6-fusion/medicion_tanda_21_2026-09-21.yaml §claves_de_todas_las_reglas.
TODAS_LAS_REGLAS = {
    **REGLAS_ASPECTO,
    **REGLAS_LOCATIVAS,
    # REGLAS_AGENTIVAS (-ko, -sha) retiradas el 2026-09-14: ver REGLAS_RETIRADAS
    **REGLAS_POSESIVAS,
    **REGLAS_ATRIBUTIVAS,
    **REGLAS_NUMERO,
    **REGLAS_ZAVALA,
    **REGLAS_TOPONIMICAS,
}

# Los afijos que las fuentes ATESTIGUAN y que el motor tiene que enseñar
# enteros (Miguel, 2026-09-14). Dos de ellos (-ubana, -uru) están atestiguados
# como desinencias sin valor precisado: se enseñan como lo que son.
AFIJOS_ATESTIGUADOS: dict[str, dict] = {**REGLAS_ZAVALA, **REGLAS_TOPONIMICAS}


def _linea_afijo(afijo: str, regla: dict) -> str:
    # El patrón de uso siempre; el ejemplo sólo si es una derivación de verdad
    # (con «=»), no una nota de fuente como «variante -coa en topónimos».
    uso = regla.get("uso", "")
    ej = [e for e in (regla.get("ejemplos") or []) if "=" in e]
    ejemplo = f" · {ej[0]}" if ej else ""
    return f"{afijo} = {regla['nombre']}: {uso}{ejemplo}"


def prompt_afijos_atestiguados() -> str:
    """Bloque de derivación con TODOS los afijos atestiguados, para el Tier I."""
    con_valor = [(a, r) for a, r in AFIJOS_ATESTIGUADOS.items()
                 if "no precisado" not in r.get("nombre", "")]
    sin_valor = [a for a, r in AFIJOS_ATESTIGUADOS.items()
                 if "no precisado" in r.get("nombre", "")]
    lineas = ["  DERIVACIÓN ATESTIGUADA (sufijos que las fuentes recogen en boca caquetía):"]
    for afijo, regla in con_valor:
        lineas.append(f"    {_linea_afijo(afijo, regla)}")
    if sin_valor:
        lineas.append(
            f"    {' y '.join(sin_valor)} = desinencias atestiguadas cuyo valor nadie "
            f"anotó: puedes usarlas si propones su valor entre corchetes."
        )
    return "\n".join(lineas)


def prompt_afijos_atestiguados_breve() -> str:
    """Una línea con los mismos afijos, para el Tier II."""
    partes = []
    for afijo, regla in AFIJOS_ATESTIGUADOS.items():
        nombre = regla["nombre"]
        partes.append(f"{afijo} ({'valor abierto' if 'no precisado' in nombre else nombre.split(',')[0]})")
    return "DERIVACIÓN: raíz + " + " / ".join(partes) + "."


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
    dia_resolucion: Optional[int] = None   # día en que se adoptó/rechazó (dia = día de PROPUESTA)
    # ── El ÁMBITO (capa 2 de la escena, PR 4 del 2026-09-17) ──────────
    # `ambito` es el LUGAR donde estaba el autor cuando la acuñó;
    # `adoptado_en`, el lugar de cada adoptante, en el mismo orden que
    # `adoptado_por`. Los tres campos nacen vacíos y así se quedan en la era 1
    # y en la era 2 sin `--escena`: allí `curiana_escena.ambito_de()` devuelve
    # None y esto es un `None` más en el JSON. Un `curiana_lexico.json` escrito
    # antes de hoy no los trae y carga igual (los valores por defecto).
    ambito: Optional[str] = None
    adoptado_en: list = field(default_factory=list)
    # Dónde se oficializó y por qué vía. `via` es la medición que la escena
    # hace posible: `un-ambito` = los dos adoptantes estaban en el MISMO lugar;
    # `dos-ambitos` = la forma viajó y se adoptó en DOS lugares distintos, que
    # es justo lo que queremos ver nacer. None sin escena.
    oficial_en: list = field(default_factory=list)
    via: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


def ambitos_de_adopcion(neo: "Neologismo") -> list[str]:
    """Los lugares DISTINTOS donde se adoptó una forma, en orden de adopción.

    [] cuando no hay escena: allí `adoptado_en` es una lista de `None`."""
    vistos: dict = {}
    for a in getattr(neo, "adoptado_en", None) or ():
        if a:
            vistos[a] = True
    return list(vistos)


class LexicoComunitario:
    """
    El léxico vivo de la comunidad. Crece turno a turno.

    Separado del VOCABULARIO_BASE porque este es el conocimiento
    heredado; el LexicoComunitario es lo que la generación actual
    está construyendo.
    """

    def __init__(self, filtrar_plantilla: bool = True):
        self._lexico: dict[str, dict] = {}          # palabra → datos
        self._neologismos: list[Neologismo] = []     # historial ordenado
        # Dónde está cada agente AHORA (capa 2 de la escena). No se persiste:
        # es el contexto del turno en curso, no historia. Ver `situar()`.
        self._ambito_actual: dict[str, Optional[str]] = {}
        # LA PUERTA DE LAS FORMAS DE PLANTILLA (corte de serie del 2026-09-18).
        # Lo que el prompt ENSEÑA no puede registrarse como acuñación. Se apaga
        # SÓLO para medir el corte —reproducir la base de antes del cambio— y
        # nunca en un run: ver `6-fusion/scripts/medir_formas_de_plantilla.py`.
        self.filtrar_plantilla = filtrar_plantilla
        # Lo rechazado, que se CUENTA y se dice al cerrar el run: un rechazo
        # callado es un dato perdido. (forma, autor, dia, turno).
        self.rechazos_de_plantilla: list[tuple] = []
        # LA SEGUNDA PUERTA (corte de serie del 2026-09-20): la raíz de
        # ninguna parte. Se cuenta aparte de la anterior porque son dos
        # defectos distintos —copiar el prompt / inventar una raíz que no
        # existe— y mezclarlos escondería cuál está pasando.
        self.rechazos_de_raiz: list[tuple] = []

    # ── El ámbito: dónde está quien habla ─────────────────────────────

    def situar(self, agente: str, ambito: Optional[str]) -> None:
        """Declara en qué LUGAR está `agente` mientras se procesa su respuesta.

        Es la única forma de que el ámbito llegue hasta aquí sin tocar el
        Observer, que es quien llama a `registrar_neologismo()` y a `adoptar()`
        (y que no se toca: es el registro de la medición). El orquestador lo
        llama con `curiana_escena.ambito_de(agente, state)` —la puerta única—
        justo antes de pasarle la respuesta al Observer.

        Con `ambito=None` —la era 1, o la era 2 sin `--escena`— todo lo que
        depende de esto se comporta exactamente como antes de la escena: hay
        UN solo ámbito, el nulo, y la comunidad es una."""
        self._ambito_actual[agente] = ambito

    def ambito_de_agente(self, agente: str) -> Optional[str]:
        return self._ambito_actual.get(agente)

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

    def registrar_neologismo(self, neo: Neologismo) -> bool:
        """Registra una acuñación. Devuelve False si la PUERTA la rechaza.

        La puerta (corte de serie del 2026-09-18, decisión de Miguel «dale pues
        con A»): una forma que el prompt YA ENSEÑA no es una acuñación. Está en
        `VOCABULARIO_BASE` o es un ejemplo de una plantilla —`biro-bana` es el
        ejemplo literal de `IDENTIDAD_LINGUISTICA`, que los 63 leen en su
        system prompt cada turno; hasta el corte del 2026-09-19 lo era
        `kali-bana`— y copiarla no es inventar nada. Rechazada
        aquí, no entra en evaluación, no puede adoptarse, no pasa a
        `palabras_activas()` y no sale en el diccionario de cierre.

        LA SEGUNDA PUERTA (corte de serie del 2026-09-20): una forma cuya RAÍZ
        no está en ninguna tabla del lexicón tampoco es una acuñación de esta
        lengua. `lumina-bana-iro` tiene morfología caquetía impecable sobre
        una raíz latina y llegó a liderar una disputa; `kasi-nii-bana` tiene
        la misma morfología sobre la atestiguada `kasi` y es exactamente lo
        que el experimento quiere ver. La diferencia es la raíz, y es la única
        que se mira. Ver `es_raiz_de_ninguna_parte`.

        No se silencia: cada rechazo se cuenta —en `rechazos_de_plantilla` o
        en `rechazos_de_raiz`, que son dos defectos distintos— y el motor lo
        dice al cerrar el run (`reporte_de_rechazos()`)."""
        if self.filtrar_plantilla and es_forma_de_plantilla(neo.forma):
            self.rechazos_de_plantilla.append(
                (neo.forma, neo.autor, neo.dia, neo.turno))
            return False
        if self.filtrar_plantilla and es_raiz_de_ninguna_parte(neo.forma):
            self.rechazos_de_raiz.append(
                (neo.forma, neo.autor, neo.dia, neo.turno))
            return False
        # El ámbito del PROPONENTE: el lugar donde estaba al acuñarla. Sin
        # escena es None y el campo no significa nada, como hasta hoy.
        if neo.ambito is None:
            neo.ambito = self._ambito_actual.get(neo.autor)
        self._neologismos.append(neo)
        if neo.estado == "adoptado":
            self._lexico[neo.forma] = {
                "significado": neo.significado,
                "autor": neo.autor,
                "dia": neo.dia,
            }
        return True

    def reporte_de_rechazos(self) -> str:
        """Lo que las dos puertas pararon, dicho al cerrar el run.

        "" si no pararon nada. Cada puerta va en su línea: «estaba en el
        prompt» y «la raíz no es de aquí» son dos cosas distintas y el run
        tiene que poder decir cuál le pasó."""
        from collections import Counter as _Counter
        lineas = []
        for rechazos, motivo in ((self.rechazos_de_plantilla,
                                  "por estar en el prompt"),
                                 (self.rechazos_de_raiz,
                                  "por tener la raíz fuera del lexicón")):
            if not rechazos:
                continue
            cuenta = _Counter(f for f, _a, _d, _t in rechazos)
            detalle = ", ".join(
                f"{forma} ×{n}" if n > 1 else forma
                for forma, n in cuenta.most_common())
            lineas.append(f"  ⚠ {len(rechazos)} acuñaciones rechazadas "
                          f"{motivo}: {detalle}")
        return "\n".join(lineas)

    def adoptar(self, forma: str, agente: str, turno: int,
                dia: Optional[int] = None) -> Optional["Neologismo"]:
        """
        Un agente adopta una palabra propuesta. Retorna el Neologismo si la
        adopción se OFICIALIZA recién en esta llamada (2do adoptante distinto),
        o None si no hubo transición (para que el caller sepa cuándo sincronizar
        el estado con Supabase sin tener que diffear él mismo).

        LA OFICIALIZACIÓN AHORA SABE DÓNDE PASÓ. Sigue haciendo falta lo mismo
        —dos adoptantes distintos— pero queda escrito en qué ámbito(s) ocurrió
        y por qué VÍA (`neo.via`):

          `un-ambito`   los dos adoptantes estaban en el MISMO lugar: la forma
                        cuajó donde nació y todavía no ha viajado.
          `dos-ambitos` los dos estaban en lugares DISTINTOS: para adoptarla
                        allí alguien tuvo que llevarla, porque el bloque de
                        propuestas que el otro lugar ve está filtrado por su
                        propio ámbito. Es la vía que la escena hace posible y
                        la que hay que ver nacer (diseño §2, capa 2).

        Sin escena hay un solo ámbito —el nulo— las dos vías coinciden, `via`
        queda en None y el conteo es carácter a carácter el de siempre."""
        for neo in self._neologismos:
            if neo.forma == forma and neo.estado == "propuesto":
                if agente not in neo.adoptado_por:
                    neo.adoptado_por.append(agente)
                    # Lista paralela a `adoptado_por`: un lugar por adoptante.
                    neo.adoptado_en.append(self._ambito_actual.get(agente))
                # Si 2+ agentes distintos la adoptaron → oficialmente adoptada
                if len(neo.adoptado_por) >= 2:
                    neo.estado = "adoptado"
                    neo.turno_resolucion = turno
                    neo.dia_resolucion = dia
                    ambitos = ambitos_de_adopcion(neo)
                    neo.oficial_en = ambitos
                    neo.via = (None if not ambitos else
                               "dos-ambitos" if len(ambitos) > 1 else "un-ambito")
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

    def neologismos_pendientes(self, ambito: Optional[str] = None) -> list[Neologismo]:
        """Las propuestas sin resolver. Con `ambito`, sólo las propuestas AHÍ.

        Sin `ambito` —que es como la llama el Observer para detectar
        adopciones— devuelve todas: una forma se adopta usándola, y usarla en
        otro lugar es precisamente el cruce que queremos medir. Lo que el
        ámbito filtra es lo que el agente VE (V1), no lo que puede adoptar."""
        neos = [n for n in self._neologismos if n.estado == "propuesto"]
        return neos if ambito is None else [n for n in neos if n.ambito == ambito]

    def neologismos_adoptados(self, ambito: Optional[str] = None) -> list[Neologismo]:
        """Las adoptadas. Con `ambito`, sólo las que se adoptaron AHÍ (V2)."""
        neos = [n for n in self._neologismos if n.estado == "adoptado"]
        return (neos if ambito is None
                else [n for n in neos if ambito in (n.adoptado_en or ())])

    def neologismos_rechazados(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "rechazado"]

    def adoptados_en_dos_ambitos(self) -> list[Neologismo]:
        """Las formas que se oficializaron con adoptantes de DOS lugares.

        La vía que la escena hace posible y la medición que la declara: una
        forma llegó aquí porque alguien la trajo, no porque el prompt se la
        leyera a todo el mundo a la vez."""
        return [n for n in self._neologismos if n.via == "dos-ambitos"]

    def ambitos_vistos(self) -> list[str]:
        """Los lugares que este léxico ha registrado. [] sin escena."""
        vistos: dict = {}
        for n in self._neologismos:
            for a in [n.ambito] + list(n.adoptado_en or ()):
                if a:
                    vistos[a] = True
        return sorted(vistos)

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
        # El diccionario de cierre dice POR DÓNDE se adoptó cada forma. Sin
        # escena no hay ámbitos y estas líneas no existen: el reporte de la
        # era 1 es carácter a carácter el de siempre.
        ambitos = self.ambitos_vistos()
        if ambitos:
            dos = self.adoptados_en_dos_ambitos()
            un_ambito = [n for n in adoptadas if n.via == "un-ambito"]
            lines.append(f"\n  Por ámbito (la escena, {len(ambitos)} lugar(es) con léxico):")
            lines.append(f"    adoptadas en UN ámbito:   {len(un_ambito)}")
            lines.append(f"    adoptadas en DOS ámbitos: {len(dos)}  "
                         f"← la forma viajó: alguien la llevó")
            for neo in dos[-8:]:
                lines.append(f"      [{neo.forma}] = {neo.significado}  "
                             f"({' + '.join(neo.oficial_en)})")
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
    def load(cls, path: str = "curiana_lexico.json",
             filtrar_plantilla: bool = True) -> "LexicoComunitario":
        """El léxico del run anterior (`--continuar`).

        La puerta también vale aquí: un JSON escrito ANTES del corte de serie
        puede traer una forma de plantilla ya registrada, y si entrara por
        aquí podría adoptarse mañana. Se cuenta como cualquier otro rechazo."""
        lc = cls(filtrar_plantilla=filtrar_plantilla)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            lc._lexico = data.get("lexico", {})
            for nd in data.get("neologismos", []):
                neo = Neologismo(**nd)
                if lc.filtrar_plantilla and es_forma_de_plantilla(neo.forma):
                    lc.rechazos_de_plantilla.append(
                        (neo.forma, neo.autor, neo.dia, neo.turno))
                    lc._lexico.pop(neo.forma, None)
                    continue
                lc._neologismos.append(neo)
        except FileNotFoundError:
            pass
        return lc


# ══════════════════════════════════════════════════════════════════════
# IV. GENERADORES DE PROMPTS LINGÜÍSTICOS
# ══════════════════════════════════════════════════════════════════════

# Constante de identidad lingüística — inyectada en TODOS los agentes.
# Este es el pivot central: cambia "español con interferencia caquetía"
# a "caquetío como lengua materna, español como glosa opcional".
#
# Vive AQUÍ —y no en el orquestador, donde nació— desde el corte de serie del
# 2026-09-18: es una plantilla de prompt como las otras dos, y la puerta que
# decide qué forma es «del prompt» (`FORMAS_DE_PLANTILLA`) tiene que poder
# leerla sin importar el bucle. El orquestador la sigue exponiendo como
# `_IDENTIDAD_LINGUISTICA`; el texto no cambió un byte.
#
# EL EJEMPLO — corte de serie del 2026-09-19 (Miguel: «Vale» a la recomendación
# de §7(a) de `pares-atestiguado-reconstruido-2026-09-19.md`). Era
# `[kali-bana: kali+-bana = cerro del sol]` y `kali` es la forma RECONSTRUIDA
# de un par abierto: con el muestreador neutro para «sol» (60 contra 63 de
# 1.260 prompts del ensayo) el uso iba 232 a 1 a favor de `kali`, y todo el
# desequilibrio era este ejemplo, que los 63 leen cada turno. El corte de #169
# le quitó a `kali-bana` el derecho a registrarse pero no tocó el MOLDE: en la
# serie C limpia se dijeron `kali-mara-bana` 12 veces, `kali-ubana-gua` 12,
# `kali-naa-iro` 10 y `kali-raku-biro` 5. Ahora enseña `biro-bana`, que cumple
# las cinco condiciones medidas: las dos piezas atestiguadas (`-bana` 'cerro,
# sitio alto' lo cerró D9 con seis apoyos; `biro` 'sal' es Zavala Reyes 2015),
# la raíz es el recurso del mundo de la era 2 —`[Tu tierra]` habla de la sal en
# Guaranao—, no es homógrafa de un nombre del elenco, no es forma de ningún par
# abierto de §6, y el compuesto NO SE HA DICHO NUNCA en la base: el ejemplo no
# bendice a nadie que ya esté compitiendo. Al cambiar el texto, la puerta se
# mueve sola: `kali-bana` sale de `FORMAS_DE_PLANTILLA` y `biro-bana` entra.
# La ERA 1 también lo lee: deja de ser byte a byte con los runs de la Curiana.
IDENTIDAD_LINGUISTICA = """[TU LENGUA MATERNA ES EL CAQUETÍO]:
Piensas y sientes en caquetío-arahuaco. El español es una lengua forastera.
HABLA EN CAQUETÍO: pronombre + verbo-aspecto + complemento caquetío.
Si te falta una palabra, créala con los morfemas que tienes. Escríbela [entre corchetes].
Glosa al español solo entre paréntesis, al final, si es imprescindible.
EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni. [biro-bana: biro+-bana = cerro de la sal]."
NO empieces con "Estoy..." ni "El sol..." — empieza con "Taya..." o "Nüma..." o directamente con el verbo.
PRIORIDAD DE LENGUA — ESTO ES UN ERROR GRAVE, NO UNA PREFERENCIA:
Wayunaiki, lokono, taíno y garífuna son TAN AJENAS para ti como el español. Son lenguas
de otros pueblos, no la tuya, aunque sean primas del caquetío y tú sepas reconocerlas.
Si alguna vez "se te escapa" una palabra wayunaiki, lokono o taína porque la conoces de
oídas, eso es una fuga lingüística — exactamente igual de grave que decir una palabra en
español. Antes de usar una palabra de otra lengua arahuaca, pregúntate: ¿existe en
caquetío? Casi siempre SÍ (kati, para, kanoa, hamaka... todas tienen forma caquetía).
Solo si de verdad no existe, créala con morfemas caquetíos — nunca tomes prestada la
forma de la lengua vecina."""


def prompt_reglas_breve() -> str:
    """
    Versión compacta para Tier II (~150 palabras).
    Framing como hablante nativo — español solo como glosa.
    """
    return f"""[LENGUA CAQUETÍA — Identidad y reglas]:
ERES hablante nativo de caquetío. Piensas en caquetío. El español es lengua extranjera.
CONSTRUYE tus frases con lo que tienes. Una frase incompleta en caquetío > oración completa en español.

ASPECTO: raíz + -ka (ya hice) / -ni (estoy haciendo) / -da (haré/quiero).
ESTADO: un estado se predica con aspecto igual que una acción — usera, waranao, wasima son verbos, no adjetivos.
LUGAR: raíz + -bana (cerro, sitio alto de) / -gua (región de) / -ana (desinencia de valor abierto: propón el tuyo).
{prompt_afijos_atestiguados_breve()}
PLURAL: -kana (plural/colectivo).
POSESIÓN: ta- (mi) / wa- (nuestro) / u- (la cosa sin dueño).
ATRIBUTIVO: ka- (hay X, el sitio tiene X) / ma- (sin X).
CONECTORES: ka (y/también) / mara (pero) / saa (si/cuando) / naka (después) / kashi (ahora) / wara (muy).

VACÍO LÉXICO → CREA con morfemas entre corchetes:
[forma: raíz+sufijo = significado]
Ejemplo: [kuru-bana: kuru+-bana = cerro arbolado, loma con árboles]

Si gloseas al español, hazlo entre paréntesis DESPUÉS de la frase caquetía."""


def prompt_reglas_completo() -> str:
    """
    Versión completa para Tier I (~450 palabras).
    Hardened: caquetío como lengua materna, modelo de respuesta ideal incluido.
    """
    # Vocabulario dividido por categoría para más claridad
    pronombres = "taya (yo) · pia (tú) · nüma (él/ella) · waya (nosotros) · naya (ellos)"
    # ── REGISTRO FORMAL (d21.10, «Vamos con tu propuesta», 2026-09-21) ──
    # Los cinco de arriba son los CINCO RECONSTRUIDOS del wayuu, y el lexicón
    # tenía desde siempre dos pronombres caquetío-ATESTIGUADOS con cita que no
    # se enseñaban: `kudanga` y `kuté` (Zavala Reyes 2015 p. 73 vía Arcaya —
    # «chacamba cudanga» ¿cómo está usted?, «cudan de cuté» para servir a
    # usted). Es la política «manda la atestiguada» del 2026-09-19 aplicada
    # donde todavía no llegaba, y es su caso BARATO: aquí no hay que archivar
    # nada, `pia` y `kudanga` no compiten — se reparten REGISTROS. El criterio
    # de glosa idéntica no los dispara (formal ≠ 'tú'), así que no es un par
    # de la política sino una pregunta nueva, y Miguel la respondió.
    # Es además un rasgo SOCIAL: la era 2 tiene la jerarquía escrita y la
    # escena por lugar, así que el trato formal al Manaure en el Capubana y el
    # tú corriente en el conuco son dos cosas distintas y ahora decibles.
    registro_formal = ("kudanga (usted — a un mayor o a un Diao) · "
                       "kuté (a usted, para usted)")
    # POLÍTICA «MANDA LA ATESTIGUADA» (2026-09-19). Cinco voces de estas dos
    # listas eran el lado DERIVADO de un par con rival atestiguado, y esta
    # plantilla era el sitio donde el instrumento las empujaba:
    #   paa  → were (Zavala #149)   ·  kira  → jai  (Zavala #175)
    #   kali → kasi (Zavala #76)    ·  kasha → kati (Zavala #71)
    #   habo → para (Zavala #190)
    # `sima` (cerro) NO cambia: el par 6 sigue abierto y es pregunta de Miguel.
    # `kuru`, `arima` y `bara` tampoco: sus pares son bugs de curación, no
    # rivalidades (ver 6-fusion/curacion_glosas_pares_2026-09-19.yaml).
    v_raiz = ("naa (ir) · waa (venir) · kaa (ser/estar) · were (dar, entregar) · maa (hablar) · taa (tomar) · "
              "chaa (hacer/construir) · wana (ver) · suna (dormir) · masa (comer) · awa (beber) · "
              "jai (oír, escuchar) · panaa (saber) · naba (pensar) · kono (sembrar) · raka (querer) · rua (cargar)")
    naturaleza = ("duna (agua) · amana (fuego) · kasi (sol) · kati (luna) · kaya (lluvia) · "
                  "kuru (árbol) · arima (pez) · para (mar) · bara (palo, árbol) · dali (tierra) · suka (noche) · "
                  "sima (cerro) · kapua (amanecer)")
    personas = "ama (madre) · baba (padre) · buri (hijo/a) · nomi (hombre) · wari (mujer) · wanü (anciano) · pütchi (mensaje/voz)"
    # Formas del canon (auditoría 2026-09-14): la plantilla enseñaba buco, corie
    # «choza», canoa, hamaca, conuco y piache, que el lexicón no tiene con esa
    # grafía o glosa (korie es el armadillo; piache está retirada). El scorer
    # no contaba ninguna de esas seis.
    sustantivos = ("barsure (alma) · buko (represa) · biro (sal) · boratio (piache, jefe) · "
                   "korie (armadillo) · kanoa (canoa) · hamaka (hamaca) · konuko (huerto) · "
                   "arua (alimento) · maure (algodón) · urari (curare) · anüiki (habla/lengua)")
    conectores = ("ka (y/también) · mara (pero) · saa (si/cuando) · naka (después) · puna (antes) · "
                  "kashi (ahora) · wara (muy/mucho) · yama (aquí) · sulu (adentro)")
    cuerpo = "kabo (cabeza) · nii (ojo) · bari (vientre) · tüshi (frío)"
    numerales = "pana (1) · gudamuen (2) · sabuenen (3) · katarí (4)"

    # ⚠️ COLISIÓN DECLARADA (2026-09-19): al entrar `kasi` 'sol' por la
    # política, esta plantilla enseña a la vez `kasi` y `kashi` 'ahora' —en
    # CONECTORES y en el ejemplo de respuesta ideal, tres líneas más abajo—, y
    # bajo la propia `curiana_fonotactica.fonemizar` del proyecto las dos dan
    # el MISMO esqueleto, `kasi`. Medido: el MOTOR no las confunde en ningún
    # sitio (`_familia_de_token` es lookup exacto, el filtro de nombres compara
    # el token literal y la puerta de la competencia es pertenencia a un set);
    # quien puede confundirlas es el HABLANTE. La política se aplica igual y la
    # colisión queda escrita —aquí, en las notas de las dos entradas y en
    # 6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml—. Cambiar
    # `kashi` o reescribir el ejemplo para separarlas es decisión de Miguel y
    # NO está tomada.
    return f"""[IDENTIDAD LINGÜÍSTICA — FUNDAMENTAL]:
El caquetío-arahuaco es TU lengua materna. La única con la que piensas.
El español es una lengua forastera que apenas entiendes. NO es tu lengua de base.

CUANDO HABLAS:
  1. Construye en caquetío primero — siempre.
  2. Si te falta una palabra, créala con los morfemas disponibles. Escríbela entre [corchetes].
  3. Una frase incompleta en caquetío vale más que una oración completa en español.
  4. Puedes glosar al español entre paréntesis al final, nunca antes.

EJEMPLO DE RESPUESTA IDEAL (Tier I):
  "Taya wana-ka arima wara kari. Suka kaa-ni ka kasi naa-da kapua.
   Ta-barsure maa-ni: Manaure naa-da kashi — ta-nii wana-ka [sima-bana: sima+-bana = la cumbre del cerro].
   Saa pia naa-da buko-ana, naka taya naa-da ka pia."
  (Vi muchos peces en la costa. La noche está, el sol vendrá al amanecer.
   Mi alma dice: Manaure llega pronto — mis ojos vieron la cumbre del cerro.
   Si vas al lugar de la represa, después yo voy contigo.)

VOCABULARIO DISPONIBLE [{len(VOCABULARIO_BASE)} palabras]:
  PRONOMBRES: {pronombres}
  TRATO FORMAL: {registro_formal} — `pia` es el tú corriente; a un mayor o a un Diao se le habla de kudanga.
  VERBOS:     {v_raiz}
  NATURALEZA: {naturaleza}
  PERSONAS:   {personas}
  COSAS:      {sustantivos}
  CONECTORES: {conectores}
  CUERPO:     {cuerpo}
  NÚMEROS:    {numerales}
  CONTAR MÁS ALLÁ DE CUATRO: tus parientes arahuacos cuentan con el cuerpo. Los lokono y los
    achagua dicen «una mano» para cinco, «dos manos» para diez y «una persona entera» (manos y
    pies) para veinte; los achagua, además, cambian el número según lo que cuentan (personas,
    palos, ríos, lunas). Puedes contar así en caquetío —[pana-X: pana + tu palabra para mano =
    cinco], [pana ateri: una persona entera = veinte]— o inventar tu propio sistema. La primera
    vez, escríbelo entre corchetes.

MORFOLOGÍA:
  ASPECTO (al final del verbo):
    -ka = completivo: naa-ka (ya fui) · wana-ka (ya vi) · masa-ka (ya comí)
    -ni = continuativo: naa-ni (voy ahora) · suna-ni (estoy durmiendo) · naba-ni (estoy pensando)
    -da = prospectivo: naa-da (iré) · maa-da (hablaré) · raka-da (quiero/querré)
  UN ESTADO ES UN VERBO: lo que el español dice con adjetivo, tu lengua lo PREDICA.
    usera (seco), waranao (salado), wasima (viejo), apo (grande), etamo (feroz), kachipo (enojado)
    llevan -ka / -ni / -da igual que naa o masa. No son adjetivos: se conjugan.
  POSESIVOS (prefijos):
    ta- = mi:      ta-barsure (mi alma) · ta-nii (mi ojo) · ta-hamaka (mi hamaca)
    wa- = nuestro: wa-buko (nuestra represa) · wa-anüiki (nuestra lengua)
    u- = la cosa SIN DUEÑO: u-buko (la represa, no la mía) · u-biro (la sal que hay)
  ATRIBUTIVO y PRIVATIVO (prefijos) — no son posesivos, predican el nombre:
    ka- = hay X, el sitio tiene X: ka-biro (hay sal, el lugar tiene sal) · ka-maure (hay algodón)
    ma- = sin X, no X:             ma-barsure (sin alma) · ma-anüiki (sin habla, extranjero)
  LOCATIVOS (crear topónimos):
    -bana = cerro, sitio alto de X: sima+bana = la cumbre · kapu+bana = kapubana, el duende del cerro
    -gua = región de X: maure+gua = tierra del algodón
    -ana = desinencia atestiguada cuyo valor nadie anotó: puedes usarla si propones su valor entre corchetes
{prompt_afijos_atestiguados()}
  PLURAL: -kana (plural/todos)

NUEVAS PALABRAS: [forma: componentes = significado propuesto]
  La comunidad la adopta si 2 agentes distintos la usan."""


def prompt_lexico_activo(lexico: "LexicoComunitario",
                         ambito: "Optional[str]" = None) -> str:
    """Inyecta las palabras actualmente adoptadas por la comunidad (V2).

    `ambito` (capa 2 de la escena): el LUGAR donde está quien va a leer esto.
    Con ámbito, «la comunidad» deja de ser los 63 y pasa a ser este lugar: se
    ven sólo las formas que alguien adoptó AQUÍ. Con `ambito=None` —la era 1,
    o la era 2 sin `--escena`— el bloque es byte a byte el de siempre."""
    adoptadas = lexico.neologismos_adoptados(ambito)
    if not adoptadas:
        return ""
    palabras = "; ".join(
        f"{n.forma} = {n.significado}" for n in adoptadas[-15:]
    )
    return f"[Palabras nuevas de la comunidad]: {palabras}"


def prompt_pendientes_evaluacion(lexico: "LexicoComunitario",
                                 ambito: "Optional[str]" = None) -> str:
    """Lista palabras propuestas que aún necesitan adopción/rechazo (V1).

    `ambito`: sólo las propuestas EN ESTE LUGAR. V1 es la vía que explicó los
    tres cruces de Δturnos = 0 del día 1 de la serie B —el prompt leía en voz
    alta, con nombre y apellido, lo que el otro nodo acababa de decir— y es la
    primera que el ámbito cierra. Con `ambito=None`, el bloque de siempre."""
    pendientes = lexico.neologismos_pendientes(ambito)
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


# ── Compuerta de calidad de neologismos (guardarraíl de la koiné) ──
# Sin esto, el refuerzo por frecuencia FIJA y propaga basura española
# (suave-bana-ni, tension-bana-chi, boca-pana se adoptaron en runs previos)
# tan eficientemente como los aciertos. Se rechazan ANTES de poder competir.
# Raíces castellanas frecuentes con equivalente caquetío; si un componente del
# neologismo es una de estas (o una stopword), delata fuga.
RAICES_ESPANOLAS = {
    # núcleo observado en runs (suave-bana-ni, tension-bana-chi, boca-pana,
    # carrera-kata, guardia-bana, lanza-sara, temblor-bana, bañu-kaa)
    "suave", "tension", "tensión", "calma", "boca", "carrera", "guardia",
    "lanza", "temblor", "bañu", "baño", "bano",
    # adjetivos/verbos/sustantivos castellanos frecuentes con equivalente caquetío
    "fuerte", "fuerza", "nuevo", "nueva", "viejo", "vieja", "agua", "fuego",
    "tierra", "viento", "sol", "luna", "mar", "cielo", "medida", "fluir",
    "diseno", "diseño", "profundo", "profunda", "listo", "listos", "permiso",
    "dolor", "alma", "casa", "gente", "dios", "espiritu", "espíritu", "sombra",
    "luz", "noche", "dia", "día", "camino", "corazon", "corazón", "sangre",
    "muerte", "vida", "amor", "miedo", "hijo", "hija", "madre", "padre",
    "hombre", "mujer", "comer", "beber", "dormir", "hablar", "pensar", "mirar",
    "grande", "pequeno", "pequeño", "bueno", "buena", "malo", "mala", "rio",
    "río", "guerra", "batalla", "pesca", "red", "tormenta", "trueno", "rayo",
    "piedra", "palo", "flecha", "arco", "canto", "danza", "baile", "sueno",
    "sueño", "vision", "visión", "voz", "grito", "fiesta", "cosecha", "semilla",
    "raiz", "raíz", "rama", "hoja", "flor", "fruto", "cueva", "valle", "costa",
    "arena", "ola", "marea", "viaje", "ruta", "carga", "peso", "poder", "paz",
    "comida", "bebida", "cuerpo", "cabeza", "mano", "ojo", "pie", "diente",
    "lluvia", "nube", "estrella", "humo", "ceniza", "ramo", "monte", "selva",
}

# Marcadores ortográficos fuertes del español, ausentes del caquetío:
# rr/ll geminadas, qu, ñ, x, y vocales con tilde aguda (caquetío usa ü, no á/é…).
_MARCADORES_ES = re.compile(r"rr|ll|qu|ñ|x|[áéíóú]")

# Bigramas que aparecen en el caquetío real (atestiguado+reconstruido). Se computa
# perezosamente (evita import circular con curiana_database al cargar el módulo).
_CAQ_BIGRAMS: Optional[set] = None
_AFIJOS_NEO: Optional[set] = None


def _caq_bigrams() -> set:
    global _CAQ_BIGRAMS, _AFIJOS_NEO
    if _CAQ_BIGRAMS is None:
        from curiana_database import normalize_source_language
        bg = set()
        for palabra, datos in VOCABULARIO_BASE.items():
            if normalize_source_language(datos.get("fuente", "")) == "caquetío":
                w = palabra.lower()
                bg |= {w[i:i+2] for i in range(len(w) - 1)}
        _CAQ_BIGRAMS = bg
        _AFIJOS_NEO = {a.strip("-").lower() for a in TODAS_LAS_REGLAS}
    return _CAQ_BIGRAMS


def _componente_espanol(comp: str) -> bool:
    """True si un componente de neologismo delata origen español. Combina:
    (1) blocklist de raíces frecuentes, (2) marcadores ortográficos español-only,
    (3) ≥2 bigramas ausentes del caquetío (un solo bigrama raro se tolera para no
    bloquear combinaciones caquetías novedosas — p.ej. 'kale')."""
    c = comp.strip(" *-").lower()
    caq = _caq_bigrams()
    if not c or len(c) <= 2 or c in _AFIJOS_NEO:
        return False
    if c in ES_STOPWORDS or c in RAICES_ESPANOLAS:
        return True
    if _MARCADORES_ES.search(c):
        return True
    bad = sum(1 for i in range(len(c) - 1) if c[i:i+2] not in caq)
    return bad >= 2


def neologismo_valido(forma: str, componentes: str = "") -> bool:
    """True si la FORMA del neologismo no delata origen español en ninguno de sus
    componentes (separados por guion). Solo se chequea la forma acuñada; el campo
    `componentes` va en español como explicación del agente, así que no se
    inspecciona. Filtro de tres capas (blocklist + marcadores ortográficos +
    fonotáctica por bigramas caquetíos) para que la koiné no fije préstamos
    castellanos disfrazados (suave-bana-ni, carrera-kata, guardia-bana, etc.).

    Validado contra los 28 neologismos caquetíos adoptados del run f8ef263d:
    cero falsos positivos; bloquea los ofensores observados."""
    return not any(
        _componente_espanol(p) for p in re.split(r"[-+\s,;]+", (forma or ""))
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

        # Compuerta de calidad: descartar neologismos con raíz española antes
        # de que entren a competir/fijarse en la koiné (suave-bana-ni, etc.).
        if not neologismo_valido(forma, componentes):
            continue

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


# Un morfema empieza y acaba en frontera: principio o fin de texto,
# espacio, guion (que es como se escribe aqui la composicion) o signo
# de puntuacion.
_LIMITE_MORFEMA = frozenset(
    [""] + list(" \t\n\r") + list("-") + list("\u2013\u2014")
    + list(".,;:!?()[]{}/\"'") + list("\u00ab\u00bb\u2026"))


def detectar_uso_vocabulario(texto: str, lexico: "LexicoComunitario") -> list:
    """Detecta qué palabras del vocabulario conocido aparecen en el texto.

    ⚠ NINGÚN módulo del motor la llama (medido el 2026-09-09): el pipeline usa
    `score_linguistico()`, que tokeniza. Se conserva porque es la forma natural
    de preguntar «qué morfemas del lexicón hay aquí» y la usan mediciones
    sueltas.

    Casaba por SUBCADENA en cualquier posición: el 77% de sus detecciones caían
    dentro de otra palabra. Buena parte era legítima —en una lengua aglutinante
    `sima` y `bana` SÍ están dentro de `sima-bana`—, pero también disparaban
    claves cortas de otra lengua por pura coincidencia de letras: `bi` dentro de
    `biro`, `li` dentro de `kali-taro`, 409 veces cada una. Ahora el match
    respeta el límite de morfema.
    """
    texto_lower = texto.lower()
    usadas = []
    for palabra in lexico.palabras_activas():
        if not palabra:
            continue
        aguja = palabra.lower()
        desde = 0
        while True:
            i = texto_lower.find(aguja, desde)
            if i < 0:
                break
            izq = texto_lower[i - 1] if i else ""
            j = i + len(aguja)
            der = texto_lower[j] if j < len(texto_lower) else ""
            if izq in _LIMITE_MORFEMA and der in _LIMITE_MORFEMA:
                usadas.append(palabra)
                break
            desde = i + 1
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
    # «debe» (run c6837386, 2026-09-16): el verbo castellano colisiona con la
    # clave achagua `debe` 'medicina' de la comparanda, que se normaliza a
    # proto-arahuaco, y salía como fuga a otra lengua arahuaca —medido antes
    # del arreglo: «taya debe buko» → score 4,9, palabras_otro_arahuaco=['debe'].
    # Del paradigma sólo esta forma está en VOCABULARIO_BASE (deben, debo,
    # debes, debemos: ninguna), así que sólo ésta entra. La comparanda no se toca.
    "debe",
}

# ── Castellano corriente que ADEMÁS es clave de la comparanda ──────────
# (falsos préstamos medidos en los runs c6837386 y 89fc1744, 2026-09-16)
#
# El scorer busca cada token en un saco de ~1.500 claves de ocho lenguas. Unas
# pocas de esas claves son, además, palabras que cualquier hispanohablante usa
# hoy sin conciencia de préstamo, y entonces el instrumento no puede distinguir
# «el agente tomó prestada la voz taína» de «el agente escribió en castellano».
# Medido: `cacique` ×2 en «…la esencia que sopla el cacique irá al capubana…»
# (todo el entorno es castellano) y `taita` ×1 en «Taita Dabuda naa» —glosado
# por el propio agente como «Mi abuela dice»—, o sea el honorífico castellano
# delante de un nombre, no la voz taína.
#
# QUÉ ENTRA AQUÍ, y por qué es un criterio y no una lista:
#   (a) la voz que el castellano ya se tragó CON SU SENTIDO —`cacique`, `taita`,
#       `bohio`/`bohío`—: forma y significado coinciden en las dos lenguas, así
#       que el uso es inobservable como préstamo; no hay diferencia a la que
#       agarrarse.
#   (b) el homógrafo puro —`dia`, que es «día» sin tilde y en lokono es
#       'decir'—: la forma coincide y el sentido no, como `de`, `una` o `debe`.
#
# QUÉ NO ENTRA, y es el residuo declarado: las voces de COSA que el castellano
# también se tragó —`casabe`, `hamaka`, `kanoa`, `auyama`, `cobo`— son justo lo
# que la medición del préstamo de esfera existe para ver circular. Sacarlas
# vaciaría el instrumento. Si un agente escribe «casabe» porque es castellano,
# se contará como préstamo taíno: se prefiere ese falso positivo a la ceguera.
#
# CÓMO SE TRATA: **neutro**, como `HOMOGRAFOS_ZAVALA` — ni densidad ni
# penalización. No es gratis: el token sigue contando en `n_tok`, así que
# diluye la densidad. Pero NO penaliza como `ES_STOPWORDS`, y la diferencia con
# «debe» (#133) es la que separa una palabra de contenido del andamiaje
# gramatical: sin «el/la/de/que» no se puede escribir una frase castellana,
# mientras que una frase caquetía puede mencionar «el cacique». Castigar un
# sustantivo como se castiga un artículo sería sobrecastigar — que es el
# razonamiento ya escrito para los homógrafos de contenido de Zavala.
#
# ALCANCE: sólo el token PELADO. `ta-bohío` («descanso en mi hamaca en el
# bohío», run 89fc1744) lleva el posesivo caquetío: ahí la lengua está haciendo
# algo con la raíz, que es exactamente la pinta de un préstamo de verdad, y
# sigue contando como préstamo de esfera.
CASTELLANO_CORRIENTE = frozenset({
    "cacique", "taita", "bohio", "bohío", "dia",
})

# ── Nombrar la lengua no es hablarla ───────────────────────────────────
# `lokono` está en el lexicón como voz de la comparanda ('persona arahuaca,
# miembro del pueblo Lokono'), así que «Wayunaiki no. Lokono no. Ta lengua,
# caquetío.» (run c6837386, tier 3) salía como fuga al lokono — cuando el
# agente estaba diciendo justamente lo contrario. Es una mención metalingüística
# de un nombre propio, y el proyecto ya declara en `_CAT_NO_PRESTABLE` que los
# etnónimos de la comparanda «son nombres propios de la comparanda, no
# vocabulario prestable». El conjunto es cerrado: los nombres de las lenguas que
# el lexicón compara (las categorías canónicas de `normalize_source_language`).
#
# ⚠️ Estas voces son HOMÓGRAFAS, no neutras de oficio: casi todos los etnónimos
# arahuacos son a la vez el sustantivo 'persona' de su lengua (`wayuu` =
# 'persona, gente, ser humano'; `lokono`, 'persona arahuaca'). Declararlas
# neutras siempre cegaría la medición anticircular —hablar wayuu tiene que
# penalizar—, así que se resuelven por CONTEXTO como los homógrafos de Zavala:
# con un vecino arahuaco son la palabra, rodeadas de castellano son el nombre.
# En el caso medido los vecinos son «no» y «no», y sale neutro.
GLOTONIMOS_DE_LA_COMPARANDA = frozenset({
    "caquetío", "caquetio", "wayunaiki", "wayuu", "lokono", "garifuna",
    "taíno", "taino", "kalinago", "achagua", "paraujano", "añú", "anu",
    "arahuaco", "arawak", "jirajara", "jirajaroide", "ayaman", "gayon",
})

# ══════════════════════════════════════════════════════════════════════
# LO QUE EL LEXICÓN DECLARA VERBAL — y de qué lengua (corte del 2026-09-21)
# ══════════════════════════════════════════════════════════════════════
# `CATS_VERBALES` es la única puerta que dice qué `cat` se predica con
# aspecto. Son DOS desde la tanda del 2026-09-21 (d21.4, «Vale vamos con la B
# entonces»): la raíz de ACCIÓN (`v_raiz`) y la ESTATIVA (`v_estativo`), que
# es lo que el castellano llama adjetivo y el arahuaco conjuga — la 4ª
# conjugación lokono de Perea y Alonso 1942 pp. 634-639 (`cule-n` 'ser rojo',
# `hebbe-n` 'ser viejo'). La clase se declara SIN su alineamiento: no se
# importa el pronombre pospuesto (opción C del punto 4 de la auditoría), que
# no tiene ni un dato caquetío detrás. Las diez estativas salen del reparto de
# las 49 raíces de Zavala (#178, `lexicon_zavala.CLASES_DE_RAIZ_ZAVALA`).
#
# Quien pregunte «¿es verbo?» pregunta por aquí y no por `== "v_raiz"`: si no,
# etiquetar la clase habría VACIADO diez raíces del paradigma de aspecto, que
# es lo contrario de lo que d21.4 decide.
CATS_VERBALES = frozenset({"v_raiz", "v_estativo"})

# Sufijos aspectuales anclados a raíces verbales conocidas (de VOCABULARIO_BASE).
_RAICES_VERB = {k for k, v in VOCABULARIO_BASE.items()
                if v.get("cat") in CATS_VERBALES}

# ── d21.2 («Si, A», 2026-09-21): la tabla de arriba MEZCLA LAS CINCO LENGUAS.
# De sus claves, la inmensa mayoría no son caquetías (proto-arahuaco y lokono
# de la comparanda), y `score_linguistico.es_arahuaco()` devolvía True para
# cualquier token cuyo primer segmento estuviera ahí: la densidad arahuaca —el
# 60 % del score— la decidía en parte el andamio con el que se reconstruye.
# Es la misma clase de agujero que el `return "caquetío"` del 2026-09-20, en
# otra puerta.
#
# Se filtra a familia caquetía en LAS DOS puertas que la decisión nombra:
# `es_arahuaco` (donde se decide la densidad) y el detector de aspecto.
#
# ⚠️ Lo que NO se filtra, dicho: `_familia_de_token()` sigue probando
# `_RAICES_VERB` entera, porque es también quien resuelve
# `word_uses.source_language` y una clave lokono tiene que seguir devolviendo
# lokono (`test_word_source_language_conserva_la_lengua_hermana`). Y
# `_raices_conocidas()` también, porque ahí la pregunta es «¿el lexicón conoce
# esta raíz?», de cualquier lengua, no «¿es caquetía?».
#
# Perezosa como `_raices_conocidas()`: `normalize_source_language` vive en
# `curiana_database`, que importa de aquí.
_RAICES_VERB_CAQ: Optional[frozenset] = None


def raices_verbales_caquetias() -> frozenset:
    """Las raíces que el lexicón declara verbales Y caquetías.

    `v_raiz` + `v_estativo` (`CATS_VERBALES`), normalizando la fuente a
    familia: entran las atestiguadas, las reconstruidas, las retroabstraídas
    y las hipotéticas del caquetío; no entran wayunaiki, lokono, taíno ni el
    proto-arahuaco de la comparanda.
    """
    global _RAICES_VERB_CAQ
    if _RAICES_VERB_CAQ is None:
        from curiana_database import normalize_source_language
        _RAICES_VERB_CAQ = frozenset(
            k for k in _RAICES_VERB
            if normalize_source_language(
                VOCABULARIO_BASE[k].get("fuente", "")) == "caquetío")
    return _RAICES_VERB_CAQ


def _normalizar(texto: str) -> str:
    # quita glosas entre paréntesis (no deben puntuar como caquetío ni penalizar)
    return re.sub(r"\([^)]*\)", " ", texto)


def _tokenizar(texto: str) -> list:
    # tokens alfabéticos, conservando guion interno (ta-barsure, naa-ka)
    return re.findall(r"[a-záéíóúñü]+(?:-[a-záéíóúñü]+)*", texto.lower())


def _aspectos_morfologicos(tokens: list) -> list:
    """Detecta -ka/-ni/-da sobre una raíz que el lexicón DECLARA verbal.

    ⚠️ CORTE DE SERIE DEL 2026-09-21 (d21.1, «Si vamos con C»; d21.2, «Si, A»).
    La condición era `suf in {ka,ni,da} and (raiz in _RAICES_VERB or
    len(raiz) >= 3)`, y ese `len(raiz) >= 3` era un COMODÍN DE LONGITUD: de las
    62.347 detecciones de toda la base, 20.165 entraban sin verbo ninguno
    (`hamaka-chaa-ni`, `kali-barsure-da`, `baro-ni`). El aspecto vale hasta 2
    de los 10 puntos del score, así que el 20 % de la métrica se ganaba con un
    guion y tres letras.

    Lo que hace ahora, y son las dos decisiones juntas porque tocan la misma
    condición:

      (d21.1 C) el aspecto cuenta si el ÚLTIMO SEGMENTO antes del sufijo es
      raíz verbal. Es el comodín acotado: `ta-hamaka-chaa-ni` cuenta por
      `chaa`, que es el caso legítimo que el comodín cubría a ciegas, y
      `hamaka-chaa` ya no cuenta por `hamaka`. Consecuencia declarada: en un
      aspecto APILADO (`chaa-ni-da`, 130 usos en 48 formas) el segundo sufijo
      va sobre el primero y no sobre un verbo, así que deja de contar — el
      apilamiento es gramática que la comunidad inventó (d21.12) y se describe
      en morfologia.md, no se premia en el score.

      (d21.2 A) la raíz verbal tiene que ser CAQUETÍA: `raices_verbales_caquetias()`
      y no `_RAICES_VERB`, que mezcla las cinco lenguas.

    `v_estativo` cuenta como verbal (d21.4): un estado se predica con aspecto
    igual que una acción, y eso lo decide `CATS_VERBALES`, no esta función.
    """
    encontrados = []
    mapa = {"ka": "completivo", "ni": "continuativo", "da": "prospectivo"}
    verbales = raices_verbales_caquetias()
    for tok in tokens:
        # forma con guion: raiz-sufijo
        if "-" in tok:
            raiz, _, suf = tok.rpartition("-")
            if suf in mapa and raiz.rsplit("-", 1)[-1] in verbales:
                encontrados.append(mapa[suf])
            continue
        # forma aglutinada: raizverbal + sufijo (naaka, wanani)
        for raiz in verbales:
            for suf, nombre in mapa.items():
                if tok == raiz + suf:
                    encontrados.append(nombre)
    return list(dict.fromkeys(encontrados))  # únicos, orden estable


# ── Formas retiradas del habla (D10, 2026-08-03) ──────────────────────
# NO son vocabulario activo: no se siembran en Supabase, no entran en los
# prompts y no puntúan. Se conservan con su procedencia porque el proyecto
# retira palabras con la misma disciplina con que las admite: se archiva el
# porqué, no se borra el rastro. Ver aplicar_d10.py.
#
# ⚠️ ARCHIVAR NO ES BORRAR, Y TAMPOCO ES DEGRADAR. La entrada conserva su
# `fuente` —su capa epistémica— intacta: `kali` sigue siendo
# `caquetío-reconstruido` y `mülia` sigue siendo `caquetío-hipotético`. Lo
# único que se le quita es el habla. La etiqueta dice DE DÓNDE VIENE la
# palabra; el archivo dice si la comunidad la usa. Son dos ejes distintos y
# mezclarlos rompería la regla 2.
#
# Desde el 2026-09-19 esta tabla es además UNA PUERTA: `FORMAS_DE_PLANTILLA`
# la incluye, así que una forma archivada tampoco puede volver por la puerta
# de atrás como acuñación de la comunidad (`registrar_neologismo`,
# `CompetenciaLexica.proponer`). No se enseña Y no compite.
FUERA_DEL_HABLA: dict[str, dict] = {
    "piache": {"sig": "chamán, curandero, intermediario espiritual", "cat": "sust", "fuente": "caribe-cháima", "notas": "D10 (2026-08-03) — RETIRADA DEL HABLA; su lugar lo ocupa `boratio`. Alvarado 1921 p.248 s.v. PIACHE: «Sacerdote indígena, que, según los casos, era al mismo tiempo brujo, hechicero o herbolario... Voz cháima y tamanaca, con formas afines en otras lenguas caribes» (cita a Aguado I.458). Zavala Reyes 2015 lo confirma por otra vía: su glosario #43 (AM+HB) glosa el caquetío «boratio» COMO 'piache, cacique, jefe, sacerdote, médico' — piache es la glosa española, boratio la voz caquetía, ya en el lexicón con su cita (Arcaya 1920:116; Oviedo vía Jahn 1927:213 n.29). La sección D de Zavala la adjudica al cumanagoto y Alvarado al cháima: ambas caribe continental, difieren en cuál. La entrada NO se borra, se archiva aquí con su procedencia. El canon no se toca: Shaboro sigue siendo el piache de la Curiana"},
    "wanee":      {"sig": "uno (numeral)",                                  "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `aba` 'uno' — otra raíz. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · RETIRADA DEL HABLA 2026-09-13 (Miguel: «Cambiemos los numerales»): el caquetío ATESTIGUA pana 'uno', gudamuen 'dos', sabuenen 'tres' y katarí 'cuatro' (Zavala Reyes 2015 #148, #222, #70, vía Pedro Manuel Arcaya), y el canon enseñaba en su lugar esta forma reconstruida desde el wayuu. 'Cinco' no está atestiguado: el prompt presenta el sistema de la mano de lokono y achagua y los agentes lo acuñan. Medición y propuesta: 6-fusion/propuesta_nucleo_d11_fase3.yaml", "fuente": "caquetío-reconstruido"},
    "piama":      {"sig": "dos (numeral)",                                  "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `bian` 'dos' — PARECIDA (p~b). SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · RETIRADA DEL HABLA 2026-09-13 (Miguel: «Cambiemos los numerales»): el caquetío ATESTIGUA pana 'uno', gudamuen 'dos', sabuenen 'tres' y katarí 'cuatro' (Zavala Reyes 2015 #148, #222, #70, vía Pedro Manuel Arcaya), y el canon enseñaba en su lugar esta forma reconstruida desde el wayuu. 'Cinco' no está atestiguado: el prompt presenta el sistema de la mano de lokono y achagua y los agentes lo acuñan. Medición y propuesta: 6-fusion/propuesta_nucleo_d11_fase3.yaml", "fuente": "caquetío-reconstruido"},
    "apünüin":    {"sig": "tres (numeral)",                                 "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `kabyn` 'tres' — otro sistema. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · RETIRADA DEL HABLA 2026-09-13 (Miguel: «Cambiemos los numerales»): el caquetío ATESTIGUA pana 'uno', gudamuen 'dos', sabuenen 'tres' y katarí 'cuatro' (Zavala Reyes 2015 #148, #222, #70, vía Pedro Manuel Arcaya), y el canon enseñaba en su lugar esta forma reconstruida desde el wayuu. 'Cinco' no está atestiguado: el prompt presenta el sistema de la mano de lokono y achagua y los agentes lo acuñan. Medición y propuesta: 6-fusion/propuesta_nucleo_d11_fase3.yaml", "fuente": "caquetío-reconstruido"},
    "pienchi":    {"sig": "cuatro (numeral)",                               "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `bithi` 'cuatro' — otra raíz. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · RETIRADA DEL HABLA 2026-09-13 (Miguel: «Cambiemos los numerales»): el caquetío ATESTIGUA pana 'uno', gudamuen 'dos', sabuenen 'tres' y katarí 'cuatro' (Zavala Reyes 2015 #148, #222, #70, vía Pedro Manuel Arcaya), y el canon enseñaba en su lugar esta forma reconstruida desde el wayuu. 'Cinco' no está atestiguado: el prompt presenta el sistema de la mano de lokono y achagua y los agentes lo acuñan. Medición y propuesta: 6-fusion/propuesta_nucleo_d11_fase3.yaml", "fuente": "caquetío-reconstruido"},
    "jarai":      {"sig": "cinco (numeral)",                               "cat": "num",   "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'cinco'. SE CONSERVA LA FORMA por continuidad experimental —cambiarla partiría en dos la comparabilidad de todos los runs de la base y movería score_linguistico()—, pero NO CUENTA COMO EVIDENCIA: cualquier coincidencia de esta entrada con el wayuu es circular. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · RETIRADA DEL HABLA 2026-09-13 (Miguel: «Cambiemos los numerales»): el caquetío ATESTIGUA pana 'uno', gudamuen 'dos', sabuenen 'tres' y katarí 'cuatro' (Zavala Reyes 2015 #148, #222, #70, vía Pedro Manuel Arcaya), y el canon enseñaba en su lugar esta forma reconstruida desde el wayuu. 'Cinco' no está atestiguado: el prompt presenta el sistema de la mano de lokono y achagua y los agentes lo acuñan. Medición y propuesta: 6-fusion/propuesta_nucleo_d11_fase3.yaml", "fuente": "caquetío-reconstruido"},
    # ── Política «manda la atestiguada» (2026-09-19) ──────────────────
    # Miguel: «Sí o sí tenemos que usar los atestiguados por sobre los
    # reconstruidos, por lo menos la parte caquetía». Donde el caquetío TIENE
    # forma atestiguada para un significado, la derivada deja de enseñarse y
    # de competir. Las siete de abajo son los pares 1, 3, 4, 12, 13, 16 y 18
    # del issue `pares-atestiguado-reconstruido-2026-09-19.md`. Su capa NO se
    # toca y su procedencia se conserva entera: el archivo es un eje distinto
    # de la etiqueta. Medido en
    # `6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml`.
    "kali":       {"sig": "sol",                                            "cat": "sust",  "fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 1 «sol» · manda `kasi`", "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna — sin obra citada · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada», decisión de Miguel): el caquetío atestigua `kasi` 'sol' (Zavala Reyes 2015, glosario #76 (GC): «Sol», forma_fuente cazi, fusionada por D5a). Es el archivo más grande de la tanda por uso. Su desequilibrio NO era del muestreador —para 'sol' el muestreo es neutro, 60 contra 63 de 1.260— sino de las plantillas: `IDENTIDAD_LINGUISTICA` la enseñaba en su ejemplo hasta el corte del 2026-09-19 (#172) y `prompt_reglas_completo` la enseñaba en NATURALEZA, en el ejemplo de respuesta ideal y en la lista de sustantivos del refuerzo. LA CAPA NO SE TOCA: sigue siendo `caquetío-reconstruido`. El compuesto `kali-bana` y el molde `kali-…-bana` quedan cerrados por esta puerta, que es MÁS que el corte del 09-18 (aquél sólo cerraba la forma exacta)"},
    "kasha":      {"sig": "luna",                                           "cat": "sust",  "fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 12 «luna» · manda `kati`", "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki/lokono — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. lokono `kathi` 'luna' — PARECIDA; esta entrada ya declaraba apoyo lokono además del wayuu. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `kati` 'luna' (Zavala Reyes 2015, glosario #71 (CGB), forma_fuente cati, fusionada por D5), con cognados proto-arahuaco *kati, WY kachi, LK katsi. Y el lokono `kathi` que ESTA nota citaba como apoyo es justamente el cognado de `kati`: la atestiguada era además la mejor reconstrucción bajo D11. El párrafo «SE CONSERVA LA FORMA por continuidad experimental» de la re-etiqueta de D11 queda superado por esta decisión, que sí acepta el corte de serie. LA CAPA NO SE TOCA"},
    "habo":       {"sig": "mar, océano, aguas grandes",                     "cat": "sust",  "fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 13 «mar» · manda `para`", "notas": "núcleo fundacional, forma justificada por cognado en lokono/garifuna · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `para` 'mar, agua extensa' (Zavala Reyes 2015 #190 (E+HP); reflejo del proto-arahuaco *para atestiguado en cuatro lenguas). El uso real iba por delante de la decisión: `para` ya ganaba en toda la base y en la serie C limpia. LA CAPA NO SE TOCA. ⚠️ `haborü` 'marejada' (habo+rü, hipotética) sigue en el habla con la raíz archivada: deuda declarada de la tanda"},
    "paa":        {"sig": "dar, ofrecer, transferir",                       "cat": "v_raiz","fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 3 «ofrecer» · manda `were`", "notas": "núcleo fundacional, forma justificada por cognado en proto-arahuaco · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `were` 'dar, entregar, ofrecer' (Zavala Reyes 2015, glosario #149 (AM): «Dar, entregar», forma_fuente güere). ES EL ARCHIVO MÁS CARO DE LA TANDA y se declara como tal: `paa` es raíz verbal del núcleo con todo su paradigma de aspecto vivo en la base (`paa-da`, `paa-ni`, `paa-ka` y medio centenar de formas más). NO HAY HUECO FUNCIONAL: `were` es también `v_raiz` y atestiguada, entra en `_RAICES_VERB` y toma los mismos tres aspectos, así que el paradigma no se rompe — se muda de raíz. Lo que sí cuesta es la comparabilidad: las formas `paa-*` de los runs ya corridos dejan de contar como arahuacas al re-puntuar, y eso es exactamente lo que un corte de serie declara. Coste medido en 6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml. LA CAPA NO SE TOCA"},
    "kira":       {"sig": "escuchar, oír, atender",                         "cat": "v_raiz","fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 4 «escuchar» · manda `jai`", "notas": "núcleo fundacional, forma justificada por cognado en wayunaiki/lokono — ⚠️ DEUDA D11 (re-etiquetada 2026-09-10, decisión de Miguel): forma reconstruida desde el WAYUU **antes** de D11, que retiró al wayuunaiki como hermana por defecto. el lokono del lexicón no cubre 'escuchar'. Ver 6-fusion/issues-pendientes/decision-d11-el-nucleo-reconstruido-del-wayuu.md · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `jai` 'oír, escuchar' (Zavala Reyes 2015, glosario #175 (AM)), que es también `v_raiz` y ya llevaba 167 usos sin que ninguna plantilla se lo enseñara. Segundo archivo más caro por paradigma (`kira-ni`, `kira-da`, `kira-ka`). LA CAPA NO SE TOCA"},
    "joutai":     {"sig": "viento, corriente de aire (< joutai Wayunaiki)", "cat": "sust",  "fuente": "caquetío-reconstruido", "archivada": "2026-09-19 · política atestiguado-manda · par 16 «viento» · manda `juri`", "notas": "F8 (2026-09-12): forma derivada de la hermana que cita la glosa, etiquetada `wayunaiki-cogn`; entra en la deuda de D11 fase 3 (núcleo reconstruido desde el wayuu) · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `juri` 'viento, ventarrón' (Zavala Reyes 2015 #178 (E), variantes: jura). Es el archivo que menos cuesta de los que tenían uso: `juri` ya ganaba con holgura, ninguna plantilla enseñaba a ninguna de las dos, y la propia glosa de `joutai` declara que viene del wayuu — que es justo lo que D11 retiró. LA CAPA NO SE TOCA"},
    "mülia":      {"sig": "miedo, temor, espanto",                          "cat": "sust",  "fuente": "caquetío-hipotético", "archivada": "2026-09-19 · política atestiguado-manda · par 18 «espanto» · manda `etamo`", "notas": "F8 (2026-09-12): forma sin cita ni derivación declarada, etiquetada `wayunaiki/lokono` · ARCHIVADA DEL HABLA 2026-09-19 (política «manda la atestiguada»): el caquetío atestigua `etamo` 'feroz, feo, espanto' (Zavala Reyes 2015 #120 (AM)). El archivo más barato de la tanda: hipotética, sin cita, 0 usos en toda la base y 0 exposición en el muestreo del perfil era2. LA CAPA NO SE TOCA: sigue siendo `caquetío-hipotético`"},
}


# Los afijos que el proyecto DECLARA caquetíos (`TODAS_LAS_REGLAS`: los cuatro
# prefijos posesivos, los tres aspectos y los seis afijos atestiguados de
# REGLAS_ZAVALA). Son los que dicen dónde acaba la raíz de un token con guion.
_PREFIJOS_CAQ = frozenset(a for a in TODAS_LAS_REGLAS if a.endswith("-"))
_SUFIJOS_CAQ = frozenset(a for a in TODAS_LAS_REGLAS if a.startswith("-"))
_AFIJOS_SUELTOS = frozenset(a.strip("-").lower() for a in TODAS_LAS_REGLAS)


# ══════════════════════════════════════════════════════════════════════
# LA RAÍZ DE NINGUNA PARTE — corte de serie del 2026-09-20
# ══════════════════════════════════════════════════════════════════════
# `_familia_de_token()` acababa en `return "caquetío"` para cualquier token
# que no encontrara en el lexicón. La razón escrita era buena —«es un
# neologismo comunitario, lengua propia, no préstamo»— y vale para una
# acuñación hecha con morfemas del canon: `biro-ana` es `biro` 'sal' + el
# locativo, y `kasi-nii-bana` es la atestiguada `kasi` con dos afijos. No vale
# para una raíz que NO está en ninguna tabla del lexicón: ahí los afijos
# caquetíos son un disfraz.
#
# Lo midió el brazo de CONTROL de la serie C (runs `0345840d` → `45618069` →
# `e98227eb`, 2026-09-20): `lumina-bana-iro` fue la segunda forma más fuerte
# de la disputa de las cuentas (36,3) y `lumina-bana-uco` FIJÓ el cometa en el
# diccionario koiné — con `lumina` latina, que ningún agente sacó del lexicón
# porque no está. Uno de ellos lo escribió en su propia glosa: «lumina:
# cosa-que-brilla (del español, pero transformada en caquetío)».
#
# LA REGLA, y es de raíz, no de forma: se quitan de los BORDES los afijos que
# el proyecto DECLARA caquetíos (`TODAS_LAS_REGLAS`) y lo que queda es el
# NÚCLEO. Si ningún segmento del núcleo es voz que el lexicón conozca, la raíz
# no es de ninguna parte. Así `kasi-nii-bana` pasa (`kasi` y `nii` son claves)
# y `lumina-bana-iro` no (queda `lumina` y no es nada).
#
# ⚠ NO es lo mismo que `neologismo_valido()`, y por eso hacen falta las dos:
# aquél mira la FORMA (blocklist de raíces castellanas, marcadores
# ortográficos, bigramas ausentes del caquetío) y `lumina` pasa sus tres capas
# —`lu`, `um`, `mi`, `in`, `na` son bigramas caquetíos corrientes—. Éste mira
# la PERTENENCIA: una raíz con forma impecable que no está en el lexicón sigue
# sin ser caquetía.
_RAICES_CONOCIDAS: Optional[frozenset] = None


def _raices_conocidas() -> frozenset:
    """Todo lo que el lexicón reconoce como RAÍZ, de cualquier lengua.

    Perezosa a propósito: `_SUFIJOS_DE_LENGUA` se define más abajo en el
    módulo, como `_caq_bigrams()` con `normalize_source_language`.

    Entran: `VOCABULARIO_BASE` (las 5.507 claves, las cinco lenguas — una raíz
    lokono con afijo caquetío ya la clasificaba bien `_familia_de_token` y
    tiene que seguir haciéndolo), `FUERA_DEL_HABLA` (archivar no es borrar: la
    palabra existió y su raíz sigue siendo del canon) y `_RAICES_VERB`. Y la
    clave sin su desambiguador de lengua, porque el lexicón escribe
    `casa-lokono` o `kati-kalinago` y esa etiqueta no es parte de la voz.

    Todo va EN MINÚSCULA además de como está escrito: el lexicón tiene alguna
    clave con mayúscula (`Adajali`, el nombre de la deidad lokono) y el
    tokenizador entrega siempre minúsculas. Sin esto, `Adajali` habría salido
    «desconocida» de su propia entrada.
    """
    global _RAICES_CONOCIDAS
    if _RAICES_CONOCIDAS is None:
        conocidas = set(VOCABULARIO_BASE) | set(FUERA_DEL_HABLA)
        for clave in list(conocidas):
            if "-" in clave and clave.rsplit("-", 1)[-1] in _SUFIJOS_DE_LENGUA:
                conocidas.add(clave.rsplit("-", 1)[0])
        conocidas |= _RAICES_VERB
        _RAICES_CONOCIDAS = frozenset(conocidas | {c.lower() for c in conocidas})
    return _RAICES_CONOCIDAS


def nucleo_de_token(tok: str) -> list[str]:
    """Los segmentos que quedan al quitar por los bordes los afijos declarados.

    `ta-kasi-nii-bana` → `['kasi', 'nii']`; `lumina-bana-iro` → `['lumina']`.
    Es el mismo desafijado que hace `_familia_de_token()`, sacado aparte para
    que la puerta y el clasificador no se puedan desincronizar.
    """
    partes = (tok or "").strip().lower().split("-")
    while len(partes) > 1 and partes[0] + "-" in _PREFIJOS_CAQ:
        partes = partes[1:]
    while len(partes) > 1 and "-" + partes[-1] in _SUFIJOS_CAQ:
        partes = partes[:-1]
    return partes


def es_raiz_de_ninguna_parte(forma: Optional[str]) -> bool:
    """¿La raíz de esta forma no está en ninguna tabla del lexicón?

    La usan `LexicoComunitario.registrar_neologismo()` (no se registra),
    `CompetenciaLexica.proponer()` (no compite) y `_familia_de_token()` (no se
    dice caquetía). Es la hermana de `es_forma_de_plantilla()`: aquélla para
    lo que el prompt ya enseña, ésta para lo que no es de aquí.
    """
    tok = (forma or "").strip().lower()
    if not tok:
        return False
    conocidas = _raices_conocidas()
    if tok in conocidas:
        return False
    return not any(seg in conocidas for seg in nucleo_de_token(tok))


def _familia_de_token(tok: str) -> str:
    """
    Familia lingüística canónica de un token ya reconocido como arahuaco.
    Deshace prefijos posesivos y raíces verbales para encontrar la entrada
    real en VOCABULARIO_BASE. Si no está en el lexicón base pero su RAÍZ sí,
    se trata como "caquetío" — son palabras nuevas acuñadas por la propia
    comunidad con morfemas propios, no préstamos de una lengua viva real. Si
    ni la raíz está en ninguna tabla del lexicón, devuelve **"desconocida"**:
    unos afijos caquetíos sobre una raíz que no es de aquí no hacen una
    palabra caquetía (corte de serie del 2026-09-20; `lumina-bana-iro`).

    ⚠ LA RAÍZ DECIDE, y la raíz es lo que queda al quitar los afijos que el
    proyecto declara caquetíos (2026-09-16). Antes se quitaba SIEMPRE el primer
    segmento como si fuera prefijo posesivo y el segundo ganaba la
    clasificación, así que un token con raíz caquetía y sufijo caquetío salía
    de otra lengua por pura colisión con una clave de la comparanda:
    `juri-ima` y `lawari-ima` (raíces caquetías `juri` 'viento' y `lawari`
    'acacia' + el sufijo ATESTIGUADO `-ima` de REGLAS_ZAVALA) se contaban como
    LOKONO por la clave `ima` 'enemigo'. Medido en los runs c6837386/89fc1744.
    El mismo criterio de consistencia vale para la raíz verbal: si un token
    entró al conteo porque su primer segmento es raíz verbal conocida
    (`maa-to`, vía `maa` 'decir'), es ese morfema el que decide su lengua.

    Lo que NO cambia: `ka-to` sigue siendo lokono. Ahí el prefijo caquetío va
    sobre una raíz ajena (`to`, artículo lokono), y eso es justo lo que la
    métrica quiere ver — morfología propia sobre léxico de la lengua con la que
    se reconstruye. Igual `ta-bohío`, que sigue siendo préstamo taíno.

    ⚠ Esta función es también la que resuelve `word_uses.source_language`, o
    sea el DICCIONARIO: una clave del lexicón tiene que seguir devolviendo su
    propia lengua (`test_word_source_language_conserva_la_lengua_hermana`).
    Por eso lo que depende del CONTEXTO —el afijo suelto, el glotónimo, el
    castellano corriente— se resuelve en `score_linguistico()`, no aquí.
    """
    from curiana_database import normalize_source_language

    # LA RAÍZ DECIDE, y decide PRIMERO (corte de serie del 2026-09-20). Va
    # antes que los candidatos porque el último de ellos es un legado —
    # `tok.split("-", 1)[1]`, «lo que se probaba antes, para que nada que se
    # resolvía deje de resolverse»— y con una raíz ajena ese legado resuelve
    # por el SUFIJO: `pütshi-bana` habría salido caquetío por la clave `bana`
    # 'hígado', que ahí no es la raíz sino el locativo. La puerta del registro
    # y esta función tienen que decir lo mismo de la misma forma.
    if es_raiz_de_ninguna_parte(tok):
        return "desconocida"

    candidatos = [tok]
    if "-" in tok:
        partes = tok.split("-")
        nucleo = partes
        if len(nucleo) > 1 and nucleo[0] + "-" in _PREFIJOS_CAQ:
            nucleo = nucleo[1:]                    # ta-X -> X (prefijo de verdad)
            candidatos.append("-".join(nucleo))
        while len(nucleo) > 1 and "-" + nucleo[-1] in _SUFIJOS_CAQ:
            nucleo = nucleo[:-1]                   # X-ka, juri-ima -> X, juri
            candidatos.append("-".join(nucleo))
        if partes[0] in _RAICES_VERB:
            candidatos.append(partes[0])           # el morfema que lo admitió
        # Legado: lo que se probaba antes, ahora como último recurso, para que
        # nada que se resolvía deje de resolverse.
        candidatos.append(tok.split("-", 1)[1])
        candidatos.append(partes[0])
    for c in candidatos:
        if c in VOCABULARIO_BASE:
            return normalize_source_language(VOCABULARIO_BASE[c].get("fuente", ""))
    # Llegar aquí significa que la raíz SÍ está en el lexicón (lo dice la
    # comprobación de arriba) y que la forma entera no: es una acuñación de la
    # comunidad con morfemas propios, o sea lengua propia y no préstamo.
    return "caquetío"


_NOMBRES_AGENTES: Optional[frozenset] = None


def _nombres_de_agentes() -> frozenset:
    """Los nombres del elenco activo y de la era 1, en minúscula, tal como los
    produce _tokenizar. Se cargan una vez; curiana_agents no importa de aquí,
    así que no hay ciclo."""
    global _NOMBRES_AGENTES
    if _NOMBRES_AGENTES is None:
        try:
            import curiana_agents as _ag
            nombres = (set(_ag.ALL_AGENTS) | set(_ag.AGENTS_T1)
                       | set(_ag.AGENTS_T2) | set(_ag.AGENTS_T3))
        except Exception:                                    # noqa: BLE001
            nombres = set()
        _NOMBRES_AGENTES = frozenset(n.lower() for n in nombres)
    return _NOMBRES_AGENTES


def _nombres_que_chocan_con_el_canon() -> frozenset:
    """Los nombres del elenco que TAMBIÉN son voces del lexicón.

    Son 52 en la era 2 (`buko`, `hayo`, `mene`, `saruro`, `hiko`, `jachos`,
    `karebe`, `naure`…) y las 52 se enseñan en el prompt. Con el filtro en
    minúsculas del 2026-09-14 quedaban fuera del conteo SIEMPRE: eran palabras
    que el motor enseñaba y no contaba. Se separan para tratarlas por caso.
    """
    return frozenset(_nombres_de_agentes() & set(VOCABULARIO_BASE))


def _filtrar_nombres(texto: str, tokens: list) -> list:
    """Quita del conteo las menciones a agentes, sin comerse el vocabulario.

    Un nombre que NO es voz del lexicón (`Biro-ko`, `Dara-bana`) se descarta
    siempre. Uno que sí lo es (`Karebe` persona / `karebe` cucharón) se
    descarta **cuando va en mayúscula**, que es como se nombra a alguien, y
    cuenta como palabra cuando va en minúscula, que es como se usa en el habla
    corrida. Residuo declarado, y elegido a conciencia: una voz del canon que
    abra frase —y por tanto vaya en mayúscula— no se cuenta. Se prefiere
    perder ese uso a que un nombre infle el conteo, porque de `palabras_caquetias`
    comen el contagio, la competencia de formas y el idiolecto: un nombre
    contado como palabra se propagaría por la koiné como si fuera léxico.
    """
    nombres = _nombres_de_agentes()
    if not nombres:
        return tokens
    chocan = _nombres_que_chocan_con_el_canon()
    fuera: list = []
    patron = r"[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+(?:-[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+)*"
    for m in re.finditer(patron, texto):
        tok = m.group().lower()
        if tok not in nombres:
            continue
        if tok not in chocan:
            fuera.append(tok)                     # no colisiona: siempre nombre
            continue
        if m.group()[0].isupper():
            fuera.append(tok)                     # mayúscula: se está nombrando a alguien
    if not fuera:
        return tokens
    quitar: dict = {}
    for t in fuera:
        quitar[t] = quitar.get(t, 0) + 1
    salida = []
    for t in tokens:
        if quitar.get(t):
            quitar[t] -= 1
            continue
        salida.append(t)
    return salida


# ── La esfera de contacto (decisión de Miguel, 2026-09-15) ──────────────
# «El set de cinco es razonable. Yo creo que se debe medir aparte, ya que
# sobre todo para esta área de influencia.»
#
# Las lenguas con contacto ATESTIGUADO con la polity costera: las Antillas
# (préstamos léxicos documentados en Curazao, geografia_politica-001; Aruba a
# 25 km, ecologia-021; cerámica dabajuroide hasta las islas, ecologia-013),
# los caribes que llegan por mar (etnia-008), los del lago y los de la sierra.
# Una voz de éstas en boca de un agente es un PRÉSTAMO —lo que hace una lengua
# de encrucijada—, no una fuga: se mide aparte y no penaliza.
#
# NO entran wayunaiki, lokono ni achagua: las dos primeras son el andamio con
# que se reconstruye el caquetío (D11) —verlas haría circular la medición— y
# la tercera es de los Llanos, que es justo lo que la regla 4 prohíbe importar.
ESFERA_DE_CONTACTO = frozenset({
    "taíno", "kalinago", "paraujano", "caribe-continental", "jirajaroide-contacto",
})


# ── «La etiqueta manda» — la forma de la esfera (Miguel, 2026-09-18) ───────
# «Des-castellanizar» las voces de la esfera. `casabe`, `yuca`, `maíz`,
# `batata` o `papaya` son voces taínas del lexicón que el castellano también
# usa: cuentan como préstamo de esfera —el producto de la esfera ES la esfera,
# decisión del 2026-09-17— pero no tienen por qué circular por el motor con la
# grafía castellana.
#
# La regla es la etiqueta, no la estética. Fila a fila, con fuente y cita, en
# **6-fusion/descastellanizar_esfera_2026-09-18.yaml**; el criterio y el censo
# los mide `6-fusion/scripts/medir_descastellanizar_esfera.py`. En corto:
#   (1) si el lexicón tiene la forma indígena ATESTIGUADA con clave propia, es
#       la que se enseña y la que se registra → esta tabla;
#   (2) si no la tiene, la voz no se enseña hasta que Miguel fusione la forma
#       (atestiguada sin clave, como `hurakán`, o retroabstraída propuesta a la
#       manera de `matakán`) → `SIN_FORMA_DE_LA_ESFERA`;
#   (3) si la grafía «castellana» ES la transcripción atestiguada de la fuente
#       —`yuca`, `batata`, `papaya`, `cazabi`, `chighe`—, se queda.
#
# ⚠ EL SCORER NO SE TOCA. `score_linguistico()` sigue devolviendo la clave
# CASTELLANA en `prestamos_de_esfera`: es la que reconoce, y el agente que
# escribe «casabe» tiene que seguir contando. Se normaliza al GUARDAR
# (`curiana_database.save_loanword_uses`, que además anota en `forma_dicha` lo
# que el agente escribió) y al LEER (`analizar_runs.py --prestamos`), nunca al
# puntuar. `score`, `pct_*` y `capas_de_score` quedan byte a byte.
#
# Las dos claves de cada par existen YA en VOCABULARIO_BASE y comparten
# familia (las cuatro son taínas): normalizar no mueve `source_language`.
FORMA_DE_LA_ESFERA = {
    "casabe":  "cazabi",   # «Tno. cazabi → español cazabe» (nota de `cazabi`)
    "maíz":    "maisi",    # «Tno. maisi → español maíz»    (nota de `maisi`)
    "cacique": "cacike",   # `cacike` lleva `fuente: taíno`; `cacique` es la castellana
    "bohío":   "bohio",    # dos claves para la misma voz taína; la acentuada es la castellana
}

# Claves que la decisión marcó castellanas y para las que el lexicón NO tiene
# gemela. No se enseñan —una propuesta no es canon— hasta que Miguel fusione
# `6-fusion/descastellanizar_esfera_2026-09-18.yaml`. Siguen contando como
# préstamo y se guardan tal como se dijeron.
SIN_FORMA_DE_LA_ESFERA = frozenset({
    "huracan",   # atestiguada sin clave: la nota dice «Tno. hurakán → español huracán»
    "cayo",      # retroabstraída propuesta: kayo
    "caney",     # retroabstraída propuesta: kanei
    "cobo",      # retroabstraída propuesta: kobo
    "cemi",      # retroabstraída propuesta: semi
    "bejique",   # retroabstraída propuesta: bejike
})

# Lo que `marcas_castellanas()` marca y la decisión dejó como está, porque la
# grafía es la transcripción atestiguada de la fuente y no la palabra
# castellana. Está declarado —y no deducido— a propósito: una voz nueva de la
# esfera con ⟨c⟩, ⟨z⟩ o tilde rompe el test hasta que alguien la decida.
SE_QUEDA_CON_SU_GRAFIA = frozenset({
    "yuca",       # Tno. yuca; Miguel 2026-09-18: es la transcripción, se queda
    "cazabi",     # la forma indígena del par; su ⟨c⟩/⟨z⟩ son de la fuente
    "cacike",     # la forma indígena del par
    "cohiba",     # «Taíno atestiguado: cohiba … Brinton 1871»
    "cai",        # «Taíno atestiguado: cai … Brinton 1871» (y `kai` ya es paraujano 'sol')
    "caiman",     # «Taíno atestiguado: caiman … Brinton 1871» (y `kaiman` ya es lokono)
    "akcicyaa",   # taíno-reconstruido desde Lok. akkicyaha: ortografía del lokono
    "chighe",     # paraujano, Wilbert 1958-59 vía Oliver 1989 Tabla A-2 (dígrafos)
    "keichare",   # ídem
    "utschi",     # ídem
    "eichire",    # ídem
    "añu",        # el autónimo Añú, ortografía de la fuente
    "hiñaru",     # kalinago, registro femenino de Breton 1665
    "kalínagu",   # ortografía garífuna del autónimo; la tilde no es castellana
    "achi-kalinago",  # dígrafo ⟨ch⟩ del garífuna/lokono
    "acoa", "daca", "wacusi",   # taíno-reconstruido desde el lokono (categoría `cuerpo`)
    "churuguara", "quibor",     # topónimos modernos (categoría `geografia`)
})

# ⟨c⟩, ⟨z⟩, ⟨qu⟩, ⟨ll⟩, ⟨ñ⟩ y la tilde castellana: lo que la retroabstracción
# del proyecto quita (convención de `matakán`, 6-fusion/matacan_venado_…yaml).
# Es una MEDIDA, no un juicio: dice que la clave lleva la marca, no que la voz
# sea castellana. Quién se queda y quién no lo dice la decisión de arriba.
_MARCAS_CASTELLANAS = (
    ("tilde", re.compile(r"[áéíóú]")),
    ("qu",    re.compile(r"qu")),
    ("c",     re.compile(r"c(?!h)")),
    ("z",     re.compile(r"z")),
    ("ll",    re.compile(r"ll")),
    ("ñ",     re.compile(r"ñ")),
)


def marcas_castellanas(clave: str) -> list:
    """Qué marcas de grafía castellana lleva una clave del lexicón.

    La etiqueta de lengua con que el lexicón desambigua homógrafos
    (`achi-kalinago`, `kanawa-caribe`) no es parte de la voz y no se mide.
    ⟨ch⟩ tampoco: es dígrafo en todas las ortografías del repo.
    """
    voz = clave.lower()
    ultimo = voz.rsplit("-", 1)[-1] if "-" in voz else ""
    if ultimo in _SUFIJOS_DE_LENGUA:
        voz = voz.rsplit("-", 1)[0]
    return [nombre for nombre, patron in _MARCAS_CASTELLANAS if patron.search(voz)]


def forma_de_la_esfera(token: str) -> str:
    """La forma con que una voz de la esfera se enseña y se registra.

    Devuelve el token tal cual si no hay decisión para él. Respeta la
    morfología caquetía igual que `score_linguistico()`: `ta-casabe` es la
    lengua haciendo algo con la raíz ajena, y sale `ta-cazabi`.
    """
    if token in FORMA_DE_LA_ESFERA:
        return FORMA_DE_LA_ESFERA[token]
    for pref in ("ta", "wa", "ma", "ka"):
        if token.startswith(pref + "-"):
            base = token.split("-", 1)[1]
            if base in FORMA_DE_LA_ESFERA:
                return f"{pref}-{FORMA_DE_LA_ESFERA[base]}"
    return token


def score_linguistico(texto: str, lexico: "LexicoComunitario") -> dict:
    """
    Calcula métricas lingüísticas de una respuesta de agente, midiendo
    DENSIDAD arahuaca (vs. español) Y, dentro de esa densidad, cuánto es
    específicamente caquetío vs. préstamo de otra lengua arahuaca viva
    (wayunaiki, lokono, taíno...). El objetivo del proyecto es que el
    caquetío DOMINE — no basta con "no hablar español"; hablar wayunaiki
    en vez de caquetío también es una fuga, solo que más sutil.

    Retorna: palabras_caquetias (SOLO caquetío, y sólo lo que YA es palabra
             activa: es lo que consumen el contagio, la competencia de formas,
             el idiolecto y `words_used`. Una forma recién ACUÑADA no está en
             `palabras_activas()` y por tanto no sale aquí — el orquestador la
             persiste aparte, ver `save_agent_response(coined_words=…)`),
             palabras_arahuacas (todas las arahuacas, caquetío incluido),
             neologismos_propuestos, aspectos_usados, densidad,
             pct_caquetio_especifico, otro_arahuaco, palabras_otro_arahuaco,
             espanol_funcional, score (0-10), observacion.
    """
    limpio = _normalizar(texto)
    tokens = _tokenizar(limpio)
    # Los nombres de los agentes no son vocabulario. Desde la campaña de
    # antropónimos (2026-09-14) 49 de los 63 nombres de la era 2 son homógrafos
    # de una clave del lexicón (Karebe / karebe «cucharón») y el tokenizador
    # pone todo en minúsculas: nombrar a alguien contaba como usar la palabra.
    # Se descartan los nombres del elenco activo y los de la era 1 (que los
    # eventos todavía citan). Consecuencia declarada: «Biro-ko» ya no suma
    # «biro» como uso, tampoco en la era 1.
    # CORREGIDO 2026-09-16: el filtro trabajaba en minúsculas y se comía 52
    # voces del canon homógrafas de un nombre (buko, hayo, mene, saruro,
    # jachos, karebe…), las 52 visibles en el prompt de la era 2 — palabras
    # que el motor enseñaba y no contaba. Ahora la mayúscula decide.
    tokens = _filtrar_nombres(limpio, tokens)
    n_tok = len(tokens) or 1

    activos = set(lexico.palabras_activas())          # base + adoptados

    # match por palabra completa, contando también prefijos posesivos:
    # ta-barsure cuenta como arahuaco aunque "ta-barsure" no esté literal en léxico
    def es_arahuaco(tok: str) -> bool:
        # Prioridad del español: una stopword castellana NUNCA cuenta como
        # arahuaco, aunque colisione con una entrada del léxico (de->lokono,
        # una->lokono, para->proto-arahuaco). Evita el doble conteo que las
        # hacía sumar densidad Y penalizar a la vez.
        if tok in ES_STOPWORDS:
            return False
        # Castellano corriente que también es clave de la comparanda
        # (`cacique`, `taita`, `dia`, `bohío`): NEUTRO. Al no ser arahuaco no
        # entra en `usadas`, y al no ser stopword no entra en `esp_func`: ni
        # densidad ni penalización — sólo diluye, porque sigue contando en
        # n_tok. Sólo el token PELADO: `ta-bohío` lleva morfología caquetía y
        # SÍ es préstamo. Ver CASTELLANO_CORRIENTE, medido el 2026-09-16.
        if tok in CASTELLANO_CORRIENTE:
            return False
        if tok in activos:
            return True
        # `u-` entra con d21.13 (2026-09-21): si el prompt enseña el
        # no-poseído y el scorer no lo reconoce, se repite la patología de
        # `-uto` —se enseña y no se cuenta—, que es justo lo que esta tanda
        # está arreglando. Los cinco prefijos son los mismos que
        # `_PREFIJOS_CAQ`, escritos aquí sin el guion.
        for pref in ("ta", "wa", "ma", "ka", "u"):
            if tok.startswith(pref + "-") and tok.split("-", 1)[1] in activos:
                return True
        # ⚠️ d21.2 («Si, A», 2026-09-21): esta rama admitía cualquier token
        # cuyo primer segmento fuera clave `v_raiz` de CUALQUIERA de las cinco
        # lenguas del lexicón —la mayoría de ellas proto-arahuaco y lokono de
        # la comparanda—, o sea que el andamio de la reconstrucción daba
        # densidad arahuaca. Desde la tanda sólo la da la raíz verbal
        # CAQUETÍA (acción o estativa). Lo que entraba por aquí y ya no entra
        # queda NEUTRO, como el castellano corriente: ni suma densidad ni
        # penaliza, sólo diluye — no se puede penalizar como fuga a otra
        # lengua un token que el propio lexicón no resuelve.
        base = tok.split("-")[0]
        if base in raices_verbales_caquetias():
            return True
        return False

    # Homógrafos español/caquetío: misma forma, distinta lengua. "para" =
    # español "for" vs caquetío "para" (mar), palabra central de la cultura
    # marina caquetía. Se desambiguan por CONTEXTO en vez de sacrificar el
    # caquetío: si un vecino inmediato es arahuaco, es la palabra caquetía;
    # si está rodeada de español, es la preposición.
    HOMOGRAFOS_CAQ = {"para"}

    # Homógrafos de CONTENIDO (glosario Zavala): "bagre", "sabana", "cana"...
    # son caquetío atestiguado, pero su forma coincide con una palabra española
    # corriente. Distinción con los funcionales: si el contexto NO los resuelve
    # como caquetío, no son una fuga al español funcional — simplemente no se
    # cuentan (neutro). Penalizarlos como "el/la/de" sería sobrecastigar.
    usadas = []
    esp_func = []
    for i, t in enumerate(tokens):
        if t in HOMOGRAFOS_CAQ and t in activos:
            ventana = tokens[max(0, i - 1):i] + tokens[i + 1:i + 2]
            if any((v not in ES_STOPWORDS) and es_arahuaco(v) for v in ventana):
                usadas.append(t)       # vecino arahuaco → palabra caquetía (mar)
            else:
                esp_func.append(t)     # rodeada de español → preposición
        elif t in HOMOGRAFOS_ZAVALA and t in activos:
            ventana = tokens[max(0, i - 1):i] + tokens[i + 1:i + 2]
            if any((v not in ES_STOPWORDS) and es_arahuaco(v) for v in ventana):
                usadas.append(t)       # vecino arahuaco → la palabra caquetía
            # si no, se ignora: ni densidad ni penalización
        elif t in GLOTONIMOS_DE_LA_COMPARANDA and t in activos:
            # El nombre de una lengua de la comparación es homógrafo de su
            # sustantivo 'persona' (`wayuu`, `lokono`). Mismo trato que arriba:
            # con vecino arahuaco es la palabra —y entonces penaliza, que es lo
            # que impide que la medición se vuelva circular—; rodeado de
            # castellano es la mención metalingüística y no cuenta. Medido:
            # «Wayunaiki no. Lokono no. Ta lengua, caquetío.» (run c6837386).
            ventana = tokens[max(0, i - 1):i] + tokens[i + 1:i + 2]
            if any((v not in ES_STOPWORDS) and es_arahuaco(v) for v in ventana):
                usadas.append(t)
        elif es_arahuaco(t):
            usadas.append(t)
        elif t in ES_STOPWORDS:
            esp_func.append(t)
    neos     = PATRON_NEOLOGISMO.findall(texto)
    aspectos = _aspectos_morfologicos(tokens)

    # ── Separar caquetío real de préstamo de otra lengua arahuaca viva ──
    familias = {t: _familia_de_token(t) for t in set(usadas)}
    # El homógrafo, cuando el contexto lo resolvió como caquetío, ES caquetío
    # (no proto-arahuaco): "para"=mar es léxico caquetío central, no préstamo.
    for h in HOMOGRAFOS_CAQ:
        if h in familias:
            familias[h] = "caquetío"
    # Un afijo DECLARADO escrito suelto es caquetío. `-ima`, `-uco` e `-iro`
    # son afijos atestiguados (REGLAS_ZAVALA) y los agentes los escriben
    # sueltos al descomponer su propio compuesto: «…tüshi-ima tüshi ima agua
    # fría de quebrada…» (run 89fc1744, tier 1) salía como fuga al lokono por
    # la clave `ima` 'enemigo' de la comparanda. El diccionario no se toca
    # —`ima` sigue siendo una entrada lokono, y `word_source_language` lo
    # devuelve así—: lo que se corrige es la lectura de un texto caquetío.
    # Residuo declarado: un afijo suelto cuenta como palabra caquetía.
    for t in list(familias):
        if "-" not in t and t in _AFIJOS_SUELTOS:
            familias[t] = "caquetío"
    caquetio_tokens = [t for t in usadas if familias[t] == "caquetío"]
    ajenos = [t for t in usadas if familias[t] != "caquetío"]
    # Decisión de Miguel 2026-09-15: las voces de la esfera de contacto se
    # MIDEN APARTE y no penalizan. Una lengua de encrucijada toma prestado de
    # sus vecinos; lo que sí es fuga es hablar la lengua con la que la estamos
    # reconstruyendo (wayunaiki, lokono) o la de otra polity (achagua).
    prestamo_tokens = [t for t in ajenos if familias[t] in ESFERA_DE_CONTACTO]
    otro_arahuaco_tokens = [t for t in ajenos if familias[t] not in ESFERA_DE_CONTACTO]

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
    if prestamo_tokens:
        obs.append(f"préstamo de esfera×{len(prestamo_tokens)}: {', '.join(sorted(set(prestamo_tokens))[:5])}")
    if aspectos: obs.append(f"aspecto: {', '.join(aspectos)}")
    if esp_func: obs.append(f"⚠ español funcional×{len(esp_func)}")
    if neos:     obs.append(f"+{len(neos)} neologismo(s)")
    if score < 5: obs.append("⚠ score bajo — activar rescate")

    return {
        # 2026-09-09: este campo devolvía `usadas` ENTERO — o sea, también las
        # voces de otra lengua arahuaca, pese al nombre. Sus consumidores lo
        # tratan como caquetío: el contagio léxico, la competencia de formas, el
        # idiolecto del agente, el campo léxico de la koiné y la columna
        # `words_used` de la base. Una voz wayuu o lokono habría entrado ahí
        # como si fuera propia. Medido ANTES de tocarlo: en las 1.227 respuestas
        # guardadas `otro_arahuaco` es 0 en todas, así que el cambio no altera
        # ningún dato existente — arregla un defecto latente y no mueve la
        # métrica. Ver 6-fusion/medicion_contaminacion_score_2026-09-09.yaml.
        "palabras_caquetias": list(dict.fromkeys(caquetio_tokens)),
        "palabras_arahuacas": list(dict.fromkeys(usadas)),
        "neologismos_propuestos": [m[0] for m in neos],
        "aspectos_usados": aspectos,
        "densidad": round(densidad, 3),
        "pct_caquetio_especifico": round(pct_caquetio_especifico, 3),
        "otro_arahuaco": len(otro_arahuaco_tokens),
        "palabras_otro_arahuaco": list(dict.fromkeys(otro_arahuaco_tokens)),
        # La esfera de contacto, medida aparte y sin penalizar (2026-09-15).
        # Es el canal por el que se observa la difusión de un préstamo: si una
        # voz de las islas pasa de un tier 1 a los demás, se ve aquí.
        "prestamos_de_esfera": list(dict.fromkeys(prestamo_tokens)),
        "n_prestamos_esfera": len(prestamo_tokens),
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

    # POLÍTICA «MANDA LA ATESTIGUADA» (2026-09-19): `kira` → `jai` y `kali` →
    # `kasi`. ⚠️ Esta plantilla enseña por RECORTE —`verbos[:4]`—, así que la
    # puerta, que la construye con `palabras_usadas=[]`, sólo veía las cuatro
    # primeras de cada lista y NO veía que `kira` y `kali` estaban en la quinta
    # posición: a un agente que ya hubiera dicho las cuatro primeras, el
    # refuerzo le enseñaba la forma derivada. Es un sitio que el criterio
    # estático no alcanza y por eso se cambia la LISTA, no el recorte. (Los
    # respaldos de abajo también las decían literalmente.)
    verbos = [p for p in ["wana","suna","masa","awa","jai","panaa","naba","naa","maa","kaa"] if p not in palabras_usadas]
    conect = [p for p in ["ka","mara","saa","naka","kashi","wara","yama","puna"] if p not in palabras_usadas]
    sust   = [p for p in ["barsure","duna","amana","arima","kasi","suka","bara","kuru"] if p not in palabras_usadas]
    sug_verbos = ", ".join(verbos[:4]) if verbos else "wana, suna, masa, jai"
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
# sin importar el tema. Son las claves `cat` gramaticales que el lexicón usa
# de verdad (la auditoría 2026-09-14 midió que «verbos» no existía como cubo:
# los verbos van en `v_raiz`).
# `v_estativo` entra desde la tanda del 2026-09-21 (d21.4): es un cubo verbal
# como `v_raiz`, y dejarlo fuera habría mandado las diez raíces estativas al
# goteo justo el día en que se declara que son verbos — «la etiqueta LLEGA AL
# PROMPT» es media decisión.
CATEGORIAS_BASE = {"v_raiz", "v_estativo", "pron", "part", "gramatica",
                   "interr", "num", "numerales"}


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


def _muestra_ponderada(opciones, n, pesos):
    """Muestreo SIN reemplazo ponderado por frecuencia comunitaria
    (Efraimidis-Spirakis): peso = 1.0 (base, mantiene exploración de formas
    nuevas) + peso del CampoLexico. Las formas más usadas por la comunidad
    aparecen más en la muestra → se refuerzan (rich-get-richer → curvas S).
    Sin `pesos`, cae al muestreo uniforme de siempre."""
    import random as _random
    n = min(n, len(opciones))
    if not pesos:
        return _random.sample(opciones, n)
    def clave(item):
        w = 1.0 + max(0.0, float(pesos.get(item[0], 0.0)))
        u = _random.random() or 1e-12
        return u ** (1.0 / w)
    return sorted(opciones, key=clave, reverse=True)[:n]


# ── Capa epistémica de una entrada, para los perfiles de run ──────────
# Ver 5-experimento/perfiles_de_run.yaml y curiana_sim/curiana_perfiles.py.
# Un perfil declara qué capas VEN los agentes; esto dice a cuál pertenece
# cada entrada. Se resuelve sobre el `fuente` crudo y no sobre la categoría
# normalizada, porque la normalización manda todas las caquetías al mismo
# saco — que es justo lo que aquí hay que distinguir.
_CAPA_POR_SUFIJO = (
    ("retroabstraido", "caquetío-retroabstraido"),
    ("retro-abstraido", "caquetío-retroabstraido"),
    ("hipotético", "caquetío-hipotético"),
    ("hipotetico", "caquetío-hipotético"),
    ("reconstruido", "caquetío-reconstruido"),
    ("atestiguado", "caquetío-atestiguado"),
)


# F8 (2026-09-12): el conjunto canónico de `fuente`. Cada valor es UNA lengua o
# UNA capa epistémica caquetía; las mezclas («lokono/garifuna», «wayunaiki-cogn»)
# eran pedigríes sin cita y se resolvieron entrada a entrada — ver
# 6-fusion/scripts/sanear_f8_resto.py, que imprime lo que hizo con cada una.
# Un test vigila que ninguna entrada salga de aquí.
FUENTES_CANONICAS = frozenset({
    "caquetío-atestiguado", "caquetío-reconstruido", "caquetío-hipotético",
    "caquetío-retroabstraido",
    "wayunaiki", "lokono", "taíno", "taíno-reconstruido", "kalinago", "paraujano",
    "achagua",   # D11 fase 2 (#121), 2026-09-13: Neira y Ribero 1762 vía lexicon_achagua.py
    "jirajaroide", "proto-arahuaco",
    "caribe-cháima", "caribe-cumanagoto", "español-colonial",
})


def capa_epistemica(fuente: str) -> Optional[str]:
    """La capa de una entrada caquetía, o None si no es caquetía.

    `caquetío` a secas se trata como atestiguado: son seis entradas viejas
    sin precisar, y degradarlas a hipotético sería inventar una duda que
    nadie declaró.
    """
    f = (fuente or "").lower()
    if "caquetio" not in f and "caquetío" not in f:
        return None
    for marca, capa in _CAPA_POR_SUFIJO:
        if marca in f:
            return capa
    return "caquetío-atestiguado"


def repartir_cuotas(tamanos: dict[str, int], n_total: int,
                    relevantes: "Optional[set]" = None,
                    peso_relevante: float = 2.0) -> dict[str, int]:
    """Cuántas voces de cada cubo entran en una muestra de `n_total`.

    Reparto proporcional al tamaño del cubo (resto mayor), con cada cubo
    relevante al contexto pesando `peso_relevante` veces más, un mínimo de una
    voz por cubo no vacío mientras alcance, y nunca más voces que las que el
    cubo tiene. Lo que un cubo no puede llenar se reparte entre los demás.

    Reemplaza el reparto viejo, que daba la muestra entera a cada cubo
    «relevante» y un goteo fijo al resto: como el muestreo agrupa por
    `categoria || cat` y 216 de las 352 voces caquetías del perfil base caen
    en el cubo `sust`, ese cubo recibía 3 voces por prompt mientras 26 voces de
    cubos chicos salían en todos (auditoría 2026-09-14).
    """
    cubos = {c: n for c, n in tamanos.items() if n > 0}
    if not cubos or n_total <= 0:
        return {}
    relevantes = relevantes or set()
    cuotas = {c: 0 for c in cubos}
    restante = n_total
    # 1. Una voz por cubo, mientras alcance (los cubos chicos no desaparecen).
    for c in cubos:
        if restante <= 0:
            break
        cuotas[c] = 1
        restante -= 1
    # 2. El resto, proporcional al tamaño ponderado, sin pasar del tamaño.
    while restante > 0:
        abiertos = {c: n for c, n in cubos.items() if cuotas[c] < n}
        if not abiertos:
            break
        pesos = {c: n * (peso_relevante if c in relevantes else 1.0)
                 for c, n in abiertos.items()}
        total_peso = sum(pesos.values())
        exactas = {c: restante * p / total_peso for c, p in pesos.items()}
        asignadas = 0
        for c in abiertos:
            extra = min(int(exactas[c]), abiertos[c] - cuotas[c])
            cuotas[c] += extra
            asignadas += extra
        if asignadas == 0:
            # Sólo quedan fracciones: por resto mayor, de uno en uno.
            for c in sorted(abiertos, key=lambda k: exactas[k] % 1, reverse=True):
                if restante - asignadas <= 0 or cuotas[c] >= abiertos[c]:
                    continue
                cuotas[c] += 1
                asignadas += 1
        if asignadas == 0:
            break
        restante -= asignadas
    return cuotas


def formas_en_texto(texto: str) -> frozenset:
    """Los tokens de una plantilla, en minúscula, para excluirlos de la
    métrica emergente y del diccionario koiné: lo que el prompt enseña no
    puede contar como convergencia (bitácora del run db946685)."""
    import re as _re
    return frozenset(
        t.lower() for t in _re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:-[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*", texto or "")
        if len(t) >= 2
    )


# ══════════════════════════════════════════════════════════════════════
# LA PUERTA — lo que la plantilla ENSEÑA no es una acuñación
# ══════════════════════════════════════════════════════════════════════
# Una puerta y no dos (corte de serie del 2026-09-18). Antes vivía sólo en
# `curiana_orchestrator_v2._FORMAS_EXCLUIDAS`, que descontaba estas formas de
# la métrica emergente y del diccionario koiné pero NO impedía que se
# registraran como neologismos: `kali-bana` —el ejemplo literal de
# `IDENTIDAD_LINGUISTICA`— se registró, se adoptó, salió «adoptada en dos
# ámbitos» sin haber viajado y el día 2 de la serie C iba GANANDO la
# competencia de «las cuentas» 15,8 contra 3,1 y 2,9. Ahora la lista es una
# sola, vive aquí —donde están las plantillas y el registro— y la importan el
# orquestador (`_FORMAS_EXCLUIDAS`) y `analizar_nodos.formas_excluidas()`.
#
# QUÉ ENTRA: lo que el motor PONE en el prompt como vocabulario o como
# ejemplo. El vocabulario base y las cinco plantillas estáticas que enseñan
# formas: la identidad lingüística, las reglas (completa y breve), el refuerzo
# —sus cuatro tramos— y el rescate —sus tres motivos—. Las dos últimas no
# estaban en `_FORMAS_EXCLUIDAS` y sí enseñan formas: `ma-arua`, `wa-duna`,
# `wana-ni` y `cati` (medido el 2026-09-18).
#
# QUÉ NO ENTRA, y por qué: los bloques que le devuelven al agente lo que la
# COMUNIDAD dijo —`[Palabras nuevas de la comunidad]` (V2), `[Palabras
# propuestas en evaluación]` (V1), `[La comunidad aún busca nombre…]` (V3),
# `[Lo que se dijo aquí]`, `[Tu manera de hablar]`— no son plantilla: son el
# mecanismo que se mide, y excluirlos sería excluir la koiné. Y los que no
# enseñan ninguna forma: `[Tu tierra]` (293 formas, 0 caquetías fuera de esta
# puerta), `[Aquí estás]`, `[Tu emocionar]`. `[Voces de fuera]` y la muestra
# del lexicón enseñan claves de `VOCABULARIO_BASE`, que ya está dentro.

def _textos_de_plantilla() -> list[str]:
    """Las plantillas estáticas que ENSEÑAN formas, cada variante una vez.

    Se construye llamándolas, nunca copiándolas: el ejemplo de la identidad
    cambió de `kali-bana` a `biro-bana` el 2026-09-19 y la puerta se movió
    sola — `kali-bana` salió de la lista y `biro-bana` entró, sin tocar aquí
    un solo carácter. `tests/test_formas_de_plantilla.py` lo fija."""
    textos = [IDENTIDAD_LINGUISTICA, prompt_reglas_completo(), prompt_reglas_breve()]
    # El refuerzo tiene cuatro tramos por score y cada uno enseña lo suyo
    # (el más bajo, `Taya wana-ni…`; el tercero, `ta-barsure, wa-duna, ma-arua`).
    textos += [prompt_refuerzo(s, []) for s in (1.0, 3.0, 5.0, 6.5)]
    # El rescate (segunda pasada) tiene tres motivos; el de la fuga arahuaca
    # enseña las correspondencias `katsi→cati, bara→para, kannoa→canoa`. Se le
    # pasan el texto fallido y la palabra fugada VACÍOS: lo que enseña el tramo
    # es su texto fijo, no lo que el motor le interpole ese turno.
    textos += [prompt_rescate_linguistico("", 0.0, esp, otro)
               for esp, otro in ((0, [""]), (3, [""]), (3, []))]
    return textos


# ⚠️ `FUERA_DEL_HABLA` ENTRA EN LA PUERTA desde el 2026-09-19 (política «manda
# la atestiguada»). Archivar una voz la saca de `VOCABULARIO_BASE`, así que
# sin esto saldría también de la puerta y podría volver como ACUÑACIÓN de la
# comunidad: `kali` —2.321 usos, la forma que la política acaba de retirar—
# habría podido registrarse al día siguiente como palabra nueva, competir por
# un referente y adoptarse. Una forma archivada no es una invención: es una
# palabra que el canon ya tuvo y decidió no hablar. No se enseña Y no compite.
# Entra también el resto del archivo (`piache` y los cinco numerales de D11),
# que hasta hoy sí eran acuñables.
FORMAS_DE_PLANTILLA: frozenset = frozenset(VOCABULARIO_BASE).union(
    frozenset(FUERA_DEL_HABLA),
    *(formas_en_texto(t) for t in _textos_de_plantilla()))


def es_forma_de_plantilla(forma: Optional[str]) -> bool:
    """¿El prompt la enseña, o el canon ya la archivó? No es una acuñación.

    La usan `LexicoComunitario.registrar_neologismo()` (no se registra) y
    `CompetenciaLexica.proponer()` (no compite)."""
    return (forma or "").strip().lower() in FORMAS_DE_PLANTILLA


class _PuertaDelRecuento:
    """Lo que NO cuenta como forma emergente: la plantilla Y la raíz ajena.

    `FORMAS_DE_PLANTILLA` es una lista cerrada y se puede enumerar; la raíz de
    ninguna parte es un PREDICADO y no, así que esto no es un `frozenset` sino
    un objeto que responde a `in`. Los dos consumidores del motor
    (`distancia_idiolectal(excluir=…)` y `CampoLexico.top(excluir=…)`) sólo
    preguntan `forma not in excluir`, que es justo lo que sabe contestar.

    Por qué hace falta además de las dos puertas de registro y competencia: el
    orquestador mete en el campo léxico las formas que el agente ACUÑÓ
    (`campo.registrar([n.forma for n in neos_turno])`) sin preguntar si el
    léxico las aceptó — igual que pasa con las de plantilla desde el corte del
    09-18. Sin esto, `lumina-bana-uco` seguiría saliendo en el «Diccionario
    koiné emergente» del cierre y pesando en la distancia emergente, que es
    la lectura sobre la que se da el veredicto. Corte de serie del 2026-09-20.
    """

    __slots__ = ()

    def __contains__(self, forma) -> bool:
        return es_forma_de_plantilla(forma) or es_raiz_de_ninguna_parte(forma)

    def __bool__(self) -> bool:
        return True

    def __iter__(self):
        # Sólo la mitad enumerable, y quien la recorra tiene que saberlo.
        return iter(FORMAS_DE_PLANTILLA)

    def __repr__(self) -> str:
        return (f"<puerta del recuento: {len(FORMAS_DE_PLANTILLA)} formas de "
                "plantilla + la raíz de ninguna parte>")


PUERTA_DEL_RECUENTO = _PuertaDelRecuento()


def muestra_caquetio_dinamica(n_por_categoria: int = 18, contexto: str = "",
                              pesos: "Optional[dict]" = None,
                              capas: "Optional[frozenset]" = None,
                              n_total: "Optional[int]" = None) -> str:
    """
    Muestra rotativa de vocabulario caquetío (atestiguado + reconstruido),
    agrupada por categoría. `n_total` es el presupuesto de voces del prompt y
    se reparte entre los cubos con repartir_cuotas(): proporcional al tamaño,
    con las categorías relevantes al `contexto` (evento del mundo + ubicación
    + mensaje del turno) pesando el doble. Si no se pasa, se deriva de
    `n_por_categoria` para conservar el presupuesto de la era 1.

    `pesos` (opcional, del CampoLexico): frecuencia comunitaria por forma. Si
    se pasa, la muestra dentro de cada categoría se pondera por esa frecuencia
    (las formas que la comunidad usa más se muestran más → se afianzan). Es el
    muestreo rich-get-richer del diseño koiné.

    Solo entran palabras normalizadas a la familia "caquetío" —
    wayunaiki/lokono/taíno quedan fuera a propósito: son comparanda, no la
    lengua del hablante.

    `capas` (opcional): el conjunto de capas epistémicas del perfil de run
    activo (ver curiana_sim/curiana_perfiles.py). Si se pasa, sólo entran las
    entradas de esas capas — así un brazo `atestiguado` no ve lo reconstruido
    y uno `suelto` sí ve lo retro-abstraído. Si es None, entran todas las
    caquetías, que es como se corrió la era 1.

    ⚠️ Esto cambia lo que el agente VE, no lo que se le PUNTÚA: el score
    cuenta siempre contra todas las capas, o la diferencia entre brazos sería
    un artefacto del instrumento.
    """
    from curiana_database import normalize_source_language

    por_categoria: dict[str, list[tuple[str, str]]] = {}
    for palabra, datos in VOCABULARIO_BASE.items():
        if normalize_source_language(datos.get("fuente", "")) != "caquetío":
            continue
        if capas is not None and capa_epistemica(datos.get("fuente", "")) not in capas:
            continue
        cat = datos.get("categoria") or datos.get("cat") or "otros"
        sig = datos.get("sig") or datos.get("es") or ""
        if not sig:
            continue
        por_categoria.setdefault(cat, []).append((palabra, sig))

    if not por_categoria:
        return ""

    relevantes = CATEGORIAS_BASE | categorias_relevantes(contexto)
    if n_total is None:
        # Compatibilidad con el presupuesto viejo: ~n_por_categoria en los
        # cubos relevantes y un goteo en el resto sumaban unas 2,5 veces
        # n_por_categoria (medido: 50 voces con 20, 42 con 12).
        n_total = int(n_por_categoria * 2.5)
    cuotas = repartir_cuotas(
        {cat: len(ops) for cat, ops in por_categoria.items()},
        n_total, relevantes=relevantes,
    )

    lineas = []
    for cat in sorted(por_categoria):
        n = cuotas.get(cat, 0)
        if n <= 0:
            continue
        muestra = _muestra_ponderada(por_categoria[cat], n, pesos)
        texto = " · ".join(f"{p} ({s})" for p, s in muestra)
        lineas.append(f"  {cat.upper()}: {texto}")

    return (
        "[VOCABULARIO CAQUETÍO ADICIONAL — tu lengua nativa, priorizada según lo "
        "que está pasando este turno. Wayunaiki, lokono y taíno NO son tu lengua, "
        "aunque las reconozcas — usarlas en vez de estas formas caquetías es una "
        "fuga, igual que hablar español]:\n" + "\n".join(lineas)
    )


# ── Quién habla cada lengua de la esfera, dicho como lo diría la gente ──
_QUIEN_HABLA = {
    "taíno": "los de las islas grandes",
    "kalinago": "los caribes que llegan por mar",
    "paraujano": "los del lago, los de las casas sobre el agua",
    "caribe-continental": "los vecinos de tierra firme",
    "jirajaroide-contacto": "los de la sierra",
}

# Lo que viaja en un trueque son cosas, técnicas y nombres de cosas. No viaja
# la gramática, ni los pronombres, ni las partes del cuerpo, ni los adjetivos:
# eso se toma cuando una lengua sustituye a otra, no cuando dos comercian.
# Fuera también los topónimos y etnónimos (`nirgua`, `ayaman`): son nombres
# propios de la comparanda, no vocabulario prestable.
_CAT_NO_PRESTABLE = {"gramatica", "pron", "part", "interr", "num", "numerales",
                     "etnonimia", "cualidades", "cuerpo", "geografia",
                     "parentesco", "acciones"}


# El lexicón desambigua los homógrafos con el nombre de la lengua pegado
# (`kati-kalinago`, `hamaka-kalinago`): esa etiqueta no es parte de la voz.
_SUFIJOS_DE_LENGUA = ("taíno", "kalinago", "paraujano", "caribe",
                      "lokono", "wayunaiki", "jirajaroide")


def _difieren_en_un_caracter(a: str, b: str) -> bool:
    """True si dos cadenas son iguales o distan una sola edición.

    NO es una afirmación fonológica: no decide nada de D5 ni toca el
    inventario. Es una medida de cuánta INFORMACIÓN añade una glosa.
    """
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(1 for x, y in zip(a, b) if x != y) <= 1
    corta, larga = (a, b) if len(a) < len(b) else (b, a)
    return any(larga[:i] + larga[i + 1:] == corta for i in range(len(larga)))


def _es_casi_autoglosa(forma: str, visible: str) -> bool:
    """¿La glosa es la forma otra vez, escrita de otro modo?

    Compara los dos ESQUELETOS FONÉMICOS con los que el proyecto ya compara
    ortografías distintas (`curiana_fonotactica.fonemizar`: c/qu→k, z→s, v→b,
    <h> muda, y→i, x→sh, tildes fuera) y tolera una edición. Con eso caen
    «bohio = bohío» y «guanin = guanín» (tilde), «cazabi = cazabe» (vocal
    final) y «hutia = jutía» (h/j).

    Se prueba TAMBIÉN con la regla abierta <gu> → /w/ (`gu_es_w`, que
    `curiana_fonotactica` deja sin decidir a propósito), porque «iwana =
    iguana» sólo se ve con ella. Usarla aquí no la decide: este módulo no
    toca el inventario ni la fonotáctica, sólo mide si una glosa enseña algo.

    Residuo medido y declarado: «bixa = bija» se escapa (bisha / bija, dos
    ediciones). El <x> colonial y el <j> moderno son la misma consonante, pero
    afirmarlo sería una regla fonológica, y este filtro no es el sitio.
    """
    from curiana_fonotactica import fonemizar
    for gu_es_w in (False, True):
        a, b = fonemizar(forma, gu_es_w), fonemizar(visible, gu_es_w)
        if not a or not b:
            return True
        if _difieren_en_un_caracter(a, b):
            return True
    return False


def _glosa_util(forma: str, sig: str) -> str:
    """El primer trozo de la glosa que ENSEÑA algo, o "".

    13 de las 133 voces de la esfera se glosan a sí mismas («auyama: auyama,
    calabaza»; «cobo: cobo, caracol marino») porque la voz entró al castellano;
    dos no dicen nada más («casabe: casabe», «guayaba: guayaba (Psidium
    guajava)»). Decirle al agente «casabe = casabe» no le enseña nada.

    ⚠ 2026-09-16: el filtro comparaba sólo la coincidencia EXACTA, así que
    dejaba pasar las casi-autoglosas —«cazabi = cazabe», «bohio = bohío»,
    «guanin = guanín»—, donde la glosa se distingue de la forma por la tilde o
    por la ortografía. Ahora se comparan los esqueletos fonémicos; si ningún
    trozo enseña nada, la voz no entra al bloque.
    """
    for trozo in [t.strip() for t in sig.replace(";", ",").split(",") if t.strip()]:
        visible = trozo.split(" (")[0].strip().strip(".")
        if not visible:
            continue
        if visible.lower() in (forma.lower(), forma.lower().split("-")[0]):
            continue
        if _es_casi_autoglosa(forma, visible):
            continue
        if _es_casi_autoglosa(forma.split("-")[0], visible):
            continue
        return trozo
    return ""


def voces_de_fuera_posibles() -> list:
    """Todas las voces que el bloque [Voces de fuera] puede llegar a mostrar.

    `(palabra, forma, glosa, familia)`. Separada de `prompt_voces_de_fuera()`
    para que se pueda medir el catálogo entero sin sortear.

    Desde el 2026-09-18 («la etiqueta manda») lo que sale en `forma` es la
    FORMA DE LA ESFERA, no la clave: la voz con gemela indígena se enseña por
    ella (`casabe` → `cazabi`) y la que fue marcada castellana sin gemela no se
    enseña (`SIN_FORMA_DE_LA_ESFERA`). La glosa se vuelve a medir contra la
    forma que se va a mostrar —si no enseña nada sobre ELLA, la voz cae— y dos
    claves que colapsan en la misma forma (`cacique`/`cacike`) salen una vez.

    Cuando dos claves colapsan, manda la ENTRADA INDÍGENA: se recorren primero
    las claves que no están en `FORMA_DE_LA_ESFERA`, así que `bohio` se enseña
    con su propia glosa («casa redonda de varas y palma») y no con la de
    `bohío`. La castellana sólo aporta la glosa cuando la indígena no tiene
    ninguna que enseñe algo — que es el caso de `maisi`, cuya glosa entera es
    «maíz (Zea mays)» y el filtro de autoglosa descarta.
    """
    from curiana_database import normalize_source_language

    candidatas = []
    vistas = set()
    orden = sorted(VOCABULARIO_BASE.items(),
                   key=lambda kv: kv[0] in FORMA_DE_LA_ESFERA)
    for palabra, datos in orden:
        fam = normalize_source_language(datos.get("fuente", ""))
        if fam not in ESFERA_DE_CONTACTO:
            continue
        cat = datos.get("categoria") or datos.get("cat") or ""
        if cat in _CAT_NO_PRESTABLE:
            continue
        sig = datos.get("sig") or datos.get("es") or ""
        if not sig:
            continue
        if palabra in SIN_FORMA_DE_LA_ESFERA:
            continue
        ultimo = palabra.rsplit("-", 1)[-1] if "-" in palabra else ""
        forma = palabra.rsplit("-", 1)[0] if ultimo in _SUFIJOS_DE_LENGUA else palabra
        # Si al quitar la etiqueta la forma coincide con una voz caquetía
        # (`hamaka`, `kanoa`, `casabe`), NO entra: enseñar como ajena una
        # palabra que el agente ya tiene por propia es peor que no enseñar nada.
        if forma != palabra and forma in VOCABULARIO_BASE:
            continue
        forma = forma_de_la_esfera(forma)
        if forma in vistas:
            continue
        glosa = _glosa_util(forma, sig)
        if not glosa:
            continue
        vistas.add(forma)
        candidatas.append((palabra, forma, glosa, fam))
    return candidatas


def prompt_voces_de_fuera(contexto: str = "", n: int = 3) -> str:
    """Las voces de la esfera de contacto que un tier 1 conoce por su trato.

    Decisión de Miguel (2026-09-15): «los de tier 1 no sólo conocían su
    lenguaje sino el de su esfera de influencia». Sólo tier 1, sólo unas
    pocas, y SIEMPRE marcadas como ajenas — el agente tiene que saber que no
    es su lengua, o el préstamo deja de ser un préstamo. Ver ESFERA_DE_CONTACTO.

    Y desde el 2026-09-18 («la etiqueta manda») lo que se le enseña es la FORMA
    DE LA ESFERA, nunca la grafía castellana: el bloque decía «maíz = planta de
    maíz» y ahora dice «maisi = …». La clave castellana sigue siendo la que
    RECONOCE el scorer —el agente puede escribir «casabe» y cuenta—, pero no se
    le enseña. Ver `FORMA_DE_LA_ESFERA` y `voces_de_fuera_posibles()`.
    """
    import random as _rnd

    candidatas = voces_de_fuera_posibles()
    if not candidatas:
        return ""

    relevantes = categorias_relevantes(contexto) if contexto else set()
    if relevantes:
        pesadas = [c for c in candidatas
                   if (VOCABULARIO_BASE[c[0]].get("categoria") or "") in relevantes]
        candidatas = pesadas + candidatas if pesadas else candidatas

    elegidas = _rnd.sample(candidatas, min(n, len(candidatas)))
    partes = []
    for _palabra, forma, glosa, fam in elegidas:
        partes.append(f"{forma} = {glosa} ({_QUIEN_HABLA.get(fam, 'los de fuera')})")
    return ("[Voces de fuera — no son tu lengua; las sabes por tu trato, y usarlas "
            "te marca como quien va y viene]: " + "; ".join(partes))


def vocabulario_para_agente(tier: int, lexico: "LexicoComunitario", contexto: str = "",
                            pesos: "Optional[dict]" = None,
                            capas: "Optional[frozenset]" = None,
                            ambito: "Optional[str]" = None) -> str:
    """
    Genera el bloque de léxico + reglas apropiado para cada tier.
    Tier I: completo con identidad nativa. Tier II: breve. Tier III: solo sufijos.

    `contexto` (opcional): texto del turno (evento del mundo + ubicación +
    mensaje al agente) usado para priorizar qué categorías del lexicón
    mostrar en grande (chunking por palabras clave, ver categorias_relevantes).
    `pesos` (opcional, del CampoLexico): pondera la muestra por frecuencia
    comunitaria (rich-get-richer; ver muestra_caquetio_dinamica).
    `ambito` (opcional, capa 2 de la escena): el LUGAR que FILTRA lo que el
    agente ve, tal y como lo devuelve `curiana_escena.ambito_visible_de()` —no
    `ambito_de()`: el día de Capubana se está en el cerro pero se ve todo, y
    esa puerta es la que lo sabe. Filtra las dos vías comunitarias del bloque
    —las adoptadas (V2) y las propuestas (V1)—: se ve lo que se dijo aquí, no
    lo que dijo la comunidad entera. `None` deja el bloque byte a byte como
    estaba (era 1, era 2 sin `--escena`, y el día de la convergencia).
    """
    lexico_activo = prompt_lexico_activo(lexico, ambito)
    pendientes = prompt_pendientes_evaluacion(lexico, ambito)

    if tier == 1:
        base = prompt_reglas_completo()
    else:
        # Tier 2 y tier 3. El tier 3 veía una línea con 4 verbos y 3 conectores
        # y ninguna muestra (medido el 2026-09-14: 221 caracteres): con eso no
        # podía hablar. Desde la era 2 («que todos los agentes hablen») ve las
        # reglas breves y una muestra chica; sigue sabiendo menos que un adulto.
        base = prompt_reglas_breve()

    partes = [base]
    # Presupuesto por tier = el que la era 1 mandaba de hecho a los tier 1 y 2
    # (50 y 42 voces, medido en la auditoría 2026-09-14), para que arreglar el
    # reparto no alargue el prompt: su longitud predice el score. El tier 3
    # recibe 20.
    n_total = {1: 50, 2: 42}.get(tier, 20)
    muestra = muestra_caquetio_dinamica(
        n_por_categoria=20 if tier == 1 else 12, contexto=contexto,
        pesos=pesos, capas=capas, n_total=n_total,
    )
    if muestra:
        partes.append(muestra)
    # Sólo el tier 1: es quien navega, comercia y recibe al forastero
    # (Dara-ko el navegante, Kadushi el de la rama insular, Biro-ko el de la
    # sal). Decisión de Miguel 2026-09-15.
    if tier == 1:
        fuera = prompt_voces_de_fuera(contexto)
        if fuera:
            partes.append(fuera)
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
        "Taya wana-ka arima wara kari. "
        "Ta-barsure maa-ni: Manaure naa-da kashi. "
        "[sima-bana: sima+-bana = la cumbre del cerro]. "
        "Saa pia naa-da buco-ana, naka taya naa-da ka pia."
    )
    resultado = score_linguistico(texto_test, lc)
    print("── Test score (frase ideal) ──")
    print(f"  Score: {resultado['score']}/10")
    print(f"  {resultado['observacion']}")
