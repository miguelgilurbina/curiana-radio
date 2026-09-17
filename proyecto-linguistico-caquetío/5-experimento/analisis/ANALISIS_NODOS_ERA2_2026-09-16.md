---
tipo: analisis
ambito: la cadena de tres días de la era 2 — GUARANAO y AMUAY
herramienta: curiana_sim/analizar_nodos.py
medido: 2026-09-16
base: supabase local (docker), runs c6837386 → 89fc1744 → 0193873d
estatus: piloto exploratorio (n = 1 cadena, 3 días) — no confirma nada por sí solo
---

# Los dos nodos de la era 2, a los tres días — 2026-09-16

> Todo lo de abajo sale de `python curiana_sim/analizar_nodos.py --run 0193873d`.
> Ninguna cifra está escrita a mano. Si una parece rara, se vuelve a medir.

La pregunta del `DISENO_ERA2.md` §7 no es si cada nodo converge consigo mismo
—eso ya lo hacía la era 1— sino si **las formas cruzan la frontera** y si la
**distancia entre nodos** se contrae. Tres días de campaña no la contestan.
Contestan otra cosa, más pequeña y más útil: **qué mide el instrumento y qué
no**. Este informe dice lo que los datos sostienen y se para ahí.

---

## 0 · Qué se midió

| Run | Día | Semilla | Motor | Arrancado |
|---|---|---|---|---|
| `c6837386` | 1 | 1 | `c69e042e` | 2026-09-16 16:31 UTC |
| `89fc1744` | 2 | 2 | `cb389991` | 2026-09-16 18:30 UTC |
| `0193873d` | 3 | 3 | `1be0d52f` | 2026-09-16 20:02 UTC |

**Divergencia sembrada: 2 vectores-semilla distintos entre los 63 agentes; 62
comparten el mismo.** Es el hallazgo que ordena todo lo demás — está en la §5.1
y conviene leerlo antes que las tablas.

Elenco: **63 agentes — GUARANAO 39, AMUAY 24**. Los 63 hablan en algún momento
de la cadena, así que la cobertura del análisis es del **100 % de los usos**
(`analizar_nodos.py` lo mide y avisa si baja del 90 %: el run `aafc5c32` del
2026-09-14 declara `elenco: era2` y habla con los nombres de la era 1, y ahí la
cobertura cae al 6,7 %).

`06482296` **no entra**: es un día 3 interrumpido a los dos turnos, hermano de
`0193873d` en el árbol de `continuado_desde`. La cadena se sube hacia atrás,
que es la rama única.

---

## 1 · La reserva que va primero: GUARANAO habla más de lo que le toca

| Día | Nodo | Usos | Cuota de usos | Cuota del censo | Agentes activos | Formas distintas |
|---|---|---|---|---|---|---|
| 1 | GUARANAO | 1.299 | 69,8 % | 61,9 % | 37 | 248 |
| 1 | AMUAY | 562 | 30,2 % | 38,1 % | 23 | 179 |
| 2 | GUARANAO | 1.024 | 56,6 % | 61,9 % | 39 | 218 |
| 2 | AMUAY | 786 | 43,4 % | 38,1 % | 23 | 196 |
| 3 | GUARANAO | 1.321 | 71,5 % | 61,9 % | 36 | 264 |
| 3 | AMUAY | 526 | 28,5 % | 38,1 % | 16 | 145 |

GUARANAO es el 61,9 % del censo y se lleva el 69,8 %, el 56,6 % y el 71,5 % del
habla. El día 3 **sólo hablaron 16 de los 24 agentes de AMUAY**: es el día peor
muestreado de los tres, y es justo el día del que sale todo veredicto de
tendencia. Cualquier lectura de conteos crudos por nodo es, en primer lugar, una
lectura de este desbalance — por eso todo lo que sigue va normalizado por
hablantes posibles del nodo.

---

## 2 · Las formas emergentes

**369 formas emergentes**, con **1.659 usos** de los 5.518 de la cadena (30 %).
«Emergente» = todo lo dicho que no esté en el vocabulario base **ni en lo que
las plantillas del prompt enseñan** (5.898 formas excluidas, el mismo conjunto
con el que el motor mide su distancia emergente), más todo neologismo
registrado y las formas fijadas en `koine_lexicon`.

### 2.1 · El umbral, declarado

`tasa` = hablantes distintos del nodo / hablantes **posibles** del nodo (39 y
24). La clasificación compara **tasas**, nunca conteos:

- **exclusiva** — la tasa del otro nodo es 0.
- **inclinada** — la razón de tasas alcanza **2,0**: el doble de prevalencia
  normalizada.
- **compartida** — razón por debajo de 2,0 en los dos sentidos.
- **poco-atestiguada** — menos de **3 hablantes** en total: con dos bocas,
  «exclusiva de AMUAY» y «lo dijo un señor» son la misma frase.

El 2,0 es grueso a propósito. Con 39 y 24 hablantes posibles y formas que llegan
a un puñado de bocas, una diferencia menor cabe entera dentro de a quién le tocó
hablar (el roster rota 12 agentes por turno). La tabla imprime siempre la razón
cruda para que se pueda aplicar otro umbral.

### 2.2 · Las formas principales, normalizadas

`habl` = hablantes distintos · `tasa` = sobre 39 (GUA) y 24 (AMU).

| Forma | Usos | GUA habl | GUA tasa | AMU habl | AMU tasa | Razón | Clase | Acuñó | Cruce |
|---|---|---|---|---|---|---|---|---|---|
| `panaa-ni` | 108 | 34 | 0,872 | 17 | 0,708 | 1,23 | compartida | ~AMU+GUA d1t1 | n/a |
| `wana-ni` | 87 | 28 | 0,718 | 18 | 0,750 | 1,04 | compartida | ~GUA d1t1 | d1t2 (+1t) |
| **`kali-iro-pabu`** ★ | 41 | 18 | 0,462 | 11 | 0,458 | **1,01** | compartida | AMU+GUA d1t5 | **n/a** |
| `kuri-bana-iro-pabu` | 39 | 21 | 0,538 | 6 | 0,250 | **2,15** | inclinada→GUA | GUA d1t5 | d1t6 (+1t) |
| `raka-ni` | 39 | 13 | 0,333 | 12 | 0,500 | 1,50 | compartida | ~AMU+GUA d1t1 | n/a |
| `tüshi-juri` | 33 | 16 | 0,410 | 7 | 0,292 | **1,41** | compartida | GUA d2t1 | d2t1 (+0t) |
| `wana-da` | 31 | 15 | 0,385 | 9 | 0,375 | 1,03 | compartida | ~AMU+GUA d1t1 | n/a |
| `kaa-da` | 29 | 9 | 0,231 | 8 | 0,333 | 1,44 | compartida | ~AMU+GUA d1t1 | n/a |
| `nii-bana` | 27 | 16 | 0,410 | 8 | 0,333 | 1,23 | compartida | GUA d1t6 | d2t3 (+3t) |
| `biro-kali` | 24 | 17 | 0,436 | 4 | 0,167 | **2,62** | inclinada→GUA | AMU d1t2 | d1t2 (+0t) |
| `sima-pabu` | 24 | 12 | 0,308 | 7 | 0,292 | 1,05 | compartida | AMU d2t1 | d2t3 (+2t) |
| `tüshi-bana` | 22 | 12 | 0,308 | 9 | 0,375 | 1,22 | compartida | GUA d1t1 | d1t2 (+1t) |
| `juri-ni` | 20 | 13 | 0,333 | 4 | 0,167 | **2,00** | inclinada→GUA | ~GUA d1t3 | d2t1 (+4t) |
| `sima-maa` | 19 | 12 | 0,308 | 6 | 0,250 | 1,23 | compartida | AMU d2t6 | d3t2 (+2t) |
| `kali-duma` | 18 | 10 | 0,256 | 4 | 0,167 | 1,54 | compartida | GUA d1t2 | d1t4 (+2t) |
| `uyama-ni` | 18 | 15 | 0,385 | 2 | 0,083 | **4,62** | inclinada→GUA | GUA d1t5 | d3t4 (+11t) |
| `biro-duma` | 15 | 12 | 0,308 | 1 | 0,042 | **7,38** | inclinada→GUA | GUA d1t2 | d1t4 (+2t) |
| `kuri-sima-pabu` | 4 | 1 | 0,026 | 3 | 0,125 | 4,88 | inclinada→AMU | **AMU+GUA d3t5** | **n/a** |

★ la única fijada en `koine_lexicon` (concepto `cuentas_vidrio`, día 1, soporte
12,8 sobre 5 variantes). `~` = acuñador aproximado por primer uso, sin registro
en `neologisms`. `n/a` = la acuñaron los dos nodos en el mismo turno.

**Tres correcciones a la lectura a mano del 2026-09-16:**

1. **`kali-iro-pabu` no es una forma compartida porque cruzara: nació en los dos
   nodos a la vez.** La acuñaron cinco agentes en el turno 5 del día 1 —Tauta y
   Talata (AMUAY, los Corubos) y Chakamba, Chirwa y Ucibo (GUARANAO, los
   Tacuatos)— en el mismo evento de nombramiento. Con tasas 0,462 y 0,458 no
   hay nada que explicar: no hubo frontera que atravesar.
2. **`tüshi-juri` no está inclinada a GUARANAO.** 16 contra 7 lo parece; 0,410
   contra 0,292 es razón 1,41 y se queda del lado compartido. Es el caso que
   justifica la normalización entera.
3. **`kuri-sima-pabu` tampoco es una innovación de AMUAY.** La acuñaron a la vez
   Tebekoa (AMUAY, Guasicures de Caseto) y Sawaka (GUARANAO, casa del Manaure)
   en el turno 5 del día 3, y sólo prendió en AMUAY. Cuatro usos en un solo
   turno de vida: **nacida, no asentada**. Su razón de 4,88 descansa en tres
   bocas, justo en el piso de la clasificación.

`kuri-bana-iro-pabu` sí está inclinada a GUARANAO (2,15), y por poco: mueve el
umbral a 2,5 y pasa a compartida. La acuñó Chuchubi (GUARANAO, los Cayudes) y
los días 2 y 3 vive casi entera en su nodo (16 de 20 usos el día 2, 14 de 17 el
día 3).

### 2.3 · El reparto entero

| Clase | Formas | GUARANAO | AMUAY |
|---|---|---|---|
| poco-atestiguada (< 3 hablantes) | 238 | — | — |
| compartida | 65 | — | — |
| inclinada | 36 | 21 | 15 |
| exclusiva | 23 | 19 | 4 |
| sin usos registrados | 7 | — | — |

**El 64 % de las formas emergentes no llega a tres bocas.** De las 124
clasificables: **84 cruzaron de nodo, 22 no cruzaron y 18 nacieron en los dos
nodos a la vez.**

**La exclusividad de este corpus es un artefacto de soporte, no una frontera
dialectal.** 17 de las 23 «exclusivas» están exactamente en el piso de 3
hablantes, y al subir el mínimo a 5 (`--min-hablantes 5`) las exclusivas caen de
**23 a 3**. Las clasificables bajan a 77, de las cuales 63 cruzaron y sólo 2 no.
Es decir: **casi todo lo que se dice lo bastante como para medirlo, cruza.**

Sensibilidad del umbral de inclinación (`--umbral`): 1,5 → 48 inclinadas · 2,0 →
36 · 3,0 → 23. El veredicto «compartida/inclinada» de las formas del borde se
mueve con él; el de las de la cabeza de la tabla, no.

### 2.4 · La velocidad del cruce

De las 21 formas con **acuñador registrado en `neologisms`** y algún uso: 18
cruzaron, 1 no, 2 nacieron multinodo. De las que cruzaron, la mediana está en
**~2 turnos** (0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 6, 6, 6, 6, 9, 11); cinco
cruzan en el **mismo turno** en que se acuñan. El máximo son 11 turnos
(`uyama-ni`, acuñada por Jaiata el día 1 y oída en AMUAY el día 3).

| Forma | Acuñador | Nodo | Acuñada | Cruzó | Clase final |
|---|---|---|---|---|---|
| `kali-iro-pabu` | Chakamba, Chirwa, Talata, Tauta, Ucibo | AMU+GUA | d1t5 | n/a | compartida |
| `kuri-bana-iro-pabu` | Chuchubi | GUARANAO | d1t5 | d1t6 (+1t) | inclinada→GUA |
| `tüshi-juri` | Hayo | GUARANAO | d2t1 | d2t1 (+0t) | compartida |
| `nii-bana` | Karebe | GUARANAO | d1t6 | d2t3 (+3t) | compartida |
| `biro-kali` | Isiro | AMUAY | d1t2 | d1t2 (+0t) | inclinada→**GUA** |
| `sima-pabu` | Tebekoa | AMUAY | d2t1 | d2t3 (+2t) | compartida |
| `sima-maa` | Isiro | AMUAY | d2t6 | d3t2 (+2t) | compartida |
| `uyama-ni` | Jaiata | GUARANAO | d1t5 | d3t4 (+11t) | inclinada→GUA |
| `sima-naa` | Jachos | GUARANAO | d1t6 | d2t4 (+4t) | exclusiva→**AMU** |
| `kali-iro-bana` | Manaure | GUARANAO | d1t5 | no cruzó | exclusiva→GUA |

Dos casos van al revés de lo que se esperaría y merecen mirada: **`biro-kali` la
acuña Isiro (AMUAY, los Corubos) y acaba inclinada a GUARANAO** (17 hablantes
contra 4), y **`sima-naa` la acuña Jachos (GUARANAO, los Cayudes) y acaba
exclusiva de AMUAY** (0 contra 5). El nodo de origen no predice el nodo donde la
forma se asienta.

Siete neologismos más se propusieron y **no los dijo nadie nunca**
(`chiriware-maa`, `duni-siwato`, `kintera-bacoa`, `kudu-ni`, `kura-iro-pabu`,
`perimetro-bana`, `tüshi-ima`). Cinco de los siete son del día 1 o del turno 6
—el último del día—, y tres de ellos son de Duraboa y Uria en el mismo turno.

---

## 3 · Un artefacto del instrumento, medido

> **En el 72,5 % de las acuñaciones (29 de 40), la forma acuñada NO queda en
> `word_uses` en la misma respuesta que la acuña.**

Al acuñar, la forma todavía no está en el léxico comunitario, así que
`palabras_caquetias` no la reconoce y `words_used` no la recoge. Comprobado en
el caso concreto: Chuchubi escribe *«Taya wana-ka kuri-bana-iro-pabu…»* en el
turno 5 del día 1, y su `words_used` contiene `bana` y `barsure` pero **no**
`kuri-bana-iro-pabu`. El primer uso que sí queda en la base es el del que la
**adoptó**, que puede ser del otro nodo — y de hecho lo fue: el día 1
`kuri-bana-iro-pabu` sólo aparece en boca de dos agentes de AMUAY, mientras que
en GUARANAO, el nodo que la acuñó, no se registra hasta el día 2.

Consecuencias, en orden de importancia:

1. **`neologisms.proposed_by` es la única fuente fiable de acuñación.** De las
   124 formas clasificables, sólo **21** tienen acuñador registrado; las otras
   103 llevan un acuñador aproximado por primer uso, marcado con `~`. Con 12
   agentes hablando en el turno 1 del día 1, ese `~` vale muy poco.
2. **Cualquier ruta de contagio leída sólo de `word_uses` invierte el origen de
   las formas que cruzan rápido.** Hay que descontarlo antes de decir «nació en
   AMUAY».
3. El conteo por nodo del día de la acuñación subestima al nodo del acuñador en
   exactamente una boca por forma.

Es una medición, no una sospecha: `analizar_nodos.py` la imprime en cada corrida
y si algún día sale 0, esta sección se borra.

---

## 4 · La distancia idiolectal: intra-nodo contra entre nodos

### 4.1 · El método, y por qué no es el del motor

Los idiolectos de `curiana_koine` **no se guardan por día en la base**: sólo
quedan enteros y al cierre en `curiana_koine.json`. Así que los vectores se
**reconstruyen desde `word_uses` × `turns`**: el vector de un agente en un día
es el `Counter` de las formas caquetías que ese día dijo. La distancia es la
misma —`1 − coseno`, con `curiana_koine._coseno`— y el filtro de agentes con
poco vocabulario también (`min_formas` 5 en ventana, 3 en emergente, los valores
con los que el orquestador llama a `distancia_idiolectal`). Lo que cambia es la
ventana: aquí es **el día**, no los últimos 10 turnos de habla.

Tres lecturas: **ventana** (el día), **emergente** (el día sin vocabulario base
ni formas de plantilla) y **acumulada emergente** (del día 1 al día d, sin base);
la tercera es control, porque converge sola por acumulación —el artefacto que
`DISENO_KOINE.md` §7 documenta.

### 4.2 · Lo medido

| Día | Lectura | n | intra GUA | intra AMU | intra | **entre** | brecha |
|---|---|---|---|---|---|---|---|
| 1 | ventana | 60 | 0,5881 | 0,6113 | 0,5945 | 0,6009 | +0,0064 |
| 2 | ventana | 62 | 0,5804 | 0,6050 | 0,5866 | 0,6005 | +0,0139 |
| 3 | ventana | 52 | 0,5474 | 0,5884 | 0,5540 | 0,5720 | +0,0180 |
| 1 | emergente | 57 | 0,8916 | 0,9031 | 0,8945 | 0,9021 | +0,0076 |
| 2 | emergente | 62 | 0,8504 | 0,8424 | 0,8484 | 0,8567 | +0,0083 |
| 3 | emergente | 52 | 0,8180 | 0,7958 | 0,8144 | 0,8107 | **−0,0037** |
| 1 | acumulada emerg. | 57 | 0,8916 | 0,9031 | 0,8945 | 0,9021 | +0,0076 |
| 2 | acumulada emerg. | 63 | 0,8141 | 0,8203 | 0,8158 | 0,8261 | +0,0103 |
| 3 | acumulada emerg. | 63 | 0,7373 | 0,7679 | 0,7456 | 0,7613 | +0,0157 |

Veredictos del día 1 al día 3 (margen del 2 % de caída relativa para llamar
«más rápido» a una de las dos):

| Lectura | intra | entre | Veredicto |
|---|---|---|---|
| ventana | 0,5945 → 0,5540 (**−6,8 %**) | 0,6009 → 0,5720 (**−4,8 %**) | **intra-nodo baja más rápido** |
| emergente | 0,8945 → 0,8144 (−8,9 %) | 0,9021 → 0,8107 (−10,1 %) | bajan igual |
| acumulada emergente | 0,8945 → 0,7456 (−16,7 %) | 0,9021 → 0,7613 (−15,6 %) | bajan igual |

### 4.3 · Contraste con lo que guardó el motor

| Día | acumulada | ventana (10 turnos) | emergente | n |
|---|---|---|---|---|
| 1 | 0,1993 | 0,6038 | 0,8995 | 60 |
| 2 | 0,2295 | 0,4665 | 0,8203 | 62 |
| 3 | 0,2357 | 0,3754 | 0,7254 | 52 |

La ventana del motor cae mucho más (0,6038 → 0,3754) que la de aquí (0,5945 →
0,5540) porque la suya es de 10 turnos de habla y a estas alturas abarca casi la
cadena entera: acumula más formas por vector y por tanto más solape. **No son la
misma cifra y no deben compararse**; el día 1 casi coinciden (0,6038 contra
0,5945) porque ahí las dos ventanas contienen aproximadamente lo mismo.

---

## 5 · Qué sostienen los datos

**No hay evidencia de koiné *entre nodos* en esta cadena. Tampoco de diglosia.
Lo que hay es que los dos nodos nunca estuvieron separados.**

La brecha entre la distancia entre-nodos y la intra-nodo es de **+0,006 a
+0,018** en la lectura de ventana, sobre distancias de ~0,6. Eso es entre el
1 % y el 3 % de la magnitud. En la lectura emergente del día 3 la brecha incluso
**se invierte** (−0,0037): los pares cruzados se parecen algo *más* que los
pares del mismo nodo. Con tres puntos, esa inversión es ruido, no un hallazgo;
lo que sí dice es que **la frontera no está separando a nadie de forma medible**.

Y es coherente con lo demás:

- de las 124 formas clasificables, **84 cruzaron**, y con un piso de soporte
  decente (5 hablantes) cruzan 63 de 77;
- las que cruzan lo hacen en **~2 turnos de mediana**, cinco de ellas en el
  mismo turno en que nacen;
- la única forma fijada en `koine_lexicon` **nació simultáneamente en los dos
  nodos**, no cruzó de uno al otro;
- las inclinaciones que quedan no siguen al nodo del acuñador (`biro-kali`,
  `sima-naa` van al revés).

**La lectura honesta es que el §1 del `DISENO_ERA2` no se está cumpliendo:
«sembrar divergencia para medir convergencia».** Y la causa está medida, no
supuesta — es la §5.1.

El único mecanismo que sí produce reparto por nodo en estos datos es la
**acuñación**: quién estuvo hablando en el turno del evento de nombramiento. Y
ese mecanismo **reparte a los dos lados a la vez**, porque el referente se le
presenta a todos los agentes activos del turno.

### 5.1 · La causa: la pre-carga de idiolectos se perdió en la era 2

> **62 de los 63 agentes de la era 2 arrancan con el MISMO vector-semilla. Sólo
> uno —Manaure— conserva el suyo.** Medido: `analizar_nodos.py` lo imprime en
> cada corrida (`divergencia_sembrada`); hay **2 vectores-semilla distintos**
> entre los 63.

`curiana_koine.FORMAS_SEED` y `EMOCIONAR_SEED` están **indexados por los nombres
de la era 1**. La campaña de antropónimos del 2026-09-14 (`8fb8b17`) renombró a
60 de los 63 agentes, y el orquestador siembra llamando `emocionar_de(nombre)` y
`formas_semilla(nombre)` con el nombre NUEVO, sin pasar por `ALIAS_ERA1`. El
único que acierta es Manaure, cuyo nombre no cambió. Los otros 62 caen al
`_NUCLEO_FALLBACK` con el aspecto por defecto y reciben, literalmente, la misma
lista: `taya · pia · nüma · naa · wana · maa · ka · mara · naa-ni · wana-ni`.
`curiana_koine.py` no menciona la palabra `nodo` ni una vez.

Esto no es un detalle de tuning. `DISENO_KOINE.md` §4 lo escribió como
precondición, en estas palabras: *«sin esta pre-carga, todos arrancan iguales y
"convergencia" no significa nada»*. Es exactamente lo que se está midiendo
arriba: dos nodos que nunca estuvieron abiertos no pueden cerrarse.

Explica de una sola vez todas las observaciones de la §5: la brecha de 0,006, la
inversión del día 3, el 84 de 124 que cruza, y que el nodo del acuñador no
prediga dónde se asienta la forma.

### 5.2 · Lo que esto sugiere hacer antes de correr más días

1. **Arreglar la siembra**: resolver `ALIAS_ERA1` al buscar en `FORMAS_SEED` y
   `EMOCIONAR_SEED`, con un test que vigile cuántos agentes del elenco activo
   reciben semilla propia. Es la pieza más barata y la que más cambia.
2. **Sembrar la divergencia POR NODO** (`FORMAS_SEED` por nodo, §8 del diseño,
   marcada «chico») — sin eso, más días de campaña miden lo mismo con más
   decimales.
3. **Escalonar los eventos de nombramiento por nodo**, o presentarlos a un nodo
   antes que al otro, para que haya una ruta que observar en vez de dos
   nacimientos simultáneos.
4. **Guardar el nodo en el esquema** (`turns` / `agent_responses` / `word_uses`,
   §8 del diseño, marcada «chico»). Hoy el nodo se resuelve por nombre contra
   `curiana_agents_era2`, y eso se rompe en cuanto los nombres cambian — pasó
   con `aafc5c32`.
5. **Guardar los idiolectos por día**, o al menos su vector, para no tener que
   reconstruirlos.

---

## 6 · Las reservas, todas juntas

1. **Tres días.** Cualquier «tendencia» son dos segmentos. El
   `veredicto_convergencia` del motor pide el último tercio de la curva; aquí el
   último tercio es un día.
2. **GUARANAO habla más de lo que le toca** (69,8 / 56,6 / 71,5 % contra un
   61,9 % del censo), y **el día 3 sólo hablaron 16 de los 24 agentes de AMUAY**.
   Es el día del que sale todo veredicto.
3. **El instrumento cambió entre el 14 y el 16.** El run `aafc5c32` (14-09) corrió
   en `19b0e16`, con `agentes_hash` distinto (los nombres de la era 1, antes de la
   campaña de antropónimos), `lexicon_hash` distinto y 198 hechos de corpus contra
   209. **No es comparable con esta cadena y no se comparó.**
4. **El instrumento también cambió *dentro* de la cadena.** Los tres días
   corrieron en tres commits distintos (`c69e042e`, `cb389991`, `1be0d52f`): entre
   el día 2 y el día 3 entraron `curiana_eventos.py` entero, `curiana_mundo`, el
   Director de la era 2 y la migración `loanword_uses`. El `corpus_hash` cambia
   entre el día 2 y el día 3 (`b8e63844` → `c845200e`). Los días 1 y 2 narraron
   con eventos de la era 1 —«Biro-ko», «los Guaycarí» en Paraguaná— y el día 3
   no. **La cadena no es un experimento de instrumento constante.**
5. **Las semillas son distintas por día** (1, 2, 3), por diseño de `--continuar`.
6. **El artefacto de la §3** (72,5 % de acuñaciones sin uso registrado) sesga toda
   ruta leída de `word_uses`.
7. **`kali-iro-pabu` es la única forma fijada en `koine_lexicon` de la cadena
   entera**, y se fijó el día 1. No hay serie de fijación que leer.
8. **La pre-carga de idiolectos no estaba activa** (§5.1). Esta cadena no es una
   prueba de la pregunta de la koiné entre nodos: es la medición de un
   instrumento al que le faltaba la mitad del montaje. Cuando se arregle, hay que
   **volver a correr los tres días**, no comparar contra estas cifras.
9. **Estatus: piloto exploratorio.** n = 1 cadena, sin ablación de compañía. El
   `DISENO_ERA2` §7 pide la mini-ablación como vara; no existe todavía.

---

## 7 · Cómo se reproduce

```bash
cd curiana_sim
python analizar_nodos.py --run 0193873d            # la tabla entera
python analizar_nodos.py --run 0193873d --formas   # sólo las formas
python analizar_nodos.py --run 0193873d --distancia
python analizar_nodos.py --run 0193873d --min-hablantes 5   # la prueba de la §2.3
python analizar_nodos.py --run 0193873d --umbral 3.0        # la sensibilidad
python analizar_nodos.py --todo                    # las cadenas de la era 2
python analizar_nodos.py --run 0193873d --json > nodos.json
```

*Relacionado: [[DISENO_ERA2]] · [[DISENO_KOINE]] · [[BITACORA_RUNS]] ·
`curiana_sim/analizar_nodos.py` · `curiana_sim/tests/test_nodos.py`*
