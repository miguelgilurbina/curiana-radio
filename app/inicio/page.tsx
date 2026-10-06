import type { Metadata } from "next";
import { getAllEditions } from "@/lib/content";
import { getSenales } from "@/lib/senales";
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

export const metadata: Metadata = {
  title: "Curiana Radio - 88.8 FM",
  description:
    "Emitimos desde una Paraguaná paralela, unos años después del Renacimiento de La Curiana. Una transmisión al mes: música, ensayo, una lengua que renace y el arte del camino.",
  alternates: { canonical: "/inicio" },
};

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
      {ultima && <UltimaTransmision edicion={ultima} />}
      <ArchivoSuscripcion ediciones={ediciones} />
    </div>
  );
}
