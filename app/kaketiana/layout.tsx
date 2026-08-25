import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Simulador — Emergencia Lingüística Caquetía | Curiana Radio",
  description:
    "Simulación multi-agente de la lengua Caquetío-Arahuaco · Golfete de Coro · Siglo XIV-XV",
};

// El layout solo pone el tema del cronista y el fondo de la sección; el
// chrome (masthead + cronología) lo arma cada página: las interiores vía
// SimShell, el landing por actos — el Acto I "laboratorio" va a sangre
// completa y redefine los tokens --sim-* al registro oscuro.
export default function SimuladorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div data-sim-theme="cronista" className="min-h-screen bg-(--sim-paper) animate-fade-in">
      {children}
    </div>
  );
}
