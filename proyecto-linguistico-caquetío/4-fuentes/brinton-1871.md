---
tipo: fuente
obra: "The Arawack Language of Guiana in its Linguistic and Ethnological Relations"
autor: "Brinton, Daniel G."
anio: 1871
genero: linguistica-comparativa
local: ["fuentes_caquetios/Brinton_1871_texto.txt", "fuentes_caquetios/Brinton_1871_Arawack_Language_Guiana.pdf (0 bytes)"]
paginas: "—"
capa_texto: si
estado_minado: minado
cobertura: "el vocabulario antillano (pp. 11-14) y la toponimia (pp. 14-15), pasaje a pasaje; el resto por patrón"
prioridad: hecha
sostiene: {hechos_corpus: 0, entradas_lexicon: 84}
verificado: 2026-09-21
aliases: ["Brinton 1871"]
---

# Brinton 1871 — *The Arawack Language of Guiana*

## Qué es

Comparativa arahuaca del s. XIX. Es la fuente que **más entradas del lexicón
cita después de [[zavala-reyes-2015]]**: 84 — aunque casi todas del lado lokono
y taíno, no caquetío (solo 1 de familia caquetía).

## Estado técnico (verificado 2026-07-29) — ⚠️ el PDF está vacío

| Archivo | Estado |
|---|---|
| `Brinton_1871_Arawack_Language_Guiana.pdf` | **0 bytes** — inservible |
| `Brinton_1871_texto.txt` | **86 KB de texto plano, íntegro** ✔ |

El minado se hizo sobre el `.txt`, así que **la fuente sigue disponible** — pero
el PDF de respaldo no existe. Si alguna vez hace falta verificar una página o una
tabla contra el original, hay que reconseguirlo. **Uno de los 6 archivos de 0
bytes del repositorio** (ver [[INDICE_FUENTES]]).

## Qué ha dado

- **4 pares LK-TN reales** (lokono-taíno) para la validación comparativa de
  `arahuaco_comparative.py`.
- **Un bug corregido en `REGLAS_LK_TN`** — el hallazgo más valioso: minar la
  fuente reveló que la regla de transducción estaba mal.
- 84 entradas del lexicón lo citan en `notas`.

## Segunda minería — campaña del taíno, 2026-09-21 (parcela T2)

Propuesta en `6-fusion/taino_brinton_1871.yaml`; cola de decisión en
`6-fusion/issues-pendientes/taino-lascasas-pane-brinton-2026-09-21.md`.

### 🔴 La atestación es del CRONISTA, no de Brinton

Es lo primero que hay que saber de esta fuente y no estaba escrito. Brinton no
oyó hablar taíno a nadie: la lengua llevaba tres siglos muerta. **Cada entrada
de su vocabulario es una cita**, y lo que vale como procedencia es la obra
citada. Detrás de las 68 entradas hay: Las Casas (*Apologética* caps. 2, 46,
61, 120, 197, 198, 199, 204, 241; *General* lib. i caps. 90 y 120, lib. iii
caps. 21 y 33), Pedro Mártir (*Décadas*, 12 entradas), Oviedo, Pané, Navarrete
(*Viages*, o sea el diario de Colón) y Richardo (diccionario cubano del s. XIX).

**Corroboraciones falsas detectadas** (skill §8): `caona`/`nozay`/`tuob`,
`macana` y `guanara` parecen confirmar a [[las-casas-1875]] y a [[pane-c1498]],
y no: Brinton cita el mismo diario y el mismo Pané por otra puerta. Apoyo real
en los tres casos: **uno**.

### El nombre «taíno» es una invención del siglo XIX, y Brinton lo dice

> The latter truncated form of the word was adopted by Rafinesque and others,
> as a general name for the people and language of Hayti. **There is not the
> slightest authority for this** (p. 13)

`taíno` es el truncamiento de `nitayno`, un **título** de nobleza —«caballero y
señor principal» en [[las-casas-1875]] tomo I cap. LVIII, `taynos nobiles` en
Pedro Mártir— que Rafinesque ascendió a nombre de pueblo en 1836. Los autónimos
que sí hay son locales: `lucayos` = `lukku kairi` «hombres de las islas» (p.
15), `Siboneyes` = `siba eyeri` «hombres de las rocas» (p. 14). Encaja con lo
que dicen Pané y Las Casas: **no había un pueblo ni una lengua a los que poner
un nombre único.**

### Qué dio esta vez

- **El vocabulario entero: 68 entradas** (pp. 11-14), cada una con su cronista,
  su glosa verbatim y la comparanda arawack que Brinton propone.
- **Los 4 numerales** con sus cognados arawack (p. 14, de Las Casas *Apol.*
  204) — dato de **filiación**, no de contacto.
- **Cinco frases y compuestos** con glosa, incluida la única conversación taína
  conocida (`Teitoca teitoca...`, de Pedro Mártir), que Brinton no reconoce
  como arahuaca. **Es verificable aquí mismo**: [[angleria-1892]] está en el
  repo.
- **`ma-` privativo y `-caco` 'ojos'**, sacados de dos insultos que recoge Las
  Casas (p. 14). El caquetío tiene `ma-` privativo declarado con dos apoyos:
  esto es lo más fuerte que la parcela pone en la mesa del cruce.
- **«la penúltima sílaba luenga»**: la frase de Las Casas que se buscaba en el
  tomo I y que allí no existe está aquí, citada de la *General* lib. iii cap.
  21 (p. 14, nota 28), sobre `Cibon-eyes`.
- **`bazca` 'no'**, la única palabra de MACORIX conocida (p. 18), y la noticia
  de que macorix eran **dos** provincias, de arriba y de abajo.

### Lo que resultó falso

- **`lokono` aparece 0 veces.** Brinton dice siempre `Arawack` y da el autónimo
  `lukkunu` 'men'. Quien busque «lokono» aquí saca cero y concluye mal.
- **El PDF sigue con 0 bytes**, dos meses después de que se anotara.
- La ortografía arawack de Brinton sigue **convención alemana** (misioneros
  moravos): su `j` es /j/, su `w` es /v/, su `ch` es /x/. Quien lea esa columna
  con valores ingleses la lee mal. No estaba dicho.

### Qué falta

1. **Reconseguir el PDF** para poder citar páginas (F9). El OCR conservó los
   números en los encabezados corridos y así se recuperaron las pp. 3, 4, 9,
   10, 11, 12, 14, 15 y 18 — pero **13, 16 y 17 se perdieron**.
2. Nunca se le preguntó por **transmisión/pedagogía** — [[04_transmision]] lo
   deja anotado: se minó solo bajo el lente léxico.
3. Es material directo para F5 ([[oliver-1989-cap2]]): más cognados verificados
   = más munición para validar o degradar las 441 formas de
   `lexicon_candidatos.py`.
4. **Verificar contra [[angleria-1892]]** las 12 entradas que Brinton toma de
   Pedro Mártir, más la conversación. Convertiría 12 citas de segunda mano en
   primarias sin descargar nada. Es lo de mayor rendimiento por hora que queda.
5. `Bugi` y `Aiba`, que Brinton atribuye a Pané, **no están en el Pané del
   repo** (0 ocurrencias). Sin resolver.

## Enlaces

[[oliver-1989-cap2]] · [[perea-alonso-1942]]

---

## Bitácora: Brinton escribe *cohoba*, no *cohiba* (2026-09-23, cc.7)

p. 12, «Cohóba, the native name of tobacco»; p. 13, «Tabaco, the pipe used in
smoking the cohoba» (texto del repo y `6-fusion/taino_brinton_1871.yaml`). La
nota del lexicón que atribuye `cohiba` a Brinton cita mal la forma. 🔴 El PDF
del repo está commiteado VACÍO en esta rama (blob `e69de29`, 0 bytes); #220
lo repone (2.179.167 bytes). Por eso no se vio la imagen: la forma sale de la
capa de texto y de la transcripción de T10, que coinciden. Detalle: `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml` §zayas.cohiba_tabako.
