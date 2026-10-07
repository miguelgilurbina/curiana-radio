// El wiki de JAI Sounds, tal como lo deja jai-sounds/scripts/exportar.mjs en
// content/jai-sounds/wiki/. La base es la fuente; el sitio solo lee esto.

export interface Censo {
  pistas: number;
  ms: number;
  desde: number | null;
  hasta: number | null;
  artistas: number;
  /** Los tres que más se repiten: [slug de artista, veces]. */
  presentes: [string, number][];
}

export interface EstacionWiki {
  /** Su turno en el dial (0-22): de ahí sale el matiz. */
  i: number;
  slug: string;
  nombre: string;
  spotify_id: string;
  portada: string | null;
  /** Slugs de canción, en el orden de la playlist. */
  pistas: string[];
  censo: Censo;
}

export interface Resena {
  cuerpo: string;
  publicada_en: string | null;
}

export interface Internet {
  titulo: string | null;
  extracto: string;
  url: string;
  idioma: string | null;
  licencia: string | null;
}

export interface Voces {
  resena?: Resena;
  internet?: Internet;
}

export interface CreditoMB {
  rol: string;
  attrs: string[];
  n: string;
  /** Slug de artista si está en el dial; si no, null. */
  a: string | null;
  mbid: string;
}

export interface GrabacionMB {
  /** isrc: la misma grabación · busqueda: por título y duración (puede ser otra edición). */
  via?: "isrc" | "busqueda" | null;
  /** Primera edición según MusicBrainz. */
  f: string | null;
  g: string[];
  tags: string[];
  cr: CreditoMB[];
  obras: { titulo: string; mbid: string }[];
  ed: { f: string | null; t: string; tipo: string | null; sec: string[] }[];
}

export interface CancionWiki extends Voces {
  t: string;
  /** Slugs de artista, en orden de crédito. */
  a: string[];
  al: string | null;
  n: number | null;
  ms: number | null;
  /** La fecha del álbum según Spotify (a menudo la del reissue). */
  fecha: string | null;
  spotify: string;
  id: string;
  img: string | null;
  /** [estación, puesto (1-based), en el dial desde] */
  dial: [number, number, string | null][];
  /** undefined: sin consultar · null: MusicBrainz no la tiene */
  mb?: GrabacionMB | null;
}

export interface AlbumWiki extends Voces {
  t: string;
  tipo: string | null;
  fecha: string | null;
  a: string[];
  img: string | null;
  id: string;
  canciones: string[];
}

export interface PersonaMB {
  nombre: string;
  mbid: string;
  a: string | null;
  desde?: string | null;
  hasta?: string | null;
}

export interface ArtistaMB {
  tipo: string | null;
  pais: string | null;
  area: string | null;
  origen: string | null;
  inicio: string | null;
  fin: string | null;
  desamb: string | null;
  g: string[];
  tags: string[];
  miembros: PersonaMB[];
  de: PersonaMB[];
  links: Partial<Record<"wikipedia" | "wikidata" | "discogs" | "bandcamp" | "web", string>>;
}

export interface ArtistaWiki extends Voces {
  n: string;
  id: string;
  mb: ArtistaMB | null;
  canciones: string[];
  albumes: string[];
  /** Quienes comparten estación: [slug de artista, estación]. */
  cerca: [string, number][];
}

/** Una fila del tracklist de la batea: lo que la contraportada y la ficha necesitan. */
export interface FilaPista {
  s: string;
  t: string;
  a: { s: string; n: string }[];
  al: { s: string; n: string } | null;
  /** Año a mostrar: primera edición si MusicBrainz la sabe, si no Spotify. */
  y: string | null;
  /** Fecha de Spotify, para el «spotify dice …» cuando difiere. */
  ys: string | null;
  /** Primera edición completa de MusicBrainz. */
  f: string | null;
  d: string;
  img: string | null;
  desde: string | null;
  /** Otras estaciones donde suena. */
  tambien: number[];
  r: string | null;
  spotify: string;
}

export interface DatosEstacion {
  i: number;
  filas: FilaPista[];
  /** Solo las primeras filas (el HTML inicial): el resto llega por /jai-sounds/datos/NN. */
  parcial?: boolean;
}
