import type { Metadata } from "next";
import { SPOTIFY_SHOW } from "@/components/jai-sounds/estilos";
import { PORTAFOLIO, REDES } from "@/lib/redes";

// ── La ficha del sitio para buscadores, redes y agentes ───────────────
// Una sola fuente para lo que el sitio dice de sí mismo: la metadata de cada
// página, los datos estructurados (JSON-LD), el sitemap y /llms.txt leen de
// aquí. Las descripciones son el copy de la casa, no SEO de relleno.

export const SITIO = {
  nombre: "Curiana Radio",
  url: "https://curianaradio.com",
  locale: "es_VE",
  idioma: "es",
  lema: "88.8 FM",
  // El copy de la casa (layout de #256, 2026-10-06): la larga para buscadores,
  // la bajada para redes y tarjetas.
  descripcion:
    "Una radio del futuro que se sintoniza desde acá. Kaketiana, el mundo y la lengua de los caquetíos; JAI Sounds, la curaduría musical; y Señales, lo que escribe su creador.",
  bajada: "Una radio del futuro que se sintoniza desde acá: Kaketiana, JAI Sounds y Señales.",
  repo: "https://github.com/miguelgilurbina/curiana-radio",
} as const;

// Los perfiles del proyecto (schema.org sameAs): las redes de lib/redes.ts,
// el podcast y el repo.
export const PERFILES = [...REDES.map((r) => r.url), `https://open.spotify.com/show/${SPOTIFY_SHOW}`, SITIO.repo];

export function urlAbsoluta(ruta: string): string {
  return ruta.startsWith("http") ? ruta : `${SITIO.url}${ruta === "/" ? "" : ruta}`;
}

/** Recorta en el último espacio antes de `max` y cierra con «…». Para las
 *  descripciones: Google corta hacia los 155 caracteres y las redes antes. */
export function recortar(texto: string, max = 155): string {
  const limpio = texto.replace(/\s+/g, " ").trim();
  if (limpio.length <= max) return limpio;
  const corte = limpio.slice(0, max - 1);
  const espacio = corte.lastIndexOf(" ");
  return `${(espacio > max * 0.6 ? corte.slice(0, espacio) : corte).replace(/[\s,;:.—–-]+$/, "")}…`;
}

interface Imagen {
  url: string;
  alt: string;
  width?: number;
  height?: number;
}

interface OpcionesMetadatos {
  titulo: string;
  descripcion: string;
  /** Ruta canónica de la página, empezando en «/». */
  ruta: string;
  /** La tarjeta para redes; por omisión la de la radio. */
  imagen?: Imagen;
  /** Título para redes si difiere del <title> (sin el sufijo del sitio). */
  tituloSocial?: string;
  tipo?: "website" | "article";
  publicado?: string;
  noIndex?: boolean;
}

/** Una tarjeta de /og (1200×630, ver lib/og). */
export function tarjeta(clave: string, alt: string): Imagen {
  return { url: `/og/${clave}`, alt, width: 1200, height: 630 };
}

export const TARJETA_RADIO = tarjeta("curiana", "Curiana Radio · 88.8 FM — la espiral sobre la noche");
export const TARJETA_JAI = tarjeta("jai-sounds", "JAI Sounds, la curaduría musical de Curiana Radio");

/**
 * La metadata completa de una página. Existe porque Next fusiona openGraph
 * por reemplazo, no campo a campo: una página que declara su openGraph pierde
 * la imagen y el siteName del layout, y una que no lo declara se comparte con
 * el título de la portada. Aquí cada página declara todo, siempre.
 */
export function metadatos({
  titulo,
  descripcion,
  ruta,
  imagen = TARJETA_RADIO,
  tituloSocial,
  tipo = "website",
  publicado,
  noIndex,
}: OpcionesMetadatos): Metadata {
  const description = recortar(descripcion);
  return {
    title: titulo,
    description,
    alternates: { canonical: ruta },
    openGraph: {
      title: tituloSocial ?? titulo,
      description,
      url: ruta,
      siteName: SITIO.nombre,
      locale: SITIO.locale,
      type: tipo,
      ...(tipo === "article" && publicado ? { publishedTime: publicado } : {}),
      images: [imagen],
    },
    ...(noIndex ? { robots: { index: false, follow: true } } : {}),
  };
}

// ── Datos estructurados (schema.org) ──────────────────────────────────

export const ID_ORGANIZACION = `${SITIO.url}/#organizacion`;
export const ID_SITIO = `${SITIO.url}/#sitio`;

/** La radio como entidad: lo que Google y los agentes usan para saber quién
 *  publica. Va en el layout raíz, una vez por página. */
export function jsonLdSitio() {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": ID_ORGANIZACION,
        name: SITIO.nombre,
        url: SITIO.url,
        logo: urlAbsoluta("/icon-512.png"),
        description: SITIO.descripcion,
        sameAs: PERFILES,
        // «Quién transmite» (/sobre): el laboratorio creativo de su creador
        founder: { "@type": "Person", name: "Miguel Gil Urbina", url: PORTAFOLIO.url },
      },
      {
        "@type": "WebSite",
        "@id": ID_SITIO,
        name: SITIO.nombre,
        alternateName: `${SITIO.nombre} ${SITIO.lema}`,
        url: SITIO.url,
        inLanguage: SITIO.idioma,
        publisher: { "@id": ID_ORGANIZACION },
      },
    ],
  };
}

/** La miga de pan como BreadcrumbList: [nombre, ruta] desde la sección. */
export function jsonLdMigas(migas: [string, string][]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: migas.map(([name, ruta], i) => ({
      "@type": "ListItem",
      position: i + 1,
      name,
      item: urlAbsoluta(ruta),
    })),
  };
}
