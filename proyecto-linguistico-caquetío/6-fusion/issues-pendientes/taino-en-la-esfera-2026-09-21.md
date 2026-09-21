# El taíno en la esfera: primos, no vecinos — y el vector que faltaba

**Campaña del taíno, parcela T5 (el mundo), 2026-09-21.** Encargo de Miguel:
«buscar tal cual lo hicimos con el resto de lenguas fuentes y **anexarlas a
nuestra esfera**. Y analizar también las similitudes con el Caquetío.»

**Ninguna cifra de este borrador está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/medir_taino_en_la_esfera.py
python 6-fusion/scripts/medir_taino_en_la_esfera.py --sin-base   # si Supabase no está levantado
```

Datos, citas y las entradas propuestas, en
`6-fusion/taino_en_la_esfera_2026-09-21.yaml`.

---

## 0. Antes de nada: dos cosas del encargo resultaron falsas al medirlas

1. **`moreno-mayar-2018` no es genética del Caribe.** El encargo lo listaba
   como «genética antigua del Caribe (Schroeder_et_al_2018…)». Es *Early human
   dispersals within the Americas* (Science 362), sobre Beringia y el
   Pleistoceno tardío, y el repo ya lo documenta: el archivo se llamó
   «Schroeder…Caribbean_Taino» durante meses sin serlo, y nadie llegó a
   citarlo — 0 hechos del corpus, 0 entradas del lexicón. El Schroeder de
   verdad sí está, y está minado.

2. **Dos de las fuentes que esta parcela necesitaba están en 0 bytes**, hoy,
   verificado:
   - `Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf` — la monografía que define
     la tradición dabajuroide frente a las series antillanas.
   - `Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf` — la única
     genómica del Caribe precontacto con muestras de **varias** poblaciones.

   Las dos estaban ya declaradas vacías en sus notas desde 2026-07-29. Lo que
   añado es que **siguen así** y que son justo las dos que cerrarían las dos
   negativas más fuertes de este informe.

   Y una tercera: **tesseract no está instalado** en esta máquina (ni en PATH
   ni en `C:/Program Files/Tesseract-OCR`). La memoria del proyecto da el OCR
   por disponible desde 2026-08-14 y hoy no lo está, así que la tesis escaneada
   de Oliver (79 MB, 801 pp.) sólo se pudo leer por los capítulos 2 y 3, que
   traen capa de texto propia.

---

## 1. El veredicto, en una frase

**No hay ni una pieza de evidencia —arqueológica, genética ni
etnohistórica— de contacto precolombino entre la polity caquetía costera y las
Antillas Mayores taínas.** Lo que sí hay, abundante y fechado, es movimiento
**colonial en sentido único**: caquetíos deportados a La Española y a Puerto
Rico desde 1513. Eso no anexa el taíno a la esfera. Lo convierte en el vecino
que el caquetío conoció por haber sido llevado a su isla encadenado.

El taíno y el caquetío son **primos, no vecinos**. Salieron del mismo nodo
arahuaco hace dos milenios largos y por puertas distintas —el taíno por
Trinidad y el arco antillano, el caquetío por los Llanos hacia el oeste— y no
consta que se volvieran a encontrar.

---

## 2. El cero, verificado (regla 6)

El encargo decía que un `grep` de «taín/taino» en `3-mundo/etnias.yaml` no
devuelve nada. **Es cierto**, y el cero aguanta un barrido de 26 ortografías —
las que usaría un cronista (antillano, arahuaco insular, isleño, lucayo,
boriquén, Española, Santo Domingo) y las de cultura material (ostionoide,
chicoide, meillacoide, guanín).

| Diana | Resultado |
|---|---|
| `3-mundo/etnias.yaml` | **1 acierto**: «Antillas», una vez, en el `aviso_familia` de `etnia-008` — «un contacto caribe en la polity costera solo cabe POR MAR… o desde las Antillas». Es una posibilidad declarada, no un vecino |
| `3-mundo/asentamientos.yaml` | **cero absoluto** |
| `3-mundo/corpus/` | **47 aciertos** — y ahí está el punto |

**El taíno ya vive en el repo, pero en tres papeles que no son el de vecino**:
comparanda de parentesco (avunculocalidad, sucesión matrilineal, poliginia
cacical — vía Keegan 1989), rama del árbol arahuaco («el arco norteño»), y
estrato del lexicón. Los tres son profundidad temporal o método comparativo.
Que el taíno esté en el corpus no llena el hueco de `etnias.yaml`: lo hace más
visible.

Y hay un contexto que conviene tener delante: el registro tiene 8 etnias y
**sólo una toca la polity costera**, que es `etnia-008`, canon-simulación con
`deuda: sin-procedencia`. El hueco del taíno no es una omisión suya; es el
estado del registro entero.

---

## 3. ⭐ Lo que hay que leer primero — para T1, T2 y T4

Esto cambia cómo se mina el taíno **para léxico**, que es lo que las otras
parcelas están haciendo ahora. Son tres vectores y el proyecto sólo tenía
escrito uno.

### Vector 1 — el español llevó el taíno a Venezuela. Lo dice Oliver, tres veces

> «Both the terms **caney** (chief's house) and **fotuto** or fututo
> (trumpet-like instrument) are Taíno (Arawakan) words, and **were probably
> introduced by the Spanish from the Antilles**… That Taíno was used often
> (e.g. **cacique, huracán, hamaca**, etc.) is of no surprise since most
> Spanish had to stop in Hispaniola before continuing elsewhere.»
> — Oliver 1989, cap. 3, p. 241 (n. 83)

> «[**naboria**] is of Taíno origin and was probably applied by Federmann and
> not the Caquetío. Federmann probably learned this term (as he did other terms
> such as **cacique**) in his various stays in Hispaniola. There is a remote,
> however unlikely, possibility that both Caquetío and Taíno languages used the
> same term for this institution.»
> — Oliver 1989, cap. 3, p. 283 (n. 131)

> «Other terms, such as **maraca** /maraka/ are probably of Taíno origin and
> possibly brought in along with **cacique** /kasike/ and many others by the
> Spanish, all of whom had to go through Hispaniola before reaching Venezuela.
> To that end, **one must be careful about some terms (e.g. barbacoa) offered
> by the Spanish as "native"**…»
> — Oliver 1989, cap. 2, p. 151

*(Esa tercera cita ya estaba en `4-fuentes/oliver-1989-cap2.md` §«Qué falta»
punto 5, como tarea de revisar tres etiquetas del lexicón — `barbacoa`,
`maraca`, `cacique`. Lleva ahí desde que se minó el capítulo y sigue sin
hacerse. Las dos del cap. 3 son nuevas.)*

**La regla operativa que sale de ahí**: para llamar «esfera» a una voz taína
hace falta atestación indígena **independiente del castellano** en el área —
van Buurt o Gatschet en las islas, Zavala o Medina en Paraguaná. Sin eso, la
hipótesis por defecto es el hispanismo del XVI y la etiqueta degrada.

Y el lexicón **ya aplicó ese razonamiento una vez, bien**: `hamaka` lleva
escrito en sus propias notas *«se queda RECONSTRUIDA (mismo motivo que kanoa:
hamaca es préstamo taíno del propio español)»*. Lo que falta es aplicarlo al
resto.

### Vector 2 — ⭐⭐ y al revés: había caquetíos hablando en Santo Domingo desde 1513

Este es el que el proyecto **no** tenía escrito, y corta en la dirección
contraria.

> «fueron llevados como esclavos a Santo Domingo como dos mil indios de tales
> islas (y probablemente de la costa firme cercana) por el capitán Diego de
> Salazar, tocando algunos a Ampies, quien **conversándolos** observó que
> parecían "gente de más razón y habilidad que otros indios destas partes".»
> — Arcaya 1920, p. 158

Y Oliver lo corrobora por el lado del contenido: Ampíes obtuvo su información
sobre el oro y las piedras del interior «from the Caquetío, who were his
**personal servants in Hispaniola**», y razona que **tenía** que venir de ellos
porque Ampíes no había estado aún en Falcón ni en las islas y su enviado nunca
llegó a la Guajira (cap. 3, p. 212).

**Por qué es oro.** Oliver ya usó este argumento una vez, y en una sola
dirección: duda de que `datihao` sea caquetío porque *«Oviedo's long time
residence in Hispaniola may be a factor here»*, y concluye que probablemente
fuera *«equally shared by both Taíno and Caquetío»* (cap. 2, n. 42, p. 146).
Con Arcaya p. 158 delante, **el mismo argumento corre al revés**: en Santo
Domingo había hablantes de las dos lenguas, y la residencia de un cronista allí
no decide de cuál copió. Una voz «de La Española» no es automáticamente taína.

*(El lexicón tiene `datihao` como `caquetío-atestiguado` sin la reserva de
Oliver. Ya estaba anotado en `4-fuentes/oliver-1989-cap2.md`; sigue abierto.)*

### Vector 3 — el mejor candidato local es un topónimo de Paraguaná

`Caçicure` / `Casicure`, el nombre colectivo de las aldeas de Paraguaná, que
Oliver deriva del lokono `kassikoan` 'habitar, tener casa' y relaciona con el
taíno `kasike` 'cabeza de casa(s)' (cap. 3, p. 262). ⚠️ No es contacto: es
cognado de familia. Pero es un topónimo vivo cuya etimología pasa por el taíno,
y eso es de T4.

---

## 4. La evidencia, por clase y por época

### Arqueológica

- **La serie dabajuroide para en las ABC.** Marcador arqueológico del caquetío,
  ~1.300 km de litoral, c. 800–1600 d.C., de la costa occidental de Falcón
  hasta las Antillas Neerlandesas — y no más allá (`ecologia-013`; Antczak &
  Antczak 2015). Ninguna fuente del repo menciona ostionoide, chicoide ni
  meillacoide en Falcón o las ABC, ni dabajuroide en las Antillas Mayores.
  ⚠️ El límite es un negativo medido sobre lo que el repo tiene, y la obra que
  lo zanjaría está en 0 bytes.
- **El eje largo apunta al OESTE.** Las vajillas de Los Médanos A/B son *«precisely
  those of the latest ceramic complex found in the Ranchería valley»* (Oliver
  cap. 4), con fechas congruentes con lo que las crónicas decían del comercio
  caquetío en la Alta Guajira; el pico del contacto Guajira ↔ Los Médanos está
  en **1400 d.C.**, dentro de la ventana simulada (cap. 3, p. 200). Apoyos
  independientes: motivos avemorfos guajiros en la cerámica arubeña
  (Martínez-Cruzado 2003) y las «piedras verdes» ligadas a la Sierra Nevada de
  Santa Marta. **Cuando la polity costera comercia lejos, comercia al oeste.**
- **Al este llega a Las Aves y Los Roques**, en disputa con caribes desde 1200
  d.C. (Antczak 2017 p. 157). De ahí al arco antillano, nadie ha trazado una
  ruta — `horizonte-de-contacto` ya lo dejó escrito.
- La jadeíta del Motagua en las Antillas **Menores** es conexión de objeto de
  época **saladoide (~250-500 d.C.)**, mil años antes de la ventana, y no toca
  Falcón.

### Genética — y qué dicen EXACTAMENTE

**Schroeder 2018**: el genoma de **una** mujer lucaya de Preacher's Cave
(Bahamas), muerta ~500 años antes del contacto, a 12,4×. Sale más próxima a los
**palikur** y a otros hablantes arahuacos de las cuencas del Amazonas y el
Orinoco, por cuatro métodos independientes. En el análisis por haplotipos
(ChromoPainter) los arahuacos copan los primeros puestos y ahí entran los
**wayuu**, que no salían por SNP; los autores lo atribuyen a flujo
ístmico-colombiano que los wayuu tienen y el taíno antiguo no. **Cero menciones
de caquetío, dabajuroide, Aruba o Paraguaná** en todo el texto.

⚠️ Eso mide **de dónde salió una población**, a escala de milenios. No mide con
quién trataba en el siglo XV. «Los taínos vienen del norte de Sudamérica» + «el
caquetío es arahuaco del norte de Sudamérica» **no** compone «se trataban».

**Martínez-Cruzado 2003**: 9 de 13 mtDNA amerindios arubeños son del haplogrupo
**D**; la lucaya de Schroeder es **B2**, que el propio paper señala como raro en
el Caribe de hoy. Haplogrupos distintos — pero las muestras arubeñas son de
población **moderna**, la firma del mestizaje colonial. n=1 antiguo contra n=13
modernos no da para afirmar nada, y la nota de Schroeder en el repo ya lo
declara como pregunta bien planteada. Aquí queda igual.

### Etnohistórica — precontacto: nada

Ningún cronista del repo describe tráfico precolombino entre la costa caquetía
o las ABC y las Antillas Mayores. El único relato de primera mano de esa red
antes de que los españoles la reorganizaran es Anglería sobre el viaje de Niño
y Guerra (1499-1500), y la red es **continental y de eje este-oeste**:

> «Preguntados los curianenses de dónde conseguían aquel oro, indicaban que lo
> traen de cierta región llamada **Cauchieto**, que distaba **hacia el
> Occidente**, por costa derecha, seis soles… También éstos llevaban perlas al
> cuello, pero se les proporcionaban de **Curiana** á cambio de oro.»

Medido en el vol. 1 (421 KB): «Curiana/Curian» 12, «Cauchie» 5, «Paria» 23,
«perlas» 38 — y «lucay» 0, «Hispaniol» 0, «Gigante» 0, «caquet» 0. Las
provincias que enumera son todas de tierra firme.
*(Qué nombra «Curiana» en Anglería sigue en disputa, #33; lo que la cita
sostiene es la forma de la red, no la identificación del lugar.)*

**Las dos afirmaciones positivas que existen, y por qué no suben:**

1. **Antolínez 1944** (vía Morón 2012) — la única del repo: *«Los Zemi o ídolos
   de piedra del Estado Falcón, son exactamente iguales a los de los Taínos de
   Cuba; las denominaciones geográficas de esta isla, y la de los distritos
   políticos de la nación Kaketía… coinciden sorprendentemente.»* Ni un objeto
   listado, ni un museo, ni un número de catálogo, ni uno de los topónimos que
   «coinciden». Es un artículo de prensa (El Universal, 9-IX-1944) de un
   difusionista de los cuarenta — el mismo que deriva `capo` de un étimo tupí y
   sostiene que el taíno tiene 50 % de voces guaraníes. `hipotetico`.
   **Lo que lo haría dato**: un catálogo. Los cemíes de Falcón están publicados;
   comparar dos corpus de láminas es trabajo de una tarde.
2. **Esteves 1989** — el «estrato taíno / caribe insular» de Paraguaná (Amuay,
   Elegüey, Maragüey, Jamaica, Maitiruma). **Ya degradado por el repo**: es
   parecido de sonido sin documento, las cuatro voces que aduce (batey, mamey,
   caney, carey) son taínas del español general —precisamente las del vector
   1—, la etiqueta «caribe insular» nombra una lengua arahuaca, y B.6 midió
   0/5 en Oliver §3.2.4.

### Etnohistórica — colonial: es lo único que hay

| Año | Qué | Fuente |
|---|---|---|
| 1499 | Curazao = «Ysla de Gigantes», Aruba = «Ysla de Brasil» | Oliver cap. 3 p. 249; Arcaya (Castellanos) |
| desde 1502 | Redadas en la costa de Falcón *«especially designed to supply Hispaniola with Indian labor, since the local Taíno population had dramatically decreased due to disease»* | Oliver cap. 3 p. 250 |
| **1513** | Curazao, Aruba y Bonaire declaradas «islas inútiles»; los colonos de **Santo Domingo y Puerto Rico** autorizados a llevarse indios. «La gran saca de **dos mil** indios que hizo **Diego de Salazar**, llevándoselos **sin duda** también de Paraguaná» | Arcaya 1920 p. 153 |
| 1513-15 | Ampíes compra caquetíos en La Española, raideados por **Martín Baso Zabala** desde Aruba, Curazao «and probably the Mainland», y los mete en su casa como indios de servicio | Oliver cap. 3 pp. 212, 250 |
| 1525 | Ampíes obtiene de esos caquetíos la información sobre el oro y las piedras de tierra firme | Oliver cap. 3 p. 212 |
| 1520-26 | Manaure *«sent caciques to Curaçao and Aruba, and even Hispaniola»* | Oliver cap. 3 p. 266 |
| 1526-27 | 150-200 devueltos a Aruba y Curazao, *«mainly Caquetíos, but some Arawaks from other Caribbean islands»* | Martínez-Cruzado 2003 (Hartog 1961); Oliver p. 251 |
| 1530s | Caquetíos y bubures de Juruara herrados en Maracaibo y enviados a Santo Domingo (esfera **occidental**) | Oliver cap. 3 p. 201 |

**La relación caquetío↔taíno mejor documentada que existe es ésta**: los
caquetíos fueron llevados a La Española **a sustituir a los taínos que se
morían**. No es una esfera de interacción; es su opuesto.

🔴 **Discrepancia que NO se promedia**: Arcaya da 1513 y Diego de Salazar;
Oliver da 1515 y Martín Baso Zabala (y menciona además un raid de «Baso Zavala»
en 1513). Puede haber una o varias sacas. Cerrarlo pide Ramos Pérez 1978 y
CoDoIn 1864/1868.

⚠️ Y el «sin duda» del tramo Paraguaná/costa es de **Arcaya**: el documento
cubre las islas. Se registra como inferencia suya.

---

## 5. Lo que propongo entrar (regla 5: lo decide Miguel)

**Una** entrada en `3-mundo/etnias.yaml`:

```yaml
- id: etnia-009
  nombre: taíno
  etiqueta: hipotetico
  familia_linguistica: arahuaca
  polity_caquetia: costera        # con sus islas: Oliver las mete dentro
  tipo_de_contacto: ninguno       # ninguno documentado en precontacto
  intensidad: ninguna
  procedencia: {obra: oliver-1989-cap3, pagina: "250"}
```

**Por qué `costera` y no otra**: no hay una polity insular que separar. Oliver
es literal — *«the largest contiguous territory under a single Caquetío polity
comprised, at the time of Contact, the coastal plains of what is today the
State Falcón, Venezuela, **including the Netherland Antilles**»* (cap. 3,
p. 198). Cruzar de Cumarebo a Curazao es moverse **dentro** de la polity.

**Por qué `hipotetico`**: `atestiguado` diría que la relación existió en la
ventana simulada, y no consta. `canon-simulacion` diría que la inventamos para
el elenco, y tampoco — el taíno sí está en el motor, pero entró por la puerta
del léxico, no por la del mundo.

Y **dos hechos de corpus** (`geografia_politica-014` y `-015`): la deportación
colonial, y el horizonte marítimo de la polity con sus tres tramos documentados
y el cuarto que no existe.

### 🔴 Un problema de esquema que hay que decidir

**`etnias.yaml` no tiene campo `epoca`, y el 9.º guardián no lo valida.** Sin
él, esta ficha —con `procedencia` válida y `polity_caquetia: costera`— pasa el
validador **diciendo que hay un vecino documentado de la Curiana**, cuando lo
documentado es de 1513 y de signo contrario.

Es el mismo problema que `asentamientos.yaml` ya resolvió partiendo `etiqueta`
/ `atestacion` / `precontacto`. Propongo `epoca` con vocabulario cerrado
(`precontacto` · `contacto-temprano` · `colonial` · `varias`), exigido cuando
`polity_caquetia: costera`. **Toca `curiana_sim/compilar_etnias.py`, así que es
decisión tuya, no de esta campaña.** Mientras tanto la ficha lo lleva como
`epoca_propuesta` y el validador lo ignora.

---

## 6. Consecuencia para el experimento — opciones, sin decidir

**Lo medido**: el taíno es, con diferencia, la lengua más presente de la esfera
en el prompt — **25 de las 43** voces que `[Voces de fuera]` puede mostrarle a
un tier 1 (58,1 %), y **35 de los 40** préstamos registrados en toda la base.
Y entre esas 25 están **`cacike` y `naboria`** — las dos que Oliver nombra
expresamente como traídas por el español desde La Española — y **`kunuku`**,
cuya propia entrada del lexicón dice *«kunuku es la forma papiamenta del conuco
taíno, **no** un caquetío insular»*.

**Lo que NO cambia**: nada de esto toca la decisión del 2026-09-17 («el
producto de la esfera ES la esfera»). Esa decisión no se apoyaba en que el
taíno fuera vecino, sino en que el caquetío no tiene voz propia para casabe.
Los cinco casos que la sostienen —`cazabi`, `maisi`, `yuca`, `batata`,
`papaya`— son **productos**, y son exactamente los que la skill §3 declara
préstamo areal normal. Esta parcela no los toca.

**Lo que ya juega a favor**: «la etiqueta manda» (2026-09-18) ya sacó del
bloque, por un motivo completamente distinto —no tener gemela indígena—,
cuatro de las voces que Oliver marca: `caney`, `huracan`, `cemi` y `bejique`
están en `SIN_FORMA_DE_LA_ESFERA` y no se enseñan. La convergencia es
casualidad, pero reduce el problema antes de empezar.

### Las opciones

**A. No tocar nada.** El taíno entró a `ESFERA_DE_CONTACTO` por una decisión
que no dependía de la vecindad, y un negativo no obliga a mover el motor.
*En contra*: el bloque le enseña a un agente de Paraguaná del siglo XV la
palabra para 'jefe' y la de 'servidor del cacique' cuya única vía documentada
es la boca de un español del XVI. No es un préstamo de esfera: es un
anacronismo con etiqueta de préstamo.

**B. Partir la etiqueta taína por VECTOR, sin tocar el scorer.** (b1) voces con
atestación indígena independiente del castellano en el área —van Buurt o
Gatschet en las islas, Zavala o Medina en Paraguaná— siguen enseñándose; (b2)
voces cuya única vía documentada es el español de Hispaniola salen de
`[Voces de fuera]`, igual que salieron las de `SIN_FORMA_DE_LA_ESFERA`.
*A favor*: es la regla que Oliver formula, y la que el lexicón ya aplicó bien
una vez con `hamaka`. No mueve el score: el que diga `cacike` sigue contando.
*En contra*: hay que auditar 25 voces una por una, con etiqueta y cita cada
una. Es una campaña, no una tarde.

**C. Dejar sólo las voces de PRODUCTO** y sacar las de institución y ritual
(`cacike`, `nitaino`, `naboria`, `batey`, `areito`, `dujo`, `maboya`,
`akcicyaa`). *A favor*: que se comparta una planta es préstamo areal normal;
que se comparta el vocabulario de la organización social es otra cosa, y de la
institución taína no hay ni un hilo de evidencia de contacto. *En contra*: el
criterio producto/institución lo pongo yo, no una fuente — el eje de la skill
§3 es sobre **filiación** (pronombres, numerales, morfemas), no instituciones.
Y `maboya` ya se dijo en un run.

**D. Dejar el motor quieto y arreglar sólo el MUNDO**: entrar `etnia-009` y los
dos hechos de `geografia_politica`, para que la próxima sesión no vuelva a
preguntar. La decisión sobre el prompt se toma después, con la auditoría de B
hecha. *A favor*: separa lo medido (el mundo) de lo que hay que auditar (las 25
voces), y no mueve `score` a mitad de serie. Y es literalmente lo que pediste:
«anexarlas a nuestra esfera» — la anexión, cuando la evidencia dice que no hubo
trato, es escribir que no lo hubo.

### Mi recomendación

**D ahora, B como campaña siguiente.** A se descarta porque `cacike` y
`naboria` están en el prompt hoy y ahora sabemos qué son. C se descarta porque
el criterio es mío y porque cuatro de las voces que más molestarían ya están
fuera por otra puerta.

---

## 7. Lo que NO se encontró (las negativas valen — skill §6)

- Ningún objeto antillano en Falcón, Paraguaná ni las ABC: ni cerámica
  ostionoide/chicoide/meillacoide, ni guanín, ni cemí atribuido con catálogo.
- Ningún objeto dabajuroide en las Antillas Mayores.
- Ningún cronista que describa travesía, comercio ni noticia entre la costa
  caquetía y las Antillas Mayores antes de 1499.
- **Ninguna cifra de distancia de travesía con fuente en el repo.** Paraguaná ↔
  Aruba está (`~25 km`, `ecologia-021`); de las ABC a La Española no hay
  ninguna, y no se pone a mano.
- **Nada sobre los lucayos llevados a las perlas de Cubagua**: cero menciones
  de «lucay» en *todo* el repo, y cero en Anglería vol. 1 y en Arcaya. Es una
  deportación real y documentada en otra literatura, pero el repo no la tiene,
  y además Cubagua es de la costa oriental — fuera de la polity costera.
- **Ninguna lista Swadesh del caquetío contra el taíno.** El Apéndice A de la
  tesis de Oliver (las listas de 100 palabras para lenguas arahuacas, pp.
  559-594 impresas) sigue con el OCR ilegible (#62). Es la pieza que mediría de
  verdad la distancia caquetío↔taíno.
- **Nada sobre la recuperación contemporánea del taíno ni su escritura.**
  Decisión tuya: no es dato del siglo XV, y no se buscó.

---

## 8. Obras que harían falta — anotadas, no descargadas

| Obra | Por qué | Derechos |
|---|---|---|
| **Rouse & Cruxent 1963**, *Venezuelan Archaeology* | Define el dabajuroide frente a las series antillanas. Ya en la bibliografía; archivo en 0 bytes | En copyright (Yale UP); préstamo controlado en archive.org |
| **Rouse 1992**, *The Tainos* | Las series antillanas (saladoide → ostionoide → chicoide): diría si el borde norte del dabajuroide y el borde sur del ostionoide se tocan o dejan vacío | En copyright (Yale UP) |
| **Keegan & Hofman 2017**, *The Caribbean before Columbus* | La síntesis moderna; trata expresamente las conexiones continente↔islas. También cerraría Keegan 1989, que el corpus cita sin haber leído entero | En copyright (OUP) |
| **Fernandes et al. 2020**, Nature 590 | La genómica del Caribe precontacto con varias poblaciones. Ya en la bibliografía; archivo en 0 bytes | **Acceso abierto en PMC** — descargable |
| **Boomert 2000**, *Trinidad, Tobago and the Lower Orinoco* | El eslabón por el que el taíno entró a las Antillas: documentaría que las dos rutas no se cruzan | En copyright |
| **Antczak & Antczak 2006**, *Los ídolos de las Islas Prometidas* | Los Roques y Las Aves de primera mano: el borde oriental del mar caquetío | En copyright |
| **Ramos Pérez 1978** (la monografía, no la reseña) | Resolvería la discrepancia 1513/1515 y Salazar/Baso Zabala, y daría el texto completo de lo que Ampíes dijo de sus caquetíos | no verificado |
| **CoDoIn 1864 y 1868** | Las cartas de Ampíes al Rey que Oliver cita por página | **Dominio público** (s. XIX) |
| **Hartog 1961/1968** | La cronología de deportaciones y retornos que dos de nuestras notas usan de segunda mano | En copyright |

---

## 9. Lo que vi de paso y merece otra campaña

1. **La vía de cada voz «de la esfera» no está declarada en ninguna parte.**
   `kunuku` tiene en sus `notas` que es papiamento, no caquetío insular, y aun
   así se enseña. `hamaka` tiene el razonamiento correcto y se aplicó. No hay
   un campo que diga por dónde llegó una voz, así que la decisión depende de
   que alguien lea las notas. Es la misma familia de patología que la auditoría
   de morfología encontró: se enseña por una puerta y se documenta por otra.

2. **`etnia-008` (el caribe del elenco) es el único vecino de la polity
   costera, y es canon-simulación.** El registro de vecinos, tal como está, dice
   que la sociedad que simulamos no tenía ningún vecino documentado. Eso o es
   un hallazgo enorme o es un hueco de minería, y ahora mismo no está dicho
   cuál de los dos.

3. **Los cemíes de Falcón.** Antolínez afirmó en 1944 que son «exactamente
   iguales» a los de Cuba. Está publicado por los dos lados. Comparar los dos
   corpus con láminas convertiría la única afirmación positiva de esta parcela
   en dato o la enterraría, y en los dos casos sería progreso.
