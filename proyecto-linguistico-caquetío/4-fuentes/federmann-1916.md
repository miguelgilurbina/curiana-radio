---
tipo: fuente
obra: "Narración del primer viaje de Federmann a Venezuela"
autor: "Federmann, Nicolás (trad. y notas de Pedro Manuel Arcaya)"
anio: 1916
publicacion: "Caracas, Lit. y Tip. del Comercio, 1916. Traducción castellana de Arcaya hecha sobre la FRANCESA de Ternaux-Compans (1837), no sobre el alemán — Arcaya lo declara (p. 20: «En el texto francés, no sabemos si también en el original alemán…») —, con notas del traductor francés y de Arcaya. El original es la *Indianische Historia* (Hagenau, Sigmund Bund, 1557)"
edicion_del_ejemplar: "ejemplar de la University of North Carolina at Chapel Hill digitalizado por archive.org (narraciondelprim00fede); + el original alemán de 1557 (ejemplar de la John Carter Brown Library, indianischehisto00fede) y la reedición alemana de Klüpfel 1859 (nfedermannsundhs00kl)"
genero: cronica
local:
  - "fuentes_caquetios/Federmann_1916_Narracion_Primer_Viaje_Arcaya.pdf"
  - "fuentes_caquetios/Federmann_1916_Narracion_Primer_Viaje_Arcaya.txt"
  - "fuentes_caquetios/Federmann_1557_Indianische_Historia.pdf"
  - "fuentes_caquetios/Federmann_Kluepfel_1859_Reisen_texto_aleman.pdf"
  - "fuentes_caquetios/Federmann_Kluepfel_1859_Reisen_texto_aleman.txt"
paginas: "135 impresas (154 pp. de PDF; impresa = pdf − 10, medido en 100 páginas)"
capa_texto: si
descargado: 2026-09-22
origen_digital: "Internet Archive — https://archive.org/details/narraciondelprim00fede (1916) · https://archive.org/details/indianischehisto00fede (1557) · https://archive.org/details/nfedermannsundhs00kl (1859)"
acceso: >-
  Dominio público. 1916: traductor Pedro Manuel Arcaya (1874-1958), fallecido
  hace más de 60 años (Venezuela: vida + 60) y publicada antes de 1931 (EE. UU.);
  archive.org no la restringe. 1557 y 1859: sin derechos. Descargado el
  2026-09-22. 1916: 9.359.616 bytes, sha256
  dbe79cd85abf437d58ad54e54b014924962605e696fa24ef3c86d7bfd1ad7ec5.
  1557: 25.545.486 bytes, sha256
  9bf5cfed6ce099de291714c7825baad34db82c263f6ad020705b2db7c423cde8.
  1859: 12.004.554 bytes, sha256
  f6c85158b4378308e4bdbdb1ab02787a514734bdc7167d4e04e7d751961d2cbe.
estado_minado: parcial
cobertura: "minado 2026-09-23 (minería 3): la costa (cap. I Paraguaná, II-III Coro, XIII-XIV vuelta por la costa oriental), la lengua (intérpretes, costa frente a interior, voces y nombres en la grafía de 1557), el seretón (cero medido) y la fauna, cotejado con el alemán y 1557 en imagen; del interior sólo caps. VIII y XII y lo que ya se citaba de segunda mano. SIN leer de corrido: caps. VI-VII y IX (sólo sondas). 2026-09-23 (cc.5): leídos los pasajes de los guaycaríes de los caps. X-XI (1916 pp. 84-101), cotejados con 1557 [77]-[78] y [83] en imagen. Propuestas: 6-fusion/federmann_1530_costa_2026-09-22.yaml y 6-fusion/guaiqueries_manaure_dabajuroide_2026-09-23.yaml"
prioridad: alta
tareas: [F12]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
minado: 2026-09-23
aliases: ["Federmann", "Federmann 1916", "Narración de Federmann", "Indianische Historia"]
---

# Federmann 1916 — *Narración del primer viaje*

## 🔴 Aviso de polity antes que nada (regla 4)

[[arcaya-1920]] sitúa el grueso de Federmann con precisión:

> "De los Caquetíos del **Yaracuy y Barquisimeto** hay noticias detalladísimas en
> la Narración de Federmann (**capítulos VIII y XII**)"

**Eso no es la polity que simulamos.** Modelamos la costera del Golfete
(`curiana_polities.py`); Barquisimeto y los Llanos son polities distintas, y
Oliver §3.8 documenta que confundirlas es el error clásico. Nada de los caps.
VIII y XII entra al corpus costero sin marcarlo explícitamente.

Ver [[polities-caquetias]] y [[oliver-1989-cap3-vecinos]].

## Lo que trae, y a qué polity pertenece

**Barquisimeto / Valles del Turbio** — cifras de poblamiento (pp. 109-110 según
la obra secundaria que Miguel está consultando, pendiente de identificar):

> "Paré cerca de quince días en sus aldeas; son en **número de veinte y tres** y
> todas situadas a la margen del río, a distancia de una legua o media legua una
> de otra… estas aldeas podrían reunir en medio día **treinta mil hombres**.
> Además, sus aldeas están **fortificadas** […] porque son enemigos de las
> **cuatro naciones vecinas** […] De todos los países que atravesamos en ninguna
> parte encontramos una población tan numerosa en tan pequeño territorio, ni
> aldeas tan considerables ni tan fortificadas"

Aldeas fortificadas, hostilidad con cuatro vecinos, asentamiento lineal sobre el
río, agregación defensiva. Es un retrato **denso y distinto** del de la costa. Si
algún día se modela una segunda polity (#83, D14), ésta es su fuente base.

**Costa / Coro** — el arranque del viaje sí toca la polity costera:

> "hice mis preparativos y el martes 12 de septiembre me puse en camino con
> ciento diez españoles a pie y dieciséis a caballo, acompañados por **cien
> indios llamados Caquetíos** que llevaban nuestros víveres y todo lo necesario
> para nuestra subsistencia o defensa"

Cien porteadores caquetíos reclutados desde Coro: dato de relación con los
españoles y de capacidad de movilización, ese sí del litoral.

**Yaracuy** (pp. 62-63) — densidad, y la cita estructural del proyecto:

> "creo que les sería fácil reunir en un día hasta **veinte mil guerreros**.
> Aunque los habitantes de todas estas aldeas son de la **misma nación, no están
> bajo el dominio de un solo señor** […] no están todos aliados, pero forman
> **pequeñas confederaciones de dos, tres o cuatro aldeas**. Sus aldeas son a
> veces de media legua de largo y no tienen sino una sola calle o dos cuando
> más, y **una casa la habitan a menudo cinco y hasta ocho familias**"

⭐ *"de la misma nación, no están bajo el dominio de un solo señor"* es
testimonio ocular del s. XVI de que **"caquetío" nombra una etnia, no una unidad
política** — el respaldo textual de la regla 4 y del modelo de
`curiana_polities.py`. Y "cinco a ocho familias por casa" es dato de residencia
que toca [[mapa-familia]].

## Estado

~~No localizada.~~ **En el repo desde el 2026-09-22** (ver bitácora al pie): la
edición de 1916, el original alemán de 1557 y la reedición alemana de 1859.
Las citas de arriba vinieron de segunda mano y **no se han cotejado todavía**
con el texto: la página que dan («pp. 62-63», «pp. 109-110») es de la obra
secundaria, no necesariamente de la de 1916.

> ⚠️ **Cotejadas el 2026-09-23** (bitácora al pie): el texto coincide, pero
> **las páginas están cambiadas** — Barquisimeto (23 aldeas, 30.000 hombres,
> fortificadas) es pp. 62-63; el Yaracuy/Vararida (20.000 guerreros, «misma
> nación», confederaciones, cinco a ocho familias) es pp. 109-110.

Índice: [[INDICE_FUENTES]]

---

## 2026-09-11 — una pregunta concreta esperando a esta fuente

Miguel, al fallar las voces de nivel C del dictado de Medina: «el ceretón está
presente tanto por **Federmann** y se mantiene hasta el día de hoy en mitos».

**No se ha podido verificar**: esta obra sigue `no-disponible` en el repo. Se
buscó lo que sí se podía —la forma con permutación laxa (`seretón`, `ceretón`,
`cerretón`, `zeretón`) y el concepto del hombre que se transforma— en los **27
textos extraídos**, y el resultado es **cero** en ambos. Eso mide el alcance
del repo, no la memoria de Miguel (regla 6): Federmann es justamente el texto
que falta.

Por eso la prioridad sube de `media` a `alta`. Ya no es «una crónica más que
convendría tener»: es la fuente que decidiría si el **seretón** es un hecho de
creencia con atestación del s. XVI y continuidad hasta hoy —de lo más fuerte
que podría tener el corpus— o solo una voz del habla viva recogida por Medina.

Búsqueda: `6-fusion/scripts/buscar_sereton.py`.

---

## 2026-09-22 — conseguida: tres ediciones, en el repo (campaña minería 3, F1)

**Qué se bajó y de dónde** (todo de Internet Archive, dominio público; tamaños
y sha256 en `acceso`):

| Archivo | Qué es | Texto |
|---|---|---|
| `Federmann_1916_Narracion_Primer_Viaje_Arcaya.pdf` + `.txt` | la edición que cita el vault: traducción de Arcaya, Caracas 1916, 154 pp. de PDF | capa OCR del ítem, `pdftotext` 192 KB; **impresa = pdf − 10** (medido en 100 páginas) |
| `Federmann_1557_Indianische_Historia.pdf` | el **original** alemán (Hagenau 1557), ejemplar JCB, 144 imágenes, sin paginar | la capa de texto es **basura** (Fraktur mal leído): se lee en imagen |
| `Federmann_Kluepfel_1859_Reisen_texto_aleman.pdf` + `.txt` | reedición del alemán por Klüpfel (Stuttgart, Litterarischer Verein, 1859), en tipo romano | OCR legible, 452 KB; **impresa = pdf − 8** en el tramo de Federmann |

**⚠️ Lo que cambia cómo se lee la de 1916 (medido al descargar, sin minar).**
Arcaya **no tradujo del alemán**: tradujo la versión **francesa** de Ternaux-
Compans (1837) y lo dice él mismo en nota (p. 20: no sabe si un error de fecha
está «también en el original alemán»). Además conserva las notas del
«traductor francés» junto a las suyas. Toda forma indígena, número o nombre
que vaya a decidir algo se **coteja con el alemán** (1557 en imagen, o Klüpfel
1859 por texto): la cadena es alemán → francés → castellano, y cada eslabón
pudo mover una grafía (minar-fuente §8, el caso Brinton/Las Casas).

**Estructura (medida en el índice, pp. 133-135):** nota del traductor p. 3,
dedicatoria p. 5, dieciséis capítulos pp. 9-129. Lo que toca la polity
costera son el **cap. I** (desembarco en **Paraguaná**, la india rescatada por
Ampíes, el camino a Coro, pp. 9-22) y los caps. **II-III** y **XIV** (Coro,
salida con los cien caquetíos porteadores, vuelta). Los caps. **VIII** (p. 59)
y **XII** (p. 107) son los «Caquetíos» del interior (Yaracuy/Barquisimeto):
otra polity (regla 4). Las notas de Arcaya identifican lugares con nombres
modernos (p. ej. la aldea del cap. I = «Hurehurebo», Jurijurebo): eso es
Arcaya en 1916, no Federmann.

**Medido al descargar, sin leer todavía:** `caquet` sale 42 veces en el `.txt`
de 1916, `intérprete|lengua` 28, `tigre` 8. **`seretón` y variantes
(`seret`, `ceret`, `cerret`, `zeret`) dan 0** en la de 1916 — cero de consulta,
no de fuente, hasta que se lea el alemán y se busque el concepto (regla 6).

**Qué preguntarle** (el encargo del minero está en
`6-fusion/issues-pendientes/encargo-mineria-federmann.md`): la Paraguaná y el
Coro de 1530 (pueblos, casas, jefes, Manaure y su gente, lengua e intérpretes,
comida, fauna), el seretón, y los caps. VIII y XII marcados como la otra
polity.

---

## 2026-09-23 — minada la costa, cotejada con el alemán (minería 3)

**Qué se preguntó**: qué dice Federmann de la gente de la costa —Paraguaná y
Coro— en 1530-1531; la lengua y los intérpretes; el seretón; la fauna; y, con
`polity: interior`, los caps. VIII y XII. Propuesta entera, con página y
eslabón por dato: `6-fusion/federmann_1530_costa_2026-09-22.yaml`.

**Cómo se lee esta obra (añádase a leer-fuente §5):**

- La cadena tiene **cuatro** eslabones: un diario notarial castellano perdido
  (Federmann dice que sólo lo tradujo, p. 122) → alemán 1557 → francés de
  Ternaux 1837, que **normalizó los nombres propios** (nota en p. 124) →
  Arcaya 1916, que tradujo del francés (lo dice en la **p. 2**, no sólo en la
  nota de la p. 20).
- 1557 no tiene paginación: se cita por la página `[n]` que Klüpfel 1859 marca
  en su texto. Imagen del PDF (1-based) = `[n]` + 10 entre [9] y [48], y
  + 12 en [111]-[112]: el desfase **deriva**.
- Klüpfel: impresa = pdf − 8. Su OCR falla en los nombres (`Ruynari`,
  `Caquelios`, `Tohtietsch`); toda forma que decide algo se miró en 1557.
- Voces que la 1916 pone y el alemán no: «botuto» (alemán: `hörner`, cuernos).
  Nombres que la 1916 junta y el alemán separa: «Vararida» es el nombre
  indígena y «el valle de las damas» el que le pusieron los españoles.

**Qué se halló (lo que más pesa):**

- **La lengua de la costa y la del interior.** Federmann no creía que los
  caquetíos de Barquisimeto, a 73 Meilen y tras cuatro lenguas ajenas,
  hablaran como los de Coro; la buena noticia le pareció increíble (1557 [46]).
  Y en los hechos, un caquetío de Coro sirve de `Tolmetsch` en Barquisimeto y
  los mismos intérpretes sirven en el valle del Yaracuy. Junto a Pérez de
  Tolosa 1546 («aunque algo difieren en la habla á los de Coro», t. II
  p. 234): una lengua de la costa a los llanos, con variación.
- **Paraguaná en enero de 1530**: pesca nocturna con fuego desde la orilla;
  una aldehuela de tres casas con unas dieciséis personas en una; agua lejos;
  «toda clase de peces»; miedo a la trata (el alemán dice «a menudo»);
  **Miraca en 1530**, ocho años antes que la carta de Bastidas que abre hoy la
  cadena de nodo-031.
- **Manaure** sale una sola vez, como `Manuaury` (1557 [112]): los cristianos
  «viven en Coro, en la tierra del cacique Manuaury», dicho a caquetíos de la
  costa del Yaracuy.
- **El etnónimo**: la primera mención del original es `Caquecios` (1557
  [19]); luego `Caquetios`.
- La 1916 **invierte** un pasaje: «excepto los que viven cerca de Coro»; el
  alemán dice «tanto en torno a Coro como aquí» (1557 [48]).
- **Interior**: las páginas de las citas de segunda mano estaban cambiadas
  (arriba); y la frase más limpia para la regla 4 es otra: los caquetíos del
  valle, «aunque de una nación» con los de Barquisimeto, «no son amigos»
  (Klüpfel p. 70).

**Qué NO se halló (ceros medidos):**

- **El seretón**: cero de la forma (con permutación c/s/z, e/a, r/rr) y cero
  del concepto de transformación, en la 1916 y en el alemán. Lo que hay son
  los **enanos** ayamanes de la sierra (`Zwergen`) y una enana que Federmann
  dejó en Coro (1557 [35]): la raíz probable del «enano de los Welser» del
  barrido web, no del hombre que se vuelve animal.
- Ninguna **palabra** caquetía: las voces que Federmann glosa («Canoa, also
  heissen der Indios schiff», Hamaca, Barbacoa, Buhio, Mahys, Macana) son del
  escribano castellano; ninguna es caquetío atestiguado.
- De la **dieta vegetal** y los **animales** de la costa, nada salvo peces.
- De las **costumbres de los de Coro**, nada: promete tratarlas «más abajo» y
  no lo hace.
- Que la india de Paraguaná fuera **hija de Manaure** no lo dice Federmann:
  es una cadena de Arcaya (Castellanos + carta de Ampíes).

**Qué falta:** caps. VI-VII (Cayones, Xaguas) y IX-XI (Cuybas, Guaycaríes,
la laguna) sin leer de corrido; los nombres del interior sin cotejar en 1557;
la carta de Ampíes (Fernández Duro 1885 t. II pp. 207-218) sin clave propia en
la bibliografía.

---

## 2026-09-23 — campaña cc.5 (asiento de Manaure, guaiqueríes, cronología dabajuroide)

**Qué se preguntó**: el pasaje de los guaycaríes con caquetíos que Miguel
recordaba, verbatim y con página, en la 1916 y en el alemán.

**Qué se halló** (visto en imagen: 1916 pp. 90 y 94, pdf 100 y 104; 1557
imágenes 87-88 y 93):

- **Cap. XI, pp. 89-90 = 1557 [77]-[78]**: guaycaríes y caquetíos viven en
  paz en el mismo territorio, se necesitan, hacen mercado —pescado por frutas y
  víveres—, «pero cada una habita aldeas distintas». El alemán dice más: los
  caquetíos viven «enthalb vñ her enhalb» (a los dos lados del río) y las dos
  naciones «vnthereinander gemischt» (mezcladas) «doch iede in sondern
  Pueblos». Glosa marginal: «Guaycari kolschw[artz] vischer». Aquí el
  etnónimo va `Caquecios`.
- **p. 94 = [83]**: dos guaycaríes que sabían caquetío porque las dos naciones
  viven mezcladas; **p. 95 = [83]**: la pesquería-mercado de pocas casas;
  **pp. 92 y 100**: el señor de Itabana con caquetíos sujetos y la alianza de
  guerra del cacique guaycarí con el caquetío de Caraho.
- **Desfase 1557**: [77]-[78] = imágenes 87-88 y [83] = 93 (+10, como entre
  [9] y [48]). Klüpfel: el pasaje es p. 57 y el de la lengua p. 61.
- La 1916 entiende «beschicket ich den Cacique … derselben Nation» como «mandé
  el cacique que había conducido, a su aldea»; el alemán parece decir que
  Federmann mandó llamar al señor de los guaycaríes, que tiene sus pueblos a
  milla y media del agua. Lectura nuestra, declarada en la propuesta.

**Qué NO se halló**: la «descripción» de los guaycaríes que Federmann promete
no llega (cero de `negr`/`pintad` fuera del cap. XI; cero de `schwar` en
Klüpfel fuera del pasaje). Ninguna palabra guaycarí. Y **no dice**
«supusieron eran Guayqueríes»: los nombra sin duda (p. 84; Klüpfel p. 55). Ese
«supusieron» de `etnias.yaml` etnia-002 viene de Brito Figueroa.

**La nota (a) de Arcaya, p. 89**, es del editor: no sabe si son los guaiquerís
de Margarita; «de éstos se cree que eran rama de la familia Guarauna».

Propuesta: `6-fusion/guaiqueries_manaure_dabajuroide_2026-09-23.yaml`; issue: `6-fusion/issues-pendientes/guaiqueries-manaure-dabajuroide-2026-09-23.md`.

## 2026-09-24 — campaña cosmovisión marina

**Se preguntó:** ¿dice esta obra algo del MAR en la vida simbólica, ritual o
cosmológica de los caquetíos de la costa (un ser, un mito, un rito, una
ofrenda, un tabú)? Rama `campana/cosmovision-marina-2026-09-24`; propuesta en
`6-fusion/cosmovision_marina_2026-09-24.yaml`.

**Cómo:** Barridas la traducción de 1916 y la edición alemana de 1859 (que trae además a Staden: sus ventanas son tupinambá y no cuentan). Medido con `6-fusion/scripts/medir_cosmovision_marina.py`: `federmann1916`: 3 ventanas creencia × mar (3 con un nombre de la costa occidental cerca), 0 creencia × cielo de control; `federmann1859`: 11 ventanas creencia × mar (0 con un nombre de la costa occidental cerca), 13 creencia × cielo de control.

**Se halló:** El dato más fino del barrido: los AYAMANES del interior «no se adornan sino con pequeñas piedras negras y brillantes […] y también de conchas marítimas que compran a otras naciones y que son raras en este pueblo tan lejano del mar que no lo conocen ni a sus orillas se han aproximado nunca» (p. 45). La concha vale lejos del mar: es un bien de prestigio que la costa exporta (regla 4: ayamán; la costa es el origen). El «botuto» de guerra de la p. 35 es del interior y es palabra de Arcaya, el traductor.

**No se halló:** Cero creencia del mar en la costa (cap. I Paraguaná, II-III Coro).
