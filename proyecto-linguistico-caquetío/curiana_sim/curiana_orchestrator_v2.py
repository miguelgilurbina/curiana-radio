"""
CURIANA — Orquestador v2: Motor de Emergencia Lingüística
==========================================================
Versión refactorizada con lexicon engine, observer lingüístico,
reportes periódicos y simulación de largo plazo (días/meses/años).

Uso:
    python curiana_orchestrator_v2.py                     # interactivo
    python curiana_orchestrator_v2.py --auto 10           # 10 turnos
    python curiana_orchestrator_v2.py --auto 60 --anio    # 1 año simulado (60 dias = 120 turnos)
    python curiana_orchestrator_v2.py --auto 240 --reporte # 4 años simulados con reporte anual LLM
"""

import os
import sys
import json
import random
import argparse
from collections import Counter
from typing import Optional

import anthropic

# Cargar variables de entorno desde curiana_sim/.env (Supabase + Anthropic)
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass

# El elenco se elige ANTES de importar curiana_agents, porque todos los
# módulos importan su ALL_AGENTS al cargarse. --elenco era2 fija la variable;
# argparse lo vuelve a declarar más abajo sólo para la ayuda.
if "--elenco" in sys.argv:
    _i = sys.argv.index("--elenco")
    if _i + 1 < len(sys.argv):
        os.environ["CURIANA_ELENCO"] = sys.argv[_i + 1]

from curiana_database import get_anthropic_client, get_db
from curiana_agents import (
    ALL_AGENTS, AGENTS_T1, AGENTS_T2, AGENTS_T3,
    ELENCO, MUNDO, ROSTER_NUCLEO,
)
from huella_de_base import huella as huella_de_base, resumen as resumen_huella
from curiana_state import (
    ComunidadState,
    DIAS_POR_ESTACION,
    DIAS_POR_ANIO,
    estacion_equivalente,
    estado_inicial,
    momento_de_turno,
    EVENTOS_COTIDIANOS,
    EVENTOS_ESTACIONALES,
    MOMENTOS_DIA,
    LOCACIONES,
)
from curiana_lexicon import (
    LexicoComunitario,
    vocabulario_para_agente,
    prompt_lexico_activo,
    score_linguistico,
    prompt_rescate_linguistico,
    PUERTA_DEL_RECUENTO,
    IDENTIDAD_LINGUISTICA,
    olvidar_raices_onomatopeyicas,
    VOCABULARIO_BASE,
)
from curiana_observer import ObserverAgent
from curiana_social import (
    DifusionLexica,
    necesita_rescate,
    prompt_rasgos_dialectales,
)
from curiana_koine import (
    IdiolectoAgente,
    CampoLexico,
    CompetenciaLexica,
    REFERENTES_NOVEDOSOS,
    agentes_sin_precarga,
    estimulo_de_referente,
    referentes_del_mundo,
    toca_nombrar,
    emocionar_de,
    fijar_semilla,
    prompt_emocionar,
    prompt_idiolecto,
    distancia_idiolectal,
    guardar_koine,
    cargar_koine,
    semilla_de_precarga_guardada,
)
from curiana_cadena import (
    cadena_de_runs,
    config_de,
    linea_de_brazo,
    lineas_de_serie,
    resumen_de_cadena,
    serie_koine_de_cadena,
    texto_veredicto,
)
from curiana_eventos import (
    alias_del_elenco,
    catalogo_para_elenco,
    decir_para_el_mundo,
    elenco_era1,
)
from curiana_director import director_system, guardar_reflexion, reflexion_del_dia
from curiana_mundo import resumen_del_mundo
# La escena por lugar (era 2, --escena). Con la escena apagada —que es como
# viene— `ambito_de` devuelve None, `escena_de` {} y `bloque_aqui_estas` "":
# importar este módulo no cambia un byte del prompt, ni en la era 1 ni en la 2.
from curiana_escena import (
    CAPUBANA_CADA_POR_DEFECTO,
    ambito_de,
    ambito_visible_de,
    bloque_aqui_estas,
    bloque_lo_que_se_dijo_aqui,
    dichos_del_turno,
    escena_de,
    es_dia_de_capubana,
    glosa_de as glosa_de_lugar,
    volcado_de_escena,
)
from functools import lru_cache


# ══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS_AGENT = 500      # Espacio para frases en caquetío + glosa + neologismos
MAX_TOKENS_DIRECTOR = 600

# Koiné: roster FIJO de participantes (población constante desde el día 1). Se
# rota una ventana sobre este roster cada turno, de modo que todos hablan en los
# primeros ~2 días — a diferencia de la entrada gradual anterior, que inflaba la
# distancia idiolectal en el medio del run y confundía la métrica de convergencia.
# Mezcla caquetíos nucleares + periféricos + foráneos/de contacto (la mezcla que
# se asienta en koiné). Se filtra a los existentes en ALL_AGENTS al usarse.
PARTICIPANTES_KOINE = [
    # caquetíos nucleares (formadores de norma)
    "Manaure", "Shaboro", "Nubiri-sha", "Buio-sha", "Tawaka", "Dare-nu",
    "Korie-ko", "Paugis-sha",
    # caquetíos periféricos
    "Watapana", "Dara-ko", "Biro-ko", "Saruro-sha", "Chiriware",
    # contacto insular / caribe
    "Kadushi", "Marokoto-ni",
    # foráneos (aportantes de la mezcla)
    "Tariwa", "Kawa-ni", "Piru-sha", "Tari-ko", "Wata-ni",
    "Nabaraka", "Raka-bi", "Chorota",
]

# Constante de identidad lingüística — inyectada en TODOS los agentes.
# Vive en `curiana_lexicon` desde el corte de serie del 2026-09-18 (es una
# plantilla de prompt, y la puerta de las formas de plantilla tiene que poder
# leerla sin importar el bucle). El texto no cambió un byte; este alias es
# para que nadie tenga que cambiar de sitio para leerla.
_IDENTIDAD_LINGUISTICA = IDENTIDAD_LINGUISTICA

# Lo que las plantillas ENSEÑAN no puede contar como koiné: el run db946685
# (bitácora, 2026-09-14) tenía «ta-barsure naba-ni» en el 17,5 % de las
# respuestas como piso constante de copia, y esas formas flexionadas no están
# en VOCABULARIO_BASE, así que la métrica emergente y el diccionario koiné las
# contaban como convergencia. Se excluyen junto con el vocabulario base.
#
# Desde el 2026-09-18 es LA MISMA lista que la puerta del registro
# (`curiana_lexicon.FORMAS_DE_PLANTILLA`): eran dos y una de las dos no se
# respetaba, así que `kali-bana` se descontaba de la métrica emergente y a la
# vez se registraba, se adoptaba y competía. Una sola puerta, declarada donde
# están las plantillas. Trae además lo que enseñan el refuerzo y el rescate,
# que esta lista no miraba (`ma-arua`, `wa-duna`, `wana-ni`, `cati`).
#
# Y desde el corte de serie del 2026-09-20 trae también LA RAÍZ DE NINGUNA
# PARTE. El orquestador mete en el campo léxico todo lo que el agente acuñó
# —`campo.registrar([n.forma for n in neos_turno])`— sin preguntar si el
# léxico lo aceptó, así que sin esto `lumina-bana-uco` seguiría saliendo en el
# diccionario koiné del cierre y pesando en la distancia emergente, que es la
# lectura del veredicto. No es una lista: es un predicado con `__contains__`
# (`curiana_lexicon.PUERTA_DEL_RECUENTO`), porque las raíces posibles no se
# pueden enumerar.
_FORMAS_EXCLUIDAS = PUERTA_DEL_RECUENTO

# Elenco que habla. Miguel, 2026-09-14: «me gustaría que todos los agentes
# hablen, porque si no ¿para qué tenerlos ahí?» y «los foráneos no deberían
# entrar de momento». El roster `todos` son todos los agentes de etnia caquetía
# (incluidos los tier 3 y los mestizos o insulares), sin los foráneos; `koine`
# es el roster fijo de 23 con el que corrió la era 1.
ETNIAS_FORANEAS = frozenset({"caribe", "gayón", "guaycarí", "jirajara"})


def es_foraneo(agente: dict) -> bool:
    etnia = (agente.get("etnia") or "caquetío").lower()
    return etnia in ETNIAS_FORANEAS


def roster_de_habla(nombre: str = "koine") -> list[str]:
    """Quiénes rotan hablando. `koine`: los 23 de la era 1. `todos`: todos los
    agentes no foráneos, en el orden del roster koiné primero (formadores de
    norma) y luego el del elenco."""
    if nombre == "koine":
        return [a for a in PARTICIPANTES_KOINE if a in ALL_AGENTS]
    if nombre == "nucleo":
        # Los que el casting de la era 2 hace rotar de continuo (en_roster);
        # sin elenco de la era 2 cae al roster koiné.
        r = [a for a in ROSTER_NUCLEO if a in ALL_AGENTS and not es_foraneo(ALL_AGENTS[a])]
        return r or roster_de_habla("koine")
    if nombre != "todos":
        raise ValueError(f"roster desconocido: {nombre!r} (koine | nucleo | todos)")
    primero = [a for a in PARTICIPANTES_KOINE if a in ALL_AGENTS and not es_foraneo(ALL_AGENTS[a])]
    resto = [a for a, d in ALL_AGENTS.items() if a not in primero and not es_foraneo(d)]
    return primero + resto


# Las zonas de pesca de la era 2 dichas para un hablante, no en clave
# (6-fusion/estructura_social_era2.yaml, decision_creativa_2026-09-14).
ZONAS_DE_PESCA = {
    "ZG2": "la orilla del Golfete",
    "ZA1": "la costa oeste, de Punta Cardón a Los Taques",
}


def prompt_gente(agent: dict) -> str:
    """El nodo, la casa y el sitio del agente, para el prompt. Sólo el elenco
    de la era 2 los trae; en la era 1 devuelve vacío. Es la pieza que la
    auditoría 2026-09-14 §7 echaba en falta: ninguna parte del prompt sabía en
    qué nodo estaba el agente."""
    if not agent.get("nodo"):
        return ""
    partes = [f"tu nodo es {agent['nodo']}", f"tu casa, la de {agent.get('casa')}",
              f"tu sitio, {agent.get('sitio')}"]
    linaje = str(agent.get("linaje") or "").split(" (")[0].strip()
    if linaje:
        partes.append(f"tu linaje, {linaje}")
    zona = ZONAS_DE_PESCA.get(agent.get("zona_de_pesca") or "")
    if zona and agent.get("sitio") == "Caseto":
        # Decisión de Miguel 2026-09-16 (tanda del 15, p5): Caseto está a ~22 km
        # de su playa. Conuco principal, pesca de visita: de sus 12, 2 son de mar.
        partes.append(f"tu gente siembra en Caseto; los que pescan bajan a {zona}, a un día de ida")
    elif zona:
        partes.append(f"tu gente pesca en {zona}")
    return ("[Tu gente]: " + "; ".join(partes) + ". Hay otro nodo al otro lado del "
            "cerro, que habla a su manera; sólo os juntáis en el Capubana y por los "
            "que se casaron cruzando.")


# ══════════════════════════════════════════════════════════════════════
# CLIENTE
# ══════════════════════════════════════════════════════════════════════

def get_client(run_id: Optional[str] = None) -> anthropic.Anthropic:
    """
    Devuelve el cliente Anthropic con LangSmith wrapping si está configurado.
    Delega a curiana_database.get_anthropic_client() para unificar setup.
    """
    return get_anthropic_client(run_id=run_id)


# ══════════════════════════════════════════════════════════════════════
# MEMORIA DE AGENTES (rolling: las últimas MAX_NOTAS notas)
# ══════════════════════════════════════════════════════════════════════
# Eran 3 notas de turno. Con los días encadenados (--continuar) el cierre de
# cada día añade una nota por agente con lo que hizo —los momentos en que
# habló y lo que acuñó—, y hacen falta ranuras para que esa nota sobreviva a
# los turnos del día siguiente.

class AgentMemory:
    MAX_NOTAS = 5

    def __init__(self):
        self._memory: dict[str, list[str]] = {}

    def add(self, agent_name: str, note: str):
        self._memory.setdefault(agent_name, []).append(note)
        self._memory[agent_name] = self._memory[agent_name][-self.MAX_NOTAS:]

    def get(self, agent_name: str) -> Optional[str]:
        notes = self._memory.get(agent_name, [])
        return " | ".join(notes) if notes else None

    def save(self, path="curiana_memory.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._memory, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path="curiana_memory.json") -> "AgentMemory":
        m = cls()
        try:
            with open(path, encoding="utf-8") as f:
                m._memory = json.load(f)
        except FileNotFoundError:
            pass
        return m


# ══════════════════════════════════════════════════════════════════════
# LLAMADA A AGENTE (con léxico inyectado)
# ══════════════════════════════════════════════════════════════════════

def _invoke(client: anthropic.Anthropic, system: str, user_message: str) -> str:
    """Una llamada cruda al modelo del agente."""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_AGENT,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )
    return resp.content[0].text.strip()


def call_agent(
    client: anthropic.Anthropic,
    agent_name: str,
    state: ComunidadState,
    lexico: LexicoComunitario,
    observer: ObserverAgent,
    user_message: str,
    agent_memory: Optional[str] = None,
    difusion: Optional[DifusionLexica] = None,
    idiolectos: Optional[dict] = None,
    competencia: Optional["CompetenciaLexica"] = None,
    campo: Optional[CampoLexico] = None,
    ablacion: bool = False,
    capas: Optional[frozenset] = None,
) -> str:
    agent = ALL_AGENTS.get(agent_name)
    if not agent:
        return f"[Agente '{agent_name}' no encontrado]"

    tier = agent.get("tier", 2)
    etnia = agent.get("etnia", "caquetío")

    # System prompt base del agente. Los tier 3 de la era 1 no traen
    # system_prompt (se arma aquí); los de la era 2 lo traen generado, con su
    # nodo, su casa y su sitio.
    if tier == 3:
        base_prompt = agent.get("system_prompt") or (
            f"Eres {agent_name} de la Curiana, comunidad caquetía del Golfete de Coro. "
            f"{agent.get('descripcion', '')} Responde brevemente en personaje."
        )
    else:
        base_prompt = agent.get("system_prompt", f"Eres {agent_name} de la Curiana.")

    # ⚠ El MENSAJE pasa por el traductor, no sólo el system prompt. El estímulo
    # de un turno con evento es «[Situación]: {state.evento_del_turno}…», y
    # hasta el 2026-09-17 se mandaba crudo: el bloque del mundo iba traducido
    # desde #143, pero el user_message no, así que el evento semilla de la era
    # 1 llegó a los agentes por esta puerta. Medido en el run b06f57ea: 23 de
    # 72 respuestas del día 1 dijeron «Shaboro» y 16 «Buio-sha» (12 de 12 en
    # el turno 2), mientras el Director —cuya puerta sí traducía— decía
    # «Sawaka». Si no sobrevive ninguna frase, el agente recibe el momento del
    # día antes que un mensaje vacío (la API lo rechaza).
    dicho = decir_para_el_mundo(user_message, state.mundo).strip()
    user_message = dicho or MOMENTOS_ESTIMULO.get(state.momento, "¿Qué haces ahora?")

    # El estímulo del turno nombra el sitio del agente (era 2) o la Curiana.
    # Va DESPUÉS del traductor: el marcador no es texto del mundo.
    user_message = user_message.replace("{lugar}", agent.get("sitio") or "la Curiana")

    # Contexto dinámico del mundo, dicho para el elenco activo. En la era 1 es
    # el mismo string; en la era 2 pasa por curiana_eventos.decir_para_el_mundo()
    # porque el estado semilla de la era 1 (estado_inicial_test) trae «Shaboro
    # salió de su choza… Buio-sha lo vio desde lejos» en evento_del_turno. Desde
    # el 2026-09-17 un run de la era 2 arranca de estado_inicial('PARAGUANÁ') y
    # ya no lo trae; el traductor se queda porque un estado continuado puede
    # venir de antes y porque el catálogo no es la única puerta.
    world_context = decir_para_el_mundo(state.to_context_string(), state.mundo)

    # Ubicación actual. Con la escena encendida (era 2, --escena) la puerta es
    # `ambito_de`: el LUGAR donde el agente está en este momento del día, que
    # es lo que run_turn acaba de escribir en `ubicaciones_override`. Sin
    # escena —la era 1 y la era 2 sin el flag— devuelve None y se lee lo de
    # siempre: el override (que nadie escribe) o su ubicacion_default.
    #
    # ESTAR no es VER, y son dos puertas (curiana_escena, 2026-09-18):
    #   `ambito`       DÓNDE ESTÁ  → [Aquí estás] y la ubicación de siempre; es
    #                  también el que `run_turn` le declara al léxico con
    #                  `situar()`, así que es el que queda escrito en la
    #                  acuñación y en la adopción.
    #   `ambito_visto` QUÉ VE      → el filtro de todo lo comunitario que entra
    #                  al prompt (capa 2, PR 4): las propuestas en evaluación
    #                  (V1), las adoptadas (V2), las competencias abiertas (V3)
    #                  y el campo léxico que pondera la muestra (V4).
    # Coinciden todos los días menos el de Capubana, donde `ambito` es
    # "Capubana" —allí está la gente— y `ambito_visto` es None: ese día no hay
    # frontera y las cuatro vías vuelven a ser de la comunidad entera, que es
    # lo que la convergencia significa (diseño §4, decisión p7).
    # Con `None` las cuatro vías son globales y el prompt es el de siempre.
    ambito = ambito_de(agent_name, state)
    ambito_visto = ambito_visible_de(agent_name, state)
    ubicacion = ambito or state.ubicaciones_override.get(
        agent_name, agent.get("ubicacion_default", "plaza")
    )

    # Léxico + reglas apropiadas para el tier (priorizado por el contexto
    # del turno: evento del mundo + ubicación + mensaje — ver chunking en
    # curiana_lexicon.categorias_relevantes)
    # Ablación (run de control): se apagan las tres inyecciones que EMPUJAN
    # la convergencia desde el prompt — muestreo rich-get-richer (pesos),
    # sugerencias de contagio y competencias abiertas. La medición (observer,
    # difusión, competencia como registro) sigue intacta: la diferencia entre
    # un run normal y uno --ablacion es cuánta convergencia es emergente vs.
    # inducida por el andamiaje.
    contexto_turno = f"{world_context} {ubicacion} {user_message}"
    # V4: el muestreo rich-get-richer se pondera con el campo DE ESTE LUGAR.
    # Sin ámbito, `pesos_de(None)` es el campo global de siempre — el mismo
    # objeto, no una copia: el sorteo sale idéntico.
    pesos_campo = (campo.pesos_de(ambito_visto)
                   if (campo is not None and not ablacion) else None)
    bloque_lexico = vocabulario_para_agente(
        tier, lexico, contexto=contexto_turno, pesos=pesos_campo, capas=capas,
        ambito=ambito_visto,
    )

    # Feedback lingüístico si el agente tuvo score bajo
    feedback = observer.feedback_para_agente(agent_name)

    # Rasgos dialectales según etnia (L2 con sintaxis propia, insulares, etc.)
    rasgos = prompt_rasgos_dialectales(etnia)

    # Contagio: palabras que el agente "ha oído" de gente que respeta
    sugerencia_contagio = ""
    if difusion is not None and not ablacion:
        sugs = difusion.sugerencias_para(agent_name, lexico=lexico)
        if sugs:
            txt = "; ".join(f"{f} = {s}" if s else f for f, s in sugs)
            sugerencia_contagio = (
                f"[Has oído estas palabras nuevas en boca de gente que respetas; "
                f"empléalas si encajan]: {txt}"
            )

    # Ensamblado del system prompt
    # Orden: persona → identidad lingüística → dialecto → mundo → léxico → contagio → memoria → refuerzo
    system_parts = [base_prompt, "---", _IDENTIDAD_LINGUISTICA]
    # Emocionar (Maturana): disposición que moldea CÓMO lenguajea — semilla de
    # idiolecto. Va junto a la identidad lingüística.
    system_parts.append(prompt_emocionar(agent_name, etnia))
    if rasgos:
        system_parts.append(rasgos)
    # [Aquí estás] SUSTITUYE a [Tu ubicación] cuando hay escena: dónde estás,
    # qué momento del día es y quiénes están contigo, en ≤ 200 caracteres
    # (curiana_escena.bloque_aqui_estas). Sin escena devuelve "" y la línea es
    # la de siempre, carácter a carácter.
    aqui_estas = bloque_aqui_estas(agent_name, state)
    system_parts += ["---", world_context,
                     aqui_estas or f"[Tu ubicación]: {ubicacion}"]
    # [Lo que se dijo aquí] (capa 2, decisión p5 → A): las ≤ 3 intervenciones
    # del MOMENTO ANTERIOR que se dijeron en este mismo lugar, ≤ 280 car. Va
    # pegado a [Aquí estás] porque es la otra mitad de la misma idea: el lugar.
    # Sin escena, y en el primer turno de un run nuevo, devuelve "".
    se_dijo_aqui = bloque_lo_que_se_dijo_aqui(agent_name, state)
    if se_dijo_aqui:
        system_parts.append(se_dijo_aqui)
    gente = prompt_gente(agent)
    if gente:
        system_parts.append(gente)
        # [Tu tierra] (2026-09-16): el mundo por sitio, período y momento, en
        # ≤ 320 caracteres (decisiones p1-p8 de la tanda del 15). Sólo la era 2:
        # la Curiana de la era 1 no tiene canon de sitios.
        if agent.get("sitio") and state.mundo == "PARAGUANÁ":
            from curiana_mundo import bloque_tu_tierra
            tierra = bloque_tu_tierra(agent.get("sitio"), state.estacion, state.momento,
                                      agente=agent_name, dia=state.dia, capas=capas)
            if tierra:
                system_parts.append(tierra)
    if bloque_lexico:
        system_parts.append(bloque_lexico)
    if sugerencia_contagio:
        system_parts.append(sugerencia_contagio)
    # Competencias léxicas abiertas: empuja a reusar una forma rival que ya
    # circula (en vez de inventar otra) → una se impone y se fija en la koiné.
    if competencia is not None and not ablacion:
        # V3 con ámbito: sólo las formas rivales que se propusieron AQUÍ. La
        # fijación sigue siendo comunitaria — el ámbito filtra lo que se VE.
        bloque_comp = competencia.prompt_competencias(ambito=ambito_visto)
        if bloque_comp:
            system_parts.append(bloque_comp)
    # Idiolecto acumulado (entrenchment): "tu manera de hablar" derivada del
    # perfil de frecuencia del agente. Reemplaza/enriquece la memoria cruda.
    if idiolectos is not None and agent_name in idiolectos:
        bloque_idio = prompt_idiolecto(idiolectos[agent_name])
        if bloque_idio:
            system_parts.append(bloque_idio)
    if agent_memory:
        system_parts.append(f"[Tu memoria reciente]: {agent_memory}")
    if feedback:
        system_parts.append(feedback)

    system = "\n".join(system_parts)

    # 1ª pasada
    response = _invoke(client, system, user_message)

    # ── RESCATE INTRA-TURNO (auditoría §3.4, extendido): un único reintento
    #    si la densidad es baja (español) O si el agente recurrió mucho a
    #    otra lengua arahuaca (wayunaiki/lokono/taíno) en vez de caquetío —
    #    esa fuga es más sutil que el español pero igual de indeseada, el
    #    objetivo es que el caquetío DOMINE, no solo "no hablar español" ──
    metr = score_linguistico(response, lexico)
    # D3 (#34, 2026-09-01): el umbral se evalúa sobre el score NORMALIZADO
    # por dialecto, y en ablación no hay rescate — curiana_social.
    # necesita_rescate(). A la base va siempre el score CRUDO.
    if necesita_rescate(metr, etnia, ablacion):
        rescate = prompt_rescate_linguistico(
            response, metr["score"], metr.get("espanol_funcional", 0),
            metr.get("palabras_otro_arahuaco"),
        )
        try:
            response2 = _invoke(client, system, user_message + "\n\n" + rescate)
            metr2 = score_linguistico(response2, lexico)
            mejor = metr2["score"] > metr["score"] or metr2.get("pct_caquetio_especifico", 0) > metr.get("pct_caquetio_especifico", 0)
            if mejor:
                response = response2
        except Exception:
            pass  # ante fallo de red, conserva la 1ª respuesta

    return response


# ══════════════════════════════════════════════════════════════════════
# DIRECTOR / NARRADOR
# ══════════════════════════════════════════════════════════════════════

# El Director habla del mundo que el elenco fija: «de la Curiana» en la era 1,
# «de Paraguaná» en la 2 (curiana_director.director_system; el texto de la era
# 1 es el de siempre). Hasta el 2026-09-16 era «de la Curiana» también en
# Paraguaná, y sin mundo: inventó «la sombra del ceibo» (ecologia-032).
DIRECTOR_SYSTEM = director_system(MUNDO)


def director_narrate(
    client: anthropic.Anthropic,
    state: ComunidadState,
    interactions: list[dict],
) -> str:
    """El cierre narrativo del turno. En la era 2 lleva el mundo —la frase
    del período, la del momento y las restricciones del corpus, ≤ 400
    caracteres (curiana_mundo.resumen_del_mundo)—, el elenco en escena y, si
    hay, lo que el Director dejó anotado al cerrar el día anterior. El cierre
    queda en state.cierres_del_dia para la reflexión del día (--reflexion).

    Todo el texto libre que entra —el estado, las intervenciones y las notas—
    pasa por decir_para_el_mundo(): en la era 1 es el mismo string byte a byte;
    en la era 2 se traducen los nombres y se caen las frases con marcos que
    Paraguaná no tiene. Sin eso, el Director del día 3 (run 0193873d) escribió
    «Los Caquetíos y Guaycarí se juntan…» copiando su propia nota del día 2."""
    decir = lambda t: decir_para_el_mundo(t, state.mundo)                 # noqa: E731
    linea = lambda i: f"- {i['agent']}: {decir(i['response'])[:100]}..."  # noqa: E731
    # Decisión 6 → A (Miguel, 2026-09-17): con escena, el Director sigue siendo
    # UNO por turno —cero llamadas más— pero recibe las intervenciones
    # AGRUPADAS POR LUGAR. No mueve ninguna métrica de lengua (su texto no
    # llega al prompt del agente, diseño §1.6): arregla la coherencia del
    # mundo, que es lo que le hizo escribir «las canoas volverán al Golfete»
    # para gente que no estaba en el Golfete. Sin escena, el resumen es el de
    # siempre, byte a byte.
    escena = getattr(state, "escena_del_turno", None) or {}
    if escena:
        por_lugar: dict = {}
        for i in interactions:
            por_lugar.setdefault(escena.get(i["agent"]) or "", []).append(i)
        bloques = []
        for lugar in sorted(por_lugar):
            bloques.append(f"[{glosa_de_lugar(lugar) or 'sin lugar'}]")
            bloques += [linea(i) for i in por_lugar[lugar]]
        resumen = "\n".join(bloques)
    else:
        resumen = "\n".join(linea(i) for i in interactions)
    partes = [f"Estado: {decir(state.to_context_string())}"]
    if state.mundo == "PARAGUANÁ":
        mundo = resumen_del_mundo(state)
        if mundo:
            partes.append(mundo)
        gente = list(dict.fromkeys(i["agent"] for i in interactions if i.get("agent")))
        if gente:
            partes.append("[La gente que hay hoy]: " + ", ".join(gente)
                          + ". No nombres a nadie que no esté en esta lista.")
    notas = decir(state.notas_orquestador or "").strip()[:400]
    if notas:
        partes.append("[Lo que el Director dejó anotado al cerrar el día anterior]: " + notas)
    partes.append(f"Interacciones: {resumen}")
    partes.append("Escribe el cierre narrativo del turno (2-3 oraciones).")
    prompt = "\n".join(partes)
    # El mundo que se narra es el del estado (en un run coincide con el del
    # elenco: state.fijar_mundo(MUNDO)); si difieren, manda el estado.
    system = DIRECTOR_SYSTEM if state.mundo == MUNDO else director_system(state.mundo)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_DIRECTOR,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    texto = resp.content[0].text.strip()
    state.cierres_del_dia = (list(state.cierres_del_dia) + [texto])[-max(1, state.turnos_por_dia):]
    return texto


@lru_cache(maxsize=None)
def _eventos_del_elenco() -> tuple[list, list]:
    """El catálogo de curiana_state dicho para el elenco activo (curiana_eventos):
    la era 1 intacta; la era 2 con los nombres traducidos por ALIAS_ERA1, sin
    foráneos y sin los eventos que sólo tienen sentido con ellos. Antes
    run_turn filtraba `agentes_involucrados` con `a in ALL_AGENTS` y nunca
    resolvía el alias: en la era 2 casi ningún evento traía a sus
    protagonistas y el Director narraba «Biro-ko» en Paraguaná."""
    era1 = elenco_era1()
    foraneos = frozenset(n for n, a in era1.items() if es_foraneo(a))
    alias = alias_del_elenco(ELENCO)
    sin_equivalente = frozenset(set(era1) - set(alias) - foraneos)
    return catalogo_para_elenco(ELENCO, alias, foraneos, sin_equivalente)


def director_select_event(state: ComunidadState) -> Optional[dict]:
    prob = 0.3
    if state.nivel_tension == "alto":
        prob += 0.2
    if state.nivel_alimentos == "escaso":
        prob += 0.15
    if state.dia % 3 == 0:
        prob += 0.3
    if random.random() > prob:
        return None
    # El pool estacional se filtra por la CLAVE "estacion" de cada evento, no
    # por posición en la lista. Antes se partía con [:3]/[3:], lo que dejaba
    # los tres eventos etiquetados `seca` dentro del pool de lluvias y hacía
    # inalcanzables otros tres genéricos. Un evento sin clave `estacion` vale
    # para todo el año.
    # Era 2 (2026-09-16): el estado trae un período (viento/seca_larga/siembra)
    # y los eventos están escritos en estaciones de la era 1; se comparan por
    # equivalencia (viento → seca). Un evento con `periodo` es más fino y sólo
    # cae en ese período: la gran cosecha de sal y las perlas en el viento, la
    # fiesta de fin de seca en la seca larga (clima_era2.yaml).
    equiv = estacion_equivalente(state.estacion)
    def _cae(e: dict) -> bool:
        if e.get("periodo") and equiv != state.estacion:      # el mundo tiene períodos
            return e["periodo"] == state.estacion
        return e.get("estacion") in (None, state.estacion, equiv)
    # Los eventos, dichos para el elenco activo (era 2: sin nombres de la era 1
    # ni foráneos; ver _eventos_del_elenco y curiana_eventos).
    cotidianos, estacionales = _eventos_del_elenco()
    pool = cotidianos + [e for e in estacionales if _cae(e)]
    return random.choice(pool)


# ══════════════════════════════════════════════════════════════════════
# TURNO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

# {lugar} lo rellena call_agent con el sitio del agente (era 2) o «la Curiana».
MOMENTOS_ESTIMULO = {
    "amanecer": "Amanece en {lugar}. ¿Qué estás haciendo al comenzar el día?",
    "mañana":   "La mañana avanza en {lugar}. ¿En qué estás trabajando?",
    "mediodia": "Es mediodía. El calor obliga al descanso. ¿Dónde estás y qué piensas?",
    "tarde":    "La tarde en {lugar}. ¿Qué haces o con quién hablas?",
    "anochecer":"El sol cae sobre {lugar}. ¿Cómo terminas tu día?",
    "noche":    "La noche cae. ¿Qué pensamientos tienes?",
}


def referentes_pendientes_de(state: ComunidadState) -> list[dict]:
    """Los referentes novedosos que a esta comunidad aún no le han puesto
    delante, en el orden de su catálogo. Un run que continúa sigue
    la secuencia donde el día anterior la dejó (state.referentes_introducidos);
    uno nuevo la empieza. Antes cada run la reiniciaba y un día de seis turnos
    sólo llega al primero: la serie A nombró las mismas cuentas tres días.

    El catálogo depende del MUNDO (tanda de la base, 2026-09-23): la era 2 lee
    `6-fusion/referentes_era2.yaml` y la era 1 sigue con REFERENTES_NOVEDOSOS."""
    vistos = set(state.referentes_introducidos)
    return [dict(r) for r in referentes_del_mundo(state.mundo)
            if r["id"] not in vistos]


def run_turn(
    client: anthropic.Anthropic,
    state: ComunidadState,
    memory: AgentMemory,
    lexico: LexicoComunitario,
    observer: ObserverAgent,
    user_input: Optional[str] = None,
    verbose: bool = True,
    db=None,
    run_id: Optional[str] = None,
    difusion: Optional[DifusionLexica] = None,
    idiolectos: Optional[dict] = None,
    campo: Optional[CampoLexico] = None,
    competencia: Optional[CompetenciaLexica] = None,
    naming_referente: Optional[dict] = None,
    ablacion: bool = False,
    capas: Optional[frozenset] = None,
    db_fallos: Optional[Counter] = None,
    agentes_por_turno: int = 6,
    roster: Optional[list[str]] = None,
) -> list[dict]:
    """Un turno. `agentes_por_turno` es la ventana que habla; `roster`, sobre
    quiénes rota (None = el roster koiné de la era 1, ver roster_de_habla).
    En un turno con evento hablan primero los agentes que el evento nombra y
    la ventana se completa con la rotación, para que cada turno tenga el
    mismo número de voces."""
    interactions = []
    if db_fallos is None:
        db_fallos = Counter()  # descartable si el caller no lo pidió
    roster_explicito = roster is not None
    roster = list(roster) if roster_explicito else [a for a in PARTICIPANTES_KOINE if a in ALL_AGENTS]
    roster_set = set(roster)

    # ── 0. LA ESCENA DEL TURNO (era 2, --escena) ──────────────────────
    # Dónde está cada uno de LOS 63 en este momento del día, no sólo los 12
    # que hablan: un mapa con 12 de 63 no es un mundo. Se escribe en
    # `ubicaciones_override`, el campo que llevaba cuatro lectores —el prompt
    # (:355) y curiana_social.vecinos() (:134, :149)— y cero escrituras. Va
    # ANTES de elegir la ventana, pero no la toca: la escena dice dónde está
    # cada uno, no quién habla (decisión 4 → A). Con la escena apagada
    # devuelve {} y aquí no pasa nada.
    escena = escena_de(state)
    state.escena_del_turno = escena
    if escena:
        state.ubicaciones_override = dict(escena)

    def _ventana() -> list[str]:
        # Ventana rotatoria sobre el roster, avanzando `agentes_por_turno` por
        # turno. Contador GLOBAL de turnos (no state.turno, que cicla dentro
        # del día): con state.turno la ventana se clavaba y de 23 participantes
        # solo hablaban 12.
        if not roster:
            return list(state.agentes_en_escena)
        n_turno = (state.dia - 1) * state.turnos_por_dia + (state.turno - 1)
        k = (n_turno * agentes_por_turno) % len(roster)
        return [roster[(k + i) % len(roster)]
                for i in range(min(agentes_por_turno, len(roster)))]

    # Evento de nombramiento: aparece un referente sin palabra caquetía y se
    # presenta a TODOS los agentes activos este turno → acuñan formas rivales
    # para el MISMO concepto (induce la competencia que la koiné luego fija).
    naming_concepto: Optional[str] = None
    if naming_referente and competencia is not None:
        naming_concepto = naming_referente["id"]
        competencia.activar(naming_concepto, naming_referente["desc"],
                            animal=bool(naming_referente.get("animal")))
    # La puerta onomatopéyica (db.6): abierta SÓLO en el turno en que se
    # nombra a un animal, y sólo para lo que se registra ese turno. Se cierra
    # al final de run_turn. Sin animal —la era 1, el cometa— queda cerrada.
    lexico.puerta_onomatopeyica = (
        naming_concepto if naming_concepto and naming_referente.get("animal")
        else None)

    # 1. Director: ¿hay evento?
    evento = director_select_event(state)
    if evento:
        state.evento_del_turno = evento["descripcion"]
        state.eventos_activos = [evento["id"]]
        # Los efectos declarados por el evento SÍ mueven el mundo: sin esto,
        # "gran cosecha de sal" se narraba y la sal seguía escasa al turno
        # siguiente, y el contexto inyectado a los agentes era invariable.
        state.aplicar_efecto(evento.get("efecto"))
        involucrados = [
            a for a in evento.get("agentes_involucrados", state.agentes_en_escena)
            if a in ALL_AGENTS and a not in ("toda_la_comunidad", "guerreros")
        ]
        if roster_explicito:
            # Con roster declarado, un evento no mete a quien el roster deja
            # fuera (los foráneos, de momento).
            involucrados = [a for a in involucrados if a in roster_set]
        agentes_activos = involucrados or [a for a in state.agentes_en_escena if a in roster_set][:5]
        for a in _ventana():
            if len(agentes_activos) >= agentes_por_turno:
                break
            if a not in agentes_activos:
                agentes_activos.append(a)
    else:
        agentes_activos = _ventana()

    # 1b. Registrar el turno en la DB — DESPUÉS de que el Director decida.
    #     Antes iba primero, así que `turns.event_description` guardaba el
    #     evento del turno ANTERIOR: cuando el Director elegía uno nuevo, la
    #     fila decía una cosa y los agentes recibían otra (b06f57ea: la fila
    #     del turno 3 dice el evento semilla y el turno 3 corrió con «Los
    #     pescadores regresan…»). Y se guarda ya DICHO para el mundo activo:
    #     la era 1 escribe el mismo string; la era 2, sin nombres de la era 1.
    turn_id: Optional[str] = None
    if db and run_id:
        try:
            turn_id = db.save_turn(
                run_id=run_id,
                day=state.dia,
                turn_num=state.turno,
                moment=state.momento,
                season=state.estacion,
                event_description=decir_para_el_mundo(
                    state.evento_del_turno or "", state.mundo).strip() or None,
            )
        except Exception as e:
            db_fallos["turns"] += 1
            if verbose:
                print(f"  ⚠ DB turn error: {e}")

    # 1c. Las presencias: los 63 con su lugar, no sólo los 12 que hablan. Es
    #     lo que hace posible el visor sobre el mapa (PR 10) y la brecha por
    #     LUGAR. La escribe el agente de la base (PR 3, en paralelo): aquí
    #     sólo se llama si el método existe, para que las dos ramas puedan
    #     entrar en cualquier orden.
    if escena and db and run_id and turn_id:
        guardar_presencias = getattr(db, "save_presencias", None)
        if guardar_presencias is not None:
            try:
                guardar_presencias(run_id=run_id, turn_id=turn_id, dia=state.dia,
                                   turno=state.turno, momento=state.momento,
                                   escena=state.escena_del_turno)
            except Exception:
                db_fallos["presencias"] += 1

    if verbose:
        print(f"\n{'='*60}")
        print(f"  DÍA {state.dia} | TURNO {state.turno} | {state.momento.upper()}")
        print(f"  {state.estacion.upper()} — {state.clima}")
        if state.evento_del_turno:
            print(f"  📍 {state.evento_del_turno}")
        # El visor de texto (PR 8): la escena del turno en una línea, para que
        # se pueda depurar desde el primer run sin esperar al mapa. Va dentro
        # del bloque verboso, así que --silencioso no lo ve.
        if escena and es_dia_de_capubana(state):
            print("  ▲ DÍA DE CAPUBANA: los dos nodos en el cerro, los seis momentos")
        volcado = volcado_de_escena(state, escena)
        if volcado:
            print(f"  {volcado}")
        print(f"{'='*60}\n")

    # 2. Estímulo del turno. Todo lo que sale de aquí pasa por
    #    decir_para_el_mundo() dentro de call_agent: el evento va crudo y se
    #    traduce en la puerta. El nombramiento nombra el mundo del estado
    #    —«ALGO NUEVO EN PARAGUANÁ»—; escrito «EN LA CURIANA», el traductor de
    #    la era 2 se habría comido la frase entera (Curiana es un marco de
    #    MARCOS_FUERA_ERA2) y con ella el referente que hay que nombrar.
    if naming_concepto:
        donde = "LA CURIANA" if state.mundo == "CURIANA" else state.mundo
        # NOVEDAD o HUECO, con «[Lo que se oye]» si lo hay (db.4, db.6). Para
        # un referente sin `tipo` —la era 1— es el molde de siempre, carácter a
        # carácter (test_tanda_base).
        stimulus = estimulo_de_referente(naming_referente, donde)
        if verbose:
            print(f"  ✦ NOMBRAMIENTO: {naming_referente['desc'][:60]}")
    elif user_input:
        stimulus = user_input
    elif state.evento_del_turno:
        stimulus = f"[Situación]: {state.evento_del_turno}. ¿Cómo reaccionas?"
    else:
        stimulus = MOMENTOS_ESTIMULO.get(state.momento, "¿Qué haces ahora?")

    # 3. Activar agentes. Los tier 3 hablan también (antes se saltaban aquí
    # aunque un evento los llamara): call_agent ya les arma su prompt corto.
    for agent_name in agentes_activos[:agentes_por_turno]:
        if agent_name not in ALL_AGENTS:
            continue
        agent = ALL_AGENTS[agent_name]
        tier = agent.get("tier", 2)

        # DÓNDE ESTÁ QUIEN VA A HABLAR. La misma puerta que usa el prompt, y
        # la única. Se le declara al léxico ANTES de que el Observer registre
        # nada: `registrar_neologismo()` y `adoptar()` los llama él —y el
        # Observer no se toca, es el registro de la medición—, así que el
        # lugar tiene que estar puesto de antemano para que la acuñación
        # sepa dónde nació y la adopción, en qué ámbito se oficializó.
        # Sin escena esto pone None y todo se comporta como siempre.
        ambito_hablante = ambito_de(agent_name, state)
        lexico.situar(agent_name, ambito_hablante)

        mem = memory.get(agent_name)
        response = call_agent(
            client, agent_name, state, lexico, observer, stimulus, mem,
            difusion=difusion, idiolectos=idiolectos, competencia=competencia,
            campo=campo, ablacion=ablacion, capas=capas,
        )

        interaccion = {
            "agent": agent_name,
            "tier": tier,
            "etnia": agent.get("etnia", "caquetío"),
            "response": response,
            "momento": state.momento,
            "neologismos": [],
        }
        interactions.append(interaccion)

        # Análisis lingüístico por el Observer
        registro = observer.analizar(
            agente=agent_name,
            etnia=agent.get("etnia", "caquetío"),
            tier=tier,
            texto=response,
            dia=state.dia,
            turno=state.turno,
            momento=state.momento,
            estacion=state.estacion,
        )

        interaccion["neologismos"] = [
            n.forma for n in getattr(registro, "neologismos_extraidos", [])]

        # Detectar adopciones de palabras propuestas por otros
        neos_oficializados = observer.procesar_adopciones(
            response, agent_name, state.turno, dia=state.dia)

        # Contagio: propagar exposición de las palabras emergentes que usó este
        # agente (no las del vocabulario base) a sus vecinos sociales.
        if difusion is not None:
            for forma in getattr(registro, "palabras_caquetias", []):
                if forma not in VOCABULARIO_BASE:
                    difusion.propagar_uso(forma, agent_name, state)
            for neo in getattr(registro, "neologismos_extraidos", []):
                difusion.propagar_uso(neo.forma, agent_name, state)

        # Competencia léxica: en un turno de nombramiento, las formas acuñadas
        # son variantes rivales del concepto presentado. En cualquier turno, el
        # reuso de una forma ya en competencia le suma soporte (la hace ganar).
        if competencia is not None:
            for neo in getattr(registro, "neologismos_extraidos", []):
                if naming_concepto:
                    competencia.proponer(naming_concepto, neo.forma, agent_name,
                                         ambito=ambito_hablante)
                else:
                    competencia.registrar_uso(neo.forma, agent_name)
            for forma in getattr(registro, "palabras_caquetias", []):
                competencia.registrar_uso(forma, agent_name)

        # Koiné: actualizar idiolecto del agente (entrenchment) y campo léxico
        # comunitario (frecuencia para muestreo + métrica de convergencia).
        formas_usadas = getattr(registro, "palabras_caquetias", [])
        neos_turno = getattr(registro, "neologismos_extraidos", [])
        if idiolectos is not None:
            if agent_name not in idiolectos:
                idiolectos[agent_name] = IdiolectoAgente(
                    agent_name, emocionar_de(agent_name, agent.get("etnia")))
            idiolectos[agent_name].registrar(formas_usadas, neos_turno)
        if campo is not None:
            # V4: la frecuencia se acumula EN EL LUGAR donde se dijo. El campo
            # global sigue siendo la suma de los lugares, así que el
            # diccionario koiné del cierre y `guardar_koine` no cambian.
            campo.registrar(formas_usadas, ambito=ambito_hablante)
            campo.registrar([n.forma for n in neos_turno], ambito=ambito_hablante)

        # Persistir en Supabase
        if db and run_id and turn_id:
            try:
                # Extraer listas del registro
                words_used = list(getattr(registro, "palabras_caquetias", []))
                aspects_used = list(getattr(registro, "aspectos_usados", []))
                neos = getattr(registro, "neologismos_extraidos", [])
                neo_count = len(neos)

                # La forma que se ACUÑA es una palabra usada por quien la
                # acuña. `score_linguistico` no la ve —sólo reconoce
                # `lexico.palabras_activas()` (base + adoptados) y una
                # acuñación recién propuesta no está ahí—, así que
                # `palabras_caquetias` no la traía y `word_uses` registraba
                # como PRIMER usuario al adoptante, que puede ser del otro
                # nodo: 29 de 40 acuñaciones de la era 2 (72,5%, medido por
                # analizar_nodos.py el 2026-09-16). Eso invierte las rutas de
                # contagio que se leen de `word_uses`. Va aparte de
                # `words_used` —no se toca el scorer ni, por tanto, la serie—
                # y con `source_language='caquetío'` declarado: una acuñación
                # pasó la compuerta fonotáctica, no está en el lexicón y
                # `word_source_language()` la dejaría en NULL.
                acunadas = [n.forma for n in neos
                            if n.forma and n.forma not in words_used]

                # DÓNDE SE DIJO. La columna existe desde #155 y
                # `save_agent_response` la acepta, pero nadie se la pasaba: el
                # día 1 de la serie C (run b7bc51dc) cerró con 0 de 72 filas
                # con lugar mientras `presencias` tenía las 378. Va el ÁMBITO
                # del hablante —el mismo `ambito_de` que filtró lo que vio y
                # que se le declaró al léxico arriba—, nunca el nodo, que no es
                # lo mismo. Sin escena es None y `save_agent_response` no
                # menciona siquiera la columna: la fila es la de siempre.
                response_id = db.save_agent_response(
                    turn_id=turn_id,
                    run_id=run_id,
                    agent_name=agent_name,
                    ethnicity=agent.get("etnia", "caquetío"),
                    tier=tier,
                    response_text=response,
                    score=registro.score,
                    words_used=words_used,
                    aspects_used=aspects_used,
                    neologisms_proposed=neo_count,
                    coined_words=acunadas,
                    lugar=ambito_hablante,
                )
                registro.response_id = response_id

                # Préstamos de la esfera de contacto: tabla aparte y con su
                # lengua real, para leer la difusión tier 1 → tier 2/3 desde
                # la base en vez de re-puntuar response_text a mano (deuda
                # del run c6837386, 2026-09-16). No entran en words_used.
                prestamos = list(getattr(registro, "prestamos_de_esfera", []))
                if prestamos:
                    try:
                        db.save_loanword_uses(
                            response_id=response_id,
                            run_id=run_id,
                            turn_id=turn_id,
                            agent_name=agent_name,
                            tier=tier,
                            day=state.dia,
                            turn_num=state.turno,
                            words=prestamos,
                        )
                    except Exception:
                        db_fallos["loanword_uses"] += 1

                # Persistir neologismos propuestos
                for neo in neos:
                    try:
                        db.save_neologism(
                            run_id=run_id,
                            turn_id=turn_id,
                            proposed_by=agent_name,
                            proposed_day=state.dia,
                            form=neo.forma,
                            components=getattr(neo, "componentes", ""),
                            meaning=neo.significado,
                            morphological_rule=getattr(neo, "regla_aplicada", "desconocida"),
                        )
                    except Exception:
                        # No interrumpir por neologismo fallido, pero contarlo:
                        # perder escrituras en silencio corrompe el análisis.
                        db_fallos["neologisms"] += 1

                # Sincronizar adopciones oficializadas este turno (antes solo
                # se actualizaba el LexicoComunitario en memoria; Supabase
                # quedaba con status="propuesto" para siempre)
                for neo_oficial in neos_oficializados:
                    try:
                        db.update_neologism_status(
                            form=neo_oficial.forma,
                            run_id=run_id,
                            status="adoptado",
                            adopted_by=neo_oficial.adoptado_por,
                            adopted_turn_id=turn_id,
                        )
                    except Exception:
                        db_fallos["neologism_status"] += 1

            except Exception as e:
                db_fallos["agent_responses"] += 1
                if verbose:
                    print(f"  ⚠ DB agent error ({agent_name}): {e}")

        # Guardar en memoria del agente
        memory.add(agent_name, f"D{state.dia}T{state.turno}: {response[:70]}")

        if verbose:
            print(f"  [{agent_name} — {agent.get('etnia','caquetío').upper()}]")
            print(f"  {response}")
            score_bar = "●" * int(registro.score) + "○" * (10 - int(registro.score))
            print(f"  ╰─ {score_bar} {registro.score}/10")
            for neo in registro.neologismos_extraidos:
                print(f"     ✦ NUEVO: [{neo.forma}] = {neo.significado}")
            print()

    # 3b. LO QUE SE DIJO AQUÍ, para el momento SIGUIENTE (capa 2, decisión
    #     p5 → A). Se guarda al CERRAR el turno y se lee al abrir el que
    #     viene: dentro del mismo turno nadie oye a nadie, que es lo que
    #     separa este bloque de la V1 —el orden de habla dejaría de ser
    #     destino sólo si oír cuesta un turno para todos por igual. Cada
    #     frase pasa por decir_para_el_mundo(), como el resto del texto libre
    #     que llega al agente, y se guarda la frase caquetía sin su glosa.
    #     Sin escena la lista queda vacía y el bloque no existe.
    if escena:
        state.dichos_del_turno_anterior = dichos_del_turno(
            escena, interactions,
            decir=lambda t: decir_para_el_mundo(t, state.mundo),
        )

    # 4. Narración del director
    if interactions and verbose:
        narration = director_narrate(client, state, interactions)
        print(f"  ── Narrador ──")
        print(f"  {narration}")

    # 5. Reporte Observer del turno
    if verbose:
        print(observer.reporte_turno(state.dia, state.turno))

    # 6. Avanzar estado
    if campo is not None:
        campo.decaer()  # recambio léxico: formas no usadas pierden peso
    # En PARAGUANÁ el evento dura UN turno y no más: el día tiene seis momentos
    # y el evento es la situación de UNO de ellos, así que al cerrar el turno
    # se archiva y se apaga. Si el Director no elige otro en el turno
    # siguiente, el estímulo vuelve a ser el momento del día; repetirlo es
    # decisión suya, que puede volver a elegirlo. En CURIANA no se toca: dos
    # turnos por día y el evento dura el día, como siempre (avanzar_turno).
    # Medido el 2026-09-17 sobre `turns`: sin esto el evento semilla fue la
    # situación de los turnos 1-3 del run b06f57ea, «Los pescadores regresan…»
    # la de los turnos 4-5, y «Poco pescado. Los Guaycarí…» la de los turnos
    # 4-6 del run 89fc1744.
    if state.mundo == "PARAGUANÁ":
        state.cerrar_evento_del_turno()
    state.avanzar_turno()
    # La puerta onomatopéyica vale un turno (db.6).
    lexico.puerta_onomatopeyica = None

    return interactions


# ══════════════════════════════════════════════════════════════════════
# MODO INTERACTIVO
# ══════════════════════════════════════════════════════════════════════

def interactive_mode(client: anthropic.Anthropic):
    print("\n" + "="*60)
    print("  CURIANA — Laboratorio de Emergencia Lingüística v2")
    print("  Golfete de Coro · Falcón · Siglo XIV-XV")
    print("="*60)

    try:
        state = ComunidadState.load()
        print("  → Estado cargado.")
    except Exception:
        # El estado inicial es el del MUNDO que fija el elenco, no el de la
        # era 1 (ver auto_mode y curiana_state.estado_inicial).
        state = estado_inicial(MUNDO)
        print("  → Nuevo test run.")
    state.fijar_mundo(MUNDO)

    memory = AgentMemory.load()
    lexico = LexicoComunitario.load()
    lexico_anterior = len(lexico.neologismos_adoptados())

    try:
        obs_client = client
        observer = ObserverAgent.load(obs_client, lexico)
    except Exception:
        observer = ObserverAgent(client, lexico)

    # Difusión léxica (contagio sociolingüístico) — persiste durante todo el run
    difusion = DifusionLexica()

    # Koiné: idiolecto por agente + campo léxico (ver auto_mode)
    idiolectos = {
        nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia")))
        for nm, a in ALL_AGENTS.items()
    }
    campo = CampoLexico()
    competencia = CompetenciaLexica()
    db_fallos: Counter = Counter()

    # Inicializar DB (gracefully degraded si no hay Supabase)
    db = get_db()
    # La huella se sella al arrancar: sin ella no se puede saber, mirando el
    # run, sobre qué lexicón/corpus/elenco corrió (issue #68).
    _h = huella_de_base()
    print(f"  base: {resumen_huella(_h)}")
    run_id = db.create_run(model=MODEL,
                           config={"mode": "interactive", **_h})
    client = get_client(run_id)  # re-crear con run_id para LangSmith

    print(f"\n  Vocabulario disponible: {len(lexico.palabras_activas())} palabras")
    print(f"  Situación: {state.evento_del_turno or 'La Curiana despierta.'}")
    print(f"  Run ID: {run_id[:8]}...\n")

    # #42: mismo cierre garantizado que auto_mode. total_turns contaba
    # state.turno (sólo vale 1 o 2) y total_days no restaba el día en curso.
    turnos_hechos = 0
    try:
        while True:
            try:
                user_input = input("  [CURIANA]> ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not user_input:
                turnos_hechos += 1
                run_turn(client, state, memory, lexico, observer, db=db, run_id=run_id,
                         difusion=difusion, idiolectos=idiolectos, campo=campo,
                         competencia=competencia, db_fallos=db_fallos)
            elif user_input.lower() == "salir":
                break
            elif user_input.lower() == "estado":
                print(f"\n{state.to_context_string()}\n")
            elif user_input.lower() == "lexico":
                print(f"\n{lexico.reporte_linguistico()}\n")
            elif user_input.lower() == "ranking":
                print("\n  Ranking lingüístico:")
                for agente, score in observer.ranking_linguistico():
                    bar = "█" * int(score) + "░" * (10 - int(score))
                    print(f"    {agente:15} {bar} {score:.1f}/10")
                print()
            elif user_input.lower().startswith("habla "):
                agent_name = user_input[6:].strip()
                if agent_name not in ALL_AGENTS:
                    print(f"  Agente no encontrado. Disponibles: {', '.join(list(AGENTS_T1.keys())[:8])}...")
                else:
                    try:
                        msg = input(f"  ¿Qué le dices a {agent_name}? > ").strip()
                        response = call_agent(
                            client, agent_name, state, lexico, observer, msg,
                            memory.get(agent_name), difusion=difusion,
                            idiolectos=idiolectos,
                        )
                        print(f"\n  [{agent_name}]: {response}\n")
                        observer.analizar(
                            agent_name,
                            ALL_AGENTS[agent_name].get("etnia", "caquetío"),
                            ALL_AGENTS[agent_name].get("tier", 2),
                            response, state.dia, state.turno, state.momento, state.estacion
                        )
                        memory.add(agent_name, f"D{state.dia}: conversación directa")
                    except (EOFError, KeyboardInterrupt):
                        break
            elif user_input.lower().startswith("evento "):
                evento_id = user_input[7:].strip()
                todos = EVENTOS_COTIDIANOS + EVENTOS_ESTACIONALES
                ev = next((e for e in todos if e["id"] == evento_id), None)
                if ev:
                    state.evento_del_turno = ev["descripcion"]
                    state.eventos_activos = [evento_id]
                    print(f"  Evento '{ev['nombre']}' activado.")
                else:
                    print(f"  IDs disponibles: {[e['id'] for e in todos]}")
            elif user_input.lower() == "reporte dia":
                print(observer.reporte_dia(state.dia - 1))
            elif user_input.lower() == "exportar":
                observer.exportar_csv()
                observer.exportar_neologismos_csv()
            else:
                turnos_hechos += 1
                run_turn(
                    client, state, memory, lexico, observer,
                    user_input=user_input, db=db, run_id=run_id,
                    difusion=difusion, idiolectos=idiolectos, campo=campo,
                    competencia=competencia, db_fallos=db_fallos,
                )
    finally:
        # Guardar todo
        state.save()
        memory.save()
        lexico.save()
        observer.save()
        observer.exportar_csv()
        observer.exportar_neologismos_csv()

        # Cerrar run
        db.end_run(run_id, total_turns=turnos_hechos, total_days=state.dia - 1)
    if db_fallos:
        print(f"  ⚠ {sum(db_fallos.values())} escritura(s) a DB fallaron: "
              + ", ".join(f"{t}×{n}" for t, n in db_fallos.most_common()))
    print("  Guardado. ¡Hasta la próxima jornada en la Curiana!")


# ══════════════════════════════════════════════════════════════════════
# MODO AUTOMÁTICO (con reportes periódicos)
# ══════════════════════════════════════════════════════════════════════

def _imprimir_cadena(db, run_id: Optional[str]) -> None:
    """La serie y el veredicto de la CADENA entera, al cerrar un run continuado.

    En la era 2 un run es un día: su propia serie tiene un punto y el veredicto
    dice siempre «datos insuficientes». La evidencia de koiné vive en la cadena
    `continuado_desde`, que este bloque lee de la base y juzga con el MISMO
    criterio (`curiana_cadena.veredicto`).

    Sin base (modo JSON) no hay cadena que leer y no se imprime nada; un fallo
    al leerla se avisa y no tumba el reporte de un run ya terminado."""
    if not db or not run_id:
        return
    try:
        cadena = cadena_de_runs(db, run_id)
        if len(cadena) < 2:
            return                      # run suelto: su propia serie ya se dijo
        avisos: list[str] = []
        serie = serie_koine_de_cadena(db, run_id, avisos=avisos, cadena=cadena)
        print(f"\n  CADENA — {len(cadena)} runs encadenados: {resumen_de_cadena(cadena)}")
        brazo = linea_de_brazo(cadena)
        if brazo:
            print(f"    {brazo}")
        for aviso in avisos:
            print(f"    ⚠ {aviso}")
        if not serie:
            print("    (sin días medidos en la cadena)")
            return
        for linea in lineas_de_serie(serie):
            print(f"    {linea}")
        print(f"    {texto_veredicto(serie)}")
    except Exception as e:
        print(f"\n  ⚠ no se pudo leer la cadena de runs: {e}")


class BrazoIncompatible(SystemExit):
    """Una cadena `--continuar` que cambiaría de brazo a la mitad."""


def comprobar_brazo_de_escena(db, state, escena: bool, capubana_cada: int):
    """Un run continuado tiene que correr con el MISMO brazo que el anterior.

    «Una escena no puede entrar a mitad de cadena: es una serie nueva desde el
    día 1» (diseño §5.4). Si el run anterior corrió con escena y éste no —o al
    revés—, el motor avisa y se niega: la diferencia entre brazos es la
    evidencia, y una cadena mitad y mitad no la mide, la ensucia.

    Se mira primero la CONFIG del run anterior, que es donde el brazo queda
    sellado; si no hay base que leer (modo JSON, mock, o un run que no está),
    se cae al estado en disco, que también lo recuerda. Si ninguno de los dos
    dice nada, se avisa y se sigue: no hay con qué comparar.
    """
    anterior = None
    origen = ""
    run_id = getattr(state, "run_anterior", None)
    if db is not None and run_id:
        try:
            run = db.get_run(run_id)
        except Exception:                                    # noqa: BLE001
            run = None
        if run:
            cfg = config_de(run)
            if "escena" in cfg:
                anterior = (bool(cfg.get("escena")), cfg.get("capubana_cada") or 0)
                origen = f"la config del run {str(run_id)[:8]}"
    if anterior is None and getattr(state, "escena", None) is not None:
        anterior = (bool(state.escena), int(getattr(state, "capubana_cada", 0) or 0))
        origen = "el estado en disco (curiana_state.json)"
    if anterior is None:                                     # pragma: no cover
        print("  ⚠ no se pudo leer el brazo del run anterior: la cadena sigue sin comprobar")
        return
    ahora = (bool(escena), int(capubana_cada) if escena else 0)
    if anterior == ahora:
        return
    di = lambda b, n: ("con escena" if b else "sin escena") + (      # noqa: E731
        f", Capubana cada {n}" if b and n else "")
    raise BrazoIncompatible(
        "\n  ✗ --continuar con OTRO brazo: el run anterior corrió "
        f"{di(*anterior)} y éste pediría {di(*ahora)}.\n"
        f"    (leído de {origen})\n"
        "    Una escena no puede entrar ni salir a mitad de cadena: la\n"
        "    evidencia es la DIFERENCIA entre dos cadenas completas con la\n"
        "    misma semilla, no una cadena mitad y mitad. Arranca una serie\n"
        "    nueva desde el día 1 (--serie ...) o repite el brazo anterior.\n"
    )


def config_resuelta(
    turnos: int,
    perfil: "Perfil",
    agentes_por_turno: int = 6,
    roster_nombre: str = "koine",
    turnos_por_dia: Optional[int] = None,
    semilla: Optional[int] = None,
    continuar: bool = False,
    reflexion: bool = False,
    serie: Optional[str] = None,
    escena: bool = False,
    capubana_cada: int = CAPUBANA_CADA_POR_DEFECTO,
    ablacion: bool = False,
) -> dict:
    """Lo que el run diría de sí mismo, ANTES de gastar nada.

    Es la misma resolución que hace `auto_mode`: el perfil manda sobre los
    flags sueltos, `capubana_cada` sólo significa algo con escena, y
    `continuado_desde` sale del estado en disco, que es de donde `--continuar`
    lo saca. No llama a la API, ni a la base, ni a git: lee el YAML de
    perfiles (que ya está cargado) y `curiana_state.json` si lo hay."""
    continuado = None
    if continuar:
        try:
            continuado = ComunidadState.load().run_anterior
        except Exception:                                # noqa: BLE001
            continuado = None
    return {
        "turnos": int(turnos),
        "elenco": ELENCO,
        "mundo": MUNDO,
        "agentes": len(ALL_AGENTS),
        "perfil": perfil.nombre,
        "capas": len(perfil.capas),
        "andamiaje": perfil.andamiaje,
        "ablacion": bool(perfil.ablacion or ablacion),
        "serie": serie,
        "agentes_por_turno": int(agentes_por_turno),
        "roster": roster_nombre,
        "roster_n": len(roster_de_habla(roster_nombre)),
        "turnos_por_dia": turnos_por_dia,
        "semilla": semilla,
        "continuar": bool(continuar),
        "continuado_desde": continuado,
        "reflexion": bool(reflexion),
        "escena": bool(escena),
        "capubana_cada": int(capubana_cada) if escena else None,
    }


def imprimir_dry_run(cfg: dict) -> None:
    """`--dry-run`: la config resuelta y nada más. Cero llamadas, cero filas."""
    print(f"\n{'='*60}")
    print("  --dry-run: la config resuelta. No se llama a nada.")
    print(f"{'='*60}")
    orden = ["turnos", "elenco", "mundo", "agentes", "perfil", "capas",
             "andamiaje", "ablacion", "serie", "agentes_por_turno", "roster",
             "roster_n", "turnos_por_dia", "semilla", "continuar",
             "continuado_desde", "reflexion", "escena", "capubana_cada"]
    for clave in orden:
        valor = cfg.get(clave)
        print(f"  {clave:20} {'—' if valor is None else valor}")
    if cfg["escena"]:
        cada = cfg["capubana_cada"]
        print(f"\n  brazo: con escena" +
              (f", Capubana cada {cada} día(s)" if cada else ", sin Capubana"))
    else:
        print("\n  brazo: sin escena (el de control: el prompt es el de siempre)")
    if cfg["continuar"] and not cfg["continuado_desde"]:
        print("  ⚠ --continuar sin run anterior en curiana_state.json: "
              "el run arrancaría del estado que haya, sin `continuado_desde`")
    print(f"{'='*60}\n")


def auto_mode(
    client: anthropic.Anthropic,
    turnos: int,
    reporte_anual: bool = False,
    verbose: bool = True,
    perfiles: bool = False,
    ablacion: bool = False,
    perfil: Optional["Perfil"] = None,
    agentes_por_turno: int = 6,
    roster_nombre: str = "koine",
    turnos_por_dia: Optional[int] = None,
    semilla: Optional[int] = None,
    continuar: bool = False,
    reflexion: bool = False,
    serie: Optional[str] = None,
    escena: bool = False,
    capubana_cada: int = CAPUBANA_CADA_POR_DEFECTO,
):
    """
    Corre N turnos automáticamente.
    Genera reportes al final de cada día, estación y año simulado.

    ablacion=True → run de CONTROL: se apagan las inyecciones de prompt que
    empujan la convergencia (contagio, competencias abiertas, muestreo
    ponderado). Comparar un run normal contra su ablación separa la
    convergencia emergente de la inducida por el andamiaje.

    agentes_por_turno / roster_nombre → cuántos hablan por turno y sobre qué
    elenco rota la ventana (ver roster_de_habla). La era 1: 6 sobre `koine`.

    turnos_por_dia → cuántos turnos tiene un día (la era 1: 2). Con 6 se
    recorren los seis momentos del día.

    semilla → fija el azar del motor (eventos, muestras, nombramientos) y se
    sella en la huella del run. El modelo sigue siendo no determinista.

    continuar=True → encadena días: arranca del estado, la memoria, el lexicón,
    el observer y la koiné (idiolectos y campo) que dejó el run anterior en
    disco, y declara en su config de qué run viene. Lo que NO se hereda todavía:
    la difusión social y las competencias léxicas abiertas.

    reflexion=True → al cerrar cada día, UNA llamada más: el Director, con el
    mundo, lee los cierres del día y el reporte medido y escribe 4-6 oraciones
    (curiana_director.reflexion_del_dia). Va al log, a state.notas_orquestador
    (el día siguiente la ve) y a curiana_director.json. Apagado por defecto.

    escena=True → el BRAZO de la escena por lugar (curiana_escena.py, era 2):
    cada turno, cada uno de los 63 tiene un lugar; el prompt cambia
    `[Tu ubicación]` por `[Aquí estás]` y el Director recibe las
    intervenciones agrupadas por lugar. Apagado por defecto: sin el flag, el
    prompt de la era 2 es byte a byte el de hoy y el de la era 1 también. Se
    sella en simulation_runs.config junto con `capubana_cada`, y una cadena
    NO puede cambiar de brazo a la mitad (el motor se niega).

    capubana_cada → cada cuántos días convergen los dos nodos en el cerro
    (decisión 7 → A del 2026-09-17; 3 en la primera cadena). Sólo cuenta con
    escena=True.

    Mapeo temporal (con turnos_por_dia = 2):
        1 turno = media jornada
        2 turnos = 1 día
        60 días = 1 estación (seca o lluvias)
        120 días = 1 año (2 estaciones)
        → 240 turnos = 1 año simulado completo
    """
    if semilla is not None:
        random.seed(semilla)
    # La pre-carga de idiolectos sortea sus formas con su propio dado
    # (blake2b sobre semilla+nombre), no con el RNG global: el motor lo
    # comparte con eventos, muestreo y nombramientos, y la semilla tiene que
    # ser reproducible aunque cambie el orden en que se consume el azar.
    fijar_semilla(semilla)

    if continuar:
        state = ComunidadState.load()
        memory = AgentMemory.load()
        lexico = LexicoComunitario.load()
        try:
            observer = ObserverAgent.load(client, lexico)
        except Exception:                                    # noqa: BLE001
            observer = ObserverAgent(client, lexico)
        # La competencia léxica viaja con la koiné desde el 2026-09-18: sin
        # ella, una disputa abierta moría al amanecer (y con un run = un día,
        # ninguna podía fijarse jamás). Un JSON anterior devuelve una vacía.
        idiolectos, campo, competencia = cargar_koine()
        # La semilla de la PERSONA es la de la CADENA (db.3, tanda de la base,
        # 2026-09-23): el dado de la ficha —formas-semilla y aspecto de
        # respaldo del emocionar— se fija con la semilla con que se sembró el
        # día 1, y `random.seed()` sigue con la del día (eventos, muestreo,
        # nombramientos). Antes, a 7 de 63 agentes el `[Tu emocionar]` les
        # cambiaba de un día a otro. Un JSON anterior no la trae: sigue la del
        # día, como hasta entonces, y el aviso de abajo lo dice.
        semilla_de_la_persona = semilla_de_precarga_guardada()
        if semilla_de_la_persona is not None:
            fijar_semilla(semilla_de_la_persona)
        # Un agente nuevo en el elenco arranca con su semilla de idiolecto.
        for nm, a in ALL_AGENTS.items():
            idiolectos.setdefault(nm, IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia"))))
        # ⚠ La semilla NO se recupera continuando. `cargar_koine` reconstruye
        # los idiolectos con peso_semilla=0 a propósito (las frecuencias
        # guardadas ya traen la semilla del día 1), así que una cadena que
        # arrancó SIN pre-carga no la va a tener nunca por seguir encadenando:
        # hay que re-correr desde el día 1. Se mide y se avisa.
        sin_precarga = agentes_sin_precarga(idiolectos, ALL_AGENTS)
        if sin_precarga and semilla_de_la_persona is not None:
            print(f"  ⚠ cadena sin pre-carga de idiolectos: {len(sin_precarga)} de "
                  f"{len(ALL_AGENTS)} agentes heredan un idiolecto sin ninguna "
                  f"de sus formas-semilla (viene de un run anterior al "
                  f"2026-09-16). Continuar NO la recupera: hay que re-correr "
                  f"la cadena desde el día 1.")
        elif sin_precarga:
            # Sin la semilla de la cadena, las formas se derivan con la del
            # día y el aviso puede ser falso: medido el 2026-09-21, una cadena
            # bien sembrada daba 2 de 63 el día 2 y 3 de 63 el día 3.
            print(f"  ⚠ {len(sin_precarga)} de {len(ALL_AGENTS)} agentes sin sus "
                  f"formas-semilla — pero la koiné guardada no dice con qué "
                  f"semilla se sembró (motor anterior al 2026-09-23), así que "
                  f"el aviso puede ser falso. Ver 6-fusion/issues-pendientes/"
                  f"semilla-del-dia-mueve-a-la-persona-2026-09-21.md.")
        # El estado guardado apunta al turno siguiente al último corrido, así
        # que un día completo anterior deja al nuevo run en el amanecer.
    else:
        # El estado del día 1 es el del MUNDO que fija el elenco. Hasta el
        # 2026-09-17 todo run que no continuaba arrancaba del de la era 1:
        # «Shaboro salió de su choza… Buio-sha lo vio desde lejos», la escena
        # y las tensiones de la Curiana, y `estacion="seca"`, en Paraguaná.
        state = estado_inicial(MUNDO)
        memory = AgentMemory()
        lexico = LexicoComunitario()
        observer = ObserverAgent(client, lexico)
        # Koiné: idiolecto por agente (pre-cargado con su emocionar → divergencia
        # inicial) + campo léxico comunitario + serie temporal de distancia
        # idiolectal (la métrica de convergencia: debe CONTRAERSE).
        idiolectos = {
            nm: IdiolectoAgente(nm, emocionar_de(nm, a.get("etnia")))
            for nm, a in ALL_AGENTS.items()
        }
        campo = CampoLexico()
        # Un run que no continúa empieza la competencia de cero, como siempre.
        competencia = CompetenciaLexica()
        # El día 1 siembra la cadena: su semilla es la de la persona.
        semilla_de_la_persona = semilla
        # Y empieza sin raíces onomatopéyicas admitidas (db.6); al continuar,
        # `LexicoComunitario.load()` las reconstruye de lo guardado.
        olvidar_raices_onomatopeyicas()
    if turnos_por_dia is not None:
        state.turnos_por_dia = int(turnos_por_dia)
        if not continuar:
            state.momento = momento_de_turno(state.turno, state.turnos_por_dia)
    # El elenco decide el mundo que encabeza el contexto y su calendario: la
    # era 2 arranca en el Tiempo de Viento, no en la «seca» de la era 1.
    state.fijar_mundo(MUNDO)
    roster = roster_de_habla(roster_nombre)
    difusion = DifusionLexica()
    # (dia, acumulada, ventana, emergente) — la acumulada se conserva por
    # compatibilidad histórica; la señal científica es ventana/emergente
    # (la acumulada converge por mera acumulación del vocabulario base).
    serie_distancia: list[tuple[int, Optional[float], Optional[float], Optional[float]]] = []
    participantes: set[str] = set()   # agentes que REALMENTE hablaron (para la métrica)
    db_fallos: Counter = Counter()    # escrituras a Supabase que fallaron, por tabla

    # Koiné: competencia léxica (fijación por significado). Cada ~4 turnos se
    # introduce un referente novedoso sin nombre → varios agentes acuñan formas
    # rivales → la comunidad fija una por frecuencia × prestigio.
    # La `competencia` se creó arriba: HEREDADA con --continuar (2026-09-18),
    # vacía sin él. Que sobreviva es lo que permite que una disputa siga abierta
    # al día siguiente y pueda llegar al umbral; cada día se sigue evaluando la
    # fijación al cerrarlo, como hasta hoy.
    abiertas = competencia.activas()
    if abiertas:
        detalle = ", ".join(f"{cid} ({len(r['variantes'])} variantes)"
                            for cid, r in abiertas.items())
        print(f"  ◇ competencias heredadas, aún en disputa: {detalle}")
    cadencia_nombramiento = 4
    referentes_pendientes = referentes_pendientes_de(state)

    # Inicializar DB (CurianaDB real o CurianaDBMock si no está configurada)
    db = get_db()
    # El brazo de la escena NO puede cambiar a mitad de cadena (diseño §5.4:
    # «una escena no puede entrar a mitad de cadena: es una serie nueva desde
    # el día 1»). Se comprueba ANTES de crear el run, para no dejar una fila
    # huérfana en la base.
    if continuar:
        comprobar_brazo_de_escena(db, state, escena, capubana_cada)
    # Lo que el run dice de sí mismo, y lo que el estado hereda al día
    # siguiente. `capubana_cada` sólo significa algo con escena.
    state.escena = bool(escena)
    state.capubana_cada = int(capubana_cada) if escena else 0
    _h = huella_de_base(semilla=semilla)
    print(f"  base: {resumen_huella(_h)}")
    if _h.get("motor_sucio"):
        print("  ⚠ árbol sucio: este run NO será citable (ver huella_de_base.py)")

    # El PERFIL manda sobre los flags sueltos: si viene uno, su `andamiaje`
    # decide la ablación, y sus capas deciden qué lengua ven los agentes. El
    # perfil RESUELTO se guarda entero en config —no su nombre— para que este
    # run siga diciendo con qué se corrió aunque el perfil cambie después.
    # Ver 5-experimento/disenos/05_perfiles_de_run.md.
    if perfil is None:
        from curiana_perfiles import cargar_perfil
        perfil = cargar_perfil()
    ablacion = perfil.ablacion
    capas = perfil.capas
    print(f"  perfil: {perfil.nombre} — {len(capas)} capa(s) léxica(s), "
          f"andamiaje {perfil.andamiaje}")

    run_id = db.create_run(
        model=MODEL,
        config={"max_turns": turnos, "mode": "auto",
                "elenco": ELENCO, "mundo": MUNDO,
                "agentes_por_turno": agentes_por_turno,
                "roster": roster_nombre, "roster_n": len(roster),
                "turnos_por_dia": state.turnos_por_dia,
                "dia_inicial": state.dia,
                "continuado_desde": state.run_anterior if continuar else None,
                # La serie separa SETS de runs dentro de una era (Miguel,
                # 2026-09-16: los tres días del 16 quedan como pruebas —serie A,
                # instrumento incompleto— y lo que arranca con la pre-carga es
                # la serie B). Se sella aquí para que los análisis la lean.
                "serie": serie,
                # El brazo de la escena, sellado como se sella el perfil: el
                # run dice de sí mismo con qué corrió. `capubana_cada` es None
                # sin escena, para que la config no sugiera una cadencia que
                # no se aplicó.
                "escena": bool(escena),
                "capubana_cada": int(capubana_cada) if escena else None,
                # Con qué semilla se derivó lo de la ficha (db.3): la del día 1
                # de la cadena. None = koiné de un motor anterior, que usaba
                # la del día.
                "semilla_de_la_persona": semilla_de_la_persona,
                **perfil.como_config(), **_h},
    )
    # Re-crear cliente con run_id para que LangSmith use el proyecto correcto
    client = get_client(run_id)

    estacion_anterior = state.estacion
    anio_simulado = (state.dia - 1) // DIAS_POR_ANIO + 1
    dia_inicio_estacion = state.dia
    tpd = state.turnos_por_dia
    # Lo que cada agente hizo hoy: al cerrar el día pasa a su memoria.
    hizo_hoy: dict[str, dict[str, list[str]]] = {}

    print(f"\n{'='*60}")
    print(f"  CURIANA — Modo Automático: {turnos} turnos")
    print(f"  ({turnos // tpd} días simulados de {tpd} turnos · "
          f"{turnos // (tpd * DIAS_POR_ANIO)} año(s) aprox.)")
    print(f"  elenco: {ELENCO} ({len(ALL_AGENTS)} agentes) · mundo {MUNDO}"
          + (f" · serie {serie}" if serie else ""))
    print(f"  habla: {agentes_por_turno} por turno sobre el roster `{roster_nombre}` ({len(roster)})")
    if escena:
        print(f"  escena: sí (cada uno de los {len(ALL_AGENTS)} en su lugar; "
              f"Capubana cada {capubana_cada} día(s))"
              if capubana_cada > 0 else
              f"  escena: sí (cada uno de los {len(ALL_AGENTS)} en su lugar; "
              f"sin Capubana en esta cadena)")
    else:
        print("  escena: no (brazo de control: el prompt es el de siempre)")
    if continuar:
        print(f"  continúa desde el día {state.dia} (run anterior: {(state.run_anterior or '?')[:8]})")
    print(f"  Run ID: {run_id[:8]}...")
    if ablacion:
        print("  ⚗ ABLACIÓN: sin contagio, sin competencias en prompt, sin muestreo ponderado")
    print(f"{'='*60}\n")

    # #42: el run se cierra SIEMPRE, también si se interrumpe (Ctrl+C, un
    # error de API, un teardown). Antes end_run() iba después del bucle sin
    # finally, y un run cortado quedaba con total_turns=0 y ended_at NULL.
    turnos_hechos = 0
    reflexiones_hechas = 0
    try:
        for t in range(turnos):
            # ¿Toca evento de nombramiento? (cada `cadencia` turnos, si quedan referentes)
            naming_referente = None
            # Era 1: cada `cadencia_nombramiento` turnos, como siempre. Era 2
            # (tanda de la base): el quinto momento de los días impares, uno
            # cada dos días (curiana_koine.toca_nombrar).
            if referentes_pendientes and toca_nombrar(
                    state.mundo, state.dia, state.turno, t, cadencia_nombramiento):
                naming_referente = referentes_pendientes.pop(0)
                state.referentes_introducidos.append(naming_referente["id"])

            interactions = run_turn(
                client, state, memory, lexico, observer,
                verbose=verbose, db=db, run_id=run_id,
                difusion=difusion, idiolectos=idiolectos, campo=campo,
                competencia=competencia, naming_referente=naming_referente,
                ablacion=ablacion, capas=capas, db_fallos=db_fallos,
                agentes_por_turno=agentes_por_turno, roster=roster,
            )
            participantes.update(i["agent"] for i in interactions)
            for i in interactions:
                h = hizo_hoy.setdefault(i["agent"], {"momentos": [], "neos": []})
                h["momentos"].append(i.get("momento") or "")
                h["neos"] += i.get("neologismos") or []
            turnos_hechos += 1

            # Reporte al final de cada día
            if state.turno == 1 and state.dia > 1:  # acaba de cambiar de día
                dia_terminado = state.dia - 1
                # Memoria del día: lo que cada agente hizo, para que mañana
                # (en este run o en uno continuado) se acuerde.
                for nm, h in hizo_hoy.items():
                    nota = f"D{dia_terminado}: hablé al {', '.join(m for m in h['momentos'] if m)}"
                    if h["neos"]:
                        nota += f"; acuñé {', '.join(dict.fromkeys(h['neos']))}"
                    memory.add(nm, nota)
                # Quiénes hablaron hoy: es el elenco que la reflexión le pasa
                # al Director («la gente que hay hoy es: …»). state.agentes_en_escena
                # NO sirve: desde el 2026-09-17 trae los nombres de la era 2 en
                # la era 2, pero es la escena del día 1 y NADIE la actualiza
                # turno a turno; quien habló de verdad es esto.
                gente_de_hoy = sorted(hizo_hoy)
                hizo_hoy = {}
                # Distancia medida SOLO sobre quienes hablaron (población real).
                # Tres lecturas: acumulada (histórica, sesgada a converger por
                # acumulación del vocabulario base), ventana (habla reciente real)
                # y emergente (ventana sin vocabulario base: solo neologismos).
                dist = distancia_idiolectal(idiolectos, solo=participantes)
                dist_vent = distancia_idiolectal(idiolectos, solo=participantes, ventana=True)
                dist_emer = distancia_idiolectal(idiolectos, solo=participantes,
                                                 ventana=True, excluir=_FORMAS_EXCLUIDAS,
                                                 min_formas=3)
                serie_distancia.append((dia_terminado, dist, dist_vent, dist_emer))
                # Evaluar fijación de competencias léxicas del día
                fijadas = competencia.evaluar_fijacion(dia_terminado)
                if db and run_id:
                    try:
                        db.save_koine_metric(run_id, dia_terminado, dist or 0.0,
                                             len(participantes),
                                             distance_ventana=dist_vent,
                                             distance_emergente=dist_emer)
                        for cid, forma in fijadas:
                            d = competencia.diccionario_koine().get(cid, {})
                            db.save_koine_lexicon(run_id, cid, d.get("desc", ""), forma,
                                                  dia_terminado, d.get("soporte"), d.get("n_variantes"))
                    except Exception:
                        db_fallos["koine_metrics"] += 1
                reporte_del_dia = observer.reporte_dia(dia_terminado)
                if verbose:
                    print(reporte_del_dia)
                    fmt = lambda v: "s/d" if v is None else v
                    print(f"  ◇ Koiné — distancia idiolectal ({len(participantes)} agentes): "
                          f"acumulada={fmt(dist)} · ventana={fmt(dist_vent)} · "
                          f"emergente={fmt(dist_emer)}  (↓ = converge)")
                    for cid, forma in fijadas:
                        print(f"  ◆ Koiné fija: '{cid}' → {forma}")
                # La reflexión del Director (--reflexion): una llamada por día,
                # con los cierres del día y el reporte medido. Se imprime
                # siempre que se pide (es un reporte, también con --silencioso),
                # queda en el estado para mañana y en curiana_director.json.
                if reflexion:
                    texto = reflexion_del_dia(client, state, reporte_del_dia,
                                              state.cierres_del_dia, dia=dia_terminado,
                                              gente_en_escena=gente_de_hoy,
                                              model=MODEL)
                    state.notas_orquestador = texto
                    guardar_reflexion(dia_terminado, texto, run_id,
                                      nuevo=(not continuar and reflexiones_hechas == 0))
                    reflexiones_hechas += 1
                    print(f"\n# REFLEXIÓN DEL DIRECTOR — Día {dia_terminado}\n{texto}\n")
                state.cierres_del_dia = []

            # Detección de cambio de estación
            if state.estacion != estacion_anterior:
                if verbose:
                    print(observer.reporte_estacion(estacion_anterior))
                estacion_anterior = state.estacion
                dia_inicio_estacion = state.dia

                # Cada vez que completa un año (2 estaciones), reporte anual.
                # El año se cierra al VOLVER a la seca (días 121, 241, 361…), no
                # con `dia % 120 == 0`: el cambio de estación nunca cae en un
                # múltiplo exacto de 120, así que esa condición no se cumplía jamás
                # y --reporte no producía nada.
                anio_en_curso = (state.dia - 1) // DIAS_POR_ANIO + 1
                if reporte_anual and anio_en_curso > anio_simulado:
                    print(observer.reporte_anual_llm(anio_simulado))
                    anio_simulado = anio_en_curso
    finally:
        # Guardar localmente: es lo que un run continuado (--continuar) hereda.
        state.run_anterior = run_id
        state.save()
        memory.save()
        lexico.save()
        observer.save()
        observer.exportar_csv()
        observer.exportar_neologismos_csv()
        guardar_koine(idiolectos, campo, competencia)

        # Cerrar run en DB, con lo que de verdad se corrió
        db.end_run(run_id, total_turns=turnos_hechos, total_days=state.dia - 1)
        if turnos_hechos < turnos:
            print(f"  ⚠ run interrumpido: {turnos_hechos} de {turnos} turnos "
                  f"({state.dia - 1} días). Cerrado igual en la base.")

    # Reporte final
    print(f"\n{'═'*60}")
    print(f"  SIMULACIÓN COMPLETADA: {turnos} turnos = {state.dia - 1} días")
    print(f"{'═'*60}")
    print(lexico.reporte_linguistico())
    # Lo que la puerta paró: acuñaciones que eran el propio prompt. Se DICE,
    # no se silencia — un rechazo callado es un dato perdido, y la cifra es
    # la que avisa de que la plantilla se está copiando (corte de serie del
    # 2026-09-18). Sin rechazos la línea no sale y el cierre es el de siempre.
    rechazos = lexico.reporte_de_rechazos()
    if rechazos:
        print()
        print(rechazos)
    print()
    print("  Ranking lingüístico final:")
    for agente, score in observer.ranking_linguistico()[:8]:
        bar = "█" * int(score) + "░" * (10 - int(score))
        print(f"    {agente:15} {bar} {score:.1f}/10")

    # ── Resumen koiné: ¿convergió la lengua? ──
    print(f"\n{'─'*60}")
    print("  KOINÉ — convergencia (distancia idiolectal media por día)")
    if ablacion:
        print("  ⚗ RUN DE ABLACIÓN (control sin inyecciones de convergencia)")
    print(f"{'─'*60}")
    if serie_distancia:
        for linea in lineas_de_serie(serie_distancia):
            print(f"  {linea}")
        # Veredicto sobre la métrica MÁS EXIGENTE con datos suficientes:
        # emergente > ventana > acumulada (la acumulada converge casi siempre
        # por acumulación del vocabulario base — no es evidencia por sí sola).
        # No basta con fin < inicio: una curva que baja al principio y se
        # estanca (típico de la ablación) daría un falso "converge". El
        # veredicto mira también la pendiente del último tercio (ver
        # veredicto_convergencia en curiana_koine.py).
        # El criterio vive en curiana_cadena.veredicto() para que el run y su
        # cadena no puedan juzgarse con varas distintas.
        print(f"  {texto_veredicto(serie_distancia)}")
    _imprimir_cadena(db, run_id)
    print("\n  Diccionario koiné emergente (formas más extendidas):")
    for forma, peso in campo.top(15, excluir=_FORMAS_EXCLUIDAS):
        print(f"    {forma:18} {peso:.1f}")

    # ── Fijación por competencia: el diccionario koiné de conceptos nuevos ──
    print(competencia.reporte())

    # ── Integridad de datos: escrituras a Supabase que fallaron ──
    if db_fallos:
        total_fallos = sum(db_fallos.values())
        print(f"\n  ⚠ PERSISTENCIA INCOMPLETA: {total_fallos} escritura(s) a DB fallaron")
        for tabla, n in db_fallos.most_common():
            print(f"      {tabla}: {n}")
        print("    Los análisis sobre Supabase de este run pueden estar incompletos.")

    if reporte_anual:
        print(observer.reporte_anual_llm(anio_simulado))

    if perfiles and hasattr(db, "client"):
        print(f"\n{'─'*60}")
        print("  Generando perfiles curados por agente (Observer)...")
        n = observer.generar_perfiles_curados(db, run_id)
        print(f"  ✓ {n} perfil(es) curado(s) generado(s).")
        print(f"{'─'*60}")


# ══════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Curiana v2 — Motor de emergencia lingüística caquetía"
    )
    parser.add_argument(
        "--auto", type=int, default=0,
        help="Turnos automáticos (0 = interactivo). 240 = 1 año simulado."
    )
    parser.add_argument(
        "--anio", action="store_true",
        help="Atajos: --auto 240 (1 año). Equivale a --auto 240."
    )
    parser.add_argument(
        "--reporte", action="store_true",
        help="Generar reporte anual LLM al completar cada año simulado."
    )
    parser.add_argument(
        "--silencioso", action="store_true",
        help="Solo mostrar reportes, no cada interacción individual."
    )
    parser.add_argument(
        "--perfiles", action="store_true",
        help="Al terminar, generar perfiles curados por agente (rol, arco, "
             "frases célebres) vía el Observer y guardarlos en Supabase."
    )
    parser.add_argument(
        "--perfil", type=str, default=None,
        help="Perfil de run declarado en 5-experimento/perfiles_de_run.yaml "
             "(base, atestiguado, suelto, control, suelto-control). Define qué "
             "capas del lexicón ven los agentes y si hay andamiaje de "
             "convergencia. Se guarda resuelto en simulation_runs.config. "
             "Sin él se usa `base`, que es como se corrió la era 1."
    )
    parser.add_argument(
        "--listar-perfiles", action="store_true",
        help="Lista los perfiles disponibles y sale."
    )
    parser.add_argument(
        "--agentes-por-turno", type=int, default=6,
        help="Cuántos agentes hablan por turno (la era 1: 6).",
    )
    parser.add_argument(
        "--roster", choices=["koine", "nucleo", "todos"], default="koine",
        help="Sobre qué elenco rota la ventana: `koine` (los 23 fijos de la era 1), "
             "`nucleo` (los 24 en_roster del casting de la era 2) "
             "o `todos` (todos los agentes no foráneos, tier 3 incluidos).",
    )
    parser.add_argument(
        "--elenco", choices=["era1", "era2"], default=None,
        help="Qué elenco carga el motor: `era1` (curiana_agents.py, 60) o `era2` "
             "(curiana_agents_era2.py, generado desde 6-fusion/elenco_era2.yaml). "
             "Se aplica antes de importar (fija CURIANA_ELENCO).",
    )
    parser.add_argument(
        "--turnos-por-dia", type=int, default=None,
        help="Turnos por día simulado (la era 1: 2; con 6 se recorren los seis "
             "momentos del día). Un run continuado hereda el del anterior.",
    )
    parser.add_argument(
        "--semilla", type=int, default=None,
        help="Semilla del azar del motor; se sella en la huella del run.",
    )
    parser.add_argument(
        "--continuar", action="store_true",
        help="Encadena días: arranca del estado, la memoria, el lexicón y la koiné "
             "que dejó en disco el run anterior.",
    )
    parser.add_argument(
        "--reflexion", action="store_true",
        help="Al cerrar cada día, una llamada más: el Director, con el mundo, lee los "
             "cierres del día y el reporte medido y escribe 4-6 oraciones (qué cambió, "
             "qué palabra prendió, qué queda abierto). Va al log, al estado y a "
             "curiana_director.json. Apagado por defecto: cuesta API.",
    )
    parser.add_argument(
        "--serie", default=None,
        help="Etiqueta del set de runs dentro de la era (p. ej. era2-b); se sella en "
             "la config del run. Separa las pruebas de lo que cuenta.",
    )
    parser.add_argument(
        "--escena", action="store_true",
        help="La escena por lugar (era 2): cada turno, cada uno de los 63 está en "
             "un lugar —su oficio y la hora lo deciden— y el prompt cambia "
             "[Tu ubicación] por [Aquí estás] (dónde estás, qué momento y quién "
             "está contigo, ≤ 200 car.). El Director recibe las intervenciones "
             "agrupadas por lugar, sin llamadas de más. Apagado por defecto: sin "
             "él, el prompt es byte a byte el de hoy. Se sella en la config y una "
             "cadena --continuar no puede cambiar de brazo a la mitad.",
    )
    parser.add_argument(
        "--capubana-cada", type=int, default=CAPUBANA_CADA_POR_DEFECTO,
        help="Cada cuántos días convergen los dos nodos en el cerro: ese día todos "
             f"están en el Capubana los seis momentos (por defecto "
             f"{CAPUBANA_CADA_POR_DEFECTO}; 0 = sin convergencia). El calendario "
             "del canon pone el ciclo mayor en los días 55-58 de la seca, "
             "inalcanzable en una cadena de ocho: la cadencia es un parámetro "
             "declarado y sellado, como el perfil. Sólo cuenta con --escena.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Imprime la CONFIG RESUELTA del run que se correría —perfil, serie, "
             "escena, capubana_cada, semilla, continuado_desde— y sale sin "
             "llamar a nada: ni a la API, ni a la base, ni a git. Es para leer "
             "el brazo antes de gastar un día de API.",
    )
    parser.add_argument(
        "--ablacion", action="store_true",
        help="Run de CONTROL: apaga las inyecciones de prompt que empujan la "
             "convergencia (sugerencias de contagio, competencias abiertas, "
             "muestreo ponderado por frecuencia). Comparar contra un run normal "
             "separa la convergencia emergente de la inducida por el andamiaje."
    )
    args = parser.parse_args()

    from curiana_perfiles import cargar_perfil, nombres as _nombres_perfil
    if args.listar_perfiles:
        import curiana_perfiles
        curiana_perfiles.main()
        sys.exit(0)
    # --ablacion sigue funcionando solo: es el atajo al perfil `control`.
    if args.perfil:
        perfil = cargar_perfil(args.perfil)
    elif args.ablacion:
        perfil = cargar_perfil("control")
    else:
        perfil = cargar_perfil()

    extra = dict(agentes_por_turno=args.agentes_por_turno, roster_nombre=args.roster,
                 turnos_por_dia=args.turnos_por_dia, semilla=args.semilla,
                 continuar=args.continuar, reflexion=args.reflexion, serie=args.serie,
                 escena=args.escena, capubana_cada=args.capubana_cada)

    # --dry-run va ANTES de get_client(): crear el cliente ya exige la clave y
    # la gracia de esta bandera es poder leer el brazo sin tocar nada.
    if args.dry_run:
        _turnos = (120 * (args.turnos_por_dia or 2)) if args.anio else args.auto
        imprimir_dry_run(config_resuelta(_turnos, perfil, ablacion=args.ablacion,
                                         **extra))
        sys.exit(0)

    client = get_client()

    if args.anio:
        tpd = args.turnos_por_dia or 2
        auto_mode(client, 120 * tpd, reporte_anual=True, verbose=not args.silencioso,
                   perfiles=args.perfiles, ablacion=args.ablacion,
                   perfil=perfil, **extra)
    elif args.auto > 0:
        auto_mode(
            client, args.auto,
            reporte_anual=args.reporte,
            verbose=not args.silencioso,
            perfiles=args.perfiles,
            ablacion=args.ablacion,
            perfil=perfil,
            **extra,
        )
    else:
        interactive_mode(client)
