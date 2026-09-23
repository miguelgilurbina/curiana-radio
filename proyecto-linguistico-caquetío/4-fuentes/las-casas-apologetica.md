---
tipo: fuente
obra: "Apologética historia sumaria (Historiadores de Indias, tomo I)"
autor: "Casas, Bartolomé de las"
anio: "1909 [c. 1527-1559]"
genero: cronica
local: "fuentes_caquetios/LasCasas_Apologetica_NBAE13_Serrano_1909.pdf"
paginas: 725
capa_texto: si
estado_minado: minado
cobertura: "caps. X-XIII, XLIV, LXV, LXX, CXX-CXXI, CXXX, CLXVI-CLXVII, CXCVI-CXCIX, CCIII-CCV y CCXLI pasaje a pasaje; el tomo entero por patrón"
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-22
aliases: ["Las Casas Apologética", "Apologética historia sumaria", "NBAE 13", "Historiadores de Indias tomo I"]
---

# Las Casas 1909 [c. 1527-1559] — *Apologética historia sumaria*

> Edición de **Manuel Serrano y Sanz**, *Nueva Biblioteca de Autores
> Españoles* **13** = *Historiadores de Indias*, tomo I. Madrid,
> Bailly-Baillière é Hijos, 1909. **Completa**: caps. I-CCLXVII más el
> Epílogo, 696 páginas impresas de cuerpo.

## Qué es

La etnografía, no la denuncia. Donde la *Historia de las Indias*
([[las-casas-1875]]) narra, ésta **describe**: religión, gobierno,
matrimonio, herencia, medicina, juego, comida, y —esto es lo que la
hace única— **cómo sonaba la lengua**. Las Casas marca el acento de la
voz indígena sistemáticamente: 97 formas distintas llevan «la última
sílaba luenga», «la penúltima breve», «la letra *e* luenga».
`penúltima` sale **38** veces aquí y **0** en el tomo I de la
*Historia*.

Era la fuente primaria taína que más falta hacía y no estaba en el
repo. La [[#Sesión 6 — segunda campaña del taíno, 2026-09-22 parcela T9|sesión de abajo]]
la incorporó.

## Descarga (autorizada por Miguel, 2026-09-22)

| | |
|---|---|
| **URL** | https://archive.org/download/historiadoresdei01serr/historiadoresdei01serr.pdf |
| **Ítem** | `historiadoresdei01serr` — escaneado por la University of Toronto, 2011 |
| **Fecha** | 2026-09-22 |
| **Derechos** | **Dominio público.** Obra de 1909; autor del texto muerto en 1566, editor (Serrano y Sanz, 1868-1932) muerto hace más de 70 años. archive.org no declara licencia porque no hace falta |
| **Tamaño** | 91.938.944 bytes (91,94 MB) — **por debajo de los 95 MB, así que se commitea** |
| **sha256** | `06fc0fdb5e3c116fa6c97521f3aa18700fea8a4dddea0c39ef25fb94a4800d3f` |
| **En el repo** | `fuentes_caquetios/LasCasas_Apologetica_NBAE13_Serrano_1909.pdf` y su extracción `...1909.txt` (3,6 MB) |

También se descargó, y se usó para cotejar, el `djvu.txt` del mismo
ítem (4,2 MB) y **ocho páginas en imagen** por
`https://archive.org/download/historiadoresdei01serr/page/n<HOJA>.jpg`
(hoja = página pdf − 1), a 2412×3631 px. Las imágenes **no** se
commitean: se regeneran con esa URL.

## Estado técnico (verificado 2026-09-22)

- **725 páginas pdf**, capa de texto **sí** (ABBYY, 3,48 MB en plano).
- **El desfase pdf ↔ impresa es CONSTANTE: `impresa = pdf − 14`.**
  Medido sobre las 388 páginas donde el número impreso de la cabecera se
  lee: **367 dan exactamente 14** y las 21 restantes son ruido de OCR
  (−36, −486, +104…), no otro desfase. Es la diferencia práctica grande
  con [[las-casas-1875]], donde el desfase iba de +8 a +69 y la página
  impresa era interpolación: **aquí toda cita lleva página impresa
  exacta**.
- El **índice general original** está en pdf 711-725 (impresas 697-704);
  es tabla a dos columnas y necesita `-layout`.

### ⚠️ Tres extractores, tres textos — y ninguno basta

| voz | pdftotext | pdftotext -layout | djvu.txt |
|---|---|---|---|
| `behique` | 6 | 4 | 4 |
| **`guaoxeri`** | **0** | **0** | **1** |
| `dujo` | 21 | 21 | 24 |
| `macorix` | 8 | 8 | 9 |
| `opia` | 85 | 84 | 84 |

**`guaoxerí` —uno de los tres tratamientos de rango, de lo más valioso
que da la obra— sólo existe en el djvu y en la imagen.** Con un
extractor, falta.

Y hay una trampa peor que la de CLAUDE.md («tablas a dos columnas»):
el cuerpo va a dos columnas y pdftotext **entrelaza carácter a carácter
las líneas de columnas vecinas** en las zonas apretadas. `-layout` NO
lo arregla. Ejemplo real de la p. 516, donde estaban las glosas de
`baharí` y `matunherí`:

```
elááloslmoasByaoshreañroírseesñloordlelqatumíeatlbulaonp;rdiemceeir--a
```

Se resolvió **leyendo la imagen**. Ocho páginas se leyeron así: 177,
446, 447, 516, 521, 538 (×2) y 534.

## Sesión 6 — segunda campaña del taíno, 2026-09-22 (parcela T9)

Propuesta completa en `6-fusion/taino2_las_casas_apologetica.yaml`;
la cola de decisión en
`6-fusion/issues-pendientes/taino2-apologetica-2026-09-22.md`;
las cifras las emite `6-fusion/scripts/medir_taino2_apologetica.py`.

### Qué se preguntó y qué dio

| Pregunta | Resultado |
|---|---|
| voces de la lengua de La Española, con glosa, página y atribución | **35 entradas** (`lexico.lx.01`-`lx.35`), todas con página impresa exacta |
| qué dice de la lengua misma | **8 pasajes** (`metalinguistico.ml.01`-`ml.08`) |
| instituciones que el canon caquetío también tiene | **9 fichas** (`instituciones.i01`-`i09`) |
| contacto islas ↔ Tierra Firme | **6 fichas** (`contacto.co.01`-`co.06`) |
| cuántas de las 52 entradas taínas del lexicón reciben cita primaria | **24 la reciben limpia** (21 voces distintas), **3 con conflicto**, **25 siguen sin cita** |
| voces nuevas que la obra da y el lexicón no tiene | **17** |

### Lo que corrige a lo que se creía

- **La tripartición de lenguas de La Española NO es «taíno / macorix /
  ciguayo».** El pasaje nítido (cap. CXCVII, p. 517) dice: *«Tres
  lenguas habia en esta Isla distintas, que la una á la otra no se
  entendía: la una era de la gente que llamábamos el Macoríx de abajo,
  y la otra de los vecinos del Macoríx de arriba […] la otra lengua fué
  la universal de toda la tierra»*. **Los dos macorix y la universal.**
  El ciguayo no está en la lista. Esto es lo que [[las-casas-1875]]
  dejaba en suspenso («no me acuerdo si diferian estos en la lengua»):
  la versión nítida existe y no dice lo que la bibliografía repite.
- **`areíto` no aparece ni una vez en toda la obra.** 0 en los tres
  extractores y cuatro grafías del XVI. La **institución** está entera
  (pp. 537-538: trescientos hombres brazo con brazo, atabales de madera
  sin cuero, *«la letra de sus cantos era referir cosas antiguas»*), y
  la palabra no. Es el caso inverso al de `macana` en el tomo I de la
  *Historia*, donde estaba el nombre y no la cosa.
- **Las Casas nunca llama «taínos» a los taínos.** El etnónimo no está.
- **Los numerales de Brinton no son los de esta edición.** Brinton cita
  «Apol. cap. 204» para *1 hequeti, 2 yamosa, 3 cauocum, 4 yaraoucobre*;
  el capítulo es correcto (p. 538) pero NBAE 13 lee **`hequetí`,
  `yamocá`, `canocúm`, `yamoncobre`** — verificado en imagen. Tres de
  cuatro no coinciden, y nuestro lexicón tiene `yamosa` por esa vía.
- **Las Casas descalifica en parte a su propio informante.** De fray
  Ramón Pané dice que de las tres lenguas *«no supo sino la una de una
  chica provincia […] y aquélla no perfectamente, y de la universal
  supo no mucho»* (p. 321-322), y que *«no hablaba del todo bien nuestra
  castellana lengua, como fuese catalán de nación»* (p. 447). Eso le
  pone techo a `6-fusion/taino_pane_c1498.yaml`.
- **`macana` es «vocablo desta isla y no de la Tierra Firme»**, dicho
  con todas las letras (p. 177, verificado en imagen), junto con
  `cotaras`, `bixa`, `maiz` y `maguey`. Entra como tercer dato en la
  campaña abierta de `macana-etiqueta-2026-09-21.md`.
- **`daca` significa 'yo', no 'mano'** (p. 447). Nuestro `daca` 'mano'
  es reconstrucción desde el lokono; el atestiguado es otro. Conflicto
  de glosa, no de forma.

### Lo más grande para la esfera

Cap. CXX, p. 321. Las Casas declara **un área cultural única** que va
de las Antillas a la costa continental: *«las gentes desta Española, y
la de Cuba […] y todas las islas de los Lucayos […] desde cerca de la
Tierra Firme que se dice la Florida, hasta la punta de Paria […] y
también por la costa de la mar las gentes de la Tierra Firme, por
aquella ribera de Paria, y todo lo de allí abajo hasta Veragua, cuasi
toda era una manera de religión»*.

El tramo **Paria → Veragua contiene la Kaketiana**. No dice «los
caquetíos» ni dice que sea la misma gente o la misma lengua: dice «una
manera de religión», y lo dice con interés apologético. Pero es una
afirmación de **esfera hecha por la fuente**, no por nosotros, y es el
marco de [[esfera-de-interaccion]] escrito en 1559.

### Qué NO dio (medido, con las grafías del XVI)

- **`guatiao` = 0.** Con `guaitiao`, `datihao`, «trocar nombres»,
  «tomar el nombre». El intercambio ritual de nombres —que el encargo
  pedía como paralelo principal— **no está en la Apologética**. Quien
  lo use tiene que apoyarse en Oviedo y sólo en Oviedo.
- **El origen del guanín = 0.** Las cuatro ocurrencias están en la
  misma página (521) y hablan del uso y del olor, nunca de dónde venía.
  La cadena guanín → Tierra Firme, que la arqueología usa, no está aquí.
- **Navegación de altura = 0.** Hay canoas de ochenta y cien personas,
  con su material y sus remos, y ni una travesía entre islas ni al
  continente.
- **Los caribes como intermediarios = 0.** Salen sólo como razzia
  («infestan y salen de sus proprias islas y tierras por hacer guerra á
  los de otras partes, islas y Tierra Firme», p. 539). Ni comercio, ni
  transporte, ni trueque.
- **`maboya` = 0.** Lo que hay es `hupía` 'el ánima del hombre'
  (p. 535), que no es un espíritu maligno.
- **`atabey` = 0** — la forma de esta edición es **`Atabex`** (p. 321).
  Un cero que medía la consulta, no la fuente.
- Sin rastro alguno: `akcicyaa`, `cai`, `manigua`, `mayani`, `papaya`,
  `thigisi`, `wacusi`, `wagulo`. Y dan ocurrencias que **no son la
  voz**: `abba`, `acoa`, `aduri`, `agari`, `cobo`, `taita`, `cayo`
  (ruido), `tuna` (un río), `caiman` (epígrafe del editor moderno),
  `piragua` (Tierra Firme, p. 645).

## Qué falta

- **Cotejar con la edición de O'Gorman (1967)**, que no tenemos y está
  en copyright. Es la única manera de decidir si las formas de Brinton
  (`yamosa`, `cauocum`, `yaraoucobre`, `dujo`) vienen de otro testimonio
  del manuscrito o de un salto en la cadena. Hasta entonces, los
  conflictos `c02` quedan abiertos y **no se reescribe nada**.
- Los ~180 capítulos de erudición clásica y los bloques de Nueva España
  y del Perú **no se leyeron pasaje a pasaje** (~75 % de la obra). No
  alimentan esta parcela; sí alimentarían una de «cómo compara Las
  Casas», que nadie ha pedido.
- Regla que deja, y es la contraria a la de [[las-casas-1875]]: *una
  fuente que rinde para una pregunta puede rendir DIEZ VECES MÁS para
  la misma pregunta si es la obra correcta del mismo autor.* El tomo I
  de la *Historia* dio 26 voces y 10 pasajes; la *Apologética* da 35
  voces con página exacta, 8 pasajes, 9 instituciones y 6 fichas de
  contacto. Antes de dar por agotado a un cronista, mirar **qué obra
  suya** se le preguntó.

---

## Bitácora: manatí, tabacos y cohoba (2026-09-23, cc.7)

Tres pasajes, ✅ vistos en imagen (impresa = pdf − 14 con el pdf contado desde
1):

- **p. 27** (cap. X): «á la boca de los rios, entre el agua salada y dulce,
  los que llamaban los indios *manatíes*, la penúltima sílaba luenga». Es la
  cita de Zayas t. II p. 178, y contradice a Oviedo t. I p. 434, que dice que
  el nombre lo pusieron los cristianos.
- **p. 181**: el rollo de hojas, «y estos mosquetes llamaban *tabacos*, la
  media sílaba luenga». Es el rollo encendido, no la yerba de dentro.
- **p. 445**: «Estos polvos y estas cerimonias ó actos se llamaban *cohoba*,
  la media sílaba luenga, en su lenguaje»; y **p. 446**, «Yo los vi algunas
  veces celebrar su cohoba». La cohoba es el polvo y el rito, no el tabaco.

Detalle: `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml` §zayas.
