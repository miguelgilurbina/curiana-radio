# Migración de runs → página estática: mostrar la evolución entre simulaciones

Diseño de trabajo para la rama `feat/migracion-runs-evolucion`. El objetivo no
es solo migrar más datos: es darle a `/simulador` una **dimensión temporal
entre runs**, para contar el arco del proyecto (caquetío 8% → 92% → 99%; deriva
plana → koiné con diccionario → experimento de control) en vez de una sola foto.

## El problema

Hoy `/simulador` muestra **un solo run** (`2e729f3f`, del 22-jun, pre-koiné):

- La capa **editorial** (`content/simulador/editorial.json` + `lib/editorial.ts`)
  ya es multi-run: tiene `runs[]`, `run_activo`, y la validación reconoce que
  "runs futuros traerán sus propios seeds".
- Pero la capa de **datos** es de un solo run: `resumen.json`, `personajes.json`,
  `neologismos.json` son singulares — cada `export_*_seed.py` los **sobreescribe**.
  Solo puede vivir el detalle de un run a la vez.
- No hay **nada cross-run**: ni la convergencia, ni la fijación, ni la evolución
  del caquetío se pueden comparar entre simulaciones porque no existe una
  estructura que las junte.

Además, dos tipos de dato de la era koiné no tienen representación en la página:
`koine_metrics` (curvas de convergencia) y `koine_lexicon` (el diccionario
emergente — el resultado más contable del proyecto).

## La estrategia: índice cross-run + detalle por run

Dos capas nuevas, bien separadas:

### 1. Índice cross-run (la espina dorsal comparativa) — ✅ hecho en esta rama

`content/simulador/runs/index.json`, generado por
`curiana_sim/export_runs_index.py`. Una fila por run **curado** (no todos: la
selección es explícita en `MANIFIESTO` dentro del script; smokes y runs de
desarrollo quedan en `BITACORA_RUNS.md`, no en la página).

Cada fila trae lo mínimo para comparar y para dibujar la evolución:

- identidad: `id8`, `seed_run_id`, `categoria` (baseline/koine/experimento/insignia),
  `hito` editorial, `started_at`, días/turnos, agentes.
- lingüística: `avg_score`, `pct_caquetio`, `neologismos_adoptados`.
- `convergencia`: lectura más exigente con datos (emergente > ventana >
  acumulada), con `inicio`/`fin`/`delta_pct` y la `serie` completa para
  sparkline. **Marca la `lectura`** para que la página muestre la reserva: la
  acumulada infla por acumulación del léxico base (ver `DISENO_KOINE.md §7`).
- `fijacion`: conceptos fijados + las formas ganadoras (concepto, forma, día,
  nº de variantes que compitieron).
- `pareja`/`rol`: enlaza los dos brazos de un experimento normal↔ablación.

Loader tipado: `lib/runs.ts` (`getRunsIndex`, `getRunIndexEntry`,
`getParejaExperimento`).

Degradación honesta: los runs anteriores al 2026-07-04 (`9bb920eb`, `20091e1f`)
no tienen ventana/emergente (columnas NULL) → el índice reporta su acumulada y
la marca como tal. No se inventa una métrica que no se midió.

### 2. Detalle por run (refactor pendiente de los exporters actuales)

Mover de singular → por-run:

```
content/simulador/
  runs/
    index.json                    ← ✅ espina cross-run
    2e729f3f/{resumen,personajes,neologismos}.json
    20091e1f/{resumen,personajes,neologismos,koine_lexicon}.json
    ...
```

Los tres `export_*_seed.py` ya aceptan `run_id` como argumento; el cambio es
que escriban a `runs/<id8>/` en vez de sobreescribir la raíz, y que el índice
sepa qué detalle existe. `lib/resumen.ts`, `lib/personajes.ts`,
`lib/neologismos.ts` ganan un parámetro de run (con el run activo como default,
para no romper las páginas actuales).

> Compatibilidad: mientras se migra, dejar los JSON singulares en la raíz como
> alias del run insignia, o migrar loaders y páginas en el mismo commit. No
> dejar la página a medias apuntando a rutas que aún no existen.

## Cambios de UI propuestos (requieren tu criterio de diseño — NO hechos aún)

1. **`/simulador` gana una sección "La evolución"** entre las ediciones y el
   detalle del run insignia: una línea de tiempo de los runs curados con su
   hito y una micro-métrica (caquetío %, convergencia). Es el arco del proyecto
   de un vistazo. Fuente: `getRunsIndex()`.
2. **Sección "El diccionario koiné"**: las formas fijadas de `20091e1f` (y del
   experimento) — concepto, forma ganadora, de cuántas variantes, qué día. Es
   el resultado más tangible y no está en la página hoy.
3. **Sección "La prueba de control"**: el par `038d7b9d`/`bdc54134` lado a lado
   — las dos curvas de convergencia emergente y la diferencia (−17.9% vs −6.6%).
   Es la pieza científica; `getParejaExperimento("038d7b9d")` la sirve entera.
4. El índice de "Ediciones" existente puede leer `categoria`/`hito` del índice
   en vez de tenerlos hardcodeados en `editorial.json`.

Las voces editoriales (Manaure, narrador) de cada run nuevo siguen viviendo en
`editorial.json` — el índice es dato medido, no narrativa. Se cruzan en la
página, como ya se hace hoy.

## Egress / producción

Sin riesgo nuevo: todo sale de Supabase **local** a JSON commiteado. La página
en producción nunca consulta la base (misma razón por la que se borró el Vercel
viejo). Añadir un run a la página = correr los exporters localmente + commit.

## Estado

**En producción (2026-07-07/08):**
- ✅ `export_runs_index.py` + `content/simulador/runs/index.json` (6 runs curados).
- ✅ `lib/runs.ts` (loader tipado + `getParejaExperimento()`).
- ✅ **Página propia `/simulador/runs`** con las tres secciones: la evolución
  (timeline cross-run), la prueba de control (experimento normal vs. ablación,
  `ConvergenciaChart` de doble línea) y el diccionario koiné. `/simulador` la
  anuncia con un callout destacado + anexo. Resolvió el problema de
  descubribilidad (las secciones estaban al 48% de scroll de la edición
  insignia; ahora la evolución arranca al 9% de su propia página).

**Pendiente:**
- ⏳ **Detalle por run** (`runs/<id8>/{resumen,personajes,neologismos}.json`):
  refactor de los tres `export_*_seed.py` a escribir por run + loaders con
  parámetro de run + ruta dinámica `/simulador/runs/[id8]` para que cada
  entrada del timeline sea navegable. Hoy el timeline no es clickable porque no
  hay a dónde ir. **Es infraestructura sin consumidor todavía**; conviene
  hacerlo junto con la UI que lo consuma, no antes.
- ⏳ **Reparar `20091e1f`** (el run del diccionario koiné, sin perfiles porque el
  teardown lo cortó en el turno 57). Escribe solo a Supabase local y cuesta
  centavos de Haiku, pero **no es un one-liner**: `generar_perfiles_curados`
  es un método de `ObserverAgent` (`curiana_observer.py:538`,
  `observer.generar_perfiles_curados(db, run_id)`) y necesita un `ObserverAgent`
  construido con un cliente Anthropic + el léxico. Lo más limpio es un script
  chico que replique el bloque `--perfiles` del orquestador
  (`curiana_orchestrator_v2.py:961`) apuntado al `run_id` de `20091e1f`, y
  luego `python export_personajes_seed.py 20091e1f-...` para regenerar su seed.
  (Además hoy no tiene consumidor en la página hasta que exista el detalle por
  run — ver punto anterior.)
