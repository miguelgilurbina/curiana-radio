# 2ª campaña del taíno — T6: Oviedo y Valdés, tomos II, III y IV

**Fecha**: 2026-09-22 · **Rama**: `campana/taino2-oviedo-ii-iv`
**Datos**: [`6-fusion/taino2_oviedo_venezuela.yaml`](../taino2_oviedo_venezuela.yaml)
**Nota de fuente**: [`4-fuentes/oviedo-y-valdes-1852-1855.md`](../../4-fuentes/oviedo-y-valdes-1852-1855.md)

---

## 0. Lo que resultó falso al medirlo

Cuatro cosas, y las cuatro estaban escritas en el repo o en el encargo.

### a) «El apéndice de voces del editor no existe»

`4-fuentes/oviedo-y-valdes-1851.md` lo dijo ayer, apoyándose en «el rastreo del
2026-08-14 sobre el tomo IV».

**Existe.** «VOCES AMERICANAS EMPLEADAS POR OVIEDO», tomo IV, impresas
**593-607**, con una **BIBLIOGRAFIA** de sus 23 vocabularios en la 608. Doce
entradas marcadas «(Lengua de Venezuela)». Es exactamente lo que Jahn 1927 p.213
n.29 llama «el Apéndice al tomo IV».

La conclusión de ayer era correcta sobre **el tomo I** —lo que cierra ese volumen
es un índice de capítulos— y se extendió al IV sin tenerlo delante.

### b) «Oviedo no nombra a los caquetíos»

Medido ayer en el tomo I con `caquet` = 0 y `caiquet` = 0.

**Los nombra 12 veces en el tomo II**, y las sondas seguían dando cero porque
**la obra escribe `çaquitios`**. Verificado en imagen (t. II p.297, en cursiva).
El editor moderniza a `zaquitios` en el glosario.

Es `minar-fuente` §2 en su forma más cara: el cero no midió la fuente, midió
nuestra ortografía — y de ese cero se había sacado una afirmación sobre la
fuente. **A las sondas de esta obra: `çaquiti`, `zaquiti`, `saquiti`.**

### c) «`datihao` está atestiguada a las dos orillas por Oviedo»

Es el encargo de esta campaña, es `creencia-001` y es la ficha del lexicón.

`datihao`/`dalihao` aparece **una vez en los cuatro tomos**: t. I p.473, en boca
de Agüeybana, en San Juan. En el **cuerpo** de los tomos II, III y IV: **cero**,
con siete sondas y con el guion de fin de línea deshecho. La atestación
«venezolana» es **una entrada del glosario del editor** (t. IV p.598). Ver §2.

### d) «El desfase se calcula UNA vez por tomo»

Cierto en el t. II (13) y en el t. IV (15). **Falso en el t. III**: 13 hasta la
pdf ≈150 y 15 desde ahí. Y en el propio tomo I la impresa 473 cae en la pdf 590
—desfase **117**—, no 118 como dice su ficha; la cita de T1 es correcta, la
fórmula no lo es en ese tramo.

### e) Y una mía, de la primera pasada de esta misma minería

Di las islas ABC por ausentes con las sondas `curazao`, `aruba` y `bonaire`.
**Están** (§5): el OCR las da `Aniba` y `Boijnare`. Escribí el aviso de (b) en
este mismo archivo y acto seguido caí en él. Queda dicho.

---

## 1. La trampa nueva: el guion de fin de línea

La caja es de dos columnas estrechas y **parte las palabras**. La capa OCR
conserva el guion, así que un `grep` sobre el texto crudo no ve la mitad:

| Voz | crudo | con el guion deshecho |
|---|---|---|
| `çaquitio` | 9 | **12** |
| `boratio` | 16 | **18** |
| `Veneçuela` | 31 | **39** |
| `çemyruco` | **0** | **1** |

Y aun deshaciéndolo, `busera` y `datos` siguen en **0**, porque el OCR las
destroza (`Intsera`, `dalos`). Las dos se leyeron en imagen.

**Propuesta para CLAUDE.md** (fila nueva de «Trampas medidas», si Miguel quiere):
*en las ediciones a dos columnas el conteo es una cota inferior; deshacer el
guion antes de contar, y aun así verificar en imagen lo que se va a citar.*

---

## 2. 🔴 El caso `datihao` — la decisión que pide esta minería

### Lo medido

| | |
|---|---|
| en el **cuerpo** de los tomos II-IV | **0** |
| en el **tomo I** | **1**: impresa 473, libro XVI cap. V, boca de **Agüeybana**, **San Juan** |
| en el **glosario del editor**, t. IV p.598 | «**Datihao**: señor: el que presta su nombre al esclavo. **(Lengua de Venezuela.)**» — imagen |

### Por qué la etiqueta del editor no se sostiene

1. **La glosa es la paráfrasis del pasaje de San Juan.** Allí el hombre se ofrece
   como **naboría** (siervo) y Agüeybana le contesta «á mi *dalihao* (que quiere
   deçir mi señor, ó el que, como yo, se nombra)». Señor + esclavo + compartir el
   nombre: los tres elementos están ahí y en ningún otro sitio de la obra.
2. **El editor no tenía fuente venezolana.** Su propia bibliografía (t. IV p.608)
   lista 23 vocabularios: mexicano, siete de quechua y aimara, guaraní,
   cumanagoto, dos de Chile, moxo, tagalo, voces cubanas. **Ninguno de Venezuela
   ni de la costa caribe venezolana.**
3. **Tenía al lado la voz que sí lo es.** `Diao` va dos entradas más abajo, misma
   inicial, misma glosa 'señor', y **sí** es venezolana y **sí** está en el cuerpo
   del texto (t. II pp.299-300).

### La cadena, con su punto de fuga marcado

1. Oviedo t. I p.473 — `dalihao`, San Juan. **ATESTIGUADO.**
2. Amador de los Ríos t. IV p.598 (1855) — «(Lengua de Venezuela)». **ETIQUETA DEL EDITOR.**
3. Jahn 1927 p.213 n.29 — voz caquetía del apéndice. **SEGUNDA MANO DE LA ETIQUETA.**
4. Oliver 1989 cap. 2 n.42 — duda, concluye «equally shared». **LECTURA.**
5. `creencia-001` + ficha del lexicón — `caquetío-atestiguado` **sin reserva**. ← aquí se perdió la duda.

Oliver dudaba porque «Oviedo hablaba de los indios de la Provincia de Venezuela
en general y su larga residencia en La Española pudo hacerle usar taíno». **La
duda era buena y el motivo era otro**: Oviedo no habló de los indios de Venezuela
— habló de San Juan. El «en general» es del editor de 1855.

### Opciones para Miguel

- **(a)** `datihao` pasa a **`taíno-atestiguado`**, con nota de que el editor de
  1855 la dio por venezolana y de que Oliver la ve compartida. `diao` carga con el
  peso de la palabra caquetía para 'señor' — y puede, porque está en el cuerpo del
  texto, en Venezuela, con glosa y con atribución.
- **(b)** Se queda `caquetío-atestiguado` **con la reserva escrita** en `notas` y
  en `creencia-001`: el apoyo venezolano es editorial, no del cronista.
- **(c)** `caquetío-hipotético`, que es lo que la regla 2 pide para un dato cuyo
  único apoyo es una etiqueta de tercera mano.

**Recomendación del minador: (a).** No perdemos el concepto; perdemos una segunda
palabra que nunca estuvo. Y lo que sí ganamos es que la política «la atestiguada
manda» pueda aplicarse de verdad: hay una forma venezolana atestiguada para
'señor' (`diao`) y no hace falta la otra.

⚠️ Esto **no toca** la etimología de Oliver (`/da-/` 1sg + `/-(i)tiao/` sobre
lokona `/atti/`), ni su separación de `diao` y `datihao` en dos lexemas, ni el
prefijo `/d-/` como rasgo del caquetío. Toca de qué orilla es el testimonio.

---

## 3. Correcciones al corpus, con página

| Entrada | Qué hay que cambiar |
|---|---|
| `creencia-001` | forma **`boratio`**, una t (18 apariciones, imagen). Referencia a **t. II pp.298-299** (cuerpo) **+ t. IV p.595** (glosario). Decir que la atribución **caquetía** es del editor: Oviedo dice «los indios de Veneçuela». Las dos citas **no son independientes** (skill §8): no suben la entrada a «dos fuentes» |
| `creencia-001b` | página correcta, pero **«el díao es a la vez boratio» no está en Oviedo**. Partir: lo político cita Oviedo t. II p.299; lo religioso cita **sólo Arcaya** y baja de capa |
| `creencia-010` | hecho exacto y **atribuido explícitamente a los çaquitios** — pero la página es la **297**, no la 299-300 |
| `creencia-010b` | correcto. Ampliar a **pp.299-300**. Falta el cierre del rito: «É haçen á su semejança una figura de madera de relieve y pequeña … y **queman allí también esta imágen suya de palo**» |
| `creencia-010c` | correcto y verbatim. Matiz: `busera` es el nombre de la **xagua**, no de la bixa — el corpus lo tiene bien y el **glosario del editor** lo tiene mal |
| `creencia-004b` | correcto, p.329. **Añadir el testigo**: el obispo Bastidas «á voce viva», con Acuña, Naveros, Salvatierra y Limpias. ⚠️ Y **son dos ayunos distintos**: el de la p.329 (antes de cosa de importancia) y el que el boratio impone a la casa del enfermo (p.299). No fundirlos |
| ficha `tara` | 🔴 glosa **'langosta'**. Cuarta fuente y primera de primera mano: «Hay mucha **langosta**, que los indios llaman *tara* … si dá en un mahical, lo tala todo … también los indios en su venganza las toman y embanastan y **se las comen asadas**» (t. II p.331). No queda nada al otro lado de la balanza |
| ficha `macato` | ✅ **sin cambio**. El aviso de `jahn-1927.md` («comida vs. bebida») se cierra: Oviedo dice «çierto brevaje … muy espesso como maçamorra ó puches … algo açedo». Las dos cosas a la vez |
| ficha `hayo` | T1 lo degradó por duda de OCR en el t. I p.206. Aquí sale **limpio dos veces con glosa** (t. II pp.286, 294). Se puede levantar la duda. ⚠️ Pero es voz **areal**: el propio editor dice «común á diferentes comarcas … Venezuela y Nueva Granada», y el cuerpo lo confirma (pp.390, 408) |

---

## 4. Voces nuevas propuestas (ninguna toca el lexicón: esto propone)

Las tres que más valen, y las tres invisibles al OCR:

- **`datos`** (t. II p.331, imagen) — «cardones de los altos y derechos, á los
  quales en aquella tierra los llaman *datos*». 🟢 **`dato` sigue vivo en Falcón y
  Paraguaná.** ⚠️ Ojo a la homonimia: Oliver 1989 cap. 2 lista `dato` entre las
  voces caquetías con /d-/ inicial, donde es un **título**, no un cactus. O son
  homógrafos o alguien leyó mal; no se resuelve aquí.
- **`çemyrucos`** (t. II p.331, imagen) — «árboles … la fructa es muy semejante
  en la vista á las çereças». 🟢 **`semeruco`**, vivo en todo Falcón, con la
  comparación que explica el nombre castellano moderno.
- **`comoho`** (t. II p.331, imagen) — «otra fructa … que en efeto son tunas».
  ✅ **Segunda atestación independiente de verdad**: T1 lo halló en el t. I
  pp.313-314, otro libro y otro informante, doce años de diferencia.

Y cuatro más, con reservas escritas: `caça` (p.299), `icoraotas` (p.281),
`amana`/`aniana` (p.281, imagen **dudosa**: la tipografía no separa `m` de `ni`),
`haperon`/`raporon`/`baporon` (pp.286, 294, con la nota del propio editor
declarando la vacilación).

🔴 **Corrección de cadena en `icoraotas`**: la página imprime `icoraotas`, el
glosario del editor lematiza `Ycouoata` y Jahn escribe `icoroata`. Tres formas,
una palabra, y **sólo una está en el texto de Oviedo**.

⚠️ **Y regla 4**: `icoraotas` y `amana` son de los **corbaços** de la sierra del
Mene, no de los çaquitios. Los propios çaquitios de Oviedo están al sur y al
oeste de Coro, hacia la laguna y el Apure — **no son la polity costera que
simulamos**. Es dato caquetío de otra comarca de la esfera.

---

## 5. La pregunta del contacto — un cero grande, y un cero mío que era falso

### 🔴 Primero el error propio: las islas ABC sí están

En la primera pasada di por **0** `curazao`/`curaçao`, `aruba`/`oruba` y
`bonaire`/`buynare`/`boynare`. **Tercera vez en la misma sesión que un cero medía
mi ortografía y no la de la obra** — y la había escrito yo dos secciones más
arriba. Están en el **t. II, libro XXI cap. VI, impresas 131-132** (imagen):

> «más al Poniente de la isla de las Aves está la isla *Boynare*; más al Poniente
> de la isla Boynare está otra que se llama *Corazante*; más al Poniente de
> Corazante está la isla llamada ***Aruba***.»
>
> «no guardar los nombres primeros es poner confusión en todo. Á la que la carta
> llama *Corazante* **llaman los indios *Corazao***, y el almirante que la
> descubrió la dexó con su nombre: á la quel almirante llamó *Poregari* llaman
> agora *Yaruma* ó de *Orchilla*.»

El OCR las da `Boijnare`/`Boynarc` y `Aniba`. `Aruba` está **impresa como hoy**.
🟢 Atestación del nombre **indígena** de Curaçao con la fórmula que el proyecto
exige, y una defensa del topónimo indígena frente al cartográfico firmada por el
cronista. ⚠️ Pero **no dice de qué gente son esos indios** (`no-declarada`), y
`Poregari` es el nombre que puso **Colón**.

Y con la misma pasada cayó otro cero falso: **`Coquibacoa` se imprime
`Quiquibacoa`** (pp.132, 296).

⚠️ **Estas dos páginas no dan gente**: es una derrota de costa leída sobre la
carta de marear. Cambia el cero sobre los **nombres**, no el cero sobre el
**contacto**.

### El episodio de la hija de Manaure — no está

Se buscó expresamente (encargo del coordinador): la embajada de Manaure a Juan
de Ampíes c. 1525 con su «pariente y deudo» **Baracoica**, que vivía en las islas
ABC, y la hija llevada a La Española (Arcaya 1920 pp.160-161, 166-167). Sería la
**segunda fuente** del único contacto costa ↔ islas ↔ Antillas con parentesco que
el proyecto tiene.

🔴 **`Manaure` = 0. `Ampíes`/`Ampués`/`Anpies` = 0. `Baracoica`/`Varacoica` = 0.
La hija = 0.** En los tres tomos. Los seis «aciertos» de Ampíes en el t. II y los
cinco del t. IV son todos `anies` = «antes», comprobados uno a uno.

**Y hay una razón, no es azar**: el libro XXV arranca la historia de la provincia
**en 1528**, con la llegada de Alfínger y los Welser («de la venida de los
alemanes á la Tierra-Firme y gobernaçión del golpho de Venezuela, y del primer
gobernador», p.269). El período de Ampíes (1521-1528) **queda fuera del arranque
de su relato**. Oviedo no lo cuenta porque su libro empieza después. Quien lo
busque, al **libro XIX del tomo I** y a Las Casas.

### El resto de los ceros

«islas de los Gigantes» (el nombre) = **0** — los 42 «gigantes» de la obra son
los **patagones** del estrecho de Magallanes y los guyrandos del Plata ·
`Hayti`/`Haiti` = **0** fuera del glosario · indios de Venezuela en La Española =
**0** · taínos en Tierra Firme = **0** · «como en esta isla» y «la misma palabra»
= **0**.

Lo que cruza el mar en este libro son **españoles**: Alfínger llega a Santo
Domingo y pasa a su gobernación; los procuradores de Coro van a la Corte;
Federmann escribe desde Jamaica; el obispo Bastidas pasa de Venezuela al obispado
de San Juan. Ni un indígena.

**Lo que sí hay, y vale**, es la red de intercambio *dentro* de Tierra Firme, con
los çaquitios dentro:

> «Viven de pesquerias, é van é vienen á la ribera desta laguna y **rescatan é
> venden aquel pescado que matan, por mahiz é por otras cosas, con otras
> generaçiones de indios *çaquitios* é bubures**.» — t. II p.300, imagen

Y la red de la sal y el maíz de las pp.293-294, donde un náufrago español es
**comprado y vendido** entre tres nasçiones por un águila de oro y transportado
en canoa. Eso es la esfera, atestiguada, y va a `3-mundo/`.

**Oviedo compara tres veces** y ninguna es de lengua: los cuerpos («de la color y
estatura de los destas islas», p.329), el tabaco (p.298) y el funeral — y **ésa
separa**: el endocanibalismo de los huesos lo tiene por rasgo de **Tierra
Firme** y lo compara con Artemisia y Juan de Mena, no con La Española.

**Conclusión para la campaña**: la evidencia del contacto precolombino **no va a
salir de Oviedo**. Él es un buen testigo de dos vocabularios que no se tocan.
Decirlo ahorra noches (skill §6). Queda **el libro XIX del tomo I**, que T1 dejó
sin leer y señaló como «el libro con más costa de Venezuela»: si en algún sitio
de Oviedo están las islas de enfrente de Coro, es ahí.

Y una cosa que **sí** suma, aunque no sea léxica: el funeral de los çaquitios
(canto nocturno que recita las hazañas del muerto, cremación, huesos molidos,
bebida ritual) y el `areyto` antillano —que el glosario define «danza y cantar de
los indios, en que se celebraban las victorias y proezas de sus antepasados, **ya
en los funerales**»— hacen lo mismo con nombres distintos. **Paralelo de conducta
sin paralelo de palabra.** Es materia de esfera cultural y es más honesto que
forzar una etimología.

---

## 6. Otras entradas del glosario que este repo debería mirar

- **`Macana`** (t. IV p.601, imagen): «especie de maza de armas … **(Lengua de
  Haiti y Cuba.)**». El repo tiene abierta la etiqueta de `macana` (PR #184,
  issue `taino-caquetio-similitudes-2026-09-21.md`). Aquí hay atribución
  explícita, y **no es venezolana**. En el cuerpo del libro XXV las macanas las
  llevan los **guaypies** (p.305), tierra adentro, y Oviedo no dice que la palabra
  sea suya.
- **`Piache`** (t. IV p.603): «sacerdote supremo … entre los indios del Paraguay y
  de Huyapari». ✅ Confirma la auditoría del 2026-08-03. `piache` = **0** en el
  libro XXV. Lo que los çaquitios tienen es el **boratio**.
- **`Guaxiro`** (t. IV p.599): «capitán, jefe, caudillo ó señor entre los indios
  **caribes** de Tierra-Firme». Materia del mapa-familia; nadie lo había visto.
- **`Areyto`** (t. IV p.594): ver §5.

---

## 7. Cobertura real, por tomo

| Tomo | Leído entero | Leído por fórmula de nombrar | Sin leer |
|---|---|---|---|
| **II** (544 pdf / 530 impresas) | Libro XXV caps. IX (297-302) y XXII (328-332); apertura del libro XXV (269-271) | **Libro XXV entero**, 269-332: 88 pasajes extraídos con las diez fórmulas y leídos uno a uno | libros XX-XXIV (3-268) y XXVI-XXVIII (333-530) — sólo sondas |
| **III** (680 pdf / 646 impresas) | — | — | **todo**. Sondado y **cero**: `Veneçuela` 1, `çaquiti` 0, `diao` 0, `borat` 0, `Maracaybo` 0, `Curiana` 0, `Paraguaná` 0 |
| **IV** (656 pdf / 622 impresas) | glosario «Voces americanas» (593-607) y su bibliografía (608) | — | libros XXXIX-L (1-592) — sólo sondas; lo único de Venezuela es un naufragio que acaba en Coro (531-535), **sin lengua** |

Son 1.880 páginas impresas entre los tres. Se leyó el libro de Venezuela y el
apéndice, que era el encargo, y se dice lo que no se leyó.

---

## 8. Qué queda abierto

1. **La decisión sobre `datihao`** (§2). Es la que más mueve.
2. **La glosa de `tara`** (§3). Ya no hay nada al otro lado.
3. **El resto del glosario del tomo IV**: quince páginas de voces americanas
   glosadas **y atribuidas por lengua**. Para el taíno las hay a puñados y nadie
   las ha vaciado.
4. **El libro XIX del tomo I** y **el tomo I con imagen íntegra**
   (`historiageneral00fernguat`, 55 MB en Internet Archive). Es donde puede estar
   la gente de las islas ABC y, si está en Oviedo, el episodio de Ampíes.
5. **Los topónimos insulares a la campaña de topónimos**: `Corazao` (nombre
   indígena declarado), `Boynare`, `Aruba`, `Yaruma`/`Orchilla`, `Isla Roca`,
   `Páxaros ó de Aves`, `Quiquibacoa`, `Miraca`, `isla de Tara`, `Curiana` (río).
   No al lexicón: a `2-lengua/toponimos.yaml` por su puerta (`campana-toponimos`).
5. **Cruzar el mapa del libro XXV** (25 generaçiones, 26 pueblos, 11 ríos, 2
   caciques nombrados) contra `3-mundo/etnias.yaml`. ⚠️ Es el mapa **colonial** de
   1528-1546: regla 3, no se proyecta.
6. **La homonimia de `dato`** (§4): cactus en Oviedo, título en Oliver.
