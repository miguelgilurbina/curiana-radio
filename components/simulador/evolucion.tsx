// La evolución entre simulaciones: el meta-relato del proyecto.
// Cada run es una expedición del cronista; esta capa las junta y deja leer
// el arco (deriva plana → koiné con diccionario → experimento de control).
// Datos: content/simulador/runs/index.json vía lib/runs.ts — medido, no
// narrativa; por eso habla casi todo en monospace (registro del instrumento).
import type { RunIndexEntry, FormaFijada } from "@/lib/runs";
import { RUN_CATEGORIAS } from "@/lib/sim-theme";

const fmtFecha = (iso: string) =>
  new Date(iso).toLocaleDateString("es-VE", { day: "numeric", month: "short", year: "numeric" });

// ── Sparkline: el trazo del instrumento ───────────────────────────────
// Distancia idiolectal media por día; baja = las voces se acercan.
function Sparkline({ serie, color }: { serie: number[]; color: string }) {
  if (serie.length < 2) return null;
  const w = 112;
  const h = 26;
  const pad = 2;
  const min = Math.min(...serie);
  const max = Math.max(...serie);
  const span = max - min || 1;
  const pts = serie.map((v, i) => {
    const x = pad + (i / (serie.length - 1)) * (w - pad * 2);
    const y = pad + ((max - v) / span) * (h - pad * 2);
    return [x, y] as const;
  });
  const d = pts.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`).join(" ");
  const [ex, ey] = pts[pts.length - 1];
  return (
    <svg
      viewBox={`0 0 ${w} ${h}`}
      width={w}
      height={h}
      aria-hidden="true"
      className="shrink-0 overflow-visible"
    >
      <path d={d} fill="none" stroke={color} strokeWidth="1.5" strokeLinecap="round" opacity="0.85" />
      <circle cx={ex} cy={ey} r="2.4" fill={color} />
    </svg>
  );
}

// ── Una expedición del cronista ───────────────────────────────────────
function RunEntry({ run }: { run: RunIndexEntry }) {
  const cat = RUN_CATEGORIAS[run.categoria] ?? RUN_CATEGORIAS.koine;
  const conv = run.convergencia;
  const pctCaq = run.pct_caquetio != null ? Math.round(run.pct_caquetio * 100) : null;

  return (
    <li className="relative border-l border-(--sim-rule) pl-5 pb-10 last:pb-0">
      <span
        aria-hidden="true"
        className="absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full"
        style={{ background: cat.color }}
      />

      {/* Registro del instrumento: id, fecha, tamaño */}
      <div className="flex flex-wrap items-center gap-2 font-sans text-xs text-(--sim-ink-faint)">
        <code className="sim-mono rounded bg-(--sim-paper-deep) px-1.5 py-0.5 text-(--sim-ink-soft)">
          {run.id8}
        </code>
        <span>{fmtFecha(run.started_at)}</span>
        {run.total_turnos != null && (
          <span className="tabular-nums">
            {run.total_turnos} turnos · {run.total_dias} días
          </span>
        )}
        <span
          className="inline-flex items-center rounded-full px-2 py-0.5 font-medium"
          style={{ background: `${cat.color}1a`, color: cat.color, border: `1px solid ${cat.color}33` }}
        >
          {run.rol === "ablacion" ? "⚗ ablación" : run.rol === "normal" ? "⚗ experimento · normal" : cat.label}
        </span>
      </div>

      {/* La voz editorial: qué significó este run */}
      <p className="mt-1.5 max-w-reading font-serif text-lg leading-snug text-(--sim-ink)">{run.hito}</p>

      {/* La medición */}
      <div className="mt-3 flex flex-wrap items-end gap-x-8 gap-y-3">
        {pctCaq != null && (
          <div>
            <span className="sim-mono block text-[0.65rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              Caquetío
            </span>
            <span className="sim-mono mt-0.5 block text-xl font-semibold leading-none tabular-nums text-(--sim-ink)">
              {pctCaq}%
            </span>
          </div>
        )}
        {conv?.delta_pct != null && (
          <div>
            <span className="sim-mono block text-[0.65rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              Convergencia · {conv.lectura}
              {conv.lectura === "acumulada" && " †"}
            </span>
            <span className="mt-0.5 flex items-end gap-3">
              <span className="sim-mono text-xl font-semibold leading-none tabular-nums text-(--sim-ink)">
                {conv.delta_pct > 0 ? "+" : "−"}
                {Math.abs(conv.delta_pct).toFixed(1)}%
              </span>
              <Sparkline serie={conv.serie} color={cat.color} />
            </span>
          </div>
        )}
        {run.neologismos_adoptados > 0 && (
          <div>
            <span className="sim-mono block text-[0.65rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              Adoptadas
            </span>
            <span className="sim-mono mt-0.5 block text-xl font-semibold leading-none tabular-nums text-(--sim-ink)">
              {run.neologismos_adoptados}
            </span>
          </div>
        )}
        {run.fijacion && (
          <div>
            <span className="sim-mono block text-[0.65rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
              Fijadas
            </span>
            <span className="sim-mono mt-0.5 block text-xl font-semibold leading-none tabular-nums text-(--sim-ink)">
              {run.fijacion.conceptos_fijados}
            </span>
          </div>
        )}
      </div>
    </li>
  );
}

// ── La línea de tiempo completa ───────────────────────────────────────
export function EvolucionTimeline({ runs }: { runs: RunIndexEntry[] }) {
  const hayAcumulada = runs.some((r) => r.convergencia?.lectura === "acumulada");
  return (
    <div>
      <ol className="mt-8">
        {runs.map((run) => (
          <RunEntry key={run.id8} run={run} />
        ))}
      </ol>
      {hayAcumulada && (
        <p className="mt-6 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
          † Runs anteriores a la corrección metodológica del 4 de julio: solo midieron la distancia
          acumulada, que converge en parte por acumulación del vocabulario compartido. Los runs
          posteriores usan la lectura <em>emergente</em> (solo formas nuevas), más exigente y honesta.
        </p>
      )}
    </div>
  );
}

// ── El diccionario koiné: las palabras que la comunidad fijó ──────────
// Entradas de diccionario real: lema en display, glosa en serif, la
// trazabilidad (variantes rivales, día, run) en el registro del instrumento.
function EntradaDiccionario({ forma, id8 }: { forma: FormaFijada; id8: string }) {
  return (
    <div className="border-t border-(--sim-rule) py-4">
      <dt className="sim-display text-xl font-semibold text-(--sim-fuego)">{forma.form}</dt>
      <dd className="mt-1">
        {forma.descripcion && (
          <p className="max-w-reading font-serif italic leading-snug text-(--sim-ink-soft)">
            «{forma.descripcion}»
          </p>
        )}
        <p className="sim-mono mt-1.5 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
          {forma.n_variantes != null && `venció a ${forma.n_variantes - 1} rival${forma.n_variantes - 1 === 1 ? "" : "es"}`}
          {forma.fijada_dia != null && ` · fijada el día ${forma.fijada_dia}`}
          {" · "}
          <code>{id8}</code>
        </p>
      </dd>
    </div>
  );
}

export function DiccionarioKoine({ runs }: { runs: RunIndexEntry[] }) {
  const entradas = runs
    .filter((r) => r.fijacion)
    .flatMap((r) => r.fijacion!.formas.map((forma) => ({ forma, id8: r.id8 })));
  if (entradas.length === 0) return null;

  return (
    <div>
      <dl className="mt-8 grid grid-cols-1 gap-x-10 sm:grid-cols-2">
        {entradas.map(({ forma, id8 }) => (
          <EntradaDiccionario key={`${id8}-${forma.concepto}`} forma={forma} id8={id8} />
        ))}
      </dl>
      <p className="mt-8 max-w-reading font-sans text-xs leading-relaxed text-(--sim-ink-faint)">
        Sobre estas palabras: ningún diccionario colonial las registra — nacieron dentro de la
        simulación, cuando la comunidad necesitó nombrar algo nuevo y varias formas rivales
        compitieron hasta que una se fijó. Usan la morfología caquetía documentada del proyecto,
        pero son lengua simulada, no reconstrucción histórica.
      </p>
    </div>
  );
}
