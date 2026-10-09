---
tipo: fuente
obra: "Histoire générale des Antilles habitées par les François, tome II: contenant l'histoire naturelle"
autor: "Du Tertre, Jean-Baptiste"
anio: 1667
publicacion: "París, Thomas Iolly, 1667-1671, 4 tomos. El t. II (1667) contiene la historia natural y el «Traité des Sauvages» (los caribes)"
edicion_del_ejemplar: "ejemplar de la Wellcome Collection en archive.org (b33275944_0002, metadato «Vol. 2»). Las seis copias JCB histoiregenerale00dute_0 a _5 no dicen en sus metadatos qué tomo son"
genero: cronica
local:
  - "fuentes_caquetios/DuTertre_1667_Histoire_Generale_Antilles_t2.txt"
paginas: "610 pp. de PDF (en el PDF en línea). Desfase pdf→impresa NO constante por las láminas: −28 (pdf 100 = p. 72), −48 (pdf 300 = p. 252), −64 (pdf 560 = p. 496): leer el número impreso. Las pp. 365-366 (la iniciación del boyé que cita Rouse) caen hacia pdf 415-420"
capa_texto: si
estado_minado: minado-parcial
descargado: 2026-10-09
origen_digital: "Internet Archive — https://archive.org/details/b33275944_0002 (_djvu.txt del ítem; el PDF se midió y no se guardó en git por su peso)"
acceso: >-
  Dominio público (1667). Descargado el 2026-10-09 con la autorización de
  Miguel. Sólo el TXT va a git: 1.102.497 bytes, sha256
  71c211ec81d557d832d35dd393db41d6a173ed0263000d406afa5201dde169ae.
  El PDF (236.194.737 bytes, sha256
  beaf57df47fa5b154c40dbd79a5cb6899301439517ace6fb7f3252b2a51846cc) se bajó
  para medir el desfase y se borró del scratchpad: PDF SOLO EN ONEDRIVE, no en
  git (D8), si Miguel lo baja de
  https://archive.org/download/b33275944_0002/b33275944_0002.pdf
prioridad: media
sostiene: {hechos_corpus: 0, entradas_lexicon: 0}
verificado: 2026-10-09
propuesto_por: "nota de decisión 08_creencia_kalinago_que-minar (K2)"
aliases: ["Du Tertre 1667", "Du Tertre t. II", "Histoire générale des Antilles", "du-tertre-1667"]
minado: 2026-10-09
cobertura: "2026-10-09 (minería 2, esferas kalinago): traité VII cap. I (pp. 356-418) entero en el OCR; 22 páginas en imagen en el visor de archive.org (lista en la propuesta). Sin leer: traités I-VI y VIII, cap. II del VII"
---

# Du Tertre 1667, t. II — el tratado de los «sauvages»

> **Qué es.** El dominico Jean-Baptiste Du Tertre fue misionero en Guadalupe,
> **compañero de misión de Breton**. Su tomo II trae, tras la historia
> natural, el *Traité des Sauvages*: los caribes insulares por dentro — el
> boyé y su iniciación (pp. 365-366, la cita que Rouse 1948 le atribuye), los
> funerales, los huesos guardados, lo que no se nombra. Es la fuente de la que
> **Rochefort copió** (edición de 1654) y comparte misión con Breton: los tres
> no son testigos independientes.

## Qué preguntarle

De [[08_creencia_kalinago_que-minar]] (Minería 3) y [[09_creencia_kalinago_mineria]]:

1. **¿Sostiene Du Tertre lo que Rouse le atribuye?** La iniciación del boyé
   (pp. 365-366; P5), los huesos guardados por el boyé, las cenizas del jefe,
   «no nombrar al muerto», el funeral en dos tiempos.
2. **¿Es opoyem el alma del muerto?** (lo que Breton deja en duda).
3. **Independencia.** Du Tertre y Breton compartieron misión: lo que repite a
   Breton no suma testigo; lo que sólo él trae, sí. Separar en cada hecho el
   sustrato arahuaco (comparable al caquetío) de la capa caribe, como en Breton.

## Cómo se lee

- Sólo hay texto en el repo (OCR de archive.org del francés del XVII: ſ
  larga, u/v, láminas que rompen la numeración). Sirve para localizar; las
  citas se leen en imagen desde el PDF en línea (`leer-fuente`, §5): abrir
  `https://archive.org/details/b33275944_0002/page/n<pdf-1>` con el número de
  página del PDF.
- Para ir de página impresa a PDF, sumar ~48-64 según el tramo (ver
  `paginas:`): comprobar siempre la cabecera.

## Estado

Medido al descargar el 2026-10-09; leído el mismo día por la minería 2 de las hermanas (sección «Minería 2 — esferas», abajo). Entró el 2026-10-09 con la tanda de
descargas de la campaña de creencia.

## Minería 2 — esferas (2026-10-09)

**Se preguntó** lo del encargo de las hermanas (las cinco esferas, tema por
tema del README §4) y lo de la minería 1 que esperaba a este tomo: ¿sostiene
Du Tertre lo que Rouse le atribuye —la iniciación de cinco meses (pp.
365-366), los huesos guardados, las cenizas, «no nombrar al muerto»? ¿Es
opoyem el alma del muerto? Sesión: [[10_hermanas_kalinago_esferas]].
Propuesta: `6-fusion/hermanas_kalinago_2026-10-09.yaml`.

**Cómo.** El traité VII, cap. I (pp. 356-418) se leyó entero en el OCR del
repo y se citó desde el **visor de archive.org** (la página en imagen, sin
bajar el libro), 22 páginas. **Desfase en línea: impresa = n − 57** de p. 360
a p. 393 (n417-n450); tras la lámina «Visite des Sauvages aux François» (dos
escaneos), **impresa = n − 59** desde p. 395 (n454) a p. 412 (n471). La
cabecera «397» que el OCR lee en el arranque de «Des Carbets» es la p. 395 (lo
confirma la tabla del tomo). Lo no visto se cita con `verificado_en_imagen:
no`.

**Qué es, comprobado.** Du Tertre y Breton no son dos testigos: en p. 361
Du Tertre copia a Breton 1665 pp. 229-230 «Voicy ses propres paroles»; las
anécdotas de la sesión del boyé, la lucha y el caso de brujería son de Breton
(«Nostre Pere Raymond en a veu un»). Sus informantes propios: el frère
Charles (Dominica), du Parquet (Martinica) y «un jeune homme, qui avoit esté
long temps esclave parmi eux». Y contesta a Rochefort en varios sitios.

| Dato | Página | Tema | Etiqueta | Sustrato |
|---|---|---|---|---|
| El primer padre Kalinago, envenenado por sus hijos, hecho pez Atraioman | p. 360 | cosmos-origen | atestiguado | caribe |
| Cita a Breton: Callinago, la conquista, «à la reserve des femmes»; los reyes y los abouyou; las cabezas en las cuevas para mostrarlas a los hijos | p. 361 | lengua-registro, sucesion-politica, narracion-mito | atestiguado (copia) | arahuaco / caribe |
| «combatre les Ygneris, qui estoient les naturels du pays»; los Igneri que quedaban en las montañas de Guadalupe eran esclavos arahuacos huidos | pp. 361-362 | lengua-registro | atestiguado | arahuaco |
| Iniciación del boyé: «apres avoir long temps jeûné» (sin «cinq mois»); el dios de un tal, la diosa de una tal | pp. 365-366 | iniciacion-especialista, espiritu-tutelar | atestiguado | arahuaco |
| El dios Yris heredado del padre; el viaje por encima del sol | p. 366 | espiritu-tutelar | atestiguado | sin decidir |
| La cura: palpar, soplar, sacar espinas y huesecillos, chupar; festín «Ichéiry»; genipa | pp. 367-368 | enfermedad-cura | atestiguado | arahuaco |
| Huesos de un muerto sacados del sepulcro, envueltos en algodón: «c'est l'ame du mort qui parle»; brujería con ellos | p. 369 | segundo-entierro | atestiguado | arahuaco |
| Marmousets de algodón echados al mar antes de viajar | p. 369 | especialista | atestiguado | sin decidir |
| Ídolos de algodón en cuevas de Martinica: «les Dieux des Ygneris» | pp. 369-370 | lugar-sagrado | atestiguado | arahuaco |
| Eclipse y danza; ayunos; tabúes de comida; primos hijos de dos hermanos = hermanos; sin apellidos | p. 371 | tiempo-calendario, tabu, descendencia | atestiguado | sin decidir |
| Tres almas: corazón (al cielo), cabeza y brazo (se vuelven Maboyas) | p. 372 | alma | atestiguado | sin decidir |
| La covada de cuarenta días | pp. 372-374 | infancia-nombre | atestiguado | arahuaco |
| Custodia materna; varones con el padre, niñas con la madre; qué se enseña; pubertad | p. 376 | descendencia, curriculo-edad | atestiguado | arahuaco |
| El rito del Mancefenil; las «Cousines germaines qui décendent de ligne feminine» | p. 377 | curriculo-edad, matrimonio | atestiguado | caribe / sin decidir |
| **Residencia**: la novia va a casa del capitán; el yerno común va a casa del suegro; evitación de los suegros; poliginia | p. 378 | residencia, matrimonio | atestiguado | arahuaco |
| Trabajo de las mujeres; «une infamie à un homme d'avoir touché le travail d'une femme»; corrige a Rochefort | p. 383 | roles-de-genero | atestiguado | sin decidir |
| Sin comercio entre ellos; lo que cambian con los franceses; piedras verdes | pp. 383-385 | alianza-intercambio, comercio-rutas | atestiguado (capa de texto) | sin decidir |
| Caracolis: «or de bas aloy», de los Alloüagues por socios de intercambio; de tierra firme | p. 393 | alianza-intercambio | atestiguado | arahuaco |
| El caserío de familia; el carbet y su puerta del espíritu | pp. 395-396 | hogar-casa, sociedades-masculinas | atestiguado | sin decidir |
| Piraguas, canoas, navegación por estrellas | pp. 398-399 | navegacion | atestiguado | sin decidir |
| Tres clases de capitán; nunca jóvenes; poder sólo en la guerra; «Caciques» desconocido | pp. 399-400 | jefatura, sucesion-politica | atestiguado | caribe |
| Consejo de guerra: las viejas y la arenga que mujeres y niños no entienden | p. 401 | guerra, lengua-registro | atestiguado | caribe |
| Entierro de un niño visto; luto de un año; esclavos del muerto | pp. 411-412 | muerte-entierro | atestiguado | arahuaco / sin decidir |

**No dio** (`meta.ceros`): «cinq mois» 0 (y p. 365 en imagen dice «long
temps»); cenizas del muerto 0; «no nombrar al muerto» 0 (sí «point de
surnoms»); huesos de antepasados guardados en casa en calabazas 0 (es un
muerto, del sepulcro, en algodón); Louquo 0; tributo 0; el segundo tiempo
«au bout de l'an» de Breton no lo repite.

**Deuda.** El PDF no está en el repo (236 MB, sólo en línea): cada cita nueva
exige el visor. Sin leer: traités I-VI y VIII. Cotejar con la edición de 1654
(cihm_34860) qué es de 1654 y qué añadió en 1667.
