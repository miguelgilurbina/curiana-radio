# «Golfete» en Paraguaná: por dónde entra, a quién le sobra y qué decidir

**Deuda del día 1 limpio de la serie B** (run `3973d317`, 2026-09-17). El
Director cerró el día con:

> «Mañana el juri seguirá fuerte desde el este, **las canoas volverán al
> Golfete**, y habrá que ver si la sal y el casabe sostienen la calma.»

y 2 de 72 respuestas de agentes dijeron «Golfete».

**Ninguna cifra de este borrador está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/medir_golfete_era2.py --run 3973d317
```

(el ensayo en seco no llama a la API; `--base` y `--run` consultan el Supabase
local por `docker exec`).

---

## 0. Antes de nada: la premisa del encargo era falsa

El encargo decía que los dos nodos de la era 2 están en la costa **oeste**,
sobre el Golfo de Venezuela, y que el Golfete es la otra costa. **El canon dice
otra cosa**, y es lo primero que hay que fijar porque cambia la respuesta a las
tres preguntas.

| nodo | sitio | zona | `en_una_frase` (sitios_era2.yaml) |
|---|---|---|---|
| **GUARANAO** | Tacuato | ZG2 | «la aldea de la orilla **del Golfete** que mira a Coro» |
| **GUARANAO** | El Cayude | ZG2 | «la otra aldea **del Golfete**, al oeste de los Tacuatos» |
| GUARANAO | Moruy | — | «la casa del Manaure al pie del Capubana… el único sitio sin playa» |
| GUARANAO | Capubana | — | «el centro compartido… la marca que se ve desde el mar» |
| **AMUAY** | Carirubana | ZA1 | «la playa de pescadores del extremo sur de **la costa oeste**» |
| **AMUAY** | Caseto | ZA1 | «la aldea del interior de AMUAY, a la sombra oeste del cerro» |
| *(de fondo)* | laguna de Guaranao | ZG1 | «la salina en la boca de una quebrada, y la ensenada» |

Y las zonas, tal como las nombra el prompt (`ZONAS_DE_PESCA`, resueltas desde
`elenco_era2.yaml`):

- `ZG2` = **«la orilla del Golfete»** — de Matacán a Tacuato y el Bajo de Supí
- `ZA1` = **«la costa oeste, de Punta Cardón a Los Taques»**

> **El Golfete es la orilla de GUARANAO.** No es un residuo de la era 1, no es
> un marco fuera de sitio y no es de toda Paraguaná: es el agua de dos de los
> siete sitios y de 25 de los 63 agentes. Lo que NO es del Golfete es AMUAY.

El nombre del nodo despista —la ensenada y la laguna de Guaranao están en la
costa oeste, a 3 km de Carirubana— pero el reparto de sitios es el de la
decisión del 2026-09-14 y ya está declarado: `sitios_era2.yaml` §meta anota
además que Oliver reparte los clanes **al revés** («the Amuayes… southern part
and the Guaranaos… northern part», DOC 264) y que la decisión lo ignora *por
decisión, no por descuido* (deuda #122, la frase cardinal).

---

## 1. Por dónde entra: las siete vías, medidas

Ensayo en seco, sin API. `Golfete` / `Golfo (no -te)` / `costa oeste`:

| # | vía | textos | «Golfete» | ¿le sobra a alguien? |
|---|---|---:|---:|---|
| 1 | `estado_inicial('PARAGUANÁ').evento_del_turno` (el evento semilla) | 1 | 1 | **no** — nombra las dos aguas, una por nodo |
| 2 | `bloque_tu_tierra` — 126 combinaciones | 126 | 41 | **sí**, 7 de las 41 |
| 3 | `resumen_del_mundo` — `[El mundo]`, 18 combinaciones | 18 | 1 | **sí**, esa 1 |
| 4 | `catalogo_para_elenco('era2')` — 24 eventos | 24 | 2 | a revisar (`expedicion_perlas`, `vigilancia_perimetro_amanecer`) |
| 5 | ficha del agente (`system_prompt`, módulo generado) | 63 | 19 | **no** — 14 GUARANAO + 5 cruzados *a propósito* |
| 6 | `prompt_gente()` — `[Tu gente]` | 63 | 25 | **no** — son exactamente los 25 de ZG2 |
| 7 | `decir_para_el_mundo()` — el traductor del mundo | — | 0 filtrados | **no filtra** (ver §4c) |

### 1.1 El evento semilla NO es la fuga

El encargo lo señalaba como sospechoso. Medido, es **el texto que mejor hace la
geografía de todo el motor**: da a cada nodo su agua.

> «En **Tacuato, a la orilla del Golfete**, y en **Carirubana, la playa de
> pescadores de la costa del oeste**, se botan las canoas antes de que el
> alisio monte…»

Y en este run ni siquiera llegó a nadie: `run_turn` llama a
`director_select_event()` **antes** de armar el estímulo, y el turno 1 sacó
evento («El buko baja. Los conucos se resienten»), que sobrescribió la semilla.
*(Con la probabilidad del turno 1 —0,3— la semilla sobrevive 7 de cada 10
días; aquí cayó el 3.)*

### 1.2 La fuga estructural: **la frase de la TARDE del Tiempo de Viento**

`clima_era2.yaml`, `frases_del_cargador.viento.momentos.tarde`:

> «El viento arrecia y **el Golfete** se pone difícil: la canoa vuelve.»

Esa frase entra en `[Tu tierra]` de **los siete sitios** (7/7 en viento/tarde)
y en `[El mundo]` del Director. Es la única de las 18 frases de momento que
nombra un lugar, y es la única combinación de `[El mundo]` con la palabra.

El reparto de las 41 combinaciones de `[Tu tierra]` con «Golfete» lo deja claro:

| sitio | nodo | combinaciones con «Golfete» |
|---|---|---|
| Tacuato | GUARANAO | **18/18** ← su agua, en todas |
| El Cayude | GUARANAO | **18/18** ← su agua, en todas |
| Moruy · Capubana · laguna | GUARANAO / — | 1/18 cada uno ← **sólo** viento/tarde |
| Caseto · Carirubana | AMUAY | 1/18 cada uno ← **sólo** viento/tarde |

Y su origen agrava el caso: la frase viene de `periodos[P1].el_dia.tarde`, que
cita `ecologia-026` (Camacho 2011) — «las corrientes las gobiernan la marea y,
sobre todo, la acción tangencial del viento del este, que arrecia en el curso
del día y empuja las corrientes hasta cerca de 1 m/s **por la tarde**». Esa
medición es **del Golfete de Coro** y de ningún otro sitio. Decírsela a
Carirubana es proyectar la hidrodinámica de una laguna costera somera sobre
mar abierto del Golfo de Venezuela, donde el corpus no tiene ni un hecho
(`sitios_era2.yaml`: «La costa oeste (Caseto, Carirubana) no tiene ni un hecho
del corpus»).

### 1.3 En el run 3973d317, pieza a pieza

Reconstruidas las piezas deterministas del prompt de las 72 respuestas:

```
42/72  [Tu tierra]              30/72  [Tu gente]        23/72  la ficha
47/72  por alguna vía  —  GUARANAO 34, AMUAY 13
```

De los 42 de `[Tu tierra]`, **12 son de sitios que no tienen esa agua** y los
12 caen en el **turno 4 (tarde)**: Caseto 8, Moruy 3, Carirubana 1. El turno de
la tarde no tuvo ni un agente de Tacuato o El Cayude: a los 12 que hablaron se
les dijo que su agua era el Golfete, y a ninguno de los que la tienen.

Y el Director vio `[El mundo]` con «Golfete» en **1 de los 6 turnos**, el 4.
Su cierre del día («las canoas volverán al Golfete») es esa frase devuelta:
la reflexión del día lee los seis cierres del día, y el del turno 4 es el que
llevaba la palabra.

---

## 2. Qué dice el canon de la costa de cada nodo

- **`sitios_era2.yaml`** — ya citado arriba. Guaranao (la laguna) es **sal y
  ensenada**: la salina en la boca de una quebrada, `ZG1`, «de fondo». El
  manglar y el caimán se degradaron a no proyectables (Aular Leal 2014: la
  laguna nace en 1985).
- **`4-fuentes/arcaya-1920.md`, p. 22** — las salinas de Guaranao son «las más
  importantes» de Paraguaná, y en la misma página: «Ningún río, ni siquiera un
  arroyo, riega a Paraguaná» y «apenas una fuente intermitente en el cerro de
  Santa Ana». Arcaya p. 20 es el que da el Golfete como somero y «sólo
  navegable en pequeñas embarcaciones y por prácticos».
- **`3-mundo/corpus/ecologia.yaml`**:
  - `ecologia-026` — el **Golfete de Coro**: laguna costera somera, marea
    semidiurna de ~50 cm, corrientes que arrecian por la tarde. *(La fuente de
    la frase de la tarde.)*
  - `ecologia-015` — la ictiofauna «de las aguas someras y los manglares **del
    Golfete**».
  - `ecologia-007` — cauces efímeros; el Mitare es «el principal de la vertiente
    del **Golfo de Venezuela**». Es el único hecho que nombra el golfo.
  - `ecologia-018` / `ecologia-032` — cardonal, sin ríos ni ceibas (ya en las
    restricciones del Director).
  - `ecologia-077…084` (la tanda del 09-15, decisión p4): el matacán (077), los
    jachos (078), el buco (079), **las atalayas de cardúmenes de la costa
    oeste** (080: Sarabón y Suriquiba, «a menos de 10 km de Carirubana» — «el
    dato de oficio mejor localizado de toda la costa oeste»), la cal de concha
    (081), la aridez (082), el pulso de Sievers (083) y la laguna de hoy (084).
- **¿Dice el mundo en qué agua pescan los nodos?** **Sí, y sólo por una vía:**
  `[Tu gente]` («tu gente pesca en la orilla del Golfete» / «…en la costa
  oeste, de Punta Cardón a Los Taques»), que reciben los 49 agentes con zona.
  Los 14 sin zona (Moruy y el Capubana) no reciben ninguna agua — y son los que
  la frase de la tarde arrastra al Golfete.

---

## 3. Lo que ya se hizo (instrumento, en esta rama)

Una restricción más del Director, leída del corpus por id, con el mismo
contrato que las dos que ya había (si un id falta, la línea no se dice):

```
son dos aguas y no una: la orilla del este, con su marea, y la costa oeste
de Punta Cardón            ← ecologia-026 · ecologia-080
```

`[El mundo]` pasa de 247 a 339 caracteres como máximo (tope 400). **La línea no
nombra el Golfete a propósito**: la restricción va en las 18 combinaciones y
nombrarla ahí multiplicaría por nueve la exposición del Director a la palabra
que sobra. `tests/test_director.py` lo vigila.

Esto no arregla la frase de la tarde: sólo le dice al Director que hay otra
agua. Lo que sigue **lo decide Miguel**.

---

## 4. Las tres decisiones

### (a) La frase del período P1 — ¿se cambia?

No hay que tocar el evento semilla (§1.1). Lo que hay que decidir es **la frase
de la tarde** (`clima_era2.yaml`, `frases_del_cargador.viento.momentos.tarde`;
presupuesto ≤ 90 caracteres).

| | propuesta | qué la sostiene | coste |
|---|---|---|---|
| **A1** *(neutra)* | «El viento arrecia y **el agua** se pone difícil: la canoa vuelve.» (60) | `ecologia-026` para el Golfete y `ecologia-005`/`020` (alisio ENE los doce meses, arrecia en la seca) para la otra orilla; la generalización es canon-simulación y se declara | ninguno: cambio de una línea de YAML |
| **A2** *(por zona)* ⭐ | «El viento arrecia y **{tu agua}** se pone difícil: la canoa vuelve.» con `ZG2 → el Golfete`, `ZA1 → la costa del oeste`, sin zona `→ el agua` | lo mismo, y además `ZONAS_DE_PESCA` ya resuelve ese mapa; cada agente oye su propia orilla | un marcador `{tu agua}` en `bloque_tu_tierra`, resuelto desde `sitios()[sitio]['zona_de_pesca']` (≈15 líneas y un test) |
| A3 | dejarla y confiar en que la primera línea de `[Tu tierra]` («Carirubana, la playa… de la costa oeste») corrija | — | ninguno; es lo que ya pasa, y no bastó |

**Recomiendo A2**, y A1 si se quiere cero código. Razón: A2 no es sólo
higiene geográfica — es exactamente el eje del experimento. La koiné se mide
por la distancia entre los dos nodos; si el prompt les da el mismo referente de
agua, el instrumento borra la diferencia que quiere medir. Con A2, «el agua que
se pone difícil por la tarde» es un referente DISTINTO en cada nodo, y las
formas que acuñen para él son comparables.

> Nota de redacción: la frase de la tarde no es una decisión de Miguel, es
> redacción del escriba del 2026-09-16 (`frases_del_cargador` se declara
> «REDACCIÓN de canon-simulación»). Se deja sin tocar igualmente porque cambia
> lo que el agente VE a mitad de la serie B, y eso sí es decisión de serie.

### (b) `[El mundo]` del Director — ¿debe decir qué nodo mira a qué agua?

**No como decía el encargo** («los dos nodos miran al oeste»): sería falso.
Las opciones reales, sobre la línea que ya entró en §3:

| | propuesta | largo | `[El mundo]` máx (tope 400) |
|---|---|---:|---:|
| **B1** *(lo que hay)* | «son dos aguas y no una: la orilla del este, con su marea, y la costa oeste de Punta Cardón» | 90 | **339** |
| **B2** ⭐ | «GUARANAO pesca el Golfete, al este del cerro; AMUAY la costa oeste, de Punta Cardón a Los Taques» | 96 | **345** |
| B3 | B2 + «; el Golfete queda al otro lado de la península» | 143 | **392** |

**Recomiendo B2.** Es el mapa que el Director necesita para no hablar de «las
canoas» en singular, y sale del canon de la era 2 (`sitios_era2.yaml`
`zona_de_pesca` + `ZONAS_DE_PESCA`), no de `ecologia.yaml`: por eso no lo puse
ya — nombrar los nodos saca la línea del contrato «sólo lo que el corpus
sostiene por id» y hay que declarar la fuente nueva. B3 deja `[El mundo]` a 8
caracteres del tope, y `resumen_del_mundo` **descarta la línea entera** si no
cabe: la primera frase de momento que crezca deja al Director sin
restricciones, incluidas las del cardonal. No lo recomiendo.

### (c) `decir_para_el_mundo` — ¿debe reescribir «Golfete»? → **NO**

Y es un no rotundo, por cinco razones medidas:

1. **Es canon y es cierto.** El Golfete es el agua de 2 de los 7 sitios, de la
   zona ZG2 y de 25 de los 63 agentes. `MARCOS_FUERA_ERA2` filtra lo que este
   mundo **no tiene** (guaycaríes, jirajaras, gayones, la Curiana como lugar).
   El Golfete lo tiene.
2. **El filtro es destructivo.** `texto_para_elenco()` no reescribe: tira la
   **frase entera** que lleva un marco prohibido. Meter «Golfete» ahí borraría
   del cierre del Director y de sus notas toda frase sobre la orilla de
   GUARANAO — 25 agentes se quedarían sin su propia agua en la crónica.
3. **La palabra no es el error; el destinatario sí.** De las 13 respuestas con
   «Golfete» en los siete runs de la era 2: 9 de agentes de Tacuato o El Cayude
   (su agua), 1 de Moruy (su nodo), 1 de Ebokoa —cuya ficha dice «te criaste a
   la orilla del Golfete y hoy pescas mar grueso en la costa del oeste»— y 1 de
   Bajari, el corredor «que cruza a GUARANAO varias veces al año». **Queda una
   sola indefendible: Turicha**, cantor de Caseto, en el turno de la tarde del
   día 1 de la era 2. Un filtro global mataría 12 usos correctos para corregir 1.
4. **Cinco fichas lo dicen a propósito.** Los 5 agentes de AMUAY cuyo
   `system_prompt` nombra el Golfete son los cruzados (Kasebo, Dipopo, Ebokoa,
   Mene, Tigi): «Tú te criaste pescando el Golfete y **lo dices demasiado**»;
   «sus tres hijos han crecido **oyendo dos nombres para cada pez**»; «ha
   tenido que aprender nombres nuevos para árboles que aquí no crecen y **sigue
   usando los suyos cuando nadie escucha**». Ese es **el canal de contacto
   entre nodos** que el diseño de la koiné puso ahí. Filtrar la palabra
   apagaría el experimento.
5. **Haría invisible la medición.** Que un agente de AMUAY diga «Golfete» es
   precisamente el dato: o viene de allá (y entonces es difusión, que es lo que
   queremos ver) o se lo dijo el prompt (y entonces es un bug del instrumento,
   que es lo que acabamos de encontrar). Con un filtro en medio, las dos cosas
   se ven igual: silencio.

---

## 5. Deuda que queda abierta

- **Los dos eventos del catálogo** (`expedicion_perlas`: «los buceadores se
  internan en el Golfete»; `vigilancia_perimetro_amanecer`: «Dara-bana ya
  escruta el horizonte del Golfete»). Están escritos para la Curiana, que sí
  estaba en el Golfete. Con el elenco de la era 2 le llegan a todo el mundo.
  `REESCRITURAS_ERA2` es exactamente el lugar donde se arreglan, y es una tabla
  de redacción declarada: dos entradas más, si Miguel quiere.
- **Los 14 agentes sin zona de pesca** (Moruy y el Capubana) no reciben ninguna
  agua en `[Tu gente]`. Son los que la frase de la tarde arrastra. Con A2
  oirían «el agua», que es lo correcto para quien no tiene playa.
- **La deuda #122** (la frase cardinal de Oliver: reparte los clanes al revés
  que el canon de la era 2) sigue abierta y es la raíz de que «GUARANAO» sea el
  nodo del Golfete y no el de la ensenada que lleva su nombre.
- **El run `3973d317` no es comparable a uno posterior a estos cambios.** Si
  algo de §4 se aplica, la serie B arranca de nuevo o se declara el corte.
