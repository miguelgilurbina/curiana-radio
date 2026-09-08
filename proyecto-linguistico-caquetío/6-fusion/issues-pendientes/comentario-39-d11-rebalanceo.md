## D11 decidida: se rebalancea hacia el eje lokono-taíno, con achagua más adelante

Miguel, 2026-09-08:

> «Yo creo que deberíamos rebalancear con el lokono y achagua más adelante.
> Ya que culturalmente son los más cercanos, al igual que el taíno que hemos
> visto como se comparten ciertas palabras.»

Es la opción **rebalancear** de las tres que el cómputo del 2026-08-31 dejó
planteadas, y se ejecuta por fases. Registro completo en
`6-fusion/decisiones_tanda_2026-09-08.yaml`.

### Qué significa, operativamente

El wayuunaiki **deja de ser la hermana por defecto de la que se reconstruye**
y pasa a ser una comparanda más. No se retira nada: las 781 entradas wayuu no
se borran, se re-encuadran, y el wayuu sigue siendo la comparanda etnográfica
central y bien fundada. Lo que se mueve es de quién se reconstruye la lengua.

### Las fases

1. **Lokono, ahora**, desde lo que el repo ya tiene. La pata que no depende de
   ninguna compra es **Perea Alonso 1942** (*Filología Comparada Arawak*, tomo
   I): 926 páginas con capa de texto, en el repo, **sin minar**. Además quedan
   las tablas A-1 y A-3 a A-7 de Oliver sin transcribir, y Brinton 1871.
2. **Achagua, más adelante**, y con una razón medida para el «más adelante»:
   el repo **no tiene ninguna fuente achagua propia**. Solo tres formas como
   comparanda en `cognados.yaml` vía Oliver cap. 2, más etnografía en Gumilla
   y Rivero. Hay que adquirir: el artículo de Meléndez Lozano sobre el *Arte y
   Vocabulario* de 1762 es PDF libre en el IAI de Berlín, y el manuscrito de
   Neira y Rivero está digitalizado en la Library of Congress.
3. **La etiqueta del núcleo reconstruido**, que esto no cierra. Rebalancear la
   comparanda no re-deriva sola la Capa 2: `taya`, `pia`, `kai`, `kashi`,
   `wuin`, `eka` y `piama` salen de la columna guajira. O se re-deriva, o se
   declara la base guajira como decisión de modelado declarada. Sigue abierto.

### La convergencia que vale la pena anotar

La intuición cultural de Miguel coincide con **Antolínez 1944**, que el
proyecto ya citaba sin conectarlo a este issue: *«los kaketíos son los más
conspicuos representantes de los Arawak de la costa de Guayana, o Lokono…
muy afín de la taína»*. Era opinión de autor; ahora tiene tres cómputos
independientes al lado y un cuarto apoyo que es regla y no parecido: la
correspondencia CQ *barisi* : LK *bálisi* : WY *palíi* (cognado-001), donde el
caquetío conserva la /b-/ como el lokono frente a la /p-/ guajira.

### 🔴 La cautela sobre el taíno, que decide qué cuenta

Las 53 entradas taínas del lexicón **no son una sola cosa**. Medido el
2026-09-08, se parten en tres, y solo una sirve como evidencia de parentesco:

| Clase | n | Qué son | Valen para D11 |
|---|---|---|---|
| Reconstruidas **desde el lokono** | 9 | abba, acoa, aduri, agari, akcicyaa, daca, thigisi, wacusi, wagulo — la nota lo dice: «Reconstrucción hipotética Taíno desde Lok.» | **NO**: son lokono con otra etiqueta |
| Antillanismos culturales | 35 | cacique, maíz, yuca, batata, bohío, ají, tabaco, casabe, caney, nagua, piragua, iguana, manatí, cemí, areíto, macana… | **NO**: prueban contacto y repertorio (#119), no parentesco |
| Atestiguadas con cognado lokono (Brinton 1871) | 9 | cai 'isla' ~ Lok. kairi · mayani 'no' ~ Lok. ma · taita 'padre' ~ Lok. itti · caimán · casabe · cohiba · higuana · tuna · yamosa 'dos' | **SÍ**, y son las únicas |

🔴 **La trampa**: si el rebalanceo cuenta «lokono + taíno» sin separar estas
clases, las nueve reconstruidas desde el lokono se cuentan **dos veces** y el
resultado sale inflado a favor del eje que queremos probar. Es exactamente el
error que produjo el 80% de fallo de las 441 hipotéticas: transducir y luego
contar la transducción como evidencia.

Y una corrección al pasar: `daca` en el lexicón es **'mano'** (reconstruida
desde el lokono *daka*), no la primera persona. El argumento del prefijo /dA-/
es de Oliver sobre la lengua, y **el lexicón no lo tiene atestiguado**: la
primera persona del canon es `taya`, que sale de la columna guajira. Eso no
resta a la decisión, pero conviene no citar como apoyo algo que el dato no
sostiene.

### Y lo que ningún eje explica

Once de los veinticuatro conceptos atestiguados no se parecen a **ninguna** de
las cinco columnas: arena, camino, cerro, mar, grande, oír, raíz, sangre, dos,
usted, una-luna. El caquetío tiene fondo propio en el vocabulario básico. El
rebalanceo no debe taparlo: la pregunta nunca fue de quién es dialecto, sino
con qué mezcla y cuánto fondo propio se reconstruye.

### Estado del gate

La condición 8 se levanta **cuando la fase 1 esté aplicada**, no al tomar la
decisión: el gate mide dato, no intención.
