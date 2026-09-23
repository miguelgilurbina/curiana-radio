# El arte achagua, leído: qué le aporta a D11 una hermana arahuaca del norte que no es wayuu

**Tercera campaña de minería, parcela M4 (2026-09-22/23).** Se leyó por visión el
**arte** de Neira y Ribero 1762 —pliegos 7 der.-23 izq., pp. 1-32 de la numeración
del manuscrito—, que era lo único grande que quedaba sin minar de la obra. Con las
pp. 33-42 que se minaron el 09-12, **el arte está leído entero**.

- Propuesta y evidencia, pregunta por pregunta, con página, pliego y ejemplo literal:
  `6-fusion/achagua_arte_neira_ribero_2026-09-22.yaml`
- Cifras (regla 1): `6-fusion/medicion_arte_achagua_2026-09-22.yaml`, que emite
  `6-fusion/scripts/medir_arte_achagua.py`
- Regla 5: esto **propone**. No se tocó `curiana_lexicon.py`, `lexicon_achagua.py`,
  el YAML del vocabulario, `2-lengua/` ni el corpus.
- Regla 4: el achagua es de los **Llanos**. Nada de aquí es dato caquetío; todo
  entra, si entra, como comparanda marcada.

> **Veredicto en una frase:** el achagua confirma lo que la morfología ya declara
> con van Buurt y Perea —`wa-`, el par `ka-`/`ma-`, que los irracionales no llevan
> plural, que el aspecto importa más que el tiempo— y contradice lo que el motor
> enseña desde el wayuu —`ta-`, `-kana` para todo, un solo juego de persona, `-ka`/
> `-ni`/`-da`—; y en ningún caso aporta un dato **caquetío**.

---

## 1. Lo que dice el arte, en siete líneas

| # | Pregunta | El achagua | `morfologia.md` |
|---|---|---|---|
| 1 | Personas | **Dos juegos**, dichos por el autor: prefijos `Nu- Ji- Ri- Ru- Gua- Y- Na-` para «los demás verbos», sufijos `-na -si -ni -no -bi -y -na` para los compuestos de «ser» y para el **objeto** (p. 12, 16, 27). 1sg `nu-`, 1pl `gua-` = /wa-/ | `wa-` **coincide**; `ta-` **contradice**; un solo juego **contradice** (y coincide con lo que §5 declara del lokono) |
| 2 | Aspecto/tiempo | Tiempo a la latina (`-nimi-` pasado, `-su` futuro, `-bita` subj., `-ca` infinitivo, `-cata` gerundio) y el autor dice que **casi no se usa**: «el pres.te de Indicativo es el q.e hace el gasto» (p. 28) | `-ka`/`-ni`/`-da` **no apoyados**: `-ca` es infinitivo y `-ni` es 3sg.m. La convergencia «aspecto, no tiempo» de §7 **gana una segunda voz** |
| 3 | Posesión | El no-poseído es un **sufijo** `-si` que cae al poseer (`Sarricanasi` → `Nusarricana`); cuatro clases de nombre y una quinta que se posee con adjetivo (`Nusina Ema`) (p. 32-33) | `u-` prefijo: **coincide la categoría, no la forma** |
| 4 | `ka-`/`ma-` | **Par mínimo**: `masacorreyisa` «cosa limpia» / `casacorreyisa` «cosa sucia» (p. 18-19); `Cabarruani vyuna` «estoi rico»; `Cagicunacana` «yo pecador» (p. 25, 27); `ma-` sobre verbo: «Sin beber = Mairracasa» | «tiene X» / «sin X» **coinciden**; el «hay X» impersonal **no** es `ca-` en achagua |
| 5 | Nominalización | Productiva: `-erri` agente (`Ycaberri` «el que ve»), `-nicay` paciente con el agente de prefijo (`Nucabanicay` «lo que yo veo»), `-can(s)i`/`-si` acción y abstracto (p. 4-6, 11, 13) | Contradice «no hay nominalizador» **como rasgo de familia**; no toca el negativo caquetío |
| 6 | Plural | **Lo inanimado y lo irracional no llevan plural** (p. 6); muchedumbre con el adjetivo `Carruna`; racionales en `-nay`/`-beni`/`-sanã` | `-kana` para todo **contradice**; el hueco declarado de §10 **coincide** |
| 7 | Numerales | El arte **no tiene capítulo** de numerales (cero verificado página a página). Medido: `gudamuen` se parece a `juchama-` lo que cualquier forma achagua al azar | **no dice**; `gudamuen` sigue sin filiación |

## 2. Lo que resultó distinto de lo que se esperaba

- **El «Ji» de las listas es «Si».** La S larga mayúscula del copista se parece a la J;
  los ejemplos en minúscula lo prueban (`Nacabauʃi` «te miran»). Leído mal, la 2sg
  sufijal se confunde con la prefijal. Va a `meta.clave_de_lectura.nueva` del YAML.
- **La comunidad reinventó el privativo verbal achagua.** `morfologia.md` §11 llama
  «segunda invención, y nadie la había nombrado» a `ma-` sobre verbo (`ma-awa` «sin
  beber»). El vocabulario achagua dice, con el mismo verbo, «Sin beber = Mairracasa».
  Como el «4.ª conjugación lokono reinventada» de §5. **Lo emergente no es evidencia de
  lo atestiguado**, pero el hallazgo de §11 gana su comparanda.
- **El `ka-` del «hay viento» no sale del achagua.** El achagua usa `ca-` para «que
  tiene X» y lo conjuga (`Ca-barruani vyu-na` «estoi rico»); para el «hay» impersonal
  usa otras piezas («Hay mucho calor = Amo ayusamí»; «No hay = Quenia»).
- **La trampa `-kana`, medida.** El arte llama «nombres verbalizados q.e tienen el cana»
  a `Cagicunacana`: ahí `-cana` es `-ca` + `-na` 1sg. En todo el vocabulario achagua,
  las formas que fonemizadas acaban en `kana` no tienen ni una glosa plural
  (`medicion_arte_achagua_2026-09-22.yaml` §trampa_kana).
- **La calibración de Jahn queda cerrada.** «León», la única `no-esta` de las 34, está
  en el arte: `Nerrianarre` (p. 19). Jahn da `mirrianare`.

## 3. Qué NO se encontró

- **Ni un dato caquetío.** Las sondas sobre la capa `caquetío-atestiguado` dan cero en
  las dos preguntas donde podían dar algo: ninguna voz en `ka-`/`ma-` con glosa de
  «sin», «hay» o «tiene», y ninguna con las formas de los nominalizadores achagua y
  glosa de agente o de acción (el único eco, `kachipo` «enojado» frente al achagua
  `cabarecayi` «colérico», es un caso sin base).
- **Numerales en el arte**: no hay capítulo; los cardinales del proyecto son del
  vocabulario (09-12).
- **Gramática achagua en Fabo 1911**: no existe (él mismo lo dice, p. 112). Lo que
  escribe del verbo achagua (p. 88, 91) es una generalización desde el sáliva y el
  guahibo, sin un ejemplo achagua. Su poema de la p. 115 muestra en uso `-nicay`,
  `ca-`, `-beni` y `Carruna`, pero Fabo lo atribuye a Rivero o a Neira: **no es
  independiente**.
- **Gilij 1782, t. III**: ver §5.

## 4. Las opciones, y qué recomiendo

- **A — Escribir el achagua como tercera comparanda en `2-lengua/morfologia.md`**, sin
  tocar el motor: §5 (las dos hermanas parten la persona en dos juegos; el sufijado es
  también el objeto), §6 (par mínimo `ca-`/`ma-`, y la reserva sobre el «hay» impersonal),
  §7 (el testimonio de uso de la p. 28 junto al de Perea p. 606), §10 (no-poseído por
  sufijo; irracionales sin plural en las dos hermanas; nominalizadores achagua) y §11
  (`Mairracasa` junto a `ma-awa`). *(recomendada: es documentación, no mueve score)*
- **B — Dar a `ka-`/`ma-` la cita del achagua** en su entrada del motor
  (`REGLAS_ATRIBUTIVAS`), junto a van Buurt y Perea, como comparanda marcada. §3 de la
  nota dice «la nota sabe más que el código»: con esto sabría más. Cambia texto del
  módulo, no el prompt ni el score; medir antes. *(recomendada con A)*
- **C — Revisar la glosa de `ka-` «hay X»**: dejar «tiene X / que tiene X» como valor
  con apoyo de las tres hermanas y marcar «hay X» impersonal como extensión del
  proyecto. *(para decidir: toca el ejemplo `ka-juri` del prompt y la decisión d21.5 C)*
- **D — Importar el juego sufijado, o la restricción de número de los irracionales.**
  *(no recomendada: sigue sin haber un dato caquetío; con dos hermanas de acuerdo el
  hueco declarado se refuerza, pero la razón de §5 para no importar sigue en pie)*
- **E — Pasar la calibración de «león» de `no-esta` a `difiere`** (arte p. 19) en el YAML
  del vocabulario y regenerar su módulo. *(recomendada; es de quien fusione: este minero
  no toca ese YAML)*
- **F — Nada de esto ahora.** *(siempre disponible)*

**Mi recomendación: A + B + E + G**, H como campaña corta, y C como pregunta abierta en el tablero.

## 5. Gilij (tomo III, 1782)

El OCR con `ocr_fuente.py` salió casi vacío (391 de 457 páginas); se rehízo sobre la
imagen incrustada y lo citado se verificó en imagen. Detalle en el YAML
(`gilij_1780_1783`) y en la ficha.

- **El achagua es maipure**: «è certo dico, che l'Acciàgua è un dialetto del Maipùre»
  (p. 205), con Gumilla. La filiación arahuaca del norte del achagua ya estaba escrita en
  1782. Del arahuaco lokono («Aruàca») dice que no sabe nada.
- **De paso, el maipure** (cap. X, pp. 185-190; fuera del encargo, sin minar entero):
  «nuja io, pìa tu … uaja noi» (p. 186) y dos conjugaciones, activa y «passiva, la quale
  serve anche pe' neutri», ésta sacada del verbo «ser» (p. 187). Es la **tercera
  hermana con el corte activo/estativo** y la **primera no wayuu que da `pia`**.
- **Pronombres achagua** (apéndice II, pp. 345-346): «Nuja io, Gijà tu, Pijà quegli,
  Rujà quella, Guajà noi, Ijà voi, Najà coloro»: seis de siete como en Neira; la 3sg m.
  difiere («Pijà» / «Ria»). Gilij conocía el manuscrito de Rivero (Note, p. 410): **no
  cuenta como atestación independiente**.
- **Caquetíos: cero en el tomo III**, medido sin tildes sobre el OCR entero
  (`medicion_arte_achagua_2026-09-22.yaml` §gilij_tomo_iii). «Coro» sale una vez como
  ciudad, de pasada, en el apéndice del taíno (p. 228): Gilij duda de que las voces
  antillanas del castellano vinieran «da quei di Coro». Es para la campaña del taíno. Los
  tomos I y IV no se leyeron.

**Opción G — `pia` deja de ser «sólo wayuu»**: anotar en `morfologia.md` §1 que el maipure
de Gilij da `pìa` «tú». No lo vuelve caquetío ni cambia su capa (sigue reconstruido), pero
es el único pronombre del juego wayuu que una hermana del norte no wayuu repite letra por
letra. *(recomendada, con A)*
- **H — Minar el cap. X de Gilij** (gramática maipure, pp. 185-190) como comparanda del
  norte para D11. *(recomendada como campaña corta aparte)*

## 6. Lo que no cupo, declarado

- Una **segunda lectura independiente** del arte (otro lector, mismas páginas) no se
  hizo: todo es de un lector, con zoom sobre cada línea citada.
- El `Y-` de `Ycaberri` «el que ve» y de `Ybana` (p. 6, 23) no lo explica el autor:
  ¿2pl o índice impersonal? Si fuera impersonal, sería el pariente más cercano del
  `u-` lokono en achagua. Pregunta abierta.
- El locativo achagua distingue **líquido** (`Vni yaco` «en el agua») de no líquido
  (`Cainabe naco` «en la tierra») (p. 29-30). Para un pueblo de mar es una pregunta que
  el proyecto no se ha hecho.
- Censo de los tainismos del lado castellano y de los préstamos que el autor marca
  (ficha, «Qué daría esta obra»): siguen sin hacer.

**Miguel decide.**
