// El umbral: la transición wiki → experimento del manual de Kaketiana
// (design_handoff_kaketiana, Vistas §05). Arranca en la placa clara del wiki
// (6b «Sal y almagre»), anochece en una banda sin texto y del otro lado ya es
// la tinta del laboratorio, que es firma exclusiva del Acto I: ahí la escala
// epistémica va de la evidencia a la ficción —▮ → ◆ → ◇ → ◉— con los tokens
// del registro oscuro, y el degradado termina en el mismo #0f1621 del
// laboratorio, sin corte. (El handoff pone la escala a media transición; aquí
// va del lado oscuro para que todas las etiquetas se lean.)
import Masthead from "@/components/simulador/Masthead";
import Etiqueta from "@/components/kaketiana/Etiqueta";
import type { AbstractContent } from "@/lib/abstract";

export default function Umbral({ umbral, destino }: { umbral: AbstractContent["umbral"]; destino: string }) {
  const [antes, despues] = umbral.ficcion.split("ficción declarada");
  return (
    <section aria-label="El umbral del experimento">
      <div data-kk-dir="sal" className="kk-umbral-claro">
        <div className="mx-auto max-w-6xl px-4 pt-8 sm:px-6 lg:px-8">
          <Masthead />
        </div>
        <div className="mx-auto flex max-w-[65ch] flex-col gap-4 px-4 pb-14 pt-8 sm:px-6 md:pt-14">
          <span className="kk-label text-(--sim-ink-soft)">{umbral.miga}</span>
          <h2 className="sim-display text-4xl font-semibold leading-[1.08] tracking-tight text-(--sim-ink) md:text-[2.6rem]">
            {umbral.titulo.map((linea, i) => (
              <span key={i} className="block">
                {linea}
              </span>
            ))}
          </h2>
          <p className="font-serif text-lg italic leading-[1.7] text-(--sim-ink-soft)">{umbral.entrada}</p>
        </div>
      </div>

      <div className="kk-umbral-banda h-28 md:h-40" aria-hidden="true" />

      <div data-sim-acto="laboratorio" className="bg-(--sim-paper)">
        <div className="mx-auto flex max-w-[65ch] flex-col gap-8 px-4 pb-16 pt-2 sm:px-6 md:pb-20">
          <p
            className="flex flex-wrap items-center gap-x-4 gap-y-3"
            aria-label="De lo atestiguado a la ficción declarada"
          >
            <Etiqueta grado="atest" />
            <span aria-hidden="true" className="sim-mono text-[0.8rem] text-(--sim-ink-faint)">→</span>
            <Etiqueta grado="rec" />
            <span aria-hidden="true" className="sim-mono text-[0.8rem] text-(--sim-ink-faint)">→</span>
            <Etiqueta grado="hip" />
            <span aria-hidden="true" className="sim-mono text-[0.8rem] text-(--sim-ink-faint)">→</span>
            <Etiqueta grado="canon" />
          </p>
          <p className="font-sans text-[0.95rem] leading-[1.75] text-(--sim-ink-soft)">
            {antes}
            <strong className="font-semibold text-(--sim-ink)">ficción declarada</strong>
            {despues}
          </p>
          <div className="flex flex-col gap-2.5 border-l-4 border-(--sim-rubrica)/30 pl-6">
            <span className="sim-mono text-[0.66rem] tracking-[0.14em] text-(--sim-ink-faint)">{umbral.nota}</span>
            <a href={destino} className="kk-accion self-start text-[0.85rem]">
              {umbral.accion}
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
