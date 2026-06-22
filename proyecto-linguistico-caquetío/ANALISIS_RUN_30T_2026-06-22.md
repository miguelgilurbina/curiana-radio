# Análisis — Simulación de 30 turnos (15 días, año 1)

**Run ID:** `2e729f3f-ebf4-4d23-8142-c4c65b06e27b`
**Corrido:** 2026-06-22, 06:08–06:31 UTC (~23 min de simulación + ~10 min de perfiles curados)
**Comando:** `python curiana_orchestrator_v2.py --auto 30 --perfiles --reporte`

Esta es la primera corrida larga con el pipeline completo calibrado en esta
sesión: lexicón honesto (157 caquetío real, 441 reconstrucciones sin
verificar excluidas del scoring), penalización de fuga a otras lenguas
arahuacas, chunking contextual del vocabulario, observador consolidado con
curación de perfiles, y contagio léxico social.

## Métricas cuantitativas

| Métrica | Valor |
|---|---|
| Respuestas de agentes | 155 |
| Score promedio | 7.21/10 |
| Composición — caquetío | **92.2%** |
| Composición — wayunaiki | 0.0% |
| Composición — lokono | 3.1% |
| Composición — taíno | 0.2% |
| Composición — proto-arahuaco | 0.8% |
| Neologismos propuestos (en memoria) | 89 |
| Neologismos adoptados (2+ agentes distintos) | 72 |
| Perfiles curados generados | 20/20 |
| Frases curadas | 99 |

El objetivo explícito de la sesión — "que el caquetío domine, ~70%+" — se
cumple con margen amplio. La fuga a otras lenguas arahuacas vivas
(wayunaiki/lokono/taíno) prácticamente desapareció tras retaguear el núcleo
fundacional del lexicón y penalizar esa fuga igual que el español.

## Hallazgos cualitativos

El reporte anual generado por el observador (LLM) describe el año como una
"explosión creativa lingüística": ningún neologismo fue rechazado, y la
comunidad convergió espontáneamente en conceptos-llave — `tensión-bana`
("donde tiembla la calma") fue acuñada independientemente y adoptada por
cinco agentes distintos (Shaboro, Corie-ko, Manaure, Watapana, Buio-sha),
sugiriendo que el modelo de contagio social (`curiana_social.py`) está
generando convergencia real, no solo ruido.

**Perfiles destacados** (ver `agent_profiles`/`agent_quotes` en Supabase
para los 20 completos):

- **Manaure** (avg 7.37) — arco de tensión entre autoridad temporal (sal) y
  legitimidad ritual (clima); el lenguaje se vuelve más imperativo hacia el
  final, consolidando su voz de mando.
- **Tawaka** (avg 7.27, 6 neologismos propuestos, 16 adoptados — el más
  prolífico) — evoluciona de ansiedad reflexiva a un guerrero templado pero
  fracturado por su afecto no resuelto hacia Buio-sha.
- **Shaboro** (avg 7.04) — transita de la vigilancia a la pedagogía
  deliberada, transmitiendo su saber chamánico a Buio-sha mientras su
  cuerpo envejece.

**Frase de mayor impacto** (9.8/10, según el analista): `Guaranaro-sha`
acuñó *"masa-bana-sha"* (lugar-de-comer-mujer) — el observador la describe
como "acto de habla que funda una categoría social inexistente... revolucionario
en contexto patriarcal", coherente con la ficha de Guaranaro-sha como
"pescadora que quebranta el tabú de género".

## Bugs encontrados y corregidos durante este análisis

El propio proceso de analizar el run reveló dos bugs reales, no hipotéticos:

1. **`max_tokens=1024` insuficiente en `analizar_agente_curado()`** — 4/20
   perfiles fallaron con JSON truncado a mitad de la última cita
   (protagonistas con 20+ intervenciones generan justificaciones largas).
   Subido a 2048; los 4 perfiles (Manaure, Dare-nu, Naure-sha, Buio-sha) se
   regeneraron correctamente reconstruyendo el historial desde Supabase.
2. **Adopción de neologismos nunca sincronizada con Supabase** —
   `LexicoComunitario.adoptar()` marcaba 72/89 neologismos como "adoptado"
   en memoria, pero `db.update_neologism_status()` nunca se llamaba desde
   el orquestador. Todo quedaba en `status="propuesto"` para siempre.
   Corregido y reparado retroactivamente (20/27 neologismos en Supabase
   pasaron a `adoptado`).

## Hallazgo pendiente (no resuelto)

De los **89 neologismos** que `LexicoComunitario` registró en memoria
durante el run, solo **28 llegaron a `db.save_neologism()`** en Supabase —
**52 nunca se persistieron en absoluto** (no es un problema de status, son
filas que no existen). Hipótesis de causa: el patrón de extracción
`PATRON_NEOLOGISMO` busca el formato explícito `[forma: componentes =
significado]` en el texto; probablemente solo calza la *primera* vez que
un agente lo escribe así — usos posteriores de la misma forma, ya
"sabida", no repiten el formato y no vuelven a intentar guardarse. Esto
afecta cualquier análisis cuantitativo sobre el *volumen* total de
neologismos (aunque no afecta los perfiles curados, que usan el texto
completo de las respuestas, no la tabla `neologisms`). Requiere revisar
`curiana_observer.py::analizar()` y el flujo de extracción antes de
decidir un fix — queda para otra sesión.

## Recomendaciones para la simulación de 1 año (`--auto 240 --anio`)

1. El pipeline aguanta runs largos sin intervención (30 turnos corrieron
   sin caídas, solo el bug puntual de `max_tokens` en la fase de perfiles,
   ya corregido).
2. A este ritmo (~45 min para 30 turnos + perfiles), 240 turnos tomarían
   varias horas — planificar como tarea en background, no interactiva.
3. Antes de la corrida de 1 año, vale la pena investigar el hallazgo
   pendiente de arriba (neologismos no persistidos), ya que a mayor escala
   esa pérdida de datos crece proporcionalmente y afectaría más al análisis
   de "qué palabras prendieron y cuáles no".
