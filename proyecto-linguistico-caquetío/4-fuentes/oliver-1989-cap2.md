---
tipo: fuente
obra: "Chapter 2: Arawakan Historical Linguistics"
autor: "Oliver, José R."
anio: 1989
genero: linguistica-comparativa
local: "fuentes_caquetios/Chapter 2 Linguistics- Oliver 1989.pdf"
paginas: 109
capa_texto: parcial
acceso: "Libre — la tesis completa (823 pp., incluye este capítulo) está en UCL Discovery, depositada por el propio Oliver: PDF https://discovery.ucl.ac.uk/id/eprint/10157455/1/Oliver_10157455_thesis_redacted.pdf · ficha https://discovery.ucl.ac.uk/id/eprint/10157455/. Verificado en el rastreo de 2026-08-14."
estado_minado: minado
cobertura: "§2.8 «The Caquetío Language» (pp. 142-151) minado en F5 (2026-08-03) + relectura de pp. 146-151 y p. 97 para el cruce taíno↔caquetío (2026-09-21)"
prioridad: alta
minado: 2026-09-21
tareas: [F5]
cobertura: "lingüística comparativa, cognados y correspondencias (F5, 2026-08-03) + releído por el taíno: filiación vs. contacto y el vector español-Hispaniola (2026-09-21, campaña del taíno T5)"
sostiene: {hechos_corpus: 2, entradas_lexicon: 2, propone_cognados: 16, propone_correspondencias: 14, propone_entradas_lexicon: 5, propone_pares_validacion: 10}
verificado: 2026-09-21
minado: 2026-09-21
aliases: ["Oliver 1989 cap. 2", "Oliver cap. 2", "Linguistics"]
---

# Oliver 1989, cap. 2 — Lingüística histórica arahuaca

## Qué es

**El pilar teórico de la Capa 2 del proyecto** (reconstrucción con base real).
109 páginas de lexicoestadística y fonología comparada de 31 lenguas arahuacas,
de las que solo **§2.8 «The Caquetío Language» (pp. 142-151)** trata directamente
del caquetío. Es la fuente natural de `COGNADOS` y de las `REGLAS_*` de
`arahuaco_comparative.py`.

Minado en F5 (2026-08-03). La propuesta vive en
`curiana_sim/cognados_oliver.py`; el minador y su verificación, en
`curiana_sim/minar_oliver_cap2.py`. **Ninguno modifica el motor.**

## Estado técnico (verificado 2026-08-03)

| Dato | Valor |
|---|---|
| Tamaño | 12.3 MB · 109 páginas |
| Capa de texto | **parcial**: buena en la prosa (282K caracteres), **nula en las tablas** |
| Receta | `pdftotext -enc UTF-8 -layout` — **con `-layout`, no sin él** |
| Paginación | El número está al **pie** de cada plana, seguido del encabezado corrido de la siguiente. 106 marcadores detectados; el rango real es pp. 52-160 |
| Artefacto 1 | Extracción a **una palabra por línea**: 14.2% de las líneas sin `-layout`, **3.9% con** `-layout`. Reparable con `reunir_lineas_partidas()` |
| Artefacto 2 | **24 páginas son solo pie de figura**: el contenido es imagen sin capa de texto |

### Las tablas comparativas no existen como texto

La tarea original pedía «reconstruir las tablas de vocabulario comparativo».
**No se pueden reconstruir por extracción: no hay nada que reconstruir.**

- **Tabla 3** (*Arawakan Phoneme Reflexes*, p. 104) y **Tabla 8** (*Comparative
  Lexicostatistical Data*, p. 130) son páginas-imagen: solo sale el pie.
- **Tablas 4, 5, 6 y 7** (fonemas proto-arahuacos según Matteson; achagua;
  piapoco; guajiro; paraujano; lokono) están embebidas como imagen **dentro de
  páginas con prosa**: ni siquiera el pie llega al texto. La prosa las cita
  («shown in Table 5 below») y nunca aparecen.
- Recuperarlas exige **OCR sobre el render**, no extracción. Es una tarea
  distinta, con coste distinto.

Sí salieron como texto cuatro tablitas menores, y están volcadas en
`cognados_oliver.py`: los 6 pares guajiro/lokono/island-carib de Taylor 1977:38
(p. 119), los 5 cognados dudosos guajiro-paraujano (p. 114), los 8 cognados
dudosos lokono-achagua (p. 122), y las Tablas 9 y 10 de milenios de separación
(pp. 130-131).

### El Apéndice A no está en el repositorio

El capítulo cita cinco veces un **Apéndice A** que este PDF **no contiene**:
«Appendix A: Tables A1, A2, A8, A9», «item #43, #53, #83, #87 Appendix A».
Ahí viven las listas de 100 palabras de Swadesh para 31 lenguas, **la lista
completa de términos caquetíos (su Tabla 8)** y los vocabularios cuyón de los
que salió `auri`. **Es la pieza que falta y la que más rendiría** — más que
cualquier OCR de las tablas de este capítulo.

## Qué ha dado

### 16 sets de cognados con caquetío atestiguado (§2.8)

9 de confianza **alta**, 5 **media**, 2 **baja**. **11 de los 16 llevan una
reserva textual del propio Oliver**, reproducida en el campo `oliver_duda` y que
no debe limpiarse al importar.

| Concepto | CQ | Hermanas (selección) | p. | Confianza |
|---|---|---|---|---|
| ceniza | **barisi** | LK *bálisi* · WY *palíi* · PA *\*p-/b-ali-* | 142 | alta |
| almagre | bariki | achagua *ki-rrayi*, piapoco *ki-reri* | 142 | baja |
| tapir | kama | WY *ama'* · maipure *kiema* · baré *dehema* · +6 | 143 | alta |
| árbol | **-ada-** | LK *ada/adada/ida* · WY *ata'* · baré *adda* · +8 | 144 | alta |
| calabaza | auyama | achagua *uyama* · guarequena *uiiayama* · +5 | 145 | alta |
| espíritu | capú | wapishana *capishi* · baré *capuyo* | 145 | baja |
| bachaco | koke | yavitero *hoke* · maipure *kuki* · LK *kuse* | 145 | media |
| señor | diao | LK *dai-yana-ho*, *dia* 'palabra' | 146 | media |
| aliado ritual | daitiao | TN *daitia-o/waitiao* · LK *da-tti/da-iti* · PA *\*-atti-* | 147 | alta |
| **diente** | **dare** | LK *d-ari* · WY *t-ali* · PJ *t-a()i* · TN *m-a(h)i-te* | 147 | alta |
| fruto del cardón | dato | LK *-atti-* | 147 | media |
| chamán | boratio | LK/TN *-ati* + *-(h)o* | 147 | media |
| **ser vivo** | **kaketío** | LK *kakïtho* · piro *kaxiti* · ipuriná *kakiti* | 148 | alta |
| canal | buko | LK *wáburúkku/wáboróko* | 148 | media |
| **perro** | **auri** | CAIC/maipure/achagua/piapoco *auri* · PJ *-y-eri* | 151 | alta |
| mar | para | WY *palaa'* · TN *bara-wa* | 150 | alta |

### 14 correspondencias fonológicas (C1-C13)

Es lo que las 441 formas `hipotético-no-verificado` nunca tuvieron. Las de más
consecuencia:

- **C1 — el prefijo de 1.ª persona singular.** PA `*/nV-/` → `/dA-/` en lokono,
  taíno y «perhaps Caquetío» → `/tA-/` en guajiro-paraujano. Evidencia caquetía:
  *diao*, *datihao*, *dare*, *dato*. **El caquetío conserva /d-/.**
- **C2 / C3** — «two very regular and systematic sound changes»: LK /d/ : WY /t/
  y LK /b/ : WY /p/. El caquetío cae del lado lokono en ambas
  (*barisi* : *bálisi* : *palíi*; *-bana* y no *-pana*) — **con un contraejemplo
  que Oliver no explica: *para* 'mar' frente a LK *bara*, TN *bara-wa*.**
- **C4 / C4b** — LK /th/ : WY /s ~ sh/ : CAIC /t/ (Taylor 1977:38), y
  CQ /t/ : LK /th/ (*kaketío* : *kakïtho*). Cadena nueva y limpia; el proyecto
  no tiene ninguna regla para el /th/ lokono.
- **C5 —** las palatales guajiras /ch/, /ñ/, /sh/ «arose as phonemes not very
  long ago» (Taylor 1978). **Munición principal contra las 441.**
- **C8 / C9 —** dos **límites**, no reglas: /r/~/l/ es indecidible en todo el
  corpus, y Oliver **excluye las vocales** de su método por falta de
  transcripción fonética fiable.

### 8 afijos, con página y valor

`-si` (nominalizador, PA *\*-tsi/\*-si*), `-(h)o` (nominalizador solemne, forma
títulos y etnónimos), `-bana`, `-coa`, `-oa`, `-ba-/-va-` (valor
**indeterminado**, dicho por Oliver), `k-/kV-` (atributivo, alterna con cero),
`mV-` (privativo). Los dos primeros faltan en `REGLAS_ZAVALA`.

### El nudo `daitiao` / `datihao` / `diao` — **cerrado**

**Dos lexemas, no tres ni uno.** `daitiao` = `datihao` (misma palabra, dos
grafías coloniales); `diao` es **otra palabra**.

Oliver les da **dos etimologías distintas**: *diao* = `/d-ia(o)/` sobre la raíz
lokona `/d-ai-/` de 'palabra/lengua'; *datihao/daitiao* = `/da-/` + `/-(i)tiao/`
sobre la raíz de parentesco lokona `/atti/`. Y da los prefijos con su valor
gramatical, sin que haya que inferirlo: «The prefix /wa- [gua-]/ is a third
person plural marker, and /da-/ in da(i)tia-o is first person singular marker»
(p. 147). **Confirma la conclusión de la minería de Zavala ([[zavala-reyes-2015]], F7).**

Dos matices que hay que conservar:

1. La frase «*diao* is, in many ways, closely related to *datihao*» (n. 42)
   **no es una identificación**: son parientes por compartir el prefijo `/d-/`
   y el sufijo `/-(h)o/`, no la raíz. Se ha leído mal antes.
2. **Oliver duda de que *datihao* sea caquetío** (n. 42, p. 146): Oviedo hablaba
   de «los indios de la Provincia de Venezuela» en general y su larga residencia
   en La Española pudo hacerle usar taíno. Descarta el guajiro-paraujano y
   concluye que probablemente fuera «equally shared by both Taíno and Caquetío».
   **El lexicón tiene `datihao` como `caquetío-atestiguado` sin esa reserva.**

### El ancla del «arco norteño» — verificada, y dice lo contrario

Esta nota afirmaba antes que Oliver «confirma que las dos hermanas más cercanas
del caquetío son el wayuunaiki y el paraujano», y sobre eso se apoya
[[01_familia_caquetia]] §2. **Con el texto delante, Oliver dice lo contrario:**

> «it seems reasonable, for the moment, to regard Caquetío as emerging from a
> similar background to that of **Lokono rather than from a Guajiro-Paraujano
> ancestry**» (p. 150)

> «a preliminary examination of selected Guajira-Falcón toponyms show **far more
> differences in sound sequences than similarities**» (p. 150)

> «Caquetío, which I have shown to have the **strongest affinities with Lokono**»
> (p. 155)

Sus tres pilares: el prefijo `/dA-/` de 1sg (solo lokono y taíno lo tienen), la
innovación léxica *auri* 'perro', y *kaketío* = LK *kakïtho*.

Lo que Oliver **sí** dice sobre el par guajiro-paraujano es que son entre **sí**
las dos lenguas arahuacas más próximas que se conocen (64.2% de vocabulario
básico, separación mínima 1.0 milenio, ca. A.D. 900-1200) — afirmación sobre
**ellas dos**, no sobre el caquetío. Y hace salir a lokono, island carib, taíno y
caquetío del **mismo nodo** del que salió el conjunto guajiroide (p. 155): el
caquetío es **primo** del wayuunaiki, no hermano.

**El «arco norteño» sigue existiendo como hecho geográfico y de contacto** — el
Golfete linda con la Guajira — **pero eso es contacto, no filiación**, y Oliver
no los confunde. Registrar las dos cosas por separado, en la lógica de D7.

Distancias que Oliver **sí** midió: LK–WY 31.3% (2.6 milenios) · LK–baniva 28.7%
· LK–piapoco 25% · LK–achagua 18% (3.8) · WY–achagua 13% (4.6) · LK–island carib
43.7-52.5%. **Del caquetío no hay medición**: no existe lista de 100 palabras.
Su posición es cualitativa y el propio Oliver la llama «tentative».

## Qué le propone a la Capa 2

### Las 441 `hipotético-no-verificado`: **82 adjudicables (18.6%)**

`python curiana_sim/minar_oliver_cap2.py --adjudicar` aplica cuatro claves
derivadas de las correspondencias, sobre el contenido real de
`lexicon_candidatos.py`:

| Clave | n | Veredicto | Fundamento |
|---|---|---|---|
| **A1** | 7 | degradar + **corregir** | *d-* lokona convertida en *t-* caquetía. C1: el caquetío conserva /d-/. `tari`, `tacuty`, `tali`, `te`, `toma`, `tian`, `anucu` — la forma buena es la de *d-*, así que **son reparables, no descartables** |
| **A2** | 13 | degradar | *b-* lokona convertida en *p-* caquetía. C3, con el contraejemplo *para* |
| **A3** | 62 | degradar | derivadas de una forma wayunaiki con /ch/, /sh/ o /ñ/ — fonemas que el guajiro adquirió «not very long ago» (C5). Proyectarlos al s. XV es un anacronismo |
| **A4** | 5 | **sustituir** | el hueco ya lo cubre un caquetío atestiguado en Oliver (*paraca*→`para`, *palii*→`barisi`, *tari*→`dare`…) |
| A5 | 45 | **sin veredicto** | difieren de su fuente solo en vocales, y Oliver **excluye las vocales** de su método (C9). No se puede fingir que se resolvieron |

Sin duplicar: **82 accionables sobre 441**. No es el lote entero, y el resto no
queda validado — queda **sin adjudicar**, que es distinto.

### 8 revisiones al motor (ninguna aplicada)

| Regla | Veredicto |
|---|---|
| `REGLAS_LK_CQ` R13 `^d → t` | **FALSIFICADA** — eliminar |
| `REGLAS_LK_CQ` R5 `^b → p`, R9 `b intervocálica → p` | degradada: no regular (contraejemplo *para*) |
| `REGLAS_WY_CQ` R4 `sh → ch` | sospechosa (C5) |
| `REGLAS_LK_WY` R7 `r ante vocal → l` | sin fundamento fonológico (C8) |
| `REGLAS_WY_LK` R9 `^w → b` | corregible → `^w → o` (C6) |
| `COGNADOS['persona']` | mal emparejado: el cognado de *kaketío* es *kakïtho*, no *lokono* |
| `COGNADOS['mar']` | ampliable: TN *bara-wa* junto a *bagua* |
| `COGNADOS['luna']` | a verificar: Taylor da LK *káthi*, el proyecto usa *katsi* — y sobre *katsi* descansa la regla `ts → t` |

### 10 pares de validación nuevos, con fuente externa

`PARES_VALIDACION` pasaría de **18 a 28**. Con el motor de **hoy** pasan **3 de
10** — y ese es el punto: los 7 fallos son exactamente la lista de reglas a
revisar. **No se corrigen forzando la regla**; eso sería circular.

### 5 entradas caquetías atestiguadas ausentes del lexicón

`auri` 'perro' (p. 151 — el lexicón no tiene ninguna palabra caquetía para
'perro'), `barisi` 'ceniza' (p. 142 — tampoco la tenía), `ada` 'árbol' y
`adabacoa` (p. 144), `daitiao` como variante de `datihao` (p. 147).

## Bitácora — la campaña del taíno, parcela T4 (2026-09-21)

**Qué se le preguntó**: qué comparten de verdad el taíno y el caquetío
ATESTIGUADO, en léxico, morfología y onomástica; y si lo que comparten es
herencia arahuaca común, préstamo de esfera o casualidad. Este capítulo es la
fuente secundaria principal, porque compara las dos lenguas explícitamente.

Propuesta y medición en `6-fusion/cruce_taino_caquetio_2026-09-21.yaml`
(la genera `6-fusion/scripts/cruce_taino_caquetio.py`, re-ejecutable, con
`--check`); las opciones para Miguel, en
`6-fusion/issues-pendientes/taino-caquetio-similitudes-2026-09-21.md`.
**No se tocó el canon** (regla 5).

### Qué dio este capítulo, con página

| p. | qué | cómo quedó en el cruce |
|---|---|---|
| 147 | `/da-/` en `da(i)tia-o` es marca de 1ª sg.; el `/dA-/` está en lokono, taíno y «perhaps Caquetío» (p. 136) | **mismo morfema**, y el paralelo mejor sostenido — pero **ya contado por D11 vía lokono**: repetirlo por la vía taína sería contar dos veces el mismo dato |
| 147 n. 43 | el privativo `/mV-/` es **común a las lenguas maipures** | confirma que el caquetío tiene lo de la familia; **no** acerca el taíno al caquetío más que a cualquier hermana |
| 147 | `/wa- [gua-]/` es marca de **3ª plural** en taíno | el `-gua` caquetío del canon es un **sufijo locativo**: misma sílaba, posición y función contrarias. No es apoyo |
| 148 lista j) | los sufijos toponímicos caquetíos: `-bana`, `-coa/-koa`, `-oa`, `-kiva`, `(e)-bo`, `-wa [gua-]` | **`-oa`, `-kiva` y `-bo` no están en el canon** (ni en `morfemas.yaml` ni en `TODAS_LAS_REGLAS`) y el cruce los mide vivos en la toponimia: 6/78, 4/78 y 5/78. Hueco **propio**, con la cita ya localizada |
| 148 | taíno `pana-pe(n)` y `Agüey-bana`; y el `-bana` bajo 'rodear, cubrir, extensión' | **mismo formante, glosa distinta**: el paralelo taíno **no corrobora D9** ('cerro, sitio alto'), tira hacia el 'ancho/llano' de van Buurt. Y en las 78 formas indígenas de Pané `-bana` da **0** |
| 148 n. 44 | los gentilicios `-ío/-yo` (Luca-yo, Cigüa-yo, Kaket-ío), de **Vescelius, comunicación personal 1982** | **no citable**: no hay dato publicado detrás. Lo que sí está argumentado es `kaket-ío` ~ lokono `kakïtho` (p. 148), y no necesita la nota |
| 149 | taíno `coa` 'palo cavador' junto a la postposición `-coa` | Oliver lo trae como apoyo **semántico** ('lo puntiagudo'), no morfológico: un palo cavador es un **nombre**. No es el mismo morfema |
| 150 | taíno `bara-wa` 'mar' junto al caquetío `para-` | **el mejor cabo suelto de la campaña de `-gua`** (d21.7, hoy sin cita): misma raíz y mismo elemento detrás que `para-gua` |
| 151 | *«one must be careful about some terms (e.g. barbacoa) offered by the Spanish as "native" Caquetío»* | explica el «estrato taíno» que Esteves ve en Paraguaná: `batey`, `mamey`, `caney`, `carey` son castellano antillano. En Pané, `-ey` da **0 de 78** |
| 97 | el estado de la clasificación del taíno: Noble, Taylor, Rouse | resumido con en qué se apoya cada uno en `meta.clasificacion` del YAML |

### Qué NO dio, y hay que decirlo

- **Ni una pareja léxica.** Cruzando las 228 entradas `caquetío-atestiguado`
  contra las 39 taínas atestiguadas del lexicón: **4 conceptos con glosa exacta
  compartida y 0 parecidos** sobre el umbral. Un control **no arahuaco**
  (jirajara/ayomán de [[jahn-1927]], 83 formas comparables) da **12 conceptos
  comparables y el mismo 0**. El taíno **no gana al control**. El lokono sí (5 parecidos
  donde el azar da 0,98; p = 0,000), que es lo que este capítulo sostiene.
- **Ni una correspondencia fonética taíno~caquetío**: sin pares parecidos no hay
  nada que poner a predecir.
- El cruce **por forma sin filtro de glosa** da 15 parejas taínas sobre 0,75 y
  **las 15 son ruido** (`kiba` 'piedra' ~ `cohiba` 'tabaco'; `kasi` 'sol' ~
  `cazabi` 'casabe').

### La reserva de la n. 42, otra vez

Este capítulo es también el que **duda de que `datihao` sea caquetío** (n. 42,
p. 146) y concluye que probablemente fuera *«equally shared by both Taíno and
Caquetío»*. El lexicón lo sigue teniendo como `caquetío-atestiguado` **sin esa
reserva**, y `2-lengua/cognados.yaml` lo empareja con el taíno citando esta
misma página. Es el caso que la skill `minar-fuente` §8 manda tratar con
cuidado, y sigue abierto.

### Deuda nueva que deja esta bitácora

1. **Las 52 entradas taínas del lexicón tienen 0 `procedencia.obra`** (regla 8).
   Mientras no la tengan, cualquier cifra que salga de ellas mide nuestra lista.
2. `2-lengua/cognados.yaml` tiene **16 sets que emparejan CQ con TN**, y sólo 4
   citan a alguien —los cuatro, a este capítulo—. De los otros 12, **4 tienen en
   la columna caquetía una forma que el lexicón etiqueta como taína o lokona**,
   2 son etnónimos circulares y 2 son la misma palabra castellana escrita dos
   veces. Ver el issue §2.4.
3. `auri` 'perro' **sigue etiquetada `achagua`** en el lexicón, tres años de
   proyecto después de que este capítulo (p. 151) la declare la voz caquetía y
   uno de sus tres pilares. Ya estaba en «Qué falta» desde el 2026-08-03.

## Qué falta

1. **Conseguir el Apéndice A de Oliver 1989.** Es lo de mayor rendimiento
   pendiente en toda la fuente: contiene la lista completa de términos caquetíos
   y las 31 listas de Swadesh. No está en el repositorio.
2. **OCR de las Tablas 3-8** (páginas-imagen). La Tabla 3 (reflejos fonémicos de
   12 protolenguas y lenguas) es la única tabla sistemática de correspondencias
   del capítulo, y es la que cerraría las reglas del motor.
3. **Decidir la lengua donante prioritaria.** El lexicón tiene 781 entradas
   wayunaiki frente a 228 lokono — 3.4 a 1 a favor de la hermana que Oliver
   considera **más lejana**. Candidata a decisión en [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision).
4. **Corregir [[01_familia_caquetia]] §2**, que se apoya en la lectura invertida
   del arco norteño.
5. Revisar tres etiquetas del lexicón a la luz de este capítulo: `guaitiao`
   (Oliver lo da como taíno 3pl, préstamo al español), `cachicamo` (Oliver lo da
   como **préstamo del tamanaco**, lengua caribe, p. 145) y `barbacoa`/`maraca`/
   `cacique` («one must be careful about some terms offered by the Spanish as
   "native" Caquetío», p. 151).

## Releído el 2026-09-21 para el taíno (campaña del taíno, T5)

**Qué se preguntó.** ¿Qué dice este capítulo de la relación taíno↔caquetío: es
parentesco, es contacto, o es el español de por medio? Medido sobre el PDF
extraído con `pdftotext`: `Taíno` 62 · `Island Carib` 42 · `Antill` 17 ·
`Hispaniol` 3 · `Arawak` 379 · `Lucay` 0 · `Cuba` 1.

**Qué se halló — y confirma que es parentesco, no esfera.**

- **Salen del mismo nodo, y por puertas distintas.** Oliver hace que el grupo
  que dio taíno e island carib entrara a las Antillas **desde Trinidad y la
  costa oriental de Venezuela**, mientras el que dio el caquetío se fue al
  **oeste** hacia los Llanos, *«following the footsteps of the earliest splinter
  group that was to evolve into Guajiro-Paraujano»*. Divergencia de ≥ 1,8 y
  probablemente 2,6 milenios. Son **primos, no vecinos** — y la ruta lo explica.
- **El punto 5 de arriba es más importante de lo que parecía.** La frase de la
  p. 151 tiene contexto: *«Other terms, such as **maraca** /maraka/ are probably
  of Taíno origin and possibly brought in along with **cacique** /kasike/ and
  many others by the Spanish, all of whom had to go through Hispaniola before
  reaching Venezuela»*. Y [[oliver-1989-cap3]] lo repite dos veces más (p. 241
  n. 83 con `caney`, `fotuto`, `huracán`, `hamaca`; p. 283 n. 131 con
  `naboria`). No es una cautela de paso: es una tesis del autor, dicha tres
  veces en dos capítulos.
- **La reserva sobre `datihao` corta en las dos direcciones.** La n. 42 (p. 146)
  duda de que sea caquetío porque *«Oviedo's long time residence in Hispaniola
  may be a factor here»*. Pero [[oliver-1989-cap3]] p. 212 y [[arcaya-1920]]
  p. 158 documentan que **en Santo Domingo había caquetíos deportados desde
  1513, y que Ampíes conversaba con ellos**. Una voz recogida «en La Española»
  no es automáticamente taína. El argumento de Oliver es simétrico y él sólo lo
  usó en un sentido.

**Qué NO da**: ni una afirmación de contacto taíno↔caquetío en el siglo XV.
Toda la relación que traza es de filiación. Ver
`6-fusion/taino_en_la_esfera_2026-09-21.yaml` §para_las_otras_parcelas.

---

## Bitácora — campaña `-gua` (2026-09-21)

**Qué se le preguntó.** ¿Enuncia Oliver un formante toponímico `-gua`/`-wa`, y
con qué valor? (d21.7: el motor enseña `-gua` = 'región, área amplia' sin clave
foránea.)

**Qué dio — y es el hallazgo de la campaña.** **Sí lo enuncia, y es la única
obra del repo que lo hace.** §2.8, apartado «j) Suffixes /-bana/ and /-coa/»,
**p. 148**:

> «The most common "suffixes" in Caquetío toponyms are those ending in:
> a) -bana · b) -coa/-koa · c) -oa · d) -kiva · e) (e)-bo · **f) -wa [gua-]**»

⚠️ **Da la forma, no el valor.** De los seis glosa tres —`-bana`
'surrounding/expanse', `-coa` «superlativo de la preposición 'en' o 'sobre'»
(coincidiendo con Perea y Perea 1948:87), `-oa` reflexivo— y **nunca vuelve a
f) -wa**. Ninguna glosa, en todo el capítulo, para ese sexto.

**Y dice el valor fonémico, con estas letras** (p. 142, sobre el mismo topónimo
que Esteves segmenta como bari+sigua):

> «in the Borojó area there is a river designated today as **bari-si-gua
> (gua=/wa/)** and in the Bariro area we find bari-si-gu()-ita»

Es el dato que D5c (#36) pedía, escrito por el autor: **`gu` ante vocal es /w/**.
Con él, el lema del morfema del motor sería `-wa`.

**Y una explicación rival para `parawa`** (p. 150): da el taíno de 'mar' como
`/bara-wa/` junto al guajiro `/palaa'/`. El `-wa` de `parawa` tiene hermano
arahuaco dentro de la misma palabra, así que `paragua` no necesita leerse como
`para` + un locativo.

**Lo que NO dio.** Cero glosa de `-wa`. Cero uso de 'region' referido a un
sufijo caquetío. La lista de la nota, «8 afijos, con página y valor», no
recogía `-wa`: queda añadido aquí.

> Medición entera: `6-fusion/propuesta_gua_procedencia_2026-09-21.yaml`
> (la escribe `6-fusion/scripts/medir_gua_procedencia.py`). Opciones para
> Miguel: `6-fusion/issues-pendientes/gua-procedencia-2026-09-21.md`.

## Enlaces

[[oliver-1989-cap3]] · [[zavala-reyes-2015]] · [[brinton-1871]] · [[perea-alonso-1942]] · [[gatschet-1885]] · [[jahn-1927]]
