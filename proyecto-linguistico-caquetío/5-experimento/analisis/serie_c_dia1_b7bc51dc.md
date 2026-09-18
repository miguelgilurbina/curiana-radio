---
tipo: analisis
ambito: el día 1 de la serie C — el primer día con el LUGAR como ámbito
herramienta: 6-fusion/scripts/medir_cruce_kali_bana.py · curiana_sim/analizar_nodos.py --lugar
medido: 2026-09-18
base: supabase local (docker), run b7bc51dc (era2-c, día 1, semilla 21)
estatus: medición de un run (n = 1 día, sin brazo de control) — no confirma nada por sí solo
---

# El día 1 de la serie C — ¿viajó algo, o sólo lo parece?

> Todo lo de abajo lo imprimen `6-fusion/scripts/medir_cruce_kali_bana.py` y
> `curiana_sim/analizar_nodos.py --run b7bc51dc --lugar`. Ninguna cifra está
> escrita a mano. El motor **no se tocó**: esto es medición.

El run `b7bc51dc` es el primer día en que el ámbito de lo que un agente **ve**
es el LUGAR (capa 2 del diseño `existir-en-el-mundo-escena-por-lugar-2026-09-17`,
§2). Al cerrar dejó tres cosas que piden explicación: una forma **adoptada en
dos ámbitos** (`kali-bana`), una competencia **sin fijar** con tres rivales, y
**29 formas nacidas en varios lugares a la vez**. Este informe contesta las
tres, y la respuesta de las tres es la misma: **lo que parece circulación es, en
su mayor parte, el instrumento**.

---

## 0 · Qué se midió

| campo | valor |
|---|---|
| run | `b7bc51dc` · 2026-09-18 05:28 UTC |
| serie / elenco / perfil | `era2-c` · `era2` (63) · `era2` |
| brazo | `--escena` · `capubana_cada` 3 · semilla 21 · `continuado_desde` `null` |
| ventana | 12 agentes/turno · 6 turnos/día · roster `todos` (63) |
| motor | `5770de66`, árbol limpio |
| filas | 72 respuestas · 378 presencias · 1.851 `word_uses` · 39 neologismos · **0** en `koine_lexicon` |
| `agent_responses.lugar` | escrito en 72 de 72 · discrepan de `presencias`: 0 |
| lugares con nodo | 28 · **compartido por los dos: `camino:Moruy-Caseto`** (3 turnos) |

Y lo que `analizar_nodos.py --lugar` cierra sobre el día:

```
231 formas emergentes ubicables
 72 salieron de su lugar · 149 murieron en él · 29 nacieron en varios a la vez
 turnos hasta salir: mediana 2 · mínimo 1 · máximo 5 · MISMO TURNO: 0
 pasaron por un lugar compartido: 8
```

**Los tres cruces de Δturnos = 0 de la serie B se fueron a cero.** Es la
predicción del diseño §5.1 y se cumplió: V1 dejó de leer en voz alta lo que el
otro lugar acababa de decir.

---

## 1 · `kali-bana` — ni viajó ni se re-acuñó: **estaba en el prompt**

### 1.1 · El hallazgo, en una línea

`kali-bana` es el **EJEMPLO literal** del bloque `_IDENTIDAD_LINGUISTICA`, que
va en el system prompt de **los 63, todos los turnos**
(`curiana_sim/curiana_orchestrator_v2.py:156-171`, línea **161**):

```
EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni. [kali-bana: kali+-bana = cerro del sol]."
```

El propio motor ya lo sabe: `kali-bana` está en `_FORMAS_EXCLUIDAS`
(`curiana_orchestrator_v2.py:178-183`, 5.898 formas), el conjunto que declara
«lo que las plantillas ENSEÑAN» y que se descuenta de la métrica emergente
precisamente para que copiar el prompt no cuente como koiné.

### 1.2 · Quién la dijo, dónde y **en qué orden dentro del turno**

Del texto de las respuestas, con frontera de palabra (`kali-bana-ka` y
`kali-bana-iro` **no** cuentan) y ubicado por `presencias`:

| d/t | orden en el turno | agente | lugar | nodo | veces | ¿en `word_uses`? |
|---|---|---|---|---|---|---|
| d1t1 | **2.º** | **Sawaka** | **Capubana** | GUARANAO | 1 | **no** |
| d1t1 | **8.º** | **Simaure** | Moruy | GUARANAO | 3 | sí |
| d1t2 | 5.º | **Dakawa** | **Carirubana:taller_canoas** | **AMUAY** | 1 | **no** |
| d1t3 | 11.º | Harifuche | Moruy | GUARANAO | 1 | **no** |
| d1t3 | 12.º | Hiko | Moruy | GUARANAO | 1 | sí |
| d1t4 | 1.º | Kumarawa | Moruy | GUARANAO | 1 | sí |
| d1t4 | 3.º | Buriche | Moruy | GUARANAO | 1 | sí |
| d1t5 | 11.º | Chuchubi | El Cayude | GUARANAO | 2 | sí |
| d1t6 | 9.º | Karebe | Moruy | GUARANAO | 1 | sí |
| d1t6 | 11.º | Apoaure | Moruy | GUARANAO | 2 | sí |
| d1t6 | 12.º | Sawaka | Capubana | GUARANAO | 2 | sí |

10 agentes, **4 lugares** (Capubana, Carirubana:taller_canoas, El Cayude,
Moruy). Y el dato que rompe la historia del viaje:

> **Sawaka la dijo en el Capubana el 2.º del turno 1 — seis intervenciones
> ANTES de que Simaure la propusiera en Moruy (8.ª).** En el primer turno en
> que suena, ya suena en **dos lugares**.

Sawaka: «Tüshi-bana o **kali-bana**… nüma raka-da ma-maa-ni, yama».
Simaure, seis turnos de habla después: «…naa-da saa **kali-bana** [kali-bana:
kali + bana = la cumbre del sol]…», que es el ejemplo del prompt con la glosa
cambiada («cerro del sol» → «la cumbre del sol»).

`word_uses` **no ve** tres de las once apariciones (Sawaka t1, Dakawa t2,
Harifuche t3): mientras la forma está en `propuesto` no es una
`palabra_activa`, no entra en `palabras_caquetias` y no deja fila (CLAUDE.md,
«una forma recién acuñada no es una `palabra_activa`»). Por eso
`analizar_nodos --lugar` la fecha «nació en Moruy, salió d1t5, Δ4 turnos» y a
nivel de nodo la clasifica **`exclusiva→GUA` con 0 hablantes de AMUAY** — con
el hablante de AMUAY (Dakawa) invisible en la tabla que lo mediría.

### 1.3 · Las vías, una por una, para cada usuario

`ambito_de(agente, state)` es la puerta única, y el filtro se aplicó bien. Lo
que cada uno **podía ver** (V1 reconstruida como `neologismos_pendientes(ambito)`
con el corte del motor, V2 como `neologismos_adoptados(ambito)`, V4 como
`CampoLexico.pesos_de(ambito)`, y `[Lo que se dijo aquí]` reconstruido con
`curiana_escena.frase_dicha` + `dichos_aqui` sobre las respuestas del momento
anterior):

| d/t | agente | lugar | V1 trae la forma | V2 | V4 peso en su lugar | oyó aquí | ¿la oyó? |
|---|---|---|---|---|---|---|---|
| d1t1 | Sawaka | Capubana | · | · | 0,97 | 0 | **no** |
| d1t1 | Simaure | Moruy | · | · | 5,48 | 0 | **no** |
| d1t2 | **Dakawa** | **Carirubana:taller_canoas** | **·** | **·** | **0,0** | **0** | **no** |
| d1t3 | Harifuche | Moruy | **sí** | · | 5,48 | 0 | no |
| d1t3 | Hiko | Moruy | **sí** | · | 5,48 | 0 | no |
| d1t4 | Kumarawa | Moruy | · | sí | 5,48 | 3 | **SÍ** |
| d1t4 | Buriche | Moruy | · | sí | 5,48 | 3 | **SÍ** |
| d1t5 | Chuchubi | El Cayude | · | · | 0,94 | 0 | no |
| d1t6 | Karebe | Moruy | · | sí | 5,48 | 1 | no |
| d1t6 | Apoaure | Moruy | · | sí | 5,48 | 1 | no |
| d1t6 | Sawaka | Capubana | · | · | 0,97 | 0 | no |

(V4 «peso» es el del cierre, no el del instante: se lee como «cuánto pesa la
forma en ese lugar al final del día», no como lo que el muestreador vio.)

Y las puertas que el diseño **no cuenta entre las cuatro vías**:

- **La quinta vía — el contagio léxico.** `DifusionLexica` inyecta
  «[Has oído estas palabras nuevas en boca de gente que respetas]»
  (`curiana_orchestrator_v2.py:413-422`) y **no recibe ámbito**: viaja por
  `curiana_social.vecinos()` = vínculos resueltos + co-ubicación. Reconstruida
  con el mismo modelo del motor (`prestigio_de(hablante) × peso_del_vínculo`,
  umbral 0,6): la exposición de **Dakawa** a `kali-bana` antes de hablar era
  **0,000** —no es vecino de Simaure— y la de los de Moruy, **0,255**, por
  debajo del umbral. **A nadie se le sugirió.** La vía existe y está abierta,
  pero este día no disparó.
- **La sexta puerta — el detector de adopciones.**
  `curiana_observer.procesar_adopciones` recorre
  `lexico.neologismos_pendientes()` **sin ámbito**
  (`curiana_lexicon.py:7418-7427`, y está declarado: «lo que el ámbito filtra
  es lo que el agente VE (V1), no lo que puede adoptar»). Consecuencia
  medida: Dakawa dice `kali-bana` en Carirubana:taller_canoas **por su cuenta**
  y queda registrado como **adoptante 1** de la propuesta de Moruy; Harifuche,
  en Moruy y con V1 delante, es el **adoptante 2**; `adoptar()` ve dos lugares
  distintos y escribe `via = "dos-ambitos"` — la vía «alguien la llevó». Nadie
  la llevó.
- **La séptima puerta — la memoria propia y el idiolecto.** `AgentMemory`
  guarda sólo lo que dijo uno mismo, y `[Tu manera de hablar]`
  (`curiana_koine.py:1008-1017`) resume su idiolecto acumulado: «sueles decir:
  …; **acuñaste:** …». **Ninguno de los dos recibe ámbito**, y por construcción
  no pueden: son del agente, no del lugar. Es la vía por la que una forma **sí**
  viaja en el motor de hoy —el agente la lleva encima— y es la que va a decidir
  el día 3 (§2.3). Aquí no explica nada: ni Sawaka ni Dakawa tenían `kali-bana`
  en su idiolecto antes de decirla.
- **El Director y el catálogo de eventos: descartados.** Lo que el Director
  narra no llega al prompt del agente (`to_context_string` no incluye
  `cierres_del_dia` ni `notas_orquestador`), y el evento que sí llega —
  `[Situación del turno]`, dentro de `world_context` — es **el mismo para los
  63**: puede explicar que todos hablen del buko, no que una forma aparezca en
  un lugar y no en otro. Los dos eventos del día están en la §5.6.

### 1.4 · ¿Es re-acuñable de forma independiente?

Sí, y por partida doble:

| pieza | en `VOCABULARIO_BASE` | la enseña una plantilla del prompt |
|---|---|---|
| `kali` (sol) | sí | sí |
| `bana` (`-bana` cerro, sitio alto) | sí | sí |

`kali` + `-bana` son dos morfemas que el prompt enseña a **todos**, y además el
compuesto **ya viene armado en el ejemplo**. No hace falta que viaje: basta con
que dos agentes lean el mismo prompt.

### 1.5 · Veredicto

> **NO VIAJÓ, Y TAMPOCO ES UNA RE-ACUÑACIÓN INDEPENDIENTE INTERESANTE: ES
> COPIA DE LA PLANTILLA.** La `via = "dos-ambitos"` de `kali-bana` es un falso
> positivo del instrumento, no el primer viaje medido.

Lo sostienen cuatro cosas, cada una suficiente por sí sola:

1. La forma está literalmente en el system prompt de los 63, y el propio motor
   la tiene en `_FORMAS_EXCLUIDAS`.
2. Sonó en dos lugares en el turno 1, y el primero en decirla (Sawaka, 2.º) lo
   hizo **antes** de que existiera la propuesta (Simaure, 8.ª).
3. Ninguna de las cuatro vías por ámbito la llevó a Carirubana:taller_canoas:
   V1 vacía, V2 vacía, V4 en 0,0, `[Lo que se dijo aquí]` vacío (a ese taller
   no había ido nadie el turno anterior).
4. La quinta vía —el contagio, que **sí** cruzaría— dio exposición 0,000 para
   Dakawa.

La única circulación real y fechable que hubo fue **dentro de Moruy**: el
bloque `[Lo que se dijo aquí]` del turno 4 llevó a Kumarawa y a Buriche lo que
Harifuche y Hiko habían dicho en el turno 3, en el mismo sitio. Eso es la capa
2 funcionando. Lo otro es el ejemplo del prompt volviendo por la puerta de
atrás.

### 1.6 · Qué habría que registrar para poder decidirlo la próxima vez

Sin implementar nada — es una lista para que Miguel decida:

1. **Guardar el bloque comunitario que vio cada agente.** Una columna
   `vias_vistas jsonb` en `agent_responses` (o una tabla `prompt_vias`) con las
   formas de V1, V2, V3, el contagio, el idiolecto y `[Lo que se dijo aquí]`
   **tal y como se armaron**. Hoy todo eso se reconstruye a posteriori y la
   reconstrucción es una hipótesis: con el bloque guardado, «¿pudo verla?» deja
   de discutirse.
2. **Registrar los usos que `word_uses` no ve.** 16 apariciones de un
   neologismo en el texto sobre 11 formas no dejan fila, porque mientras la
   forma está en `propuesto` no es `palabra_activa`. Sin ellas, «salió de su
   lugar en el turno N» está sistemáticamente retrasado — `kali-bana` fue el
   caso extremo (Δ4 turnos medidos sobre un cruce que fue Δ1).
3. **Excluir de la acuñación lo que la plantilla ya enseña.**
   `registrar_neologismo()` (`curiana_lexicon.py:7346-7358`) no comprueba
   `_FORMAS_EXCLUIDAS`; `formas_emergentes()` (`analizar_nodos.py:449-452`) las
   devuelve al conjunto emergente *por ser neologismo registrado*. Dos formas
   del día entraron así: `kali-bana` y `warawara`. Un guardián barato: un test
   que afirme que ningún neologismo registrado está en `_FORMAS_EXCLUIDAS`.
4. **Declarar el orden de habla.** `agent_responses` se ordena por
   `created_at`; un `orden_en_el_turno` explícito haría trivial la pregunta
   «¿quién lo dijo primero?», que aquí fue la que decidió el caso.
5. **Decidir si `procesar_adopciones` debe respetar el ámbito.** Hoy no lo
   respeta a propósito, y por eso `via = "dos-ambitos"` puede nacer sin que
   nadie haya llevado nada. Si se quiere que esa etiqueta signifique lo que
   dice, la adopción tiene que exigir que el adoptante **pudiera ver** la
   propuesta (V1 en su ámbito, o el bloque de oír, o el contagio) — y si no la
   veía, registrarla como **coincidencia**, que es una tercera vía y es un
   dato, no un error.

---

## 2 · La disputa de las cuentas tiene geografía — y cada nodo va a la suya

El evento de nombramiento cayó en el **turno 5** (cadencia 4) con el referente
`cuentas_vidrio`, «unas cuentas brillantes y duras que un mercader trajo de
tierras lejanas». Salieron **16 variantes rivales**, una por acuñación del
turno. Ninguna se fijó: `koine_lexicon` del run está **vacío**.

`CompetenciaLexica` **no se persiste** (`guardar_koine()` escribe idiolectos y
campo, nada más), así que el soporte se reconstruye re-ejecutando el modelo del
motor sobre lo que la base guardó: `proponer` = 1,0 + prestigio,
`registrar_uso` = 0,5 + prestigio, descontando que lo que un agente acuña no es
`palabra_activa` en su propio turno. La reconstrucción reproduce las cifras del
cierre.

### 2.1 · Las tres rivales

| forma | soporte | la propuso | la reusó | lugar(es) | nodo | `pesos_de(lugar)` |
|---|---:|---|---|---|---|---:|
| **`kali-uco-aima`** | **3,65** | Chirwa, Chakamba (t5) | Patapati (t6) | **Tacuato** | **GUARANAO** | Tacuato **2,8518** |
| **`ucibo-kali-duruco`** | **3,45** | Arika, Talata (t5) | Tigi (t6) | **Carirubana** | **AMUAY** | Carirubana **2,8518** |
| **`kali-boro`** | **2,80** | Tauta ×2 (t5) | — | **Carirubana** | **AMUAY** | Carirubana **1,8818** |

Quién las dijo, turno a turno (texto, con frontera de palabra):

- `kali-uco-aima` — t5 Chirwa, t5 Chakamba; t6 Birokoa, t6 Patapati. **Cuatro
  bocas, un solo lugar: Tacuato.**
- `ucibo-kali-duruco` — t5 Arika, t5 Talata; t6 Waru, t6 Tigi. **Cuatro bocas,
  un solo lugar: Carirubana.**
- `kali-boro` — t5 Tauta, y nadie más. **Una boca, Carirubana.**

Las trece restantes no salieron de su lugar de acuñación y ninguna llega al
soporte de las tres: `kali-rua` (Manaure, Moruy, 2,00), `susü-kiba` y
`bira-susü-ana` (Sawaka, Capubana, 2,00 cada una), `ishasü-bana-kuna` (Cege,
El Cayude, 1,70), `kari-biro-tabi` / `kua-biro-kana` / `kari-jaro-ima` (Ebokoa,
Carirubana:orilla, 1,45 cada una), `ishasü-kuna-ubana` y `piki-ishasü`
(Chuchubi, El Cayude, 1,35), `kali-uco-iro` (Chirwa, Tacuato, 1,30),
`kali-bana-iro`, `barsure-ana` y `kali-bana-iro-kana` (Ucibo, Tacuato:orilla,
1,30 cada una).

**Soporte total 29,85 · el líder se lleva el 12,2 %.** El umbral de fijación es
el **55 %** con soporte mínimo 3,0: la competencia no está cerca de resolverse,
y no porque las rivales estén empatadas sino porque las 16 variantes se
acuñaron en **siete ámbitos distintos** —Tacuato, Carirubana, Moruy, Capubana,
El Cayude, Carirubana:orilla y Tacuato:orilla— y ninguna llega a la mitad de
nada.

### 2.2 · ¿Cada nodo va camino de fijar una distinta?

**Sí, y el campo léxico ya lo dice: ninguna de las tres rivales tiene peso
fuera de su lugar.** `kali-uco-aima` existe en Tacuato y sólo en Tacuato;
`ucibo-kali-duruco` y `kali-boro`, en Carirubana y sólo ahí. GUARANAO va hacia
`kali-uco-aima`; AMUAY tiene una disputa **interna** entre `ucibo-kali-duruco`
(2,85) y `kali-boro` (1,88) que se resuelve dentro de Carirubana, sin que
Tacuato se entere.

Es exactamente lo que la capa 2 tenía que producir: **dos campos léxicos
paralelos**. Y es también su factura: sin puerta entre lugares, ninguna de las
dos gana nunca.

### 2.3 · Predicción medible para el día 2 (víspera) y el día 3 (Capubana)

Con `--capubana-cada 3`: el **día 2 es la víspera** y el **día 3 es la
convergencia** (`es_dia_de_capubana`, `curiana_escena.py:133-144`).

**Día 2 — la disputa no se mueve, y el motor no puede moverla.**

1. `koine_lexicon` seguirá **sin fila** para `cuentas_vidrio`. No porque las
   rivales empaten: porque `auto_mode` crea una `CompetenciaLexica()` **nueva**
   aunque se continúe (`curiana_orchestrator_v2.py:1520`), el concepto no se
   hereda, y `referentes_introducidos = ['cuentas_vidrio']` impide que se
   vuelva a presentar. **La disputa de las cuentas está técnicamente muerta el
   día 2.** Si el día 2 aparece una fila `cuentas_vidrio` en `koine_lexicon`,
   esta lectura está mal.
2. Lo único de las tres rivales que sobrevive al cambio de día es (a) su peso
   en `CampoLexico.por_ambito` —Tacuato 2,8518 y Carirubana 2,8518 / 1,8818,
   decayendo a 0,97 por registro— y (b) el `[Tu manera de hablar]` de sus
   cuatro acuñadores, que lleva **`acuñaste: kali-uco-aima`** (Chirwa,
   Chakamba), **`acuñaste: ucibo-kali-duruco`** (Arika, Talata) y
   **`acuñaste: kali-boro`** (Tauta) **a donde vaya el agente**: el idiolecto no
   está partido por ámbito. Es el verdadero vehículo de viaje del motor de hoy.
3. El **único lugar con los dos nodos** el día 2 vuelve a ser
   `camino:Moruy-Caseto`, y ahora con **tres** personas: Bajari (AMUAY) y
   Humohumo (GUARANAO), los dos mensajeros, **más Karebe** (linaje AMUAY,
   casada en Moruy), que la víspera anda el camino de la alianza
   (`curiana_escena_era2.TRAVESIA`). Ninguno de los tres es de Tacuato ni de
   Carirubana: **las rivales no pueden llegar al único lugar de contacto**. Lo
   que Humohumo sí lleva encima es lo suyo: `acuñaste: kali-juro`.
   → Falsable: si el día 2 aparece `kali-uco-aima` o `ucibo-kali-duruco` en
   `camino:Moruy-Caseto`, ha cruzado por una vía que esta medición no ha
   identificado.
4. `analizar_nodos --lugar` del día 2 debería seguir dando **mismo turno: 0**, y
   la mediana de turnos hasta salir ≥ 2.

**Día 3 — el Capubana junta a la gente, pero no junta lo que la gente ve.**

5. Los **63 comparten ámbito `Capubana` los seis momentos**. Lo que ese ámbito
   les ofrece está **heredado del día 1, y es el de sus dos ocupantes** (Sawaka
   y Hayo): `pesos_de('Capubana')` trae **71 formas**, y las tres rivales pesan
   **0,0** en él. V1 en el cerro serán las **dos** propuestas que se hicieron
   allí y siguen pendientes —`susü-kiba` y `bira-susü-ana`, las de Sawaka— y V2
   estará **vacía**.
   → Predicción dura: **el día de Capubana NO re-expone las formas de Tacuato
   ni las de Carirubana.** Lo que se una ese día se unirá porque alguien lo
   diga, no porque el prompt se lo lea.
6. Por tanto, si `kali-uco-aima` y `ucibo-kali-duruco` se encuentran el día 3,
   será por `[Tu manera de hablar]` de sus cuatro acuñadores —si la ventana de
   12 los saca a hablar— y por `[Lo que se dijo aquí]`, que ese día sí tiene a
   los 63 en un solo sitio y debería dispararse en **60 de 72 prompts** (el
   diseño lo estima; es la cifra a comprobar).
   → Falsable: si el día 3 ninguna de las dos aparece en boca de alguien que no
   sea de su lugar, el Capubana **no sirve como puerta** tal y como está
   implementado, y hay que llevar el campo al cerro explícitamente.
7. **`Capubana` y `Capubana:fuente` son dos cadenas distintas** y no se ven
   entre sí: el día 3 los tres que suben a la fuente en la seca quedarían fuera
   del ámbito del cerro. Hoy no muerde (el día 3 manda a los 63 a `Capubana`),
   pero es una costura del diseño que conviene declarar.
8. La brecha intra/entre del día 1 es **0,0040 (ventana)** y **0,0127
   (emergente)**. La firma que el diseño §5.1 pide es el **diente de sierra**:
   que suba los días 1-2 y **baje tras el día 3**. Con un solo día no hay serie;
   con tres, la habrá — y si la brecha **no** cae tras el Capubana, la lectura
   de §2.3.5 (el cerro junta cuerpos, no ámbitos) queda confirmada por partida
   doble.

---

## 3 · Las 29 nacidas en varios lugares: ninguna es del nombramiento, y todas
son morfología

De las 231 formas emergentes ubicables, **29 nacieron en varios lugares a la
vez** (la forma suena en ≥ 2 lugares en el mismo día×turno de su primera
aparición, que es la definición de `analizar_nodos.cruce_por_lugar`).

| origen | cuántas |
|---|---:|
| del **evento de nombramiento** (nacidas en el turno 5) | **0** |
| formas que el prompt ya **enseña** (`_FORMAS_EXCLUIDAS`) | **0** |
| **el resto** | **29** |
| …de ellas, **compuestos transparentes** (todas sus piezas se enseñan a los 63) | **29** |
| …de ellas, sin explicar | **0** |

Reparto por turno de nacimiento: **d1t1 20 · d1t2 3 · d1t3 2 · d1t4 4 ·
d1t5 (el nombramiento) 0**.

**Cero del nombramiento.** Es un resultado del brazo, y es la predicción del
diseño §5.1 cumplida por otra puerta: el evento se presenta a los 12 del turno
en lugares distintos (capa 3 pendiente), pero **cada uno acuñó una forma
distinta**, así que ninguna nació en dos sitios. Las dos coincidencias que hubo
—`kali-uco-aima` en dos bocas y `ucibo-kali-duruco` en dos bocas— ocurrieron
**dentro del mismo lugar** (Tacuato y Carirubana), que es adopción local, no
simultaneidad.

Lo mismo por NODO, para poder contrastarlo con el informe del motor: **17
formas nacieron en los dos nodos a la vez** sobre todas las emergentes
(`analizar_nodos.py` publica **12** porque sólo cuenta las 43 *clasificables*,
las que llegan a tres hablantes), y su turno de nacimiento es **d1t1 12 · d1t2
1 · d1t4 4 · d1t5 0**. El informe por nodo glosa esa cifra como «evento de
nombramiento simultáneo»: **en este run la glosa no aplica** —ninguna nace en
el turno 5—. La etiqueta es una hipótesis heredada del día 1 de la serie B, no
una medición de este día.

**Las 29, una a una, son flexión y derivación del material común**:

```
wana-ni  kaa-ka  wana-da  kaa-da  panaa-da  raka-ni  maa-ka  naba-da  naba-ka
paa-da   ma-wara panaa-ka panaa-ni rua-da   ma-para  masa-da paa-ni   rua-ni
juri-da  ma-biro dichiba-ni juri-ubana kono-kana ma-arua ma-duna siwa-ni
taa-da   taa-ni  wa-para
```

Raíz del `VOCABULARIO_BASE` + un afijo que la plantilla enseña a todos: `-ka`
(completivo), `-ni` (continuativo), `-da` (prospectivo), `ma-` (sin/no), `wa-`
(nuestro), `-ubana`, `-kana`. **20 de las 29 nacen en el turno 1**, antes de que
circulara absolutamente nada. Que `wana-ni` suene el mismo turno en el Capubana
y en el jagüey de Tacuato no es contacto: es que los dos leyeron la misma tabla
de aspectos.

**Conclusión: de las 29, 0 cruzaron. Las 29 son compuestos transparentes
re-acuñados en paralelo.** Y una consecuencia para el instrumento: el umbral de
«forma emergente» deja pasar la flexión regular del vocabulario base, que por
construcción aparece en todas partes a la vez. Si «nacieron en varios lugares»
va a ser una métrica de la escena, tiene que contar **sólo lo no transparente**
— o el número medirá la morfología, no el mundo.

---

## 4 · Los tres avisos que deja el día

1. **`via = "dos-ambitos"` todavía no significa «alguien la llevó».** El único
   caso del run es un falso positivo de plantilla. Antes de leer esa etiqueta
   como evidencia, hace falta el punto 5 de la §1.6.
2. **`word_uses` llega tarde a las formas nuevas.** 16 apariciones sobre 11
   formas no dejan fila; todo Δturnos leído de esa tabla está sesgado hacia
   arriba. El caso medido: Δ4 declarado sobre un cruce real de Δ1 — y en
   dirección contraria a la que la tabla dice.
3. **La competencia léxica no sobrevive a `--continuar`.** Un referente por
   día, una `CompetenciaLexica()` nueva cada día y `referentes_introducidos`
   heredado: **ninguna competencia puede durar más de un día**, y con el ámbito
   repartiendo las variantes en nueve lugares, ninguna competencia de un día
   llega al 55 %. Tal y como está, la serie C **no puede** fijar una entrada de
   koiné por competencia. Es decisión de Miguel si eso se arregla antes del
   brazo de control (§5.4 del diseño) o si la serie se corre así y se mide la
   ausencia.

---

## 5 · Límites de esta lectura

1. **n = 1 día, sin brazo de control.** La evidencia del diseño es la
   DIFERENCIA entre dos cadenas completas con la misma semilla (§5.4). Aquí no
   hay contra qué restar.
2. **V1, V2 y el bloque de oír están RECONSTRUIDOS**, no leídos: el motor no
   guarda lo que cada agente vio. La reconstrucción usa las funciones del propio
   motor y el estado del cierre, pero es una hipótesis sobre un proceso que no
   dejó rastro. Es justo lo que pide arreglar la §1.6.1.
3. **El soporte de competencia está reconstruido** por la misma razón
   (`CompetenciaLexica` no se persiste). Reproduce las cifras del cierre, lo
   que es un control, no una prueba.
4. **La exposición de contagio se reconstruye con `vecinos()` sin el estado del
   turno**, añadiendo la co-ubicación desde `presencias`. El motor la calcula
   sobre `ubicaciones_override`, que `presencias` refleja fila a fila
   (discrepan: 0), así que la diferencia debería ser nula — pero no está
   comprobada turno a turno.
5. **`kali-uco-aima` vs. `kali-uco-iro` y las dos entradas duplicadas de
   `ucibo-kali-duruco` y `kali-boro`** (dos `Neologismo` con la misma forma)
   hacen que el conteo de «variantes» del concepto dependa de si se cuentan
   entradas o formas. Aquí se cuentan **formas** (16).
6. **Lo que un agente oye del Director no llega a su prompt**
   (`to_context_string` no incluye cierres ni notas), así que el Director no se
   consideró como vía. El evento del turno **sí** llega, siempre, dentro de
   `world_context` (`curiana_state.to_context_string:325-326`, línea
   `[Situación del turno]`) y además como mensaje de usuario salvo en el turno
   de nombramiento, donde el estímulo es `[ALGO NUEVO EN PARAGUANÁ]`. El día
   tuvo exactamente **dos** (`turns.event_description`): t1 «El buko baja. Los
   conucos se resienten. Tensión sobre el agua.» y t5 «Manaure convoca ritual
   urgente. Su autoridad teocrática se activa.». **Ninguno nombra ninguna de
   las formas estudiadas**, y los dos son iguales para los 63: un evento no
   puede explicar una diferencia entre lugares.

---

## 6 · Cómo se reproduce

```bash
# la medición de este informe, entera
python 6-fusion/scripts/medir_cruce_kali_bana.py
python 6-fusion/scripts/medir_cruce_kali_bana.py --forma kali-uco-aima
python 6-fusion/scripts/medir_cruce_kali_bana.py --json > cruce.json

# los curiana_*.json del cierre están gitignorados y viven en el checkout donde
# se corrió el run, no en un worktree:
python 6-fusion/scripts/medir_cruce_kali_bana.py --estado-dir <ruta>/curiana_sim

# el informe por lugar del motor
cd curiana_sim
python analizar_nodos.py --run b7bc51dc --lugar
python curiana_escena.py --oir            # los bloques [Lo que se dijo aquí]

# la base, directa
docker exec supabase_db_curiana_sim psql -U postgres -d postgres -Atc "<sql>"
```

Ninguna de las dos herramientas llama a la API ni lee `curiana_sim/.env`:
`medir_cruce_kali_bana.py` saca `_IDENTIDAD_LINGUISTICA` con `ast` para no
importar el orquestador (que arrastraría `curiana_database` y su
`load_dotenv()`) y consulta la base por `docker exec … psql`.

*Relacionado: [[existir-en-el-mundo-escena-por-lugar-2026-09-17]] ·
[[ANALISIS_NODOS_ERA2_2026-09-16]] · [[DISENO_KOINE]] · [[BITACORA_RUNS]] ·
`curiana_sim/curiana_escena.py` · `curiana_sim/analizar_nodos.py`*
