import Link from "next/link";
import type { Metadata } from "next";
import type { Retirada } from "@/types/fichas";
import { getRetiradas } from "@/lib/fichas";
import { Overline, EmptyState } from "@/components/simulador/ui";
import { CapaSello } from "@/components/simulador/capa";

export const metadata: Metadata = {
  title: "Las voces retiradas — Kaketiana | Curiana Radio",
  description:
    "Las palabras que estuvieron en el habla de la simulación y salieron de ella: cuál las sustituye y por qué. Archivar no es borrar.",
};

// El archivo de FUERA_DEL_HABLA: lo que se retiró, con su capa intacta
// («archivar no es borrar y tampoco es degradar»), la fecha, el motivo en una
// frase y la voz que ocupa su lugar. Generado por export_fichas_seed.py.
export default function RetiradasPage() {
  const retiradas = getRetiradas();

  // Agrupadas por motivo, el grupo más grande primero.
  const grupos = new Map<string, { texto: string; voces: Retirada[] }>();
  for (const r of retiradas) {
    const g = grupos.get(r.motivo) ?? { texto: r.motivo_texto, voces: [] };
    g.voces.push(r);
    grupos.set(r.motivo, g);
  }
  const ordenados = [...grupos.entries()].sort((a, b) => b[1].voces.length - a[1].voces.length);

  return (
    <article className="mx-auto max-w-[760px]">
      <Link
        href="/kaketiana/lexicon"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← El diccionario
      </Link>

      <header className="mt-5">
        <Overline>El archivo</Overline>
        <h1 className="mt-1 sim-display text-3xl font-bold tracking-tight text-(--sim-ink) md:text-4xl">
          Las voces que el proyecto retiró
        </h1>
        <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          <strong className="text-(--sim-ink)">{retiradas.length} palabras</strong> estuvieron en el
          habla de la simulación y salieron de ella. No se borran: cada una conserva su etiqueta y su
          procedencia, y aquí se dice por qué salió y qué voz ocupa su lugar.
        </p>
      </header>

      {retiradas.length === 0 ? (
        <div className="mt-8">
          <EmptyState title="Aún no hay archivo" hint="Corre export_fichas_seed.py." />
        </div>
      ) : (
        ordenados.map(([motivo, g]) => (
          <section key={motivo} className="mt-12">
            <div className="flex items-baseline justify-between gap-4 border-b border-(--sim-ink) pb-2">
              <h2 className="max-w-reading sim-display text-lg font-semibold leading-snug text-(--sim-ink) md:text-xl">
                {g.texto}
              </h2>
              <span className="sim-mono shrink-0 text-xs tabular-nums text-(--sim-ink-faint)">
                {g.voces.length}
              </span>
            </div>
            <ul>
              {g.voces.map((r) => (
                <li
                  key={r.ancla}
                  id={r.ancla}
                  className="scroll-mt-24 border-b border-(--sim-rule) py-3 target:bg-(--sim-paper-deep)"
                >
                  <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                    <span className="sim-display text-lg font-semibold text-(--sim-ink-soft)">{r.forma}</span>
                    <span className="font-sans text-sm text-(--sim-ink-soft)">{r.glosa}</span>
                  </div>
                  <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 font-sans text-xs text-(--sim-ink-faint)">
                    {r.capa ? (
                      <CapaSello capa={r.capa} />
                    ) : (
                      r.lengua && <span className="uppercase tracking-[0.12em]">no caquetía · {r.lengua}</span>
                    )}
                    {r.fecha && <span className="sim-mono tabular-nums">retirada el {r.fecha}</span>}
                    {r.sustitutas.length > 0 && (
                      <span>
                        en su lugar:{" "}
                        {r.sustitutas.map((s, i) => (
                          <span key={s.forma}>
                            {i > 0 && ", "}
                            {s.slug ? (
                              <Link
                                href={`/kaketiana/lexicon/${s.slug}`}
                                className="sim-display text-sm font-semibold text-(--sim-fuego) transition-colors hover:text-(--sim-rubrica)"
                              >
                                {s.forma}
                              </Link>
                            ) : (
                              <span className="sim-display text-sm font-semibold text-(--sim-ink-soft)">{s.forma}</span>
                            )}
                          </span>
                        ))}
                      </span>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        ))
      )}
    </article>
  );
}
