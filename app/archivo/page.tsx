import { getAllEditions } from '@/lib/content';
import EditionCard from '@/components/archive/EditionCard';
import { Heading, BodyText } from '@/components/ui/Typography';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Archivo - Curiana Radio',
  description: 'Todas las transmisiones de Curiana Radio. Explora ediciones pasadas, descubre nuevas frecuencias.',
  openGraph: {
    title: 'Archivo - Curiana Radio',
    description: 'Todas las transmisiones de Curiana Radio. Explora ediciones pasadas, descubre nuevas frecuencias.',
  },
};

export default async function ArchivoPage() {
  const editions = await getAllEditions();

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Page Header */}
        <header className="mb-16 text-center">
          <div className="text-sm font-sans tracking-[0.2em] uppercase text-earth-600 mb-4">
            Curiana Radio — 88.8 FM
          </div>
          <Heading level={1} className="mb-6">
            Archivo de Transmisiones
          </Heading>
          <BodyText className="max-w-2xl mx-auto text-deep-600">
            Cada edición es una frecuencia única. Explora las transmisiones pasadas y sintoniza
            las conversaciones entre música, tecnología y contemplación.
          </BodyText>
        </header>

        {/* Editions Grid */}
        {editions.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {editions.map((edition) => (
              <EditionCard key={edition.slug} edition={edition} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <BodyText className="text-deep-600">
              No hay ediciones disponibles en este momento.
            </BodyText>
          </div>
        )}
      </div>
    </div>
  );
}
