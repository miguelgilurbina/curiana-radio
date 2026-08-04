import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "JAI Sounds — Curaduría musical | Curiana Radio",
  description:
    "Un dial de moods. Curaduría musical que cruza géneros: lo que la máquina ya no sabe medir, lo decide el oído.",
  openGraph: {
    title: "JAI Sounds — Curaduría musical",
    description: "Un dial de moods desde Curiana Radio · 88.8 FM",
    type: "website",
  },
};

// El layout solo fija el registro de la sección; el chrome lo arma cada
// página. Mismo patrón que /simulador: la arista es dueña de su tema.
export default function JaiSoundsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      data-jai-theme="dial"
      className="min-h-screen bg-(--jai-noche) text-(--jai-luz) animate-fade-in"
    >
      {children}
    </div>
  );
}
