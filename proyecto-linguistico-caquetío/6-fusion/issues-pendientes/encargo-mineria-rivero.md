# Encargo de minería — Rivero 1883: los caquetíos del Casanare y el continuo achagua

> Redactado el 2026-09-22 por el agente F1 de la minería 3 («las fuentes que
> faltan»). **No se lanzó**: el coordinador lo lanza en la tanda siguiente
> (modelo Opus 5.5, `isolation: worktree`). Es autosuficiente.

## Antes de nada

1. Lee ENTERO el preámbulo común de la campaña:
   `C:\Users\migue\AppData\Local\Temp\claude\C--Users-migue-OneDrive-Documents-Desarrollo-Curiana-Radio\e151545b-f417-449f-a359-2217e42971dd\scratchpad\PREAMBULO_MINERIA_3.md`
   (ruta absoluta). Manda sobre todo salvo `CLAUDE.md`. Si ya no existe, las
   reglas están en `proyecto-linguistico-caquetío/CLAUDE.md` y en las skills.
2. `proyecto-linguistico-caquetío/CLAUDE.md`, y las skills
   `.claude/skills/minar-fuente/SKILL.md` y `.claude/skills/leer-fuente/SKILL.md`.
3. **Git, al empezar**: rama `campana/mineria3-rivero`, desde `main`;
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`.
   Commits por rutas explícitas.
4. Tu ficha: `proyecto-linguistico-caquetío/4-fuentes/rivero-1883.md`.

## La obra

`fuentes_caquetios/Rivero_1883_Historia_Misiones_Casanare.pdf` (sólo imagen)
y `.txt` (el OCR de archive.org, con un salto de página por hoja: la página
del PDF se cuenta igual que con pdftotext). Impresa ≈ pdf − 21 en el cuerpo,
con tramos a − 19: lee el número impreso. El OCR confunde `Caquetío` con
`Caquetá`: **mira en imagen** todo lo que cites (leer-fuente §3), y si una
zona es ilegible, pásale `curiana_sim/ocr_fuente.py --lang spa` a esas
páginas.

## La pregunta

1. **⭐ Los caquetíos de los Llanos del Casanare.** Rivero nombra presos
   «Caquetíos y Achaguas» (pdf 48 y 50), el pueblo misional de «Caquetíos de
   Pauto» (pdf 222), un misionero «lidiando con la lengua» del pueblo de Pauto
   (pdf 172) y caquetíos en el Guaviare en 1723 (pdf 411). ¿Qué dice de esa
   gente y, sobre todo, de **su lengua** (nombre, parecido con el achagua,
   intérpretes, catecismos, voces)? Es otra polity (regla 4): comparanda
   interna del caquetío, nunca dato de la costa. Si el hallazgo sostiene una
   «tercera polity caquetía», redacta el issue para Miguel (toca
   `curiana_sim/curiana_polities.py`, que tú NO editas).
2. **El continuo achagua**: el pasaje de las «más de veinte Naciones ó
   Provincias» «bajo un mismo idioma» con diferencias «como las que existen en
   Castilla» (p. 21, pdf 42). Verifícalo en imagen y busca todo lo que diga de
   variación, intercomprensión y lenguas francas. Es el referente para
   `5-experimento/DISENO_KOINE.md` que la ficha ya anuncia.
3. **Voces achaguas** con glosa que sirvan de comparanda
   (`curiana_sim/lexicon_achagua.py` es generado: no se toca; propón en YAML).
4. **Fauna** (esquema `fauna:` del preámbulo), `epoca: colonial`.

## Entrega

- `6-fusion/rivero_1883_2026-MM-DD.yaml` con `meta`, hallazgos con `obra:
  rivero-1883`, página impresa, cita verbatim recortada, `epoca`, etiqueta y
  `polity`; y `fauna:`.
- Bitácora nueva en la ficha, `estado_minado`/`cobertura` verdaderos.
- `python curiana_sim/guardianes.py --rapido` en verde; push; PR contra
  `main` sin mergear, cuerpo terminado en
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Informe ≤ 400 palabras: primero lo que del encargo resultó falso al medir.
