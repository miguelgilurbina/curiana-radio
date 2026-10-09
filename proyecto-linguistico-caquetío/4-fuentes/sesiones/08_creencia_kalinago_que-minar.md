---
tipo: decision-mineria
pregunta: "¿Qué minar de la cosmovisión kalinago para el ensayo «¿En qué creía el caquetío?», y cómo separar lo que viene del sustrato arahuaco (comparable) de lo caribe (no comparable)?"
pueblo: kalinago
fecha: 2026-10-08
moc: mapa-creencia
ensayo: 03_creencia_caquetia
corpus: [creencia.yaml]
estado: "propuesta: no se ha minado ni descargado nada; las páginas son pistas de la capa de texto, sin ver en imagen"
---

# Creencia kalinago: qué minar, y con qué tamiz

> [[mapa-creencia]] · [[03_creencia_caquetia|ensayo 03]] · [[03_creencia|hoja de fuentes de la sesión 3]] · [[INDICE_FUENTES]]
> Toca: [[breton-1665]] · [[adam-1879]] · [[goeje-1939]] · [[steward-1948-hsai-4]] · [[pane-c1498]] · [[las-casas-apologetica]] · [[oviedo-y-valdes-1852-1855]] · [[arcaya-1920]]

**En corto.** El ensayo 03 reconstruye la creencia caquetía desde el wayuu
(Vía A) y desde María Lionza (Vía B). Lo kalinago puede dar una vía más
sólida, porque el habla de mujeres ya cuenta como hermana arahuaca (D1). Pero
sólo sirve si cada hecho pasa un tamiz que separe la capa arahuaca de la
caribe **dentro del mismo pueblo**. Lo primero que hay que minar ya está en el
repo: Breton 1665-1666 en imagen, con Goeje 1939 pp. 37-39 como tamiz y Rouse
1948 como índice. Después, si Miguel autoriza la descarga, Rochefort 1658 y Du
Tertre 1667 t. II.

Esta nota **propone qué minar**. No decide ninguna capa ni toca el canon
(regla 5). Lo que necesita de Miguel está en §4.4, y se publica como issue
`decision` cuando arranque la campaña (regla 10).

---

## 1. Lo que el vault ya tiene

### 1.1 Breton 1665-1667 ([[breton-1665]])

- **Local.** Los tres PDF están en OneDrive, fuera de git (D8), bajados con
  permiso de Miguel el 2026-09-23. El OCR `.djvu.txt` está en git y es malo:
  s larga, ligaduras, dos columnas mezcladas y la cursiva caribe rota.
  Desfases medidos en la ficha: 1665, impresa = pdf − 22; 1666, impresa =
  pdf − 8.
- **Minado una sola vez, y por el MAR.** La campaña de la cosmovisión marina
  (2026-09-24) lo leyó para el mar: `6-fusion/cosmovision_marina_2026-09-24.yaml`
  §comparanda.kalinago, cm24-c-k01…k08. Los ~400 pares h/f del tomo de 1666
  no se han leído enteros, porque la tanda de las hermanas usó a Goeje.
- **Lo que esa campaña dejó, de paso, que toca la creencia.** `zemi` se
  escribe `chemijn` en Breton (falso cero resuelto). El `oumêcou` es un
  espíritu maligno «sin lugar» (1665 p. 424). Los kalinago «n'ont point de
  connoissance de la création» (p. 424). Las ofrendas del boyé se hacen en la
  casa y de noche. El tabú del manatí no es «par motif de religion (au reserve
  des boyez)» (p. 275). Y las cabezas de los enemigos se guardaban en las
  cuevas de la orilla (pp. 229-230). **Nada de eso está en `creencia.yaml`.**
- **¿Tiene entradas de creencia? Sí, y largas.** Se midió hoy pasando
  `pdftotext` página a página por los PDF de OneDrive (en el scratchpad, nada
  en el repo) y buscando las grafías de Breton. Son **pistas de la capa de
  texto, sin ver en imagen**. La página impresa sale del desfase de la ficha
  y se confirma al leer.

| Lo que se busca | 1665 caraïbe-français (impresa) | 1666 français-caraïbe (impresa) |
|---|---|---|
| `chemijn` «Dieu, mon Dieu», y el plural `cheméignum` | p. 135 | p. 312 (en una entrada por identificar) |
| `icheiri` y la entrada **Ichéiricou**: entre Chemijn y Mapoya hay tanta diferencia «comme parmy nous entre Dieu & diable»; es «inoüy» que se ofrezcan sacrificios a mapoya; no se dice «el dios de los salvajes» sino «le Dieu d'un tel boyé»; si el espíritu es hombre es dios, si es mujer, diosa; no tienen nombre para la oración, pero no hay fiesta de bebida sin ofrenda | pp. 130, 283-284 | p. 216 (`licheiri`) |
| `mapoya`: un tabú de comida («ne sont pas mangées parce qu'ils disent que le mapoya»), el mal que da el mapoya, el eclipse | pp. 8, 21, 56, 271, 342, 370 | p. 221 |
| `oupoyem`/`opoyem` «esprit»; `mapoya` «esprit malin»; temen a los mapoyas y a los oumêcou; y Breton cuenta que usó `mapoya` para explicarles qué es el Diablo | p. 424 | — |
| `ioüanni` «cœur, âme, vie, courage» | p. 307 (y pp. 82, 122, 353) | p. 17 (Ame); p. 284, entrada *penser*: «pioüanni, f. banichi» |
| `anichi` «cœur, âme», la forma de mujeres | pp. 40-41 | p. 284 |
| `akali` «âme, forme, figure» | p. 9 | — |
| la inmortalidad del alma | p. 237 | — |
| `boyé`, `boyâicou`; «femme qui estoit boyée»; los viejos de los boyés | pp. 83, 216-217, 283-286, 300, 341 | pp. 52, 241, 313 |
| entierro | pp. 165, 227, 343 | p. 144 (con forma f.) |

Lo más valioso que asoma son dos cosas:

1. **Una sesión de boyé contada por Breton en primera persona** (1665
   p. 217, paráfrasis). Hay dos boyés y un canto. Se echa humo de tabaco
   hacia arriba «en lugar de incienso». El espíritu baja y cae «como un saco
   de harina». El boyé le ofrece asiento y comida y bebida. Se hace siempre
   de noche y con el fuego apagado. Breton quiso entrar una vez con un tizón
   para impedirlo, y **las mujeres no lo dejaron**.
2. **La frase de método que hay que tener delante todo el tiempo** (p. 424):
   para explicar el Diablo, Breton usó `mapoya`. La pareja chemijn = Dios /
   mapoya = diablo es, al menos en parte, del misionero, y él mismo la plantea
   así en la entrada Ichéiricou.

### 1.2 Adam 1879 y Goeje 1939

- **[[adam-1879]]** está minado y hecho. Para la creencia da una sola línea,
  ya vista en imagen por la campaña del mar. Es la p. 303: «Démon (bon),
  chemes, zemi. — F. chemiin». Es decir, **el espíritu bueno lleva la forma de
  mujeres, y es la del cemí taíno**. Adam lee a Breton, así que no es un
  testigo aparte. Lo demás de Adam es lengua y transmisión: la negación de
  mujeres `ma-` (p. 277) y la crianza a cargo de las mujeres (p. 301, de donde
  sale `transmision-035`).
- **[[goeje-1939]]** tiene una sección «II a. — Religion, magie, etc.» del
  caribe insular en las **pp. 37-39** (pdf 38-40). En el margen pone la sigla
  de origen de cada voz. La ficha la da como «sin transcribir» (pp. 35-43),
  salvo las formas f. (2026-09-24) y el `Umeku` de la p. 38. **Es justo el
  tamiz que pide este encargo, ya hecho por un especialista.**

  Se leyó hoy en la capa de texto. Antes de citar, las formas en cursiva y la
  columna de siglas se miran en imagen: la ficha avisa de que el OCR las
  rompe. Goeje tiene copyright, así que sólo cita corta.

| Concepto | Hombres (h.) | Mujeres (f.) | Origen que da Goeje | Lo que pone al lado |
|---|---|---|---|---|
| hombre-medicina | `boye`, `boyei`, `boyahi-ku` | — | kalina `puye`, tupí `paje` | (su lista taína: `behiko`, `buhuitihu`, p. 7) |
| dios, genio tutelar | `išeiri` | forma del tipo `seme`/`chemijn` (a verificar en imagen; Adam p. 303: F. `chemiin`) | — | lokono `seme-he`; taíno `semi` |
| espíritu | `akambue` | — | kalina `aka` | — |
| espíritu o alma del muerto | — | `opoyem`, `upoyem` | — | taíno `hupia` |
| «diable» | `mapoya` (garífuna `mafuiya`…) | — | «ma-poya (sans-esprit?)», con interrogación | — |
| alma, corazón, valor | `iuani` | `anisi` | kalina `yevan` | — |
| primer hombre, semidiós | `lukuo` | — | sigla «A?» | lokono `loko` 'hombre', `(h)ialoko` 'espíritu' |
| espíritu que hunde canoas | `Umeku`, `Umoku` | — | «K?» | kalina `Semuye` (Penard) |

### 1.3 Rouse 1948, «The Carib», en HSAI 4 ([[steward-1948-hsai-4]])

Está en el repo, es de dominio público y su capa de texto es buena. La ficha
dice que a Rouse sólo se lo sondeó buscando caquetíos (con resultado
negativo): **el capítulo caribe no se ha leído**. Es una síntesis de tercera
mano (Du Tertre, La Borde, Rochefort, Labat, Breton), pero ordenada por temas
y con notas que dicen de dónde sale cada cosa. Lo que trae, leído hoy en la
capa de texto (las páginas son aproximadas, porque el desfase deriva: ver la
ficha):

- **p. 545, «The ethnography of the Lesser Antilles».** Los igneri, los
  arahuacos de las islas antes del caribe: ídolos de algodón en cuevas,
  petroglifos y entierro «either primary or secondary».
- **pp. 558-559, la muerte.**
  - No se nombra a los muertos, y se examina el cuerpo por si hubo brujería.
  - El muerto va sentado, en una hamaca nueva, en una fosa dentro del carbet.
  - La fosa se deja abierta diez días, con comida y llanto, y con fuego
    alrededor.
  - Los enseres van al fuego o a la fosa, y a veces se quema la casa.
  - El jefe dice una oración fúnebre con las hazañas del guerrero, y más
    tarde hay un segundo festín sobre la tumba.
  - Y una frase sin nota de fuente: «in the case of a chief the Carib
    sometimes burned the corpse and mixed its ashes into a drink».
- **p. 560.** Imágenes de `maboya` talladas, como amuleto y en la popa de las
  piraguas.
- **pp. 561-563, «Religion and shamanism».**
  - **Las almas.** Hay varias, ligadas al latido del corazón y de las
    arterias. La del corazón sube a un paraíso con los espíritus buenos
    (`akamboue`). Las demás se quedan en los huesos o se van al monte y a la
    orilla, y son `maboya`; las del mar se llaman `omicou`.
  - **El espíritu personal.** Cada uno tiene el suyo (`ichieri`). Se le
    pone ofrenda de casabe y primicias en una mesa, sin ídolo.
  - **Los `maboya`.** Causan pesadillas, enfermedad, naufragio, trueno,
    huracán, terremoto y eclipse.
  - **Los boyez.** Se aprende con un boyé mayor, con cinco meses de ayuno
    (Du Tertre t. II pp. 365-366; La Borde lo cuenta distinto). Las sesiones
    son de noche y a oscuras, y el espíritu habla a veces por boca de una
    anciana.
  - **Los huesos.** **Algunos boyés guardaban en casa el pelo o los huesos
    de sus antepasados, en calabazas o envueltos en algodón, y por ellos
    hablaba el espíritu.**
  - **Brujería y cura.** Las acusaciones de brujería caen sobre mujeres; se
    cura chupando.
- **El resumen del editor, pp. 25-26:** «A reflection of Arawakan religion is
  seen in offerings made to guardian spirits, which were not, however,
  represented by idols». Es la hipótesis de 1948 sobre qué es arahuaco en la
  religión caribe. Sirve para ponerla a prueba, no como dato.

### 1.4 La hermana taína ya está en casa

Para la prueba de dos hermanas (§2.1) no hace falta bajar nada del lado
taíno:

- **[[pane-c1498]].** Cap. XIII: el alma del vivo es `goeiz` y la del muerto
  `opia`; los muertos salen de noche, no tienen ombligo y comen guabaza. Cap.
  XII: Coaibai, la casa de los muertos. Caps. XIV-XX: el behique y los
  cemíes.
- **Rouse 1948, «The Arawak», p. 532** (síntesis; sus primarias son Oviedo,
  Las Casas y Pané). El cacique muerto se abría y **se secaba al fuego para
  guardarlo como cemí**, y las cabezas se guardaban en cestas en casa de los
  hijos. Es el paralelo más cercano del díao caquetío, desecado sobre brasas y
  guardado en su casa (Oviedo t. II p. 300, `creencia-010b`). Ojo con §3.1:
  Oviedo es testigo de las dos orillas.
- **[[las-casas-apologetica]]**, ya minada para el taíno (cemí, behique,
  hupía).

### 1.5 Corpus y lexicón

- **`3-mundo/corpus/creencia.yaml` no tiene ninguna entrada kalinago ni
  caribe** (grep de hoy; el único «adam» que sale es «atestiguadamente»). El
  ensayo 03 nombra a los caribes insulares una sola vez: el segundo entierro
  «entre los Motilones y los caribes insulares», vía Jahn 1927 p. 111.
- **Lo kalinago del corpus está en otras esferas**, y marcado como hecho
  KALINAGO, no caquetío: `transmision-035` (el doble registro y la crianza
  por las madres) y `parentesco-028`/`-032` (el relato de la conquista, hoy
  discutido, y el habla de hombres como posible pidgin).
- **El lexicón tiene tres deudas** que la campaña tendría que levantar como
  issue. No se tocan aquí.
  - `maboya` (`kalinago`, esfera de contacto) dice «equivalente al buio en
    cosmología caquetía» **sin fuente**. Su procedencia es
    «ii-solo-secundaria» (Coll y Toste, Bachiller), y la primaria que le
    falta es Breton.
  - `bejique` dice «cognado de piache (Lokono piaye)». Pero Goeje emparenta
    el `boyé` con el kalina `puye` y el tupí `paje`, y el proyecto ya sacó
    `piache` del habla por ser voz cháima-tamanaca (D10).
  - `cemi` (taíno) anota que Bachiller y Goeje lo dan también en eyeri, el
    habla de mujeres.
- **Agentes.** Marokoto-ni, «el Caribe» del elenco de la era 1.

### 1.6 Lo decidido sobre hombres y mujeres, y por qué es el matiz central

- **D1 (tanda de las hermanas, aplicada el 2026-09-24).** El habla de mujeres
  kalinago cuenta como cuarta hermana arahuaca. Donde el kalinago tiene dos
  palabras, el caquetío va con la de mujeres (sol, luna, mar, diente, hombre,
  mujer, piedra); lo caribe sale en la fauna y en las cosas de la esfera. Está
  en `6-fusion/kalinago_mujeres_2026-09-23.yaml`,
  `kalinago_mujeres_goeje_2026-09-24.yaml` y
  `decisiones_tanda_hermanas_2026-09-24.yaml`. El núcleo se rehízo desde el
  lokono y el habla de mujeres: con dos hermanas, la voz es reconstruida; con
  una, hipotética.
- **`transmision-035`.** El doble registro es un hecho kalinago y no se
  proyecta a las caquetías.
- **`parentesco-032` y la ficha de Adam.** El relato de la conquista (matar a
  los hombres arahuacos y tomar a las mujeres) es de los informantes de Breton
  y está discutido.

Lo que esto obliga para la creencia, y no estaba dicho:

1. **El par h/f es un par de PALABRAS, no de creencias.** En el s. XVII
   hombres y mujeres kalinago vivían la misma religión. Que el espíritu bueno
   tenga nombre de mujeres (`chemiin`) y nombre de hombres (`icheiri`) dice
   que el concepto tiene una capa arahuaca en la lengua. No dice que las
   mujeres creyeran otra cosa. Un nombre arahuaco es una **pista** para buscar
   la creencia en una hermana; no la prueba.
2. **Y al revés.** Que el chamán se llame con voz caribe-tupí (`boyé`) no
   vuelve caribe a la institución: el chamanismo con tabaco y ayuno es
   panamericano. Lo que decide si un rasgo es comparable es su **contenido**
   repetido en otra hermana arahuaca, no la etiqueta de su nombre.
3. **El vocabulario religioso pasó por el misionero.** `chemijn` traduce
   «Dieu» y `mapoya` «diable» porque Breton los usó así para catequizar
   (§1.1). La capa colonial está dentro de las glosas, no sólo en la fecha.

---

## 2. Qué pregunta responde lo kalinago

### 2.1 El tamiz: arahuaco comparable, caribe no comparable

Es la regla del lexicón aplicada a hechos culturales: dos hermanas =
reconstruido, una = hipotético. Encima van «la atestiguada manda» y la regla
3. Cada hecho kalinago pasa estos pasos, en orden:

| Paso | Pregunta | Si sí | Si no |
|---|---|---|---|
| 0 | ¿El caquetío ya lo tiene atestiguado (Oviedo, Arcaya)? | El kalinago es **corroboración**, como el wayuu en `creencia-010d`. La entrada caquetía no cambia de capa | sigue |
| 1 | ¿Breton lo vio, lo oyó contar, o sólo lo dice una fuente posterior que lo copia (§3.1)? | se anota en el hecho | — |
| 2 | El nombre: ¿forma de mujeres (f.) o sigla A/am en Goeje? ¿O de hombres con sigla K/Tu? | pista arahuaca o pista caribe | sin pista: el nombre no decide |
| 3 | El contenido: ¿está el mismo rasgo en OTRA hermana arahuaca, con fuente propia? (taíno: Pané, Oviedo, Las Casas; lokono: Brett vía Brinton; achagua: Neira y Ribero, Gilij) | **dos hermanas → `reconstruido`** para el caquetío, con las dos comparandas citadas | **una hermana → `hipotetico`**, y el perfil era2 no la enseña |
| 4 | ¿Está en los caribes de tierra firme (kalina, cumanagoto, cháima, tamanaco) y en ninguna hermana arahuaca? | **caribe: no se proyecta.** Va a `6-fusion/` §comparanda como esfera de contacto (le sirve a un personaje caribe como Marokoto-ni), nunca al caquetío | — |
| 5 | ¿Sale sólo de la tradición garífuna o dominiquesa del s. XX? | `retro-abstraido`, como María Lionza: NUNCA sube a `reconstruido` | — |

Y tres cerrojos más:

- **Precontacto ≠ colonial (regla 3).** Todo lo kalinago escrito es de entre
  1619 y 1705, de las Antillas Menores, 130 a 200 años después del contacto.
  Que la capa arahuaca de los kalinago sea anterior a 1492 es una hipótesis:
  la misma que sostiene D1 en el léxico. Proyectar un hecho cultural kalinago
  al caquetío del s. XIV-XV pide decidirlo explícitamente (K4, §4.4), como el
  canon decidió proyectar el poder de Manaure sobre las tormentas.
- **Regla 4.** Los kalinago no son una polity caquetía ni un vecino de la
  Kaketiana: son esfera de contacto. Entran como comparanda de hermana, nunca
  como «lo que se hacía en la costa».
- **D11, mirando hacia atrás.** Desde D11 el wayuu es vecino, no hermana por
  defecto. Pero la Vía A del ensayo etiqueta `reconstruido` analogías que
  descansan sólo en el wayuu: `creencia-002`, `-005` a `-009`, `-011` y
  `-012`. Si el kalinago y el taíno sostienen la misma estructura, esas
  entradas ganan dos hermanas. Si no, se quedan con un solo apoyo, que ya no
  cuenta como hermana. No se decide aquí: es la pregunta que la minería deja
  medida.

### 2.2 Las preguntas, una por hueco del ensayo

| # | Pregunta para el ensayo 03 | Lo kalinago, con su registro | La otra hermana | Lo caquetío | Capa que podría dar |
|---|---|---|---|---|---|
| P1 | El «espíritu que ven los boratios» (Oviedo t. II p. 298, `creencia-025`): ¿es un espíritu tutelar propio, como el cemí? | `chemijn`/`chemiin` (f.) ~ `icheiri` (h.): espíritu personal, uno por persona, con ofrenda de casabe y primicias, sin ídolo; «el dios de tal boyé» (1665 pp. 135, 283-284; Rouse p. 562) | taíno `cemí` (Pané, Oviedo); lokono `seme-he` (Goeje p. 38) | el boratio ve al espíritu y le habla, y lo pinta en sus joyas y en madera (Oviedo t. II p. 298) | `reconstruido` si el contenido (espíritu propio y ofrenda de comida) casa en dos hermanas. El nombre NO se caquetiza |
| P2 | ¿Tienen nombres distintos el alma del vivo y el espíritu del muerto? | f. `anichi` 'corazón, alma' (h. `ioüanni`) frente a f. `opoyem` 'espíritu' (1665 pp. 40-41, 307, 424; 1666 p. 284) | taíno `goeiz` / `opia` (Pané XIII); Goeje pone `opoyem` junto a `hupia` (p. 38) | una sola voz atestiguada, `barsure` 'alma'; el muerto que ronda no tiene nombre (hueco léxico) | la estructura, `reconstruido` con dos hermanas. `opoyem ~ opia` va además a cognados como candidato, con la regla de minar-fuente §2: forma Y glosa |
| P3 | ¿Hay varias almas, con destinos distintos? | almas del corazón y de las arterias; la del corazón sube con los `akamboue` (h.); las otras se quedan en los huesos, el monte y la orilla como `maboya` (Rouse pp. 561-562, que lo toma de Rochefort y Du Tertre) | no consta: Pané da un alma del vivo, no varias; el wayuu da cuerpo, huesos y aa'in, pero cae bajo D11 | el alma «ronda la sepultura o la choza, o recorre el bosque y la sabana» (Arcaya pp. 104-108, `creencia-008b`) | probablemente `hipotetico` (sólo kalinago), salvo que aparezca en otra hermana. Los destinos «monte y orilla» corroboran `008b` |
| P4 | ¿Qué es el `maboya`, y es arahuaco? | `mapoya` 'esprit malin' (1665 pp. 21, 271, 342, 370, 424): tabú de comida, enfermedad, eclipse; amuletos tallados (Rouse p. 560). Goeje: «ma-poya (sans-esprit?)», con interrogación | la conjetura de Goeje sería arahuaca si `ma-` es el privativo de mujeres (Adam p. 277) y `-poya` es el `opoyem`/`opía`. **Es una hipótesis a probar, no un dato** | muertos temidos que obedecen los conjuros del hechicero (`008b`); el lexicón iguala `maboya` a `buio` sin fuente | aclara el nombre del lexicón; para el caquetío, a lo sumo corroboración de `008b` |
| P5 | ¿Cómo se hace un boratio, y cómo trabaja? | el boyé aprende con un boyé mayor, con ayuno largo y tabaco; la sesión es de noche y a oscuras; el espíritu baja, come y habla, a veces por boca de una anciana; **también hubo mujeres boyé** (1665 pp. 216-217; Rouse pp. 562-563) | el behique taíno: ayuno, vómito, cohoba, y el cemí que habla (Pané XIV-XX) | piache por ayuno prolongado y pelo largo (Arcaya p. 101, que habla de Nueva Segovia: regla 4); adivinación con tabaco (Oviedo t. II p. 298) | el NOMBRE `boyé` es caribe-tupí (Goeje p. 37) y no se proyecta; el contenido que comparte con el behique, `reconstruido` |
| P6 | Los huesos de los mayores como poder | boyés que guardan el pelo y los huesos de sus antepasados en calabazas, y por ellos habla el espíritu (Rouse pp. 562-563) | el cacique taíno desecado al fuego y guardado como cemí; las cabezas en cestas (Rouse p. 532) | el díao desecado sobre brasas y guardado años en su casa (Oviedo t. II p. 300, `010b`) | ya está atestiguado. El kalinago y el taíno corroboran, y lo que aportan es el **porqué** (el muerto guardado es un espíritu que habla), que hoy lo da sólo el wayuu |
| P7 | Beber al muerto: ¿es arahuaco o es otra cosa? | «a veces quemaban el cuerpo del jefe y mezclaban sus cenizas en una bebida» (Rouse p. 559, sin fuente) | en el taíno no consta; el HSAI 4 lo llama «rasgo amazónico» al hablar de otros pueblos | beber los huesos molidos en maçato, atestiguado (`010`, `010c`, `023`) | sólo corroboración. **Hay que saber de qué primaria sale y si es caribe o arahuaca**: si es caribe, NO cuenta como sustrato |
| P8 | El funeral: el llanto, la casa, el nombre, el segundo tiempo | fosa abierta diez días con comida; casa quemada o abandonada; no se nombra al muerto; el jefe dice sus hazañas; segundo festín sobre la tumba (Rouse pp. 558-559; Breton 1665 pp. 165, 227, 343; 1666 p. 144, con forma f.) | taíno: la casa se quema con el muerto dentro (Rouse p. 532); igneri: entierro primario o secundario (p. 545) | canto de hazañas de noche (`010`); casa del díao que nadie vuelve a habitar (`010b`) | corrobora lo atestiguado. «No nombrar al muerto» hoy sólo lo da el wayuu: con kalinago y taíno, se puede medir |
| P9 | ¿Hay mito de origen? `Louquo` | el primer hombre, un semidiós. Goeje (p. 39) pone `lukuo` junto al lokono `loko` 'hombre' y `hialoko` 'espíritu', con sigla «A?» | el lokono, por el nombre | ninguno atestiguado; el ensayo no tiene mito de origen | sólo si aparece con contenido en otra hermana: el nombre es pista. **En Breton, `Lúcuo` sale 0** (campaña del mar): está en Rochefort, Du Tertre o La Borde |
| P10 | El cielo y el miedo | el eclipse es el mapoya que se come la luna, y se baila toda la noche; hay constelaciones que traen huracán (ya en `cm24-c-k02`) | taíno: el sol y la luna salen de una cueva (Pané) | el díao «da los temporales» (`013`) | comparanda; el caquetío no tiene dato |

### 2.3 Lo que lo kalinago NO responde

- **La forma caquetía de nada.** Ningún hecho kalinago da una palabra
  caquetía. Según la decisión 5 del ensayo, los nombres de la hermana se
  citan, no se caquetizan; si un piache acuña la forma en un run, eso es el
  dato.
- **La religión de la costa caquetía en concreto (regla 4).** Da comparanda
  de hermana, no testimonio de la Kaketiana.
- **El mar como lugar sagrado.** La campaña del 2026-09-24 ya midió que en
  Breton no hay dueño del mar.

---

## 3. Candidatas a minar

Comprobado hoy, 2026-10-08:

- «En el repo» quiere decir: el PDF en OneDrive y el texto en git, sin bajar
  nada.
- «HTTP 200» quiere decir que la URL responde. **No se bajó nada.**
- Bajar es decisión de Miguel (leer-fuente §6).

| Obra | Qué aporta | Dónde | Formato y tamaño | Esfuerzo | Lengua | Capa al proyectar |
|---|---|---|---|---|---|---|
| **Breton 1665**, *Dictionaire caraibe-françois* | P1-P10: las entradas de §1.1, la sesión de boyé vista por él, las formas f. | **en el repo** (OneDrive); archive.org `dictionairecarai00bret` (JCB) | PDF 63,5 MB; OCR malo; desfase −22 | medio: ~20-25 pp. en imagen (estimado) | francés del s. XVII: hay que leerlo **en imagen** (s larga, ligaduras, u/v, cursiva para el caribe) | comparanda kalinago, `atestiguado` para los kalinago de 1635-1654; al caquetío, sólo por el tamiz de §2.1 |
| **Breton 1666**, *Dictionaire françois-caraibe* | el registro h/f de cada concepto religioso (Ame, Boyé, Diable, Dieu, Esprit, Mort, Penser…) | **en el repo** (OneDrive); archive.org `dictionairefranc00bret` | PDF 54,4 MB; desfase −8 | bajo-medio: ~10-15 entradas | ídem | ídem |
| Breton 1665, **edición crítica de 1999** (Besada Paisa dir., con Bernabé, de Pury, Relouzat, Renault-Lescure, Thouvenot y Troiani; Karthala-IRD, 419 pp.) | lente de lectura: el prólogo dice que modernizaron el francés y añadieron explicaciones | IRD Horizon, `horizon.documentation.ird.fr/exl-doc/pleins_textes/pleins_textes_7/b_fdi_03_02/010017260.pdf`, HTTP 200. El catálogo la marca a la vez «open access» y «réservé», pero el enlace directo responde | PDF 32 MB; sin abrir: no se sabe si tiene capa de texto ni si conserva la paginación de 1665, que es la que se cita | bajo, si tiene texto | francés moderno | ninguna propia: **se cita a Breton 1665 en imagen**. La edición tiene copyright (cita corta) |
| Breton, *Relations de l'île de la Guadeloupe* (1647; textos de 1654 y 1656) | narración de misión: la religión en contexto | edición de la Société d'Histoire de la Guadeloupe, 1978: **no se localizó copia libre**. Traducción inglesa (Turner, 1958) en eHRAF «Kalinago», de suscripción. Manioc tiene a Rennard 1929, *Les Caraïbes, la Guadeloupe 1635-1656*, que se basa en ellas (PAP11003, 90 MB según el buscador; sin abrir) | — | alto | francés del s. XVII | como Breton; Rennard es paráfrasis de segunda mano |
| **Rochefort 1658**, *Histoire naturelle et morale des iles Antilles*, libro II | Louquo y el origen (P9), las almas (P3), el funeral y las cenizas (P7-P8), boyés y maboya en prosa | archive.org `histoirenaturell02roch` (JCB, 1658, libre); otras copias: `histoirenaturell00roch_0`, `ayer_1000_.r6_1658`. **Davies 1666** en inglés: archive.org `historyofcaribb00roch` y **EEBO-TCP A57484**, transcripción limpia CC0, en GitHub `textcreationpartnership/A57484` | 1658: 566 imágenes, PDF 69,5 MB, OCR 1,2 MB; parte moral pp. 263-514, vocabulario pp. 515-527. TCP: XML de 1,24 MB | medio: el TCP localiza y la imagen de 1658 cita | francés del s. XVII (imagen); inglés de 1666 (TCP) | igual que Breton, **pero dependiente** (§3.1). Davies añade y quita material respecto del francés (aviso del JCB): se localiza en Davies, se cita del francés |
| **Du Tertre 1667-1671**, *Histoire générale des Antilles*, t. II | la iniciación del boyé (pp. 365-366, la cita de Rouse; P5), el funeral, los huesos guardados | archive.org `b33275944_0002` (Wellcome, «Vol. 2» declarado). Las seis copias JCB, `histoiregenerale00dute_0` a `_5`, no dicen qué tomo es cada una: hay que mirarlo. La versión de 1654 está en `cihm_34860`. Gallica, según la bibliografía de Kullberg (URL sin comprobar) | Wellcome: 610 imágenes, PDF 236 MB, OCR 1,1 MB; JCB: PDF de ~35 a 63 MB | medio-alto: identificar el tomo y medir el desfase | francés del s. XVII (imagen) | igual que Breton, **dependiente** (Du Tertre fue compañero de misión de Breton) |
| Labat 1722, *Nouveau voyage aux isles de l'Amérique* | Dominica hacia 1700: costumbres, poca religión | archive.org `nouveauvoyageaux02laba_0` (1722, t. II, Getty, libre); hay ediciones de 1724 y 1742 | PDF 45,5 MB, 656 imágenes | alto para lo que rinde | francés de 1722 | kalinago tardío, unos 200 años después del contacto; el único testigo fuera del grupo de Breton, y sesgado |
| Taylor 1951, *The Black Carib of British Honduras* | garífuna del s. XX: dügü (rito de los ancestros), gubida, buyei (← boyé) | archive.org `bwb_P9-CJE-197`, **préstamo controlado** (restricted); en copyright | 196 imágenes | alto (préstamo) | inglés | tradición viva posterior, con capa africana: **`retro-abstraido`**, nunca `reconstruido` |
| Taylor 1938, «The Caribs of Dominica» (BAE Bull. 119, pp. 103-159) | Dominica moderna, leyendas | Smithsonian repository (sin copyright en EE. UU.); el PDF devolvió **403 a curl**: hay que abrirlo en el navegador | ~3,7 MB, según el buscador | bajo | inglés | `retro-abstraido` |
| Taylor y Hoff 1980 (IJAL 46(4), el habla de hombres como pidgin caribe); Taylor 1977, *Languages of the West Indies* | lengua, no creencia: el matiz h/f | JSTOR / compra; no comprobado | — | — | inglés | apoyo de método para §1.6, no hechos |
| Hulme y Whitehead 1992, *Wild Majesty* | antología en inglés, con traducciones nuevas de textos raros; índice sin verificar | archive.org `wildmajestyencou0000unse`, **préstamo controlado**; Clarendon/OUP, en copyright | 394 imágenes | medio (préstamo) | inglés | ninguna propia: es **un mapa, no un testigo**. Hereda la capa del texto que traduzca |
| *(ya en el repo)* **Goeje 1939**, pp. 37-39 | el tamiz h/f y las siglas de origen (§1.2) | en git | capa de texto; la cursiva, en imagen | bajo: 3 pp. | francés de 1939 | instrumento, no testigo; copyright (cita corta) |
| *(ya en el repo)* **Rouse 1948**, HSAI 4, pp. 545-565 (y Steward pp. 24-26) | el índice de temas con sus fuentes (§1.3) | en git | capa de texto buena | bajo | inglés | instrumento de tercera mano: un `reconstruido` nunca se apoya sólo en él |

**Fuera de la lista, para anotar:**

- **La Borde 1674**, *Relation de l'origine, mœurs, coustumes, religion…
  des Caraïbes*, en el *Recueil de divers voyages*: archive.org
  `recueildediversv00unkn`, y hay otras copias. Es la teogonía (Louquo y los
  demás) que Antolínez cita de tercera mano. Es jesuita, y en parte
  independiente del grupo Breton-Du Tertre-Rochefort.
- **El Anónimo de Carpentras** (1618-1620; edición de Moreau, 1987): el
  testimonio más temprano y el más independiente de Breton. Tiene copyright y
  no hay copia libre.

### 3.1 Independencia (minar-fuente §8)

**Breton, Du Tertre y Rochefort no son tres testigos.** Du Tertre y Breton
fueron compañeros de misión en Guadalupe. Rochefort copió de Du Tertre 1654 y
de papeles de Breton. Y Adam, Goeje y Rouse leen a todos ellos.

Para contar dos atestaciones kalinago hace falta un testigo de fuera de ese
grupo: La Borde, Labat o el Anónimo de Carpentras.

Lo mismo vale del lado caquetío-taíno. Oviedo describe tanto al díao como al
cacique taíno, y un paralelo que sólo cuente Oviedo puede ser su manera de
contar.

---

## 4. Recomendación

### 4.1 Orden

1. **Breton 1665 + 1666, en imagen y por entradas.**
   - Ya está en el repo: no hay que bajar nada.
   - Se lee con Goeje 1939 pp. 37-39 como tamiz y Rouse 1948 pp. 545-563 como
     índice de temas.
   - Es la primaria de todo lo demás, y la única que trae la marca f., que es
     la que decide el lado arahuaco.
2. **Rochefort 1658, libro II (la historia moral).**
   - Se localiza con la transcripción TCP de Davies 1666 y se cita del
     francés de 1658 en imagen.
   - Cubre lo que el diccionario dispersa o no tiene: Louquo (P9), las almas
     (P3), el funeral (P8) y las cenizas del jefe (P7).
   - **Pide permiso para bajar.**
3. **Du Tertre 1667, t. II: el tratado de los «sauvages».**
   - Sirve para verificar lo que Rouse le atribuye (la iniciación del boyé,
     P5) y el funeral.
   - Cuenta como segundo testigo SÓLO donde no repita a Breton.
   - **Pide permiso para bajar.**

**No ahora:**

- Labat: tardío.
- Taylor 1951 y la etnografía garífuna: s. XX, retro-abstraído.
- Hulme y Whitehead: mapa, no testigo.
- Las *Relations* de Breton: no hay copia libre.

La edición crítica de 1999 entra si la lectura del 1665 en imagen se atasca.

### 4.2 Preguntas de minería (formato minar-fuente)

**Minería 1: Breton 1665-1666 (con Goeje pp. 37-39 y Rouse pp. 545-563)**

- **Pregunta (§0).** Para cada una de P1-P10: ¿qué dice Breton? ¿En qué
  registro (h., f. o común)? ¿Lo vio o lo oyó contar? ¿Y con qué sigla de
  origen lo marca Goeje?
- **Ortografía antes de contar (§2).** Breton escribe `ch` por la `s`/`sh`
  inicial (p. 442). Los acentos agudos y circunflejos varían, y usa `ou`/`oü`
  por `u`/`w`, s larga y `u`/`v`. Las variantes mínimas a buscar:
  - el espíritu bueno: `chemijn chemiin cheme- çemijn zemi`
  - el espíritu personal: `icheiri ichéiri ichéiricou licheiri`
  - el maboya: `mapoya maboya mápoya mapoyanum`
  - el espíritu del muerto: `oupoyem opoyem poyem`
  - el alma-corazón de hombres: `ioüanni iouanni ioüânni liouanni nioüanni`
  - el alma-corazón de mujeres: `anichi nanichi banichi lanichi`
  - los espíritus buenos: `akamboué akambou kamboue`
  - el espíritu del mar: `oumêcou oumecou omicou`
  - el chamán: `boyé boye boyez boyâicou boyahicou`
  - el primer hombre: `Louquo Lúcuo lukuo`

  El cero de Louquo en Breton, que ya midió la campaña del mar, se vuelve a
  medir con estas variantes antes de darlo por bueno (regla 6). La marca de
  mujeres es «f.» delante de la forma (verificada en imagen en 1666 p. 3).
- **Pasajes (§3).**
  - Las páginas de la tabla de §1.1, cada una vista en imagen con pymupdf
    (leer-fuente §3).
  - En el tomo de 1666, las entradas francesas *Ame, Boyé, Diable, Dieu,
    Esprit, Enterrer, Mort, Os, Songe/Rêver, Sorcier, Médecin, Penser,
    Ombre*.
  - Goeje pp. 37-39 en imagen, con la columna de siglas.
- **Qué se anota por hallazgo.**
  - La forma exacta y su registro.
  - La página impresa, vista.
  - El contenido, en paráfrasis con cita corta.
  - Si Breton lo vio, lo oyó o lo deduce.
  - La marca colonial, si la glosa es catequística (Dieu, diable, sacrifice,
    prière).
- **Esferas (§4).**
  - Creencia: comparanda kalinago.
  - Lengua-cognados: `opoyem ~ opía`, `chemiin ~ cemí ~ seme-he`,
    `anichi ~ ?`, siempre con el filtro de la glosa.
  - Transmisión: cómo se hace un boyé, y las mujeres boyé.
  - Lexicón: las notas de `maboya` y `bejique` van a un issue, no se corrigen
    a mano.
- **Negativas que hay que poder escribir (§6).**
  - Si Breton NO da forma de mujeres para el chamán ni para el espíritu malo.
  - Si en Breton no hay varias almas (entonces son de Rochefort o Du Tertre).
  - Si `Louquo` sigue en 0.
- **Salida (§7).**
  - El YAML `6-fusion/creencia_kalinago_<fecha>.yaml`, con dos secciones:
    - §comparanda.kalinago: un hecho por id, con `registro`, `sigla_goeje`,
      `testigo`, `epoca` y `lugar`.
    - §tamiz: P1-P10, cada una con su veredicto (corroboración, candidato a
      reconstruido, hipotético o caribe).
  - El issue, en `6-fusion/issues-pendientes/`.
  - La bitácora, en [[breton-1665]] (y en [[goeje-1939]] y
    [[steward-1948-hsai-4]]).
  - Y al cerrar, `python generar_bandeja.py`.

**Minería 2: Rochefort 1658 (localizado con Davies 1666 TCP)**

- **Pregunta.** ¿Qué dice Rochefort que Breton no diga sobre:
  - Louquo y el origen,
  - las almas y su destino,
  - el funeral y las cenizas del jefe,
  - el boyé y el maboya?

  ¿Y qué de eso es copia de Breton o de Du Tertre 1654?
- **Ortografía.** Además de las variantes de Breton, las de Rochefort
  (probables: `Louquo`, `Maboya`, `Boyé`, `Akambouë`, `Chemeen`; se miden en
  el TCP antes de contar). Davies anglicaniza las grafías: se miden aparte.
- **Pasajes.** Los capítulos del libro II sobre religión, almas, origen y
  exequias (la parte moral va de la p. 263 a la 514). Se localizan en el TCP
  y se citan del francés de 1658 en imagen.
- **Independencia.** Por cada hecho: ¿ya está en Breton? Si está, Rochefort
  no suma testigo.
- **Salida.** El mismo YAML de la minería 1, en una sección propia.

**Minería 3: Du Tertre 1667, t. II**

- **Pregunta.** ¿Sostiene Du Tertre lo que Rouse le atribuye? Esto es: cinco
  meses de ayuno; una mesa con casabe, fruta y oüicou; y el boyé viejo que
  llama a su espíritu con humo de tabaco. ¿Y qué añade sobre los muertos y los
  huesos guardados?
- **Ortografía.** `Boyé`, `Maboya`, `Chemeen`/`Chemiin`, `oüicou`,
  `Akambouë`. Hay que medir el desfase del tomo, que puede derivar por las
  láminas.
- **Pasajes.** Las pp. 365-366 que cita Rouse y el resto del tratado de los
  «habitants naturels». Antes, identificar cuál de las copias JCB es el t. II.
- **Independencia.** Du Tertre y Breton compartieron misión: lo que repite a
  Breton no suma.

### 4.3 Qué sale, y adónde

En la minería no entra nada al canon. Para cada hecho, la propuesta dice cuál
de estas cinco salidas le toca:

- (a) corroboración de un hecho caquetío atestiguado;
- (b) candidato a `reconstruido` (dos hermanas);
- (c) `hipotetico` (una hermana);
- (d) caribe: comparanda de esfera;
- (e) tradición viva: `retro-abstraido`.

Si Miguel lo fusiona, el ensayo 03 gana una «Vía A′: las hermanas antillanas»,
junto a la wayuu.

### 4.4 Lo que esta nota le pide a Miguel

- **K1.** Permiso para bajar Rochefort 1658 (archive.org, 69,5 MB) y la
  transcripción TCP de Davies 1666 (1,24 MB).
- **K2.** Permiso para bajar Du Tertre 1667 t. II: la copia del Wellcome (236
  MB) o la copia JCB que resulte ser el t. II (~60 MB).
- **K3.** Si se baja o no la edición crítica de 1999 (IRD, 32 MB) como ayuda
  de lectura.
- **K4.** La regla de proyección de §2.1 para los hechos culturales
  kalinago:
  - dos hermanas = `reconstruido`; una = `hipotetico`;
  - el nombre h/f es una pista, no una prueba;
  - la capa arahuaca kalinago se proyecta al caquetío del s. XIV-XV sólo con
    una segunda hermana;
  - lo garífuna es `retro-abstraido`.

  Sin K4, la minería sólo puede dejar comparanda.

Nada de esto se ha publicado todavía. Cuando arranque la campaña, va como
issue con la etiqueta `decision` (regla 10).

### 4.5 Rastro de esta nota

- **Las pistas de página de Breton.** Salen de `pdftotext -enc UTF-8` sobre
  los PDF de OneDrive, buscando las grafías de §4.2 y aplicando los desfases
  de la ficha. El texto extraído quedó en el scratchpad y no en el repo: se
  regenera en un segundo, y lo que vale está en la tabla de §1.1.
- **Las URLs.** Se comprobaron el 2026-10-08 con un HEAD de curl y con la API
  de metadatos de archive.org. No se bajó ninguna obra.
- **Los conteos del corpus.** Grep de hoy sobre `3-mundo/corpus/*.yaml`.
