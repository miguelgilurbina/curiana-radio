# El taíno y el caquetío: qué comparten de verdad

Miguel, 2026-09-21, encargando la campaña del taíno:

> «Y analizar también las similitudes con el Caquetío.»

**Esto es una MEDICIÓN.** Al hacerla no se tocó nada: ni `curiana_lexicon.py`,
ni `lexicon_*.py`, ni `2-lengua/`, ni `3-mundo/corpus/`, ni `cognados.yaml`
(regla 5). **Ningún cognado entra al canon por este archivo.**

| archivo | qué tiene |
|---|---|
| `6-fusion/scripts/cruce_taino_caquetio.py` | lo mide todo y escribe el YAML. `--check` dice si está al día |
| `6-fusion/cruce_taino_caquetio_2026-09-21.yaml` | el cruce entero: parejas, auditoría del cero, morfología, onomástica, controles |
| `6-fusion/control_jirajarano_jahn_1927.yaml` | la lista de CONTROL no arahuaca (Jahn 1927 pp. 388-391), generada aparte |

Ninguna cifra de aquí abajo está escrita a mano: las imprime el script.

---

## 0. Lo primero: tres cosas del encargo que resultaron falsas al medirlas

1. **`ni-` de `nitaíno` no es un prefijo pronominal, y quien lo desmiente es la
   fuente de la que salieron nuestras voces taínas.** [[brinton-1871]], p.
   impresa 14: *«There is not the slightest authority for this»* — y añade que
   tampoco la hay para suponer, con Von Martius, que la primera sílaba sea un
   prefijo pronominal. Lo deriva del arahuaco `nuddan` 'estar firme, hacer algo
   bien'. Estaba descartado desde 1871 en el libro que ya teníamos.

2. **`curiana_sim/jirajaroide_frontera_lexicon.json` no sirve como control.**
   El encargo lo proponía. De sus **20 entradas, 10 son ranuras vacías con la
   forma literal `?`**; de las 10 que quedan, **4 son caquetío** y las 6 restantes
   son topónimos y etnónimos sin glosa léxica. **Cero conceptos cruzables.** (Y
   de paso: su propio `_estadisticas.pendientes_verificacion` dice **9** donde
   las ranuras vacías son **10** — una cifra a mano dentro del archivo, regla 1.)
   El control se sacó del vocabulario jirajara/ayomán de [[jahn-1927]]
   (85 filas, **83 con forma comparable**), que sí sirve.

3. **`daca` no es lo que el lexicón dice que es.** El encargo la nombraba como
   evidencia del `da-` de 1ª persona, y tiene razón — pero el lexicón la tiene
   como `taíno-reconstruido` con la glosa **'mano'**, reconstruida desde el
   lokono `daka`. La forma que [[pane-c1498]] atestigua (cap. XXV) es `daca`
   **'yo'**: *«Dios naboria daca»*, glosado por el propio Pané «yo soy siervo
   de Dios». Son dos cosas distintas bajo la misma clave. Ver §5(F).

Y una cuarta, del método y no del encargo: **el cero del cruce léxico no mide
las dos lenguas, mide las dos listas.** Todo el §2 es eso.

---

## 1. El veredicto, en una frase

**El taíno y el caquetío atestiguado no comparten ni una sola pareja léxica
medible con la lista que el repo tiene hoy; lo que comparten es lo que comparte
toda la familia arahuaca (`ma-` privativo, `da-` de 1ª persona, el nominalizador
`-(h)o`) más un puñado de tainismos que llegaron con el castellano — y las dos
onomásticas no comparten formantes.**

```
═══ RESUMEN, capa caquetío-atestiguado (228 entradas) ═══
  taíno        entradas    39 · comparables   4 · parecidos  0 (azar 0.03, p=1.0)   · sim media 0.294 (azar 0.308)
  lokono       entradas   638 · comparables  43 · parecidos  5 (azar 0.98, p=0.0)   · sim media 0.370 (azar 0.305)
  wayunaiki    entradas   769 · comparables  36 · parecidos  3 (azar 0.44, p=0.007) · sim media 0.348 (azar 0.290)
  achagua      entradas  3568 · comparables  70 · parecidos  1 (azar 0.71, p=0.52)  · sim media 0.329 (azar 0.302)
  kalinago     entradas    23 · comparables   8 · parecidos  2 (azar 0.24, p=0.017) · sim media 0.472 (azar 0.336)
  paraujano    entradas    47 · comparables  12 · parecidos  3 (azar 0.15, p=0.0)   · sim media 0.413 (azar 0.262)
  jirajarano   entradas    83 · comparables  12 · parecidos  0 (azar 0.08, p=1.0)   · sim media 0.215 (azar 0.289)
```

**El taíno empata con el control.** El jirajara/ayomán no es arahuaco, tiene más
conceptos comparables con el caquetío (12) que el taíno (4), y da el mismo cero.
La única lengua que gana claramente al azar es el **lokono** (5 parecidos donde
el azar da 0,98; p = 0,000), que es exactamente lo que Oliver sostiene y lo que
D11 ya tiene escrito. El achagua **no** supera al azar (p = 0,52) pese a sus
3.568 entradas — el modelo nulo está haciendo su trabajo.

---

## 2. Léxico: el cero, y por qué es un cero de la lista

### 2.1 Los cuatro conceptos comparables, uno a uno

Con un denominador de cuatro, los casos **son** el resultado:

| concepto | caquetío atestiguado | taíno | sim |
|---|---|---|---:|
| iguana | `barbache` (Zavala #33) | `iwana` / `higuana` | 0,33 |
| cacique | `boratio` (Zavala p. 66) | `cacike` | 0,31 |
| dos | `gudamuen` (Zavala #148) | `yamosa` | 0,29 |
| río | `paro` (Zavala #195) | `tuna` | 0,25 |

Los cuatro muy por debajo del umbral (0,62). Y **el más interesante es 'dos'**:
es numeral, o sea del dominio que casi nunca viaja, y por tanto el único de los
cuatro que valdría como dato de filiación. `gudamuen` no se parece a `yamosa`
ni a nada — ni al lokono `biama` ni al wayuu `piama`. Eso es un dato del
caquetío, no del taíno, y merece mirarse aparte.

### 2.2 Veinte descartados por glosa sólo cercana

El filtro de significado descartó 20 voces caquetías que tienen glosa *cercana*
en taíno pero no idéntica: `ateri` 'hombre, varón', `diao` 'señor principal',
`para` 'mar', `wike` 'río navegable', `wa` 'conuco', `bagre` 'pez'… Están
listadas en el YAML. No son parejas perdidas: son glosas que no recortan igual
el mundo, y contarlas sería inventar el emparejamiento.

### 2.3 El paso por forma, sin filtro de significado: **15 de 15 ruido**

El encargo pedía cruzar también por esqueleto fonémico. Hecho, con el listón más
alto (0,75 y cuatro fonemas). Resultado:

```
  taíno        parejas  15 · con la glosa también  0 · ruido  15
  jirajarano   parejas   8 · con la glosa también  0 · ruido   8   (control)
  lokono       parejas  85 · con la glosa también  2 · ruido  83
  achagua      parejas 106 · con la glosa también  0 · ruido 106
```

Las quince taínas son la demostración de manual de por qué el filtro de glosa
existe: `kiba` 'piedra' ~ `cohiba` 'tabaco' (0,89), `kasi` 'sol' ~ `cazabi`
'casabe' (0,80), `kuna` 'pez' ~ `tuna` 'agua' (0,75), `buio` 'serpiente, dios
del trueno' ~ `bohio` 'casa' (0,75). **Ninguna significa lo mismo.**

### 2.4 Y ahora lo que de verdad explica el cero: la etiqueta

`2-lengua/cognados.yaml` **ya emparejaba** caquetío con taíno en **16 sets**, y
nadie los había auditado como grupo. El reparto:

```
ATESTIGUADO CON CITA                                  4
EL LADO CAQUETÍO NO ES CAQUETÍO                       4
SIN PROCEDENCIA                                       4
CIRCULAR: es un etnónimo                              2
NO ES UN COGNADO: la misma palabra escrita dos veces  2
```

- **Los 4 con cita** son de [[oliver-1989-cap2]]: `daitiao`~`daitia-o/waitiao`
  (p. 147), `dare`~`m-a(h)i-te` 'diente' (p. 147), `boratio`~`-atti-+-hu`
  (p. 147), `para`~`bara-wa` 'mar' (p. 150).
- **«El lado caquetío no es caquetío»**: `cognado-022` y `cognado-028` ponen
  `casabe` y `yuca` en la columna CQ, y el lexicón tiene esas dos claves
  etiquetadas **`taíno`**. Un set que empareja una voz taína con la misma voz
  taína no dice nada del caquetío. Igual `cognado-027` (`cairi`, que el lexicón
  tiene como `kairi` **lokono**).
- **«La misma palabra escrita dos veces»**: `canoa`~`canoa`, `hamaca`~`hamaca`,
  sin cita. Lo que prueban es que nosotros escribimos igual las dos columnas.
- **Circulares**: `caquetio`~`taino` y `karibna`~`caribe`. Emparejar el nombre
  de un pueblo con el de otro no es un cognado léxico — y `taino` como autónimo
  ya lo desmiente Brinton (§0.1).

**Y dos voces taínas que existen en el repo y el cruce no ve:**

| voz | dónde está | pareja caquetía | por qué importa |
|---|---|---|---|
| `siba` 'piedra' | en el lexicón, etiquetada **`lokono`**; `taino_hipotetico.json` la declara «Taíno atestiguado» y [[brinton-1871]] p. 14 la imprime *«Siba, a stone»* | `kiba` 'piedra' (forma_fuente `quiva`), **caquetío-atestiguado**, Zavala #218 + #92 | el cruce la puntúa **0,75 contra el lokono y 0 contra el taíno, y es la misma forma**. Es el ejemplo más limpio de que el cero mide la etiqueta |
| `bagua` / `bara-wa` 'mar' | `cognado-016` **con cita** (Oliver p. 150) y `cognado-019`; Brinton p. 11 *«Bagua, the sea»* | `para` / `parawa` 'mar', caquetío-atestiguado | **el lexicón no tiene ninguna entrada taína para 'mar'**. Es la pareja CQ~TN mejor citada que hay y el cruce por glosa no puede verla |

De las 14 formas que `taino_hipotetico.json` declara «Taíno atestiguado», **1 no
lleva la etiqueta `taíno` en el lexicón**: `siba`.

### 2.5 El límite duro, que hay que decir antes que nada

**Las 52 entradas taínas del lexicón tienen 0 `procedencia.obra`.** Las 43
atestiguadas dicen «Brinton 1871» en `notas`, y eso no es una clave foránea
(regla 8): el validador no lo comprueba. Por eso esto es un **script** y no una
tabla — cuando entren las transcripciones de T1/T2 con su procedencia, se vuelve
a correr y las cifras cambian.

---

## 3. Morfología: once candidatos, y la mayoría comparten sílaba, no morfema

La tabla completa, con la cita de cada lado, está en el YAML (`meta.morfologia`).
Resumen:

| candidato | veredicto |
|---|---|
| `ma-` privativo (`mahite`) | **mismo morfema** — y arahuaco común, no taíno-caquetío |
| `ma-` privativo (`manicato`) | indecidible: el sentido es negativo, pero nadie lo segmenta |
| `ka-`/`ca-` atributivo | **sin apoyo**: la sílaba está, ninguna fuente afirma el morfema en taíno |
| `da-` de 1ª sg. | **mismo morfema** — el mejor sostenido, y ya contado por D11 |
| `gua-` / `-gua` | **dos morfemas distintos con la misma sílaba** |
| `-bana` (Agüeybana) | mismo formante, **glosa distinta — y la distinta es la nuestra** |
| `-coa` / `-bakoa` | **no es el mismo morfema**: el `coa` taíno es un NOMBRE |
| `-(h)o` · gentilicio `-ío/-yo` | plausible para `-(h)o`; **no citable** para `-ío/-yo` |
| `-(i)tiao` (`guatiao`) | mismo morfema según Oliver — pero es el caso de la skill §8 |
| `ni-` / `nitaíno` | 🔴 **falso** (§0.1) |
| `-bo` / `-abo` | sin pareja — y es un hueco del propio canon caquetío |

Los tres que hay que leer despacio:

**`ma-` privativo — sí, pero no prueba lo que parece.** Brinton p. 13 segmenta
`mahite` contra el arahuaco *«marikata, you have no teeth (ma negative, ari
tooth)»*, y Oliver p. 147 n. 43 lo generaliza: el privativo `/mV-/` es **común a
las lenguas maipures**. O sea que confirma que el caquetío tiene lo que la
familia tiene, y **no acerca el taíno al caquetío más que a cualquier otra
hermana**. La sonda lo dice también: de las 39 voces taínas del lexicón, 5
empiezan por `ma-` y sólo una (`mayani` 'no') es plausiblemente privativa; de
las 342 formas caquetías atestiguadas, 4 empiezan por `ma-` y **ninguna** es
privativa (`manaure`, `masato`, `maure`, `mazato`). Contar sílabas no es contar
morfemas — es la trampa que el proyecto se tragó dos veces esta misma semana
(`macana` no sostenía `-kana`, y el `-po` de `apopo` era reduplicación).

**`gua-`: la trampa está, y debajo hay algo.** El `gua-` taíno que documentan
Brinton (p. 12, citando a Pedro Mártir: *«a very frequent prefix»*) y Oliver
(p. 147: marcador de 3ª plural) es un **prefijo**; el `-gua` caquetío del canon
es un **sufijo** locativo. Misma sílaba, posición contraria, función contraria:
contar uno como apoyo del otro sería repetir lo de `-kana`. **Pero** hay un
paralelo real y distinto: taíno `bara-wa` 'mar' y caquetío `para-gua` tienen la
misma raíz 'mar' y el mismo elemento detrás. No prueba la glosa 'región' — es la
**primera pista independiente que tiene la campaña de `-gua` (d21.7)**, que hoy
no cita a nadie.

**`-bana`: el paralelo taíno empuja contra D9.** Oliver p. 148 mete en la misma
bolsa el `-bana` caquetío, el taíno `pana-pe(n)` 'fruto del pan' y `Agüey-bana`,
el guajiro `a-pana` 'hoja' y el lokono `-bana` 'techo', todos bajo 'rodear,
cubrir, extensión'. El canon del proyecto le dio 'cerro, sitio alto' (D9, seis
apoyos caquetíos propios). Las dos cosas pueden convivir —la nota ya deja viva
la lectura 'ancho/llano' de van Buurt para `kabana`, `darubana` y `guacaubana`—
pero **el paralelo taíno no corrobora D9: tira al otro lado**, y conviene que
eso quede escrito antes de que alguien lo cite como refuerzo.

---

## 4. Onomástica: los dos sistemas no comparten formantes

La misma sonda sobre los tres corpus, lado a lado (tabla entera en el YAML):

| formante | topónimos caq. (78) | antropónimos caq. (48) | onomástica taína de Pané (78) |
|---|---:|---:|---:|
| `gua-` | 10 % | 8 % | **24 %** |
| `ma-` | 4 % | 6 % | 14 % |
| `-bana` | 8 % | 4 % | **0 %** |
| `-coa` | 6 % | 2 % | **0 %** |
| `-bo` | 6 % | 6 % | **0 %** |
| `-ey/-ay` | 3 % | 2 % | **0 %** |
| `-ana` | 12 % | 6 % | **0 %** |
| `-kiva/-quiva` | 5 % | 2 % | **0 %** |
| `-ex` final | 0 % | **0 %** | 6 % |
| `-el` final | 3 % | **0 %** | **21 %** |

⚠️ **El sesgo que hay que descontar**: los corpus no son del mismo género. El
caquetío sin descartar es sobre todo **toponimia** y la sonda de Pané es sobre
todo **antroponimia y nombres de mito**. Que `-bana` y `-coa` —formantes de
lugar— den cero en Pané puede medir que Pané casi no nombra lugares. **La
columna que sí compara género con género es la de antropónimos caquetíos**, y es
la que da los ceros más limpios: `-ex` 0 de 48 y `-el` 0 de 48, contra 6 % y
21 % en el taíno. Los antropónimos taínos se hacen con un juego de formantes
(`-ex`, `-el`: Guarionex, Guabancex, Marocael, Cacivaquel) que **no existe** en
el nuestro.

**El `-ey` de Esteves.** El canon tiene siete topónimos con la atribución
«taíno / caribe insular» de Esteves (`amuay`, `coabana`, `guayacanal`,
`maicara`, `maitiruma`, `oripopo`, `pitajaya`). `4-fuentes/esteves-1989.md` §6
ya dice que la atribución sale de **parecido de sonido sin documento** —
*«por su fonética la voz pertenece al caribe insular, como batey, mamey, caney,
carey»* (p. 14)— y que la etiqueta está mal puesta, porque el caribe insular de
Breton es una lengua arahuaca. Lo que este cruce añade: **esas cuatro voces son
castellano antillano**, entraron en el español antes de que nadie escribiera un
topónimo de Paraguaná, y en la onomástica taína de Pané el formante `-ey` da
**0 de 78**. Un `-ey` en Paraguaná mide la boca del cronista, no la lengua del
sitio. Es el mismo aviso que da Oliver p. 151 para `maraca`, `cacique` y
`barbacoa`: *«one must be careful about some terms offered by the Spanish as
"native" Caquetío»*.

**Los gentilicios en `-ío/-yo` — no citables.** «Luca-yo, Cigüa-yo, Kaket-ío»
sale de [[oliver-1989-cap2]] n. 44 p. 148, y Oliver la atribuye a **Gary
Vescelius, comunicación personal de 1982**. No hay dato publicado detrás, no hay
lista, y Lucayo y Ciguayo son exónimos coloniales. Escribirlo como apoyo sería
inventar una clave foránea. Lo que sí está argumentado, y no necesita a
Vescelius, es `kaket-ío` = `kake-` + `-(h)o` contra el lokono `kakïtho` (p. 148).

---

## 5. La pregunta de clasificación, con humildad

El caquetío atestiguado son **228 entradas de lexicón y 78 topónimos sin
descartar**, casi todo fitonimia y zoonimia de Paraguaná y Coro. Del taíno el
repo tiene **43 voces atestiguadas y ninguna con procedencia**. Eso no da para
una clasificación y este cruce no la intenta. Oliver, que tenía más, llama
«tentative» a la suya y dice que del caquetío **no hay medición** porque no
existe lista de 100 palabras.

Las posiciones que el repo tiene, con en qué se apoyan (detalle y citas en el
YAML, `meta.clasificacion`):

| quién | qué dice | se apoya en |
|---|---|---|
| Oliver 1989 | el caquetío sale del fondo del **lokono**; lokono, island carib, taíno y caquetío salen del mismo nodo | **datos** (`/dA-/`, `auri`, `kaketío`~`kakïtho`, `-bana`≠`-pana`) — salvo el descarte del guajiro, que es **geografía** y «preliminary» |
| Noble 1965 | el taíno es vástago directo del proto-arahuaco | porcentajes **sin lista publicada** — Oliver: «misleading and ambiguous at the very best» |
| Taylor 1977 | el taíno viene del proto-maipure; comparte más con el island carib que con el lokono | **datos**, 60 ítems; el propio Taylor deja abierto el préstamo |
| Rouse 1986 | el taíno evolucionó del proto-norteño | la opinión de Arróm y la escasez reconocida: *«room for disagreement»* |
| Vescelius 1982 | los etnónimos en `-ío/-yo` van juntos | **nada publicado**: una nota al pie de una conversación |

**Lo que nuestro material puede aportar**: decir si una voz caquetía atestiguada
tiene pareja taína con la misma glosa y de qué dominio es; medir cuántas de esas
parejas salen por azar (que es lo que ninguna de las posiciones de arriba hizo);
y dejar escritos los formantes que Oliver declara del caquetío y el canon nunca
recogió (`-bo`, `-oa`, `-kiva`).

**Lo que NO puede**: medir distancia lexicoestadística, decidir dónde cae el
caquetío en el árbol, ni usar el taíno como prueba a favor o en contra de D11 —
el `/dA-/` que comparten taíno y caquetío lo comparte también el lokono, y por
esa vía ya está contado. Contarlo otra vez por la vía taína sería **contar dos
veces el mismo dato**.

---

## 6. Las opciones, para Miguel

### La que pesa en el diseño del experimento

**¿El taíno sigue siendo sólo lengua de CONTACTO (esfera: se presta y no
penaliza), o pasa a ser también COMPARANDA de la reconstrucción (andamio, como
el wayuu y el lokono, que sí penalizan)?**

- **(A) Se queda como lengua de CONTACTO, y nada cambia en el motor.**
  `ESFERA_DE_CONTACTO` sigue igual, `prestamos_de_esfera` sigue sin penalizar,
  el tier 1 sigue recibiendo `[Voces de fuera]`. Lo que se añade es **deuda
  documental**: darles `procedencia.obra` a las 43, que es trabajo de T1/T2.
  *Coste*: ninguno en el motor. *Lo que se gana*: que la etiqueta diga la verdad
  medida — el taíno no es comparanda porque no hay proximidad medible.

- **(B) Pasa a COMPARANDA y penaliza.** Habría que meterlo en el andamio junto
  al wayuu y el lokono, sacarlo de `ESFERA_DE_CONTACTO` y hacer que hablar taíno
  reste. *Coste medido*: `6-fusion/medicion_hispanismos_loanword_uses_2026-09-17.yaml`
  dice que **111 de 161 formas-respuesta con préstamo son cinco voces taínas**
  (casabe, maíz, yuca, batata, papaya). Penalizarlas borraría justo el fenómeno
  que la esfera existe para medir, y va **contra** la decisión de Miguel del
  2026-09-17 («el producto de la esfera ES la esfera»). Y añadiría una tercera
  lengua-andamio **sin una sola clave foránea**, que es la enfermedad que D11
  está tratando de curar.

- **(C) Camino de en medio: contacto por defecto, comparanda declarada sólo para
  los cuatro sets con cita.** Los cuatro `ATESTIGUADO CON CITA` de
  `cognados.yaml` (todos de Oliver cap. 2) entran como comparanda con su página;
  el resto se queda en la esfera. *Coste*: hay que decidir si esos cuatro
  penalizan o no, y tres de los cuatro (`daitiao`, `boratio`, `dare`) son
  justamente las voces con la reserva de la n. 42 de Oliver.

- **(D) Congelar la decisión hasta que T1/T2 entreguen.** Re-correr
  `cruce_taino_caquetio.py` cuando las 43 tengan procedencia y decidir con el
  número nuevo. *Coste*: nada se mueve mientras tanto, y el script ya está hecho
  para eso.

**Mi recomendación: (A), con (D) como red.** El cruce no encontró ninguna
proximidad que justifique subir el taíno a andamio: empata con una lengua no
arahuaca de control, y su único paralelo morfológico sólido (`da-`) ya está
contado por el lokono en D11. Y (B) tiene un coste medido y contradice una
decisión tomada. Lo que sí hay que hacer, decida lo que decida, es **la deuda de
procedencia**: mientras las 43 no citen a nadie, cualquier número que salga de
ellas —este incluido— mide nuestra lista.

### Las secundarias, cada una con su letra

- **(E) `siba` 'piedra'.** Hoy es `lokono` en el lexicón, aunque
  `taino_hipotetico.json` la declara «Taíno atestiguado» y Brinton la imprime en
  su vocabulario taíno. Opciones: (E1) dejarla como está y anotar en `notas` que
  también está atestiguada en taíno; (E2) re-etiquetarla; (E3) duplicar la
  entrada con desambiguador de lengua, como `kati-kalinago`. Sea cual sea,
  `cognado-026` (`quiva`~`siba`) es hoy **el mejor candidato a subir de
  reconstruido a atestiguado con cita en los dos lados**.
- **(F) El homógrafo `daca`.** El lexicón: `taíno-reconstruido` 'mano', desde el
  lokono. Pané: `daca` 'yo'. Hay que decidir si conviven con desambiguador o si
  la reconstruida se archiva (la política de `atestiguado-manda` es de la parte
  caquetía, así que aquí no muerde sola).
- **(G) Los 8 sets malos de `cognados.yaml`.** Los 4 de «el lado caquetío no es
  caquetío», los 2 etnónimos circulares y los 2 «misma palabra dos veces».
  Opciones: retirarlos, o darles cita. Tal como están, inflan el número de
  cognados del canon con parejas que no dicen nada.
- **(H) `-bana` y D9.** Dejar escrito en `2-lengua/morfologia.md` §8 que el
  paralelo taíno de Oliver empuja hacia 'cubierto / extensión' y **no** refuerza
  'cerro'. No reabre D9; impide que alguien lo cite al revés.
- **(I) `-gua` (d21.7).** Añadir `bara-wa` / `bagua` a la campaña como primera
  pista independiente, con la reserva de que el `gua-` taíno de Brinton y Oliver
  es un prefijo y no el sufijo del canon.
- **(J) Tres formantes caquetíos que Oliver declara y el canon no tiene.**
  Oliver cap. 2 p. 148 lista los sufijos toponímicos caquetíos como `-bana`,
  `-coa/-koa`, `-oa`, `-kiva`, `(e)-bo`, `-wa [gua-]`. El canon tiene los dos
  primeros y `-gua`; **`-oa`, `-kiva` y `-bo` no están en ninguna parte** — ni en
  `morfemas.yaml` ni en `TODAS_LAS_REGLAS`—, y el cruce los mide vivos en la
  toponimia: `-oa` **6/78**, `-bo` **5/78**, `-kiva/-quiva` **4/78**
  (`jadacaquiva`, `quiquiba`, `todariquiba`, `yauquiba`) y **0 en taíno** en los
  tres. Es hueco propio, no pregunta taína, y sale barato: la cita está y las
  formas también. ⚠️ Y el `-kiva` tiene una lectura que cierra sola: la glosa de
  fuente de `jadacaquiva` dice *«Quiba en caquetío es pedruzco»*, o sea que el
  «sufijo» de Oliver puede ser el lexema `kiba` 'piedra' en composición — el
  mismo `kiba` del par con el `siba` taíno de (E). Conviene mirarlo con esa
  hipótesis delante antes de declararlo morfema.
- **(K) `auri` 'perro'.** Sigue etiquetada `achagua` aunque Oliver p. 151 la
  declara la voz caquetía para 'perro' y es uno de sus tres pilares. Ya estaba
  anotado en `4-fuentes/oliver-1989-cap2.md` §«Qué falta» desde el 2026-08-03 y
  sigue sin hacer.

---

## 7. Lo que NO se encontró

- **Ni una pareja léxica.** Cero entre el caquetío atestiguado y el taíno, con
  el control no arahuaco dando el mismo cero.
- **Ni una correspondencia fonética taíno~caquetío.** 0 pares parecidos, así que
  0 correspondencias que probar. (El lokono da 5 correspondencias distintas y
  **ninguna con 3 apoyos**: tampoco ahí hay regla, sólo el mejor candidato.)
- **`manicato` no sostiene `ma-`**: Brinton no lo segmenta y el OCR de su
  etimología no es legible — hay que verla en imagen antes de citarla.
- **Ningún formante toponímico compartido** entre las dos onomásticas: `-bana`,
  `-coa`, `-bacoa`, `-oa`, `-bo`, `-ey`, `-ana` y `-kiva` dan **0 de 78** en la
  onomástica taína de Pané, y `-ex`/`-el` dan **0 de 48** en la caquetía.
- **Ninguna atestación taína de `-bana` fuera de `Agüeybana`.** Oliver lo cita
  como antropónimo (p. 148) y el corpus de Pané —78 formas indígenas— no trae
  ni una. El «paralelo» es un nombre.

---

## 8. Lo que vi de paso y merece otra campaña

1. **`gudamuen` 'dos' no se parece a nada arahuaco.** Ni `biama` lokono, ni
   `piama` wayuu, ni `yamosa` taíno, ni `aban`/`biama` kalinago. Es una voz
   atestiguada por Zavala (#148, PMA), es un numeral —el dominio de filiación
   por excelencia— y **no encaja**. O es un error de la compilación de Zavala, o
   es el dato más raro que tiene el caquetío. Merece una minería propia.
2. **Los tres formantes de Oliver que el canon no recogió** (§6.J). Media sesión
   con la cita ya localizada.
3. **El caquetío tiene `-bo` productivo y nadie lo ha glosado**: `borobo`,
   `cumarebo`, `guacurebo`, `jurijurebo`, `turijerebo`. Es el mismo tipo de
   hueco que `-shi/-chi` en `morfemas.yaml`, que ya está declarado como objetivo
   nº 1 de la toponimia insular.

---

## Enlaces

[[oliver-1989-cap2]] · [[brinton-1871]] · [[pane-c1498]] · [[jahn-1927]] ·
[[esteves-1989]] · [[zavala-reyes-2015]] · [[metodo-comparativo]] ·
[[morfologia]] · [[toponimia]]
