---
tipo: fuente
obra: "Historia de las Indias, tomo I"
autor: "Las Casas, Bartolomé de"
anio: "1875 [c. 1561]"
genero: cronica
local: "fuentes_caquetios/Las_Casas_1875_Historia_Indias_vol1.pdf"
paginas: 613
capa_texto: si
estado_minado: minado
cobertura: "caps. XL-LXVIII pasaje a pasaje (primer viaje y La Española), por léxico taíno (2026-09-21, T2) y por la etnohistoria del contacto (2026-09-22, T7); el tomo entero por patrón"
desfase_pagina: "NO es constante: el PDF es el ebook de Gutenberg y su pie es un contador propio. Se ancla por CAPÍTULO con 6-fusion/scripts/mapa_capitulos_las_casas.py"
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["Las Casas 1875", "Historia de las Indias"]
---

# Las Casas 1875 [c. 1561] — *Historia de las Indias*, tomo I

## Qué es

Durante tres sesiones fue **una fuente de rendimiento nulo, y eso estaba
documentado tres veces**. El 2026-09-21 dejó de serlo: no cambió la fuente,
cambió la pregunta. Se le preguntó por **taíno** —no por caquetío, no por
corpus cultural— y el tomo I dio 26 voces con glosa y 10 pasajes sobre la
lengua misma. La lección vale más que el dato: *«un hallazgo negativo bien
medido baja la prioridad de una fuente», pero sólo para la pregunta que se le
hizo.*

## Estado técnico (verificado 2026-07-29)

2.2 MB · 613 páginas · capa de texto **sí** (47K caracteres en 30 pp.) ·
`pdftotext` o `pypdf`.

## Qué ha dado: nada, en tres intentos

| Sesión | Qué se buscó | Resultado |
|---|---|---|
| 1 — familia | `sobrino…cacique`, `cacicazgo`, `hereda…cacic` | sin coincidencias relevantes |
| 3 — creencia | `behique`, `cemí`, `areíto` | sin coincidencias en el vol. 1 |
| 4 — transmisión | `enseñ*`, `doctrina`, `educaci*`, `orator*` | casi todos los hits son prólogo apologético, biografía de Colón o catequesis cristiana — **no pedagogía indígena** |

## Por qué es esperable

El tomo I cubre sobre todo Antillas y Colón, y **termina antes** de que Ampíes
funde Coro (1527). La sucesión cacical de Coro que documenta
[[oliver-1989-cap3]] viene de fuentes de archivo (probanzas, obispo Martí), no
de Las Casas. La religión taína está en otros pasajes y volúmenes.

## Sesión 5 — campaña del taíno, 2026-09-21 (parcela T2)

Propuesta completa en `6-fusion/taino_las_casas_1875.yaml`; la cola de decisión
en `6-fusion/issues-pendientes/taino-lascasas-pane-brinton-2026-09-21.md`.

### ⚠️ El PDF no es el libro de 1875

Es el **ebook de Project Gutenberg #49298** llevado a PDF. Su pie de página es
un contador propio: coincide con el índice del pdf en **609 de 613** páginas.
La paginación de 1875 **no está en el cuerpo del texto**.

Se recupera porque **el índice original de 1875 sobrevive** en las páginas pdf
572-596, con sus números impresos. De ahí sale el mapa capítulo → (página
impresa, página pdf) para los 82 capítulos, que emite
`6-fusion/scripts/mapa_capitulos_las_casas.py`. El desfase **no es constante**:
va de +8 en el cap. I a +69 en el LXXXII, así que una cita se ancla por
capítulo y la página impresa dentro de él es interpolación declarada.

Para el índice hace falta `pdftotext -layout`: es una tabla a dos columnas y
sin `-layout` los números se mezclan con la prosa.

### Qué dio

| Qué se preguntó | Resultado |
|---|---|
| voces taínas con glosa, página y atribución | **26**, caps. XL-LXVII |
| qué dice sobre la lengua misma | **10 pasajes**: 3 de acento, 2 de la tesis de «toda una lengua» (las dos en boca de Colón), 1 de transcripción defectuosa, 2 de variedades, 1 de etnónimo, 1 de intérpretes |
| variedades e inteligibilidad entre islas | ver abajo |

Las piezas: `nacan` 'medio' con análisis morfológico del cronista
(`Cuba`+`nacan`), `turey` 'cielo', el trío `caona`/`nozay`/`tuob` para 'oro' en
tres zonas, `cacique` y `nitayno` con sus rangos ordenados, `cazabí` cuatro
veces, `çabana`, `hutía`, `iguana`, `cupey`, `guaminiquinajes`.

### Lo que corrige a lo que se creía

- **«la penúltima luenga» NO está en el tomo I** (`penultima` = 0). Lo que hay
  es «la última sílaba luenga y aguda» (×2, `Guanahaní` y `Haytí`) y «la última
  aguda» (×1, `axí`). La frase famosa es del **lib. III cap. 21**, que no
  tenemos, y llega por [[brinton-1871]] p. 14 nota 28: «llamábanse en su
  lengua, Cibon-eyes, la penúltima sílaba luenga».
- **La tripartición de lenguas es más floja de lo que se dice.** El cap. LXVII
  dice que mazoriges y cyguayos «tenían diversas lenguas de la universal de
  toda la isla» y acto seguido: «No me acuerdo si diferian estos en la lengua
  [...] puesto que conversé hartas veces con ambas generaciones». La versión
  nítida está en la *Apologética*, que no tenemos.
- **`ciguayo` escrito así aparece 1 vez; `cyguayo`, 4.** Un grep con la grafía
  moderna se pierde 4 de 6 (regla 6).
- **`macana` sale 2 veces y las dos son la misma línea del epígrafe** del cap.
  LXVII (cabecera + índice). En el cuerpo el arma se describe sin nombrarla:
  «una espada de tabla de palma [...] no aguda, sino chata».

### Qué NO dio (medido con todas las grafías del XVI)

**Religión taína: cero.** `cemi`/`zemi`/`çemi` = 0, `behique`/`buhiti` = 0,
`areito`/`areyto` = 0, `cohoba` = 0, `Yocahu` = 0, `Atabey` = 0, `Guabancex` =
0, `bagua` = 0, `duho` = 0, `naboria` = 0. Confirma las sesiones 1, 3 y 4, esta
vez con la lista completa. `opia` da 77 y **es todo ruido** (propia, copia).
También a 0: `barbacoa`, `batea`, `jagua`, `guayaba`, `guacamayo`, `naguas`,
`Anacaona`, `Xaragua`, `Boriquén`.

## Sesión 6 — campaña del taíno 2, 2026-09-22 (parcela T7)

**Qué se preguntó.** Ya no por el léxico sino por la **noticia**: ¿qué decían
los isleños de lo que había al sur? ¿De dónde decían que venía el guanín? ¿Se
entendían con alguien? Datos y citas en
`6-fusion/taino2_etnohistoria_contacto.yaml`; lo mide
`6-fusion/scripts/medir_taino2_etnohistoria.py`.

⚠️ **Las citas van ancladas por capítulo**, no por número de página: el PDF es
el ebook de Gutenberg y su pie es un contador propio (lo midió T2). La página
impresa que se da es interpolación declarada dentro del capítulo.

### ⭐ Lo mejor que dio: los lucayos nombraron una tierra no rodeada de agua

**Cap. LIII** (pdf 417, impresa ~369), 12 de diciembre de 1492:

> «**Parece que los indios dichos daban á entender que el Babeque era tierra
> firme, porque decian que no estaba cercada de agua, y que estaba detras desta
> isla Española, la cual llamaban Caritaba ó Caribana, que era como cosa
> infinita**; y á mi parecer, que, cierto lo decian por tierra firme, y que
> **debian tener noticia de la tierra firme**… le parece que tienen razon en
> nombrar tanto á Babeque, y por otro nombre á Caribana, porque **debian de ser
> trabajados de la gente della**»

Es noticia indígena de diciembre de 1492 — anterior, por fuerza, a cualquier
intermediación europea. ⚠️ Lo que **no** sostiene: no identifica el lugar
(`Caribana` es la punta oriental de Urabá en la cartografía posterior, y usar
eso aquí sería proyectar un nombre colonial hacia atrás); describe razzias
recibidas, no comercio; y el propio Las Casas escribe «cuanto el Almirante
creia que entendia».

### Y el control que lo descuenta, en el mismo tomo

**Cap. XLVII** (pdf 391, impresa ~346):

> «**De donde parece, que ninguna ó cuasi ninguna cosa les entendian**, porque,
> en esta isla, ni nunca hobo gente de un ojo, ni caníbales que comiesen los
> hombres»

Es el aviso que el propio transmisor pone sobre toda la serie, y lo pone con un
caso falsable que resultó falso.

### El guanín

- **Cap. LX** (pdf 456, impresa ~402) — la definición por el criterio de ellos:
  «llamábanle **turey**, como á cosa del cielo… y así hacian á **una especie de
  oro bajo que tenia la color que tiraba á color algo morada, y que ellos
  llamaban guanin**, por el olor cognoscian ser fino y de mayor estima».
- **Cap. LXVII** (pdf 493, impresa ~435) — el guanín venía de otro sitio, y Las
  Casas corrige el otro sitio: «lo que aquí dice que entendia **haber isla que
  llamaba Guanin**, donde habia mucho oro, y **no era sino que habia en alguna
  parte guanin mucho**».
- **Cap. LXVII** (pdf 496, impresa ~437) — el rey de Samaná «afirmando que allí
  habia mucho [oro], y **en otras islas, como Carib y Matinino**».

### La ruta, descrita como cadena

**Cap. LXVIII** (pdf 498, impresa ~439):

> «van **renclera de islas**, desde la de Sant Juan… **hasta la de la Trinidad,
> que se apega con la tierra firme de Paria**, bien, camino de 300 leguas, y
> que **cada noche, yendo en un barco, pueden dormir en una dellas**»

y, unas líneas antes, la única dirección que los indios señalaron con el dedo:
«**señaláronle los indios** que la isla, ó de Sant Juan, ó de Matinino, ó de
Carib… **quedaba á la parte del Sueste**».

⚠️ La «renclera» es observación de **Las Casas**, sobre un barco español y con
lo que él sabe del siglo XVI. Que la ruta exista no dice que se recorriera.

### Qué NO dio (medido)

`curiana` **0** · `coquibacoa` **0** · `margarita` **0** · `cumaná` **0**.
Control en el mismo texto: `isla` 930, `oro` 482, `tierra firme` 98. El tomo I
acaba con el regreso del primer viaje: **quien busque la Kaketiana aquí no la
va a encontrar, y eso no es un hallazgo sobre la Kaketiana.**

## Qué falta

- 🔴 **Media docena de citas del repo dicen «Las Casas» sin decir a qué
  volumen**, y el que tenemos acaba en 1493. Conviene que digan tomo.
- **Los tomos II-V y la *Apologética* no están en el repositorio.** Ahí está el
  grueso: [[brinton-1871]] cita de ellos los caps. 2, 46, 61, 120, 197, 198,
  199, 204 y 241 de la *Apologética* (los numerales, los tres rangos sociales,
  `batey`, `guayzas`, `bixa`) y el lib. III cap. 21 de la *General*.
  Conseguirlos elevaría de golpe la cita primaria del taíno. **No se descargó
  nada**: lo decide Miguel.
- Regla que deja: *no toda fuente del corpus rinde para todo tema*. Mismo
  precedente que [[perea-alonso-1942]]. **Y su reverso, aprendido aquí: un
  rendimiento nulo es nulo PARA LA PREGUNTA QUE SE HIZO.** Antes de archivar
  una fuente, mirar qué se le preguntó.

---

## Bitácora: los tabacos (2026-09-23, cc.7)

Historia t. I, lib. I, **cap. XLVI** (capa de texto; el PDF es el ebook de
Gutenberg y se cita por capítulo): «Estos mosquetes, ó como los llamaremos,
llaman ellos *tabacos*». Es el pasaje que cita Zayas, y coincide con la
Apologética p. 181. Detalle: `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml` §zayas.cohiba_tabako.

## 2026-09-24 — campaña cosmovisión marina (comparanda)

**Se halló:** Matininó en boca de los informantes de Colón (enero de 1493), «una
isla … habitada de solas mujeres», que Las Casas cree «fábulas» (lib. I, cap.
LXVII; la paginación de esta copia es interpolada). **No se halló:** reverso ni
guaicán (el vol. 1 no llega a la Cuba de 1494).

COMPARANDA, no dato caquetío. Detalle en `6-fusion/cosmovision_marina_2026-09-24.yaml` §comparanda.
