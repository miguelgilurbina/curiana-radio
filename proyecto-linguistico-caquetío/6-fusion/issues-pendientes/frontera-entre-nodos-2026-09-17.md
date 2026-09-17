# La frontera entre nodos: el motor no tiene ninguna

**Para que Miguel decida.** Esto es una medición del motor tal como está y
tres diseños de frontera. **No se implementó nada**: el motor no se toca en
esta tarea.

> La pregunta de la era 2 es si se forma una koiné **entre** GUARANAO y AMUAY,
> dos nodos que «sólo se juntan en el Capubana y por los que se casaron
> cruzando» — así lo dice el bloque `[Tu gente]` que cada agente recibe
> (`curiana_sim/curiana_orchestrator_v2.py:227-229`).
>
> El día 1 limpio de la serie B (run `3973d317`, 2026-09-17) contesta que no
> hay dos nodos que juntar: brecha intra/entre de **0,0154** (ventana) y
> **0,0057** (emergente); de 54 formas clasificables **31 cruzaron** (mediana
> 1 turno, **3 en el mismo turno**), 13 nacieron en los dos nodos a la vez y
> 10 no cruzaron. La serie A ya lo había dicho en el cierre del día 3: «los
> nodos nunca estuvieron separados».
>
> **La sospecha era correcta, pero no por donde parecía.** El contagio social
> —el único sitio donde uno buscaría la frontera— *sí* la tiene, por accidente
> y al 100 %. Lo que no la tiene es el **prompt**: tres bloques de texto que se
> arman una vez para toda la comunidad y se le mandan a los 63.

---

## 1. Lo medido — por dónde cruza una forma, con fichero:línea

Todo lo de esta sección sale de leer el código y de consultar la base sobre el
run `3973d317`. Ninguna cifra está escrita a mano.

### 1.1 El prompt del agente: nadie oye a nadie… salvo por tres bloques globales

El system prompt se ensambla en `curiana_orchestrator_v2.py:391-433`. **No
existe ningún bloque `[Lo que se dijo]`**: `grep` sobre `curiana_sim/*.py` no
encuentra ni uno. Un agente **nunca lee la intervención de otro agente**.

| pieza | dónde | ¿sabe de nodos? |
|---|---|---|
| `AgentMemory` | `curiana_orchestrator_v2.py:252-278`, se escribe en `:908` y `:1347-1351` | sólo guarda **lo que dijo él mismo** — nunca a otro |
| `prompt_gente` — `[Tu gente]` | `curiana_orchestrator_v2.py:208-229` | **sí, y es la única**: dice nodo, casa, sitio, linaje y la frase del Capubana. Es descripción, no mecánica |
| `[Tu tierra]` | `curiana_orchestrator_v2.py:406-411` → `curiana_mundo.bloque_tu_tierra` | sí, por **sitio** (lo único local de verdad) |
| el estímulo del turno | `curiana_orchestrator_v2.py:714-729` | no: los 12 del turno reciben **el mismo** texto |
| `to_context_string` (el mundo) | `curiana_state.py:294-306` | no: un mundo, una situación, una tensión |
| `prompt_idiolecto` / `prompt_emocionar` | `curiana_koine.py:928-946` | no, pero son **por agente** — no cruzan |

Y la **ventana de 12** (`curiana_orchestrator_v2.py:630-640`) es una rotación
sobre el roster: decide **quién habla**, no quién oye. No es un canal.

**Las cuatro vías que sí cruzan** son todas globales, sin partición por nodo:

| # | vía | dónde se arma | dónde se inyecta | a quién |
|---|---|---|---|---|
| **V1** | `[Palabras propuestas en evaluación]` — las últimas **5 propuestas con el nombre de su autor** | `curiana_lexicon.py:7523-7532` (`neologismos_pendientes`, `:7345-7346`) | `curiana_lexicon.py:8755-8756` dentro de `vocabulario_para_agente` | todo **tier ≤ 2** |
| **V2** | `[Palabras nuevas de la comunidad]` — las últimas **15 adoptadas** | `curiana_lexicon.py:7512-7520`; se oficializa con **2 adoptantes cualesquiera** (`LexicoComunitario.adoptar`, `:7307-7330`) y entra en `palabras_activas()` (`:7287-7294`) | `curiana_lexicon.py:8753-8754` | **todos** |
| **V3** | `[La comunidad aún busca nombre…]` — las formas rivales de cada concepto abierto | `curiana_koine.py:1036-1048` | `curiana_orchestrator_v2.py:418-421` | **todos** (salvo `--ablacion`) |
| **V4** | muestreo **rich-get-richer** del lexicón, ponderado por el `CampoLexico` comunitario | `curiana_koine.py:709-737`; se alimenta sin partir por nodo en `curiana_orchestrator_v2.py:805-807` | `curiana_orchestrator_v2.py:369-372` → `curiana_lexicon.py:8475-8490` | **todos** (salvo `--ablacion`) |

Matiz de V4: el muestreo ponderado sólo recorre `VOCABULARIO_BASE`
(`curiana_lexicon.py:8509-8518`), así que empuja la lectura **ventana**, no la
**emergente**. V1, V2 y V3 mueven las dos.

### 1.2 `curiana_social.py`: la única frontera que hay, y está rota

`grep -c nodo curiana_social.py` → **0**. No hay nodos, no hay matriz de
contacto, no hay distancia.

Lo que hay es `vecinos()` (`curiana_social.py:117-142`): vínculos explícitos +
co-ubicación. Medido sobre el elenco activo de la era 2:

```
aristas de vecinos() en el elenco era2:
  intra-nodo: 708 · entre nodos: 0 · a agentes inexistentes: 3
```

- **`VINCULOS` está indexado por los nombres de la ERA 1**
  (`curiana_social.py:101-111`) — el mismo agujero que `FORMAS_SEED`
  (DISENO_KOINE §4). De 63 agentes, **1 clave viva** (Manaure), y sus tres
  destinos (`Nubiri-sha`, `Shaboro`, `Chiriware`) **no existen en el elenco**:
  el agente de más prestigio propaga su habla a tres fantasmas.
- **`PRESTIGIO` igual** (`curiana_social.py:59-69`): sólo Manaure sobrevive.
  Medido: `1.0 ×1 · 0.5 ×16 · 0.4 ×36 · 0.2 ×10` — el prestigio de la era 2 es
  el tier con otro nombre, y es el que pondera la fijación de la koiné
  (`CompetenciaLexica._prestigio`, `curiana_koine.py:987-992`).
- Queda la **co-ubicación** (`PESO_COUBICACION = 0.3`, `:114`) vía
  `agents_at_location` (`curiana_agents.py:619-620`), que compara
  `ubicacion_default`. En la era 2 `ubicacion_default == sitio` y cada sitio
  está en un nodo → **0 aristas entre nodos**.

**Conclusión:** `DifusionLexica` (`curiana_social.py:174-203`) y su bloque
`[Has oído estas palabras nuevas en boca de gente que respetas]`
(`curiana_orchestrator_v2.py:381-389`) **nunca cruzan de nodo**. El motor sí
tiene una frontera — y es la única vía que no la necesita, porque el prompt la
rodea por los otros cuatro lados.

### 1.3 El Director: un narrador para dos nodos, pero hoy no es una vía

`director_narrate` (`curiana_orchestrator_v2.py:475-522`) escribe **un** cierre
por turno para toda la comunidad, y recibe `[La gente que hay hoy]` con los
nombres de los dos nodos mezclados (`:501-504`). Su texto va a
`state.cierres_del_dia` (`:521`) → `reflexion_del_dia`
(`curiana_director.py:97-140`) → `state.notas_orquestador` (`:1401`) → **vuelve
al Director** (`:505-507`).

**No llega al agente:** `to_context_string` no incluye `notas_orquestador`
(`curiana_state.py:294-306`) y `call_agent` no lee ni los cierres ni las notas.
Así que el Director **no es hoy un canal de cruce**; es una incoherencia de
mundo (habla de «la comunidad» donde hay dos) y un canal futuro si algún día se
le inyecta al agente.

### 1.4 La ventana de 12 por turno, medida sobre `3973d317`

| turno | GUARANAO | AMUAY |
|---|---|---|
| D1 T1 amanecer | 10 | 2 |
| D1 T2 mañana | 7 | 5 |
| D1 T3 mediodía | **12** | **0** |
| D1 T4 tarde | 3 | 9 |
| D1 T5 anochecer | 6 | 6 |
| D1 T6 noche | 9 | 3 |
| **total** | **47** | **25** |

Cinco de seis turnos mezclan nodos; uno salió puro GUARANAO. La rotación es
determinista (`_ventana`, `:630-640`) salvo cuando un evento mete primero a sus
protagonistas (`:659-672`): por eso T5 midió 6/6 donde la rotación pura daba
7/5. Reserva: GUARANAO es 39 de 63 del censo (61,9 %) y se llevó el 69,9 % de
los usos del día.

### 1.5 Cuántas veces un agente de AMUAY vio en su prompt algo de GUARANAO

Los prompts no se guardan, pero V1 es una función determinista del orden de
registro, que sí está en la base (`neologisms.created_at` y
`agent_responses.created_at`). Reconstruido bloque a bloque:

```
respuestas de tier<=2 con el bloque no vacío ......... 59
  con al menos una forma de autor del OTRO nodo ..... 34
    AMUAY oyendo a GUARANAO ......................... 22
    GUARANAO oyendo a AMUAY ......................... 12
neologismos del run: 18 (GUARANAO 12, AMUAY 6)
```

Y esto **explica las tres formas que `analizar_nodos.py` marca con Δturnos = 0**
(«mismo turno: 3»). Trazando el orden de habla dentro de D1T1:

| forma | acuña | primer uso fuera del nodo |
|---|---|---|
| `biro-ana` | Simaure [GUARANAO], hablante **8/12** | Tebekoa [AMUAY] **11/12** y Kasebo [AMUAY] **12/12**, mismo turno |
| `duna-rua-ana` | Karebe [GUARANAO], hablante **7/12** | Tebekoa [AMUAY] **11/12**, mismo turno |
| `chaa-da-ma` | Karebe [GUARANAO], hablante **7/12** | Tebekoa [AMUAY] **11/12**, mismo turno |

Tebekoa y Kasebo son exactamente los dos agentes de AMUAY cuyo bloque V1
reconstruido dice, literalmente, *«'biro-ana' (propuesta por Simaure: …)»*.
**El cruce en el mismo turno no es contagio: es el prompt leyendo en voz alta
lo que acaba de decir el otro nodo, con nombre y apellido.**

Las **13 formas «nacidas en los dos nodos a la vez»** tienen su propia puerta:
el evento de nombramiento presenta el mismo referente a los 12 del turno sin
mirar de dónde son (`curiana_orchestrator_v2.py:714-721` y `:1321-1325`), así
que los dos nodos acuñan a la vez por construcción. `kashi-kasuta-iro`, la
única fijada en `koine_lexicon`, la propusieron 2 de GUARANAO y 5 de AMUAY en
el mismo turno D1T5.

### 1.6 Resumen: el reparto de la culpa

| vía | ¿cruza? | cuánto pesa en el día 1 |
|---|---|---|
| V1 propuestas con autor | **sí** | 34 de 59 respuestas; explica los 3 cruces de Δturnos = 0 |
| V2 adoptadas de la comunidad | **sí** | 12 de 18 neologismos llegaron a `adoptado` |
| V3 competencias abiertas | **sí** | la única forma fijada nació multinodo |
| V4 muestreo ponderado | **sí**, sobre el vocabulario base | mueve `ventana`, no `emergente` |
| evento de nombramiento | **sí** | 13 de 54 formas nacen en los dos nodos |
| `DifusionLexica` / prestigio | **no** (0 de 708 aristas) | y encima está desconectada: 1 de 63 nombres vivos |
| Director | no llega al agente | 0 |

---

## 2. Lo que el canon dice del contacto entre esos dos sitios

- **Los dos canales, escritos** — `5-experimento/DISENO_ERA2.md` §4: (1) los
  esposos exogámicos, «contacto continuo, de baja intensidad: cada uno habla su
  variante de origen dentro del nodo del cónyuge»; (2) las ceremonias del
  Capubana, «contacto periódico, de alta intensidad»; (3) **«sin canal
  artificial»**. La frecuencia del canal 2 quedó *«por definir en
  implementación»* — y sigue sin definir.
- **El calendario del merejuy** —
  `6-fusion/estructura_social_era2.yaml` §4 `ciclo_ritual_merejuy`: el ciclo
  mayor CM cae en los **días 55-58 de la seca**, una vez por año simulado
  (120 días), con «subida y convergencia» de las delegaciones y regreso «con
  las formas nuevas». El ciclo menor CL es de contacto **«bajo: solo el agua y
  un emisario cruzan»**. El continuo CC son los esposos y los waitiao.
- **Quiénes son el puente**, del elenco generado
  (`curiana_sim/curiana_agents_era2.py`, medido): **10 agentes** con linaje del
  otro nodo — Kasebo, Duraboa, Dunakoa, Ebokoa (esposos entrantes), Dipopo,
  Mene, Urari, Waranaro (esposas del apopo del otro nodo), Karebe (esposa
  principal traída del otro nodo) y Kumarawa (cuarta esposa del Manaure, de
  Carirubana). **6 de ellos están en el roster**, que es lo que el propio
  elenco declara como `portadores_entre_nodos_en_el_roster`.
- **Los nodos son canon** — `3-mundo/asentamientos.yaml` nodo-027 (Moruy):
  «asiento de los Amuayes tras el reasentamiento desde Cayerda»; «los indios de
  Moruy eran los más belicosos de Paraguaná … sus peleas por la tierra»; «uno
  de los dos nodos de la era 2». Y nodo-025 (Cayeruba/Cayerúa) es «el primer
  asiento de los Amuayes».
- **Pero la esfera avisa contra el muro** —
  `3-mundo/esfera-de-interaccion.md` §2.1, citando a Antczak et al. 2017 p. 157:
  «las fronteras espaciales entre hablantes caribes, arahuacos y otros no deben
  considerarse impermeables». La regla 4 de `CLAUDE.md` dice lo mismo por el
  otro lado: la unidad es **la esfera**, no una comarca.

**⚠ La geografía no sostiene un muro binario.** Distancias entre los sitios del
elenco, calculadas de las coordenadas del propio canon
(`curiana_agents_era2.SITIOS`):

```
ENTRE NODOS:  Moruy-Caseto 7.6 km · Caseto-Capubana 9.4 · El Cayude-Caseto 9.4
              ... Tacuato-Carirubana 41.1
INTRA-NODO:   Moruy-Capubana 3.4 · Tacuato-El Cayude 12.7 · Caseto-Carirubana 23.2
media intra 14.7 km · media entre 22.2 km
```

**Moruy y Caseto son de nodos distintos y están a 7,6 km; Tacuato y El Cayude
son del mismo nodo y están a 12,7 km.** Una frontera binaria nodo-contra-nodo
contradice el mapa. Si se pone, se pone declarada como `canon-simulacion` — o
mejor, se pone por **sitio y distancia**, que es lo que el canon aguanta.

---

## 3. Tres diseños. Ninguno implementado

Para los tres vale lo mismo, y es la línea roja:

> **No se toca el scorer.** `score_linguistico()`, `pct_*` y `capas_de_score`
> quedan idénticos. La frontera cambia **lo que el agente ve**, nunca con qué
> se le puntúa — es la misma regla que gobierna los perfiles
> (`5-experimento/disenos/05_perfiles_de_run.md`, y el test que la vigila).
> Tampoco se tocan: `curiana_observer` (el registro), el catálogo de eventos,
> `curiana_mundo`, el elenco generado ni `word_uses` / `koine_metrics` como
> esquema. Y una frontera **no puede entrar a mitad de cadena**: es un brazo
> nuevo, con su cadena desde el día 1 (`--serie`).

### Diseño A — la palabra circula por nodo; el Capubana la mezcla

**Qué es.** Las cuatro vías globales pasan a tener una copia por nodo. El
agente ve las propuestas, las adoptadas, las competencias abiertas y la
frecuencia comunitaria **de su nodo**. En el turno del Capubana —uno de los
seis momentos, o un día de cada N— ve las dos.

**Qué cambia en el motor.**
- `curiana_lexicon.py`: `prompt_pendientes_evaluacion` (`:7523`) y
  `prompt_lexico_activo` (`:7512`) reciben un `ambito` y filtran por el nodo
  del autor / de los adoptantes; `vocabulario_para_agente` (`:8709`) lo pasa.
  `LexicoComunitario` (`:7258`) guarda el nodo del proponente y de cada
  adoptante — la oficialización con 2 adoptantes (`adoptar`, `:7307`) pasa a
  ser por nodo, con una vía de «adoptada en los dos» que es justo lo que
  queremos ver nacer.
- `curiana_koine.py`: `CampoLexico` (`:709`) pasa a `{nodo: pesos}`;
  `CompetenciaLexica` (`:975`) guarda el nodo de cada proponente y
  `prompt_competencias` (`:1036`) filtra.
- `curiana_orchestrator_v2.py`: `call_agent` (`:296`) resuelve el nodo del
  agente una vez y lo pasa a las cuatro; `run_turn` (`:805-807`) registra en el
  campo del nodo del hablante; el evento de nombramiento (`:714-721`) pasa a
  presentarse **a un nodo por vez**, salvo en el turno del Capubana.
- Una función nueva y sola: `es_turno_de_capubana(state)` — el momento y la
  cadencia, leídos del canon (`estructura_social_era2.yaml` CM/CL/CC), no
  cableados.

**Qué debería moverse en `analizar_nodos.py`.** Es el diseño que ataca lo
medido, así que aquí está la predicción falsable:
- **`mismo turno: 3` → 0.** Si V1 deja de cruzar y sigue habiendo cruces en el
  mismo turno, el diagnóstico de §1.5 está mal.
- **`Δturnos` mediana 1 → ≥ la cadencia del Capubana.**
- **`multinodo 13` → ~0** en los días sin Capubana (el nombramiento deja de ser
  simultáneo).
- **`exclusiva` 10 y `inclinada` 13 suben; `compartida` 31 baja.**
- **brecha intra/entre**: hoy 0,0154 (ventana) y 0,0057 (emergente) — debería
  abrirse el día 1 y **cerrarse después de cada Capubana**. Ese diente de
  sierra, y no el nivel absoluto, es la firma de la koineización entre nodos.

**Coste.** El mayor de los tres: toca tres módulos y la clase que guarda el
léxico comunitario. Estimación honesta: **1-2 días**, la mitad en los tests
(hay que probar que la era 1 sigue byte a byte, donde `nodo` es `None`).

### Diseño B — matriz de contacto en `curiana_social`, con los casados de puente

**Qué es.** `vecinos()` deja de ser «vínculos + misma ubicación» y pasa por una
matriz de contacto: intra-nodo 1,0; entre nodos `p` pequeño; y los 10 portadores
del §2 con `p` alto hacia su nodo de origen — son el puente que el canon escribió.

**Qué cambia en el motor.**
- `curiana_social.py`: una `MATRIZ_CONTACTO` nueva; `vecinos()` (`:117`) la
  aplica como multiplicador del peso; `VINCULOS` (`:101`) y `PRESTIGIO` (`:59`)
  se resuelven por `ALIAS_ERA1` — **esto hay que hacerlo igual, con frontera o
  sin ella**: hoy 62 de 63 agentes no tienen ni vínculo ni prestigio propio, y
  el prestigio es lo que pondera la fijación de la koiné.
- Nada más. `DifusionLexica` (`:162`) no cambia de forma.

**Qué debería moverse.** Casi nada, y **ese es el hallazgo**: `vecinos()` ya da
**0 aristas entre nodos**, así que la matriz con `p` pequeño confirma lo que ya
pasa. Lo que B mueve de verdad es otra cosa: revivir `VINCULOS`/`PRESTIGIO`
cambia **quién** gana las competencias (`CompetenciaLexica._prestigio`) y a
quién se le sugiere qué, y **da a los 10 portadores su primer papel mecánico**.
En `analizar_nodos.py` se vería en el `acuñó` de las formas fijadas y en el
`cruce` de las que hoy no cruzan (10). La brecha intra/entre **no se moverá**.

**Coste.** **Medio día**, casi todo en `curiana_social.py`. Es el diseño barato.

**Reserva.** Con `ubicacion_default == sitio`, una matriz *por nodo* ignora que
Moruy y Caseto están a 7,6 km. Si se hace B, hágase **por sitio** con la
distancia de `SITIOS` — el dato ya está en el módulo generado.

### Diseño C — el Director narra por nodo

**Qué es.** Dos cierres por turno, uno por nodo, cada uno viendo sólo las
intervenciones de su gente; y en el turno del Capubana, uno solo.

**Qué cambia en el motor.**
- `curiana_orchestrator_v2.py`: `director_narrate` (`:475`) se llama una vez por
  nodo con `interactions` particionadas; `[La gente que hay hoy]` (`:501-504`)
  ya sería del nodo.
- `curiana_director.py`: `reflexion_del_dia` (`:97`) por nodo, y
  `state.notas_orquestador` pasa a `{nodo: nota}` (`curiana_state.py:190`).
- Coste API: **×2 llamadas de Director por turno** (y ×2 la reflexión).

**Qué debería moverse en `analizar_nodos.py`.** **Nada.** Lo dice §1.3: el
Director no llega al prompt del agente. C arregla la *coherencia del mundo* —
hoy un narrador dice «la comunidad» donde hay dos y nombra a gente de los dos
nodos en la misma frase— y prepara el terreno por si algún día su cierre se le
inyecta al agente. Pero no es una frontera lingüística.

**Coste.** **Medio día** de código y el doble de gasto de Director por turno.

---

## 4. Qué recomiendo

1. **A, y A primero.** Es el único de los tres que toca lo que está medido: las
   cuatro vías que cruzan son de prompt, no de red social.
2. **B no sustituye a A**: `vecinos()` ya da 0 aristas entre nodos. B con `p`
   pequeño no movería la brecha ni un punto.
3. **C no mueve ninguna métrica de nodo**, porque el Director no llega al agente.
4. Pero **la mitad de B hay que hacerla igual**: `VINCULOS` y `PRESTIGIO` por
   `ALIAS_ERA1`. Hoy 62 de 63 agentes no tienen prestigio propio, y el prestigio
   pondera la fijación de la koiné: es el mismo agujero que DISENO_KOINE §4 ya
   cerró para las semillas, en el módulo de al lado.
5. **La frontera se declara `canon-simulacion`, no se deduce del mapa**: Moruy y
   Caseto son de nodos distintos y están más cerca que Tacuato y El Cayude.
6. **Y va como brazo, no como parche**: una cadena con frontera contra una sin
   ella, misma semilla. La evidencia es la diferencia — la misma lógica de
   `--ablacion`.

### Cuántos días de cadena harían falta

- **Mínimo técnico: 2 días.** `analizar_nodos.py` dice «datos insuficientes» con
  uno (lo dice hoy, sobre `3973d317`), y `curiana_cadena.py` necesita dos días
  cerrados para emitir veredicto.
- **Para ver la frontera: 3 días.** Basta para que `mismo turno` caiga a 0,
  `multinodo` se desplome y `exclusiva`/`inclinada` suban — son efectos del
  día 1, inmediatos.
- **Para ver la koiné *entre* nodos: 6-8 días encadenados.** Hacen falta al
  menos dos Capubana para tener dos dientes de la sierra, y el nombramiento
  tarda ~7 días en agotar los 10 `REFERENTES_NOVEDOSOS` con la cadencia de 4
  turnos (`curiana_orchestrator_v2.py:1251`) y 6 turnos por día.
- **Con brazo de control: el doble.** 12-16 días de API entre las dos cadenas.
- ⚠ El CM del canon cae en los **días 55-58 de la seca** — inalcanzable en una
  cadena de 8. La cadencia del Capubana en el motor tendrá que ser un parámetro
  declarado (`--capubana-cada N`), no el calendario literal, y decirlo en la
  config del run como se dice el perfil.

---

## 5. Lo que no toca ninguno de los tres

`score_linguistico()` · `pct_caquetio` y los demás `pct_*` · `capas_de_score` ·
`curiana_observer` · el catálogo de eventos y `decir_para_el_mundo` ·
`curiana_mundo` y `[Tu tierra]` · el elenco generado · el esquema de
`word_uses`, `koine_metrics` y `koine_lexicon` · la era 1, que tiene que seguir
byte a byte (allí `nodo` es `None` y las cuatro vías deben quedar globales).

---

*Medido el 2026-09-17 sobre el run `3973d317` (serie B, día 1) y sobre el
código de `curiana_sim/` en `main` a esa fecha. Herramienta:
`python analizar_nodos.py --run 3973d317`.*
