"use client";

import Link from "next/link";
import ImagenObra from "./ImagenObra";
import { ETIQUETA_LICENCIA, type ObraGrid } from "@/types/galeria";

interface ObraCardProps {
  obra: ObraGrid;
  blobBase: string | null;
  /** Medidas calculadas por el motor del mosaico, en píxeles. */
  ancho: number;
  alto: number;
  /** Abre el lightbox. La pieza sigue siendo un <a> real a la ficha: el
   *  lightbox es mejora progresiva, no el único camino a la obra. */
  onAmpliar: () => void;
  /** Las primeras piezas cargan con prioridad; el resto, perezosas. */
  prioridad?: boolean;
}

export default function ObraCard({
  obra,
  blobBase,
  ancho,
  alto,
  onAmpliar,
  prioridad = false,
}: ObraCardProps) {
  return (
    <Link
      href={`/galeria/${obra.slug}`}
      onClick={(e) => {
        // Respetar ctrl/cmd/click medio: eso es "ábrelo en otra pestaña",
        // no "ampliá aquí".
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        onAmpliar();
      }}
      style={{ width: ancho, height: alto, backgroundColor: obra.color }}
      className="group relative block shrink-0 overflow-hidden focus-visible:z-10"
    >
      <ImagenObra
        obra={obra}
        blobBase={blobBase}
        prioridad={prioridad}
        // El motor ya sabe cuántos píxeles ocupa la pieza: decírselo evita que
        // el navegador baje una variante mayor de la necesaria.
        sizes={`${Math.ceil(ancho)}px`}
        className="h-full w-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.04]"
      />

      {/* Rótulo. Aparece al pasar por encima o al enfocar con teclado; en
          pantallas táctiles no hay hover, así que ahí vive siempre visible. */}
      <div className="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-deep-900/85 via-deep-900/45 to-transparent p-4 pt-10 opacity-0 transition-opacity duration-300 group-hover:opacity-100 group-focus-visible:opacity-100 [@media(hover:none)]:opacity-100">
        <h3 className="line-clamp-2 font-serif text-base leading-tight text-white drop-shadow-sm">
          {obra.titulo}
        </h3>
        <p className="mt-1 font-sans text-[0.65rem] tracking-[0.15em] uppercase text-earth-200">
          {obra.estado === "pendiente"
            ? "Sin render"
            : ETIQUETA_LICENCIA[obra.licencia]}
        </p>
      </div>
    </Link>
  );
}
