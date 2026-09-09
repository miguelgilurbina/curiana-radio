# Decisión de modelo para la era 2: el habla que no se puede atestiguar

**Propuesta de Miguel, 2026-09-09:**

> «Para esta Era 2, como decisión de modelo, es poder enriquecer lo más posible
> palabras que no podemos atestiguar como caquetías pero que intuimos por
> coloquialidad o tradición oral, que es lo que representa el diccionario de
> Medina.»

Esto es una decisión, no una tarea: cambia qué entra al habla de los agentes y,
por tanto, qué mide el proyecto. Va al tablero con label `decision`.

---

## ⚠️ ACTUALIZACIÓN (2026-09-09, más tarde): la pregunta estaba mal planteada

Miguel propuso después que **la capa léxica sea un parámetro de cada run**. Eso
disuelve esta decisión: no hay que elegir de una vez si las voces intuidas
entran al habla — se corre un brazo con ellas y otro sin ellas, y se mide la
diferencia. Igual que `--ablacion` hace con el andamiaje de convergencia.

Ver `5-experimento/disenos/05_perfiles_de_run.md`. Las tres opciones de más
abajo siguen siendo el mapa de lo que está en juego, pero **ya no hay que
escoger una**: pasan a ser tres perfiles de run que se corren y se comparan.

Lo que sí sigue haciendo falta decidir es la **etiqueta**
(`caquetío-retroabstraido` como capa propia), porque sin ella no hay nada que
encender ni apagar por perfil.

---

## Lo que está en juego, medido

Las voces de nivel **B** (11) y **C** (33) del dictado suman **44**, de las
cuales **43 son nuevas** para el lexicón. Y caen justo donde el proyecto
declara sus huecos:

| Campo | Voces |
|---|---|
| flora (con medicinal, fruto, agua) | **20** |
| fauna (con mar) | **13** |
| casa, oficio, comida | **8** |
| creencia, cuerpo | 2 |

Contra las 301 entradas caquetías actuales, eso es un **+14%**, concentrado en
flora, fauna y oficio doméstico — que es exactamente el punto ciego que la
memoria del proyecto le atribuía a Medina desde el principio: *«vocabulario del
oficio diario que los cronistas no anotaron»*.

Hoy el habla se reparte así:

| Etiqueta | n |
|---|---|
| `caquetío-atestiguado` | 224 |
| `caquetío-reconstruido` | 68 |
| `caquetío` (a secas) | 6 |
| `caquetío-hipotético` | 2 |

---

## El mecanismo ya existe, y hay precedente

**D10 (2026-08-03) ya resolvió el caso general.** `normalize_source_language()`
manda `caquetío-hipotético` a la categoría `caquetío`, y lo documenta con esta
razón:

> *«la LENGUA no se discute, solo baja la confianza de la entrada — por eso
> comparte categoría con el resto del caquetío y no puntúa peor»*

O sea: el proyecto ya decidió una vez que una entrada puede estar **en boca de
los agentes con la confianza rebajada, sin ser castigada por el score**. Lo que
Miguel propone es aplicar esa misma lógica a un material nuevo.

Y el protocolo del dictado **lo previó**: su §5 dice que el nivel B va al corpus
y al lexicón activo no *«salvo decisión explícita»*. Esta sería esa decisión.

---

## La distinción que yo no perdería

Propongo **no** reutilizar `caquetío-hipotético`, sino abrir
**`caquetío-retroabstraido`**, porque son dos cosas distintas y la diferencia es
justamente lo que hace valioso a Medina:

| Etiqueta | Qué es incierto | Ejemplo |
|---|---|---|
| `caquetío-reconstruido` | nada de la forma: se derivó por regla desde una lengua hermana | `*cati` desde el lokono `katsi` |
| `caquetío-hipotético` | **la forma misma** — se propuso, no se documentó | las 441 aisladas |
| **`caquetío-retroabstraido`** | **no la forma, sino el sustrato**: la palabra existe y está documentada en boca viva; lo que no sabemos es si el sustrato es caquetío | `curubo`, `gualamo`, `totocoro` |

`retro-abstraido` no es un invento mío: es la marca que el propio protocolo
define para la criba de Miguel. Colapsarla dentro de `hipotético` borraría la
diferencia entre *«nos lo inventamos»* y *«lo dice un paraguanero de ochenta
años»*, que no es poca.

---

## 🔴 La trampa que NO aplica aquí, y conviene decirlo

El reflejo del proyecto ante «meter formas no verificadas» son **las 441
hipotéticas**, con su ~80% de fallo. Ese reflejo es sano, y aquí **no aplica**:

- Las 441 eran **transducidas**: formas fabricadas por máquina aplicando reglas.
  Su modo de fallo era *la forma no existe*.
- Estas 43 son **palabras reales en bocas reales**, con página y glosa textual.
  Su modo de fallo es otro: *el sustrato podría ser castellano, caribe o
  papiamento en vez de caquetío* — y para eso están los seis filtros de descarte,
  que ya se les aplicaron (por eso son B y C y no D).

Son riesgos distintos. Aplicar la lección de las 441 a este material sería usar
la vara equivocada.

---

## Lo que cuesta

1. **La comparabilidad con los runs publicados se rompe.** `score_linguistico()`
   contará estas 43 como caquetío, así que la densidad y las métricas de koiné
   de la era 2 no serán comparables con las de la era 1. Si la era 2 arranca
   como línea base nueva —y el protocolo del run 1 auditado dice que sí—, el
   coste es bajo. Si se quiere comparar, hay que correr también el brazo sin
   ellas.
2. **El diccionario público las mostrará.** Necesita que la etiqueta se vea en
   `/kaketiana`, no que se diluya en «caquetío».
3. **Riesgo de deriva de etiqueta**: que dentro de seis meses alguien las lea
   como atestiguadas. Se ataja con un test que fije el censo por etiqueta.

## Lo que compra

1. **43 palabras de flora, fauna y oficio** — el vocabulario del día a día, que
   es lo que un agente necesita para hablar de pescar, sembrar y cocinar sin
   caer al castellano.
2. **Coherencia con la tesis del proyecto.** Si la hipótesis es que el habla
   paraguanera conserva sustrato, meter ese sustrato en boca de los agentes es
   *poner la hipótesis a rodar*, que es para lo que existe la simulación.
3. **Un eje nuevo que medir**: si las voces retro-abstraídas se contagian y
   sobreviven igual que las atestiguadas, o si los agentes las rechazan. Eso es
   un resultado, no un supuesto.

---

## Las tres opciones

**A — Entran todas (B y C) como `caquetío-retroabstraido`.**
Es lo que la propuesta pide en su forma más plena. 43 voces.

**B — Entran solo las B (11), y las C esperan tu revisión una a una.**
Miguel ya dijo que va a revisar las C buscando la coloquialidad en internet. Esta
opción respeta ese trabajo: lo que su revisión suba, entra después.
*Es la que yo recomendaría*, porque no cuesta nada esperar y su revisión puede
mover voces de C a B con evidencia nueva.

**C — No entran al habla; van solo al corpus cultural.**
Lo que dice el protocolo hoy. Conserva la pureza de la métrica y deja el
vocabulario del oficio fuera de la boca de los agentes.

---

## Si se aprueba, qué hay que tocar

1. `normalize_source_language()`: mapear `caquetío-retroabstraido` → `caquetío`,
   con su razón escrita al lado como hizo D10.
2. `aplicar_medina.py`: una función que suba el nivel elegido con la etiqueta,
   idempotente y con `--dry-run`.
3. Un test que fije el censo por etiqueta, para que la deriva no pase callada.
4. La nota de `2-lengua/lexicon.md` y el diccionario público, para que la
   etiqueta se vea.
5. Declarar en `BITACORA_RUNS.md` que la era 2 arranca con línea base nueva.
