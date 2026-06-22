import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getAllPersonajes, getPersonajeBySlug } from "@/lib/personajes";
import { Card, Overline, Avatar, ScoreGauge, StatCard } from "@/components/simulador/ui";

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

  return (
    <div>
      <Link
        href="/simulador/personajes"
        className="font-sans text-sm text-earth-600 hover:text-frequency transition-colors"
      >
        ← Personajes
      </Link>

      {/* Encabezado */}
      <header className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-start sm:gap-5">
        <Avatar name={p.nombre} size={64} />
        <div className="min-w-0">
          <h1 className="font-serif text-3xl md:text-4xl font-bold text-deep-900">{p.nombre}</h1>
          <p className="mt-1 font-sans text-sm text-earth-500">
            {[p.etnia, p.edad ? `${p.edad} años` : null, p.ubicacion_default?.replaceAll("_", " ")]
              .filter(Boolean)
              .join(" · ")}
          </p>
          {p.rol_comunidad && (
            <p className="mt-2 max-w-reading font-serif text-lg italic text-deep-800">{p.rol_comunidad}</p>
          )}
        </div>
      </header>

      {/* Stats */}
      <div className="mt-6 grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Intervenciones" value={p.total_respuestas} sub="en este run" accent="#3d5777" />
        <StatCard
          label="Score promedio"
          value={p.avg_score != null ? p.avg_score.toFixed(1) : "—"}
          sub="densidad lingüística / 10"
          accent="#2E7D4F"
        />
        <StatCard label="Palabras propuestas" value={p.neologismos_propuestos} accent="#C47A2B" />
        <StatCard label="Palabras adoptadas" value={p.neologismos_adoptados} sub="por la comunidad" accent="#5B4FCF" />
      </div>

      {/* Biografía + arco */}
      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {p.descripcion && (
          <Card className="p-5 md:p-6">
            <Overline>Quién es</Overline>
            <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
              {p.descripcion}
            </p>
          </Card>
        )}
        {p.resumen_arco && (
          <Card className="p-5 md:p-6">
            <Overline>Su arco en esta simulación</Overline>
            <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
              {p.resumen_arco}
            </p>
          </Card>
        )}
      </div>

      {/* Frases curadas */}
      {p.quotes.length > 0 && (
        <div className="mt-8">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-serif text-xl font-semibold text-deep-900">Frases</h2>
            <Overline>{p.quotes.length} curadas</Overline>
          </div>
          <div className="flex flex-col gap-4">
            {p.quotes.map((q, i) => (
              <Card key={i} className="p-5">
                {/* Caquetío — la voz, tratamiento editorial */}
                <blockquote className="border-l-[3px] border-frequency pl-4">
                  <p className="font-serif text-2xl md:text-[1.75rem] italic leading-snug text-deep-900">
                    {q.quote}
                  </p>
                </blockquote>

                {/* Traducción — para leer, sin adorno */}
                {q.traduccion && (
                  <p className="mt-2 pl-[19px] font-sans text-[0.95rem] leading-relaxed text-earth-600">
                    {q.traduccion}
                  </p>
                )}

                {/* Justificación del analista */}
                {q.justificacion && (
                  <p className="mt-3 max-w-reading font-sans text-sm leading-relaxed text-earth-500">
                    {q.justificacion}
                  </p>
                )}

                <div className="mt-3 flex flex-wrap items-center gap-3 border-t border-earth-200/70 pt-3 font-sans text-xs text-earth-500">
                  {q.day != null && <span>día {q.day}</span>}
                  {q.impacto_score != null && <ScoreGauge score={q.impacto_score} width={56} />}
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Navegación entre personajes */}
      <div className="mt-10 flex items-center justify-between border-t border-earth-200/70 pt-6 font-sans text-sm">
        <Link href={`/simulador/personajes/${anterior.slug}`} className="text-earth-600 hover:text-frequency transition-colors">
          ← {anterior.nombre}
        </Link>
        <Link href={`/simulador/personajes/${siguiente.slug}`} className="text-earth-600 hover:text-frequency transition-colors">
          {siguiente.nombre} →
        </Link>
      </div>
    </div>
  );
}
