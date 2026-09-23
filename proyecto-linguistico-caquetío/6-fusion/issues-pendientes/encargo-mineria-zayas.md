# Encargo de minería — Zayas y Alfonso 1931: las voces taínas que Goeje apoya en Zayas

> Redactado el 2026-09-22 por el agente F1 de la minería 3 («las fuentes que
> faltan»). **No se lanzó** y no es de las prioritarias de esta campaña: el
> coordinador (o Miguel) decide si va en la tanda siguiente o en la próxima
> campaña del taíno. Modelo Opus 5.5, `isolation: worktree`. Autosuficiente.

## Antes de nada

1. Lee ENTERO el preámbulo común de la campaña:
   `C:\Users\migue\AppData\Local\Temp\claude\C--Users-migue-OneDrive-Documents-Desarrollo-Curiana-Radio\e151545b-f417-449f-a359-2217e42971dd\scratchpad\PREAMBULO_MINERIA_3.md`
   (ruta absoluta). Si ya no existe, las reglas están en
   `proyecto-linguistico-caquetío/CLAUDE.md` y en las skills.
2. `CLAUDE.md`, `.claude/skills/minar-fuente/SKILL.md`,
   `.claude/skills/leer-fuente/SKILL.md`, y los YAML de las dos campañas del
   taíno (`6-fusion/taino_*.yaml`, `6-fusion/taino2_*.yaml`).
3. **Git, al empezar**: rama `campana/mineria3-zayas`, desde `main`;
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`.
4. Tu ficha: `4-fuentes/zayas-1931.md` (léela: explica edición y derechos).

## La obra

En git sólo están los `.txt`
(`fuentes_caquetios/Zayas_1931_Lexicografia_Antillana_2ed_t1.txt`, `_t2.txt`,
un salto de página por hoja). Los PDF pesan 381 y 441 MB y **no se
commitean**: para ver una página en imagen, bájalos de dLOC (URL en la ficha)
a tu scratchpad, nunca al repo. Es la **2ª ed. (1931)**: las páginas que cita
Goeje son de la 1ª (1914) y no coinciden.

## La pregunta

1. Las cuatro voces que [[goeje-1939]] apoya en Zayas con página (`anaki`,
   `anaiboa`, `anua`, `manaya`): ¿qué dice Zayas, con qué fuente (cronista)
   y qué página de 1931?
2. Las voces de `6-fusion/taino_lista_maestra_2026-09-22.yaml` sin fuente
   primaria localizada: ¿las trae Zayas y a quién se las atribuye? **Dos
   obras que se copian son una atestación** (minar-fuente §8): lleva cada voz
   a la crónica que Zayas cite, y marca como suya (del editor) toda
   etimología que no venga de la fuente.
3. **Fauna** antillana con nombre indígena (esquema `fauna:` del preámbulo),
   sólo si la fuente la describe.

## Entrega

`6-fusion/zayas_1931_2026-MM-DD.yaml` (`obra: zayas-1931`), bitácora en la
ficha, guardianes `--rapido` en verde, push, PR contra `main` sin mergear
(cuerpo terminado en `🤖 Generated with [Claude Code](https://claude.com/claude-code)`),
informe ≤ 400 palabras que empiece por lo que resultó falso al medir.
