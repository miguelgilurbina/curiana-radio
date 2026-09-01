# Dossier D3 — `normalizar_por_dialecto()`: cablearla o eliminarla

> Borrador de comentario para [#34]. Publicar con:
> `gh issue comment 34 --body-file 6-fusion/issues-pendientes/comentario-34-dossier-d3.md`
> (quitando esta cabecera). Preparado 2026-08-31 para la tanda de decisiones.

---

## Qué es, medido (no de memoria)

`curiana_social.py` §IV define la variación dialectal en dos mitades:

1. **`prompt_rasgos_dialectales(etnia)` — SÍ cableada** (`curiana_orchestrator_v2.py:236`):
   inyecta en el prompt los rasgos de habla por etnia ("SVO estricto, léxico
   caquetío mínimo" para un caribe).
2. **`normalizar_por_dialecto(score, etnia)` — NO cableada** (0 llamadas fuera
   de sus tests y su smoke test): escalaría el score crudo por la densidad
   objetivo del dialecto (`score × 0.65/objetivo`, acotado a 10) — "justicia
   L2": no medir al guaycarí con la vara del nativo.

Las densidades objetivo son **constantes puestas por nosotros** (caquetío
0.65 · aruba 0.60 · guaycarí 0.45 · gayón 0.40 · jirajara 0.35 · caribe
0.25), sin base empírica declarada.

## El hallazgo que cambia el problema

**El score crudo SÍ tiene efecto dentro del run.** No es solo una métrica que
se guarda: el *rescate intra-turno* (`orchestrator:289-303`) reintenta la
respuesta cuando `score < 5.0` o hay fuga a otra lengua arahuaca.

La consecuencia de la asimetría actual (mitad 1 cableada, mitad 2 no):

- El prompt le dice al caribe "habla con léxico caquetío mínimo" (densidad
  objetivo 0.25).
- El rescate lo castiga por obedecer: con esa densidad, `score < 5.0` es su
  estado normal → **reintento crónico empujándolo al caquetío**.
- **El motor pelea contra su propio diseño dialectal**, y gasta tokens en
  ello (cada rescate es una llamada extra al modelo).

Y un segundo hallazgo de diseño experimental: **el rescate NO se apaga con
`--ablacion`** (no está gateado por el flag, medido en el orquestador). Es
una inyección que empuja convergencia y sobrevive al brazo de control — y
dispara *más* para los no nativos, así que el diferencial de presión está
correlacionado con la etnia. Para la tesis de koiné ("la evidencia es la
DIFERENCIA normal vs. ablación") eso contamina el control.

## Lo que NO está en juego

- El prestigio es estático (explícito > etnia > tier): el score no lo toca.
  No hay más vías de retroalimentación que el rescate.
- Los rasgos de prompt (mitad 1) funcionan y nadie propone tocarlos.

## Las opciones, con su contra

**A · Cablear en el RESCATE, no en la métrica** *(recomendada)*.
El umbral del reintento se evalúa sobre el score normalizado
(`normalizar_por_dialecto(metr["score"], etnia) < 5.0`); lo que se guarda en
la base sigue siendo el score CRUDO.
- A favor: elimina el reintento crónico del no nativo; la medición queda
  intacta (la lección de fase 1 —"el instrumento medía en parte a sus
  autores"— desaconseja hornear constantes nuestras en los datos
  almacenados); la función deja de ser código muerto con UN caller claro.
- Contra: las densidades objetivo siguen siendo constantes de autor — pero
  acotadas a una decisión de reintento, no a los datos. Calibrarlas
  empíricamente (de los runs) queda como mejora declarada.

**B · Eliminar** (con la disciplina de D10: se archiva con su porqué, no se
borra el rastro).
- A favor: menos superficie; la métrica ya carga dos avisos (pct saturada
  #69, confusor de longitud r=−0.48) y no necesita un tercero.
- Contra: deja VIVO el reintento crónico anti-caribe — la asimetría de hoy,
  pero ya sin documentar como intención pendiente. Habría que al menos
  gatear el rescate por etnia o por `--ablacion`, que es… volver a la
  opción A por la puerta de atrás.

**C · Cablear en la métrica almacenada** (normalizar el score que va a la
base).
- Contra fuerte: contamina la serie histórica (los runs viejos son crudos),
  hornea las constantes de autor en el dato, y rompe la comparabilidad del
  análisis por agente que ya exige controlar la longitud del prompt. No la
  recomendamos ni como variante.

## Decisión adyacente que este dossier destapa (una línea)

¿El rescate intra-turno debe apagarse en `--ablacion`? Hoy sobrevive al
brazo de control. Si la respuesta es sí, es un `and not ablacion` en el
orquestador — y el protocolo del run 1 lo declara.

## Qué cierra

La condición 6 del gate exige D3 decidida (PLAN_MAESTRO §6.3). Cualquiera de
A o B la cierra; A además arregla la asimetría medida.
