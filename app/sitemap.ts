import { MetadataRoute } from 'next';
import { getAllEditions } from '@/lib/content';
import { getAllPersonajes } from '@/lib/personajes';
import { getSlugs } from '@/lib/galeria';
import { getWikiGenerado, getWikiIndice } from '@/lib/wiki';
import { getFichas, getFichasSeed } from '@/lib/fichas';
import { SITIO } from '@/lib/seo';

// lastModified sólo donde hay una fecha de verdad (la de publicación de una
// edición, la de la última exportación del vault para el wiki y el
// diccionario). Antes iba new Date() en todo: una fecha que cambia en cada
// build le enseña a Google a ignorar el campo. Donde no hay fecha, no se pone.
function fecha(iso: string | undefined | null): Date | undefined {
  return iso ? new Date(iso) : undefined;
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const editions = await getAllEditions();
  const baseUrl = SITIO.url;
  const wikiGenerado = fecha(getWikiGenerado());
  const fichasGeneradas = fecha(getFichasSeed().generado);

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      changeFrequency: 'monthly',
      priority: 1,
    },
    {
      // la landing: / es la intro El Disco, que lleva aquí
      url: `${baseUrl}/inicio`,
      changeFrequency: 'monthly',
      priority: 1,
    },
    {
      url: `${baseUrl}/archivo`,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/galeria`,
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
    { path: '/kaketiana/pueblo', priority: 0.8 },
    { path: '/kaketiana/lengua', priority: 0.8 },
    { path: '/kaketiana/experimento', priority: 0.8 },
    { path: '/kaketiana/experimento/era-1', priority: 0.5 },
    { path: '/kaketiana/bibliografia', priority: 0.7 },
    { path: '/kaketiana/personajes', priority: 0.7 },
    { path: '/kaketiana/lexicon', priority: 0.7 },
    { path: '/kaketiana/lexicon/retiradas', priority: 0.4 },
    { path: '/kaketiana/no-sabemos', priority: 0.6 },
    { path: '/kaketiana/neologisms', priority: 0.7 },
  ].map(({ path, priority }) => ({
    url: `${baseUrl}${path}`,
    changeFrequency: 'monthly' as const,
    priority,
  }));

  // Fichas de personaje (rutas dinámicas del seed curado).
  const personajePages: MetadataRoute.Sitemap = getAllPersonajes().map((p) => ({
    url: `${baseUrl}/kaketiana/personajes/${p.slug}`,
    changeFrequency: 'monthly' as const,
    priority: 0.5,
  }));

  // JAI Sounds: la curaduría musical — la portada del dial y el podcast.
  // Las páginas de mood entran cuando exista la taxonomía real.
  const jaiSoundsPages: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}/jai-sounds`,
      changeFrequency: 'weekly' as const,
      priority: 0.9,
    },
    {
      url: `${baseUrl}/jai-sounds/descubriendo`,
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    },
  ];

  // Fichas de obra de la galería.
  const galeriaPages: MetadataRoute.Sitemap = getSlugs().map((slug) => ({
    url: `${baseUrl}/galeria/${slug}`,
    changeFrequency: 'monthly' as const,
    priority: 0.5,
  }));

  // Los artículos del wiki (pueblo/lengua del vault exportado). Son el
  // contenido de fondo del sitio: prioridad alta, por encima de los anexos.
  const wikiPages: MetadataRoute.Sitemap = getWikiIndice().map((p) => ({
    url: `${baseUrl}/kaketiana/${p.seccion}/${p.slug}`,
    lastModified: wikiGenerado,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  // Las voces del diccionario, una por página: el contenido más propio del
  // sitio (no existe en ningún otro lugar con su fuente y su capa).
  const vocesPages: MetadataRoute.Sitemap = getFichas().map((f) => ({
    url: `${baseUrl}/kaketiana/lexicon/${f.slug}`,
    lastModified: fichasGeneradas,
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }));

  return [
    ...staticPages,
    ...editionPages,
    ...simuladorPages,
    ...personajePages,
    ...jaiSoundsPages,
    ...galeriaPages,
    ...wikiPages,
    ...vocesPages,
  ];
}
