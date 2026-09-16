"""
CURIANA — Estado de la Comunidad (State Management)
Gestión del estado del mundo: tiempo, clima, eventos, ubicaciones.
"""

import json
import copy
from dataclasses import dataclass, field, asdict
from typing import Optional


# ============================================================
# Constantes del calendario comprimido
# ============================================================

ESTACIONES = {
    "seca": {
        "nombre": "Tiempo de Viento",
        "meses_equiv": "Dic–May",
        "descripcion": "Viento noreste fuerte. Pesca máxima. Expediciones a las islas. Cosecha de sal. Comercio intenso.",
        "actividades_primarias": ["pesca", "salinar", "expedicion_islas", "intercambio"],
        "clima_base": "despejado, viento noreste",
    },
    "lluvias": {
        "nombre": "Tiempo de Siembra",
        "meses_equiv": "Jun–Nov",
        "descripcion": "Lluvias frecuentes. Siembra y cultivo. Buko lleno. Menos navegación. Ceremonias.",
        "actividades_primarias": ["cultivar", "sembrar", "ritual_siembra", "construir"],
        "clima_base": "nublado, lluvias frecuentes, viento suave",
    },
}

MOMENTOS_DIA = ["amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche"]

# Calendario comprimido: 60 días simulados = 1 estación; 120 = 1 año (2
# estaciones). Coincide con el mapeo declarado en auto_mode() del orquestador.
# Es el calendario de la ERA 1 (mundo CURIANA) y no se toca.
DIAS_POR_ESTACION = 60
DIAS_POR_ANIO = 120

# ── El año de la era 2 (mundo PARAGUANÁ) ─────────────────────────────
# Decisión de Miguel, 2026-09-15 (6-fusion/decisiones_tanda_2026-09-15.yaml,
# p1: «A. Definitivamente»): tres períodos, 50/40/30. Lo atestiguado son dos
# partes —una seca larga y un pulso corto de lluvias en octubre-diciembre
# (ecologia-006; Sievers lo vio en Paraguaná en 1892, Arcaya p. 24)—; partir
# la seca en dos es canon-simulación. El motor decía lluvias «Jun–Nov», que son
# los meses más secos: eso se corrige aquí. Detalle: 6-fusion/clima_era2.yaml.
# Los períodos NO llevan nombre caquetío a propósito (p2): que lo acuñen.
# `equivale` traduce el período a la estación de la era 1 para que los eventos
# escritos con `estacion: seca/lluvias` sigan cayendo donde toca.
PERIODOS_ERA2 = {
    "viento": {
        "nombre": "Tiempo de Viento",
        "meses_equiv": "Ene–May",
        "dias": 50,
        "equivale": "seca",
        "descripcion": "El alisio arrecia: fabrica la sal, aclara el agua. Buceo, travesía a las islas, pesca nocturna con jachos.",
        "actividades_primarias": ["pesca", "salinar", "expedicion_islas", "intercambio"],
        "clima_base": "despejado, alisio firme del este",
    },
    "seca_larga": {
        "nombre": "la seca larga",
        "meses_equiv": "Jun–Sep",
        "dias": 40,
        "equivale": "seca",
        "descripcion": "El «largo verano»: el jagüey baja, se chupa jajato contra la sed, sólo el cerro da agua. Al final, la subida al Capubana.",
        "actividades_primarias": ["acarreo_de_agua", "pesca", "intercambio", "consulta_piache"],
        "clima_base": "cielo limpio, calor seco, el viento afloja",
    },
    "siembra": {
        "nombre": "Tiempo de Siembra",
        "meses_equiv": "Oct–Dic",
        "dias": 30,
        "equivale": "lluvias",
        "descripcion": "El pulso: chubascos cortos, cauces efímeros, conuco de ciclo corto; el salinar para.",
        "actividades_primarias": ["cultivar", "sembrar", "ritual_siembra", "construir"],
        "clima_base": "nubes cargadas, chubascos cortos, viento suave",
    },
}

# El calendario de cada mundo: [(id de estación, días)]. Los dos suman 120.
CALENDARIOS = {
    "CURIANA":   [("seca", DIAS_POR_ESTACION), ("lluvias", DIAS_POR_ESTACION)],
    "PARAGUANÁ": [(k, v["dias"]) for k, v in PERIODOS_ERA2.items()],
}

# Todas las estaciones que el estado puede nombrar, con su ficha.
ESTACIONES_TODAS = {**ESTACIONES, **PERIODOS_ERA2}


def calendario_de(mundo: str) -> list:
    return CALENDARIOS.get(mundo or "CURIANA", CALENDARIOS["CURIANA"])


def estacion_equivalente(estacion: str) -> str:
    """El período de la era 2 dicho en la estación de la era 1 (viento → seca);
    una estación de la era 1 se devuelve tal cual."""
    return ESTACIONES_TODAS.get(estacion, {}).get("equivale", estacion)

# Turnos por día. La era 1 corrió con 2 (amanecer y tarde); la era 2 pide días
# más largos —Miguel, 2026-09-14: «es preferible que un día tenga muchos más
# turnos, así podríamos tener una simulación por día»— y con 6 se recorren los
# seis momentos de MOMENTOS_DIA. El valor vive en el estado, así que un run
# continuado hereda el ritmo del anterior.
TURNOS_POR_DIA_ERA1 = 2


def momento_de_turno(turno: int, turnos_por_dia: int) -> str:
    """El momento del día que toca al turno `turno` (1-based) cuando el día
    tiene `turnos_por_dia` turnos: los momentos se reparten a espacios
    iguales sobre MOMENTOS_DIA. Con 2 turnos da amanecer y tarde (la era 1);
    con 6, los seis momentos."""
    n = max(1, int(turnos_por_dia))
    i = ((turno - 1) * len(MOMENTOS_DIA)) // n
    return MOMENTOS_DIA[min(max(i, 0), len(MOMENTOS_DIA) - 1)]


def ESTACION_DE_DIA(dia: int, mundo: str = "CURIANA") -> str:
    """Estación que corresponde a un día simulado en el calendario de `mundo`.

    CURIANA (era 1): día 1 = seca, alternando cada 60. PARAGUANÁ (era 2):
    viento 1-50, seca larga 51-90, siembra 91-120, y vuelta a empezar."""
    d = (dia - 1) % DIAS_POR_ANIO
    acumulado = 0
    for estacion, dias in calendario_de(mundo):
        acumulado += dias
        if d < acumulado:
            return estacion
    return calendario_de(mundo)[-1][0]

LOCACIONES = [
    "orilla", "manglar", "plaza", "casa_cacique", "choza_piache",
    "conuco", "buco", "salinar", "taller_canoas", "bohios",
    "perimetro", "camino_islas", "matorral",
]

# Ritmo de actividades por momento del día
ACTIVIDADES_POR_MOMENTO = {
    "amanecer":   ["preparar_comida", "preparar_redes", "ritual_matutino"],
    "mañana":     ["pesca", "cultivar", "artesan ia", "construir_canoas", "patrulla"],
    "mediodia":   ["descanso", "comer", "socializar"],
    "tarde":      ["intercambio", "enseñar", "reparar", "socializar", "consejo"],
    "anochecer":  ["consejo", "historias", "consulta_piache", "cenar"],
    "noche":      ["dormir", "ritual_nocturno", "guardia"],
}


# ============================================================
# Estado del mundo
# ============================================================

@dataclass
class ComunidadState:
    # Tiempo
    dia: int = 1
    turno: int = 1          # 1 = mañana, 2 = tarde/noche
    estacion: str = "seca"  # "seca" | "lluvias"
    momento: str = "amanecer"

    # Ambiente
    clima: str = "despejado, viento noreste suave"
    nivel_alimentos: str = "normal"   # "abundante" | "normal" | "escaso" | "crisis"
    nivel_sal: str = "bajo"           # necesitan ir al salinar
    nivel_tension: str = "bajo"       # "bajo" | "medio" | "alto" | "critico"

    # Eventos
    eventos_activos: list = field(default_factory=list)
    evento_del_turno: Optional[str] = None
    historial_eventos: list = field(default_factory=list)

    # Agentes en escena (los que están "activos" este turno)
    agentes_en_escena: list = field(default_factory=lambda: [
        "Manaure", "Shaboro", "Nubiri-sha", "Tawaka", "Dare-nu"
    ])

    # Ubicaciones actuales (overrides de ubicacion_default)
    ubicaciones_override: dict = field(default_factory=dict)

    # Memoria de relaciones (tensiones activas entre pares)
    tensiones_activas: dict = field(default_factory=lambda: {
        "Tawaka-Korie-ko": {"nivel": "medio", "causa": "diferencia generacional sobre tradición"},
        "Chiriware-Marokoto-ni": {"nivel": "alto", "causa": "desconfianza étnica profunda"},
        "Biro-ko-Tariwa": {"nivel": "medio", "causa": "disputa precio sal/pescado"},
        "Manaure-Kadushi": {"nivel": "bajo", "causa": "noticias de islas que cuestionan autoridad"},
    })

    # Notas del orquestador. Desde el 2026-09-16, con --reflexion, guarda la
    # última reflexión del Director al cerrar el día: el día siguiente
    # (--continuar) la ve en su prompt.
    notas_orquestador: str = ""

    # Los cierres narrativos del Director en el día en curso (uno por turno):
    # los deja director_narrate() y los lee la reflexión del día, que los
    # vacía al cerrar. Nunca guarda más de un día.
    cierres_del_dia: list = field(default_factory=list)

    # Ritmo del día (ver TURNOS_POR_DIA_ERA1) y el run del que viene este
    # estado cuando se encadenan días (--continuar): un run continuado declara
    # en su config de qué run hereda el mundo, la memoria y la koiné.
    turnos_por_dia: int = TURNOS_POR_DIA_ERA1
    run_anterior: Optional[str] = None
    # El nombre del mundo que encabeza el contexto: CURIANA en la era 1,
    # PARAGUANÁ en la era 2 (lo fija el elenco activo, ver curiana_agents.MUNDO).
    mundo: str = "CURIANA"

    def avanzar_turno(self):
        """Avanza un turno y, al cerrar el día, el calendario.

        El día tiene `turnos_por_dia` turnos; el momento de cada uno sale de
        momento_de_turno(). Con 2 turnos es la media jornada de la era 1."""
        if self.turno < self.turnos_por_dia:
            self.turno += 1
        else:
            self.turno = 1
            self.dia += 1
            # Registrar evento del día anterior
            if self.evento_del_turno:
                self.historial_eventos.append({
                    "dia": self.dia - 1,
                    "evento": self.evento_del_turno
                })
                self.evento_del_turno = None
            self._actualizar_estacion()
        self.momento = momento_de_turno(self.turno, self.turnos_por_dia)

    def fijar_mundo(self, mundo: str):
        """Pone el mundo y, si la estación actual no es de su calendario (un
        estado nuevo trae `seca` y la era 2 empieza en `viento`), la recalcula
        del día. Un estado continuado (--continuar) ya trae la suya."""
        self.mundo = mundo
        validas = {e for e, _ in calendario_de(mundo)}
        if self.estacion not in validas:
            self.estacion = ESTACION_DE_DIA(self.dia, mundo)
            self.clima = ESTACIONES_TODAS[self.estacion]["clima_base"]

    def _actualizar_estacion(self):
        """Pasa a la estación que toca según el calendario del mundo (era 1:
        seca/lluvias cada DIAS_POR_ESTACION; era 2: viento/seca larga/siembra).

        Antes NADIE asignaba `estacion`: los runs transcurrían enteros en
        "seca". Eso dejaba inalcanzables 9 de los 25 eventos (incluidos los
        seis escritos con más detalle etnográfico), y como el reporte anual
        cuelga del cambio de estación, la bandera --reporte no hacía nada.
        """
        nueva = ESTACION_DE_DIA(self.dia, self.mundo)
        if nueva != self.estacion:
            self.estacion = nueva
            self.clima = ESTACIONES_TODAS[nueva]["clima_base"]

    def aplicar_efecto(self, efecto: dict):
        """Aplica el efecto de un evento sobre el estado del mundo.

        Los 25 eventos declaran `efecto` (nivel_alimentos, nivel_sal,
        nivel_tension) pero nadie lo leía: el mundo quedaba congelado en sus
        valores iniciales y todos los agentes recibían, en todos los turnos de
        todos los runs, el mismo "Alimentos: normal. Sal (biro): bajo."

        NOTA DE DISEÑO: los niveles PERSISTEN hasta que otro evento los cambie
        — no hay decaimiento ni regresión a la media. Una "gran cosecha de sal"
        deja `nivel_sal=abundante` indefinidamente. Es mejor que el mundo
        congelado de antes, pero modelar el consumo (la sal se gasta, la
        tensión se enfría) es una decisión pendiente, no algo que este arreglo
        deba inventar por su cuenta.
        """
        for clave, valor in (efecto or {}).items():
            if hasattr(self, clave):
                setattr(self, clave, valor)

    def to_context_string(self) -> str:
        """Genera el string de contexto que se inyecta en cada llamada de agente."""
        est = ESTACIONES_TODAS.get(self.estacion) or ESTACIONES["seca"]
        lines = [
            f"[{self.mundo} — {est['nombre']}]",
            f"Día {self.dia}, Turno {self.turno} ({self.momento}). {self.clima}.",
            f"Alimentos: {self.nivel_alimentos}. Sal (biro): {self.nivel_sal}. Tensión comunitaria: {self.nivel_tension}.",
        ]
        if self.evento_del_turno:
            lines.append(f"[Situación del turno]: {self.evento_del_turno}")
        if self.eventos_activos:
            lines.append(f"[Eventos activos]: {'; '.join(self.eventos_activos)}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ComunidadState":
        return cls(**d)

    def save(self, path: str = "curiana_state.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str = "curiana_state.json") -> "ComunidadState":
        with open(path, encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


# ============================================================
# Estado inicial para el test run
# ============================================================

def estado_inicial_test() -> ComunidadState:
    """
    Día 1 de la seca. Shaboro tuvo un sueño.
    El nivel de sal es bajo — necesitan ir al salinar.
    """
    return ComunidadState(
        dia=1,
        turno=1,
        estacion="seca",
        momento="amanecer",
        clima="despejado, viento noreste suave, cielo rosado",
        nivel_alimentos="normal",
        nivel_sal="bajo",
        nivel_tension="bajo",
        evento_del_turno=(
            "Shaboro salió de su choza antes del amanecer con expresión grave. "
            "Buio-sha lo vio desde lejos: ha tenido un sueño de los que importan. "
            "Manaure todavía no ha salido de su casa."
        ),
        agentes_en_escena=["Manaure", "Shaboro", "Buio-sha", "Tawaka", "Dare-nu", "Korie-ko"],
    )


# ============================================================
# Catálogo de eventos activables
# ============================================================

EVENTOS_COTIDIANOS = [
    {
        "id": "pesca_abundante",
        "nombre": "Pesca abundante",
        "descripcion": "Los pescadores regresan con más de lo esperado. El humor mejora.",
        "efecto": {"nivel_alimentos": "abundante", "nivel_tension": "bajo"},
        "agentes_involucrados": ["Bagre-ko", "Tariwa", "Waranaro-sha"],
    },
    {
        "id": "pesca_mala",
        "nombre": "Pesca mala",
        "descripcion": "Poco pescado. Los Guaycarí culpan al calor; los Caquetíos al mal ritual.",
        "efecto": {"nivel_alimentos": "escaso"},
        "agentes_involucrados": ["Bagre-ko", "Tariwa", "Shaboro"],
    },
    {
        "id": "niño_enfermo",
        "nombre": "Niño enfermo",
        "descripcion": "Uno de los niños tiene fiebre alta. La familia busca al piache.",
        "efecto": {"nivel_tension": "medio"},
        "agentes_involucrados": ["Shaboro", "Buio-sha", "Paugis-sha", "Wama-sha"],
    },
    {
        "id": "disputa_vecinos",
        "nombre": "Disputa entre vecinos",
        "descripcion": "Dos familias en conflicto por límites del conuco.",
        "efecto": {"nivel_tension": "medio"},
        "agentes_involucrados": ["Manaure", "Nubiri-sha", "Korie-ko"],
    },
    {
        "id": "canoa_islas_llega",
        "nombre": "Llega canoa de las islas",
        "descripcion": "La canoa de Kadushi llega desde Aruba con bienes y noticias.",
        "efecto": {},
        "agentes_involucrados": ["Kadushi", "Watapana", "Manaure", "Chiriware"],
    },
    {
        "id": "raspado_salinar",
        "nombre": "Raspado de la sal en el salinar",
        "descripcion": "El sol del mediodía ha secado las charcas costeras y la costra de biro brilla blanca y dura. Biro-ko y los suyos la raspan con conchas y palas de madera, los pies hinchados por la salmuera, amontonando la sal en cestos que cargarán hasta los bohíos. El aire sabe a sal y el reflejo ciega.",
        "efecto": {"nivel_sal": "abundante"},
        "agentes_involucrados": ["Biro-ko", "Moruy-sha", "Suba-ko", "Wama-ko"],
    },
    {
        "id": "consulta_piache_sueno",
        "nombre": "Consulta al piache por un sueño",
        "descripcion": "Alguien llega a la choza de Shaboro con un sueño que no lo deja en paz. El piache aviva las brasas de copal, escucha en silencio y sopla humo sobre el rostro del que consulta. Buio-sha observa desde el rincón, aprendiendo a separar el sueño que avisa del que solo es miedo.",
        "efecto": {"nivel_tension": "bajo"},
        "agentes_involucrados": ["Shaboro", "Buio-sha"],
    },
    {
        "id": "raspar_yuca_casabe",
        "nombre": "Preparación del casabe",
        "descripcion": "Las mujeres rallan la yuca amarga sobre el rallo de piedra y exprimen la pulpa en el sebucán colgado de la viga, escurriendo el jugo venenoso gota a gota. La torta blanca se extiende en el budare al fuego y el olor del casabe tostado se cuela en todos los bohíos. Tina-sha dirige el ritmo del trabajo.",
        "efecto": {"nivel_alimentos": "normal"},
        "agentes_involucrados": ["Tina-sha", "Wama-sha", "Piri-sha", "Naure-sha"],
    },
    {
        "id": "tejido_y_alfareria",
        "nombre": "Jornada de tejedoras y ceramistas",
        "descripcion": "Bajo la sombra de los bohíos las manos no descansan: Saruro-sha levanta una vasija enrollando culebrillas de barro, Kahu-sha anuda una hamaca de maure y Pira-sha corrige a las jóvenes que copian los diseños antiguos. Se habla poco; el trabajo se enseña mirando.",
        "efecto": {},
        "agentes_involucrados": ["Saruro-sha", "Kahu-sha", "Pira-sha", "Kori-sha", "Kawa"],
    },
    {
        "id": "trueque_visitantes_plaza",
        "nombre": "Intercambio con visitantes en la plaza",
        "descripcion": "En la plaza central se despliegan los bienes: el Jirajara muestra ocre y carne seca de la sierra, el caquetío ofrece biro y cerámica, y los regateos se cruzan en varias lenguas a medio entender. Nubiri-sha vigila de lejos quién da y quién recibe, anotando en su memoria cada deuda.",
        "efecto": {},
        "agentes_involucrados": ["Watapana", "Nabaraka", "Chorota", "Biro-ko", "Nubiri-sha"],
    },
    {
        "id": "ofrenda_ancestros_anochecer",
        "nombre": "Ofrenda del anochecer a los ancestros",
        "descripcion": "Al caer la luz, las familias dejan un poco de casabe y chicha junto al lugar donde reposan los huesos de los mayores. Bana-mana recita en voz baja los nombres de los muertos para que no se olviden, y los niños escuchan los nombres que un día tendrán que repetir ellos.",
        "efecto": {"nivel_tension": "bajo"},
        "agentes_involucrados": ["Bana-mana", "Sha-korie", "Paugis-sha"],
    },
    {
        "id": "vigilancia_perimetro_amanecer",
        "nombre": "Relevo de vigilancia en el perímetro",
        "descripcion": "Antes de que aclare, Chiriware reparte los puestos de guardia mirando hacia el este, de donde vienen los Caribes. Los jóvenes guerreros se frotan los ojos y ocupan sus lugares; Dara-bana ya escruta el horizonte del Golfete buscando velas que no deberían estar.",
        "efecto": {"nivel_tension": "bajo"},
        "agentes_involucrados": ["Chiriware", "Taku-ko", "Pari-nu", "Dara-bana", "Chiri-ko"],
    },
    {
        "id": "preparar_chicha",
        "nombre": "Preparación de la chicha de maíz",
        "descripcion": "Las mujeres mastican el maíz cocido y escupen la pasta en la múcura de barro para que fermente, un trabajo paciente que tomará días. La chicha agria es para la fiesta que viene; mientras tanto huele a grano dulce y fuego, y las niñas aprenden mirando cómo se mide el agua.",
        "efecto": {"nivel_alimentos": "normal"},
        "agentes_involucrados": ["Naure-sha", "Wama-sha", "Sha-korie", "Tawi"],
    },
]

EVENTOS_ESTACIONALES = [
    {
        "id": "sequia_inicio",
        "nombre": "Inicio de sequía",
        "descripcion": "El buko baja. Los conucos se resienten. Tensión sobre el agua.",
        "efecto": {"nivel_alimentos": "escaso", "nivel_tension": "alto"},
        "agentes_involucrados": ["Manaure", "Shaboro", "Korie-ko", "Buko-ko"],
    },
    {
        "id": "tormenta_fuerte",
        "nombre": "Tormenta fuerte",
        "descripcion": "Manaure convoca ritual urgente. Su autoridad teocrática se activa.",
        "efecto": {"nivel_tension": "medio"},
        "agentes_involucrados": ["Manaure", "Shaboro", "toda_la_comunidad"],
    },
    {
        "id": "llegada_nabaraka",
        "nombre": "Nabaraka el Jirajara llega",
        "descripcion": "El comerciante serrano trae minerales y carne seca de la sierra.",
        "efecto": {},
        "agentes_involucrados": ["Nabaraka", "Raka-bi", "Watapana", "Biro-ko"],
    },
    {
        "id": "rumor_raid_caribe",
        "nombre": "Rumor de raid Caribe",
        "descripcion": "Dara-bana vio canoas extrañas al este. Chiriware activa el perímetro.",
        "efecto": {"nivel_tension": "alto"},
        "agentes_involucrados": ["Chiriware", "Dara-bana", "Manaure", "Tawaka", "guerreros"],
    },
    {
        "id": "ceremonia_iniciacion",
        "nombre": "Ceremonia de iniciación",
        "descripcion": "Dare-nu y Daru serán iniciados. La comunidad entera participa.",
        "efecto": {"nivel_tension": "bajo"},
        "agentes_involucrados": ["Manaure", "Shaboro", "Dare-nu", "Daru", "Paugis-sha"],
    },
    {
        "id": "watapana_parte_islas",
        "nombre": "Watapana parte a las islas",
        "descripcion": "El mercader principal sale en expedición. Estará fuera 8-10 días.",
        "efecto": {},
        "agentes_involucrados": ["Watapana", "Dara-ko", "Manaure", "Kadushi"],
    },

    # ── Nuevos eventos de la SECA (Tiempo de Viento) ──────────────
    {
        "id": "gran_cosecha_sal",
        "nombre": "Gran cosecha de sal de la seca",
        "estacion": "seca",
        "periodo": "viento",          # era 2: el alisio fabrica la sal (clima_era2.yaml)
        "descripcion": "El viento noreste sopla firme y las charcas del salinar se han secado por completo: es la gran cosecha del año. Toda mano disponible baja a raspar el biro hasta que los cestos rebosan, porque esta sal alimentará el trueque de muchas lunas. Biro-ko cuenta los montones con orgullo feroz mientras Manaure decide cuánto se guarda y cuánto se cambia.",
        "efecto": {"nivel_sal": "abundante", "nivel_tension": "bajo"},
        "agentes_involucrados": ["Biro-ko", "Manaure", "Watapana", "Moruy-sha", "Wama-ko"],
    },
    {
        "id": "expedicion_perlas",
        "nombre": "Temporada de buceo de perlas",
        "estacion": "seca",
        "periodo": "viento",          # era 2: agua clara y calma (ecologia-017)
        "descripcion": "Con el agua clara y calma de la seca, los buceadores se internan en el Golfete a arrancar las ostras de los bajíos, conteniendo el aliento hasta que los pulmones arden. Las perlas que salen de ellas no se comen, pero compran alianzas y esposas; un puñado vale más que una canoa de pescado. El riesgo es real: el mar se cobra a veces un buceador.",
        "efecto": {"nivel_tension": "medio"},
        "agentes_involucrados": ["Dara-ko", "Bagre-ko", "Tari-ko", "Piri", "Watapana"],
    },
    {
        "id": "fiesta_cosecha_chicha",
        "nombre": "Fiesta del fin de la seca",
        "estacion": "seca",
        "periodo": "seca_larga",      # era 2: «antes de que lleguen las lluvias»
        "descripcion": "Antes de que lleguen las lluvias la comunidad se reúne en la plaza: corre la chicha agria en las múcuras, suenan los tambores y las maracas, y los viejos cuentan las hazañas de los ancestros. Es noche de risas, alianzas y, a veces, de viejas rencillas que el licor desentierra; Manaure preside repartiendo el primer trago como símbolo de su mano.",
        "efecto": {"nivel_tension": "bajo", "nivel_alimentos": "abundante"},
        "agentes_involucrados": ["Manaure", "Nubiri-sha", "Bana-mana", "toda_la_comunidad"],
    },

    # ── Nuevos eventos de las LLUVIAS (Tiempo de Siembra) ─────────
    {
        "id": "ritual_siembra_primeras_lluvias",
        "nombre": "Ritual de las primeras lluvias",
        "estacion": "lluvias",
        "descripcion": "Las primeras nubes cargadas se amontonan sobre el llano y Shaboro guía el ritual para que la lluvia caiga buena y no como tormenta destructora. Se ofrenda casabe y se sopla humo hacia el cielo; Korie-ko ya ha preparado los conucos y aguarda la señal del piache para clavar las primeras estacas de yuca.",
        "efecto": {"nivel_tension": "bajo"},
        "agentes_involucrados": ["Shaboro", "Manaure", "Korie-ko", "Buio-sha", "Buko-ko"],
    },
    {
        "id": "crecida_buco",
        "nombre": "Crecida del buko",
        "estacion": "lluvias",
        "descripcion": "Las lluvias han llenado el buko hasta el borde y el agua corre por los canales hacia los conucos sedientos. Korie-ko y Buko-ko caminan las represas reparando filtraciones bajo el aguacero, aliviados y tensos a la vez: demasiada agua de golpe puede reventar las paredes de barro que tanto cuesta levantar.",
        "efecto": {"nivel_alimentos": "abundante", "nivel_tension": "bajo"},
        "agentes_involucrados": ["Korie-ko", "Buko-ko", "Ita-ko", "Wari-ko"],
    },
    {
        "id": "duelo_ritual_difunto",
        "nombre": "Duelo y ceremonia funeraria",
        "estacion": "lluvias",
        "descripcion": "Un mayor ha muerto y la comunidad se reúne bajo la lluvia para el duelo: se entona el llanto ritual, se prepara el cuerpo y se guardan sus huesos según la costumbre para que su barsure halle el camino. Paugis-sha y Sha-korie dirigen el lamento de las mujeres; Bana-mana añade el nombre del difunto a la lista de los que no deben olvidarse.",
        "efecto": {"nivel_tension": "medio"},
        "agentes_involucrados": ["Paugis-sha", "Sha-korie", "Shaboro", "Bana-mana"],
    },
]
