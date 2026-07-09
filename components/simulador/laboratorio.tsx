// Acto I — el laboratorio: el abstract de disertación del proyecto.
// Estas piezas viven dentro de [data-sim-acto="laboratorio"], que redefine
// la paleta --sim-* al registro oscuro del instrumento (ver globals.css):
// por eso hablan con los mismos tokens que el cronista y no llevan colores
// propios, salvo los de DATOS (lib/sim-theme.ts).
import type { AbstractContent, ConceptoAbstract, PasoPipeline } from "@/lib/abstract";
import { Overline } from "@/components/simulador/ui";

// ── La portada del laboratorio ────────────────────────────────────────
export function PortadaLab({ pitch }: { pitch: AbstractContent["pitch"] }) {
  return (
    <header>
      <Overline>{pitch.overline}</Overline>
      <h2 className="sim-display mt-2 text-4xl font-semibold leading-[1.02] tracking-tight text-(--sim-ink) sm:text-5xl md:text-6xl">
        {pitch.titulo}
      </h2>
      <p className="mt-6 max-w-reading font-sans text-base leading-relaxed text-(--sim-ink-soft) md:text-lg">
        {pitch.bajada}
      </p>
    </header>
  );
}

// ── El abstract formal (registro de paper, voz de disertación) ────────
export function AbstractCientifico({ parrafos }: { parrafos: string[] }) {
  return (
    <section id="abstract" className="mt-14 scroll-mt-24">
      <Overline>Abstract</Overline>
      <div className="sim-capitular mt-4 border-l-[3px] border-(--sim-rubrica)/70 pl-5 md:pl-7">
        {parrafos.map((p, i) => (
          <p
            key={i}
            className="mt-5 max-w-reading font-serif text-lg leading-relaxed text-(--sim-ink) first:mt-0"
          >
            {p}
          </p>
        ))}
      </div>
    </section>
  );
}

// ── Los conceptos: el experimento, término a término ──────────────────
function Concepto({ concepto, n }: { concepto: ConceptoAbstract; n: number }) {
  return (
    <div id={`concepto-${concepto.id}`} className="scroll-mt-24">
      <dt className="flex items-baseline gap-3">
        <span className="sim-mono text-xs tabular-nums text-(--sim-ink-faint)">
          {String(n).padStart(2, "0")}
        </span>
        <span className="sim-display text-xl font-semibold text-(--sim-ink)">
          {concepto.termino}
        </span>
      </dt>
      <dd className="mt-1.5">
        <p className="font-serif italic leading-snug text-(--sim-fuego)">{concepto.lema}</p>
        <p className="mt-2 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
          {concepto.cuerpo}
        </p>
        {concepto.dato && (
          <p className="sim-mono mt-3 border-l-2 border-(--sim-rubrica)/60 pl-3 text-xs leading-relaxed text-(--sim-ink-soft)">
            {concepto.dato}
          </p>
        )}
      </dd>
    </div>
  );
}

export function Conceptos({ conceptos }: { conceptos: ConceptoAbstract[] }) {
  return (
    <section id="conceptos" className="mt-14 scroll-mt-24">
      <Overline>Los conceptos</Overline>
      <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
        El experimento, término a término
      </h3>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        Estas ideas bastan para leer todo lo que sigue. Ninguna requiere haber estudiado
        lingüística; todas están medidas en los datos.
      </p>
      <dl className="mt-8 grid grid-cols-1 gap-x-12 gap-y-10 sm:grid-cols-2">
        {conceptos.map((c, i) => (
          <Concepto key={c.id} concepto={c} n={i + 1} />
        ))}
      </dl>
    </section>
  );
}

// ── El pipeline: de las crónicas al dato ──────────────────────────────
export function PipelineFlujo({ pasos }: { pasos: PasoPipeline[] }) {
  return (
    <section id="pipeline" className="mt-14 scroll-mt-24">
      <Overline>El flujo</Overline>
      <h3 className="sim-display mt-1 text-3xl font-semibold tracking-tight text-(--sim-ink) md:text-4xl">
        De las crónicas al dato
      </h3>
      <ol className="mt-8 flex flex-col items-stretch gap-3 lg:flex-row lg:items-center">
        {pasos.map((paso, i) => (
          <li key={paso.titulo} className="contents">
            {i > 0 && (
              <span
                aria-hidden="true"
                className="self-center font-serif text-xl leading-none text-(--sim-rubrica) rotate-90 lg:rotate-0"
              >
                →
              </span>
            )}
            <div className="flex-1 rounded-xl border border-(--sim-rule) bg-(--sim-paper-deep) p-4">
              <span className="sim-mono text-[0.65rem] tabular-nums uppercase tracking-[0.14em] text-(--sim-ink-faint)">
                {String(i + 1).padStart(2, "0")}
              </span>
              <p className="sim-display mt-0.5 text-lg font-semibold text-(--sim-ink)">
                {paso.titulo}
              </p>
              <p className="mt-1 font-sans text-xs leading-relaxed text-(--sim-ink-soft)">
                {paso.sub}
              </p>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
