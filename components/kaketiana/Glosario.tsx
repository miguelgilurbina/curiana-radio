"use client";

import { useId, useState } from "react";
import type { ConceptoAbstract } from "@/lib/abstract";

// Los conceptos del experimento como glosario plegable: se ve el término y su
// lema; la explicación se abre al tocarlo. Antes eran ocho bloques abiertos a
// la vez (la página se sentía sobrecargada, Miguel 2026-10-01). Mismo
// paradigma que Desplegable: botón con estado y aria-expanded.
function Termino({ concepto, n }: { concepto: ConceptoAbstract; n: number }) {
  const [abierto, setAbierto] = useState(false);
  const id = useId();
  return (
    <li id={`concepto-${concepto.id}`} className="scroll-mt-24 border-t border-(--sim-rule)">
      <button
        type="button"
        aria-expanded={abierto}
        aria-controls={id}
        onClick={() => setAbierto((a) => !a)}
        className="group flex w-full items-baseline gap-3 py-3 text-left"
      >
        <span className="sim-mono text-xs tabular-nums text-(--sim-ink-soft)">{String(n).padStart(2, "0")}</span>
        <span className="flex-1">
          <span className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
            {concepto.termino}
          </span>
          <span className="ml-2 font-serif text-sm italic text-(--sim-fuego)">{concepto.lema}</span>
        </span>
        <span aria-hidden="true" className="sim-mono text-xs text-(--sim-rubrica)">
          {abierto ? "−" : "+"}
        </span>
      </button>
      <div id={id} hidden={!abierto} className="kk-desplegable-cuerpo pb-4 pl-7">
        <p className="max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">{concepto.cuerpo}</p>
        {concepto.dato && (
          <p className="sim-mono mt-3 border-l-2 border-(--sim-rubrica)/60 pl-3 text-xs leading-relaxed text-(--sim-ink-soft)">
            {concepto.dato}
          </p>
        )}
      </div>
    </li>
  );
}

export default function Glosario({ conceptos }: { conceptos: ConceptoAbstract[] }) {
  return (
    <ul className="border-b border-(--sim-rule)">
      {conceptos.map((c, i) => (
        <Termino key={c.id} concepto={c} n={i + 1} />
      ))}
    </ul>
  );
}
