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
    // El pergamino del cronista: fondo propio de la sección, tapa el
    // gradiente global de la radio sin tocarla (tokens en globals.css).
    <div data-sim-theme="cronista" className="min-h-screen bg-(--sim-paper)">
      <div className="mx-auto max-w-6xl px-4 pb-24 pt-8 animate-fade-in sm:px-6 lg:px-8">
      {/* Masthead de revista: filete doble, nameplate en display, línea de edición */}
      <header className="mb-10">
        <div className="sim-double-rule" aria-hidden="true" />
        <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 py-3">
          <h1 className="sim-display text-4xl font-semibold tracking-tight text-(--sim-ink) md:text-5xl">
            Simulador Caquetío
          </h1>
          <Overline>Laboratorio lingüístico · 88.8 FM</Overline>
        </div>
        <div className="border-b border-(--sim-ink)" aria-hidden="true" />
        <p className="sim-mono mt-2 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
          Golfete de Coro · Siglos XIV–XV · Una crónica que se sigue escribiendo
        </p>
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
    </div>
  );
}
