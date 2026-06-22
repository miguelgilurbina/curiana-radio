import Link from "next/link";
import { getNeologismos } from "@/lib/neologismos";
import { Card, Overline, EmptyState } from "@/components/simulador/ui";
import NeologismosFilter from "@/components/simulador/NeologismosFilter";

export default function NeologismsPage() {
  const neologismos = getNeologismos();

  // dedupe por cita: una frase puede declarar varios neologismos a la vez
  // (ej. "kali-bana-chaa...masa-bana-sha..." en la misma oración) -- sin esto
  // se repite la misma cita en varias tarjetas "destacadas".
  const vistas = new Set<string>();
  const destacados = neologismos
    .filter((n) => n.destacado)
    .sort((a, b) => (b.destacado!.impacto_score ?? 0) - (a.destacado!.impacto_score ?? 0))
    .filter((n) => {
      if (vistas.has(n.destacado!.quote)) return false;
      vistas.add(n.destacado!.quote);
      return true;
    })
    .slice(0, 3);

  return (
    <div>
      <header className="mb-6">
        <Overline>Léxico emergente</Overline>
        <h2 className="mt-1 font-serif text-2xl md:text-3xl font-semibold text-deep-900">Neologismos</h2>
        <p className="mt-1 max-w-reading font-sans text-sm text-earth-600">
          Palabras que los agentes inventaron con sus propios morfemas durante la simulación
          curada. La comunidad las adopta cuando dos hablantes distintos las usan.
        </p>
      </header>

      {neologismos.length === 0 ? (
        <EmptyState title="Sin neologismos todavía" />
      ) : (
        <>
          {destacados.length > 0 && (
            <div className="mb-8">
              <h3 className="mb-3 font-serif text-lg font-semibold text-deep-900">Las que prendieron de verdad</h3>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                {destacados.map((n) => (
                  <Link key={n.id} href={`/simulador/personajes/${n.destacado!.agente_slug}`}>
                    <Card className="h-full p-4 sim-card-hover">
                      <span className="font-serif text-xl font-semibold text-frequency">{n.form}</span>
                      <p className="mt-1 font-sans text-sm text-deep-800">{n.meaning}</p>
                      <blockquote className="mt-3 border-l-[3px] border-frequency pl-3">
                        <p className="font-serif text-base italic leading-snug text-deep-900">{n.destacado!.quote}</p>
                      </blockquote>
                      {n.destacado!.traduccion && (
                        <p className="mt-1.5 pl-[15px] font-sans text-xs text-earth-600">{n.destacado!.traduccion}</p>
                      )}
                      <p className="mt-2 font-sans text-xs text-earth-500">— {n.destacado!.agente}</p>
                    </Card>
                  </Link>
                ))}
              </div>
            </div>
          )}

          <h3 className="mb-3 font-serif text-lg font-semibold text-deep-900">Todas las propuestas</h3>
          <NeologismosFilter neologismos={neologismos} />
        </>
      )}
    </div>
  );
}
