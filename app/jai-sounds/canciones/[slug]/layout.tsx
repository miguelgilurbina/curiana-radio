import type { ReactNode } from "react";
import { notFound } from "next/navigation";
import { cancion } from "@/lib/jai-wiki";

// Si la canción no está en el dial, se dice ANTES de responder. El loading.tsx de
// esta carpeta (el esqueleto «sintonizando») envuelve sólo a la página: este
// layout corre fuera de él, así que un notFound() aquí llega como 404 de
// verdad. Desde la página llegaba tarde —la respuesta ya había salido con 200
// para pintar el esqueleto— y los buscadores veían un 200 «no está en el dial».
export default async function Layout({ children, params }: { children: ReactNode; params: Promise<{ slug: string }> }) {
  if (!cancion((await params).slug)) notFound();
  return children;
}
