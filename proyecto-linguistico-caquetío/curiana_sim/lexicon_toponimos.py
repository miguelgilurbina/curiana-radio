# -*- coding: utf-8 -*-
"""
CURIANA — Propuesta F11: descomposición del corpus toponímico y antroponímico
=============================================================================

**Propuesta CURADA A MANO.** `minar_toponimos.py` produce los candidatos y las
cuentas de recurrencia; este módulo es el veredicto humano sobre ellos, con la
razón escrita al lado. El automatismo no decide: en un método que consiste en
cortar palabras hasta que cuadren, dejar decidir al algoritmo *es* el error.

**Ninguna de estas formas entra a `VOCABULARIO_BASE` por este camino.** El
destino natural es el mismo que el del protocolo de minado
(`investigacion/disenos/02_protocolo_habla_paraguanera.md` §5): corpus y lista
de candidatas, revisión humana explícita después.

Documento de método y resultados:
    investigacion/disenos/03_descomposicion_toponimica.md

Escala de veredicto:
    A — segmentación confirmada: todos los morfemas ya atestiguados y la glosa
        se reconstruye con ellos.  (`jurijurebo` es el caso tipo.)
    B — un morfema nuevo despejado, con recurrencia ≥2 y glosa consistente.
    C — segmentación plausible sin recurrencia. Se registra, no se promueve.
    D — descartada, con la razón.
"""

FUENTES = (
    "Zavala Reyes 2015 (TOPONIMOS_ZAVALA 45 + ANTROPONIMOS_ZAVALA 14, con glosa "
    "española) · Gatschet 1885 (31 topónimos de Aruba, sin glosa) · "
    "van Buurt 2014 §7 (176 topónimos ABC, sin glosa) y §8-10 (15 etimologías "
    "comentadas por el autor)"
)

# ───────────────────────────────────────────────────────────────────────────
# NIVEL A — segmentación confirmada
# ───────────────────────────────────────────────────────────────────────────
# Todos los morfemas ya estaban atestiguados ANTES de este análisis, y la glosa
# que da la fuente se reconstruye con ellos. Son las ecuaciones cerradas.

NIVEL_A = {
    "jurijurebo": {
        "clase": "topónimo",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Paso de los vientos",
        "segmentacion": "juri~juri + ebo",
        "morfemas": {
            "juri": "viento, ventarrón  [lexicón, caquetío-atestiguado, Zavala #178]",
            "ebo": "camino, paso, senda  [lexicón, caquetío-atestiguado, Zavala #117]",
        },
        "glosa_reconstruida": "viento(-viento) + paso = 'paso de los vientos'",
        "razon": "los dos morfemas ya estaban en el lexicón y la traducción "
                 "cierra sin residuo. La reduplicación juri~juri explica el "
                 "PLURAL de la glosa ('los vientos', no 'el viento'); la "
                 "segunda copia pierde la vocal final por haplología "
                 "(juri-jur-ebo).",
        "observacion": "Estaba archivado en TOPONIMOS_ZAVALA como 'glosa "
                       "incierta' y fuera del habla. Es el caso que originó "
                       "toda la tarea F11. Formas atestiguadas (2026-09-07): "
                       "Hurihurebo (Bastidas 1538, AGI, «pueblo de la Provincia "
                       "de Paraguaná»), Hurehurebo (Castellanos 1589, II-1, «Señor "
                       "de la ciudad Hurehurebo» y en la lista de las once "
                       "ciudades), Jurijurebo (Zavala, Esteves p. 47: «lugar al "
                       "norte de Pueblo Nuevo, cercano a El Vínculo; todavía hay "
                       "vestigios de su cementerio»).",
        # La tercera voz: lecturas que conviven sin pisar la glosa impresa ni
        # la segmentación (esquema en 2-lengua/datos-de-lengua.md).
        "lecturas": [
            {"tipo": "etimologia-analitica",
             "lectura": "hure 'arena' -> hurehure 'arenal' -> hurehurebo 'lugar de "
                        "muchos arenales' (reduplicación + sufijo -bo)",
             "quien": "González Batista", "fecha": "2026-08-25", "eje": "significado",
             "procedencia": dict(obra="gonzalez-batista-nombre-de-coro"),
             "veredicto": "descartada como lectura principal (2026-08-25): Zavala "
                          "#178-179 tiene glosa impresa y juri~juri + ebo cierra sin "
                          "residuo; el propio autor la da como conjetura («si hure "
                          "fuera como creemos»). Se conserva por D7. Detalle: "
                          "6-fusion/toponimia_coro_espina.yaml §veredicto-jurijurebo"},
            {"tipo": "testimonio-residente",
             "lectura": "Jurijurebo está en Judibana (Paraguaná); judi y juri son la "
                        "misma palabra deformada, y el viento es el rasgo dominante "
                        "del sitio: el topónimo moderno y el antiguo comparten raíz "
                        "y referente",
             "quien": "Miguel Gil Urbina, residente en Judibana", "fecha": "2026-08-25",
             "eje": "referente",
             "apoyo": "converge con la ubicación que dan las fuentes divulgativas "
                      "(esteves-1989) y con la tradición local de Judibana "
                      "(velasco-2015-resistencia §judibana_tradicion)"},
        ],
    },
    "yacarebacoa": {
        "clase": "topónimo",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Pueblo del bosque",
        "segmentacion": "yacare + bacoa",
        "morfemas": {
            "yacare": "pueblo  [despejado — ver MORFEMAS_DESPEJADOS]",
            "bacoa": "bosque, lugar, paraje, sitio fértil  [lexicón, "
                     "caquetío-atestiguado]",
        },
        "glosa_reconstruida": "pueblo + bosque = 'pueblo del bosque'",
        "razon": "`yacare` aparece en el propio corpus de Zavala con glosa "
                 "'Pueblo. Caimán'; `bacoa` está en el lexicón. La ecuación "
                 "cierra pieza por pieza y en el mismo orden.",
    },
    "quibacoas": {
        "clase": "topónimo",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Bosques pedregosos",
        "segmentacion": "quiba + (b)acoa   [haplología de la sílaba -ba-]",
        "morfemas": {
            "quiba": "piedra, roca  [lexicón `quiva`/`cuiva`; van Buurt §8 "
                     "'siba or quiba means stone or rock']",
            "bacoa": "bosque, lugar, paraje, sitio fértil  [lexicón, "
                     "caquetío-atestiguado]",
        },
        "glosa_reconstruida": "piedra + bosque = 'bosques pedregosos'",
        "razon": "la `-s` final es plural castellano de Zavala, no caquetío. "
                 "Resuelto, corrobora las dos piezas a la vez.",
        "observacion": "⚠ Resuelve un problema del lexicón: hay una entrada "
                       "`quiba` = 'ayuda' (Zavala #203) y otra `quiva`/`cuiva` "
                       "= 'piedra'. El topónimo, con glosa 'pedregosos', "
                       "confirma 'piedra' — y coincide con van Buurt. Ver "
                       "CONFLICTOS. (Cerrado el 2026-08-31: ambas fusionadas "
                       "como `kiba`, homónimos declarados; el sentido piedra "
                       "lleva el sig activo.)",
    },
    "cumarebo": {
        "clase": "topónimo",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Camino del cacique Cumare",
        "segmentacion": "Cumare + ebo",
        "morfemas": {
            "Cumare": "antropónimo — la propia fuente lo identifica como el "
                      "nombre del cacique",
            "ebo": "camino, paso, senda  [lexicón, caquetío-atestiguado]",
        },
        "glosa_reconstruida": "Cumare + camino = 'camino de Cumare'",
        "razon": "la glosa NOMBRA su propia clave: Zavala dice de quién es el "
                 "camino. El único morfema léxico es `ebo`, y encaja. Segunda "
                 "atestación independiente de `ebo` (la otra es `jurijurebo`).",
    },
    "guacaubana": {
        "clase": "topónimo",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Río escondido",
        "segmentacion": "guaca/waka + -ubana",
        "morfemas": {
            "waka": "subterráneo, bajo tierra  [van Buurt §6, vía Oliver 1989; "
                    "sostiene `sawaka` 'inframundo']",
            "-ubana": "desinencia  [AFIJOS_ZAVALA, Zavala #265, sin valor "
                      "precisado por la fuente]",
        },
        "glosa_reconstruida": "bajo tierra + (desinencia) = 'río escondido'",
        "razon": "'escondido' ← waka 'bajo tierra' es una alineación limpia, y "
                 "el compuesto recurre en la isla: **Wakubana / Wacobana** "
                 "(Aruba, mapa de 1825; Gatschet 1885 lo registra igual). Dos "
                 "atestaciones separadas por el mar y por 130 años.",
        "observacion": "⚠ A con reserva: `-ubana` sigue sin glosa, así que la "
                       "parte 'río' de la traducción NO queda explicada por "
                       "ningún morfema. La ecuación cierra a medias.",
    },
    "barisi": {
        "clase": "topónimo",
        "subtipo": "identidad — corrobora, no descompone",
        "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Región de tierras coloradas cerca del mar",
        "segmentacion": "barisi (= `barici` del lexicón, misma forma)",
        "morfemas": {
            "barici": "agua turbia, tierras coloradas rojizas  [lexicón, "
                      "caquetío-atestiguado]",
        },
        "glosa_reconstruida": "'tierras coloradas' ← barici, literal",
        "razon": "no hay composición que resolver: el topónimo ES la palabra. "
                 "Pero la coincidencia de glosa entre la entrada del glosario y "
                 "la del listado toponímico es corroboración interna, y no "
                 "estaba registrada.",
    },
    # ── La campaña de Esteves 1989, lote 1 (2026-09-06) — ver NIVEL_B ──
    "judibana": {
        "id": "toponimo-075",
        "clase": "topónimo", "fuente": "esteves-1989", "pagina": 47,
        "glosa_fuente": "Judi, jurí: viento. Bana: sitio alto",
        "segmentacion": "judi + bana",
        "morfemas": {
            "judi": "viento  [= juri, lexicón caquetío-atestiguado, Zavala #178; "
                    "la variante judi la da Esteves]",
            "bana": "cerro, sitio alto  [lexicón caquetío-atestiguado, Zavala "
                    "#26; D9 resuelta 2026-08-31]",
        },
        "glosa_reconstruida": "viento + sitio alto = 'el cerro del viento'",
        "razon": "Esteves da la segmentación y las dos glosas, y los dos "
                 "morfemas ya estaban atestiguados por otra fuente (Zavala): la "
                 "ecuación cierra sin residuo. Sexta atestación de bana 'cerro' "
                 "en Esteves y la que trae la variante judi de juri (r~d), la "
                 "misma raíz de jurijurebo (toponimo-001) y del hudi de "
                 "Hudishibana (Aruba).",
        "observacion": "«Antiguamente era un fundo pecuario de la aldea de "
                       "Guanadito, hoy es una moderna ciudad del municipio Los "
                       "Taques.» Es el pueblo donde se crió Miguel: el único "
                       "topónimo del canon con testimonio de residente. Nombra "
                       "también a la hija de Manaure en la tradición local — "
                       "significado ≠ referente: la etimología vale igual si "
                       "nombra al cerro o a la persona.",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "el viento es el rasgo dominante del sitio y de Paraguaná "
                        "entera; judi y juri son la misma palabra deformada, y el "
                        "topónimo moderno y el antiguo (Jurijurebo) comparten raíz "
                        "y referente",
             "quien": "Miguel Gil Urbina, residente en Judibana", "fecha": "2026-08-25",
             "eje": "ambos"},
            {"tipo": "tradicion-local",
             "lectura": "«Judibana era una hermosa mujer, que era esposa del Gran "
                        "Cacique de Jurijurebo»",
             "quien": "leyenda que recoge Esteves", "fecha": "2026-09-06",
             "eje": "referente", "procedencia": dict(obra="esteves-1989", pagina=47),
             "veredicto": "el propio autor: «Es pura leyenda, nada consta en "
                          "documentos»"},
            {"tipo": "testimonio-residente",
             "lectura": "Judibana era el nombre de la hija del cacique Manaure, "
                        "unida al señor de Jurijurebo, al que mataron con perros: "
                        "así lo tenía desde niño, antes de leer a Velasco",
             "quien": "Miguel Gil Urbina, criado en Judibana", "fecha": "2026-08-25",
             "eje": "referente",
             "apoyo": "Velasco 2015 recoge la misma tradición; dos receptores "
                      "independientes salvo fuente común reciente (reserva "
                      "declarada en velasco-2015-resistencia §judibana_tradicion)"},
            {"tipo": "hipotesis",
             "lectura": "doña Juana, la mujer del señor de Hurehurebo bautizada en "
                        "casa de Ampiés (Castellanos 1589, línea 48166), sería el "
                        "bautismo de Judibana: Ju[dib]ana → Juana por truncamiento",
             "quien": "proyecto", "fecha": "2026-08-25", "eje": "referente",
             "veredicto": "no demostrada: la homofonía puede ser casual y la "
                          "tradición pudo derivar el nombre desde el verso "
                          "(castellanos_1589_toponimos.yaml §3)"},
        ],
    },
    # ── Lote 4 (2026-09-07): los del mapa de Miguel que «no estaban» en
    # Esteves — estaban, con otra grafía. Un nombre que sigue vivo es dato.
    "yauquiba": {
        "id": "toponimo-105",
        "clase": "topónimo", "fuente": "esteves-1989", "pagina": 67,
        "glosa_fuente": "Yabu-quiba: la piedra del yabo, árbol resinoso",
        "segmentacion": "yabu + quiba",
        "morfemas": {
            "yabo": "cercidium, árbol resinoso  [lexicón caquetío-atestiguado, "
                    "Zavala — la misma glosa que da Esteves]",
            "kiba": "piedra  [lexicón caquetío-atestiguado, Zavala #92/#218]",
        },
        "glosa_reconstruida": "yabo + piedra = 'la piedra del yabo'",
        "razon": "Esteves segmenta y glosa, y los dos morfemas ya estaban "
                 "atestiguados por Zavala con las mismas glosas: cierra sin "
                 "residuo. Séptima forma de la familia -quiba de Paraguaná.",
        "observacion": "Población del municipio Moruy; 1881: 26 casas, 199 "
                       "vecinos. ⭐ La cabecera de Esteves dice Yauquiba, pero su "
                       "propia segmentación dice Yabu-quiba — y el mapa vivo "
                       "(fotos de Miguel, 2026-09-01: YABUQUIVA) conserva la b "
                       "del étimo que el libro perdió en la cabecera. El nombre "
                       "en uso es más fiel que el gazeteer.",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "vivo en el mapa actual como Yabuquiva, sector del "
                        "Capubana; con Jadacaquiva hace crecer la familia "
                        "-quiva/-quiba de la península",
             "quien": "Miguel Gil Urbina (fotos del mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
}

# ───────────────────────────────────────────────────────────────────────────
# NIVEL B — morfema nuevo despejado, recurrencia ≥2
# ───────────────────────────────────────────────────────────────────────────

NIVEL_B = {
    # ── Lote 6 (2026-09-07): del censo de -ana para #109. Es el capubana
    # 'duende del cerro' de Zavala #61, escrito por Esteves con h. Y la
    # percha de la hipótesis del centro sagrado de Miguel (2026-09-01). ──
    "capuhana": {
        "id": "toponimo-113", "clase": "topónimo", "fuente": "esteves-1989",
        "pagina": 26,
        "glosa_fuente": "«Capu-hana, con hache intercalada para deshacer el "
                        "diptongo, es el nombre de un pequeño cerro, cerca de "
                        "Misaray. Quiere decir: el cerro del duende. Capú: duende, "
                        "ente sobrenatural. Bana: cerro, sitio alto»",
        "segmentacion": "capu + (h)ana   [< capu + bana, con b > h intervocálica]",
        "morfemas": {
            "capu": "duende, espíritu protector de los árboles  [capo/capú del "
                    "lexicón; Zavala #61 capubana 'duende del cerro']",
            "bana": "cerro, sitio alto  [D9, resuelta 2026-08-31; el «Barna» del "
                    "OCR es Bana]",
        },
        "glosa_reconstruida": "cerro del duende",
        "razon": "dos morfemas atestiguados, glosa impresa y referente dicho (un "
                 "cerro). Segunda atestación del compuesto capubana, ahora como "
                 "topónimo y con el núcleo al final: Esteves lee 'el cerro del "
                 "duende' donde Zavala glosaba 'duende del cerro', y el referente "
                 "decide. B y no A porque la forma con h es de Esteves y la "
                 "identificación con el capubana de Zavala es nuestra.",
        "observacion": "Alternancia b~h intervocálica: permutación nueva para la "
                       "skill. En el mapa vivo: «Cerro Capuana» (OSM, 11.844 "
                       "-69.896), unos 6 km al NE de la cumbre del Cerro Santa "
                       "Ana; Esteves lo llama «pequeño cerro cerca de Misaray». "
                       "Tensión con la lectura de Miguel, que identifica el "
                       "Capubana con el Cerro Santa Ana entero: o son dos "
                       "Capubana o el nombre bajó del cerro grande al pequeño.",
        "lecturas": [
            {"tipo": "hipotesis",
             "lectura": "el Capubana es el Cerro Santa Ana (el Cerro de Capú, "
                        "D9/Velasco) y el centro sagrado del sector: Moruy, donde "
                        "se hacía el merejuy para la chicha ritual, a su izquierda; "
                        "Chamuriana, con el agua que baja del cerro, al sur; "
                        "Cayerúa al norte. Sitios con funciones rituales distintas "
                        "organizados en torno a la morada del dueño Capo",
             "quien": "Miguel Gil Urbina", "fecha": "2026-09-01", "eje": "referente",
             "apoyo": "Velasco: el cerro se llamaba Cerro de Capú; Salas: la "
                      "cabecera religiosa del polity en Paraguaná; Oliver p. 275: "
                      "silencio de cronistas sobre lo ritual («quite secretive»)",
             "veredicto": "canon-simulación como modelo espacial (Claude, "
                          "2026-09-01): ninguna fuente lo dice así de explícito, "
                          "pero es consistente con tres piezas canónicas. Esteves "
                          "da el nombre a un cerro pequeño cerca de Misaray, no al "
                          "macizo. Detalle: 6-fusion/toponimia_paraguana_miguel.yaml "
                          "§capubana-centro-sagrado"},
            {"tipo": "tradicion-local",
             "lectura": "en el cerro de Capuhana hay un duende que, junto con una "
                        "serpiente emplumada con una estrella en la cabeza, impide "
                        "que sean cortados los árboles de la localidad; Esteves lo "
                        "emparenta con la leyenda de la serpiente emplumada del "
                        "Guárico, «cuyos primitivos habitantes eran también de "
                        "ascendencia caquetía»",
             "quien": "tradición local recogida por Francisco Tamayo, vía Esteves "
                      "1989", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="esteves-1989", pagina=26)},
        ],
    },
    "adabacoa": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Todo arboleda",
        "segmentacion": "ada + bacoa",
        "despeja": "ada",
        "razon": "con `bacoa` = 'bosque' ya puesto, el resto tiene que valer "
                 "'árbol'. Recurre en `guadabacoa` 'Arboleda' (wa-ada-bacoa).",
    },
    "guadabacoa": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Arboleda",
        "segmentacion": "wa- + ada + bacoa   [haplología de -a-]",
        "despeja": "ada",
        "razon": "segunda aparición de `ada`, con la misma glosa que la "
                 "primera. El `wa-` inicial es el prefijo de pluralidad de van "
                 "Buurt §6 (de Goeje 1928), lo que explica que Zavala glose "
                 "`adabacoa` 'TODO arboleda' y este simplemente 'arboleda'.",
        "observacion": "⚠ (2026-09-07) Es el mismo nombre que Esteves escribe "
                       "Guaidabacoa («Guadabacoa es como está escrito en el "
                       "censo de 1881», p. 39: lugar pecuario al norte de "
                       "Jadacaquiva, 2 casas, 35 habitantes) y que González "
                       "Batista analiza como Guaibacoa. Dos segmentaciones "
                       "compiten con morfemas atestiguados las dos: wa-ada-bacoa "
                       "'arboleda' (Zavala) y way-bacoa 'sitio de guái, el árbol "
                       "parecido a la ceiba' (Esteves y González Batista, "
                       "independientes). Se conserva la de Zavala como principal "
                       "por ser la que glosa 'arboleda'; las otras van en "
                       "lecturas. Formas antiguas: Guaybacoa entre las once "
                       "ciudades de Castellanos (1589) y Guaibacoa en la carta de "
                       "Bastidas (1538, nodo-003) — la identificación con ESTE "
                       "lugar no está demostrada.",
        "lecturas": [
            {"tipo": "glosa-fuente",
             "lectura": "«Guaidabacoa, con sílaba epentética intercalada, es una "
                        "voz compuesta de guái, árbol parecido a la ceiba y "
                        "bacoa: sitio, paraje»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=39),
             "veredicto": "way 'árbol parecido a la ceiba' es caquetío-atestiguado "
                          "en el lexicón: la ecuación también cierra por aquí. "
                          "Conflicto de segmentación declarado, sin resolver"},
            {"tipo": "etimologia-analitica",
             "lectura": "Guaibacoa = 'el valle (bacoa) de las ceibas (guay)'",
             "quien": "González Batista", "fecha": "2026-08-25", "eje": "significado",
             "procedencia": dict(obra="gonzalez-batista-nombre-de-coro"),
             "veredicto": "coincide con Esteves por vía independiente; 'valle' es "
                          "matiz suyo de bacoa"},
            {"tipo": "hipotesis",
             "lectura": "la Guaybacoa «ciudad de grandísimo momento» de Castellanos "
                        "(1589) y la Guaibacoa de Bastidas (1538) serían este "
                        "mismo lugar del norte de Jadacaquiva",
             "quien": "proyecto", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="castellanos-elegias", pagina="185 (línea 48252)"),
             "veredicto": "no demostrada: Castellanos dice «doce leguas en torno» "
                          "de Coro, y Paraguaná cabe; pero nadie fija el sitio"},
        ],
    },
    "bobare": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Sitio de cultivo", "segmentacion": "bob(o) + -are",
        "despeja": "-are",
        "razon": "cuatro topónimos en -are glosados 'Sitio de X'.",
    },
    "cabudare": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "sitio de cultivo", "segmentacion": "cabud- + -are",
        "despeja": "-are", "razon": "ídem.",
    },
    "dabudare": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Sitio de extracción de barro",
        "segmentacion": "dabuda + -re",
        "despeja": "-are",
        "razon": "el mejor de los cuatro: `dabuda` = 'barro loza' YA está en el "
                 "lexicón como caquetío-atestiguado, así que la ecuación deja "
                 "el sufijo despejado contra un morfema conocido, no contra un "
                 "hueco.",
        "observacion": "(2026-09-07) Tres grafías, un lugar probable: Dabudare "
                       "(Zavala), Dabadubare (Esteves p. 37: «aldea del "
                       "municipio Santa Ana. Dabuda: barro de loza») y "
                       "Davaduvare en el mapa vivo (fotos de Miguel, sector del "
                       "Capubana). La identificación no está demostrada; el "
                       "cruce se registra aquí y no como entrada nueva.",
        "lecturas": [
            {"tipo": "glosa-fuente",
             "lectura": "Dabadubare, aldea del municipio Santa Ana: «Dabuda: "
                        "barro de loza (ver Abudure)»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "ambos",
             "procedencia": dict(obra="esteves-1989", pagina=37),
             "veredicto": "misma raíz dabuda que Zavala; Esteves no glosa el "
                          "resto (-bare ~ -are 'sitio de')"},
            {"tipo": "testimonio-residente",
             "lectura": "vivo en el mapa actual como Davaduvare, sector del "
                        "Capubana, junto a Uarayadito y Cayerúa",
             "quien": "Miguel Gil Urbina (fotos del mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
    "pachacuare": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Sitio de palmeras", "segmentacion": "pachacu + -are",
        "despeja": "-are", "razon": "ídem.",
    },
    "bariquisimeto": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Río de aguas turbias",
        "segmentacion": "bari- + -quisimeto",
        "despeja": "bari-",
        "razon": "junto con `barisi` 'tierras coloradas', dos topónimos donde "
                 "`bari-` cubre el color rojizo/turbio. El lexicón ya tiene "
                 "`barici` 'agua turbia' y `bariki` 'tierra colorada': el par "
                 "toponímico sugiere que son **variantes de una misma raíz** "
                 "`bari-`, no dos palabras.",
        "observacion": "El residuo `-quisimeto` queda sin explicar y sin "
                       "recurrencia: la parte 'río' de la glosa no se "
                       "reconstruye.",
    },
    "yacare": {
        "clase": "topónimo", "fuente": "zavala-reyes-2015",
        "glosa_fuente": "Pueblo. Caimán",
        "segmentacion": "yacare (sin composición)",
        "despeja": "yacare",
        "razon": "la propia entrada glosa 'Pueblo', y `yacarebacoa` 'Pueblo del "
                 "bosque' lo confirma en composición. Dos apoyos.",
        "observacion": "⚠ La glosa doble 'Pueblo. Caimán' es sospechosa: "
                       "*yacaré* 'caimán' es un tupí-guaraní panamericano que "
                       "entró al español general. Puede haber contaminación de "
                       "la glosa. El valor 'pueblo' se apoya en "
                       "`yacarebacoa`; el valor 'caimán' NO se usa aquí.",
    },
    # ── La campaña de Esteves 1989, lote 1 (2026-09-06): los del mapa de Miguel
    # que están en el índice del libro. Ids explícitos desde 075: los 74 de
    # arriba no se mueven (otros archivos los citan). `pagina` es la del libro.
    "abudure": {
        "id": "toponimo-076",
        "clase": "topónimo", "fuente": "esteves-1989", "pagina": 11,
        "glosa_fuente": "sitio de donde se extrae barro de las raíces",
        "segmentacion": "(a)dabuda + ure   [aféresis de la d- inicial]",
        "despeja": "ure",
        "razon": "Esteves segmenta y glosa: «voz compuesta de dabuda y ure, que "
                 "literalmente expresa: barro y raíz». `dabuda` 'barro loza' ya "
                 "es caquetío-atestiguado en el lexicón (Zavala) y `ure` 'raíz' "
                 "también; el autor lo verifica en el terreno («gruesas vetas de "
                 "barro de loza en los cangilones labrados por la lluvia»). Con "
                 "`dabudare` (toponimo-011) la raíz queda en dos topónimos con "
                 "dos sufijos.",
        "observacion": "⚠ El valor de `-ure` sigue en conflicto declarado: "
                       "Esteves lo lee literal ('raíz', «presente en muchos "
                       "topónimos indígenas de Paraguaná»); el proyecto tenía "
                       "-ure ~ -are 'sitio de'. Aquí las dos dan casi lo mismo. "
                       "Aldea al SO de Moruy; censo 1881: 6 casas, 50 vecinos. "
                       "Vivo en el mapa (fotos de Miguel, 2026-09-01).",
    },
    "buchuhaco": {
        "id": "toponimo-086",
        "clase": "topónimo", "fuente": "esteves-1989", "pagina": 24,
        "glosa_fuente": "los dos buches. Buche: cardo, Aco: par, casal, pareja",
        "segmentacion": "buche + aco   [«con hache intercalada para deshacer el diptongo»]",
        "despeja": "aco",
        "razon": "`buche` 'melocacto, cardo globoso' ya es caquetío-atestiguado; "
                 "`aco` 'dos, par' lo da Esteves dos veces con la misma glosa "
                 "(Buchuhaco y Guachaco 'los dos zorros', p. 38): recurrencia 2.",
        "observacion": "⚠ `aco` 'dos' choca con `gudamuen` 'dos' del lexicón: "
                       "variación dialectal o atribución errada, sin resolver. "
                       "Ensenada pesquera 7 km al norte de Adícora («algunos "
                       "esnobistas le han cambiado el nombre por el horrendo "
                       "Saint Tropez. ¡Qué barbaridad!»). En el mapa vivo como "
                       "Buchuaco.",
    },
}

# ───────────────────────────────────────────────────────────────────────────
# MORFEMAS DESPEJADOS — el entregable central
# ───────────────────────────────────────────────────────────────────────────
# Cada uno con su glosa inferida y LA LISTA DE TOPÓNIMOS QUE LO SOSTIENEN.
# `contraejemplos` es tan importante como `apoyos`: un morfema que falla en la
# mitad de sus apariciones no es un morfema, es una coincidencia gráfica.

MORFEMAS_DESPEJADOS = {
    "-bacoa": {
        "glosa_inferida": "bosque, arboleda; formante toponímico de "
                          "'paraje cubierto de'",
        "estatus": "CORROBORADO (no es nuevo: `bacoa` ya está en el lexicón "
                   "como caquetío-atestiguado). Lo nuevo es su uso SUFIJAL "
                   "productivo, que REGLAS_ZAVALA no recoge.",
        "apoyos": ["adabacoa (Todo arboleda)", "guadabacoa (Arboleda)",
                   "quibacoas (Bosques pedregosos)",
                   "yacarebacoa (Pueblo del bosque)"],
        "contraejemplos": ["sazaribacoa (Río de los maizales) — la glosa no "
                           "menciona bosque; encaja mejor con la acepción "
                           "'sitio fértil' de la misma entrada"],
        "apoyo_externo": [
            "Alvarado 1921, vía van Buurt §10: `-baca` 'grupo, matorral, "
            "espesura' en topónimos venezolanos (Yatu Bacu, Dauguaraubaca)",
            "insular sin glosa: Barbacoa (Aruba), Maniguacoa (Curaçao)",
        ],
        "recurrencia": 5,
        "veredicto": "El morfema mejor sostenido de todo el ejercicio: 5 "
                     "topónimos glosados + apoyo independiente de Alvarado.",
    },
    "-are": {
        "glosa_inferida": "sitio de, paraje de (sufijo locativo)",
        "estatus": "NUEVO — despejado aquí por primera vez",
        "apoyos": ["bobare (Sitio de cultivo)", "cabudare (sitio de cultivo)",
                   "dabudare (Sitio de extracción de barro)",
                   "pachacuare (Sitio de palmeras)",
                   "taratarare (Hato, conuco — un hato es un lugar)"],
        "contraejemplos": ["guasare (Árbol cactáceo) — no denota lugar",
                           "chunare (Mazorca tierna) — no denota lugar"],
        "recurrencia": 5,
        "veredicto": "5 de 7 apariciones en posición final con glosa "
                     "descriptiva denotan un LUGAR, y las 4 más limpias dicen "
                     "literalmente 'Sitio de'. `dabudare` es el caso decisivo "
                     "porque su base `dabuda` 'barro loza' ya está atestiguada.",
        "conflicto": "⚠ van Buurt §5 recoge `-ure` (papiamentu -huri/-uri) "
                     "glosado 'raíz' por Cruz Esteves 1989, y lo declara "
                     "equivalente al `-ure` continental. La evidencia "
                     "toponímica dice 'sitio de'. Glosa en disputa — misma "
                     "situación que `-bana` (el tablero de decisiones D9).",
    },
    "ada-": {
        "glosa_inferida": "árbol",
        "estatus": "NUEVO en el caquetío — pero con cognado arahuaco fuerte",
        "apoyos": ["adabacoa (Todo arboleda)", "guadabacoa (Arboleda)"],
        "contraejemplos": [],
        "apoyo_externo": [
            "Lokono `ada` 'árbol' (cognado arahuaco directo)",
            "van Buurt §5 documenta `bara`/`bari` 'árbol' (cf. Lokono balli) "
            "como OTRA raíz de árbol en el mismo sistema — no compiten",
        ],
        "recurrencia": 2,
        "veredicto": "Recurrencia mínima (2) pero con las dos glosas idénticas "
                     "('arboleda') y cognado arahuaco de manual. B sólido.",
        "advertencia": "El despeje no es estrictamente forzoso: con `-bacoa` "
                       "= 'arboleda' por sí solo, `ada-` podría ser cualquier "
                       "otra cosa. Lo que lo sostiene es el cognado lokono, no "
                       "la ecuación.",
    },
    "bari-": {
        "glosa_inferida": "rojizo, turbio (del color del agua o de la tierra)",
        "estatus": "REAGRUPACIÓN de dos entradas ya existentes",
        "apoyos": ["barisi (Región de tierras coloradas cerca del mar)",
                   "bariquisimeto (Río de aguas turbias)"],
        "contraejemplos": ["el lexicón tiene además `bari` = 'vientre, "
                           "barriga', homógrafo sin relación"],
        "recurrencia": 2,
        "veredicto": "Propone unificar `barici` 'agua turbia' y `bariki` "
                     "'tierra colorada' bajo una raíz `bari-` + formantes. NO "
                     "propone tocar el lexicón: propone la pregunta.",
    },
    "yacare": {
        "glosa_inferida": "pueblo, poblado",
        "estatus": "NUEVO",
        "apoyos": ["yacare (Pueblo. Caimán)",
                   "yacarebacoa (Pueblo del bosque)"],
        "contraejemplos": [],
        "recurrencia": 2,
        "veredicto": "Cierra la ecuación de `yacarebacoa` sin residuo. Pero ver "
                     "la advertencia de contaminación tupí en NIVEL_B.",
    },
    "wa-": {
        "glosa_inferida": "prefijo de pluralidad / 'tener'",
        "estatus": "CORROBORADO (van Buurt §6, de Goeje 1928) — nuevo es el "
                   "apoyo toponímico continental",
        "apoyos": ["guadabacoa (Arboleda) frente a adabacoa (TODO arboleda)",
                   "guamabatriba (Muchas tierras de cultivo)"],
        "contraejemplos": ["muchos topónimos en gua-/wa- sin glosa; el prefijo "
                           "es demasiado frecuente para probar nada por sí solo"],
        "recurrencia": 2,
        "veredicto": "C alto / B bajo. La pareja adabacoa~guadabacoa es "
                     "elegante pero es UNA pareja.",
    },
}

# ───────────────────────────────────────────────────────────────────────────
# NIVEL C — plausible, sin recurrencia suficiente. Se registra, no se promueve.
# ───────────────────────────────────────────────────────────────────────────

NIVEL_C = {
    # ── Las lecturas del 25 de agosto, fusionadas el 2026-09-07 por orden de
    # Miguel («que no quede nada pendiente por ahí sin guardar o fusionar»).
    # Venían sueltas en toponimia_coro_espina.yaml, lengua_toponimia_quibacoa.yaml
    # y petroglifos_y_manaure.yaml. ──
    "curiana": {
        "id": "toponimo-111", "clase": "topónimo", "fuente": "arcaya-1920",
        "pagina": 169,
        "glosa_fuente": "«Coro o Curiana se denominaba el pueblo que allí tenían "
                        "fundado los indios, y Curiana la costa vecina» (Arcaya "
                        "p. 169); «Curiana: territorio donde estaban asentados los "
                        "caquetíos» (Zavala 2015, nota 4)",
        "segmentacion": "curi-/cori- + -ana   [-ana: forma atestiguada, sin glosa "
                        "desde #109]",
        "razon": "el nombre del proyecto no tenía entrada: vivía en el lexicón y "
                 "en D2 (#33). Forma atestiguada en tres grafías (Curiana, "
                 "Coriana, Coro), pero ninguna fuente impresa la glosa: las dos "
                 "glosas de fuente son referenciales. Cuatro lecturas del "
                 "significado compiten, ninguna cierra, y -ana perdió la glosa "
                 "'lugar de' el 2026-09-07. C: forma segura, significado abierto.",
        "observacion": "D2 (#33), territorio o asentamiento: Arcaya da las dos "
                       "cosas. Y hay un segundo Coriana: Oliver (cap. 3 p. 207) "
                       "lee «Coria-na» entre los nombres de aldea wanebucán de "
                       "Punta Espada-Chichibacoa (Guajira), «suspiciously "
                       "Caquetío».",
        "lecturas": [
            {"tipo": "etimologia-analitica",
             "lectura": "coro 'espina' → Coriana 'tierra de las espinas, o la "
                        "tierra del espinar, de vegetación espinosa, e "
                        "indirectamente, tierra de cardones' (con paragua 'mar' + "
                        "na 'tierra' = Paraguaná como paralelo); «Coriana, y no "
                        "Curiana, que nos parece un barbarismo»",
             "quien": "González Batista", "fecha": "2026-08-25", "eje": "significado",
             "procedencia": dict(obra="gonzalez-batista-nombre-de-coro"),
             "veredicto": "PLAUSIBLE (Miguel, 2026-08-25): la línea más "
                          "prometedora del autor, abierta. Depende de na = "
                          "'tierra', que ninguna fuente impresa da (Zavala #184: na "
                          "'como, semejante'). Su ejemplo corocoro como plural de "
                          "coro se refutó con Alvarado 1921 (onomatopeya del canto "
                          "del ave, voz caribe/tupí; el pez, por las manchas rojas): "
                          "cae el ejemplo, no la tesis, que se apoya en "
                          "tococoro/totocoro vivos en la arquitectura coriana, en "
                          "dato 'fruto del cardón' (Zavala) y en el cardonal de "
                          "Coro que figuraba entre los linderos de las propiedades. "
                          "Cautela general sobre el autor (Miguel)."},
            {"tipo": "etimologia-de-cronista",
             "lectura": "la serie Coro-/Curi- («la antigua Coriana, Coroquide, "
                        "Corobore, Coroquidiro, Ocorote, Corocoro, Cocorote») "
                        "remite a «Koori, avispa, en guajiro o Kuru, lagartija»; y "
                        "«Coro = viento» de Castellanos «esto es un error»",
             "quien": "Arcaya 1920", "fecha": "2026-08-25", "eje": "significado",
             "procedencia": dict(obra="arcaya-1920", pagina=170),
             "veredicto": "formante productivo sin glosa acordada: avispa o "
                          "lagartija (Arcaya), espina o cardón (González Batista; "
                          "D10 degradó coro 'cardón grande'), viento (Castellanos, "
                          "Miguel). Compiten; ninguna con glosa impresa del "
                          "caquetío."},
            {"tipo": "etimologia-de-cronista",
             "lectura": "«Coro viento quiere decir en lengua generosa»",
             "quien": "Castellanos 1589", "fecha": "2026-09-04", "eje": "significado",
             "procedencia": dict(obra="castellanos-elegias", pagina=185),
             "veredicto": "casi seguro el latín corus/caurus 'viento del "
                          "noroeste', que el castellano heredó como coro 'viento "
                          "noroeste': juego del poeta, no glosa caquetía; Arcaya lo "
                          "llama error. No es apoyo independiente de curi ~ juri."},
            {"tipo": "hipotesis",
             "lectura": "curi- (Curiana, Coriana) y juri 'viento' son la misma "
                        "palabra con dos pronunciaciones, una de Coro y otra de "
                        "Paraguaná: Curiana 'tierra del viento', paralelo de "
                        "Judibana 'cerro del viento' y Jurijurebo 'paso de los "
                        "vientos'",
             "quien": "Miguel Gil Urbina", "fecha": "2026-09-05", "eje": "significado",
             "apoyo": "cudan ~ judan en la fórmula de Mitare (c~j del lado de "
                      "Coro); juri ~ judi ya aceptada para Judibana; «aquella "
                      "tierra muy ventosa» (Castellanos)",
             "veredicto": "validación BAJA-MEDIA (Claude, 2026-09-05): una /k/ no "
                          "se cae como la h/j; el pariente wayuu del viento arranca "
                          "en h o w; Mitare no reparte limpio por región. Esteves no "
                          "trae variante con c/k (0 verificado, 2026-09-07): "
                          "neutro, porque solo cubre Paraguaná. La prueba pasa al "
                          "lado de Coro. Detalle: "
                          "6-fusion/toponimia_paraguana_miguel.yaml §Curiana / Coro"},
            {"tipo": "glosa-fuente",
             "lectura": "el mismo nombre nombra el pueblo y la costa: «Coro o "
                        "Curiana se denominaba el pueblo que allí tenían fundado "
                        "los indios, y Curiana la costa vecina»",
             "quien": "Arcaya 1920", "fecha": "2026-08-25", "eje": "referente",
             "procedencia": dict(obra="arcaya-1920", pagina=169),
             "veredicto": "es la pregunta de D2 (#33), con dos casos desde el "
                          "2026-08-25: en Coquibacoa la extensión sitio → región es "
                          "explícitamente española (Arcaya p. 130); en Curiana "
                          "Arcaya no separa quién extendió qué."},
            {"tipo": "hipotesis",
             "lectura": "hay un segundo Coriana: «Coria-na», nombre de aldea "
                        "wanebucán en Punta Espada-Chichibacoa (Guajira), junto a "
                        "«Paragua-nil»: morfemas «suspiciously Caquetío» que Oliver "
                        "explica por el nexo comercial con los caquetíos de allí",
             "quien": "Oliver 1989", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="oliver-1989-cap3", pagina=207),
             "veredicto": "si Coria-na se repite donde no hay nada que llamar Coro, "
                          "la raíz coria- es léxica (formación común, 'tierra o "
                          "lugar de X') o el nombre viajó con los comerciantes: en "
                          "los dos casos toca D2. Está también en la lista viva de "
                          "-ana (#109)."},
        ],
    },
    # Rehabilitado el 2026-09-07 (propuesta del 2026-08-25,
    # lengua_toponimia_quibacoa.yaml §3). Conserva su id: sigue listado en
    # DESCARTES «glosa meramente referencial» como `reubicado` para que el
    # contador no se mueva.
    "quiquiba": {
        "id": "toponimo-034", "clase": "topónimo", "fuente": "arcaya-1920",
        "pagina": 130,
        "glosa_fuente": "«tomaron por las costas de la Goagira, región que "
                        "llamaron de Coquibacoa, o de Quiquibacoa, por el nombre "
                        "indígena de uno de sus sitios. Este nombre se le dio "
                        "también entonces al Golfo, y aun se extendió a todas las "
                        "tierras que lo rodean, inclusive las de Paraguaná»",
        "segmentacion": "qui~quiba (reduplicado) + bacoa",
        "morfemas": {
            "quiba": "piedra  [Zavala #218 quiva, #92 cuiva/kiba: atestiguado]",
            "bacoa": "lugar, paraje  [atestiguado; morfema-001]",
        },
        "glosa_reconstruida": "lugar de las piedras, el pedregal",
        "razon": "estaba descartado por glosa referencial (Zavala solo nombra). "
                 "Arcaya p. 130 da el referente (un sitio de la Guajira, luego el "
                 "Golfo) y la forma con -bacoa; con quiba 'piedra' y bacoa 'lugar' "
                 "hay ecuación, y quibacoas 'Bosques pedregosos' (Zavala #204) es "
                 "la misma composición sin reduplicar. C y no B porque la "
                 "reduplicación es patrón con casos (jurijurebo sí, quibaquibi "
                 "no), Quiba #203 'ayuda' choca con Quiva #218 'piedra', y la "
                 "glosa es reconstruida, no impresa.",
        "observacion": "Regla 3: la extensión al Golfo y sus tierras es española; "
                       "lo indígena es el sitio. La grafía más antigua es la "
                       "reduplicada: «Quinquevacoa» en la capitulación de Ojeda "
                       "(28-VII-1500, Otte 1963: 3, vía Oliver cap. 3 p. 211); de "
                       "la Cosa 1500 escribe Coquibacoa sobre toda la Guajira "
                       "(p. 192). Y el cabo Chichibacoa «suspiciously sounds like "
                       "Coquibacoa, except for a /k/::/ch/ sound shift» (p. 249 "
                       "n. 94): el sitio puede seguir vivo con otro sonido.",
        "lecturas": [
            {"tipo": "etimologia-analitica",
             "lectura": "qui~quiba (reduplicación con valor plural, como juri → "
                        "jurijurebo) + bacoa 'lugar de' = 'lugar de las piedras, "
                        "el pedregal'",
             "quien": "proyecto", "fecha": "2026-08-25", "eje": "significado",
             "apoyo": "quiva/cuiva/kiba 'piedra' (Zavala #218, #92); -bacoa en "
                      "cinco topónimos glosados; Arcaya p. 36: iparcoa 'cascajo' "
                      "= ipar 'piedra' + -coa en guajiro, el formante con la misma "
                      "raíz en lengua hermana",
             "veredicto": "rehabilitado a nivel C el 2026-09-07 (Miguel: lo del "
                          "25 de agosto se guarda o se fusiona); subir a B pide un "
                          "segundo caso de reduplicación plural o una glosa "
                          "impresa."},
            {"tipo": "hipotesis",
             "lectura": "el cabo Chichibacoa, en el norte de la Guajira, es "
                        "Coquibacoa con /k/ > /ch/: el sitio indígena de Arcaya "
                        "seguiría vivo en el mapa",
             "quien": "Oliver 1989", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="oliver-1989-cap3", pagina=249),
             "apoyo": "un nombre que sigue vivo es dato (Miguel); Punta "
                      "Chichibacoa existe en el mapa de hoy"},
        ],
    },
    "la cuiba": {
        "id": "toponimo-112", "clase": "topónimo", "fuente": "moron-2012-petroglifos",
        "glosa_fuente": "sitio de la leyenda del Rey Manaure (Aguas Termales de "
                        "Agua Clara), que destaca por «la riqueza de cristales de "
                        "cuarzo a ras del suelo»",
        "segmentacion": "cuiba (< cuiva/quiva/kiba 'piedra'), con artículo castellano",
        "morfemas": {
            "cuiba": "piedra  [Zavala #92 «Cuiva. Kiba (PMA): Piedra», #218 «Quiva "
                     "(E): Piedra»: atestiguado]",
        },
        "glosa_reconstruida": "la piedra, el pedregal",
        "razon": "Morón no glosa el nombre; la ecuación la da el sitio: un lugar de "
                 "cristales de cuarzo a ras del suelo llamado con la palabra "
                 "caquetía para 'piedra'. Es el principio toponímico (el nombre "
                 "describe el rasgo del sitio) en un caso verificable en terreno. "
                 "C: un morfema atestiguado y el referente a favor; sin glosa "
                 "impresa y sin página del topónimo en la fuente.",
        "observacion": "Homógrafo del etnónimo cuiba (3-mundo/etnias.yaml, "
                       "etnia-001: guahibos de los Llanos). La hipótesis de que el "
                       "etnónimo sea un exónimo caquetío 'gente de la piedra' sigue "
                       "sin verificar; este sitio la hace más llamativa, no la "
                       "prueba. Nombre vivo en Falcón: localizar en el barrido OSM.",
        "lecturas": [
            {"tipo": "hipotesis",
             "lectura": "si cuiva/quiva = 'piedra', La Cuiba nombra exactamente el "
                        "rasgo dominante del sitio: cristales de cuarzo a ras del "
                        "suelo",
             "quien": "proyecto", "fecha": "2026-08-25", "eje": "ambos",
             "procedencia": dict(obra="moron-2012-petroglifos"),
             "apoyo": "principio toponímico, enunciado por separado por González "
                      "Batista y por la Relación de 1578 sobre la provincia de "
                      "lengua Caraca; conjunto de cognados 'piedra' ipa (wayuu) / "
                      "siba (lokono) / quiva-cuiva-kiba (caquetío), Arcaya 1920 "
                      "p. 36",
             "veredicto": "fusionado como nivel C el 2026-09-07 (Miguel: lo del 25 "
                          "de agosto se guarda o se fusiona)."},
            {"tipo": "tradicion-local",
             "lectura": "la leyenda del Rey Manaure en La Cuiba / Aguas Termales de "
                        "Agua Clara: la viejita caquetía, el machete, la culebra "
                        "amarilla y las barritas de oro",
             "quien": "tradición oral recogida por Morón 2012", "fecha": "2026-08-25",
             "eje": "referente",
             "procedencia": dict(obra="moron-2012-petroglifos")},
        ],
    },
    "alaurima": {
        "glosa_fuente": "Río blanco o claro", "segmentacion": "alaur- + -ima",
        "razon": "`-ima` 'humedad, quebrada' (AFIJOS_ZAVALA #165, confirmado "
                 "independientemente por van Buurt §10 vía Onima) alinea con "
                 "'río'. `alaur-` = 'blanco/claro' no recurre en ningún otro "
                 "topónimo del corpus: conjetura.",
    },
    "capadare": {
        "glosa_fuente": "Diente de tigre", "segmentacion": "capa- + dare",
        "razon": "`dare` = 'diente' está en el lexicón y alinea. `capa-` = "
                 "'tigre/jaguar' cerraría la ecuación, pero no recurre. Además "
                 "el lexicón no tiene ninguna palabra para felino, así que no "
                 "hay con qué contrastarlo.",
    },
    "sazaribacoa": {
        "glosa_fuente": "Río de los maizales", "segmentacion": "sazari- + bacoa",
        "razon": "`sazari-` = 'maíz' sería el despeje natural, pero no recurre "
                 "y el lexicón no tiene la palabra (solo derivados: `buriche` "
                 "chicha de maíz, `amaca` sitio de moler maíz). Además la "
                 "glosa no menciona bosque, lo que tensiona el valor de "
                 "`-bacoa`.",
    },
    "paraguaná": {
        "glosa_fuente": "Rodeada del mar", "segmentacion": "para(gua) + -na",
        "razon": "corrobora `para`/`paragua` = 'mar' del lexicón. Pero 'rodeada' "
                 "no queda explicada y `-na` es demasiado frecuente (34 formas "
                 "del corpus) para significar nada demostrable.",
        "observacion": "Grafía: Zavala #192 y Esteves p. 56 imprimen Paraguaná "
                       "con tilde; el canon la guardó sin ella hasta la auditoría "
                       "de tildes del 2026-09-07 (#109 §3: la -aná tónica es el "
                       "dato que distinguiría este sufijo del -ana de Curiana). "
                       "Censo de -ana en Esteves, mismo día: "
                       "6-fusion/censo_ana_esteves_109.yaml.",
        "lecturas": [
            {"tipo": "etimologia-analitica",
             "lectura": "para 'agua en grandes cantidades' (Zavala #190) + gua "
                        "'terreno cercado' (#122) + na 'como, semejante' (#184) ≈ "
                        "'a manera de tierra cercada por el mar': explica el "
                        "'rodeada' que para(gua) + -na dejaba sin origen",
             "quien": "proyecto", "fecha": "2026-08-25", "eje": "significado",
             "apoyo": "tres morfemas ya atestiguados; la tilde de Paraguaná (-aná "
                      "tónica) sería el dato que decide",
             "veredicto": "pendiente: #109 (abierto)"},
            {"tipo": "etimologia-analitica",
             "lectura": "paragua 'mar, agua grande' + na 'tierra' = 'la tierra "
                        "rodeada de mar'",
             "quien": "González Batista", "fecha": "2026-08-25", "eje": "significado",
             "procedencia": dict(obra="gonzalez-batista-nombre-de-coro"),
             "veredicto": "depende de na = 'tierra', que ninguna fuente impresa da; "
                          "choca con na = 'como' (Zavala #184, atestiguado). Es la "
                          "pieza que decide #109"},
            {"tipo": "glosa-fuente",
             "lectura": "«Conuco en medio del mar es la más repetida de las "
                        "significaciones que le dan al topónimo»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=56),
             "veredicto": "Esteves no la firma: la reporta como la significación "
                          "«que le dan». Es la tradición local impresa en 1989, "
                          "veintiséis años antes de que el proyecto la conociera "
                          "como etimología popular «tipo Wikipedia»"},
            {"tipo": "etimologia-de-cronista",
             "lectura": "«Está suficientemente averiguado que Para significa agua»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=56),
             "apoyo": "converge con Zavala #190 para 'agua dulce o salada en "
                      "grandes cantidades' y #191 paragua 'mar'"},
            {"tipo": "hipotesis",
             "lectura": "'conuco en medio del mar' es, morfema a morfema, para "
                        "'agua' + gua 'conuco, heredad, terreno cercado' (Zavala "
                        "#122, HP): la tradición que Esteves recoge coincide con la "
                        "segmentación para-gua-ná de la primera lectura, y por una "
                        "vía independiente de Zavala. Sigue sin morfema el 'en "
                        "medio de' / 'rodeada'. Y el censo de -ana en Esteves "
                        "(2026-09-07) no da ningún -ana 'lugar de': el 'lugar' de "
                        "Esteves es bacoa",
             "quien": "proyecto", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=56),
             "veredicto": "pendiente: #109 (la decisión sobre la glosa de -ana es "
                          "de Miguel; censo en 6-fusion/censo_ana_esteves_109.yaml)"},
        ],
    },
    "guamabatriba": {
        "glosa_fuente": "Muchas tierras de cultivo",
        "segmentacion": "wa- + mabatriba",
        "razon": "`wa-` plural alinea con 'muchas'; el resto es un bloque de "
                 "nueve caracteres sin recurrencia ni paralelo. Se registra por "
                 "el prefijo, no por el resto.",
    },
    "turijerebo": {
        "glosa_fuente": "Lugar de descanso", "segmentacion": "turije- + ebo",
        "razon": "tercera aparición de `-ebo`, pero con glosa 'lugar' y no "
                 "'camino'. Compatible por extensión ('paso' → 'lugar de "
                 "paso'), no demostrable.",
    },
    "guacurebo": {
        "glosa_fuente": "Quebrada que crece", "segmentacion": "guacu- + -rebo",
        "razon": "**contraejemplo útil**: si `-ebo` fuera 'camino', esta glosa "
                 "no encaja. Registrado para que la corroboración de `ebo` no "
                 "se cuente más limpia de lo que es: 2 aciertos, 2 dudosos.",
        "observacion": "(2026-09-07) Esteves lo analiza como guacoa + ebo 'el "
                       "paso de la guacoa' (p. 38): con eso el contraejemplo de "
                       "`ebo` deja de serlo (ya anotado en esteves-1989.md). "
                       "«En el censo de 1881 toda Guacurebo pertenecía a Moruy y "
                       "tenía 34 casas»; la variante de Moruy es Guasurebo. En el "
                       "mapa vivo aparece como GUACUBERO (fotos de Miguel): "
                       "metátesis r/b, el nombre sigue en uso.",
        "lecturas": [
            {"tipo": "glosa-fuente",
             "lectura": "«proviene de Guacoa, pero más explícito por el sufijo "
                        "ebo, o sea que expresa: el paso de la guacoa»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=38),
             "veredicto": "compatible con ebo 'paso' (Zavala #117); la glosa de "
                          "Zavala 'quebrada que crece' queda como la divergente"},
            {"tipo": "testimonio-residente",
             "lectura": "vivo en el mapa actual como Guacubero, sector del Capubana",
             "quien": "Miguel Gil Urbina (fotos del mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
    "taratarare": {
        "glosa_fuente": "Hato, conuco",
        "segmentacion": "tara~tara (reduplicación) + -are",
        "razon": "reduplicación exacta clara + el sufijo locativo `-are`. La "
                 "base `tara` no se puede fijar: el lexicón dice 'venado' y "
                 "Zavala #238 dice 'langosta, mariposa' — conflicto ya "
                 "registrado en INDICE_FUENTES.",
        "eco_insular": "van Buurt §8: Taratata / Tatarata (Aruba) y, en Falcón, "
                       "Taratara, Taratare y Tatatarare (Cruz Esteves 1989). "
                       "**Cinco variantes reduplicadas del mismo tema.**",
    },
    "poapao": {
        "glosa_fuente": "Serranía de Coro", "segmentacion": "poa~pao",
        "razon": "reduplicación parcial evidente; la glosa es un identificador "
                 "geográfico, no una traducción, así que no hay qué despejar.",
    },
    "jadicuar": {
        "glosa_fuente": "Sitio donde abunda jajato. Salicornia fructuosa",
        "segmentacion": "jadi- + -cuar",
        "razon": "`jajato` está en el lexicón ('chloris radiata, yerba "
                 "forrajera, lugar de arena') y `jadi-`~`jaja-` podría ser la "
                 "misma raíz, pero la correspondencia d~j no está documentada "
                 "en ninguna de las tres ortografías.",
        "observacion": "⭐ (2026-09-07) Jadícuar es el nombre primitivo de ADÍCORA "
                       "(Esteves p. 14: «de Jadícuar a Jadícora, de Jadícora a "
                       "Jatícora, hasta llegar al sugestivo y poético Adícora de "
                       "hoy»): el topónimo de Zavala y la capital de municipio de "
                       "la costa oriental son el mismo nombre. Esteves confirma la "
                       "glosa 'jajatal' por vía independiente y, en el apéndice, "
                       "segmenta jade 'jajato' + cuar, «desinencia de los "
                       "sustantivos colectivos en lengua cumanagota» (Caulín): "
                       "topónimo híbrido según él — atribución cumanagota en "
                       "cuarentena (B.6). Nodo-012 adicora. Puerto de goletas a "
                       "las islas hasta los años 50 (Medina Colina, s. XX).",
        "lecturas": [
            {"tipo": "glosa-fuente",
             "lectura": "«El nombre primitivo era Jadícuar, que quiere decir: "
                        "jajatal, sitio donde abunda el jajato, hierba halófila de "
                        "terrenos salobres»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "ambos",
             "procedencia": dict(obra="esteves-1989", pagina=14),
             "veredicto": "coincide con Zavala; segunda atestación de la glosa"},
            {"tipo": "etimologia-analitica",
             "lectura": "jade 'jajato' + cuar, colectivo cumanagoto "
                        "'aglomeración, abundancia' según Caulín — «este cuar "
                        "tiene el mismo significado del tuba de los caquetíos»",
             "quien": "Esteves 1989 (apéndice)", "fecha": "2026-09-07",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=73),
             "veredicto": "la parte caquetía (jajato, tuba) está atestiguada; la "
                          "atribución del sufijo al cumanagoto es de Esteves vía "
                          "Caulín, sin geografía que la sostenga (Oliver §3.2.4 "
                          "pone a los cumanagotos en la costa oriental)"},
        ],
    },
    "chunare": {
        "glosa_fuente": "Apellido. Mazorca tierna",
        "clase": "antropónimo",
        "segmentacion": "chu- + -nare",
        "razon": "**el único antropónimo del corpus con glosa descriptiva.** No "
                 "resuelve: ni `chu-` ni `-nare` recurren con esa semántica, y "
                 "'mazorca' no es un lugar, así que el `-are` locativo no "
                 "aplica.",
    },
    "Casibari": {
        "clase": "topónimo (Aruba)", "fuente": "van-buurt-2014 §8",
        "glosa_fuente": "'there are hard rocks'",
        "segmentacion": "ca- + siba + rí",
        "razon": "**prueba de humo del método, no hallazgo**: van Buurt ya "
                 "publicó esta etimología y de ella salieron los morfemas del "
                 "inventario. Que el segmentador la reproduzca valida el "
                 "procedimiento; no aporta información nueva.",
    },
    "Hudishibana": {
        "clase": "topónimo (Aruba)", "fuente": "van-buurt-2014 §8",
        "glosa_fuente": "'windy plain'", "segmentacion": "hudi + -shi- + bana",
        "razon": "ídem. Interés adicional: `hudi` 'viento' es la misma raíz que "
                 "el `juri` continental de `jurijurebo`. **La palabra para "
                 "'viento' aparece en un topónimo del Golfete y en otro de "
                 "Aruba, en dos ortografías distintas.**",
    },
    # ── La campaña de Esteves 1989, lote 1 (2026-09-06) — ver NIVEL_B ──
    "adaure": {
        "id": "toponimo-080", "fuente": "esteves-1989", "pagina": 13,
        "glosa_fuente": "apellido indígena; «no descartamos que provenga de Dara, "
                        "en tal caso en forma patronímica: quizás la Dara fuera "
                        "el ave totémica de la tribu»",
        "segmentacion": "a- + dar(a) + -ure   [prótesis y epéntesis, según Esteves]",
        "razon": "`dara` 'alcaraván' es caquetío-atestiguado y el autor lo "
                 "propone con reservas; `-ure` recurre (Abudure, Babahuro) pero "
                 "aquí no hay glosa que cierre. Serie de apellidos en -aure que "
                 "Esteves lista y no analiza: Adaure, Timaure, Yaraure, "
                 "Chunaure, Manaure (p. 13). Un nombre propio atestigua sus "
                 "morfemas aunque nombre a un linaje.",
        "observacion": "Aldea al oeste de Buenavista; censo 1881: 87 casas, 522 "
                       "vecinos, «más importante que muchas poblaciones cabeceras "
                       "de municipio». Hill Peña: «tribu belicosa»; Martí 1773 la "
                       "nombra. En el mapa vivo.",
    },
    "amaraya": {
        "id": "toponimo-081", "fuente": "esteves-1989", "pagina": 14,
        "glosa_fuente": "puede ser una alteración de «maracaya», otro nombre "
                        "indígena que recibe el «güirito», gato silvestre",
        "segmentacion": "a- + maraya (< maracaya, con síncopa)",
        "razon": "zoónimo con prótesis vocálica, patrón que Esteves documenta en "
                 "Adaro < dara. Conjetura declarada («puede ser»); maracaya no "
                 "está en el lexicón. Aldea al sur de Jadacaquiva; censo 1881, "
                 "como Amaralla: 16 casas, 108 vecinos.",
    },
    "baraived": {
        "id": "toponimo-087", "fuente": "esteves-1989", "pagina": 21,
        "glosa_fuente": "Bara: árbol; en Baraivere, la forma primitiva, «la "
                        "desinencia bere actuaría como adjetivo o como sustantivo "
                        "para formar una voz compuesta»",
        "segmentacion": "bara + i + bere   [formas antiguas Baraivede, Baraivere]",
        "razon": "`bara` 'palo, árbol' es caquetío-atestiguado (#101: 'árbol', no "
                 "'río') y Esteves lo pone; el resto queda sin glosa — el autor "
                 "lo deja abierto y solo aporta el paralelo guaraní Uretebere "
                 "'raíz amarga' (bere 'amargo'), que no es caquetío. Rechaza la "
                 "etimología popular «vara y ved».",
        "observacion": "Capital de municipio; censo 1881: 256 casas, 1.724 vecinos "
                       "con Maquigua, Miraca, Camunare y Charaima. Esteves: «en "
                       "los topónimos indígenas de Paraguaná casi no hay voces "
                       "agudas» — dato para la auditoría de tildes (#109).",
        "lecturas": [
            {"tipo": "etimologia-popular",
             "lectura": "unos marinos perdidos vararon en los bancos de arena y "
                        "uno dijo «vara y ved»; de ahí el nombre",
             "quien": "tradición local, recogida por Esteves", "fecha": "2026-09-06",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=21),
             "veredicto": "descartada por el propio autor («estamos en total "
                          "desacuerdo con tan expeditivo procedimiento»); se "
                          "registra para no re-investigarla"},
        ],
    },
    "caseto": {
        "id": "toponimo-088", "fuente": "esteves-1989", "pagina": 30,
        "glosa_fuente": "planta herbácea de las malvas espigadas, el Malvastrum "
                        "spicatum de los botánicos",
        "segmentacion": "caseto (fitónimo, sin composición)",
        "razon": "el topónimo ES el nombre de una planta que el lexicón no tiene: "
                 "no hay ecuación que despejar sino una palabra nueva propuesta "
                 "por Esteves. Aldea del municipio Santa Ana; censo 1881: 45 "
                 "casas, 303 vecinos.",
        "lecturas": [
            {"tipo": "etimologia-popular",
             "lectura": "Gaseto < gaceta, porque en el lugar vivía quien redactaba "
                        "una hoja periódica",
             "quien": "versión local, recogida por Esteves", "fecha": "2026-09-06",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=30),
             "veredicto": "el autor la llama «un tanto fantasiosa por lo que tiene "
                          "de chauvinismo»"},
        ],
    },
    "cocodite": {
        "id": "toponimo-079", "fuente": "esteves-1989", "pagina": 31,
        "glosa_fuente": "el sufijo «dito» es distintivo de los sustantivos "
                        "colectivos en lengua indígena",
        "segmentacion": "coco + -dito   [Cocodito en papeles escriturados de 1590]",
        "razon": "`-dito` 'colectivo abundancial' lo atestigua Esteves cuatro "
                 "veces y lo atribuye al caquetío (Guanadito, p. 41); la base "
                 "coco- no la glosa nadie. Cierra la mitad de la ecuación.",
        "observacion": "Colinas al oeste de Pueblo Nuevo; San José de Cocodite, "
                       "censo 1881: 34 casas, 243 vecinos, «desapareció "
                       "totalmente cuando la hambruna de 1912». El papel de 1590 "
                       "(tierras compuestas a favor de Alonso Arias Vaca) es el "
                       "documento más antiguo que cita el libro.",
    },
    "jadacaquiva": {
        "id": "toponimo-083", "fuente": "esteves-1989", "pagina": 45,
        "glosa_fuente": "Quiba en caquetío es pedruzco",
        "segmentacion": "jada(ca) + quiva",
        "razon": "`quiva`/`kiba` 'piedra' es caquetío-atestiguado y Esteves lo "
                 "pone en su serie (Jadacaquiva, Quibarute, Tiquiba, Todariquiba, "
                 "Yauquiba, Quibucara); la base jada(ca)- no la glosa: solo "
                 "recoge dos etimologías populares y las relativiza («ambas "
                 "versiones hay que recibirlas con las reservas del caso, por la "
                 "razón de que Jadacaquiva antiguamente tuvo otros nombres»). "
                 "Cierra la mitad de la ecuación.",
        "observacion": "Capital de municipio; 1881: 243 casas, 1.840 vecinos; "
                       "iglesia de 1740, «de los más antiguos de Paraguaná». Con "
                       "Yabuquiva (mapa de Miguel, no en Esteves) la familia "
                       "-quiva/-quiba de Paraguaná crece.",
        "lecturas": [
            {"tipo": "etimologia-popular",
             "lectura": "los nativos, con miedo a los caballos, se armaban de "
                        "piedras y gritaban «¡Jaca... quiba!»: ¡piedra contra esas "
                        "jacas!",
             "quien": "versión local, recogida por Esteves", "fecha": "2026-09-06",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=45),
             "veredicto": "el autor la llama «pintoresca» y «hilarante»; mezcla "
                          "caquetío y andaluz"},
            {"tipo": "etimologia-popular",
             "lectura": "en una sequía machacaban macoyas de jajato contra "
                        "piedras para chupar el jugo y gritaban «¡Jajato... "
                        "quiba!»",
             "quien": "versión local, recogida por Esteves", "fecha": "2026-09-06",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=46),
             "veredicto": "«menos hilarante»; el autor la recibe con reservas"},
            {"tipo": "hipotesis",
             "lectura": "jada- sería el mismo jadi-/jaja- de Jadícuar 'jajatal' "
                        "(jajato, lexicón) + quiva 'piedra': 'las piedras del "
                        "jajatal' — la segunda versión popular contendría el dato "
                        "real (jajato) envuelto en anécdota",
             "quien": "proyecto", "fecha": "2026-09-06", "eje": "significado",
             "veredicto": "sin apoyo independiente; la correspondencia d~j de "
                          "jadicuar (toponimo-024) tampoco está documentada"},
        ],
    },
    "machuruca": {
        "id": "toponimo-084", "fuente": "esteves-1989", "pagina": 49,
        "glosa_fuente": "viene de caruca, paja áspera con la cual se le da "
                        "consistencia al barro batido para la torta que se aplica "
                        "a paredes y techos de las casas humildes",
        "segmentacion": "ma- + c(h)aruca",
        "razon": "fitónimo con prefijo: Esteves deriva el nombre de caruca, que "
                 "el lexicón no tiene; el ma- inicial queda sin explicar (¿el "
                 "mismo ma- de Manaure, Maicara, Maitiruma?). Sin recurrencia "
                 "de caruca.",
        "observacion": "Aldea del municipio Santa Ana, sin censo en 1881 «incluida "
                       "en los Ejidos del Pueblo». Sitio FAL-152 de Oliver "
                       "(nodo-026, Urumaco y Dabajuroide) y, según Esteves, "
                       "cementerio indígena y petroglifo en Misaray. En el mapa "
                       "vivo, sector del Capubana.",
    },
    "maicara": {
        "id": "toponimo-085", "fuente": "esteves-1989", "pagina": 49,
        "glosa_fuente": "«en un documento de Composición de Tierras hemos leído: "
                        "Maicuare, éste sería tal vez el nombre primitivo»",
        "segmentacion": "mai- + cu- + -are   [sobre la forma primitiva Maicuare]",
        "razon": "Esteves no glosa; solo la forma antigua. Sobre ella alinea "
                 "`-are` 'sitio de' (morfema-002, cuatro topónimos en Zavala); "
                 "mai- no tiene glosa caquetía (Esteves usa mái 'manantial' solo "
                 "como caribe insular, en Maitiruma). Conjetura nuestra sobre la "
                 "mitad del nombre.",
        "observacion": "Aldea de Buenavista; 1881: 21 casas, 146 vecinos. En el "
                       "mapa vivo.",
    },
    "maitiruma": {
        "id": "toponimo-078", "fuente": "esteves-1989", "pagina": 49,
        "clase": "topónimo (estrato caribe insular, según Esteves)",
        "glosa_fuente": "en el caribe insular, mái significa: manantial, ojo de "
                        "agua; iruma: azul celeste, o sea que Maitiruma expresa: "
                        "manantial azul",
        "segmentacion": "mai + iruma   [según Esteves; no caquetío]",
        "razon": "la ecuación cierra, pero con morfemas de otra lengua: ni mai ni "
                 "iruma están en el lexicón caquetío (e'iruma wayuu 'primogénito' "
                 "es falso amigo). Uno de los cinco topónimos de Paraguaná que "
                 "Esteves da como no caquetíos (Amuay, Elegüey, Maragüey, "
                 "Jamaica, Maitiruma): evidencia de convivencia de lenguas en la "
                 "península (cola B.6, Oliver §3.2.4).",
        "observacion": "Aldea del municipio Santa Ana; 1881: 52 casas, 342 "
                       "vecinos. Geolocalizado: la escuela Maitiruma está al pie "
                       "este del cerro de Santa Ana, en el mismo complejo de agua "
                       "que Chamuriana (toponimia_paraguana_miguel.yaml "
                       "§capubana-centro-sagrado). ⚠ El estrato es INFERENCIA "
                       "léxica de Esteves, sin documento, y su etiqueta nombra "
                       "una lengua arahuaca (el caribe insular de Breton): B.6, "
                       "minada el 2026-09-07, no da ningún grupo de lengua "
                       "caribe en Paraguaná (6-fusion/oliver_324_caribes.yaml "
                       "§5).",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "el 'manantial azul' cae al pie este del Capubana, donde "
                        "sigue habiendo agua y uno de los pocos bosques xerófitos "
                        "que quedan: converge con Chamuriana ('agua que baja del "
                        "cerro') en un radio de pocos kilómetros",
             "quien": "Miguel Gil Urbina (mapa y terreno)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
    # ── Lote 2 (2026-09-07): los del «caribe insular», cerrados con B.6 ──
    "amuay": {
        "id": "toponimo-090", "fuente": "esteves-1989", "pagina": 14,
        "glosa_fuente": "«la voz da la idea de cavidad subterránea, haitón, cueva "
                        "grande. Y justamente en las cercanías de Amuay hay unas "
                        "cuevas naturales que debieron ser habituales residencias "
                        "de los nativos»",
        "segmentacion": "amu- + -ay   [sin morfema caquetío que alinee]",
        "razon": "la glosa es una idea del autor («da la idea de»), sin fuente; "
                 "ningún morfema del canon alinea. Lo que sí está atestiguado "
                 "por otra vía es que el nombre es el ETNÓNIMO de uno de los dos "
                 "clanes caquetíos de la península, los Amuayes, con territorio "
                 "al sur y reasentamiento Cayerda → Moruy (Delmonte 1883 vía "
                 "Oliver cap. 3 pp. 275-276; paraguana_dos_clanes.yaml). El "
                 "topónimo hereda el nombre del grupo, como la bahía de "
                 "Guaranao el del otro clan. Se registra en C por el etnónimo, "
                 "no por la glosa.",
        "observacion": "⚠ Esteves lo atribuye al «caribe insular» «por su "
                       "fonética, como batey, mamey, caney, carey» (p. 16): "
                       "cuatro taínismos del español general; y el caribe insular "
                       "de Breton es lengua arahuaca. B.6 (Oliver §3.2.4, minada "
                       "2026-09-07) no da ningún grupo caribe en Paraguaná. "
                       "Conflicto amuay-caquetio-vs-caribe RESUELTO por Miguel el "
                       "2026-09-07 a favor de la etnohistoria. Bahía y población de Los "
                       "Taques; 1881: 8 casas, 60 vecinos; «hoy» ~400 casas y "
                       "3.000 habitantes; también la etimología «muelle» (1924), "
                       "que Esteves descarta.",
        "lecturas": [
            {"tipo": "hipotesis",
             "lectura": "el topónimo es el etnónimo del clan Amuay, sub-grupo "
                        "caquetío que controlaba el sur de la península con "
                        "playas de pesca excluyentes frente a los Guaranaos",
             "quien": "proyecto", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="oliver-1989-cap3", pagina="275-276"),
             "apoyo": "González Batista y Delmonte 1883 vía Oliver; el mismo patrón "
                      "etnónimo → topónimo que Guaranao → bahía de Guaranao"},
            {"tipo": "etimologia-analitica",
             "lectura": "'cavidad subterránea, cueva grande', por las cuevas "
                        "naturales cercanas; voz del caribe insular «por su "
                        "fonética»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=16),
             "veredicto": "inferencia fonética sin documento; la etiqueta de "
                          "estrato está mal puesta (6-fusion/oliver_324_caribes.yaml "
                          "§5). Se conserva como voz del cronista local"},
            {"tipo": "etimologia-popular",
             "lectura": "de «muelle», por el endeble muelle de 1924 cuando el "
                        "puerto fue aduana marítima",
             "quien": "«algunos, inocentemente», según Esteves", "fecha": "2026-09-07",
             "eje": "significado", "procedencia": dict(obra="esteves-1989", pagina=16),
             "veredicto": "anacrónica: el nombre es anterior (censo 1881)"},
        ],
    },
    # ── Lote 3 (2026-09-07): las ciudades de Castellanos con entrada en Esteves ──
    "todariquiba": {
        "id": "toponimo-094", "fuente": "esteves-1989", "pagina": 64,
        "glosa_fuente": "«Tubariquiba y no Todariquiba, quiere decir: pedregal. "
                        "Tuba: aglomeración. Quiba: pedruzco»",
        "segmentacion": "toda/tuba + ri + quiba",
        "razon": "los dos morfemas de Esteves están atestiguados en el lexicón "
                 "(tuba 'aglomeración, montón'; kiba 'piedra'), pero su ecuación "
                 "exige ENMENDAR la forma: los primarios dicen Todariquiba "
                 "(Bastidas 1538) y Todariquibo (Castellanos 1589), no "
                 "Tubariquiba. Zavala #250 tiene toda- como «desinencia» sin "
                 "valor: la forma atestiguada segmenta sin enmienda, pero sin "
                 "glosa para toda-. Cierra a medias.",
        "observacion": "«Legendaria ciudad caquetía que se supone fuera asiento "
                       "del gobierno del Cacique Manaure» (Esteves); la carta de "
                       "Bastidas (AGI 1538) la pone a dos leguas de Coro con el "
                       "cacique Don Alexandro; Castellanos la encabeza entre las "
                       "«ciudades de grandísimo momento». Ubicación sin fijar: "
                       "Esteves recoge Tacuato y los Médanos de Coro, y objeta "
                       "que allí hay arena, no piedra. Es nodo-001 del registro "
                       "de asentamientos (la Curiana de la simulación).",
        "lecturas": [
            {"tipo": "hipotesis",
             "lectura": "toda- (Zavala #250, desinencia sin valor) + ri + quiba "
                        "'piedra': la forma atestiguada de 1538 y 1589 se "
                        "segmenta sin enmendar; falta la glosa de toda-",
             "quien": "proyecto", "fecha": "2026-09-07", "eje": "significado",
             "veredicto": "pendiente de que toda- reciba glosa en otra fuente"},
        ],
    },
    "miraca": {
        "id": "toponimo-095", "fuente": "esteves-1989", "pagina": 52,
        "clase": "topónimo (glosa guaraúna, según Esteves)",
        "glosa_fuente": "«De la voz hemos averiguado que en lengua guaraúna, "
                        "Miraca es atarraya. Miraca sanuco: atarraya pequeña»",
        "segmentacion": "miraca (sin composición; voz warao según Esteves)",
        "razon": "la glosa viene de otra lengua (warao) y de un «hemos "
                 "averiguado» sin cita: ningún morfema caquetío alinea. Lo firme "
                 "es la cadena de atestación, la más larga del canon: Myraca con "
                 "el cacique Bonyata en la carta de Bastidas (1538), pueblo de "
                 "Paraguaná en 1556 según Arcaya (vía Esteves), «ciudad de "
                 "grandísimo momento» en Castellanos (1589), 79 casas en el censo "
                 "de 1881, y población viva hoy — «de los cuales sólo existe hoy "
                 "el pueblo de Miraca», dice Esteves de las tres ciudades.",
        "observacion": "⭐ Cinco siglos con el mismo nombre en el mismo sitio "
                       "(Baraived). Un topónimo que sigue en uso es dato aunque "
                       "no tenga etimología: aquí la continuidad del asentamiento "
                       "está mejor sostenida que la de cualquier otro nombre de "
                       "la península. Candidato a nodo en asentamientos.yaml.",
        "lecturas": [
            {"tipo": "etimologia-analitica",
             "lectura": "'atarraya' en warao (guaraúno); «Miraca sanuco: atarraya "
                        "pequeña»",
             "quien": "Esteves 1989", "fecha": "2026-09-07", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=52),
             "veredicto": "sin cita ni ruta de contacto warao–caquetío; encaja con "
                          "un pueblo de costa pescadora, que es poco. Misma "
                          "cuarentena que sus atribuciones caribe insular y "
                          "cumanagota"},
        ],
    },
    # ── Lote 4 (2026-09-07): los del mapa con otra grafía en Esteves ──
    "jarayadito": {
        "id": "toponimo-102", "fuente": "esteves-1989", "pagina": 46,
        "glosa_fuente": "«Jarayadito significa espinar, retamal, ñaragatal. El "
                        "sufijo dito es distintivo de los nombres colectivos "
                        "abundanciales»",
        "segmentacion": "jaraya + -dito",
        "razon": "`-dito` colectivo abundancial está atestiguado por Esteves "
                 "cuatro veces y atribuido al caquetío; la base jaraya "
                 "'espina, retama' se despeja por sustracción de la glosa, sin "
                 "recurrencia. Cierra la mitad.",
        "observacion": "⭐ Tres grafías en tres siglos y el nombre sigue vivo: "
                       "Sarayadite (censo de 1881), Jarayadito (Esteves), "
                       "UARAYADITO (mapa vivo, fotos de Miguel 2026-09-01, junto a "
                       "Moruy y Cayerúa). La inicial j ~ s ~ u es la misma "
                       "aspiración inestable de Hurehurebo ~ Jurijurebo. Aldea del "
                       "municipio Moruy; 1881: 9 casas, 58 vecinos.",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "vivo en el mapa actual como Uarayadito, en el mismo "
                        "sector que Moruy y Cayerúa",
             "quien": "Miguel Gil Urbina (fotos del mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
    "barunú": {
        "id": "toponimo-103", "fuente": "esteves-1989", "pagina": 23,
        "glosa_fuente": "«El nombre viene de Barubaru (palo delgado), palmera con "
                        "cuyas hojas fabrican esteras los nativos. Esta palmera "
                        "abunda en las faldas del Cerro de Santa Ana»",
        "segmentacion": "baru~baru (bara 'palo', reduplicado) + -nú",
        "razon": "`bara` 'palo, árbol' es caquetío-atestiguado y la reduplicación "
                 "es patrón del corpus (jurijurebo, quibaquiba, barabara "
                 "'olivo'); el -nú final queda sin explicar y el fitónimo "
                 "barubaru no tiene segunda fuente. Cierra a medias.",
        "observacion": "Aldea al norte de Moruy; 1881: 5 casas, 29 habitantes. "
                       "Esteves lo pone en su serie Bara- indígena (Bariquí, "
                       "Baracara, Barunú, p. 22). En el mapa vivo, PARUNU (fotos "
                       "de Miguel): p por b y u por ú, y el nombre sigue.",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "vivo en el mapa actual como Parunu, sector del Capubana",
             "quien": "Miguel Gil Urbina (fotos del mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
        ],
    },
    "cayeruba": {
        "id": "toponimo-104", "fuente": "esteves-1989", "pagina": 30,
        "glosa_fuente": "«¿Origen de la voz? ¿Simaruba? Es posible, hay "
                        "abundancia de este árbol rutáceo en sus contornos» "
                        "(leído en la imagen; la línea está borrosa en el OCR)",
        "segmentacion": "caye + ruba (?)   [conjetura fitonímica del autor]",
        "razon": "Esteves solo conjetura, con interrogación, un fitónimo "
                 "(simaruba); ningún morfema del canon alinea. Lo que sí está "
                 "firme es la existencia y la antigüedad del lugar, por cuatro "
                 "vías: cerámica aborigen abundante y un cementerio (Esteves), "
                 "pueblo de Paraguaná en 1556 según Arcaya (vía Esteves p. 52), "
                 "Cayerda como primer asiento de los Amuayes en Delmonte 1883 "
                 "(vía Oliver p. 276), y el sitio FAL-143 de Oliver "
                 "(nodo-025, dabajuroide, precontacto probable).",
        "observacion": "⭐ Un lugar, cuatro grafías: Cayerda / Cayerta / "
                       "«Coyarna» (Delmonte vía Oliver), Cayeruba (Esteves, que "
                       "llama a la grafía Cayerúa «nacida de snobismo»), y "
                       "CAYERÚA en el mapa vivo, la forma que Miguel verificó "
                       "(«Cayerda no existe, pero Cayerúa sí»). Aldea de Pueblo "
                       "Nuevo, omitida en el censo de 1881 («la omisión es "
                       "inexplicable»).",
        "lecturas": [
            {"tipo": "testimonio-residente",
             "lectura": "«Cayerda no existe, pero Cayerúa sí»: en el mapa actual "
                        "aparece Cayerúa cerca de Moruy, con Uarayadito en el "
                        "mismo sector",
             "quien": "Miguel Gil Urbina (mapa)", "fecha": "2026-09-01",
             "eje": "referente"},
            {"tipo": "hipotesis",
             "lectura": "Cayerda (Delmonte 1883), Cayeruba (Esteves 1989) y "
                        "Cayerúa (mapa 2026) son un solo lugar, el primer asiento "
                        "de los Amuayes; las variantes -erda/-erta/-eruba/-erúa "
                        "son ruido de transmisión sobre un mismo nombre",
             "quien": "proyecto", "fecha": "2026-09-07", "eje": "referente",
             "procedencia": dict(obra="oliver-1989-cap3", pagina=276),
             "veredicto": "muy probable por la geografía (Esteves y el mapa lo "
                          "ponen donde Delmonte); sin documento que las iguale"},
        ],
    },
    # ── Lote 5 (2026-09-07): los nodos de la era 2 — Moruy, Chamuriana, Adícora ──
    "moruy": {
        "id": "toponimo-108", "fuente": "esteves-1989", "pagina": 53,
        "glosa_fuente": "«Es más aceptable considerar la voz como una alteración "
                        "de merejuy, cierta levadura o preparación agria que "
                        "usaban para acelerar la fermentación del maíz cocido con "
                        "que elaboraban la chicha embriagadora, que consumían en "
                        "ceremonias religiosas»",
        "segmentacion": "moruy (< merejuy, según Esteves; sin composición)",
        "razon": "la etimología es propuesta de Esteves («más aceptable»), sin "
                 "fuente, y merejuy no está en el lexicón; el paso merejuy → "
                 "moruy pide varios cambios vocálicos y una síncopa. Ningún "
                 "morfema del canon alinea. Lo firme es el lugar: asiento del "
                 "clan Amuay tras el reasentamiento desde Cayerda (Delmonte 1883 "
                 "vía Oliver), pueblo de Paraguaná en 1556 (Arcaya vía Esteves "
                 "p. 52), sitio FAL-149 de Oliver (nodo-027), 213 casas en 1881, "
                 "y hoy capital de municipio.",
        "observacion": "⭐ Esteves: «los indios de Moruy eran los más belicosos de "
                       "Paraguaná, hay testimonios escritos» de sus peleas contra "
                       "los españoles que les usurpaban tierras — contra el "
                       "«Caquetío, who were always peaceful» de Oliver (n. 154): "
                       "otra etiqueta colonial. «La comunidad con más apego a las "
                       "costumbres de sus antepasados»: cerámica, silletas, "
                       "bernegales, jabón de la tierra; apellidos sin deformar "
                       "(Caguao, Cuauro, Mabo, Guarecuco, Cotopo). Es uno de los "
                       "dos nodos de la era 2 (DISENO_ERA2 §2). La versión de "
                       "merejuy que Miguel recogió «sin identificar» era esta "
                       "página.",
        "lecturas": [
            {"tipo": "etimologia-popular",
             "lectura": "los naturales temían a los moros (los piratas) y al ver "
                        "barcos gritaban «¡Moro... uy!»",
             "quien": "tradición oral, recogida por Esteves y por Miguel",
             "fecha": "2026-09-01", "eje": "significado",
             "procedencia": dict(obra="esteves-1989", pagina=53),
             "veredicto": "Esteves: «demasiado infantil»; el proyecto: etimología "
                          "de anécdota, improbable"},
            {"tipo": "etimologia-popular",
             "lectura": "del quechua muru 'viruela' o 'pepa'",
             "quien": "tradición recogida por Miguel", "fecha": "2026-09-01",
             "eje": "significado",
             "veredicto": "exige préstamo quechua sin ruta: improbable"},
            {"tipo": "hipotesis",
             "lectura": "Moruy era un cacique: topónimo < antropónimo, el patrón "
                        "regional (cf. Manaure)",
             "quien": "tradición recogida por Miguel; validación del proyecto",
             "fecha": "2026-09-01", "eje": "referente",
             "veredicto": "compatible con merejuy por la regla 0 (un cacique puede "
                          "llamarse por el oficio del sitio); sin documento"},
            {"tipo": "hipotesis",
             "lectura": "Moruy y Santa Ana (Chamuriana) eran del mismo clan, en "
                        "órbita del Capubana: Moruy donde se hacía el merejuy para "
                        "la chicha ritual, a la izquierda del cerro; la asignación "
                        "de Delmonte (Guaranaos en Santa Ana) describiría geografía "
                        "colonial",
             "quien": "Miguel Gil Urbina", "fecha": "2026-09-01", "eje": "referente",
             "veredicto": "canon-simulacion como modelo espacial (validación en "
                          "toponimia_paraguana_miguel.yaml §capubana-centro-sagrado); "
                          "Oliver confirma el REASENTAMIENTO Cayerda → Moruy, que "
                          "huele a reducción colonial"},
        ],
    },
    "chamuriana": {
        "id": "toponimo-109", "fuente": "esteves-1989", "pagina": 35,
        "glosa_fuente": "«Antigua aldea indígena en cuyas cercanías los españoles "
                        "fundaron en 1538 el pueblo de Santa Ana de Paraguaná. En "
                        "el lugar se hallan restos de cerámica indígena y europea. "
                        "Nada sabemos del significado de la voz»",
        "segmentacion": "chamur- + -iana",
        "razon": "Esteves no glosa. Lo único que alinea es la terminación -iana, "
                 "la misma de Coriana/Curiana, sobre el formante -ana (forma "
                 "atestiguada, glosa 'lugar de' en disputa, #109): un dato más "
                 "para esa cola, no una etimología. Lo firme es el referente: la "
                 "aldea nativa anterior a 1538 junto a la que se fundó Santa Ana, "
                 "con cerámica indígena y europea (nodos 013 y 024: el cerro "
                 "tiene tres dataciones precontacto, hasta 1415).",
        "observacion": "⭐ El nombre nativo del sitio de Santa Ana, que Miguel "
                       "había hallado en investigación coloquial sin fuente "
                       "citable: la fuente es esta (p. 35). Esteves fecha la "
                       "fundación española en 1538; Miguel la da como franciscana. "
                       "Con Moruy, Cayerúa y Maitiruma orbita el Capubana: el otro "
                       "nodo de la era 2.",
        "lecturas": [
            {"tipo": "tradicion-local",
             "lectura": "«elegida por los nativos debido a la abundancia de agua "
                        "dulce que bajaba del cerro»",
             "quien": "crónica local, recogida por Miguel", "fecha": "2026-09-01",
             "eje": "referente",
             "veredicto": "sin procedencia para la frase; el agua del cerro es "
                          "verificable (Maitiruma, el bosque xerófito)"},
            {"tipo": "hipotesis",
             "lectura": "el pueblo de Santa Ana es fundación colonial (franciscana "
                        "según Miguel, «los españoles» en 1538 según Esteves) y el "
                        "nodo norte precontacto no puede anclarse en él como "
                        "pueblo: el sitio y su agua se llamaban Chamuriana",
             "quien": "Miguel Gil Urbina", "fecha": "2026-09-01", "eje": "referente",
             "veredicto": "Esteves lo sostiene: aldea indígena ANTERIOR a la "
                          "fundación, con cerámica de las dos épocas"},
        ],
    },
    "supí": {
        "id": "toponimo-077", "fuente": "esteves-1989", "pagina": 61,
        "glosa_fuente": "es un árbol cactáceo que exuda una goma medicinal, es el "
                        "guamacho Pereskia de los botánicos",
        "segmentacion": "supí (fitónimo, sin composición)",
        "razon": "el topónimo ES una palabra atestiguada, pero con dos glosas que "
                 "no coinciden: Zavala da `supi` 'sitio a orilla del mar; arena; "
                 "arboleda supide' (lexicón, caquetío-atestiguado) y Esteves "
                 "'guamacho (Pereskia)'. Dos lugares en Paraguaná: el balneario "
                 "El Supí cerca de Adícora y otro en Baraived. Sin cognado que "
                 "decida, queda en C con el conflicto declarado.",
        "observacion": "En El Supí, playa de Adícora, «hay un placer de piedras "
                       "escritas» (petroglifos): el único rastro no funerario del "
                       "conjunto arqueológico de Paraguaná que reporta Esteves. "
                       "En el mapa vivo.",
        "lecturas": [
            {"tipo": "glosa-fuente",
             "lectura": "supi: sitio a orilla del mar; arena; arboleda supide",
             "quien": "Zavala Reyes 2015 (glosario)", "fecha": "2026-09-06",
             "eje": "significado", "procedencia": dict(obra="zavala-reyes-2015"),
             "veredicto": "compite con el fitónimo de Esteves; un balneario de "
                          "arena a orilla del mar encaja con las dos"},
        ],
    },
}

# ───────────────────────────────────────────────────────────────────────────
# NIVEL D — descartes razonados
# ───────────────────────────────────────────────────────────────────────────
# Documentar el descarte vale tanto como el hallazgo: evita re-minarlo.

DESCARTES = {
    # Lote 3 (2026-09-07): las ciudades «de grandísimo momento» de Castellanos
    # (II, Elegía 1, 1589) que ninguna fuente glosa. Son atestaciones de
    # EXISTENCIA del s. XVI, no de significado: por eso están en
    # asentamientos.yaml como nodos y aquí como descartados. Varias siguen
    # vivas — Zazárida, Capatárida — y eso es dato aunque no haya etimología.
    "Castellanos 1589: nombrados en las Elegías, sin glosa en ninguna fuente": {
        "razon": "Castellanos enumera, no traduce; Arcaya y Esteves los sitúan "
                 "o los dan por perdidos; ningún morfema del canon alinea sin "
                 "forzar. Se registran con su forma de 1589, su identificación "
                 "moderna y su nodo, para que la campaña no los vuelva a abrir "
                 "sin dato nuevo.",
        "fuente": "castellanos-elegias",
        "ids": {"hurraque": "toponimo-096", "zazarida": "toponimo-097",
                "carao": "toponimo-098", "tomodore": "toponimo-099",
                "capatarida": "toponimo-100", "carona": "toponimo-101"},
        "paginas": {"hurraque": "185 (línea 48260)", "zazarida": "185 (línea 48249)",
                    "carao": "185 (línea 48251)", "tomodore": "185 (línea 48251)",
                    "capatarida": "185 (línea 48251)", "carona": "185 (línea 48252)"},
        "formas": [
            "hurraque (Hurraqui en Castellanos; «pueblo caquetío mencionado por "
            "Juan de Castellanos» en Esteves p. 43, que supone Jurraque como "
            "pronunciación primitiva y no sabe dónde estuvo: quizá Misaray, en "
            "Machuruca, donde hay cementerio indígena, o El Supí, donde hay "
            "piedras escritas; la grafía en -i explica el cero de Oliver)",
            "zazarida (Zacerida en Castellanos; Sacerida/Zazárida en Arcaya; "
            "carta de Bastidas 1538 vía Oliver p. 251, nodo-006; hoy Zazárida, "
            "población viva de Falcón)",
            "carao (Castellanos; «Arcaya lo suponía en el actual Carazao»)",
            "tomodore (Tamadoré en Castellanos; Tomadoré cerca de La Vela según "
            "Arcaya; carta de Bastidas 1538 vía Oliver p. 251, nodo-004)",
            "capatarida (Capatarida en Castellanos; carta de Bastidas 1538 vía "
            "Oliver p. 251, nodo-007; hoy Capatárida, capital del municipio "
            "Buchivacoa: nombre vivo desde 1538)",
            "carona (Castellanos; Arcaya: «ni el nombre queda» — pues aquí está, "
            "en 1589)",
        ],
    },
    # Lote 4 (2026-09-07): lo castellano del mapa vivo, registrado y no callado
    # (filtro 1 del protocolo del habla paraguanera).
    "castellano: nombres del mapa vivo en español": {
        "razon": "el nombre es transparente en castellano; no hay sustrato que "
                 "despejar. Se registra para que el barrido del mapa no lo "
                 "vuelva a proponer.",
        "ids": {"la rinconada": "toponimo-106", "pedregalito": "toponimo-107"},
        "formas": [
            "la rinconada (mapa vivo, sector del Capubana; fotos de Miguel 2026-09-01)",
            "pedregalito (mapa vivo, sector del Capubana; fotos de Miguel 2026-09-01)",
        ],
    },
    # La campaña de Esteves 1989, lote 1 (2026-09-06). El grupo trae `fuente`,
    # `paginas` e `ids` para que el migrador cite y no mueva el contador.
    # «Descartado» aquí = sin etimología despejable, NO «no existió»: los
    # dos son lugares vivos del mapa de Miguel.
    "Esteves 1989: sin glosa en la fuente y ningún morfema conocido alinea": {
        "razon": "Esteves da referente, censo e historia, pero ninguna glosa "
                 "propia: solo la etimología popular, que él mismo relativiza. "
                 "Sin ecuación bilingüe no hay morfema que despejar; se registra "
                 "para que la campaña no lo vuelva a abrir sin dato nuevo.",
        "fuente": "esteves-1989",
        "ids": {"charaima": "toponimo-082", "jacuque": "toponimo-089",
                "elegüey": "toponimo-091", "maragüey": "toponimo-092",
                "jamaica": "toponimo-093", "jayana": "toponimo-110"},
        "paginas": {"charaima": 35, "jacuque": 44, "elegüey": 37, "maragüey": 37,
                    "jamaica": 46, "jayana": 46},
        "formas": [
            "charaima (población entre Adícora y Baraived; censo 1881: 79 casas, "
            "527 habitantes; nombre primitivo Charaide en su Título de "
            "Composición; Esteves no sabe qué relación guarda con el cacique "
            "Charaima de Margarita, abuelo del guayquerí Francisco Fajardo)",
            "jacuque (sabanas y hatos en Jadacaquiva; Punta de Jacuque, por donde "
            "«no se puede confirmar históricamente» Federmann desembarcó los "
            "caballos de Santo Domingo en 1530; etimología popular: jaca "
            "andaluza + ¡huy!, «se dice que los nativos, sorprendidos al ver los "
            "caballos o jacas, exclamaron, asustados»)",
            # Lote 2 (2026-09-07): los «caribe insular» que B.6 dejó sin estrato.
            # Esteves no da glosa, solo la etiqueta — y la etiqueta es inferencia
            # suya sobre la terminación -güey, con nombre de lengua equivocado
            # (el caribe insular de Breton es arahuaco). Ver oliver_324_caribes §5.
            "elegüey (nombre antiguo de Punta Cardón, hoy solo del cementerio "
            "viejo en la Puntica; «es voz taína, del caribe insular», sin glosa: "
            "lo que Esteves ve es la terminación -güey, formante de la toponimia "
            "taína; ningún morfema caquetío alinea)",
            "maragüey (pequeña península en Casicure, en la otra costa del "
            "Golfete de Coro; «también es voz taína», sin glosa; misma "
            "terminación -güey que Elegüey; no está en el índice de Esteves "
            "porque no es de Paraguaná)",
            "jamaica (lugar de Buenavista formado alrededor de «la casa grande de "
            "Jamaica»: con toda probabilidad una hacienda bautizada con el nombre "
            "de la isla; la glosa que da Esteves, «tierra de los manantiales», es "
            "la etimología taína de la isla, de los libros, no un dato local)",
            # 2026-09-07, con la decisión B de #109: Miguel pidió que los -ana
            # sin glosa entren a la lista, y nombró a Jayana. Nombre vivo.
            "jayana (antiguo fundo pecuario cerca de Amuaicito, hoy caserío del "
            "municipio Los Taques; con Adícora, único puerto de Paraguaná con "
            "Resguardo Marítimo en la Colonia, habilitado en 1834 para exportar "
            "ganado en pie; Esteves cree que es el Guarama de un mapa antiguo; "
            "sin glosa; termina en -ana, formante sin glosa desde #109: está en "
            "la lista viva de 6-fusion/censo_ana_esteves_109.yaml)",
        ],
    },
    "glosa meramente referencial": {
        "razon": "la glosa IDENTIFICA al referente (quién es, dónde queda) sin "
                 "traducirlo. No hay ecuación bilingüe: no hay significado que "
                 "despejar.",
        # 2026-09-07: cinco formas siguen aquí SOLO para que el contador de ids
        # no se mueva (el migrador las salta): los cuatro Quicer- viven en el
        # grupo «antropónimos de Barquisimeto» con sus ids 030-033, y quiquiba
        # se rehabilitó a NIVEL_C con su id 034.
        "reubicados": ["quiceraguru", "quiceroaboa", "quiceromata", "quiciroata",
                       "quiquiba"],
        "formas": ["baracoica (Cacique de Curazao)", "huay (Nombre propio)",
                   "quiceraguru", "quiceroaboa", "quiceromata", "quiciroata",
                   "quiquiba", "tamani", "timaure (Apellido)",
                   "tumarure (Apellido de un cacique)",
                   "xaraguamari (Cacique de Yaracuy)",
                   "yarosabana (Cacique de los Guaragua)",
                   "dabajuro (Población de Falcón)", "doaca (Asiento indígena)",
                   "iboa (Comunidad indígena)", "parotaima (Indígena del Yaracuy)",
                   "tabicure (Indio caquetío del valle de las Damas)",
                   "todarahuato (Indígena de la Vela)",
                   "yaracuy (Indígena del Valle de las Damas)",
                   "caquetío (Buena gente — etnónimo, no descripción del lugar)",
                   "xirahara (Población indígena vecina)",
                   "yaruca (Indígena caquetío)"],
    },
    "antropónimos de Barquisimeto (Zavala #207-210)": {
        "razon": "la fuente los glosa como «Nombre propio indígena en "
                 "Barquisimeto»: son antropónimos, no topónimos, y de otra "
                 "polity (regla 4). Estaban como topónimos de glosa referencial "
                 "desde el origen del registro; reclasificados el 2026-09-07 "
                 "(propuesta del 2026-08-25, lengua_toponimia_quibacoa.yaml "
                 "§bug-antroponimos-como-toponimos). Conservan sus ids.",
        "clase": "antropónimo",
        "polity": "barquisimeto",
        "fuente": "zavala-reyes-2015",
        "ids": {"quiceraguru": "toponimo-030", "quiceroaboa": "toponimo-031",
                "quiceromata": "toponimo-032", "quiciroata": "toponimo-033"},
        "formas": ["quiceraguru (Nombre propio indígena en Barquisimeto)",
                   "quiceroaboa (Nombre propio indígena en Barquisimeto)",
                   "quiceromata (Nombre propio indígena en Barquisimeto)",
                   "quiciroata (Nombre propio indígena en Barquisimeto)"],
    },
    "glosa circular": {
        "razon": "la 'traducción' es el propio topónimo castellanizado. No "
                 "aporta significado.",
        "formas": ["cemirucos → 'Semerucos'",
                   "aruba → 'Oruba. Oruma. Oirubae'"],
    },
    "glosa mutilada en la fuente": {
        "razon": "Zavala deja la glosa incompleta; no hay con qué alinear.",
        "formas": ["coroque → 'Árbol de ¿?'"],
    },
    "castellanización moderna": {
        "razon": "formación española sobre base indígena o no; la terminación "
                 "delata la creación en español.",
        "formas": ["zamurano ← esp. *zamuro* + -ano"],
    },
    "opacos: ningún morfema conocido alinea": {
        "razon": "la glosa es descriptiva y utilizable, pero ninguna "
                 "segmentación reconstruye nada. Son los que quedan para una "
                 "pasada futura con más morfemas en el inventario.",
        "formas": ["aburí (aguas de un río lleno de arena)",
                   "acatute (Pueblo entre valles)",
                   "alcaboa (Tierras solas o desiertas)",
                   "aricula (Punto de tierra)", "guanajo (Cardón muy lanoso)",
                   "guasare (Árbol cactáceo)", "siguruba (Salvar. Caserío)",
                   "tarai (Garipial o caripial)"],
    },
    "van Buurt §8-10 sin contenido segmentable": {
        "razon": "el comentario del autor es histórico o anecdótico, no "
                 "etimológico: no hay glosa que despejar.",
        "formas": ["Adicoura", "Amboïna", "Arashi", "Burubunu", "Buynari",
                   "Curaçao", "Macuarima", "Matividiri", "Taratata",
                   "Yatu Bacu", "Balashi", "Onima", "Cariatávo"],
    },
}

# ───────────────────────────────────────────────────────────────────────────
# CORROBORACIÓN DEL LEXICÓN  —  pregunta 1
# ───────────────────────────────────────────────────────────────────────────
# Palabras del lexicón que quedan confirmadas por aparecer DENTRO de un
# topónimo cuya glosa es consistente con la suya. Es corroboración barata e
# independiente: alimenta el eje FIDELIDAD sin minar una fuente nueva.

CORROBORACIONES_LEXICON = {
    # ── independientes: la glosa del TOPÓNIMO confirma la de la PALABRA, y
    #    son dos listados distintos de la fuente (glosario vs. toponimia).
    "bacoa": {"glosa_lexicon": "bosque, lugar, paraje, sitio fértil",
              "toponimos": ["adabacoa", "guadabacoa", "quibacoas",
                            "yacarebacoa"], "independencia": "alta"},
    "ebo": {"glosa_lexicon": "camino, paso, senda",
            "toponimos": ["cumarebo", "jurijurebo"], "independencia": "alta",
            "nota": "dos contraejemplos con glosa divergente: guacurebo, "
                    "turijerebo"},
    "juri": {"glosa_lexicon": "viento, ventarrón", "toponimos": ["jurijurebo"],
             "independencia": "alta",
             "nota": "y eco insular en Hudishibana 'windy plain' (van Buurt)"},
    "kiba": {"glosa_lexicon": "piedra", "toponimos": ["quibacoas"],
             "independencia": "alta",
             "nota": "grafías fuente quiva/quiba/cuiva (colisiones D5 2026-08-31: "
                     "fusionadas como kiba, con kiba-2 'ayuda' de homónimo "
                     "declarado). El topónimo corrobora kiba-1 'piedra' — y Zavala "
                     "#92 «Cuiva. Kiba» trae la grafía k impresa"},
    "barici": {"glosa_lexicon": "agua turbia, tierras coloradas rojizas",
               "toponimos": ["barisi"], "independencia": "alta"},
    "bariki": {"glosa_lexicon": "tierra colorada",
               "toponimos": ["bariquisimeto"], "independencia": "media"},
    "dabuda": {"glosa_lexicon": "barro loza", "toponimos": ["dabudare"],
               "independencia": "alta"},
    "dare": {"glosa_lexicon": "diente; hijo", "toponimos": ["capadare"],
             "independencia": "alta"},
    "para/paragua": {"glosa_lexicon": "mar, agua extensa",
                     "toponimos": ["paraguaná"], "independencia": "alta"},
    "wa": {"glosa_lexicon": "conuco, heredad, terreno cercado cultivado",
            "toponimos": ["guamabatriba"], "independencia": "media",
            "nota": "compite con el prefijo gua-/wa- de pluralidad"},
    # ── NO independientes: el morfema salió del mismo análisis etimológico que
    #    ahora lo 'confirma' (van Buurt §8-10). Se listan aparte para no
    #    inflar la cuenta.
    "siba": {"glosa_lexicon": "piedra, roca", "toponimos": ["Casibari"],
             "independencia": "NULA — van Buurt derivó el morfema DE este "
                              "topónimo"},
    "ka-": {"glosa_lexicon": "localizador 'hay'", "toponimos": ["Casibari"],
            "independencia": "NULA — ídem"},
    "rí": {"glosa_lexicon": "fuerte, duro", "toponimos": ["Casibari"],
           "independencia": "NULA — ídem"},
    "bana": {"glosa_lexicon": "ancho, llano", "toponimos": ["Hudishibana"],
             "independencia": "NULA — ídem"},
    "kari": {"glosa_lexicon": "costa, orilla", "toponimos": ["Cariatávo"],
             "independencia": "NULA — ídem"},
    "bala": {"glosa_lexicon": "el mar", "toponimos": ["Balashi"],
             "independencia": "NULA — ídem"},
    "-ima": {"glosa_lexicon": "humedad, quebrada",
             "toponimos": ["alaurima", "Onima"], "independencia": "media",
             "nota": "`alaurima` SÍ es independiente (Zavala); `Onima` no"},
}

# ───────────────────────────────────────────────────────────────────────────
# REDUPLICACIÓN  —  pregunta 2
# ───────────────────────────────────────────────────────────────────────────

REDUPLICACION = {
    "afirmacion_de_gatschet": (
        "Gatschet 1885, sobre los topónimos de Aruba: varios se forman por "
        "duplicación de la raíz disílaba, proceso usado —dice— para la "
        "onomatopeya, para los diminutivos, o para objetos que existen en gran "
        "número."
    ),
    "medicion": {
        "toponimos_del_corpus": "26 de 287 formas (9%) con unidad reduplicada "
                                "de ≥3 caracteres",
        "lexicon_caquetio": "9 de 210 formas de ≥5 caracteres (4,3%), "
                            "descontando dos falsos positivos gráficos "
                            "(`barbasco`, préstamo español; `barbache`)",
        "control_wayunaiki": "22 de 703 (3,1%)",
        "control_lokono": "1 de 138 (0,7%)",
        "control_taino": "0 de 40 (0%)",
    },
    "veredicto": (
        "SÍ es un proceso productivo, y el control cuantitativo lo sostiene: "
        "la tasa en el corpus caquetío (toponimia 9%, léxico 4,3%) está por "
        "encima de la de las lenguas hermanas del mismo lexicón (wayunaiki "
        "3,1%, lokono 0,7%, taíno 0%). No es un artefacto del método de "
        "detección, porque el método es el mismo para todas."
    ),
    "valores_semanticos": {
        "onomatopeya (fauna)": {
            "peso": "DOMINANTE — 7 de las 9 reduplicaciones del léxico son "
                    "nombres de animales, y 5 de ellas son aves",
            "casos": ["warawara 'caracara'", "chuchubi 'sinsonte'",
                      "chuchube 'paraulata'", "querequere 'ave pequeña'",
                      "humohumo 'el ave que vuela'", "chogogo 'flamenco'",
                      "tuqueque 'gecko'"],
            "insular": ["Warawara (Seru, Aruba)", "Wao-Wao (Seru)",
                        "Wiriwari (Boca)", "Kodekodectu"],
        },
        "pluralidad / abundancia": {
            "peso": "SOSTENIDO por el mejor caso del corpus",
            "casos": ["jurijurebo 'Paso de los VIENTOS' ← juri 'viento' "
                      "(singular en el lexicón, plural en la glosa)",
                      "Shishiribana frente a Shiribana / Siribana — el MISMO "
                      "topónimo con y sin reduplicación de la sílaba inicial, "
                      "en Bonaire y Aruba respectivamente"],
        },
        "especificación / intensidad": {
            "peso": "PLAUSIBLE, sin glosa que lo pruebe",
            "casos": ["barabara 'árbol de madera DURA y pesada' ← bara 'árbol' "
                      "(van Buurt §5)",
                      "quibaquibi 'baquiano, conocedor'",
                      "patapati 'anegadizo'", "pariri 'pantano'"],
        },
        "diminutivo": {
            "peso": "SIN APOYO",
            "nota": "Gatschet lo menciona, pero ni un solo caso del corpus lo "
                    "sostiene. El diminutivo caquetío documentado es afijal: "
                    "`-iro` (Zavala #166) y `-bi` (van Buurt §6). **Este es un "
                    "punto donde el dato disponible contradice a la fuente y "
                    "hay que decirlo.**",
        },
    },
    "propuesta_para_REGLAS_ZAVALA": {
        "regla": "REDUPLICACIÓN de la raíz (total o con haplología de la vocal "
                 "final de la segunda copia)",
        "forma": "X + X  →  X~X    ·    X + X(-V)  →  X~X'  (haplología)",
        "valor": "(1) formación de nombres de animales por onomatopeya; "
                 "(2) pluralidad o abundancia del referente",
        "ejemplo_canonico": "juri 'viento' → juri~jur-ebo 'paso de los vientos'",
        "advertencia": "El valor (1) es formación léxica, no morfología "
                       "productiva en el habla: un agente no debería "
                       "reduplicar para 'inventar un ave'. El valor (2) sí es "
                       "candidato a regla viva.",
    },
}

# ───────────────────────────────────────────────────────────────────────────
# ANTROPÓNIMOS  —  pregunta 3
# ───────────────────────────────────────────────────────────────────────────

ANTROPONIMOS = {
    "total": 14,
    "con_glosa_descriptiva": 1,
    "resueltos": 0,
    "detalle": {
        "chunare": "Apellido. Mazorca tierna — la única glosa con contenido "
                   "léxico. No segmenta (nivel C).",
        "los_otros_13": "'Nombre propio', 'Apellido', 'Cacique de X', 'nombre "
                        "indígena del Yaracuy' — puras etiquetas de referencia.",
    },
    "veredicto": (
        "**Los antropónimos NO rinden como los topónimos, y por una razón "
        "estructural, no por mala suerte.** Un topónimo se glosa describiendo "
        "el lugar ('Río escondido'); un antropónimo se glosa identificando a la "
        "persona ('Cacique de Curazao'). La ecuación bilingüe existe solo "
        "cuando la fuente TRADUCE, y con los nombres de persona Zavala casi "
        "nunca traduce: los ubica. Rendimiento 1/14 en glosa utilizable y 0/14 "
        "en descomposición, frente a 20/45 utilizables y 11/45 con algún "
        "resultado en los topónimos."
    ),
    "consecuencia": "No vale la pena buscar más antropónimos con este método. "
                    "Sí vale la pena, en cambio, que las minerías futuras "
                    "registren la glosa COMPLETA de un antropónimo cuando la "
                    "haya: `chunare` demuestra que a veces la hay.",
}

# ───────────────────────────────────────────────────────────────────────────
# FORMATIVOS FRECUENTES SIN GLOSA  —  lo que queda abierto
# ───────────────────────────────────────────────────────────────────────────
# Los 207 topónimos insulares no tienen traducción, así que no rinden ecuación.
# Pero sí muestran QUÉ formantes son frecuentes — y por tanto dónde valdría la
# pena buscar una glosa en una fuente futura.

FORMATIVOS_SIN_GLOSA = {
    "-shi / -chi": {
        "apariciones": 22,
        "ejemplos": ["Balashi", "Hudishibana", "Arashi", "Bushiri", "Cadushi",
                     "Canashito", "Cashunti", "Catashi", "Cudishi", "Macoshi",
                     "Tibushi", "Teishi", "Sasarawichi", "Angochi", "Anamichi"],
        "nota": "**El formante más frecuente del corpus insular y nadie lo ha "
                "glosado.** Ni Gatschet, ni van Buurt, ni Zavala. Es el "
                "objetivo nº 1 de cualquier minería futura de toponimia ABC.",
    },
    "-ari / -ri": {
        "apariciones": 7,
        "ejemplos": ["Handebirari", "Kasiaari", "Yabarubari", "Arikurari",
                     "Cubari", "Damari", "Kassibari"],
        "nota": "van Buurt glosa `rí` 'fuerte, duro, durable' solo dentro de "
                "Casibari. Falta comprobar si vale igual en los otros seis.",
    },
    "-kuri / -curi": {
        "apariciones": 3,
        "ejemplos": ["Warerukuri", "Antikuri", "Kamakuri"],
        "nota": "ya señalado en SUFIJOS_NO_CODIFICADOS de lexicon_gatschet.",
    },
    "-bari": {
        "apariciones": 3,
        "ejemplos": ["Yabarubari", "Cubari", "Kassibari"],
        "nota": "⚠ INDICE_FUENTES ya concluyó que **`-bari` no es un afijo**; "
                "van Buurt lo explica como `bara`/`bari` 'árbol'. Coherente "
                "con que aparezca en posición final de topónimos.",
    },
    # #109, decisión B de Miguel (2026-09-07): la forma está atestiguada, la
    # glosa 'lugar de' se retira. El censo de Esteves dio cero casos glosados
    # así (6-fusion/censo_ana_esteves_109.yaml): el 'lugar' paraguanero es
    # -bacoa. Paraguaná dejó de sostenerla (segmentación abierta) y Curiana
    # tiene expediente propio (#33). La lista de abajo es VIVA: cada -ana
    # nuevo sin glosa entra aquí; si una fuente glosa uno como 'lugar de', se
    # reabre #109.
    "-ana": {
        "apariciones": 6,
        "ejemplos": ["Paraguaná", "Curiana", "Chamuriana", "Cujicana",
                     "Jayana", "Coria-na (aldea wanebucán de la Guajira, "
                     "Oliver 1989 cap. 3 p. 207)"],
        "nota": "Forma atestiguada, **glosa retirada** (#109, decisión B, "
                "2026-09-07). Tenía 'lugar de' con dos apoyos, Paraguaná y "
                "Curiana; Paraguaná no descompone con ella («Rodeada del mar», "
                "«conuco en medio del mar» en Esteves p. 56) y Curiana no "
                "tiene glosa de fuente. Censo de Esteves: 13 formas en -ana, "
                "6 son -bana, 1 es -bana con h (Capuhana), 2 llevan el -ana en "
                "la raíz, 4 sin glosa, 0 'lugar de'. Compite con na 'como, "
                "semejante' (Zavala #184) y con -ná tónica de Paraguaná. "
                "Excluye -bana (#38, resuelto) y los -ana dentro de raíz "
                "(guariana, maracapana). El motor conserva -ana 'lugar de' "
                "como convención de la simulación (canon-simulación), no "
                "como dato.",
    },
}

# ───────────────────────────────────────────────────────────────────────────
# CONFLICTOS QUE ESTE ANÁLISIS ABRE  (para F1 / el tablero de decisiones)
# ───────────────────────────────────────────────────────────────────────────

CONFLICTOS = {
    "quiba": "El lexicón tiene `quiba` = 'ayuda' (Zavala #203) y "
             "`quiva`/`cuiva` = 'piedra'. `quibacoas` 'Bosques PEDREGOSOS' y "
             "van Buurt §8 ('siba or quiba means stone') apoyan 'piedra'. "
             "Probable homógrafo mal fusionado.",
    "guaca": "El lexicón tiene `guaca` = 'ave, cotorra' (Zavala). van Buurt §6 "
             "(vía Oliver 1989) tiene `waka` = 'subterráneo, bajo tierra'. "
             "`guacaubana` = 'Río ESCONDIDO' apoya la segunda. Dos morfemas "
             "distintos que colapsan en la misma grafía castellana.",
    "-are vs -ure": "Evidencia toponímica: 'sitio de'. van Buurt §5 (Cruz "
                    "Esteves 1989): 'raíz'. Glosa en disputa — hermana de la "
                    "D9 de `-bana`.",
    "barici / bariki": "Dos entradas del lexicón con glosas solapadas y una "
                       "misma raíz probable `bari-` 'rojizo, turbio'. Los "
                       "topónimos `barisi` y `bariquisimeto` conservan las dos "
                       "variantes.",
}

# ───────────────────────────────────────────────────────────────────────────

TOTALES = {
    "toponimos_glosados_procesados": 74,
    "  zavala_toponimos": 45,
    "  zavala_antroponimos": 14,
    "  van_buurt_etimologias": 15,
    "toponimos_sin_glosa_como_control": 244,
    "  gatschet_1885": 31,
    "  van_buurt_s7_variantes": 213,
    "nivel_A": 6,
    "nivel_B": 8,
    "nivel_C": 13,
    "nivel_D": 47,
    "morfemas_despejados": 6,
    "  nuevos": 3,          # -are, ada-, yacare
    "  corroborados_o_reagrupados": 3,   # -bacoa, bari-, wa-
    "palabras_del_lexicon_corroboradas": 10,   # independencia alta o media
    "palabras_corroboradas_sin_independencia": 6,
    "reduplicacion": "productiva — ver REDUPLICACION",
    "antroponimos_utiles": 1,
}
