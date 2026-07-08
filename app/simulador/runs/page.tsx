import type { Metadata } from "next";
import Link from "next/link";
import { getRunsIndex, getParejaExperimento } from "@/lib/runs";
import { EvolucionTimeline, DiccionarioKoine } from "@/components/simulador/evolucion";
import { ExperimentoControl } from "@/components/simulador/experimento";
import { Asterismo } from "@/components/simulador/prose";
import { Overline, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "La evolución entre simulaciones — Simulador Caquetío | Curiana Radio",
  description:
    "El arco del proyecto, simulación a simulación: de una lengua que apenas se sostenía a una koiné con diccionario propio, y la prueba de control que lo confirma.",
};

// El meta-relato del proyecto: qué pasó ENTRE las simulaciones. Vive en su
// propia página (no enterrado al pie de la edición insignia) porque es la
// lectura comparativa, no la crónica de un run. Datos: lib/runs.ts.
export default function RunsPage() {
  const runsIndex = getRunsIndex();
  const experimento = getParejaExperimento("038d7b9d");

  if (!runsIndex || runsIndex.runs.length === 0) {
    return (
      <article className="mx-auto max-w-[720px]">
        <header>
          <Overline>Bitácora de expediciones</Overline>
          <h2 className="mt-1 sim-display text-2xl font-semibold text-(--sim-ink) md:text-3xl">
            La evolución entre simulaciones
          </h2>
        </header>
        <div className="mt-8">
          <EmptyState
            title="Aún no hay runs curados"
            hint="Corre export_runs_index.py contra Supabase local tras las simulaciones."
          />
        </div>
      </article>
    );
  }

  return (
    <article className="mx-auto max-w-[720px]">
      <header>
        <Link
          href="/simulador"
          className="sim-mono text-[0.7rem] uppercase tracking-[0.14em] text-(--sim-ink-faint) transition-colors hover:text-(--sim-fuego)"
        >
          ← Volver a la edición
        </Link>
        <div className="mt-4">
          <Overline>Bitácora de expediciones</Overline>
        </div>
        <h2 className="mt-1 sim-display text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
          La evolución, simulación a simulación
        </h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          Cada corrida es una expedición: mismo golfete, misma gente, y un instrumento que cada vez
          mide mejor. Lo que empezó como una comunidad que apenas sostenía su lengua terminó formando
          una koiné — y la última expedición salió con un grupo de control para probar que la
          convergencia no era un truco del andamiaje.
        </p>
        <p className="mt-3 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
          Se muestran las {runsIndex.runs.length} expediciones que aportan al relato: los runs largos
          y calibrados. Las corridas de desarrollo y las pruebas cortas — la mayoría de las más de
          veinte simulaciones que se hicieron — quedan registradas en la bitácora del proyecto, no
          aquí.
        </p>
      </header>

      <section id="evolucion" className="mt-4 scroll-mt-24">
        <EvolucionTimeline runs={runsIndex.runs} />
      </section>

      {experimento && (
        <>
          <Asterismo />
          <section id="experimento" className="scroll-mt-24">
            <Overline>La prueba de control</Overline>
            <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
              ¿La lengua converge sola?
            </h2>
            <ExperimentoControl normal={experimento.normal} ablacion={experimento.ablacion} />
          </section>
        </>
      )}

      <Asterismo />
      <section id="diccionario-koine" className="scroll-mt-24">
        <Overline>Lo que la comunidad nombró</Overline>
        <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
          El diccionario koiné
        </h2>
        <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
          Cuando algo nuevo llegó al golfete — un cometa, una fiebre, un metal amarillo — la comunidad
          necesitó nombrarlo. Varias formas compitieron; estas ganaron.
        </p>
        <DiccionarioKoine runs={runsIndex.runs} />
      </section>
    </article>
  );
}
