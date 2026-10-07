import type { Metadata } from "next";
import { getAllEditions } from "@/lib/content";
import { getSenales } from "@/lib/senales";
import { LIBERADA } from "@/lib/secciones";
import HeroAristas from "@/components/landing/HeroAristas";
import {
  Aristas,
  ArchivoSuscripcion,
  Interludio,
  Manifiesto,
  QuienTransmite,
  Senales,
  UltimaTransmision,
} from "@/components/landing/Secciones";
import { metadatos, SITIO } from "@/lib/seo";

export const metadata: Metadata = metadatos({
  titulo: `${SITIO.nombre} - ${SITIO.lema}`,
  descripcion: SITIO.descripcion,
  ruta: "/inicio",
});

// La landing v1 · la noche: el marco que contiene todas las aristas. Llega
// después de la intro El Disco (/), pero también se entra directo: quien
// llega aquí ve el carrusel sin intro. BRAND_MVP.md §10. La cabecera y el pie
// son los comunes de la noche (shell 1a, §13), los pone ShellRadio.
export default async function Inicio() {
  const ediciones = await getAllEditions();
  const ultima = ediciones[0];
  const senales = getSenales({ limite: 3 });

  return (
    <div data-radio="noche" className="bg-(--noche-fondo) text-(--noche-hueso)">
      {/* la llegada desde la intro: amanece desde el negro del disco */}
      <div className="noche-velo" aria-hidden="true" />
      <HeroAristas edicion={{ numero: String(ultima?.number ?? "01"), slug: ultima?.slug ?? "01" }} />
      <Manifiesto />
      <QuienTransmite />
      <Senales senales={senales} />
      <Interludio />
      <Aristas />
      {/* La última edición y el archivo vuelven cuando se libere el archivo
          (lib/secciones.ts); la suscripción vive en el pie de la noche. */}
      {LIBERADA.archivo && ultima && <UltimaTransmision edicion={ultima} />}
      {LIBERADA.archivo && <ArchivoSuscripcion ediciones={ediciones} />}
    </div>
  );
}
