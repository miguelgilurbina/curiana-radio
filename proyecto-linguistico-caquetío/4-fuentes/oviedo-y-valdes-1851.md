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
cobertura: "medida, no escrita a mano: `6-fusion/taino_oviedo_valdes_1851.yaml` → `meta.cobertura` y `meta.libros_leidos`. Las cifras las emite `python 6-fusion/scripts/medir_taino_oviedo.py --check`"
acceso: "El PDF local está TRUNCADO pero es legible con MuPDF en modo reparación (ver más abajo). La imagen escaneada sólo sobrevive hasta la impresa 154. Para lo que falta, la ed. Amador de los Ríos es libre en Internet Archive: tomo II https://archive.org/details/historiageneral01fernguat · tomo IV https://archive.org/details/historiageneral04fernguat"
prioridad: alta
tareas: [F9]
verificado: 2026-09-21
minado: 2026-09-21
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

## Qué falta

1. **Conseguir una copia con la imagen completa** (Internet Archive, ed. Amador
   de los Ríos). Desbloquea las 47 formas que hoy son sólo OCR — entre ellas
   `eracra`, `datihao` y las cinco batatas. Es lo más rentable de toda la lista.
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
