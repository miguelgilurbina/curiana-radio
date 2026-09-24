---
tipo: nota-viva
ambito: estado del lexicón activo
fuente_de_verdad: curiana_sim/curiana_lexicon.py
total: 5490
familia_caquetia: 380
sin_cita: 0
medido: 2026-09-24
---

# El lexicón

> El lexicón activo es `VOCABULARIO_BASE` en `curiana_sim/curiana_lexicon.py`.
> **Esta nota lo describe; no lo define.** Las cifras de los bloques
> generados las mide y las escribe `curiana_sim/tabla_lexicon.py` con las mismas
> funciones que el tablero, y `generar_tablero.py` lo llama en cada cierre: hasta
> el 2026-09-24 eran una foto del 2026-08-04 escrita a mano («1413 entradas»)
> que la wiki pública seguía publicando.

## El tamaño real

<!-- GENERADO por curiana_sim/tabla_lexicon.py: tamano -->
**5.490 entradas activas** en `VOCABULARIO_BASE`, y **77** archivadas en `FUERA_DEL_HABLA` (fuera del habla, con su capa intacta).
<!-- /GENERADO -->

```bash
cd curiana_sim && python -c "import curiana_lexicon as L; print(len(L.VOCABULARIO_BASE))"
```

## Desglose por lengua

El campo `fuente` tiene muchos valores crudos distintos;
`normalize_source_language()` (en `curiana_database.py`) los colapsa a estas
categorías:

<!-- GENERADO por curiana_sim/tabla_lexicon.py: lenguas -->
| Categoría normalizada | Entradas | % |
|---|---:|---:|
| proto-arahuaco | 3.572 | 65,1 % |
| wayunaiki | 769 | 14,0 % |
| lokono | 636 | 11,6 % |
| **caquetío** | 380 | 6,9 % |
| paraujano | 47 | 0,9 % |
| taíno | 45 | 0,8 % |
| kalinago | 25 | 0,5 % |
| jirajaroide-contacto | 7 | 0,1 % |
| caribe-continental | 6 | 0,1 % |
| español-colonial | 3 | 0,1 % |

> **93,1 % del lexicón no es caquetío**: son comparanda, están ahí para reconstruir y medir, no para hablar.
<!-- /GENERADO -->

> `score_linguistico()` trata las comparanda como tan ajenas como el español —
> una fuga a wayunaiki penaliza igual que un artículo castellano (ver
> [[mapa-motor]] §scoring)—, salvo la esfera de contacto, que se mide aparte.
>
> El desbalance wayunaiki : lokono fue el objeto de la decisión de fondo D11 →
> [[metodo-comparativo]] §el desbalance.

## Las capas epistémicas del caquetío

> ⚠️ **El núcleo ya no es lo que era**: desde la
> **tanda de las hermanas (2026-09-24)** el «núcleo fundacional» se rehízo
> desde el lokono y el habla de mujeres kalinago —dos hermanas con la misma
> forma = reconstruida, una = hipotética—, sus voces viejas (que citaban
> «cognado» sin obra) están archivadas en `FUERA_DEL_HABLA` con su capa, y
> donde el caquetío atestiguado ya decía la cosa, manda él. Registro:
> `6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml`; cifras:
> `6-fusion/medicion_tanda_hermanas_2026-09-24.yaml`.

<!-- GENERADO por curiana_sim/tabla_lexicon.py: capas -->
De las **380** entradas de familia caquetía:

| Etiqueta | n |
|---|---:|
| `caquetío-atestiguado` | 185 |
| `caquetío-hipotético` | 76 |
| `caquetío-retroabstraido` | 75 |
| `caquetío-reconstruido` | 44 |

**0 sin `notas`** (sin cita).
<!-- /GENERADO -->

(Las entradas sin `notas` eran 82 en julio de 2026.)

## Quién sostiene el "atestiguado"

Este es el dato más importante de la nota.

<!-- GENERADO por curiana_sim/tabla_lexicon.py: sostiene -->
De las **185** entradas `caquetío-atestiguado`, cuántas citan a cada obra en su campo `notas` (una entrada puede citar varias; los patrones salen del `autor` y los `aliases` de cada nota de `4-fuentes/`, como en el tablero):

| Obra | Entradas que la citan |
|---|---:|
| [[zavala-reyes-2015]] | 174 |
| [[zavala-reyes-2018]] | 174 |
| [[arcaya-1920]] | 12 |
| [[arcaya-obra-inedita-1995]] | 12 |
| [[oliver-1989-apendice-a]] | 12 |
| [[oliver-1989-cap2]] | 12 |
| [[oliver-1989-cap3-vecinos]] | 12 |
| [[oliver-1989-cap3]] | 12 |
| [[oliver-1989-cap4]] | 12 |
| [[oliver-2000-guanin]] | 12 |
| [[alvarado-1921]] | 11 |
| [[van-buurt-2014]] | 7 |
| [[coll-y-toste-1897]] | 6 |
| [[brinton-1871]] | 5 |
| [[gatschet-1885]] | 4 |
| [[goeje-1939]] | 3 |
| [[oviedo-y-valdes-1851]] | 3 |
| [[angulo-molina]] | 2 |
| [[oviedo-y-valdes-1852-1855]] | 2 |
| [[medina-colina-sxx]] | 2 |
| [[las-casas-1875]] | 2 |
| [[las-casas-apologetica]] | 2 |
| [[castellanos-elegias]] | 2 |
| [[castellanos-nuevo-reino-1886]] | 2 |
| [[jahn-1927]] | 1 |
| [[gonzalez-batista-2002-fundacion]] | 1 |
| [[gonzalez-batista-nombre-de-coro]] | 1 |
| [[ballesteros-1550]] | 1 |
| [[pane-c1498]] | 1 |
| *sin obra reconocida en `notas`* | 0 |
<!-- /GENERADO -->

> **El caquetío atestiguado del proyecto es, casi entero, el glosario de Zavala
> Reyes 2015** (la tabla de arriba lo mide). Las demás obras figuran como fuentes del proyecto y aportan una
> decena de entradas entre todas. No es un defecto de curación: es lo que hay
> publicado. Pero significa que **un error sistemático de Zavala sería un error
> sistemático del proyecto**, y que ampliar la base documental (F9: Oviedo t. II
> y el apéndice de voces caquetías del t. IV) es la deuda más cara que queda.

Zavala está **cerrado al 100 %**: `minar_zavala_glosario.py` parsea las 288
entradas del glosario. 225 (78 %) entran al habla activa; 63 (22 %) quedan
**fuera por diseño** — 45 topónimos, 14 antropónimos y 4 descartes. No es deuda:
es curación. Los topónimos excluidos, sin embargo, resultaron ser una mina de
morfemas → [[toponimia]].

## Las 441 candidatas aisladas

`curiana_sim/lexicon_candidatos.py` guarda **441 formas
`hipotético-no-verificado`**, **fuera del lexicón activo y fuera de Supabase**
desde 2026-06-28.

Las generó `reconstruir_caquetio_gaps.py` transduciendo fonológicamente
cualquier palabra wayunaiki, lokono o taína con la misma glosa española, **sin
verificar cognación real** contra `COGNADOS`. La minería de pares objetivos
(`minar_pares_validacion.py`) midió **~80 % de fallo** contra datos reales.

Por qué se aislaron, y no solo se re-etiquetaron: estando en `VOCABULARIO_BASE`
producían **falsos positivos en `score_linguistico()`** — un "la" o un "para"
españoles matcheaban contra entradas hipotéticas y el motor los contaba como
caquetío.

De dónde se transdujo cada una, medido sobre el campo `notas`:

| Lengua de partida | Candidatas |
|---|---:|
| solo wayunaiki | **388** (88 %) |
| solo lokono | 46 |
| ambas | 5 |
| taíno | 2 |

Ese 88 % es la misma sesgo que denuncia D11: **se reconstruyó desde la hermana
que Oliver considera la más lejana**, lo que explicaría parte del 80 % de fallo.

## La regla: **manda la atestiguada**

> **Decisión de Miguel, 2026-09-19.** «Sí o sí tenemos que usar los
> atestiguados por sobre los reconstruidos, por lo menos la parte caquetía.»
> Es una **política**, no una respuesta par a par:
> `6-fusion/decisiones_tanda_2026-09-19.yaml` (d19.b).

**Donde el caquetío tiene forma atestiguada para un significado, ésa es la que
la comunidad habla y la que el instrumento enseña.** La derivada —reconstruida,
retroabstraída o hipotética— no se borra: se **archiva** con su procedencia, y
deja de enseñarse y de competir.

### Para qué es, entonces, la capa reconstruida

> **Precisión de Miguel, 2026-09-20** (d19.c). «Al final no pasa nada si hay
> símiles. En todo lenguaje hay símiles. Pero lo importante es que usemos sí o
> sí lo atestiguado, y **lo reconstruido lo usemos para nuestros blind
> spots**.»

La reconstrucción existe para **cubrir los huecos donde no hay atestación** —los
puntos ciegos de la documentación—, no para duplicar lo que ya está
documentado. De ahí sale el criterio para los casos dudosos:

- **La sinonimia en sí no es el problema.** Toda lengua tiene símiles, y dos
  voces *atestiguadas* para lo mismo son un dato, no un error: se conservan las
  dos y se declara la variación.
- **Lo que la política corrige es la reconstrucción compitiendo con la
  atestación**, que es una sinonimia que inventamos nosotros y que además el
  instrumento amplifica (ver la medición: decide la plantilla, no el
  muestreador).
- **Una reconstruida sin rival atestiguado se queda sin discusión**: está
  haciendo exactamente aquello para lo que existe. Por eso la política no toca
  los aspectos ni el grueso de las 86 reconstruidas.
- **Y el caso barato: rival atestiguado que NO compite.** Cuando la forma
  atestiguada existe pero cubre otro registro, no hay nada que archivar — se
  reparten el uso. Ver los pronombres, abajo.

El criterio operativo, porque es lo que decide los casos dudosos:

| Pregunta | Respuesta |
|---|---|
| **¿Mismo significado?** | La **glosa normalizada idéntica**, y sólo ésa, dispara la política sola. Normalización: NFC + minúsculas · fuera paréntesis y corchetes · fuera diacríticos · fuera el artículo inicial y la puntuación de los extremos · espacios colapsados. **Sin diccionario de sinónimos**: decidir que «cerro» y «loma» son lo mismo es una afirmación sobre el significado, y la decide Miguel (regla 2). |
| **¿Y el solapamiento parcial?** | **No es par.** Dos glosas que sólo comparten una palabra —«empezar, crear, originar» contra «hacer, construir, crear»— son una **glosa mal afinada**. Van a curación, no a la política. |
| **¿Qué cuenta como atestiguado?** | La etiqueta `caquetío-atestiguado` **más su cita** en `notas` (regla 8). La etiqueta sola no basta, y `caquetío` a secas tampoco: eso es etiquetado antiguo, no atestación. |
| **¿Qué se hace con la derivada?** | Se **archiva**: sale de `VOCABULARIO_BASE`, entra en `FUERA_DEL_HABLA` y conserva forma, glosa, **su capa epistémica intacta** y su `notas` entera, más un campo `archivada` con su fecha y su par. **Archivar no es borrar y tampoco es degradar** — la etiqueta dice de dónde viene la palabra, el archivo dice si la comunidad la habla. Dos ejes. |
| **¿Hasta dónde llega?** | **Sólo donde EXISTE rival atestiguado.** El grueso del lexicón caquetío es reconstrucción legítima porque no hay atestación (los aspectos y la mayoría de las reconstruidas) y se queda como está. Esto no es una poda del núcleo. ⚠️ Los **pronombres** ya no son ejemplo de esto: ver abajo. |

Aplicada el 2026-09-19 a siete pares: manda `kasi` sobre `kali` (sol), `were`
sobre `paa` (ofrecer), `jai` sobre `kira` (escuchar), `kati` sobre `kasha`
(luna), `para` sobre `habo` (mar), `juri` sobre `joutai` (viento) y `etamo`
sobre `mülia` (espanto). Medición del corte —incluidos los dos costes que
había que decir antes de aplicar, el paradigma de `paa` y la colisión
`kasi`/`kashi`— en
`6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml`. Lo que queda
abierto (`sima` y once glosas por afinar) está en
`6-fusion/curacion_glosas_pares_2026-09-19.yaml`.

### El caso barato: los pronombres

> ⚠️ **Corrección del 2026-09-21** (d21.10). Esta nota decía que la política «no
> toca los pronombres» porque **no tienen rival atestiguado**, y **eso no es
> exacto**. El lexicón tiene **dos pronombres caquetío-atestiguados con cita**:
> `kudanga` 'usted, vos (2ª persona formal)' y `kuté` 'a usted, para usted
> (dativo formal)' — [[zavala-reyes-2015]] p. 73, citando a [[arcaya-1920]]:
> *«chacamba cudanga»* '¿cómo está usted?' y *«cudan de cuté»* 'para servir a
> usted'. Hasta esa fecha el prompt enseñaba **cinco pronombres, los cinco
> reconstruidos del wayuu**, y ninguno de los dos atestiguados.

**Y aun así no hay nada que archivar: por eso es el caso barato de la
política.** El criterio de arriba pide **glosa normalizada idéntica**, y 'usted
(formal)' no es 'tú': **no hay par**, así que la política no se dispara sola y
hace falta una decisión aparte — que es la que Miguel tomó. `pia` y `kudanga`
no compiten: **se reparten registros**, `pia` para el tú corriente y `kudanga`
para dirigirse a un mayor o a un Diao. Es un rasgo social además de gramatical,
y la era 2 tiene la jerarquía escrita para usarlo — el trato formal al Manaure
en el Capubana y el tú corriente en el conuco.

Sirve de plantilla para los que vengan: **«hay forma atestiguada» no significa
siempre «archiva la otra»**. Si las dos cubren el mismo significado, manda la
atestiguada y la derivada se archiva; si cubren **registros distintos**, entran
las dos y se declara el reparto. Detalle gramatical en [[morfologia]] §1.

## `FUERA_DEL_HABLA` — el archivo, no la papelera

`FUERA_DEL_HABLA` es un dict del propio `curiana_lexicon.py` para entradas
**retiradas del habla activa sin borrarlas**: conservan forma, glosa y toda su
procedencia documental, pero no se ofrecen a los agentes ni cuentan para el
scoring.

> ⚠️ **Y desde el 2026-09-19 es además una puerta.** `FORMAS_DE_PLANTILLA`
> incluye `FUERA_DEL_HABLA`, así que una forma archivada **tampoco compite**:
> no se registra como acuñación ni entra en la competencia léxica. Sin eso,
> archivar una voz la sacaba de `VOCABULARIO_BASE`, la sacaba de la puerta y
> la dejaba volver al día siguiente como «palabra nueva de la comunidad» —
> `kali`, con 2.321 usos detrás, habría vuelto la primera.

**Empezó con un solo miembro: `piache`.** Retirada el 2026-08-03 (D10). Su
lugar lo ocupa `boratio`, que sí es caquetío atestiguado. Las dos fuentes
coinciden:

- [[alvarado-1921]] p.248: *"Voz cháima y tamanaca, con formas afines en otras
  lenguas caribes"*.
- [[zavala-reyes-2015]] glosario #43 glosa el caquetío `boratio` **como**
  'piache, cacique, jefe, sacerdote, médico' — es decir, *piache* es la **glosa
  española**, `boratio` la voz caquetía.

El canon no se tocó: Shaboro sigue siendo el piache de la Curiana
([[mapa-creencia]]). El mecanismo es el importante: **archivar con procedencia
es distinto de borrar**, y deja el camino abierto si aparece evidencia en
contra.

Después entraron los **cinco numerales reconstruidos del wayuu** (`wanee`,
`piama`, `apünüin`, `pienchi`, `jarai`), retirados el 2026-09-13 cuando Miguel
decidió «Cambiemos los numerales» — el caquetío atestigua `pana`, `gudamuen`,
`sabuenen` y `katarí`. Y el 2026-09-19, las **siete de la política «manda la
atestiguada»**. Hoy el archivo tiene **13 miembros** (6 → 13 en esa tanda,
medido en `6-fusion/medicion_politica_atestiguado_manda_2026-09-19.yaml`
§censo; se cuenta con `len(FUERA_DEL_HABLA)`), todos con su capa original y su
procedencia entera. Las tres tandas son la misma regla dicha
tres veces: donde hay dato, el dato manda; donde no lo hay, la reconstrucción
es legítima y se queda.

## Los conflictos de glosa abiertos

Tres entradas cuya glosa activa **contradice a la fuente**, y que **no se
reescriben** porque corregirlas obliga a tocar el canon del mundo. Cada una
lleva su razonamiento completo en el campo `notas` de la entrada.

| Palabra | Glosa activa | Qué dice la fuente | Issue |
|---|---|---|---|
| `tara` | 'venado, ciervo' | **Doble corroboración en contra**: [[zavala-reyes-2015]] #238 'langosta, mariposa'; [[alvarado-1921]] p.283 'polilla o mariposa' (cf. *TARÍTA*, "mariposa o tara pequeña"). La glosa activa no tiene fuente localizada. | [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) |
| `saruro` | 'árbol saruro (frutos pequeños)' | Sin cita localizada; la fuente reasigna. | [#47](https://github.com/miguelgilurbina/curiana-radio/issues/47) |
| `corie` | 'choza, habitación' | [[zavala-reyes-2015]] #90 'armadillo' — **y el propio canon del proyecto ya dice armadillo**: `3-mundo/corpus/genealogia.yaml` da "corie (armadillo)" como tótem del linaje Paugis. La glosa contradice a la fuente **y** a su propio canon. | [#46](https://github.com/miguelgilurbina/curiana-radio/issues/46) |

**Por qué son caros.** `tara` sostiene material del corpus ecológico
([[mapa-ecologia]], `ecologia.yaml`, [[02_ecologia_golfete]] §10.6); `corie` da
nombre al asentamiento Korie-ko. Corregir la glosa no es editar una fila: es
mover el mundo. Por eso quedan como decisión de Miguel.

## Las 3 entradas que quedan sin cita

`auditar_82.py` cruza las cuatro minerías (Alvarado F3, Gatschet F4, van Buurt
F6, Zavala F7) y adjudica cada entrada de familia caquetía sin `notas`. El censo
arrancó en 82 y hoy va en **3**:

```
CENSO: 3 entradas de familia caquetía sin cita
0 confirman · 0 reclasifican · 0 conflicto de glosa · 0 a revisar · 3 sin rastro
```

Las 3 restantes **no dejan rastro en ninguna de las cuatro fuentes minadas**.
Ya no son deuda de minería sino de decisión: o aparece una fuente nueva (F9) o
se degradan a `caquetío-reconstruido`.

## Avisos operativos

> ⚠️ **Queries a la tabla `lexicon` en Supabase**: PostgREST corta cada
> respuesta en `max_rows` (1000). Con 1413 palabras, toda query sin `.range()`
> se trunca **en silencio**. Paginar con `.range(desde, desde+999)`.

> ⚠️ **`lexicon_zavala.py` no es solo una propuesta**: `curiana_lexicon.py` lo
> importa (`GLOSARIO_ZAVALA`, `HOMOGRAFOS_ZAVALA`). Regenerarlo **cambia el
> comportamiento de `score_linguistico()`**. Los otros tres módulos de propuesta
> (`lexicon_alvarado.py`, `lexicon_gatschet.py`, `lexicon_van_buurt.py`) no se
> importan en ninguna parte.

## Enlaces

[[morfologia]] · [[toponimia]] · [[metodo-comparativo]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision)
