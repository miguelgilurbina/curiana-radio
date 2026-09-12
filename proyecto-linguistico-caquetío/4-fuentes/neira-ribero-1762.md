---
tipo: fuente
obra: "Arte y vocabulario de la lengua achagua"
autor: "Neira, Alonso de (S.J.) y Ribero, Juan (S.J.)"
anio: 1762
genero: gramatica
publicacion: "Manuscrito. Terminado el 14 de septiembre de 1762; la copia de la Real Biblioteca es del 23 de abril de 1788 (RBPR II/2910): [4] h. + 42 p. + 70 f. + [3] h., 152×104 mm"
local: "fuentes_caquetios/Neira_Ribero_1762_Arte_y_Vocabulario_Lengua_Achagua_RB_II-2910.pdf (102 pliegos a 2787×1949 px, sin capa de texto) + fuentes_caquetios/neira_ribero_1762/001-102.jpg — ⚠️ SOLO EN ONEDRIVE, no en git (.gitignore, D8 #37 abierta: son 200 MB)"
paginas: 102
capa_texto: no
estado_minado: sin-minar
prioridad: alta
tareas: [D11-fase-2]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-12
descargado: 2026-09-12
origen_digital: "Real Biblioteca Digital (Patrimonio Nacional), manifiesto IIIF II-2910; también en la Library of Congress (2021667801). Dominio público"
aliases: ["Neira y Ribero 1762", "Neyra y Ribero", "Arte achagua", "Arte y vocabulario achagua", "Neira 1762"]
---

# Neira y Ribero 1762 — *Arte y vocabulario de la lengua achagua*

## Por qué está aquí

Es **el diccionario del achagua**: la gramática (*arte*) y el vocabulario que
dos jesuitas de las misiones del Meta compilaron en el siglo XVII y que se
trasuntó en 1762. Todo lo que el repo tiene de achagua —las 34 voces de Jahn,
que a su vez son de Fabo— es de segunda o tercera mano; esto es la fuente.
Fase 2 de D11 (#39).

Descargado el 2026-09-12 con autorización de Miguel, imagen a imagen desde el
manifiesto IIIF de la Real Biblioteca (102 lienzos), y montado en PDF con
`pymupdf`. La copia de la Library of Congress no se pudo descargar (403).

## Qué es (por la ficha de la Real Biblioteca; sin leer todavía)

Tres piezas encuadernadas: el **arte** (gramática, 42 pp.), el **vocabulario**
(70 folios, castellano-achagua y achagua-castellano según el catálogo) y una
doctrina cristiana con confesionario. El estudio de referencia es Meléndez
Lozano 1997, «El *Arte y vocabulario de la lengua achagua*… aportes y
limitaciones» (en Zimmermann, *La descripción de las lenguas amerindias en la
época colonial*), que no está en el repo.

## Cómo se lee

✅ **Medido el 2026-09-12: se lee bien.** Las imágenes son de resolución
completa (2787×1949 px por pliego, dos páginas por imagen) y la letra del
copista de 1788 es una cursiva clara: a resolución nativa se distinguen sin
esfuerzo las entradas del vocabulario («Azul — Vregirrayi», «Baba — Errusí»,
«Bacilar — Nubedua»). Lo que no se puede es OCR: es lectura en imagen,
recorte a recorte (media página por recorte, ~12 entradas cada uno).


Manuscrito del XVIII: **no hay OCR y no va a haberlo bueno**. Se lee en
imagen, página a página, con `pymupdf` para renderizar o directamente los
JPG. Antes de minar: (1) localizar dónde empieza el vocabulario y en qué
orden va; (2) fijar la ortografía del copista (la `ch`, la `qu`, la `y`); (3)
transcribir primero las 34 voces de Jahn para calibrar, y sólo después el
resto. Es trabajo de tardes, no de una.

## Qué preguntarle

1. Las 34 voces de Jahn/Fabo, una a una: ¿están, y con qué grafía?
2. Los pronombres y los numerales achagua — el núcleo que D11 quiere re-derivar
   sin depender del wayuu.
3. La terminación `-are`/`-re` que Fabo declara «propia y exclusiva» del
   achagua: ¿cuántas voces la llevan en el vocabulario?
4. Léxico ecológico y material: cardón, sal, canoa, pesca, maíz, yuca.

## Enlaces

[[fabo-1911]] · [[jahn-1927]] · [[rivero-1883]]
