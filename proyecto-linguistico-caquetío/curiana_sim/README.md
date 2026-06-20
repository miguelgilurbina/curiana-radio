# Curiana — Simulador de Emergencia Lingüística Caquetía

> *"Curiana: territorio donde estaban asentados los caquetíos."*
> — Zavala Reyes (2015, nota 4)

## Qué es esto

Curiana es un **simulador de emergencia lingüística**: una comunidad multiétnica
pre-contacto europeo en la **Curiana** (Golfete de Coro, Falcón, Venezuela, siglos
XIV–XV), poblada por 60 agentes LLM (claude-haiku-4-5).

El objetivo no es la narrativa sino el **lenguaje**. Los agentes hablan caquetío
(arahuaco) como lengua materna, con el español solo como glosa. Cuando enfrentan
un vacío léxico, aplican reglas morfológicas reales (basadas en wayunaiki, lokono,
taíno) para **acuñar palabras nuevas**. Un Observer lingüístico analiza cada turno,
puntúa la densidad caquetía, detecta neologismos y registra cuándo una palabra nueva
es **adoptada** por la comunidad (cuando 2 agentes distintos la usan). El resultado es
una simulación de cómo una lengua puede emerger y derivar a lo largo de días, meses y
años simulados.

## Stack técnico

| Capa | Tecnología |
|---|---|
| LLM | Anthropic `claude-haiku-4-5-20251001` (`anthropic==0.109.1`) |
| Backend | Python 3.10 |
| Persistencia (opcional) | Supabase / PostgreSQL (`supabase==2.31.0`) |
| Tracing (opcional) | LangSmith (`langsmith==0.8.15`) |
| Config | `python-dotenv==1.2.2` |
| Frontend | Next.js 14 + React 18 + Recharts + Tailwind + `@supabase/supabase-js` |

Sin Supabase, la simulación corre en **modo local JSON** (`CurianaDBMock`) — todo
funciona, solo que no se persiste en la nube.

## Instalación rápida (comandos paso a paso)

```bash
# 1. Entrar al backend
cd curiana_sim

# 2. (Recomendado) crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar dependencias pinneadas
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
#   edita .env y pon al menos ANTHROPIC_API_KEY

# 5. Verificar el stack SIN gastar tokens (imports, léxico, DB mock, scoring)
python test_quick.py
#   esperado: "✓ 8/8 módulos OK"  (exit 0)
```

## Cómo correr la simulación

```bash
# Modo interactivo (recomendado para explorar)
python curiana_orchestrator_v2.py

# 10 turnos automáticos (5 días simulados)
python curiana_orchestrator_v2.py --auto 10

# 1 año simulado completo (~240 turnos)
python curiana_orchestrator_v2.py --auto 240 --anio

# 1 año con reporte lingüístico anual generado por LLM
python curiana_orchestrator_v2.py --auto 240 --reporte
```

### Comandos interactivos

| Comando | Acción |
|---|---|
| `[Enter]` | Avanzar turno |
| `habla Shaboro` | Conversar con un agente |
| `estado` | Ver estado del mundo |
| `lexico` | Ver léxico comunitario vivo |
| `ranking` | Ranking de agentes por densidad lingüística |
| `reporte dia` | Reporte lingüístico del día actual |
| `evento niño_enfermo` | Forzar un evento |
| `exportar` | Exportar CSVs de análisis |
| `salir` | Guardar y cerrar |

### Sembrar el léxico en Supabase (opcional)

```bash
python curiana_database.py seed     # inserta VOCABULARIO_BASE en la tabla lexicon
python curiana_database.py test     # test local de composición de lengua
python curiana_database.py check    # muestra el último run registrado
```

## Variables de entorno

| Variable | Obligatoria | Descripción |
|---|---|---|
| `ANTHROPIC_API_KEY` | **Sí** | Clave de la API de Anthropic. Sin ella no hay simulación. |
| `SUPABASE_URL` | No | URL del proyecto Supabase. Sin esto → modo local JSON. |
| `SUPABASE_SERVICE_KEY` | No | `service_role` key (bypassa RLS para escritura desde el backend). |
| `LANGSMITH_API_KEY` | No | Activa el tracing automático de todas las llamadas LLM. |
| `LANGSMITH_PROJECT` | No | Nombre del proyecto LangSmith (default: `curiana`). |

Copia `.env.example` a `.env` y rellena los valores.

## Arquitectura

```
curiana_sim/
├── curiana_agents.py          # 60 agentes (Tier I/II/III) con system prompts
├── curiana_state.py           # Estado del mundo: tiempo, clima, eventos, locaciones
├── curiana_lexicon.py         # Motor morfológico: vocab + reglas + léxico vivo
├── curiana_observer.py        # Observer lingüístico + Juez + reportes periódicos
├── curiana_database.py        # Capa Supabase + LangSmith (+ CurianaDBMock)
├── curiana_orchestrator_v2.py # Director + loop principal de simulación
├── supabase_schema.sql        # Schema PostgreSQL (tablas + vistas)
├── test_quick.py              # Verificación rápida sin llamadas LLM
├── requirements.txt
├── .env.example
└── data/                      # Persistencia JSON/CSV (se genera al correr)
```

| Archivo | Responsabilidad |
|---|---|
| `curiana_agents.py` | Define los 60 agentes en 3 tiers con personalidad, etnia, ubicación y relaciones. Expone `ALL_AGENTS`, `get_agent`, `get_tier`, `agents_at_location`. |
| `curiana_state.py` | `ComunidadState` (día, turno, estación, clima, tensión, eventos) + catálogos de eventos cotidianos/estacionales. Genera el contexto inyectado en cada agente. |
| `curiana_lexicon.py` | Núcleo lingüístico: `VOCABULARIO_BASE` (93 palabras), reglas morfológicas, `LexicoComunitario` (léxico vivo), `score_linguistico`, `extraer_neologismos_del_texto`, generadores de prompts. |
| `curiana_observer.py` | `ObserverAgent`: analiza cada respuesta, puntúa, extrae neologismos, detecta adopciones, genera reportes por turno/día/estación/año y exporta CSVs. |
| `curiana_database.py` | `CurianaDB` (Supabase) y `CurianaDBMock` (no-op local). `get_db()` elige según entorno. `get_anthropic_client()` envuelve con LangSmith. `language_composition()` calcula proporciones por lengua fuente. |
| `curiana_orchestrator_v2.py` | El Director: selecciona eventos y agentes activos, ejecuta el loop de turnos, conecta agentes + estado + léxico + observer + DB. |

### Flujo por turno

```
Director → selecciona evento + agentes activos (3–6)
    ↓
Cada agente recibe: system_prompt + estado del mundo + léxico activo
                    + reglas morfológicas + feedback (si score previo bajo)
    ↓
Agente responde en caquetío (usa vocab, aplica aspecto, propone neologismos)
    ↓
Observer analiza: palabras usadas → neologismos → score 0–10 → adopciones
    ↓
Director narra el cierre del turno
```

## El léxico caquetío

**Vocabulario base: 93 palabras** — caquetío atestiguado (Zavala 2015, Jahn 1927,
Alvarado 1921) + cognados arahuacos (wayunaiki, taíno, lokono, garifuna). Cada
entrada lleva su `fuente`, que `curiana_database.py` normaliza a 5 categorías
canónicas: `caquetío`, `wayunaiki`, `lokono`, `taíno`, `arahuaco`.

Palabras clave: `barsure` (alma) · `buco` (represa) · `biro` (sal) · `chiriguare`
(gavilán) · `maure` (algodón) · `urari` (curare) · `piache` (chamán) · `arima` (pez) ·
`duna` (agua) · `bara` (río) · `taya` (yo) · `wana` (ver).

### Sistema morfológico (wayunaiki como referencia)

**Aspecto verbal** (sufijo al verbo):
- `-ka` → completivo: `pescado-ka` = ya pesqué
- `-ni` → continuativo: `naa-ni taya` = voy ahora mismo
- `-da` → prospectivo: `naa-da taya` = iré / quiero ir

**Locativos** (topónimos): `-ana` (lugar de → `coro+ana` = Curiana) · `-bana` (orilla
de) · `-gua` (región de).

**Agentivos**: `-ko` (hombre asociado a → `biro+ko` = salinero) · `-sha` (mujer
asociada a → `maure+sha` = tejedora). **Plural**: `-kana`.

**Posesivos** (prefijos): `ta-` (mi → `ta-barsure`) · `wa-` (nuestro) · `ma-` (sin/no).

### Emergencia lingüística

Cuando un agente necesita nombrar algo sin palabra disponible, aplica las reglas y
propone la forma nueva entre corchetes:

```
[golfete-bana: golfete+-bana = orilla interior del golfete]
```

Si **2 agentes distintos** la usan → entra al léxico comunitario permanente.

## Dashboard Next.js

`curiana_dashboard/` es un frontend Next.js 14 que visualiza la evolución lingüística
en tiempo real desde Supabase (Recharts para los gráficos, Tailwind para el estilo,
`@supabase/supabase-js` para los datos en vivo).

```bash
cd curiana_dashboard
npm install
cp .env.local.example .env.local      # pon NEXT_PUBLIC_SUPABASE_URL / ANON_KEY
npm run dev                            # http://localhost:3000
```

Requiere que el backend haya corrido al menos una simulación con Supabase configurado
(las tablas las crea `supabase_schema.sql`). Ver `curiana_dashboard/DEPLOY.md` para el
despliegue. Estructura: `app/` (rutas), `components/` (gráficos y tablas), `lib/`
(cliente Supabase).
```
curiana_dashboard/
├── app/            # rutas y páginas Next.js
├── components/     # charts (Recharts) + tablas de neologismos
├── lib/            # cliente @supabase/supabase-js
├── package.json
└── .env.local.example
```
