// JAI Sounds — tipos compartidos entre la taxonomía curatorial (repo) y el
// catálogo (Supabase). La división no es accidental: Spotify deprecó
// audio-features el 2024-11-27, así que el mood NO puede derivarse de
// valence/energy. Lo pone la curaduría, a mano, y por eso vive en git.

// ── Taxonomía curatorial: content/jai-sounds/moods.json ───────────────

export interface Mood {
  slug: string;
  /** Nombre en la portada. */
  nombre: string;
  /** Posición en el dial — el índice se ordena por este número. */
  frecuencia: string;
  /** Una línea: qué se siente, no qué género es. */
  bajada: string;
  /**
   * Ángulo de matiz en **oklch** (0-360) con el que se pinta la estación.
   * No es hsl: oklch mantiene la luminosidad percibida al girar el matiz, y
   * así ninguna estación cae bajo el contraste AA. 25 rojo · 55 ámbar ·
   * 150 verde · 240 azul · 300 violeta · 355 rosa.
   */
  hue: number;
  /** Géneros que el mood cruza. El "trans" de transgénero: son puentes. */
  cruces: string[];
  /** IDs de playlist de Spotify que alimentan este mood. */
  playlists: string[];
  /**
   * true = semilla de estructura, no curaduría real. La portada lo marca en
   * pantalla para que nadie confunda andamio con criterio.
   */
  borrador: boolean;
}

export interface Taxonomia {
  moods: Mood[];
}

// ── Ficha editorial: content/jai-sounds/playlists.json ───────────────

/**
 * Una playlist publicada, con su copy. La unidad principal de JAI Sounds.
 * Todo lo editable vive en git, no en Spotify.
 */
export interface FichaPlaylist {
  slug: string;
  spotify_id: string;
  nombre: string;
  pistas: number;
  /** El copy propio. Vacío = todavía sin escribir. */
  descripcion: string;
  /** Arqueología: lo que quedó en Spotify. No es un destino a sincronizar. */
  descripcion_spotify: string | null;
  /** Portada propia. null = se pinta un color derivado del slug. */
  portada: string | null;
  /** Slug de mood, si algún día agrupamos por encima de las playlists. */
  mood: string | null;
  estado: "pendiente" | "copy" | "listo";
}

// ── Catálogo: tablas de Supabase (esquema `jai`) ─────────────────────

export interface JaiArtist {
  id: string;
  name: string;
  /** Lo que AFIRMA Spotify. Puede venir vacío; no es la taxonomía. */
  spotify_genres: string[] | null;
  popularity: number | null;
  image_url: string | null;
  synced_at: string;
}

export interface JaiTrack {
  id: string;
  name: string;
  album_name: string | null;
  album_image_url: string | null;
  /** Spotify da precisión variable — ver release_date_precision. */
  release_date: string | null;
  release_date_precision: "year" | "month" | "day" | null;
  duration_ms: number | null;
  isrc: string | null;
  popularity: number | null;
  spotify_url: string | null;
  synced_at: string;
}

export interface JaiPlaylist {
  id: string;
  name: string;
  description: string | null;
  image_url: string | null;
  track_count: number | null;
  /** Cambia cuando la playlist cambia — permite saltar re-ingestas. */
  snapshot_id: string | null;
  synced_at: string;
}

/** Conteos para el landing. Un solo viaje, no 12k filas. */
export interface CensoCatalogo {
  tracks: number;
  artistas: number;
  albums: number;
}
