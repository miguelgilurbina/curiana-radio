import Link from "next/link";
import { Heading, BodyText } from "@/components/ui/Typography";

export default function EditionNotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="max-w-2xl mx-auto text-center">
        <Heading level={1} className="mb-6">
          404
        </Heading>

        <Heading level={2} className="mb-8">
          Edición No Encontrada
        </Heading>

        <BodyText className="mb-8 text-center mx-auto">
          Lo sentimos, esta edición aún no ha sido transmitida o no existe.
          Quizás la frecuencia cambió momentáneamente.
        </BodyText>

        <div className="space-x-4">
          <Link
            href="/"
            className="inline-block px-6 py-3 border-2 border-frequency text-frequency font-sans text-sm tracking-wider hover:bg-frequency hover:text-white transition-colors"
          >
            Volver al Inicio
          </Link>

          <Link
            href="/archivo"
            className="inline-block px-6 py-3 border-2 border-deep-700 text-deep-700 font-sans text-sm tracking-wider hover:bg-deep-700 hover:text-white transition-colors"
          >
            Ver Archivo
          </Link>
        </div>
      </div>
    </div>
  );
}
