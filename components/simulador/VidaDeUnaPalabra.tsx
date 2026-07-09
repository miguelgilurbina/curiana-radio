import Link from "next/link";
import type { Neologismo } from "@/lib/neologismos";
import { Overline } from "@/components/simulador/ui";

// El ejemplo vivo del Acto I: la biografía de una sola palabra, de la boca
// que la compuso a la comunidad que la hizo suya. Nada explica mejor el
// experimento completo que este recorrido — teoría (Conceptos) arriba,
// este caso concreto abajo. La palabra se elige en abstract.json
// (ejemplo_form) y se valida en build contra neologismos.json.
export default function VidaDeUnaPalabra({
  neo,
  proposerSlug,
}: {
  neo: Neologismo;
  proposerSlug?: string;
}) {
  const adoptantes = neo.adopted_by ?? [];

  return (
    <section id="vida-de-una-palabra" className="mt-14 scroll-mt-24">
      <Overline>Vida de una palabra</Overline>
      <div className="mt-4 rounded-2xl border border-(--sim-rule) bg-(--sim-paper-deep) p-6 sm:p-8">
        <p className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
          <span className="sim-display text-3xl font-semibold italic text-(--sim-fuego) md:text-4xl">
            {neo.form}
          </span>
          <span className="font-serif italic leading-snug text-(--sim-ink-soft)">
            «{neo.meaning}»
          </span>
        </p>

        <ol className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
          <li className="border-l-2 border-(--sim-rubrica)/60 pl-4">
            <span className="sim-mono block text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              Día {neo.proposed_day} · La propuesta
            </span>
            <p className="mt-1.5 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              {proposerSlug ? (
                <Link
                  href={`/simulador/personajes/${proposerSlug}`}
                  className="font-medium text-(--sim-ink) transition-colors hover:text-(--sim-fuego)"
                >
                  {neo.proposed_by}
                </Link>
              ) : (
                <span className="font-medium text-(--sim-ink)">{neo.proposed_by}</span>
              )}{" "}
              la compone con la morfología del proyecto:{" "}
              <code className="sim-mono rounded bg-(--sim-paper) px-1.5 py-0.5 text-xs">
                {neo.components}
              </code>
              . Todavía no es una palabra: es una apuesta.
            </p>
          </li>
          <li className="border-l-2 border-(--sim-rubrica)/60 pl-4">
            <span className="sim-mono block text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              La adopción
            </span>
            <p className="mt-1.5 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              {adoptantes.length > 0 ? (
                <>
                  <span className="font-medium text-(--sim-ink)">{adoptantes.join(" y ")}</span> la
                  repiten en sus propias frases. Desde ese momento ya no es de quien la inventó: es
                  de la comunidad.
                </>
              ) : (
                "Nadie la repitió: murió en la boca de uno solo, como la mayoría."
              )}
            </p>
          </li>
        </ol>

        {neo.destacado && (
          <blockquote className="mt-7 border-t border-(--sim-rule) pt-6">
            <p className="sim-display text-lg italic leading-snug text-(--sim-fuego) md:text-xl">
              {neo.destacado.quote}
            </p>
            <p className="mt-2 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              {neo.destacado.traduccion}
            </p>
            <footer className="sim-mono mt-3 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              — {neo.destacado.agente}, dentro de la simulación · la palabra ya vive en otra boca
            </footer>
          </blockquote>
        )}
      </div>
    </section>
  );
}
