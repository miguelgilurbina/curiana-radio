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
estado_minado: minada-parcial
cobertura: "medida, no escrita a mano: `6-fusion/achagua_neira_ribero_1762.yaml` → `meta.cobertura` (pliegos leídos, letras vistas, entradas, dudas, resultado de la calibración) y `meta.censo_de_terminaciones` (la `-are`/`-re`). Las cifras las emite `construir.py`; si se vuelve a minar, se regeneran"
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
recorte a recorte (media página por recorte, ~12 entradas cada uno). Cada
pliego JPG trae DOS páginas; se recorta por mitades con `pymupdf`
(`get_pixmap(matrix, clip)` sobre el JPG abierto como documento; factor
píxel/punto 4,167).

### Índice de pliegos (leído en hojas de contacto el 2026-09-12)

| Pliegos | Qué hay |
|---|---|
| 1-5 | tapas, guardas, hojas en blanco |
| 6 | portada («Arte y Vocabulario de la lengua Achagua. Doctrina Christiana, Confessonario… Trasumptado en el Pueblo de San Juan Francisco Regis, año de 1762») y la nota de la copia de 1788 |
| 7-27 | **el ARTE**: prosa gramatical con paradigmas; en el 11 se ven tablas (¿pronombres/declinación?), del 17 al 27 «Reglas» y «Tratados» numerados |
| 28 (dcha.) | empieza el **VOCABULARIO castellano → achagua**, «Castellano A Achagua» |
| 28-98 | el vocabulario entero, alfabético por el castellano, dos columnas, ~28 líneas por página. Cabeceras de letra vistas: B 40 · C 44 · D 52 · E 57 · F 63 · G 65 · H 66 · J 71 · L 73 · M 77 · N 78 · O 79 · Q 86 · R 87 · S 90 · T 93 · V 96 |
| 98 | última página escrita, con colofón |
| 99-102 | blancas y guarda |

⚠️ En esta copia **no aparece** ni la parte achagua → castellano ni la
doctrina/confesionario que anuncia la portada: 71 pliegos de vocabulario ≈ 141
páginas ≈ los 70 folios del catálogo, y se acaba. Estimación: ~4.000 entradas.

### Cómo consumirlo, en orden

1. **Calibrar con las 34 de Jahn/Fabo** (`6-fusion/comparandas_jahn_1927.yaml`):
   buscar cada concepto castellano en su letra, transcribir y comparar. Si
   las 34 cuadran, la cadena Neira → Fabo → Jahn queda medida.
2. **El arte**: pronombres y numerales (pliegos 7-27) — el núcleo que D11
   quiere re-derivar sin depender del wayuu.
3. **La terminación `-are`/`-re`**: censo sobre la columna achagua.
4. **El resto**, letra a letra, a `6-fusion/achagua_neira_ribero_1762.yaml`
   con `transcripcion: lectura en imagen, verificar` en cada entrada (regla 2).

Alternativa si se quiere OCR de verdad: Transkribus tiene modelos públicos de
HTR para cursiva española del XVIII; exige subir las 102 imágenes a un servicio
externo — decisión de Miguel, no del escriba.

## Qué preguntarle

1. Las 34 voces de Jahn/Fabo, una a una: ¿están, y con qué grafía?
2. Los pronombres y los numerales achagua — el núcleo que D11 quiere re-derivar
   sin depender del wayuu.
3. La terminación `-are`/`-re` que Fabo declara «propia y exclusiva» del
   achagua: ¿cuántas voces la llevan en el vocabulario?
4. Léxico ecológico y material: cardón, sal, canoa, pesca, maíz, yuca.

## Qué ha dado

**Primera lectura en imagen, 2026-09-12** (escriba, agente Opus 5). Todo lo leído
está en `6-fusion/achagua_neira_ribero_1762.yaml` — propuesta, no canon (regla 5).
Ni una cifra se repite aquí: viven medidas en `meta.cobertura` de ese archivo.

### Cómo se leyó

Recortes de media página a resolución nativa sobre los JPG (`pymupdf`, factor
4,167 px/pt), leídos con visión, cuatro por pliego. **Sin OCR y sin red.**

**La clave de lectura que costó media hora y hay que heredar: el copista escribe
la `r` con un glifo que parece `z` o `x`.** No hay que adivinarlo — lo dice el
propio manuscrito en el párrafo de «Pronunciación» (pliego 7, dcha.): *«la R no
la hacen erre, sino r como los Españoles, y así no dicen Riarrumirre, sino
riarrumirre»*, con las cuatro palabras escritas con ese glifo. Glifo simple = r,
doble = rr. Quien vuelva sin esto transcribirá `Vregizzayi` por `Vregirrayi`.
Va anotado en `meta.ortografia_del_copista`.

### Lo que se preguntó, y qué contestó

1. **Las 34 voces de Jahn/Fabo, una a una** — hecho, en `calibracion_jahn`, con
   pliego y lado. Veredicto por voz (`coincide` / `difiere` / `no-esta`) y el
   recuento en `meta.cobertura`. **La cadena Neira → Fabo → Jahn se sostiene en
   lo esencial**, con dos reservas que sí importan:
   - **`agua` y `río` están corridos un escalón.** Jahn da `agua = mena`,
     `río = unibe`. El manuscrito dice **`Agua — Vni`** (pliego 32) y **`Mar —
     Manoa`** (pliego 74). Es decir: lo que Fabo/Jahn llaman «agua» es el *mar*,
     y lo que llaman «río» es el *agua*. Quien haya usado `mena` como 'agua'
     comparanda estaba comparando con 'mar'.
   - **`kapauje` no es «flecha» a secas**: el manuscrito distingue
     `Flecha — Querriasui` de `Flecha con hierro — Caubasui, caubase`
     (pliego 64). `kapauje` es la segunda, o sea una voz **post-contacto**.
     Es exactamente la trampa de la regla 3, dentro de una comparanda.
   - Varias voces de Jahn **no son lemas del manuscrito** y hubo que sacarlas de
     ejemplos dentro de otras entradas: `canoa` (ida), `sepultura` (nirri),
     `tabaco` (chema), `diente` (eri), `lengua` (nuinene). El manuscrito **no
     tiene lema «Diente»** — verificado leyendo los cuatro pliegos de la D donde
     tocaría (regla 6).

2. **Pronombres y numerales** — hecho, en `arte`. Los pronombres salen del
   pliego 8 completos, absolutos e iniciales, con el paradigma de `Saricanasi`
   'padre' que enseña cómo se posee un nombre. **El arte NO tiene capítulo de
   numerales**: verificado pliego a pliego en los 12-23, que son conjugaciones
   (regla 6). Los cardinales hubo que recogerlos del vocabulario. Lo que sí hay
   al cerrar el arte (pliego 28 izq.) es «Modos de decir uno», y ahí está el
   hallazgo: **el numeral concuerda con un clasificador de clase**
   (`aba-su` pluma, `aba-coa` luna, `aba-nai` piña, `aba-bai` hacha…), y el
   manuscrito da el paradigma **completo** para 'dos' bajo el lema `Dos`
   (pliego 56). El sistema es **de base cinco sobre la mano**: `abacase` 'cinco'
   es «una mano», y de ahí salen 50, 100 y 200.

3. **La terminación `-are`/`-re` que Fabo declara «propia y exclusiva»** —
   medida, no opinada: `meta.censo_de_terminaciones`, contada por
   `construir.py` sobre las formas achagua sueltas. **La respuesta es que no.**
   Las terminaciones dominantes son `-si` (el absoluto de no-poseído, que cae en
   cuanto el nombre se posee: `Saricanasi` → `Nusaricana`), `-yi`/`-cayi`
   (adjetival) y `-ri`. La `-re` existe y es real, pero es minoritaria. La
   proporción exacta está en el YAML.

4. **Léxico ecológico y material** — sí, y más de lo que la pregunta pedía:
   `Achote — Tirri`, `Mais — Cana`, `Casabe — Jerri/Berri`, `Budare — Juari`,
   `Masato — Amu`, `Canalete — tena`, `Barbasco — Cuna`, cinco nombres de
   trampas de pesca bajo `Garlito`, y **diez peces con nombre propio** bajo
   `Pez ó pescado` (pliego 83).

### Lo que salió sin buscarlo

- **El panteón achagua, nombre a nombre** (pliego 56): el de las labranzas, el
  de las riquezas, el del fuego, el causador de temblores, el flechero, el de
  las tempestades, el de los truenos; y aparte las **diosas**, con la criadora
  de los achaguas y la madre del lucero de la tarde. Es un hecho de mundo, no de
  lengua, y no lo anunciaba ninguna ficha.
- **Astronomía**: las Cabrillas (Pléyades), el Carro del cielo, el Camino de
  Santiago (Vía Láctea), el lucero de la tarde y el de la mañana con nombres
  distintos, y un lema para el cometa.
- **Parentesco**: hermano mayor / hermano / hermano menor, cada uno con su
  **vocativo** propio (`tay`, `tau`, `Jchu`); hermano *de un vientre* aparte; y
  el marido con lema propio mientras la mujer casada solo se dice derivándola
  de él (`Canirricayo`). El **linaje** tiene nombre (`Cuisaunasi`) y va **con
  nombre de animal**: «Linage de tigre», «de Papagayos» (pliego 72).
- **Variación dialectal declarada por el propio autor**: bajo el lema `Mas`
  (pliego 74) da dos construcciones y dice *«sic in Casanare»* frente a la otra.
  El jesuita sabía que no describía una lengua homogénea.
- Seis maneras de hablar con nombre propio (a gritos, pasito, enflautado,
  predicando, gordo…), el diminutivo general `-rrimi` explicado por el autor, y
  una partícula de **reciprocidad** (`Vrriamãca`) que sirve igual para el don
  devuelto y para la ofensa devuelta.

### Qué NO se hizo

- **El vocabulario no está entero.** Se leyeron los pliegos que dice
  `meta.cobertura.pliegos_leidos`; el resto sigue sin tocar. Faltan enteras las
  letras I/J, K, Q, V/U y buena parte de A (34-39), C (50-51), D (54-55),
  H-I (68-71), M (75-77), P (80, 84-85), R (86-87, 90-91), S (93) y T (96-98).
  Por eso quedaron en `no-esta` cinco voces de Jahn: `arena`, `leña`, `león`,
  `nariz` y `esposa` — **no significa que no estén**, significa que su letra no
  se leyó (regla 6 al revés: este cero mide la lectura, no la fuente).
- **La lista alfabética de verbos de los pliegos 23-27** («Noticias necesarias…
  Partículas y verbos de este Idioma, orden Alphabético») está sin minar. Es
  prosa gramatical, no vocabulario, y es material de primer orden.
- El resto del **arte** (declinaciones, seis conjugaciones, tratados, el
  capítulo de «equívocos de esta lengua» del pliego 27) está sin minar.
- Nada se llevó al lexicón ni al corpus, y no se abrió ningún issue: esto es
  comparanda achagua y la decisión de qué hacer con ella es de D11 (#39).

## Enlaces

[[fabo-1911]] · [[jahn-1927]] · [[rivero-1883]]
