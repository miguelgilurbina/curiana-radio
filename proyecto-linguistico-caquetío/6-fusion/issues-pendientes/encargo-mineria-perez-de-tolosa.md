# Encargo de minería — Pérez de Tolosa 1546: la costa caquetía veinte años después

> Redactado el 2026-09-22 por el agente F1 de la minería 3 («las fuentes que
> faltan»). **No se lanzó**: el coordinador lo lanza en la tanda siguiente
> (modelo Opus 5.5, `isolation: worktree`). Es autosuficiente.

## Antes de nada

1. Lee ENTERO el preámbulo común de la campaña:
   `C:\Users\migue\AppData\Local\Temp\claude\C--Users-migue-OneDrive-Documents-Desarrollo-Curiana-Radio\e151545b-f417-449f-a359-2217e42971dd\scratchpad\PREAMBULO_MINERIA_3.md`
   (ruta absoluta, fuera del repo). Manda sobre todo salvo `CLAUDE.md`. Si ya
   no existe, las reglas están en `proyecto-linguistico-caquetío/CLAUDE.md` y
   en las dos skills de abajo.
2. `proyecto-linguistico-caquetío/CLAUDE.md` entero, y las skills
   `.claude/skills/minar-fuente/SKILL.md` y `.claude/skills/leer-fuente/SKILL.md`.
3. **Git, al empezar**: rama `campana/mineria3-perez-de-tolosa`, desde `main`;
   `git fetch origin` y `git merge origin/campana/mineria3-fuentes-que-faltan --no-edit`
   (el PDF sólo está en esa rama). Commits por rutas explícitas.
4. Tu ficha: `proyecto-linguistico-caquetío/4-fuentes/perez-de-tolosa-1546.md`
   — su bitácora del 2026-09-22 tiene el mapa del apéndice.

## La obra

`fuentes_caquetios/Oviedo_Banos_1885_FernandezDuro_t2_Documentos.pdf` + `.txt`:
el t. II de Oviedo y Baños editado por Cesáreo Fernández Duro (Madrid, 1885),
con el apéndice «DOCUMENTOS» desde la p. 207. Impresa = pdf − 11 (con saltos
en las láminas: comprueba el número impreso). OCR de archive.org: `ç`, tildes
y cortes de línea fallan; toda cita que vaya a decidir algo se mira en imagen.

Lo tuyo son las **cartas y la relación del Ldo. Juan Pérez de Tolosa** (1546):
primera carta p. 219, **«Relación de las tierras y provincias de la
gobernación de Venezuela» pp. 225-235**, segunda carta p. 236, tercera carta
pp. 248-258. Lee además, porque van juntos y nadie los ha minado: la carta de
Ampíes (p. 209), la «Relación de diferentes Gobernadores» anónima (p. 215) y
el interrogatorio de la pesquisa contra los Welser (p. 259 ss.).

## La pregunta

**¿Cómo era la costa caquetía —Coro, Paraguaná, sotavento y barlovento— en
1546, según quien la gobernó?** Con página, para cada punto:

1. **Asentamiento y demografía**: «medianos pueblos», cuántos, dónde; la
   Paraguaná «casi despoblada» («no hay en toda ella trecientos indios»); el
   pasaje de las **«cuatrocientas casas»** que citaba una obra secundaria —
   **no sale con una búsqueda simple**: búscalo bien (OCR partido, cifra en
   número) y, si no está, dilo con lo que buscaste. Cruza con
   `3-mundo/asentamientos.yaml` (propón, no toques).
2. **Subsistencia**: caza y pesca, jagüeyes y agua, «ropa de hamacas», lo que
   daban a los españoles; y el despoblamiento y la trata (Alfinger, Espira,
   esclavos de Paraguaná). Todo con `epoca: contacto-temprano` o `colonial`:
   **nada de esto es norma precontacto** sin decisión explícita (regla 3).
3. **⭐ Lengua**: «aunque algo difieren en la habla á los de Coro» (p. 234,
   los caquetíos de los llanos). Es un testigo del s. XVI de variación
   dialectal entre polities caquetías. Transcríbelo en imagen, sitúalo (qué
   gente, qué región) y propón a qué toca (regla 4, `curiana_social.py`,
   `5-experimento/DISENO_KOINE.md`) en un issue si pide decisión. Busca
   además toda otra mención de lengua, intérpretes o voces indígenas.
4. **Manaure y los jefes**: «Manaore, el mayor principal que en la gente
   caquetia se hallaba» (tercera carta, p. 248), las canoas que Alfinger le
   quitó (interrogatorio), y todo jefe con nombre.
5. **Fauna** (esquema `fauna:` del preámbulo), en especial pesca y caza.
6. Marca lo que es de **Barquisimeto/Tocuyo/llanos** como otra polity.

## Entrega

- `6-fusion/perez_de_tolosa_1546_2026-MM-DD.yaml` con `meta` (edición,
  desfase medido, qué se leyó y qué no), hallazgos por esfera con `obra:
  perez-de-tolosa-1546` (Ampíes, la relación anónima y el interrogatorio:
  proponles clave o cítalos como documentos del mismo tomo, y dilo),
  página impresa, cita verbatim recortada, `epoca`, etiqueta; y `fauna:`.
- Bitácora nueva en la ficha, con `estado_minado`/`cobertura` verdaderos.
- Issues en `6-fusion/issues-pendientes/` para lo que pida decisión.
- `python curiana_sim/guardianes.py --rapido` en verde; push; PR contra
  `main` sin mergear, cuerpo terminado en
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Informe ≤ 400 palabras: primero lo que del encargo resultó falso al medir.
