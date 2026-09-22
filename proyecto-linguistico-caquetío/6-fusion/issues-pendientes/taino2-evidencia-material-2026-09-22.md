# Sí hubo contacto, y no fue con el taíno: los caquetíos de Curazao llevan dos tercios de sangre antillana

**Segunda campaña del taíno, parcela T8 (la evidencia material: arqueología y
genética), 2026-09-22.** Encargo de Miguel: *«Ve avanzando con la búsqueda,
descarga y minado de fuentes para corroborar pre contacto con Taíno y minar más
info»*, sobre lo de la noche anterior: *«tiene que haber una forma de probar si
hubo algún tipo de contacto. O sea de que es plausible es plausible.»*

**Ninguna cifra del lado del repo está escrita a mano.** Las imprime

```bash
python 6-fusion/scripts/medir_taino2_evidencia_material.py
python 6-fusion/scripts/medir_taino2_evidencia_material.py --json
```

Las cifras del lado de las fuentes son citas y llevan obra y página. Datos,
citas, descargas y propuestas en
`6-fusion/taino2_evidencia_material_contacto.yaml`.

---

## 0. Cinco cosas del encargo que resultaron falsas al medirlas

1. **«El punto de partida es la campaña 1, que concluyó "nada precolombino"».**
   Ese punto de partida **cae en su pieza central**. Fernandes et al. 2020 —la
   obra que la campaña 1 no pudo abrir porque el archivo estaba en 0 bytes—
   contiene ADN antiguo de **dos aldeas caquetías de Curazao**, y sus autores
   describen *«major gene flow from the Antilles that affected Curaçao»*. El
   cero de la campaña 1 era un cero de la **biblioteca**, no del registro.

2. **«Descarga Fernandes; es acceso abierto».** El texto sí es accesible (Europe
   PMC lo sirve como XML, y el suplemento entero está abierto en la web del
   laboratorio autor), pero **el PDF de PMC no se deja descargar** —devuelve una
   página «Preparing to download»— y la licencia **no es CC**: es la de Nature,
   que permite minar pero no redistribuir. El archivo de 0 bytes del repo
   **sigue en 0 bytes a propósito**; lo que entra es el preprint de bioRxiv, que
   sí es CC y **no es el mismo texto** (le falta justamente el suplemento donde
   está el hallazgo).

3. **«Nägele et al. 2020, versión en PubMed Central si la hay».** No la hay.
   Europe PMC: `isOpenAccess = N`, sin PMCID, «Subscription required». Anotada
   y no descargada.

4. **«Rouse y Cruxent 1963, descárgalo si está en archive.org en préstamo legal
   o en acceso abierto».** Está en dos ejemplares, los dos con
   `access-restricted-item: true` y en `inlibrary`/`printdisabled`: **préstamo
   digital controlado**, que no es descarga. No se bajó. El hueco de
   2026-07-29 sigue abierto y ahora se sabe que seguirá abierto hasta que
   alguien pida un préstamo o compre el libro.

5. **«Oliver 2000 … ¿de dónde del continente? ¿pasa la ruta por Falcón o por
   las ABC?»** El capítulo no tiene versión abierta y no se obtuvo, así que no
   se le atribuye nada. La pregunta sí tiene respuesta, por la arqueometalurgia
   que lo cita: el guanín cubano apunta a **Colombia** (tairona, zenú,
   nahuange) por argumento **iconográfico, no químico**, y ni Falcón ni las ABC
   aparecen en ningún punto de la ruta.

*(Y una sexta, menor: las dos obras que cerrarían la predicción de las piedras
verdes —Knaf et al. 2021 y Casale et al. 2024— **son CC-BY** y aun así Elsevier
y Wiley devuelven 403 a la descarga automática. Están localizadas, con DOI, y
con un navegador se abren.)*

---

## 1. El veredicto, en una frase

**Sí hay evidencia material de contacto precolombino entre la esfera caquetía y
las Antillas, y es genética: los enterrados en dos aldeas caquetías de Curazao,
fechadas 1160-1500 y 1443-1522 d.C., llevan ~dos tercios de ancestría de las
Antillas MENORES — pero esa misma fuente cierra la puerta del taíno, porque
dice expresamente que la ancestría se comparte con las Menores y no con las
Mayores.** El contacto existió; era por la cadena del sur, no con el taíno.

---

## 2. El hallazgo, con sus números y sus límites

De la *Supplementary Information* de Fernandes et al. 2020, SI2 «Curaçao»:

> «The individuals analysed for this study come from **two Caquetio
> settlements**, associated archaeologically with large quantities of
> Dabajuroid ceramics.»

- **De Savaan (C-0021)**: contexto **1160-1500 d.C.**, 14 tumbas recuperadas.
- **Santa Cruz (C-0004)**: contexto **1443-1522 d.C.**; los españoles lo
  reportaron como el pueblo de un cacique caquetío.

Y el modelo de ancestría (qpAdm):

| Modelo | Fuente antillana | Fuente continental | p |
|---|---|---|---|
| clados mayores | `*Caribbean_Ceramic` 68,0 ± 5,1 % | `*Venezuela_Ceramic` 32,0 ± 5,1 % | 0,298 |
| con competencia de modelos | `*LesserAntilles_Ceramic` **74,5 ± 3,7 %** | `*Venezuela_Ceramic` 25,5 ± 3,7 % | 0,362 |

El componente continental lo ligan a la llegada del dabajuroide hacia 500 d.C.;
el antillano, a algo posterior:

> «suggesting that there was **major gene flow from the Antilles** that affected
> Curaçao in the centuries after the arrival of Dabajuroid pottery. An important
> topic for future research will be to identify the **archaeological correlates**
> of these events.»

### Los cuatro límites, que no se pueden saltar

1. **Es de las Antillas MENORES.** El texto principal: la ancestría se comparte
   con las Antillas Menores *«but not the Greater Antilles»*. Las referencias
   del subclado son Anse à la Gourde (Guadalupe) y Lavoutte (Santa Lucía).
   ⚠️ Con un matiz que hay que degradar en duda: el modelo de grafo (qpGraph)
   dice que la mejor fuente es «una población **entre** las Mayores y las
   Menores». Las dos lecturas están en la misma obra.
2. **No hay fecha para la mezcla.** Los autores declaran que no pudieron
   obtener estimaciones viables para Curazao (sí para Haití: 16,5 ± 3,3
   generaciones). El evento cabe en cualquier punto entre c. 500 y c. 1300 d.C.
3. **La muestra es pequeña y el clado es marginal.** De Savaan y Santa Cruz
   forman clado entre sí sólo «marginally» (p = 0,011), y el número exacto de
   individuos está en un `.xlsx` que PMC no sirve — no se escribe a mano.
4. **No hay ni un objeto.** Los propios autores dejan por escrito que
   identificar el correlato arqueológico es tarea futura. Hoy hay huesos y no
   hay cacharros.

---

## 2 bis. El complemento etnohistórico: cruzar a las islas era un hábito

Esto no es evidencia material y no cuenta como una de las seis predicciones,
pero cambia cómo se lee el hallazgo. La carta de Ampíes al Rey, desde Santo
Domingo, finales de 1525 o principios de 1526 (Arcaya 1920, pp. 159-160,
publicada en Oviedo y Baños, ed. Fernández Duro, t. II, p. 209), dice tres
cosas verificadas hoy en el propio texto:

- en Curazao, Aruba y Bonaire había «hasta doscientas personas de todas
  edades»;
- los indios de la costa de enfrente —«desde Paraguachoa hasta la punta de
  Coquibacoa», nombrando **Sauca y Paraguaná**— «**muchas veces se pasaban
  allá a holgar con ellos**»;
- el cacique que le llevó la embajada, **don Juan Baracoica**, «está en las
  islas **y es su pariente y deudo**» — de Manaure.

Costa y ABC no eran dos orillas que se visitaban: eran **una sola comunidad
con parentesco**. Y si las islas eran el sitio al que la gente de la costa se
pasaba constantemente, y la gente enterrada allí lleva dos tercios de
ancestría de las Antillas Menores, entonces **las ABC son donde el continente
y la descendencia antillana convivían**. El puente no era un viaje raro; era
una casa compartida.

⚠️ **Dos cosas que esto no hace.** No salta a las Antillas Mayores: en la misma
carta, el único vínculo con La Española es la armada española que se llevó a la
hija de Manaure y la devolución que hizo Ampíes — contacto **colonial**, en
barco europeo. Y no fecha nada: es de 1525-26 y presenta la costumbre como ya
establecida, que es lo más que un documento de contacto puede hacer.
Proyectarlo al siglo XV es una decisión (regla 3), no una lectura.

---

## 3. La tabla de predicciones

| # | Predicción del encargo | ¿Vista? | Dónde | Fuerza |
|---|---|---|---|---|
| 1 | **Guanín**: ¿de dónde del continente, y pasa por Falcón o las ABC? | Parcialmente — llegó antes de 1492, pero **no por aquí** | Martinón-Torres et al. 2012, pp. 449 y 451 | media |
| 2 | **Piedras verdes**: ¿procedencia venezolana o guajira? | **No**, y la literatura ni lo plantea | Queffelec 2024, pp. 231-234 | alta (como negativo) |
| 3 | **Cerámica**: ¿tiestos antillanos aquí o dabajuroides allá? | **No** en un sentido; un caso dudoso en el otro | Urbina 2011, Zavala 2018, Dijkhoff 1997 §3.5 | alta (negativo) / muy baja (el positivo) |
| 4 | **Conchas y botuto**: ¿tráfico documentado? | **No** | Zavala 2018 Tabla II; Mol 2007 §6.7.5 | media-alta (como negativo) |
| 5 | **Genética**: ¿flujo continente↔islas tras la migración inicial? | ⭐⭐ **Sí — y en dirección islas → continente** | Fernandes 2020, Nature 590:106 y SI2/SI9 | alta |
| 6 | **El puente ABC**: ¿contactos hacia el norte? | La arqueología dice «no se sabe»; los huesos dicen «sí» | Dijkhoff 1997 §3.5 y §3.7; Fernandes 2020 | alta |

### El detalle que más duele de cada fila

- **(1)** *«The strongest argument supporting Colombia as a source of some of
  the guanín found in Cuba comes from **iconographic rather than chemical
  data**»* (Martinón-Torres et al. 2012, p. 449). Y la ruta dentro de Cuba se
  lee de este a oeste. ⚠️ **La trampa a evitar**: Oliver liga las «piedras
  verdes» del comercio caquetío a la Sierra Nevada de Santa Marta, y el guanín
  de Cuba apunta a orfebres **de la Sierra Nevada de Santa Marta**. Eso no es
  contacto entre caquetíos y taínos: es que **eran clientes del mismo taller,
  por caminos distintos**. Mismo proveedor, no mismo trato.
- **(2)** En una síntesis de 54 páginas sobre la lapidaria caribeña, **el área
  caquetía no aparece**: cero menciones de Aruba, Bonaire, dabajuroide, Guajira
  o Falcón. La lapidaria antillana se emparenta con el área ístmo-colombiana.
- **(3)** **Cero en las 24 sondas antillanas** en Urbina 2011 (192 yacimientos
  de Falcón costero) y en Zavala 2018 (Médanos de Coro, siglos XIV-XVIII), con
  control positivo en las dos. El único positivo del otro lado es **un sello de
  cerámica de Aruba** con «similitudes tipológicas» con sellos de Haití y Santo
  Domingo — dicho de pasada, sin figura ni catálogo, por un autor que en la
  misma página concluye: *«Of connections with the Greater Antilles, I think
  not much can be said yet»*. Y la mejor estatuilla «taína» de Aruba resulta
  parecerse a un tipo dominicano que **Rouse clasifica como falsificación**.
- **(4)** El botuto de los Médanos de Coro es **3 unidades sobre 304 fragmentos
  de concha (1,0 %)**: comida, no mercancía. Y el valioso taíno de concha —el
  guaíza— no baja del **sur de las Antillas Menores**: el más meridional con
  contexto es de Lavoutte, Santa Lucía.
- **(5)** Y en la otra dirección, nada: ninguna migración continental posterior
  entró en las Antillas, con potencia de detección declarada de **~2-8 %**. La
  esfera tiene **una sola dirección medible**.
- **(6)** El único rasgo material compartido ABC ↔ Antillas Mayores en toda la
  parcela son **las pictografías** (están en las ABC y en las Mayores, y **no**
  en las Menores) — y están **sin fechar**, y el propio autor traza la conexión
  posible por el continente, no por el mar.

---

## 4. Lo que NO se encontró (las negativas valen — skill §6)

- Ni un tiesto ostionoide, chicoide, meillacoide, elenoide ni palmetto en
  Falcón, Paraguaná, las ABC, Los Roques o Las Aves.
- Ni un tiesto dabajuroide ni valencioide en las Antillas Mayores.
- Ni una pieza de guanín, tumbaga, jadeíta, cemí, trigonolito, duho ni guaíza
  al sur de Santa Lucía.
- Ningún análisis de procedencia geoquímico concluyente de metal antillano.
- Ninguna fecha para el evento de mezcla de Curazao.
- El número exacto de individuos de Curazao analizados.
- Nägele 2020, Rouse y Cruxent 1963, Oliver 2000, Rouse 1992, Keegan y Hofman
  2017, Boomert 2000, Haviser 1987: no obtenidas, cada una con su motivo
  anotado en su nota de `4-fuentes/`.

---

## 5. 🔴 Una discrepancia de fechas que no se promedia

[[haviser-1990]] da para los dos esqueletos de De Savaan exhumados en 1980 un
C-14 sobre hueso de **1.500 ± 200 a.p.** (≈250-650 d.C.). El suplemento de
Fernandes da para el yacimiento un contexto de **1160-1500 d.C.** (≈790-450
a.p.). **No son la misma fecha ni de lejos.** O los individuos secuenciados no
son los de 1980, o hay dos fechados del mismo sitio sin conciliar. Quien quiera
afinar la época del flujo génico antillano tiene que resolverlo — probablemente
con Haviser 1987, que es la fuente de las fechas de contexto y no está en
abierto.

---

## 6. Qué diría de la hipótesis de Miguel con esto en la mano

Miguel dijo: *«de que es plausible es plausible»*. Con lo medido, la respuesta
honesta es **sí, y no de la forma que esperabas**. La esfera caquetía no
estaba sellada por el nororiente: por ahí entró gente, y bastante. Lo que no
tocaba era el mundo taíno. Y hay un tercer hecho incómodo que conviene decir
entero: de los tres ejes largos —Guajira al oeste, Los Roques al este, el arco
antillano más allá— **el tercero sólo se ve en los huesos**. La arqueología no
lo ha encontrado, y los autores de la genética lo dejan escrito como tarea.

### Las opciones

**A. No tocar nada, y guardar el hallazgo en `6-fusion/`.** El hallazgo es de
ancestría, no de lengua ni de objetos, y el mundo del motor no se mueve por un
dato genético sin fecha.
*A favor*: es conservador y no mueve canon a mitad de campaña.
*En contra*: `3-mundo/etnias.yaml` seguiría diciendo que la sociedad que
simulamos no tenía **ningún** vecino documentado, cuando ahora hay uno con ADN.

**B. Entrar sólo la corrección a la campaña 1.** Arreglar el `gen-03` de
`taino_en_la_esfera_2026-09-21.yaml` («DOS NEGATIVOS MEDIDOS en la clase
genética»), que ya no es cierto, y el `aviso` de `arq-01`.
*A favor*: barato, y evita que queden en `6-fusion/` dos documentos de la misma
campaña que se contradicen sin decirlo.
*En contra*: se queda a medias; el dato sigue sin llegar al mundo.

**C. B + una ficha de vecino nueva: `etnia-010`, «arahuacos de las Antillas
Menores», `atestiguado`, contacto poblacional hacia las islas ABC.** Con la
`etnia-009` (taíno, contacto ninguno) de la campaña 1 al lado, las dos fichas
juntas cuentan la historia entera: el primo lejano que nunca vino, y el vecino
que sí vino y del que nadie hablaba.
*A favor*: es lo que la evidencia sostiene, y con la etiqueta más fuerte que
esta parcela puede dar.
*En contra*: 🔴 choca con el problema de esquema que la campaña 1 levantó —
**`etnias.yaml` no tiene campo `epoca` y el 9.º guardián no lo valida**. Aquí
muerde más, porque esta ficha sí es `atestiguado`: sin época diría que el
elenco del siglo XV tenía vecinos antillanos documentados, cuando lo
documentado es ancestría sin fechar.

**D. C + resolver primero el campo `epoca` en `etnias.yaml`** (vocabulario
cerrado: `precontacto` · `contacto-temprano` · `colonial` · `varias`, exigido
cuando `polity_caquetia: costera`).
*A favor*: es el arreglo de raíz, sirve para las dos fichas y para todas las
que vengan.
*En contra*: toca `curiana_sim/compilar_etnias.py`, que es motor, y por tanto
es decisión tuya y de otra sesión.

### Mi recomendación

**B ahora mismo, C en cuanto exista `epoca`.** B es corrección de algo que ya
está mal escrito en `6-fusion/` y no cuesta nada. C es lo correcto, pero
meterla sin `epoca` es meter en el registro de vecinos una afirmación
`atestiguado` que el validador no puede contradecir y que un lector
razonablemente leería como «en el siglo XV había antillanos en Curazao». Eso
es exactamente la trampa de la regla 3, y no vale la pena por ir tres días más
rápido.

**Y lo que NO propongo, para que quede dicho**: nada de tocar
`ESFERA_DE_CONTACTO`, el prompt ni el scorer. El hallazgo es de las Antillas
Menores y las voces de la esfera que el motor enseña son taínas. No se mueve
una etiqueta de lengua con un dato de ancestría. La auditoría de las 25 voces
taínas que la campaña 1 dejó abierta (su opción B) sigue abierta y sigue siendo
la siguiente cosa que hacer.

---

## 7. Lo que vi de paso

1. **Dijkhoff 1997 cierra una deuda documental** que
   `4-fuentes/martinez-cruzado-2003.md` llevaba abierta desde el 2026-08-14.
   Y trae una **tercera versión** del episodio de la deportación: «In 1515
   Diego de Salazar … took about 2000 Indians of Aruba, Bonaire and Curaçao».
   Arcaya daba 1513 y Salazar; Oliver, 1515 y Baso Zabala; Dijkhoff, 1515 y
   Salazar. Las tres bajan de Hartog o de Oliver: **no son independientes**.
2. **Aruba pudo ser un puesto comercial de frontera del caquetío costero**, y
   el contacto entre los caquetíos de la Guajira y los de Paraguaná pasaba por
   ella (Dijkhoff §3.9, citando a Oliver 1989:306). Es geografía política, es
   de otra parcela, y no está en el corpus.
3. **El contacto entre Aruba y Curazao «possibly went for a great deal via the
   mainland»**, porque las corrientes entre las islas son traicioneras. Si es
   cierto, la esfera insular no es un arco isla-a-isla sino un radio desde la
   costa — y eso sí toca cómo se imagina el mar en el motor.
4. **Dos filones de arqueología insular abierta que el repo no había tocado**:
   los congresos de la IACA digitalizados en la University of Florida Digital
   Collections (ufdc.ufl.edu) y el fondo `mana.aw` / Biblioteca Nacional Aruba
   en archive.org. De ahí salieron Haviser 1990 y Dijkhoff 1997 en una tarde.
5. **Casale et al. 2024 es el hilo vivo.** La petrografía de la cerámica
   arubeña deja un **grupo 3, decorado, del Urumaco Temprano, de origen
   incierto**. Es la única pista material viva hacia una cerámica no local en
   las ABC, y el artículo es CC-BY: basta abrirlo con un navegador.
