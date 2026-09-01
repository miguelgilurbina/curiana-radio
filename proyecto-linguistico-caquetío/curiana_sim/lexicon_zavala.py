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
    "kuna":          {"sig": "pez del golfete de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez del golfete de Coro [Zavala Reyes 2015 #95 (E)]", "forma_fuente": "cuna", "notas": "Zavala Reyes 2015 #95 (E)"},
    "kunaro":        {"sig": "pez del golfete de Coro. Promicops Guasa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez del golfete de Coro. Promicops Guasa [Zavala Reyes 2015 #96 (E)]", "forma_fuente": "cunaro", "identificacion_moderna": "Rhomboplites aurorubens (pargo cunaro, de altura) según SVDB. Zavala transcribe 'Promicops Guasa' (por Promicrops itajara, hoy Epinephelus itajara, el mero guasa): dos peces distintos.", "notas": "Zavala Reyes 2015 #96 (E)"},
    "dara":          {"sig": "alcaraván", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Alcaraván [Zavala Reyes 2015 #102 (HB+E)]", "notas": "Zavala Reyes 2015 #102 (HB+E)"},
    "waranaro":      {"sig": "pez lisa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez lisa [Zavala Reyes 2015 #139 (HB+E)]", "forma_fuente": "guaranaro", "identificacion_moderna": "sin resolver; 'lisa' apunta a Mugil spp. (M. curema / M. incilis son las del Golfete). La hoja de fuentes 02_ecologia lo daba por 'sin identificación taxonómica firme' cuando Zavala YA lo glosaba.", "notas": "Zavala Reyes 2015 #139 (HB+E)"},
    "naure":         {"sig": "jojoto", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Jojoto [Zavala Reyes 2015 #185 (E)]", "notas": "Zavala Reyes 2015 #185 (E)"},
    "naure":         {"sig": "planta bejucosa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta bejucosa [Zavala Reyes 2015 #186 (E)]", "notas": "Zavala Reyes 2015 #186 (E)"},

    # ── T3 — sustantivos concretos: fauna, flora, paisaje, técnica ──
    # Varios cierran 'huecos léxicos' que ecologia_lexicon_map.md daba por vacíos
    # (taques=salina, bisure=lagartija, chaguanco=zorro, jachos=teas de pesca).
    "ako":           {"sig": "comida. Par, casal, pareja", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Comida. Par, casal, pareja [Zavala Reyes 2015 #4 (E+AM)]", "forma_fuente": "aco", "notas": "Zavala Reyes 2015 #4 (E+AM); variantes: aca"},
    "arata":         {"sig": "mono", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mono [Zavala Reyes 2015 #13 (AM)]", "notas": "Zavala Reyes 2015 #13 (AM)"},
    "arika":         {"sig": "árbol de jícara o totumo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de jícara o totumo [Zavala Reyes 2015 #14 (AM)]", "forma_fuente": "arica", "notas": "Zavala Reyes 2015 #14 (AM)"},
    "bakoa":         {"sig": "bosque, lugar, paraje, sitio fértil", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bosque, lugar, paraje, sitio fértil [Zavala Reyes 2015 #18 (AM+E)]", "forma_fuente": "bacoa", "notas": "Zavala Reyes 2015 #18 (AM+E)"},
    "bajareke":      {"sig": "tabico hecho de tierra palos y bejuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tabico hecho de tierra palos y bejuco [Zavala Reyes 2015 #24 (AM)]", "forma_fuente": "bajareque", "notas": "Zavala Reyes 2015 #24 (AM)"},
    "barabara":      {"sig": "árbol de madera dura y pesada. Olivo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de madera dura y pesada. Olivo [Zavala Reyes 2015 #30 (A)]", "notas": "Zavala Reyes 2015 #30 (A)"},
    "barbasko":      {"sig": "hierba de borrachera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hierba de borrachera [Zavala Reyes 2015 #32 (HB)]", "forma_fuente": "barbasco", "notas": "Zavala Reyes 2015 #32 (HB)"},
    "bisure":        {"sig": "lagartija", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lagartija [Zavala Reyes 2015 #41 (HB+E)]", "notas": "Zavala Reyes 2015 #41 (HB+E)"},
    "buche":         {"sig": "planta xerofita, melocato, cardo globoso, rastrero", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta xerofita, melocato, cardo globoso, rastrero [Zavala Reyes 2015 #45 (AM+E)]", "notas": "Zavala Reyes 2015 #45 (AM+E); variantes: buchi"},
    "kabana":        {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #51 (HB)]", "forma_fuente": "cabana", "notas": "Zavala Reyes 2015 #51 (HB)"},
    "kakuro":        {"sig": "pequeña avispa negra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña avispa negra [Zavala Reyes 2015 #54 (E+A)]", "forma_fuente": "cacuro", "notas": "Zavala Reyes 2015 #54 (E+A)"},
    "kamaroa":       {"sig": "árbol lactescente, de hojas parecidas al papayo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol lactescente, de hojas parecidas al papayo [Zavala Reyes 2015 #56 (A)]", "forma_fuente": "camaroa", "notas": "Zavala Reyes 2015 #56 (A)"},
    "kapubana":      {"sig": "duende del cerro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende del cerro [Zavala Reyes 2015 #61 (HB)]", "forma_fuente": "capubana", "notas": "Zavala Reyes 2015 #61 (HB)"},
    "kaketillo":     {"sig": "árbol. Madera de construcción, resistente a la humedad", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol. Madera de construcción, resistente a la humedad [Zavala Reyes 2015 #63 (E+A)]", "forma_fuente": "caquetillo", "notas": "Zavala Reyes 2015 #63 (E+A)"},
    "karapa":        {"sig": "árbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol resinoso [Zavala Reyes 2015 #65 (E)]", "forma_fuente": "carapa", "notas": "Zavala Reyes 2015 #65 (E)"},
    "karuka":        {"sig": "paja, da consistencia al barro que se aplica a paredes y techos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paja, da consistencia al barro que se aplica a paredes y techos [Zavala Reyes 2015 #67 (E)]", "forma_fuente": "caruca", "notas": "Zavala Reyes 2015 #67 (E)"},
    "kaseto":        {"sig": "planta herbácea", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta herbácea [Zavala Reyes 2015 #68 (E)]", "forma_fuente": "caseto", "notas": "Zavala Reyes 2015 #68 (E)"},
    "kaskito":       {"sig": "agrio, fermentado", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Agrio, fermentado [Zavala Reyes 2015 #69 (HB)]", "forma_fuente": "casquito", "notas": "Zavala Reyes 2015 #69 (HB)"},
    "kaujaro":       {"sig": "árbol de madera blanda, fruta mucilaginosa, del género cordia", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de madera blanda, fruta mucilaginosa, del género cordia [Zavala Reyes 2015 #72 (E)]", "forma_fuente": "caujaro", "notas": "Zavala Reyes 2015 #72 (E)"},
    "kayude":        {"sig": "árbol frutal, guanábano silvestre, turagua", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol frutal, guanábano silvestre, turagua [Zavala Reyes 2015 #73 (E)]", "forma_fuente": "cayude", "notas": "Zavala Reyes 2015 #73 (E)"},
    "cege":          {"sig": "lechuza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lechuza [Zavala Reyes 2015 #78 (HB)]", "forma_fuente": "cegue", "notas": "Zavala Reyes 2015 #78 (HB)"},
    "chawanko":      {"sig": "zorro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Zorro [Zavala Reyes 2015 #80 (A)]", "forma_fuente": "chaguanco", "notas": "Zavala Reyes 2015 #80 (A)"},
    "chaure":        {"sig": "cegue. Lechuza que anida en cuevas de terrenos arenosos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cegue. Lechuza que anida en cuevas de terrenos arenosos [Zavala Reyes 2015 #81 (HB+E)]", "notas": "Zavala Reyes 2015 #81 (HB+E)"},
    "chipare":       {"sig": "matapalo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Matapalo [Zavala Reyes 2015 #82 (E)]", "notas": "Zavala Reyes 2015 #82 (E)"},
    "chirwa":        {"sig": "tinaja pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tinaja pequeña [Zavala Reyes 2015 #83 (HB)]", "forma_fuente": "chirgua", "notas": "Zavala Reyes 2015 #83 (HB)"},
    "kokuy":         {"sig": "penca. Planta rizomoza que da un vino agradable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Penca. Planta rizomoza que da un vino agradable [Zavala Reyes 2015 #87 (HB+CGB+A)]", "forma_fuente": "cocuy", "notas": "Zavala Reyes 2015 #87 (HB+CGB+A); era homógrafo del español en grafía fuente (cocuy) — la migración D5 disolvió la colisión"},
    "kurari":        {"sig": "árbol de roble, tecoma", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de roble, tecoma [Zavala Reyes 2015 #97 (E)]", "forma_fuente": "curari", "notas": "Zavala Reyes 2015 #97 (E)"},
    "dabuda":        {"sig": "barro loza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Barro loza [Zavala Reyes 2015 #99 (HB+E)]", "notas": "Zavala Reyes 2015 #99 (HB+E)"},
    "dakawa":        {"sig": "árbol de corteza gris, madera compacta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de corteza gris, madera compacta [Zavala Reyes 2015 #101 (A)]", "forma_fuente": "dacagua", "notas": "Zavala Reyes 2015 #101 (A)"},
    "darubana":      {"sig": "camino, vía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Camino, vía [Zavala Reyes 2015 #104 (AM)]", "notas": "Zavala Reyes 2015 #104 (AM); variantes: durabana"},
    "dato":          {"sig": "fruto del cardón", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fruto del cardón [Zavala Reyes 2015 #105 (HB)]", "notas": "Zavala Reyes 2015 #105 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "dipopo":        {"sig": "fibra de cocuiza, cabuya", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fibra de cocuiza, cabuya [Zavala Reyes 2015 #109 (AM)]", "notas": "Zavala Reyes 2015 #109 (AM)"},
    "ditero":        {"sig": "insecto, hormiga que daña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insecto, hormiga que daña [Zavala Reyes 2015 #110 (AM)]", "notas": "Zavala Reyes 2015 #110 (AM)"},
    "dibidibe":      {"sig": "árbol cuyo fruto es una baya que da tinta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol cuyo fruto es una baya que da tinta [Zavala Reyes 2015 #112 (E)]", "forma_fuente": "dividive", "notas": "Zavala Reyes 2015 #112 (E)"},
    "ebo":           {"sig": "camino, paso, senda", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Camino, paso, senda [Zavala Reyes 2015 #117 (E)]", "notas": "Zavala Reyes 2015 #117 (E)"},
    "waka":          {"sig": "ave, cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave, cotorra [Zavala Reyes 2015 #123 (E)]", "forma_fuente": "guaca", "notas": "Zavala Reyes 2015 #123 (E); era homógrafo del español en grafía fuente (guaca) — la migración D5 disolvió la colisión"},
    "wache":         {"sig": "murciélago, zorro blanco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Murciélago, zorro blanco [Zavala Reyes 2015 #125 (E+AM)]", "forma_fuente": "guache", "notas": "Zavala Reyes 2015 #125 (E+AM)"},
    "wako":          {"sig": "planta herbácea de la familia de las portulacea", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta herbácea de la familia de las portulacea [Zavala Reyes 2015 #126 (E)]", "forma_fuente": "guaco", "notas": "Zavala Reyes 2015 #126 (E)"},
    "wakoa":         {"sig": "paloma", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paloma [Zavala Reyes 2015 #127 (HB)]", "forma_fuente": "guacoa", "notas": "Zavala Reyes 2015 #127 (HB)"},
    "wakuaro":       {"sig": "palo de tinte", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palo de tinte [Zavala Reyes 2015 #128 (A+AM)]", "forma_fuente": "guacuaro", "notas": "Zavala Reyes 2015 #128 (A+AM)"},
    "wairon":        {"sig": "hoguera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hoguera [Zavala Reyes 2015 #132 (HB)]", "forma_fuente": "guairon", "notas": "Zavala Reyes 2015 #132 (HB)"},
    "wamacho":       {"sig": "árbol cactáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol cactáceo [Zavala Reyes 2015 #134 (A+E)]", "forma_fuente": "guamacho", "notas": "Zavala Reyes 2015 #134 (A+E)"},
    "warataro":      {"sig": "barro de loza, para la fábrica de budares y ollas", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Barro de loza, para la fábrica de budares y ollas [Zavala Reyes 2015 #141 (E)]", "forma_fuente": "guarataro", "notas": "Zavala Reyes 2015 #141 (E)"},
    "wariana":       {"sig": "arbusto halófilo, frailejón de la playa. Tabaco pescador", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arbusto halófilo, frailejón de la playa. Tabaco pescador [Zavala Reyes 2015 #142 (E)]", "forma_fuente": "guariana", "notas": "Zavala Reyes 2015 #142 (E)"},
    "waru":          {"sig": "volturido, cataneja. Ave mayor que el zamuro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Volturido, cataneja. Ave mayor que el zamuro [Zavala Reyes 2015 #143 (E)]", "forma_fuente": "guaru", "notas": "Zavala Reyes 2015 #143 (E)"},
    "way":           {"sig": "árbol parecido a la ceiba", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol parecido a la ceiba [Zavala Reyes 2015 #147 (E+A)]", "forma_fuente": "guay", "notas": "Zavala Reyes 2015 #147 (E+A); era homógrafo del español en grafía fuente (guay) — la migración D5 disolvió la colisión"},
    "harifuche":     {"sig": "maíz tostado y miel", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maíz tostado y miel [Zavala Reyes 2015 #153 (HB)]", "notas": "Zavala Reyes 2015 #153 (HB)"},
    "huaymujo":      {"sig": "pequeño cangrejo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeño cangrejo [Zavala Reyes 2015 #158 (E)]", "notas": "Zavala Reyes 2015 #158 (E)"},
    "humohumo":      {"sig": "el ave que vuela", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "El ave que vuela [Zavala Reyes 2015 #160 (AM)]", "notas": "Zavala Reyes 2015 #160 (AM)"},
    "igi":           {"sig": "árbol, matapalo, paují", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol, matapalo, paují [Zavala Reyes 2015 #164 (E)]", "forma_fuente": "igui", "notas": "Zavala Reyes 2015 #164 (E)"},
    "isiro":         {"sig": "árbol corpulento sapindáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol corpulento sapindáceo [Zavala Reyes 2015 #167 (A)]", "notas": "Zavala Reyes 2015 #167 (A)"},
    "jachos":        {"sig": "teas de madera, para encandilar en las labores de pesca nocturna", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Teas de madera, para encandilar en las labores de pesca nocturna [Zavala Reyes 2015 #169 (E)]", "notas": "Zavala Reyes 2015 #169 (E)"},
    "jajato":        {"sig": "chloris Radiata. Yerba forrajera. Lugar de arena", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Chloris Radiata. Yerba forrajera. Lugar de arena [Zavala Reyes 2015 #176 (A+AM)]", "notas": "Zavala Reyes 2015 #176 (A+AM)"},
    "judereke":      {"sig": "árbol ramoso, parecido al chiguare", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol ramoso, parecido al chiguare [Zavala Reyes 2015 #177 (E)]", "forma_fuente": "judereque", "notas": "Zavala Reyes 2015 #177 (E)"},
    "jusual":        {"sig": "sembrar, siembra, sembradío. Conuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sembrar, siembra, sembradío. Conuco [Zavala Reyes 2015 #180 (AM)]", "notas": "Zavala Reyes 2015 #180 (AM)"},
    "koro":          {"sig": "cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cotorra [Zavala Reyes 2015 #181 (HB)]", "notas": "Zavala Reyes 2015 #181 (HB)"},
    "parawa":        {"sig": "mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mar [Zavala Reyes 2015 #191 (GC)]", "forma_fuente": "paragua", "notas": "Zavala Reyes 2015 #191 (GC)"},
    "parawatan":     {"sig": "árbol maderable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol maderable [Zavala Reyes 2015 #193 (AM)]", "forma_fuente": "paraguatan", "notas": "Zavala Reyes 2015 #193 (AM)"},
    "piritu":        {"sig": "palmera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palmera [Zavala Reyes 2015 #199 (E+A+AM)]", "notas": "Zavala Reyes 2015 #199 (E+A+AM)"},
    "kerekere":      {"sig": "ave pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave pequeña [Zavala Reyes 2015 #202 (AM)]", "forma_fuente": "querequere", "notas": "Zavala Reyes 2015 #202 (AM)"},
    "kikuidi":       {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #211 (HB)]", "forma_fuente": "quicuidi", "notas": "Zavala Reyes 2015 #211 (HB)"},
    "kiwa":          {"sig": "concha de almeja y otros moluscos. Sitio del estado Lara", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Concha de almeja y otros moluscos. Sitio del estado Lara [Zavala Reyes 2015 #214 (E+AM)]", "forma_fuente": "quigua", "notas": "Zavala Reyes 2015 #214 (E+AM)"},
    "ruba":          {"sig": "especie de abeja silvestre negra de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de abeja silvestre negra de Coro [Zavala Reyes 2015 #221 (A)]", "notas": "Zavala Reyes 2015 #221 (A)"},
    "samuro":        {"sig": "punta hacia el mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta hacia el mar [Zavala Reyes 2015 #223 (AM)]", "notas": "Zavala Reyes 2015 #223 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "sibidiwa":      {"sig": "arbusto euforbiaceo. Jatrofa Gossy Pifolia", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arbusto euforbiaceo. Jatrofa Gossy Pifolia [Zavala Reyes 2015 #226 (E+A)]", "forma_fuente": "sibidigua", "notas": "Zavala Reyes 2015 #226 (E+A)"},
    "supi":          {"sig": "sitio a orilla del mar. Arena. Arboleda supide", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio a orilla del mar. Arena. Arboleda supide [Zavala Reyes 2015 #230 (AM+PMA)]", "notas": "Zavala Reyes 2015 #230 (AM+PMA)"},
    "taboro":        {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #233 (HB)]", "notas": "Zavala Reyes 2015 #233 (HB)"},
    "take":          {"sig": "árbol nucífero", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol nucífero [Zavala Reyes 2015 #236 (E)]", "forma_fuente": "taque", "notas": "Zavala Reyes 2015 #236 (E); era homógrafo del español en grafía fuente (taque) — la migración D5 disolvió la colisión"},
    "takes":         {"sig": "salina", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Salina [Zavala Reyes 2015 #237 (AM)]", "forma_fuente": "taques", "notas": "Zavala Reyes 2015 #237 (AM); era homógrafo del español en grafía fuente (taques) — la migración D5 disolvió la colisión"},
    "taratore":      {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #241 (AM)]", "notas": "Zavala Reyes 2015 #241 (AM)"},
    "tauta":         {"sig": "pequeña paloma de hábitos ictiófagos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña paloma de hábitos ictiófagos [Zavala Reyes 2015 #244 (E)]", "notas": "Zavala Reyes 2015 #244 (E)"},
    "tiwa":          {"sig": "árbol rutáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol rutáceo [Zavala Reyes 2015 #246 (E)]", "forma_fuente": "tigua", "notas": "Zavala Reyes 2015 #246 (E)"},
    "tigi":          {"sig": "pequeña paloma que se alimenta de peces", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña paloma que se alimenta de peces [Zavala Reyes 2015 #247 (E)]", "forma_fuente": "tigui", "notas": "Zavala Reyes 2015 #247 (E)"},
    "tijua":         {"sig": "paloma de canto onomatopéyico", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paloma de canto onomatopéyico [Zavala Reyes 2015 #248 (E)]", "notas": "Zavala Reyes 2015 #248 (E)"},
    "tomatei":       {"sig": "punta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta [Zavala Reyes 2015 #252 (AM)]", "notas": "Zavala Reyes 2015 #252 (AM)"},
    "tubarao":       {"sig": "arenales", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arenales [Zavala Reyes 2015 #254 (E)]", "notas": "Zavala Reyes 2015 #254 (E)"},
    "tupure":        {"sig": "siembra de cacao", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra de cacao [Zavala Reyes 2015 #256 (s/sigla)]", "notas": "Zavala Reyes 2015 #256 (s/sigla)"},
    "tukinemo":      {"sig": "llano, plano", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Llano, plano [Zavala Reyes 2015 #258 (AM)]", "forma_fuente": "tuquinemo", "notas": "Zavala Reyes 2015 #258 (AM)"},
    "turicha":       {"sig": "ave cantadora. Flauta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave cantadora. Flauta [Zavala Reyes 2015 #260 (AM)]", "notas": "Zavala Reyes 2015 #260 (AM)"},
    "turumako":      {"sig": "cerro, meseta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cerro, meseta [Zavala Reyes 2015 #262 (AM)]", "forma_fuente": "turumaco", "notas": "Zavala Reyes 2015 #262 (AM)"},
    "turupia":       {"sig": "árbol espinoso. Sitio en Cumarebo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol espinoso. Sitio en Cumarebo [Zavala Reyes 2015 #263 (AM+A)]", "notas": "Zavala Reyes 2015 #263 (AM+A)"},
    "tuturutos":     {"sig": "hierba de propiedades eméticas. Usado para cuajar quesos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hierba de propiedades eméticas. Usado para cuajar quesos [Zavala Reyes 2015 #264 (E)]", "notas": "Zavala Reyes 2015 #264 (E)"},
    "uria":          {"sig": "plantío, siembra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Plantío, siembra [Zavala Reyes 2015 #273 (AM)]", "notas": "Zavala Reyes 2015 #273 (AM)"},
    "yabo":          {"sig": "cercidium Virid. Arbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cercidium Virid. Arbol resinoso [Zavala Reyes 2015 #278 (E+A+AM)]", "notas": "Zavala Reyes 2015 #278 (E+A+AM)"},
    "yakure":        {"sig": "árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare [Zavala Reyes 2015 #281 (AM+E)]", "forma_fuente": "yacure", "notas": "Zavala Reyes 2015 #281 (AM+E)"},
    "yagruma":       {"sig": "caracol, molusco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caracol, molusco [Zavala Reyes 2015 #282 (A)]", "notas": "Zavala Reyes 2015 #282 (A)"},
    "yapamata":      {"sig": "siembra, plantío", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra, plantío [Zavala Reyes 2015 #283 (AM)]", "notas": "Zavala Reyes 2015 #283 (AM)"},
    "yaro":          {"sig": "bejuco. Planta venenosa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bejuco. Planta venenosa [Zavala Reyes 2015 #285 (AM)]", "notas": "Zavala Reyes 2015 #285 (AM)"},

    # ── T4 — verbos, cualidades y abstractos ──
    # El lexicón activo es pobre en verbos y cualidades; este tier lo compensa.
    "aka":           {"sig": "bejuco", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bejuco [Zavala Reyes 2015 #3 (E)]", "forma_fuente": "aca", "notas": "Zavala Reyes 2015 #3 (E); era homógrafo del español en grafía fuente (aca) — la migración D5 disolvió la colisión"},
    "apo":           {"sig": "grande", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Grande [Zavala Reyes 2015 #11 (AM)]", "notas": "Zavala Reyes 2015 #11 (AM)"},
    "bachure":       {"sig": "maneto, patituerto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maneto, patituerto [Zavala Reyes 2015 #19 (A)]", "notas": "Zavala Reyes 2015 #19 (A)"},
    "badamaro":      {"sig": "extraer, sacar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Extraer, sacar [Zavala Reyes 2015 #20 (AM)]", "notas": "Zavala Reyes 2015 #20 (AM)"},
    "baharuko":      {"sig": "abuelo, viejo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Abuelo, viejo [Zavala Reyes 2015 #22 (AM)]", "forma_fuente": "baharuco", "notas": "Zavala Reyes 2015 #22 (AM)"},
    "baperon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #27 (HB)]", "notas": "Zavala Reyes 2015 #27 (HB)"},
    "barbache":      {"sig": "iguana", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Iguana [Zavala Reyes 2015 #33 (PMA)]", "notas": "Zavala Reyes 2015 #33 (PMA)"},
    "beceremikore":  {"sig": "dominar, triunfar, victoria", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Dominar, triunfar, victoria [Zavala Reyes 2015 #39 (AM)]", "forma_fuente": "beceremicore", "notas": "Zavala Reyes 2015 #39 (AM)"},
    "kachipo":       {"sig": "en voz vulgar, enojado, colérico", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "En voz vulgar, enojado, colérico [Zavala Reyes 2015 #53 (A)]", "forma_fuente": "cachipo", "notas": "Zavala Reyes 2015 #53 (A)"},
    "kana":          {"sig": "demonio", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio [Zavala Reyes 2015 #57 (HB)]", "forma_fuente": "cana", "notas": "Zavala Reyes 2015 #57 (HB); era homógrafo del español en grafía fuente (cana) — la migración D5 disolvió la colisión"},
    "kapo":          {"sig": "duende, ente sobrenatural", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende, ente sobrenatural [Zavala Reyes 2015 #59 (E)]", "forma_fuente": "capo", "notas": "Zavala Reyes 2015 #59 (E); era homógrafo del español en grafía fuente (capo) — la migración D5 disolvió la colisión"},
    "kapu":          {"sig": "demonio. Señala Galeotto Cey la pronunciación “cap”", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio. Señala Galeotto Cey la pronunciación “cap” [Zavala Reyes 2015 #60 (HB)]", "forma_fuente": "capu", "notas": "Zavala Reyes 2015 #60 (HB)"},
    "karama":        {"sig": "ramazón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ramazón [Zavala Reyes 2015 #64 (E)]", "forma_fuente": "carama", "notas": "Zavala Reyes 2015 #64 (E); era homógrafo del español en grafía fuente (carama) — la migración D5 disolvió la colisión"},
    "chuchube":      {"sig": "paraulata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paraulata [Zavala Reyes 2015 #85 (HB)]", "notas": "Zavala Reyes 2015 #85 (HB)"},
    "komoho":        {"sig": "higo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Higo [Zavala Reyes 2015 #88 (HB)]", "forma_fuente": "comoho", "notas": "Zavala Reyes 2015 #88 (HB)"},
    "despopo":       {"sig": "fuerza", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fuerza [Zavala Reyes 2015 #107 (AM)]", "notas": "Zavala Reyes 2015 #107 (AM)"},
    "dichiba":       {"sig": "límite, línea", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Límite, línea [Zavala Reyes 2015 #108 (AM)]", "forma_fuente": "dichiva", "notas": "Zavala Reyes 2015 #108 (AM)"},
    "domaria":       {"sig": "enredarse, atormentar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Enredarse, atormentar [Zavala Reyes 2015 #114 (AM)]", "notas": "Zavala Reyes 2015 #114 (AM)"},
    "duriwa":        {"sig": "hacer trabajos cortos", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hacer trabajos cortos [Zavala Reyes 2015 #116 (AM)]", "forma_fuente": "durigua", "notas": "Zavala Reyes 2015 #116 (AM)"},
    "etamo":         {"sig": "feroz, feo, espanto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Feroz, feo, espanto [Zavala Reyes 2015 #120 (AM)]", "notas": "Zavala Reyes 2015 #120 (AM)"},
    "waidima":       {"sig": "integro", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Integro [Zavala Reyes 2015 #131 (AM)]", "forma_fuente": "guaidima", "notas": "Zavala Reyes 2015 #131 (AM)"},
    "wamipa":        {"sig": "hueco, profundidad", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hueco, profundidad [Zavala Reyes 2015 #135 (AM)]", "forma_fuente": "guamipa", "notas": "Zavala Reyes 2015 #135 (AM)"},
    "warakaro":      {"sig": "tapirama silvestre", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tapirama silvestre [Zavala Reyes 2015 #138 (E)]", "forma_fuente": "guaracaro", "notas": "Zavala Reyes 2015 #138 (E)"},
    "waranao":       {"sig": "salado, ácido", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Salado, ácido [Zavala Reyes 2015 #140 (E)]", "forma_fuente": "guaranao", "notas": "Zavala Reyes 2015 #140 (E)"},
    "wasima":        {"sig": "viejo, anciano", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Viejo, anciano [Zavala Reyes 2015 #145 (AM)]", "forma_fuente": "guasima", "notas": "Zavala Reyes 2015 #145 (AM)"},
    "gika":          {"sig": "yabo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Yabo [Zavala Reyes 2015 #150 (E)]", "forma_fuente": "guica", "notas": "Zavala Reyes 2015 #150 (E)"},
    "gide":          {"sig": "arreglar, acomodar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arreglar, acomodar [Zavala Reyes 2015 #151 (AM)]", "forma_fuente": "guide", "notas": "Zavala Reyes 2015 #151 (AM)"},
    "hueke":         {"sig": "sitio de trabajo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio de trabajo [Zavala Reyes 2015 #155 (AM)]", "forma_fuente": "hueque", "notas": "Zavala Reyes 2015 #155 (AM)"},
    "ikoroata":      {"sig": "caraota", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caraota [Zavala Reyes 2015 #162 (HB)]", "forma_fuente": "icoroata", "notas": "Zavala Reyes 2015 #162 (HB)"},
    "jabal":         {"sig": "adquirir", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Adquirir [Zavala Reyes 2015 #168 (AM)]", "notas": "Zavala Reyes 2015 #168 (AM)"},
    "jadarayte":     {"sig": "recoger", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Recoger [Zavala Reyes 2015 #172 (AM)]", "notas": "Zavala Reyes 2015 #172 (AM)"},
    "juri":          {"sig": "viento, ventarrón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Viento, ventarrón [Zavala Reyes 2015 #178 (E)]", "notas": "Zavala Reyes 2015 #178 (E); variantes: jura"},
    "lawari":        {"sig": "acacia Espinoza, acacia. Lauadrí", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Acacia Espinoza, acacia. Lauadrí [Zavala Reyes 2015 #182 (E+A+PMA)]", "forma_fuente": "laguari", "notas": "Zavala Reyes 2015 #182 (E+A+PMA)"},
    "orumo":         {"sig": "urumu. Apamate. No confundir con el Myrciacucuo llata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Urumu. Apamate. No confundir con el Myrciacucuo llata [Zavala Reyes 2015 #187 (A+PMA)]", "notas": "Zavala Reyes 2015 #187 (A+PMA)"},
    "patapati":      {"sig": "anegadizo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Anegadizo [Zavala Reyes 2015 #198 (AM)]", "notas": "Zavala Reyes 2015 #198 (AM)"},
    "popoi":         {"sig": "ahí. Adverbio de lugar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ahí. Adverbio de lugar [Zavala Reyes 2015 #201 (AM)]", "notas": "Zavala Reyes 2015 #201 (AM)"},
    "kibakibi":      {"sig": "baquiano, conocedor", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Baquiano, conocedor [Zavala Reyes 2015 #205 (AM)]", "forma_fuente": "quibaquibi", "notas": "Zavala Reyes 2015 #205 (AM)"},
    "kiboata":       {"sig": "engañar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar [Zavala Reyes 2015 #206 (AM)]", "forma_fuente": "quiboata", "notas": "Zavala Reyes 2015 #206 (AM)"},
    "kidiboata":     {"sig": "engañar, engañado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar, engañado [Zavala Reyes 2015 #213 (AM)]", "forma_fuente": "quidiboata", "notas": "Zavala Reyes 2015 #213 (AM)"},
    "kiwawa":        {"sig": "especie de haba grande y blanca", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de haba grande y blanca [Zavala Reyes 2015 #215 (A)]", "forma_fuente": "quiguagua", "notas": "Zavala Reyes 2015 #215 (A)"},
    "kiricias":      {"sig": "sangre, sangrado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sangre, sangrado [Zavala Reyes 2015 #217 (AM)]", "forma_fuente": "quiricias", "notas": "Zavala Reyes 2015 #217 (AM)"},
    "raporon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #220 (HB)]", "notas": "Zavala Reyes 2015 #220 (HB)"},
    "sinwanguso":    {"sig": "insolente", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insolente [Zavala Reyes 2015 #229 (PMA)]", "forma_fuente": "singuanguso", "notas": "Zavala Reyes 2015 #229 (PMA)"},
    "surupa":        {"sig": "blatta orientalis. Cucaracha", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Blatta orientalis. Cucaracha [Zavala Reyes 2015 #231 (A)]", "notas": "Zavala Reyes 2015 #231 (A)"},
    "tuba":          {"sig": "aglomeración, montón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Aglomeración, montón [Zavala Reyes 2015 #253 (E)]", "notas": "Zavala Reyes 2015 #253 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "ubeda":         {"sig": "acacia fétida. Mapurite, cují hediondo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Acacia fétida. Mapurite, cují hediondo [Zavala Reyes 2015 #266 (A)]", "notas": "Zavala Reyes 2015 #266 (A)"},
    "uray":          {"sig": "envoltura o vaina de las cerbatanas", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Envoltura o vaina de las cerbatanas [Zavala Reyes 2015 #271 (AM)]", "notas": "Zavala Reyes 2015 #271 (AM)"},
    "ure":           {"sig": "raíz", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Raíz [Zavala Reyes 2015 #272 (E)]", "notas": "Zavala Reyes 2015 #272 (E)"},
    "usera":         {"sig": "seco, arenoso", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Seco, arenoso [Zavala Reyes 2015 #275 (AM)]", "notas": "Zavala Reyes 2015 #275 (AM)"},
}


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
    "homografos": 4,
    "homografos_disueltos_d5": 9,
    "colisiones_d5": 2,
    "toponimos": 45,
    "antroponimos": 14,
    "descartados": 4,
    "ya_en_lexicon_antes_del_import": 72,
    "entradas_pdf": 288,
}
