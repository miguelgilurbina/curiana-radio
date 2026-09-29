import type { CSSProperties } from "react";

/**
 * El monograma jA. Monocromo en reposo y solo bajo el mouse recorre el dial
 * (reglas en `.jai-ja`, globals.css). Es decorativo: el nombre de la sección
 * siempre está escrito al lado, así que va oculto a lectores de pantalla.
 *
 * `tamano` acepta cualquier longitud CSS (112, "clamp(96px,14vw,168px)",
 * "100%"). Para que gire con el hover de un contenedor, ponle
 * `jai-ja-gatillo` al contenedor.
 */
export default function JA({
  tamano,
  className = "",
  style,
}: {
  tamano: number | string;
  className?: string;
  style?: CSSProperties;
}) {
  return (
    <span
      aria-hidden
      className={`jai-ja ${className}`}
      style={{ width: tamano, ...style }}
    />
  );
}
