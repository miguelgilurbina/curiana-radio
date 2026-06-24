import { getLexicon } from "@/lib/lexicon";
import { Overline, EmptyState } from "@/components/simulador/ui";
import LexiconFilter from "@/components/simulador/LexiconFilter";

export default function LexiconPage() {
  const palabras = getLexicon();

  return (
    <div>
      <header className="mb-6">
        <Overline>Vocabulario base</Overline>
        <h2 className="mt-1 font-serif text-2xl md:text-3xl font-semibold text-deep-900">
          Léxico Caquetío-Arahuaco
        </h2>
        <p className="mt-1 font-sans text-sm text-earth-600">
          {palabras.length} palabras reconstruidas a partir de fuentes coloniales y lenguas arawak hermanas.
        </p>
      </header>

      {palabras.length === 0 ? (
        <EmptyState
          title="Aún no hay lexicón cargado"
          hint="Corre export_lexicon_seed.py contra Supabase local."
        />
      ) : (
        <LexiconFilter palabras={palabras} />
      )}
    </div>
  );
}
