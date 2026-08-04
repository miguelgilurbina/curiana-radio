/**
 * Parte CLIENT-SAFE de la muestra: tipos y funciones puras.
 *
 * Vive separada de index.ts porque ese lee del disco con `fs`, y los
 * componentes de cliente (la mesa de curaduría) necesitan estos tipos y
 * formateadores. Importar un valor de un módulo que toca `fs` arrastra el
 * módulo entero al bundle del navegador y rompe el build. Aquí no hay
 * ningún import de Node: este archivo puede cruzar la frontera.
 */
import type { Mood } from "@/types/jai-sounds";

export interface ArtistaMuestra {
  id: string;
  nombre: string;
  generos: string[];
  hue: number;
}

export interface AlbumMuestra {
  id: string;
  nombre: string;
  artista_id: string;
  anio: number;
}

export interface TrackMuestra {
  id: string;
  nombre: string;
  album_id: string;
  artistas: string[];
  duracion_ms: number;
  popularidad: number;
  mood_slug: string;
  nota: string;
  destacado: boolean;
}

export interface PlaylistMuestra {
  id: string;
  nombre: string;
  descripcion: string;
  mood_slug: string;
  tracks: string[];
}

export interface Muestra {
  artistas: ArtistaMuestra[];
  albums: AlbumMuestra[];
  tracks: TrackMuestra[];
  playlists: PlaylistMuestra[];
}

/** Una pista con todo resuelto — lo que la UI necesita de verdad. */
export interface TrackResuelto extends TrackMuestra {
  album: AlbumMuestra | null;
  artistasResueltos: ArtistaMuestra[];
  mood: Mood | null;
  /** Unión de los géneros de sus artistas: el "cruce" de la pista. */
  generos: string[];
}

export interface PlaylistResuelta extends PlaylistMuestra {
  mood: Mood | null;
  pistas: TrackResuelto[];
  duracionTotalMs: number;
}

/** Un artista con lo que se le cuelga: obra, alcance, dónde cruza. */
export interface ArtistaResuelto extends ArtistaMuestra {
  albums: AlbumMuestra[];
  totalPistas: number;
  moods: Mood[];
  /** Otros artistas del catálogo con los que comparte al menos un género. */
  vecinos: { artista: ArtistaMuestra; comunes: string[] }[];
}

export function formatearDuracion(ms: number): string {
  const total = Math.round(ms / 1000);
  const min = Math.floor(total / 60);
  const seg = total % 60;
  return `${min}:${String(seg).padStart(2, "0")}`;
}

export function formatearDuracionLarga(ms: number): string {
  const min = Math.round(ms / 60000);
  if (min < 60) return `${min} min`;
  const h = Math.floor(min / 60);
  return `${h} h ${min % 60} min`;
}
