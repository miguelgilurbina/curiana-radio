import Link from "next/link";
import type { Metadata } from "next";
import type { PreguntaAbierta } from "@/types/fichas";
import { getNoSabemos } from "@/lib/fichas";
import { Overline, EmptyState } from "@/components/simulador/ui";

export const metadata: Metadata = {
  title: "Lo que no sabemos — Kaketiana | Curiana Radio",
  description:
    "Las preguntas que el proyecto caquetío no ha podido cerrar, con lo que hay medido hasta hoy y de dónde sale cada cifra.",
};

// El borde de lo que sabemos. Las preguntas, su planteamiento y cada cifra
// vienen de content/wiki/no-sabemos.json (export_no_sabemos_seed.py), que las
// lee de los YAML de medición del vault al exportar: aquí no se escribe
// ningún número.

const ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];

function formatear(n: number): string {
  return n.toLocaleString("es-VE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function Barras({ barras }: { barras: NonNullable<PreguntaAbierta["barras"]> }) {
  return (
    <figure className="mt-6">
      <figcaption className="sim-mono text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
        {barras.titulo}
      </figcaption>
      <ul className="mt-3 space-y-2.5">
        {barras.filas.map((b) => (
          <li key={b.etiqueta} className="grid grid-cols-[minmax(0,1fr)_auto] gap-x-3 gap-y-1 sm:grid-cols-[13rem_minmax(0,1fr)_3rem] sm:items-center">
            <span className="font-sans text-sm text-(--sim-ink)">{b.etiqueta}</span>
            <span className="sim-mono text-right text-sm tabular-nums text-(--sim-ink) sm:order-last">
              {formatear(b.valor)}
            </span>
            <span className="col-span-2 sm:col-span-1">
              <span className="block h-2 rounded-full bg-(--sim-rule)" aria-hidden="true">
                <span
                  className="block h-2 rounded-full bg-(--sim-fuego)"
                  style={{ width: `${Math.max(0, Math.min(1, b.valor)) * 100}%` }}
                />
              </span>
              <span className="mt-0.5 block font-sans text-xs text-(--sim-ink-faint)">{b.detalle}</span>
            </span>
          </li>
        ))}
      </ul>
    </figure>
  );
}

function Pregunta({ p, numero }: { p: PreguntaAbierta; numero: number }) {
  const espera = p.estado === "espera-la-corrida-base";
  return (
    <section id={p.slug} className="mt-16 scroll-mt-24 border-t border-(--sim-rule) pt-8 first:mt-10">
      <div className="flex items-baseline gap-4">
        <span aria-hidden="true" className="sim-display w-8 shrink-0 text-2xl text-(--sim-rubrica)">
          {ROMANOS[numero] ?? numero + 1}
        </span>
        <div className="min-w-0">
          <h2 className="sim-display text-2xl font-semibold leading-tight text-(--sim-ink) md:text-3xl">
            {p.pregunta}
          </h2>
          {espera && (
            <span className="mt-3 inline-flex items-center rounded-full border border-dashed border-(--sim-ink-faint) px-2.5 py-0.5 font-sans text-[0.7rem] font-medium uppercase tracking-[0.12em] text-(--sim-ink-soft)">
              Espera la corrida base
            </span>
          )}

          <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            {p.planteamiento}
          </p>

          {p.medido.length > 0 && (
            <div className="mt-6 border-l-2 border-(--sim-fuego) pl-4">
              <Overline>Lo medido</Overline>
              <ul className="mt-2 space-y-2">
                {p.medido.map((m) => (
                  <li key={m} className="max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink)">
                    {m}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {p.barras && <Barras barras={p.barras} />}

          <p className="mt-6 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            <strong className="font-semibold text-(--sim-ink)">Lo que falta.</strong> {p.lo_que_falta}
          </p>

          <div className="mt-6 space-y-1">
            {p.fuentes.map((f) => (
              <p key={f.ruta} className="font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
                <span className="uppercase tracking-[0.12em]">Fuente</span>{" "}
                <code className="sim-mono break-all text-[0.95em] text-(--sim-ink-soft)">{f.ruta}</code>
                {" — "}
                {f.que}
                {f.fecha && <span className="sim-mono tabular-nums"> · {f.fecha}</span>}
              </p>
            ))}
          </div>

          {p.enlaces.length > 0 && (
            <div className="mt-4 flex flex-wrap gap-x-5 gap-y-1.5 font-sans text-sm">
              {p.enlaces.map((e) => (
                <Link
                  key={e.href}
                  href={e.href}
                  className="font-medium text-(--sim-fuego) transition-colors hover:text-(--sim-rubrica)"
                >
                  {e.texto} →
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default function NoSabemosPage() {
  const { preguntas, generado } = getNoSabemos();
  const abiertas = preguntas.filter((p) => p.estado === "abierta").length;

  return (
    <article className="mx-auto max-w-[760px]">
      <Link
        href="/kaketiana"
        className="font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-fuego)"
      >
        ← Kaketiana
      </Link>

      <header className="mt-5">
        <Overline>El borde</Overline>
        <h1 className="mt-1 sim-display text-4xl font-bold tracking-tight text-(--sim-ink) md:text-5xl">
          Lo que no sabemos
        </h1>
        <p className="mt-4 max-w-reading font-sans text-lg leading-relaxed text-(--sim-ink-soft)">
          Reconstruir una lengua sin hablantes es, sobre todo, saber dónde se acaba lo que se sabe.
          Estas son las preguntas que el proyecto no ha podido cerrar, con lo que hay medido hasta hoy.
        </p>
        {preguntas.length > 0 && (
          <p className="mt-3 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-faint)">
            {abiertas} abiertas; {preguntas.length - abiertas} a la espera de la corrida base. Cada cifra
            sale de un archivo de medición del proyecto, y se dice cuál
            {generado && <> — generado el <span className="sim-mono tabular-nums">{generado}</span></>}.
          </p>
        )}
      </header>

      {preguntas.length === 0 ? (
        <div className="mt-8">
          <EmptyState title="Aún no hay preguntas" hint="Corre export_no_sabemos_seed.py." />
        </div>
      ) : (
        <>
          <nav aria-label="Las preguntas" className="mt-8">
            <ol className="space-y-1.5 font-sans text-sm">
              {preguntas.map((p, i) => (
                <li key={p.slug} className="flex gap-3">
                  <span className="sim-display w-8 shrink-0 text-(--sim-rubrica)">{ROMANOS[i] ?? i + 1}</span>
                  <a
                    href={`#${p.slug}`}
                    className="text-(--sim-ink-soft) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:text-(--sim-fuego)"
                  >
                    {p.pregunta}
                  </a>
                </li>
              ))}
            </ol>
          </nav>

          {preguntas.map((p, i) => (
            <Pregunta key={p.slug} p={p} numero={i} />
          ))}
        </>
      )}
    </article>
  );
}
