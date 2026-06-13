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
        "descripcion": "Lluvias frecuentes. Siembra y cultivo. Buco lleno. Menos navegación. Ceremonias.",
        "actividades_primarias": ["cultivar", "sembrar", "ritual_siembra", "construir"],
        "clima_base": "nublado, lluvias frecuentes, viento suave",
    },
}

MOMENTOS_DIA = ["amanecer", "mañana", "mediodia", "tarde", "anochecer", "noche"]

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
        "Tawaka-Corie-ko": {"nivel": "medio", "causa": "diferencia generacional sobre tradición"},
        "Chiriguare-Marokoto-ni": {"nivel": "alto", "causa": "desconfianza étnica profunda"},
        "Biro-ko-Tariwa": {"nivel": "medio", "causa": "disputa precio sal/pescado"},
        "Manaure-Kadushi": {"nivel": "bajo", "causa": "noticias de islas que cuestionan autoridad"},
    })

    # Notas del orquestador
    notas_orquestador: str = ""

    def avanzar_turno(self):
        """Avanza un turno (media jornada)."""
        if self.turno == 1:
            self.turno = 2
            self.momento = "tarde"
        else:
            self.turno = 1
            self.dia += 1
            self.momento = "amanecer"
            # Registrar evento del día anterior
            if self.evento_del_turno:
                self.historial_eventos.append({
                    "dia": self.dia - 1,
                    "evento": self.evento_del_turno
                })
                self.evento_del_turno = None

    def to_context_string(self) -> str:
        """Genera el string de contexto que se inyecta en cada llamada de agente."""
        est = ESTACIONES[self.estacion]
        lines = [
            f"[CURIANA — {est['nombre']}]",
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
        agentes_en_escena=["Manaure", "Shaboro", "Buio-sha", "Tawaka", "Dare-nu", "Corie-ko"],
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
        "agentes_involucrados": ["Bagre-ko", "Tariwa", "Guaranaro-sha"],
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
        "agentes_involucrados": ["Manaure", "Nubiri-sha", "Corie-ko"],
    },
    {
        "id": "canoa_islas_llega",
        "nombre": "Llega canoa de las islas",
        "descripcion": "La canoa de Kadushi llega desde Aruba con bienes y noticias.",
        "efecto": {},
        "agentes_involucrados": ["Kadushi", "Watapana", "Manaure", "Chiriguare"],
    },
]

EVENTOS_ESTACIONALES = [
    {
        "id": "sequia_inicio",
        "nombre": "Inicio de sequía",
        "descripcion": "El buco baja. Los conucos se resienten. Tensión sobre el agua.",
        "efecto": {"nivel_alimentos": "escaso", "nivel_tension": "alto"},
        "agentes_involucrados": ["Manaure", "Shaboro", "Corie-ko", "Buco-ko"],
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
        "descripcion": "Dara-bana vio canoas extrañas al este. Chiriguare activa el perímetro.",
        "efecto": {"nivel_tension": "alto"},
        "agentes_involucrados": ["Chiriguare", "Dara-bana", "Manaure", "Tawaka", "guerreros"],
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
]
