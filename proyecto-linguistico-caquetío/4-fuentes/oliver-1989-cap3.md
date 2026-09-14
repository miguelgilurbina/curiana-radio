---
tipo: fuente
obra: "Chapter 3: XVI Century Ethnic Boundaries and the Nature of Caquetío Polities (en *The Archaeological, Linguistic and Ethnohistorical Evidence for the Expansion of Arawakan into Northwestern Venezuela*)"
autor: "Oliver, José R."
anio: 1989
genero: academico
local: "fuentes_caquetios/Chapter 3 Ethnohistory.DOC-comprimido.pdf"
paginas: 113
capa_texto: si
acceso: "Libre — la tesis completa (823 pp., incluye este capítulo) está en UCL Discovery, depositada por el propio Oliver: PDF https://discovery.ucl.ac.uk/id/eprint/10157455/1/Oliver_10157455_thesis_redacted.pdf · ficha https://discovery.ucl.ac.uk/id/eprint/10157455/. Verificado en el rastreo de 2026-08-14."
estado_minado: minado
cobertura: "familia (sesión 1), geografía política (sesión 5), economía/cerámica/guerra/religión (2026-08-04, issue #59), la esfera occidental §3.2 (2026-09-07, quinta polity), paginación DOC 2006 vs. impresa 1989 (2026-09-14)"
prioridad: media
sostiene: {hechos_corpus: 15, entradas_lexicon: 2, entradas_reforzadas: 1}
verificado: 2026-09-14
minado: 2026-08-04
aliases: ["Oliver 1989 cap. 3", "Oliver cap. 3", "Ethnohistory"]
---

# Oliver 1989, cap. 3 — Etnohistoria de los cacicazgos caquetíos

## Qué es

**La fuente académica más productiva del proyecto, con diferencia.** Reconstruye
la sucesión del cacicazgo histórico de Coro a partir de probanzas y crónicas del
siglo XVI al XVIII, y fija la geografía política caquetía. Es el pilar de dos
sesiones enteras del programa cultural ([[mapa-familia]] y
[[mapa-geografia-politica]]).

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Tamaño | 1.8 MB · 113 páginas |
| Capa de texto | **sí**, buena (~310K caracteres) |
| Receta | `pdftotext -enc UTF-8` o `pypdf`; ambos funcionan |
| Artefacto conocido | **Es de `pypdf`, no del PDF** (medido 2026-08-04): `pypdf` parte "Todariquiba" en **"T odariquiba"** en sus 7 apariciones; `pdftotext -enc UTF-8`, con o sin `-layout`, la da **limpia** en las 7. La receta manda: si una búsqueda no da nada, probar la otra antes de concluir que el dato no está |
| ⚠️ Paginación | **Este PDF no es la tesis impresa.** Es la reedición DOC/PDF de 2006: su cabecera es pdf + 182, y no coincide con la página de 1989. Ver §Paginación |

## Paginación: dos ediciones del mismo capítulo (2026-09-14)

**Qué se preguntó.** El 2026-09-13 apareció que el capítulo está en el repo
dos veces, con paginaciones distintas, y que las citas de
`oliver-1989-cap3` mezclan las dos. ¿En qué edición está cada cita, y cuál es
su página impresa?

**Las dos ediciones.**

| | Edición DOC/PDF 2006 | Tesis impresa 1989 |
|---|---|---|
| Archivo | `Chapter 3 Ethnohistory.DOC-comprimido.pdf` | `Oliver_1989_Tesis_Arawakan_NW_Venezuela_UCL.pdf` (escaneo) |
| Texto | capa de texto | ninguno: OCR con `ocr_fuente.py` |
| Página | cabecera = pdf + 182 (constante en sus 113 páginas) | impresa = pdf − 27 (cabecera leída en las 141 páginas OCR, pdf 205-345) |
| Notas al pie | numeradas desde 1 en el capítulo | numeradas corrido: **nota impresa = nota DOC + 92** |

Entre las dos **no hay desfase constante**: la impresa intercala páginas de
figura, y va de −1 al principio del capítulo a +17 al final. Y la DOC no es solo
re-maquetación: añade material *«only in PDF version, 2006»* (la imagen
satelital del Yaracuy, fotos, color) y **cambia alguna grafía**: el primer
asiento de los Amuayes, «Cayerta» en la impresa (276), sale «Cayerúa» en la DOC
(264).

**Qué se halló.** La propuesta completa, cita por cita y con reemplazo, está en
`6-fusion/paginas_oliver_cap3_doc_vs_impresa.yaml`. Incluye el mapa de las 113
páginas DOC a su página impresa. Lo gordo:

- **La mayoría de las citas de este capítulo están en la DOC**: §3.2 (salvo
  los caribes), el pacto de Todariquiba, el buco, Barquisimeto y el tamude. Las
  que están en la impresa son las que se minaron sobre el escaneo:
  `oliver-1989-cap3-vecinos` (223-250), los dos clanes de Paraguaná (275-276) y
  *Arubanas* (256). Y un grupo no cuadra con **ninguna** de las dos (abajo).
- **La «corrección» del 2026-09-01 (255-256 → 265-266) fue un cambio de
  edición, no un error**: 255-256 era la DOC. El corpus quedó en la impresa; el
  ensayo 01, en la DOC.
- **Hay citas que no son de ninguna de las dos.** La poligamia de Manaure, la
  viuda «carnal or classificatory?» y el traslado de la hija se citaban en
  260-262. Están en DOC 268-269 = impresa 280-281, mirado a ojo en la 280. La
  frase «inherited by the son of the diao» está en §3.11, impresa 305. Y
  **la carta de Bastidas de 1538** se colgaba de la p. 251, que es la del pacto
  de 1527; está en DOC 258-259 = impresa 269, mirado a ojo. Esto último afecta a
  cinco nodos de `asentamientos.yaml` y a tres topónimos.
- **Dos errores de contenido que salieron al paso**, anotados como colaterales
  en el YAML. (1) La maloca de 40-50 es de **Curazao** (Vespucio), no de
  Barquisimeto/Yaracuy como decía la tabla de abajo (impresa 275). (2) La «red
  de alianzas por comercio: cuentas de concha, sal y azabache» de
  §Economía es de los **jirajaranos**, que además «none … had developed a
  confederation» (impresa 245). La sal con los enemigos es de Barquisimeto
  (impresa 247). Regla 4.

**Qué no se hizo.** No se tocaron el corpus, `curiana_polities.py`,
`lexicon_toponimos.py` ni los ensayos (regla 5). Tampoco las tablas de esta
nota: **siguen con las páginas tal como se citaron**, y el YAML da la
equivalencia. No se barrieron las otras notas de `4-fuentes/`, `1-plan/` ni
`2-lengua/*.md`.

> 📌 **Convención propuesta (la decide Miguel): citar la impresa.** La obra es
> la tesis de 1989, y las otras notas de Oliver ya citan la impresa
> (`-vecinos`, Tabla A-8, dos clanes). La DOC sigue siendo la mejor para
> **buscar**: se busca la frase en la DOC y se traduce con el mapa del YAML,
> nunca sumando un desfase. Toda «n. N» debe decir de qué edición es.

## Qué ha dado

**15 hechos del corpus** — el número más alto de cualquier fuente junto a
[[jahn-1927]] y [[camacho-2011]]:

| Página | Hallazgo | Entrada |
|---|---|---|
| 189 | Los caquetíos de la Guajira como *"avant guarde posts"* originados en Falcón costero | `geografia_politica-002` |
| 190 n.4 | El término wayuu correcto es *eirrüku*/*apüshi*, no "clan" (citando Goulet 1981) | — |
| 249 | San Bartolomé de Vespucio en el **Golfete de Coro**, no Maracaibo (vía Ramos Pérez 1976: 88) → el nombre "Venezuela" | `geografia_politica-006` |
| 251 | Pacto de 1527; *"the main diao or great cacique, Manaure"*; **Todariquiba** | `geografia_politica-003` |
| ~~255-256~~ **265-266** | Sucesión Don Sancho Uriacoa → Don Luis Caguallo → Don Luis Martínez Manaure; conflicto de "bastardía" en Paraguaná (Martí 1969) — **páginas corregidas 2026-09-01** (la 255 es la Fig. 40, la 256 el viaje de Ojeda; verificado a ojo). Detalle nuevo: los que impugnan son "the Indians of Santa Ana and Moruy" — las dos parcialidades actuando | `parentesco-001/003` |
| **275-276** | ⭐ **Los DOS CLANES de Paraguaná** (minería del 2026-09-01, a pregunta de Miguel): **Amuayes** (sur; primero Cayerda, luego Moruy) y **Guaranaos** (norte; Santa Ana), cada uno con beach heads y derechos de pesca propios, un jefe supra-aldea por grupo, ambos bajo el polity costero de Manaure. Oliver cita González Batista 1984 + Delmonte 1883. Modelo general: aldeas como cacicazgos taínos, fronteras por matrimonio y parentesco; maloca 40-50 (Vespucci); silencio de cronistas sobre estructuras rituales ("quite secretive") | `6-fusion/paraguana_dos_clanes.yaml` |
| 260-262 | Poligamia de Manaure (*"the only cacique unambiguously cited to be polygamous"*); la viuda que "se casa" con su hijo — *"carnal or classificatory?"* | `parentesco-002/015` |
| 262-263 | El **buco** de Ballesteros [1550]: 4-5 mil indios para repararlo, 14-15 mil de población, 400 hacia 1550 | `geografia_politica-004/005` |
| 268-270 | El oficio heredado por el hijo del diao (s. XVI); linaje como base de la jefatura local; malocas de 40-50 en Barquisimeto/Yaracuy — **contrastadas explícitamente** con el patrón costero | `parentesco-001` |
| 287-288 | El vínculo achagua-caquetío vía *mude* → *tamude* ("primos"), citando Jahn 1927: 213 | `parentesco-021` |

**Lexicón**: 2 entradas lo citan (`diao`, `uriacoa`) — ambas por **corrección**
de una glosa previa sin fuente.

### §3.2 *The Western Sphere*, releída el 2026-09-07 para la quinta polity

**Qué se preguntó.** Miguel decidió modelar la esfera occidental (Maracaibo,
la Guajira) como polity futura «porque Oliver también menciona información de
esa región en el contexto de Coquibacoa». ¿Qué dice, y con qué página? Este
PDF tiene capa de texto y §3.2 está entero (la tesis completa no la tiene).
~~Página impresa = pdf + 182.~~ **No** (2026-09-14): eso es la cabecera de la
edición DOC 2006. Las páginas de esta tabla son DOC; su página impresa está en
`6-fusion/paginas_oliver_cap3_doc_vs_impresa.yaml` (ver §Paginación).

**Qué se halló** (todo en `curiana_polities.py::POLITIES["occidental"]`):

| Página | Hallazgo |
|---|---|
| 185 | La *Western Sphere* definida: el lago de Maracaibo y sus llanuras aluviales, la Guajira semiárida, los valles del Ranchería y el César; el noreste del lago como «strategic locus» de paso entre Venezuela, la Guajira, Santa Marta y el Magdalena |
| 189 | Tesis: los asentamientos caquetíos de la Guajira fueron «avant guarde posts» que comerciaban sal por oro con wanebucanes y coanaos; «undoubtedly originated from Coastal Falcón» (ya `geografia_politica-002`) |
| 191 | Castellanos llama **Coquibacoa** al norte-noreste de la Guajira (Macuira, Jarara), con sementeras; Pedro de Limpias encontró allí resistencia **«guanebucán y caquetío»**, guerreros «con armas castellanas en las manos» (Parra 1930a: 284) |
| 192 | El mapa de Juan de la Cosa (1500) y el anónimo de c. 1534 escriben **Coquibacoa** sobre la península; «guajiro» no aparece en ninguno |
| 199 | Esteban Martín (1534): la costa de la Gobernación «toda poblada de caquetíos» ochenta leguas al oeste de Coro hasta el Cabo de la Vela; y **«En Coquibacoa y en el Cabo de la Vela… poblado de indios coanaos e caquetíos»**. La Gobernación entera se llamó Coquibacoa a principios del XVI. Dos sectores caquetíos: Cabo de la Vela y Punta Espada–Chichibacoa |
| 200 | Cronología: en la Guajira quizá desde **1200 d.C.**; la intensificación del contacto Los Médanos ↔ Cabo de la Vela / Punta Espada–Chichibacoa **tiene su pico en 1400 d.C.** (n. 28). La arqueología de la Guajira, «as yet unknown» (n. 27) |
| 202 | Los caquetíos de Juruara y los de la Guajira, «avant guarde settlements of the expanding Caquetío peoples»; «very little is known about the culture»; rasgo común: siempre en las mejores tierras bajas de cultivo, **nunca en tierras altas** |
| 207 | ⭐ Los wanebucanes, de lengua desconocida, quizá arahuacos: en sus nombres de aldea hay morfemas «suspiciously Caquetío» — **«Paragua-nil» y «Coria-na»** — que Oliver explica por el nexo comercial con los caquetíos en Punta Espada–Chichibacoa. Un segundo *Coriana*, en la Guajira (#33); y una segmentación *paragua* + sufijo, *coria* + *-na* (#109) |
| 211 | Las «piedras verdes» de la capitulación de Ojeda (1500: «Quinquevacoa… donde están las piedras verdes») como bien de ese comercio |
| 222 | El balance de la esfera: solo los caquetíos tienen distribución amplia, como «frontier settlements or outposts»; minoría numérica; socios wanebucanes y coanaos, «shunned» onotos, kusi'na y wayú (ya `geografia_politica-009/010`) |
| 249 n. 94 | El cabo **Chichibacoa** «suspiciously sounds like Coquibacoa, except for a /k/::/ch/ sound shift» |
| 292 | Cerámica: formas de vasija de aparición súbita y tardía en Coro «which can only have been derived from the Ranchería area» (Los Médanos ↔ Portacelli) |

**Qué no se halló.** Nada sobre liderazgo, demografía ni religión de estos
caquetíos: los tres ejes quedan como huecos en el módulo, a propósito.

## Por qué importa metodológicamente

Este capítulo es la razón por la que existe la regla *precontacto ≠ colonial*.
Su registro patrilineal es dato real del **cacicazgo colonial** (s. XVI-XVIII),
no del precontacto que la simulación modela — y el propio Oliver desconfía de la
lectura simple: duda entre "hijo" carnal y clasificatorio, y registra que la
legitimidad se impugnaba por **la madre**. Ver [[01_familia_caquetia]] §1.

## Los cuatro barridos restantes — minado 2026-08-04 (issue #59)

Se le preguntó por **economía, cerámica, guerra y religión**. La cosecha es
desigual: guerra y economía son abundantes, la cerámica es una sola frase (pero
decisiva), y la religión es escasa **y casi toda de Barquisimeto, no de la
costa** — que es justo donde vive la simulación.

> 📌 Lo que salió de aquí está modelado en [[polities-caquetias]] y en
> `curiana_sim/curiana_polities.py`.

> ⚠️ **La advertencia que atraviesa los cuatro barridos.** Oliver dedica el
> capítulo a demostrar que **los caquetíos NO eran una cultura homogénea**: la
> Curiana de este proyecto es **caquetío costero** (Coro, Todariquiba), y buena
> parte de lo que sigue es de **Barquisimeto/Yaracuy**, que él contrasta
> explícitamente con la costa. Importar lo uno por lo otro es el mismo error que
> [[01_familia_caquetia]] §1 ya evita con la sucesión. Cada hallazgo abajo va
> marcado con su polity.

### Guerra — el barrido más productivo

- **[Barquisimeto] Doble jefatura: Jefe de Paz y Jefe de Guerra** (pp. 276-279).
  Oliver propone que son **personas distintas**, porque los atributos se
  contradicen: el Jefe de Guerra **acumula** rango por hazañas militares, y lo
  exhibe en adornos corporales; el Jefe de Paz **debe redistribuir** —maíz,
  *maçato*, yuca, legumbres a cambio de trabajo en los campos— y pierde
  autoridad si acumula. Explícitamente "vagamente reminiscente del *Big Man*
  melanesio", con las cautelas de Ross (1978).
- **[Barquisimeto] Los dos oficios solo operan en su contexto.** En paz los
  aldeanos declaran que "no tienen señor que los gobierne"; en guerra la
  autoridad se centraliza y jerarquiza. Federmann (1530) y el documento de 1579
  coinciden en la negativa a reconocer un jefe paramount.
- **[Barquisimeto] Aldeas fortificadas** ("fortificadas", quizá empalizadas), 23
  aldeas agrupadas, ~4.000 habitantes cada una (Federmann [1557] 1958:66-67).
- **[Barquisimeto/Yaracuy] El ciclo de paz y guerra tiene motor agrícola**
  (p. 278): valles de tamaño limitado + crecimiento demográfico → expansión
  sobre territorio ya poblado → guerra. Y la jefatura de paz **depende** del
  excedente agrícola, que la presión demográfica erosiona. Solo la victoria o la
  derrota completa rompe el ciclo.
- **[Yaracuy] Confederación elástica**: aldeas aliadas de dos en dos o de cuatro
  en cuatro, menos poderosas que Barquisimeto por no estar unidas — pero
  Federmann anota que **se unirían si fueran atacadas** con fuerza suficiente.
- **[Cojedes-Llanos] Guerra de captura de esclavos, institucionalizada** (n. 126,
  p. 277). Federmann pidió comprar una *naboria* en la aldea de **Itabana** y se
  la negaron, "aunque acostumbraban a comprarlas y venderlas entre sí". Oliver
  subraya que **esto solo vale para el bajo Cojedes**, y que no hay tal
  afirmación para los caquetíos de otras áreas.
- **[Contraste] Los kalina/kalinago sí hacen del raid de prisioneros el motor
  del prestigio** (Dreyfus 1983-4); la guerra caquetía de Barquisimeto es, en
  cambio, "constreñida", y su causa probable es la merma de espacio agrícola.
  Es un matiz que **le quita generalidad al modelo caribe** de
  `parentesco-028/029`.

### Religión — poco, y casi nada costero

- **[Barquisimeto] Sacrificio humano por sequía** (documento de 1579, Arellano
  Moreno 1964:189-190). Cuando falta el agua, compran a la madre la muchacha
  "más hermosa y mejor agestada" de diez años para arriba, la llevan a la ribera
  del río y la degüellan con una piedra sin filo, "y ofrecen la sangre por
  sacrificio, y dicen que aquella quieren dar **al sol por mujer**" — porque el
  sol está enojado y por eso no llueve. Tras la llegada española lo siguen
  haciendo **a escondidas**.
  > Dato **colonial y de Barquisimeto**. No es norma precontacto de la Curiana
  > costera, y proyectarlo sería exactamente lo que la regla del proyecto
  > prohíbe. Se registra porque es el único rito caquetío descrito con detalle
  > en todo el capítulo, y porque la ecuación **sol-enojado → sequía → esposa**
  > es material cosmológico de primer orden si alguna vez se decide usarlo.
- **[Barquisimeto] El *boratio* vive apartado**, en una casita de paja propia,
  fuera de la aldea principal (1579). Y el jefe de paz de Barquisimeto **no** es
  a la vez gran chamán.
- **[Costa] Manaure sí lo era** (p. ~251 y ss.): su poder no era solo secular
  sino **sagrado** — Oliver sospecha que su reputación descansaba en su
  capacidad de gran chamán "que podía controlar y predecir fenómenos naturales",
  mediando entre lo sobrenatural y lo natural. Etiqueta corporal elaborada:
  llevado siempre en hamaca por un séquito, adornos de oro y cuentas de concha.
- **[Llanos del norte] Ninguno de los jefes** aparece caracterizado con poderes
  chamánicos; el liderazgo militar con los guaycaríes es colaborativo y menos
  centralizado.

> **La estructura que sale de cruzar los tres**: el caquetío costero **fusiona**
> poder secular y sagrado en una sola persona (Manaure); Barquisimeto los
> **separa** en tres (jefe de paz, jefe de guerra, boratio apartado); los Llanos
> no registran el eje sagrado. La Curiana de la simulación está en el extremo
> fusionado — y Shaboro como piache aparte de Manaure es, en rigor, más el
> modelo de Barquisimeto que el costero.

### Economía

- **[Costa/Guajira] Red de alianzas comercial**: cuentas de concha, **sal** y
  **azabache**. Las aldeas de la región desarrollaron una "confederación" —una
  red amplia de alianzas— sobre la base del comercio.
- **[Barquisimeto] Comerciaban sal con sus propios enemigos**, rodeados de
  ellos. El oro venía de las serranías de **Nirgüa-Buria**; la sal, probablemente
  por el valle del **Yaracuy**.
- **[Estratégico] El límite Barquisimeto/Yaracuy es el paso entre los Llanos y
  la costa caribeña**: controlarlo era controlar el comercio y las
  comunicaciones. Es una de las causas de la competencia entre ambas polities.
- **[Barquisimeto] El *maçato* (cerveza de maíz) es el instrumento político**
  del jefe de paz: el más estimado es quien lo dispensa con más generosidad — y
  además "sabe dar ejemplo: buen trabajador".

### Cerámica — una sola frase, y vale por el barrido entero

> "the Coastal Caquetío distribution in time and space is **precisely
> congruent** with the distribution of the **Dabajuran Sub-Tradition** of
> Falcón"

Y en paralelo, los complejos del interior se atan a la **Sub-Tradición
Tierran**. Es decir: Oliver hace corresponder sus dos polities caquetías
(costera vs. Barquisimeto) con las dos sub-tradiciones cerámicas
(Dabajurán vs. Tierran).

Además: sitio arqueológico con **cerámica dabajurana y mayólica del s. XVI** en
**Tomodore**; y formas de vasija aparecidas tarde en el área de Coro (Los
Médanos, Portacelli) que **solo pueden derivar del área del Ranchería** —
correspondiendo con el comercio caquetío de la Guajira.

> ⚠️ **Cruzar con [[antczak-2017-cariban]] p. 157, que cita este mismo pasaje y
> luego lo complica**: "no todos los rasgos arqueológicos recuperados en los
> sitios de la costa de Falcón son dabajuroides, lo que plantea un desafío a
> nuestra comprensión de los caquetíos protohistóricos" (José Oliver 2016,
> *pers. comm.*). El propio Oliver matizó en 2016 la ecuación que había hecho
> en 1989.

### Lexicón: `capu` gana una segunda fuente independiente

El documento de 1579 cita, **marcándolo como caquetío explícitamente**, la
palabra con que el chamán llama a lo que los españoles entienden por "demonio":

> "allí dentro llaman al demonio, que en su lengua llaman **capú** (y ésto es en
> la lengua caquetía) […] y este nombre que ellos tienen puesto al demonio
> (también) nos tienen puesto a nosotros. Y esto es en la lengua caquetía, que
> es la más común"

`capu` ya estaba en el lexicón como `caquetío-atestiguado` vía
[[zavala-reyes-2015]] #60, que lo trae de Galeotto Cey. Ahora tiene **dos
fuentes independientes** —Cey y el documento de 1579— separadas y coincidentes.
Es el mismo tipo de convergencia que [[gatschet-1885]]↔[[van-buurt-2014]], y
sube la entrada de "atestiguada por una fuente" a "atestiguada por dos".

El detalle etnográfico que trae de regalo —**los caquetíos aplicaron el mismo
nombre a los españoles**— es demasiado bueno para no dejarlo anotado.

> 📌 **Por qué la segunda cita no está en el código.** `capu` vive en
> `curiana_sim/lexicon_zavala.py`, que **lo genera**
> `minar_zavala_glosario.py`: cualquier anotación a mano se pierde en la
> siguiente regeneración. La cita de 1579 se queda aquí hasta que se decida
> cómo un lema generado puede acumular fuentes de fuera del glosario de Zavala
> — que es un problema real del diseño del lexicón, no un olvido de esta
> sesión, y afecta a toda entrada que alguna vez gane una segunda atestación.

## Qué falta

- No importar sin más el dato de las malocas del interior a la Curiana costera:
  **el propio Oliver los distingue**.
- **Los hallazgos de arriba están en la nota, no en el corpus.** Ninguno se ha
  fusionado a `3-mundo/corpus/`: son propuesta para revisión, en la misma
  disciplina que los minadores del lexicón.
- ~~La **religión costera** sigue siendo el hueco~~ — **resuelto el 2026-08-04**:
  todo el detalle ritual de *este capítulo* es de Barquisimeto, sí, pero
  [[arcaya-1920]] pp. 97-100 trae el oficio del boratio costero completo
  (oráculo, adivinación doméstica y cura paso a paso), citando a Oviedo y Valdés
  t. II p. 298. [[jahn-1927]] no aporta aquí: su material religioso es guajiro,
  ayomán y timote.
- Cadena de citas a verificar: Ballesteros [1550] en Bécker 1950, Martí 1969,
  Ponce y Vaccari 1977, [[ramos-perez-1978]] — todos llegan **vía Oliver**.

## Enlaces

[[oliver-1989-cap2]] · [[01_familia_caquetia]] · [[05_geografia_politica_y_sucesion]]
