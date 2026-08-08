---
tipo: nota
pregunta: "¿Cómo se trabaja aquí sin que la infra haya que rehacerla luego?"
medido: 2026-08-06
---

# El harness — cómo escala este proyecto

> Escrito al salir Opus 5, revisando qué setup de desarrollo merece este
> proyecto. La pregunta no es *"¿qué herramientas hay?"* sino *"¿qué es lo que
> se rompe cuando esto crece, y qué lo evita sin rehacer la infra?"*.

## Diagnóstico: no había harness

Medido el 2026-08-06:

| Pieza | Estado |
|---|---|
| `.claude/commands/` | 5 comandos, **todos del stack web** (Next.js, TypeScript, UI) — ninguno de este proyecto |
| `.claude/skills/` | vacío |
| `.claude/agents/` | vacío |
| hooks | ninguno |
| `settings.json` compartido | no existe (solo `settings.local.json`, personal) |
| CLAUDE.md | 319 líneas, 19 KB, con 25 cifras exactas escritas a mano |

**Todo el rigor del proyecto dependía de que el agente se acordara.** Y se
acordaba —hay cinco guardianes escritos y buenos— pero acordarse no es un
método: es suerte con buena racha.

## El principio

> **Lo que no puede fallar, no puede depender de que alguien lo recuerde.**

Este proyecto tiene una virtud rara: sus invariantes son **ejecutables**. "El
corpus es válido", "el grafo resuelve", "todo rasgo tiene fuente" no son buenas
intenciones — son cinco scripts que devuelven 0 o 1. Eso es lo que hace que el
harness sea barato: no hay que inventar la validación, solo cablearla.

## Las cuatro capas, y qué va en cada una

### 1. Guardianes — la verdad ejecutable

```bash
python curiana_sim/guardianes.py     # los 5, ~9 s
```

| Guardián | Qué protege |
|---|---|
| `pytest tests/` | el motor (125 tests) |
| `test_quick.py` | el stack arranca sin API keys (8/8) |
| `check_vault_links.py --strict` | ningún wikilink roto |
| `compilar_corpus.py --check` | los 161 hechos validan |
| `curiana_polities.py --check` | ningún rasgo sin fuente |

**Regla**: nada se da por cerrado sin los cinco en verde. Cada uno **tiene que
haber fallado alguna vez a propósito** para saber que sirve — los cinco lo han
hecho.

`generar_tablero.py --check` **queda fuera a propósito**: se pone viejo cada vez
que cambia una cifra medida, que es constantemente. Se regenera, no se vigila.

### 2. Skills — los procedimientos que se repiten

Una skill es un procedimiento que ya se ha hecho varias veces y que **se hacía
mal la primera vez**. No es documentación: es lo que evita repetir el error.

| Skill | Estado | Por qué |
|---|---|---|
| `minar-fuente` | ✅ escrita | 8 minerías con la misma forma; el paso "verifica la ortografía antes de contar" existe porque el mismo error apareció **3 veces en una noche** |
| `sesion-corpus` | pendiente | las 5 sesiones del programa cultural tienen estructura idéntica (pregunta → ensayo → YAML → hoja de fuentes) |
| `analizar-run` | pendiente | ahora que `analizar_runs.py` existe, el procedimiento de leerlo es codificable |

### 3. CLAUDE.md — solo lo que cambia el comportamiento

Se cargó en cada sesión, así que su coste es por sesión. La regla que lo bajó de
19 KB a 7,7 KB sin perder nada:

> **Si el dato se puede consultar, va en un puntero. Si su ausencia causa un
> error, va en CLAUDE.md.**

Lo que **sí** va: los nueve invariantes, la tabla de trampas medidas (cada fila
costó un error real), los comandos, y el mapa de dónde está cada cosa.

Lo que **no**: cifras (→ `TABLERO.md`), metodología larga (→ `2-lengua/`),
historia de las minerías (→ `4-fuentes/`), arquitectura (→ `ARQUITECTURA.md`).

El archivo llegó a decir *"las cifras exactas NO van aquí"* y a continuación
listar veinticinco. Un documento que se contradice a sí mismo no lo lee nadie.

### 4. Permisos — que el agente no pregunte lo obvio

`settings.local.json` acumulaba entradas efímeras (mensajes de commit concretos
ya usados) y otras demasiado amplias (`Bash(git rm *)`, `Bash(python -c ' *)`).

Lo que corresponde: un `settings.json` **compartido** con los comandos
seguros y repetidos de este proyecto —`pytest`, `pdftotext`, `docker exec …
psql`, los guardianes— y dejar `settings.local.json` para lo personal, además
de sacarlo del control de versiones.

## Lo que NO hay que montar

Tan importante como lo anterior:

- **Nada de subagentes por ahora.** El trabajo es secuencial y con mucho estado
  compartido (el lexicón, el corpus, el canon). Un subagente arrancaría en frío
  y volvería a derivar el contexto que ya está en la sesión.
- **Nada de CI en la nube todavía.** Los guardianes corren en 9 segundos en
  local. CI tendría sentido cuando haya más de una persona.
- **Nada de hooks que bloqueen.** Un hook que impida cerrar cuando un guardián
  falla suena bien y sería un incordio: hay estados intermedios legítimos
  (minar una fuente rompe el tablero hasta regenerarlo). Los guardianes se
  corren; no vigilan.

## Qué escala mal si no se toca

Del análisis de arquitectura, ordenado por cuándo va a doler:

| # | Qué | Cuándo duele |
|---|---|---|
| 1 | `curiana_lexicon.py`: 7.554 líneas, **87% dato** | ya duele — cada palabra nueva es un commit al mismo archivo |
| 2 | Ciclo `lexicon ↔ database` | cuando alguien suba un import al nivel del módulo |
| 3 | El orquestador importa los 7 módulos del motor | al entrar una segunda polity (D14) |
| 4 | 1.484 líneas de scripts ya consumidos | cada vez que alguien lee el repo |

**La única que merece llamarse refactor es la 1**, y su solución no es "meterlo
en la base" —perderías el diff, que es lo que hace creíble al proyecto— sino
sacar el dato a `lexicon/*.yaml` por capa epistémica, cargado por una función
que cachee. Se sigue revisando en PR, se sigue diffeando, y `lexicon_zavala`
deja de ser un caso especial porque *todas* las fuentes serían datos.

## El orden que propongo

1. **Ya hecho**: `guardianes.py`, skill `minar-fuente`, CLAUDE.md reescrito.
2. **Una tarde**: `settings.json` compartido · mover los 12 scripts a
   `curiana_sim/historico/` · `normalize_source_language` a `curiana_lexicon`
   (rompe el ciclo).
3. **Cuando llegue D14**: extraer del orquestador la construcción del prompt.
4. **El refactor de verdad**: el lexicón a datos. Cuando estorbe de verdad, no
   antes.

## Enlaces

[[ARQUITECTURA]] · [[PLAN_MAESTRO]] · [[mapa-motor]] · [[ANALISIS_BASE_2026-08-06]]
