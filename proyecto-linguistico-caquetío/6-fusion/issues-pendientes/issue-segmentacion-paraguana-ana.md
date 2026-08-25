`-ana` está como atestiguado y su único caso sólido no descompone

## El problema

`2-lengua/morfologia.md` §3 marca **`-ana` 'lugar de' como `atestiguado`**, con
dos apoyos: *paraguana* y *curiana*. `2-lengua/toponimia.md` es más explícito
todavía: llama a `paraguana` **"el caso que sostiene `-ana`"**.

Los dos apoyos son frágiles, y el principal probablemente esté mal segmentado.

## 1. La segmentación actual no explica la glosa, y el propio registro lo admite

`2-lengua/toponimos.yaml`, entrada `toponimo-018`:

```yaml
forma: "paraguana"
glosa_fuente: "Rodeada del mar"
segmentacion: "para(gua) + -na"
razon: "corrobora para/paragua = 'mar'. Pero 'rodeada' no queda explicada
        y -na es demasiado frecuente (34 formas) para significar nada demostrable."
```

`paragua` 'mar' + `-ana` 'lugar de' daría *'lugar del mar'*. Zavala dice
**"Rodeada del mar"**. El 'rodeada' se queda sin origen, y la nota lo reconoce.

## 2. Hay una segmentación que sí cierra, con tres morfemas ya atestiguados

Las tres están en el glosario de Zavala **y ya en nuestro lexicón** como
`caquetío-atestiguado`:

```
190. Para (E)(HP): Aguadulce o salada en grandes cantidades.
122. Gua      (HP): Conuco, heredad, terreno cercado con algo.
184. Na       (HP): Partícula equivalente a "como" o "semejante".
---
192. Paraguaná (GC): Rodeada del mar.
```

`para` + `gua` + `na` ≈ **"a manera de tierra cercada por el mar"**. El 'rodeada'
sale de `gua` = 'terreno **cercado**', no de un locativo. Y `-ná` no es 'lugar
de': es la partícula comparativa que ya tenemos glosada como "como, semejante a".

Teníamos las tres piezas y no las usamos.

## 3. 🔴 El acento se perdió al registrar, y era el dato que distinguía

La fuente imprime **`Paraguaná`**, con tilde. `toponimos.yaml` guarda
`forma: paraguana`, sin ella.

Eso importa porque abre una hipótesis que hoy **no es testeable con nuestros
propios datos**: que `-ana` (átona) y `-aná` (tónica) sean morfemas distintos —
locativo el primero, partícula comparativa el segundo. Si es así, `Curiana` y
`Paraguaná` no comparten sufijo, y la coincidencia gráfica que sostiene `-ana`
es un artefacto de haber borrado el acento.

**Acción mínima e independiente de todo lo demás: auditar las tildes de las 74
entradas de `toponimos.yaml` contra sus fuentes.** `Cariatávo` conservó la suya,
`paraguana` no. Es pérdida silenciosa de dato.

## 4. Qué queda de `-ana` si esto se acepta

- *paraguana* → deja de sostenerlo (pasa a `para-gua-ná`).
- *curiana* → es la única que queda, y es una entrada con **`fuente: caquetío`,
  sin capa epistémica declarada**, glosada desde una nota al pie de Zavala
  («territorio donde estaban asentados los caquetíos»). Su segunda glosa en
  nuestro lexicón, «lugar del cardón», **no sale de ninguna fuente localizada** —
  igual que el `coro` = 'cardón grande' que D10 ya degradó por eso mismo.

Un morfema con etiqueta `atestiguado` puede quedarse con **cero casos sólidos**.
Por la regla 2, en duda se degrada.

## ⚠️ La objeción honesta: el orden del compuesto no cuadra

En `capubana` (#61 'duende del cerro' = `capu` 'demonio' + `bana` 'cerro') el
**núcleo va primero**. Si `paraguaná` siguiera ese patrón sería 'mar cercado' =
un golfo, no una península. Para que dé 'tierra cercada por el mar', `gua` tiene
que ser el núcleo y `para` el modificador — orden inverso.

**Uno de los dos análisis tiene el orden al revés.** Resolverlo requiere medir el
orden en más compuestos del glosario (`guadabacoa`, `guamabatriba`, `darubana`,
`yarosabana`, `curicuriro`). Es la pieza que falta y no debería decidirse sin ella.

## Propuesta

1. Degradar `-ana` de `atestiguado` mientras no tenga un caso que descomponga.
2. Registrar `para-gua-ná` como segmentación alternativa **con su objeción de
   orden anotada**, no como sustituta directa.
3. Auditar las tildes de `toponimos.yaml` (independiente, hazlo ya).
4. Declarar la deuda de `curiana`: capa epistémica sin declarar + glosa 'lugar
   del cardón' sin procedencia.
5. Medir el orden núcleo/modificador en los compuestos del glosario.

Relacionado: #38 (D9, `-bana`), #33 (D2, el nombre "Curiana").

---
*Verificado contra `fuentes_caquetios/Palabras Vivas de una Lengua Muerta.pdf`
(`pdftotext -enc UTF-8 -layout`). Números de entrada del glosario, no de página.*
