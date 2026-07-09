import { Overline } from "@/components/simulador/ui";

// Masthead de revista: filete doble, nameplate en display, línea de edición.
// Habla en tokens --sim-*: sobre el pergamino es tinta parda; dentro del
// Acto I "laboratorio" se resuelve solo al registro oscuro del instrumento.
export default function Masthead() {
  return (
    <header className="mb-10">
      <div className="sim-double-rule" aria-hidden="true" />
      <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 py-3">
        <h1 className="sim-display text-4xl font-semibold tracking-tight text-(--sim-ink) md:text-5xl">
          Simulador Caquetío
        </h1>
        <Overline>Laboratorio lingüístico · 88.8 FM</Overline>
      </div>
      <div className="border-b border-(--sim-ink)" aria-hidden="true" />
      <p className="sim-mono mt-2 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
        Golfete de Coro · Siglos XIV–XV · Una crónica que se sigue escribiendo
      </p>
    </header>
  );
}
