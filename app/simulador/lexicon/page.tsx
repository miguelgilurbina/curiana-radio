import type { Metadata } from "next";
import { getLexicon } from "@/lib/lexicon";
import { Overline, EmptyState } from "@/components/simulador/ui";
import LexiconDiccionario from "@/components/simulador/LexiconDiccionario";

export const metadata: Metadata = {
  title: "Léxico — Simulador Caquetío | Curiana Radio",
  description:
    "El vocabulario base de la simulación: palabras atestiguadas en crónicas coloniales y reconstrucciones desde las lenguas arawak hermanas.",
};

export default function LexiconPage() {
  // El id (UUID) no aporta nada en la UI — recortarlo aligera el payload
  // que viaja al cliente para el filtro/paginación.
  const palabras = getLexicon().map(({ id: _id, ...rest }) => rest);

  return (
    <article className="mx-auto max-w-[720px]">
      <header className="mb-6">
        <Overline>Vocabulario base</Overline>
        <h2 className="mt-1 font-serif text-2xl font-semibold text-deep-900 md:text-3xl">
          Léxico Caquetío-Arahuaco
        </h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
          {palabras.length} palabras: las atestiguadas vienen de crónicas coloniales y del trabajo
          académico que las rescató; el resto son reconstrucciones desde las lenguas arawak hermanas
          (wayunaiki, lokono, taíno). Cada entrada declara su fuente — esa etiqueta es la etimología
          honesta de este diccionario.
        </p>
      </header>

      {palabras.length === 0 ? (
        <EmptyState
          title="Aún no hay lexicón cargado"
          hint="Corre export_lexicon_seed.py contra Supabase local."
        />
      ) : (
        <LexiconDiccionario palabras={palabras} />
      )}
    </article>
  );
}
