// Las estaciones de la nav de la noche (shell 1a «El dial», SHELL.md). El
// diseño trae MANIFIESTO · JAI SOUNDS · KAKETIANA · GALERÍA · BUCHIBE ·
// ARCHIVO; Miguel sumó SEÑALES (2026-10-05). Buchibe todavía no tiene
// sección: está en el dial, pero no se puede sintonizar.

export interface Estacion {
  id: string;
  nombre: string;
  href: string | null;
}

export const ESTACIONES: Estacion[] = [
  { id: "manifiesto", nombre: "Manifiesto", href: "/inicio#manifiesto" },
  { id: "senales", nombre: "Señales", href: "/senales" },
  { id: "jai-sounds", nombre: "JAI Sounds", href: "/jai-sounds" },
  { id: "kaketiana", nombre: "Kaketiana", href: "/kaketiana" },
  { id: "galeria", nombre: "Galería", href: "/galeria" },
  { id: "buchibe", nombre: "Buchibe", href: null },
  { id: "archivo", nombre: "Archivo", href: "/archivo" },
];

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
