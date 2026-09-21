# Campaña del taíno — T1: Oviedo y Valdés 1851, vol. I

**Fecha**: 2026-09-21 · **Rama**: `campana/taino-oviedo`
**Datos**: [`6-fusion/taino_oviedo_valdes_1851.yaml`](../taino_oviedo_valdes_1851.yaml)
**Las cifras**: `python 6-fusion/scripts/medir_taino_oviedo.py --check`

---

## 0. Lo que resultó falso al medirlo

**La ficha de esta obra decía que el PDF no se podía leer. Se puede.**

`4-fuentes/oviedo-y-valdes-1851.md` (verificado el 2026-07-29) daba el archivo
por «🔴 corrupto»: `pypdf` falla, `pdftotext` extrae **0 caracteres**, veredicto
«no procesable con las herramientas actuales», y encima «sería el volumen
equivocado». De ahí salía la etiqueta `estado_minado: no-disponible` y la frase
«**la deuda documental más grande del proyecto**».

Medido hoy:

| | |
|---|---|
| El archivo está **truncado** | 0 `%%EOF`, 0 `startxref` — por eso los dos extractores se plantan |
| **MuPDF lo abre en modo reparación** | reconstruye la tabla de referencias: `is_repaired = True` |
| Páginas | **766** |
| Capa de texto | **3.000.938 caracteres**, OCR antiguo, 12 páginas del PDF casi vacías |
| ¿Volumen equivocado? | **No.** Portada: «HISTORIA GENERAL Y NATURAL DE LAS INDIAS… PRIMERA PARTE. MADRID… 1851», ed. Amador de los Ríos, libros I-XIX |

Es exactamente la trampa que CLAUDE.md ya tiene escrita —«`pypdf` ≠
`pdftotext`»— con un tercer extractor que nadie había probado. **La regla
necesita una tercera columna: cuando los dos fallan, probar MuPDF antes de
declarar una fuente ilegible.** Hay otras dos obras en
`fuentes_caquetios/` con 0 bytes y varias marcadas como no procesables: merece
un barrido (ver §6).

### Pero hay un límite real, y es duro

La capa de texto sobrevivió; **la imagen escaneada no, a partir de cierto
punto**. Medido página a página sobre las 766:

- impresas **1-154**: la página se renderiza → **la forma se verifica con los ojos**
- impresas **155-618**: `format error: object is not a stream` → **sólo queda el OCR**

Y esto importa más de lo que parece, porque:

> **El editor de 1851 pone las voces indígenas en CURSIVA, y el OCR falla justo
> en la cursiva.** O sea: el OCR corrompe precisamente la palabra que se busca.

Medido, con la página delante:

| OCR dice | La página dice | p. |
|---|---|---|
| `buhüí` | **`buhití`** | 126 |
| `gemi` | **`çemi`** | 126 |
| `hixa` | **`bixa`** | 146 |
| `huhio` | `buhio` | 163 |
| `ca9abi` / `cagabi` | `caçabi` | 268 |
| `atjre` | ¿`ayre`? — sin imagen, sin resolver | 500 |

Y no se puede detectar la cursiva por software: la capa es `GlyphLessFont`, sin
información de fuente. Se localiza con el OCR y se lee con los ojos, o no se
lee.

**Consecuencia para todo lo que sigue**: cada entrada del YAML declara
`verificacion: imagen` o `verificacion: ocr-sin-imagen`. De las 89 formas
transcritas, **28 están verificadas en imagen y 47 son lectura de OCR** (14
parciales). Las de OCR **no se fusionan sin ver la página** en otra copia.

---

## 1. Veredicto

**Oviedo vale, y mucho.** Es lo que el encargo suponía: el cronista que más
vocabulario da con glosa. En 82 páginas impresas citadas salen **89 formas**,
de las cuales **64 no están en el lexicón**. Y **30 de las 52 entradas taínas
del lexicón quedan con cita** gracias a esta obra — de 0 con
`procedencia.obra` que había esta mañana.

Lo que lo hace bueno no es el número: es que Oviedo **glosa**. «hico quiere
deçir lo mismo que soga ó cuerda»; «çemi… es el mismo que nosotros llamamos
diablo»; «que los indios llaman caçique, assi como los chripstianos decimos
rey». Eso es un diccionario disperso en una crónica.

Y glosa **contra** la costumbre cuando hace falta: «llaman los indios *tabaco*,
**é no á la hierva** ó sueño que les toma (como pensaban algunos)».

---

## 2. Lo que hay que decidir — opciones para Miguel

### A. ¿Se fusionan las 30 citas al lexicón?

Las 30 entradas taínas del lexicón que Oviedo puede citar hoy no tienen
`procedencia.obra`. Colgarles `oviedo-y-valdes-1851` con libro/capítulo/página
las saca de la deuda `sin-procedencia` (regla 8).

- **A1** — Fusionar las **que están verificadas en imagen** y sólo esas
  (`areito`, `dujo`, `cemi`, `bejique`, `tabako`, `bixa`, `huracan`, `hutia`,
  `iwana`/`higuana`, `cacique`/`cacike`). Es lo más conservador y lo que la
  regla 2 pide: en duda, degradar.
- **A2** — Fusionar las 30, marcando las de OCR con una nota de verificación
  pendiente en `notas`.
- **A3** — No fusionar nada hasta conseguir una copia con imagen completa.

**Recomiendo A1.** Cierra hoy la mitad del hueco sin meter ni una forma que no
haya visto un par de ojos, y deja A2 para cuando llegue la copia buena.

### B. ¿Qué se hace con `eracra`?

`eracra` es el mejor hallazgo léxico de la parcela:

> «las quales comunmente llaman *buhio* en estas islas todas (que quiere deçir
> casa ó morada); pero propriamente **en la lengua de Hayti** el buhio ó casa
> se llama *eracra*» — Lib. VI cap. I, p.163

Es la **única** vez en el volumen que Oviedo separa la voz pan-insular de la
voz «propia de la lengua», y nombra la lengua. El lexicón tiene `bohio`/`bohío`
(la de koiné colonial, la que pasó al castellano) y **no tiene la propia**.

- **B1** — Entra a la esfera como `taíno`, con la cita, cuando esté verificada
  en imagen.
- **B2** — Entra ya, etiquetada y con la verificación pendiente anotada.
- **B3** — Se queda en `6-fusion/` hasta la copia buena.

**Recomiendo B1**, y que se verifique pronto: es una página, la 163.

### C. `datihao` — la deuda documental, y el problema que abre

**La voz está.** Libro XVI cap. V, p.473, en boca del caçique **Agueybana**:

> «Adelante, adelante, á mi *dalihao* (que quiere deçir **mi señor, ó el que,
> como yo, se nombra**), dexa ese bellaco.»

La ficha decía que `creencia-001` (*borattio* / *datihao-diao* = «señor»)
colgaba de Jahn p.213 n.29, que cita «el apéndice al tomo IV» de Oviedo, y que
el rastreo del 2026-08-14 verificó que **ese apéndice no existe**. Conclusión de
entonces: cadena de cita irreproducible, prioridad bajada.

Pues la voz estaba en el **tomo I**, que el repo ya tenía, y en una página que
nadie podía leer porque el PDF se daba por roto.

**Pero al leerla aparecen tres problemas, y son más interesantes que el
hallazgo:**

1. **No es dato caquetío.** Oviedo la pone en boca de un caçique de
   **Boriquén (San Juan)**, en el libro de la conquista de San Juan. El corpus
   la trata como caquetía. Eso es un salto de isla a Tierra-Firme que nadie
   decidió (regla 4) y que además es colonial (regla 3).
2. **No es segunda atestación independiente.** Jahn y nosotros bebemos del
   mismo Oviedo (skill §8). Lo que cambia no es el número de fuentes: es que
   ahora se puede leer la primera.
3. **La glosa tiene dos mitades y el corpus sólo recogió una.** «mi señor» **y**
   «el que, como yo, se nombra» — lo segundo es el hermanamiento por
   intercambio de nombre, una institución, no un título.

Y `borattio` **no está**: `borat*` = 0 en todo el volumen, verificado.

- **C1** — Se abre issue de corrección sobre `creencia-001` y se reetiqueta el
  dato como **taíno de San Juan**, no caquetío; el uso caquetío queda como
  proyección explícita o se retira.
- **C2** — Se deja como está y se anota la duda en `notas`.
- **C3** — Se espera a verificar `dalihao` vs `datihao` en imagen antes de
  tocar nada.

**Recomiendo C3 y luego C1.** La forma exacta no se puede leer (p.473 > 154) y
`l`/`t` es la confusión de OCR de manual; pero la **atribución a San Juan** no
depende de la grafía y ya es firme. O sea: la corrección epistémica se puede
preparar ya, la cita literal no.

### D. Tres glosas del lexicón que la fuente contradice

Ninguna se toca aquí (§8: no se reescribe una glosa en una minería).

| Clave | El lexicón dice | Oviedo dice | p. |
|---|---|---|---|
| `caney` | «bohío **rectangular** del **cacique**» | el caney es la casa **redonda**; la de caçiques y principales es la otra, «á dos aguas y luenga» | 164-165 |
| `batey` | «**plaza** central del poblado, cancha de…» | el batey es **el juego** de pelota: «el juego de la pelota que ellos llaman batey» | 163, 471 |
| `tabako` | «tabaco (Nicotiana tabacum), pipa ceremonial» | el tabaco es **el cañuto**, «**é no á la hierva**… como pensaban algunos» | 131 |

Y dos más suaves: `piragua` («canoa grande» — para Oviedo es la **misma** canoa
con otro nombre según la isla, no un tamaño) y `huracan` («espíritu del viento
destructor» — Oviedo lo da sólo como nombre del temporal).

- **D1** — Un issue por glosa, con la cita.
- **D2** — Un solo issue con las cinco.

**Recomiendo D2**: son la misma patología (glosa enriquecida más allá de lo que
la fuente sostiene) y conviene verlas juntas.

### E. Lo de la costa de Venezuela

Tres voces y un topónimo, y van arriba del YAML porque es lo que este proyecto
busca:

- **`Paraguana`** (p.205) — «que **los indios llaman** á aquella provinçia
  Paraguana», en el camino de Coro al cabo de Sanct Román. Atestación de 1548,
  con testigos juramentados ante la Audiencia en 1540 y nombrados. Es la fuente
  **más antigua del repo** para el nombre y llega por vía independiente de
  Esteves y de Medina.
- **`comoho`** (pp.313-314) — «en la provinçia de **Venezuela** en la
  Tierra-Firme se llama comoho»: el cardón de las tunas y su fruta. Declarado
  dos veces, en título y cuerpo. Es ecología del **cardonal**, el paisaje del
  corpus caquetío (`ecologia-007/018/032`).
- **`hado`/`hayo`** (p.206) — «en la gobernación de Venecuela se dice *hado*»,
  la hierba de mascar que en Nicaragua es `yaat` y en el Perú `coca`. **El OCR
  da `hado` dos veces, pero `hado` es castellano y el contexto pide voz
  indígena: la lectura esperable es `hayo`**, que además es clave del lexicón.
  Sin imagen no se decide. **Degradada** (regla 2).
- **`yaguaraha`** (p.326) — «llaman los indios á esta fructa yaguaraha», en
  **Cubagua**. Costa de Venezuela, pero la oriental: guaiquerí/cumanagoto, no
  caquetío. Se anota lejos.

⚠️ **Oviedo no dice «caquetío» ni una vez en este volumen**: `caquet` = 0,
`caiquet` = 0, `Curiana` = 0, `Coquibacoa` = 0, `Arubar?` = 0. Todos
verificados con variantes (regla 6). «Provinçia de Veneçuela» en 1548 es la
gobernación de los Welser entera, no una etnia: `comoho` y `hado` **no se
pueden llamar caquetíos**, van a la esfera con la etiqueta más baja que aguante.

- **E1** — `Paraguana` a la campaña de topónimos como atestación nueva;
  `comoho` a `ecologia.yaml` como dato del cardonal; `hado` congelado hasta
  verificar.
- **E2** — Todo congelado hasta tener la copia con imagen.

**Recomiendo E1.** `Paraguana` y `comoho` no dependen de una letra dudosa, y
`Paraguana` es demasiado buena para dejarla esperando.

---

## 3. Qué se preguntó y qué dio

**La pregunta**: ¿qué voces da Oviedo COMO de la lengua de La Española (o de
Cuba, San Juan, Jamáyca, los lucayos), con qué glosa y en qué página?

**Dio** (`--check` emite las cifras):

- 89 formas transcritas, 89 distintas, en 82 páginas impresas
- por sección: costa de Venezuela 4 · la Española 54 · otras islas 25 · no taíno 6
- 18 campos tocados (planta, animal, rito, casa, autoridad, alimento, cultivo,
  navegación, objeto, topónimo, antropónimo, parentesco, guerra, ecología,
  medicina, creencia, transmisión, geografía)
- 30 de las 52 entradas taínas del lexicón quedan con cita; 64 voces nuevas

**Lo mejor, por si se lee sólo esto**: `eracra` (la voz propia de la lengua de
Hayti frente al `buhio` pan-insular) · `dalihao`/`datihao` con glosa doble ·
`buhití` (el behique, con su forma real) · las **cinco especies de batata**
nombradas (`aniguamar`, `atibiuneix`, `guaraca`, `guacarayca`, `guananagax`) y
las **tres de piña** (`yayama`, `boniama`, `yayagua`) · `curi-á` con **nota de
acentuación** de Oviedo · el censo de cuadrúpedos de la isla (`hutia`, `quemi`,
`mohuy`, `cori` y el perro).

---

## 4. Qué NO dio — y los ceros verificados (regla 6)

Un cero mide la consulta, no la fuente. Éstos se probaron con variantes:

| Se buscó | Resultado | Por qué |
|---|---|---|
| `Jamaica` | **0** | la obra escribe **Jamáyca**. El cero era de la consulta |
| `nitaino` / `nitayno` / `nilaino` | **0** | **Oviedo no da la voz en este volumen.** El lexicón tiene `nitaino` y sigue sin cita |
| `maboya` / `mabuya` | **0** | no está. El lexicón tiene `maboya` y sigue sin cita |
| `behique` / `bohique` | **0** | la voz existe, pero Oviedo la escribe **`buhití`** |
| `borattio` / `borat*` | **0** | el dato de `creencia-001` **no está aquí** |
| `cemi` con c | **0** | la obra escribe **`çemi`**, que el OCR da como `gemi` |
| `cazabe` con z | **0** | la obra escribe **`caçabi`** |
| `caquetío` / `caiquetío` / `Curiana` / `Coquibacoa` | **0** | Oviedo no nombra a los caquetíos en el vol. I |

**Y el funeral del díao no está**: ni la desecación sobre brasas, ni «beber los
huesos». Sigue en el tomo II, como decía la ficha. Esa parte de la deuda **no
se ha cerrado**.

**El «vocabulario de voces americanas» del editor tampoco existe** en este
volumen: lo que hay al final (impresas 619-648) es un **índice de capítulos**.
Sirve para localizar, no para citar. (Es coherente con lo que el rastreo del
2026-08-14 ya había verificado para el tomo IV.)

### 22 de las 52 siguen sin cita

`abba`, `acoa`, `aduri`, `agari`, `akcicyaa`, `cai`, `caiman`, `cayo`, `cobo`,
`cohiba`, `daca`, `guabina`, `kunuku`*, `manigua`, `maboya`, `mayani`,
`nitaino`, `taita`, `thigisi`, `tuna`, `wacusi`, `wagulo`, `yamosa`.

Las 9 `taíno-reconstruido` (`abba`, `acoa`, `aduri`, `agari`, `akcicyaa`,
`daca`, `thigisi`, `wacusi`, `wagulo`) **no van a salir de una crónica**: son
reconstrucciones, y esta obra no da pronombres ni partes del cuerpo. Para ésas
la fuente es Brinton o el lokono, no Oviedo.
`mayani` y `cohiba` son de **Pané**, que es otra parcela de esta campaña.

\* `kunuku` sí tiene cita (`conuco`), pero con forma distinta — ver §2.A.

---

## 5. Cobertura real: qué se leyó y qué no

**Leído de verdad**:

- **Libro V completo o casi** (impresas 124-160) — ritos, çerimonias,
  costumbres. Es el libro más denso en voces glosadas y, por suerte, casi todo
  él cae en la franja con imagen.
- **Libro VI, caps. I-IV y XIX-XX** (161-171, 205-207) — casas, batey, canoas,
  huracanes; Paraguaná y la hierva de Venezuela.
- **Libro VII completo** (263-286) — agricultura.

**Sondeado con lectura dirigida**: Libros I-IV (pp. 25, 41, 48-50, 62-68, 82,
90) · VIII (296-297, 305-306, 313-315, 323, 326) · IX-XI (376, 380) · XII-XIV
(393-396, 424, 433, 442) · XVI-XVII (471-473, 480, 500-501).

**NO leído**:

- **Libro XV** (449-461)
- **Libro XVIII** (578-585) — Jamáyca
- **Libro XIX** (586-618) — **Tierra-Firme, Cubagua, Cumaná**. Es el que más
  costa de Venezuela tiene y **queda abierto**. Sólo se sondeó.
- el grueso de los libros VIII-XVII fuera de las páginas citadas

**Por qué**: son 618 páginas impresas y la verificación por imagen sólo es
posible en 154. Se priorizó lo que pedía el encargo —costumbres, agricultura,
plantas, animales— y se dice lo que falta en vez de insinuar que se leyó todo.

---

## 6. Lo que vi de paso y merece otra campaña

1. **🔴 Barrer `fuentes_caquetios/` con MuPDF.** Si esta obra estaba marcada
   «no procesable» y tenía 3 MB de texto dentro, puede haber más. Y medido
   hoy (`find fuentes_caquetios -maxdepth 1 -type f -size 0`): **4 de los 58
   archivos pesan 0 bytes** — `Brinton_1871_Arawack_Language_Guiana.pdf`,
   `Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf`,
   `Ramos_Perez_1978_resenia_Persee.pdf` y
   `Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf`. Ojo: puede ser que sean
   marcadores de OneDrive sin descargar y no archivos vacíos de verdad —
   **eso hay que verificarlo antes de concluir nada** (el de Brinton tiene al
   lado su `.txt` de 87 KB, así que la obra sí está en el repo). Medir cuántas
   obras están mal clasificadas es media tarde y puede desbloquear varias.
2. **El Libro XIX de este mismo volumen** (pp.586-618): Tierra-Firme, Cubagua,
   Cumaná, Maracapana. Es donde más probable es que haya más voces de la costa
   de Venezuela, y está sin leer.
3. **La política «la atestiguada manda» tiene un primo en la esfera.** El
   lexicón tiene pares esfera/castellano donde la forma de la FUENTE es una
   tercera cosa: `kunuku` vs `conuco` (Oviedo), `maisi` vs `mahiz`, `bejique`
   vs `buhití`, `iwana`/`higuana` vs `yvana`, `aji` vs `axi`. Las claves
   parecen venir del papiamentu o de la ortografía moderna, no de la fuente
   del XVI. Merece una revisión propia: **¿qué grafía enseña el motor para una
   voz de la esfera, la de la fuente o la normalizada?** Es la misma pregunta
   que resolvió `FORMA_DE_LA_ESFERA` para castellano↔indígena, un escalón más
   abajo.
4. **`hamaca` y `canoa` no son claves del lexicón** pese a estar entre las
   voces taínas mejor atestiguadas del volumen, con glosa explícita. Puede ser
   decisión consciente; si no lo es, son dos huecos fáciles.
5. **Duplicados en el lexicón**: `bohio`/`bohío`, `cacique`/`cacike`,
   `casabe`/`cazabi`, `maisi`/`maíz`, `iwana`/`higuana` son cinco pares de
   claves para cinco conceptos. Tres de ellos son justamente los que
   `FORMA_DE_LA_ESFERA` mapea. Conviene medir si el motor los cuenta dos veces.
