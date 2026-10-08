import type { Metadata, Viewport } from "next";
import { Archivo_Black, Fraunces, Inter, Lora } from "next/font/google";
import "./globals.css";
import ShellRadio from "@/components/layout/ShellRadio";
import JsonLd from "@/components/seo/JsonLd";
import { jsonLdSitio, SITIO, TARJETA_RADIO } from "@/lib/seo";
import Analitica from "@/components/analitica/Analitica";
import CabeceraNoche from "@/components/shell/CabeceraNoche";
import PieNoche from "@/components/shell/PieNoche";
import { getAllEditions } from "@/lib/content";
import { getSenales, haySenales } from "@/lib/senales";
import { SCRIPT_LUZ } from "@/lib/luz";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const lora = Lora({
  subsets: ["latin"],
  variable: "--font-lora",
  display: "swap",
});

// Display editorial del simulador (titulares del tema cronista); el resto
// de la radio no la usa. Pedimos los ejes variables SOFT y WONK (no vienen
// por defecto) para fijar una configuración firma en .sim-display: WONK 1
// activa las formas irregulares de estilo antiguo de Fraunces — lo que hace
// que la display se sienta propia y no la instancia por defecto del CDN.
// next/font ya self-hostea el archivo (sin request en runtime a Google).
const fraunces = Fraunces({
  subsets: ["latin"],
  axes: ["SOFT", "WONK"],
  variable: "--font-fraunces",
  display: "swap",
});

// "Type 3c": la voz de cartel del sistema — Archivo Black comprimida por
// transform (ver .cartel en globals.css y BRAND_MVP.md §2.1). Solo tiene
// peso 400; la compresión la pone el CSS, no la fuente.
const archivoBlack = Archivo_Black({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-archivo-black",
  display: "swap",
});

// La metadata base del sitio. Cada página declara la suya completa con
// metadatos() (lib/seo.ts); esto es el respaldo de lo que no la declare. Sin
// canonical aquí a propósito: se heredaría y toda página diría ser la portada.
export const metadata: Metadata = {
  metadataBase: new URL(SITIO.url),
  title: `${SITIO.nombre} - ${SITIO.lema}`,
  description: SITIO.descripcion,
  applicationName: SITIO.nombre,
  openGraph: {
    title: `${SITIO.nombre} · ${SITIO.lema}`,
    description: SITIO.bajada,
    siteName: SITIO.nombre,
    locale: SITIO.locale,
    type: "website",
    images: [TARJETA_RADIO],
  },
  twitter: { card: "summary_large_image" },
  // Favicon "la noche": espiral hueso sobre deep-900 (BRAND_MVP.md §8.1).
  // Los archivos viven en public/; no hay app/favicon.ico que los pise.
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon-32x32.png", type: "image/png", sizes: "32x32" },
      { url: "/favicon-16x16.png", type: "image/png", sizes: "16x16" },
    ],
    apple: { url: "/apple-touch-icon.png", sizes: "180x180" },
  },
  manifest: "/site.webmanifest",
};

export const viewport: Viewport = {
  themeColor: "#0F1621",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // lo que el shell de la noche necesita saber: la última edición (para
  // «sintonizar ahora»), la arista de cada señal (la aguja marca la estación
  // de la arista cuando se lee una señal) y si hay señales que anunciar (sin
  // ninguna, Señales no sale en la cabecera ni en el pie)
  const ultima = (await getAllEditions())[0];
  const edicion = { numero: String(ultima?.number ?? "01"), slug: ultima?.slug ?? "01" };
  const aristaDeSenal = Object.fromEntries(getSenales().map((s) => [s.slug, s.aristas[0] ?? null]));
  const conSenales = haySenales();

  return (
    // suppressHydrationWarning: SCRIPT_LUZ pone data-luz en <html> antes de
    // hidratar (la luz que eligió el lector, lib/luz.ts); no es un desajuste.
    <html
      lang="es"
      className={`${inter.variable} ${lora.variable} ${fraunces.variable} ${archivoBlack.variable}`}
      suppressHydrationWarning
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: SCRIPT_LUZ }} />
      </head>
      <body className="font-sans antialiased">
        <JsonLd datos={jsonLdSitio()} />
        <ShellRadio
          cabecera={<CabeceraNoche edicion={edicion} aristaDeSenal={aristaDeSenal} haySenales={conSenales} />}
          pie={<PieNoche edicion={edicion} haySenales={conSenales} />}
        >
          {children}
        </ShellRadio>
        <Analitica />
      </body>
    </html>
  );
}
