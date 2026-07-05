import type { Metadata } from "next";
import Link from "next/link";
import { getRunActivo, getRunsPublicados } from "@/lib/editorial";
import { getManaureFragment } from "@/lib/manaure";
import { getResumen } from "@/lib/resumen";
import { getAllPersonajes } from "@/lib/personajes";
import ManaureVoice from "@/components/simulador/ManaureVoice";
import LanguageDriftChart from "@/components/simulador/LanguageDriftChart";
import { Epoca, EventoItem, DataAside } from "@/components/simulador/prose";
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
                ? "bg-deep-800 text-earth-50"
                : "border border-earth-200 text-earth-600"
            }`}
          >
            <span className="tabular-nums">{String(i + 1).padStart(2, "0")}</span>
            {r.fecha}
          </span>
        ))}
      </div>

      {/* Cabecera del run activo */}
      <header>
        <h2 className="font-serif text-3xl font-bold leading-tight text-deep-900 md:text-4xl">
          {run.titulo}
        </h2>
        {run.subtitulo && (
          <p className="mt-3 max-w-reading font-serif text-lg italic leading-snug text-earth-700">
            {run.subtitulo}
          </p>
        )}
        {resumen && (
          <p className="mt-3 font-sans text-sm text-earth-600">
            <code className="rounded bg-earth-100 px-1.5 py-0.5 text-earth-700">
              {resumen.run_id.slice(0, 8)}
            </code>
            <span className="mx-2 text-earth-300">·</span>
            {resumen.model}
            <span className="mx-2 text-earth-300">·</span>
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

          {/* La historia, época por época */}
          {run.epocas.map((epoca) => {
            const voz = epoca.manaure ? getManaureFragment(epoca.manaure) : null;
            return (
              <Epoca key={epoca.id} epoca={epoca}>
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

          {/* La deriva, medida — el chart embebido en la narrativa */}
          <section id="deriva" className="mt-14 scroll-mt-24">
            <Overline>La marea, medida</Overline>
            <h2 className="mt-1 font-serif text-2xl font-semibold text-deep-900 md:text-3xl">
              Composición de la lengua, turno a turno
            </h2>
            {derivaVoz && <ManaureVoice fragment={derivaVoz} />}
            {run.deriva?.nota && (
              <p className="mb-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
                {run.deriva.nota}
              </p>
            )}
            <LanguageDriftChart data={resumen.drift} />
          </section>

          {cierre && <ManaureVoice fragment={cierre} />}
        </>
      )}

      {/* Anexos: la wiki de referencia detrás de la historia */}
      <footer className="mt-14 border-t border-earth-200/70 pt-8">
        <Overline>Seguir explorando</Overline>
        <ul className="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-3">
          {ANEXOS.map((a) => (
            <li key={a.href}>
              <Link href={a.href} className="group block">
                <span className="font-serif text-lg font-semibold text-deep-900 transition-colors group-hover:text-frequency">
                  {a.label} →
                </span>
                <span className="mt-1 block font-sans text-sm leading-relaxed text-earth-600">{a.desc}</span>
              </Link>
            </li>
          ))}
        </ul>

        <p className="mt-10 max-w-reading font-sans text-xs leading-relaxed text-earth-500">
          Sobre este contenido: las voces del narrador y de Manaure son reconstrucción editorial
          hipotética, escrita para esta publicación. Los datos — palabras, adopciones, deriva — salen
          de la simulación tal cual ocurrieron. El caquetío de los fragmentos usa la morfología
          documentada del proyecto y se marca siempre con su grado de certeza.
        </p>
      </footer>
    </article>
  );
}
