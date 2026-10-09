---
tipo: sesion-mineria
pregunta: "¿Qué dice la creencia kalinago, pasada por el tamiz h/f y arahuaco/caribe/colonial, que sirva al caquetío? ¿Y qué hace con la Vía A del ensayo 03?"
pueblo: kalinago
fecha: 2026-10-09
moc: mapa-creencia
ensayo: 03_creencia_caquetia
plan: 08_creencia_kalinago_que-minar
propuesta: 6-fusion/creencia_kalinago_2026-10-09.yaml
issue: 6-fusion/issues-pendientes/lexicon-maboya-bejique-sin-respaldo-2026-10-09.md
estado: "propuesta: nada fusionado; nada descargado"
---

# Creencia kalinago: la minería de Breton, con Goeje de tamiz y Rouse de índice

> [[mapa-creencia]] · [[03_creencia_caquetia|ensayo 03]] · plan: [[08_creencia_kalinago_que-minar]] · [[03_creencia|hoja de la sesión 3]]
> Fuentes: [[breton-1665]] · [[goeje-1939]] · [[steward-1948-hsai-4]] · [[pane-c1498]] · [[oviedo-y-valdes-1852-1855]] · [[arcaya-1920]]

**En corto.** Breton cuenta más de lo que el ensayo 03 sabe del chamán
antillano, y lo cuenta con el francés del confesor dentro. Tres cosas
cambian el ensayo:

1. **El espíritu del especialista tiene dos hermanas.** El ichéiri kalinago
   y el cemí taíno coinciden en lo que hacen, no en cómo se llaman. Son
   gente que fue, hombres y mujeres. Mandan el huracán, hacen crecer la
   yuca, dan y curan males y comen lo que se les pone. Eso es candidato a
   `reconstruido`.
2. **El modelo de la enfermedad de la Vía A (`creencia-006`, el alma que se
   aleja) choca con las dos hermanas antillanas.** Y choca también con el
   propio caquetío: Oviedo t. II p. 299 describe al boratio **chupando** el
   lugar del dolor y mostrando la espina o la piedra. Esa cura atestiguada
   no está en el corpus.
3. **La pareja «Dios/diablo» es del misionero.** Breton catequiza con
   `Ichéiri` y `chemiin`, y confiesa que usó `mapoya` para el Diablo. A
   mapoya, dice él mismo, nadie le ofrecía nada.

La propuesta entera, hecho por hecho, está en
`6-fusion/creencia_kalinago_2026-10-09.yaml`. El issue de las dos notas del
lexicón está en
`6-fusion/issues-pendientes/lexicon-maboya-bejique-sin-respaldo-2026-10-09.md`.

---

## 1. Qué se preguntó y cómo se leyó

- **La pregunta.** Es la de la Minería 1 del plan ([[08_creencia_kalinago_que-minar]]
  §4.2): P1-P10, cada una con su registro (h., f. o común), si Breton lo vio o
  lo oyó, y la sigla de origen de Goeje.
- **La regla de capa.** Es la decisión de Miguel del 2026-10-09, opción C:
  - lo nuevo con dos tradiciones arahuacas independientes es `reconstruido`;
  - con una sola, `hipotetico`;
  - lo que sólo ilumina un hecho caquetío atestiguado es `lectura`.

  A esas tres se suman dos salidas que no van al caquetío: `comparanda-esfera`
  para la capa caribe y `no-proyecta` para la capa colonial o el léxico.
- **Cómo se leyó.** Primero `pdftotext` de los PDF de OneDrive al scratchpad,
  para localizar las grafías de §4.2 del plan. Después, cada pasaje que se
  cita, recortado en bandas con pymupdf y leído **en imagen**. Las páginas
  vistas están en `meta.cobertura` de la propuesta. Los desfases de la ficha
  se confirmaron al leer: 1665, impresa = pdf − 22; 1666, impresa = pdf − 8;
  Goeje, pdf − 1. El de Rouse deriva: pdf 697 = p. 545, pdf 716 = p. 564 y
  pdf 723 = p. 565.
- **La hermana taína** es Pané, del texto de Wikisource del repo, citado por
  capítulo: es independiente de Breton. **El lado caquetío** es Oviedo t. II
  pp. 298-299, visto hoy en imagen, más los ids de `creencia.yaml`, leídos
  sin editar.
- **Cifras.** Las da el YAML; se miden así:
  `python -c "import yaml,collections as c; h=yaml.safe_load(open('6-fusion/creencia_kalinago_2026-10-09.yaml',encoding='utf-8'))['comparanda']['kalinago']['hechos']; print(len(h), c.Counter(x['capa'] for x in h), c.Counter(x['sustrato'] for x in h))"`.
  Al cerrar daba 21 hechos:
  - por capa: 6 `lectura`, 6 `no-proyecta`, 4 `hipotetico`, 3
    `comparanda-esfera` y 2 `reconstruido`;
  - por sustrato: 12 arahuaco, 4 sin decidir, 3 caribe y 2 colonial.

## 2. Lo que dio, pregunta por pregunta

### P1. El espíritu tutelar (ck09-01 a 04)

- **El nombre.** «Dieu, Icheíri Iouloúca, f. Chemiin» (1666 p. 118). Goeje
  (p. 38) filia la forma de mujeres al lokono `seme-he` (sigla «f 2 am 10»),
  y las dos de hombres al kalina: `išeiri` «hK?» e `iuluka` «hK». Breton
  avisa de que otros dicen `çemijn` (1665 p. 96), que es el cemí. El par mide
  la palabra, no la creencia.
- **De quién es.** Es del boyé, no de todos. «Les Boyés font les autres
  boyés»: el aprendiz ayuna, el boyé hace bajar a su espíritu, «qui luy en
  donne vn», y se dice «le Dieu d’vn tel boyé» (1665 p. 283; también p. 286).
  Rouse (p. 562) dice que cada caribe tenía el suyo y llama maboya al
  espíritu del boyé. Breton, el testigo, dice lo contrario en las dos cosas.
- **Qué hace** (1665 pp. 283-284, 271, 341):
  - no hay fiesta de bebida sin ofrenda para él;
  - hace crecer la yuca y se le deben las primicias;
  - hay espíritus jóvenes y viejos, hombres y mujeres, y uno «se dit auoir
    esté autrefois Arroüagues»;
  - hacen los huracanes, dan males que otros no curan y mandan a los boyés
    qué hierbas tomar;
  - se los teme más de lo que se los ama.

  Pané cap. XV da lo mismo de los cemíes: algunos tienen los huesos de los
  padres; unos hablan, otros hacen nacer la comida, llover o correr el viento.
  En el cap. XX un cemí manda enfermedad si no se le da yuca, y en el cap.
  XXIII Guabancex, que es mujer, manda viento y agua.
- **La ofrenda.** Es casabe sobre la mesa (`matoútou`) (1665 p. 56; h. y f.
  en 1666 p. 312). Pané cap. XVI: la comida en la casa del cemí.

Veredicto: **candidato a `reconstruido` como estructura** (ck09-03 y 04), y
**`lectura`** de `creencia-025` y `creencia-013`. Ningún nombre se
caquetiza.

### P2 y P3. El alma (ck09-12, 13)

- **El alma del vivo.** «Ame, nacáli, nioüanni. f. nánichi» (1666 p. 17).
  Goeje pone `aniši` de mujeres junto al `goeiz` taíno («fT?»). El pulso es
  «l’ame de la main (disent les Sauuages)» (1665 pp. 40-41).
- **El espíritu.** «esprit, acanſáncou, acámbouée, f. opoyem» (1666 p. 158).
  Breton glosa sólo «esprit». Lo de «âme de mort» es de Goeje (p. 38), que
  no dice de dónde lo saca.

**Degradado a `hipotetico`.** El taíno separa con claridad el alma del vivo
y la del muerto («goeiz … opia», Pané cap. XIII); el kalinago de Breton no
lo hace. `opoyem ~ opía` va a cognados como candidato, con el aviso de que
la glosa sólo casa vía Goeje. Las «varias almas» son sólo de Rouse.

### P4. El mapoya (ck09-09 a 11)

- **Lo que es.** Es «esprit malin» (1665 p. 424), sin forma de mujeres en
  1666 p. 118. Se come la luna en el eclipse y se baila toda la noche
  (pp. 21, 370). Manda males (p. 342). La pesadilla es pelear con él (p. 341).
  Y a él no se le ofrece nada (p. 283).
- **Su nombre.** Goeje le pone sigla «fam?» y lee `ma-poya` «(sans-âme ?)».
  En Breton está el positivo, «Kapoyénti nyáim, il y a là vn esprit»
  (p. 424). Es una lectura, no una prueba.
- **La capa colonial.** Es fuerte: Breton lo usó para el Diablo (p. 424), el
  catecismo prohíbe «sacrifier aux diables» con `mapoyanum` (p. 56) y el
  francés de las islas llamaba ya «maboya» a un lagarto (p. 8).

Veredicto: `hipotetico`, y en ningún caso es el buio (ver el issue). Los
`oumécou` y `couloúbi` son caribes (Goeje: «K?», «KTu») y van a la esfera.

### P5. El boyé y su sesión (ck09-05 a 08)

- **La sesión, en primera persona** (1665 pp. 216-218, todo visto en
  imagen):
  - la ofrenda va al fondo de la casa redonda, con una hamaca;
  - hay canto, y humo de tabaco hacia arriba «au lieu d’encens»;
  - el espíritu cae «comme vn sac de farine», se sienta y come;
  - se apaga el fuego y se hace siempre de noche;
  - «les femmes m’arresterent»;
  - y la que bajó «estoit vne femme qui estoit boyée».
- **Las canciones.** Breton se negó a escribirlas: «que ie n’ay iamais
  voulu ny entendre, ny écrire» (p. 218). Es una ausencia deliberada, no un
  cero de la fuente.
- **El nombre.** `boyé` es «KTu» en Goeje y no tiene forma de mujeres (1666
  p. 52): es caribe, a la esfera.
- **La cura.** Es por succión: los boyés «succent le mal … (à ce qu’ils
  disent) tantost des pierres» (1665 p. 167). Pané cap. XVI da lo mismo.

Veredicto:
- `lectura` de lo que Oviedo ya atestigua del boratio: el encierro en un
  buhío con «ahumadas que llaman tabacos» (t. II p. 298) y la cura por
  succión (p. 299; §5);
- `hipotetico` para las boratias, porque es una sola hermana y la wayuu ya
  no cuenta (D11).

### P6, P7 y P8. Los muertos (ck09-14 a 19)

- **El funeral, visto por Breton** (1665 pp. 237-238):
  - pintan al muerto de rojo, lo envuelven en algodón y lo entierran en
    medio de la casa en la postura «qu’ils auoiet dans le ventre de leur
    mere»;
  - lloran cantando de noche y al alba;
  - ponen pan y bebida en la fosa y hacen fuego alrededor;
  - y **«au bout de l’an»** vuelven, levantan las tablas, pisan la tierra
    sobre «les corps consommez», beben día y noche y a veces dejan la casa
    («comme ie l’ay veu apres la mort d’Henri Comte»).

  Corrobora `creencia-010`, `010b` y `010c` y la estructura de `010d`: es
  `lectura`. No corrobora beber los huesos: se bebe **sobre** la fosa.
- **El canibalismo kalinago es de enemigos.** «Resiouys toy par ce qu’on
  mangera de l’Arroüague» (1665 p. 216). Es caribe y va a la esfera: la
  lógica contraria a la del caquetío.
- **Los huesos de los antepasados guardados por el boyé** (Rouse p. 562) y
  **las cenizas del jefe en bebida** (Rouse p. 559, sin nota) no están en la
  capa de texto de Breton. El primero tiene hermana taína primaria (Pané
  caps. IX, XV y XVI): es `lectura` del díao guardado (`010b`). Al segundo no
  se le conoce fuente: sin decidir.
- **«No nombrar al muerto»** no está en Breton. Lo que hay en p. 221 es la
  tecnonimia de los vivos casados.

### P9 y P10

- **Louquo.** Da 0 en Breton (cinco variantes en la capa de texto de los dos
  tomos). Goeje lo toma de La Borde: su sigla «1 bo», p. 39, se lee en la
  clave de la p. 19. Pendiente.
- **El eclipse comido por el mapoya** queda como comparanda: el caquetío no
  tiene dato.

## 3. Los tres hallazgos más fuertes

1. **El espíritu del especialista, con dos hermanas.** Ichéiri (Breton 1665
   pp. 56, 283-284) y cemí (Pané caps. XV, XVI, XX, XXIII) son espíritus de
   gente que fue. Mandan viento, temporal, crecimiento y enfermedad, y comen
   lo que se les pone. Es lo primero que la Vía A′ antillana le da al
   ensayo como `reconstruido`: candidato, que espera K4.
2. **Lo antillano y Oviedo contradicen `creencia-006`.** Las dos hermanas
   antillanas y el propio Oviedo describen el mal como algo **enviado o
   metido** que el especialista **chupa y saca**, no como un alma que se
   aleja. La cura caquetía por succión (t. II p. 299) está atestiguada y no
   está en el corpus (`ck09-L1`).
3. **La capa colonial está dentro de las glosas, y Breton la confiesa.**
   - Catequiza con `Ichéiri` («La crainte de Dieu…», 1665 p. 41;
     «Lichéirigoni-Christê», 1666 p. 103).
   - Catequiza con `chemiin` («Dieu s’est incarné», 1666 p. 211).
   - Usa `mapoya` para el Diablo (1665 p. 424).
   - Prohíbe ofrecer a los `mapoyanum` lo que se ofrece al ichéiri (p. 56).
   - Rouse, que lee a Du Tertre, lleva la confusión un paso más allá: llama
     maboya al espíritu del boyé.

## 4. Lo que no se halló (regla 6)

- Forma de mujeres para el chamán (1666 p. 52) y para el mapoya (1666
  p. 118): ninguna.
- Varias almas: sólo «l’ame de la main».
- Louquo: 0. Los huesos del boyé y las cenizas del jefe: 0 en la capa de
  texto de Breton.
- Tierra de los muertos con nombre: ninguna en lo leído.
- Las canciones del boyé: censuradas por Breton.

Todo cero de capa de texto mide la capa, no la obra.

## 5. Hallazgo lateral: la cura del boratio (Oviedo t. II p. 299)

Visto en imagen. El boratio:
- pregunta al enfermo si quiere sanar y si cree que él lo sanará;
- manda ayunar a la casa (esto ya está en `creencia-023`);
- con las manos «como quien quiere juntar otra cosa, diçe que le allega el
  alma á un cabo, y despues çierra el puño y sóplale con la boca diçiendo:
  Allá yras mal»;
- grita hasta quedar ronco;
- «chúpale con la boca aquel miembro ó lugar del dolor»;
- y al cabo de cinco o seis días muestra «la espina ó piedra ó palo»: «Cata
  aqui lo que te mataba».

Va en la propuesta como `ck09-L1`, con etiqueta `atestiguado`, para que
Miguel decida si entra a `creencia.yaml`. Dos avisos:
- «allega el alma» es ambiguo y aquí no se decide. Con el soplo y el «Allá
  yras mal» se parece más a despedir el mal, como en Pané cap. XVI, que a
  traer de vuelta un alma perdida.
- La polity es la gobernación de Venezuela, no sólo la costa (regla 4).

## 6. Qué queda

- **K1 y K2** (Rochefort 1658, Du Tertre 1667 t. II). Verifican si `opoyem`
  es el alma del muerto (P2 subiría a `reconstruido`), los huesos del boyé,
  las cenizas del jefe y «no nombrar al muerto», y la iniciación de cinco
  meses que Rouse atribuye a Du Tertre t. II pp. 365-366.
- **La Borde** (fuera del repo): Louquo y la teogonía.
- **El cruce con el minero lokono**: `seme-he` y la ofrenda al espíritu
  tutelar, por si el lokono da una tercera hermana.
- **K4 sigue abierta.** Sin ella, lo marcado `reconstruido` es candidato.
- **No se leyeron** los ~400 pares h/f de 1666 enteros, ni la Grammaire ni el
  Catéchisme.

---

## Auditoría de la Vía A

Lo wayuu se queda como comparanda (opción C). Esto es lo que la hermana
antillana dice de cada id; ninguno se edita. Se lee así: **corrobora** = otra
hermana arahuaca, con fuente propia, dice lo mismo; **contradice** = dicen
otra cosa; **no toca** = no hablan de eso.

- **`creencia-002`, el piache cura por el sueño: corrobora en parte.** El
  espíritu auxiliar que revela causa y remedio tiene dos hermanas:
  - los espíritus «ordonnent aux Boyez de prendre de telles herbes pour tels
    maux» (Breton 1665 p. 284);
  - los cemíes le dicen al behique «de dónde provino la enfermedad» (Pané
    cap. XV).

  El sueño como lugar de la cura no lo toca nadie: las dos hermanas lo hacen
  en sesión nocturna o con cohoba.
- **`creencia-003`, la parafernalia del piache: corrobora, y mejor que eso.**
  - Tabaco, canto y casa cerrada y a oscuras, de noche: Breton 1665
    pp. 216-217 (visto) y Pané caps. XV, XVI y XIX.
  - Oviedo t. II p. 298 ya lo atestigua del boratio: «se ençierran en un
    buhío solo: y allí se echan unas ahumadas que llaman tabacos», y le
    pagan con una joya de oro.
  - El espíritu-serpiente sólo es taíno (cemíes «en forma de culebras», Pané
    cap. XVIII). En Breton el espíritu cae «comme vn sac de farine».
- **`creencia-005`, en el sueño el alma sale del cuerpo: no toca.** La
  pesadilla kalinago es un ataque de fuera: «comme s’ils estoient aux prises
  auec máboya» (Breton 1665 p. 341). Rouse p. 562 dice lo mismo. Nadie dice
  que el alma salga.
- **`creencia-006`, la enfermedad es el alma que se aleja: contradice.**
  - Las dos hermanas antillanas dan el mal enviado y la cura por succión:
    Breton 1665 pp. 167, 271 y 342; Pané caps. XVI y XX.
  - El caquetío también: el boratio «chúpale con la boca aquel miembro ó
    lugar del dolor» y muestra la espina (Oviedo t. II p. 299).
  - El «allega el alma á un cabo» de esa misma página es ambiguo y no salva
    el modelo.
- **`creencia-007`, males comunes y males del espíritu: corrobora en parte.**
  - La división, sí: los espíritus dan males «que les autres ne peuvent
    guarir» (Breton 1665 p. 284), y las mujeres curan con hierbas (Rouse
    p. 563, tercera mano).
  - La semejanza como cura, no. En Breton la semejanza daña: es el tabú del
    manatí (p. 275).
- **`creencia-008`, los muertos recientes peligrosos y los antiguos
  protectores: corrobora la ambivalencia.**
  - Los espíritus que fueron gente curan y dañan, y «ils craignent plus les
    premiers qu’ils ne les ayment» (Breton 1665 pp. 271, 283-284).
  - En el taíno, las opías nocturnas se temen (Pané cap. XIII) y los cemíes
    con huesos de los antepasados ayudan (cap. XV).
  - El robo del alma de los niños no lo toca nadie.
- **`creencia-009`, la tierra de los muertos sin premio ni castigo: no
  toca.**
  - Breton no da tierra de los muertos con nombre.
  - Sus «peines … coulpes» (1665 p. 237) son lectura de confesor (ck09-15),
    y el paraíso de guerreros de Rouse (p. 561 n. 10) es de tercera mano:
    ninguno de los dos sirve para medir.
  - La tierra con nombre es taína (Coaibai, Pané cap. XII), y la mide el
    minero taíno.
- **`creencia-010d`, el segundo entierro y el alma que se funde: corrobora
  la estructura.** Breton lo vio: «au bout de l’an ils retournent pleurer,
  leuent les planches … boiuent le reste du iour & de la nuict, & quelquefois
  quittent les maisons» (1665 pp. 237-238). El porqué —el alma individual
  que se funde con los mayores— no lo toca.
- **`creencia-011`, los tabúes de quien maneja los huesos: no toca.** En
  Breton nadie manipula huesos con tabúes. Las mujeres guardan la sesión y
  son boyé (p. 217), no exhumadoras.
- **`creencia-012`, los huesos y las cenizas traen la lluvia: corrobora
  reformulado.**
  - Lo que tiene dos hermanas es la versión amplia: los espíritus de gente
    que fue hacen el huracán y crecer la yuca (Breton 1665 pp. 56, 284), y
    los cemíes con huesos de los antepasados hacen llover, soplar el viento
    y nacer la comida (Pané caps. XI, XV y XXIII).
  - El mecanismo «cenizas o huesos → nubes» de su referencia (Civrieux, sobre
    los cumanagotos) es caribe de tierra firme: por el tamiz, a comparanda de
    esfera.
