# Oliver 1989, lo que quedaba a medias: la A-9 entera, los vecinos, los dabajuranos y el mar

**Tercera campaña de minería, parcela M1 (2026-09-22).** Encargo de Miguel:
«lanza agentes paralelos para que minen lo que tenemos pendiente, a medias,
parciales […]», y de la fauna: «tomando en cuenta que el aspecto marino era
esencial en la cosmovisión caquetía».

**Ninguna cifra de este borrador está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/oliver1989_restante.py --check
```

y quedan en `6-fusion/medicion_oliver1989_restante_2026-09-22.yaml`. Los datos,
con página y cita: `6-fusion/oliver1989_lexico_restante_2026-09-22.yaml`
(lengua) y `6-fusion/oliver1989_restante_2026-09-22.yaml` (mundo, con la clave
`fauna:` del preámbulo).

---

## 0. Lo que resultó falso al medirlo

1. **Las correspondencias C1-C13 no están en el Apéndice A.** El apéndice son
   tablas, nada más; las correspondencias están en el cap. 2 (Tabla 3 y §2.5-2.8),
   que ya es `minado`. Lo que sí se hizo fue ponerlas a predecir sobre la A-9
   (§2.3).
2. **Oliver no le da a D9 una segunda fuente para 'cerro'.** La ficha del
   apéndice lo afirmaba por la fila 17 («a hill in Paraguaná»). Pero la fila 2
   glosa `-bana` como **«surrounding»**, y el cap. 2 (DOC p. 150) lo explica por
   el lokono 'alrededor, extensión, techo'. «A hill» describe el REFERENTE de
   Capubana. Oliver está del lado de 'cubierto' — el mismo que van Buurt §6, que
   llega «vía Oliver»: son una sola atestación. D9 no cae (sus seis apoyos no
   incluían a Oliver); cae la frase de la ficha.
3. **La A-9 no tiene 49 filas ni 33 números sin asignar.** Tiene 50, todas
   numeradas y en orden alfabético: el dictado no tenía la 48, `taboro`. Y las
   cursivas no son tres filas sino cuatro: la 4 `baperón` también va en
   cursiva. Siguen siendo tres referentes, porque la 47 dice «(also baperón)».
4. **La nota «Tamanaco» junto a 'luna' en la Tabla 8 no existe.** La repetían
   `tabla_a8_jirajarano.yaml` y la ficha de los vecinos como «préstamo caribe
   dentro del jirajarano». Mirada en imagen, la fila 73 no la lleva. El Tamanaco
   que Oliver sí nombra está en el cap. 2, y es para `capu` y `cachicamo`.
5. **No hay zooarqueología de Oliver que minar.** «all of the faunal remains
   recovered at Túcua and at Corralito. These remain lost as well» (p. 438
   n. 305). Lo que hay es lo que el texto nombra de pasada, y está en `fauna:`.
   Coincide con lo que trajo la parcela de Urbina/Casale/Knaf (PR #203): casi
   cero.
6. **La Tabla 15 «recalibrada en 2006» tiene las mismas cifras que la de
   1989.** `tabla15_c14_oliver.yaml` salió del .DOC y dice que Oliver la
   recalibró con OxCal para el PDF de 2006. Leída en el escaneo de 1989 (p. 459,
   en imagen): cero filas difieren (medición §tabla15). La calibración que el
   texto declara es Stuiver y Reimer 1986.
7. **La A-1 no es un «vocabulario paraujano completo».** Es una página: el
   formulario Swadesh-100 de Wilbert rellenado a mano, que es la fuente de la
   columna paraujana de la A-2 ya transcrita.

---

## 1. Qué se preguntó y qué dio, por esfera

### 1.1 Lengua — la A-9 entera, en imagen

Todas las filas (§a9_vs_lexicon.filas), con su número, forma, fonémica, las dos glosas, la cursiva y,
cruzando con el §2.8 del cap. 2, **de dónde saca Oliver cada voz**. El estado de
cada fila contra el lexicón lo mide el script (§a9_vs_lexicon): la gran mayoría
ya está activa como caquetía; las ausentes y las que sólo son referencia van
con nombre en la medición.

Lo que cambia algo:

- **`busera`**, la jagua (tinte negro-azulado), no está en el lexicón con
  ninguna grafía. Oviedo t. II p. 300, en el cuerpo, la llama busera; la bixa
  roja va al lado como otra cosa. Oliver acierta en la A-9 («pintura
  negra-Genipa») y se equivoca en la n. 213 del cap. 3 («red [...] Bixa»), que
  es la glosa del EDITOR de Oviedo. Una atestación (Oviedo), no dos: Oliver
  bebe de él. Propuesta: `caquetío-atestiguado`, dominio creencia (el segundo
  funeral del díao).
- **`kama` 'danta' no es SIN_RASTRO.** Su nota dice que su «ruta» era la fila
  tapir de la A-7, que no existe. La fila está en la A-9 (15) y el cap. 2 da la
  fuente: la Relación de Barquisimeto de 1579. Y hay huesos de tapir en los
  fogones de Túcua (cap. 4, p. 439). Propuesta: subirla, con la polity de
  Barquisimeto declarada.
- **`auri` 'perro' no es caquetío atestiguado**: Oliver lo halló en una lista
  CUYÓN y lo infiere prestado del caquetío de Barquisimeto (cap. 2, p. 151; en
  la Tabla 8 va en la columna cuyón, «(ARAWAKAN)»). La clave está ocupada por
  la comparanda achagua.
- **La época y la polity de la A-9**: el título dice «from the XVIth century»,
  pero la fuente que Oliver da para `dare` es habla viva de Paraguaná (años 80),
  para Capubana una leyenda que oyó en Santa Ana, y para varias la Relación
  de Barquisimeto de 1579 (regla 4; cuáles, en
  §a9_vs_lexicon.fuente_relacion_de_barquisimeto_1579). Va fila por fila en el YAML.
- **`çabana`**: con la ç leída /s/, como la transcribe Oliver, no está; sólo
  aparece si la ç se lee c, como `kabana` (medición §a9_vs_lexicon). Una
  cedilla perdida puede estar dando /k/ a una /s/.
- **`guarataro`** (cap. 4, p. 447): «a fossilized oyster [...] burned and
  crushed», desgrasante de la olla en Corralito. Tercera fuente, y converge con
  Medina (el desgrasante) contra Zavala/Esteves (el barro).
- **`Túcua`** 'punta, cuerno' (p. 438, en imagen) y **`zazare /çaçare/`**, la
  matriz calcárea del desgrasante (p. 438): la primera, etimología de Oliver por
  el lokono; la segunda, término de alfarería sin lengua declarada. Ninguna
  está en el lexicón ni en la mesa de topónimos.

### 1.2 Las correspondencias, a predecir

En la A-9 no cursiva no hay **ninguna** voz con /p-/ inicial y sí varias con
/b-/: C3 no falla en la muestra de Oliver. Pero es una selección suya, hecha,
dice él, por su «higher degree of inference a correlation with other Arawakan
languages». En las claves `caquetío-atestiguado` del lexicón sí hay /p-/
iniciales (la medición las lista): C3 no se rompe en su propia muestra, y eso
no es probarla.

### 1.3 Tabla 8 (jirajarano): lo que faltaba

Las filas de la p. 592 que el OCR no había dado (§mundo.tabla8_filas_nuevas_p592:
casa, venado, culebra, conejo, armadillo, báquiro, danta, perro, maíz, yuca,
hamaca…), los porcentajes, las fuentes (Jahn 1927, Loukotka 1968, Oramas 1916)
y el árbol. **Hay porcentajes impresos que no cuadran con su fracción**
(cuántos y cuáles, §a8_aritmetica).

### 1.4 Mundo — los vecinos (cap. 3, §3.2.3 y §3.3)

Grupos con página (§mundo.vecinos_con_pagina): coanao, wanebucán, tairo,
xiriguana, haruacana, jirajara, ayomán, gayón, xagua, camagos, y el chipa.
**Todos menos el chipa faltan en `3-mundo/etnias.yaml`**
(§mundo.vecinos_sin_entrada_en_etnias_yaml). Lo que más pesa:

- **El jirajara es el vecino de tierra adentro de la polity costera**: la
  Sierra de San Luis está «three leagues from the city of Coro»; en paz, entre
  1527 y 1530, abastecían de maíz a Coro; y Oliver propone que las «hijas de
  caribes» con que estaba casado Manaure eran jirajaras de San Luis. Sería la
  primera entrada de `etnias.yaml` con `polity_caquetia: costera` y fuente.
- **Contradicción con `etnia-003 ciparicoto`**: el canon dice arahuaca (Zavala
  vía Molina); Oliver, «clearly different from the Caquetío, and perhaps
  related to Carib» (p. 251). En duda, degradar a `desconocida`.
- **Los coanaos**: socios de sal por oro; Esteban Martín hablaba con ellos en
  caquetío sin intérprete — la lengua caquetía como lengua de trato en la
  Guajira.

### 1.5 Manaure: dónde vivía (al lado de lo que trajeron otras parcelas)

Oliver da dos cosas que no hay que fundir. **Antes del pacto**, como corazonada
declarada: su sede era el cacicazgo de **Caçicure, en Pueblo Viejo** (FAL-77,
al NE de Mitare) — tesis p. 277 n. 206. **Desde 1527**, dato: se reasienta
junto a Coro, en **Todariquiba**, «about 1 or so leagues from Coro», y Oliver
sospecha que quedó dentro del Coro moderno (DOC pp. 251, 259). Con eso, Cey 1545
(«en Coro») y el documento de 1527 («Todariquiba») pueden estar diciendo el mismo
sitio. Lo único que toca el precontacto es Caçicure, y es hipótesis de Oliver.

### 1.6 Arqueología (cap. 4, §4.7-4.15)

La cronología dabajurana con sus fechas, los sitios con lo que el texto dice
de cada uno, la cultura material (dos vajillas, concha como desgrasante, el
paso del budare al aripo —«from caçabe to arepa»—, el maíz desde el principio,
el cuenco tetrápodo del masato funerario, el batracio y el ave), y **metal: cero
en la arqueología**. Contactos: hacia el norte, sólo las ABC y dentro de la
polity (cero menciones de las Antillas Mayores en el cap. 4: §antillas); hacia
el oeste, **una ruta de mar** Ranchería–Curazao–Coro después de 1300.

### 1.7 Fauna (clave `fauna:`)

Las entradas por obra y época están en la medición (§fauna). Sólo una lleva
especie porque la fuente la da (Donax, el chipichipi de los concheros de Pueblo
Viejo, en un pie de foto de 2006). Ninguna trae sonido: **Oliver no describe
cómo suena ningún animal**.

---

## 2. El mar: con cita, y el cero medido

**Lo que Oliver sí dice** (todo con página en el YAML, §mar): la polity costera
«had also learned maritime navigation, and had colonized the Netherlands
Antilles» hacia 1100-1200 (p. 483, en imagen); desde 1300 una ruta marítima
Ranchería–Curazao–Coro (pp. 474-477); parientes en Curazao; amuayes y guaranaos
con sus playas y «specific fishing grounds»; concheros en todos los sitios
cerca de la costa; cuentas de concha casi como moneda; y los ayomanes, tierra
adentro, que compraban conchas porque «they know nothing about the sea».

**Lo que no dice**: ni un rito, un ser, una ofrenda ni un tabú ligados al mar en
la polity costera. El script busca ventanas de texto donde una palabra del mar
coincida con una de la creencia en los cinco textos (§mar); las pocas que salen
son falsos positivos (un cosmógrafo, las islas «under the control of Manaure»
junto a su poder sobre las tormentas, una nota sobre la danza de las turas). Lo
sagrado que Oliver da a la costa es el poder de Manaure sobre la lluvia, el
granizo, el trueno, la sequía y «the fruitfulness of the land»: cielo y tierra
de cultivo.

**Lectura**: Oliver no refuta la tesis de Miguel; no tiene con qué. Su fuente de
creencia costera es mínima y ninguna le pregunta al mar. Lo que sí sostiene es
que la polity costera se hizo navegando. Llevar eso a creencia sería
`hipotetico`.

---

## 3. Cobertura real, por capítulo

| Parte | Qué se leyó en esta parcela | Qué queda |
|---|---|---|
| Apéndice A | A-9 entera en imagen; Tabla 8 entera (p. 592 en imagen); A-1 identificada | **A-3 a A-7** sin transcribir (sólo la fila 53 'liver', de antes); A-1 sin cotejar con la columna paraujana de la A-2 |
| Cap. 3 §3.2.3 | tesis pp. 211-222, OCR guardado | — |
| Cap. 3 §3.3 (3.3.1-3.3.3) | tesis pp. 231-254, OCR guardado | — |
| Cap. 3 §3.2.4 | (minado el 2026-09-07) | — |
| Cap. 4 §4.7-4.15 | tesis pp. 411-487, OCR guardado; Tabla 15, pp. 438, 439, 456, 483 en imagen | §4.1-4.6 (la tradición Macro-Tocuyanoide, pre-caquetía); las Tablas 16-17 (frecuencias de bordes); los Apéndices C (figuras) y D (histogramas; sólo se miró el perfil de Corralito, D-77) |

Lo que no se pudo y dónde está: la **Relación de Nueva Segovia de Barquisimeto
(1579)** en Arellano Moreno 1964 — la fuente de varias voces de la A-9 — no está en
el repo; el manuscrito **Oliver Ms. 1987c** (donde estarían la fauna y el
análisis de Pueblo Viejo) no está publicado.

---

## 4. Opciones para Miguel

- **A.** Tomar la A-9 verificada como la tabla de referencia (el dictado queda
  como historia) y aplicar las notas del YAML léxico: `busera` nueva, `kama`
  sube con Barquisimeto declarado, `auri` no sube, notas en `warataro`,
  `kumarawa`, `dare`, `baperón`/`raporón`, `capu`/`kapubana`.
- **B.** Además, `etnias.yaml`: los grupos que faltan, con el jirajara
  como vecino de la costera (`hipotetico` por la boda) y `etnia-003` degradada
  a familia `desconocida`.
- **C.** Registrar la tesis del mar como hecho `hipotetico` de creencia,
  apoyado en la navegación (dato) y sin dato de creencia (declarado).
- **D.** Nada al canon todavía: pedir antes Arellano Moreno 1964 a la parcela
  de búsqueda, porque decide la época y la polity de las voces de la A-9 que
  Oliver saca de ella.

**Recomendación: A + B ahora, D en paralelo, C no.** A y B son dato con página
y no dependen de nada; D mejora A sin bloquearla; C sería escribir en la
creencia lo que la fuente no dice.

## 5. Visto de paso (para otra campaña)

- `tabla15_c14_oliver.yaml` y el texto discrepan en ISGS-1423 (tabla 550 ± 110,
  texto p. 456 500 ± 110) y la p. 436 llama a Túcua «FAL-69» (es FAL-60).
  Erratas del original; el registro de nodos debería anotarlas.
- La ficha `oliver-1989-cap4` dice `capa_texto: si` y el `.DOC` que la
  justificaba no está en el repo: el capítulo sólo existe en el escaneo, sin
  capa. Corregido en la ficha.
- El pie de foto de Pueblo Viejo y otras «Illustration added for the PDF
  version only» muestran que el `.DOC` del cap. 3 es la **revisión de 2006**, no
  la tesis de 1989: citar por él mezcla dos ediciones.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
