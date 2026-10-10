---
tipo: sesion
fecha: 2026-10-09
pueblo: lokono
sesion: 10
quien: 'minero lokono, minería 2 «esferas de las hermanas» (Claude Opus 5.5), rama vault/hermanas-lokono'
plan: 08_creencia_lokono_que-minar
propuesta: 6-fusion/hermanas_lokono_2026-10-09.yaml
minadas: [brett-1868, roth-1915, brett-1880, steward-1948-hsai-4, gumilla-1791, perea-alonso-1942, goeje-1939]
estado: "propuesta sin fusionar — nada al corpus, al lexicón ni a 3-mundo/hermanas/; nada descargado"
descripcion: "Las cinco esferas lokonas desde Brett 1868, Roth 1915 y Brett 1880: matrilinaje con nombre, yerno en casa del suegro, la capitanía colonial, la guerra con los caribes, el piache que sueña el diagnóstico, la fiesta de los látigos, y la Vía A wayuu auditada en todas las esferas."
---

# Las esferas lokonas — sesión 10 (minería 2)

> Fichas: [[brett-1868]] · [[roth-1915]] · [[brett-1880]] · [[steward-1948-hsai-4]] · [[gumilla-1791]] · [[perea-alonso-1942]] · [[goeje-1939]]
> La minería 1 de creencia: [[08_creencia_lokono_que-minar]] (el plan) · [[09_creencia_lokono_mineria]] (la bitácora)
> Los mapas del caquetío que esto toca: [[mapa-familia]] · [[mapa-geografia-politica]] · [[mapa-creencia]] · [[mapa-ecologia]] · [[mapa-transmision]]
> El esquema: `3-mundo/hermanas/README.md` · la esfera: [[esfera-de-interaccion]]

Miguel, 2026-10-09: «tal cual como armamos estas esferas para los caquetíos,
deberíamos hacerlo para cada una de sus hermanas». Esta es la de los lokono,
la hermana lingüística más cercana. La propuesta está en
`6-fusion/hermanas_lokono_2026-10-09.yaml`; las cuentas por esfera, etiqueta
y capa las da `python curiana_sim/compilar_hermanas.py` (no se copian aquí).
La creencia de la minería 1 la migró otra rama
(`hermanas_lokono_creencia-migrada_2026-10-09.yaml`, `lokono-creencia-001…008`);
aquí la creencia empieza en 101 y dice, en `mineria_1`, a qué hecho viejo
corrobora o corrige.

---

## 1. Método

- **Pregunta por tema, no por obra.** La lista de temas del README §4 fue la
  lista de preguntas. Un tema sin dato es un cero, y va a `meta.ceros` con su
  sonda.
- **Texto por página.** Los `.txt` de archive.org no traen el número de
  página; se sacó la capa del PDF página a página con pymupdf, para
  localizar con número de pdf. Toda cita se leyó después en la **imagen**, y
  la página impresa se tomó de la cabecera. El desfase de las tres obras
  nuevas **deriva** con las láminas (Brett de − 24 a − 58, Roth de + 98 a
  + 92); está escrito en cada ficha.
- **La capa engaña donde importa.** Roth: «hurokwa» es *burokwa*, «labui» es
  *babui*, y los números de sección salen corridos (se citan páginas). Brett:
  «Arawcinili» es *Arawânili*; Brett 1880 pierde el «1» de la p. 18.
- **Ortografía antes de contar** (minar-fuente §2): `Arawak`/`Arawâk`,
  `Lokono`, `Yauhahu`/`Yawahu`, `Semecici`/`semecihi`/`semi-cici`/`semi-chichi`,
  `Orehu`/`Oriyu`, `Maquarri`/`Makuari`, `Aruacas`, `Aruacay`. Medido en
  `meta.ortografia_medida`.
- **Sólo cuenta lo lokono.** En Roth, lo marcado «Arawak», «Pomeroon
  Arawaks» o «(A)»; lo de «the Indians» es areal. En Brett, el capítulo de los
  arawak y lo que él da con su nombre; el resto de los caps. IX-X es «the
  Indians».
- **El filtro «específico, no pan-areal»** se aplica declarándolo: cada hecho
  dice en `dominios` si es `especifico-lokono` o `areal-guayana`, y lo areal
  sólo puede ir a `comparanda-esfera`, `no-proyecta` o `lectura`. El campo
  `filtro` dice qué cambiaría sin él.

## 2. Lo más fuerte, por esfera

### Parentesco

1. **El matrilinaje con nombre, de primera mano.** Brett p. 98: las familias
   lokonas (Siwidi, Karuafudi, Onisidi…) «all descend in the female line»,
   nadie se casa con su mismo nombre y sí puede casarse en la familia del
   padre. Es la fuente que **le faltaba a parentesco-023** (hoy «etnografía
   secundaria web») y la primera hermana con página para **parentesco-005**,
   que descansa sólo en el wayuu. Y Brett pone el contraste en el mismo
   libro: la mujer caribe «is always in bondage to her male relations»
   (p. 353).
2. **El yerno vive con el suegro y trabaja para él** (Brett p. 101; Roth
   p. 316, de viejos: el yerno que pasa las pruebas es «one of the legal heirs
   of the house»). Una aldea de tres hermanas con sus maridos (p. 352).
3. **La muerte de la esposa cierra la alianza**: la fiesta del Maquarri la da
   el hermano de la muerta, y tras ella el viudo deja de tener lazo con la
   familia de ella (p. 158).
4. **Las raíces de hermano cambian con el sexo de quien habla**, en dos
   registros independientes: Brett p. 117 y los moravos de 1802 (Perea
   p. 556). Se propone un tema nuevo, `terminologia`.

### Geografía política

1. **Lo que Brett ve es la capitanía colonial**: capitanes nombrados por el
   gobernador, placa de plata y bastón, y «I have no power over my people»
   (pp. 103, 155, 158). No proyecta.
2. **El único dato político de la época del contacto** es de tercera mano: el
   Aruacay del bajo Orinoco, s. XVI, con un jefe principal y nueve subjefes,
   uno por barrio (Kirchhoff en el HSAI 4, p. 487). Ilumina el modelo caquetío
   de diao y apopo sin cambiarle la capa.
3. **La guerra con los caribes como historia oral**: el mando de un solo
   jefe en la emergencia, la casa-fuerte con las flechas de un año, el juicio
   del jefe caribe por «their old men and chief warriors» (pp. 486-493). Gumilla
   lo contradice para el Orinoco: los aruacas «se les han sujetado» a los
   caribes (t. I p. 154).
4. **La justicia es el talión dentro de la familia**: al que mató a su mujer
   lo mata su propio hermano (pp. 104-105). Ninguna compensación.

### Creencia (lo nuevo)

1. **El piache arawak sueña el diagnóstico** (Roth p. 348): tras la vigilia
   de la invocación, en su banco, «will proceed to smoke and dream, and in
   his dream he will discover» quién mandó el mal y cómo curarlo. **Corrige a
   la minería 1**, que había dado la cura lokona por sólo de vigilia: vigilia
   y sueño se suceden.
2. **B4 cerrado**: la tradición de Orehu y Arawânili está en Brett 1868
   pp. 400-402, contada en 1841 por Maraka-kore, «an old semi-cici». Y Brett
   **no** llama al yauhahu «supreme spiritual being»: eso lo puso Brinton.
3. **R2 a medias**: la persona lokona es la sombra, *(h)iyá*, y el muerto
   *(h)iyaloko*, bueno o malo según ayude o dañe (Roth p. 152). De sueño como
   viaje del alma, nada lokono.
4. **R4 negativo**: ningún tratamiento lokono de los huesos. Lo que hay es una
   **fiesta posterior** —el Maquarri meses después, con las imágenes y los
   látigos enterrados—, y en el s. XVI el Aruacay hacía una conmemoración
   después del entierro y un reto de latigazos en la borrachera (HSAI 4
   pp. 488, 490).
5. **Los muertos lokonos van arriba**: con Hubuiri, el señor del cielo
   (Navarrete, s. XVI, por Roth p. 119), o al aire sobre las casas (Roth
   p. 161). Va contra la lectura de creencia-028 (la tierra de los muertos,
   abajo).
6. **El eclipse de luna**: la luna se duerme en el camino del sol; se la
   despierta con tambores y se ayuna toda la noche (Roth p. 257, de primera
   mano). Es la práctica lunar que el puente léxico *kati ~ kathi* no tenía.

### Ecología

Poco y casi todo de otro medio: la seca del Golfete no es la selva del
Pomeroon. Lo que sirve: la expedición de cangrejos al mar en canoa (Brett
p. 88), la etimología —de Brett, dudosa— de *bohío* como *bawhu-yuho* «muchas
casas» (p. 484), y que arawak, warao y caribes le dijeran a Roth que el tabaco
vino de las islas (p. 334). Todo `comparanda-esfera`.

### Transmisión

1. **Partículas según el sexo de quien habla y de quien escucha** (Roth
   p. 307): *tashi/tade/tara*, *babui/dadai/daido*. No es una lengua de mujeres
   como la kalinago: es un puñado de palabras de conversación.
2. **Palabras que no se dicen en la canoa** (Roth p. 252): el piache es
   *katau-chi*, «el que sabe». La mayoría de las vedadas son préstamos del
   español: la práctica, como se ve, es colonial.
3. **Navarrete, s. XVI**: una escuela donde los viejos *Cemetu* cuentan las
   tradiciones y el cielo (Roth p. 345). Tercera mano, pero es el lokono más
   cercano a la época caquetía.
4. **El piache se elige y se aprende**, a veces del abuelo (Roth p. 332), y
   había mujeres piache (p. 334). La madre pone el primer nombre y el piache
   el segundo (p. 305).

## 3. Lo que no salió

Medido con sonda, en `meta.ceros`: **sucesión política** (ningún caso
lokono), **tributo**, **segundo entierro** (ningún hueso), **sueño como viaje
del alma**, **escritura y marca** (los petroglifos son de «former Indian
inhabitants»), **sociedades masculinas**, **caza** (sólo lo general). Y
ningún dato de la luna en Brett 1868 ni de tótem en toda la Guayana (Roth
p. 297).

## 4. Auditoría de la Vía A, en las cinco esferas

La Vía A son los hechos caquetíos `reconstruido` apoyados en el wayuu (y,
en transmisión, los wayuu `atestiguado` que el corpus usa de comparanda).
Veredicto por hecho: el campo `via_a` de cada hecho de la propuesta.

| Hecho caquetío | Qué dice | Lokono | Desde |
|---|---|---|---|
| parentesco-005 | linaje y nombre por la madre | **corrobora** | Brett p. 98 |
| parentesco-008 | exogamia de clan | **corrobora** | Brett p. 98; Roth p. 319 |
| parentesco-006 | el tío materno es la autoridad | matiza | el hermano de la muerta preside su rito (Brett p. 158) |
| parentesco-009 | la viuda pasa al hermano del muerto | matiza | la muerte de la esposa CIERRA la alianza del viudo (p. 158) |
| parentesco-011 | términos distintos para tío materno y paterno | matiza | raíces distintas según el sexo de quien habla (p. 117) |
| creencia-002 | el piache trabaja el sueño | **corrobora en parte** (era «contradice») | Roth p. 348 |
| creencia-003 | parafernalia: tabaco, urari, serpiente | matiza | sonajero, banco, muñeco (Roth pp. 329-331) |
| creencia-005 | soñar es el alma que sale | matiza | el alma lokona es la sombra; sin teoría del sueño |
| creencia-006 | la enfermedad es el alma que se aleja | **contradice** | algo metido en el cuerpo por el yauhahu (Brett pp. 361-365) |
| creencia-007 | males comunes y males del espíritu | **corrobora en parte** (era «no toca») | Brett p. 365; Roth pp. 345-346 |
| creencia-008 | muertos peligrosos | **corrobora en parte** | el muerto bueno o malo (Roth p. 152); «don't trouble me» (p. 155) |
| creencia-009 | tierra de los muertos con nombre | matiza | arriba, sin nombre (Roth pp. 119, 161) |
| creencia-010d | segundo velorio con huesos | matiza | fiesta posterior sin huesos |
| creencia-011 | tabúes de quien toca los huesos | no toca | |
| creencia-012 | huesos → lluvia | no toca | la lluvia lokona se hace con la camudi (Roth p. 267) |
| transmision-017, 030 | la vocación la revela un sueño o los espíritus | **contradice** | el aspirante elige y busca maestro (Brett p. 362) |
| transmision-019 | precio de sangre | **contradice** | talión, sin compensación (Brett p. 104) |
| transmision-034 | el palabrero | matiza | ningún mediador lokono |
| transmision-020, 028 | currículo y encierro puberal | corrobora en parte | Roth pp. 309-316 (areal) |
| transmision-021 | no nombrar al muerto | corrobora en parte | Roth pp. 252, 305 |
| transmision-033 | la mujer chamán | corrobora en parte | mujeres piache (Roth p. 334) |
| transmision-035 | dos maneras de hablar | matiza | partículas por sexo, no dos lenguas |

**En una línea:** en parentesco el lokono **sostiene** la Vía A (matrilinaje
y exogamia con fuente primaria); en creencia la **corrige** en lo que importa
(la causa del mal) y la sostiene en parte en lo demás (el sueño del piache,
los muertos peligrosos); en transmisión **la contradice** en la vocación del
piache y en la justicia. Ojo con una trampa: el muerto ambivalente lokono,
*hiyaloko*, y el wayuu *yoluja* pueden ser la misma palabra areal (Roth la
da en toda la Guayana): ahí el parecido no prueba herencia.

## 5. Decisiones para Miguel

1. **El filtro «específico, no pan-areal».**
   - *Si se adopta* (como está aplicado): lo areal no proyecta. `lok-04` (la
     enfermedad metida por un espíritu) baja de hipotético a lectura; la
     covada, el encierro puberal, la dieta de la parentela, los espíritus del
     agua y el mito de la luna quedan como comparanda para personajes. Lo
     que sube al caquetío es poco y muy propio: matrilinaje con nombre,
     yerno en casa del suegro, eclipse de la luna dormida, partículas por
     sexo, fiesta posterior al entierro.
   - *Si no se adopta*: `lok-04` y la intrusión pasan a `reconstruido`
     (lokono de Brett + taíno de Pané), y los hechos marcados `areal-guayana` suben
     a `hipotetico`. El caquetío ganaría covada, encierro puberal y espíritus
     del agua, que son de toda la Guayana y casi seguro también caribes.
   - *Tercera vía*: adoptarlo, pero aceptar como específico lo que la fuente
     contrasta explícitamente con otro pueblo (Brett, matrilinaje frente a la
     mujer caribe). Es lo que se hizo con `lokono-parentesco-001`.
2. **parentesco-005 y 023.** ¿Se les añade Brett p. 98 como fuente? Con el
   taíno con página (minería taína), la matrilinealidad cumple la regla C sin
   el wayuu.
3. **creencia-028.** La hermana pone a los muertos arriba; el corpus, abajo,
   por una palabra (*waka*). ¿Se anota la tensión en el hecho, o se baja la
   capa?
4. **El tema `terminologia`** para parentesco: adoptarlo o fundirlo en
   `descendencia`.
5. **El Aruacay como lokono.** Es la única ventana al s. XVI (jefe y nueve
   subjefes, entierro en la casa, látigo). La filiación es de Kirchhoff
   («probably Arawakan»). ¿Se acepta como lokono?
6. **Lexicón** (sin tocarlo): la glosa lokona de *uni* es 'lluvia' y 'agua'
   es *uni-abu* (Roth p. 268, Brett p. 415, Perea p. 559), mientras el núcleo
   enseña *uni* 'agua'; *adaiahu* 'governor' roza *díao* con glosa
   coincidente y sin regla; *bana(na)* lokono aparece en 'hoja' y en
   numerales, no como 'cerro' (expediente D9). En `para_el_lexicon`.
7. **Descargas** (lo decide Miguel): Roth 1924 (artes y costumbres, la
   ecología que el 1915 no trata), Goeje 1942 (la iniciación) y Navarrete en
   su edición de 1964.

## Qué no se hizo

No se tocó `3-mundo/`, `2-lengua/`, el lexicón ni ningún índice. No se
descargó nada. No se migró la minería 1 (es de otra rama). No se leyeron
enteros Brett 1868 ni Roth 1915: lo no leído está en `meta.no_leido`.
