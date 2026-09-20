# La morfología arahuaca, revisada entera

Miguel, 2026-09-20:

> «Echarle una revisada a toda la morfología arahuaca, para que ajustemos;
> quiero que tengamos la morfología bien clara.»

Esto es lo que salió. Un medidor, una medición y este resumen:

| archivo | qué tiene |
|---|---|
| `6-fusion/scripts/auditar_morfologia.py` | el medidor: inventario, uso sobre `word_uses`, combinaciones no declaradas, el aspecto rama a rama y las sondas del contraste |
| `6-fusion/medicion_morfologia_2026-09-20.yaml` | la medición entera, morfema a morfema |
| `6-fusion/borrador_morfologia_2026-09-20.md` | cómo quedaría `2-lengua/morfologia.md` **si se aceptara todo** — borrador, NO aplicado |

**Ninguna cifra de aquí está escrita a mano.** Las imprime
`CURIANA_ELENCO=era2 PYTHONIOENCODING=utf-8 python 6-fusion/scripts/auditar_morfologia.py`.

**Nada del canon ni del motor se ha tocado** (regla 5). Este archivo propone;
fusionar es otra sesión, y las de §6 las decide Miguel una a una.

> ⚠️ **Lo que esta auditoría NO toca, por encargo**: la `cat` de ninguna
> entrada. Otra sesión está clasificando en paralelo las **49 raíces que la
> heurística de `minar_zavala_glosario.py` marcó `v_raiz`** (estativo / acción /
> nombre). Donde esta auditoría necesita esa clasificación —y la necesita en
> los puntos 2, 3 y 4— **la cita como pendiente y mide cuánto depende de
> ella**, sin adelantarla.

---

## 0. La regla de segmentación, y su control

Todo el §3 descansa en partir una forma en prefijos + núcleo + sufijos. **Esa
partición es la del motor, no un regex de esta auditoría**: se pelan por los
bordes los afijos de `_PREFIJOS_CAQ` y `_SUFIJOS_CAQ`, prefijos primero, en el
mismo orden que `curiana_lexicon.nucleo_de_token()`. Lo único que añade el
medidor es apuntar **qué** afijo peló, que el motor tira.

```
control de segmentación: 2.546 formas comprobadas · 0 desvíos contra
                         nucleo_de_token() · VERDE
```

Si el control sale en rojo el script se planta antes de medir nada.

---

## 1. El inventario

```
morfemas en el motor            21   (19 en TODAS_LAS_REGLAS + 2 retirados)
morfemas en 2-lengua/morfemas.yaml   11
morfemas propuestos sin importar     24   (lexicon_van_buurt + lexicon_gatschet)
```

Por capa epistémica, los 21 del motor:

| capa | n |
|---|---:|
| reconstruido sobre el andamio wayuu/lokono (deuda D11) | **9** |
| atestiguado (Zavala, van Buurt, Alvarado, González Batista, Velasco) | 8 |
| retirada (`-ko`, `-sha`, 2026-09-14) | 2 |
| canon-simulación (`-ana`) | 1 |
| reconstruido sin andamio declarado (`-gua`) | 1 |

Y la cifra que ordena todo lo demás:

```
con clave foránea válida a 4-fuentes/bibliografia.yaml (regla 8):  9 de 21
```

Los doce sin procedencia: `-ka` · `-ni` · `-da` · `ta-` · `wa-` · `ma-` ·
`ka-` · `-kana` · `-naiki` · `-gua` · `-ko` · `-sha`.

> **Léase despacio: los tres aspectos, los cuatro prefijos posesivos, el plural
> y el locativo `-gua` son toda la gramática viva del motor, y ninguno apunta a
> una obra.** Lo que llevan en el campo de apoyo es el cognado wayunaiki
> («-iraa (imperfective suffix)», «ma- (prefijo negativo, cognado directo)») o
> una frase sin fuente («Topónimos venezolanos de Falcón y Sucre»).
>
> Matiz que hay que decir para no exagerar: **`2-lengua/morfologia.md` §2 SÍ
> cita apoyo insular independiente para `ka-` y `wa-`** —van Buurt §8
> *Casibari* y §6 vía de Goeje 1928—. Lo que falta es que la entrada del motor
> lo lleve: hoy el campo `atestiguado` de las cuatro posesivas está vacío y el
> único texto es el cognado wayuu. La nota sabe más que el código.

---

## 2. Las cuatro patologías

El encargo pedía tres. Salió una cuarta de las otras tres, y es la que más
pesa.

### (a) El motor lo ENSEÑA y el canon no lo declara — **1**

| morfema | qué pasa |
|---|---|
| `-ana` | Capa **canon-simulación**: #109 (decisión B de Miguel, 2026-09-07) retiró la glosa 'lugar de' porque el censo de Esteves dio cero casos y el «lugar» paraguanero es `-bacoa`. **Y las dos plantillas siguen enseñando literalmente «`-ana` = lugar de X»** (`prompt_reglas_completo` y `prompt_reglas_breve`). Es el patrón exacto del `kali-bana`: el canon decide una cosa y el prompt sigue diciendo otra. |

Y un residuo del mismo tipo, medido aparte: **`-uto` aparece en el prompt sin
regla detrás**. Viene del campo `uso` de `-uco` («RAÍZ + -uco / -uto»), que
`prompt_afijos_atestiguados()` renderiza entero. No está en
`TODAS_LAS_REGLAS`, así que el desafijador no lo conoce: se enseña y no se
reconoce.

### (b) El canon lo DECLARA y el motor no lo reconoce al puntuar — **9**

Los nueve están en `2-lengua/morfemas.yaml`, que es canon de datos de lengua,
y ninguno entra en `TODAS_LAS_REGLAS`, así que **ni el desafijador de
`_familia_de_token()` ni `nucleo_de_token()` los ven**:

| morfema | glosa | estado |
|---|---|---|
| `-bacoa` | bosque, arboleda | ✅ **sí está** en el motor desde 2026-09-14 |
| `-are` | 'sitio de' (locativo) | glosado, recurrencia 5, glosa en disputa con el `-ure` de van Buurt |
| `ada-` | árbol | glosado, cognado lokono `ada` |
| `bari-` | rojizo, turbio | glosado, reagrupación |
| `yacare` | pueblo, poblado | glosado |
| `-shi / -chi` | — | **22 apariciones, el formante más frecuente del corpus insular y nadie lo ha glosado** |
| `-ari / -ri` | — | 7 apariciones |
| `-kuri / -curi` | — | 3 apariciones |
| `-bari` | — | 3 apariciones; `INDICE_FUENTES` ya concluyó que no es afijo |

Y uno que no es de `morfemas.yaml` y pesa más que todos ellos:

| **la REDUPLICACIÓN** | `2-lengua/morfologia.md` §4 la declara **medida y productiva** —9,0 % de la toponimia caquetía contra 3,1 % del control wayunaiki y 0,7 % del lokono— con valores de pluralidad/abundancia y onomatopeya. **El motor no tiene ni una regla que la produzca ni una que la reconozca.** |
|---|---|

### (c) Apoyo SÓLO en el andamio wayuu/lokono que D11 mandó retirar — **9**

`-ka` · `-ni` · `-da` · `ta-` · `wa-` · `ma-` · `ka-` · `-kana` · `-naiki`
(más `-ko` y `-sha`, ya retirados el 2026-09-14 **por exactamente esta razón**:
«sin fuente; era convención de la era 1»).

Ocho de los nueve se enseñan, y algunos en cinco plantillas a la vez. Es lo que
`6-fusion/lokono_gramatica_perea_1942.yaml` ya había anotado para D11 fase 3:
la decisión abierta «declarar la etiqueta del núcleo reconstruido» **no afecta
sólo a la Capa 2 léxica; afecta al sistema morfológico entero**.

### (d) El motor lo ENSEÑA y no hay clave foránea a la bibliografía — **9**

`-ka` · `-ni` · `-da` · `-gua` · `ta-` · `wa-` · `ma-` · `ka-` · `-kana`.

No es lo mismo que (a) —ahí el canon dice otra cosa— ni que (c) —ahí el apoyo
existe pero es el andamio—: **aquí no hay apoyo que citar.** Regla 8: lo que
no tiene fuente se declara `deuda: sin-procedencia`. Hoy no se declara; se
enseña.

### Deuda documental de las tablas (no llega al prompt, pero es lo que lee quien venga detrás)

```
1 ejemplo con forma ARCHIVADA        piache + kana = los piaches   (piache está en FUERA_DEL_HABLA desde D10)
3 ejemplos con voz de OTRA LENGUA    wayuu + kana = wayuukana · wayuu + naiki = wayuunaiki · ada + -bacoa
5 derivados que el lexicón NO TIENE  Corogua · Judibana · wayuukana · adabacoa · yacarebacoa
```

Las tres reglas que enseñan a formar plural y gentilicio lo hacen **con la
lengua que `IDENTIDAD_LINGUISTICA` declara «tan ajena para ti como el
español»**. Y el módulo ya se había escrito la nota correcta para otro caso
(`paa-ka`, 2026-09-19: «una referencia muerta aquí es deuda igual»).

---

## 3. Qué hace la gente con ellos

Medido sobre `word_uses` de toda la base:

```
95.445 usos · 2.546 formas distintas
43.756 usos en formas que llevan un afijo declarado
por era y serie:  era1 63.533 · era2/era2-c 21.038 · era2 (sin serie) 7.591 · era2/era2-b 3.283
```

### El ranking

| morfema | clase | usos | formas | raíces | categoría de la raíz (top 3) |
|---|---|---:|---:|---:|---|
| `-ni` | aspecto | 14.850 | 216 | 143 | v_raiz 13.460 · fuera-del-lexicón 1.160 · adj 111 |
| `-da` | aspecto | 8.721 | 165 | 99 | v_raiz 7.690 · fuera-del-lexicón 799 · sust 172 |
| `-ka` | aspecto | 7.442 | 130 | 90 | v_raiz 6.999 · fuera-del-lexicón 421 · sust 22 |
| `ta-` | posesivo | 6.843 | 282 | **258** | sust 5.528 · fuera-del-lexicón 574 · v_raiz 527 |
| `-bana` | locativo | 2.323 | 254 | 149 | **fuera-del-lexicón 886** · sust 515 · v_raiz 504 |
| `ma-` | posesivo | 2.195 | 190 | 175 | sust 923 · v_raiz 529 · part 272 |
| `ka-` | posesivo | 564 | 102 | 97 | sust 409 · fuera-del-lexicón 67 · título 28 |
| `wa-` | posesivo | 401 | 103 | 98 | sust 256 · fuera-del-lexicón 52 · v_raiz 51 |
| `-ana` | locativo | 290 | 77 | 53 | sust 150 · v_raiz 116 |
| `-kana` | número | 258 | 74 | 55 | **v_raiz 162** · pron 51 |
| `-iro` | derivativo | 229 | 52 | 36 | adj 74 · sust 53 |
| `-uco` | derivativo | 205 | 45 | 28 | sust 106 · fuera-del-lexicón 40 |
| `-ubana` | derivativo | 106 | 39 | 30 | sust 49 · v_raiz 41 |
| `-gua` | locativo | 102 | 49 | 37 | v_raiz 65 |
| `-aima` | derivativo | 94 | 29 | 19 | sust 52 · v_raiz 36 |
| `-ima` | derivativo | 88 | 25 | 22 | adj 38 · sust 29 |
| `-bacoa` | toponímico | 57 | 31 | 19 | v_raiz 40 |
| `-uru` | derivativo | **2** | 2 | 1 | v_raiz 2 |
| `-naiki` | número | **0** | 0 | 0 | — |

Tres lecturas:

1. **`ka-` y `ma-` juntos son 2.759 usos**, contra 6.843 de `ta-` solo. El
   mecanismo arahuaco bueno para predicar un nombre existe y se usa — pero
   `ka-` está declarado como «posesivo genérico», no como atributivo (punto 5).
2. **`-naiki` no lo ha dicho nadie nunca**, y ninguna plantilla lo enseña. Es
   un morfema que sólo vive en el desafijador.
3. **886 de los 2.323 usos de `-bana` van sobre una raíz que no está en el
   lexicón** — `lumina-bana`, `kali-bana` (archivada), `karu-bana`,
   `suave-bana`, `tension-bana`. Es el molde del corte del 2026-09-19 visto
   desde el otro lado.

### Las violaciones de slot — 13 casos, 1.778 usos

El slot sale del campo `uso` de cada regla, **no se decide aquí**: «VERBO_RAIZ
+ -ka» exige verbo, «ta- + SUSTANTIVO» exige sustantivo. Sólo se juzga cuando
la raíz está en el lexicón.

| usos | familia |
|---:|---|
| **1.132** | posesivo / atributivo sobre raíz verbal |
| **484** | aspecto sobre raíz no verbal |
| **162** | número sobre raíz verbal |

Y caso a caso:

| usos | caso | ejemplos |
|---:|---|---|
| 529 | **posesivo `ma-` sobre raíz verbal** | `ma-awa`, `ma-chaa`, `ma-bachure` |
| 527 | **posesivo `ta-` sobre raíz verbal** | `ta-chaa`, `ta-awa`, `ta-masa-da` |
| 172 | aspecto `-da` sobre sustantivo | `biro-ana-da`, `bureche-da` |
| 162 | **número `-kana` sobre raíz verbal** | `awa-kana`, `chaa-ni-kana`, `maa-da-kana` |
| 111 | aspecto `-ni` sobre **adjetivo** | `siwato-ni`, `ta-siwato-ni`, `kali-tüshi-ni` |
| 89 | aspecto `-ni` sobre partícula | `kali-mara-ni`, `kashi-bana-ni` |
| 51 | posesivo `wa-` sobre raíz verbal | `wa-jai`, `wa-awa`, `wa-duriwa` |
| 32 | aspecto `-da` sobre adjetivo | `siwato-da`, `ma-siwato-da`, `tüshi-da-uco` |
| 29 | aspecto `-ni` sobre sustantivo | `bureche-ni`, `sima-duna-ni` |
| 28 | aspecto `-da` sobre partícula | `mara-chaa-da` |
| 25 | posesivo `ka-` sobre raíz verbal | 14 formas |
| 22 | aspecto `-ka` sobre sustantivo | 3 formas |
| 1 | aspecto `-ni` sobre pronombre | 1 forma |

> ⚠️ **Estas cifras dependen de la clasificación pendiente.** `ma-awa` es
> «violación» porque `awa` 'beber' tiene `cat: v_raiz`; `siwato-ni` es
> «violación» porque `siwato` 'desganado, apático' tiene `cat: adj`. Cuando la
> otra sesión reparta las 49 raíces de Zavala en estativo / acción / nombre,
> **las dos columnas se mueven**, y la mitad de estas violaciones puede dejar
> de serlo. Por eso van aquí como lo que son: la pregunta, no el veredicto.

### Las combinaciones no declaradas — **57 patrones, 988 usos, 273 formas**

**Ninguna regla del proyecto declara apilamiento.** Los quince campos `uso` de
`TODAS_LAS_REGLAS` son de UN afijo sobre UNA raíz. Todo lo de abajo es
gramática que la comunidad produjo sin que nadie la escribiera.

Por **secuencia de clases**, que es como se cita en prosa (la categoría de la
raíz se abstrae; los totales los suma el script, no esta tabla):

| usos | formas | secuencia |
|---:|---:|---|
| 300 | 35 | RAÍZ + locativo + aspecto |
| 151 | 19 | RAÍZ + locativo + derivativo |
| 130 | 48 | **RAÍZ + aspecto + ASPECTO** |
| 114 | 35 | posesivo + RAÍZ + locativo |
| 53 | 20 | **RAÍZ + locativo + LOCATIVO** |
| 40 | 14 | posesivo + RAÍZ + derivativo |
| 39 | 4 | **RAÍZ + derivativo + DERIVATIVO** |
| 35 | 15 | posesivo + RAÍZ + aspecto |
| 20 | 4 | RAÍZ + derivativo + locativo |
| 18 | 12 | RAÍZ + aspecto + número |
| 8 | 7 | posesivo + RAÍZ + locativo + aspecto (**cuatro slots**) |
| 7 | 4 | posesivo + RAÍZ + derivativo + derivativo (**cuatro slots**) |
| 5 | 3 | RAÍZ + locativo + locativo + aspecto (**cuatro slots**) |

Y por patrón completo, con la categoría de la raíz dentro:

| usos | formas | patrón | ejemplos |
|---:|---:|---|---|
| 145 | 6 | RAÍZ[fuera-del-lexicón] + locativo + aspecto | `paa-bana-ni`, `suave-bana-ni`, `karu-bana-ni` |
| 121 | 42 | **RAÍZ[v_raiz] + aspecto + ASPECTO** | `chaa-da-ka`, `chaa-ni-da`, `jai-ni-da` |
| 88 | 2 | RAÍZ[sust] + locativo + aspecto | `biro-ana-da`, `nii-bana-da` |
| 76 | 3 | **RAÍZ[adj] + locativo + derivativo** | `kasuta-bana-iro`, `siwato-bana-uco` |
| 67 | 17 | posesivo + RAÍZ[sust] + locativo | `ka-biro-ana`, `ma-arua-bana` |
| 60 | 5 | RAÍZ[fuera-del-lexicón] + locativo + derivativo | `lumina-bana-iro`, `lumina-bana-uco` |
| 53 | 25 | RAÍZ[v_raiz] + locativo + aspecto | `chaa-bana-ni`, `juri-bana-ni` |
| 42 | 18 | **RAÍZ[v_raiz] + locativo + LOCATIVO** | `awa-bana-gua`, `kapu-bana-gua`, `kono-ana-gua` |
| 38 | 12 | posesivo + RAÍZ[sust] + derivativo | `ka-barsure-ima`, `ma-biro-uco` |
| 38 | 11 | posesivo + RAÍZ[fuera-del-lexicón] + locativo | `ta-kali-bana`, `ma-tension-bana` |
| 35 | 2 | **RAÍZ[sust] + derivativo + DERIVATIVO** | `biro-uco-aima`, `kati-iro-ubana` |
| 17 | 11 | RAÍZ[v_raiz] + aspecto + número | `maa-ni-kana`, `masa-da-kana` |
| 13 | 12 | RAÍZ[v_raiz] + derivativo + aspecto | `juri-aima-ni`, `awa-iro-ni` |
| 7 | 4 | **posesivo + RAÍZ + derivativo + DERIVATIVO** (cuatro slots) | `ka-biro-uco-aima`, `wa-biro-uco-aima` |

**Esta lista es media auditoría, y hay que leerla al derecho.** No es ruido:
es el sistema que los agentes construyeron para cubrir lo que el nuestro no
les da.

- **`chaa-ni-da`, `jai-ni-da`** — dos aspectos apilados, 130 usos en 48 formas.
  En un sistema de tres marcas sin orden declarado, eso es lo que pasa.
- **`awa-bana-gua`, `kono-ana-gua`** — dos locativos, 53 usos. Y tiene una
  lectura buena: `-gua` está declarado como «menos específico que `-ana`», o
  sea que los agentes están componiendo **lugar dentro de región**, que es
  exactamente lo que la jerarquía declarada invita a hacer y nadie autorizó.
- **`ta-chaa` «mi hacer», `ta-masa-da`, `ma-awa`** — **1.132 usos** de prefijo
  posesivo o atributivo sobre raíz verbal. **Eso es una nominalización**, y el
  sistema no tiene nominalizador (punto 11).
- **`siwato-ni` «está desganado», `tüshi-da`, `ma-siwato-ni`** — aspecto sobre
  raíz no verbal, **484 usos**, de los que 143 son sobre adjetivo (111 con
  `-ni` + 32 con `-da`). **Eso es un verbo estativo**, y el sistema no tiene la
  clase (punto 4).
- **`ka-biro-uco-aima`** — prefijo + raíz + dos derivativos. La comunidad
  construyó una palabra de cuatro slots con un sistema que declara uno.

---

## 4. El aspecto, rama a rama

`_aspectos_morfologicos()` vale hasta **2 de los 10 puntos** del score (20 %).
Su condición es `suf in {ka, ni, da} and (raiz in _RAICES_VERB or len(raiz) >= 3)`.

```
control contra _aspectos_morfologicos(): VERDE (0 desvíos de 3.379 respuestas)

_RAICES_VERB: 1.424 claves   proto-arahuaco 1.078 · lokono 273 · caquetío 73

detecciones totales: 62.347
  raíz verbal caquetía RECONSTRUIDA del núcleo     40.315
  COMODÍN DE LONGITUD (ningún verbo de por medio)  20.165
  raíz verbal caquetía ATESTIGUADA (cat pendiente)  1.856
  aglutinado (naaka, masaka)                            10
  raíz verbal LOKONO                                     1
```

Dos cosas, y la segunda es más grave que la primera.

**Una.** `_RAICES_VERB` se construye como `{k for k, v in VOCABULARIO_BASE if
v['cat'] == 'v_raiz'}` — **sin filtrar por lengua**. De sus 1.424 claves,
**1.351 no son caquetías**. Y `score_linguistico.es_arahuaco()` devuelve
`True` para cualquier token cuyo primer segmento esté ahí. Es la misma clase
de agujero que el `return "caquetío"` del 2026-09-20, en otra puerta.

**Dos, y es la que manda.** Medido en puntos y no en detecciones, **el
componente de aspecto está SATURADO**:

```
media de puntos de aspecto por respuesta            1,9982  (de un máximo de 2,0)
la misma media si el comodín no contara             1,9296
respuestas cuyo punto de aspecto cambiaría             211  de 3.379
respuestas cuyo aspecto ENTERO es comodín               21  de 3.379
```

El 20 % del score **no discrimina nada**: casi todas las respuestas tocan el
tope. Es exactamente la trampa de `pct_caquetio` (issue #69, «91 % de las
respuestas en 1.0 — no la uses para comparar agentes»), en el otro quinto de
la métrica, y no estaba escrita. Tapar el comodín es correcto y **no arregla
la saturación**: la mueve de 1,9982 a 1,9296.

---

## 5. El contraste arahuaco

Contra la comparanda que el repo ya tiene, y sólo contra fuentes de
`4-fuentes/`. Cada sonda sobre el canon dice qué se buscó (regla 6).

### 5.1 Clases de verbo: estativo vs. activo — **HUECO**

**La comparanda.** [[perea-alonso-1942]] pp. 634-640: la **4ª conjugación
lokono es la de los ESTATIVOS** —colores, tamaños, sabores, estados:
`cule-n` 'ser rojo', `ibe-n` 'estar lleno', `hebbe-n` 'ser viejo'— y lleva el
pronombre **pospuesto**. Y pp. 598-599 y 608, la teoría de Quandt que Perea
recoge: *cualquier nombre, adjetivo o partícula se hace verbo anteponiendo
`a-` o `c-`*. De ahí la frase que resume el hueco entero:

> «"Rojo" no es un adjetivo en lokono: es el verbo `cule-n` "ser rojo" […].
> Para una retroabstracción caquetía esto dice que buscar "adjetivos" sueltos
> es buscar en la categoría equivocada.»
> — `6-fusion/lokono_gramatica_perea_1942.yaml` §la_teoria_de_las_clases_segun_quand

**Qué hace hoy el proyecto.** Sonda: las categorías de `VOCABULARIO_BASE`.

```
¿hay cat «estativo»?  NO      ¿hay cat «activo»?  NO
cats de familia caquetía: sust 283 · v_raiz 73 · adj 11 · part 10 · pron 7 ·
                          título 4 · num 4 · topón 1 · interr 1
```

**El hueco.** Hay **una sola clase verbal** (`v_raiz`) y **una clase `adj`
de 11 miembros** que en un sistema arahuaco probablemente no debería existir.
Y los agentes ya lo notaron: `siwato-ni`, `tüshi-da`, `ma-siwato-ni`,
`kasuta-bana-iro` — **143 usos de aspecto sobre adjetivo**, que es la 4ª
conjugación lokono reinventada desde el uso.

Es también **el caso que destapó la sesión de hoy**: el viento. `juri` 'viento,
ventarrón' lleva `cat: v_raiz` —puesto por la heurística— y de ahí `juri-ni`
(157 usos) entra por la rama buena del detector de aspecto y cuenta como verbo
conjugado. Si `juri` fuera estativo, `juri-ni` sería gramatical de otra manera;
si fuera nombre, el camino bueno era `ka-juri` 'hay viento' (van Buurt §8).

### 5.2 Alineamiento y marcas de persona — **HUECO**

**La comparanda.** [[perea-alonso-1942]] pp. 635 y 652 da **dos juegos**:

| | prefijados (transitivos) | pospuestos (estativos y negativos) |
|---|---|---|
| 1sg | `d-a-` / `da-` | `de` |
| 2sg | `b-a-` / `bu-` | `bu` |
| 3vr | `l-a-` / `li-` | `i` |
| 3nv | `t-a-` / `tu-` | `n` |
| 1pl | `w-a-` / `wa-` | `u` |
| 2pl | `h-a-` / `hù-` | `hù` |
| 3pl | `n-a-` / `na-` | `ye` |

Regla del propio Perea: *transitivo → prefijado; intransitivo, estativo o
negativo → pospuesto* (`halli-kebbe de` 'me alegro'). Y `2-lengua/morfologia.md`
ya lo cita desde el 2026-09-12.

**Qué hace hoy el proyecto.**

```
pronombres del prompt, por capa:
  taya · pia · nüma · waya · naya   →   los CINCO caquetío-reconstruido, del wayuu
pronombres caquetíos ATESTIGUADOS en el lexicón:
  kudanga  'usted, vos (2da persona formal)'      Zavala p.73 vía Arcaya: «chacamba cudanga»
  kuté     'a usted, para usted (dativo formal)'   Zavala p.73 vía Arcaya: «cudan de cuté»
```

**El hueco, y una contradicción.** El caquetío del canon **no tiene ni un
pronombre atestiguado en el prompt** y tiene **un solo juego**, sin
alineamiento. Y `2-lengua/lexicon.md` afirma que la política «manda la
atestiguada» «no toca los pronombres» porque «no tienen rival atestiguado»:
**eso es falso para la segunda persona**. `kudanga` y `kuté` existen, están
atestiguados con cita, y no se enseñan. El criterio de glosa idéntica no los
dispara (formal ≠ `pia` 'tú'), así que **no es un caso de la política: es una
pregunta nueva** (punto 10).

### 5.3 Posesión alienable / inalienable — **HUECO**

**La comparanda.** [[perea-alonso-1942]] p. 587: índices personales sobre el
nombre (`da-si-kua` 'mi casa') **y el índice absoluto `u-`/`ù-`**:
`u-si-kua-hù` = *LA casa, sin poseedor*. Es la marca de **no-poseído**, que es
como el arahuaco dice lo que en otras familias es alienabilidad. Y p. 586, los
posesivos absolutos: `da-kía` 'mío', `wa-kía` 'nuestro'.

**Qué hace hoy el proyecto.** Sonda: reglas cuyo `desc` mencione alienable o
no-poseído → **cero**. Hay cuatro prefijos posesivos y **ninguna forma de
decir «la casa» sin decir «mi casa»**.

**El hueco.** Un agente que quiera nombrar un objeto sin dueño no tiene cómo,
y en cambio tiene `ta-` a mano: eso explica parte de los 6.843 usos de `ta-`
sobre **258 raíces distintas**, que es el morfema más productivo del sistema
después del aspecto.

### 5.4 `ka-` atributivo / `ma-` privativo — **CONTRADICCIÓN**

**La comparanda.** [[van-buurt-2014]] §8: `ka-` es **localizador,
'hay / existe(n)'** — *Casibari* = «hay rocas duras». [[perea-alonso-1942]]
p. 555, **par mínimo**: `k-ere-u-ti` 'casado' / `m-ere-u-ti` 'soltero';
`c-a-nsi-ti` 'amante' = *el que TIENE afecto*. Es el par atributivo/privativo,
morfología corriente de la familia.

**Qué hace hoy el proyecto.** `REGLAS_POSESIVAS['ka-']`:

```
nombre: "posesivo genérico / asociativo"
desc:   "El/la que tiene X, poseído por, asociado con."
uso:    "ka- + SUSTANTIVO  →  el/la de X"
apoyo:  "ka- (prefijo posesivo no-pronominal)"      ← wayunaiki, sin obra
prompt: "ka- = el/la del: ka-biro (el salinero) · ka-maure (la del algodón)"
```

**La contradicción.** El `desc` («el/la que TIENE X») es correcto; **el nombre,
la tabla en que vive y el ejemplo del prompt lo convierten en un posesivo**.
`ka-biro` se enseña como 'el salinero' —una persona— cuando en van Buurt sería
'hay sal'. El resultado es que `ka-` se usa 564 veces contra 6.843 de `ta-`:
**el mecanismo bueno para predicar un nombre está archivado dentro de la tabla
de posesivos y se usa doce veces menos que el posesivo de primera persona**.
Y con el viento, que es el caso de hoy, los agentes usaron la vía mala —
conjugar `juri-ni`— teniendo `ka-juri` disponible.

### 5.5 Número y colectivo (`-kana`) — **EXCESO Y CERO VERIFICADO**

**La comparanda.** [[perea-alonso-1942]] p. 556: el plural lokono es
**pospuesto `-nu`** (`wadi-li-nu` 'varones'), y —esto importa— **los
irracionales NO distinguen número**: `keyu` 'venado, venados', `siba` 'piedra,
piedras', `adda` 'árbol, árboles', `a-wadu-lli` 'viento, vientos'. Perea añade
que los pocos animales pluralizados que aparecen son «huella del traductor
alemán».

**Qué hace hoy el proyecto.** `REGLAS_NUMERO['-kana']` declara
*«-kana (sufijo plural, **COGNADO DIRECTO con Caquetío**)»*. Sonda: qué forma
caquetía sostiene ese cognado.

```
claves de familia caquetía terminadas en -kana:   sakana   ('ofrenda, dádiva ritual', caquetío-HIPOTÉTICO)
ocurrencias de «kana» en 2-lengua/toponimos.yaml:  0
«kana» en lexicon_zavala.py:                       #57 (HB) 'demonio' — un LEMA, no un sufijo
```

**El exceso.** El único «cognado directo con caquetío» que el canon puede
exhibir es una forma **hipotética**, y la única `kana` atestiguada es
'demonio'. El cero está verificado con las tres consultas de arriba. Además el
plural se usa 258 veces y **162 de ellas sobre raíz verbal** (`maa-ni-kana`,
`masa-da-kana`), que la propia regla prohíbe.

### 5.6 Clasificadores y género — **HUECO DECLARADO, y quizá bien**

**La comparanda.** [[perea-alonso-1942]] p. 554: *no hay género gramatical;
hay **varonil** y **no varonil***, con sufijos `-ti/-tti` vr. y `-tu/-ttu` nv.,
y `-nu` plural común. El no varonil comprende a las mujeres, a los animales de
ambos sexos y a todas las cosas. Los achagua de [[neira-ribero-1762]] cambian
el numeral según lo que cuentan (personas, palos, ríos, lunas) — y el prompt
del proyecto **ya se lo cuenta a los agentes** en el bloque «contar más allá de
cuatro».

**Qué hace hoy el proyecto.** Sonda: reglas cuyo nombre o `desc` mencionen
género → **cero**.

**Lectura.** Aquí el hueco puede ser la decisión correcta: no hay ni un dato
caquetío de género, y la distinción varonil/no varonil es de las que arrastran
una cosmovisión entera. Importarla sería exactamente lo que la regla 4 prohíbe.
Pero **el hueco hay que declararlo**, no dejarlo por descuido — sobre todo
porque los antropónimos de la era 2 se rehicieron en septiembre precisamente
para quitar `-ko`/`-sha`, que era un género inventado.

### 5.7 Nominalización — **HUECO, y la comunidad ya lo llenó**

**La comparanda.** [[perea-alonso-1942]] pp. 609-612: nombre de acción **`-hù`**
(`a-iyaha-dda-hù` 'andadura'), **`-hi`** en los estativos (`c-a-nsi-hi` 'amor',
`halli-kebbe-hi` 'alegría'); participios `-ti`/`-tu`/`-nu`; agentivo `-ha-li-n`.
Y p. 561 el instrumental-local **`-na`** sobre la partícula durativa `-coa-`
(`a-balti-coa-na` 'asiento', `diki-kua-na` 'espejo'), con el aviso del propio
Perea: *«son pocos los vocablos así formados»*.

**Qué hace hoy el proyecto.** Sonda: reglas que deriven un nombre de un verbo
→ **cero**.

**El hueco, y lo que se hizo con él.** Los agentes **nominalizan con el
posesivo**: 1.107 usos de `ta-`/`ma-`/`wa-`/`ka-` sobre raíz verbal —
`ta-chaa` 'mi hacer', `wa-jai` 'nuestro oír', `ma-awa` 'sin beber'. Es una
solución razonable y no es la arahuaca. El `-na` de Perea, además, roza el
`-ana` del punto 6 por una vía independiente, con la cautela ya escrita en
`6-fusion/lokono_gramatica_perea_1942.yaml` §na-locativo-109: *es evidencia
comparativa de una lengua hermana, no evidencia sobre el caquetío*.

### 5.8 El sistema de aspecto de tres marcas — **¿LO SOSTIENE ALGO ATESTIGUADO? NO**

**La comparanda.** El propio canon lo declara: las tres marcas salen **enteras**
del wayunaiki (`-ka` ← tríada A en pasado; `-ni` ← `-iraa`; `-da` ← `-ee`
desiderativo + tríada C). Las tres tienen homógrafo lokono con otro valor
(`-ca` raíz de *ser/estar*, `-ni` el auxiliar `a-ni-n`, `-da/-dda` la partícula
del presente que **ni Perea ni de Goeje saben explicar**), y el YAML ya declara
que **eso no se afirma como cognación**: son formas de dos letras, y medir
parecido así es lo que produjo el 80 % de fallo de las 441 hipotéticas.

Y hay dos datos más, los dos de [[perea-alonso-1942]]:

- **El futuro lokono atestiguado es `-pa`**, con paradigma (`d-a-iyaha-ddi-pa`
  'andaré'). El prospectivo `-da` del canon no viene de ahí.
- p. 606, el gramático sospechando de su propia fuente: *«todo el mecanismo
  temporal de los pretéritos sea tan sólo uno de los tantos perfeccionamientos
  a priori de los misioneros»*, y que lo que la lengua hacía era un presente
  narrativo. **Eso es convergencia a favor de modelar con ASPECTO y no con
  tiempo** — es juicio de autor, no prueba, pero con su razón dicha.

**Qué hace hoy el proyecto.** Sonda: entradas `caquetío-atestiguado` que
sostengan `-ka`, `-ni` o `-da` → **cero en las tres**.

**La respuesta a la pregunta del encargo: no.** Nada atestiguado del caquetío
sostiene el sistema de tres marcas. Lo sostiene el wayuu, que es lo que D11
retiró como hermana por defecto, y el propio `morfologia.md` §2 ya lo dice
desde el 2026-09-08. Lo que esta auditoría añade es que **es el 20 % del score
y está saturado** (§4), o sea que el instrumento no sólo enseña una
reconstrucción sin apoyo: la premia hasta el tope casi siempre.

### 5.9 Reduplicación — **DECLARADA, MEDIDA, NO IMPLEMENTADA**

**La comparanda.** [[gatschet-1885]]: topónimos arubanos por duplicación de la
raíz disílaba (onomatopeya, diminutivo, pluralidad).
[[perea-alonso-1942]] p. 679: *«recurso frecuente en nuestro Arawak»* que
Schumann no menciona — `a-sucusu-n` 'lavar' → `a-sucu-sucu-n` 'bautizar';
`a-dia-n` → `a-dia-dia-n` 'disertar'.

**Qué hace hoy el proyecto.** `2-lengua/morfologia.md` §4 la mide y la declara
productiva (9,0 % de la toponimia caquetía contra 3,1 % wayunaiki y 0,7 %
lokono, mismo detector para todos). Sonda sobre el motor: reglas de
reduplicación → **cero**. No se enseña, no se reconoce, no se puntúa.

**El hueco.** Es el único rasgo que el proyecto ha **medido con control** y no
ha llevado al motor. Y la propia nota ya deja dicho cuál sería el alcance: *el
valor onomatopéyico es formación léxica histórica, no morfología viva; el de
pluralidad sí es candidato a regla productiva*.

### 5.10 Diminutivo — **BIEN, con un segundo sin incorporar**

`-iro` está atestiguado ([[zavala-reyes-2015]] #166), se enseña, se usa 229
veces sobre 36 raíces, y **el propio corpus contradice a Gatschet** en el punto
del diminutivo por reduplicación: cero casos. Eso está bien hecho y así se
queda. Lo que falta es `-bi`, el **segundo diminutivo** de [[van-buurt-2014]]
§6 (*gobí, gogorobí, kokorobí, lobi, makambí*), que sigue en
`MORFEMAS_VAN_BUURT` sin incorporar.

---

## 6. Decisiones (14)

Cada una lleva su tipo. **Corrección de error** = el sistema no hace lo que ya
está decidido, se arregla y no hace falta decidir nada. **Decisión de canon** =
la toma Miguel. **Corte de serie** = cambia lo que el agente VE o lo que el
scorer CUENTA, con su coste dicho.

> El coste común de todos los cortes de serie: **la serie C se repetiría**. Sus
> dos brazos —con escena y control, 216 + 216 respuestas— están medidos en
> `6-fusion/medicion_raices_de_ninguna_parte_2026-09-20.yaml` §serie_c. Si se
> aceptan varios puntos a la vez, **se aplican juntos y se re-corre una sola
> vez**; aplicarlos de uno en uno cuesta una serie por punto. Y todo corte que
> toque el scorer hay que medirlo antes con el patrón A/B de
> `medir_politica_atestiguado_manda.py`: el módulo de `--ref` contra el del
> árbol de trabajo, con su control en verde.

---

### 1. El comodín de longitud del detector de aspecto
**Tipo: corrección de error + corte de serie.**

`_aspectos_morfologicos()` cuenta `-ka/-ni/-da` sobre cualquier raíz con guion
de tres o más letras, sin mirar si hay verbo. **20.165 detecciones de 62.347
entran por ahí** (`hamaka-chaa-ni`, `kali-barsure-da`, `baro-ni`).

- **A.** Quitar el comodín: el aspecto sólo cuenta sobre `_RAICES_VERB`.
  *Coste medido: la media de puntos de aspecto baja de 1,9982 a 1,9296; cambia
  el punto en 211 de 3.379 respuestas; 21 respuestas se quedan sin aspecto.*
- **B.** Dejarlo, y declararlo en `CLAUDE.md` como residuo elegido.
- **C.** Sustituirlo por un comodín acotado: sólo si el ÚLTIMO segmento antes
  del aspecto es raíz verbal (`ta-hamaka-chaa-ni` cuenta por `chaa`), que es el
  caso legítimo que el comodín estaba cubriendo a ciegas.

**Recomendación: C.** A es correcto y tira el caso bueno (los compuestos con
verbo dentro); B deja abierta la puerta por la que entra `lumina-bana-ni`. C
cierra el agujero sin perder el compuesto, que es justo lo que el arreglo de la
raíz de ninguna parte ya hizo en la otra puerta.

### 2. `_RAICES_VERB` mezcla las cinco lenguas
**Tipo: corrección de error + corte de serie.**

`_RAICES_VERB` = todas las claves con `cat: v_raiz` de `VOCABULARIO_BASE`, **sin
filtrar lengua**: 1.424 claves, de las que **1.351 no son caquetías** (1.078
proto-arahuaco, 273 lokono). `score_linguistico.es_arahuaco()` devuelve `True`
para cualquier token cuyo primer segmento esté ahí.

- **A.** Filtrar a familia caquetía (73 claves) en las dos puertas
  —`es_arahuaco` y el detector de aspecto—.
- **B.** Filtrarlo sólo en `es_arahuaco` (que es donde decide densidad) y dejar
  el detector de aspecto con la tabla entera.
- **C.** Dejarlo y declararlo.

**Recomendación: A**, y **aplicado a la vez que el punto 1**: los dos tocan las
mismas dos funciones y un corte de serie cuesta lo mismo por uno que por dos.
⚠️ **Depende de la clasificación pendiente**: las 73 caquetías incluyen las 49
que la otra sesión está repartiendo. Esto se aplica **después** de esa tanda,
no antes.

### 3. El componente de aspecto está saturado
**Tipo: decisión de canon.**

Media 1,9982 sobre un máximo de 2,0. El 20 % del score no separa a nadie — la
misma trampa que `pct_caquetio` (#69), en otro quinto de la métrica.

- **A.** Dejarlo y **escribirlo** en `CLAUDE.md` junto a la fila de
  `pct_caquetio`: «el componente de aspecto está saturado, no lo uses para
  comparar agentes».
- **B.** Cambiar el peso: un punto por aspecto distinto sobre **tipos de raíz**
  distintos, o medir densidad de aspecto (aspectos / verbos) en vez de
  variedad.
- **C.** Bajar el tope de 2,0 a 1,0 y devolver el punto a la riqueza léxica.

**Recomendación: A ahora, B en el próximo corte grande.** Cambiar el peso mueve
el score de toda la base y no arregla ninguna verdad sobre la lengua; escribir
la trampa cuesta cero y evita la próxima conclusión falsa. B es un rediseño de
la métrica y merece su propio diseño en `5-experimento/`.

### 4. Declarar la clase de verbo: estativo vs. activo
**Tipo: decisión de canon + corte de serie.**

Es el rasgo que destapó el caso de hoy. Lokono tiene una conjugación entera de
estativos con pronombre pospuesto ([[perea-alonso-1942]] pp. 634-640) y el
caquetío del canon tiene una sola clase verbal y 11 adjetivos. Los agentes ya
conjugan los adjetivos: 143 usos.

- **A.** No declarar la clase. Los adjetivos siguen siendo adjetivos y
  `siwato-ni` sigue siendo una violación de slot que nadie sanciona.
- **B.** Declarar la clase **sin cambiar la morfología**: se añade
  `cat: v_estativo` a las entradas que lo sean y se dice en el prompt que un
  estado se predica con aspecto igual que una acción. Sin pronombre pospuesto.
- **C.** Declarar la clase **con su alineamiento**, importando el juego
  pospuesto del lokono (punto 5.2): estativo → pronombre detrás.

**Recomendación: B.** C es tipológicamente más fiel y **no tiene ni un dato
caquetío detrás**: importaría un paradigma entero de la hermana que D11 dejó
abierta, que es exactamente la clase de préstamo que este proyecto lleva un mes
deshaciendo. B legitima lo que los agentes ya hacen, cuesta una etiqueta y una
línea de prompt, y deja C disponible si D11 fase 3 se resuelve hacia el lokono.

⚠️ **B se ejecuta con la otra sesión, no contra ella**: las 49 raíces de Zavala
se están repartiendo ahora mismo en estativo / acción / nombre. **Esa tanda ES
la mitad de esta decisión.** Lo que queda para Miguel es si la etiqueta llega
al prompt o se queda en el lexicón.

### 5. `ka-` es atributivo, no posesivo
**Tipo: decisión de canon + corte de serie.**

[[van-buurt-2014]] §8 lo documenta como localizador 'hay, existe(n)'
(*Casibari*); [[perea-alonso-1942]] p. 555 da el par mínimo con el privativo
`m-`. El motor lo tiene en `REGLAS_POSESIVAS` con nombre «posesivo genérico» y
lo enseña como `ka-biro = el salinero`. Se usa 564 veces contra 6.843 de `ta-`.

- **A.** Cambiar sólo el **nombre y el apoyo**: `ka-` = atributivo /
  existencial, con la cita de van Buurt en el campo `atestiguado`. El prompt no
  cambia.
- **B.** A, **y además cambiar el ejemplo del prompt**: `ka-biro = hay sal, el
  lugar tiene sal` junto a `ka-maure`. Mueve el prompt → corte de serie.
- **C.** A y B, **y sacar `ka-` y `ma-` de `REGLAS_POSESIVAS` a una tabla
  propia** `REGLAS_ATRIBUTIVAS`, que es lo que son. Cambia
  `TODAS_LAS_REGLAS` sólo en la agrupación, no en las claves, así que el
  desafijador no se mueve.

**Recomendación: C.** Es la corrección que más lengua arregla por menos coste:
las claves no cambian, `nucleo_de_token()` devuelve lo mismo, y el par
`ka-`/`ma-` deja de estar escondido en la tabla equivocada. El único corte es
el ejemplo del prompt, y va con los demás.

> Con esto, el caso del viento tiene su vía buena escrita: **`ka-juri` 'hay
> viento'** en vez de `juri-ni`.

### 6. `-ana`: el motor enseña la glosa que #109 retiró
**Tipo: decisión de canon + corte de serie.**

El canon retiró 'lugar de' el 2026-09-07 (censo de Esteves: 0 casos). Las dos
plantillas siguen enseñando «`-ana` = lugar de X». La propia regla se declara
`canon-simulación` en su campo `evidencia` — o sea que **está escrito que el
prompt dice algo que el dato no sostiene**, y aun así lo dice. Uso: 290 sobre
53 raíces.

- **A.** Quitar `-ana` del prompt y dejarlo sólo en el desafijador (que es
  donde hace falta para no romper el conteo de las formas ya dichas).
- **B.** Enseñarlo **sin glosa**, como se enseñan `-ubana` y `-uru`:
  *«desinencia atestiguada cuyo valor nadie anotó; puedes usarla si propones su
  valor entre corchetes»*. Es el patrón que el proyecto ya eligió para ese
  caso exacto.
- **C.** Dejarlo como está y declarar la convención en `CLAUDE.md`.

**Recomendación: B.** Es coherente con lo que el proyecto ya hace con las
desinencias sin valor, respeta #109 sin borrar una forma atestiguada, y
**abre** la posibilidad de que los agentes propongan la glosa — que es
exactamente lo que esta simulación existe para observar. A tira un formante
atestiguado; C mantiene el error con permiso.

### 7. `-gua`: sin procedencia
**Tipo: decisión de canon.**

Único apoyo escrito: «Topónimos venezolanos de Falcón y Sucre». Cero clave
foránea. Se enseña en las dos plantillas y se usa 102 veces sobre 37 raíces.

- **A.** Declararlo `deuda: sin-procedencia` y seguir enseñándolo, como hace
  el resto del proyecto con lo que no tiene fuente.
- **B.** Buscarle la fuente: `2-lengua/toponimos.yaml` tiene 109 topónimos en
  canon y el gazeteer de Esteves está minado. Es una campaña corta, y si
  aparece, `-gua` pasa a atestiguado.
- **C.** Degradarlo a `canon-simulación` como `-ana` hasta que aparezca.

**Recomendación: B, con A mientras tanto.** Es el único de los doce sin cita
que tiene una fuente plausible ya en el repo y sin minar para esta pregunta.
Declararlo cuesta una línea; buscarlo, media sesión.

### 8. `-kana`: el «cognado directo con caquetío» que no tiene forma detrás
**Tipo: decisión de canon.**

La regla afirma *«COGNADO DIRECTO con Caquetío»*. El único `-kana` de familia
caquetía en el lexicón es `sakana` 'ofrenda', **hipotética**; en `toponimos.yaml`
hay cero; en Zavala `kana` es 'demonio', un lema. Y el ejemplo de la regla
forma el plural **de una palabra wayuu** (`wayuu + kana = wayuukana`).

- **A.** Bajar la afirmación: `-kana` pasa a `reconstruido desde el wayunaiki`,
  deuda D11 como los tres aspectos, y se reescribe el ejemplo con una voz
  caquetía (`barsure-kana`, que la regla ya trae).
- **B.** A, y además **archivarlo** del habla hasta que aparezca un plural
  caquetío: el lokono pluraliza con `-nu` pospuesto y **no pluraliza los
  irracionales** ([[perea-alonso-1942]] p. 556), así que puede que el caquetío
  tampoco.
- **C.** Dejarlo.

**Recomendación: A.** B es tentador y va demasiado lejos: quitar el plural deja
a los agentes sin forma de decir «los ancianos» y el dato lokono es de otra
lengua. A corrige la afirmación falsa —que es lo que la regla 2 exige— y deja
la forma, que no estorba. **Lo que sí se hace sin preguntar**: reescribir los
tres ejemplos que enseñan wayuu.

### 9. `-naiki`: cero usos, cero plantillas, apoyo circular
**Tipo: decisión de canon.**

0 usos en 95.445. Ninguna plantilla lo enseña. Su apoyo es literalmente el
nombre de la lengua andamio (`wayuunaiki`), y su único ejemplo también.

- **A.** Retirarlo a `REGLAS_RETIRADAS`, junto a `-ko` y `-sha`, por la misma
  razón que se retiraron aquéllos: sin fuente, y era convención.
- **B.** Dejarlo en el desafijador y quitarlo de la documentación.
- **C.** Dejarlo como está.

**Recomendación: A.** Es gratis —nadie lo ha dicho nunca, así que no mueve
ningún score— y es la misma regla que Miguel ya aplicó el 2026-09-14. ⚠️ Sacarlo
de `TODAS_LAS_REGLAS` **sí mueve `_SUFIJOS_CAQ`**, así que aunque el uso sea
cero hay que medirlo antes: puede haber una forma en `-naiki` que hoy se
desafija y mañana no.

### 10. `kudanga` y `kuté`: los pronombres atestiguados que no se enseñan
**Tipo: decisión de canon + corte de serie.**

El prompt enseña cinco pronombres, **los cinco reconstruidos del wayuu**. El
lexicón tiene **dos pronombres caquetío-atestiguados con cita**
([[zavala-reyes-2015]] p. 73 vía Arcaya: «chacamba cudanga» ¿cómo está usted?,
«cudan de cuté» para servir a usted) y **ninguno se enseña**. La política
«manda la atestiguada» no los dispara porque la glosa no es idéntica (formal ≠
`pia` 'tú'), pero `2-lengua/lexicon.md` afirma que «los pronombres no tienen
rival atestiguado», **y eso no es exacto**.

- **A.** Añadir los dos al prompt **como registro formal**, junto a los cinco:
  `pia` para el tú corriente, `kudanga` para dirigirse a un mayor o a un Diao.
  Es un rasgo social, no sólo gramatical, y la era 2 tiene jerarquía escrita.
- **B.** Añadirlos al lexicón visible sin tocar la plantilla (ya están; se
  quedan en la muestra rotativa).
- **C.** No tocarlos, y **corregir la frase de `lexicon.md`** para que no diga
  que no hay rival.

**Recomendación: A**, con C incluido en cualquier caso. Es la política de Miguel
del 2026-09-19 aplicada donde todavía no llegó: hay forma atestiguada, se usa.
Y aquí ni siquiera hay que archivar nada —`pia` y `kudanga` no compiten, se
reparten registros—, así que es el caso barato de esa política.

### 11. La nominalización que falta y que la comunidad ya inventó
**Tipo: decisión de canon + corte de serie.**

Cero reglas que deriven nombre de verbo. Los agentes lo resuelven con el
posesivo: **1.107 usos** de `ta-`/`ma-`/`wa-`/`ka-` sobre raíz verbal
(`ta-chaa` 'mi hacer', `wa-jai` 'nuestro oír').

- **A.** No declarar nada y **reconocer lo que hacen**: quitar «posesivo sobre
  verbo» de la lista de violaciones y declarar en `morfologia.md` que el
  posesivo nominaliza. Es describir el sistema que emergió.
- **B.** Declarar un nominalizador propio y enseñarlo. Sin dato caquetío: el
  `-hù` / `-hi` es lokono ([[perea-alonso-1942]] pp. 609-612).
- **C.** Abrir una **campaña de retroabstracción**: buscar en Zavala, Alvarado
  y Arcaya nombres de acción que compartan terminación con un verbo, a la
  manera de `matakán`. Si sale algo, entra atestiguado; si no, A.

**Recomendación: C, con A mientras tanto.** B importa morfología lokono sin
dato y es justo lo que el proyecto decidió no hacer. A es honesto y gratis y
además **es un hallazgo**: la comunidad llenó un hueco por su cuenta, y eso es
lo que la simulación existe para producir. C es la única vía que puede darle
fuente.

### 12. El apilamiento de afijos: 57 patrones que nadie declaró
**Tipo: decisión de canon.**

988 usos, 273 formas, hasta cuatro slots (`ka-biro-uco-aima`). El sistema
declara UN afijo por regla y no dice ni que se puedan apilar ni en qué orden.

- **A.** **Declarar que es libre**: escribir en `morfologia.md` que los afijos
  se apilan y que el orden no está fijado, y dejar la lista medida como el
  registro de lo que la comunidad hace. No se toca el prompt.
- **B.** Declarar un **orden de plantilla**
  (`posesivo + RAÍZ + derivativo + locativo + número + aspecto`) derivado de lo
  que ya se dice, y enseñarlo. Corte de serie, y **decide por la comunidad**
  algo que la comunidad estaba decidiendo sola.
- **C.** Declarar sólo las **dos exclusiones** que sí parecen errores —dos
  aspectos en la misma forma (121 usos) y dos locativos (42 usos)— y dejar el
  resto libre.

**Recomendación: A.** Es el punto donde más se nota qué clase de proyecto es
esto: **la gramática emergente es el resultado, no el defecto**. Fijar el orden
(B) convertiría un hallazgo en una instrucción y haría circular la medición —
el mismo error que enseñar `kali-bana` y luego contarla como acuñación. C es
tentador pero `chaa-ni-da` («lo está haciendo y lo va a hacer») no es
obviamente agramatical en un sistema sin tiempo; llamarlo error es una
afirmación sobre una lengua que no tenemos.

### 13. Los tres huecos que se deciden juntos: posesión, número, género
**Tipo: decisión de canon.**

Los tres son rasgos que la comparanda documenta con cita y el canon no tiene:
**no-poseído** (`u-si-kua-hù` 'LA casa', Perea p. 587), **número de los
irracionales** (Perea p. 556) y **varonil / no varonil** (Perea p. 554). Los
tres tienen la misma forma de decisión, y por eso van en un punto.

- **A.** **Declarar los tres huecos** en `morfologia.md` §nuevo «lo que un
  sistema arahuaco tiene y éste no», con su cita y sin importar nada. El
  proyecto declara lo que le falta, como declara sus deudas de fuente.
- **B.** Importar el que menos cosmovisión arrastra —el **no-poseído**, que es
  puramente gramatical— y dejar los otros dos declarados.
- **C.** Importar los tres desde el lokono.

**Recomendación: B.** El no-poseído tapa un hueco real y medido: 6.843 usos de
`ta-` sobre 258 raíces es, en parte, agentes que no tienen otra forma de
nombrar una cosa. Género (C) es lo que la regla 4 prohíbe importar sin
marcarlo, y el proyecto acaba de pasar por eso con `-ko`/`-sha`. El número de
los irracionales es un dato precioso y de otra lengua: se declara y se espera.

### 14. D5 en la morfología: `-bacoa`, `-uto` y los ejemplos rancios
**Tipo: corrección bajo una decisión ya tomada + corte de serie.**

D5 decidió el 2026-08-31 que **la grafía española es grafía y el lema fonémico
es la palabra**. La morfología se quedó fuera de esa migración:

- `-bacoa` se escribe con `c` y **el lema del lexicón es `bakoa`**, atestiguado.
  El prompt enseña `ada + -bacoa = adabacoa`, y **ninguna de las tres formas
  existe en `VOCABULARIO_BASE`** (`bakoa` sí).
- `-uto` se escribe en el prompt (dentro del `uso` de `-uco`) **sin estar en
  `TODAS_LAS_REGLAS`**: se enseña y no se reconoce.
- `Judibana`, `Corogua`, `adabacoa`, `yacarebacoa`, `wayuukana` son derivados
  que las reglas presentan y el lexicón no tiene.

- **A.** Migrar los afijos al lema fonémico (`-bakoa`), declarar `-uto` como
  variante dentro de su regla y reescribir los cinco derivados con formas del
  lexicón. **Cambia una clave de `TODAS_LAS_REGLAS` → cambia `_SUFIJOS_CAQ` →
  mueve `nucleo_de_token()` y con él el score.** Hay que medirlo antes.
- **B.** Sólo la deuda documental (ejemplos y `-uto`), sin tocar la clave
  `-bacoa`.
- **C.** Dejarlo todo y anotar la excepción de D5.

**Recomendación: B ahora, A en el mismo corte que los puntos 1, 2 y 5.**
B es gratis y arregla lo que lee la próxima sesión. A es correcto pero mueve el
desafijador, así que va con los otros cortes y con su medición: hay 57 usos de
`-bacoa` en la base y todos dejarían de segmentarse igual.

---

## Deudas abiertas que deja esta auditoría

- **Las 49 raíces de Zavala.** Los puntos 2, 3 y 4 no se pueden cerrar sin esa
  clasificación. Esta auditoría midió cuánto depende de ella: **1.856 de las
  62.347 detecciones de aspecto** descansan hoy en una `cat` puesta por una
  heurística de una línea, y buena parte de las 1.778 violaciones de slot
  dejarían de serlo o pasarían a serlo según cómo se reparta.
- **`-shi` / `-chi`, 22 apariciones, sin glosar.** `morfemas.yaml` lo llama
  «el formante más frecuente del corpus insular y nadie lo ha glosado… el
  objetivo nº 1 de cualquier minería futura de toponimia ABC». Sigue siéndolo.
- **`-are` vs. `-ure`.** La toponimia dice 'sitio de', van Buurt §5 dice
  'raíz'. `morfemas.yaml` lo declara *«hermana de D9»* y sigue abierto. Con
  cinco apoyos y `dabudare` como caso decisivo, es la próxima D9.
- **D11 fase 3 sigue siendo el nudo.** Nueve de los 21 morfemas y el 100 % del
  aspecto y de la posesión dependen de ella. Lo que esta auditoría añade a
  `decision-d11-fase3-nucleo-lokono-achagua.md` es que **la fase 3 no es una
  re-etiqueta: es la morfología entera**.
- **El arte del achagua sin minar.** `6-fusion/achagua_neira_ribero_1762.yaml`
  §arte dice: *«Del arte (pliegos 7-27) se extrajeron SOLO pronombres y
  numerales… El resto (declinaciones, seis conjugaciones, tratados, los
  capítulos de "equívocos" y el verbo sustantivo) queda sin minar y es material
  de primer orden»*. Para los puntos 4, 11 y 13 **es la fuente que falta** —y
  es de los Llanos, así que entra como comparanda marcada, nunca como canon
  costero (regla 4).
- **`-bi`, el segundo diminutivo** ([[van-buurt-2014]] §6), sigue en
  `MORFEMAS_VAN_BUURT` sin adjudicar.
