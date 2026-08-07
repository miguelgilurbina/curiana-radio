---
tipo: nota
pregunta: "¿Cómo está construido el motor, y dónde va a doler?"
medido: 2026-08-06
modulos: 50
lineas: 30651
---

# Arquitectura del motor — medida, no recordada

> Todo lo de aquí sale de leer el AST y el grafo de imports, no de la memoria
> de nadie. Fecha de medición: 2026-08-06.

## El titular

**30.651 líneas en 50 módulos. El motor de verdad son ~4.300.** El resto es
dato-como-código (~12.000), minadores (~5.500), scripts de un solo uso ya
consumidos (~1.500) y herramientas de medición (~2.300).

Eso no es malo en sí — pero conviene saberlo, porque casi todas las decisiones
de escalado que parecen "refactorizar el motor" son en realidad **decisiones
sobre dónde vive el dato**.

## Las cinco capas que hay hoy

```
┌─ MOTOR (~4.300 líneas) ─ lo que corre una simulación
│   curiana_orchestrator_v2  1043   el bucle; importa a los otros seis
│   curiana_observer          708   scoring, análisis, perfiles curados
│   curiana_database          690   Supabase + LangSmith + composición
│   curiana_agents            578   los 60 personajes (dato, no lógica)
│   curiana_koine             563   idiolectos, competencia léxica, métricas
│   curiana_state             404   día, estación, locaciones, eventos
│   curiana_social            290   contagio léxico, prestigio, dialecto
│
├─ DATO-COMO-CÓDIGO (~12.000)
│   curiana_lexicon          7554   ⚠️ 87% son 11 dicts anotados
│   lexicon_van_buurt        1587   propuesta de minería
│   cognados_oliver          1443   propuesta de minería
│   lexicon_alvarado         1243   propuesta de minería
│   lexicon_toponimos         739 · lexicon_gatschet 618 · lexicon_candidatos 466
│   lexicon_zavala            372   ⚠️ el único que el motor IMPORTA
│
├─ MINADORES (~5.500)  minar_*.py — uno por fuente, todos con la misma forma
├─ MEDICIÓN (~2.300)   generar_tablero · compilar_corpus · curiana_polities ·
│                      analizar_runs · auditar_82 · check_vault_links
└─ ARQUEOLOGÍA (~1.500) 12 scripts sin importador y sin mención en la doc
```

## Los cuatro problemas reales

### 1. 🔴 `curiana_lexicon.py` es una base de datos disfrazada de módulo

| | Líneas | % |
|---|---|---|
| 11 dicts anotados (`AnnAssign`) | **6.540** | **87%** |
| 20 funciones | 566 | 7% |
| 2 clases | 162 | 2% |

**Una línea de lógica por cada once de dato.** Y lo importan **17 módulos**, así
que cada import parsea 6.540 líneas de literales.

Esto es lo que va a doler al escalar: cada palabra nueva es un commit al mismo
archivo, los conflictos de merge son inevitables, y no hay forma de consultar el
lexicón sin cargarlo entero en memoria.

> **El síntoma ya apareció**: `lexicon_zavala.py` es generado, `curiana_lexicon`
> lo importa, y por eso una segunda atestación de `capu` no tiene dónde vivir
> (issue abierto). El problema no es ese lema: es que el dato y el código
> comparten archivo.

### 2. 🟠 Ciclo `curiana_lexicon ↔ curiana_database`

Los dos se importan mutuamente. Funciona **solo** porque los imports son locales
a la función:

- `curiana_lexicon` pide `normalize_source_language` en 3 sitios
- `curiana_database` pide `VOCABULARIO_BASE` y `_familia_de_token` en 3 sitios

Es una bomba de relojería: el día que alguien suba uno de esos imports al nivel
del módulo —lo natural al limpiar— el import revienta en círculo.

**La causa de fondo**: `normalize_source_language()` es lógica de *lengua*, no
de *base de datos*, y está en el módulo equivocado. Moverla a `curiana_lexicon`
rompe el ciclo sin tocar nada más.

> Este ciclo ya costó un bug real: `word_source_language()` (en `database`) y
> `_familia_de_token()` (en `lexicon`) hacían el mismo trabajo con distinto
> criterio, y **la mitad del corpus se guardó sin lengua** durante 23 runs. Dos
> caminos para la misma pregunta es exactamente lo que produce un ciclo.

### 3. 🟡 1.484 líneas de arqueología

Doce módulos sin importador y sin mención en la documentación:

`aplicar_reconstruccion` · `copy_local_to_prod` · `export_lexicon_seed` ·
`export_resumen_seed` · `patch_integrate_comparative` · `patch_lexicon_jirajaroide` ·
`patch_lexicon_kalinago` · `patch_lexicon_lokono_full` · `patch_lexicon_wayunaiki_full` ·
`regenerar_quotes_traduccion` · `seed_demo_run` · `wayunaiki_phonology`

Son migraciones que ya corrieron. **No estorban al motor, pero sí a quien lee el
repo**: cinco `patch_lexicon_*` sugieren que hay cinco formas de parchear el
lexicón, y no hay ninguna — ya se aplicaron todas.

No hay que borrarlas a ciegas: `wayunaiki_phonology` y
`patch_integrate_comparative` contienen reglas que quizá sigan valiendo. Pero
deberían estar en `curiana_sim/historico/` con un README que diga qué se aplicó
y cuándo.

### 4. 🟡 El orquestador conoce a todo el mundo

`curiana_orchestrator_v2` importa los otros **siete** módulos del motor. Es el
único punto donde se juntan, y hoy funciona porque el motor es pequeño.

No es un problema todavía. Lo será cuando entre una segunda polity (D14) o un
segundo tipo de run: ahí el orquestador pasa de "el bucle" a "el sitio donde se
cablea todo", que es el patrón que obliga a refactorizar.

## Lo que está bien y conviene no tocar

- **La disciplina de minería**: cada `minar_*.py` emite una *propuesta* y no
  toca el lexicón activo. Es lo que ha permitido minar ocho fuentes sin romper
  nada, y es replicable tal cual para las fuentes nuevas.
- **La capa de medición**: `generar_tablero`, `compilar_corpus`,
  `curiana_polities --canon`, `analizar_runs`, `check_vault_links`. Cinco
  guardianes que miden contra el dato y no contra la documentación. Es la mejor
  decisión de arquitectura del proyecto.
- **Las etiquetas epistémicas** atravesando lexicón y corpus. Es lo que hace que
  el proyecto sea investigación y no fanfiction.
- **El motor es pequeño**: 4.300 líneas para una simulación multi-agente con
  scoring lingüístico, contagio social y métricas de convergencia es poco. La
  complejidad está donde debe.

## El orden en que yo lo abordaría

| # | Qué | Por qué ahora | Coste |
|---|---|---|---|
| 1 | Mover `normalize_source_language` a `curiana_lexicon` | rompe el ciclo, sin cambiar comportamiento | 1 h |
| 2 | Mover los 12 scripts a `curiana_sim/historico/` con README | el repo deja de mentir sobre qué se puede correr | 1 h |
| 3 | Sacar `VOCABULARIO_BASE` a datos (YAML/SQLite) con una capa de acceso | **es la decisión de escalado de verdad** — ver abajo | 1-2 días |
| 4 | Extraer del orquestador la construcción del prompt | lo pide D14 (segunda polity) y el confusor de longitud | 0.5 día |

### Sobre el punto 3, que es el que se pregunta el proyecto

El lexicón como código tiene una virtud real que no hay que perder: **está
versionado, se revisa en PR y cada cambio tiene su commit y su porqué**. Eso es
justamente lo que hace creíble al proyecto.

La salida no es "meterlo en la base" —perderías el diff— sino **separar el dato
del módulo conservando git**: un `lexicon/*.yaml` por capa epistémica, cargado
por una función que cachee. Se sigue revisando en PR, se sigue diffeando, deja
de ser un archivo de 7.554 líneas, y `lexicon_zavala` deja de ser un caso
especial porque *todas* las fuentes serían datos.

Es la única de las cuatro que merece llamarse refactor. Las otras tres son
higiene y se pueden hacer en una tarde.

## Enlaces

[[mapa-motor]] · [[polities-caquetias]] · [[ANALISIS_BASE_2026-08-06]] · [[PLAN_MAESTRO]]
