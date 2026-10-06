import type { Metadata } from "next";
import { frauncesJai } from "./fraunces-jai";
import { SCRIPT_SEMILLA } from "@/lib/jai-rotacion";

export const metadata: Metadata = {
  title: "JAI Sounds — Curaduría musical | Curiana Radio",
  description:
    "La música es la huella humana de la vida vivida. Curaduría musical de Curiana Radio: un dial de estaciones que gira de color, no de canciones.",
  openGraph: {
    title: "JAI Sounds — Curaduría musical",
    description:
      "jay · caquetío · oír, escuchar. Un dial de estaciones desde Curiana Radio · 88.8 FM",
    type: "website",
  },
};

// El layout solo fija el registro de la sección; el chrome lo arma cada
// página. Mismo patrón que /simulador: la arista es dueña de su tema.
export default function JaiSoundsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      data-jai-theme="dial"
      className={`${frauncesJai.variable} min-h-screen bg-(--jai-noche) text-(--jai-luz) animate-fade-in`}
    >
      {/* La semilla del dial, antes del primer pintado (lib/jai-rotacion). */}
      <script dangerouslySetInnerHTML={{ __html: SCRIPT_SEMILLA }} />
      {children}
    </div>
  );
}
