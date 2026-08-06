---
tipo: indice
ambito: todas las fuentes del proyecto
archivos_en_fuentes_caquetios: 29
obras_distintas: 24
archivos_vacios: 4
minadas_2026_08_03: [alvarado-1921, gatschet-1885, van-buurt-2014, zavala-reyes-2015]
medido: 2026-08-04
---

# Índice de fuentes — estado real, medido

> Esta nota es la versión **viva y verificada** de la tabla de
> [[PLAN_MAESTRO]] §1.1. Cada fila se midió el 2026-07-29 abriendo el archivo:
> tamaño, páginas (`pypdf`), capa de texto (`pdftotext -f 1 -l 30`), y cuántos
> hechos del corpus y entradas del lexicón lo citan realmente.
>
> **El nombre de un archivo no es un dato verificado.** Tres de las conclusiones
> de abajo contradicen lo que el proyecto creía.

## Las tres correcciones que salieron de medir

1. **🟢 [[alvarado-1921]] SÍ tiene capa de texto.** Estaba clasificada como
   "escaneo de imagen, no extraíble sin OCR" — eso era `pypdf`. Con `pdftotext`
   salen **704 KB de texto limpio, 354 páginas**. **F3 no está bloqueada.**
   Lo mismo valía ya para [[arcaya-1920]] y [[jahn-1927]].
2. **🟢 [[oviedo-y-banos]] está disponible.** El archivo de 0 bytes que la
   hacía figurar como corrupta era `Oviedo_Banhos_1885_...`, ya borrado (#53);
   el gemelo `Oviedo_Banhos_Conquista_Poblacion_...` tiene **519 páginas con
   texto**. La obra que el programa señaló por su cobertura de sucesión cacical
   **existe**.
3. **🟢 Un archivo tenía el nombre de otra obra — resuelto (#54).**
   `Schroeder_et_al_2018_PNAS_Origins_Caribbean_Taino.pdf` contenía en realidad
   *Early human dispersals within the Americas* (Moreno-Mayar et al., Science
   2018). Nadie lo citó — por suerte. Hoy es
   `MorenoMayar_et_al_2018_Science_Early_Human_Dispersals.pdf`, ver
   [[moreno-mayar-2018]].

## ⚠️ Cómo NO medir una fuente (aprendido el 2026-08-04)

La tanda de minería de esa noche tropezó **tres veces** con la misma clase de
error, y las tres veces el síntoma fue idéntico: *un `grep` devuelve cero y uno
concluye que la fuente no habla del tema*. No era la fuente: era la consulta.

| Fuente | El `grep` que falló | Por qué | La realidad |
|---|---|---|---|
| [[antczak-2017-cariban]] | `Caqueti` → 0 | el PDF descompone acentos: `Caquet´ıo` | 8 menciones, media p. 157 sobre la frontera caquetía |
| [[oviedo-y-banos]] | `caquet` → 0 | Oviedo escribe **`caiquetía`**, y `Coriana` por Curiana | 7 menciones, incluido el pasaje de Manaure |
| [[oliver-1989-cap3]] | `Todariquiba` → 0 con `pypdf` | `pypdf` lo parte en `T odariquiba`; `pdftotext` no | 7 apariciones limpias |

Reglas que salen de ahí, y que valen para toda minería futura:

1. **Buscar por raíz corta y sin acentos** (`caquet`, `Manaur`, `Paraguan`)
   antes de dar por ausente un tema.
2. **Probar la otra receta de extracción** antes de concluir. `pdftotext` y
   `pypdf` no producen el mismo texto sobre el mismo PDF.
3. **Las fuentes coloniales no usan la ortografía moderna.** Antes de buscar un
   etnónimo o un topónimo en una crónica, leer una página al azar y ver cómo lo
   escribe *esa* obra.
4. Un cero es un resultado que hay que **verificar**, no uno que se pueda
   reportar directamente.

## Inventario medido

### Disponibles y con texto

| Fuente | Pp. | Estado de minado | Sostiene | Prioridad |
|---|---|---|---|---|
| [[zavala-reyes-2015]] | 20 | ✅ **completo (288/288)** | 7 hechos · **164 lex.** · **62 citas para F1** | hecha |
| [[oliver-1989-cap3]] | 113 | ✅ **minado** (4 barridos cerrados 2026-08-04) | **15 hechos** · 2 lex. | hecha |
| [[oliver-1989-cap2]] | 109 | **sin minar** | 1 hecho | **F5 · ALTA — la única del gate que queda** |
| [[arcaya-1920]] | 348 | minado (religión/familia) | **13 hechos** · 1 lex. | media |
| [[jahn-1927]] | 510 | parcial (3 sesiones) | **16 hechos** · 4 lex. | media |
| [[alvarado-1921]] | 354 | ✅ **minado** (109 de 1551 a fondo) | A=3 B=36 C=13 **D=57** · **18 adjudicaciones** | hecha |
| [[gatschet-1885]] | 7 (2 txt) | ✅ **minado** | 48 léxicas + 31 topón. + 6 fórmulas · **5 citas** | hecha |
| [[van-buurt-2014]] | 48 | ✅ **minado** | §6=88 · §11=29 · 180 topón. · **8 citas** | hecha |
| [[oviedo-y-banos]] | 519 | ✅ **minado** — solo el cap. III toca a los caquetíos | 1 hecho, **ascendido a cita directa** | hecha |
| [[camacho-2011]] | 13 | minado | **16 hechos** | hecha |
| [[antczak-2015-las-aves]] | 38 | minado | 7 hechos | hecha |
| [[antczak-2017-cariban]] | 45 | ✅ **minado** | 0 hechos · refuerza `parentesco-032` | hecha |
| [[adam-1879]] | 27 | minado | 1 hecho | hecha |
| [[angleria-1892]] | 460+492 | parcial (1 dato) | 1 hecho | media |
| [[las-casas-1875]] | 613 | minado — **nulo ×3** | 0 | baja |
| [[guerra-curvelo-palabrero]] | 22 | minado | 4 hechos | hecha |
| [[perea-alonso-1942]] | 926 | **descartada** (gramática lokono) | 0 | descartada |
| [[moreno-mayar-2018]] | 14 | sin minar | 0 | baja |
| [[brinton-1871]] (txt) | — | minado | **84 entradas del lexicón** | hecha |

### Bloqueadas o rotas

| Fuente | Problema | Ruta de salida |
|---|---|---|
| [[gilij-1780-1783]] | **sin capa de texto** (1323 pp. en 3 vols., verificado) | OCR externo, o la traducción de Tovar 1965 |
| [[oviedo-y-valdes-1851]] | **PDF corrupto** — y además es el volumen equivocado (el material está en t. II y t. IV) | F9 · **la deuda documental mayor** |
| [[rouse-cruxent-1963]] | **0 bytes** | F9 |
| [[fernandes-2020]] | **0 bytes** | recuperable (Nature / PMC) |
| [[ramos-perez-1978]] | **0 bytes** | recuperable (Persée) |

### 🔴 Los 4 archivos de 0 bytes

`Brinton_1871_Arawack_Language_Guiana.pdf` (el `.txt` sí existe) ·
`Fernandes_et_al_2020_Nature_Genetic_History_Caribbean.pdf` ·
`Ramos_Perez_1978_resenia_Persee.pdf` ·
`Rouse_Cruxent_1963_Venezuelan_Archaeology.pdf`

> Eran seis. Los dos duplicados muertos (`Oviedo_Banhos_1885_...` y
> `Perea_Alonso_1942_..._Lenguas_Arawak_TomoI.pdf`) **se borraron el 2026-08-04**
> (#53): ambas obras estaban ya en el repo bajo otro nombre, y el primero hizo
> figurar a [[oviedo-y-banos]] como corrupta durante meses. Los cuatro que
> quedan son huecos reales.

### Fuentes externas (sin archivo local)

Sostienen **27 hechos del corpus** — más que ninguna fuente local salvo Jahn y
Camacho. Ninguna está archivada en el repositorio.

| Fuente | Sostiene | Estado |
|---|---|---|
| [[paz-reverol-2017-2018]] | 9 hechos | leídos íntegros · **archivar** (Dialnet) |
| [[amodio-perez-2006]] | 6 hechos | leído íntegro · **archivar** (guao.org) |
| [[perrin-1992-1995]] | 6 hechos | **de segunda mano**, vía Paz Reverol |
| [[maria-lionza-culto]] | 4 hechos (`retro-abstraido`) | 2 de 5 obras leídas |
| [[keegan-1989]] | 2 hechos | **de segunda mano**, vía resúmenes |
| [[vansina-ong]] | 2 hechos | **de segunda mano**, vía reseñas |

Además, ~20 hechos de [[mapa-ecologia]] se apoyan en **literatura web general**
(Inparques, SVDB, FAO, SciELO, Atlas del Arte Precolombino) sin obra citable con
página. Es el punto más flojo del corpus para F10.

## La tanda de minería del 2026-08-03 (F3, F4, F6, F7)

Cuatro fuentes minadas en paralelo. **Ninguna tocó `curiana_lexicon.py`**: cada
una emite una propuesta para revisión humana. `curiana_sim/auditar_82.py` cruza
las cuatro y emite el veredicto por palabra para el censo de citas (F1):

```
61 confirman · 13 reclasifican · 3 conflicto de glosa · 5 sin rastro
F1 puede adjudicar con evidencia: 77 de 82 (94%)
```

**Lo que la tanda le quitó al proyecto** — y es el resultado que más vale:

- **13 entradas del lexicón resultan NO ser caquetías** según la fuente que
  debería sostenerlas. Entre ellas `piache` (*"voz cháima y tamanaca"*,
  [[alvarado-1921]] p.248 — la palabra para chamán), `ture` (cháima, y es un
  **asiento**, no una vasija), `pauji` (es un **árbol** del chaima),
  `watapana` (*"del cum. araguatapanár"*), `kunuku` (*"voz taina"*),
  `auyama`, `kukuisa`, `caraota`, `cumaragua`, `guanepe`, `bureche`, `tata`,
  `coro`.
- **3 conflictos de glosa** — la fuente tiene la palabra, con otro significado:
  `tara` (lexicón 'venado' vs. Zavala #238 **'langosta, mariposa'**), `saruro`
  ('árbol' vs. #224 **'boa'**), `corie` ('choza' vs. #90 **'armadillo'**).
  **Citarlas a Zavala sería un error.**
- **4 falsos amigos**: `caraota`, `pauji`, `piache` y `coro` no son voces del
  glosario — son la **glosa española** con que Zavala traduce a `icoroata`,
  `paugis`, `boratio`; y `coro`='cardón' no sale de Zavala (#181 es *Koro*
  'cotorra').
- **`warawara` trae la identificación de [[gatschet-1885]] sin saberlo**:
  *"Cathartes curasoica"* es la lectura de 1885. Es un **caracara**
  (*Caracara cheriway*), no un zamuro. Familia distinta.

**Lo que le dio:**

- **La cadena de custodia de Zavala aguanta**: 24 de 26 entradas con sigla `A`
  se rastrean a su página exacta en [[alvarado-1921]].
- **Triple atestación** (continental / insular 1882 / viva) en 5 formas, y
  **16 coincidencias** [[gatschet-1885]]↔[[van-buurt-2014]] entre dos
  recolecciones independientes separadas por 130 años.
- **Afijos**: `-ima` confirmado independientemente por van Buurt (Cruz Esteves
  1989); apoyo insular para `-aima`, `-ubana`, `-uru`; **cero** para `-iro`,
  `-uco`; `-bi` 'pequeño' aparece como **segundo diminutivo documentado**; y
  **`-bari` no es un afijo**. ⚠️ `-bana` tiene la forma validada y **la glosa
  en disputa** → [[DECISIONES_ABIERTAS]] D9.
- **Zavala llena 4 huecos léxicos** que el corpus daba por abiertos, incluido
  el nº 4 por presión (**especies de pez**: `cuna`, `cunaro`, `guaranaro`,
  `bagre`).
- **24 voces nuevas de nivel B** en Alvarado, del patrón *"Árbol indeterminado
  de Coro"* — las menos castellanizables del repertorio. Dos cierran huecos:
  `aiton` ("sima profunda del E. Falcón") y `tocororo` ("tallo leñoso del
  cardón"). **Van al corpus cultural, no a `VOCABULARIO_BASE`** (protocolo §5).

## Cobertura real del lexicón — quién sostiene el "atestiguado"

De las **231 entradas `caquetío-atestiguado`**, medidas por citas en `notas`
(estado **anterior** a aplicar las 62 citas que F7 recuperó — eso es F1):

| Fuente | Entradas que la citan |
|---|---|
| [[zavala-reyes-2015]] | **164** |
| [[oliver-1989-cap3]] | 2 |
| [[oviedo-y-valdes-1851]] (vía terceros) | 2 |
| Galeotto Cey (vía Zavala) | 2 |
| [[arcaya-1920]] | 1 |
| [[jahn-1927]] | 1 |
| [[alvarado-1921]] · [[van-buurt-2014]] · [[gatschet-1885]] · Las Casas | **0** |
| **sin ninguna nota** | **82 (26% de las 314 de familia caquetía)** |

> `CLAUDE.md` describía `caquetío-atestiguado` como citable a *"Galeotto Cey,
> Oviedo, Las Casas… Zavala Reyes 2015, Oliver 1989, Jahn 1927"*. En el dato,
> **es Zavala y casi nadie más**.
>
> Ese es, en una tabla, el argumento entero del eje FIDELIDAD. Tras la tanda del
> 2026-08-03 las tres fuentes que tenían penetración **cero** ya están minadas y
> con 31 adjudicaciones listas: aplicarlas es **F1**.

### Después de F1 — aplicadas las citas recuperadas (2026-08-03)

`curiana_sim/aplicar_citas_82.py` escribió **63 citas** en `notas`. De las
**231 entradas `caquetío-atestiguado`**, cuántas cita ahora cada fuente
(medido sobre `VOCABULARIO_BASE`; una entrada puede citar a más de una, y la
corroboración cruzada es deliberada):

| Fuente | Antes | Ahora |
|---|---|---|
| [[zavala-reyes-2015]] | 164 | **211** |
| [[alvarado-1921]] | 0 | **4** |
| [[van-buurt-2014]] | 0 | **6** |
| [[gatschet-1885]] | 0 | **3** |
| Galeotto Cey (vía Zavala) | 2 | 11 |
| [[arcaya-1920]] / Arcaya 1995 | 1 | 7 |
| [[oviedo-y-valdes-1851]] (vía terceros) | 2 | 6 |
| [[oliver-1989-cap2]] · [[oliver-1989-cap3]] | 2 | 5 |
| [[jahn-1927]] | 1 | 1 |
| Las Casas | 0 | 0 |

**El censo de familia caquetía sin ninguna nota bajó de 82 a 19**
(`python curiana_sim/auditar_82.py --resumen`). Las 19 que quedan **no son
deuda de minería sino de decisión**: 13 que las fuentes reclasifican a otra
lengua, 3 con conflicto de glosa — todas bloqueadas por **D10** en
[[DECISIONES_ABIERTAS]] — y 3 sin rastro real (`kama`, `koke`, `wabarsure`).
> **D10 se resolvió el mismo día**: las 16 quedaron adjudicadas y el censo bajó
> a 3. Ver «D10 aplicada» más abajo.

> Las tres fuentes con penetración cero ya no están en cero, pero el cuadro de
> fondo no cambió: **sigue siendo Zavala y casi nadie más**. Lo nuevo es que
> ahora hay 14 entradas con doble fuente independiente, y que
> [[gatschet-1885]] entró corrigiendo un error vivo (ver `warawara`, D7).

## D10 aplicada — las 16 adjudicadas (2026-08-03)

Miguel resolvió **D10 por grupos, no en bloque**: las 16 entradas que la tanda
de minería contradijo no son homogéneas, así que reciben tres políticas
distintas. Las aplicó `curiana_sim/aplicar_d10.py` (idempotente, con
`--dry-run`); ningún otro archivo del canon se tocó.

**El censo de familia caquetía sin cita bajó de 19 a 3** — solo quedan las tres
`SIN_RASTRO` reales (`kama`, `koke`, `wabarsure`).

### Grupo 1 — la fuente nombra otra lengua → se reasigna `fuente` (8)

Se conserva la forma y la entrada: siguen siendo vocabulario del mundo, solo
que prestado. `score_linguistico()` ya las trata como ajenas al caquetío.

| Palabra | `fuente` nueva | Evidencia |
|---|---|---|
| `piache` | `caribe-cháima` · **fuera del habla** | [[alvarado-1921]] p.248 *"voz cháima y tamanaca"*; en [[zavala-reyes-2015]] es la glosa española de `boratio` (#43) |
| `ture` | `caribe-cháima` | Alvarado p.301 *"voz cháima"* (Tauste) — y es un **asiento**, no una vasija |
| `pauji` | `caribe-cháima` | Alvarado p.244 — es un **árbol** (*Bumelia buxifolia*), no un ave; la voz caquetía del ave es `paugis` |
| `watapana` | `caribe-cumanagoto` | Alvarado p.163 *"del cum. araguatapanár, oreja de araguato"* |
| `auyama` | `caribe-cumanagoto` | Alvarado p.16 *"voz cum."* (Ruiz Blanco) |
| `kunuku` | `taíno` | Alvarado p.89 *"voz taina"* (Las Casas V.307); van Buurt lo repite en prosa |
| `kukuisa` | `español-colonial` | Alvarado p.84 vía Caulín I.3: *"los indios llaman **caruata** y los españoles **cocuiza**"* |
| `caraota` | `español-colonial` | Alvarado p.58; en Zavala es la **glosa** de `icoroata` (#162) |

**Dos etiquetas nuevas**, dadas de alta en
`curiana_database.py::normalize_source_language()` (y en `LANG_CATEGORIES`):

- **`caribe-continental`** ← `caribe-cháima`, `caribe-cumanagoto`,
  `caribe-tamanaco`. El lexicón ya distinguía `kalinago` (caribe **insular**) y
  `kalinago-caribe-overlay`; lo que faltaba era el caribe de **tierra firme**,
  que es el que Alvarado declara. El sufijo `-continental` es justo lo que lo
  separa del insular ya presente. El orden de las comprobaciones importa:
  `kalinago-caribe-overlay` también contiene *caribe* y se resuelve antes.
- **`español-colonial`** ← `español`. Sin categoría propia caerían en el
  `return` por defecto (`proto-arahuaco`) y se contarían como arahuacas.

**`piache` sale del habla y `boratio` ocupa su lugar.** No se borra: pasa a
`FUERA_DEL_HABLA`, un dict nuevo al final de `curiana_lexicon.py` que conserva
la entrada entera con su procedencia. Deja de sembrarse, de aparecer en prompts
y de puntuar. **El canon no se tocó**: Shaboro sigue siendo el piache de la
Curiana. ⚠️ Queda pendiente que `curiana_koine.py::FORMAS_SEED` siembra todavía
la forma «piache» a Shaboro y a Buio-sha.

### Grupo 2 — conflicto de glosa → se corrige la glosa, se conserva la palabra (6)

Política **D7**: la glosa de la fuente va verbatim a `glosa_fuente`, la lectura
descartada queda registrada en `notas`. Nada se pierde en silencio.

| Palabra | Qué pasó |
|---|---|
| `cumaragua` | `sig` → *caracol de las costas de Paraguaná* (Alvarado p.102). ⚠️ **La glosa anterior sí tenía fuente**: Zavala #93 (HB+E) «Ciruela, espuma rosada», fuerza F. Registrada en `notas` |
| `bureche` | `sig` → *bebida fermentada de casabe* (Alvarado p.34) y `cat` v_raiz → sust. ⚠️ **La glosa anterior sí tenía fuente**: Zavala #49 (AM) «Hacer, realizar», fuerza F. Y crea cuasi-duplicado con `buriche` (#50, «Licor fermentado») |
| `guanepe` | **La glosa se conserva** — Alvarado p.152 la confirma palabra por palabra. Lo que desmiente es la **geografía**: Barcelona y Guayana, no Coro. Reserva anotada |
| `tara` | ⚠️ **conflicto abierto, NO reescrita** — ver abajo |
| `saruro` | ⚠️ **conflicto abierto, NO reescrita** — ver abajo |
| `corie` | ⚠️ **conflicto abierto, NO reescrita** — ver abajo |

**Las tres que no se reescriben.** Se buscó fuente para la glosa **actual** y
**no aparece en ninguna parte** — ni en [[alvarado-1921]], ni en
[[van-buurt-2014]], ni en [[gatschet-1885]]. Pero las tres sostienen material
del canon, así que quedan con su glosa y una `notas` que deja el conflicto
**abierto y visible**. Un conflicto documentado es mejor que una corrección
inventada.

- **`tara`** — es el más fuerte de los tres y el único con **doble
  corroboración independiente**: Zavala #238 (HB+PMA+AM) «Langosta, mariposa»
  *y* Alvarado p.283, donde `tara` vale polilla o mariposa (cf. TARÍTA,
  *"mariposa o tara pequeña"*). Cero fuentes para 'venado'. Corregirla obliga a
  tocar `cultura/ecologia.yaml`, [[02_ecologia_golfete]] §10.6 y
  [[02_capas_biosfera]], donde *tara*='venado' es un argumento entero.
- **`saruro`** — su único rastro en el repo es una lista de Notion
  (*Venezolanismos de Origen Indígena*) citada en `DISENO_KOINE` §8, y allí se
  usa para confirmar la terminación **-aro/-uro**, no para sostener la glosa.
  En contra: Zavala #224 (E) «Serpiente no venenosa. Boa constrictora». Da
  nombre a **Saruro-sha**.
- **`corie`** — el hallazgo incómodo: **el propio canon ya dice armadillo**.
  `cultura/genealogia.yaml` da *"corie (armadillo)"* como tótem del linaje
  Paugis y la ficha de Buio-sha usa *"corie (armadillo) como elogio"*. La glosa
  del lexicón ('choza, habitación') contradice a la fuente **y a su propio
  canon a la vez**. Da nombre a **Corie-ko**.

### Grupo 3 — solo bajada de tier, sin cambio de lengua (2)

Etiqueta nueva **`caquetío-hipotético`**, que sigue normalizando a `caquetío`:
es deliberado — la **lengua** no se discute, solo baja la **confianza**.

| Palabra | Por qué |
|---|---|
| `tata` | [[van-buurt-2014]] la pone en su **§11** (*"less certain links to Caquetío"*), no en §6. Zavala #243 la marca fuerza D (panhispánico infantil) |
| `coro` | Zavala #181 es **`Koro` = 'cotorra'**. La glosa 'cardón grande' no sale de ninguna fuente: en Alvarado *coro* aparece 55 veces y **siempre como topónimo** |

⚠️ **`coro` no se borra y el canon no se toca**: da nombre a la ciudad de Coro y
aparece en todo el sitio público. Lo que se retira es el respaldo de la glosa.

### Composición del lexicón tras D10

`piache` sale del habla, así que el activo pasa de 1416 a **1413** entradas.

| Categoría | Entradas |
|---|---|
| wayunaiki | 781 |
| **caquetío** | **304** |
| lokono | 227 |
| taíno | 57 *(+1: `kunuku`)* |
| kalinago | 19 |
| proto-arahuaco | 8 |
| jirajaroide-contacto | 7 |
| **caribe-continental** *(nueva)* | **4** |
| kalinago-caribe-overlay | 4 |
| **español-colonial** *(nueva)* | **2** |

## Convención de estas notas

Cada nota de fuente declara en su frontmatter: `capa_texto`, `estado_minado`,
`prioridad`, `tareas` (las F# de [[PLAN_MAESTRO]] §1) y `sostiene`
(hechos del corpus / entradas del lexicón). Cuando una tarea F# se ejecute, **se
actualiza la nota de la fuente**, no un markdown suelto — ese es el punto de V1.

## Recetas de extracción que funcionan

```bash
# Regla general: si `pypdf` devuelve vacío, probar pdftotext ANTES de declarar ilegible
pdftotext -enc UTF-8 archivo.pdf salida.txt          # documento entero
pdftotext -enc UTF-8 -f 116 -l 118 archivo.pdf -     # solo unas páginas, a stdout
```

`-enc UTF-8` no es opcional: sin él, `pdftotext` emite Latin-1 y los acentos
llegan rotos.

## Enlaces

[[PLAN_MAESTRO]] · [[DECISIONES_ABIERTAS]]
