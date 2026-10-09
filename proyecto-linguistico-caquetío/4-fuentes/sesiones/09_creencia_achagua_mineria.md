---
tipo: mineria
corpus: [creencia.yaml]
fecha: 2026-10-09
pueblo: achagua
pregunta: "¿Qué creían y hacían los achaguas con sus dioses, sus especialistas, sus muertos y sus fiestas; qué dice Gilij de los maipures; y qué de eso corrobora, contradice o no toca lo que el canon caquetío atestigua o reconstruye desde el wayuu?"
ensayo: 03_creencia_caquetia
moc: mapa-creencia
plan: 08_creencia_achagua_que-minar
propuesta: 6-fusion/creencia_achagua_2026-10-09.yaml
estado: "minado: Rivero lib. II caps. VI-VIII, Neira y Ribero preguntado por la creencia, Gilij t. III lib. I; propuesta sin fusionar"
---

# Creencia achagua: la minería

> [[08_creencia_achagua_que-minar|el plan]] · [[03_creencia_caquetia|ensayo]] · [[mapa-creencia]] · [[03_creencia|hoja de la sesión 3]]
> Fuentes: [[rivero-1883]] · [[neira-ribero-1762]] · [[gilij-1780-1783]] · (de paso) [[steward-1948-hsai-4]] · [[gumilla-1791]]
> Propuesta: [[creencia_achagua_2026-10-09]] · censo y validador: `6-fusion/scripts/censo_creencia_neira_ribero.py`
> Método: [[metodo-comparativo]] · skills `minar-fuente` y `leer-fuente`

Bitácora de la minería que el plan del 2026-10-08 dejó ordenada. No se
descargó nada (Gilij t. II espera el ok de Miguel). No se tocó el corpus, el
lexicón, el ensayo, los índices ni el YAML de la transcripción de Neira: todo
lo que se propone está en la propuesta, y lo que hay que corregir en otras
notas está listado abajo (§5) para quien integre.

Regla de capa: la **opción C** de Miguel (2026-10-09). Lo nuevo es
`reconstruido` sólo con dos tradiciones arahuacas independientes, `hipotetico`
con una, y `lectura` si sólo ilumina un hecho caquetío ya atestiguado. Las
cifras (hechos por capa y por medio, el censo del vocabulario) no se escriben
aquí: las da `python 6-fusion/scripts/censo_creencia_neira_ribero.py`, que
además valida la propuesta.

## 0. En una línea

El achagua **corrobora con un observador independiente** tres gestos que el
caquetío ya atestigua (el llanto que canta lo que el muerto hizo, el ajuar
para el camino, la muerte por hechizo), da **una segunda hermana arahuaca** a
tres hechos de la Vía A (el especialista que cura con tabaco y canto, el alma
que sale y vuelve, el muerto temido) y **no da nada** al segundo entierro, al
beber los huesos, a la exhumadora ni a los huesos que traen la lluvia.

## 1. Qué se leyó y cómo

| Obra | Qué | Cómo | Imagen |
|---|---|---|---|
| [[rivero-1883]] | lib. II caps. VI-VIII, pp. 102-118, enteros | OCR de archive.org para localizar; desfase pdf − 21 | todas las citas que deciden una capa: pp. 104-108, 110-113, 115-116, 118; y fuera del tramo pp. 198 y 211 |
| [[neira-ribero-1762]] | el vocabulario, preguntado por la creencia | consultas y un censo por script sobre `6-fusion/achagua_neira_ribero_1762.yaml` | cada voz que se cita: pliegos 35, 41-43, 49, 52-53, 56-57, 61-62, 68-69, 74, 78-79, 89, 92 (recortes a 2,2-4,2 px/pt; `Prubisana` a 9) |
| [[gilij-1780-1783]] | t. III, libro I «Della religione antica degli Orinochesi», pp. 1-34, entero | el `.ocr.txt` del repo; desfase − 21 hasta el pdf 50 y − 19 después | pp. 6-7, 9-10, 13-15, 17-18, 20-24, 29, 32-34, 159 y la nota de la p. 402 |

**Independencia (minar-fuente §8).** Juan Ribero, coautor del vocabulario, es
Juan Rivero: crónica y vocabulario son **un testigo**. Gilij es otro
observador, de otro pueblo (los maipures) y con informantes con nombre (el
regolo Caravàna); pero para él el achagua es «un dialetto del Maipùre»
(t. III p. 205), de modo que achagua y maipure son **dos observadores de una
misma tradición**. Así se contaron. Si cuentan como dos tradiciones para la
opción C, lo decide Miguel (§7): de eso depende que varios `hipotetico` suban.
Hernández de Alba (HSAI) resume a Rivero, Gumilla y Karsten y no cuenta.

**Precontacto frente a colonial.** Todo es colonial. Rivero escribe hacia 1736
«lo que he hallado... averiguado por larga experiencia de los fundadores de
estos pueblos» (p. 102): la gentilidad recordada del XVII y los pueblos de
misión de su tiempo, con el marco del demonio y la busca del «verdadero
Dios». Gilij escribe en Roma (1782) de su misión de 1749-1767, para probar a
los «increduli» que los orinoquenses conocían por tradición lo revelado. Cada
hecho de la propuesta dice en `describe` qué cuenta la fuente y cómo se
escribió; lo que lleva huella doctrinal clara no se proyecta.

## 2. Qué se halló

### 2.1 [[rivero-1883]], caps. VI-VII (los achaguas)

- **Sin culto, con tradición.** «No adoran ídolos los Achaguas» (p. 104); al
  creador lo conocen «pero no por eso le adoran», y a los dioses menores «no
  para adorar en ellos, sino como una pura tradición y fábula que les contaban
  sus viejos» (pp. 112-113). → `ach-cr-01`, `lectura` de creencia-008c.
- **Cuaygerri**, «el que todo lo sabe», que creó el cielo y las demás cosas,
  «y esto enseñan á sus hijos» (p. 112). La imagen dice *Cuaygerri* las dos
  veces: el *Cuoygerri* del plan es del OCR. → `ach-cr-02`, `hipotetico`.
- **Los dioses con dominio** (p. 113): *Jurrana-minari* (labranzas), *Baraca*
  (riquezas), *Cuisiabirri* (fuego), *Pruvisana* (temblores), *Achacató* (dios
  tonto), y «un catálogo de dioses y diosas, que omito». → `ach-cr-03`.
- **La yopa** (pp. 104-105): adivinación colectiva antes de la guerra o el
  viaje, por la ventana de la nariz. Planta del llano y práctica de todo el
  llano (los airicos «como los Achaguas», p. 116). → `ach-cr-08`, no se
  proyecta.
- **El sueño al alba** (p. 105): cada mañana, en cada caney, «empezando el
  primero de todos su Cacique ó Capitán», se cuentan los sueños «en tono de
  lamentación». No es cosa del piache. → `ach-cr-10`, `hipotetico`; corrobora
  el núcleo de creencia-005 y matiza 002.
- **La Chuvay** (p. 106): la fiesta a los dioses es una danza de disfraces «á
  manera de matachines». → `ach-cr-05`, no se proyecta.
- **El hechizo y la venganza** (p. 106): prenda del ausente + chica en un
  calabacito = «Carrage, Mojan ú Camerico»; toda muerte se achaca al «Moján ó
  hechicero», y de ahí las discordias entre parcialidades. La oruga del
  veneno es *barbarí* (el OCR dice «barban»). → `ach-cr-13`, `lectura` de
  008b.
- **La bebezón mayor** (pp. 107-108) y **la berría** de cazabe (p. 110). La
  forma —todo el pueblo, pintados, sentados por rango, servidos por los
  mozos— es `lectura` de 010c; la bebida es de yuca brava y no se proyecta.
  → `ach-cr-18`, `ach-cr-19`.
- **La agonía** (p. 111): las armas junto al moribundo «para que se defienda
  de la muerte y de la enfermedad»; el soplo y el humo de tabaco; la hija
  mayor o la mujer que lo peina. → `ach-cr-14`, `hipotetico`.
- ⭐ **El llanto que alaba** (pp. 111-112): un pregonero convoca, se llora en
  comunidad y luego uno a uno, «haciendo memoria de su valentía», alabando las
  manos y los pies del muerto, «y así le van refiriendo sus virtudes»; a la
  mujer, «aquellas manos que hacían tan buen cazabe». Es el mismo gesto que
  Oviedo atestigua para el caquetío común (creencia-010): **dos observadores
  independientes de dos pueblos arahuacos.** → `ach-cr-15`, `lectura`
  (corrobora 010).
- **El entierro en la casa con ajuar** (p. 112): armas, hamaca, comida y
  trastes «para que en el camino de la otra vida tengan con qué defenderse».
  → `ach-cr-16`, `lectura` de 008c y corroboración parcial de 009.
- **Catana** (p. 113), el diluvio «con aguacero muy grande», leído como Noé.
  → `ach-cr-20`, no se proyecta.

**El cap. VIII** (girara y airicos) sirve para separar lo achagua de lo
llanero general (`fx-02`): Rivero abre diciendo que «toda la gentilidad de los
Llanos» se parece tanto que lo de unos vale para otros, y que los girara
tienen en sus entierros «los mismos ritos que los Achaguas». El funeral con
ajuar, la yopa y el mohán que sopla son del llano entero; el panteón,
Cuaygerri, los sueños al alba, la Chuvay, la berría y el llanto que alaba los
da como achaguas.

**Fuera del tramo**, buscando la negativa del segundo entierro en todo el OCR,
salieron dos páginas que no son achaguas pero pesan:

- ⭐ **p. 211, los sálivas** (`fx-01`): entierran, y en el «cabo de año»
  desentierran los huesos, los velan días y noches, los queman y beben las
  cenizas, «en lo cual les parece que beben toda la valentía y propiedades del
  difunto». Es la comparanda **regional** más cercana al caquetío que bebe los
  huesos, con su propio porqué. No es hermana (lengua sáliba).
- **p. 198, la carta del Superior de 1665** (`fx-05`): «Mojanes, muchísimos,
  todos Yoperos y supersticiosos; unos reconocían á los cerros por sus dioses,
  otros á los pájaros, otros á las estrellas, muchos al Sol». «Dicho pueblo»
  puede ser **Pauto, de «Cacatíos de nación»** (p. 54), o el Puerto, achagua.
  Si es Pauto, sería la única noticia de la creencia de un grupo caquetío (de
  los Llanos, regla 4). Hay que leer la carta entera para fijarlo.

### 2.2 [[neira-ribero-1762]], preguntado por la creencia

- **El censo.** El script clasifica los lemas de creencia en siete campos y
  marca cada uno doctrina / indígena / dudoso con una regla escrita (no un
  juicio caso a caso); cuenta las voces con `-minari` y mide las páginas sin
  entradas. Todo está en el bloque `censo_neira` de la propuesta.
- **`-minari` no es 'dios-dueño': es 'el que tiene X / el dado a X'.** Lo
  llevan el médico (`Debi minari`), el patrón de la nao, el labrador, el amo
  de casa, el dueño del cielo (`Eriminari`), el idólatra (`Ecunai minarí`), y
  también 'pacífico', 'parlero', 'astuto' o, en una página sin transcribir,
  'dado a mujeres' (`Inaminari`). Un dios de Rivero lo lleva; el ser supremo
  maipure también (`minàri`, «padrone», Gilij p. 6). → `ach-cr-04`,
  `hipotetico`; ruta arahuaca sólo parcial para creencia-015.
- **El que cura cantando y soplando.** `Numariu` 'encantar, curar cantando',
  `Maricai` 'encanto' y 'brujería' («curar con ella = Numariu»), `Camaricacay`
  'brujo'; y en el pliego 92 der., que el YAML no transcribió, «Soplar à los
  enfermos — Numariuni» y «Soplam.to tal — Chabicuri» (= 'ensalmo', 'cura
  tal'). Con el humo de tabaco de Rivero: `ach-cr-06`, **segunda hermana de
  creencia-003**.
- **«Piache» y «mohán» no son achaguas.** El vocabulario no los trae; Gilij
  dice que *Piàce* es 'médico' y viene «dalla lingua Caribe» (p. 9).
  → `ach-cr-07`, `lectura`.
- **El alma dentro y fuera.** «Ánima en el cuerpo — Gabasí. Fuera d[e]l =
  Guabasimi» (35 der.); revivir es que el alma «vuelve a su lugar» (`Guabasi
  esuayua`, con el `esua-` de «Bolver à mi lugar»); desmayarse se dice con
  ella. `Guabasí` es alma, corazón y estómago. → `ach-cr-11`, **segunda
  hermana de 005 y 006** en su núcleo, con la reserva del calco («volver en
  sí»).
- **El muerto que anda.** Duende = `Guabaimi` (el alma con el `-mi` de lo que
  ya fue); «Blanco Español — Guabaymi... Así llaman los Duendes»; «Ojos p.a
  ver almas = Guabaimi tuibabare». → `ach-cr-12`, **segunda hermana de 008**.
- **Las honras son un convite.** «Honras de Dif.to — Tanasí / ofrenda tal =
  Yrrubaydacasí» (68 izq.), y `Tanasí` es también 'boda, convite'; aparte,
  «Ofrenda de difuntos = Jrrubaidacasi» (78 der.), que puede ser lema de
  doctrina. → `ach-cr-17`, `hipotetico`; ruta arahuaca para 016 todavía
  insuficiente.
- **El cielo.** `Eno` es el trueno (y un dios del pliego 56); las Cabrillas,
  el Camino de Santiago, el Carro, el Crucero, los dos luceros y el cometa
  tienen voz; entre las diosas hay una madre del lucero de la tarde y una
  estrella. → `ach-cr-21`, `ach-cr-22`.
- **El sueño en el vocabulario**: «Soñar — Masiu numaca», «Sueño — Dasuisi»,
  «Soñar, tener pesadillas — Carrunata numayu» (con la raíz de 'miedo'), en el
  mismo pliego 92 der. sin transcribir.

### 2.3 [[gilij-1780-1783]], t. III libro I (los maipures)

- **Purrùnaminàri**, ser supremo, que hizo al hombre y no tiene culto
  (pp. 6-7, 23, 29). La etimología «il padrone del tutto» es de Gilij, no de
  los maipures, que «non dispiaceva loro la mia interpetrazione». La costilla
  y la luz antes que el sol (p. 23) el propio Gilij las da por Génesis.
  → `mai-cr-01`, `hipotetico` con `ach-cr-02`.
- **Tapanimarru**, «immortale... bellissima, e vergine», madre de Sìsiri
  (p. 7): huella doctrinal, no se proyecta; pero su nombre se parece a la diosa
  achagua `tabaminarro` y entra en la lectura del panteón. → `mai-cr-02`.
- **El más allá con premio y castigo** (p. 13; «la casa del Demonio Vasùri»,
  p. 33): contradice el «sin premio ni castigo» de creencia-009, con sospecha
  de eco doctrinal. → `mai-cr-03`.
- **El demonio son los muertos violentos** (pp. 14-15): `Vasùri` (no
  «Vasìtri») es el alma de quien murió en guerra o en pleito; la del que muere
  de muerte natural es `amitàminè`. → `mai-cr-04`, matiza 008.
- **Las estrellas fueron gente** (pp. 17-18). → `mai-cr-05`.
- **El cielo es `Eno`**, «la qual voce significa similmente il tuono, e lo
  schioppo» (p. 21; «Cielo — Eno», p. 159). → con `ach-cr-21`.
- **Sin templos ni ritos** (p. 10). → con `ach-cr-01`.
- **Queti es 'animal'** (p. 159), no un ser: la pregunta del plan se cierra.
- Y en las notas (p. 402), los **otomacos** lloran a sus muertos antes del
  alba recitando que les traían pescado y tortugas (`fx-03`): tercer pueblo de
  la región con el llanto que recita.

## 3. El panteón del pliego 56, con las dos imágenes

Vistos hoy el pliego 56 izq. de la copia de 1788 y la p. 113 de Rivero.

- **La copia**: «Dioses de los Achaguas = Jurruna minari. El de las Labranzas
  = Varaca. El de las riquezas = Cuisiaberri. El del fuego [=] Prubisana. El
  causador de temblores = Apichabirri. Flechero = tarrari. De las tempestades
  = Eno. De los truenos [=] Achacato. Dios tonto = Amaribaca Vreca, capurraye
  Dios signo del cielo.» (Los «=» tras «fuego» y «truenos» caen en el lomo.)
- **Rivero**: «Jurrana-minari, al de las labranzas; Baraca, al de las
  riquezas; Cuisiabirri, al del fuego; Pruvisana, al causador de los
  temblores; Achacató, dios tonto».
- **Se confirma el corrimiento de un escalón**: corriendo los nombres de la
  copia uno a la izquierda casan los cinco pares de Rivero, y `Eno` cae en
  «los truenos», que es lo que dice el vocabulario (87 der., 96 izq.).
  Argumento nuevo: la copia se lee como la frase de Rivero, «Nombre, glosa;
  Nombre, glosa», con los «=» puestos al estilo del vocabulario («glosa =
  voz»); el último ítem, sin «=», conserva el orden nombre-glosa. Indicio
  débil: «Riqueza = Guarrua» (89 der.).
- **La grafía**: la imagen dice `Prubisana`, no el `Purubisana` del YAML.
- **Lo abierto**: el par `Jurruna minari` / `tabaminarro` (masc. / fem.) se
  explica con y sin corrimiento. Y las **diosas** no se deciden: a favor de
  correrlas, `tabaminarro` ≈ `Tapanimarru`, la madre maipure (daría
  «tabaminarro, criadora de los Achaguas»); en contra, `Jarrutua` lleva `-tua`
  'madre' y casa sin correr con «madre del lucero de la tarde». Lo robusto:
  entre las diosas hay una madre del lucero vespertino y una estrella.
- ¿`Jurruna/Jurrana-minari` = `Purrùnaminàri`? Sigue siendo pregunta: Rivero
  lo hace dios de las labranzas y Gilij ser supremo, y `purrùna` 'todo' es
  conjetura de Gilij (en Neira 'todo' es `Maqueni`, y `purruna-` es
  'anegar').

El detalle, en la sección `panteon_neira_56` de la propuesta. El YAML de Neira
no se corrige aquí: genera `lexicon_achagua.py`, que importa el motor.

## 4. Lo que no está (y qué se leyó para decirlo)

- **Segundo entierro achagua**: ninguno en los caps. VI-VIII, ni en las
  páginas del OCR entero con *huesos*, *calavera*, *difunt* o *entierr*. El
  único del libro es el sáliva (p. 211).
- **Beber los huesos**: sólo el sáliva.
- **Tierra de los muertos con nombre**: ni en Rivero (sólo «el camino de la
  otra vida») ni en Neira. El maipure tiene lugares de premio y castigo sin
  topónimo.
- **La exhumadora y sus tabúes; huesos y lluvia**: nada en las tres obras.
- **Dueño de un lugar que veda**: nada achagua; sólo el indicio sin fijar de
  1665 (cerros tenidos por dioses).
- **Las mujeres excluidas de la Chuvay «lest they die»** (HSAI p. 410): no
  está en Rivero pp. 102-118 ni sale en Gumilla por búsqueda; tampoco
  «Tanasuri», el Pruvisana que carga la tierra ni el culto a las lagunas. Sin
  fuente localizada.
- **El mar**: nada, como ya midió [[cosmovision_marina_2026-09-24]].

## 5. Correcciones para quien integre (no se editaron)

1. **Plan 08**: «Cuoygerri» es del OCR (la imagen dice *Cuaygerri*); las
   páginas de Gilij eran el marcador del OCR: Purrùnaminàri pp. 6-7 (no 8-9),
   la costilla p. 23 (no 25), Queti y el demonio p. 159 (no 155); el demonio es
   `Vasùri`, no «Vasìtri»; Tapanimarru está en la p. 7.
2. **El PDF de Gilij t. III salta las pp. 30-31** (pdf 50 = p. 29, pdf 51 =
   p. 32): el desfase pasa de − 21 a − 19 ahí. El marcador «impresa» del OCR
   lleva − 19 en todo el tomo, y por eso el plan citaba dos páginas de más.
3. **El YAML de Neira** (`6-fusion/achagua_neira_ribero_1762.yaml`):
   `Purubisana` → `Prubisana` (56 izq.); «Guabauimi» (62 izq.) parece
   `Guabaimi`; y **siete páginas sin transcribir** (32 der., 40 izq., 41 der.,
   52 izq., 72 izq., 79 der., 92 der.), medidas por lado en
   `censo_neira.lados_sin_entradas` y vistas en imagen: todas tienen entradas.
   El ensamblador mide huecos por pliego y no las ve. Por eso la ficha de
   Neira y el plan 08 §1.1 («no queda ninguna página por leer en imagen») no
   son exactos. Las líneas de creencia de 52 izq. y 92 der. se leyeron hoy y
   están en la propuesta; el resto de esas páginas sigue sin transcribir.
4. **Notas que dicen que Gilij no tiene capa de texto** (el t. III tiene OCR
   desde el 2026-09-23 y su libro I queda minado aquí):
   - `3-mundo/ensayos/03_creencia_caquetia.md`, línea 20 (la cabecera, justo
     tras el frontmatter: «Sin minar · gilij-1780-1783 (sin capa de texto)»);
   - `3-mundo/mapa-creencia.md`, líneas 61 y 76;
   - `3-mundo/mapa-transmision.md`, línea 62 (no estaba en la lista del
     encargo);
   - `4-fuentes/INDICE_FUENTES.md`, línea 104 (la fila de Gilij);
   - `4-fuentes/sesiones/03_creencia.md`, líneas 169 y 177.
5. **Las fichas**: a las tres se les añadió la sección «Minado para creencia
   (2026-10-09)» en el cuerpo, sin tocar el frontmatter. Al integrar,
   `cobertura`, `minado` y `verificado` de [[rivero-1883]],
   [[neira-ribero-1762]] y [[gilij-1780-1783]] deberían decirlo, y después
   regenerarse la bibliografía.

## 6. Qué quedó por leer

- **Gilij t. II** (*Costumi*: piaches, curación, funerales, el «ballo
  Queti»): no está en el repo; descargarlo lo decide Miguel.
- **Gilij t. III pp. 30-31**, que faltan en el escaneo del repo.
- **Gilij t. III, notas pp. 401-410**: vistas sólo la 401 y la 402.
- **Rivero, la carta de 1665 entera** (pp. 197-201), para fijar quién era
  «dicho pueblo» (`fx-05`). Y los pasajes de creencia de otras naciones que
  no se leyeron: los tunebos y tame de la p. 56 (sólo OCR).
- **Neira**: las siete páginas sin transcribir (salvo las líneas de creencia
  de dos); y en imagen, las voces que la propuesta da como «transcripción»
  (astronomía, 32 izq., 67 izq. y der., 87-88 der., 96 izq.).
- **El cotejo con el kalinago** (las estrellas que dan viento, de
  `cosmovision_marina`), que podría ser la segunda tradición de `ach-cr-22`.
- **Paz Reverol 2017** (no está en el repo): ver si el wayuu cuenta los
  sueños al amanecer; sería la segunda tradición de `ach-cr-10`.
- **Gumilla**, los capítulos de religión (la minería E del plan), y la
  fuente de las afirmaciones de HSAI sobre la Chuvay.

## 7. Lo que queda para Miguel

1. **¿Achagua y maipure son una tradición o dos** para la opción C? Gilij dice
   dialecto. Con dos, `ach-cr-02` (creador sin culto), `ach-cr-04` (los
   «dueños») y `ach-cr-22` (las estrellas) podrían subir a `reconstruido`.
2. **El corrimiento del panteón**: aplicarlo al YAML de Neira (y regenerar
   `lexicon_achagua.py`) o dejarlo anotado.
3. **La carta de 1665**: si «dicho pueblo» resulta ser Pauto, es la primera
   noticia de la creencia de un grupo caquetío (de los Llanos) y pide su
   propia decisión de capa y de polity.
4. **El sáliva** que bebe las cenizas: si el ensayo lo usa como comparanda
   regional del rito del díao, junto a (o en lugar de) la teoría wayuu de
   010d.

## Auditoría de la Vía A

Lo que hacen el achagua (Rivero, Neira) y el maipure (Gilij) con cada hecho
del canon reconstruido desde el wayuu. `creencia.yaml` no se editó. Lo que
sólo tiene apoyo wayuu y el achagua no confirma queda **señalado para
revisión, no degradado**.

- **creencia-002** (el piache trabaja el sueño) — **no toca; matiza.** El
  sueño achagua no es del especialista: «esto en cada caney ó casa, empezando
  el primero de todos su Cacique ó Capitán» (Rivero p. 105). Ningún
  diagnóstico por el sueño. Sigue con una sola tradición.
- **creencia-003** (tabaco, licor, cantos, urari) — **corrobora en parte.**
  Tabaco y canto: «Encantar, curar cantando — Numariu» (Neira 61 izq.),
  «Soplar à los enfermos — Numariuni» (92 der.), el piache que inciensa «con
  ciertos ensalmos» (Rivero p. 105). Licor, urari y espíritu-serpiente, no; y
  «piache-mohán» es voz regional (Gilij p. 9: *Piàce*, «dalla lingua
  Caribe»).
- **creencia-005** (soñar no es dormir; el alma sale) — **corrobora el
  núcleo.** «Anima en el Cuerpo — Gabasí. fuera d[e]l = Guabasimi» (Neira
  35 der.), y lo soñado se cuenta en público cada mañana (Rivero p. 105). El
  viaje nocturno del alma en el sueño no aparece.
- **creencia-006** (enfermedad = alma que se aleja) — **corrobora con
  reservas.** «Revivir — Guabasi esuayua», el alma que vuelve a su lugar
  (Neira 89 der.; «Bolver à mi lugar — Nuesuayua», 42 der.). Que la
  enfermedad sea eso, no; y el moribundo se defiende de la muerte «con el
  arco, las flechas y la macana» (Rivero p. 111).
- **creencia-007** (males comunes y del espíritu; lo igual cura lo igual) —
  **no toca.** Nada en lo leído.
- **creencia-008** (los muertos recientes, peligrosos; los antiguos,
  protectores) — **corrobora; matiza.** «Duende — Guabaimi» y «Blanco Español
  — Guabaymi... Así llaman los Duendes» (Neira 57 y 42 izq.); en el maipure,
  el demonio son «l'anime... di persone uccise in guerra, o in private
  contese» (Gilij p. 15): el peligro lo da la muerte violenta, no la
  reciente. Nada de antiguos que protegen.
- **creencia-009** (tierra de los muertos con nombre; sin premio ni castigo)
  — **corrobora en parte; contradice en parte.** Hay camino y la vida sigue
  con las mismas cosas: «para que en el camino de la otra vida tengan con qué
  defenderse» (Rivero p. 112). Sin topónimo. El maipure tiene premio y
  castigo, «a’ cattivi un pozzo, in cui ardevi perpetuamente il fuoco» (Gilij
  p. 13), probablemente con eco doctrinal.
- **creencia-010d** (el wayuu explica por qué se beben o redepositan los
  huesos) — **no toca.** Ni achaguas ni maipures exhuman. El vecino que sí
  bebe los huesos es sáliva, y lo explica de otro modo: «les parece que beben
  toda la valentía y propiedades del difunto» (Rivero p. 211). 010d queda sin
  hermana arahuaca.
- **creencia-011** (la exhumadora y sus tabúes) — **no toca.** Nada en las
  tres obras.
- **creencia-012** (huesos o cenizas y lluvia) — **no toca.** Nada achagua ni
  maipure; la lluvia como «el vino de los dioses» derramado es de girara y
  airicos (Rivero p. 116).

## Enlaces

[[08_creencia_achagua_que-minar]] · [[creencia_achagua_2026-10-09]] ·
[[03_creencia_caquetia]] · [[mapa-creencia]] · [[03_creencia]] ·
[[rivero-1883]] · [[neira-ribero-1762]] · [[gilij-1780-1783]] ·
[[gumilla-1791]] · [[steward-1948-hsai-4]] · [[oviedo-y-valdes-1851]] ·
[[arcaya-1920]] · [[paz-reverol-2017-2018]] · [[perrin-1992-1995]] ·
[[maria-lionza-culto]] · [[metodo-comparativo]] · [[polities-caquetias]] ·
[[cosmovision_marina_2026-09-24]] · [[INDICE_FUENTES]]
