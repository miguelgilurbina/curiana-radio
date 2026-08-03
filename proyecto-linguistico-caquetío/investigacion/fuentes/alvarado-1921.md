---
tipo: fuente
obra: "Glosario de voces indígenas de Venezuela"
autor: "Alvarado, Lisandro"
anio: 1921
genero: glosario
local: "fuentes_caquetios/Alvarado_1921_Glosario_Voces_Indigenas_Venezuela.pdf"
paginas: 354
capa_texto: si
estado_minado: minado
prioridad: media
tareas: [F3]
sostiene: {hechos_corpus: 1, entradas_lexicon: 0, entradas_lexicon_corroboradas: 39, cadena_custodia_zavala_A: "24/26"}
verificado: 2026-08-03
aliases: ["Alvarado 1921", "Glosario de voces indígenas"]
---

# Alvarado 1921 — *Glosario de voces indígenas de Venezuela*

## Qué es

Un glosario **nacional** de voces indígenas: caribe, cumanagoto, chaima,
tamanaca, taíno, guajiro, quechua, nahua y antillanismos ya castellanizados.
Lisandro Alvarado es además uno de los nueve compiladores del glosario de
[[zavala-reyes-2015]] (sigla `A`), así que parte de nuestro "atestiguado" venía
de él **de tercera mano** — hasta hoy.

**Estado: minado (F3, 2026-08-03).** Extracción con
`pdftotext -enc UTF-8` (no con `pypdf`, que devuelve vacío en este archivo y
por eso F3 figuró un año como "bloqueada por falta de OCR"). El minador vive en
`curiana_sim/minar_alvarado_glosario.py`; su propuesta, en
`curiana_sim/lexicon_alvarado.py`. **Ninguna voz entró a `VOCABULARIO_BASE`.**

| Dato | Valor |
|---|---|
| Tamaño · páginas | 26.9 MB · 354 pp. (glosario impreso 1–318; offset PDF = +30) |
| Texto extraído | 704 KB, acentos correctos |
| **Lemas parseados** | **1551** |
| Evaluados a fondo (con señal geográfica o curados a mano) | 109 |
| Veredicto A / B / C / **D** | 3 / 36 / 13 / **57** |

## Qué ha dado

### 1. La prueba de fiabilidad de la Capa 1 — **pasa** (24/26)

Era la pregunta más barata y más importante de esta fuente: *las entradas del
lexicón con sigla `A` en [[zavala-reyes-2015]], ¿se pueden rastrear a su lugar
exacto en el glosario de Alvarado, o son cita de tercera mano?*

**24 de 26 se rastrean a una página concreta** (`--cadena`). Las otras dos
también están, pero el OCR de 1921 las deformó: `guay` → p.145, leída como
"GUÁL. *Bombax* sp. Ceiba. Voz usada en Coro"; `cocuy` → p.84, fusionada con
COCUIZA. **La cadena de custodia de Zavala aguanta.** Dos casos merecen mirada:

- `laguari` (lexicón) = **LAUADRÍ** p.184, "Árbol indeterminado del E. Falcón.
  D. t. Laguadrí" — variante ortográfica, confirmada.
- `quiguagua` (lexicón) = **GUAGUA** p.261, "Especie de haba de Coro, grande y
  blanca" — glosa idéntica, forma sin la sílaba inicial.

### 2. Tres voces de nivel **A**

| Voz | p. | Evidencia |
|---|---|---|
| **poporo** | 255 | *"Arma, a manera de porra, usada por los antiguos **Caquetíos** y los Guagíros"* (Ref. Castellanos). **Única atribución caquetía explícita de todo el glosario.** |
| **mene** | 218 | Oviedo II.301 (*"betún a manera de brea o pez derretida"*); Codazzi sitúa los yacimientos en **Coro** y Maracaibo. |
| **maure** | 216 | Carvajal 168 y Castellanos (faja/tejido); vivo en **Coro** en 1921 como "pieza de dril". Doble anclaje, colonial y coriano. |

Las tres ya estaban en el lexicón **sin cita**. Ahora la tienen.

### 3. Un filón inesperado: 24 voces nuevas de nivel **B**

Alvarado repite una fórmula centenares de veces: *"Árbol indeterminado de
Coro"*. Son voces que la ciencia de 1921 **no supo traducir a un taxón** — es
decir, las menos castellanizables del repertorio, y ninguna cae en los 6
filtros. 36 llegaron a nivel B; **24 no están en el lexicón**:

`achichive · aiton · anuano · araguan · aripino · barimiso · barisigua · boque ·
camare · chiguare · chiriga · cuaguaro · cusuca · guaitoco · isicagua · lauadri ·
manata · mapuare · maque · pirota · sibucaro · tocororo · urupagua · urupaguita`

Dos cierran **huecos léxicos** que `ecologia_lexicon_map.md` daba por vacíos:

- **`aiton`** (p.5) — *"Sima profunda formada en algunos parajes del E.
  Falcón"*. Término de **paisaje**, justo lo que las crónicas no anotaron.
- **`tocororo`** (p.292) — *"Tallo leñoso del cirio o cardón"* (Lara, Falcón).
  Nombra una **parte** del cardón, planta central del paisaje caquetío.

Y **`cumaragua`** (p.102) es la única voz del glosario localizada en
**Paraguaná** — con un conflicto de glosa que se documenta abajo.

## Descartes razonados

57 voces cayeron en los filtros. Documentarlas evita que alguien las
re-descubra dentro de seis meses. La lista completa está en
`DESCARTES` de `lexicon_alvarado.py`; las que más importan porque **ya están en
el lexicón etiquetadas como caquetío**:

| Voz | p. | Filtro | Lo que dice Alvarado |
|---|---|---|---|
| **piache** | 248 | F6 caribe | *"Voz cháima y tamanaca, con formas afines en otras lenguas caribes"*. Es la palabra para chamán. |
| **auyama** | 16 | F6 caribe | *"Voz cum."* (cumanagota), vía Ruiz Blanco; variantes *ayuyáma*, *huyáma*. |
| **ture** | 301 | F6 caribe | *"Voz cháima"* (Tauste), usada en **Cumaná y Margarita**, no en Coro. |
| **pauji** | 244 | F6 caribe | Derivado del chaima — y es un **árbol** (*Bumelia buxifolia*), no un ave. |
| **piritu** | 253 | F6 caribe | *"En car. piritu, en cum. piríchu, lo mismo"*. Crece en Coro, pero la voz es caribe. |
| **watapana** → **guatapanar** | 163 | F6 caribe | *"Del cum. araguatapanár, oreja de araguato"*; y *"Guatapaná, en Cuba"*. |
| **kunuku** → **conuco** | 89 | F4 taíno | *"Voz taina"* (Las Casas V.307). |
| **kukuisa** → **cocuiza** | 84 | F4/F6 | Caulín I.3: *"una especie de pita que los indios llaman **caruata** y los españoles **cocuiza**"* — cocuiza es el nombre del lado español. |
| **caraota** | 58 | F4 | Nombre corriente panvenezolano de las judías, sin origen indígena declarado. |

Descartes que **no** tocan el lexicón pero conviene dejar por escrito:

- **`chimbanquele`, `chimbique`, `tamunango`** (pp.121-122, 283) — bailes
  **afrodescendientes** de Coro (S. Benito, S. Antonio). Filtro 5. Están
  localizados en Coro, sí; no son sustrato indígena.
- **`dibibe`, `dispopo`, `tura`** (pp.132-133, 301) — **ayamán/gayón**, es
  decir jirajaroide (filtro 6). El baile de Tura es de Churuguara, Falcón:
  localización correcta, filiación equivocada. Es el error más fácil de
  cometer con esta fuente.
- **`camuro`** (p.51) y **`tequiara`** (p.288) — *"del guajiro amuru"*, *"del
  guajiro tekiara"*. Filtro 3.
- **`chapapote`** (p.113) — *"Del azt. chapápotl"*, pese a citarse en la Costa
  de Coro. Filtro 4. Un asfalto de Coro con nombre náhuatl.
- **`carebe`** (p.62) — Alvarado mismo dice que es *"voz tomada de algún
  dialecto andino"*.
- **`hamaca`, `guaca`, `curiara`, `butaque`, `duro`, `manare`, `adorote`** —
  antillanismos y caribismos de circulación nacional. Filtros 4 y 6.

**Ausencias que también son dato:** `kadushi`, `chuchubi`, `chogogo`,
`watapana` (como tal) **no aparecen en un glosario nacional de 1921**. Es
consistente con que sean formas **papiamentas de las islas ABC** — el filtro 2
del protocolo, y territorio de [[van-buurt-2014]], no de esta fuente.

## Cobertura de las 82 sin cita

Adjudicación completa en `AUDITORIA_82` de `lexicon_alvarado.py`
(`python minar_alvarado_glosario.py --82`). Resumen: **18 de 82 resueltas**
(7 confirman, 11 reclasifican); 64 no concluyentes, de las cuales **57 no dejan
rastro alguno** en Alvarado.

| Palabra | ¿Aparece? | Cita exacta | Veredicto |
|---|---|---|---|
| poporo | lema p.255 | "Arma, a manera de porra, usada por los antiguos Caquetíos y los Guagíros" (Cast.) | **confirma** — y da la cita que faltaba |
| mene | lema p.218 | "Betún a manera de brea o pez derretida" (Ov. II.301); Coro y Maracaibo (Cod.) | **confirma** |
| maure | lema p.216 | "Son a fuer de faxas mujeriles muy curiosas" (Carv. 168); "en Coro… pieza de dril" | **confirma** |
| mazato | lema p.217 | "este maçato es algo acedo, y tiénenlo por muy excelente brevaje" (Ov. II.297) | **confirma** la glosa; forma panamericana, filiación no |
| cachicamo | lema p.41 | "Edentados de la fam. de los Dasipódidos, género Dásypus" | **confirma** la glosa; sin origen declarado |
| tuqueque | lema p.300 | "Saurios de la familia de los Ascalabotos… *Thecadactylus rapicaudus*" | **confirma** la glosa; sin origen ni localización |
| buco | lema p.34 | "Caz, acequia. Voz antigua… Úsase aún en el E. Lara. ¿Vendrá del ant. *buca*, boca?" | **confirma** la glosa; ⚠ la propia fuente duda del origen, y localiza en Lara |
| auyama | lema p.16 | "Voz cum. que Ruiz Blanco traslada 'calabaza'" | **reclasifica** → cumanagoto (caribe) |
| piache | lema p.248 | "Voz cháima y tamanaca, con formas afines en otras lenguas caribes" | **reclasifica** → caribe |
| ture | lema p.301 | "Asiento pequeño… Us. en Cumaná y Margarita. Voz cháima" | **reclasifica** → caribe, y la glosa es *asiento*, no *vasija* |
| pauji | lema p.244 | "*Bumelia buxifolia*. Sapotáceas. Árbol espinoso… Del ch. pao—" (cf. IGÜÍ p.175: "Paují… Coro") | **reclasifica** → árbol, no ave; chaima |
| watapana | lema p.163 (*guatapanar*) | "Del cum. araguatapanár, oreja de araguato… Guatapaná, en Cuba" | **reclasifica** → cumanagoto; la forma *watapana* es papiamenta |
| kunuku | lema p.89 (*conuco*) | "Voz taina" (Cas. V.307) | **reclasifica** → taíno vía español |
| kukuisa | lema p.84 (*cocuiza*) | "los indios llaman caruata y los españoles cocuiza" (Caul. I.3) | **reclasifica** → nombre del lado español |
| caraota | lema p.58 | "Nombre dado corrientemente a varias clases de judías, habas o habichuelas" | **reclasifica** → panvenezolano sin origen indígena |
| bureche | lema p.34 | "Bebida fermentada que preparan los indios guayaneses… el casabe" | **reclasifica** — ⚠ conflicto de glosa: el lexicón lo tiene como verbo *hacer* |
| cumaragua | lema p.102 | "Especie de caracol de las costas de **Paraguaná**" | **reclasifica** — ⚠ conflicto de glosa: el lexicón dice *ciruela, Spondias mombin* |
| guanepe | lema p.152 | "Así llaman en **Barcelona y Guayana** una especie de cabestrillo… en que las madres indígenas llevan sus niños" | **reclasifica** — confirma la glosa, **desmiente la geografía** |
| chiriguare | mención p.126 | "Después que samuro come, chiriguare roe" (refrán) | no concluyente — confirma el sentido de ave carroñera, nada más |
| amaca | mención p.171 | solo como variante de *hamaca* | no concluyente — homógrafo |
| apana | mención p.229 | quichua *apana*, "añadidura" (étimo de *ñapa*) | no concluyente — homógrafo |
| cuté | lema p.110 | "Véase Carate" (enfermedad de la piel) | no concluyente — homógrafo |
| curiana | mención p.279 | s.v. SURÚPA: *curiana* como palabra **española** para cucaracha | no concluyente — el topónimo no está en el glosario |
| coro | mención ×55 | siempre como topónimo; no hay lema CORO = 'cardón' | no concluyente |
| tara | mención p.285 | "TARÍTA. Mariposa o *tara* pequeña"; "ser tara negra" | no concluyente — en Alvarado *tara* es polilla, no venado |
| tata | mención | solo en "tata-cuá" (indígenas de Mérida) y en "patata" | no concluyente |
| kadushi · chuchubi · chogogo · warawara | **ausentes** | — | no concluyente — pero su ausencia apunta a papiamento ([[van-buurt-2014]]) |
| *las otras 50* | **ausentes** | — | no concluyente: Alvarado no adjudica ni a favor ni en contra |

> **Lectura honesta:** Alvarado **no salva** a las 82. Resuelve 18. De esas 18,
> solo **3** (`poporo`, `mene`, `maure`) sostienen la etiqueta
> `caquetío-atestiguado`; **11 la contradicen**. Para las 57 mudas, F1 sigue
> teniendo que decidir con otro criterio.

## Qué falta

1. **F1 puede ejecutarse ya** con evidencia en la mano para 18 de las 82, y con
   3 candidatas extra a reetiquetar que no estaban en la lista: `piritu`,
   `paugis` y `caquetillo` (esta última porque el propio Alvarado solo
   *pregunta* si es "voz afín de caquetío").
2. **Decisión humana pendiente sobre las 24 voces nuevas de nivel B.** El
   destino natural, según el protocolo §5, es el **corpus cultural**, no
   `VOCABULARIO_BASE`. `aiton` y `tocororo` son las que más tientan porque
   cierran huecos léxicos: precisamente por eso hay que decidirlas a mano.
3. **Cruce con [[van-buurt-2014]] (F6)** — la ausencia sistemática de las
   formas papiamentas (`kadushi`, `chuchubi`, `chogogo`, `watapana`) en un
   glosario nacional de 1921 convierte ese cruce en **la prueba de control del
   filtro 2**: si van Buurt las documenta en Curaçao y Alvarado no las conoce en
   tierra firme, la vía de entrada al lexicón fue insular, no coriana. F6 se
   minó en paralelo (`curiana_sim/lexicon_van_buurt.py`); el cruce está por
   hacer y es barato.
4. **No se agotó el glosario.** Se evaluaron a fondo 109 de 1551 lemas: los que
   llevan señal geográfica explícita. Un segundo barrido por **campo semántico**
   (pesca, marea, médano, salina) sobre los 1442 restantes podría dar más, con
   rendimiento decreciente y riesgo creciente de falso positivo.

## Enlaces

[[MOC_ecologia]] · [[MOC_motor]] · [[02_protocolo_habla_paraguanera]] ·
[[zavala-reyes-2015]] · [[van-buurt-2014]] · [[gatschet-1885]] ·
[[oviedo-y-valdes-1851]] · [[INDICE_FUENTES]]
