#!/usr/bin/env node
/**
 * JAI Sounds · ingesta de Spotify → Supabase
 * ---------------------------------------------------------------------
 * Uso, en el orden en que se usa la primera vez:
 *
 *   --login              Abre el consentimiento de Spotify y guarda la
 *                        sesión en ~/.secrets/. Una sola vez.
 *
 *   --listar             Lista TODAS tus playlists (incluidas privadas) con
 *                        nombre, id y nº de pistas. No escribe nada. De aquí
 *                        salen los moods reales.
 *
 *   --sync               Ingesta las playlists declaradas en
 *                        content/jai-sounds/moods.json.
 *   --sync <url|id> …    Ingesta esas.
 *   --sync --todas       Ingesta todas tus playlists sin preguntar.
 *   --sync --guardadas   Ingesta además "Canciones que te gustan".
 *
 * Flags: --dry-run (no escribe)  --force (ignora snapshot_id)
 *
 * Credenciales — SOLO por variables de entorno de la sesión, nunca en un
 * archivo del repo (el proyecto vive dentro de OneDrive: un .env con
 * secretos se sincroniza a la nube aunque esté gitignoreado):
 *   SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
 *   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
 *
 * Lo que NO trae, y no es un olvido: valence, energy, danceability, tempo.
 * Spotify deprecó /audio-features el 2024-11-27 y devuelve 403 a toda app
 * creada después. El mood lo pone la curaduría, no la API.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";
import {
  ErrorDeConfig,
  haySesion,
  login,
  tokenDeApp,
  tokenDeUsuario,
} from "./spotify_auth.mjs";

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.resolve(AQUI, "..", "..");
const TAXONOMIA = path.join(RAIZ, "content", "jai-sounds", "moods.json");

const API = "https://api.spotify.com/v1";
const LOTE_UPSERT = 500;
/** Pseudo-playlist para "Canciones que te gustan", que no tiene id propio. */
const ID_GUARDADAS = "me-saved-tracks";

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

// ── Cliente HTTP ─────────────────────────────────────────────────────

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

  if (res.status === 401) {
    fatal(
      `401 en ${ruta}\n` +
        "  Token inválido o sin el scope necesario. Reintentar --login."
    );
  }

  if (!res.ok) fatal(`Spotify ${res.status} en ${ruta}: ${await res.text()}`);
  return res.json();
}

/** Recorre un endpoint paginado hasta el final. */
async function paginar(rutaInicial, token) {
  const items = [];
  let url = rutaInicial;
  while (url) {
    const pagina = await api(url, token);
    items.push(...pagina.items);
    url = pagina.next;
  }
  return items;
}

// ── Lecturas ─────────────────────────────────────────────────────────

async function misPlaylists(token) {
  const crudas = await paginar(`${API}/me/playlists?limit=50`, token);
  return crudas.filter(Boolean).map((p) => ({
    id: p.id,
    name: p.name,
    description: p.description ?? null,
    image_url: p.images?.[0]?.url ?? null,
    track_count: p.tracks?.total ?? null,
    snapshot_id: p.snapshot_id ?? null,
  }));
}

async function traerPlaylist(id, token) {
  const meta = await api(
    `/playlists/${id}?fields=id,name,description,images,snapshot_id,tracks(total)`,
    token
  );
  const items = await paginar(
    `${API}/playlists/${id}/tracks?limit=100&offset=0`,
    token
  );
  return { meta, items };
}

async function traerGuardadas(token) {
  const items = await paginar(`${API}/me/tracks?limit=50`, token);
  return {
    meta: {
      id: ID_GUARDADAS,
      name: "Canciones que te gustan",
      description: "Biblioteca guardada del usuario (/me/tracks).",
      images: [],
      // No hay snapshot_id: siempre se re-ingesta.
      snapshot_id: null,
      tracks: { total: items.length },
    },
    items,
  };
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

async function listar(token) {
  const listas = await misPlaylists(token);
  const total = listas.reduce((s, p) => s + (p.track_count ?? 0), 0);

  log(`\n${listas.length} playlists · ${total} pistas en total\n`);
  for (const p of listas) {
    log(`  ${String(p.track_count ?? "?").padStart(5)}  ${p.name}`);
    log(`         ${p.id}`);
  }
  log(
    "\nSiguiente paso: agrupar estas listas en moods dentro de\n" +
      "content/jai-sounds/moods.json (campo `playlists`) y poner borrador:false.\n" +
      "O ingestar todo de una con: --sync --todas\n"
  );
}

async function inspeccionar(ids, token) {
  log(`\nInspeccionando ${ids.length} playlist(s) — no se escribe nada.\n`);
  for (const id of ids) {
    const meta = await api(`/playlists/${id}?fields=id,name,tracks(total)`, token);
    log(`  ${meta.name}`);
    log(`    id: ${meta.id}   pistas: ${meta.tracks.total}`);
  }
}

async function sincronizar(fuentes, token, { dryRun, force }) {
  const db = dryRun ? null : conectarSupabase();
  const artistasVistos = new Set();
  let totalPistas = 0;

  for (const fuente of fuentes) {
    log(`\n▸ ${fuente === ID_GUARDADAS ? "Canciones guardadas" : fuente}`);

    const { meta, items } =
      fuente === ID_GUARDADAS
        ? await traerGuardadas(token)
        : await traerPlaylist(fuente, token);

    log(`  ${meta.name} — ${items.length} items`);

    if (!force && db && meta.snapshot_id) {
      const { data } = await db
        .from("jai_playlists")
        .select("snapshot_id")
        .eq("id", meta.id)
        .maybeSingle();
      if (data?.snapshot_id === meta.snapshot_id) {
        log("  · sin cambios desde la última ingesta — salto");
        continue;
      }
    }

    const { tracks, artistas, enlacesTrackArtista, enPlaylist } =
      normalizar(items);
    const descartados = items.length - enPlaylist.length;
    if (descartados > 0) {
      log(`  · ${descartados} descartados (locales, episodios o borrados)`);
    }
    totalPistas += tracks.size;

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
    await upsert(
      db,
      "jai_track_artists",
      enlacesTrackArtista,
      "track_id,artist_id"
    );
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

  log(`\n✓ ${totalPistas} pistas procesadas.\n`);
}

// ── Entrada ──────────────────────────────────────────────────────────

function playlistsDeLaTaxonomia() {
  if (!fs.existsSync(TAXONOMIA)) fatal(`No encuentro ${TAXONOMIA}`);
  const { moods } = JSON.parse(fs.readFileSync(TAXONOMIA, "utf-8"));
  const ids = [...new Set(moods.flatMap((m) => m.playlists ?? []))];
  if (ids.length === 0) {
    fatal(
      "Ningún mood declara playlists todavía.\n" +
        "  Correr primero: --listar   (y llenar el campo `playlists`)\n" +
        "  O ingestar todo de una:    --sync --todas"
    );
  }
  return ids;
}

async function main() {
  const argv = process.argv.slice(2);
  const flags = new Set(argv.filter((a) => a.startsWith("--")));
  const sueltos = argv.filter((a) => !a.startsWith("--"));

  if (flags.has("--login")) {
    await login();
    log("Siguiente: node jai-sounds/scripts/ingest_spotify.mjs --listar\n");
    return;
  }

  const modos = ["--listar", "--inspect", "--sync"].filter((m) => flags.has(m));
  if (modos.length !== 1) {
    fatal(
      "Elegí un modo: --login, --listar, --inspect o --sync.\n" +
        "  Ver la cabecera del archivo para el flujo completo."
    );
  }
  const modo = modos[0];

  // Con sesión de usuario leemos también lo privado; sin ella, solo lo
  // público — y --listar directamente no existe sin usuario.
  const conUsuario = haySesion();
  if (!conUsuario && (modo === "--listar" || flags.has("--todas") || flags.has("--guardadas"))) {
    fatal(
      "Eso necesita sesión de usuario.\n" +
        "  Correr primero: node jai-sounds/scripts/ingest_spotify.mjs --login"
    );
  }
  const token = conUsuario ? await tokenDeUsuario() : await tokenDeApp();
  if (!conUsuario) {
    log("· Sin sesión de usuario: solo playlists públicas por id.");
  }

  if (modo === "--listar") return listar(token);

  if (modo === "--inspect") {
    if (sueltos.length === 0) {
      fatal(
        "--inspect necesita al menos una playlist:\n" +
          "  node ingest_spotify.mjs --inspect https://open.spotify.com/playlist/..."
      );
    }
    return inspeccionar(sueltos.map(idDePlaylist), token);
  }

  // --sync
  let fuentes;
  if (flags.has("--todas")) {
    fuentes = (await misPlaylists(token)).map((p) => p.id);
    log(`· ${fuentes.length} playlists encontradas en tu cuenta.`);
  } else if (sueltos.length > 0) {
    fuentes = sueltos.map(idDePlaylist);
  } else if (flags.has("--guardadas")) {
    fuentes = [];
  } else {
    fuentes = playlistsDeLaTaxonomia();
  }
  if (flags.has("--guardadas")) fuentes.push(ID_GUARDADAS);

  await sincronizar(fuentes, token, {
    dryRun: flags.has("--dry-run"),
    force: flags.has("--force"),
  });
}

// Un error de configuración es una instrucción para el usuario; solo lo
// inesperado merece stack trace.
main().catch((e) =>
  fatal(e instanceof ErrorDeConfig ? e.message : (e.stack ?? String(e)))
);
