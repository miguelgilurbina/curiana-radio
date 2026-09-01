## ✅ DECIDIDA — opción A + apagado en ablación (Miguel, 2026-09-01) y APLICADA

**Veredicto**: cablear `normalizar_por_dialecto()` en el **umbral del rescate intra-turno** — el reintento se decide sobre el score normalizado por etnia; **a la base va siempre el score CRUDO**. Y el rescate **se apaga en `--ablacion`**: es una inyección que empuja convergencia y el brazo de control corre sin ella.

Aplicado por `aplicar_tanda_09_01.py`: nueva `curiana_social.necesita_rescate(metr, etnia, ablacion)` con 5 tests (`tests/test_rescate_d3.py`); el orquestador la usa; la nota de código-muerto de `curiana_social` pasó a nota de decisión. Reserva declarada: las densidades objetivo siguen siendo constantes de diseño sin base empírica — acotadas al reintento son operables; calibrarlas desde los runs queda anotado. Registro: `6-fusion/decisiones_tanda_2026-09-01.yaml`.

El dossier que la sirvió, para el registro:

---

## Qué era, medido (no de memoria)

La variación dialectal tenía dos mitades: `prompt_rasgos_dialectales(etnia)` **sí cableada** (inyecta rasgos de habla por etnia en el prompt), y `normalizar_por_dialecto(score, etnia)` — la "justicia L2" que compensaría esa vara — **jamás llamada** desde la auditoría del 2026-07-20. Las densidades objetivo: caquetío 0.65 · aruba 0.60 · guaycarí 0.45 · gayón 0.40 · jirajara 0.35 · caribe 0.25, constantes puestas por nosotros.

## El hallazgo que cambió el problema

**El score crudo SÍ tenía efecto dentro del run**: el rescate intra-turno reintenta cuando `score < 5.0`. Un caribe obedeciendo su propio prompt (densidad 0.25) vivía bajo ese umbral → **reintento crónico empujándolo al caquetío**, pagando una llamada extra al modelo casi cada turno. El motor peleaba contra su propio diseño dialectal.

Y el segundo: **el rescate no estaba gateado por `--ablacion`** — una inyección de convergencia sobreviviendo al brazo de control, con presión correlacionada a la etnia. Para la tesis ("la evidencia de koineización es la DIFERENCIA normal vs. ablación") eso contaminaba el control.

Lo que NO estaba en juego: el prestigio es estático (el score no lo toca) — no había más vías de retroalimentación.

## Las opciones que se sirvieron

**A** cablear en el umbral del rescate, guardar el crudo ← **elegida** (la lección de fase 1 — "el instrumento medía en parte a sus autores", r=−0.48 — prohíbe hornear constantes nuestras en los datos) · **B** eliminar estilo D10 (dejaba vivo el reintento crónico) · **C** normalizar lo almacenado (contamina la serie histórica y rompe comparabilidad — descartada de plano).

Con esto y D1 (#32), la **condición 6 del gate queda cerrada**. Se cierra el issue.
