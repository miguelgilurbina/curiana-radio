---
tipo: nota-viva
ambito: historia del proyecto, reconstruida del historial
periodo: 2026-06-13 → hoy
commits: 78
actualizado: 2026-08-03
---

# Línea de tiempo del proyecto

> Reconstruida de `git log` y de los documentos de cada fase. Existe por una
> razón concreta: **saber sobre qué base corrió cada cosa**. Sin esta línea no se
> puede decidir qué resultados siguen valiendo y cuáles hay que repetir — que es
> exactamente la pregunta abierta hoy (ver
> [[01_que_probaron_los_seis_runs]]).

## Las cuatro eras

| Era | Periodo | Qué se construyó | Estado de sus resultados |
|---|---|---|---|
| **I — Motor** | 06-13 → 06-23 | El simulador funcionando: agentes, contagio, scoring, dashboard | ⚠️ pruebas de desarrollo |
| **II — Koiné** | 06-29 → 07-08 | Convergencia, idiolecto, fijación, ablación | ⚠️ una sola corrida es evidencia limpia |
| **III — Corpus cultural** | 07-17 → 07-27 | 161 hechos etiquetados, 5 ensayos, 5 hojas de fuentes | ✅ vigente |
| **IV — Auditoría** | 07-27 → hoy | Moratoria, vault, minería de fuentes, censo de citas | ✅ en curso |

---

## Era I — construir el motor (2026-06-13 → 06-23)

**11 días. Del repo vacío al primer run largo.**

- **06-13** — `init repo + fix 3 critical bugs from audit`. El proyecto nace ya
  con una auditoría encima.
- **06-13** — `curiana_social.py`: contagio lingüístico entre agentes.
- **06-16** — suite de pipeline (30 checks) + generador de datos demo.
- **06-20** — canonicalización del esquema del lexicón; se separa categoría
  gramatical de dominio semántico. Se renombra *arahuacano* → **proto-arahuaco**.
- **06-21** — **expansión v4 del lexicón: +1003 palabras** (wayunaiki, lokono,
  kalinago, jirajaroide). Aquí nace el desbalance que hoy es [D11](https://github.com/miguelgilurbina/curiana-radio/issues/39).
- **06-21** — reconstrucción comparativa del caquetío + chunking contextual.
- **06-22** — se penaliza la **fuga a otra lengua arahuaca** y se retaguea el
  núcleo fundacional. El caquetío pasa de ~27% a ~91% del output.
- **06-22** — 🔬 **RUN `2e729f3f`** — primer run largo calibrado. 30 turnos,
  155 respuestas, 92.2% caquetío.
- **06-23** — `corregir 5 bugs reales encontrados en code review max effort`.

**Lo que quedó de esta era:** el motor. Y una lección que se repetiría: cada
inspección profunda encuentra deuda.

---

## Era II — la koiné emergente (2026-06-29 → 07-08)

**La era más productiva y la más comprimida. Casi todo ocurre en un solo día.**

### La madrugada del 29 de junio

Cinco cambios en catorce horas, y aquí está el confound que
[[01_que_probaron_los_seis_runs]] documenta:

```
02:34  aislar 441 candidatos no verificados del léxico activo   ← −441 entradas
02:49  motor de koiné emergente (emocionar, idiolecto, convergencia)
02:51  prioridad de stopwords españolas sobre el léxico          ← toca el scoring
12:01  homógrafo "para" por contexto + compuerta de neologismos  ← toca el scoring
12:10  ampliar blocklist de neologismos
```

- **06-29** — 🔬 **RUN `f8ef263d`** — primer run koiné. 99.2% caquetío.
  **El salto desde 92.2% no es atribuible a una sola causa.**
- **06-29** — población constante + métrica persistida + compuerta fonotáctica.
- **06-29** — 🔬 **RUN `9bb920eb`** — 60 turnos, 30 días. Convergencia −39.7%.
- **06-29** — fijación por competencia + eventos de nombramiento.
- **06-29** — 🔬 **RUN `20091e1f`** — diccionario koiné de 7 conceptos fijados.
  ⚠️ Su registro en el índice tiene `total_turnos: 0`, un bug de exportación
  nunca reparado.
- **06-29** — muestreo ponderado por frecuencia (*rich-get-richer*).
- **07-04** — métrica de convergencia **corregida** + soporte de ablación.
- **07-06** — 🔬 **RUNS `038d7b9d` + `bdc54134`** — **el experimento de control**:
  normal vs. ablación, mismo motor, mismo día. −17.9% vs −6.6%.
  **La única evidencia limpia del proyecto.**
- **07-07/08** — índice cross-run, secciones públicas, y el veredicto aprende a
  distinguir *plateau* de convergencia sostenida.

**Lo que quedó:** la prueba de que la koiné converge, y el diseño experimental
correcto (comparar dos runs que difieren en una sola cosa).

---

## Era III — el corpus cultural (2026-07-17 → 07-27)

**Cuatro sesiones en paralelo, una pregunta cada una, triple entregable
(ensayo + YAML + hoja de fuentes).**

- **07-17** — sesión 1/4 **familia**: matrilinealidad, avunculado, el cuello de
  botella matrimonial. De aquí sale la regla *precontacto ≠ colonial*.
- **07-17** — sesión 3/4 **creencia**: `boratio`, el segundo entierro
  atestiguado, y el resultado negativo de María Lionza.
- **07-17** — sesión 2/4 **ecología**: tierra pobre / mar rico, las capas de
  biosfera.
- **07-19** — sesión 4/4 **transmisión**: el currículo por edad, los puntos
  únicos de falla, y el programa wayuu que se levantó aparte.
- **07-26** — sesión 5 **geografía política**: *apopo/diao/boratio*,
  Todariquiba, la escala de 14-15 mil personas.

**Lo que quedó:** 161 hechos con etiqueta epistémica y referencia. **Vigente** —
ninguna corrección posterior lo ha tocado, salvo el §2 del ensayo 01 (ver Era IV).

---

## Era IV — la auditoría (2026-07-27 → hoy)

**El pivote. Deja de producirse y empieza a verificarse.**

- **07-27** — importar el glosario de **Zavala Reyes 2015**: del 23% al 76%.
  Aparecen palabras que **daban nombre a agentes** y no puntuaban como caquetío.
- **07-27** — **cuatro bugs del motor que sesgaban todo run** + tests de
  regresión. `uriacoa` resulta ser un apellido, no un título.
- **07-29** — 📋 **[[PLAN_MAESTRO]]**: moratoria de simulaciones. Cuatro ejes —
  FIDELIDAD, VAULT, JARDÍN, MOTOR.
- **07-29** — decisión de herramienta: Obsidian como lente, el repo como vault.
- **08-03** — **V0 + V1 del vault**: `INDICE`, 6 MOCs, 30 notas de fuente,
  `el tablero de decisiones`, verificador de enlaces. El inventario **medido**
  corrige tres supuestos (Alvarado sí es legible, Oviedo y Baños existe, hay 6
  archivos de 0 bytes).
- **08-03** — **minería en paralelo** de Alvarado, Gatschet, Van Buurt y cierre
  de Zavala (288/288). Se descubre que **13 entradas del lexicón no son
  caquetías** según su propia fuente — `piache` entre ellas.
- **08-03** — **F1**: 63 citas aplicadas, el censo de entradas sin cita baja de
  **82 a 19**.
- **08-03** — **F5 (Oliver cap. 2)**: el «arco norteño» estaba **invertido**. El
  caquetío desciende del lokono, no del guajiro-paraujano. → D11.
- **08-03** — **F11**: los topónimos son ecuaciones bilingües. 3 morfemas nuevos,
  10 corroboraciones, y la reduplicación confirmada como productiva.

---

## Lo que esta línea deja claro

1. **El lexicón cambió en las cuatro eras**, y sigue cambiando hoy. Ningún run
   corrió sobre la base actual.
2. **Los cinco runs anteriores al par de ablación no son comparables** ni entre
   sí ni con nada futuro.
3. **El corpus cultural es la parte más estable** del proyecto: producido en la
   Era III, sin correcciones de fondo salvo una.
4. **Cada auditoría profunda encontró deuda invisible** — en el motor (5 bugs),
   en el glosario (23% importado), en las etiquetas (`diao`, `uriacoa`), en la
   disponibilidad de fuentes (6 archivos vacíos), y en la filiación misma de la
   lengua (D11). El patrón no se ha roto ni una vez.

## Enlaces

[[01_que_probaron_los_seis_runs]] · [[04_protocolo_run_1_era_auditada]] · [[PLAN_MAESTRO]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) · [[BITACORA_RUNS]]
