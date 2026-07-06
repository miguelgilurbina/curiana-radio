// Primitivas de UI del Simulador — tema "Cronista digital": papel pergamino,
// tinta parda, rúbrica roja para lo editorial (tokens --sim-* en globals.css,
// scoped al data-sim-theme del layout). Colores de DATOS: lib/sim-theme.ts
import type { ReactNode, CSSProperties } from "react";
import { scoreColor } from "@/lib/sim-theme";

export { LANGS } from "@/lib/sim-theme";

// ── Superficie / tarjeta ──────────────────────────────────────────────
export function Card({
  children,
  className = "",
  style,
}: {
  children: ReactNode;
  className?: string;
  style?: CSSProperties;
}) {
  return (
    <div
      className={`sim-card rounded-2xl border border-(--sim-rule) bg-(--sim-paper-deep) backdrop-blur-sm ${className}`}
      style={style}
    >
      {children}
    </div>
  );
}

// ── Etiqueta de sección (overline) ────────────────────────────────────
// Rúbrica del cronista: lo editorial va en tinta roja, como en las crónicas
// reales (de ahí la palabra "rúbrica").
export function Overline({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <span className={`font-sans text-[0.7rem] font-medium tracking-[0.18em] uppercase text-(--sim-rubrica) ${className}`}>
      {children}
    </span>
  );
}

// ── Tarjeta de métrica ────────────────────────────────────────────────
export function StatCard({
  label,
  value,
  sub,
  accent = "#3d5777",
}: {
  label: string;
  value: ReactNode;
  sub?: string;
  accent?: string;
}) {
  return (
    <Card className="p-5 sim-card-hover">
      <Overline>{label}</Overline>
      <div className="mt-2 font-serif text-3xl md:text-4xl font-semibold leading-none" style={{ color: accent }}>
        {value}
      </div>
      {sub && <div className="mt-1.5 font-sans text-xs text-(--sim-ink-faint)">{sub}</div>}
    </Card>
  );
}

// ── Barra de score 0–10 ───────────────────────────────────────────────
export function ScoreGauge({ score, width = 96 }: { score: number; width?: number }) {
  const pct = Math.max(0, Math.min(10, score)) * 10;
  const hue = scoreColor(score);
  return (
    <div className="flex items-center gap-2" title={`${score.toFixed(1)} / 10`}>
      <div className="h-1.5 rounded-full bg-(--sim-rule) overflow-hidden" style={{ width }}>
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: hue }} />
      </div>
      <span className="font-sans text-xs tabular-nums text-(--sim-ink-soft)">{score.toFixed(1)}</span>
    </div>
  );
}

// ── Avatar de agente (iniciales, color determinista) ──────────────────
const AVATAR_COLORS = ["#C47A2B", "#2E7D4F", "#5B4FCF", "#B04040", "#6D8A9E", "#3d5777", "#8a6c57"];

export function Avatar({ name, size = 34 }: { name: string; size?: number }) {
  const clean = (name || "?").replace(/[^\p{L}]/gu, " ").trim();
  const parts = clean.split(/\s+/);
  const initials = (parts.length > 1 ? parts[0][0] + parts[1][0] : clean.slice(0, 2)).toUpperCase();
  let h = 0;
  for (let i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0;
  const color = AVATAR_COLORS[h % AVATAR_COLORS.length];
  return (
    <span
      aria-hidden="true"
      className="inline-flex shrink-0 items-center justify-center rounded-full font-serif font-semibold"
      style={{ width: size, height: size, background: `${color}1f`, color, fontSize: size * 0.4 }}
    >
      {initials}
    </span>
  );
}

// ── Tiempo relativo ("hace 2 min") ────────────────────────────────────
export function relativeTime(iso?: string): string {
  if (!iso) return "";
  const d = new Date(iso).getTime();
  if (Number.isNaN(d)) return "";
  const s = Math.max(0, Math.round((Date.now() - d) / 1000));
  if (s < 45) return "ahora";
  const m = Math.round(s / 60);
  if (m < 60) return `hace ${m} min`;
  const h = Math.round(m / 60);
  if (h < 24) return `hace ${h} h`;
  const dd = Math.round(h / 24);
  return `hace ${dd} d`;
}

// ── Pill de lengua / etiqueta de color ────────────────────────────────
export function LangPill({ color, children }: { color: string; children: ReactNode }) {
  return (
    <span
      className="inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-sans text-[0.7rem] font-medium"
      style={{ background: `${color}1a`, color, border: `1px solid ${color}33` }}
    >
      {children}
    </span>
  );
}

// ── Indicador "en vivo" ───────────────────────────────────────────────
export function LiveDot({ status }: { status: "connecting" | "live" | "off" }) {
  const color = status === "live" ? "#2E7D4F" : status === "connecting" ? "#C47A2B" : "#9d7f66";
  const label = status === "live" ? "En vivo" : status === "connecting" ? "Conectando" : "Sin conexión";
  return (
    <span className="inline-flex items-center gap-1.5 font-sans text-xs text-(--sim-ink-soft)">
      <span className="relative flex h-2 w-2">
        {status === "live" && (
          <span className="absolute inline-flex h-full w-full rounded-full opacity-60 animate-ping" style={{ background: color }} />
        )}
        <span className="relative inline-flex h-2 w-2 rounded-full" style={{ background: color }} />
      </span>
      {label}
    </span>
  );
}

// ── Skeleton de carga ─────────────────────────────────────────────────
export function Skeleton({ className = "", style }: { className?: string; style?: CSSProperties }) {
  return <div className={`animate-pulse rounded-md bg-(--sim-rule) ${className}`} style={style} />;
}

// ── Estado vacío ──────────────────────────────────────────────────────
export function EmptyState({ title, hint }: { title: string; hint?: ReactNode }) {
  return (
    <Card className="px-6 py-12 text-center">
      <div className="font-serif text-lg text-(--sim-ink)">{title}</div>
      {hint && <div className="mt-2 font-sans text-sm text-(--sim-ink-soft) max-w-md mx-auto">{hint}</div>}
    </Card>
  );
}
