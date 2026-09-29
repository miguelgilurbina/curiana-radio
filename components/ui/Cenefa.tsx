import type { ReactNode } from "react";
import { ESPIRAL_TRAZO } from "@/lib/espiral-trazo";

// La cenefa: la espiral del isotipo repetida como guarda alrededor de una
// pieza (la portada de una edición, un cartel). Port del componente del
// design system: el trazo va como SVG en data-URI, así que no hay imagen
// extra que cargar.
interface CenefaProps {
  children: ReactNode;
  color?: string;
  /** lado de cada espiral y ancho de la guarda, en px */
  tamano?: number;
  lados?: "todos" | "horizontal" | "vertical";
  fondo?: string;
  opacidad?: number;
}

export default function Cenefa({
  children,
  color = "currentColor",
  tamano = 48,
  lados = "todos",
  fondo = "transparent",
  opacidad = 1,
}: CenefaProps) {
  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">` +
    `<path d="${ESPIRAL_TRAZO}" fill="none" stroke="${color}" stroke-width="12.4" stroke-linecap="round"/></svg>`;
  const banda = {
    position: "absolute" as const,
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svg)}")`,
    backgroundRepeat: "repeat",
    backgroundSize: `${tamano}px ${tamano}px`,
    opacity: opacidad,
    pointerEvents: "none" as const,
  };
  const horizontal = lados === "todos" || lados === "horizontal";
  const vertical = lados === "todos" || lados === "vertical";

  return (
    <div style={{ position: "relative", background: fondo, padding: tamano }}>
      {horizontal && <span aria-hidden="true" style={{ ...banda, top: 0, left: 0, right: 0, height: tamano }} />}
      {horizontal && <span aria-hidden="true" style={{ ...banda, bottom: 0, left: 0, right: 0, height: tamano }} />}
      {vertical && <span aria-hidden="true" style={{ ...banda, top: 0, bottom: 0, left: 0, width: tamano }} />}
      {vertical && <span aria-hidden="true" style={{ ...banda, top: 0, bottom: 0, right: 0, width: tamano }} />}
      <div style={{ position: "relative" }}>{children}</div>
    </div>
  );
}
