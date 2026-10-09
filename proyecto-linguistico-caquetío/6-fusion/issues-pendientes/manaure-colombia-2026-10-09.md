# Los Manaure de Colombia: ¿homenaje o herencia? — y lo que sí deja la búsqueda

**Para que Miguel decida.** El 2026-10-09 Miguel escribió: «hay un pueblo que
tengo entendido que está también en la frontera, que se llama Manaure, en
Colombia… podríamos investigar más sobre esos Manaure de Colombia». Son dos:
**Manaure (La Guajira)**, el de las salinas, y **Manaure Balcón del Cesar**,
en la vertiente occidental del Perijá. La minería del mismo día barrió los
106 textos de `fuentes_caquetios/` y leyó en la web lo que no exigía
descargar. Todo el detalle, con cita, página y etiqueta, está en
`6-fusion/manaure_colombia_2026-10-09.yaml`; las cifras, en
`6-fusion/medicion_manaure_colombia_2026-10-09.yaml` (las emite
`6-fusion/scripts/medir_manaure_colombia_2026-10-09.py`); la bitácora, en
`4-fuentes/sesiones/13_manaure_colombia.md`.

---

## Lo que se halló, en siete líneas

1. **Desde cuándo.** La primera mención del lugar guajiro que se pudo leer es
   de **1948** (Steward, *Handbook* vol. 4, p. 374: en la temporada de la
   sal, los guajiros del interior «flock to Manaure»). Una noticia de **1864**
   (salinas activas de Chimare, Manaure y Navío Quebrado) sale sólo en un
   resumen de buscador, sin página de origen. El del Cesar no tiene nada más
   viejo que su tradición de fundación (**1874 o 1875**, Buenaventura Maya).
2. **Ningún Manaure colonial al oeste del golfo.** En Oviedo, Castellanos,
   Aguado, Pérez de Tolosa, Carvajal y Oviedo y Baños el único Manaure es el
   de Coro. El mapa del lago que acompaña a Oviedo (t. II, lámina I, visto en
   imagen) no tiene ninguno.
3. **La leyenda que lo muda al lago es del s. XIX.** En 1892 el editor de
   Carvajal ya imprimía que el gran cacique Manaure era «soberano de las
   naciones índicas que habitaban las inmediaciones de la laguna de
   Maracaybo». Es lo mismo que dice hoy el Cesar: «el cacique que gobernó
   Maracaibo».
4. **No hay familia -aure en el oeste.** En el mapa vivo (OSM) de la Guajira,
   el Cesar y el Zulia los únicos nombres en -aure son los dos Manaure y el
   Río Manaure. En las fuentes, un solo nombre occidental del s. XVI:
   **Mapaure, «tierra de Xuduara»** (Oviedo t. II p. 295, agosto de 1533,
   visto en imagen), entre pemenos y bubures. Y -aure sale también en
   Trinidad (Paralaure), en el Orinoco (Parataure) y entre los tarmas
   (Urimaure): no es marca caquetía por sí solo.
5. **Bubures y buredes.** La tradición del Cesar («indios bobures o
   boredes» venidos de Venezuela por el Perijá) acierta en los dos pueblos,
   que son del s. XVI, y en el lugar de los buredes: la lámina de Oviedo los
   pone en **El Valle** (el de Upar). Pero ninguna fuente los une a un
   Manaure. El único puente entre el Manaure de Coro y gente «caribe» es de
   1526 («casado con hijas de caribes»), y Oliver lee que eran jirajaras.
6. **Una homógrafa.** *Manare* es el cernidor de caña y, en el occidente y
   la cordillera, un aro de mimbre (Alvarado 1921 pp. 199-200); Carvajal ya
   la escribe «manaures» en 1647. El «Arco Manaure» que Morón recoge en
   Mérida y el lago (el halo de la luna) se explica mejor como un aro que
   como el cacique.
7. **Veredicto**: **homenaje probable, herencia no documentada**. Lo que
   reabriría la pregunta: que un papel del s. XVIII o de la primera mitad
   del XIX traiga «Manaure» en la Guajira o en el Valle de Upar.

---

## Las decisiones

### D1 · ¿Qué se dice de los Manaure colombianos?

- **A (recomendada).** Se registran como **nombres del s. XIX-XX, homenaje
  probable al cacique de Coro**, sin entrar al canon de topónimos (no son de
  la Kaketiana ni tienen lectura). Quedan en este YAML y en la bitácora,
  listos para reabrirse si aparece un papel anterior a 1850.
- **B.** Se abre una ficha en `2-lengua/toponimos.yaml` como `descartado`
  con su observación (nombre vivo, fecha de fundación, versiones del origen),
  para que el mapa los muestre. Coste: el canon de topónimos es de la
  Kaketiana; estos quedan fuera de su ámbito.
- **C.** No se registran.

### D2 · Mapaure (1533)

- **A (recomendada).** Entra al canon de topónimos como topónimo de la
  esfera **occidental**, `descartado` en lectura (sin glosa), con la
  observación «Juruara, 1533; Jahn lo iguala a Moporo» y la nota de que es
  el único -aure occidental del s. XVI. Regla 4: no toca la polity costera.
- **B.** Se queda en `6-fusion/` hasta que la esfera occidental tenga su
  propio registro de lugares.

### D3 · Los hechos para el corpus (geografía política, esfera occidental)

Dieciocho hechos con id provisional `manaure-col-001…018`. Los que valen
para el canon, por si se fusionan:

- **manaure-col-003** (la lámina: buredes en El Valle) y **manaure-col-018**
  (Castillo, 1538: un pueblo caquetío y otro bobure en Chorna) refuerzan
  `etnia-004`, `etnia-005` y `geografia_politica-009`.
- **manaure-col-004** (1526, «casado con hijas de caribes») es de la polity
  costera y toca parentesco y alianzas; Oliver lo lee como jirajaras.
- **manaure-col-005** (la grafía *Manaore*, Pérez de Tolosa) va a las
  variantes de `manaure` en `6-fusion/antroponimos_caquetios.yaml`.
- **manaure-col-017** (el -aure fuera de la Kaketiana) matiza el formante
  `-aure` de `antroponimos_caquetios.yaml` y de `sistema_de_nombres_era2.yaml`:
  atestiguado no es exclusivo.

Opciones: **A** fusionar esos cinco y dejar el resto en `6-fusion/`;
**B** fusionarlos todos; **C** ninguno por ahora.

### D4 · La homógrafa *manare*

- **A (recomendada).** Una nota en `antroponimos_caquetios.yaml` (entrada
  `manaure`): «en la pluma colonial, manaure ~ manare (cernidor); el "Arco
  Manaure" del occidente es más probablemente el aro». Etiqueta de la
  lectura: hipotético.
- **B.** Nada.

### D5 · Fuentes a pedir (descargar o prestar lo decides tú)

Por orden de lo que responderían a la pregunta 1:

1. **Aguilera Díaz, *Aspectos históricos y socioeconómicos de las salinas de
   Manaure*** (Banco de la República, 2004; PDF libre en web.archive.org) —
   de dónde sale el 1864.
2. **Simons 1885**, *An exploration of the Goajira peninsula* (Proceedings
   of the RGS, con mapa; dominio público) — Steward lo usa en la página
   siguiente; su mapa sería la primera cartografía con el nombre.
3. **El *Derrotero de las islas Antillas*** (1810, BNE; 1820, Cervantes
   Virtual; dominio público) — la costa de Riohacha al Cabo de la Vela.
4. **Felipe Pérez, *Jeografía del Estado del Magdalena*** (1863/1868) y la
   **Carta corográfica del Magdalena** (1864) — si existe una «sabana de
   Manaure» antes de 1874.
5. **Julián 1787** (ed. Unimagdalena, descarga libre) y **Narváez y la Torre
   1778** (BanRep) — la Guajira del s. XVIII.

Las URL están en `fuentes_a_buscar` del YAML.

---

## De paso

- **La pregunta de Miguel trae una versión que no se localizó**: el nombre
  guajiro como «el resplandor de un indígena de gran abolengo». Si sabes de
  dónde la tienes, va a `origen_del_nombre` con su fuente.
- **Una grafía para las sondas**: *Manaore* (Pérez de Tolosa, FD t. II
  p. 248) y *Mauaure* (el OCR de Castellanos 1857). La regla 6 pide medirlas
  antes de contar.
- **Carvajal 1647** sigue siendo la tradición del Manaure que se va hacia el
  **sur** (los llanos del Apure, la laguna de Caranaca), no hacia el oeste.
