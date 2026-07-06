import type { Metadata } from "next";
import { getNeologismos } from "@/lib/neologismos";
import { getAllPersonajes } from "@/lib/personajes";
import { Overline, EmptyState } from "@/components/simulador/ui";
import NeologismosCronologia from "@/components/simulador/NeologismosCronologia";

export const metadata: Metadata = {
  title: "Neologismos — Simulador Caquetío | Curiana Radio",
  description:
    "Las palabras que los agentes inventaron, día a día: cuáles prendieron, cuáles murieron y quién las acuñó.",
};

export default function NeologismsPage() {
  const neologismos = getNeologismos();
  const slugPorNombre = Object.fromEntries(getAllPersonajes().map((p) => [p.nombre, p.slug]));

  return (
    <article className="mx-auto max-w-[720px]">
      <header>
        <Overline>Léxico emergente</Overline>
        <h2 className="mt-1 font-serif text-2xl font-semibold text-(--sim-ink) md:text-3xl">Neologismos</h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          Palabras que los agentes inventaron con sus propios morfemas durante la historia, ordenadas
          por su día de acuñación. La comunidad adopta una palabra cuando dos hablantes distintos la
          usan — y algunas se glosaron de más de una manera: ambas acepciones quedan registradas,
          como en un diccionario de verdad.
        </p>
      </header>

      <div className="mt-8">
        {neologismos.length === 0 ? (
          <EmptyState title="Sin neologismos todavía" />
        ) : (
          <NeologismosCronologia neologismos={neologismos} slugPorNombre={slugPorNombre} />
        )}
      </div>
    </article>
  );
}
