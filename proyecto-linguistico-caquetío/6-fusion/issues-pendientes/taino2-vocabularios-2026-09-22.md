# T10 — Los vocabularios antillanos: la lista taína con cadena de custodia

**Segunda campaña del taíno, parcela T10. 2026-09-22.**
Rama `campana/taino2-vocabularios`. PROPUESTA (regla 5): nada de esto toca el
canon.

---

## Lo que de este encargo resultó falso al medirlo

| Lo que decía | Lo medido |
|---|---|
| «Goeje 1939 … en Persée, gratis» | gratis de **leer**, no de descargar: el PDF de Persée está tras un **captcha**, que no se salta. El mismo fichero está abierto en la Biblioteca Digital Curt Nimuendajú, y de ahí salió |
| «pp. 1-128» (Goeje) | **pp. 1-120** |
| «el estudio que junta taíno, kalinago y **lokono**» | `lokono` aparece **0 veces** en Goeje; escribe `Arawak` (29). Misma trampa que Brinton |
| «**Zayas 1914** … en dLOC» | la ficha de dLOC responde 200 y **no sirve el texto**; `zayas`, `lexicografía antillana` y `voces usadas por los aborígenes` dan **0 resultados en archive.org**. NO se consiguió. Y sin embargo es citable: Goeje la apoya con página en cuatro voces (`anaki` p. 33, `anaiboa` p. 32, `anua` p. 52, `manaya` p. 78) |
| «Coll y Toste 1897 … lo que alcances» | se consiguió, y **sin capa de texto** (273 bytes con `pdftotext`). Se guarda el OCR de archive.org, 489 KB, declarado como OCR y no como cita |
| «Granberry y Vescelius 2004 … es la única obra que asigna cada voz a una variedad» | **no es la única.** Bachiller 1883, apéndice (A), publica la lista de Rafinesque con la isla marcada —Cuba, Jamaica, Lucayas— y con un bloque **eyeri** aparte. Y Goeje nombra Macorix, Ciguayo, lucayo y «lengua de Cuba». Granberry sigue haciendo falta, pero ya no partimos de cero |
| (mío) «Bachiller da 5 de 51 claves» | **un cero de la consulta.** Segmenté por un patrón de guion que el OCR mueve. Buscando la palabra suelta: **37 de 47**. Regla 6, tercera vez en el repo |

---

## El veredicto en una frase

**La lista taína del proyecto pasa de 52 voces sin cita a 263 con cadena de
custodia, de las cuales 172 son de clase (i) —atestiguadas por un cronista del
XVI—, y los conceptos comparables con el caquetío atestiguado suben de 4 a 12:
el cruce se puede re-correr y seguirá siendo pequeño, porque el límite ya no es
la lista taína sino que el caquetío atestiguado tiene 190 conceptos y casi
ninguno coincide con lo que los cronistas glosaron.**

---

## Las cifras, y de dónde salen

Todas las emite `6-fusion/scripts/consolidar_taino.py` (con `--check`) sobre
`6-fusion/taino_lista_maestra_2026-09-22.yaml`. Ninguna está escrita a mano.

| Cifra | Valor | De dónde |
|---|---|---|
| voces taínas distintas | **263** | 6 transcripciones unidas por lema, con union-find sobre todas las variantes |
| clase (i) primaria del XVI | **172** | ≥1 cronista del XV-XVI detrás |
| clase (ii) sólo secundaria | **77** | la trae un compilador y ninguno dice de qué cronista sale |
| clase (iii) conjetura moderna → NO ENTRA | **14** | sin cronista y con marca de conjetura |
| con **2 o más cronistas independientes** | **22** | skill §8: cronistas distintos, no obras |
| con variedad o isla declarada | **98** | |
| voces que alguna fuente **saca** del taíno | **22** | `piragua`, `maboya`, `behiko`, `taita`, `baeza`, `tuob`, `kabuya`, `tiburon`, `name`… |
| de las **52 claves taínas del lexicón**, con al menos un cronista | **41** | ayer eran 0 con `procedencia.obra` y ~36 con cita en prosa |
| sin voz en la lista | **7** | y son **exactamente** las 7 reconstruidas desde el lokono |
| conjeturas modernas detectadas entre las 52 | **1** (`maboya`) | su único apoyo es la lista de Rafinesque |
| conceptos del caquetío **atestiguado** | **190** | `CL.VOCABULARIO_BASE`, capa atestiguada |
| comparables con la lista **vieja** | **4** | reproduce el número del cruce del 09-21 |
| comparables con la lista **maestra** | **12** | ⚠️ **es un SUELO**: Goeje glosa en francés y sólo se traducen las glosas de una palabra con una tabla declarada de 46 entradas; lo que no está en la tabla no cuenta |
| los 9 que sólo aporta la lista nueva | alma, bejuco, bosque, cuatro, mar, piedra, sabana, sacerdote, tres | |

---

## 🔴 Lo que más mueve

### 1. La cadena está rota en Brinton, y se puede probar sin salir del repo

El coordinador pasó el dato del agente de la Apologética: Las Casas, *Apologética*
(NBAE 13) p. 177, da los numerales `yamocá`, `canocúm`, `yamoncobre`. Cotejado
contra el texto de Brinton que ya teníamos:

| | Brinton p. 14 (dice copiar Las Casas cap. 204) | Apologética p. 177 | Goeje 1939 p. 17 |
|---|---|---|---|
| 1 | hequeti | — | heketi |
| 2 | **yamosa** | yamocá | yamoka |
| 3 | **cauocum** | canocúm | kanokum |
| 4 | **yaraoucobre** | yamoncobre | yamonko-bre |

**3 de 4 discrepan, y en los tres Goeje coincide con el primario.**

Y hay prueba interna, que no necesita la Apologética: Brinton escribe que el 4
*«evidently formed from yamosa»* — pero **su propia forma `yaraoucobre` no
contiene `yamosa` por ningún lado**, mientras que la forma real `yamoncobre` sí
empieza por `yamo-`. El análisis es correcto y la transcripción no. Esa frase
está en el repo desde el 2026-07-29 y nadie la había puesto a prueba contra sí
misma.

Consecuencia: la clave **`yamosa`** del lexicón viene de la lectura mala; y las
**84 entradas del lexicón que citan a Brinton** quedan bajo sospecha de
transcripción —no de existencia—. La voz existe; la letra hay que verificarla
contra el cronista.

### 2. `macana` tiene atribución explícita del cronista

Las Casas, misma página: «vocablo desta isla y no de la Tierra Firme». Es de las
poquísimas veces que un cronista dice **de dónde es** una voz en vez de qué
significa. Toca `6-fusion/propuesta_macana_etiqueta_2026-09-21.yaml`: si es
antillana por declaración, su presencia en tierra firme es **préstamo**, y
Bachiller p. 239 documenta la vía (Gumilla la registra en el Orinoco, s. XVIII,
con el castellano de por medio). ⚠️ No confundir con `matacán` 'venado'.

### 3. `daca` — tres testimonios y ninguno dice «mano»

Pané (`Dios naboria daca` 'yo soy siervo de Dios'), Goeje p. 17
(`mayani-makana, Juan Desquivel daca` 'no me mates, porque soy Juan de
Esquivel') y Bachiller p. 270 («expresa el ser o la existencia… Las Casas
escribe `daca`, Pané `dacha`»). La entrada del lexicón es
`taíno-reconstruido` y glosa **«mano»**.

### 4. El par atributivo/privativo tiene ahora apoyo taíno

Goeje p. 17 declara `ka-` 'avec, présent' y `ma-` 'sans, absent' con las mismas
correspondencias arahuacas del canon, y hay **siete formas taínas** con `ka-`
(`ka-hoba`, `ka-sabi`, `ka-ona`, `ka-k-ona`, `kasike`, `caçibaxagua`,
`bu-ti-k-ako`) y **cinco** con `ma-` (`m-ahi-te`, `Matinino`, `Macorix`,
`amaiaua`, `mayani`). d21.5 pasa de dos fuentes a tres lenguas de la esfera.

### 5. `gua-` es prefijo de 1ª plural, y eso NO cierra la deuda de `-gua`

Goeje: `T gua-` corresponde a `wa-` 'nosotros', y anota que Pedro Mártir lo
tomaba por el artículo. Está en `gu-aroko-el`, `guamechyna`, `guaoxeri`. ⚠️ El
canon tiene `-gua` **sufijo** locativo con `deuda: sin-procedencia`. Son cosas
distintas. Lo que esto aporta es un **aviso metodológico**: la sonda `gua-/wa-`
del cruce puede estar contando posesivos.

### 6. `cohiba` y `tabako` están al revés en el lexicón

Brinton, Goeje y Bachiller, independientes: `cohiba` es la **planta** y `tabaco`
el **instrumento** (el canuto). Tres apoyos y ninguna relación entre ellos.

### 7. Tres voces del lexicón que las fuentes sacan del taíno

- **`piragua`**: Goeje la pone en el caribe insular y sospecha del español
  *vela*; Rafinesque vía Bachiller la marca **eyeri**; y Goeje avisa aparte de
  que `piragua`, `kanoa` y `hamaka` viajaron a otras lenguas indígenas **por vía
  del español**. Tres manos, ninguna la llama taína. **Es la que peor aguanta de
  las 52.**
- **`maboya`**: Goeje la da como caribe de Honduras (`ma-poya`) y Bachiller la
  publica en la lista **eyeri**. La taína para 'espíritu del muerto' es `hupia`.
- **`bejique`**: Goeje da `behiko` como **caribe insular usado en Haití** y
  `buhuitihu` como el taíno; Bachiller lo da de Cuba y las Lucayas con cita de
  Las Casas *Apol.* p. 436. **Los dos intermediarios discrepan.**

### 8. `taita` — la degradación la firma Bachiller

No está en su lista taína: está en el **apéndice (C)**, el de las voces que
pasan por indígenas y vienen de otras partes. Corrige a Pichardo —que es la
única autoridad detrás de nuestra entrada, vía Brinton— y propone el vascuence
`aita`. Goeje: 0 ocurrencias. Y el propio Pichardo, verificado en su
diccionario, sólo la marca «voz ind.», sin cronista.

### 9. `guabina` sube, y `manigua` no

`guabina` aparece en Bachiller p. 267 dentro de la enumeración de peces de
nombre indio **de Las Casas**: sube de «sin apoyo» a «atestiguada, libro por
localizar». `manigua` sólo aparece en la **sección 3ª** de Bachiller, que es el
cubano del s. XIX: no sube de clase.

### 10. Las 7 reconstruidas dan cero en los dos vocabularios

`acoa`, `aduri`, `agari`, `akcicyaa`, `thigisi`, `wacusi`, `wagulo` —las que
este proyecto generó con `reconstruir_taino()` desde el lokono— **no aparecen ni
en Goeje ni en Bachiller**. Dos vocabularios antillanos independientes. No es
una laguna: es la contraprueba del método.

---

## Lo que NO se encontró

- **`mayani`, `yamosa`/`yamocá` y `abba`/`hequeti` en Bachiller: cero las tres.**
  Los numerales y la negación siguen colgando de la *Apologética* caps. 204 y
  241, **que el repo no tiene** (aunque otro agente de esta campaña sí la leyó).
- **Zayas y Alfonso 1914**: no se consiguió. Ni en archive.org ni en dLOC.
- **Tejera, *Indigenismos***: no se buscó (moderno y probablemente en copyright).
- **La errata de Goeje de 1940**: el enlace de etnolinguistica devuelve HTTP 500.
- **La asignación voz a voz a una variedad**: sólo 98 de 263 la tienen, y casi
  todas por la lista de Rafinesque, que es de fiar a medias. Granberry y
  Vescelius 2004 **sigue siendo la pieza que falta** (en copyright: no se
  descarga; se compra, ISBN 9780817351236, o préstamo interbibliotecario).
- **El kalinago de Goeje** (pp. 31-110, más de la mitad de la obra, con habla de
  hombres y de mujeres): sin leer. Las 23 entradas kalinago del lexicón siguen
  sin tocar.

---

## Opciones para Miguel

Todas son propuestas. Las de nivel de entrada están detalladas en
`taino_goeje_1939.yaml` §propuesta (g1-g7) y
`taino_bachiller_morales_1883.yaml` §propuesta (b1-b5).

### A — La tanda de etiqueta (8 entradas, no toca el motor)

Aplicar lo que dos o tres fuentes independientes sostienen: `taita` fuera del
taíno; `piragua` y `maboya` a `kalinago`; `bejique` con la duda anotada;
`cohiba`/`tabako` con las glosas intercambiadas; `daca` con glosa 'yo' y capa
`taíno`; `yamosa` → `yamocá`; `guabina` con la cita de Las Casas.
**Coste**: mueve `prestamos_de_esfera` sólo si alguna llega al prompt —
`piragua` y `maboya` no están entre las 43 candidatas de `[Voces de fuera]`,
así que el motor no se entera. **Ganancia**: 8 entradas dejan de mentir.

### B — Sólo lo que tiene tres apoyos (3 entradas)

`taita`, `cohiba`/`tabako`, `daca`. Es la versión conservadora: se mueve
únicamente lo que tres fuentes independientes dicen igual.

### C — Nada de entradas; sólo la lista maestra al canon de datos

Dejar el lexicón como está y usar `taino_lista_maestra_2026-09-22.yaml` como
fuente de `procedencia.obra` para las 41 claves que ya tienen cronista. Es lo
que más deuda cierra con menos riesgo: la regla 8 dice que citar es una clave
foránea, y hoy esas 41 no citan a nadie.

### D — Re-correr el cruce con la lista nueva

`cruce_taino_caquetio.py` lee `curiana_lexicon`, no la lista maestra, así que
**hoy no se puede**: haría falta que la lista maestra entre al lexicón (opción
A o C) o que el cruce aprenda a leer un YAML. Con 12 conceptos comparables en
vez de 4, el cruce sigue siendo pequeño pero deja de medir sólo productos: entra
`piedra` (`kiba` ~ `siba`), `mar`, `bosque`, `sabana`, `cuatro`, `tres`.

### Recomendación del minador

**C primero, luego A.** Poner las 41 citas es cerrar una deuda declarada sin
mover ninguna glosa ni ninguna capa, y deja el terreno listo para que A se
aplique con la evidencia ya enganchada a cada entrada. D no antes de C: re-correr
el cruce sobre la lista vieja sería medir otra vez el mismo 4.

Y una cosa aparte, que no es una opción sino un aviso: **si Brinton falla en 3
de 4 numerales donde se le puede cotejar, las 84 entradas del lexicón que lo
citan necesitan una pasada de verificación de FORMA contra el cronista.** Eso es
una campaña, no una tanda.

---

## Lo que vi de paso y no es de mi parcela

- **Goeje cita dos veces un «dialecte de Aruba»** (`luaidanga` 'calabaza',
  `hanuhana` 'hormiga') sin decir de dónde lo saca. Aruba está en la Kaketiana.
  Hay que buscarlo en su bibliografía y cruzarlo con `Gatschet_1885_Aruba_texto.txt`
  y con van Buurt, que ya están en el repo. Si no es Gatschet, hay una fuente
  arubana que el proyecto no conoce.
- **Goeje deja 46 plantas y 12 animales sin identificar y manda buscarlos en
  Oviedo**, que sí tenemos. Ahí caerían `cobo`, `guabina` y `manigua`.
- **Bachiller retradujo la Relación de Pané** (sección 2.1, pp. 165-184) y la
  confrontó con otras traducciones. Cotejarla con `taino_pane_c1498.yaml` es
  barato y puede mover glosas.
- **Pichardo tiene 17 ocurrencias de `manigua`, 12 de `guabina` y 31 de `cayo`**
  sin minar: es el material para separar el tainismo panhispánico de la voz
  antillana atestiguada.
- `duho`/`dulios` y `naitano`/`nitainos` siguen partidos en la lista maestra
  porque sus variantes no comparten lema normalizado. Residuo declarado: son
  2 voces de más sobre 263.
