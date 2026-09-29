import type { CSSProperties } from "react";
import JA from "./JA";

/**
 * La placa de estación (manual de marca, pág. 07): cuadrada, a escuadra,
 * filete de 3px a la izquierda en la señal, el monograma al centro y el
 * nombre en Fraunces abajo. El matiz no viene de la playlist sino de su
 * turno en el dial: `i` de `n`, girado por la semilla de la sesión.
 */
export default function EstacionCard({
  numero,
  nombre,
  descripcion,
  dato,
  marca,
  portada,
  i,
  sector,
  activa,
  onSintonizar,
}: {
  numero: string;
  nombre: string;
  descripcion?: string;
  /** La línea mono de abajo: "280 pistas". */
  dato: string;
  /** Rótulo en la esquina de la placa, en la señal: "edición #01". */
  marca?: string;
  portada: string | null;
  i: number;
  sector: number;
  activa: boolean;
  onSintonizar: () => void;
}) {
  return (
    <li className="min-w-0">
      <button
        type="button"
        aria-pressed={activa}
        onClick={onSintonizar}
        style={{ "--jai-i": i, "--jai-sector": sector } as CSSProperties}
        className={`jai-estacion jai-ja-gatillo group flex h-full w-full flex-col cursor-pointer bg-(--jai-panel) text-left outline-3 outline-offset-0 transition-[outline-color] duration-300 focus-visible:outline-(--jai-luz) ${
          activa ? "outline-(--jai-senal)" : "outline-transparent"
        }`}
      >
        <span className="relative block aspect-square overflow-hidden bg-(--jai-senal-tenue)">
          {portada ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={portada}
              alt=""
              className="absolute inset-0 h-full w-full object-cover"
            />
          ) : (
            <JA tamano="64%" className="absolute left-[18%] top-[18%]" />
          )}
          <span
            aria-hidden
            className="absolute inset-y-0 left-0 w-[3px] bg-(--jai-senal) opacity-60 transition-opacity duration-300 group-hover:opacity-100 group-aria-pressed:opacity-100"
          />
          <span className="jai-dato absolute left-4 top-3 text-[10px] text-(--jai-senal)">
            {numero}
          </span>
          {marca ? (
            <span className="jai-dato absolute right-3 top-3 text-[10px] text-(--jai-senal)">
              {marca}
            </span>
          ) : null}
        </span>
        <span className="flex flex-1 flex-col gap-2 p-4">
          <span className="jai-titulo text-lg leading-[1.1] text-(--jai-luz) sm:text-xl">
            {nombre}
          </span>
          {descripcion ? (
            <span className="text-sm leading-relaxed text-(--jai-luz-soft)">
              {descripcion}
            </span>
          ) : null}
          <span className="jai-dato text-[10px] tabular-nums text-(--jai-luz-faint)">
            {dato}
          </span>
        </span>
      </button>
    </li>
  );
}
