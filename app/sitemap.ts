import { MetadataRoute } from 'next';
import { getAllEditions } from '@/lib/content';

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
  ];

  // Edition pages
  const editionPages: MetadataRoute.Sitemap = editions.map((edition) => ({
    url: `${baseUrl}/${edition.slug}`,
    lastModified: new Date(edition.publishedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.9,
  }));

  return [...staticPages, ...editionPages];
}
