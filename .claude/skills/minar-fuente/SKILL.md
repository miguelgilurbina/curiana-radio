---
name: minar-fuente
description: Minar una fuente documental del proyecto lingüístico caquetío (PDF o texto en fuentes_caquetios/) para una pregunta concreta. Usar cuando se pida minar, leer, barrer o extraer datos de una obra — Oliver, Jahn, Arcaya, Zavala, Oviedo, Alvarado, van Buurt, Gatschet, Antczak — o de una fuente nueva que se incorpore. También al verificar si una fuente sostiene una entrada del corpus o del lexicón.
---

# Minar una fuente

Protocolo destilado de diez minerías reales. Cada paso está porque **saltárselo
costó un error concreto** que aquí se nombra.

## 0. Antes de abrir nada: ¿qué pregunta le haces?

Una minería sin pregunta produce un resumen, y un resumen no sirve para nada.
La pregunta sale del issue, del corpus o del hueco que se quiere llenar.

Si la pregunta viene de un issue, **léelo entero primero**: suele traer la
receta técnica y el artefacto conocido.

## 1. Extraer — y desconfiar del extractor

```bash
pdftotext -enc UTF-8 "fuentes_caquetios/OBRA.pdf" salida.txt
```

- **`pypdf` y `pdftotext` no producen el mismo texto.** Medido: `pypdf` parte
  "Todariquiba" en `T odariquiba` en sus 7 apariciones; `pdftotext` la da limpia
  en las 7. Y al revés, Arcaya devuelve **vacío** con `pypdf` y 467 KB con
  `pdftotext`.
- **Las tablas a dos columnas se desalinean** sin `-layout`. Si vas a leer una
  tabla comparativa, extrae *otra vez* con `-layout` y compara. Así se
  recuperaron `tapári`/`tarágla` en Jahn pp. 438-439.

## 2. 🔴 Medir la ortografía ANTES de contar

**Este paso existe porque el mismo error apareció tres veces en una noche.**

Un `grep` que devuelve cero **no prueba que la fuente no hable del tema**:
prueba que tu consulta no encontró nada. Los tres casos reales:

| Fuente | El grep que falló | Por qué | La realidad |
|---|---|---|---|
| Antczak 2017 | `Caqueti` → 0 | el PDF descompone acentos: `Caquet´ıo` | 8 menciones |
| Oviedo y Baños | `caquet` → 0 | escribe **`caiquetía`**, y `Coriana` por Curiana | 7 menciones |
| Oliver cap. 3 | `Todariquiba` → 0 | `pypdf` lo parte | 7 apariciones |

Antes de concluir nada:

```bash
# 1. raíz corta y sin acentos, no la palabra entera
for t in caquet caiquet Coriana Curiana Manaur Paraguan; do
  printf "%-12s %s\n" "$t" "$(grep -o -i "$t" salida.txt | wc -l)"
done
# 2. lee una página al azar y mira cómo escribe ESA obra los nombres
```

Las crónicas coloniales **no usan la ortografía moderna**. Nunca.

## 3. Leer los pasajes, no los conteos

Los conteos te llevan a la página; el dato está en el texto. Extrae contexto
generoso (`grep -o ".\{300\}PATRÓN.\{400\}"`) y **lee lo que hay alrededor**.

Localiza la **página impresa**, no la del PDF. Suelen diferir por un desfase
constante que se calcula una vez (en Antczak: pdf + 130 = impresa).

## 4. Repartir el hallazgo por esferas, no solo al lexicón

**Esta es la parte que se venía haciendo mal.** Medido el 2026-08-06: de 30
obras, **18 dejan rastro en una sola esfera**. Parte es real —un paper de
genética no da topónimos— y parte es que se minaba con el lexicón en la cabeza y
lo demás caía donde cayera.

Antes de escribir nada, pregúntate a **cuál de estas** va cada hallazgo:

| Esfera | Dónde vive | Qué acepta |
|---|---|---|
| lengua — léxico | propuesta `lexicon_*.py` | palabras, glosas, afijos |
| lengua — cognados | `2-lengua/cognados.yaml` | relaciones entre lenguas |
| lengua — topónimos | `2-lengua/toponimos.yaml`, `morfemas.yaml` | nombres de lugar, formantes |
| mundo — parentesco | `3-mundo/corpus/parentesco.yaml` | familia, sucesión, linaje |
| mundo — ecología | `3-mundo/corpus/ecologia.yaml` | medio, fauna, flora, huecos léxicos |
| mundo — creencia | `3-mundo/corpus/creencia.yaml` | rito, muerte, boratio, cosmos |
| mundo — transmisión | `3-mundo/corpus/transmision.yaml` | cómo se aprende y se enseña |
| mundo — geografía política | `geografia_politica.yaml`, `polities-caquetias.md` | territorio, autoridad, polities |
| experimento | `5-experimento/` | lo que cambia cómo se corre o se mide |

Una fuente buena alimenta **varias**. Oliver cap. 3 dio geografía política,
guerra, economía y religión en el mismo barrido; Jahn dio parentesco, un mapa de
polities y una corroboración léxica.

Comprueba después con `python curiana_sim/medir_sostiene.py --esferas`.

## 5. Y escribir la bitácora en la nota de la fuente

La nota (`4-fuentes/<slug>.md`) es la **bitácora**: qué se preguntó, qué se
halló, qué **no** se halló, qué deuda queda. Ya no es el almacén — el dato vive
en su esfera y cita la obra por `procedencia.obra`.

Actualiza el frontmatter: `estado_minado`, `cobertura`, `verificado`, `minado`.

⚠️ **`sostiene` no se toca a mano.** Se mantenía así y ha derivado en 17 de 30
obras. Lo mide `medir_sostiene.py`.

Si la obra es nueva en el repo, regenera la bibliografía para que su id exista
como clave foránea: `python curiana_sim/generar_bibliografia.py`.

Estructura que funciona:

- **Qué es** y **si trata de lo que se creía** — Antczak resultó no tratar de lo
  que el corpus asumía, y decirlo primero fue lo más útil de esa minería.
- **Qué ha dado**, con página por hallazgo.
- **Veredicto por entrada** si el encargo era verificar entradas del corpus.
- **Qué falta**, incluida la deuda documental nueva que la minería genera.

## 6. Las negativas valen tanto como las positivas

Oviedo y Baños fue señalada *"por su cobertura de sucesión cacical"*. Medido: la
cobertura **no existe** (Manaure aparece 2 veces en 519 páginas). Escribir eso
ahorra que alguien vuelva a gastar una noche ahí.

Un hallazgo negativo **bien medido** baja la prioridad de una fuente y eso es
progreso.

## 7. Propuesta, no fusión

**No toques `curiana_lexicon.py` ni `3-mundo/corpus/*.yaml` en una minería.**

Cada minador emite una *propuesta* (`lexicon_*.py`) o deja los hallazgos en la
nota. La fusión al corpus es decisión humana. Es lo que ha permitido minar ocho
fuentes sin romper nada.

⚠️ Excepción con trampa: `lexicon_zavala.py` **sí** lo importa
`curiana_lexicon`. Regenerarlo cambia `score_linguistico()`.

## 8. Segundas atestaciones y conflictos

Si la fuente confirma algo que ya estaba: eso **sube** una entrada de "una
fuente" a "dos independientes", que es de lo más valioso que hay.

Pero comprueba que sea **independiente de verdad**. Jahn parecía corroborar la
filiación caquetía de `datihao` y no: está citando el mismo apéndice de Oviedo
del que viene la duda. Una corroboración falsa es peor que ninguna.

Si contradice al lexicón, **no reescribas la glosa**: añade la evidencia a
`notas` y levanta/actualiza el issue. Cambiar una glosa mueve canon.

## 9. Cerrar

```bash
python curiana_sim/guardianes.py     # los siete en verde
python curiana_sim/generar_tablero.py
```

Y en el commit: qué se preguntó, qué se encontró, **qué NO se encontró**, y qué
deuda nueva queda. Si la minería tocó un issue, coméntalo ahí con la evidencia
en vez de dejarlo solo en el markdown.
