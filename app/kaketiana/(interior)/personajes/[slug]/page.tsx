import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getAllPersonajes, getPersonajeBySlug } from "@/lib/personajes";
import { getRunActivo } from "@/lib/editorial";
import { Overline, Avatar, ScoreGauge } from "@/components/simulador/ui";
import { DataAside } from "@/components/simulador/prose";
import { EVENTO_TIPOS } from "@/lib/sim-theme";

interface PersonajePageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getAllPersonajes().map((p) => ({ slug: p.slug }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: PersonajePageProps): Promise<Metadata> {
  const { slug } = await params;
  const p = getPersonajeBySlug(slug);
  if (!p) return { title: "Personaje no encontrado | Curiana Radio" };
  return {
    title: `${p.nombre} — Personajes del Simulador | Curiana Radio`,
    description: p.rol_comunidad || p.descripcion.slice(0, 160),
  };
}

export default async function PersonajePage({ params }: PersonajePageProps) {
  const { slug } = await params;
  const personajes = getAllPersonajes();
  const p = personajes.find((x) => x.slug === slug);
  if (!p) notFound();

  const idx = personajes.findIndex((x) => x.slug === slug);
  const anterior = personajes[(idx - 1 + personajes.length) % personajes.length];
  const siguiente = personajes[(idx + 1) % personajes.length];

  // Apariciones en la cronología curada del run activo
  const run = getRunActivo();
  const apariciones = run.epocas.flatMap((epoca) =>
    epoca.eventos
      .filter((ev) => ev.personaje === slug)
      .map((ev) => ({ ...ev, epocaId: epoca.id, epocaTitulo: epoca.titulo }))
  );

  const [heroQuote, ...restoQuotes] = p.quotes;

  return (
    <article className="mx-auto max-w-[720px]">
      <Link
        href="/kaketiana/personajes"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← Personajes
      </Link>

      {/* Encabezado de la ficha */}
      <header className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-start sm:gap-5">
        <Avatar name={p.nombre} size={72} />
        <div className="min-w-0">
          <h1 className="sim-display tracking-tight text-3xl font-bold text-(--sim-ink) md:text-4xl">{p.nombre}</h1>
          <p className="mt-1 font-sans text-sm text-(--sim-ink-faint)">
            {[p.etnia, p.edad ? `${p.edad} años` : null, p.ubicacion_default?.replaceAll("_", " ")]
              .filter(Boolean)
              .join(" · ")}
          </p>
          {p.rol_comunidad && (
            <p className="mt-2 max-w-reading font-serif text-lg italic leading-snug text-(--sim-ink-soft)">
              {p.rol_comunidad}
            </p>
          )}
        </div>
      </header>

      {/* Su voz, primero */}
      {heroQuote && (
        <blockquote className="mt-8 border-l-[3px] border-(--sim-fuego) pl-5 md:pl-7">
          <p className="font-serif text-2xl italic leading-snug text-(--sim-ink) md:text-3xl">
            {heroQuote.quote}
          </p>
          {heroQuote.traduccion && (
            <p className="mt-2 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{heroQuote.traduccion}</p>
          )}
          {heroQuote.day != null && (
            <p className="mt-2 font-sans text-xs text-(--sim-ink-faint)">día {heroQuote.day}</p>
          )}
        </blockquote>
      )}

      <DataAside
        items={[
          { label: "Intervenciones", value: p.total_respuestas, sub: "en esta edición" },
          { label: "Score promedio", value: p.avg_score != null ? p.avg_score.toFixed(1) : "—", sub: "densidad lingüística / 10" },
          { label: "Propuestas", value: p.neologismos_propuestos, sub: "palabras nuevas" },
          { label: "Adoptadas", value: p.neologismos_adoptados, sub: "por la comunidad" },
        ]}
      />

      {/* Biografía y arco, como lectura corrida */}
      {p.descripcion && (
        <section className="mt-8">
          <Overline>Quién es</Overline>
          <p className="mt-2 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            {p.descripcion}
          </p>
        </section>
      )}
      {p.resumen_arco && (
        <section className="mt-8">
          <Overline>Su arco en esta edición</Overline>
          <p className="mt-2 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            {p.resumen_arco}
          </p>
        </section>
      )}

      {/* Cruce con la cronología curada */}
      {apariciones.length > 0 && (
        <section className="mt-8">
          <Overline>En la cronología</Overline>
          <ol className="mt-3">
            {apariciones.map((ev, i) => {
              const tipo = EVENTO_TIPOS[ev.tipo];
              return (
                <li key={i} className="relative border-l border-(--sim-rule) pl-5 pb-5 last:pb-0">
                  <span
                    aria-hidden="true"
                    className="absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full"
                    style={{ background: tipo.color }}
                  />
                  <div className="flex flex-wrap items-center gap-2 font-sans text-xs text-(--sim-ink-faint)">
                    <span className="tabular-nums font-medium text-(--sim-ink-soft)">Día {ev.dia}</span>
                    <span
                      className="inline-flex items-center rounded-full px-2 py-0.5 font-medium"
                      style={{ background: `${tipo.color}1a`, color: tipo.color, border: `1px solid ${tipo.color}33` }}
                    >
                      {tipo.label}
                    </span>
                  </div>
                  {ev.forma && (
                    <p className="mt-1 sim-display text-lg font-semibold text-(--sim-fuego)">{ev.forma}</p>
                  )}
                  {ev.nota && (
                    <p className="mt-1 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                      {ev.nota}
                    </p>
                  )}
                  <Link
                    href={`/kaketiana/experimento#epoca-${ev.epocaId}`}
                    className="mt-1 inline-block font-sans text-xs text-(--sim-ink-faint) transition-colors hover:text-(--sim-fuego)"
                  >
                    ver en «{ev.epocaTitulo}» →
                  </Link>
                </li>
              );
            })}
          </ol>
        </section>
      )}

      {/* El resto de sus frases curadas */}
      {restoQuotes.length > 0 && (
        <section className="mt-10">
          <div className="flex items-baseline justify-between">
            <h2 className="sim-display text-xl font-semibold text-(--sim-ink)">Más frases</h2>
            <Overline>{restoQuotes.length} curadas</Overline>
          </div>
          <div className="mt-2">
            {restoQuotes.map((q, i) => (
              <div key={i} className="border-t border-(--sim-rule) py-6 first:border-t-0">
                <blockquote className="border-l-[3px] border-(--sim-fuego) pl-4">
                  <p className="font-serif text-xl italic leading-snug text-(--sim-ink) md:text-2xl">
                    {q.quote}
                  </p>
                </blockquote>
                {q.traduccion && (
                  <p className="mt-2 pl-[19px] font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                    {q.traduccion}
                  </p>
                )}
                {q.justificacion && (
                  <p className="mt-3 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-faint)">
                    {q.justificacion}
                  </p>
                )}
                <div className="mt-3 flex flex-wrap items-center gap-3 font-sans text-xs text-(--sim-ink-faint)">
                  {q.day != null && <span>día {q.day}</span>}
                  {q.impacto_score != null && <ScoreGauge score={q.impacto_score} width={56} />}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Navegación entre personajes */}
      <div className="mt-12 flex items-center justify-between border-t border-(--sim-rule) pt-6 font-sans text-sm">
        <Link
          href={`/kaketiana/personajes/${anterior.slug}`}
          className="text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
        >
          ← {anterior.nombre}
        </Link>
        <Link
          href={`/kaketiana/personajes/${siguiente.slug}`}
          className="text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
        >
          {siguiente.nombre} →
        </Link>
      </div>
    </article>
  );
}
