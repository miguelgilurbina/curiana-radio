# Curiana — Simulación Comunitaria Caquetía

Comunidad caquetía del **Golfete de Coro** (Curiana, Falcón), siglo XIV–XV, pre-contacto europeo.

> "Curiana: territorio donde estaban asentados los caquetíos." — Zavala Reyes (2015, nota 4)

## Archivos

| Archivo | Descripción |
|---|---|
| `curiana_agents.py` | 60 agentes: Tier I (15 protagonistas), Tier II (33 tipificados), Tier III (12 fondo) |
| `curiana_state.py` | Estado del mundo: tiempo, clima, eventos, catálogo de eventos activables |
| `curiana_orchestrator.py` | Director/orquestador principal. Loop interactivo o automático. |
| `curiana_README.md` | Este archivo |

## Requisitos

```bash
pip install anthropic
export ANTHROPIC_API_KEY="tu-clave-aquí"
```

## Uso

### Modo interactivo (recomendado para test run)
```bash
python curiana_orchestrator.py
```

Comandos dentro de la simulación:
- `[Enter]` → Avanzar turno automáticamente
- `habla Shaboro` → Conversar directamente con un agente
- `habla Tawaka` → etc.
- `estado` → Ver estado actual de la comunidad
- `evento niño_enfermo` → Forzar un evento específico
- `salir` → Guardar y salir

### Modo automático (10 turnos = 5 días)
```bash
python curiana_orchestrator.py --auto 10
```

## La Comunidad

**60 agentes** organizados en 3 tiers:

| Tier | Cantidad | Descripción |
|---|---|---|
| I — Protagonistas | 15 | System prompt completo ~180 palabras. Personalidad, relaciones, quirks. |
| II — Tipificados | 33 | System prompt ~70 palabras. Rol + rasgos + actividad. |
| III — Fondo | 12 | Descripción de 1 frase. Solo contexto ambiental. |

### Composición étnica
- Caquetíos: ~43 agentes (lengua nativa)
- Guaycarí: 5 (Caribe, bilingüe fluido)
- Jirajaras/Gayones: 3 (Macro-Chibcha, L2 Caquetío con errores)
- Caribe expansionista: 1 (Caquetío mínimo, reluctante)
- Caquetío de Aruba: 1 (acento de islas)

### Calendario comprimido
- 1 turno = media jornada (mañana o tarde)
- 1 día = 2 turnos
- Estaciones: Seca (viento + pesca + comercio) / Lluvias (siembra + ritual)

## Protagonistas Tier I (nombres)

Manaure · Shaboro · Nubiri-sha · Watapana · Dara-ko · Paugis-sha · Biro-ko · Tawaka · Saruro-sha · Chiriguare · Kadushi · Buio-sha · Corie-ko · Dare-nu · Marokoto-ni

## Estado Inicial del Test Run

- Día 1, Amanecer, inicio de la Seca
- Shaboro tuvo un sueño grave durante la noche
- El nivel de sal (biro) está bajo — se necesita ir al salinar
- Manaure no ha salido todavía de su casa

## Costos estimados (Haiku)

| Escenario | Turnos | Costo aprox. |
|---|---|---|
| Test run mínimo | 4 turnos (2 días) | ~$0.02–0.05 |
| Sesión media | 10 turnos (5 días) | ~$0.05–0.15 |
| Semana completa | 24 turnos | ~$0.20–0.50 |

*Haiku es ~20x más barato que Sonnet. Ideal para simulaciones de comunidad.*

## Arquitectura

```
[Usuario / Script automático]
         ↓ input / [Enter]
[Director Agent]
   · Decide evento del turno
   · Selecciona agentes activos
   · Narra el cierre de turno
         ↓
[Agentes activos (3-6 por turno)]
   · Tier I: System prompt completo + contexto dinámico
   · Tier II: System prompt compacto + contexto dinámico
   · Cada agente tiene memoria ligera (últimas 3 interacciones)
         ↓
[State Manager]
   · Actualiza día/turno/momento
   · Registra historial de eventos
   · Persiste en JSON entre sesiones
```

## Notas lingüísticas

Los agentes responden en **español con interferencia caquetía**:
- Aspecto en lugar de tiempo: "ya pescado-ka" (completivo), "estoy-pescando-ni" (continuativo)
- Vocabulario caquetío insertado: *barsure* (alma), *buco* (represa), *biro* (sal), *chiriguare* (gavilán), *maure* (algodón), *urari* (veneno/medicina), *Curiana* (territorio)
- Jirajaras: errores de L2 (prefijos omitidos, orden alterado)
- Caribe Marokoto-ni: sintaxis directa, Caquetío mínimo
