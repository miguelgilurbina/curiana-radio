# Galería: plan de monetización e interfaz

Continuación de [`GALERIA.md`](GALERIA.md), que documenta la infraestructura ya
construida. Este documento decide **qué se vende** y **cómo se navega**.

Fecha: 2026-08-10. Base: 821 obras publicadas en `content/galeria/obras.json`.

---

## 0. Punto de partida, medido

Todo lo de abajo sale de contar sobre el manifest real, no de estimar.

| Señal | Valor | Consecuencia |
|---|---|---|
| Obras publicadas | 821 | — |
| Con `licencia: reservado` | **821 (100%)** | No hay nada ofrecible hoy |
| Con `tags` | **0** | La faceta «Motivos» nunca se pinta |
| Series | **1** (`archivo`, descripción `TODO`) | La faceta «Serie» nunca se pinta |
| Con `originalKey` | **0** | Los másteres solo existen en un disco local |
| Lado mayor ≥ 1.400 px | 129 (16%) | Techo de impresión |
| Lado mayor 1.200–1.399 px | 432 (53%) | " |
| Lado mayor < 1.200 px | 260 (32%) | " |
| Orientación | 479 horizontal · 251 cuadrada · 91 vertical | El póster vertical es el formato que más se vende, y es el que menos tenemos |
| Prompts que nombran a una persona real | **0** | No hay derechos de imagen que pedir |
| Prompts que citan a un artista real | 6 | Decisión curatorial, no legal |
| Prompts que nombran una marca registrada | 2 | Se apartan y ya |
| **Catálogo licenciable** | **813 (99%)** | Casi todo el archivo |
| …de esas, con lado ≥ 1.200 px | **561** | Licenciable *y* usable en grande |

### Tres callejones que hay que nombrar antes de seguir

**1. La barra de filtros está viva pero vacía.** `GaleriaGrid` esconde la faceta
de series si `series.length > 1` es falso, y la de motivos si no hay tags. Con
una serie y cero tags, el bloque completo se reduce a «821 obras · Barajar».
Se construyó una interfaz de navegación facetada y hoy no navega nada: para
llegar a la obra 700 hay que hacer scroll por 699.

**2. Techo de resolución.** `ESCALERA = [400, 800, 1400]` con
`withoutEnlargement: true`: los archivos servidos nunca superan el máster, y el
máster ronda 1.024–1.400 px.

| Lado mayor | A 300 DPI | A 200 DPI | A 150 DPI |
|---|---|---|---|
| 1.024 px | 8,7 cm | 13,0 cm | 17,3 cm |
| 1.344 px | 11,4 cm | 17,1 cm | 22,8 cm |
| 1.400 px | 11,9 cm | 17,8 cm | 23,7 cm |

Un póster A3 (29,7 × 42 cm) a 300 DPI pide ~3.500 × 4.960 px. Estamos a un
factor de 3,5×. **Sin upscaling no hay pósters.** Hay postales.

**3. Los másteres son un punto único de fallo.** `originalKey` está en cero: los
PNG originales viven en un disco, fuera de la plataforma. Si ese disco muere, la
resolución máxima del archivo pasa a ser 1.400 px para siempre y cualquier vía
de impresión futura queda cerrada. Esto es urgente e independiente de todo lo
demás.

---

## Parte 1 — Monetización

### 1.1 La decisión de fondo: licenciar antes que imprimir

La aritmética decide sola.

**Vía impresión (POD).** Un póster con márgenes normales de POD deja entre 8 y
20 € por unidad. Para llegar a 500 € al mes hacen falta ~35 ventas mensuales, lo
que exige tráfico sostenido, catálogo con formato vertical (tenemos 91), pasarela
de pago, gestión de IVA/IOSS si se vende a la UE, y una política de devoluciones.
Y hoy ni siquiera se puede imprimir en A3.

**Vía licencia.** Una licencia editorial son 80–150 €. Una comercial pequeña,
300–600 €. Cinco licencias al año igualan un semestre de póster, con **cero**
infraestructura de pago: se factura y se cobra por transferencia. El producto no
se fabrica, no se envía y no se devuelve.

El catálogo además juega a favor de la licencia: 465 obras limpias, cada una con
`alt` descriptivo y `concepto` escritos mirando la imagen, y 821 páginas
estáticas ya en el `sitemap.ts`. Eso es un activo de SEO de cola larga apuntando
justo al comprador que busca «imagen desierto atardecer torre» y necesita
derechos, no un póster.

> Esto **no cancela** el print. Lo pone en la fase 3, cuando exista upscaling y
> una razón para montar la pasarela. La sección 1.5 lo deja especificado.

### 1.2 Derechos: el obstáculo que resultó no estar ahí

Conviene decir primero lo que **no** es un problema, porque la intuición
heredada de la fotografía de stock lleva a la conclusión contraria.

**No hacen falta cesiones de imagen.** Un *model release* existe para que una
persona real consienta el uso de su cara. Aquí no posó nadie: las figuras son
sintéticas. No hay a quién pedirle permiso porque no hay nadie.

Y al revisar los prompts uno por uno, tampoco aparece el caso que sí importaría
—que la máquina hubiera reproducido a alguien concreto—:

- **Cero prompts nombran a una persona viva.** Los 34 que dicen «portrait of» o
  «photo of» describen arquetipos: *«an androgynous entity»*, *«a Caqueto native
  American from the 16th century»*, *«an albino african man»*, *«a middle aged
  person who works…»*. El único humano nombrado en las 821 es Simón Bolívar,
  muerto en 1830.
- **Solo 6 citan a un artista real** (Moebius, Bruce Pennington ×2, Octavio
  Ocampo, Hajime Sorayama, Jeff Easley). Los demás «in the style of» nombran una
  época o una estética: *1990s arawak*, *polaroid*, *soviet realism*, *1970s
  japanese photography*. Y el estilo no es objeto de copyright: esto es una
  decisión curatorial tuya, no una restricción legal.
- **Solo 2 nombran una marca registrada** (*polaroid*, *Call of Duty on a
  Playstation*). Eso sí es marca, y por eso se apartan.

De ahí el triaje real:

| Montón | Criterio | Nº | Licencia destino |
|---|---|---|---|
| **Verde** | Todo lo demás | **813 (99%)** | `comercial` o `editorial` |
| **Ámbar** | Cita a un artista real | 6 | Tu decisión: curatorial, no legal |
| **Rojo** | Nombra una marca registrada | 2 | `reservado` |

El catálogo comercial no son 352 obras: son **813**, y **561** con lado ≥ 1.200 px.
Prácticamente todo el archivo es vendible.

Queda un residuo, y es honesto dimensionarlo en vez de convertirlo en política:
un modelo generativo puede producir por casualidad una cara que se parezca a
alguien real, y eso no se puede auditar por adelantado. Es raro, y la mitigación
proporcionada es reactiva —si alguien lo señala, se retira esa obra—, no
bloquear 288 imágenes por si acaso.

### 1.3 La escalera de licencias

Precios publicados, no «consúltanos». Un precio a la vista convierte varias veces
más que un formulario ciego, y filtra al que no va en serio antes de que te
escriba.

| Nivel | Qué cubre | Precio |
|---|---|---|
| **Personal** | Fondo de pantalla, impresión doméstica, un ejemplar sin reventa | 15–25 € |
| **Editorial** | Prensa, docencia, divulgación, podcast art, tesis | 80–150 € |
| **Comercial** | Portada de disco, libro indie, web de marca, local | 300–600 € |
| **Comercial ampliada** | Campaña, packaging, textil de marca, OOH | 1.200 € + |
| **Exclusiva / buyout** | Se retira del catálogo | Negociada |
| **CC BY-NC** | Regalada, con atribución | 0 € |

La escalera aplica a las 813 del montón verde sin distinciones: al no haber
personas reales ni propiedad ajena retratada, no hay razón para reservar los
niveles altos a un subconjunto. Las 2 de marca se quedan en `reservado` y las 6
que citan a un artista las decides tú. El CC BY-NC es un subconjunto de ~20
elegidas a mano.

El nivel CC BY-NC no es caridad: es el anzuelo de descubrimiento. Veinte obras
libres circulando con atribución hacen más por el tráfico que cualquier anuncio,
y el tipo ya existe en `TipoLicencia`.

El esquema de datos aguanta todo esto sin migración: `licencia`,
`licenciaDetalle.print` y `licenciaDetalle.notas` ya están en el manifest. Falta
un campo de precio, y es un añadido, no un cambio.

### 1.4 Canales, ordenados por esfuerzo

**a) Directo desde la ficha.** La ficha ya tiene el aside de datos técnicos con
el hueco comentado esperando (`app/galeria/[slug]/page.tsx:134`). Ahí va el
bloque de licencia: etiqueta, precio, botón. El botón abre un formulario que
manda un correo con el slug precargado. Es una tarde de trabajo y es el canal de
mayor margen: 100%.

**b) Adobe Stock — el piso pasivo.** Acepta contenido generado con IA desde 2022
declarándolo con la casilla correspondiente. Su restricción es sobre personas,
lugares y marcas **identificables**, y la clave está en esa palabra: mide el
resultado, no el origen. Una figura sintética anónima la cumple; nuestros
arquetipos la cumplen. Solo quedan fuera las 2 de marca. Paga por
PayPal/Payoneer/Skrill, así que **no necesita pasarela**. La contrapartida es
honesta: 33% de royalty y céntimos por descarga. No es la tesis; es un suelo que
no cuesta nada mantener y es **no exclusivo**, así que no estorba a la venta
directa. Subir 800 imágenes con metadatos es un script, no un trabajo.

**c) Archivo listo para imprimir — el puente al print sin ser comerciante.**
Esto responde directo a «gente que quiera enmarcar o imprimir». En vez de
fabricar y enviar, se vende **el derecho más el archivo**: el comprador descarga
un TIFF/PNG a máxima resolución con licencia personal y lo lleva a la imprenta o
al marco que quiera. Sin stock, sin envío, sin aduana, sin devoluciones. Es un
producto digital, lo que simplifica muchísimo el cobro. Requiere el upscaling de
la fase 3 para las obras grandes, pero funciona ya para tamaños ≤ A5.

**d) POD propio con checkout.** Fase 3. Ver 1.5.

**e) Marketplaces de print.** Displate y Society6 aceptan obra propia asistida
por IA y su público va explícitamente a decorar paredes. Etsy la acepta con
declaración obligatoria («Designed by», no «Made by») y una moderación
automática agresiva. Saatchi Art **prohíbe** obra generada por prompt: descartada.
Son canales de cero infraestructura y cero control de marca — útiles como prueba
de mercado, malos como destino final.

### 1.5 La vía print, especificada para cuando toque

No se construye ahora, pero conviene dejar decidido lo caro:

1. **Rescatar los másteres primero** (ver 3.1). Sin eso no hay fase 3.
2. **Upscale curado, no masivo.** Elegir 40–60 obras verticales y cuadradas,
   llevarlas a 4K–6K con un upscaler neuronal y revisar artefactos una por una.
   Un upscale por lote sin revisión produce dedos derretidos a tamaño A2, y eso
   sí destruye la marca. El límite aquí es de curaduría y de cómputo, no de
   derechos: hay 561 candidatas elegibles.
3. **Socio de fabricación.** Comparadas:

   | | Fuerte en | Débil en |
   |---|---|---|
   | **Prodigi** | Giclée museo, aprobación del Fine Art Trade Guild, marca blanca, API REST de dropship, fábricas propias UK/UE | Menos variedad textil |
   | **Gelato** | Producción local en 30+ países (envío barato al comprador rico), API con 5.000 llamadas/día en el plan libre | Enruta a terceros: control de calidad indirecto |
   | **Printful** | Textil, packaging de marca, fábricas propias Letonia/España | Márgenes más ajustados en fine art |

   Para esta galería: **Prodigi** para papel y **Printful** para prenda. Ambos
   API-first, que es lo que pide «usar nuestra página como base de datos».
4. **La arquitectura no cambia.** `obras.json` sigue siendo la fuente de verdad;
   el POD nunca guarda el catálogo. El pedido se compone en el servidor con el
   `originalKey`, se manda a la API del fabricante y se guarda el número de
   seguimiento. La galería es el catálogo; el fabricante es una función.

### 1.6 El cobro: lo que la vía licencia te ahorra

Aquí está la ventaja escondida de licenciar primero, dado desde dónde cobras.

- **Stripe no acepta registro directo desde Chile** (figura en *preview*); en
  hispanoamérica opera con España y México. El rodeo habitual es constituir una
  LLC en EE. UU., lo que implica entidad, contabilidad y un asesor — decisión de
  negocio, no de código.
- **Los Merchant of Record** (Lemon Squeezy, Paddle, Gumroad) resuelven el IVA
  global, pero **liquidan por Stripe Connect**: si Stripe no cubre tu país, ellos
  tampoco pagan. Hay que verificarlo con el país concreto antes de construir nada
  encima.
- **Binance sirve como vía de cobro personal, no como facturación B2B.** Una
  revista, una universidad o una discográfica pagan contra factura por
  transferencia; su departamento de compras no manda USDT. Guárdalo para
  liquidaciones y para el comprador particular que lo pida.
- **Una licencia no necesita pasarela.** Se emite una factura y se cobra por
  transferencia, Wise, PayPal o Payoneer. Con 5–20 operaciones al año, montar
  checkout automático es resolver un problema que no tienes.

**Y un coste real que hay que asumir el día uno:** [`GALERIA.md:44`](GALERIA.md)
ya lo advierte. El plan Hobby de Vercel está restringido por contrato a uso
personal no comercial. En cuanto se cobre una sola licencia hace falta **Pro
(~20 USD/mes)**. Es contractual, no técnico, y no hay forma de esquivarlo.

### 1.7 Mercados de mayor poder adquisitivo implican inglés

Los compradores de licencia con presupuesto están en EE. UU., Reino Unido,
Alemania y los nórdicos. El sitio está **íntegramente en español**, incluidos los
821 `alt` y `concepto` que son precisamente el activo de SEO.

No hace falta traducir el sitio entero. Hace falta que la superficie comercial
hable inglés: la ficha de obra (`alt` y `concepto` bilingües en el manifest), una
página `/licensing`, y los metadatos de Adobe Stock. Los `alt` ya existen en
español y traducirlos es un paso más del pipeline por lotes que ya escribió
`scripts/galeria-describir.mjs`. Es la palanca de ingreso más barata de todo
este documento y la más fácil de posponer para siempre.

---

## Parte 2 — Interfaz

### 2.1 Lo urgente: devolverle la navegación al mosaico

Por orden de impacto sobre esfuerzo:

**a) Generar los tags.** Ya existe la maquinaria: `galeria-describir.mjs`
describió las 821 por lotes con el SDK de Anthropic. Un
`scripts/galeria-etiquetar.mjs` calcado sobre un vocabulario **cerrado** de 12–18
motivos (`desierto`, `mar`, `arquitectura`, `figura`, `nocturno`, `maquinaria`,
`textil`, `ritual`…) resucita la faceta que ya está construida. Vocabulario
cerrado, no libre: 300 tags únicos son tan inútiles como cero.

**b) Describir las series y partir el archivo.** `archivo` con descripción
`TODO` es un marcador de posición. Tres o cuatro series con nombre real hacen
que la faceta aparezca (`series.length > 1`) y le dan al mosaico una historia.

**c) Navegar por color.** Cada obra ya trae su color dominante. Agrupado por
tono, el catálogo se reparte así: 313 neutro · 149 naranja · 112 azul · 76 cian ·
69 rojo · 44 verde · 37 amarillo · 21 magenta. Es un eje de navegación completo
que **no cuesta ni un byte de datos nuevos**, y en una galería es el filtro más
natural que existe: la gente busca «algo azul para esa pared». Ordenar el mosaico
por tono en vez de al azar, además, lo convierte en un degradado.

**d) Buscador.** `titulo + alt + concepto` ya viajan al cliente. Un filtro de
subcadena sobre 821 registros es instantáneo y no necesita servidor.

**e) Sincronizar el lightbox con la URL.** Hoy no se puede compartir una obra
ampliada ni cerrarla con el botón «atrás». Un `?obra=<slug>` en el historial
arregla las dos cosas y de paso hace compartible cada apertura.

**f) Deuda del lightbox:** sin gesto de deslizar en táctil, sin precarga de la
vecina (cada flecha es una espera en blanco), sin zoom. Las tres son pequeñas y
las tres se notan.

**g) Mostrar la licencia.** El hueco comentado en la ficha es el que convierte la
galería en negocio. Depende de la Parte 1.

### 2.2 Lo que ya está bien y no hay que tocar

El motor de mosaico justificado, la medición por callback de ref, la escalera
WebP servida plana sin transformaciones facturables, el color dominante como
reserva de hueco, el barajado con `useSyncExternalStore` para no romper la
hidratación y `separarHermanas()`. Es trabajo bien pensado. La Parte 3 construye
encima, no lo sustituye.

---

## Parte 3 — Motion graphics

La galería es de una radio. La metáfora rectora no es «animación bonita» sino
**sintonizar una señal**: ruido que se resuelve en imagen. Eso da coherencia y
evita el catálogo de efectos sueltos.

Hay un precedente en el repo que conviene seguir: `sim-amanecer` en
[`globals.css:208`](app/globals.css) usa `animation-timeline: view()` dentro de un
`@supports`, animación dirigida por scroll en CSS puro, sin JS y sin degradar
donde no existe. Ese es el patrón.

**Antes de nada, una deuda:** no hay una sola regla `prefers-reduced-motion` en
todo `globals.css`, y ya hay tres animaciones corriendo (`gradient-shift`,
`sim-caret-blink`, `sim-amanecer`). Con un mosaico animado de 800 piezas eso pasa
de descuido a problema de accesibilidad real. Todo lo de abajo va envuelto en
`@media (prefers-reduced-motion: no-preference)`, y esa regla se añade primero.

### Las ideas, por relación impacto/coste

**1. Sintonía al cargar (la firma de la casa).** Hoy el hueco es un rectángulo de
color plano y la imagen aparece de golpe. En vez de eso: mientras carga, una
franja de barrido recorre el bloque de color dominante —estática de radio— y al
llegar la imagen entra con una rampa breve de `filter: saturate(0.4) blur(6px)`
a nítido. La señal se engancha. Convierte una espera inevitable en identidad de
marca, cuesta un `keyframes` y un `onLoad` en `ImagenObra`, y la brand ya está
construida sobre 88.8 FM.

**2. Barajar como transición real, no como parpadeo.** Hoy `key={firma}` en
`Mosaico` desmonta y remonta: 800 piezas desaparecen y reaparecen. Con la View
Transitions API y un `view-transition-name` por slug, las piezas **vuelan** a su
nueva posición. Es el momento estrella de la galería y ahora mismo es su peor
frame. Next 16 lo habilita con `experimental.viewTransition: true` y React 19.2
expone `unstable_ViewTransition`; también se puede llamar a
`document.startViewTransition` directamente en el handler `barajar()` y saltarse
la bandera. Es la de mayor impacto visual de la lista.

**3. La pieza se abre en lightbox (elemento compartido).** Misma API: la baldosa
crece hasta ser el lightbox en vez de aparecer un modal encima. Es el gesto que
distingue una galería cuidada de una plantilla.

**4. Revelado por filas al bajar.** Cada fila del mosaico sube 16 px y aparece al
entrar en pantalla. `animation-timeline: view()` dentro de `@supports`, copiando
`sim-amanecer`. Cero JS, cero coste de runtime, y hace que 800 piezas se sientan
como un desplazamiento y no como un volcado.

**5. Foco selectivo al pasar por encima.** Ya existe `group-hover:scale-[1.04]`.
Súmale que las hermanas de la misma fila bajen a `saturate(0.6)` con `:has()`: la
mirada se enfoca sola. Es el gesto de la fotografía editorial, son dos líneas de
CSS.

**6. El dial del cursor.** En escritorio, un halo radial muy tenue siguiendo al
puntero sobre el mosaico, como la aguja barriendo la banda. Solo con puntero
fino (`@media (hover: hover) and (pointer: fine)`), y debe ir con
`background-position` o un pseudoelemento con `transform`, nunca provocando
repintado del mosaico.

**7. Paralaje de profundidad.** Cada imagen se desplaza unos píxeles dentro de su
baldosa a distinta velocidad según la fila: el tejido respira al bajar. Bonito y
peligroso: solo `translate3d`, y es la primera candidata a caer si el móvil
sufre.

**8. El contador que cuenta.** Al cambiar de filtro, «821 obras» rueda hasta el
nuevo número en vez de saltar. Detalle pequeño, comunica que el sistema respondió.

### Presupuesto de rendimiento, para que esto no arruine el mosaico

- Solo `transform`, `opacity` y `filter`. Nada que dispare *layout*.
- Ni una animación fuera de pantalla: la ventana de `TANDA = 60` de `Mosaico` ya
  acota cuántas piezas hay vivas; que las animaciones respeten ese mismo límite.
- Sin librería de animación. React 19.2 + View Transitions + CSS cubren las ocho
  ideas. Meter Framer Motion serían ~40 KB para lo que el navegador ya hace.
- Medir INP en móvil antes y después. Si el paralaje o el dial mueven la aguja,
  se caen: la galería la sostiene la imagen, no el efecto.

---

## Orden propuesto

| Fase | Qué | Por qué antes que lo siguiente |
|---|---|---|
| **0** | Subir los másteres a un Blob privado y poblar `originalKey` | Es lo único irreversible si sale mal. Todo el print futuro depende de ello |
| **1** | Tags + series + navegación por color + buscador | El catálogo no se puede vender si no se puede recorrer |
| **2** | Apartar las 8 obras marcadas, abrir las 813 y publicar precios en la ficha | Primer ingreso posible. Requiere Vercel Pro |
| **3** | Sintonía al cargar, revelado por filas, View Transitions al barajar y al abrir | La capa que hace que la galería se sienta cara |
| **4** | Superficie comercial en inglés + `/licensing` + carga a Adobe Stock | Abre los mercados de mayor poder adquisitivo |
| **5** | Upscale curado de 40–60 obras, integración con Prodigi/Printful | El print, cuando haya con qué imprimir y a quién venderle |

Las fases 1 y 3 son independientes de las de negocio y se pueden ir haciendo en
paralelo.

---

## Fuentes consultadas

- [Prodigi Print API](https://www.prodigi.com/print-api/) — API REST de dropship, fábricas UK/UE.
- [Adobe Stock: contenido generativo](https://helpx.adobe.com/stock/contributor/help/generative-ai-content.html) y [FAQ](https://helpx.adobe.com/stock/contributor/submit-your-content/submit-generative-ai-content/adobe-stock-generative-ai-faq.html) — política de IA, declaración obligatoria.
- [Lemon Squeezy: países soportados](https://docs.lemonsqueezy.com/help/getting-started/supported-countries) — cobertura de MoR.
- [Stripe global](https://stripe.com/global) — países soportados.
- [Saatchi Art: política de IA](https://support.saatchiart.com/hc/en-us/articles/27671947605915-AI-Generated-Art-Policy) — prohíbe obra generada por prompt.
- [Resolución y DPI para impresión](https://letsenhance.io/blog/all/image-resolution-print-quality/) — umbrales de 150/300 DPI.
- [Alternativas a Prodigi (comparativa POD)](https://fourthwall.com/blog/prodigi-alternatives-for-print-on-demand) y [alternativas a Printful](https://www.gelato.com/blog/printful-alternatives).
- [React 19.2 View Transitions en Next 16](https://www.digitalapplied.com/blog/react-19-2-view-transitions-animate-navigation-nextjs-16).
