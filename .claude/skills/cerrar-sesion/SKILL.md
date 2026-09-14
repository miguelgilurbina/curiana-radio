---
name: cerrar-sesion
description: Dejar el trabajo del proyecto lingüístico caquetío en estado de traspaso, para que otra sesión arranque en frío sin preguntar. Mide (guardianes, tablero con --gh), rescata lo valioso del scratchpad, publica o lista los borradores, escribe el handoff o la revisión en 1-plan/ sin cifras a mano, commitea por rutas y abre el PR. Usar cuando se pida cerrar, terminar, dejar todo listo, hacer el traspaso o el handoff, resumir dónde quedamos para la próxima sesión, preparar o abrir el PR, o antes de que acabe un bloque de trabajo de varios días.
---

# Cerrar una sesión

Destilado del handoff del 2026-09-11, de la revisión pre-era 2 del 2026-09-12 y
de los PR #118 y #125. Cada paso está porque saltárselo costó algo que aquí se
nombra.

«Estado de traspaso» es lo que el handoff del 09-11 dice antes que nada: *«no
hay nada roto ni a medio hacer»*, y lo que queda son decisiones con nombre. Una
sesión nueva, sin esta conversación, tiene que poder:

- ver el estado medido sin fiarse de nadie (`TABLERO.md`, `6-fusion/BANDEJA.md`);
- saber qué espera a Miguel y qué no;
- encontrar **en el repo** todo lo que esta sesión averiguó;
- dar el siguiente paso sin tener que deducirlo otra vez.

## 1. Medir

```bash
cd proyecto-linguistico-caquetío
python curiana_sim/guardianes.py            # entero: --rapido se salta los tests
python curiana_sim/generar_tablero.py --gh
python curiana_sim/generar_bandeja.py
git status --short
```

- **Los guardianes, enteros.** Los tests son justo lo que se mueve cuando cambia
  el lexicón.
- **El tablero, con `--gh`.** Sin red, el gate cuenta como abiertas las
  decisiones que ya están cerradas: 3 de 9 donde eran 6 (`051c746`), 3 de 9
  donde eran 7 (`09545d8`), y otra vez el 2026-09-13.
- **Un guardián en rojo no se cierra en silencio.** Se arregla, o el handoff dice
  cuál está en rojo, por qué y cómo se arregla. `1-plan/HARNESS.md` reconoce que
  hay estados intermedios legítimos; el handoff es donde se declaran.
- **`git status`: cada fichero sin trackear** o se añade por ruta, o va al
  `.gitignore` (una fuente pesada, por D8), o se borra. No hay cuarta opción, y
  `git add -A` no es ninguna de las tres: barrió una carpeta sin trackear dos
  veces (`67a0f53`, `65a14c1`).

## 2. Vaciar el scratchpad de lo que vale

Lista el scratchpad de la sesión y decide fichero a fichero:

| Si es… | Va a… |
|---|---|
| una medición, una tabla extraída, un censo | `6-fusion/<tema>.yaml`, o el script que lo produce a `6-fusion/scripts/` |
| un borrador de issue o de comentario | `6-fusion/issues-pendientes/` |
| texto u OCR de una fuente | `fuentes_caquetios/OBRA.txt` o `.ocr.txt` (`leer-fuente` §1-2) |
| una lectura en imagen | el YAML de transcripción en `6-fusion/` (`leer-fuente` §4) |
| el script de un solo uso que aplicó algo | `6-fusion/scripts/`, citado en `aplicado_por` |
| un recorte PNG o una salida regenerable | se queda |

Por qué: la medición de D9 del 2026-08-14 se salvó de milagro; la pasada OCR de
Oliver del 2026-08-17 se perdió. Y hay una razón menos obvia, la del seretón:
*«al comprobar una afirmación propia, el repo incluye lo que uno ya escribió»*.
Eso sólo funciona si lo que uno escribió está en el repo.

## 3. Borradores y decisiones: publicados, o con nombre

- **La sección «Redactado y sin publicar» de la BANDEJA.** Cada borrador o se
  publica (`fusionar-propuesta` §11, con el visto bueno de Miguel), o queda
  listado en el handoff con lo que espera. El PR #125 cerró con «la cola de
  borradores queda en cero»; el handoff del 09-11 los listó («publicar los 6
  issues»). Las dos cosas valen. Lo que no vale es no decirlo.
- **La tanda de decisiones.** Cada decisión tiene su `estado`: `CERRADA`,
  `APLICADA`, `EN CURSO`, o abierta y a la espera de Miguel. Si algo está
  **fallado pero no aplicado**, se dice con esas palabras: el nivel C estuvo así
  un día entero, y fue lo único que el handoff del 09-11 marcó como «escrito
  pero no aplicado».
- **Cada decisión pendiente** con el número de issue, las salidas posibles, la
  recomendación y lo que bloquea.

## 4. Las bitácoras, al día

- **La ficha de cada fuente tocada** (`4-fuentes/<slug>.md`). En el frontmatter:
  `estado_minado`, `cobertura` (qué pregunta se le hizo, porque «minado» no es
  «agotada»), `verificado` y `minado`. En el cuerpo: «Qué ha dado» y «Qué NO se
  hizo» o «Qué falta». `sostiene` no se toca a mano.
- **La propuesta en `6-fusion/`**: `meta.fusionado`, o «aplicado», si se fusionó.
- **Lo que la sesión aprendió fallando va a la skill o a `CLAUDE.md`, en el
  commit de esta sesión**, no sólo al handoff. Así se hizo con «agotar el repo
  antes de salir a la web» (`b17e67d`) y con la regla 4 ampliada (`c3beaef`:
  «queda en la regla 4 de CLAUDE.md y en la skill de la campaña, que es donde se
  escribe»). Por eso el handoff del 09-11 pudo decir «todo esto está ya en las
  dos skills».

## 5. El handoff o la revisión, en `1-plan/`

`1-plan/SIGUIENTE_TANDA.md` es la nota viva: se pone al día la sección cuyo
estado cambió (el commit `9404bd2` tocó su §A.3). El handoff es el traspaso con
fecha de un bloque de trabajo: un encargo nuevo de Miguel, un bloque de varios
días, o lo que haya que saber antes de un PR grande. La revisión es la auditoría
medida que Miguel pide («revisar que no tengamos ningún agujero»).

- **Nombre**: `1-plan/HANDOFF_AAAA-MM-DD.md` o
  `1-plan/REVISION_<TEMA>_AAAA-MM-DD.md`.
- **Frontmatter**:

  ```yaml
  ---
  tipo: handoff                      # o revision
  de: sesión del 2026-09-10/11 (campaña de topónimos, Jahn, D11 fase 1)
  para: la siguiente sesión
  encargo_de_miguel: >-
    «el encargo, literal»
  sustituye_en_parte_a: HANDOFF_2026-09-11.md   # si procede
  ---
  ```

- **La estructura que funcionó en el handoff** (09-11): «Lo primero que hay que
  saber» (si hay algo roto, en qué rama, si está empujada); 1. Dónde está el
  proyecto, medido; 2. Lo que espera decisión de Miguel; 3. El encargo nuevo:
  qué hay, qué buscar con nombre y apellido, y cómo cruzarlo cuando llegue;
  4. Los programas abiertos; 5. Lo aprendido para no repetirlo; 6. Los flecos
  técnicos.
- **La de la revisión** (09-12): «Cómo se midió»; lo que se cerró antes de
  revisar (tabla con commit y efecto medido); los agujeros, ordenados por lo que
  bloquean; el orden propuesto; y «lo que no es agujero aunque lo parezca».
- **Sin cifras a mano.** Es mejor el puntero («`TABLERO.md` §4», «`meta.cobertura`
  del YAML»). Si un número hace falta para entender algo, se dice de dónde sale y
  cuándo se midió, como abre la revisión: *«Todo lo que lleva número sale de
  correr, hoy: guardianes.py, generar_tablero.py --gh… No copiar cifras de aquí a
  otro sitio»*. El porqué está medido: el lexicón tenía 1.676 entradas en el
  handoff del 09-11, 1.894 al día siguiente y 5.518 al abrir el PR.
- **El handoff anterior no se reescribe.** Se le pone una línea arriba que
  apunte al nuevo: «> **2026-09-12**: el estado vivo está en
  [[REVISION_PRE_ERA2_2026-09-12]]. Esto queda como registro de lo que se
  traspasó».
- **Los wikilinks `[[...]]` resuelven por basename**, y el guardián «grafo del
  vault» falla si hay uno roto. Después de escribir, vuelve a correr los
  guardianes.

## 6. Commits y push

- **Por ruta**, y `git status` limpio al final.
- **El estilo** está en `fusionar-propuesta` §12. El commit de cierre suele ser
  `docs(handoff)` o `docs(plan)`.
- **El tablero regenerado va en el commit que cambió lo que mide**, o en uno
  propio si se regenera después: `chore(medido)` (`09545d8`) o
  `chore(fuentes)` (`5da70ba`).
- **Empuja la rama.** El estado de la rama es parte del traspaso: la revisión
  del 09-12 lo dejó dicho («va por 14 commits sobre `main`, empujada, sin PR»).

## 7. El PR

Abrir un PR publica: si Miguel no lo ha pedido, pregúntale antes.

```bash
gh pr create --base main --head <rama> --title "<qué consigue la rama>" --body-file <cuerpo.md>
```

El cuerpo, sobre el modelo del #125:

```markdown
## Qué cierra esta rama

N commits (fechas) que … Todo medido por `guardianes.py` y `generar_tablero.py --gh`;
las cifras de abajo son las del tablero al abrir el PR, no copiadas de otro sitio.

### <tema>
### Decisiones tomadas en el tablero
`#39` D11 · `#37` D8 · … Registro: `6-fusion/decisiones_tanda_<fecha>.yaml`. Abiertos nuevos: …
### El gate
### Lo que conviene saber al revisar
- los ficheros generados del diff, y dónde se corrigen (el YAML, no el módulo)
- lo que no viaja en git (D8) y dónde está
- dónde está el handoff o la revisión
- los flecos medidos y no tocados
```

- **El título** dice qué consigue la rama, con el resultado: «D11 ejecutada:
  Perea entero, el achagua como comparanda, F8 saneada y siete decisiones
  cerradas — el gate sin rojos».
- **Si hubo correcciones sobre la marcha, van en su sección**, como en el #118
  («Correcciones hechas sobre la marcha»): lo que se afirmó, que era falso, y
  dónde se retiró. El proyecto mide lo que no encuentra tanto como lo que
  encuentra.
- Al final, la línea de atribución que indique el harness.

## 8. Después del merge

```bash
git checkout main && git pull
cd proyecto-linguistico-caquetío
python curiana_sim/generar_tablero.py --gh
python curiana_sim/generar_cronica.py       # 1-plan/CRONICA.md: cada cambio que llegó a main
```

Y un commit `chore(medido): tablero remedido con red y crónica al día tras el
merge de #N`, como `09545d8` tras el #118.

## 9. Lista de verificación

- [ ] `guardianes.py` entero, en verde, o el rojo declarado en el handoff
- [ ] `generar_tablero.py --gh` y `generar_bandeja.py` regenerados
- [ ] scratchpad revisado: nada valioso fuera del repo
- [ ] borradores publicados, o listados con lo que esperan
- [ ] tanda de decisiones con el `estado` de cada una
- [ ] fichas de fuente y propuestas con su estado real
- [ ] lecciones en la skill o en `CLAUDE.md`, no sólo en el handoff
- [ ] handoff o revisión sin cifras a mano, y el anterior apuntando al nuevo
- [ ] commits por ruta, `git status` limpio, rama empujada
- [ ] PR con «Lo que conviene saber al revisar» (si toca, y con el visto bueno de Miguel)

## 10. Las trampas que costaron algo

| Trampa | Qué pasó |
|---|---|
| Tablero sin `--gh` | el gate pintado en rojo sin serlo, tres veces |
| `git add -A` desde la raíz | `design_handoff_marca_e_intro`, dos veces |
| Medición en el scratchpad | la de D9, salvada de milagro; el OCR de Oliver, perdido |
| Buscar sólo en las fuentes, y no en lo ya escrito | «cero, no verificable» sobre el seretón, con el dato en un barrido propio de dos días antes |
| Cifras copiadas en el handoff | envejecieron en un día |
| Obra nueva sin regenerar la bibliografía | guardián en rojo; commit `5da70ba` |
| «Fallado» leído como «aplicado» | el nivel C, un día escrito y sin aplicar |
| Lección que se queda sólo en el handoff | la siguiente sesión no lee handoffs viejos; las skills sí se cargan |
