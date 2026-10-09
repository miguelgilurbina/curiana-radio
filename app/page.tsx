import type { Metadata } from "next";
import IntroDisco from "@/components/intro/IntroDisco";
import { haySenales } from "@/lib/senales";
import { metadatos, SITIO } from "@/lib/seo";

export const metadata: Metadata = metadatos({
  titulo: `${SITIO.nombre} - ${SITIO.lema}`,
  descripcion: SITIO.descripcion,
  ruta: "/",
});

// La puerta de la radio: la intro El Disco. Una vez por sesión; quien ya
// sintonizó pasa directo a la landing (/inicio). BRAND_MVP.md §9.
export default function Home() {
  return <IntroDisco haySenales={haySenales()} />;
}
