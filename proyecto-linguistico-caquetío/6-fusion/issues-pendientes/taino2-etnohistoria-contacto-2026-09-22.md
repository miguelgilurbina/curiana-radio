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
`6-fusion/taino2_etnohistoria_contacto.yaml` (27 hallazgos + 3 de la Kaketiana).
Tu corrección del 21 (dc.4, PR #193) y lo que esta parcela le añade van en §3.

---

## 0. Lo que de este encargo resultó falso al medirlo

1. 🔴 **`decisiones_campanas_2026-09-21.yaml` §dc.4 no está en `main`: vive en
   el PR #193, sin mergear** — y **el error de decirlo fue mío**. Escribí «no
   existe en ninguna rama» apoyándome en `git log --all --diff-filter=A`, que
   devolvía cero. El cero era de mi consulta: el worktree se cortó de `main` y
   `--all` sólo ve lo que esta copia tiene. Con un `git fetch origin` delante,
   el mismo comando devuelve `f01e4e6`. Es **la regla 6 aplicada a git** —*un
   cero hay que verificarlo*— y es la misma familia que la trampa nº 5 de esta
   lista. La parcela arrancó sin su punto de partida y lo recuperó a mitad de
   camino; lo que dc.4 dice, y lo que esta parcela le añade, está en §3.

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
| **Oviedo, definiéndolo** | **«son pieças de cobre doradas; é si algund oro tienen, es muy poco ó ninguno»** | **Oviedo vol. I, p. 507** |

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

## 3. Tu argumento (dc.4) con esto en la mano

Lo que dijiste el 21:

> «aunque no sepamos de contacto precolombino conocemos que durante la
> conquista Manaure supo de parientes (incluso de su hija) que fue raptada y
> llevada a la Española. Y él mandó gentes a contactarlos y recuperarlos. Por
> lo que **debe haber habido contacto precolombino**. Y diao y diaitao que son
> símiles son las versiones caquetías de la versión Taína. Un cognado que hace
> match.»

### Lo que T7 le añade, y una corrección de alcance

**El tramo costa ↔ ABC te lo confirma por el otro lado, pero no es lo que
parece.** No es contacto entre dos mundos: es movimiento **dentro de la misma
polity**. Oliver es literal —el territorio caquetío costero al contacto
comprendía las llanuras de Falcón «**including the Netherland Antilles**»— y
esta parcela lo ve desde el mar: en agosto de 1499, el primer paso europeo por
esa agua recorre **Coro → Curazao → cabo de San Román → golfo de Coquibacoa**
como un solo tramo de costa (Navarrete t. III, pp. 7-9). Que Baracoica viva en
las islas y sea «pariente y deudo» de Manaure **prueba que la esfera cruza el
agua**. No prueba nada sobre los taínos.

Así que tu argumento se apoya en dos tramos de naturaleza distinta: el primero
es sólido y es de la esfera; el segundo (islas ↔ La Española) lo hacen barcos
castellanos entre 1513 y 1526. **El salto a precolombino cuelga entero del
segundo**, y ese salto es lo que yo tenía que ir a buscar en las fuentes.

### A favor, encontré una cosa — y es buena

El 12 de diciembre de 1492, antes de que ningún europeo hubiera bajado al sur,
los lucayos que Colón llevaba a bordo sostuvieron que detrás de La Española
había una tierra **que no estaba cercada de agua**, le dieron nombre y dijeron
que su gente les hacía daño. Es noticia indígena, es necesariamente anterior a
los europeos, y va en tu dirección. Lo que no hace es localizar la tierra.

### En contra, encontré dos

En Paria, 1498, con gente de las islas a bordo, **no se entendieron**, y lo
escribió Colón. Y en los tres libros de Anglería que narran Paria, Curiana y
Pinzón la palabra «intérprete» no sale ni una vez, mientras sale once en los
libros de las islas.

### Pero eso **no contradice** lo de `datihao` — y ahí está lo interesante

Que una institución y su nombre sean compartidos por taíno y caquetío, **y** que
en Paria nadie se entendiera, no son dos hechos en pelea: **son la firma de una
cadena**. Un nombre de alianza entre señores viaja de tramo en tramo sin que los
extremos se hablen. Y Anglería lo dice de las ferias de Curiana con todas las
letras: se comercia «**pero de cerca**», y el oro aleado «**se les llevan de
otras partes á cambio**» (vol. 1, pp. 308-309). El modelo que el material
aguanta es el de **eslabones cortos**, no el del viaje largo — que es, dicho sea
de paso, una hipótesis más fuerte y más comprobable que «hubo contacto».

### Y sobre `datihao`, un aviso de calidad

Fui a leer la atestación de San Juan en el Oviedo que ya teníamos
(vol. I, lib. XVI cap. V, p. impresa 473). Dice:

> «é cómo llegó luego Agueybana, **dixo la lengua, en el lenguaje de los
> indios**: "Señor, ¿por qué me mandas matar? Yo te serviré é seré tu naboría";
> y entonces dixo el cacique: "Adelante, adelante, **á mi dalihao (que quiere
> decir mi señor, ó el que, como yo, se nombra)**, dexa ese bellaco."»

**La calidad de esta atestación es la mejor de toda la serie, y lo es por el eje
de esta parcela: quién tradujo.** Quien habla es Johan González, a quien Oviedo
llama dos veces «la lengua» y una «**grande lengua**» — un español que sabía
boriquén lo bastante para meterse desnudo y pintado en un areíto y entender lo
que cantaban. Y la glosa de Oviedo, «**el que, como yo, se nombra**», es la del
intercambio de nombres: la institución, no un título.

⚠️ **Dos reservas, y las dos importan.** (a) La capa de texto lee `dalihao`, no
`datihao`, que es la confusión l/t del OCR que la campaña de Oviedo ya había
marcado como urgente — y **la imagen escaneada de ese PDF no llega a la
p. 473**. Medido hoy sobre las 766 páginas del vol. I: `datihao` 0 ·
`guatiao` 0 · `tiao` 0, y `dalihao` 1. La forma no se cita hasta verla en otra
copia. (b)
dc.4 pone las dos atestaciones en pie de igualdad; no lo están: **ésta se puede
leer y pesar, y la de «los indios de la Provincia de Venezuela» el proyecto no
la ha visto** — está en un tomo que no tenemos y llega por Jahn 1927 p. 213
n. 29. Antes de llamarlo «cognado que hace match», leer la segunda.

### Y una cosa que ordena todo el apartado del guanín

Oviedo lo **define**, en el volumen que ya teníamos:

> «**porque el letor entienda qué cosas son guanines, para adelante digo que son
> pieças de cobre doradas; é si algund oro tienen, es muy poco ó ninguno**»
> — vol. I, lib. XVII cap. IX, p. impresa 507

Cobre dorado. Eso hace que el «oro bajo» de Colón, el «oro aunque no puro… como
el alemán de que se acuñan los florines» de Anglería y el «color algo morada» de
Las Casas sean el mismo objeto, y confirma que hablamos de la aleación del
istmo.

⚠️ **Y de paso demuestra el vector 1 de Oliver en el acto**: ese pasaje es de
**Yucatán**, y Oviedo aplica sin pestañear una palabra antillana a unos objetos
mayas, con un intérprete español de por medio. Que un cronista llame `guanín` a
algo **no atestigua que allí se llamara así** — lo cual rebaja, y no poco, las
dos apariciones de Chiribichi que yo mismo había puesto arriba.

---

## 4. 🔴 El hallazgo lateral, que es el que más mueve el repo

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

## 5. Lo poco que estas obras dan de la Kaketiana, y es dato

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

## 6. Qué le hace todo esto a la hipótesis — con letras

dc.4 dejaba tres afirmaciones con tres etiquetas, y sólo la tercera abierta:
costa ↔ ABC con parentesco = `atestiguado`; costa/islas ↔ La Española 1513-1526
= `atestiguado`, colonial; **contacto precolombino con las Antillas Mayores =
`hipotético`, pendiente de ti**. Es esa tercera la que esta parcela fue a medir.

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
Entran al repo la bitácora de las seis obras, las 27 citas clasificadas y las
negativas medidas, para que nadie vuelva a gastar una noche en esto. La
hipótesis conserva su capa y gana algo que no tenía: **un cuerpo de evidencia
negativa bien medida**, que es lo que permite decir dónde habría que buscar
después.
*A favor*: es lo que la regla 2 manda —en duda, degradar— y lo que el estado
del material aguanta. *En contra*: no te da lo que pediste.

**C. Se parte en dos afirmaciones, y cada una toma su capa.**
- **C1 — «el guanín circulaba entre Tierra Firme y las Antillas Mayores antes
  de 1492»**: a esto los textos le dan bastante. El objeto está en las dos
  orillas, lo define un cronista como cobre dorado, tiene un nombre común, y
  los isleños decían que venía de fuera. Podría ir a `reconstruido` con el
  apoyo de estas citas.
- **C2 — «la esfera caquetía participaba en ese circuito»**: a esto los textos
  no le dan nada. Se queda `hipotético`, y con una razón escrita.
*A favor*: es lo que de verdad mide el material, y separa lo que hoy está
fundido en una sola frase. *En contra*: parte una afirmación que formulaste
entera, y C1 no es de este proyecto (es del Caribe, no de la Kaketiana).

**E — la que salió al leer dc.4, y no estaba antes.**
**Se cambia la afirmación por una más fuerte: «el contacto, si lo hubo, fue por
CADENA de tramos cortos, no por travesía».** Esto no es una etiqueta más floja:
es una hipótesis **con predicciones**. Predice lo que encontramos —institución y
nombre compartidos (`datihao`) **y** ninguna inteligibilidad en Paria— porque un
nombre de alianza viaja de eslabón en eslabón sin que los extremos se hablen. Y
predice lo que Anglería dice de las ferias de Curiana: se comercia «**pero de
cerca**» y el oro aleado «**se les llevan de otras partes á cambio**». Y es
falsable: si aparece un objeto antillano en las ABC o un dabajuroide en las
Mayores, la cadena tiene un tramo que no debería.
*A favor*: convierte una creencia en un programa. *En contra*: reformula lo que
dijiste, y eso lo decides tú, no yo.

**D. Baja.**
No. Nada de lo medido contradice el contacto: lo que hay es ausencia de
registro, y la ausencia de registro en cronistas que preguntaban por el oro no
es evidencia de ausencia. Se descarta.

### Mi recomendación

**C + E.** C porque es la única que no miente en ninguno de los dos sentidos:
dice que sí hay un circuito del guanín documentado por los propios indios entre
el continente y las islas grandes, y dice que la Kaketiana no aparece en él. Y E
porque es lo que tu propio argumento pide cuando se le quita el salto: tú
observaste que Manaure tenía parientes al otro lado del agua y mandó gente a
buscarlos — **eso es exactamente un eslabón**, y el modelo de eslabones explica
los dos hechos que parecían reñidos (`datihao` compartida, Paria mudo) sin
forzar ninguno.

Y deja el trabajo siguiente **nombrado**: si C2 ha de subir alguna vez, lo que
lo subiría es un objeto, no una crónica — el oro de Curazao de 1502
(`t7.kak2`) es exactamente ese objeto, y está a tres folios de distancia.

Si prefieres una sola afirmación y ninguna reformulación, entonces **B**.

---

## 7. Lo que haría falta, en orden de coste

| Qué | Por qué | Coste |
|---|---|---|
| **Navarrete, *Colección diplomática*, t. II — autos del pleito de Hojeda, fols. 16-21** | Decide si hubo o no oro en Curazao en 1502. Es la única pieza de esta parcela que podría mover la Kaketiana | bajo — dominio público, archive.org |
| **Historia del Almirante, vol. 1** (`historiadelalmir01col`) | 1.º y 2.º viaje, y el capítulo donde Hernando reproduce a Pané. Para T2 | bajo — 382 KB |
| **Las Casas, *Historia de las Indias*, vols. 2-3** | El tercer viaje y los viajes menores en la versión de Las Casas. Hoy sólo tenemos el vol. 1, que acaba en 1493 | bajo-medio |
| **Pedro Simón, *Noticias historiales*** | Es quien dice que Coro se fundó en «una provincia llamada Curiana». Cerraría #33 por el otro lado | medio |
| **Granberry & Vescelius 2004** | Separa las siete comunidades de habla antillanas. Decidiría qué taíno es cada voz | alto — en copyright |

---

## 8. Lo que vi de paso

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
