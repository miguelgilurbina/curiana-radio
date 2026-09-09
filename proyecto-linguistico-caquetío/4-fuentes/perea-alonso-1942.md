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
cobertura: "Parte I (Fraseario, pp. 1-541) vaciada por script. Parte II (Compendio Gramatical, pp. 545-~700) sin minar. Introducción (Río de la Plata) fuera de alcance."
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
| II — Compendio Gramatical | 545-~700 | Fonética, morfología y sintaxis del lokono, sobre Schumann y Quand. **Sin minar** |

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

`6-fusion/auditoria_a2_perea.yaml`. La columna lokono de la tabla A-2 de Oliver
es la que sostiene D11, y hasta hoy nadie la había contrastado con una fuente
primaria **independiente** — las entradas lokono del lexicón vienen de Goeje
1928 y Brinton 1871, y Oliver bebe de los mismos. Perea vacía a Schultz 1802
directamente.

De las 18 filas: **12 confirman, 2 divergen (sangre, grande), 1 parcial, 3 no
son medibles** porque los Hechos no dicen esas palabras.

Y las dos filas que el proyecto más usa quedan con atestación primaria:

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
Verificado buscando el lema exacto: **no hay entrada para agua, árbol, arena,
raíz, pez ni casa**.

Consecuencia operativa para la fase 1 de D11: esta fuente **no equilibra la
columna wayuu concepto por concepto**. La equilibra en gramática, partículas,
partes del cuerpo, parentesco y vocabulario abstracto — y deja intacto el hueco
del léxico ecológico y material, que es justo donde el caquetío atestiguado
tiene más masa. Para ese hueco hacen falta de Goeje 1928 o Bennett 1989.

Tampoco toca ninguna otra esfera: no da geografía política, ni parentesco
caquetío, ni ecología. Es una fuente de **una sola esfera** a propósito.

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

## Qué falta

- **La Parte II, el Compendio Gramatical** (pp. 545-~700): fonética, artículo,
  género, número, caso, posesivos, verbo, sintaxis. Es el mejor material del
  repo para contrastar la morfología del caquetío reconstruido, y sigue sin
  minar. El paradigma posesivo está en la p. 587.
- Las **201 raíces nuevas con dos o más atestaciones** esperan fusión humana.
- Las **486 con una sola** son cola, no lote.
- La **introducción rioplatense** trae comparanda arawak general (`WUNI` agua ~
  maipure/baniva/yavitero `WENI`) que nadie ha mirado.
- Los tomos II a V nunca se publicaron o no están en el repo; el tomo III iba a
  ser el **vocabulario arawak-español**, que es lo que de verdad haría falta.

## Enlaces

[[brinton-1871]] · [[oliver-1989-cap2]] · [[medina-colina-sxx]]
