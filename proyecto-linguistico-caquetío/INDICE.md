---
tipo: indice-raiz
proyecto: Curiana — proyecto lingüístico caquetío
vault: este mismo repositorio
actualizado: 2026-07-29
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
- ⚖️ [[DECISIONES_ABIERTAS]] — lo que solo Miguel puede decidir. 7 abiertas.
- 📚 [[INDICE_FUENTES]] — estado **medido** de las 24 obras: qué se puede leer,
  qué está minado, qué sostiene cada una.

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

El lexicón usa su propia escala paralela: `caquetío-atestiguado` (233),
`caquetío-reconstruido` (68) e `hipotético-no-verificado` (441, **aisladas** en
`lexicon_candidatos.py` con ~80% de fallo medido).

## Estado, medido el 2026-07-29

| | |
|---|---|
| Corpus cultural | **161 hechos**, todos con `referencia` |
| Lexicón activo | **1416** palabras · 314 de familia caquetía · **82 sin cita (26%)** |
| Fuentes | 24 obras · **6 archivos de 0 bytes** · 4 sin minar de prioridad ALTA |
| Motor | **45 tests en verde**, congelado |
| Runs | 6 curados (1489 respuestas), **pre-auditoría** |

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
