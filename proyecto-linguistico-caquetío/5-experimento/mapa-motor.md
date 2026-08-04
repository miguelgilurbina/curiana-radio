---
tipo: moc
ambito: motor de simulación, lexicón y runs
estado: congelado — moratoria de simulaciones vigente
tests: 45 (en verde, verificado 2026-07-29)
lexicon_activo: 1416
medido: 2026-07-29
---

# MOC — El motor, el lexicón y los runs

> Mapa de contenido de la parte que **sí es código**. El motor está congelado
> (sano, testeado) y las simulaciones en pausa: ver [[PLAN_MAESTRO]] §0 y §4.
> Este MOC existe para que el vault no sea solo la mitad cultural del proyecto.

## Estado medido (2026-07-29)

| Métrica | Valor | Cómo se midió |
|---|---|---|
| Tests | **45, todos en verde** | `python -m pytest tests/ -q` |
| Lexicón activo | **1416** palabras | `len(VOCABULARIO_BASE)` |
| Familia caquetía | **314** entradas | `fuente` que contiene "caquet" |
| …de ellas **sin `notas`** | **82 (26%)** | el corazón de F1 |
| Valores distintos de `fuente` (dato crudo) | **21** | la doc declara 8 categorías normalizadas |
| Colisiones c/k/qu | **10** | 1 es falso positivo: `coro` (cardón) ≠ `koro` (cotorra) |
| Corpus cultural | **161 hechos**, 0 sin `referencia` | 78 atestiguado · 55 reconstruido · 14 canon-simulación · 10 hipotético · 4 retro-abstraído |
| Runs curados | 6 (1489 respuestas) | [[BITACORA_RUNS]] |

## Las piezas del motor

| Módulo | Qué hace |
|---|---|
| `curiana_orchestrator_v2.py` | Orquestador principal; un Haiku por agente; rescate intra-turno |
| `curiana_agents.py` | 60 agentes históricos en 3 tiers |
| `curiana_lexicon.py` | Vocabulario + morfología + prompts + `score_linguistico()` |
| `curiana_koine.py` | `IdiolectoAgente`, `CampoLexico`, `CompetenciaLexica` → [[DISENO_KOINE]] |
| `curiana_social.py` | `DifusionLexica` (prestigio × vínculo × co-ubicación), variación dialectal |
| `curiana_state.py` | Día, estación, eventos, locaciones |
| `curiana_observer.py` | Análisis lingüístico, scoring 0-10, neologismos, perfiles curados |
| `curiana_database.py` | Supabase + LangSmith + `normalize_source_language()` |
| `arahuaco_comparative.py` | Método comparativo: `COGNADOS` (37), transducción, validación |

## Documentos de diseño

- [[DISENO_KOINE]] — la dirección conceptual (Maturana, Cynefin, el emocionar);
  el arco diverso → converge, y las 3 lecturas de convergencia.
- [[CANON_TIERRA]] — ritos como mecanismo de transmisión; opciones A/B; el hueco
  de envejecimiento. Su marco teórico está en [[04_transmision_saber]].
- [[IDEA_PERFILES_AGENTES]] — perfiles curados por agente (`--perfiles`).
- [[MIGRACION_RUNS_EVOLUCION]] — índice cross-run para el sitio estático.
- [[ANALISIS_RUN_30T_2026-06-22]] · [[BITACORA_RUNS]] — qué produjeron los runs.

## La epistemología del lexicón

Ocho categorías activas de `fuente` tras normalizar. Las tres que importan:

- **`caquetío-atestiguado` (233)** — dato citable. Pero: **164 de esas entradas
  citan a [[zavala-reyes-2015]]** y prácticamente nadie más. [[alvarado-1921]],
  [[van-buurt-2014]] y [[gatschet-1885]] tienen **0 entradas que los citen**,
  pese a figurar como fuentes del proyecto.
- **`caquetío-reconstruido` (68)** — el núcleo fundacional que los prompts
  presentan a los agentes desde el día 1.
- **`hipotético-no-verificado` (441)** — **aisladas** en `lexicon_candidatos.py`
  desde 2026-06-28: transducciones fonológicas sin verificar cognación, con ~80%
  de fallo medido. No se siembran ni se importan.

> ⚠️ Queries a la tabla `lexicon`: PostgREST corta en 1000 filas. Con 1416
> palabras, toda query nueva sin `.range()` se trunca en silencio.

## Las decisiones congeladas

- **M1 / D3** — `normalizar_por_dialecto()`: cablearla o eliminarla.
- **M2** — persistencia de efectos sin decaimiento (la sal abundante se queda
  abundante para siempre).
- **D5** — política ortográfica c/k del lexicón (10 colisiones medidas).

Todas en [[DECISIONES_ABIERTAS]].

## Lo que el corpus le pide al motor y todavía no existe

- **Tabla de eventos rituales en el Observer** (paralela a `neologisms`) y la
  métrica de **eco por rol** — el experimento Bana-mana de [[mapa-transmision]].
- **`forma_transmision`** como etiqueta que module la métrica de fidelidad.
- **`compilar_corpus.py`** — validador del corpus cultural (V2 del plan). Hoy
  **nada valida** los 161 hechos: es el equivalente cultural de estos 45 tests.
- Los **9 huecos léxicos** de [[mapa-ecologia]] como candidatos sembrables.
- Los bloques `rol_*` componibles de [[mapa-familia]] §6.6.

## El gate

Las simulaciones se reanudan cuando se cumplan **todas** las condiciones de
[[PLAN_MAESTRO]] §6. El re-export del sitio se hará solo desde el primer run
post-auditoría: los 6 runs actuales quedan como material de desarrollo del motor.
