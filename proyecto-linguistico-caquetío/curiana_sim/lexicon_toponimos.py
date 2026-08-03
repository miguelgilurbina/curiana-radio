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
                       "toda la tarea F11.",
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
                       "CONFLICTOS.",
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
}

# ───────────────────────────────────────────────────────────────────────────
# NIVEL B — morfema nuevo despejado, recurrencia ≥2
# ───────────────────────────────────────────────────────────────────────────

NIVEL_B = {
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
                     "situación que `-bana` (DECISIONES_ABIERTAS D9).",
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
    "paraguana": {
        "glosa_fuente": "Rodeada del mar", "segmentacion": "para(gua) + -na",
        "razon": "corrobora `para`/`paragua` = 'mar' del lexicón. Pero 'rodeada' "
                 "no queda explicada y `-na` es demasiado frecuente (34 formas "
                 "del corpus) para significar nada demostrable.",
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
}

# ───────────────────────────────────────────────────────────────────────────
# NIVEL D — descartes razonados
# ───────────────────────────────────────────────────────────────────────────
# Documentar el descarte vale tanto como el hallazgo: evita re-minarlo.

DESCARTES = {
    "glosa meramente referencial": {
        "razon": "la glosa IDENTIFICA al referente (quién es, dónde queda) sin "
                 "traducirlo. No hay ecuación bilingüe: no hay significado que "
                 "despejar.",
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
                   "caquetio (Buena gente — etnónimo, no descripción del lugar)",
                   "xirahara (Población indígena vecina)",
                   "yaruca (Indígena caquetío)"],
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
        "formas": ["aburi (aguas de un río lleno de arena)",
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
    "quiva/quiba": {"glosa_lexicon": "piedra", "toponimos": ["quibacoas"],
                    "independencia": "alta",
                    "nota": "⚠ desambigua contra la entrada homógrafa "
                            "`quiba` = 'ayuda'"},
    "barici": {"glosa_lexicon": "agua turbia, tierras coloradas rojizas",
               "toponimos": ["barisi"], "independencia": "alta"},
    "bariki": {"glosa_lexicon": "tierra colorada",
               "toponimos": ["bariquisimeto"], "independencia": "media"},
    "dabuda": {"glosa_lexicon": "barro loza", "toponimos": ["dabudare"],
               "independencia": "alta"},
    "dare": {"glosa_lexicon": "diente; hijo", "toponimos": ["capadare"],
             "independencia": "alta"},
    "para/paragua": {"glosa_lexicon": "mar, agua extensa",
                     "toponimos": ["paraguana"], "independencia": "alta"},
    "gua": {"glosa_lexicon": "conuco, heredad, terreno cercado cultivado",
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
    "cari": {"glosa_lexicon": "costa, orilla", "toponimos": ["Cariatávo"],
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
}

# ───────────────────────────────────────────────────────────────────────────
# CONFLICTOS QUE ESTE ANÁLISIS ABRE  (para F1 / DECISIONES_ABIERTAS)
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
