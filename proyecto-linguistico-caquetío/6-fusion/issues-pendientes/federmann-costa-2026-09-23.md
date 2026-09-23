# Federmann en la costa (1530-1531): seis cosas que decide Miguel

**Minería 3, parcela Federmann, 2026-09-22/23.** Encargo:
`6-fusion/issues-pendientes/encargo-mineria-federmann.md`. Datos, citas
verbatim, página impresa y eslabón de cada dato en
`6-fusion/federmann_1530_costa_2026-09-22.yaml`; bitácora en
`4-fuentes/federmann-1916.md`.

Todo es `contacto-temprano` (1530-1531): nada se proyecta al s. XIV-XV sin
decidirlo (regla 3).

---

## 0. Lo que resultó falso al medirlo

1. **Las páginas de las citas del interior estaban cambiadas** en la ficha y en
   `6-fusion/polities_no_costeras_federmann.yaml` (prop-polity-001 a 005, que
   vinieron de Brito Figueroa): Barquisimeto (23 aldeas, 30.000 hombres,
   fortificadas) es **pp. 62-63**; el valle del Yaracuy/Vararida (20.000
   guerreros, «misma nación», confederaciones, cinco a ocho familias) es
   **pp. 109-110**. El texto coincide.
2. La cita estructural «misma nación, no un solo señor […] confederaciones»
   **funde dos grupos** con el «[…]». Y hay una frase mejor, sin elisión: los
   caquetíos del valle, «aunque de una nación» con los de Barquisimeto, «no son
   amigos» (alemán, Klüpfel p. 70; 1916 p. 108).
3. «Federmann escribe caquetíos» (Arcaya): la primera mención del original es
   **`Caquecios`** (1557 [19], verificado en imagen).
4. La 1916 dice «excepto los que viven cerca de Coro» y el alemán dice **lo
   contrario**: «tanto en torno a Coro como aquí» (1557 [48], verificado).
5. Que la india rescatada por Ampíes fuera hija de Manaure **no lo dice
   Federmann**: es una cadena de inferencias de Arcaya.
6. La cadena no es alemán → francés → castellano: **son cuatro eslabones**. El
   alemán ya traduce un diario notarial castellano, y el francés normalizó los
   nombres propios.

---

## 1. Corregir las páginas de prop-polity-001 a 005

Es un arreglo de datos, no de canon, pero toca una propuesta que no es de esta
parcela.

- **(A)** Corregirlas en `polities_no_costeras_federmann.yaml` y cambiar su
  `via: brito-figueroa-poblacion-economia` por la lectura directa
  (federmann-1916, pp. 62-63 y 109-110). *Recomendada.*
- **(B)** Dejar ese archivo como está y que valga `federmann_1530_costa`
  (fed-int-001 a 006) como la versión cotejada.

## 2. Miraca en 1530 (nodo-031)

Federmann llega a «einen Puebles Miraca» en enero de 1530 y allí encuentra
comida para más de cien hombres (1557 [13], verificado en imagen). La cadena de
nodo-031 empieza hoy en Bastidas 1538.

- **(A)** Sumar federmann-1916 p. 20 a `procedencia` y 1530 al principio de la
  cadena; `precontacto` sigue `desconocido`. *Recomendada.*
- **(B)** Dejarlo en la propuesta hasta que se revise nodo-031 entero.

## 3. La costa y el interior hablaban la misma lengua, con variación

Federmann (1530): un caquetío de Coro sirve de intérprete en Barquisimeto, y los
mismos intérpretes sirven en el valle del Yaracuy; no creía que a 73 Meilen
hablaran como en Coro, y la buena noticia le pareció increíble. Pérez de Tolosa
(1546): los caquetíos de los llanos «algo difieren en la habla á los de Coro».
Dos testigos independientes.

- **(A)** Llevarlo al corpus (geografía política y lengua) como hecho
  `atestiguado`, `contacto-temprano`, con las dos citas, sin decir nada de
  cómo era esa lengua. *Recomendada.*
- **(B)** Dejarlo como nota en `3-mundo/polities-caquetias.md`.
- **(C)** Esperar a Gumilla y a Rivero (la otra minería de esta campaña), que
  hablan de los caquetíos de los llanos.

## 4. El seretón

Cero de la palabra y cero del hombre que se transforma, en castellano y en
alemán. Lo que hay es la **nación ayamán de enanos** de la sierra y **una enana
que Federmann dejó en Coro** (1557 [35], verificado): muy probablemente, la raíz
del «enano de los Welser» que el barrido web atribuía al ceretón.

- **(A)** Registrar en `ceret_on_hipotesis_miguel.yaml` que Federmann aporta el
  enano, no el nombre ni la transformación, y que la frase «el ceretón está en
  Federmann» no se sostiene tal cual. El seretón de Medina sigue en el corpus
  por su propio mérito, como ya falló Miguel. *Recomendada.*
- **(B)** Seguir buscando el ceretón en Castellanos y en Oviedo y Baños antes
  de escribir nada.

## 5. ¿La costa oriental (Xaragua, Martinico, Atycares) es la Kaketiana?

A la vuelta, Federmann recorre 65-80 Meilen de costa caquetía «aliada» desde la
boca del Yaracuy hasta Coro, con canoas y una alianza «confederada» entre una
nación de la sierra (Atycares) y dos aldeas caquetías. Ninguno de esos lugares
es nodo.

- **(A)** Es de la esfera: abrir candidatos a nodo con `atestacion: colonial` y
  región nueva `falcon-oriental`.
- **(B)** Es otra polity costera (regla 4): se marca `polity: costa-oriental` y
  se queda fuera del mapa de la era 2. *Recomendada por ahora*: nada de lo que
  dice Federmann la une al Golfete más que el nombre de la nación.

## 6. `Oyama`: ¿ñame o auyama?

En una aldea ayamán el original enumera «Mahis / Juca / Batata / Oyama» (1557
[24], verificado). La 1916 traduce «ñames». `Oyama` se parece más a
*auyama/ahuyama* (calabaza). Es de la sierra (no caquetía), pero es una
atestación fechada de un producto de la esfera.

- **(A)** Anotarla como candidata para quien cure las voces de la esfera, con
  las dos lecturas y sin decidir. *Recomendada.*
- **(B)** Descartarla: la equivalencia no se puede probar desde Federmann.

---

**Lo que esta parcela no hizo**: leer de corrido los caps. VI-VII y IX-XI (sólo
sondas), ni cotejar en 1557 los nombres del interior. Si algún día se modela una
segunda polity (#83, D14), eso es lo que falta.
