---
tipo: sesion
fecha: 2026-10-09
obra: acasio-2023-capubana-calendario
quien: minero (Claude Opus 5.5), rama vault/acasio-capubana
descripcion: "Acasio 2023 leído entero: «Capubana» es una estación de petroglifos de la falda, no el cerro; la lectura metónica es hipótesis de autor y no se puede refutar tal como está"
---

# Sesión 10 — Acasio 2023, la estación Capubana

> [[acasio-2023-capubana-calendario]] · [[esteves-1989]] ·
> [[monumento-cerro-santa-ana]] · [[mapa-creencia]] · propuesta:
> `6-fusion/acasio_capubana_2026-10-09.yaml` · borrador de issue:
> `6-fusion/issues-pendientes/capubana-nombre-acasio-2026-10-09.md`

## Qué se preguntó

Miguel lo está leyendo y dice que «es importantísimo para la creencia y de
alguna forma confirma que el Cerro Santa Ana era llamado también Capu Bana».
Hasta hoy sólo se habían localizado sus figuras. Seis preguntas: a qué llama
«Capubana» y con qué apoyo; qué es dato y qué hipótesis en el calendario
metónico; qué otras piedras y qué bibliografía; qué son las «Calzadas»; quién,
cuándo y para qué; y si da base para una cuenta lunar en el canon.

## Cómo

Las 21 páginas (impresas 305-325, pdf + 304) en texto y en imagen; las figuras
en su imagen nativa. El `.txt` del repo es la salida de `pdftotext` y conserva
los acentos. Las negativas llevan su sonda, sin acentos y en minúsculas, y se
repitieron sobre una extracción nueva.

## Qué salió

1. **El nombre.** «Capubana» es siempre una *estación* de arte rupestre «en la
   falda del cerro de Santa Ana» (p. 305), a 210 m, «en el primer piso biótico
   del monumento natural» y «muy cerca de las calzadas» (p. 308). El cerro es
   siempre «Cerro de Santa Ana». El nombre de la estación ya estaba en el
   título de Salazar 2017 (Inparques), y Acasio no dice de dónde sale. **No
   confirma que el cerro se llamara Capubana.** Lo que da es un uso vivo del
   nombre, con b, pegado a la falda del macizo. Pero la b coincide con el
   capubana de Zavala #61, sigla HB (Hernández Baño, que escribió también
   sobre petroglifos de Falcón): hasta leer a Salazar, no cuenta como
   atestación independiente.
2. **El petroglifo** existe y está bien descrito: una roca de 0,76 × 0,70 m
   junto a un bloque grabado de casi 4 m; un rectángulo de dos filas y tres
   columnas, con 8 trazos dentro y 3 encima, sobre un vástago; 33 × 19 cm. Eso
   es atestiguado (moderno). **La lectura metónica es hipotética**: el método
   es de Rebullida, para la España neolítica; los trazos reciben rótulos, no
   cuentan lunaciones; la regla de «saltar» trazos y la excepción del año 19
   son las que dejan sitio a los números que hacen falta; el 118 se busca, no
   se calcula; no hay nada medido en el cielo. Tal como está, ningún
   resultado habría contado en contra. Confunde además el ciclo metónico con
   la regresión de los nodos (p. 314).
3. **Las otras piedras.** Acasio separa la Piedra de Siraba (2013, «glifos
   lunares») y la de Misaray (2016, «calendario Luni-solar») de la estación
   Capubana. Por él, la estación **no** es las «Piedras del Almanaque» de
   Esteves; la candidata es su Piedra de Siraba. Bibliografía: siete obras,
   tres suyas, Salazar 2017, una web de Barcelona y dos de Rebullida.
4. **«Calzadas»** es el nombre de un lugar junto a la estación, y el
   petroglifo se llama por él «Calendario de las Calzadas». No dice qué son:
   ni empedrado, ni muro, ni camino. No sale en Esteves ni en OSM. Nada que
   ver con las calzadas de los Llanos.
5. **Quién, cuándo, para qué.** «Nuestros originarios», sin pueblo, sin fecha,
   sin material asociado. La función agrícola y de caza que le da no tiene
   prueba.
6. **La simulación.** El artículo no da base para una cuenta lunar en el
   canon. La que hay es otra y atestiguada: `apana` 'una luna. Medición de
   tiempo' y `buiamati` 'dos lunas' (Zavala, sigla GC, Galeotto Cey, s. XVI),
   con `kati` 'luna'.

De paso, para ecología: la vegetación de la estación según Salazar 2017 trae
«urupaguita (Castela erecta Turpin)», un binomio para la familia de
`urupagua`, que en el lexicón no tiene taxón. Es una pista, no una
identificación.

## Qué no salió

Coordenadas, glosa del nombre, tradición, rito, dueño del cerro, fecha,
pueblo, las Piedras del Almanaque, y cualquier cita de Esteves, Morón,
Zavala Reyes, Hernández Baño, Oliver, Arcaya o Cruxent. Cada cero con su
sonda en la propuesta (§lo_que_no_dice).

## Qué decide Miguel

1. **toponimo-113.**
   - **A (recomendada):** se añade la lectura de Acasio (tipo `glosa-fuente`,
     eje `referente`) y una frase a la observación; nivel B sin cambios; la
     tensión sigue abierta hasta Salazar 2017.
   - **B:** además, una `forma_viva` «estación Capubana» sin coordenadas. Hay
     que ver antes si el mapa la tolera sin punto.
   - **C:** tomarlo como confirmación de que el Santa Ana entero era el
     Capubana y subir la lectura del 2026-09-01. No se recomienda: el
     artículo no lo dice.
2. **La lectura calendárica en creencia.**
   - **A (recomendada):** no entra en `creencia.yaml`. Se cambia sólo el
     «que lo subiría» de creencia-022: la lectura publicada de Siraba existe
     (Acasio 2013; Caguao y Morón 2024) y no está en el repo.
   - **B:** entra un hecho `hipotetico` «lectura de autor del s. XXI», con la
     crítica al lado. Tiene el riesgo de que un rótulo de autor
     («calendario») se lea como tradición, que es lo que «del Almanaque» sí
     es.
3. **sitios_era2 §Capubana (materiales).** ¿Se añade la estación como objeto
   del paisaje (una piedra grabada en la falda, a 210 m, junto a un bloque de
   cuatro metros), sin su lectura? Recomendado: sí, como `atestiguado`
   moderno, y con la deuda de coordenadas.
4. **Descargas.** Salazar 2017 primero, si se encuentra; luego Hernández
   Baño, Acasio 2013 y Caguao y Morón 2024. Descargar lo decide Miguel.
