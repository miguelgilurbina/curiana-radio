"""
CURIANA — Motor de koiné emergente
===================================
Implementa el arco "diverso → converge" del diseño (ver DISENO_KOINE.md):

  1. EMOCIONAR sembrado por agente — semilla de idiolecto (Maturana: la emoción
     como disposición que abre el dominio de lo decible). Extraído del emocionar
     ya latente en los system_prompt, vuelto dato.
  2. IdiolectoAgente — perfil de frecuencia de formas por agente (entrenchment).
     Memoria larga que NO expira (= el "segundo compartimento" de CANON_TIERRA).
     Se pre-carga con las formas-semilla del emocionar → divergencia el día 1.
  3. CampoLexico — frecuencia comunitaria con decaimiento (rich-get-richer +
     recambio) para muestreo ponderado.
  4. distancia_idiolectal — la métrica que prueba (o refuta) la koineización:
     debe CONTRAERSE en el tiempo.

No hace llamadas LLM: se alimenta de lo que el Observer ya extrae cada turno.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Optional


# ══════════════════════════════════════════════════════════════════════
# I. EMOCIONAR — semilla de idiolecto por agente
# ══════════════════════════════════════════════════════════════════════
# Estructura: {disposicion, sesgo_lexico (dominios semánticos preferidos),
#              aspecto (sufijo favorito), registro (frase, metafora)}
# Los dominios de sesgo_lexico son las "categoria" de VOCABULARIO_BASE
# (geografia, fauna, flora, cosmos, parentesco, cuerpo, comercio, ritual,
#  alimentos, jerarquia, tiempo).

EMOCIONAR_SEED: dict[str, dict] = {
    # ── Tier I caquetío/caquetía ──
    "Manaure":    {"disposicion": "contención vigilante — la carga del que sostiene el cielo",
                   "sesgo_lexico": ["jerarquia", "cosmos", "comercio"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Shaboro":    {"disposicion": "ternura no nombrada e ironía grave",
                   "sesgo_lexico": ["ritual", "cosmos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "alta"}},
    "Nubiri-sha": {"disposicion": "cálculo afectuoso — la red de deudas y cuidados",
                   "sesgo_lexico": ["parentesco", "comercio", "jerarquia"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "baja"}},
    "Watapana":   {"disposicion": "avidez curiosa — el placer del trato y la novedad",
                   "sesgo_lexico": ["comercio", "geografia", "fauna"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "media"}},
    "Dara-ko":    {"disposicion": "duelo callado volcado en el oficio",
                   "sesgo_lexico": ["geografia", "fauna", "flora"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Paugis-sha": {"disposicion": "franqueza cálida — memoria viva de la comunidad",
                   "sesgo_lexico": ["cuerpo", "flora", "parentesco"],
                   "aspecto": "completivo", "registro": {"frase": "media", "metafora": "media"}},
    "Biro-ko":    {"disposicion": "orgullo terco del oficio de la sal",
                   "sesgo_lexico": ["comercio", "geografia", "alimentos"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Tawaka":     {"disposicion": "ambición tensa, apenas contenida",
                   "sesgo_lexico": ["jerarquia", "cuerpo", "fauna"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Saruro-sha": {"disposicion": "paciencia del hacer — el cuidado de la materia",
                   "sesgo_lexico": ["flora", "alimentos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Chiriguare": {"disposicion": "vigilancia dura — el deber de la defensa",
                   "sesgo_lexico": ["jerarquia", "geografia", "cuerpo"],
                   "aspecto": "completivo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Buio-sha":   {"disposicion": "visión naciente, asombro reverente",
                   "sesgo_lexico": ["ritual", "cosmos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "alta"}},
    "Corie-ko":   {"disposicion": "paciencia de la tierra — la reciprocidad del conuco",
                   "sesgo_lexico": ["flora", "geografia", "tiempo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Dare-nu":    {"disposicion": "apertura ávida — las ganas de pertenecer y aprender",
                   "sesgo_lexico": ["geografia", "fauna", "alimentos"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    # ── Tier I de contacto (insular / caribe) ──
    "Kadushi":    {"disposicion": "asombro del que va y vuelve por el agua abierta",
                   "sesgo_lexico": ["geografia", "comercio", "cosmos"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "media"}},
    "Marokoto-ni":{"disposicion": "cautela del extraño que mide antes de hablar",
                   "sesgo_lexico": ["comercio", "geografia"],
                   "aspecto": "prospectivo", "registro": {"frase": "corta", "metafora": "baja"}},
    # ── Tier II foráneos (aportantes de la mezcla koiné) ──
    "Tariwa":     {"disposicion": "respeto mutuo del mar — dos pueblos que se entienden pescando",
                   "sesgo_lexico": ["geografia", "fauna", "comercio"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Kawa-ni":    {"disposicion": "esfuerzo de quien aprende la lengua de prestigio",
                   "sesgo_lexico": ["geografia", "fauna"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
    "Piru-sha":   {"disposicion": "gratitud cautelosa de la recién integrada",
                   "sesgo_lexico": ["parentesco", "alimentos", "cuerpo"],
                   "aspecto": "continuativo", "registro": {"frase": "media", "metafora": "baja"}},
    "Nabaraka":   {"disposicion": "astucia del mercader de sierra",
                   "sesgo_lexico": ["comercio", "flora", "geografia"],
                   "aspecto": "prospectivo", "registro": {"frase": "media", "metafora": "baja"}},
    "Raka-bi":    {"disposicion": "esfuerzo de quien aprende la lengua de prestigio",
                   "sesgo_lexico": ["comercio", "geografia"],
                   "aspecto": "continuativo", "registro": {"frase": "corta", "metafora": "baja"}},
}

# Disposición de respaldo por etnia (para agentes sin seed explícita).
_DISPOSICION_ETNIA = {
    "caquetío":  "arraigo sereno en la lengua propia",
    "caquetía":  "arraigo sereno en la lengua propia",
    "caquetío_aruba": "memoria marina del que cruza el agua",
    "guaycarí":  "esfuerzo de quien aprende la lengua de prestigio",
    "guaycarí_caquetío": "vaivén entre dos hablas",
    "jirajara":  "pragmatismo del comerciante de frontera",
    "gayón":     "cautela del vecino serrano",
    "caribe":    "distancia del extraño que mide antes de hablar",
}

_ASPECTO_SUFIJO = {"completivo": "-ka", "continuativo": "-ni", "prospectivo": "-da"}

# Formas-firma por agente: vocabulario caquetío característico que ancla su
# idiolecto desde el día 1 (varias provienen de la línea "Vocabulario que usas"
# de su system_prompt). El `categoria` semántico está vacío en casi todo el
# caquetío activo, así que el sesgo se siembra con estas listas explícitas, no
# por muestreo de dominio. Distintas entre agentes → divergencia inicial.
FORMAS_SEED: dict[str, list[str]] = {
    "Manaure":    ["biro", "barsure", "kali", "kasha", "chiriguare", "maa-ka", "naa-ka"],
    "Shaboro":    ["urari", "barsure", "piache", "saruro", "kasha", "suna-ni", "naba-ni"],
    "Nubiri-sha": ["ama", "buri", "arua", "biro", "conuco", "paa-da", "raka-da"],
    "Watapana":   ["biro", "maure", "canoa", "habo", "arima", "naa-da", "wana-da"],
    "Dara-ko":    ["kuru", "canoa", "bara", "arima", "cunaro", "bagre", "wana-ni"],
    "Paugis-sha": ["urari", "arua", "buri", "ama", "kabo", "kono-ka", "wana-ka"],
    "Biro-ko":    ["biro", "habo", "dali", "sima", "naa-ka", "paa-ka"],
    "Tawaka":     ["chiriguare", "kabo", "arima", "habo", "wana-da", "naa-da"],
    "Saruro-sha": ["maure", "arua", "naure", "kuru", "kono-ni", "chaa-ni"],
    "Chiriguare": ["chiriguare", "sima", "habo", "kabo", "wana-ka", "naa-ka"],
    "Buio-sha":   ["barsure", "piache", "kasha", "suka", "urari", "naba-ni"],
    "Corie-ko":   ["conuco", "buco", "kuru", "dali", "kaya", "kono-ni"],
    "Dare-nu":    ["canoa", "arima", "bara", "kuru", "naa-da", "wana-da"],
    "Kadushi":    ["habo", "canoa", "biro", "kali", "maure", "naa-ni"],
    "Marokoto-ni":["biro", "habo", "canoa", "arima", "naa-da"],
    "Tariwa":     ["arima", "habo", "bara", "biro", "canoa", "wana-ni"],
    "Kawa-ni":    ["arima", "habo", "bara", "masa-ni", "naa-ni"],
    "Piru-sha":   ["ama", "buri", "arua", "conuco", "masa-ni"],
    "Nabaraka":   ["maure", "naure", "sima", "biro", "kuru", "paa-da"],
    "Raka-bi":    ["biro", "sima", "habo", "naa-ni", "paa-ni"],
}

# Núcleo caquetío compartido (fallback para agentes sin formas-firma): pronombres
# y verbos base que cualquiera usa. Se combina con el aspecto del emocionar.
_NUCLEO_FALLBACK = ["taya", "pia", "nüma", "naa", "wana", "maa", "ka", "mara"]


def emocionar_de(agente: str, etnia: Optional[str] = None) -> dict:
    """Emocionar sembrado de un agente, o uno derivado de su etnia."""
    if agente in EMOCIONAR_SEED:
        return EMOCIONAR_SEED[agente]
    return {
        "disposicion": _DISPOSICION_ETNIA.get(etnia or "caquetío", "arraigo en la lengua propia"),
        "sesgo_lexico": ["geografia", "fauna", "alimentos"],
        "aspecto": "continuativo",
        "registro": {"frase": "media", "metafora": "baja"},
    }


# ── Formas-semilla: vocabulario caquetío característico del agente ──
# Se usa para pre-cargar el idiolecto (divergencia día 1) y para el prompt.

def formas_semilla(agente: str, emo: dict) -> list[str]:
    """Formas-firma del agente. Explícitas (FORMAS_SEED) o, en su defecto, el
    núcleo compartido marcado con el aspecto del emocionar."""
    if agente in FORMAS_SEED:
        return list(dict.fromkeys(FORMAS_SEED[agente]))
    suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", "continuativo"), "-ni")
    base = list(_NUCLEO_FALLBACK)
    base += [f"naa{suf}", f"wana{suf}"]   # verbos base con su aspecto
    return list(dict.fromkeys(base))


# ══════════════════════════════════════════════════════════════════════
# II. IDIOLECTO POR AGENTE — entrenchment + memoria larga
# ══════════════════════════════════════════════════════════════════════

class IdiolectoAgente:
    """Perfil de frecuencia de formas de un agente. No expira en el run."""

    def __init__(self, agente: str, emocionar: Optional[dict] = None, peso_semilla: int = 2):
        self.agente = agente
        self.emocionar = emocionar or {}
        self.frecuencias: Counter[str] = Counter()
        self.acunaciones: set[str] = set()
        self.adopciones: set[str] = set()
        # Pre-carga: las formas-semilla entran con peso, para que el día 1 ya
        # haya divergencia entre agentes (precondición de la convergencia).
        for f in formas_semilla(agente, self.emocionar):
            self.frecuencias[f] += peso_semilla

    def registrar(self, formas, neologismos=None, adoptadas=None):
        for f in formas or []:
            self.frecuencias[f] += 1
        for neo in neologismos or []:
            forma = getattr(neo, "forma", neo)
            self.acunaciones.add(forma)
            self.frecuencias[forma] += 1
        for f in adoptadas or []:
            self.adopciones.add(f)

    def top_formas(self, n: int = 6) -> list[str]:
        return [f for f, _ in self.frecuencias.most_common(n)]

    def vector(self) -> Counter:
        return self.frecuencias


# ══════════════════════════════════════════════════════════════════════
# III. CAMPO LÉXICO COMUNITARIO — frecuencia + decaimiento
# ══════════════════════════════════════════════════════════════════════

class CampoLexico:
    """Frecuencia comunitaria de formas, con decaimiento por turno (recambio)."""

    def __init__(self, decaimiento: float = 0.97):
        self.pesos: dict[str, float] = {}
        self.decaimiento = decaimiento

    def registrar(self, formas, incremento: float = 1.0):
        for f in formas or []:
            self.pesos[f] = self.pesos.get(f, 0.0) + incremento

    def decaer(self):
        """Aplica decaimiento; descarta lo despreciable (formas que mueren)."""
        self.pesos = {
            f: p * self.decaimiento
            for f, p in self.pesos.items()
            if p * self.decaimiento > 0.05
        }

    def peso(self, forma: str) -> float:
        return self.pesos.get(forma, 0.0)

    def top(self, n: int = 20) -> list[tuple[str, float]]:
        return sorted(self.pesos.items(), key=lambda x: x[1], reverse=True)[:n]


# ══════════════════════════════════════════════════════════════════════
# IV. MÉTRICA DE CONVERGENCIA — distancia idiolectal
# ══════════════════════════════════════════════════════════════════════

def _coseno(a: Counter, b: Counter) -> float:
    comunes = set(a) & set(b)
    if not comunes:
        return 0.0
    num = sum(a[k] * b[k] for k in comunes)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return num / (na * nb) if na and nb else 0.0


def distancia_idiolectal(idiolectos: dict[str, "IdiolectoAgente"], min_formas: int = 5,
                         solo: Optional[set] = None) -> float:
    """Distancia idiolectal media (1 - coseno) entre pares de agentes activos.

    Es la firma de la koineización: DEBE CONTRAERSE en el tiempo. Solo se
    consideran agentes con vocabulario suficiente (min_formas).

    `solo`: si se pasa un conjunto de nombres, restringe la medición a esos
    agentes (los que REALMENTE hablaron) — clave porque los idiolectos se
    pre-cargan con formas-semilla para los 60 agentes, y medir sobre todos
    diluiría la señal con vectores estáticos de quienes nunca participaron.
    """
    vectores = [
        idio.vector() for nombre, idio in idiolectos.items()
        if (solo is None or nombre in solo) and len(idio.vector()) >= min_formas
    ]
    if len(vectores) < 2:
        return 0.0
    distancias = []
    for i in range(len(vectores)):
        for j in range(i + 1, len(vectores)):
            distancias.append(1.0 - _coseno(vectores[i], vectores[j]))
    return round(sum(distancias) / len(distancias), 4) if distancias else 0.0


# ══════════════════════════════════════════════════════════════════════
# V. INYECCIÓN EN EL PROMPT
# ══════════════════════════════════════════════════════════════════════

def prompt_emocionar(agente: str, etnia: Optional[str] = None) -> str:
    """Línea de emocionar (Maturana): disposición + firma morfológica.
    Moldea CÓMO lenguajea; el agente nunca habla DE su emoción."""
    emo = emocionar_de(agente, etnia)
    suf = _ASPECTO_SUFIJO.get(emo.get("aspecto", ""), "")
    extra = f" Tu aspecto natural es {suf}." if suf else ""
    return f"[Tu emocionar — moldea cómo hablas, no lo menciones]: {emo['disposicion']}.{extra}"


def prompt_idiolecto(idio: "IdiolectoAgente") -> str:
    """Bloque 'tu manera de hablar' derivado del perfil acumulado (entrenchment).
    Reemplaza los snippets de texto crudo de AgentMemory."""
    top = idio.top_formas(6)
    if not top:
        return ""
    partes = [f"sueles decir: {', '.join(top)}"]
    if idio.acunaciones:
        partes.append(f"acuñaste: {', '.join(sorted(idio.acunaciones)[:4])}")
    return f"[Tu manera de hablar]: {'; '.join(partes)}."


# ══════════════════════════════════════════════════════════════════════
# VI. FIJACIÓN POR COMPETENCIA — la koiné selecciona un nombre por concepto
# ══════════════════════════════════════════════════════════════════════
# Hallazgo (run 9bb920eb): la competencia NO ocurre sola — cada agente acuña
# para un concepto distinto, así que no hay variantes rivales que fijar. Una
# koiné, en cambio, nace de una NECESIDAD REFERENCIAL COMPARTIDA: aparece algo
# nuevo que VARIOS deben nombrar, cada uno propone, y la comunidad fija una
# forma. Por eso la fijación viene en dos piezas: (a) inducir la competencia con
# "eventos de nombramiento" (REFERENTES_NOVEDOSOS), y (b) resolverla aquí.

# Referentes sin palabra caquetía: cosas nuevas (contacto, novedad natural) que
# la comunidad necesita nombrar. Cada uno dispara una competencia.
REFERENTES_NOVEDOSOS: list[dict] = [
    {"id": "cuentas_vidrio", "desc": "unas cuentas brillantes y duras que un mercader trajo de tierras lejanas, nunca vistas aquí"},
    {"id": "cometa",         "desc": "una estrella con cola que cruza el cielo varias noches seguidas"},
    {"id": "eclipse",        "desc": "el sol se oscurece en pleno día y luego vuelve, como si algo lo cubriera"},
    {"id": "fiebre_manchas", "desc": "una fiebre nueva que llena la piel de manchas, que ningún piache había visto"},
    {"id": "metal_amarillo", "desc": "un trozo de metal amarillo y pesado, distinto del oro conocido, llegado por trueque"},
    {"id": "bestia_orilla",  "desc": "un animal enorme nunca visto, varado y muerto en la orilla del golfete"},
    {"id": "marea_roja",     "desc": "el agua del golfete se tiñe de rojo durante días y mata a los peces"},
    {"id": "tambor_caribe",  "desc": "un tambor de los caribe con un sonido grave y distinto a los nuestros"},
    {"id": "planta_quema",   "desc": "una planta nueva que cura la herida pero quema la boca al probarla"},
    {"id": "cuenta_insular", "desc": "una forma de contar el valor del trueque que enseñó el mensajero de las islas"},
]


class CompetenciaLexica:
    """Acumula soporte (frecuencia × prestigio) de las formas rivales que
    compiten por un MISMO concepto nuevo, y fija una como entrada koiné cuando
    domina su concepto por encima de un umbral."""

    def __init__(self, umbral_fijacion: float = 0.55, soporte_minimo: float = 3.0):
        # concepto_id -> {desc, variantes: Counter(forma->soporte), fijada, fijada_dia}
        self.referentes: dict[str, dict] = {}
        self._forma2concepto: dict[str, str] = {}
        self.umbral = umbral_fijacion
        self.soporte_min = soporte_minimo

    def _prestigio(self, agente: str) -> float:
        try:
            from curiana_social import prestigio_de
            return prestigio_de(agente)
        except Exception:
            return 0.3

    def activar(self, concepto_id: str, desc: str):
        self.referentes.setdefault(concepto_id, {
            "desc": desc, "variantes": Counter(), "fijada": None, "fijada_dia": None})

    def proponer(self, concepto_id: str, forma: str, agente: str):
        """Un agente acuña `forma` para `concepto_id` en un evento de nombramiento."""
        ref = self.referentes.get(concepto_id)
        if ref is None or ref["fijada"] or not forma:
            return
        ref["variantes"][forma] += 1.0 + self._prestigio(agente)
        self._forma2concepto[forma.lower()] = concepto_id

    def registrar_uso(self, forma: str, agente: str):
        """Reuso posterior de una forma en competencia → suma soporte (más leve
        que proponer). Es lo que hace que una variante gane sobre las otras."""
        cid = self._forma2concepto.get((forma or "").lower())
        if not cid:
            return
        ref = self.referentes[cid]
        if ref["fijada"]:
            return
        ref["variantes"][forma] += 0.5 + self._prestigio(agente)

    def evaluar_fijacion(self, dia: int) -> list[tuple[str, str]]:
        """Fija las competencias donde una variante domina. Devuelve las recién
        fijadas [(concepto_id, forma)]."""
        nuevas = []
        for cid, ref in self.referentes.items():
            if ref["fijada"] or len(ref["variantes"]) < 2:
                continue
            total = sum(ref["variantes"].values())
            forma, sup = ref["variantes"].most_common(1)[0]
            if total >= self.soporte_min and sup / total >= self.umbral:
                ref["fijada"] = forma
                ref["fijada_dia"] = dia
                nuevas.append((cid, forma))
        return nuevas

    def activas(self) -> dict[str, dict]:
        return {cid: ref for cid, ref in self.referentes.items()
                if not ref["fijada"] and ref["variantes"]}

    def prompt_competencias(self, top: int = 4) -> str:
        """Surface las competencias abiertas para que los agentes REUSEN una
        forma rival en vez de inventar otra — así una se impone."""
        lineas = []
        for ref in self.activas().values():
            formas = [f for f, _ in ref["variantes"].most_common(top)]
            if formas:
                lineas.append(f"{ref['desc']} → {', '.join(formas)}")
        if not lineas:
            return ""
        return ("[La comunidad aún busca nombre para cosas nuevas. Si hablas de "
                "alguna, ELIGE una de las formas que ya circulan, no inventes otra]:\n  "
                + "\n  ".join(lineas))

    def diccionario_koine(self) -> dict[str, dict]:
        """{concepto_id: {desc, forma, dia, soporte, n_variantes}} de las fijadas."""
        out = {}
        for cid, ref in self.referentes.items():
            if ref["fijada"]:
                out[cid] = {
                    "desc": ref["desc"], "forma": ref["fijada"],
                    "dia": ref["fijada_dia"],
                    "soporte": round(ref["variantes"][ref["fijada"]], 2),
                    "n_variantes": len(ref["variantes"]),
                }
        return out

    def reporte(self) -> str:
        lines = ["\n  ── KOINÉ — fijación por competencia ──"]
        fijadas = self.diccionario_koine()
        lines.append(f"  Conceptos nombrados: {len(self.referentes)} | "
                     f"fijados: {len(fijadas)} | en disputa: {len(self.activas())}")
        for cid, d in fijadas.items():
            lines.append(f"    ✓ {d['desc'][:42]:42} → {d['forma']}  "
                         f"(de {d['n_variantes']} variantes, día {d['dia']})")
        for cid, ref in self.activas().items():
            top = ref["variantes"].most_common(3)
            comp = ", ".join(f"{f}({s:.1f})" for f, s in top)
            lines.append(f"    … {ref['desc'][:42]:42} ⚔ {comp}")
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════
# Smoke test
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("── curiana_koine: smoke test ──")
    idios = {}
    for nm in ("Manaure", "Shaboro", "Dara-ko", "Corie-ko", "Tariwa"):
        emo = emocionar_de(nm)
        idio = IdiolectoAgente(nm, emo)
        idios[nm] = idio
        print(f"  {nm:12} emocionar='{emo['disposicion'][:40]}...'")
        print(f"               semilla: {idio.top_formas(6)}")
        print(f"               {prompt_emocionar(nm)}")

    d0 = distancia_idiolectal(idios)
    print(f"\n  distancia idiolectal inicial (debe ser ALTA): {d0}")

    # Simular convergencia: todos empiezan a usar las mismas formas
    comunes = ["taya", "wana-ka", "para", "biro", "kali", "naa-da", "ka", "mara"]
    for _ in range(30):
        for idio in idios.values():
            idio.registrar(comunes)
    d1 = distancia_idiolectal(idios)
    print(f"  distancia tras 30 turnos de uso común (debe BAJAR): {d1}")
    assert d1 < d0, "la convergencia debería reducir la distancia idiolectal"

    campo = CampoLexico()
    campo.registrar(comunes)
    campo.registrar(["taya", "para"])
    print(f"\n  campo léxico top: {campo.top(4)}")

    # ── competencia: 3 agentes acuñan rivales para un concepto; uno gana ──
    comp = CompetenciaLexica(soporte_minimo=2.0)
    comp.activar("cometa", "estrella con cola")
    comp.proponer("cometa", "kali-dusha", "Manaure")   # cacique, prestigio alto
    comp.proponer("cometa", "suka-wana", "Tariwa")      # foráneo, prestigio bajo
    comp.proponer("cometa", "kali-rua", "Kawa-ni")
    # reuso: la forma del prestigioso se propaga
    for _ in range(4):
        comp.registrar_uso("kali-dusha", "Shaboro")
    fij = comp.evaluar_fijacion(dia=5)
    print(f"  competencia 'cometa' fijada: {fij}")
    assert any(f == "kali-dusha" for _, f in fij), "debería ganar la forma del prestigioso reusada"
    print(f"  diccionario koiné: {comp.diccionario_koine()}")
    print("  ✓ smoke test OK")
