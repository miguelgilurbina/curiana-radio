# Medición: qué se cuenta y para qué

Fecha: 2026-10-05; el embudo, los eventos nuevos y la privacidad de las URL,
2026-10-08. Cubre J4 del [`PLAN_MAESTRO`](proyecto-linguistico-caquetío/1-plan/PLAN_MAESTRO.md)
(«sin datos, "efectivo" seguirá siendo una sensación») y prepara J5, el motivo
de negocio. No decide cómo se monetiza: decide **qué hay que saber antes** de
decidirlo, y deja el sitio contándolo.

---

## 1. Qué se cuenta

**Solo, sin código propio** (Vercel Web Analytics + Speed Insights, en
`components/analitica/Analitica.tsx`, una sola vez en el layout raíz): visitas
por página, visitantes, referentes (de dónde llegan), país, dispositivo, y el
rendimiento real de quien visita. Sin cookies: no hace falta banner de
consentimiento. Vercel reconoce al visitante por una huella que se descarta
cada día; no sigue a nadie de una visita a otra.

**Eventos propios** (`lib/analitica.ts`, máximo 2 propiedades cada uno, que es
el límite de Pro):

| Evento | Cuándo | Propiedades | Dónde se dispara | Qué pregunta responde |
|---|---|---|---|---|
| `intro` | saltó el afinado o sintonizó en El Disco | `accion`: `saltar` · `sintonizar` | `components/intro/IntroDisco.tsx` | ¿la intro retiene o expulsa? |
| `arista` | clic en un enlace de navegación que lleva a una arista | `arista`: `kaketiana` · `jai-sounds` · `senales` · `sobre` (y `galeria` cuando se libere); `desde`: `cabecera` · `pie` · `landing` · `intro` | el oyente de clics de `Analitica.tsx` (ver «Cómo se marca un enlace») | ¿qué puerta funciona: la cabecera, el pie, el carrusel y las tarjetas de la landing, la intro? |
| `lectura` | llegó al final de un texto y lleva ≥ 20 s en la página | `pagina` | `components/analitica/FinDeLectura.tsx`: ediciones, Kaketiana (pueblo y lengua), Señales, ficha de canción de JAI **con reseña** | ¿se lee o se hojea? qué textos se terminan |
| `suscripcion` | **se confirmó** la suscripción al newsletter | `desde` | la página de confirmación (ver abajo) | ¿la radio convierte visitas en audiencia propia? |
| `salida` | clic en cualquier enlace externo | `destino`, `desde` | el oyente de clics de `Analitica.tsx` | ¿a Spotify (JAI), al repo, a las fuentes (archive.org…)? |
| `estacion` | pasó a otra estación de la batea de JAI Sounds | `estacion` | `components/jai-sounds/batea/Batea.tsx` | qué curaduría engancha |
| `obra` | abrió una obra de la galería en grande | `obra` | `components/galeria/GaleriaGrid.tsx` | qué piezas tienen demanda (licencia, print) |
| `luz` | cambió la luz con el interruptor | `luz`: `claro` · `oscuro` (la que eligió) | `components/senales/InterruptorLuz.tsx` (Señales, «Quién transmite») | ¿se usa la segunda luz? ¿vale la pena diseñarla en cada piel? |

Ningún evento lleva el correo ni nada que identifique a nadie.

**`suscripcion` se mide en la confirmación, no en el envío.** Enviar el
formulario no es suscribirse: falta abrir el correo y confirmar. El evento se
dispara en la página a la que lleva el enlace de confirmación, y `desde` dice
dónde se llenó el formulario si la confirmación lo sabe —nunca la URL de
confirmación ni el token—. Por si acaso, `medir()` recorta cualquier ruta de
`/suscripcion/…` a `/suscripcion`. Mientras el newsletter no confirme, lo
sigue disparando el formulario al enviarse (`components/landing/Suscripcion.tsx`):
hasta entonces el paso 5 del embudo cuenta intenciones, no suscripciones.

### Cómo se marca un enlace

Un solo oyente de clics (`Analitica.tsx`) cuenta `salida` y `arista`; los
componentes de diseño no llevan `onClick`. Para que un enlace interno cuente
como `arista`:

- **`data-desde`** en el enlace o en su contenedor más cercano: hoy lo llevan
  las dos `<nav>` de la cabecera (escritorio y el menú del móvil), el
  `<footer>` del pie y la `<nav>` de la intro.
- **La arista sale de la ruta** del enlace (`/kaketiana/…` → `kaketiana`). Un
  CTA cuya ruta no la nombra —una señal de Kaketiana enlazada desde la landing
  contaría como `senales`— lleva **`data-arista`** con la arista que
  corresponde.
- **En la landing** (`/inicio`) todo enlace sin contenedor marcado cuenta como
  `landing`: los CTA del carrusel (`HeroAristas`) y de las tarjetas
  (`Secciones`) ya se miden sin tocarlos. Aun así, el carrusel y las tarjetas
  deberían llevar **`data-desde="landing"`** en su contenedor, para no depender
  de que la landing viva en `/inicio`, y `data-arista` donde la ruta no diga
  la arista.
- Un enlace interno fuera de una navegación marcada (el «Todas las señales» de
  Kaketiana, la firma de una señal) no cuenta: no es una entrada desde la
  navegación.

### Lo que nunca sale

`antesDeEnviar` (`lib/analitica.ts`) es el `beforeSend` de Web Analytics y de
Speed Insights, lo último que ve cada envío antes de salir del navegador:

- La URL sale **sin hash y sin query, salvo los `utm_*`** (ver «UTM»). El `?t=`
  de los enlaces de confirmación, o cualquier otro parámetro, no sale.
- **Bajo `/suscripcion/` no se cuenta ninguna vista** ni métrica de
  rendimiento: esas páginas pueden llevar el token en la ruta. Los eventos
  propios sí salen —ahí se mide `suscripcion`— con la URL recortada a
  `/suscripcion`.
- Si la URL no se puede leer, no se envía.

### Ruido

- **En local** (`next dev`, `vercel dev`) se carga el script de depuración:
  escribe en la consola del navegador cada vista y cada evento, y **no envía
  nada**. Cada vista sale dos veces en la consola: es el modo estricto de
  React en desarrollo, no pasa en producción.
- **Las vistas previas** de Vercel se guardan aparte de producción; el panel
  muestra Production por defecto. Los eventos sólo se encienden en Production
  (ver «Para encenderlo»).

## 2. El embudo

El recorrido que el sitio propone, de la puerta a la audiencia propia. Es un
embudo **de proporciones, no de personas**: sin cookies, Vercel no sigue a
nadie de un paso al siguiente; se comparan los visitantes de cada paso en el
mismo período. En el panel, siempre **Production** y el mismo rango de fechas
para los cinco pasos.

| Paso | Qué es | Dónde se ve en Vercel → Analytics |
|---|---|---|
| **1. Intro** (`/`) | llegó a la puerta, El Disco | **Pages** → `/` (visitantes). **Events** → `intro` → propiedad `accion`: cuántos sintonizan y cuántos saltan el afinado |
| **2. Landing** (`/inicio`) | pasó la puerta, o entró directo | **Pages** → `/inicio`. **Referrers** con el filtro de `/inicio` (clic en la fila): quién llega directo sin pasar por la intro |
| **3. Entrada a una arista** | eligió Kaketiana, JAI Sounds o Señales | **Events** → `arista` → propiedad `arista` (a cuál) y propiedad `desde` (por qué puerta). Para el volumen de cada sección: **Pages** → `/kaketiana`, `/jai-sounds`, `/senales`; la pestaña **Routes** junta las fichas (`/senales/[slug]`, `/kaketiana/pueblo/[slug]`) |
| **4. Lectura completa** | terminó un texto | **Events** → `lectura` → propiedad `pagina`; dividido por las vistas de esa misma página en **Pages** = tasa de lectura completa |
| **5. Suscripción confirmada** | se quedó: confirmó el correo | **Events** → `suscripcion` → propiedad `desde` |

Las preguntas que responde, leídas de a dos pasos:

- **1 → 2**: visitantes de `/inicio` ÷ visitantes de `/`, y `intro` por
  `accion`. Si la intro expulsa, el paso 2 lo dice primero. Ojo: quien ya vio
  la intro en la sesión vuelve a `/` y salta solo a `/inicio`; cuenta en los
  dos.
- **2 → 3**: `arista` con `desde` = `landing` ÷ visitantes de `/inicio`. Si la
  landing no lleva a las aristas, la gente entra por la cabecera o no entra.
- **3 → 4**: `lectura` ÷ vistas, por página. Es el número que importa para
  Kaketiana; las visitas solas no distinguen al que lee del que rebota.
- **4 → 5**: `suscripcion` ÷ visitantes del sitio. Pocas lecturas y muchas
  suscripciones, o al revés, cuentan historias distintas.

## 3. Cómo leerlo cada semana

Diez minutos, los lunes. Vercel → proyecto curiana-radio → **Analytics**,
**Production**, **Last 7 days**. Cinco vistas, en este orden:

1. **El total.** Visitantes y vistas arriba del todo, con la comparación
   contra la semana anterior que el panel muestra al lado. Una subida sin
   difusión detrás se explica en la vista 3.
2. **Pages → Routes.** Qué se leyó: las fichas de Señales y de Kaketiana, y
   los pasos 1 y 2 del embudo (`/` y `/inicio`).
3. **Referrers.** De dónde llegan: LinkedIn, Instagram, YouTube, buscadores,
   y **el tráfico desde IA** —`chatgpt.com`, `perplexity.ai`, `claude.ai`,
   `bing.com` / Copilot—. Es la medida de si `/llms.txt`, el JSON-LD y la
   política de `robots.txt` («buscadores sí, entrenamiento no») funcionan.
   Con Web Analytics Plus, la pestaña **UTM Parameters** dice además qué
   publicación los trajo (ver «UTM»).
4. **Events → `arista`** (por `desde`, después por `arista`) **y `lectura`**
   (por `pagina`). Qué puerta funciona y qué se termina de leer.
5. **Events → `suscripcion`** (por `desde`) **y `salida`** (por `destino`).
   Quién se queda y a dónde se va el que se va: Spotify para JAI, las fuentes
   para Kaketiana.

Una vez al mes, además: **Speed Insights**, por si alguna página se volvió
lenta en el teléfono. Y cuando haga falta cruzar algo que el panel no cruza,
la API: `GET /v1/query/web-analytics/events/aggregate` con
`by=eventData/desde` y `filter=eventName eq 'arista'` (la misma consulta la
hace Claude con la herramienta `get_web_analytics` del MCP de Vercel).

No se anotan cifras a mano en este archivo: el panel guarda doce meses en Pro.

## 4. UTM

Sin UTM, una visita desde la app de Instagram, un cliente de correo o la app
de LinkedIn llega muchas veces **sin referente** y se cuenta como directa. Los
enlaces de difusión llevan siempre:

```
?utm_source=<linkedin|instagram|youtube|newsletter>&utm_medium=<post|bio|video|correo>&utm_campaign=<slug>
```

| Dónde va el enlace | `utm_source` | `utm_medium` | `utm_campaign` |
|---|---|---|---|
| El ensayo o una publicación de LinkedIn | `linkedin` | `post` | el slug de lo que se difunde (`ensayo-01`, el slug de la señal) |
| Una publicación de Instagram / el enlace de la bio | `instagram` | `post` / `bio` | el slug / `bio` |
| La descripción de un video de YouTube | `youtube` | `video` | el slug del video |
| El newsletter | `newsletter` | `correo` | la edición (`senal-2026-11`) |

El `<slug>` va en minúsculas, con guiones y sin tildes. El enlace lleva a lo
que se difunde (la señal, el artículo), no a la portada. Ejemplo:
`https://curianaradio.com/senales/<slug>?utm_source=linkedin&utm_medium=post&utm_campaign=ensayo-01`.

**Se leen con Web Analytics Plus** (+US$10/mes sobre Pro), en Referrers →
UTM Parameters. Sin Plus no se ven, pero la convención se fija ya: los enlaces
que circulen desde hoy van a contar el día que se active. `antesDeEnviar` ya
**deja pasar los `utm_*`** y quita todo lo demás: activar Plus no pide tocar
código. ChatGPT agrega `utm_source=chatgpt.com` a sus enlaces por su cuenta.

## 5. Para encenderlo

**Estado (2026-10-08):** Web Analytics y Speed Insights activos, el equipo en
plan Pro. Falta:

1. **Los eventos propios**: agregar `NEXT_PUBLIC_ANALITICA_EVENTOS=1` en
   Vercel → proyecto → Settings → Environment Variables, **sólo en
   Production**, y **redeployar**. Es una variable `NEXT_PUBLIC_`: se escribe
   en el código al compilar, así que sin un deploy nuevo no cambia nada.
2. **UTM (opcional)**: activar Web Analytics Plus cuando arranque la difusión
   (ver «UTM»).
3. **Search Console y Bing Webmaster Tools**: verificar `curianaradio.com` por
   DNS (registro TXT en Vercel → Domains) y enviar `/sitemap.xml`. Bing importa
   la verificación de Google en un clic, y el índice de Bing alimenta Copilot y
   parte de las búsquedas de ChatGPT: cuenta para el tráfico desde IA.

### Lo que da cada plan

| | Hobby | Pro (US$20/mes) — el actual |
|---|---|---|
| Eventos al mes | 50.000 (después se pausa) | por uso, US$0,03 cada mil |
| Historia que se guarda | **1 mes** | 12 meses |
| Eventos propios | no | sí, 2 propiedades |
| UTM (`?utm_source=linkedin`) | no | con Web Analytics Plus (+US$10) |

Para decidir monetización hace falta comparar meses, y Hobby borraba el mes
anterior: por eso Pro.

## 6. Las hipótesis y la señal que las prueba

Cada arista tiene una vía de ingreso plausible. Lo que sigue es qué número
mirar para saber si vale la pena construirla, no la decisión.

| Arista | Vía plausible | La señal | Cuándo se mira |
|---|---|---|---|
| **La radio** (ediciones, Señales, newsletter) | apoyo de la audiencia: membresía o donación recurrente | `suscripcion` ÷ visitas a `/inicio`; `lectura` de ediciones y señales | cuando el newsletter confirme suscripciones |
| **Kaketiana** | patrocinio cultural, fondos de patrimonio y de lenguas indígenas, universidades; a la larga, el diccionario impreso | `lectura` de artículos; voces más visitadas; `arista` → `kaketiana`; `salida` hacia fuentes; **referentes chatgpt.com, perplexity.ai, claude.ai, bing.com** | a los 3 meses de difusión. Un fondo pide alcance demostrable: esto es esa evidencia |
| **JAI Sounds** | patrocinio de la curaduría; curaduría por encargo | `estacion`; `arista` → `jai-sounds`; `salida` → open.spotify.com; `lectura` de reseñas | a los 3 meses |
| **Galería** | licencias primero, print después (decidido en [`GALERIA_PLAN.md`](GALERIA_PLAN.md) §1.1) | `obra` (las más ampliadas son el catálogo a licenciar); visitas a `/galeria/[slug]` desde buscadores de imágenes | cuando haya licencias publicadas |

Lo que no está en la tabla a propósito: **publicidad**. Necesita un volumen de
visitas que un proyecto así no tiene ni busca, y ensucia la página.
