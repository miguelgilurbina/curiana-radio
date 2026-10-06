import type { CSSProperties } from "react";

// La escala de sintonía del shell 1a «El dial»: marcas de 1px cada 14px en el
// filete fuerte y, si se pide, la aguja de 2px en el acento. Es decoración: la
// aguja que marca dónde estás vive en la nav (CabeceraNoche).
export default function EscalaDial({
  alto,
  aguja,
  paso = 14,
  className = "",
}: {
  alto: number;
  /** posición de la aguja, en % del ancho */
  aguja?: number;
  paso?: number;
  className?: string;
}) {
  const marcas = `repeating-linear-gradient(90deg, var(--noche-filete-fuerte) 0 1px, transparent 1px ${paso}px)`;
  const fondo =
    aguja === undefined
      ? marcas
      : `${marcas}, linear-gradient(var(--noche-acento), var(--noche-acento)) ${aguja}% 0 / 2px 100% no-repeat`;
  return <div aria-hidden="true" className={className} style={{ height: alto, background: fondo } as CSSProperties} />;
}
