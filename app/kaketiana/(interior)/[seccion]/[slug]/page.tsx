import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getWikiPagina, getWikiParams } from "@/lib/wiki";
import type { SeccionWiki } from "@/types/wiki";
import ArticuloEnsayo from "@/components/kaketiana/ArticuloEnsayo";
import ArticuloReferencia from "@/components/kaketiana/ArticuloReferencia";

interface ArticuloProps {
  params: Promise<{ seccion: string; slug: string }>;
}

export async function generateStaticParams() {
  return getWikiParams();
}

export const dynamicParams = false;

function esSeccion(s: string): s is SeccionWiki {
  return s === "pueblo" || s === "lengua";
}

export async function generateMetadata({ params }: ArticuloProps): Promise<Metadata> {
  const { seccion, slug } = await params;
  if (!esSeccion(seccion)) return { title: "No encontrado | Curiana Radio" };
  const p = getWikiPagina(seccion, slug);
  if (!p) return { title: "No encontrado | Curiana Radio" };
  return {
    title: `${p.titulo} — Kaketiana | Curiana Radio`,
    description: p.resumen,
  };
}

export default async function ArticuloPage({ params }: ArticuloProps) {
  const { seccion, slug } = await params;
  if (!esSeccion(seccion)) notFound();
  const pagina = getWikiPagina(seccion, slug);
  if (!pagina) notFound();

  // Las dos vistas del manual de Kaketiana: `pueblo` es prosa larga con citas
  // de crónicas, el artículo de fondo (Vistas §02); `lengua` es obra de
  // consulta —una de cada cinco líneas es tabla—, a ancho completo y con las
  // tablas en fichas en el móvil (Vistas §03).
  return seccion === "pueblo" ? <ArticuloEnsayo pagina={pagina} /> : <ArticuloReferencia pagina={pagina} />;
}
