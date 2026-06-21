# Idea: sección de perfiles de agentes

Pendiente de retomar en esta rama (`feature/perfiles-agentes`).

## Motivación

Mostrar mejor el trabajo de la simulación: además de las métricas de deriva
lingüística, dar a los 60 personajes históricos un espacio propio donde se
vea quiénes son y cómo "hablaron" a lo largo de la simulación. Le da alma
al proyecto, no solo números.

## Qué queremos construir

Una sección/página `/agentes` en el dashboard con:

- **Grid de tarjetas**: nombre, rol en la comunidad, tier (cacique/adulto/joven).
- **Vista de detalle por agente**: frases célebres, resumen de su arco
  narrativo, aporte léxico (neologismos propuestos/adoptados), línea de
  tiempo de sus turnos.
- Un **agente analista** (Claude Haiku) que, tras cada simulación, lee
  todas las respuestas de un personaje y elige sus frases más célebres /
  con más impacto, con una justificación corta y un score 0-10.

## Qué ya se construyó (commit `f101540`, en esta rama)

- Migración `curiana_sim/supabase/migrations/20260620000000_agent_profiles.sql`
  — tablas `agent_profiles` (rol, resumen de arco, métricas agregadas) y
  `agent_quotes` (frases + justificación + impacto_score), con RLS de
  lectura pública y realtime habilitado.
- `curiana_database.py` — métodos `get_agent_responses`,
  `save_agent_profile`, `save_agent_quote`, `clear_agent_quotes`.
- `curiana_sim/curiana_perfilador.py` — script CLI que corre el análisis
  con Haiku y persiste los perfiles. Uso:
  ```bash
  python curiana_perfilador.py                 # último run, todos los agentes
  python curiana_perfilador.py --run <uuid>
  python curiana_perfilador.py --agent Manaure
  ```

## Qué falta

1. Aplicar la migración `20260620000000_agent_profiles.sql` (cuando se
   decida la base a usar — ver `feature/supabase-local` para el setup
   local que reemplaza temporalmente al proyecto cloud, que llegó a
   8.17 GB de egress sobre el límite de 5 GB del plan Free).
2. Correr `curiana_perfilador.py` contra un run real y revisar la calidad
   de las frases elegidas / justificaciones.
3. Construir la página `/agentes` en `curiana_dashboard` (grid + detalle).
4. Decidir si el perfilador corre automáticamente al final de cada
   `--auto N`, o se deja como paso manual aparte (para no gastar
   llamadas extra a Haiku en cada run de prueba) — quedó sin resolver.
5. Pensar en un retrato/ícono simple por agente (¿generado, ¿genérico
   por tier/etnia/género?).

## Decisión pendiente abierta

¿El perfilador se integra al pipeline automático del orquestador o
se mantiene como paso manual post-simulación? Evaluar costo en
llamadas a Haiku vs. comodidad.
