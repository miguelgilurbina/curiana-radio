---
tipo: analisis
ambito: los 6 runs de la era de desarrollo (2026-06-22 a 2026-07-06)
respuestas_analizadas: 1489
datos: content/simulador/runs/index.json + historial de git
medido: 2026-08-03
---

# Qué probaron los seis runs — y qué no

> **Veredicto en una frase:** de los seis runs, **uno solo es un experimento
> controlado**; los otros cinco son pruebas de desarrollo del motor cuyos
> resultados **no son comparables entre sí**, porque entre corrida y corrida
> cambió tanto el motor como el instrumento que los mide.
>
> Esto no es un fracaso. Es exactamente lo que se esperaría de una fase de
> construcción — pero hay que decirlo con todas las letras **antes** de que
> alguien cite el 99% de caquetío como un resultado.

## Los datos

| Run | Fecha | Categoría | Días | Turnos | Resp. | Score | %caq | Neol. | Convergencia |
|---|---|---|---|---|---|---|---|---|---|
| `2e729f3f` | 06-22 | baseline | 15 | 30 | 155 | 7.21 | **92.2%** | 20 | — |
| `f8ef263d` | 06-29 | koiné | 15 | 30 | 155 | 7.53 | 99.2% | 28 | — |
| `9bb920eb` | 06-29 | koiné | 30 | 60 | 295 | 7.45 | 99.0% | 40 | acum. −39.7% |
| `20091e1f` | 06-29 | koiné | **0 ⚠️** | **0 ⚠️** | 290 | 7.42 | 99.0% | 41 | acum. −44.5% |
| `038d7b9d` | 07-06 | experimento | 30 | 60 | 300 | 7.31 | 99.1% | 63 | emerg. −17.9% |
| `bdc54134` | 07-06 | experimento | 30 | 60 | 294 | 7.30 | **99.7%** | 39 | emerg. −6.6% |

*Fuente: `content/simulador/runs/index.json`, generado 2026-07-07. 1489 respuestas.*

---

## 1. El hallazgo central: el instrumento se movió

`pct_caquetio` no es una observación del mundo: es la salida de
`score_linguistico()`, que **consulta el lexicón**. Si el lexicón cambia, la
métrica cambia de significado aunque los agentes hablen exactamente igual.

Y el lexicón cambió. Reconstruido desde git, el tamaño en cada corrida:

| Run | Entradas del lexicón |
|---|---|
| `2e729f3f` (baseline) | **~1717** |
| los cuatro de junio-julio | **~1276** |
| **hoy** | **1414** |

La caída de 1717 a 1276 es de **441 entradas exactas**. No es coincidencia: es
el commit `3b490b7`, *"aislar 441 candidatos no verificados del léxico activo"*,
del **2026-06-29 a las 02:34** — es decir, **entre el baseline y el primer run
koiné**.

### El confound, con nombres y horas

Entre la corrida baseline (06-22) y la primera koiné (06-29 16:26) entraron
**cinco cambios en catorce horas**, y solo uno de ellos es "el motor de koiné":

```
06-29 02:34  refactor(lexicon): aislar 441 candidatos no verificados
06-29 02:49  feat(koine): motor de koiné emergente
06-29 02:51  fix(scoring): prioridad de stopwords españolas sobre el léxico
06-29 12:01  feat(scoring): homógrafo "para" por contexto + compuerta de neologismos
06-29 12:10  fix(koine): ampliar blocklist de neologismos
```

**Tres de los cinco tocan el sistema de medición, no la conducta de los agentes.**

Por lo tanto: el salto de **92.2% → 99.2% de caquetío no es interpretable**. Puede
deberse al motor de koiné, o a que se quitaron 441 palabras que producían falsos
positivos, o a que se arregló el scorer dos veces esa misma madrugada. Con estos
datos **no se puede separar**, y ninguna corrida posterior vuelve a la condición
anterior para desempatar.

> El proyecto ya sabía que las 441 contaminaban `score_linguistico` — está escrito
> en `CLAUDE.md`. Lo que no estaba escrito es que **su retirada ocurrió justo entre
> las dos corridas cuya diferencia se atribuye a otra cosa**.

---

## 2. Qué sí quedó probado: la ablación

**El único experimento controlado del proyecto** es el par del 2026-07-06:

| | `038d7b9d` (normal) | `bdc54134` (ablación) |
|---|---|---|
| Motor | commit `0e632852` | **el mismo commit** |
| Fecha | mismo día | mismo día |
| Convergencia (emergente) | **−17.9%** | **−6.6%** |
| Conceptos fijados | 6 | 4 |
| Neologismos adoptados | **63** | 39 |

Esto **sí** es evidencia: mismo motor, mismo lexicón, mismo día, y la única
diferencia es apagar las tres inyecciones de prompt que empujan la convergencia.
La diferencia (−17.9% vs −6.6%) es la señal de koineización, y está bien medida.

Es también el diseño que hay que repetir: **la evidencia no está en el número de
un run, está en la diferencia entre dos runs que solo se distinguen en una cosa.**

---

## 3. Lo que las métricas actuales no discriminan

- **`avg_score` es plano**: 7.21 – 7.53 en seis corridas con motores muy
  distintos. Un rango de 0.32 puntos sobre 10. O el motor no cambió tanto como
  creemos, o **la métrica no mide lo que creemos**. Merece una revisión antes de
  usarla como criterio de nada.
- **`pct_caquetio` está saturado**: cinco de seis runs entre 99.0% y 99.7%. Una
  métrica que no varía no informa. Sirvió para detectar el problema original
  (27% de caquetío), pero **ya cumplió su función**; para la fase siguiente hace
  falta otra cosa.
- **Las lecturas de convergencia no son comparables**: los runs de junio usan
  "acumulada" y los de julio "emergente". Son métricas distintas
  (`DISENO_KOINE.md` §7 documenta tres lecturas). Comparar −39.7% con −17.9%
  **no significa nada**.
- **Ninguna corrida tiene barras de error.** Un solo run por condición, sin
  repeticiones ni semillas distintas. No sabemos cuánta de la diferencia
  observada es varianza del propio LLM.

---

## 4. Bugs de datos encontrados al analizar

1. **`20091e1f` tiene `total_dias: 0` y `total_turnos: 0`** con 290 respuestas
   registradas. Es imposible. El exportador (`export_runs_index.py`) no está
   calculando esos campos para ese run — probablemente porque la métrica se
   persistió con otro esquema. **Los datos del run pueden estar bien; el índice
   no.**
2. **El índice está congelado el 2026-07-07** y no se ha regenerado desde
   entonces. Cualquier análisis que lo use está mirando una foto de hace un mes.
3. **`agentes` varía de 20 a 38** entre runs con el mismo elenco de 60. Es el
   número de agentes que *hablaron*, no los que existen — pero el nombre del
   campo no lo dice, y `9bb920eb` está anotado como *"población constante"*
   cuando el índice le asigna 32.

---

## 5. Conclusión operativa

**Los seis runs cumplieron su función: construir y depurar el motor.** Encontraron
bugs reales, calibraron el scoring, demostraron que la koiné converge y produjeron
el par de ablación que es la única evidencia limpia del proyecto.

**Lo que no son es un conjunto de datos analizable.** No se puede escribir "el
caquetío subió del 92% al 99% gracias a la koiné" porque el dato no lo sostiene.

Y esta noche el lexicón volvió a moverse — 63 citas nuevas, una glosa corregida,
los homógrafos de 28 a 14 (lo que **cambia `score_linguistico` ahora mismo**), y 13
entradas pendientes de reclasificar por D10. **La condición para que el próximo run
sea analizable es que la base deje de moverse debajo de él.**

→ El protocolo para que eso no vuelva a pasar está en
[[04_protocolo_run_1_era_auditada]].

## Enlaces

[[BITACORA_RUNS]] · [[ANALISIS_RUN_30T_2026-06-22]] · [[DISENO_KOINE]] · [[PLAN_MAESTRO]] · [[LINEA_DE_TIEMPO]]
