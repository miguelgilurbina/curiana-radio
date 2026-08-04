---
tipo: ensayo
sesion: 2/4 — programa corpus cultural
pregunta: "¿Dónde existía el caquetío?"
moc: MOC_ecologia
corpus: [ecologia.yaml]
fuentes: [camacho-2011, antczak-2015-las-aves, rouse-cruxent-1963, alvarado-1921, jahn-1927]
version: v2
---

# ¿Dónde existía el caquetío?

## La ecología, la geografía, la hidrología y la fauna del mundo de la Curiana

*Sesión 2 del programa «corpus cultural». Investigación y redacción, siglos XIV–XV,
Golfete de Coro, noroccidente de Venezuela.*
*(v2 — amplía la capa biológica y cierra los huecos de cobertura detectados en la revisión
de la v1: `conuco`, `taller_canoas`, el alisio como sección propia y el reetiquetado de las
afirmaciones apoyadas solo en prensa.)*

> **Método y marcas.** Este ensayo describe el medio físico y biológico donde vivió la
> comunidad simulada de la Curiana. La etnohistoria (crónicas, arqueología) casi no describe
> el paisaje: lo da por supuesto. Por eso aquí la fuente principal es la **ciencia natural
> moderna** —geomorfología, climatología, ecología, zoología— proyectada hacia atrás con los
> cambios conocidos. Cada hecho del corpus (`curiana_sim/cultura/ecologia.yaml`) lleva una de
> cuatro marcas: **atestiguado** (citable a fuente concreta, incluida ciencia natural moderna),
> **reconstruido** (inferencia razonada, p. ej. proyectar la ecología actual 600 años atrás),
> **retro-abstraído** (tradición viva local de Paraguaná / Coro), **hipotético** (plausible sin
> respaldo). En duda, se degrada a la más débil.

> **Mapa** · [[MOC_ecologia]] — [[02_ecologia|hoja de fuentes]] — `ecologia.yaml` · `ecologia_lexicon_map.md`
> **Fuentes** · [[camacho-2011]] (pilar) · [[antczak-2015-las-aves]] · [[rouse-cruxent-1963]] (**0 bytes**) · [[alvarado-1921]] · [[jahn-1927]]
> **Diseños que salieron de aquí** · [[02_capas_biosfera]] · [[02_motor_ambiental]] · [[02_protocolo_habla_paraguanera]]

---

## 1. El hueco que este ensayo llena

El canon existente (`CULTURA_CAQUETIA.md`) es fuerte en cosmología, economía, política y
lengua, y define el ciclo bianual seca/lluvias (§2). Pero nunca describe **el sustrato físico
y biológico**: qué era una duna, de dónde salía el agua dulce, qué peces había en el Golfete,
qué animales compartían el mundo con la gente, por qué el salinar solo produce en la seca. Las
locaciones de la simulación —`orilla`, `manglar`, `salinar`, `conuco`, `buco`, `matorral`,
`taller_canoas`, `camino_islas`— existen como etiquetas sin sustancia ecológica. Este ensayo y
su corpus dan esa sustancia, y —lo más productivo para el experimento lingüístico— **localizan
los huecos léxicos**: fenómenos centrales del paisaje que la comunidad vive a diario pero para
los que el lexicón todavía no tiene palabra caquetía. Esos huecos son el lugar natural donde la
simulación puede acuñar neologismos.

---

## 2. Geografía física precolonial: istmo, golfete, península

La Curiana se sitúa en el vértice de tres unidades que aún hoy definen el noroccidente
falconiano: el **Golfete de Coro** (una bahía somera y semicerrada), la **Península de
Paraguaná** (un macizo casi insular al norte) y el **Istmo de los Médanos** (la lengua de arena
que une Paraguaná al continente y separa el Golfete del mar Caribe abierto).

La pregunta clave para la simulación —¿cómo era este paisaje **hace 600 años**?— tiene una
respuesta tranquilizadora **para la forma del terreno**: prácticamente igual al actual. Camacho
et al. (2011) datan la estabilización del Istmo de Médanos hacia hace **~4 000 años**, cuando el
ascenso tectónico y el nivel del mar en su posición actual fijaron la línea de costa. Doce mil
años atrás el mar estaba 85 m más bajo y la costa 20 km más al este; pero para el siglo XV toda
esa dinámica ya había concluido. El caquetío caminó, esencialmente, sobre los mismos médanos que
hoy protege el Parque Nacional Médanos de Coro. **[atestiguado — Camacho et al. 2011]**

> ⚠️ **Pero esta licencia NO se extiende a la fauna.** La geomorfología y el clima son
> constantes entre el s. XV y hoy; **la fauna no lo es**. La caza indiscriminada moderna ha
> vaciado el paisaje de sus grandes mamíferos (ver §10.6). Proyectar la fauna actual hacia atrás
> **subestima** el mundo animal caquetío. Esta es una corrección importante respecto a la primera
> versión de este ensayo, que trataba «el paisaje» como un bloque único. **[reconstruido]**

El istmo es un mosaico de ambientes sedimentarios que, de este a oeste, se ordenan así (Camacho
et al. 2011): una **playa** de hasta 200 m de ancho; un campo de **dunas longitudinales
estabilizadas** (~51 km²), montículos alargados de 800–1 200 m de longitud y 5–10 m de altura,
orientados ENE–WSW, paralelos al viento y fijados por vegetación xerófila; un cordón de
**salinas** (~11 km²); y una vasta **zona pantanosa** (~80 km²). Coexisten además **dunas
transversales activas** (~12 km²) —arena móvil, sin fijar— que son el rostro más famoso de «los
Médanos». La distinción entre la duna viva que camina con el viento y la duna vieja tapizada de
cují y grama es una lectura del paisaje que cualquier caquetío haría, y —ver §12— no tiene
palabra en el lexicón. **[atestiguado — Camacho et al. 2011]**

---

## 3. Clima: el desierto costero BSh/BWh y sus consecuencias

Coro y su istmo son **semiáridos a áridos**. El registro de la estación Coro da ~380–417 mm de
lluvia al año, temperatura media de 28 °C con una variación anual mínima (1–2 °C) y viento del
**ENE los doce meses del año** (Camacho et al. 2011; datos climáticos de Coro). El núcleo de los
médanos alcanza la aridez plena (BWh de Köppen); la franja de Coro es semiárida cálida (BSh). La
lluvia no se reparte: se concentra en un pulso corto (octubre–diciembre) y el resto del año la
evaporación potencial supera con mucho a la precipitación.

Tres consecuencias estructuran la vida de la Curiana:

1. **El agua dulce es el recurso limitante, no el alimento.** En un litoral con pesca, sal y
   conucos, lo que escasea es agua bebible. De ahí el peso desmesurado que el canon y la
   simulación dan al **buco** y a los oficios de Corie-ko y Buco-ko: no es folclore hidráulico,
   es supervivencia — y además es un hecho histórico documentado (§5). **[reconstruido]**
2. **La estacionalidad es eólica y pluvial, no térmica.** «Seca» y «lluvias» se distinguen por
   el viento y el agua del cielo, no por la temperatura (que apenas se mueve). El calendario
   ritual bianual del canon coincide exactamente con el clima real. **[atestiguado — datos Coro]**
3. **La evaporación es un aliado, no solo una amenaza:** es la que fabrica la sal (§7).

---

## 4. El alisio del noreste: el hecho ecológico maestro

Si este mundo tiene un solo protagonista no humano, es el **viento**. El alisio del ENE sopla
**los doce meses del año**, con velocidad media de ~6,1 m/s (~20 km/h) y máximos en la seca
(marzo–mayo). Su dirección es tan constante que las tablas climáticas de Coro registran ENE en
los doce meses, sin excepción. **[atestiguado — Camacho et al. 2011, pp. 9, 15]**

Lo notable es cuántas cosas *distintas* explica un solo hecho físico:

- **Construye el territorio.** Las dunas longitudinales son paralelas al viento porque el viento
  las hizo; el istmo entero es un producto eólico (§2).
- **Fabrica la sal.** Viento + sol evaporan las charcas del salinar y dejan la costra de *biro*
  (§7). Sin alisio no hay economía salinera, y sin sal no hay poder redistributivo de Manaure.
- **Ordena la pesca.** Mueve el agua, la aclara, y con ella desplaza los cardúmenes (§10.5).
- **Gobierna las corrientes del Golfete.** Las corrientes del golfete las rigen la marea y, sobre
  todo, la acción tangencial del viento: el aire arrecia en el curso del día y empuja las
  corrientes hasta cerca de **1 m/s por la tarde**. La mañana es calma; la tarde es trabajo duro
  de remo. **[atestiguado — estudios de corrientes del Golfete de Coro]**
- **Abre y cierra el camino a las islas.** **Aruba está a ~25 km al norte de Paraguaná**,
  alcanzable en canoa y en días claros visible. El poblamiento arahuaco de las ABC y la
  dispersión de la cerámica dabajuroide hasta ellas prueban navegación indígena regular
  (Antczak & Antczak 2015). **[atestiguado]**
- **Define la estación.** El «Tiempo de Viento» del canon *es* el alisio arreciando.

Y sin embargo: el lexicón tiene **joutai** (viento genérico) y **habobrisa** (brisa del Golfete),
pero **no un nombre propio para el alisio**. La fuerza que ordena el año no está nombrada (§12).

---

## 5. Hidrología: ríos efímeros y la ingeniería del agua

La zona de Coro se drena por cursos modestos y estacionales. El **río Mitare** (~120 km) es el
principal de la vertiente del Golfo de Venezuela; los ríos **Coro** y **Caujarao** desembocan en
el Golfo de la Vela, y **Ricoa, Hueque y Tocuyo** en la costa nororiental (Camacho et al. 2011).
Pero en clima BSh estos cauces son en gran parte **efímeros**: llevan agua tras el pulso de
lluvias y se reducen a hilos o lechos secos el resto del año. No hay un gran río perenne que
garantice agua. **[atestiguado / reconstruido]**

Aquí aparece el dato más valioso de esta ampliación. El **buco no es solo una palabra del
lexicón: es un hecho histórico documentado.** Los caquetíos desarrollaron un sistema de riego
llamado precisamente **buco**, que **trazaron en las márgenes del río Coro**; y los caquetíos del
Valle del Turbio idearon sistemas para llevar agua de los ríos a los campos cultivados. La
ingeniería hidráulica que el canon (§7) atribuye a la Curiana como «vida intelectual» está
atestiguada con su nombre propio y su ubicación. **[atestiguado — fuentes sobre agricultura
caquetía y el sistema buco del río Coro]**

Esto convierte al `buco` de la simulación en la locación **mejor anclada históricamente** de
todas. Alrededor de él, el lexicón conserva el verbo **jaguey** («estancar, represar, crear
charco artificial») y **jacuque** («regar, irrigar»). La comunidad no espera el agua: la
**captura** en el pulso húmedo y la **administra** durante la seca. El evento `crecida_buco`
—reparar las represas bajo el aguacero, temiendo que reviente la pared de barro— dramatiza con
exactitud este régimen: demasiada agua de golpe es tan peligrosa como la sequía.

---

## 6. El conuco: agricultura en el borde del desierto

El canon afirma que la Curiana siembra yuca, maíz, batata y caraota, pero nunca dice **cómo**.
La agricultura caquetía está documentada: era **muy desarrollada**, basada en **maíz, yuca y
batata**, y apoyada en riego (§5). **[atestiguado]**

El **conuco** no es una parcela sin más: es un sistema agrícola de **perturbación y sucesión**
con una lógica ecológica precisa. Se tala y se quema; **las cenizas devuelven al suelo los
nutrientes que estaban almacenados en la vegetación**; los troncos talados se dejan en el sitio,
donde frenan la erosión y alimentan hongos y microorganismos. El conuco **gana biodiversidad con
el tiempo** —es policultivo, no monocultivo— y esa mezcla es justamente lo que **previene las
plagas** que arruinarían una cosecha uniforme. Su función declarada es dar **seguridad
alimentaria a un grupo familiar**. **[atestiguado — literatura sobre el conuco indígena]**

Tres consecuencias para la simulación:

1. **El conuco es conocimiento, no rutina.** Saber qué se siembra junto a qué, cuándo quemar y
   qué dejar en pie es un saber técnico transmitido — material para las escenas de enseñanza
   (Corie-ko a los jóvenes) que hoy son genéricas.
2. **Es familiar, no estatal.** Da seguridad alimentaria a *un grupo familiar*: encaja con el
   evento `disputa_vecinos` («dos familias en conflicto por límites del conuco») y con la
   matrilinealidad del canon (§6) — ¿de quién es el conuco, de la línea materna?
3. **Quemar en un semiárido ventoso es peligroso.** Tala y quema + alisio constante = un riesgo
   real que la comunidad debe gestionar. **[reconstruido]**

---

## 7. Las salinas y el ciclo del *biro*

La sal (**biro**, caquetío atestiguado) es el bien estratégico del canon (§3). Su producción es
un fenómeno físico directo: en las **salinas costeras** el agua de mar queda estancada en charcas
someras y el sol más el viento la **evaporan** hasta dejar una costra de sal que se raspa a mano.
La salina viva más cercana y emblemática es **Las Cumaraguas**, en Paraguaná —depósito natural de
evaporación solar, cosecha artesanal heredada por generaciones, teñida de rosa por el alga
*Dunaliella*—; en la macroescala venezolana se le suman Araya (Sucre) y Los Olivitos (Zulia).
**[reconstruido — el proceso evaporítico es física elemental y la salina existe y opera así hoy,
pero la documentación consultada es periodística y describe una operación artesanal de ~80 años,
no una continuidad precolonial demostrada]**

La consecuencia para la simulación es que **el ciclo del biro está sincronizado con la seca**: es
el «Tiempo de Viento» (alisio fuerte + sol intenso + poca lluvia) el que seca las charcas y
permite la gran cosecha. El evento `gran_cosecha_sal` (estación=seca) y el `raspado_salinar`
descansan sobre este hecho evaporítico. El lexicón tiene **biro** (sal) y **borojo** («salina,
lago salado de Coro», atestiguado), pero no palabra para la **costra de sal** ni para el agua
**salobre** (§12).

---

## 8. El manglar del Golfete

El borde oeste del Golfete de Coro y el noreste de Paraguaná sostienen **manglares** —el único
bosque verdadero de este mundo semiárido—. Los estudios de suelos de la zona documentan el
**mangle rojo** (*Rhizophora mangle*, dominante y de mayor complejidad estructural en sectores
como Iguanita) y el **mangle negro** (*Avicennia germinans*, dominante en otros). Venezuela
cuenta con **cuatro especies de mangle** —rojo, negro, blanco (*Laguncularia racemosa*) y
botoncillo (*Conocarpus erectus*)—, todas esperables en este sistema. **[atestiguado]**

Ecológicamente el manglar es el **contrapunto húmedo y fértil** del matorral seco: guardería de
peces juveniles, banco de moluscos, refugio de aves acuáticas y migratorias, y fuente de madera
dura y medicina. Pero su función más útil para la simulación es **química**: la corteza del
mangle rojo es rica en **taninos (10–40 %)**, que sirven para curtir cueros y —sobre todo— para
**teñir y endurecer cuerdas, redes y sedales**. El mangle negro aporta ~12,5 % como colorante.
Es un enlace directo **manglar → pesca**: la red (*atara*) de Bagre-ko se trata con la corteza
del propio manglar. Además la corteza es cicatrizante, antiséptica y antidiarreica, y la madera
da carbón de alta calidad y postes. **El único bosque de este mundo es también su botiquín y su
ferretería.** **[atestiguado — etnobotánica de *Rhizophora* / *Avicennia*]**

El lexicón nombra el manglar genérico (**mankaba**) y el cangrejo (**ukura**), pero no distingue
las especies de mangle ni nombra la **raíz-zanco** que define visualmente el paisaje (§12).

---

## 9. Flora xerófila: vivir sin agua

Fuera del manglar, la vegetación es **xerófila**: plantas resistentes al déficit hídrico y a la
sal. La zona de vida es **monte espinoso tropical**. Dominan **cují yaque** (*Prosopis
juliflora*), **yabo**, **espinito**, **tunas**, **cardones** y cactus. **[atestiguado — Camacho
et al. 2011; caracterización del PN Médanos de Coro]**

La vegetación además **lee la duna**: Camacho et al. documentan que las crestas se cubren de cují
rastrero; los flancos, de gramíneas (*Aristida cognata*, *Sporobolus virginicus*); y las
depresiones interdunares —los «callejones»— de arbustos como *Acacia tortuosa*, *Lycium
tweedianum* y *Croton punctatus*. Cada parte del médano tiene su planta: un mapa botánico que un
recolector como Suba-ko leería como nosotros leemos un letrero.

El repertorio útil que el lexicón ya nombra es amplio: cardón (**coro / kadushi**, y su fruto
**caduchi**), dividivi (**watapana**, fuente de taninos también), cocuiza (**kukuisa**, agave de
fibra para cuerda), sábila (**rülipi**), y el cují/trupillo (**adoptivo**, forma hermana). Añádase
tuna, guamacho y guayacán. **[atestiguado]**

---

## 10. La fauna: ¿con quién compartían el mundo?

Esta es la capa que la primera versión del ensayo dejó como catálogo suelto y que aquí se trata
como lo que es: **una biología con estructura, y con una paradoja en el centro.**

### 10.1 La paradoja: un ecosistema terrestre pobre

El dato más importante sobre la fauna terrestre de este mundo es **cuán poca hay**. Las
caracterizaciones del Parque Nacional Médanos de Coro son explícitas: *«la fauna, así como la
vegetación, es escasa, principalmente debido a las condiciones extremas del clima desértico»*.
No es un bosque tropical rebosante: es un desierto costero con una nómina animal corta.
**[atestiguado]**

La consecuencia cultural es fuerte y **corrige por implicación al canon**: **la caza no puede ser
un pilar alimentario de la Curiana.** Un istmo semiárido no sostiene presión cinegética
suficiente para alimentar a un poblado. La caza es **complemento, prestigio y símbolo** —no
despensa—. La despensa real es **el mar** (§10.5), y en segundo lugar el conuco (§6). Esto
explica, retroactivamente, por qué la cultura caquetía que el canon describe es **marítima,
salinera y comerciante** en vez de cazadora: no fue una elección, fue lo único que la ecología
permitía. **[reconstruido]**

### 10.2 Mamíferos

La nómina de mamíferos del istmo y su entorno es corta y de talla pequeña-mediana
**[atestiguado — fauna del PN Médanos de Coro]**:

| Animal | Especie | Nota |
|---|---|---|
| **Zorro común** | *Cerdocyon thous* | El carnívoro del matorral; cazador nocturno |
| **Oso melero** | *Tamandua tetradactyla* | Hormiguero arborícola — come los bachacos (**koke**) |
| **Conejo sabanero** | *Sylvilagus floridanus* | Presa menor accesible y frecuente |
| **Mapurite** | *Conepatus semistriatus* | Mofeta; presencia inconfundible por el olor |
| **Rabipelado** | *Didelphis marsupialis* | Zarigüeya; carroñero y merodeador de conucos |
| **Venado caramerudo** | *Odocoileus virginianus* | **tara** en el lexicón — ver §10.6 |

Nótese lo que **no** hay: ni jaguar, ni danta, ni grandes herbívoros de manada. El **kama**
(tapir/danta) del lexicón atestiguado **no es fauna local**: es animal de tierra firme húmeda, y
si la palabra existe en caquetío es por el alcance de la red de contacto, no por el patio de casa.
El **kabadaro** (jaguar) del lexicón es forma hermana wayunaiki, no un vecino del istmo.

### 10.3 Reptiles: los verdaderos dueños del desierto

Donde los mamíferos escasean, los reptiles dominan — es la firma de todo ecosistema árido. En
Falcón se registran **cascabel** (*Crotalus durissus*), **coral**, **mapanare**, **tigra
cazadora**, **lagartijo**, **mato real**, **tortuga mordelona** e **iguana** (*Iguana iguana*,
**iwana**), además del **tuqueque** (gecko) que el lexicón ya nombra. Las cascabeles habitan
específicamente las zonas de laguna entre cardones, acacias, cujíes y guayacanes. La región
alberga incluso **el lagarto más pequeño del mundo** (3–5 cm). **[atestiguado]**

Para la simulación esto importa por dos vías: **la iguana es proteína real y accesible** (a
diferencia del venado), y **las serpientes venenosas son una amenaza cotidiana** — lo que da
sentido material al *urari* (veneno-medicina) del piache y a la farmacopea de Paugis-sha. El
miedo a la mordedura es el miedo mejor fundado de este paisaje. **[reconstruido]**

### 10.4 Aves: la excepción abundante

Contra la pobreza mamífera, **las aves son el gran espectáculo biológico** de este litoral. El
análogo protegido más cercano —el Refugio de Fauna Silvestre Cuare, primer humedal Ramsar de
Venezuela, en el mismo estado Falcón— reúne **más de 350 especies** y concentra el **79 % de las
familias de aves acuáticas del país**. Destacan **flamenco** (*Phoenicopterus ruber*), **corocora
roja** (*Eudocimus ruber*), garzas (real, paleta, morena), playeros migratorios, patos y gaviotas.
**[atestiguado para Cuare; reconstruido como análogo del Golfete]**

En las islas, la arqueología documenta colonias de **bobas** (*Sula* sp.) sobre suelos de
**guano** (Antczak & Antczak 2015). Y el lexicón conserva un núcleo de aves con carga simbólica:
**chiriguare** (gavilán), **warawara** (zamuro), **pauji**, **chuchubi** (sinsonte), **tokoko /
chogogo** (flamenco).

Las aves son, además, **un reloj y un oráculo**: la llegada estacional de migratorias marca el
año, y el comportamiento de las aves marinas delata dónde está el pescado — el canal perfecto
para que el medio «hable» sin hablar (ver anexo).

### 10.5 El mar: la despensa verdadera

Aquí está la abundancia que la tierra niega. Las aguas someras, los manglares y el Golfo de
Venezuela sostienen **pargo** (*Lutjanus*), **corvina** (*Cynoscion*), **mero**
(*Epinephelus*), **róbalo** (*Centropomus*), **lisa** (*Mugil*), **sábalo**, **jurel**,
**corocoro**, **sardina**, **cazón**, y el **bagre marino** (*Bagre marinus* / *Arius*); en aguas
más profundas, el **cunaro** (pargo de altura, *Rhomboplites aurorubens*). **[atestiguado]**

Y por encima de los peces, la megafauna: **manatí** (*Trichechus manatus*, **manatü** —
literalmente «vaca marina del golfete» en el lexicón), **delfines**, **tiburones** (**kanawari**)
y **cuatro especies de tortuga marina** —verde, carey, cardón y cabezón—. La arqueología insular
confirma el consumo intensivo de tortuga (223 restos en un solo sitio, con las cabezas cortadas
y descartadas fuera del yacimiento) y del **botuto** o caracol reina (*Lobatus gigas*, **cobo**),
en densidades altísimas. Súmense quiguas (*Cittarium pica*), cangrejos (**ukura**) y la **ostra
perlífera**, que produce la **tüma** (perla) del comercio de prestigio. **[atestiguado — Antczak
& Antczak 2015]**

**El contraste es la tesis biológica de esta sesión:** un mundo terrestre pobre junto a un mar
riquísimo. Toda la cultura caquetía —canoas, redes, buceo, sal para conservar el pescado, rutas
a las islas, y un dueño espiritual del mar al que hay que pedir permiso— es la respuesta lógica a
ese desequilibrio. Bagre-ko no es supersticioso por folclore: reza al único proveedor fiable que
tiene.

### 10.6 Advertencia: la fauna de hoy no es la de entonces

**Este es el matiz que corrige la licencia del §2.** La geomorfología y el clima del s. XV son
los de hoy; **la fauna no**. El **venado caramerudo** (*Odocoileus virginianus*) —el **tara** del
lexicón caquetío atestiguado— hoy **está ausente de gran parte del estado Falcón**, y la causa
documentada es la **caza indiscriminada y sistemática moderna**, que ha desplomado sus
poblaciones en toda Venezuela. **[atestiguado]**

Es decir: **que el caquetío tuviera una palabra propia y atestiguada para el venado es evidencia
de que el venado estaba ahí.** La lengua conserva el testimonio de una fauna que la escopeta
borró. Por tanto:

- **Proyectar la fauna actual hacia atrás subestima el mundo animal caquetío.** El istmo del s. XV
  era pobre en fauna *por el clima*, pero **menos pobre que el de hoy**, que además está
  empobrecido *por el hombre*.
- **Regla de método para el corpus:** cuando el lexicón atestiguado nombra un animal que hoy
  falta localmente (como *tara*), **la palabra pesa más que el censo moderno**. El vacío es
  reciente. **[reconstruido]**

---

## 11. Lo que la tierra da: cerámica y madera

### 11.1 La tradición dabajuroide

La cerámica no es un detalle decorativo: es el **marcador arqueológico** que identifica al pueblo
caquetío. La **serie Dabajuroide**, originaria de la costa occidental de Falcón, se distribuye por
todo el estado y hasta las Antillas Neerlandesas (ABC), cubriendo ~1 300 km de litoral; se fecha
c. **800–1600 d.C.** y está directamente correlacionada con **una única unidad étnica y
lingüística: el caquetío** (Atlas del Arte Precolombino Venezolano; Antczak & Antczak 2015).
**[atestiguado]**

Sus rasgos —vasijas polícromas pintadas sobre **engobe blanco**, vasijas efigie, formas
trípodes/multípodes con base anular calada, **bases redondas impresas con tejido de algodón** que
dejó su huella al desintegrarse la fibra, y urnas funerarias globulares y cilíndricas con tapa
cónica que modela figuras humanas— implican una cadena técnica concreta para las alfareras del
elenco (Saruro-sha, Cahu-sha, Pira-sha). En su forma general esa cadena es: arcilla amasada y
**desgrasada con arena de barranco libre de sales** (evita grietas al secar y cocer);
construcción por **urdido** (culebrillas superpuestas — justo como el canon ya lo narra); acabado
con **engobe** blanco; y **cocción a fuego abierto**. En un entorno salino, *la calidad de la
arena importa*: un detalle que una alfarera experta vigilaría. **[atestiguado / reconstruido]**

### 11.2 El taller de canoas: el problema de la madera

La locación `taller_canoas` y el oficio de Dara-ko plantean una pregunta que el canon nunca hace:
**¿de qué madera?** La canoa caribeña de un solo tronco se labraba tradicionalmente en **cedro
rojo** (*Cedrela odorata*), **caoba** (*Swietenia*) o **ceiba** (*Ceiba pentandra*), ahuecando el
tronco **con fuego, sin instrumentos de hierro**; los saberes indígenas de canoa incluyen la
**clasificación de las maderas por peso y dureza**. **[atestiguado]**

Y aquí surge una inferencia con consecuencias: **cedro, caoba y ceiba no son árboles del cardonal
espinoso.** El monte espinoso tropical de Coro produce cují, yabo, dividivi y cardón — leña,
fibra, tanino y postes, pero **no troncos de diez metros**. De modo que la madera de las canoas
grandes **tuvo que venir de fuera**: de bosques de galería en los cauces, de la sierra, o por
intercambio. **[reconstruido]**

Esto tiene tres efectos narrativos que la simulación puede usar tal cual:

1. **La canoa es un objeto de importación y, por tanto, de valor.** Dara-ko no trabaja un material
   abundante: trabaja un bien escaso y viajado.
2. **Enlaza `taller_canoas` con la red de comercio** (Nabaraka el Jirajara baja de la sierra) y
   con `camino_islas`: sin madera foránea no hay travesía a Aruba.
3. **El fuego es la herramienta,** no el hierro — coherente con el horizonte tecnológico del s. XV
   y con el evento de construcción de canoas.

---

## 12. Los huecos léxicos: dónde la simulación puede crear lengua

Cruzar el paisaje real con el lexicón revela vacíos sistemáticos. Son el hallazgo más útil de esta
sesión, porque marcan **dónde un piache, un pescador o una alfarera tendrían presión real para
acuñar una palabra** (morfología disponible: locativos `-ana/-bana`, agentivos `-ko/-sha`,
posesivos `ta-/wa-/nü-`). Los principales:

- **La duna / el médano.** El accidente que *define* el territorio no tiene palabra. (Cuidado con
  el falso amigo: `duna` en el lexicón significa **agua**, no médano.) Ni la duna viva ni la
  fijada tienen nombre caquetío.
- **El cardumen / banco de peces** — el objeto del oficio de Bagre-ko, y sin embargo mudo.
- **El alisio** como entidad nombrada, distinta del genérico *joutai* (§4).
- **Los peces cunaro, guaranaro y bagre** — usados como nombres de agentes, no lexicalizados como
  especies.
- **La marea** — figura como concepto en los prompts pero no como lexema (y el Golfete tiene marea
  real, semidiurna, de ~50 cm).
- **El agua salobre / el salitre** y la **costra de sal**.
- **La quebrada / arroyo efímero** — el cauce que solo corre tras la lluvia. Hay formas hermanas
  (*luwopu* lokono, *laa* wayuu) pero ninguna caquetía ni ninguna que capture *lo efímero*.
- **El istmo / la lengua de arena** que une Paraguaná al continente.
- **La raíz-zanco del mangle** y la **diferencia mangle rojo / negro**.
- **La avifauna del humedal** (corocora, garzas, playeros) y la **ostra perlífera** (el molusco;
  la perla sí tiene nombre, *tüma*).
- **La madera de canoa foránea** (§11.2) — el material más valioso del taller no tiene nombre
  propio.

Cada uno de estos vacíos es una invitación: no un error del lexicón, sino **espacio de diseño**
para que la lengua siga construyéndose, como el propio canon (§5) afirma que debe ocurrir. El
mapa completo, entrada por entrada, está en `curiana_sim/cultura/ecologia_lexicon_map.md`.

---

## 13. Decisiones de diseño para la simulación

1. **Dar sustancia ecológica a cada locación.** El corpus enlaza cada locación (`orilla`,
   `manglar`, `salinar`, `conuco`, `buco`, `matorral`, `taller_canoas`, `camino_islas`, `bohios`)
   con especies, procesos y estacionalidad reales, para que los prompts de escena dejen de ser
   genéricos.
2. **Anclar los eventos ambientales existentes en su causa física.** `gran_cosecha_sal` ↔
   evaporación de la seca; `crecida_buco` ↔ pulso de lluvias oct–dic sobre cauces efímeros;
   `expedicion_perlas` / `watapana_parte_islas` ↔ agua clara y alisio de la seca. Ningún evento
   nuevo se inventa; se les da fundamento.
3. **Corregir el peso de la caza.** La fauna terrestre es escasa (§10.1): la caza debe leerse como
   **complemento y prestigio**, no como despensa. El mar y el conuco alimentan a la Curiana. Si
   alguna escena presenta la caza como fuente principal de comida, contradice la ecología.
4. **No proyectar la fauna moderna hacia atrás** (§10.6). Cuando el lexicón atestiguado nombra un
   animal hoy ausente (*tara*), la palabra manda sobre el censo actual.
5. **Tratar los huecos léxicos como oportunidades, no como deudas.** No se debe «rellenar» el
   lexicón a mano: el valor del experimento es que **emerjan** en boca de un agente cuando la
   escena lo empuje. El corpus los marca con `hueco_lexico: true` para que el diseño los conozca.
6. **Sincronizar clima → recurso → tensión.** La cadena real (estación → alisio → evaporación /
   cardúmenes / lluvia → abundancia o escasez → tensión social) sugiere sustituir el catálogo
   estático de eventos por un motor ambiental dinámico (anexo; spec en
   `investigacion/disenos/02_motor_ambiental.md`).

---

## Anexo — Agentes ecológicos: el Golfete, el viento y el manglar como actores

**Idea.** Hoy `curiana_state.py` dispara eventos ambientales de un catálogo fijo
(`EVENTOS_COTIDIANOS`, `EVENTOS_ESTACIONALES`). La propuesta —**solo conceptual, no
implementar**— es modelar el medio como un pequeño elenco de **agentes ecológicos**: el
**Golfete**, el **Alisio**, el **Manglar**, el **Salinar**, el **Buco**. No son personajes que
hablan: son procesos con estado que evoluciona. Su regla de oro es que **su «voz» nunca llega
como dato crudo al agente humano**, sino solo por **canales culturalmente verosímiles**.

**Tres capas.** Cada señal ecológica se traduce en cascada:

1. **Hecho ecológico** (estado del agente ambiental): el Alisio arrecia → el Golfete se pone claro
   y frío → los cardúmenes de cunaro se mueven a los bajíos del norte.
2. **Experiencia de los agentes humanos** (lo único que perciben): la pesca de Bagre-ko cae tres
   días seguidos en el sitio de siempre; el agua sabe distinta; **las bobas vuelan hacia el
   norte** (§10.4 — las aves son el mejor canal: delatan el pescado sin explicarlo).
3. **Interpretación religiosa/cultural** (lo que dicen y hacen): Shaboro sueña que el dueño del
   mar «se llevó los peces»; se lee como presagio; se ofrenda *sakana*; se acusa a un mal ritual o
   a un *wanülüü*. La causa física real (el viento movió el cardumen) **nunca se enuncia**: emerge
   como teología y como tensión social (los Guaycarí culpan al calor, los caquetíos al ritual —
   como ya ocurre en el evento `pesca_mala`).

**Del catálogo estático al motor dinámico.** En vez de elegir un evento de una lista, el motor
correría una cadena causal cada turno:

```
estación → intensidad del alisio → claridad/temperatura del Golfete
        → posición de los cardúmenes → resultado de pesca
        → nivel de alimentos → nivel de tensión
        → probabilidad de sueño/presagio del piache
```

Y en paralelo: `pulso de lluvia (oct–dic) → nivel del buco → estado de los conucos → cosecha`;
`sol+viento de la seca → costra del salinar → cosecha de biro → poder redistributivo de Manaure`.
Los «eventos» actuales dejarían de ser tarjetas fijas y pasarían a ser **lecturas del estado del
motor** al cruzar un umbral.

**Por qué importa para el experimento lingüístico.** Un entorno que *empuja* —un cardumen que se
fue y no tiene nombre, un médano nuevo que el viento levantó anoche, una costra de sal que hay que
describir— es precisamente el tipo de presión comunicativa bajo la cual las lenguas naturales
acuñan palabras. Los **huecos léxicos** del §12 dejan de ser una lista y se vuelven **situaciones
jugables**: el motor ambiental crea la necesidad, y la lengua responde. El Golfete, así, no habla
caquetío —pero es la razón por la que el caquetío crece.

---

## Bibliografía

- **Camacho, R., Salazar, S., González, L., Pacheco, H. & Suárez, C. (2011).** «Caracterización
  geomorfológica de las dunas longitudinales del Istmo de Médanos, estado Falcón, Venezuela».
  *Investigaciones Geográficas, Boletín del Instituto de Geografía, UNAM*, núm. 76, pp. 7–19.
  [Geografía física, clima, dunas, paleogeografía, flora de dunas e hidrología costera. PDF leído
  en `fuentes_caquetios/`.]
- **Antczak, M. M. & Antczak, A. (2015).** «Late Pre-Colonial and Early Colonial Archaeology of
  the Las Aves Archipelagos, Venezuela». *Contributions in New World Archaeology* 8, pp. 1–37.
  [Navegación insular, cerámica dabajuroide, botuto (*Lobatus gigas*), tortugas, bobas/guano,
  pesca de perlas. PDF leído en `fuentes_caquetios/`.]
- **Atlas del Arte Precolombino Venezolano** — «Serie Dabajuroide». [Cronología (800–1600 d.C.),
  distribución y rasgos; correlación con el caquetío.] <https://atlasprecolombino.com/estilo/serie-dabajuroide/>
- **Inparques / caracterizaciones del Parque Nacional Médanos de Coro.** [Zona de vida (monte
  espinoso tropical), flora xerófila, nómina de mamíferos, escasez faunística.]
- **Refugio de Fauna Silvestre Cuare (Falcón), sitio Ramsar (1988).** [Avifauna del humedal
  falconiano: >350 especies, 79 % de familias acuáticas; flamenco, corocora, garzas, playeros.]
- **Parque Nacional Morrocoy (Falcón).** [Tortugas marinas (verde, carey, cardón, cabezón),
  delfines, ictiofauna costera; las cuatro especies de mangle de Venezuela.]
- **Literatura sobre el conuco indígena** (p. ej. Wataniba, *El conuco indígena: más que una
  parcela agrícola*). [Lógica ecológica del conuco: perturbación y sucesión, cenizas, policultivo,
  seguridad alimentaria familiar.]
- **Fuentes sobre agricultura caquetía y el sistema de riego *buco*** del río Coro y el Valle del
  Turbio. [Maíz, yuca, batata; riego atestiguado con nombre propio.]
- **Etnobotánica y farmacología de *Rhizophora mangle* / *Avicennia germinans*.** [Taninos
  (10–40 %), curtido y tinción de redes, usos medicinales y madereros.]
- **Fuentes sobre construcción indígena de canoas** (cedro, caoba, ceiba; ahuecado con fuego).
- **Datos climáticos e hidrológicos de Coro y del río Mitare**; **estudios de corrientes y
  transporte de sedimentos en la boca del Golfete de Coro** (marea semidiurna ~50 cm, corrientes
  ~1 m/s por la tarde, barra de Punta Caimán).
- **Ictiofauna del Golfo de Venezuela / La Vela de Coro** (FAO, SVDB). [Pargo, corvina, mero,
  róbalo, bagre marino; *cunaro* = *Rhomboplites aurorubens*.]
- **Fuentes del lexicón para nombres de especies:** Alvarado, L. (1921), *Glosario de voces
  indígenas de Venezuela*; Jahn, A. (1927), *Los aborígenes del occidente de Venezuela*; Zavala
  Reyes (2015). [Ya integradas al lexicón; los PDFs en `fuentes_caquetios/` son escaneos de imagen
  sin capa de texto — ver hoja de fuentes.]

> **Nota sobre una fuente prevista y no disponible:** `Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf`
> figura en `fuentes_caquetios/` pero está **vacío (0 bytes)**. La caracterización de la cerámica
> dabajuroide se apoya, en su lugar, en el Atlas del Arte Precolombino Venezolano y en Antczak &
> Antczak (2015). Ver la hoja de fuentes para el detalle.
