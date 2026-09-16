# El mundo de la era 2, atado a los nodos: sitios y clima

Miguel, 2026-09-14:

> «¿Cómo podemos adecuar y más bien atestiguar información que tenemos en el
> mundo acorde a los nodos de la era 2?» · «Tener una sección de clima y
> temporada, y así cuando inyectamos el mundo lo inyectamos bajo un esquema
> climatológico.»

Esto es lo que salió. Dos archivos de datos, un medidor y este resumen:

| archivo | qué tiene |
|---|---|
| `6-fusion/sitios_era2.yaml` | el mundo por lugar: 7 sitios × 7 dominios, cada línea con procedencia o deuda, etiqueta, capa, estación y voz caquetía o hueco |
| `6-fusion/clima_era2.yaml` | el año: 3 períodos con viento, lluvia, mar, agua dulce y cielo; el día dentro de cada período; qué abre y cierra por sitio; los ritos; y lo que cambiaría en el motor |
| `6-fusion/scripts/verificar_sitios_era2.py` | lo mide y lo valida (regla 1 y regla 8) |

**Ninguna cifra de abajo está escrita a mano.** Las imprime
`python 6-fusion/scripts/verificar_sitios_era2.py --conteos`, en verde.

```
lineas_total 175 · lineas_sitios 107 · lineas_clima 68 · sitios 7
huecos_lexicos 14 · testimonios_miguel 3 · lineas_con_deuda 17
voces_caquetias_citadas 74 · hechos_del_corpus_citados 47 · obras_citadas 11
dias_simulados 120
```

Por etiqueta: **atestiguado 112**, reconstruido 19, canon-simulación 19,
retro-abstraído 18, testimonio-miguel 3, hipotético 4.

> **ACTUALIZADO 2026-09-16.** Miguel respondió las ocho preguntas de §6 una a
> una en la conversación (registro: `6-fusion/decisiones_tanda_2026-09-15.yaml`)
> y todo se aplicó el mismo día: tres períodos 50/40/30 en `curiana_state`
> (p1); períodos sin nombre caquetío (p2); el «yararé» era el **yacaré** —
> caimán— y la laguna de Guaranao tiene ficha (`laguna-guaranao-parque`), con
> lo que tres testimonios subieron a atestiguado-moderno (p3, p8); los diez
> hechos entraron al corpus antes del primer run (p4: ecologia-078 a 084,
> creencia-020 a 022); Caseto siembra y pesca de visita (p5); el Capubana tiene
> las coordenadas del pico (p6); y el cargador `curiana_mundo.py` arma
> `[Tu tierra]` con tope de 320 y test sobre las 126 combinaciones (p7). Los
> conteos de arriba son los de después. Este borrador no se publicó: las
> decisiones se tomaron aquí.

---

## 1. Qué tiene cada sitio

Líneas de canon por sitio y dominio (medido):

| sitio | agua | pesca | recol. | tierra | monte | sal | mater. | **total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Tacuato | 4 | 5 | 3 | 3 | 2 | 2 | 2 | **21** |
| Moruy | 3 | 1 | 3 | 4 | 3 | 1 | 5 | **20** |
| Caseto | 2 | 2 | 2 | 3 | 2 | 1 | 3 | **15** |
| Capubana | 5 | 2 | 1 | 1 | 3 | 1 | 2 | **15** |
| El Cayude | 2 | 3 | 2 | 2 | 2 | 1 | 1 | **13** |
| Carirubana | 1 | 2 | 3 | 1 | 2 | 2 | 1 | **12** |
| laguna de Guaranao *(de fondo)* | 1 | 2 | 1 | 1 | 3 | 2 | 1 | **11** |
| **TOTAL** | **18** | **17** | **15** | **15** | **17** | **10** | **15** | **107** |

**El reparto no es parejo y eso es el hallazgo.** El Golfete (Tacuato, El
Cayude) y el conglomerado del cerro (Moruy, Capubana) tienen dato de recurso
con página. La costa oeste (Caseto, Carirubana) casi no lo tiene: el corpus de
ecología cubre el Golfete y el istmo y **no tiene ni un hecho del Golfo de
Venezuela**. Lo que esos dos sitios pescan se sostiene en la decisión de zonas
del 2026-09-14, declarada como tal.

### Lo mejor de cada sitio

- **Tacuato** — ⭐ la pesca nocturna: «Cunaro […] del cual extraían manteca para
  untar los "jachos", teas de madera, comúnmente de curarí, para encandilar en
  labores de pesca nocturna» (Esteves **p. 33**). El pez da la luz con que se
  pesca el pez. Es la única técnica de pesca con hora del día en todo el repo, y
  `jachos` es voz **caquetío-atestiguada**. Más el Resguardo de Salinas colonial
  (p. 62) y el Caño del Muaco, «una albufera cercana a la población de Tacuato»
  (p. 54).
- **El Cayude** — la ensenada de Cuara en la ribera norteña del Golfete (p. 31)
  y el `waranaro`, «un pez más pequeño que la lisa» (p. 41). ⚠️ Su entrada en el
  gazeteer está **medio destruida en el OCR** (OCR 2, p. 30): deuda de relectura
  del PDF, siendo un sitio en escena.
- **Moruy** — la casa del Manaure es el único sitio **sin zona de pesca** en
  `curiana_agents_era2.SITIOS`: recibe y reparte. A cambio tiene el barro
  («gruesas vetas de barro de loza en los cangilones labrados por la lluvia»,
  p. 11, entrada Abudure), el `warataro` «barro de loza, gomoso, con que fabrican
  budares y ollas» (p. 41), la alfarería viva con silletas, bernegales y jabón de
  la tierra (pp. 52-53), y el merejuy de la chicha (pp. 53-54, etimología del
  autor sin cita → **hipotético**).
- **Caseto** — ⚠️ **tensión declarada**: está a ~22 km de su zona de pesca ZA1.
  La decisión del 2026-09-14 le dio una playa que no tiene a la vista. Lo que sí
  tiene cerca: el **barbasco**, «nombre común a varias plantas cuyas propiedades
  estupefacientes se aprovechan en la pesca» (p. 22), junto a Cocodite.
- **Carirubana** — ⭐⭐ **las dos atalayas de cardúmenes**: Sarabón, «punto costeño
  al Norte de Punta Cardón que sirvió de atalaya a los pescadores para avistar
  (columbrar) los cardúmenes» (p. 58), y Suriquiba, igual, en Punta Cardón
  (p. 61). Es el dato de oficio mejor localizado de toda la costa oeste. Y ⭐ el
  guairón: «los aborígenes para obtener cal con qué pelar el maíz, incineraban
  conchas de almejas; y en este lugar hemos visto señales, antiquísimas y
  abundantes, de los guairones» (p. 28). Cierra el circuito entero: la concha
  hace la cal, la cal pela el maíz, y la misma concha bruñe la olla.
- **Capubana** — ⭐ el cerro es **instrumento de navegación**: la indicación
  «m. alto» del mapa de Juan de la Cosa (c. 1500) «significa […] que navegando por
  ahí observó él un "monte alto", […] porque el monte es el cerro de Santa Ana de
  Paraguaná» (Arcaya **p. 134**). El centro espiritual es también la aguja de
  marear. Y ⭐⭐ **«Las Piedras del Almanaque»**: petroglifos en el cerro de Siraba,
  «unido al cerro de Santa Ana por el lado Noreste» (Esteves **p. 60**) — el único
  objeto del repo que la tradición asocia a un calendario, y está pegado al
  Capubana.
  ⚠️ **Y un cero importante**: Esteves no dice NADA del cerro sobre quebradas,
  agua que baje, nubes, neblina ni bosque de altura. El bosque nublado **no sale
  de esta fuente**: sale de INPARQUES/MINEC (ficha `monumento-cerro-santa-ana`).
- **laguna de Guaranao** — entra como sitio **de fondo** (no está en `SITIOS`)
  porque Miguel la nombró. Carga cuatro de los seis testimonios suyos y las
  salinas «más importantes» de Paraguaná (Arcaya p. 22), con la fama curativa de
  su sal (Esteves p. 41) y su destrucción por aguas cloacales.

### ⚠️ Corrección al canon, de paso

**«La elegía de Coro» no contiene el pasaje de Coro.** Los versos de los
cardones, los hobos, «perdices, conejos y venados», la «grande pesquería de
pescados» y el «largo verano» están en las **líneas 48205-48280**, que caen en la
**INTRODUCCIÓN a la Parte II (47059-48482)** y NO dentro de la Elegía I
(48483-55151), que es el rango con el que el repo venía citando. Y dentro de la
elegía la geografía se desplaza: los cardones, los jaqueyes y las perlas son de
**Maracaibo y la Guajira**, no de la costa caquetía. Dos grafías rompen los greps
del repo: **`zavana`** (nunca *sabana*) y **`jaquey`** (nunca *jagüey*); más
`cenados` por venados y `caquelio` por caquetío en el OCR.

---

## 2. El esquema de clima

**Lo atestiguado son dos partes, no 60/60.** La lluvia es un pulso corto
—Camacho la mide en octubre-diciembre (`ecologia-006`) y **Sievers la vio en
persona en Paraguaná**: estuvo allí «en los últimos días de octubre y primeros de
noviembre de 1892, **época lluviosa**», y «meses después habría podido contemplar
las "feraces campiñas" vueltas tristes secadales» (Arcaya **p. 24**)—. El resto
del año es seca, con el alisio del ENE los doce meses y más fuerte en la seca.

Sobre eso, el canon propone **tres períodos** (el tercero es decisión, no dato):

| id | nombre | meses | días simulados | qué lo define |
|---|---|---|---|---:|
| **P1** | Tiempo de Viento | enero-mayo | **50** | el alisio arrecia: sal, agua clara, buceo, travesía a las islas, pesca nocturna con jachos |
| **P2** | la seca larga | junio-septiembre | **40** | el «largo verano»: el jagüey baja, se chupa jajato contra la sed, **sólo el cerro da agua**, y al final la convergencia |
| **P3** | Tiempo de Siembra | octubre-diciembre | **30** | el pulso: conuco de ciclo corto, cauces efímeros, el salinar para |

Suma 12 meses y **120 días simulados**: el año no cambia de tamaño, cambia de
reparto. La partición en dos es lo atestiguado; **partir la seca en dos es
decisión de simulación** y va declarada como `canon-simulacion`. La alternativa
mínima (seca 90 / lluvias 30, sin tocar la estructura de dos estaciones) está en
el archivo.

**El día dentro del período** está escrito por separado para cada uno: el
amanecer flojo de viento contra la tarde en que el alisio «arrecia en el curso
del día y empuja las corrientes hasta cerca de 1 m/s» (`ecologia-026`), el
anochecer en que se untan los jachos, la noche de la pesca con teas, y el
anochecer de la seca larga en que «le preguntan si lloverá o si el año será seco
o abundante» (Arcaya p. 98, Oviedo — con regla 4 declarada).

**Los períodos se quedan SIN nombre caquetío, a propósito.** `madunaka` «sequía»
existe pero es caquetío-hipotética, y el perfil `era2` esconde las 38 hipotéticas
por decisión del 2026-09-14: mostrarla sería adelantarle al agente la palabra que
el experimento quiere verle acuñar. Cada período lleva sus **raíces disponibles**
(`juri`, `kasi`, `biro`, `apana` / `usera`, `duna` / `kaya`, `tabri`, `jusual`,
`kono`) y ningún rótulo. Que el nombre lo acuñen ellos es el resultado, no el
andamio.

### Lo que cambiaría en el motor

- `curiana_state.ESTACIONES` pasa de dos entradas a tres; `DIAS_POR_ESTACION` de
  un entero a un mapa id → días; `ESTACION_DE_DIA` de alternancia módulo 2 a
  acumulado sobre tres tramos.
- Los meses del motor **no coinciden con el dato**: hoy dice lluvias «Jun-Nov», y
  junio y julio son los meses más secos. Sievers estuvo en el pulso en fechas que
  el motor llama seca.
- Los seis `EVENTOS_ESTACIONALES` se reparten solos: `gran_cosecha_sal` y
  `expedicion_perlas` a P1, `fiesta_cosecha_chicha` a P2 (es «antes de que lleguen
  las lluvias»), y los tres de lluvias a P3. El ritual de primeras lluvias deja de
  caer en el día 61 de 120 y cae en el 91.
- **Campos muertos que revivirían**: `descripcion` y `actividades_primarias` de
  cada estación **no los lee nadie** — `to_context_string()` sólo emite `nombre` y
  `clima_base`. Igual `ACTIVIDADES_POR_MOMENTO`: el prompt dice «Turno 1
  (amanecer)» y no dice qué significa el amanecer. Son exactamente el material del
  bloque `[Tu tierra]`.
- **Nada de esto toca `capas_de_score` ni el perfil `era2`.** Un cambio de
  calendario mueve QUÉ ve el agente del mundo, nunca con qué se le puntúa.

---

## 3. Los huecos léxicos declarados

**14 líneas** declaran `hueco_lexico: true`. Los que importan para la era 2:

| concepto | estado | dónde |
|---|---|---|
| ~~el venado~~ | ⭐ **CERRADO el mismo 2026-09-14**, en otra sesión y por decisión de Miguel: `matakán` [caquetío-retroabstraido], `ecologia-077`. Este canon ya lo usa en cuatro líneas. Sigue sin haber palabra **atestiguada** | `6-fusion/matacan_venado_2026-09-14.yaml` |
| **el manglar** | `mankaba` existe pero es **hipotética** y el perfil `era2` la esconde; las 4 especies y la raíz-zanco siguen mudas | `ecologia-011`, `hueco-lex` del mapa |
| **el cardumen** | el objeto y el oficio existen con **lugar propio** (las dos atalayas) y sin palabra | `hueco-lex-002`; Esteves pp. 58 y 61 |
| **la marea** | figura en los prompts y no es lexema; el fenómeno está medido (~50 cm) | `hueco-lex-007`; `ecologia-026` |
| **la duna / el médano** | el accidente que define el territorio, mudo; ⚠️ falso amigo: `duna` = AGUA | `hueco-lex-001` |
| **la quebrada efímera** | el cauce que sólo lleva agua tras la lluvia | `hueco-lex-006`; Arcaya pp. 14 y 16 |
| **la costra de sal y lo salobre** | hay `biro` y `borojo`, no el producto raspado ni el estado intermedio | `hueco-lex-005` |
| **el período del año** | ninguna estación tiene nombre caquetío. Sí hay unidad de tiempo: `apana` «una luna», `buiamati` «dos lunas», las dos atestiguadas | hueco nuevo de esta campaña |
| **barubaru** | la palma de cuyas hojas se hacen esteras, «abunda en las faldas del Cerro de Santa Ana», sin entrada en el lexicón | Esteves p. 23 |
| **el barbasco** | la única técnica de pesca de agua quieta que aparece, sin palabra | Esteves p. 22 |

**Este canon no propone ninguna forma nueva.** Usa 73 voces que ya existen, cada
una con su capa verificada contra `capa_epistemica()`, y deja los huecos a la
vista. Son el cebo de la acuñación emergente: el agente tiene la cosa y no la
palabra.

---

## 4. El yararé

> «En la laguna de Guaranao hay manglares, **yararés** y peces.»

**CERO en todo el material.** Barrido sobre `fuentes_caquetios/*.txt` y
`*.ocr.txt`, `3-mundo/`, `2-lengua/`, `6-fusion/`, `curiana_sim/*.py` (incluidos
`curiana_lexicon.py` y los `lexicon_*.py`) y el dictado de Medina Colina; raíces
`yarar`, `jarar`, `yaray`, `jaray`. Los cuatro mineros de esta campaña (Esteves,
Arcaya, Oliver, Castellanos) lo confirmaron por separado.

Lo único que aparece son otras palabras:

- `jarayadito`, topónimo del municipio Moruy, glosado «espinar, retamal,
  ñaragatal» (< *jaraya* 'espina, retama', toponimo-102). No es yararé.
- la sierra `Jarara` de la Guajira (`polities-caquetias.md`).
- `Mayarare` en Castellanos, línea 30063, fuera de Coro.
- un `Yarar` suelto en una columna de vocabulario OCR de Fabo 1911 (línea 5835),
  de lenguas del oriente colombiano, sin glosa.

**Queda como `testimonio-miguel`, sin identificar y fuera del mundo hasta que se
resuelva.** No se propone ninguna identificación: no se sabe siquiera si es ave,
reptil, crustáceo o planta. (Se anota sólo para que Miguel lo descarte: el
lexicón tiene `yawasa` «yaguaza, ave comestible de aguas cenagosas; hoy extinguida
en la península», caquetío-reconstruido, que es el único animal de laguna con
nombre del repo. No suena a yararé y no se usa.)

**En cambio el venado sí se resolvió, y el mismo día.** Este barrido lo halló por
su lado: el nombre vivo es **MATACÁN** — «cérvido de poca alzada. En tiempos
pasados había rebaños de este tipo de venado en los bosques de Paraguaná. Se han
extinguido por la cacería incontrolada» (Esteves p. 51)— y da además nombre a una
punta del Golfete que «hoy es una aldea de pescadores». El animal sigue vivo en el
cerro (venado matacán, Monumento Natural). **Otra sesión llegó a lo mismo y Miguel
decidió fonemizarlo** («sí o sí lo tenemos que utilizar»): `matakán` entró al
lexicón como **caquetío-retroabstraido** y al corpus como `ecologia-077`, con el
sustrato en duda declarado (`6-fusion/matacan_venado_2026-09-14.yaml`). Este canon
usa la voz nueva en cuatro líneas y ya no declara el hueco. Lo que sigue faltando
es una glosa «venado» en fuente caquetía que la suba a **atestiguada**.

---

## 5. El cargador de mundo: diseño de `curiana_mundo.py` (SIN implementar)

La pieza que falta para que todo esto llegue al agente. **No se ha escrito una
línea de código**: esto es el diseño que Miguel aprueba o corrige.

### Qué mide hoy el prompt

Medido el 2026-09-14 con el elenco `era2` y el perfil `era2`
(`vocabulario_para_agente` + `_IDENTIDAD_LINGUISTICA` + `prompt_emocionar` +
`to_context_string` + ficha; script en el scratchpad):

| parte | caracteres |
|---|---:|
| bloque de MUNDO (`to_context_string`) | **152** |
| identidad lingüística (fija) | 1.250 |
| ficha del agente (63 agentes) | min 346 · media **515** · max 678 (Manaure) |
| bloque léxico tier 1 | 4.435 |
| bloque léxico tier 2 y tier 3 | 995 |
| **prompt completo, tier 1** (17 agentes) | media **6.730** |
| **prompt completo, tier 2** (36 agentes) | media **3.205** |
| **prompt completo, tier 3** (10 agentes) | media **3.117** |
| **prompt completo, los 63** | media **4.142** (min 3.043, max 6.841) |

Hoy el mundo son **152 caracteres iguales para los 63 agentes**: día, turno,
momento, clima base y tres niveles. No nombra el sitio, ni el recurso, ni la
estación con contenido.

### El presupuesto propuesto

**`[Tu tierra]` ≤ 320 caracteres, tope duro.**

Por qué ese número, y no «lo que quepa»: **la longitud del prompt predice el
score con r = −0,48** (CLAUDE.md). Cualquier cosa que se añada al prompt se paga.
320 caracteres:

- **duplican con creces** el bloque de mundo actual (152 → ~472), que es el salto
  que hace falta para que el sitio deje de ser un nombre;
- cuestan **+7,7 %** sobre el prompt medio (4.142), **+4,8 %** sobre un tier 1 y
  **+10,3 %** sobre un tier 3 — el tier 3 es el que proporcionalmente más paga, y
  es justo el que hoy ve menos lengua (ver `saber_por_funcion_y_posicion` en
  `decisiones_tanda_2026-09-14.yaml`);
- caben **tres o cuatro líneas de canon** rendidas en prosa corta, que es
  exactamente lo que hace falta para decir «dónde estás, en qué momento del año, y
  qué se hace hoy aquí».

### Cómo se armaría el bloque

```
bloque_tu_tierra(sitio, periodo, momento, semilla, presupuesto=320) -> str
```

1. **Carga.** Lee `sitios_era2.yaml` y `clima_era2.yaml` — o, mejor, un módulo
   generado desde ellos, como `curiana_agents_era2.py` se genera desde
   `elenco_era2.yaml` (mismo patrón, mismo `--check`). Así el motor no parsea YAML
   en caliente y el guardián detecta la desincronización.
2. **Filtro.** Se quedan las líneas cuya `estacion` case con el período (o sea
   `todo el año`) y cuyo momento case, si lo declaran.
3. **Prioridad.** (a) lo que `abre_y_cierra` dice que ese período abre en ese
   sitio; (b) `agua` — es el recurso limitante de este litoral; (c) el dominio de
   la zona del sitio (`mar_y_pesca` si tiene zona, `tierra` si no, que es el caso
   de Moruy); (d) el resto, rotando.
4. **Rotación determinista.** Indexada por `(agente, día)` y sembrada con
   `--semilla`, para que el mismo agente no vea la misma línea todos los días y el
   run siga siendo reproducible.
5. **Render.** Prosa corta en castellano, **sin etiquetas epistémicas** — la
   etiqueta vive en el YAML, no en la cabeza del agente—, con la `voz_caquetia`
   incrustada cuando existe, porque cada aparición es una ocasión de usar la
   palabra. Ejemplo (Tacuato, P1, noche, **278 caracteres** medidos):

   > `[Tu tierra] Tacuato, la orilla del Golfete. Tiempo de Viento: el juri sopla`
   > `firme y el agua está clara. Es de noche: se untan los jachos con manteca de`
   > `kunaro y se sale a encandilar. El jagüey todavía tiene del agua del año`
   > `pasado. El biro de las charcas está listo para raspar.`

6. **Tope duro.** Se trunca **por línea entera**, nunca a media frase, y hay un
   test que recorre las **126 combinaciones** (7 sitios × 3 períodos × 6 momentos)
   y afirma `len(bloque) <= presupuesto` en todas.

### Qué NO debe hacer

- **No mostrar voces hipotéticas.** El perfil `era2` esconde las 38 por decisión
  del 2026-09-14: `mankaba`, `tüma`, `marisi`, `atara`, `yuri` y `kanua` aparecen
  en el canon como apoyo del escriba, y el render tiene que saltárselas. Un test
  lo vigila.
- **No inyectar los `testimonio-miguel` con `deuda: sin-procedencia`** hasta que
  Miguel los resuelva. El yararé, sobre todo: meterlo sería fabricar mundo.
- **Sí inyectar los `hueco_lexico`**, pero como COSA sin palabra: «el banco de
  peces que se ve desde la punta» y no una forma inventada. Ese es el cebo.
- **No tocar `capas_de_score`.**

---

## 6. Preguntas (8)

1. **¿Tres períodos (50/40/30) o dos (90/30)?** Los dos respetan el corpus. El de
   tres es el que hace visible la seca larga, que es donde el Capubana cobra
   sentido; el de dos es un cambio de una línea en `curiana_state`.
2. **¿Los períodos se quedan sin nombre caquetío**, para que lo acuñen los
   agentes? (Es lo que propongo; la alternativa es darles un rótulo en el prompt,
   y entonces `madunaka` sale del escondite de las hipotéticas.)
3. **¿Qué es el yararé?** ¿Ave, reptil, crustáceo, planta? ¿Lo oíste en
   Paraguaná o lo leíste? Con la categoría se puede buscar en el dictado de Medina
   (66 entradas de fauna y flora) y en el gazeteer. Mientras tanto no entra.
4. **Los hechos nuevos que la campaña propone: ¿se fusionan antes o después del
   primer run?** Son siete para `ecologia.yaml` (los jachos, el barbasco, las
   atalayas de cardúmenes, el guairón y la cal, el cují como señal de agua, el
   pulso de Sievers, y el matacán que ya entró) y tres para `creencia.yaml` (el
   tabú de caza, el dueño del cerro, las Piedras del Almanaque). Si entran antes,
   el cargador de mundo puede citarlos; si entran después, el primer run corre con
   el canon de hoy.
5. **Caseto tiene su playa a ~22 km.** ¿Se queda con ZA1 y decimos en el prompt
   que caminan a ella, o su dominio principal pasa a ser el conuco y pescan «de
   visita»?
6. **El Capubana está con `lat: None, lon: None`** en `curiana_agents_era2.py`.
   ¿Se rellenan con el pico del mapa vivo (11.8183, −69.9524, 830 m)? Sería
   regenerar el módulo.
7. **¿Presupuesto de 320 caracteres para `[Tu tierra]`?** Es +7,7 % sobre el
   prompt medio y r = −0,48 nos dice que se paga. Se puede bajar a 240 o subir a
   400; lo que no se puede es no fijarlo.
8. **El manglar de la laguna de Guaranao es tuyo y no tiene fuente** (cero en
   Arcaya, Oliver, Castellanos; en Esteves el único manglar de Paraguaná está en
   Babahuro, costa de Adícora). ¿Lo perseguimos —una ficha ambiental o una imagen
   de satélite lo subiría a atestiguado-moderno— o entra como canon-simulación
   para el primer run?

---

## Deudas abiertas que deja la campaña

- **Releer dos páginas del PDF de Esteves.** El OCR las trae invertidas e
  ilegibles: OCR 2 p. 42 (Guaricure, Guaruguaja, Guasare, Guatacare, Guayacanal) y
  OCR 5 p. 101 (Ceiba, Cerey, Cibita, Cocorote, **COCUIZA y COCUY** — justo las dos
  de fibra y bebida). Y la entrada **CAYUDE** (OCR 2, p. 30) está medio destruida,
  siendo un sitio en escena.
- **La frase cardinal de Oliver sigue al revés.** DOC 264: «the Amuayes which
  controlled the **southern** part and the Guaranaos who controlled the
  **northern** part». #122 decidió lo contrario. La deuda sigue abierta y la
  decisión del 2026-09-14 la ignora por decisión, no por descuido.
- **«Las Piedras del Almanaque»** (Esteves p. 60) no tienen lectura publicada.
  Comprobar si el inventario de petroglifos de Morón 2012 para Falcón incluye
  Siraba.
- **Los hechos nuevos para el corpus.** `sitios_era2.yaml`
  §`propuestas_a_otras_esferas` propone siete para `ecologia.yaml` (el matacán, los
  jachos, el barbasco, las atalayas, el guairón, el cují como señal de agua, el
  pulso de Sievers) y tres para `creencia.yaml` (el tabú de caza, el dueño del
  cerro, las Piedras del Almanaque). Regla 5: los propone; fusionarlos es otra
  sesión.
