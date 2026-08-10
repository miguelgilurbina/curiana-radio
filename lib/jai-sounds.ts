import fs from "fs";
import path from "path";
import { supabase, supabaseConfigured } from "./supabase";
import type {
  CensoCatalogo,
  FichaPlaylist,
  Mood,
  Taxonomia,
} from "@/types/jai-sounds";

const DIR = path.join(process.cwd(), "content", "jai-sounds");

/**
 * La curaduría vive AQUÍ, no en Spotify: descripciones, portadas y criterio
 * son contenido versionado, y se revisan en un diff como se revisa un texto.
 * Spotify solo aportó el catálogo y sirve de reproductor.
 */
function leerJSON<T>(archivo: string, vacio: T): T {
  try {
    return JSON.parse(fs.readFileSync(path.join(DIR, archivo), "utf-8")) as T;
  } catch (err) {
    // Falta el archivo (clon nuevo): estado vacío legítimo, no un bug.
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return vacio;
    // JSON malformado SÍ debe romper el build: es un error editorial.
    throw err;
  }
}

/**
 * Las playlists son la unidad principal de JAI Sounds. Se ordenan por número
 * de pistas: sin portadas ni descripciones todavía, el tamaño es la única
 * jerarquía honesta que tenemos.
 */
export function getPlaylists(): FichaPlaylist[] {
  const { playlists } = leerJSON<{ playlists: FichaPlaylist[] }>(
    "playlists.json",
    { playlists: [] }
  );
  return [...playlists].sort((a, b) => (b.pistas ?? 0) - (a.pistas ?? 0));
}

/**
 * Agrupador opcional por encima de las playlists. Hoy está vacío a
 * propósito — ver la nota en moods.json.
 */
export function getMoods(): Mood[] {
  const { moods } = leerJSON<Taxonomia>("moods.json", { moods: [] });
  return [...moods].sort(
    (a, b) => parseFloat(a.frecuencia) - parseFloat(b.frecuencia)
  );
}

/**
 * Matiz estable por playlist mientras no haya portada propia: mismo slug,
 * mismo color siempre. Evita que la parrilla se vea como un formulario
 * vacío y desaparece sin ruido cuando llegue el arte de verdad.
 */
export function hueDeSlug(slug: string): number {
  // FNV-1a: se acumula en 32 bits y se reduce UNA vez al final. Tomar el
  // módulo dentro del bucle (que es lo que hacía antes) tira la mayor parte
  // de la entropía y amontona los colores.
  let h = 0x811c9dc5;
  for (let i = 0; i < slug.length; i++) {
    h ^= slug.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0) % 360;
}

const CENSO_VACIO: CensoCatalogo = {
  tracks: 0,
  artistas: 0,
  albums: 0,
};

/**
 * Conteos del catálogo. Las tablas viven en el esquema `jai`, no en
 * `public`, así que hay que pedírselo explícitamente — y además el esquema
 * debe estar expuesto en la config de la API del proyecto.
 *
 * Nunca lanza: sin Supabase configurado devuelve ceros y el landing
 * renderiza igual. La curaduría no depende de la base.
 */
export async function getCenso(): Promise<CensoCatalogo> {
  if (!supabaseConfigured) return CENSO_VACIO;
  try {
    const jai = supabase.schema("jai");
    const [tracks, artistas, albums] = await Promise.all([
      jai.from("tracks").select("*", { count: "exact", head: true }),
      jai.from("artists").select("*", { count: "exact", head: true }),
      jai.from("albums").select("*", { count: "exact", head: true }),
    ]);
    return {
      tracks: tracks.count ?? 0,
      artistas: artistas.count ?? 0,
      albums: albums.count ?? 0,
    };
  } catch {
    return CENSO_VACIO;
  }
}
