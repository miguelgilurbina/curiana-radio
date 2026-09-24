---
tipo: nota-viva
ambito: afijos y reglas de formación de palabras
fuente_de_verdad: curiana_sim/curiana_lexicon.py (TODAS_LAS_REGLAS, REGLAS_ZAVALA, REGLAS_TOPONIMICAS)
propuestas: [lexicon_van_buurt.py, lexicon_gatschet.py, lexicon_toponimos.py]
medido: 2026-09-20 (6-fusion/scripts/auditar_morfologia.py)
decidido: 2026-09-21 (6-fusion/decisiones_tanda_2026-09-21.yaml); 2026-09-23 (6-fusion/decisiones_tanda_final_2026-09-23.yaml)
---

# La morfología

> ⚠️ **La tanda final (2026-09-23) cambió el núcleo — D11 fase 3.** Lo que
> abajo figura como «reconstruido desde el wayuu» y deuda de D11 ya no se
> enseña: los pronombres son `dai`, `bui`, `lihi`/`tuhu`, `waya`, `naya` (de
> lokono, taíno y achagua); el aspecto es el verbo solo para el presente,
> `-kuba` para lo que ya pasó y `-ba` para lo que vendrá (hipotéticos: el
> taíno no atestigua ninguna marca); el posesivo de 1sg es `da-`. `-ka`, `-ni`,
> `-da` y `ta-` siguen en el desafijador (`REGLAS_EN_DESUSO`) porque la base
> entera está dicha con ellos. `-iro` y `-uco` pasaron a «leídos en
> topónimos» (`REGLAS_ESTEVES`): su única fuente era Esteves por la sigla (E)
> de Zavala. Las formas, sus citas y su coste están en
> `6-fusion/propuesta_d11_fase3_pronombres_aspectos_2026-09-23.yaml`,
> `6-fusion/propuesta_d11_voces_wayuu_2026-09-23.yaml` y
> `6-fusion/medicion_tanda_final_2026-09-23.yaml`; la bitácora lo cuenta en el
> punto 15 del «Cambio de instrumento». Las tablas de abajo son la foto de la
> auditoría del 2026-09-20 y se regeneran con `6-fusion/scripts/tabla_morfemas.py`.

> ⚠️ **La tanda de las hermanas (2026-09-24) no toca ningún morfema, pero sí
> las capas y los ejemplos.** El habla de mujeres kalinago cuenta como
> hermana (D1): `bui`, `lihi` y `tuhu` son ahora **reconstruidos** (lokono =
> kalinago de mujeres, Goeje 1939 p. 24), y el apoyo de `-kuba`, `-ba`, `ma-`
> y `ka-` gana un testigo (Adam 1879 pp. 277 y 300-301) sin dejar de ser
> hipotético. Los ejemplos que el prompt da de cada afijo cambian de raíz
> porque el núcleo cambió de voces: `kunu-kuba`, `kunu-ba`, `kidi-bana`,
> `ada-bakoa` (la raíz del topónimo Adabacoa, que d21.14 había quitado cuando
> `ada` era lokono), `hime-aima`, `da-akusi`. Registro en
> `6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml`; bitácora, punto 16.

> Lo que un agente puede **construir**, no sólo nombrar. Cada morfema va aquí
> con **su evidencia y su estado** — porque el proyecto mezcló durante mucho
> tiempo afijos atestiguados con afijos de trabajo sin marcar la diferencia, y
> eso contamina hacia adelante: los agentes acuñan con ellos en cada run.
>
> **Y desde la revisión del 2026-09-20 va también con lo que le falta.** Nueve
> de los 21 morfemas del motor se apoyan sólo en el andamio wayuu/lokono que
> D11 mandó retirar, y un sistema arahuaco tiene rasgos —clases de verbo,
> no-poseído, género— que éste no tiene. Declarar un hueco es parte de
> describir el sistema.

**Cómo se llegó a esta versión.** Miguel, 2026-09-20: «echarle una revisada a
toda la morfología arahuaca, para que ajustemos; quiero que tengamos la
morfología bien clara». De ahí salieron un medidor
(`6-fusion/scripts/auditar_morfologia.py`), una medición
(`6-fusion/medicion_morfologia_2026-09-20.yaml`), un issue con catorce
decisiones (`6-fusion/issues-pendientes/morfologia-revision-2026-09-20.md`) y
las catorce respuestas de Miguel del 2026-09-21
(`6-fusion/decisiones_tanda_2026-09-21.yaml`). Esta nota es el canon que
resulta de esas catorce. **Ninguna cifra está escrita a mano**: todas salen de
la medición, y la tabla del §3 la emite un script.

> ⚠️ **Qué está decidido y qué está aplicado.** Las catorce están **decididas**.
> Las que tocan `curiana_sim/` —el detector de aspecto, `_RAICES_VERB`,
> `REGLAS_ATRIBUTIVAS`, `-ana` sin glosa, `-kana`, `-naiki`, `kudanga`/`kuté`,
> el no-poseído, las glosas de los ejemplos— van en **un solo corte de serie**,
> no en cuatro: la serie C se repite una vez, con todo dentro. **Ese corte está
> hecho**: es el punto 13 del «Cambio de instrumento» de
> `5-experimento/BITACORA_RUNS.md` (#182, 2026-09-21), medido en
> `6-fusion/medicion_tanda_21_2026-09-21.yaml`. Donde esta nota decía
> «pendiente del corte» dice ahora **[aplicado en el corte 13]**, y lo que el
> corte midió distinto de lo que la auditoría estimaba está dicho en su sitio.
> Lo que dice de la **lengua** es canon desde el 2026-09-21.

---

## 1. El orden básico y los pronombres

```
pronombre + verbo-aspecto + complemento
Pronombres: taya (yo) · pia (tú) · nüma (él/ella) · waya (nosotros) · naya (ellos)
            + el registro FORMAL atestiguado: kudanga (usted) · kuté (a usted)
Neologismo: [forma: componentes = significado]
```

Los **cinco primeros son reconstruidos desde el wayuu** y son deuda de D11
fase 3: el canon no tiene ni un pronombre atestiguado en ese juego.

Los **dos últimos son caquetío atestiguado con cita**: [[zavala-reyes-2015]]
p. 73, vía Arcaya — *«chacamba cudanga»* '¿cómo está usted?' y *«cudan de
cuté»* 'para servir a usted'. Entran al habla por decisión del 2026-09-21
(d21.10) **como registro formal**, junto a los cinco y no contra ellos: `pia`
para el tú corriente, `kudanga` para dirigirse a un mayor o a un Diao. Es un
rasgo social además de gramatical, y la era 2 tiene la jerarquía escrita — el
trato formal al Manaure en el Capubana y el tú corriente en el conuco.
**[aplicado en el corte 13]**: la línea `TRATO FORMAL` va en
`prompt_reglas_completo`, o sea que la recibe el tier 1 —quien trata con el
Manaure y con el forastero—, no el elenco entero.

> **Corrección a [[lexicon]] §«manda la atestiguada»**: la frase «los pronombres
> no tienen rival atestiguado» **no era exacta**. Para la segunda persona sí lo
> hay. Lo que ocurre es que la política d19.b no lo dispara —la glosa no es
> idéntica, 'usted formal' ≠ 'tú'—, así que no es un caso de la política sino
> una decisión aparte. Y es el **caso barato** de esa política: no hay que
> archivar nada, las dos formas se reparten registros.

---

## 2. Cómo se lee este inventario

Cada morfema lleva cuatro cosas, y las cuatro juntas son lo que costó una
auditoría entera:

1. **forma y función declarada**;
2. **capa epistémica** — atestiguado / reconstruido / canon-simulación /
   retirado. Una sola por morfema, y **en duda se degrada** (regla 2);
3. **cita**, que es una **clave foránea** a `4-fuentes/bibliografia.yaml`
   (regla 8). Lo que no la tiene lleva `deuda: sin-procedencia` escrito: el
   hueco se admite, **callarlo no**;
4. **qué hace el motor con él** — en qué plantillas se enseña y por qué puertas
   del scorer pasa. Un morfema que el prompt enseña y el canon no declara es un
   error que se propaga en cada run; lo aprendimos tres veces en un día
   (`kali-bana`, el molde `X-bana`, la vía mala del viento).

La partición de una forma en prefijos + núcleo + sufijos **es la del motor, no
un regex de la auditoría**: se pelan los afijos de `_PREFIJOS_CAQ` y
`_SUFIJOS_CAQ` por los bordes, prefijos primero, en el mismo orden que
`nucleo_de_token()`. El control lo comprueba núcleo a núcleo:

```
control de segmentación: 2.546 formas · 0 desvíos contra nucleo_de_token() · VERDE
```

---

## 3. El inventario: los 21 morfemas del motor

```
morfemas en el motor                  21   (19 en TODAS_LAS_REGLAS + 2 retirados)
morfemas en 2-lengua/morfemas.yaml    11
morfemas propuestos sin importar      24   (lexicon_van_buurt + lexicon_gatschet)

con clave foránea válida a 4-fuentes/bibliografia.yaml:   9 de 21
```

Por capa: **9** reconstruidos sobre el andamio wayuu/lokono (deuda D11), **8**
atestiguados, **2** retirados (`-ko`, `-sha`, 2026-09-14), **1**
canon-simulación (`-ana`) y **1** reconstruido sin andamio declarado (`-gua`).

La tabla la emite `6-fusion/scripts/tabla_morfemas.py` desde la medición. **No
se edita a mano**: se regenera.

```bash
python 6-fusion/scripts/tabla_morfemas.py            # las dos tablas
python 6-fusion/scripts/tabla_morfemas.py --check    # ¿cuadran los totales?
```

### Los 21 morfemas del motor

| Morfema | Clase | Capa | Cita (clave foránea) | ¿Lo enseña? | ¿Lo reconoce el scorer? | Usos |
|---|---|---|---|---|---|---:|
| `-ni` | aspecto | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (5) | desafija · suelto · **aspecto (2/10 pts)** | 14.850 |
| `-da` | aspecto | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (3) | desafija · suelto · **aspecto (2/10 pts)** | 8.721 |
| `-ka` | aspecto | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (5) | desafija · suelto · **aspecto (2/10 pts)** | 7.442 |
| `ta-` | posesivo | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (4) | desafija · suelto · **es_arahuaco** | 6.843 |
| `-bana` | locativo | **atestiguado** | [[gonzalez-batista-nombre-de-coro]] · [[velasco-2015-resistencia]] · [[zavala-reyes-2015]] | sí (3) | desafija · suelto | 2.323 |
| `ma-` | posesivo | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (3) | desafija · suelto · **es_arahuaco** | 2.195 |
| `ka-` | posesivo | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (2) | desafija · suelto · **es_arahuaco** | 564 |
| `wa-` | posesivo | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (3) | desafija · suelto · **es_arahuaco** | 401 |
| `-ana` | locativo | canon-simulación | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 290 |
| `-kana` | número | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | sí (2) | desafija · suelto | 258 |
| `-iro` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 229 |
| `-uco` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 205 |
| `-ubana` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 106 |
| `-gua` | locativo | reconstruido | ⚠️ `deuda: sin-procedencia` | sí (2) | desafija · suelto | 102 |
| `-aima` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 94 |
| `-ima` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 88 |
| `-bacoa` | toponímico | **atestiguado** | [[alvarado-1921]] · [[van-buurt-2014]] | sí (2) | desafija · suelto | 57 |
| `-uru` | derivativo | **atestiguado** | [[zavala-reyes-2015]] | sí (2) | desafija · suelto | 2 |
| `-naiki` | número | reconstruido · andamio D11 | ⚠️ `deuda: sin-procedencia` | no | desafija · suelto | **0** |
| `-ko` | agentivo | retirada | ⚠️ `deuda: sin-procedencia` | no | no | fuera del censo |
| `-sha` | agentivo | retirada | ⚠️ `deuda: sin-procedencia` | no | no | fuera del censo |

*Leyenda.* **¿Lo enseña?** = en cuántas de las cinco plantillas estáticas
aparece (identidad, reglas completa, reglas breve, refuerzo, rescate).
**¿Lo reconoce el scorer?** — *desafija* = entra en `_PREFIJOS_CAQ` /
`_SUFIJOS_CAQ` y por tanto en `nucleo_de_token()` y `_familia_de_token()`;
*suelto* = escrito sin guion cuenta como palabra caquetía (`_AFIJOS_SUELTOS`);
*aspecto* = `_aspectos_morfologicos()`, hasta 2 de los 10 puntos;
*es_arahuaco* = la densidad arahuaca, el 60 % del score. **Usos** = sobre
`word_uses` de toda la base (95.445 usos, 2.546 formas; 43.756 en formas con
afijo declarado). Un `0` es un cero **medido**, no un hueco.

### Lo que el canon de datos declara y el scorer no ve

Los nueve de abajo están en `2-lengua/morfemas.yaml`, que es canon de datos de
lengua, y **ninguno entra en `TODAS_LAS_REGLAS`**: ni el desafijador de
`_familia_de_token()` ni `nucleo_de_token()` los ven.

| Morfema | Glosa | Dónde está declarado | Recurrencia | ¿Lo reconoce el scorer? |
|---|---|---|---:|---|
| `-are` | sitio de, paraje de (sufijo locativo) | 2-lengua/morfemas.yaml | 5 | **no** |
| `ada-` | árbol | 2-lengua/morfemas.yaml | 2 | **no** |
| `bari-` | rojizo, turbio (del color del agua o de la tierra) | 2-lengua/morfemas.yaml | 2 | **no** |
| `yacare` | pueblo, poblado | 2-lengua/morfemas.yaml | 2 | **no** |
| `-shi / -chi` | **sin glosar** | 2-lengua/morfemas.yaml | 22 | **no** |
| `-ari / -ri` | **sin glosar** | 2-lengua/morfemas.yaml | 7 | **no** |
| `-kuri / -curi` | **sin glosar** | 2-lengua/morfemas.yaml | 3 | **no** |
| `-bari` | **sin glosar** | 2-lengua/morfemas.yaml | 3 | **no** |
| `REDUPLICACIÓN` | pluralidad/abundancia y onomatopeya; 9,0 % del corpus toponímico | 2-lengua/morfologia.md §9 · `REDUPLICACION` en `lexicon_toponimos.py` | — | **no** |

### Las cuatro patologías, leídas de las tablas

El encargo pedía tres. Salió una cuarta de las otras tres, y es la que más pesa.

- **(a) El motor lo ENSEÑA y el canon no lo declara — 1.** `-ana`: capa
  canon-simulación y «sí» en la columna de enseñanza. Ver §8. *(Residuo del
  mismo tipo: `-uto` se escribía en el prompt dentro del campo `uso` de `-uco`
  **sin estar en `TODAS_LAS_REGLAS`** — se enseñaba y no se reconocía. Declarado
  como variante por d21.14, ver §4.)*
- **(b) El canon lo DECLARA y el scorer no lo reconoce — 9.** La segunda tabla,
  entera. La reduplicación es el caso que más escuece: es el único rasgo que el
  proyecto ha **medido con control** y no ha llevado al motor (§9).
- **(c) Apoyo SÓLO en el andamio wayuu/lokono que D11 mandó retirar — 9.** Los
  que llevan capa «reconstruido · andamio D11»: `-ka`, `-ni`, `-da`, `ta-`,
  `wa-`, `ma-`, `ka-`, `-kana`, `-naiki`. Ocho de los nueve se enseñan, y
  algunos en cinco plantillas a la vez. Es lo mismo que ya se retiró en
  `-ko`/`-sha` el 2026-09-14, por exactamente esta razón.
- **(d) El motor lo ENSEÑA y no hay clave foránea — 9.** Los que cruzan
  `deuda: sin-procedencia` con «sí» en enseñanza: `-ka`, `-ni`, `-da`, `-gua`,
  `ta-`, `wa-`, `ma-`, `ka-`, `-kana`. No es lo mismo que (a) —ahí el canon dice
  otra cosa— ni que (c) —ahí el apoyo existe pero es el andamio—: **aquí no hay
  apoyo que citar.**

> **Léase despacio: los tres aspectos, los cuatro prefijos de posesión y
> atribución, el plural y el locativo `-gua` son toda la gramática viva del
> motor, y ninguno apunta a una obra.** Lo que llevan en el campo de apoyo es el
> cognado wayunaiki («-iraa (imperfective suffix)», «ma- (prefijo negativo,
> cognado directo)») o una frase sin fuente («Topónimos venezolanos de Falcón y
> Sucre»).
>
> Matiz, para no exagerar: **esta nota sí cita apoyo insular independiente para
> `ka-` y `wa-`** —[[van-buurt-2014]] §8 y §6 vía de Goeje 1928—. Lo que falta
> es que la entrada del motor lo lleve: el campo `atestiguado` de las cuatro
> está vacío y el único texto es el cognado wayuu. **La nota sabe más que el
> código.**

### Qué mueve en esta tabla la tanda del 2026-09-21

Sin cifras, porque las cifras del corte se miden cuando el corte se aplique:

| Morfema | Qué decidió Miguel | Dónde |
|---|---|---|
| `ka-` · `ma-` | dejan de ser posesivos: **atributivo** y **privativo**, en tabla propia `REGLAS_ATRIBUTIVAS` | d21.5 C · §6 |
| `-ana` | se enseña **sin glosa**, como `-ubana` y `-uru` | d21.6 B · §8 |
| `-gua` → **`-wa`** | la campaña halló fuente para la FORMA (Oliver 1989 cap. 2 p. 148) y ninguna para la glosa: se enseña **sin glosa**, con el lema fonémico | d21.7 B → dc.2 C + E (tanda de la base) · §7 |
| `-kana` | la afirmación «cognado directo con caquetío» baja a **reconstruido desde el wayunaiki** | d21.8 A · §7 |
| `-naiki` | **se retira** a `REGLAS_RETIRADAS`, con `-ko` y `-sha` | d21.9 A · §7 |
| `-uto` | se declara **variante** dentro de la regla de `-uco`, para que deje de enseñarse sin reconocerse | d21.14 B · §4 |
| `-bacoa` | migra al lema fonémico **`-bakoa`** en el mismo corte de serie, y se mide antes | d21.14 A · §4 |

---

## 4. Los afijos atestiguados — `REGLAS_ZAVALA` y `REGLAS_TOPONIMICAS`

Documentados en el glosario de [[zavala-reyes-2015]] con su cita literal en el
campo `atestiguado`, más un formante toponímico de fuera de Zavala.

| Afijo | Valor | Cita |
|---|---|---|
| `-iro` | **diminutivo** — la única marca de diminutivo documentada | Zavala #166 (E): *«desinencia que se usa en diminutivo»* |
| `-aima` | abundancia (variante `-coa` en topónimos) | Zavala #6 (AM+PMA): *«desinencia que significa abundancia»* |
| `-ima` | humedad / quebrada | Zavala #165 (E+PMA): *«desinencia que significa humedad, quebrada»* |
| `-uco` | cauce, quebrada (**variante `-uto`**) | Zavala #268 (E): *«sufijo. Quebrada, cauce»* |
| `-ubana` | desinencia, **valor no precisado por la fuente** | Zavala #265 (AM) |
| `-uru` | desinencia, **valor no precisado por la fuente** | Zavala #274 (AM) |
| `-bacoa` | bosque, arboleda; paraje cubierto de | `morfemas.yaml` morfema-001 (Esteves 1989, cinco topónimos glosados) + [[alvarado-1921]] `-baca` vía [[van-buurt-2014]] §10 |

> `-ubana` y `-uru` son honestos precisamente por lo que **no** dicen: Zavala
> los registra como desinencias de la lengua sin darles valor semántico, y el
> proyecto no se lo inventó. Ese es el patrón a seguir en todo lo demás — y
> desde el 2026-09-21 es también el patrón de `-ana` (§8).

`-ima` tiene **corroboración independiente**: [[van-buurt-2014]] §10 lo
documenta como 'húmedo, mojado' (forma `nima`) vía Cruz Esteves 1989, en el
topónimo *Onima* de Bonaire. Dos fuentes que no se citan entre sí, misma glosa.

### D5 aplicada a la morfología (d21.14)

D5 decidió el 2026-08-31 que **la grafía española es grafía y el lema fonémico
es la palabra**. La morfología se quedó fuera de esa migración, y la tanda del
2026-09-21 la parte en dos:

- **Ahora (opción B): la deuda documental.** Los ejemplos de las reglas se
  reescriben con formas que el lexicón tenga, y `-uto` se declara como variante
  dentro de la regla de `-uco` **[aplicado en el corte 13]** — se declara y se
  enseña, pero **no entra en `TODAS_LAS_REGLAS`**: añadir la clave movería
  `_SUFIJOS_CAQ`, y eso no es lo que decide 14 B. Residuo declarado: se enseña
  y el scorer no lo reconoce. Hasta el corte, el prompt enseñaba
  `ada + -bacoa = adabacoa` y **ninguna de las tres formas está en
  `VOCABULARIO_BASE`** (`bakoa` sí); y cinco derivados —`Judibana`, `Corogua`,
  `adabacoa`, `yacarebacoa`, `wayuukana`— los presentan las reglas y el lexicón
  no los tiene. Tres de esos ejemplos enseñan a formar plural y gentilicio **con
  la lengua que `IDENTIDAD_LINGUISTICA` declara «tan ajena para ti como el
  español»**, y uno usa una forma archivada (`piache`, en `FUERA_DEL_HABLA`
  desde D10). No llegan al prompt del agente —`prompt_afijos_atestiguados()`
  sólo renderiza `REGLAS_ZAVALA` y `REGLAS_TOPONIMICAS`— pero son lo que lee
  quien venga detrás, y el propio módulo ya se había escrito la nota correcta
  para otro caso (`paa-ka`, 2026-09-19: *una referencia muerta aquí es deuda
  igual*).
- **Con el corte de serie (opción A): `-bacoa` → `-bakoa`.** Cambia una clave de
  `TODAS_LAS_REGLAS` → cambia `_SUFIJOS_CAQ` → mueve `nucleo_de_token()` y con
  él el score, y hay **57 usos** de `-bacoa` en la base que dejarían de
  segmentarse igual. **Se midió antes** (`medir_tanda_21.py`), y salió limpia:
  **32 formas / 65 usos** cambian de borde y **ninguna** cambia
  `es_raiz_de_ninguna_parte()` ni `_familia_de_token()`, que son los dos únicos
  consumidores del núcleo. Por eso se aplicó entera. El ejemplo del prompt es
  `kuru-bakoa`, que no se había dicho nunca en la base.
  **[aplicado en el corte 13]**

---

## 5. Las clases de verbo: **estativo** y **de acción**

*(Decisión d21.4, opción B: se declara la clase **sin importar el
alineamiento**.)*

Un **estativo** es una raíz cuyo significado es una **propiedad o un estado**
—tamaño, sabor, color, edad, condición del terreno, estado de ánimo— y que en
arahuaco **se conjuga como verbo**, no se usa como adjetivo. En el canon lleva
`cat: v_raiz`, entra en `_RAICES_VERB` y admite los tres aspectos (`-ka`,
`-ni`, `-da`) como cualquier otro verbo. Un **verbo de acción** es lo que el
castellano ya reconoce como verbo. Y **la etiqueta llega al prompt**, que es lo
que Miguel decidió: una línea diciendo que **un estado se predica con aspecto
igual que una acción**. **[aplicado en el corte 13]**: `cat: v_estativo` en el
minador, el bloque «UN ESTADO ES UN VERBO» en la plantilla completa y la línea
`ESTADO:` en la breve — llega a todo el elenco, no sólo al tier 1.

**La comparanda.** [[perea-alonso-1942]] describe la **4ª conjugación lokono**
—infinitivo en `-en`— como la clase de los estativos: colores, tamaños,
sabores, estados, con tres ejemplos impresos: `cule-n` 'ser rojo', `ibe-n`
'estar lleno', `hebbe-n` 'ser viejo' (pp. 634-640). Y en pp. 598-599 y 608 está
la regla que los fabrica, atribuida a Quandt: *cualquier nombre, adjetivo o
partícula se hace verbo anteponiendo `a-` o `c-`*. Perea lo dice sin rodeos:
«rojo» no es un adjetivo en lokono, es el verbo `cule-n`. De ahí la frase que
resume el hueco entero: **buscar «adjetivos» sueltos es buscar en la categoría
equivocada.**

La achagua de [[neira-ribero-1762]] hace lo mismo sobre una raíz, con el
atributivo `ca-`/`ka-`: `cabareuno` 'enojarse' / `cabarecayi` 'colérico' /
`cabareumí` 'es bravo'; y con el privativo `ma-`: `macarray` 'seco' /
`macarracataní` 'seco, estando seco'. *(Es de los Llanos: entra como comparanda
marcada, nunca como canon costero — regla 4.)*

**Los agentes lo descubrieron antes que nosotros.** La medición encontró **484
usos de aspecto sobre raíz no verbal**, de los que **143 son sobre adjetivo**
(111 con `-ni`, 32 con `-da`): `siwato-ni` 'está desganado', `ma-siwato-ni`,
`tüshi-da`, `tüshi-gua-da`, `kali-tüshi-ni`. Es la 4ª conjugación lokono
reinventada desde el uso.

### Los diez estativos declarados

El reparto de las **49 raíces** que una heurística de una línea de
`minar_zavala_glosario.py` había marcado `v_raiz` se hizo el 2026-09-20 (#178):
**10 estativos, 9 de acción, 29 nombres y 1 adverbio**. La clasificación fila a
fila vive en `lexicon_zavala.CLASES_DE_RAIZ_ZAVALA`; los números del corte, en
`6-fusion/medicion_clases_de_raiz_2026-09-20.yaml`.

| Raíz | Glosa de la fuente ([[zavala-reyes-2015]]) | Apoyo más directo |
|---|---|---|
| `apo` | Grande | LK `ipi-lli-be` 'ser grande' |
| `bachure` | Maneto, patituerto | LK `hiccu-li` 'ser cojo' |
| `kachipo` | En voz vulgar, enojado, colérico | ACH `cabareuno` 'enojarse' |
| `etamo` | Feroz, feo, espanto | ACH `carruicay` / `carrunatacayi` |
| `waidima` | Integro | WY `waneepiaa` **'ser entero'** |
| `waranao` | Salado, ácido | WY `palawaa` **'ser salado'** |
| `wasima` | Viejo, anciano | LK `hebbe` **'ser viejo'** — ejemplo impreso de Perea |
| `patapati` | Anegadizo | tipológico; `deuda: sin-procedencia` |
| `sinwanguso` | Insolente | tipológico; `deuda: sin-procedencia` |
| `usera` | Seco, arenoso | WY `josoo` **'estar seco'**; ACH `macarray` |

Las cuatro en negrita son el apoyo fuerte: **el propio lexicón ya glosa esas
voces hermanas en forma verbal** —«ser entero», «ser salado», «estar seco»,
«ser viejo»—, o sea que el proyecto ya sabía que el concepto es un verbo; sólo
que no lo había dicho del caquetío. Y `hebbe` es, además, uno de los tres
ejemplos con que Perea define la 4ª conjugación (pp. 634-640).

### Lo que NO se importa, y por qué no

**El alineamiento no entra.** El lokono tiene **dos juegos de pronombre
sujeto** —prefijado en los transitivos (`d-a-`, `b-a-`, `l-a-`, `t-a-`, `w-a-`,
`h-a-`, `n-a-`) y **pospuesto** en estativos y negativos (`de`, `bu`, `i`, `n`,
`u`, `hù`, `ye`)—, con regla explícita del propio Perea: *transitivo →
prefijado; intransitivo, estativo o negativo → pospuesto* (`halli-kebbe de` 'me
alegro', pp. 635 y 652).

**Y aun así no se importa.** Razón, dicha entera porque es el criterio de todos
los casos como éste: **no hay ni un dato caquetío detrás**. Importar el juego
pospuesto sería traer un paradigma entero de la hermana cuya filiación D11 dejó
abierta — exactamente el préstamo que este proyecto lleva un mes deshaciendo, y
lo que la regla 4 prohíbe hacer sin marcarlo. El canon no tiene ni un pronombre
atestiguado en ese juego y los cinco que usa son reconstruidos del wayuu.
Proponer `apo taya` 'yo (soy) grande' sería **re-derivar el núcleo desde el
lokono**, que es D11 fase 3 y está abierta. Que el lokono ponga el sujeto detrás
en los estativos es la razón **tipológica** para reconocer la clase, no una
forma que se copie. Queda disponible si D11 fase 3 se resuelve hacia el lokono.

> ⚠️ **Tensión abierta, y no se resuelve aquí.** El lexicón tiene además una
> categoría `adj` con **11 entradas** —`anasa` 'bueno', `tüshi` 'frío', `mütsia`
> 'negro', `kasuta` 'blanco', `sünatü` 'rojo', `tsipana` 'verde', `kanawa`
> 'amarillo', `siwato` 'desganado'…—, casi todas reconstruidas del wayuu. Son
> exactamente los «colores, tamaños, sabores» que Perea llama estativos:
> `sünatü` 'rojo' es, palabra por palabra, el `cule-n` de la p. 634. Están en la
> categoría equivocada por el mismo motivo que las 49 —nadie la declaró— pero
> **moverlas a `v_raiz` las metería en `_RAICES_VERB` y volvería a mover el
> score**. Es una segunda tanda, y va después de que este corte cierre.

---

## 6. `ka-` atributivo y `ma-` privativo — no son posesivos

*(Decisión d21.5, opción C: cambia el nombre, cambia el ejemplo del prompt, y
los dos salen de `REGLAS_POSESIVAS` a una tabla propia `REGLAS_ATRIBUTIVAS`.)*

**Es el cambio de fondo de la revisión.** `ka-` vivía en `REGLAS_POSESIVAS` con
el nombre «posesivo genérico / asociativo» y el prompt lo enseñaba como
`ka-biro = el salinero` — **una persona**.

**La comparanda dice otra cosa.** [[van-buurt-2014]] §8 lo documenta como
**localizador, 'hay / existe(n)'**: *Casibari* = «hay rocas duras», `ka-` +
`siba` 'piedra' + `rí` 'duro'. Y [[perea-alonso-1942]] p. 555 da el **par
mínimo** completo contra el privativo `m-`: `k-ere-u-ti` 'casado' /
`m-ere-u-ti` 'soltero', `c-a-nsi-ti` 'amante' = *el que TIENE afecto*. Es
morfología corriente de la familia: el par atributivo / privativo.

Así que:

| Prefijo | Valor | Apoyo |
|---|---|---|
| `ka-` | **atributivo / existencial** — 'hay X, tiene X' | [[van-buurt-2014]] §8 (*Casibari*); par mínimo lokono en [[perea-alonso-1942]] p. 555 |
| `ma-` | **privativo** — 'sin X, no X' | par mínimo con `ka-` ([[perea-alonso-1942]] p. 555); WY `ma-` cognado |

**[aplicado en el corte 13]** el paso a `REGLAS_ATRIBUTIVAS` y el ejemplo nuevo
del prompt, `ka-biro = 'hay sal, el sitio tiene sal'` junto a `ka-maure`. El
cambio es de **agrupación, no de claves**: `TODAS_LAS_REGLAS` sigue teniendo las
mismas entradas, y el invariante **se midió**: `nucleo_de_token()` devuelve lo
mismo, forma a forma, en toda la base — 0 cambios.

### La consecuencia escrita: «hay viento» es `ka-juri`, no `juri-ni`

**Un nombre se predica con `ka-`, no con aspecto.** La prueba práctica, que es
también la frontera de la clase estativa del §5: **si para decirlo en presente
hace falta `ka-`, no es estativo**.

El caso que lo destapó fue el viento. `juri` 'viento, ventarrón' llevaba
`cat: v_raiz` —puesto por la heurística— y de ahí `juri-ni` entraba por la rama
buena del detector de aspecto y contaba como verbo conjugado. #178 lo reclasificó
como nombre. Y los agentes, teniendo `ka-juri` disponible y sin enseñar, habían
agarrado la vía mala:

```
juri-ni  157 usos   ·   juri-ka  37   ·   juri-da  33
ka-juri    3 usos   ·   ma-juri   3
```

Y no es sólo el viento. Sobre los **30 nombres** que #178 sacó de `v_raiz`, la
vía del aspecto lleva **617 usos en 70 formas**; la vía de `ka-`, **6 usos en 4
formas**; la de `ma-`, **57 en 12**. En general los agentes usan mucho los dos
prefijos —`ka-` 564 usos, `ma-` 2.195— pero casi nunca sobre estos nombres.

> **Por qué importa, medido.** `ka-` y `ma-` juntos suman **2.759 usos** contra
> **6.843** de `ta-` solo: el mecanismo arahuaco bueno para **predicar un
> nombre** estaba escondido dentro de la tabla de posesivos y se usaba doce
> veces menos que el posesivo de primera persona.

> ⚠️ **Lo ya dicho no se reescribe.** Los usos de `juri-*` con aspecto que la
> base ya tiene quedan como se dijeron, igual que en los cuatro cortes
> anteriores. `juri` **es** caquetío atestiguado y la fila dice la verdad sobre
> su lengua; lo que estaba mal es el molde, y para eso está el corte declarado.

---

## 7. Las reglas de trabajo: aspecto, posesión y número — y la deuda D11

`REGLAS_ASPECTO`, `REGLAS_LOCATIVAS`, `REGLAS_POSESIVAS`, `REGLAS_NUMERO` (y,
tras el corte, `REGLAS_ATRIBUTIVAS`). **La mayoría se apoya en cognados
wayunaiki, no en dato caquetío** — lo declaran ellas mismas en un campo
`wayunaiki`, que es lo correcto, pero conviene leerlo como lo que es.

| Afijo | Valor | Base | Capa |
|---|---|---|---|
| `-ka` | completivo | WY tríada A en contexto de pasado | reconstruido · `deuda: sin-procedencia` |
| `-ni` | continuativo / imperfectivo | WY `-iraa` | reconstruido · `deuda: sin-procedencia` |
| `-da` | prospectivo / intencional | WY `-ee` desiderativo + tríada C | reconstruido · `deuda: sin-procedencia` |
| `ta-` / `wa-` | posesivo 1ª sg / pl | WY `ta-` / `wa-`, cognados directos; `wa-` además [[van-buurt-2014]] §6 (de Goeje 1928) | reconstruido (`wa-` con apoyo insular) |
| `ka-` / `ma-` | atributivo / privativo | ver §6 | **atestiguado** en la nota; la entrada del motor lo lleva con el corte |
| `-kana` | plural colectivo | WY `-kana` | reconstruido desde el wayunaiki · `deuda: sin-procedencia` |
| `-naiki` | 'lengua de, habla de' | WY `-naiki` | **retirado** (d21.9) |
| `-ana` | formante toponímico, **sin glosa** | ver §8 | atestiguado, sin valor |
| `-wa` (fuente: `-gua`) | formante toponímico, **sin glosa** (la 'región' se retiró en dc.2) | Oliver 1989 cap. 2 pp. 142, 148 | atestiguado, sin valor |
| `-bana` | **'cerro, sitio alto'** | ver §8 | **atestiguado** |

### El alcance de D11 fase 3

> **Medido el 2026-09-08 y confirmado el 2026-09-20.** Las tres marcas de
> aspecto —`-ka`, `-ni`, `-da`— salen **enteras** del wayunaiki. Así que
> «declarar la etiqueta del núcleo reconstruido» (la fase 3 de D11, abierta) no
> afecta sólo a la Capa 2 léxica: **afecta al sistema morfológico completo** —
> aspecto, posesión y número, que son nueve de los 21 morfemas. **La fase 3 no
> es una re-etiqueta: es la morfología entera.**
>
> Las tres tienen homógrafo en lokono con otro valor declarado —`-ca` es ahí la
> raíz del verbo *ser/estar*, `-ni` el auxiliar `a-ni-n`, y `-da`/`-dda` la
> partícula del presente que **ni Perea ni de Goeje saben explicar**—, pero
> **eso no se afirma como cognación**: son formas de dos letras, y medir
> parecido en formas así es lo que produjo el 80 % de fallo de las 441
> hipotéticas. Detalle y páginas en
> `6-fusion/lokono_gramatica_perea_1942.yaml` §verbo.
>
> **Y la pregunta directa, contestada: ¿hay algo atestiguado del caquetío que
> sostenga las tres marcas? No.** La sonda —entradas `caquetío-atestiguado` que
> sostengan `-ka`, `-ni` o `-da`— **da cero en las tres**.

> **Añadido el 2026-09-12.** Los paradigmas completos (pp. 609-684) están
> vaciados en el mismo YAML, §`verbo_paradigmas`. El futuro lokono de Schumann
> es **`-pa`**, con paradigma (`d-a-iyaha-ddi-pa` 'andaré'); el prospectivo
> `-da` del canon sale del wayuu `-ee`. No se afirma cognación entre ambos — se
> anota para la fase 3: si el núcleo se re-deriva desde el lokono, el futuro
> tiene forma atestiguada. Y [[perea-alonso-1942]] p. 606 deja además al
> gramático sospechando de su propia fuente: *«todo el mecanismo temporal de los
> pretéritos sea tan sólo uno de los tantos perfeccionamientos a priori de los
> misioneros»*, y que lo que la lengua hacía era un presente narrativo. **Eso es
> convergencia a favor de modelar con ASPECTO y no con tiempo** — juicio de
> autor, no prueba, pero con su razón dicha.

### `-kana`: el «cognado directo» que no tenía forma detrás (d21.8)

La regla afirmaba *«COGNADO DIRECTO con Caquetío»*. Las tres sondas dicen que no:

```
claves de familia caquetía terminadas en -kana:   sakana  ('ofrenda', caquetío-HIPOTÉTICO)
ocurrencias de «kana» en 2-lengua/toponimos.yaml:  0
«kana» en lexicon_zavala.py:                       #57 (HB) 'demonio' — un LEMA, no un sufijo
```

El único «cognado directo» exhibible es una forma **hipotética**, y la única
`kana` atestiguada es 'demonio'. La afirmación **baja a «reconstruido desde el
wayunaiki», deuda D11 como los tres aspectos**, y los ejemplos que formaban
plural con voz wayuu se reescriben con voz caquetía (`barsure-kana`).

**La forma se queda.** Archivarla dejaría a los agentes sin manera de decir «los
ancianos», y el dato lokono en contra —el plural es `-nu` pospuesto y **los
irracionales no distinguen número**, [[perea-alonso-1942]] p. 556— es de otra
lengua. Se declara como hueco en §10, no se importa.

> Se usa 258 veces, y **162 de ellas sobre raíz verbal** (`maa-ni-kana`,
> `masa-da-kana`, `chaa-ni-kana`), que la propia regla prohíbe. Esa cifra
> depende de la clasificación de raíces: ver §11.

### `-naiki`: se retira (d21.9)

**0 usos en 95.445.** Ninguna plantilla lo enseñaba. Su apoyo escrito era
literalmente el nombre de la lengua andamio (`wayuunaiki`) y su único ejemplo
también: apoyo circular. Se retira a `REGLAS_RETIRADAS` junto a `-ko` y `-sha`,
**por la misma razón por la que se retiraron aquéllos el 2026-09-14**: sin
fuente, y era convención.

> ⚠️ Retirarlo es gratis en uso y **no** en desafijado: sacarlo de
> `TODAS_LAS_REGLAS` mueve `_SUFIJOS_CAQ`, así que aunque el uso sea cero hay
> que **medir antes** por si alguna forma hoy se desafija y mañana no.
> **[aplicado en el corte 13]** — medido: 0 formas cambian de núcleo.

### `-gua`: sin procedencia, y una campaña abierta (d21.7)

> **Resuelto en la tanda de la base (2026-09-23, dc.2 C + E).** La campaña
> encontró fuente para la FORMA y ninguna para la glosa: Oliver 1989 cap. 2
> p. 148 lista «f) -wa [gua-]» entre los sufijos toponímicos caquetíos y nunca
> le da valor; p. 142 escribe «gua=/wa/». El único `gua` glosado es el
> sustantivo `wa` 'conuco' (Zavala #122), que dice lo contrario de «región
> amplia», y leerlos como un morfema sería inferencia nuestra. Así que la
> regla pasa a **`-wa`**, se enseña **sin glosa** junto a `-ana` y deja de ser
> deuda. 54 formas de la base se segmentan distinto (112 usos) y una sola
> cambia de clase. Medido en `6-fusion/medicion_tanda_base_2026-09-23.yaml`.
> Lo de abajo es cómo estaba antes.

Único apoyo escrito: la frase «Topónimos venezolanos de Falcón y Sucre». **Cero
clave foránea.** Se enseña en las dos plantillas y se usa **102 veces sobre 37
raíces**. Mientras tanto se declara `deuda: sin-procedencia` y **se sigue
enseñando**, como hace el resto del proyecto con lo que no tiene fuente.

**La campaña**, que es lo que Miguel eligió: buscarle fuente en
`2-lengua/toponimos.yaml` (109 topónimos en canon) y en el gazeteer de Esteves
ya minado. Es media sesión, y `-gua` es el único de los doce sin cita que tiene
una fuente plausible ya en el repo y sin minar para esta pregunta. **Apoyo que
ya existe en el canon**: `paragua` se lee como `para` 'mar' + `-gua`, y por eso
el 2026-09-19 se decidió **no** fusionar `parawa`/`para` — fusionarlas habría
borrado este morfema.

---

## 8. `-bana` vs. `-ana` — resueltos, cada uno a su manera

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
**Los dos afijos coexisten.**

### El estado

- **`-bana` = 'cerro, sitio alto' — RESUELTO y atestiguado** (D9/#38,
  2026-08-31). Seis apoyos convergentes: Zavala #26 «Bana (E): Sitio, cerro
  alto» (lema directo), la composición contigua `kapu` #60 + `kapubana` #61
  'duende **del cerro**', [[gonzalez-batista-nombre-de-coro]] usándolo como
  establecido (*Guadadubana* = 'el cerro de las cañas'), el lazo referencial del
  dueño Capo en el cerro de Santa Ana — que **se llamaba Cerro de Capú**
  ([[velasco-2015-resistencia]]) —, *Judibana* = 'cerro del viento', y las dos
  fuentes de van Buurt. Contra 'orilla': cero — y `kari` #66 'orilla del mar' ya
  cubre ese campo. Es **homónimo declarado** de `bana` 'hígado' (reconstruido
  por cognado lokono).

  ⚠️ Las formas que no encajan **no se forzaron**: `kabana` 'sabana' (probable
  préstamo castellano), `darubana` 'camino', `guacaubana` 'río escondido' quedan
  como segmentación dudosa o polisemia pendiente — la lectura 'ancho/llano' de
  van Buurt sigue viva **para ellas**, registrada. Y [[perea-alonso-1942]] añade
  el lado lokono con atestaciones: `u-banna` 'sobre, encima, la superficie de'
  (`SURA u-banna` = la azotea), que queda **más cerca del 'ancho, llano' de van
  Buurt que del 'cerro' de D9**. No derriba D9; tampoco lo refuerza, y
  presentarlo como refuerzo sería leer hacia la conclusión que conviene.

  > **Lo que la medición añade**: `-bana` es el locativo más productivo —**2.323
  > usos, 254 formas, 149 raíces**— y **886 de esos usos van sobre una raíz que
  > no está en el lexicón**: `lumina-bana`, `kali-bana` (archivada),
  > `karu-bana`, `suave-bana`, `tension-bana`. Es el molde del corte del
  > 2026-09-19 visto desde el otro lado: la puerta de la raíz de ninguna parte
  > cierra la forma, y este número dice cuánto había detrás.

  > **Y un argumento morfológico que conviene tener escrito** (d21.16): `-bana`
  > es un **sufijo** locativo, no un sustantivo. Compone —`kali-bana`,
  > `biro-bana`— pero **no nombra**, así que «cerro ya se dice con `-bana`» no
  > se sostiene como razón para archivar `sima` o `turumako`.

- **`-ana` — forma atestiguada, SIN GLOSA** (#109, decisión B de Miguel,
  2026-09-07; y desde el 2026-09-21 también **en el prompt**, d21.6 B). Es
  `morfema-011` en `morfemas.yaml`, formativo sin valor declarado, con lista
  viva de casos en `6-fusion/censo_ana_esteves_109.yaml` (Paraguaná, Curiana,
  Chamuriana, Cujicana, Jayana, y el Coria-na wanebucán de Oliver p. 207).

  Hasta esta tanda el motor lo conservaba con glosa 'lugar de' como **convención
  de la simulación**, y las dos plantillas la enseñaban — o sea que **el prompt
  decía algo que el canon había retirado**, escrito y todo en el propio campo
  `evidencia` de la regla. Ahora se enseña **como se enseñan `-ubana` y `-uru`**:
  *desinencia atestiguada cuyo valor nadie anotó; puedes usarla si propones su
  valor entre corchetes*. Ni se quita del prompt —eso tiraría un formante
  atestiguado— ni se deja el error con permiso. Y **abre** la posibilidad de que
  los agentes propongan la glosa, que es para lo que existe esta simulación. Uso
  actual: **290 sobre 53 raíces**. **[aplicado en el corte 13]**

  *Paraguana* dejó de ser su apoyo: la fuente imprime **Paraguaná** con tilde,
  la glosa «Rodeada del mar» no despeja con 'lugar de', y existe la segmentación
  alternativa `para` + `gua` 'terreno cercado' + `ná` (los tres atestiguados en
  Zavala #190/#122/#184). **Censo hecho el 2026-09-07**: de las 13 formas en
  -ana del índice de Esteves, 6 son `-bana`, 1 es `-bana` con h (Capuhana), 2
  llevan el -ana dentro de una raíz léxica, y 4 van sin glosa. **Ninguna glosada
  'lugar de'**: el 'lugar' de Esteves es `bacoa`.

  > Una nota comparativa, con su cautela: el lokono **sí** forma nombres de
  > lugar e instrumento con un sufijo `-na`, casi siempre sobre la partícula
  > durativa `-coa-` — `a-balti-coa-na` 'asiento', `diki-kua-na` 'espejo'
  > ([[perea-alonso-1942]] p. 561). Es evidencia de **una lengua hermana, no
  > evidencia sobre el caquetío**, y el propio Perea avisa de que *«son pocos
  > los vocablos así formados»*. Lo que aporta es que la hipótesis retirada no
  > era absurda: era insostenible **con el dato caquetío**.

> El mismo patrón se repite en `-are` vs. `-ure`: la evidencia toponímica dice
> 'sitio de' (cinco apoyos, `dabudare` como caso decisivo), van Buurt §5 dice
> 'raíz'. Ver [[toponimia]] §conflictos. **Es la próxima D9 y sigue abierta.**

---

## 9. La reduplicación

[[gatschet-1885]] afirma que varios topónimos arubanos se forman **duplicando
la raíz disílaba**, para onomatopeya, diminutivo o pluralidad.
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
  #166) y `-bi` ([[van-buurt-2014]] §6, sin incorporar). *Aquí el dato
  contradice a la fuente y hay que decirlo.*

Advertencia de uso: el valor onomatopéyico es **formación léxica histórica**, no
morfología viva. Un agente no debería reduplicar para inventar un ave. El valor
de pluralidad sí es candidato a regla productiva.

> ⚠️ **Deuda abierta, y de las que escuecen.** Es el único rasgo que el proyecto
> ha **medido con control** y **no ha llevado al motor**: no se enseña, no se
> reconoce al puntuar, no hay regla. Está en la patología (b) del §3, y si la
> regla productiva de pluralidad entra es decisión de Miguel: no estaba entre
> las catorce.

---

## 10. Lo que un sistema arahuaco tiene y éste no

*(Sección nueva, decisión d21.13, opción B: se importa **sólo el no-poseído**;
los otros dos se declaran como huecos con su cita y se esperan.)*

Declarar el hueco es parte de describir el sistema. Callarlo es lo que la
regla 8 prohíbe para las fuentes, y vale igual para la gramática.

| Rasgo | Qué dice la comparanda | Qué hace este sistema |
|---|---|---|
| **Posesión no-poseída** | [[perea-alonso-1942]] p. 587: índices personales sobre el nombre (`da-si-kua` 'mi casa') **y el índice absoluto `u-`/`ù-`** — `u-si-kua-hù` = *LA casa, sin poseedor*. Y p. 586, posesivos absolutos `da-kía` 'mío', `wa-kía` 'nuestro' | **ENTRA.** Es el único de los tres que se importa, porque es **puramente gramatical** y tapa un hueco medido: sin él, un agente que quiera nombrar una cosa sin dueño no tiene cómo, y `ta-` está a mano — **6.843 usos sobre 258 raíces distintas**. **[aplicado en el corte 13]**: `REGLAS_POSESIVAS["u-"]`, reconocido y enseñado; añadir la clave mueve `_PREFIJOS_CAQ` y se midió — 0 formas cambian de núcleo |
| **Género / clases** | [[perea-alonso-1942]] p. 554: no hay género gramatical; hay **varonil** y **no varonil**, con sufijos `-ti/-tti` vr. y `-tu/-ttu` nv., y `-nu` plural común. El no varonil comprende a las mujeres, a los animales de ambos sexos y a todas las cosas. Los achagua de [[neira-ribero-1762]] cambian el numeral según lo que cuentan (personas, palos, ríos, lunas) | **HUECO DECLARADO, y a propósito.** No hay **ni un dato caquetío** de género, y la distinción varonil/no varonil arrastra una cosmovisión entera: importarla es exactamente lo que **la regla 4 prohíbe** — importar un rasgo sin marcarlo. Y el proyecto acaba de pasar por eso al retirar `-ko`/`-sha`, que era un género inventado. Se espera |
| **Número de los irracionales** | [[perea-alonso-1942]] p. 556: `keyu` 'venado, venados', `siba` 'piedra, piedras', `adda` 'árbol, árboles', `a-wadu-lli` 'viento, vientos' — los irracionales **no distinguen número**; y los pocos animales pluralizados que aparecen son «huella del traductor alemán» | **HUECO DECLARADO.** `-kana` se aplica a todo. Es un dato precioso **y de otra lengua**: se anota y se espera. Bajar `-kana` (§7) no es lo mismo que importar esta restricción |
| **Alineamiento** | [[perea-alonso-1942]] pp. 635 y 652: dos juegos de pronombre — prefijado `d-a-, b-a-, l-a-…` en transitivos, pospuesto `de, bu, i, n, u, hù, ye` en estativos y negativos | **Un solo juego, sin alineamiento.** Declarado, no importado, con la razón escrita en §5 |
| **Nominalización** | [[perea-alonso-1942]] pp. 609-612: nombre de acción `-hù` (`a-iyaha-dda-hù` 'andadura'), `-hi` en los estativos (`c-a-nsi-hi` 'amor', `halli-kebbe-hi` 'alegría'), participios `-ti/-tu/-nu`, agentivo `-ha-li-n` | **No hay regla, y las fuentes tampoco la registran** (campaña del 2026-09-21: negativo medido, con control positivo). Lo que el atestiguado sí da es **derivación cero** —`jusual` «Sembrar, siembra, sembradío»— y lo que la comunidad hizo fue nominalizar con el posesivo. Ver §11. El `-hù`/`-hi` lokono **no se importa**: sería morfología de otra lengua sin dato |
| **Reduplicación** | [[gatschet-1885]] y [[perea-alonso-1942]] p. 679 | Medida con control (§9), **no implementada** |
| **Segundo diminutivo `-bi`** | [[van-buurt-2014]] §6: *gobí, gogorobí, kokorobí, lobi, makambí* | En `MORFEMAS_VAN_BUURT`, **sin adjudicar** |

---

## 11. La gramática que emergió

**Ésta es la sección por la que existe el proyecto.** Miguel, 2026-09-21, al
decidir el punto de la nominalización:

> «Muy interesante cómo los agentes lo resolvieron. Eso es súper importante irlo
> dejando en nuestros sights, porque es literalmente la idea del proyecto: ver
> el surgimiento del lenguaje, un resurgimiento, una reimaginación.»

### El criterio, que es lo que separa un hallazgo de un error

Un patrón que el motor no declara puede ser dos cosas muy distintas, y la
diferencia **no es de gusto**:

- **Si alguna plantilla lo enseña, es artefacto y se corrige.** El instrumento
  se estaría midiendo a sí mismo. Es lo que pasó con `kali-bana`, que era el
  ejemplo literal de `IDENTIDAD_LINGUISTICA` y se contaba como acuñación de la
  comunidad; y con el molde `kali-…-bana`, que ninguna plantilla enseñaba pero
  cuya raíz sí venía del ejemplo.
- **Si no lo enseña nadie, es emergencia y se describe.** No se devuelve al
  prompt convertido en regla: hacerlo **convertiría un hallazgo en una
  instrucción** y haría circular la medición — el mismo error, con otro nombre.

Las dos cosas de abajo pasan la prueba: **ninguna plantilla las enseña.**

### El apilamiento libre — 57 patrones, 988 usos, 273 formas

*(Decisión d21.12, opción A.)*

**Ninguna regla del proyecto declara apilamiento de afijos**: los quince campos
`uso` de `TODAS_LAS_REGLAS` son de UN afijo sobre UNA raíz. Los agentes
apilaron igual, **hasta cuatro slots** en una palabra.

| Secuencia de clases | Usos | Formas | Ejemplos |
|---|---:|---:|---|
| RAÍZ + locativo + aspecto | 300 | 35 | `biro-ana-da`, `chaa-bana-ni`, `eroa-bana-da` |
| RAÍZ + locativo + derivativo | 151 | 19 | `isiro-bana-uco`, `juri-bana-uco`, `kali-bana-ima` |
| RAÍZ + **aspecto + aspecto** | 130 | 48 | `chaa-da-ka`, `chaa-ni-da`, `jacura-ni-ka` |
| posesivo + RAÍZ + locativo | 114 | 35 | `ka-barsure-ana`, `ka-biro-ana`, `ka-kalu-bana` |
| RAÍZ + **locativo + locativo** | 53 | 20 | `awa-bana-gua`, `juri-bana-gua`, `kapu-bana-gua` |
| posesivo + RAÍZ + derivativo | 40 | 14 | `ka-barsure-ima`, `ka-biro-uco`, `ma-barsure-ubana` |
| RAÍZ + **derivativo + derivativo** | 39 | 4 | `biro-uco-aima`, `kali-uco-iro`, `kati-iro-ubana` |
| posesivo + RAÍZ + aspecto | 35 | 15 | `ma-cucu-da`, `ma-puri-ka`, `ma-siwato-ni` |
| RAÍZ + derivativo + locativo | 20 | 4 | `kali-iro-bana`, `kali-ubana-gua`, `kati-iro-bana` |
| RAÍZ + aspecto + número | 18 | 12 | `chaa-ni-kana`, `maa-ni-kana`, `masa-da-kana` |
| RAÍZ + derivativo + aspecto | 13 | 12 | `awa-iro-ni`, `juri-aima-ni`, `juri-ubana-ni` |
| posesivo + RAÍZ + locativo + aspecto (**cuatro slots**) | 8 | 7 | `ta-chaa-bana-ni`, `ma-nii-bana-da`, `ta-karu-bana-ni` |
| posesivo + RAÍZ + derivativo + derivativo (**cuatro slots**) | 7 | 4 | `ka-biro-uco-aima`, `wa-biro-uco-aima` |
| RAÍZ + locativo + locativo + aspecto (**cuatro slots**) | 5 | 3 | `masa-bana-gua-ni`, `naba-ana-bana-ni` |

*(Catorce de las **27 secuencias** medidas, que suman los 988 usos; las trece
restantes están en `6-fusion/medicion_morfologia_2026-09-20.yaml`
§`combinaciones_no_declaradas`. Los **57 patrones** son estas secuencias con la
categoría de la raíz dentro.)*

**Se declara que los afijos se apilan y que el orden NO está fijado**, y la
lista medida queda como el registro de lo que hace la comunidad. El prompt no se
toca.

**Y se dice por qué no se fija.** Fijar un orden de plantilla
(`posesivo + RAÍZ + derivativo + locativo + número + aspecto`) sería devolverles
como regla lo que ellos inventaron: convertiría un hallazgo en una instrucción y
haría circular la medición. **Tampoco se declaran las dos «exclusiones»**
—dos aspectos apilados (130 usos) y dos locativos (53)—, porque `chaa-ni-da`
(«lo está haciendo y lo va a hacer») **no es obviamente agramatical en un
sistema de aspecto sin tiempo**, y llamarlo error sería una afirmación sobre una
lengua que no tenemos.

Dos lecturas que conviene tener escritas:

- **`awa-bana-gua`, `kono-ana-gua`** componen *lugar dentro de región*, que es
  exactamente lo que invita la propia jerarquía declarada («`-gua`: menos
  específico que `-ana`») y que nadie autorizó.
- **`ka-biro-uco-aima`** es prefijo + raíz + dos derivativos: la comunidad
  construyó una palabra de cuatro slots con un sistema que declara uno.

### Dos invenciones sobre raíz verbal — 960 usos, 92 formas

*(Decisión d21.11: **A** —describir el sistema que emergió— y **C** como
campaña. La campaña corrió el 2026-09-21 y cerró en negativo; Miguel aceptó
**A + B**, y **E + F** para esta sección:
`6-fusion/decisiones_campanas_2026-09-21.yaml`, dc.3. Abajo, «Lo que dicen las
fuentes».)*

**Sonda sobre el canon: reglas que deriven un nombre de un verbo → cero.** El
sistema no tiene nominalizador, y la comunidad hizo **dos cosas distintas** con
un prefijo sobre raíz verbal. Hasta el 2026-09-21 esta sección las sumaba bajo
el titular «el posesivo» — y desde d21.5 `ma-` y `ka-` **no son posesivos** (§6).

```
1. NOMINALIZACIÓN CON EL POSESIVO                    470 usos · 48 formas
   ta- sobre raíz verbal   453 usos · 37 formas   ta-chaa 'mi hacer'
   wa- sobre raíz verbal    17 usos · 11 formas   wa-jai 'nuestro oír'

2. PREDICACIÓN PRIVATIVA / ATRIBUTIVA SOBRE VERBO    490 usos · 44 formas
   ma- sobre raíz verbal   471 usos · 34 formas   ma-awa 'sin beber', ma-panaa 'sin saber'
   ka- sobre raíz verbal    19 usos · 10 formas   ka-chaa, ka-eroa
                                                  ────────────────────
                                                     960 usos · 92 formas
```

Sólo la **primera** es nominalización: el posesivo exige un nombre y lo que hay
debajo es un verbo. La **segunda** es predicación negativa sobre un verbo con un
prefijo que el canon declara para NOMBRES (§6) — una segunda invención, y nadie
la había nombrado. Medido sobre 95.445 usos de `word_uses` (runs anteriores al
2026-09-21), 45 raíces verbales y 112 agentes, con el segmentador comprobado
forma a forma contra `nucleo_de_token()`:
`6-fusion/medicion_nominalizacion_emergente_2026-09-21.yaml`.

> **Las cifras anteriores de esta sección (1.107 y 1.132) eran de ANTES de #178**,
> que sacó 30 raíces de `v_raiz`: con menos raíces verbales hay menos «prefijo
> sobre verbo». No estaban mal medidas; medían otro lexicón.

**De quién viene.** El campo es mental —saber, pensar, querer, decir—, no
manual. Y viene de arriba: en la era 2 la casa del Manaure dice 143 de esos usos
y **el Manaure solo, 59** — es el hablante que más lo hace. Por nodo, la tasa
por hablante posible es 7,1 en GUARANAO y 4,2 en AMUAY. **Ninguna** de las 29
entradas de koiné fijadas en la base es de este tipo: el invento circula y no se
ha fijado.

**Se sacó «posesivo sobre verbo» de la lista de violaciones y se declara que el
posesivo nominaliza.** Es describir el sistema que emergió, no sancionarlo. Es
una solución razonable y **no es la arahuaca** —el lokono nominaliza con `-hù`
y `-hi`—, y eso es precisamente lo que la hace un dato: la comunidad llenó un
hueco por su cuenta, con lo que tenía a mano.

#### Lo que dicen las fuentes: no hay nominalizador que retroabstraer (A), y sí derivación cero (B)

La campaña (`6-fusion/propuesta_nominalizador_2026-09-21.yaml`,
`6-fusion/medicion_nominalizador_2026-09-21.yaml`) trabajó con la **glosa
verbatim** de las 288 entradas de [[zavala-reyes-2015]], no con la curada:
30 verbos (19 de acción, 11 estativos) y 46 nombres de acción, agente,
instrumento o resultado (34 sin las dudosas).

- **El negativo, medido.** De 66 parejas «lema + resto = lema», **una sola** es
  verbo + resto = nombre: `apo` #11 «Grande» + `-po` = `apopo` #12. Muere: el
  verbo lleva el mismo final, n = 2, y la reduplicación parcial (§9, medida con
  control) lo explica sin morfema nuevo — compartir sílaba no es compartir
  morfema. De 23 terminaciones que aparecen a la vez en verbos y en nombres,
  ninguna aguanta. `-ba` salía significativa (×4,47, p = 0,0014) y **desaparece**
  al quitar las glosas dudosas.
- **Y el método no es ciego.** Sobre un grupo de control —nombres de
  lugar-de-cosa, n = 11— sí detecta `-ebo` (×13,09, p = 0,00079). Ve donde hay;
  el cero es real.
- **Dónde más se miró, y no hay**: [[oliver-1989-apendice-a]] tabla A-9 (0 de
  49), [[medina-colina-sxx]] (0 de 66), [[alvarado-1921]] (sólo verbos
  castellanos denominales). [[arcaya-1920]] p. 75 declara que no dejó
  vocabulario ni frases con que conocer la estructura gramatical.

**La opción A de d21.11 deja de ser provisional**: no se retroabstrae ningún
nominalizador, y **sigue sin importarse el `-hù`/`-hi` lokono** —sería morfología
de otra lengua sin dato caquetío—. El hueco queda **declarado** (regla 8).

**Lo que el material SÍ registra: derivación cero** (capa
`caquetío-atestiguado`, [[zavala-reyes-2015]], compilador AM). Cuatro entradas
glosan con **una sola forma** el verbo y su nombre, más una dudosa:

| forma | # | glosa verbatim |
|---|---|---|
| `jusual` | 180 | «Sembrar, siembra, sembradío. Conuco» — infinitivo, nombre de acción y nombre de lugar en UNA forma: si hubiera nominalizador, aquí se vería |
| `jacuque` | 170 | «Regar, regadío» |
| `beceremicore` | 39 | «Dominar, triunfar, victoria» |
| `etamo` | 120 | «Feroz, feo, espanto» (`v_estativo` en el canon) |
| `siguruba` | 228 | «Salvar. Caserío, sitio» — *dudosa*: la segunda mitad puede ser un topónimo |

Y del lado del nombre, `quiricias` #217: «Sangre, sangrado».

> ⚠️ **La reserva, que no es menor.** Una glosa que enumera «sembrar, siembra,
> sembradío» puede ser el compilador diciendo *de qué va* la palabra, no una
> afirmación sobre las clases de palabra del caquetío. Lo que se afirma es: **el
> material atestiguado no registra ninguna marca de nominalización, y donde da
> las dos cosas las da con la misma forma.** Lo que NO se afirma es que «el
> caquetío no marcaba la nominalización». Y un límite más: **los 19 verbos de
> acción del glosario son los 19 de Angulo Molina** — todo el verbo caquetío del
> proyecto es una sola lista, que no está en el repo. Una corroboración dentro
> de ella no es independiente.

Que la plantilla ENSEÑE la derivación cero («un verbo puede decirse como nombre
tal cual») era cambio de prompt y **se aplicó en la tanda de la base**
(2026-09-23): «un verbo es también su nombre, sin marca — jusual es sembrar y la
siembra», en las dos plantillas.
Y lo emergente **no es evidencia** de lo atestiguado, ni al revés: que los
agentes nominalicen con `ta-` y que Zavala glose «sembrar, siembra» con una sola
forma son dos hechos de dos mundos.

> Y una propuesta que salió de aquí y no es de esta tanda: que **«qué inventaron
> ellos que el sistema no tiene» pase a ser un informe del cierre de día**, en
> vez de un hallazgo de auditoría cada dos meses.

> ⚠️ **Las cifras de violación de slot dependen de la clase de la raíz.**
> `ma-awa` era «violación» porque `awa` 'beber' lleva `cat: v_raiz`;
> `siwato-ni` lo era porque `siwato` 'desganado' lleva `cat: adj`. #178 ya
> movió 30 de las 49 raíces de Zavala, y la tanda de la categoría `adj` (§5)
> podría mover hasta once más. En total la medición contó **13 casos y 1.778
> usos**:
> 1.132 de posesivo/atributivo sobre raíz verbal (hoy 960, tras #178), 484 de aspecto sobre raíz no
> verbal y 162 de número sobre raíz verbal. Léanse como **la pregunta, no como
> el veredicto**.

---

## 12. Qué reconoce el motor al puntuar

Una cosa es enseñar un morfema y otra contarlo. Las puertas son cuatro, y
conviene saber cuál es cuál:

| Puerta | Qué hace | Quién entra |
|---|---|---|
| `_PREFIJOS_CAQ` / `_SUFIJOS_CAQ` | el desafijado de `nucleo_de_token()` y `_familia_de_token()`: dice dónde acaba la raíz | los afijos activos de `TODAS_LAS_REGLAS` |
| `_AFIJOS_SUELTOS` | un afijo escrito suelto cuenta como palabra caquetía | los mismos, sin guion |
| `_aspectos_morfologicos()` | hasta **2 de los 10 puntos** del score | `-ka`, `-ni`, `-da` sobre raíz verbal — y, hasta el corte, sobre cualquier raíz de tres letras o más (el comodín, abajo) |
| `score_linguistico.es_arahuaco()` | densidad arahuaca, el **60 %** del score | prefijo posesivo/atributivo + raíz activa, y raíz verbal |

### Las dos correcciones de la tanda **[aplicadas en el corte 13]**

1. **`_RAICES_VERB` mezcla las cinco lenguas** (d21.2, opción A). Se construye
   como `{k for k, v in VOCABULARIO_BASE if v['cat'] == 'v_raiz'}`, **sin
   filtrar por lengua**. El día de la medición eran **1.424 claves, de las que
   1.351 no eran caquetías** (1.078 proto-arahuaco, 273 lokono) y sólo 73 lo
   eran. Y `es_arahuaco()` devuelve `True` para cualquier
   token cuyo **primer segmento** esté ahí. Es la misma clase de agujero que el
   `return "caquetío"` del 2026-09-20, en otra puerta. Se filtra a familia
   caquetía **en las dos puertas** —`es_arahuaco` y el detector de aspecto—.

   > Después de #178 la tabla quedó en **1.394 claves, 43 de familia caquetía**.
   > Se recuenta con:
   > ```bash
   > cd curiana_sim && python -c "import curiana_lexicon as L; print(len(L._RAICES_VERB))"
   > ```

2. **El comodín de longitud del detector de aspecto** (d21.1, opción C). La
   condición era `suf in {ka, ni, da} and (raiz in _RAICES_VERB or len(raiz) >= 3)`:
   **`-ka`/`-ni`/`-da` sobre cualquier raíz con guion de tres letras, sin
   comprobar que hubiera verbo debajo**. De **62.347 detecciones en toda la
   base, 20.165 entraban por ahí** (`hamaka-chaa-ni`, `kali-barsure-da`,
   `baro-ni`, `pütchi-mara-ni`). Se sustituye por un comodín **acotado**: cuenta
   si el **último segmento antes del aspecto** es raíz verbal, que es el caso
   legítimo que el comodín cubría a ciegas (`ta-hamaka-chaa-ni` cuenta por
   `chaa`). Cerrar el agujero sin perder el compuesto es lo que el arreglo de la
   raíz de ninguna parte ya hizo en la otra puerta.

   Las cinco ramas del detector, medidas:

   ```
   detecciones totales: 62.347
     raíz verbal caquetía RECONSTRUIDA del núcleo      40.315
     COMODÍN DE LONGITUD (ningún verbo de por medio)   20.165
     raíz verbal caquetía ATESTIGUADA                   1.856
     aglutinado (naaka, masaka)                            10
     raíz verbal LOKONO                                     1
   ```

> ⚠️ **EL COMPONENTE DE ASPECTO ESTÁ SATURADO** (d21.3, opción A). Media de
> **1,9982 puntos por respuesta sobre un máximo de 2,0**. El 20 % del score **no
> separa a nadie** — es la misma trampa que `pct_caquetio` (issue #69) en otro
> quinto de la métrica, y no estaba escrita. **No uses el aspecto para comparar
> agentes.**
>
> Y tapar el comodín **no arregla la saturación**: la mueve a **1,9296**, cambia
> el punto en **211 de 3.379 respuestas** y deja **21** sin aspecto ninguno.
> **El peso NO se cambia en esta tanda** —eso es un rediseño de la métrica y
> necesita su propio diseño en `5-experimento/disenos/`—, pero **se vuelve a
> medir después de aplicar las dos correcciones**: al exigir verbo de verdad, la
> saturación puede caerse sola. Si sigue saturada con el número nuevo, se abre
> el rediseño.
>
> **Medido después del corte 13, y NO se cayó sola.** Sobre las 3.379 respuestas
> de la base: media **1,9982 → 1,9532**, y **95,59 %** siguen en el tope (antes
> 99,82 %); cambian 143 respuestas y 9 quedan sin aspecto. Cae **menos** que el
> 1,9296 que la auditoría estimaba para «tapar el comodín», y por una razón
> buena: la opción C de d21.1 cuenta el aspecto cuando el **último segmento**
> antes del sufijo es verbo, y eso recupera los compuestos que sí llevan verbo
> dentro (`ta-hamaka-chaa-ni` sigue contando por `chaa`). En la serie C la media
> queda en 1,9271. **El aspecto sigue sin separar a nadie: el rediseño del peso
> (opción B) queda abierto**, con su propio diseño. Medición:
> `6-fusion/medicion_tanda_21_2026-09-21.yaml` §`d21_3_saturacion`.

---

## 13. Morfemas propuestos, aún no incorporados

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
'costa, orilla' y `waka` → `sawaka` 'inframundo'. **Y uno es el que corrige la
función declarada de un prefijo del motor**: el `ka-` 'hay, existe' de §8, que
es la base del §6 de esta nota.

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

Despejados de ecuaciones bilingües; el método está en [[toponimia]] y en
[[03_descomposicion_toponimica]].

| Morfema | Glosa | Estado | Recurrencia |
|---|---|---|---:|
| `-bacoa` | bosque, arboleda | **incorporado** al motor (2026-09-14); migra al lema fonémico `-bakoa` con el corte (§4) | 5 |
| `-are` | 'sitio de' (locativo) | **abierto** — glosa en disputa con el `-ure` de van Buurt. La próxima D9 | 5 |
| `ada-` | árbol | **nuevo**, con cognado lokono `ada` | 2 |
| `bari-` | rojizo, turbio | reagrupado | 2 |
| `yacare` | pueblo, poblado | **nuevo** | 2 |
| `wa-` | pluralidad / 'tener' | corroborado; incorporado como posesivo | 2 |

Y cuatro **sin glosar que el scorer no ve** (patología (b) del §3):
`-shi`/`-chi` (22 apariciones, **el formante más frecuente del corpus insular y
nadie lo ha glosado** — el objetivo nº 1 de cualquier minería futura de
toponimia ABC), `-ari`/`-ri` (7), `-kuri`/`-curi` (3) y `-bari` (3, que
`INDICE_FUENTES` ya concluyó que **no es afijo**).

---

## 14. Las deudas que esta nota deja abiertas

- **D11 fase 3 es el nudo.** Nueve de los 21 morfemas y el 100 % del aspecto y
  de la posesión dependen de ella. Ver
  [[decision-d11-fase3-nucleo-lokono-achagua]].
- **`-gua` sin procedencia**, con campaña corta abierta (§7).
- **`-shi`/`-chi`, 22 apariciones, sin glosar** (§13).
- **`-are` vs. `-ure`**, la próxima D9 (§8).
- **La reduplicación**, medida con control y no implementada (§9).
- **`-bi`, el segundo diminutivo** de [[van-buurt-2014]] §6, sin adjudicar.
- **La categoría `adj` de 11 entradas**, que probablemente son estativos (§5).
- **El arte del achagua sin minar.** `6-fusion/achagua_neira_ribero_1762.yaml`
  §arte: del arte (pliegos 7-27) se sacaron **sólo** pronombres y numerales; las
  declinaciones, las seis conjugaciones, los tratados, los capítulos de
  «equívocos» y el verbo sustantivo quedan sin minar. Para las clases de verbo,
  la nominalización y la posesión **es la fuente que falta** — y es de los
  Llanos, así que entra como comparanda marcada, nunca como canon costero
  (regla 4).

---

## Enlaces

[[lexicon]] · [[toponimia]] · [[metodo-comparativo]] · [[datos-de-lengua]] ·
[[mapa-motor]] · [el tablero de decisiones](https://github.com/miguelgilurbina/curiana-radio/issues?q=is%3Aissue+label%3Adecision) ·
[[zavala-reyes-2015]] · [[van-buurt-2014]] · [[gatschet-1885]] ·
[[perea-alonso-1942]] · [[neira-ribero-1762]] · [[alvarado-1921]] ·
[[gonzalez-batista-nombre-de-coro]] · [[velasco-2015-resistencia]] ·
[[03_descomposicion_toponimica]]
