#!/usr/bin/env node
/**
 * JAI Sounds · exportar el wiki
 * ---------------------------------------------------------------------
 * La base es la FUENTE; el sitio no la lee en vivo (curiana-produccion es
 * plan gratis y se pausa sola). Este script saca de la base lo que el wiki
 * necesita —y de las reseñas, SOLO las publicadas— y lo deja como JSON en
 * content/jai-sounds/wiki/, de donde las páginas se arman estáticas. Si la
 * base se pausa, el sitio no se entera.
 *
 *   estaciones.json   las 23, con su tracklist y su censo
 *   canciones.json    slug → canción (Spotify + MusicBrainz + las dos voces)
 *   albumes.json      slug → álbum
 *   artistas.json     slug → artista (+ «suena cerca de»)
 *
 * Uso:  node jai-sounds/scripts/exportar.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { RAIZ, conectar, esPrincipal, log, todas, trozos } from "./_comun.mjs";

const SALIDA = path.join(RAIZ, "content", "jai-sounds", "wiki");
const DIAL = path.join(RAIZ, "content", "jai-sounds", "playlists.json");

const porId = (filas, k = "id") => new Map(filas.map((f) => [f[k], f]));
const ordenar = (rel) => [...(rel ?? [])].sort((a, b) => a.position - b.position);
const anio = (f) => (f ? Number.parseInt(String(f).slice(0, 4), 10) || null : null);

/** Las dos voces de una entidad, si las tiene. */
function voces(entidad, id, internet, resenas) {
  const w = internet.get(`${entidad}:${id}`);
  const r = resenas.get(`${entidad}:${id}`);
  return {
    ...(r ? { resena: { cuerpo: r.cuerpo, publicada_en: r.publicada_en } } : {}),
    ...(w ? { internet: { titulo: w.titulo, extracto: w.extracto, url: w.url, idioma: w.idioma, licencia: w.licencia } } : {}),
  };
}

/**
 * Arma el export a partir de las tablas ya leídas. Pura: la prueba le pasa
 * tablas de juguete. `dial` es playlists.json en el orden de las estaciones.
 */
export function armar(dial, t) {
  const tracks = porId(t.tracks), albums = porId(t.albums), artists = porId(t.artists);
  const mbRec = porId(t.mb_recordings, "track_id"), mbArt = porId(t.mb_artists, "mbid");
  const internet = new Map(t.internet.map((w) => [`${w.entidad}:${w.entidad_id}`, w]));
  const resenas = new Map(t.resenas.filter((r) => r.estado === "publicada").map((r) => [`${r.entidad}:${r.entidad_id}`, r]));
  const slugArtistaPorMb = new Map(t.artists.filter((a) => a.mbid && a.slug).map((a) => [a.mbid, a.slug]));
  const trackArtistas = new Map(), albumArtistas = new Map();
  for (const r of t.track_artists) (trackArtistas.get(r.track_id) ?? trackArtistas.set(r.track_id, []).get(r.track_id)).push(r);
  for (const r of t.album_artists) (albumArtistas.get(r.album_id) ?? albumArtistas.set(r.album_id, []).get(r.album_id)).push(r);
  const artSlugs = (rels) => ordenar(rels).map((r) => artists.get(r.artist_id)?.slug).filter(Boolean);

  const canciones = {}, albumes = {}, artistas = {};
  const estacionesPorTrack = new Map();

  const estaciones = dial.map((p, i) => {
    const filas = t.playlist_tracks.filter((x) => x.playlist_id === p.spotify_id).sort((a, b) => a.position - b.position);
    const pistas = filas
      .filter((x) => tracks.get(x.track_id)?.slug)
      .map((x, k) => {
        const pos = k + 1;
        (estacionesPorTrack.get(x.track_id) ?? estacionesPorTrack.set(x.track_id, []).get(x.track_id)).push([i, pos, x.added_at?.slice(0, 10) ?? null]);
        return tracks.get(x.track_id).slug;
      });
    return { i, slug: p.slug, nombre: p.nombre, spotify_id: p.spotify_id, portada: p.portada, pistas };
  });

  // ── canciones ──
  for (const [trackId, enDial] of estacionesPorTrack) {
    const tr = tracks.get(trackId);
    const al = albums.get(tr.album_id);
    const mb = mbRec.get(trackId);
    canciones[tr.slug] = {
      t: tr.name,
      a: artSlugs(trackArtistas.get(trackId)),
      al: al?.slug ?? null,
      n: tr.track_number ?? null,
      ms: tr.duration_ms ?? null,
      fecha: al?.release_date ?? null,
      spotify: tr.spotify_url ?? `https://open.spotify.com/track/${trackId}`,
      id: trackId,
      img: al?.image_url ?? null,
      dial: enDial,
      // undefined: no se consultó · null: MusicBrainz no la tiene
      mb: mb === undefined ? undefined : !mb.mbid ? null : {
        f: mb.primera_edicion,
        g: mb.generos,
        tags: mb.tags,
        cr: mb.creditos.map((c) => ({ rol: c.rol, attrs: c.atributos, n: c.nombre, a: slugArtistaPorMb.get(c.mbid) ?? null, mbid: c.mbid })),
        obras: mb.obras,
        ed: mb.ediciones.map((e) => ({ f: e.fecha, t: e.titulo, tipo: e.tipo, sec: e.secundarios ?? [] })),
      },
      ...voces("cancion", trackId, internet, resenas),
    };
  }

  // ── álbumes ──
  for (const c of Object.values(canciones)) {
    if (!c.al) continue;
    const al = t.albums.find((a) => a.slug === c.al);
    albumes[c.al] ??= {
      t: al.name,
      tipo: al.album_type,
      fecha: al.release_date,
      a: artSlugs(albumArtistas.get(al.id)),
      img: al.image_url,
      id: al.id,
      canciones: [],
      ...voces("album", al.id, internet, resenas),
    };
  }
  for (const [slug, c] of Object.entries(canciones)) if (c.al) albumes[c.al].canciones.push(slug);

  // ── artistas: los que firman canciones o álbumes del dial ──
  const firmantes = new Set([...Object.values(canciones).flatMap((c) => c.a), ...Object.values(albumes).flatMap((a) => a.a)]);
  const porSlug = new Map(t.artists.filter((a) => a.slug).map((a) => [a.slug, a]));
  for (const slug of firmantes) {
    const ar = porSlug.get(slug);
    const m = ar.mbid ? mbArt.get(ar.mbid) : null;
    artistas[slug] = {
      n: ar.name,
      id: ar.id,
      mb: m ? {
        tipo: m.tipo, pais: m.pais, area: m.area, origen: m.origen, inicio: m.inicio, fin: m.fin, desamb: m.desambiguacion,
        g: m.generos, tags: m.tags,
        miembros: m.miembros.map((x) => ({ ...x, a: slugArtistaPorMb.get(x.mbid) ?? null })),
        de: m.integrante_de.map((x) => ({ ...x, a: slugArtistaPorMb.get(x.mbid) ?? null })),
        links: Object.fromEntries(["wikipedia", "wikidata", "discogs", "bandcamp", "web"].filter((k) => m[k]).map((k) => [k, m[k]])),
      } : null,
      canciones: Object.entries(canciones).filter(([, c]) => c.a.includes(slug)).map(([s]) => s),
      albumes: Object.entries(albumes).filter(([, a]) => a.a.includes(slug)).map(([s]) => s),
      ...voces("artista", ar.id, internet, resenas),
    };
  }

  // ── «suena cerca de»: quienes comparten estación, con la estación nombrada ──
  const porEstacion = estaciones.map((e) => new Set(e.pistas.flatMap((s) => canciones[s].a)));
  for (const [slug, ar] of Object.entries(artistas)) {
    const cuenta = new Map();
    porEstacion.forEach((set, i) => {
      if (!set.has(slug)) return;
      for (const otro of set) if (otro !== slug) {
        const c = cuenta.get(otro) ?? { n: 0, e: i };
        c.n++;
        cuenta.set(otro, c);
      }
    });
    ar.cerca = [...cuenta].sort((a, b) => b[1].n - a[1].n || a[0].localeCompare(b[0])).slice(0, 8).map(([a, c]) => [a, c.e]);
  }

  // ── el censo de cada estación ──
  for (const e of estaciones) {
    const cs = e.pistas.map((s) => canciones[s]);
    const anios = cs.map((c) => anio(c.mb?.f) ?? anio(c.fecha)).filter(Boolean);
    const cuenta = new Map();
    cs.forEach((c) => c.a.forEach((a) => cuenta.set(a, (cuenta.get(a) ?? 0) + 1)));
    e.censo = {
      pistas: cs.length,
      ms: cs.reduce((s, c) => s + (c.ms ?? 0), 0),
      desde: anios.length ? Math.min(...anios) : null,
      hasta: anios.length ? Math.max(...anios) : null,
      artistas: cuenta.size,
      presentes: [...cuenta].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 3),
    };
  }

  return { estaciones, canciones, albumes, artistas };
}

async function leerPorIds(db, tabla, columnas, campo, ids) {
  const out = [];
  for (const lote of trozos([...new Set(ids)].filter(Boolean), 200)) {
    const { data, error } = await db.from(tabla).select(columnas).in(campo, lote);
    if (error) throw new Error(`${tabla}: ${error.message}`);
    out.push(...data);
  }
  return out;
}

async function main() {
  const db = conectar();
  const { playlists } = JSON.parse(fs.readFileSync(DIAL, "utf8"));
  const dial = [...playlists].sort((a, b) => (b.pistas ?? 0) - (a.pistas ?? 0));

  log("▸ leyendo la base…");
  const playlist_tracks = await leerPorIds(db, "playlist_tracks", "playlist_id, track_id, position, added_at", "playlist_id", dial.map((p) => p.spotify_id));
  const ids = playlist_tracks.map((x) => x.track_id);
  const tracks = await leerPorIds(db, "tracks", "id, name, slug, album_id, track_number, duration_ms, spotify_url", "id", ids);
  const track_artists = await leerPorIds(db, "track_artists", "track_id, artist_id, position", "track_id", ids);
  const albums = await leerPorIds(db, "albums", "id, name, slug, album_type, release_date, image_url", "id", tracks.map((x) => x.album_id));
  const album_artists = await leerPorIds(db, "album_artists", "album_id, artist_id, position", "album_id", albums.map((a) => a.id));
  const artists = await leerPorIds(db, "artists", "id, name, slug, mbid", "id", [...track_artists, ...album_artists].map((r) => r.artist_id));
  const mb_recordings = await leerPorIds(db, "mb_recordings", "track_id, mbid, primera_edicion, generos, tags, creditos, obras, ediciones", "track_id", ids);
  const mbids = [...artists.map((a) => a.mbid), ...mb_recordings.flatMap((m) => (m.creditos ?? []).map((c) => c.mbid))];
  const mb_artists = await leerPorIds(db, "mb_artists", "*", "mbid", mbids);
  const internet = await todas(() => db.from("internet").select("entidad, entidad_id, titulo, extracto, url, idioma, licencia"));
  const resenas = await todas(() => db.from("resenas").select("entidad, entidad_id, cuerpo, estado, publicada_en").eq("estado", "publicada"));

  const sinSlug = tracks.filter((x) => !x.slug).length + artists.filter((x) => !x.slug).length + albums.filter((x) => !x.slug).length;
  if (sinSlug) log(`  ⚠ ${sinSlug} filas sin slug: correr antes npm run jai:slugs`);

  const w = armar(dial, { playlist_tracks, tracks, track_artists, albums, album_artists, artists, mb_recordings, mb_artists, internet, resenas });
  fs.mkdirSync(SALIDA, { recursive: true });
  for (const [nombre, datos] of Object.entries(w)) {
    const archivo = path.join(SALIDA, `${nombre}.json`);
    fs.writeFileSync(archivo, JSON.stringify(datos));
    log(`  · ${nombre}.json: ${Array.isArray(datos) ? datos.length : Object.keys(datos).length} · ${Math.round(fs.statSync(archivo).size / 1024)} KB`);
  }
  log(`\n✓ wiki exportado: ${resenas.length} reseñas publicadas.\n`);
}

if (esPrincipal(import.meta.url)) await main();
