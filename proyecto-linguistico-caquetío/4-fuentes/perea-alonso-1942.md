---
tipo: fuente
obra: "Filología comparada de las lenguas y dialectos arawak, tomo I"
autor: "Perea y Alonso, Sixto"
anio: 1942
genero: gramatica
local: "fuentes_caquetios/Perea_Alonso_1942_Filologia_Comparada_Arawak_TomoI.pdf (926 pp., ÚTIL)"
paginas: 926
capa_texto: si
estado_minado: minada-parcial
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-08
minado: 2026-09-08
cobertura: "Parte I (Fraseario, pp. 1-541) vaciada por script. Parte II (Compendio Gramatical) leída a mano hasta la p. 601; el verbo (pp. 602-680) sin minar. Introducción (Río de la Plata) fuera de alcance."
aliases: ["Perea Alonso 1942", "Perea y Alonso 1942", "Filología comparada arawak"]
---

# Perea y Alonso 1942 — *Filología comparada de las lenguas arawak*, tomo I

## Lo primero: estaba descartada, y la descartamos por la pregunta equivocada

El 2026-07-29 esta obra se cerró como **descartada**, con este motivo: *"se
esperaba trabajo comparativo entre lenguas arahuacas; resultó ser gramática
lokono pura, no comparativa"*. `CLAUDE.md` la registraba como precedente de
*"no dio resultado"*.

El diagnóstico era correcto y la conclusión ya no lo es. Con **D11 decidida el
2026-09-08** —rebalancear hacia el eje lokono-taíno— la pregunta cambió, y
"gramática lokono pura" pasó de ser el defecto a ser exactamente el material
que hace falta. Es la **única pata de la fase 1 que no depende de una compra ni
de una descarga**.

Vale como precedente al revés: *descartada para lo que se le preguntó entonces*
no es *inútil*. Conviene releer la lista de descartadas cada vez que cambia una
decisión de rumbo.

Corrección de paso: el autor es **Sixto** Perea y Alonso, no Sigfrido. El libro
lo nombra diecisiete veces.

## Qué es realmente

Tres cosas distintas encuadernadas juntas, y sólo la segunda y la tercera
sirven al proyecto:

| Parte | pp. impresas | Qué es |
|---|---|---|
| Introducción | I-CX | *Apuntes para la prehistoria indígena del Río de la Plata*: la tesis de que charrúas, chanás, guenoas y minuanes hablaban dialectos arawak. **Fuera de nuestro alcance.** Trae un vocabulario chaná/guenoa/charrúa/minuán con comparanda arawak al margen |
| **I — Fraseario** | **1-541** | **Concordancia lokono de los Hechos de los Apóstoles.** El material |
| **II — Compendio Gramatical** | **545-~700** | **Fonética, morfología y sintaxis del lokono**, sobre Schumann y Quand. Minado hasta la p. 601; el verbo (602-680), no |

El **Fraseario** es la pieza. Perea vació el texto bíblico de **Theodor
Schultz, 1802** —*Act Apostel-nu*, los Hechos de los Apóstoles, traducido del
alemán para la misión morava de la Guayana Holandesa— y lo ordenó por concepto.
Cada una de las **1.060 entradas numeradas** da:

- el concepto en español, con sus glosas **latina, portuguesa, francesa e
  inglesa** (que desambiguan la acepción exacta, cosa que un vocabulario
  español-arawak solo no haría);
- debajo, **todas** las frases lokono donde la voz aparece, **citadas por
  capítulo-versículo** y **ya segmentadas en morfemas por el propio Perea**.

Es decir: no es una lista de palabras, es un **corpus con concordancia**. Cada
forma viene con su contexto y su ancla verificable.

## Qué ha dado (medido el 2026-09-08)

Propuesta en `6-fusion/lokono_perea_1942.yaml`, generada por
`curiana_sim/minar_perea.py`.

| | |
|---|---|
| Entradas numeradas del Fraseario | 1.060 |
| Parseadas | 1.040 (las 20 restantes caen en las 29 páginas que faltan del escaneo) |
| Raíces lokono aisladas tras la criba | **724** |
| Corroboran una entrada del lexicón | 38 (12 con la glosa también) |
| **Nuevas** | **686**, de ellas **201 con dos o más atestaciones** |

Para el orden de magnitud de D11: la columna lokono del lexicón tiene hoy 275
entradas y la wayuu 781. Esta fuente sola aporta 686 candidatas nuevas.

### El hallazgo que más pesa: la columna A-2 auditada

`6-fusion/auditoria_a2_perea.yaml`.

🔴 **Corrección del 2026-09-09.** Escribí que esta auditoría contrastaba la
columna de Oliver contra una fuente **independiente**. Es falso, y lo desmiente
el propio Oliver: al reseñar las fuentes del lokono en su capítulo 2 dice que
las obras de Quandt y Schultz *«have been the subject of a small paper by
Brinton (1871) and a very detailed philological analysis by Silvio Perea y
Alonso (1942)»*, y más adelante cita *«(Perea y Alonso 1942)»* como la fuente
de sus etimologías lokono. **Perea es una de las fuentes de Oliver.**

Eso convierte la tabla en otra cosa: no es corroboración, es **control de
transmisión**. Dice que la columna es fiel a la fuente que Oliver usó — útil
para detectar deriva y errores de copia, inútil como voto a favor de D11. Es la
trampa del §8 del protocolo de minado, la misma de Jahn citando el apéndice de
Oviedo. Lo que sí queda en pie: Oliver da las formas **sin cita**, y Perea las
da con capítulo y versículo, así que ahora son verificables una a una.

De las 18 filas: **14 coinciden, 2 divergen** (sangre, grande) y **2 están
ausentes de la obra entera** (arena, raíz). La primera pasada dio 12/2/1/3 y
estaba mal medida — ver el aviso más abajo.

Las dos divergencias son ahora lo más interesante de la tabla: son puntos donde
la columna de Oliver se aparta de una fuente que él mismo reseñó, y cada una
está sostenida en tres o cuatro lugares del libro.

Y las dos filas que el proyecto más usa quedan **ancladas a un versículo**:

- **luna**: `catti`, Hechos 2-20, *«dia tu-ppa CATTI ù-ttù bia»* = «como también
  la LUNA en sangre» (pp. 60 y 66). La fila bandera del cómputo del 2026-08-31
  —CQ *cati* ~ LK *kathi*, similitud 1.00— ya no depende de una sola columna.
- **diente**: `na-ri-sibu`, Hechos 7-54, *«crujían SUS DIENTES»* (p. 32).
  Atestigua la raíz `-ri` que Oliver empareja con el caquetío *dare* en su
  p. 147.

### Otras corroboraciones con cita

`wadi-li` 'varón' (x9), `cabbuin` 'tres' (x7), `hadda-lli` 'sol' (x3), `biama`
'dos' (x3), `cairi` 'isla' (x2), `siba` 'piedra', `luccu` 'persona', `bibiti`
'cuatro', `hallicai` 'quién', `abba` 'uno'. Varias estaban en el lexicón como
*"forma Brinton 1871"*: ahora tienen **segunda atestación independiente**.

### Un dato que toca la corrección sobre `daca`

El lexicón reconstruye el taíno `daca` 'mano' desde un supuesto lokono *daka*.
Perea da la mano lokono como **`-ccabbu`** con cinco atestaciones —`lù-ccabbu`
'su mano', `bu-ccabbu` 'tu mano', `na-ccabbu` 'sus manos'— que es la forma
`akkabu` que el lexicón ya tiene por otro lado. No resuelve de dónde salió
*daka*, pero refuerza que ahí hay algo que revisar.

### Una trampa que nombra el propio autor y el cruce reencontró

Perea avisa (p. 546) que la alternancia r/l hace que la postposición
`-ruccu ~ -luccu` 'en, dentro' colisione con `luccu` 'hombre, persona, indio'.
El cruce automático cayó justo ahí: propuso `lluccu` 'como, según, conformar'
contra la entrada `lukku` 'hombre, persona' del lexicón. Homónimos, no cognados.

## Qué NO ha dado, y por qué

**El Fraseario es la concordancia de un libro, y ese libro es los Hechos de los
Apóstoles.** Su campo semántico es el de una narración mediterránea del siglo I.
Buscando el lema exacto: **no hay entrada para agua, árbol, arena, raíz, pez ni
casa**.

⚠️ Y el aviso que me tuve que hacer a mí mismo el mismo día: **el índice de
lemas no es la obra**. Agua (`wuni-abu`) y árbol (`adda`) sí están, en el
Compendio Gramatical, pp. 559 y 556. La primera pasada de la auditoría los dio
por no medibles porque sólo había buscado en el Fraseario. Arena y raíz sí
faltan de las 926 páginas — eso está verificado contra la obra entera.

Consecuencia operativa para la fase 1 de D11: esta fuente **no equilibra la
columna wayuu concepto por concepto**. La equilibra en gramática, partículas,
partes del cuerpo, parentesco y vocabulario abstracto — y deja intacto el hueco
del léxico ecológico y material, que es justo donde el caquetío atestiguado
tiene más masa. Para ese hueco hacen falta de Goeje 1928 o Bennett 1989.

Del Fraseario no sale nada de otras esferas: ni geografía política, ni
ecología, ni parentesco. El **Compendio** sí — la terminología de parentesco de
su p. 556 va a la esfera de mundo, no al lexicón.

## Cómo se lee este PDF (para quien vuelva)

- **`pdftotext -enc UTF-8`**, no `pypdf`. Salida en
  `fuentes_caquetios/Perea_Alonso_1942_..._TomoI.txt`.
- **El escaneo repite pliegos.** Hay páginas impresas que aparecen dos y tres
  veces (todo el preliminar VI-XII, y bastantes del Fraseario), y **faltan 29**.
  Por eso el desfase pdf→impresa **deriva** y no se puede sumar una constante:
  hay que leer el número impreso de cada página. Orientativo: el Fraseario ocupa
  pdf 165-763 = impresas 1-541.
- **Clave panfonética propia** (p. impresa CI): `c` = /k/ siempre (sólo en ca,
  co, cu; `k` en ke, ki), `q` = k, `ù` = ü alemana, `x` = sh inglesa, `cx` = ch
  española, `w` = w inglesa. Y él mismo dice (p. 546) que las geminadas alternan
  «sin motivo aparente» — l/ll, d/dd, t/tt — así que para comparar se colapsan.
- **El estrato importa**: esto es lokono de **1802**. Perea documenta que el de
  Brett (1849) ya diverge —«la g sustituye con frecuencia a la k de los Moravos,
  y la i, u, t de aquéllos se ha transformado en e, o, cx»—, de modo que este
  material está **más cerca en el tiempo** de los documentos caquetíos que
  Goeje 1928, Brinton 1871 o Pet 1987.

## La Parte II: el Compendio Gramatical (minado el 2026-09-08)

Propuesta en `6-fusion/lokono_gramatica_perea_1942.yaml`. Leída a mano —son
paradigmas y prosa, no entradas repetidas— hasta la p. 601.

Lo que da, y que el proyecto no tenía de ninguna lengua hermana con paradigma
completo:

- **Índices personales** (p. 587, de Schumann): `da-` mi, `bu-` tu, `lù-` su
  (vr.), `tù-` su (nv.), `wa-` nuestro, `hù-` vuestro, `na-` su (pl.), `u-/ù-`
  absoluto. Y la forma libre `de` = 'yo' (p. 550) — el prefijo /da-/ que Oliver
  invoca como su primer apoyo de D11, con paradigma.
- **Género varonil / no varonil**, no masculino/femenino (p. 554): `-ti/-tti`
  vr., `-tu/-ttu` nv., plural `-nu`. El no varonil cubre mujeres, animales y
  cosas. Esto es lo que valida el inventario de afijos con que se aisló la raíz
  en el Fraseario.
- **Atributivo `k-` frente a privativo `m-`**, con par mínimo: `k-ere-u-ti`
  'casado' / `m-ere-u-ti` 'soltero' (p. 555). Le quita el aire de recurso *ad
  hoc* a la lectura que Oliver propone del `ki-` de *bariki*.
- **El sistema pentevigesimal** (pp. 565-568): 5 = `abba-te-cabbe` 'una mano',
  10 = `bi-ama-te-ccabbu` 'dos manos', **20 = `abba luccu` 'un hombre'**. Con la
  cautela del propio Perea sobre si los numerales de los moravos son auténticos.
- **`-cundi` / `-cunna-tu` / `-cunna-na` = 'gente de, vecino de, habitante de'**
  (p. 565): `Berbice-cundi`, y en el texto `egypten-cun-di` 'el egipcio'. El
  mecanismo lokono para hacer gentilicio sobre topónimo. El caquetío no tiene
  uno declarado en el canon.
- **Una terminología de parentesco cruzada** (p. 556) — va a la esfera de mundo,
  no al lexicón: `a-ttilliki-tti` 'hermano **de mujer**' frente a `u-yurda-tu`
  'hermana **de varón**', `a-buki-ti` 'hermano mayor de varón' frente a
  `ittilla-tu` 'hermana mayor de mujer'. Raíces distintas según el sexo del
  hablante, no sólo terminación.

### Y lo que toca decisiones ya tomadas

Con la cautela escrita al lado en la propuesta: esto es evidencia **comparativa
de una lengua hermana**, no evidencia sobre el caquetío.

- **`u-banna` = 'sobre, encima, la superficie de'**, ocho o más apariciones:
  *wunabu u-banna-man* 'por sobre toda la tierra', *SURA u-banna* 'la azotea',
  *casaccu u-banna* 'arriba en el cielo'. **Corregido el 2026-09-09**: escribí
  que era «el mismo campo semántico» que el `-bana` 'cerro, sitio alto' de D9, y
  no lo es. Oliver mismo glosa el `-bana` lokono como *'surrounding'*,
  *'expanse'* y *'roof, cover'* — **sin citar de dónde** —, y lo que Perea aporta
  son justo las atestaciones que a esa glosa le faltaban. Eso queda **más cerca
  del 'ancho, llano' de van Buurt** que del 'cerro' de D9. No derriba D9, que se
  apoya en seis apoyos venezolanos y en el lema directo de Zavala; pero mi
  lectura estaba forzada hacia la conclusión que me convenía.
  Lo que sí sostiene, y es el argumento real de Oliver, es la **b**: su apoyo es
  *«-bana instead of -pana»*, o sea la misma correspondencia b/p de
  *barisi* : *palii*. Y en lokono `pana` es otra raíz por completo — 'matar,
  herir' —, así que la b- de `-banna` no es un accidente de transcripción.
- **Un `-na` locativo-instrumental** sobre la durativa `-coa-/-kua-` (p. 561):
  `a-hùrki-da-coa-na` 'lugar de reunión', `a-balti-coa-na` 'asiento'. No
  resucita la glosa 'lugar de' de `-ana` que **#109** retiró —el censo de
  Esteves midió cero y sigue midiendo cero—, pero dice que la hipótesis no era
  absurda: era insostenible *con el dato caquetío*.
- **`-ccabbu` 'mano'**, confirmada además por los numerales. Refuerza que el
  `daca` 'mano' reconstruido desde un supuesto lokono *daka* hay que revisarlo:
  Perea no da *daka* en ninguna parte.

## Qué falta

- **El verbo** (pp. 602-680): paradigmas completos de conjugación —`iyaha`,
  `ttuba`, `sonnucu`, `halli`, `kebbe`, `hadubu`—, aspecto y modo. Es lo único
  que queda del tomo I.
- Las **201 raíces nuevas con dos o más atestaciones** esperan fusión humana.
- Las **486 con una sola** son cola, no lote.
- La **introducción rioplatense** trae comparanda arawak general (`WUNI` agua ~
  maipure/baniva/yavitero `WENI`) que nadie ha mirado.
- Los tomos II a V nunca se publicaron o no están en el repo; el tomo III iba a
  ser el **vocabulario arawak-español**, que es lo que de verdad haría falta.

## Enlaces

[[brinton-1871]] · [[oliver-1989-cap2]] · [[medina-colina-sxx]]
