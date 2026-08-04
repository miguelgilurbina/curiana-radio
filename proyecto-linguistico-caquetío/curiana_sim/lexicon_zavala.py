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
    "cuna":          {"sig": "pez del golfete de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez del golfete de Coro [Zavala Reyes 2015 #95 (E)]", "notas": "Zavala Reyes 2015 #95 (E)"},
    "cunaro":        {"sig": "pez del golfete de Coro. Promicops Guasa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez del golfete de Coro. Promicops Guasa [Zavala Reyes 2015 #96 (E)]", "identificacion_moderna": "Rhomboplites aurorubens (pargo cunaro, de altura) según SVDB. Zavala transcribe 'Promicops Guasa' (por Promicrops itajara, hoy Epinephelus itajara, el mero guasa): dos peces distintos.", "notas": "Zavala Reyes 2015 #96 (E)"},
    "dara":          {"sig": "alcaraván", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Alcaraván [Zavala Reyes 2015 #102 (HB+E)]", "notas": "Zavala Reyes 2015 #102 (HB+E)"},
    "guaranaro":     {"sig": "pez lisa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pez lisa [Zavala Reyes 2015 #139 (HB+E)]", "identificacion_moderna": "sin resolver; 'lisa' apunta a Mugil spp. (M. curema / M. incilis son las del Golfete). La hoja de fuentes 02_ecologia lo daba por 'sin identificación taxonómica firme' cuando Zavala YA lo glosaba.", "notas": "Zavala Reyes 2015 #139 (HB+E)"},
    "naure":         {"sig": "jojoto", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Jojoto [Zavala Reyes 2015 #185 (E)]", "notas": "Zavala Reyes 2015 #185 (E)"},
    "naure":         {"sig": "planta bejucosa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta bejucosa [Zavala Reyes 2015 #186 (E)]", "notas": "Zavala Reyes 2015 #186 (E)"},

    # ── T3 — sustantivos concretos: fauna, flora, paisaje, técnica ──
    # Varios cierran 'huecos léxicos' que ecologia_lexicon_map.md daba por vacíos
    # (taques=salina, bisure=lagartija, chaguanco=zorro, jachos=teas de pesca).
    "aco":           {"sig": "comida. Par, casal, pareja", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Comida. Par, casal, pareja [Zavala Reyes 2015 #4 (E+AM)]", "notas": "Zavala Reyes 2015 #4 (E+AM); variantes: aca"},
    "arata":         {"sig": "mono", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mono [Zavala Reyes 2015 #13 (AM)]", "notas": "Zavala Reyes 2015 #13 (AM)"},
    "arica":         {"sig": "árbol de jícara o totumo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de jícara o totumo [Zavala Reyes 2015 #14 (AM)]", "notas": "Zavala Reyes 2015 #14 (AM)"},
    "bacoa":         {"sig": "bosque, lugar, paraje, sitio fértil", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bosque, lugar, paraje, sitio fértil [Zavala Reyes 2015 #18 (AM+E)]", "notas": "Zavala Reyes 2015 #18 (AM+E)"},
    "bajareque":     {"sig": "tabico hecho de tierra palos y bejuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tabico hecho de tierra palos y bejuco [Zavala Reyes 2015 #24 (AM)]", "notas": "Zavala Reyes 2015 #24 (AM)"},
    "barabara":      {"sig": "árbol de madera dura y pesada. Olivo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de madera dura y pesada. Olivo [Zavala Reyes 2015 #30 (A)]", "notas": "Zavala Reyes 2015 #30 (A)"},
    "barbasco":      {"sig": "hierba de borrachera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hierba de borrachera [Zavala Reyes 2015 #32 (HB)]", "notas": "Zavala Reyes 2015 #32 (HB)"},
    "bisure":        {"sig": "lagartija", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lagartija [Zavala Reyes 2015 #41 (HB+E)]", "notas": "Zavala Reyes 2015 #41 (HB+E)"},
    "buche":         {"sig": "planta xerofita, melocato, cardo globoso, rastrero", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta xerofita, melocato, cardo globoso, rastrero [Zavala Reyes 2015 #45 (AM+E)]", "notas": "Zavala Reyes 2015 #45 (AM+E); variantes: buchi"},
    "cabana":        {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #51 (HB)]", "notas": "Zavala Reyes 2015 #51 (HB)"},
    "cacuro":        {"sig": "pequeña avispa negra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña avispa negra [Zavala Reyes 2015 #54 (E+A)]", "notas": "Zavala Reyes 2015 #54 (E+A)"},
    "camaroa":       {"sig": "árbol lactescente, de hojas parecidas al papayo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol lactescente, de hojas parecidas al papayo [Zavala Reyes 2015 #56 (A)]", "notas": "Zavala Reyes 2015 #56 (A)"},
    "capubana":      {"sig": "duende del cerro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende del cerro [Zavala Reyes 2015 #61 (HB)]", "notas": "Zavala Reyes 2015 #61 (HB)"},
    "caquetillo":    {"sig": "árbol. Madera de construcción, resistente a la humedad", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol. Madera de construcción, resistente a la humedad [Zavala Reyes 2015 #63 (E+A)]", "notas": "Zavala Reyes 2015 #63 (E+A)"},
    "carapa":        {"sig": "árbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol resinoso [Zavala Reyes 2015 #65 (E)]", "notas": "Zavala Reyes 2015 #65 (E)"},
    "caruca":        {"sig": "paja, da consistencia al barro que se aplica a paredes y techos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paja, da consistencia al barro que se aplica a paredes y techos [Zavala Reyes 2015 #67 (E)]", "notas": "Zavala Reyes 2015 #67 (E)"},
    "caseto":        {"sig": "planta herbácea", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta herbácea [Zavala Reyes 2015 #68 (E)]", "notas": "Zavala Reyes 2015 #68 (E)"},
    "casquito":      {"sig": "agrio, fermentado", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Agrio, fermentado [Zavala Reyes 2015 #69 (HB)]", "notas": "Zavala Reyes 2015 #69 (HB)"},
    "caujaro":       {"sig": "árbol de madera blanda, fruta mucilaginosa, del género cordia", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de madera blanda, fruta mucilaginosa, del género cordia [Zavala Reyes 2015 #72 (E)]", "notas": "Zavala Reyes 2015 #72 (E)"},
    "cayude":        {"sig": "árbol frutal, guanábano silvestre, turagua", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol frutal, guanábano silvestre, turagua [Zavala Reyes 2015 #73 (E)]", "notas": "Zavala Reyes 2015 #73 (E)"},
    "cegue":         {"sig": "lechuza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Lechuza [Zavala Reyes 2015 #78 (HB)]", "notas": "Zavala Reyes 2015 #78 (HB)"},
    "chaguanco":     {"sig": "zorro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Zorro [Zavala Reyes 2015 #80 (A)]", "notas": "Zavala Reyes 2015 #80 (A)"},
    "chaure":        {"sig": "cegue. Lechuza que anida en cuevas de terrenos arenosos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cegue. Lechuza que anida en cuevas de terrenos arenosos [Zavala Reyes 2015 #81 (HB+E)]", "notas": "Zavala Reyes 2015 #81 (HB+E)"},
    "chipare":       {"sig": "matapalo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Matapalo [Zavala Reyes 2015 #82 (E)]", "notas": "Zavala Reyes 2015 #82 (E)"},
    "chirgua":       {"sig": "tinaja pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tinaja pequeña [Zavala Reyes 2015 #83 (HB)]", "notas": "Zavala Reyes 2015 #83 (HB)"},
    "cocuy":         {"sig": "penca. Planta rizomoza que da un vino agradable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Penca. Planta rizomoza que da un vino agradable [Zavala Reyes 2015 #87 (HB+CGB+A)]", "notas": "Zavala Reyes 2015 #87 (HB+CGB+A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "coques":        {"sig": "hormiga roja", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hormiga roja [Zavala Reyes 2015 #89 (HB)]", "notas": "Zavala Reyes 2015 #89 (HB)"},
    "cuiva":         {"sig": "piedra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Piedra [Zavala Reyes 2015 #92 (PMA)]", "notas": "Zavala Reyes 2015 #92 (PMA); variantes: kiba"},
    "curari":        {"sig": "árbol de roble, tecoma", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de roble, tecoma [Zavala Reyes 2015 #97 (E)]", "notas": "Zavala Reyes 2015 #97 (E)"},
    "dabuda":        {"sig": "barro loza", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Barro loza [Zavala Reyes 2015 #99 (HB+E)]", "notas": "Zavala Reyes 2015 #99 (HB+E)"},
    "dacagua":       {"sig": "árbol de corteza gris, madera compacta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol de corteza gris, madera compacta [Zavala Reyes 2015 #101 (A)]", "notas": "Zavala Reyes 2015 #101 (A)"},
    "darubana":      {"sig": "camino, vía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Camino, vía [Zavala Reyes 2015 #104 (AM)]", "notas": "Zavala Reyes 2015 #104 (AM); variantes: durabana"},
    "dato":          {"sig": "fruto del cardón", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fruto del cardón [Zavala Reyes 2015 #105 (HB)]", "notas": "Zavala Reyes 2015 #105 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "dipopo":        {"sig": "fibra de cocuiza, cabuya", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fibra de cocuiza, cabuya [Zavala Reyes 2015 #109 (AM)]", "notas": "Zavala Reyes 2015 #109 (AM)"},
    "ditero":        {"sig": "insecto, hormiga que daña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insecto, hormiga que daña [Zavala Reyes 2015 #110 (AM)]", "notas": "Zavala Reyes 2015 #110 (AM)"},
    "dividive":      {"sig": "árbol cuyo fruto es una baya que da tinta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol cuyo fruto es una baya que da tinta [Zavala Reyes 2015 #112 (E)]", "notas": "Zavala Reyes 2015 #112 (E)"},
    "ebo":           {"sig": "camino, paso, senda", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Camino, paso, senda [Zavala Reyes 2015 #117 (E)]", "notas": "Zavala Reyes 2015 #117 (E)"},
    "guaca":         {"sig": "ave, cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave, cotorra [Zavala Reyes 2015 #123 (E)]", "notas": "Zavala Reyes 2015 #123 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "guache":        {"sig": "murciélago, zorro blanco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Murciélago, zorro blanco [Zavala Reyes 2015 #125 (E+AM)]", "notas": "Zavala Reyes 2015 #125 (E+AM)"},
    "guaco":         {"sig": "planta herbácea de la familia de las portulacea", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Planta herbácea de la familia de las portulacea [Zavala Reyes 2015 #126 (E)]", "notas": "Zavala Reyes 2015 #126 (E)"},
    "guacoa":        {"sig": "paloma", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paloma [Zavala Reyes 2015 #127 (HB)]", "notas": "Zavala Reyes 2015 #127 (HB)"},
    "guacuaro":      {"sig": "palo de tinte", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palo de tinte [Zavala Reyes 2015 #128 (A+AM)]", "notas": "Zavala Reyes 2015 #128 (A+AM)"},
    "guairon":       {"sig": "hoguera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hoguera [Zavala Reyes 2015 #132 (HB)]", "notas": "Zavala Reyes 2015 #132 (HB)"},
    "guamacho":      {"sig": "árbol cactáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol cactáceo [Zavala Reyes 2015 #134 (A+E)]", "notas": "Zavala Reyes 2015 #134 (A+E)"},
    "guarataro":     {"sig": "barro de loza, para la fábrica de budares y ollas", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Barro de loza, para la fábrica de budares y ollas [Zavala Reyes 2015 #141 (E)]", "notas": "Zavala Reyes 2015 #141 (E)"},
    "guariana":      {"sig": "arbusto halófilo, frailejón de la playa. Tabaco pescador", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arbusto halófilo, frailejón de la playa. Tabaco pescador [Zavala Reyes 2015 #142 (E)]", "notas": "Zavala Reyes 2015 #142 (E)"},
    "guaru":         {"sig": "volturido, cataneja. Ave mayor que el zamuro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Volturido, cataneja. Ave mayor que el zamuro [Zavala Reyes 2015 #143 (E)]", "notas": "Zavala Reyes 2015 #143 (E)"},
    "guay":          {"sig": "árbol parecido a la ceiba", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol parecido a la ceiba [Zavala Reyes 2015 #147 (E+A)]", "notas": "Zavala Reyes 2015 #147 (E+A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "harifuche":     {"sig": "maíz tostado y miel", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maíz tostado y miel [Zavala Reyes 2015 #153 (HB)]", "notas": "Zavala Reyes 2015 #153 (HB)"},
    "huaymujo":      {"sig": "pequeño cangrejo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeño cangrejo [Zavala Reyes 2015 #158 (E)]", "notas": "Zavala Reyes 2015 #158 (E)"},
    "humohumo":      {"sig": "el ave que vuela", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "El ave que vuela [Zavala Reyes 2015 #160 (AM)]", "notas": "Zavala Reyes 2015 #160 (AM)"},
    "igui":          {"sig": "árbol, matapalo, paují", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol, matapalo, paují [Zavala Reyes 2015 #164 (E)]", "notas": "Zavala Reyes 2015 #164 (E)"},
    "isiro":         {"sig": "árbol corpulento sapindáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol corpulento sapindáceo [Zavala Reyes 2015 #167 (A)]", "notas": "Zavala Reyes 2015 #167 (A)"},
    "jachos":        {"sig": "teas de madera, para encandilar en las labores de pesca nocturna", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Teas de madera, para encandilar en las labores de pesca nocturna [Zavala Reyes 2015 #169 (E)]", "notas": "Zavala Reyes 2015 #169 (E)"},
    "jajato":        {"sig": "chloris Radiata. Yerba forrajera. Lugar de arena", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Chloris Radiata. Yerba forrajera. Lugar de arena [Zavala Reyes 2015 #176 (A+AM)]", "notas": "Zavala Reyes 2015 #176 (A+AM)"},
    "judereque":     {"sig": "árbol ramoso, parecido al chiguare", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol ramoso, parecido al chiguare [Zavala Reyes 2015 #177 (E)]", "notas": "Zavala Reyes 2015 #177 (E)"},
    "jusual":        {"sig": "sembrar, siembra, sembradío. Conuco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sembrar, siembra, sembradío. Conuco [Zavala Reyes 2015 #180 (AM)]", "notas": "Zavala Reyes 2015 #180 (AM)"},
    "koro":          {"sig": "cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cotorra [Zavala Reyes 2015 #181 (HB)]", "notas": "Zavala Reyes 2015 #181 (HB)"},
    "paragua":       {"sig": "mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Mar [Zavala Reyes 2015 #191 (GC)]", "notas": "Zavala Reyes 2015 #191 (GC)"},
    "paraguatan":    {"sig": "árbol maderable", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol maderable [Zavala Reyes 2015 #193 (AM)]", "notas": "Zavala Reyes 2015 #193 (AM)"},
    "piritu":        {"sig": "palmera", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Palmera [Zavala Reyes 2015 #199 (E+A+AM)]", "notas": "Zavala Reyes 2015 #199 (E+A+AM)"},
    "querequere":    {"sig": "ave pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave pequeña [Zavala Reyes 2015 #202 (AM)]", "notas": "Zavala Reyes 2015 #202 (AM)"},
    "quicuidi":      {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #211 (HB)]", "notas": "Zavala Reyes 2015 #211 (HB)"},
    "quigua":        {"sig": "concha de almeja y otros moluscos. Sitio del estado Lara", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Concha de almeja y otros moluscos. Sitio del estado Lara [Zavala Reyes 2015 #214 (E+AM)]", "notas": "Zavala Reyes 2015 #214 (E+AM)"},
    "quiva":         {"sig": "piedra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Piedra [Zavala Reyes 2015 #218 (E)]", "notas": "Zavala Reyes 2015 #218 (E)"},
    "ruba":          {"sig": "especie de abeja silvestre negra de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de abeja silvestre negra de Coro [Zavala Reyes 2015 #221 (A)]", "notas": "Zavala Reyes 2015 #221 (A)"},
    "samuro":        {"sig": "punta hacia el mar", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta hacia el mar [Zavala Reyes 2015 #223 (AM)]", "notas": "Zavala Reyes 2015 #223 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "sibidigua":     {"sig": "arbusto euforbiaceo. Jatrofa Gossy Pifolia", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arbusto euforbiaceo. Jatrofa Gossy Pifolia [Zavala Reyes 2015 #226 (E+A)]", "notas": "Zavala Reyes 2015 #226 (E+A)"},
    "supi":          {"sig": "sitio a orilla del mar. Arena. Arboleda supide", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio a orilla del mar. Arena. Arboleda supide [Zavala Reyes 2015 #230 (AM+PMA)]", "notas": "Zavala Reyes 2015 #230 (AM+PMA)"},
    "taboro":        {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Serranía [Zavala Reyes 2015 #233 (HB)]", "notas": "Zavala Reyes 2015 #233 (HB)"},
    "taque":         {"sig": "árbol nucífero", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol nucífero [Zavala Reyes 2015 #236 (E)]", "notas": "Zavala Reyes 2015 #236 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "taques":        {"sig": "salina", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Salina [Zavala Reyes 2015 #237 (AM)]", "notas": "Zavala Reyes 2015 #237 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "taratore":      {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sabana [Zavala Reyes 2015 #241 (AM)]", "notas": "Zavala Reyes 2015 #241 (AM)"},
    "tauta":         {"sig": "pequeña paloma de hábitos ictiófagos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña paloma de hábitos ictiófagos [Zavala Reyes 2015 #244 (E)]", "notas": "Zavala Reyes 2015 #244 (E)"},
    "tigua":         {"sig": "árbol rutáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol rutáceo [Zavala Reyes 2015 #246 (E)]", "notas": "Zavala Reyes 2015 #246 (E)"},
    "tigui":         {"sig": "pequeña paloma que se alimenta de peces", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Pequeña paloma que se alimenta de peces [Zavala Reyes 2015 #247 (E)]", "notas": "Zavala Reyes 2015 #247 (E)"},
    "tijua":         {"sig": "paloma de canto onomatopéyico", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paloma de canto onomatopéyico [Zavala Reyes 2015 #248 (E)]", "notas": "Zavala Reyes 2015 #248 (E)"},
    "tomatei":       {"sig": "punta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Punta [Zavala Reyes 2015 #252 (AM)]", "notas": "Zavala Reyes 2015 #252 (AM)"},
    "tubarao":       {"sig": "arenales", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arenales [Zavala Reyes 2015 #254 (E)]", "notas": "Zavala Reyes 2015 #254 (E)"},
    "tupure":        {"sig": "siembra de cacao", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra de cacao [Zavala Reyes 2015 #256 (s/sigla)]", "notas": "Zavala Reyes 2015 #256 (s/sigla)"},
    "tuquinemo":     {"sig": "llano, plano", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Llano, plano [Zavala Reyes 2015 #258 (AM)]", "notas": "Zavala Reyes 2015 #258 (AM)"},
    "turicha":       {"sig": "ave cantadora. Flauta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ave cantadora. Flauta [Zavala Reyes 2015 #260 (AM)]", "notas": "Zavala Reyes 2015 #260 (AM)"},
    "turumaco":      {"sig": "cerro, meseta", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cerro, meseta [Zavala Reyes 2015 #262 (AM)]", "notas": "Zavala Reyes 2015 #262 (AM)"},
    "turupia":       {"sig": "árbol espinoso. Sitio en Cumarebo", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol espinoso. Sitio en Cumarebo [Zavala Reyes 2015 #263 (AM+A)]", "notas": "Zavala Reyes 2015 #263 (AM+A)"},
    "tuturutos":     {"sig": "hierba de propiedades eméticas. Usado para cuajar quesos", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hierba de propiedades eméticas. Usado para cuajar quesos [Zavala Reyes 2015 #264 (E)]", "notas": "Zavala Reyes 2015 #264 (E)"},
    "uria":          {"sig": "plantío, siembra", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Plantío, siembra [Zavala Reyes 2015 #273 (AM)]", "notas": "Zavala Reyes 2015 #273 (AM)"},
    "yabo":          {"sig": "cercidium Virid. Arbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Cercidium Virid. Arbol resinoso [Zavala Reyes 2015 #278 (E+A+AM)]", "notas": "Zavala Reyes 2015 #278 (E+A+AM)"},
    "yacure":        {"sig": "árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare [Zavala Reyes 2015 #281 (AM+E)]", "notas": "Zavala Reyes 2015 #281 (AM+E)"},
    "yagruma":       {"sig": "caracol, molusco", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caracol, molusco [Zavala Reyes 2015 #282 (A)]", "notas": "Zavala Reyes 2015 #282 (A)"},
    "yapamata":      {"sig": "siembra, plantío", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Siembra, plantío [Zavala Reyes 2015 #283 (AM)]", "notas": "Zavala Reyes 2015 #283 (AM)"},
    "yaro":          {"sig": "bejuco. Planta venenosa", "cat": "sust", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bejuco. Planta venenosa [Zavala Reyes 2015 #285 (AM)]", "notas": "Zavala Reyes 2015 #285 (AM)"},

    # ── T4 — verbos, cualidades y abstractos ──
    # El lexicón activo es pobre en verbos y cualidades; este tier lo compensa.
    "aca":           {"sig": "bejuco", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Bejuco [Zavala Reyes 2015 #3 (E)]", "notas": "Zavala Reyes 2015 #3 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "apo":           {"sig": "grande", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Grande [Zavala Reyes 2015 #11 (AM)]", "notas": "Zavala Reyes 2015 #11 (AM)"},
    "bachure":       {"sig": "maneto, patituerto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Maneto, patituerto [Zavala Reyes 2015 #19 (A)]", "notas": "Zavala Reyes 2015 #19 (A)"},
    "badamaro":      {"sig": "extraer, sacar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Extraer, sacar [Zavala Reyes 2015 #20 (AM)]", "notas": "Zavala Reyes 2015 #20 (AM)"},
    "baharuco":      {"sig": "abuelo, viejo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Abuelo, viejo [Zavala Reyes 2015 #22 (AM)]", "notas": "Zavala Reyes 2015 #22 (AM)"},
    "baperon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #27 (HB)]", "notas": "Zavala Reyes 2015 #27 (HB)"},
    "barbache":      {"sig": "iguana", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Iguana [Zavala Reyes 2015 #33 (PMA)]", "notas": "Zavala Reyes 2015 #33 (PMA)"},
    "barique":       {"sig": "arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija [Zavala Reyes 2015 #35 (AM+HB)]", "notas": "Zavala Reyes 2015 #35 (AM+HB)"},
    "beceremicore":  {"sig": "dominar, triunfar, victoria", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Dominar, triunfar, victoria [Zavala Reyes 2015 #39 (AM)]", "notas": "Zavala Reyes 2015 #39 (AM)"},
    "cachipo":       {"sig": "en voz vulgar, enojado, colérico", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "En voz vulgar, enojado, colérico [Zavala Reyes 2015 #53 (A)]", "notas": "Zavala Reyes 2015 #53 (A)"},
    "cana":          {"sig": "demonio", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio [Zavala Reyes 2015 #57 (HB)]", "notas": "Zavala Reyes 2015 #57 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "capo":          {"sig": "duende, ente sobrenatural", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Duende, ente sobrenatural [Zavala Reyes 2015 #59 (E)]", "notas": "Zavala Reyes 2015 #59 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "capu":          {"sig": "demonio. Señala Galeotto Cey la pronunciación “cap”", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Demonio. Señala Galeotto Cey la pronunciación “cap” [Zavala Reyes 2015 #60 (HB)]", "notas": "Zavala Reyes 2015 #60 (HB)"},
    "carama":        {"sig": "ramazón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ramazón [Zavala Reyes 2015 #64 (E)]", "notas": "Zavala Reyes 2015 #64 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "chuchube":      {"sig": "paraulata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Paraulata [Zavala Reyes 2015 #85 (HB)]", "notas": "Zavala Reyes 2015 #85 (HB)"},
    "comoho":        {"sig": "higo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Higo [Zavala Reyes 2015 #88 (HB)]", "notas": "Zavala Reyes 2015 #88 (HB)"},
    "despopo":       {"sig": "fuerza", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Fuerza [Zavala Reyes 2015 #107 (AM)]", "notas": "Zavala Reyes 2015 #107 (AM)"},
    "dichiva":       {"sig": "límite, línea", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Límite, línea [Zavala Reyes 2015 #108 (AM)]", "notas": "Zavala Reyes 2015 #108 (AM)"},
    "domaria":       {"sig": "enredarse, atormentar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Enredarse, atormentar [Zavala Reyes 2015 #114 (AM)]", "notas": "Zavala Reyes 2015 #114 (AM)"},
    "durigua":       {"sig": "hacer trabajos cortos", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hacer trabajos cortos [Zavala Reyes 2015 #116 (AM)]", "notas": "Zavala Reyes 2015 #116 (AM)"},
    "etamo":         {"sig": "feroz, feo, espanto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Feroz, feo, espanto [Zavala Reyes 2015 #120 (AM)]", "notas": "Zavala Reyes 2015 #120 (AM)"},
    "guaidima":      {"sig": "integro", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Integro [Zavala Reyes 2015 #131 (AM)]", "notas": "Zavala Reyes 2015 #131 (AM)"},
    "guamipa":       {"sig": "hueco, profundidad", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Hueco, profundidad [Zavala Reyes 2015 #135 (AM)]", "notas": "Zavala Reyes 2015 #135 (AM)"},
    "guaracaro":     {"sig": "tapirama silvestre", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Tapirama silvestre [Zavala Reyes 2015 #138 (E)]", "notas": "Zavala Reyes 2015 #138 (E)"},
    "guaranao":      {"sig": "salado, ácido", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Salado, ácido [Zavala Reyes 2015 #140 (E)]", "notas": "Zavala Reyes 2015 #140 (E)"},
    "guasima":       {"sig": "viejo, anciano", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Viejo, anciano [Zavala Reyes 2015 #145 (AM)]", "notas": "Zavala Reyes 2015 #145 (AM)"},
    "guica":         {"sig": "yabo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Yabo [Zavala Reyes 2015 #150 (E)]", "notas": "Zavala Reyes 2015 #150 (E)"},
    "guide":         {"sig": "arreglar, acomodar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Arreglar, acomodar [Zavala Reyes 2015 #151 (AM)]", "notas": "Zavala Reyes 2015 #151 (AM)"},
    "hueque":        {"sig": "sitio de trabajo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sitio de trabajo [Zavala Reyes 2015 #155 (AM)]", "notas": "Zavala Reyes 2015 #155 (AM)"},
    "icoroata":      {"sig": "caraota", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Caraota [Zavala Reyes 2015 #162 (HB)]", "notas": "Zavala Reyes 2015 #162 (HB)"},
    "jabal":         {"sig": "adquirir", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Adquirir [Zavala Reyes 2015 #168 (AM)]", "notas": "Zavala Reyes 2015 #168 (AM)"},
    "jadarayte":     {"sig": "recoger", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Recoger [Zavala Reyes 2015 #172 (AM)]", "notas": "Zavala Reyes 2015 #172 (AM)"},
    "juri":          {"sig": "viento, ventarrón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Viento, ventarrón [Zavala Reyes 2015 #178 (E)]", "notas": "Zavala Reyes 2015 #178 (E); variantes: jura"},
    "laguari":       {"sig": "acacia Espinoza, acacia. Lauadrí", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Acacia Espinoza, acacia. Lauadrí [Zavala Reyes 2015 #182 (E+A+PMA)]", "notas": "Zavala Reyes 2015 #182 (E+A+PMA)"},
    "orumo":         {"sig": "urumu. Apamate. No confundir con el Myrciacucuo llata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Urumu. Apamate. No confundir con el Myrciacucuo llata [Zavala Reyes 2015 #187 (A+PMA)]", "notas": "Zavala Reyes 2015 #187 (A+PMA)"},
    "patapati":      {"sig": "anegadizo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Anegadizo [Zavala Reyes 2015 #198 (AM)]", "notas": "Zavala Reyes 2015 #198 (AM)"},
    "popoi":         {"sig": "ahí. Adverbio de lugar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ahí. Adverbio de lugar [Zavala Reyes 2015 #201 (AM)]", "notas": "Zavala Reyes 2015 #201 (AM)"},
    "quiba":         {"sig": "ayuda", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Ayuda [Zavala Reyes 2015 #203 (AM)]", "notas": "Zavala Reyes 2015 #203 (AM)"},
    "quibaquibi":    {"sig": "baquiano, conocedor", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Baquiano, conocedor [Zavala Reyes 2015 #205 (AM)]", "notas": "Zavala Reyes 2015 #205 (AM)"},
    "quiboata":      {"sig": "engañar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar [Zavala Reyes 2015 #206 (AM)]", "notas": "Zavala Reyes 2015 #206 (AM)"},
    "quidiboata":    {"sig": "engañar, engañado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Engañar, engañado [Zavala Reyes 2015 #213 (AM)]", "notas": "Zavala Reyes 2015 #213 (AM)"},
    "quiguagua":     {"sig": "especie de haba grande y blanca", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Especie de haba grande y blanca [Zavala Reyes 2015 #215 (A)]", "notas": "Zavala Reyes 2015 #215 (A)"},
    "quiricias":     {"sig": "sangre, sangrado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Sangre, sangrado [Zavala Reyes 2015 #217 (AM)]", "notas": "Zavala Reyes 2015 #217 (AM)"},
    "raporon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Calabaza con cal [Zavala Reyes 2015 #220 (HB)]", "notas": "Zavala Reyes 2015 #220 (HB)"},
    "sigua":         {"sig": "blando", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Blando [Zavala Reyes 2015 #227 (E)]", "notas": "Zavala Reyes 2015 #227 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "singuanguso":   {"sig": "insolente", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "glosa_fuente": "Insolente [Zavala Reyes 2015 #229 (PMA)]", "notas": "Zavala Reyes 2015 #229 (PMA)"},
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
    "aca",
    "bagre",
    "cana",
    "capo",
    "carama",
    "cocuy",
    "dato",
    "guaca",
    "guay",
    "samuro",
    "sigua",
    "taque",
    "taques",
    "tuba",
})


# Veredicto por forma, para que la marca sea auditable y no un acto de fe.
VEREDICTO_HOMOGRAFOS: dict[str, str] = {
    "aca": "#3 (E) 'bejuco'. Caquetía. Colisiona con 'acá' si se escribe sin tilde.",
    "bagre": "#21 (AM) 'pez'. Caquetía según la fuente; el 'bagre' español es a su vez indigenismo. Colisión real.",
    "cana": "#57 (HB) 'demonio'. Caquetía; colisiona con 'cana'/'caña'.",
    "capo": "#59 (E) 'duende'. Caquetía (cf. #60 capu 'demonio'); colisión menor con 'capo'.",
    "carama": "#64 (E) 'ramazón'. Caquetía; 'carama' existe en español rural (escarcha).",
    "cocuy": "#87 'penca; planta que da un vino'. Indigenismo de circulación pan-venezolana: ATRIBUCIÓN DÉBIL además de homógrafo.",
    "dato": "#105 (HB) 'fruto del cardón'. Caquetía, pero 'dato' es altísima frecuencia en español: la marca es imprescindible.",
    "guaca": "#123 (E) 'ave, cotorra'. Caquetía; 'guaca' español (quechua, tesoro) es otra cosa.",
    "guay": "#147 (E)(A) 'árbol parecido a la ceiba'. Caquetía; colisiona con la interjección.",
    "samuro": "#223 (AM) 'punta hacia el mar'. La forma coincide con 'zamuro' (zoónimo venezolano) y la glosa es geográfica: ATRIBUCIÓN DÉBIL.",
    "sigua": "#227 (E) 'blando'. Caquetía; 'sigua' antillano es otra cosa.",
    "taque": "#236 (E) 'árbol nucífero'. Caquetía; 'taque' español es regional y raro.",
    "taques": "#237 (AM) 'salina'. Es también el topónimo Los Taques (Paraguaná): la glosa es la etimología del lugar. ATRIBUCIÓN DÉBIL.",
    "tuba": "#253 (E) 'aglomeración, montón'. Caquetía; colisiona con 'tuba'.",
}


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
    "vocabulario_activo": 151,
    "homografos": 14,
    "toponimos": 45,
    "antroponimos": 14,
    "descartados": 4,
    "ya_en_lexicon_antes_del_import": 66,
    "entradas_pdf": 288,
}
