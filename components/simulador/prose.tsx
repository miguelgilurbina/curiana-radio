// Primitivas de la wiki narrativa: la columna de lectura del simulador.
// Complementan a ui.tsx (que sigue siendo la capa de tarjetas/badges);
// estas piezas arman el flujo de texto: épocas, eventos, datos embebidos.
import type { ReactNode } from "react";
import Link from "next/link";
import type { EventoEditorial, EpocaEditorial } from "@/lib/editorial";
import { EVENTO_TIPOS } from "@/lib/sim-theme";
import { Avatar } from "@/components/simulador/ui";

const ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];

// ── Sección de época (folio del manuscrito, ancla de la cronología) ────
export function Epoca({
  epoca,
  folio,
  children,
}: {
  epoca: EpocaEditorial;
  folio?: number;
  children?: ReactNode;
}) {
  return (
    <section id={`epoca-${epoca.id}`} className="mt-14 scroll-mt-24 first:mt-0">
      <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-(--sim-rubrica)">
        {folio != null && ROMANOS[folio - 1] ? `Folio ${ROMANOS[folio - 1]} · ` : ""}
        Días {epoca.dias[0]}–{epoca.dias[1]}
      </span>
      <h2 className="mt-1 sim-display text-2xl font-semibold text-(--sim-ink) md:text-3xl">{epoca.titulo}</h2>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
        {epoca.resumen}
      </p>
      {children}
    </section>
  );
}

// ── Evento curado de la cronología ────────────────────────────────────
export function EventoItem({
  evento,
  personajeNombre,
}: {
  evento: EventoEditorial;
  personajeNombre?: string;
}) {
  const tipo = EVENTO_TIPOS[evento.tipo];
  return (
    <li className="relative border-l border-(--sim-rule) pl-5 pb-6 last:pb-0">
      <span
        aria-hidden="true"
        className="absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full"
        style={{ background: tipo.color }}
      />
      <div className="flex flex-wrap items-center gap-2 font-sans text-xs text-(--sim-ink-faint)">
        <span className="tabular-nums font-medium text-(--sim-ink-soft)">Día {evento.dia}</span>
        <span
          className="inline-flex items-center rounded-full px-2 py-0.5 font-medium"
          style={{ background: `${tipo.color}1a`, color: tipo.color, border: `1px solid ${tipo.color}33` }}
        >
          {tipo.label}
        </span>
      </div>

      {(evento.forma || personajeNombre) && (
        <div className="mt-1.5 flex flex-wrap items-baseline gap-x-2 gap-y-1">
          {evento.forma && (
            <Link
              href="/simulador/neologisms"
              className="sim-display text-lg font-semibold text-(--sim-fuego) hover:underline"
            >
              {evento.forma}
            </Link>
          )}
          {personajeNombre && evento.personaje && (
            <Link
              href={`/simulador/personajes/${evento.personaje}`}
              className="inline-flex items-center gap-1.5 font-sans text-sm text-(--sim-ink-soft) transition-colors hover:text-(--sim-ink)"
            >
              <Avatar name={personajeNombre} size={20} />
              {personajeNombre}
            </Link>
          )}
        </div>
      )}

      {evento.nota && (
        <p className="mt-1.5 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{evento.nota}</p>
      )}
    </li>
  );
}

// ── Datos embebidos en el flujo del texto (no un grid aparte) ─────────
// La capa digital del cronista: el instrumento que mide habla en monospace.
export function DataAside({
  items,
}: {
  items: { label: string; value: ReactNode; sub?: string }[];
}) {
  return (
    <aside className="my-8 flex flex-wrap gap-x-10 gap-y-4 border-y border-(--sim-rule) py-4">
      {items.map((it) => (
        <div key={it.label}>
          <span className="sim-mono block text-[0.65rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-faint)">
            {it.label}
          </span>
          <span className="sim-mono mt-1 block text-xl font-semibold leading-none text-(--sim-ink)">
            {it.value}
          </span>
          {it.sub && <span className="mt-1 block font-sans text-xs text-(--sim-ink-faint)">{it.sub}</span>}
        </div>
      ))}
    </aside>
  );
}

// ── Asterismo: separador de secciones del manuscrito ──────────────────
export function Asterismo() {
  return (
    <div aria-hidden="true" className="my-12 text-center font-serif text-lg tracking-[0.5em] text-(--sim-ink-faint)">
      ⁂
    </div>
  );
}
