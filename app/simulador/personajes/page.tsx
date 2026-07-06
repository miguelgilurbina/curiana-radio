import Link from "next/link";
import type { Metadata } from "next";
import { getAllPersonajes, type Personaje } from "@/lib/personajes";
import { Overline, Avatar, ScoreGauge, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "Personajes — Simulador Caquetío | Curiana Radio",
  description: "Las voces curadas de la Curiana: quiénes son y cómo cambió su lengua durante la historia.",
};

// Índice editorial — dramatis personae de la edición, no un grid de cards.
// El tier del seed ordena por protagonismo en el run curado.
const GRUPOS: { tier: number | null; label: string }[] = [
  { tier: 1, label: "Voces principales" },
  { tier: 2, label: "Más voces de la Curiana" },
];

function EntradaPersonaje({ p }: { p: Personaje }) {
  const quote = p.quotes[0];
  const meta = [p.etnia, p.edad ? `${p.edad} años` : null].filter(Boolean).join(" · ");
  return (
    <li className="border-t border-(--sim-rule) first:border-t-0">
      <Link href={`/simulador/personajes/${p.slug}`} className="group flex gap-4 py-5">
        <Avatar name={p.nombre} size={48} />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
            <h3 className="font-serif text-xl font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
              {p.nombre}
            </h3>
            <span className="font-sans text-xs text-(--sim-ink-faint)">{meta}</span>
            {p.neologismos_adoptados > 0 && (
              <span className="font-sans text-xs text-(--sim-ink-faint)">✦ acuñó {p.neologismos_adoptados}</span>
            )}
          </div>
          <p className="mt-1 line-clamp-2 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
            {p.rol_comunidad}
          </p>
          {quote && (
            <p className="mt-2 line-clamp-2 font-serif text-[0.95rem] italic text-(--sim-ink)">
              "{quote.quote}"
            </p>
          )}
        </div>
        {p.avg_score != null && (
          <div className="hidden shrink-0 self-center sm:block">
            <ScoreGauge score={p.avg_score} width={56} />
          </div>
        )}
      </Link>
    </li>
  );
}

export default function PersonajesPage() {
  const personajes = getAllPersonajes();

  if (personajes.length === 0) {
    return (
      <EmptyState
        title="Aún no hay personajes curados"
        hint="Corre export_personajes_seed.py tras una simulación con --perfiles."
      />
    );
  }

  const agrupados = GRUPOS.map((g) => ({
    ...g,
    personajes: personajes.filter((p) => p.tier === g.tier),
  })).filter((g) => g.personajes.length > 0);
  const sinTier = personajes.filter((p) => !GRUPOS.some((g) => g.tier === p.tier));

  return (
    <article className="mx-auto max-w-[720px]">
      <header>
        <Overline>Quiénes hablan</Overline>
        <h2 className="mt-1 font-serif text-2xl font-semibold text-(--sim-ink) md:text-3xl">Personajes</h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          {personajes.length} voces de la Curiana con historia propia. Cada una llegó con una
          biografía fija — y salió de la historia con un arco, un puñado de palabras nuevas y
          frases que nadie le escribió de antemano.
        </p>
      </header>

      {agrupados.map((g) => (
        <section key={g.label} className="mt-10">
          <Overline>{g.label}</Overline>
          <ul className="mt-3">
            {g.personajes.map((p) => (
              <EntradaPersonaje key={p.slug} p={p} />
            ))}
          </ul>
        </section>
      ))}

      {sinTier.length > 0 && (
        <section className="mt-10">
          <Overline>Otras voces</Overline>
          <ul className="mt-3">
            {sinTier.map((p) => (
              <EntradaPersonaje key={p.slug} p={p} />
            ))}
          </ul>
        </section>
      )}
    </article>
  );
}
