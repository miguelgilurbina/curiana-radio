"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";
import Background from "./Background";

// El chrome de la radio (fondo animado, navegación y pie) envuelve todas las
// páginas menos las que traen el suyo: la intro El Disco y la landing de la
// noche, que tiene su barra en el hero y su colofón al pie.
const PROPIAS = new Set(["/", "/intro", "/inicio"]);

export default function ShellRadio({
  nav,
  footer,
  children,
}: {
  nav: ReactNode;
  footer: ReactNode;
  children: ReactNode;
}) {
  const ruta = usePathname();
  if (PROPIAS.has(ruta)) return <main>{children}</main>;
  return (
    <Background>
      {nav}
      <main className="pt-16">{children}</main>
      {footer}
    </Background>
  );
}
