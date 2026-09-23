---
tipo: fuente
obra: "Colección de los viages y descubrimientos que hicieron por mar los españoles desde fines del siglo XV, tomo III: Viages menores, y los de Vespucio; poblaciones en el Darién; suplemento al tomo II"
autor: "Fernández de Navarrete, Martín"
anio: 1829
genero: cronica
publicacion: "Madrid, Imprenta Real, 1829. Edición documental: Navarrete reconstruye cada viaje menor a partir de los autos de los pleitos colombinos, las capitulaciones reales y las relaciones impresas, y publica los documentos íntegros en la Sección Tercera y el Apéndice"
edicion_del_ejemplar: "ejemplar de la Biblioteca Nazionale di Napoli digitalizado por Google; la portada sale '1839' en el OCR, la fecha bibliográfica es 1829"
local: "fuentes_caquetios/Navarrete_1829_Coleccion_Viages_t3_Viages_Menores_Vespucio.txt"
paginas: "~470 + apéndices"
capa_texto: si
estado_minado: parcial
cobertura: "la Sección Primera entera (viajes menores de 1499-1502: Hojeda–La Cosa–Vespucio, Niño y Guerra, Bastidas, Hojeda 1502) y los pasajes de Vespucio sobre la isla de los Gigantes — 2026-09-22, campaña del taíno 2, T7 + la COSTA OCCIDENTAL 1499-1502 y su gente, por esferas (Sección Primera pp. 3-41 entera, docs. X-XI y XVII-XX, suplemento doc. XLVII, pleitos pp. 543-545 y 590, Vespucio pp. 210-262) — 2026-09-23, minería 3, M2"
prioridad: alta
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-09-23
minado: 2026-09-23
descargado: 2026-09-22
origen_digital: "archive.org/details/bub_gb_HFzXrEyoeCAC — texto OCR (bub_gb_HFzXrEyoeCAC_djvu.txt), 1.766.446 bytes, sha256 2574a0dca4fd41083a68596a3b180492f671febb20dd9202940c9c7be69ec251. Dominio público (Public Domain Mark 1.0 declarado por archive.org; ed. 1829). Descargado el 2026-09-22 con la autorización de Miguel de esta campaña"
aliases: ["Navarrete 1829", "Navarrete t. III", "Viages menores", "Colección de los viages y descubrimientos t. III"]
---

# Navarrete 1829 — *Colección de los viages y descubrimientos*, tomo III

## Por qué está aquí, y por qué debería haber llegado antes

**Es el tomo de los viajes que sí pasaron por la Kaketiana.** Colón nunca fue a
Coro; Hojeda, Juan de la Cosa y Vespucio sí, en agosto de 1499, y Hojeda volvió
en 1502. Este volumen reconstruye esos viajes y —lo que importa— **publica los
documentos**: las capitulaciones reales, las instrucciones de a bordo y las
declaraciones juradas de los pleitos, con folio.

Lo trae la parcela T7 para la etnohistoria del contacto, pero alimenta al menos
tres esferas más: geografía política (los nombres indígenas del golfo y de los
cabos), topónimos (Coquibacoa, Curiana, San Román, los Gigantes) y fuentes (los
autos del pleito Hojeda-Vergara-Ocampo, que nadie ha leído).

## Estado técnico (verificado 2026-09-22)

Texto OCR de archive.org, 1.731.319 caracteres. Escaneo de Google sobre un
ejemplar napolitano: erratas abundantes (`Cutiana` por `Curiana`, `Hojcda`,
`Quinquíbacoa`), pero legible. El folio impreso va dentro del flujo
(`14 VIAGES MENORES` / `SECCION PRIMERA. 33`), así que la cita se verifica sin
la imagen. El PDF (21,7 MB) **no** se bajó: la URL está arriba.

🔴 **La trampa que costó tres consultas a cero.** El `_djvu.txt` separa las
palabras con **dos** espacios: `tierra firme` devuelve 0 y `tierra-firme`
devuelve 52; `no se entendian` devuelve 0 donde la frase está entera. Toda
consulta de más de una palabra tiene que ir con `\s+`. Lo cose
`6-fusion/scripts/medir_taino2_etnohistoria.py` (función `patron()`).

## Qué se preguntó (2026-09-22, campaña del taíno 2, parcela T7)

Las cinco preguntas de la parcela. **Medido**: `paria` 116 · `curiana` 28 ·
`guanin` 23 · `coquibacoa` 16 · `vespuci` 172 · `perla` 135 · `canoa` 50 ·
`caribana` 5 — y en el tramo que narra Hojeda 1499 / Niño y Guerra / Hojeda
1502 caen 18 de los 28 `curiana`, 14 de los 23 `guanin` y 6 de los 16
`coquibacoa`.

## Qué ha dado

### 🔴 1. Hay DOS Curianas, y las separa con un documento (toca el issue #33)

> «Ambos llaman **tierra de Curiana**, que es el rescate de las perlas, **á la
> costa que está enfrente de la Margarita, y comprende la costa de Cumaná y
> golfo de Cariaco**. Comprueba esta situación de Curiana el artículo 1.º de la
> capitulación que hizo Hojeda con los Reyes católicos, donde se le previene
> "que no toque en la tierra del rescate de las perlas de esta parte de Paria,
> desde el paraje de los Frailes, antes de la Margarita, fasta el Farallón,
> **tierra que se llama Curiana**". Pedro Mártir dice que desde la punta de
> Paria á Curiana hay ciento y veinte leguas, pero no llegan ni á ciento.
> **Nuestros historiadores trastornaron este viage, porque ignoraron la
> verdadera situación de Curiana.**» — **p. 13, nota 4**

> «El P. Fr. Pedro Simón en su conquista de tierra firme dice, folio 667, que
> **la ciudad de Coro está fundada en una provincia de indios llamada
> Curiana**… que la fundó el año 1517 el capitán Juan de Ampíes, cerca del
> pueblo que los indios llamaron Curiana… **Esta Curiana es distinta de la que
> hemos hablado en la nota 4 de la pág. 13.**» — **p. 32, nota 3**

No es opinión de erudito decimonónico: se apoya en la capitulación real de
Hojeda, que delimita «Curiana» entre los Frailes y el Farallón, frente a
Margarita. **Consecuencia para el repo**: la cita de Anglería sobre
Curiana ↔ Cauchieto, que la primera campaña usó como «la forma de la red»
([[angleria-1892]] §2026-09-21), describe la costa **oriental** de Venezuela.
La conclusión de T5 se sostiene; que sea una red de la Kaketiana, no.

### 2. El primer paso europeo por la Kaketiana, agosto de 1499 (pp. 7-9)

De la ensenada de Coro pasan a **«la isla de Curazao, que llamaron de los
Gigantes»**; luego «á una que juzgaron ser isla, distante diez leguas de la de
Curazao, y en ella vieron el Cabo que forma una península y llamaron **de
S. Román**» (Paraguaná); doblan el cabo y entran en un gran golfo con «una gran
población… fundadas artificiosamente en el agua sobre estacas hincadas en el
fondo y comunicándose de unas á otras con canoas». Y:

> «Llamó Hojeda á este Golfo de Venecia… **Los indios le llamaban Golfo de
> Coquibacoa**»

El nombre indígena del golfo, **dicho como indígena**. De ahí siguen al cabo de
la Vela y vuelven a La Española el 5 de septiembre de 1499.

### 3. Oro en Curazao en 1502 — y la propia fuente lo pone en duda (p. 34, §26)

> «Siguieron juntos poco después á **la isla de los Gigantes (Curazao)**, se
> internaron como media legua hasta llegar á la población de los indios, en
> quienes notaron que **traían ciertos pedazos de oro colgados de las narices y
> orejas**; pero nada les tomaron, ni aún brasil que parece vieron en
> abundancia… Pasaron luego á **Coquibacoa**… **Parecióles el país pobre y
> miserable.**»

⚠️ Nota 3 de la misma página: «Así lo aseguran algunos testigos: **otros
presentados por Vergara y Ocampo dicen que no vieron oro**, y sí muy poco
brasil en la isla de los Gigantes. V. los fol. 19 vto., 17 y otros.»

Testimonio de pleito, con dos partes interesadas. **En duda, degradar**
(regla 2). Si se sostuviera sería metal en las islas de la polity costera en
1502, y el metal no se hace allí. **Se cierra leyendo los folios**, que están
publicados en la *Colección diplomática*, tomo II.

### 4. El guanín de Curiana venía del oeste, y era moneda de rescate (pp. 16-17, 34)

> «servíanse de las perlas… ya para **comerciar con las naciones vecinas, y
> adquirir guanines que indicaban venirles de una provincia llamada Cauchieto,
> que estaba al occidente á seis soles ó dias de distancia**»

Y en 1502, con las indias que Hojeda tomó por la fuerza: «unas se rescataron
**por guanines**… Los pobres indios venían después con seguro á rescatar estas
mismas prendas **á precio de guanines**» (p. 34). El guanín funcionando como
unidad de rescate en Tierra Firme.

> 🔴 **Corregido el 2026-09-23 (minería 3, M2).** Este apartado junta las dos
> Curianas. Las pp. 16-17 son la **oriental** (Niño y Guerra, 1499); el
> rescate de 1502 es de la **occidental** —«una tierra de riego que los indios
> llamaban Curiana y él nombró Valfermoso» (p. 32)— y está en la **p. 33**, no
> en la 34. Y «adquirir guanines que indicaban venirles de… Cauchieto» es frase
> de Navarrete (o de Muñoz): Anglería, su fuente, no usa la palabra. Ver abajo
> §2026-09-23 y `6-fusion/cronicas_contacto_costa_occidental_2026-09-22.yaml`
> (m2.m1).

### 5. La lengua: el negativo medido (p. 34)

`intérprete` sale **19** veces en el volumen y **cero** en todo el relato de los
viajes menores por esta costa. `lengua` sale **una** vez en ese tramo, y es un
español:

> «se presentó **Juan de Buenaventura**, á quien Bastidas dejó en la provincia
> de Citarma, que es tierra nevada (Provincia de Sta. Marta), y había
> permanecido **trece meses** tratando con los indios y **aprendiendo su
> lengua**»

### 6. Vespucio sobre la isla de los Gigantes (Sección Segunda, pp. 258-260)

Navarrete imprime el latín y su traducción. Vespucio sólo cuenta peleas: «**no
consentían que tomásemos cosa alguna de su país**», y bautiza la isla «de los
Gigantes» por la talla de sus habitantes. Ni una palabra de lengua ni de trato.
⚠️ Navarrete es explícitamente escéptico con él: «Por ventura nació la voz de
entender mal las expresiones de horror con que se indicaban los Caribes, y eso
bastó á Vespucci para fingir que había visto Pantasileas y Anteos» (p. 7), y
añade que en 1502 «volvieron á reconocer esta isla… y **no hallaron ningún
gigante ni giganta**». Para datos de Vespucio, capa baja.

### 7. Los pleitos colombinos, con la Kaketiana dentro (p. 543)

Pregunta 5.ª del interrogatorio: «descubrieron en la costa de Tierra firme
hacia el poniente **desde los Frailes é los Gigantes fasta la parte que agora
se llama Coquibacoa**». Es la ruta declarada bajo juramento: **costeando**.

## Qué NO da

- Ni una noticia de tráfico entre las ABC y las Antillas Mayores.
- Ni una palabra de la lengua de Coquibacoa o de los Gigantes. Nadie apuntó
  nada: preguntaron por el oro y por las perlas.
- Ni una mención de Manaure, de los caquetíos por su nombre, ni de Paraguaná
  con ese nombre (el cabo es «de S. Román»).

## 2026-09-23 — la costa occidental y su gente (minería 3, parcela M2)

**Qué se preguntó.** Lo que T7 no: qué cuenta el tomo de la costa de Tierra
Firme occidental —Coquibacoa, San Román, Paraguaná, Coro, las dos Curianas,
los Gigantes— y de su gente, esfera por esfera, más toda mención de animales y
del mar. Leído a mano: la Sección Primera entera (pp. 3-41), los documentos X,
XI y XVII-XX (pp. 85-108), el doc. XLVII del suplemento (pp. 518-519), los
pleitos de las pp. 543-545 y 590, y la Lettera de Vespucio pp. 210-262. El
volumen entero, barrido con `6-fusion/scripts/medir_cronicas_costa_occidental.py`,
que además cose los guiones de fin de línea (`Co-`/`quibacoa`) y asigna cada
`curiana` a la oriental o a la occidental con reglas declaradas. Datos y citas:
`6-fusion/cronicas_contacto_costa_occidental_2026-09-22.yaml`.

**Qué dio (lo nuevo):**

- **La Curiana occidental de 1502** (p. 32): «una tierra de riego que los
  indios llamaban Curiana y él nombró Valfermoso», donde Hojeda firmó la
  instrucción del 7 de abril (doc. XIX, p. 107). Coro según Navarrete (p. 8
  n. 3), con su itinerario en contra (Puerto Flechado). El OCR dice «rieeo».
- **El rescate «á precio de guanines»** allí mismo (p. 33).
- **La cédula del 3-IX-1501** (suplemento, pp. 518-519): los castellanos sacaban
  guanines «de las islas de la Paria é de Caquibacoa» y se los vendían a los
  indios de La Española. El vector castellano del guanín, documentado.
- **Isabel**, la intérprete indígena de 1502 (doc. XX, pp. 107-108; p. 36 n. 1).
- **La capitulación**: la «isla» de Coquibacoa «donde están las piedras
  verdes, de las cuales trugistes muestra» (p. 86); y que en 1499 tomaron
  Paraguaná por isla (p. 8).
- **El palafito de Vespucio: «veinte grandes casas»** (p. 219), y distinto del
  lago de San Bartolomé, donde «tomamos las indias» (doc. XVIII, p. 105).
- **La isla de los Gigantes**: cinco casas en una hondonada (p. 256); y la
  **isla de las hierbas** (pp. 251-255), con hierba y polvo blanco en
  calabacitas, que Navarrete tiene por Marajó y el relato pone junto a Curazao.
- **Las grafías de Coquibacoa** de los documentos, que el medidor lista con
  folio: ⚠️ **todas del OCR**, sin ver en imagen.

**Qué NO dio:** ni Paraguaná ni Aruba ni Bonaire por su nombre, ni los
caquetíos, ni una palabra de la lengua de esa costa.

**⚠️ Trampas de esta obra, medidas:** (1) el guion de fin de línea parte
`Co-quibacoa` y `ti-gres` (en Hernando): se cose antes de contar; (2) las
cabeceras del OCR traen folios rotos (`303` por `203`, `91` por `21`): el
medidor se queda con la cadena que crece a ritmo de página y marca con «≈» lo
interpolado; (3) Navarrete pone palabras que su fuente no tiene («guanines»,
«macanas», pp. 15 y 17, donde Anglería escribe «oro aunque no puro» y
«armados á su modo»).

## Qué falta

- **Verificar en imagen** las pp. 32 («riego»), 86-89, 518 y 544 (las grafías
  de Coquibacoa). El PDF no se bajó; está en archive.org
  (`bub_gb_HFzXrEyoeCAC`).
- **Los autos del pleito Hojeda-Vergara-Ocampo**, citados aquí por folio
  (fols. 16-17, 19, 21, 29, 44, 67, 69-73, 85-88) y publicados en la
  *Colección diplomática*, tomo II de esta misma obra. Cerrarían el punto del
  oro de Curazao.
- La Sección Tercera (poblaciones en el Darién) y el Apéndice entero: leídos
  sólo de paso.
- **Pedro Simón, *Noticias historiales***, que es la otra pata del issue #33.

## Enlaces

[[angleria-1892]] · [[colon-hernando-1892]] · [[navarrete-1859-viages-colon]] ·
[[oliver-1989-cap3]] · [[gonzalez-batista-nombre-de-coro]]
