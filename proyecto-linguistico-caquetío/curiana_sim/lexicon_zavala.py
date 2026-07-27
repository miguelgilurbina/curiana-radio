"""
CURIANA — Glosario de Zavala Reyes (2015), importado por tiers
==============================================================

GENERADO por `minar_zavala_glosario.py` — no editar a mano: reejecutar el
script si cambia la curación. Fuente:

    Zavala Reyes, Miguel Enrique (2015). "Palabras vivas de una lengua
    muerta: legado arawak-caquetío". Boletín Antropológico 33(89), pp. 58-76.
    Universidad de Los Andes. → fuentes_caquetios/

MOTIVO (auditoría 2026-07-20): el lexicón contenía solo ~66 de las 286
entradas del glosario (23%). Faltaban palabras que el propio proyecto usa
como nombre de agente (buio, bagre, cunaro, guaranaro, dara, naure) — que
por tanto NO puntuaban como caquetío — y ocho afijos atestiguados ausentes
de las reglas morfológicas.

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
    "bagre":         {"sig": "pez", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #21 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "buio":          {"sig": "serpiente, boa, diablo, dios del mal", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #48 (AM)"},
    "cuna":          {"sig": "pez del golfete de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #95 (E)"},
    "cunaro":        {"sig": "pez del golfete de Coro. Promicops Guasa", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #96 (E)"},
    "dara":          {"sig": "alcaraván", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #102 (HB+E)"},
    "guaranaro":     {"sig": "pez lisa", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #139 (HB+E)"},
    "naure":         {"sig": "jojoto", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #185 (E)"},
    "naure":         {"sig": "planta bejucosa", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #186 (E)"},

    # ── T3 — sustantivos concretos: fauna, flora, paisaje, técnica ──
    # Varios cierran 'huecos léxicos' que ecologia_lexicon_map.md daba por vacíos
    # (taques=salina, bisure=lagartija, chaguanco=zorro, jachos=teas de pesca).
    "aco":           {"sig": "comida. Par, casal, pareja", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #4 (E+AM); homógrafo con español — resuelto por contexto en score_linguistico; variantes: aca"},
    "arata":         {"sig": "mono", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #13 (AM)"},
    "arica":         {"sig": "árbol de jícara o totumo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #14 (AM)"},
    "bacoa":         {"sig": "bosque, lugar, paraje, sitio fértil", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #18 (AM+E)"},
    "bajareque":     {"sig": "tabico hecho de tierra palos y bejuco", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #24 (AM)"},
    "barabara":      {"sig": "árbol de madera dura y pesada. Olivo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #30 (A)"},
    "barbasco":      {"sig": "hierba de borrachera", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #32 (HB)"},
    "bisure":        {"sig": "lagartija", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #41 (HB+E)"},
    "buche":         {"sig": "planta xerofita, melocato, cardo globoso, rastrero", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #45 (AM+E); variantes: buchi"},
    "cabana":        {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #51 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "cacuro":        {"sig": "pequeña avispa negra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #54 (E+A)"},
    "camaroa":       {"sig": "árbol lactescente, de hojas parecidas al papayo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #56 (A)"},
    "capubana":      {"sig": "duende del cerro", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #61 (HB)"},
    "caquetillo":    {"sig": "árbol. Madera de construcción, resistente a la humedad", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #63 (E+A)"},
    "carapa":        {"sig": "árbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #65 (E)"},
    "caruca":        {"sig": "paja, da consistencia al barro que se aplica a paredes y techos", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #67 (E)"},
    "caseto":        {"sig": "planta herbácea", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #68 (E)"},
    "casquito":      {"sig": "agrio, fermentado", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #69 (HB)"},
    "caujaro":       {"sig": "árbol de madera blanda, fruta mucilaginosa, del género cordia", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #72 (E)"},
    "cayude":        {"sig": "árbol frutal, guanábano silvestre, turagua", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #73 (E)"},
    "cegue":         {"sig": "lechuza", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #78 (HB)"},
    "chaguanco":     {"sig": "zorro", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #80 (A)"},
    "chaure":        {"sig": "cegue. Lechuza que anida en cuevas de terrenos arenosos", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #81 (HB+E)"},
    "chipare":       {"sig": "matapalo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #82 (E)"},
    "chirgua":       {"sig": "tinaja pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #83 (HB)"},
    "cocuy":         {"sig": "penca. Planta rizomoza que da un vino agradable", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #87 (HB+CGB+A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "coques":        {"sig": "hormiga roja", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #89 (HB)"},
    "cuiva":         {"sig": "piedra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #92 (PMA); variantes: kiba"},
    "curari":        {"sig": "árbol de roble, tecoma", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #97 (E)"},
    "dabuda":        {"sig": "barro loza", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #99 (HB+E)"},
    "dacagua":       {"sig": "árbol de corteza gris, madera compacta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #101 (A)"},
    "dato":          {"sig": "fruto del cardón", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #105 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "dipopo":        {"sig": "fibra de cocuiza, cabuya", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #109 (AM)"},
    "ditero":        {"sig": "insecto, hormiga que daña", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #110 (AM)"},
    "dividive":      {"sig": "árbol cuyo fruto es una baya que da tinta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #112 (E)"},
    "ebo":           {"sig": "camino, paso, senda", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #117 (E)"},
    "enea":          {"sig": "planta ciperácea", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #118 (A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "guaca":         {"sig": "ave, cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #123 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "guache":        {"sig": "murciélago, zorro blanco", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #125 (E+AM)"},
    "guaco":         {"sig": "planta herbácea de la familia de las portulacea", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #126 (E)"},
    "guacoa":        {"sig": "paloma", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #127 (HB)"},
    "guacuaro":      {"sig": "palo de tinte", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #128 (A+AM)"},
    "guairon":       {"sig": "hoguera", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #132 (HB)"},
    "guamacho":      {"sig": "árbol cactáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #134 (A+E)"},
    "guarataro":     {"sig": "barro de loza, para la fábrica de budares y ollas", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #141 (E)"},
    "guariana":      {"sig": "arbusto halófilo, frailejón de la playa. Tabaco pescador", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #142 (E)"},
    "guaru":         {"sig": "v olturido, cataneja. Ave mayor que el zamuro", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #143 (E)"},
    "guata":         {"sig": "planta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #146 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "guay":          {"sig": "árbol parecido a la ceiba", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #147 (E+A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "harifuche":     {"sig": "maíz tostado y miel", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #153 (HB)"},
    "huaymujo":      {"sig": "pequeño cangrejo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #158 (E)"},
    "humohumo":      {"sig": "el ave que vuela", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #160 (AM)"},
    "igui":          {"sig": "árbol, matapalo, paují", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #164 (E)"},
    "isiro":         {"sig": "árbol corpulento sapindáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #167 (A)"},
    "jachos":        {"sig": "teas de madera, para encandilar en las labores de pesca nocturna", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #169 (E)"},
    "jajato":        {"sig": "chloris Radiata. Yerba forrajera. Lugar de arena", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #176 (A+AM)"},
    "judereque":     {"sig": "árbol ramoso, parecido al chiguare", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #177 (E)"},
    "jusual":        {"sig": "sembrar, siembra, sembradío. Conuco", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #180 (AM)"},
    "koro":          {"sig": "cotorra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #181 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "paragua":       {"sig": "mar", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #191 (GC)"},
    "paraguatan":    {"sig": "árbol maderable", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #193 (AM)"},
    "piritu":        {"sig": "palmera", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #199 (E+A+AM)"},
    "querequere":    {"sig": "ave pequeña", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #202 (AM)"},
    "quicuidi":      {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #211 (HB)"},
    "quigua":        {"sig": "concha de almeja y otros moluscos. Sitio del estado Lara", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #214 (E+AM)"},
    "quiva":         {"sig": "piedra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #218 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "ruba":          {"sig": "especie de abeja silvestre negra de Coro", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #221 (A); homógrafo con español — resuelto por contexto en score_linguistico"},
    "samuro":        {"sig": "punta hacia el mar", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #223 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "sibidigua":     {"sig": "arbusto euforbiaceo. Jatrofa Gossy Pifolia", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #226 (E+A)"},
    "supi":          {"sig": "sitio a orilla del mar. Arena. Arboleda supide", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #230 (AM+PMA); homógrafo con español — resuelto por contexto en score_linguistico"},
    "taboro":        {"sig": "serranía", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #233 (HB)"},
    "taque":         {"sig": "árbol nucífero", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #236 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "taques":        {"sig": "salina", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #237 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "taratore":      {"sig": "sabana", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #241 (AM)"},
    "tauta":         {"sig": "pequeña paloma de hábitos ictiófagos", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #244 (E)"},
    "tigua":         {"sig": "árbol rutáceo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #246 (E)"},
    "tigui":         {"sig": "pequeña paloma que se alimenta de peces", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #247 (E)"},
    "tijua":         {"sig": "paloma de canto onomatopéyico", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #248 (E)"},
    "tomatei":       {"sig": "punta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #252 (AM)"},
    "tubarao":       {"sig": "arenales", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #254 (E)"},
    "tupure":        {"sig": "siembra de cacao", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #256 (s/sigla)"},
    "tuquinemo":     {"sig": "llano, plano", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #258 (AM)"},
    "turicha":       {"sig": "ave cantadora. Flauta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #260 (AM)"},
    "turumaco":      {"sig": "cerro, meseta", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #262 (AM)"},
    "turupia":       {"sig": "árbol espinoso. Sitio en Cumarebo", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #263 (AM+A)"},
    "tuturutos":     {"sig": "hierba de propiedades eméticas. Usado para cuajar quesos", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #264 (E)"},
    "uria":          {"sig": "plantío, siembra", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #273 (AM)"},
    "yabo":          {"sig": "cercidium Virid. Arbol resinoso", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #278 (E+A+AM)"},
    "yacure":        {"sig": "árbol leguminoso de hojas perennes. Acacia. Sitio de Cabudare", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #281 (AM+E)"},
    "yagruma":       {"sig": "caracol, molusco", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #282 (A)"},
    "yapamata":      {"sig": "siembra, plantío", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #283 (AM)"},
    "yaro":          {"sig": "bejuco. Planta venenosa", "cat": "sust", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #285 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},

    # ── T4 — verbos, cualidades y abstractos ──
    # El lexicón activo es pobre en verbos y cualidades; este tier lo compensa.
    "aca":           {"sig": "bejuco", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #3 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "apo":           {"sig": "grande", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #11 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "bachure":       {"sig": "maneto, patituerto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #19 (A)"},
    "badamaro":      {"sig": "extraer, sacar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #20 (AM)"},
    "baharuco":      {"sig": "abuelo, viejo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #22 (AM)"},
    "baperon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #27 (HB)"},
    "barbache":      {"sig": "iguana", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #33 (PMA)"},
    "barique":       {"sig": "arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #35 (AM+HB)"},
    "beceremicore":  {"sig": "dominar, triunfar, victoria", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #39 (AM)"},
    "cachipo":       {"sig": "en voz vulgar, enojado, colérico", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #53 (A)"},
    "cana":          {"sig": "demonio", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #57 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "capo":          {"sig": "duende, ente sobrenatural", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #59 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "capu":          {"sig": "demonio. Señala Galeotto Cey la pronunciación “cap”", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #60 (HB)"},
    "carama":        {"sig": "ramazón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #64 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "chuchube":      {"sig": "paraulata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #85 (HB)"},
    "comoho":        {"sig": "higo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #88 (HB)"},
    "despopo":       {"sig": "fuerza", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #107 (AM)"},
    "dichiva":       {"sig": "límite, línea", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #108 (AM)"},
    "domaria":       {"sig": "enredarse, atormentar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #114 (AM)"},
    "durigua":       {"sig": "hacer trabajos cortos. 68", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #116 (AM)"},
    "etamo":         {"sig": "feroz, feo, espanto", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #120 (AM)"},
    "guaidima":      {"sig": "integro", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #131 (AM)"},
    "guamipa":       {"sig": "hueco, profundidad", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #135 (AM)"},
    "guaracaro":     {"sig": "tapirama silvestre", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #138 (E)"},
    "guaranao":      {"sig": "salado, ácido", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #140 (E)"},
    "guasima":       {"sig": "viejo, anciano", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #145 (AM)"},
    "guica":         {"sig": "yabo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #150 (E)"},
    "guide":         {"sig": "arreglar, acomodar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #151 (AM)"},
    "hay":           {"sig": "coca", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #154 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "hueque":        {"sig": "sitio de trabajo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #155 (AM)"},
    "icoroata":      {"sig": "caraota", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #162 (HB); homógrafo con español — resuelto por contexto en score_linguistico"},
    "jabal":         {"sig": "adquirir", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #168 (AM)"},
    "jadarayte":     {"sig": "recoger", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #172 (AM)"},
    "juri":          {"sig": "viento, ventarrón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #178 (E); variantes: jura"},
    "laguari":       {"sig": "acacia Espinoza, acacia. Lauadrí", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #182 (E+A+PMA)"},
    "orumo":         {"sig": "urumu. Apamate. No confundir con el Myrciacucuo llata", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #187 (A+PMA)"},
    "patapati":      {"sig": "anegadizo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #198 (AM)"},
    "popoi":         {"sig": "ahí. Adverbio de lugar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #201 (AM)"},
    "quiba":         {"sig": "ayuda", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #203 (AM); homógrafo con español — resuelto por contexto en score_linguistico"},
    "quibaquibi":    {"sig": "baquiano, conocedor", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #205 (AM)"},
    "quiboata":      {"sig": "engañar", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #206 (AM)"},
    "quidiboata":    {"sig": "engañar, engañado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #213 (AM)"},
    "quiguagua":     {"sig": "especie de haba grande y blanca", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #215 (A)"},
    "quiricias":     {"sig": "sangre, sangrado", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #217 (AM)"},
    "raporon":       {"sig": "calabaza con cal", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #220 (HB)"},
    "sigua":         {"sig": "blando", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #227 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "singuanguso":   {"sig": "insolente", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #229 (PMA)"},
    "surupa":        {"sig": "blatta orientalis. Cucaracha", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #231 (A)"},
    "tuba":          {"sig": "aglomeración, montón", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #253 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "ubeda":         {"sig": "acacia fétida. Mapurite, cují hediondo", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #266 (A)"},
    "uray":          {"sig": "envoltura o vaina de las cerbatanas", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #271 (AM)"},
    "ure":           {"sig": "raíz", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #272 (E); homógrafo con español — resuelto por contexto en score_linguistico"},
    "usera":         {"sig": "seco, arenoso. 72", "cat": "v_raiz", "fuente": "caquetío-atestiguado", "notas": "Zavala Reyes 2015 #275 (AM)"},
}


# ══════════════════════════════════════════════════════════════════
# HOMÓGRAFOS CON ESPAÑOL — se resuelven POR CONTEXTO
# ══════════════════════════════════════════════════════════════════
# Son caquetío atestiguado, pero su forma coincide con una palabra
# española corriente. Sin tratamiento, un texto en español que diga
# "el bagre" puntuaría como caquetío. score_linguistico los cuenta solo
# si un vecino inmediato es arahuaco (mismo mecanismo que ya usa 'para').

HOMOGRAFOS_ZAVALA: frozenset = frozenset({
    "aca",
    "aco",
    "apo",
    "bagre",
    "cabana",
    "cana",
    "capo",
    "carama",
    "cocuy",
    "dato",
    "enea",
    "guaca",
    "guata",
    "guay",
    "hay",
    "icoroata",
    "koro",
    "quiba",
    "quiva",
    "ruba",
    "samuro",
    "sigua",
    "supi",
    "taque",
    "taques",
    "tuba",
    "ure",
    "yaro",
})


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
    "barisi": "Región de tierras coloradas cerca del mar. 66",   # curación manual: topónimo/etnónimo o glosa incierta
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
    "chunare": "Apellido. Mazorca tierna",
    "huay": "Nombre propio",
    "quiceraguru": "Nombre propio indígena en Barquisimeto",
    "quiceroaboa": "Nombre propio indígena en Barquisimeto",
    "quiceromata": "Nombre propio indígena en Barquisimeto",
    "quiciroata": "Nombre propio indígena en Barquisimeto",
    "quiquiba": "nombre propio indígena",
    "tamani": "Nombre propio indígena. - 71",
    "timaure": "Apellido",
    "tumarure": "Apellido de un cacique",
    "xaraguamari": "Cacique de Yaracuy",
    "yarosabana": "Cacique de los Guaragua del Yaracuy. Pueblo",
    "zamurano": "nombre indígena del Yaracuy. Pueblo",
}

DESCARTADOS_ZAVALA: dict[str, str] = {
    "baquiro": "Cochino de monte. Lisandro Alvarado señala que es cumanagota",   # Zavala/compilador la marca de otra lengua
}


TOTALES = {
    "afijos": 8,
    "vocabulario_activo": 153,
    "homografos": 28,
    "toponimos": 45,
    "antroponimos": 13,
}
