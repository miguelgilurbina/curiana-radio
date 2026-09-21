# El nominalizador que no está: se buscó así, en esto, y no hay

**Campaña C de d21.11.** Miguel, el 2026-09-21, al decidir el punto de la
nominalización: *«C y mientras no salga nada A»*. Esto es el informe de la C.

> **Veredicto en una frase:** no hay nominalizador que retroabstraer, y lo que
> el material atestiguado sí enseña es que **el nombre de acción es la raíz
> desnuda** — «Sembrar, siembra, sembradío» es **una sola forma** en el
> glosario. La opción A deja de ser provisional.

- Propuesta y evidencia: `6-fusion/propuesta_nominalizador_2026-09-21.yaml`
- Medición del lado atestiguado: `6-fusion/medicion_nominalizador_2026-09-21.yaml`
  (`6-fusion/scripts/medir_nominalizador.py`)
- Medición del lado emergente: `6-fusion/medicion_nominalizacion_emergente_2026-09-21.yaml`
  (`6-fusion/scripts/medir_nominalizacion_emergente.py`)
- Regla 5: esto **propone**. No se ha tocado `curiana_lexicon.py`, ni
  `2-lengua/`, ni el corpus.

---

## 1. Qué se preguntó

> ¿Hay en el material caquetío **atestiguado** algún nombre de acción, de
> agente, de instrumento o de resultado que comparta terminación con un verbo
> —o que se deje segmentar como raíz verbal + algo— de manera que se pueda
> retroabstraer un nominalizador, a la manera de `matakán`?

Explícitamente **no** se importó el nominalizador lokono `-hù`/`-hi` ni ningún
otro de la comparanda (opción B, que Miguel descartó). La comparanda sirvió
para reconocer un candidato caquetío si aparecía.

## 2. Cómo se buscó

Las 288 entradas del glosario de Zavala Reyes 2015 con su **glosa verbatim**
—leída del PDF por el parser del propio proyecto, no por la glosa curada del
lexicón—, clasificadas una a una con la clasificación declarada en el script y
una lista aparte de **trampas**: glosas castellanas que suenan a nombre de
acción y en la fuente son otra cosa. La más limpia: `Ucibo` #267 «**Cuenta** de
piedras», que es la chaquira, no el acto de contar.

Después: la prueba del sufijo (¿algún lema es otro lema + algo?), el control de
azar de cada terminación con p hipergeométrica exacta, y todo medido **dos
veces**, con y sin las entradas dudosas.

**Un añadido al método que el encargo no pedía y que resultó ser lo más útil:
un grupo de control.** Los nombres de «lugar definido por una **cosa**» (11),
que por hipótesis no deberían llevar nominalizador. Sirve para saber si el
método ve algo cuando hay algo.

## 3. Qué se halló

### El inventario

| | |
|---|---:|
| entradas del glosario | 288 |
| verbos de acción | 19 |
| verbos estativos | 11 |
| nombres de lugar-de-acción | 15 |
| nombres de acción | 13 |
| nombres de agente | 9 |
| nombres de resultado | 6 |
| nombres de instrumento | 5 |
| **subconjunto diana** | **46** (34 sin las dudosas) |
| grupo de control (lugar de cosa) | 11 |

Y la sonda sobre el canon, hoy, con las diecinueve reglas del corte aplicadas:
**cero** reglas que deriven un nombre de un verbo. No ha cambiado.

### El único candidato, y por qué muere

De 66 parejas «lema corto + resto = lema largo», **una sola** es verbo + resto
= nombre de la diana:

> `apo` #11 «**Grande**» + `-po` = `apopo` #12 «Nombre de jefe de parcialidad
> pequeña»

Es tentador: *«el grande»* → el que manda. Muere por tres razones, y la primera
basta:

1. **El presunto sufijo lo lleva también la base.** `apo` acaba en `-po`. Si
   `-po` nominalizara, el verbo no podría terminar igual.
2. La lectura barata es **reduplicación parcial** (`apo`→`apo-po`), y la
   reduplicación caquetía ya está medida con control (§9 de `morfologia.md`:
   9 % en la toponimia, 4,3 % en el léxico, contra 3,1 % wayuu y 0,7 % lokono).
   Un proceso que ya existe explica el caso sin morfema nuevo.
3. Control de azar: 2 casos de 34. Con n = 2 y la base llevando el final, eso
   no es un morfema.

### Las terminaciones compartidas: 23, y ninguna aguanta

Veintitrés finales de 2 y 3 letras aparecen a la vez en verbos y en nombres de
la diana. Al quitarlos, **sólo dos dejan una base atestiguada**:

- `-po` → `apo` (pero el verbo `apo` lleva el final: descalificado).
- `-re` → `dabuda` #99 «Barro loza» en `dabudare` #100 «Sitio de extracción de
  barro». La base es un **nombre**, no un verbo: eso no es un nominalizador,
  es `morfema-002`, el `-are` locativo «sitio de» que el canon ya tiene
  glosado — y que el censo de la terminación `-re` (2026-09-10) ya había
  medido como *«morfología toponímica, no derivación léxica general»*.

Los otros veintiuno dejan residuos que no son palabra.

### El control de azar, con y sin dudosas

Con las 46: `-ba` sale ×4,47 (p = 0,0014) y `-uba` ×4,70 (p = 0,0137). **Sin
las dudosas, los dos desaparecen**: sus casos eran `aruba` (una conjetura del
propio compilador: *«Puede ser Oirubae»*), `guamabatriba` y `siguruba`, los
tres marcados dudosos. Un resultado que cambia de signo según entren o no tres
entradas dudosas no es un resultado. Lo que queda es `-e`, que es «acabar en
vocal»: lo hacen 57 de las 288.

### Y la prueba de que el método no es ciego

En el **grupo de control**, `-ebo` sale con enriquecimiento **×13,09 y
p = 0,00079** — la señal más fuerte de toda la medición. Y es un morfema de
verdad, ya trabajado en la toponimia: `ebo` #117 «Camino, paso, senda».

El mismo procedimiento que no encuentra nada en los nombres de acción sí
encuentra el morfema que hay donde lo hay. **El cero de la diana es un cero
medido, no un cero del instrumento.**

## 4. Lo que el material SÍ enseña: la derivación cero

Donde el glosario da a la vez el verbo y su nombre, lo da **con la misma
forma**. Cinco entradas, las cinco de Angulo Molina:

| # | forma | glosa verbatim |
|---:|---|---|
| 39 | Beceremicore | «Dominar, triunfar, **victoria**» |
| 120 | Etamo | «Feroz, feo, **espanto**» |
| 170 | Jacuque | «Regar, **regadío**» |
| 180 | Jusual | «**Sembrar, siembra, sembradío**. Conuco» |
| 228 | Siguruba | «Salvar. **Caserío, sitio**» (dudosa) |

Y del lado del nombre, el mismo fenómeno sin infinitivo: `Quiricias` #217
«Sangre, **sangrado**».

`Jusual` es el caso mayor: **infinitivo, nombre de acción y nombre de lugar en
una sola forma**. Si el caquetío tuviera nominalizador, ahí se vería.

> ⚠️ **La reserva, que va con el hallazgo y no se separa de él.** Una glosa
> castellana que enumera «sembrar, siembra, sembradío» puede ser el compilador
> diciendo *de qué va* la palabra, no una afirmación sobre las clases de
> palabra del caquetío. Lo que se puede decir es: **el material atestiguado no
> registra ninguna marca de nominalización, y donde da las dos cosas las da con
> la misma forma.** Lo que no se puede decir es «el caquetío no marcaba la
> nominalización».

## 5. Qué NO se halló, y dónde se miró

| Fuente | Qué se preguntó | Resultado |
|---|---|---|
| **Oliver 1989, Tabla A-9** (pp. 593-594) | ¿verbos en el vocabulario caquetío del s. XVI? | **0 de 49**. El único que la criba marca es «ser viviente» (glosa de `Caquetio`): falso positivo. Las 49 son nombres |
| **Alvarado 1921** | ¿verbos caquetíos? | Sus entradas con glosa verbal son verbos **castellanos** derivados de nombres indígenas: `cachicamear`, `cebucanear`, `embijar`, `enguanepar`, `chigüirear`. Entre lenguas se prestan nombres |
| **Arcaya 1920** | ¿nombres de acción? | Él mismo lo cierra, p. 75: *«No se conserva de él, desgraciadamente, vocabulario alguno, ni mucho menos hay frases que permitan conocer su estructura gramatical»*. Lo único que da son siete voces de la Relación de Barquisimeto de 1579, **las siete nombres** |
| **Medina Colina** (dictado) | ¿verbos en las voces vivas? | **0 de 66**. Cero *del dictado*, que es parcial por diseño: queda comprobar el físico |
| **Comparanda lokono** (Perea pp. 609-612) | ¿un caquetío en `-hu`/`-hi`/`-ti`/`-tu`/`-na` tras raíz verbal? | cero. Y no se importa nada (opción B) |
| **Comparanda achagua** (Neira y Ribero) | ¿un caquetío en `-si`/`-ci` tras raíz verbal? | cero en la diana. Los tres caquetíos en `-si`/`-ci` son `barici`, `barisi` (misma raíz `bari-`, ya glosada) y `quiricias`, que es justo un caso de derivación cero |

### Y el límite que hay que decir en voz alta

**Los diecinueve verbos de acción del glosario vienen del mismo compilador:
Angulo Molina.** Los cinco restantes que no son suyos son estativos. Todo el
verbo caquetío que el proyecto tiene es **una sola lista**, y una corroboración
dentro de ella no es independiente (la trampa de `datihao` en Jahn). Si de esta
campaña hubiera salido un candidato, ése habría sido su techo de confianza.

**Angulo Molina no está en el repo.** Entra como deuda, y es de las gordas.

## 6. Lo emergente — y es OTRA sección

> **Esto no es evidencia de lo atestiguado.** Va aparte a propósito.

Medido sobre los 95.445 usos de `word_uses` de los runs anteriores al
2026-09-21 (corte declarado: se están escribiendo runs nuevos mientras se mide,
y las cifras tienen que ser reproducibles). Control de segmentación contra
`nucleo_de_token()`: **0 desvíos**.

**960 usos en 92 formas, sobre 45 raíces verbales, en boca de 112 hablantes
distintos.**

### Dos invenciones, no una

| | usos | formas | |
|---|---:|---:|---|
| posesivo `ta-`/`wa-` + raíz verbal | **470** | 48 | `ta-chaa` «mi hacer», `wa-jai` «nuestro oír». **Esto es nominalización** |
| atributivo/privativo `ma-`/`ka-` + raíz verbal | **490** | 44 | `ma-panaa` «sin saber», `ma-awa` «sin beber». **Esto no lo es** |

El titular de `morfologia.md` §11 —«La nominalización con el posesivo»— suma
los cuatro prefijos, y desde **d21.5** dos de ellos no son posesivos: `ma-` es
privativo y `ka-` atributivo. La mitad de esos usos no son nombres: son
predicación negativa sobre un verbo. Y **extender el privativo de nombres a
verbos es una segunda invención que nadie ha nombrado todavía** — arguablemente
la más interesante, porque `ma-` está declarado para nombres («sin X») y ellos
lo pusieron sobre «saber».

### Sobre qué raíces, y con qué sentido

Las quince formas más dichas, con la glosa de su raíz:

```
ma-kaa      133   «estar, existir, ser (cópula)»       48 hablantes
ta-maa      120   «decir, hablar, comunicar»           41
ma-panaa     85   «saber, conocer, entender»           37   → declarada «sin saber, ignorante»
ta-naba      71   «pensar, reflexionar, meditar»       32
ma-raka      68   «querer, desear, necesitar»          31
ta-panaa     55   «saber, conocer, entender»           30
ta-raka      46   «querer, desear, necesitar»          30
ta-rua       32   «cargar, transportar, llevar»        22
ta-wana      29   «ver, observar, mirar»               21
ma-rua       27   «cargar, transportar, llevar»        20
ma-naba      21   «pensar, reflexionar, meditar»       18
ma-wana      17   «ver, observar, mirar»               15
ma-waidima   15   «íntegro»                            15
ma-maa       14   «decir, hablar, comunicar»           10
ma-suna      14   «dormir, reposar, descansar»         11
```

**El campo es mental y de habla**, no material: saber, pensar, querer, decir,
ver, existir. Lo que la comunidad necesitó nombrar y no podía fue *el pensar*,
*el saber*, *el querer*. De las 45 raíces, **24 son caquetío-atestiguadas y 15
reconstruidas**.

### Por nodo, por casa, por gente

| | usos | hablantes posibles | tasa |
|---|---:|---:|---:|
| GUARANAO | 276 | 39 | **7,1** |
| AMUAY | 102 | 24 | **4,2** |
| (era 1, sin nodo) | 582 | — | — |

Por tier: **201 el tier 1, 161 el tier 2, 16 el tier 3**. Por casa, la del
Manaure va primera (143), y detrás los Tacuatos (75), los Cayudes (58), los
Guasicures (53) y los Corubos (49).

Y el dato que más dice: **el Manaure solo aporta 59 de los 378 usos de la era 2
— uno de 63 hablantes hace el 15,6 %.** Detrás, Sawaka el boratio (15) y
Patapati (14). No se reparte por oficio: se reparte por **prestigio**. El
que más nominaliza es el que más autoridad tiene, y eso es exactamente lo que
un sociolingüista esperaría de una innovación que se propaga desde arriba.

> ⚠️ Es conteo **crudo**, no tasa por turno: quien más habló más dice, y el
> Manaure sale en todos los turnos en que está. La lectura de prestigio es una
> hipótesis que esta medición **sugiere** y no prueba; para probarla hace falta
> normalizar por intervenciones, que no se hizo.

### ¿Se fijó alguna?

**No.** De las 29 entradas fijadas en el diccionario de koiné de toda la base,
**cero** son nominalización emergente. Se usa muchísimo y no ha fijado nada:
es habla corriente, no una disputa de referente ganada.

### Y una cifra de `morfologia.md` §11 que hay que actualizar

§11 dice **1.107 + 25 = 1.132**. Hoy, sobre los mismos runs, salen **960**. La
diferencia, **172**, está medida y es exactamente la de las raíces que **#178**
dejó de considerar verbales el 2026-09-20: `ka-juri`, `ka-popoi`, `ka-kana`,
`ma-kapo`, `ma-hueke`, `ma-baharuko`, `ma-kibakibi`, `ma-kiricias`… 36 formas.
960 + 172 = 1.132, exacto.

Las dos cifras son correctas para su estado del lexicón; la de hoy es la del
canon en `main`. Y la corrección va donde d21.5 quería: **`ka-juri` sale del
recuento porque `juri` es un nombre**, y `ka-juri` «hay viento» es el
atributivo haciendo su trabajo.

## 7. Lo que salió de paso

1. **El prefijo `ja-`.** Siete de los trece lemas en J- del glosario son
   verbos: 53,8 % contra el 10,4 % del glosario entero, **p = 7,4e-05**.
   Zavala #173 da el mismo lema en dos formas —«Jadicuar. **Adicora**»— y el
   propio Zavala, en su §5 (p. 72), habla del «prefijo "A" en los topónimos
   costeros». Del lado lokono los infinitivos se citan con `a-`
   (`a-sucusu-n`), y el achagua con `nu-`: **prefijar el verbo es arahuaco**.
   No es un nominalizador; si acaso es lo contrario. Y los siete son del mismo
   compilador, y el glosario es alfabético: hay que descartar que el
   amontonamiento sea un artefacto de cómo Angulo Molina ordenó su lista.
   **Es la pista más limpia que ha dado esta medición y pide campaña propia.**

2. **`-ebo` tiene un quinto apoyo, y es el primero léxico.** `cazebo` #75 (GC)
   «Poniente» = `cazi` #76 (GC) «Sol» + `ebo` «camino» → *el camino del sol*.
   Las dos piezas atestiguadas, la traducción cierra sin residuo, y es de otro
   compilador que los cuatro topónimos ya trabajados. Es el método de D9 para
   `-bana`. La entrada `kasebo` del lexicón no lleva la segmentación.

3. **Los nombres de agente atestiguados son reduplicados, no sufijados.** Tres
   de los nueve: `quibaquibi` ← `quiba`, `humohumo`, `apopo` ← `apo`. §9 ya
   lista los dos primeros bajo otros valores; lo que esta campaña añade es que
   en el subconjunto de agentes **la reduplicación es el único proceso que deja
   base atestiguada**. (Con un aviso: `baquiano` es palabra castellana; antes
   de leer `quibaquibi` como agentivo hay que descartar que la glosa sea la
   etimología del compilador.)

4. **`mene`/`cumaragua`: la ⚠️ D de la ficha de Zavala se cierra.**
   `4-fuentes/zavala-reyes-2015.md` marcaba la cita de su p. 62 —«"mene" y
   "cumaragua" nombre de la **ciruela**»— porque «la sintaxis de Arcaya es
   ambigua». Fui al Arcaya original: p. 75 dice «mene y cumaragua (nombres de
   la **viruela**)», y la Tabla A-9 de Oliver, independiente, trae «viruela».
   No era ambigüedad de sintaxis: **Zavala leyó *ciruela* donde Arcaya puso
   *viruela***, y eso explica también la glosa de `Cumaragua` #93.

## 8. Las opciones, y qué recomiendo

### Sobre la pregunta de la campaña

- **A — cerrar la pregunta con el negativo y convertir la A de d21.11 en
  definitiva.** Se escribe en `morfologia.md` §10 (fila «Nominalización») y
  §11 que el material atestiguado no registra marca de nominalización, con las
  citas y con la reserva del §4 de arriba. El hueco queda **declarado**, que es
  lo que la regla 8 pide. *(recomendada)*
- **B — además de A, declarar la derivación cero como rasgo del atestiguado.**
  Es decir: escribir que en las fuentes el nombre de acción aparece con la
  forma del verbo (`jusual`, `jacuque`, `beceremikore`, `quiricias`), capa
  `caquetío-atestiguado`, con su cita. Es una afirmación sobre lo que las
  fuentes registran, no sobre la lengua. *(recomendada junto con A)*
- **C — dejar la pregunta abierta hasta minar el arte de Neira y Ribero y
  llegar a Angulo Molina.** Honesta, pero deja la A de d21.11 provisional otros
  meses y las dos fuentes son de mucho trabajo. *(no recomendada como estado,
  sí como deuda escrita)*
- **D — proponer igualmente un `-po` agentivo retroabstraído sobre `apo` →
  `apopo`.** *(no recomendada: el verbo lleva el mismo final, n = 2, y la
  reduplicación lo explica sin morfema nuevo — sería exactamente el error de
  `macana`/`-kana` de la semana pasada, compartir sílaba y no morfema)*

**Mi recomendación: A + B.** El negativo está bien medido, tiene control
positivo que lo valida, y B convierte un «no encontramos nada» en un dato con
cita.

### Sobre lo emergente

- **E — actualizar la cifra de §11 a 960/92 y decir con qué estado del lexicón
  se midió.** *(recomendada: es la regla 1)*
- **F — partir §11 en dos**: la nominalización posesiva (470 usos, 48 formas) y
  la predicación privativa sobre verbo (490 usos, 44 formas), que hoy van
  sumadas bajo un titular que dice «posesivo» y desde d21.5 ya no lo es.
  *(recomendada)*
- **G — dejarlo como está y sólo corregir la cifra.** *(no recomendada: el
  titular afirma algo que la propia tanda del 21 desmintió)*

### Sobre lo que salió de paso

- **H — abrir campaña del prefijo `ja-`** (sub-01). *(recomendada: es barata y
  es la pista más fuerte)*
- **I — llevar `cazebo` = `cazi` + `ebo` a la mesa de `-ebo`** de la campaña de
  topónimos. *(recomendada: es una línea)*
- **J — curar `cumaragua`** con la lectura de Arcaya. *(para decidir: cambiar
  una glosa mueve canon)*
- **K — nada de esto ahora.** *(siempre disponible)*

**Miguel decide.**
