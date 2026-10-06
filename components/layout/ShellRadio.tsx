"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";
import Background from "./Background";

// El marco de cada página, según la ruta:
// - la intro El Disco (/, /intro) va sin marco: trae el suyo;
// - la noche —la landing, Señales y «Quién transmite»— lleva el shell La Noche
//   (CabeceraNoche + PieNoche, BRAND_MVP §13);
// - el resto del sitio sigue con el papel de la radio (Navigation + Footer)
//   hasta que su vista entre a la noche.
const SIN_MARCO = new Set(["/", "/intro"]);
const esNoche = (ruta: string) =>
  ruta === "/inicio" || ruta === "/sobre" || ruta === "/senales" || ruta.startsWith("/senales/");

export default function ShellRadio({
  nav,
  footer,
  cabeceraNoche,
  pieNoche,
  children,
}: {
  nav: ReactNode;
  footer: ReactNode;
  cabeceraNoche: ReactNode;
  pieNoche: ReactNode;
  children: ReactNode;
}) {
  const ruta = usePathname();
  if (SIN_MARCO.has(ruta)) return <main>{children}</main>;
  if (esNoche(ruta))
    return (
      <>
        {cabeceraNoche}
        <main>{children}</main>
        {pieNoche}
      </>
    );
  return (
    <Background>
      {nav}
      <main className="pt-16">{children}</main>
      {footer}
    </Background>
  );
}
