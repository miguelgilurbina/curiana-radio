#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — barrer el mapa vivo de la Kaketiana (OpenStreetMap)
=============================================================

El método está en la skill `campana-toponimos` §9: una lista de nombres del
mapa vivo con coordenadas, por región; cruzarla con la mesa de la campaña; lo
que no está en ninguna fuente es lo nuevo y entra a la cola con deuda; lo
castellano se filtra antes de segmentar y se registra aparte.

La fuente es OpenStreetMap vía Overpass (Miguel lo decidió el 2026-09-07:
«vamos con OSM»). Licencia ODbL: © los colaboradores de OpenStreetMap. Las
cuatro regiones son las de `3-mundo/asentamientos.yaml`: paraguana,
golfete-de-coro, falcon-occidental, islas-abc.

Lo que este script NO hace: decidir nivel, glosa ni etimología de nada. Es
un inventario cruzado. Regla 5: propone; el humano fusiona. Regla 3: un
nombre vivo en el mapa de 2026 es época moderna hasta que un documento lo
lleve atrás. Regla 4: un nombre de Falcón occidental no es de la polity
costera sin decirlo — por eso cada entrada lleva su región.

Uso:
    python barrer_mapa.py --descargar   # Overpass → fuentes_caquetios/osm_kaketiana/*.json
    python barrer_mapa.py               # compila 6-fusion/toponimos_mapa_kaketiana.yaml + informe
    python barrer_mapa.py --lote        # imprime lo nuevo por región (lo que no está en ninguna fuente)
"""

import argparse
import datetime as dt
import io
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict

import yaml

_AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(_AQUI)
CRUDO_DIR = os.path.join(REPO, "fuentes_caquetios", "osm_kaketiana")
SALIDA = os.path.join(REPO, "6-fusion", "toponimos_mapa_kaketiana.yaml")
MESA = os.path.join(REPO, "6-fusion", "toponimos_por_fuente.yaml")
OVERPASS = "https://overpass-api.de/api/interpreter"
AGENTE = "curiana-radio/barrer_mapa (proyecto-linguistico-caquetio; contacto en el repo)"

# Cajas (S, W, N, E). Medidas a ojo sobre el mapa el 2026-09-07; si una
# región queda corta, se amplía aquí y se vuelve a descargar.
REGIONES = {
    "paraguana": [(11.55, -70.35, 12.25, -69.65)],
    "golfete-de-coro": [(11.25, -70.10, 11.55, -69.25)],
    "falcon-occidental": [(10.55, -71.05, 11.45, -70.10)],
    "islas-abc": [(12.40, -70.08, 12.65, -69.85),    # Aruba
                  (11.97, -69.18, 12.42, -68.72),    # Curazao
                  (12.00, -68.44, 12.33, -68.18)],   # Bonaire
}

# Qué etiquetas OSM se convierten en qué `tipo` del inventario. Lo que no
# está aquí se descarta (muelles, plazas, estados…) y se cuenta.
TIPOS = {
    ("place", "city"): "poblado", ("place", "town"): "poblado",
    ("place", "village"): "poblado", ("place", "hamlet"): "caserío",
    ("place", "locality"): "lugar", ("place", "neighbourhood"): "sector",
    ("place", "suburb"): "sector", ("place", "farm"): "fundo",
    ("place", "isolated_dwelling"): "casa", ("place", "island"): "isla",
    ("place", "islet"): "islote", ("place", "quarter"): "sector",
    ("natural", "peak"): "cerro", ("natural", "hill"): "cerro",
    ("natural", "ridge"): "fila", ("natural", "saddle"): "abra",
    ("natural", "valley"): "valle", ("natural", "cape"): "punta",
    ("natural", "bay"): "bahía", ("natural", "beach"): "playa",
    ("natural", "water"): "laguna", ("natural", "wetland"): "ciénaga",
    ("natural", "spring"): "manantial", ("natural", "dune"): "médano",
    ("natural", "sand"): "arenal", ("natural", "peninsula"): "península",
    ("natural", "cliff"): "farallón", ("natural", "reef"): "arrecife",
    ("natural", "shoal"): "bajo", ("natural", "strait"): "boca",
    ("natural", "rock"): "piedra", ("natural", "stone"): "piedra",
    ("natural", "wood"): "monte", ("natural", "scrub"): "monte",
    ("waterway", "stream"): "quebrada", ("waterway", "river"): "río",
    ("waterway", "canal"): "caño", ("waterway", "ditch"): "caño",
    ("landuse", "salt_pond"): "salina",
}

# Genéricos castellanos que van delante del nombre propio. Se quitan antes de
# clasificar y de cruzar: «Cerro Tausabana» cruza como «tausabana».
GENERICOS = {
    "el", "la", "los", "las", "de", "del", "de la", "de los", "de las", "y",
    "cerro", "cerros", "cerrito", "punta", "cabo", "bahia", "bahía", "playa",
    "playita", "quebrada", "rio", "río", "laguna", "lagunita", "salina",
    "salinas", "saladillo", "hato", "puerto", "boca", "ensenada", "isla",
    "islote", "cayo", "cano", "caño", "loma", "lomas", "sabana", "sabanas",
    "sierra", "fila", "morro", "monte", "pico", "bajo", "alto", "medano",
    "médano", "medanos", "médanos", "urbanizacion", "urbanización", "sector",
    "barrio", "caserio", "caserío", "fundo", "hacienda", "finca", "hato",
    "san", "santa", "santo", "villa", "pueblo", "ciudad", "km", "kilometro",
    "kilómetro", "paso", "cruce", "vuelta", "distribuidor", "club",
}

# Palabras castellanas frecuentes en topónimos. Un nombre cuyas palabras
# (sin genéricos) están TODAS aquí es castellano y se registra aparte.
CASTELLANO = {
    "nuevo", "nueva", "nuevos", "nuevas", "viejo", "vieja", "grande", "chico",
    "chica", "chiquito", "pequeño", "blanco", "blanca", "negro", "negra",
    "colorado", "colorada", "verde", "azul", "amarillo", "rojo", "prieto",
    "alto", "alta", "bajo", "baja", "arriba", "abajo", "norte", "sur", "este",
    "oeste", "centro", "medio", "media", "largo", "larga", "hondo", "honda",
    "seco", "seca", "dulce", "salado", "salada", "rico", "rica", "bonito",
    "bonita", "lindo", "linda", "bello", "bella", "buen", "buena", "buenos",
    "buenas", "vista", "esperanza", "victoria", "libertad", "union", "unión",
    "paz", "cruz", "cruces", "piedra", "piedras", "pedregal", "pedregalito",
    "arena", "arenas", "arenal", "barro", "barrial", "barrialito", "agua",
    "aguas", "aguada", "aguita", "pozo", "pozos", "pocito", "jaguey",
    "jagüey", "manantial", "quebrada", "corral", "corrales", "corralito",
    "cercado", "cerca", "portachuelo", "puerta", "ventana", "casa", "casas",
    "casita", "rancho", "ranchos", "ranchito", "rincon", "rincón",
    "rinconada", "rinconcito", "valle", "vallecito", "llano", "llanito",
    "sabana", "sabaneta", "sabanita", "loma", "lomita", "cerrito", "cerrote",
    "pelon", "pelón", "atravesado", "platero", "cano", "sabino", "conejo",
    "conejal", "conejalito", "venado", "tigre", "tigrera", "zorro", "gato",
    "gatos", "perro", "perros", "burro", "burros", "chivo", "chivos", "cabra",
    "cabras", "vaca", "vacas", "toro", "toros", "caballo", "yegua", "gallo",
    "gallina", "paloma", "palomas", "palomar", "loro", "loros", "garza",
    "garzas", "pelicano", "pelícano", "alcatraz", "iguana", "tortuga",
    "culebra", "culebras", "cangrejo", "pescado", "pescadores", "pescador",
    "carbon", "carbón", "cal", "caliza", "cocuy", "cardon", "cardón",
    "cardones", "cardonal", "cardonales", "cuji", "cují", "cujies", "cujíes",
    "cujisal", "cujizal", "tuna", "tunas", "tunal", "yabo", "yabal", "yabos",
    "dividive", "dividivi", "dividivales", "mangle", "mangles", "manglar",
    "manglares", "manglito", "uvero", "uveros", "uva", "uvas", "cocotero",
    "coco", "cocos", "palma", "palmas", "palmar", "palmita", "palmarito",
    "guamache", "guamacho", "guamachal", "taparo", "taparito", "guacimo",
    "guácimo", "jobo", "jobal", "jobito", "mamon", "mamón", "mamonal",
    "guanabano", "guanábano", "aceituno", "aceitunos", "cerezo", "olivo",
    "olivos", "naranjo", "naranjal", "limon", "limón", "limonal", "tamarindo",
    "tamarindos", "almendro", "almendron", "almendrón", "ceiba", "ceibal",
    "ceibita", "roble", "robles", "cedro", "cedros", "pino", "pinos",
    "guayabo", "guayabal", "guayabito", "carrizal", "carrizo", "bejuco",
    "bejucal", "espino", "espinal", "espinito", "cactus", "brasil", "brasilito",
    "cairo", "berlin", "berlín", "paris", "parís", "aires", "carmen",
    "carmelo", "carmelero", "rosario", "rosa", "rosas", "isabel", "elena",
    "maria", "maría", "jose", "josé", "juan", "pedro", "pablo", "antonio",
    "francisco", "rafael", "miguel", "luis", "lucia", "lucía", "ana", "ines",
    "inés", "teresa", "barbara", "bárbara", "lorenzo", "nicolas", "nicolás",
    "cristobal", "cristóbal", "roman", "román", "vicente", "andres", "andrés",
    "felipe", "diego", "martin", "martín", "domingo", "sebastian",
    "sebastián", "gabriel", "simon", "simón", "bolivar", "bolívar",
    "sucre", "urdaneta", "falcon", "falcón", "zamora", "miranda", "colina",
    "colinas", "costa", "costanera", "cabecera", "ciudad", "pueblo", "pueblito",
    "caserio", "caserío", "estacion", "estación", "mercado", "muelle",
    "aeropuerto", "refineria", "refinería", "terminal", "puente", "cruce",
    "carretera", "camino", "vereda", "vuelta", "cementerio", "capilla",
    "iglesia", "ermita", "calvario", "cristo", "rey", "reina", "reyes",
    "santisima", "santísima", "trinidad", "concepcion", "concepción",
    "candelaria", "milagro", "milagros", "socorro", "consuelo", "carmen",
    "chimenea", "horno", "hornos", "calera", "caleras", "tejar", "tejeria",
    "alfarería", "loza", "salinero", "salinera", "gallera", "matadero",
    "botalon", "botalón", "represa", "dique", "tanque", "tanques", "molino",
    "molinos", "trapiche", "ingenio", "central", "campo", "campos",
    "campamento", "cuartel", "fuerte", "fortin", "fortín", "castillo",
    "torre", "faro", "aduana", "resguardo", "playita", "playon", "playón",
    "ensenada", "caleta", "boquete", "boca", "bocaina", "canal", "caño",
    "cienaga", "ciénaga", "cienaguita", "pantano", "charco", "charcos",
    "charcote", "salitral", "salado", "saladillo", "jardin", "jardín",
    "paraiso", "paraíso", "progreso", "porvenir", "recreo", "retiro",
    "descanso", "encanto", "amparo", "refugio", "delicias", "flores",
    "florida", "primavera", "verano", "invierno", "sol", "luna", "estrella",
    "estrellas", "cielo", "mar", "marina", "marino", "barlovento",
    "sotavento", "muerto", "muertos", "vivo", "vivos", "gordo", "gorda",
    "flaco", "flaca", "pintado", "pintada", "quemado", "quemada", "rajado",
    "rajada", "partido", "partida", "hueco", "huecos", "cueva", "cuevas",
    "cuevita", "hoyo", "hoyos", "caja", "cajon", "cajón", "mesa", "mesita",
    "tablazo", "tabla", "tablas", "silla", "sillon", "sillón", "campana",
    "campanario", "sombrero", "sombrerito", "dedo", "dedos", "mano", "cabeza",
    "pie", "pies", "diente", "dientes", "muela", "espalda", "codo", "hombro",
    "cintura", "corazon", "corazón", "ojo", "ojos", "boca", "nariz", "oreja",
    "lengua", "cuello", "pata", "patas", "cola", "colita", "cacho", "cachos",
    "cuerno", "cuernos", "pico", "picos", "cresta", "crestas", "lomo",
    "distribuidor", "kite", "badell", "pilatos", "don", "doña", "doctor",
    "general", "coronel", "capitan", "capitán", "teniente", "sargento",
    "cabo", "soldado", "padre", "madre", "hermano", "hermanos", "hermana",
    "hermanas", "hijo", "hijos", "hija", "hijas", "abuelo", "abuela", "tio",
    "tío", "tia", "tía", "primo", "primos", "compadre", "comadre", "amigo",
    "amigos", "vecino", "vecinos", "gente", "indio", "indios", "india",
    "indias", "negro", "negros", "moreno", "morenos", "mulato", "mulatos",
    "zambo", "zambos", "criollo", "criollos", "isleño", "isleños", "margariteño",
    "margariteños", "guajiro", "guajiros", "guajira", "holandes", "holandés",
    "holandesa", "frances", "francés", "ingles", "inglés", "aleman", "alemán",
    "español", "española", "portugues", "portugués", "italiano", "italiana",
    "turco", "turcos", "chino", "chinos", "arabe", "árabe", "judio", "judío",
    "libertador", "constitucion", "constitución", "independencia", "republica",
    "república", "patria", "nacion", "nación", "estado", "municipio",
    "parroquia", "distrito", "zona", "area", "área", "parque", "plaza",
    "avenida", "calle", "callejon", "callejón", "esquina", "manzana", "cuadra",
    "lote", "lotes", "parcela", "parcelas", "parcelamiento", "conjunto",
    "residencias", "residencial", "urbanismo", "vivienda", "viviendas",
    "invasion", "invasión", "asentamiento", "comunidad", "colonia",
    # lo que el primer barrido (2026-09-07) dejó pasar
    "brisas", "brisa", "cañada", "canada", "centenario", "falda", "golfete",
    "golfo", "venezuela", "guadalajara", "guadalupe", "guayaquil", "idea",
    "italia", "miramar", "mata", "matas", "mirador", "miraflores", "montalban",
    "montalbán", "palmira", "pastora", "pastor", "pauji", "paují", "angosta",
    "angosto", "tamboron", "tamborón", "tambor", "ruinas", "ruina", "caribe",
    "poza", "pozas", "prueba", "maraven", "escondido", "escondida", "caiman",
    "caimán", "culata", "barco", "barcos", "cuestion", "cuestión", "infierno",
    "fidelino", "barra", "huesa", "prudencio", "tembladal", "temblador",
    "navarrete", "rodeo", "rojiza", "rojizo", "selva", "silencio", "tres",
    "cuatro", "cinco", "dos", "marias", "marías", "valentin", "valentín",
    "zaino", "zaíno", "bomba", "california", "clavellinas", "clavellina",
    "curaridal", "curari", "doral", "enramada", "balsamar", "balsamo",
    "bálsamo", "negras", "grandes", "chicas", "chicos", "pozon", "pozón",
    "acantilados", "acantilado", "zambrano", "aguacerito", "aguacero",
    "algarrobal", "algarrobito", "algarrobo", "corozal", "corozo", "mujica",
    "alegria", "alegría", "fortuna", "providencia", "trinchera", "trincheras",
    "muralla", "murallas", "cabaña", "cabañas", "posada", "hotel", "quinta",
    "quintas", "granja", "granjas", "vivero", "criadero", "estero", "esteros",
    "cocal", "cocales", "platanal", "cañaveral", "cañamelar", "maizal",
    "yucal", "melonar", "sandial", "frijolar", "arrozal", "cafetal",
    "cacaotal", "potrero", "potreros", "corralón", "corralon", "pastizal",
    "sabanal", "chaparral", "chaparro", "chaparros", "espinar", "tunero",
    "cardonero", "salinero", "playero", "montañero", "costero", "isleta",
    "islita", "islote", "cayito", "bajito", "altico", "cerrote", "morrito",
    "picacho", "picachos", "farallon", "farallón", "farallones", "peñon",
    "peñón", "peña", "peñas", "peñita", "roca", "rocas", "laja", "lajas",
    "lajita", "cascajo", "cascajal", "arenilla", "arenoso", "arenosa",
    "barroso", "barrosa", "salitre", "salitroso", "yeso", "yesera", "cal",
    "caliche", "tierra", "tierras", "tierrita", "terreno", "terrenos",
}

# Palabras de origen indígena que el castellano de Falcón lexicalizó
# (fitónimos y zoónimos sobre todo): «Cardón Grande», «Los Cujíes», «El Yabo»
# son nombres castellanos hechos con un préstamo. Se marcan aparte para que
# nadie los tome por nombres caquetíos, y para que nadie los pierda tampoco.
VOZ_INDIGENA_LEXICALIZADA = {
    "cuji", "cují", "cujies", "cujíes", "cujisal", "cujizal", "yabo", "yabal",
    "yabos", "dividive", "dividivi", "dividivales", "guamache", "guamacho",
    "guamachal", "taparo", "taparito", "guacimo", "guácimo", "jobo", "jobal",
    "jobito", "mamon", "mamón", "mamonal", "guanabano", "guanábano", "ceiba",
    "ceibal", "ceibita", "guayabo", "guayabal", "guayabito", "bejuco",
    "bejucal", "cocuy", "tuna", "tunas", "tunal", "iguana", "jaguey", "jagüey",
    "mangle", "mangles", "manglar", "manglares", "manglito", "tabla", "tablas",
    "jagua", "jaguas", "mapora", "totumo", "totumos", "cocuiza", "cocuizal",
    "caimito", "guayacan", "guayacán", "curari", "curarí", "cardon", "cardón",
    "cardones", "cardonal", "cardonales", "guaritoto", "olivo", "chivo",
    "chivos", "conejo", "conejal",
}


def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def clave(forma: str) -> str:
    """La misma clave de cruce que `juntar_toponimos.clave`: sin tildes, sin
    artículo, solo letras."""
    f = re.sub(r"\s*\(.*?\)\s*", " ", forma).strip()
    f = re.sub(r"^(el|la|los|las)\s+", "", f, flags=re.I)
    return re.sub(r"[^a-z]", "", sin_tildes(f.lower()))


def palabras(nombre: str) -> list[str]:
    return [w for w in re.split(r"[\s\-–/,.]+", sin_tildes(nombre.lower())) if w]


def nombre_propio(nombre: str) -> str:
    """Quita los genéricos castellanos de delante y de detrás: «Cerro Tausabana»
    → «Tausabana»; «El Bajo de Supi» → «Supi»."""
    ws = palabras(nombre)
    while ws and ws[0] in GENERICOS:
        ws.pop(0)
    while len(ws) > 1 and ws[-1] in GENERICOS:
        ws.pop()
    return " ".join(ws)


# Sufijos que delatan una palabra castellana aunque no esté en la lista
# («Estanquecito», «Correría», «Pilancón», «Tembladal»). Solo se aplican a
# palabras de 6+ letras: un topónimo indígena corto no cae aquí.
SUFIJOS_CASTELLANOS = (
    "ito", "ita", "itos", "itas", "cito", "cita", "illo", "illa", "illos",
    "illas", "on", "ones", "ado", "ada", "ados", "adas", "ero", "era", "eros",
    "eras", "eria", "erias", "oso", "osa", "osos", "osas", "eño", "eña",
    "ense", "ista", "mento", "miento", "cion", "ciones", "dad", "tad", "ura",
    "eza", "anza", "ancia", "encia", "ismo", "azo", "aza", "ejo", "eja",
    "uelo", "uela", "al", "ales", "ar", "ares", "ino", "ina",
)
# Los que no siguen el sufijo: nombres indígenas que terminan como si fueran
# castellanos (Jadícuar, Cayerúa no; pero -al/-ar/-ino/-ina/-ada son
# frecuentes en la toponimia caquetía: Adícora no, pero Abudare sí acaba en
# -are). Por eso -ar/-al solo cuentan con palabra reconocida delante.
SUFIJOS_DEBILES = ("al", "ales", "ar", "ares", "ino", "ina", "ada", "adas", "on", "ones")

# Primeras palabras que hacen castellano al nombre entero: santoral y
# categorías modernas (urbanismo, vialidad).
CABEZAS_CASTELLANAS = {"san", "santa", "santo", "sector", "urbanizacion",
                       "urbanización", "urb", "retorno", "distribuidor",
                       "conjunto", "residencias", "parcelamiento", "hacienda",
                       "fundo", "finca", "hato", "club", "hotel", "posada",
                       "estacion", "estación", "aeropuerto", "refineria",
                       "refinería", "terminal", "laguna estacionaria"}

# Genéricos neerlandeses y papiamentos de las islas ABC. Se quitan antes de
# mirar el nombre propio (Seru Warawara → warawara); si lo que queda es
# neerlandés, el nombre es colonial holandés y se registra aparte.
GENERICOS_ABC = {
    "seru", "sero", "ceru", "boka", "boca", "kaya", "playa", "punt", "punta",
    "baai", "bay", "rooi", "roi", "kunuku", "tera", "hofi", "hòfi", "wela",
    "cas", "kas", "cura", "kura", "salinja", "saliña", "salina", "lagun",
    "laguna", "pos", "putu", "bij", "van", "de", "der", "den", "het", "en",
    "sint", "st", "nieuw", "oud", "groot", "klein", "zuid", "noord", "oost",
    "west", "punt", "berg", "plantage", "landhuis", "kamp",
}
NEERLANDES = (
    "berg", "straat", "weg", "baai", "hof", "huis", "dorp", "plein", "kade",
    "gracht", "dijk", "veld", "burg", "stad", "wijk", "laan", "park", "zicht",
    "lust", "rust", "vreugd", "vrede", "hoop", "zorg", "wacht", "tuin", "bosch",
    "bos", "heuvel", "dal", "meer", "zee", "haven", "poort", "brug", "molen",
    "werf", "steeg", "hoek", "einde", "land", "polder", "kust",
)


def clasificar(nombre: str, region: str = "") -> str:
    """castellano · castellano-con-voz-indigena · neerlandes-papiamento ·
    por-clasificar. Heurístico y transparente: el humano revisa
    `por-clasificar`, que es la clase que importa."""
    ws_todas = palabras(nombre)
    if ws_todas and (ws_todas[0] in CABEZAS_CASTELLANAS
                     or " ".join(ws_todas[:2]) in CABEZAS_CASTELLANAS):
        return "castellano"
    ws = [w for w in ws_todas if w not in GENERICOS]
    if not ws:
        return "castellano"

    def es_castellana(w: str) -> bool:
        if w in CASTELLANO:
            return True
        if len(w) >= 6 and any(w.endswith(s) for s in SUFIJOS_CASTELLANOS
                               if s not in SUFIJOS_DEBILES):
            return True
        return False

    if all(es_castellana(w) for w in ws):
        if any(w in VOZ_INDIGENA_LEXICALIZADA for w in ws):
            return "castellano-con-voz-indigena"
        return "castellano"
    if region == "islas-abc":
        ws_abc = [w for w in ws_todas if w not in GENERICOS_ABC and w not in GENERICOS]
        if not ws_abc:
            return "neerlandes-papiamento"
        if all(w in CASTELLANO or any(w.endswith(s) for s in NEERLANDES)
               or w in GENERICOS_ABC for w in ws_abc):
            return "neerlandes-papiamento"
    return "por-clasificar"


def laxa(k: str) -> str:
    """La regla de permutación de la skill (§7): j~s~u~h inicial, b~v~p, r~b.
    Reduce las dos claves a una forma laxa antes de medir distancia."""
    k = k.replace("v", "b").replace("p", "b")
    if k[:1] in ("h", "s", "u"):
        k = "j" + k[1:]
    return k


def _lev(a: str, b: str, maximo: int) -> int:
    if abs(len(a) - len(b)) > maximo:
        return maximo + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > maximo:
            return maximo + 1
        prev = cur
    return prev[-1]


# ══════════════════════════════════════════════════════════════════════
# DESCARGA
# ══════════════════════════════════════════════════════════════════════

def consulta(caja) -> str:
    s, w, n, e = caja
    return f"""[out:json][timeout:180];
(
  nwr["name"]["place"]({s},{w},{n},{e});
  nwr["name"]["natural"]({s},{w},{n},{e});
  nwr["name"]["waterway"]({s},{w},{n},{e});
  nwr["name"]["landuse"~"salt_pond"]({s},{w},{n},{e});
);
out center tags;"""


def descargar() -> None:
    import requests
    os.makedirs(CRUDO_DIR, exist_ok=True)
    hoy = dt.date.today().isoformat()
    for region, cajas in REGIONES.items():
        for i, caja in enumerate(cajas, 1):
            ruta = os.path.join(CRUDO_DIR, f"{region}-{i}.json")
            t0 = time.time()
            r = requests.post(OVERPASS, data={"data": consulta(caja)}, timeout=300,
                              headers={"User-Agent": AGENTE})
            r.raise_for_status()
            datos = r.json()
            datos["_curiana"] = {"region": region, "caja": list(caja), "descargado": hoy,
                                 "licencia": "ODbL 1.0 — © OpenStreetMap contributors",
                                 "consulta": consulta(caja)}
            with open(ruta, "w", encoding="utf-8") as fh:
                json.dump(datos, fh, ensure_ascii=False, indent=0)
            print(f"  {region}-{i}: {len(datos['elements'])} elementos, "
                  f"{os.path.getsize(ruta) // 1024} KB, {time.time() - t0:.1f}s")
            time.sleep(2)   # cortesía con Overpass
    with open(os.path.join(CRUDO_DIR, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(
            "# Volcado OSM de la Kaketiana\n\n"
            f"Descargado el {hoy} con `python curiana_sim/barrer_mapa.py --descargar` "
            "desde Overpass (https://overpass-api.de). Un archivo por caja; la caja, "
            "la consulta y la fecha van en `_curiana` dentro de cada JSON.\n\n"
            "**Licencia**: ODbL 1.0, © los colaboradores de OpenStreetMap. Se cita como "
            "`fuente_mapa: osm` en `6-fusion/toponimos_mapa_kaketiana.yaml`.\n\n"
            "Es capa de datos, no fuente documental: un nombre aquí prueba que el nombre "
            "está vivo en 2026 y dónde, nada más (regla 3).\n")


# ══════════════════════════════════════════════════════════════════════
# COMPILAR
# ══════════════════════════════════════════════════════════════════════

def cargar_crudo() -> list[dict]:
    if not os.path.isdir(CRUDO_DIR):
        sys.exit("no hay volcado: corre primero `python barrer_mapa.py --descargar`")
    salida = []
    for nombre in sorted(os.listdir(CRUDO_DIR)):
        if not nombre.endswith(".json"):
            continue
        with open(os.path.join(CRUDO_DIR, nombre), encoding="utf-8") as fh:
            datos = json.load(fh)
        region = datos["_curiana"]["region"]
        for e in datos["elements"]:
            e["_region"] = region
            salida.append(e)
    return salida


def tipo_de(tags: dict):
    for k in ("place", "natural", "waterway", "landuse"):
        if k in tags:
            return TIPOS.get((k, tags[k])), f"{k}={tags[k]}"
    return None, "?"


def cargar_mesa():
    """Índice de la mesa por clave: {clave: entrada del indice_de_formas}."""
    if not os.path.exists(MESA):
        return {}, {}
    with open(MESA, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    por_clave, por_palabra = {}, defaultdict(set)
    for e in doc.get("indice_de_formas") or []:
        formas = [e["forma"]] + list(e.get("variantes") or [])
        for f in formas:
            k = clave(f)
            if k:
                por_clave.setdefault(k, e)
                if len(k) >= 5:
                    por_palabra[k].add(e["forma"])
    return por_clave, por_palabra


def cruzar(propio: str, por_clave, por_palabra):
    """Devuelve (entrada de la mesa | None, cómo). `cómo` es exacto, parcial
    (una palabra del nombre está en la mesa) o aproximado (distancia 1-2 tras
    la permutación laxa: es para REVISAR, no cuenta como encontrado)."""
    k = clave(propio)
    if k in por_clave:
        return por_clave[k], "exacto"
    # palabra por palabra (≥5 letras): «Bajo de Supi» → supi
    for w in palabras(propio):
        kw = clave(w)
        if len(kw) >= 5 and kw in por_clave:
            return por_clave[kw], f"parcial:{w}"
    # aproximado: Jurujurebo ~ jurijurebo, Cividual ~ sibidigual, Guaydabacos ~ guaidabacoa
    if len(k) >= 6:
        kl, maximo = laxa(k), (2 if len(k) >= 8 else 1)
        mejor = None
        for k2, e in por_clave.items():
            if len(k2) < 6:
                continue
            d = _lev(kl, laxa(k2), maximo)
            if d <= maximo and (mejor is None or d < mejor[0]):
                mejor = (d, k2, e)
        if mejor:
            return mejor[2], f"aproximado:{mejor[1]}"
    return None, ""


def compilar(entradas_crudas: list[dict]) -> tuple[list, dict]:
    por_clave, por_palabra = cargar_mesa()
    vistos, entradas, descartes = set(), [], Counter()
    for e in entradas_crudas:
        tags = e.get("tags") or {}
        nombre = (tags.get("name") or "").strip()
        if not nombre:
            continue
        tipo, etiqueta = tipo_de(tags)
        if tipo is None:
            descartes[etiqueta] += 1
            continue
        lat = e.get("lat") or (e.get("center") or {}).get("lat")
        lon = e.get("lon") or (e.get("center") or {}).get("lon")
        if lat is None or lon is None:
            descartes["sin-coordenadas"] += 1
            continue
        firma = (e["_region"], clave(nombre), tipo)
        if firma in vistos:
            descartes["duplicado"] += 1
            continue
        vistos.add(firma)

        propio = nombre_propio(nombre) or nombre
        clase = clasificar(nombre, e["_region"])
        reg = {"forma": nombre, "tipo": tipo, "lat": round(float(lat), 5),
               "lon": round(float(lon), 5), "region": e["_region"],
               "fuente_mapa": "osm", "osm": f"{e['type']}/{e['id']}",
               "osm_tag": etiqueta, "clase": clase}
        if clave(propio) != clave(nombre):
            reg["nombre_propio"] = propio
        if clase == "por-clasificar":
            m, como = cruzar(propio, por_clave, por_palabra)
            if m:
                cr = m.get("cruces") or {}
                reg["cruce"] = {"con": m["forma"], "como": como,
                                "fuentes": list(m.get("fuentes") or [])}
                for campo in ("en_canon", "en_esteves", "en_nodos", "en_mapa_miguel"):
                    if cr.get(campo):
                        reg["cruce"][campo] = cr[campo]
                if como.startswith("aproximado"):
                    reg["revisar"] = True     # puede ser el mismo nombre con otra grafía, o no
                    reg["nuevo"] = True       # hasta que alguien lo confirme
                    reg["deuda"] = "sin-procedencia"
            else:
                reg["nuevo"] = True
                reg["deuda"] = "sin-procedencia"
        entradas.append(reg)

    orden = {"por-clasificar": 0, "castellano-con-voz-indigena": 1,
             "neerlandes-papiamento": 2, "castellano": 3}
    entradas.sort(key=lambda r: (r["region"], orden[r["clase"]], clave(r["forma"])))
    return entradas, descartes


def resumen(entradas: list, descartes: Counter) -> dict:
    por_region = {}
    for region in REGIONES:
        rs = [r for r in entradas if r["region"] == region]
        pc = [r for r in rs if r["clase"] == "por-clasificar"]
        firmes = [r for r in pc if "cruce" in r and not r.get("revisar")]
        por_region[region] = {
            "total": len(rs),
            "castellano": sum(r["clase"] == "castellano" for r in rs),
            "castellano_con_voz_indigena": sum(r["clase"] == "castellano-con-voz-indigena" for r in rs),
            "neerlandes_papiamento": sum(r["clase"] == "neerlandes-papiamento" for r in rs),
            "por_clasificar": len(pc),
            "de_ellos_en_canon": sum(bool((r.get("cruce") or {}).get("en_canon")) for r in firmes),
            "de_ellos_en_esteves": sum(bool((r.get("cruce") or {}).get("en_esteves")) for r in firmes),
            "de_ellos_en_alguna_fuente": len(firmes),
            "aproximados_a_revisar": sum(bool(r.get("revisar")) for r in pc),
            "nuevos": sum(r.get("nuevo", False) and not r.get("revisar") for r in pc),
        }
    return {"entradas": len(entradas), "por_region": por_region,
            "descartados_por_etiqueta": dict(descartes.most_common())}


def escribir(entradas: list, descartes: Counter) -> dict:
    res = resumen(entradas, descartes)
    fecha = None
    for nombre in sorted(os.listdir(CRUDO_DIR)):
        if nombre.endswith(".json"):
            with open(os.path.join(CRUDO_DIR, nombre), encoding="utf-8") as fh:
                fecha = json.load(fh)["_curiana"]["descargado"]
            break
    doc = {
        "meta": {
            "generado_por": "curiana_sim/barrer_mapa.py",
            "generado": dt.date.today().isoformat(),
            "editar_a_mano": "no — se edita el script o se vuelve a descargar, y se regenera",
            "fuente_mapa": "OpenStreetMap vía Overpass, descargado el " + str(fecha),
            "licencia": "ODbL 1.0 — © OpenStreetMap contributors",
            "que_es": ("inventario del mapa vivo de la Kaketiana, cruzado con la mesa de la "
                       "campaña (toponimos_por_fuente.yaml). Skill campana-toponimos §9. "
                       "No es canon: lo `nuevo` es la cola, con deuda declarada."),
            "clases": {
                "por-clasificar": "nombre no castellano (o con una palabra no reconocida): candidato a la campaña",
                "castellano-con-voz-indigena": "nombre castellano hecho con un préstamo lexicalizado (Cardón, Cují, Yabo…): se registra, no se segmenta",
                "castellano": "nombre castellano: se registra aparte (filtro 1 del habla paraguanera)",
            },
            "cajas": {r: [list(c) for c in cs] for r, cs in REGIONES.items()},
            "resumen": res,
        },
        "entradas": entradas,
    }
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# GENERADO por curiana_sim/barrer_mapa.py — no editar a mano.\n")
        yaml.safe_dump(doc, fh, allow_unicode=True, sort_keys=False, width=110,
                       default_flow_style=None)
    return res


def informe(res: dict, entradas: list, lote: bool) -> None:
    print(f"\n── el mapa vivo de la Kaketiana (OSM) ── {res['entradas']} nombres\n")
    print(f"  {'región':20} {'total':>6} {'castell.':>9} {'c/voz':>6} {'nl/pap':>7} "
          f"{'por clas.':>10} {'en fuente':>10} {'≈revisar':>9} {'nuevos':>7}")
    for region, r in res["por_region"].items():
        print(f"  {region:20} {r['total']:6} {r['castellano']:9} "
              f"{r['castellano_con_voz_indigena']:6} {r['neerlandes_papiamento']:7} "
              f"{r['por_clasificar']:10} {r['de_ellos_en_alguna_fuente']:10} "
              f"{r['aproximados_a_revisar']:9} {r['nuevos']:7}")
    if res["descartados_por_etiqueta"]:
        print("\n  descartados por etiqueta OSM: " + ", ".join(
            f"{k} {n}" for k, n in list(res["descartados_por_etiqueta"].items())[:10]))
    if lote:
        for region in REGIONES:
            rs = [r for r in entradas if r["region"] == region and r["clase"] == "por-clasificar"]
            aprox = [r for r in rs if r.get("revisar")]
            nuevos = [r for r in rs if r.get("nuevo") and not r.get("revisar")]
            if aprox:
                print(f"\n  ≈ {region}: {len(aprox)} aproximados, a revisar")
                for r in aprox:
                    print(f"      {r['forma']:30} ~ {r['cruce']['con']:22} {r['tipo']:9} "
                          f"{r['lat']:.4f}, {r['lon']:.4f}")
            if nuevos:
                print(f"\n  ▸ {region}: {len(nuevos)} nuevos (en ninguna fuente)")
                for r in nuevos:
                    print(f"      {r['forma']:34} {r['tipo']:10} {r['lat']:.4f}, {r['lon']:.4f}")
    print(f"\n  → {os.path.relpath(SALIDA, REPO)}\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Barrer el mapa vivo de la Kaketiana (OSM)")
    ap.add_argument("--descargar", action="store_true", help="Overpass → fuentes_caquetios/osm_kaketiana/")
    ap.add_argument("--lote", action="store_true", help="imprime lo nuevo por región")
    args = ap.parse_args(argv)
    if args.descargar:
        print("\n── descargando de Overpass ──")
        descargar()
    entradas, descartes = compilar(cargar_crudo())
    res = escribir(entradas, descartes)
    informe(res, entradas, args.lote)
    return 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
