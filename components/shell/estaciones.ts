import { LIBERADA, type Seccion } from "@/lib/secciones";

// Las estaciones de la nav de la noche (shell 1a «El dial», SHELL.md). El
// diseño trae MANIFIESTO · JAI SOUNDS · KAKETIANA · GALERÍA · BUCHIBE ·
// ARCHIVO; Miguel sumó SEÑALES (2026-10-05). Sólo salen las que están al aire
// (lib/secciones.ts): hoy Galería, Buchibe y el archivo siguen en el taller.

export interface Estacion {
  id: string;
  /** si es una sección que se libera aparte */
  seccion?: Seccion;
  nombre: string;
  href: string | null;
}

export const ESTACIONES: Estacion[] = (
  [
    { id: "manifiesto", nombre: "Manifiesto", href: "/inicio#manifiesto" },
    { id: "senales", nombre: "Señales", href: "/senales" },
    { id: "jai-sounds", seccion: "jai-sounds", nombre: "JAI Sounds", href: "/jai-sounds" },
    { id: "kaketiana", seccion: "kaketiana", nombre: "Kaketiana", href: "/kaketiana" },
    { id: "galeria", seccion: "galeria", nombre: "Galería", href: "/galeria" },
    { id: "buchibe", seccion: "buchibe", nombre: "Buchibe", href: null },
    { id: "archivo", seccion: "archivo", nombre: "Archivo", href: "/archivo" },
  ] satisfies Estacion[]
).filter((e) => !e.seccion || LIBERADA[e.seccion]);

const SECCIONES = ["kaketiana", "jai-sounds", "galeria", "archivo"];

/** La estación donde está el lector. En una señal, la de su arista (SHELL.md
 *  «Comportamiento»); si no tiene arista, Señales. */
export function estacionActiva(ruta: string, aristaDeSenal: Record<string, string | null>): string | null {
  if (ruta === "/inicio") return "manifiesto";
  if (ruta === "/senales") return "senales";
  const senal = ruta.match(/^\/senales\/([^/]+)/);
  if (senal) return aristaDeSenal[senal[1]] ?? "senales";
  const seccion = SECCIONES.find((s) => ruta === `/${s}` || ruta.startsWith(`/${s}/`));
  return seccion ?? null;
}
