import localFont from "next/font/local";

// La Fraunces de JAI: la misma familia del sitio, pero con los ejes que la
// sección necesita y el resto no — opsz (la display vive en opsz 9, tripas
// gruesas) e itálica (la voz de Descubriendo con Chocolate).
//
// Va como fuente LOCAL a propósito. Con next/font/google las dos instancias
// se registran con el mismo nombre de familia ("Fraunces"), y al navegar de
// JAI al simulador la de JAI (con opsz) le pisaría la display: .sim-display
// usa opsz automático y cambiaría de contraste. Local, la familia se llama
// distinto y no se cruzan. Los archivos son el subconjunto latino de Google
// Fonts (OFL, github.com/undercasetype/Fraunces), con opsz 9-144, wght,
// SOFT y WONK.
//
// Vive en su propio módulo porque la usan dos lugares: el layout de JAI y
// las señales que llevan la piel de JAI (app/senales/[slug]).
export const frauncesJai = localFont({
  src: [
    { path: "./fuentes/fraunces-jai.woff2", style: "normal", weight: "100 900" },
    {
      path: "./fuentes/fraunces-jai-italica.woff2",
      style: "italic",
      weight: "100 900",
    },
  ],
  variable: "--font-fraunces-jai",
  display: "swap",
  fallback: ["Georgia", "serif"],
  adjustFontFallback: "Times New Roman",
});
