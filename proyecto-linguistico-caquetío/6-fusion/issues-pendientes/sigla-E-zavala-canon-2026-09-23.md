# La sigla (E) de Zavala es Esteves: el canon, re-medido

**Para que Miguel decida.** Campaña corta de cierre, decisión **cc.4**
(«la sigla es Zavala Esteves, eh, ok, miramos también el canon de eso»), que
es la opción 1-A del issue `toponimos-esteves-lote-2026-09-22.md`. Nada se ha
aplicado: esto propone.

- La lectura, voz por voz y con página: `6-fusion/sigla_E_zavala_lectura_2026-09-23.yaml` (sin cifras).
- Las cifras las escribe `6-fusion/scripts/medir_sigla_E_zavala.py` en
  `6-fusion/medicion_sigla_E_zavala_2026-09-23.yaml` (`--check` dice si está al
  día). Todo número de abajo sale de ahí; entre corchetes, la sección.

---

## 0. Lo que resultó falso al medirlo

1. **«Esteves y van Buurt dicen lo mismo» es una sola fuente.** van Buurt 2014
   escribe «(Cruz Esteves, 1989)» detrás de `ure` 'raíz', `juri` 'viento',
   `cari` 'costa' e `ima` 'húmedo', y su «bara means tree» va en el mismo
   párrafo. Así que la nota de `bara` («con Esteves 1989 y van Buurt 2014
   diciendo lo mismo»), la de `kari`, el conflicto de `-ure` en
   `morfemas.yaml` y la razón de *alaurima* en `lexicon_toponimos.py` —«`-ima`…
   confirmado independientemente por van Buurt §10 vía Onima»— cuentan dos
   veces a Esteves.
2. **`waranao` 'salado, ácido' no está en Esteves.** La entrada GUARANAO (p. 41,
   vista en imagen) describe la salina, la fama de su sal para los ojos y la Zona
   Franca; no glosa la voz. Y es la que `prompt_reglas_breve` pone de ejemplo de
   verbo estativo **a los 63** («usera, waranao, wasima son verbos»).
3. **El único apoyo de `ure` 'raíz' que no es un topónimo es un topónimo
   guaraní**: el «Uretebere» de Cabeza de Vaca, «Ure: raíz; Bere: amargo»
   (p. 22).
4. **`tuba` 'aglomeración' nace de enmendar un nombre atestiguado.** Esteves
   dice que Todariquiba no significa nada y que la forma buena sería
   «Tubariquiba», 'pedregal' (p. 64). Y **`rao`** es 'arena' en la p. 64 y
   'aglomeración' en la p. 92.
5. **`-iro` no es un diminutivo caquetío atestiguado**: Esteves dice
   «diminutivo de voces indígenas», en dos topónimos de la Parte II (pp. 88 y
   104). **`-uco`** es inducción suya: «lo hemos hallado formando voces
   compuestas» (p. 31). Los dos se enseñan bajo el rótulo «sufijos que las
   fuentes recogen en boca caquetía».
6. **Cumarebo (toponimo-004, nivel A) no tiene «segunda atestación
   independiente de ebo»**: la otra que nombra es Jurijurebo, y las dos son
   Esteves. Zavala #94 (E) «Camino del cacique Cumare» es Esteves p. 105.
7. **`jachos` es, casi seguro, castellano**: «hacho» 'tea', con la h aspirada.
   Esteves lo pone entre comillas y no lo da por indígena (p. 33).
8. **`naure` lleva la glosa de otra palabra**: 'planta bejucosa' es *ñaure*
   (#186); *naure* es 'jojoto' (#185), y ésa sí tiene testigo fuera de
   Esteves (Alvarado 1921 p. 226, *náura*).
9. **La cifra**: hoy no son «43 de 228» sino **43 de 227** atestiguadas
   [el_canon]. Y 43 sólo si se cuenta la entrada que da la glosa de cada voz;
   contando todo número de Zavala que la nota nombra salen 42, porque `bara`
   cita de paso a *barabara* (A) [el_canon.atestiguadas_solo_E.diferencias].
10. **El desfase de página de Esteves no es constante en los tomos 4 y 6**
    (faltan la p. 82, blanca, y la 144). La skill `campana-toponimos` §2 sólo da
    los de los tomos 1-3; con +72 a ciegas, Bariro sale en la p. 87 y está en la
    88, Bisure en la 89 y está en la 90.

Y una confirmación que conviene escribir: **las (E) de Zavala son Esteves 1989,
frase por frase.** «Guaru… voltúrido, cataneja, ave mayor que el zamuro» es la
p. 42 («el voltúrido que llamamos cunareja, ave mayor que el zamuro»); Iguí,
Dividive, Caujaro y Tuturutos son las glosas entre paréntesis de las pp. 117,
110, 100 y 66. Zavala no lo pone en su bibliografía.

## 1. Qué dice Esteves de cada una

Del glosario, 81 entradas llevan (E) y 58 sólo (E) [glosario_zavala]. En el
lexicón las citan 65 atestiguadas; **43 dependen sólo de (E)**. Leídas en el
libro, se reparten así [por_opcion.B]:

| Qué hace Esteves con la voz | Cuántas | Ejemplos |
|---|---|---|
| etimología de un topónimo, o «en caquetío X es Y» sin fuente, o no está | 12 | `juri`, `kari`, `ure`, `tuba`, `rao`, `siwa`, `aka`, `tubarao`, `naure`, `waru`, `waranao` + `jachos` |
| nombre vivo de una planta, animal, materia u objeto de la península | 26 | `kaseto`, `kaujaro`, `tauta`, `tigi`, `tijua`, `warataro`, `tuturutos`, `saruro`, `kuna`… |
| la forma está en otra fuente y la glosa encaja (reconstruido) | 2 | `ebo` (Cazebo 'poniente' de Galeotto Cey, Guacurebo), `bara` (barabara 'árbol de Coro', Alvarado) |
| hay otra fuente de la misma voz | 3 | `igi` (Alvarado: «Coro»), `waka` (Alvarado: guaca «Us. en Occ.»), `kapo` (= `kapu`, HB y Oliver A-9) |

Las 22 que llevan (E) **y otra sigla** (AM, HB, A, PMA, HP, GC) se sostienen
sin la doble cuenta: les queda al menos esa otra [voces]. Entre ellas `para`
(HP y el *paragua* de Galeotto Cey), `kiba` (PMA), `bakoa` (AM y la Relación
de 1579) y `bisure`, `chaure`, `waranaro` (la Tabla A-9 de Oliver).

## 2. Pregunta 1 — la etiqueta de las 40 que no tienen otra fuente

La regla ya estaba escrita, en la ficha de Esteves: *una etimología suya sin
cita entra como `hipotetico`, sube a `reconstruido` si corrobora algo que ya
teníamos, y sólo llega a `atestiguado` si se persigue el documento*. El canon
la aplicaba a Esteves por su nombre y no a Esteves por su sigla.

- **A. Degradar todas a hipotético** (regla 2 sin matices). Cambian **40**.
  Todas salen del perfil `era2` (la capa hipotética no se muestra):
  **2.990** apariciones menos en el ensayo de muestreo de 1.260 prompts, y
  **1.817** usos en la base de voces que la comunidad deja de ver.
- **B. Según lo que hace Esteves con cada una** (la tabla de arriba). Cambian
  **40**: **12 → hipotético, 26 → retroabstraído** (la capa de las voces vivas
  documentadas cuyo sustrato caquetío no consta, precedente `chiriware` y
  `tukeke` del 2026-09-10), **2 → reconstruido**. Sólo las 12 salen del perfil
  `era2`: **935** apariciones menos en el ensayo, **1.557** usos (casi todo
  `juri` y `kari`).
- **C. Marcar sin degradar.** Cambian **0**: la nota y la procedencia pasan a
  decir «Esteves 1989 p. N». Barato, pero la etiqueta seguiría diciendo
  «atestiguado» de lo que su propia fuente llama etimología.
- **D. Degradar sólo las etimologías.** Cambian **11** (las de B sin `jachos`);
  las voces vivas y las corroboradas se quedan atestiguadas.

Lo que no cambia con ninguna: **el score** (`score_linguistico()` no lee la
capa; `capas_de_score` tiene las cuatro). Lo que sí cambia con A, B y D:
cualquier voz que salga de una capa sembrable **re-sortea las 52 semillas de
idiolecto derivadas** de 63 (el sorteo es módulo el tamaño del campo, así que
mueve también a quien no la llevaba: la llevaban 22 en A y 12 en B)
[cadena.semillas_de_idiolecto_derivadas]. Es el precio de cualquier cambio de
capa, no de éste en particular, pero hay que pagarlo antes de la corrida base
y no después.

**Mi recomendación: B.** Es la regla que la ficha de Esteves ya tenía, y
distingue lo que Esteves *vio* (una planta que se llama así en la península)
de lo que *dedujo* (que *juri* es viento porque Jurijurebo lo sería).

## 3. Pregunta 2 — la política «manda la atestiguada», par por par

De los siete archivos del 2026-09-19 [cadena.politica_manda_la_atestiguada]:

| par | manda | archivada | con A, B o D |
|---|---|---|---|
| 1 sol | `kasi` (GC) | `kali` | se sostiene |
| 3 ofrecer | `were` (AM) | `paa` | se sostiene |
| 4 escuchar | `jai` (AM) | `kira` | se sostiene |
| 12 luna | `kati` (CGB) | `kasha` | se sostiene |
| 13 mar | `para` (E+HP; *paragua* GC) | `habo` | se sostiene |
| **16 viento** | **`juri` (E)** | **`joutai`** | **se cae**: ya no hay rival atestiguado |
| 18 espanto | `etamo` (AM) | `mülia` | se sostiene |

`joutai` no vuelve, pero por otra razón: su propia nota la declara derivada
del wayuu (deuda D11), y cc.12 manda no reconstruir desde el wayuu. Lo que
cambia es el **motivo escrito** del archivo, y que **'viento' se queda con una
sola voz, hipotética**. Con `para` hay un matiz que no la tumba: Esteves cita a
Hill Peña (p. 41), así que HP y E no son del todo ajenos; la *paragua* de
Galeotto Cey sí lo es.

- **a. Se mantiene el archivo de `joutai` por D11** y se reescribe su
  `archivada`; `juri` queda como la voz del viento, con la capa que decida la
  pregunta 1. Si hace falta otra, es trabajo de D11 fase 3 (lokono, taíno o
  achagua).
- **b. Desarchivar `joutai`**: dos voces sin atestación compitiendo, y una del
  wayuu. Va contra cc.12.
- **c. Mantener `juri` atestiguada como excepción** porque es la única voz del
  viento. Va contra la regla 2.

**Recomendación: a.** Tampoco se caen: la convivencia `bara`/`kuru` (d21.16:
con B las dos quedan reconstruidas, y el motivo era la sinonimia, no la capa)
ni D9: `-bana` 'cerro' se sostiene sin Esteves (Capubana HB, Guadadubana de
González Batista, el Cerro de Capú de Velasco). Pero la instrucción de `-bana`
—«para la orilla del mar usa `kari`»— y su argumento —«la costa atestiguada es
`kari`»— descansan en una sola línea de Esteves (p. 28), la misma que da
*bana* 'cerro'.

## 4. Pregunta 3 — lo que el prompt enseña

[voces.*.exposicion; por_opcion.*.cambian_y_alguna_plantilla_la_ensena]

- **`kari` está en el EJEMPLO de `IDENTIDAD_LINGUISTICA`** («Taya wana-ka arima
  wara kari»), que leen los 63 cada turno, y en la respuesta ideal de
  `prompt_reglas_completo`. Con A, B o D, el ejemplo de identidad enseñaría una
  voz hipotética: la misma situación que `kali` el 2026-09-19.
- **`waranao`** es ejemplo de verbo estativo en la plantilla completa y en la
  breve (los 63), y su glosa ni siquiera está en Esteves.
- **`bara`** está en NATURALEZA de la completa y en el rescate.
- **`juri`** sale en **42** de los 126 bloques de `[Tu tierra]`: la frase del
  período de viento es «el juri sopla firme del este». Y `jachos` en **14**
  («se untan los jachos…»). El canon del mundo (`clima_era2.yaml`,
  `sitios_era2.yaml`) **copia la capa** en sus `voz_caquetia`: `juri` cinco
  veces, `kari` cuatro, `jachos` tres… — si la capa cambia, esas copias quedan
  mintiendo [cadena.canon_del_mundo_…].

- **a. Cambiar los ejemplos** de `kari` y `waranao` por voces con otra fuente,
  medido antes, como se hizo con `kali`; y actualizar las `voz_caquetia`.
- **b. Dejar los ejemplos** con la capa nueva declarada en la plantilla.

**Recomendación: a**, dentro de la última tanda antes de la corrida base
(cc.12), porque cambia el prompt de los 63 y abre corte de serie.

## 5. Pregunta 4 — los afijos que se enseñan

[afijos]

| afijo | fuera de Esteves | se enseña | usos en la base |
|---|---|---|---|
| `-iro` 'diminutivo' | nada | tier 1 (línea) y los 63 (línea breve) | 408, en 77 formas |
| `-uco`/`-uto` 'quebrada' | nada | ídem | 303, en 61 formas |
| `-ima` 'humedad' | la sigla PMA (Arcaya 1920 da cero; la «confirmación» de van Buurt es Esteves) | ídem | 183 |
| `dito` 'colectivo' | nada | no se enseña | 0 |

`-bana` y `-bakoa` se sostienen. ¿Qué le pasa a un afijo que el prompt enseña
y que deja de ser atestiguado? Tres caminos, medidos:

- **a. Reetiquetarlo y seguir enseñándolo con el rótulo verdadero**: sale de
  `AFIJOS_ATESTIGUADOS` a un grupo propio («lo que Esteves lee en los
  topónimos»), sigue en `TODAS_LAS_REGLAS`. El desafijador y el score no se
  mueven; el prompt cambia en el rótulo.
- **b. Dejar de enseñarlo sin sacarlo del desafijador**: el tier 1 pierde dos
  líneas (94 y 52 caracteres) y la línea breve dos elementos; lo ya dicho
  sigue contando.
- **c. Retirarlo del todo, como `-ko` y `-sha`.** Medido: **reabre el agujero
  de *lumina*.** Sin `-iro` y `-uco` en el desafijador, `lumina-bana-iro` y
  `lumina-bana-uco` —la forma que fijó el cometa en el brazo de control— dejan
  de ser «desconocida» y vuelven a contar como caquetías, porque `bana`
  ('hígado', reconstruida) queda en el núcleo como raíz conocida.

**Recomendación: a.** El diminutivo es justo un *blind spot* (d19.c: lo
reconstruido es para los huecos) y no hay otro; la quebrada tiene `-ima`. La c
queda descartada por lo que rompe.

## 6. Pregunta 5 — los topónimos del canon

[toponimos] De los 26 topónimos A y B, **6** tienen una pieza sólo de Esteves:

| topónimo | hoy | propuesta | por qué |
|---|---|---|---|
| Jurijurebo (001) | A | **C** | juri y ebo sólo de Esteves; la glosa también (#179 (E) = p. 47). La ciudad no se toca: está en Castellanos |
| Cumarebo (004) | A | **C** | #94 (E) = Esteves p. 105 |
| Judibana (075) | A | **B** | bana se sostiene; juri recurre tres veces |
| Carirubana (148) | B | **C** | residuo *-ru-* y además cari sólo de Esteves |
| Abudure (076) | B | B | dabuda (HB) + ure recurrente |
| Buchuhaco (086) | B | B | buche (AM, Alvarado) + «aco: par» recurrente |

- **a.** Aplicar los cuatro cambios en la misma tanda.
- **b.** Sólo de aquí en adelante — es la 1-B del lote, que cc.4 ya descartó.

**Recomendación: a.**

## 7. Pregunta 6 — `jachos`

- **a.** Reasignarla a español, como `caraota` en D10, después de verificar
  «hacho» en el DRAE (fuera del repo).
- **b.** Dejarla hipotética.

**Recomendación: a**, verificada. Es homógrafa de un nombre del elenco: el
agente no cambia, la voz sí.

## 8. Mi recomendación, junta

**1-B, 2-a, 3-a, 4-a, 5-a, 6-a**, todo en la última tanda antes de la corrida
base que cc.12 ya pide (D11 fase 3, coro, poporo, las voces de Zayas), medido
una vez: cambia el prompt de los 63 y re-sortea las semillas derivadas, así que
es corte de serie.

## 9. Lo que queda, y lo que vi de paso

- **Curación de glosas**: `naure` (arriba); `waranaro` es «un pez más pequeño
  que la lisa» en Esteves, no la lisa; `wache` es 'zorro' en Esteves y el coatí
  en Alvarado; `chipare` es 'matapalo' en Esteves y quizá 'piedra' en Arcaya
  1920.
- **Duplicados de D5**: `kapo` (E) y `kapu` (HB) son la misma voz.
- **La misma pregunta vale para la sigla A.** En varias voces E+A lo que
  Alvarado dice es de fuera del área (`kaketillo`: «del Zulia», con
  interrogación). Aquí se contó la sigla como el canon siempre la contó; revisar
  lo que dice Alvarado de cada una es otra campaña.
- **HP (Hill Peña)**: Esteves lo cita (p. 41) y su obra no está en el repo.
- **La skill `campana-toponimos` §2** necesita los desfases de los tomos 4-6
  (+72/+73, +100, +129/+130). No la toqué: lo decide Miguel.
- **`medir_sostiene.py`** no ve a Esteves detrás de la sigla: su ficha dice
  `sostiene: []` mientras sostiene, vía Zavala, 43 voces atestiguadas.
