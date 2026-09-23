---
tipo: fuente
obra: "Lexicografía antillana. Diccionario de voces usadas por los aborígenes de las Antillas Mayores y de algunas de las menores y consideraciones acerca de su significado y de su formación"
autor: "Zayas y Alfonso, Alfredo"
anio: 1931
publicacion: "2ª ed., La Habana, Tipos-Molina y Cía., 1931, 2 tomos (1ª ed.: La Habana, El Siglo XX, 1914, un tomo)"
edicion_del_ejemplar: "la 2ª ed. de 1931, ejemplar digitalizado por la University of Florida para la Digital Library of the Caribbean (dLOC, AA00089831, vols. 00001 y 00002). NO es la de 1914 que cita Goeje: la paginación no coincide"
genero: vocabulario
local:
  - "fuentes_caquetios/Zayas_1931_Lexicografia_Antillana_2ed_t1.txt"
  - "fuentes_caquetios/Zayas_1931_Lexicografia_Antillana_2ed_t2.txt"
paginas: "t. I: 284 pp. de PDF; t. II: el resto del diccionario (ver el .txt, un salto de página por hoja)"
capa_texto: si
descargado: 2026-09-22
origen_digital: "dLOC / UFDC — https://dloc.com/AA00089831/00001 y /00002; los PDF se sirven en https://ufdcimages.uflib.ufl.edu/AA/00/08/98/31/00001/AA00089831_00001.pdf y .../00002/AA00089831_00002.pdf"
acceso: >-
  🟡 Los PDF pesan 381.832.748 y 441.578.577 bytes (sha256
  5b194ccf342cd0ce557aa02ac13f969b3bbea9e25756dacbc9c2404eeea10398 y
  38eadc8888fc919f05fda17c6b8d68662c6b84370663299c4a7845128e77395f): pasan
  de 95 MB y NO se commitean; en git van sólo los .txt de su capa de texto
  (`pdftotext -enc UTF-8`). Para ver una página en imagen, se vuelven a bajar
  de las URL de `origen_digital`. DERECHOS: dLOC no certifica dominio
  público — su nota dice que el ítem «may be protected by copyright» y lo
  sirve por uso legítimo para investigación. La lectura de esta ficha: Zayas
  murió en 1934; en Cuba (país de origen) el plazo de vida + 50 venció en
  1984, antes del 1 de enero de 1996, así que la URAA no lo restauró en
  EE. UU. → dominio público en origen y en EE. UU. Es una lectura, no un
  dictamen: se usa para investigación, con cita corta, y la decisión de
  redistribuir más es de Miguel. La 1ª ed. (1914) está en HathiTrust como
  «pdus» (sólo EE. UU.) y detrás de una verificación de navegador: no se bajó.
estado_minado: parcial
cobertura: "minado el 2026-09-23 para la lista maestra taína: las 4 voces que Goeje apoya en Zayas, las claves taínas del lexicón que Zayas trae y las voces de la lista sin cronista que Zayas trae como cabeza, más la fauna que describe (6-fusion/taino_zayas_1931.yaml). SIN barrer: el resto del diccionario, sobre todo topónimos y caciques de los repartimientos de 1514"
prioridad: media
verificado: 2026-09-23
minado: 2026-09-23
aliases: ["Zayas 1914", "Zayas 1931", "Zayas y Alfonso", "Lexicografía antillana"]
---

# Zayas y Alfonso 1931 — *Lexicografía antillana* (2ª ed.)

## Por qué entra

La segunda campaña del taíno (`6-fusion/issues-pendientes/taino2-vocabularios-2026-09-22.md`)
la buscó y no la consiguió: «la ficha de dLOC responde 200 y no sirve el
texto». El texto sí está: dLOC es una aplicación de JavaScript, pero el PDF
completo se sirve en su servidor de imágenes (`ufdcimages.uflib.ufl.edu`),
junto a un METS con los metadatos. Se localizó y se bajó el 2026-09-22
(campaña minería 3, F1).

Es fuente citable: [[goeje-1939]] la apoya **con página** en cuatro voces
(`anaki` p. 33, `anaiboa` p. 32, `anua` p. 52, `manaya` p. 78) — páginas de la
**1ª ed. (1914)**, que ésta no reproduce. Medido al descargar en el `.txt` del
t. I: `anaiboa` ×2, `manaya` ×7, `anaki` ×0 (cero de consulta hasta mirar
variantes y el t. II).

## Cómo se lee

- Es comparanda de la **esfera antillana** (taíno), no caquetío (regla 4 y la
  política del préstamo de esfera en `CLAUDE.md`).
- Zayas compila de cronistas y de sus antecesores cubanos (Pichardo,
  Bachiller y Morales): **dos obras que se copian son UNA atestación**
  (minar-fuente §8). Cada voz se lleva a la crónica que Zayas cite.
- La recuperación contemporánea del taíno no es dato (decisión de Miguel);
  Zayas es de 1914-1931 y no entra en esa exclusión, pero sus etimologías son
  suyas, no de la fuente.

## Qué preguntarle

No se lanzó minero (no es de las prioritarias de esta campaña). La pregunta
natural es la de la campaña del taíno: las voces de `6-fusion/taino_lista_maestra_2026-09-22.yaml`
que Goeje apoya en Zayas, verificadas aquí con su fuente declarada.

## Bitácora

### 2026-09-23 — minería 3, parcela Zayas (para la lista maestra taína)

**Qué se preguntó**: (1) qué dice Zayas de las cuatro voces que Goeje apoya en
él; (2) qué cronista del XVI declara Zayas para las claves taínas del lexicón y
para las voces de la lista maestra sin cronista; (3) fauna con descripción.

**Qué se halló** (datos en `6-fusion/taino_zayas_1931.yaml`; cómo engancharlo y
lo que mueve, en `6-fusion/issues-pendientes/zayas-1931-en-la-lista-maestra-2026-09-23.md`):

- De las cuatro de Goeje, sólo `anaiboa` tiene fuente del XVI (Relación de
  Echagoían, c. 1561; ✅ imagen, t. I p. 37). `anaki` es **eyerí** según Zayas
  (✅ imagen, t. I p. 39); `anua` no existe en esta edición y lo más probable es
  que sea `aura` mal leída; `manaya` viene de «las tradiciones haitianas» sin
  nombrar a Pané.
- Zayas **nombra al cronista** con la voz dentro del pasaje en la mayoría de
  las entradas leídas (sobre todo Las Casas, Oviedo, Pedro Mártir, Gómara,
  Herrera y documentos de 1514-1561). Por eso sube de clase voces que la lista
  tenía sin cronista.
- Dos trampas de editor, declaradas por el propio Zayas: `bagua` 'mar' viene del
  apéndice de la Academia a Oviedo (como `datihao`), y la «haba de oro» del
  editor de los Documentos Inéditos es un error que Zayas corrige con Las Casas.
- Un conflicto entre cronistas: `manatí` (Las Casas: «los que llamaban los
  indios manatíes»; Oviedo: nombre de los cristianos).

**Cómo se lee esta obra** (clave ortográfica para `leer-fuente` §5): la capa de
dLOC es OCR; confunde c/e y ñ/fi y **se come las glosas en cursiva** (`Anaquí.— i`
por «Enemigo, en el dialecto Eyerí»). Algunas cabezas salen sin raya
(`Aji. Planta…`, `Caney.`), y un parser de «Cabeza.—» no las ve. Página impresa
= PDF − 27 (t. I) y PDF − 7 (t. II). Las imágenes se bajan por página, sin el PDF
entero: `…/AA/00/08/98/31/00001/NNNNN.jpg`, con NNNNN = PDF + 10 en el t. I (medido
en tres páginas); el desfase del t. II no se midió.

**Qué NO se halló / qué falta**: ninguna de las siete claves del lexicón
`sin-voz-en-la-lista` está en Zayas (medido sobre las cabezas). No se barrió el
diccionario entero. Sólo dos entradas se verificaron en imagen.

## Enlaces

[[goeje-1939]] · [[bachiller-morales-1883]] · [[pichardo-1862]]

---

## Bitácora: sus siete voces, llevadas a la fuente primaria (2026-09-23, cc.7)

Miguel pidió decidir, «en base a lo que decía el texto», si las voces que
Zayas trae son taínas. Se fue a los pasajes que Zayas cita, o que debió
citar. Cuatro correcciones a lo que dejó la parcela de Zayas (#220):

- **Bagua** (t. I p. 72). Zayas cita sólo el apéndice de la Academia, pero la
  voz está en el **cuerpo** de Oviedo, t. I p. 436 (✅ imagen): «Llaman los
  indios de aquesta Isla Española á la mar *bagua*». Es taína, y la `lectura`
  de `taino_zayas_1931.yaml` («la voz sigue sin cronista») hay que
  corregirla: el cero era del OCR, que se come la cursiva.
- **Aura** (t. I p. 60). Es la voz que Goeje p. 14 cita (✅ imagen: «vautour T
  *aura* (ZAYAS, p. 52…)»). `anua` era un error de la transcripción de Goeje
  del repo, no de Goeje.
- **Manatí** (t. II p. 178). La cita de Las Casas es fiel: Apologética p. 27
  (✅ imagen).
- **Tabaco / Cohoba** (t. II p. 254; t. I «Cohoba»). La afirmación de Zayas de
  que la planta se llamaba «Cojoba o Cojiba» no tiene cronista: viene del
  glosario del editor de Oviedo (1855) y de Pichardo (1862). Los pasajes que
  él mismo cita son del rollo (tabaco) y del polvo y el rito (cohoba).

Detalle y etiquetas: `6-fusion/fuentes_poporo_coro_zayas_2026-09-23.yaml` §zayas.
