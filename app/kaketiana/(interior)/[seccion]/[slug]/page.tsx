import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getWikiGenerado, getWikiPagina, getWikiParams } from "@/lib/wiki";
import { ID_ORGANIZACION, jsonLdMigas, metadatos, recortar, tarjeta, urlAbsoluta } from "@/lib/seo";
import { SECCIONES_WIKI, type SeccionWiki, type WikiPagina } from "@/types/wiki";
import JsonLd from "@/components/seo/JsonLd";
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
  return metadatos({
    titulo: `${p.titulo} — Kaketiana | Curiana Radio`,
    tituloSocial: p.titulo,
    descripcion: p.resumen,
    ruta: `/kaketiana/${seccion}/${slug}`,
    tipo: "article",
    imagen: tarjeta(`kaketiana/${seccion}/${slug}`, p.titulo),
  });
}

/** El artículo para buscadores y agentes: qué pregunta, de quién, y sobre
 *  qué obras se sostiene (citation enlaza a la bibliografía, obra por obra). */
function jsonLdArticulo(seccion: SeccionWiki, p: WikiPagina) {
  const ruta = `/kaketiana/${seccion}/${p.slug}`;
  const generado = getWikiGenerado();
  return [
    {
      "@context": "https://schema.org",
      "@type": "Article",
      headline: p.titulo,
      description: recortar(p.resumen),
      url: urlAbsoluta(ruta),
      image: urlAbsoluta(`/og${ruta}`),
      inLanguage: "es",
      ...(generado ? { dateModified: generado } : {}),
      author: { "@id": ID_ORGANIZACION },
      publisher: { "@id": ID_ORGANIZACION },
      isPartOf: { "@type": "CreativeWork", name: "Kaketiana", url: urlAbsoluta("/kaketiana") },
      about: { "@type": "Thing", name: "Pueblo caquetío" },
      citation: p.fuentes.map((f) => ({
        "@type": "CreativeWork",
        name: f.titulo,
        url: urlAbsoluta(`/kaketiana/bibliografia#${f.slug}`),
      })),
    },
    jsonLdMigas([
      ["Kaketiana", "/kaketiana"],
      [SECCIONES_WIKI[seccion].label, `/kaketiana/${seccion}`],
      [p.titulo, ruta],
    ]),
  ];
}

export default async function ArticuloPage({ params }: ArticuloProps) {
  const { seccion, slug } = await params;
  if (!esSeccion(seccion)) notFound();
  const pagina = getWikiPagina(seccion, slug);
  if (!pagina) notFound();

  // Las dos vistas del manual de Kaketiana: `pueblo` es prosa larga con citas
  // de crónicas, el artículo de fondo (Vistas §02); `lengua` es obra de
  // consulta —una de cada cinco líneas es tabla—, a ancho completo y con las
  // tablas en fichas en el móvil (Vistas §03). Las dos llevan su JSON-LD.
  return (
    <>
      <JsonLd datos={jsonLdArticulo(seccion, pagina)} />
      {seccion === "pueblo" ? <ArticuloEnsayo pagina={pagina} /> : <ArticuloReferencia pagina={pagina} />}
    </>
  );
}
