import type { Metadata, Viewport } from "next";
import { Archivo_Black, Fraunces, Inter, Lora } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/layout/Navigation";
import Footer from "@/components/layout/Footer";
import ShellRadio from "@/components/layout/ShellRadio";
import JsonLd from "@/components/seo/JsonLd";
import { jsonLdSitio, SITIO, TARJETA_RADIO } from "@/lib/seo";
import Analitica from "@/components/analitica/Analitica";

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
    title: `${SITIO.nombre} - ${SITIO.lema}`,
    description: SITIO.descripcion,
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

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${inter.variable} ${lora.variable} ${fraunces.variable} ${archivoBlack.variable}`}>
      <body className="font-sans antialiased">
        <JsonLd datos={jsonLdSitio()} />
        <ShellRadio nav={<Navigation />} footer={<Footer />}>
          {children}
        </ShellRadio>
        <Analitica />
      </body>
    </html>
  );
}
