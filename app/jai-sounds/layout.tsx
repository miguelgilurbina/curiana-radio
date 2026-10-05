import type { Metadata } from "next";
import localFont from "next/font/local";
import { SCRIPT_SEMILLA } from "@/lib/jai-rotacion";

export const metadata: Metadata = {
  title: "JAI Sounds — Curaduría musical | Curiana Radio",
  description:
    "La música es la huella humana de la vida vivida. Curaduría musical de Curiana Radio: un dial de estaciones que gira de color, no de canciones.",
  openGraph: {
    title: "JAI Sounds — Curaduría musical",
    description:
      "jai · caquetío · oír, escuchar. Un dial de estaciones desde Curiana Radio · 88.8 FM",
    type: "website",
  },
};

// La Fraunces de JAI: la misma familia del sitio, pero con los ejes que la
// sección necesita y el resto no — opsz (la display vive en opsz 9, tripas
// gruesas) e itálica (la voz de Descubriendo con Chocolate).
//
// Va como fuente LOCAL a propósito. Con next/font/google las dos instancias
// se registran con el mismo nombre de familia ("Fraunces"), y al navegar de
// JAI al simulador la de JAI (con opsz) le pisaría la display: .sim-display
// usa opsz automático y cambiaría de contraste. Local, la familia se llama
// distinto y no se cruzan. Los archivos son el subconjunto latino de Google
// Fonts (OFL, github.com/undercasetype/Fraunces), con opsz 9-144, wght,
// SOFT y WONK.
const frauncesJai = localFont({
  src: [
    { path: "./fuentes/fraunces-jai.woff2", style: "normal", weight: "100 900" },
    {
      path: "./fuentes/fraunces-jai-italica.woff2",
      style: "italic",
      weight: "100 900",
    },
  ],
  variable: "--font-fraunces-jai",
  display: "swap",
  fallback: ["Georgia", "serif"],
  adjustFontFallback: "Times New Roman",
});

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
