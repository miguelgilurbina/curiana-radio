---
tipo: fuente
obra: "Historia general y natural de las Indias, vol. I"
autor: "Fernández de Oviedo y Valdés, Gonzalo"
anio: "1851 [s. XVI]"
genero: cronica
publicacion: "Madrid, Imprenta de la Real Academia de la Historia, 1851. Primera parte (libros I-XIX), ed. José Amador de los Ríos, cotejada con el códice original"
local: "fuentes_caquetios/Oviedo_Valdes_1851_Historia_General_Indias_vol1.pdf"
paginas: "766 en el PDF · 618 impresas de cuerpo + índice (619-648). Desfase: impresa = pdf − 118"
capa_texto: si
estado_minado: minada-parcial
cobertura: "medida, no escrita a mano (+ el guanín y la calidad de intermediación, 2026-09-22, campaña del taíno 2 T7): `6-fusion/taino_oviedo_valdes_1851.yaml` → `meta.cobertura` y `meta.libros_leidos`. Las cifras las emite `python 6-fusion/scripts/medir_taino_oviedo.py --check`"
acceso: "El PDF local está TRUNCADO pero es legible con MuPDF en modo reparación (ver más abajo). La imagen escaneada sólo sobrevive hasta la impresa 154. Para lo que falta, la ed. Amador de los Ríos es libre en Internet Archive: tomo II https://archive.org/details/historiageneral01fernguat · tomo IV https://archive.org/details/historiageneral04fernguat"
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
  y 329), como decía la ficha vieja. **Esa parte de la deuda sigue abierta.**
- **El «apéndice de voces» del editor no existe aquí** tampoco: lo que cierra
  el volumen (impresas 619-648) es un **índice de capítulos**, útil para
  localizar, no para citar. Coherente con el rastreo del 2026-08-14 sobre el
  tomo IV.

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

## Qué falta

1. **Conseguir una copia con la imagen completa** (Internet Archive, ed. Amador
   de los Ríos). Desbloquea las 47 formas que hoy son sólo OCR — entre ellas
   `eracra`, `datihao` y las cinco batatas. Es lo más rentable de toda la lista.
   🔴 **Y es ahora más urgente**: con t7.d1 medido, `dalihao` es el único
   portador de la forma en todo el volumen y la imagen no llega a la p. 473.
2. **Leer el Libro XIX** (impresas 586-618): Tierra-Firme, Cubagua, Cumaná,
   Maracapana. Es el que más costa de Venezuela tiene y quedó sin leer.
3. **Leer los libros XV y XVIII** y el grueso de VIII-XVII fuera de las páginas
   ya citadas.
4. **Tomo II** para el funeral del díao (pp.299-300, 329) y el ayuno ritual
   (p.329), que es lo que sostiene `creencia-010` y `creencia-004b` vía Arcaya.
5. **Decidir lo de `creencia-001`**: Oviedo atribuye `dalihao` a San Juan. El
   corpus lo trata como caquetío. Ver §C del issue.

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
