# La prueba lingüística del contacto: cómo se distingue un préstamo de un cognado

Miguel, la noche del 2026-09-21:

> «Yo creo que tiene que haber una forma de probar si hubo algún tipo de
> contacto… Y diao y daitiao que son símiles son las versiones caquetías de la
> versión Taína. Un cognado que hace match.»

Y a la mañana siguiente: «Ve avanzando con la búsqueda, descarga y minado de
fuentes para corroborar pre contacto con Taíno y minar más info.»

**Sí hay una forma. Está construida, controlada y aplicada.** Esto es una
MEDICIÓN: no se tocó `curiana_lexicon.py`, ni `lexicon_*.py`, ni `2-lengua/`,
ni `3-mundo/corpus/`, ni `cognados.yaml` (regla 5). Ninguna cifra de aquí abajo
está escrita a mano: las imprime el script.

| archivo | qué tiene |
|---|---|
| `6-fusion/scripts/cruce_taino_caquetio.py` | el instrumento. `--check` dice si el YAML está al día |
| `6-fusion/cruce_taino_caquetio_2026-09-22.yaml` | el cruce entero + el test + sus controles (generado) |
| `6-fusion/cruce_taino_caquetio_2026-09-21.yaml` | la medición de ayer. **No se tocó**: el script la lee para el antes/después |

---

## 0. Lo que del encargo resultó FALSO al medirlo

1. **`datihao` NO está atestiguada a las dos orillas en nada que el repo pueda
   leer.** El encargo decía «Oviedo, San Juan tomo I p. 473 … y "los indios de
   la Provincia de Venezuela", otro tomo». Barrido el tomo I entero
   (3.001.703 caracteres, pymupdf en modo reparación): **una sola** ocurrencia
   de la familia, `dalihao`, impresa 473, en boca del cacique **Agueybana de
   San Juan**. `tiao`, `guatiao`, `guaitiao`, `diao` y `borat*` dan **cero** en
   el volumen. Y `Oviedo_Banhos_Conquista_Poblacion_Venezuela.pdf`, que por el
   nombre parecía la candidata, es de **otro autor** (José de Oviedo y Baños,
   1723) y da cero en las seis grafías (1.195.750 caracteres barridos hoy).
   **La comparación letra a letra que el encargo pide no se puede hacer: no hay
   dos cadenas, hay una.** Y esa una es lectura de OCR sin imagen (impresa
   473 > 154), justo con la confusión `l`/`t` en el sitio de la duda.

2. **Pero la otra orilla no está en el tomo IV: está en el tomo II, y la página
   la tenemos en casa desde siempre.** Esto es lo más importante que encontré,
   y contradice tanto al encargo como a la ficha de la fuente. Barrido
   **Arcaya 1920**, que el repo ya tiene en PDF (348 pp., 469.953 caracteres):
   en su p. impresa 48, nota **(33)**, cita literalmente *«Oviedo y Valdez.—
   Historia general y natural de las Indias, **tomo 2, pág. 299**»*; en la
   p. 115 nota (22), *«tomo II, pág. 297»*; en la p. 116 nota (23), *«pág. 300»*
   (el funeral del díao). **Jahn mandaba a un apéndice del tomo IV que no
   existe; Arcaya lleva cien años dando tomo y página del tomo II.** Y lo que
   hay allí es **`diao`**, no `datihao`: Arcaya copia la glosa del propio
   Oviedo, «señor principal que tiene muchos indios y le son subjetos otros
   caciques».

3. **`diao` SÍ tiene una segunda fuente independiente, y tampoco lo sabíamos.**
   Arcaya p. 48: los caquetíos de Coro llamaban «díaos» a sus caciques
   principales, *«nombre idéntico al de **tiaos**»* con que se designaba —según
   el **Padre Carvajal**, nota (34): *«Relación del descubrimiento del Río
   Apure. Pág. 317»*— a los **caquetíos de Apure**. Eso **no pasa por Oviedo ni
   por Oliver**. Y el corpus lo llevaba escrito: `creencia-001b` dice «el díao
   (diao; tiao entre los caquetíos de Apure)». El dato estaba; lo que no estaba
   era la lectura. **Ver §4.5, porque toca D11.**

4. **Los dos lados caquetíos de la familia `-tiao` citan la misma página.**
   `datihao` y `waitiao` llevan los dos «Oliver 1989 cap. 2 p. 147, sobre
   Oviedo y Valdés». No son dos atestaciones: son una obra leída por un autor.
   Y **`datihao`, `daitiao` y `guaitiao` dan CERO en Arcaya**, que lee a Oviedo
   con lupa y le cita tomo, página y nota. Eso no la desmiente; sí confirma que
   el lado caquetío de `datihao` es la lectura de un solo autor.

5. **`ni-` de `nitaíno` sigue sin ser prefijo** —Brinton p. 14 lo desmiente, ya
   estaba en el issue de ayer—, y añado la medición del otro lado: **en taíno
   no existe ningún `diao` ni `-tiao` con valor de rango**. Ver §4.3.

6. **La predicción P7 la escribí DESPUÉS y lo digo.** Las seis primeras
   correspondencias están escritas antes de mirar ninguna pareja. La séptima
   (`caq /k/ ~ /s/`) la **exigió el control**: `koke` ~ `kuse` 'bachaco', que
   Oliver sostiene con página, salía «préstamo». El hueco era de mi tabla, no
   del par. Queda declarada como añadida hoy y **con dos apoyos, por debajo del
   listón de tres del propio proyecto**, así que no decide nada por sí sola.

7. Una del método, no del encargo: **la tabla de correspondencias es de un PAR
   de lenguas, no universal.** La `/r/` distingue caquetío de taíno y **no**
   distingue caquetío de lokono. Aplicar la tabla equivocada fue lo que hizo
   fallar el control la primera vez.

---

## 1. El test, en una página

Un cognado heredado y un préstamo por contacto **dejan huellas distintas**:

- Un **cognado** ha vivido en las dos lenguas desde que se separaron, así que
  sufrió los cambios de sonido de cada una. Se parece, pero **difiere
  exactamente donde una correspondencia regular manda que difiera**.
- Un **préstamo** cruzó después, así que llega casi intacto: **no exhibe la
  diferencia que tocaba**. O trae sonidos que la cadena no produce, y entonces
  la viola. O cae en un campo donde las palabras viajan (alianza, rango,
  comercio, prestigio).
- Y un préstamo **prueba contacto**; un cognado **prueba parentesco**. No son
  la misma pregunta.

El test corre sobre **esqueletos consonánticos**, porque Oliver excluye las
vocales de su propio método (C9), y trata `/r/ ~ /l/` como indecidible (C8).
Lee `⟨gu⟩` como `/w/`, que es lo que hace visible `bagua` = /bawa/.

Devuelve una **letra**:

| | qué significa |
|---|---|
| **A** | cognado heredado: cumple al menos una correspondencia regular |
| **B** | préstamo o cruce reciente: viola una correspondencia, **o** no exhibe ninguna diferencia donde una consonante diagnóstica mandaba cambiar |
| **C** | indecidible **con una razón concreta**, casi siempre ésta: la palabra no tiene ninguna consonante diagnóstica, o sea **no tiene dónde diferir** |

La pieza clave es **«consonante diagnóstica»**: aquella para la que lo predicho
**no** es la identidad. Sin una de ésas, dos formas idénticas no prueban nada,
por mucho que se parezcan. **Entre caquetío y taíno sólo `/r/` es diagnóstica.
Entre caquetío y lokono, ninguna.**

---

## 2. Las predicciones, escritas antes

Nadie ha publicado correspondencias caquetío↔taíno. Lo que sí existe son dos
patas, y se pueden **componer**:

- **pata A** caquetío ↔ lokono — Oliver 1989 cap. 2, C1-C13, con página
- **pata B** taíno ↔ lokono — Brinton 1871 pp. 11-14, recogidas ayer por T2 en
  `taino_brinton_1871.yaml §correspondencias_para_T4`

| | predicción | de dónde | ¿diagnóstica? |
|---|---|---|---|
| **P1** | caq `/r/` ~ taí **∅ o `/w/`** | el caq conserva la /r/ lokona (`dare`:`d-ari`, `barisi`:`bálisi`, `para`:`bara`); el taí la pierde (`maisi`:`marisi`, `cai`:`kairi`, `bagua`:`bara`) | **SÍ**, 3 apoyos |
| **P2** | caq `/b/` ~ taí `/b/` | C3: LK /b/ : WY /p/, y el caquetío cae del lado lokono | no: identidad esperada |
| **P2b** | caq `/p/` ~ taí `/b/` | la excepción de `para`:`bara` que Oliver deja sin explicar (p. 150) | no: 1 apoyo |
| **P3** | caq `/d-/` ~ taí `/d-/` | C1, el pilar de D11 | **no, y ése es el punto** — ver abajo |
| **P4** | caq `/t/` ~ taí `/t/` | C4b (`kaketío`:`kakïtho`) | no: `fonemizar` colapsa ⟨th⟩ antes del test |
| **P6** | **la firma del préstamo**: cero diferencia donde una diagnóstica mandaba cambiar | Oliver mide 2,6-3,8 milenios entre hermanas: a esa distancia da tiempo | — |
| **P7** | caq `/k/` ~ taí `/s/` | *(añadida hoy, la exigió el control)* `koke`:`kuse` + `siba`:`siba` | no: **2 apoyos, bajo el listón** |

> **P3 es la que contesta la pregunta de Miguel sobre `da-`.** La transitividad
> predice que un cognado caquetío de taíno `da-` + `-(i)tiao` se dice
> **`da-tiao`** — y eso es exactamente lo que hay. **Pero no decide nada**: el
> `/d-/` separa al trío caquetío-taíno-lokono del par guajiro-paraujano
> (`/tA-/`), no al caquetío del taíno. Un préstamo taíno habría entrado con su
> `/d-/` intacto. Es dato de filiación, ya contado por D11.

**P1 puesta a prueba sobre el corpus entero** (tasa de `/r/` sobre el total de
consonantes de cada lista) — y aquí hay un **resultado incómodo que hay que
decir**:

```
caquetío-atestiguado  0,2048      taíno       0,0702
achagua               0,1239      lokono      0,0776
kalinago              0,1373      wayunaiki   0,0776
paraujano             0,0980      jirajarano  0,0868  (control)
```

P1 se cumple **pareja a pareja** (tres casos con cita), pero **la tasa global
no la corrobora**: el lokono tiene casi la misma tasa que el taíno. El que se
sale de la fila es el **caquetío**, casi tres veces por encima del taíno — y
eso puede ser el sesgo de su lista (fitonimia de Zavala) antes que un rasgo de
la lengua. La predicción se sostiene en tres parejas, no en el corpus.

---

## 3. El control: el test clasifica bien lo que ya sabemos

Obligatorio. Si no separa lo conocido, no sirve para lo desconocido.

```
a) HEREDADAS  caquetío↔lokono con cita de Oliver   n=10   {C:10}   fallos 0
b) PRESTADAS  taíno→castellano (Brinton lo dice)   n=18   {B:2, C:16}   fallos 0
c) NO PARIENTE caquetío↔jirajarano (Jahn 1927)     n=12   {B:6, C:6}   fallos 0
```

**Veredicto: el test es SANO.** Ninguna heredada sale préstamo, ninguna
prestada sale herencia, ninguna pareja con la lengua no pariente sale herencia.

**Y es débil, y eso también es el resultado**: *decide* 0 de 10 heredadas y
2 de 18 prestadas. El resto queda en C **por falta de consonante diagnóstica**.
Con el material de hoy el test dice «no sé» mucho más que «sí» o «no» — pero
cuando dice algo, no se equivoca en lo que ya sabíamos.

---

## 4. Lo que dio con el material de hoy

### 4.1 El cruce, re-corrido con las transcripciones de T1/T2

El cruce de ayer leía **sólo las 43 voces taínas del lexicón, que no citan a
nadie**. Hoy lee además Oviedo, Las Casas, Pané y Brinton, que sí traen obra y
página:

```
                  2026-09-21              2026-09-22
taíno       ent   39 · cmp  4 · par 0  →  ent 141 · cmp 20 · par 2 · cognado-probable 1 · p=0,117
lokono      ent  638 · cmp 43 · par 5  →  igual (p=0,007)
wayunaiki   ent  769 · cmp 36 · par 3  →  igual (p=0,007)
achagua     ent 3568 · cmp 70 · par 1  →  igual (p=0,500)
jirajarano  ent   83 · cmp 12 · par 0  →  igual (p=1,000)   ← control
```

De las 141 voces taínas, **112 llevan obra y página**; 29 siguen sin clave
foránea (son las del lexicón que nadie ha citado todavía).

**El cero de ayer era de la lista, y se levantó en parte.** Los conceptos
comparables pasan de **4 a 20** y aparecen **las dos parejas que el issue de
ayer decía que el cruce no podía ver**:

| pareja | sim | letra | por qué |
|---|---:|:--:|---|
| caq `parawa` 'mar' ~ taí `bagua` (Brinton p. 11) | 0,667 | **A** | cumple `p~b` (P2b) **y** `r~∅` (P1, 3 apoyos) |
| caq `kiba` 'piedra' (f. fuente `quiva`) ~ taí `siba` (Brinton p. 13) | 0,750 | **C** | la cubriría `k~s`, pero son 2 apoyos y uno es esta misma pareja: sería circular |

⚠️ **Pero el taíno sigue sin ganarle al azar**: `p = 0,117` para 2 parecidos
donde el modelo nulo da 0,69. Con 20 conceptos comparables no hay potencia. El
**lokono** sí gana (`p = 0,007`), que es lo que Oliver sostiene y D11 ya tiene.
El **jirajarano no arahuaco** sigue en cero.

Y el paso **por forma sin filtro de glosa** sigue siendo ruido puro: 36 parejas
taínas sobre el umbral, **0 con la glosa también**.

### 4.2 `datihao` — el caso de prueba

Aplicado el test a lo que hay:

| pareja | esqueletos | letra |
|---|---|:--:|
| caq `datihao` ~ taí `guatiao` | `dt ~ wt` | **C** |
| caq `guaitiao` (= la `forma_fuente` de `waitiao`) ~ taí `guatiao` | `wt ~ wt` | **C** |
| caq `datihao` ~ el `dalihao` del OCR de Oviedo | `dt ~ dl` | **no se aplica** |

- La primera sale C porque **la diferencia inicial `d~w` no es sonido, es
  morfología**: 1ª sg. `/dA-/` frente a 3ª pl. `/wa- [gua-]/`, que es lo que
  Oliver escribe en la p. 147. Quitado el prefijo, **las dos raíces son
  idénticas** (`/t/`) y `/t/` no es diagnóstica.
- La segunda sale C por lo mismo, sin ni siquiera el prefijo de por medio: las
  dos formas son la misma palabra, letra a letra.
- La tercera **no se mete en el test**: `t~l` es la confusión del OCR en una
  cursiva de una página sin imagen. Meterla sería medir al escáner.

**Las dos lecturas, con su peso:**

- **(A) cognado heredado — peso medio.** Oliver lo escribe («This Taíno term is
  cognate to Caquetio daitiao», p. 147) y le da etimología en proto-arahuaco:
  `/da-/` + `/-(i)tiao/` sobre la raíz de parentesco `/atti/`, con el lokono
  `da-tti`/`da-iti` y el `ahati` 'companion, playmate' que Brinton da (p. 12).
  Vocabulario de parentesco, del que casi nunca viaja. **En contra**: la
  evidencia formal es **nula**, y no puede no serlo.
- **(B) préstamo por contacto — peso medio-alto.** El campo. `guatiao` no es
  parentesco a secas: es el nombre de una **institución de alianza entre
  señores** —el trueque de nombres entre Ponce de León y Agüeybaná, Las Casas
  II:291— y las instituciones de alianza viajan con los aliados. Oviedo la oye
  en boca de un cacique de Boriquén hablando con españoles. Y **el propio
  Oliver duda de su dato**: «I have no absolute certainty that it belongs to a
  Caquetío language… He could very well have used Taíno», y concluye «equally
  shared by both Taíno and Caquetío» (n. 42, p. 146).
- **(C) indecidible — peso ALTO, y es el veredicto del instrumento.** No por
  prudencia: **por una razón concreta**. La palabra no tiene consonante
  diagnóstica; falta la mitad del dato; y la mitad que hay es OCR sin imagen.

**El test queda escrito para cuando llegue la forma que falta**
(`meta.el_caso_datihao.el_test_que_queda_escrito_para_cuando_llegue_el_dato`),
para que no se decida después de verla:

| si la forma de Venezuela es… | entonces | por qué |
|---|---|---|
| **idéntica** letra a letra a la de San Juan | **B se refuerza mucho** | un cronista con veinte años en La Española escribiendo la misma cadena en las dos orillas es indistinguible de uno que proyecta — el escenario que Oliver teme |
| `datihao` frente a `guatiao`, o sea difiere **sólo en el prefijo** | **sigue siendo C** | es lo que ya hay: morfología compartida, no correspondencia de sonido |
| con **`/r/`** donde el taíno no la tiene (*`daritiao`) | **A, y fuerte** | sería P1 cumpliéndose en la voz misma |
| con **`/t-/`** inicial (*`tatihao`) | **A por vía guajiro-paraujana**, y falsaría P3 | sería dato contra la tesis lokonoide de Oliver |
| **otra palabra distinta** para lo mismo | **B se refuerza** | si el caquetío tiene voz propia para el aliado ritual, la `-tiao` es la importada |
| aparece una atestación caquetía de `-tiao` **que no venga de Oviedo** | **cambia el fondo entero** | las dos entradas del lexicón citan la misma página de Oliver sobre el mismo Oviedo. **Para `datihao` sigue sin aparecer; para `diao` sí apareció** — ver §4.5 |

### 4.3 `diao` — medido, sin forzar el match ni negarlo

**La frase de Miguel se parte en dos y las dos mitades miden distinto.**

- **`datihao` SÍ tiene gemela taína**: `guatiao` 'friend, companion'
  (brinton-1871 p. 12, cronista Richardo; lokono `ahati`). Misma raíz, distinto
  prefijo de persona. Es la que el test no puede decidir (§4.2).
- **`diao` NO tiene gemela taína ninguna.** Barrida toda la lista taína del
  cruce (141 voces) y los lemas de Brinton pp. 11-14: **no hay ningún `diao`
  ni ningún `dia-`**. Y el campo de rango entero, lado a lado:

  | caquetío atestiguado (5) | taíno (11) |
  |---|---|
  | `manaure`, `diao`, `apopo`, `boratio`, `waitiao` | `bajari`, `bejique`, `caçique`, `guatiao`, `matum`, `matunheri`, `naboria`, `naborias`, `nitaino`, `nitainos`, `taita` |

  Dos parejas pasan el umbral en todo el campo: `waitiao ~ guatiao` (0,92, **C**)
  y `waitiao ~ taita` (0,67, **B** — el test la rechaza por violación, que es lo
  que tenía que hacer con el ruido). **`diao` no aparece en ninguna.**

**Qué comparten `diao` y `datihao` con precisión** (y en esto Oliver ya estaba
escrito en `4-fuentes/oliver-1989-cap2.md`, «el nudo», y no se había leído
despacio):

- el prefijo `/d-/` de 1ª sg. — que comparten también con el lokono y el taíno,
  así que **no es un lazo entre estas dos palabras**;
- el sufijo `/-(h)o/` nominalizador solemne, que también lleva `boratio`.

**Qué NO comparten:**

- **la raíz**: `/-ai-/` 'palabra, lengua' contra `/-atti-/` 'pariente'. Dos
  etimologías distintas, del mismo autor, en dos páginas seguidas;
- **la glosa**: 'señor principal, jefe mayor' (Zavala p. 67, por vía caquetía
  propia) contra 'padrino de cautivo, el que presta su nombre'. Rango contra
  alianza. Bajo la política del 2026-09-19 —glosa normalizada idéntica o no hay
  par— no son el mismo concepto ni de lejos.

**La pareja que `diao` sí tiene es LOKONA** (`dai-yana-ho`, cognado-008, Oliver
p. 146). Y ésa es dato de filiación, la columna de D11, no la del contacto.

### 4.5 Y lo que de verdad apareció: `díao` (Coro) frente a `tiao` (Apure)

Esto no lo pedía el encargo y es, creo, el hallazgo de la parcela. Bloque
entero en `meta.la_otra_orilla_estaba_en_casa`.

Arcaya 1920, p. impresa 48, dice que los caquetíos de **Coro** llamaban
**`díaos`** a sus caciques principales y que es *«nombre idéntico al de
`tiaos`»* con que se designaba a los caquetíos de **Apure**, según el Padre
Carvajal (*Relación del descubrimiento del Río Apure*, p. 317).

**`díao` ~ `tiao` es un contraste `/d-/ ~ /t-/ dentro del caquetío`, entre dos
polities.** Y `/d-/` frente a `/t-/` es **exactamente la C1 de Oliver**: el
prefijo de 1ª sg. que sólo lokono y taíno conservan como `/dA-/`, mientras el
guajiro-paraujano innova `/tA-/`. Es el pilar del que cuelga la tesis
lokonoide del caquetío, y con ella **D11**.

Dos lecturas, y no las decido yo:

- **el contraste es real y es dialectal** → «el caquetío conserva `/d-/`» pasa a
  ser una afirmación sobre el caquetío **costero**, no sobre el caquetío. El de
  Apure caería del lado de la innovación `/tA-/`. Sería la **regla 4 mordiendo
  en la fonología**, que es donde nadie la había mirado.
- **el contraste es de copista** → Carvajal oyó o escribió sin la `/d-/`, o
  Arcaya normalizó. Una ocurrencia en un texto de 1648 que no tenemos no
  sostiene un dialecto.

**Qué lo decidiría**: la p. 317 de Carvajal. No está en el repo, es del s. XVII
y es de dominio público. Es la misma clase de dato que falta para `datihao`:
una página.

⚠️ Y el aviso que va delante de la alegría: **`tiao` es de Apure**, y la
regla 4 dice que importar un rasgo de los Llanos sin marcarlo es el error que
Oliver denuncia. Se anota como dato de la esfera caquetía ancha, no de la
polity costera que la simulación modela.

### 4.6 El acento: un tercer eje que llega con el PR #194

La parcela de la *Apologética* cerró mientras yo medía y deja tres datos que
tocan este test. Bloque en `meta.el_eje_prosodico_que_viene`. **No los lee el
script** —ese YAML está en el PR #194, no en `main`, y si lo leyera `--check`
fallaría para quien no tenga esa rama—: van declarados con su cita.

1. **`guatiao` = 0 en toda la *Apologética***, y la institución del cambio de
   nombre **sí** está descrita allí. Las Casas cuenta el rito y no usa la
   palabra. Súmese a que el `Guatiao` de Brinton no viene de un cronista sino
   de **Richardo, *Diccionario provincial*** — obra cubana del **siglo XIX**.
   **Las dos orillas del caso son finas**, no sólo la caquetía.
2. **`daca` 'yo' confirmado también allí**, además de Pané cap. XXV. P3 gana un
   apoyo independiente — y sigue sin distinguir herencia de préstamo, que es lo
   que P3 ya declaraba.
3. **Las Casas marca el acento de 97 formas taínas**, y eso da un eje nuevo: el
   acento de una forma heredada debería seguir un patrón; el de un préstamo no
   tiene por qué. **Y ya dice algo sin necesidad de ejecutarlo**: los tres
   títulos de rango taínos que Las Casas acentúa son **oxítonos y acaban los
   tres en `-í` tónica** — `Guaoxerí` «la última sílaba luenga», `Baharí` «la
   misma última luenga», `Matunherí` «el acento en la postrera sílaba». No son
   tres palabras sueltas: **son una serie**. El taíno hace títulos con un molde
   `raíz + -í tónica`, y `diao` no lo tiene ni de forma ni de acento. Es una
   **segunda razón, independiente de la forma**, para que `diao` no tenga
   gemela taína.

⚠️ El límite: **el acento del caquetío no está medido en ninguna parte**. La
tilde de `díao` es editorial (Arcaya 1920), no marca de cronista. El eje sirve
hoy para describir el taíno y todavía no para comparar. Lo que lo cerraría es
una fuente que marque acento en caquetío.

### 4.7 Los morfemas compartidos van en la columna de FILIACIÓN

Un morfema gramatical compartido no prueba que dos pueblos se hablaran: prueba
que vienen del mismo sitio. Tabla entera en
`meta.morfemas_compartidos_son_filiacion_no_contacto`. En corto:

| morfema | taíno | columna |
|---|---|---|
| `ma-` privativo | `mahite`, Brinton p. 14 (✓ está en las transcripciones) | filiación, y **ni siquiera taíno-caquetía**: Oliver p. 147 n. 43 lo declara común a las **maipures** |
| `da-` 1ª sg. | `daca` 'yo', Pané cap. XXV | filiación, y es el pilar de D11 |
| `-(h)o` nominalizador | Oliver p. 147, «characteristic of both Taíno and Lokono» | filiación |
| `gua-`/`wa-` 3ª pl. | Brinton p. 12 | filiación — ojo, el `-gua` **locativo** del canon es otra cosa |
| `-caco` 'ojos' | `buticaco`, `xeyticaco`, Brinton p. 14 | **ninguna**: es hueco caquetío, no pareja |

> **Ninguno de estos morfemas prueba contacto.** Lo que probaría contacto es
> léxico: una voz que viajó. Y para eso hace falta el test, no el inventario de
> afijos.

---

## 5. El veredicto provisional

**Hay una forma de probarlo, está construida y pasa sus controles; con el
material de hoy prueba PARENTESCO y no prueba CONTACTO — y el caso que Miguel
señaló, `datihao`, sale indecidible por una razón precisa (la palabra no tiene
dónde diferir), mientras que la otra mitad de su frase, `diao`, no tiene gemela
taína que buscar.**

| | letra | |
|---|:--:|---|
| `datihao` / `daitiao` ~ taíno `guatiao` | **C** | con B pesando más que A por el campo (alianza entre señores) y por la duda del propio Oliver. Y hoy sabemos que **las dos orillas del caso son finas**: `guatiao` = 0 en la *Apologética* y el de Brinton viene de un diccionario cubano del XIX |
| `diao` ~ ¿taíno? | **no aplica** | no hay candidato taíno, ni por forma ni por acento. Su pareja es lokona, y es filiación |
| caq `parawa` ~ taí `bagua` 'mar' | **A** | la única A del cruce, y cumple dos correspondencias |
| caq `kiba` ~ taí `siba` 'piedra' | **C** | la cerraría un tercer apoyo independiente de `k~s` |
| caq `díao` (Coro) ~ caq `tiao` (Apure) | **fuera del test** | no es caquetío↔taíno: es caquetío↔caquetío, y toca C1 y D11. §4.5 |

---

## 6. Lo que NO encontré

- **La página de Oviedo tomo II p. 299.** Localizada, no leída: el repo no
  tiene el tomo II. Es el dato que decide el caso, y ahora se sabe dónde está.
- **La p. 317 de Carvajal**, que decidiría si el `tiao` de Apure es dialecto o
  copista. Tampoco está en el repo, y es del s. XVII y de dominio público.
- **`datihao` en ninguna fuente que no sea Oliver.** Cero en Arcaya (348 pp.),
  cero en la *Apologética*, cero en Las Casas tomo I, cero en Pané, cero en
  Brinton.
- **Ninguna correspondencia caquetío↔taíno con tres apoyos propios.** La única
  que llega al listón (P1) llega **por composición**, no por parejas
  caquetío-taíno observadas.
- **Ningún `diao`, `dia-` ni `-tiao` de rango en taíno.** Cero verificado sobre
  las 141 voces del cruce y los lemas de Brinton pp. 11-14.
- **Corroboración de P1 en el corpus.** Pareja a pareja sí; en la tasa global
  de `/r/`, no.
- **Significación del taíno.** `p = 0,117`: las 2 parejas no le ganan al azar.

---

## 7. Las opciones, para Miguel

### La decisión de fondo: ¿qué se hace con este test?

- **(A) El test se queda como instrumento de campaña, en `6-fusion/`, y se
  vuelve a correr cuando entren fuentes.**
  *Coste*: ninguno. *Lo que se gana*: cada fuente nueva actualiza las letras
  sola, y `--check` avisa si el YAML se desfasa. *Lo que no se gana*: el canon
  no cambia, `cognados.yaml` sigue con sus 16 sets CQ~TN sin auditar.

- **(B) El test se aplica a `cognados.yaml` entero y cada set recibe su letra.**
  *Coste*: una sesión. *Lo que se gana*: los 51 sets dejarían de ser una lista
  plana y pasarían a decir si son herencia, préstamo o indecidible — y los
  cuatro «la misma palabra escrita dos veces» que el issue de ayer encontró
  quedarían clasificados con criterio y no a ojo. *El riesgo*: es un cambio de
  canon de datos de lengua, y **esta campaña sólo propone**.

- **(C) El test se lleva al motor como capa de `score_linguistico()`.**
  *Coste*: rompe la serie, y el instrumento no está para eso. **No lo
  recomiendo** y lo escribo para que la opción quede descartada por escrito.

### La decisión sobre `datihao`, que es de etiqueta

- **(D) `datihao` se queda como `caquetío-atestiguado`, como está hoy.**
  *A favor*: Oliver la declara cognada y la etiqueta refleja la mejor fuente.
  *En contra*: el propio Oliver duda de que sea caquetía, y el lexicón **no
  lleva esa reserva escrita**.

- **(E) `datihao` conserva la etiqueta y se le añade la reserva de Oliver en
  `notas`, con la cita de la n. 42.** Sin cambiar de capa: la etiqueta dice de
  dónde viene la palabra y la nota dice qué duda su fuente. Es un cambio de una
  línea en `curiana_lexicon.py` y lo tiene que hacer un fusionador, no yo.

- **(F) `datihao` se degrada.** En duda, degradar (regla 2). *En contra*: la
  duda no es sobre la forma —Oviedo la imprime— sino sobre **de quién es la
  boca**, y para eso el proyecto tiene la regla 4 y no la escala de capas.

### La que abre el hallazgo de Arcaya

- **(G) `díao` (Coro) ~ `tiao` (Apure) se anota como pregunta abierta sobre
  C1 y D11**, con la cita de Arcaya p. 48 y la de Carvajal p. 317, y **no se
  toca nada**. Es el contraste `/d-/ ~ /t-/` dentro del caquetío, entre dos
  polities, y `/d-/` es el pilar de la tesis lokonoide. *Lo que se gana*: que
  quede escrito antes de que alguien cite «el caquetío conserva /d-/» como si
  fuera de toda la nación caquetía. *Lo que cuesta*: nada hoy; una fuente
  (Carvajal) mañana.

- **(H) Además de anotarla, se le pide a alguien la p. 317 de Carvajal y el
  tomo II de Oviedo.** Son dos páginas y cierran dos casos: el de `tiao` y el
  de `datihao`. **No es una decisión: es un encargo**, y es lo único de toda
  esta lista que mueve la aguja de verdad.

### Y dos que no son opcionales

- **(I) `creencia-001` (`boratio`) cita «Oviedo y Valdés, Historia general,
  apéndice t. IV (en Jahn 1927:213 n.29)» — un apéndice que no existe.** Y
  Arcaya, que el repo tiene, da la cita buena por otra vía: **tomo II** y
  15 apariciones de `boratio` con la descripción entera del oficio
  (pp. impresas 98-100). La referencia se puede arreglar sin depender de nada
  nuevo.
- **(J) `parentesco-012` afirma que «daitiao» es cognado del taíno.** Esta
  medición no lo desmiente, pero deja escrito que **el test no lo confirma**
  (letra C) y que la afirmación tiene una sola fuente. Si se queda, que se
  quede con la reserva; es la misma decisión que (E), en el corpus en vez de
  en el lexicón.

### Mi recomendación

**(A) + (E) + (G) + (H), y (I) de paso.** El test vale como instrumento de
campaña y no como canon: su propio control dice que decide poco, y meter en el
lexicón algo que decide 0 de 10 casos conocidos sería exactamente la enfermedad
que D11 denuncia. (E) cuesta una línea y cierra una deuda real: el lexicón
afirma hoy, sin reserva, algo de lo que su única fuente duda por escrito. (G)
es escribir un hallazgo antes de que se pierda. **(H) es lo único que mueve la
aguja**: dos páginas —Oviedo tomo II p. 299 y Carvajal p. 317— y los dos casos
se resuelven solos, porque el test ya está escrito y espera.

---

## 8. Lo que vi de paso

- **Arcaya 1920 estaba sin minar para esto y tiene 15 `boratio`** con la
  descripción entera del oficio copiada de Oviedo (pp. impresas 98-100), más
  las citas de tomo y página que el proyecto buscaba. La ficha de la fuente
  dice que se minó; para la familia `-tiao` no se había mirado.
- **`naboria` da cero en Oviedo tomo I con esa grafía, y aparece tres veces.**
  La obra escribe `naboría`, con tilde. Es un cero de consulta de manual
  (regla 6) y lo dejo escrito porque la transcripción de T1 sí la recogió — la
  trampa está en quien busque después.
- **`caquet*` da cero en el tomo I entero de Oviedo.** La palabra «caquetío» no
  aparece en el volumen.
- **El `hado`/`hayo` de Oviedo p. 206 sigue sin verificar** y es la voz más
  cercana a la Kaketiana que el tomo I tiene («la gobernación de Venezuela»).
  Una página de otra copia lo cierra.
- **`comoho`**, el fruto del cardón «en la provinçia de Veneçuela» (Oviedo
  p. 313-314), tampoco está en el lexicón y es del cardonal que el corpus ya
  tiene medido. No es caquetío declarado —Oviedo dice la gobernación entera—
  pero es de la esfera y de la ecología correcta.
- **El extractor de glosas deja 34 voces sin glosa** de las transcripciones
  (topónimos, antropónimos y frases largas, sobre todo). El inventario entero
  sale en `insumos.transcripciones.bitacora_de_glosas` para auditarlo a ojo: si
  alguien ve una glosa recuperable, se añade a `GLOSA_DECLARADA` y el
  denominador sube.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
