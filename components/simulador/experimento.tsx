// La prueba de control: el par normal vs. ablación. La sección más "de
// laboratorio" del simulador — su tesis es metodológica, no narrativa: la
// koineización emergente se prueba por la DIFERENCIA entre un run con el
// andamiaje de prompt encendido y su gemelo con el andamiaje apagado.
// Datos: getParejaExperimento() en lib/runs.ts.
import type { RunIndexEntry } from "@/lib/runs";
import ConvergenciaChart from "@/components/simulador/ConvergenciaChart";

function pct(delta: number | null): string {
  if (delta == null) return "—";
  return `${delta > 0 ? "+" : "−"}${Math.abs(delta).toFixed(1)}%`;
}

// Una columna de la comparación (un brazo del experimento).
function Brazo({
  run,
  color,
  etiqueta,
}: {
  run: RunIndexEntry;
  color: string;
  etiqueta: string;
}) {
  const conv = run.convergencia;
  return (
    <div className="flex-1">
      <div className="flex items-center gap-2">
        <span aria-hidden="true" className="inline-block h-2.5 w-2.5 rounded-full" style={{ background: color }} />
        <span className="font-sans text-sm font-semibold text-(--sim-ink)">{etiqueta}</span>
        <code className="sim-mono rounded bg-(--sim-paper-deep) px-1.5 py-0.5 text-[0.7rem] text-(--sim-ink-soft)">
          {run.id8}
        </code>
      </div>
      <dl className="mt-3 space-y-2">
        <div className="flex items-baseline justify-between gap-3">
          <dt className="sim-mono text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
            Convergencia
          </dt>
          <dd className="sim-mono text-lg font-semibold tabular-nums text-(--sim-ink)">
            {pct(conv?.delta_pct ?? null)}
          </dd>
        </div>
        <div className="flex items-baseline justify-between gap-3">
          <dt className="sim-mono text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
            Conceptos fijados
          </dt>
          <dd className="sim-mono text-lg font-semibold tabular-nums text-(--sim-ink)">
            {run.fijacion?.conceptos_fijados ?? 0}
            <span className="text-(--sim-ink-faint)"> / 10</span>
          </dd>
        </div>
        <div className="flex items-baseline justify-between gap-3">
          <dt className="sim-mono text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
            Palabras adoptadas
          </dt>
          <dd className="sim-mono text-lg font-semibold tabular-nums text-(--sim-ink)">
            {run.neologismos_adoptados}
          </dd>
        </div>
      </dl>
    </div>
  );
}

export function ExperimentoControl({
  normal,
  ablacion,
}: {
  normal: RunIndexEntry;
  ablacion: RunIndexEntry;
}) {
  const dNormal = normal.convergencia?.delta_pct ?? null;
  const dAblacion = ablacion.convergencia?.delta_pct ?? null;
  const factor =
    dNormal != null && dAblacion != null && dAblacion !== 0
      ? Math.abs(dNormal / dAblacion)
      : null;

  return (
    <div>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        ¿Y si la lengua converge sola, sin que nada la empuje? Para saberlo corrimos dos veces la
        misma simulación: una <strong className="font-semibold text-(--sim-ink)">normal</strong>, y
        otra de <strong className="font-semibold text-(--sim-ink)">control</strong> con el andamiaje
        apagado — sin sugerir contagio entre agentes, sin abrir competencias por nombrar las cosas,
        sin reforzar las formas ya usadas. Si ambas convergen igual, la koiné era un truco del
        andamiaje. No lo fue.
      </p>

      <figure className="mt-6">
        <ConvergenciaChart
          normal={normal.convergencia?.serie ?? []}
          ablacion={ablacion.convergencia?.serie ?? []}
        />
        <figcaption className="sim-mono mt-3 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
          Fig. 2 · Distancia idiolectal media por día (lectura emergente: solo formas nuevas). Baja =
          las voces se acercan. La normal sigue cayendo; el control se estanca hacia el día 16.
        </figcaption>
      </figure>

      <div className="mt-8 flex flex-col gap-6 rounded-2xl border border-(--sim-rule) bg-(--sim-paper-deep) p-6 sm:flex-row">
        <Brazo run={normal} color="#5B4FCF" etiqueta="Normal" />
        <div aria-hidden="true" className="hidden w-px self-stretch bg-(--sim-rule) sm:block" />
        <Brazo run={ablacion} color="#9d7f66" etiqueta="Ablación (control)" />
      </div>

      {factor != null && (
        <p className="mt-6 max-w-reading font-serif text-lg leading-snug text-(--sim-ink)">
          Con el andamiaje encendido, la comunidad converge{" "}
          <strong className="font-semibold text-(--sim-fuego)">{factor.toFixed(1)}× más</strong> que
          su control. Esa diferencia — no la caída de la curva normal por sí sola — es la evidencia
          de que la koiné <em>emerge</em>.
        </p>
      )}

      <p className="mt-6 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
        Nota metodológica: la convergencia se lee en tres escalas (acumulada, ventana y emergente);
        esta figura usa la emergente, la más exigente, que solo mira las formas nacidas en la
        simulación. La acumulada de ambos runs es casi idéntica (−44% vs −41%) porque converge por
        mera acumulación del vocabulario compartido — un artefacto, no koineización.
      </p>
    </div>
  );
}
