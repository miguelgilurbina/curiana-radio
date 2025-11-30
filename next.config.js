/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    formats: ['image/webp', 'image/avif'],
  },
  // We'll add MDX support after installing next-mdx-remote
};

module.exports = nextConfig;
