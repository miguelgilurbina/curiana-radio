import { srcSetDe, urlVariante, type ObraGrid } from "@/types/galeria";
import PlaceholderTile from "./PlaceholderTile";

/**
 * La imagen de una obra, servida como archivo plano desde Vercel Blob.
 *
 * Es un `<img>` a pelo y no `next/image` a propósito. La escalera de anchos ya
 * está generada en la ingesta, así que no hace falta que nada la produzca al
 * vuelo: `/_next/image` factura una transformación por cada fallo de caché y
 * hace esperar al primer visitante de cada variante. Aquí el navegador elige
 * del `srcset` y el archivo sale del CDN tal cual.
 *
 * El hueco se reserva con `aspect-ratio` y se pinta del color dominante, así
 * que el mosaico no se mueve mientras cargan las piezas.
 */

interface ImagenObraProps {
  obra: ObraGrid;
  blobBase: string | null;
  /** Qué ancho ocupará la pieza. Sin esto el navegador asume 100vw. */
  sizes: string;
  /** La primera pantalla carga con prisa; el resto, en diferido. */
  prioridad?: boolean;
  className?: string;
}

export default function ImagenObra({
  obra,
  blobBase,
  sizes,
  prioridad = false,
  className = "",
}: ImagenObraProps) {
  const mayor = obra.anchos[obra.anchos.length - 1];
  const src = mayor ? urlVariante(blobBase, obra.slug, mayor) : null;

  if (!src) {
    return <PlaceholderTile slug={obra.slug} conRotulo={false} className={className} />;
  }

  return (
    /* El <img> es deliberado, no un descuido. La regla de Next asume que hay
       que optimizar al vuelo, pero la escalera ya está generada en la ingesta
       y se sirve desde el CDN. Cambiarlo por <Image /> reintroduciría justo el
       coste por transformación y la espera del primer visitante que evitamos.
       Ver GALERIA.md → «Por qué NO usamos la optimización de imágenes». */
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={src}
      srcSet={srcSetDe(blobBase, obra)}
      sizes={sizes}
      alt={obra.alt}
      width={obra.w ?? undefined}
      height={obra.h ?? undefined}
      loading={prioridad ? "eager" : "lazy"}
      // `high` en la primera pantalla adelanta estas peticiones a las de la
      // cola normal; `auto` deja que el navegador decida en el resto.
      fetchPriority={prioridad ? "high" : "auto"}
      decoding="async"
      style={{ backgroundColor: obra.color }}
      className={className}
    />
  );
}
