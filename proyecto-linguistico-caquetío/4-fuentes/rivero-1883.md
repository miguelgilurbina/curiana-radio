---
tipo: fuente
obra: "Historia de las Misiones de los Llanos de Casanare y los ríos Orinoco y Meta"
autor: "Rivero, Juan"
anio: 1883
publicacion: "Bogotá, Imprenta de Silvestre y Compañía, 1883 (ed. de Ramón Guerra Azuola; escrita hacia 1736)"
edicion_del_ejemplar: "ejemplar de la University of California digitalizado por Google, en archive.org (historiadelasmi00rivegoog)"
genero: cronica
local:
  - "fuentes_caquetios/Rivero_1883_Historia_Misiones_Casanare.pdf"
  - "fuentes_caquetios/Rivero_1883_Historia_Misiones_Casanare.txt"
paginas: "475 pp. de PDF; impresa ≈ pdf − 21 en el cuerpo (medido: el pasaje de la p. 21 cae en el pdf 42), con tramos a − 19: leer el número impreso"
capa_texto: "no — el PDF es sólo imagen; el .txt es el OCR del ítem de archive.org (djvu.xml) pasado a texto con un salto de página por hoja, así que la página del PDF se cuenta como con pdftotext"
descargado: 2026-09-22
origen_digital: "Internet Archive — https://archive.org/details/historiadelasmi00rivegoog"
acceso: >-
  Dominio público: impreso en Bogotá en 1883, autor Juan Rivero (1681-1736);
  archive.org lo marca NOT_IN_COPYRIGHT. Descargado el 2026-09-22:
  36.489.039 bytes, sha256
  43bcb5c8dfda33b632e96599a4e575eef503b4b1bce231f434f509bfde92ef91. Hay una
  reedición de 1956 en archive.org (historiadelasmis00rive) que NO se bajó:
  su aparato editorial de 1956 puede tener derechos.
estado_minado: parcial
cobertura: "minado 2026-09-23: todas las menciones de caquetíos (raíz medida, 12 aciertos, leídos en contexto) y los pasajes de lengua, variación e intérpretes; voces achaguas con glosa (4 vistas en imagen, 8 sólo OCR). FALTA: fauna y flora del Libro I (pp. 1-20), el resto de la etnografía achagua (pp. 102-118) por esferas, y ver en imagen las 8 voces OCR"
prioridad: media
tareas: [F12]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-23
minado: 2026-09-23
aliases: ["Rivero 1883", "Juan Rivero", "Historia de las Misiones de los Llanos"]
---

# Rivero 1883 — *Historia de las Misiones de los Llanos*

## 🔴 No es caquetío — es achagua (regla 4)

Los **achaguas** son otro pueblo **arahuaco**, de los llanos del Casanare, Meta y
Apure. Nada suyo entra al corpus costero. Se registra porque es un **pariente
lingüístico** con documentación colonial abundante, y por un pasaje concreto.

## ⭐ El pasaje: un continuo dialectal arahuaco, descrito en su época

> "La Nación Achagua ha sido la más numerosa de cuantas pueblan estas comarcas
> […] **Más de veinte naciones o provincias contaban los Achaguas bajo un mismo
> idioma**, si bien había y aun hay, algunas diferencias, como las que existen
> en Castilla entre portugueses y gallegos, asturianos y otros." (p. 21)

Una lengua arahuaca repartida en **veinte provincias**, con variación interna que
el cronista compara con la variación regional peninsular — es decir, mutuamente
inteligible pero perceptible.

**Eso es el escenario sociolingüístico que el experimento simula**, atestiguado
para una lengua hermana. Toca [[DISENO_KOINE]] y la variación dialectal de
`curiana_social.py`: da un referente histórico de cuánta divergencia cabe dentro
de "un mismo idioma" en el mundo arahuaco de tierra firme.

## Dónde buscarla

Obra clásica, edición de 1883 (escrita hacia 1736). Suele estar digitalizada en
repositorios colombianos y en Internet Archive. Emparejar con
[[gilij-1780-1783]], que ya está en el repo y cubre el Orinoco.

## Estado

~~No localizada.~~ **En el repo desde el 2026-09-22** (ver abajo).

## 2026-09-22 — conseguida (campaña minería 3, F1)

El pasaje de las «veinte Naciones ó Provincias» bajo «un mismo idioma» está en
el pdf 42 (p. 21 impresa), así que la cita de la ficha se sostiene en esta
edición — falta verla en imagen antes de citarla.

⭐ **Lo que el vault no esperaba, medido al descargar (sin leer):** Rivero
nombra **caquetíos en los Llanos del Casanare** — presos «Caquetíos y
Achaguas» en una entrada (pdf 48 y 50), el pueblo misional de «Caquetíos de
Pauto» (pdf 222), un misionero «lidiando con la lengua» del pueblo de Pauto
(pdf 172; el OCR dice `Caquetá`/`Caquetd` y hay que verlo en imagen) y
caquetíos en el Guaviare en 1723 (pdf 411). Si la lectura se sostiene, es
**una tercera polity caquetía con lengua propia en el s. XVIII**, lejos de la
costa: comparanda interna, nunca dato costero (regla 4). Junto con el «algo
difieren en la habla á los de Coro» de [[perez-de-tolosa-1546]] (p. 234), es
material para la variación dentro del caquetío.

**Qué preguntarle** (el encargo del minero está en
`6-fusion/issues-pendientes/encargo-mineria-rivero.md`): los caquetíos del
Casanare y su lengua; el continuo achagua de las «veinte provincias»; y lo que
diga de cómo se aprendían y se hablaban esas lenguas en la misión.

## 2026-09-23 — minada (campaña minería 3, rama `campana/mineria3-rivero`)

Propuesta en `6-fusion/rivero_1883_2026-09-23.yaml`. Issue para Miguel en
`6-fusion/issues-pendientes/rivero-caquetios-casanare-2026-09-23.md`.

**Qué se preguntó.** Los caquetíos de los Llanos y su lengua; el continuo
achagua; voces achaguas con glosa; fauna.

**Cómo se lee esta obra.**

- **La ortografía:** Rivero escribe `Caquetíos` y también **`Cacatíos`**
  (p. 54). Un grep de `caquet` se come esas dos, que son las que dicen que
  Pauto era caquetío. La raíz des-guionada da 12 aciertos: 10 de caquetíos,
  el río Caquetá del prólogo de 1883 y un falso positivo.
- **Desfase:** pdf − 21 hasta la p. 201 y pdf − 19 desde la p. 283 como
  muy tarde (medido en la cabecera de cada página citada).
- **El OCR tiene fallos:** lee mal cabeceras (pdf 75 dice «64»; la imagen,
  54) y se come la cursiva (`numerraidary` sale «n^vhonumverraidary»).

**Qué se halló.**

- **Caquetíos.** Hay dos grupos. El de Pauto y Tame (piedemonte, reducido
  desde antes de 1629) incluye un pueblo «*Caquetíos de Pauto*» en 1666. El
  de Barragua, Airico y Guaviare (gentiles) es el que los achaguas llaman
  «*Tamudes*» (p. 29). Sobre la lengua hay **una sola línea**: «la lengua
  *Caquetá* de su pueblo de Pauto» (p. 151). La IMPRESIÓN dice Caquetá; no
  es error del OCR. Rivero no da voces caquetías ni la compara con el
  achagua.
- **Tamude.** Rivero no une *Tamudes* con *mude* 'primo'. *mude* es el
  saludo al huésped «aunque nunca lo sean» (p. 420). La etimología que está
  en `parentesco-021` es de Jahn 1927.
- **Continuo achagua.** La cita de la p. 21 se sostiene en imagen, con
  «aun hay **ahora**» (la cita de arriba lo omitía). Hay además dos
  descripciones de un achagua de segunda lengua «por infinitivos» (pp. 316 y
  401). Y la escala de la variación: achagua/saliva es la de «vizcaínos y
  castellanos» (p. 194).
- **Voces achaguas.** 12 voces con glosa, 4 de ellas vistas en imagen.
  Fauna: 4, al paso.

**Qué NO se halló (medido).** Intérpretes o catecismos caquetíos con
nombre; el parecido entre caquetío y achagua; caquetíos en el Sinaruco
(Jahn los pone allí, pero no salen de esta edición); Manare (Rivero sólo
nombra Chire, a medio día del río Pauto).

**Una atestación, no dos.** Todo lo de Jahn 1927 sobre los caquetíos del
Casanare sale de aquí (y de Gilij), y la polity `llanos` de
`curiana_polities.py` se apoya en Jahn.

**Deuda.**

- Gilij t. IV p. 487 (Manare, caquetíos del Orinoco).
- La edición de 1956, para la p. 151.
- 8 voces sin ver en imagen.
- El Libro I para fauna y flora.
- La etnografía achagua (pp. 102-118) por esferas.

Índice: [[INDICE_FUENTES]]
