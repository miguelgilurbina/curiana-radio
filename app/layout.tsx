import type { Metadata } from "next";
import { Inter, Lora } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/layout/Navigation";
import Footer from "@/components/layout/Footer";
import Background from "@/components/layout/Background";

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

export const metadata: Metadata = {
  title: "Curiana Radio - 88.8 FM",
  description: "Transmisión Cultural desde Abya Yala - A cultural newsletter experience delivered as immersive web pages.",
  metadataBase: new URL("https://curianaradio.com"), // Update with actual domain
  openGraph: {
    title: "Curiana Radio - 88.8 FM",
    description: "Transmisión Cultural desde Abya Yala",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${inter.variable} ${lora.variable}`}>
      <body className="font-sans antialiased">
        <Background>
          <Navigation />
          <main className="pt-16">
            {children}
          </main>
          <Footer />
        </Background>
      </body>
    </html>
  );
}
