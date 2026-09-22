---
tipo: fuente
obra: "Historia general y natural de las Indias, tomos II, III y IV"
autor: "Fernández de Oviedo y Valdés, Gonzalo"
anio: "1852-1855 [s. XVI]"
genero: cronica
publicacion: "Madrid, Imprenta de la Real Academia de la Historia. Tomo II (segunda parte, libros XX-XXVIII) 1852 · tomo III (segunda parte, libros XXIX-XXXVIII) 1853 · tomo IV (tercera parte, libros XXXIX-L, + glosario e índices) 1855. Ed. José Amador de los Ríos, cotejada con el códice original"
edicion_del_ejemplar: "digitalización de la Biblioteca Ludwig von Mises, Universidad Francisco Marroquín (colección Shook), en Internet Archive"
local:
  - "fuentes_caquetios/Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf"
  - "fuentes_caquetios/Oviedo_Valdes_1853_Historia_General_Indias_vol3.pdf"
  - "fuentes_caquetios/Oviedo_Valdes_1855_Historia_General_Indias_vol4.pdf"
paginas: "t. II: 544 pdf / 530 impresas, desfase 13 · t. III: 680 pdf / 646 impresas, desfase 13 hasta la pdf ~150 y 15 desde ahí · t. IV: 656 pdf / 622 impresas, desfase 15"
capa_texto: si
estado_minado: minada-parcial
cobertura: "t. II Libro XXV entero (el de la Provincia de Venezuela, impresas 269-332): caps. IX y XXII leídos línea a línea, el resto por barrido de las diez fórmulas de nombrar. t. IV: el glosario «Voces americanas empleadas por Oviedo» (impresas 593-607) y su bibliografía (608), enteros. t. III: sólo sondas, y dio cero. El detalle en `6-fusion/taino2_oviedo_venezuela.yaml` → `meta.cobertura_real`"
acceso: "Dominio público, descargados el 2026-09-22 de Internet Archive (los tres registros llevan `possible-copyright-status: NOT IN COPYRIGHT`). t. II https://archive.org/details/historiageneral01fernguat (45.433.954 B, sha256 a9fb3477b3e5250ea8147343b9b10e90c66c7f9018291187b6892615a14fbbd7) · t. III https://archive.org/details/historiageneral02fernguat (54.727.062 B, sha256 3e795e42f22785ab1007147023113c0881f22fc9dad545302ec407e3fffcfa77) · t. IV https://archive.org/details/historiageneral04fernguat (53.090.352 B, sha256 0d5dcc0270726c2b376e658ac53e856246c30375a8dd0eb958986171719f4a40). Los tres pesan menos de 95 MB y están commiteados. El tomo I de la misma digitalización, con la imagen íntegra, es `historiageneral00fernguat` (55.449.811 B) y sigue sin descargar"
prioridad: alta
verificado: 2026-09-22
minado: 2026-09-22
aliases: ["Oviedo t. II", "Oviedo t. III", "Oviedo t. IV", "Oviedo 1852", "Oviedo 1855", "Historia general y natural tomos II-IV", "Apéndice del tomo IV", "Voces americanas empleadas por Oviedo"]
---

# Oviedo y Valdés — *Historia general y natural de las Indias*, tomos II, III y IV

> El tomo I tiene su propia nota: [[oviedo-y-valdes-1851]]. Esta cubre los tres
> que faltaban y que el repo llevaba un año citando de oídas.

## Qué es, y por qué hacía falta

La edición de Amador de los Ríos (Real Academia de la Historia) es la **única
completa** de la obra: los cincuenta libros de Oviedo en cuatro tomos. El repo
sólo tenía el primero. En los otros tres estaban cuatro cosas que el canon cita
y nadie había visto: el **libro de la Provincia de Venezuela**, el **díao**, el
**boratio** y el **apéndice de voces del tomo IV**.

Están las cuatro. Y una de ellas dice algo distinto de lo que creíamos.

## 🔴 Lo primero: el apéndice del tomo IV existe

`oviedo-y-valdes-1851.md` decía, el 2026-09-21, que «el "apéndice de voces" del
editor no existe», y lo daba por «coherente con el rastreo del 2026-08-14 sobre
el tomo IV».

Existe. Se llama **«VOCES AMERICANAS EMPLEADAS POR OVIEDO»**, ocupa las impresas
**593-607 del tomo IV** y lo cierra una **BIBLIOGRAFIA** de los 23 vocabularios
que el editor manejó (impresa 608). Es el apéndice que Jahn 1927 p.213 n.29 cita
como fuente de seis voces caquetías, y trae **doce entradas marcadas «(Lengua de
Venezuela)»**.

La conclusión de ayer era correcta **sobre el tomo I** —lo que cierra ese volumen
es un índice de capítulos— y se extendió al tomo IV sin tenerlo delante.

## 🔴 Y lo segundo: Oviedo escribe `çaquitios`, no «caquetíos»

Por eso todas las sondas daban cero. El etnónimo sale **12 veces en el tomo II**
(impresas 296, 297, 300, 303-306, 314, 315, 326), en cursiva la primera vez, y
verificado en imagen:

> «En la provinçia de Veneçuela los indios naturales della, en espeçial los de la
> generaçión que llaman *çaquitios*, tienen por costumbre, quando muere algún
> señor ó caçique ó indio prinçipal juntarse todos en aquel pueblo donde el
> difunto vivía…» — t. II, libro XXV cap. IX, impresa **297**

El editor lo moderniza a `zaquitios` en el glosario del tomo IV. **Añádanse
`çaquiti`, `zaquiti` y `saquiti` a las sondas de esta obra para siempre**: es la
trampa de `minar-fuente` §2 en su forma más cara, porque el cero se había
convertido en la afirmación «Oviedo no nombra a los caquetíos».

## Dónde está el libro de Venezuela

**Tomo II, Libro XXV** («libro sesto de la segunda parte»), impresas **269-332**:

> «…el qual tracta de la gobernaçión de la provinçia del golpho de Veneçuela y
> otras provinçias, questán por sus Magestades encomendadas á la grand compañía
> de los alemanes Velzares en la Tierra-Firme.»

Dos capítulos concentran casi todo:

| Cap. | Impresas | Qué trae |
|---|---|---|
| **IX** | 297-302 | el funeral de los çaquitios, el boratio y su cura, el díao y su funeral de dos tiempos, `maçato`, `caça`, `busera`, `mene` |
| **XXII** | 328-332 | el ayuno ritual, los grados de nobleza por tatuaje, y el párrafo de flora y fauna con `tara`, `datos`, `comoho` y `çemyrucos` |

El cap. XXII **declara su testigo**: todo lo que cuenta se lo dijo «á voce viva»
el obispo **don Rodrigo de Bastidas**, corroborado por el tesorero Acuña, el
contador Naveros, Pedro de Salvatierra y el capitán Pedro de Limpias. Es una
cadena de custodia explícita, que es más de lo que tiene casi ningún hecho del
corpus.

## Estado de los tres PDF

Los tres son **sanos**: `pymupdf` los abre sin reparar, `pdftotext` funciona y
**la imagen está completa**. Nada del calvario del tomo I (truncado, y con el
escaneo roto desde la impresa 155).

```python
import pymupdf
d = pymupdf.open("fuentes_caquetios/Oviedo_Valdes_1852_Historia_General_Indias_vol2.pdf")
d[i].get_text()          # impresa = pdf − 13 en el t. II
```

### ⚠️ Pero el OCR sigue sin servir para contar

Dos razones, las dos medidas:

1. **La ç sale `g`, `f`, `r` o `z`**, igual que en el tomo I (`hager`, `diçen` →
   `digen`, `çaquitios` → `gaquitios`/`raqiiitios`).
2. 🔴 **La caja de dos columnas parte las palabras a fin de línea** y la capa OCR
   conserva el guion. Sin deshacerlo, el conteo miente:

| Voz | `grep` crudo | con el guion deshecho |
|---|---|---|
| `çaquitio` | 9 | **12** |
| `boratio` | 16 | **18** |
| `Veneçuela` | 31 | **39** |
| `çemyruco` | **0** | **1** |

Y aun deshaciéndolo, `busera` y `datos` siguen dando **0**, porque el OCR las
destroza (`Intsera`, `dalos`). Las dos están en la página y se leyeron con los
ojos. **En esta edición el conteo es siempre una cota inferior.**

### El desfase no es constante en el tomo III

t. II: **13**, constante (301 de 314 encabezados legibles). t. IV: **15**,
constante (341 de 357). t. III: **13** hasta la pdf ≈150 y **15** desde ahí. No
afecta a ninguna cita porque el tomo III no dio nada — pero la frase «se calcula
UNA vez por tomo» no vale aquí.

## Qué ha dado — minería del 2026-09-22 (2ª campaña del taíno, T6)

Datos en [`6-fusion/taino2_oviedo_venezuela.yaml`](../6-fusion/taino2_oviedo_venezuela.yaml),
discusión en
[`6-fusion/issues-pendientes/taino2-oviedo-ii-iv-2026-09-22.md`](../6-fusion/issues-pendientes/taino2-oviedo-ii-iv-2026-09-22.md).

**Lo mejor, por si se lee sólo esto:**

- **`datihao` no está en el libro de Venezuela.** Ver la sección siguiente: es el
  hallazgo que más mueve.
- **`diao`** (t. II pp.299-300, imagen) — «en algunas partes desta gobernaçión de
  Veneçuela el señor prinçipal, que tiene muchos indios y le son subjetos otros
  caçiques, **llámanle *diao***». Nótese: *algunas partes de la gobernación*, no
  *los çaquetíos*, y **sin decir en ningún momento que sea un boratio**.
- **`boratio`**, con una sola t, 18 veces (pp.298-299, imagen), con el rito de
  cura entero — el ayuno impuesto a la casa, el soplo («Allá yrás mal»), el
  chupar, la espina escondida —, que el corpus no tiene.
- **El funeral del cacique común está en la p.297, no en la 299-300**, y es el
  único de los dos que Oviedo atribuye **explícitamente a los çaquitios**.
- **`tara` = langosta**, descrita como plaga y como comida (p.331). Cuarta fuente
  y la primera de primera mano contra la glosa 'venado' del lexicón.
- **Tres voces vivas de Falcón con atestación de 1548 y glosa del cronista**:
  `datos` (el cardón alto), `comoho` (la tuna) y `çemyrucos` (el semeruco, «la
  fructa es muy semejante en la vista á las çereças»). Las tres en la p.331; las
  tres invisibles al OCR o al conteo; las tres leídas en imagen.
- **`Curiana` es un río** para Oviedo, entre la Punta Seca y el cabo de San
  Román (t. II, libro XXI, p.131). Dos apariciones en 544 páginas, las dos en el
  mismo pasaje.
- **`Miraca`**, el primer pueblo de Paraguaná a trece leguas de Coro (p.296).
- **Las islas ABC con sus nombres**, y el indígena de Curaçao dicho como tal:
  `Boynare`, `Aruba`, «llaman los indios *Corazao*» (pp.131-132, imagen). Y
  **`Quiquibacoa`** = Coquibacoa (pp.132, 296). Ver más abajo: los dos ceros que
  lo tapaban eran míos.
- **La red de intercambio, atestiguada**: los palafitos de la laguna «van é
  vienen á la ribera desta laguna y rescatan é venden aquel pescado que matan,
  por mahiz é por otras cosas, con otras generaçiones de indios *çaquitios* é
  bubures» (p.300, imagen).

## El caso `datihao` — lo que esta minería cambia

El proyecto sostiene desde el arranque que `datihao` está atestiguada **a las dos
orillas**: en San Juan por Oviedo (t. I p.473) y en Venezuela por «el apéndice
del t. IV» vía Jahn 1927 p.213 n.29. De ahí sale `caquetío-atestiguado` en el
lexicón y la referencia de `creencia-001`.

Medido:

| | |
|---|---|
| `datihao`/`dalihao` en el **cuerpo** de los tomos II, III y IV | **0** (siete sondas distintas, con y sin el guion deshecho) |
| En el **tomo I** | **1**: impresa 473, libro XVI cap. V, en boca de **Agüeybana**, en **San Juan** |
| En el **glosario del editor**, t. IV p.598 | «**Datihao**: señor: el que presta su nombre al esclavo. **(Lengua de Venezuela.)**» — verificado en imagen |

La glosa del editor es la paráfrasis exacta del pasaje de San Juan: allí el hombre
se ofrece como **naboría** (siervo) y Agüeybana le responde llamándole «mi
*dalihao* … el que, como yo, se nombra». Señor + esclavo + compartir el nombre:
los tres elementos están en ese pasaje y en ningún otro sitio de la obra.

Y **la bibliografía del propio glosario** (impresa 608) no contiene **ni un solo
vocabulario de Venezuela**: Molina, siete de quechua y aimara, Ruiz de guaraní,
Yangües de cumanagoto, Valdivia y Febres de Chile, Marbán de moxo, Noveda de
tagalo, Pichardo de voces cubanas. El editor no tenía de dónde sacar una voz
venezolana que no estuviera en el texto que editaba.

La hipótesis más económica es que **el editor glosó el pasaje de San Juan y le
puso la etiqueta equivocada**, arrastrado por `Diao` —dos entradas más abajo,
misma inicial, misma glosa 'señor', y ésa **sí** venezolana.

La cadena queda así:

1. Oviedo t. I p.473 — `dalihao`, San Juan, Agüeybana. **Atestiguado.**
2. Amador de los Ríos, t. IV p.598 (1855) — «(Lengua de Venezuela)». **Etiqueta del editor.**
3. Jahn 1927 p.213 n.29 — cita el apéndice como voz caquetía. **Segunda mano.**
4. Oliver 1989 cap. 2 n.42 — duda, y concluye «equally shared». **Lectura.**
5. `creencia-001` y el lexicón — `caquetío-atestiguado`, **sin la reserva**.

Oliver dudaba porque «Oviedo hablaba de los indios de la Provincia de Venezuela
en general». La duda era buena y **el motivo era otro**: Oviedo no habló de los
indios de Venezuela en absoluto — habló de San Juan. El «en general» es del
editor.

⚠️ Esto **no toca** la etimología de Oliver (`/da-/` 1sg + `/-(i)tiao/`), ni su
separación de `diao` y `datihao` en dos lexemas, ni el prefijo `/d-/` como rasgo
del caquetío. Toca **de qué orilla es el testimonio de esa palabra**.

## Qué NO ha dado — los ceros, verificados (regla 6)

| Se buscó | Resultado |
|---|---|
| `caquet` / `caiquet` | **0** en los tres tomos — la obra escribe `çaquitios` |
| `datihao` / `dalihao` en el cuerpo | **0** en los tres tomos |
| `Curiana` | 2 en el t. II (un solo pasaje), **0** en el t. III y el t. IV |
| `Coquibacoa` | **0** en los tres |
| `Manaure`, `Ampíes` | **0** en los tres |
| `Manaure`, `Ampíes`, `Baracoica`, la hija llevada a La Española | **0** en los tres. Los «aciertos» de `Ampíes` son todos `anies` = «antes», mal leídos por el OCR. El libro XXV arranca la historia de la provincia **en 1528**, con los Welser: el período de Ampíes queda fuera de su relato |
| «islas de los Gigantes» (el nombre) | **0**. Los 42 «gigantes» de la obra son los **patagones** del estrecho de Magallanes y los guyrandos del Plata |
| ~~`Curazao`, `Aruba`, `Bonaire`~~ | 🔴 **ESTE CERO ERA MÍO Y ERA FALSO** — ver abajo |
| `Hayti` / `Haiti` | **0** en el t. II y el t. III; en el t. IV, sólo dentro del glosario del editor |
| indios de Venezuela en La Española, o taínos en Tierra Firme | **0**. Lo que cruza el mar en este libro son **españoles** |
| «como en esta isla», «la misma palabra» | **0** — Oviedo nunca empareja una voz venezolana con una antillana |
| **Tomo III entero** | Perú, Nicaragua y Nueva Granada. `Veneçuela` = 1 de paso, `Maracaybo` = 0, `diao` = 0, `borat` = 0. **Descartado para esta pregunta** |

## 🔴 El cero de las islas ABC era mío, y era falso

En la primera pasada di por **0** `curazao`/`curaçao`, `aruba`/`oruba` y
`bonaire`/`buynare`/`boynare` en los tres tomos. **Tercera vez en la misma
sesión que un cero medía mi ortografía y no la de la obra.** Las islas están, y
con sus nombres, en el **tomo II, libro XXI cap. VI, impresas 131-132**:

> «más al Poniente de la isla de las Aves está la isla *Boynare*; más al Poniente
> de la isla Boynare está otra que se llama *Corazante*; más al Poniente de
> Corazante está la isla llamada ***Aruba***.»

El OCR las da `Boijnare`/`Boynarc` y `Aniba`, y por eso ninguna sonda las veía.
`Aruba` está **impresa exactamente como hoy**. Y la frase que más vale:

> «no guardar los nombres primeros es poner confusión en todo. Á la que la carta
> llama *Corazante* **llaman los indios *Corazao***, y el almirante que la
> descubrió la dexó con su nombre: á la quel almirante llamó *Poregari* llaman
> agora *Yaruma* ó de *Orchilla*.» — t. II, impresa **132**, imagen

🟢 Atestación explícita del nombre **indígena** de Curaçao con la fórmula que el
proyecto exige («llaman los indios»), y una **defensa del topónimo indígena
frente al cartográfico** firmada por el cronista. ⚠️ Pero Oviedo **no dice de qué
gente son esos indios**: `atribucion: no-declarada` en cuanto a lengua. Y
`Poregari` es el nombre que puso **Colón**, no un indígena — la frase distingue
tres capas y hay que leerla entera.

Con la misma pasada cayó otro cero falso: **`Coquibacoa` se imprime
`Quiquibacoa`** (pp.132 y 296), con dos localizaciones independientes y una
distancia medida desde el cabo de San Román.

⚠️ **Lo que estas dos páginas NO dan es gente.** El capítulo es una derrota de
costa leída sobre la carta de marear: nombra islas, leguas y cabos, y no dice
una palabra de quién vive en ellas. **Cambia el cero sobre los nombres, no el
cero sobre el contacto.**

---

Y el cero que más pesa: **en 1.880 páginas no hay una sola línea que ponga en
relación a los indios de la costa de Venezuela con los de las Antillas.** La
evidencia del contacto precolombino no va a salir de Oviedo; él es un buen
testigo de dos vocabularios que no se tocan. Lo único que compara son cuerpos
(«de la color y estatura de los destas islas», p.329), plantas (el tabaco,
p.298) y una costumbre — y ésa **la separa**: el endocanibalismo de los huesos lo
tiene por rasgo de **Tierra Firme**, y lo compara con Artemisia y Juan de Mena
en vez de con La Española (pp.297-298).

## 🟢 Y un capítulo que apareció por accidente: los aruacas

**Tomo II, libro XXIV cap. XVII, impresas 266-267** — «De la notiçia que se tiene
de los indios llamados *aruacas* en la Tierra-Firme, y dónde viven». Un pueblo
arahuaco entre el Marañón y Trinidad, con cadena de custodia declarada: dos
vecinos de Margarita que vinieron a Santo Domingo, y un **morisco que vivió doce
años con ellos**, «tomó muy bien la lengua» y volvió en 1544 como general de su
flota.

> «contractan por los ríos arriba muchas leguas y con muchas y diversas nasçiones
> que ellos tienen por amigos, y **en la mar assimesmo contractan en mas de
> tresçientas leguas de costa, con armadas de çinqüenta é sessenta navíos, canoas
> é piraguas**, con quinientos é ochoçientos indios de pelea»

Es un **mecanismo atestiguado** de comercio marítimo arahuaco a gran escala, con
llegada a Margarita y Cubagua. ⚠️ Pero es del **s. XVI** y del **golfo de Paria**:
reglas 3 y 4. No se proyecta ni se traslada al Golfete. Tres voces con glosa:
`abas` (p.267), `pretos ó moavis` (p.266) y el topónimo `Aruacay`, del que el
propio Oviedo duda.

## Qué falta

1. **El libro XIX del tomo I** (Tierra-Firme, impresas 586-618), que T1 dejó sin
   leer y señaló como «el libro con más costa de Venezuela». Si en algún sitio de
   Oviedo está la gente de las islas ABC —o el episodio de Ampíes—, es ahí.
2. **El libro XXIV del tomo II entero** (impresas 213-270): Cubagua, las perlas,
   Paria, el Huyapari. El capítulo de los aruacas salió por accidente; el resto
   del libro no se ha tocado.
2. **El tomo I con imagen íntegra**: `historiageneral00fernguat` en Internet
   Archive, 55 MB. Desbloquea las 47 formas que hoy sólo tiene T1 en OCR.
3. **El resto del glosario del tomo IV**: sólo se vaciaron las doce entradas
   marcadas Venezuela y cinco más que este repo tenía abiertas (`Macana`,
   `Piache`, `Guaxiro`, `Areyto`, `Manato`). Son quince páginas de voces
   americanas glosadas y atribuidas por lengua; para el taíno las hay a puñados.
4. **Los libros XX-XXIV y XXVI-XXVIII del tomo II** (impresas 3-268 y 333-530):
   Cubagua y las perlas están ahí, y no se han leído.
5. **Cruzar el mapa del libro XXV** (25 generaçiones de indios, 26 pueblos, 11
   ríos) contra `3-mundo/etnias.yaml` y `compilar_etnias.py`. ⚠️ Es el mapa
   **colonial** de 1528-1546: regla 3.

## Qué sostenía antes — y qué cambia

| Entrada | Vía | Estado tras esta minería |
|---|---|---|
| `creencia-001` (`boratio`) | Jahn p.213 n.29 + Arcaya | **Fuente primaria localizada**: t. II pp.298-299 (cuerpo) y t. IV p.595 (glosario). La forma es `boratio`, una t. La atribución **caquetía** es del editor: Oviedo dice «los indios de Veneçuela» |
| `creencia-001b` (el díao) | Oviedo t. II p.299 + Arcaya | Página **correcta**. Pero la ecuación **díao = boratio no está en Oviedo**: la pone Arcaya. Hay que partir la referencia |
| `creencia-010` (funeral del cacique) | Oviedo t. II pp.299-300 | Hecho **exacto** y atribuido a los çaquitios — pero la página es la **297** |
| `creencia-010b`, `010c` (funeral del díao) | Oviedo t. II p.300 | **Correctos y verbatim**, `busera` incluida. Falta en el corpus la efigie de palo que arde con el muerto |
| `creencia-004b` (ayuno) | Oviedo t. II p.329 | **Correcto**, y con testigo declarado (el obispo Bastidas). ⚠️ Son **dos ayunos distintos**: el de la p.329 y el que el boratio impone en la p.299 |
| ficha `datihao` | Jahn / apéndice t. IV | 🔴 **El apoyo venezolano es editorial.** Propuesta de degradación en el issue |
| ficha `tara` ('venado') | Jahn, Zavala, Alvarado | 🔴 **Cuarta fuente, primera de primera mano**: `langosta`, con descripción |
| ficha `macato` ('bebida') | Jahn (⚠️ comida vs. bebida) | ✅ **Se cierra**: Oviedo dice «çierto brevaje … muy espesso como maçamorra». Las dos cosas |

⚠️ `sostiene` no se toca a mano; lo mide `medir_sostiene.py`.

## Enlaces

[[oviedo-y-valdes-1851]] · [[jahn-1927]] · [[arcaya-1920]] · [[oliver-1989-cap2]] ·
[[alvarado-1921]] · [[zavala-reyes-2015]] · [[03_creencia_caquetia]]
