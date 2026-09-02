import type { Metadata } from "next";
import IntroGate from "@/components/intro/IntroGate";

export const metadata: Metadata = {
  title: "Sintonizar — Curiana Radio",
  description:
    "La pantalla de entrada de Curiana Radio: el remolino serigráfico y la espiral del isotipo en bulto.",
  robots: { index: false, follow: true },
};

// La intro oficial, siempre. En / solo se ve una vez por sesión (IntroGate);
// aquí se puede volver a ver. Al sintonizar, va a la landing.
export default function IntroPage() {
  return <IntroGate siempre />;
}
