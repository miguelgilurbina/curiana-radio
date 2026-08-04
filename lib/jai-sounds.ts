import fs from "fs";
import path from "path";
import { supabase, supabaseConfigured } from "./supabase";
import type { CensoCatalogo, Mood, Taxonomia } from "@/types/jai-sounds";

const TAXONOMIA_PATH = path.join(
  process.cwd(),
  "content",
  "jai-sounds",
  "moods.json"
);

/**
 * La taxonomía es contenido versionado, no base de datos: es el criterio
 * curatorial y se revisa en un diff como se revisa un texto. Misma decisión
 * que el lexicón del simulador.
 */
export function getMoods(): Mood[] {
  let raw: string;
  try {
    raw = fs.readFileSync(TAXONOMIA_PATH, "utf-8");
  } catch (err) {
    // Sin taxonomía no hay dial. Es un estado vacío legítimo (clon nuevo),
    // no un bug -- la portada muestra el vacío y lo dice.
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw err;
  }
  // JSON malformado SÍ debe romper el build: un mood a medio escribir es un
  // error editorial, no "sin datos".
  const moods = (JSON.parse(raw) as Taxonomia).moods ?? [];
  return [...moods].sort(
    (a, b) => parseFloat(a.frecuencia) - parseFloat(b.frecuencia)
  );
}

export function hayTaxonomiaEnBorrador(moods: Mood[]): boolean {
  return moods.some((m) => m.borrador);
}

const CENSO_VACIO: CensoCatalogo = {
  tracks: 0,
  artistas: 0,
  playlists: 0,
  porPlaylist: {},
};

/**
 * Conteos para la portada. 12k tracks no se traen al cliente: se cuentan en
 * Postgres (head + count exact) y el desglose por playlist sale de la vista
 * jai_playlist_counts.
 *
 * Nunca lanza: si Supabase no está configurado o la migración no corrió aún,
 * devuelve censo en cero y la portada renderiza el dial sin cifras.
 */
export async function getCenso(): Promise<CensoCatalogo> {
  if (!supabaseConfigured) return CENSO_VACIO;

  try {
    const [tracks, artistas, playlists, conteos] = await Promise.all([
      supabase.from("jai_tracks").select("*", { count: "exact", head: true }),
      supabase.from("jai_artists").select("*", { count: "exact", head: true }),
      supabase.from("jai_playlists").select("*", { count: "exact", head: true }),
      supabase.from("jai_playlist_counts").select("playlist_id, total"),
    ]);

    const porPlaylist: Record<string, number> = {};
    for (const fila of conteos.data ?? []) {
      porPlaylist[fila.playlist_id as string] = Number(fila.total);
    }

    return {
      tracks: tracks.count ?? 0,
      artistas: artistas.count ?? 0,
      playlists: playlists.count ?? 0,
      porPlaylist,
    };
  } catch {
    // Tablas aún no creadas / red caída: el dial vale sin cifras.
    return CENSO_VACIO;
  }
}

/** Cuántos tracks respaldan un mood, sumando sus playlists. */
export function contarMood(mood: Mood, censo: CensoCatalogo): number {
  return mood.playlists.reduce(
    (total, id) => total + (censo.porPlaylist[id] ?? 0),
    0
  );
}
