---
tipo: fuente
obra: "Palabras vivas de una lengua muerta: legado arawak-caquetío"
autor: "Zavala Reyes, Miguel Enrique"
anio: 2015
publicacion: "Boletín Antropológico 33(89), enero-junio, pp. 58-76. Universidad de Los Andes, Mérida"
genero: glosario
local: "fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf"
paginas: 20
capa_texto: si
estado_minado: completo
cobertura: "288/288 entradas parseadas (100%); 225 en el habla activa (78%), 63 fuera por diseño"
prioridad: alta
tareas: []
sostiene: {hechos_corpus: 7, entradas_lexicon: 164, citas_recuperadas_82: 62}
verificado: 2026-08-03
aliases: ["Zavala 2015", "Zavala Reyes 2015", "Palabras Vivas"]
---

# Zavala Reyes 2015 — *Palabras vivas de una lengua muerta*

## Qué es

**La fuente atestiguada central del proyecto.** Un artículo académico de 20
páginas cuyo núcleo es un **glosario caquetío compilado de nueve autores**
(identificados por siglas: PMA = Pedro Manuel Arcaya, HB = Adrián Hernández
Baño, E = Juan Esteves, AM = Angulo Molina, A = Lisandro Alvarado, GC = Galeotto
Cey, CGB = Carlos González Batista, AAM = Antonio Arellano Moreno, HP = Aníbal
Hill Peña). Es, en la práctica, **el único puente masivo** entre el lexicón
activo y una fuente citable.

> El nombre del archivo no delata al autor. Se confirmó por metadata del PDF
> (`/Title`, `/Author`, `/Subject`) en la sesión 5 — hasta entonces el proyecto
> citaba a Zavala sin tener localizado su PDF.

## Estado técnico (verificado 2026-08-03)

| Dato | Valor |
|---|---|
| Tamaño | 594 KB · 20 páginas |
| Capa de texto | **sí**, limpia |
| Receta | `pdftotext -enc UTF-8 "Palabras Vivas de una Lengua Muerta.pdf" out.txt` |
| Entradas numeradas | **288** (glosario en pp. 65-72, numeración 1-288 sin saltos) |
| Entradas parseadas | **288 / 288** por `minar_zavala_glosario.py` — el parseo **cierra** |

## Qué ha dado

**Lexicón — 164 entradas lo citan** (todas de familia caquetía). Tras la
auditoría del 2026-07-20 y el cierre F7 del 2026-08-03:

| Tier | n | Destino |
|---|---|---|
| Ya presentes antes del import | 66 | — |
| T1 afijos | 8 | `REGLAS_ZAVALA` — `-iro` (diminutivo), `-aima`, `-ima`, `-uco`, `-ubana`, `-uru`… |
| T2 nombres de agente | 8 | `buio`, `bagre`, `cunaro`, `guaranaro`, `dara`, `naure`, `cuna` — **daban nombre a agentes y no puntuaban como caquetío** |
| T3 concreto | 91 | fauna, flora, paisaje, técnica |
| T4 abstracto | 52 | verbos, cualidades |
| T5 topónimos | 45 | `TOPONIMOS_ZAVALA` — **fuera del habla**, referencia de canon |
| T5b antropónimos | 14 | `ANTROPONIMOS_ZAVALA` — idem |
| T6 descartados | 4 | `baquiro` (cumanagoto según Alvarado) + `hay`, `enea`, `guata` (ver §homógrafos) |
| **Total** | **288** | — |

**La cifra correcta de cobertura.** El antiguo *"76%, faltan 24%"* mezclaba dos
cosas distintas y sobreestimaba el trabajo pendiente:

- **Capturado**: 288/288 = **100%**. Nada del glosario queda sin leer ni sin
  clasificar.
- **En el habla activa**: 66 + 8 afijos + 151 de vocabulario = **225 (78%)**.
- **Fuera del habla por diseño**: 45 topónimos + 14 antropónimos + 4 descartes
  = **63 (22%)**. No es deuda: es curación.

**Corpus cultural — 7 hechos**: `parentesco-034/035/036` (el vocabulario de
rango *diao* / *apopo* / *boratio*), `geografia_politica-007` ("Curiana:
territorio donde estaban asentados los caquetíos", nota al pie 4),
`geografia_politica-008` (managuanare/managuarire vía González, PLINCODE p. 23),
`creencia-015b` (*Yaracuy* #284 y *Tabicure* #232).

**Correcciones que produjo.** `diao` pasó de "señor de segundo orden" (una
inferencia sin cita) a "señor principal, jefe mayor". `uriacoa` pasó de "título
del cacique mayor" a antropónimo. Ambos son el caso testigo del problema que la
[[PLAN_MAESTRO|auditoría]] persigue.

## Cierre del parseo (F7, 2026-08-03)

El regex perdía **dos entradas** y mutilaba **nueve definiciones**. Las causas
están documentadas en `RESCATES_PARSEO`, y se corrigieron en
`_normalizar_plano()` — es decir, **atacando la causa, no parcheando entradas**
(los tres patrones son únicos en el glosario, verificado por conteo).

| Qué | Entradas | Por qué fallaba |
|---|---|---|
| Perdida | **#31 Baracoica (HP)** *"Cacique de Curazao"* | Única entrada que separa siglas y definición con **punto** en vez de dos puntos; el regex exigía `:` |
| Perdida | **#104 Darubana (durabana) (AM)** *"Camino, vía"* | Único lema con variante entre paréntesis en minúscula: no casaba ni el grupo del lema (excluye `(`) ni el de siglas (1-4 letras) |
| Mutiladas | #37, #77, #116, #156, #195, #235, #275 | Arrastraban el número de plana pegado a la definición (*"…cerca del mar. 66"*) |
| Mutiladas | #143 *Guaru*, #183 *Manaure* | pypdf parte la versal inicial: *"V olturido"*, *"V ocero"* |

`extraer()` ahora **verifica** que estén las 288 y avisa por `stderr` si vuelve a
abrirse un hueco. Además se arregló el `UnicodeEncodeError` de consola Windows
(cp1252): `_forzar_utf8()`, invocada solo al correr el script como programa.

## Los 28 homógrafos con español — veredicto uno por uno

La pregunta de la revisión no era "¿colisiona con el español?" sino
**"¿es la voz caquetía, o es la palabra española con la que Zavala la glosa?"**.

- **14 siguen marcadas** — colisión real, el scoring las resuelve por contexto:
  `aca` #3, `bagre` #21, `cana` #57, `capo` #59, `carama` #64, `cocuy` #87,
  `dato` #105, `guaca` #123, `guay` #147, `samuro` #223, `sigua` #227,
  `taque` #236, `taques` #237, `tuba` #253.
  De ellas, **tres con atribución débil**: `cocuy` (indigenismo de circulación
  pan-venezolana), `samuro` (la forma coincide con el zoónimo *zamuro* y la
  glosa es geográfica), `taques` (es el topónimo Los Taques de Paraguaná; la
  glosa "salina" es la etimología del lugar).
- **11 pierden la marca** — no son palabras del español, y marcarlas hacía que
  el scorer **sub-contara** caquetío legítimo: `aco`, `apo`, `cabana` (el
  español es *cabaña*, con ñ), `icoroata`, `koro`, `quiba`, `quiva`, `ruba`,
  `supi`, `ure`, `yaro`. Ver `DESMARCADAS_F7` en el minador.
- **3 salen del habla** (nivel D del [[02_protocolo_habla_paraguanera|protocolo
  de descarte]]):
  - **`hay`** #154 *"Coca"* — coincide con el verbo español más frecuente;
    ninguna resolución por contexto compensa eso. En su lugar queda **`hayo`**
    #156, forma corriente del mismo referente, ya en el lexicón y sin colisión.
  - **`enea`** #118 *"Planta ciperácea"* — *enea* (~anea, *Typha*) **es** la
    palabra española del junco: Alvarado está dando el nombre castellano.
  - **`guata`** #146 *"Planta"* — glosa vacía (no dice qué planta) más
    homógrafo. Mismo criterio que `coroque` (*"Árbol de ¿?"*).

**Cuatro falsos amigos aclarados de paso** — no son homógrafos, son la *glosa
española* de otra entrada, y por tanto no deben tratarse como voz caquetía:
`caraota` glosa a *icoroata* #162 · `paují` glosa a *paugis* #197 · `piache`
glosa a *boratio* #43 · y `coro` **no viene de aquí**: Zavala #181 es *Koro*
'cotorra', no 'cardón'.

## D7 aplicada — glosa de la fuente vs. identificación moderna

Decidido por Miguel el 2026-08-03: se registran **las dos**, en campos
separados, y ninguna gana. `glosa_fuente` lleva el texto **verbatim** de Zavala
con número y siglas, **y es la que el agente habla**; `identificacion_moderna`
es nota auditable. Implementado en `_entrada_py()` + `IDENTIFICACION_MODERNA`.

| Palabra | `glosa_fuente` | `identificacion_moderna` |
|---|---|---|
| `cunaro` | "Pez del golfete de Coro. Promicops Guasa" [#96 (E)] | *Rhomboplites aurorubens* (pargo cunaro, de altura), SVDB. La grafía de Zavala apunta a *Promicrops itajara* (hoy *Epinephelus itajara*, mero guasa): **dos peces distintos** |
| `guaranaro` | "Pez lisa" [#139 (HB+E)] | sin resolver; *Mugil* spp. (*M. curema* / *M. incilis* en el Golfete) |

> `guaranaro` es el caso testigo de **dato que estaba en casa y no se vio**:
> [[02_ecologia]] lo daba por *"sin identificación taxonómica firme"* mientras
> Zavala lo glosaba desde siempre.

### Tres conflictos de glosa detectados al cruzar (⚠️ abiertos)

No son D7 (glosa vs. taxón) sino **glosa vs. glosa**: el lexicón dice una cosa y
Zavala otra distinta. Es muy improbable que estas tres vengan de aquí, así que
citarlas a Zavala sería un error:

| Forma | Lexicón dice | Zavala dice |
|---|---|---|
| `tara` | venado, ciervo (*Odocoileus virginianus*) | #238 (HB+PMA+AM) "Langosta, mariposa" |
| `saruro` | árbol saruro (frutos pequeños) | #224 (E) "Serpiente no venenosa. Boa constrictora" |
| `corie` | choza, habitación, espacio propio | #90 (HB) "Armadillo" |

## Huecos léxicos que Zavala llena

Cruce completo del glosario contra [[ecologia_lexicon_map|los huecos declarados]]
de `3-mundo/corpus/ecologia_lexicon_map.md`:

| Hueco declarado | Zavala lo llena |
|---|---|
| **especies de pez** ("cunaro/guaranaro/bagre son nombres de agente, no de especie") | ✅ **Sí, y era el hueco nº 4 de la lista**: #95 `cuna`, #96 `cunaro`, #139 `guaranaro` "pez lisa", #21 `bagre` "pez" |
| zorro común (*Cerdocyon thous*) | ✅ #80 `chaguanco` "Zorro"; #125 `guache` "Murciélago, zorro blanco" |
| mato real, lagartijo | ✅ #41 `bisure` "Lagartija" |
| arcilla / engobe / desgrasante | ✅ #141 `guarataro` "Barro de loza, para la fábrica de budares y ollas"; #99 `dabuda` "Barro loza" |
| agua salobre / salitre | ◐ parcial: #140 `guaranao` "Salado, ácido" (adjetivo) |
| avifauna del humedal | ◐ parcial: #202 `querequere` "Ave pequeña", #102 `dara` "Alcaraván", #244 `tauta` / #247 `tigüí` / #248 `tijúa` (palomas ictiófagas), #143 `guaru` |
| quebrada / arroyo efímero | ◐ parcial: los afijos `-uco`/`-uto` #268 y `-ima` #165 sí nombran "quebrada, cauce", pero como sufijo |
| duna/médano · cardumen · alisio · marea · cascabel · madera de canoa · tala y quema · istmo · mangle por especie | ❌ **siguen abiertos** |

## `datihao` / `daitiao` / `diao` — el nudo resuelto

Son **dos lexemas**, no tres, y **ninguno de los dos viene de Zavala salvo
`diao`**:

1. **`diao`** — Zavala #106 (HB+AM) *"Señor principal. Jefe mayor"*. Coincide con
   Oviedo y Valdés vía [[oliver-1989-cap2]] §g: *"señor o cacique del territorio
   zaquitios… el señor principal, que tiene muchos indios y a quien otros
   caciques están sujetos"*. **Cita firme.**
2. **`datihao` = `daitiao`** — **una sola palabra, dos grafías**. Oliver escribe
   *datihao* al citar a Oviedo (*"señor: el que presta su nombre al esclavo"*,
   Oviedo y Valdés [1535-1557] 1944: 41) y *daitiao* al hacer el análisis
   morfológico. **No está en el glosario de Zavala**: la glosa del lexicón
   ("padrino de cautivo, el que presta su nombre al esclavo") es de Oviedo vía
   Oliver, y ahí es donde debe citarse.
3. **`guaitiao`** es el **mismo lexema con otro prefijo de persona**: raíz
   `-(i)tiao` (recíproco) con `da-` 1ª sg. → *daitiao*, con `wa- [gua-]` 3ª pl.
   → taíno *waitiao/watiao* → préstamo español *guaitiao* 'amigo, aliado'.
   Cognado con lokono `da-tti / da-iti`, raíz de parentesco `/-atti-/`.

Oliver es explícito en que *diao* está **"closely related to"** *datihao*, no que
sean lo mismo — y **advierte** que no tiene certeza absoluta de que *datihao* sea
caquetío (Oviedo habla de la Provincia de Venezuela en general; Oliver se inclina
por atribuirlo al caquetío por descarte). **Jahn 1927 p. 213 n.29 ("datihao/diao
= señor") los conflaciona**; no pudo re-verificarse aquí porque el PDF de Jahn no
tiene capa de texto en esas páginas.

→ Acción pendiente (fuera de F7, toca `curiana_lexicon.py`): poner nota a
`datihao` citando Oviedo/Oliver, **no** Zavala.

## Cobertura de las 82 sin cita

De las 82 entradas de familia caquetía sin nota, **62 quedan con cita exacta a
Zavala** (número de entrada, siglas y glosa verbatim), 4 se aclaran como falsos
amigos y 16 quedan sin rastro. Eso convierte F1 de "degradar por defecto" a
"adjudicar con evidencia".

**Fuerza de la atribución** — F = fuerte (referente local, no panvenezolano,
glosa específica) · D = débil (fitónimo/zoónimo de circulación pan-venezolana, o
glosa ambigua).

### A. Entrada directa del glosario (52)

| palabra | nº | siglas | glosa verbatim | fuerza |
|---|---|---|---|---|
| `amaca` | #9 | AM | Sitio de moler maíz | F |
| `apana` | #10 | GC | Una luna. Medición de tiempo | F |
| `ateri` | #17 | GC | Hombre | F |
| `bajarí` | #25 | AM | Recorrer, caminar | F |
| `barici` | #34 | HB | Agua turbia | F |
| `borojo` | #44 | AM | Salina de Coro, comercio de la sal | F |
| `buco` | #46 | AM+CGB | Chorro de agua, presa de agua | F |
| `buiamati` | #47 | GC | dos lunas. Medición de tiempo | F |
| `bureche` | #49 | AM | Hacer, realizar | F |
| `buriche` | #50 | AM | Licor fermentado | F |
| `caduchi` | #55 | HB | Higo, breva | D (glosa española del fruto) |
| `cari` | #66 | E | Orilla del mar | F |
| `catarí` | #70 | PMA | Número cuatro | F |
| `cati` | #71 | CGB | Luna [catire: persona de tez blanca] | F |
| `cazá` | #74 | HB | Puche de maíz | F |
| `cazebo` | #75 | GC | Poniente | F |
| `cazi` | #76 | GC | Sol | F |
| `cazicure` | #77 | GC | Parte del levante | F |
| `chiriguare` | #84 | HB | Gavilán | D (voz zoonímica panvenezolana) |
| `corie` | #90 | HB | Armadillo | ⚠️ **conflicto de glosa** (ver arriba) |
| `cumaragua` | #93 | HB+E | Ciruela, espuma rosada | F (también topónimo de Falcón) |
| `dare` | #103 | HB | Diente | F (Oliver la confirma en Paraguaná) |
| `duraboa` | #115 | AM | Conuco, sembrado | F |
| `eroa` | #119 | AM | Empezar, crear | F |
| `garabal` | #121 | AM | Tierra de crianza o tierra de pasto | F |
| `gua` | #122 | HP | Conuco, heredad, terreno cercado con algo | F |
| `guanepe` | #137 | E | Cesto para cargar a los niños | F |
| `gudamuen` | #148 | PMA | Numero dos | F |
| `güere` | #149 | AM | Dar, entregar | F |
| `güique` | #152 | AM | Río navegable | F |
| `humocaro` | #159 | GC | Mujer bella | F |
| `iero` | #163 | GC | Mujer | F |
| `jacuque` | #170 | AM | Regar, regadío | F |
| `jacura` | #171 | AM | Guardar | F |
| `jaguey` | #174 | AM | Establecer, estancar | D (*jagüey* es panamericano, de taíno) |
| `jai` | #175 | AM | Oír, escuchar | F |
| `na` | #184 | HP | Partícula equivalente a "como" o "semejante" | F |
| `pariri` | #194 | AM | Pantano, ciénaga | F |
| `paro` | #195 | AM | Río | F |
| `quidi` | #212 | AM | Cerro, altura | F |
| `rao` | #219 | E | Arena | F |
| `sabuenen` | #222 | PMA | Número tres | F |
| `saruro` | #224 | E | Serpiente no venenosa. Boa constrictora | ⚠️ **conflicto de glosa** |
| `tabri` | #234 | AM | Conuco, siembra | F |
| `tara` | #238 | HB+PMA+AM | Langosta, mariposa | ⚠️ **conflicto de glosa** |
| `tarica` | #242 | AM | Laguna | F |
| `tata` | #243 | AM | Padre, papá | D (*tata* es panhispánico infantil) |
| `tebe` | #245 | AM | Lugar de cultivo | F |
| `tuqueque` | #257 | E+A+PMA | Lagarto casero | D (voz venezolana corriente) |
| `ture` | #259 | AM | Vasija, utensilio | F |
| `ucibo` | #267 | AM | Cuenta de piedras | F |
| `urapa` | #269 | AM | Sitio de cría de animales | F |

### B. Entrada del glosario con variante ortográfica (3)

| palabra | nº | siglas | glosa verbatim | fuerza |
|---|---|---|---|---|
| `bariki` | #35 *Barique* | AM+HB | Arcilla roja. Almagre. Galeotto Cey indica Bariquizi o bija | F (Arcaya la cita también en la Relación de Barquisimeto 1579) |
| `buko` | #46 *Buco* | AM+CGB | Chorro de agua, presa de agua | F (misma palabra que `buco`, grafía con k) |
| `chuchubi` | #85 *Chuchube* | HB | Paraulata | F (*Mimus gilvus*, coincide con la glosa del lexicón) |

### C. Prosa y notas al pie del artículo, no del glosario (7)

| palabra | ubicación | glosa verbatim | fuerza |
|---|---|---|---|
| `chacamba` | p. 73, citando a Arcaya (1995) | *"fórmula de saludo: **chacamba** cudanga (¿Cómo está usted?)"* — recogida a una anciana de Mitare | F — es **la única frase caquetía conservada** |
| `cudanga` | p. 73, ídem | *"chacamba **cudanga** (¿Cómo está usted?)"* | F |
| `cudan` | p. 73, ídem | *"**cudan** de cuté (para servir a usted)"*; variante de 1905: *"judan de cuteo"* | F |
| `cuté` | p. 73, ídem | *"cudan de **cuté** (para servir a usted)"* | F |
| `curiana` | nota al pie (4) | *"Curiana: territorio donde estaban asentados los caquetíos"* | F (ya en el corpus como `geografia_politica-007`) |
| `maure` | nota al pie (3) | *"Maure: fibra de algodón con la que tejían las hamacas"* | F |
| `mene` | p. 62, citando a Arcaya (1920) sobre la Relación de Barquisimeto 1579 | *"«mene» y «cumaragua» nombre de la ciruela"* | ⚠️ D — la sintaxis de Arcaya es ambigua y el lexicón glosa `mene` como *petróleo/rezumadero*: la cita **no confirma** esa glosa |

### D. Falsos amigos — la palabra es la GLOSA, no la voz (4)

| palabra | qué pasa en realidad |
|---|---|
| `caraota` | #162 glosa el caquetío **`icoroata`** como 'caraota'. La voz caquetía es *icoroata* |
| `pauji` | #197 glosa el caquetío **`paugis`** como 'paují'. La voz caquetía es *paugis* |
| `piache` | #43 glosa el caquetío **`boratio`** como 'piache, cacique, jefe, sacerdote, médico'. *Piache* es cumanagoto |
| `coro` | #181 es **`Koro` = 'cotorra'**, no 'cardón'. El `coro`='cardón grande' del lexicón **no sale de Zavala** |

### E. Sin rastro en Zavala — F1 debe buscarlas en otra parte (16)

`auyama`, `cachicamo`, `chogogo`, `datihao`, `guaitiao`, `kadushi`, `kama`,
`koke`, `kukuisa`, `kunuku`, `mazato`, `poporo`, `sawaka`, `wabarsure`,
`watapana`, `warawara`.

Patrón claro: **casi todas son de la vertiente insular** (papiamento de Aruba /
Curazao: `kadushi`, `kukuisa`, `kunuku`, `watapana`, `warawara`, `koke`) o
**construcciones internas del proyecto** (`wabarsure` = *wa-* + *barsure*,
`sawaka`). `datihao` y `guaitiao` sí tienen fuente firme: Oviedo vía
[[oliver-1989-cap2]] (ver arriba). Ninguna de las 16 debe citarse a Zavala.

## Caveats de método (heredados de la propia fuente)

- Es una **compilación de nueve autores**, no una recolección de campo. Algunos
  fitónimos y zoónimos son voces indígenas de circulación pan-venezolana cuya
  atribución *específicamente caquetía* es más débil que la de un `diao`. Cada
  entrada importada lleva en `notas` el número de glosario y las siglas del
  compilador, para que esa procedencia quede auditable — y la columna «fuerza»
  de las tablas de arriba marca las débiles.
- El propio Zavala cita a [[arcaya-1920]], [[alvarado-1921]] y
  [[oviedo-y-banos]] — es decir, buena parte de nuestro "atestiguado" llega
  **de tercera mano**.

## Qué falta

1. **Fusión humana al lexicón** (fuera del alcance del minador, que solo emite
   propuesta): aplicar las 62 citas recuperadas, la nota Oviedo/Oliver de
   `datihao`, y resolver los tres conflictos de glosa (`tara`, `saruro`,
   `corie`).
2. **Las 16 sin rastro** (§E) necesitan otra fuente: papiamento / Aruba
   ([[gatschet-1885]], Maduro 1966) para la vertiente insular.
3. `mene`: decidir si la glosa 'petróleo' se sostiene, porque la única cita
   disponible dice otra cosa.

## Herramientas

- `curiana_sim/minar_zavala_glosario.py` — parsea, clasifica por tiers, **no
  modifica** el lexicón: emite propuesta.
  - Reporta *"ya presentes: 66 (22%)"* **a propósito**: excluye su propia
    importación para ser idempotente. No es un fallo de la fusión — los 151 sí
    están en `VOCABULARIO_BASE` (verificado).
  - `RESCATES_PARSEO`, `DESMARCADAS_F7`, `DESCARTAR_DEL_HABLA` e
    `IDENTIFICACION_MODERNA` documentan en código cada decisión de arriba.
- `curiana_sim/lexicon_zavala.py` — generado, no editar a mano. Exporta además
  `VEREDICTO_HOMOGRAFOS` y `DESCARTADOS_ZAVALA`.

## Enlaces

[[mapa-geografia-politica]] · [[mapa-creencia]] · [[mapa-motor]] ·
[[05_geografia_politica_y_sucesion]] · [[oliver-1989-cap2]] · [[INDICE_FUENTES]]
