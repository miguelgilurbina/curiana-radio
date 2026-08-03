---
tipo: indice-raiz
proyecto: Curiana — proyecto lingüístico caquetío
vault: este mismo repositorio
actualizado: 2026-08-03
---

# Curiana — índice del vault

> **La nota raíz.** Si estás abriendo esto en Obsidian por primera vez, empieza
> aquí. Si lo estás leyendo en GitHub, funciona igual: es markdown.

## Qué es este proyecto

Reconstrucción del **caquetío** —lengua arahuaca extinta del Golfete de Coro,
Venezuela, siglos XIV-XV— y un experimento computacional donde 60 personajes
históricos la hablan y la hacen derivar. Dos mitades:

- **La investigación** — fuentes, corpus cultural, lexicón auditado. *Esto es el
  contenido.*
- **El motor** — la simulación multi-agente que lo pone a hablar. *Hoy
  congelado*: ver la moratoria en [[PLAN_MAESTRO]] §0.

## La regla del vault

> **El vault ES el repositorio.** Nunca un silo paralelo. Git sigue siendo el
> historial; `.obsidian/` y `.trash/` están en `.gitignore` porque son config
> local, no conocimiento.

Obsidian es **una lente**, no la fuente de verdad. El formato es markdown plano
con frontmatter YAML — legible por VS Code, Foam, SilverBullet o `cat`. La lógica
crítica (validación del corpus) vivirá en `compilar_corpus.py`, **nunca en
plugins** ([[PLAN_MAESTRO]] §2).

Para abrirlo: en Obsidian, *Open folder as vault* → esta carpeta
(`proyecto-linguistico-caquetío/`).

## Por dónde entrar

### Los mapas (MOC)

Uno por pregunta del programa cultural, más uno del código:

| MOC | Pregunta | Hechos |
|---|---|---|
| [[MOC_familia]] | ¿Cómo era la familia caquetía? | 39 |
| [[MOC_ecologia]] | ¿Dónde existía el caquetío? | 54 |
| [[MOC_creencia]] | ¿En qué creía? | 26 |
| [[MOC_transmision]] | ¿Cómo sabía lo que sabía? | 34 |
| [[MOC_geografia_politica]] | ¿Cuál era el mundo de Manaure? | 8 |
| [[MOC_motor]] | El código, el lexicón y los runs | — |

### Las notas de trabajo

- 📋 [[PLAN_MAESTRO]] — la hoja de ruta. Los 4 ejes: FIDELIDAD, VAULT, JARDÍN,
  MOTOR. **Fuente de verdad del backlog.**
- ⚖️ [[DECISIONES_ABIERTAS]] — lo que solo Miguel puede decidir. **9 abiertas**, dos de fondo (D10, D11).
- 📚 [[INDICE_FUENTES]] — estado **medido** de las 24 obras: qué se puede leer,
  qué está minado, qué sostiene cada una.
- 🕰️ [[LINEA_DE_TIEMPO]] — las cuatro eras del proyecto y sobre qué base corrió
  cada cosa. Necesaria para saber qué resultados siguen valiendo.
- 🔬 [[01_que_probaron_los_seis_runs]] — el análisis de los runs existentes:
  qué probaron, qué no, y por qué no son comparables.
- 🧪 [[04_protocolo_run_1_era_auditada]] — cómo se corre y se mide la próxima
  simulación para que sí sea analizable.

## El territorio

```
proyecto-linguistico-caquetío/          ← raíz del vault
├── INDICE.md                            ← estás aquí
├── PLAN_MAESTRO.md · DECISIONES_ABIERTAS.md
├── CANON_TIERRA.md · DISENO_KOINE.md · BITACORA_RUNS.md · …
├── mocs/                                ← los 6 mapas de contenido
├── investigacion/
│   ├── ensayos/          ← los 5 mini-ensayos (el argumento)
│   ├── hojas_fuentes/    ← qué se buscó, qué se halló, qué quedó abierto
│   ├── disenos/          ← biosfera, motor ambiental, protocolo paraguanero
│   ├── fuentes/          ← una nota por obra + INDICE_FUENTES
│   └── PROGRAMA_WAYUU.md
├── fuentes_caquetios/                   ← los PDF (no se editan, se citan)
└── curiana_sim/
    ├── cultura/          ← el corpus: 161 hechos en YAML + genealogía
    ├── curiana_*.py      ← el motor
    └── tests/            ← 45 tests, el guardián
```

## Las cinco etiquetas epistémicas

Todo hecho del corpus lleva una, y **en duda se degrada a la más débil**:

| Etiqueta | Significa | n |
|---|---|---|
| `atestiguado` | crónica o trabajo académico con cita concreta | 78 |
| `reconstruido` | inferencia razonada con comparanda citada | 55 |
| `canon-simulacion` | dato del propio elenco/mundo ya establecido | 14 |
| `hipotetico` | plausible, sin respaldo — licencia narrativa | 10 |
| `retro-abstraido` | tradición viva posterior; **nunca asciende** | 4 |

El lexicón usa su propia escala paralela: `caquetío-atestiguado` (231),
`caquetío-reconstruido` (68) e `hipotético-no-verificado` (441, **aisladas** en
`lexicon_candidatos.py` con ~80% de fallo medido — de las que la minería de
[[oliver-1989-cap2]] hace **82 adjudicables**).

## Estado, medido el 2026-08-03

| | |
|---|---|
| Corpus cultural | **161 hechos**, todos con `referencia` |
| Lexicón activo | **1414** palabras · 312 de familia caquetía · **19 sin cita** (eran 82) |
| Fuentes | 24 obras · **6 archivos de 0 bytes** · **las 3 ALTA del gate, minadas** |
| Motor | **45 tests en verde**, congelado |
| Runs | 6, declarados **era de desarrollo** — ver [[01_que_probaron_los_seis_runs]] |
| Decisiones | **9 abiertas**, 2 resueltas |

> Las 19 entradas sin cita que quedan **ya no son deuda de minería sino de
> decisión**: 13 que una fuente reclasifica a otra lengua y 3 conflictos de
> glosa esperan a [[DECISIONES_ABIERTAS|D10]]; 3 no dejan rastro en ninguna
> fuente.

## Convenciones

- **Enlaces**: `[[alvarado-1921]]` — el nombre del archivo, sin extensión, entre
  dobles corchetes. Obsidian los resuelve en
  todo el vault; los nombres de archivo son únicos a propósito.
- **Frontmatter**: cada nota declara su `tipo` (`moc`, `fuente`, `ensayo`,
  `nota-viva`, `indice`). Las de fuente añaden `estado_minado`, `prioridad`,
  `tareas` y `sostiene`.
- **Un hallazgo se escribe donde vive su objeto**: si F3 mina Alvarado, el
  resultado se escribe en [[alvarado-1921]], no en un markdown nuevo. Ese es el
  punto del vault entero.
- **Los números se miden, no se recuerdan.** Toda cifra de estas notas lleva
  fecha de medición.

## Enlaces

[[PLAN_MAESTRO]] · [[DECISIONES_ABIERTAS]] · [[INDICE_FUENTES]] ·
[[MOC_familia]] · [[MOC_ecologia]] · [[MOC_creencia]] · [[MOC_transmision]] ·
[[MOC_geografia_politica]] · [[MOC_motor]]
