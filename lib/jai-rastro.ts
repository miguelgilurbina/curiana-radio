/**
 * El rastro del wiki: el camino que alguien recorre en la sesión, de la
 * batea a una canción, de ahí a su álbum, a quien lo firma… Vive en
 * sessionStorage y es del cliente: no toca el servidor ni la caché.
 *
 * Visitar un punto que ya está en el camino VUELVE a él (corta lo que venía
 * después); visitar uno nuevo lo agrega al final.
 */

export type TipoRastro = "estacion" | "cancion" | "album" | "artista";

export interface PuntoRastro {
  tipo: TipoRastro;
  slug: string;
  /** El nombre, tal como se lee en la miga. */
  n: string;
  /** Solo estaciones: su turno en el dial, para el color. */
  e?: number;
}

const CLAVE = "jai:rastro";
const EVENTO = "jai:rastro";

export function leerRastro(): PuntoRastro[] {
  try {
    const r = JSON.parse(sessionStorage.getItem(CLAVE) ?? "[]");
    return Array.isArray(r) ? r : [];
  } catch {
    return [];
  }
}

export function guardarRastro(r: PuntoRastro[]) {
  try {
    sessionStorage.setItem(CLAVE, JSON.stringify(r));
  } catch {
    // Sin sessionStorage el rastro dura lo que dura la página.
  }
  window.dispatchEvent(new Event(EVENTO));
}

/** Pura: el camino después de visitar `p`. */
export function trasVisitar(r: PuntoRastro[], p: PuntoRastro): PuntoRastro[] {
  const k = r.findIndex((x) => x.tipo === p.tipo && x.slug === p.slug);
  return k >= 0 ? r.slice(0, k + 1) : [...r, p];
}

export function visitar(p: PuntoRastro) {
  guardarRastro(trasVisitar(leerRastro(), p));
}

/** Entrar desde la batea reinicia el camino con la estación. */
export function empezarEn(p: PuntoRastro) {
  guardarRastro([p]);
}

export function suscribirRastro(fn: () => void) {
  window.addEventListener(EVENTO, fn);
  window.addEventListener("storage", fn);
  return () => {
    window.removeEventListener(EVENTO, fn);
    window.removeEventListener("storage", fn);
  };
}

export function hrefDe(p: PuntoRastro): string {
  if (p.tipo === "estacion") return `/jai-sounds#${String((p.e ?? 0) + 1).padStart(2, "0")}`;
  const ruta = { cancion: "canciones", album: "albumes", artista: "artistas" }[p.tipo];
  return `/jai-sounds/${ruta}/${p.slug}`;
}
