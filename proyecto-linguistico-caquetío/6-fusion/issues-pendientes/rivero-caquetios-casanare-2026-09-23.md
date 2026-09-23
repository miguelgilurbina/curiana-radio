# Los caquetíos del Casanare en Rivero: no hay polity nueva, y `tamude` no dice «primos»

Encargo: `6-fusion/issues-pendientes/encargo-mineria-rivero.md` (minería 3).
Datos, citas y páginas: `6-fusion/rivero_1883_2026-09-23.yaml`. Las citas
de aquí están vistas en imagen salvo donde se dice lo contrario. Esto es
una propuesta (regla 5): no se tocó `curiana_polities.py`, ni el corpus, ni
el lexicón.

---

## 0. Lo que del encargo resultó FALSO al medirlo

1. **«El OCR confunde `Caquetío` con `Caquetá`».** No en el pasaje que
   importa. En la p. 151 (pdf 172) la IMPRESIÓN de 1883 dice «la lengua
   *Caquetá* de su pueblo de Pauto», en cursiva. El OCR leyó bien. Las otras
   seis `Caquetíos` las lee bien también.
2. **El recuento de menciones.** Un grep de `caquet` da 6 y deja fuera las
   dos que dicen qué gente vivía en Pauto: Rivero escribe **`Cacatíos`**
   («los que se hallaron en Pauto, Cacatíos de nación», p. 54). Con la raíz
   medida hay 12 aciertos en 9 páginas; de ellos, 10 son caquetíos.
3. **«Tercera polity caquetía».** `curiana_polities.py` ya tiene cuatro
   atestiguadas más la occidental. Y la `llanos` ya pone su territorio «hasta
   Casanare, y algunos grupos hacia el Orinoco en el estrecho de Barraguán»,
   citando a Jahn 1927, que lo saca de Rivero. Lo que Rivero aporta es
   **material de primera mano** para ese extremo, y un aviso de que no se
   parece a lo que la polity describe.

## 1. Qué dice Rivero de los caquetíos de los Llanos

Son dos grupos, y Rivero no los relaciona entre sí:

- **Pauto y Tame, en el piedemonte del Casanare.** Se redujeron antes de
  1629. «Cacatíos de nación» (p. 54), con un pueblo misional llamado
  «*Caquetíos de Pauto*» en 1666 (p. 201) y otros en la órbita de Tame en
  1663 (p. 144).
- **Barragua, Airico y Guaviare, al sur del Meta.** Eran gentiles, y los
  achaguas los llamaban «*Tamudes*» (p. 29, antes de 1657). Había caquetíos
  en el Guaviare en 1723 (p. 392).

**Sobre su lengua da una sola línea**, hacia 1667: el P. Meland estaba
«lidiando con la lengua *Caquetá* de su pueblo de Pauto» (p. 151). Rivero
no dice nada de su parecido con el achagua. Tampoco da nombre de intérprete,
catecismo con nombre ni una sola voz. Lo que rodea esa línea:

- La doctrina de Pauto tenía cinco o seis pueblecitos, «y en cada pueblo se
  hablaba distinta lengua» (p. 57).
- Hacia 1625 los jesuitas tradujeron catecismos «cada cual en el lenguaje de
  su partido» (pp. 59-60). Puede haber existido un catecismo en alguna lengua
  de Pauto, pero Rivero no dice cuál, ni qué se hizo de él.
- Cuando volvieron los jesuitas, tras la exploración de 1659, el
  doctrinero seguía sin saber la lengua (p. 100).

**Cruces.**

- **Pérez de Tolosa 1546** («algo difieren en la habla á los de Coro»). Rivero
  coincide en que había un habla caquetía en los Llanos, pero no la compara
  con la de Coro.
- **Federmann.** Rivero no nombra intérpretes para los caquetíos. Es un
  negativo.
- **Arcaya n. 31 (Manare, en el corregimiento de Chire).** Rivero pone Chire
  «como á medio día de distancia del río de Pauto» (p. 82), así que Manare
  cae en la comarca de los caquetíos de Pauto. Que allí se congregara a los
  restos lo dice **Gilij** a través de Jahn, no Rivero.

## 2. Decisión A: la polity de los caquetíos del Casanare

La polity `llanos` es la de Federmann: bajo Cojedes, s. XVI, jefes sin eje
chamánico y guerra de captura. Rivero describe otra cosa en el extremo
suroeste que esa misma polity reclama. Es el s. XVII-XVIII, en el
piedemonte andino, con gente reducida en misión junto a Tunebos y Támaras y
con una lengua que el misionero aprendía aparte de la achagua.

- **(a)** No tocar `curiana_polities.py`. Anotar en la ficha y en
  `3-mundo/polities-caquetias.md` que el «hasta Casanare… Barraguán» de la
  polity `llanos` descansa en Rivero, vía Jahn, y es un dato **colonial**.
- **(b)** Añadir a la polity `llanos` una nota con cita directa a
  `rivero-1883` (pp. 29, 54, 144, 151, 201, 392), con el aviso de que no hay
  prueba de continuidad política con los caquetíos del Cojedes.
- **(c)** Abrir una sexta polity `casanare`, como la occidental: futura y
  no simulada.

**Recomiendo (b).** Una línea de Rivero no basta para una polity nueva: no
dice nada de autoridad, economía ni guerra. Pero la cita de primera mano
debería estar donde hoy sólo está Jahn.

## 3. Decisión B: `parentesco-021` (`tamude` ← `mude` «primo»)

Hoy la entrada está en el canon como `atestiguado`. Su cadena es Rivero →
Jahn 1927 → Oliver 1989 → canon. Rivero atestigua **dos cosas separadas**:

- el etnónimo *Tamudes*, sin glosa (p. 29, pdf 50);
- *mude* 'primo' (pp. 419-420, pdf 438-439), que es el **saludo ceremonial
  al huésped** entre los achaguas del Airico: «saludasen á los *primos*, que
  así se llaman en tales casos **aunque nunca lo sean**».

Rivero no une las dos. Tres cosas son de Jahn: que *Tamudes* contenga
*mude*, que los achaguas trataran a los caquetíos «literalmente como
primos» y que eso pruebe origen común. Y el propio Rivero debilita la
lectura, porque *mude* es cortesía con cualquier huésped. En el repo hay
además dos datos que no casan:

- Neira y Ribero 1762 da «Primo = **N**ude» (pliego 85).
- `6-fusion/petroglifos_y_manaure.yaml` trae «tamudi» 'abuelos (en los
  Llanos)', vía Antolínez.

- **(a)** Partir la entrada. El etnónimo y la voz *mude* quedan
  `atestiguado`, citando `rivero-1883` pp. 29 y 420. La etimología y el
  «como primos» pasan a una entrada `hipotetico` que cita a Jahn.
- **(b)** Bajar la entrada entera a `hipotetico` (regla 2: en duda,
  degradar).
- **(c)** Dejarla como está.

**Recomiendo (a).** Lo atestiguado se queda, y la inferencia se ve como lo
que es.

## 4. Para el experimento (sin decisión: es referente)

Hay dos descripciones de época de un **achagua de segunda lengua**:

- p. 316: «sólo usaba de los infinitivos é impersonales». El intérprete
  nativo responde «con las mismas frases é impropiedades» para que lo
  entiendan.
- p. 401: «por infinitivos abstractos y otros modos irregulares […] de
  manera que se les entiende».

Además, la escala de la variación: dentro del achagua es la de «portugueses
y gallegos» (p. 21), y entre achagua y saliva, la de «vizcaínos y
castellanos» (p. 194). Todo esto va para `5-experimento/DISENO_KOINE.md`.

## 5. Lo que queda para otra campaña

- **Gilij 1780-1783, t. IV p. 487**, sobre los caquetíos del Orinoco y de
  Manare. Está en el repo y es la otra mitad de este issue.
- **La reedición de 1956** (archive.org `historiadelasmis00rive`), para ver
  si el manuscrito decía «Caquetá» o «Caquetía» en la p. 151. No se bajó
  por los posibles derechos del aparato de 1956.
- Las voces achaguas que sólo se leyeron en el OCR (8), que hay que ver en
  imagen antes de fusionarlas. El Libro I entero, para fauna.
