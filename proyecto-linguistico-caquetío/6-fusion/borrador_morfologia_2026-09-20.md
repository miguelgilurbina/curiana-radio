> ⚠️ **BORRADOR — NO APLICADO.** Así quedaría `2-lengua/morfologia.md` si
> Miguel aceptara las catorce decisiones de
> `6-fusion/issues-pendientes/morfologia-revision-2026-09-20.md` con la
> recomendación de cada una. Vive en `6-fusion/` porque un minador propone y el
> humano fusiona (regla 5). **Todas las cifras salen de
> `6-fusion/medicion_morfologia_2026-09-20.yaml`**, que genera
> `6-fusion/scripts/auditar_morfologia.py`; ninguna está escrita a mano, y al
> fusionar hay que volver a correrlo, no copiar de aquí.
>
> Lo que este borrador da por aceptado, punto por punto: 1→C · 2→A · 3→A ·
> 4→B · 5→C · 6→B · 7→B · 8→A · 9→A · 10→A · 11→C(+A) · 12→A · 13→B · 14→A.

---

---
tipo: nota-viva
ambito: afijos y reglas de formación de palabras
fuente_de_verdad: curiana_sim/curiana_lexicon.py (TODAS_LAS_REGLAS, REGLAS_ZAVALA, REGLAS_ATRIBUTIVAS)
propuestas: [lexicon_van_buurt.py, lexicon_gatschet.py, lexicon_toponimos.py]
medido: 2026-09-20 (6-fusion/scripts/auditar_morfologia.py)
---

# La morfología

> Lo que un agente puede **construir**, no solo nombrar. Cada afijo va aquí con
> **su evidencia y su estado** — porque el proyecto mezcló durante mucho tiempo
> afijos atestiguados con afijos de trabajo, sin marcar la diferencia, y eso
> contamina hacia adelante: los agentes acuñan neologismos con ellos en cada run.
>
> **Y desde el 2026-09-20 va también con lo que le falta.** La auditoría de esa
> fecha midió que nueve de los 21 morfemas del motor se apoyan sólo en el
> andamio wayuu/lokono que D11 mandó retirar, y que un sistema arahuaco tiene
> rasgos —clases de verbo, no-poseído, género— que éste no tiene. Declarar un
> hueco es parte de describir el sistema.

## El orden básico

```
pronombre + verbo-aspecto + complemento
Pronombres: taya (yo) · pia (tú) · nüma (él/ella) · waya (nosotros) · naya (ellos)
            + el registro FORMAL atestiguado: kudanga (usted) · kuté (a usted)
Neologismo: [forma: componentes = significado]
```

Los cinco primeros son **reconstruidos desde el wayuu** y son deuda de D11
fase 3. Los dos últimos son **caquetío atestiguado** con cita
([[zavala-reyes-2015]] p. 73, vía Arcaya: *«chacamba cudanga»* ¿cómo está
usted?, *«cudan de cuté»* para servir a usted) y entran al habla por la
política «manda la atestiguada» del 2026-09-19. No compiten con `pia`: se
reparten el registro, y la era 2 tiene jerarquía escrita para usarlos.

> **Corrección al §«manda la atestiguada» de [[lexicon]]**: la frase «los
> pronombres no tienen rival atestiguado» no era exacta. Para la segunda
> persona sí lo hay, sólo que en registro formal — y por eso el caso no lo
> dispara la política (la glosa no es idéntica) sino una decisión aparte.

## 0. Cómo se lee este inventario

Cada morfema lleva cuatro cosas, y la cuarta es la que costó una auditoría
entera:

1. **forma** y **función declarada**;
2. **capa epistémica** — atestiguado / reconstruido / canon-simulación /
   retirado;
3. **apoyo con cita**, que es una **clave foránea** a
   `4-fuentes/bibliografia.yaml` (regla 8). Lo que no la tiene lleva
   `deuda: sin-procedencia` escrito;
4. **dónde lo enseña el motor** — en qué plantillas aparece y por qué puertas
   del scorer pasa. Un morfema que el prompt enseña y el canon no declara es
   un error que se propaga en cada run; lo aprendimos tres veces en un día
   (`kali-bana`, el molde `X-bana`, la vía mala del viento).

## 1. Afijos atestiguados — `REGLAS_ZAVALA` y `REGLAS_TOPONIMICAS`

Documentados en el glosario de [[zavala-reyes-2015]] con su cita literal en el
campo `atestiguado`, más un formante toponímico de fuera de Zavala.

| Afijo | Valor | Cita |
|---|---|---|
| `-iro` | **diminutivo** — la única marca de diminutivo documentada | Zavala #166 (E): *"desinencia que se usa en diminutivo"* |
| `-aima` | abundancia (variante `-coa` en topónimos) | Zavala #6 (AM+PMA): *"desinencia que significa abundancia"* |
| `-ima` | humedad / quebrada | Zavala #165 (E+PMA): *"desinencia que significa humedad, quebrada"* |
| `-uco` | cauce, quebrada (**variante `-uto`, declarada**) | Zavala #268 (E): *"sufijo. Quebrada, cauce"* |
| `-ubana` | desinencia, **valor no precisado por la fuente** | Zavala #265 (AM) |
| `-uru` | desinencia, **valor no precisado por la fuente** | Zavala #274 (AM) |
| `-bakoa` | bosque, arboleda; paraje cubierto de | `morfemas.yaml` morfema-001 (Esteves 1989, cinco topónimos glosados) + [[alvarado-1921]] `-baca` vía [[van-buurt-2014]] §10 |

> `-ubana` y `-uru` son honestos precisamente por lo que **no** dicen: Zavala
> los registra como desinencias de la lengua sin darles valor semántico, y el
> proyecto no se lo inventó. Ese es el patrón a seguir en todo lo demás — y
> desde el 2026-09-20 es también el patrón de `-ana` (§3).

`-ima` tiene **corroboración independiente**: [[van-buurt-2014]] §10 lo
documenta como 'húmedo, mojado' (forma `nima`) vía Cruz Esteves 1989, en el
topónimo *Onima* de Bonaire. Dos fuentes que no se citan entre sí, misma glosa.

> **D5 aplicada a la morfología** (2026-09-20). El afijo se escribe con el
> **lema fonémico**, no con la grafía colonial: `-bakoa`, no `-bacoa`. Es la
> misma decisión del 2026-08-31 —«la grafía española es grafía; el lema
> fonémico es la palabra»— llegando a la tabla que se le había quedado fuera.
> El lexicón ya tenía `bakoa` atestiguado con `k`, y la regla enseñaba un
> derivado (`adabacoa`) que no existe en `VOCABULARIO_BASE` con ninguna
> grafía. Al migrar la clave cambia `_SUFIJOS_CAQ` y con él `nucleo_de_token()`:
> es corte de serie, y va medido.
>
> **`-uto`** dejó de ser un fantasma del prompt: aparecía dentro del campo
> `uso` de `-uco` y por tanto se enseñaba, pero no estaba en
> `TODAS_LAS_REGLAS` y el desafijador no lo conocía. Ahora está declarado como
> variante.

## 2. Reglas de trabajo del proyecto

`REGLAS_ASPECTO`, `REGLAS_LOCATIVAS`, `REGLAS_POSESIVAS`, `REGLAS_ATRIBUTIVAS`,
`REGLAS_NUMERO`. **La mayoría se apoya en cognados wayunaiki, no en dato
caquetío** — lo declaran ellas mismas en un campo `wayunaiki`, que es lo
correcto, pero conviene leerlo como lo que es: **nueve de los 21 morfemas del
motor no tienen otra cosa detrás**, y **doce no tienen ninguna clave foránea a
la bibliografía**.

| Afijo | Valor | Base | Capa |
|---|---|---|---|
| `-ka` | completivo | WY tríada A en contexto de pasado | reconstruido · `deuda: sin-procedencia` |
| `-ni` | continuativo | WY `-iraa` | reconstruido · `deuda: sin-procedencia` |
| `-da` | prospectivo / intencional | WY `-ee` desiderativo + tríada C | reconstruido · `deuda: sin-procedencia` |
| `ta-` / `wa-` | posesivo 1ª sg / pl | WY `ta-` / `wa-`, cognados directos; `wa-` además [[van-buurt-2014]] §6 (de Goeje 1928) | reconstruido (`wa-` con apoyo insular) |
| `ka-` | **atributivo / existencial** — 'hay X, tiene X' | [[van-buurt-2014]] §8 (*Casibari* = 'hay rocas duras'); par mínimo lokono en [[perea-alonso-1942]] p. 555 | **atestiguado** |
| `ma-` | **privativo** — 'sin X, no X' | par mínimo con `ka-` ([[perea-alonso-1942]] p. 555: `k-ere-u-ti` casado / `m-ere-u-ti` soltero); WY `ma-` cognado | **atestiguado** |
| `-kana` | plural colectivo | WY `-kana` | reconstruido desde el wayunaiki · `deuda: sin-procedencia` |
| `-ana` | formante toponímico, **sin glosa** (#109, 2026-09-07) | ver §3 | atestiguado, sin valor |
| `-gua` | región, área amplia | topónimos de Falcón y Sucre | reconstruido · `deuda: sin-procedencia` |
| `-bana` | **'cerro, sitio alto'** — D9 resuelta 2026-08-31, seis apoyos | ver §3 | **atestiguado** |

### `ka-` y `ma-` ya no son posesivos

**Es el cambio de fondo de la revisión de 2026-09-20.** `ka-` vivía en
`REGLAS_POSESIVAS` con el nombre «posesivo genérico / asociativo» y el prompt
lo enseñaba como `ka-biro = el salinero` — una persona. En [[van-buurt-2014]]
§8 es un **localizador**: *Casibari* = «hay rocas duras», `ka-` + `siba`
'piedra' + `rí` 'duro'. Y [[perea-alonso-1942]] p. 555 da el par mínimo
completo contra el privativo `m-`.

Están ahora en su propia tabla, `REGLAS_ATRIBUTIVAS`, y el prompt enseña
`ka-biro` = **'hay sal, el sitio tiene sal'** junto a `ka-maure`. Las claves no
cambian, así que el desafijador devuelve exactamente lo mismo.

> **Por qué importa, medido.** `ka-` y `ma-` juntos suman 2.759 usos contra
> 6.843 de `ta-` solo: el mecanismo arahuaco bueno para **predicar un nombre**
> estaba escondido dentro de la tabla de posesivos y se usaba muchas menos
> veces que el posesivo de primera persona. El caso que lo destapó fue el
> viento: los agentes conjugaban `juri-ni` —tratando un nombre como verbo—
> teniendo `ka-juri` 'hay viento' disponible y sin enseñar.

### Las clases de verbo: **estativo** y **de acción**

Hasta el 2026-09-20 el lexicón tenía **una sola clase verbal** (`cat: v_raiz`)
y once adjetivos. Un sistema arahuaco no funciona así:

> [[perea-alonso-1942]] pp. 634-640 — la **4ª conjugación lokono** es la de los
> estativos: colores, tamaños, sabores, estados. `cule-n` 'ser rojo', `ibe-n`
> 'estar lleno', `hebbe-n` 'ser viejo'. Y pp. 598-599, la regla de Quandt que
> Perea recoge: cualquier nombre o adjetivo se hace verbo con `a-` o `c-`.
> «"Rojo" no es un adjetivo en lokono: es el verbo "ser rojo"».

**Los agentes lo descubrieron antes que nosotros.** La medición encontró **484
usos de aspecto sobre raíz no verbal**, de los que 143 son sobre adjetivo (111
con `-ni` y 32 con `-da`): `siwato-ni` 'está desganado', `tüshi-da`,
`ma-siwato-ni`, `kasuta-bana-iro`. Es la conjugación estativa reinventada desde
el uso.

Desde entonces el lexicón distingue **estativo** y **de acción**, y el prompt
dice que un estado se predica con aspecto igual que una acción. **No se importó
el alineamiento** —el lokono pone el pronombre detrás en los estativos
([[perea-alonso-1942]] pp. 635 y 652)— porque eso sería traer un paradigma
entero de la hermana cuya filiación D11 dejó abierta. Queda disponible si D11
fase 3 se resuelve hacia el lokono.

> ⚠️ El reparto concreto de las raíces de Zavala en estativo / acción / nombre
> se hizo en la tanda de clasificación de las 49 que la heurística de
> `minar_zavala_glosario.py` había marcado `v_raiz` de una pasada. Esa
> clasificación es lo que esta sección da por hecho; antes de ella, `juri`
> 'viento' era un verbo.

### El alcance de D11 fase 3

> **Medido el 2026-09-08 y confirmado el 2026-09-20.** Las tres marcas de
> aspecto —`-ka`, `-ni`, `-da`— salen **enteras** del wayunaiki. Así que
> «declarar la etiqueta del núcleo reconstruido» (la fase 3 de D11, abierta)
> no afecta sólo a la Capa 2 léxica: **afecta al sistema morfológico completo**
> — aspecto, posesión y número, que son nueve de los 21 morfemas.
>
> Las tres tienen homógrafo en lokono con otro valor declarado —`-ca` es ahí la
> raíz del verbo *ser/estar*, `-ni` el auxiliar `a-ni-n`, y `-da/-dda` la
> partícula del presente que ni Perea ni Goeje saben explicar—, pero **eso no
> se afirma como cognación**: son formas de dos letras, y medir parecido en
> formas así es lo que produjo el 80 % de fallo de las 441 hipotéticas.
> Detalle y páginas en `6-fusion/lokono_gramatica_perea_1942.yaml` §verbo.
>
> Y la pregunta directa, contestada: **¿hay algo atestiguado del caquetío que
> sostenga las tres marcas? No.** La sonda —entradas `caquetío-atestiguado`
> que sostengan `-ka`, `-ni` o `-da`— da cero en las tres.

> **Añadido el 2026-09-12.** Los paradigmas completos (pp. 609-684) están
> vaciados en el mismo YAML, §`verbo_paradigmas`. El futuro lokono de Schumann
> es **`-pa`**, con paradigma (`d-a-iyaha-ddi-pa` 'andaré'); el prospectivo
> `-da` del canon sale del wayuu `-ee`. No se afirma cognación entre ambos —
> se anota para la fase 3 de D11: si el núcleo se re-deriva desde el lokono,
> el futuro tiene forma atestiguada. Y el lokono tiene **dos juegos de
> pronombre sujeto**: prefijado en los transitivos (`d-a-`, `b-a-`…) y
> pospuesto en estativos y negativos (`de`, `bu`, `i`, `n`, `u`, `hu`, `ye`).

### `-kana` y `-naiki`, corregidos

`-kana` declaraba *«COGNADO DIRECTO con Caquetío»* y **no había forma caquetía
detrás**: la única clave de familia caquetía terminada en `-kana` es `sakana`
'ofrenda', **hipotética**; `2-lengua/toponimos.yaml` da cero; y la `kana`
atestiguada de Zavala (#57) es un lema, 'demonio'. La afirmación se bajó a
**reconstruido desde el wayunaiki**, deuda D11 como los tres aspectos. La
forma se queda: quitar el plural dejaría a los agentes sin forma de decir «los
ancianos», y el dato lokono en contra —el plural es `-nu` pospuesto y **los
irracionales no distinguen número**, [[perea-alonso-1942]] p. 556— es de otra
lengua.

**`-naiki` se retiró** a `REGLAS_RETIRADAS`, junto a `-ko` y `-sha` y por la
misma razón que aquéllos: sin fuente, y era convención. Su apoyo escrito era
literalmente el nombre de la lengua andamio (`wayuunaiki`) y su único ejemplo
también. En 95.445 usos de `word_uses` **nadie lo dijo nunca**, y ninguna
plantilla lo enseñaba: retirarlo no movió ningún score.

### Los ejemplos ya no enseñan wayuu

Tres reglas formaban plural y gentilicio **con la lengua que
`IDENTIDAD_LINGUISTICA` declara «tan ajena para ti como el español»**
(`wayuu + kana = wayuukana`, `wayuu + naiki = wayuunaiki`) y una enseñaba una
forma archivada (`piache + kana`, retirada por D10 en 2026-08-03). No llegaban
al prompt —`prompt_afijos_atestiguados()` sólo renderiza `REGLAS_ZAVALA` y
`REGLAS_TOPONIMICAS`— pero eran lo que leía quien viniera detrás. Reescritos
con formas del lexicón, que es lo que el propio módulo ya se había anotado
para `paa-ka`: *una referencia muerta aquí es deuda igual*.

## 3. `-bana` vs. `-ana` — resueltos, cada uno a su manera

Es la decisión **D9**:
[#38](https://github.com/miguelgilurbina/curiana-radio/issues/38), y su
continuación [#109](https://github.com/miguelgilurbina/curiana-radio/issues/109).

### El problema, tal como fue

El proyecto enseñaba a los agentes, **desde el día 1 y sin ninguna cita**, que
`-bana` significa *'orilla, borde, límite'*. Era productivo: cada run generaba
neologismos con él. Si la glosa está mal, cada run propaga el error.

| Fuente | Glosa de `-bana` | Evidencia |
|---|---|---|
| El proyecto (hasta 2026-08-31) | 'orilla, borde' | **ninguna** |
| [[van-buurt-2014]] §8 | **'ancho, llano'** | *Hudishibana* = 'llano ventoso' (`hudi` viento) |
| [[van-buurt-2014]] §6, vía Oliver | **'cubierto'** | *wakaubana* = 'cubierto por lo subterráneo' |

Las **tres palabras atestiguadas** del lexicón que terminan en `-bana` le daban
la razón a van Buurt y no al proyecto: `kabana` 'sabana' (un llano ancho, no
una orilla), `darubana` 'camino' (una franja llana, no un borde), `kapubana`
'duende del cerro'. [[gatschet-1885]] aporta cuatro topónimos arubanos con el
afijo — *Shiribana, Tarabana, Wakubana, Bushiribani*.

### Y sin embargo `-bana` también existe

No es que `-bana` sea un error de segmentación de `-ana`. **La reduplicación lo
prueba**: existen *Shiribana* (Aruba) y *Shishiribana* (Bonaire) — el mismo
topónimo, con y sin reduplicación de la sílaba inicial. Si la raíz es `shiri` y
se reduplica a `shishiri`, lo que queda detrás es `-bana` entero, no `-ana`.
Los dos afijos coexisten.

### El estado

- **`-bana`** = **'cerro, sitio alto' — RESUELTO y atestiguado** (D9/#38,
  2026-08-31). Seis apoyos convergentes: Zavala #26 «Bana (E): Sitio, cerro
  alto» (lema directo), la composición contigua `kapu` #60 + `kapubana` #61
  'duende **del cerro**', González Batista usándolo como establecido
  (*Guadadubana* = 'el cerro de las cañas'), el lazo referencial del dueño Capo
  en el cerro de Santa Ana — que **se llamaba Cerro de Capú** ([[velasco-2015-resistencia]]),
  *Judibana* = 'cerro del viento', y las dos fuentes de van Buurt. Contra
  'orilla': cero — y `kari` #66 'orilla del mar' ya cubre ese campo. Es
  **homónimo declarado** de `bana` 'hígado' (reconstruido por cognado lokono).

  ⚠️ Las formas que no encajan **no se forzaron**: `kabana` 'sabana' (probable
  préstamo castellano), `darubana` 'camino', `guacaubana` 'río escondido'
  quedan como segmentación dudosa o polisemia pendiente — la lectura
  'ancho/llano' de van Buurt sigue viva **para ellas**, registrada. Y
  [[perea-alonso-1942]] añade el lado lokono con atestaciones: `u-banna`
  'sobre, encima, la superficie de' (`SURA u-banna` = la azotea), que queda
  **más cerca del 'ancho, llano' de van Buurt que del 'cerro' de D9**. No
  derriba D9; tampoco lo refuerza, y presentarlo como refuerzo sería leer hacia
  la conclusión que conviene.

  > **Lo que la medición añade en 2026-09-20**: `-bana` es el locativo más
  > productivo (2.323 usos, 254 formas, 149 raíces) y **886 de esos usos van
  > sobre una raíz que no está en el lexicón** — `lumina-bana`, `kali-bana`
  > (archivada), `karu-bana`, `suave-bana`. Es el molde del corte del
  > 2026-09-19 visto desde el otro lado: la puerta de la raíz de ninguna parte
  > cierra la forma, y este número dice cuánto había detrás.

- **`-ana`** — **forma atestiguada, SIN GLOSA** (#109, decisión B de Miguel,
  2026-09-07; y desde el 2026-09-20 también **en el prompt**). Es
  `morfema-011` en `morfemas.yaml`, formativo sin valor declarado, con lista
  viva de casos en `6-fusion/censo_ana_esteves_109.yaml` (Paraguaná, Curiana,
  Chamuriana, Cujicana, Jayana, y el Coria-na wanebucán de Oliver p. 207).

  Hasta el 2026-09-20 el motor lo conservaba con glosa 'lugar de' como
  **convención de la simulación**, y las dos plantillas la enseñaban — o sea
  que el prompt decía algo que el canon había retirado, escrito y todo en el
  propio campo `evidencia` de la regla. Ahora se enseña **como se enseñan
  `-ubana` y `-uru`**: *desinencia atestiguada cuyo valor nadie anotó; puedes
  usarla si propones su valor entre corchetes*. Es el patrón que el proyecto ya
  había elegido para ese caso exacto, respeta #109 sin borrar un formante
  atestiguado, y **abre** la posibilidad de que los agentes propongan la glosa
  — que es para lo que existe esta simulación.

  *Paraguana* dejó de ser su apoyo: la fuente imprime **Paraguaná** con tilde,
  la glosa «Rodeada del mar» no despeja con 'lugar de', y existe la
  segmentación alternativa `para` + `gua` 'terreno cercado' + `ná` (los tres
  atestiguados en Zavala #190/#122/#184). **Censo hecho el 2026-09-07**: de las
  13 formas en -ana del índice de Esteves, 6 son `-bana`, 1 es `-bana` con h
  (Capuhana), 2 llevan el -ana dentro de una raíz léxica, y 4 van sin glosa.
  **Ninguna glosada 'lugar de'**: el 'lugar' de Esteves es `bacoa`.

  > Una nota comparativa, con su cautela: el lokono **sí** forma nombres de
  > lugar e instrumento con un sufijo `-na`, casi siempre sobre la partícula
  > durativa `-coa-` — `a-balti-coa-na` 'asiento', `diki-kua-na` 'espejo'
  > ([[perea-alonso-1942]] p. 561). Es evidencia de una lengua hermana, **no
  > evidencia sobre el caquetío**, y el propio Perea avisa de que *«son pocos
  > los vocablos así formados»*. Lo que aporta es que la hipótesis retirada no
  > era absurda: era insostenible **con el dato caquetío**.

> El mismo patrón se repite en `-are` vs `-ure`: la evidencia toponímica dice
> 'sitio de' (cinco apoyos, `dabudare` como caso decisivo), van Buurt §5 dice
> 'raíz'. Ver [[toponimia]] §conflictos. **Es la próxima D9 y sigue abierta.**

## 4. La reduplicación

[[gatschet-1885]] afirma que varios topónimos arubanos se forman **duplicando la
raíz disílaba**, para onomatopeya, diminutivo o pluralidad.
[[perea-alonso-1942]] p. 679 lo confirma del lado lokono como *«recurso
frecuente en nuestro Arawak»* que Schumann ni menciona: `a-sucusu-n` 'lavar' →
`a-sucu-sucu-n` 'bautizar'. F11 lo **midió** (`REDUPLICACION` en
`lexicon_toponimos.py`), con el mismo detector aplicado a todos los corpus:

| Corpus | Formas con unidad reduplicada | Tasa |
|---|---|---:|
| **Toponimia caquetía** | 26 de 287 | **9,0 %** |
| **Léxico caquetío** | 9 de 210 | **4,3 %** |
| control wayunaiki | 22 de 703 | 3,1 % |
| control lokono | 1 de 138 | 0,7 % |
| control taíno | 0 de 40 | 0 % |

**Es productiva, y no es un artefacto del método**: el detector es el mismo
para todos y el caquetío está claramente por encima de sus hermanas.

Valores medidos:

- **Onomatopeya (fauna) — dominante.** 7 de las 9 reduplicaciones léxicas son
  animales, 5 de ellas aves: `warawara`, `chuchubi`, `chuchube`, `querequere`,
  `humohumo`, `chogogo`, `tuqueque`.
- **Pluralidad / abundancia — sostenido.** `jurijurebo` 'Paso de los **vientos**'
  ← `juri` 'viento' (singular en el lexicón, **plural en la glosa**). Y el par
  *Shiribana* / *Shishiribana*.
- **Intensidad — plausible, sin glosa que lo pruebe.** `barabara` 'árbol de
  madera **dura**' ← `bara` 'árbol'.
- **Diminutivo — sin apoyo.** Gatschet lo menciona; **ni un solo caso del corpus
  lo sostiene**. El diminutivo caquetío documentado es afijal: `-iro` (Zavala
  #166) y `-bi` ([[van-buurt-2014]] §6, sin incorporar). *Aquí el dato
  contradice a la fuente y hay que decirlo.*

Advertencia de uso: el valor onomatopéyico es **formación léxica histórica**, no
morfología viva. Un agente no debería reduplicar para inventar un ave. El valor
de pluralidad sí es candidato a regla productiva.

> ⚠️ **Deuda abierta, y de las que escuecen.** Es el único rasgo que el
> proyecto ha **medido con control** y **no ha llevado al motor**: no se
> enseña, no se reconoce al puntuar, no hay regla. La auditoría del 2026-09-20
> lo dejó en la patología (b) —lo que el canon declara y el scorer no ve— y la
> decisión de si la regla productiva de pluralidad entra es de Miguel.

## 5. Lo que un sistema arahuaco tiene y éste no

*(Sección nueva, 2026-09-20. Declarar el hueco es parte de describir el
sistema; callarlo es lo que la regla 8 prohíbe para las fuentes y vale igual
para la gramática.)*

| Rasgo | Qué dice la comparanda | Qué hace este sistema |
|---|---|---|
| **Alineamiento** | [[perea-alonso-1942]] pp. 635 y 652: **dos juegos** de pronombre — prefijado `d-a-, b-a-, l-a-…` en transitivos, pospuesto `de, bu, i, n, u, hu, ye` en estativos y negativos | **Un solo juego**, sin alineamiento. Declarado, no importado (ver §2, clases de verbo) |
| **Posesión no-poseída** | [[perea-alonso-1942]] p. 587: índice absoluto `u-`/`ù-` — `u-si-kua-hù` = *LA casa, sin poseedor*; y posesivos absolutos `da-kía` 'mío' (p. 586) | **Importado**, porque el hueco era funcional: sin él un agente no tiene cómo nombrar una cosa sin dueño, y `ta-` está a mano — 6.843 usos sobre 258 raíces |
| **Género / clases** | [[perea-alonso-1942]] p. 554: no hay género, hay **varonil / no varonil**, sufijos `-ti/-tti` vr. y `-tu/-ttu` nv., `-nu` plural común. Los achagua de [[neira-ribero-1762]] cambian el numeral según lo que cuentan | **Hueco declarado, y a propósito.** No hay ni un dato caquetío de género, y la distinción arrastra una cosmovisión entera: importarla es lo que la regla 4 prohíbe. Además el proyecto acaba de pasar por eso al retirar `-ko`/`-sha`, que era un género inventado |
| **Número de los irracionales** | [[perea-alonso-1942]] p. 556: `keyu` 'venado, venados', `siba` 'piedra, piedras', `adda` 'árbol, árboles' — los irracionales **no distinguen número** | **Hueco declarado.** `-kana` se aplica a todo. Es un dato precioso y de otra lengua: se anota y se espera |
| **Nominalización** | [[perea-alonso-1942]] pp. 609-612: nombre de acción `-hù` (`a-iyaha-dda-hù` 'andadura'), `-hi` en los estativos (`c-a-nsi-hi` 'amor'), participios `-ti/-tu/-nu`, agentivo `-ha-li-n` | **No hay regla — y la comunidad la inventó**: 1.132 usos de prefijo posesivo o atributivo sobre raíz verbal (`ta-chaa` 'mi hacer', `wa-jai` 'nuestro oír', `ma-awa` 'sin beber'). Declarado como lo que es. Campaña de retroabstracción abierta para buscarle forma atestiguada a la manera de `matakán` |
| **Reduplicación** | [[gatschet-1885]] y [[perea-alonso-1942]] p. 679 | Medida (§4), no implementada |
| **Segundo diminutivo `-bi`** | [[van-buurt-2014]] §6: *gobí, gogorobí, kokorobí, lobi, makambí* | En `MORFEMAS_VAN_BUURT`, sin adjudicar |

## 6. La gramática que la comunidad escribió sola

**Ninguna regla del proyecto declara apilamiento de afijos**: los quince campos
`uso` de `TODAS_LAS_REGLAS` son de UN afijo sobre UNA raíz. Los agentes
apilaron igual. La medición del 2026-09-20 encontró **57 patrones distintos,
988 usos, 273 formas**, y hasta cuatro slots en una palabra:

| secuencia | usos | formas | ejemplos |
|---|---:|---:|---|
| RAÍZ + locativo + aspecto | 300 | 35 | `chaa-bana-ni`, `biro-ana-da`, `juri-bana-ni` |
| RAÍZ + locativo + derivativo | 151 | 19 | `kasuta-bana-iro`, `siwato-bana-uco` |
| RAÍZ + **aspecto + aspecto** | 130 | 48 | `chaa-da-ka`, `chaa-ni-da`, `jai-ni-da` |
| posesivo + RAÍZ + locativo | 114 | 35 | `ka-biro-ana`, `ma-arua-bana`, `ta-kali-bana` |
| RAÍZ + **locativo + locativo** | 53 | 20 | `awa-bana-gua`, `kapu-bana-gua`, `kono-ana-gua` |
| RAÍZ + **derivativo + derivativo** | 39 | 4 | `biro-uco-aima`, `kati-iro-ubana` |
| posesivo + RAÍZ + locativo + aspecto (**cuatro slots**) | 8 | 7 | `ta-chaa-bana-ni` |
| posesivo + RAÍZ + derivativo + derivativo (**cuatro slots**) | 7 | 4 | `ka-biro-uco-aima`, `wa-biro-uco-aima` |

**Se declara que el apilamiento es libre y que el orden no está fijado.** No se
enseña un orden de plantilla, y es una decisión, no un descuido: fijarlo
convertiría un hallazgo en una instrucción y haría circular la medición — el
mismo error que enseñar `kali-bana` y luego contarla como acuñación de la
comunidad.

Dos lecturas que conviene tener escritas:

- **`awa-bana-gua`, `kono-ana-gua`** componen *lugar dentro de región*, que es
  exactamente lo que invita la propia jerarquía declarada («`-gua`: menos
  específico que `-ana`») y que nadie autorizó.
- **`chaa-ni-da`** («lo está haciendo y lo va a hacer») no es obviamente
  agramatical en un sistema de aspecto sin tiempo. Llamarlo error sería una
  afirmación sobre una lengua que no tenemos.

## 7. Qué reconoce el motor al puntuar

Una cosa es enseñar un morfema y otra contarlo. Las puertas son cuatro, y
conviene saber cuál es cuál:

| Puerta | Qué hace | Quién entra |
|---|---|---|
| `_PREFIJOS_CAQ` / `_SUFIJOS_CAQ` | el desafijado de `nucleo_de_token()` y `_familia_de_token()`: dice dónde acaba la raíz | los 18 afijos activos de `TODAS_LAS_REGLAS` |
| `_AFIJOS_SUELTOS` | un afijo escrito suelto cuenta como palabra caquetía | los mismos, sin guion |
| `_aspectos_morfologicos()` | hasta **2 de los 10 puntos** del score | `-ka`, `-ni`, `-da` sobre raíz verbal **caquetía** |
| `es_arahuaco()` | densidad arahuaca, el 60 % del score | prefijo posesivo + raíz activa, y raíz verbal caquetía |

Dos correcciones del 2026-09-20 viven aquí:

1. **`_RAICES_VERB` ya filtra por lengua.** Se construía con todas las claves
   `cat: v_raiz` de `VOCABULARIO_BASE` **sin mirar la fuente**, y de sus 1.424
   claves **1.351 no eran caquetías** (1.078 proto-arahuaco, 273 lokono).
   `es_arahuaco()` devolvía `True` para cualquier token cuyo primer segmento
   estuviera ahí. Es la misma clase de agujero que el `return "caquetío"` del
   2026-09-20, en otra puerta.
2. **El comodín de longitud está acotado.** El detector aceptaba
   `-ka/-ni/-da` sobre cualquier raíz con guion de tres letras o más, sin
   verbo de por medio: **20.165 de las 62.347 detecciones** de toda la base
   entraban por ahí (`hamaka-chaa-ni`, `kali-barsure-da`, `baro-ni`). Ahora
   cuenta si el **último segmento antes del aspecto** es raíz verbal, que es el
   caso bueno que el comodín cubría a ciegas.

> ⚠️ **EL COMPONENTE DE ASPECTO ESTÁ SATURADO.** Media de 1,9982 puntos por
> respuesta sobre un máximo de 2,0. El 20 % del score **no separa a nadie** —
> es la misma trampa que `pct_caquetio` (issue #69) en otro quinto de la
> métrica. Tapar el comodín es correcto y **no arregla la saturación**: la
> mueve a 1,9296. **No uses el aspecto para comparar agentes.** Rediseñar el
> peso es otra decisión y tiene que pasar por `5-experimento/disenos/`.

## 8. Morfemas propuestos, aún no incorporados

Tres módulos emiten propuestas que **`curiana_lexicon.py` no importa**. Están
para revisión humana, no en el habla.

### `MORFEMAS_VAN_BUURT` — 19 morfemas (`lexicon_van_buurt.py`)

Afijos: `-ima` 'húmedo' · `-ure`/`-huri` 'raíz' · `-bana` 'ancho, llano' ·
`-apana`/`-pana` 'hoja' · `-bi` **segundo diminutivo** · `wa-` pluralidad ·
`ka-` 'hay, existe' · `-ato` parentesco · `-baca` 'matorral, espesura' ·
`-utu` 'pez'.
Raíces: `bara`/`bari` 'árbol' · `bala` 'mar' · `cari` 'costa, orilla' ·
`abo` 'lugar' · `tabo` 'confluencia' · `siba`/`quiba` 'piedra' · `rí` 'duro' ·
`hudi`/`juri` 'viento' · `waka` 'subterráneo'.

Dos de ellos resolvieron entradas del lexicón que estaban sin cita: `cari`
'costa, orilla' y `waka` → `sawaka` 'inframundo'. **Y uno se incorporó el
2026-09-20**: el `ka-` 'hay, existe' de §8, que es el que corrigió la función
declarada del prefijo (§2).

### `AFIJOS_EN_TOPONIMOS` — el control de Gatschet (`lexicon_gatschet.py`)

Cruza los seis afijos de `REGLAS_ZAVALA` contra los 31 topónimos arubanos de
[[gatschet-1885]], que **no llevan glosa**. Es un control de **forma**, no de
significado: dice dónde aparece cada afijo, no qué quiere decir.

`-aima`: *Kibaima* · `-ubana`: *Wakubana* · `-uru`: *Shabururi, Warerukuri,
Antikuri, Kamakuri, Wariruri, Weburi* · `-bana`: *Shiribana, Tarabana,
Wakubana, Bushiribani* · `-iro`, `-ima`, `-uco`: **cero apariciones**.

Que `-iro`, `-ima` y `-uco` no aparezcan en Aruba no los invalida: son afijos
continentales con cita propia en Zavala.

### `MORFEMAS_DESPEJADOS` — 6 morfemas de la toponimia (`lexicon_toponimos.py`)

Despejados de ecuaciones bilingües; el método está en [[toponimia]].

| Morfema | Glosa | Estado | Recurrencia |
|---|---|---|---:|
| `-bakoa` | bosque, arboleda | **incorporado** al motor (2026-09-14; migrado al lema fonémico 2026-09-20) | 5 |
| `-are` | 'sitio de' (locativo) | **abierto** — glosa en disputa con el `-ure` de van Buurt. La próxima D9 | 5 |
| `ada-` | árbol | **nuevo**, con cognado lokono `ada` | 2 |
| `bari-` | rojizo, turbio | reagrupado | 2 |
| `yacare` | pueblo, poblado | **nuevo** | 2 |
| `wa-` | pluralidad / 'tener' | corroborado; incorporado como posesivo | 2 |

Y cuatro **sin glosar** que el scorer no ve: `-shi`/`-chi` (22 apariciones,
**el formante más frecuente del corpus insular y nadie lo ha glosado** — el
objetivo nº 1 de cualquier minería futura de toponimia ABC), `-ari`/`-ri` (7),
`-kuri`/`-curi` (3) y `-bari` (3, que `INDICE_FUENTES` ya concluyó que **no es
afijo**).

## Enlaces

[[lexicon]] · [[toponimia]] · [[metodo-comparativo]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) · [[zavala-reyes-2015]] · [[van-buurt-2014]] · [[gatschet-1885]] · [[perea-alonso-1942]] · [[neira-ribero-1762]] · [[03_descomposicion_toponimica]]
