import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      // /jai-sounds/muestra son maquetas con datos inventados. La página ya
      // lleva noindex en su metadata; esto es el segundo cinturón, para que
      // ni siquiera se rastree mientras exista.
      disallow: ['/jai-sounds/muestra'],
    },
    sitemap: 'https://curianaradio.com/sitemap.xml',
  };
}
