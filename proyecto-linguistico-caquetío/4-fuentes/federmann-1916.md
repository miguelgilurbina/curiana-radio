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
estado_minado: sin-minar
cobertura: "nada minado todavía; texto extraído y estructura medida al descargar (ver bitácora 2026-09-22)"
prioridad: alta
tareas: [F12]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
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
