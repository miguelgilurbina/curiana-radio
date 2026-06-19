// Primitivas de UI del Simulador — lenguaje editorial de Curiana Radio
// (tonos tierra / azul profundo, serif Lora en títulos, acento frequency).
// Los colores salen de la única fuente de verdad: lib/sim-theme.ts
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
      className={`rounded-2xl border border-earth-200/70 bg-earth-50/80 backdrop-blur-sm shadow-sm ${className}`}
      style={style}
    >
      {children}
    </div>
  );
}

// ── Etiqueta de sección (overline) ────────────────────────────────────
export function Overline({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <span className={`font-sans text-[0.7rem] font-medium tracking-[0.18em] uppercase text-earth-600 ${className}`}>
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
    <Card className="p-5 transition-shadow hover:shadow-md">
      <Overline>{label}</Overline>
      <div className="mt-2 font-serif text-3xl md:text-4xl font-semibold leading-none" style={{ color: accent }}>
        {value}
      </div>
      {sub && <div className="mt-1.5 font-sans text-xs text-earth-500">{sub}</div>}
    </Card>
  );
}

// ── Barra de score 0–10 ───────────────────────────────────────────────
export function ScoreGauge({ score, width = 96 }: { score: number; width?: number }) {
  const pct = Math.max(0, Math.min(10, score)) * 10;
  const hue = scoreColor(score);
  return (
    <div className="flex items-center gap-2" title={`${score.toFixed(1)} / 10`}>
      <div className="h-1.5 rounded-full bg-earth-200 overflow-hidden" style={{ width }}>
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: hue }} />
      </div>
      <span className="font-sans text-xs tabular-nums text-earth-600">{score.toFixed(1)}</span>
    </div>
  );
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
    <span className="inline-flex items-center gap-1.5 font-sans text-xs text-earth-600">
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
  return <div className={`animate-pulse rounded-md bg-earth-200/60 ${className}`} style={style} />;
}

// ── Estado vacío ──────────────────────────────────────────────────────
export function EmptyState({ title, hint }: { title: string; hint?: ReactNode }) {
  return (
    <Card className="px-6 py-12 text-center">
      <div className="font-serif text-lg text-deep-800">{title}</div>
      {hint && <div className="mt-2 font-sans text-sm text-earth-600 max-w-md mx-auto">{hint}</div>}
    </Card>
  );
}
