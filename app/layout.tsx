import type { Metadata, Viewport } from "next";
import { Archivo_Black, Fraunces, Inter, Lora } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/layout/Navigation";
import Footer from "@/components/layout/Footer";
import ShellRadio from "@/components/layout/ShellRadio";
import CabeceraNoche from "@/components/shell/CabeceraNoche";
import PieNoche from "@/components/shell/PieNoche";
import { getAllEditions } from "@/lib/content";
import { getSenales } from "@/lib/senales";
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

export const metadata: Metadata = {
  title: "Curiana Radio - 88.8 FM",
  description: "Transmisión Cultural desde Abya Yala - A cultural newsletter experience delivered as immersive web pages.",
  metadataBase: new URL("https://curianaradio.com"), // Update with actual domain
  openGraph: {
    title: "Curiana Radio - 88.8 FM",
    description: "Transmisión Cultural desde Abya Yala",
    type: "website",
  },
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
  // «sintonizar ahora») y la arista de cada señal (la aguja marca la estación
  // de la arista cuando se lee una señal)
  const ultima = (await getAllEditions())[0];
  const edicion = { numero: String(ultima?.number ?? "01"), slug: ultima?.slug ?? "01" };
  const aristaDeSenal = Object.fromEntries(getSenales().map((s) => [s.slug, s.aristas[0] ?? null]));

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
        <ShellRadio
          nav={<Navigation />}
          footer={<Footer />}
          cabeceraNoche={<CabeceraNoche edicion={edicion} aristaDeSenal={aristaDeSenal} />}
          pieNoche={<PieNoche edicion={edicion} />}
        >
          {children}
        </ShellRadio>
      </body>
    </html>
  );
}
