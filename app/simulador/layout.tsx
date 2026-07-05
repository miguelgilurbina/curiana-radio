import type { Metadata } from "next";
import { Overline } from "@/components/simulador/ui";
import Timeline from "@/components/simulador/Timeline";
import { getRunActivo } from "@/lib/editorial";

export const metadata: Metadata = {
  title: "Simulador — Emergencia Lingüística Caquetía | Curiana Radio",
  description:
    "Simulación multi-agente de la lengua Caquetío-Arahuaco · Golfete de Coro · Siglo XIV-XV",
};

export default function SimuladorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // La cronología del run activo es la navegación primaria de toda la
  // sección; el lector avanza en el tiempo de la simulación.
  const run = getRunActivo();
  const epocas = run.epocas.map(({ id, titulo, dias, hito }) => ({ id, titulo, dias, hito }));

  return (
    <div className="mx-auto max-w-6xl px-4 pb-24 pt-8 animate-fade-in sm:px-6 lg:px-8">
      <header className="mb-8">
        <Overline>Laboratorio lingüístico · 88.8 FM</Overline>
        <h1 className="mt-1 font-serif text-3xl font-bold text-deep-900 md:text-4xl">
          Simulador Caquetío
        </h1>
      </header>

      <div className="lg:grid lg:grid-cols-[230px_minmax(0,1fr)] lg:gap-12">
        <aside className="hidden lg:block">
          <Timeline runTitulo={run.titulo} epocas={epocas} variant="sidebar" />
        </aside>

        <div className="min-w-0">
          <div className="lg:hidden">
            <Timeline runTitulo={run.titulo} epocas={epocas} variant="bar" />
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
