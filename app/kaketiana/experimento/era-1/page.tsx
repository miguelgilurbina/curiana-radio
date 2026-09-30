import type { Metadata } from "next";
import { Fragment } from "react";
import Link from "next/link";
import { getRunActivo, getRunsPublicados } from "@/lib/editorial";
import { getManaureFragment } from "@/lib/manaure";
import { getResumen } from "@/lib/resumen";
import { getAllPersonajes } from "@/lib/personajes";
import { getRunsIndex, getParejaExperimento } from "@/lib/runs";
import { getGlosasPorManaure, getGlosasPorEvento } from "@/lib/glosas";
import Masthead from "@/components/simulador/Masthead";
import Timeline from "@/components/simulador/Timeline";
import Umbral from "@/components/simulador/Umbral";
import ManaureVoice from "@/components/simulador/ManaureVoice";
import GlosaCronista from "@/components/simulador/GlosaCronista";
import LanguageDriftChart from "@/components/simulador/LanguageDriftChart";
import { EvolucionTimeline, DiccionarioKoine } from "@/components/simulador/evolucion";
import { ExperimentoControl } from "@/components/simulador/experimento";
import { Epoca, EventoItem, DataAside, Asterismo } from "@/components/simulador/prose";
import { Overline, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "La era 1 del experimento — cómo se construyó el motor | Curiana Radio",
  description:
    "Las seis simulaciones de junio y julio de 2026 con las que se construyó el motor de Kaketiana: pruebas de desarrollo, no resultados, y el primer experimento de control.",
};

// El copy de esta página era el del abstract de la era 1; queda aquí, fijo,
// porque ya no cambia.
const CIERRE =
  "Hasta aquí, el instrumento: lo que se midió, tal como se midió. Lo que sigue es lo que se oyó — la crónica del run insignia, contada por el señor de la Curiana y por un cronista que lo ve todo.";
const NOTA_HONESTIDAD =
  "Sobre este contenido: los datos — palabras, adopciones, deriva, convergencia — salen de la simulación tal cual ocurrieron y son reproducibles desde la bitácora del proyecto. Las voces del narrador y de Manaure son reconstrucción editorial hipotética, escrita para esta publicación, y se marcan siempre con su grado de certeza.";

const ANEXOS = [
  { href: "/kaketiana/personajes", label: "Personajes", desc: "Las veinte voces de la crónica de esta era y sus arcos." },
  { href: "/kaketiana/lexicon", label: "Léxico", desc: "Las voces caquetías, palabra por palabra, con su fuente y cómo la sabemos." },
  { href: "/kaketiana/neologisms", label: "Neologismos", desc: "Todas las palabras inventadas: las que prendieron y las que no." },
  // /kaketiana/fuentes no existe desde 2026-08-24: el wiki es /kaketiana
  { href: "/kaketiana", label: "Fuentes", desc: "El wiki de investigación: crónicas, glosarios y el mundo caquetío, cada dato con su fuente." },
];

// La era 1 (2026-06-22 → 2026-07-06): las simulaciones con las que se
// construyó el motor. Antes era el landing del experimento; desde la era 2 es
// su historia. La bitácora del proyecto (5-experimento/BITACORA_RUNS.md,
// decisión de Miguel del 2026-08-03) pide que cualquier cita de estos números
// lleve su advertencia: va arriba, antes de cualquier cifra.
export default function EraUnoPage() {
  const runsIndex = getRunsIndex();
  const runNormal = runsIndex?.runs.find((r) => r.rol === "normal");
  const experimento = runNormal ? getParejaExperimento(runNormal.id8) : null;

  const runs = getRunsPublicados();
  const run = getRunActivo();
  const resumen = getResumen();
  const personajes = getAllPersonajes();
  const nombrePorSlug = new Map(personajes.map((p) => [p.slug, p.nombre]));
  const epocasNav = run.epocas.map(({ id, titulo, dias, hito }) => ({ id, titulo, dias, hito }));

  const hero = run.manaure_hero ? getManaureFragment(run.manaure_hero) : null;
  const derivaVoz = run.deriva?.manaure ? getManaureFragment(run.deriva.manaure) : null;
  const cierre = run.manaure_cierre ? getManaureFragment(run.manaure_cierre) : null;

  const pctCaquetio =
    resumen?.pct_caquetio_final != null ? `${Math.round(resumen.pct_caquetio_final * 100)}%` : "—";

  return (
    <>
      <div data-sim-acto="laboratorio" className="bg-(--sim-paper)">
        <div className="mx-auto max-w-6xl px-4 pb-20 pt-8 sm:px-6 lg:px-8">
          <Masthead />

          <div className="mx-auto max-w-[820px]">
            <header>
              <Link
                href="/kaketiana/experimento"
                className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
              >
                ← El experimento, hoy
              </Link>
              <div className="mt-6">
                <Overline>Historia del motor · era 1</Overline>
              </div>
              <h2 className="sim-display mt-2 text-4xl font-semibold leading-tight tracking-tight text-(--sim-ink) md:text-5xl">
                Cómo se construyó el instrumento
              </h2>
              <p className="mt-5 max-w-reading font-sans text-base leading-relaxed text-(--sim-ink-soft) md:text-lg">
                Entre junio y julio de 2026 corrieron las primeras simulaciones: de veinte a treinta y
                ocho personajes en un Golfete de Coro sin mapa, con un lexicón que todavía mezclaba el
                caquetío con sus lenguas vecinas. Sirvieron para construir el motor. Esta página las
                conserva tal como se publicaron entonces.
              </p>
            </header>

            <aside className="mt-8 rounded-xl border border-(--sim-rubrica)/60 bg-(--sim-paper-deep) px-5 py-4">
              <p className="font-sans text-sm font-semibold text-(--sim-ink)">
                Léase con esta advertencia
              </p>
              <ul className="mt-2 list-disc space-y-1.5 pl-5 font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                <li>
                  Las seis simulaciones de esta era son{" "}
                  <strong className="text-(--sim-ink)">pruebas de desarrollo del motor, no resultados</strong>.
                  Entre una y otra cambiaron el motor y el instrumento que las mide, así que no se
                  comparan entre sí.
                </li>
                <li>
                  La única comparación limpia es el par de control del 6 de julio: mismo motor, mismo
                  día, una sola diferencia.
                </li>
                <li>
                  El lexicón de entonces trataba al wayuunaiki como lengua hermana y enseñaba palabras
                  que el proyecto después retiró. Algunas aparecen en la crónica de abajo; el
                  diccionario actual dice cuáles y por qué.
                </li>
              </ul>
            </aside>

            {/* La bitácora: qué pasó ENTRE las simulaciones (antes /simulador/runs) */}
            <section id="bitacora" className="mt-14 scroll-mt-24">
              <Overline>Bitácora de expediciones</Overline>
              <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
                La evolución, simulación a simulación
              </h3>
              <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                Cada corrida es una expedición: mismo golfete, misma gente, y un instrumento que
                cada vez mide mejor. Lo que empezó como una comunidad que apenas sostenía su lengua
                terminó formando una koiné — y la última expedición salió con un grupo de control
                para probar que la convergencia no era un truco del andamiaje.
              </p>
              {runsIndex && runsIndex.runs.length > 0 ? (
                <>
                  <EvolucionTimeline runs={runsIndex.runs} />
                  <p className="mt-4 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
                    Se muestran las {runsIndex.runs.length} expediciones que aportan al relato. Las
                    corridas de desarrollo y las pruebas cortas — la mayoría de las más de veinte
                    simulaciones que se hicieron — quedan en la bitácora del proyecto, no aquí.
                  </p>
                </>
              ) : (
                <div className="mt-6">
                  <EmptyState
                    title="Aún no hay runs curados"
                    hint="Corre export_runs_index.py contra Supabase local tras las simulaciones."
                  />
                </div>
              )}
            </section>

            {experimento && (
              <section id="experimento" className="mt-14 scroll-mt-24">
                <Overline>La prueba de control</Overline>
                <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
                  ¿La lengua converge sola?
                </h3>
                <ExperimentoControl normal={experimento.normal} ablacion={experimento.ablacion} />
              </section>
            )}

            </div>
        </div>
      </div>

      {/* ══ EL UMBRAL ══════════════════════════════════════════════════ */}
      <Umbral texto={CIERRE} />

      {/* ══ ACTO II · LA CRÓNICA ══════════════════════════════════════ */}
      <div className="mx-auto max-w-6xl px-4 pb-24 pt-14 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-[230px_minmax(0,1fr)] lg:gap-12">
          <aside className="hidden lg:block">
            <Timeline runTitulo={run.titulo} epocas={epocasNav} variant="sidebar" />
          </aside>

          <div className="min-w-0">
            <div className="lg:hidden">
              <Timeline runTitulo={run.titulo} epocas={epocasNav} variant="bar" />
            </div>

            <article className="max-w-[720px]">
              {/* Índice de ediciones: hoy una, la arquitectura lista para varias */}
              <div className="mb-6 flex flex-wrap items-center gap-2">
                <Overline>Acto II · La crónica</Overline>
                {runs.map((r, i) => (
                  <span
                    key={r.id}
                    className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 font-sans text-xs ${
                      r.id === run.id
                        ? "bg-(--sim-ink) text-(--sim-paper)"
                        : "border border-(--sim-rule) text-(--sim-ink-soft)"
                    }`}
                  >
                    <span className="tabular-nums">{String(i + 1).padStart(2, "0")}</span>
                    {r.fecha}
                  </span>
                ))}
              </div>

              {/* Cabecera del run activo */}
              <header>
                <h2 className="sim-display text-5xl font-semibold leading-[0.95] tracking-tight text-(--sim-ink) md:text-6xl">
                  {run.titulo}
                </h2>
                {run.subtitulo && (
                  <p className="mt-4 max-w-reading font-serif text-xl italic leading-snug text-(--sim-ink-soft) md:text-2xl">
                    {run.subtitulo}
                  </p>
                )}
                {resumen && (
                  // Registro del instrumento: la capa digital habla en monospace
                  <p className="sim-mono mt-3 text-xs text-(--sim-ink-soft)">
                    <code className="rounded bg-(--sim-paper-deep) px-1.5 py-0.5">
                      {resumen.run_id.slice(0, 8)}
                    </code>
                    <span className="mx-2 text-(--sim-rule)">·</span>
                    {resumen.model}
                    <span className="mx-2 text-(--sim-rule)">·</span>
                    {new Date(resumen.started_at).toLocaleDateString("es-VE", { dateStyle: "long" })}
                  </p>
                )}
              </header>

              {hero && <ManaureVoice fragment={hero} variant="hero" />}
              {run.manaure_hero &&
                getGlosasPorManaure(run.manaure_hero).map((g) => <GlosaCronista key={g.id} glosa={g} />)}

              {!resumen ? (
                <EmptyState
                  title="Aún no hay un run curado"
                  hint="Corre export_resumen_seed.py tras una simulación con --perfiles."
                />
              ) : (
                <>
                  <DataAside
                    items={[
                      { label: "Días simulados", value: resumen.total_days ?? 0, sub: `${resumen.total_turns ?? 0} turnos` },
                      { label: "Score promedio", value: resumen.avg_score?.toFixed(2) ?? "—", sub: "densidad lingüística / 10" },
                      { label: "% Caquetío", value: pctCaquetio, sub: "último turno" },
                      { label: "Adoptados", value: resumen.total_adoptados, sub: `de ${resumen.total_neologismos} propuestos` },
                    ]}
                  />

                  <Asterismo />

                  {/* La historia, folio por folio */}
                  {run.epocas.map((epoca, i) => {
                    const voz = epoca.manaure ? getManaureFragment(epoca.manaure) : null;
                    return (
                      <Epoca key={epoca.id} epoca={epoca} folio={i + 1}>
                        {voz && <ManaureVoice fragment={voz} />}
                        {epoca.eventos.length > 0 && (
                          <ol className="mt-6">
                            {epoca.eventos.map((ev, i) => (
                              <Fragment key={i}>
                                <EventoItem
                                  evento={ev}
                                  personajeNombre={ev.personaje ? nombrePorSlug.get(ev.personaje) : undefined}
                                />
                                {ev.forma &&
                                  getGlosasPorEvento(ev.forma).map((g) => (
                                    <li key={g.id} className="list-none pl-5">
                                      <GlosaCronista glosa={g} />
                                    </li>
                                  ))}
                              </Fragment>
                            ))}
                          </ol>
                        )}
                      </Epoca>
                    );
                  })}

                  <Asterismo />

                  {/* La deriva, medida — el chart embebido en la narrativa */}
                  <section id="deriva" className="mt-14 scroll-mt-24">
                    <Overline>La marea, medida</Overline>
                    <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
                      Composición de la lengua, turno a turno
                    </h2>
                    {derivaVoz && <ManaureVoice fragment={derivaVoz} />}
                    {run.deriva?.nota && (
                      <p className="mb-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                        {run.deriva.nota}
                      </p>
                    )}
                    <figure>
                      <LanguageDriftChart data={resumen.drift} />
                      <figcaption className="sim-mono mt-3 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
                        Fig. 1 · Proporción de cada lengua en el habla de la comunidad, por turno
                      </figcaption>
                    </figure>
                  </section>

                  {cierre && <ManaureVoice fragment={cierre} />}

                  {/* La crónica se sigue escribiendo */}
                  <p aria-hidden="true" className="mt-6">
                    <span className="sim-caret" />
                  </p>
                </>
              )}

              {/* El diccionario koiné: el producto del experimento, ya en el
                  registro del pergamino — las palabras que la comunidad fijó */}
              {runsIndex && runsIndex.runs.some((r) => r.fijacion) && (
                <>
                  <Asterismo />
                  <section id="diccionario-koine" className="scroll-mt-24">
                    <Overline>Lo que la comunidad nombró</Overline>
                    <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
                      El diccionario koiné
                    </h2>
                    <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
                      Cuando algo nuevo llegó al golfete — un cometa, una fiebre, un metal amarillo —
                      la comunidad necesitó nombrarlo. Varias formas compitieron; estas ganaron.
                    </p>
                    <DiccionarioKoine runs={runsIndex.runs} />
                  </section>
                </>
              )}

              {/* ══ ACTO III · SEGUIR EXPLORANDO ══════════════════════ */}
              <footer className="mt-14 border-t border-(--sim-rule) pt-8">
                <Overline>Acto III · Seguir explorando</Overline>
                <ul className="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-3">
                  {ANEXOS.map((a) => (
                    <li key={a.href}>
                      <Link href={a.href} className="group block">
                        <span className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                          {a.label} →
                        </span>
                        <span className="mt-1 block font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{a.desc}</span>
                      </Link>
                    </li>
                  ))}
                </ul>

                <p className="mt-10 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
                  {NOTA_HONESTIDAD}
                </p>
              </footer>
            </article>
          </div>
        </div>
      </div>
    </>
  );
}
