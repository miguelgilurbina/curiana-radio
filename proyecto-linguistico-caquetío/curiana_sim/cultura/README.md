# `curiana_sim/cultura/` — Corpus cultural caquetío

Corpus de hechos culturales etiquetados por confianza epistémica, en el
mismo espíritu que el lexicón distingue `caquetío-atestiguado` de
`hipotético-no-verificado` (ver `CLAUDE.md`). Cada archivo YAML es la
salida de una sesión de investigación del programa "corpus cultural";
los ensayos y hojas de fuentes que los respaldan viven en
`investigacion/ensayos/` e `investigacion/hojas_fuentes/` en la raíz del
proyecto.

## Esquema común

```yaml
- id: <dominio>-NNN
  contenido: >
    El hecho, 1-4 frases.
  fuente: atestiguado | reconstruido | retro-abstraido | hipotetico
  referencia: "cita concreta (autor+año, o CANON_TIERRA.md / curiana_agents.py)"
  dominios: [lista, de, dominios]
  agentes_relacionados: [Nombre-Agente, ...]
  implicacion_simulacion: >
    Opcional. Qué implica esto para el diseño de la simulación.
```

Etiquetas de `fuente` (degradar en caso de duda):

- **atestiguado** — fuente concreta citada (crónica, trabajo académico).
- **reconstruido** — comparativa arahuaca u otra sociedad oral, comparanda
  citada explícitamente.
- **retro-abstraido** — inferido desde el propio elenco/canon del
  proyecto (p. ej. `curiana_agents.py`) o desde tradición viva posterior /
  intuición local de Paraguaná, sin fuente académica directa.
- **hipotetico** — plausible pero sin respaldo.

## Índice de archivos

- [`transmision.yaml`](transmision.yaml) — Sesión 4: transmisión oral del
  saber. Currículo por edad, formas de transmisión y su fidelidad
  diferencial, saberes restringidos vs. abiertos, puntos únicos de falla
  del elenco (Bana-mana, Tari-ko, Nubiri-sha...), comparanda wayuu
  (jayeechi, ouutsü/Lapü) y teoría de oralidad (Vansina, Ong). Ensayo:
  `investigacion/ensayos/04_transmision_saber.md`.

*(Las sesiones 1-3 del programa "corpus cultural" —familia, ecología,
creencia— aún no tienen archivo en este índice al momento de escribir
esto; añadir aquí cuando se creen.)*
