---
tipo: sesion-mineria
pregunta: "¿Qué dice de la creencia lokona lo que ya está en el repo, qué autoriza para el caquetío con la regla estricta, y qué le hace a la Vía A wayuu?"
pueblo: lokono
fecha: 2026-10-09
sesion: 9
moc: mapa-creencia
ensayo: 03_creencia_caquetia
plan: 08_creencia_lokono_que-minar
propuesta: 6-fusion/creencia_lokono_2026-10-09.yaml
minadas: [gumilla-1791, brinton-1871, goeje-1939]
cruzadas: [pane-c1498, oviedo-y-valdes-1852-1855]
estado: "propuesta sin fusionar — nada al corpus ni al lexicón; nada descargado"
---

# Minería lokona para la creencia — sesión 9

> [[mapa-creencia]] · [[03_creencia_caquetia|ensayo]] · el plan: [[08_creencia_lokono_que-minar]] · [[03_creencia|hoja de la sesión 3]]
> Obras: [[gumilla-1791]] · [[brinton-1871]] · [[goeje-1939]] · cruces: [[pane-c1498]] · [[oviedo-y-valdes-1852-1855]]
> Las otras hermanas del mismo programa: [[08_creencia_taino_que-minar]] · [[08_creencia_achagua_que-minar]] · [[08_creencia_kalinago_que-minar]]
> Método: [[metodo-comparativo]] · [[lexicon]]

Es el paso 0 de la nota [[08_creencia_lokono_que-minar]] y lo que del resto
ya estaba en el repo: Gumilla t. I, Brinton 1871 y Goeje 1939, leídos para la
creencia lokona y cruzados con Pané y con Oviedo. La propuesta está en
`6-fusion/creencia_lokono_2026-10-09.yaml`; esta nota es la bitácora. No toca
el corpus, el lexicón, el ensayo ni los índices (regla 5). No se descargó nada:
Roth 1915 y Brett 1868 esperan el «adelante» de Miguel.

**La regla de capa** es la decisión de Miguel del 2026-10-09 (opción C de la
nota 08 §3.3) para lo nuevo: `reconstruido` sólo con dos tradiciones
arahuacas hermanas independientes que coinciden en un rasgo específico;
`hipotetico` con una sola, o con dos en un rasgo pan-americano (nota 08
§3.3, «específico, no pan-areal»; regla 2, «en duda, degradar»); `lectura`
cuando lo lokono sólo ilumina un hecho caquetío ya atestiguado, que no cambia
de capa. Lo wayuu de la Vía A se queda y se audita (§7).

---

## 1. Qué se leyó

| Obra | Qué se leyó | Cómo |
|---|---|---|
| [[gumilla-1791]] t. I | Cap. X (los aruacas, pp. 154-157), cap. XIV (ritos funerarios, pp. 199-207), cap. XV (enfermos y piaches, pp. 208-213) y el barrido de todo el tomo con las sondas de §2 | `.txt` del repo para localizar; **cada cita, vista en imagen** (pymupdf) en su página impresa |
| Gumilla t. II | Su única mención aruaca (pdf 63, la costa hacia Cayena) y el cap. XXIII, el eclipse de luna (p. 274) | Igual |
| [[brinton-1871]] | Toda la parte etnológica: la lista de 1598 (p. 9), el vocabulario taíno con sus comparandas arawak (pp. 11-14), el mito de la p. 18 y la composición de palabras (p. 8) | `.txt` + imagen del PDF que repuso #204 |
| [[goeje-1939]] | Las dos secciones «Religion, Magie» (taína, pp. 7-8; kalinago, pp. 37-38), sol y luna (pp. 53-54) y el eclipse (p. 80). Sólo las formas `A` (lokono) y las que hacen de segunda hermana | `.txt` + imagen; la cursiva del OCR no se cita sin verla |
| [[pane-c1498]] (cruce) | Caps. VI (Guabonito), XIII (goeiz y opía), XIV (bohutis, mayohavau), XV-XVI (la cura del behique) | Texto de Wikisource (sin páginas: se cita el capítulo) |
| [[oviedo-y-valdes-1852-1855]] (cruce) | t. II pp. 298-299, el boratio | Imagen |

## 2. Método

**Ortografía antes de contar** (minar-fuente §2). Medido el 2026-10-09 con
`grep -o -i <sonda> <obra>.txt | wc -l`, sobre los `.txt` de `fuentes_caquetios/`:

| Obra | Sonda | Sale | Qué es en realidad |
|---|---|---|---|
| Gumilla t. I | `aruac` | 12 | Más una que el OCR rompe: «Nacion AriMca» (p. 156, imagen: *Aruaca*). `lokono`, `arauac`, `aroac` dan 0 |
| Gumilla t. I | `maraca` | 6 | Sólo 2 son el instrumento (p. 155); el resto es Maracaibo |
| Gumilla t. I | `piache` · `médico` | 8 · 9 | Todas leídas |
| Gumilla t. I | `tabaco` · `sueño` · `tempestad` · `trueno` | 11 · 7 · 4 · 1 | Ninguna aruaca: comercio, sueño de los viajeros, tormentas de la navegación |
| Gumilla t. II | `aruac` | 1 | La costa hacia Cayena (pdf 63) |
| Brinton | `Orehu` · `Yauhahu` · `Yauwahu` · `Arawanili` | 4 · 4 · 1 · 3 | Todo en la p. 18 |
| Brinton | `semeci` · `semeti` · `maraka` | 1 · 1 · 1 | pp. 18 · 13 · 18 |
| Brinton | `Aiomun` · `Kondi` · `Kururu` · `Aluberi` · `Alubiri` · `semi-chichi` · `semicici` · `Semecici` | 0 | Ceros de consulta con todas las variantes de la nota 08: estos nombres no están |
| Brinton | `moon` · `dream` | 0 · 0 | La luna sale como `luna` (latín) en la lista de la p. 9 |
| Goeje | `Orehu` · `Yauhahu` · `semi-chichi` · `Aiomun` · `Hadali` | 0 | `lokono` también da 0: el lokono es la sigla `A` |
| Goeje | `Kururu` | 3 | Falsos: *akururusu* 'tordre' y vecinas (línea 3553 del `.txt`), no Kururumanni |
| Goeje | `seme` | 25 | Casi todas son `semence`, `semer`, `semelle`; las de creencia son `seme(-he)` y `šeme` (pp. 7 y 38) |

**Página impresa.** Leída en la cabecera de cada imagen. Desfases medidos:
Gumilla t. I, pdf − 24 en pp. 154-157, − 30 en pp. 199-208 y − 32 en pp.
210 y 311 (deriva, como dice su ficha); Brinton, pdf − 8; Goeje, pdf − 1;
Oviedo t. II, pdf − 14 en pp. 298-299.

**Una segunda hermana sólo cuenta si es independiente** (minar-fuente §8).
Gumilla da aruaca y achagua en el mismo pasaje: dos pueblos, un observador.
Brett llega por Brinton: tercera mano. Pané es independiente de todo lo
lokono. Lo que Gumilla generaliza («todas quantas Naciones he tratado») es
areal y no cuenta como hermana.

## 3. Qué salió

Ocho hechos lokonos, una entrada areal con forma de hecho y cinco pistas para
el lexicón. Por capa (ids de la propuesta):

- **`reconstruido`: ninguno.** Dos candidatos tenían dos hermanas y los baja
  el filtro de especificidad: `lok-04` (la enfermedad metida por un
  espíritu: lokono y taíno) y `lok-03` (el espíritu propio del piache:
  lokono y taíno). Sin ese filtro, `lok-04` sería `reconstruido`. Lo decide
  Miguel, y el YAML lo dice en el campo `filtro` de cada uno.
- **`hipotetico`:** `lok-02` (la maraca), `lok-03`, `lok-04`, `lok-09` (Orehu
  y el arte del piache venido del agua, con Guabonito como paralelo taíno).
- **`lectura`:** `lok-01` (la consulta nocturna en casa aparte → el encierro
  del boratio, Oviedo p. 298), `lok-05` (la cura de vigilia → la cura a
  gritos, Oviedo p. 299), `lok-07` (armas en la fosa, rito aparte para el jefe
  achagua → 010b y 008c), `lok-08` (el médico se lleva los bienes del muerto →
  contraste con 008c). Y `lok-06`, areal (el ayuno de la parentela → 023).
- **Para el lexicón (no son creencia):** `lok-L1` (luna), `lok-L2` (la raíz
  *seme-* 'espíritu'), `lok-L3` (*ibina/ibien* 'remedio, hechizo, tinte'),
  `lok-L4` (el sonajero: las hermanas no coinciden) y `lok-L5` (dos claves
  lokonas del lexicón que no dicen lo que Brinton dice).

### Los tres hallazgos más fuertes

1. **El piache lokono cura despierto, y el boratio también.** Gumilla: la
   consulta es «toda la noche gritando» en «casitas apartadas, pero á vista
   de las Poblaciones» (p. 155), y «los Piaches Aruacas ni duermen, ni dexan
   dormir» (p. 210). Oviedo dice lo mismo del boratio, y eso es caquetío
   atestiguado: se encierra «en un buhío solo» con humo de tabaco uno, dos o
   tres días (t. II p. 298) y cura dando «tantas voçes é ahullidos ençima del
   enfermo que queda ronco» (p. 299). Ninguna fuente arahuaca del repo pone
   la cura en el sueño: la Vía A de 002 se queda sin apoyo de hermana.
2. **La enfermedad es algo que un espíritu mete en el cuerpo, en dos
   hermanas.** El mito de Brett (Brinton p. 18): «Pain and sickness are the
   invisible shafts he shoots at men, *yauhahu simaira* the arrows of
   Yauhahu». Pané cap. XVI: «mira cómo te lo he sacado del cuerpo, donde tu
   cemí te lo había puesto». Y Oviedo p. 299 ya atestigua la mitad caquetía:
   el boratio chupa y saca «la espina ó piedra ó palo» — «Cata aqui lo que te
   mataba». Contradice la etiología de 006 (el alma que se aleja). La flecha
   lokona usa la palabra corriente para 'flecha', ya en la lista de Trinidad
   de 1598 (*symare*; *semaara* en 1800, p. 9).
3. **G2 resuelto: el ayuno de la parentela es areal, no aruaca.** Gumilla
   abre el cap. XV «hablo de todas quantas Naciones he tratado» (p. 208) y
   la receta del ayuno «al enfermo y á toda la parentela» es de «los mas de
   ellos» (p. 210). Lo único aruaca de esa página es la vigilia. No cuenta
   como hermana del ayuno caquetío (023), aunque lo acompaña.

Y una corroboración léxica completa (`lok-L1`): la luna lokona es *cattehel*
en 1598, *katsi* en 1800 (Brinton p. 9), *kathi* en Oliver, y en Goeje *kači*
(p. 54) y *kati u-bule* 'luna nueva' (p. 53). El puente con el caquetío *kati*
se sostiene; la nota de `kati` («LK katsi […] Brinton 1871») queda comprobada
en imagen.

### Correcciones que salen de paso (no se tocan aquí)

- **`akkicyaha`** (lexicón, lokono, «espíritu del ser vivo», cita Brinton):
  Brinton p. 12 escribe *akkuyaha*, «the spirit of a living animal» (imagen a
  600 ppp). Y la clave **`akkuyaha`** del lexicón guarda otra cosa: «poder»,
  fuente wayunaiki, nota «Way. apülain». Parece una colisión de claves.
- **`semett`** (lexicón, lokono, cita Brinton): Brinton p. 13 escribe *semeti*.
- **Goeje no escribe *kathi*:** su lokono es *kači* (p. 54). *kathi* es de la
  Tabla A-2 de Oliver.
- **El «hochet» taíno de Goeje** (*maiohaua*, p. 7) es su lectura del
  *mayohavau* de Pané, que Pané describe como instrumento de madera para
  cantar (cap. XIV), no como sonajero.

## 4. Respuestas a lo que la nota 08 preguntaba

**G1 — los aruacas de Gumilla.** El piache (p. 155): consulta de noche en
casa aparte, con la maraca, gritando, mudando la voz para dar la respuesta
del espíritu, para saber si el enfermo vivirá; se cobra con «todo lo mejor
del difunto» (`lok-01`, `lok-02`, `lok-08`). Tiene un espíritu propio, con el
que habla cada noche (pp. 156-157, `lok-03`, de oídas). El entierro (pp.
199-200): «con todas armas», un cañizo a un palmo sobre el cuerpo y hojas de
plátano para que no le caiga tierra (`lok-07`). Lo que los distingue de los
achaguas: los achaguas hacen ese rito **sólo** con capitanes y caciques, y
sellan con barro «para que no entren las hormigas á inquietar al difunto».

**G2 — el ayuno de la parentela y la vigilia.** El ayuno es areal (p. 208 y
210); la vigilia es aruaca (p. 210, remite a la p. 155). Ver arriba.

**G3 — el entierro «con todas armas».** Dos pueblos, un observador, y no
una generalización: Gumilla distingue (los aruacas, todos; los achaguas,
sólo los jefes). Frente al caquetío: el díao tiene un rito aparte, como el
capitán achagua (010b), y en ninguno de los dos el cuerpo del jefe queda bajo
tierra; el ajuar de 008c tiene la contraria de la p. 207 («ménos entre los
Aruacas, en donde […] el Médico carga con casi todo»). Nada de esto cambia una
capa caquetía. **Negativa que sirve:** de los huesos de los aruacas, Gumilla
no dice nada; los huesos guardados que da son warao (canasto colgado, p. 199)
y caribe (caja colgada al cabo del año, p. 201).

**(2) Goeje y Brinton: Orehu, Yawahu/Yauhahu, semi-chichi, Aiomun Kondi,
con la grafía de cada obra.**

| Lo que se buscaba | Brinton 1871 | Goeje 1939 |
|---|---|---|
| Orehu | *Orehu*, «the spirit of the waters, the woman Orehu» (p. 18, de Brett) | 0 |
| Yawahu / Yauhahu | *Yauwahu or Yauhahu*, «a supreme spiritual being»; *yauhahu simaira* (p. 18) | 0 |
| semi-chichi (el piache) | *semeci* «the sorcery» (p. 18); *semeti* «sorcerers, diviners, priests» (p. 13) | *seme(-he)* «dieux ou esprits qui leur apparaissent dans l'état de transe» (p. 7), *seme-he* «dieu, génie tutélaire» (p. 38): el espíritu, no el piache |
| Aiomun Kondi, Kururumanni | 0 | 0 |
| la maraca | *maraka*, «the holy calabash containing white pebbles» (p. 18) | *A maraka*, compartida con el tupí y el caribe (pp. 7, 37); el habla de mujeres dice *šišira* (p. 37) |

**(3) El puente *kathi ~ kati*.** Verificado en el lexicón (`kati`,
caquetío-atestiguado, Zavala #71; `kathi`, lokono, `lexicon_a2.py`, Oliver
A-2 fila 73) y en las obras (`lok-L1`). Es puente **léxico**: no hay en el
repo ningún mito, eclipse ni rito lunar lokono. Las dos pistas de eclipse que
hay no son de hermana: los loláca y atabáca de Gumilla t. II p. 274 («¿No
vés, como se nos muere la Luna?») y el kalinago de **hombres** de Goeje p. 80
(*li-huesekebu-li nonum*, de *uekebu* 'mourir'). El mito lokono de la luna
está en Rybka 2018 y en Brett, fuera del repo.

## 5. Qué no salió

- **Gumilla, de los aruacas:** nada de tabaco, sueño, alma, tormentas,
  huesos, segundo entierro, iniciación del piache ni ayuno del piache. Medido
  con las sondas de §2 y leído en los tres capítulos.
- **Brinton:** ningún ser supremo con nombre propio fuera del «supreme» de
  Yauhahu; ningún Aiomun Kondi, Kururumanni ni Aluberi; nada del muerto, del
  alma (salvo la glosa *akkuyaha*) ni de la luna como creencia.
- **Goeje:** su sección «Religion, magie» lokona no existe como tal: lo
  lokono sale en la columna `A` de las secciones taína y kalinago. Ninguna
  forma `A` para sueño, alma de muerto ni piache (fuera de *maraka*,
  *seme-he*, *ibina*, *(h)ialoko* 'esprit' —compartida con el kalina— y *üya*
  'image, ombre').
- **Ningún dato lokono precontacto.** Lo más antiguo es la lista de Trinidad
  de 1598, y es léxico.

## 6. Cuánto queda

- **Roth 1915 y Brett 1868**, localizados en la nota 08 §3.2, sin descargar.
  Son los que pueden subir `lok-04` y `lok-09` a `reconstruido` o tumbarlos, y
  los únicos que contestarían R2 (la persona y el sueño), R4 (los huesos) y
  B4 (cerrar `cm24-c-l01` con la página de Brett).
- **Rybka 2018** (web): el único camino para que *kati ~ kathi* sea puente de
  creencia y no sólo de palabra.
- **Navarrete** (s. XVI) y **Goeje 1942** (la iniciación lokona): sin copia.
- **Oviedo t. II p. 299, el gesto sobre el alma.** El boratio, abriendo y
  cerrando las manos sobre el enfermo «como quien quiere juntar otra cosa,
  diçe que le allega el alma á un cabo», y luego cierra el puño y sopla:
  «Allá yras mal». Se puede leer como devolverle el alma o como juntar el mal
  para soplarlo fuera. Decide si 006 tiene apoyo caquetío. No es lokono: lo
  dejo para Miguel. La cura entera ya la propuso
  `6-fusion/taino2_oviedo_venezuela.yaml` (creencia-001, «y_lo_que_se_gana»).
- **Gumilla t. II** no se barrió para creencia más allá del eclipse.

## 7. Auditoría de la Vía A

Cada hecho wayuu de `3-mundo/corpus/creencia.yaml` (sin editarlo), frente a
lo que esta minería encontró. «Corrobora» exige una hermana arahuaca; lo
areal se dice aparte. Las páginas son las impresas, vistas en imagen.

| Id | Qué dice la Vía A | Veredicto | La cita |
|---|---|---|---|
| **creencia-002** | El piache cura en el sueño, guiado por espíritus auxiliares | **Contradice** (el sueño) · corrobora el espíritu auxiliar | Gumilla t. I p. 210: «los Piaches Aruacas ni duermen, ni dexan dormir, ni al enfermo, ni á otros»; p. 155: «se pasan toda la noche gritando». El espíritu propio: p. 156, «su demonio, con quien hablaba todas las noches». Y el caquetío atestiguado tampoco cura en sueño: Oviedo t. II p. 298, «se ençierran en un buhío solo» |
| **creencia-003** | Tabaco, licor, cantos, urari; cierra la casa; cobra; espíritu-serpiente | **Corrobora en parte** | La casa cerrada: Gumilla p. 155, «encerrados en ellas los Médicos». El cobro, pero en bienes del muerto: p. 155, «todo lo mejor del difunto». Añade la maraca (p. 155; Brinton p. 18). No toca tabaco, licor, urari ni serpiente |
| **creencia-005** | Soñar no es dormir; el barsure sale de noche | **No toca** | Cero sueño lokono en las tres obras. Lo único del alma: Brinton p. 12, «Ar. akkuyaha, the spirit of a living animal», sin nada del sueño. El sueño-aviso de Gumilla p. 311 es de la arenga de todas las naciones (areal) |
| **creencia-006** | La enfermedad es el alma que se aleja; curar es negociar su regreso | **Contradice** | Brinton p. 18 (de Brett): «Pain and sickness are the invisible shafts he shoots at men, *yauhahu simaira* the arrows of Yauhahu». Pané cap. XVI: «donde tu cemí te lo había puesto». Abierto: Oviedo p. 299, «le allega el alma á un cabo» (§6) |
| **creencia-007** | Males comunes frente a males del espíritu; lo semejante cura | **No toca** | Para Brett toda enfermedad es flecha («pain and sickness», p. 18): no separa. Goeje p. 38: una sola palabra para «sortilège, remède, teinture», *A ibina*, *f ibien* |
| **creencia-008** | Muertos recientes peligrosos; antiguos protectores | **No toca** | Nada lokono. Lo areal de Gumilla pp. 210-211 («andan vagueando no léjos de sus sepulturas») va con 008b, que es atestiguado |
| **creencia-009** | Tierra de los muertos; la vida sigue igual; sin premio ni castigo | **No toca** | Gumilla p. 200: el aruaca va «con todas armas á la sepultura», sin decir para qué. Lo único lokono del más allá en el corpus sigue siendo *waka* (creencia-028) |
| **creencia-010d** | Segundo velorio wayuu; los huesos al osario; el alma se funde | **No toca** (negativa medida) | Gumilla pp. 199-200 describe la fosa aruaca y nada de los huesos. Los huesos guardados que da son warao (p. 199) y caribe (p. 201), no hermanas |
| **creencia-011** | Tabúes de quien toca los huesos (vigilias, no tocarse) | **No toca** | Sin segundo entierro lokono no hay exhumadora. La vigilia de la p. 210 es del piache en la cura, no de quien maneja huesos |
| **creencia-012** | Huesos y cenizas → nubes → lluvia | **No toca** | Nada lokono une los muertos con la lluvia |

**En una línea:** de los diez hechos de la Vía A, lo lokono del repo
contradice dos (002 en el sueño, 006 en la causa del mal), corrobora en parte
uno (003) y no toca siete. Lo que contradice, contradice con apoyo: en los dos
casos el caquetío atestiguado de Oviedo (pp. 298-299) cae del lado de la
hermana y no del wayuu.
