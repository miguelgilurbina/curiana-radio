# D11 fase 3: el núcleo re-derivado desde lokono + achagua, y un perfil de run para medirlo

Miguel, 2026-09-13, sobre el núcleo que el 2026-09-10 se re-etiquetó sin tocar
formas: pide **la retroabstracción**, o sea, qué pondría en su lugar el eje que
eligió D11.

Esto es una decisión, no una tarea. Cambiar el núcleo cambia la lengua que
hablan los 60 agentes en cada frase, así que va al tablero con label
`decision`. Los datos casilla por casilla están en
`6-fusion/propuesta_nucleo_d11_fase3.yaml` y las cifras en
`6-fusion/scripts/medir_coste_nucleo_d11.py`.

---

## Lo corto

1. **De las 24 casillas finas de la propuesta, 9 tienen apoyo real**: 4
   atestiguadas y 5 reconstruidas. Las otras 15 sólo admiten candidatas
   hipotéticas. Recuento sacado del YAML, no a mano.
2. **Los numerales 1-4 no hay que reconstruirlos: ya están atestiguados.**
   `pana`, `gudamuen`, `sabuenen` y `katarí` son entradas caquetío-atestiguado
   del lexicón desde hace meses (Arcaya y Zavala). El canon enseña en su lugar
   `wanee`, `piama`, `apünüin` y `pienchi`, que son wayuu.
3. **`waya` y `naya` se quedan como están.** El achagua da `Guaya` y `Naya`
   letra por letra, y el lokono concuerda en el prefijo. Cambia la
   justificación, no la forma.
4. **El aspecto (`-ka`/`-ni`/`-da`) no se puede re-derivar con lo que hay.**
   Ninguna de las tres marcas tiene concordancia sistemática. Las candidatas
   son formas de dos letras, y el gramático del lokono cree que el aparato de
   tiempo de su propia fuente es invento misionero.
5. **Recomendación:** un perfil `nucleo-d11` frente a `base`, con pronombres,
   posesivos y numerales re-derivados y el aspecto sin tocar, declarado como
   convención de la simulación. Pero antes hay que arreglar dos cosas del
   instrumento (§5).

---

## 1. Cómo se asignó cada etiqueta

Una sola etiqueta por candidata, en este orden:

| Etiqueta | Cuándo |
|---|---|
| `caquetío-atestiguado` | una fuente caquetía da la forma **para esa casilla** |
| `caquetío-reconstruido` | lokono y achagua concuerdan en el prefijo (consonante **y** vocal) y la forma está documentada en una de las dos; **o** una hermana da la forma y una fuente segmenta ese mismo morfema en voces caquetías atestiguadas |
| `caquetío-hipotético` | todo lo demás, incluidas las composiciones nuestras. En duda, aquí |

Los estratos del lokono se citan por separado: Schumann 1755 y Schultz 1802
vía Perea, Brinton 1871, Pet 1987 y la A-2 de Oliver. El achagua es la
**transcripción por visión** del 2026-09-12, con pliego y lado.

---

## 2. La tabla

| Casilla | Hoy (origen wayuu) | Lokono | Achagua | ¿Concuerdan? | Traza caquetía | **Propuesta** | Etiqueta |
|---|---|---|---|---|---|---|---|
| 1sg | `taya` | `de`, `da-` (p. 550, 587), *dai* (A-2) | `Nuya`, `Nu-` (pl. 8) | **no** (d / n) | **sí**: `d-` en *dare*, *datihao* (Oliver p. 147) | **`daya`** | hipotético |
| 2sg | `pia` | `bu-` (p. 587), `bi` (Pet), *bii* (A-2) | `Jia`, `Ji-` (pl. 8) | no (b / j) | indirecta: C3, b- por p- | **`bia`** ⚠️ | hipotético |
| 3sg m. | `nüma` | `lù-`/`li-` (p. 587) | `Ria`, `Ri-` (pl. 8) | casi: l~r, par indecidible (C8, Oliver p. 105) | no | **`ria`** ⚠️ | hipotético |
| 3sg no m. | `nüma` | `tù-` (p. 587) | `Ruya`, `Ru-` (pl. 8) | no (t / r) | no | **`ruya`** ⚠️ | hipotético |
| 1pl | `waya` | `wa-` (p. 587), *wai* | `Guaya` = /waya/ (pl. 8) | **sí** | no | **`waya`** (se queda) | reconstruido |
| 2pl | — | `hù-` (p. 587) | `Ja`, `J-` (pl. 8) | consonante sí, vocal no | no | `ja` (opcional) | hipotético |
| 3pl | `naya` | `na-` (p. 587) | `Naya`, `Na-` (pl. 8) | **sí** | no | **`naya`** (se queda) | reconstruido |
| pos. 1sg | `ta-` | `da-` | `Nu-` | no | **sí** (C1) | **`da-`** | reconstruido |
| pos. 1pl | `wa-` | `wa-` | `Gua-` | **sí** | no | **`wa-`** (se queda) | reconstruido |
| pos. 3pl | — | `na-` | `Na-` | **sí** | no | **`na-`** | reconstruido |
| pos. 2sg / 3sg | `pi-`/`nü-` (sólo en CLAUDE.md) | `bu-` / `lù-`, `tù-` | `Ji-` / `Ri-`, `Ru-` | no / casi | no | `bi-` / `ri-`, `ru-` | hipotético |
| 1 | `wanee` | `abba` (p. 565) | `aba-` + clasif. (pl. 28) | **sí**, *aba | **`pana`**, `apana` 'una luna' | **`pana`** | **atestiguado** |
| 2 | `piama` | `bi-ama` (p. 565) | `Juchamata` (pl. 56) | parcial (-ama) | **`gudamuen`**, `buia-`, `aco` | **`gudamuen`** | **atestiguado** |
| 3 | `apünüin` | `c-a-bbu-hin` (p. 565) | `Mataritaí` (pl. 96) | no | **`sabuenen`** | **`sabuenen`** | **atestiguado** |
| 4 | `pienchi` | `bi-bi-ti` (p. 565) | *no hallado* | no evaluable | **`katarí`** | **`katarí`** | **atestiguado** |
| 5 | `jarai` | `abba-te-cabbe` «una mano» | `Abacase` «una mano» (pl. 48) | **en la estructura** | no | `pana-kabu` | hipotético |
| 10 | `polo` (¡wayunaiki!) | `bi-ama-te-ccabbu` «dos manos» | `Juchamage` (pl. 55) | en la estructura | `buia-` ligada | `buia-kabu` | hipotético |
| 20 | — | `abba luccu` «un hombre» | `Abacaí tacay` (pl. 96) | parcial | `ateri` 'hombre' | `pana ateri` | hipotético |
| completivo | `-ka` | `-bi` pret. inmed. (p. 605); `-ca` = 'ser' | `-mi` (un ejemplo, pl. 59) | no | no | `-bi` | hipotético |
| continuativo | `-ni` | `-bo` (Pet); `a-ni-n` = 'ser' | `-ní` = 3.ª persona | no | no | `-bo` ⚠️ | hipotético |
| prospectivo | `-da` | `-pa` futuro (p. 605); `-fa/-ha` (Pet) | `-ba`, `-su/-saba` futuro (pl. 24) | **en función**, 2 letras | no | `-pa` | hipotético |

⚠️ = la forma ya es clave de otra lengua en el lexicón (ver §5).

---

## 3. Dónde lokono y achagua concuerdan y dónde no

**Concuerdan:**
- el **prefijo de 1pl** `wa-` / `gua-`;
- el **prefijo de 3pl** `na-` / `Na-`;
- el **'uno'** *aba*;
- que **la 3.ª singular distingue género**. El `nüma` del canon, que no lo
  distingue, no tiene apoyo en ninguna de las dos;
- la **estructura del numeral**: base cinco por la mano, 5 = 'uno + mano',
  10 = 'dos + mano';
- la **base -ya** de la forma libre. La tienen el achagua, el maipure, el
  island-carib y el wayuu; el lokono es el único que va aparte (`da-i`).

**No concuerdan:**
- la **1sg**: el lokono tiene `d-` y el achagua conserva la `n-` protoarahuaca
  (Oliver C1). Aquí manda la traza caquetía: *dare* 'diente' frente a lokono
  *d-ari* 'mi diente' y wayuu *t-ali*, que Oliver lee como prefijo de 1sg
  (p. 147). Por eso `da-` sale reconstruido. Pero `daya` es una composición que
  ninguna lengua documenta, y por eso sale hipotético;
- la **2sg** (`b-` / `j-`) y la **3sg no masculina** (`t-` / `r-`);
- los **numerales 2-4**: el lokono y el achagua van cada uno por su lado, y el
  caquetío atestiguado por un tercero. `gudamuen` no se parece a ninguno
  (0.25-0.38).

**Una coincidencia que se registra y no se afirma:** `sabuenen` 'tres' ~
lokono *c-a-bbu-hin* da 0.50, justo en el umbral del cómputo D11. Es una sola
comparación contra el estrato de 1755; con el *kabyn* de 1987 baja a 0.38. No
es prueba de nada.

**Formas de dos letras.** `da-`, `na-`, `-pa`, `-bi` y `-bo` son de dos
letras. Donde se apoyan (`wa-`, `na-`, `da-`), el apoyo no viene del parecido:
viene de alinear el paradigma entero, casilla por casilla, en las dos
hermanas. En el aspecto no hay paradigma que alinear, y por eso las tres
candidatas se quedan en hipotético. La del futuro también: `-pa` / `-ba`
coinciden en función y en forma, pero son dos letras con b/p, y el achagua
tiene además `-su/-saba`.

---

## 4. Lo que cuesta, medido

`medir_coste_nucleo_d11.py`, 2026-09-13:

| Forma | Constructores de prompt (de 6) | Apariciones en prompts | Koiné | Score | Tests | Demos |
|---|---|---|---|---|---|---|
| `taya` | 3 (incl. `_IDENTIDAD_LINGUISTICA`, que reciben todos) | 6 | núcleo de reserva | — | 21 | 21 |
| `pia`, `nüma` | 1 y 2 | 3 y 2 | núcleo de reserva | — | 0 y 2 | 2 y 3 |
| `waya`, `naya` | 1 | 1 | — | — | 2 y 0 | 1 y 4 |
| cada numeral | 1 (sólo tier I) | 1 | — | — | 0 | ≤1 |
| `ta-` | 5 | 10 | — | tupla de `es_arahuaco` | 7 | 5 |
| `-ka` · `-ni` · `-da` | 5 · 6 · 4 | 10 · 11 · 11 | 32 formas-firma de `FORMAS_SEED` | mapa de aspecto (2 de 10 puntos) | 19 · 23 · 5 | 16 · 17 · 13 |

Además, `taya` sale 3 veces en las `instruccion_agente` de `-ni` y `-da`, y
los tres aspectos son regla propia en `REGLAS_ASPECTO`.

**Corpus.** No se re-midió, porque Supabase local está apagado. La última
medición (`ANALISIS_BASE_2026-08-06.md`) da:
- **18.752 de 54.936 usos** llevan sufijo de aspecto;
- **3.840** llevan prefijo posesivo;
- **`taya` es la forma más usada del corpus**.

Lo que se re-deriva es el andamiaje, que es justo lo que los agentes
consolidaron primero.

**Lectura.** Los numerales son casi gratis y ya están atestiguados. Los
pronombres son caros sólo en `taya`. El aspecto es lo caro de verdad, y es
donde menos evidencia hay. Coste y evidencia van en sentido contrario.

---

## 5. Qué rompe, y dos trampas del instrumento

**Comparabilidad con la era 1.** Si se cambia el canon, se rompe entera: es
otra lengua en cada frase. Si se hace **por perfil**, `base` sigue siendo la
misma y la era 1 sigue siendo comparable con `base`. El brazo nuevo es una
línea aparte.

**`score_linguistico()`**. `capas_de_score` no se toca. Pero hay dos listas
cableadas: la tupla de prefijos de `es_arahuaco()` (`ta`, `wa`, `ma`, `ka`) y
el mapa de `_aspectos_morfologicos` (`ka`, `ni`, `da`). Si el brazo nuevo
dice `da-X` y el score sólo reconoce `ta-`, ese brazo pierde densidad por
construcción. La salida es que las dos listas sean la **unión** de los dos
núcleos en todos los brazos. Eso puede mover un poco el score de `base` si
algún agente de base produce `da-X` o `na-X`, y hay que declararlo.

🔴 **Trampa 1: el núcleo no llega por la capa léxica.** Los perfiles filtran
el muestreador, pero pronombres, numerales y aspecto están **cableados** en
seis sitios:
- `prompt_reglas_completo`, `prompt_reglas_breve` y el bloque de tier III;
- `_IDENTIDAD_LINGUISTICA`, `prompt_refuerzo` y `prompt_rescate_linguistico`.

A eso se suman `_NUCLEO_FALLBACK` y `FORMAS_SEED` en la koiné. Un perfil que
sólo cambie `capas_lexicas` no cambia el núcleo. Y de paso: **el brazo
`atestiguado` también recibe `taya`, `pia`, `wanee`…**, porque vienen
cableados. Es menos «duro» de lo que dice su descripción.

🔴 **Trampa 2: colisiones de clave.** `bia` ya es clave lokono ('in'), y `ria`
y `ruya` son claves achagua. Mientras lo sean, el score clasificará a un
agente del brazo nuevo que las diga como **fuga a otra lengua arahuaca**. Hay
que renombrar la comparanda antes de sembrar, con el mismo precedente de
`ja-achagua` y `biama-kalinago`. `de` queda descartada del todo: está en
`ES_STOPWORDS` y puntuaría como español.

---

## 6. Las salidas

**A — Re-derivar en el canon.** Cambiar el núcleo para todos los runs. Es lo
coherente con D11 llevado hasta el final. Rompe la comparabilidad con todo lo
publicado y fija como lengua de los agentes diez candidatas hipotéticas.
*No la recomiendo.*

**B — Perfil `nucleo-d11` frente a `base`** *(mi recomendación)*. Un eje
nuevo en `perfiles_de_run.yaml`, **`nucleo: wayuu | d11`**, ortogonal a capas
y andamiaje, con la misma semilla y los mismos nodos que `base`. Ve:
- **pronombres**: `daya` · `bia` · `ria` / `ruya` · `waya` · `naya`;
- **posesivos**: `da-` · `bi-` · `ri-` / `ru-` · `wa-` · `na-`;
- **numerales**: `pana` · `gudamuen` · `sabuenen` · `katarí` · `pana-kabu` ·
  `buia-kabu` · `pana ateri`;
- **aspecto**: sin cambiar. `-ka`/`-ni`/`-da` se declaran
  **canon-simulación**, como ya se hizo con `-ana` 'lugar de'.

Responde a una pregunta con número: **¿cambia la koineización cuando el
andamiaje gramatical deja de ser wayuu?** Se mide en velocidad de
convergencia, score y formas que se fijan.

**C — Perfil pleno, aspecto incluido (`-bi` / `-bo` / `-pa`).** *No ahora.*
Las tres son hipotéticas, dos chocan con claves o con morfemas vivos, y
cambiarlas obliga a tocar el mapa de aspecto del score. Queda escrita como
segundo paso si B muestra algo.

### Si se aprueba B, qué hay que tocar

1. **El eje C.** `nucleo` en `perfiles_de_run.yaml` y en
   `curiana_perfiles.py`. Los seis constructores de prompt, `_NUCLEO_FALLBACK`
   y `FORMAS_SEED` pasan a leer el núcleo del perfil.
2. **El score.** La tupla de prefijos de `es_arahuaco()` pasa a la unión de
   los dos núcleos, y un test lo vigila, igual que el de `capas_de_score`.
3. **Las claves.** Renombrar las comparanda `bia`, `ria` y `ruya`.
4. **El lexicón** (fusión de Miguel). Añadir `daya`, `bia`, `ria`, `ruya`,
   `pana-kabu`, `buia-kabu` y `pana ateri` con su etiqueta. Re-etiquetar
   `waya`, `naya` y `wa-` con la justificación nueva. No crear nada para 1-4:
   ya existen.
5. **`BITACORA_RUNS.md`.** Declarar el brazo y su línea de comparación.

### Tres decisiones finas dentro de B

- **¿`da-` reconstruido o hipotético?** Lo propongo reconstruido por *dare*.
  Pero Oliver da la correspondencia para «PERHAPS Caquetío» (p. 136) y duda
  de *datihao* (n. 42). Si esa duda pesa, se degrada.
- **¿Partir `nüma` en `ria` / `ruya`?** Las dos hermanas lo hacen. Pero
  obliga al agente a elegir género, y eso es gramática, no sólo forma.
- **¿Qué 'dos' para el habla?** Hay tres atestiguados (`gudamuen`, `buia-`,
  `aco`) que no se reducen a uno. Propongo `gudamuen` suelto y `buia-` en
  compuestos, y conservar las tres lecturas.

---

## 7. De paso: desfases medidos que no esperan a la decisión

- `CLAUDE.md` y `2-lengua/morfologia.md` enseñan `tayamaa` 'nosotros', que no
  existe ni en el lexicón ni en el motor. La entrada es `waya`.
- `CLAUDE.md` declara los posesivos `pi-` y `nü-`, pero `REGLAS_POSESIVAS` no
  los tiene.
- La nota de `jarai` dice que el lokono del lexicón no cubre 'cinco'. Sí lo
  cubre: `abbatekkabe`.
- `pana` 'uno' cita a Arcaya y a Zavala sin página.

**Regla 3.** Todo lo anterior es forma de lengua. Que el lokono diga 20 =
«un hombre» no autoriza a decir cómo contaban los caquetíos, y el género
gramatical de la 3.ª persona no dice nada de su parentesco.
