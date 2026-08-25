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
    ];
  },
};

module.exports = nextConfig;
