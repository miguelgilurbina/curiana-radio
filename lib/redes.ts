// Las redes de Curiana Radio (Miguel, 2026-10-03: «@curianaradio en ig y
// youtube»). Un solo lugar: el pie global, el colofón de la landing y el pie
// de cada señal leen de aquí.
export const REDES = [
  { nombre: "Instagram", usuario: "@curianaradio", url: "https://www.instagram.com/curianaradio/" },
  { nombre: "YouTube", usuario: "@curianaradio", url: "https://www.youtube.com/@curianaradio" },
] as const;

// El portafolio de Miguel como desarrollador (Miguel, 2026-10-05): sale en
// «Quién transmite» (/sobre), en la landing y como url del autor en el
// JSON-LD de cada señal.
export const PORTAFOLIO = { texto: "miguelgilurbina.com", url: "https://www.miguelgilurbina.com/" } as const;
