# `cultura/` — Corpus cultural caquetío

Corpus estructurado (YAML) que da sustancia etnográfica y ecológica a la simulación
de la Curiana. Es el producto del programa **«corpus cultural»** (4 sesiones de
investigación), cada una guiada por una pregunta y con tres entregables: un
mini-ensayo (`investigacion/ensayos/`), un archivo YAML aquí, y una hoja de fuentes
(`investigacion/hojas_fuentes/`).

Estos archivos son **datos de referencia para el diseño**, no se cargan (todavía) en
el orquestador. Su función es: (1) anclar los prompts de escena y los eventos en
hechos verificables; (2) enlazar cada hecho con la locación de `curiana_state.py` y la
palabra de `curiana_lexicon.py` que le corresponde; y (3) **localizar los huecos
léxicos** — fenómenos que la comunidad vive sin tener palabra para ellos, que son los
candidatos naturales a neologismo emergente en la simulación.

## Índice

| Archivo | Pregunta guía | Ensayo |
|---|---|---|
| [`ecologia.yaml`](ecologia.yaml) | ¿Dónde existía el caquetío? El medio físico, geografía e hidrología del Golfete de Coro | [`02_ecologia_golfete.md`](../../investigacion/ensayos/02_ecologia_golfete.md) |

*(Las demás sesiones del programa añadirán sus archivos a esta tabla.)*

### Documentos de apoyo de la sesión 02 (ecología)

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

## Esquema de cada entrada

```yaml
- id: <dominio>-NNN
  contenido: >
    El hecho, 1–4 frases.
  fuente: atestiguado | reconstruido | retro-abstraido | hipotetico
  referencia: "Autor Año, p. XX"          # fuente concreta
  dominios: [ecologia, pesca]              # ejes temáticos
  agentes_relacionados: [Bagre-ko, Dara-ko]
  palabra_lexicon: cunaro                  # forma caquetía existente; null si es hueco léxico
  locacion: manglar                        # locación de curiana_state.py, si aplica
  implicacion_simulacion: >                # opcional
    Cómo debería influir en la simulación.
```

Al final de cada archivo, una sección `huecos_lexicos:` reúne las entradas marcadas
`hueco_lexico: true` — fenómenos importantes del paisaje/cultura **sin palabra** en el
lexicón.

## Marcas de `fuente` (metodología idéntica en las 4 sesiones)

- **`atestiguado`** — citable a una fuente concreta. Para ecología, incluye ciencia
  natural moderna citada (geomorfología, climatología, ictiofauna, arqueología).
- **`reconstruido`** — inferencia razonada, p. ej. proyectar la ecología actual 600
  años hacia atrás con los cambios conocidos.
- **`retro-abstraido`** — tradición viva local / intuición informada de Paraguaná o Coro.
- **`hipotetico`** — plausible sin respaldo.

Regla: **en duda, degradar a la marca más débil.**

## Convenciones

- Todo en español.
- No se escriben API keys ni secretos en estos archivos (el repo sincroniza a OneDrive).
- Estos YAML no tocan el código Python ni la app Next.js; son documentación estructurada.
