# Curiana Dashboard — Deploy en Vercel

## 1. Preparar variables de entorno

Copia `.env.local.example` → `.env.local` y agrega tus valores de Supabase:

```
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

Encuéntralos en tu proyecto Supabase: **Settings → API → Project URL / anon key**.

## 2. Instalar y correr localmente

```bash
cd curiana_dashboard
npm install
npm run dev
# → http://localhost:3000
```

## 3. Deploy en Vercel

```bash
# Primera vez (desde la carpeta curiana_dashboard)
npx vercel

# Agregar variables de entorno en el wizard:
#   NEXT_PUBLIC_SUPABASE_URL = ...
#   NEXT_PUBLIC_SUPABASE_ANON_KEY = ...

# Re-deploy
npx vercel --prod
```

O directamente desde el Dashboard de Vercel:
- Conecta el repo de GitHub
- Establece el root directory como `curiana_dashboard`
- Agrega las env vars en **Settings → Environment Variables**

## 4. Conectar simulación Python

En el mismo directorio que el orquestador, crea o edita el `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...        # service_role key (no el anon key)
LANGSMITH_API_KEY=ls__...          # opcional
LANGSMITH_PROJECT=curiana          # opcional
```

Luego:

```bash
# Sembrar léxico en Supabase (solo una vez)
python curiana_database.py seed

# Correr simulación (guarda en Supabase automáticamente)
python curiana_orchestrator_v2.py --auto 20
```

El dashboard en Vercel se actualiza en tiempo real mientras corre la simulación.

## Estructura del proyecto

```
curiana_dashboard/
├── app/
│   ├── layout.tsx          # Nav + root layout
│   ├── page.tsx            # Dashboard principal (real-time)
│   ├── lexicon/page.tsx    # Explorador del léxico
│   └── neologisms/page.tsx # Neologismos propuestos/adoptados
├── components/
│   ├── LanguageDriftChart.tsx  # Area chart de deriva lingüística
│   └── AgentFeed.tsx           # Feed de respuestas en tiempo real
├── lib/
│   └── supabase.ts         # Cliente Supabase + tipos TypeScript
└── DEPLOY.md               # Este archivo
```
