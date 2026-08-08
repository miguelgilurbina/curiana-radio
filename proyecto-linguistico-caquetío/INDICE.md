---
tipo: indice-raiz
proyecto: Curiana — proyecto lingüístico caquetío
vault: este mismo repositorio
actualizado: 2026-08-06
---

# Curiana — índice del vault

> **La nota raíz.** Si estás abriendo esto en Obsidian por primera vez, empieza
> aquí. Si lo estás leyendo en GitHub, funciona igual: es markdown.

## Qué es este proyecto

Reconstrucción del **caquetío** —lengua arahuaca extinta del Golfete de Coro,
Venezuela, siglos XIV-XV— y un experimento computacional donde 60 personajes
históricos la hablan y la hacen derivar.

## Las cinco carpetas, cinco preguntas

El vault está ordenado por **la pregunta que responde cada carpeta**, no por
tipo de archivo. Si no sabes dónde va algo, pregúntate qué pregunta contesta.

| Carpeta | Pregunta | Entra por |
|---|---|---|
| **`1-plan/`** | ¿Qué hacemos y qué falta? | [[PLAN_MAESTRO]] |
| **`2-lengua/`** | ¿Cómo es el caquetío? | [[mapa-lengua]] |
| **`3-mundo/`** | ¿Cómo era ese pueblo? | los cinco mapas de abajo |
| **`4-fuentes/`** | ¿De dónde lo sabemos? | [[INDICE_FUENTES]] |
| **`5-experimento/`** | ¿Qué probamos con el simulador? | [[mapa-motor]] |

Fuera de esa numeración solo hay tres cosas, y las tres son herramienta, no
conocimiento: `curiana_sim/` (el código), `fuentes_caquetios/` (los PDF, que se
citan y no se editan) y `supabase/` (el esquema).

## Los mapas

Un mapa es un **índice de navegación**: te dice qué hay y dónde. No es un
ensayo. Los ensayos —el argumento, con su evidencia— viven en
`3-mundo/ensayos/`, y cada mapa enlaza al suyo.

| Mapa | Pregunta | Hechos |
|---|---|---|
| [[mapa-lengua]] | ¿Cómo es el caquetío? | 1413 palabras |
| [[mapa-familia]] | ¿Cómo era la familia caquetía? | 39 |
| [[mapa-ecologia]] | ¿Dónde existía el caquetío? | 54 |
| [[mapa-creencia]] | ¿En qué creía? | 26 |
| [[mapa-transmision]] | ¿Cómo sabía lo que sabía? | 34 |
| [[mapa-geografia-politica]] | ¿Cuál era el mundo de Manaure? | 8 |
| [[polities-caquetias]] | ¿Cuántos caquetíos había, y cuál simulamos? | 4 polities |
| [[horizonte-de-contacto]] | ¿Hasta dónde llegaba su mundo? ¿Tocó a los mayas? | prospección |
| [[mapa-motor]] | El código, los tests y los runs | — |

## Las notas de trabajo

- 🌙 [[SIGUIENTE_TANDA]] — **qué lanzar en la próxima tanda de trabajo
  desatendido, y cómo se encarga.** Empieza por aquí si arrancas en frío.
- 📋 [[PLAN_MAESTRO]] — la hoja de ruta. Los 4 ejes: FIDELIDAD, VAULT, JARDÍN,
  MOTOR. **Fuente de verdad del backlog.**
- ⚖️ [Decisiones abiertas](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) — lo que solo Miguel puede decidir, en el
  tablero de GitHub. Cada una lleva su argumento y su evidencia dentro; ya no
  hay nota en el repo que las duplique.
- 🔧 [[HARNESS]] — cómo se trabaja aquí y por qué; los guardianes.
- 🏗️ [[ARQUITECTURA]] — el motor medido: 50 módulos, dónde va a doler.
- 📚 [[INDICE_FUENTES]] — estado **medido** de las obras: qué se puede leer, qué
  está minado, qué sostiene cada una.
- 🕰️ [[LINEA_DE_TIEMPO]] — las cuatro eras del proyecto y sobre qué base corrió
  cada cosa. Necesaria para saber qué resultados siguen valiendo.
- 🔬 [[01_que_probaron_los_seis_runs]] — qué probaron los runs existentes, qué
  no, y por qué no son comparables.
- 🧪 [[04_protocolo_run_1_era_auditada]] — cómo se corre y se mide la próxima
  simulación para que sí sea analizable.

## El territorio

```
proyecto-linguistico-caquetío/          ← raíz del vault
├── INDICE.md                            ← estás aquí
├── CLAUDE.md · check_vault_links.py     ← config y guardián del grafo
│
├── 1-plan/          ¿qué hacemos y qué falta?
│   └── PLAN_MAESTRO · LINEA_DE_TIEMPO · SIGUIENTE_TANDA · HARNESS
│
├── 2-lengua/        ¿cómo es el caquetío?
│   └── mapa-lengua · lexicon · morfologia · toponimia · metodo-comparativo
│
├── 3-mundo/         ¿cómo era ese pueblo?
│   ├── mapa-familia · mapa-ecologia · mapa-creencia · mapa-transmision
│   │   · mapa-geografia-politica · polities-caquetias
│   ├── CULTURA_CAQUETIA.md  ← el canon narrativo: cómo se vivía ahí
│   ├── ensayos/     ← los 5 mini-ensayos (el argumento, no el índice)
│   └── corpus/      ← 161 hechos en YAML + genealogía
│
├── 4-fuentes/       ¿de dónde lo sabemos?
│   ├── INDICE_FUENTES + una nota por obra (30)
│   └── sesiones/    ← bitácoras: qué se buscó, qué se halló, qué quedó abierto
│
├── 5-experimento/   ¿qué probamos con el simulador?
│   ├── mapa-motor · ARQUITECTURA · DISENO_KOINE · CANON_TIERRA · …
│   ├── analisis/    ← qué produjeron los runs
│   └── disenos/     ← biosfera, motor ambiental, toponimia, protocolos
│
├── fuentes_caquetios/    ← los PDF (no se editan, se citan)
├── curiana_sim/          ← el motor + 125 tests, los guardianes
└── supabase/             ← el esquema versionado
```

## La regla del vault

> **El vault ES el repositorio.** Nunca un silo paralelo. Git sigue siendo el
> historial; `.obsidian/` y `.trash/` están en `.gitignore` porque son config
> local, no conocimiento.

Obsidian es **una lente**, no la fuente de verdad. El formato es markdown plano
con frontmatter YAML — legible por VS Code, Foam, SilverBullet o `cat`. La
lógica crítica (validación del corpus) vivirá en `compilar_corpus.py`, **nunca
en plugins** ([[PLAN_MAESTRO]] §2).

Para abrirlo: en Obsidian, *Open folder as vault* → esta carpeta.

## Las cinco etiquetas epistémicas

Todo hecho del corpus lleva una, y **en duda se degrada a la más débil**:

| Etiqueta | Significa | n |
|---|---|---|
| `atestiguado` | crónica o trabajo académico con cita concreta | 78 |
| `reconstruido` | inferencia razonada con comparanda citada | 55 |
| `canon-simulacion` | dato del propio elenco/mundo ya establecido | 14 |
| `hipotetico` | plausible, sin respaldo — licencia narrativa | 10 |
| `retro-abstraido` | tradición viva posterior; **nunca asciende** | 4 |

El lexicón usa su propia escala paralela — `caquetío-atestiguado` (226),
`caquetío-reconstruido` (68) e `hipotético-no-verificado` (441, **aisladas** en
`lexicon_candidatos.py`). Ver [[lexicon]].

## Estado

> 📊 **El estado vive en [[TABLERO]], y se genera.** Ninguna cifra se copia a
> mano: `python curiana_sim/generar_tablero.py` las mide contra el dato —
> lexicón, corpus, frontmatter de las fuentes, gate y decisiones— y reescribe
> `TABLERO.md` con la fecha de medición.

Los tres números que resumen el momento (medidos el 2026-08-06):

- **3 entradas del lexicón sin cita**, de las 82 que había el 2026-07-21. Las
  que quedan ya no son deuda de minería sino de decisión: no dejan rastro en
  ninguna de las cuatro fuentes minadas.
- **161 hechos del corpus, los 161 con `referencia`.**
- **2 de las 9 condiciones del gate** para reanudar simulaciones. El resto,
  con su porqué, en [[TABLERO]] §4.

## Convenciones

- **Enlaces**: `[[alvarado-1921]]` — el nombre del archivo, sin extensión, entre
  dobles corchetes. Obsidian los resuelve en todo el vault; los nombres de
  archivo son únicos a propósito, **así que mover una nota no rompe enlaces**.
- **Frontmatter**: cada nota declara su `tipo` (`moc`, `fuente`, `ensayo`,
  `nota-viva`, `indice`, `diseño`). Las de fuente añaden `estado_minado`,
  `prioridad`, `tareas` y `sostiene`.
- **Mapa ≠ ensayo.** Un mapa navega; un ensayo argumenta. Si un mapa empieza a
  argumentar, el argumento se muda a `3-mundo/ensayos/`.
- **Un hallazgo se escribe donde vive su objeto**: si se mina Alvarado, el
  resultado va en [[alvarado-1921]], no en un markdown nuevo. Ese es el punto
  del vault entero.
- **Los números se miden, no se recuerdan.** Toda cifra lleva fecha de medición.

## Enlaces

[[PLAN_MAESTRO]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) · [[LINEA_DE_TIEMPO]]
