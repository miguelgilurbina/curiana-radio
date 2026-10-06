// Qué está al aire (Miguel, 2026-10-06): por ahora se liberan sólo Curiana
// Radio —la landing, Señales y «Quién transmite»—, Kaketiana y JAI Sounds. La
// Galería, Cuentos de Buchibe y el archivo de ediciones siguen en el taller:
// no salen en la cabecera, ni en el pie, ni en la landing, ni en Señales, ni
// en el sitemap, y en producción sus rutas vuelven a la radio
// (next.config.js, SIN_LIBERAR). Liberar una es cambiar su línea aquí y
// sacarla de SIN_LIBERAR.
export const LIBERADA = {
  kaketiana: true,
  "jai-sounds": true,
  galeria: false,
  buchibe: false,
  archivo: false,
} as const;

export type Seccion = keyof typeof LIBERADA;

/** «dos registros»: cuántas estaciones están al aire, en palabras */
export function registros(n: number): string {
  const palabras = ["ningún", "un", "dos", "tres", "cuatro", "cinco"];
  return `${palabras[n] ?? n} ${n === 1 ? "registro" : "registros"}`;
}
