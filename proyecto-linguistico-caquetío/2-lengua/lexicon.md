---
tipo: nota-viva
ambito: estado del lexicón activo
fuente_de_verdad: curiana_sim/curiana_lexicon.py
total: 1413
familia_caquetia: 304
sin_cita: 3
medido: 2026-08-04
---

# El lexicón

> El lexicón activo es `VOCABULARIO_BASE` en `curiana_sim/curiana_lexicon.py`.
> **Esta nota lo describe; no lo define.** Todas las cifras se midieron el
> 2026-08-04 corriendo el propio módulo, no copiándolas de la documentación
> anterior (que decía 1416 y 1414 en sitios distintos).

## El tamaño real

**1413 entradas.** No 1416 ni 1414: esos números están en `CLAUDE.md` y en
[[INDICE]] y quedaron atrás.

```bash
cd curiana_sim && python -c "import curiana_lexicon as L; print(len(L.VOCABULARIO_BASE))"
```

## Desglose por lengua

El campo `fuente` tiene **25 valores crudos distintos**;
`normalize_source_language()` (en `curiana_database.py`) los colapsa a estas
categorías:

| Categoría normalizada | Entradas | % |
|---|---:|---:|
| **wayunaiki** | **781** | 55,3 % |
| **caquetío** (todas las capas) | **304** | 21,5 % |
| **lokono** | **227** | 16,1 % |
| taíno | 57 | 4,0 % |
| kalinago | 19 | 1,3 % |
| proto-arahuaco | 8 | 0,6 % |
| jirajaroide-contacto | 7 | 0,5 % |
| caribe-continental | 4 | 0,3 % |
| kalinago-caribe-overlay | 4 | 0,3 % |
| español-colonial | 2 | 0,1 % |

> **Cuatro de cada cinco palabras del lexicón no son caquetío.** Son comparanda:
> están ahí para reconstruir, no para hablar. `score_linguistico()` las trata
> como tan ajenas como el español — una fuga a wayunaiki penaliza igual que un
> artículo castellano (ver [[mapa-motor]] §scoring).
>
> El reparto wayunaiki : lokono de **3,4 a 1** es el objeto de la decisión de
> fondo D11 → [[metodo-comparativo]] §el desbalance.

## Las capas epistémicas del caquetío

De las 304 entradas de familia caquetía:

| Etiqueta | n | Qué significa |
|---|---:|---|
| `caquetío-atestiguado` | **226** | Dato histórico real, citable a una obra concreta. Es lo único que no se discute. |
| `caquetío-reconstruido` | **68** | El **núcleo fundacional**: pronombres, numerales, verbos básicos que `prompt_reglas_completo()` presenta a los agentes desde el día 1. No siempre atestiguado — pero es la lengua de la simulación, no un préstamo. |
| `caquetío` (sin sufijo) | **8** | Etiquetado antiguo, sin capa declarada. Deuda de normalización. |
| `caquetío-hipotético` + `…/topónimo` | **2** | Marcadas como conjetura explícita. |

**3 entradas de familia caquetía siguen sin `notas`** (sin cita). Eran 82 en
julio de 2026.

## Quién sostiene el "atestiguado"

Este es el dato más importante de la nota. De las **226** entradas
`caquetío-atestiguado`, cuántas citan a cada obra en su campo `notas`:

| Obra | Entradas que la citan | |
|---|---:|---|
| [[zavala-reyes-2015]] | **215** | 95 % |
| [[alvarado-1921]] | 8 | ▍ |
| [[arcaya-1920]] | 8 | ▍ |
| [[van-buurt-2014]] | 7 | ▏ |
| [[oviedo-y-valdes-1851]] (vía terceros) | 6 | ▏ |
| [[oliver-1989-cap2]] | 5 | ▏ |
| [[gatschet-1885]] | 3 | ▏ |
| [[jahn-1927]] | 1 | |
| Galeotto Cey (vía terceros) | 1 | |
| [[brinton-1871]] | 1 | |
| *sin `notas`* | 2 | |

> **El caquetío atestiguado del proyecto es, en un 95 %, el glosario de Zavala
> Reyes 2015.** Las demás obras figuran como fuentes del proyecto y aportan una
> decena de entradas entre todas. No es un defecto de curación: es lo que hay
> publicado. Pero significa que **un error sistemático de Zavala sería un error
> sistemático del proyecto**, y que ampliar la base documental (F9: Oviedo t. II
> y el apéndice de voces caquetías del t. IV) es la deuda más cara que queda.

Zavala está **cerrado al 100 %**: `minar_zavala_glosario.py` parsea las 288
entradas del glosario. 225 (78 %) entran al habla activa; 63 (22 %) quedan
**fuera por diseño** — 45 topónimos, 14 antropónimos y 4 descartes. No es deuda:
es curación. Los topónimos excluidos, sin embargo, resultaron ser una mina de
morfemas → [[toponimia]].

## Las 441 candidatas aisladas

`curiana_sim/lexicon_candidatos.py` guarda **441 formas
`hipotético-no-verificado`**, **fuera del lexicón activo y fuera de Supabase**
desde 2026-06-28.

Las generó `reconstruir_caquetio_gaps.py` transduciendo fonológicamente
cualquier palabra wayunaiki, lokono o taína con la misma glosa española, **sin
verificar cognación real** contra `COGNADOS`. La minería de pares objetivos
(`minar_pares_validacion.py`) midió **~80 % de fallo** contra datos reales.

Por qué se aislaron, y no solo se re-etiquetaron: estando en `VOCABULARIO_BASE`
producían **falsos positivos en `score_linguistico()`** — un "la" o un "para"
españoles matcheaban contra entradas hipotéticas y el motor los contaba como
caquetío.

De dónde se transdujo cada una, medido sobre el campo `notas`:

| Lengua de partida | Candidatas |
|---|---:|
| solo wayunaiki | **388** (88 %) |
| solo lokono | 46 |
| ambas | 5 |
| taíno | 2 |

Ese 88 % es la misma sesgo que denuncia D11: **se reconstruyó desde la hermana
que Oliver considera la más lejana**, lo que explicaría parte del 80 % de fallo.

## `FUERA_DEL_HABLA` — el archivo, no la papelera

`FUERA_DEL_HABLA` es un dict del propio `curiana_lexicon.py` para entradas
**retiradas del habla activa sin borrarlas**: conservan forma, glosa y toda su
procedencia documental, pero no se ofrecen a los agentes ni cuentan para el
scoring.

**Hoy tiene un solo miembro: `piache`.** Retirada el 2026-08-03 (D10). Su lugar
lo ocupa `boratio`, que sí es caquetío atestiguado. Las dos fuentes coinciden:

- [[alvarado-1921]] p.248: *"Voz cháima y tamanaca, con formas afines en otras
  lenguas caribes"*.
- [[zavala-reyes-2015]] glosario #43 glosa el caquetío `boratio` **como**
  'piache, cacique, jefe, sacerdote, médico' — es decir, *piache* es la **glosa
  española**, `boratio` la voz caquetía.

El canon no se tocó: Shaboro sigue siendo el piache de la Curiana
([[mapa-creencia]]). El mecanismo es el importante: **archivar con procedencia
es distinto de borrar**, y deja el camino abierto si aparece evidencia en
contra.

## Los conflictos de glosa abiertos

Tres entradas cuya glosa activa **contradice a la fuente**, y que **no se
reescriben** porque corregirlas obliga a tocar el canon del mundo. Cada una
lleva su razonamiento completo en el campo `notas` de la entrada.

| Palabra | Glosa activa | Qué dice la fuente | Issue |
|---|---|---|---|
| `tara` | 'venado, ciervo' | **Doble corroboración en contra**: [[zavala-reyes-2015]] #238 'langosta, mariposa'; [[alvarado-1921]] p.283 'polilla o mariposa' (cf. *TARÍTA*, "mariposa o tara pequeña"). La glosa activa no tiene fuente localizada. | [#45](https://github.com/miguelgilurbina/curiana-radio/issues/45) |
| `saruro` | 'árbol saruro (frutos pequeños)' | Sin cita localizada; la fuente reasigna. | [#47](https://github.com/miguelgilurbina/curiana-radio/issues/47) |
| `corie` | 'choza, habitación' | [[zavala-reyes-2015]] #90 'armadillo' — **y el propio canon del proyecto ya dice armadillo**: `3-mundo/corpus/genealogia.yaml` da "corie (armadillo)" como tótem del linaje Paugis. La glosa contradice a la fuente **y** a su propio canon. | [#46](https://github.com/miguelgilurbina/curiana-radio/issues/46) |

**Por qué son caros.** `tara` sostiene material del corpus ecológico
([[mapa-ecologia]], `ecologia.yaml`, [[02_ecologia_golfete]] §10.6); `corie` da
nombre al asentamiento Corie-ko. Corregir la glosa no es editar una fila: es
mover el mundo. Por eso quedan como decisión de Miguel.

## Las 3 entradas que quedan sin cita

`auditar_82.py` cruza las cuatro minerías (Alvarado F3, Gatschet F4, van Buurt
F6, Zavala F7) y adjudica cada entrada de familia caquetía sin `notas`. El censo
arrancó en 82 y hoy va en **3**:

```
CENSO: 3 entradas de familia caquetía sin cita
0 confirman · 0 reclasifican · 0 conflicto de glosa · 0 a revisar · 3 sin rastro
```

Las 3 restantes **no dejan rastro en ninguna de las cuatro fuentes minadas**.
Ya no son deuda de minería sino de decisión: o aparece una fuente nueva (F9) o
se degradan a `caquetío-reconstruido`.

## Avisos operativos

> ⚠️ **Queries a la tabla `lexicon` en Supabase**: PostgREST corta cada
> respuesta en `max_rows` (1000). Con 1413 palabras, toda query sin `.range()`
> se trunca **en silencio**. Paginar con `.range(desde, desde+999)`.

> ⚠️ **`lexicon_zavala.py` no es solo una propuesta**: `curiana_lexicon.py` lo
> importa (`GLOSARIO_ZAVALA`, `HOMOGRAFOS_ZAVALA`). Regenerarlo **cambia el
> comportamiento de `score_linguistico()`**. Los otros tres módulos de propuesta
> (`lexicon_alvarado.py`, `lexicon_gatschet.py`, `lexicon_van_buurt.py`) no se
> importan en ninguna parte.

## Enlaces

[[morfologia]] · [[toponimia]] · [[metodo-comparativo]] · [[DECISIONES_ABIERTAS]]
