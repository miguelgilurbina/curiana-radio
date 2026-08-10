"use client";

import { useCallback, useMemo, useState } from "react";
import ObraCard from "./ObraCard";
import {
  alturaObjetivoPara,
  aspectoDeObra,
  componerFilas,
} from "@/lib/mosaico";
import type { ObraGrid } from "@/types/galeria";

/** Casi cero: las piezas se tocan y el conjunto se lee como un tejido. */
const GAP = 4;

/**
 * Ancho asumido al renderizar en servidor, donde no hay contenedor que medir:
 * max-w-7xl (1280) menos el padding lateral de la página. El HTML estático
 * sale ya maquetado —importa para SEO y para que no haya un hueco en blanco—
 * y al hidratar se remide contra el viewport real.
 */
const ANCHO_SSR = 1216;

/** Piezas que cargan con priority: aproximadamente la primera fila. */
const PIEZAS_PRIORITARIAS = 4;

/**
 * Cuántas piezas se pintan de entrada y cuántas se añaden por tanda.
 *
 * El catálogo entero viaja al cliente en el payload —son metadatos, unos
 * pocos KB comprimidos— pero pintarlo de golpe metería ~800 nodos con imagen
 * en el DOM y varios cientos de KB de HTML en la respuesta. Se pinta una
 * ventana y crece al bajar.
 */
const TANDA = 60;

interface MosaicoProps {
  obras: ObraGrid[];
  blobBase: string | null;
  onAmpliar: (indice: number) => void;
}

export default function Mosaico({ obras, blobBase, onAmpliar }: MosaicoProps) {
  const [ancho, setAncho] = useState(ANCHO_SSR);
  const [limite, setLimite] = useState(TANDA);

  /**
   * Medición por callback de ref, no por efecto: React la ejecuta durante el
   * commit, antes de pintar, así que la primera medida no depende de que el
   * navegador llegue a componer un frame. Importa — los callbacks de
   * ResizeObserver se entregan dentro del ciclo de render, y una pestaña que
   * aún no se ha mostrado no lo ejecuta: sin la medida síncrona el mosaico se
   * quedaría maquetado a ANCHO_SSR y desbordaría su contenedor.
   *
   * El observer sigue, pero solo para lo que viene después: cambios de ancho
   * sin cambio de viewport (barra de scroll que aparece, zoom, panel lateral).
   */
  const medirContenedor = useCallback((el: HTMLDivElement | null) => {
    if (!el) return;
    const medir = () => {
      const medido = el.getBoundingClientRect().width;
      if (medido > 0) setAncho(medido);
    };
    medir();
    const observador = new ResizeObserver(medir);
    observador.observe(el);
    return () => observador.disconnect();
  }, []);

  /** Centinela al pie: al asomarse, pide la siguiente tanda. */
  const observarPie = useCallback((el: HTMLDivElement | null) => {
    if (!el) return;
    const observador = new IntersectionObserver(
      (entradas) => {
        if (entradas.some((e) => e.isIntersecting)) {
          setLimite((l) => l + TANDA);
        }
      },
      // Margen generoso: la tanda siguiente se prepara antes de que el borde
      // llegue a la vista, así el scroll no se topa con un vacío.
      { rootMargin: "1200px 0px" }
    );
    observador.observe(el);
    return () => observador.disconnect();
  }, []);

  const pintadas = useMemo(() => obras.slice(0, limite), [obras, limite]);
  const quedan = obras.length - pintadas.length;

  const filas = useMemo(
    () =>
      componerFilas(pintadas, ancho, aspectoDeObra, {
        alturaObjetivo: alturaObjetivoPara(ancho),
        gap: GAP,
      }),
    [pintadas, ancho]
  );

  // El motor conserva el orden, así que un contador corrido basta para saber
  // a qué posición de `obras` corresponde cada pieza (lo que espera el lightbox).
  let indice = -1;

  return (
    <div>
      {/* overflow-hidden como red: entre el HTML servido a ANCHO_SSR y la
          primera medida, las filas pueden ser más anchas que el hueco real.
          Que eso se recorte un instante es aceptable; que empuje la página de
          lado, no. */}
      <div ref={medirContenedor} className="overflow-hidden">
        {filas.map((fila, i) => (
          <div
            key={i}
            className="flex"
            style={{
              gap: GAP,
              marginBottom: i === filas.length - 1 ? 0 : GAP,
            }}
          >
            {fila.celdas.map((celda) => {
              indice++;
              const posicion = indice;
              return (
                <ObraCard
                  key={celda.item.slug}
                  obra={celda.item}
                  blobBase={blobBase}
                  ancho={celda.ancho}
                  alto={celda.alto}
                  prioridad={posicion < PIEZAS_PRIORITARIAS}
                  onAmpliar={() => onAmpliar(posicion)}
                />
              );
            })}
          </div>
        ))}
      </div>

      {quedan > 0 && (
        <div ref={observarPie} className="mt-8 text-center">
          {/* Botón además del centinela: el scroll infinito a secas deja sin
              salida a quien navega con teclado, y funciona igual si el
              IntersectionObserver no llega a dispararse. */}
          <button
            type="button"
            onClick={() => setLimite((l) => l + TANDA)}
            className="border border-earth-300 px-5 py-2 font-sans text-sm text-earth-700 transition-colors hover:border-frequency hover:text-frequency"
          >
            Ver más ({quedan} {quedan === 1 ? "obra" : "obras"})
          </button>
        </div>
      )}
    </div>
  );
}
