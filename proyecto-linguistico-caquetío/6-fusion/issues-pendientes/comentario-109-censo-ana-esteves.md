## El censo de -ana en Esteves está hecho: cero casos de 'lugar de'

El comentario del 2026-08-25 puso la condición de cierre: «lo que zanjaría si
`-ana` 'lugar de' tiene diez casos o tiene uno son los topónimos de Esteves
1989, sin minar». Los tres volúmenes tienen OCR desde el 2026-09-06 y el censo
se hizo el 2026-09-07 (`6-fusion/censo_ana_esteves_109.yaml`, con página por
forma).

### Lo medido

De las 186 formas del índice de Esteves, **13 terminan en -ana/-aná**:

| Clase | n | Cuáles |
|---|---|---|
| son `-bana` (#38) | 6 | Judibana, Carirubana, Coabana, Chichibana, Pipiribana, Tausabana |
| `-bana` con h intercalada | 1 | Capuhana = Capu-hana, «Bana: cerro» (p. 26) |
| el -ana está dentro de una raíz | 2 | Cariguariana (< *guariana* 'arbusto', p. 28), Maracapana (< 'totumitas', p. 51) |
| sin glosa | 4 | Paraguaná, Chamuriana, Cujicana, Jayana |
| **glosadas 'lugar de'** | **0** | — |

Cuando Esteves quiere decir 'lugar de' usa **`bacoa`**: Curumubacoa «lugar de
los zamuros» (p. 33), Tutubacoa «el lugar de los tuturutos» y Datobacoa «lugar
de los datos» (p. 66), Guaidabacoa «bacoa: sitio, paraje». Ni una vez -ana.

### Lo que Esteves sí da para Paraguaná (p. 56)

> «Conuco en medio del mar es la más repetida de las significaciones que le
> dan al topónimo. Está suficientemente averiguado que Para significa agua.»

Morfema a morfema, 'conuco en medio del mar' es `para` 'agua' + `gua` 'conuco,
heredad, terreno cercado' (Zavala #122, HP): **la segmentación `para-gua-ná`
de este issue, por una vía independiente de Zavala** y veintiséis años antes
de que la conociéramos como etimología «tipo Wikipedia». Sigue sin morfema el
'en medio de' / 'rodeada'. Registrado como tres lecturas en `toponimo-018`.

### La objeción de orden, medida

El issue objeta que en *capubana* «duende del cerro» (Zavala #61) el núcleo va
primero, y que `para-gua-ná` daría entonces 'mar cercado' (un golfo). En los
seis compuestos en -bana que Esteves glosa, **el núcleo va al final en cinco**
(Judibana 'cerro del viento', Coabana 'cerro de las coas', Achichibana 'cerro
de los achechives', Tautabana 'cerro de las palomas', Capuhana 'el cerro del
duende'); la excepción, Carirubana 'orilla del cerro', admite igual 'cerro de
la orilla'. Y Capuhana **es el mismo compuesto que capubana**: Zavala lo glosa
'duende del cerro', Esteves 'el cerro del duende' con el referente a la vista
(«un pequeño cerro, cerca de Misaray»). El referente decide por Esteves. Con
núcleo final, `para-gua-ná` es 'conuco de agua', no un golfo.

Cautela: son segmentaciones de cronista, no dato independiente. Vale que el
patrón sea consistente y que el referente de Capuhana esté dicho.

### Un dato colateral de Oliver (cap. 3 p. 207), en los dos platillos

Entre los nombres de aldea **wanebucán** de Punta Espada–Chichibacoa (Guajira)
Oliver lee morfemas «suspiciously Caquetío»: **«Paragua-nil» y «Coria-na»**, y
lo explica por el nexo comercial con los caquetíos de allí. A favor: `-na` es
sufijo también para él, y los formantes viajan con el comercio (un segundo
*Coriana*, fuera de Coro: toca #33). En contra: Oliver corta **`paragua`
entera** como raíz (Zavala #191 'mar'), no `para` + `gua`; si el paralelo vale,
Paraguaná es `paragua` + `ná` y el 'conuco' de Esteves vuelve a quedarse sin
morfema. Ninguna de las dos lecturas cierra sin residuo.

### La auditoría de tildes (punto 3 del issue), hecha

Contra Esteves (índice, 34 formas en canon) y Zavala (glosario): tres
discrepancias, corregidas en `lexicon_toponimos.py` y regeneradas:
`paraguana` → **`paraguaná`** (Zavala #192, Esteves p. 56), `caquetio` →
**`caquetío`**, `aburi` → **`aburí`** (Zavala #1). Los ids no cambian.

### Lo que queda es decisión, no trabajo

`-ana` sigue como «forma atestiguada, glosa 'lugar de' en disputa». Con el
censo a cero, las opciones:

- **A.** Mantener «en disputa» y esperar Medina Colina y el barrido del mapa.
- **B.** Retirar la glosa 'lugar de': `-ana` pasa a `FORMATIVOS_SIN_GLOSA`
  (forma atestiguada, significado sin apoyo); Paraguaná deja de sostenerla;
  Curiana queda con su expediente propio (#33, D2).
- **C.** Aceptar `para-gua-ná` como segmentación principal de Paraguaná
  (nivel B) con el residuo 'en medio de' declarado.

Recomendación del proyecto: **B**, y C solo como lectura (ya está) hasta que
aparezca el morfema del 'rodeada'.

---
*Medido sobre `fuentes_caquetios/Esteves_1989_Toponimos_Paraguana_{1,2,3}.ocr.txt`
(pdf → impresa: +6 / +25 / +55); cada entrada leída en su página. Zavala:
`pdftotext -enc UTF-8 -layout`.*
