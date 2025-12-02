import { notFound } from 'next/navigation';
import { MDXRemote } from 'next-mdx-remote/rsc';
import { getEditionBySlug, getAllEditionSlugs } from '@/lib/content';
import Navigation from '@/components/layout/Navigation';
import { Heading, BodyText, Quote, Caption, SectionTitle } from '@/components/ui/Typography';
import type { Metadata } from 'next';

// MDX components mapping
const components = {
  h1: (props: any) => <Heading level={1} {...props} />,
  h2: (props: any) => <Heading level={2} {...props} />,
  h3: (props: any) => <Heading level={3} {...props} />,
  h4: (props: any) => <Heading level={4} {...props} />,
  p: (props: any) => <BodyText {...props} />,
  blockquote: (props: any) => <Quote {...props} />,
};

interface EditionPageProps {
  params: Promise<{
    edition: string;
  }>;
}

// Generate static params for all editions
export async function generateStaticParams() {
  const slugs = getAllEditionSlugs();
  return slugs.map((slug) => ({
    edition: slug,
  }));
}

// Enable dynamic params for editions not in generateStaticParams
export const dynamicParams = true;

// Generate metadata for SEO
export async function generateMetadata({ params }: EditionPageProps): Promise<Metadata> {
  const { edition: slug } = await params;
  const edition = await getEditionBySlug(slug);

  if (!edition) {
    return {
      title: 'Edition Not Found - Curiana Radio',
    };
  }

  return {
    title: `#${edition.metadata.number}: ${edition.metadata.title} - Curiana Radio`,
    description: edition.metadata.description,
    openGraph: {
      title: `#${edition.metadata.number}: ${edition.metadata.title}`,
      description: edition.metadata.description,
      type: 'article',
      publishedTime: edition.metadata.publishedAt,
      images: edition.metadata.ogImage ? [edition.metadata.ogImage] : [],
    },
  };
}

export default async function EditionPage({ params }: EditionPageProps) {
  const { edition: slug } = await params;
  const edition = await getEditionBySlug(slug);

  if (!edition) {
    notFound();
  }

  const { metadata, sections } = edition;

  return (
    <>
      {/* Pass edition number to navigation */}
      <div className="min-h-screen">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          {/* Edition Header */}
          <header className="mb-16 text-center">
            <div className="text-sm font-sans tracking-[0.2em] uppercase text-earth-600 mb-4">
              Edición #{metadata.number}
            </div>
            <Heading level={1} className="mb-4">
              {metadata.title}
            </Heading>
            <div className="text-earth-600 font-sans text-sm mb-2">
              {new Date(metadata.publishedAt).toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </div>
            <div className="text-deep-700 font-serif text-xl italic">
              {metadata.theme}
            </div>
          </header>

          {/* Intro Section */}
          {sections.intro && (
            <section className="mb-20 animate-fade-in">
              <div className="prose prose-lg max-w-none">
                <MDXRemote source={sections.intro.mdxSource} components={components} />
              </div>
            </section>
          )}

          {/* Jai Sounds Section */}
          {sections.jaiSounds && (
            <section className="mb-20 animate-fade-in">
              <SectionTitle>Jai Sounds</SectionTitle>
              <div className="prose prose-lg max-w-none">
                <MDXRemote source={sections.jaiSounds.mdxSource} components={components} />
              </div>

              {/* Spotify Embed */}
              {metadata.spotifyPlaylistId && (
                <div className="mt-8">
                  <iframe
                    src={`https://open.spotify.com/embed/playlist/${metadata.spotifyPlaylistId}?utm_source=generator&theme=0`}
                    width="100%"
                    height="380"
                    frameBorder="0"
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy"
                    className="rounded-lg shadow-lg"
                  ></iframe>
                </div>
              )}
            </section>
          )}

          {/* Hybrid Section */}
          {sections.hybrid && (
            <section className="mb-20 animate-fade-in">
              <SectionTitle>Hybrid</SectionTitle>
              <div className="prose prose-lg max-w-none">
                <MDXRemote source={sections.hybrid.mdxSource} components={components} />
              </div>
            </section>
          )}

          {/* Closing Section */}
          {sections.closing && (
            <section className="mb-20 animate-fade-in text-center">
              <div className="prose prose-lg max-w-none mx-auto">
                <MDXRemote source={sections.closing.mdxSource} components={components} />
              </div>
            </section>
          )}

          {/* Navigation to Archive */}
          <div className="text-center pt-16 border-t border-earth-200">
            <a
              href="/archivo"
              className="inline-block text-deep-700 hover:text-frequency transition-colors font-sans text-sm tracking-wide uppercase"
            >
              ← Ver todas las ediciones
            </a>
          </div>
        </div>
      </div>
    </>
  );
}
