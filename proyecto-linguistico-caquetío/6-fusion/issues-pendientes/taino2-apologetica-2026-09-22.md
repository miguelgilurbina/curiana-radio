# La *Apologética* de Las Casas: 24 entradas del lexicón reciben cita, 3 entran en conflicto y el `guatiao` no existe

**Segunda campaña del taíno, parcela T9** · rama `campana/taino2-apologetica` ·
datos y citas en `6-fusion/taino2_las_casas_apologetica.yaml` · cifras de
`6-fusion/scripts/medir_taino2_apologetica.py` · bitácora en
`4-fuentes/las-casas-apologetica.md`.

Regla 5: esto **propone**. No se tocó `curiana_lexicon.py`, ni `2-lengua/*`,
ni `3-mundo/corpus/`, ni `6-fusion/BANDEJA.md`.

---

## 0. Lo que de mi propio encargo resultó falso al medirlo

1. **`6-fusion/decisiones_campanas_2026-09-21.yaml` §dc.4 no existe.** El
   encargo me mandó leerlo como parte de lo que dejó la primera campaña.
   `ls 6-fusion/decisiones_*` da once ficheros y ninguno se llama así; el de
   esa fecha es `decisiones_tanda_2026-09-21.yaml` y un grep insensible por
   `taino|taíno|apologet` sobre él da **0**. La cola de decisión de la campaña
   del taíno vive en `6-fusion/issues-pendientes/taino-*-2026-09-21.md` (cinco
   ficheros), que sí leí. **Si alguien escribió ese §dc.4, no llegó a main.**
2. **El desfase pdf ↔ impresa no hay que interpolarlo.** El encargo lo
   planteaba como en la parcela T2, donde iba de +8 a +69. Aquí es
   **constante**: `impresa = pdf − 14`, en 367 de las 388 páginas donde el
   número impreso se lee. Toda cita de esta parcela lleva página impresa
   **exacta**.
3. **`areíto` no está en la obra.** El encargo lo pedía como una de las cinco
   instituciones a comparar. 0 ocurrencias, tres extractores, cuatro grafías.
   La cosa está y el nombre no.
4. **El `guatiao` tampoco.** Era el paralelo institucional que el encargo
   ponía primero. 0, con `guaitiao`, `datihao` y tres paráfrasis.
5. **La sucesión matrilineal sí está, pero no donde la busqué.** Un grep por
   `sobrino` sobre La Española da 0 y **es la consulta**: Las Casas escribe
   «no los hijos de los señores, sino los de sus hermanas sucedían en sus
   estados» (p. 521). Salió leyendo el capítulo entero.

---

## 1. Veredicto, en una frase

**La *Apologética* es la fuente taína más rentable que ha entrado al repo —
24 de las 52 entradas taínas del lexicón pasan de no citar a nadie a tener
cita con página impresa exacta, y de paso trae la única frase taína completa
del corpus, los tres tratamientos de rango y un área cultural declarada que
llega hasta Veragua— pero desmiente tres cosas que el proyecto daba por
buenas: la tripartición de lenguas, los numerales que tenemos vía Brinton, y
la glosa de `daca`.**

---

## 2. Las cifras, y de dónde salen

Todas las emite `python 6-fusion/scripts/medir_taino2_apologetica.py`.

| Cifra | Valor | De dónde |
|---|---|---|
| páginas pdf | 725 | `--desfase` |
| desfase constante | `impresa = pdf − 14`, 367 de 388 | `--desfase` |
| voces con marca prosódica | **97 formas distintas**, 108 ocurrencias | `--prosodia` (es un SUELO: la red pierde los casos de columna zipeada) |
| `penúltima` en la obra | **38** — en la *Historia* tomo I era **0** | `--ortografia` |
| `areito` / `guatiao` / `taino` | **0 / 0 / 0** | `--ortografia` |
| entradas del lexicón con cita limpia | **24** de 52 (21 voces distintas) | `--cobertura` |
| con cita pero en conflicto | **3** | `--cobertura` |
| siguen sin cita primaria | **25** | `--cobertura` |
| voces nuevas que el lexicón no tiene | **17** | `taino2_las_casas_apologetica.yaml` §veredicto |

Entradas del YAML: 35 de léxico, 8 metalingüísticas, 9 de institución, 6 de
contacto, 6 de conflicto, 8 de negativo verificado.

---

## 3. Lo que NO encontré (regla 6: cada cero verificado con grafías del XVI)

- **`guatiao`, `guaitiao`, `datihao`, «trocar nombres», «tomar el nombre» = 0.**
  El intercambio ritual de nombres, que en Oviedo es `datihao` «el que, como
  yo, se nombra», **no está en la etnografía taína más detallada del XVI**.
  Eso no lo niega, pero quien apoye el paralelo caquetío en el guatiao se
  apoya en Oviedo y sólo en Oviedo.
- **El origen del guanín = 0.** Cuatro ocurrencias, todas en la p. 521, todas
  sobre el uso y el olor («que ellos olian»). La cadena guanín → Tierra Firme
  no está aquí.
- **Canoas de altura = 0.** Hay canoas de ochenta y cien personas con su
  material y sus remos; no hay una sola travesía.
- **Caribes como intermediarios = 0.** Sólo razzia, y explícitamente sobre
  «islas y Tierra Firme» (p. 539).
- **`maboya` = 0** (lo que hay es `hupía` 'el ánima del hombre', p. 535).
  **`atabey` = 0** (la forma es `Atabex`, p. 321). **`cohiba` = 0** (lo que hay
  es `cohoba` y `tabacos`, que son dos cosas distintas).
- Sin rastro: `akcicyaa`, `cai`, `manigua`, `mayani`, `papaya`, `thigisi`,
  `wacusi`, `wagulo`. Con ocurrencias que **no son la voz**: `abba`, `acoa`,
  `aduri`, `agari`, `cobo`, `taita`, `cayo`, `tuna` (un río), `caiman`
  (epígrafe del editor moderno), `piragua` (Tierra Firme).

---

## 4. Cobertura real

**Leído pasaje a pasaje: 11 bloques de capítulos, ~55 páginas impresas de 696
(≈ 8 %).** Son los que el encargo pedía: caps. X-XIII (comida, casa), XLIV
(esclavos, batey-plaza), LXV (los «vocablos desta isla»), LXX (tabacos),
CXX-CXXI (religión, cemíes, behiques, las tres lenguas), CXXX (el caney),
CLXVI-CLXVII (cohoba, ayuno, naboría daca), CXCVI-CXCIX (los cinco reyes, los
tratamientos, las tres lenguas, matrimonio, herencia, çibas, guanín),
CCIII-CCV (hupía, cura por soplo, bailes, batey, numerales, caribes) y CCXLI
(coincidencias de lenguas, herencia en Panamá).

**Barrido por patrón sobre las 725 páginas:** 107 bloques de prosodia, 108
ocurrencias de voz-con-acento, 180 líneas de contexto de trece términos
clave, y las 52 claves del lexicón con grafías declaradas.

**NO leído:** los ~180 capítulos de erudición clásica (Grecia, Roma, Egipto,
la India) y el grueso de Nueva España y el Perú — ≈ 75 % de la obra. No
alimentan esta parcela. 169 de los 267 capítulos se localizaron por cabecera;
los otros 98 se ubican por el desfase constante, que basta.

---

## 5. Lo que hay que decidir — opciones con letras

### D1. `daca`: el lexicón dice 'mano', Las Casas dice 'yo'

El lexicón trae `daca` 'mano', `taíno-reconstruido` desde el lokono `daka`.
Las Casas, p. 447, en la única frase taína completa que hay: *«Dios naboría
daca» […] Naboría queria decir sirviente ó criado, y **daca quiere decir yo**.*
Las glosas no coinciden, así que no es un caso de la política «la atestiguada
manda» (que exige glosa idéntica): es el caso de al lado.

- **(A)** Corregir la glosa de `daca` a 'yo' y volverla `taíno` atestiguado con
  esta cita. Coste: `daca` está en `VOCABULARIO_BASE` como voz de cuerpo y el
  motor la enseña; cambiar su glosa mueve canon y hay que medirlo.
- **(B)** Dejar `daca` 'mano' como reconstrucción y **añadir** `daca` 'yo' como
  entrada taína atestiguada aparte. Coste: homógrafos en el lexicón, que ya ha
  dado problemas (`biro-bana`/`kali-bana`, `kasi`/`kashi`).
- **(C)** Archivar `daca` 'mano' en `FUERA_DEL_HABLA` —es una reconstrucción
  que el dato atestiguado contradice— y quedarse sólo con 'yo'.
- **(D)** No tocar nada y anotar el conflicto en `notas`.

**Recomiendo (D) ahora y (C) después**, y en ese orden: la entrada 'mano' no
tiene cita y la 'yo' sí, pero mover una clave de `VOCABULARIO_BASE` es corte de
serie y esta parcela no ha medido su coste.

### D2. Los numerales: Brinton no lee lo que lee NBAE 13

| | Brinton 1871 (en el repo) | NBAE 13 p. 538 (verificado en imagen) |
|---|---|---|
| 1 | hequeti | **hequetí** ✅ |
| 2 | **yamosa** (está en el lexicón) | **yamocá** ❌ |
| 3 | cauocum | **canocúm** ❌ |
| 4 | yaraoucobre | **yamoncobre** ❌ |

- **(A)** Cambiar `yamosa` → `yamocá` con esta cita.
- **(B)** Dejar `yamosa` y anotar en `notas` que NBAE 13 lee otra forma, con
  página, hasta poder cotejar con O'Gorman 1967.
- **(C)** Archivar `yamosa` por forma no verificable.

**Recomiendo (B).** Brinton pudo leer otro testimonio del manuscrito y no
tenemos cómo saberlo: la edición moderna está en copyright. Cambiar una forma
por otra sin poder cotejar es sustituir una incertidumbre por otra.

### D3. `macana` — dato nuevo para una campaña abierta

`macana-etiqueta-2026-09-21.md` midió que el apoyo achagua **no existe** (las
tres formas de Neira y Ribero significan 'dormidera', 'mazorca de maíz' e
'indecible') y que la cita que la sostiene es de otra glosa. Hoy entra un
tercer dato, y es de signo contrario a la etiqueta actual
(`caquetío-reconstruido`):

> «Estos vocablos *cotaras*, **macanas**, *bixa*, y *maiz*, y *maguey*, fueron
> vocablos desta isla y no de la Tierra Firme, porque por otros vocablos allá
> estas cosas llaman.» — cap. LXV, **p. 177**, verificado en imagen.

- **(A)** Re-etiquetar `macana` como préstamo de la **esfera** (taíno
  atestiguado, cita Las Casas p. 177), no como raíz caquetía reconstruida.
- **(B)** Llevar la cita al issue de macana y decidir las tres piezas juntas.
- **(C)** No tocar.

**Recomiendo (B).** La decisión de macana ya está abierta con dos datos; éste
es el tercero y el más directo, pero es una sola frase de un cronista que
escribe desde La Española y compara con «la Tierra Firme» de Panamá y el Perú,
no con Coro. Merece la decisión completa, no un parche.

### D4. Las 17 voces nuevas: ¿entran o no?

`Guaoxerí`, `Baharí`, `Matunherí`, `exbuneyes`, `cohoba`, `Vaybrama`,
`Yocahu Yagua Maorocotí`, `Atabex`, `Guaca`, `Yocahuguama`, `hupía`,
`taguaguas`, `çibas`, `batea`, `hequetí`, `canocúm`, `yamoncobre`.

- **(A)** Ninguna. Son comparanda taína y el lexicón ya tiene un 80 % de
  comparanda (CLAUDE.md: «el 80% del lexicón no es caquetío»).
- **(B)** Sólo las tres de **registro** (`Guaoxerí`, `Baharí`, `Matunherí`),
  porque el caquetío ya tiene esa categoría viva con `kudanga`/`kuté` (d21.10)
  y no tiene con qué compararla.
- **(C)** Todas, con `fuente: taíno` y cita.

**Recomiendo (B).** Es la única de las tres que añade una **categoría** que el
canon necesita y no tiene comparanda: una escala de tratamiento de tres grados,
atestiguada, con acento y con la traducción del propio cronista. Las otras
catorce son léxico antillano que no le hace falta a nadie hoy.

### D5. `areíto`: la entrada existe y su fuente no la trae

`areito` está en el lexicón como voz taína glosada «danza ritual narrativa,
celebración colectiva». La glosa es **exactamente** lo que Las Casas describe
(«la letra de sus cantos era referir cosas antiguas», p. 538). La forma no
aparece en 725 páginas.

- **(A)** Dejarla y declarar `deuda: sin-procedencia` (regla 8).
- **(B)** Buscar su cita en Oviedo, que sí usa la palabra — hay ya
  `6-fusion/taino_oviedo_valdes_1851.yaml` de la primera campaña.
- **(C)** Citar la **descripción** de Las Casas p. 537-538 para la glosa y
  dejar la forma sin cita, diciéndolo.

**Recomiendo (B) y, mientras tanto, (C).** La glosa queda sostenida hoy y la
forma espera a quien mine Oviedo por esa palabra concreta.

### D6. `caney` — un adjetivo sin fuente

Nuestra glosa dice «caney, bohío **rectangular** del cacique». Las Casas dice
«caney era la casa del señor principal» y declara que **nunca preguntó qué
significaba el vocablo** (p. 345). «Rectangular» no está en la fuente.

- **(A)** Añadir la cita y marcar «rectangular» como `deuda: sin-procedencia`.
- **(B)** Quitar «rectangular».
- **(C)** Buscar de dónde salió antes de tocarla.

**Recomiendo (A).** Regla 8: el hueco se admite, callarlo no.

---

## 6. Lo que vi de paso y no me tocaba

- **Las Casas descalifica a Pané.** De fray Ramón dice que de las tres lenguas
  «no supo sino la una de una chica provincia […] y aquélla no perfectamente,
  y de la universal supo no mucho» (pp. 321-322), y que «no hablaba del todo
  bien nuestra castellana lengua, como fuese catalán de nación» (p. 447).
  Esto le pone un techo a `6-fusion/taino_pane_c1498.yaml`, que es de la
  primera campaña, y debería escribirse en `4-fuentes/pane-c1498.md`. No lo
  hice: no es mi parcela.
- **Prestigio dialectal declarado en 1559.** Xaraguá hablaba «más delgada y de
  mejores y suaves vocablos polida» y «aquel reino de Xaraguá era la corte
  desta Isla» (p. 516). Es el mecanismo que `curiana_social.prestigio_de()`
  pondera y que `DISENO_KOINE` §4 quiere ver emerger, documentado en la esfera.
- **Una tipología de guerra en tres causas** (p. 520): cazar en términos
  ajenos, pescar en ríos ajenos, y una alianza matrimonial rota. Dos de tres
  son territorio de subsistencia. Si el motor tuviera que generar un conflicto
  entre nodos, ésta es la tipología documentada más cercana.
- **Un foráneo que llega de otra isla y acaba siendo rey**: Caonabó «era de
  nación Lucayo, natural de las islas de los Lucayos, que se pasó dellas acá,
  y por ser varón en las guerras y en la paz señalado, llegó á ser rey»
  (p. 515), y se casó con la hermana del rey de Xaraguá. Precedente para el
  elenco de la era 2.
- **El canto de trabajo**: «Cuando se juntaban munchas mujeres á rallar las
  raíces de que hacian el pan caçabí, cantaban cierto canto que tenia muy buena
  sonada» (p. 538). Un género aparte del baile, y con oficio.
- **Las Casas hace, en 1559, lo que la skill §2 prohíbe** — enumerar parecidos
  de forma entre lenguas sin parentesco (`umbra`, `michi`, `homo`, `batea` /
  Batea de Cataluña, p. 633) — **y lo hace para desmontarlos**. Es un
  precedente metodológico citable.
