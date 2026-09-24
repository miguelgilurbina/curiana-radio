---
name: fusionar-propuesta
description: Llevar al canon del proyecto lingüístico caquetío lo que espera en 6-fusion/ — una propuesta de minería, un fallo o una decisión de Miguel — ya sea al lexicón (curiana_lexicon.py o un módulo lexicon_*.py generado), al corpus cultural (3-mundo/corpus/*.yaml) o como re-etiqueta de capa o de fuente; y publicar en GitHub el borrador que la acompaña. Usar cuando se pida fusionar, aplicar, meter al lexicón o al corpus, re-etiquetar entradas, aplicar una tanda de decisiones, regenerar un módulo generado, o publicar o cerrar un issue de decisión. Los topónimos tienen su propio cierre en campana-toponimos §6-7.
---

# Fusionar una propuesta

El ritual para pasar de `6-fusion/` al canon, destilado de las fusiones del 11
al 13 de septiembre de 2026: las raíces y los verbos lokono de Perea (D11, fases
1 y 1b), F8, los tainismos de Medina, el nivel C al corpus, las retroabstraídas y
el achagua como módulo generado. `minar-fuente` propone; esto fusiona. Cada paso
está porque saltárselo costó un error que aquí se nombra.

Las reglas de `CLAUDE.md` mandan; aquí pesan sobre todo la 1 (ninguna cifra a
mano), la 2 (etiqueta epistémica, y en duda degradar), la 5 (el humano fusiona),
la 8 (citar es una clave foránea) y la 10 (las decisiones viven en el tablero).

## 0. La decisión es de Miguel, y se registra antes de tocar nada

Se registra en la tanda `6-fusion/decisiones_tanda_AAAA-MM-DD.yaml`, con el
mismo patrón que las del 08-30, 09-01, 09-08 y 09-12. Una clave por decisión:

```yaml
tainismos_de_medina:
  issue: 'https://github.com/miguelgilurbina/curiana-radio/issues/NNN'   # si lo hay
  estado: APLICADA (2026-09-12)
  decision_literal: >-
    «Si están como taíno en otra fuente y son panhispánicas entonces deben
    clasificar como caquetío. [...]»
  lectura_operativa: >-
    caquetío-RECONSTRUIDO, no atestiguado — el precedente kanoa/hamaca/konuko.
  aplicado_por: [6-fusion/scripts/tainismos_medina_a_caquetio.py, 6-fusion/scripts/fusionar_tainismos_medina.py]
  deuda: 'lo que queda sin fuente o sin decidir'
```

- **La cita va literal, entre comillas latinas, aunque sea «#39 sí.».** Una
  paráfrasis pierde el alcance de lo autorizado: «Fusionemos lo que conseguimos
  achagua» metió el vocabulario de Neira y Ribero y **no** a Fabo, que quedó
  fuera declarado (`achagua_121.fuera`).
- **La lectura operativa es tuya, y se escribe aparte.** Miguel dijo que los
  tainismos «deben clasificar como caquetío»; se aplicaron como *reconstruido*
  por precedente. Si eso no se escribe por separado, parece que él decidió
  *atestiguado*. Lo mismo con D8: «#37 sí» se leyó como la opción intermedia.
- **Una autorización vale para lo que dice, y nada más.** «Seguiré tu
  recomendación con respecto al 124» es la opción A de #124. Lo que salga al
  aplicar y nadie previó (una colisión, un homógrafo, una capa dudosa) **se
  salta, se imprime y se le lleva a Miguel**; no se resuelve de paso.
  `fusionar_medina_retroabstraido.py` salta las colisiones «(son decisión
  aparte)», y la acuñación `hikoteya` quedó conviviendo con `hikotea` porque
  retirarla era otra decisión.
- Al terminar: `estado: APLICADA (fecha)` y `aplicado_por` en la decisión, y en
  `meta.estado` de la tanda, cuántas quedan.

## 1. Medir antes de escribir

- **Primero un `--dry-run` que imprima la tabla entrada por entrada.** F8 se
  midió «uno a uno antes de tocar nada», y así salió que 30 «lokono» eran
  acuñaciones de la simulación. El handoff hablaba de «dos grafías del taíno»;
  medidas, eran dos cosas distintas: 9 eran una tilde, y 9 eran formas generadas
  por regla (commit `032e5f4`).
- **Mira la capa de lo que ya está antes de contarlo como apoyo.** 23 entradas
  `caquetío-reconstruido` venían del wayuu, y los numerales que parecían la
  mejor prueba eran circulares (`bed4ec4`, `35fc6a9`).
- **Anota el total de entradas activas antes de empezar.** Es la alarma de §3.

## 2. Dónde va cada cosa

| Qué | Dónde | Precedente |
|---|---|---|
| Entradas léxicas en número manejable a mano | un bloque dentro de `VOCABULARIO_BASE` (§3) | fases 1 y 1b de D11, tainismos, retroabstraídas |
| Una comparanda del tamaño de un diccionario, sacada de una transcripción | módulo generado `curiana_sim/lexicon_<x>.py` + import con `setdefault` (§4) | achagua |
| Cambiar la capa o la `fuente` de entradas que ya están | la entrada misma: `fuente` + huella en `notas` (§3) | F8, D11 fase 3, tainismos |
| Hechos de mundo | `3-mundo/corpus/<esfera>.yaml` (§8) | nivel C de Medina |
| Topónimos | `lexicon_toponimos.py` → `migrar_toponimos.py` | `campana-toponimos` §6-7 |

No inventes un fichero: el nivel C entró en `ecologia.yaml`, que ya tenía los
dominios `oficios`, `ceramica` y `agricultura`.

## 3. Lexicón: el bloque va DENTRO de `VOCABULARIO_BASE`

```python
t = io.open(p, encoding="utf-8").read()
ini = t.index("VOCABULARIO_BASE: dict[str, dict] = {")
fin = t.index("REGLAS_ASPECTO", ini)            # el dict que viene después
region = t[ini:fin]
ancla = None
for m in re.finditer(r'^\s*"[^"]+":\s*\{.*\},\s*$', region, re.M):
    ancla = m                                   # la última entrada DE LA REGIÓN
corte = ini + ancla.end()
```

🔴 **La trampa de `FUERA_DEL_HABLA`.** El primer intento de la fase 1 buscaba la
última entrada **del fichero**, y las 171 raíces cayeron dentro de
`FUERA_DEL_HABLA`, el dict de las palabras retiradas, que va más abajo en el
mismo archivo. El síntoma fue que el total de entradas activas no se movió.
Hubo que restaurar desde una copia y rehacerlo acotando la región
(`fusionar_perea_d11_fase1.py`, commit `7f9a1ba`). Por eso: **mide el total de
entradas activas antes y después**, importando `curiana_lexicon` en un proceso
nuevo. Si no se movió lo que tenía que moverse, algo cayó fuera.

- **El regex supone una entrada por línea** (`"clave": {...},`), que es como
  escriben todos los scripts de fusión. No cambies el formato.
- **Cabecera comentada en el bloque**:
  `# ═══ D11 FASE 1b (2026-09-12) — qué es y de dónde`. Sirve también de marca
  de idempotencia (§9).
- **Escapa las glosas.** Un `"` o un `\` dentro de `sig` o `notas` rompe el
  literal de Python; `limpio()` los cambia por `'` y los quita.
- **Para re-etiquetar una entrada que ya está**: localiza `"clave": {`, busca
  `"fuente"` **dentro de esa entrada** (acotado hasta su `},`), sustitúyelo y
  pon la huella al principio de `notas` (`huella + " · "`), o crea `notas` si no
  hay. 🔴 El regex de `notas` tiene que admitir que `notas` sea **el último
  campo**: falló justo con `dare` (commit `7f5ec72`).
- **Y comprueba que no se movió nada más.** El re-etiquetado de D11 fase 3
  (`2bf64f4`) se verificó así: las mismas entradas antes y después, las mismas
  claves, sólo las `notas` esperadas modificadas, y cero cambios en forma, `sig`,
  `cat` y `fuente`.

## 4. Lexicón grande: un módulo generado

- `6-fusion/scripts/generar_lexicon_<x>.py` lee el YAML de la propuesta y
  escribe `curiana_sim/lexicon_<x>.py`. El módulo lleva una cabecera «GENERADO
  por … No se edita a mano: se corrige el YAML y se regenera», el dict
  (`COMPARANDA_ACHAGUA`), los homógrafos (`HOMOGRAFOS_ACHAGUA`) y, en el
  docstring, las cifras medidas al generar.
- **El import va en `curiana_lexicon.py`, detrás de los otros y con el mismo
  patrón:**

  ```python
  try:
      from lexicon_achagua import COMPARANDA_ACHAGUA
  except ImportError:      # el módulo generado no está presente
      COMPARANDA_ACHAGUA = {}

  for _f, _e in COMPARANDA_ACHAGUA.items():
      VOCABULARIO_BASE.setdefault(_f, _e)
  ```

  Con `setdefault` nunca se pisa una clave: si una forma ya estaba con otra
  etiqueta, gana la que estaba, y corregir esa colisión es otra decisión (así
  lo dice el comentario del import de Zavala).
- **Declara la trampa en `CLAUDE.md`**, en la fila de «generados Y se
  importan»: regenerar el módulo cambia `score_linguistico()`. El commit del
  achagua (`993a4e9`) la actualizó.
- **Sácalo de la cola en `generar_bandeja.py`**: un módulo generado que el motor
  importa ya no es propuesta. El mismo commit lo hizo.
- **Las correcciones van al YAML, nunca al módulo.** Dos commits editaron a mano
  `toponimos.yaml`, y la regeneración siguiente deshizo 25 entradas.

## 5. Claves

| Caso | Clave | Por qué |
|---|---|---|
| Voz caquetía, de cualquier capa | **lema fonémico de D5**: `from aplicar_fase2_d5 import lema_fonemico` (gua→wa, gue→ge, c→k salvo ce/ci, z→s, v→b), con la grafía original en `forma_fuente` | D5 está cerrada, y así están `konuko`/conuco y las retroabstraídas. **No** uses el `fonemizar()` de los scripts de barrido, que colapsa `ce→se` |
| Comparanda | la forma de la fuente, con sólo las normalizaciones declaradas (Neira: `V`/`J` iniciales → `u`/`i`); la grafía entera en `forma_fuente` | la clave tiene que poder volver a la página |
| Homógrafo de una clave existente | `<forma>-lokono`, `<forma>-achagua` | precedente `kati-kalinago`. Y no es un tecnicismo: `bara` caquetío es 'palo' y `bara` lokono es 'mar' |
| Homógrafo de una palabra española, o de dos letras o menos | igual, con sufijo | 🔴 `score_linguistico()` cuenta como arahuaco cualquier token igual a una clave, **sin filtrar por fuente**: `casa`, `carta` o `manta` como claves desnudas contaminan la métrica. Se detectan con `RAICES_ESPANOLAS` + `ES_STOPWORDS` + una lista corta, medida sobre ese lote |
| La misma clave ya está con la misma forma | se salta: es corroboración, y se lista en la propuesta | los 26 verbos de Perea que ya estaban |

## 6. `fuente`, capa y `cat`

| Capa | Cuándo | Precedente |
|---|---|---|
| `caquetío-atestiguado` | una fuente da la voz como caquetía | Zavala. Borojó se quedó en esta capa, con el conflicto escrito en `notas` (#123) |
| `caquetío-reconstruido` | la forma se justifica por un cognado hermano citado, sin atestación caquetía | kanoa/hamaca/konuko (D5, colisiones, 2026-08-31); tainismos de Medina. **Si la hermana es el wayuu, la entrada suma a la deuda de D11 fase 3** |
| `caquetío-hipotético` | acuñación sin cita | las 30 «lokono» de F8, que eran acuñaciones de junio |
| `caquetío-retroabstraido` | forma documentada en boca viva, con sustrato incierto | catire, chiriware, tukeke; Medina A/B/C (#124). Sólo la ven los perfiles `suelto` |
| `taíno-reconstruido` | forma generada por regla desde otra lengua | las 9 de `reconstruir_taino()` |

- **En duda, degradar** (regla 2).
- **Nunca `caquetío` a secas.** `capa_epistemica()` la promovía **en silencio** a
  atestiguada, incluidas dos entradas cuya propia nota decía que la atribución
  era débil (`0014185`). Hoy lo vigila un test.
- **Un valor nuevo de `fuente` se declara, no se inventa en una entrada.** Va a
  `FUENTES_CANONICAS`, con un comentario que da la razón (lo vigila
  `test_ninguna_entrada_sale_del_conjunto_canonico_de_fuentes`). Si es una
  lengua, también va a `FAMILIAS` en `curiana_fonotactica.py`, como el achagua.
  Si es una capa caquetía, tiene que estar en `capas_lexicas` de algún perfil de
  `5-experimento/perfiles_de_run.yaml`, o sus entradas no llegan a ningún agente
  (`test_capas_epistemicas.py`).
- **Di qué cambia para los agentes.** Al pasar a hipotético, las acuñaciones de
  F8 empezaron a verse en el perfil `base`; el commit lo declaró.
- **Si el filtro fonotáctico cae con la fuente nueva, se arregla el instrumento
  para esa ortografía, no los datos, y no en global.** Con Perea se puso en rojo
  el test que protege el orden lokono > wayuu de D11. Eran sus geminadas y su
  `ù`, no el dato (`e1aa50f`).
- **`cat`**: la fuente casi nunca la da. Se infiere de la glosa (infinitivo →
  `v_raiz`, el resto → `sust`) y **se declara en `notas`**. No descartes por
  «ilegibles» las glosas de una letra: `baddia` 'y' y `mùn` 'a' eran palabras
  gramaticales, justo de las que el lexicón anda pobre (`7f9a1ba`). Y no copies
  la `cat` de la columna wayuu: la revisión pre-era 2 midió que es ficticia (B1).

## 7. `notas`: la procedencia y la huella

Cada entrada tiene que responder sin abrir otro fichero:

- **de dónde**: obra, página impresa (o pliego y lado), forma de la fuente y
  estrato (Schumann 1755 vía Perea no es Schultz 1802), y el número de
  atestaciones si lo hay;
- **qué es la forma**: «transcripción por visión: verificar en imagen antes de
  citar»;
- **qué se infirió**: «`cat` INFERIDA de la glosa», «clave desambiguada como
  `x-lokono` porque…»;
- **la huella de la decisión**: «Fusión fase 1b de D11, 2026-09-12», o
  «Decisión de Miguel 2026-09-12 (tainismos de Medina): «…»», y «Etiqueta
  anterior: `taíno`» cuando se re-etiqueta;
- **lo que falta**: «página no dictada (⚠️ pendiente)». Una página no se
  infiere: a Caracubana le pusieron la p. 95 sacándola de la entrada vecina, se
  retiró y quedó como `deuda: sin-pagina` (`2b24c4f`).

Si la entrada choca con otra fuente, la glosa no se reescribe: se añade la
evidencia a `notas` (`minar-fuente` §8; Borojó, opción 3). Y la deuda se declara:
el 'hijo' de `dare` quedó dicho sin procedencia.

## 8. Corpus: al final de la lista, y parsear antes de escribir

Es el patrón de `6-fusion/scripts/fusionar_nivel_c_medina.py`:

1. **Ids: el siguiente libre del prefijo** (el máximo `ecologia-NNN` + 1).
   Nunca se renumera.
2. **Inserta al final de la lista de ítems `<prefijo>-NNN`, con la sangría de
   esa lista, y antes de cualquier clave de nivel 0 que venga detrás.** En
   `ecologia.yaml`, los huecos léxicos cuelgan de otra clave: pegar al final del
   fichero habría metido los hechos dentro de ella.
3. `yaml.safe_dump(..., allow_unicode=True, sort_keys=False)`, sangrado con la
   sangría de la lista, y un comentario de cabecera con la decisión.
4. 🔴 **Parsea el texto nuevo antes de escribirlo, y comprueba que los ids
   nuevos son los últimos de la lista.** Si no lo son, no se escribe.
5. **Campos**: `id`, `voz`, `contenido` (con página), `fuente` (la etiqueta
   epistémica), `referencia`, `procedencia: {obra, pagina}` (la clave foránea de
   la regla 8), `dominios`, `palabra_lexicon`, `lectura` (el porqué) y `limite`,
   con las reglas 3 y 4 escritas al lado: Medina describe el siglo XX y la
   esfera, no sólo Paraguaná.
6. `python curiana_sim/compilar_corpus.py --check`.
7. **El enganche**: si la voz entra después al lexicón, se rellena
   `palabra_lexicon` en su hecho, como se hizo con las retroabstraídas.

## 9. El script de fusión

Va en `6-fusion/scripts/<verbo>_<qué>.py`, y lo cita el `aplicado_por` de la
tanda.

- **El docstring lleva** la decisión literal, qué se aplica, qué reglas se
  respetan y **qué se midió**. El de `sanear_f8_resto.py` es el modelo.
- **Ruta relativa a `__file__`**
  (`R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))`),
  como los scripts posteriores a la fase 1, que llevaba la ruta absoluta escrita.
- **`sys.stdout.reconfigure(encoding="utf-8", errors="replace")`**: la consola
  de Windows es cp1252 (trampa de `CLAUDE.md`).
- **`--dry-run`**, que imprime y sale sin escribir.
- **Idempotente**: si encuentra su marca (la cabecera del bloque, o la `MARCA`
  del corpus), imprime «ya aplicado; nada que hacer» y sale con 0.
- **Imprime lo que hizo, entrada por entrada, y lo que saltó, con la razón**
  («ya en el lexicón — corroboración», «colisión: la clave ya existe»).
- **Escribe con `newline="\n"`.**
- **Deja dicho en la propuesta que está aplicada**: `meta.fusionado` en el YAML
  (`tainismos_en_medina.yaml`), «✅ Aplicado al corpus el …» en el fallo
  (nivel C), y lo mismo en la ficha de la fuente. El handoff del 09-11 tenía 33
  voces «falladas pero aún no aplicadas»: esa diferencia tiene que verse.
- **Nada en el scratchpad.** El generador de Perea se metió dentro de
  `minar_perea.py`, con `--dry-run`, justo «para que nada valioso quede en el
  scratchpad».

## 10. Después: medir, en este orden

```bash
cd proyecto-linguistico-caquetío
python curiana_sim/guardianes.py                 # los diez, con tests: el lexicón los mueve
python curiana_sim/generar_tablero.py --gh       # SIEMPRE con --gh
python curiana_sim/generar_bandeja.py
python curiana_sim/generar_bibliografia.py       # si entró una obra nueva
python curiana_sim/medir_sostiene.py --esferas   # qué sostiene cada obra, no a mano
```

- **`--gh` siempre.** Sin red, el panel de decisiones sale «no medido» y el gate
  cuenta como abiertas las decisiones cerradas en GitHub: pintó 3 de 9 donde
  eran 6 (`051c746`), otra vez 3 de 9 donde eran 7 (`09545d8`), y volvió a pasar
  el 2026-09-13. La regresión era del instrumento, no del proyecto. Sin red,
  no se commitea el tablero.
- **Si un guardián se pone en rojo, averigua si es el dato o el instrumento**
  antes de tocar nada (la ortografía de Perea, `e1aa50f`).
- Si tocaste topónimos, sigue la cadena de `campana-toponimos` §7.
- Pon al día la ficha de la fuente (`estado_minado`, `cobertura`, «qué ha
  dado»); `CLAUDE.md` si hay una trampa nueva o un generado nuevo; y
  `1-plan/SIGUIENTE_TANDA.md` si cambió el gate.

## 11. Publicar en GitHub y archivar el borrador

Regla 10: las decisiones viven en el tablero. Los borradores se redactan en
`6-fusion/issues-pendientes/`: `issue-<tema>.md`, `decision-<tema>.md`,
`comentario-<nº>-<tema>.md`, `fallo-<tema>.md`.

**Publicar es escribir fuera del repo, y necesita el visto bueno de Miguel.** El
clasificador de la sesión puede bloquearlo (la BANDEJA lo dice: «se publican a
mano con `--body-file`»). Si bloquea, déjale el comando exacto:

```bash
R=miguelgilurbina/curiana-radio
gh issue create  --repo $R --title "D## — qué se decide" --label decision --body-file 6-fusion/issues-pendientes/decision-<tema>.md
gh issue comment <nº> --repo $R --body-file 6-fusion/issues-pendientes/comentario-<nº>-<tema>.md
gh issue close   <nº> --repo $R --comment "Cerrada: «…» (Miguel, fecha). Registro: 6-fusion/decisiones_tanda_<fecha>.yaml"
```

- **Título `D## — qué`** para las decisiones: `generar_tablero.py` lo parsea
  (`TITULO_DEC`), y las que no lo siguen salen igual en el panel, pero con «—».
  Etiquetas en uso: `decision`, `fidelidad`, `motor`, `datos`, `jardin`.
- **El gate lee el estado del issue, no el trabajo.** La condición 8 siguió en
  rojo con la fase 1 fusionada, hasta que se cerró #39 (`7f9a1ba`). Se cierra
  con el resultado medido en el comentario, y después se corre el tablero con
  `--gh`.
- **Se archiva**: `git mv` del borrador a `publicados/`, y una fila en
  `publicados/README.md` (`| archivo | dónde se publicó | fecha |`). También
  tienen fila los que «no se publicó: se aplicó» o «se implementó».
- **En la tanda**, `publicado:` con los números de issue. Después se regenera la
  bandeja, para que baje «Redactado y sin publicar».

## 12. El commit

- **Título**: `tipo(ámbito): qué entra - lo que se aprendió`, con `feat`, `fix`,
  `docs` o `chore` y ámbitos como `lexicon`, `d11`, `f8`, `corpus`,
  `decisiones`, `fuentes` o `achagua`. El título cuenta el hallazgo, no sólo la
  acción: «las dos grafías del taíno no eran una tilde - eran nueve formas
  inventadas por regla sin etiqueta».
- **Cuerpo**: primero la cita de Miguel que lo autoriza. Luego, en mayúsculas y
  según haga falta: LO QUE ENTRA · LO QUE MIDE (antes → después) · LO QUE SE
  ROMPIÓ Y POR QUÉ · LO QUE NO ENTRÓ · FLECO MEDIDO DE PASO. Los errores propios,
  con nombre («DOS ERRORES PROPIOS, corregidos»). Al final, el estado de los
  guardianes y la línea de atribución.
- **Las cifras del commit sí valen**: son una foto con fecha, y dicen cómo se
  midieron. Las de los documentos, no (regla 1).
- **`git add` por ruta, nunca `-A` desde la raíz.** Dos veces barrió una carpeta
  sin trackear (`design_handoff_marca_e_intro`: `67a0f53`, `65a14c1`).

## 13. Las trampas que costaron algo

| Trampa | Qué pasó |
|---|---|
| Ancla buscada en todo el fichero | 171 raíces dentro de `FUERA_DEL_HABLA`, y el total activo no se movió |
| Regex de `notas` que exige campo detrás | falló con `dare`, donde `notas` era el último |
| Clave desnuda que es palabra española | `score_linguistico()` la habría contado como arahuaca |
| `fuente: caquetío` a secas | promovida en silencio a atestiguada |
| Glosa de una letra tomada por ilegible | `baddia` 'y' y `mùn` 'a' eran palabras gramaticales |
| Editar a mano un generado | 25 entradas de `toponimos.yaml` deshechas al regenerar |
| Tablero sin `--gh` | gate en 3 de 9 dos veces, y otra el 2026-09-13 |
| Decisión aplicada más allá de lo dicho | no pasó porque las colisiones se saltaron y se imprimieron: mantenlo así |
| Fallo escrito y no aplicado | 33 voces «falladas pero no aplicadas» durante un día entero |
| `git add -A` desde la raíz | `design_handoff_marca_e_intro`, dos veces |
| Página inferida de la entrada vecina | Caracubana p. 95, retirada |

## 14. Hooks

Parte de este ritual se puede cablear para que no dependa de acordarse.
La propuesta, sin instalar, está en `.claude/skills/HOOKS_PROPUESTOS.md`.
