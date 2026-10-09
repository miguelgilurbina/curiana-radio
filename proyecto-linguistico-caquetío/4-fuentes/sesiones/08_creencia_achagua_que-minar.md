---
tipo: decision-mineria
corpus: [creencia.yaml]
fecha: 2026-10-08
pueblo: achagua
pregunta: "¿Qué hay que minar de los achaguas, y en qué orden, para que el ensayo «¿En qué creía el caquetío?» sume una tercera vía: la hermana arahuaca de los Llanos?"
ensayo: 03_creencia_caquetia
moc: mapa-creencia
estado: "propuesta: no se ha minado nada; el orden y las capas los decide Miguel"
---

# Creencia achagua: qué minar antes de minar

> [[03_creencia_caquetia|ensayo]] · [[mapa-creencia]] · [[03_creencia|hoja de fuentes de la sesión 3]] · [[INDICE_FUENTES]]
> En juego: [[rivero-1883]] · [[neira-ribero-1762]] · [[gilij-1780-1783]] · [[gumilla-1791]] · [[steward-1948-hsai-4]] · [[fabo-1911]]
> Método: [[metodo-comparativo]] · skills `minar-fuente` y `leer-fuente`

Nota de decisión, no minería. No se descargó nada y no se tocó ni el corpus,
ni el lexicón, ni las fichas, ni el ensayo. Lo que aquí se cita de una página
se leyó hoy en el OCR del repo, que es **pista**, salvo donde dice **«visto en
imagen»**. Las cifras de la obra (cuántos lemas, cuántas voces) no se dan:
las mide un script cuando se mine (regla 1).

## 0. En una línea

El ensayo reconstruye la creencia caquetía desde el wayuu (Vía A) y desde el
culto de María Lionza (Vía B). El achagua puede ser una **tercera vía: la
hermana arahuaca con etnografía colonial de la creencia**. Y lo mejor de esa vía
**ya está en el repo sin minar**: Rivero 1883, libro II, caps. VI-VIII. Para
empezar no hay que descargar nada.

---

## 1. Lo que el vault ya tiene

### 1.1 [[neira-ribero-1762]]: leído entero, pero sólo se le preguntó por la lengua

- **Estado.** El vocabulario (pliegos 28-98) y el arte están leídos por visión,
  y la transcripción vive en `6-fusion/achagua_neira_ribero_1762.yaml`
  (propuesta). **No queda ninguna página por leer en imagen.** Queda
  preguntarle a lo transcrito por la creencia y ver en imagen lo que se vaya a
  citar. Las imágenes están sólo en OneDrive
  (`fuentes_caquetios/neira_ribero_1762/NNN.jpg`, fuera de git).
- **Nunca se le preguntó por la creencia.** El panteón y la astronomía
  salieron «sin buscarlos» (ficha, primera pasada). Una consulta de hoy por lema
  castellano en el YAML da, entre otras, estas voces de creencia. Son
  transcripción por visión: hay que verificarlas antes de citarlas.

| Campo | Lema → voz achagua (pliego) |
|---|---|
| dioses y dueños | «Dioses de los Achaguas» y «Diosas»: el panteón, 56 izq. (ver §1.6) · «Dueño del cielo» = `minari, Eriminari` (57 izq.) · «Médico» = `Debi minari` (74 der.) · «Patrón de la Nao» = `Jda minari` |
| creador | «Criador» = `Yquenuederrí, Ymanuderrí` (51 izq.) · «Criar de nada», «Ser Dios», «Dar el alma», «Confiar en Dios»: **lemas de doctrina** |
| seres | «Demonio, Diablo» = `tanasimi` (53 izq.; = Gumilla t. II p. 24) · «Duende» = `Guabaimi` (57 izq.), la misma voz que «Blanco Español» (42 izq.) |
| persona | «Alma» = `Guabasí` (34 izq.), que en el pliego 62 es también 'estómago' · «Espíritu, aliento» = `Careran` (62 izq.) · «Sombra» = `tanari, Nutana` (92 izq.) |
| especialista | «Brujo» = `Camaricacay` (43 der.) · «Encantador» = `Camaricacayi` · «Encantar, curar cantando» = `Numariu` (61 izq.) · «Hechizar (dicen cocinarle)» = `Nuchanaum` (67 izq.) · «Agüero voluntario» / «fortuito» = `Cayubacaybe` / `Emimay` (32 izq.) |
| muerte | «Difunto» = `Mucuiarimi`, «Cadáver» = `Masicasimi` (56 izq.) · «Muerto» = `Mucurrí`, «Muerte» = `Barinacaren` (76 der.) · «Antepasado» = `Bainacusamí` (36 izq.) · **«Ofrenda de difuntos» = `Jrrubaidacasi`** (78 der.) · «Sepultura» = `Nirrí` (91 der.) · «Desenterrar» = `Numichedau` (54 der.) |
| ayuno y fiesta | «Abstinencia, ayuno» = `Dacãiba` (29 der.) y un «Ayuno tal» aparte (33 izq.) · «Borrachera» = `Camaybacay` (43 izq.) · «Mudanza, baile» = `Ybabedacasí` (76 der.) · «Flauta» = `Jba` (64 izq.) |
| cielo | «Cielo» = `Erri` (48 izq.) · Pléyades = `Jbinai` (44 der.) · Vía Láctea = `Besibami` (45 der.) · luceros de la tarde y de la mañana con nombres distintos (73 izq.) · cometa (49 izq.) · eclipse de luna (57 der.) · trueno = `Eno` (87 der.) · diluvio = `Catana` (56 izq.) |

Lo que esa tabla ya sugiere, sin minar todavía:

- **Los dioses achaguas son «dueños».** `-minari` es 'dueño' en lemas que no
  tienen nada de religiosos (el patrón de la nao, el médico). Es la misma
  categoría que el canon caquetío reconstruye para los «espíritus dueños»
  (`creencia-015`, `-021`), y que hoy sostienen el wayuu y María Lionza.
- **El brujo es el que cura cantando.** `Camaricacay` sale de la misma raíz que
  «encantar, curar cantando».
- **Hay una ofrenda a los difuntos con nombre propio.** Es la pieza que a
  `creencia-016` (alimentar a los muertos) le falta, porque hoy sólo la sostiene
  María Lionza, como `retro-abstraido`.
- **Hipótesis para el arte, no dato:** `tanasimi` 'demonio' podría ser
  `tana-` 'sombra' (`tanari`) + `-si` absoluto + `-mi` caducidad («lo que
  fue»), el sufijo de `Mucuiarimi` 'difunto' y de `Bainacusamí` 'antepasado'.
  Si se sostuviera, el «demonio» de los jesuitas sería **la sombra del muerto**,
  el *yoluja* de la Vía A. Eso lo decide la morfología del arte, no el parecido.

### 1.2 [[rivero-1883]]: en el repo, y su etnografía de la creencia sin minar

PDF de imagen más el OCR de archive.org en `fuentes_caquetios/`. La ficha dice
lo que falta: «la etnografía achagua (pp. 102-118) por esferas». La campaña de
cosmovisión marina sólo sacó tres cosas de ahí: la *chaca* (p. 105, vista en
imagen), los agoreros de la pesca (p. 104) y el diluvio *Catana* (p. 113). Lo
demás está intacto, y es justo lo que el ensayo necesita:

| Capítulo (libro II) | pp. (pdf) | Qué trae (leído hoy en el OCR) |
|---|---|---|
| VI. Ritos, costumbres, usanzas y supersticiones de la nación achagua | 102-106 (123-127) | «No adoran ídolos los Achaguas»; agoreros por el canto de los pájaros, por el encuentro de animales y por el primer pez flechado; **la yopa**, que se toma en grupo y adivina según la ventana de la nariz por la que mana; la *chaca* con el piache, que bendice el pescado con humo de tabaco; **el relato de los sueños al alba, en cada caney, empezando por el cacique, «en tono de lamentación»**; la fiesta de máscaras *Chuvay*; el hechizo a distancia con pelo o saliva (*carrage*, *mojan* o *camerico*); y la muerte atribuida siempre al «mojan», que acaba en venganza entre parcialidades |
| VII. Mantenimientos y bebidas; ritos de los entierros | 107-113 (128-134) | La **bebezón solemne**, «el mayor [día] del año», con flautillas, en la que todo el pueblo bebe *berría*, la chicha de cazabe (`berri`). **El funeral**: un pregonero convoca; el llanto es colectivo, alabando las virtudes del muerto «de cuerpo presente» durante tres o cuatro días; se le entierra en la casa con sus armas, la hamaca, comida y abalorios «para el camino de la otra vida». **Un creador, *Cuaygerri*, «el que todo lo sabe»**, que se enseña a los hijos. Los dioses menores, con su dominio (p. 113, **visto en imagen**: «*Jurrana-minari*, al de las labranzas; *Baraca*, al de las riquezas; *Cuisiabirri*, al del fuego; *Pruvisana*, al causador de los temblores; *Achacató*, dios tonto»). Y *Catana* |
| VIII. Abusos, costumbres y supersticiones de la nación Girara y los Airicos | 113-118 (134-139) | Los vecinos del llano. Rivero abre el capítulo diciendo que «toda la gentilidad de los Llanos y del río Orinoco es tan parecida» que lo de unos vale para otros. Es comparanda de la comparanda: se mina sólo para separar lo achagua de lo llanero general |

⭐ Hay un paralelo que reordena el ensayo y que hoy nadie ha escrito. El llanto
achagua que va «refiriendo [las] virtudes» del muerto (p. 112) es el mismo
gesto que Oviedo atestigua para el caquetío común: lo lloran «cantando, y
diciendo en aquel cantar lo que hizo mientras vivió» (`creencia-010`). Lo mismo
pasa con el ajuar «para el camino» (Rivero p. 112) y los enseres «para que no le
falte nada en la otra vida» (Arcaya p. 117, `creencia-008c`). **Son dos
observadores independientes de dos pueblos arahuacos.** Esto se puede
corroborar, que es lo que más vale (`minar-fuente` §8).

### 1.3 [[gilij-1780-1783]]: el tomo de la religión tiene OCR desde el 2026-09-23

- En el repo están los tt. I, III y IV. **Falta el t. II** (*De' costumi degli
  Orinochesi*).
- **El t. III tiene OCR** (`Gilij_1782_Saggio_Storia_Americana_vol3.ocr.txt`,
  sobre la imagen incrustada; es pista). Su libro I es **«della religione degli
  Orinochesi»**, y las creencias propiamente dichas ocupan más o menos las
  pp. 1-40 (pdf ~20-60). El resto del libro I trata de la misión.
- **Purrúnaminári** es **maipure, no achagua**: es el Ser supremo, «tanto
  universale» en el alto Orinoco como Amalivacá en el bajo. Gilij lo descompone
  como *purrúna* 'todo' + *minári* 'dueño': «il padrone del tutto» (t. III
  pp. 8-9). Le atribuye un hijo nacido de una virgen inmortal, y un relato en el
  que saca una costilla al hombre dormido para hacer a la mujer, que **el propio
  Gilij** dice que está «parola per parola nel Genesi» (p. 25). El índice del
  tomo trae además **«Tapanimarru, chi sia? 6»**, y Neira tiene «Diosas =
  `tabaminarro`» (56 izq.).
- **Para Gilij el achagua es «un dialetto del Maipùre»** (t. III p. 205; ficha).
  Por eso la religión maipure es la comparanda más cercana después de la
  achagua.
- **Lo que hay que corregir en el vault**, sin tocarlo ahora: `mapa-creencia`,
  la fila de Gilij en [[INDICE_FUENTES]], la hoja de la sesión 3 y el
  frontmatter del ensayo dicen todavía que Gilij está «sin capa de texto».
  **Para el t. III ya no es verdad.**

### 1.4 [[gumilla-1791]]: en el repo, con poco achagua de creencia

Ya está minado para la costa, las voces y las lenguas. Su religión es
**multinacional**, y lo achagua aparece suelto:

- `Tanasimi` como nombre achagua del demonio, en una lista de demonios por
  nación (t. II cap. III, pp. 23-24).
- El mito de origen de los troncos y los ríos (*Univerrenais*, t. I p. 114, ya
  minado).
- La tumba de los capitanes achaguas, con la tapa de barro que se resana cada
  mañana (t. I p. 200).
- *Catena Manóa* (t. II pp. 6-7, ya minado).

Los capítulos de difuntos (t. I caps. XIII-XIV) traen **segundos entierros de
otras naciones**, como los guaraúnos y los caribes, y los de curación
(cap. XV), los eclipses (t. II cap. XXIII) y la idolatría (t. II cap. III) son
generales.

**El «antecedente de 1741»** de [[metodo-comparativo]] es Gumilla t. II p. 32,
verificado en imagen el 2026-09-24. Es una regla de método: «los pronombres
dicen la filiación, el léxico puede ser comercio». No es dato de creencia.

### 1.5 [[steward-1948-hsai-4]]: la síntesis en inglés ya está en el repo

Hernández de Alba, «The Achagua and their neighbors», pp. 399-412 (pdf
523-536), con capa de texto. Tiene secciones *Religion* (p. 410), *Shamanism
and magic* (p. 411) y *Mythology* (p. 412). **Es secundaria**: resume a Rivero,
Gumilla y Karsten (la cadena Rivero → Hernández de Alba no es una segunda
atestación). Sirve como mapa y trae dos lecturas que hay que cotejar:

- Lee **«*Gurrana* minari»**.
- Afirma que **las mujeres quedaban excluidas de las danzas de máscaras «lest
  they die»**. En las pp. 104-106 de Rivero eso no sale: hay que localizarlo.

### 1.6 ⚠️ El panteón de Neira está corrido un escalón respecto de Rivero (visto en imagen)

El pliego 56 izq. de la copia de 1788, **visto en imagen hoy**, dice lo mismo
que transcribió el escriba:

> «Dioses de los Achaguas = Jurruna minari. El de las Labranzas = Varaca. El de
> las riquezas = Cuisiaberri. El del fuego = Prubisana. El causador de temblores
> = Apichabirri. Flechero = tarrari. De las tempestades = Eno. De los truenos =
> Achacato. Dios tonto = Amaribaca Vreca, capurraye Dios signo del cielo.»

Rivero p. 113 (**visto en imagen**) empareja otra cosa: *Jurrana-minari* con
las labranzas, *Baraca* con las riquezas, *Cuisiabirri* con el fuego,
*Pruvisana* con los temblores y *Achacató* con el dios tonto. Si se corren los
nombres de Neira **un escalón a la izquierda**:

- casan los cinco pares de Rivero;
- y además **`Eno` cae en «De los truenos»**, que es lo que dice el propio
  vocabulario («Rayo, el trueno = Eno», 87 der.).

Sin correrlos no casa ninguno. Es la trampa de Jahn con agua/río (`leer-fuente`
§1: tabla desplazada que «sigue pareciendo válida»), pero esta vez dentro del
manuscrito.

Hay un indicio débil más: «Rico = `Cabarruanicayi`» (`barru`) apoya que
*Baraca* sea el de las riquezas.

**Consecuencias:**

- *Jurruna minari* no sería «dioses de los achaguas» en general, sino **el
  dueño de las labranzas**.
- El YAML lleva `Purubisana` donde la imagen dice, al parecer, `Prubisana`
  (Rivero imprime *Pruvisana*). Hay que verlo a 2-3×.
- Neira y Rivero **no son testigos independientes**: Juan Ribero es el mismo
  Juan Rivero. Lo que decide entre los dos es el vocabulario, no la mayoría.

Que *Jurruna/Jurrana-minari* (achagua) sea el *Purrúnaminári* maipure de Gilij
es una **pregunta, no un hallazgo**. Hay tres lecturas del nombre (J-, G-, P-) y
dos glosas (labranzas / dueño del todo), y en el propio vocabulario
`purruna-` es 'anegar' («Anegar = Nupurrunaidau», 35 der.).

### 1.7 El corpus y lo demás

- **`creencia.yaml` no tiene ni un hecho achagua.** Lo achagua del corpus está
  en parentesco (`parentesco-021`, `-022` y `-040`: los Tamudes, *mude*, los
  linajes con nombre de animal) y en geografía política (los caquetíos de los
  Llanos, con cuatro testigos). La comparanda achagua de la creencia que existe
  es la del mar, que está en `6-fusion/cosmovision_marina_2026-09-24.yaml`
  §comparanda.achagua y **no** en el corpus.
- **PDFs:** Rivero, Gumilla (2 tt.), Gilij (tt. I, III y IV), Fabo, Jahn y HSAI
  4 están en `fuentes_caquetios/`. Neira y Ribero está sólo en OneDrive.
- **Una trampa ya identificada:** en la web circula como mito «achagua» el del
  dios **Purú** y su hija, que mata a la serpiente. Gumilla lo da para los
  **sálivas** (vía HSAI p. 411). No es achagua.

---

## 2. Qué pregunta responde lo achagua, y por qué vale como comparanda

### 2.1 Por qué es legítima

1. **Por filiación.** Es arahuaco maipure (Gilij t. III p. 205). Loukotka 1968,
   vía Fabre, pone al caquetío en la misma rama que el achagua y el piapoco
   (rastreo del 2026-08-14). Y el núcleo del lexicón ya usa el achagua (`waya`,
   `naya`, `-ba`; D11, tanda de las hermanas).
2. **Por historia.** Hubo caquetíos en los Llanos y vecindad
   caquetío-achagua documentada (Pauto, los Tamudes y la «Nación Cacatia», en
   Rivero y Gumilla; `geografia_politica`; [[polities-caquetias]]). El modelo de
   Oliver hace pasar al caquetío ancestral por los Llanos del norte
   (`geografia_politica-012`, hipotético).
3. **Por documentación.** Es la **única hermana arahuaca de tierra firme del
   norte con una etnografía de la creencia anterior al s. XIX**. El wayuu de la
   Vía A es etnografía del s. XX.

**Lo que no autoriza.** El cruce del 2026-09-13 (ficha de Neira) midió que el
caquetío atestiguado **no** se parece más al achagua que al lokono o al wayuu.
El achagua es una hermana, no la madre. Vale lo que valga cada rasgo, contado
como **una hermana más**.

### 2.2 Las preguntas concretas

| Pregunta del ensayo | Qué hay hoy en el canon | Qué puede dar el achagua | Dónde |
|---|---|---|---|
| **El cosmos y los dioses**: ¿había seres con dominio, y es el «señor de las tormentas» de Manaure un título de ese tipo? | Manaure y las tormentas (`creencia-013`, atestiguado); los dueños, `retro-abstraido` (`-015`) | Dioses-«dueños» (`-minari`) con dominios, entre ellos **la tempestad y el trueno** (`Eno`); un creador, *Cuaygerri*; diosas, y la madre del lucero de la tarde; astronomía con nombres | Rivero pp. 112-113; Neira 56-57, 44-45, 73, 87; Gilij t. III pp. 6-9 |
| **Los chamanes**: ¿qué hace el especialista y con qué? | `boratio`, el díao, el ayuno (atestiguados); el tabaco y el sueño, `reconstruido` **sólo desde el wayuu** (`-002`, `-003`, `-005`) | El piache que inciensa con tabaco; el brujo «que cura cantando»; la adivinación con yopa; los agoreros; el hechizo a distancia; **el sueño contado al alba por el cacique** | Rivero pp. 104-106; Neira 43, 61, 67, 32 |
| **El culto a los muertos**: ¿cómo se llora, dónde se entierra, se alimenta al muerto, hay segundo tiempo? | Funerales del común y del díao (atestiguados, Oviedo/Arcaya); la ofrenda, `retro-abstraido` (`-016`); hueso → lluvia, `reconstruido` (`-012`) | El llanto que canta las virtudes; el ajuar para el camino; la ofrenda de difuntos con nombre; el entierro en la casa; la tumba del capitán que se resana | Rivero pp. 111-112; Gumilla t. I p. 200; Neira 78, 56, 91, 54 |
| **Las fiestas**: ¿qué fiesta reúne a todos, y con qué? | El llamamiento para «beber los huesos del díao» con vino de maíz (atestiguado) | La bebezón solemne, «el mayor día del año»; la *Chuvay* de máscaras; la *chaca* | Rivero pp. 106-110 |

### 2.3 Qué se puede proyectar y qué no

**El criterio.** Se proyecta **la forma**: quién hace qué, en qué orden y con
qué estructura. Lo que el **medio** decide no se proyecta. Los Llanos son
sabana, ríos, várzea, yuca brava y pesca de río; la Kaketiana es costa seca,
cardonal, mar y sal.

| Se puede proyectar (con capa, §2.4) | No se proyecta |
|---|---|
| El llanto que canta lo que el muerto hizo; el ajuar para el viaje (ya atestiguados para el caquetío: el achagua **corrobora**) | La *chaca* y la adivinación por el primer pez flechado, que son de **río** (la campaña marina ya lo midió: no hay rito del mar achagua) |
| No hay ídolos ni templo, y los seres se invocan por especialistas (corrobora `creencia-008c`) | El culto a las lagunas y el diluvio como «laguna general» (*Catena Manóa*), que son agua dulce de llanura |
| La muerte atribuida a hechizo y la venganza que sigue (corrobora `-008b`) | La *berría*, chicha de **cazabe**. La bebida caquetía atestiguada es el **vino de maíz** (Oviedo) |
| Los seres como «dueños» de un dominio (segunda hermana para `-015`) | La *Chuvay* de máscaras y la exclusión de las mujeres, si se confirma: es un complejo del Orinoco y de la Amazonía noroeste sin rastro costero |
| La ofrenda a los difuntos (segunda hermana para `-016`) | Los **nombres** de los dioses. Igual que con Pulowi o Juyá, no se caquetizan por decreto: si la simulación funciona, un agente acuñará |
| El sueño como asunto público, contado al alba (segunda hermana para `-002`/`-005`) | El segundo entierro y el beber los huesos. **El achagua no lo registra** en lo leído hasta hoy: el rito del díao se queda como caquetío, con paralelos warao, caribe y wayuu (Gumilla t. I cap. XIV; Vía A) |

### 2.4 Cómo leer a dos misioneros del XVIII, y qué capa da

**El precontacto no es la colonia** ([[polities-caquetias]]; la regla 3 de
`CLAUDE.md`). Rivero escribe hacia 1736 y Gumilla en 1741. Neira se trasuntó en
1762. Los achaguas que describen viven en reducción jesuita (Rivero narra esas
fundaciones del s. XVII) y bajo las armadas caribes que suben a cautivar
(Gumilla t. II cap. IX). Gilij anota que los viejos, «che fan le veci de'
libri», ya habían muerto. Hay que pasar tres filtros por pasaje:

1. **La huella doctrinal.** Cada misionero busca al «verdadero Dios». Rivero
   dice de *Cuaygerri* que «bajo este nombre conocen a su modo al verdadero
   Dios», y en *Catana* lee a Noé. En Gilij, Purrúnaminári hace a la mujer de
   una costilla. En Neira hay lemas **pedidos para la doctrina** («Criar de
   nada», «Ser Dios», «Dar el alma»). Lo que lleve esa huella no se proyecta.
2. **El marco del demonio.** Para el jesuita, todo rito es trato con el
   demonio (la yopa es «hablar con el demonio»; *Tanasimi*, «demonio»). La
   etiqueta dice que **había un ser**, no qué era. Se lee el ser y se tira la
   etiqueta.
3. **La independencia.** Rivero y Neira son el **mismo autor**. Gumilla es del
   mismo medio jesuita ([[metodo-comparativo]]). Gilij leyó a Gumilla y supo
   del manuscrito de Rivero, pero sus maipures son su propio campo. Una
   coincidencia entre Rivero y Neira es **una** atestación.

**La capa: la regla del lexicón aplicada a los hechos.** Es una propuesta y la
decide Miguel.

- **El hecho achagua** entra como `atestiguado` **para su pueblo y su época**:
  colonial, Casanare y Meta, como la comparanda de `cosmovision_marina`. Nunca
  como dato caquetío.
- **Si el caquetío ya lo atestigua** (el llanto, el ajuar, la ausencia de
  ídolos, la muerte por hechizo), el achagua **corrobora**. La entrada no cambia
  de capa: se anota en `notas`/`lectura`.
- **Si el canon lo tiene `reconstruido` desde una sola hermana** (el sueño y el
  tabaco, desde el wayuu), el achagua es **la segunda hermana**. Se aplica el
  criterio con que se rehízo el núcleo («dos hermanas = reconstruida; una =
  hipotética»). Al revés, lo que sólo tenga apoyo wayuu y el achagua no
  confirme queda señalado para revisión, no degradado sin más.
- **Si el canon lo tiene `retro-abstraido` desde María Lionza** (`-015` los
  dueños, `-016` alimentar a los muertos), el achagua más el wayuu darían **una
  ruta arahuaca independiente** del culto del s. XX. Puede justificar
  `reconstruido` **con la comparanda citada**, y la Vía B se queda en lo que el
  ensayo ya decide para ella: estética y geografía.
- **Lo contemporáneo no es dato** (campaña del taíno). Lo que digan los achaguas
  de hoy (Meléndez 2004; la caracterización del Ministerio de Cultura) sirve
  para ver **si un nombre sigue vivo**: `retro-abstraido` como mucho.

---

## 3. Candidatas a minar

Disponibilidad comprobada hoy, 2026-10-08.

| # | Obra | Qué aporta a la creencia | Dónde y en qué formato | Esfuerzo | Capa al proyectar |
|---|---|---|---|---|---|
| A | **Rivero 1883**, libro II, caps. VI-VIII, pp. 102-118 | Lo central: dioses, creador, piache, yopa, sueños, hechizo, funeral, bebezón, *Chuvay* | **En el repo.** PDF de imagen y `.txt` OCR de archive.org (`historiadelasmi00rivegoog`, dominio público). Desfase pdf − 21 en este tramo | **Bajo**: unas 17 páginas, con el OCR para localizar y la imagen para citar | `atestiguado` achagua colonial. Al caquetío: corroboración o segunda hermana (§2.4) |
| B | **Neira y Ribero 1762**: una *consulta* a lo ya transcrito | El léxico de la creencia (§1.1) y el panteón (§1.6) | **En OneDrive**: el YAML en `6-fusion/` y los JPG en `fuentes_caquetios/neira_ribero_1762/` (IIIF de la Real Biblioteca II/2910). No queda nada por leer, sólo por verificar | **Muy bajo**: un script sobre el YAML y unas imágenes a 2-3× | Igual que A: es el mismo autor, así que no suma testigo |
| C | **Gilij t. III**, libro I, pp. ~1-40 | La religión maipure (Purrúnaminári, Tapanimarru, Queti), el más allá, el demonio, la ausencia de idolatría. Es la hermana más cercana del achagua, con un observador distinto | **En el repo**: PDF y `.ocr.txt` en italiano, con la ſ leída `f` (pista). Desfase −19 que deriva | **Medio**: italiano del XVIII, verificar en imagen | `atestiguado` maipure. Es la tercera hermana para los dueños y el creador |
| D | **Gilij t. II** (*Costumi*): lib. II caps. XVI-XX (piaches, curación, «se i Piaci sieno stregoni», muerte, funerales y luto, pp. 86-~115) y lib. IV caps. XVI-XXI (juegos, bailes, «ballo Queti», bebidas, pp. 266-~300) | Piache y funeral orinoquenses, con la mirada de Gilij | **No está en el repo.** archive.org `saggiodistoriaam02gili` (Getty): 438 imágenes, PDF 24,3 MB, `djvu.txt` 831 KB. Dominio público (1781). **Descargarlo lo decide Miguel** | **Medio** | Como C; ojo, que es mayoritariamente tamanaco, caribe |
| E | **Gumilla 1791**: t. II cap. III, t. I caps. XIV-XV y t. II cap. XXIII | El demonio por naciones, los funerales del Orinoco (segundos entierros no achaguas), la curación, los eclipses | **En el repo**, con capa de texto. La ed. de 1791 reimprime la obra de 1741/1745 | **Bajo-medio** | Lo achagua, como A. Lo demás es comparanda regional, no hermana |
| F | **Hernández de Alba 1948** (HSAI 4, pp. 399-412) | Una síntesis que sirve de mapa y dos lecturas que cotejar (§1.5) | **En el repo**, con capa de texto | **Muy bajo** | Ninguna propia: es secundaria y no cuenta como testigo |
| G | **Meléndez Lozano**: *La lengua achagua. Estudio gramatical* (CCELA, *Descripciones* 11, 1998); **la compilación de tradición oral (2004, con Mateo Kabarte como fuente principal)**; *Diccionario achagua-español, español-achagua* (Uniandes, 2011, 158 pp., ed. preliminar) | Si los nombres de 1736/1762 siguen vivos (`tanasimi`, `-minari`, el creador); las grafías modernas (`júuba` 'yopo', `tʃéma` 'tabaco') | **No están en línea en abierto** (no se encontraron). Hay que comprarlos o pedirlos por préstamo. Reseña del diccionario: *Maguaré* 26 (2), 2012 | **Alto** en conseguirlo, **bajo** en leerlo | `retro-abstraido` como mucho: es lo contemporáneo, de un pueblo evangelizado |
| H | **Wilbert y Simoneau**, *Folk Literature of South American Indians* (UCLA) | **No existe un volumen achagua.** El catálogo de UCLA lista sikuani (1992), cuiva (1991) y yaruro (1990), que son vecinos del llano no arahuacos, y **guajiro** (1986, 2 vols., con Perrin), que es de la **Vía A**, no de esta | — | — | Negativo bien medido: no hay que buscarlo más |
| I | Otras | Morey 1975 (*Ethnohistory of the Colombian and Venezuelan Llanos*, tesis, Utah; UMI 1981), sin texto libre localizado: síntesis, con caquetío-cuyba-jirara. Mora Camargo 1986 («Cataruben», *Rev. Col. de Antropología* 26, abierta), que es arqueología. Reinoso (piapoco, 1999/2002), que es **gramática piapoco**, no cosmovisión | Préstamo o descarte | — | Secundarias |

**Una corrección al encargo:** no hay un «*Achagua: Diccionario*, 1998». La obra
de 1998 es la **gramática** de Meléndez; el diccionario es de 2011. Y Reinoso
trabaja el **piapoco**, no el achagua.

---

## 4. Recomendación: tres minerías, en este orden

**Por qué este orden.** Las tres están ya en el repo (A y C) o en OneDrive (B):
no hay que descargar nada. A responde las cuatro preguntas de §2.2. B la ancla
en el léxico y resuelve el panteón. C añade un observador distinto y la hermana
maipure. D, E y G vienen después, si hacen falta. D y G necesitan el ok de
Miguel o una compra.

Cada minería deja una **propuesta en `6-fusion/`**, sin tocar `creencia.yaml`
(regla 5). Cada hecho lleva `pueblo`, `epoca`, `procedencia` y un campo
`proyeccion_caquetio`, cuyo valor es uno de: `corrobora:<id>`,
`segunda-hermana:<id>`, `ruta-arahuaca:<id>` o `no-se-proyecta:<motivo>`.
Además deja la bitácora en la ficha y un issue en `issues-pendientes/` con las
decisiones de capa (§2.4).

### 1º Rivero 1883, libro II, caps. VI-VIII (pp. 102-118)

- **§0 Pregunta.** ¿Qué creían y hacían los achaguas con sus dioses, sus
  especialistas, sus muertos y sus fiestas, y qué de eso es un gesto que el
  caquetío ya atestigua, que el canon sólo reconstruye desde el wayuu o que
  sólo sostiene María Lionza?
- **§2 Antes de contar, medir la ortografía.** Rivero escribe `Cuaygerri` y
  `Cuoygerri` en la misma página (el OCR da los dos). El OCR rompe los nombres
  en cursiva (`Jurrana^minari`, `Fruvisana` por *Pruvisana*, `Cmsiabirri`) y
  las cabeceras. Variantes que hay que probar: `piach`, `moh[aá]n|moj[aá]n`,
  `yopa`, `chaca`, `chuvay`, `minari`, `catana`, `difunt|entierr|llanto`,
  `sue[ñn]`, `berr[ií]a`, `mujeres`. Ningún cero vale sin leer el capítulo.
- **§3 Pasajes y preguntas.**
  1. Los dioses (pp. 112-113): el nombre, el dominio y el orden de cada uno;
     qué se dice de *Cuaygerri* y qué es lectura cristiana («verdadero Dios»).
     ¿Se les ofrecía algo? ¿Tenían especialista?
  2. Los especialistas (pp. 104-106): quién adivina, quién cura y quién hechiza;
     qué instrumentos usa; si es colectivo o de oficio; y si el «piache» es
     palabra achagua o de la lengua general de la misión (Neira no la trae como
     lema: medirlo).
  3. El sueño (p. 105): quién cuenta, cuándo, en qué tono y para qué. Este es
     el pasaje que le da segunda hermana a `creencia-002`/`-005`.
  4. Los muertos (pp. 111-112): la convocatoria, el llanto (¿quién canta, qué
     dice?), cuánto dura, dónde y cómo se entierra, el ajuar, el destino del
     alma. **¿Hay segundo tiempo?** (negativa a medir).
  5. La fiesta (pp. 106-110): la bebezón, quién sirve, con qué música y cuándo;
     la *Chuvay*; y **localizar la exclusión de las mujeres** que da HSAI.
  6. El cap. VIII: lo que Rivero dice que es «común» al llano frente a lo
     achagua.
- **§4 Esferas.** Sobre todo creencia. También transmisión (el creador «esto
  enseñan a sus hijos», el relato de sueños), geografía política (el cacique
  que abre el relato, el caney como unidad, la tumba del capitán), parentesco
  (quién llora y quién entierra) y ecología (la *chaca* y la yopa, ya en
  `cosmovision_marina`; no duplicar).
- **§6 Negativas que hay que dejar escritas**: el segundo entierro; los huesos;
  el mar; el dueño del trueno con culto. Y cualquier coincidencia con
  Pulowi/Juyá **por forma**.
- **§8 Independencia.** Rivero es el mismo autor que Neira: una atestación.
  Oviedo y Arcaya son caquetíos e independientes. HSAI no cuenta.
- **Imagen.** Hay que ver cada cita que decida una capa. Las pp. 112-113 ya
  están vistas hoy para el panteón.

### 2º Neira y Ribero: una consulta de creencia sobre el YAML ya transcrito

- **§0 Pregunta.** ¿Qué campo léxico de la creencia registra el vocabulario,
  qué lemas son de **doctrina** (los pidió el jesuita) y cuáles son
  **indígenas**, y qué orden tiene de verdad el panteón?
- **Cómo.** Un script sobre `6-fusion/achagua_neira_ribero_1762.yaml` que emita
  el censo: lemas por campo, con pliego y una marca
  `doctrina`/`indigena`/`dudoso`. **No se escribe una lista a mano.** Después,
  una verificación en imagen a 2-3× de cada voz que se vaya a citar.
- **Preguntas.**
  1. El panteón (56 izq.): ¿se confirma el desplazamiento de §1.6? Se lee la
     línea entera, incluido el remate «Amaribaca Vreca, capurraye Dios signo del
     cielo», que con el corrimiento queda sin glosa. ¿Es `Prubisana` o
     `Purubisana`? ¿Está desplazada también la lista de las diosas (*Vrumadua*,
     *Jarrutua*, *Jumenirro*)?
  2. `-minari`: todas las entradas que lo llevan. ¿Es 'dueño' en todas?
     ¿*Jurruna-* se relaciona con `purruna-` 'anegar' (35 der.) o con
     `Currucabe` 'labranza de maíz'?
  3. `tanasimi`: ¿lo segmenta el arte (`tana-` 'sombra' + `-si` + `-mi`)? Se
     contrasta con `Mucuiarimi`, `Bainacusamí` y `Masicasimi`.
  4. `Guabasi` 'alma' = 'estómago': ¿es una sede vital indígena (compárese el
     *aa'in* wayuu, «entre el pecho y el corazón») o una elección del
     catequista?
  5. «Ofrenda de difuntos», «Desenterrar», «Ayuno tal», «Agüero voluntario» y
     «fortuito»: ¿hay ejemplos que digan **qué** se ofrece, **por qué** se
     desentierra y **qué** ayuno es?
- **Salida.** La corrección del panteón **no** se hace en el YAML sin una
  segunda lectura. Va a la propuesta y a la ficha, y la decide quien fusione
  (el YAML genera `lexicon_achagua.py`, que importa el motor: ver la trampa en
  `CLAUDE.md`).

### 3º Gilij t. III, libro I «Della religione», pp. ~1-40

- **§0 Pregunta.** ¿Qué dice Gilij del Ser supremo, los seres menores, el
  demonio, los muertos y los piaches **de los maipures**, y qué se puede
  cotejar, nombre a nombre, con el achagua de Rivero y Neira?
- **§2 Ortografía.** Usar la clase `[fs]` donde se espere una `s`. El OCR da
  `Parrúnaminári`/`Purrúnaminári`, `Siri`/`Sisiri` y `eAmalivacá`. Los maipures
  salen como `Maipùri`/`Maipùre` y el achagua como `Acciàgua`. El desfase deriva
  (medido en la ficha), así que se cita la cabecera de la imagen.
- **Preguntas.**
  1. Purrúnaminári (pp. 8-9 y 25): la etimología de Gilij (*purrúna* 'todo'),
     los hechos que se le atribuyen y **qué marca él mismo como eco cristiano**.
  2. Tapanimarru (p. 6) ↔ `tabaminarro` 'diosas' de Neira: ¿quién es?
  3. Queti y Vasìtri (p. 155 del tomo; y el «ballo Queti» del t. II): ¿qué
     son?
  4. El más allá y el destino de los malos (pp. ~27-32): ¿hay lugar de los
     muertos con nombre?
  5. Qué separa Gilij como tamanaco (Amalivacá, caribe) de lo maipure. **Lo
     caribe no es hermana.**
- **§8 Independencia.** Gilij es otro observador, con otros informantes. Pero
  leyó a Gumilla: una coincidencia Gilij-Gumilla se comprueba antes de
  contarla.

### Después, si las tres lo piden

- Gilij t. II (piaches y funerales), **con el ok de Miguel para descargarlo**.
- Los capítulos de religión de Gumilla.
- Meléndez 2004 y 2011, para la continuidad de los nombres. Hay que
  conseguirlos.

### Lo que esta decisión deja para Miguel

1. **El orden de arriba**, y si las tres minerías van como una sola campaña o
   por separado.
2. **La regla de capas de §2.4**: si el criterio «dos hermanas = reconstruida;
   una = hipotética» se aplica también a los hechos de creencia.
3. **Descargar Gilij t. II** (archive.org, unos 24 MB).
4. **Si el ensayo gana una «Vía C»** (la hermana de los Llanos) o si el achagua
   entra repartido como corroboración dentro de las secciones que ya tiene.

## Enlaces

[[03_creencia_caquetia]] · [[mapa-creencia]] · [[03_creencia]] ·
[[rivero-1883]] · [[neira-ribero-1762]] · [[gilij-1780-1783]] ·
[[gumilla-1791]] · [[steward-1948-hsai-4]] · [[fabo-1911]] · [[jahn-1927]] ·
[[arcaya-1920]] · [[oviedo-y-valdes-1851]] · [[perrin-1992-1995]] ·
[[paz-reverol-2017-2018]] · [[maria-lionza-culto]] · [[metodo-comparativo]] ·
[[polities-caquetias]] · [[esfera-de-interaccion]] · [[INDICE_FUENTES]]

Fuentes web consultadas el 2026-10-08:

- [Gilij t. II en archive.org](https://archive.org/details/saggiodistoriaam02gili)
- [UCLA LAI, catálogo de *Folk Literature*](https://forms.international.ucla.edu/lai/publications/folk)
- [Reseña del diccionario de Meléndez, *Maguaré* 26 (2), 2012](https://dialnet.unirioja.es/descarga/articulo/4862382.pdf)
- [Morey 1975 en Glottolog](https://glottolog.org/resource/reference/id/7988)
- [Mora Camargo 1986](https://revistas.icanh.gov.co/index.php/rca/article/view/1575)
