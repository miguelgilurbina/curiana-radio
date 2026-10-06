#!/usr/bin/env node
/**
 * JAI Sounds · enriquecer el dial con MusicBrainz
 * ---------------------------------------------------------------------
 * Spotify ya no da géneros ni créditos. MusicBrainz sí, y lo encuentra por
 * ISRC (el 100% de las pistas lo tiene) o, si el ISRC no está registrado
 * allá, por título + artista + duración. Con la búsqueda de respaldo la
 * cobertura sube de ~63% a ~90%.
 *
 * Escribe:
 *   jai.mb_recordings   géneros, primera edición, créditos, obras, ediciones
 *   jai.mb_artists      país, origen, años, géneros, miembros, enlaces
 *   jai.artists.mbid    el puente Spotify → MusicBrainz
 *   jai.albums.mb_release_group
 *
 * Su API pide 1 consulta por segundo y un User-Agent con contacto. Todo pasa
 * por una caché en ~/.cache/jai-sounds/musicbrainz.json: cortar y volver a
 * correr no repite consultas.
 *
 * Uso:  node jai-sounds/scripts/musicbrainz.mjs [--force] [--dry-run]
 *   --force   vuelve a enriquecer pistas que ya tienen fila (usa la caché)
 */
import { cacheEnDisco, conectar, esPrincipal, idsDelDial, log, todas, trozos, upsert } from "./_comun.mjs";

const UA = "CurianaRadio-JAI/0.1 ( https://curianaradio.com )";

export const normalizar = (s) =>
  (s ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\(.*?\)|\[.*?\]| - .*$/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();

const escaparLucene = (s) => s.replace(/(["\\+\-!(){}[\]^~*?:/]|&&|\|\|)/g, "\\$1");

/** La ruta de búsqueda de respaldo. Es también la clave de la caché. */
export function rutaBusqueda(titulo, artista) {
  const q = `recording:"${escaparLucene(titulo.replace(/ - .*$/, ""))}" AND artist:"${escaparLucene(artista)}"`;
  return `recording?query=${encodeURIComponent(q)}&limit=5`;
}

/** Entre varias grabaciones, la que acredita al mismo primer artista. */
export function mejorGrabacion(recs, artista) {
  if (!recs?.length) return null;
  const a = normalizar(artista);
  return recs.find((r) => (r["artist-credit"] ?? []).some((c) => normalizar(c.name) === a || normalizar(c.artist?.name) === a)) ?? recs[0];
}

/** Candidatas de la búsqueda: puntaje alto y duración parecida (±15 s). */
export function candidatasBusqueda(recs, ms) {
  return (recs ?? []).filter((x) => (x.score ?? 0) >= 90 && (!ms || !x.length || Math.abs(x.length - ms) < 15000));
}

export function filaGrabacion(trackId, det, via) {
  const ediciones = new Map();
  for (const rel of det.releases ?? []) {
    const g = rel["release-group"];
    if (g && !ediciones.has(g.id)) {
      ediciones.set(g.id, { id: g.id, titulo: g.title, tipo: g["primary-type"] ?? null, secundarios: g["secondary-types"] ?? [], fecha: g["first-release-date"] || rel.date || null });
    }
  }
  const porConteo = (xs) => [...(xs ?? [])].sort((a, b) => b.count - a.count);
  return {
    track_id: trackId,
    mbid: det.id,
    via,
    primera_edicion: det["first-release-date"] || null,
    generos: porConteo(det.genres).map((g) => g.name),
    tags: porConteo(det.tags).slice(0, 8).map((g) => g.name),
    creditos: (det.relations ?? []).filter((r) => r["target-type"] === "artist").map((r) => ({ rol: r.type, atributos: r.attributes ?? [], nombre: r.artist?.name, mbid: r.artist?.id })),
    obras: (det.relations ?? []).filter((r) => r["target-type"] === "work").map((r) => ({ titulo: r.work?.title, mbid: r.work?.id })),
    ediciones: [...ediciones.values()].sort((a, b) => (a.fecha ?? "9").localeCompare(b.fecha ?? "9")),
    consultado_en: new Date().toISOString(),
  };
}

/**
 * La fila de una canción que MusicBrainz no tiene. Completa a propósito: en
 * un upsert por lotes, una columna ausente llega como NULL, no como su
 * default, y los arrays son NOT NULL.
 */
export function filaNoEncontrada(trackId) {
  return { track_id: trackId, mbid: null, via: null, primera_edicion: null, generos: [], tags: [], creditos: [], obras: [], ediciones: [], consultado_en: new Date().toISOString() };
}

/**
 * Spotify → MusicBrainz, artista por artista: por nombre, y si los nombres
 * no casan pero la cantidad sí, por orden. Si nada casa, no se adivina.
 */
export function puenteArtistas(spotify, creditos) {
  const out = {};
  spotify.forEach((s, i) => {
    const porNombre = creditos.find((a) => normalizar(a?.name) === normalizar(s.name));
    const a = porNombre ?? (creditos.length === spotify.length ? creditos[i] : null);
    if (a?.id) out[s.id] = a.id;
  });
  return out;
}

export function filaArtista(a) {
  const url = (tipo) => (a.relations ?? []).find((r) => r.type === tipo)?.url?.resource ?? null;
  const porConteo = (xs) => [...(xs ?? [])].sort((x, y) => y.count - x.count);
  const banda = (dir) => (a.relations ?? []).filter((r) => r.type === "member of band" && r.direction === dir);
  return {
    mbid: a.id,
    nombre: a.name,
    tipo: a.type ?? null,
    pais: a.country ?? null,
    area: a.area?.name ?? null,
    origen: a["begin-area"]?.name ?? null,
    inicio: a["life-span"]?.begin ?? null,
    fin: a["life-span"]?.end ?? null,
    desambiguacion: a.disambiguation || null,
    generos: porConteo(a.genres).map((g) => g.name),
    tags: porConteo(a.tags).slice(0, 8).map((g) => g.name),
    miembros: banda("backward").map((r) => ({ nombre: r.artist?.name, mbid: r.artist?.id, desde: r.begin ?? null, hasta: r.end ?? null })),
    integrante_de: banda("forward").map((r) => ({ nombre: r.artist?.name, mbid: r.artist?.id })),
    wikidata: url("wikidata"),
    wikipedia: url("wikipedia"),
    discogs: url("discogs"),
    bandcamp: url("bandcamp"),
    web: url("official homepage"),
    consultado_en: new Date().toISOString(),
  };
}

/** El release group del álbum de Spotify: el que se llama igual. */
export function grupoDelAlbum(nombreAlbum, ediciones) {
  const n = normalizar(nombreAlbum);
  return ediciones.find((e) => normalizar(e.titulo) === n)?.id ?? null;
}

export function clienteMB(cache) {
  let ultima = 0;
  return async function mb(ruta) {
    if (ruta in cache.datos) return cache.datos[ruta];
    for (let k = 0; k < 5; k++) {
      const espera = ultima + 1100 - Date.now();
      if (espera > 0) await new Promise((r) => setTimeout(r, espera));
      ultima = Date.now();
      let r;
      try {
        r = await fetch(`https://musicbrainz.org/ws/2/${ruta}${ruta.includes("?") ? "&" : "?"}fmt=json`, { headers: { "User-Agent": UA }, signal: AbortSignal.timeout(20000) });
      } catch {
        await new Promise((s) => setTimeout(s, 3000));
        continue;
      }
      if (r.status === 503 || r.status === 429) {
        await new Promise((s) => setTimeout(s, 3000 * (k + 1)));
        continue;
      }
      if (r.ok || r.status === 404 || r.status === 400) {
        const v = r.ok ? await r.json() : null;
        cache.datos[ruta] = v;
        cache.marcar();
        return v;
      }
    }
    return null;
  };
}

async function main() {
  const force = process.argv.includes("--force");
  const seco = process.argv.includes("--dry-run");
  const db = conectar();
  const cache = cacheEnDisco("musicbrainz.json");
  const mb = clienteMB(cache);

  const ids = await idsDelDial(db);
  const hechas = new Set(force ? [] : (await todas(() => db.from("mb_recordings").select("track_id"))).map((f) => f.track_id));
  const pendientes = ids.filter((id) => !hechas.has(id));
  log(`▸ ${ids.length} canciones en el dial · ${pendientes.length} por enriquecer`);

  const pistas = [];
  for (const lote of trozos(pendientes, 200)) {
    const { data, error } = await db.from("tracks").select("id, name, isrc, duration_ms, album_id, albums(name), track_artists(position, artist_id, artists(name))").in("id", lote);
    if (error) throw error;
    pistas.push(...data);
  }

  const grabaciones = [], puente = {}, albumGrupo = {}, artistasMB = new Set();
  let k = 0;
  for (const t of pistas) {
    k++;
    const artistas = [...(t.track_artists ?? [])].sort((a, b) => a.position - b.position).map((x) => ({ id: x.artist_id, name: x.artists?.name ?? "" }));
    const isrc = (t.isrc ?? "").replace(/[^A-Za-z0-9]/g, "").toUpperCase();
    let rec = null, via = null;
    if (isrc) {
      rec = mejorGrabacion((await mb(`isrc/${isrc}?inc=artist-credits`))?.recordings, artistas[0]?.name);
      if (rec) via = "isrc";
    }
    if (!rec && artistas[0]) {
      rec = mejorGrabacion(candidatasBusqueda((await mb(rutaBusqueda(t.name, artistas[0].name)))?.recordings, t.duration_ms), artistas[0].name);
      if (rec) via = "busqueda";
    }
    const det = rec ? await mb(`recording/${rec.id}?inc=artist-credits+releases+release-groups+genres+tags+artist-rels+work-rels+url-rels`) : null;
    if (!det) {
      // Buscada y no encontrada: se anota para no volver a preguntar.
      grabaciones.push(filaNoEncontrada(t.id));
      continue;
    }
    const fila = filaGrabacion(t.id, det, via);
    grabaciones.push(fila);
    const creditos = (det["artist-credit"] ?? []).map((c) => c.artist).filter(Boolean);
    Object.assign(puente, puenteArtistas(artistas, creditos));
    creditos.forEach((a) => artistasMB.add(a.id));
    if (t.album_id && !albumGrupo[t.album_id]) {
      const g = grupoDelAlbum(t.albums?.name, fila.ediciones);
      if (g) albumGrupo[t.album_id] = { id: t.album_id, name: t.albums.name, mb_release_group: g };
    }
    if (k % 50 === 0) log(`  ${k}/${pistas.length}`);
  }
  cache.guardar();
  const encontradas = grabaciones.filter((g) => g.mbid).length;
  log(`  encontradas ${encontradas}/${grabaciones.length}`);

  log(`▸ ${artistasMB.size} artistas en MusicBrainz`);
  const artistas = [];
  for (const id of artistasMB) {
    const a = await mb(`artist/${id}?inc=genres+tags+url-rels+artist-rels`);
    if (a) artistas.push(filaArtista(a));
  }
  cache.guardar();

  if (seco) {
    log("\n[dry-run] nada escrito.\n");
    return;
  }
  await upsert(db, "mb_recordings", grabaciones, "track_id");
  await upsert(db, "mb_artists", artistas, "mbid");
  // De a 200: con 1.700 ids en un solo `in`, la URL de PostgREST no entra.
  const nombres = new Map();
  for (const lote of trozos(Object.keys(puente), 200)) {
    const { data, error } = await db.from("artists").select("id, name").in("id", lote);
    if (error) throw error;
    data.forEach((a) => nombres.set(a.id, a.name));
  }
  await upsert(db, "artists", Object.entries(puente).filter(([id]) => nombres.has(id)).map(([id, mbid]) => ({ id, name: nombres.get(id), mbid })), "id");
  await upsert(db, "albums", Object.values(albumGrupo), "id");
  log("\n✓ MusicBrainz listo.\n");
}

if (esPrincipal(import.meta.url)) await main();
