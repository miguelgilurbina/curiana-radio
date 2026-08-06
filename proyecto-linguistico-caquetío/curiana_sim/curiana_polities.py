#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CURIANA — las polities caquetías, como dato
===========================================

Oliver dedica su capítulo 3 a demostrar una cosa que el proyecto venía tratando
como si no importara: **los caquetíos no eran una sola cultura**. Hablaban la
misma lengua —eso lo sostiene él con fuerza— pero sus formaciones políticas
diferían en seis ejes que él enumera: patrón de asentamiento, densidad,
estratificación social, autoridad y liderazgo, presión sobre la tierra y actitud
ante la guerra. Y remata rechazando el "Cacicazgo Teocrático" de Steward y Faron
precisamente porque *"blurs the differences that make a difference"*.

La simulación modela **una** de esas formaciones: la costera (Coro,
Todariquiba, el Golfete). Este módulo pone las cuatro por escrito, con su fuente
por rasgo, para que:

1. La costera deje de ser *"lo caquetío"* a secas y pase a ser una opción
   explícita entre varias — que es lo que era.
2. Se pueda **detectar cuándo el canon importa un rasgo de otra polity** sin
   marcarlo (ver `coherencia_del_canon()`).

   ⚠️ Y para no equivocarse al hacerlo. La primera versión de este módulo daba
   por confirmado que Shaboro, piache aparte de Manaure, era un préstamo de
   Barquisimeto. **Era falso**: la costa también tenía boratio "en cada pueblo
   principal" (Oviedo y Valdés t. II p.298, en Arcaya 1920 pp. 97-100). El eje
   que separa a las dos polities no es que exista el oficio, sino que en la
   costa **el jefe es además gran chamán** — y el canon ya lo cumple, porque
   Manaure es "gobernante Y piache en uno". El chequeo mira eso.
3. Cuando se decida dar vida a las otras, el dato ya esté reunido y citado en
   vez de inventarse en el momento.

QUÉ ES Y QUÉ NO ES UNA POLITY AQUÍ
----------------------------------
`polity` NO es lo mismo que `etnia`, y conviene no confundirlos porque el motor
ya usa el segundo:

- **`etnia`** (en `curiana_agents.py`) responde *¿de qué pueblo es esta
  persona?* — caquetío, guaycarí, jirajara, caribe. Alimenta la variación
  dialectal de `curiana_social.py` y la disposición de `curiana_koine.py`.
- **`polity`** (aquí) responde *¿en qué formación política caquetía vive?* —
  costera, Barquisimeto, Yaracuy, Llanos. Los 60 agentes actuales son todos de
  la costera, sean de la etnia que sean.

Son ejes ortogonales: un guaycarí de la costa y un caquetío de Barquisimeto se
diferencian en cosas distintas.

DISCIPLINA DE FUENTES
---------------------
**Cada rasgo lleva su cita.** Un rasgo sin fuente es un bug, y `validar()` lo
reporta. Donde una fuente dice algo solo de una polity, se registra solo para
esa: la tentación de completar la tabla por simetría es exactamente el error que
Oliver denuncia. Los huecos se dejan como `None` y se ven.

⚠️ **Casi todo esto es dato de crónica colonial (s. XVI)**, sobre todo de
Federmann (1530) y del documento de 1579. La simulación transcurre en los siglos
XIV-XV. Vale la regla de siempre del proyecto: no proyectar sin decidirlo. El
campo `epoca` de cada rasgo dice de cuándo es el dato.

Uso:
    python curiana_polities.py                 # informe comparativo
    python curiana_polities.py --contrastar costera barquisimeto
    python curiana_polities.py --canon         # coherencia del canon actual
    python curiana_polities.py --check         # exit 1 si hay rasgos sin fuente
"""

import argparse
import io
import sys
from dataclasses import dataclass
from typing import Optional

# La formación que la simulación modela hoy. Todo lo que vive en
# `curiana_agents.py` y `curiana_state.py` pertenece a esta.
POLITY_SIMULADA = "costera"


@dataclass(frozen=True)
class Rasgo:
    """Un rasgo de una polity, con la fuente que lo sostiene.

    `epoca` importa tanto como `valor`: casi todo el corpus etnohistórico es del
    s. XVI y la simulación es de los siglos XIV-XV.
    """
    valor: str
    fuente: str
    epoca: str = "s. XVI (crónica colonial)"

    def __str__(self) -> str:
        return self.valor


@dataclass(frozen=True)
class Polity:
    id: str
    nombre: str
    territorio: Rasgo
    liderazgo: Optional[Rasgo] = None
    asentamiento: Optional[Rasgo] = None
    demografia: Optional[Rasgo] = None
    economia: Optional[Rasgo] = None
    guerra: Optional[Rasgo] = None
    religion: Optional[Rasgo] = None
    ceramica: Optional[Rasgo] = None
    notas: str = ""

    # Los seis ejes en los que Oliver dice que las polities difieren, más dos
    # que el proyecto necesita (religión y cerámica).
    EJES = ("territorio", "liderazgo", "asentamiento", "demografia",
            "economia", "guerra", "religion", "ceramica")

    def rasgos(self) -> dict:
        """Los ejes con dato, en orden. Los huecos NO se rellenan."""
        return {eje: getattr(self, eje) for eje in self.EJES
                if getattr(self, eje) is not None}

    def huecos(self) -> list:
        return [eje for eje in self.EJES if getattr(self, eje) is None]


# ══════════════════════════════════════════════════════════════════════
# LAS CUATRO POLITIES
# ══════════════════════════════════════════════════════════════════════

_OLIVER = "Oliver 1989, cap. 3"
_JAHN = "Jahn 1927, pp. 200-202 (siguiendo a Arcaya 1920)"
_ANTCZAK = "Antczak, Urbani & Antczak 2017, J World Prehist 30, p. 157"
_OVIEDO_B = "Oviedo y Baños [1723], cap. III (ed. Biblioteca Ayacucho, pp. 26-28)"

POLITIES = {

    "costera": Polity(
        id="costera",
        nombre="Caquetío costero (Coro, Paraguaná, el Golfete y las islas)",
        territorio=Rasgo(
            "La franja llana y estéril próxima al mar, desde el Lago frente a "
            "Maracaibo hasta poco al este de la boca del Yaracuy, incluida "
            "Paraguaná; y de Paraguaná a Curazao, Aruba y Bonaire.",
            _JAHN + "; " + _ANTCZAK + " (ruta dabajuroide a las islas, ~900 d.C.)",
            epoca="s. XVI documental (Jahn/Arcaya) + ~900 d.C. arqueológico "
                  "(Antczak) para el salto insular"),
        liderazgo=Rasgo(
            "Jerárquico, en un único jefe paramount (el diao) que es **además "
            "gran chamán**: poder secular y sagrado fundidos en una persona. "
            "Manaure media entre lo natural y lo sobrenatural, y su reputación "
            "descansa en poder predecir y controlar fenómenos naturales.",
            _OLIVER + ", pp. 251 y ss., 279"),
        asentamiento=Rasgo(
            "Aldeas dispersas por las llanuras costeras.",
            _OLIVER + ", p. 279"),
        demografia=Rasgo(
            "Aldeas de tamaño medio, ~200 a 500 personas.",
            _OLIVER + ", p. 279"),
        economia=Rasgo(
            "Red de alianzas sostenida en comercio: cuentas de concha, sal y "
            "azabache. Salinas abundantes; tierra arenosa y falta de aguas, "
            "comarca por lo demás 'abundante y regalada' — la tesis de tierra "
            "pobre y mar rico.",
            _OLIVER + " (confederación por comercio); " + _OVIEDO_B + " (Coro: "
            "'su terreno arenoso y falto de aguas', 'abundantes salinas')"),
        guerra=Rasgo(
            "Disputa documentada con los grupos de descendencia caribe "
            "(valencioides) por el acceso y control de los archipiélagos de Las "
            "Aves y Los Roques, entre 1200 d.C. y el Contacto. La presencia "
            "dabajuroide en el norte de Falcón contuvo el asentamiento "
            "valencioide en la costa occidental.",
            _ANTCZAK,
            epoca="1200 d.C. - Contacto (arqueológico) — **dentro de la ventana "
                  "de la simulación**"),
        religion=Rasgo(
            "**Dos niveles, no uno.** (a) El jefe paramount ejerce además de "
            "gran chamán — es el rasgo que la distingue de Barquisimeto. "
            "(b) Y por debajo, **'en cada pueblo principal hay un boratio'**, "
            "sacerdote y médico a la vez: se encierra solo en un buhío con "
            "tabaco 'que le saca el sentido' uno, dos, tres días o más, y sale "
            "con la respuesta sobre la lluvia, el año seco o abundante, y si "
            "deben ir a la guerra; se le paga con joyas de oro. Para las "
            "preguntas pequeñas —si habrá caza, si la mujer lo quiere bien— "
            "**'cada uno es boratio'**: adivinación doméstica con tabaco "
            "enrollado en una mazorca, leyendo la ceniza (curva como hoz = "
            "bien; recta = al revés).",
            _OLIVER + ", p. 279 (el jefe como gran chamán); Oviedo y Valdés, "
            "*Historia General y Natural de las Indias*, t. II p. 298, citado "
            "extensamente en Arcaya 1920, pp. 97-100"),
        ceramica=Rasgo(
            "Su distribución en tiempo y espacio es 'precisely congruent' con "
            "la sub-tradición **Dabajurana**. ⚠️ El propio Oliver matizó esto "
            "en 2016: no todos los rasgos de los sitios de la costa de Falcón "
            "son dabajuroides.",
            _OLIVER + "; matiz en " + _ANTCZAK + " (José Oliver 2016, pers. comm.)",
            epoca="arqueológico, larga duración"),
        notas="Es la polity que la simulación modela. Todo `curiana_agents.py` "
              "y `curiana_state.py` pertenece aquí.",
    ),

    "barquisimeto": Polity(
        id="barquisimeto",
        nombre="Caquetío de Barquisimeto (valle del Turbio y sabanas de Lara)",
        territorio=Rasgo(
            "El valle del Turbio y las sabanas de Barquisimeto, bajando al sur "
            "por Sarare y Acarigua hacia Cojedes.",
            _JAHN),
        liderazgo=Rasgo(
            "**Doble jefatura, y sin jefe paramount**: un Jefe de Paz y un Jefe "
            "de Guerra, que Oliver sospecha personas distintas porque los "
            "atributos se contradicen. El de Guerra acumula rango por hazañas "
            "militares y lo exhibe en adornos corporales; el de Paz debe "
            "redistribuir y pierde autoridad si acumula. Cada oficio solo opera "
            "en su contexto: en paz los aldeanos declaran que 'no tienen señor "
            "que los gobierne'; en guerra la autoridad se centraliza.",
            _OLIVER + ", pp. 276-279 (Federmann 1530 y documento de 1579)"),
        asentamiento=Rasgo(
            "23 aldeas fuertemente agrupadas y **fortificadas** ('fortificadas', "
            "quizá empalizadas). Viviendas de hasta ocho familias — tipo maloca.",
            _OLIVER + ", pp. 277-279 (Federmann [1557] 1958: 66-67)"),
        demografia=Rasgo(
            "~4.000 personas por aldea. Densidad muy superior a la costera.",
            _OLIVER + ", p. 277"),
        economia=Rasgo(
            "Comerciaban **sal con sus propios enemigos**, estando rodeados de "
            "ellos. El oro venía de las serranías de Nirgüa-Buria; la sal, "
            "probablemente por el valle del Yaracuy. El maçato (cerveza de "
            "maíz) es el instrumento político del Jefe de Paz, que redistribuye "
            "maíz, yuca y legumbres a cambio de trabajo en los campos.",
            _OLIVER + ", pp. 276-278"),
        guerra=Rasgo(
            "Ciclo de paz y guerra con **motor agrícola**: valles de tamaño "
            "limitado más crecimiento demográfico llevan a expandirse sobre "
            "territorio ya poblado. La jefatura de paz depende del excedente "
            "agrícola, que la presión erosiona. Solo la victoria o la derrota "
            "completa rompe el ciclo. Guerra 'constreñida', a diferencia de la "
            "kalina, que sí hace del raid de prisioneros el motor del prestigio.",
            _OLIVER + ", p. 278"),
        religion=Rasgo(
            "El **boratio vive apartado**, en su propia casita de paja fuera de "
            "la aldea principal, y el Jefe de Paz **no** es a la vez gran "
            "chamán: poder político y poder sagrado están separados. "
            "⚠️ Sacrificio humano por sequía documentado en 1579: compran a la "
            "madre una muchacha de diez años arriba y la degüellan en la ribera "
            "para darla 'al sol por mujer', porque el sol está enojado y por eso "
            "no llueve. Tras la llegada española lo siguen haciendo a escondidas.",
            _OLIVER + ", pp. 276-279 (documento de 1579, Arellano Moreno "
            "1964: 189-190)",
            epoca="1579 — **colonial y tardío**; no proyectar al precontacto"),
        ceramica=Rasgo(
            "Oliver la hace corresponder con la sub-tradición **Tierran**, en "
            "paralelo a costera↔Dabajurana.",
            _OLIVER,
            epoca="arqueológico, larga duración"),
        notas="El contraste más fuerte con la costera, y la fuente de varios "
              "rasgos que el canon del proyecto usa sin marcar su origen.",
    ),

    "yaracuy": Polity(
        id="yaracuy",
        nombre="Caquetío del Yaracuy (el valle que llamaban Vararida)",
        territorio=Rasgo(
            "El valle del río Yaracuy, **que ellos llamaban Vararida** y que "
            "Federmann bautizó 'de Las Damas'; hoy el corazón del Estado "
            "Yaracuy.",
            _JAHN),
        liderazgo=Rasgo(
            "**Confederación elástica**: no forman una unidad, sino grupos de "
            "dos, tres o cuatro aldeas aliadas entre sí — por eso Federmann los "
            "juzga menos poderosos que Barquisimeto. Pero anota que **se unirían "
            "si fueran atacados** con fuerza suficiente.",
            _OLIVER + ", p. 278 (Federmann [1557] 1958: 108)"),
        asentamiento=Rasgo(
            "Densidad variable: unos son racimos de tres aldeas, otros "
            "viviendas sueltas, y algunos se estiran linealmente hasta milla y "
            "media con una o dos calles a lo sumo. Viviendas de cinco a ocho "
            "familias.",
            _OLIVER + ", p. 278 (Federmann)"),
        demografia=Rasgo(
            "Tan poblado como Barquisimeto en número total, pero repartido de "
            "otro modo.",
            _OLIVER + ", p. 278"),
        economia=Rasgo(
            "El límite Barquisimeto/Yaracuy es **el paso entre los Llanos y la "
            "costa caribeña**: controlarlo era controlar el comercio y las "
            "comunicaciones. Es una de las causas de la competencia entre ambas.",
            _OLIVER + ", p. 278"),
        guerra=Rasgo(
            "En competencia dura con Barquisimeto por tierra, espacio y "
            "(probablemente) acceso al mar Caribe.",
            _OLIVER + ", p. 278"),
        # religion y ceramica quedan vacías a propósito: la fuente no dice.
        notas="Oliver advierte que 'no es en absoluto una sola unidad política'. "
              "Es la polity peor documentada de las cuatro.",
    ),

    "llanos": Polity(
        id="llanos",
        nombre="Caquetío de los Llanos del norte (Cojedes, Portuguesa, Apure)",
        territorio=Rasgo(
            "Del alto Cojedes-Portuguesa hacia el sur; todo el alto llano por "
            "Portuguesa y Zamora (sabanas de Pedraza y Santa Bárbara), alto "
            "Apure, hasta Casanare, y algunos grupos hacia el Orinoco en el "
            "estrecho de Barraguán.",
            _JAHN),
        liderazgo=Rasgo(
            "Liderazgo militar y secular en la misma persona (como en la "
            "costa), pero **menos centralizado**: con los guaycaríes aliados la "
            "jefatura militar es cosa de colaboración, no de mando. "
            "**Ninguno de los jefes aparece con poderes chamánicos** — el eje "
            "sagrado no se registra.",
            _OLIVER + " (comportamiento de los diao de Curahamara e Itabana)"),
        economia=Rasgo(
            "En el bajo Cojedes, **comercio de esclavos capturados** entre "
            "grupos: Federmann pidió comprar una naboria en la aldea de Itabana "
            "y se la negaron, 'aunque acostumbraban a comprarlas y venderlas "
            "entre sí'.",
            _OLIVER + ", n. 126, p. 277 (Federmann [1557] 1958: 94)"),
        guerra=Rasgo(
            "**Guerra de captura de esclavos institucionalizada** — pero Oliver "
            "subraya que esto vale **solo** para el bajo Cojedes y que no hay "
            "afirmación equivalente para los caquetíos de otras áreas. La razzia "
            "esclavista era común y extendida en los Llanos en general.",
            _OLIVER + ", n. 126, p. 277"),
        religion=Rasgo(
            "Ausencia notable: ninguno de los jefes es caracterizado como chamán.",
            _OLIVER),
        notas="Es la polity que más se aleja del modelo costero, y la única con "
              "esclavitud documentada. Oliver acota el dato con cuidado; "
              "conviene no generalizarlo.",
    ),
}


# ══════════════════════════════════════════════════════════════════════
# CONSULTA
# ══════════════════════════════════════════════════════════════════════

def polity(pid: str) -> Polity:
    if pid not in POLITIES:
        raise KeyError(f"polity desconocida: {pid!r} "
                       f"(conocidas: {', '.join(sorted(POLITIES))})")
    return POLITIES[pid]


def la_simulada() -> Polity:
    """La polity que el motor modela hoy."""
    return polity(POLITY_SIMULADA)


def contrastar(a: str, b: str) -> dict:
    """Ejes en que dos polities difieren, con el dato de cada una.

    Devuelve `{eje: (rasgo_a, rasgo_b)}`. Un eje donde una de las dos no tiene
    dato **sale igual**, con `None` en su lado: el hueco es información.
    """
    pa, pb = polity(a), polity(b)
    salida = {}
    for eje in Polity.EJES:
        ra, rb = getattr(pa, eje), getattr(pb, eje)
        if ra is None and rb is None:
            continue
        if ra is None or rb is None or ra.valor != rb.valor:
            salida[eje] = (ra, rb)
    return salida


def prompt_polity(pid: str) -> str:
    """Fragmento de prompt que sitúa a un agente en su formación política.

    Pensado para concatenarse en `curiana_orchestrator_v2.py::build_system()`,
    al lado de `prompt_rasgos_dialectales()`. Hoy no se inyecta: la simulación
    corre entera en una sola polity, así que añadirlo no cambiaría nada. Existe
    para cuando haya más de una.
    """
    p = polity(pid)
    partes = [f"Vives entre los {p.nombre}."]
    if p.liderazgo:
        partes.append(f"Autoridad: {p.liderazgo.valor}")
    if p.asentamiento:
        partes.append(f"Tu gente vive así: {p.asentamiento.valor}")
    if p.economia:
        partes.append(f"De qué vive: {p.economia.valor}")
    return "[" + " ".join(partes) + "]"


# ══════════════════════════════════════════════════════════════════════
# VALIDACIÓN
# ══════════════════════════════════════════════════════════════════════

def validar() -> list:
    """Todo rasgo lleva fuente; la polity simulada existe. Devuelve problemas."""
    problemas = []
    if POLITY_SIMULADA not in POLITIES:
        problemas.append(f"POLITY_SIMULADA={POLITY_SIMULADA!r} no existe")

    for pid, p in POLITIES.items():
        if pid != p.id:
            problemas.append(f"{pid}: la clave no coincide con .id={p.id!r}")
        if p.territorio is None:
            problemas.append(f"{pid}: sin territorio (es el único eje obligatorio)")
        for eje, rasgo in p.rasgos().items():
            if not rasgo.fuente or not rasgo.fuente.strip():
                problemas.append(f"{pid}.{eje}: rasgo sin fuente")
            if not rasgo.valor or not rasgo.valor.strip():
                problemas.append(f"{pid}.{eje}: rasgo sin valor")
    return problemas


def coherencia_del_canon() -> list:
    """¿El canon del motor coincide con la polity que dice modelar?

    Comprueba lo que se puede comprobar leyendo `curiana_agents.py`. No es
    exhaustivo —la mayoría de los rasgos son narrativos y no viven en el
    código— pero atrapa el caso que motivó este módulo.
    """
    avisos = []
    try:
        from curiana_agents import ALL_AGENTS
    except Exception as e:                                       # noqa: BLE001
        return [f"no se pudo leer curiana_agents.py: {e}"]

    # Lo que separa a la costera de Barquisimeto NO es que existan boratios
    # —los hay en las dos, "en cada pueblo principal hay un boratio"— sino si
    # el JEFE es además gran chamán. En la costa sí; en Barquisimeto el jefe de
    # paz no lo es (Oliver p.279). Así que la comprobación mira al cacique, no
    # a si los oficios están repartidos entre personas distintas.
    if POLITY_SIMULADA == "costera":
        caciques = [n for n, a in ALL_AGENTS.items()
                    if a.get("ubicacion_default") == "casa_cacique"]
        marcas = ("piache", "chamán", "chaman", "teocrátic", "teocratic",
                  "boratio", "tormenta")

        def _es_tambien_chaman(a: dict) -> bool:
            texto = " ".join(str(a.get(c, "")) for c in
                             ("descripcion", "system_prompt")).lower()
            return any(m in texto for m in marcas)

        sin_don = [n for n in caciques if not _es_tambien_chaman(ALL_AGENTS[n])]
        if caciques and len(sin_don) == len(caciques):
            avisos.append(
                f"ningún cacique del elenco ({', '.join(caciques)}) aparece "
                "como gran chamán, y eso es lo que distingue a la polity "
                "'costera' de la de barquisimeto (Oliver 1989 cap.3 p.279): "
                "en la costa el diao gobierna el cuerpo y el cielo. Revisar "
                "el canon o cambiar POLITY_SIMULADA.")

    # Las etnias son un eje distinto del de polity, pero conviene ver que el
    # campo esté sano: 'caquetío' y 'caquetía' son el mismo pueblo escrito en
    # dos géneros, y cualquier agrupación por etnia los separa.
    etnias = {a.get("etnia") for a in ALL_AGENTS.values() if a.get("etnia")}
    if {"caquetío", "caquetía"} <= etnias:
        avisos.append(
            "el campo `etnia` usa 'caquetío' y 'caquetía' como valores "
            "distintos (concuerdan con el género de la persona, no con el "
            "pueblo). Hoy no rompe nada porque las tablas que lo consumen "
            "duplican la entrada, pero cualquier agrupación nueva por etnia "
            "contará dos pueblos donde hay uno.")

    sin_etnia = [n for n, a in ALL_AGENTS.items() if not a.get("etnia")]
    if sin_etnia:
        avisos.append(
            f"{len(sin_etnia)} agentes sin campo `etnia`; caen al defecto "
            f"'caquetío' en el orquestador: {', '.join(sorted(sin_etnia)[:6])}"
            + (" …" if len(sin_etnia) > 6 else ""))

    return avisos


# ══════════════════════════════════════════════════════════════════════
# INFORME
# ══════════════════════════════════════════════════════════════════════

def _forzar_utf8() -> None:
    for nombre in ("stdout", "stderr"):
        flujo = getattr(sys, nombre)
        if hasattr(flujo, "buffer") and (flujo.encoding or "").lower() != "utf-8":
            setattr(sys, nombre, io.TextIOWrapper(
                flujo.buffer, encoding="utf-8", errors="replace", line_buffering=True))


def _envolver(texto: str, ancho: int = 66, sangria: str = " " * 6) -> str:
    import textwrap
    return textwrap.fill(texto, ancho, initial_indent=sangria,
                         subsequent_indent=sangria)


def informe() -> None:
    print("\n── Las polities caquetías ──")
    for pid, p in POLITIES.items():
        marca = "  ◄ LA QUE SIMULAMOS" if pid == POLITY_SIMULADA else ""
        print(f"\n  [{pid}] {p.nombre}{marca}")
        print(f"      ejes con dato: {len(p.rasgos())}/{len(Polity.EJES)}"
              + (f"   huecos: {', '.join(p.huecos())}" if p.huecos() else ""))

    print("\n\n── Contraste: la costera frente a las otras tres ──")
    print("  (un eje solo cuenta como distinto si AMBAS tienen dato; si a una "
          "le falta,\n   la diferencia es de documentación, no de las polities)")
    for otra in ("barquisimeto", "yaracuy", "llanos"):
        dif = contrastar(POLITY_SIMULADA, otra)
        ambas = [e for e, (a, b) in dif.items() if a is not None and b is not None]
        solo_una = [e for e in dif if e not in ambas]
        print(f"\n  costera ↔ {otra}")
        print(f"      distintas en {len(ambas)} ejes: {', '.join(ambas)}")
        if solo_una:
            print(f"      sin comparar (falta dato en una): {', '.join(solo_una)}")


def informe_canon() -> None:
    print("\n── Coherencia del canon con la polity simulada "
          f"('{POLITY_SIMULADA}') ──")
    avisos = coherencia_del_canon()
    if not avisos:
        print("  ✓ sin discrepancias detectables desde el código")
        return
    for a in avisos:
        print("\n  ⚠ " + _envolver(a).lstrip())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Las polities caquetías, como dato")
    ap.add_argument("--contrastar", nargs=2, metavar=("A", "B"),
                    help="muestra los ejes en que A y B difieren")
    ap.add_argument("--canon", action="store_true",
                    help="comprueba el canon del motor contra la polity simulada")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 si algún rasgo no tiene fuente")
    args = ap.parse_args(argv)

    problemas = validar()

    if args.contrastar:
        a, b = args.contrastar
        dif = contrastar(a, b)
        print(f"\n── {a} ↔ {b} — {len(dif)} ejes distintos ──")
        for eje, (ra, rb) in dif.items():
            print(f"\n  ▸ {eje.upper()}")
            for etiqueta, r in ((a, ra), (b, rb)):
                if r is None:
                    print(f"    {etiqueta}: (la fuente no dice)")
                else:
                    print(f"    {etiqueta}:")
                    print(_envolver(r.valor))
                    print(f"{' ' * 6}— {r.fuente}  [{r.epoca}]")
    elif args.canon:
        informe_canon()
    else:
        informe()
        informe_canon()

    if problemas:
        print(f"\n  ✗ {len(problemas)} problema(s) de dato:")
        for p in problemas:
            print(f"     {p}")
    elif not args.contrastar:
        print(f"\n  ✓ {len(POLITIES)} polities, todos los rasgos con fuente")

    return 1 if (args.check and problemas) else 0


if __name__ == "__main__":
    _forzar_utf8()
    sys.exit(main())
