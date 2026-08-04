---
tipo: diseño
ambito: cómo se corre y se mide la próxima simulación
estado: propuesta — requiere decisión de Miguel
depende_de: [D3, D5, D9, D10, D11]
creado: 2026-08-03
---

# Protocolo del Run 1 de la era auditada

> **Premisa que lo motiva:** los seis runs existentes no son comparables entre
> sí porque entre corrida y corrida cambió el motor **y** el instrumento que los
> mide ([[01_que_probaron_los_seis_runs]]). Este documento existe para que eso
> no vuelva a pasar.
>
> **La regla de oro:** *nunca cambiar la conducta y la medición en el mismo paso.*

---

## 1. El principio: la base se congela y se sella

Hoy no se puede saber, mirando un run, sobre qué lexicón corrió. Hay que
reconstruirlo de git, como hizo [[LINEA_DE_TIEMPO]]. Eso se acaba:

**Cada run registra, en su propia fila, la huella de la base sobre la que corrió.**

| Campo nuevo | Qué guarda |
|---|---|
| `lexicon_hash` | SHA-256 del `VOCABULARIO_BASE` serializado y ordenado |
| `lexicon_n` | número de entradas |
| `motor_commit` | el SHA del commit HEAD al arrancar |
| `motor_sucio` | si había cambios sin commitear (un run sucio no es citable) |
| `corpus_hash` | hash de los YAML de `cultura/` |
| `semilla` | la semilla de aleatoriedad, para poder repetir |

Sin esos seis campos, un run **no es evidencia**: es una anécdota.

Implementación: una función `huella_de_base()` en `curiana_database.py`, llamada
al abrir el run y persistida en `simulation_runs`.

---

## 2. Precondiciones — el gate, actualizado

[[PLAN_MAESTRO]] §6 fija el gate original. Lo que la auditoría añadió:

| # | Condición | Estado |
|---|---|---|
| 1 | Lexicón: 0 entradas de familia caquetía sin cita **o sin degradar** | 🟡 19 pendientes → **D10** |
| 2 | Pares c/k resueltos (F2) | 🔴 → **D5** |
| 3 | Las 3 fuentes ALTA minadas (F3, F4, F5) | ✅ **hecho 2026-08-03** |
| 4 | `compilar_corpus.py` en verde (V2) | 🔴 no existe |
| 5 | Citas del corpus verificadas por muestreo (F10) | 🔴 |
| 6 | D1, D3 y D5 tomadas | 🔴 |
| 7 | **La glosa de `-bana` resuelta** | 🟡 → **D9**. Es productivo: los agentes acuñan con él |
| 8 | **El desbalance wayunaiki/lokono resuelto** | 🟠 → **D11**. Cambia de qué lengua se reconstruye |
| 9 | **`export_runs_index.py` reparado** | 🔴 `20091e1f` exporta 0 turnos con 290 respuestas |

**7, 8 y 9 son nuevas** y salieron de esta auditoría. La 8 es la más pesada: si
se decide reequilibrar hacia el lokono, hay que re-derivar la Capa 2 **antes**
del run, no después.

---

## 3. El diseño experimental

### 3.1 Los runs vienen en pares

El único resultado limpio del proyecto es el par ablación de julio. Se
institucionaliza:

> **Ningún run se corre solo.** Cada condición se corre contra un control que
> difiere en **exactamente una** variable, el mismo día, sobre la misma base.

### 3.2 Réplicas, porque hay un LLM en el bucle

Los agentes son Haiku. Dos corridas idénticas **no dan lo mismo**, y hoy no
sabemos cuánto de la diferencia observada es varianza del modelo.

> **Mínimo 3 réplicas por condición**, con semillas distintas. Cualquier efecto
> menor que la dispersión entre réplicas **no se reporta como hallazgo**.

Esto multiplica el costo por 3 — y es justamente por eso que conviene decidir
primero qué pregunta se hace.

### 3.3 La secuencia de hitos

| Hito | Qué es | Criterio de cierre |
|---|---|---|
| **H0 — Base sellada** | `huella_de_base()` implementada y probada | un run de humo registra los 6 campos |
| **H1 — Instrumento fijo** | Métricas revisadas y **congeladas** antes de correr nada | `score_linguistico` no vuelve a tocarse hasta H5 |
| **H2 — Run de calibración** | 1 run corto (10 turnos) solo para verificar tubería | los 6 campos se persisten; el exportador no miente |
| **H3 — Baseline de la era** | 3 réplicas de la condición neutra | dispersión entre réplicas medida y publicada |
| **H4 — Par experimental** | 3 réplicas normal + 3 ablación | la diferencia supera la dispersión de H3 |
| **H5 — Análisis y cierre** | Informe con barras de error | se declara qué quedó probado y qué no |

**H3 es el hito que el proyecto nunca ha tenido**: saber cuánto ruido hay antes
de interpretar señal.

---

## 4. Las métricas hay que rehacerlas

Lo que la auditoría encontró ([[01_que_probaron_los_seis_runs]] §3):

| Métrica | Problema | Qué hacer |
|---|---|---|
| `pct_caquetio` | **saturada** — 5 de 6 runs entre 99.0 y 99.7 | Ya cumplió su función (detectó el 27% inicial). Baja a métrica de salud, no de resultado |
| `avg_score` | **plana** — rango de 0.32 en seis motores distintos | Revisar qué mide. Si no discrimina, no sirve de criterio |
| convergencia | **tres lecturas** no comparables entre sí | Elegir **una** para el veredicto y publicar las tres. Ya está documentado en [[DISENO_KOINE]] §7 |
| — | **no hay barras de error** | Sale de las réplicas (§3.2) |

### La métrica que falta

Ninguna de las actuales responde la pregunta del proyecto:
**¿se transmitió el saber?** El experimento Bana-mana de
[[04_transmision_saber]] la define con precisión — *¿algún agente que solo
presenció vuelve a nombrar a esos ancestros sin que Bana-mana esté presente?* —
y necesita una tabla de eventos rituales en el Observer que **todavía no existe**.

Es una respuesta binaria, narrable y barata. Debería ser el resultado principal
del Run 1, no un extra.

---

## 5. Qué hacer con los seis runs viejos

**Se conservan, etiquetados como lo que son.** No se borran: documentan cómo se
construyó el motor, y el par de ablación sigue siendo evidencia válida dentro de
su propia base.

- `BITACORA_RUNS.md` lleva una cabecera que los declara **era de desarrollo**.
- El sitio público **no re-exporta desde ellos** ([[PLAN_MAESTRO]] §6.4).
- Cualquier cita de sus números lleva la advertencia de comparabilidad.

---

## 6. Lo que este protocolo cuesta

Conviene decirlo antes de empezar: **3 réplicas × 2 condiciones = 6 corridas**
para H4, más H2 y H3. Frente a un run suelto, es entre 7 y 10 veces más API.

La alternativa es más barata y ya sabemos a dónde lleva: seis runs que no se
pueden comparar.

## Enlaces

[[01_que_probaron_los_seis_runs]] · [[LINEA_DE_TIEMPO]] · [[PLAN_MAESTRO]] · [[DISENO_KOINE]] · [[CANON_TIERRA]] · [[DECISIONES_ABIERTAS]]
