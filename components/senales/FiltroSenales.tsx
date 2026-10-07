"use client";

import { useState, type CSSProperties } from "react";
import { ARISTAS, type Arista, type SenalResumen } from "@/lib/senales-comun";
import FilaSenal from "./FilaSenal";

// El índice de Señales con su filtro (design_handoff_senales_luces): Todas ·
// la radio · Kaketiana · JAI Sounds · Galería · Buchibe, cada uno con el sello
// de su arista. Botones mono en mayúsculas, 36px de alto, radio de 2px; el
// activo sobre la placa con borde de texto, los demás con el filete y la
// tinta del acento al pasar. Mismo paradigma que las pestañas del sitio:
// botones con su estado y aria-pressed.
type Filtro = "todas" | "radio" | Arista;

const OPCIONES: { id: Filtro; nombre: string }[] = [
  { id: "todas", nombre: "Todas" },
  { id: "radio", nombre: "La radio" },
  // sólo las aristas al aire (lib/secciones.ts)
  ...(Object.keys(ARISTAS) as Arista[]).filter((a) => ARISTAS[a].liberada).map((a) => ({ id: a, nombre: ARISTAS[a].corto })),
];

export default function FiltroSenales({ senales }: { senales: SenalResumen[] }) {
  const [filtro, setFiltro] = useState<Filtro>("todas");

  const visibles = senales.filter((s) =>
    filtro === "todas" ? true : filtro === "radio" ? !s.aristas.length : s.aristas.includes(filtro),
  );
  const nombre = OPCIONES.find((o) => o.id === filtro)?.nombre;

  return (
    <div className="flex flex-col gap-7">
      <div role="group" aria-label="Filtrar por arista" className="flex flex-wrap gap-2">
        {OPCIONES.map((o) => (
          <button
            key={o.id}
            type="button"
            aria-pressed={filtro === o.id}
            onClick={() => setFiltro(o.id)}
            className={`flex min-h-9 cursor-pointer items-center gap-2 rounded-[2px] border px-3.5 font-mono text-[0.6875rem] tracking-[0.16em] whitespace-nowrap text-(--e-texto) uppercase transition-colors duration-300 ${
              filtro === o.id
                ? "border-(--e-texto) bg-(--e-placa)"
                : "border-(--e-filete) hover:border-(--noche-frecuencia-tinta)"
            }`}
          >
            {o.id !== "todas" && (
              <i
                aria-hidden="true"
                className="block h-[7px] w-[7px]"
                style={{ background: `var(--sello-${o.id})` } as CSSProperties}
              />
            )}
            {o.nombre}
          </button>
        ))}
      </div>
      <div aria-live="polite" className="flex flex-col">
        {visibles.length ? (
          visibles.map((s) => <FilaSenal key={s.slug} senal={s} />)
        ) : (
          <p className="m-0 border-t border-(--e-filete) py-5 font-serif text-base italic text-(--e-texto-2)">
            Todavía no hay señales en {filtro === "radio" ? "la radio" : nombre}.
          </p>
        )}
      </div>
    </div>
  );
}
