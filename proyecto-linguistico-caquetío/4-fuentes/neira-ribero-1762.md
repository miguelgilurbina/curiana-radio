---
tipo: fuente
obra: "Arte y vocabulario de la lengua achagua"
autor: "Neira, Alonso de (S.J.) y Ribero, Juan (S.J.)"
anio: 1762
genero: gramatica
publicacion: "Manuscrito. Terminado el 14 de septiembre de 1762; la copia de la Real Biblioteca es del 23 de abril de 1788 (RBPR II/2910): [4] h. + 42 p. + 70 f. + [3] h., 152×104 mm"
local: "fuentes_caquetios/Neira_Ribero_1762_Arte_y_Vocabulario_Lengua_Achagua_RB_II-2910.pdf (102 pliegos a 2787×1949 px, sin capa de texto) + fuentes_caquetios/neira_ribero_1762/001-102.jpg — ⚠️ SOLO EN ONEDRIVE, no en git (.gitignore, por D8 #37 — cerrada el 2026-09-12 con la opción intermedia: son 200 MB)"
paginas: 102
capa_texto: no
estado_minado: minado
cobertura: "LEÍDA ENTERA la copia: vocabulario (pliegos 28-98) y arte (pliegos 7-28 izq.). El vocabulario y el arte de las pp. 33-42, medidos en `6-fusion/achagua_neira_ribero_1762.yaml` → `meta.cobertura` y `meta.censo_de_terminaciones` (los emite `6-fusion/scripts/ensamblar_achagua_neira_ribero.py`). El arte de las pp. 1-32 (declinaciones, conjugaciones, pasiva, géneros, pretéritos, sintaxis, posesión), en `6-fusion/achagua_arte_neira_ribero_2026-09-22.yaml` (2026-09-22/23), con cifras en `6-fusion/medicion_arte_achagua_2026-09-22.yaml`. Quedan PREGUNTAS, no páginas: censo de tainismos del lado castellano, censo de préstamos marcados por el autor, y una segunda lectura independiente del arte"
prioridad: alta
tareas: [D11-fase-2]
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-23
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
| 28-98 | el vocabulario entero, alfabético por el castellano, dos columnas, ~28 líneas por página. Cabeceras de letra vistas: B 40 · C 44 · D 52 · E 57 · F 63 · G 65 · H 66 · J 71 · L 71 dcha. (al pie) · M 77 · N 78 · O 79 · Q 86 · R 87 · S 90 · T 93 · V 96 |
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

---

**Segunda lectura en imagen, 2026-09-12** (escriba, agente Opus 5). Misma
técnica, mismos recortes, misma clave de lectura heredada — la `r` con glifo de
`z` —, y ahora con aumento a 2-3× sobre la línea cuando no se decidía. Todo
sigue en `6-fusion/achagua_neira_ribero_1762.yaml`; las cifras siguen medidas en
`meta.cobertura`, y las emite ahora
`6-fusion/scripts/ensamblar_achagua_neira_ribero.py`.

### Lo que cierra

**El vocabulario está leído de punta a punta.** Se leyeron los 31 pliegos que
faltaban (33-39, 42-43, 50-51, 54-55, 68-71, 75-77, 80, 84-87, 90-91, 93,
96-98) y ya no queda hueco entre el 28 y el 98 — lo comprueba el propio script,
que mide los huecos en vez de creerse la lista. Entran enteras I/J, Q, V/U, X y
Z, y se cierran los huecos de A, C, D, H, M, P, R, S y T.

**No hay letra K**: de la J se pasa a la L, y las dos cabeceras están en el
mismo pliego 71. De paso, la tabla de cabeceras de la ficha estaba corrida: la
L no empieza en el 73 sino al pie del 71 dcha.

**La lista alfabética de verbos del arte (23 dcha.-26 izq.) está minada**, y
con ella los dos capítulos que la siguen: el del verbo sustantivo (26) y el de
los «equívocos de esta lengua» (27). Viven en `arte.verbos`.

**De las 14 dudas, diez quedan resueltas y dos a medias.** Las que no: la voz
de las hormigas que comen los achaguas (pliego 79) y el final de `Jbai-` bajo
«Haz» (66).

### Lo que corrige a la primera pasada

- **El lema «Diente» sí existe** (pliego 55 dcha.), y trae el paradigma
  posesivo entero: `Erí` / `Nue` mío / `Je` tuyo / `re` / `que` / `Ne`. La
  primera pasada lo dio por ausente «verificado leyendo 52, 53, 56 y 57» — pero
  los pliegos 54 y 55 no se habían leído. Es la regla 6 en su forma exacta: un
  cero que medía la lectura, no la fuente. La regla vale también al revés, y
  aquí costó una afirmación falsa.
- **De las cinco voces de Jahn que quedaron `no-esta`, cuatro aparecen**:
  `arena` = *Caina* (37), `nariz` = *Dacusí* (77, y el `nutako` de Jahn es su
  forma poseída `nu-dacu`), `esposa` = *Nuinu* (76), `leña` = *Sichaba* (70,
  degradada a `difiere` por la consonante inicial). Solo `león` sigue sin
  aparecer, y ahora ese cero sí está medido: la L está leída entera.
- **El casabe es `Berrí`, con B.** El pliego 97 dcha. lo escribe con la misma B
  redonda de `Abaiba` dentro del propio renglón.
- **La asimetría `Nuriu` / `Jirru` no era descuido del copista**: el pliego 80
  izq. repite el paradigma entero (Nuriu, Jirru, Irru, Ruriu, Guariu, Jarru,
  Nariu), con glifo simple en 1sg/3f/1pl/3pl y doble en 2sg/3m/2pl.
- **La `-are`/`-re` de Fabo sigue siendo minoritaria** medida ahora sobre el
  vocabulario entero, y la dominante sigue siendo `-si`. La proporción, en
  `meta.censo_de_terminaciones`.

### Lo que salió nuevo

- **El sistema de numerales, entero y medido.** `cage` es 'mano', y el numeral
  se construye encima: `abacage` cinco = «una mano», `Abaibacage` seis,
  `Juchamatabacage` siete, `Juchamage` diez, `Juchamacage Abaí Ribana` quince
  («dos manos y un pie»), `Abacaí tacay` veinte, treinta = «un tacay y dos
  manos encima», `Juchamatacay` cuarenta, `Mataritaí tacaí` sesenta,
  `Juchamacage chana abacagetacaí` mil. Es **base cinco por la mano hasta 20 y
  vigesimal por encima**, con `tacay` = 20. La primera pasada había leído
  `abacase`; la voz es `aba-cage`, con 'mano' dentro.
- **El clasificador de clase no es cosa del numeral: es del sintagma de
  medida.** El mismo juego que toma `aba-` 'uno' lo toman `manu-` 'ancho'
  (35 dcha.) y `aurre-` 'angosto' (36 izq.): -ricu casa, -girra ropa, -ba río,
  -bai hacha, -su palo, -numa puerta.
- **El autor distingue animado de inanimado en el plural**, y lo dice: «el `na`
  es nota de 3.as personas de plural, y las cosas inanimadas no le tienen, como
  consta el Arte» (87 izq.).
- **'Nación' se dice con la raíz de 'habla'**: `Guachuanibérri` 'de mi nación',
  sobre `chuani`; y el plural de «Hombre Racional» es `Guachuanibenay`, «los
  que hablan». Hay además lema para **intérprete** (`Eberrí chuanisí`, 70).
- **Un solo verbo cubre «ser», «estar» y «tener»**: `Vyuna / Vyugi / Vyumí /
  Vyubí / Vyuy / Vyuna` (26 izq.).
- **El español y el duende comparten nombre**, y lo dice el jesuita: «Blanco
  Español — Guabaymí, Guabaymigeraí. Así llaman los Duendes» (42 izq.).
- **El autor marca los préstamos**: bajo «Morena cosa» anota que `Samoruna` es
  «hisp[anice] term[inus] hurtado» (76 dcha.).
- Léxico que la pregunta 4 pedía y no tenía: **la sal** con lema propio
  (`Ybidūma`, 90) y **la salina** (`Ybidūma sucu`), más `bai` 'sal' de
  «Sin sal — Mabayisa»; la **yuca** mansa y brava con sus dos yucales
  (`Quenirro` / `Alirrí`, 71); el **sebucán** (`Erricaí`, 93); la **quiripa**,
  que el autor dice que hacen los Otomacos (34, 54, 90); once **árboles** con
  nombre propio bajo un solo lema (37 dcha.); seis **culebras** (51 dcha.);
  cuatro insectos picadores (76 dcha.); el **temblador** (93 dcha.).
- **Topónimos**: el río Meta es `Meda` (75 dcha.), y hay `Casanare Numana`
  'boca de Casanare' (42) y `Guaviare ge sana` 'los del Guaviare' (26 dcha.).
- **Parentesco por línea**: el achagua no tiene una sola voz de 'pariente',
  sino formas distintas según por dónde se es pariente — por hermanas
  (`Nugisa`), por la mujer (`Nerrimasí`) y una tercera cuya abreviatura
  castellana no se deja leer, anotada en `dudas` (80 dcha.). Y la hermana de un
  varón (`Richerro`) no se dice como la hermana de una mujer (`Ruerraí`).

### Qué sigue sin hacerse

- El **arte** propiamente dicho (pliegos 7-22: declinaciones, las seis
  conjugaciones, los tratados) sigue sin minar. De él solo hay pronombres,
  numerales, los posesivos adjetivos y el sufijo `-mi` de «cosa ya pasada».
- Nada se llevó al lexicón ni al corpus, y no se abrió ningún issue. Sigue
  siendo comparanda achagua, y la decisión es de D11 (#39).

## Cruce achagua ↔ caquetío (2026-09-13)

**Escriba (agente Opus 5), por #121.** Script reproducible:
`6-fusion/scripts/cruzar_achagua_caquetio.py`. Datos, veredicto por concepto y
todas las cifras: `6-fusion/cruce_achagua_caquetio_2026-09-13.yaml` —
propuesta, no canon (regla 5). Como en el resto de esta nota, ninguna cifra se
repite aquí: el reparto vive en `meta.resumen_atestiguado`, el azar en
`…por_lengua.*.azar` y la prueba de predicción en `meta.prueba_de_prediccion`.

### Qué se preguntó

¿Qué voces caquetías tienen cognado plausible en achagua, y el caquetío
**atestiguado** se parece más al achagua, al lokono o al wayuu? Con las tres
reglas del método de `cruzar_achagua_jahn.py` puestas en código:

- **Por concepto, nunca por forma suelta.** Solo cuenta la glosa exacta (una
  sola palabra en los dos lados, con la ortografía de 1762 normalizada). Lo que
  sigue a «v.g.» es ejemplo; «Cachama, un pescado» es una clase, no el concepto.
- **La capa antes que el parecido.** Una forma reconstruida o hipotética
  parecida a la lengua de la que sus `notas` dicen que salió es `circular`.
  La filiación se mide solo sobre la capa atestiguada.
- **Contra la propia regla, dos controles.** Un modelo nulo por permutación
  —el achagua ofrece más lemas por concepto que el lokono o el wayuu, y sin
  control eso lo favorecería— y una prueba de predicción de las
  correspondencias sobre conceptos que no se usaron para verlas.

Pronombres y numerales, fuera: los lleva otro escriba.

### Qué salió

- **Lo que manda es el hueco.** La capa atestiguada es sobre todo fitonimia y
  zoonimia de Paraguaná y Coro (Zavala), y un vocabulario de los Llanos rara vez
  la nombra con la misma glosa. Los conceptos con glosa exacta en las tres
  comparandas a la vez son un puñado. Cualquier reparto sobre esa base es frágil,
  y el YAML lo da con su esperado por azar al lado.
- **Las tres lenguas dan algo más de parecido que el azar, y ninguna se
  despega.** El achagua reúne más pares en bruto porque tiene más conceptos
  comparables, no porque se parezca más: por tasa y por similitud media sobre el
  azar, el lokono da la señal más limpia y el wayuu no queda lejos. Con estos
  recuentos no se puede decir que el caquetío atestiguado esté más cerca del
  achagua.
- **Candidatos con el achagua** (capa atestiguada): `kiba` 'piedra' ~ `Jba`
  (83 dcha.), el único que se parece a la vez al achagua y al lokono (`siba`),
  con la advertencia de que tres fonemas dan un parecido barato; `aka` 'bejuco'
  ~ `Acua` («Sarmiento, bejuco», 90 dcha.), también de tres fonemas; `bakoa`
  'bosque' ~ `Abaca` (43 izq.); `tarika` 'laguna' ~ `Carisa` (71 dcha.), débil;
  y `arata` 'mono' ~ `Rrabata` «Mona» (76 izq.), que **no es hallazgo a
  ciegas**: salió al añadir el sinónimo mona → mono después de auditar los
  ceros, y el YAML lo declara en `parametros.sinonimos_añadidos_tras_auditar_ceros`.
- **Con el lokono** se reencuentran pares ya conocidos (las propias `notas`
  caquetías los citan): `kati` 'luna' ~ `kathi` (A-2) y `para` 'mar' ~ `bara`
  (Schultz vía Perea). `iero` 'mujer' se parece a la vez al lokono `hiaro`
  (Pet) y al wayuu `jierü`.
- **Con el wayuu**: `saruro` 'boa' ~ `sarulu`. Toca la etiqueta de `saruro`,
  cuya nota dice que si resultara voz del área bajaría a retroabstraído: un
  parecido con el guajiro no lo prueba, pero es la pregunta que hay que hacerle.
  `dara` 'alcaraván' ~ `kaarai` es débil, y la glosa wayuu trae «(dara)» entre
  paréntesis, probablemente el regionalismo.
- **Circulares, y no cuentan**: `mütsia`, `anasa`, `yama` y `wana` se parecen al
  wayuu del que se sacaron; `kali`, `sipara` y `kaiwa`, al lokono; `bari`, al
  achagua, porque su nota la deriva del proto-arahuaco. La lista con sus
  similitudes, en `meta.circulares`.
- **Sesgo inverso, encontrado de paso.** Varias entradas **lokono** del lexicón
  sin fuente se escribieron «como cognado de» la voz caquetía (`katsi`
  «cognado de cati caquetío», y también `hadalli`, `baraha`, `hamaha`, `koïa`,
  `piaye`). Compararlas mide la mano que las escribió, no la lengua: se
  excluyeron del cruce y quedan en `meta.comparanda_excluida_por_sesgo_inverso`.
  El lexicón no se tocó.
- **La prueba de predicción no sostiene ninguna correspondencia.** Con tan pocos
  pares, ninguna regla junta dos apoyos en un mismo pliegue. Dejando fuera los
  conceptos que la sugirieron, todas las correspondencias vistas fallan, no
  superan al azar o no tienen casos: `caq #k ~ ach ∅` (de `kiba ~ iba`),
  `caq k ~ lok s` (de `kiba ~ siba`), `caq p ~ lok b` (de `para ~ bara`),
  `caq r ~ way l` (de `saruro ~ sarulu`). Es la hipótesis `k-` cayéndose otra
  vez, ahora contra el azar.
- **La trampa de Jahn, controlada**: con glosa exacta, agua = `Vni` y mar =
  `Manoa`, y ninguna entrada de Neira tiene `mena` (`meta.control_trampa_jahn`).
- La sensibilidad a `gu_es_w` no cambia el cuadro (`meta.sensibilidad_gu_es_w_true`).

### Qué NO

- **No se decide filiación.** Lo que el cruce permite decir es: «las tres
  comparandas dan algo por encima del azar, ninguna domina, y la base comparable
  es mínima». Nada de esto apoya todavía re-derivar el núcleo desde el achagua.
- **Ningún par es cognado verificado.** Son candidatos con glosa exacta y forma
  parecida, sin correspondencias regulares que los sostengan. Las formas achagua
  son transcripción por visión: verificar el pliego en imagen antes de citar.
- **Glosa exacta no es significado idéntico.** Quedan fuera del alcance del
  filtro la aposición sin artículo («Pajaro, Dios te de») y alguna homonimia; se
  auditaron a mano los emparejamientos de lema con varios segmentos, y ninguno
  de los parecidos contados sale de ahí.
- No se tocó `curiana_lexicon.py`, ningún `lexicon_*.py` ni `3-mundo/corpus/`,
  y no se abrió issue. Pronombres, numerales y el arte más allá de
  `arte.verbos` quedan fuera. El paraujano va como columna informativa, no en el
  reparto (ahí salta `kasi` 'sol' ~ `kai`).
- **Queda para quien fusione**: limpiar las entradas lokono con sesgo inverso;
  preguntarle a `saruro` si es voz del área; y verificar en imagen `Jba`,
  `Acua`, `Abaca`, `Carisa` y `Rrabata` antes de citar ninguno.

## Consulta puntual: `macana` (2026-09-21)

**Agente de campaña (Claude), por el encargo de `d21.8`.** Lectura en imagen de
cuatro páginas, no minería. Todo el detalle, con las citas literales y el
veredicto, en `6-fusion/propuesta_macana_etiqueta_2026-09-21.yaml`; las
opciones para Miguel, en
`6-fusion/issues-pendientes/macana-etiqueta-2026-09-21.md`. Propuesta, no canon
(regla 5).

### Qué se le preguntó al Arte

Si `Macanasi`, `Macanayi` y `Mamacanayisa` —vistas de paso al comprobar el
plural `-kana`— son apoyo arahuaco **independiente** para la entrada `macana`
del lexicón, hoy `caquetío-reconstruido`. Y, si lo fueran, si esa
independencia del castellano se podría sostener, siendo `macana` voz del
castellano de Indias desde hacía 250 años en 1762.

### Qué contestó

**Que no, y por una razón más fuerte de la esperada.** Las tres formas existen
con la grafía citada —verificadas en imagen a resolución nativa, factor medido
4,1667 px/pt, con la clave de la `r` con glifo de `z`— pero **ninguna significa
'macana'**:

| Forma | Pliego | Entrada literal | Glosa literal |
|---|---|---|---|
| `Macanasi` | 56 der. | `Dormidera — Macanasi` | Dormidera |
| `Macanayi` | 74 der. | `Mazorca de mais — Macanayi` | Mazorca de maíz |
| `Mamacanayisa` | 70 izq. | `Yndecible — Mamacanayisa` | Yndecible |

Y ninguna está suelta: `Macanasi` cierra ocho lemas DORMIR- seguidos (con
`Dormitorio — Macarrusi` justo encima); `Macanayi` va entre `Mazo — tataubari`
y `Matalotage — Marruen`; `Mamacanayisa` es la de en medio de
`Yndisoluble — Mabasaidacanayisa` · `Yndecible — Mamacanayisa` ·
`Yndivisible — Maisidacanayisa`.

**La morfología la declara la propia obra**, y eso desarma la lectura
«raíz `macana-`»: el arte trae, en la lista alfabética de partículas y verbos
(**26 izq.**), una entrada cuyo lema castellano es literalmente
**«Verbal en "bilis"»**, forma `-nayisa`, con los ejemplos
`Macabacanayisa = invisible`, `Manoacamanimisa = los bautizados`,
`Mebedacanisa = los q[u]e no creen`, y la nota del autor «también es nota de
participio de presente, y de pretérito estas partículas: `-yisa`, `-misa`,
`-nisa`». Con el privativo `ma-` —que el Arte usa él mismo en
`Sin sal — Mabayisa` (sobre `bai`) y `Sin Padre — Masaricanayisa` (sobre
`Saricanasi`)— `Ma-ma-canayisa` es un adjetivo en -ble negado, y la cadena
«macana» cae a caballo de tres morfemas. El vocabulario da **once paralelos**
de la misma plantilla (`Yncreible — Mabedacanayisa`,
`Ynfinito — Masutedacanayisa`, `Ymplacable — Mananedacanayisa`…, y el positivo
`Maravilloso — Cadedacanayisa`). Ninguno es un arma.

**Y el Arte contesta además la pregunta contraria, que es la que decidía.**
Tiene lema `Macana`, en el **pliego 73 der.**, bajo la cabecera «Castellano. —
M. — Achagua.»:

> `Macana. — — — — Guacaba. / La mia = Nucaba[ba]mi.`
> `Macana de enlatar. — — — Juba.`

Como el vocabulario va **castellano → achagua**, `macana` está del lado
**castellano**: es la palabra con la que pregunta el misionero, y el achagua
contesta con `Guacaba`, no cognada. No es un caso suelto — el jesuita usa
sistemáticamente tainismos panhispánicos como cabecera castellana, con voz
achagua propia enfrente: `Casabe — Berrí` (46 der.), `Hamaca — Edasi`
(67 izq.), `Mais — Cana` (73 der.), `Manati — Apia` (74 izq.), `Canoa — ida`.
Seis de seis. Y **sabe marcar un hispanismo** cuando lo ve (`Morena cosa —
Samoruna`, «hisp[anice] term[inus] hurtado», 76 der.): aquí no marcó nada
porque no había nada que marcar.

**Veredicto:** la obra no corrobora `macana`; documenta que una lengua arahuaca
del norte, pariente cercana del caquetío, tenía su **propia palabra no
cognada** para el objeto. Es `minar-fuente` §8 en su forma exacta — *una
corroboración falsa es peor que ninguna*—, y de la misma familia que la trampa
de Jahn con `datihao` que esta misma nota ya registra.

Dudas de lectura anotadas: en el ejemplo de `Macana`, el copista escribe
`Nucabami` con un `ba` volado, marca de inserción — `Nucababami` o
`Nucabamiba` (la transcripción del 09-12 puso lo segundo). No decide nada.

### Qué daría esta obra si se minara (sin minarla: es otra campaña)

Lo primero, un aviso de planificación que esta consulta dejó claro: **el
vocabulario de esta copia va sólo castellano → achagua, alfabético por el
castellano** (pliegos 28-98, dos columnas, la parte achagua → castellano no
está en esta copia). Eso significa que **se le puede preguntar por concepto,
pero no por forma**: cualquier pregunta del tipo «¿existe la forma X en
achagua?» obliga a leerlo entero. Las cifras de entradas, pliegos y letras
están medidas en `meta.cobertura` de
`6-fusion/achagua_neira_ribero_1762.yaml` y las emite
`6-fusion/scripts/ensamblar_achagua_neira_ribero.py` (regla 1: no se repiten
aquí).

Lo que sigue sin minar y pagaría, por orden de rendimiento:

1. **El arte propiamente dicho, pliegos 7-22** — declinaciones, las seis
   conjugaciones, los tratados. Es lo único grande que queda, y es lo que más
   falta hace: la morfología derivativa que esta consulta necesitó (`-si`
   absoluto del no-poseído, `-yi`/`-cayi` adjetival, privativo `ma-`, el
   «verbal en bilis» `-(da)canayisa`) hubo que reunirla de **una** entrada del
   arte y de una serie del vocabulario. Minado, convertiría la comparanda
   achagua del repo de lista de palabras en morfología — que es exactamente lo
   que D11 (#39) necesita para dejar de apoyarse en el wayuu.
2. **Censo de los lemas CASTELLANOS que son tainismos o americanismos
   panhispánicos**, con la voz achagua enfrente. Esta consulta encontró seis a
   mano y los seis dan voz achagua no cognada. Hecho entero, el repo tendría
   una respuesta **medida** a la pregunta que vuelve cada vez que se propone un
   tainismo como caquetío: *¿cómo trata un vocabulario misionero del XVIII las
   voces antillanas?* Es acotado y de alto valor de control.
3. **Censo de los préstamos que el autor marca él mismo** (del tipo
   `Samoruna`, «hisp. term. hurtado»). Da la medida de cuánto castellano
   reconocía el propio jesuita, y calibra el punto 2.
4. **Campos semánticos que el vocabulario tiene y el repo no ha sacado**: la
   serie derivativa `ma-…-(da)canayisa` entera como paradigma; el sistema de
   clasificadores de clase, que el vocabulario muestra en tres bases distintas
   (`aba-` 'uno', `manu-` 'ancho', `aurre-` 'angosto') y que el arte debería
   explicar; y el paradigma posesivo, que asoma en media docena de lemas.

⚠️ `sostiene` no se toca a mano (lo mide `medir_sostiene.py`), y esta consulta
no llevó nada al lexicón ni al corpus: sigue siendo comparanda achagua y la
decisión es de D11 (#39) y de Miguel.

## El arte, pp. 1-32 (2026-09-22/23)

**Agente de la tercera campaña de minería (parcela M4), por D11.** Lectura por
visión de los pliegos 7 der.-23 izq. Datos, página por página y con la
comparación contra `2-lengua/morfologia.md`:
`6-fusion/achagua_arte_neira_ribero_2026-09-22.yaml`; cifras:
`6-fusion/medicion_arte_achagua_2026-09-22.yaml` (script
`6-fusion/scripts/medir_arte_achagua.py`); opciones para Miguel:
`6-fusion/issues-pendientes/achagua-arte-morfologia-2026-09-22.md`. Propuesta,
no canon (regla 5); comparanda de los Llanos (regla 4).

### Cómo se lee el arte

- **Tiene paginación propia** (esquina superior): pliego N izq. = p. 2(N-7),
  der. = p. 2(N-7)+1; comprobado en 7 der. = p. 1, 12 izq. = p. 10, 23 der. = p. 33.
  Se cita «p. X (pliego N lado)».
- **Desde el pliego 10 la página izquierda pasa del lomo**: el recorte por
  mitades corta el final de las líneas. Se recorta con solape (x 3-56 % y
  46-99 %).
- **Clave nueva**: la S larga MAYÚSCULA (ſ) se parece a la J. En las listas de
  sufijos de las pp. 12 y 16 la 2sg sale «Ji» y es «Si»: lo prueban los ejemplos
  en minúscula de la misma página (`Nacabauʃi`). Va también a
  `meta.clave_de_lectura` del YAML nuevo.
- El autor **declara que imita a Nebrija** (p. 1): la rejilla de casos y tiempos
  es suya; lo que la rejilla no pedía y anota igual es lo que más vale.

### Qué se le preguntó, y qué contestó

1. **Personas**: dos juegos, dichos por el autor (p. 12): prefijos `Nu- Ji- Ri-
   Ru- Gua- Y- Na-` para «los demás verbos», sufijos `-na -si -ni -no -bi -y
   -na` para los compuestos de «ser» y, los mismos, para el objeto (p. 16:
   `Nacabauna` «me miran»). 1sg `nu-`, 1pl `gua-`.
2. **Tiempo/aspecto**: paradigma latino (`-nimi-`, `-su`, `-bita`, `-ca`
   infinitivo, `-cata` gerundio) y un testimonio de uso: «el pres.te de
   Indicativo es el q.e hace el gasto» (p. 28). `-ca` y `-ni` existen con otro
   valor que en el proyecto.
3. **Posesión**: el no-poseído es un sufijo `-si` que cae al poseer; cuatro
   clases de nombre y una quinta con adjetivo posesivo (p. 32-33).
4. **`ca-`/`ma-`**: par mínimo `masacorreyisa`/`casacorreyisa` (p. 18-19), y el
   nombre predicado conjugado (`Cabarruani vyuna` «estoi rico», p. 25;
   `Cagicunacana` «yo pecador», p. 27). El «hay» impersonal no es `ca-`.
5. **Nominalización**: `-erri` agente, `-nicay` paciente, `-can(s)i`/`-si`
   acción y abstracto (pp. 4-6, 11, 13).
6. **Plural**: lo inanimado y lo irracional no llevan plural (p. 6).
7. **Numerales**: el arte no tiene capítulo (cero verificado en las 32 páginas).

### De paso

- **«León» está en el arte** (`Nerrianarre`, p. 19): cierra la única `no-esta`
  de la calibración de Jahn (`mirrianare`). El YAML del vocabulario no se tocó:
  queda para quien fusione.
- El locativo distingue líquido (`yaco`) de no líquido (`naco`) (pp. 29-30), y
  hay una segunda nota dialectal del autor: «el au lo hacen en Casanare ao» (p. 21).

### Qué NO

- Ningún dato caquetío: las sondas sobre la capa atestiguada dan cero para
  `ka-`/`ma-` con glosa atributiva y para las formas de los nominalizadores
  achagua (medición citada arriba).
- No hay segunda lectura independiente del arte: un lector, con zoom sobre cada
  línea citada. Las dudas de lectura, en `dudas` del YAML.
- No se tocó `lexicon_achagua.py`, su YAML, `curiana_lexicon.py`, `2-lengua/` ni
  el corpus.

**✅ Aplicado al canon el 2026-09-24** (tanda de las hermanas, `6-fusion/decisiones_tanda_hermanas_2026-09-24.yaml`): `uni` 'agua' (pliego 32 izq.) y `unia` 'lluvia' (pliego 73 der.) son reconstruidas con el lokono; `saika` 'bueno' (pliegos 43-44) es hipotética; `maa` 'decir' se queda con «Numau» (pliego 55 der.). Las claves achagua `uni` y `unia` pasaron a `-achagua`.

## Enlaces

[[fabo-1911]] · [[jahn-1927]] · [[rivero-1883]]
