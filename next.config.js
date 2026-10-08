// ── Cabeceras de seguridad ─────────────────────────────────────────────
// El sitio es estático y no tiene sesiones; su único formulario (el newsletter)
// postea al mismo origen (/api/suscripcion). Lo que se protege es al lector:
// que nadie meta la radio en un iframe ajeno, que una inyección no pueda cargar
// scripts de otro dominio ni mandar datos a otro lado, que el navegador no
// adivine tipos. La CSP lista a mano cada tercero que el sitio usa a
// propósito; si se agrega uno (un proveedor, un embed), va aquí o el
// navegador lo bloquea y lo dice en la consola.
//
// 'unsafe-inline' en script-src no es descuido: Next mete el payload de RSC
// en <script> en línea y la única alternativa (nonces) obliga a renderizar
// cada página por pedido, que este sitio 100% estático no necesita.
const esDev = process.env.NODE_ENV !== 'production';
// Las vistas previas llevan la barra de Vercel (comentarios), que carga de
// vercel.live. Producción no la necesita.
const esVistaPrevia = process.env.VERCEL_ENV === 'preview';

const BLOB = 'https://*.public.blob.vercel-storage.com';
const csp = {
  'default-src': ["'self'"],
  'script-src': [
    "'self'",
    "'unsafe-inline'",
    esDev && "'unsafe-eval'",
    // En desarrollo @vercel/analytics carga su script de depuración de aquí;
    // en producción lo sirve el propio dominio (/_vercel/insights).
    esDev && 'https://va.vercel-scripts.com',
    esVistaPrevia && 'https://vercel.live',
  ],
  'style-src': ["'self'", "'unsafe-inline'", esVistaPrevia && 'https://vercel.live'],
  'img-src': [
    "'self'",
    'data:',
    'blob:',
    BLOB,
    // las teselas de los mapas de Kaketiana (Leaflet)
    'https://tile.openstreetmap.org',
    // las portadas de álbum del wiki de JAI Sounds (CDN de Spotify)
    'https://i.scdn.co',
    esVistaPrevia && 'https://vercel.live',
    esVistaPrevia && 'https://vercel.com',
  ],
  'font-src': [
    "'self'",
    'data:',
    esVistaPrevia && 'https://vercel.live',
    esVistaPrevia && 'https://assets.vercel.com',
  ],
  'connect-src': [
    // el newsletter postea a /api/suscripcion y Resend se llama desde el
    // servidor: el navegador no habla con ningún proveedor de correo
    "'self'",
    esDev && 'ws:',
    esVistaPrevia && 'https://vercel.live',
    esVistaPrevia && 'wss://ws-us3.pusher.com',
  ],
  'media-src': ["'self'", BLOB],
  // los reproductores de JAI Sounds y de las ediciones, y los videos de
  // Señales (youtube-nocookie: sin cookies hasta que alguien le da play)
  'frame-src': [
    'https://open.spotify.com',
    'https://www.youtube-nocookie.com',
    esVistaPrevia && 'https://vercel.live',
  ],
  'worker-src': ["'self'", 'blob:'],
  'manifest-src': ["'self'"],
  'object-src': ["'none'"],
  'base-uri': ["'self'"],
  'form-action': ["'self'"],
  'frame-ancestors': ["'none'"],
};
const politica = Object.entries(csp)
  .map(([directiva, fuentes]) => [directiva, ...fuentes.filter(Boolean)].join(' '))
  .join('; ');

const cabecerasDeSeguridad = [
  { key: 'Content-Security-Policy', value: politica },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  // strict-origin-when-cross-origin y no no-referrer: la política de uso de
  // las teselas de OpenStreetMap pide un Referer válido.
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
  // Sólo lo que el sitio nunca usa. autoplay, encrypted-media y fullscreen
  // quedan libres porque el embed de Spotify los pide.
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()',
  },
];

// Las secciones que siguen en el taller (Miguel, 2026-10-06): la Galería, el
// archivo de ediciones y las ediciones mismas (/01…). En producción vuelven a
// la radio; en local y en las vistas previas se ven, para seguir trabajándolas.
// Va a la par de LIBERADA en lib/secciones.ts: al liberar una, sale de aquí.
const SIN_LIBERAR =
  process.env.VERCEL_ENV === 'production'
    ? ['/galeria', '/galeria/:path*', '/archivo', '/:edicion(\\d{1,3})'].map((source) => ({
        source,
        destination: '/inicio',
        permanent: false,
      }))
    : [];

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  // Next 16.3 escribe AGENTS.md y CLAUDE.md en la raíz cada vez que arranca
  // `next dev`. El repo ya tiene su CLAUDE.md y no quiere el otro.
  agentRules: false,
  async headers() {
    return [{ source: '/:path*', headers: cabecerasDeSeguridad }];
  },
  images: {
    formats: ['image/webp', 'image/avif'],
    // La galería NO usa este optimizador: sus imágenes ya se sirven como
    // WebP pre-generado desde Blob con un <img srcset>, justo para no gastar
    // transformaciones facturables (ver GALERIA.md). Este patrón queda
    // habilitado para cualquier otro uso de next/image sobre Blob.
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.public.blob.vercel-storage.com',
      },
    ],
  },
  // We'll add MDX support after installing next-mdx-remote
  async redirects() {
    return [
      // 2026-09-28 — el dominio propio. La dirección vieja de Vercel manda al
      // dominio nuevo con la misma ruta, para que los enlaces viejos no mueran
      // y no haya dos copias del sitio. Sólo atrapa ese host exacto: las
      // vistas previas de las ramas (otros *.vercel.app) no se tocan.
      {
        source: '/:path*',
        has: [{ type: 'host', value: 'curiana-radio.vercel.app' }],
        destination: 'https://curianaradio.com/:path*',
        permanent: true,
      },
      // /simulador/runs se fusionó al landing de tres actos (Acto I).
      {
        source: '/simulador/runs',
        destination: '/kaketiana/experimento#bitacora',
        permanent: true,
      },
      // 2026-08-24 — /simulador pasó a ser /kaketiana ("el lugar de la gente").
      // La sección dejó de ser "el simulador con anexos" para ser una wiki
      // sobre el pueblo caquetío, con el experimento como una parte más.
      // El landing de tres actos se mudó a /kaketiana/experimento.
      {
        source: '/simulador',
        destination: '/kaketiana',
        permanent: true,
      },
      // Las fichas de fuente dejaron de tener página propia: ahora son
      // bibliografía, con ancla por obra.
      {
        source: '/simulador/fuentes/:seccion/:slug',
        destination: '/kaketiana/bibliografia',
        permanent: true,
      },
      {
        source: '/simulador/fuentes',
        destination: '/kaketiana/bibliografia',
        permanent: true,
      },
      {
        source: '/simulador/:path*',
        destination: '/kaketiana/:path*',
        permanent: true,
      },
      ...SIN_LIBERAR,
    ];
  },
};

module.exports = nextConfig;
