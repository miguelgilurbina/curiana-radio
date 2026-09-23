# Encargo de minería — Federmann (1530-1531): Paraguaná y Coro

> Redactado el 2026-09-22 por el agente F1 de la minería 3 («las fuentes que
> faltan»). **No se lanzó**: el coordinador lo lanza en la tanda siguiente
> (modelo Opus 5.5, `isolation: worktree`). Es autosuficiente.

## Antes de nada

1. Lee ENTERO el preámbulo común de la campaña:
   `C:\Users\migue\AppData\Local\Temp\claude\C--Users-migue-OneDrive-Documents-Desarrollo-Curiana-Radio\e151545b-f417-449f-a359-2217e42971dd\scratchpad\PREAMBULO_MINERIA_3.md`
   (ruta absoluta, fuera del repo). Manda sobre todo salvo `CLAUDE.md`. Si
   esa ruta ya no existe, las reglas equivalentes están en
   `proyecto-linguistico-caquetío/CLAUDE.md` y en las dos skills de abajo.
2. `proyecto-linguistico-caquetío/CLAUDE.md` entero, y las skills
   `.claude/skills/minar-fuente/SKILL.md` y `.claude/skills/leer-fuente/SKILL.md`.
3. **Git, al empezar**: tu rama es `campana/mineria3-federmann`, desde `main`.
   Los PDF sólo están en la rama del buscador, así que haz
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`
   antes de leer nada. Commits por rutas explícitas, nunca `git add -A`.
4. Tu ficha: `proyecto-linguistico-caquetío/4-fuentes/federmann-1916.md` —
   léela entera, sobre todo la bitácora del 2026-09-22.

## La obra

Nikolaus Federmann estuvo en Paraguaná y Coro en 1530-1531: es el testigo
europeo **más temprano** de la costa caquetía después de Ampíes. Tienes tres
textos en `fuentes_caquetios/`:

- `Federmann_1916_Narracion_Primer_Viaje_Arcaya.pdf` + `.txt` — la de Arcaya
  (Caracas 1916), impresa = pdf − 10. ⚠️ **Traducida de la francesa de
  Ternaux (1837), no del alemán** (Arcaya lo dice en la p. 20).
- `Federmann_1557_Indianische_Historia.pdf` — el original (Hagenau 1557), sin
  paginar y con capa de texto inservible: se lee en imagen (leer-fuente §3).
- `Federmann_Kluepfel_1859_Reisen_texto_aleman.pdf` + `.txt` — el alemán
  reeditado en 1859, en tipo romano, OCR legible, impresa = pdf − 8.

Regla de trabajo: lees la de 1916 para localizar; **toda forma indígena,
nombre propio o cifra que vaya a una propuesta se coteja con el alemán**
(Klüpfel por texto y, si decide algo, 1557 en imagen). Declara en cada dato
qué eslabón lo da.

## La pregunta

**¿Qué dice Federmann de la gente de la costa —Paraguaná y Coro— en 1530-1531?**
En concreto, y con página:

1. **Paraguaná** (cap. I, pp. 9-22): el desembarco, la aldea, cuánta gente y
   cómo vive, la india rescatada por Ampíes, el camino a Coro, lo que comen y
   lo que les dan. Qué nodos de `3-mundo/asentamientos.yaml` toca y cuáles
   serían nuevos (propón, no toques el registro).
2. **Coro y su gente** (caps. II-III y XIV): Manaure o sus sucesores (Arcaya
   en nota identifica a una hija del «Gran Cacique de Coro»), jefes,
   parentesco, los «cien indios llamados Caquetíos» porteadores, qué relación
   tienen con los españoles.
3. **Lengua**: intérpretes (quiénes, qué lenguas, cómo se comunicaban),
   **toda voz indígena** que aparezca (en el alemán, con su grafía; y la de
   la traducción al lado), nombres de pueblos y personas.
4. **El seretón** (pregunta de Miguel del 2026-09-11, ver la ficha): ¿hay en
   Federmann un hombre que se transforma, o una palabra parecida? Búscalo en
   el alemán y por el concepto, no sólo por la forma. Un cero se declara con
   lo que se buscó (regla 6).
5. **Fauna** (esquema `fauna:` del preámbulo): todo animal, con su nombre en
   la fuente en las dos lenguas, lugar y época `contacto-temprano`.
6. **Los caps. VIII (p. 59) y XII (p. 107)** son los caquetíos del interior
   (Yaracuy/Barquisimeto): **otra polity**. Mínalos también —aldeas
   fortificadas, confederaciones, «cinco a ocho familias por casa»—, pero
   cada dato marcado `polity: interior` y nunca como dato de la costa
   (regla 4). Coteja las citas que la ficha ya trae de segunda mano.

## Entrega

- `6-fusion/federmann_1530_costa_2026-MM-DD.yaml` (la fecha del día en que
  trabajes) con: `meta` (ediciones, cadena de traducción, desfases medidos,
  qué se leyó y qué no), los hallazgos por esfera (geografía política,
  asentamientos, familia, lengua, creencia, ecología) cada uno con `obra`
  (`federmann-1916` — la bibliografía ya tiene esa clave), página impresa,
  cita verbatim recortada, `epoca` y etiqueta epistémica; y `fauna:`.
- Bitácora nueva en la ficha (qué preguntaste, qué hallaste, qué no;
  `estado_minado` y `cobertura` que digan la verdad). No toques `sostiene`.
- Si algo pide decisión de Miguel, un issue en `6-fusion/issues-pendientes/`.
- `python curiana_sim/guardianes.py --rapido` en verde. Push y PR contra
  `main` con `gh pr create`, **sin mergear**; el cuerpo termina con
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Informe ≤ 400 palabras: primero lo que del encargo resultó falso al medir.
