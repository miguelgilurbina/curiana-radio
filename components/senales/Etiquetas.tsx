import Link from "next/link";
import type { CSSProperties } from "react";
import { ARISTAS, type Arista } from "@/lib/senales-comun";

// Las aristas de una señal, en el registro del dato. Enlazan a su sección
// cuando la sección existe; sin arista, la señal es de «la radio».
//
// En las listas de la noche (índice, landing) cada arista lleva su sello: un
// cuadro con la tinta de su manual (--sello-* en globals.css), para que se
// sepa de qué arista es una señal antes de abrirla. Dentro de una señal no
// hace falta: la página entera ya va en la piel de su arista.

const SELLO = "inline-block h-[7px] w-[7px] shrink-0";
const NOCHE = "font-mono text-[0.68rem] uppercase tracking-[0.2em] text-(--noche-hueso-2)";

function Sello({ id }: { id: Arista | "radio" }) {
  return <span aria-hidden="true" className={SELLO} style={{ background: `var(--sello-${id})` } as CSSProperties} />;
}

export default function Etiquetas({
  aristas,
  enlazar = true,
  sello = false,
  clase = NOCHE,
  hover = "hover:text-(--noche-frecuencia-tinta)",
}: {
  aristas: readonly Arista[];
  enlazar?: boolean;
  sello?: boolean;
  /** la tinta del dato según la superficie (por defecto, la noche) */
  clase?: string;
  hover?: string;
}) {
  if (!aristas.length) {
    return (
      <span className={`inline-flex items-center gap-2 ${clase}`}>
        {sello && <Sello id="radio" />}
        La radio
      </span>
    );
  }
  return (
    <span className="flex flex-wrap gap-x-4 gap-y-1">
      {aristas.map((id) => {
        const { nombre, href, liberada } = ARISTAS[id];
        const contenido = (
          <>
            {sello && <Sello id={id} />}
            {nombre}
          </>
        );
        return enlazar && href && liberada ? (
          <Link
            key={id}
            href={href}
            className={`relative z-[1] inline-flex items-center gap-2 transition-colors duration-300 ${clase} ${hover}`}
          >
            {contenido}
          </Link>
        ) : (
          <span key={id} className={`inline-flex items-center gap-2 ${clase}`}>
            {contenido}
          </span>
        );
      })}
    </span>
  );
}
