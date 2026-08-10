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
        destination: '/simulador#bitacora',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;
