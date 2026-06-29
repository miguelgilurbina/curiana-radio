# Curiana — Simulador de Emergencia Lingüística Caquetía

Proyecto de investigación + experimento computacional: una simulación multi-agente donde 60 personajes históricos (pueblo Caquetío, Golfete de Coro, Venezuela, siglos XIV-XV) hablan en caquetío-arahuaco reconstruido. Los agentes evolucionan el idioma en tiempo real: inventan palabras, adoptan neologismos de otros, y su "deriva lingüística" queda registrada en Supabase y visualizada en un dashboard Next.js.

## Stack

```
curiana_sim/        → Python 3.11+ (simulación)
  curiana_lexicon.py      → vocabulario de 1262 palabras (activas; 441 hipotéticas aisladas en lexicon_candidatos.py) + reglas morfológicas + prompts
                            (muestra_caquetio_dinamica() prioriza caquetío por chunking contextual)
  curiana_agents.py       → 60 agentes históricos en 3 tiers (caciques, adultos, jóvenes)
  curiana_orchestrator_v2.py → orquestador principal (Claude Haiku por agente)
  curiana_observer.py     → análisis lingüístico + scoring 0-10 + detección de neologismos
                            + curación de perfiles de fin de run (analizar_agente_curado(),
                            generar_perfiles_curados() → agent_profiles/agent_quotes)
  curiana_social.py       → contagio léxico entre agentes (DifusionLexica: prestigio +
                            grafo social + exposición acumulada) + variación dialectal por etnia
  curiana_state.py        → estado del mundo (día, estación, eventos, locaciones)
  curiana_database.py     → Supabase client + LangSmith wrapper + language_composition()
                            + normalize_source_language() (8 categorías activas, ver abajo)
  arahuaco_comparative.py → método comparativo (transducir, COGNADOS, reconstruir_caquetio)
  supabase/migrations/    → schema versionado (init + fixes; supabase_schema.sql es referencia)

curiana_dashboard/  → Next.js 14 + Tailwind + Recharts + Supabase JS
  app/page.tsx            → dashboard en tiempo real (Supabase real-time subscriptions)
  app/lexicon/page.tsx    → explorador del léxico (1262 palabras, 8 categorías, paginado)
  app/neologisms/page.tsx → palabras inventadas por los agentes (propuesto/adoptado/rechazado)
  components/LanguageDriftChart.tsx → area chart de composición lingüística por turno
  components/AgentFeed.tsx          → feed en vivo de respuestas de agentes
  lib/supabase.ts         → cliente Supabase + tipos TypeScript + LANG_COLORS (8 categorías)
```

> ⚠️ **Queries a la tabla `lexicon`:** PostgREST limita cada respuesta a
> `max_rows` (1000, ver `supabase/config.toml`). Con 1262 palabras, cualquier
> query nueva sobre `lexicon` sin `.range()` se trunca silenciosamente.
> Pagina con `.range(desde, desde+999)` hasta que la página devuelta tenga
> menos de 1000 filas (ver `loadLexicon()` en `app/page.tsx` o `app/lexicon/page.tsx`).

## Modelo LLM

`claude-haiku-4-5-20251001` para todos los agentes (costo-efectivo). El cliente se crea en `curiana_database.py::get_anthropic_client()`. Si `LANGSMITH_API_KEY` está en el entorno, wrappea automáticamente con `wrap_anthropic()`.

## Variables de entorno

> ⚠️ **Supabase: correr en LOCAL por defecto (Docker), no en cloud.** El
> proyecto cloud llegó a 8.17 GB de egress (límite del plan Free: 5 GB) por
> el dashboard público con `realtime` + el patrón de tráfico típico de
> `*.vercel.app` (escaneo automático). El proyecto Vercel se borró por esa
> razón. Hasta decidir un reemplazo (Vercel con Deployment Protection, VPS
> propio, etc.), todo el trabajo de desarrollo/simulación corre contra
> Supabase local:
> ```bash
> cd curiana_sim && supabase start   # levanta Docker; ver supabase/config.toml
>                                     # (puertos 64321-64329, NO los default
>                                     #  54321-54329: esos los usan otros
>                                     #  proyectos supabase locales como
>                                     #  fintech.benditaia.cl. API=64321 DB=64322)
> ```
> `curiana_sim/.env` ya tiene ambos bloques (local activo, cloud comentado)
> — para volver a cloud, intercambiar qué bloque está comentado.

```bash
# curiana_sim/.env  (ver .env.example)
ANTHROPIC_API_KEY=sk-ant-...       # obligatorio
SUPABASE_URL=http://127.0.0.1:64321   # local (supabase start). Sin esto, modo JSON local.
SUPABASE_SERVICE_KEY=eyJ...           # service_role key local (ver `supabase status`)
LANGSMITH_API_KEY=ls__...             # opcional
LANGSMITH_PROJECT=curiana             # opcional
```

```bash
# curiana_dashboard/.env.local  (ver .env.local.example)
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:64321
NEXT_PUBLIC_SUPABASE_ANON_KEY=...     # anon key local (ver `supabase status`)
```

> ⚠️ **Carga de `.env` en scripts Python:** cada entrypoint que se corra
> directo (`python curiana_xxx.py ...`) debe cargar `curiana_sim/.env` por sí
> mismo — leer `os.environ` no basta. `curiana_orchestrator_v2.py` y
> `curiana_database.py` ya lo hacen con `load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))`
> al inicio del módulo. Si agregas un nuevo `__main__` (p.ej. en
> `curiana_observer.py`), copia ese mismo bloque o fallará con
> "Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY".

## Comandos clave

```bash
# Setup Python
cd curiana_sim
pip install -r requirements.txt
python test_quick.py          # verifica el stack sin API keys (debe dar 8/8 OK)
supabase start                 # levanta Supabase local (ver nota de egress arriba)
python curiana_database.py seed  # siembra las 1262 palabras activas en Supabase

# Correr simulación
python curiana_orchestrator_v2.py                    # modo interactivo
python curiana_orchestrator_v2.py --auto 10          # 10 turnos automáticos
python curiana_orchestrator_v2.py --auto 240 --anio  # 1 año simulado
python curiana_orchestrator_v2.py --auto 30 --perfiles --reporte
  # --perfiles: genera perfiles curados por agente al cerrar el run
  #             (rol, arco narrativo, frases célebres → agent_profiles/agent_quotes)
  # --reporte:  reporte anual LLM al completar cada año simulado

# Dashboard
cd curiana_dashboard
npm install
npm run dev          # http://localhost:3000
npx vercel           # deploy a Vercel — ⚠️ ver nota de egress: activar
                      # Deployment Protection antes de desplegar a producción
```

## Metodología del lexicón y validación

El lexicón activo distingue 8 categorías de `fuente` (ver `normalize_source_language()`
en `curiana_database.py`), porque "caquetío" mezclaba históricamente dato real
con especulación sin marcar:

- **`caquetío-atestiguado`** (75) — dato histórico real, citable a crónicas
  coloniales (Galeotto Cey, Oviedo, Las Casas) y trabajo académico (Zavala
  Reyes 2015, Oliver 1989, Jahn 1927).
- **`caquetío-reconstruido`** (82: 12 base + 2 topónimo + 68 núcleo
  fundacional) — vocabulario de trabajo del proyecto: pronombres, numerales,
  verbos básicos que `prompt_reglas_completo()`/`breve()` presentan a los
  agentes desde el día 1. No siempre atestiguado, pero es la lengua de la
  simulación, no un préstamo.
- **`hipotético-no-verificado`** (441) — **AISLADAS del léxico activo**
  (2026-06-28) a `curiana_sim/lexicon_candidatos.py` (`CANDIDATOS_NO_VERIFICADOS`).
  Palabras generadas por `reconstruir_caquetio_gaps.py` transduciendo
  fonológicamente CUALQUIER palabra wayunaiki/lokono/taíno con la misma glosa,
  **sin verificar cognación real** contra `COGNADOS` (el único set curado, 37
  entradas). La minería de pares objetivos (`minar_pares_validacion.py`) mostró
  ~80% de fallos contra datos reales. Estando en `VOCABULARIO_BASE` producían
  falsos positivos en `score_linguistico` (el "la"/"para" español matcheaba
  contra entradas hipotéticas), así que se sacaron del léxico y de Supabase. No
  se importan ni se siembran; quedan como material para una futura validación
  sistemática.
- **wayunaiki (781), lokono (228), taíno (57), proto-arahuaco (9), kalinago
  (19), kalinago-caribe-overlay (4), jirajaroide-contacto (7)** — lenguas
  hermanas/de contacto, tratadas como tan ajenas como el español para
  scoring (ver siguiente sección).

**Para fortalecer la Capa 2 (reconstrucción con base real):** minar más
fuentes publicadas con `fuentes_caquetios/*.pdf` (ya minado: Brinton 1871,
que dio 4 pares LK-TN reales y corrigió un bug en `REGLAS_LK_TN`; *no* dio
resultado: Perea Alonso 1942, que es gramática Lokono pura, no comparativa
entre lenguas arahuacas). `arahuaco_comparative.py::validar()` corre la
suite de validación (18 pares al momento de escribir esto).

## Scoring lingüístico (`score_linguistico()` en `curiana_lexicon.py`)

El objetivo del proyecto es que el caquetío **domine**, no solo que se evite
el español. `score_linguistico()` penaliza dos fugas distintas:
1. Español funcional (`el/la/de/que/...`) — penalización fuerte (hasta −3).
2. Otra lengua arahuaca viva (wayunaiki/lokono/taíno) en vez de su forma
   caquetía — penalización moderada (hasta −2.5), vía `_familia_de_token()`.

El rescate intra-turno (`curiana_orchestrator_v2.py::call_agent()`) dispara
reintento tanto por score bajo como por fuga a otra lengua arahuaca
(`otro_arahuaco >= 3` y `pct_caquetio_especifico < 0.3`).

Verificado en runs reales contra Supabase local: caquetío pasó de ~27% a
~91-93% del output tras estos cambios + retaguear el núcleo fundacional.

## Morfología caquetío-arahuaca

```
Orden: pronombre + verbo-aspecto + complemento
Pronombres: taya (yo), pia (tú), nüma (él/ella), tayamaa (nosotros)
Aspectos: -ka (completivo), -ni (continuativo), -da (prospectivo)
Prefijos posesivos: ta- (mi), pi- (tu), nü- (su)
Locativos: -bana (orilla/borde), -ana (lugar de), -ko (interior de)
Neologismos: agentes proponen [forma: componentes = significado]
```

## Arquitectura de datos

```
simulation_runs → turns → agent_responses → word_uses
                                          → neologisms
                       → phrase_etymologies
                       → agent_profiles → agent_quotes   (perfiles curados, --perfiles)
lexicon  (seed desde VOCABULARIO_BASE)
```

Real-time en Supabase: `agent_responses`, `turns`, `neologisms`, `agent_profiles`,
`agent_quotes` publicados en `supabase_realtime`.

## Próximos pasos del proyecto

1. Analizar los datos de la simulación larga ya corrida (ver
   `agent_profiles`/`agent_quotes` y `language_drift_by_turn` en Supabase
   local) — este era el objetivo original: simular, documentar, analizar.
2. Decidir qué mostrar públicamente (la página debe mostrar el proyecto en
   sí, curado — no necesariamente todos los datos crudos).
3. Decidir el reemplazo del proyecto Supabase cloud borrado (ver nota de
   egress arriba) antes de cualquier deploy público del dashboard.
4. Seguir fortaleciendo la Capa 2 minando más fuentes publicadas (ver
   sección de metodología arriba) si se quiere reconstruir más caquetío
   con base real, validando las 441 `hipotético-no-verificado` ya aisladas en
   `lexicon_candidatos.py` (minar fuentes y conservar solo las que pasen).

## Archivos de referencia

- `IDEA_PERFILES_AGENTES.md` — diseño de la sección de perfiles de agentes
  (rol, arco narrativo, frases célebres) y su implementación.
- `test_quick.py` — test suite sin API keys (debe dar 8/8 OK).
- `requirements.txt` — dependencias pinneadas.
- `.env.example` / `.env.local.example` — templates de variables de entorno.
- `curiana_sim/minar_pares_validacion.py` — mina el propio corpus para
  pares de validación objetivos (caquetío atestiguado + cognado hermano).
- `curiana_sim/retag_nucleo_fundacional.py` /
  `retag_reconstruccion_no_verificada.py` — scripts de corrección de
  etiquetado del lexicón (documentan por qué quedó como quedó).
