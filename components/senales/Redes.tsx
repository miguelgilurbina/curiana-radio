import { REDES } from "@/lib/redes";

// Las redes de Curiana Radio en una fila. `clase` es la tinta completa del
// enlace según la superficie donde caiga (la noche por defecto; dentro de una
// señal, el dato de su piel). El usuario no cambia de caja: @curianaradio.
const NOCHE =
  "font-mono text-[0.72rem] uppercase tracking-[0.14em] text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-frecuencia-tinta)";

export default function Redes({ clase = NOCHE, className = "" }: { clase?: string; className?: string }) {
  return (
    <ul className={`m-0 flex list-none flex-wrap items-center gap-x-6 gap-y-2 p-0 ${className}`}>
      {REDES.map((r) => (
        <li key={r.nombre}>
          <a href={r.url} target="_blank" rel="noopener noreferrer" className={clase}>
            {r.nombre} · <span className="normal-case">{r.usuario}</span>
          </a>
        </li>
      ))}
    </ul>
  );
}
