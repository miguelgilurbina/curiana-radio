import FrequencyBadge from "@/components/ui/FrequencyBadge";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-earth-200 bg-earth-50/50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex flex-col md:flex-row items-center justify-between space-y-6 md:space-y-0">
          {/* Frequency Badge */}
          <div className="flex items-center space-x-4">
            <FrequencyBadge />
            <div className="text-sm text-earth-600 font-sans">
              Transmisión Cultural desde Abya Yala
            </div>
          </div>

          {/* Links */}
          <div className="flex items-center space-x-6 text-sm font-sans">
            <a
              href="https://github.com/miguelgilurbina/curiana-radio"
              target="_blank"
              rel="noopener noreferrer"
              className="text-deep-700 hover:text-frequency transition-colors"
            >
              GitHub
            </a>
            <span className="text-earth-400">·</span>
            <div className="text-earth-600">
              © {currentYear} Curiana Radio
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-8 pt-8 border-t border-earth-200 text-center">
          <p className="text-xs text-earth-500 font-sans leading-relaxed max-w-2xl mx-auto">
            Una experiencia de newsletter cultural presentada como páginas web inmersivas.
            Cada edición mensual es un viaje completo que combina música curada, narrativa experimental,
            visuales generadas por IA y reflexiones sobre tecnología y cultura.
          </p>
        </div>
      </div>
    </footer>
  );
}
