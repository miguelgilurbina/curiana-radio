# Curiana — Simulador de Emergencia Lingüística Caquetía

Proyecto de investigación + experimento computacional: una simulación multi-agente donde 60 personajes históricos (pueblo Caquetío, Golfete de Coro, Venezuela, siglos XIV-XV) hablan en caquetío-arahuacano reconstruido. Los agentes evolucionan el idioma en tiempo real: inventan palabras, adoptan neologismos de otros, y su "deriva lingüística" queda registrada en Supabase y visualizada en un dashboard Next.js.

## Stack

```
curiana_sim/        → Python 3.11+ (simulación)
  curiana_lexicon.py      → vocabulario de 146 palabras + reglas morfológicas + prompts
  curiana_agents.py       → 60 agentes históricos en 3 tiers (caciques, adultos, jóvenes)
  curiana_orchestrator_v2.py → orquestador principal (Claude Haiku por agente)
  curiana_observer.py     → análisis lingüístico + scoring 0-10 + detección de neologismos
  curiana_state.py        → estado del mundo (día, estación, eventos, locaciones)
  curiana_database.py     → Supabase client + LangSmith wrapper + language_composition()
  supabase_schema.sql     → schema completo PostgreSQL (7 tablas + vistas + RLS)

curiana_dashboard/  → Next.js 14 + Tailwind + Recharts + Supabase JS
  app/page.tsx            → dashboard en tiempo real (Supabase real-time subscriptions)
  app/lexicon/page.tsx    → explorador del léxico (146 palabras con filtros)
  app/neologisms/page.tsx → palabras inventadas por los agentes (propuesto/adoptado/rechazado)
  components/LanguageDriftChart.tsx → area chart de composición lingüística por turno
  components/AgentFeed.tsx          → feed en vivo de respuestas de agentes
  lib/supabase.ts         → cliente Supabase + tipos TypeScript
```

## Modelo LLM

`claude-haiku-4-5-20251001` para todos los agentes (costo-efectivo). El cliente se crea en `curiana_database.py::get_anthropic_client()`. Si `LANGSMITH_API_KEY` está en el entorno, wrappea automáticamente con `wrap_anthropic()`.

## Variables de entorno

```bash
# curiana_sim/.env  (ver .env.example)
ANTHROPIC_API_KEY=sk-ant-...       # obligatorio
SUPABASE_URL=https://xxx.supabase.co  # opcional (sin esto corre en modo JSON local)
SUPABASE_SERVICE_KEY=eyJ...           # service_role key (NO el anon key)
LANGSMITH_API_KEY=ls__...             # opcional
LANGSMITH_PROJECT=curiana             # opcional
```

```bash
# curiana_dashboard/.env.local  (ver .env.local.example)
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

## Comandos clave

```bash
# Setup Python
cd curiana_sim
pip install -r requirements.txt
python test_quick.py          # verifica el stack sin API keys (debe dar 8/8 OK)
python curiana_database.py seed  # siembra las 146 palabras en Supabase

# Correr simulación
python curiana_orchestrator_v2.py                    # modo interactivo
python curiana_orchestrator_v2.py --auto 10          # 10 turnos automáticos
python curiana_orchestrator_v2.py --auto 240 --anio  # 1 año simulado

# Dashboard
cd curiana_dashboard
npm install
npm run dev          # http://localhost:3000
npx vercel           # deploy a Vercel
```

## Bugs críticos a corregir (de la auditoría Opus — ver AUDITORIA_OPUS.md)

### BUG 1 — CRÍTICO: system_prompts dicen "Responde en español"
En `curiana_agents.py`, casi todos los `system_prompt` de los agentes terminan con "Responde en español...". Esto anula el bloque `_IDENTIDAD_LINGUISTICA` del orquestador. **Es la causa raíz #1 de que los agentes hablen español.** Hay que remover esa instrucción de todos los prompts.

### BUG 2: score_linguistico() mide mal
La función actual hace substring match (encuentra "ka" dentro de "Tawaka") y nunca penaliza el español. Ver `AUDITORIA_OPUS.md` §2 para la versión mejorada con tokenización real y penalización.

### BUG 3: Field names incorrectos en el orquestador
En `curiana_orchestrator_v2.py::run_turn()`, los `getattr` para guardar en Supabase usan nombres de campo incorrectos:
- `registro.palabras_caquetias` → verificar el nombre real en `curiana_observer.py`
- `registro.aspectos_detectados` → verificar el nombre real
- `neo.regla` → debería ser `neo.regla_aplicada` (o el nombre real en Neologismo)
Esto hace que `aspects_used` y la regla morfológica siempre se guarden vacíos en Supabase.

## Morfología caquetío-arahuacana

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
lexicon  (seed desde VOCABULARIO_BASE)
```

Real-time en Supabase: `agent_responses`, `turns`, `neologisms` publicados en `supabase_realtime`.

## Próximos pasos del proyecto

1. Corregir los 3 bugs arriba antes de cualquier otra cosa
2. Leer `AUDITORIA_OPUS.md` — tiene código Python listo para los fixes
3. Implementar `curiana_social.py` — contagio lingüístico entre agentes (ver §5 de la auditoría)
4. Deploy Vercel del dashboard
5. Correr una simulación de 240 turnos (1 año) y analizar la deriva lingüística

## Archivos de referencia generados esta sesión

- `AUDITORIA_OPUS.md` — auditoría técnica completa (687 líneas, código incluido)
- `CULTURA_CAQUETIA.md` — enciclopedia etnográfica precolonial (cosmología, economía, ritual)
- `test_quick.py` — test suite sin API keys (8/8 tests)
- `requirements.txt` — dependencias pinneadas
- `.env.example` — template de variables de entorno
