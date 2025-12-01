import { Heading, BodyText } from "@/components/ui/Typography";
import FrequencyBadge from "@/components/ui/FrequencyBadge";

export default function Home() {
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

        {/* Coming Soon Badge */}
        <div className="inline-block px-8 py-4 border-2 border-frequency text-frequency font-sans text-sm tracking-[0.2em] uppercase hover:bg-frequency hover:text-white transition-all duration-300 cursor-pointer">
          Próximamente
        </div>

        {/* Subtle hint */}
        <p className="mt-12 text-sm text-earth-600 font-sans italic">
          Sintoniza la frecuencia. La primera transmisión está por comenzar.
        </p>
      </div>
    </div>
  );
}
