---
tipo: nota-viva
ambito: qué lanzar en la próxima tanda de trabajo desatendido
preparado: 2026-08-04
tablero: TABLERO.md
---

# Siguiente tanda

> **Para una sesión que arranca en frío.** Esta nota dice **qué** lanzar, **en
> qué orden** y —lo más importante— **cómo se encarga el trabajo en este
> proyecto**. La lista de tareas está en los issues; lo que no está en ningún
> lado es la disciplina del encargo, y sin ella una sesión produce material que
> hay que tirar.
>
> Antes de nada: corre `python curiana_sim/generar_tablero.py` y lee
> `TABLERO.md`. Los números de esta nota pueden haber envejecido.

## Por qué esta tanda y no otra

El gate para reanudar simulaciones está en **1 de 9** condiciones. Seis de las
ocho que faltan **dependen de una decisión de Miguel** y no se pueden tocar sin
él. Esta tanda ataca lo que **sí** se puede mover solo, y lo que Miguel pidió
explícitamente: *"seguir engordando el lexicón, seguir minando fuentes y
entrecruzando información"*.

## Las cinco sesiones, en paralelo

| # | Issue | Qué es | Por qué ahora |
|---|---|---|---|
| 1 | [#57](https://github.com/miguelgilurbina/curiana-radio/issues/57) | **Minar Oviedo y Baños** | 519 páginas con texto, **disponibles y nunca leídas**. El programa la señaló por su cobertura de sucesión cacical. La mejor relación esfuerzo/rendimiento del repo |
| 2 | [#59](https://github.com/miguelgilurbina/curiana-radio/issues/59) | **Barridos de Oliver cap. 3** | El capítulo más productivo (15 hechos) solo se minó para familia y geografía. Sin preguntar: economía, cerámica, guerra, religión |
| 3 | [#58](https://github.com/miguelgilurbina/curiana-radio/issues/58) | **Minar Antczak 2017** | 45 pp. open access. Respalda o corrige `parentesco-028/029/032/033`, las entradas más especulativas del corpus, que hoy se apoyan en búsquedas web |
| 4 | [#66](https://github.com/miguelgilurbina/curiana-radio/issues/66) | **`compilar_corpus.py`** | **Condición 4 del gate.** Hoy nada valida los 152 hechos: es el equivalente cultural de los 45 tests del motor |
| 5 | [#41](https://github.com/miguelgilurbina/curiana-radio/issues/41) [#53](https://github.com/miguelgilurbina/curiana-radio/issues/53) [#54](https://github.com/miguelgilurbina/curiana-radio/issues/54) [#55](https://github.com/miguelgilurbina/curiana-radio/issues/55) | **Lote de higiene** | Cuatro arreglos mecánicos que caben en una sesión: el bug de cp1252 y los tres de archivos |

**No lanzar sin Miguel**: cualquier issue con label `decision`, más #45 `tara`,
#47 `saruro` y #40 `FORMAS_SEED` (tocan canon). #42 (exportador) necesita
Supabase levantado, así que tampoco sirve desatendido.

## El patrón de encargo — esto es lo que hay que copiar

Toda sesión de minería lleva **las mismas seis restricciones duras**. Sin ellas
el resultado no se puede fusionar:

1. **NO modificar `curiana_sim/curiana_lexicon.py`.** Se emite una **propuesta**
   en un módulo aparte (`lexicon_<fuente>.py`), como hace
   `minar_zavala_glosario.py`. La fusión al léxico activo es **decisión humana
   explícita** — es la regla de oro 1 del protocolo de descarte.
2. **NO ejecutar comandos de git.** Varias sesiones corren en paralelo sobre el
   mismo repo; consolida y commitea quien las lanzó.
3. **NO correr simulaciones ni gastar API en runs.** Hay moratoria
   ([[PLAN_MAESTRO]] §0).
4. **NO tocar** `TABLERO.md` (se genera), `PLAN_MAESTRO.md`,
   `DECISIONES_ABIERTAS.md` ni `4-fuentes/INDICE_FUENTES.md` — los consolida el
   que lanza, para que no colisionen entre sí.
5. **Envolver `sys.stdout` en UTF-8** bajo `__main__`, nunca al importar. La
   consola de Windows es cp1252 y revienta con `§` o `ü`.
6. **Temporales en el scratchpad del sistema**, nunca en el árbol del repo.

Y **los tres entregables** de una minería:

- El **minador** (`curiana_sim/minar_<fuente>.py`), reproducible y con modo informe.
- La **propuesta** (`curiana_sim/lexicon_<fuente>.py`), con el veredicto y **la
  razón** de cada entrada.
- **La nota de la fuente actualizada** en `4-fuentes/` — «Qué ha dado», «Qué
  falta» y **«Descartes razonados»**. Documentar un descarte vale tanto como un
  hallazgo: evita que alguien lo re-descubra en seis meses.

## Las tres reglas de método que más se olvidan

- **Regla cero del descarte**: *una voz no es caquetía por defecto.* El
  protocolo de 6 filtros está en
  [[02_protocolo_habla_paraguanera]] §3-5 y aplica a cualquier fuente. El
  proyecto ya cometió el error contrario una vez: 441 palabras transducidas sin
  verificar, ~80% de fallo medido.
- **D7 (resuelta)**: cuando la glosa histórica y la identificación científica
  moderna difieren, **se registran las dos** en campos separados —
  `glosa_fuente` (la que habla el agente) e `identificacion_moderna`. Ninguna
  gana.
- **Precontacto ≠ colonial**: nunca tratar un dato de crónica post-contacto
  como norma precontacto sin que el canon ya decida proyectarlo.

## Cómo verificar antes de dar algo por cerrado

```bash
python check_vault_links.py --strict                        # 0 rotos
python -m pytest curiana_sim/tests/ -q                      # 45 passed
PYTHONIOENCODING=utf-8 python curiana_sim/test_quick.py     # 8/8
PYTHONIOENCODING=utf-8 python curiana_sim/auditar_82.py --resumen
PYTHONIOENCODING=utf-8 python curiana_sim/generar_tablero.py
```

**Un test rojo tras una minería suele significar que una palabra reasignada
está cableada en el motor.** No es ruido: es el hallazgo.

## Al consolidar

Un **PR por issue**, no un cajón — la lección de #31, que abrió como V0+V1 y
terminó con siete commits de cosas distintas. Y regenerar el tablero al cerrar,
porque cada `TABLERO.md` commiteado es un punto de la serie temporal que el
proyecto no tenía.

## Lo que Miguel tiene que decidir para que esto siga

Seis condiciones del gate están bloqueadas por él. Por orden de cuánto destraban:

1. **[#39](https://github.com/miguelgilurbina/curiana-radio/issues/39) — D11, wayunaiki vs. lokono.** La de más fondo. **388 de las 441
   candidatas (88%) se transdujeron solo desde wayunaiki**, y Oliver dice que el
   caquetío desciende del lokono. Si se reequilibra, hay que re-derivar la Capa 2
   **antes** del Run 1, no después.
2. **[#38](https://github.com/miguelgilurbina/curiana-radio/issues/38) — D9, `-bana` / `-ana`.** Productivo: contamina cada neologismo que
   acuñen los agentes. La evidencia está reunida en [[morfologia]].
3. **[#46](https://github.com/miguelgilurbina/curiana-radio/issues/46) — `corie`.** Probablemente ni siquiera es decisión: la fuente **y el
   propio canon** dicen *armadillo*; solo el lexicón dice 'choza'.
