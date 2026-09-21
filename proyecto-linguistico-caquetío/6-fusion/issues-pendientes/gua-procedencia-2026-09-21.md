# `-gua` sí tiene fuente — pero no para lo que enseña

**Para que Miguel decida.** Campaña corta de **d21.7** («Si me parece, B»,
2026-09-21). Nada se ha aplicado: esto propone. La medición entera, con cita
literal y página impresa de cada hallazgo, está en
`6-fusion/propuesta_gua_procedencia_2026-09-21.yaml`, que **genera**
`6-fusion/scripts/medir_gua_procedencia.py` (con `--check`).

---

## 0. Lo primero, porque cambia la pregunta

El encargo decía: *¿tiene fuente `-gua`?*, dando por hecho que su único apoyo
era la frase «Topónimos venezolanos de Falcón y Sucre».

**Tiene dos fuentes, y ninguna de las dos dice «región».**

1. **La FORMA está atestiguada.** Oliver 1989, cap. 2, **p. 148**, en la sección
   «j) Suffixes /-bana/ and /-coa/»:

   > «The most common "suffixes" in Caquetío toponyms are those ending in:
   > a) -bana · b) -coa/-koa · c) -oa · d) -kiva · e) (e)-bo · **f) -wa [gua-]**»

   Es la clave foránea que la regla no tenía. **Pero Oliver glosa tres de los
   seis** —`-bana` 'surrounding/expanse', `-coa` 'superlativo de en/sobre',
   `-oa` reflexivo— y **nunca vuelve a f) -wa**. Da la forma; no da el valor.

2. **Hay un `gua` caquetío atestiguado CON glosa, y el lexicón ya lo tiene.**
   Zavala Reyes 2015, glosario **p. 68**:

   > «122. **Gua** (HP): Conuco, heredad, terreno cercado con algo.»

   Vive en `curiana_lexicon.py` como clave **`wa`**, `cat: sust`,
   `caquetío-atestiguado`, `forma_fuente: gua`, con esa cita en `notas`. O sea
   que el repo lleva las dos cosas a la vez desde hace meses —un `gua`
   sustantivo 'terreno cercado' **con** cita y un `-gua` sufijo 'región amplia'
   **sin** ella— y nadie las había puesto una al lado de la otra.

**La glosa del prompt va al revés de la de la fuente.** «Terreno cercado con
algo» es un pedazo de tierra acotado y cultivado. El motor enseña «zona más
amplia asociada con X, **menos específico** que -ana». Si es el mismo formante,
estamos enseñando lo contrario de lo que dice el único testigo.

Así que la pregunta de la campaña deja de ser «¿tiene fuente?» y pasa a ser
**«tiene fuente: ¿la glosa que enseñamos es la suya?»**. Y la respuesta medida
es que no.

---

## 1. Qué se halló

| # | Hallazgo | Obra · p. impresa |
|---|---|---|
| H1 | `-wa [gua-]` listado como sufijo toponímico caquetío, **sin glosa** | oliver-1989-cap2 · 148 |
| H2 | **«bari-si-gua (gua=/wa/)»** — Oliver escribe el valor fonémico | oliver-1989-cap2 · 142 |
| H3 | «Gua (HP): Conuco, heredad, terreno cercado con algo» | zavala-reyes-2015 · 68 |
| H4 | gu = /w/ es adaptación castellana: «watapana… more original than guatapaná» | van-buurt-2014 · 27 |
| H5 | `quigua` 'top shell' — el `-gua` de Maquigua es una concha, no un sufijo | van-buurt-2014 · 32 |

**Y el lema.** H2 y H4 dicen lo mismo que el propio lexicón ya practica:
`paragua`→`parawa`, `sibidigua`→`sibidiwa`, `quigua`→`kiwa`, `sigua`→`siwa`,
`cumaragua`→`kumarawa`. El morfema, si se conserva, debería escribirse **`-wa`**.
Es el movimiento de d21.14 (`-bacoa` → `-bakoa`). **No lo he aplicado**: es
D5/D5c (#36) y lo decides tú.

---

## 2. Qué NO se halló — y está medido

**Cinco obras, cinco búsquedas declaradas, cero apoyos para «región de».**

- **Esteves 1989.** Los **25** topónimos en `-gua` del gazetteer (10 en el
  índice de Paraguaná, 15 en el de Falcón; 23 distintos). De los que glosa:
  **9 plantas, 2 animales, 1 híbrido castellano, 5 donde él mismo segmenta y el
  corte cae en otro sitio, 10 sin etimología. Cero 'región de'.** Y no por falta
  de vocabulario locativo: cuando Esteves quiere decir lugar usa `bacoa`,
  `bana`, `ebo`, `uco/duco`, `are` — los cinco con glosa.

  El caso que decide es **Urupaguaduco** (p. 66): *«significa la quebrada de las
  urupaguas»*. Ahí sí hay locativo y **es `-duco`**; `urupagua` entra entero
  como nombre de planta.

  Los cinco que parten por otro sitio, con sus palabras:
  - **Barisigua** (p. 19): *«Bari —sigua: palo blando; bara; árbol. Sigua:
    blando»* — el `-gua` es la cola de `sigua` 'blando', voz atestiguada aparte
    (Zavala #227, p. 70).
  - **Maquigua** (p. 49): *«En antiguas escrituras se lee: Moriquigua. […]
    Quigua: concha de almeja»* — el segmento es `quigua` (Zavala #214, p. 70).
  - **Caradacagua** (p. 33): *«una reducción de Caramatacaigua… En lengua
    cumanagota, “caramata” es carbón y “caigua” es un molusco»* — filiación
    **cumanagoto** declarada (la trampa 4), y el `gua` va dentro de `caigua`.
  - **Dibaragua** (p. 38): *«la prótesis silábica “di” y la metátesis de
    “baragua” por “guaraba”»* — el `gua` viene de un `gua-` **inicial**.
  - **Chiguarigua** (p. 107): *«Voz compuesta de “chigua”, nasa, cesto, y
    “arigua”, un insecto melífero»* — los dos trozos llevan `gua` dentro.

  Y la contaminación castellana existe y está medida: **Quiyegua** (p. 57) es
  *«una voz híbrida de español y caquetío: Piedra y Yegua»*.

- **Alvarado 1921.** Cero enunciados sobre un formante. Lo que tiene son
  lexemas: «BARISÍGUA. Árbol indeterminado de Coro y Zulia» (p. 23), «ARÍGUA.
  Especie de abeja silvestre», «ASYÁGUA. Médula del maguéi». Plantas y bichos.
- **Jahn 1927.** Sí enumera desinencias toponímicas arahuacas, y `gua` no está:
  *«tienen en sus terminaciones la desinencia ari, uri, e iri, que revelan su
  procedencia de las lenguas aruacas»*.
- **Arcaya 1920.** Cero. `gua` sólo dentro de topónimos (Acurigua, Barragua,
  Churuguara).
- **Medina Colina (habla viva del s. XX).** Lo tiene registrado, y como lo
  contrario de un locativo: `patrones_observados` §`-igua` — *«barisigua
  (Erythrina), con tacarigua y samanigua de Alvarado y los topónimos regionales
  en -igua: **formante fitonímico**/toponímico de filiación no resuelta»*.

Una negativa así de repartida no es un hueco de minería. Es un resultado.

---

## 3. El azar, medido

`-gua` es el **2.º final de tres letras más frecuente** del gazetteer (**23 de
565**), pegado a `-are` (24), `-ure` (22) y `-ana` (22). Una terminación no es
un morfema hasta que el resto es raíz conocida **con sentido**:

| final | termina en | el resto es raíz | sobrevive al filtro de significado |
|---|---|---|---|
| `-gua` | 23 | 5 | **0** |
| `-are` | 24 | 3 | — |
| `-ure` | 22 | 2 | — |
| `-ana` | 22 | 5 | — |

Los cinco aciertos de `-gua`, revisados uno a uno (skill `minar-fuente` §2 —
cinco falsos de siete en el cruce achagua):

- `bajarigua ← bajarí` 'recorrer, caminar' · Bajarigua es una salina. **No.**
- `barisigua ← barici` 'agua turbia' · es un bucare, y Esteves parte por
  `bari+sigua`. **No.**
- `casigua ← kasi` 'sol' · es una marantácea. **No.**
- `guagua ← gua` · casa con la propia forma bajo examen. **Circular.**
- `baragua ← bara` 'palo, árbol' · el significado **sí** casa… pero entonces el
  resto es `-gua` sobre un árbol, no una región, y Esteves lo glosa como el
  nombre entero del árbol. **Parcial, y en contra.**

El dato que más pesa: **`-ana` da exactamente la misma tasa, y su glosa 'lugar
de' se retiró por eso en #109.** Aplicar dos varas distintas a la misma
medición sería el error que esa decisión ya corrigió.

---

## 4. El «apoyo que ya existe en el canon» es circular

d21.7 dice: *«`paragua` se lee como `para` 'mar' + `-gua`, y por eso el
2026-09-19 se decidió NO fusionar `parawa`/`para`»*.

La decisión del 09-19 (`curacion_glosas_pares_2026-09-19.yaml`, par 14) se
apoya en **tres** patas, y d21.7 recoge la tercera:

1. los esqueletos fonémicos no coinciden (`para` / `parawa`, con y sin gu→w);
2. Zavala las trae como dos entradas de **dos informantes**, #190 (E+HP) y #191
   (GC);
3. *«`-gua` es un LOCATIVO declarado del proyecto ('región de X',
   `REGLAS_LOCATIVAS`), así que `paragua` se lee sin forzar nada como `para` +
   `-gua`»*.

🔴 **La pata (3) usa el morfema como prueba de sí mismo.** Las patas (1) y (2)
son independientes, así que **la decisión de no fusionar `parawa`/`para` no se
cae** — lo que se cae es que ese par sirva de apoyo a `-gua`.

Y hay una explicación rival con fuente: Oliver p. 150 da el taíno de 'mar' como
**`/bara-wa/`** junto al guajiro `/palaa'/`. El `-wa` de `parawa` tiene hermano
arahuaco **dentro de la misma palabra**: es voz heredada, no `para` + 'conuco'.

**Dos cosas más que salieron de paso:**

- **El mismo topónimo sostiene dos glosas incompatibles en el mismo repo.**
  `Paraguaná` es ejemplo de `-gua` 'región' en el prompt, y de `gua` 'terreno
  cercado' (#122) en `toponimos.yaml` (toponimo-018) y en
  `censo_ana_esteves_109.yaml`. Es la patología (a) de la tabla de morfología
  otra vez: el motor enseña una cosa y el canon declara otra.
- **Un ejemplo que no ejemplifica.** El tercer ejemplo de la regla es «Araya
  (región salina)» — un topónimo de Sucre que **no contiene `-gua`**. Se quedó
  en d21.14, que sólo comprobó que las raíces estuvieran en el lexicón.
- **La frase «Topónimos venezolanos de Falcón y Sucre» entró en el commit
  inicial del repo** (`475457d`) y no se ha tocado desde entonces: es anterior a
  la regla 8 y nunca tuvo clave foránea.

---

## 5. Y lo que la gente hace con él

Medido sobre `word_uses` con runs `started_at < '2026-09-21'` y la segmentación
del motor: **102 usos · 49 formas · 37 raíces** (reproduce exactamente la cifra
de d21.7). Pero repartido así:

| categoría de la raíz | usos |
|---|---|
| `v_raiz` | 65 |
| raíz fuera del lexicón | 23 |
| `sust` | 7 |
| `adj` | 7 |

**Dos de cada tres usos ponen el locativo sobre una raíz verbal**: `awa-gua`
(beber), `jai-bana-gua` (oír), `kono-gua`. «La región de beber» no es lo que la
glosa promete. El campo `uso` de la regla dice «RAÍZ + -gua» y no declara slot,
así que nada lo impide. **Decidas lo que decidas sobre la glosa, el slot hay que
declararlo** — es el mismo hueco que d21.5 cerró para `ka-`/`ma-`.

---

## 6. Las opciones

**A — Se queda como está, con la deuda declarada.**
Sigue `deuda: sin-procedencia` y sigue enseñándose «región / área amplia». Es lo
que d21.7 dejó rigiendo mientras tanto. **Coste**: ahora sabemos que la deuda no
es «falta fuente» sino «hay fuente y dice otra cosa», y dejarlo así es enseñar
a sabiendas una glosa que el canon contradice. Es exactamente lo que `-ana`
hizo durante dos semanas y que d21.6 llamó *«el canon decidiendo una cosa y el
prompt diciendo otra»*.

**B — Se re-glosa con lo atestiguado: `-gua` pasa a ser el `wa` de Zavala.**
La regla deja de ser «región, área amplia» y pasa a «conuco, heredad, terreno
cercado», con su cita (Zavala 2015 #122, p. 68) y su clave foránea, y la capa
sube de `reconstruido` a `atestiguado`. **Coste**: hay que decidir si el
sustantivo `wa` y el sufijo `-gua` son el mismo morfema — Zavala lo da como
lema suelto, no como desinencia — y hay que resolver la colisión con el
posesivo `wa-` 'nuestro' y con el `wa-` de pluralidad de `morfemas.yaml`
(morfema-006). Tres `wa` distintos en el mismo sistema es un problema nuevo.

**C — Se enseña SIN GLOSA, como `-ana`, `-ubana` y `-uru`.**
La forma se queda (la atestigua Oliver p. 148), la glosa 'región' se retira, y
el agente puede usarla proponiendo él el valor entre corchetes. Es literalmente
el patrón que tú elegiste hace cinco días en d21.6 para el caso gemelo, y el
que el proyecto ya tiene para una desinencia atestiguada sin valor anotado.
**Coste**: el prompt pierde el único recurso que nombra «región», y los 102 usos
actuales quedan sin modelo — aunque 65 de ellos ya iban sobre verbo, o sea que
el modelo no se estaba siguiendo.

**D — Se retira a `REGLAS_RETIRADAS`, como `-ko`, `-sha` y `-naiki`.**
**Coste**: tirarías un formante que Oliver **sí** atestigua. `-naiki` se retiró
con 0 usos y sin ninguna fuente; aquí hay 102 usos y hay fuente para la forma.
Lo digo para que esté sobre la mesa, no porque lo recomiende.

**E — Se cambia el lema a `-wa` (D5c).**
Ortogonal a las anteriores: cualquiera de A–D puede ir con `-gua` o con `-wa`.
Hay dos fuentes para hacerlo (Oliver p. 142 «gua=/wa/», van Buurt p. 27) y el
lexicón ya lo practica en cinco lemas. **Coste**: mueve `_SUFIJOS_CAQ`, o sea
que hay que medir antes con el patrón A/B, igual que d21.9; y es D5/D5c (#36),
que es una decisión más grande que esta campaña.

---

## 7. Mi recomendación

**C, con la nota de B escrita, y E aparte.**

Por qué C y no B: para re-glosar como 'conuco, terreno cercado' hay que afirmar
que el sustantivo `gua` de Zavala **es** el sufijo de Oliver, y eso no lo dice
ninguna fuente — lo diría el proyecto. Sería cambiar una glosa sin apoyo por
otra glosa sin apoyo, sólo que esta vez con una cita al lado que en realidad
habla de otra cosa. En duda, degradar (regla 2).

Por qué C y no A: porque ahora hay fuente para la forma y hay fuente contra la
glosa. `deuda: sin-procedencia` se queda corto y además ya no es cierto: la
deuda es de VALOR, no de procedencia, y conviene que el campo lo diga.

Por qué C y no D: Oliver lo lista. Tirarlo sería el error inverso al de `-ana`.

Lo que C cuesta de verdad —quedarse sin manera de decir «región»— es
precisamente la clase de hueco que esta simulación existe para llenar: si los
agentes necesitan la noción, que la propongan ellos y se mida cuál gana. Es el
argumento con el que cerraste d21.6.

**Y lo que hay que escribir pase lo que pase, decidas A, B, C o D:**

1. El **slot**. Hoy es `cualquiera` y el 64 % del uso cae sobre verbo.
2. La **nota de B** en la evidencia de la regla: que existe `wa` #122 'conuco,
   terreno cercado' con cita, y que es la lectura que el canon usa para
   Paraguaná. Que no se vuelva a perder.
3. **«Araya (región salina)»** sale de los ejemplos: no contiene el morfema.
4. Que `Paraguaná` deje de ejemplificar dos glosas incompatibles a la vez.

---

## 8. Lo que esta campaña no pudo medir

- **Hill Peña (HP)**, el compilador del que Zavala toma #122, no tiene obra en
  `fuentes_caquetios/` ni entrada en `bibliografia.yaml`. La cadena es
  Zavala → HP y del segundo eslabón no se verifica nada. Es **una** atestación,
  no dos.
- **El OCR de Esteves es pista, no cita** (así lo declara su propia nota). Las
  cinco citas de §2 llevan página impresa y **hay que verlas en imagen** antes
  de sacarlas del repo. Las de Zavala, van Buurt y Oliver salen de capa de texto
  propia y están verificadas contra el PDF.
- El censo de Esteves se hizo sobre el **índice** de la parte 1 (187 nombres) y
  las **387** entradas parseadas de la parte 2. No cubre los 413 topónimos que
  la nota de la fuente atribuye al libro entero.
- No se midió el corpus insular (Gatschet, van Buurt ABC) como universo del test
  del azar: allí el formante frecuente es `-shi/-chi`, que `morfemas.yaml`
  declara sin glosar (morfema-007) y que su propia nota llama **«el objetivo
  nº 1 de cualquier minería futura de toponimia ABC»**. Es otra campaña.

## 9. Lo que vi de paso y merece campaña propia

- **`-igua` como formante FITONÍMICO.** Nueve de las glosas de Esteves en
  `-gua` son plantas, Medina Colina lo tiene anotado como patrón del habla viva,
  y Alvarado añade `barisígua`, `tacarigua`, `samanigua`, `asyágua`. Si `-gua`
  es algo, el candidato con más apoyos **no** es 'región': es 'planta'. No lo he
  propuesto como glosa porque ninguna fuente lo enuncia — pero nueve casos es
  más de lo que tenía `-are` cuando se despejó.
- **Tres `wa` distintos en el sistema**: el sustantivo `wa` 'conuco' (Zavala
  #122), el posesivo `wa-` 'nuestro' que el prompt enseña, y el `wa-` de
  pluralidad / 'tener' de `morfemas.yaml` morfema-006 (van Buurt §6, de Goeje
  1928) — al que Oliver p. 147 añade un cuarto valor: *«The prefix /wa- [gua-]/
  is a third person plural marker»*. Cuatro lecturas de la misma sílaba, ninguna
  declarada frente a las otras.
