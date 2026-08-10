/**
 * Datos de MUESTRA para evaluar el diseño antes de que exista la ingesta.
 * ---------------------------------------------------------------------
 * SOLO SERVIDOR: lee del disco. Los componentes de cliente deben importar
 * de ./tipos, nunca de aquí.
 *
 * Todo el andamio de la muestra se borra de una vez: esta carpeta,
 * app/jai-sounds/muestra/, components/jai-sounds/Propuesta*.tsx y
 * content/jai-sounds/muestra.json. La ruta pública /jai-sounds no importa
 * nada de esto.
 */
import fs from "fs";
import path from "path";
import type { Mood } from "@/types/jai-sounds";
import type {
  AlbumMuestra,
  ArtistaMuestra,
  ArtistaResuelto,
  Muestra,
  PlaylistResuelta,
  TrackMuestra,
  TrackResuelto,
} from "./tipos";

export * from "./tipos";

const MUESTRA_PATH = path.join(
  process.cwd(),
  "content",
  "jai-sounds",
  "muestra.json"
);

export function getMuestra() {
  // Los moods de la muestra viven en su propio fixture, no en la taxonomía
  // real: son inventados, y el contenido de verdad no debe cargar con ellos.
  const { artistas, albums, tracks, playlists, moods } = JSON.parse(
    fs.readFileSync(MUESTRA_PATH, "utf-8")
  ) as Muestra & { moods: Mood[] };

  const porArtista = new Map(artistas.map((a) => [a.id, a]));
  const porAlbum = new Map(albums.map((d) => [d.id, d]));
  const porMood = new Map(moods.map((m) => [m.slug, m]));

  const resolver = (t: TrackMuestra): TrackResuelto => {
    const artistasResueltos = t.artistas
      .map((id) => porArtista.get(id))
      .filter((a): a is ArtistaMuestra => Boolean(a));
    return {
      ...t,
      album: porAlbum.get(t.album_id) ?? null,
      artistasResueltos,
      mood: porMood.get(t.mood_slug) ?? null,
      generos: [...new Set(artistasResueltos.flatMap((a) => a.generos))],
    };
  };

  const pistas = tracks.map(resolver);
  const porPista = new Map(pistas.map((t) => [t.id, t]));

  const listas: PlaylistResuelta[] = playlists.map((p) => {
    const suyas = p.tracks
      .map((id) => porPista.get(id))
      .filter((t): t is TrackResuelto => Boolean(t));
    return {
      ...p,
      mood: porMood.get(p.mood_slug) ?? null,
      pistas: suyas,
      duracionTotalMs: suyas.reduce((s, t) => s + t.duracion_ms, 0),
    };
  });

  const fichas: ArtistaResuelto[] = artistas.map((a) => {
    const suyas = pistas.filter((t) => t.artistas.includes(a.id));
    const moodsDelArtista = [
      ...new Map(
        suyas
          .map((t) => t.mood)
          .filter((m): m is Mood => Boolean(m))
          .map((m) => [m.slug, m])
      ).values(),
    ];
    // El "cruce" hecho grafo: con quién comparte territorio y en qué.
    const vecinos = artistas
      .filter((otro) => otro.id !== a.id)
      .map((otro) => ({
        artista: otro,
        comunes: otro.generos.filter((g) => a.generos.includes(g)),
      }))
      .filter((v) => v.comunes.length > 0)
      .sort((x, y) => y.comunes.length - x.comunes.length);

    return {
      ...a,
      albums: albums.filter((d) => d.artista_id === a.id),
      totalPistas: suyas.length,
      moods: moodsDelArtista,
      vecinos,
    };
  });

  const albumesOrdenados: AlbumMuestra[] = [...albums].sort(
    (a, b) => a.anio - b.anio
  );

  return { pistas, listas, fichas, albums: albumesOrdenados, moods };
}
