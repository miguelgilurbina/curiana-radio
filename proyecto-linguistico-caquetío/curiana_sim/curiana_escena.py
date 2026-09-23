"""
CURIANA — la escena de la era 2, capa 1: ESTAR.

Hasta hoy un agente nacía en su sitio y moría en su sitio:
`state.ubicaciones_override` —el campo pensado para moverlos— tenía cuatro
lectores y CERO escrituras (medido el 2026-09-17 con
`6-fusion/scripts/derivar_escena_por_lugar.py --motor`). Este módulo es quien
lo escribe.

LA PUERTA ES UNA
----------------
`ambito_de(agente, state)` devuelve **el lugar donde ese agente está en este
momento del día**, o `None`. `None` significa «no hay escena»: la era 1, o un
run de la era 2 sin `--escena`. Todo lo que la capa 2 (OÍR, PR 4) filtre por
ámbito pasa por aquí —o por `ambito_visible_de`, que es esta misma con el día
de Capubana abierto (sección siguiente)— y por ningún otro sitio.

Devuelve una CADENA y no un booleano a propósito: mañana, con la capa 4
(POTESTAD), esta misma puerta devolverá adónde se movió el agente por decisión
suya, y quien la llame no tendrá que cambiar.

ESTAR NO ES VER: `ambito_visible_de` (2026-09-18)
-------------------------------------------------
El día 1 de la serie C midió que el Capubana **juntaba cuerpos, pero no
ámbitos**: con `--capubana-cada 3`, el día 3 `ambito_de` devolvía `"Capubana"`
para los 63 y eso es UN LUGAR MÁS, cuyo léxico era el de sus dos ocupantes del
día 1 (Sawaka y Hayo, 71 formas): V2 vacía y las tres rivales de «las cuentas»
a 0. El diseño dice lo contrario (§4 y la decisión p7): ese día **todos ven
todo**.

Por eso hay dos puertas y no una, y dicen dos cosas distintas:

  `ambito_de(agente, state)`          dónde ESTÁ  → el registro (`situar`, y de
                                      ahí `Neologismo.ambito` / `adoptado_en`),
                                      `[Aquí estás]`, `presencias`, el campo.
                                      El día de Capubana devuelve `"Capubana"`,
                                      que es donde la gente está de verdad.
  `ambito_visible_de(agente, state)`  qué VE      → las cuatro vías (V1 las
                                      propuestas, V2 las adoptadas, V3 las
                                      competencias, V4 el campo que pondera la
                                      muestra) y `[Lo que se dijo aquí]`.
                                      El día de Capubana devuelve `None`, que
                                      es lo que las cuatro vías **ya** entienden
                                      como «sin filtro»: la unión de todos los
                                      ámbitos, sin un parámetro nuevo en
                                      `LexicoComunitario`, `CampoLexico` ni
                                      `CompetenciaLexica`.

Los dos coinciden todos los demás días, y los dos devuelven `None` sin escena.

DE DÓNDE SALE LA ESCENA
-----------------------
De `curiana_escena_era2.py`, módulo GENERADO desde `6-fusion/escena_era2.yaml`
(y ése, del elenco: ninguna fila se escribió agente a agente). Aquí no hay
tabla: hay lectura. La tabla es determinista —`(clase, momento, período) →
lugar`— así que la capa 1 no usa azar: ni el RNG global del motor (que está
compartido con los eventos y el muestreo, y sacar un número de él desplazaría
la cadena) ni `hash()` (salado por proceso).

LO QUE NO HACE
--------------
No toca el scorer, ni `capas_de_score`, ni la ventana de 12 (decisión 4 → A:
la escena dice DÓNDE está cada uno, no quién habla), ni el catálogo de eventos,
ni `[Tu tierra]`. En la era 1 no existe.

CAPA 2 — OÍR (2026-09-17, PR 4)
-------------------------------
`bloque_lo_que_se_dijo_aqui()` es el otro bloque que la escena pone en el
prompt: lo que se dijo EN ESTE LUGAR en el momento ANTERIOR, ≤ 3
intervenciones y ≤ 280 caracteres (decisión p5 → A). No el mismo turno: eso
sería la V1 de hoy con otro nombre, que es literalmente el mecanismo que
produjo los tres cruces de Δturnos = 0 del día 1 de la serie B.

El ámbito del bloque es el de AHORA —`ambito_visible_de(agente, state)`, la
misma puerta que filtra las cuatro vías— y no el del momento anterior: todo lo
que el agente ve pasa por un solo ámbito, y así un lugar «recuerda» lo que se
dijo en él hace un momento aunque quien llega no estuviera. La alternativa (oír
sólo si estabas allí cuando se dijo) pide una puerta más y queda anotada para
Miguel.

Ensayo sin API (como `curiana_mundo.py`):

    python curiana_escena.py            # las 63 × 6 × 3 escenas, con su largo
    python curiana_escena.py --capubana # el día de la convergencia
    python curiana_escena.py --oir      # los bloques [Lo que se dijo aquí]
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Optional

try:
    import curiana_escena_era2 as _tabla
except ImportError:                                   # pragma: no cover
    _tabla = None

MUNDO = "PARAGUANÁ"

# El bloque [Aquí estás] sustituye a [Tu ubicación] (una línea) en la era 2.
# Tope duro: el prompt medio de la era 2 son 7.206 caracteres y r = −0,48 entre
# longitud y score, así que cada bloque lleva presupuesto (diseño §1.8 y §2).
PRESUPUESTO = 200

# Decisión 7 → A (Miguel, 2026-09-17): la cadencia del Capubana es un parámetro
# declarado que el run dice de sí mismo, como el perfil. N = 3 en la primera
# cadena (dos convergencias en ocho días); el calendario del canon la pone en
# los días 55-58 de la seca, inalcanzable en una cadena corta.
CAPUBANA_CADA_POR_DEFECTO = 3

# El momento del día, dicho en prosa para el bloque.
MOMENTO_EN_PROSA = {
    "amanecer": "al amanecer",
    "mañana": "en la mañana",
    "mediodia": "al mediodía",
    "tarde": "en la tarde",
    "anochecer": "a la caída del sol",
    "noche": "de noche",
}

CABEZA = "[Aquí estás]: "

# ── Capa 2: OÍR ───────────────────────────────────────────────────────
# Tope duro del bloque entero (decisión p5 → A: ≤ 3 intervenciones, 280
# caracteres). Medido en el diseño §2: +3,5 % del prompt medio.
PRESUPUESTO_OIR = 280
MAX_DICHOS = 3
# Lo que se recorta de cada intervención antes de guardarla en el estado.
TOPE_FRASE = 70
CABEZA_OIR = "[Lo que se dijo aquí, en este mismo sitio, hace un momento]:"


# ══════════════════════════════════════════════════════════════════════
# 1. ¿HAY ESCENA?
# ══════════════════════════════════════════════════════════════════════

def hay_tabla() -> bool:
    return _tabla is not None


def escena_activa(state) -> bool:
    """True sólo en un run de la era 2 que corrió con `--escena`.

    Tres condiciones, y las tres se comprueban: el brazo (`state.escena`), el
    mundo (PARAGUANÁ; en CURIANA no hay escena ni canon de sitios) y que el
    período del estado sea uno de los tres de la era 2."""
    if _tabla is None or not getattr(state, "escena", False):
        return False
    if getattr(state, "mundo", None) != MUNDO:
        return False
    return getattr(state, "estacion", None) in _tabla.PERIODOS


def capubana_cada(state) -> int:
    """La cadencia declarada del run; 0 = no hay convergencia en esta cadena."""
    try:
        return max(0, int(getattr(state, "capubana_cada", 0) or 0))
    except (TypeError, ValueError):                    # pragma: no cover
        return 0


def es_dia_de_capubana(state, cada: Optional[int] = None) -> bool:
    """¿Convergen hoy los dos nodos en el cerro?

    Con cadencia 3, los días 3, 6, 9… Ese día TODOS están en el Capubana los
    seis momentos: es lo que el canon describe del ciclo mayor —las
    delegaciones suben y el díao de cada clan entrega lo suyo al Manaure, que
    redistribuye— comprimido a una cadencia declarada."""
    n = capubana_cada(state) if cada is None else max(0, int(cada or 0))
    if n <= 0:
        return False
    dia = int(getattr(state, "dia", 0) or 0)
    return dia > 0 and dia % n == 0


def es_vispera_de_capubana(state, cada: Optional[int] = None) -> bool:
    """El día anterior a la convergencia: es cuando el canon hace subir el
    aporte de AMUAY por el camino de la alianza (curiana_escena_era2.TRAVESIA)."""
    n = capubana_cada(state) if cada is None else max(0, int(cada or 0))
    if n <= 0:
        return False
    dia = int(getattr(state, "dia", 0) or 0)
    return dia > 0 and (dia + 1) % n == 0


# ══════════════════════════════════════════════════════════════════════
# 2. LA ESCENA DEL TURNO
# ══════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=None)
def _escena(dia: int, momento: str, periodo: str, cada: int) -> tuple:
    """La escena como tupla de pares (cacheable e inmutable). Determinista:
    los mismos argumentos dan la misma escena, siempre y sin azar."""
    if _tabla is None or momento not in _tabla.MOMENTOS or periodo not in _tabla.PERIODOS:
        return ()
    if cada > 0 and dia > 0 and dia % cada == 0:
        cerro = _tabla.CAPUBANA["lugar"]
        return tuple((a, cerro) for a in _tabla.AGENTES)
    i = _tabla.MOMENTOS.index(momento)
    lugar = {a: f[periodo][i] for a, f in _tabla.ESCENA.items()}
    # La travesía de la alianza: la víspera de la convergencia, quien el canon
    # hace cruzar («la esposa principal viene por él») anda el camino
    # compartido en los tres momentos en que el camino se anda.
    if cada > 0 and dia > 0 and (dia + 1) % cada == 0:
        for fila in _tabla.TRAVESIA.get("filas") or []:
            if momento not in (fila.get("momentos") or ()):
                continue
            for a in fila.get("agentes") or ():
                if a in lugar:
                    lugar[a] = fila["lugar"]
    return tuple(sorted(lugar.items()))


def escena_de(state) -> dict:
    """{agente: lugar} para LOS 63 en el momento actual — no sólo los 12 que
    hablan. Un mapa con 12 de 63 no es un mundo (diseño §5b).

    `{}` en la era 1 y con la escena apagada."""
    if not escena_activa(state):
        return {}
    return dict(_escena(int(state.dia), state.momento, state.estacion,
                        capubana_cada(state)))


def ambito_de(agente: str, state) -> Optional[str]:
    """LA PUERTA. El lugar donde está `agente` en este momento del día.

    `None` en la era 1 y cuando la escena está apagada. Es una cadena y no un
    booleano porque mañana devolverá adónde se movió por potestad (capa 4)."""
    if not escena_activa(state):
        return None
    return dict(_escena(int(state.dia), state.momento, state.estacion,
                        capubana_cada(state))).get(agente)


def sin_frontera(state) -> bool:
    """¿Hoy el ámbito no filtra nada?

    El día de Capubana los 63 están en el cerro los seis momentos y el diseño
    (§4, decisión p7) dice que ese día **todos ven todo**. Sin escena es
    siempre False: allí no hay fronteras que quitar porque no hay ninguna."""
    return escena_activa(state) and es_dia_de_capubana(state)


def ambito_visible_de(agente: str, state) -> Optional[str]:
    """LA PUERTA DE LO QUE SE VE (frente a `ambito_de`, que es la de dónde se
    ESTÁ). La llaman las cuatro vías y el bloque de oír, y nadie más.

    Devuelve lo mismo que `ambito_de` salvo el día de Capubana, donde devuelve
    `None` — «sin filtro», la unión de todos los ámbitos, que es exactamente lo
    que V1/V2/V3/V4 hacen ya con `ambito=None`. Así el día de la convergencia
    el prompt vuelve a los números de la comunidad entera (DISENO_KOINE §6) sin
    que `LexicoComunitario`, `CampoLexico` ni `CompetenciaLexica` necesiten un
    parámetro nuevo, y lo que se propone o se adopta ese día se sigue
    registrando en `"Capubana"`, que es donde pasó."""
    if sin_frontera(state):
        return None
    return ambito_de(agente, state)


def presentes_en(lugar: str, escena: dict, sin: Optional[str] = None) -> list:
    """Quiénes están en ese lugar, en orden determinista."""
    return sorted(a for a, l in (escena or {}).items() if l == lugar and a != sin)


def glosa_de(lugar: Optional[str]) -> str:
    """Cómo se dice ese lugar en prosa: «la orilla de Tacuato»."""
    if not lugar:
        return ""
    if _tabla is None:                                 # pragma: no cover
        return lugar
    return _tabla.glosa_de(lugar)


def nodo_de(lugar: Optional[str]) -> Optional[str]:
    if not lugar or _tabla is None:                    # pragma: no cover
        return None
    return (_tabla.LUGARES.get(lugar) or {}).get("nodo")


def lugares() -> dict:
    """EL CATÁLOGO de la tabla decidida: `{lugar: {tipo, sitio, nodo, lat,
    lon, glosa, locacion, extremos, puntos, compartido}}`.

    La misma puerta que `ambito_de`, para quien necesita el mapa entero y no
    un agente: hoy el exportador del visor (`export_escena_seed.py`), que
    antes leía la PROPUESTA —y por eso `camino:Moruy-Caseto`, que sólo existe
    en la tabla DECIDIDA, salía «sin coordenada»—. Copia superficial de cada
    fila: el catálogo es de lectura.

    `{}` si no hay tabla (la era 1 no tiene canon de sitios)."""
    if _tabla is None:                                 # pragma: no cover
        return {}
    return {lugar: dict(fila) for lugar, fila in _tabla.LUGARES.items()}


# ══════════════════════════════════════════════════════════════════════
# 3. [Aquí estás] — lo que el agente ve
# ══════════════════════════════════════════════════════════════════════

def _y(nombres: list) -> str:
    """«A, B y C» — la lista dicha como se dice."""
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " y " + nombres[-1]


def bloque_aqui_estas(agente: str, state, presupuesto: int = PRESUPUESTO) -> str:
    """El bloque que en la era 2 con escena sustituye a `[Tu ubicación]`.

    Dice tres cosas y ninguna más: dónde estás, qué momento del día es y
    quiénes están contigo. Si son muchos, cuántos son y los primeros. Tope
    duro `presupuesto`: se recorta la lista de nombres, nunca el lugar.

    Devuelve "" si no hay escena — y entonces el prompt es el de siempre.
    """
    escena = escena_de(state)
    lugar = escena.get(agente)
    if not lugar:
        return ""
    momento = MOMENTO_EN_PROSA.get(getattr(state, "momento", ""), "")
    donde = glosa_de(lugar)
    cabeza = f"{CABEZA}en {donde}" + (f", {momento}." if momento else ".")
    otros = presentes_en(lugar, escena, sin=agente)
    if not otros:
        cola = " No hay nadie más aquí."
        return (cabeza + cola)[:presupuesto]
    cola = (f" Contigo está {otros[0]}." if len(otros) == 1
            else f" Contigo están {_y(otros)}.")
    if len(cabeza) + len(cola) > presupuesto:
        cola = ""
        for k in range(len(otros) - 1, 0, -1):
            prueba = f" Contigo hay {len(otros)}: {', '.join(otros[:k])}…"
            if len(cabeza) + len(prueba) <= presupuesto:
                cola = prueba
                break
        if not cola:
            cola = f" Contigo hay {len(otros)}."
    return (cabeza + cola)[:presupuesto]


# ══════════════════════════════════════════════════════════════════════
# 3b. [Lo que se dijo aquí] — la capa 2: OÍR
# ══════════════════════════════════════════════════════════════════════

# La glosa va entre paréntesis y la acuñación entre corchetes: lo que se
# guarda es LA FRASE CAQUETÍA, no su traducción (el agente no necesita que le
# lean en español lo que su vecino acaba de decir; eso le enseñaría el español
# y alargaría el bloque el doble).
_GLOSA = re.compile(r"\([^)]*\)")
_CORCHETE = re.compile(r"\[[^\]]*\]")
_ESPACIOS = re.compile(r"\s+")
_FIN_DE_FRASE = re.compile(r"[.!?;\n]+")
# Una palabra con guion dentro (`naa-ka`, `biro-ana`) o uno de los cinco
# pronombres: el marcador más barato de que una oración va en caquetío y no en
# castellano. No es el scorer y no lo toca — no puntúa nada, sólo elige qué
# oración de la respuesta se repite en voz alta.
# D11 fase 3 (2026-09-23): entran los pronombres de las hermanas (`dai`, `bui`,
# `lihi`, `tuhu`); los viejos se quedan porque un agente puede seguir
# diciéndolos, y lo que se mira aquí es si la oración va en caquetío.
_MARCA_CAQUETIA = re.compile(
    r"\b(?:dai|bui|lihi|tuhu|taya|pia|nüma|numa|waya|naya)\b|\w+-\w+",
    re.IGNORECASE)


def frase_dicha(texto: str, tope: int = TOPE_FRASE) -> str:
    """La frase caquetía de una intervención, sin su glosa y recortada.

    Devuelve "" si no queda nada que repetir — y entonces esa voz no entra en
    el bloque, que es mejor que meter media oración en castellano."""
    limpio = _CORCHETE.sub(" ", _GLOSA.sub(" ", texto or ""))
    oraciones = [_ESPACIOS.sub(" ", o).strip() for o in _FIN_DE_FRASE.split(limpio)]
    oraciones = [o for o in oraciones if len(o) >= 4]
    if not oraciones:
        return ""
    elegida = next((o for o in oraciones if _MARCA_CAQUETIA.search(o)), oraciones[0])
    if len(elegida) <= tope:
        return elegida
    corte = elegida[:tope].rsplit(" ", 1)[0] or elegida[:tope]
    return corte.rstrip(" ,;:-") + "…"


def dichos_del_turno(escena: dict, interacciones, decir=None,
                     tope: int = TOPE_FRASE) -> list:
    """Lo que se dijo este turno, con el lugar donde se dijo.

    Es lo que `run_turn` guarda en `state.dichos_del_turno_anterior` al cerrar
    el turno, para que el turno siguiente lo oiga. `decir` es
    `curiana_eventos.decir_para_el_mundo` atado al mundo del estado: el bloque
    es texto libre que llega al agente y pasa por la misma puerta que el resto
    (se inyecta desde fuera para que este módulo no importe el motor).

    `[]` sin escena: sin lugar no hay «aquí»."""
    if not escena:
        return []
    decir = decir or (lambda t: t)
    salida = []
    for i in interacciones or []:
        agente = i.get("agent") or i.get("agente")
        lugar = escena.get(agente)
        if not agente or not lugar:
            continue
        frase = frase_dicha(decir(i.get("response") or i.get("texto") or ""), tope)
        if frase:
            salida.append({"agente": agente, "lugar": lugar, "frase": frase})
    return salida


def dichos_aqui(agente: str, lugar: Optional[str], dichos,
                maximo: int = MAX_DICHOS, todos: bool = False) -> list:
    """Las ≤ 3 intervenciones del momento anterior que se dijeron en `lugar`.

    Se queda con las ÚLTIMAS: dentro de un turno el orden es el de habla, y lo
    último que se oyó es lo que se tiene más fresco.

    `todos=True` (el día de Capubana) no filtra por lugar: ese día se oye lo
    que dijo **cualquiera** en el momento anterior, estuviera donde estuviera —
    el primer turno del día de la convergencia oye lo que se dijo la noche
    anterior repartido por los sitios, que es justo la gente que acaba de
    subir al cerro."""
    if not todos and not lugar:
        return []
    mismos = [d for d in (dichos or [])
              if (todos or d.get("lugar") == lugar) and d.get("agente") != agente]
    return mismos[-maximo:]


def bloque_lo_que_se_dijo_aqui(agente: str, state,
                               presupuesto: int = PRESUPUESTO_OIR) -> str:
    """El bloque de la capa 2. "" cuando no hay nada que oír.

    Nada que oír es un dato y no un fallo: un pescador solo en el agua a la
    mañana tiene el ámbito vacío y por eso no oye a nadie (decisión p3 → A)."""
    if not escena_activa(state):
        return ""
    # La puerta de lo que se VE: el día de Capubana devuelve None y entonces
    # no hay filtro de lugar — se oye a cualquiera del momento anterior.
    lugar = ambito_visible_de(agente, state)
    dichos = dichos_aqui(agente, lugar,
                         getattr(state, "dichos_del_turno_anterior", None),
                         todos=(lugar is None))
    if not dichos:
        return ""
    lineas = [CABEZA_OIR]
    largo = len(CABEZA_OIR)
    for d in dichos:
        linea = f"\n— {d['agente']}: «{d['frase']}»"
        if largo + len(linea) > presupuesto:
            break
        lineas.append(linea)
        largo += len(linea)
    if len(lineas) == 1:                       # ni una cupo: mejor nada
        return ""
    return "".join(lineas)


# ══════════════════════════════════════════════════════════════════════
# 4. El volcado al log (PR 8): la escena depurable desde el primer run
# ══════════════════════════════════════════════════════════════════════

_MAX_NOMBRES_EN_EL_LOG = 3


def volcado_de_escena(state, escena: Optional[dict] = None) -> str:
    """«escena del turno · mediodía: Tacuato: Birokoa, Chakamba… · ZG2: …».

    Una línea por turno, para que la escena se pueda mirar desde el primer run
    sin esperar al visor sobre el mapa (diseño §10, opción B). Devuelve "" si
    no hay escena: quien lo imprime decide si es momento de imprimir."""
    escena = escena_de(state) if escena is None else escena
    if not escena:
        return ""
    por_lugar: dict = {}
    for agente, lugar in escena.items():
        por_lugar.setdefault(lugar, []).append(agente)
    partes = []
    for lugar in sorted(por_lugar):
        gente = sorted(por_lugar[lugar])
        visibles = ", ".join(gente[:_MAX_NOMBRES_EN_EL_LOG])
        if len(gente) > _MAX_NOMBRES_EN_EL_LOG:
            visibles += f"… (+{len(gente) - _MAX_NOMBRES_EN_EL_LOG})"
        partes.append(f"{lugar}: {visibles}")
    momento = getattr(state, "momento", "")
    return f"escena del turno · {momento}: " + " · ".join(partes)


# ══════════════════════════════════════════════════════════════════════
# 5. Ensayo sin API
# ══════════════════════════════════════════════════════════════════════

class EstadoDeEnsayo:
    """Lo mínimo que la escena mira de un estado. Para el ensayo y los tests:
    aquí no se importa ComunidadState, que arrastraría el motor entero."""

    def __init__(self, dia=1, momento="amanecer", estacion="viento",
                 escena=True, capubana_cada=0, mundo=MUNDO, turno=1,
                 dichos_del_turno_anterior=None):
        self.dia = dia
        self.turno = turno
        self.momento = momento
        self.estacion = estacion
        self.escena = escena
        self.capubana_cada = capubana_cada
        self.mundo = mundo
        self.dichos_del_turno_anterior = list(dichos_del_turno_anterior or [])


def combinaciones() -> list:
    """Las 63 × 6 × 3 escenas (agente × momento × período), para el ensayo y
    para el test del tope."""
    if _tabla is None:                                 # pragma: no cover
        return []
    return [(a, m, p) for a in _tabla.AGENTES
            for p in _tabla.PERIODOS for m in _tabla.MOMENTOS]


# Lo que «dice» cada agente en el ensayo de --oir: una frase caquetía corta y
# determinista, armada con su propio nombre. No sale de ningún run ni de
# ninguna llamada: es un andamio para medir LARGOS, que es lo que el ensayo
# tiene que decir (el prompt medio son 7.206 caracteres y r = −0,48).
def _frase_de_ensayo(agente: str) -> str:
    raiz = agente.lower().replace("-", "")[:6]
    return (f"Taya naa-ka {raiz}-ana wara kari "
            f"(he visto el {raiz} en el agua).")


def _dichos_de_ensayo(dia: int, momento: str, periodo: str, cada: int) -> list:
    """Lo que se dijo en el momento ANTERIOR, en el ensayo: hablan los doce de
    la ventana —los mismos doce en todos los lugares donde estén."""
    previo = dict(_escena(dia, momento, periodo, cada))
    hablaron = sorted(previo)[:12]
    inter = [{"agent": a, "response": _frase_de_ensayo(a)} for a in hablaron]
    return dichos_del_turno(previo, inter)


def _ensayo_de_oir(cada: int, dia: int) -> None:
    """`--oir`: reconstruye los bloques e imprime sus largos.

    Si hay un run guardado en `curiana_state.json` con
    `dichos_del_turno_anterior`, se usan ÉSOS —son los de verdad—; si no, el
    andamio de arriba. En los dos casos lo que se mide es lo mismo: cuántos
    bloques salen, con cuántas voces y cuánto ocupan."""
    import json
    import os
    guardados = []
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "curiana_state.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            guardados = json.load(f).get("dichos_del_turno_anterior") or []
    except (OSError, ValueError):                      # pragma: no cover
        guardados = []
    de_donde = (f"del run guardado ({os.path.basename(ruta)})" if guardados
                else "del ensayo (no hay run guardado con dichos)")
    print(f"\n  [Lo que se dijo aquí] — {de_donde}")
    largos, con_bloque, voces = [], 0, []
    for periodo in _tabla.PERIODOS:
        for i, momento in enumerate(_tabla.MOMENTOS):
            anterior = _tabla.MOMENTOS[i - 1] if i else _tabla.MOMENTOS[-1]
            dichos = guardados or _dichos_de_ensayo(dia, anterior, periodo, cada)
            st = EstadoDeEnsayo(dia=dia, momento=momento, estacion=periodo,
                                capubana_cada=cada,
                                dichos_del_turno_anterior=dichos)
            for agente in _tabla.AGENTES:
                b = bloque_lo_que_se_dijo_aqui(agente, st)
                if not b:
                    continue
                con_bloque += 1
                largos.append(len(b))
                voces.append(b.count("\n— "))
                print(f"{len(b):4}  {periodo:<11}{momento:<10}{agente:<12} "
                      + b.replace("\n", " ⏎ "))
    total = len(_tabla.AGENTES) * len(_tabla.MOMENTOS) * len(_tabla.PERIODOS)
    print(f"\n  {con_bloque} de {total} escenas traen bloque "
          f"({100 * con_bloque / total:.0f} %); {total - con_bloque} no oyen nada")
    if largos:
        print(f"  largo: media {sum(largos)/len(largos):.0f} · min {min(largos)} · "
              f"max {max(largos)} · tope {PRESUPUESTO_OIR}")
        print(f"  voces por bloque: media {sum(voces)/len(voces):.1f} · "
              f"max {max(voces)} · tope {MAX_DICHOS}")


def _main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    cada = 3 if "--capubana" in sys.argv else 0
    dia = 3 if "--capubana" in sys.argv else 1
    if _tabla is None:                                 # pragma: no cover
        print("no hay tabla de escena (curiana_escena_era2.py)")
        return
    if "--oir" in sys.argv:
        _ensayo_de_oir(cada, dia)
        return
    largos = []
    for agente, momento, periodo in combinaciones():
        st = EstadoDeEnsayo(dia=dia, momento=momento, estacion=periodo,
                            capubana_cada=cada)
        b = bloque_aqui_estas(agente, st)
        largos.append(len(b))
        print(f"{len(b):3}  {periodo:<11}{momento:<10}{agente:<12} {b}")
    print(f"\n  {len(largos)} escenas ({len(_tabla.AGENTES)} agentes × "
          f"{len(_tabla.MOMENTOS)} momentos × {len(_tabla.PERIODOS)} períodos)")
    print(f"  largo: media {sum(largos)/len(largos):.0f} · min {min(largos)} · "
          f"max {max(largos)} · tope {PRESUPUESTO}")
    st = EstadoDeEnsayo(dia=dia, momento="mediodia", capubana_cada=cada)
    print(f"\n  {volcado_de_escena(st)}")


if __name__ == "__main__":
    _main()
