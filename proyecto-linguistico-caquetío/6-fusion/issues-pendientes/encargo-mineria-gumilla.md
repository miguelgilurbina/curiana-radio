# Encargo de minería — Gumilla 1791: comparanda achagua (prioridad baja)

> Redactado el 2026-09-22 por el agente F1 de la minería 3 («las fuentes que
> faltan»). **No se lanzó**: el coordinador decide si lo lanza (modelo Opus
> 5.5, `isolation: worktree`). Es autosuficiente. Prioridad **baja**: si hay
> que elegir, van antes Federmann, Pérez de Tolosa, Rivero y el HSAI.

## Antes de nada

1. Lee ENTERO el preámbulo común de la campaña:
   `C:\Users\migue\AppData\Local\Temp\claude\C--Users-migue-OneDrive-Documents-Desarrollo-Curiana-Radio\e151545b-f417-449f-a359-2217e42971dd\scratchpad\PREAMBULO_MINERIA_3.md`
   (ruta absoluta). Si ya no existe, las reglas están en
   `proyecto-linguistico-caquetío/CLAUDE.md` y en las skills.
2. `proyecto-linguistico-caquetío/CLAUDE.md`, y las skills
   `.claude/skills/minar-fuente/SKILL.md` y `.claude/skills/leer-fuente/SKILL.md`.
3. **Git, al empezar**: rama `campana/mineria3-gumilla`, desde `main`;
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`.
4. Tu ficha: `4-fuentes/gumilla-1791.md`. Y la de [[gilij-1780-1783]], que lo
   discute, y las de Neira y Ribero 1762 y Fabo 1911 (la comparanda achagua
   que el proyecto ya tiene).

## La obra

`fuentes_caquetios/Gumilla_1791_Historia_Natural_Orinoco_t1.pdf`/`_t2.pdf` +
sus `.txt` (capa de texto de archive.org). OCR del XVIII: `s` larga, `ſ`,
`ç`; el desfase pdf→impresa **no es constante** (t. I: − 24/− 32/− 34; t. II:
− 8/− 10/− 12): número impreso de cada página. `caquet` da 0 en los dos
tomos: verifica con variantes antes de cerrarlo.

## La pregunta

1. **Voces achaguas** (y sálivas) con glosa, cada una cotejada con el
   achagua de Neira y Ribero 1762 (`6-fusion/achagua_neira_ribero_1762.yaml`)
   y Fabo 1911: ¿coincide, difiere, no está? Es la misma calibración que
   leer-fuente §4.4. Propuesta en YAML; `lexicon_achagua.py` no se toca.
2. **Lo que diga de lenguas**: lenguas generales, intérpretes, variación,
   cómo aprendían los misioneros. Referente para la koiné, no dato caquetío.
3. **Cualquier mención de caquetíos** (con variantes de grafía) o de la costa.
4. **Fauna** (esquema `fauna:` del preámbulo), `epoca: colonial`, región
   Orinoco/llanos — nada es de Paraguaná sin decirlo la fuente.

## Entrega

`6-fusion/gumilla_1791_2026-MM-DD.yaml` (`obra: gumilla-1791`), bitácora en
la ficha, guardianes `--rapido` en verde, push, PR contra `main` sin mergear
(cuerpo terminado en `🤖 Generated with [Claude Code](https://claude.com/claude-code)`),
informe ≤ 400 palabras que empiece por lo que resultó falso al medir.
