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
cobertura: "familia (sesión 1), geografía política (sesión 5), economía/cerámica/guerra/religión (2026-08-04, issue #59)"
prioridad: media
sostiene: {hechos_corpus: 15, entradas_lexicon: 2, entradas_reforzadas: 1}
verificado: 2026-08-04
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
