// Primitivas de la wiki narrativa: la columna de lectura del simulador.
// Complementan a ui.tsx (que sigue siendo la capa de tarjetas/badges);
// estas piezas arman el flujo de texto: épocas, eventos, datos embebidos.
import type { ReactNode } from "react";
import Link from "next/link";
import type { EventoEditorial, EpocaEditorial } from "@/lib/editorial";
import { EVENTO_TIPOS } from "@/lib/sim-theme";
import { Avatar } from "@/components/simulador/ui";

// ── Sección de época (ancla de la cronología) ─────────────────────────
export function Epoca({ epoca, children }: { epoca: EpocaEditorial; children?: ReactNode }) {
  return (
    <section id={`epoca-${epoca.id}`} className="mt-14 scroll-mt-24 first:mt-0">
      <span className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-earth-600">
        Días {epoca.dias[0]}–{epoca.dias[1]}
      </span>
      <h2 className="mt-1 font-serif text-2xl font-semibold text-deep-900 md:text-3xl">{epoca.titulo}</h2>
      <p className="mt-3 max-w-reading font-sans text-[0.95rem] leading-relaxed text-earth-700">
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
    <li className="relative border-l border-earth-200 pl-5 pb-6 last:pb-0">
      <span
        aria-hidden="true"
        className="absolute -left-[4.5px] top-1.5 h-2 w-2 rounded-full"
        style={{ background: tipo.color }}
      />
      <div className="flex flex-wrap items-center gap-2 font-sans text-xs text-earth-500">
        <span className="tabular-nums font-medium text-earth-600">Día {evento.dia}</span>
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
              className="font-serif text-lg font-semibold text-frequency hover:underline"
            >
              {evento.forma}
            </Link>
          )}
          {personajeNombre && evento.personaje && (
            <Link
              href={`/simulador/personajes/${evento.personaje}`}
              className="inline-flex items-center gap-1.5 font-sans text-sm text-earth-600 transition-colors hover:text-deep-800"
            >
              <Avatar name={personajeNombre} size={20} />
              {personajeNombre}
            </Link>
          )}
        </div>
      )}

      {evento.nota && (
        <p className="mt-1.5 max-w-reading font-sans text-sm leading-relaxed text-earth-700">{evento.nota}</p>
      )}
    </li>
  );
}

// ── Datos embebidos en el flujo del texto (no un grid aparte) ─────────
export function DataAside({
  items,
}: {
  items: { label: string; value: ReactNode; sub?: string }[];
}) {
  return (
    <aside className="my-8 flex flex-wrap gap-x-10 gap-y-4 border-y border-earth-200/70 py-4">
      {items.map((it) => (
        <div key={it.label}>
          <span className="block font-sans text-[0.7rem] font-medium uppercase tracking-[0.18em] text-earth-600">
            {it.label}
          </span>
          <span className="mt-0.5 block font-serif text-2xl font-semibold leading-none text-deep-800">
            {it.value}
          </span>
          {it.sub && <span className="mt-1 block font-sans text-xs text-earth-500">{it.sub}</span>}
        </div>
      ))}
    </aside>
  );
}
