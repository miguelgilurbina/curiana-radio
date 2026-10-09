---
tipo: bitacora-mineria
pregunta: "¿Qué rasgos de la religión taína de contacto sobreviven al bajar a las primarias del repo, y qué hacen frente a la creencia caquetía?"
pueblo: taino
fecha: 2026-10-09
moc: mapa-creencia
ensayo: 03_creencia_caquetia
plan: 08_creencia_taino_que-minar
propuesta: 6-fusion/creencia_taino_2026-10-09.yaml
script: 6-fusion/scripts/medir_plantilla_oviedo.py
estado: "minado A1-A3 sin descargar nada; nada fusionado; decide Miguel"
---

# Lo taíno para la creencia caquetía: la minería (A1, A2, A3)

> [[mapa-creencia]] · [[03_creencia_caquetia|ensayo]] · [[08_creencia_taino_que-minar|la nota de decisión]] · [[03_creencia|hoja de la sesión 3]]
> Obras minadas: [[oviedo-y-valdes-1851]] · [[oviedo-y-valdes-1852-1855]] · [[pane-c1498]] · [[las-casas-apologetica]] · [[angleria-1892]] · [[colon-hernando-1892]] · [[steward-1948-hsai-4]]
> Propuesta: `6-fusion/creencia_taino_2026-10-09.yaml` · Cifras: `python 6-fusion/scripts/medir_plantilla_oviedo.py --conteos`

**En una frase.** De la «religión arahuaca compartida» queda un rasgo con
primaria en las dos orillas: la imagen de madera del muerto principal, que el
caquetío quema con el díao y el taíno conserva con los huesos dentro y el
nombre del muerto; lo demás, o es plantilla de Oviedo, o es de Barquisimeto, o
es contraste.

**La regla de capas** es la de Miguel del 2026-10-09 (opción C): lo nuevo es
`reconstruido` sólo con dos tradiciones arahuacas independientes, `hipotetico`
con una, y `lectura` si sólo ilumina un hecho caquetío ya atestiguado, sin
tocarle la capa. Lo wayuu de la Vía A se queda y se audita al final.

---

## 1. Qué se leyó y cómo

Nada se descargó. Todo está en `fuentes_caquetios/`. Lo que se cita «en
imagen» se vio con `pymupdf` a resolución nativa (`leer-fuente` §3). El resto
se leyó en la capa de texto, y así lo dice la propuesta.

**A1 — Oviedo a las dos orillas.** Se leyeron enteros, con el guion de fin de
línea deshecho, dos tramos:

- el t. I, lib. V, caps. I-III (impresas 124-140), de la copia íntegra;
- el t. II, lib. XXV, cap. IX (impresas 296-302).

Los dos tomos se sondaron enteros por los huesos, la desecación, el
entierro, Plinio y la magia. El test de plantilla lo hace
`6-fusion/scripts/medir_plantilla_oviedo.py`. El script mide qué parte de los
bigramas de contenido de cada tramo comparte con el de La Española, y lo
compara con dos controles del mismo autor y del mismo tomo: los piaches de
Camanagoto, gente caribe (t. II lib. XXIV cap. XII), y la entrada de Espira,
pura narración (t. II lib. XXV cap. X). Las cifras están en `meta.medido` de
la propuesta y no se copian aquí (regla 1).

**A2 — Pané y sus testigos.** Se leyeron cuatro cadenas:

- **Pané-Wikisource**, caps. IX-XXV;
- **Las Casas**, *Apologética*: el cap. CXX (pp. 320-323), los caps.
  CLXVI-CLXVII (pp. 444-447) y la p. 535, donde habla por su cuenta;
- **Anglería**, vol. 1, Déc. I lib. IX, entero (pp. 339-360);
- **Hernando Colón 1892**, vol. 2, pp. 1-12, entero: es el final de la
  Escritura de fray Román.

El cotejo, rasgo por rasgo, está en `cotejo_pane`. Hay una regla de
independencia (`minar-fuente` §8): Las Casas y Anglería dependen de Pané, así
que coincidir con él mide la transmisión, no el rito. Lo que Las Casas cuenta
por su cuenta (p. 446 «yo los vi»; p. 535) sí es otro testigo.

**A3 — Steward y Rouse 1948.** Se leyeron Steward pp. 21-24 (la 21 en imagen)
y, de Rouse, «Life cycle», «Religion» y «Shamanism» (pp. 531-538; la 532 en
imagen). Cada rasgo se bajó a la primaria de cada lado. Para el lado
caquetío se usó lo que ya había hecho `6-fusion/hsai_caquetios_2026-09-23.yaml`
con Hernández de Alba.

**Desfases medidos hoy sobre las cabeceras.** En las dos ediciones de Oviedo
el pdf contado desde 1 va **uno por delante** de la cifra que traen las
fichas, que cuentan desde 0:

| Tomo | Página pdf (desde 1) | Página impresa |
|---|---|---|
| Oviedo t. I, copia íntegra | 245 | 125 |
| Oviedo t. II | 311 | 297 |

En el t. II, la impresa 255 lleva el folio «525» por errata de imprenta.

## 2. Qué salió

### Los tres hallazgos más fuertes

1. **La imagen de madera del muerto principal, con el destino contrario.**
   - *Lado caquetío*, Oviedo t. II p. 300 (imagen): «É haçen á su semejança
     una figura de madera de relieve y pequeña». La ponen bajo la hamaca del
     díao **desde el día en que muere** y la queman con él cuando, años
     después, se quema el cuerpo para beber los huesos («hasta que le queman,
     como es dicho»).
   - *Lado taíno*, Las Casas p. 321 (imagen), copiando **una carta de Colón**
     y no a Pané: estatuas de madera huecas, «donde metian los huesos de sus
     padres … y éstas llamaban del nombre de la persona cuyos huesos allí
     encerraban». Pané cap. XV da los cemíes con huesos.
   - *Lo que sale:* misma clase de objeto y destino opuesto. Es lo único de la
     lista de Steward que sobrevive con primaria en las dos orillas. Y
     contradice que la disolución del muerto (creencia-010d) sea arahuaca
     general: el taíno conserva al muerto nombrado. Va como `lectura`
     (ct-t01), y la efigie caquetía como `atestiguado` (ct-c01).

2. **Oviedo no calcó el texto, pero sí el marco.**
   - *Lo medido:* el capítulo venezolano comparte con el de La Española lo
     mismo que el de los piaches caribes de Camanagoto (`meta.medido`).
   - *Lo que se comparte* es marco y fórmula:
     - Plinio sobre la medicina y el arte mágico, alegado **tres veces**,
       para los buhitís (t. I p. 126), para los piaches (t. II p. 255) y para
       los boratios (t. II p. 299, «que se alegó por mí en el preçedente
       libro», que es el XXIV).
     - La escena del especialista encerrado que consulta al diablo sobre la
       lluvia y la guerra, que aparece en las tres orillas (t. I pp. 138-139;
       t. II pp. 255 y 298).
     - Las fórmulas «ahumadas que llaman tabacos» y «brasa sin llama» bajo
       la hamaca: la desecación del díao se cuenta con la frase con que Oviedo
       describe cómo se calienta un taíno en su hamaca (t. I p. 132).
   - *Consecuencia:* ningún rasgo de ese marco cuenta como semejanza entre el
     taíno y el caquetío. Lo que la plantilla de La Española **no** tenía —el
     funeral del díao, la cura paso a paso— es testimonio de la otra orilla.

3. **La cura tiene la misma secuencia en las dos orillas, y no es calco.**
   - *Lado caquetío*, Oviedo t. II p. 299 (imagen): el boratio, «con las
     manos çerrándolas é abriéndolas … como quien quiere juntar otra cosa,
     diçe que le allega el alma á un cabo, y despues çierra el puño y sóplale
     con la boca diçiendo: *Allá yras mal*»; luego chupa y enseña «la espina ó
     piedra ó palo».
   - *Lado taíno:*
     - Pané, cap. XVI: tira, va a la puerta, despide el mal con un soplo
       «como si despidiese una paja».
     - Anglería p. 351 (imagen): «con ellas así juntas sale corriendo á la
       puerta … y abriendo las manos las sacude».
     - Las Casas p. 535 (imagen), por su cuenta: «con aquel estregar y soplar
       echasen el mal fuera».
   - *Por qué no es calco:* Oviedo no tenía esta secuencia en su buhití, que
     es sólo herbolario (t. I p. 126).
   - *Por qué no prueba filiación:* las piezas son regionales. Los pemenos de
     la laguna curaban con «bramar y soplar y echar taco» (t. II p. 293,
     imagen).
   - *Dos cosas más:* es la primera vez que el corpus tendría al **alma** en
     la cura caquetía atestiguada (ct-c02), y la cura no está como hecho en
     `creencia.yaml`.

### El resto, en una línea cada uno (detalle en la propuesta)

- **Beber los huesos no es taíno.** Ninguna de las cuatro primarias lo trae:
  el cacique se entierra (Oviedo t. I p. 134; Las Casas p. 535). Oviedo mismo
  hace del endocanibalismo de los huesos una costumbre de Tierra Firme, «en
  esta Tierra-Firme … muchos las tragan» (t. II p. 297, imagen). Va en
  ct-t02.
- **Los muertos de noche tienen dos testigos independientes.** Pané y Anglería
  dan los caminos, el ombligo y el miedo que enferma («muchos enferman y se
  quedan lelos», p. 349, imagen); Las Casas, por su cuenta, «el gran miedo que
  tenian de los fantasmas de noche … hupías» (p. 535). Con el wayuu son dos
  tradiciones (ct-t04).
- **La tierra de los muertos con nombre, en un extremo, donde la vida sigue.**
  `Coaibai`, «en un extremo de la isla, llamado Soraya». Con Jepira son dos
  tradiciones, y el núcleo de creencia-009 queda `reconstruido` (ct-t05). La
  voz caquetía, `sawaka`, dice **abajo**: el contraste se conserva.
- **Los dos nombres del alma no se sostienen.** Pané da `goeiz` y `opia`, pero
  Las Casas, por su cuenta, da una sola palabra, `hupía`, «el ánima»: en duda,
  `hipotetico` (ct-t06). Lo que sí autoriza es **declarar el hueco**: no hay
  voz caquetía para el muerto que vuelve.
- **El poder sobre la lluvia, en dos sitios distintos.** El taíno lo pone en
  cemíes que posee el cacique: Pané, en cuatro cadenas, y Las Casas preguntando
  él mismo, p. 445. El caquetío lo pone en la persona del señor (creencia-013).
  Ojo con un detalle: la lluvia de Boinayol y Maroya sólo está en Wikisource,
  porque Anglería da la cueva por el sol y la luna (p. 347, imagen). Va en
  ct-t11.
- **El señor que adivina el primero** está en las cuatro cadenas y en Las
  Casas de vista. Pero en la única primaria caquetía de rito el oráculo es el
  **boratio** de cada pueblo, y el díao es otro (ct-t12, ct-c03). Esto deja
  más sola la mitad religiosa de creencia-001b.
- **La cohoba es polvo en todas las fuentes menos en Oviedo**, que la hace
  humo. El contraste «el caquetío fuma, el taíno aspira» descansa, del lado
  caquetío, en el único cronista que se equivocó con el lado taíno (ct-t13).
- **Ninguna venganza contra el médico en lo caquetío.** El boratio que no cura
  se va con su excusa del diablo (ct-t10).

## 3. Qué no se encontró (regla 6: con su sonda)

- **Desecación del cacique taíno, o çemi con huesos, en Oviedo t. I:** cero,
  con las sondas `huess-`, `enxug-`, `brasa` y `enterr-` sobre el tomo entero.
  Los únicos huesos de un señor son de Cozumel (p. 506) y los cuerpos «asados
  en barbacoa» son de la Florida (p. 561).
- **La primaria de Rouse p. 532 no está en el repo.** Rouse dice que al cacique
  se lo «dried over the fire» y que las cabezas se guardaban en cestas. Cero
  en Oviedo t. I, Pané-Wikisource, Las Casas, Anglería (vol. 1 y 4), Colón
  vol. 2 y Navarrete t. I. La candidata, sin verificar, es la relación del
  Almirante en el vol. 1 de la *Historia* de 1892 (B3).
- **Adivinación con tabaco en las fuentes taínas:** cero. La de Steward es
  sólo caquetía y doméstica.
- **En el lib. XXV de Oviedo:** `çemi`, `areyto` y `duho` dan cero, y «como en
  esta isla» también.
- **`sueñ-` en Pané-Wikisource:** cero.

## 4. Correcciones a la nota de decisión

- **El cap. IX no es del obispo Bastidas.** No declara informante (cero de
  «informado», «voce viva» o de testigos en las pp. 297-301). Bastidas es el
  informante del cap. XXII (p. 328).
- **El desfase de las dos ediciones de Oviedo va uno por delante** si el pdf
  se cuenta desde 1 (ver la tabla del §1).
- **Las Casas no saca de Pané los cemíes con huesos.** Los saca de una
  **carta de Colón** (p. 321), con dos detalles que Pané no trae: el nombre
  del muerto y la estatua que habla.
- **La p. 535 de Las Casas es del cap. CCIV**, «De la Medicina practicada en
  la isla Española», que empieza en la p. 534. No es del CCIII, como dice
  `6-fusion/taino2_las_casas_apologetica.yaml` (i04).
- **Colón 1892 vol. 2 no trae los caps. XI-XVII de Pané**, sólo del XIX en
  adelante. Para P1, P3 y P5 la tercera cadena es Anglería, no Colón.
- **Lo que Steward llama «resemblances» en el sacrificio y el adoratorio es
  axagua** (ya lo había medido `6-fusion/hsai_caquetios_2026-09-23.yaml`). Y Steward mismo, en la p. 24,
  niega el sacrificio humano a los arahuacos de las Antillas.

## 5. Cuánto queda

- **Leído:** el encargo A1-A3 entero, sin descargas.
- **Lo que pide descarga (D3 de la nota de decisión):**
  - B3, la *Historia del Almirante* vol. 1. Es la única que puede dar la
    desecación del cacique taíno: si aparece, el paralelo r3 pasa de «imagen»
    a «imagen + desecación».
  - B1, Bourne 1906, como control del cotejo.
  - B2, Ulloa 1571, para la `opia` frente a la `hupía` sin la retraducción.
- **Lo que pide préstamo o compra:** Oliver 2009 (C1).
- **Lo que pide fusión (ya lo pedía T6):** la efigie (ct-c01), la cura y la
  consulta del boratio (ct-c02, ct-c03) y partir creencia-001b.

## Decisiones para Miguel

- **D-t1 — Fusionar el lado caquetío:** ct-c01 (la efigie), ct-c02 (la cura,
  con el alma) y ct-c03 (la consulta). Los tres son Oviedo directo y
  `atestiguado`.
- **D-t2 — Las capas de los hechos taínos:**
  - `lectura`: ct-t01, 02, 03, 04, 07, 08, 11, 12 y 14;
  - `reconstruido`: ct-t05;
  - `hipotetico`: ct-t06;
  - `no-se-propone`: ct-t09, 10 y 13.

  La cuenta la imprime el script.
- **D-t3 — Bajar B3** para cerrar la desecación del cacique taíno.

---

## Auditoría de la Vía A

Una línea por hecho wayuu (y vecino) de la Vía A. **Corrobora**, **contradice**
o **no toca**, con la cita. El hecho de la propuesta que lo sostiene va entre
paréntesis.

| id | Veredicto | Cita |
|---|---|---|
| creencia-002 | **corrobora en parte** | El trance en que un espíritu revela la causa del mal: Pané cap. XV, Anglería p. 350, Las Casas p. 323, y el boratio, «porque el diablo me lo ha dicho assi» (Oviedo t. II p. 299). El **sueño** como medio, no: `sueñ-` = 0 en Pané (ct-t07) |
| creencia-003 | **corrobora en parte** | Casa vaciada y cerrada para curar, y canto: Pané cap. XVI; Anglería p. 350, «echan del hemiciclo á todos, excepto uno ó dos». Tabaco **fumado** del especialista caquetío: Oviedo t. II p. 298. La serpiente auxiliar tiene eco de una sola cadena (Pané cap. XVIII). No toca urari ni licor. Aviso: su `reconstruido` descansa en vecinos **no** arahuacos (ayomán, timote) (ct-t08, ct-t10, ct-c03) |
| creencia-005 | **no toca** | El alma taína se aparece de noche (Pané cap. XIII, `goeiz`; Las Casas p. 535, `hupía`), pero ninguna fuente la hace viajar en el sueño (ct-t06) |
| creencia-006 | **contradice** (como etiología única) | En lo taíno el mal es intrusión o envío del cemí desatendido (Pané caps. XVI y XX; Anglería pp. 351-352), no alma perdida. Del lado caquetío, el boratio «le allega el alma á un cabo» antes de soplar el mal (Oviedo t. II p. 299): un ancla atestiguada pero ambigua (ct-t09, ct-c02) |
| creencia-007 | **corrobora en parte** | Hay males que manda un espíritu y exigen al especialista (Pané caps. XVI y XX; Anglería p. 352), y el buhití es a la vez herbolario y adivino (Oviedo t. I p. 126). El principio de semejanza no aparece (ct-t09) |
| creencia-008 | **corrobora** | «El gran miedo que tenian de los fantasmas de noche» (Las Casas p. 535, testigo propio); los muertos en los caminos y el miedo que enferma (Pané, proemio y cap. XIII; Anglería p. 349). Con el wayuu son dos tradiciones. La ambivalencia —el muerto antiguo que protege— no la da el taíno (ct-t04, ct-t14) |
| creencia-009 | **corrobora** | `Coaibai`, «en un extremo de la isla, llamado Soraya», donde los muertos comen y yacen (Pané caps. XII-XIII; Anglería p. 348, sin el nombre). Con Jepira son dos tradiciones. Se conserva el contraste con creencia-028, «abajo» (ct-t05) |
| creencia-010d | **contradice** la generalización | El taíno **conserva** al muerto principal, con su nombre, dentro de una estatua de madera (Las Casas p. 321, carta de Colón; Pané cap. XV). La disolución en el colectivo es caquetía y wayuu, no arahuaca general (ct-t01, ct-t02, ct-c01) |
| creencia-011 | **no toca** | Ninguna fuente taína dice quién manipula los huesos ni sus tabúes. Y del lado caquetío, quien cuida el cuerpo del díao es «su hijo y subçessor en el Estado» (Oviedo t. II p. 300), no una mujer o una anciana (ct-c01) |
| creencia-012 | **no corrobora** | Pané cap. XV pone los cemíes con huesos y los que hacen llover como clases distintas. Ninguna fuente taína enlaza los huesos con la lluvia (ct-t11) |

Fuera de la Vía A quedan creencia-008b y 008c, que son atestiguados (Arcaya),
no wayuu. ct-t04 entra como `lectura` de 008b, y ct-t12 deja más sola la
mitad religiosa de creencia-001b.
