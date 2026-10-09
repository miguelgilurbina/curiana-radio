import Link from "next/link";
import Sello from "@/components/shell/Sello";
import EscalaDial from "@/components/shell/EscalaDial";
import Suscripcion from "@/components/landing/Suscripcion";
import { REDES } from "@/lib/redes";
import { VOZ } from "./voces";

// Señales sin señales (Miguel, 2026-10-08: «que el estado vacío sea una vista
// trabajada, no una línea»). Va en la piel de la radio y habla el idioma del
// shell: la escala del dial con su aguja buscando la estación, el sello, el
// dato en mono. Mientras tanto, la señal sigue en las redes, el RSS y el
// correo. La aguja busca una sola vez (4.5 s) y se queda; con movimiento
// reducido, quieta. El copy de la nota es un borrador en la voz de «Quién
// transmite» (/sobre): Miguel lo cambia.

const DATO = `${VOZ.dato} text-(--e-texto-2)`;
const FILA =
  "group flex min-h-11 items-baseline justify-between gap-4 border-b border-(--e-filete) py-3 transition-colors duration-300";
const DESTINO =
  "font-serif text-lg font-semibold text-(--e-texto) transition-colors duration-300 group-hover:text-(--e-enlace-hover)";

export default function SenalesVacia() {
  return (
    <section aria-labelledby="senales-afinando" className="flex flex-col gap-12 sm:gap-16">
      {/* el dial, buscando: decoración */}
      <div aria-hidden="true" className="flex flex-col gap-2.5 border-t border-(--e-filete) pt-8">
        <div className="relative">
          <EscalaDial alto={18} className="hidden sm:block" />
          <EscalaDial alto={14} paso={12} className="sm:hidden" />
          <span className="senales-aguja" />
        </div>
        <div className={`flex justify-between gap-4 ${DATO}`}>
          <span>87.5</span>
          <span>Buscando la primera señal</span>
          <span className="hidden sm:inline">108</span>
        </div>
      </div>

      {/* el sello y la nota */}
      <div className="grid gap-7 sm:grid-cols-[auto_minmax(0,1fr)] sm:gap-12">
        <Sello tamano={72} className="sm:hidden" />
        <Sello tamano={128} className="hidden sm:block" />
        <div className="flex max-w-[34rem] flex-col gap-6">
          <h2
            id="senales-afinando"
            className={`m-0 ${VOZ.titulo} text-[clamp(1.9rem,4.4vw,2.9rem)] leading-[1.1] text-(--e-titulo)`}
          >
            La primera señal se está afinando.
          </h2>
          <figure className="m-0 flex flex-col gap-3 [border-left:2px_solid_var(--e-riel)] pl-5">
            <blockquote className={`m-0 ${VOZ.sumario} text-[clamp(1.08rem,2vw,1.3rem)] leading-[1.55] text-(--e-texto-2)`}>
              <p className="m-0">
                Aquí voy a escribir yo, desde acá: lo que anoto en la libreta, lo que escucho, lo que imagino. La
                primera todavía no sale; mientras tanto, la radio sigue al aire.
              </p>
            </blockquote>
            <figcaption className={DATO}>
              —{" "}
              <Link href="/sobre" className={VOZ.accion}>
                Miguel Gil Urbina →
              </Link>
            </figcaption>
          </figure>
        </div>
      </div>

      {/* mientras tanto: las redes, el RSS y el correo */}
      <div className="grid gap-10 border-t border-(--e-filete) pt-8 md:grid-cols-2 md:gap-12">
        <div className="flex flex-col gap-2">
          <h3 className={`m-0 font-normal ${DATO}`}>Mientras tanto, la señal sigue en</h3>
          <ul className="m-0 flex list-none flex-col p-0">
            {REDES.map((r) => (
              <li key={r.nombre}>
                <a href={r.url} target="_blank" rel="noopener noreferrer" className={FILA}>
                  <span className={DATO}>{r.nombre}</span>
                  <span className={DESTINO}>
                    {r.usuario} <span aria-hidden="true">↗</span>
                  </span>
                </a>
              </li>
            ))}
            <li>
              <a href="/senales/rss.xml" className={FILA}>
                <span className={DATO}>RSS</span>
                <span className={DESTINO}>la primera, en tu lector</span>
              </a>
            </li>
          </ul>
        </div>

        {/* La suscripción es del shell: va en una placa que se queda de noche
            aunque el lector haya pasado la radio a claro (globals.css). */}
        <div className="shell-noche flex flex-col gap-3.5 self-start border border-(--noche-filete) bg-(--noche-panel) p-5 sm:p-6">
          <h3 className="m-0 font-mono text-[0.625rem] font-normal tracking-[0.3em] text-(--noche-dato)">
            QUE TE LLEGUE AL CORREO
          </h3>
          <Suscripcion variante="pie" />
        </div>
      </div>

      <Link href="/inicio" className={`self-start ${DATO} ${VOZ.accion}`}>
        ← Volver a la radio
      </Link>
    </section>
  );
}
