"use client";

import { useSyncExternalStore } from "react";
import { alCambiarLuz, elegirLuz, luzElegida, opuesta, type Luz } from "@/lib/luz";
import { medir } from "@/lib/analitica";

// El interruptor de luz (design_handoff_senales_luces §2): un solo botón que
// alterna, con las dos luces a la vista. La activa va primero, en el color del
// texto y subrayada; la otra, en el secundario. Los glifos llevan U+FE0E para
// que iOS no los pinte como emoji. Objetivo táctil de 44px. Sólo sale si la
// piel tiene su otra luz diseñada. La elección vale para todo el sitio. Cada
// cambio se cuenta (`luz`, MEDICION.md): saber si la función se usa.

const GLIFO: Record<Luz, string> = { claro: "☀︎", oscuro: "☾︎" };
const rotulo = (l: Luz) => `[ ${GLIFO[l]} ${l} ]`;

export default function InterruptorLuz({
  nativo,
  alterno,
  activo,
  className = "",
}: {
  nativo: Luz;
  alterno: boolean;
  /** el color de la luz activa (el texto de donde cae); la otra hereda el secundario */
  activo: string;
  className?: string;
}) {
  // en el servidor no hay elección: se pinta la luz nativa
  const elegida = useSyncExternalStore(alCambiarLuz, luzElegida, () => null);
  if (!alterno) return null;

  const actual = elegida ?? nativo;
  const otra = opuesta(actual);
  return (
    <button
      type="button"
      onClick={() => {
        elegirLuz(otra);
        medir("luz", { luz: otra });
      }}
      aria-pressed={actual === "claro"}
      aria-label={`Luz ${actual}. Cambiar a ${otra}`}
      className={`flex min-h-11 cursor-pointer items-center gap-2 ${className}`}
    >
      <span aria-hidden="true" className={`whitespace-nowrap border-b border-current pb-0.5 ${activo}`}>
        {rotulo(actual)}
      </span>
      <span aria-hidden="true">/</span>
      <span aria-hidden="true" className="whitespace-nowrap">
        {rotulo(otra)}
      </span>
    </button>
  );
}
