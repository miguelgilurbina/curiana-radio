# Capubana en Acasio 2023: el nombre de una estación de la falda, no del cerro

**Para que Miguel decida.** Acasio 2023 se leyó entero el 2026-10-09 (en
texto y en imagen). Afina dos entradas del canon, toponimo-113 y
creencia-022, y deja una propuesta para `sitios_era2.yaml` §Capubana. Todo el
detalle, con cita, página y sonda, está en
`6-fusion/acasio_capubana_2026-10-09.yaml`; la bitácora, en
`4-fuentes/acasio-2023-capubana-calendario.md`.

---

## Lo que dice, y lo que no

1. **«Capubana» es siempre una estación de arte rupestre**: «en la estación
   de arte rupestre Capubana, en la falda del cerro de Santa Ana» (p. 305);
   «Esta estación rupestre se localiza muy cerca de las calzadas, en el primer
   piso biótico del monumento natural a una altura de 210 m.s.n.m» (p. 308).
   El cerro es siempre «Cerro de Santa Ana». **En ninguna parte dice que el
   cerro se llamara Capubana**, ni qué significa el nombre, ni de dónde sale
   (sondas «llamad», «nombre», «denomin», «toponim», «duende»: 0).
2. **El nombre no es suyo.** Lo trae el título de su referencia [4]: «Salazar
   E. Primera Caracterización de los Petroglifos de la estación Capubana –
   Santa Ana. Inparques; 2017» (p. 325).
3. **No da coordenadas.** El Cerro Capuana de OSM está a 6,7 km al ENE de la
   cumbre; las 1.900 ha del monumento equivalen a un círculo de unos 2,5 km de
   radio. Si la estación está «en el primer piso biótico del monumento», lo
   probable es que esté en la falda del macizo y no en el Cerro Capuana. Sin
   el polígono del monumento no se decide.
4. **La forma con b puede no ser independiente.** Coincide con `kapubana`
   'duende del cerro' de Zavala Reyes 2015 #61, sigla HB: Hernández Baño, que
   escribió también sobre petroglifos de Falcón (2000). Si Salazar tomó el
   nombre de ahí, es el mismo dato con otro sello.
5. **No es las Piedras del Almanaque.** Acasio separa su Piedra de Siraba
   (2013, «glifos lunares», p. 313) de la estación Capubana. La candidata a
   las «Piedras del Almanaque» de Esteves (p. 60) es aquélla.
6. **La lectura calendárica es hipotética** y, tal como está construida, no
   se puede refutar (acasio-011): los trazos reciben rótulos, la regla del
   salto y la excepción del año 19 dejan sitio a los valores que hacen falta,
   y no hay nada medido en el cielo. No atribuye el grabado a ningún pueblo
   ni lo fecha.

## A. toponimo-113 (Capuhana)

- **A (recomendada):** añadir la lectura de Acasio (`glosa-fuente`, eje
  `referente`, texto en el YAML §toponimia_propuesta) y una frase a la
  `observacion`. Nivel B sin cambios. La tensión «dos Capubana / el nombre
  bajó / nombre de sector» sigue abierta hasta leer Salazar 2017. Se edita
  `lexicon_toponimos.py` y se regenera.
- **B:** A y además una `forma_viva` «estación Capubana» sin coordenadas.
  Antes hay que comprobar que `export_mapa_seed.py` acepta una forma viva sin
  punto: todas las de hoy lo llevan.
- **C:** leer el artículo como confirmación de que el Santa Ana entero era el
  Capubana y subir la lectura del 2026-09-01. **No se recomienda**: el
  artículo no lo dice.

## B. creencia-022 (las Piedras del Almanaque)

- **A (recomendada):** sin cambio de etiqueta. Se reescribe el «que lo
  subiría»: la lectura publicada de Siraba existe (Acasio 2013; Caguao y
  Morón 2024) y no está en el repo; y aun leída, una lectura de Acasio sería
  hipotética. Se añade que Acasio 2023 es otra estación.
- **B:** además, un hecho nuevo `hipotetico` con la lectura metónica de
  Capubana, marcada como «lectura de autor del s. XXI». Tiene un riesgo: que
  un rótulo de autor («Calendario de las Calzadas») se lea como tradición, que
  es lo que «del Almanaque» sí es.

## C. sitios_era2 §Capubana (materiales)

- **A (recomendada):** añadir la estación como objeto del paisaje, sin su
  lectura: una piedra grabada de menos de un metro junto a un bloque de casi
  cuatro, en la falda, a 210 m (`atestiguado`, moderno; procedencia
  acasio-2023-capubana-calendario, pp. 308-312), con la deuda de coordenadas.
- **B:** esperar a Salazar 2017.

## D. Descargas (decide Miguel)

En este orden: Salazar 2017 (Inparques; sin localizar, probablemente
literatura gris); Hernández Baño 2000 y 1984; Acasio 2013 (la web trae
prólogo y fotos, no el texto); Caguao y Morón 2024 (localizado en Google
Drive). Lista completa en el YAML §fuentes_nuevas_a_buscar.

## Lo que NO se propone

- Ninguna cuenta lunar en el motor. Si se quieren lunas en el calendario de
  tres períodos, la base atestiguada es `apana` y `buiamati` (Zavala #10 y
  #47, sigla GC), no este artículo.
- Ningún cambio a D9 ni a la glosa de `-bana`: Acasio no da glosa.
