# Brief de diseño — JAI Sounds: la batea y el wiki

Para una instancia de **Claude Design**. Este brief pide un handoff de alta
fidelidad, en el mismo formato que `design_handoff_jai_sounds`: README,
`designs/*.html` y `assets/`, para recrearlo en el código de Curiana Radio
(Next.js 16 App Router + Tailwind v4).

Fecha: 2026-10-05. Cliente: Miguel (Curiana Radio).

---

## 1. Qué es JAI Sounds

La tercera arista de Curiana Radio (88.8 FM): curaduría musical **sin fronteras
de género**. Cada canción entra por lo que describe (la experiencia viva que la
trajo al mundo, el sentimiento que la sostiene), no por lo que es.

- **jai** (caquetío) = **oír, escuchar**. Fuente: Zavala Reyes 2015, glosario
  #175, «Jai (AM): Oír, escuchar.» Nunca «ruido, sonido»: esa glosa estaba mal.
  **Decidido (Miguel, 2026-10-05):** se escribe **jai**, como la fuente. El
  rótulo es «jai · caquetío · oír, escuchar»; la *y* del handoff anterior
  queda descartada.
- El dial son **23 estaciones** (playlists de Miguel en Spotify), cada una con
  **portada propia** de arte original. Las portadas son el alma visual: ver
  `assets/portadas-spotify.png` (adjunta).

## 2. Lo que hay hoy y por qué no sirve

En producción, `curianaradio.com/jai-sounds` hoy tiene, en este orden: el hero
con el escrito fundacional, frases sueltas del escrito difuminadas, una grilla
de 23 placas iguales (el monograma jA sobre un color) y la estación
sintonizada con un embed de Spotify.

Miguel la rechazó por cuatro razones:
- **Mucho texto antes de la música.**
- **23 placas iguales**, que se ven como un muro repetido.
- **El escrito partido**, que corta la lectura.
- **Larga y mal ordenada.**

Lo que quiere, en sus palabras: *«un panel de radio. Que la gente pudiese sentir
como si estuviese browseando vinilos pero de forma digital. Con énfasis en la
curaduría, pero con la profundidad de poder ir al detalle en cuanto a
canciones»* y *«un wiki con cada canción, álbum y artista para que el rabbit
hole sea lo más profundo posible»*.

## 3. Dirección elegida: «la batea»

Hay maquetas navegables con datos reales; Miguel eligió la **A · la batea**.
Están en <https://claude.ai/artifact/8UvUT13mz9of6CGmNru8fP>, que es privada:
Miguel la abre y comparte capturas. Capturas adjuntas: `maqueta-a-escritorio.png`
y `maqueta-a-movil.png`.

Estructura de `/jai-sounds`, de arriba abajo:

1. **Consola** (una franja). Lleva el jA, «jai sounds», el rótulo «jai ·
   caquetío · oír, escuchar» y una lectura mono de la estación: «estación
   09 / 23 · hue 296».
2. **La batea**, a la izquierda. El disco del frente se ve completo y los seis
   de atrás asoman por arriba, cada uno con su lomo («10 · Tambores de mi
   sangre»). Se pasa de disco con ← →, con la rueda o deslizando en el móvil;
   el disco que se va cae hacia adelante. Abajo van los **separadores**: 23
   miniaturas para saltar a cualquier estación.
3. **La contraportada**, a la derecha. Tiene:
   - el nombre de la estación;
   - sus datos: pistas, duración total, rango de años y artistas distintos;
   - «más presentes» (los tres artistas que más se repiten);
   - el espacio de la **nota de curaduría** de la estación;
   - el botón «escuchar en spotify»;
   - el **tracklist completo**.
4. **La ficha de pista**. Se abre al tocar una fila y es la puerta al wiki:
   álbum, año, duración, «en el dial desde», «también en [otras estaciones]» y,
   si existe, la reseña. Cada nombre lleva a su página.
5. Debajo de la música, **una sola vez y entero**: § 01 la música (el escrito
   fundacional), § 02 el viaje (presenta el podcast Descubriendo con Chocolate)
   y el canal (el show «Curiana Radio» en Spotify). El texto literal está en
   `components/jai-sounds/escrito.ts`.

Lo que queremos que el diseño mejore sobre la maqueta: la sensación física de
la batea (peso, cantos, el gesto de pasar), la jerarquía de la contraportada y
la ficha de pista como antesala del wiki.

## 4. El wiki: canción, álbum y artista

Cada entidad tiene su página, y todo nombre en cualquier página es un enlace.
El objetivo es que uno entre por una canción y salga una hora después cuatro
artistas más lejos.

### Las dos voces (regla de Miguel)

Cada página tiene **dos bloques de texto**, y nunca se confunden:

- **«JAI»**: la reseña propia de Miguel. Si no hay, el estado vacío dice
  **«JAI Sounds aún no le hace review»**. Hoy no hay ninguna, así que el diseño
  tiene que verse bien **vacío** y también con una reseña **larga** (markdown,
  varios párrafos).
- **«Esto dice el internet»**: un extracto de Wikipedia, siempre con su fuente,
  licencia (CC BY-SA) y enlace. Es una voz ajena y tiene que leerse como cita,
  no como voz de JAI.

### Rutas

| Página | URL |
|---|---|
| Canción | `/jai-sounds/canciones/[slug]` (ej. `on-the-nature-of-daylight-max-richter`) |
| Álbum | `/jai-sounds/albumes/[slug]` |
| Artista | `/jai-sounds/artistas/[slug]` |

### Datos disponibles por página (reales; diseñar con estos, no inventar)

**Canción**
- De Spotify: título, artistas (en orden: principal y featuring), álbum, número
  de pista, duración, fecha del álbum, portada del álbum (640px), enlace a
  Spotify.
- Del dial: en qué estaciones está, en qué posición y desde cuándo («en el
  dial desde 2023-09-17»). Además, la canción **anterior y la siguiente** en
  cada estación: la secuencia también es curaduría.
- De MusicBrainz:
  - **primera edición**: suele diferir de Spotify, que da la del reissue;
    «The Sound of Silence» figura como 1968 y salió en 1966;
  - **géneros y tags** de la grabación;
  - **créditos** (productor, ingeniero, mezcla, músicos con su instrumento,
    voces), cada uno con enlace a su página de artista;
  - la **obra** (la composición);
  - las **ediciones** (álbum original, compilaciones, en vivo).
- Las dos voces: JAI e internet.

**Álbum**
- Portada, título, artistas, tipo (álbum, single, compilación) y fecha.
- Qué canciones del álbum están en el dial y en qué estaciones.
- Las dos voces.

**Artista**
- De MusicBrainz: tipo (persona o grupo), país, origen («se formó en…»), años
  (inicio y fin), géneros, **miembros** (si es grupo) o **grupos de los que fue
  parte**, y enlaces (Wikipedia, Discogs, Bandcamp, web oficial).
- Del dial:
  - todas sus canciones y en qué estaciones;
  - sus álbumes presentes;
  - rango de años de lo suyo que suena;
  - «suena cerca de»: otros artistas que comparten estación con él.
- Las dos voces.

### El rastro

Propuesta para que el hoyo se sienta como hoyo: un **rastro** visible del
camino recorrido en la sesión, por ejemplo «Sound Gods → The Alan Parsons
Project → I Robot → Eric Woolfson → …», con vuelta atrás a cualquier punto.
Diseñarlo como componente propio.

### Cifras reales (para dimensionar)

- 23 estaciones · **1.944 canciones** · **1.700 álbumes** · **1.759 artistas**.
- MusicBrainz encuentra alrededor del **90%** de las canciones.
- Géneros: en ~30% de las grabaciones y ~57% de los artistas.
- Créditos: en ~37% de las canciones.
- Wikipedia o Wikidata: en ~50% de los artistas.
- Hay que diseñar el **dato ausente** con elegancia: muchas páginas tendrán poco,
  y una página con poco tiene que seguir invitando a seguir.

### Ejemplos reales para las maquetas

- **El Pozo Instrumental** (estación 09, 87 pistas). Contiene «Richter: On the
  Nature of Daylight» (Max Richter, Lorenz Dangel, 2025), la única canción con
  reseña, que viene de la edición #01: *«Una pieza que habita el espacio entre
  la melancolía y la esperanza. Las cuerdas se despliegan como ondas de radio
  atravesando el éter…»*
- **The Sound of Silence**, de Simon & Garfunkel:
  - estación Sound Gods;
  - Spotify dice 1968 y MusicBrainz dice 1966-01-17;
  - créditos: producer Tom Wilson; instrument Vinnie Bell, Bob Bushnell, Al
    Gorgoni, Bobby Gregg; vocal Art Garfunkel;
  - géneros: folk rock, folk pop, singer-songwriter;
  - el artista es un grupo de EE. UU. desde 1963.
- **Squarepusher**, «Goodnight Jade» (1996-05-31): ambient, IDM, jungle. Es una
  persona del Reino Unido, nacido el 1975-01-17. Tiene Wikipedia y Discogs.
- **SANAM**, «Mouathibatti» (2023): grupo del Líbano, experimental rock /
  post-rock, sin Wikipedia (caso de dato escaso).

## 5. Sistema visual JAI (no negociable)

Viene del handoff anterior y del manual de marca.

- **Registro**: la cabina de noche.
  - Noche `#0b1119`, panel `#131c28` y filete `#24303f`.
  - Luz `#f1ece2`, con secundario `#b9c3d1` y meta `#7b8a9c`.
- **Señal por estación**: `oklch(0.8 0.15 hue)`; la versión tenue es
  `oklch(0.28 0.06 hue)`. El hue no es de la estación: es su turno en el dial,
  `hue(i) = (semilla + i·360/N) mod 360`, con la semilla por sesión. El color es
  dato, no decoración.
- **Tipografía**:
  - Fraunces display: 900, `opsz 9`, `SOFT 50`, `WONK 1`, en minúscula.
  - Fraunces para títulos: 700, `opsz 72`, `WONK 1`.
  - Fraunces para manifiesto y reseña: 500, `opsz 72`, `SOFT 30`, `WONK 1`.
  - Inter 400 para leer (1.65–1.75, máximo 65ch).
  - Mono (`ui-monospace, Cascadia Mono, Consolas`) para datos, en minúscula y
    con tracking 0.3em.
- **El jA** (monograma): **monocromo en reposo**. Solo recorre los matices del
  dial en hover. El logo original es negro sobre blanco. Nada de ruedas de
  color ni conic-gradients.
- **A escuadra**: radios 0, sin sombras, nada que rebote. Las transiciones de
  color y borde duran 300 ms.
- **Frequency `#ff6b35`**: solo para el chrome de la radio, nunca dentro de JAI.
- **Descubriendo con Chocolate**: su propia paleta fija, «orbe» (índigo y
  lavanda: `#1b1a33`, `#23224a`, `#c9c8f5`, `#eceafd`), y Fraunces itálica
  `opsz 144`, `SOFT 100`.
- Respetar `prefers-reduced-motion`. El móvil es de primera clase: la batea se
  pasa deslizando a los lados, porque el gesto vertical es del scroll.

## 6. Restricciones técnicas

- Los datos salen de Supabase (esquema `jai`) **solo en el servidor**, con
  caché. Nada de consultas desde el navegador.
- Imágenes:
  - las portadas de las estaciones están en el repo (`public/jai/portadas`,
    640px);
  - las portadas de álbum vienen del CDN de Spotify (`i.scdn.co`, 640/300/64px).
- El reproductor es el embed oficial de Spotify (playlist o canción). No hay
  audio propio.
- Las reseñas son markdown y las escribe Miguel en Obsidian.

## 7. Qué pedimos en el handoff

1. **`/jai-sounds`**: consola, batea, contraportada, ficha de pista y lo de
   abajo (escrito, viaje, canal). En escritorio y en móvil.
2. **Canción, álbum y artista**: cada página llena (con reseña y con internet)
   y casi vacía (sin reseña, sin Wikipedia, pocos datos).
3. **El rastro** como componente.
4. **Estados**: cargando, sin datos de MusicBrainz y sin reseña.
5. Un README con tokens, medidas e interacciones, como el anterior.

El handoff vuelve a la raíz del proyecto como `design_handoff_jai_wiki/`, sin
versionar, igual que los anteriores.
