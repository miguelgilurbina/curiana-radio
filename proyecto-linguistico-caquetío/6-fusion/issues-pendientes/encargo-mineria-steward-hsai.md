# Encargo de minería — HSAI 4 y 5 (1948-1949): qué dice el *Handbook* de los caquetíos y de dónde lo saca

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
3. **Git, al empezar**: rama `campana/mineria3-steward-hsai`, desde `main`;
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`.
   Commits por rutas explícitas.
4. Tus fichas: `4-fuentes/steward-1948-hsai-4.md` (vol. 4, el importante) y
   `4-fuentes/steward-1949.md` (vol. 5, extracto).

## Las obras

- `fuentes_caquetios/Steward_1948_HSAI_vol4_Circum-Caribbean_Tribes.pdf` +
  `.txt` — volumen entero. **El desfase deriva por las láminas** (+ 124 en la
  arqueología de Venezuela, + 136 en los capítulos de Venezuela): lee el
  número impreso de cada página.
- `fuentes_caquetios/Steward_1949_HSAI_vol5_pp655-772_y_bibliografia.pdf` +
  `.txt` — extracto: impresa = pdf + 644 (pp. 655-772) y pdf + 654 (la
  bibliografía).

Son **síntesis de 1948-1949** sobre crónicas del XVI: nada de aquí sube a
`atestiguado` sin la fuente primaria que cite (regla 2). El valor es saber
**de dónde viene cada lugar común** del vault sobre los caquetíos.

## La pregunta

1. **Hernández de Alba, «Tribes of northwestern Venezuela» (vol. 4,
   pp. 469-474)**: saca cada afirmación sobre los caquetíos (jefe, religión,
   parentesco, casas, subsistencia, calendario —«when such and such fruits
   ripen», p. 474—, comercio, guerra) **con la fuente que él cite** (Simón,
   Oviedo y Baños, Castellanos, Aguado, Pérez de Tolosa, Federmann…). Para
   cada una: ¿esa fuente está en el repo (`4-fuentes/bibliografia.yaml`)? ¿El
   vault ya la tenía, y de dónde? ¿Es de la costa o del interior (regla 4)?
2. **Kirchhoff** («Tribes north of the Orinoco», pp. 481-493, y «Food-gathering
   tribes of the Venezuelan Llanos»): los caquetíos de los llanos como
   «overlords» de guamos y otomacos; lo que diga de lenguas y de intercambio.
3. **Kidder II, «The archeology of Venezuela»** (pp. 413-438): lo que dé de
   Falcón y la costa (sitios, cerámica, cronología) como contrapeso a la
   ausencia de `rouse-cruxent-1963` (ver su ficha).
4. **Vol. 5, Parte 3** (pp. 655-668): las cifras de población de «Venezuela,
   north of Orinoco» (86.300 y 144.000 en la tabla de la p. 663, OCR: en
   imagen) y el método. Nivel máximo `hipotetico`, como dice la ficha.
   **Parte 4** (pp. 669-772): cada rasgo atribuido a los caquetíos (jefe en
   hamaca, cenizas bebidas, sacerdote-jefe…) con la fuente que dé.
5. **Rouse, «The West Indies» y «The Arawak»** (vol. 4, pp. 495 ss.): sólo lo
   que toque la esfera de contacto con la costa caquetía o las islas ABC.
6. **Fauna** (esquema `fauna:` del preámbulo) de los capítulos de Venezuela.

## Entrega

- `6-fusion/hsai_caquetios_2026-MM-DD.yaml` con `meta` y, por afirmación:
  capítulo, autor, página impresa, cita verbatim recortada (obra en dominio
  público), fuente que cita, si está en el repo, polity, `epoca`, etiqueta
  (`obra: steward-1948-hsai-4` o `steward-1949`); y `fauna:`.
- Bitácora nueva en las dos fichas, `estado_minado`/`cobertura` verdaderos.
- `python curiana_sim/guardianes.py --rapido` en verde; push; PR contra
  `main` sin mergear, cuerpo terminado en
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Informe ≤ 400 palabras: primero lo que del encargo resultó falso al medir.
