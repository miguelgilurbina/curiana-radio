#!/usr/bin/env node
/**
 * JAI Sounds · ingesta de playlists de Spotify → Supabase
 * ---------------------------------------------------------------------
 * Uso:
 *   node ingest_spotify.mjs --inspect <url|id> [...]   Solo mira: imprime
 *       nombre, id y nº de pistas. Sirve para derivar los moods reales
 *       antes de escribir nada. No toca la base de datos.
 *
 *   node ingest_spotify.mjs --sync                     Ingesta todas las
 *       playlists referenciadas en content/jai-sounds/moods.json.
 *
 *   node ingest_spotify.mjs --sync <url|id> [...]      Ingesta esas.
 *
 * Flags: --dry-run (no escribe)  --force (ignora snapshot_id y re-ingesta)
 *
 * Credenciales — SOLO por variables de entorno de la sesión, nunca en un
 * archivo del repo (este proyecto vive dentro de OneDrive: un .env con
 * secretos se sincroniza a la nube aunque esté gitignoreado):
 *   SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
 *   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
 *
 * Alcance del flujo Client Credentials: lee playlists PÚBLICAS por id. No
 * puede listar /me/playlists ni abrir privadas — eso exige Authorization
 * Code con redirect. Si alguna colección es privada, hacerla pública un
 * momento o pedir el flujo de usuario (otro PR).
 *
 * Lo que NO trae, y no es un olvido: valence, energy, danceability, tempo.
 * Spotify deprecó /audio-features el 2024-11-27 y devuelve 403 a toda app
 * creada después. El mood lo pone la curaduría, no la API.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.resolve(AQUI, "..", "..");
const TAXONOMIA = path.join(RAIZ, "content", "jai-sounds", "moods.json");

const API = "https://api.spotify.com/v1";
const LOTE_UPSERT = 500;

// ── Utilidades ───────────────────────────────────────────────────────

const log = (...a) => console.log(...a);
const fatal = (msg) => {
  console.error(`\n✗ ${msg}\n`);
  process.exit(1);
};

function trozos(arr, n) {
  const out = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}

/** Acepta id pelado, URL de open.spotify.com o URI spotify:playlist:… */
function idDePlaylist(entrada) {
  const limpio = entrada.trim();
  const url = limpio.match(/playlist[/:]([A-Za-z0-9]+)/);
  if (url) return url[1];
  if (/^[A-Za-z0-9]{22}$/.test(limpio)) return limpio;
  fatal(`No reconozco esto como playlist de Spotify: "${entrada}"`);
}

// ── Spotify ──────────────────────────────────────────────────────────

async function obtenerToken() {
  const id = process.env.SPOTIFY_CLIENT_ID;
  const secret = process.env.SPOTIFY_CLIENT_SECRET;
  if (!id || !secret) {
    fatal(
      "Faltan SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET en el entorno.\n" +
        "  Crear una app en https://developer.spotify.com/dashboard y exportarlas\n" +
        "  en la sesión del shell (NO en un archivo del repo — OneDrive sincroniza)."
    );
  }

  const res = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${Buffer.from(`${id}:${secret}`).toString("base64")}`,
    },
    body: "grant_type=client_credentials",
  });

  if (!res.ok) {
    fatal(`Spotify rechazó las credenciales (${res.status}): ${await res.text()}`);
  }
  return (await res.json()).access_token;
}

/** GET con reintento ante 429, respetando Retry-After. */
async function api(ruta, token, intento = 0) {
  const res = await fetch(ruta.startsWith("http") ? ruta : `${API}${ruta}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 429) {
    const espera = Number(res.headers.get("Retry-After") ?? 2) + 1;
    if (intento >= 5) fatal(`Rate limit persistente en ${ruta}`);
    log(`  · 429 — esperando ${espera}s`);
    await new Promise((r) => setTimeout(r, espera * 1000));
    return api(ruta, token, intento + 1);
  }

  if (res.status === 403) {
    fatal(
      `403 en ${ruta}\n` +
        "  Si es /audio-features o /recommendations: están deprecados desde\n" +
        "  2024-11-27 y no hay vía de acceso para apps nuevas."
    );
  }

  if (!res.ok) fatal(`Spotify ${res.status} en ${ruta}: ${await res.text()}`);
  return res.json();
}

async function traerPlaylist(id, token) {
  const meta = await api(`/playlists/${id}?fields=id,name,description,images,snapshot_id,tracks(total)`, token);

  const items = [];
  let url = `${API}/playlists/${id}/tracks?limit=100&offset=0`;
  while (url) {
    const pagina = await api(url, token);
    items.push(...pagina.items);
    url = pagina.next;
  }

  return { meta, items };
}

async function traerArtistas(ids, token) {
  const artistas = [];
  for (const lote of trozos([...ids], 50)) {
    const res = await api(`/artists?ids=${lote.join(",")}`, token);
    artistas.push(...res.artists.filter(Boolean));
  }
  return artistas;
}

// ── Normalización ────────────────────────────────────────────────────

function normalizar(items) {
  const tracks = new Map();
  const artistas = new Set();
  const enlacesTrackArtista = [];
  const enPlaylist = [];

  items.forEach((item, indice) => {
    const t = item?.track;
    // Pistas locales (sin id), episodios de podcast y huecos de canciones
    // borradas del catálogo: no son parte de la curaduría musical.
    if (!t || !t.id || t.type !== "track") return;

    if (!tracks.has(t.id)) {
      tracks.set(t.id, {
        id: t.id,
        name: t.name,
        album_name: t.album?.name ?? null,
        album_image_url: t.album?.images?.[0]?.url ?? null,
        release_date: t.album?.release_date ?? null,
        release_date_precision: t.album?.release_date_precision ?? null,
        duration_ms: t.duration_ms ?? null,
        isrc: t.external_ids?.isrc ?? null,
        popularity: t.popularity ?? null,
        spotify_url: t.external_urls?.spotify ?? null,
      });

      (t.artists ?? []).forEach((a, pos) => {
        if (!a.id) return;
        artistas.add(a.id);
        enlacesTrackArtista.push({ track_id: t.id, artist_id: a.id, position: pos });
      });
    }

    enPlaylist.push({
      track_id: t.id,
      position: indice,
      added_at: item.added_at ?? null,
    });
  });

  return { tracks, artistas, enlacesTrackArtista, enPlaylist };
}

// ── Supabase ─────────────────────────────────────────────────────────

function conectarSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    fatal(
      "Faltan SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY en el entorno.\n" +
        "  La service_role key es la única que puede escribir (ver RLS en la\n" +
        "  migración). Nunca la pongas en un NEXT_PUBLIC_* ni en un archivo."
    );
  }
  return createClient(url, key, { auth: { persistSession: false } });
}

async function upsert(db, tabla, filas, onConflict) {
  if (filas.length === 0) return;
  for (const lote of trozos(filas, LOTE_UPSERT)) {
    const { error } = await db.from(tabla).upsert(lote, { onConflict });
    if (error) fatal(`Upsert en ${tabla}: ${error.message}`);
  }
  log(`  · ${tabla}: ${filas.length} filas`);
}

// ── Modos ────────────────────────────────────────────────────────────

async function inspeccionar(ids, token) {
  log(`\nInspeccionando ${ids.length} playlist(s) — no se escribe nada.\n`);
  for (const id of ids) {
    const meta = await api(`/playlists/${id}?fields=id,name,tracks(total)`, token);
    log(`  ${meta.name}`);
    log(`    id: ${meta.id}   pistas: ${meta.tracks.total}`);
  }
  log(
    "\nSiguiente paso: agrupar estas playlists en moods dentro de\n" +
      "content/jai-sounds/moods.json (campo `playlists`) y poner borrador:false.\n"
  );
}

async function sincronizar(ids, token, { dryRun, force }) {
  const db = dryRun ? null : conectarSupabase();
  const artistasVistos = new Set();

  for (const id of ids) {
    log(`\n▸ ${id}`);
    const { meta, items } = await traerPlaylist(id, token);
    log(`  ${meta.name} — ${items.length} items`);

    if (!force && db) {
      const { data } = await db
        .from("jai_playlists")
        .select("snapshot_id")
        .eq("id", meta.id)
        .maybeSingle();
      if (data?.snapshot_id === meta.snapshot_id) {
        log("  · sin cambios desde la última ingesta (snapshot_id igual) — salto");
        continue;
      }
    }

    const { tracks, artistas, enlacesTrackArtista, enPlaylist } = normalizar(items);
    const descartados = items.length - enPlaylist.length;
    if (descartados > 0) {
      log(`  · ${descartados} items descartados (locales, episodios o borrados)`);
    }

    const nuevos = [...artistas].filter((a) => !artistasVistos.has(a));
    const filasArtistas = (await traerArtistas(nuevos, token)).map((a) => ({
      id: a.id,
      name: a.name,
      spotify_genres: a.genres ?? [],
      popularity: a.popularity ?? null,
      image_url: a.images?.[0]?.url ?? null,
    }));
    nuevos.forEach((a) => artistasVistos.add(a));

    if (dryRun) {
      log(
        `  · [dry-run] ${tracks.size} pistas, ${filasArtistas.length} artistas nuevos`
      );
      continue;
    }

    // Orden obligado por las claves foráneas: artistas y pistas antes que
    // los enlaces que las referencian.
    await upsert(db, "jai_artists", filasArtistas, "id");
    await upsert(db, "jai_tracks", [...tracks.values()], "id");
    await upsert(db, "jai_track_artists", enlacesTrackArtista, "track_id,artist_id");
    await upsert(
      db,
      "jai_playlists",
      [
        {
          id: meta.id,
          name: meta.name,
          description: meta.description ?? null,
          image_url: meta.images?.[0]?.url ?? null,
          track_count: meta.tracks?.total ?? null,
          snapshot_id: meta.snapshot_id ?? null,
        },
      ],
      "id"
    );
    await upsert(
      db,
      "jai_playlist_tracks",
      enPlaylist.map((e) => ({ ...e, playlist_id: meta.id })),
      "playlist_id,track_id"
    );
  }
}

// ── Entrada ──────────────────────────────────────────────────────────

function playlistsDeLaTaxonomia() {
  if (!fs.existsSync(TAXONOMIA)) fatal(`No encuentro ${TAXONOMIA}`);
  const { moods } = JSON.parse(fs.readFileSync(TAXONOMIA, "utf-8"));
  const ids = [...new Set(moods.flatMap((m) => m.playlists ?? []))];
  if (ids.length === 0) {
    fatal(
      "Ningún mood declara playlists todavía.\n" +
        "  Correr primero: node ingest_spotify.mjs --inspect <url> ...\n" +
        "  y llenar el campo `playlists` de cada mood."
    );
  }
  return ids;
}

async function main() {
  const argv = process.argv.slice(2);
  const flags = new Set(argv.filter((a) => a.startsWith("--")));
  const sueltos = argv.filter((a) => !a.startsWith("--"));

  const modoInspect = flags.has("--inspect");
  const modoSync = flags.has("--sync");
  if (modoInspect === modoSync) {
    fatal("Elegí un modo: --inspect o --sync. Ver la cabecera del archivo.");
  }

  // --inspect existe justamente para cuando la taxonomía aún está vacía:
  // exige URLs explícitas en vez de ir a buscarlas donde no hay.
  if (modoInspect && sueltos.length === 0) {
    fatal(
      "--inspect necesita al menos una playlist:\n" +
        "  node ingest_spotify.mjs --inspect https://open.spotify.com/playlist/..."
    );
  }

  const ids = (sueltos.length > 0 ? sueltos : playlistsDeLaTaxonomia()).map(
    idDePlaylist
  );

  const token = await obtenerToken();

  if (modoInspect) return inspeccionar(ids, token);

  await sincronizar(ids, token, {
    dryRun: flags.has("--dry-run"),
    force: flags.has("--force"),
  });
  log("\n✓ Listo.\n");
}

main().catch((e) => fatal(e.stack ?? String(e)));
