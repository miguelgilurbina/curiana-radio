# M5 — Los vocabularios antillanos que quedaron a medias

**Tercera campaña de minería, parcela M5. 2026-09-22/23.** Rama
`campana/mineria3-vocabularios`. PROPUESTA (regla 5): nada de esto toca el canon.
Fuentes: Goeje 1939 (el kalinago), Bachiller 1883 (Rafinesque, eyeri, su Pané),
Coll y Toste (los dos vocabularios), Pichardo 1862 (sólo OCR).

---

## Lo que de este encargo resultó falso al medirlo

| Lo que se daba por hecho | Lo medido |
|---|---|
| (T10, ayer) «`piragua`: Rafinesque vía Bachiller la marca **eyeri**» — el tercer apoyo para sacarla del taíno | **Falso.** En la imagen de p. 389: «Bote, *Piraguas*, **B.**» y «Bote, *Canoa*, *Payes*, **E.**». El bloque «eyeri» lleva DOS marcas; la `B.` (no definida, por el contenido Borinquen) es taíno/castellano. Rafinesque pone `piragua` en Borinquen y `canoa` en el eyeri. Quedan dos apoyos, no tres |
| (T10) «`Ditaino` aparece también en la lista eyeri» | **Falso**: «Noble, *Ditaino*, **B.**» |
| (T10) «Perro *Aleo*», «Gusano *casi*», «Opoyem», «Quinaxes = C; Hutía = L» | `Alco`, `cusi`, `Opoyun`; y la marca C. cubre `Usias`, `Hutia` y `Quinaxes`: `hutia` es de Cuba **y** de las Lucayas en esa lista |
| (ficha) Coll y Toste «es el original de 1897» | **No.** El escaneo es la **2.ª edición** (Isabel Cuchí Coll, Bilbao, Editorial Vasco Americana, s. f., «todos los derechos reservados»), con apéndice del Instituto de Cultura Puertorriqueña (fundado en 1955); el texto cita obras de 1907. 1897 es la fecha del premio. Las páginas citadas son las de esa edición |
| (T10) «luaidanga» 'calabaza' en el «dialecte de Aruba» | **`waidanga`** (imagen, p. 15): la `w` cursiva sale `lu` en el OCR |
| (encargo) «el dialecte de Aruba que Goeje cita dos veces sin decir de dónde sale» | Sale de **Pinart (1882) vía Gatschet (1885)**, que el repo ya tiene: `waidanga` 'water-gourd' y `hanahana` 'Formica cephalota' (Goeje imprime `hanuhana`), y Goeje pone el arubano justo en la entrada donde Gatschet lo compara con el caribe insular `hage`. Y no son dos citas insulares sino **cuatro**: también `chogogo` (Bonaire, flamenco, p. 60) y `ayaka` (papiamento de Curaçao, p. 115) |

---

## El veredicto en una frase

**De las 23 voces kalinago del lexicón, Goeje sostiene 11, emparienta 4 y no da
8 —y esas 8 son casi todas la voz taína o lokono del concepto con la etiqueta
cambiada—; la lista maestra taína pasa de 263 a 1.039 voces y los conceptos
comparables con el caquetío atestiguado de 12 a 30, pero al leerlos, de los 18
nuevos sólo 12 son pares de concepto y 11 de ellos descansan en una sola obra
sin cronista (Coll y Toste, cap. X).**

---

## Las cifras, y de dónde salen

Todas las emite `6-fusion/scripts/consolidar_taino.py --check` sobre
`6-fusion/taino_lista_maestra_2026-09-22.yaml` (regenerada), salvo donde se dice.

| Cifra | T10 (ayer) | Ahora | De dónde |
|---|---|---|---|
| voces taínas distintas | 263 | **1.039** | §resumen — la mayor parte la aporta Coll y Toste (1.025 registros: 721 del cap. XII + 304 del cap. X) |
| clase (i) primaria del XVI | 172 | **366** | §resumen.por_clase |
| clase (ii) sólo secundaria | 77 | **573** | ídem |
| clase (iii) conjetura → no entra | 14 | **100** | ídem (conjeturas de Coll y Toste: «radical», «significa»…) |
| con 2+ cronistas independientes | 22 | **95** | ídem |
| sacadas del taíno por alguna fuente | 22 | **80** | ídem |
| las 52 claves taínas del lexicón con cronista | 41 | 41 | §las_52 — no se mueve |
| conceptos comparables con el caquetío atestiguado | 12 | **30** | §conceptos_comparables (misma `conceptos()` que el cruce) |
| claves kalinago del lexicón cruzadas con Goeje | 0 | **23 de 23** | §kalinago_de_goeje |
| … con apoyo / parcial / sin apoyo | — | **11 / 4 / 8** | ídem (veredictos leídos en imagen en `kalinago_goeje_1939.yaml` §cruce) |
| conceptos caquetíos atestiguados con voz kalinago transcrita | — | **10** (suelo) | ídem |

### Los 18 conceptos que añade esta parcela, leídos uno a uno (lectura a mano, no cifra del script)

- **Pares de concepto (12):** `sol` (Coll: *Guey*), `luna` (Coll: *Caraya*; y
  *Mona* eyeri, sacada), `hombre` (*Guacokío*), `mujer` (*Guarique*), `hijo`
  (*Guaili*; y *guali* con Pané detrás), `grande` (*Ma*), `lugar` (*Yara*),
  `lagartija`, `serpiente` (*Jubo*), `cotorra` (*Xaxabi*), `médico` y `diablo`
  (*Mabuya*, que es eyeri: sacada del taíno). **Once de los doce sólo los
  sostiene el cap. X de Coll y Toste**, clase (ii), sin cronista por entrada.
- **Artefactos del instrumento (6):** `árbol`, `insecto`, `pez`, `ave` (un
  hipónimo glosado con su clase: «*Yaba*. — Árbol (*Andira inermis*)» no es la
  palabra 'árbol'); `río` (colisión de lema `agua`/`jagua` — y el «Río, *Agua*»
  de Rafinesque es castellano, lo dice Bachiller); `pantano` (entrada fundida por
  el OCR de Coll y Toste). **Hay que corregirlos antes de re-correr el cruce.**

---

## 🔴 Lo que más mueve

### 1. El kalinago del lexicón: 8 de 23 sin apoyo en Goeje, y es un patrón

`kasabi`, `yuka`, `hamaka`, `ikoa` (~ LK *sikoa*), `kasaku` (~ LK *kassaku*),
`pira`, `baruwa`, `amourou`: Goeje da el concepto con OTRA voz (el casabe es
*aleiba*/*ereba*; la yuca *kiere*/*key*; la hamaca *akat*/*ekera*; la casa
*mana*, *ubana*, *obogne*…; el pez *aoto*; la guerra *ualime*). Es el mismo
patrón que la primera campaña encontró en las nueve «taíno-reconstruido»: una
lengua vecina con la etiqueta cambiada. Detalle, página y forma en
`6-fusion/kalinago_goeje_1939.yaml` §cruce_con_el_lexicon.

### 2. El lexicón no dice el registro, y el registro es lo que define al kalinago

`kati` 'luna', `marisi`, `hiñaru` son de **mujeres** (arahuacas); `barana`,
`Kalinago` de **hombres** (y Goeje da `barana` de origen KALINA/tupí —*parana*—,
no arahuaco: la arahuaca es la de mujeres, `balaua` ~ A *bara*). Y `hiñaru`
está **mal glosada**: Goeje la da como 'mujer' (habla de mujeres), no 'persona'.
El par real de Goeje es *uekeli*/*eyeri* 'hombre' y *uele*/*inharu* 'mujer';
`baruwa` no aparece.

### 3. `duna`: la nota del lexicón atribuye `tuna` al lokono; Goeje, a los kalina

«eau, rivière *tonê, tona*, … K *tuna*, 5, 6 *duna*» (sigla K) — y en la misma
página el agua arawak es *wuini*. `duna` es garífuna; el caribe insular antiguo
dice *tona*.

### 4. Sol y luna: la pareja caquetía atestiguada está en la esfera

En habla de mujeres kalinago el sol es **`kaši`** y la luna **`kati`**, las dos
con la sigla arahuaca 1 am 62 (Goeje p. 54, verificado en imagen); el eyeri de
Rafinesque (Bachiller p. 389) trae *Kachi* 'sol' y *Kati* 'luna', que son las
mismas vía Rochefort. El caquetío atestiguado tiene `kasi` 'sol' y `kati`
'luna'. Comparandum de esfera, no propuesta: no mueve glosas.

### 5. El «eyeri» de Rafinesque es el habla de mujeres del caribe insular

Cruzado voz a voz con Goeje: *Eyeri* 'hombre', *Inara* 'mujer', *Kati*,
*Kachi*, *Ubec* 'cielo', *Nekera* 'cama' (~ *ekera* 'hamaca'), *Boyez*,
*Tuhonoco* 'casa' (~ *ubonoko*). La cabecera de Bachiller («dialecto de las
mujeres caribes») acierta; lo único falso es «de Borinquen».

### 6. La Pané de Bachiller no es un testigo de Pané

`6-fusion/taino3_pane_bachiller_cotejo.yaml` (script `cotejar_pane_bachiller.py`):
de 49 formas de Pané, 19 iguales, 10 variantes, 8 ausentes y **12 restituidas**
por Bachiller — y en dos lo declara él: pone *guanaba* «así lo dice Pedro
Mártir» donde su texto dice *guabasa*, y *Epilegaaanita* donde el texto dice
*Opigielqaouiran* («visible errata»). Su declaración de método (p. 166) nombra a
Oviedo, Mártir, **Rafinesque** y Brasseur como fuentes de la restitución. Donde
difiere de Wikisource, la forma no es de Pané: es de Mártir o de Rafinesque.
`daca`: Bachiller escribe «*Dio Aboriadacha*» (p. 182).

### 7. `chogogo` (Bonaire) es caribe según Goeje

«flamant *tuguku*, K *tokoko*, dialecte de Bonaire *chogogo*» (sigla K). Van
Buurt 2014 lo tiene como voz caquetía del papiamento. Si Goeje tiene razón, el
flamenco de las islas caquetías lleva nombre caribe.

---

## Lo que NO se encontró / no se hizo

- **El vocabulario kalinago de Goeje, transcrito a medias**: 859 entradas en pp.
  31-34, 44-48, 68-69, 85-93 y 102 (cinco escribas cortados por el límite de
  uso; sus tramos están medidos en el YAML). **Sin transcribir**: pp. 35-43,
  49-67 (incluidos ANIMALES y plantas), 70-84, 94-101 y 103-118. Las líneas que
  el cruce necesitó de esas páginas se leyeron en imagen.
- **La fuente del «dialecte de Bonaire»**: Goeje no la da; 0 en Gatschet y 0 en
  su bibliografía.
- **Pichardo: sin minar.** Sí queda hecho el OCR propio con tesseract (1,23 MB,
  314 pp., columnas separadas, desfase impresa = pdf − 26 medido en dos puntos):
  `Voz ind` 386 veces; `Las Casas` 28, `Herrera` 22, `Oviedo` 17, `Enciso` 4.
  ⚠️ `taita` da 0 en este OCR y 4 en el de archive.org: el OCR nuevo pierde
  alguna cabeza en negrita; no sustituye al viejo, lo acompaña.
- **Coll y Toste, transcrito AUTOMÁTICAMENTE**: 721 entradas del cap. XII y 304
  del cap. X, con página, autoridades y tipo de apoyo por regla. De una muestra
  aleatoria de 20 (semilla 20260922), 19 cotejadas en imagen: cabeza y página
  bien en 17; dos errores (una entrada fundida con la siguiente por el OCR,
  `Macuaque`+`Macorí`; y una cita de Las Casas perdida en el margen, `Yaque`,
  que por eso sale «sin fuente»); y una clasificación discutible (`Tingüíbi`:
  «parece» la marca como conjetura). La sección I está dañada en el OCR. Es
  material para buscar, no para citar sin ver la imagen.

---

## Opciones para Miguel

### A — Citas y registro para el kalinago (no toca el motor)

Poner `procedencia.obra: goeje-1939` con página a las 11 voces con apoyo, y el
registro (hombres/mujeres) en `notas`. Fundir `kalinagu`/`kalínagu`.

### B — A, más curar las 8 sin apoyo y la glosa de `hiñaru`

Las 8 a `deuda: sin-procedencia` (o buscarles Breton 1665 directo) y `hiñaru`
→ 'mujer'. Si alguna está entre las candidatas de `[Voces de fuera]`, el prompt
cambia: se mide antes.

### C — Corregir la etiqueta de T10 sobre `piragua` antes de la tanda A de T10

La opción A de T10 mandaba `piragua` al kalinago con «tres fuentes»; ahora son
dos. Sigue siendo la peor sostenida de las 52, pero la decisión ya no es por
unanimidad.

### D — Re-correr el cruce taíno↔caquetío con la lista maestra

Sólo después de quitar los seis artefactos (§ «Los 18 conceptos»): con ellos,
el 30 promete más de lo que hay.

**Recomendación del minador: A y C ya; B después de medir `[Voces de fuera]`;
D no antes de limpiar los artefactos.**

---

## Lo que vi de paso y merece otra campaña

- **Breton 1665-66 directo** (el diccionario caribe-francés): es la fuente de
  casi todo el kalinago antiguo de Goeje y la única forma de cerrar las 8 sin
  apoyo. Está en facsímil de 1892/1900 (dominio público).
- **El vocabulario de animales kalinago (Goeje pp. 58-62)** quedó sin
  transcribir: es el tramo que más les sirve a los agentes de fauna.
- **Pichardo** tiene 386 «Voz ind.»; separar las que citan cronista (Las
  Casas 28, Herrera 22, Oviedo 17) de las que no, es una sesión.
- Coll y Toste cita el **Informe de 1582** (Santa Clara y Ponce de León) y el
  **Repartimiento de 1514** para cientos de topónimos y caciques: documentos de
  época que podrían subir voces de clase (ii) a (i) si el repo los tuviera.
