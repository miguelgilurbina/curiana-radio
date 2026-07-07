import type { Metadata } from "next";
import Link from "next/link";
import { getRunActivo, getRunsPublicados } from "@/lib/editorial";
import { getManaureFragment } from "@/lib/manaure";
import { getResumen } from "@/lib/resumen";
import { getAllPersonajes } from "@/lib/personajes";
import { getRunsIndex } from "@/lib/runs";
import { EvolucionTimeline, DiccionarioKoine } from "@/components/simulador/evolucion";
import ManaureVoice from "@/components/simulador/ManaureVoice";
import LanguageDriftChart from "@/components/simulador/LanguageDriftChart";
import { Epoca, EventoItem, DataAside, Asterismo } from "@/components/simulador/prose";
import { Overline, EmptyState } from "@/components/simulador/ui";

export function generateMetadata(): Metadata {
  const run = getRunActivo();
  return {
    title: `${run.titulo} — Simulador Caquetío | Curiana Radio`,
    description: run.subtitulo,
  };
}

const ANEXOS = [
  { href: "/simulador/personajes", label: "Personajes", desc: "Las veinte voces curadas del run y sus arcos." },
  { href: "/simulador/lexicon", label: "Léxico", desc: "El vocabulario reconstruido, palabra por palabra." },
  { href: "/simulador/neologisms", label: "Neologismos", desc: "Todas las palabras inventadas: las que prendieron y las que no." },
];

export default function SimuladorPage() {
  const runs = getRunsPublicados();
  const run = getRunActivo();
  const resumen = getResumen();
  const runsIndex = getRunsIndex();
  const nombrePorSlug = new Map(getAllPersonajes().map((p) => [p.slug, p.nombre]));

  const hero = run.manaure_hero ? getManaureFragment(run.manaure_hero) : null;
  const derivaVoz = run.deriva?.manaure ? getManaureFragment(run.deriva.manaure) : null;
  const cierre = run.manaure_cierre ? getManaureFragment(run.manaure_cierre) : null;

  const pctCaquetio =
    resumen?.pct_caquetio_final != null ? `${Math.round(resumen.pct_caquetio_final * 100)}%` : "—";

  return (
    <article className="mx-auto max-w-[720px]">
      {/* Índice de ediciones: hoy una, la arquitectura lista para varias */}
      <div className="mb-6 flex flex-wrap items-center gap-2">
        <Overline>Ediciones</Overline>
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
        {/* Headline + deck, jerarquía de revista */}
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
                      <EventoItem
                        key={i}
                        evento={ev}
                        personajeNombre={ev.personaje ? nombrePorSlug.get(ev.personaje) : undefined}
                      />
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

      {/* El meta-relato: qué pasó ENTRE las simulaciones */}
      {runsIndex && runsIndex.runs.length > 1 && (
        <>
          <Asterismo />
          <section id="evolucion" className="scroll-mt-24">
            <Overline>Bitácora de expediciones</Overline>
            <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
              La evolución, simulación a simulación
            </h2>
            <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
              Cada corrida es una expedición: mismo golfete, misma gente, y un instrumento que cada
              vez mide mejor. Lo que empezó como una comunidad que apenas sostenía su lengua terminó
              formando una koiné — y la última expedición salió con un grupo de control para probar
              que la convergencia no era un truco del andamiaje.
            </p>
            <EvolucionTimeline runs={runsIndex.runs} />
          </section>

          <Asterismo />
          <section id="diccionario-koine" className="scroll-mt-24">
            <Overline>Lo que la comunidad nombró</Overline>
            <h2 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
              El diccionario koiné
            </h2>
            <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
              Cuando algo nuevo llegó al golfete — un cometa, una fiebre, un metal amarillo — la
              comunidad necesitó nombrarlo. Varias formas compitieron; estas ganaron.
            </p>
            <DiccionarioKoine runs={runsIndex.runs} />
          </section>
        </>
      )}

      {/* Anexos: la wiki de referencia detrás de la historia */}
      <footer className="mt-14 border-t border-(--sim-rule) pt-8">
        <Overline>Seguir explorando</Overline>
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
          Sobre este contenido: las voces del narrador y de Manaure son reconstrucción editorial
          hipotética, escrita para esta publicación. Los datos — palabras, adopciones, deriva — salen
          de la simulación tal cual ocurrieron. El caquetío de los fragmentos usa la morfología
          documentada del proyecto y se marca siempre con su grado de certeza.
        </p>
      </footer>
    </article>
  );
}
