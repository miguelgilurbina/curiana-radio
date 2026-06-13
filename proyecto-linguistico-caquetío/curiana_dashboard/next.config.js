/** @type {import('next').NextConfig} */
const nextConfig = {
  // La lectura de Supabase real-time usa WebSockets — no necesita config especial.
  // Si en el futuro agregas imágenes de dominio externo, añádelas aquí:
  // images: { domains: ["..."] },
};

module.exports = nextConfig;
