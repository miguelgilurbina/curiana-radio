import type { Glosa } from "@/lib/glosas";

// La glosa del cronista: el eco de una palabra ATESTIGUADA (crónica real)
// en la lengua que la simulación produjo. Se lee como la anotación de un
// escriba posterior en el margen de un manuscrito — por eso el registro es
// distinto al del evento o la voz de Manaure: es la mano de otro, mirando
// desde afuera del relato.
export default function GlosaCronista({ glosa }: { glosa: Glosa }) {
  return (
    <aside className="my-5 flex gap-3 rounded-lg border border-(--sim-rubrica)/25 bg-(--sim-rubrica)/[0.05] px-4 py-3.5">
      <span aria-hidden="true" className="mt-0.5 shrink-0 font-serif text-lg leading-none text-(--sim-rubrica)/70">
        ❧
      </span>
      <div>
        <p className="font-sans text-[0.7rem] font-medium uppercase tracking-[0.14em] text-(--sim-rubrica)">
          Glosa del cronista · palabra atestiguada
        </p>
        <p className="mt-1.5 flex flex-wrap items-baseline gap-x-2">
          <span className="sim-display text-base font-semibold italic text-(--sim-ink)">
            {glosa.palabra_real}
          </span>
          <span className="font-sans text-sm text-(--sim-ink-soft)">«{glosa.significado_real}»</span>
        </p>
        <p className="mt-1.5 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
          {glosa.nota}
        </p>
        <p className="sim-mono mt-2 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
          {glosa.cita}
        </p>
      </div>
    </aside>
  );
}
