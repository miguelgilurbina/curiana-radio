"use client";

import { useId, useState, type ReactNode } from "react";

// «Seguir leyendo» del Manifiesto: el resto del texto se abre en el lugar,
// sin salir de la landing. Mismo paradigma que Desplegable de Kaketiana: un
// botón con su estado, aria-expanded y aria-controls, en el registro del dato
// de la noche. Reemplaza al <details> nativo que tenía la sección (feedback
// de Miguel, 2026-10-01: el framework del proyecto, nada de HTML suelto). Al
// abrir, el botón baja debajo del texto para poder volver a cerrarlo.
export default function SeguirLeyendo({ children }: { children: ReactNode }) {
  const [abierto, setAbierto] = useState(false);
  const id = useId();

  return (
    <div>
      {/* entra con la misma animación que el Desplegable de Kaketiana */}
      <div id={id} hidden={!abierto} className="kk-desplegable-cuerpo">
        {children}
      </div>
      <button
        type="button"
        aria-expanded={abierto}
        aria-controls={id}
        onClick={() => setAbierto((a) => !a)}
        className={`cursor-pointer font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento) ${abierto ? "mt-6" : ""}`}
      >
        {abierto ? "LEER MENOS ↑" : "SEGUIR LEYENDO ↓"}
      </button>
    </div>
  );
}
