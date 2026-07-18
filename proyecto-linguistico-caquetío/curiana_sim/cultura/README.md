# curiana_sim/cultura/ — Corpus cultural estructurado

Corpus YAML de hechos culturales caquetíos, producido por el programa de 4
sesiones de investigación "corpus cultural". Complementa la guía en prosa
`curiana_sim/CULTURA_CAQUETIA.md` con datos discretos, etiquetados por
fiabilidad, pensados para alimentar prompts, ambientación y eventos de la
simulación sin mezclar dato con especulación.

Cada sesión de investigación produce tres entregables:
- un mini-ensayo en `investigacion/ensayos/`,
- un archivo YAML aquí en `cultura/`,
- una hoja de fuentes en `investigacion/hojas_fuentes/`.

## Esquema de cada entrada YAML

```yaml
- id: <dominio>-001            # id estable, único dentro del archivo
  contenido: >
    El hecho, 1-4 frases.
  fuente: atestiguado | reconstruido | retro-abstraido | hipotetico
  referencia: "Pollak-Eltz 1972" / "Perrin 1995, analogía wayuu" / "crónica: Oviedo t. IV"
  dominios: [creencia, muerte]         # etiquetas temáticas libres
  agentes_relacionados: [Shaboro, Buio-sha]   # nombres de curiana_agents.py
  implicacion_simulacion: >
    Opcional: cómo usar esto en la simulación.
```

## Metodología de etiquetado (idéntica en las 4 sesiones)

- **`atestiguado`** — crónica colonial o trabajo académico con cita concreta.
- **`reconstruido`** — inferencia por comparación arahuaca (wayuu, lokono, taíno…)
  con la comparanda citada.
- **`retro-abstraido`** — traza inferida desde una tradición viva posterior (p.ej.
  el culto de María Lionza) o intuición local; NUNCA se asciende a `reconstruido`.
- **`hipotetico`** — plausible pero sin respaldo.

Regla de oro: **en duda, degradar**. La frontera `reconstruido`/`retro-abstraido`
debe quedar impecable.

## Índice de archivos

| Archivo | Sesión | Tema | Entregables asociados |
|---|---|---|---|
| [`creencia.yaml`](creencia.yaml) | 03 | Religión, muerte, piache, sistema onírico | [ensayo](../../investigacion/ensayos/03_creencia_caquetia.md) · [fuentes](../../investigacion/hojas_fuentes/03_creencia.md) |

*(Las sesiones 01, 02 y 04 añadirán sus archivos a esta tabla.)*
