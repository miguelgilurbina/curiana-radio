---
tipo: fuente
obra: "Colección de los viajes y descubrimientos que hicieron por mar los españoles desde fines del siglo XV, tomo I (2.ª ed.): Viajes de Colón; Almirantazgo de Castilla"
autor: "Fernández de Navarrete, Martín"
anio: "1858 [documentos de 1492-1504]"
genero: cronica
publicacion: "Madrid, Imprenta Nacional, 1858 (segunda edición). Edición documental: contiene el Diario del primer viaje en la transcripción de Las Casas, la carta del doctor Chanca, la **Relación del tercer viaje** de Colón a los Reyes y la relación del cuarto"
edicion_del_ejemplar: "ejemplar digitalizado por Google; archive.org data la publicación en 1859, la portada dice 1858"
local: "fuentes_caquetios/Navarrete_1859_Coleccion_Viages_t1_Viages_de_Colon.txt"
paginas: "~550"
capa_texto: si
estado_minado: parcial
cobertura: "la Relación del tercer viaje (pp. ~390-420), preguntada por el guanín y por la lengua en Paria — 2026-09-22, campaña del taíno 2, T7"
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
minado: 2026-09-22
descargado: 2026-09-22
origen_digital: "archive.org/details/coleccion-de-los-viajes-y-descubrimiento-i — texto OCR ('Coleccion_de_los_viajes_y_descubrimiento I_djvu.txt'), 1.597.527 bytes, sha256 c84739d9cdef9001a7498b557ef64275fb0e9c15440c93bac6986b6c1ac130a3. Dominio público (Public Domain Mark 1.0 declarado por archive.org). Descargado el 2026-09-22 con la autorización de Miguel de esta campaña"
aliases: ["Navarrete 1858", "Navarrete t. I", "Viajes de Colón", "Relación del tercer viaje", "Diario del primer viaje"]
---

# Navarrete 1858 — *Colección de los viajes y descubrimientos*, tomo I

## Por qué está aquí

Porque trae **la Relación del tercer viaje en la letra de Colón**, y ésa es la
página donde se decide la pregunta de esta campaña. Hasta hoy el repo sólo
tenía el tercer viaje por dos paráfrasis —Anglería y Hernando Colón—, y las dos
difieren entre sí justo en la frase que importa.

También trae el **Diario del primer viaje**, que es el original que
[[las-casas-1875]] parafrasea capítulo a capítulo. ⚠️ Por eso **no es una
segunda atestación de nada de lo que dice Las Casas** (skill `minar-fuente`
§8): es el mismo testigo por la misma mano. Sirve para leer la letra, no para
duplicar el apoyo.

## Estado técnico (verificado 2026-09-22)

Texto OCR, 1.559.770 caracteres. Mismo escaneo de Google, mismas erratas, mismo
folio impreso dentro del flujo (`DE COLON. 401` / `402 TERCER VIAGE`). PDF de
30,2 MB **no** descargado.

🔴 **Doble espacio en el OCR**: las consultas de más de una palabra tienen que
ir con `\s+`. `no se entendian` devolvía 0 **en la página donde la frase está
entera**; `tercer viage` devolvía 0 con la obra dentro. Ver
`6-fusion/scripts/medir_taino2_etnohistoria.py`.

## Qué ha dado (2026-09-22, campaña del taíno 2, parcela T7)

### 🔴🔴 p. 400 — «no se entendían», en la letra de Colón

> «los llevaron á una casa muy grande hecha á dos aguas, y no redonda, como
> tienda de campo… y hicieron traer pan, y de muchas maneras frutas é vino de
> muchas maneras blanco é tinto, mas no de uvas… los hombres todos estaban
> juntos á un cabo de la casa, y las mugeres en otro. **Recibieron ambas las
> partes gran pena porque no se entendían, ellos para preguntar á los otros de
> nuestra patria, y los nuestros por saber de la suya.**»

Agosto de 1498, costa sur de Paria. Es el único punto de Tierra Firme donde la
inteligibilidad se pone a prueba y se anota el resultado. Anglería lo
parafrasea —«Les molestaba mucho el no poder entender á los nuestros ni ser
ellos entendidos», vol. 1 p. 273— y es el mismo testigo.

⚠️ **Lo que el texto no dice**: no dice que hubiera intérpretes taínos en las
barcas y que fracasaran. Dice que «los nuestros» y «ellos» no se entendieron.
Fuerte por contexto, no por letra.

### 🔴 p. 401 — el oro bajo de Paria venía de una TIERRA ALTA al poniente

> «muchos traían **piezas de oro bajo** colgado al pescuezo. **Las canoas de
> ellos son muy grandes** y de mejor hechura que no son estas otras, y mas
> livianas, y en el medio de cada una tienen **un apartamiento como cámara** en
> que vi que andaban los principales con sus mugeres. Llamé allí á este lugar
> Jardines… Procuré mucho de saber donde cogían aquel oro, y **todos me
> aseñalaban una tierra frontera dellos al Poniente, que era muy alta, mas no
> lejos**; mas todos me decian que no fuese allá porque allí comían los
> hombres, **y entendí entonces que decian** que eran hombres caríbales, é que
> serian como los otros, **y después he pensado que podría ser que lo decian
> porque allí habría animalias**.»

Tres cosas en un párrafo: (a) el guanín («oro bajo») de Paria venía, según
ellos, de **tierra** y del **oeste**, no de ninguna isla — lo que corrige la
paráfrasis de [[colon-hernando-1892]] p. 57, que escribe «otras islas
occidentales»; (b) **las canoas de Paria son mejores y mayores que las
antillanas**, dicho por quien llevaba seis años mirando canoas caribeñas; (c)
Colón pone su propia reserva epistémica dos veces, y es lo que hace citable
todo lo demás.

Y unas líneas antes (p. ~399): «procuré mucho de saber donde las hallaban [las
perlas], y me dijeron que **allí, y de la parte del Norte de aquella tierra**».

### p. ~369 — Chanca, segundo viaje: «si lengua toviésemos»

> «Lo que parece desta gente es que **si lengua toviesemos** que todos se
> convertirían… yo les he preguntado qué es aquello, dicenme que es cosa de
> **Turey, que quiere decir del cielo**… ansi piensan que cuanto nosotros
> traemos que es cosa del cielo, que á todo llaman Turey»

El segundo viaje entero, con diecisiete naves, sin intérprete útil. Y la glosa
de `turey`, que es la que explica el pasaje del guanín en [[las-casas-1875]]
p. 456.

## Medido

`carib` 60 · `canoa` 104 · `lengua` 77 · `paria` 14 · `matinino` 7 ·
`babeque` 16 · `almadía` 26 · `intérprete` 5 — y **`curiana` 0 ·
`coquibacoa` 0 · `gigante` 0 · `caribana` 0** (`caritaba` 1). Control:
`isla` 789, `oro` 517.

El cero de `curiana` y `coquibacoa` es real y esperable: este tomo es de los
viajes **de Colón**, y Colón no pasó por la Kaketiana. Eso está en
[[navarrete-1829-viages-menores]].

## Qué NO da

- Nada de la Kaketiana, por lo dicho.
- Ninguna lista de palabras de Paria: Colón apunta el nombre de la tierra y
  poco más.
- La *Relación del tercer viaje* **no usa la palabra `guanín`**: dice «oro
  bajo». La palabra entra al castellano por el Diario y por Las Casas.

## Qué falta

- Leer el **Diario del primer viaje** entero con las preguntas de lengua
  delante. T7 lo tocó sólo donde Las Casas ya había llevado.
- El **cuarto viaje** (está en este tomo): Cariai y Veragua, que es donde el
  guanín aparece en su región de origen. Leído sólo por
  [[colon-hernando-1892]].

## Enlaces

[[las-casas-1875]] · [[colon-hernando-1892]] · [[angleria-1892]] ·
[[navarrete-1829-viages-menores]]
