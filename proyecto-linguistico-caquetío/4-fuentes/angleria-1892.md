---
tipo: fuente
obra: "Fuentes Históricas sobre Colón y América (Décadas del Nuevo Mundo), vols. 1 y 4"
autor: "Anglería, Pedro Mártir de"
anio: "1892 [c. 1530]"
genero: cronica
local: ["fuentes_caquetios/Angleria_1892_Fuentes_Historicas_Colon_America_vol1.pdf", "fuentes_caquetios/Angleria_1892_Fuentes_Historicas_Colon_America_vol4.pdf"]
paginas: "460 + 492"
capa_texto: si
estado_minado: parcial
prioridad: alta
cobertura: "transmisión del saber, vol. 4 (sesión 4) + la costa y su red de intercambio, vol. 1 (2026-09-21, campaña del taíno T5) + la etnohistoria del contacto en los dos volúmenes (2026-09-22, campaña del taíno 2, T7)"
desfase_pagina: "impresa = pdf − 64 en el vol. 1; impresa = pdf − 8 en el vol. 4 (medido 2026-09-22 sobre los folios que el escaneo conserva)"
sostiene: {hechos_corpus: 1, entradas_lexicon: 0}
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["Anglería 1892", "Pedro Mártir", "Décadas"]
---

# Anglería 1892 [c. 1530] — *Fuentes históricas sobre Colón y América*

## Qué es

Crónica temprana (compuesta hacia 1530). Dos volúmenes en el repo, 952 páginas
en total. Rendimiento **muy desigual**: el vol. 4 dio el mejor dato puntual de
la sesión 4; el vol. 1 no dio nada relevante.

## Estado técnico (verificado 2026-07-29)

| Archivo | Tamaño | Páginas | Capa de texto |
|---|---|---|---|
| vol. 1 | 20.3 MB | 460 | **sí** (26K car. en 30 pp.) |
| vol. 4 | 21.0 MB | 492 | **sí** (18K car. en 30 pp.) |

`pdftotext -enc UTF-8`. Escaneo antiguo: OCR con erratas, pero utilizable.

## Qué ha dado

**Vol. 4, p. 236 — el areíto antillano** descrito como genealogía cantada: al
entrar en la ceremonia, los danzantes *"colmaban de maravillosas alabanzas al
zeme, y referían cantando las hazañas de los antepasados del cacique"*.

Es **la comparanda atestiguada más fuerte** de [[04_transmision_saber]]: la
función exacta que `ofrenda_ancestros_anochecer` ya asigna a Bana-mana en
`curiana_state.py` ("los niños escuchan los nombres que un día tendrán que
repetir ellos"). → `transmision-018`.

**Vol. 1**: nada relevante en las páginas muestreadas (contenido más
naturalista/zoológico).

## 2026-09-21 — el vol. 1 preguntado por la COSTA (campaña del taíno, T5)

**Qué se preguntó.** ¿Conecta Anglería la costa de Curiana con las Antillas?
¿Describe una red de intercambio, y en qué dirección? Era uno de los tres
huecos que esta nota declaraba («quedan sin preguntar religión, Curiana/Coro,
comercio»). Extraído con `pdftotext -enc UTF-8` (421 KB).

**Medido**: `Curiana/Curian` 12 · `perlas` 38 · `Paria` 23 · `Cauchie` 5 ·
`Española` 84 · `margaritas` 3 — y **`lucay` 0 · `Hispaniol` 0 · `Gigante` 0 ·
`caquet` 0 · `caiquet` 0 · `Coriana` 0**.

**Qué se halló: la red es continental y de eje este-oeste.** El relato del viaje
de Niño y Guerra (1499-1500):

> *«Preguntados los curianenses de dónde conseguían aquel oro, indicaban que lo
> traen de cierta región llamada **Cauchieto**, que distaba **hacia el
> Occidente**, por costa derecha, **seis soles**, esto es, camino de seis
> días… También éstos llevaban perlas al cuello, pero se les proporcionaban de
> **Curiana á cambio de oro**.»*

Oro del oeste por perlas de la costa, en tramos de seis días de navegación
costera. Y las provincias que enumera son **todas de tierra firme**: *«Paria,
Curiana, Cuchibacoa, Cahuyeto, Laturnia, Caubana, Urabain, Zaraboroa,
Veragua»*. Ni una isla antillana en la lista, ni una mención de tráfico hacia
el norte.

⚠️ **Qué nombra «Curiana» aquí sigue en disputa** (#33; ver
[[gonzalez-batista-nombre-de-coro]]) y esta minería **no lo resuelve**. Lo que
la cita sostiene es la **forma** de la red, no la identificación del lugar.

> 🔴 **Actualizado el 2026-09-22 (T7).** [[navarrete-1829-viages-menores]]
> pp. 13 n. 4 y 32 n. 3 separa **dos** Curianas con un documento —la
> capitulación real de Hojeda, que delimita «tierra que se llama Curiana»
> entre los Frailes y el Farallón— y sitúa la de este viaje en **la costa de
> Cumaná y el golfo de Cariaco**, declarando que la de Coro (Pedro Simón,
> Ampíes 1517) «**es distinta**». Si eso se acepta, **la red Curiana ↔
> Cauchieto es de la costa ORIENTAL de Venezuela**, a 400-800 km de Coro: la
> forma de la red se sostiene, que sea de la Kaketiana no. Lo decide Miguel;
> ver `6-fusion/taino2_etnohistoria_contacto.yaml` §hallazgo_lateral.

**Qué NO da**: nada de los lucayos, nada de las islas de los Gigantes, ni una
mención de los caquetíos por su nombre. Es el negativo que la parcela T5
necesitaba: el único relato de primera mano de esa costa antes de que los
españoles la reorganizaran no conoce ninguna ruta hacia las Antillas Mayores.
Ver `6-fusion/taino_en_la_esfera_2026-09-21.yaml` §inventario.

## 2026-09-22 — los dos volúmenes preguntados por la LENGUA y el GUANÍN (campaña del taíno 2, T7)

**Qué se preguntó.** Las cinco preguntas de la parcela T7: el guanín, lo que
los isleños decían del sur, lo que la costa decía del norte, la lengua y los
intérpretes, y la ruta. Datos y citas en
`6-fusion/taino2_etnohistoria_contacto.yaml`; lo mide
`6-fusion/scripts/medir_taino2_etnohistoria.py`.

**⚠️ El desfase de página, medido de una vez** y anotado ya en el frontmatter:
**vol. 1: impresa = pdf − 64; vol. 4: impresa = pdf − 8.** Nadie lo había
escrito, y se recalculaba en cada sesión.

### 🔴 El negativo que esta obra sostiene: el intérprete no cruza a Tierra Firme

`intérprete` en el vol. 1: **11 aciertos, en las pp. 39, 111, 126, 141, 143,
144, 182, 188, 198, 200 y 208 — todas en los libros de La Española y Cuba**. En
los libros VII-IX, que narran el tercer viaje (Paria), el de Niño y Guerra
(Curiana) y el de Pinzón: **cero**. Control en el mismo texto: `lengua` 17,
`entend` 26, `por señas` 8 — y tres de esas «por señas» caen justamente en
Paria (pp. 268-269) y en Curiana (p. 306).

No es que el género no registre estas cosas: Anglería **nombra** al intérprete
y califica su competencia cuando la hay —«sirviendo de intérprete Diego, *cuyo
idioma era casi semejante al de éstos*» (p. 182, Cuba); «por medio del
intérprete Diego Colón, *que entendía aquel idioma*» (p. 198)— y registra el
fracaso cuando falta: en La Navidad, el hermano de Guacanagarí «habló en su
lengua… pero, *como no había intérpretes, no entendieron lo que decía*»
(p. 144).

### Qué más dio, vol. 1

- **p. 268** — «acuden presurosos á los nuestros… de los cuales **coligieron
  por señas** que aquella tierra se llamaba Paria». El topónimo mejor
  establecido del tercer viaje se obtuvo por gestos.
- **pp. 272-273** — «Preguntados dónde se criaba el oro aquel que llevaban,
  **señalaron con el dedo que en ciertos montes de enfrente**… aunque **no
  pudieron entender bien** si lo decían por caníbales ó por fieras silvestres.
  **Les molestaba mucho el no poder entender á los nuestros ni ser ellos
  entendidos.**» ⚠️ Es paráfrasis de la *Relación del tercer viaje*, hoy en el
  repo ([[navarrete-1859-viages-colon]] p. 400): **el mismo testigo, no un
  segundo** (skill §8).
- **p. 304** — en Curiana, Niño «**con gestos y señas** les dio á entender que
  se le acercaran con sus canoas».
- **pp. 308-309** — «Tienen orzas, cántaros, ollas y demás utensilios… **compradas
  de otra parte**. Pues celebran sus ferias entre sí… **pero de cerca**» y
  «animales primorosamente formados de oro, **aunque no puro**, pero **se les
  llevan de otras partes á cambio**». El objeto de oro aleado está en Curiana y
  viene de fuera; el mercado local se declara de corto radio.
- **p. 315** — «**En la Curiana encontraron la cabeza de un caníbal clavada en
  la puerta de cierto principal**, cual bandera ó yelmo tomado al enemigo».
- **p. 316** — Haraia, la sal: «formando con ella como ladrillos, **la venden á
  los extraños á cambio de cosas ajenas**».
- **`guanín` no aparece ni una vez en las 460 páginas del vol. 1.** La voz no
  llega a Anglería por el tercer viaje ni por Curiana.

### Qué dio el vol. 4

- **p. 331** (Década VIII, por los dominicos de Chiribichi) — «Afirman que los
  habitantes de estas regiones son caribes ó caníbales… Se sabe que **salen á
  caza de hombres en flotas de barquillas de un solo madero, recorriendo
  innumerables islas**… **Carib, en todas las lenguas de aquellos países, es lo
  mismo que más fuerte que los demás**… Se llaman también caribes **de la
  región caribana, situada en la parte oriental de Urabá**». Tres datos: la voz
  es areal, el radio es de islas, y `Caribana` está en el Darién.
- **pp. 335-336 y 364** — las dos únicas apariciones de `guanín` en toda la
  obra, y las dos en **Tierra Firme oriental**: «Llevan grano de maíz,
  esclavos, oro ó alhajas de oro, **que ellos llaman guanines**» (la feria de
  Chiribichi) y «otros se cuelgan al pecho planchas de oro **que llaman
  guanines**». ⚠️ Anglería nunca estuvo allí: lo oyó de frailes que pasaron por
  La Española — es el vector 1 de Oliver (la voz taína llevada por el español)
  con otra cara. Y es **colonial**, no precontacto.
- **p. 133** — «se encontraron á los caníbales con **una armada de canoas** que
  habían navegado en ordenada formación, **muchas millas desde sus confines á
  caza de hombres**. Las canoas… á veces son **capaces de 80 remos**».
- **pp. 74-75** — el carpintero yucayo que vació un tronco, lo cargó de maíz y
  calabazas de agua y llevaba **doscientas millas** de mar cuando una nave lo
  interceptó. No prueba ninguna ruta precolombina; acota por abajo lo posible.

### ⚠️ Dos trampas de ortografía medidas aquí

1. **`gigante` en el vol. 4 NO es la Isla de los Gigantes.** Los 9 aciertos son
   el **rey gigante Datha de Duhare**, de la expedición de Ayllón a Chicora
   (las Carolinas). Curazao como «isla de los Gigantes» está en
   [[navarrete-1829-viages-menores]], no aquí.
2. **El vol. 4 escribe `yucayo` (11) tanto como `lucayo` (10).** Un barrido con
   una sola grafía se pierde la mitad (regla 6).

## Qué falta

- **Barrido dirigido a los caquetíos**: queda sin preguntar la religión. La
  transmisión se barrió en la sesión 4, la **costa/comercio** el 2026-09-21 y
  la **lengua y el contacto** el 2026-09-22 (arriba).
- **Los volúmenes 2 y 3.** Con el vol. 1 y el vol. 4 ya medidos en tres
  preguntas distintas, el argumento de «medir primero lo que hay» está agotado:
  el rendimiento del vol. 1 pasó de «nada relevante» a nueve citas en cuanto se
  le hizo otra pregunta.
- Es una de las crónicas que [[PLAN_MAESTRO]] §1.1 marca como "apenas tocadas",
  junto a [[las-casas-1875]] y [[oviedo-y-valdes-1851]].
- El areíto sale de Anglería para las **Antillas**, no para Coro: se usa como
  comparanda estructural, no como dato caquetío.

## Enlaces

[[04_transmision_saber]] · [[las-casas-1875]] · [[colon-hernando-1892]] ·
[[navarrete-1859-viages-colon]] · [[navarrete-1829-viages-menores]]
