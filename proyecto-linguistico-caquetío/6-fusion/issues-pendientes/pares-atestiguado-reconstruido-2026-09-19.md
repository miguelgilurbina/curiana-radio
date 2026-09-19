# Dos palabras para la misma cosa: los pares atestiguado / reconstruido

Miguel, 2026-09-18, de oído:

> «¿Por qué es `kali` si sol es `kazi`?»

**Para que Miguel decida, par a par.** Esto es una MEDICIÓN del lexicón, de la
base y del prompt. **No se tocó nada**: ni `curiana_lexicon.py`, ni el motor,
ni las plantillas (regla 5).

| archivo | qué tiene |
|---|---|
| `6-fusion/pares_atestiguado_reconstruido_2026-09-19.yaml` | los pares, con las dos fichas enteras, sus citas, su uso por era y serie y su exposición en el prompt |
| `6-fusion/scripts/medir_pares_atestiguado_reconstruido.py` | lo mide todo y escribe el YAML |

**Ninguna cifra de aquí abajo está escrita a mano.** Las imprime
`python 6-fusion/scripts/medir_pares_atestiguado_reconstruido.py`, con los dos
controles en verde:

```
entradas con `fuente` que empieza por «caquetío-»: 401
   atestiguado 228 · reconstruido 86 · retroabstraído 49 · hipotético 38
   con `caquetío` a secas (fuera del criterio): 0

PARES — criterio ESTRICTO (glosa normalizada idéntica):        3
PARES — criterio LAXO (+ sinónimo compartido):                19
   atestiguado × reconstruido    estricto 3   laxo 17
   atestiguado × retroabstraído  estricto 0   laxo  0
   atestiguado × hipotético      estricto 0   laxo  2
POR CONTENCIÓN (exploratorio, ruidoso — se lista aparte):     28
SÓLO OTRA GRAFÍA, dentro de los pares:                         0
MISMO ESQUELETO FONÉMICO, buscando por la FORMA:               5

control de raíz: 0 discrepancias en 2271 tokens
serie C limpia es cadena: True (b847944d → 17c2271e → 9a98de67, 3 días, 18 turnos)
```

---

## 1. El criterio, declarado

La glosa (`sig`) es texto libre — «sol», «cerro, sitio alto», «yo (1ra persona
singular)» —, así que hay que normalizarla antes de comparar, y la
normalización es una decisión que conviene tener escrita.

**Normalización:** NFC + minúsculas · fuera lo que va entre paréntesis y
corchetes · fuera los diacríticos (á→a, ü→u, ñ→n) · fuera el artículo inicial
y la puntuación de los extremos · espacios colapsados.

**No se aplica ningún diccionario de sinónimos.** Decidir que «cerro» y «loma»
son la misma glosa es una afirmación sobre el significado, y eso lo decides tú
(regla 2: en duda, degradar). Lo que el encargo llamaba «sinónimos evidentes»
se captura sin inventar nada: comparando los sinónimos **que la propia glosa
ya separa con una coma**.

| criterio | qué exige | n |
|---|---|---:|
| **ESTRICTO** | la glosa normalizada completa es idéntica | **3** |
| **LAXO** | estricto, o las dos glosas comparten uno de sus propios sinónimos | **19** |
| *contención* | *una glosa entera cae dentro de la otra («grande» dentro de «ave rapaz grande»)* | *28, aparte* |

La contención va **aparte y no cuenta**: es ruidosa por construcción — casi
todo lo que añade es un modificador compartido, no un par de palabras rivales.
Está en el YAML (`por_contencion_exploratorio`) por si quieres verla.

**Los compuestos los decide el motor, no un regex mío.** `_candidatos_motor()`
reproduce paso a paso la construcción de candidatos de
`curiana_lexicon._familia_de_token()` **con las tablas de afijos del propio
motor** (`_PREFIJOS_CAQ`, `_SUFIJOS_CAQ`, `_RAICES_VERB`), y el control
comprueba token a token, sobre los 2.271 tokens distintos de la base, que da
la misma lengua que el motor: **0 discrepancias**. Un token es de la familia de
una raíz si ES la raíz, si la lleva como elemento separado por guion, o si la
raíz aparece al deshacer prefijos y sufijos. *Residuo declarado*: las formas
aglutinadas sin guion no entran — `kali-kasibana` cuenta para `kali` y no para
`kasi`, porque su segundo elemento es `kasibana`. El motor tampoco las
segmenta: es la misma ceguera, no una distinta.

---

## 2. El hallazgo: **decide la plantilla, no el muestreador**

Cruzando «a qué forma enseña una plantilla estática» con «qué forma se dice
más» en toda la base, sobre los 19 pares:

| a quién enseña una plantilla | gana la atestiguada | gana la derivada |
|---|---:|---:|
| **sólo a la derivada** | 0 | **12** |
| **sólo a la atestiguada** | — | — |
| a las dos | 1 | 2 |
| **a ninguna** | **4** | 0 |

**Doce de doce y cuatro de cuatro.** Cuando la plantilla enseña sólo la
reconstruida, gana la reconstruida, siempre. Cuando no enseña a ninguna de las
dos, gana la atestiguada, siempre. Los tres casos mixtos se reparten.

No es causal —nadie ha corrido el contrafactual— pero no deja mucho sitio: la
capa epistémica no explica nada que el prompt no explique antes.

---

## 3. La exposición: el muestreador ya favorece a la atestiguada, y pierde igual

Ensayo sin API (`random.seed(20260919)`): los 63 agentes del elenco de la era
2, cada uno con su tier real y su presupuesto de voces (50 / 42 / 20), 20
sorteos cada uno = **1.260 prompts**, con las capas del perfil `era2` y el
campo léxico vacío.

| forma | capa | cubo del muestreador | sale en el muestreo | la enseña una plantilla | uso (toda la base) |
|---|---|---|---:|---|---:|
| `kasi` sol | atestiguada | `sust` (226 voces) | 60/1260 | — | 10 |
| `kali` sol | reconstruida | `sust` (226 voces) | 63/1260 | **IDENTIDAD_LINGUISTICA** + reglas completo | **2.321** |
| `kati` luna | atestiguada | `cosmos` (2 voces) | **624/1260** | IDENTIDAD_LINGUISTICA | 42 |
| `kasha` luna | reconstruida | `sust` (226 voces) | 59/1260 | reglas completo | 168 |

Dos cosas, y las dos importan para la pregunta (b) de abajo:

1. **Para «sol» el muestreador es neutro** (60 contra 63) y aun así la
   reconstruida gana **232 a 1**. La asimetría es entera del ejemplo de la
   plantilla.
2. **Para «luna» el muestreador ya favorece a la atestiguada diez a uno**
   (624 contra 59) y la reconstruida seguía ganando 168 a 42. Lo único que
   movió la aguja fue que `kati` también entrara en una plantilla: en la
   **serie C limpia** el marcador es **11 a 11**, y `kati` sube (era 1: 8 ·
   serie C: 30).

La exposición del muestreo **no la decide la capa epistémica: la decide el
tamaño del cubo.** `repartir_cuotas()` da una voz a cada cubo antes de repartir
el resto, así que `para` —sola en el cubo `geografia`— sale en **1.260 de
1.260** prompts, y `kasi` —una de las 226 del cubo `sust`— en uno de cada
veinte. Hay **12 cubos de una sola voz** sobre 25, para 363 voces caquetías.

`[Tu tierra]` no enseña ninguna de las formas de ningún par: **0 de 126**
bloques. Confirma lo que ya decía la tabla de trampas.

---

## 4. Los que son sólo otra grafía (los más baratos)

**Dentro de los pares: cero.** D5a ya hizo su trabajo — `cazi`→`kasi` y
`cati`→`kati` están fusionadas, con la grafía de fuente en `forma_fuente`.

Buscando por la **forma** en vez de por la glosa —entradas atestiguada y
derivada con el mismo esqueleto fonémico (`curiana_fonotactica.fonemizar`, con
y sin la regla abierta gu→w)— salen **5**. Son **candidatas, no veredictos**:
el esqueleto sólo dice que las dos se escriben igual una vez quitada la grafía
colonial; si son la misma palabra lo dicen las glosas.

| esqueleto | atestiguada | derivada | ¿qué es? |
|---|---|---|---|
| `arifuke` | `harifuche` 'maíz tostado y miel' (Zavala #153) | `arifuke` 'harina de maíz…' (retroabstraída, Medina Colina 2013 p.31) | **la única que parece de verdad la misma palabra.** Dos preparaciones de maíz, dos fuentes, un esqueleto. Fusión pendiente, no decisión de canon |
| `kasi` | `kasi` 'sol' | `kashi` 'ahora, en este momento' | **colisión**, no variante — pero es un dato: bajo la fonemización del propio proyecto, «sol» y «ahora» son homógrafas |
| `kasa` | `kasá` 'puche de maíz' | `kasha` 'luna' | colisión |
| `amaka` | `amaka` 'sitio de moler maíz' | `hamaka` 'hamaca' | colisión |
| `koro` | `koro` 'cotorra' (Zavala #181) | `coro` 'cardón grande' (hipotética) | **ya adjudicada**: D5b (`decisiones_tanda_2026-08-30.yaml` §d5.b_pares) dice «NO TOCAR: falso positivo» |

Que el barrido re-encuentre el caso que D5b ya resolvió es el control de que
está mirando donde debe.

---

## 5. Sol y luna, en detalle

### `kasi` (atestiguada) contra `kali` (reconstruida) — 'sol'

|  | `kasi` | `kali` |
|---|---|---|
| capa | `caquetío-atestiguado`, `forma_fuente: cazi` | `caquetío-reconstruido`, «núcleo fundacional» |
| cita | Zavala Reyes 2015, glosario #76 (GC): «Sol» | «forma justificada por cognado en lokono/garifuna» — sin obra citada |
| toda la base | 9 sueltas + 1 compuesta = **10** | 867 sueltas + 1.454 compuestas = **2.321** |
| serie C limpia | 3 + 1 = **4** | 52 + 50 = **102** |
| la enseña | nadie | **IDENTIDAD_LINGUISTICA** (los 63, cada turno) y reglas completo (los 15 del tier 1) |
| compuestas en la serie C limpia | `kasi-bana` 1 | `kali-mara-bana` 12, `kali-ubana-gua` 12, `kali-naa-iro` 10, `kali-raku-biro` 5, `ma-kali` 3… |

**25 a 1 en la serie limpia**, 232 a 1 en toda la base, con el muestreador
neutro. Y la koiné se está construyendo encima: `kali-mara-bana` es la primera
entrada fijada de la era.

### `kati` (atestiguada) contra `kasha` (reconstruida) — 'luna'

`kati` es el `cati` de las fuentes fusionado por D5 (Zavala #71, CGB), con
cognados proto-arahuaco \*kati, WY *kachi*, LK *katsi*. `kasha` lleva **deuda
D11** declarada en su propia nota — y esa nota cita como apoyo el lokono
`kathi`, que es precisamente el cognado de `kati`. **La atestiguada es además
la mejor reconstrucción bajo D11.**

Marcador: 42 a 168 en toda la base, pero **11 a 11 en la serie C limpia**, con
`kati` subiendo. Es el par más barato de cerrar de los tres estrictos.

---

## 6. Las decisiones, par a par

**Las opciones, siempre las mismas.** Para cada par:

- **A** — manda la atestiguada. La reconstruida **no se borra** (se archiva con
  su procedencia, como `piache`): lo que se le quita es que el prompt la
  enseñe.
- **B** — **conviven, declaradas como variación**. Una lengua puede tener dos
  palabras para el sol. Si es B, hay que decirlo en el lexicón y que el
  instrumento deje de empujar a una de las dos por accidente.
- **C** — caso especial, explicado en cada fila.

Y una **regla de casa** que propongo para no decidir diecinueve veces a ojo:
*glosa idéntica → hay que elegir (A). Glosa que sólo comparte un sinónimo →
B, y de paso se afina la glosa para que deje de parecer un par (eso es
curación, no canon).*

> **Ojo con lo que esto NO es.** De los 19, sólo **6** son rivales de verdad
> (1, 3, 6, 12, 13, 16). Los otros 13 son **bugs de curación** —una `cat`
> equivocada, una glosa demasiado ancha, una deuda ya declarada— que el
> criterio laxo saca a la luz. Eso también es un resultado.

| # | glosa | atestiguada | derivada | uso base | serie C | recomiendo |
|---:|---|---|---|---:|---:|---|
| 1 | **sol** | `kasi` | `kali` (recon) | 10 : 2321 | 4 : 102 | **A** |
| 2 | crear | `eroa` | `chaa` (recon) | 97 : 1256 | 5 : 30 | B |
| 3 | **ofrecer** | `were` | `paa` (recon) | 17 : 1222 | 2 : 37 | B |
| 4 | escuchar | `jai` | `kira` (recon) | 167 : 831 | 12 : 32 | B |
| 5 | pez | `bagre` | `arima` (recon) | 0 : 643 | 0 : 45 | C |
| 6 | **cerro** | `turumako` | `sima` (recon) | 1 : 510 | 1 : 13 | C |
| 7 | hijo | `dare` | `buri` (recon) | 18 : 303 | 5 : 8 | C |
| 8 | sembrar | `jusual` | `kono` (recon) | 4 : 221 | 0 : 16 | C |
| 9 | árbol | `bara` | `kuru` (recon) | 38 : 211 | 4 : 6 | B |
| 10 | árbol | `igi` | `kuru` (recon) | 6 : 211 | 1 : 6 | C |
| 11 | luna | `apana` | `kasha` (recon) | 16 : 168 | 3 : 11 | C |
| 12 | **luna** | `kati` | `kasha` (recon) | 42 : 168 | 11 : 11 | **A** |
| 13 | **mar** | `para` | `habo` (recon) | 311 : 125 | 48 : 6 | **A** |
| 14 | mar | `parawa` | `habo` (recon) | 0 : 125 | 0 : 6 | C |
| 15 | anciano | `wasima` | `wanü` (recon) | 10 : 120 | 2 : 5 | C |
| 16 | **viento** | `juri` | `joutai` (recon) | 544 : 19 | 154 : 1 | **A** |
| 17 | cactus columnar | `kadushi` | `coro` (hipot.) | 120 : 1 | 0 : 0 | C |
| 18 | espanto | `etamo` | `mülia` (hipot.) | 20 : 0 | 1 : 0 | A |
| 19 | iguana | `barbache` | `iguana` (recon) | 2 : 0 | 0 : 0 | C |

### Lo que hay detrás de cada recomendación

1. **sol · A.** Glosa idéntica, cita sólida (Zavala #76) contra una nota sin
   obra. El muestreador es neutro: **todo** el 232 a 1 es el ejemplo de la
   plantilla. *Coste:* corte de serie (§7) y, sobre todo, **`kasi` y `kashi`
   'ahora' comparten esqueleto fonémico** bajo la propia `fonemizar` del
   proyecto, y `kashi` está en las dos plantillas de reglas y lleva 2.537 usos.
   Si ese choque te parece inasumible, la respuesta honrada es **B**.
2. **crear · B.** No son la misma palabra: `eroa` es 'empezar, crear,
   originar' (Zavala #119) y `chaa` 'hacer, construir'. Comparten una palabra
   de la glosa, nada más. Afinar la glosa de `chaa` y cerrar.
3. **ofrecer · B, pero es el par más caro.** 'dar, entregar, ofrecer' contra
   'dar, ofrecer, transferir' son de verdad lo mismo. La A sería retirar `paa`
   de la enseñanza, y `paa` es una raíz verbal del núcleo con 1.222 usos y todo
   su paradigma de aspecto. Recomiendo B declarada; si quieres A, dilo y se
   mide aparte.
4. **escuchar · B.** Igual que 3, con menos dinero encima: `jai` (Zavala #175)
   ya lleva 167 usos sin que nadie se lo enseñe.
5. **pez · C.** `bagre` no significa 'pez': es un pez concreto, y su propia
   nota avisa de que es homógrafo del español. Corregir la glosa; no es par.
6. **cerro · C.** `turumako` 'cerro, meseta' (Zavala #262) contra `sima`
   'cerro, montaña'. Pero **el caquetío ya dice 'cerro' con `-bana`**
   (atestiguado, D9, seis apoyos), así que el par en realidad es a tres bandas.
   Pregunta: ¿`sima` sobra?
7. **hijo · C.** La glosa de `dare` ya lleva **deuda declarada**: la fuente
   dice 'diente' y 'hijo' es extensión del proyecto. Resolver la deuda antes
   de llamarlo par.
8. **sembrar · C.** `jusual` es sustantivo ('siembra, sembradío, conuco') y
   `kono` raíz verbal. No compiten; la glosa engaña.
9. **árbol · B.** `bara` 'palo, árbol' (decisión #101) contra `kuru` 'árbol,
   madera, tronco'. Variación real y útil — el palo cortado y el árbol vivo.
10. **árbol · C.** `igi` es un árbol concreto (matapalo/paují). Glosa.
11. **luna · C, y es un fallo del criterio, dicho.** `apana` glosa 'una luna
    (unidad de tiempo ~30 días)' — es **el mes**, no el astro. Empareja sólo
    porque la normalización quita el paréntesis. Reglosar a 'mes'.
12. **luna · A, la más barata de las tres estrictas.** `kati` es atestiguada
    (Zavala #71) **y** la mejor reconstrucción bajo D11 — el lokono `kathi`
    que la nota de `kasha` cita como apoyo es su propio cognado. Ya va 11 a 11
    en la serie limpia y subiendo.
13. **mar · A, y casi no cuesta.** `para` ya gana 311 a 125 y 48 a 6: el uso
    real va por delante de la decisión. Reflejo de proto-arahuaco \*para
    atestiguado en cuatro lenguas.
14. **mar · C.** `parawa` (Zavala #191, GC) y `para` (Zavala #190) son la
    misma palabra en dos fuentes. Es D5, no canon: ¿se fusionan?
15. **anciano · C.** `wasima` está declarada `v_raiz` siendo un adjetivo, y
    **es homógrafa de un nombre del elenco**. Arreglar la ficha primero.
16. **viento · A, y es la única que no cuesta nada.** `joutai` declara en su
    propia glosa que viene del wayuu («< joutai Wayunaiki»), que es justo lo
    que D11 retiró. `juri` (Zavala #178) ya gana 544 a 19 y **154 a 1** en la
    serie limpia. Ninguna plantilla enseña a ninguna de las dos: **retirar
    `joutai` de la enseñanza no cambia ni un byte del prompt y no obliga a
    cortar serie.**
17. **cactus · C, ya decidido.** D10 le quitó a `coro` el respaldo de la glosa
    'cardón' y el perfil `era2` ni siquiera la muestra (0 de 1.260). Sólo
    queda limpiar.
18. **espanto · A, gratis.** `mülia` es hipotética, 0 usos, 0 exposición.
19. **iguana · C.** La forma «reconstruida» es la palabra castellana `iguana`;
    su sitio está en el trabajo de `FORMA_DE_LA_ESFERA`
    (`descastellanizar_esfera_2026-09-18.yaml`), no aquí. Y `barbache` está
    declarada `v_raiz` siendo un sustantivo.

---

## 7. Las dos preguntas de instrumento

**Las dos cambian lo que el agente VE, y por tanto las dos obligan a un CORTE
DE SERIE**: la serie C se repetiría desde el día 1, igual que el 2026-09-18.
Coste medido de la serie C limpia: **3 días, 18 turnos** (`b847944d` →
`17c2271e` → `9a98de67`), a ≈ 11 min de API el día ≈ **33 min**. Las dos se
pueden aplicar en el mismo corte; hacerlas por separado cuesta el doble.

### (a) ¿El ejemplo de `IDENTIDAD_LINGUISTICA` deja de usar `kali-bana`?

Hoy dice, y lo leen **los 63 cada turno** (`curiana_orchestrator_v2.py`, el
ensamblado del system prompt no mira el tier):

```
EJEMPLO: "Taya wana-ka arima wara kari. Ta-barsure naba-ni.
          [kali-bana: kali+-bana = cerro del sol]."
```

`kali-bana` lleva **235 usos** en la base. Desde el corte del 2026-09-18 ya no
puede registrarse como acuñación (#169), **pero se sigue enseñando** — y el
corte no tocó los compuestos: en la serie C limpia se dijeron `kali-mara-bana`
12 veces, `kali-ubana-gua` 12, `kali-naa-iro` 10 y `kali-raku-biro` 5. Cerrar
la puerta a la forma no cierra la puerta al molde.

Pase lo que pase el ejemplo enseña algo; la pregunta es **qué**. El script
lista las raíces que cumplen cinco condiciones verificadas —atestiguada, con
cita, no homógrafa de un nombre del elenco, que no sea forma de ningún par
abierto, y cuyo compuesto con `-bana` **no se haya dicho nunca** en la base—:

| propuesta | raíz | cita | usos de la raíz |
|---|---|---|---:|
| **`[biro-bana: biro+-bana = cerro de la sal]`** | `biro` 'sal' | Zavala Reyes 2015 (Angulo Molina); recurso estratégico de Coro | 694 |
| `[kari-bana: kari+-bana = cerro de la orilla]` | `kari` 'orilla del mar' (`forma_fuente: cari`) | Zavala Reyes 2015 #66 (E); Cruz Esteves 1989 vía van Buurt | 78 |
| `[maure-bana: maure+-bana = cerro del algodón]` | `maure` 'fibra de algodón' | Zavala nota al pie (3); Alvarado 1921 p.216; Carvajal; Castellanos | 217 |

**Recomiendo `biro-bana`.** Las dos piezas son atestiguadas (`-bana` 'cerro,
sitio alto' lo cerró D9 con seis apoyos), la raíz es la que el mundo de la era
2 tiene delante —la sal es el recurso de Paraguaná— y el compuesto no se ha
dicho jamás, así que el ejemplo no bendice a nadie que ya esté compitiendo. Y
sobre todo: **no toca ningún par de §6**, así que la decisión (a) se puede
tomar antes que las diecinueve.

*Alternativa que no cuesta corte de serie:* dejar el ejemplo y aceptar que el
molde `X-bana` es del instrumento. Es defendible, pero entonces hay que decirlo
en el diseño de la koiné, porque `kali-mara-bana` —la primera entrada fijada de
la era— nació de ahí.

### (b) ¿El muestreador prefiere la atestiguada cuando hay par?

**Recomiendo que no, o al menos no primero**, y la medición es la razón:

- Para «sol», el muestreador ya es neutro (60 contra 63 de 1.260) y la
  reconstruida gana 232 a 1. Tocar el muestreador **no habría movido nada**.
- Para «luna», el muestreador ya favorece a la atestiguada **diez a uno** (624
  contra 59) y la reconstruida seguía ganando. Lo que empató el marcador fue
  que `kati` entrara también en una plantilla.
- Y lo que decide la exposición del muestreo hoy **no es la capa sino el
  tamaño del cubo**: 12 de 25 cubos tienen una sola voz, que sale en casi
  todos los prompts, mientras el cubo `sust` reparte una plaza entre 226.
  Preferir la atestiguada encima de ese reparto añadiría un sesgo sobre otro
  sesgo, y los dos quedarían dentro del mismo número.

Si aun así quieres tocarlo, la versión barata y medible es **desempatar sólo
dentro del par**: cuando las dos formas de un par caigan en la misma muestra,
que salga la atestiguada. Eso no cambia el presupuesto de voces ni la longitud
del prompt (r = −0,48), y se puede medir con el mismo ensayo de 1.260 prompts.

---

## 8. Cómo responder

Una línea por decisión, como en `mundo-era2-sitios-y-clima.md` §6:

```
1 A · 2 B · 3 B · … · 19 C
a: biro-bana   (o: se queda · otra raíz)
b: no · sí · sólo desempate dentro del par
```

---

## Deudas abiertas que deja la medición

- **13 de los 19 pares son bugs de curación, no decisiones**: `cat` equivocada
  (`wasima`, `barbache`, `jusual`), glosa demasiado ancha (`bagre`, `igi`,
  `apana`), deuda ya declarada (`dare`). Cerrarlos hace que el criterio laxo
  baje de 19 a ~6 y que la próxima medición no vuelva a traerlos.
- **`harifuche` / `arifuke`** es la única fusión de D5 que queda viva: dos
  preparaciones de maíz con el mismo esqueleto, una en Zavala #153 y otra en
  Medina Colina 2013 p. 31. Barata y no la pide nadie todavía.
- **`kasi` y `kashi` colisionan** bajo la fonemización del proyecto. Sea cual
  sea la respuesta a la decisión 1, la colisión existe y conviene que esté
  escrita en las dos entradas.
- **El corte del 2026-09-18 cerró la puerta a la FORMA, no al MOLDE.**
  `kali-bana` ya no se registra, pero `kali-mara-bana` sí. Si eso es lo que se
  quería, está bien; si no, es otra decisión.
- **El reparto por cubos del muestreador** (12 cubos de una voz sobre 25) hace
  que la exposición de una voz dependa de en qué `categoria` la pusieron. No es
  de este issue, pero contamina cualquier medición de exposición futura.
- **Seis entradas escriben `notas` dos veces**, y Python se queda en silencio
  con la última: `maure`, `saruro`, `curiana`, `bana`, `ma`, `ana` (medido con
  `ast` sobre el fuente). En `bana` la nota que se pierde es la que lleva **D9
  y la cita de Zavala #26**, que es en lo que se apoya la sección de morfología
  del `CLAUDE.md`. Es regla 8 y va aparte de este issue: las citas que se leen
  arriba son las que sobreviven.
