# El mar de Paraguaná en el s. XV: lo que se comía está en los conchales, lo que sonaba está en la historia natural, y lo sagrado del mar todavía no tiene fuente

**Tercera campaña de minería, parcela de fauna FA3 (el mar), 2026-09-22.**
Encargo de Miguel, verbatim: *«…pensando en el territorio pero también en el
Mar tomando en cuenta que el aspecto marino era esencial en la cosmovisión
caquetía […] realizar una campaña para describirlos visualmente, y si es posible
encontrar la onomatopeya que hacen, así le damos a los agentes una descripción
y onomatopeya que "escuchar" por así decirlo.»*

**Ninguna cifra del lado del repo está escrita a mano.** Las imprimen

```bash
python 6-fusion/scripts/medir_fauna_mar.py --conteos   # el bloque meta.medido
python 6-fusion/scripts/medir_fauna_mar.py             # valida: topes, citas, capas
python 6-fusion/scripts/caja_marina_obis_gbif.py       # la caja OBIS/GBIF (usa red)
```

Las cifras del lado de las fuentes son citas y llevan obra y página. Todo está
en `6-fusion/fauna_paraguana_mar_2026-09-22.yaml` (especies, `cosmovision_marina`,
`candidatos_referente`, `propuestas_ecologia`) y
`6-fusion/fauna_mar_caja_obis_gbif_2026-09-22.yaml` (generado).

---

## 0. Lo que del encargo resultó falso al medirlo

1. **«La laguna de Guaranao» como una de las aguas de la era 2.** En el s. XV
   Guaranao era **salina** en la boca de una quebrada (Arcaya p. 22); la
   laguna con manglar y peces nació hacia 1985 de un colector roto
   (ecologia-084). Su fauna de hoy —lisa, corocoro, lenguado— **no se
   proyecta**. El manglar del s. XV está en el borde oeste del Golfete
   (ecologia-011), y ahí van la ostra de mangle y el camarón pistola.
2. **La Tabla II de Zavala Reyes et al. 2018 no está en la p. 404**, como
   dicen la ficha y el aviso del coordinador: está en la **p. 405** de
   *Interciencia* 43(6) (✅ verificado en imagen: cabecera y pie).
3. **`kumarawa` no es sólo «caracol»**: Esteves (p. 33, s.v. CUMARAGUAS, las
   salinas) dice *«Cumaragua es el nombre que dan a un pequeño cangrejo de
   caparazón rosada»* con la significación *«espuma rosada»*. D10 adjudicó la
   glosa a Alvarado por localización sin tener este testigo.
4. **«manatí» no es, según Oviedo, el nombre indígena del animal**: *«por esso
   los chripstianos le llamaron manatí»* por sus dos manos, y en la Española
   *«le quitaron su nombre»* (t. I, p. 434). El lexicón lo tiene como taíno sin
   procedencia, y la lista maestra del taíno lo da como atestiguado por la
   p. 433, que es la captura y no el nombre.
5. **El índice de Esteves no tiene un topónimo «Manate»**: es «Manare»
   (cumanagoto, «cesto de fibra»). Cero de manatí en el gazeteer.
6. **OBIS y GBIF no «pueblan» el mar grande**: dentro de la caja de la
   península hay cero registros de delfines, ballenas, manatí, foca monje, pez
   sierra, mero guasa y tortugas verde y cabezona. Es un cero de muestreo
   (regla 6): las fuentes impresas sí dan nidos de las dos tortugas y un
   rorcual en Paraguaná. Y la trampa de las ausencias disfrazadas (PR #205)
   se aplicó: los registros con estado no presente se descartan y se cuentan.

## 1. Veredicto en una frase

El mar de la era 2 se puede poblar con prueba —lo que se comía está en los
conchales (chipichipi y almeja en tierra firme; botuto, quigua y tortuga en las
islas), lo que se veía y sonaba está en la historia natural—, delfín y tortugas
marinas siguen sin nombre caquetío, y la tesis de un mar sagrado **no tiene
todavía ninguna fuente caquetía**: tiene tres vecinos (lokono, taíno, wayuu)
donde el mar sí da poder, origen o rebaño.

## 2. Lo que hay (ver el YAML para cada cifra y su página)

- **Especies**: una entrada por especie o grupo, con `presencia_s_xv`
  (segura / probable / dudosa / excluida) y su porqué, nombres por lengua con
  su clave, `es_hueco`, `descripcion_visual` ≤ 220 con su fuente y `sonido`.
  Las cuentas están en `meta.medido`.
- **La prueba de oro, los conchales**: Médanos de Coro (s. XIV-XVIII,
  Zavala Reyes et al. 2018 p. 405): *Donax striatus* 42,4 %, *Callista* 27,0 %,
  *Diodora* 8,9 %, *Strombus pugilis* 6,3 %, *Crassostrea* 4,9 %, *Lobatus
  gigas* 1,0 %. En Aruba (Tanki Flip, vía van Buurt pp. 33 y 43): macabí de
  hueso 13,7 % y macabí 5,2 % de los restos de pez.
- **Las migratorias contra los períodos**: las cuatro tortugas anidan en la
  costa norte y este de abril a septiembre, con el pico en junio-julio → **P2,
  la seca larga**, de noche (Rondón-Médicci 2013, Tabla 2 verificada en
  imagen). La costa oeste (AMUAY) no tiene nidos: allí la tortuga es de la
  pesca. En el Golfete hubo desove de cardón y verde, y Tacuato fue playa de la
  verde en 1988. La jorobada, en P1 y dudosa. **La estación de los
  cardúmenes no tiene fuente leída** (la surgencia del Caribe sur: deuda).
- **Los sonidos con fuente**: el mero guasa y la cuna retumban (*Boom*,
  *Thundering Roll*, FishSounds); los roncos roncan al sacarlos; las corvinas
  tamborean; el jurel croa; el sapo de piedra llama (*Boop*); el camarón
  pistola chasquea; la tortuga cardón resopla, bombea y gruñe al tapar el nido
  (Cook y Forrest 2005); la foca monje «roncaba tan recio que desde lejos se
  oía» (Oviedo p. 428); la tonina es el «soplón» de la costa (Romero et al.
  1991 p. 172). **Ninguna fuente da una onomatopeya en castellano o en lengua
  indígena**: dan el nombre del sonido. Los silabeos del YAML son todos
  `hipotetico`.
- **Cosmovisión**: hechos sostenidos con cita (el mar en el léxico y en el
  nombre de la tierra, la despensa, la moneda de concha, el tabaco que decide
  si se sale a pescar, el camino a las islas, el cerro que se ve desde el mar,
  el pez que da la luz), intuiciones no sostenidas con lo que las subiría, y
  comparanda (Orehu lokono, el mar de la calabaza taíno, el «ganado de
  Pulowi» wayuu).
- **Candidatos a referente** (cuántos: `meta.medido`), empezando por el
  delfín «soplón» y la tortuga que desova.

## 3. Lo que NO se encontró

- Ningún conchal cuantificado de la costa OESTE ni del Golfete paraguanero; la
  campaña de arqueología (M8, PR #203) tampoco lo halló en Urbina, Casale y
  Knaf.
- Ningún hueso de pez identificado en tierra firme caquetía.
- Ningún mito, dueño o rito caquetío del mar.
- Ningún registro de delfín en Paraguaná ni en el Golfete.
- Ningún sonido de las tortugas verde, carey y cabezona.
- Sin cubrir por falta de tiempo (el coordinador pidió terminar las entregas
  antes de ampliar): las descripciones de varios invertebrados van
  `reconstruido` o con `deuda: sin-procedencia` (la API de Wikipedia cortó);
  las esponjas, los corales de arrecife y los peces de arrecife de las islas
  (loros, morenas, escorpiones del papiamento) están sólo nombrados en
  `para_otras_parcelas` o sin entrada.

## 4. Opciones para Miguel

**(a) Los candidatos a referente.** A — llevarlos todos a
`REFERENTES_NOVEDOSOS` en un corte de serie; B — llevar sólo los que son
huecos del canon (los que llevan `hueco_canon`: delfín, tortuga que desova,
tortugas de pico, cardumen, concha perlífera) y dejar los de sonido para un
brazo aparte; C — no tocar el motor todavía y
usarlos sólo en `[Tu tierra]`. **Recomiendo B**: son los que el canon ya declaró
mudos y no cambian qué se mide.

**(b) `kumarawa`.** A — abrir de nuevo D10 con el testigo de Esteves p. 33
(cangrejo rosado de las salinas); B — anotarlo en `notas` y dejar la glosa;
C — nada. **Recomiendo A**: la glosa de un nombre de SALINA (Las Cumaraguas) es
justo la que decide si la voz es de mar abierto o de charca.

**(c) El cunaro.** A — dejar su identificación en disputa (mero guasa frente a
pargo cunaro) en el lexicón y en ecologia-015 (pe-7); B — fijar el mero guasa
por la manteca; C — nada. **Recomiendo A**: la manteca es lectura mía.

**(d) La cosmovisión marina.** A — abrir la campaña de los tres caminos de
cm-n2 (Oviedo t. II releído en contexto ritual; ajuares dabajuroides con
M8; petroglifos con motivos marinos); B — dejarla como hipótesis declarada;
C — escribir el dueño del mar en el canon como reconstruido. **Recomiendo A**,
y nunca C sin fuente (regla 2).

## 5. Deudas y cosas vistas de paso

- **Bitácoras pendientes** en fichas que otras parcelas pueden estar tocando
  hoy (para no chocar): `esteves-1989` (Cumaraguas p. 33, Paguara p. 55,
  Tumatey p. 66, Matividiro p. 51; el índice de OCR 6 lee «Manate» por
  «Manare»; los pies de página 51-55 del OCR 2 salen como 21-27),
  `oviedo-y-valdes-1851` (libro XIII caps. I-IX leídos para fauna; impresa =
  pdf − 118 en ese tramo), `arcaya-1920` (pp. 41, 46, 98-99, 120, 197, 233, 264
  para el mar), `zavala-reyes-2018` (la Tabla II es p. 405).
- **La lista maestra del taíno** trata `manati` como taíno atestiguado: ver
  el punto 0.4.
- **La surgencia**: Castellanos, Varela y Muller-Karger 2002 (*Memoria de la
  Fundación La Salle* 154) y los trabajos de la Guajira (SciELO) no se
  pudieron leer (403): son la fuente de la estación de los cardúmenes.
- Los scripts de consulta de FishBase, FishSounds y Wikipedia quedaron en el
  scratchpad; cada dato que dieron va en el YAML con su URL.

🤖 Generado con [Claude Code](https://claude.com/claude-code)
