"""
CURIANA — Observer Agent + Juez Lingüístico
=============================================
El Observer es un meta-agente que no participa en la simulación
pero observa todo. Analiza el lenguaje, detecta neologismos,
acumula métricas y genera reportes periódicos.

No tiene personalidad ni ubicación. Es el ojo externo del lingüista.

Modelo: claude-haiku-4-5-20251001 (mismo stack, sin dependencias nuevas)
"""

import json
import csv
import os
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict

import anthropic

from curiana_lexicon import (
    LexicoComunitario,
    Neologismo,
    score_linguistico,
    extraer_neologismos_del_texto,
    prompt_refuerzo,
    VOCABULARIO_BASE,
)


# ══════════════════════════════════════════════════════════════════════
# I. REGISTRO DE TURNO
# ══════════════════════════════════════════════════════════════════════

@dataclass
class RegistroInteraccion:
    """Una interacción de agente analizada lingüísticamente."""
    dia: int
    turno: int
    momento: str
    estacion: str
    agente: str
    etnia: str
    tier: int
    texto: str
    # Análisis lingüístico
    palabras_caquetias: list = field(default_factory=list)
    neologismos_propuestos: list = field(default_factory=list)
    aspectos_usados: list = field(default_factory=list)
    score: float = 0.0
    observacion: str = ""
    # Neologismos extraídos (objetos completos)
    neologismos_extraidos: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["neologismos_extraidos"] = [asdict(n) for n in self.neologismos_extraidos]
        return d

    def to_csv_row(self) -> dict:
        return {
            "dia": self.dia,
            "turno": self.turno,
            "momento": self.momento,
            "estacion": self.estacion,
            "agente": self.agente,
            "etnia": self.etnia,
            "tier": self.tier,
            "score": self.score,
            "palabras_caquetias": "|".join(self.palabras_caquetias),
            "neologismos": "|".join(self.neologismos_propuestos),
            "aspectos": "|".join(self.aspectos_usados),
            "texto_100": self.texto[:100],
        }


# ══════════════════════════════════════════════════════════════════════
# II. OBSERVER AGENT
# ══════════════════════════════════════════════════════════════════════

OBSERVER_SYSTEM = """Eres el Observador Lingüístico de la simulación comunitaria de la Curiana.
Tu trabajo es analizar respuestas de agentes y producir reportes sobre la evolución del lenguaje.

La Curiana es un asentamiento caquetío del Golfete de Coro, Venezuela, siglo XIV-XV.
Los agentes hablan caquetío-arahuaco. Tu trabajo es medir la densidad y pureza de su caquetío
y detectar fugas al español. Nuevas palabras pueden surgir cuando los agentes las crean productivamente
usando reglas morfológicas.

Tu análisis debe ser:
- PRECISO: solo marca como caquetío lo que claramente viene del vocabulario arahuaco
- EMPÁTICO: entiende el contexto cultural de cada interacción
- CIENTÍFICO: piensa como un lingüista de campo que observa emergencia lingüística

Responde SIEMPRE en JSON válido con la estructura que se te pida."""


class ObserverAgent:
    """
    El observer analiza interacciones y acumula el historial lingüístico.
    Genera reportes bajo demanda: por turno, día, estación, o año simulado.
    """

    def __init__(self, client: anthropic.Anthropic, lexico: LexicoComunitario):
        self.client = client
        self.lexico = lexico
        self._historial: list[RegistroInteraccion] = []
        self._scores_por_agente: dict[str, list[float]] = {}

    # ── Análisis de una interacción ───────────────────────────────────

    def analizar(
        self,
        agente: str,
        etnia: str,
        tier: int,
        texto: str,
        dia: int,
        turno: int,
        momento: str,
        estacion: str,
        usar_llm: bool = False,
    ) -> RegistroInteraccion:
        """
        Analiza lingüísticamente una respuesta de agente.

        usar_llm=True → usa Haiku para análisis más rico (cuesta tokens)
        usar_llm=False → análisis local con regex (gratis, suficiente para correr rápido)
        """

        # Análisis local (siempre se hace)
        metricas = score_linguistico(texto, self.lexico)
        neos = extraer_neologismos_del_texto(texto, agente, dia, turno)

        registro = RegistroInteraccion(
            dia=dia,
            turno=turno,
            momento=momento,
            estacion=estacion,
            agente=agente,
            etnia=etnia,
            tier=tier,
            texto=texto,
            palabras_caquetias=metricas["palabras_caquetias"],
            neologismos_propuestos=metricas["neologismos_propuestos"],
            aspectos_usados=metricas["aspectos_usados"],
            score=metricas["score"],
            observacion=metricas["observacion"],
            neologismos_extraidos=neos,
        )

        # Análisis enriquecido con LLM (opcional, para reportes importantes)
        if usar_llm and neos:
            enriquecido = self._analizar_con_llm(texto, neos, agente)
            if enriquecido:
                registro.observacion = enriquecido.get("observacion", registro.observacion)

        # Registrar neologismos en el léxico comunitario
        for neo in neos:
            self.lexico.registrar_neologismo(neo)

        # Acumular score del agente
        if agente not in self._scores_por_agente:
            self._scores_por_agente[agente] = []
        self._scores_por_agente[agente].append(metricas["score"])

        self._historial.append(registro)
        return registro

    def _analizar_con_llm(
        self,
        texto: str,
        neos: list[Neologismo],
        agente: str,
    ) -> Optional[dict]:
        """
        Análisis enriquecido: valida si los neologismos son morfológicamente
        coherentes con las reglas arahuacas.
        """
        neos_str = "\n".join(
            f"  [{n.forma}: {n.componentes} = {n.significado}]"
            for n in neos
        )
        prompt = f"""El agente {agente} dijo:
"{texto}"

Propuso estas palabras nuevas:
{neos_str}

Analiza si cada neologismo:
1. Es morfológicamente coherente con las reglas arahuacas (prefijos/sufijos conocidos)
2. Tiene sentido semántico en contexto caquetío
3. Podría ser adoptada por la comunidad

Responde en JSON:
{{
  "validaciones": [
    {{"forma": "palabra", "coherencia": true/false, "razon": "...", "recomendacion": "adoptar|rechazar|evaluar"}}
  ],
  "observacion": "Resumen del análisis lingüístico de este turno"
}}"""

        try:
            resp = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
                system=OBSERVER_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            return json.loads(resp.content[0].text)
        except Exception:
            return None

    # ── Detección de adopciones/rechazos ─────────────────────────────

    def procesar_adopciones(self, texto: str, agente: str, turno: int):
        """
        Detecta si un agente usó palabras propuestas por otros,
        registrándolo como adopción.
        """
        texto_lower = texto.lower()
        for neo in self.lexico.neologismos_pendientes():
            if neo.forma in texto_lower and neo.autor != agente:
                self.lexico.adoptar(neo.forma, agente, turno)

    # ── Feedback para próximo turno ───────────────────────────────────

    def feedback_para_agente(self, agente: str) -> str:
        """
        Genera feedback lingüístico para inyectar en el próximo prompt
        del agente si su score es bajo.
        """
        scores = self._scores_por_agente.get(agente, [])
        if not scores:
            return ""
        score_reciente = scores[-1]
        palabras_usadas = []
        if self._historial:
            ultimas = [r for r in self._historial if r.agente == agente]
            if ultimas:
                palabras_usadas = ultimas[-1].palabras_caquetias
        return prompt_refuerzo(score_reciente, palabras_usadas)

    # ── Score promedio por agente ─────────────────────────────────────

    def score_promedio(self, agente: str) -> float:
        scores = self._scores_por_agente.get(agente, [0.0])
        return round(sum(scores) / len(scores), 1)

    def ranking_linguistico(self) -> list[tuple[str, float]]:
        """Ranking de agentes por score promedio de densidad caquetía."""
        ranking = [
            (agente, self.score_promedio(agente))
            for agente in self._scores_por_agente
        ]
        return sorted(ranking, key=lambda x: x[1], reverse=True)

    # ── Reportes ──────────────────────────────────────────────────────

    def reporte_turno(self, dia: int, turno: int) -> str:
        """Reporte al final de cada turno."""
        registros = [r for r in self._historial if r.dia == dia and r.turno == turno]
        if not registros:
            return ""

        lines = [f"\n  ── Observer: Turno {dia}.{turno} ──"]
        for r in registros:
            score_str = f"{'●' * int(r.score)}{'○' * (10 - int(r.score))}"
            lines.append(f"  {r.agente:15} {score_str} {r.score:.1f}/10  {r.observacion[:60]}")
            for neo in r.neologismos_extraidos:
                lines.append(f"    ✦ NUEVO: [{neo.forma}] = {neo.significado}")

        neos_turno = sum(len(r.neologismos_extraidos) for r in registros)
        if neos_turno:
            lines.append(f"  → {neos_turno} neologismo(s) propuesto(s) este turno")

        pendientes = self.lexico.neologismos_pendientes()
        if pendientes:
            lines.append(f"  → {len(pendientes)} palabra(s) en evaluación comunitaria")

        return "\n".join(lines)

    def reporte_dia(self, dia: int) -> str:
        """Reporte al final de cada día (2 turnos)."""
        registros = [r for r in self._historial if r.dia == dia]
        if not registros:
            return ""

        total_interacciones = len(registros)
        score_dia = sum(r.score for r in registros) / total_interacciones if registros else 0
        palabras_dia = set()
        for r in registros:
            palabras_dia.update(r.palabras_caquetias)
        neos_dia = [n for r in registros for n in r.neologismos_extraidos]

        lines = [
            f"\n{'═'*60}",
            f"  REPORTE LINGÜÍSTICO — DÍA {dia}",
            f"{'═'*60}",
            f"  Interacciones analizadas: {total_interacciones}",
            f"  Score promedio del día:   {score_dia:.1f}/10",
            f"  Vocabulario caquetío activo hoy: {', '.join(sorted(palabras_dia)[:12])}",
        ]
        if neos_dia:
            lines.append(f"\n  Palabras nuevas propuestas ({len(neos_dia)}):")
            for neo in neos_dia:
                lines.append(f"    [{neo.forma}] = {neo.significado}  (por {neo.autor})")

        adoptadas_hoy = [n for n in self.lexico.neologismos_adoptados()
                         if n.dia == dia]
        if adoptadas_hoy:
            lines.append(f"\n  ✓ Adoptadas hoy ({len(adoptadas_hoy)}):")
            for neo in adoptadas_hoy:
                lines.append(f"    [{neo.forma}] = {neo.significado}")

        lines.append(f"\n  Léxico total disponible: {len(VOCABULARIO_BASE) + len(self.lexico.neologismos_adoptados())} palabras")
        lines.append(f"{'═'*60}")
        return "\n".join(lines)

    def reporte_estacion(self, estacion: str) -> str:
        """Reporte al final de una estación (seca o lluvias)."""
        registros = [r for r in self._historial if r.estacion == estacion]
        if not registros:
            return ""

        dias = sorted(set(r.dia for r in registros))
        score_estacion = sum(r.score for r in registros) / len(registros)

        # Evolución por día
        evolucion = {}
        for r in registros:
            if r.dia not in evolucion:
                evolucion[r.dia] = []
            evolucion[r.dia].append(r.score)
        evol_str = " → ".join(
            f"D{d}:{sum(v)/len(v):.1f}"
            for d, v in sorted(evolucion.items())
        )

        neos_estacion = [n for r in registros for n in r.neologismos_extraidos]
        adoptadas = [n for n in self.lexico.neologismos_adoptados()
                     if any(r.dia == n.dia and r.estacion == estacion for r in registros)]

        nombre_est = "Seca (viento + pesca)" if estacion == "seca" else "Lluvias (siembra + ritual)"

        lines = [
            f"\n{'╔'+'═'*58+'╗'}",
            f"  REPORTE DE ESTACIÓN — {nombre_est.upper()}",
            f"  Días simulados: {len(dias)}  |  Interacciones: {len(registros)}",
            f"  Score promedio: {score_estacion:.1f}/10",
            f"  Evolución: {evol_str}",
            f"\n  Neologismos propuestos: {len(neos_estacion)}",
            f"  Neologismos adoptados:  {len(adoptadas)}",
        ]

        # Top 3 agentes más activos lingüísticamente
        ranking = self.ranking_linguistico()
        if ranking:
            lines.append("\n  Top agentes por densidad lingüística:")
            for agente, score in ranking[:5]:
                bar = "█" * int(score) + "░" * (10 - int(score))
                lines.append(f"    {agente:15} {bar} {score:.1f}")

        if adoptadas:
            lines.append("\n  Palabras que entraron a la lengua esta estación:")
            for neo in adoptadas:
                lines.append(f"    [{neo.forma}] = {neo.significado}  (acuñó: {neo.autor})")

        lines.append(f"{'╚'+'═'*58+'╝'}")
        return "\n".join(lines)

    def reporte_anual_llm(self, anio_simulado: int) -> str:
        """
        Reporte anual generado con Haiku — síntesis profunda del año lingüístico.
        Este sí usa tokens pero se llama solo 1 vez por año simulado.
        """
        adoptadas = self.lexico.neologismos_adoptados()
        rechazadas = self.lexico.neologismos_rechazados()
        ranking = self.ranking_linguistico()[:5]

        datos = {
            "anio": anio_simulado,
            "total_interacciones": len(self._historial),
            "score_promedio_global": round(
                sum(r.score for r in self._historial) / max(len(self._historial), 1), 1
            ),
            "palabras_adoptadas": [
                {"forma": n.forma, "sig": n.significado, "autor": n.autor}
                for n in adoptadas
            ],
            "palabras_rechazadas": [n.forma for n in rechazadas],
            "top_agentes": [{"agente": a, "score": s} for a, s in ranking],
            "vocabulario_total": len(VOCABULARIO_BASE) + len(adoptadas),
        }

        prompt = f"""Eres un lingüista analizando el año {anio_simulado} de la simulación
de la comunidad caquetía de Curiana.

Datos del año:
{json.dumps(datos, ensure_ascii=False, indent=2)}

Escribe un reporte narrativo (4-6 párrafos) que describa:
1. Cómo evolucionó el lenguaje este año
2. Qué palabras nuevas entraron al léxico y por qué son significativas
3. Quiénes fueron los agentes más productivos lingüísticamente
4. Tendencias observadas (¿se usa más aspecto verbal? ¿más topónimos? ¿préstamos de otras etnias?)
5. Predicción: ¿qué palabras pendientes probablemente se adoptarán el próximo año?

Escribe como un lingüista apasionado que ha vivido este año junto a la comunidad."""

        try:
            resp = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=700,
                system=OBSERVER_SYSTEM,
                messages=[{"role": "user", "content": prompt}],
            )
            reporte = resp.content[0].text.strip()
            header = f"\n{'╔'+'═'*58+'╗'}\n  REPORTE ANUAL — AÑO SIMULADO {anio_simulado}\n{'╚'+'═'*58+'╝'}\n"
            return header + reporte + "\n"
        except Exception as e:
            return f"\n[Observer — reporte anual falló: {e}]\n"

    # ── Exportación ───────────────────────────────────────────────────

    def exportar_csv(self, path: str = "curiana_linguistica.csv"):
        """Exporta todo el historial de interacciones a CSV para análisis externo."""
        if not self._historial:
            return
        fieldnames = list(self._historial[0].to_csv_row().keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in self._historial:
                writer.writerow(r.to_csv_row())
        print(f"  → CSV exportado: {path} ({len(self._historial)} registros)")

    def exportar_neologismos_csv(self, path: str = "curiana_neologismos.csv"):
        """Exporta todos los neologismos propuestos/adoptados a CSV."""
        todos = [n for r in self._historial for n in r.neologismos_extraidos]
        if not todos:
            return
        fieldnames = ["turno", "dia", "autor", "forma", "componentes",
                      "significado", "regla_aplicada", "estado", "adoptado_por"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for n in todos:
                d = asdict(n)
                d["adoptado_por"] = "|".join(d.get("adoptado_por", []))
                writer.writerow({k: d[k] for k in fieldnames})
        print(f"  → Neologismos exportados: {path} ({len(todos)} entradas)")

    # ── Persistencia ──────────────────────────────────────────────────

    def save(self, path: str = "curiana_observer.json"):
        data = {
            "historial": [r.to_dict() for r in self._historial],
            "scores_por_agente": self._scores_por_agente,
            "timestamp": datetime.now().isoformat(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, client: anthropic.Anthropic, lexico: LexicoComunitario,
             path: str = "curiana_observer.json") -> "ObserverAgent":
        obs = cls(client, lexico)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            obs._scores_por_agente = data.get("scores_por_agente", {})
            for rd in data.get("historial", []):
                neos = [Neologismo(**n) for n in rd.pop("neologismos_extraidos", [])]
                r = RegistroInteraccion(**rd)
                r.neologismos_extraidos = neos
                obs._historial.append(r)
        except FileNotFoundError:
            pass
        return obs


# ══════════════════════════════════════════════════════════════════════
# TEST STANDALONE
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import anthropic as _anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Sin ANTHROPIC_API_KEY — test local solamente")
        client = None
    else:
        client = _anthropic.Anthropic(api_key=api_key)

    lc = LexicoComunitario()

    # Simular algunas interacciones
    textos_test = [
        ("Shaboro", "caquetío", 1,
         "Ta-barsure inquieto-ni. Naa-ka waya orilla antes del amanecer. "
         "El Golfete tiene olor diferente. Llamo a este lugar [golfete-bana: golfete+-bana = orilla interior del golfete]."),
        ("Tawaka", "caquetío", 1,
         "Pescado-ka wanee canoa esta mañana. Biro escaso-ni en wa-salinar. "
         "Hay que ir-da a las islas."),
        ("Bagre-ko", "guaycarí", 2,
         "El viento bueno para pescar. Traigo-da más pescado que ayer."),
        ("Nabaraka", "jirajara", 2,
         "Traer minerales de sierra. Ta-pueblo lejos. Querer intercambiar."),
    ]

    if client:
        obs = ObserverAgent(client, lc)
    else:
        # Test sin LLM
        class FakeObs:
            def __init__(self): pass
        obs = ObserverAgent.__new__(ObserverAgent)
        obs.client = None
        obs.lexico = lc
        obs._historial = []
        obs._scores_por_agente = {}

    for agente, etnia, tier, texto in textos_test:
        r = obs.analizar(agente, etnia, tier, texto, dia=1, turno=1,
                         momento="amanecer", estacion="seca", usar_llm=False)
        print(f"  [{agente}] score={r.score}/10  {r.observacion[:70]}")
        for neo in r.neologismos_extraidos:
            print(f"    ✦ [{neo.forma}] = {neo.significado}")

    print()
    print(obs.reporte_turno(1, 1))
    print()
    print(obs.reporte_dia(1))
    print()
    print(lc.reporte_linguistico())
