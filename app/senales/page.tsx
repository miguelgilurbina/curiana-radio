import Link from "next/link";
import type { Metadata } from "next";
import { getSenales, hayPublicadas } from "@/lib/senales";
import FiltroSenales from "@/components/senales/FiltroSenales";
import InterruptorLuz from "@/components/senales/InterruptorLuz";
import SenalesVacia from "@/components/senales/SenalesVacia";
import { radio } from "@/components/senales/pieles/radio";
import { VOZ } from "@/components/senales/voces";
import { REDES } from "@/lib/redes";

// Mientras no haya ninguna publicada, el índice existe por URL pero no se
// indexa (ni entra al sitemap ni se enlaza desde el shell: lib/senales.ts).
// El resto de la metadata la pone el layout.
export const metadata: Metadata = hayPublicadas() ? {} : { robots: { index: false, follow: true } };

// El índice de Señales (design_handoff_senales_luces, «Índice de Señales»):
// siempre en la piel de la radio y siguiendo el interruptor global. Lee los
// alias --e-* de esa piel, como la plantilla de una entrada. Sin señales, la
// vista de espera (SenalesVacia).
export default function Senales() {
  const senales = getSenales();
  const dato = `${VOZ.dato} text-(--e-texto-2)`;

  return (
    <div {...radio.atributos} data-piel={radio.id} className="min-h-screen px-6 pt-12 pb-28 animate-fade-in sm:pt-16">
      <div className="mx-auto flex max-w-[56rem] flex-col gap-7">
        <div className={`flex flex-wrap items-center justify-between gap-x-6 gap-y-1 ${dato}`}>
          <span>Curiana Radio / Señales</span>
          <InterruptorLuz nativo={radio.nativo} alterno={radio.alterno} activo="text-(--e-texto)" className={dato} />
        </div>

        <header className="flex flex-col gap-2.5">
          <h1 className="m-0 font-serif text-[clamp(2.2rem,5.4vw,3.5rem)] leading-[1.08] font-semibold">Señales</h1>
          <p className="m-0 max-w-[46ch] font-serif text-[clamp(1.05rem,2.2vw,1.3rem)] leading-[1.5] italic text-(--e-texto-2)">
            La radio transmite desde después. Las señales se escriben desde acá.
          </p>
          {/* sin señales, la firma, las redes y el RSS van en la vista de espera */}
          {senales.length > 0 && (
            <p className={`m-0 mt-1.5 flex flex-wrap items-center gap-x-4 gap-y-1 ${dato}`}>
              <Link href="/sobre" className={VOZ.accion}>
                Escribe Miguel Gil Urbina →
              </Link>
              {REDES.map((r) => (
                <a key={r.nombre} href={r.url} target="_blank" rel="noopener noreferrer" className={VOZ.accion}>
                  {r.nombre}
                </a>
              ))}
              <a href="/senales/rss.xml" className={VOZ.accion}>
                RSS
              </a>
            </p>
          )}
        </header>

        {senales.length > 0 ? <FiltroSenales senales={senales} /> : <SenalesVacia />}
      </div>
    </div>
  );
}
