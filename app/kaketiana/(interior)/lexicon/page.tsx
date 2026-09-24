import Link from "next/link";
import type { Metadata } from "next";
import { getFichasSeed, getIndiceFichas, getRetiradas } from "@/lib/fichas";
import { Overline, EmptyState } from "@/components/simulador/ui";
import DiccionarioVivo from "@/components/simulador/DiccionarioVivo";

export const metadata: Metadata = {
  title: "El diccionario — Kaketiana | Curiana Radio",
  description:
    "Las voces del caquetío, una por una: qué significan, de qué fuente salen y cuán seguras son — atestiguadas, reconstruidas desde las lenguas hermanas, retroabstraídas del habla viva o hipotéticas.",
};

// El diccionario de la lengua viva: sólo voces caquetías, cada una con su
// capa epistémica. Las comparandas (wayuu, lokono, achagua…) son el andamio
// de la reconstrucción y no se listan aquí. Todo sale de content/wiki/
// fichas.json (export_fichas_seed.py): ninguna cifra se escribe a mano.
export default function LexiconPage() {
  const seed = getFichasSeed();
  const indice = getIndiceFichas();
  const retiradas = getRetiradas();

  return (
    <article className="mx-auto max-w-[760px]">
      <header className="mb-8">
        <Overline>El diccionario</Overline>
        <h2 className="mt-1 sim-display text-3xl font-semibold text-(--sim-ink) md:text-4xl">
          La lengua, palabra por palabra
        </h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          <strong className="text-(--sim-ink)">{seed.n} voces caquetías.</strong> Ninguna se da por
          sabida: cada una lleva la marca de cómo la sabemos, y debajo, la fuente con su página. Las
          palabras de las lenguas hermanas que sirvieron para reconstruir no están aquí — son el
          andamio, no la lengua.
        </p>
      </header>

      {indice.length === 0 ? (
        <EmptyState
          title="Aún no hay fichas"
          hint="Corre export_fichas_seed.py en proyecto-linguistico-caquetío/curiana_sim/."
        />
      ) : (
        <DiccionarioVivo fichas={indice} capas={seed.capas} />
      )}

      <footer className="mt-14 grid gap-6 border-t border-(--sim-ink) pt-6 sm:grid-cols-2">
        {retiradas.length > 0 && (
          <Link href="/kaketiana/lexicon/retiradas" className="group block">
            <Overline>El archivo</Overline>
            <span className="mt-1 block sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
              Las {retiradas.length} voces que el proyecto retiró →
            </span>
            <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
              Las que se enseñaron y dejaron de enseñarse, con el porqué. Archivar no es borrar.
            </span>
          </Link>
        )}
        <Link href="/kaketiana/no-sabemos" className="group block">
          <Overline>El borde</Overline>
          <span className="mt-1 block sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
            Lo que no sabemos →
          </span>
          <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
            Las preguntas que el proyecto no ha podido cerrar, con lo que hay medido.
          </span>
        </Link>
      </footer>
    </article>
  );
}
