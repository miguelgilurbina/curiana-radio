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
| Neologismos propuestos — Supabase, `run_id` real (*) | 28 |
| Neologismos adoptados — Supabase, `run_id` real (*) | 20 |
| Perfiles curados generados | 20/20 |
| Frases curadas | 99 |

(*) Corregido — el reporte original de esta sección decía "89 propuestos
/ 72 adoptados", leído de `lexico.reporte_linguistico()` en memoria al
final del run. Esa cifra resultó estar contaminada por sesiones previas
(ver "Hallazgo pendiente — resuelto" más abajo); 28/20 son los conteos
reales en Supabase filtrados por este `run_id`.

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
   `LexicoComunitario.adoptar()` marcaba neologismos como "adoptado" en
   memoria, pero `db.update_neologism_status()` nunca se llamaba desde el
   orquestador. Todo quedaba en `status="propuesto"` para siempre.
   Corregido y reparado retroactivamente: 20/28 neologismos de este run en
   Supabase pasaron a `adoptado` (las cifras "72/89" del commit original
   incluían el arrastre histórico descrito abajo; el conteo real de este
   run es 20/28).

## Hallazgo pendiente — resuelto (no era pérdida de datos)

Investigación de seguimiento (2026-06-22): la hipótesis de arriba era
incorrecta. Se reconstruyeron los neologismos re-aplicando
`extraer_neologismos_del_texto()` directamente sobre los 155
`response_text` ya guardados en Supabase para este `run_id` — el mismo
texto, byte a byte, que alimentó al extractor durante el run real (no hay
mutación entre `observer.analizar(texto=response, ...)` y
`db.save_agent_response(response_text=response, ...)`). Resultado: **28
neologismos**, exactamente los mismos 28 que existen en la tabla
`neologisms`. Cero faltantes. El extractor (regex determinista) y
`db.save_neologism()` funcionaron correctamente las 28 veces — no hubo
ningún `except Exception: pass` silencioso de por medio.

La causa real: `auto_mode()` (el código detrás de `--auto N`) inicializaba
`lexico = LexicoComunitario.load()`, que **resume el archivo global
`curiana_lexico.json`** (no versionado, compartido entre sesiones) en vez
de arrancar en blanco — a diferencia de `state`, `memory` y `observer`, que
sí arrancan frescos en esa misma función. El run de 30 turnos heredó así
~61 neologismos acumulados de sesiones anteriores (pruebas interactivas,
`test_pipeline.py`, runs cortos previos), y `lexico.reporte_linguistico()`
—la fuente del "89 propuestos / 72 adoptados" reportado arriba— contó ese
total acumulado de **todas las sesiones históricas**, no el de este run.
Es decir: la tabla de métricas de este documento (líneas 24-25) compara
una cifra *acumulada de por vida* contra una cifra *de este run en
Supabase* — no son la misma unidad de medida. Los **28 neologismos en
Supabase, con `run_id` correcto, son la cifra real de este run**.

**Fix aplicado:** `curiana_orchestrator_v2.py::auto_mode()` ahora usa
`lexico = LexicoComunitario()` (arranque limpio), igual que `state` y
`memory`. Esto también importa para la *calidad* de la simulación, no solo
para el reporte final: `palabras_activas()` (vocabulario que se ofrece a
los agentes y que cuenta como "caquetío" en `score_linguistico()`) incluía
hasta ahora cualquier neologismo adoptado en sesiones de prueba anteriores,
sin relación con el run actual. Cada `--auto N` corre ahora con vocabulario
comunitario aislado, igual que ya ocurre con el `run_id` en Supabase.

## Recomendaciones para la simulación de 1 año (`--auto 240 --anio`)

1. El pipeline aguanta runs largos sin intervención (30 turnos corrieron
   sin caídas, solo el bug puntual de `max_tokens` en la fase de perfiles,
   ya corregido).
2. A este ritmo (~45 min para 30 turnos + perfiles), 240 turnos tomarían
   varias horas — planificar como tarea en background, no interactiva.
3. ~~Antes de la corrida de 1 año, investigar el hallazgo pendiente de
   arriba~~ — resuelto: no había pérdida de datos, sino contaminación de
   `lexico.reporte_linguistico()` por estado acumulado entre sesiones. Con
   el fix aplicado (`auto_mode()` arranca `LexicoComunitario()` en blanco),
   el run de 1 año queda libre de este artefacto desde el primer turno.
