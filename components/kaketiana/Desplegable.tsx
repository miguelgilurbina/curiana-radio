"use client";

import { useId, useState, type ReactNode } from "react";

// «Más hondo»: la forma de bajar de capa sin salir de la página. El lector ve
// lo esencial y decide si abre el detalle (Miguel, 2026-10-01: «darle la
// batuta al usuario para que pueda llegar lo más lejos en el rabbit hole como
// desee»). Mismo paradigma que las pestañas de SerieBrazosChart: un botón con
// su estado, aria-expanded y aria-controls, y la acción en registro terminal
// del manual. Al abrir, el cuerpo amanece (kk-desplegar en globals.css).
export default function Desplegable({
  abrir,
  cerrar = "[ cerrar ↑ ]",
  children,
  className = "",
}: {
  /** El texto de la acción cerrada: «[ ver el dato ↓ ]». */
  abrir: string;
  cerrar?: string;
  children: ReactNode;
  className?: string;
}) {
  const [abierto, setAbierto] = useState(false);
  const id = useId();

  return (
    <div className={className}>
      <button
        type="button"
        aria-expanded={abierto}
        aria-controls={id}
        onClick={() => setAbierto((a) => !a)}
        className="kk-accion cursor-pointer text-left text-[0.7rem]"
      >
        {abierto ? cerrar : abrir}
      </button>
      <div id={id} hidden={!abierto} className="kk-desplegable-cuerpo mt-4">
        {children}
      </div>
    </div>
  );
}
