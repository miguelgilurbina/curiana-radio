# Medición: qué se cuenta y para qué

Fecha: 2026-10-05. Cubre J4 del [`PLAN_MAESTRO`](proyecto-linguistico-caquetío/1-plan/PLAN_MAESTRO.md)
(«sin datos, "efectivo" seguirá siendo una sensación») y prepara J5, el motivo
de negocio. No decide cómo se monetiza: decide **qué hay que saber antes** de
decidirlo, y deja el sitio contándolo.

---

## 1. Qué se cuenta

**Solo, sin código propio** (Vercel Web Analytics + Speed Insights, en
`components/analitica/Analitica.tsx`): visitas por página, visitantes,
referentes (de dónde llegan), país, dispositivo, y el rendimiento real de quien
visita. Sin cookies: no hace falta banner de consentimiento.

**Eventos propios** (`lib/analitica.ts`, máximo 2 propiedades cada uno):

| Evento | Cuándo | Propiedades | Qué pregunta responde |
|---|---|---|---|
| `suscripcion` | alguien confirmó su correo (el segundo paso del doble opt-in, en `/suscripcion/confirmar`) | `desde` = el tema: `edicion` o `senales` | ¿la radio convierte visitas en audiencia propia? ¿qué frecuencia eligen? |
| `lectura` | llegó al final de un artículo o edición y lleva ≥ 20 s en la página | `pagina` | ¿se lee o se hojea? qué textos se terminan |
| `salida` | clic en cualquier enlace externo | `destino`, `desde` | ¿a Spotify (JAI), al repo, a las fuentes (archive.org…)? |
| `estacion` | pasó a otra estación de la batea de JAI Sounds | `estacion` | qué curaduría engancha |
| `obra` | abrió una obra de la galería en grande | `obra` | qué piezas tienen demanda (licencia, print) |
| `intro` | saltó el afinado o sintonizó en El Disco | `accion` | ¿la intro retiene o expulsa? |

Ningún evento lleva el correo ni nada que identifique a nadie.

## 2. Para encenderlo

1. **Vercel → proyecto curiana-radio → Analytics → Enable**, y lo mismo en
   **Speed Insights**. Sin eso, los scripts (`/_vercel/insights/…`) responden 404
   y no se cuenta nada.
2. **Eventos propios**: sólo existen en el plan **Pro**. En Hobby no se
   registran, por eso el código los tiene apagados. Al pasar a Pro, agregar
   `NEXT_PUBLIC_ANALITICA_EVENTOS=1` a las variables de producción y redeployar.
3. **Search Console y Bing Webmaster Tools**: verificar `curianaradio.com` por
   DNS (registro TXT en Vercel → Domains) y enviar `/sitemap.xml`. Bing importa
   la verificación de Google en un clic, y el índice de Bing alimenta Copilot y
   parte de las búsquedas de ChatGPT: cuenta para el tráfico desde IA.

### Lo que el plan Hobby no alcanza

| | Hobby | Pro (US$20/mes) |
|---|---|---|
| Eventos al mes | 50.000 (después se pausa) | por uso, US$0,03 cada mil |
| Historia que se guarda | **1 mes** | 12 meses |
| Eventos propios | no | sí, 2 propiedades |
| UTM (`?utm_source=linkedin`) | no | con Web Analytics Plus (+US$10) |

Para decidir monetización hace falta comparar meses, y Hobby borra el mes
anterior. **Recomendación:** pasar a Pro cuando arranque la difusión (el
ensayo de LinkedIn, IG, YouTube), no antes; hasta entonces el tráfico es
mínimo y lo que hay se ve igual en Hobby.

## 3. Las hipótesis y la señal que las prueba

Cada arista tiene una vía de ingreso plausible. Lo que sigue es qué número
mirar para saber si vale la pena construirla, no la decisión.

| Arista | Vía plausible | La señal | Cuándo se mira |
|---|---|---|---|
| **La radio** (ediciones, newsletter) | apoyo de la audiencia: membresía o donación recurrente | `suscripcion` ÷ visitas al sitio (el formulario está en el pie de todas las páginas); `lectura` de ediciones | cuando Miguel configure Resend ([`NEWSLETTER.md`](NEWSLETTER.md)); hasta entonces el formulario está cerrado |
| **Kaketiana** | patrocinio cultural, fondos de patrimonio y de lenguas indígenas, universidades; a la larga, el diccionario impreso | `lectura` de artículos; voces más visitadas; `salida` hacia fuentes; **referentes chatgpt.com, perplexity.ai, claude.ai, bing.com** | a los 3 meses de difusión. Un fondo pide alcance demostrable: esto es esa evidencia |
| **JAI Sounds** | patrocinio de la curaduría; curaduría por encargo | `estacion`; `salida` → open.spotify.com | a los 3 meses |
| **Galería** | licencias primero, print después (decidido en [`GALERIA_PLAN.md`](GALERIA_PLAN.md) §1.1) | `obra` (las más ampliadas son el catálogo a licenciar); visitas a `/galeria/[slug]` desde buscadores de imágenes | cuando haya licencias publicadas |

Lo que no está en la tabla a propósito: **publicidad**. Necesita un volumen de
visitas que un proyecto así no tiene ni busca, y ensucia la página.

## 4. Cómo se lee

- **Tráfico desde IA**: en Analytics → Referrers. ChatGPT agrega
  `utm_source=chatgpt.com` a sus enlaces; en Hobby se ve el referente igual.
  Es la medida de si `/llms.txt`, el JSON-LD y la política de `robots.txt`
  («buscadores sí, entrenamiento no») están funcionando.
- **Eventos por propiedad**: Analytics → Events → elegir el evento → agrupar por
  propiedad. Desde la API: `GET /v1/query/web-analytics/events/aggregate`.
- **Lecturas**: `lectura` ÷ visitas de la misma página = tasa de lectura
  completa. Es el número que importa para Kaketiana; las visitas solas no
  distinguen al que lee del que rebota.
