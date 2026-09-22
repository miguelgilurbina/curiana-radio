# Lo que sabían unos de otros en 1492-1500 — y qué hace eso con la hipótesis

**Segunda campaña del taíno, parcela T7 (la etnohistoria del contacto),
2026-09-22.** Encargo de Miguel: «*Ve avanzando con la búsqueda, descarga y
minado de fuentes para corroborar pre contacto con Taíno y minar más info*», y
la noche anterior: «*Yo creo que tiene que haber una forma de probar si hubo
algún tipo de contacto. O sea de que es plausible es plausible.*»

**Ninguna cifra de este borrador está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/medir_taino2_etnohistoria.py
python 6-fusion/scripts/medir_taino2_etnohistoria.py --obra angleria-v1
```

Los hallazgos con su cita literal, su clase, su época y su fuerza están en
`6-fusion/taino2_etnohistoria_contacto.yaml` (24 hallazgos + 3 de la Kaketiana).

---

## 0. Lo que de este encargo resultó falso al medirlo

1. 🔴 **`6-fusion/decisiones_campanas_2026-09-21.yaml` no existe.** El encargo
   lo daba como el punto de partida de esta parcela — «§dc.4, la corrección de
   Miguel sobre el episodio de la hija de Manaure: LÉELA ENTERA». No está en el
   árbol de trabajo, no está en `main`, y `git log --all --diff-filter=A` sobre
   ese patrón devuelve cero. Lo único que el repo tiene sobre «la hija de
   Manaure» es la tradición del topónimo **Judibana**, que es otro asunto. **La
   parcela arrancó sin su punto de partida.** Si esa corrección existe, hay que
   traerla al repo antes de que una tercera campaña vuelva a buscarla.

2. **`keegan-1989` no está en el repo.** El encargo lo listaba como «ya en el
   repo». Su nota declara `local: null` y «NO consultado en texto completo»
   desde el 2026-07-29 — y sostiene dos hechos del corpus.

3. **«Mártir es explícito con Curiana… busca *intérprete*»** — lo es, pero al
   revés. `intérprete` sale **11 veces** en el vol. 1 y **las 11 caen antes del
   libro VII**, es decir en los libros de La Española y Cuba. En los tres
   libros que narran Paria, Curiana y el viaje de Pinzón: **cero**. Control en
   el mismo volumen: `lengua` 17, `entend` 26, `por señas` 8.

4. **«La Isla de los Gigantes» en Anglería vol. 4 es un falso amigo.** Los 9
   aciertos de `gigante` son el **rey gigante Datha de Duhare**, de la
   expedición de Ayllón a las Carolinas. Ni uno es Curazao.

5. 🔴 **Un espacio literal vale cero sobre el OCR de archive.org.** Los
   `_djvu.txt` separan palabras con **dos** espacios. `no se entendian`
   devolvía 0 justo en el texto donde está la frase entera y **en la propia
   mano de Colón**; `tierra firme` devolvía 0 en Hernando Colón, donde sale 37
   veces. Es la trampa de `minar-fuente` §2 con otra cara, y el medidor la cose
   de una vez: cada espacio de una diana pasa a `\s+`.

---

## 1. El veredicto, en una frase

**Los europeos sí preguntaron, y lo que trajeron es asimétrico**: los isleños
tenían noticia de una tierra firme al sur que no habían visto y cuya gente les
hacía daño; los de la costa tenían el oro bajo que los taínos llamaban `guanín`
y decían que les venía del **oeste por tierra**; y en el único punto de Tierra
Firme donde la lengua se puso a prueba —Paria, agosto de 1498— Colón escribió
de su mano que **no se entendían**.

---

## 2. Lo que sí hay, y de dónde sale

### ⭐ El mejor apoyo de la hipótesis: los lucayos nombraron una tierra que no estaba rodeada de agua

> «**Parece que los indios dichos daban á entender que el Babeque era tierra
> firme, porque decian que no estaba cercada de agua, y que estaba detras desta
> isla Española, la cual llamaban Caritaba ó Caribana, que era como cosa
> infinita**; y á mi parecer, que, cierto lo decian por tierra firme, y que
> **debian tener noticia de la tierra firme**… le parece que tienen razon en
> nombrar tanto á Babeque, y por otro nombre á Caribana, porque **debian de ser
> trabajados de la gente della**»
> — Las Casas 1875, vol. 1, **lib. I, cap. LIII** (pdf 417, impresa ~369)
> — 12 de diciembre de 1492

Es **noticia indígena recogida**, y la fecha la hace inevitablemente anterior a
los europeos: 12 de diciembre de 1492. Indios lucayos, nacidos en las Bahamas,
sostuvieron ante Colón que detrás de La Española había una tierra grande que no
estaba rodeada de agua, le dieron nombre, y dijeron que su gente les hacía
daño.

**Lo que no sostiene**, y hay que decirlo entero: no identifica el lugar
—`Caribana` es la punta oriental del golfo de Urabá en la cartografía
posterior, y usar eso aquí sería proyectar hacia atrás un nombre que los
españoles fijaron después—; no describe comercio sino razzias recibidas; y el
propio Las Casas escribe «**cuanto el Almirante creia que entendia**».

Y en la misma obra, cien páginas antes, está el control que lo descuenta:

> «**De donde parece, que ninguna ó cuasi ninguna cosa les entendian**, porque,
> en esta isla, ni nunca hobo gente de un ojo, ni caníbales que comiesen los
> hombres» — **lib. I, cap. XLVII** (pdf 391, impresa ~346)

### ⭐⭐ El guanín, contestado por el primario

El encargo pedía «*recoge TODO lo que digan las fuentes, literal*». Lo que
dicen, ordenado:

| Quién | Dónde venía el guanín | Fuente |
|---|---|---|
| taínos de La Española, 1492 | de otro sitio; Colón entendió «una isla llamada Guanín» y **Las Casas le corrige**: no había tal isla | Las Casas, caps. LX y LXVII |
| taínos de Samaná, 1493 | «en otras islas, como Carib y Matinino» | Las Casas, cap. LXVII |
| **gente de Paria, 1498** | **«una tierra frontera dellos al Poniente, que era muy alta, mas no lejos»** | **Colón, de su mano**, Navarrete t. I p. 401 |
| curianenses (Cumaná), 1500 | de Cauchieto, «hacia el Occidente, por costa derecha, seis soles» | Anglería vol. 1 p. 310 |
| mercaderes de Chiribichi, c. 1520 | es la mercancía de la feria: «oro ó alhajas de oro, **que ellos llaman guanines**» | Anglería vol. 4 pp. 335-336 |
| gente de Veragua, 1502 | **«se cogía en la tierra firme muy cerca de ellos»**; águilas y espejos de guanín | Hernando Colón p. 165 |

Leído junto: **el guanín de las islas se decía de fuera y nunca de un sitio
comprobable; el guanín de Tierra Firme se decía del oeste; y donde se hacía de
verdad era el istmo.** Los dos extremos apuntan al mismo foco lejano. Ninguno
apunta al otro.

🔴 **Y una paráfrasis que hay que retirar de circulación.** Hernando Colón
escribe que los de Paria decían que el guanín «nacía en **otras islas
occidentales**» (p. 57). Su padre escribió «**una tierra** frontera dellos al
Poniente, que era muy alta», y Anglería, parafraseando el mismo papel, escribió
«ciertos montes de enfrente» (vol. 1, p. 272). Dos dicen tierra, uno dice islas,
y el que dice islas es el que pasó por el italiano de Ulloa. Donde está el
primario, la paráfrasis no suma: resta.

### ⭐⭐⭐ La lengua — y aquí la parcela da su resultado más limpio

> «los llevaron á una casa muy grande hecha á dos aguas… y hicieron traer pan, y
> de muchas maneras frutas é vino… **Recibieron ambas las partes gran pena
> porque no se entendían, ellos para preguntar á los otros de nuestra patria, y
> los nuestros por saber de la suya.**»
> — **Cristóbal Colón**, *Relación del tercer viaje*, en Navarrete t. I, p. 400

Anglería lo parafrasea —«Les molestaba mucho el no poder entender á los
nuestros ni ser ellos entendidos», vol. 1, p. 273— y es **el mismo testigo, no
un segundo** (skill §8).

⚠️ **Lo que el texto no dice**: no dice que hubiera intérpretes taínos en las
barcas y que fracasaran. Dice que «los nuestros» y «ellos» no se entendieron.
Como evidencia de que el taíno no servía en Paria es fuerte por contexto, no
por letra. **No la sobrevendamos.**

Lo que la rodea sí es un silencio con forma:

- Anglería **nombra** al intérprete cuando lo hay y dice cómo de bien entendía
  — «sirviendo de intérprete Diego, **cuyo idioma era casi semejante al de
  éstos**» (p. 182, Cuba); «por medio del intérprete Diego Colón, **que
  entendía aquel idioma**» (p. 198).
- Y sabe registrar el fracaso dentro de las islas: en La Navidad, el hermano de
  Guacanagarí «habló en su lengua… pero, **como no había intérpretes, no
  entendieron lo que decía**» (p. 144).
- Y en los tres libros de Tierra Firme, ninguno: **cero de once**. Ahí escribe
  «por señas» — incluso para obtener el topónimo: «**coligieron por señas** que
  aquella tierra se llamaba Paria» (p. 268), y en Curiana «**con gestos y
  señas** les dio á entender» (p. 304).
- En el relato completo de los viajes menores (Hojeda 1499, Niño y Guerra
  1499-1500, Hojeda 1502), `intérprete` **cero** sobre 19 aciertos del volumen,
  y `lengua` **una** vez: el español **Juan de Buenaventura**, a quien Bastidas
  dejó en Santa Marta, que «había permanecido **trece meses** tratando con los
  indios y aprendiendo su lengua» (Navarrete t. III, p. 34).

**El único hombre que en 1502 entiende a los indios de esa costa es un español
que se quedó trece meses a aprender.**

### Los caribes y la ruta

- **Una cabeza de caribe clavada en la puerta de un principal de Curiana**
  (Anglería vol. 1, p. 315). Estaba ahí antes de que llegara la nave.
- `carib` glosado por los dominicos de Chiribichi como **'más fuerte que los
  demás' en todas las lenguas de aquellos países**, y sus flotas «á caza de
  hombres… **recorriendo innumerables islas**» (vol. 4, p. 331); canoas «capaces
  de **80 remos**», navegando «en ordenada formación, **muchas millas desde sus
  confines**» (vol. 4, p. 133).
- Las canoas de **Paria**, vistas por Colón, «son **muy grandes** y de mejor
  hechura que no son estas otras… y en el medio de cada una tienen **un
  apartamiento como cámara**» (Navarrete t. I, p. 401).
- La ruta, cuando alguien la describe, es **la cadena**: «van **renclera de
  islas**, desde la de Sant Juan… hasta la de la Trinidad, que se apega con la
  tierra firme de Paria… y **cada noche, yendo en un barco, pueden dormir en
  una dellas**» (Las Casas, cap. LXVIII).
- Y la única travesía larga documentada es de 1520 y es una fuga: un carpintero
  yucayo vació un tronco, lo cargó de maíz y calabazas de agua y llevaba
  **doscientas millas** cuando lo interceptaron (Anglería vol. 4, pp. 74-75).

---

## 3. 🔴 El hallazgo lateral, que es el que más mueve el repo

**Hay dos Curianas, y Navarrete las separa con un documento.**

> «Ambos llaman **tierra de Curiana**, que es el rescate de las perlas, **á la
> costa que está enfrente de la Margarita, y comprende la costa de Cumaná y
> golfo de Cariaco**. Comprueba esta situación de Curiana el artículo 1.º de la
> capitulación que hizo Hojeda con los Reyes católicos, donde se le previene
> "que no toque en la tierra del rescate de las perlas de esta parte de Paria,
> desde el paraje de los Frailes, antes de la Margarita, fasta el Farallón,
> **tierra que se llama Curiana**"… **Nuestros historiadores trastornaron este
> viage, porque ignoraron la verdadera situación de Curiana.**»
> — Navarrete t. III, p. 13 n. 4

> «El P. Fr. Pedro Simón… dice que **la ciudad de Coro está fundada en una
> provincia de indios llamada Curiana**… que la fundó el año 1517 el capitán
> Juan de Ampíes, cerca del pueblo que los indios llamaron Curiana… **Esta
> Curiana es distinta de la que hemos hablado en la nota 4 de la pág. 13.**»
> — Navarrete t. III, p. 32 n. 3

Esto toca el **issue #33** y toca material **ya fusionado**: la cita de
Anglería sobre Curiana ↔ Cauchieto, que la primera campaña usó como «la forma
de la red» (`4-fuentes/angleria-1892.md` §2026-09-21 y
`6-fusion/taino_en_la_esfera_2026-09-21.yaml`), **describe una red de la costa
oriental de Venezuela, a 400-800 km de Coro**. La conclusión de T5 —«la red es
continental y de eje este-oeste»— **se sostiene**; lo que deja de sostenerse es
que sea una red de la Kaketiana. T5 ya había puesto el aviso («qué nombra
Curiana sigue en disputa»); lo que esta parcela añade es el documento.

**No lo cierro yo**: lo dejo medido, con las dos citas y su apoyo documental,
para que lo decidas.

---

## 4. Lo poco que estas obras dan de la Kaketiana, y es dato

- **El primer paso europeo, agosto de 1499**: Hojeda, Juan de la Cosa y
  Vespucio pasan de la ensenada de Coro a **Curazao, «que llamaron de los
  Gigantes»**; de allí a la península del **cabo de San Román** (Paraguaná); y
  entran en «un gran golfo… **Los indios le llamaban Golfo de Coquibacoa**»,
  con la gran población de casas sobre estacas (Navarrete t. III, pp. 7-9). El
  nombre indígena del golfo, **dicho como indígena**.
- **1502, Curazao**: los de Hojeda «notaron que **traían ciertos pedazos de oro
  colgados de las narices y orejas**; pero nada les tomaron» (p. 34, §26).
  ⚠️ Y la nota 3 de la misma página: «Así lo aseguran algunos testigos: **otros
  presentados por Vergara y Ocampo dicen que no vieron oro**». Es testimonio de
  pleito, con dos partes interesadas. **En duda, degradar** (regla 2). Si se
  sostuviera, sería metal en las islas de la polity costera en 1502 y el metal
  no se hace allí. **Se cierra leyendo los folios 16-17, 19 y 21 de los autos**,
  publicados en la *Colección diplomática* de Navarrete, tomo II.
- Y el negativo: `curiana` **0** y `coquibacoa` **0** en Las Casas vol. 1 y en
  Hernando Colón. **Quien busque la Kaketiana en los cronistas del taíno no la
  va a encontrar, y eso no es un hallazgo sobre la Kaketiana.**

---

## 5. Qué le hace todo esto a la hipótesis — con letras

El estado actual de la afirmación «hubo contacto precolombino entre la esfera
caquetía y el mundo taíno» es `hipotético`. Con lo de esta parcela en la mano:

**A. Sube a `reconstruido`.**
*A favor*: hay noticia indígena, anterior a cualquier intermediación europea,
de que los isleños sabían de una tierra firme al sur y de su gente; hay una
ruta física descrita y transitable a saltos; hay flotas de ochenta remos
moviéndose por «innumerables islas»; y hay un objeto —el guanín— que
efectivamente circula desde un foco continental hasta las Antillas Mayores.
*En contra*: nada de eso toca la **Kaketiana**. La tierra firme que los lucayos
nombraron no se puede localizar sin proyectar hacia atrás un topónimo colonial;
el guanín llega a las islas desde el istmo, no desde Coro; y la única prueba de
lengua disponible salió negativa. **Subir de capa con esto sería subir por
plausibilidad, no por evidencia.**

**B. Se queda en `hipotético`, pero con el expediente escrito.**
Entran al repo la bitácora de las cinco obras, las 24 citas clasificadas y las
negativas medidas, para que nadie vuelva a gastar una noche en esto. La
hipótesis conserva su capa y gana algo que no tenía: **un cuerpo de evidencia
negativa bien medida**, que es lo que permite decir dónde habría que buscar
después.
*A favor*: es lo que la regla 2 manda —en duda, degradar— y lo que el estado
del material aguanta. *En contra*: no le da a Miguel lo que pedía.

**C. Se parte en dos afirmaciones, y cada una toma su capa.**
- **C1 — «el guanín circulaba entre Tierra Firme y las Antillas Mayores antes
  de 1492»**: a esto los textos le dan bastante. El objeto está en las dos
  orillas, tiene un nombre común, y los isleños decían que venía de fuera.
  Podría ir a `reconstruido` con el apoyo de estas citas.
- **C2 — «la esfera caquetía participaba en ese circuito»**: a esto los textos
  no le dan nada. Se queda `hipotético`, y con una razón escrita.
*A favor*: es lo que de verdad mide el material, y separa lo que hoy está
fundido en una sola frase. *En contra*: parte una afirmación que Miguel formuló
entera, y C1 no es de este proyecto (es del Caribe, no de la Kaketiana).

**D. Baja.**
No. Nada de lo medido contradice el contacto: lo que hay es ausencia de
registro, y la ausencia de registro en cronistas que preguntaban por el oro no
es evidencia de ausencia. Se descarta.

### Mi recomendación

**C.** Porque es la única que no miente en ninguno de los dos sentidos: dice que
sí hay un circuito del guanín documentado por los propios indios entre el
continente y las islas grandes, y dice que la Kaketiana no aparece en él. Y
porque deja el trabajo siguiente **nombrado**: si C2 ha de subir alguna vez, lo
que lo subiría es un objeto, no una crónica — el oro de Curazao de 1502
(`t7.kak2`) es exactamente ese objeto, y está a tres folios de distancia.

Si prefieres una sola afirmación, entonces **B**.

---

## 6. Lo que haría falta, en orden de coste

| Qué | Por qué | Coste |
|---|---|---|
| **Navarrete, *Colección diplomática*, t. II — autos del pleito de Hojeda, fols. 16-21** | Decide si hubo o no oro en Curazao en 1502. Es la única pieza de esta parcela que podría mover la Kaketiana | bajo — dominio público, archive.org |
| **Historia del Almirante, vol. 1** (`historiadelalmir01col`) | 1.º y 2.º viaje, y el capítulo donde Hernando reproduce a Pané. Para T2 | bajo — 382 KB |
| **Las Casas, *Historia de las Indias*, vols. 2-3** | El tercer viaje y los viajes menores en la versión de Las Casas. Hoy sólo tenemos el vol. 1, que acaba en 1493 | bajo-medio |
| **Pedro Simón, *Noticias historiales*** | Es quien dice que Coro se fundó en «una provincia llamada Curiana». Cerraría #33 por el otro lado | medio |
| **Granberry & Vescelius 2004** | Separa las siete comunidades de habla antillanas. Decidiría qué taíno es cada voz | alto — en copyright |

---

## 7. Lo que vi de paso

1. **La bitácora de `angleria-1892` da el vol. 1 por «no dio nada relevante»**
   en su sesión de 2026-07-29, y luego T5 sacó de él la cita más citada de la
   primera campaña, y ahora T7 ocho más. Una fuente «que no dio nada» suele
   significar «que no se le preguntó nada».

2. **`las-casas-1875` es sólo el vol. 1** y acaba con el regreso del primer
   viaje. Media docena de cosas que el repo atribuye a «Las Casas» tendrían que
   decir a qué volumen, porque el que tenemos no llega.

3. **Nadie ha medido el desfase de página de los PDF escaneados y lo ha escrito
   en la nota.** Lo calculé tres veces hoy (Anglería vol. 1: impresa = pdf − 64;
   vol. 4: − 8; Las Casas: 0) y va ahora en el medidor, pero es el tipo de dato
   que debería vivir en el frontmatter de la fuente y no en la cabeza del
   minador de turno.
