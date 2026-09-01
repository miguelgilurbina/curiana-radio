---
tipo: nota
pregunta: "¿Cómo se corre, se analiza y se muestra un run?"
medido: 2026-08-06
base: los 23 runs de la base local
---

# La dinámica de los runs — de la simulación a lo que se muestra

> Escrito después de analizar los 23 runs que ya existen. Casi todas las
> decisiones de abajo salen de algo que salió mal en ellos.

## El problema que hay que resolver primero

De los 23 runs almacenados, **ninguno es plenamente citable**. No porque estén
mal corridos, sino porque no se puede saber contra qué corrieron: hubo que
reconstruirlo de git para poder analizar los seis primeros. Y tres cosas más:

| Lo que pasó | Consecuencia |
|---|---|
| `pct_caquetio` saturada (91% en 1.0) | la métrica principal no distingue nada |
| La longitud del prompt predice el score (r = −0.48) | cualquier lectura por agente puede ser un artefacto de autoría |
| n = 1 run por brazo | el resultado de koiné es señal, no prueba |

**La dinámica de abajo está diseñada para que esas cuatro cosas no vuelvan a
pasar.**

---

## Las cuatro etapas

```
  1. SELLAR    →   2. CORRER    →   3. LEER (×2)    →   4. MOSTRAR
  la huella        el par            observador           el jardín
                   normal/ablación   + cronista
```

### 1. Sellar — antes de arrancar

`huella_de_base.py` graba en la propia fila del run: hash y tamaño del lexicón,
del corpus y del elenco; la polity simulada; el commit del motor; y **si el
árbol estaba sucio**.

> **Un run con el árbol sucio no es citable.** El commit dice una cosa y el
> código que corrió decía otra. No se impide —hay motivos legítimos para probar
> algo sin commitear— pero queda marcado y el análisis puede excluirlo.

El elenco entra en la huella aunque el issue original no lo pedía, y es el que
más sesga: si alguien reescribe una ficha entre dos runs, los scores cambian sin
que nada más haya cambiado.

### 2. Correr — en pares, no sueltos

**La unidad de experimento no es el run: es el par normal/ablación.** Un run
solo no dice nada, porque no hay contra qué contrastarlo.

```bash
python curiana_orchestrator_v2.py --auto 60 --perfiles --reporte
python curiana_orchestrator_v2.py --auto 60 --perfiles --reporte --ablacion
```

Y **el par hay que repetirlo**. Con n=1 los 30 días de un run son
pseudo-réplicas: comparten agentes, semilla y trayectoria, así que los p-valores
contestan *"¿difieren estas dos series?"*, no *"¿difieren estas dos
condiciones?"*. Para lo segundo hace falta tratar el **run** como unidad, y eso
pide 5 pares como mínimo.

### 3. Leer — dos lecturas del mismo run, y esa es la idea

Aquí está lo que el proyecto no tenía y sí necesita: **el mismo material leído
desde fuera y desde dentro.**

| | El observador | El cronista |
|---|---|---|
| Qué es | `curiana_observer.py` | `curiana_cronista.py` |
| Desde dónde mira | fuera | dentro |
| Qué produce | métricas, convergencia, scores | arcos, qué le pasó a quién |
| En qué lengua piensa | análisis | `boratio`, `diao`, `barsure` |
| Qué estatus tiene | medición | **lectura, nunca fuente** |

No es decoración. Es la misma tensión que atraviesa el proyecto entero: las
fuentes describen a los caquetíos en vocabulario ajeno, y el proyecto lleva
meses corrigiéndolo. El cronista aplica esa corrección a los datos **propios**.

Y hay una razón práctica: el observador puede decirte que la distancia de koiné
bajó 0.07, pero no que **Korie-ko acuñó treinta y siete palabras y nadie adoptó
ninguna**. Eso es un arco, y hace falta leerlo.

### 4. Mostrar — la evidencia debajo, no delante

El orden que propongo para el jardín público: **el cronista arriba, las
métricas debajo como respaldo**. Un gráfico de distancia de koiné no le dice
nada a nadie que no sepa ya qué es una koiné; «el año en que la palabra de
Shaboro para la fiebre se impuso sobre la de Manaure» sí.

Pero con la evidencia a un clic, siempre. Es lo que separa esto de la
divulgación floja.

---

## Qué datos interesan, por nivel

Cuatro niveles, y el de abajo no vale sin el de arriba.

### Nivel 0 — ¿es válido este run?

`huella` completa · `motor_sucio` false · el exportador da turnos > 0 (hoy hay
un run, `20091e1f`, con 0 turnos y 290 respuestas — [#42](https://github.com/miguelgilurbina/curiana-radio/issues/42))

**Si falla el nivel 0, lo demás no se mira.**

### Nivel 1 — la lengua (la pregunta científica)

| Qué | Cómo | Estado |
|---|---|---|
| Convergencia | `koine_metrics`, 3 lecturas/día | ✅ funciona |
| Composición por lengua | `word_uses.source_language` | ✅ arreglado (era 50% NULL) |
| **Morfología productiva** | uso de aspectos y prefijos | 🆕 **ahora medible** |
| Neologismos | propuestos → adoptados → fijados | ✅ |
| Score | `agent_responses.score` | ⚠️ controlar longitud de prompt |
| ~~`pct_caquetio`~~ | — | 🔴 **saturada, no usar** ([#69](https://github.com/miguelgilurbina/curiana-radio/issues/69)) |

La morfología productiva es lo nuevo y lo más interesante: hasta el arreglo del
`source_language`, las 18.752 formas con sufijo de aspecto se guardaban sin
lengua. Ahora se puede preguntar **si los agentes usan más morfología con el
tiempo**, que es una pregunta mucho mejor que «¿hablan caquetío?» — a la que
todos contestan que sí al 99%.

### Nivel 2 — los agentes (comportamiento)

- **Prestigio**: ¿las palabras de tier 1 se propagan más? Hoy no está medido.
- **Adopción**: quién adopta de quién → un grafo, no una cuenta.
- **Los mudos**: 19 de 60 agentes nunca hablaron en ningún run. Eso es diseño,
  no accidente, y hay que decidirlo.
- ⚠️ **Todo esto exige controlar la longitud del prompt.** Sin ese control,
  «el agente X lideró» puede ser «a X le escribimos más texto».

### Nivel 3 — la narrativa

- Arcos por agente (hoy: `agent_profiles.resumen_arco`, generado por LLM)
- Citas (405, curación sólida al 98,5%; sesgo leve hacia lo breve)
- Eventos del mundo y cómo respondieron
- 🆕 **La lectura del cronista**: el año contado desde dentro

---

## Lo que hay que construir, en orden

| # | Qué | Por qué ahora | Estado |
|---|---|---|---|
| 1 | `huella_de_base()` en cada run | sin esto nada es comparable | ✅ **hecho** |
| 2 | Métricas que discriminen | `pct_caquetio` no sirve | 🔴 [#69](https://github.com/miguelgilurbina/curiana-radio/issues/69) |
| 3 | Modo analítico del cronista | leer arcos desde dentro | 🟡 el prompt existe, falta cablearlo |
| 4 | Control de longitud de prompt | o igualar los prompts, o meterlo como covariable | 🔴 |
| 5 | 5 pares normal/ablación | tratar el run como unidad | 🔴 |
| 6 | Arreglar el exportador | [#42](https://github.com/miguelgilurbina/curiana-radio/issues/42) | 🔴 |

El **2** y el **4** son los que de verdad bloquean: mientras la métrica esté
saturada y el confusor sin controlar, correr más runs produce más datos que no
se pueden interpretar.

---

## La decisión que hay debajo de todo esto

Correr más runs **no es lo siguiente**. Lo siguiente es que un run sea legible.

Hoy hay 23 runs y 54.936 usos de palabra, y el análisis serio de anoche produjo
sobre todo hallazgos sobre **el instrumento**, no sobre la lengua: la métrica
está saturada, medio corpus estaba sin clasificar, el score mide en parte cuánto
escribimos nosotros. Eso no es un fracaso — es lo que pasa cuando por fin miras
los datos en serio— pero dice claramente dónde está el trabajo.

## Enlaces

[[ANALISIS_BASE_2026-08-06]] · [[cronista]] · [[DISENO_KOINE]] · [[04_protocolo_run_1_era_auditada]] · [[LINEA_DE_TIEMPO]] · [[mapa-motor]]
