# Existir en el mundo: la escena por lugar

**Para que Miguel decida.** Esto es un diseño y una medición. **No se
implementó nada**: el motor no se toca en esta tarea. Lo único que se escribe
es la tabla propuesta (`6-fusion/escena_por_lugar_propuesta_2026-09-17.yaml`)
y los dos scripts que la derivan y la miden.

> Continúa `6-fusion/issues-pendientes/frontera-entre-nodos-2026-09-17.md`, que
> midió que el motor **no tiene frontera en el prompt** y propuso tres diseños.
> Miguel eligió el A y lo reformuló: el ámbito no es el nodo, **es el lugar
> donde el agente está hoy**, y dónde está lo deciden su oficio y la hora.

Toda cifra de este borrador la imprimen dos scripts:

```bash
python 6-fusion/scripts/derivar_escena_por_lugar.py --motor   # la tabla y lo que sale de ella
python 6-fusion/scripts/derivar_escena_por_lugar.py --yaml    # + reescribe la propuesta
python 6-fusion/scripts/medir_presupuesto_escena.py           # lo que cuesta en el prompt
```

Ninguno llama a la API ni lee `curiana_sim/.env`. El segundo evita a propósito
importar `curiana_orchestrator_v2` —importarlo arrastra `curiana_database` y su
`load_dotenv()`— y saca del fichero con `ast` las dos constantes que necesita.

---

## 0. Qué pidió Miguel

> «Sí o sí es importante que podamos establecer una forma de poder hacer que
> estos nodos interactúen entre sí pero que además puedan tener su desarrollo
> propio y así luego veremos competiciones de conceptos entre nodos. El mundo
> más allá de un lugar debería poderse "recorrer" según la potestad del
> agente.»

> «Si no se mueven, ¿cómo podemos hacer que hagan cosas y "existan" en el mundo
> que les describimos?»

**La lectura operativa, en tres líneas.**

1. El **ámbito** de lo que un agente ve deja de ser la comunidad entera y pasa
   a ser **el lugar donde está hoy**; dónde está lo deciden su oficio y la hora,
   y más adelante su potestad de moverse.
2. **Los nodos no se programan: salen del mapa.** Un lugar pertenece al nodo de
   quien lo trabaja; los lugares donde coinciden los dos son el contacto, y no
   hay que declarar ninguna frontera para que la haya.
3. **Existir es dejar rastro**: lo que un agente hizo, trajo y dio tiene que
   quedar en el estado y volver al mundo, o «moverse» es sólo una etiqueta más
   en el prompt.

---

## 1. Lo que hay hoy — medido, con fichero:línea

### 1.1 La ubicación existe, es fija, y nadie la mueve

| pieza | dónde | qué hace |
|---|---|---|
| `ubicacion_default` | `curiana_agents_era2.py` (63 fichas) | en la era 2 **es el sitio**: Tacuato, El Cayude, Moruy, Caseto, Carirubana y —uno solo— Capubana |
| `ubicaciones_override` | `curiana_state.py:176-177` | el campo pensado para moverlos |
| lectura en el prompt | `curiana_orchestrator_v2.py:355-357` → `:399` | `[Tu ubicación]: {ubicación}`, una línea |
| lectura social | `curiana_social.py:134` y `:149` | la co-ubicación de `vecinos()` |
| `agents_at_location` | `curiana_agents.py:619-620` | compara `ubicacion_default`, nada más |

Medido con `derivar_escena_por_lugar.py --motor`:

```
usos de `ubicaciones_override` fuera de tests: 4 (escrituras reales: 0)
```

**Cuatro lecturas y cero escrituras.** Nadie mueve a nadie: un agente nace en
su sitio y muere en su sitio. Esa es la respuesta literal a la pregunta de
Miguel — no es que se muevan poco, es que el campo que los movería no se
escribe nunca.

Y hay dos estructuras más que ya describen el día y **no las lee nadie**:

- `curiana_state.py:131-135` `LOCACIONES` — las trece locaciones de la era 1
  (`orilla`, `manglar`, `conuco`, `salinar`, `taller_canoas`, `buco`…). El
  orquestador la **importa** (`:55`) y no la usa: es un import muerto. Quien sí
  la usa es `compilar_corpus.py:647-649`, que valida contra ella el campo
  `locacion` del corpus.
- `curiana_state.py:138-145` `ACTIVIDADES_POR_MOMENTO` — «qué se hace en cada
  momento del día», escrito y **con una sola aparición en todo `curiana_sim/`:
  su propia definición**. El motor ya tenía la idea de esta tarea y nunca la
  enchufó.

> El corpus, en cambio, sí está indexado por locación: **56 de 157 hechos** de
> `ecologia` + `transmision` + `creencia` traen `locacion` (orilla 15, matorral
> 12, manglar 7, camino_islas 7, buco 4, salinar 3, bohíos 3, taller_canoas 3,
> conuco 2). Es el índice que a la capa 1 le hace falta y ya existe.

### 1.2 No hay bloque de oír

No existe ningún `[Lo que se dijo]`: un `grep` sobre `curiana_sim/*.py` no
encuentra ninguno (medido en la propuesta de la frontera §1.1). Un agente
**nunca lee la intervención de otro agente**. `AgentMemory`
(`curiana_orchestrator_v2.py:252-278`, se escribe en `:908` y `:1347-1351`)
guarda **sólo lo que dijo él mismo**, cinco notas rodantes.

### 1.3 Las cuatro vías por las que hoy cruza una forma — todas globales

De `frontera-entre-nodos-2026-09-17.md` §1.1, sin partición por nodo ni por
lugar:

| # | vía | dónde se arma | a quién |
|---|---|---|---|
| **V1** | `[Palabras propuestas en evaluación]` — las últimas **5 propuestas con el nombre de su autor** | `curiana_lexicon.py:7523-7532`, inyectada en `:8755-8756` | todo tier ≤ 2 |
| **V2** | `[Palabras nuevas de la comunidad]` — las últimas **15 adoptadas** (oficializa con 2 adoptantes cualesquiera, `:7307-7330`) | `curiana_lexicon.py:7512-7520` → `:8753-8754` | todos |
| **V3** | `[La comunidad aún busca nombre…]` — las formas rivales | `curiana_koine.py:1036-1048` → `orchestrator:418-421` | todos |
| **V4** | muestreo rich-get-richer ponderado por el `CampoLexico` | `curiana_koine.py:709-737`, alimentado en `orchestrator:805-807` | todos |

V1 es la que explicó los tres cruces de Δturnos = 0 del día 1 de la serie B: el
prompt leía en voz alta, con nombre y apellido, lo que el otro nodo acababa de
decir.

### 1.4 La ventana de 12 es un sorteo, no un canal

`_ventana` (`curiana_orchestrator_v2.py:630-640`) es una rotación determinista
sobre el roster con un contador **global** de turnos. Decide **quién habla**,
no quién oye. Un turno con evento mete primero a los agentes que el evento
nombra (`:659-672`) y completa con la rotación.

### 1.5 `hizo_hoy`: el único rastro que existe, y es local

`hizo_hoy` (`curiana_orchestrator_v2.py:1298`, se llena en `:1337-1339`) es una
**variable local de `auto_mode`**. Al cerrar el día se vuelca a la memoria de
cada agente como una nota (`:1347-1351`):

> `D3: hablé al amanecer, mediodia; acuñé biro-ana`

Y se vacía (`:1358`). No dice **dónde** estuvo, ni **qué hizo**, ni **qué
trajo**: dice a qué hora habló. No está en `ComunidadState`, así que
`--continuar` no lo hereda como estado (sólo sobrevive lo que ya pasó a
`AgentMemory`).

### 1.6 Qué narra el Director, y desde qué

`director_narrate` (`:475-522`) recibe: la línea de estado
(`state.to_context_string()`), `resumen_del_mundo(state)` (≤ 400 car.),
`[La gente que hay hoy]` con los nombres mezclados de los dos nodos
(`:501-504`), sus propias notas del día anterior (`:505-507`) y las
intervenciones recortadas a 100 caracteres (`:492-495`). Su texto va a
`state.cierres_del_dia` (`:521`) → `reflexion_del_dia`
(`curiana_director.py:97-150`) → `state.notas_orquestador` (`:1401`) → **vuelve
al Director**. Nunca llega al agente: `to_context_string`
(`curiana_state.py:294-306`) no incluye ni los cierres ni las notas.

**El Director narra desde lo que se DIJO, nunca desde lo que se HIZO** — porque
no hay nada hecho que narrar.

### 1.7 Qué guarda la base por respuesta

Consultado en el Postgres local (sólo lectura):

```
agent_responses: id, turn_id, run_id, agent_name, ethnicity, tier,
                 response_text, score, pct_caquetio, pct_wayunaiki, pct_lokono,
                 pct_taino, pct_proto_arahuaco, aspects_used, words_used,
                 neologisms_proposed, langsmith_trace_url, created_at
turns:           id, run_id, day, turn_num, moment, season, event_description,
                 created_at
```

**Ni `agent_responses` ni `turns` tienen columna de lugar.** Hoy el único modo
de saber dónde estaba alguien es mirar su `ubicacion_default` en el módulo
generado — y como no cambia nunca, es exacto y es inútil.

### 1.8 Lo que cuesta hoy el prompt

Medido con `medir_presupuesto_escena.py` (elenco `era2`, mundo PARAGUANÁ,
perfil `era2`, día 1 del viento):

| pieza | caracteres |
|---|---:|
| identidad lingüística (fija) | 1.250 |
| bloque de mundo `to_context_string` | 579 |
| ficha del agente (63) | media **515** (min 346 · max 678) |
| bloque léxico tier 1 / 2 / 3 | 7.438 · 3.328 · 2.221 |
| `[Tu tierra]` (1.134 combinaciones) | media **284** (tope 320; max medido 320) |
| **prompt entero tier 1** (17) | media **10.465** |
| **prompt entero tier 2** (36) | media **6.301** |
| **prompt entero tier 3** (10) | media **4.924** |
| **los 63** | media **7.206** (min 4.819 · max 10.769) |

⚠ El prompt creció mucho desde la medición del 2026-09-14 (media 4.142): entró
`[Tu tierra]` y creció el bloque léxico. Con **r = −0,48** entre longitud y
score, esto ya es la restricción de diseño más dura que tiene la era 2, y es la
razón de que cada bloque de abajo lleve tope.

---

## 2. Las cuatro capas de «existir»

Las cuatro son independientes y acumulativas. La 1 sola ya cambia el mundo; la
2 es el diseño A de la frontera con «lugar» en vez de «nodo»; la 3 es la que
hace que exista algo que narrar; la 4 es la que Miguel pidió con la palabra
*potestad*.

---

### Capa 1 — ESTAR: la escena por turno

**Qué es.** Cada turno, cada agente tiene un **lugar**, sacado de la tabla
`oficio × momento → lugar` (§3). El lugar no es un nombre nuevo: es
`sitio` × `locación`, y la locación es el vocabulario que el corpus ya usa.

**Qué cambia en el motor.**

- **Módulo nuevo `curiana_escena.py`**, hermano de `curiana_mundo.py`: carga la
  tabla desde `6-fusion/escena_por_lugar_propuesta_*.yaml` (o desde un módulo
  generado, mismo patrón que `curiana_agents_era2.py` con su `--check`) y
  expone tres funciones:
  - `escena_de(state) -> dict[agente, lugar]` — dónde está cada uno de los 63
    este turno;
  - `ambito_de(agente, state) -> str | None` — **la puerta única**. Devuelve el
    lugar en la era 2 y `None` en la era 1. Todo lo que la capa 2 filtra pasa
    por aquí y sólo por aquí;
  - `bloque_aqui_estas(agente, state, presupuesto=200) -> str`.
- `curiana_state.ComunidadState`: **no hace falta campo nuevo**. La escena
  escribe en `ubicaciones_override`, que ya existe (`:176-177`), que ya lee el
  prompt (`orchestrator:355-357`) y que ya lee `curiana_social.vecinos()`
  (`:134`). Cuatro lectores esperando a que alguien escriba.
- `curiana_orchestrator_v2.run_turn`: una llamada a `escena_de(state)` al abrir
  el turno, antes de elegir la ventana.
- `call_agent`: `[Tu ubicación]: {lugar}` (`:399`) se sustituye por
  `[Aquí estás]`, con el lugar dicho en prosa y los co-presentes.

**Qué ve el agente** (medido: **157 caracteres**, tope propuesto **200**):

```
[Aquí estás]: en la orilla de Tacuato, a la caída del sol, untando los
jachos. Contigo están Birokoa, que sube del salinar, y Chakamba, que ronda
las canoas.
```

Coste: **+2,2 %** sobre el prompt medio, +1,5 % en tier 1, +3,2 % en tier 3. Y
sustituye a `[Tu ubicación]`, así que el neto es menor.

**Qué se persiste.**

- **Estado**: `ubicaciones_override` ya va en `to_dict()`/`from_dict()`
  (`curiana_state.py:308-313`), así que `--continuar` lo hereda gratis.
- **Base**: hace falta migración. Dos opciones, y **no se hace aquí**:
  1. **Columna `lugar text` en `agent_responses`** — barata, una columna, y
     sirve para todo el análisis por lugar (`analizar_nodos.py`). Pero sólo
     sabe de los **12 que hablaron**; los otros 51 están en algún sitio y no
     queda registro.
  2. **Tabla `presencias`** `(id, run_id, turn_id, day, turn_num, agent_name,
     lugar, lat, lon, hablo boolean)` — 63 filas por turno × 6 turnos = **378
     filas por día**, nada. Es la que hace posible el visor (§5b), porque un
     mapa con 12 de 63 no es un mundo.

  **Recomendación: las dos.** `presencias` para el mundo y el visor;
  `agent_responses.lugar` denormalizado para que las consultas de lengua no
  tengan que unir. Migración declarada, no ejecutada.

**Qué es canon y qué canon-simulación.** La tabla lleva etiqueta por fila (§3).
Es canon la hora de varias celdas: la pesca nocturna del cunaro con jachos en el
Tiempo de Viento (`ecologia-078`, Esteves p. 33), el ciclo del biro sincronizado
con la seca (`ecologia-009`, `ecologia-010`), el mediodía sin trabajo
(`clima_era2.yaml` P2), el canto de noche del cantor (`creencia-010`, Oviedo vía
Arcaya pp. 116-118), el encierro de 1-3 días del boratio (`arcaya-1920`
pp. 97-100), la fuente del cerro que no cierra nunca (`arcaya-1920` p. 22). Es
canon-simulación **el reparto**: que ESTE agente esté en ESE lugar a ESA hora.

**Coste: 1 día**, la mitad en tests (la era 1 byte a byte: allí `ambito_de`
devuelve `None` y `ubicaciones_override` sigue vacío).

---

### Capa 2 — OÍR: el lugar como ámbito

**Qué es.** Dos cosas a la vez:

1. un bloque nuevo **`[Lo que se dijo aquí]`** con las intervenciones de los
   que estaban en el mismo lugar;
2. **las cuatro vías globales pasan a ser del lugar**. Es el diseño A de la
   frontera con «lugar» en vez de «nodo», y por eso la puerta es una sola:
   `ambito_de(agente, state)`.

**Qué cambia en el motor.**

- `curiana_lexicon.py`: `prompt_pendientes_evaluacion` (`:7523`) y
  `prompt_lexico_activo` (`:7512`) reciben un `ambito` y filtran por el lugar
  del autor / de los adoptantes; `vocabulario_para_agente` (`:8709`) lo pasa.
  `LexicoComunitario` (`:7258`) guarda el lugar del proponente y de cada
  adoptante, y `adoptar` (`:7307`) oficializa **por ámbito**, con una vía de
  «adoptada en dos ámbitos» que es justo lo que queremos ver nacer.
- `curiana_koine.py`: `CampoLexico` (`:709`) pasa a `{ambito: pesos}`;
  `CompetenciaLexica` (`:975`) guarda el ámbito de cada proponente y
  `prompt_competencias` (`:1036`) filtra.
- `curiana_orchestrator_v2.run_turn`: agrupa las `interactions` del turno por
  lugar y las pasa a `call_agent`; registra en el campo del ámbito del hablante
  (`:805-807`).
- `curiana_social.vecinos()` deja de necesitar arreglo aparte: con
  `ubicaciones_override` escrito, la co-ubicación (`:138-141`) empieza a
  significar algo por primera vez. **`VINCULOS` y `PRESTIGIO` siguen rotos**
  (indexados por los nombres de la era 1: 1 de 63 vivo) y eso hay que
  arreglarlo igual, con escena o sin ella — ver `frontera…` §4.4.

**Qué ve el agente** (medido: **254 caracteres**, tope propuesto **280**, ≤ 3
intervenciones de ≤ 70 caracteres):

```
[Lo que se dijo aquí, en este mismo sitio, hace un momento]:
— Birokoa: «taya naa-ka biro-ana» (he raspado la costra de sal).
— Chakamba: «pia chaa-da-ma?» (¿no vas a salir tú?).
— Waranaro: «wa-kari duna-rua-ana» (nuestro pescado está en el agua honda).
```

Coste: **+3,5 %** medio, +2,4 % t1, +5,2 % t3.

⚠ **El turno anterior, no el actual.** Si el bloque trae lo dicho en el MISMO
turno, el orden de habla vuelve a ser destino: es exactamente el mecanismo de V1
que produjo los tres cruces de Δturnos = 0 (Tebekoa y Kasebo oyendo a Simaure
porque hablaron después que él). Con el momento anterior, oír cuesta un turno
para todos por igual. Es la pregunta 5.

**¿Hay algo que oír?** Medido con `medir_presupuesto_escena.py [5]`, sin tocar
la ventana de 12, sobre el roster `todos` (63) y 6 días:

```
226 escenas, 125 con una sola voz, 101 con dos o más  →  45 % de las escenas
y por HABLANTE: 307 de 432 intervenciones (71 %) caen en un lugar donde
habla alguien más ese mismo turno.
```

O sea: **7 de cada 10 intervenciones tienen compañía**, y el mediodía —cuando
todos vuelven a la aldea— concentra hasta 8 voces en un solo lugar. La capa 2
tiene material sin tocar la ventana.

**Qué se persiste.** Nada nuevo más allá de la capa 1: el bloque se reconstruye
de `agent_responses` + `lugar`. Sí conviene sellar en `simulation_runs.config`
que el run corrió con escena y con qué tabla (como se sella el perfil).

**Canon.** El ámbito por lugar es **canon-simulación** declarado. Lo que el
canon sostiene es que los oficios trabajan separados y que los sitios son de
alguien: «cada sub-grupo tenía sus propias cabezas de playa, *entitling them to
specific fishing grounds*» (`oliver-1989-cap3` p. 275, atestiguado), y que cómo
se repartían «can not be inferred from the available data» (misma página).

**Coste: 1,5-2 días.** Es el mayor: toca tres módulos y la clase que guarda el
léxico comunitario.

---

### Capa 3 — HUELLA: que lo que se hace quede

**Qué es.** Hoy una respuesta es texto que se puntúa y se guarda. Con huella, la
respuesta deja **qué hizo, qué trajo, qué dio y adónde va**; el estado lo
guarda; el Director narra **desde lo que pasó** y no sólo desde lo que se dijo;
y los referentes novedosos pueden **nacer de lo que un viajero trae**.

**Qué cambia en el motor.**

- `ComunidadState`: `hizo_hoy` sube de local de `auto_mode`
  (`orchestrator:1298`) a **campo del estado**, con lugar: `{agente: {momentos,
  lugares, neos, trajo, dio}}`. Así `--continuar` lo hereda y el día siguiente
  existe el ayer.
- `curiana_observer.ObserverAgent.analizar`: extrae la huella. **Dos formas, y
  recomiendo la primera:**
  - **derivada** — lo que hizo = su clase de oficio × su lugar (ya está en la
    tabla); lo que trajo = las formas que usó **que no son de su ámbito**. Cero
    coste de prompt, cero riesgo sobre el score.
  - **declarada** — se le pide al agente un sufijo `[hice: … | traigo: … |
    voy: …]` y se extrae con regex, como ya se extraen los neologismos. Más
    fiel, pero **añade salida** y la salida también se puntúa.
- `director_narrate`: además de `Interacciones:`, recibe `Lo que pasó:` — tres
  o cuatro líneas de huella agregadas por lugar. Es lo que le permite escribir
  «las canoas volvieron a Tacuato» porque volvieron, y no porque se le ocurrió.
- **Los referentes, del viajero.** Hoy el evento de nombramiento presenta el
  mismo referente a los 12 del turno sin mirar de dónde son
  (`orchestrator:714-721`, cadencia en `:1321-1325`), y por eso **13 de 54
  formas del día 1 nacieron en los dos nodos a la vez**. Con huella, el
  referente entra **en un lugar** —el que lo ve— y viaja con quien viaja. Es el
  cambio que mata la simultaneidad por construcción.

**Qué ve el agente** (dos bloques, medidos **156** y **122** caracteres, topes
**180** y **150**):

```
[Ayer]: raspaste el biro de las charcas de Tacuato y lo contaste antes de que
suba al cerro; al anochecer bajaste a la orilla. Dijiste «biro-ana» dos veces.

[Hoy llegó gente]: Bajari, de Caseto, trajo el llamamiento del cerro y una
palabra que aquí nadie usa: «kashi-kasuta-iro».
```

Coste: +2,2 % y +1,7 % medio. El primero **sustituye** a la nota de día que
`AgentMemory` le pasa hoy por `[Tu memoria reciente]` (`:428-429`) y que dice,
literalmente, «D3: hablé al amanecer, mediodia; acuñé biro-ana».

**Qué se persiste.** `presencias` gana `trajo text[]` y `dio text[]`; o, si
Miguel prefiere una sola tabla, un `huella jsonb` en `agent_responses`.
**Migración declarada, no ejecutada.** Y `state.hizo_hoy` entra en el JSON del
estado, que es lo que `--continuar` lee.

**Canon.** El don que sube y baja del cerro es canon: el diao de cada clan
«entrega lo suyo a Manaure, que redistribuye» y cada delegación baja «con lo
recibido y con las formas nuevas» (`estructura_social_era2.yaml`
§ciclo_ritual_merejuy, CM fases 4 y 5; `creencia-013`; Ampíes f. 14). El
`waitiao` —«amigo ritual, aliado de alianza», con intercambio de nombres entre
aliados (`oliver-1989-cap2` p. 147, atestiguado)— es la voz caquetía del
vínculo entre personas de nodos distintos, y el elenco ya tiene a un agente que
se llama así.

**Coste: 2 días.**

---

### Capa 4 — POTESTAD: recorrer el mundo

**Qué es.** El agente **elige** adónde ir mañana, dentro de lo que su papel
permite; el Director valida. Es lo que Miguel pidió con esa palabra: el mundo
más allá de un lugar se recorre **según la potestad del agente**.

**Qué cambia en el motor.**

- `curiana_escena.potestad_de(agente) -> set[lugar]` — derivada del canon, no
  escrita agente a agente.
- `call_agent`: bloque `[A dónde puedes ir mañana]`.
- `run_turn` / `escena_de`: si el agente declaró destino y está en su potestad,
  la escena del día siguiente lo pone allí; si no, la tabla manda. **El Director
  no se convierte en juez**: la validación es una comprobación de pertenencia al
  conjunto, no una llamada más.

**Qué potestades da el canon.**

| quién | potestad | fuente |
|---|---|---|
| **Manaure** | preside la convergencia del cerro; sube en hamaca con séquito de los dos clanes por turnos | `of-01`, `of-11`; `creencia-013`; Ampíes f. 14 |
| **el boratio mayor (Sawaka)** | vive en el cerro, abre y cierra la convergencia, se encierra 1-3 días | `of-02`; `arcaya-1920` pp. 97-100 |
| **el ayunante (Hayo)** | sube al cerro con él; ayuna en el manglar | `of-04`; `transmision-001` |
| **la boratia de pueblo (Paugis)** | su aldea; «en cada pueblo principal hay un boratio», al que **todos acuden** | `of-03`; `arcaya-1920` pp. 97-100 |
| **quien trueca** | la salina y el camino; la concha es la unidad de cuenta y la sal sale de la península | `sitios_era2.yaml` Tacuato.recoleccion y .sal; `ecologia-009` |
| **los pescadores** | **su** zona y no la del otro: ZG2 para GUARANAO, ZA1 para AMUAY | decisión 2026-09-14; `oliver-1989-cap3` p. 275 |
| **los casados cruzando** | su nodo de origen. Medidos: **11** viven en el nodo del cónyuge, **6 en el roster** | derivado del linaje contra el linaje de la casa |
| **Bajari, el corredor** | «el más rápido de AMUAY: lleva el llamamiento de casa en casa cuando el cerro convoca» — **5 destinos, 4 fuera de su nodo** | `of-12`; ficha |
| **Humohumo** | «lleva los recados del Manaure a los apopos de las cuatro casas» — **4 destinos, 2 fuera de su nodo** | `of-12`; ficha |
| **Chuchubi** | «corre los avisos entre El Cayude, Tacuato y Moruy» — **2 destinos, 0 fuera de su nodo** | ficha |
| **Wamipa** | el hallazgo de la medición: hijo del Manaure y de Karebe, **linaje Warana (AMUAY)**, criado en Moruy, y su tío materno es **Tebekoa, el apopo de Caseto**. Por la regla matrilineal el sobrino va con el tío materno | `transmision-025`, `transmision-027`; ficha |

**Qué ve el agente** (medido: **170 caracteres**, tope **200**):

```
[A dónde puedes ir mañana]: la orilla de Tacuato (la tuya), el conuco, el
salinar, o el camino a Moruy, que es un día de ida. A la costa del oeste no
vas: no es tu playa.
```

Coste: +2,4 % medio, +3,5 % t3.

**Qué se persiste.** `presencias.va_a` (o el mismo `huella jsonb`). Y en
`simulation_runs.config`, si el brazo corrió con potestad.

**Canon vs. canon-simulación.** Atestiguado: que hay convergencia y que las
delegaciones suben y bajan; que un boratio hay por pueblo y todos acuden a él;
que cada subgrupo tiene sus playas. Canon-simulación: la lista concreta de
lugares alcanzables por cada oficio y **la cadencia** — el CM del canon cae en
los días 55-58 de la seca y una cadena de 8 días no llega: la cadencia del
Capubana tendrá que ser un parámetro declarado (`--capubana-cada N`) sellado en
la config, como se sella el perfil.

**Coste: 2 días.**

**Los cuatro bloques juntos**: 859 caracteres = **+11,9 %** sobre el prompt
medio, +8,2 % en tier 1, **+17,4 % en tier 3**. El tier 3 es el que
proporcionalmente más paga, como con `[Tu tierra]`. Si Miguel quiere abaratar,
el recorte natural es dar a los tier 3 sólo las capas 1 y 3 (estar y ayer) y
no el bloque de oír.

---

## 3. La tabla propuesta — derivada, no escrita

`6-fusion/escena_por_lugar_propuesta_2026-09-17.yaml`, generada por
`6-fusion/scripts/derivar_escena_por_lugar.py --yaml`.

**Cómo se deriva, y por qué importa que se derive.** Ninguna fila se escribió
agente a agente:

1. La **clase de oficio** sale de `oficio` y `rol_en_la_casa` de la ficha por
   **reglas de palabra clave declaradas y ordenadas** (la primera que casa
   gana). Están en el script y en el YAML (`§reglas_de_clase`), para que se
   puedan discutir.
2. El **lugar** sale de una **plantilla** (`{sitio}:orilla`, `{zona}`,
   `Capubana`, `camino:{sitio}`) que se resuelve con la ficha de cada agente.

Consecuencia: **si el casting cambia, la tabla cambia sola**. Y el nodo de un
lugar no se programa: sale del mapa.

### 3.1 Cobertura

```
63 agentes en 22 clases de oficio; sin clasificar: 0
viento      63 de 63 con lugar en los 6 momentos
seca_larga  63 de 63 con lugar en los 6 momentos
siembra     63 de 63 con lugar en los 6 momentos
lugares distintos en los tres períodos: 29
```

Las 22 clases: `mensajeria` 3 · `mando` 3 · `oraculo` 2 · `curacion` 1 ·
`huesos` 2 · `cantor` 1 · `arbitraje` 1 · `merejuy` 1 · `sal` 1 ·
`agua_dulce` 3 · `vigia` 2 · `marisqueo` 2 · `casa` 5 · `fibra` 5 · `pesca` 8 ·
`canoa` 3 · `conuco` 5 · `monte` 2 · `alfareria` 3 · `vision` 1 ·
`memoria_de_casa` 3 · `ninez` 6.

Un agente cambia de clase con el año si **su ficha lo dice**: Kunaro-bana
(«pesca el cunaro en la seca y trabaja **el conuco en las lluvias**») pasa a
`conuco` en el período de siembra. Es la única regla de ese tipo y está leída
del texto, no inferida.

### 3.2 La tabla, en corto (Tiempo de Viento)

| clase | amanecer | mañana | mediodía | tarde | anochecer | noche | etiqueta |
|---|---|---|---|---|---|---|---|
| `pesca` | {zona} | {zona} | {sitio} | orilla | orilla | **{zona}** | canon-sim. (ecologia-078 fecha la noche) |
| `marisqueo` | orilla | orilla | {sitio} | orilla | {sitio} | {sitio} | canon-sim. |
| `vigia` | punta | punta | {sitio} | punta | {sitio} | {sitio} | atest. la atalaya (ecologia-080) |
| `sal` | salinar | salinar | {sitio} | salinar | {sitio} | {sitio} | atest. el ciclo (ecologia-009/010) |
| `conuco` | conuco | conuco | {sitio} | conuco | {sitio} | {sitio} | atest. el conuco (ecologia-029/030) |
| `agua_dulce` | {jagüey} | {jagüey} | {sitio} | {jagüey} | {sitio} | {sitio} | atest. la fuente (arcaya p. 22) |
| `monte` | {sitio} | matorral | {sitio} | matorral | {sitio} | {sitio} | canon-sim. |
| `alfareria` | {sitio} | taller | {sitio} | taller | {sitio} | {sitio} | atest. la cadena técnica (ecologia-025) |
| `fibra` | {sitio} | {sitio} | {sitio} | taller | {sitio} | {sitio} | canon-sim. |
| `canoa` | orilla | taller_canoas | {sitio} | taller_canoas | {sitio} | {sitio} | atest. la canoa (ecologia-031/032) |
| `casa` · `mando` · `curacion` · `huesos` · `cantor` · `merejuy` · `memoria_de_casa` · `vision` · `ninez` | {sitio} los seis momentos | | | | | | ver el YAML |
| `arbitraje` | {sitio} | conuco | {sitio} | orilla | {sitio} | {sitio} | hipotético (of-13) |
| `oraculo` | **Capubana** los seis momentos | | | | | | atest. el encierro (arcaya 97-100) |
| `mensajeria` | {sitio} | **camino** | camino | camino | {sitio} | {sitio} | reconstr. (of-12) |

Excepciones por período, todas leídas del canon:

- **seca larga**: `agua_dulce` va a **`Capubana:fuente`** (el cargador lo dice
  literalmente: «La hora del agua: se va al jagüey, **o a la fuente del
  cerro**»); el `conuco` «espera, seco» y su gente se queda en la aldea.
- **siembra**: «el salinar está parado», así que `sal` pasa al conuco; la
  `alfareria` de Moruy iría al barrial de Abudure, que la lluvia descubre
  (Esteves p. 11).
- **viento**: la `pesca` sale de noche con los jachos (`ecologia-078`).

### 3.3 Ocupación — cuánta gente hay en cada lugar, por momento

Tiempo de Viento, **extracto** (los 29 lugares de los tres períodos, en el YAML
`§ocupacion`, y la escena de los 63 uno a uno en `§escena_por_agente`):

```
lugar                       amane  mañan  medio  tarde  anoch  noche
Capubana                        2      2      2      2      2      2
Capubana:fuente                 1      1      ·      1      ·      ·
Carirubana                      6      6     12      5     11     11
Carirubana:orilla               5      2      ·      3      1      ·
Carirubana:taller_canoas        ·      3      ·      3      ·      ·
Caseto                          7      5     11      3     10     10
Caseto:conuco                   3      3      ·      3      ·      ·
El Cayude                       7      5     11      5     10     10
El Cayude:punta                 2      2      ·      2      ·      ·
Moruy                          11     10     11      9     12     12
Tacuato                         6      2     13      1     10     10
Tacuato:salinar                 1      1      ·      1      ·      ·
ZA1                             3      3      ·      ·      ·      3
ZG2                             5      5      ·      ·      ·      5
camino:Caseto / El Cayude / Moruy   ·  1 c/u  1 c/u  1 c/u   ·      ·
```

**Escenas (lugares con alguien) por momento**: viento 16 · 24 · **9** · 27 ·
10 · 8; seca larga 14 · 21 · 9 · 23 · 10 · 6; siembra 15 · 23 · 9 · 24 · 6 · 6.

El día tiene forma: **la mañana y la tarde dispersan** (24 y 27 lugares
ocupados) y **el mediodía y la noche juntan** (9 y 8). Eso no lo decidí yo: lo
dice el cargador del clima («el sol pega; hora de sombra, de comer y de
hablar»).

### 3.4 Lugares compartidos — el hallazgo incómodo

```
(a) EMERGENTES — los dos nodos en el mismo lugar el mismo momento: 0
(b) DECLARADOS compartidos por decisión:
    Capubana          lo ocupa: GUARANAO
    Capubana:fuente   lo ocupa: GUARANAO
```

**Cero.** En los 6 momentos de los 3 períodos, GUARANAO y AMUAY no coinciden
nunca. Y el cerro, que la decisión del 2026-09-14 declara «centro compartido»,
**sólo lo ocupa GUARANAO**: los dos agentes que tienen oficio allí (Sawaka y
Hayo) son de la casa del Manaure, y **AMUAY no tiene ni un agente de
`agua_dulce`**, así que en la seca larga, cuando el jagüey baja y la fuente del
cerro es la única agua corriente de la península, los tres que suben son los
tres de GUARANAO.

Es un resultado, no un fallo del elenco. Dice tres cosas:

1. **El mundo no produce contacto por sí solo.** La escena reproduce fielmente
   lo que el canon dice —zonas de pesca «separadas y exclusivas»— y el
   resultado es dos mundos paralelos. Si la koiné entre nodos va a existir, el
   contacto hay que **declararlo** o hay que **hacerlo viajar**.
2. **El canon ya tiene el mecanismo del agua, y es de envío, no de visita.** El
   ciclo menor CL dice: «cada clan hace su rito con su boratio de pueblo; **el
   boratio mayor manda agua del cerro a los dos**», con contacto «bajo: solo el
   agua y un emisario cruzan». El agua **baja**; los de AMUAY no suben. Eso es
   mensajería, que es la capa 4.
3. **Los tres mensajeros son hoy el único canal que cruza solo.** Medido:

```
Chuchubi  GUARANAO  desde El Cayude   → Moruy, Tacuato            (0 fuera)
Humohumo  GUARANAO  desde Moruy       → Carirubana, Caseto, El Cayude, Tacuato  (2 fuera)
Bajari    AMUAY     desde Caseto      → Capubana, Carirubana, El Cayude, Moruy, Tacuato  (4 fuera)
destinos fuera del propio nodo, sumados los tres: 6
```

**Los candidatos a lugar compartido, con su canon**, para que Miguel elija
(pregunta 2):

| candidato | qué lo sostiene | distancia medida |
|---|---|---|
| **el Capubana** | decisión 2026-09-14: «centro compartido que congrega… a nivel energético»; la fuente «NO CIERRA NUNCA» | Moruy 3,4 km · **Caseto 9,4 km** |
| **el camino Moruy–Caseto** | el elenco lo llama *la alianza*: «Caseto es el sitio de AMUAY más cercano a Moruy… ese camino corto ES la alianza: la esposa principal viene por él» | **7,6 km — el par más cercano de todo el mapa, y es ENTRE nodos** |
| **la laguna de Guaranao** | «las salinas más importantes» de Paraguaná (arcaya p. 22); a ~3 km de Carirubana (AMUAY) **y lleva el nombre del otro clan**; el elenco la declara «tensión declarada» | 3 km de Carirubana |
| **la zona ZX (Adícora–Buchuaco)** | el canon la declara «el candidato natural a caladero disputado y a pleito de linderos que se arregla en la convergencia (of-13)» | entre ZA3 y ZG2 |

Y el aviso geográfico que ya daba la propuesta de la frontera, re-medido aquí:

```
  3.4  Moruy – Capubana   (intra)
  7.6  Moruy – Caseto     (ENTRE)
  9.4  Caseto – Capubana  (ENTRE)
  9.4  El Cayude – Caseto (ENTRE)
 12.7  Tacuato – El Cayude (intra)
media intra 14.7 km · media entre 22.2 km
```

**Los tres pares más cercanos después de Moruy–Capubana son los tres ENTRE
nodos.** Una frontera binaria contradice el mapa; una frontera por lugar y
distancia no.

### 3.5 Los cruzados por matrimonio — 11, y uno que no estaba en la lista

Derivados del linaje del agente contra el linaje declarado de su casa (no de
una lista escrita): **11 viven en el nodo del cónyuge, 6 en el roster** — que
es exactamente el `portadores_entre_nodos_en_el_roster: 6` que el propio elenco
declara.

| nombre | de | vive en | clase de oficio | roster |
|---|---|---|---|---|
| Dipopo | GUARANAO | Caseto (AMUAY) | fibra | |
| Ebokoa | GUARANAO | Carirubana (AMUAY) | pesca | ✓ |
| Kasebo | GUARANAO | Caseto (AMUAY) | pesca | ✓ |
| Mene | GUARANAO | Carirubana (AMUAY) | canoa | |
| Dunakoa | AMUAY | El Cayude (GUARANAO) | agua_dulce | ✓ |
| Duraboa | AMUAY | Tacuato (GUARANAO) | pesca | |
| Karebe | AMUAY | Moruy (GUARANAO) | mando | ✓ |
| Kumarawa | AMUAY | Moruy (GUARANAO) | casa | |
| Urari | AMUAY | Tacuato (GUARANAO) | monte | ✓ |
| **Wamipa** | AMUAY | Moruy (GUARANAO) | agua_dulce | |
| Waranaro | AMUAY | El Cayude (GUARANAO) | pesca | ✓ |

**Wamipa no estaba en la lista de diez de la propuesta de la frontera**, porque
aquella contaba cónyuges y él es un **hijo**: linaje Warana por su madre Karebe,
nacido y criado en la casa Kaira, y su tío materno es Tebekoa, el apopo de
Caseto. Con la regla matrilineal y el tío materno que se lleva al sobrino
(`transmision-025`, `transmision-027`), Wamipa es el primer caso de potestad de
cruce **por descendencia y no por matrimonio** — y es, además, el guardián del
agua del cerro. Si el agua baja a AMUAY, baja con él.

### 3.6 Etiqueta por fila

Cada clase lleva su `etiqueta` y su `fuente` en el YAML. Resumen: **4 clases
atestiguadas en su hora** (`sal`, `cantor`, `oraculo`, `curacion`), **5 con el
oficio atestiguado y el día canon-simulación** (`pesca`, `vigia`, `conuco`,
`alfareria`, `canoa`), **2 hipotéticas** (`arbitraje` of-13, `merejuy` of-07),
**2 reconstruidas** (`memoria_de_casa`, `mensajeria`), el resto
canon-simulación. Ninguna fila entra al prompt con su etiqueta: la etiqueta vive
en el YAML, como con `[Tu tierra]`.

---

## 4. La escena: cómo se elige, qué se conserva

### 4.1 El sorteo, y de qué RNG

**La tabla es determinista**: `(clase, momento, período) → plantilla → lugar`.
No hace falta azar para la capa 1. El azar entra en **tres sitios y sólo tres**:

1. a qué casa llega hoy un mensajero (de sus 2-5 destinos);
2. si un cruzado por matrimonio visita hoy su nodo de origen (capa 4);
3. qué línea del canon ve el agente en su lugar, si hubiera varias.

**Nunca con `hash()`** —va salado por proceso (`PYTHONHASHSEED`) y no repetiría
un run— y **nunca con el `random` global del motor**: ese está compartido con
`director_select_event` (`orchestrator:548`), con el muestreo del lexicón y con
los nombramientos, así que sacar un número de él **desplaza la cadena de
eventos** y dos runs con la misma semilla dejarían de ser el mismo run. La serie
B quedaría incomparable consigo misma.

**Se usa el mismo patrón que ya está en el motor**: `blake2b(semilla del run,
nombre del agente, día, momento)`, como `curiana_koine.formas_seed_de()`
(DISENO_KOINE §4). `curiana_mundo._indice` (`:225-231`) usa `sha1(agente|día)`,
de la misma familia pero **sin semilla**: la escena sí la toma, para que
`--semilla N` mueva los viajes y el run siga siendo reproducible.

### 4.2 La ventana de 12 no se toca

`_ventana` sigue igual (`:630-640`): la escena decide **dónde está** cada uno,
no **quién habla**. Así el día sigue teniendo 12 voces × 6 turnos = 72
respuestas y los días siguen siendo comparables con la serie B, que es la
condición para que la diferencia signifique algo.

La alternativa —elegir la ventana **por lugar**, para garantizar ≥ 2 voces por
escena— cambia quién habla y rompe la comparabilidad. Y la medición dice que no
hace falta: **71 % de las intervenciones ya caen en un lugar con más de un
hablante**. Es la pregunta 4.

### 4.3 Qué oye un agente: ¿hoy, o también ayer?

Tres opciones, de menos a más memoria:

- **el momento anterior, mismo lugar** (lo que recomiendo): oír cuesta un turno
  para todos por igual y el orden de habla deja de ser destino;
- **el momento anterior + el cierre de ayer en ese lugar**: da continuidad de
  día a día, que es lo que `--continuar` necesita, pero duplica el bloque;
- **el mismo turno**: es V1 otra vez, con otro nombre.

### 4.4 El evento de nombramiento y el evento del Director

- **El nombramiento pasa a ser de un lugar.** Hoy se presenta a los 12 del
  turno (`:714-721`) y por eso 13 de 54 formas nacieron en los dos nodos a la
  vez. Con escena, el referente aparece **donde tiene sentido que aparezca** —
  una bestia varada en la orilla, un cometa en cualquier sitio de noche— y
  viaja con quien lo cuenta. Requiere que `REFERENTES_NOVEDOSOS` declare la
  locación de cada referente: **10 referentes, una línea cada uno**, y es una
  edición de `curiana_koine`, no del scorer.
- **El evento del Director no cambia.** `director_select_event` sigue eligiendo
  uno por turno y `evento_para_elenco()` sigue diciéndolo para el mundo activo.
  Lo único que la escena le añade es que el evento **puede** declarar lugar
  (varios ya lo insinúan en la prosa); si lo declara, sus protagonistas están
  allí ese turno. Sin declararlo, se comporta como hoy.

### 4.5 La era 1, byte a byte

En CURIANA **no hay escena**:

- `ambito_de()` devuelve `None` → las cuatro vías siguen globales;
- `escena_de()` devuelve `{}` → `ubicaciones_override` sigue vacío y
  `[Tu ubicación]` sigue saliendo de `ubicacion_default`, que allí es una de las
  13 `LOCACIONES` y no un sitio;
- ningún bloque nuevo se añade al prompt.

Un test tiene que afirmar que el prompt de la era 1 es **idéntico carácter a
carácter** con y sin el módulo de escena cargado, como ya se hace con
`estado_inicial('CURIANA')` y con `decir_para_el_mundo`.

---

## 5. Medición: qué debería moverse, y el brazo de control

### 5.1 Qué debería moverse en `analizar_nodos.py`

Hoy, sobre el día 1 de la serie B (run `3973d317`): brecha intra/entre
**0,0154** (ventana) y **0,0057** (emergente); de 54 formas clasificables **31
cruzaron** (mediana 1 turno, **3 en el mismo turno**), **13 nacieron multinodo**
y 10 no cruzaron.

Predicciones falsables, por capa:

| métrica | hoy | con capas 1-2 | con 1-3 | si no pasa |
|---|---|---|---|---|
| `mismo turno` | **3** | **0** | 0 | el diagnóstico de V1 (frontera §1.5) está mal |
| `multinodo` | **13** | baja | **~0** | el nombramiento no era la puerta |
| `Δturnos` mediana | 1 | ≥ 2 | ≥ cadencia de viaje | oír por lugar no filtra nada |
| `exclusiva` / `inclinada` | 10 / 13 | suben | suben más | los ámbitos no separan |
| `compartida` | 31 | baja | baja | idem |
| **brecha intra/entre** | 0,0154 / 0,0057 | **se abre el día 1** | se abre y **se cierra tras cada Capubana** | no hubo nunca dos nodos |

**La firma es el diente de sierra, no el nivel.** Que la brecha suba y baje con
la cadencia del Capubana es lo que distingue koineización de ruido; un nivel
alto constante sólo dice que separamos dos poblaciones.

### 5.2 Métricas nuevas que la escena hace posibles

Todas se leen de `presencias` + `word_uses` sin tocar el scorer:

- **brecha por LUGAR**, no sólo por nodo: es la lectura que el mapa aguanta
  (Moruy–Caseto 7,6 km contra Tacuato–El Cayude 12,7 km);
- **primera aparición de una forma fuera de su lugar de nacimiento**, con el
  agente que la llevó — la ruta de contagio deja de inferirse y se lee;
- **cuántas formas mueren en su lugar** (las que no salen nunca): hoy no se
  puede medir porque no hay lugar.

### 5.3 Cuántos días de cadena

- **mínimo técnico: 2 días** — `analizar_nodos.py` dice «datos insuficientes»
  con uno y `curiana_cadena.py` necesita dos días cerrados.
- **para ver la escena: 3 días** — `mismo turno` a 0 y `multinodo` desplomado
  son efectos del día 1.
- **para ver la koiné entre lugares: 6-8 días encadenados** — hacen falta dos
  Capubana para dos dientes de la sierra, y el nombramiento tarda ~7 días en
  agotar los 10 referentes con la cadencia de 4 turnos.
- **con brazo de control: el doble**, 12-16 días de API.

### 5.4 El brazo de control

**Misma semilla, sin escena.** No es `--ablacion` (esa apaga las tres
inyecciones que empujan la convergencia y seguirá existiendo aparte): es
`--escena / --sin-escena` sobre la misma semilla y la misma serie. La evidencia
es la **diferencia**, como con la ablación. Y —esto no es negociable— **una
escena no puede entrar a mitad de cadena**: es una serie nueva desde el día 1
(`--serie era2-c`).

---

## 5b. Verlo: el mundo es un grafo, no un tablero

Miguel pregunta si hará falta «un emulador visual, como un videojuego». **No, y
conviene que no.**

**Lo que se está construyendo no es un tablero de casillas: es un grafo de
lugares.** Nodos: las 29 posiciones de la tabla (aldeas, orillas, conucos,
salinares, puntas, talleres, el cerro). Aristas: los caminos entre aldeas, las
zonas de pesca que unen a varias casas de un mismo nodo, y el Capubana, que toca
a los dos. Un motor de juego resolvería colisiones, pathfinding y física que
aquí no significan nada; el grafo lo resuelve una consulta.

**El «emulador» más barato es un visor de repetición sobre el mapa real de
Paraguaná**: quién estaba dónde en cada turno, y qué dijo allí. No simula: lee.
Y ya hay dónde ponerlo.

**Referencia.** Es exactamente el diseño de *Generative Agents* (Park et al.,
2023, «Smallville»): agentes con **posición**, **horario por rol**,
**percepción por cercanía**, **memoria** y **conversación por co-presencia**. Lo
que allí se veía como un videojuego era **una repetición del estado**, no la
simulación: el mundo vivía en las estructuras de datos y el sprite sólo lo
dibujaba. Las cuatro capas de §2 son, una a una, esas mismas piezas — estar,
percibir, recordar, moverse — y la nuestra tiene encima algo que Smallville no
tenía: cada lugar cita una fuente.

**Coordenadas: ¿se puede dibujar hoy?** Medido:

```
41 puntos con lat/lon en el canon de la era 2
  propio            8 de 29 — el canon los sitúa con lat/lon propios
  heredado         16 de 29 — se dibujarían ENCIMA de su aldea
  zona              2 de 29 — no son un punto: son el área de sus lugares
  arista            3 de 29 — no son un punto: son un camino entre dos aldeas
  sin-coordenada    0 de 29
```

Los 41 puntos salen de `sitios_era2.yaml`, `elenco_era2.yaml`,
`estructura_social_era2.yaml` (zonas pesqueras + lugares del Kapubana) y del
**mapa vivo** que `2-lengua/toponimos.yaml` guarda en el campo `mapa_vivo` (el
par de OSM en prosa, que `barrer_mapa.py` cruza). **Ningún lugar se queda sin
nada**: 8 tienen punto propio, 16 heredan el de su aldea, 2 son áreas y 3 son
caminos. Eso basta para un mapa honesto; lo que falta para afinarlo son puntos
de detalle (el salinar de Tacuato, los jagüeyes, los talleres), y ésos **no los
tiene el canon** — no se inventan.

**Dónde vive el visor.** El sitio público ya tiene el patrón exacto:
`curiana_sim/export_*_seed.py` escribe JSON estático en `content/simulador/` y
la página Next lo lee en build (`lib/runs.ts` sobre
`content/simulador/runs/index.json`); la ruta `/simulador` redirige a
`/kaketiana` desde el 2026-08-24 (`next.config.js`) y el experimento vive en
`/kaketiana/experimento`. Un visor de escena serían dos piezas del mismo molde:

- `curiana_sim/export_escena_seed.py` → `content/simulador/escena/<run>.json`
  con `{dia, turno, momento, agente, nodo, lugar, lat, lon, texto_recortado}`
  leído de `presencias` + `agent_responses`;
- `components/simulador/MapaDeEscena.tsx` — el mapa de Paraguaná, los 29 lugares
  como nodos, los caminos como aristas, un control de turno y, al pinchar un
  lugar, lo que se dijo allí.

Sin motor de juego, sin servidor, sin egress: **estático, como todo lo demás**.
Y tiene un efecto colateral que vale por sí solo: **un visor es un guardián**.
El día que el Director diga que las canoas volvieron al Golfete y en el mapa no
haya nadie en el Golfete, se ve de un vistazo.

---

## 6. Lo que no se toca

`score_linguistico()` · `pct_caquetio` y los demás `pct_*` · `capas_de_score` ·
`curiana_observer` como registro · el esquema de `word_uses`, `koine_metrics` y
`koine_lexicon` · el catálogo de eventos y `decir_para_el_mundo` ·
`curiana_mundo` y `[Tu tierra]` · el elenco generado · el corpus · **la era 1,
que tiene que seguir byte a byte**.

La regla es la misma que gobierna los perfiles: **la escena cambia lo que el
agente VE, nunca con qué se le PUNTÚA**
(`5-experimento/disenos/05_perfiles_de_run.md`, y el test que la vigila). Si el
score se moviera con la escena, la diferencia entre brazos sería un artefacto
del instrumento.

---

## 7. Las preguntas para Miguel

### 1. ¿La tabla es `oficio × momento` con excepciones de período, o `oficio × período × momento` entera?

- **A.** Por momento, con excepciones declaradas donde el canon fecha la hora
  (lo medido: 22 clases × 6 momentos + 5 excepciones).
- **B.** Entera: 22 × 3 × 6 = 396 celdas, cada una decidida.
- **C.** Por momento y sin excepciones: el período sólo cambia el texto de
  `[Tu tierra]`, no el lugar.

> **Recomiendo A.** La excepción es donde está el canon —el biro de la seca, los
> jachos de noche, «el conuco espera, seco»— y B pide decidir 396 veces lo que
> el cargador del clima ya decidió seis veces por período.

### 2. ¿Qué lugares se comparten entre nodos?

La escena derivada da **cero** lugares compartidos emergentes, y el Capubana,
declarado compartido, sólo lo ocupa GUARANAO.

- **A.** Sólo el **Capubana**, y en el día de Capubana (la cadencia de la
  pregunta 7). El resto del año, dos mundos.
- **B.** Capubana **+ el camino Moruy–Caseto**, que el elenco llama «la
  alianza» y que el mapa dice que es el par más cercano de todos (7,6 km).
- **C.** Capubana + camino **+ la laguna de Guaranao** como salina de los dos
  (a 3 km de Carirubana, con el nombre del otro clan encima) **+ ZX
  Adícora-Buchuaco** como caladero disputado, que es lo que of-13 arbitra.

> **Recomiendo B para la serie C y dejar C para la siguiente.** El camino ya
> está escrito en el canon como el canal de la alianza y no hay que inventar
> nada; la laguna y ZX abren pleito (que es material bueno) pero meten dos
> lugares nuevos con gente nueva, y la primera cadena tiene que poder
> atribuirle el efecto a una cosa.

### 3. ¿Cuántas escenas por turno y cuántas voces por escena?

Medido sin tocar nada: 9 escenas al mediodía, 27 a la tarde; 71 % de las
intervenciones tienen compañía en su lugar.

- **A.** Las que salgan (entre 6 y 27), sin tope.
- **B.** Tope de escenas por turno: si salen más de N, los lugares con una sola
  persona se colapsan a su aldea.
- **C.** Mínimo de voces: un lugar con una sola persona no es escena y esa
  persona se cuenta en su aldea.

> **Recomiendo A.** Un pescador solo en el agua a la mañana **es** el dato: su
> ámbito está vacío y por eso no oye nada. Colapsarlo sería devolver la
> comunidad global por la puerta de atrás.

### 4. ¿La ventana de 12 se elige por lugar?

- **A.** No: `_ventana` sigue igual y la escena sólo dice dónde está cada uno.
- **B.** Sí: se eligen 3-4 lugares por turno y hablan los que estén allí.
- **C.** Mixto: 8 por rotación y 4 completando los lugares donde ya hay alguien.

> **Recomiendo A.** B garantiza conversación pero cambia **quién habla**, y con
> ello la comparabilidad con la serie B: el número de voces por agente y por día
> es la base de `distancia_idiolectal`. La medición dice que A ya deja al 71 %
> de las intervenciones con compañía.

### 5. ¿Cuánto se oye?

- **A.** El **momento anterior**, mismo lugar, ≤ 3 intervenciones, tope 280
  caracteres.
- **B.** El momento anterior **+ el cierre de ayer en ese lugar** (memoria de
  día a día, ~+150 car.).
- **C.** El **mismo turno**, los que ya hablaron antes que tú.

> **Recomiendo A.** C es V1 con otro nombre: es literalmente el mecanismo que
> produjo los tres cruces en el mismo turno del día 1. B es mejor con la capa 3
> ya dentro, no antes.

### 6. ¿El Director narra por escena?

- **A.** Uno por turno, como hoy, pero recibiendo las intervenciones
  **agrupadas por lugar** (0 llamadas más).
- **B.** Uno por lugar con gente (×6 a ×27 llamadas por turno — inviable).
- **C.** Uno por turno + uno por el Capubana cuando hay convergencia (×2 sólo
  esos días).

> **Recomiendo A, y C cuando entre el Capubana.** El Director no llega al prompt
> del agente (§1.6), así que narrar por escena **no mueve ninguna métrica de
> lengua**: arregla la coherencia del mundo, que es real pero no es la
> pregunta, y B multiplica el gasto por veinte para eso.

### 7. ¿Cuál es la cadencia del Capubana?

El canon pone el ciclo mayor CM en los **días 55-58 de la seca**, una vez por
año simulado de 120 días — inalcanzable en una cadena de 8.

- **A.** `--capubana-cada N` declarado y sellado en la config, con N = 3 para
  la primera cadena (dos convergencias en 8 días).
- **B.** El calendario literal: no hay Capubana en la serie C.
- **C.** Comprimir el año simulado (120 → 24 días) para que el calendario del
  canon caiga dentro.

> **Recomiendo A.** Es lo mismo que se hizo con el perfil: un parámetro
> declarado que el run dice de sí mismo. C toca el calendario, que es canon
> fusionado y del que cuelgan las estaciones, los eventos y `[Tu tierra]`.

### 8. ¿Los referentes novedosos nacen del viajero?

- **A.** Sí: el referente aparece **en un lugar** y sólo lo ven los que estén
  allí; viaja con quien viaja. Pide declarar la locación de los 10 referentes.
- **B.** No: sigue presentándose a los 12 del turno (y `multinodo` sigue en 13).
- **C.** Mixto: los referentes de cosa (la bestia varada, la marea roja) por
  lugar; los del cielo (el cometa, el eclipse) a todos, porque el cielo se ve
  desde los dos nodos.

> **Recomiendo C.** Es más fiel y es más barato de justificar: un eclipse **sí**
> lo ven los dos nodos a la vez, y esa simultaneidad deja de ser un artefacto
> para ser un hecho del mundo. Con C, las formas multinodo que queden significan
> algo.

### 9. ¿La serie C arranca con las capas 1-2 solas, o 1-3?

- **A.** **1-2** (estar + oír): el brazo mínimo que ataca lo medido, ~3 días de
  código.
- **B.** **1-3** (+ huella): el Director narra desde lo que pasó y los
  referentes viajan; ~5 días.
- **C.** Las cuatro de una vez; ~7 días.

> **Recomiendo A, con la capa 3 como segundo brazo de la misma serie.** Con 1-2
> la diferencia contra el control es atribuible a una cosa: el ámbito. Si entra
> también la huella, y la brecha se abre, no sabremos si fue el ámbito o el
> viaje de los referentes. Y la capa 4 (potestad) **necesita** la 3: sin rastro
> de lo que se trajo, moverse no deja nada.

### 10. ¿Se hace el visor de repetición?

- **A.** Sí, sobre el mapa real, en `/kaketiana`: `export_escena_seed.py` +
  `MapaDeEscena.tsx`, estático, leyendo `presencias`. Medio día de exportador,
  1-2 de componente. Es además un guardián: un Director que narra a gente que no
  estaba allí se ve de un vistazo.
- **B.** Un volcado de texto por turno en el log (`escena del turno: Tacuato:
  Birokoa, Chakamba…`), gratis, sin mapa.
- **C.** Nada por ahora.

> **Recomiendo A, con B el mismo día como andamio.** B cuesta diez líneas y hace
> la escena depurable desde el primer run; A es lo que convierte la escena en
> algo que se puede *mirar* —y en un guardián— y es barato porque el molde ya
> existe: un exportador y un componente, estáticos, sin motor de juego y sin
> egress. Lo único que pide A antes de lucir es la tabla `presencias` (PR 3),
> porque un mapa con 12 de 63 no es un mundo.

---

## 8. Plan de implementación por PRs

Cada PR trae sus tests y su **ensayo sin API** (un `python <módulo>.py` que
imprime lo que produciría, como `curiana_mundo.py` imprime las 126
combinaciones). Ninguno gasta API hasta el PR de run.

| # | PR | Qué entra | Tests | Ensayo sin API | Días | Serie / brazo |
|---|---|---|---|---|---|---|
| **1** | `escena: la tabla, en datos` | fusiona `escena_por_lugar_propuesta_*.yaml` decidido, + `generar_escena.py` (módulo generado, patrón de `generar_agentes_era2.py` con `--check`) | cobertura 63/63 en los 3 períodos; toda plantilla resuelve; ningún lugar sin sitio | `python 6-fusion/scripts/derivar_escena_por_lugar.py` | 0,5 | ninguno (datos) |
| **2** | `escena: ESTAR` | `curiana_escena.py` (`escena_de`, `ambito_de`, `bloque_aqui_estas`); `run_turn` escribe `ubicaciones_override`; `[Aquí estás]` sustituye a `[Tu ubicación]` | **la era 1 byte a byte** (prompt idéntico con y sin el módulo); tope 200 en las 63 × 6 × 3 combinaciones; `ambito_de` devuelve `None` en CURIANA | `python curiana_escena.py` imprime las 1.134 escenas y su largo | 1 | serie C, brazo `escena` |
| **3** | `escena: la base` | migración `presencias` + `agent_responses.lugar`; `save_presencias()`; `analizar_nodos.py --lugar` | el mock escribe y lee; 378 filas por día; un run sin escena no escribe nada | `analizar_nodos.py --lugar` sobre un run viejo (no hay lugar: avisa y sigue) | 0,5 | — |
| **4** | `escena: OÍR` | `ambito` en `LexicoComunitario`, `CampoLexico`, `CompetenciaLexica` y `vocabulario_para_agente`; bloque `[Lo que se dijo aquí]` | la era 1 byte a byte con `ambito=None`; adopción por ámbito; tope 280; el bloque trae el momento ANTERIOR | `python curiana_escena.py --oir` reconstruye el bloque de un run guardado | 1,5-2 | serie C, brazo `escena` |
| **5** | `escena: el control` | `--escena/--sin-escena`, sellado en `config`; `curiana_cadena` no mezcla brazos | una cadena con escena y otra sin ella no se unen; la config lo dice | `--dry-run` imprime la config resuelta | 0,5 | los dos brazos |
| **6** | *(run)* **serie C, 3 días × 2 brazos** | — | — | — | 0 código | `era2-c`, semillas iguales |
| **7** | `escena: HUELLA` | `hizo_hoy` al estado con lugar; huella derivada en el observer; `Lo que pasó:` al Director; referentes con locación | `--continuar` hereda `hizo_hoy`; el scorer no se mueve (test de `capas_de_score`); tope 180 + 150 | `python curiana_escena.py --huella` sobre un run guardado | 2 | serie C, brazo `escena+huella` |
| **8** | `escena: el visor de texto` | volcado de la escena al log por turno | el volcado no rompe `--silencioso` | el propio log | 0,2 | — |
| **9** | `escena: POTESTAD` | `potestad_de()`; `[A dónde puedes ir mañana]`; validación por pertenencia | nadie va a donde no puede; la era 1 no tiene potestad; tope 200 | `python curiana_escena.py --potestad` imprime la potestad de los 63 | 2 | serie C, brazo `escena+huella+potestad` |
| **10** | `escena: el mapa` | `export_escena_seed.py` + `MapaDeEscena.tsx` en `/kaketiana` | el JSON valida contra el esquema; la página construye sin base | `npm run build` | 1,5-2 | — |
| — | **aparte, hágase o no la escena** | `VINCULOS` y `PRESTIGIO` por `ALIAS_ERA1` (hoy 1 de 63 vivo, y el prestigio pondera la fijación de la koiné) | prestigio propio para los 63 | `python curiana_social.py` | 0,5 | cualquiera |

**Total hasta el primer run comparable (PRs 1-6): ~4 días de código** y 6 días
de API (3 días × 2 brazos). Con huella y potestad, ~8 días de código y 12-16 de
API.

---

*Medido el 2026-09-17 sobre `6-fusion/elenco_era2.yaml` (63 agentes),
`sitios_era2.yaml`, `clima_era2.yaml`, `estructura_social_era2.yaml`,
`3-mundo/corpus/`, `2-lengua/toponimos.yaml` y el código de `curiana_sim/` en
la rama de trabajo. Herramientas:
`6-fusion/scripts/derivar_escena_por_lugar.py` y
`6-fusion/scripts/medir_presupuesto_escena.py`. Ninguna cifra está escrita a
mano.*
