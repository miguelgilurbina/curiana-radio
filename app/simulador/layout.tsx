import type { Metadata } from "next";
import { Overline } from "@/components/simulador/ui";
import SubNav from "@/components/simulador/SubNav";

export const metadata: Metadata = {
  title: "Simulador — Emergencia Lingüística Caquetía | Curiana Radio",
  description:
    "Simulación multi-agente de la lengua Caquetío-Arahuacana · Golfete de Coro · Siglo XIV-XV",
};

export default function SimuladorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 pb-24 pt-8 animate-fade-in">
      <header className="mb-6">
        <Overline>Laboratorio lingüístico · 88.8 FM</Overline>
        <h1 className="mt-1 font-serif text-3xl md:text-4xl font-bold text-deep-900">
          Simulador Caquetío
        </h1>
      </header>
      <div className="mb-8">
        <SubNav />
      </div>
      {children}
    </div>
  );
}
