// La etiqueta epistémica: cómo sabemos cada palabra. Es la marca de la casa
// y se pinta igual en todos los niveles — el índice, la ficha, el wiki, el
// archivo de voces retiradas. Color (tokens --capa-*) + glifo + palabra: el
// glifo va de lleno a vacío, de lo documentado a lo conjeturado, para que la
// etiqueta no dependa sólo del color.
import { CAPA, type CapaEpistemica } from "@/lib/sim-theme";

export function CapaGlifo({ capa, size = 12 }: { capa: CapaEpistemica; size?: number }) {
  const color = CAPA[capa].color;
  return (
    <svg
      aria-hidden="true"
      width={size}
      height={size}
      viewBox="0 0 12 12"
      className="inline-block shrink-0 align-[-0.1em]"
    >
      {capa === "atestiguado" && <circle cx="6" cy="6" r="5.25" fill={color} />}
      {capa === "reconstruido" && (
        <>
          <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" />
          <path d="M6 1.25 A4.75 4.75 0 0 0 6 10.75 Z" fill={color} />
        </>
      )}
      {capa === "retroabstraido" && (
        <>
          <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" />
          <circle cx="6" cy="6" r="2" fill={color} />
        </>
      )}
      {capa === "hipotetico" && (
        <circle cx="6" cy="6" r="4.75" fill="none" stroke={color} strokeWidth="1.5" strokeDasharray="2.2 1.5" />
      )}
    </svg>
  );
}

/** Glifo + palabra, en el color de la capa. `lg` para la cabecera de la ficha. */
export function CapaSello({ capa, tamano = "sm" }: { capa: CapaEpistemica; tamano?: "sm" | "lg" }) {
  const info = CAPA[capa];
  const grande = tamano === "lg";
  return (
    <span
      className={`inline-flex items-center gap-1.5 font-sans font-semibold uppercase ${
        grande ? "text-xs tracking-[0.16em]" : "text-[0.65rem] tracking-[0.12em]"
      }`}
      style={{ color: info.color }}
    >
      <CapaGlifo capa={capa} size={grande ? 14 : 10} />
      {info.label}
    </span>
  );
}
