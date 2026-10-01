// La gramática del trazo de los puntos del mapa de la portada (manual de
// Kaketiana: sólido es evidencia, firme es inferencia, discontinuo es duda).
// Aparte de lib/mapa.ts porque aquel lee el disco y esto lo usan también el
// mapa (cliente) y su leyenda (servidor).
import type { NivelLectura } from "@/lib/mapa";

export const OCRE = "#b06a1c"; // --sim-fuego en 6b
export const SAL = "#f2ede3"; // --sim-paper en 6b

export const ESTILO_NIVEL: Record<
  NivelLectura,
  { radio: number; relleno: string; opacidad: number; trazo?: string; etiqueta: string }
> = {
  A: { radio: 5, relleno: OCRE, opacidad: 0.95, etiqueta: "la lectura cierra con morfemas atestiguados" },
  B: { radio: 5, relleno: SAL, opacidad: 1, etiqueta: "la lectura exige un morfema despejado" },
  C: { radio: 4.5, relleno: SAL, opacidad: 0.6, trazo: "2 2", etiqueta: "la lectura es plausible" },
  // Punteado: la duda del manual. El nombre está; su lectura, no.
  sin: { radio: 4, relleno: SAL, opacidad: 0, trazo: "1 3", etiqueta: "sin lectura" },
};
