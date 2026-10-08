# El newsletter: cómo funciona y qué falta configurar

Fecha: 2026-10-08. Proveedor único: **Resend**. Todo el código está hecho; lo
que falta es la cuenta de Resend y las variables en Vercel (§2). Mientras falten,
el formulario se muestra deshabilitado con «LA SUSCRIPCIÓN ABRE PRONTO», como
hasta ahora.

Decisiones de Miguel (2026-10-08): doble opt-in; remitente
«Curiana Radio <senales@curianaradio.com>», con reply-to configurable; el lector
elige qué recibe: **cada Señal** o **la edición mensual** (que las trae todas),
por defecto la edición.

---

## 1. Qué se construyó y por qué

### El flujo

1. **El formulario** (`components/landing/Suscripcion.tsx` →
   `FormularioSuscripcion.tsx`): en el pie de todas las páginas, en la landing y
   en la página de un enlace caducado. Correo + tema (LA EDICIÓN, CADA MES /
   CADA SEÑAL) + un campo trampa invisible. Postea JSON a `/api/suscripcion`.
2. **`POST /api/suscripcion`** (`app/api/suscripcion/route.ts`): valida, firma
   un token y le manda al lector un correo **«Confirma tu frecuencia en Curiana
   Radio»** con un botón CONFIRMAR →. No guarda nada.
3. **El lector abre el enlace** → `/suscripcion/confirmar?t=…`
   (`app/suscripcion/confirmar/page.tsx`): verifica la firma y la fecha y da de
   alta el contacto en Resend: en el segmento «Newsletter», con el tema elegido
   en *opt-in* y el otro en *opt-out*. Muestra «Quedaste en la frecuencia», mide
   el evento `suscripcion` (MEDICION.md) y borra el token de la barra.
4. **Los envíos** se hacen desde Resend (Broadcasts), eligiendo segmento y tema
   (§3). Las bajas también las lleva Resend (§5).

### Por qué así

- **Doble opt-in**: nadie entra a la lista sin probar que el correo es suyo. Así
  no se le escribe a quien no lo pidió (un tercero, un bot), la lista no se llena
  de direcciones falsas que rebotan, y Resend exige rebotes bajo 4 % y quejas
  bajo 0,08 % ([límites de cuenta][cuotas]).
- **Topics de Resend para el tema**: un topic por frecuencia («Cada Señal», «La
  edición, cada mes»). Un envío se dirige a un topic y le llega sólo a quien
  está suscrito a él, y el lector puede cambiar de topic o salir de uno desde la
  página de baja de Resend sin dejar los demás ([Topics][topics]).
- **Un token firmado y no una base de datos**: el sitio sigue sin estado. El
  token es `base64url(JSON{ e, t, exp })` + `.` + HMAC-SHA256 con
  `SUSCRIPCION_SECRET` (`lib/newsletter/token.ts`); vale 48 horas. Sin el
  secreto nadie puede fabricar uno ni cambiarle el correo o el tema. Va
  **firmado, no cifrado**: quien decodifique el enlace ve el correo (§6).

### Los archivos

| Archivo | Qué hace |
|---|---|
| `lib/newsletter/config.ts` | lee las variables; `configurado()` exige las cinco obligatorias |
| `lib/newsletter/suscriptor.ts` | valida el correo y el tema (lo usan el formulario y la ruta) |
| `lib/newsletter/token.ts` | `firmar` / `verificar` (HMAC, `timingSafeEqual`, 48 h) |
| `lib/newsletter/correo.ts` | el correo de confirmación, en HTML (la noche de la marca) y en texto |
| `lib/newsletter/resend.ts` | `enviarConfirmacion` y `darDeAlta` con el SDK oficial `resend` |
| `app/api/suscripcion/route.ts` | el primer paso |
| `app/suscripcion/confirmar/page.tsx` | el segundo paso (noindex, fuera del sitemap) |
| `components/landing/SuscripcionConfirmada.tsx` | mide y limpia la URL al confirmar |
| `lib/newsletter/*.test.mjs` | pruebas: `npm run newsletter:test` |

### Lo que responde la ruta

| Caso | Respuesta | El formulario dice |
|---|---|---|
| faltan variables | 503 (y en el registro, qué variable falta, nunca su valor) | La señal no salió… |
| no es `application/json` | 415 | — |
| `Origin` (o `Referer`) no es el sitio | 403 | La señal no salió… |
| cuerpo de más de 2 KB | 413 | — |
| JSON roto, correo o tema inválidos | 400 | Revisa el correo… |
| campo trampa con algo | 200 `{ok:true}` **sin hacer nada** | (cree que funcionó) |
| correo enviado | 200 `{ok:true}`, esté o no suscrito ya | Revisa tu correo: te mandamos un enlace para confirmar |
| Resend falla | 502 (el error al registro, sin el correo) | La señal no salió… |
| demasiados intentos | 429, lo pone el **Firewall de Vercel** (§2, paso 8) | Demasiados intentos; espera un momento. |

Orígenes permitidos: `https://curianaradio.com`; en vistas previas, también la
URL del deploy y la de la rama (`VERCEL_URL`, `VERCEL_BRANCH_URL`); fuera de
Vercel, `localhost`. El enlace del correo vuelve al origen desde el que se pidió:
en producción, curianaradio.com; en una vista previa, esa vista previa.

### Dónde la doc de Resend no alcanzaba

- **Crear un contacto que ya existe.** La [doc de errores][errores] no tiene un
  código para «ya existe», y crear uno repetido responde éxito
  ([resend-node#494][494]) sin decir si aplica `unsubscribed`, el segmento y los
  temas. Por eso `darDeAlta` **pregunta primero** (`contacts.get` por correo): si
  no existe, lo crea con todo ([crear contacto][crear]); si existe, lo actualiza
  por partes: `unsubscribed:false`, lo suma al segmento y fija los temas
  ([temas del contacto][temas-contacto]). Si dos confirmaciones se cruzan y la
  segunda creación falla con un 409 o un mensaje de «already exists», cae al
  mismo camino. Sumar al segmento a quien ya está se toma como éxito por la
  misma regla.
- **Errores.** El SDK no lanza: devuelve `{ data, error }`. Cualquier error que
  no sea esos dos casos corta el alta y la página dice «La señal se cortó» con
  un botón para reintentar (el enlace sigue sirviendo).
- **Re-suscribirse es cambiar de tema.** Confirmar otra vez, con otro tema,
  deja el último: el elegido en *opt-in*, el otro en *opt-out*. Y si alguien se
  había dado de baja de todo, confirmar de nuevo lo reactiva: es su nuevo sí.

---

## 2. La configuración, paso a paso (para Miguel)

En este orden. Ninguna clave se escribe en el repo ni en `.env.local` (la
carpeta sincroniza a OneDrive): todo va a Vercel.

1. **Crear la cuenta** en [resend.com](https://resend.com) (plan Free).
2. **El dominio.** Resend → **Domains** → **Add Domain** → `curianaradio.com`
   ([dominios][dominios]). Resend muestra los registros DNS:
   - **MX** `send` → el valor de Resend (`feedback-smtp.…amazonses.com`), prioridad 10
     (el Return-Path: recibe los rebotes; no toca el correo de la raíz);
   - **TXT** `send` → `v=spf1 include:amazonses.com ~all` (SPF);
   - **TXT** `resend._domainkey` → la clave DKIM que muestre Resend.

   Copiarlos en **Vercel → Domains → curianaradio.com → DNS Records → Add**, con
   el nombre sin el dominio (`send`, no `send.curianaradio.com`)
   ([guía de Resend para Vercel][resend-vercel]; Resend también ofrece *Auto
   configure*). Sumar **DMARC**: TXT `_dmarc` → `v=DMARC1; p=none;` (con
   `rua=mailto:…` si se quieren los reportes); `p=none` primero y endurecer
   cuando todo pase ([DMARC][dmarc]). Volver a Resend → **Verify DNS Records**:
   puede tardar unas horas.

   Resend sugiere enviar desde un subdominio (p. ej. `noticias.curianaradio.com`)
   para aislar la reputación ([subdominio o raíz][subdominio]). Miguel eligió
   `senales@curianaradio.com`; se puede cambiar después con `NEWSLETTER_FROM`.
3. **La clave.** Resend → **API Keys** → **Create API Key**, permiso **Full
   access**: *Sending access* «solo puede enviar correos» y el alta de contactos
   la necesita completa ([permisos][permisos]). Copiarla una sola vez.
4. **Vercel → proyecto curiana-radio → Settings → Environment Variables**
   ([variables][vercel-env]). Entorno **Production** (y **Preview** si se quiere
   probar en una vista previa), marcadas como *Sensitive*:
   - `RESEND_API_KEY` = la clave del paso 3.
5. **El segmento y los temas.** Resend → **Audience**:
   - **Segments → Create Segment** → «Newsletter» → menú ··· → *copy Segment ID*
     ([segmentos][segmentos]) → `RESEND_SEGMENT_ID`.
   - **Topics → Create Topic**, dos veces ([topics][topics]):
     «Cada Señal» → `RESEND_TOPIC_SENALES_ID`;
     «La edición, cada mes» → `RESEND_TOPIC_EDICION_ID`.
     *Default subscription*: **Opt-out** (le llega sólo a quien lo eligió; no se
     puede cambiar después). *Visibility*: **Public** (los dos aparecen en la
     página de baja y el lector puede pasarse de uno al otro). Si el panel no
     muestra el ID, sale de la API: `GET https://api.resend.com/topics` con la
     clave.
6. **El secreto** (≥ 32 bytes), generado en la terminal y pegado directo en
   Vercel, nunca en un archivo:
   - `openssl rand -base64 48`, o
   - `node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"`

   → `SUSCRIPCION_SECRET`. Si se cambia, los enlaces ya enviados dejan de
   servir (piden otro y listo).
7. **El remitente** (opcionales):
   - `NEWSLETTER_FROM`: por defecto `Curiana Radio <senales@curianaradio.com>`.
   - `NEWSLETTER_REPLY_TO`: por defecto el mismo remitente. **Ojo:**
     curianaradio.com hoy no recibe correo (no tiene MX en la raíz), así que una
     respuesta a `senales@` rebota. Poner aquí un buzón que Miguel lea, o
     configurar la recepción del dominio antes.
8. **Redeploy.** Deployments → el último de producción → ··· → **Redeploy**. Hace
   falta: las páginas estáticas deciden al compilar si el formulario está
   abierto.
9. **Probar con el correo propio**: suscribirse desde curianaradio.com → llega
   «Confirma tu frecuencia» (mirar spam la primera vez) → CONFIRMAR → «Quedaste
   en la frecuencia». En Resend → Audience → Contacts, el contacto debe estar en
   «Newsletter» con el tema elegido. Suscribirse otra vez con el otro tema y
   confirmar: el tema cambia.
10. **El límite por IP.** Vercel → proyecto → **Firewall** → **Configure** →
    **+ New Rule** ([rate limiting][waf]): nombre «suscripcion»; *If* Request
    Path *equals* `/api/suscripcion`; *Then* **Rate Limit**, Fixed Window,
    **10 minutos, 5 peticiones**, clave **IP**, acción *Default (429)* → Save →
    **Review Changes → Publish**. En Hobby cabe **una** regla de rate limit por
    proyecto (y tres reglas propias en total).

### Las variables

| Variable | Obligatoria | Qué es |
|---|---|---|
| `RESEND_API_KEY` | sí | clave de Resend con permiso completo |
| `RESEND_SEGMENT_ID` | sí | el segmento «Newsletter» |
| `RESEND_TOPIC_SENALES_ID` | sí | el topic «Cada Señal» |
| `RESEND_TOPIC_EDICION_ID` | sí | el topic «La edición, cada mes» |
| `SUSCRIPCION_SECRET` | sí | ≥ 32 bytes; firma los enlaces |
| `NEWSLETTER_FROM` | no | remitente; por defecto `Curiana Radio <senales@curianaradio.com>` |
| `NEWSLETTER_REPLY_TO` | no | a dónde van las respuestas; por defecto el remitente |

Ninguna es `NEXT_PUBLIC_`: no llegan al navegador. `NEXT_PUBLIC_SUSCRIPCION_URL`
ya no existe.

---

## 3. Cómo mandar un envío

**Desde el panel (lo normal).** Resend → **Broadcasts** → crear
([editor][editor]): remitente `Curiana Radio <senales@curianaradio.com>`,
audiencia el segmento **Newsletter** y el **topic** del envío («La edición, cada
mes» para la edición; «Cada Señal» para una Señal suelta). El pie lleva el
enlace de baja: el bloque de baja del editor, o un enlace a
`{{{RESEND_UNSUBSCRIBE_URL}}}`. Mandar un *Test email* al correo propio y
después enviar o programar.

**Por la API.** Crear el broadcast y mandarlo ([crear][broadcast-crear],
[enviar][broadcast-enviar], [guía][broadcast-api]):

```bash
# la clave se exporta en la shell, nunca en un archivo
curl -X POST https://api.resend.com/broadcasts \
  -H "Authorization: Bearer $RESEND_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "segment_id": "<RESEND_SEGMENT_ID>",
    "topic_id": "<RESEND_TOPIC_EDICION_ID>",
    "from": "Curiana Radio <senales@curianaradio.com>",
    "subject": "La edición de octubre",
    "html": "<p>…</p><p><a href=\"{{{RESEND_UNSUBSCRIBE_URL}}}\">Dejar de recibir</a></p>"
  }'
# → { "id": "…" }
curl -X POST https://api.resend.com/broadcasts/<id>/send \
  -H "Authorization: Bearer $RESEND_API_KEY" -H "Content-Type: application/json" \
  -d '{ "scheduled_at": "in 1 hour" }'   # opcional; sin él, sale ya
```

Sin `topic_id` el envío va a todo el segmento sin mirar los temas. Un broadcast
hecho en el editor no se puede mandar con `/broadcasts/{id}/send`.

---

## 4. Límites del plan gratis

Verificado en la doc de Resend el 2026-10-08 ([cuotas][cuotas],
[límites de la API][rate], [precios][precios]):

- **Los correos de confirmación son transaccionales**: 3.000 al mes y **100 al
  día** (día UTC; cuentan también los recibidos). Pasado el tope, Resend
  responde 429 `daily_quota_exceeded`, la ruta 502 y el lector ve «La señal no
  salió». Un día de difusión con más de 100 suscripciones lo alcanza: ese día
  hace falta Transactional Pro (US$20/mes, 50.000 al mes, sin tope diario).
- **Los envíos (Broadcasts) son marketing** y se cuentan por contactos, no por
  correos: Free = **correos ilimitados hasta 1.000 contactos**, 3 segmentos.
  Más de 1.000 suscriptores → Marketing Pro (desde US$40/mes, 5.000 contactos).
  *Corrección al plan inicial:* el tope de 100 al día **no** se aplica a los
  Broadcasts; se aplica a los correos de confirmación.
- **API**: 10 peticiones por segundo por cuenta. Una confirmación usa 2 (nuevo)
  o 4 (existente).

---

## 5. Bajas

No hay página de baja propia: la lleva Resend. Cada Broadcast lleva
`{{{RESEND_UNSUBSCRIBE_URL}}}` y esa página (personalizable en
[Settings → Unsubscribe page][baja]) muestra los topics públicos: el lector
puede salir de uno («Cada Señal») y quedarse en el otro, o salir de todo
(`unsubscribed: true`: no le llega ningún Broadcast). El sitio no
guarda nada que haya que borrar.

---

## 6. Lo que quedó fuera y lo que conviene saber

- **El correo va en el enlace**, firmado pero legible si se decodifica. Queda en
  el historial del lector hasta que la página lo borra y en los registros de
  peticiones de Vercel. Si molesta: cifrar el token (AES-GCM con el mismo
  secreto) en vez de sólo firmarlo.
- **Los escáneres de enlaces** de algunos correos corporativos (Outlook Safe
  Links y similares) abren los enlaces antes que la persona; eso confirmaría la
  suscripción sola. Si pasa, la salida es que la página pida un clic
  («Confirmar») en vez de confirmar al cargar.
- **`desde`** (la página del formulario) viaja en el POST pero no se guarda: el
  evento `suscripcion` se mide al confirmar y lleva el tema. Para saber desde
  qué página se suscriben habría que crear una propiedad de contacto en Resend.
- **Sin correo de bienvenida** ni secuencia: después de confirmar, lo siguiente
  que llega es el próximo envío.
- **El copy del pie** dice «LA SEÑAL, CADA MES» y el de la landing «una señal al
  mes»; ahora también se puede elegir cada Señal. Cambiarlo es decisión de
  Miguel.
- **Probar en local** sin tocar Resend: el SDK respeta `RESEND_BASE_URL`, así que
  se puede apuntar a un servidor falso que conteste como la API (así se probó
  este flujo, con una clave inválida y un Resend de mentira).

[cuotas]: https://resend.com/docs/knowledge-base/account-quotas-and-limits
[rate]: https://resend.com/docs/api-reference/rate-limit
[precios]: https://resend.com/pricing
[topics]: https://resend.com/docs/dashboard/contacts/manage-topics
[segmentos]: https://resend.com/docs/dashboard/contacts/manage-segments
[dominios]: https://resend.com/docs/dashboard/domains/introduction
[resend-vercel]: https://resend.com/docs/knowledge-base/vercel
[dmarc]: https://resend.com/docs/dashboard/domains/dmarc
[subdominio]: https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain
[permisos]: https://resend.com/docs/api-reference/api-keys/create-api-key
[errores]: https://resend.com/docs/api-reference/errors
[crear]: https://resend.com/docs/api-reference/contacts/create-contact
[temas-contacto]: https://resend.com/docs/api-reference/contacts/update-contact-topics
[494]: https://github.com/resend/resend-node/issues/494
[editor]: https://resend.com/docs/dashboard/broadcasts/editor
[broadcast-crear]: https://resend.com/docs/api-reference/broadcasts/create-broadcast
[broadcast-enviar]: https://resend.com/docs/api-reference/broadcasts/send-broadcast
[broadcast-api]: https://resend.com/docs/dashboard/broadcasts/send-broadcast-with-api
[baja]: https://resend.com/docs/dashboard/settings/unsubscribe-page
[vercel-env]: https://vercel.com/docs/environment-variables
[waf]: https://vercel.com/docs/vercel-firewall/vercel-waf/rate-limiting
