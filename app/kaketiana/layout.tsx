import type { Metadata } from "next";
import NavKaketiana from "@/components/kaketiana/NavKaketiana";

export const metadata: Metadata = {
  title: "Kaketiana — el mundo del kaketío | Curiana Radio",
  description:
    "El wiki de investigación sobre el pueblo caquetío del Golfete de Coro (siglos XIV-XV) y la reconstrucción de su lengua, con un experimento de simulación. Cada afirmación con su fuente.",
};

// El marco de toda la sección, del manual de Kaketiana (design_handoff_
// kaketiana): la placa 6b «Sal y almagre» (data-kk-dir="sal", que gana sobre
// el pergamino del cronista porque se declara después en globals.css), los
// micro-labels del manual (data-kk) y una sola navegación para todas las
// páginas. El experimento redefine sus tramos a la tinta del laboratorio
// (data-sim-acto="laboratorio"): esa inversión es la firma del Acto I.
export default function KaketianaLayout({ children }: { children: React.ReactNode }) {
  return (
    <div
      data-sim-theme="cronista"
      data-kk
      data-kk-dir="sal"
      className="min-h-screen bg-(--sim-paper) animate-fade-in"
    >
      <NavKaketiana />
      {children}
    </div>
  );
}
