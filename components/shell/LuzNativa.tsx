"use client";

import { useSyncExternalStore } from "react";
import { alCambiarLuz, luzElegida, olvidarLuz } from "@/lib/luz";

// «Volver a la luz de cada sección» (design_handoff_senales_luces §1): un
// enlace discreto en el pie que borra la elección del lector. Sólo sale si
// hay una elección que borrar.
export default function LuzNativa({ className = "" }: { className?: string }) {
  const elegida = useSyncExternalStore(alCambiarLuz, luzElegida, () => null);
  if (!elegida) return null;
  return (
    <button type="button" onClick={olvidarLuz} className={`cursor-pointer text-left ${className}`}>
      [ volver a la luz de cada sección ]
    </button>
  );
}
