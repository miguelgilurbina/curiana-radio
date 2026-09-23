# Ampíes sobre Manaure: «se hace adorar como Dios» o «como digo»

**Fecha**: 2026-09-23 · **Rama**: `campana/mineria3-perez-de-tolosa`
**Datos**: [`6-fusion/perez_de_tolosa_1546_2026-09-23.yaml`](../perez_de_tolosa_1546_2026-09-23.yaml) §`cotejo_ampies`
**Label propuesto**: `decision`

---

## El problema

La carta de Juan de Ampíes al Rey (c. 1525-1526) es la única fuente primaria
de que el gran cacique de Coro se hacía adorar y «daba los temporales». En el
repo hay **tres lecturas de esa misma carta**, y no coinciden:

| Lectura | Qué dice | De dónde |
|---|---|---|
| Fernández Duro 1885, t. II **p. 212** (verificado en imagen) | «el cual por ser tan gran señor se hace adorar **como Dios**, dando á entender á los indios que él da los temporales» | el impreso; no localicé en el tomo de qué copia viene |
| Velasco 2015, «Folio 14» | «por ser tan gran señor se haze adorar **como digo** dando a entender a los indios q el da los temporales» | el manuscrito del AGI (`4-fuentes/velasco-2015-resistencia.md` §2) |
| Arcaya 1920 **p. 161** | «…se llama Naure o Anaure,. . . . e luego yo enbié…» | **se salta la frase**: dice copiar de Fernández Duro |

Con «como Dios», Ampíes dice que el cacique se hace adorar **como un dios**.
Con «como digo», dice que se hace adorar, y punto. Lo que **no** cambia: «se
hace adorar» y «él da los temporales», que es lo que usan `creencia-013` y el
Capubana de `clima_era2.yaml`.

Son tres lecturas de **una** atestación (`minar-fuente` §8). Arcaya depende de
Fernández Duro; Fernández Duro y Velasco leyeron cada uno por su lado.

## Lo que ya está en el canon y lo que se movería

- `creencia-013` («al cacique teocrático se le atribuye poder sobre las lluvias
  y las tormentas») cita «crónicas del contacto sobre Manaure»: **no cambia**
  con ninguna de las dos lecturas, pero le falta la cita primaria.
- Quien quiera escribir que a Manaure lo adoraban «como a un dios» tiene
  **sólo** la lectura de 1885, y en contra una lectura del manuscrito.

## Opciones

- **A — Citar las dos y no decidir.** `creencia-013` pasa a citar la p. 212 de
  Fernández Duro y el folio 14 vía Velasco, con la variante en `notas`, y nada
  del canon se apoya en «como Dios». *Recomendada mientras no se vea el
  manuscrito.*
- **B — Ver el manuscrito.** Pedir la imagen del folio 14 al AGI (PARES) o a
  Velasco, y decidir con ella. Es la única salida que resuelve.
- **C — Seguir a Velasco («como digo»)** porque leyó el manuscrito. No se
  recomienda sin ver la imagen: la ficha de Velasco ya anota que atribuye cosas
  sin cita (el nombre «Judibana»).

**Recomendación: A ahora, y B cuando se pueda.** Mientras tanto, ningún
contenido del corpus debe decir «adorado como un dios» apoyándose sólo en esta
carta.

## De paso, lo que el cotejo corrigió

- El pasaje está en la **p. 212**, no en la 209 (`antroponimos_caquetios.yaml`
  heredó la 209 de la nota 3 de Arcaya p. 160, que da la página donde **empieza**
  la carta).
- La carta dice que Baracoica «es su pariente y deudo» de los indios de la
  costa. «Hijo del mismo Manaure» es de Arcaya p. 199, sin fuente allí.
- La hija del gran cacique **no tiene nombre** en la carta; «Judibana» es de
  Velasco (ya anotado en su ficha).
