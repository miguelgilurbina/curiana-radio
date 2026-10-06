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
