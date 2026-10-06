"use client";

import type { ReactNode } from "react";
import { usePathname } from "next/navigation";

// El marco de cada página. La intro El Disco (/, /intro) va sin marco: trae
// el suyo. Todo lo demás va en el shell La Noche (CabeceraNoche + PieNoche,
// BRAND_MVP §13): desde el 2026-10-06 ya no queda el papel de la radio (la
// nav, el pie y el fondo animado de antes se retiraron).
const SIN_MARCO = new Set(["/", "/intro"]);

export default function ShellRadio({
  cabecera,
  pie,
  children,
}: {
  cabecera: ReactNode;
  pie: ReactNode;
  children: ReactNode;
}) {
  const ruta = usePathname();
  if (SIN_MARCO.has(ruta)) return <main>{children}</main>;
  return (
    <>
      {cabecera}
      <main>{children}</main>
      {pie}
    </>
  );
}
