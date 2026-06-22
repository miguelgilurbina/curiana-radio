import Link from "next/link";
import type { Metadata } from "next";
import { getAllPersonajes } from "@/lib/personajes";
import { Card, Overline, Avatar, ScoreGauge, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "Personajes — Simulador Caquetío | Curiana Radio",
  description: "Sesenta personajes, veinte voces curadas: quiénes son y cómo cambió su lengua durante la simulación.",
};

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

  return (
    <div>
      <header className="mb-6">
        <Overline>Quiénes hablan</Overline>
        <h2 className="mt-1 font-serif text-2xl md:text-3xl font-semibold text-deep-900">Personajes</h2>
        <p className="mt-1 max-w-reading font-sans text-sm text-earth-600">
          {personajes.length} voces de la Curiana con historia propia. Cada una llegó con una biografía
          fija — y salió de la simulación con un arco, un puñado de palabras nuevas y frases que nadie
          le escribió de antemano.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {personajes.map((p) => {
          const topQuote = p.quotes[0];
          return (
            <Link key={p.slug} href={`/simulador/personajes/${p.slug}`} className="group">
              <Card className="flex h-full flex-col p-5 sim-card-hover">
                <div className="flex items-start gap-3">
                  <Avatar name={p.nombre} size={42} />
                  <div className="min-w-0">
                    <h3 className="font-serif text-lg font-semibold text-deep-900 group-hover:text-frequency transition-colors">
                      {p.nombre}
                    </h3>
                    <p className="font-sans text-xs text-earth-500">
                      {[p.etnia, p.edad ? `${p.edad} años` : null].filter(Boolean).join(" · ")}
                    </p>
                  </div>
                </div>

                <p className="mt-3 line-clamp-2 font-sans text-sm text-earth-700">{p.rol_comunidad}</p>

                {topQuote && (
                  <p className="mt-3 line-clamp-2 font-serif text-[0.95rem] italic text-deep-800">
                    "{topQuote.quote}"
                  </p>
                )}

                <div className="mt-auto flex items-center justify-between pt-4">
                  {p.avg_score != null ? (
                    <ScoreGauge score={p.avg_score} width={64} />
                  ) : (
                    <span className="font-sans text-xs text-earth-400">sin score</span>
                  )}
                  {p.neologismos_adoptados > 0 && (
                    <span className="font-sans text-xs text-earth-500">
                      ✦ acuñó {p.neologismos_adoptados}
                    </span>
                  )}
                </div>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
