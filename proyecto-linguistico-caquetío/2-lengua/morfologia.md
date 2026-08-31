---
tipo: nota-viva
ambito: afijos y reglas de formación de palabras
fuente_de_verdad: curiana_sim/curiana_lexicon.py (TODAS_LAS_REGLAS, REGLAS_ZAVALA)
propuestas: [lexicon_van_buurt.py, lexicon_gatschet.py, lexicon_toponimos.py]
medido: 2026-08-04
---

# La morfología

> Lo que un agente puede **construir**, no solo nombrar. Cada afijo va aquí con
> **su evidencia y su estado** — porque el proyecto mezcló durante mucho tiempo
> afijos atestiguados con afijos de trabajo, sin marcar la diferencia, y eso
> contamina hacia adelante: los agentes acuñan neologismos con ellos en cada run.

## El orden básico

```
pronombre + verbo-aspecto + complemento
Pronombres: taya (yo) · pia (tú) · nüma (él/ella) · tayamaa (nosotros)
Neologismo: [forma: componentes = significado]
```

## 1. Afijos atestiguados — `REGLAS_ZAVALA`

Seis afijos documentados en el glosario de [[zavala-reyes-2015]] que al proyecto
le faltaban. Están en `REGLAS_ZAVALA` con su cita literal en el campo
`atestiguado`.

| Afijo | Valor | Cita |
|---|---|---|
| `-iro` | **diminutivo** — la única marca de diminutivo documentada | Zavala #166 (E): *"desinencia que se usa en diminutivo"* |
| `-aima` | abundancia (variante `-coa` en topónimos) | Zavala #6 (AM+PMA): *"desinencia que significa abundancia"* |
| `-ima` | humedad / quebrada | Zavala #165 (E+PMA): *"desinencia que significa humedad, quebrada"* |
| `-uco` | cauce, quebrada (variante `-uto`) | Zavala #268 (E): *"sufijo. Quebrada, cauce"* |
| `-ubana` | desinencia, **valor no precisado por la fuente** | Zavala #265 (AM) |
| `-uru` | desinencia, **valor no precisado por la fuente** | Zavala #274 (AM) |

> `-ubana` y `-uru` son honestos precisamente por lo que **no** dicen: Zavala
> los registra como desinencias de la lengua sin darles valor semántico, y el
> proyecto no se lo inventó. Ese es el patrón a seguir en todo lo demás.

`-ima` tiene **corroboración independiente**: [[van-buurt-2014]] §10 lo
documenta como 'húmedo, mojado' (forma `nima`) vía Cruz Esteves 1989, en el
topónimo *Onima* de Bonaire. Dos fuentes que no se citan entre sí, misma glosa.

## 2. Reglas de trabajo del proyecto

Las de `curiana_lexicon.py`: `REGLAS_LOCATIVAS`, `REGLAS_POSESIVAS`,
`REGLAS_ASPECTO`, `REGLAS_NUMERO`, `REGLAS_AGENTIVAS`. **La mayoría se apoya en
cognados wayunaiki, no en dato caquetío** — lo declaran ellas mismas en un campo
`wayunaiki`, que es lo correcto, pero conviene leerlo como lo que es.

| Afijo | Valor | Base |
|---|---|---|
| `-ka` | completivo | WY tríada A en contexto de pasado |
| `-ni` | continuativo | WY `-iraa` |
| `-da` | prospectivo / intencional | WY `-ee` desiderativo + tríada C |
| `ta-` / `wa-` | posesivo 1ª sg / pl | WY `ta-` / `wa-`, cognados directos |
| `ma-` | negativo / privativo | WY `ma-`, cognado directo |
| `ka-` | posesivo genérico / asociativo | WY `ka-` |
| `-kana` | plural colectivo | WY `-kana`, **cognado directo con caquetío** |
| `-naiki` | 'lengua de, habla de' | WY `-naiki` |
| `-ana` | topónimo / lugar habitado | ver §3 |
| `-gua` | región, área amplia | topónimos de Falcón y Sucre |
| `-bana` | **'orilla / borde'** — sin cita | ver §3 |

`ka-` y `wa-` tienen apoyo insular independiente: [[van-buurt-2014]] §8 da `ka-`
como localizador *'hay, existe(n)'* (*Casibari* = 'hay rocas duras') y §6 da
`wa-` como prefijo de pluralidad y posesión (de Goeje 1928). Convergen con la
lectura wayunaiki sin depender de ella.

## 3. `-bana` vs. `-ana` — la decisión abierta

**Este es el punto más importante de la nota.** Es la decisión **D9**:
[#38](https://github.com/miguelgilurbina/curiana-radio/issues/38).

### El problema

El proyecto enseña a los agentes, **desde el día 1 y sin ninguna cita**, que
`-bana` significa *'orilla, borde, límite'*. Está en `CLAUDE.md`, en
`REGLAS_LOCATIVAS` y en las instrucciones de acuñación. Es productivo: cada run
genera neologismos con él. **Si la glosa está mal, cada run propaga el error.**

### Lo que dicen las fuentes

| Fuente | Glosa de `-bana` | Evidencia |
|---|---|---|
| El proyecto | 'orilla, borde' | **ninguna** |
| [[van-buurt-2014]] §8 | **'ancho, llano'** | *Hudishibana* = 'llano ventoso' (`hudi` viento) |
| [[van-buurt-2014]] §6, vía Oliver | **'cubierto'** | *wakaubana* = 'cubierto por lo subterráneo' |

**La forma está confirmada**; el significado no. [[gatschet-1885]] aporta cuatro
topónimos arubanos con el afijo — *Shiribana, Tarabana, Wakubana, Bushiribani*
(`AFIJOS_EN_TOPONIMOS` en `lexicon_gatschet.py`).

### Lo que dice el propio lexicón

Las **tres palabras atestiguadas** del lexicón que terminan en `-bana` le dan la
razón a van Buurt, no al proyecto:

| Palabra | Glosa | Lectura |
|---|---|---|
| `cabana` | **'sabana'** | Una sabana es un **llano ancho**. No es una orilla. |
| `darubana` | **'camino, vía'** | Un camino es una franja **llana**, no un borde. |
| `capubana` | 'duende del cerro' (`capu` 'demonio') | Neutro: no decide, pero tampoco apoya 'orilla'. |

`cabana` = 'sabana' es casi una prueba: *llano ancho* es exactamente la glosa de
van Buurt, y 'orilla' no explica nada.

### El hallazgo de Miguel: el morfema fuerte es `-ana`

> **`-ana` = 'lugar de' está atestiguado, y `-bana` nunca lo estuvo.**

La ecuación que lo cierra la da el propio Zavala: **`paraguana` = *"Rodeada del
mar"***, y `para` / `paragua` = 'mar' **ya están en el lexicón como
`caquetío-atestiguado`**. Despejando: `paragua` + `-na` / `-ana` = el lugar
definido por el mar. Y `curiana` = *"lugar del cardón"* / territorio de los
caquetíos, que es literalmente la etimología del nombre del proyecto.

Otras entradas del lexicón en `-ana`: `guariana` (arbusto halófilo de playa),
`cabana`, `capubana`, `darubana`, `curiana`.

### Y sin embargo `-bana` también existe

No es que `-bana` sea un error de segmentación de `-ana`. **La reduplicación lo
prueba**: existen *Shiribana* (Aruba) y *Shishiribana* (Bonaire) — **el mismo
topónimo, con y sin reduplicación de la sílaba inicial**. Si la raíz es `shiri`
y se reduplica a `shishiri`, entonces lo que queda detrás es `-bana` entero, no
`-ana`. Los dos afijos coexisten.

### El estado real *(actualizado 2026-08-31 — tanda de decisiones)*

Hay **dos morfemas distintos**, y las dos decisiones les dieron destinos
opuestos a los que esta nota preveía:

- **`-bana`** = **'cerro, sitio alto' — RESUELTO y atestiguado** (D9/#38,
  2026-08-31). Seis apoyos convergentes: Zavala #26 «Bana (E): Sitio, cerro
  alto» (lema directo), la composición contigua `capu` #60 + `capubana` #61
  'duende **del cerro**', González Batista usándolo como establecido
  (*Guadadubana* = 'el cerro de las cañas'), el lazo referencial del dueño
  Capo en el cerro de Santa Ana — que **se llamaba Cerro de Capú** (Velasco
  2015), *Judibana* = 'cerro del viento', y las dos fuentes que esta nota ya
  registraba. Contra 'orilla': cero — y `cari` #66 'orilla del mar' ya cubre
  ese campo. Es **homónimo declarado** de `bana` 'hígado' (reconstruido por
  cognado lokono, Pet 1987).

  ⚠️ Las formas que no encajan **no se forzaron**: `cabana` 'sabana'
  (probable préstamo castellano), `darubana` 'camino', `guacaubana` 'río
  escondido' quedan como segmentación dudosa o polisemia pendiente — la
  lectura 'ancho/llano' de van Buurt sigue viva **para ellas**, registrada.

- **`-ana`** — **forma atestiguada, glosa 'lugar de' EN DISPUTA** (#109,
  ratificado 2026-08-31): el tratamiento que antes tenía `-bana`, invertido.
  *Paraguana* dejó de ser su apoyo — la fuente imprime **Paraguaná** con
  tilde, la glosa «Rodeada del mar» no despeja con 'lugar de', y existe la
  segmentación alternativa `para` + `gua` 'terreno cercado' + `ná` (los tres
  atestiguados en Zavala #190/#122/#184), con su objeción de orden anotada.
  *Curiana* tiene expediente propio abierto. Y `na` acumula **tres glosas
  rivales** ('como, semejante' — Zavala #184, la única impresa; 'tierra' —
  González Batista; 'propuesto' — Antolínez 1944): la canónica sigue siendo
  la de Zavala. Lo que zanja la disputa es el **censo de -ana/-aná en los
  topónimos de Esteves + la auditoría de tildes** — trabajo, no decisión.

> El mismo patrón se repite en `-are` vs `-ure`: la evidencia toponímica dice
> 'sitio de', van Buurt §5 dice 'raíz'. Ver [[toponimia]] §conflictos. D9 no es
> un caso aislado: es el primero de una clase.

## 4. La reduplicación

[[gatschet-1885]] afirma que varios topónimos arubanos se forman **duplicando la
raíz disílaba**, para onomatopeya, diminutivo o pluralidad. F11 lo **midió**
(`REDUPLICACION` en `lexicon_toponimos.py`), con el mismo detector aplicado a
todos los corpus:

| Corpus | Formas con unidad reduplicada | Tasa |
|---|---|---:|
| **Toponimia caquetía** | 26 de 287 | **9,0 %** |
| **Léxico caquetío** | 9 de 210 | **4,3 %** |
| control wayunaiki | 22 de 703 | 3,1 % |
| control lokono | 1 de 138 | 0,7 % |
| control taíno | 0 de 40 | 0 % |

**Es productiva, y no es un artefacto del método**: el detector es el mismo para
todos y el caquetío está claramente por encima de sus hermanas.

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
  #166) y `-bi` (van Buurt §6). *Aquí el dato contradice a la fuente y hay que
  decirlo.*

Advertencia de uso: el valor onomatopéyico es **formación léxica histórica**, no
morfología viva. Un agente no debería reduplicar para inventar un ave. El valor
de pluralidad sí es candidato a regla productiva.

## 5. Morfemas propuestos, aún no incorporados

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

Dos de ellos resuelven entradas del lexicón que estaban sin cita: `cari`
'costa, orilla' y `waka` → `sawaka` 'inframundo'.

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
| `-bacoa` | bosque, arboleda | **corroborado** (`bacoa` ya era atestiguado; lo nuevo es su uso **sufijal**) | 5 |
| `-are` | 'sitio de' (locativo) | **nuevo** — glosa en disputa con el `-ure` de van Buurt | 5 |
| `ada-` | árbol | **nuevo**, con cognado lokono `ada` | 2 |
| `bari-` | rojizo, turbio | reagrupado | 2 |
| `yacare` | pueblo, poblado | **nuevo** | 2 |
| `wa-` | pluralidad / 'tener' | corroborado | 2 |

## Enlaces

[[lexicon]] · [[toponimia]] · [[metodo-comparativo]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) · [[zavala-reyes-2015]] · [[van-buurt-2014]] · [[gatschet-1885]] · [[03_descomposicion_toponimica]]
