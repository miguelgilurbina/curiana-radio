import type { CSSProperties } from "react";
import {
  formatearDuracion,
  formatearDuracionLarga,
  type PlaylistResuelta,
} from "@/lib/jai-sounds-muestra/tipos";

/**
 * PROPUESTA A · "Estación" — la vista pública de una playlist.
 *
 * Tesis: la playlist no es una tabla, es un texto. Lo que distingue a JAI
 * Sounds de cualquier lista de Spotify es la nota curatorial, así que la
 * nota manda sobre la metadata: la pista con nota ocupa más espacio y las
 * demás se repliegan a una línea. Es lo contrario de un reproductor.
 */
export default function PropuestaEstacion({
  lista,
}: {
  lista: PlaylistResuelta;
}) {
  return (
    <article
      style={{ "--jai-hue": lista.mood?.hue ?? 40 } as CSSProperties}
      className="jai-estacion bg-(--jai-panel)"
    >
      <header className="px-6 py-8 md:px-10 border-b border-(--jai-rule)">
        <div className="flex items-baseline gap-4">
          <span className="font-(family-name:--jai-mono) text-sm tabular-nums text-(--jai-senal)">
            {lista.mood?.frecuencia ?? "—"}
          </span>
          <span className="font-(family-name:--jai-mono) text-[0.65rem] uppercase tracking-[0.25em] text-(--jai-luz-faint)">
            {lista.mood?.nombre ?? "sin mood"}
          </span>
        </div>
        <h3 className="font-(family-name:--jai-display) text-3xl md:text-4xl mt-3">
          {lista.nombre}
        </h3>
        <p className="mt-3 max-w-reading text-(--jai-luz-soft)">
          {lista.descripcion}
        </p>
        <p className="mt-4 font-(family-name:--jai-mono) text-[0.7rem] tabular-nums text-(--jai-luz-faint)">
          {lista.pistas.length} pistas · {formatearDuracionLarga(lista.duracionTotalMs)}
        </p>
      </header>

      <ol>
        {lista.pistas.map((pista, i) => (
          <li
            key={pista.id}
            className={`px-6 md:px-10 border-b border-(--jai-rule) last:border-0 ${
              pista.nota ? "py-6" : "py-3"
            }`}
          >
            <div className="flex items-baseline gap-4">
              <span className="font-(family-name:--jai-mono) text-xs tabular-nums text-(--jai-luz-faint) w-6 shrink-0">
                {String(i + 1).padStart(2, "0")}
              </span>
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-baseline gap-x-3">
                  <span
                    className={
                      pista.destacado
                        ? "font-(family-name:--jai-display) text-xl text-(--jai-senal)"
                        : "text-(--jai-luz)"
                    }
                  >
                    {pista.nombre}
                  </span>
                  <span className="text-sm text-(--jai-luz-faint)">
                    {pista.artistasResueltos.map((a) => a.nombre).join(" · ")}
                  </span>
                </div>
                {pista.nota && (
                  <p className="mt-2 max-w-reading text-sm text-(--jai-luz-soft) border-l-2 border-(--jai-senal) pl-4">
                    {pista.nota}
                  </p>
                )}
              </div>
              <span className="font-(family-name:--jai-mono) text-xs tabular-nums text-(--jai-luz-faint) shrink-0">
                {formatearDuracion(pista.duracion_ms)}
              </span>
            </div>
          </li>
        ))}
      </ol>
    </article>
  );
}
