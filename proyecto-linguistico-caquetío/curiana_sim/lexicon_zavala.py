"""
CURIANA — Glosario de Zavala Reyes (2015), importado por tiers
==============================================================

GENERADO por `minar_zavala_glosario.py` — no editar a mano: reejecutar el
script si cambia la curación. Fuente:

    Zavala Reyes, Miguel Enrique (2015). "Palabras vivas de una lengua
    muerta: legado arawak-caquetío". Boletín Antropológico 33(89), pp. 58-76.
    Universidad de Los Andes. → fuentes_caquetios/

MOTIVO (auditoría 2026-07-20): el lexicón contenía solo ~66 de las 288
entradas del glosario (23%). Faltaban palabras que el propio proyecto usa
como nombre de agente (buio, bagre, cunaro, guaranaro, dara, naure) — que
por tanto NO puntuaban como caquetío — y ocho afijos atestiguados ausentes
de las reglas morfológicas.

CIERRE DEL PARSEO (F7, 2026-08-03): el glosario tiene 288 entradas numeradas
y hoy se parsean las 288. Antes se perdían la #31 (separa siglas y definición
con punto) y la #104 (variante del lema entre paréntesis), y nueve
definiciones venían mutiladas por el número de página o por versales
partidas por pypdf. Ver RESCATES_PARSEO en el minador.

D7 — GLOSA HISTÓRICA vs. IDENTIFICACIÓN MODERNA (decidido el 2026-08-03):
cada entrada lleva `glosa_fuente` con el texto VERBATIM de Zavala, su número
y las siglas del compilador. Esa es la glosa que el agente habla. Cuando la
ciencia moderna identifica otra cosa, se añade `identificacion_moderna` como
nota auditable; ninguna de las dos desplaza a la otra.

D5 FASE 2 — LEMA FONÉMICO (decidida 2026-08-30/F2-#36; aplicada al generado
el 2026-08-31): el vocabulario activo entra con su lema en grafía fonémica
(gua/gü→w, gue/gui→g dura, qu→k, c→k salvo ch y ce/ci, z→s, v→b) y conserva
la grafía de Zavala en `forma_fuente`. Los homógrafos cuya colisión con el
español era de la grafía colonial quedan DISUELTOS (ver
HOMOGRAFOS_DISUELTOS_D5); las colisiones de lema NO se renombran y esperan
decisión (ver COLISIONES_D5). Topónimos y antropónimos siguen en grafía
fuente por D5a. Mapa del literal: 6-fusion/migracion_lemas_fase2.yaml.

CAVEAT DE MÉTODO: el glosario de Zavala es una compilación de nueve autores
(Arcaya, Hernández Baño, Esteves, Angulo Molina, Alvarado, Galeotto Cey,
González Batista, Arellano Moreno, Hill Peña). Algunos fitónimos y zoónimos
son voces indígenas de circulación pan-venezolana cuya atribución
*específicamente caquetía* es más débil que la de un `diao` o un `barsure`.
Cada entrada lleva en `notas` el número de glosario y las siglas del
compilador para que esa procedencia quede siempre auditable.

LA CLASE DE LA RAÍZ (2026-09-20): la parte de la oración ya no sale de una
heurística de tier. Cada entrada del vocabulario activo que caía en el cajón
de resto lleva su clase declarada —estativo / acción / nombre / adverbio—
con su apoyo comparativo y su cita, en CLASES_DE_RAIZ_ZAVALA. Importa porque
`cat` verbal alimenta `curiana_lexicon._RAICES_VERB` y con ella
`score_linguistico()`. Ver CLASE_DE_LA_RAIZ en el minador.

LA CLASE ESTATIVA (2026-09-21, d21.4): las diez raíces estativas se emiten
con `cat: v_estativo` y no con `v_raiz`. Es una etiqueta, no una morfología
nueva: `curiana_lexicon.CATS_VERBALES` la cuenta como verbal, así que toman
los mismos tres aspectos y no sale ni entra ninguna raíz de _RAICES_VERB.

EXCLUIDOS del habla (ver EXCLUIR_DEL_HABLA en el minador): topónimos
modernos, antropónimos, etnónimos y glosas circulares. Están abajo en
TOPONIMOS_ZAVALA / ANTROPONIMOS_ZAVALA como referencia de canon, y NO se
mezclan con el vocabulario activo.
"""


# ══════════════════════════════════════════════════════════════════
# T1 — AFIJOS ATESTIGUADOS (el hallazgo de mayor valor)
# ══════════════════════════════════════════════════════════════════
# Amplían lo que los agentes pueden CONSTRUIR, no solo nombrar. Se
# integran a las reglas morfológicas en curiana_lexicon.py.

AFIJOS_ZAVALA: dict[str, dict] = {
    "-aima": {"glosa": "desinencia de abundancia", "forma_glosario": "aima", "notas": "Zavala Reyes 2015 #6 (AM+PMA)"},
    "dito": {"glosa": "distintivo de nombres colectivos de abundancia", "forma_glosario": "dito", "notas": "Zavala Reyes 2015 #111 (E)"},
    "-ima": {"glosa": "desinencia: humedad, quebrada", "forma_glosario": "ima", "notas": "Zavala Reyes 2015 #165 (E+PMA)"},
    "-iro": {"glosa": "desinencia de diminutivo", "forma_glosario": "iro", "notas": "Zavala Reyes 2015 #166 (E)"},
    "toda": {"glosa": "desinencia", "forma_glosario": "toda", "notas": "Zavala Reyes 2015 #250 (AM)"},
    "-ubana": {"glosa": "desinencia", "forma_glosario": "ubana", "notas": "Zavala Reyes 2015 #265 (AM)"},
    "-uco": {"glosa": "sufijo: quebrada, cauce", "forma_glosario": "uco", "notas": "Zavala Reyes 2015 #268 (E)"},
    "-uru": {"glosa": "desinencia", "forma_glosario": "uru", "notas": "Zavala Reyes 2015 #274 (AM)"},
}


# ══════════════════════════════════════════════════════════════════
# T2-T4 — VOCABULARIO ACTIVO
# ══════════════════════════════════════════════════════════════════

GLOSARIO_ZAVALA: dict[str, dict] = {

    # ── T2 — palabras que el proyecto YA USA como nombre de agente ──
    # Sin estas entradas, cuando Bagre-ko decía 'bagre' o Buio-sha decía 'buio',
    # score_linguistico NO lo contaba como caquetío: la métrica sub-contaba.
    "bagre":         {"sig": "pez", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez [Zavala Reyes 2015 #21 (AM)]", "notas": "Zavala Reyes 2015 #21 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "buio":          {"sig": "serpiente, boa, diablo, dios del mal", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serpiente, boa, diablo, dios del mal [Zavala Reyes 2015 #48 (AM)]", "notas": "Zavala Reyes 2015 #48 (AM)"},
    "kuna":          {"sig": "pez del golfete de Coro", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Pez del golfete de Coro [Zavala Reyes 2015 #95 (E)]", "forma_fuente": "cuna", "notas": "Zavala Reyes 2015 #95 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#95 Cuna (E): Pez del golfete de Coro» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 33, 44 (verificado: imagen): Cunacho (p. 33): cuna, cunaro, pez lábrido que abunda en el Golfete; Iticuna (p. 44)."},
    "kunaro":        {"sig": "pez del golfete de Coro. Promicops Guasa", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Pez del golfete de Coro. Promicops Guasa [Zavala Reyes 2015 #96 (E)]", "forma_fuente": "cunaro", "identificacion_moderna": "Rhomboplites aurorubens (pargo cunaro, de altura) según SVDB. Zavala transcribe 'Promicops Guasa' (por Promicrops itajara, hoy Epinephelus itajara, el mero guasa): dos peces distintos.", "notas": "Zavala Reyes 2015 #96 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#96 Cunaro (E): Pez del golfete de Coro. Promicops Guasa» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 33 (verificado: imagen): Cunacho, p. 33, junto a cuna."},
    "dara":          {"sig": "alcaraván", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Alcaraván [Zavala Reyes 2015 #102 (HB+E)]", "notas": "Zavala Reyes 2015 #102 (HB+E)"},
    "waranaro":      {"sig": "pez lisa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez lisa [Zavala Reyes 2015 #139 (HB+E)]", "forma_fuente": "guaranaro", "identificacion_moderna": "sin resolver; 'lisa' apunta a Mugil spp. (M. curema / M. incilis son las del Golfete). La hoja de fuentes 02_ecologia lo daba por 'sin identificación taxonómica firme' cuando Zavala YA lo glosaba.", "notas": "Zavala Reyes 2015 #139 (HB+E)"},
    "naure":         {"sig": "jojoto", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Jojoto [Zavala Reyes 2015 #185 (E)]", "notas": "Zavala Reyes 2015 #185 (E)"},
    "naure":         {"sig": "planta bejucosa", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Planta bejucosa [Zavala Reyes 2015 #186 (E)]", "notas": "Zavala Reyes 2015 #186 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#186 Ñaure (E): Planta bejucosa» la (E) es Esteves 1989, y es su única fuente: es un «en caquetío X es Y» que no dice de dónde sale, y ninguna otra obra lo corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves p. 37 (verificado: imagen): Chunaure, p. 37: Chunaure es apellido; «en lengua caquetía 'ñaure' es planta bejucosa, y 'naure', es jojoto»."},

    # ── T3 — sustantivos concretos: fauna, flora, paisaje, técnica ──
    # Varios cierran 'huecos léxicos' que ecologia_lexicon_map.md daba por vacíos
    # (taques=salina, bisure=lagartija, chaguanco=zorro, jachos=teas de pesca).
    "ako":           {"sig": "comida. Par, casal, pareja", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Comida. Par, casal, pareja [Zavala Reyes 2015 #4 (E+AM)]", "forma_fuente": "aco", "notas": "Zavala Reyes 2015 #4 (E+AM); variantes: aca"},
    "arata":         {"sig": "mono", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mono [Zavala Reyes 2015 #13 (AM)]", "notas": "Zavala Reyes 2015 #13 (AM)"},
    "arika":         {"sig": "árbol de jícara o totumo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de jícara o totumo [Zavala Reyes 2015 #14 (AM)]", "forma_fuente": "arica", "notas": "Zavala Reyes 2015 #14 (AM)"},
    "bakoa":         {"sig": "bosque, lugar, paraje, sitio fértil", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bosque, lugar, paraje, sitio fértil [Zavala Reyes 2015 #18 (AM+E)]", "forma_fuente": "bacoa", "notas": "Zavala Reyes 2015 #18 (AM+E)"},
    "bajareke":      {"sig": "tabico hecho de tierra palos y bejuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tabico hecho de tierra palos y bejuco [Zavala Reyes 2015 #24 (AM)]", "forma_fuente": "bajareque", "notas": "Zavala Reyes 2015 #24 (AM); T4 de la tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»): pareja en la ESFERA — taíno «bajareque» 'bohío grande' (Brinton p. 11; Goeje 1939 p. 10; Coll y Toste 1897 p. 191), de la tradición viva: la técnica de construcción, con la palabra que la nombra. Comparanda de la esfera, no evidencia de préstamo ni de parentesco por sí sola; no cambia glosa ni capa. Propuesta: 6-fusion/taino_tradicion_viva_2026-09-24.yaml §el_cruce"},
    "barabara":      {"sig": "árbol de madera dura y pesada. Olivo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de madera dura y pesada. Olivo [Zavala Reyes 2015 #30 (A)]", "notas": "Zavala Reyes 2015 #30 (A)"},
    "barbasko":      {"sig": "hierba de borrachera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hierba de borrachera [Zavala Reyes 2015 #32 (HB)]", "forma_fuente": "barbasco", "notas": "Zavala Reyes 2015 #32 (HB)"},
    "bisure":        {"sig": "lagartija", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lagartija [Zavala Reyes 2015 #41 (HB+E)]", "notas": "Zavala Reyes 2015 #41 (HB+E)"},
    "buche":         {"sig": "planta xerofita, melocato, cardo globoso, rastrero", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta xerofita, melocato, cardo globoso, rastrero [Zavala Reyes 2015 #45 (AM+E)]", "notas": "Zavala Reyes 2015 #45 (AM+E); variantes: buchi"},
    "kabana":        {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #51 (HB)]", "forma_fuente": "cabana", "notas": "Zavala Reyes 2015 #51 (HB); T4 de la tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»): pareja en la ESFERA — taíno «sabana» 'llanura sin árboles' (Oviedo p. 146; Brinton p. 13), de cronista del XVI: la sabana entró al castellano con s y el caquetío la tiene con k; es una de las tres parejas k ~ s (kiba/siba, kabana/sabana, kiwa/sigua) que T11 dejó en «indecidible»: se vuelve a correr después de la corrida base (T5). Comparanda de la esfera, no evidencia de préstamo ni de parentesco por sí sola; no cambia glosa ni capa. Propuesta: 6-fusion/taino_tradicion_viva_2026-09-24.yaml §el_cruce"},
    "kakuro":        {"sig": "pequeña avispa negra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña avispa negra [Zavala Reyes 2015 #54 (E+A)]", "forma_fuente": "cacuro", "notas": "Zavala Reyes 2015 #54 (E+A)"},
    "kamaroa":       {"sig": "árbol lactescente, de hojas parecidas al papayo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol lactescente, de hojas parecidas al papayo [Zavala Reyes 2015 #56 (A)]", "forma_fuente": "camaroa", "notas": "Zavala Reyes 2015 #56 (A)"},
    "kapubana":      {"sig": "duende del cerro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende del cerro [Zavala Reyes 2015 #61 (HB)]", "forma_fuente": "capubana", "notas": "Zavala Reyes 2015 #61 (HB)"},
    "kaketillo":     {"sig": "árbol. Madera de construcción, resistente a la humedad", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol. Madera de construcción, resistente a la humedad [Zavala Reyes 2015 #63 (E+A)]", "forma_fuente": "caquetillo", "notas": "Zavala Reyes 2015 #63 (E+A)"},
    "karapa":        {"sig": "árbol resinoso", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol resinoso [Zavala Reyes 2015 #65 (E)]", "forma_fuente": "carapa", "notas": "Zavala Reyes 2015 #65 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#65 Carapa (E): Árbol resinoso» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 27, 98 (verificado: ocr): Cararapa (p. 27), «forma epentética de carapa, árbol resinoso»; Carapa (p. 98)."},
    "karuka":        {"sig": "paja, da consistencia al barro que se aplica a paredes y techos", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Paja, da consistencia al barro que se aplica a paredes y techos [Zavala Reyes 2015 #67 (E)]", "forma_fuente": "caruca", "notas": "Zavala Reyes 2015 #67 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#67 Caruca (E): Paja, da consistencia al barro que se aplica a paredes y techos» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 28, 49 (verificado: imagen): Caruca (p. 28): hierba áspera para la torta de barro de los techos; Machuruca (p. 49)."},
    "kaseto":        {"sig": "planta herbácea", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Planta herbácea [Zavala Reyes 2015 #68 (E)]", "forma_fuente": "caseto", "notas": "Zavala Reyes 2015 #68 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#68 Caseto (E): Planta herbácea» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 30 (verificado: ocr): Caseto (p. 30): planta herbácea de las malvas espigadas, Malvastrum spicatum."},
    "kaskito":       {"sig": "agrio, fermentado", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Agrio, fermentado [Zavala Reyes 2015 #69 (HB)]", "forma_fuente": "casquito", "notas": "Zavala Reyes 2015 #69 (HB)"},
    "kaujaro":       {"sig": "árbol de madera blanda, fruta mucilaginosa, del género cordia", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol de madera blanda, fruta mucilaginosa, del género cordia [Zavala Reyes 2015 #72 (E)]", "forma_fuente": "caujaro", "notas": "Zavala Reyes 2015 #72 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#72 Caujaro (E): Árbol de madera blanda, fruta mucilaginosa, del género cordia» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 30, 100 (verificado: ocr): Caujarito (p. 30), diminutivo de caujaro, Cordia; Caujaro (p. 100), la glosa de Zavala palabra por palabra."},
    "kayude":        {"sig": "árbol frutal, guanábano silvestre, turagua", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol frutal, guanábano silvestre, turagua [Zavala Reyes 2015 #73 (E)]", "forma_fuente": "cayude", "notas": "Zavala Reyes 2015 #73 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#73 Cayude (E): Árbol frutal, guanábano silvestre, turagua» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 30, 100 (verificado: imagen (p. 30 en esteves_paginas_releidas_2026-09-16.yaml)): Cayude (pp. 30 y 100): árbol anonáceo, turagua."},
    "cege":          {"sig": "lechuza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lechuza [Zavala Reyes 2015 #78 (HB)]", "forma_fuente": "cegue", "notas": "Zavala Reyes 2015 #78 (HB)"},
    "chawanko":      {"sig": "zorro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Zorro [Zavala Reyes 2015 #80 (A)]", "forma_fuente": "chaguanco", "notas": "Zavala Reyes 2015 #80 (A)"},
    "chaure":        {"sig": "cegue. Lechuza que anida en cuevas de terrenos arenosos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cegue. Lechuza que anida en cuevas de terrenos arenosos [Zavala Reyes 2015 #81 (HB+E)]", "notas": "Zavala Reyes 2015 #81 (HB+E)"},
    "chipare":       {"sig": "matapalo", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Matapalo [Zavala Reyes 2015 #82 (E)]", "notas": "Zavala Reyes 2015 #82 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#82 Chipare (E): Matapalo» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 108, 117 (verificado: ocr): Ipare (p. 117): «aféresis de chipare, matapalo». En Chipare (p. 108) no glosa."},
    "chirwa":        {"sig": "tinaja pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tinaja pequeña [Zavala Reyes 2015 #83 (HB)]", "forma_fuente": "chirgua", "notas": "Zavala Reyes 2015 #83 (HB)"},
    "kokuy":         {"sig": "penca. Planta rizomoza que da un vino agradable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Penca. Planta rizomoza que da un vino agradable [Zavala Reyes 2015 #87 (HB+CGB+A)]", "forma_fuente": "cocuy", "notas": "Zavala Reyes 2015 #87 (HB+CGB+A); era homógrafo del español en grafía fuente (cocuy) — la migración D5 disolvió la colisión"},
    "kurari":        {"sig": "árbol de roble, tecoma", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol de roble, tecoma [Zavala Reyes 2015 #97 (E)]", "forma_fuente": "curari", "notas": "Zavala Reyes 2015 #97 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#97 Curarí (E): Árbol de roble, tecoma» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 33, 35, 106 (verificado: imagen): Curaidebo (p. 35): «Curarí: árbol maderable, tecoma»; la madera de los jachos (p. 33)."},
    "dabuda":        {"sig": "barro loza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Barro loza [Zavala Reyes 2015 #99 (HB+E)]", "notas": "Zavala Reyes 2015 #99 (HB+E)"},
    "dakawa":        {"sig": "árbol de corteza gris, madera compacta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de corteza gris, madera compacta [Zavala Reyes 2015 #101 (A)]", "forma_fuente": "dacagua", "notas": "Zavala Reyes 2015 #101 (A)"},
    "darubana":      {"sig": "camino, vía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Camino, vía [Zavala Reyes 2015 #104 (AM)]", "notas": "Zavala Reyes 2015 #104 (AM); variantes: durabana"},
    "dato":          {"sig": "fruto del cardón", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fruto del cardón [Zavala Reyes 2015 #105 (HB)]", "notas": "Zavala Reyes 2015 #105 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "dipopo":        {"sig": "fibra de cocuiza, cabuya", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fibra de cocuiza, cabuya [Zavala Reyes 2015 #109 (AM)]", "notas": "Zavala Reyes 2015 #109 (AM)"},
    "ditero":        {"sig": "insecto, hormiga que daña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insecto, hormiga que daña [Zavala Reyes 2015 #110 (AM)]", "notas": "Zavala Reyes 2015 #110 (AM)"},
    "dibidibe":      {"sig": "árbol cuyo fruto es una baya que da tinta", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol cuyo fruto es una baya que da tinta [Zavala Reyes 2015 #112 (E)]", "forma_fuente": "dividive", "notas": "Zavala Reyes 2015 #112 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#112 Dividive (E): Árbol cuyo fruto es una baya que da tinta» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 23, 76, 110 (verificado: ocr): Bibidure (p. 23): dividive, árbol leguminoso tintóreo; Dividive (p. 110), la glosa de Zavala entera."},
    "ebo":           {"sig": "camino, paso, senda", "cat": "sust", "fuente": "caquetío-reconstruido", "glosa_fuente": "Camino, paso, senda [Zavala Reyes 2015 #117 (E)]", "notas": "Zavala Reyes 2015 #117 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-reconstruido`. 1-B. En «#117 Ebo (E): Camino, paso, senda» la (E) es Esteves 1989, y es su única fuente: es etimología suya, pero corrobora una forma que trae otra fuente y que partimos nosotros: reconstruida. Esteves pp. 35, 38, 39, 47, 105 (verificado: imagen): Curaidebo «el paso del Curarí… Ebo: camino, paso, senda» (p. 35), Gisebo (p. 38), Guacurebo «por el sufijo ebo» (p. 39), Jurijurebo «paso, ruta, valle estrecho, cañón» (p. 47) y Cumarebo (p. 105). Corrobora: zavala-reyes-2015 p. 66: #75 Cazebo (GC) «Poniente» = cazi (GC) «sol» + -ebo: «el camino del sol» es partición NUESTRA (campaña del nominalizador, 2026-09-21)"},
    "waka":          {"sig": "ave, cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave, cotorra [Zavala Reyes 2015 #123 (E)]", "forma_fuente": "guaca", "notas": "Zavala Reyes 2015 #123 (E); era homógrafo del español en grafía fuente (guaca) — la migración D5 disolvió la colisión"},
    "wache":         {"sig": "murciélago, zorro blanco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Murciélago, zorro blanco [Zavala Reyes 2015 #125 (E+AM)]", "forma_fuente": "guache", "notas": "Zavala Reyes 2015 #125 (E+AM)"},
    "wako":          {"sig": "planta herbácea de la familia de las portulacea", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Planta herbácea de la familia de las portulacea [Zavala Reyes 2015 #126 (E)]", "forma_fuente": "guaco", "notas": "Zavala Reyes 2015 #126 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#126 Guaco (E): Planta herbácea de la familia de las portulacea» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 14, 38 (verificado: ocr): Aguaque (p. 14): viene de guaco, portulácea, pasto codiciado por las cabras.; T4 de la tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»): pareja en la ESFERA — taíno «guaco» 'planta medicinal' (Coll y Toste 1897 p. 218), de la tradición viva: planta de uso en las dos orillas. Comparanda de la esfera, no evidencia de préstamo ni de parentesco por sí sola; no cambia glosa ni capa. Propuesta: 6-fusion/taino_tradicion_viva_2026-09-24.yaml §el_cruce"},
    "wakoa":         {"sig": "paloma", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paloma [Zavala Reyes 2015 #127 (HB)]", "forma_fuente": "guacoa", "notas": "Zavala Reyes 2015 #127 (HB)"},
    "wakuaro":       {"sig": "palo de tinte", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palo de tinte [Zavala Reyes 2015 #128 (A+AM)]", "forma_fuente": "guacuaro", "notas": "Zavala Reyes 2015 #128 (A+AM)"},
    "wairon":        {"sig": "hoguera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hoguera [Zavala Reyes 2015 #132 (HB)]", "forma_fuente": "guairon", "notas": "Zavala Reyes 2015 #132 (HB)"},
    "wamacho":       {"sig": "árbol cactáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol cactáceo [Zavala Reyes 2015 #134 (A+E)]", "forma_fuente": "guamacho", "notas": "Zavala Reyes 2015 #134 (A+E)"},
    "warataro":      {"sig": "barro de loza, para la fábrica de budares y ollas", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Barro de loza, para la fábrica de budares y ollas [Zavala Reyes 2015 #141 (E)]", "forma_fuente": "guarataro", "notas": "Zavala Reyes 2015 #141 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#141 Guarataro (E): Barro de loza, para la fábrica de budares y ollas» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 41 (verificado: imagen): Guarataro (p. 41): barro de loza gomoso para budares y ollas; abunda en el lugar."},
    "wariana":       {"sig": "arbusto halófilo, frailejón de la playa. Tabaco pescador", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Arbusto halófilo, frailejón de la playa. Tabaco pescador [Zavala Reyes 2015 #142 (E)]", "forma_fuente": "guariana", "notas": "Zavala Reyes 2015 #142 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#142 Guariana (E): Arbusto halófilo, frailejón de la playa. Tabaco pescador» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 28 (verificado: imagen): Cariguariana (p. 28): guariana, arbusto halófilo, «tabaco pescador»."},
    "waru":          {"sig": "volturido, cataneja. Ave mayor que el zamuro", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Volturido, cataneja. Ave mayor que el zamuro [Zavala Reyes 2015 #143 (E)]", "forma_fuente": "guaru", "notas": "Zavala Reyes 2015 #143 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#143 Guaru (E): Volturido, cataneja. Ave mayor que el zamuro» la (E) es Esteves 1989, y es su única fuente: es un «en caquetío X es Y» que no dice de dónde sale, y ninguna otra obra lo corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves p. 42 (verificado: imagen (esteves_paginas_releidas_2026-09-16.yaml; la p. 42 está escaneada boca abajo)): Guaruguaja, p. 42: «Guar[a], en caquetío, es el voltúrido que llamamos cunareja, ave mayor que el zamuro». La saca del topónimo, que él lee como plural por duplicación (guaraguara)."},
    "way":           {"sig": "árbol parecido a la ceiba", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol parecido a la ceiba [Zavala Reyes 2015 #147 (E+A)]", "forma_fuente": "guay", "notas": "Zavala Reyes 2015 #147 (E+A); era homógrafo del español en grafía fuente (guay) — la migración D5 disolvió la colisión"},
    "harifuche":     {"sig": "maíz tostado y miel", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maíz tostado y miel [Zavala Reyes 2015 #153 (HB)]", "notas": "Zavala Reyes 2015 #153 (HB)"},
    "huaymujo":      {"sig": "pequeño cangrejo", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Pequeño cangrejo [Zavala Reyes 2015 #158 (E)]", "notas": "Zavala Reyes 2015 #158 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#158 Huaymujo (E): Pequeño cangrejo» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 43 (verificado: ocr): Imujo (p. 43): aféresis de huaymujo, pequeño cangrejo."},
    "humohumo":      {"sig": "el ave que vuela", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "El ave que vuela [Zavala Reyes 2015 #160 (AM)]", "notas": "Zavala Reyes 2015 #160 (AM)"},
    "igi":           {"sig": "árbol, matapalo, paují", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol, matapalo, paují [Zavala Reyes 2015 #164 (E)]", "forma_fuente": "igui", "notas": "Zavala Reyes 2015 #164 (E)"},
    "isiro":         {"sig": "árbol corpulento sapindáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol corpulento sapindáceo [Zavala Reyes 2015 #167 (A)]", "notas": "Zavala Reyes 2015 #167 (A)"},
    "jachos":        {"sig": "teas de madera, para encandilar en las labores de pesca nocturna", "cat": "sust", "fuente": "español-colonial", "glosa_fuente": "Teas de madera, para encandilar en las labores de pesca nocturna [Zavala Reyes 2015 #169 (E)]", "notas": "Zavala Reyes 2015 #169 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `español-colonial`. 6-a: «jacho» es el castellano «hacho» con la h aspirada. DLE (dle.rae.es, consultado el 2026-09-23), s.v. hacho¹, de hacha¹ 'vela': 'manojo de paja o esparto encendido para alumbrar' y 'leño resinoso […] usado para alumbrar'. Reasignada a español como `caraota` en D10. Esteves p. 33 (verificado: imagen): Cunacho, p. 33: del cunaro «extraían manteca para untar los 'jachos', teas de madera… para encandilar en labores de pesca nocturna». La palabra va ENTRE COMILLAS y Esteves no la da por indígena. Con 1-B habría quedado hipotética; la 6-a, verificada, la saca del caquetío"},
    "jajato":        {"sig": "chloris Radiata. Yerba forrajera. Lugar de arena", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Chloris Radiata. Yerba forrajera. Lugar de arena [Zavala Reyes 2015 #176 (A+AM)]", "notas": "Zavala Reyes 2015 #176 (A+AM)"},
    "judereke":      {"sig": "árbol ramoso, parecido al chiguare", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol ramoso, parecido al chiguare [Zavala Reyes 2015 #177 (E)]", "forma_fuente": "judereque", "notas": "Zavala Reyes 2015 #177 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#177 Judereque (E): Árbol ramoso, parecido al chiguare» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 47 (verificado: imagen): Juderecal (p. 47): colectivo de judereque, árbol ramoso parecido al chiguare."},
    "jusual":        {"sig": "sembrar, siembra, sembradío. Conuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sembrar, siembra, sembradío. Conuco [Zavala Reyes 2015 #180 (AM)]", "notas": "Zavala Reyes 2015 #180 (AM)"},
    "koro":          {"sig": "cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cotorra [Zavala Reyes 2015 #181 (HB)]", "notas": "Zavala Reyes 2015 #181 (HB)"},
    "parawa":        {"sig": "mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mar [Zavala Reyes 2015 #191 (GC)]", "forma_fuente": "paragua", "notas": "Zavala Reyes 2015 #191 (GC)"},
    "parawatan":     {"sig": "árbol maderable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol maderable [Zavala Reyes 2015 #193 (AM)]", "forma_fuente": "paraguatan", "notas": "Zavala Reyes 2015 #193 (AM)"},
    "piritu":        {"sig": "palmera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palmera [Zavala Reyes 2015 #199 (E+A+AM)]", "notas": "Zavala Reyes 2015 #199 (E+A+AM)"},
    "kerekere":      {"sig": "ave pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave pequeña [Zavala Reyes 2015 #202 (AM)]", "forma_fuente": "querequere", "notas": "Zavala Reyes 2015 #202 (AM)"},
    "kikuidi":       {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #211 (HB)]", "forma_fuente": "quicuidi", "notas": "Zavala Reyes 2015 #211 (HB)"},
    "kiwa":          {"sig": "concha de almeja y otros moluscos. Sitio del estado Lara", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Concha de almeja y otros moluscos. Sitio del estado Lara [Zavala Reyes 2015 #214 (E+AM)]", "forma_fuente": "quigua", "notas": "Zavala Reyes 2015 #214 (E+AM); T4 de la tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»): pareja en la ESFERA — taíno «sigua» 'caracolillo de costa' (Coll y Toste 1897 pp. 252, 158), de la tradición viva; es una de las tres parejas k ~ s (kiba/siba, kabana/sabana, kiwa/sigua) que T11 dejó en «indecidible»: se vuelve a correr después de la corrida base (T5). Comparanda de la esfera, no evidencia de préstamo ni de parentesco por sí sola; no cambia glosa ni capa. Propuesta: 6-fusion/taino_tradicion_viva_2026-09-24.yaml §el_cruce"},
    "ruba":          {"sig": "especie de abeja silvestre negra de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de abeja silvestre negra de Coro [Zavala Reyes 2015 #221 (A)]", "notas": "Zavala Reyes 2015 #221 (A)"},
    "samuro":        {"sig": "punta hacia el mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta hacia el mar [Zavala Reyes 2015 #223 (AM)]", "notas": "Zavala Reyes 2015 #223 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "sibidiwa":      {"sig": "arbusto euforbiaceo. Jatrofa Gossy Pifolia", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arbusto euforbiaceo. Jatrofa Gossy Pifolia [Zavala Reyes 2015 #226 (E+A)]", "forma_fuente": "sibidigua", "notas": "Zavala Reyes 2015 #226 (E+A)"},
    "supi":          {"sig": "sitio a orilla del mar. Arena. Arboleda supide", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio a orilla del mar. Arena. Arboleda supide [Zavala Reyes 2015 #230 (AM+PMA)]", "notas": "Zavala Reyes 2015 #230 (AM+PMA)"},
    "taboro":        {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #233 (HB)]", "notas": "Zavala Reyes 2015 #233 (HB)"},
    "take":          {"sig": "árbol nucífero", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol nucífero [Zavala Reyes 2015 #236 (E)]", "forma_fuente": "taque", "notas": "Zavala Reyes 2015 #236 (E); era homógrafo del español en grafía fuente (taque) — la migración D5 disolvió la colisión; CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#236 Taque (E): Árbol nucífero» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 61, 132 (verificado: ocr): Tacal y Tacaduto (p. 61): taque, árbol nucífero."},
    "takes":         {"sig": "salina", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Salina [Zavala Reyes 2015 #237 (AM)]", "forma_fuente": "taques", "notas": "Zavala Reyes 2015 #237 (AM); era homógrafo del español en grafía fuente (taques) — la migración D5 disolvió la colisión"},
    "taratore":      {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #241 (AM)]", "notas": "Zavala Reyes 2015 #241 (AM)"},
    "tauta":         {"sig": "pequeña paloma de hábitos ictiófagos", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Pequeña paloma de hábitos ictiófagos [Zavala Reyes 2015 #244 (E)]", "notas": "Zavala Reyes 2015 #244 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#244 Tauta (E): Pequeña paloma de hábitos ictiófagos» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 62 (verificado: ocr): Tausabana (p. 62): tauta, palomita de hábitos ictiófagos que baja en bandadas a las albuferas."},
    "tiwa":          {"sig": "árbol rutáceo", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Árbol rutáceo [Zavala Reyes 2015 #246 (E)]", "forma_fuente": "tigua", "notas": "Zavala Reyes 2015 #246 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#246 Tigua (E): Árbol rutáceo» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 63, 134 (verificado: ocr): Tiguadare (p. 63): tigua, árbol rutáceo."},
    "tigi":          {"sig": "pequeña paloma que se alimenta de peces", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Pequeña paloma que se alimenta de peces [Zavala Reyes 2015 #247 (E)]", "forma_fuente": "tigui", "notas": "Zavala Reyes 2015 #247 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#247 Tigüí (E): Pequeña paloma que se alimenta de peces» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 63 (verificado: ocr): Ticuí (p. 63): «Tigüí y no Ticuí» es una palomita que se alimenta de peces."},
    "tijua":         {"sig": "paloma de canto onomatopéyico", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Paloma de canto onomatopéyico [Zavala Reyes 2015 #248 (E)]", "notas": "Zavala Reyes 2015 #248 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#248 Tijúa (E): Paloma de canto onomatopéyico» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves pp. 38, 63 (verificado: ocr): Tijuro (p. 63): «se nos ha informado» que viene de tijua, paloma de canto onomatopéyico, con una copla."},
    "tomatei":       {"sig": "punta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta [Zavala Reyes 2015 #252 (AM)]", "notas": "Zavala Reyes 2015 #252 (AM)"},
    "tubarao":       {"sig": "arenales", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Arenales [Zavala Reyes 2015 #254 (E)]", "notas": "Zavala Reyes 2015 #254 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#254 Tubarao (E): Arenales» la (E) es Esteves 1989, y es su única fuente: es la etimología de un topónimo, análisis suyo, y ninguna otra obra la corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves p. 64 (verificado: imagen): Tubarao, p. 64: «significa arenales. Tuba: montón. Rao: arena»."},
    "tupure":        {"sig": "siembra de cacao", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra de cacao [Zavala Reyes 2015 #256 (s/sigla)]", "notas": "Zavala Reyes 2015 #256 (s/sigla)"},
    "tukinemo":      {"sig": "llano, plano", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Llano, plano [Zavala Reyes 2015 #258 (AM)]", "forma_fuente": "tuquinemo", "notas": "Zavala Reyes 2015 #258 (AM)"},
    "turicha":       {"sig": "ave cantadora. Flauta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave cantadora. Flauta [Zavala Reyes 2015 #260 (AM)]", "notas": "Zavala Reyes 2015 #260 (AM)"},
    "turumako":      {"sig": "cerro de cima plana, meseta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cerro, meseta [Zavala Reyes 2015 #262 (AM)]", "forma_fuente": "turumaco", "notas": "Zavala Reyes 2015 #262 (AM); GLOSA CURADA (`sig`, no `glosa_fuente`): d21.16 (2026-09-21), punto 5: «cerro, meseta» emparejaba con `sima` 'cerro, montaña, elevación' y las dos se leían como la misma palabra. Por el criterio de la propia política d19.b NO son par —solapamiento parcial, no glosa idéntica— y Miguel: «me parece bien que convivan sima y turumako […] al final no pasa nada si hay símiles». Se afinan las dos para que dejen de emparejar: `turumako` es el cerro de cima plana, que es lo que 'meseta' añade en la propia fuente (zavala-reyes-2015 #262 AM), y `sima` la elevación a secas. La glosa de la fuente queda intacta en `glosa_fuente`"},
    "turupia":       {"sig": "árbol espinoso. Sitio en Cumarebo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol espinoso. Sitio en Cumarebo [Zavala Reyes 2015 #263 (AM+A)]", "notas": "Zavala Reyes 2015 #263 (AM+A)"},
    "tuturutos":     {"sig": "hierba de propiedades eméticas. Usado para cuajar quesos", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Hierba de propiedades eméticas. Usado para cuajar quesos [Zavala Reyes 2015 #264 (E)]", "notas": "Zavala Reyes 2015 #264 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#264 Tuturutos (E): Hierba de propiedades eméticas. Usado para cuajar quesos» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 66 (verificado: imagen): Tutubacoa (p. 66): «hemos obtenido dos informaciones»; tuturutos, hierba de savia emética que cuaja el queso."},
    "uria":          {"sig": "plantío, siembra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Plantío, siembra [Zavala Reyes 2015 #273 (AM)]", "notas": "Zavala Reyes 2015 #273 (AM)"},
    "yabo":          {"sig": "cercidium Virid. Arbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cercidium Virid. Arbol resinoso [Zavala Reyes 2015 #278 (E+A+AM)]", "notas": "Zavala Reyes 2015 #278 (E+A+AM)"},
    "yakure":        {"sig": "árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare [Zavala Reyes 2015 #281 (AM+E)]", "forma_fuente": "yacure", "notas": "Zavala Reyes 2015 #281 (AM+E)"},
    "yagruma":       {"sig": "caracol, molusco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caracol, molusco [Zavala Reyes 2015 #282 (A)]", "notas": "Zavala Reyes 2015 #282 (A)"},
    "yapamata":      {"sig": "siembra, plantío", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra, plantío [Zavala Reyes 2015 #283 (AM)]", "notas": "Zavala Reyes 2015 #283 (AM)"},
    "yaro":          {"sig": "bejuco. Planta venenosa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bejuco. Planta venenosa [Zavala Reyes 2015 #285 (AM)]", "notas": "Zavala Reyes 2015 #285 (AM)"},

    # ── T4 — verbos, cualidades y abstractos ──
    # El lexicón activo es pobre en verbos y cualidades; este tier lo compensa.
    "aka":           {"sig": "bejuco", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Bejuco [Zavala Reyes 2015 #3 (E)]", "forma_fuente": "aca", "notas": "Zavala Reyes 2015 #3 (E); era homógrafo del español en grafía fuente (aca) — la migración D5 disolvió la colisión; CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#3 Aca (E): Bejuco» la (E) es Esteves 1989, y es su única fuente: es la etimología de un topónimo, análisis suyo, y ninguna otra obra la corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves pp. 83, 105 (verificado: imagen): Sólo en la Parte II: Acaca, Acarite y Acatuto (p. 83: «Aca: bejuco; uto: quebrada»). En la p. 105 da «aca: par, casal, pareja»: la misma forma con dos glosas."},
    "apo":           {"sig": "grande", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Grande [Zavala Reyes 2015 #11 (AM)]", "notas": "Zavala Reyes 2015 #11 (AM)"},
    "bachure":       {"sig": "maneto, patituerto", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maneto, patituerto [Zavala Reyes 2015 #19 (A)]", "notas": "Zavala Reyes 2015 #19 (A)"},
    "badamaro":      {"sig": "extraer, sacar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Extraer, sacar [Zavala Reyes 2015 #20 (AM)]", "notas": "Zavala Reyes 2015 #20 (AM)"},
    "baharuko":      {"sig": "abuelo, viejo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Abuelo, viejo [Zavala Reyes 2015 #22 (AM)]", "forma_fuente": "baharuco", "notas": "Zavala Reyes 2015 #22 (AM)"},
    "baperon":       {"sig": "calabaza con cal", "cat": "sust", "fuente": "caribe-pemeno", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #27 (HB)]", "notas": "Zavala Reyes 2015 #27 (HB); CAPA CURADA [tf.0, 2026-09-23 (6-fusion/decisiones_tanda_final_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caribe-pemeno`. Oviedo y Valdés t. II lib. XXV caps. V y VI (Francisco Martín, el soldado de Alfínger que vivió como indio; verificado en imagen). p. 286: «la boca llena de hayo […] é su baperon: este es un calabaço en que traen los indios çierta manera de cal; para quitar la hambre, chupándola»; p. 294: «toda aquella tierra es poblada de indios pemenos». La marca «(Lengua de Venezuela.)» es del glosario del editor (t. IV, «Baperon y Baperoni»), no de Oviedo: la trampa de `datihao` (db.2). Es la fuente del BAPÓRON de Alvarado 1921 p. 20. Pemeno = caribe según el canon (3-mundo/etnias.yaml etnia-006, filiación inferida por Oliver 1989 pp. 226-228). Detalle en 6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml §poporo.pasajes.pp-7 y §visto_de_paso.vp-baperon"},
    "barbache":      {"sig": "iguana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Iguana [Zavala Reyes 2015 #33 (PMA)]", "notas": "Zavala Reyes 2015 #33 (PMA)"},
    "beceremikore":  {"sig": "dominar, triunfar, victoria", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Dominar, triunfar, victoria [Zavala Reyes 2015 #39 (AM)]", "forma_fuente": "beceremicore", "notas": "Zavala Reyes 2015 #39 (AM)"},
    "kachipo":       {"sig": "en voz vulgar, enojado, colérico", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "En voz vulgar, enojado, colérico [Zavala Reyes 2015 #53 (A)]", "forma_fuente": "cachipo", "notas": "Zavala Reyes 2015 #53 (A)"},
    "kana":          {"sig": "demonio", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio [Zavala Reyes 2015 #57 (HB)]", "forma_fuente": "cana", "notas": "Zavala Reyes 2015 #57 (HB); era homógrafo del español en grafía fuente (cana) — la migración D5 disolvió la colisión"},
    "kapo":          {"sig": "duende, ente sobrenatural", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende, ente sobrenatural [Zavala Reyes 2015 #59 (E)]", "forma_fuente": "capo", "notas": "Zavala Reyes 2015 #59 (E); era homógrafo del español en grafía fuente (capo) — la migración D5 disolvió la colisión"},
    "kapu":          {"sig": "demonio. Señala Galeotto Cey la pronunciación “cap”", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio. Señala Galeotto Cey la pronunciación “cap” [Zavala Reyes 2015 #60 (HB)]", "forma_fuente": "capu", "notas": "Zavala Reyes 2015 #60 (HB)"},
    "karama":        {"sig": "ramazón", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Ramazón [Zavala Reyes 2015 #64 (E)]", "forma_fuente": "carama", "notas": "Zavala Reyes 2015 #64 (E); era homógrafo del español en grafía fuente (carama) — la migración D5 disolvió la colisión; CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#64 Carama (E): Ramazón» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 98 (verificado: ocr): Caramabure (p. 98): raíz de las caramas, «raíz de la ramazón»."},
    "chuchube":      {"sig": "paraulata", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paraulata [Zavala Reyes 2015 #85 (HB)]", "notas": "Zavala Reyes 2015 #85 (HB)"},
    "komoho":        {"sig": "fruto del cardón de las tunas (higo de tuna)", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Higo [Zavala Reyes 2015 #88 (HB)]", "forma_fuente": "comoho", "notas": "Zavala Reyes 2015 #88 (HB); GLOSA CURADA (`sig`, no `glosa_fuente`): T2 de la tanda de las hermanas (2026-09-24, «Acepto todo lo recomendado»): SEGUNDA ATESTACIÓN, independiente de Zavala. Oviedo, Historia general, lib. VIII cap. XXVIII, pp. 313-315 (oviedo-y-valdes-1851; p. 313 vista en imagen, pdf 432): «De los cardos de las tunas é su fructa, la qual en la provinçia de Veneçuela en la Tierra-Firme se llama comoho», y en el mismo capítulo llama «higos» a esos frutos («comiendo çinco ó seys higos destos»); p. 315: «este comoho es mas sabroso mucho que las tunas». La glosa 'higo' de Zavala es la palabra del propio cronista y se precisa: el higo de tuna. «La qual» es la fruta, no la planta: la glosa no dice que el cardón se llame comoho. Propuesta: 6-fusion/taino_tradicion_viva_2026-09-24.yaml §komoho"},
    "despopo":       {"sig": "fuerza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fuerza [Zavala Reyes 2015 #107 (AM)]", "notas": "Zavala Reyes 2015 #107 (AM)"},
    "dichiba":       {"sig": "límite, línea", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Límite, línea [Zavala Reyes 2015 #108 (AM)]", "forma_fuente": "dichiva", "notas": "Zavala Reyes 2015 #108 (AM)"},
    "domaria":       {"sig": "enredarse, atormentar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Enredarse, atormentar [Zavala Reyes 2015 #114 (AM)]", "notas": "Zavala Reyes 2015 #114 (AM)"},
    "duriwa":        {"sig": "hacer trabajos cortos", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hacer trabajos cortos [Zavala Reyes 2015 #116 (AM)]", "forma_fuente": "durigua", "notas": "Zavala Reyes 2015 #116 (AM)"},
    "etamo":         {"sig": "feroz, feo, espanto", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Feroz, feo, espanto [Zavala Reyes 2015 #120 (AM)]", "notas": "Zavala Reyes 2015 #120 (AM)"},
    "waidima":       {"sig": "integro", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Integro [Zavala Reyes 2015 #131 (AM)]", "forma_fuente": "guaidima", "notas": "Zavala Reyes 2015 #131 (AM)"},
    "wamipa":        {"sig": "hueco, profundidad", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hueco, profundidad [Zavala Reyes 2015 #135 (AM)]", "forma_fuente": "guamipa", "notas": "Zavala Reyes 2015 #135 (AM)"},
    "warakaro":      {"sig": "tapirama silvestre", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Tapirama silvestre [Zavala Reyes 2015 #138 (E)]", "forma_fuente": "guaracaro", "notas": "Zavala Reyes 2015 #138 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#138 Guaracaro (E): Tapirama silvestre» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 114 (verificado: ocr): Guaracaro (p. 114): planta anual de grano alimenticio, tapirama silvestre."},
    "waranao":       {"sig": "salado, ácido", "cat": "v_estativo", "fuente": "caquetío-hipotético", "glosa_fuente": "Salado, ácido [Zavala Reyes 2015 #140 (E)]", "forma_fuente": "guaranao", "notas": "Zavala Reyes 2015 #140 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#140 Guaranao (E): Salado, ácido» la (E) es Esteves 1989, y es su única fuente: la glosa de Zavala NO está en la página de Esteves que la origina, y ninguna otra obra la da: hipotética. Esteves p. 41 (verificado: imagen): La entrada GUARANAO (p. 41) describe la salina de Punta Cardón, la fama de su sal para los ojos (citando a Hill Peña) y la Zona Franca. NO glosa la voz: no dice «salado» ni «ácido». La búsqueda en las dos partes del OCR da la voz sólo en esta página."},
    "wasima":        {"sig": "viejo, anciano", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Viejo, anciano [Zavala Reyes 2015 #145 (AM)]", "forma_fuente": "guasima", "notas": "Zavala Reyes 2015 #145 (AM)"},
    "gika":          {"sig": "yabo", "cat": "sust", "fuente": "caquetío-retroabstraido", "glosa_fuente": "Yabo [Zavala Reyes 2015 #150 (E)]", "forma_fuente": "guica", "notas": "Zavala Reyes 2015 #150 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-retroabstraido`. 1-B. En «#150 Güica (E): Yabo» la (E) es Esteves 1989, y es su única fuente: Esteves nombra una voz VIVA de la península: la palabra existe (un nombre vivo es dato); lo que es suyo, y de Zavala al copiarlo, es que sea caquetía. Retroabstraída, como chiriware y tukeke (2026-09-10). Esteves p. 43 (verificado: imagen (lote del 2026-09-22)): Güica (p. 43): «otro nombre indígena» del árbol que llaman yabo."},
    "gide":          {"sig": "arreglar, acomodar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arreglar, acomodar [Zavala Reyes 2015 #151 (AM)]", "forma_fuente": "guide", "notas": "Zavala Reyes 2015 #151 (AM)"},
    "hueke":         {"sig": "sitio de trabajo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio de trabajo [Zavala Reyes 2015 #155 (AM)]", "forma_fuente": "hueque", "notas": "Zavala Reyes 2015 #155 (AM)"},
    "ikoroata":      {"sig": "caraota", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caraota [Zavala Reyes 2015 #162 (HB)]", "forma_fuente": "icoroata", "notas": "Zavala Reyes 2015 #162 (HB)"},
    "jabal":         {"sig": "adquirir", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Adquirir [Zavala Reyes 2015 #168 (AM)]", "notas": "Zavala Reyes 2015 #168 (AM)"},
    "jadarayte":     {"sig": "recoger", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Recoger [Zavala Reyes 2015 #172 (AM)]", "notas": "Zavala Reyes 2015 #172 (AM)"},
    "juri":          {"sig": "viento, ventarrón", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Viento, ventarrón [Zavala Reyes 2015 #178 (E)]", "notas": "Zavala Reyes 2015 #178 (E); variantes: jura; CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#178 Juri (E): Viento, ventarrón» la (E) es Esteves 1989, y es su única fuente: es la etimología de un topónimo, análisis suyo, y ninguna otra obra la corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves pp. 47, 66 (verificado: imagen): Tres veces y las tres partiendo un topónimo: Judibana («Judi, juri: viento. Bana: sitio alto», p. 47), Jurijurebo («Juri: viento; Ebo: paso…», p. 47) y Tura, que en el censo de 1881 fue «Hato de Jura» («Jura, juri: ventarrón», p. 66). No cita a nadie."},
    "lawari":        {"sig": "acacia Espinoza, acacia. Lauadrí", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Acacia Espinoza, acacia. Lauadrí [Zavala Reyes 2015 #182 (E+A+PMA)]", "forma_fuente": "laguari", "notas": "Zavala Reyes 2015 #182 (E+A+PMA)"},
    "orumo":         {"sig": "urumu. Apamate. No confundir con el Myrciacucuo llata", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Urumu. Apamate. No confundir con el Myrciacucuo llata [Zavala Reyes 2015 #187 (A+PMA)]", "notas": "Zavala Reyes 2015 #187 (A+PMA)"},
    "patapati":      {"sig": "anegadizo", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Anegadizo [Zavala Reyes 2015 #198 (AM)]", "notas": "Zavala Reyes 2015 #198 (AM)"},
    "popoi":         {"sig": "ahí. Adverbio de lugar", "cat": "part", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ahí. Adverbio de lugar [Zavala Reyes 2015 #201 (AM)]", "notas": "Zavala Reyes 2015 #201 (AM)"},
    "kibakibi":      {"sig": "baquiano, conocedor", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Baquiano, conocedor [Zavala Reyes 2015 #205 (AM)]", "forma_fuente": "quibaquibi", "notas": "Zavala Reyes 2015 #205 (AM)"},
    "kiboata":       {"sig": "engañar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar [Zavala Reyes 2015 #206 (AM)]", "forma_fuente": "quiboata", "notas": "Zavala Reyes 2015 #206 (AM)"},
    "kidiboata":     {"sig": "engañar, engañado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar, engañado [Zavala Reyes 2015 #213 (AM)]", "forma_fuente": "quidiboata", "notas": "Zavala Reyes 2015 #213 (AM)"},
    "kiwawa":        {"sig": "especie de haba grande y blanca", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de haba grande y blanca [Zavala Reyes 2015 #215 (A)]", "forma_fuente": "quiguagua", "notas": "Zavala Reyes 2015 #215 (A)"},
    "kiricias":      {"sig": "sangre, sangrado", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sangre, sangrado [Zavala Reyes 2015 #217 (AM)]", "forma_fuente": "quiricias", "notas": "Zavala Reyes 2015 #217 (AM)"},
    "raporon":       {"sig": "calabaza con cal", "cat": "sust", "fuente": "caribe-pemeno", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #220 (HB)]", "notas": "Zavala Reyes 2015 #220 (HB); CAPA CURADA [tf.0, 2026-09-23 (6-fusion/decisiones_tanda_final_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caribe-pemeno`. Oviedo y Valdés t. II lib. XXV caps. V y VI, p. 294 (verificado en imagen), entre los pemenos del sur de la laguna de Maracaibo: «salió con sus armas de indio, que eran el arco y las flechas é dardos é su raporon é hayo […] y el baporon es el calabaço de la cal para quitar la hambre». Gemela de `baperon` en la misma página; el glosario del editor del t. IV la remite allí («Rapürün [Raporon]: Vide Baperon») con la marca «(Lengua de Venezuela.)», que no es de Oviedo: la trampa de `datihao` (db.2). Pemeno = caribe según el canon (3-mundo/etnias.yaml etnia-006). Detalle en 6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml §poporo.pasajes.pp-7 y §visto_de_paso.vp-baperon"},
    "sinwanguso":    {"sig": "insolente", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insolente [Zavala Reyes 2015 #229 (PMA)]", "forma_fuente": "singuanguso", "notas": "Zavala Reyes 2015 #229 (PMA)"},
    "surupa":        {"sig": "blatta orientalis. Cucaracha", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Blatta orientalis. Cucaracha [Zavala Reyes 2015 #231 (A)]", "notas": "Zavala Reyes 2015 #231 (A)"},
    "tuba":          {"sig": "aglomeración, montón", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Aglomeración, montón [Zavala Reyes 2015 #253 (E)]", "notas": "Zavala Reyes 2015 #253 (E); homógrafo con español — resuelto por contexto en score_linguistico; CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#253 Tuba (E): Aglomeración, montón» la (E) es Esteves 1989, y es su única fuente: es la etimología de un topónimo, análisis suyo, y ninguna otra obra la corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves pp. 64, 73 (verificado: imagen): p. 64: Todariquiba no significaría nada, pero «Tubariquiba» —la forma que él propone en lugar de la de Castellanos— sería 'pedregal': «Tuba: aglomeración. Quiba: pedruzco»; y Tubarao, «Tuba: montón». p. 73 (apéndice): el «cuar» cumanagoto de Caulín «tiene el mismo significado del tuba de los caquetíos»."},
    "ubeda":         {"sig": "acacia fétida. Mapurite, cují hediondo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Acacia fétida. Mapurite, cují hediondo [Zavala Reyes 2015 #266 (A)]", "notas": "Zavala Reyes 2015 #266 (A)"},
    "uray":          {"sig": "envoltura o vaina de las cerbatanas", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Envoltura o vaina de las cerbatanas [Zavala Reyes 2015 #271 (AM)]", "notas": "Zavala Reyes 2015 #271 (AM)"},
    "ure":           {"sig": "raíz", "cat": "sust", "fuente": "caquetío-hipotético", "glosa_fuente": "Raíz [Zavala Reyes 2015 #272 (E)]", "notas": "Zavala Reyes 2015 #272 (E); CAPA CURADA [cc.4 / tf.0, 2026-09-23: la sigla (E) de Zavala es Esteves 1989, opción B (6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml)]: era `caquetío-atestiguado`, pasa a `caquetío-hipotético`. 1-B. En «#272 Ure (E): Raíz» la (E) es Esteves 1989, y es su única fuente: es la etimología de un topónimo, análisis suyo, y ninguna otra obra la corrobora: hipotética, la regla que la ficha de Esteves ya tenía. Esteves pp. 11, 18, 22 (verificado: ocr): Abudure (p. 11: «ure… quiere decir: raíz en nuestra primitiva lengua», y que está en muchos topónimos de Paraguaná) y Babahuro (p. 18, 'el caño de las raíces'). En la p. 22, a propósito de Baraivere, trae el único paralelo que da en todo el libro: el pueblo GUARANÍ «Uretebere» de Cabeza de Vaca, «Ure: raíz; Bere: amargo». En Parte II lo repite en Camurujure (p. 94) y Guaimure (p. 112)."},
    "usera":         {"sig": "seco, arenoso", "cat": "v_estativo", "fuente": "caquetío-atestiguado", "glosa_fuente": "Seco, arenoso [Zavala Reyes 2015 #275 (AM)]", "notas": "Zavala Reyes 2015 #275 (AM)"},
}


# ══════════════════════════════════════════════════════════════════
# LA CLASE DE LA RAÍZ — por qué cada `cat` es la que es
# ══════════════════════════════════════════════════════════════════
# Hasta el 2026-09-20 la parte de la oración salía de UNA heurística de
# tier (`_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}`), y el T4 es el
# cajón de resto del minador: de ahí salieron 49 `cat: v_raiz`, que es
# de donde `curiana_lexicon._RAICES_VERB` deja que `score_linguistico()`
# cuente como arahuaco cualquier token cuyo primer segmento sea una de
# ellas. Ahora cada una lleva su clase declarada con su apoyo y su cita
# (regla 8), y las que no tienen cognado lo dicen: `deuda: sin-procedencia`.
#
# Las clases son tres y media:
#   estativo → concepto adjetival que en arahuaco es VERBO (4ª conj.
#              lokono, Perea y Alonso 1942 pp. 634-639) → cat v_estativo
#   accion   → verbo pleno                              → cat v_raiz
#   nombre   → sustantivo concreto o abstracto          → cat sust
#   adverbio → deíctico de lugar (la clase de `yama`)   → cat part
#
# `v_estativo` es de la tanda del 2026-09-21 (d21.4): la clase se declara
# en la CATEGORÍA y llega al prompt, sin importar el alineamiento pospuesto
# del lokono. `curiana_lexicon.CATS_VERBALES` la cuenta como verbal, igual
# que `v_raiz`: un estado se predica con aspecto como una acción.
#
# La declaración de qué es un estativo EN ESTE PROYECTO está propuesta
# en 6-fusion/clases_de_raiz_zavala_2026-09-20.yaml, para 2-lengua/
# morfologia.md. Aquí sólo vive el reparto.
CLASES_DE_RAIZ_ZAVALA: dict[str, dict] = {
    "aka": {"clase": "nombre", "cat": "sust", "num": 3, "forma_zavala": "aca",
        "por": "'Bejuco' es una planta. El propio lexicón ya trae `yaro` 'bejuco. Planta venenosa' y `naure` 'planta bejucosa' como sust, las dos de zavala-reyes-2015; achagua `acua` 'sarmiento, bejuco' (neira-ribero-1762)."},
    "apo": {"clase": "estativo", "cat": "v_estativo", "num": 11, "forma_zavala": "apo",
        "por": "'Grande' es tamaño, y los tamaños son la 4ª conjugación estativa del lokono (perea-alonso-1942, pp. 634-639). El propio lexicón ya trae el lokono `ipi-lli-be` 'ser grande' como v_raiz. La achagua verbaliza y nominaliza la misma raíz: `numanudau` 'engrandecer', `manucaicasi` 'grandeza' (neira-ribero-1762)."},
    "bachure": {"clase": "estativo", "cat": "v_estativo", "num": 19, "forma_zavala": "bachure",
        "por": "'Maneto, patituerto' es defecto corporal, y el lokono lo dice con verbo estativo: `hiccu-li` 'ser cojo' (perea-alonso-1942), ya en el lexicón como v_raiz."},
    "badamaro": {"clase": "accion", "cat": "v_raiz", "num": 20, "forma_zavala": "badamaro",
        "por": "'Extraer, sacar', dos infinitivos transitivos. Lokono `lluccu-waria` 'sacar' (perea-alonso-1942). La achagua los marca con el pronombre PREFIJADO nu-, que es la marca del transitivo (perea-alonso-1942 p. 635): `numunuayu` 'sacar una espina', `nusiguiayu` 'sacar estrujando' (neira-ribero-1762)."},
    "baharuko": {"clase": "nombre", "cat": "sust", "num": 22, "forma_zavala": "baharuco",
        "por": "'Abuelo, viejo': término de parentesco, y el parentesco arahuaco es nombre poseído — achagua `abi` 'abuelo' (neira-ribero-1762), wayuu `atuushi` 'abuelo' y `taata` 'papá, abuelo'. DUDOSO declarado: la segunda acepción ('viejo') sí es estativa, y el par con `guasima` #145 lo enseña; manda la primera, y en duda se degrada (regla 2)."},
    "baperon": {"clase": "nombre", "cat": "sust", "num": 27, "forma_zavala": "baperon",
        "por": "'Calabaza con cal': el recipiente del chimó, un objeto. Achagua `cuirro` 'calabaza, uyama' (neira-ribero-1762); wayuu `aliita` 'totuma', `wüirü` 'auyama'. Gemela de #220 `raporon`."},
    "barbache": {"clase": "nombre", "cat": "sust", "num": 33, "forma_zavala": "barbache",
        "por": "'Iguana', zoónimo. El lexicón ya trae `iwana` y `higuana` (taíno, vía brinton-1871) e `iwana-kalinago`, las tres como sust. deuda: sin-procedencia para el lado caquetío — `barbache` no tiene cognado hermano; el apoyo es la glosa (zavala-reyes-2015 #33)."},
    "beceremikore": {"clase": "accion", "cat": "v_raiz", "num": 39, "forma_zavala": "beceremicore",
        "por": "'Dominar, triunfar, victoria': dos infinitivos y su nombre de acción, que el lokono forma con -hù/-hi sobre el verbo (perea-alonso-1942 p. 612). Achagua `nunisau` 'vencer, concluir' (neira-ribero-1762). DUDOSO declarado por la glosa mixta."},
    "kachipo": {"clase": "estativo", "cat": "v_estativo", "num": 53, "forma_zavala": "cachipo",
        "por": "'Enojado, colérico' es estado. La achagua lo conjuga sobre una raíz `cabare-` con el atributivo ca-/ka-: `cabareuno` 'enojarse', `cabarecayi` 'colérico', `cabareumí` 'es bravo' (neira-ribero-1762). Wayuu `aashichijawaa` 'enojarse'."},
    "kana": {"clase": "nombre", "cat": "sust", "num": 57, "forma_zavala": "cana",
        "por": "'Demonio', ser sobrenatural. Achagua `tanasimi` 'demonio, diablo' (neira-ribero-1762); wayuu `yolujaa` 'diablo, demonio'."},
    "kapo": {"clase": "nombre", "cat": "sust", "num": 59, "forma_zavala": "capo",
        "por": "'Duende, ente sobrenatural'. Achagua `guabaimi` 'duende' (neira-ribero-1762). Y el apoyo interno es fuerte: el compuesto ATESTIGUADO `capubana` 'duende del cerro' (zavala-reyes-2015 #61) ya es `sust` en el lexicón, y D9 lo usó como uno de los seis apoyos de `-bana` 'cerro'. La base de un compuesto nominal atestiguado no es raíz verbal."},
    "kapu": {"clase": "nombre", "cat": "sust", "num": 60, "forma_zavala": "capu",
        "por": "'Demonio'. Misma familia que #59 `capo` y misma base de `capubana` (zavala-reyes-2015 #60/#61; D9, morfologia.md §3). El lazo referencial del cerro de Santa Ana, que se llamó Cerro de Capú (velasco-2015-resistencia), es de un NOMBRE, no de un verbo."},
    "karama": {"clase": "nombre", "cat": "sust", "num": 64, "forma_zavala": "carama",
        "por": "'Ramazón', colectivo de ramas. Achagua `rinacay` 'rama' (neira-ribero-1762)."},
    "chuchube": {"clase": "nombre", "cat": "sust", "num": 85, "forma_zavala": "chuchube",
        "por": "'Paraulata', ornitónimo. Es una de las nueve reduplicaciones léxicas que F11 midió, y 5 de ellas son aves (morfologia.md §4, gatschet-1885): formación léxica de zoónimo, no morfología viva. Su gemela `chuchubi` ya es `sust` en el lexicón."},
    "komoho": {"clase": "nombre", "cat": "sust", "num": 88, "forma_zavala": "comoho",
        "por": "'Higo': el fruto, un nombre. deuda: sin-procedencia para el cognado — el apoyo es la glosa de la fuente (zavala-reyes-2015 #88)."},
    "despopo": {"clase": "nombre", "cat": "sust", "num": 107, "forma_zavala": "despopo",
        "por": "'Fuerza', nombre abstracto. En las tres comparandas del lexicón el concepto es nombre: wayuu `atsüin` 'fuerza', lokono `ansi` 'fuerza vital', y el propio caquetío `barsure` 'alma, esencia vital, fuerza interior' (sust, atestiguado: Angulo Molina vía zavala-reyes-2015). DUDOSO declarado: el wayuu tiene además `matsüinwaa` 'estar sin fuerza', que es el privativo ma- sobre la misma raíz y prueba que la raíz SE PREDICA; pero lo que Zavala glosa es el nombre, y en duda se degrada (regla 2)."},
    "dichiba": {"clase": "nombre", "cat": "sust", "num": 108, "forma_zavala": "dichiva",
        "por": "'Límite, línea'. La achagua distingue las dos cosas: el lindero es NOMBRE —`rijubana` 'linde', `ypubana` 'coto, lindero'— y para predicarlo usa otro verbo, `nuyedau rijubanã` 'terminar, poner lindero' (neira-ribero-1762). 63 usos raíz+aspecto en la base."},
    "domaria": {"clase": "accion", "cat": "v_raiz", "num": 114, "forma_zavala": "domaria",
        "por": "'Enredarse, atormentar'. El primero es reflexivo/medio, que en lokono es una conjugación entera —la 3ª, en -n-nua (perea-alonso-1942 p. 629)—, y sólo un verbo puede tener voz media."},
    "duriwa": {"clase": "accion", "cat": "v_raiz", "num": 116, "forma_zavala": "durigua",
        "por": "'Hacer trabajos cortos': la glosa ES una perífrasis verbal. Lokono `k-eme-kebbù` 'trabajar' (perea-alonso-1942 p. 648, keme-kebbu-n 'estar atareado'), ya en el lexicón como v_raiz."},
    "etamo": {"clase": "estativo", "cat": "v_estativo", "num": 120, "forma_zavala": "etamo",
        "por": "'Feroz, feo' son cualidades (4ª conj. lokono, perea-alonso-1942 p. 634); 'espanto' es su nombre de acción, que el lokono forma con -hi/-hù sobre el mismo verbo (p. 612). La achagua hace el mismo par sobre una raíz: `carruicay` 'espanto' / `carrunatacayi` 'espantoso' (neira-ribero-1762). DUDOSO declarado: glosa mixta cualidad+nombre; se mantiene verbal porque dos de las tres acepciones lo son, y porque `etamo` es la voz que MANDA en el par 18 de la política atestiguado-manda (archivó `mülia`)."},
    "waidima": {"clase": "estativo", "cat": "v_estativo", "num": 131, "forma_zavala": "guaidima",
        "por": "'Integro' = 'entero'. El lexicón ya trae el wayuu `waneepiaa` 'ser entero, -ra; ser' — la glosa misma lo declara verbo. Achagua `jaubearuba` 'cabal, entero' (neira-ribero-1762)."},
    "wamipa": {"clase": "nombre", "cat": "sust", "num": 135, "forma_zavala": "guamipa",
        "por": "'Hueco, profundidad': la segunda acepción es nombre abstracto y la primera es nombre de objeto en la achagua, `caricuibai` 'hueco' (neira-ribero-1762). DUDOSO declarado: 'hueco' admite lectura adjetival; en duda se degrada (regla 2)."},
    "warakaro": {"clase": "nombre", "cat": "sust", "num": 138, "forma_zavala": "guaracaro",
        "por": "'Tapirama silvestre', fitónimo. El lexicón ya trae `tapirama` 'frijol de grano grande' como sust (retroabstraído de medina-colina-sxx)."},
    "waranao": {"clase": "estativo", "cat": "v_estativo", "num": 140, "forma_zavala": "guaranao",
        "por": "'Salado, ácido' son sabores, y los sabores son 4ª conjugación estativa en lokono (perea-alonso-1942 p. 634). El lexicón ya trae el wayuu `palawaa` 'ser salado, -da'."},
    "wasima": {"clase": "estativo", "cat": "v_estativo", "num": 145, "forma_zavala": "guasima",
        "por": "'Viejo, anciano'. El apoyo es literal: `hebbe-n` 'ser viejo' es UNO de los tres ejemplos con que Perea define la 4ª conjugación estativa (perea-alonso-1942 p. 634), y `hebbe` ya está en el lexicón como v_raiz 'ser viejo, anciano'. DUDOSO declarado: 'anciano' también puede leerse como nombre de edad (cf. `wanü` 'anciano, mayor', sust); manda el apoyo literal, que es de la misma glosa."},
    "gika": {"clase": "nombre", "cat": "sust", "num": 150, "forma_zavala": "guica",
        "por": "'Yabo', fitónimo (el árbol del cardonal). deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #150)."},
    "gide": {"clase": "accion", "cat": "v_raiz", "num": 151, "forma_zavala": "guide",
        "por": "'Arreglar, acomodar'. Achagua `nuchuniu` 'acomodar, componer' con nu- prefijado, o sea transitivo (neira-ribero-1762; perea-alonso-1942 p. 635)."},
    "hueke": {"clase": "nombre", "cat": "sust", "num": 155, "forma_zavala": "hueque",
        "por": "'Sitio de trabajo': la glosa de la fuente es «sitio de X», un nombre de lugar. DUDOSO declarado: podría ser la nominalización de un verbo 'trabajar' (el lokono la forma con -hù, perea-alonso-1942 p. 612), pero lo que la fuente da es el nombre y en duda se degrada."},
    "ikoroata": {"clase": "nombre", "cat": "sust", "num": 162, "forma_zavala": "icoroata",
        "por": "'Caraota', fitónimo. El propio minador ya lo declara en DESMARCADAS_F7: «es la voz caquetía; 'caraota' es su glosa». Cero usos raíz+aspecto en la base. deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #162)."},
    "jabal": {"clase": "accion", "cat": "v_raiz", "num": 168, "forma_zavala": "jabal",
        "por": "'Adquirir', infinitivo transitivo. deuda: sin-procedencia — ninguna hermana del repo da 'adquirir' con glosa idéntica; el apoyo es la glosa de la fuente (zavala-reyes-2015 #168)."},
    "jadarayte": {"clase": "accion", "cat": "v_raiz", "num": 172, "forma_zavala": "jadarayte",
        "por": "'Recoger', infinitivo. El wayuu del lexicón lo dice en infinitivo dos veces —`aja'itaa` 'recoger agua', `asukaa` 'recoger leña'— aunque estén etiquetadas `sust` por el aplanamiento de la comparanda: se cita la GLOSA, no su cat. deuda: sin-procedencia — ese wayuu viene de Captain & Captain 2005, que NO es obra de 4-fuentes/bibliografia.yaml, así que no es clave foránea (regla 8)."},
    "juri": {"clase": "nombre", "cat": "sust", "num": 178, "forma_zavala": "juri",
        "por": "'Viento, ventarrón' — EL CASO CENTRAL, 227 usos raíz+aspecto. En las tres hermanas 'viento' es nombre y el soplar es verbo aparte: lokono `wadu-lli` 'viento'; wayuu `wawai` 'viento (de tempestad)' frente a `waawataa` 'soplar (el viento)'; achagua `nususube` 'viento mío' —un nombre POSEÍDO con nu-— frente a `risuayu` 'correr viento' y `guanamatau` 'echarse el viento' (neira-ribero-1762). van Buurt lo da como RAÍZ nominal `hudi`/`juri` 'viento' en Hudishibana 'llano ventoso' (van-buurt-2014 §5). Y el propio repo lo lee como nombre: `jurijurebo` 'Paso de los vientos' es la reduplicación de plural sobre `juri` (morfologia.md §4)."},
    "lawari": {"clase": "nombre", "cat": "sust", "num": 182, "forma_zavala": "laguari",
        "por": "'Acacia Espinoza, acacia. Lauadrí', fitónimo. deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #182)."},
    "orumo": {"clase": "nombre", "cat": "sust", "num": 187, "forma_zavala": "orumo",
        "por": "'Urumu. Apamate', fitónimo (Tabebuia). deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #187)."},
    "patapati": {"clase": "estativo", "cat": "v_estativo", "num": 198, "forma_zavala": "patapati",
        "por": "'Anegadizo' es propiedad del terreno, y los estados son 4ª conjugación lokono (perea-alonso-1942 p. 634). La forma es además reduplicada, y la reduplicación caquetía es productiva y medida (morfologia.md §4, gatschet-1885). deuda: sin-procedencia para el cognado — ninguna hermana da 'anegadizo' con glosa idéntica."},
    "popoi": {"clase": "adverbio", "cat": "part", "num": 201, "forma_zavala": "popoi",
        "por": "La glosa de Zavala es «Ahí. **Adverbio de lugar**»: la fuente declara la parte de la oración. El lexicón ya tiene esa clase y la llama `part` — `yama` 'aquí, en este lugar (deíctico proximal)' y `kana-pa` 'allá'. Apoyo: lokono `jon` 'allá, allí (adverbio demostrativo distal)' y `yu-mùn` 'allí' (perea-alonso-1942); achagua `neenì` 'allí' (neira-ribero-1762). 59 usos raíz+aspecto en la base — «ahí-completivo», que es lo que la heurística permitía decir."},
    "kibakibi": {"clase": "nombre", "cat": "sust", "num": 205, "forma_zavala": "quibaquibi",
        "por": "'Baquiano, conocedor': las dos acepciones son nombres de AGENTE en castellano («un baquiano», «un conocedor»), no adjetivos de estado — que es lo que la separa de `guasima` 'viejo'. El agentivo arahuaco se forma sobre el verbo (lokono -ha-li-n 'andador', perea-alonso-1942 p. 612), pero lo atestiguado aquí es la forma entera. DUDOSO declarado: si se leyera 'conocedor' como cualidad sería estativo; en duda se degrada (regla 2)."},
    "kiboata": {"clase": "accion", "cat": "v_raiz", "num": 206, "forma_zavala": "quiboata",
        "por": "'Engañar'. Lokono `muli-da` 'engañar' (perea-alonso-1942), ya v_raiz en el lexicón; achagua `nucharisuedau` 'embaucar, engañar' y `nuchanisuedau` 'burlar, engañar', con nu- prefijado (neira-ribero-1762)."},
    "kidiboata": {"clase": "accion", "cat": "v_raiz", "num": 213, "forma_zavala": "quidiboata",
        "por": "'Engañar, engañado': verbo y participio de la misma raíz, que es la prueba interna de que la base es verbal — el lokono forma el participio pasivo con -sia sobre el verbo (perea-alonso-1942 p. 612). Comparte raíz con #206 `quiboata`."},
    "kiwawa": {"clase": "nombre", "cat": "sust", "num": 215, "forma_zavala": "quiguagua",
        "por": "'Especie de haba grande y blanca', fitónimo. deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #215)."},
    "kiricias": {"clase": "nombre", "cat": "sust", "num": 217, "forma_zavala": "quiricias",
        "por": "'Sangre, sangrado'. 'Sangre' es nombre en las tres hermanas —lokono `ttenna` e `ithihi`, wayuu, achagua `yrraí` (neira-ribero-1762)— y el lokono tiene ADEMÁS el estativo aparte, `ùttùa` 'ser sangriento, estar ensangrentado' (perea-alonso-1942 p. 639): la lengua distingue el nombre del estado, y la glosa de Zavala empieza por el nombre."},
    "raporon": {"clase": "nombre", "cat": "sust", "num": 220, "forma_zavala": "raporon",
        "por": "'Calabaza con cal'. Gemela de #27 `baperon`, mismo referente y misma clase; achagua `cuirro` 'calabaza, uyama' (neira-ribero-1762)."},
    "sinwanguso": {"clase": "estativo", "cat": "v_estativo", "num": 229, "forma_zavala": "singuanguso",
        "por": "'Insolente' es cualidad de carácter; entra por la regla general de Perea (perea-alonso-1942 pp. 598-599/608: nombre, adjetivo o partícula se hacen verbo). deuda: sin-procedencia — ninguna hermana da 'insolente' con glosa idéntica."},
    "surupa": {"clase": "nombre", "cat": "sust", "num": 231, "forma_zavala": "surupa",
        "por": "'Blatta orientalis. Cucaracha', zoónimo. Achagua `baderrea` 'cucaracha' (neira-ribero-1762)."},
    "tuba": {"clase": "nombre", "cat": "sust", "num": 253, "forma_zavala": "tuba",
        "por": "'Aglomeración, montón'. La achagua tiene las DOS voces por separado —`bambasí` 'montón' (nombre) y `nuetaidau` 'amontonar' (verbo con nu- prefijado)— y la glosa de Zavala es la del nombre (neira-ribero-1762). 35 usos raíz+aspecto."},
    "ubeda": {"clase": "nombre", "cat": "sust", "num": 266, "forma_zavala": "ubeda",
        "por": "'Acacia fétida. Mapurite, cují hediondo', fitónimo. deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #266)."},
    "uray": {"clase": "nombre", "cat": "sust", "num": 271, "forma_zavala": "uray",
        "por": "'Envoltura o vaina de las cerbatanas': un objeto manufacturado. deuda: sin-procedencia para el cognado; el apoyo es la glosa (zavala-reyes-2015 #271)."},
    "ure": {"clase": "nombre", "cat": "sust", "num": 272, "forma_zavala": "ure",
        "por": "'Raíz'. Nombre en las tres hermanas: lokono `iikirahi`, wayuu `ourala`, achagua `baririba` (neira-ribero-1762). Y van Buurt lo registra como raíz nominal `-ure`/`-huri` 'raíz' (van-buurt-2014 §5, MORFEMAS_VAN_BUURT). ⚠️ homógrafo del formante toponímico `-ure`, en disputa con el `-are` 'sitio de' (morfologia.md §5)."},
    "usera": {"clase": "estativo", "cat": "v_estativo", "num": 275, "forma_zavala": "usera",
        "por": "'Seco, arenoso'. El lexicón ya trae el wayuu `josoo` 'estar seco, -ca' con la glosa en forma verbal. Paraujano `jaradu` 'seco' (oliver-1989-apendice-a, tabla A-2). Y la achagua lo predica con el privativo ma-: `macarray` 'seco', `macarracataní` 'seco, estando seco' (neira-ribero-1762), que es el mecanismo de van Buurt §8 (van-buurt-2014)."},
}


# Reparto medido, no contado a mano.
REPARTO_DE_CLASES: dict[str, int] = {
    "accion": 9,
    "adverbio": 1,
    "estativo": 10,
    "nombre": 29,
}


# Entradas del vocabulario activo SIN clase declarada: caen en la
# heurística de tier. Si esta lista deja de estar vacía para una que
# salga `v_raiz`, es que el cajón de resto volvió a decidir solo.
SIN_CLASE_DECLARADA: list[str] = [
]


# ══════════════════════════════════════════════════════════════════
# HOMÓGRAFOS CON ESPAÑOL — se resuelven POR CONTEXTO
# ══════════════════════════════════════════════════════════════════
# Son caquetío atestiguado, pero su forma coincide con una palabra
# española corriente. Sin tratamiento, un texto en español que diga
# "el bagre" puntuaría como caquetío. score_linguistico los cuenta solo
# si un vecino inmediato es arahuaco (mismo mecanismo que ya usa 'para').

# Revisión F7 (2026-08-03): las 28 formas que la heurística marcaba se
# revisaron una por una contra su entrada de Zavala. 14 siguen marcadas,
# 11 perdieron la marca por no ser palabras del español (DESMARCADAS_F7 en
# el minador) y 3 salieron del habla (DESCARTADOS_ZAVALA, abajo).

HOMOGRAFOS_ZAVALA: frozenset = frozenset({
    "bagre",
    "dato",
    "samuro",
    "tuba",
})


# Veredicto por forma, para que la marca sea auditable y no un acto de fe.
VEREDICTO_HOMOGRAFOS: dict[str, str] = {
    "bagre": "#21 (AM) 'pez'. Caquetía según la fuente; el 'bagre' español es a su vez indigenismo. Colisión real.",
    "dato": "#105 (HB) 'fruto del cardón'. Caquetía, pero 'dato' es altísima frecuencia en español: la marca es imprescindible.",
    "samuro": "#223 (AM) 'punta hacia el mar'. La forma coincide con 'zamuro' (zoónimo venezolano) y la glosa es geográfica: ATRIBUCIÓN DÉBIL.",
    "tuba": "#253 (E) 'aglomeración, montón'. Caquetía; colisiona con 'tuba'.",
}


# Homógrafos que la migración D5 DISOLVIÓ: la colisión con el español era
# de la grafía colonial, no del fonema (guaca chocaba con 'guaca'; waka no
# choca con nada). Se conserva el veredicto F7 para que nadie los vuelva a
# marcar «por si acaso» — marcarlos haría sub-contar caquetío legítimo.
HOMOGRAFOS_DISUELTOS_D5: dict[str, str] = {
    "aka": "grafía fuente «aca» — #3 (E) 'bejuco'. Caquetía. Colisiona con 'acá' si se escribe sin tilde.",
    "kana": "grafía fuente «cana» — #57 (HB) 'demonio'. Caquetía; colisiona con 'cana'/'caña'.",
    "kapo": "grafía fuente «capo» — #59 (E) 'duende'. Caquetía (cf. #60 capu 'demonio'); colisión menor con 'capo'.",
    "karama": "grafía fuente «carama» — #64 (E) 'ramazón'. Caquetía; 'carama' existe en español rural (escarcha).",
    "kokuy": "grafía fuente «cocuy» — #87 'penca; planta que da un vino'. Indigenismo de circulación pan-venezolana: ATRIBUCIÓN DÉBIL además de homógrafo.",
    "take": "grafía fuente «taque» — #236 (E) 'árbol nucífero'. Caquetía; 'taque' español es regional y raro.",
    "takes": "grafía fuente «taques» — #237 (AM) 'salina'. Es también el topónimo Los Taques (Paraguaná): la glosa es la etimología del lugar. ATRIBUCIÓN DÉBIL.",
    "waka": "grafía fuente «guaca» — #123 (E) 'ave, cotorra'. Caquetía; 'guaca' español (quechua, tesoro) es otra cosa.",
    "way": "grafía fuente «guay» — #147 (E)(A) 'árbol parecido a la ceiba'. Caquetía; colisiona con la interjección.",
}


# Colisiones de lema fonémico — NO se renombraron: cada una es una
# decisión pendiente, no un accidente. La entrada sigue en grafía fuente.
COLISIONES_D5: list[dict] = [
    {"forma": "naure", "lema_fonemico": "naure", "num": 185, "motivo": "más de una entrada del glosario da el lema «naure»"},
    {"forma": "naure", "lema_fonemico": "naure", "num": 186, "motivo": "más de una entrada del glosario da el lema «naure»"},
]


# ══════════════════════════════════════════════════════════════════
# REFERENCIA DE CANON — fuera del vocabulario activo
# ══════════════════════════════════════════════════════════════════
# Un agente no dice 'Bariquisimeto' para decir 'río turbio'. Se conservan
# por su valor etnohistórico y morfológico (muestran cómo compone la
# lengua), pero NO entran a VOCABULARIO_BASE ni puntúan.

TOPONIMOS_ZAVALA: dict[str, str] = {
    "aburi": "Para designar las aguas de un río lleno de arena",   # curación manual: topónimo/etnónimo o glosa incierta
    "acatute": "Pueblo entre valles",   # curación manual: topónimo/etnónimo o glosa incierta
    "adabacoa": "Todo arboleda",   # curación manual: topónimo/etnónimo o glosa incierta
    "alaurima": "Río blanco o claro",   # curación manual: topónimo/etnónimo o glosa incierta
    "alcaboa": "Tierras solas o desiertas",   # curación manual: topónimo/etnónimo o glosa incierta
    "aricula": "Punto de tierra",   # curación manual: topónimo/etnónimo o glosa incierta
    "aruba": "Oruba. Oruma. Puede ser Oirubae: aquel o aquella que acompaña",   # curación manual: topónimo/etnónimo o glosa incierta
    "bariquisimeto": "Río de aguas turbias",   # curación manual: topónimo/etnónimo o glosa incierta
    "barisi": "Región de tierras coloradas cerca del mar",   # curación manual: topónimo/etnónimo o glosa incierta
    "bobare": "Sitio de cultivo",   # curación manual: topónimo/etnónimo o glosa incierta
    "cabudare": "sitio de cultivo",   # curación manual: topónimo/etnónimo o glosa incierta
    "capadare": "Diente de tigre",   # curación manual: topónimo/etnónimo o glosa incierta
    "caquetio": "Buena gente",   # curación manual: topónimo/etnónimo o glosa incierta
    "cemirucos": "Semerucos",   # curación manual: topónimo/etnónimo o glosa incierta
    "coroque": "Árbol de ¿?",   # curación manual: topónimo/etnónimo o glosa incierta
    "cumarebo": "Camino del cacique Cumare",   # curación manual: topónimo/etnónimo o glosa incierta
    "dabajuro": "Población de Falcón. Escrito originalmente daguajaro",   # curación manual: topónimo/etnónimo o glosa incierta
    "dabudare": "Sitio de extracción de barro",   # curación manual: topónimo/etnónimo o glosa incierta
    "doaca": "Asiento indígena del Estado Lara. [Duaca]",   # curación manual: topónimo/etnónimo o glosa incierta
    "guacaubana": "Río escondido",   # curación manual: topónimo/etnónimo o glosa incierta
    "guacurebo": "Quebrada que crece",   # curación manual: topónimo/etnónimo o glosa incierta
    "guadabacoa": "Arboleda",   # curación manual: topónimo/etnónimo o glosa incierta
    "guamabatriba": "Muchas tierras de cultivo",   # curación manual: topónimo/etnónimo o glosa incierta
    "guanajo": "Cardón aspecto muy lanoso",   # curación manual: topónimo/etnónimo o glosa incierta
    "guasare": "Árbol cactáceo",   # curación manual: topónimo/etnónimo o glosa incierta
    "iboa": "Comunidad indígena. Enemigo, enemistad",   # curación manual: topónimo/etnónimo o glosa incierta
    "jadicuar": "Sitio donde abunda jajato. Salicornia fructuosa",   # curación manual: topónimo/etnónimo o glosa incierta
    "jurijurebo": "Paso de los vientos",   # curación manual: topónimo/etnónimo o glosa incierta
    "pachacuare": "Sitio de palmeras",   # curación manual: topónimo/etnónimo o glosa incierta
    "paraguana": "Rodeada del mar",   # curación manual: topónimo/etnónimo o glosa incierta
    "parotaima": "Indígena del Yaracuy",   # curación manual: topónimo/etnónimo o glosa incierta
    "poapao": "Serranía de Coro",   # curación manual: topónimo/etnónimo o glosa incierta
    "quibacoas": "Bosques pedregosos",   # curación manual: topónimo/etnónimo o glosa incierta
    "sazaribacoa": "Río de los maizales",   # curación manual: topónimo/etnónimo o glosa incierta
    "siguruba": "Salvar. Caserío, sitio",   # curación manual: topónimo/etnónimo o glosa incierta
    "tabicure": "Indio caquetío del valle de las Damas",   # curación manual: topónimo/etnónimo o glosa incierta
    "tarai": "Garipial o caripial",   # curación manual: topónimo/etnónimo o glosa incierta
    "taratarare": "Hato, conuco",   # curación manual: topónimo/etnónimo o glosa incierta
    "todarahuato": "Indígena de la Vela",   # curación manual: topónimo/etnónimo o glosa incierta
    "turijerebo": "Lugar de descanso",   # curación manual: topónimo/etnónimo o glosa incierta
    "xirahara": "Población indígena vecina de los caquetíos. Nombre de cacique de los llano",   # curación manual: topónimo/etnónimo o glosa incierta
    "yacare": "Pueblo. Caimán",   # curación manual: topónimo/etnónimo o glosa incierta
    "yacarebacoa": "Pueblo del bosque",   # curación manual: topónimo/etnónimo o glosa incierta
    "yaracuy": "Indígena del Valle de las Damas. Población",   # curación manual: topónimo/etnónimo o glosa incierta
    "yaruca": "Indígena caquetío",   # curación manual: topónimo/etnónimo o glosa incierta
}

ANTROPONIMOS_ZAVALA: dict[str, str] = {
    "baracoica": "Cacique de Curazao",
    "chunare": "Apellido. Mazorca tierna",
    "huay": "Nombre propio",
    "quiceraguru": "Nombre propio indígena en Barquisimeto",
    "quiceroaboa": "Nombre propio indígena en Barquisimeto",
    "quiceromata": "Nombre propio indígena en Barquisimeto",
    "quiciroata": "Nombre propio indígena en Barquisimeto",
    "quiquiba": "nombre propio indígena",
    "tamani": "Nombre propio indígena",
    "timaure": "Apellido",
    "tumarure": "Apellido de un cacique",
    "xaraguamari": "Cacique de Yaracuy",
    "yarosabana": "Cacique de los Guaragua del Yaracuy. Pueblo",
    "zamurano": "nombre indígena del Yaracuy. Pueblo",
}

DESCARTADOS_ZAVALA: dict[str, str] = {
    "baquiro": "Cochino de monte. Lisandro Alvarado señala que es cumanagota",   # Zavala/compilador la marca de otra lengua
    "enea": "Planta ciperácea",   # F7: #118 (A) 'planta ciperácea'. 'Enea' (~anea, Typha) ES la palabra española del junco; Alvarado está dando el nombre castellano de la planta, no una voz caquetía.
    "guata": "Planta",   # F7: #146 (AM) 'Planta'. Glosa vacía —no dice qué planta— y homógrafo con 'guata'. Mismo criterio que `coroque` ('Árbol de ¿?').
    "hay": "Coca",   # F7: #154 (AM) 'coca'. La forma coincide con el verbo español más frecuente ('hay'); ninguna resolución por contexto compensa eso. En su lugar queda `hayo` (#156, 'hierba quita sed'), que es la forma corriente del mismo referente y no colisiona.
}


TOTALES = {
    "afijos": 8,
    "vocabulario_activo": 145,
    "renombradas_d5": 79,
    "clases_declaradas": 49,
    "clases_sin_declarar": 0,
    "homografos": 4,
    "homografos_disueltos_d5": 9,
    "colisiones_d5": 2,
    "toponimos": 45,
    "antroponimos": 14,
    "descartados": 4,
    "ya_en_lexicon_antes_del_import": 72,
    "entradas_pdf": 288,
}
