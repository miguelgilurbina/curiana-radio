---
tipo: fuente
obra: "De Indianen Caraïben van het eiland Aruba (West-Indië)"
autor: "Koolwijk, A. J. van"
anio: 1882
publicacion: "Artículo con una lámina de figuras. La copia es de la Biblioteca Nacional Aruba (Departamento Arubiana-Caribiana)"
genero: etnografia
local: "fuentes_caquetios/vanKoolwijk_1882_Indianen_Caraiben_Aruba.pdf"
paginas: 17
capa_texto: si
acceso: "Libre, CC BY 4.0 — Internet Archive (BNADIGKOSTBARE0151)"
descargado: 2026-10-05
origen_digital: "https://archive.org/download/BNADIGKOSTBARE0151/BNA-DIG-KOSTBARE-0151.pdf"
estado_minado: minado
cobertura: "2026-10-05, minería entera por encargo de Miguel («de una»): las 8 páginas del artículo (pp. 222-229, pdf 4-11) y las dos mitades de la lámina (pdf 12-13) leídas en IMAGEN, a resolución nativa en las listas; vocabulario arubano, kari'ña de Surinam, topónimos, independencia frente a Gatschet y van Buurt, lámina y mundo por esferas. Las cifras, en 6-fusion/van_koolwijk_1882_aruba_2026-10-05.yaml (meta.cobertura.conteos)"
verificado: 2026-10-05
minado: 2026-10-05
minador: "6-fusion/scripts/minar_van_koolwijk_1882.py"
propuesta: "6-fusion/van_koolwijk_1882_aruba_2026-10-05.yaml"
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
aliases: ["van Koolwijk 1882", "Koolwijk 1882"]
---

# Van Koolwijk 1882 — Los indios de Aruba

## Qué es

El artículo del párroco van Koolwijk sobre los indígenas de Aruba, en el
*Tijdschrift van het Aardrijkskundig Genootschap* VI, pp. 222-229, con una
lámina fuera de texto (n.º 7). Llegó a Aruba el 20 de noviembre de 1880 (p.
222) y firmó el artículo allí el 20 de noviembre de 1881 (p. 227). Es el mismo
misionero que en 1885 contó «inscripciones indígenas en 27 lugares de Aruba»,
según cita Wagenaar Hummelinck. El rastreo de arte rupestre (sesión 07,
2026-08-14) lo localizó catalogado como «petroglyphs, rock paintings».

**Licencia CC BY 4.0**, la más abierta del lote: se puede reproducir citando
la fuente.

**Si trata de lo que se creía: a medias.** Se esperaba una lista de palabras
arubanas larga y una lámina de petroglifos. La lámina es de cerámica, y la
lista larga es kari'ña de Surinam. Lo arubano es más corto y está todo en la
p. 227.

## Cómo se lee

Neerlandés de 1882. **pdf + 218 = página impresa** (pdf 4 = p. 222 … pdf 11 =
p. 229; lo confirma la bibliografía de Wagenaar Hummelinck 1953, «p.
222-229, tab. excl.»). Las pp. 1-3 y 14-17 del PDF son tapas, guardas y la
hoja de licencia.

**La capa de texto no sirve para citar.** Es parcial (pdf 4 y 11 casi no
tienen texto) y en la p. 228 corre las columnas: así salió `kwai` 'pijl',
cuando en la imagen «een pijl» es `prīwa` y `kwāi` es 'kalebas'. Todo lo que
se cita se leyó en imagen con pymupdf: el escaneo trae imágenes de 2576 px
sobre 309 pt (8,35 px/pt), y las listas se recortaron a ese factor.

Las listas llevan macrón y breve. El macrón cae a menudo sobre el dígrafo
`oe` (= /u/), y la propuesta lo escribe `ōe`. Gatschet transcribe las mismas
voces con la ortografía inglesa (`oe` → `u`, `j` → `y`, `ch` → `sh`).

## Qué ha dado

Todo en `6-fusion/van_koolwijk_1882_aruba_2026-10-05.yaml`, con página, forma,
glosa neerlandesa y castellana, cruce con el repo, etiqueta y propuesta. Las
decisiones, en `6-fusion/issues-pendientes/van-koolwijk-1882-2026-10-05.md`.

- **Vocabulario arubano** (p. 227, y la nota 1 de la p. 224): voces y frases,
  cinco plantas sin glosa individual, dos animales y un conjuro para cazar la
  iguana. Sólo `carēbe` 'cuchara' **confirma** una voz atestiguada (`karebe`).
  El resto queda fuera del lexicón: o es nueva y sin cognado (`mimānta`
  'estoy asustado', `bouserānja` 'enseres', `kajappa` 'cuadrilla de siembra',
  `aboūssoe` 'torta de maíz', `auw` 'bien'), o es criolla (`pekinini`), o es
  de la esfera (`marākka`), o es la misma voz que Gatschet ya traía.
- **Corrige a Gatschet**, porque es el original impreso: `caula` y no
  `kanla`, `Cautje` y no `kantie`, `hida meeuw` y no `tida meo`, `hafe dōbo
  danwajēte` (Gatschet lo daba por irreconstruible), `wōu` y no `uou/uqu`,
  `Tarabada` como planta propia, y en los topónimos `Cassiwāri`, `Boebāri` y
  `Boekoerōi` donde el OCR de Gatschet leía Kasiaari, Cubari y Cukuroi. Y un
  **conflicto de glosa**: `bāroe hāntoe wōu` es 'oración después de comer'
  aquí y 'pedir de comer' en Gatschet.
- **Topónimos** (p. 227): tres listas, de lugares, de cerros y de grutas. Los
  tres nombres en **-bana** (Chirabāna, Tarabana, Wakoebāna) están todos en la
  lista de **cerros**, que es lo que D9 dice de `-bana`. **Kibāima** cierra como
  `kiba` 'piedra' + `-aima` 'abundancia', también un cerro (hipótesis del
  proyecto: la fuente no glosa). Da la forma más antigua de **Casibari**,
  **Arashi** y **Matividiri**, tres entradas del canon sin procedencia, y
  Matividiri tiene su par en el **Matividiro** de Paraguaná, cerro también. En
  la prosa: «Parawana» nombra la península y, a la vez, un lugar del norte de
  Aruba con una inscripción.
- **Independencia** (regla 8 de minar-fuente): van Koolwijk **no es una
  segunda atestación independiente: es la fuente primaria de la cadena** van
  Koolwijk 1881 → Pinart 1882 / Gatschet 1885 → (Hartog 1953) → van Buurt 2014.
  Firmó antes de que Pinart llegara, las listas de Gatschet son un
  subconjunto de las suyas, la anécdota del entierro y el conjuro son los
  mismos, y tres confusiones n/u delatan copia de un escrito. Van Buurt lo lee
  a través de Hartog. Consecuencia: la «TRIPLE atestación independiente» de
  `dabaraida` en `lexicon_gatschet.py` no lo es.
- **La lámina**: las 21 figuras son cerámica, según el propio texto (pp.
  223-224): cenefas pintadas en tiestos, ranas en relieve, asas, un pico, una
  vasija y la urna. Ninguna es un petroglifo. El catálogo
  `6-fusion/petroglifos_imagenes_2026-10-05.yaml` ya lo dice, figura por
  figura, junto con los sitios con inscripciones que el texto describe.
- **El kari'ña de Surinam** (pp. 227-229): la lista entera, más el
  Padrenuestro y los diez mandamientos. Es comparanda caribe fuera de la
  esfera y no entra al lexicón. Las coincidencias de forma y glosa que tiene
  con el lexicón (`tōna` ~ taíno *tuna*, `casīri`, `piaīman`, `nānā`) son
  voces areales; están leídas una a una.
- **Mundo**, por esferas (todo de 1881, como mucho `retro-abstraido`): la
  intervisibilidad Aruba–Paraguaná dicha por un testigo; la siembra con
  palo-gancho al pie de los cerros, donde se junta el agua; los alimentos de
  seca (mariscos, semillas de totumo, agave, *bringa mosa*); la manta de las
  mujeres; el entierro en urna, en cuclillas y con la cabeza fuera, hasta
  comienzos del s. XIX; la rana que sólo vive en Aruba y es el motivo de las
  vasijas; las canteras de pigmento; la tradición de que una figura bajo los
  bloques marca al dueño del sitio; la memoria de la matanza de Carachito.

## Qué NO se encontró

- **Glosas de topónimos.** El autor sólo da las listas: ningún nombre de
  lugar lleva traducción.
- **Ningún petroglifo dibujado.** Las inscripciones se describen y no se
  dibujan. Las primeras figuras publicadas de inscripciones arubanas son de
  Martin 1885 (Fontein y Canashito), según Wagenaar Hummelinck 1953.
- **Ninguna segunda atestación independiente.** Todo lo que este artículo
  comparte con Gatschet es la misma cadena.
- **Zayas 1931 no lo cita** (0 menciones en los dos tomos), y **Hartog** no
  está en el repo: sólo llega por van Buurt.
- Las valoraciones morales sobre la población (p. 222), el origen griego o
  atlántico de los arubanos y el significado que el autor da a los colores
  son especulación de 1882: se registran y no se proponen como dato.

## Qué falta

- **Decisiones de Miguel**: el issue
  `6-fusion/issues-pendientes/van-koolwijk-1882-2026-10-05.md`, con seis
  preguntas: el veredicto de independencia y sus consecuencias, las
  correcciones a Gatschet, la procedencia de tres topónimos del canon, la
  entrada de los topónimos arubanos, la lámina y la fusión del mundo.
- **Deuda documental nueva** (descargar lo decide Miguel): van Koolwijk 1881
  (Curazao, TAG 5 pp. 57-68), van Koolwijk 1885 («Indiaansche opschriften te
  Aruba»), Martin 1885 (las primeras figuras de inscripciones arubanas),
  Pinart 1890 y Hartog 1953/1968.
- Si se reabre la campaña de las ABC, este artículo es su punto de partida:
  da la forma de 1881 de cada nombre.

## Enlaces

[[wagenaar-hummelinck-1953]] · [[wagenaar-hummelinck-1962]] · [[gatschet-1885]] · [[van-buurt-2014]]
