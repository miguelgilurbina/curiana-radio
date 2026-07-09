/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    formats: ['image/webp', 'image/avif'],
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
