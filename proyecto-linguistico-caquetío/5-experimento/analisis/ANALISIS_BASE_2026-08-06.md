---
tipo: analisis
ambito: los 23 runs almacenados en la base local
herramienta: curiana_sim/analizar_runs.py
medido: 2026-08-06
base: supabase local (docker), 54.936 usos de palabra
---

# Análisis de la base — 2026-08-06

> Todo lo de abajo es **reproducible**: `python curiana_sim/analizar_runs.py --todo`.
> Si una cifra parece rara, se vuelve a medir en vez de discutirla.

## El inventario

23 runs, del 2026-06-21 al 2026-07-06. Solo cuatro pasan de 30 turnos:

| Run | Turnos | Ablación | Para qué sirve |
|---|---|---|---|
| `038d7b9d` | 60 | **no** | brazo normal del experimento de koiné |
| `bdc54134` | 60 | **sí** | brazo de control |
| `9bb920eb` | 60 | (pre) | anterior a la ablación |
| `20091e1f` | 0 turnos / 290 respuestas | (pre) | el run con el bug del exportador (#42) |

1.773 respuestas · 54.936 usos de palabra · 357 neologismos · 405 citas · 82 perfiles.

---

## 1. La koiné: la señal está, la prueba no

Contraste pareado por día entre los dos brazos de 60 turnos.

| Lectura | Normal | Ablación | Δ | p (t pareada) | d de Cohen | Días que gana el normal |
|---|---|---|---|---|---|---|
| acumulada | 0.4312 | 0.4527 | +0.0214 | 3.5e-05 | 0.89 | 26/30 |
| ventana | 0.4500 | 0.4791 | +0.0290 | 3.1e-04 | 0.75 | 22/30 |
| **emergente** | **0.5819** | **0.6571** | **+0.0752** | **7.7e-11** | **1.81** | **29/30** |

**El brazo normal converge más que la ablación en las tres lecturas**, y la
diferencia crece justo en la lectura más exigente. No es un empate con medias
distintas: es sistemático día a día.

### Tres reservas que hay que decir en voz alta

1. **n = 1 run por brazo.** Los 30 días son pseudo-réplicas —comparten agentes,
   semilla y trayectoria—, así que no son independientes. Los p-valores
   contestan *"¿difieren estas dos series?"*, no *"¿difieren estas dos
   condiciones?"*. Para lo segundo hay que repetir el par de runs y tratar el
   **run** como unidad. Con lo que hay: señal fuerte, no prueba.
2. **La brecha no crece.** En las tres lecturas la tendencia es plana o
   levemente decreciente. El mecanismo produce un desplazamiento **inmediato y
   sostenido**, no un efecto acumulativo. Si la hipótesis era *"la koiné se va
   formando"*, el dato dice más bien *"el contagio fija una diferencia desde el
   principio y la mantiene"*. Es un resultado distinto, y más modesto.
3. **30 días simulados** es una prueba del mecanismo, no del fenómeno histórico.

---

## 2. 🔴 El hallazgo que obliga a releer todo lo demás

**La longitud del `system_prompt` de un agente predice —negativamente— su score
lingüístico.**

```
largo del prompt  vs  score:   r = −0.481   p = 0.0046   (n = 33 agentes)
                               ρ = −0.480   p = 0.0047   (Spearman, robusto)
```

| Agente | Prompt | Score | | Agente | Prompt | Score |
|---|---|---|---|---|---|---|
| Manaure | 834 car. | **6.94** | | Pari-nu | 161 car. | **8.54** |
| Shaboro | 747 | 7.04 | | Chiri-ko | 155 | 7.48 |
| Watapana | 700 | 7.07 | | Piri-sha | 150 | 7.60 |

**Cuanto más caracterizado está un personaje, peor habla caquetío.** Manaure, el
diao, el centro narrativo del proyecto, tiene el prompt más largo y **el peor
score de todos**.

### Por qué esto es grave

Cualquier lectura del tipo *"el agente X lideró / se resistió a la
convergencia"* puede ser, en realidad, *"al agente X le escribimos un prompt más
largo"*. Es un **confusor que atraviesa todo el dataset** y que hasta ahora
nadie había controlado.

No es una ley sociolingüística descubierta: es una propiedad de cómo está
escrito el elenco. Pero está ahí, es medible, y **hay que controlarla en
cualquier análisis por agente que se haga a partir de ahora**.

### El corolario de género, que es el mismo hallazgo con otra cara

El campo `etnia` distingue `caquetío` (23 agentes, todos M) de `caquetía` (15,
todas F) — no son dos pueblos, es concordancia de género. Y sus métricas
difieren de verdad:

| | Score | pct_caquetío |
|---|---|---|
| Femenino (15 agentes) | 7.530 | 0.9579 |
| Masculino (17 agentes) | 7.222 | 0.9105 |
| | MW p=0.010, d=0.75 | MW p=0.041, d=0.65 |

Se mantiene dentro de cada tier, así que no es confusión de tier. **Pero los
prompts masculinos son más largos** (365 car. de media frente a 289), porque los
protagonistas son hombres. Lo más probable es que el "efecto de género" **sea el
efecto de longitud de prompt** visto por otro lado.

> ⚠️ Si alguien reporta *"las mujeres lideraron la koineización"*, estará
> reportando un artefacto de autoría. Queda escrito aquí para que no pase.

---

## 3. 🔴 La mitad del corpus estaba sin clasificar — corregido

`word_uses.source_language` venía **NULL en 27.641 de 54.936 usos (50,3%)**, y
el **100%** de esos eran formas morfológicamente complejas:

| Tipo | Usos | Formas |
|---|---|---|
| con sufijo de aspecto (`-ka`/`-ni`/`-da`) | 18.752 | 220 |
| otros compuestos con guion | 5.049 | 641 |
| con prefijo posesivo (`ta-`/`pi-`/`nü-`) | 3.840 | 155 |
| **formas simples** | **0** | **0** |

O sea: **justo los usos que prueban que los agentes manejan la morfología** eran
los que se perdían.

**Causa**: había dos caminos de reconocimiento que no se hablaban.
`score_linguistico()` usa `_familia_de_token()`, que deshace prefijos y sufijos;
`word_source_language()` —el que persiste— hacía un lookup pelado contra
`VOCABULARIO_BASE`. El motor reconocía la palabra para puntuar y la perdía al
guardarla.

**Arreglado** (`word_source_language` delega en `_familia_de_token`) y los 23
runs históricos **rellenados** con `backfill_word_uses.py`: 1016 formas
resueltas, 0 filas sin lengua. Verificado que ninguna de las 1413 entradas del
lexicón cambia de lengua al pasar por la función nueva.

---

## 4. `pct_caquetio` está saturada — confirmado con dato

Distribución de `pct_caquetio` en los dos runs de 60 turnos:

```
 80- 90%     4    0.7%
 90-100%    48    8.1%  ████
100-110%   542   91.2%  █████████████████████████████████████████████
```

**El 91% de las respuestas está en 1.0.** Desviación típica: 0.0277 (normal) y
0.0129 (ablación). La métrica **no distingue nada** — es el issue #69, ahora con
la medición delante.

Consecuencia práctica: el análisis de arriba usa **`score`**, no `pct_caquetio`.
Se nota en que la correlación con la longitud del prompt es robusta en score
(Spearman −0.48) y ruido en pct_caquetío (Spearman +0.01): en una variable
saturada, Pearson lo mueven cuatro outliers.

---

## 5. El léxico que emergió

**Concentración fuerte**: 25 formas concentran el **50%** de los 54.936 usos;
10 formas, el 26%. Es una distribución muy zipfiana, más de lo que cabría
esperar con un lexicón de 1413 palabras disponibles.

Las más usadas son el andamiaje gramatical, no el vocabulario cultural: `taya`
(yo), `wara`, `kashi`, `ta-barsure` (mi alma), `mara`, `naba-ni`, `wana-ka`,
`nüma` (él/ella). **Los agentes consolidaron una gramática antes que un mundo.**

Reparto por lengua tras el arreglo: el caquetío domina de forma abrumadora, y
las hermanas vivas quedan en trazas (lokono 1,2%, wayunaiki 1,1%, taíno 0,3%).
El objetivo del proyecto —que el caquetío domine— **está cumplido con holgura**;
tanta, que ya no queda margen para medir mejora. Ver §4.

---

## 6. Agentes

- **El tier 2 puntúa más alto que el tier 1** (7.55 vs 7.20) y habla más
  caquetío (0.974 vs 0.926). La élite habla peor: es el efecto de longitud de
  prompt otra vez, porque los tier 1 son los más caracterizados.
- **41 de 60 agentes** llegaron a hablar en algún run. 19 nunca aparecieron.
- **Corie-ko** es el más activo (132 respuestas) y el más prolífico en
  neologismos (37).
- Los perfiles curados sí producen roles ricos y distintos ("Tejedora silenciosa
  de deudas y favores; verdadera administradora de recursos y árbitro moral del
  cacicazgo matrilineal").

---

## 7. Narrativa

405 citas curadas, y la curación es **sólida al 98,5%**. Las citas buenas
exhiben morfología compuesta real:

> «Kali-bana-chaa ta-barsure—masa-bana-sha: masa+-bana+-sha wana-da wara
> pana-dusha kashi.» — Guaranaro-sha, día 14

Pero hay un sesgo pequeño y detectable: **6 citas degeneradas** (muy cortas o
sin morfología) puntúan **por encima** de la media (9.07 vs 8.43). El caso
extremo es la cita de mayor impacto de toda la base:

> **«Ríe.»** — Paugis-sha, día 28 · impacto 9.8

Una acotación escénica en español, puntuada como el momento más impactante del
corpus. No es sistémico —1,5%—, pero el curador premia lo breve y contundente
sin comprobar que sea lengua.

---

## Qué hacer con esto

| # | Qué | Dónde |
|---|---|---|
| 1 | Controlar la longitud del prompt en todo análisis por agente | este documento §2 |
| 2 | Rehacer las métricas: `pct_caquetio` saturada | issue #69 |
| 3 | Repetir el par normal/ablación varias veces para tratar el run como unidad | §1 |
| 4 | Normalizar el campo `etnia` (género ≠ etnia) | higiene, ya detectado |
| 5 | Que el curador de citas exija un mínimo de lengua | §7 |
| 6 | Igualar la longitud de los prompts, o medir controlando por ella | §2 |

## Enlaces

[[mapa-motor]] · [[DISENO_KOINE]] · [[BITACORA_RUNS]] · [[01_que_probaron_los_seis_runs]]
