# `curiana_sim/cultura/` — Corpus cultural caquetío

Corpus de hechos culturales etiquetados por confianza epistémica, en el mismo espíritu con que el
lexicón distingue `caquetío-atestiguado` de `hipotético-no-verificado` (ver `CLAUDE.md`). Complementa
la guía narrativa en prosa `curiana_sim/CULTURA_CAQUETIA.md` con datos discretos y auditables.

Es el producto del programa **"corpus cultural"** (4 sesiones de investigación, 2026-07), cada una
guiada por una pregunta y con tres entregables: un mini-ensayo (`investigacion/ensayos/`), un archivo
YAML aquí, y una hoja de fuentes (`investigacion/hojas_fuentes/`).

Estos archivos son **datos de propuesta / referencia de diseño**: no se cargan (todavía) desde ningún
script de la simulación. Su función es (1) anclar prompts, escenas y eventos en hechos verificables;
(2) enlazar cada hecho con la locación de `curiana_state.py` y la palabra de `curiana_lexicon.py` que
le corresponde; y (3) **localizar los huecos léxicos** — fenómenos que la comunidad vive sin tener
palabra para ellos, candidatos naturales a neologismo emergente. La genealogía y las relaciones
propuestas requieren revisión/veto de Miguel antes de volverse canon.

## Índice

| Archivo | Sesión | Pregunta guía | Entregables asociados |
|---|---|---|---|
| [`parentesco.yaml`](parentesco.yaml) | 1/4 — Familia | ¿Cómo era la familia caquetía? Matrilinealidad, matrimonio, sucesión, sociedades masculinas | [ensayo](../../investigacion/ensayos/01_familia_caquetia.md) · [fuentes](../../investigacion/hojas_fuentes/01_familia.md) |
| [`genealogia.yaml`](genealogia.yaml) | 1/4 — Familia | Propuesta de árbol genealógico para los 60 agentes + personas de fondo | (mismos de la sesión 1) |
| [`ecologia.yaml`](ecologia.yaml) | 2/4 — Ecología | ¿Dónde existía el caquetío? Medio físico, geografía e hidrología del Golfete de Coro | [ensayo](../../investigacion/ensayos/02_ecologia_golfete.md) · [fuentes](../../investigacion/hojas_fuentes/02_ecologia.md) |
| [`creencia.yaml`](creencia.yaml) | 3/4 — Creencia | ¿En qué creía el caquetío? Religión, muerte, piache, sistema onírico | [ensayo](../../investigacion/ensayos/03_creencia_caquetia.md) · [fuentes](../../investigacion/hojas_fuentes/03_creencia.md) |
| [`transmision.yaml`](transmision.yaml) | 4/4 — Transmisión | ¿Cómo sabía lo que sabía? Currículo por edad, formas de transmisión, saberes restringidos, puntos únicos de falla | [ensayo](../../investigacion/ensayos/04_transmision_saber.md) · [fuentes](../../investigacion/hojas_fuentes/04_transmision.md) |

### Documentos de apoyo de la sesión 2 (ecología)

- [`ecologia_lexicon_map.md`](ecologia_lexicon_map.md) — cross-check exhaustivo especie/rasgo
  → palabra caquetía → estado (caquetío / forma hermana / **hueco léxico**), con los huecos
  léxicos ordenados por presión. Señala falsos amigos (p. ej. `duna` = *agua*).
- [`../../investigacion/disenos/02_motor_ambiental.md`](../../investigacion/disenos/02_motor_ambiental.md)
  — pseudo-diseño del motor ambiental / agentes ecológicos (variables de estado, cadenas
  causales, tres capas de traducción). Solo diseño; no toca código.
- [`../../investigacion/disenos/02_capas_biosfera.md`](../../investigacion/disenos/02_capas_biosfera.md)
  — modelo de **capas de biosfera**: el escenario (geomorfología, clima) es constante desde
  ~4000 BP, pero el elenco animal se vació después del s. XV. Cinco capas, de la extinción
  global (foca monje del Caribe) al censo actual, con la regla de inferencia y su límite.
- [`../../investigacion/disenos/02_protocolo_habla_paraguanera.md`](../../investigacion/disenos/02_protocolo_habla_paraguanera.md)
  — protocolo para minar léxicos regionales paraguaneros y **medir la factibilidad** de que
  una voz sea sustrato caquetío (6 filtros de descarte, 6 criterios positivos, escala A–D).
  **La fuente aún no está en el repo**; el protocolo se escribió por adelantado.

### Documentos de apoyo de la sesión 4 (transmisión)

- [`../../investigacion/PROGRAMA_WAYUU.md`](../../investigacion/PROGRAMA_WAYUU.md) — programa de
  investigación aparte levantado por la sesión 4 (pregunta Manaure-palabrero; comparanda: sistema
  normativo wayuu, cuadernillo de Guerra Curvelo en `fuentes_caquetios/`).

## Esquema de cada entrada

```yaml
- id: <dominio>-NNN            # id estable, único dentro del archivo
  contenido: >
    El hecho cultural, 1-4 frases.
  fuente: atestiguado | reconstruido | canon-simulacion | retro-abstraido | hipotetico
  referencia: "Oliver 1989, cap. 3" / "Perrin 1995, analogía wayuu" / "curiana_agents.py (Shaboro)"
  dominios: [creencia, muerte]                # ejes temáticos libres
  agentes_relacionados: [Shaboro, Buio-sha]   # nombres de curiana_agents.py
  implicacion_simulacion: >                   # opcional
    Cómo debería reflejarse en prompts o mecánica.
```

Campos adicionales según el dominio: `palabra_lexicon` y `locacion` (ecología; `hueco_lexico: true`
marca fenómeno sin palabra caquetía), `forma_transmision` y `restringido` (transmisión). El esquema
de `genealogia.yaml` es distinto (un registro por persona, con `relaciones_atestiguadas_en_descripcion`
vs. `relaciones_propuestas`) — ver el propio archivo.

## Las cinco etiquetas de `fuente`

- **`atestiguado`** — citable a una fuente concreta con página/capítulo: crónica colonial, trabajo
  académico o (en ecología) ciencia natural moderna. El nivel más fuerte.
- **`reconstruido`** — inferido por método comparativo desde un pueblo arahuaco hermano (wayuu,
  lokono, taíno) u otra sociedad oral, con la comparanda y su fuente citadas en `referencia`.
- **`canon-simulacion`** — hecho establecido por diseño del propio proyecto (`curiana_agents.py`,
  `curiana_state.py`, `CULTURA_CAQUETIA.md`, `CANON_TIERRA.md`), sin pretensión histórica directa.
  Es el equivalente cultural del `caquetío-reconstruido` "vocabulario de trabajo" del lexicón: no es
  dato etnohistórico, es la ficción operativa de la simulación, y se marca como tal.
- **`retro-abstraido`** — traza inferida desde una **tradición viva posterior** (espiritismo
  venezolano / culto de María Lionza, cultura popular falconiana) o intuición local informada de
  Paraguaná. NUNCA se asciende a `reconstruido`.
- **`hipotetico`** — licencia narrativa plausible, sin respaldo documental ni comparativo directo.
  El nivel más débil.

Reglas: **una sola etiqueta por entrada; en duda, degradar a la más débil.** La frontera
`reconstruido`/`retro-abstraido` debe quedar impecable, y `canon-simulacion` existe precisamente
para que el canon interno nunca se disfrace de ninguna de las otras dos.

> Nota histórica: la sesión 4 etiquetó originalmente sus hechos de elenco como `retro-abstraido`;
> se reetiquetaron a `canon-simulacion` al consolidar (2026-07), y la categoría se añadió al esquema.

## Convenciones

- Todo en español.
- Estos YAML no tocan el código Python ni la app Next.js; son documentación estructurada.
- Nunca escribir API keys, tokens ni secretos en archivos de este proyecto — ni siquiera
  gitignored — porque el repo sincroniza a OneDrive.
