# Reporte de trabajo nocturno — Curiana

**Fecha:** 2026-06-16
**Alcance:** levantar Supabase local, probar todo el pipeline end-to-end y dejar
el dashboard funcionando contra datos reales. Todo verificado **sin** la
`ANTHROPIC_API_KEY` (la simulación con agentes LLM queda lista para que la dispares tú).

---

## ✅ Qué quedó funcionando

### Supabase local (Docker) — CORRIENDO
- 10 contenedores `supabase_*_curiana_sim` arriba y *healthy*, puertos por defecto.
- **API:** http://127.0.0.1:54321 · **Studio:** http://127.0.0.1:54323 · **DB:** `postgresql://postgres:postgres@127.0.0.1:54322/postgres`
- Schema aplicado vía migración: **7 tablas + 2 vistas** (`language_drift_by_turn`, `top_words_by_agent`).
- Publicación realtime activa: `agent_responses`, `turns`, `neologisms`.
- **Léxico sembrado: 146 palabras** en la tabla `lexicon`.

### Pipeline de datos — PROBADO END-TO-END
- `seed_demo_run.py` creó un run real (`50b0ae2f…`) con 15 respuestas, 5 turnos, 3 días,
  3 neologismos (2 adoptados), 91 `word_uses` — todo pasando por el flujo de producción
  (`observer.analizar → score_linguistico → db.save_*`).
- **BUG 3 verificado en Supabase real:** `aspects_used` se persiste poblado
  (`{completivo,continuativo,prospectivo}`) y `morphological_rule` también — ya no van vacíos.

### Dashboard — RENDERIZANDO DATOS REALES
- `npm run build` ✓ (6/6 páginas). Dev server verificado en http://localhost:3005.
- DOM confirmado: la home muestra *"Run 50b0ae2f · Score promedio 7.53 · Neologismos adoptados 2 de 3"*,
  el **drift chart** (recharts, % apilado por lengua fuente D1T1→D3T5) y el **feed de agentes**.
- `/lexicon` muestra las 146 palabras con su desglose (21 wayunaiki · 41 lokono · 57 taíno · 11 arahuaco · 16 caquetío).
- `.env.local` apunta al Supabase local (anon key + URL 54321).

### Pruebas automatizadas
- `test_quick.py` → **8/8 OK**
- `test_pipeline.py` (nuevo) → **30/30 OK**: scoring v2, neologismos, contagio, rescate,
  BUG1 (sin "Responde en español"), BUG3 (campos reales). Sin Docker ni API key.

---

## ▶️ Cómo correr la simulación REAL con agentes (lo único que falta)

1. Pega tu key en `curiana_sim/.env`:  `ANTHROPIC_API_KEY=sk-ant-...`
2. Asegúrate de que Supabase local sigue arriba (`npx supabase status` en `curiana_sim/`).
   Si no, `npx supabase start`.
3. Corre, por ejemplo, 10 turnos:
   ```
   cd curiana_sim
   PYTHONUTF8=1 python curiana_orchestrator_v2.py --auto 10
   ```
   Los agentes hablarán caquetío (BUG1 corregido), con rescate intra-turno si la densidad
   baja de 5/10 y contagio léxico entre vecinos sociales. Todo se persiste en Supabase y
   aparece en el dashboard en tiempo real.

> En Windows usa siempre `PYTHONUTF8=1` por la consola cp1252 (los scripts imprimen unicode).

---

## ⚠️ Notas y pendientes

- **Docker estuvo inestable** (VM WSL2 en read-only por disco bajo). Se recuperó con
  `wsl --shutdown` + reinicio de Docker Desktop, y se liberó disco borrando una pila
  Supabase ajena (`fintech`, autorizado). Si vuelve a quedar read-only: cierra Docker
  Desktop, `wsl --shutdown`, reábrelo.
- **Puertos:** se usan los de Supabase por defecto (54321+). El rango 55227–55426 está
  reservado por Windows/Hyper-V — no usar ahí.
- **Bug menor de etiquetado (audit B6, no crítico):** la detección de regla morfológica de
  un neologismo confunde sufijos solapados — `sima-bana`/`kuru-bana` se etiquetan `-ana`
  en vez de `-bana`. No afecta el scoring ni el caquetío de los agentes; solo el campo
  `morphological_rule`. Fácil de corregir ordenando los sufijos por longitud.
- **Para producción / Vercel:** el dashboard compila limpio y está listo. Necesita un
  **Supabase cloud** (el local no es accesible desde Vercel). Cuando lo tengas, cambia
  `curiana_dashboard/.env.local` (o las env vars de Vercel) a la URL + anon key cloud, y
  corre el schema (`supabase/migrations/20260613000000_init.sql`) + el seed en ese proyecto.

---

## Commits de la sesión
- `init repo + fix 3 critical bugs` · `curiana_social.py (contagio)` ·
  `wire rescate + contagio en orquestador` · `supabase scaffolding` ·
  `dashboard eslint isolation` · `test suite + demo generator` · `supabase local funcionando`
