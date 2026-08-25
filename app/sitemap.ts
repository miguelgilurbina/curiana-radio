import { MetadataRoute } from 'next';
import { getAllEditions } from '@/lib/content';
import { getAllPersonajes } from '@/lib/personajes';
import { getSlugs } from '@/lib/galeria';
import { getWikiIndice } from '@/lib/wiki';

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

  // Kaketiana: la wiki sobre el pueblo caquetío. Antes /simulador — el
  // renombrado y sus redirects están en next.config.js.
  const simuladorPages: MetadataRoute.Sitemap = [
    { path: '/kaketiana', priority: 0.9 },
    { path: '/kaketiana/experimento', priority: 0.8 },
    { path: '/kaketiana/bibliografia', priority: 0.7 },
    { path: '/kaketiana/personajes', priority: 0.7 },
    { path: '/kaketiana/lexicon', priority: 0.7 },
    { path: '/kaketiana/neologisms', priority: 0.7 },
  ].map(({ path, priority }) => ({
    url: `${baseUrl}${path}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority,
  }));

  // Fichas de personaje (rutas dinámicas del seed curado).
  const personajePages: MetadataRoute.Sitemap = getAllPersonajes().map((p) => ({
    url: `${baseUrl}/kaketiana/personajes/${p.slug}`,
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

  // Los artículos del wiki (pueblo/lengua del vault exportado). Son el
  // contenido de fondo del sitio: prioridad alta, por encima de los anexos.
  const wikiPages: MetadataRoute.Sitemap = getWikiIndice().map((p) => ({
    url: `${baseUrl}/kaketiana/${p.seccion}/${p.slug}`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  return [
    ...staticPages,
    ...editionPages,
    ...simuladorPages,
    ...personajePages,
    ...jaiSoundsPages,
    ...galeriaPages,
    ...wikiPages,
  ];
}
