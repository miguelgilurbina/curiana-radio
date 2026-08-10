import type { Metadata } from "next";
import GaleriaGrid from "@/components/galeria/GaleriaGrid";
import { Heading, BodyText } from "@/components/ui/Typography";
import { getBlobBase, getObrasGrid, getSeries, getTags } from "@/lib/galeria";

export const metadata: Metadata = {
  title: "Galería - Curiana Radio",
  description:
    "Experimentos visuales de Curiana Radio: imágenes generadas con IA sobre el desierto de Coro, la señal y la memoria caquetía.",
  openGraph: {
    title: "Galería - Curiana Radio",
    description:
      "Experimentos visuales de Curiana Radio: imágenes generadas con IA sobre el desierto de Coro, la señal y la memoria caquetía.",
  },
};

export default function GaleriaPage() {
  const obras = getObrasGrid();
  const series = getSeries();
  const tags = getTags();
  const blobBase = getBlobBase();

  return (
    <div className="min-h-screen">
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <header className="mb-14 text-center">
          <div className="mb-4 font-sans text-sm tracking-[0.2em] uppercase text-earth-600">
            Curiana Radio — 88.8 FM
          </div>
          <Heading level={1} className="mb-6">
            Galería
          </Heading>
          <BodyText className="mx-auto max-w-2xl text-deep-600">
            Experimentos visuales generados con IA. Cada imagen se publica con
            su prompt y su procedencia a la vista: la máquina es parte del
            material, no un truco que esconder.
          </BodyText>
        </header>

        {obras.length > 0 ? (
          <GaleriaGrid
            obras={obras}
            blobBase={blobBase}
            series={series}
            tags={tags}
          />
        ) : (
          <p className="py-16 text-center font-sans text-earth-600">
            Todavía no hay obras publicadas.
          </p>
        )}
      </div>
    </div>
  );
}
