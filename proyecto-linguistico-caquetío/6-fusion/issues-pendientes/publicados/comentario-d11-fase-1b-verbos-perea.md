# Comentario para D11 (#39) — fase 1b: el verbo de Perea, 2026-09-12

> Borrador para el tablero. Lo publica Miguel (regla 10). Va después del
> comentario de la fase 1 (2026-09-11, ratio 2,8 → 1,7).

**Fase 1b fusionada.** El capítulo del verbo de Perea 1942 (pp. 609-684) trae,
entre los paradigmas de Schumann, su **vocabulario verbal** (ms. 1755): 239
verbos con glosa y página, 218 fusionados como `fuente: lokono`. El lexicón
pasa de 1.676 a 1.894 entradas y la columna lokono de 448 a 666.

| | fase 0 (2026-08-31) | fase 1 (2026-09-11) | **fase 1b (2026-09-12)** |
|---|---|---|---|
| wayunaiki | 781 | 781 | 781 |
| lokono | 275 | 448 | **666** |
| ratio | 2,8 : 1 | 1,7 : 1 | **1,17 : 1** |

Cifras del `TABLERO.md` generado; no copiarlas a mano.

**Lo que aporta que no había:** los estativos (colores, tamaños, sabores:
`cule-n` rojo, `subu-le-n` verde, `seme-n` dulce, `hebbe-n` viejo, `ùsa-n`
bueno), las acciones sobre el medio (pescar con nasa, cazar con flechas de
madera, plantar, salar, hilar, tejer), el futuro `-pa` con paradigma, y el
segundo juego de pronombres (sujetos pospuestos `de, bu, i, n, u, hu, ye`).
Detalle: `6-fusion/lokono_verbos_perea_1942.yaml` y
`6-fusion/lokono_gramatica_perea_1942.yaml` §`verbo_paradigmas`.

**Lo que se rompió y se arregló:** el test del orden lokono > wayuu se puso en
rojo, y era la **ortografía** de Perea, no el dato — su `ù` se borraba al
normalizar y sus geminadas (que él declara sin valor, p. 546) inflaban los
clusters. Arreglado en `curiana_fonotactica.py`, sólo para Perea (en wayuu la
geminada contrasta). Lokono pasa al 86 %, wayuu sigue en 65 %.

**Para la decisión:** si 1,7 a 1 bastaba, 1,17 a 1 basta más. La fase 2
(achagua) sigue pendiente de conseguir Neira y Ribero 1762 o Fabo 1911. La
fase 3 (re-derivar el núcleo) tiene ahora el paradigma pronominal lokono
completo y el futuro `-pa` para hacerlo, si se decide.
