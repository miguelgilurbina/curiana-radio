---
tipo: nota-viva
ambito: los topónimos como fuente de morfemas
fuente_de_verdad: curiana_sim/lexicon_toponimos.py
diseño: 03_descomposicion_toponimica
toponimos_glosados: 74
control_sin_glosa: 244
medido: 2026-08-04
---

# La toponimia como fuente de morfemas

> El método que abrió Miguel en F11, y el mejor rendimiento por unidad de
> esfuerzo que ha tenido el proyecto. El diseño completo está en
> [[03_descomposicion_toponimica]]; esta nota es la lectura corta.

## La idea

El proyecto venía archivando los topónimos como **canon inerte**.
`minar_zavala_glosario.py` los excluye del habla activa —45 topónimos y 14
antropónimos, *"fuera del habla por diseño"*— y las otras tres minerías hacen lo
mismo. La exclusión es correcta para el **habla**: un agente no debería decir
«Bariquisimeto». Pero tuvo un efecto colateral que nadie vio:

> **Los topónimos vienen con su traducción. Son ecuaciones bilingües de las que
> se puede despejar el morfema.**

Es criptoanálisis con texto plano conocido: se tiene la forma y se tiene el
significado; se despejan las partes.

## El caso que lo destapó: `jurijurebo`

El ejemplo de Miguel, y resultó estar **ya atestiguado pieza por pieza**:

| Pieza | Estado antes de F11 |
|---|---|
| `juri` = 'viento, ventarrón' | ✅ en el lexicón, `caquetío-atestiguado` (Zavala #178) |
| `ebo` = 'camino, paso, senda' | ✅ en el lexicón, `caquetío-atestiguado` (Zavala #117) |
| **`jurijurebo`** = **"Paso de los vientos"** | ⛔ archivado fuera del habla, marcado *"glosa incierta"* |

`juri~juri` + `ebo` = 'paso de los vientos'. **La ecuación cierra sin residuo**,
con la segunda copia perdiendo la vocal final por haplología
(`juri-jur-ebo`). Y hace tres cosas a la vez:

1. **Corrobora dos palabras** del lexicón por una vía independiente.
2. **Explica el plural de la glosa** — 'los vientos', no 'el viento': la
   reduplicación marca pluralidad.
3. **Sugiere una regla morfológica que el proyecto no tenía** — la
   reduplicación, que [[gatschet-1885]] documenta explícitamente para el arubano
   y que no estaba en `REGLAS_ZAVALA`. Ver [[morfologia]] §4.

Un solo topónimo archivado como inservible confirmó dos palabras y abrió una
regla. Segunda atestación independiente de `ebo`: *cumarebo* = "Camino del
cacique Cumare".

## El método, en cuatro pasos

1. **Segmentar** contra el inventario de morfemas conocido (`AFIJOS_ZAVALA`,
   `MORFEMAS_VAN_BUURT` y las 304 formas de familia caquetía del lexicón).
2. **Alinear** los segmentos con las partes de la glosa española.
3. **Despejar** el morfema desconocido cuando todos los demás encajan.
4. **Validar por recurrencia**: un morfema en un solo topónimo es conjetura; en
   tres o cuatro con glosa consistente es un hallazgo. **La frecuencia es el
   principal control de calidad.**

### Regla cero, y por qué está en el código y no en la prosa

> **Una segmentación que "suena bien" no es evidencia.**

El proyecto ya pagó ese precio: 441 formas transducidas sin verificar cognación,
~80 % de fallo medido ([[lexicon]] §candidatas). Segmentar topónimos tiene **la
misma tentación**: cortar donde convenga hasta que cuadre. Tres defensas:

- **La glosa manda sobre la forma.** `minar_toponimos.py` enumera *todas* las
  segmentaciones posibles y **deja que la glosa elija**. Una primera versión
  elegía la óptima por la forma y sacaba `Casibari` = `kasi`+`bari` —dos
  palabras del lexicón, cobertura perfecta, cero residuo— en vez del
  `ka-siba-rí` 'hay rocas duras' que [[van-buurt-2014]] documenta. **Ambas
  cubren los ocho caracteres; solo la segunda reconstruye la traducción.** Si la
  forma decide primero, el método se convierte en la trampa que dice evitar.
- **Recurrencia mínima ≥ 2** topónimos independientes, nombrados. Residuos de
  menos de 3 caracteres no cuentan: cualquier bigrama recurre en medio corpus.
- **Los topónimos coloniales, las glosas circulares y las meramente
  referenciales se apartan**, con la razón escrita.

## El corpus

| | n | Papel |
|---|---:|---|
| Topónimos **con glosa** procesados | **74** | La materia prima: 45 topónimos + 14 antropónimos de [[zavala-reyes-2015]], 15 etimologías comentadas de [[van-buurt-2014]] §8-10 |
| Topónimos **sin glosa**, como control | **244** | 31 de [[gatschet-1885]] (Aruba) + 213 de van Buurt §7 (ABC) |

Los sin glosa no despejan nada: sirven para comprobar **dónde aparece** una
forma, no qué significa.

## Los resultados

| Nivel | n | Qué es |
|---|---:|---|
| **A** | 6 | La ecuación cierra sin residuo, con morfemas ya atestiguados |
| **B** | 8 | Fuerte, pero exige un morfema despejado |
| **C** | 13 | Plausible, recurrencia justa |
| **D** | 47 | Descartado o insuficiente |

- **6 morfemas despejados** — 3 nuevos (`-are`, `ada-`, `yacare`), 3
  corroborados o reagrupados (`-bacoa`, `wa-`, `bari-`). Detalle en
  [[morfologia]] §5.
- **10 palabras del lexicón corroboradas** por vía independiente (6 de ellas
  sin independencia real: la corroboración viene de la misma fuente).
- **La reduplicación**, medida contra tres controles. → [[morfologia]] §4
- **1 antropónimo útil** de los 14.

Que el nivel D sea el mayor (47 de 74) es señal de que el filtro funciona, no de
que el método falle.

## Casos de nivel A

| Topónimo | Glosa de la fuente | Segmentación |
|---|---|---|
| `jurijurebo` | "Paso de los vientos" | `juri~juri` + `ebo` |
| `cumarebo` | "Camino del cacique Cumare" | *Cumare* + `ebo` |
| `yacarebacoa` | "Pueblo del bosque" | `yacare` + `bacoa` |
| `quibacoas` | "Bosques pedregosos" | `quiba` + `(b)acoa`, haplología |
| `guacaubana` | "Río escondido" | `waka` 'subterráneo' + `-ubana` |
| `paraguana` | "Rodeada del mar" | `paragua` 'mar' + `-ana` — **el caso que sostiene `-ana`** ([[morfologia]] §3) |

## Conflictos que la toponimia destapó

`CONFLICTOS` en `lexicon_toponimos.py`. Todos son **homógrafos mal fusionados**:
dos morfemas distintos que colapsan en la misma grafía castellana.

| Caso | Qué pasa |
|---|---|
| `quiba` | El lexicón tiene `quiba` = 'ayuda' (Zavala #203) **y** `quiva`/`cuiva` = 'piedra'. `quibacoas` "Bosques **pedregosos**" y van Buurt §8 (*"siba or quiba means stone"*) apoyan 'piedra'. |
| `guaca` | Lexicón: `guaca` = 'ave, cotorra'. van Buurt §6 vía Oliver: `waka` = 'subterráneo'. `guacaubana` = "Río **escondido**" apoya la segunda. |
| `-are` vs `-ure` | Toponimia: 'sitio de'. van Buurt §5 (Cruz Esteves 1989): 'raíz'. Hermana de D9. |
| `barici` / `bariki` | Dos entradas con glosas solapadas y una raíz probable `bari-` 'rojizo, turbio'. Los topónimos *barisi* y *bariquisimeto* conservan las dos variantes. |

La grafía castellana de las crónicas —`c`/`k`/`qu`, `b`/`v`, `gu`/`w`— es la
causa común. Es el mismo problema que D5, la política ortográfica c/k
([el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision)).

## Por qué esto no toca el lexicón

`lexicon_toponimos.py` **es una propuesta**: `curiana_lexicon.py` no lo importa.
Misma disciplina que las cuatro minerías del 2026-08-03 — el minador emite,
el humano adjudica. Ver [[INDICE_FUENTES]].

## Lo que queda

- Los **213 topónimos ABC de van Buurt §7 sin glosa** son el mayor corpus sin
  explotar: no despejan por sí solos, pero validan formas.
- El [[02_protocolo_habla_paraguanera]] §4 ya decía —antes de F11— que *los
  topónimos son el reservorio más fiable de sustrato*. El protocolo existe; la
  fuente regional de Paraguaná todavía no está en el repo.

## Enlaces

[[morfologia]] · [[lexicon]] · [[metodo-comparativo]] · [[03_descomposicion_toponimica]] · [[zavala-reyes-2015]] · [[gatschet-1885]] · [[van-buurt-2014]] · [[alvarado-1921]]
