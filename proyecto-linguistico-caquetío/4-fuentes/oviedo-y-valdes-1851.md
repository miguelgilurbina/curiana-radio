---
tipo: fuente
obra: "Historia general y natural de las Indias, vol. I"
autor: "Fernández de Oviedo y Valdés, Gonzalo"
anio: "1851 [s. XVI]"
genero: cronica
publicacion: "Madrid, Imprenta de la Real Academia de la Historia, 1851. Primera parte (libros I-XIX), ed. José Amador de los Ríos, cotejada con el códice original"
local:
  - "fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1_completo.pdf"
  - "fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1.pdf"
paginas: "Cuerpo: impresas 1-614 (libros I-XIX); índice general 615-648. Copia íntegra (`_completo`): 776 pdf, desfase medido en `6-fusion/oviedo_restante_2026-09-22.yaml` → `meta.sondas_medidas.desfase_tomo_I_copia_integra`. Copia truncada: 766 pdf, impresa = pdf − 118 (− 117 hacia la 473)"
capa_texto: si
estado_minado: minada-parcial
cobertura: "medida, no escrita a mano. T1 (voces taínas, 2026-09-21) y T7 (guanín): `6-fusion/taino_oviedo_valdes_1851.yaml` → `meta.cobertura` y `meta.libros_leidos` (`medir_taino_oviedo.py --check`). M3 (2026-09-22: libro XIX entero, historia natural XII-XIV, las frutas de Venezuela del VIII, VI y XI, el intercambio de nombres del XVI): `6-fusion/oviedo_restante_2026-09-22.yaml` → `meta.cobertura`, `meta.libros_leidos` y `meta.sondas_medidas` (`medir_oviedo_restante.py --check`)"
acceso: "Dos copias. La íntegra, del ítem de Internet Archive de la Biblioteca Ludwig von Mises (UFM), la misma colección de los tomos II-IV, `_completo.pdf`, se descargó el 2026-09-22 (https://archive.org/details/historiageneral00fernguat, dominio público — NOT IN COPYRIGHT; 55.449.811 B; sha1 e90c436186f5afd875a67078b11a6631875f09be = el del ítem; sha256 02e88f2beffea91494f34e48e8bbe294a8d46626bf8c2d0383accf9c9be2369a; commiteada, < 95 MB): pymupdf la abre sin reparar y renderiza TODAS las páginas. La vieja, de origen no documentado, está truncada (sin imagen desde la impresa 155), tiene otra paginación de PDF y otra capa OCR (lee `dalihao` donde la íntegra lee `datihao`); se conserva porque T1 cita su paginación. Los tomos II-IV: ver [[oviedo-y-valdes-1852-1855]]"
prioridad: alta
tareas: [F9]
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["Oviedo y Valdés", "Oviedo 1851", "Historia general y natural", "Oviedo vol. I"]
---

# Oviedo y Valdés — *Historia general y natural de las Indias*, vol. I

## 🔴 Esta nota decía que la obra no se podía leer. Era falso

Hasta el 2026-09-21 esta ficha daba el PDF por **corrupto** («`pdftotext`
extrae 0 caracteres», «no procesable con las herramientas actuales») y además
por **el volumen equivocado**, y de ahí salía la frase «la deuda documental más
grande del proyecto».

Las dos cosas son falsas, medidas el 2026-09-21:

| | |
|---|---|
| El archivo está **truncado** | 0 `%%EOF`, 0 `startxref`. Por eso `pypdf` y `pdftotext` se plantan |
| **MuPDF lo abre en modo reparación** | reconstruye la tabla de referencias (`is_repaired = True`) |
| Páginas | **766** |
| Capa de texto | **3.000.938 caracteres** (OCR antiguo, `GlyphLessFont`) |
| ¿Volumen equivocado? | **No**: «HISTORIA GENERAL Y NATURAL DE LAS INDIAS… PRIMERA PARTE… 1851», libros **I-XIX** |

```python
import pymupdf                      # pypdf y pdftotext NO sirven aquí
d = pymupdf.open("fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1.pdf")
d[n].get_text()                     # impresa = pdf − 118
```

Es la trampa de CLAUDE.md «`pypdf` ≠ `pdftotext`» con un tercer extractor que
nadie había probado. **Cuando los dos fallan, probar MuPDF antes de declarar
ilegible una fuente.**

## ⚠️ Pero la imagen sólo llega hasta la impresa 154

> 🟢 **Superado el 2026-09-22 (M3):** eso vale para la copia truncada. La
> copia íntegra (`_completo.pdf`, ver `acceso`) renderiza todas las páginas.
> Lo de abajo sigue valiendo como historia y como aviso sobre la cursiva.

Medido página a página sobre las 766: las impresas **1-154** se renderizan; de
la **155 a la 618** el escaneo está roto (`format error: object is not a
stream`) y sólo queda el OCR.

Y eso importa mucho más de lo que parece, porque **el editor de 1851 pone las
voces indígenas en cursiva y el OCR falla justo en la cursiva**: corrompe
precisamente la palabra que se busca. Medido con la página delante:

| OCR | La página | p. |
|---|---|---|
| `buhüí` | **`buhití`** | 126 |
| `gemi` | **`çemi`** | 126 |
| `hixa` | **`bixa`** | 146 |

Tampoco se puede detectar la cursiva por software (la capa es `GlyphLessFont`,
sin información de fuente). Se localiza con el OCR y **se lee con los ojos**.

Por eso cada entrada de la propuesta declara `verificacion: imagen` o
`verificacion: ocr-sin-imagen`, y lo segundo **no se fusiona sin ver la
página**.

## Qué es

La crónica de Indias más antigua del repo con vocabulario **glosado**. Oviedo
vivió en Santo Domingo desde 1514 y escribe hasta 1548: no recoge listas de
palabras, pero explica lo que nombra, y con frecuencia dice de dónde es la voz
(«en esta Isla Española», «en la lengua de Hayti», «los indios de Nicaragua»).
Eso lo convierte en un diccionario disperso dentro de una historia natural.

El vol. I trae los libros que interesan: **V** (ritos y çerimonias), **VI**
(casas, batey, canoas, huracanes), **VII** (agricultura), **VIII-XI** (árboles
y hierbas), **XII-XIV** (animales, animales de agua, aves), **XVI-XVIII** (San
Juan, Cuba, Jamáyca) y **XIX** (Tierra-Firme).

## Qué ha dado — minería del 2026-09-21 (campaña del taíno, T1)

Datos en [`6-fusion/taino_oviedo_valdes_1851.yaml`](../6-fusion/taino_oviedo_valdes_1851.yaml),
discusión en [`6-fusion/issues-pendientes/taino-oviedo-2026-09-21.md`](../6-fusion/issues-pendientes/taino-oviedo-2026-09-21.md).
Las cifras salen de `python 6-fusion/scripts/medir_taino_oviedo.py --check`.

**Lo mejor, por si se lee sólo esto:**

- **`eracra`** (Lib. VI cap. I, p.163) — «comunmente llaman *buhio* en estas
  islas todas (que quiere deçir casa ó morada); pero propriamente **en la
  lengua de Hayti** el buhio ó casa se llama *eracra*». La única vez en el
  volumen que Oviedo separa la voz pan-insular de la propia de la lengua. El
  lexicón tiene `bohio` y **no** tiene `eracra`.
- **`dalihao` / `datihao`** (Lib. XVI cap. V, p.473) — «á mi *dalihao* (que
  quiere deçir **mi señor, ó el que, como yo, se nombra**)», en boca del
  caçique **Agueybana**. Es la voz que esta nota daba por irreproducible: no
  estaba en un apéndice inexistente del tomo IV, estaba en el tomo I. **Pero
  Oviedo la atribuye a San Juan, no a los caquetíos** — ver §C del issue.
- **`buhití`** (p.126) — el behique, con su forma real, verificada en imagen.
- **Cinco especies de batata** con nombre propio (p.274) y **tres de piña**
  (p.280): taxonomía agrícola indígena.
- **`curi-á`** (p.380) — con **nota de acentuación del propio Oviedo**: «la á
  se ha de deçir poquito después que se diçe curi, para açentuarla como el
  indio la nombra».
- **Costa de Venezuela**: **`Paraguana`** (p.205, «que **los indios llaman** á
  aquella provinçia Paraguana»), **`comoho`** (pp.313-314, el cardón de las
  tunas «en la provinçia de Venezuela»), **`hado`/`hayo`** (p.206, degradada
  por duda de OCR) y **`yaguaraha`** (p.326, Cubagua).

**Y el aviso de método, dicho por la fuente** (p.279):

> «en estas islas y en la Tierra-Firme hay muchas diferençias de lenguas de una
> gente á otra, é una cosa tiene muchos nombres, é también diversas cosas
> tienen un mismo nombre; y querer escudriñar este, seria nunca acabar»

Oviedo sabía que estaba mezclando lenguas y lo declaró. Cualquier uso de esta
obra como fuente léxica debe citarse con esa advertencia al lado.

## Qué NO ha dado — los ceros, verificados (regla 6)

| Se buscó | Resultado |
|---|---|
| `Jamaica` | **0** — la obra escribe **Jamáyca** |
| `nitaino` / `nitayno` / `nilaino` | **0** — Oviedo no da la voz en este volumen |
| `maboya` / `mabuya` | **0** |
| `behique` / `bohique` | **0** — la voz existe, pero él escribe **`buhití`** |
| `borattio` / `borat*` | **0** — el dato de `creencia-001` **no está aquí** |
| `caquetío` / `caiquetío` / `Curiana` / `Coquibacoa` | **0** — no nombra a los caquetíos |

- **El funeral del díao no está** en el vol. I: sigue en el tomo II (pp.299-300
  y 329), como decía la ficha vieja. **Deuda cerrada el 2026-09-22**: los tomos
  II-IV están en el repo y el funeral está leído y verificado en imagen. Ver
  [[oviedo-y-valdes-1852-1855]].
- **El «apéndice de voces» del editor no existe aquí**: lo que cierra el
  volumen (impresas 619-648) es un **índice de capítulos**, útil para
  localizar, no para citar. 🔴 **Pero la frase seguía «…tampoco», dando por
  inexistente el del tomo IV, y eso era falso** (medido el 2026-09-22): el
  apéndice del tomo IV **existe**, se llama «VOCES AMERICANAS EMPLEADAS POR
  OVIEDO», ocupa las impresas 593-607 y trae doce entradas marcadas «(Lengua de
  Venezuela)», entre ellas `Datihao` y `Diao`. Es el que cita Jahn 1927 p.213
  n.29. El «rastreo del 2026-08-14 sobre el tomo IV» que se invocaba aquí no lo
  encontró porque el tomo IV no estaba en el repo.

### 🔴 Y otras dos correcciones medidas el 2026-09-22

- **«Oviedo no nombra a los caquetíos»** (la fila de `caquetío`/`caiquetío` = 0
  de la tabla de arriba) vale para **este volumen**, no para la obra: en el tomo
  II los nombra 12 veces, y la sonda daba cero porque **la obra escribe
  `çaquitios`**. Añádanse `çaquiti`, `zaquiti` y `saquiti` a las sondas.
- **El desfase no es «impresa = pdf − 118» en todo el volumen**: la impresa 473
  —la de `dalihao`— está en la pdf **590**, o sea desfase **117**. La cita de la
  minería de T1 es correcta; la fórmula del frontmatter falla en ese tramo.

## 2026-09-22 — releído por el GUANÍN y por quién tradujo (campaña del taíno 2, T7)

**Qué se preguntó.** No por el léxico taíno en general, sino por dos cosas:
qué es el guanín, dicho por el cronista, y **con qué calidad de intermediación
llega cada dato de lengua**. Extraído con el método de MuPDF que esta nota ya
dejaba escrito. Datos y citas en `6-fusion/taino2_etnohistoria_contacto.yaml`
(t7.g7, t7.g8, t7.d1).

**Medido** sobre las 766 páginas, con el mismo script que las otras cinco
obras de la parcela (`6-fusion/scripts/medir_taino2_etnohistoria.py`, que lleva
este volumen por la vía de MuPDF): `guanin` **3** (impresas 480 y 507) ·
`cobre doradas` **1** (507) · `dalihao` **1** (473) — y `datihao` **0** ·
`datiao` **0** · `guatiao` **0** · `tiao` **0**. El único portador de la forma
en todo el volumen es ese `dalihao`.

### 🔴 Oviedo DEFINE el guanín, y no es oro

**Lib. XVII cap. IX, impresa 507** (pdf 625), viaje de Grijalva por Yucatán:

> «trayan unos **guanines** que se ponen en las orejas é unas patenas redondas
> de **guanin**… pero **porque el letor entienda qué cosas son guanines, para
> adelante digo que son pieças de cobre doradas; é si algund oro tienen, es muy
> poco ó ninguno**.»

Es la definición técnica del objeto por el cronista que además fue veedor de
fundiciones, y ordena el resto: el «oro bajo» de Colón, el «oro aunque no
puro… como el alemán de que se acuñan los florines» de [[angleria-1892]] y el
«color algo morada» de [[las-casas-1875]] son **el mismo objeto**.

⚠️ **Y es la prueba del vector 1 de Oliver en el acto.** El pasaje es de
**Yucatán**: Oviedo aplica sin pestañear una palabra antillana a unos objetos
mayas, con un intérprete español de por medio («Julián la lengua»). Que un
cronista llame `guanín` a algo **no atestigua que allí se llamara así** — lo
que rebaja el peso de las dos apariciones de `guanines` en Chiribichi
(Anglería vol. 4, pp. 335-336 y 364).

**Lib. XVI, impresa 480** (pdf 598), Boriquén 1511: «un caçique… llevaba en los
pechos **un guanin ó pieça de oro de las que suelen los indios principales
colgarse al cuello**». El uso taíno del objeto —insignia de principal— fijado
por el mismo cronista que lo define.

### `dalihao` (p. 473): lo que sí se puede citar sin reserva

No es la forma —eso queda bloqueado hasta ver la imagen—, sino **quién
tradujo**, y es lo mejor de toda la serie:

> «é cómo llegó luego Agueybana, **dixo la lengua, en el lenguaje de los
> indios**: "Señor, ¿por qué me mandas matar? Yo te serviré é seré tu naboría";
> y entonces dixo el cacique: "Adelante, adelante, **á mi dalihao (que quiere
> decir mi señor, ó el que, como yo, se nombra)**, dexa ese bellaco."»

El hablante es Johan González, a quien Oviedo llama dos veces «la lengua» y una
«**grande lengua**»: un español que sabía boriquén lo bastante para meterse
desnudo y pintado en un areíto y entender lo que se cantaba. Y la glosa
—«**el que, como yo, se nombra**»— es la del **intercambio de nombres**, es
decir la institución, no un título.

Consecuencia para `decisiones_campanas_2026-09-21.yaml` §dc.4 (PR #193): las
dos atestaciones de `datihao` **no valen lo mismo**. Ésta se puede leer y pesar;
la de «los indios de la Provincia de Venezuela» está en un tomo que el repo no
tiene y llega por [[jahn-1927]] p. 213 n. 29. Antes de llamarlo «cognado que
hace match», leer la segunda.

## 2026-09-22 — M3: el libro XIX, la historia natural y `guaitiao` (tercera campaña)

**Qué se preguntó.** Lo que T1 dejó sin leer: el libro XIX, los libros de
historia natural (todo animal de Tierra Firme o de las costas de Venezuela, con
su SONIDO si Oviedo lo da, en la clave `fauna:` común), las voces de esos
pasajes y la palabra `guaitiao`. Datos en
[`6-fusion/oviedo_restante_2026-09-22.yaml`](../6-fusion/oviedo_restante_2026-09-22.yaml);
discusión en
[`6-fusion/issues-pendientes/oviedo-restante-2026-09-22.md`](../6-fusion/issues-pendientes/oviedo-restante-2026-09-22.md).
Cifras: `python 6-fusion/scripts/medir_oviedo_restante.py --check`.

**Primero, la copia.** Se descargó la **copia íntegra** del tomo (ver
`acceso`). Renderiza todas las páginas: se acabó el límite de la impresa 154.
Todo lo que esta parcela cita en cursiva está leído en la página.

**🔴 Lo que resultó falso al medirlo:**

- **El libro XIX no es «Tierra-Firme» ni llega a la 618.** Su título: «el qual
  tracta de las islas de Cubagua é la Margarita». Ocupa las impresas
  **586-614**; en la 615 empieza el índice general (esta ficha decía «618
  impresas de cuerpo + índice (619-648)»: el cuerpo termina en la 614). Y no
  trae Coro, Paraguaná, Coquibacoa, Curiana, las islas ABC, Manaure ni Ampíes:
  leído entero, el cero es de la fuente.
- **`dalihao` era el OCR de la copia truncada: la página dice `datihao`** (p.
  473, cursiva, con zoom). Queda cerrado el punto 1 de «Qué falta».
- **`talara`, el pez de Cubagua, es `tatara`** en la página (pp. 209 y 592).
- **Los capítulos venezolanos del libro VIII no son una segunda fuente**: el
  propio Oviedo dice en el t. II p. 331 que los añadió a esta primera parte con
  la información del obispo Bastidas, y el de los cardones lo nombra.

**Qué ha dado, lo mejor:**

- **`dactos` / `dacto`** (lib. VIII cap. XXVII, pp. 311-312) — «los quales
  llaman los indios de Veneçuela dactos»: la primera fuente primaria de `dato`,
  con su estación de fruto. Y **`mamon`** (p. 327), **`çimirucos`** (p. 328), el
  **vino de comoho** (p. 315).
- **`thenocas` y `coçixas`**, las perlas en la costa de Cubagua (p. 591).
- **`uchibican`**: «en la lengua desta Isla Española se diçe serra, en lengua
  destos magueyes ó chacopati el trocar quiere deçir uchibican» (pp. 208, 385).
  El único par Tierra Firme–Antillas de los cuatro tomos, dentro de un rito: al
  eclipse de luna los chacopati le tiran flechas y lo truecan todo con sus
  vecinos, pueblo por pueblo.
- **Los indios de Maracapana gritan «Hayti, Hayti»** a los navíos en 1520 (p.
  598): conocen el nombre indígena de La Española — conocimiento colonial.
- **`bagua`, la mar** (p. 436) y **`manicato`** (p. 435), voces taínas que T1 no
  recogió.
- **Fauna con sonido**: el flamenco de Cubagua «graznan como ánsares» (p. 592),
  la cascabel de Margarita (p. 209), el lobo marino que ronca (p. 428), el
  pecarí que castañetea (p. 409), la bivana de Paria que silba (p. 417), el
  perico ligero y sus seis notas (p. 413). La tabla, en el issue §A.

**`guaitiao`: cero, y ahora con la página delante.** Oviedo cuenta el
intercambio de nombres en San Juan (pp. 467, 469, 472-473: «es de costumbre de
los indios en estas islas, que quando toman nueva amistad, toman el nombre
proprio del capitan») y en ninguno de esos pasajes aparece la palabra. La voz que
da es `datihao`. La nota de `waitiao` en el lexicón («lo describe Oviedo para el
área circuncaribe») no se sostiene: decisión en el issue §B.

**Qué NO dio:** ningún canto de ave de la costa de Venezuela aparte del
flamenco; las aves que cantan son de La Española. El capítulo de ranas y sapos
no dice cómo suenan. Nada de la gente de las islas ABC.

## Qué falta

1. ~~Conseguir una copia con la imagen completa~~ — **hecho** (2026-09-22). Lo
   que queda es USARLA para las formas `ocr-sin-imagen` de T1 (`eracra`, las
   cinco batatas…): cuántas son lo dice `meta.cobertura.por_verificacion` de
   `taino_oviedo_valdes_1851.yaml`.
2. ~~Leer el Libro XIX~~ — **hecho** por M3: es Cubagua y Margarita, 586-614.
3. **El libro VI («de los depósitos»)** entero: es el cajón de sastre de Oviedo
   y M3 sólo leyó los caps. XVI y XXII-XXIV. Allí aparecieron los chacopati.
4. **Los libros XV y XVIII**, y las plantas de La Española de VIII-XI fuera de
   las páginas ya citadas.
5. ~~Tomo II para el funeral del díao~~ — hecho por T6 ([[oviedo-y-valdes-1852-1855]]).
6. **Decidir `creencia-001` y `waitiao`** (issues de T6 y de M3).

## Qué sostenía antes (todo de segunda mano) — y qué cambia

| Entrada | Vía | Estado tras esta minería |
|---|---|---|
| `creencia-001` | *borattio* / *datihao-diao* = «señor», vía [[jahn-1927]] p.213 n.29 | **`datihao` localizado en la fuente primaria** (p.473) — pero **de San Juan**, no caquetío. `borattio` **no aparece**. Corrección pendiente |
| `creencia-001b` | el díao como jefe con poderes mágicos, vía [[arcaya-1920]] | sin cambio |
| `creencia-010`, `010b`, `010c` | el funeral del díao (t. II, 299-300), vía [[arcaya-1920]] | sin cambio — **el tomo II sigue haciendo falta** |
| `creencia-004b` | ayuno ritual antes de guerra (t. II, 329), vía [[arcaya-1920]] | sin cambio |

⚠️ `sostiene` no se toca a mano; lo mide `medir_sostiene.py`.

## Enlaces

[[arcaya-1920]] · [[jahn-1927]] · [[oviedo-y-banos]] · [[pane-c1498]] ·
[[las-casas-1875]] · [[03_creencia_caquetia]]
