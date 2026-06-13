"""
CURIANA — Motor Léxico y Morfológico
=====================================
Motor de reglas morfológicas arahuacanas para la simulación de
emergencia lingüística en la comunidad caquetía de Curiana.

Basado en:
  - Vocabulario caquetío atestiguado (Zavala Reyes 2015, Jahn 1927, Alvarado 1921)
  - Morfología Wayunaiki (Álvarez 2017; Goulet & Jusayú 1978; Mansen & Mansen 1984)
  - Cognados arahuacanos: Lokono, Taíno, Garifuna
  - Topónimos venezolanos como evidencia morfológica

Principio central:
  Los agentes NO memorizan todas las palabras. Internalizan REGLAS y
  las aplican productivamente para generar formas nuevas cuando
  encuentran un vacío léxico. Así funciona el lenguaje natural.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# I. VOCABULARIO BASE
# ══════════════════════════════════════════════════════════════════════

VOCABULARIO_BASE: dict[str, dict] = {

    # ── Caquetío atestiguado (fuentes coloniales y arqueológicas) ──────
    "barsure":    {"sig": "alma, esencia vital, fuerza interior",          "cat": "sust",  "fuente": "caquetío"},
    "buco":       {"sig": "represa, presa de agua, reservorio",             "cat": "sust",  "fuente": "caquetío"},
    "biro":       {"sig": "sal",                                            "cat": "sust",  "fuente": "caquetío"},
    "chiriguare": {"sig": "gavilán, ave rapaz grande",                      "cat": "sust",  "fuente": "caquetío"},
    "maure":      {"sig": "fibra de algodón, hilo para tejer",              "cat": "sust",  "fuente": "caquetío"},
    "urari":      {"sig": "veneno/medicina vegetal (curare)",               "cat": "sust",  "fuente": "caquetío"},
    "corie":      {"sig": "choza, habitación, espacio propio",              "cat": "sust",  "fuente": "caquetío"},
    "saruro":     {"sig": "árbol saruro (frutos pequeños)",                 "cat": "sust",  "fuente": "caquetío"},
    "tuqueque":   {"sig": "lagartija pequeña, gecko",                       "cat": "sust",  "fuente": "caquetío"},
    "coro":       {"sig": "cardón grande, cactus columnar",                 "cat": "sust",  "fuente": "caquetío/topónimo"},
    "piache":     {"sig": "chamán, curandero, intermediario espiritual",    "cat": "sust",  "fuente": "caquetío"},
    "caraota":    {"sig": "frijol negro, legumbre",                         "cat": "sust",  "fuente": "caquetío"},
    "pauji":      {"sig": "pavo de monte, ave grande",                      "cat": "sust",  "fuente": "caquetío"},
    "manaure":    {"sig": "título laudatorio del señor principal",          "cat": "título","fuente": "caquetío"},
    "curiana":    {"sig": "territorio de los caquetíos / lugar del cardón", "cat": "topón", "fuente": "caquetío"},

    # ── Arahuacano compartido (cognados en Wayunaiki, Lokono, Taíno) ──
    "wayuu":      {"sig": "persona, gente, ser humano",                     "cat": "sust",  "fuente": "wayunaiki"},
    "anüiki":     {"sig": "habla, palabra, lengua",                         "cat": "sust",  "fuente": "wayunaiki"},
    "anasa":      {"sig": "bueno, bien, bello (< anasü Wayunaiki)",         "cat": "adj",   "fuente": "wayunaiki-cogn"},
    "taya":       {"sig": "yo (1ra persona singular)",                      "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "waya":       {"sig": "nosotros (1ra persona plural)",                  "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "pia":        {"sig": "tú (2da persona singular)",                      "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "nüma":       {"sig": "él/ella (pronombre 3ra persona)",                "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "naya":       {"sig": "ellos, ellas (3ra persona plural)",              "cat": "pron",  "fuente": "wayunaiki-cogn"},
    "wanee":      {"sig": "uno (numeral)",                                  "cat": "num",   "fuente": "wayunaiki"},
    "piama":      {"sig": "dos (numeral)",                                  "cat": "num",   "fuente": "wayunaiki"},
    "apünüin":    {"sig": "tres (numeral)",                                 "cat": "num",   "fuente": "wayunaiki"},
    "pienchi":    {"sig": "cuatro (numeral)",                               "cat": "num",   "fuente": "wayunaiki"},
    "jarai":      {"sig": "cinco (numeral)",                                "cat": "num",   "fuente": "wayunaiki"},

    # ── Taíno (familia arahuacana, préstamos a todas las lenguas caribeñas) ──
    "hamaca":     {"sig": "red colgante para dormir",                       "cat": "sust",  "fuente": "taíno"},
    "canoa":      {"sig": "embarcación excavada en tronco",                 "cat": "sust",  "fuente": "taíno"},
    "cacique":    {"sig": "jefe, señor principal de la comunidad",          "cat": "sust",  "fuente": "taíno"},
    "maíz":       {"sig": "planta de maíz, grano principal",               "cat": "sust",  "fuente": "taíno"},
    "yuca":       {"sig": "tubérculo, mandioca amarga o dulce",             "cat": "sust",  "fuente": "arahuacano"},
    "batata":     {"sig": "camote, tubérculo dulce",                        "cat": "sust",  "fuente": "taíno"},
    "bohío":      {"sig": "casa comunal, choza redonda con techo cónico",   "cat": "sust",  "fuente": "taíno"},
    "conuco":     {"sig": "huerto familiar, parcela cultivada",             "cat": "sust",  "fuente": "taíno"},
    "iguana":     {"sig": "lagarto grande, iguana",                         "cat": "sust",  "fuente": "taíno/caribe"},

    # ── Raíces verbales arahuacanas (reconstruidas por comparación) ────
    "naa":        {"sig": "ir, moverse hacia",                              "cat": "v_raiz","fuente": "arahuacano"},
    "waa":        {"sig": "venir, aproximarse",                             "cat": "v_raiz","fuente": "arahuacano"},
    "kaa":        {"sig": "estar, existir, ser (cópula)",                   "cat": "v_raiz","fuente": "arahuacano"},
    "paa":        {"sig": "dar, ofrecer, transferir",                       "cat": "v_raiz","fuente": "arahuacano"},
    "maa":        {"sig": "decir, hablar, comunicar",                       "cat": "v_raiz","fuente": "arahuacano"},
    "taa":        {"sig": "tomar, coger, recibir",                          "cat": "v_raiz","fuente": "arahuacano"},
    "chaa":       {"sig": "hacer, construir, crear",                        "cat": "v_raiz","fuente": "arahuacano"},

    # ── Única frase Caquetía atestiguada ──────────────────────────────
    # "Chacamba cudanga" = ¿Cómo está usted? (saludo)
    # "Cudan de cuté"    = Para servirle a usted
    "chacamba":   {"sig": "¿cómo? (pregunta de estado)",                    "cat": "interr","fuente": "caquetío-atestiguado"},
    "cudanga":    {"sig": "usted, vos (2da persona formal)",                "cat": "pron",  "fuente": "caquetío-atestiguado"},
    "cudan":      {"sig": "servir, estar al servicio de",                   "cat": "v_raiz","fuente": "caquetío-atestiguado"},
    "cuté":       {"sig": "a usted, para usted (dativo formal)",            "cat": "pron",  "fuente": "caquetío-atestiguado"},
}


# ══════════════════════════════════════════════════════════════════════
# II. REGLAS MORFOLÓGICAS
# ══════════════════════════════════════════════════════════════════════

REGLAS_ASPECTO: dict[str, dict] = {
    "-ka": {
        "nombre": "completivo",
        "desc": "Acción terminada, resultado alcanzado. Equivale al pretérito perfecto.",
        "uso": "VERBO_RAIZ + -ka  →  acción completada",
        "ejemplos": [
            "naa-ka = ya fui / ya se fue",
            "paa-ka = ya di / ya entregué",
            "pescado-ka = ya pescé (hispanismo con sufijo caquetío)",
        ],
        "wayunaiki": "Triad A (-shi/-sü/-shii) en contexto de pasado",
        "instruccion_agente": (
            "Para indicar que algo ya terminó, agrega -ka al final: "
            "'Llegado-ka Manaure' = Manaure ya llegó. "
            "'Chaa-ka wa-buco' = nuestra represa ya está construida."
        ),
    },
    "-ni": {
        "nombre": "continuativo / imperfectivo",
        "desc": "Acción en progreso ahora mismo. Proceso activo.",
        "uso": "VERBO_RAIZ + -ni  →  acción en curso",
        "ejemplos": [
            "naa-ni = estoy yendo / va yendo",
            "pescando-ni = estoy pescando ahora",
            "maa-ni = estoy hablando",
        ],
        "wayunaiki": "-iraa (imperfective suffix)",
        "instruccion_agente": (
            "Para describir lo que haces ahora mismo, agrega -ni: "
            "'Naa-ni taya orilla' = Voy hacia la orilla ahora. "
            "'Maa-ni Shaboro' = Shaboro está hablando."
        ),
    },
    "-da": {
        "nombre": "prospectivo / intencional",
        "desc": "Acción futura o intención firme. Lo que se planea hacer.",
        "uso": "VERBO_RAIZ + -da  →  intención / futuro",
        "ejemplos": [
            "naa-da = voy a ir / iré",
            "paa-da = daré / voy a dar",
            "cudan-da = serviré / tengo intención de servir",
        ],
        "wayunaiki": "-ee (desiderative) + triad C (future intentive)",
        "instruccion_agente": (
            "Para expresar lo que harás o planeas, agrega -da: "
            "'Naa-da taya salinar' = Iré al salinar. "
            "'Maa-da taya Manaure' = Le hablaré a Manaure."
        ),
    },
}

REGLAS_LOCATIVAS: dict[str, dict] = {
    "-ana": {
        "nombre": "topónimo / lugar habitado",
        "desc": "Lugar donde abunda X, territorio asociado a X. Produce topónimos.",
        "uso": "RAÍZ + -ana  →  nombre de lugar",
        "ejemplos": [
            "coro + ana = Curiana (lugar/territorio del cardón)",
            "buco + ana = lugar de la represa",
            "biro + ana = lugar de la sal, salinar",
        ],
        "evidencia": "Curiana (Zavala 2015), Barquisimeto (*Barqui+sima/ima), Paraguaná (*Para+gua+na)",
        "instruccion_agente": (
            "Si necesitas nombrar un lugar, usa la raíz del elemento característico + -ana: "
            "Si hay muchos manglares, ese lugar es 'manglar-ana'. "
            "Si es donde se guarda la sal, es 'biro-ana'."
        ),
    },
    "-gua": {
        "nombre": "región / área asociativa",
        "desc": "Zona más amplia asociada con X. Menos específico que -ana.",
        "uso": "RAÍZ + -gua  →  región, área amplia",
        "ejemplos": [
            "Coro + gua = Corogua (región de los cardones) → hoy: Coro",
            "Para + gua + na = Paraguaná",
            "Araya (región salina)",
        ],
        "evidencia": "Topónimos venezolanos de Falcón y Sucre",
        "instruccion_agente": (
            "Para referirte a una región entera, usa -gua: "
            "'maure-gua' = la tierra del algodón (región)."
        ),
    },
    "-bana": {
        "nombre": "orilla / lugar limítrofe",
        "desc": "Borde de, orilla de, donde termina X y empieza otro espacio.",
        "uso": "RAÍZ + -bana  →  orilla, límite, punto de transición",
        "ejemplos": [
            "Mara+kai + bana = Maracaibana → Maracaibo (orilla del clan/lago Marakai)",
            "manglar + bana = orilla del manglar",
        ],
        "evidencia": "Maracaibo < *Maracai+bana (Oliver 1989, Alvarado 1921)",
        "instruccion_agente": (
            "Para orillas y límites: 'Golfete-bana' = la orilla del Golfete. "
            "'Manglar-bana' = el borde del manglar."
        ),
    },
}

REGLAS_AGENTIVAS: dict[str, dict] = {
    "-ko": {
        "nombre": "agente masculino",
        "desc": "Hombre cuya identidad/trabajo está asociado a X.",
        "uso": "RAÍZ + -ko  →  nombre o apodo masculino",
        "ejemplos": [
            "biro + ko = Biro-ko (el salinero, el hombre de la sal)",
            "corie + ko = Corie-ko (el de la choza, guardián del espacio)",
            "buco + ko = Buco-ko (el de la represa)",
        ],
        "wayunaiki": "-shi (masculine singular marker, triad A)",
        "instruccion_agente": (
            "Si un hombre trabaja con algo o es conocido por algo, su nombre o apodo "
            "puede formarse con -ko: el pescador experto podría llamarse 'bagre-ko'."
        ),
    },
    "-sha": {
        "nombre": "agente femenino",
        "desc": "Mujer cuya identidad/trabajo está asociado a X.",
        "uso": "RAÍZ + -sha  →  nombre o apodo femenino",
        "ejemplos": [
            "nubiri + sha = Nubiri-sha (la de la noche, la visionaria)",
            "paugis + sha = Paugis-sha (la de la totuma/vasija)",
            "maure + sha = Maure-sha (la tejedora, la del algodón)",
        ],
        "wayunaiki": "-sü (feminine/inanimate marker, triad A)",
        "instruccion_agente": (
            "Una mujer puede recibir nombre o apodo con -sha: "
            "la mujer que cuida el buco puede llamarse 'buco-sha'."
        ),
    },
}

REGLAS_POSESIVAS: dict[str, dict] = {
    "ta-": {
        "nombre": "posesivo 1ra singular",
        "desc": "Mi, mío/mía. Del hablante.",
        "uso": "ta- + SUSTANTIVO  →  mi X",
        "ejemplos": [
            "ta + barsure = ta-barsure (mi alma)",
            "ta + corie = ta-corie (mi choza)",
            "ta + anüiki = ta-anüiki (mi habla, mi lengua)",
        ],
        "wayunaiki": "ta- (1ra persona singular posesivo, cognado directo)",
    },
    "wa-": {
        "nombre": "posesivo 1ra plural",
        "desc": "Nuestro/nuestra. De nosotros, del grupo.",
        "uso": "wa- + SUSTANTIVO  →  nuestro X",
        "ejemplos": [
            "wa + barsure = wa-barsure (nuestra alma colectiva)",
            "wa + buco = wa-buco (nuestra represa)",
            "wa + anüiki = wa-anüiki (nuestra lengua)",
        ],
        "wayunaiki": "wa- (1ra persona plural posesivo, cognado directo)",
    },
    "ma-": {
        "nombre": "negativo / privativo",
        "desc": "Sin X, no X, carente de X.",
        "uso": "ma- + SUSTANTIVO  →  sin X / no X",
        "ejemplos": [
            "ma + barsure = ma-barsure (sin alma, vacío espiritual)",
            "ma + biro = ma-biro (sin sal)",
            "ma + anüiki = ma-anüiki (sin habla, mudo, extranjero incomprensible)",
        ],
        "wayunaiki": "ma- (prefijo negativo, cognado directo)",
    },
    "ka-": {
        "nombre": "posesivo genérico / asociativo",
        "desc": "El/la que tiene X, poseído por, asociado con.",
        "uso": "ka- + SUSTANTIVO  →  el/la de X",
        "ejemplos": [
            "ka + maure = ka-maure (el del algodón, el tejedor)",
            "ka + biro = ka-biro (el de la sal)",
            "ka + barsure = ka-barsure (el del alma fuerte, el espiritual)",
        ],
        "wayunaiki": "ka- (prefijo posesivo no-pronominal)",
    },
}

REGLAS_NUMERO: dict[str, dict] = {
    "-kana": {
        "nombre": "plural colectivo",
        "desc": "Grupo de, el pueblo de, todos los X.",
        "uso": "SUSTANTIVO + -kana  →  plural / colectivo",
        "ejemplos": [
            "wayuu + kana = wayuukana (el pueblo wayuu, todos los wayuu)",
            "barsure + kana = las almas",
            "piache + kana = los piaches, el conjunto de chamanes",
        ],
        "wayunaiki": "-kana (sufijo plural, COGNADO DIRECTO con Caquetío)",
    },
    "-naiki": {
        "nombre": "lengua de / habla de",
        "desc": "La lengua, el idioma, la forma de hablar de un pueblo.",
        "uso": "GENTILICIO + -naiki  →  nombre de la lengua",
        "ejemplos": [
            "wayuu + naiki = wayuunaiki (la lengua wayuu)",
            "caquetío + naiki = caquetío-naiki (la lengua caquetía)",
        ],
        "wayunaiki": "anüiki = habla → -naiki es sufijo derivado",
    },
}

# ── Tabla maestra de reglas (para inyectar en prompts) ──────────────
TODAS_LAS_REGLAS = {
    **REGLAS_ASPECTO,
    **REGLAS_LOCATIVAS,
    **REGLAS_AGENTIVAS,
    **REGLAS_POSESIVAS,
    **REGLAS_NUMERO,
}


# ══════════════════════════════════════════════════════════════════════
# III. LÉXICO COMUNITARIO VIVO
# ══════════════════════════════════════════════════════════════════════

@dataclass
class Neologismo:
    """Registro de una palabra nueva acuñada durante la simulación."""
    turno: int
    dia: int
    autor: str                         # nombre del agente que la acuñó
    forma: str                         # la nueva palabra
    componentes: str                   # ej: "coro + -ana"
    significado: str                   # propuesto por el agente
    contexto: str                      # frase donde apareció por primera vez
    regla_aplicada: str                # qué regla morfológica usó
    estado: str = "propuesto"          # propuesto | adoptado | rechazado | ignorado
    adoptado_por: list = field(default_factory=list)
    rechazado_por: list = field(default_factory=list)
    turno_resolucion: Optional[int] = None

    def to_dict(self) -> dict:
        return asdict(self)


class LexicoComunitario:
    """
    El léxico vivo de la comunidad. Crece turno a turno.

    Separado del VOCABULARIO_BASE porque este es el conocimiento
    heredado; el LexicoComunitario es lo que la generación actual
    está construyendo.
    """

    def __init__(self):
        self._lexico: dict[str, dict] = {}          # palabra → datos
        self._neologismos: list[Neologismo] = []     # historial ordenado

    # ── Consulta ──────────────────────────────────────────────────────

    def conoce(self, palabra: str) -> bool:
        """¿Existe esta palabra en el léxico base o comunitario?"""
        p = palabra.lower().strip()
        return p in VOCABULARIO_BASE or p in self._lexico

    def significado(self, palabra: str) -> Optional[str]:
        p = palabra.lower().strip()
        if p in VOCABULARIO_BASE:
            return VOCABULARIO_BASE[p]["sig"]
        if p in self._lexico:
            return self._lexico[p]["significado"]
        return None

    def palabras_activas(self) -> list[str]:
        """Todas las palabras disponibles (base + comunitario adoptado)."""
        base = list(VOCABULARIO_BASE.keys())
        adoptadas = [
            neo.forma for neo in self._neologismos
            if neo.estado == "adoptado"
        ]
        return base + adoptadas

    # ── Registro de neologismos ───────────────────────────────────────

    def registrar_neologismo(self, neo: Neologismo):
        self._neologismos.append(neo)
        if neo.estado == "adoptado":
            self._lexico[neo.forma] = {
                "significado": neo.significado,
                "autor": neo.autor,
                "dia": neo.dia,
            }

    def adoptar(self, forma: str, agente: str, turno: int):
        """Un agente adopta una palabra propuesta."""
        for neo in self._neologismos:
            if neo.forma == forma and neo.estado == "propuesto":
                if agente not in neo.adoptado_por:
                    neo.adoptado_por.append(agente)
                # Si 2+ agentes distintos la adoptaron → oficialmente adoptada
                if len(neo.adoptado_por) >= 2:
                    neo.estado = "adoptado"
                    neo.turno_resolucion = turno
                    self._lexico[forma] = {
                        "significado": neo.significado,
                        "autor": neo.autor,
                        "dia": neo.dia,
                    }
                break

    def rechazar(self, forma: str, agente: str, turno: int):
        """Un agente rechaza o ignora activamente una palabra propuesta."""
        for neo in self._neologismos:
            if neo.forma == forma and neo.estado == "propuesto":
                if agente not in neo.rechazado_por:
                    neo.rechazado_por.append(agente)
                if len(neo.rechazado_por) >= 3:
                    neo.estado = "rechazado"
                    neo.turno_resolucion = turno
                break

    # ── Reportes ──────────────────────────────────────────────────────

    def neologismos_pendientes(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "propuesto"]

    def neologismos_adoptados(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "adoptado"]

    def neologismos_rechazados(self) -> list[Neologismo]:
        return [n for n in self._neologismos if n.estado == "rechazado"]

    def reporte_linguistico(self) -> str:
        """Resumen del estado actual del léxico comunitario."""
        total_base = len(VOCABULARIO_BASE)
        adoptadas = self.neologismos_adoptados()
        pendientes = self.neologismos_pendientes()
        rechazadas = self.neologismos_rechazados()
        lines = [
            f"LÉXICO COMUNITARIO — Estado actual",
            f"  Vocabulario base (heredado): {total_base} palabras",
            f"  Neologismos adoptados:        {len(adoptadas)}",
            f"  En evaluación (propuestos):   {len(pendientes)}",
            f"  Rechazados/ignorados:         {len(rechazadas)}",
            f"  Total disponible:             {total_base + len(adoptadas)} palabras",
        ]
        if adoptadas:
            lines.append("\n  Palabras nuevas adoptadas:")
            for neo in adoptadas[-10:]:  # últimas 10
                lines.append(f"    [{neo.forma}] = {neo.significado}  (acuñó: {neo.autor}, día {neo.dia})")
        if pendientes:
            lines.append("\n  En evaluación:")
            for neo in pendientes[-5:]:
                adopc = len(neo.adoptado_por)
                lines.append(f"    [{neo.forma}] = {neo.significado}  ({adopc}/2 adopciones)")
        return "\n".join(lines)

    # ── Persistencia ──────────────────────────────────────────────────

    def save(self, path: str = "curiana_lexico.json"):
        data = {
            "lexico": self._lexico,
            "neologismos": [n.to_dict() for n in self._neologismos],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str = "curiana_lexico.json") -> "LexicoComunitario":
        lc = cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            lc._lexico = data.get("lexico", {})
            for nd in data.get("neologismos", []):
                neo = Neologismo(**nd)
                lc._neologismos.append(neo)
        except FileNotFoundError:
            pass
        return lc


# ══════════════════════════════════════════════════════════════════════
# IV. GENERADORES DE PROMPTS LINGÜÍSTICOS
# ══════════════════════════════════════════════════════════════════════

def prompt_reglas_breve() -> str:
    """
    Versión compacta de las reglas para inyectar en prompts Tier II/III.
    ~120 palabras.
    """
    return """[LENGUA CAQUETÍA — Reglas]:
ASPECTO: Agrega al final del verbo: -ka (ya hice), -ni (estoy haciendo), -da (haré/quiero hacer)
LUGAR: raíz + -ana = lugar de eso. raíz + -bana = orilla de. raíz + -gua = región de.
PERSONA: -ko = hombre/agente masc. -sha = mujer/agente fem. -kana = grupo/plural.
POSESIÓN: ta- = mi. wa- = nuestro. ma- = sin (negativo). ka- = el/la del/de la.
NUEVO: Si no tienes palabra para algo, CREA una con estas reglas. Escríbela entre corchetes:
[forma: raíz+sufijo = significado propuesto]
Ejemplo: Ves un lugar lleno de hamacas → [hamaca-ana: hamaca+-ana = lugar donde hacen hamacas]
USA el vocabulario base siempre que puedas en lugar del español."""


def prompt_reglas_completo() -> str:
    """
    Versión completa para Tier I (~300 palabras).
    """
    vocabulario_str = ", ".join(
        f"{k} ({v['sig'][:25]}...)" if len(v['sig']) > 25 else f"{k} ({v['sig']})"
        for k, v in list(VOCABULARIO_BASE.items())[:30]
    )
    return f"""[LENGUA CAQUETÍA — Sistema morfológico completo]:

VOCABULARIO DISPONIBLE (selección): {vocabulario_str}
[...y {len(VOCABULARIO_BASE) - 30} más en tu memoria]

ASPECTO VERBAL (siempre al final del verbo/acción):
  -ka = completivo: "naa-ka taya" = ya fui / "pescado-ka" = ya pesqué
  -ni = continuativo: "naa-ni taya" = voy ahora mismo
  -da = prospectivo: "naa-da taya" = iré / quiero ir

LOCATIVOS (para nombrar lugares):
  -ana = lugar habitado de X: "coro-ana" = Curiana (lugar del cardón)
  -bana = orilla/límite de X: "manglar-bana" = borde del manglar
  -gua = región asociada: "maure-gua" = tierra del algodón

AGENTIVOS (para nombres/roles):
  -ko = hombre asociado a X: "biro-ko" = el salinero
  -sha = mujer asociada a X: "maure-sha" = la tejedora

POSESIVOS (prefijos):
  ta- = mi: "ta-barsure" = mi alma
  wa- = nuestro: "wa-buco" = nuestra represa
  ma- = sin/no: "ma-anüiki" = sin habla (extranjero incomprensible)
  ka- = el/la del: "ka-maure" = el del algodón

PLURAL: -kana = "piache-kana" = los piaches / "wayuu-kana" = la gente

PRINCIPIO FUNDAMENTAL:
Cuando necesites decir algo y no tengas la palabra exacta, NO uses español.
Aplica las reglas y crea la forma nueva. Escríbela entre corchetes para que
la comunidad la evalúe: [nueva-forma: componentes = significado propuesto]
La comunidad decide si la adopta o no."""


def prompt_lexico_activo(lexico: LexicoComunitario) -> str:
    """
    Inyecta las palabras actualmente adoptadas por la comunidad
    (adicionales al vocabulario base).
    """
    adoptadas = lexico.neologismos_adoptados()
    if not adoptadas:
        return ""
    palabras = "; ".join(
        f"{n.forma} = {n.significado}" for n in adoptadas[-15:]
    )
    return f"[Palabras nuevas de la comunidad]: {palabras}"


def prompt_pendientes_evaluacion(lexico: LexicoComunitario) -> str:
    """
    Lista palabras propuestas que aún necesitan adopción/rechazo.
    Los agentes pueden reaccionar a ellas.
    """
    pendientes = lexico.neologismos_pendientes()
    if not pendientes:
        return ""
    items = "; ".join(
        f"'{n.forma}' (propuesta por {n.autor}: {n.significado})"
        for n in pendientes[-5:]
    )
    return f"[Palabras propuestas en evaluación — ¿las adoptas o rechazas?]: {items}"


# ══════════════════════════════════════════════════════════════════════
# V. EXTRACTOR DE NEOLOGISMOS
# ══════════════════════════════════════════════════════════════════════

import re

PATRON_NEOLOGISMO = re.compile(
    r'\[([^:\]]+):\s*([^=\]]+?)\s*=\s*([^\]]+?)\]'
)
"""
Captura: [forma: componentes = significado]
Ejemplo: [hamaca-ana: hamaca+-ana = lugar donde tejen hamacas]
Grupo 1: forma
Grupo 2: componentes
Grupo 3: significado
"""


def extraer_neologismos_del_texto(
    texto: str,
    autor: str,
    dia: int,
    turno: int,
) -> list[Neologismo]:
    """
    Extrae todos los neologismos propuestos en el texto de un agente.
    Formato esperado: [nueva-palabra: raíz+sufijo = significado]
    """
    neos = []
    for match in PATRON_NEOLOGISMO.finditer(texto):
        forma = match.group(1).strip().lower()
        componentes = match.group(2).strip()
        significado = match.group(3).strip()

        # Inferir regla aplicada
        regla = "desconocida"
        for sufijo in TODAS_LAS_REGLAS:
            if sufijo.startswith("-") and forma.endswith(sufijo[1:]):
                regla = sufijo
                break
        for prefijo in TODAS_LAS_REGLAS:
            if not prefijo.startswith("-") and forma.startswith(prefijo.rstrip("-")):
                regla = prefijo
                break

        neo = Neologismo(
            turno=turno,
            dia=dia,
            autor=autor,
            forma=forma,
            componentes=componentes,
            significado=significado,
            contexto=texto[:200],
            regla_aplicada=regla,
        )
        neos.append(neo)
    return neos


def detectar_uso_vocabulario(texto: str, lexico: LexicoComunitario) -> list[str]:
    """
    Detecta qué palabras del vocabulario conocido aparecen en el texto.
    """
    texto_lower = texto.lower()
    usadas = []
    for palabra in lexico.palabras_activas():
        if palabra in texto_lower:
            usadas.append(palabra)
    return usadas


def score_linguistico(texto: str, lexico: LexicoComunitario) -> dict:
    """
    Calcula métricas lingüísticas de una respuesta de agente.

    Retorna:
        palabras_caquetias: lista de palabras del vocabulario usadas
        neologismos_propuestos: lista de nuevas formas entre corchetes
        aspectos_usados: sufijos aspectuales detectados (-ka, -ni, -da)
        score: 0-10 (densidad caquetía)
        observacion: string descriptivo
    """
    usadas = detectar_uso_vocabulario(texto, lexico)
    neos_patron = PATRON_NEOLOGISMO.findall(texto)

    # Detectar sufijos aspectuales
    aspectos = []
    for sufijo, data in REGLAS_ASPECTO.items():
        s = sufijo[1:]  # sin el -
        if re.search(rf'\b\w+{re.escape(s)}\b', texto, re.IGNORECASE):
            aspectos.append(data["nombre"])

    # Score
    score = 0.0
    score += min(len(usadas) * 1.5, 6.0)       # hasta 6 pts por vocabulario
    score += min(len(neos_patron) * 1.5, 2.0)   # hasta 2 pts por neologismos
    score += min(len(aspectos) * 1.0, 2.0)      # hasta 2 pts por aspecto verbal
    score = round(min(score, 10.0), 1)

    obs_parts = []
    if usadas:
        obs_parts.append(f"Usó: {', '.join(usadas[:5])}")
    if aspectos:
        obs_parts.append(f"Aspecto: {', '.join(aspectos)}")
    if neos_patron:
        obs_parts.append(f"Propuso {len(neos_patron)} palabra(s) nueva(s)")
    if score < 3:
        obs_parts.append("⚠ Bajo uso de léxico caquetío")
    observacion = " | ".join(obs_parts) if obs_parts else "Sin uso de léxico caquetío detectado"

    return {
        "palabras_caquetias": usadas,
        "neologismos_propuestos": [m[0] for m in neos_patron],
        "aspectos_usados": aspectos,
        "score": score,
        "observacion": observacion,
    }


# ══════════════════════════════════════════════════════════════════════
# VI. HELPER: PROMPT DE REFUERZO PARA AGENTES CON SCORE BAJO
# ══════════════════════════════════════════════════════════════════════

def prompt_refuerzo(score: float, palabras_usadas: list[str]) -> str:
    """
    Si el score de un agente es bajo, genera un fragmento de refuerzo
    para inyectar en su próximo turno.
    """
    if score >= 6.0:
        return ""  # No necesita refuerzo
    sugerencias = [p for p in list(VOCABULARIO_BASE.keys())[:20] if p not in palabras_usadas][:6]
    sug_str = ", ".join(sugerencias)
    if score < 2.0:
        nivel = "CRÍTICO — Estás hablando casi solo en español"
        instruccion = (
            f"Recuerda: eres hablante de la lengua caquetía. "
            f"Palabras que DEBES usar: {sug_str}. "
            f"Aplica los sufijos -ka, -ni, -da para el aspecto verbal."
        )
    elif score < 4.0:
        nivel = "BAJO — Usa más léxico caquetío"
        instruccion = (
            f"Incorpora más palabras caquetías. Disponibles: {sug_str}. "
            f"Si no tienes palabra para algo, créala con las reglas [forma: componentes = sig]."
        )
    else:
        nivel = "MEDIO — Puedes profundizar"
        instruccion = (
            f"Intenta usar prefijos posesivos (ta-, wa-, ma-) "
            f"y acuñar alguna palabra nueva si hay vacío léxico."
        )
    return f"[Refuerzo lingüístico — {nivel}]: {instruccion}"


# ══════════════════════════════════════════════════════════════════════
# VII. UTILIDADES
# ══════════════════════════════════════════════════════════════════════

def vocabulario_para_agente(tier: int, lexico: LexicoComunitario) -> str:
    """
    Genera el bloque de léxico + reglas apropiado para cada tier.
    Tier I: completo. Tier II: breve. Tier III: solo sufijos.
    """
    lexico_activo = prompt_lexico_activo(lexico)
    pendientes = prompt_pendientes_evaluacion(lexico)

    if tier == 1:
        base = prompt_reglas_completo()
    elif tier == 2:
        base = prompt_reglas_breve()
    else:
        base = "[Lengua]: Usa -ka (hecho), -ni (haciendo), -da (haré). [nueva-palabra: raíz+sufijo = sig]"

    partes = [base]
    if lexico_activo:
        partes.append(lexico_activo)
    if pendientes and tier <= 2:
        partes.append(pendientes)
    return "\n".join(partes)


if __name__ == "__main__":
    # Test básico
    lc = LexicoComunitario()
    print(lc.reporte_linguistico())
    print()
    print("── Vocabulario base disponible ──")
    for k, v in list(VOCABULARIO_BASE.items())[:10]:
        print(f"  {k:15} = {v['sig']}")
    print(f"  ... y {len(VOCABULARIO_BASE) - 10} más")
    print()

    # Test del extractor
    texto_test = (
        "Naa-ni taya orilla. Ta-barsure siente el viento. "
        "El manglar aquí es diferente, lo llamo [manglar-bana: manglar+-bana = orilla viva del manglar]. "
        "Pescado-ka wanee canoa hoy."
    )
    resultado = score_linguistico(texto_test, lc)
    print("── Test score lingüístico ──")
    print(f"  Score: {resultado['score']}/10")
    print(f"  {resultado['observacion']}")
