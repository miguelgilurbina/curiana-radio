import { Heading, BodyText } from "@/components/ui/Typography";
import FrequencyBadge from "@/components/ui/FrequencyBadge";
import { getAllEditions } from "@/lib/content";
import Link from "next/link";

export default async function Home() {
  const editions = await getAllEditions();
  const latestEdition = editions[0]; // Assuming editions are sorted by date, newest first

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-4xl mx-auto text-center animate-fade-in">
        {/* Main Title */}
        <Heading level={1} className="mb-6">
          Curiana Radio
        </Heading>

        {/* Frequency Badge */}
        <div className="flex justify-center mb-8">
          <FrequencyBadge size="lg" />
        </div>

        {/* Tagline */}
        <BodyText size="lg" className="mb-12 text-center mx-auto">
          Transmisión Cultural desde Abya Yala
        </BodyText>

        {/* Description */}
        <div className="mb-12 space-y-4">
          <BodyText className="text-center mx-auto">
            Una experiencia de newsletter cultural presentada como páginas web inmersivas.
            Cada edición mensual combina música curada, narrativa experimental, visuales generados por IA
            y reflexiones sobre tecnología y cultura.
          </BodyText>
        </div>

        {/* Latest Edition Preview */}
        {latestEdition && (
          <div className="mb-8 p-8 border-2 border-earth-200 rounded-lg hover:border-frequency transition-colors">
            <div className="text-sm font-sans tracking-[0.2em] uppercase text-earth-600 mb-2">
              Última transmisión
            </div>
            <Heading level={2} className="mb-2">
              #{latestEdition.number}: {latestEdition.title}
            </Heading>
            <p className="text-deep-700 font-serif italic mb-4">
              {latestEdition.theme}
            </p>
            <BodyText className="mb-6">
              {latestEdition.description}
            </BodyText>
            <Link
              href={`/${latestEdition.slug}`}
              className="inline-block px-8 py-4 bg-frequency text-white font-sans text-sm tracking-[0.2em] uppercase hover:bg-deep-800 transition-all duration-300"
            >
              Sintonizar Ahora
            </Link>
          </div>
        )}

        {/* Archive Link */}
        <div className="mt-8">
          <Link
            href="/archivo"
            className="text-deep-700 hover:text-frequency transition-colors font-sans text-sm tracking-wide uppercase"
          >
            Ver todas las transmisiones →
          </Link>
        </div>

        {/* Subtle hint */}
        <p className="mt-12 text-sm text-earth-600 font-sans italic">
          88.8 FM — Siempre transmitiendo
        </p>
      </div>
    </div>
  );
}
