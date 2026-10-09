# Los xaguas de Carora y Pedregal: ¿achaguas? — y qué hacer con la pista de Mitare

**Para que Miguel decida.** El 2026-10-09 Miguel escribió: «he encontrado que
habían achaguas también en la zona de ahora Falcón, más que todo cerca de lo
que es Mitare, más hacia el lado occidental de Falcón». La minería del mismo
día leyó lo que el repo tiene sobre los *xaguas/axaguas/ajaguas* (Federmann
1530 en alemán y en la traducción de Arcaya, Pérez de Tolosa 1546, Aguado,
Arcaya 1920, Jahn 1927, Oliver 1989 en sus dos ediciones, Urbina 2011, Esteves
1989) y buscó en la web. Todo el detalle, con cita, página y sonda, está en
`6-fusion/xaguas_achaguas_falcon_2026-10-09.yaml`; las cifras, en
`6-fusion/medicion_xaguas_achaguas_2026-10-09.yaml` (las emite
`6-fusion/scripts/medir_xaguas_2026-10-09.py`); la bitácora, en
`4-fuentes/sesiones/11_xaguas_achaguas_falcon.md`.

---

## Lo que se halló, en seis líneas

1. **No hay una sola palabra xagua con glosa** en el repo. Oliver (tesis
   p. 245) habla de «the few words recorded by the chroniclers» y no dice
   cuáles. Lo único que hay son dos nombres de aldea de Federmann, **Coary** y
   **Cacaridi** (1557 [44]-[45], vistos en imagen), sin significado. El cruce
   por concepto con Neira y Ribero tiene cero conceptos; y por forma, los dos
   nombres no se parecen al achagua más que los nombres caquetíos del control
   (Mitare y Miraca se «parecen» más).
2. **La identidad xagua = achagua es una sola voz repetida**: el índice de
   Fernández Duro (1885) → Arcaya (1916, 1920) → Jahn 1927, que copia a
   Arcaya → el diccionario histórico de la RAE, que cita a Jahn. Arcaya
   clasifica el «dialecto» ajagua como arahuaco *deduciéndolo* de la
   identidad, sin una voz. Oliver la rechaza: sólo se parecen los nombres.
3. **El nombre**: *Ajagua* es *Axagua* tras el cambio del castellano (/ʃ/ →
   /x/); *Xagua* y *Achagua* pueden ser el mismo etnónimo mal oído, pero nada
   lo exige. Y la primera mención segura del achagua es de 1583, en el alto
   Meta (Oliver, con Useche 1987): cincuenta años después de los xaguas de
   Federmann, y lejos.
4. **Mitare**: ninguna fuente pone xaguas ni achaguas en Mitare. El pueblo es
   caquetío en el s. XVI (indios libres, Arcaya p. 230) y en 1773 (374
   caquetíos, Martí vía Oliver). Lo más cerca son **las montañas de
   Pedregal**, en la cabecera del mismo río (a unos 37 km), donde Arcaya pone
   ajaguas en encomienda y el obispo Martí, en 1773-1782, axaguas «nómadas»
   que bajaban a Pedregal y Pecaya.
5. **La trampa Baragua/Barragua**: son tres lugares (Baragua de Lara, hoy
   capital de la **parroquia Xaguas**; la Barragua de Rivero en el Airico; el
   Barraguán del bajo Meta). Ni Arcaya ni Jahn los confunden; la trampa es el
   paralelo «achaguas y caquetíos en Barragua» / «xaguas junto a caquetíos
   hacia Baragua».
6. **Lo que sí queda**: un vecino bien documentado de la polity de
   **Barquisimeto** (no la costera): aldeas en 1530, paz con bastones, guerra
   de emboscada con los gayones, lengua propia (cinco intérpretes), sal con los
   caquetíos aun siendo enemigos, culto al sol y la luna en 1579; y después,
   encomienda en la sierra de Coro, y algunos llevados a **Paraguaná** a fines
   del s. XVI (Arcaya p. 327).

---

## Las decisiones

### D1 · ¿Qué es el xagua en `etnias.yaml` (etnia-018)?

- **A (recomendada).** Sigue `familia_linguistica: desconocida`. Se amplía el
  `aviso_familia` con lo medido (la identidad con el achagua es una sola voz y
  no tiene ni una palabra), se añade `ajagua` a las variantes (es la forma
  colonial de Coro y Barquisimeto) y se rehace `donde` con las cuatro épocas
  (1530, 1546, 1579, s. XVIII). Tu decisión de hoy sobre el achagua («una
  línea maipuriana aparte de los caquetíos») queda para el achagua de los
  Llanos y de Neira; no se traslada al xagua.
- **B.** `familia_linguistica: arahuaca`, con etiqueta `hipotetico` y el aviso
  de que descansa sólo en el nombre. Es lo que dirían Arcaya y Jahn; va contra
  «en duda, degradar».
- **C.** Dos entradas: el xagua de Lara (desconocida) y un «ajagua de
  encomienda» de Falcón (s. XVII-XVIII). Separa épocas, pero inventa un
  pueblo donde las fuentes ven uno.

### D2 · La entrada `ajagua` del lexicón

`curiana_lexicon.py` tiene `ajagua` como «grupo Jirajaroide (Jirajaroid
menor)», «cuarto grupo de la familia Jirajaroide», citando a Oramas 1916. Es
una **tercera** filiación para el mismo pueblo, sostenida sólo por el título
de Oramas (que pone «Ajagua» junto al ayamán, el gayón y el jirajara); Oliver
dice que las pocas voces no se relacionan con el jirajarano.

- **A (recomendada).** Re-glosar: «etnónimo de un pueblo de Carora-Pedregal
  de filiación desconocida (xagua/axagua)», fuera de la capa jirajaroide.
- **B.** Archivarla (`FUERA_DEL_HABLA`): un etnónimo sin lengua conocida no
  enseña nada al agente.
- **C.** Dejarla como está, con una nota del conflicto.

### D3 · La pista de Mitare

- **A (recomendada).** Miguel dice dónde lo leyó. Si es «la cuenca del
  Mitare» (Pedregal, Agua Clara), la pista encaja con Arcaya y Martí, pero es
  de encomienda (s. XVII-XVIII), no del s. XV. Si es «el pueblo de Mitare», las
  fuentes leídas dicen caquetío.
- **B.** Se da por respondida con lo medido y no se busca más.

### D4 · ¿Entra algo a la esfera de la simulación (era 2, Paraguaná)?

Los xaguas son de la polity de Barquisimeto y de la colonia; lo único que toca
la Kaketiana es que encomenderos llevaron ajaguas y jirajaras a Paraguaná a
fines del s. XVI.

- **A (recomendada).** No entra nada al mundo de la simulación (regla 3: es
  colonial). Se registra en `etnias.yaml` y basta.
- **B.** Una nota en `3-mundo/esfera-de-interaccion.md` sobre la gente traída
  a Paraguaná en el s. XVI, como contexto, marcada colonial.

### D5 · Fuentes a pedir (descargar o prestar lo decides tú)

En orden de lo que responderían sobre la lengua:

1. **Oramas 1916** (*Materiales… Ajagua*): única vía a algo con glosa (voces o
   apellidos ajaguas de los padrones del Archivo Arzobispal). Dominio público
   en EE. UU.; sin copia en la web hallada.
2. **Arcaya 1977**, 3.ª ed., t. I, pp. 37-45: la edición que discute Oliver;
   ahí deberían estar las «few words».
3. **Arellano Moreno 1964**: las Relaciones de 1579 (Nueva Segovia, El
   Tocuyo, Carora) y Pérez de Tolosa en otra edición. Ya pedida para
   `nueva-segovia-1579`.
4. **Martí 1969**: la cita literal de los axaguas de Pedregal y Pecaya.
5. **Useche Losada 1987**: los «jaguas carniceros» de 1535 en el bajo Meta.

---

## De paso

- En `6-fusion/pendientes_en_alvarado_y_arcaya.yaml` §el_achagua_en_falcon,
  «Tres fuentes diciendo lo mismo» es una corroboración falsa: Jahn copia a
  Arcaya. Se propone anotar allí que la resolución es esta propuesta.
- Federmann 1916 (trad. de Arcaya, sobre la francesa) tiene dos erratas en
  este capítulo: Cacaridi «el 3 de octubre» (el alemán dice el último día de
  octubre) y el reparto de rehenes al revés que el alemán. Y Arcaya 1920
  escribe «Cocaride».
- Esteves p. 118 (vista en imagen): **«ITOWA — Antiguo nombre indígena de
  Churuguara»**. Por la forma y el sitio, probablemente la *Hittova* jirajara
  de Federmann, que Arcaya ponía «al sureste de Churuguara» (Federmann 1916
  p. 31, nota c: «El nombre de Hittova ha desaparecido»); sin cita de Esteves, es un parecido que hay que confirmar.
  No es de esta pregunta; queda para la campaña de topónimos.
