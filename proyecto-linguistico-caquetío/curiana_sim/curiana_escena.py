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
ámbito pasará por aquí y sólo por aquí.

Devuelve una CADENA y no un booleano a propósito: mañana, con la capa 4
(POTESTAD), esta misma puerta devolverá adónde se movió el agente por decisión
suya, y quien la llame no tendrá que cambiar.

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

Ensayo sin API (como `curiana_mundo.py`):

    python curiana_escena.py            # las 63 × 6 × 3 escenas, con su largo
    python curiana_escena.py --capubana # el día de la convergencia
"""

from __future__ import annotations

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
                 escena=True, capubana_cada=0, mundo=MUNDO, turno=1):
        self.dia = dia
        self.turno = turno
        self.momento = momento
        self.estacion = estacion
        self.escena = escena
        self.capubana_cada = capubana_cada
        self.mundo = mundo


def combinaciones() -> list:
    """Las 63 × 6 × 3 escenas (agente × momento × período), para el ensayo y
    para el test del tope."""
    if _tabla is None:                                 # pragma: no cover
        return []
    return [(a, m, p) for a in _tabla.AGENTES
            for p in _tabla.PERIODOS for m in _tabla.MOMENTOS]


def _main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    cada = 3 if "--capubana" in sys.argv else 0
    dia = 3 if "--capubana" in sys.argv else 1
    if _tabla is None:                                 # pragma: no cover
        print("no hay tabla de escena (curiana_escena_era2.py)")
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
