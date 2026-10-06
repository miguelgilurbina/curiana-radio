import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Señales — Curiana Radio",
  description:
    "Lo que escribe Miguel Gil Urbina, creador de Curiana Radio, sobre cada arista del imaginario: Kaketiana y JAI Sounds.",
  alternates: {
    canonical: "/senales",
    types: { "application/rss+xml": [{ url: "/senales/rss.xml", title: "Señales — Curiana Radio" }] },
  },
};

// El índice vive en la noche de la v1 (BRAND_MVP §10), como la landing que
// lo muestra; cada señal, en la piel de su arista (components/senales/
// pieles.ts). Por eso el layout no pone superficie: la pone cada página. El
// chrome global (nav y pie) lo pone ShellRadio, como en JAI Sounds.
export default function SenalesLayout({ children }: { children: React.ReactNode }) {
  return children;
}
