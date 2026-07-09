import type { ReactNode } from "react";
import Masthead from "@/components/simulador/Masthead";
import Timeline from "@/components/simulador/Timeline";
import { getRunActivo } from "@/lib/editorial";

// El chrome de las páginas interiores del simulador (léxico, neologismos,
// personajes): masthead sobre pergamino + cronología del run activo como
// navegación lateral. El landing NO usa este shell — arma su propio chrome
// por actos (laboratorio a sangre completa, luego la crónica con su
// cronología); ver app/simulador/page.tsx.
export default function SimShell({ children }: { children: ReactNode }) {
  const run = getRunActivo();
  const epocas = run.epocas.map(({ id, titulo, dias, hito }) => ({ id, titulo, dias, hito }));

  return (
    <div className="mx-auto max-w-6xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
      <Masthead />
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
