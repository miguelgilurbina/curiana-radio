---
tipo: hoja-de-fuentes
sesion: 1/4
moc: MOC_familia
---

# Hoja de fuentes — Sesión 1/4: ¿Cómo era la familia caquetía?

> [[MOC_familia]] · [[01_familia_caquetia|ensayo]] · [[INDICE_FUENTES]]
> Fuentes: [[oliver-1989-cap3]] · [[oliver-1989-cap2]] · [[jahn-1927]] · [[arcaya-1920]] · [[adam-1879]] · [[keegan-1989]] · [[las-casas-1875]] · [[oviedo-y-banos]]

## Corrección post-entrega (feedback de Miguel)

Primera versión de este ensayo presentaba la sucesión patrilineal de Oliver 1989 (cap. 3) como dato
`atestiguado` en pie de igualdad con la matrilinealidad `reconstruido` del canon, y proponía "mantener
la tensión activa" entre ambas. Miguel señaló el error: ese dato es de la administración **colonial**
del cacicazgo de Coro (siglos XVI-XVIII, ya bajo probanzas, encomienda y categorías jurídicas
españolas), no del **precontacto** (siglos XIV-XV) que el proyecto reconstruye — exactamente la
distinción que el propio preámbulo de `CULTURA_CAQUETIA.md` ya advierte no pasar por alto ("las
crónicas describen a los Caquetíos ya en contacto... no en su vida cotidiana intacta").

Se corrigió: el ensayo (§1) y `parentesco.yaml` (entradas 001-003, 015) ahora marcan explícitamente que
el registro patrilineal es dato del cacicazgo colonial, útil solo como semilla narrativa para una
posible línea futura sobre la deformación del cacicazgo tras el contacto — no como norma precontacto
en competencia con la matrilinealidad. La lectura de síntesis pasó de "tensión sin resolver" a
"precontacto = matrilineal, sin ambigüedad", con el dato de Oliver reencuadrado como evidencia de
*otra cosa* (cuán fuerte era la lógica matrilineal, que incluso se filtra y genera fricción dentro del
propio registro colonial). La poligamia de Manaure (parentesco-015) sí se mantuvo como dato utilizable,
porque el canon ya decide explícitamente "proyectar hacia atrás" ese rasgo del Manaure histórico de
contacto — una decisión de diseño ya tomada, distinta de tratar sin más un dato colonial como si fuera
precontacto.

**Lección para las sesiones 2-4 del programa**: revisar con la misma vara cualquier dato "atestiguado"
que venga de crónicas — preguntar primero si describe el precontacto que se está modelando o el
período de contacto/colonial, y solo tratarlo como norma precontacto directa si el propio canon ya
decidió proyectarlo hacia atrás a propósito (como con Manaure y las tormentas/poligamia).

## Qué se buscó

1. Instituciones familiares caquetías atestiguadas en crónicas y trabajo académico (matrimonio,
   sucesión, residencia, poligamia, clanes).
2. Sistema de clanes matrilineales wayuu (*e'irüku*) y avunculado, como comparanda arahuaca principal.
3. Terminología de parentesco arahuaca atestiguada o reconstruible, cruzada contra
   `curiana_lexicon.py` y `lexicon_candidatos.py`.
4. Casos de sucesión de cacicazgos en las crónicas coloniales de Coro/Paraguaná.
5. Relaciones familiares ya implícitas en `curiana_agents.py` (leído completo, línea por línea, antes
   de proponer nada nuevo).

## Qué se encontró (con ubicación exacta)

### Fuentes primarias (PDFs, `fuentes_caquetios/`)

Extraje a texto plano con `pypdf` (no hay OCR de por medio para los PDFs con capa de texto) los
siguientes archivos completos, guardados temporalmente en el scratchpad de la sesión (no en el
repositorio): `Chapter 2 Linguistics- Oliver 1989.pdf` (109 pp.), `Chapter 3 Ethnohistory.DOC-
comprimido.pdf` (113 pp.), `Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf` (519 pp. — nota: el
archivo pedido en las instrucciones, `Oviedo_Banhos_1885_Conquista_Venezuela.pdf`, existe en la
carpeta pero pesa 0 bytes/está corrupto; usé en su lugar
`Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf`, que sí tiene contenido y es presumiblemente la
misma obra con nombre de archivo distinto — **no llegué a buscar en él por agotamiento de tiempo de
sesión, queda abierto**), `Las_Casas_1875_Historia_Indias_vol1.pdf` (613 pp.), `Jahn_1927_Aborigenes_
Occidente_Venezuela.pdf` (510 pp.), `Arcaya_1920_Historia_Estado_Falcon.pdf` (348 pp.).

- **Oliver 1989, cap. 3 (Ethnohistory)** — la fuente más productiva con diferencia. Hallazgos clave:
  - p. 268: *"the office of chief or diao was in the XVIth century inherited by the son of the
    diao"* — sucesión patrilineal atestiguada del cacicazgo de Coro, **en tensión con la
    matrilinealidad ya asumida en CULTURA_CAQUETIA.md §6**. Ver ensayo §1 para el tratamiento
    completo de esta tensión (no la escondí ni la resolví de forma forzada).
  - pp. 255-256: sucesión documentada Manaure→Don Alexandre (hijo); Don Sancho Uriacoa→Don Luis
    Caguallo (hijo)→Don Luis Martínez Manaure (hermano, "abdicación" 1636)→hijo mayor; conflicto de
    "bastardía" en Paraguaná (s. XVIII) ligado a la identidad de la madre, citando a Martí 1969.
  - pp. 260-262: poligamia atestiguada de Manaure ("the only cacique unambiguously cited to be
    polygamous"), matrimonios con "hijas de los caribes", y el caso ambiguo de la viuda de Manaure
    que "se casa" con quien las crónicas llaman su hijo — Oliver mismo anota la duda "carnal or
    classificatory?" (p. 262). Esta duda es la base textual de la propuesta de sucesión avuncular
    de este ensayo.
  - p. 190, nota 4: el término correcto del clan wayuu no es "clan" sino *eirrüku* o *apüshi*
    (citando Goulet 1981).
  - pp. 269-270: los poblados tenían un "lesser principal chief, who probably was the head of a
    lineage group" — linaje como base de la jefatura local; contraste explícito entre los caquetíos
    costeros (el modelo de la Curiana) y los del interior (Barquisimeto/Yaracuy), donde las viviendas
    tipo maloca alojaban familias extendidas de 40-50 personas — **un dato que NO debe importarse sin
    más a la Curiana costera**, porque el propio Oliver los distingue.

- **Oliver 1989, cap. 2 (Linguistics)** — un hallazgo puntual pero valioso: p. 147, el término
  caquetío atestiguado **daitiao**, cognado de taíno *daitia-o* y lokono *da-tti/da-iti*, raíz de
  parentesco /-atti-/. No está en `curiana_lexicon.py`; queda señalado como candidato de incorporación
  futura (parentesco-012). El resto del capítulo es principalmente léxico comparativo general
  (numerales, términos básicos), sin más contenido de parentesco directamente aprovechable; la
  extracción del PDF tiene un artefacto de formato (palabras una por línea en varios tramos) que hice
  legible re-uniendo líneas con un script, pero no invertí tiempo en reconstruir tablas completas de
  vocabulario más allá de lo citado.

- **Jahn 1927** — la extracción de texto de este PDF es de calidad OCR desigual (el volumen es un
  escaneo antiguo; el frontispicio y las primeras páginas salen prácticamente ilegibles), pero el
  cuerpo del texto es utilizable. Hallazgos:
  - p. 172: matriarcado guajiro explícito ("la herencia del nombre y nacionalidad materno constituían
    un definido matriarcado"), exogamia de clan, declive de ambas costumbres para 1927.
  - pp. 172-173: levirato — la viuda pasa al hermano menor del difunto, o a un sobrino si no hay
    hermanos.
  - p. 171: insultar a un muerto delante de un tío o sobrino, ofensa gravísima.
  - pp. 438-439: tabla comparativa de términos de parentesco guajiro/paraujano (tío materno vs. tío
    paterno como entradas léxicas separadas). **Advertencia metodológica importante:** la extracción
    del PDF desalinea las dos columnas (español/guajiro) entre saltos de página, así que **no
    reconstruí las formas léxicas exactas** palabra por palabra — el riesgo de emparejar mal una
    palabra guajiro con el glosario español equivocado era demasiado alto para una cita que se
    presenta como `reconstruido`. Cito solo el patrón estructural (bifurcación léxica materno/paterno),
    que es robusto incluso con las columnas desalineadas. **Queda abierto**: alguien con acceso al PDF
    original (no solo el texto extraído) podría re-verificar esa tabla palabra por palabra para una
    sesión futura.
  - Nota: en el mismo volumen hay un bloque de vocabulario de parentesco con prefijos posesivos
    (*t-eúp* "mi sobrino", *p-eúp* "tu sobrino", *n-eúp* "su sobrino", *w-eúp* "nuestro sobrino",
    alrededor de p. 456) que **no until pertenece al wayuu ni al caquetío** — por el contexto de la
    sección y el patrón fonológico (prefijos *ki-/kiu-*, "taita" para padre) es casi con certeza
    vocabulario jirajara/ayamán u otra lengua macro-chibcha de la sierra. Lo dejo fuera de las
    comparandas arahuacas de este ensayo; podría ser útil para la categoría `jirajaroide-contacto` ya
    existente en `curiana_lexicon.py`, pero eso es trabajo de código fuera del alcance de esta sesión.

- **Arcaya 1920** — pp. 127-128: reconocimiento honesto de que los cronistas no dicen nada directo
  sobre instituciones familiares de los indios de Coro; poligamia inferida por analogía a los pueblos
  del Casanare y el Meta; bodas cacicales con grandes fiestas; sugerencia (no desarrollada) de que las
  diferencias de tatuaje podrían marcar clanes en vez de solo rango.

- **Las Casas, *Historia de las Indias*, tomo I** — búsqueda dirigida por patrones
  ("sobrino...cacique", "cacicazgo", "hereda...cacic") sin resultados relevantes. Es esperable: el
  tomo I cubre sobre todo Antillas/Colón y termina antes del período en que Ampíes funda Coro
  (1527) — la sucesión cacical de Coro que documenta Oliver viene de fuentes de archivo (probanzas,
  Bishop Martí), no de Las Casas. No revisé los tomos II-V (no están en `fuentes_caquetios/`).

- **`Oviedo_Banhos_1885_Conquista_Venezuela.pdf`** — el archivo listado en las instrucciones de la
  sesión existe pero tiene 0 bytes (corrupto o placeholder nunca completado). Usé en su lugar
  `Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf`, presente en la misma carpeta, pero **no alcancé a
  revisarlo** por límite de tiempo de la sesión — queda como pendiente explícito para la próxima
  sesión del programa o para retomar esta si Miguel lo pide.

### Fuentes secundarias (WebSearch)

Dos búsquedas dirigidas:

1. *"wayuu e'iruku clanes matrilineales sistema avunculado sobrino herencia"* — confirmó el cuadro ya
   sugerido por Jahn 1927 con lenguaje más moderno: clanes *e'irüku* con tótem/territorio propio; el
   tío materno como máxima autoridad familiar (representa al grupo en pagos por ofensas y dotes); los
   sobrinos —no los hijos— heredan bienes, prestigio y poder. **Advertencia**: son fuentes web
   generales (blogs culturales, portales de turismo, un PDF de trabajo universitario sin verificar en
   profundidad), no monografías antropológicas revisadas por pares. Las traté como
   `reconstruido`/comparanda de apoyo, no como fuente de la misma categoría que Oliver o Jahn —
   consistente con degradar a la etiqueta más débil en caso de duda.
2. *"Arawakan matrilineal kinship cacicazgo succession sister's son northern South America
   chiefdoms"* — confirmó para los taínos (la otra comparanda arahuaca central del proyecto) el mismo
   patrón: sucesión por línea femenina, preferentemente de hermano a hermana a sobrino, permitiendo
   cacicas mujeres. Mismas reservas metodológicas que arriba (fuentes generalistas, no monografías).

## Segunda ronda (2026-07-16): comparanda arahuaca ampliada + linajes como unidades de expansión

Miguel pidió tres cosas: (1) tratar la decisión genealógica como la que determina qué grupos
familiares se agregarán al expandir el elenco, (2) comparar la estructura familiar con otras
sociedades de herencia arahuaca más allá de wayuu/taíno, y (3) cerrar la descripción en un punto
coherente pero intuitivo.

Búsquedas nuevas (WebSearch, fuentes secundarias — misma reserva metodológica que la primera ronda):

1. *"Lokono Arawak social organization kinship matrilocal residence Guianas ethnography"* — los
   arawak costeros de las Guayanas: clanes matrilineales exógamos, residencia matrilocal, sucesión
   tío→sobrino o entre hermanos por línea materna. Cierra el arco norteño por el este.
2. *"Baniwa Curripaco northwest Amazon Arawak patrilineal phratries sibs exogamy social
   organization"* — el contraejemplo deliberado: los arahuacos del río Içana son PATRILINEALES
   (fratrias exógamas de sibs jerarquizados por hermanos-espíritu ancestrales). Prueba que "arahuaco"
   no implica matrilineal; la analogía debe restringirse al arco norteño-costero. Registrado como
   entrada de control metodológico (parentesco-024).
3. *"Achagua llanos Colombia Venezuela organización social matrilineal parentesco etnografía
   arawak"* — el hallazgo más útil de la ronda: linajes totémicos de animal (serpiente, murciélago,
   jaguar, zorro), cada uno con SU PROPIA CASA COMUNAL en la aldea; exogamia; poligamia con esposas
   jurídicamente iguales (cada una con conuco propio); hogar extenso con hijas casadas residiendo.
   Además se verificó en el texto extraído de Oliver (cap. 3, pp. 287-288) el vínculo
   achagua-caquetío vía *mude* → *tamude* ("primos"), citando Jahn 1927: 213 — lo que sube a los
   achagua a comparanda de primer orden: son los parientes que las propias fuentes del proyecto
   declaran primos. También conecta con Arcaya 1920: 127-128, que infería la poligamia caquetía
   precisamente "al estilo de sus afines de Casanare y el Meta" (= los achagua).

Cambios producidos: ensayo §2 ampliado con subsección "El abanico arahuaco completo"; ensayo §5.1
reencuadrado (linajes = unidades de expansión, con la imagen achagua de linaje-casa-comunal); nueva
sección §6 "Cierre: retrato de una familia de la Curiana" (síntesis intuitiva en prosa, estilo del
"día típico" del canon §4); `parentesco.yaml` +5 entradas (021-025); `genealogia.yaml` con
`capacidad_de_expansion` por linaje y vías de entrada de linajes nuevos.

## Tercera ronda (2026-07-16): taínos y kalinago en profundidad

Miguel pidió profundizar específicamente las dos comparandas antillanas: taínos, y kalinago/caribes.

1. *"Taíno kinship matrilineal avunculocal residence Keegan cacique succession..."* (WebSearch) — el
   hallazgo central es la existencia de **Keegan 1989, "The Evolution of Avunculocal Chiefdoms"
   (American Anthropologist 91(3))**: residencia avunculocal de élite (el sobrino-heredero vive con o
   junto al tío materno; el tío introduce a los varones a las sociedades masculinas), sucesión por
   hijos de la hermana salvo derecho propio por el linaje de la madre, poliginia cacical de hasta 30
   esposas, cacicas mujeres. **Advertencia**: identificado vía resúmenes de búsqueda; el paper no se
   leyó en texto completo — si el corpus taíno va a crecer en sesiones futuras, conseguir el PDF de
   Keegan 1989 (y su libro *Taíno Indian Myth and Practice*) sería la mejor inversión de fuentes.
2. *"Kalinago island carib social organization matrilocal..."* (WebSearch) — sociedad matrilineal;
   esposas cautivas de raids; matiz moderno importante: el "lenguaje de los hombres" se entiende hoy
   más como pidgin comercial con los kalina continentales que como prueba literal de conquista +
   rapto, y los kalinago como población de origen arahuaco de larga duración. La búsqueda no confirmó
   detalles de casa de hombres (karbet) ni matrilocalidad residencial específica — no se afirmaron en
   el corpus.
3. **Adam 1879 (`fuentes_caquetios/Adam_1879_Parler_hommes_femmes_langue_caraibe.pdf`, 27 pp.)** —
   extraído completo a texto y leído por pasajes. Rinde: cita de Labat sobre los dos registros;
   cuantificación (~400 pares léxicos de un vocabulario de 2-3 mil, doble serie de prefijos
   pronominales, doble verbo negativo — pp. 275-277); la explicación de los capitanes caribes a
   Breton (conquista galibi, muerte de los hombres arahuacos, toma de las mujeres, "por eso el habla
   de las mujeres es conforme en algunas cosas a la de los Arrouagues del continente") y la
   validación comparativa del propio Adam (pp. 300-302). Primera vez que esta fuente del repositorio
   se usa para el programa cultural; ya alimentaba el lexicón (baruwa/hiñaru vía Breton 1665).

Cambios producidos: ensayo §2 con dos subsecciones nuevas ("Taíno: el espejo de élite" y "Kalinago:
el espejo invertido"), párrafo del abanico ajustado (kalinago dentro del arco matrilineal norteño);
`parentesco.yaml` +3 entradas (026-028); nota avunculocal en la entrada de Waimo-ko en
`genealogia.yaml` (ubicacion_default natural: casa_cacique); bibliografía ampliada (Keegan 1989,
Adam 1879).

## Cuarta ronda (2026-07-16): el conflicto Curiana-Caribe como choque de ideologías familiares

Miguel propuso una lectura propia: que los dos polos de ideación familiar identificados en la ronda
anterior (matrimonio-alianza caquetío vs. matrimonio-captura kalinago) podrían ser precisamente la
causa de los conflictos entre ambos pueblos, no solo un dato etnográfico paralelo.

Una búsqueda de verificación (WebSearch) reforzó la base fáctica más de lo esperado: *"Carib raiding
warfare women capture bride Antilles Taino Arawak ethnohistory conflict marriage"* devolvió que la
expansión caribe hacia las Antillas Menores se describe en la literatura secundaria como un proceso
**activo durante todo el siglo XIV** (no solo un mito de origen distante), con el mismo patrón que
recoge Adam 1879: matar a los hombres, capturar a las mujeres como esposas, y de ahí el mismo
fenómeno lingüístico (mujeres capturadas hablando arahuaco dentro de comunidades de habla caribe).
Esto es relevante porque el siglo XIV es exactamente donde arranca la cronología de la simulación —
no es dato de un pasado remoto sino de la generación inmediatamente anterior al presente narrativo.
Una segunda búsqueda en español (*"Caribe raid mujeres cautivas Venezuela Coro Caquetío..."*) no
aportó fuente nueva específica de Coro, pero sí un matiz general útil: la mujer capturada podía
quedar como "esclava" o, si pasaba a concubina/esposa, "adquiría el atributo de tronco materno" del
nuevo linaje — es decir, la captura no es solo degradación permanente, tiene su propia vía de
incorporación plena. Ese matiz se incorporó a parentesco-028 para no simplificar de más.

Resultado: nueva subsección en el ensayo §2 ("Dos polos de ideación familiar, un solo frente de
conflicto"), con tabla comparativa y advertencia explícita anti-romanticización (ni caquetíos
"civilizados" ni caribes "salvajes" — dos sistemas coherentes en tensión); nuevo punto 7 en las
decisiones de diseño §5; `parentesco.yaml` con la entrada 028 corroborada y una entrada nueva
(029, `hipotetico`, la tesis causal en sí). Etiquetado con cuidado: los hechos de base
(patrón de captura, timing s. XIV) van `reconstruido`; la tesis de que ESE es el motor específico del
conflicto Curiana-Caribe queda `hipotetico`, porque ninguna fuente la afirma así de explícita — es
síntesis de esta sesión.

## Quinta ronda (2026-07-16): sociedades masculinas — excedente de solteros y "caribe" como categoría porosa

Miguel preguntó si, dado que hay poligamia por un lado y exogamia por el otro, no debería haber una
gran población de hombres que necesitan mostrarse dignos de casarse — y si "los caribes" no serían,
en parte, exactamente eso. También preguntó si esto debía expandir este ensayo o abrir uno nuevo:
decidí expandir este mismo ensayo (nueva sección §5), porque el mecanismo es consecuencia demográfica
directa de reglas ya establecidas aquí (poligamia §1c/§2, exogamia §4) y retoma directamente el hilo
"conflicto Curiana-Caribe" que quedó abierto en §2 de esta misma sesión — abrir un documento aparte
habría fragmentado un argumento a mitad de desarrollo. Si en el futuro esto se convierte en mecánica
de juego concreta (competencia de cortejo, tier de "jóvenes sin oficio", eventos de iniciación con
consecuencias sistémicas) valdría la pena un documento de diseño propio — pero eso es distinto de
investigación cultural.

Tres búsquedas (WebSearch):

1. *"polygyny bachelor surplus unmarried men warfare raiding anthropology theory bride competition"*
   — confirmó el mecanismo con fuerza: Koos & Neupert-Wentz (2020, datos georreferenciados,
   poliginia→conflicto intergrupal en África rural); caso yanomami (guerreros exitosos acceden a más
   esposas — el caso más cercano geográfica y culturalmente, sur de Venezuela/norte de Brasil); caso
   kuria de Tanzania (hombres sin hermanas casaderas, más propensos a robar ganado — mecanismo
   estructural instructivo aunque no americano); caso vikingo (poligamia/concubinato → proporción de
   sexos sesgada → raids, ScienceDirect) — útil para evitar exotización, mismo mecanismo en un pueblo
   que nadie llama "primitivo".
2. *"age-grade men's house warrior initiation society Amazon Guiana Arawak young unmarried men"* —
   resultado débil. Un detalle rescatable (hombres iniciados solteros con zona propia de hamacas en
   la casa comunal) pero **sin fuente identificable con precisión** — probablemente vinculado a
   literatura sobre las religiones Kuwai de pueblos arahuacos del norte, no confirmado en texto
   completo. Registrado en parentesco-031 con advertencia explícita de fuente débil.
3. *"Carib ethnogenesis pan-tribal warrior confederation identity not ethnic Caribbean scholarship"*
   — hallazgo importante y honesto de reconocer: "Caribe" funcionó en buena medida como categoría
   legal/política colonial (los españoles distinguían "arahuaco pacífico" de "caribe guerrero" en
   parte para decidir a quién se podía esclavizar bajo derecho castellano), y la investigación
   arqueológica reciente (morfología craneofacial) cuestiona el modelo clásico de "invasión caribe"
   con reemplazo poblacional biológico de las Antillas. **Esto obligó a volver sobre la cuarta ronda**
   (parentesco-028) para matizarla: el modelo de conquista que narra Adam 1879 —tomado con más
   confianza de la que ameritaba— es un modelo entre varios posibles, no un hecho cerrado. Se corrigió
   directamente en el ensayo §2 y se añadió parentesco-032 documentando el matiz.

De ahí surgió la hipótesis más especulativa del corpus (parentesco-033, `hipotetico` puro): que parte
de lo que la Curiana llama "caribe" podría, en la ficción, incluir bandas de hombres de origen
arahuaco diverso que resolvieron el cuello de botella matrimonial por la vía de la captura en vez del
pacto — capa de trasfondo opcional para Marokoto-ni, explícitamente NO sustituye la lectura simple ya
vigente en el canon.

Resultado: ensayo con nueva sección §5 (renumerando 5→6, 6→7); `parentesco.yaml` +4 entradas
(030-033, total 33); dos puntos nuevos de decisiones de diseño (7 y 8) más renumeración del punto de
conflicto Curiana-Caribe a 9; nuevo bloque de rol `rol_soltero_en_competencia`; corrección honesta
insertada en §2 sobre el estatus del modelo de "invasión caribe".

## Qué quedó abierto

- **`Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf` sin revisar** (519 pp.) — candidato obvio para
  una próxima pasada, ya que el propio programa lo señaló específicamente por su cobertura de
  sucesión de cacicazgos.
- **La tabla de parentesco guajiro/paraujano de Jahn 1927 (pp. 438-439) no se reconstruyó
  palabra por palabra** por riesgo de desalineación en la extracción — alguien con el PDF visual
  (no solo texto) podría hacerlo con más precisión.
- **El vocabulario tipo "ki-/kiu-" cerca de Jahn 1927 p. 456** no se identificó con certeza total
  (propongo jirajara/ayamán por contexto y fonología, pero no lo verifiqué contra una fuente
  independiente que confirme la lengua) — si se usa en el futuro, confirmar filiación primero.
- **No se consultó Zavala Reyes (2015)** directamente — es la fuente base del lexicón activo
  (`curiana_lexicon.py`) según sus propios comentarios de código, pero no está en `fuentes_caquetios/`
  como PDF navegable; el ensayo se apoya en lo que el lexicón ya extrajo de esa fuente, sin volver a
  la fuente original.
- **Ni Adam 1879, Angleria 1892, Gilij 1780-83, Perea Alonso 1942, ni el resto de PDFs en
  `fuentes_caquetios/`** se revisaron en esta sesión — quedan para sesiones futuras del programa si
  se juzgan relevantes al tema que traten (parentesco no es su foco evidente por título, salvo quizá
  Perea Alonso, gramática lokono, que el propio `CLAUDE.md` del proyecto ya señala como "no dio
  resultado" para trabajo comparativo previo).
- **La genealogía propuesta cubre completamente el esquema pedido para los 60 agentes, pero deja
  `linaje`/`madre`/`conyuge` en null para ~35 de ellos** por falta de base evidencial — ver nota de
  alcance al inicio de `genealogia.yaml`. Completar esos casos con propuestas razonadas (no solo
  relleno) es trabajo legítimo para una sesión futura, posiblemente cruzada con las otras tres
  sesiones del programa "corpus cultural" (que probablemente tocarán roles económicos/rituales que
  aclaren más vínculos).
- **No verifiqué si "daitiao" (Oliver 1989: 147) genera algún conflicto de scoring lingüístico** si se
  añadiera a `curiana_lexicon.py` — eso requeriría tocar código, fuera del alcance de esta sesión de
  investigación.
