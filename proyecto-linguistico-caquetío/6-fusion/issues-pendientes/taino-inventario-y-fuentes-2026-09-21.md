---
tipo: decision
campana: Campaña del Taíno — parcela T3
fecha: 2026-09-21
estado: sin publicar
mide: 6-fusion/scripts/medir_taino_inventario.py
datos:
  - 6-fusion/taino_inventario_2026-09-21.yaml
  - 6-fusion/taino_fuentes_mapa_2026-09-21.yaml
---

# El taíno que tenemos: de dónde salió, quién lo dice, y qué falta

Miguel pidió minar el taíno «tal cual lo hicimos con el resto de lenguas
fuentes» y anexarlo a la esfera. Antes de anexar nada hacía falta saber qué
había. Esto es el censo, y sale peor de lo que parecía por un lado y mejor por
otro.

Todas las cifras salen de `6-fusion/scripts/medir_taino_inventario.py`
(regla 1). Nada de aquí toca `curiana_sim/` ni el corpus (regla 5).

---

## Lo primero: tres cosas del encargo que no eran ciertas

0. **«Las 78» no son 78: son 56 formas distintas.** 52 en el lexicón + 26 en
   `taino_hipotetico.json` = 78 sumando, pero **22 de las 26 del JSON tienen la
   misma clave que una del lexicón** (`abba`, `acoa`, `aduri`, `agari`, `aji`,
   `akcicyaa`, `bejique`, `cai`, `caiman`, `casabe`, `cohiba`, `daca`,
   `higuana`, `maisi`, `mayani`, `taita`, `thigisi`, `tuna`, `wacusi`,
   `wagulo`, `yamosa`, `yuca`). El JSON no es un corpus aparte: es en su mayor
   parte el mismo material antes de entrar. Sólo 4 de sus 26 son formas que el
   lexicón no tiene.

1. **Pedro Mártir no falta: está en el repo y sin minar.** El encargo lo
   listaba entre «las crónicas que faltan». `angleria-1892` (*Décadas del Nuevo
   Mundo*, vols. 1 y 4, 460 + 492 pp.) está en `fuentes_caquetios/` con
   `en_repo: true` y `estado_minado: parcial`, y `entradas_lexicon: 0`. Y es
   justo la fuente en la que Brinton apoya cinco de las voces de su vocabulario
   antillano, con página. La obra más barata de conseguir ya la tenemos.

2. **«0 de 52 con `procedencia.obra`» es cierto pero incompleto.** 10 de las 52
   sí citan una obra **en prosa** dentro de `notas`. La cifra 0 mide la clave
   foránea; la cifra 10 mide lo que alguien escribió a mano. Y de las 9 citas a
   Brinton, **4 no se sostienen** (abajo).

---

## El censo

| Qué | Cuántas | Dónde |
|---|---|---|
| `fuente: taíno` | 43 | `curiana_lexicon.VOCABULARIO_BASE` |
| `fuente: taíno-reconstruido` | 9 | ídem |
| reconstrucciones hipotéticas | 26 | `curiana_sim/taino_hipotetico.json` |
| tainismos de Medina | 12 | `6-fusion/tainismos_en_medina.yaml` — **no cuentan**: se fusionaron el 2026-09-12 como `caquetío-reconstruido` |
| con `procedencia.obra` | **0 de 52** | — |
| con cita en prosa en `notas` | 10 de 52 | 9 a Brinton 1871, 1 a Alvarado + Las Casas + van Buurt (`kunuku`) |
| con `notas` vacías del todo | 3 | `bohío`, `cacique`, `maíz` |

**De dónde salieron.** Cinco commits, y 51 de las 52 entraron entre el
2026-06-13 y el 2026-06-21 — el arranque del repo, antes de que existiera la
regla 8. No es un descuido reciente: es sedimento fundacional.

| commit | fecha | entradas |
|---|---|---|
| `81391426` expand attested lexicon | 2026-06-20 | 19 |
| `573719a6` expansion v4 | 2026-06-21 | 18 |
| `774de860` fix(terminologia) | 2026-06-20 | 11 |
| `475457dc` init repo | 2026-06-13 | 3 |
| `4b93c9db` vault + minería de 5 fuentes | 2026-08-04 | 1 (`kunuku`) |

---

## Las citas que no aguantan

Nueve entradas dicen «Taíno atestiguado: X; cognado Lok. Y; **Brinton 1871**».
Brinton 1871 es *The Arawack Language of Guiana* —una comparativa del **lokono**—
pero trae dentro un «Vocabulary of the Ancient Language of the Great Antilles»
que sí es taíno. Así que la cita no es absurda. Medida forma a forma contra
`fuentes_caquetios/Brinton_1871_texto.txt`, con patrones tolerantes al OCR:

| entrada | ¿está en Brinton? | qué dice Brinton |
|---|---|---|
| `cai` 'isla' | **sí** | «Cai, cayo, or cayco, an island… Ar. kairi» |
| `caiman` | **sí** | «Caiman, an alligator, Ar. kaiman» — sin cronista |
| `mayani` | **sí, con otra glosa** | «Mayani, **of no value** ("nihil!", Pet. Martyr, p. 9). Ar. ma, no, not» |
| `taita` 'padre' | **sí, con otra fuente** | «Taita, father (**Richardo**)» — Pichardo, diccionario cubano del XIX |
| `yamosa` 'dos' | **sí** | «2 yamosa» (Las Casas, Hist. Apol. cap. 204) |
| `casabe` | **no** | lo que casa es `cassava`, palabra inglesa del cuerpo del texto |
| `cohiba` 'tabaco' | **no tal cual** | Brinton tiene `cohóba`, y glosa al revés: «Tabaco, **the pipe** used in smoking the cohoba» |
| `higuana` | **no** | ni con patrón tolerante |
| `tuna` 'agua, río' | **no** | ni con patrón tolerante |

**Y una que es exactamente la trampa de esta campaña, dentro de nuestro canon.**
`mayani` está glosada 'no, negación'. Brinton dice que `mayani` es 'of no value'
y que `ma` 'no, not' es el **comparando arahuaco**. Alguien leyó el comparando
como la glosa. Es el mismo error que tumbó `macana` en el vocabulario achagua:
se lee la glosa verbatim, siempre.

**Y una contradicción que decide sola.** Nuestro `abba` está etiquetado
`taíno-reconstruido` 'uno', reconstruido del lokono. En la página de Brinton
donde vive `abba`, el 1 taíno atestiguado es **`hequeti`** (Las Casas, Apol. cap.
204) y `abba` es el 1 **arawack**. Reconstruimos una forma para un hueco que no
existía.

⚠️ La relectura de Brinton, Oviedo, Las Casas y Pané es parcela de T1/T2. Esto
es verificación de una cita ya escrita, no minería.

**Lo que sí se puede citar hoy, y no se citaba.** Alvarado 1921 marca «Voz
taina» 48 veces (y usa además «voz caribe» 5, «voz galibi» 4, «voz cumanagota»
13, «voz cháima» 11: la obra **distingue**, y eso es lo que la hace citable).
El emparejamiento se hace por el lema castellano de Alvarado —él entra IGUANA,
MAHIZ, BATÉI; nosotros `iwana`, `maisi`, `batey`— con una tabla declarada, y
sobre el texto aplanado, sin acentos y sin el guion de fin de línea del OCR.

**La primera versión de esta medición dio 13 y tres eran falsos positivos**, del
mismo tipo exacto que el `macana` achagua que tumbó un apoyo esta misma campaña:
`cobo` casaba con «Cobo, I. 196», que es el cronista Bernabé Cobo; `cai` casaba
con la primera mitad de «Cai- mán» partida por el OCR; y `cobo` y `cacique`
entraban por un plural ajeno. Arreglado, quedan **14 claves con marca**, con
página impresa (desfase medido: pdf − 31):

`batey` p. 24 · `bohío`/`bohio` p. 29 · `caiman` p. 44 · `casabe`/`cazabi` p. 68
· `cohiba` p. 85 · `higuana`/`iwana` p. 173 · `maíz`/`maisi` p. 193 · `tabako`
p. 278 · `tuna` p. 298 · `yuca` p. 314.

Tres avisos sobre esas 14:

- **`tuna` aparece, pero con otra glosa.** Alvarado p. 298 lematiza TUNA = el
  fruto de la cactácea, no 'agua, río'. Es presencia, no apoyo.
- **`caiman` aparece diciendo lo contrario de lo que queremos.** Verbatim:
  «Caimán es **voz taina y galibi**: en cal. se decía akayumán». Es la prueba
  de la clase (iv), no su refutación.
- **14 es un suelo, no un techo.** El emparejador es deliberadamente estrecho y
  se le escapan las que están a la vista: `batata` p. 23, `caney` p. 51,
  `manati` p. 199 y `kunuku`/CONUCO p. 89 quedan fuera porque la marca cae
  lejos del lema o el OCR parte la palabra; y `bixa` p. 28 queda fuera porque
  Alvarado **no** usa ahí «voz taina» sino «**Del taino bixa**, en que la x
  equivale al sh inglés» — que de paso atestigua la regla ortográfica de esta
  campaña (⟨x⟩ = /ʃ/). Esas cinco se leyeron a mano y hay que confirmarlas al
  fusionar.

Y una simetría que vale la pena: las **9 claves sin lema castellano posible** son
exactamente las 9 `taíno-reconstruido`. Alvarado recoge el español de Venezuela;
una forma reconstruida del lokono no tiene por qué estar ahí, y no está.

Y tres contradicciones de glosa que Alvarado y Brinton abren:
`caney` (nosotros: «bohío **rectangular**»; Alvarado y Brinton: cabaña
**circular** / «a house of conical shape»), `batey` (nosotros: «plaza central,
cancha»; Brinton: `batay` el terreno, `batey` **el juego**) y `areito`
(nosotros: «danza ritual»; Brinton, citando a Oviedo: «a **song** chanted
alternately»).

---

## Qué llega al motor, y qué dicen los agentes

- `[Voces de fuera]` ofrece **43 candidatas** (25 taínas, 9 paraujanas, 5
  kalinago, 4 caribe-continental) y sólo al tier 1.
- **2 de esas 25 son `taíno-reconstruido` desde el lokono**: `akcicyaa`
  (< Lok. `akkicyaha`) y `wagulo` (< Lok. `wabulo`). Pasan porque
  `normalize_source_language('taíno-reconstruido')` devuelve `'taíno'`: la capa
  que F8 separó en `fuente` se vuelve a juntar en la puerta. El lokono es
  **andamio** y no debe verlo nadie —vernos el andamio hace circular la
  medición— y aquí entra por la puerta de la esfera con etiqueta taína.
- `taino_hipotetico.json`: **nadie lo lee**. Las 7 referencias que hay en todo
  el repo están en `arahuaco_comparative.py` (lo genera) y
  `patch_integrate_comparative.py` (lo **escribe**). No se importa, no llega al
  prompt, no cuenta en el score. Es un artefacto muerto de 26 entradas, 22 de
  ellas duplicadas de claves que ya están en el lexicón.
- `loanword_uses`: 40 filas, 35 taínas, **11 voces distintas**
  (`maisi` 11, `yuca` 8, `cazabi` 6, `casabe` 2, `u-maíz` 2, y una cada una
  `bohío`, `cacique`, `maíz`, `aji`, `maboya`, `maboya-ubana`). La tabla nació
  con la migración `20260916000000`: **no es el censo del habla**.
- **El cero verificado** (regla 6): barrido de las **3.811** respuestas de
  `agent_responses` (51 runs, 3,7 MB de texto). **41 de las 52 no se han dicho
  jamás.** Las 11 que sí, con ocurrencias: `casabe` 179, `yuca` 107, `maíz` 103,
  `cacique` 35, `bohío` 33, `bohio` 4, y una sola vez cada una `aji`, `batata`,
  `maboya`, `papaya` y `taita`. Ojo al leerlo: `maisi` y `cazabi` salen a **0**
  en el texto y a 11 y 6 en `loanword_uses`, porque el agente escribe la forma
  castellana y la base guarda la de la esfera (`maisi <- maíz`,
  `cazabi <- casabe`). Las dos cifras son ciertas y miden cosas distintas.

---

## La clasificación

| Clase | Cuántas |
|---|---|
| (i) fuente primaria localizable | 10 — y 4 de ellas con la cita rota (arriba) |
| (ii) sólo fuente secundaria | 0 |
| (iii) **sin fuente ninguna** → `deuda: sin-procedencia` | **42** |
| (iv) sospechosas de no ser taínas | 8 declaradas |

Las (iv), con su razón: `caiman` (Alvarado: «voz taina **y galibi**»),
`piragua` y `papaya` (étimo caribe en la lexicografía corriente; ninguna cita
nada), `taita` (voz de crianza panamericana; la atestación es un diccionario
cubano del XIX), `maboya` (más citada como caribe insular), `tabako` (la forma
taína atestiguada es `cohiba`/`cohóba`, que el lexicón tiene aparte), y
`cacique` y `maíz`, que son taínas sin discusión pero conviven con `cacike` y
`maisi` sin que ninguna de las cuatro cite nada.

---

## La cuarentena: el número que más importa

**Ninguna de las 56 viene de la recuperación contemporánea del taíno.** No es
una impresión, es procedencia: las 52 entraron en cinco commits de junio de
2026 y las 26 del JSON **las generó este proyecto** con
`arahuaco_comparative.reconstruir_taino()`.

**Pero 15 marcas de perfil —8 formas del lexicón y 7 del JSON, en buena parte
las mismas claves— coinciden con lo que produce la recuperación contemporánea,
porque se hicieron con el mismo método.** Los proyectos vivos (Hiwatahia–Higuayagua, de Jorge Baracutay Estevez
y Jessie Hurani Marrero, con 20.000 entradas en 2023; Tainonaíki, de Javier A.
Hernández, con alfabeto propio desde 2019) declaran abiertamente que rellenan
los huecos del taíno con **lokono, wayuu y garífuna**. Nosotros rellenamos los
nuestros con lokono. Son 8 del lexicón (`abba`, `acoa`, `aduri`, `agari`,
`daca`, `thigisi`, `wacusi`, `wagulo` — todas `cuerpo` o `gramatica`) y 7 del
JSON.

No nos contaminaron: **lo hicimos nosotros**. Eso es peor de arreglar y mejor de
auditar, porque sabemos exactamente dónde está.

El criterio operativo, con sus cinco marcas, está en
`taino_fuentes_mapa_2026-09-21.yaml` §cuarentena. Y los proyectos se describen
ahí con respeto, que es lo que merecen: son comunidades vivas rehaciendo su
lengua, y que no sean evidencia del s. XVI es la misma frase que vale para
nosotros.

---

## Lo que hay que decidir

### A. Las 42 sin fuente ninguna

- **A1.** Declarar `deuda: sin-procedencia` en las 42 y dejarlas donde están.
  El hueco se admite (regla 8), nada se mueve, nadie deja de hablar.
- **A2.** A1 + **poner la cita de Alvarado 1921 con página a las 14 que ya se
  pueden citar** (`procedencia.obra: alvarado-1921`), sin `tuna` —cuya glosa no
  coincide— y confirmando a mano las cinco que el emparejador estrecho se deja.
  Pasa ~13-18 entradas de la clase (iii) a la (i) sin abrir una sola sesión de
  minería nueva.
- **A3.** A2 + **archivar** en `FUERA_DEL_HABLA` las que no se hayan dicho
  nunca y no citen nada, hasta que alguien las sostenga. Son 41 sin uso ∩ 42 sin
  fuente. Es agresivo y mueve `FORMAS_DE_PLANTILLA`.

**Recomiendo A2.** Es medido, barato y reversible, y no mueve el score.

### B. Las cuatro citas rotas a Brinton

- **B1.** Borrar «Brinton 1871» de `casabe`, `cohiba`, `higuana` y `tuna` y
  declararlas `deuda: sin-procedencia`.
- **B2.** B1 + corregir la glosa de `mayani` a lo que dice la fuente ('de
  ningún valor, nada'), abrir issue por `caney` (circular, no rectangular),
  `batey` (el juego, no la plaza) y `areito` (canto, no danza), y **no**
  tocarlas hasta que T1/T2 lean el pasaje.
- **B3.** No tocar nada hasta que T1/T2 cierren su minería de Brinton.

**Recomiendo B2.** Una glosa mal leída es canon falso, y las cuatro las dejamos
**abiertas**, no resueltas: quien lee el pasaje es T1/T2 (skill §8: no se
reescribe una glosa en una minería ajena).

### C. `taíno-reconstruido` y `taino_hipotetico.json`

- **C1.** Dejar los dos como están. Cuesta: el lokono seguirá llegando al
  prompt con etiqueta taína (`akcicyaa`, `wagulo`).
- **C2.** **Sacar `taíno-reconstruido` de la esfera**: que
  `normalize_source_language` deje de colapsarlo en `'taíno'`, o que
  `voces_de_fuera_posibles()` lo filtre. Las 9 se quedan en el lexicón con su
  etiqueta —archivar no es borrar— pero dejan de enseñarse como voz de la
  esfera. Toca `curiana_sim/`: va en un corte de serie, medido con el patrón
  A/B, y mueve el bloque `[Voces de fuera]` de 43 a 41 candidatas.
- **C3.** C2 + **borrar `taino_hipotetico.json`**, que no lo lee nadie, o
  moverlo a `6-fusion/` con su fecha para que se vea que es una propuesta
  muerta y no un dato.
- **C4.** C3 + aplicar al taíno la política «donde hay atestiguada, manda la
  atestiguada»: `abba` 'uno' cede ante `hequeti`, que está atestiguado en Las
  Casas vía Brinton.

**Recomiendo C2 + C3.** C2 es el único hallazgo de esta parcela que está
haciendo daño ahora mismo. C3 es higiene y cuesta cero. C4 lo dejaría para
después de que T1/T2 lean Las Casas: es una decisión sobre la política, no
sobre el taíno.

### D. Qué obras conseguir

- **D1.** Sólo las gratis: **Goeje 1939** (abierta en Persée, 128 pp.) y
  **Bachiller y Morales 1883** (íntegra en archive.org). Coste cero.
- **D2.** D1 + **minar Anglería 1892**, que ya está en casa y sin minar.
- **D3.** D2 + comprar **Granberry y Vescelius 2004**, que es la única obra que
  nos dejaría decir de QUÉ taíno es cada voz (clásico, ciboney, macorís,
  ciguayo…) — la trampa 3 de esta campaña — y separar taíno de caribe insular.
- **D4.** D3 + **Zayas 1914** (dominio público, en dLOC) y **Arrom**, para las
  entradas de cosmología (`cemi`, `maboya`, `bejique`, `areito`) que no están ni
  en Alvarado ni en el vocabulario de Brinton.

**Recomiendo D2 ahora y D3 después.** D2 no cuesta dinero ni espera: Goeje
zanja los casos caribe/taíno de la clase (iv), Bachiller ya está alimentando
nuestro lexicón a dos saltos vía Alvarado, y Anglería es la fuente de primera
mano de cinco citas que hoy son de segunda.

---

## Lo que vi de paso y no es de esta parcela

1. **`kunuku` es la única entrada taína bien citada de las 52** (Alvarado 1921
   p. 89 + Las Casas V.307 + van Buurt 2014) y entró en la minería del vault
   del 2026-08-04. Es la prueba de que el protocolo funciona cuando se aplica:
   lo que falla es lo que entró antes de que existiera.

2. **`sostiene` no mide lo que parece.** `4-fuentes/brinton-1871.md` declara
   `entradas_lexicon: 84`, y 0 de las 52 taínas tienen `procedencia.obra`. No es
   una contradicción: `medir_sostiene.py` cuenta el lexicón por **coincidencia
   de alias en `notas`**, no por clave foránea (lo dice su propio docstring).
   Merece decirse en la nota, porque «84 entradas» se lee como «84 entradas
   citan a Brinton» y lo que hay son 84 menciones de texto — de las cuales, en
   la muestra taína, casi la mitad no se verifican.

3. **Cuatro pares castellano/indígena sin decidir del todo.** `cacique`/`cacike`,
   `maíz`/`maisi`, `bohío`/`bohio`, `casabe`/`cazabi` son ocho entradas para
   cuatro conceptos; `FORMA_DE_LA_ESFERA` resuelve cuál se **enseña**, pero las
   ocho siguen en `VOCABULARIO_BASE` y tres de las castellanas (`bohío`,
   `cacique`, `maíz`) tienen `notas` vacías. Es una campaña pequeña de higiene.
