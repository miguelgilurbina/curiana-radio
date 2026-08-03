---
tipo: fuente
obra: "Caquetío Indians on Curaçao during colonial times and Caquetío words in the Papiamentu Language — Some names of Animals and Plants in Papiamentu"
autor: "van Buurt, Gerard"
anio: 2014
publicacion: "Edición propia, Curaçao (ISBN 978-99904-2-348-8); base en van Buurt & Joubert, *Stemmen uit het Verleden*, 1997"
genero: glosario-etnohistoria
local: "VanBuurt_2014_CaquetioWords_Papiamentu.txt"
paginas: 48
capa_texto: si
estado_minado: sin-minar
prioridad: alta
tareas: [F6]
sostiene: {hechos_corpus: 1, entradas_lexicon: 0}
verificado: 2026-07-29
aliases: ["Van Buurt 2014", "Caquetío words in Papiamentu"]
---

# Van Buurt 2014 — Palabras caquetías en el papiamento

## Qué es

**El léxico caquetío superviviente**, tal como sobrevive dentro del papiamento
de Curazao, Aruba y Bonaire — y, metodológicamente, **la fuente más afín al
espíritu de este proyecto**: van Buurt separa explícitamente lo que es
"probablemente caquetío" de lo que tiene "vínculos menos ciertos", y explica por
qué esa distinción es necesaria.

> Su prólogo contiene una autocrítica que este proyecto haría bien en leer dos
> veces: la edición de 1997 presentaba la evidencia **sin decidir** qué palabra
> era caquetía y cuál llegó vía español, taíno o guajiro, para dejar que el
> lector concluyera. *"This has turned out to be a major mistake, leaving room
> for totally erroneous interpretations."* — La ambigüedad no marcada no es
> neutral: se lee como afirmación.

## Estado técnico (verificado 2026-07-29)

| Dato | Valor |
|---|---|
| Formato | **.txt de 92 KB**, extraído del PDF de tiboko.com — vive en la **raíz del proyecto**, no en `fuentes_caquetios/` |
| Capa de texto | sí, limpia; conserva acentos y diacríticos |
| Estructura | 12 secciones numeradas, localizables por `grep -nE "^\s*[0-9]{1,2}\. [A-Z]"` |

📌 **Nota de orden**: es la única fuente del corpus que no está en
`fuentes_caquetios/`. Moverla (o dejar constancia de por qué no) es trabajo de
un minuto que evita que se pierda de vista.

## Qué contiene (inventariado hoy, nunca minado)

| Sección | Contenido | Volumen |
|---|---|---|
| 2-4 | Llegada del hombre a Curazao; contactos Curazao–Aruba–Bonaire–Venezuela; **los caquetíos en época colonial** | etnohistoria, ~170 líneas |
| 5 | Cómo entran las palabras caquetías al papiamento | — |
| **6** | **Palabras probablemente de origen caquetío** (sin topónimos) | **~98 entradas** con identificación taxonómica |
| 7 | **Topónimos probablemente caquetíos** | ~200 líneas |
| 8-10 | Etimología y comentario de topónimos de Aruba / Curazao / Bonaire | — |
| **11** | **Palabras con vínculo menos cierto** — el tier degradado | **~24 entradas** |

Ejemplos de la sección 6: `bushi` (Melocactus, y por extensión erizo de mar),
`chibichibi` (Coereba flaveola), `catashi`, `bulabari`, `ashibi`. De la 11:
`tata` (padre), `djaka` (rata), `kinikini` (Falco sparverius), `purunchi`
(mero) — **`tata` y `kinikini` ya están en el lexicón del proyecto**, y aquí van
marcados como *menos ciertos*.

Trae además etimologías comparativas útiles: `ima/nima` "húmedo" (Cruz Esteves
1989) — que es exactamente el afijo `-ima` de `REGLAS_ZAVALA`; `-baca/-bacu`
"grupo, matorral" vía [[alvarado-1921]]; comparaciones con lokono y taíno.

## Qué falta — **F6, prioridad ALTA**

1. **0 entradas del lexicón lo citan.** El proyecto lo lista como fuente y no lo
   ha abierto. Es, junto a [[gatschet-1885]] y [[alvarado-1921]], el triángulo
   de fuentes ALTA con cero penetración en el dato.
2. Importar la sección 6 con etiqueta `caquetío-atestiguado` y la sección 11 con
   una **etiqueta degradada** — respetando la separación que el propio autor
   hace. Esta fuente **regala** la escala epistémica ya construida.
3. Cruzar con [[gatschet-1885]]: van Buurt critica explícitamente la lista de
   Pinart. Donde ambos coincidan, la confianza sube mucho.
4. La sección 4 (caquetíos en Curazao colonial) es material para
   [[MOC_geografia_politica]] — hoy solo sostiene `geografia_politica-001`.

## Enlaces

[[gatschet-1885]] · [[alvarado-1921]] · [[zavala-reyes-2015]] ·
[[MOC_geografia_politica]] · [[MOC_motor]] · [[INDICE_FUENTES]]
