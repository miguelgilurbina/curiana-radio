# La clase estativa: declararla, que hoy se hereda por accidente

**Para que Miguel la fusione a `2-lengua/morfologia.md`.** La clasificación de
las 49 raíces YA está aplicada en el minador y medida; lo que falta es lo que un
minador no puede escribir: **qué es un estativo en este proyecto**.

> ⚠️ **No se escribió en `morfologia.md`.** Otro agente está auditando la
> morfología entera en paralelo (2026-09-20). Lo de abajo pide una **sección
> nueva**, entre §2 («Reglas de trabajo del proyecto») y §3 («`-bana` vs
> `-ana`»), y no toca ninguna de las existentes.

---

## 1. De dónde sale esto

En `curiana_sim/minar_zavala_glosario.py` la parte de la oración de todo el
vocabulario activo salía de **una línea**:

```python
_CAT_POR_TIER = {"T4_abstracto": "v_raiz"}   # heurística de POS; el resto, sust
```

T4 es el **cajón de resto** del minador: lo que el regex `re_concreto` no
reconoció como cosa. De ahí salían **49** entradas con `cat: "v_raiz"`, y de
`cat: "v_raiz"` sale `curiana_lexicon._RAICES_VERB`, que hace que
`score_linguistico()` cuente como arahuaco **cualquier token cuyo primer
segmento sea una de ellas**.

**Y la corrección de Miguel es la que hace falta aquí:** no es que cuarenta no
sean verbos. En arahuaco mucho de lo que el castellano llama adjetivo **es un
verbo estativo**, así que `apo` 'grande', `usera` 'seco, arenoso', `waidima`
'íntegro', `kachipo` 'enojado', `patapati` 'anegadizo' y `waranao` 'salado'
pueden estar bien con `v_raiz` — **sólo que hoy están bien por accidente**, por
haber caído en el cajón de resto. Diez de las 49 son de esa clase. Para que
dejen de estarlo por accidente, la clase hay que declararla.

## 2. La sección propuesta

> ### N. Los estativos: lo que el castellano llama adjetivo
>
> Un **estativo** es una raíz cuyo significado es una **propiedad o un estado**
> —tamaño, sabor, color, edad, condición del terreno, estado de ánimo— y que en
> arahuaco **se conjuga como verbo**, no se usa como adjetivo. En el canon del
> proyecto lleva `cat: v_raiz`, entra en `_RAICES_VERB` y admite los tres
> aspectos (`-ka`, `-ni`, `-da`) como cualquier otro verbo.
>
> **La evidencia.** [[perea-alonso-1942]] describe la **4ª conjugación** lokono
> —infinitivo en `-en`— como «la clase de los estativos: colores, tamaños,
> sabores, estados», con tres ejemplos impresos: `cule-n` 'ser rojo', `ibe-n`
> 'estar lleno', `hebbe-n` 'ser viejo' (pp. 634-639). Su pronombre sujeto va
> **pospuesto** en forma complementaria (`de, bù, i, n, u, hù, ye`), no
> prefijado como en los transitivos (p. 635) — que es el dato que §2 de esta
> misma nota ya cita. Y en pp. 598-599/608 está la regla que los fabrica:
> «cualquier nombre, adjetivo o partícula se hace verbo anteponiendo `a-` o
> `c-`». Perea lo dice sin rodeos: «rojo» no es un adjetivo en lokono, es el
> verbo `cule-n`. **Buscar «adjetivos» sueltos es buscar en la categoría
> equivocada.**
>
> La achagua de [[neira-ribero-1762]] hace lo mismo sobre una raíz, con el
> atributivo `ca-`/`ka-`: `cabareuno` 'enojarse' / `cabarecayi` 'colérico' /
> `cabareumí` 'es bravo'; `carruicay` 'espanto' / `carrunatacayi` 'espantoso'.
> Y con el privativo `ma-`: `macarray` 'seco' / `macarracataní` 'seco, estando
> seco'.
>
> **La frontera de la clase.** Lo que **no** es un estativo es un **nombre**, y
> un nombre no se predica con aspecto sino con el atributivo/existencial `ka-`
> («hay, existe(n)», *Casibari* = 'hay rocas duras', [[van-buurt-2014]] §8) o
> con el privativo `ma-`. Por eso la prueba práctica es ésta: **si para decirlo
> en presente hace falta `ka-`, no es estativo**.
>
> **Lo que NO se afirma.** El pronombre pospuesto del lokono **no** se propone
> para el caquetío. El canon no tiene ni un pronombre atestiguado y los cinco
> que usa son reconstruidos del wayuu (D11). Que el lokono ponga el sujeto
> detrás en los estativos es la razón **tipológica** para reconocer la clase,
> no una forma que se importe: proponer `apo taya` 'yo (soy) grande' sería
> re-derivar el núcleo desde el lokono, que es **D11 fase 3** y está abierta.
>
> **Los diez estativos declarados** (glosario de [[zavala-reyes-2015]], con su
> apoyo por fila en `lexicon_zavala.CLASES_DE_RAIZ_ZAVALA`):
>
> | Raíz | Glosa de la fuente | Apoyo más directo |
> |---|---|---|
> | `apo` | Grande | LK `ipi-lli-be` 'ser grande' (v_raiz en el lexicón) |
> | `bachure` | Maneto, patituerto | LK `hiccu-li` 'ser cojo' |
> | `kachipo` | En voz vulgar, enojado, colérico | ACH `cabareuno` 'enojarse' |
> | `etamo` | Feroz, feo, espanto | ACH `carruicay`/`carrunatacayi` |
> | `waidima` | Integro | WY `waneepiaa` **'ser entero'** |
> | `waranao` | Salado, ácido | WY `palawaa` **'ser salado'** |
> | `wasima` | Viejo, anciano | LK `hebbe` **'ser viejo'** — ejemplo impreso de Perea |
> | `patapati` | Anegadizo | tipológico; `deuda: sin-procedencia` |
> | `sinwanguso` | Insolente | tipológico; `deuda: sin-procedencia` |
> | `usera` | Seco, arenoso | WY `josoo` **'estar seco'**; ACH `macarray` |
>
> Las tres marcadas en negrita son el apoyo fuerte: **el propio lexicón ya
> glosa esas voces hermanas en forma verbal** («ser entero», «ser salado»,
> «estar seco»), o sea que el proyecto ya sabía que el concepto es un verbo —
> sólo que no lo había dicho del caquetío.

## 3. La tensión que esto destapa, y que NO se resuelve aquí

`curiana_lexicon.py` tiene además una categoría **`adj`, con 11 entradas**:
`anasa` 'bueno', `tüshi` 'frío', `mütsia` 'negro', `kasuta` 'blanco', `sünatü`
'rojo', `tsipana` 'verde', `kanawa` 'amarillo', `siwato` 'desganado'… casi todas
**reconstruidas del wayuu**.

Son exactamente los «colores, tamaños, sabores» que Perea llama estativos, y
están en la categoría equivocada **por el mismo motivo que las 49**: nadie la
declaró. `sünatü` 'rojo' es, palabra por palabra, el `cule-n` de la p. 634.

**No se tocan en esta tanda**, por dos razones:

1. Viven en el **literal** de `curiana_lexicon.py`, que es canon y que un
   minador no toca (regla 5).
2. Moverlas a `v_raiz` las metería en `_RAICES_VERB` y **volvería a mover el
   score** — este corte ya mueve 84 y 93 respuestas de 216. Dos cortes en la
   misma tanda no se pueden leer por separado.

Es una **segunda tanda**, y conviene que sea después de que la auditoría de
morfología que corre en paralelo cierre.

## 4. Qué pide esta propuesta

- [ ] Fusionar la sección N a `2-lengua/morfologia.md` (o la versión que salga
      de la auditoría en curso).
- [ ] Decidir si la categoría `adj` del literal se unifica con la estativa, y
      en qué tanda.

Datos y contexto: `6-fusion/clases_de_raiz_zavala_2026-09-20.yaml` §1.
Números del corte: `6-fusion/medicion_clases_de_raiz_2026-09-20.yaml`.
Corte declarado: punto 12 del «Cambio de instrumento» de
`5-experimento/BITACORA_RUNS.md`.
