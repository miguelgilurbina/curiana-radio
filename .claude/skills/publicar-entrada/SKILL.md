---
name: publicar-entrada
description: Publicar una entrada («señal») en el blog de Curiana Radio a partir de lo que Miguel dicta o pega desde su libreta — transcribir con limpieza mínima, armar el archivo en content/senales/, subir las fotos a Vercel Blob, incrustar videos de YouTube, etiquetar por arista (Kaketiana, JAI Sounds, Galería, Buchibe) y abrir el PR con su vista previa. Usar cuando Miguel quiera publicar, subir o escribir un post, una entrada, una señal o algo en el blog; cuando dicte o pegue un texto de su libreta para el sitio; o cuando pida corregir, despublicar o reetiquetar una entrada ya publicada.
---

# Publicar una entrada

Señales es el blog de Curiana Radio (`/senales`, issue #248). La radio
transmite desde después; las señales las escribe Miguel desde acá, firmadas.
Es **un solo blog**: cada entrada lleva las aristas a las que pertenece y cada
arista muestra las suyas. La landing muestra las tres últimas de cualquier
arista.

Miguel escribe en una libreta y la **dicta** en una sesión (2026-10-03: «lo que
hago es escribir en una libreta y prefiero transcribirlo a través de una
llamada… es lo que me sale más rápido»). Este flujo es para eso: él habla, la
sesión transcribe, arma y abre el PR; él publica con su «mergea».

## 1. El texto: limpieza mínima, y se muestra antes de tocar nada

Lo que llega es un dictado (con «eh», arranques repetidos, palabras mal oídas)
o un texto pegado. Se limpia **lo mínimo**:

- puntuación y párrafos;
- fuera las muletillas y los arranques en falso («eh», «o sea, o sea»);
- los nombres que el dictado oye mal: *Kaketiana* (no «Caquetiana»),
  *JAI Sounds* (no «High Sounds»), *caquetío*, *Paraguaná*, *Buchibe*,
  *Cayerúa*, *Curiana*.

**No se reescribe.** Ni sinónimos, ni orden, ni recortes, ni frases «mejores».
Es su voz y va firmada. Si ves algo que mejorar (una repetición, una frase que
no cierra), se dice **aparte en el chat**, nunca dentro del texto.

Muéstrale el texto limpio entero y espera su ok antes de seguir. Si corrige,
aplica sus correcciones literalmente.

## 2. Lo que la entrada necesita

Una entrada es un archivo, `content/senales/<slug>.mdx`:

```mdx
---
titulo: "El título"
fecha: 2026-10-03
sumario: "Una o dos frases: lo que se ve en la tarjeta, en el índice y al compartir."
aristas: [kaketiana]          # kaketiana · jai-sounds · galeria · buchibe; vacío = «la radio»
piel: buchibe                 # opcional: sin ella, la piel de su primera arista
portada:                      # opcional
  src: https://….blob.vercel-storage.com/senales/<slug>/foto.webp
  alt: "Lo que se ve en la imagen, para quien no la ve"
  pie: "Lo que Miguel quiera decir de ella"
borrador: false               # true = se ve en local y en la vista previa, nunca en producción
---

El cuerpo en markdown.
```

- **Título, sumario, aristas:** si Miguel no los dijo, propón (dos o tres
  títulos sacados de su texto; un sumario con sus palabras; las aristas por el
  tema) y **elige él**. Una entrada puede llevar varias aristas.
- **La arista dice dónde aparece; la piel, cómo se ve** (el motor de pieles,
  `components/senales/pieles/`, BRAND_MVP §12). Sin `piel:`, la entrada se
  viste con la piel de su primera arista: Kaketiana en la placa clara, JAI en
  el dial, Galería en la sala, Buchibe en el telón; sin arista, la noche de la
  radio. Si lleva dos aristas, pregúntale cuál va primero. Si Miguel quiere
  otra piel, `piel: <id>`; si la piel que pide no existe todavía, no se
  improvisa: se diseña aparte y se registra en el motor.
- **Fecha:** la de hoy, salvo que diga otra.
- **Slug:** del título, corto, minúsculas, sin tildes, con guiones
  (`el-silicio-es-tierra`). Es la URL: no se cambia después de publicar.
- **Autor:** sale solo («Miguel Gil Urbina»). Sólo se escribe `autor:` si la
  firma es otra.

Dentro del texto, además del markdown:

- `<Figura src="…" alt="…" pie="…" />`: una imagen con su pie.
- `<Video id="…" titulo="…" />`: un video de YouTube (el id o la URL entera).
  Los videos no se suben: van a YouTube (@curianaradio) y se incrustan.

`lib/senales.ts` valida el archivo en el build: si falta un campo o una arista
no existe, el build falla con el nombre del archivo. Que falle es mejor que una
entrada rota en producción.

## 3. Las fotos: a Vercel Blob, nunca al repo

El repo vive en OneDrive (ver GALERIA.md). Las fotos van a Blob con el script,
que las pasa a WebP de 1600 px y te devuelve lo que hay que pegar:

```powershell
vercel env pull "$env:TEMP\curiana-blob.env"     # las credenciales, fuera del repo
npm run senales:imagenes -- <slug> "C:\ruta\foto 1.jpg" "C:\ruta\foto 2.png" --env "$env:TEMP\curiana-blob.env"
```

- HEIC (iPhone) no se lee: que la exporte a JPG.
- El `alt` lo escribes tú describiendo la imagen; el `pie` es de Miguel.
- Las imágenes de la galería ya están en Blob: una entrada puede usar una obra
  de la galería con su URL, sin subir nada.

## 4. El PR

- Rama desde `main`: `senales/<slug>`.
- Commit **por ruta** (sólo `content/senales/<slug>.mdx`):
  `senales: <título>` + la línea de coautoría.
- PR en español: el título de la entrada, las aristas, y el enlace a la vista
  previa de Vercel (`/senales/<slug>`). En la vista previa se ve también la
  tarjeta para compartir: `/senales/<slug>/opengraph-image`.
- **Se publica con el «mergea» explícito de Miguel.** Una pregunta o un «se ve
  bien» no es un ok.

## 5. Después de publicar

- Queda en `https://curianaradio.com/senales/<slug>`, en la landing, en el
  índice, en cada arista que lleve y en el RSS (`/senales/rss.xml`).
- Para compartir: el enlace directo (LinkedIn y WhatsApp muestran la tarjeta
  con el título). En Instagram, el enlace va en la bio o en una historia.
- Corregir una errata: otro PR sobre el mismo archivo. Despublicar: `borrador:
  true` (la URL deja de existir en producción) o borrar el archivo.

## Lo que no se hace

- **Una entrada etiquetada Kaketiana es la voz de Miguel, no el canon.** La
  página ya lo dice al pie y enlaza a la investigación. No le agregues datos
  del canon al texto, ni lo «corrijas» contra el canon. Si una cifra del texto
  choca con un seed (voces, topónimos, artículos), díselo en el chat y que
  decida él.
- No se inventa nada para rellenar: ni pie de foto, ni sumario «de marketing»,
  ni etiquetas que él no aceptó.
- No se publica en las redes desde aquí. Las redes las mueve Miguel.
