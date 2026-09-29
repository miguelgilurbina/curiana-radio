import type { ReactNode } from "react";
import { SHOW } from "./escrito";
import { CTA, SPOTIFY_SHOW } from "./estilos";

/**
 * El canal: el show «Curiana Radio» en Spotify, que es donde viven los
 * episodios de Descubriendo con Chocolate. Va con el embed oficial del
 * show — hoy muestra el show entero; una lista filtrada solo a Descubriendo
 * pediría la Web API (/shows/{id}/episodes) y filtrar por título. El alto es
 * 352 y no el 480 del diseño: el embed de un show no pasa de 352 y el resto
 * del marco quedaba vacío.
 *
 * Se pinta con los tokens del orbe: quien lo use tiene que estar dentro de
 * [data-descubriendo-theme="orbe"].
 */
export default function Canal({
  rotulo,
  titulo = "episodios",
  children,
}: {
  /** El rótulo mono de arriba; sin él, el bloque arranca en el título. */
  rotulo?: string;
  titulo?: string;
  /** Llamadas extra junto a «abrir en spotify». */
  children?: ReactNode;
}) {
  return (
    <div className="grid items-start gap-12 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
      <div className="flex flex-col gap-5">
        {rotulo ? (
          <span className="jai-dato text-[11px] text-(--orbe-meta)">{rotulo}</span>
        ) : null}
        <h2 className="jai-orbe text-[32px] leading-[1.1] text-(--orbe-texto)">
          {titulo}
        </h2>
        <p className="max-w-[44ch] text-base leading-[1.75] text-(--orbe-lavanda)">
          {SHOW}
        </p>
        <span className="jai-dato text-[11px] text-(--orbe-meta)">
          en spotify · show «curiana radio»
        </span>
        <div className="flex flex-wrap gap-3">
          <a
            href={`https://open.spotify.com/show/${SPOTIFY_SHOW}`}
            target="_blank"
            rel="noopener noreferrer"
            className={`${CTA} bg-(--orbe-lavanda) px-[22px] py-[14px] text-(--orbe-fondo) hover:bg-(--orbe-texto)`}
          >
            abrir en spotify →
          </a>
          {children}
        </div>
      </div>
      <div className="border border-(--orbe-filete) bg-(--orbe-panel) p-3">
        <iframe
          title="Curiana Radio en Spotify"
          src={`https://open.spotify.com/embed/show/${SPOTIFY_SHOW}?theme=0`}
          width="100%"
          height="352"
          allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
          loading="lazy"
          className="block border-0"
        />
      </div>
    </div>
  );
}
