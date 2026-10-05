import type { Metadata } from "next";
import IntroDisco from "@/components/intro/IntroDisco";
import { metadatos } from "@/lib/seo";

export const metadata: Metadata = metadatos({
  titulo: "Sintonizar — Curiana Radio",
  descripcion:
    "La pantalla de entrada de Curiana Radio: un disco de arena donde el viento se ordena en la espiral del isotipo.",
  ruta: "/intro",
  noIndex: true,
});

// La intro, siempre. En / solo se ve una vez por sesión; aquí se puede volver
// a ver. Al sintonizar, va a la landing.
export default function IntroPage() {
  return <IntroDisco siempre />;
}
