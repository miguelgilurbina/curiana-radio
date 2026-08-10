import { MetadataRoute } from 'next';
import { getAllEditions } from '@/lib/content';
import { getAllPersonajes } from '@/lib/personajes';
import { getSlugs } from '@/lib/galeria';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const editions = await getAllEditions();
  const baseUrl = 'https://curianaradio.com';

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 1,
    },
    {
      url: `${baseUrl}/archivo`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/galeria`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ];

  // Edition pages
  const editionPages: MetadataRoute.Sitemap = editions.map((edition) => ({
    url: `${baseUrl}/${edition.slug}`,
    lastModified: new Date(edition.publishedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.9,
  }));

  // Simulador: la sección de contenido evergreen (antes ausente del sitemap).
  // /simulador/runs se fusionó al landing (Acto I) — redirect en next.config.js.
  const simuladorPages: MetadataRoute.Sitemap = [
    { path: '/simulador', priority: 0.9 },
    { path: '/simulador/personajes', priority: 0.7 },
    { path: '/simulador/lexicon', priority: 0.7 },
    { path: '/simulador/neologisms', priority: 0.7 },
  ].map(({ path, priority }) => ({
    url: `${baseUrl}${path}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority,
  }));

  // Fichas de personaje (rutas dinámicas del seed curado).
  const personajePages: MetadataRoute.Sitemap = getAllPersonajes().map((p) => ({
    url: `${baseUrl}/simulador/personajes/${p.slug}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: 0.5,
  }));

  // JAI Sounds: la curaduría musical. Por ahora solo la portada del dial;
  // las páginas de mood entran cuando exista la taxonomía real.
  const jaiSoundsPages: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}/jai-sounds`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    },
  ];

  // Fichas de obra de la galería.
  const galeriaPages: MetadataRoute.Sitemap = getSlugs().map((slug) => ({
    url: `${baseUrl}/galeria/${slug}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: 0.5,
  }));

  return [
    ...staticPages,
    ...editionPages,
    ...simuladorPages,
    ...personajePages,
    ...jaiSoundsPages,
    ...galeriaPages,
  ];
}
