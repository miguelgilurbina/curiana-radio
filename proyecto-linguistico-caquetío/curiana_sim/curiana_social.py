"""
CURIANA — Contagio lingüístico sociolingüístico
================================================

Modelo de difusión léxica entre los 60 agentes (auditoría Opus §5).

El "contagio" del sistema base solo marca una palabra como adoptada cuando
2 agentes distintos la usan, sin propagación dirigida. Este módulo añade:

  1. Un GRAFO SOCIAL (prestigio + vínculos fuertes + co-ubicación dinámica).
  2. DifusionLexica: rastrea la "presión de exposición" de cada neologismo
     sobre cada agente y emite sugerencias léxicas cuando cruza un umbral.
  3. Perfiles DIALECTALES por etnia, con normalización del score (justicia L2):
     un hablante de segunda lengua no se mide al rasero del nativo caquetío.

Integración (en curiana_orchestrator_v2.py):

    from curiana_social import DifusionLexica, prestigio_de, normalizar_por_dialecto

    difusion = DifusionLexica()            # una sola instancia por simulación

    # — al construir el prompt del agente —
    for forma, sig in difusion.sugerencias_para(agent_name, lexico=lexico):
        system_parts.append(
            f"[Has oído '{forma}' (={sig}) en boca de gente que respetas; "
            f"empléala si encaja].")

    # — tras analizar la respuesta del agente —
    metr["score"] = normalizar_por_dialecto(metr["score"], agent.get("etnia"))
    for forma in registro.palabras_caquetias:
        difusion.propagar_uso(forma, agent_name, state)
    for neo in registro.neologismos_extraidos:
        difusion.propagar_uso(neo.forma, agent_name, state)
"""

from __future__ import annotations

from curiana_agents import ALL_AGENTS, agents_at_location, get_agent


# ══════════════════════════════════════════════════════════════════════
# I. PRESTIGIO LINGÜÍSTICO — quién marca la norma
# ══════════════════════════════════════════════════════════════════════

# Overrides explícitos para los formadores de norma (cacique, piaches, esposa
# del cacique, mensajero insular...). El resto se deriva por tier/etnia.
PRESTIGIO: dict[str, float] = {
    "Manaure": 1.0,      # Señor de la Curiana, teocrático
    "Shaboro": 1.0,      # piache anciano
    "Nubiri-sha": 0.9,   # esposa del cacique
    "Paugis-sha": 0.85,  # autoridad femenina, conocimiento de plantas
    "Buio-sha": 0.7,     # piache aprendiz
    "Bana-mana": 0.7,
    "Chiriguare": 0.65,  # jefe guerrero
    "Watapana": 0.6,
    "Kadushi": 0.55,     # mensajero insular (caquetío_aruba), contacto léxico
}

# Defaults por tier cuando el agente no aparece en PRESTIGIO.
_PRESTIGIO_TIER = {1: 0.5, 2: 0.4, 3: 0.2}

# Etnias foráneas: su norma se propaga poco (L2, baja autoridad lingüística).
_PRESTIGIO_ETNIA_FORANEA = {
    "caribe": 0.15,
    "jirajara": 0.15,
    "gayón": 0.2,
    "guaycarí": 0.25,
    "guaycarí_caquetío": 0.3,
}


def prestigio_de(agente: str) -> float:
    """Prestigio lingüístico ∈ [0,1] de un agente: explícito > etnia foránea > tier."""
    if agente in PRESTIGIO:
        return PRESTIGIO[agente]
    info = get_agent(agente)
    etnia = info.get("etnia")
    if etnia in _PRESTIGIO_ETNIA_FORANEA:
        return _PRESTIGIO_ETNIA_FORANEA[etnia]
    return _PRESTIGIO_TIER.get(info.get("tier"), 0.2)


# ══════════════════════════════════════════════════════════════════════
# II. GRAFO SOCIAL — vínculos fuertes (mentoría, parentesco, trabajo)
# ══════════════════════════════════════════════════════════════════════

# peso ∈ [0,1] = frecuencia/intensidad del contacto lingüístico. Aristas
# dirigidas: VINCULOS[A][B] = cuánto escucha B a A. Se simetriza en vecinos().
VINCULOS: dict[str, dict[str, float]] = {
    "Shaboro":   {"Buio-sha": 0.95, "Manaure": 0.7, "Bana-mana": 0.5},
    "Manaure":   {"Nubiri-sha": 0.95, "Shaboro": 0.7, "Chiriguare": 0.6},
    "Nubiri-sha": {"Manaure": 0.95, "Saruro-sha": 0.5},
    "Paugis-sha": {"Suba-ko": 0.7, "Saruro-sha": 0.5},
    "Chiriguare": {"Tawaka": 0.6, "Pari-nu": 0.7},
    "Dara-ko":   {"Dare-nu": 0.9, "Tari-ko": 0.6, "Bagre-ko": 0.5},
    "Corie-ko":  {"Tawaka": 0.5, "Ita-ko": 0.7, "Buco-ko": 0.6},
    "Kadushi":   {"Watapana": 0.5, "Marokoto-ni": 0.4},
    "Watapana":  {"Biro-ko": 0.6, "Bagre-ko": 0.5},
}

# Arista por defecto entre agentes que comparten ubicación en un turno dado.
PESO_COUBICACION = 0.3


def vecinos(agente: str, state=None) -> dict[str, float]:
    """Red de escucha de un agente: vínculos explícitos (simetrizados) +
    co-ubicación dinámica del turno actual.

    Devuelve {otro_agente: peso} donde peso ∈ [0,1] aproxima cuánta exposición
    léxica recibe ese vecino cuando `agente` habla.
    """
    red: dict[str, float] = dict(VINCULOS.get(agente, {}))
    # simetría: si otro tiene a `agente` como destino, también lo oye de vuelta
    for otro, destinos in VINCULOS.items():
        if agente in destinos:
            red[otro] = max(red.get(otro, 0.0), destinos[agente])

    # co-ubicación: ubicación actual (override) o la por defecto
    info = get_agent(agente)
    ubic = None
    if state is not None:
        ubic = getattr(state, "ubicaciones_override", {}).get(agente)
    if ubic is None:
        ubic = info.get("ubicacion_default")

    if ubic:
        for otro in _agentes_en(ubic, state):
            if otro != agente:
                red[otro] = max(red.get(otro, 0.0), PESO_COUBICACION)
    return red


def _agentes_en(ubicacion: str, state=None) -> list[str]:
    """Agentes presentes en una ubicación, respetando overrides del estado."""
    presentes = set(agents_at_location(ubicacion))
    if state is not None:
        overrides = getattr(state, "ubicaciones_override", {})
        for ag, ub in overrides.items():
            if ub == ubicacion:
                presentes.add(ag)
            else:
                presentes.discard(ag)  # se movió a otra parte
    return sorted(presentes)


# ══════════════════════════════════════════════════════════════════════
# III. DIFUSIÓN LÉXICA — presión de exposición por neologismo
# ══════════════════════════════════════════════════════════════════════

class DifusionLexica:
    """Rastrea la 'presión de exposición' de cada forma léxica emergente sobre
    cada agente. Cuando un agente acumula exposición ≥ umbral, está listo para
    adoptar la palabra y se le sugiere en el prompt."""

    def __init__(self, umbral_adopcion: float = 0.6):
        # forma -> {agente -> exposicion acumulada [0..∞)}
        self.exposicion: dict[str, dict[str, float]] = {}
        # formas que el agente ya ha empleado (no re-sugerir)
        self.usadas_por: dict[str, set[str]] = {}
        self.umbral = umbral_adopcion

    def propagar_uso(self, forma: str, hablante: str, state=None) -> None:
        """Cuando `hablante` usa `forma`, sube la exposición de sus vecinos en
        proporción a (prestigio del hablante × fuerza del vínculo)."""
        if not forma:
            return
        forma = forma.lower().strip()
        self.usadas_por.setdefault(hablante, set()).add(forma)

        pres = prestigio_de(hablante)
        red = vecinos(hablante, state)
        mapa = self.exposicion.setdefault(forma, {})
        for vecino, peso in red.items():
            mapa[vecino] = mapa.get(vecino, 0.0) + pres * peso

    def sugerencias_para(self, agente: str, lexico=None, top: int = 3) -> list[tuple[str, str]]:
        """Formas que `agente` está listo para adoptar (exposición ≥ umbral),
        excluyendo las que ya usó. Ordenadas por exposición descendente."""
        ya = self.usadas_por.get(agente, set())
        candidatas = []
        for forma, mapa in self.exposicion.items():
            if forma in ya:
                continue
            exp = mapa.get(agente, 0.0)
            if exp >= self.umbral:
                sig = ""
                if lexico is not None and hasattr(lexico, "significado"):
                    sig = lexico.significado(forma) or ""
                candidatas.append((forma, sig, exp))
        candidatas.sort(key=lambda x: x[2], reverse=True)
        return [(f, s) for f, s, _ in candidatas[:top]]

    def exposicion_de(self, agente: str, forma: str) -> float:
        """Exposición acumulada de un agente a una forma (para inspección/tests)."""
        return self.exposicion.get(forma.lower().strip(), {}).get(agente, 0.0)


# ══════════════════════════════════════════════════════════════════════
# IV. VARIACIÓN DIALECTAL — sesgos por etnia y normalización del score
# ══════════════════════════════════════════════════════════════════════

# La variación es por ETNIA/ROL (sociolingüística real), no por tier (artefacto
# de coste). densidad_objetivo = cuánto caquetío se espera de ese grupo.
DIALECTOS: dict[str, dict] = {
    "caquetío":         {"densidad_objetivo": 0.65, "rasgos": []},
    "caquetía":         {"densidad_objetivo": 0.65, "rasgos": []},
    "caquetío_aruba":   {"densidad_objetivo": 0.60,
                         "rasgos": ["lenición -k- > -g-", "léxico marino insular"]},
    "guaycarí":         {"densidad_objetivo": 0.45,
                         "rasgos": ["sintaxis SVO ocasional", "errores de prefijo"]},
    "guaycarí_caquetío": {"densidad_objetivo": 0.50,
                          "rasgos": ["mezcla guaycarí-caquetía"]},
    "gayón":            {"densidad_objetivo": 0.40,
                         "rasgos": ["orden de palabras alterado"]},
    "jirajara":         {"densidad_objetivo": 0.35,
                         "rasgos": ["orden de palabras alterado", "prefijos mal aplicados"]},
    "caribe":           {"densidad_objetivo": 0.25,
                         "rasgos": ["SVO estricto", "léxico caquetío mínimo"]},
}

# Densidad de referencia (la del nativo caquetío). El score se normaliza contra ella.
_DENSIDAD_REF = DIALECTOS["caquetío"]["densidad_objetivo"]


def perfil_dialectal(etnia: str | None) -> dict:
    """Perfil dialectal de una etnia (caquetío nativo por defecto / T3 sin etnia)."""
    return DIALECTOS.get(etnia or "caquetío", DIALECTOS["caquetío"])


def rasgos_dialectales(etnia: str | None) -> list[str]:
    """Rasgos de estilo a inyectar en el prompt del agente según su etnia."""
    return perfil_dialectal(etnia).get("rasgos", [])


def normalizar_por_dialecto(score_crudo: float, etnia: str | None) -> float:
    """Normaliza el score por la densidad objetivo del dialecto (justicia L2):
    un guaycarí no debe penalizarse al rasero del nativo. Acotado a [0,10]."""
    objetivo = perfil_dialectal(etnia)["densidad_objetivo"] or _DENSIDAD_REF
    return round(min(score_crudo * (_DENSIDAD_REF / objetivo), 10.0), 1)


def prompt_rasgos_dialectales(etnia: str | None) -> str:
    """Fragmento de prompt con la orientación de estilo dialectal (o "" si nativo)."""
    rasgos = rasgos_dialectales(etnia)
    if not rasgos:
        return ""
    return ("[Tu habla, por tu origen, tiene estos rasgos: "
            + "; ".join(rasgos) + ". Es característico, no un error.]")


# ══════════════════════════════════════════════════════════════════════
# Smoke test
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("── curiana_social: smoke test ──")
    d = DifusionLexica()

    # Shaboro (prestigio 1.0) acuña [sima-bana]; su aprendiz Buio-sha (vínculo 0.95)
    # debería cruzar el umbral 0.6 en un solo turno.
    d.propagar_uso("sima-bana", "Shaboro")
    exp_buio = d.exposicion_de("Buio-sha", "sima-bana")
    print(f"  exposición Buio-sha a 'sima-bana' tras 1 uso de Shaboro: {exp_buio:.2f}")
    assert exp_buio >= 0.6, "el aprendiz debería estar listo para adoptar"
    sugs = d.sugerencias_para("Buio-sha")
    print(f"  sugerencias para Buio-sha: {sugs}")
    assert any(f == "sima-bana" for f, _ in sugs)

    # Un periférico (Marokoto-ni, caribe, sin vínculo con Shaboro) no debería adoptar.
    sugs_lejos = d.sugerencias_para("Marokoto-ni")
    print(f"  sugerencias para Marokoto-ni (periférico): {sugs_lejos}")

    # Normalización dialectal: el mismo score crudo vale más para un L2.
    print(f"  score 4.5 caquetío → {normalizar_por_dialecto(4.5, 'caquetío')}")
    print(f"  score 4.5 caribe   → {normalizar_por_dialecto(4.5, 'caribe')}")
    assert normalizar_por_dialecto(4.5, "caribe") > normalizar_por_dialecto(4.5, "caquetío")

    print(f"  prestigio Manaure={prestigio_de('Manaure')}  "
          f"Marokoto-ni={prestigio_de('Marokoto-ni')}  Kori(T3)={prestigio_de('Kori')}")
    print("  ✓ todos los asserts OK")
