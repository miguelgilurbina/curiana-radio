---
tipo: fuente
obra: "Diccionario provincial casi-razonado de vozes cubanas"
autor: "Pichardo y Tapia, Esteban"
anio: 1862
genero: diccionario-dialectal
local: ["fuentes_caquetios/Pichardo_1862_Diccionario_Provincial_Vozes_Cubanas.pdf", "fuentes_caquetios/Pichardo_1862_Diccionario_Provincial_Vozes_Cubanas.txt", "fuentes_caquetios/Pichardo_1862_Diccionario_Provincial_Vozes_Cubanas.ocr.txt"]
paginas: "3ª ed."
capa_texto: si
descargado: 2026-09-22
origen_digital: "Internet Archive, ejemplar de la University of Toronto (diccionarioprovi00pichuoft)"
estado_minado: sin-minar
cobertura: "medido al descargar (T10); OCR propio con tesseract hecho y medido (M5, 2026-09-23). Sin minar"
prioridad: media
verificado: 2026-09-22
aliases: ["Pichardo 1862", "Richardo"]
---

# Pichardo 1862 — *Diccionario provincial casi-razonado de vozes cubanas*

## Qué es, y por qué está aquí

Un diccionario del **español de Cuba** del s. XIX. No es un vocabulario taíno
y no pretende serlo.

Está en el repo por una razón muy concreta: **es la única autoridad detrás de
la entrada `taita` de nuestro lexicón**. Brinton 1871 p. 13 apoya `taita`
'padre' en «Richardo, Dicc. Provin.», que es Pichardo. Tener el diccionario
permite ver qué dice de verdad. Como escribió la ficha del mapa de fuentes:
*el caso de uso no es añadir voces, sino poder bajar una*.

## Estado técnico

| Cosa | Medido |
|---|---|
| PDF | 25,3 MB · sha256 `ddbcee29…f8f9cba9a` |
| Texto | `pdftotext -enc UTF-8`, 1,32 MB |
| Derechos | dominio público |
| Aviso | va **a dos columnas** y el OCR las entrelaza. Todo lo de aquí está leído sobre el texto aplanado y **verificado frase a frase**, no por segmentación |

## Qué se le preguntó al descargar (medido, sin minar)

| Consulta | Ocurrencias |
|---|---|
| `taita` | 4 |
| `taino` | 3 |
| `cayo` | 31 |
| `manigua` | 17 |
| `guabina` | 12 |
| `cobo` | 4 |
| `conuco` | 3 |
| `huracan` | 2 |
| `hutia` | 1 |

## Las dos entradas que ya se leyeron

**`Taita`** — «N. s. m. — **Voz ind.** — Tratamiento familiar que dan algunos
hijos a su padre, equivalente a Papá; otros dicen Taitá y pocos Tata o Tatá».
Y añade que Santacilia publicó un artículo sobre el asunto. En otra entrada
(`Mulecón`) registra que a los negros vendedores de edad provecta «suelen
decirles Taita».

→ Pichardo la marca **«voz ind.»**, sin decir taína ni citar cronista, en un
diccionario del español de Cuba. [[bachiller-morales-1883]] p. 394 lo corrige
expresamente y la manda a su apéndice de voces que pasan por indígenas y vienen
de otras partes. **La cadena entera de `taita` en nuestro lexicón es: Brinton →
Pichardo → nada.**

**`Taino`** — «N. adj. — Voz ind. — En el segundo viage del Almirante se dice
que los de **Guadalupe** usaban de esta palabra como equivalente de nuestro
adjetivo Bueno. Véase además Nitáino».

→ 🔴 Documenta `taíno` = 'bueno' **en Guadalupe**, que es territorio caribe
insular, y remite a `nitáino`. Es una pieza más del expediente sobre el nombre
de la lengua, y viene de una isla que no es ninguna de las Antillas Mayores.

## Qué falta

Minarlo de verdad: las 17 ocurrencias de `manigua`, las 12 de `guabina` y las
31 de `cayo` dirían qué parte de nuestras voces «taínas» es en realidad cubano
del XIX. Es el trabajo que separa el tainismo panhispánico de la voz antillana
atestiguada, y no está hecho.

## Ver también

[[bachiller-morales-1883]] · [[brinton-1871]] · [[coll-y-toste-1897]]

## Bitácora 2026-09-23 — tercera campaña, parcela M5

**Qué se hizo.** Sólo el texto. El `.txt` de archive.org entrelaza las dos
columnas y es casi ilegible; se hizo **OCR propio con tesseract**
(`ocr_fuente.py --lang spa --offset -26`, desfase medido en dos puntos: pdf 33 =
p. 7, pdf 150 = p. 124): `fuentes_caquetios/Pichardo_1862_Diccionario_Provincial_Vozes_Cubanas.ocr.txt`,
columnas separadas, 11 páginas enderezadas por el script.

**Medido en el OCR nuevo, sin leer:** `Voz ind` 386 · `Las Casas` 28 ·
`Herrera` 22 · `Oviedo` 17 · `Enciso` 4 · `manigua` 13 · `guabina` 12 · `cayo`
29. ⚠️ `taita` da 0 aquí y 4 en el OCR de archive.org: el nuevo pierde alguna
cabeza en negrita. Los dos textos se quedan.

**Qué falta.** Todo el minado: separar las «Voz ind.» con cronista de las que
no, y `manigua`, `guabina`, `cayo`.
