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
cobertura: "caps. XL-LXVII pasaje a pasaje (primer viaje y La Española); el tomo entero por patrón"
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-21
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

## Qué falta

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

