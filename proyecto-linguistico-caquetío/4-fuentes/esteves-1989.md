---
tipo: fuente
obra: esteves-1989
autor: Juan de la Cruz Esteves
titulo: "Topónimos indígenas de Paraguaná y otros topónimos indígenas del estado Falcón"
lugar_año: "Caracas, 1989"
editor: Refinería de Amuay de Lagoven S.A.
estado_minado: parcial
prioridad: alta
medido: 2026-08-11
sostiene: []
---

# Esteves 1989 — Topónimos indígenas de Paraguaná

> **Qué es.** El gazeteer de Paraguaná que al proyecto le faltaba. 146 páginas
> de entradas topónimo por topónimo, con ubicación, censo y etimología
> propuesta. Es **la fuente que desbloquea [#92](https://github.com/miguelgilurbina/curiana-radio/issues/92)** —
> los poblados de Paraguaná que hoy no se pueden meter en `asentamientos.yaml`.

## Ficha

| | |
|---|---|
| Autor | **Juan de la Cruz Esteves** — cronista, poeta e investigador de Paraguaná |
| Título | *Topónimos indígenas de Paraguaná y otros topónimos indígenas del estado Falcón* |
| Publicación | Caracas, 1989 · patrocinada por la **Refinería de Amuay de Lagoven S.A.** |
| Otra obra suya | *Paraguaná histórica y geográfica* (misma colección) |
| Procedencia | Enviado por Nery R. Gil el 2026-07-27, seis PDF escaneados |

> ⚠️ **La grafía del apellido es `Esteves`, con -s.** El nombre de los archivos
> dice "Estevez"; la portada, la portadilla y la introducción de Lagoven dicen
> **Esteves**. Manda la fuente.

## Estatus epistémico: pista fuerte, autoridad débil

**No es una obra académica.** Esteves es el **cronista** de Paraguaná: recoge de
historiadores y cronistas locales, de archivos parroquiales y de saber
transmitido. Eso le da un valor que ninguna fuente académica del repo tiene
—conoce los lugares y los papeles locales— y una debilidad que hay que declarar:
**sus etimologías son propuestas suyas, no análisis lingüístico.**

Cómo entra cada cosa, entonces:

| Lo que dice | Cómo entra |
|---|---|
| Cita un documento con nombre (censo, visita pastoral, libro de bautizos) | se persigue hasta el documento; ahí sí puede ser `atestiguado` |
| Ubicación de un lugar, censo de casas y vecinos | `atestiguado` con la fecha del censo |
| Etimología propuesta sin cita | `hipotetico` — es una propuesta de un cronista, no un despeje |
| **Corrobora un morfema que ya teníamos** | ⭐ eso es lo que más rinde: segunda atestación independiente |

## 🔑 Las fuentes que Esteves usa — lo que hay que perseguir

Esto es lo más valioso de la obra para el proyecto: **es un puente hacia
documentos de archivo que no tenemos.**

| Fuente que cita | Qué es | Prioridad |
|---|---|---|
| ⭐ **Visita Pastoral del obispo Mariano Martí (1773)** | Fuente **colonial primaria**. Martí recorrió y describió las parroquias de Venezuela. Oliver 1989 ya lo cita como "Martí 1969" (la edición moderna) | **alta** |
| **Censo de 1881** | Casas y vecinos poblado por poblado. Aparece en casi cada entrada | alta |
| **Libros de bautizos parroquiales** — Jadacaquiva, 1835-1842, cura José María Valbuena | Registro nominal local | media |
| **"Antiguos papeles de la posesión de Urupaguaduco"** | Títulos de tierra coloniales | media |
| **Pedro Manuel Arcaya Madriz** | Ya lo tenemos: [[arcaya-1920]]. Esteves señala que la casa de Acaboa fue de sus ascendientes | — |

> **Martí 1773 es el que hay que conseguir.** Es el único de la lista que es
> colonial y primario, y ya está citado por Oliver, así que la edición moderna
> existe y es rastreable.

## ⚠️ Advertencia de época, la de siempre

Las fuentes de Esteves son de **1773, 1835-1842 y 1881**. Eso es *más lejos* del
precontacto que la carta de Bastidas (1538), no más cerca.

**Nada de esta obra puede sostener `precontacto: si`** en
`3-mundo/asentamientos.yaml`. Lo que sí hace, y es mucho, es dar el **inventario
de topónimos** y su ubicación — que es justo lo que [#92](https://github.com/miguelgilurbina/curiana-radio/issues/92)
necesita para dejar de tener a Paraguaná vacía.

## Lo minado hasta ahora — 10 de 146 páginas

> 🔴 **Barrido en curso.** Lo de abajo sale de las páginas 11-16 y 25 del libro.

### ⭐ Los cuatro hallazgos que ya cambian algo

**1. `jadicuar` resuelto — y contra la hipótesis que teníamos.**

`toponimos.yaml` tiene `jadicuar` sin glosa, y yo lo había marcado como posible
variante de **Jadacaquiva**. Es falso. Esteves (p. 14):

> ADÍCORA — *"El nombre primitivo era **Jadícuar**, que quiere decir: jajatal,
> sitio donde abunda el jajato, hierba halófila de terrenos salobres. Este
> Jadícuar, por uno de esos curiosos procesos de selección eufónica, ha venido
> cambiando de Jadícuar a Jadícora, de Jadícora a Jatícora, hasta llegar al
> sugestivo y poético Adícora de hoy."*

Es **el nombre indígena de Adícora**, con la cadena de cambio completa. Sirve
para subir `nodo-012` en `3-mundo/asentamientos.yaml`, que hoy está como
`reconstruido` porque solo teníamos el nombre.

**2. Una serie morfológica de apellidos caquetíos — con Manaure dentro.**

Esteves (p. 13) lista *"algunos de los apellidos de la gran familia caquetía"*:

> **Adaure · Timaure · Yaraure · Chunaure · Manaure**

Cinco formas en `-aure`. `toponimos.yaml` ya tenía `timaure` ('Apellido') y
`tumarure` ('Apellido de un cacique') sueltos y sin explicar; ahora hay serie.
Toca directamente al personaje central del elenco.

> ⚠️ Esteves **no** analiza `-aure` como morfema ni da su significado. La serie
> es suya; el análisis sería nuestro y sería `hipotetico`.

**3. 🔴 Amuay no sería caquetío: Esteves lo atribuye al caribe insular.**

> AMUAY (p. 16) — *"La voz da la idea de cavidad subterránea, haitón, cueva
> grande… **Por su fonética la voz pertenece al caribe insular**, como batey,
> mamey, caney, carey"*.

Es un topónimo **de Paraguaná** atribuido a otro estrato lingüístico. Va
directo a [[esfera-de-interaccion]]: la sociedad no era monoétnica y la lengua
no era homogénea. El lexicón ya tiene las categorías `kalinago` (19) y
`kalinago-caribe-overlay` (4) donde esto encajaría.

**4. Un documento de 1556 con voz indígena, citado textual.**

Petición de los **indios amuayes** al obispo Gerónimo de Ballesteros pidiendo
cambiar de santo patrono:

> *"A vos, Gerónimo, que sos nuestro Obispo y Amo, te pedimos dos cosas. La
> primera: es un buen santo para nuestro Patrón, pues nosotros no queremos a
> San Juan, pues como está desnudo, no va a querer que llueva para no tener
> frío. La segunda: Danos otro cura, que no sea cobarde como el que tenemos,
> que en cuanto vio venir el verano se largó…"*

**Ballesteros es el mismo obispo cuya carta de 1550 ya citamos** vía Oliver
(`geografia_politica-004/005`, el canal del `buco` y los 14-15 mil indios).
Esteves añade que fue el **segundo obispo de Coro** y que murió allí en 1558.

> ⚠️ Esteves **no da la referencia de esta petición**. Menciona la compilación
> del Coronel José Félix Blanco, *Documentos para la Historia del Libertador*
> (1875), pero en la frase siguiente y aplicada al dato de la lápida. **Hay que
> perseguir la fuente antes de usarla**: una cita sin procedencia de un texto
> tan bueno es exactamente donde conviene desconfiar.

### Morfemas que corroboran el lexicón

| Morfema | Glosa de Esteves | Estado en el repo |
|---|---|---|
| ⭐ **`bacoa`** | 'lugar, paraje' | **CORROBORADO** — el lexicón dice 'bosque, lugar, paraje, sitio fértil'. Es nuestro morfema más productivo (`adabacoa`, `guadabacoa`, `quibacoas`, `yacarebacoa`, `sazaribacoa`) y esta es una **segunda atestación independiente** |
| **`ure`** | 'raíz' — y dice que está *"presente en muchos topónimos indígenas de Paraguaná"* | 🆕 nuevo — candidato a morfema productivo |
| **`bara`** | 'árbol' | 🆕 |
| **`guani`** | 'abeja' (mansa, sin aguijón) | 🆕 |
| **`dabuda`** | 'barro de loza' (greda de cerámica local) | 🆕 |
| **`dara`** | alcaraván, *Charadrius* (ave) | 🆕 |
| **Semeruco** | Esteves lo da como nombre anterior de Camoruco | corrobora `cemirucos → 'Semerucos'` de `toponimos.yaml` |

### Topónimos con ubicación y censo

| Topónimo | Qué es | Dato |
|---|---|---|
| **Abudure** | aldea al SO de Moruy | censo 1881: 6 casas, 50 vecinos. `dabuda`+`ure` = 'sitio de donde se extrae barro de las raíces' |
| **Acaboa** | lugar pecuario, municipio Jadacaquiva | censo 1881: 2 casas, 11 vecinos. **Oratorio en 1773 (Martí)** |
| **Adaro** | Punta de Adaro, costa occidental, Los Taques | de `dara`, con prótesis vocálica y disimilación a>o |
| **Adaure** | aldea al oeste de Buenavista | censo 1881: **87 casas, 522 vecinos** — mayor que muchas cabeceras de municipio. **Martí 1773 citado textual**. Aníbal Hill Peña los da como "tribu belicosa" |
| **Adícora** | capital de municipio, costa oriental | ⭐ antes **Jadícuar** = 'jajatal' (ver arriba) |
| **Aguaque** | fundo a dos leguas al norte de Pueblo Nuevo | de *guaco*, portulácea. Casa natal de Josefa Camejo; Monumento Histórico desde 1982 |
| **Amaraya** | aldea al sur de Jadacaquiva | censo 1881 (como *Amaralla*): 16 casas, 108 vecinos. ¿de *maracaya*, el "güirito", gato silvestre? |
| **Amuay** | bahía y población, municipio Los Taques | censo 1881: 8 casas, 60 vecinos → ~400 casas y 3.000 hab. al escribir. 🔴 **atribuido al caribe insular** |
| **Antuni** | lugar pecuario al norte de Jadacaquiva | Esteves **duda que sea indígena** |
| **Buenibativa** | caserío San Pedro, municipio Adícora | de *Guanibativa*; `bativa` sin explicar |
| **Caibacoa** | sabana al oeste del fundo de Aguaque | `cái` (< *guay*, árbol tipo ceiba) + `bacoa` |
| **Camare** | municipio Pueblo Nuevo | censo 1881: 8 casas, 48 vecinos |
| **Camoruco** | cerca de Caradacagua, oeste de Pueblo Nuevo | antes *Semeruco* |

Y aparecen como referencia geográfica: **Moruy · Jadacaquiva · Los Taques ·
Adícora · Pueblo Nuevo · San Pedro · Aguaque · Caradacagua · Urupaguaduco ·
Buenavista**.

### 🔴 Lo que el cruce con nuestros datos destapó (pp. 17-19)

**El proyecto ya citaba a Esteves sin tener la obra.** `morfemas.yaml` §46-47
dice: *"van Buurt §5 recoge `-ure` (papiamentu -huri/-uri) glosado 'raíz' por
**Cruz Esteves 1989**, y lo declara equivalente al `-ure` continental. La
evidencia toponímica dice 'sitio de'."* Era un conflicto abierto contra una
fuente que no teníamos. Ahora la tenemos.

#### 1. `-ure` = 'raíz' — Esteves lo sostiene con tres topónimos

| Topónimo | Descomposición de Esteves |
|---|---|
| **Abudure** | `dabuda` 'barro de loza' + `ure` 'raíz' = 'sitio de donde se extrae barro de las raíces' |
| **Babahuro** | `baba` 'caño' + `ure` 'raíz' = 'el caño de las raíces' — *"por las abundantes raíces adventicias de los tupidos manglares"* |
| **Asubure** | nombre indígena del *sesuvio* (*Sesuvium portulacastrum*), el "vidrio". ⚠️ Esteves NO lo descompone |

Los dos primeros son referencias **literales** a raíces (raíces de manglar,
barro extraído de raíces), no a 'sitio de'. Eso **refuerza la lectura de
Esteves** frente a la nuestra, pero no la cierra: `-ure` podría ser 'sitio de'
y el sentido de raíz venir del otro elemento. Sigue en conflicto declarado.

#### 2. 🔴 `bara`: el lexicón dice 'río', dos fuentes dicen 'árbol'

Esteves (p. 19), citando el *Glosario de Voces Indígenas* de **Lisandro
Alvarado** — que es [[alvarado-1921]], obra que **ya tenemos y ya minamos**:

> *"Sabemos que **Bara**, en lengua caquetía, es voz general para designar toda
> clase de **árbol**. Nos informamos en Lisandro Alvarado que **Barabara**,
> plural por duplicación, es el nombre de un árbol caparidáceo que aquí
> conocemos con el nombre de olivo."*

Y `morfemas.yaml` §59 ya decía que **van Buurt §5** documenta `bara`/`bari`
'árbol' (cf. lokono *balli*).

**Pero `curiana_lexicon.py:113` tiene `bara` = 'río, corriente fluvial'**,
`caquetío-reconstruido`, *"forma justificada por cognado en
proto-arawakan/topónimo"*.

> Dos fuentes independientes dicen 'árbol'; el motor dice 'río'. Es el mismo
> patrón que `tara` ([#45](https://github.com/miguelgilurbina/curiana-radio/issues/45)),
> `saruro` ([#47](https://github.com/miguelgilurbina/curiana-radio/issues/47))
> y `corie` ([#46](https://github.com/miguelgilurbina/curiana-radio/issues/46)).
> Levantado aparte.

Complica el cuadro que `bara` aparece **además** como cognado lokono de `para`
'mar' (`cognados.yaml`). Tres sentidos en danza: 'río', 'árbol', 'mar'.

#### 3. `saruro` (#47) — pista, no solución

Esteves da **Asaro** (aldea de Pueblo Nuevo) y lo compara con **Sarosaro** de
La Guajira, *"plural por duplicación… un árbol cuya madera blanda utilizaban
los guajiros para obtener el fuego por frotación"*.

⚠️ **No resuelve #47.** La forma es `sarosaro`/`asaro`, no `saruro`; y es
**guajiro**, no caquetío. El issue dice que Alvarado no trae `saruro` ni como
lema — y esto no lo cambia. Es una pista para seguir, nada más.

#### 4. Dos rasgos morfológicos que se repiten

- **Reduplicación = plural.** Esteves lo dice dos veces con esas palabras:
  `Sarosaro` y `Barabara` son *"plural por duplicación"*. Nuestro
  `jurijurebo` ya usaba reduplicación. ⚠️ Pero `morfologia.md:176` la lee como
  **intensidad** (`barabara` = 'árbol de madera dura'), no como plural.
  **Otro conflicto**, y esta vez Esteves es explícito.
- **`baba` = `baja` = 'caño'.** Esteves los da como equivalentes (Bajabaroa,
  Babahuro).

#### 5. Una regla prosódica, y es nueva

> ARAJÓ (p. 17) — *"Sobre esta voz Arajó, inusitada por **aguda**, mantenemos
> reservas: **las voces agudas escasean en los topónimos indígenas de
> Paraguaná**; a nuestro modo de ver, la pronunciación primitiva debió ser:
> Arajo."*

Es una afirmación **fonotáctica comprobable** contra nuestros 74 topónimos, y
el proyecto no tenía nada sobre acento. Encaja en
[[fonotactica]] — que hoy solo mira inventario, clusters y codas.

### ⭐⭐ pp. 26-27 — evidencia para D9, y el `capu` del cronista corroborado

> **CAPUHANA** (p. 26) — *"`Capu-hana`, con hache intercalada para deshacer el
> diptongo, es el nombre de un pequeño cerro, cerca de Misaray. Quiere decir:
> **el cerro del duende**. **`Capó`: duende, ente sobrenatural. `Bana`: cerro,
> sitio alto.**"*

Dos golpes de una vez.

#### `bana` = 'cerro, sitio alto' — evidencia directa para D9 ([#38](https://github.com/miguelgilurbina/curiana-radio/issues/38))

El motor glosa `-bana` como **'orilla, borde'** (CLAUDE.md, locativos) y
`morfologia.md` como **'ancho, llano'**. Esteves dice **'cerro, sitio alto'** —
que es *lo contrario* de llano.

Es una glosa nueva y de una fuente que conoce el terreno: Capuhana **es** un
cerro. D9 lleva abierta desde el principio y **bloquea el gate**.

##### 🔴 Y en la p. 28, segunda atestación — que además explica de dónde vino nuestro error

> **CARIRUBANA** — *"significa: orilla del peñón, la orilla del cerro. **`Cari`:
> orilla. `Bana`: sitio alto.**"*
>
> **CARIGUARIANA** — *"quiere decir: la playa de los tabacones… **`Cari`:
> orilla de mar.** `Guariana`: tabaco pescador o tabacón."*

Con esto quedan **dos morfemas separados y dos atestaciones cada uno**:

| Morfema | Glosa de Esteves | Dónde |
|---|---|---|
| **`cari`** | **'orilla, orilla de mar'** | Carirubana, Cariguariana |
| **`bana`** | **'sitio alto, cerro'** | Carirubana, Capuhana |

> ⭐ **La hipótesis que esto sugiere**: el proyecto glosa `-bana` como
> **'orilla, borde'** — que es exactamente lo que Esteves asigna a **`cari`**.
> Si `Carirubana` = `cari`+`ru`+`bana` = 'orilla del cerro', entonces alguien
> leyó el compuesto entero, se quedó con 'orilla' y se lo colgó al elemento
> equivocado. **`-bana` habría absorbido el significado de `cari`.**
>
> Es una hipótesis, no un veredicto: hace falta ver de dónde salió nuestra
> glosa original. Pero explica el conflicto entero de D9 de una manera
> económica, y encaja con que `-bana` conviva con `-ana` sin que nadie sepa
> distinguirlos.

#### `capu` = 'duende, ente sobrenatural' — el cronista tenía razón

`curiana_cronista.py` sustituye *demonio* → **`capu`** como parte de
`DESCOLONIZAR`. Esa elección se hizo por coherencia interna del canon.
**Esteves la corrobora desde fuera**: `Capó` es el ente sobrenatural, y aquí no
es un demonio cristiano sino **un espíritu protector de los árboles**.

Esteves añade que equivale al **`Región`** de las creencias campesinas del
Guárico, *"cuyos primitivos habitantes eran también de ascendencia caquetía"*.

#### 🐍 Y la serpiente emplumada — con cuidado

El profesor **Francisco Tamayo**, etnólogo, recogió que en el cerro de Capuhana
hay un duende que, junto a **una serpiente emplumada con una estrella en la
cabeza**, impide que se corten los árboles. Tamayo comenta que es *"la misma
leyenda de la serpiente emplumada de los mejicanos"* y postula
**transculturación de los aztecas hacia los caquetíos**. Esteves propone lo
contrario: de los caquetíos hacia los mejicanos.

> ⚠️ **Ninguna de las dos direcciones tiene apoyo aquí.** Es una creencia
> recogida en el siglo XX: `retro-abstraido` como máximo, y la etiqueta
> **nunca asciende**. La comparación "serpiente emplumada = Quetzalcóatl" es
> difusionismo clásico y hay que tratarla como tal.
>
> Dicho eso, **toca [[horizonte-de-contacto]]** — la nota que se escribió para
> la pregunta "¿pudo un caquetío contactar con los mayas?". Aquello se cerró
> con jadeíta de Motagua en las Antillas Menores, ~1000 años antes de la
> ventana simulada. Esto es de otro tipo: folclore moderno, no material
> arqueológico. Se anota, no se usa.

##### Tercera atestación de `bana`, pp. 30-31

> **COABANA** — *"El topónimo es una voz compuesta que dice: **el cerro de las
> coas**. `Coa` es un tosco instrumento de labranza, un palo aguzado para abrir
> el surco. **`Bana`: cerro.**"*

Tres topónimos, tres veces 'cerro / sitio alto', y en los tres el referente es
un accidente elevado: **Capuhana · Carirubana · Coabana**. Para una glosa que
el proyecto tiene como 'orilla' o 'llano', es evidencia dura.

### pp. 30-31 — dos afijos corroborados y un sitio precolombino

#### ✅ `-uco` / `-uto` = 'quebrada, cauce' — corroboración limpia

> **CODUTO** — *"El sufijo **`uto`** y **`uco`**, indistintamente, lo hemos
> hallado formando voces compuestas con la significación de **quebrada,
> cauce**."*

`morfologia.md:35` ya tenía `-uco` = 'cauce, quebrada (variante `-uto`)',
**sostenido por una sola fuente**: Zavala #268. Esteves da la **misma glosa y
la misma variante** de forma independiente. Es de los afijos de
`REGLAS_ZAVALA`, así que toca al motor.

#### 🆕 `-dito` = colectivo

> **COCODITE** — *"Del topónimo sabemos que el sufijo **"dito"** es distintivo
> de los **sustantivos colectivos** en lengua indígena."*

Afijo nuevo, no está en `morfemas.yaml`. Una sola fuente y sin más ejemplos:
`hipotetico`.

#### ⭐ CAYERUBA — el primer sitio de Paraguaná con evidencia precolombina

> *"no hay dudas de que en **tiempos precolombinos** fue asiento de un populoso
> vecindario indígena, lo atestigua, aparte de la abundancia de **restos de
> cerámica aborigen** que se encuentra en el lugar, **el hallazgo reciente de
> un cementerio**."*

Esto **sí** es del tipo de evidencia que `3-mundo/asentamientos.yaml` exige para
`precontacto`: material, no documental. Hoy ningún nodo continental lo tiene.

> ⚠️ Pero es **Esteves reportando**, no un informe arqueológico. Sin excavación
> publicada ni fecha, no alcanza para `precontacto: si` —que exige
> `precontacto_razon` verificable— pero sí marca **dónde habría que buscar**.
> Curiosamente, Cayeruba **no aparece en el censo de 1881** y Esteves llama la
> omisión "inexplicable".

#### Documentos de archivo con fecha, que es lo que rinde

| Año | Qué | Dónde |
|---|---|---|
| **1590** | *"antiguos papeles escriturados… como tierras compuestas a favor de Alonso Arias Vaca"* — donde el topónimo es **Cocodito**, no Cocodite | p. 31 |
| **1698** | papeles escriturados de los linderos de la posesión de **Urupaguaduca** (topónimo *Carajaima*, antes *Caramajaima*) | p. 27 |

**1590 es el documento más antiguo que Esteves cita**, y está a 52 años del
pacto de Manaure. Merece perseguirse.

### pp. 32-33 — `bana` cuarta vez, `bacoa` segunda, y un vínculo con los jirajaras

#### `bana` / `bano` — cuarta atestación, con variante

> **CUBIANO** — *"`Cujíbano`, que es la forma primitiva, quiere decir: **el
> cerro del cují**."*

Cuatro: **Capuhana · Carirubana · Coabana · Cujíbano**. Y aparece la variante
**`-bano`**, que el proyecto no tenía registrada. (También hay un
**Cucurubano**, pero Esteves lo despacha como onomatopéyico.)

#### ✅ `bacoa` = 'lugar' — segunda atestación dentro de Esteves

> **CUMUJACOA** — *"alteración de `Curumubacoa`, quiere decir: **lugar de los
> zamuros**. `Curumu`: zamuro. **`Bacoa`: lugar.**"*

Con `Caibacoa` (p. 25) van dos dentro de esta obra, más las cinco de Zavala en
nuestro `toponimos.yaml`. **`bacoa` es el morfema mejor sostenido del corpus
toponímico.** Y `curumu` = 'zamuro' es entrada nueva.

#### ⭐ Un vínculo lingüístico caquetío–jirajara, dicho por Esteves

> **CUMARAGUAS** — *"En los valles de **Yaracuy** hay también un lugar con ese
> nombre, esto revela que **existieron vínculos lingüísticos entre caquetíos y
> jirajaras**."*

Toca dos cosas a la vez:

- **[[esfera-de-interaccion]]**: es una afirmación explícita de contacto
  lingüístico entre dos pueblos. El elenco tiene 2 agentes jirajara y el
  lexicón 7 formas `jirajaroide-contacto`.
- **[[polities-caquetias]]**: Yaracuy es una polity **distinta** de la costera
  que simulamos. Esteves cruza esa frontera con un topónimo compartido — que es
  justo el tipo de dato que la regla 4 de CLAUDE.md obliga a marcar antes de
  usar.

> ⚠️ Un topónimo compartido no prueba parentesco lingüístico: puede ser
> préstamo, coincidencia o difusión posterior. La inferencia es de Esteves.

##### 🔴 Y de paso, un conflicto de glosa

Esteves: **`cumaragua`** = *"un pequeño **cangrejo** de caparazón rosada… voz
indígena con significación de **espuma rosada**"*.

El lexicón tiene `cumaragua` = **'caracol de las costas de Paraguaná'**.
Cangrejo ≠ caracol. Menor, pero es del mismo tipo que `bara` y `tara`.

#### 🆕 El mapa de Fidalgo — fuente cartográfica

> **CUCUY** — *"La Punta de Cocuy está señalada en el **mapa de Paraguaná que
> elaboró el Brigadier Joaquín Fidalgo**."*

Fidalgo levantó la carta de la costa de Venezuela a finales del s. XVIII. Es
**fuente primaria cartográfica** y fija topónimos con posición. Va a la lista
de adquisición.

#### Dos entes sobrenaturales más

- **El Cude** (paraje boscoso con rocas cavernosas, Pedregalito, mun. Adícora):
  *"un ente sobrenatural, un espíritu perturbador que trastorna a las personas
  con su invitación al viaje del Más Allá"*. Voces, quejidos, luces nocturnas.
- Junto al **Capó** de Capuhana y el **Región** del Guárico, van tres.
  ⚠️ Todos son creencia viva recogida en el s. XX: `retro-abstraido`.

#### Y una nota ecológica que sí sirve

> **CUNACHO** — de `Cuna`/`Cunaro`, *"pez lábrido que abunda en el golfete de
> Coro y del cual extraían **manteca para untar los 'jachos'**, teas de madera,
> comúnmente de curarí, para encandilar en labores de **pesca nocturna**"*.

Técnica de pesca con antorcha alimentada con grasa de mero, en el Golfete.
Material para [[mapa-ecologia]] y para el canon.

### p. 35 — `ebo` corroborado, un sitio de 1538 y una pista guayquerí

#### ✅ `ebo` = 'camino, paso, senda' — tercera atestación, segunda fuente

> **CURAIDEBO** — *"su forma primitiva `Curarirebo`, significa: **el paso del
> Curarí**. `Curarí`: árbol maderable, tecoma. **`Ebo`: camino, paso, senda.**"*

`toponimos.yaml` lo tenía por `jurijurebo` y `cumarebo`, ambos vía Zavala.
Esteves lo da **con la glosa idéntica** y en un tercer topónimo. Junto con
`bacoa`, es de lo más firme que hay.

(Y `curarí` 'árbol maderable, tecoma' ya había salido en la p. 33 como la
madera de los `jachos` para pesca nocturna: coherencia interna.)

#### ⭐ CHAMURIANA — una aldea indígena anterior a 1538

> *"**Antigua aldea indígena** en cuyas cercanías los españoles fundaron en
> **1538** el pueblo de Santa Ana de Paraguaná. En el lugar se hallan **restos
> de cerámica indígena y europea**. Nada sabemos del significado de la voz."*

Segundo sitio de Paraguaná con evidencia material (tras Cayeruba), y este
además **fechado por el contacto**: la aldea ya estaba cuando llegaron los
españoles en 1538.

> ⚠️ Anterior a 1538 **no es precontacto**: el contacto en esta costa empieza
> hacia 1499-1527. Sigue sin dar `precontacto: si`, pero es el nodo peninsular
> con la evidencia más temprana de todo el libro hasta aquí — y la cerámica
> mixta indígena/europea documenta el momento del choque.

#### 🆕 Charaima y los guayquerí — una pista para un hueco declarado

> **CHARAIMA** — 1881: 79 casas, 527 habitantes. Nombre primitivo **`Charaide`**
> según su *Título de Composición*. Y: *"No sabemos qué relación guarda el
> nombre de esta Charaima de Paraguaná con el del **cacique Charaima de la Isla
> de Margarita, el abuelo del guayquerí Francisco Fajardo**."*

[[esfera-de-interaccion]] §6 declara como hueco: *"Si los guaycaríes eran un
grupo distinto o una denominación de otra cosa. Son 4 agentes del elenco y no
hay nota de fuente que los sostenga."*

Esto **no lo cierra** —Esteves mismo dice que no sabe si hay relación— pero es
el primer rastro documental de los guayquerí que toca el proyecto, y viene con
nombres perseguibles: cacique Charaima de Margarita, Francisco Fajardo.

#### `caramata`/`caigua`: otro estrato, y cumanagoto

> **CARADACAGUA** (p. 27) — de *Caramatacaigua*, 'guairón de cal'. **"En lengua
> cumanagota, `caramata` es carbón y `caigua` es un molusco, la almeja"**.
> Esteves lo apoya con evidencia material: vio en el sitio *"señales,
> antiquísimas y abundantes, de los guairones donde los indios quemaban
> conchas marinas para la obtención de cal"*.

Segundo topónimo de Paraguaná atribuido a lengua **no caquetía** (tras Amuay al
caribe insular). El lexicón tiene `caribe-cumanagoto` con 2 entradas. Más
material para [[esfera-de-interaccion]].

### Más fuentes que cita, según avanza el barrido

| Fuente | Dónde | Qué aporta |
|---|---|---|
| **Aníbal Hill Peña**, historiador | p. 13 | los adaures como "tribu belicosa"; Esteves dice tener papeles de sus peleas contra los españoles |
| **José Félix Blanco (Cor.)**, *Documentos para la Historia del Libertador* (1875) | p. 16 | compilación por decreto de Guzmán Blanco |
| **Obispo Gerónimo de Ballesteros** | p. 16 | 2.º obispo de Coro, † Coro 1558. **El mismo de la carta de 1550** que ya citamos vía Oliver |
| ⭐ **Lisandro Alvarado**, *Glosario de Voces Indígenas* | p. 19 | **Ya lo tenemos**: [[alvarado-1921]]. Fuente de su `bara` = 'árbol' — comprobable directamente |
| **José Luis Cisneros**, *Descripción de la Probincia de Benezuela* | p. 18 | libro colonial (1764). Da *Avotuca* como "lugar de vigilancia de las costas de Paraguaná" |

### 👍 Un punto a favor del método de Esteves

En `Acaboa` **rechaza** la etimología de *Caoba* "porque este árbol no existe en
la flora autóctona de Paraguaná". Es exactamente el tipo de control ecológico
que el proyecto aplica en [[mapa-ecologia]]. No es un cronista que acepte
cualquier cosa.

## Cómo se lee esta fuente

Los PDF **no tienen capa de texto**: son fotos de CamScanner y `pdftotext` solo
devuelve la marca de agua. Se leen extrayendo la imagen embebida de cada página
y mirándola:

```bash
python <scratchpad>/extraer_paginas.py <pdf> <desde> <hasta> <destino>
```

Los seis archivos son **contiguos y sin solapamiento**, por tramos de página del
libro: 1-25 · 25-55 · 55-72 · 72-100 · 100-129 · 129-final.

## Lo que falta

- **136 de 146 páginas.** El barrido completo es el trabajo de #92.
- ✅ ~~Comprobar `jadicuar` ↔ Jadacaquiva~~ — **resuelto y descartado**: es el
  nombre primitivo de **Adícora**.
- Perseguir a **Martí 1773** y a la petición de 1556, que Esteves cita sin dar
  procedencia.
- Hay un **Apéndice** con un artículo "Sobre el Nombre de Adícora" (remitido
  desde la p. 14). Localizarlo — probablemente en el archivo 6.

## Enlaces

[[INDICE_FUENTES]] · [[arcaya-1920]] · [[zavala-reyes-2015]] · [[toponimia]] · [[esfera-de-interaccion]] · [[mapa-ecologia]]
