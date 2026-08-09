#!/usr/bin/env node
/**
 * JAI Sounds · ingesta de Spotify → Supabase
 * ---------------------------------------------------------------------
 * Uso, en el orden en que se usa la primera vez:
 *
 *   --login              Consentimiento de Spotify; sesión a ~/.secrets/.
 *   --listar             Todas tus playlists con nombre, id y nº de
 *                        pistas. No escribe nada.
 *   --sync               Las playlists declaradas en moods.json.
 *   --sync <url|id> …    Solo esas.
 *   --sync --todas       Todas las playlists de la cuenta.
 *   --sync --guardadas   "Canciones que te gustan" (/me/tracks).
 *
 * Flags: --dry-run (no escribe)  --force (ignora snapshot_id)
 *
 * ---------------------------------------------------------------------
 * ESTADO DE LA API — verificado en vivo el 2026-08-09 contra la app de
 * este proyecto. Para una app registrada hoy:
 *
 *   VIVOS    /me · /me/tracks · /me/playlists · /playlists/{id}
 *            /playlists/{id}/items · /artists/{id} · /search
 *   MUERTOS  /playlists/{id}/tracks  → 403   (reemplazado por /items)
 *            /tracks?ids=            → 403
 *            /artists?ids=           → 403
 *            /albums/{id}            → 404
 *            /audio-features         → 403   (deprecado 2024-11-27)
 *
 * Consecuencias que NO son bugs de este script:
 *   · El envoltorio de cada elemento de playlist es `item`, no `track`
 *     (en /me/tracks sigue siendo `track` — Spotify es inconsistente).
 *   · El conteo de una playlist está en `items.total`, no `tracks.total`.
 *   · No hay `popularity` ni `genres` en ninguna parte. El álbum y los
 *     artistas se arman de lo EMBEBIDO en cada pista, que trae todo lo
 *     que necesitamos y ahorra las llamadas que además darían 403.
 * ---------------------------------------------------------------------
 *
 * Credenciales — SOLO por variables de entorno, nunca en un archivo del
 * repo (el proyecto vive en OneDrive y se sincronizaría a la nube):
 *   SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
 *   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
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
/** Las tablas viven en su propio esquema, no en public. Ver la migración. */
const ESQUEMA = "jai";
const GUARDADAS = Symbol("canciones-guardadas");

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

function idDePlaylist(entrada) {
  const limpio = entrada.trim();
  const url = limpio.match(/playlist[/:]([A-Za-z0-9]+)/);
  if (url) return url[1];
  if (/^[A-Za-z0-9]{22}$/.test(limpio)) return limpio;
  fatal(`No reconozco esto como playlist de Spotify: "${entrada}"`);
}

// ── Cliente HTTP ─────────────────────────────────────────────────────

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
        "  Endpoint deprecado para apps nuevas. Ver la tabla de endpoints\n" +
        "  vivos/muertos en la cabecera de este archivo."
    );
  }
  if (res.status === 401) {
    fatal(`401 en ${ruta}\n  Token inválido o sin scope. Reintentar --login.`);
  }
  if (!res.ok) fatal(`Spotify ${res.status} en ${ruta}: ${await res.text()}`);
  return res.json();
}

async function paginar(rutaInicial, token, alAvanzar) {
  const items = [];
  let url = rutaInicial;
  while (url) {
    const pagina = await api(url, token);
    items.push(...pagina.items);
    alAvanzar?.(items.length, pagina.total);
    url = pagina.next;
  }
  return items;
}

// ── Lecturas ─────────────────────────────────────────────────────────

async function yo(token) {
  return api("/me", token);
}

async function misPlaylists(token, miId) {
  const crudas = await paginar(`${API}/me/playlists?limit=50`, token);
  return crudas.filter(Boolean).map((p) => ({
    id: p.id,
    name: p.name,
    description: p.description || null,
    image_url: p.images?.[0]?.url ?? null,
    // El conteo migró de `tracks.total` a `items.total`.
    track_count: p.items?.total ?? p.tracks?.total ?? null,
    snapshot_id: p.snapshot_id ?? null,
    colaborativa: p.collaborative ?? null,
    publica: p.public ?? null,
    es_propia: miId ? p.owner?.id === miId : null,
  }));
}

async function traerPlaylist(id, token) {
  const meta = await api(
    `/playlists/${id}?fields=id,name,description,images,snapshot_id,owner(id),public,collaborative,items(total)`,
    token
  );
  // /tracks da 403: el endpoint vivo es /items.
  const items = await paginar(`${API}/playlists/${id}/items?limit=100`, token);
  return { meta, items };
}

async function traerGuardadas(token) {
  log("  · leyendo la biblioteca guardada (puede tardar)…");
  let ultimo = 0;
  const items = await paginar(`${API}/me/tracks?limit=50`, token, (n, total) => {
    if (n - ultimo >= 1000) {
      log(`    ${n}${total ? ` / ${total}` : ""}`);
      ultimo = n;
    }
  });
  return items;
}

// ── Normalización ────────────────────────────────────────────────────

/**
 * De una lista de elementos (de playlist o de biblioteca) saca las cuatro
 * entidades. Todo sale de lo EMBEBIDO: no hay llamadas extra que hacer
 * porque /tracks?ids= y /artists?ids= responden 403.
 */
function normalizar(elementos) {
  const tracks = new Map();
  const albums = new Map();
  const artistas = new Map();
  const trackArtistas = [];
  const albumArtistas = [];
  const posiciones = [];

  elementos.forEach((el, indice) => {
    // Playlists envuelven en `item`; /me/tracks todavía en `track`.
    const t = el?.item ?? el?.track;
    // Pistas locales (sin id), episodios y huecos de canciones borradas.
    if (!t || !t.id || t.type !== "track") return;

    if (!tracks.has(t.id)) {
      const al = t.album;
      if (al?.id && !albums.has(al.id)) {
        albums.set(al.id, {
          id: al.id,
          name: al.name,
          album_type: al.album_type ?? null,
          release_date: al.release_date ?? null,
          release_date_precision: al.release_date_precision ?? null,
          total_tracks: al.total_tracks ?? null,
          image_url: al.images?.[0]?.url ?? null,
        });
        (al.artists ?? []).forEach((a, pos) => {
          if (!a.id) return;
          artistas.set(a.id, { id: a.id, name: a.name });
          albumArtistas.push({ album_id: al.id, artist_id: a.id, position: pos });
        });
      }

      tracks.set(t.id, {
        id: t.id,
        name: t.name,
        album_id: al?.id ?? null,
        disc_number: t.disc_number ?? null,
        track_number: t.track_number ?? null,
        duration_ms: t.duration_ms ?? null,
        isrc: t.external_ids?.isrc ?? null,
        explicit: t.explicit ?? null,
        spotify_url: t.external_urls?.spotify ?? null,
      });

      (t.artists ?? []).forEach((a, pos) => {
        if (!a.id) return;
        artistas.set(a.id, { id: a.id, name: a.name });
        trackArtistas.push({ track_id: t.id, artist_id: a.id, position: pos });
      });
    }

    posiciones.push({
      track_id: t.id,
      position: indice,
      added_at: el.added_at ?? null,
    });
  });

  return { tracks, albums, artistas, trackArtistas, albumArtistas, posiciones };
}

// ── Supabase ─────────────────────────────────────────────────────────

function conectarSupabase() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new ErrorDeConfig(
      "Faltan SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY en el entorno.\n" +
        "  La service_role key es la única que puede escribir (ver RLS en la\n" +
        "  migración). Nunca la pongas en un NEXT_PUBLIC_* ni en un archivo.\n" +
        "  Para solo mirar sin escribir: añadir --dry-run."
    );
  }
  return createClient(url, key, { auth: { persistSession: false } });
}

/**
 * Escritor contra PostgREST. Las tablas viven en el esquema `jai`, no en
 * `public`: hay que pedírselo explícitamente y además exponer el esquema
 * en la config de la API del proyecto.
 */
function escritorSupabase(db) {
  const jai = () => db.schema(ESQUEMA);
  return {
    async upsert(tabla, filas, onConflict) {
      if (filas.length === 0) return;
      for (const lote of trozos(filas, LOTE_UPSERT)) {
        const { error } = await jai().from(tabla).upsert(lote, { onConflict });
        if (error) fatal(`Upsert en ${ESQUEMA}.${tabla}: ${error.message}`);
      }
      log(`  · ${tabla}: ${filas.length}`);
    },
    async consultarSnapshot(id) {
      const { data } = await jai()
        .from("playlists")
        .select("snapshot_id")
        .eq("id", id)
        .maybeSingle();
      return data?.snapshot_id ?? null;
    },
    async cerrar() {},
  };
}

/**
 * Escritor a archivo .sql. Existe porque un Supabase local puede estar
 * corriendo sin publicar puertos al host: entonces PostgREST es
 * inalcanzable pero psql sigue entrando por `docker exec`. Para carga
 * masiva además es más rápido que trocear en upserts de 500.
 *
 * El archivo resultante es portable: sirve para el local de hoy y para
 * producción mañana.
 */
function escritorSQL(ruta) {
  const salida = fs.createWriteStream(ruta, { encoding: "utf-8" });
  salida.write("begin;\n");

  // standard_conforming_strings está activo por defecto: la barra invertida
  // es literal y solo hay que duplicar la comilla simple.
  const lit = (v) => {
    if (v === null || v === undefined) return "NULL";
    if (typeof v === "number") return Number.isFinite(v) ? String(v) : "NULL";
    if (typeof v === "boolean") return v ? "true" : "false";
    return "'" + String(v).replace(/'/g, "''") + "'";
  };

  return {
    async upsert(tabla, filas, onConflict) {
      if (filas.length === 0) return;
      const cols = Object.keys(filas[0]);
      const claves = onConflict.split(",").map((c) => c.trim());
      const actualizables = cols.filter((c) => !claves.includes(c));
      const setter = actualizables.length
        ? actualizables.map((c) => `${c} = excluded.${c}`).join(", ")
        : null;

      for (const lote of trozos(filas, LOTE_UPSERT)) {
        const values = lote
          .map((f) => "(" + cols.map((c) => lit(f[c])).join(",") + ")")
          .join(",\n  ");
        salida.write(
          `insert into ${ESQUEMA}.${tabla} (${cols.join(", ")}) values\n  ${values}\n` +
            `on conflict (${claves.join(", ")}) do ${
              setter ? `update set ${setter}` : "nothing"
            };\n`
        );
      }
      log(`  · ${tabla}: ${filas.length}`);
    },
    cerrar() {
      return new Promise((res, rej) => {
        salida.write("commit;\n");
        salida.end(() => res());
        salida.on("error", rej);
      });
    },
  };
}

/** Escribe las entidades compartidas respetando las claves foráneas. */
async function guardarEntidades(w, n) {
  await w.upsert("artists", [...n.artistas.values()], "id");
  await w.upsert("albums", [...n.albums.values()], "id");
  await w.upsert("album_artists", n.albumArtistas, "album_id,artist_id");
  await w.upsert("tracks", [...n.tracks.values()], "id");
  await w.upsert("track_artists", n.trackArtistas, "track_id,artist_id");
}

// ── Modos ────────────────────────────────────────────────────────────

async function listar(token, miId) {
  const listas = await misPlaylists(token, miId);
  const propias = listas.filter((p) => p.es_propia);
  const total = listas.reduce((s, p) => s + (p.track_count ?? 0), 0);
  const totalPropias = propias.reduce((s, p) => s + (p.track_count ?? 0), 0);

  log(`\n${listas.length} playlists · ${total} pistas`);
  log(`  de las cuales tuyas: ${propias.length} · ${totalPropias} pistas\n`);

  for (const p of [...listas].sort((a, b) => (b.track_count ?? 0) - (a.track_count ?? 0))) {
    const marca = p.es_propia ? " " : "~";
    log(`${marca} ${String(p.track_count ?? "?").padStart(5)}  ${p.name}`);
    log(`          ${p.id}`);
  }
  log("\n(~ = seguida, no tuya)\n");
}

async function sincronizar(fuentes, token, { dryRun, force, miId, sqlOut }) {
  const db =
    dryRun ? null
    : sqlOut ? escritorSQL(sqlOut)
    : escritorSupabase(conectarSupabase());
  let pistasTotales = 0;

  for (const fuente of fuentes) {
    if (fuente === GUARDADAS) {
      log(`\n▸ Canciones que te gustan`);
      const elementos = await traerGuardadas(token);
      const n = normalizar(elementos);
      log(
        `  ${n.tracks.size} pistas · ${n.albums.size} álbumes · ${n.artistas.size} artistas`
      );
      pistasTotales += n.tracks.size;
      if (dryRun) {
        log("  · [dry-run] nada escrito");
        continue;
      }
      await guardarEntidades(db, n);
      await db.upsert(
        "saved_tracks",
        n.posiciones.map(({ track_id, added_at }) => ({ track_id, added_at })),
        "track_id"
      );
      continue;
    }

    log(`\n▸ ${fuente}`);
    const { meta, items } = await traerPlaylist(fuente, token);
    log(`  ${meta.name} — ${items.length} elementos`);

    // Saltar lo no cambiado exige consultar, y el escritor a .sql no puede:
    // genera SQL a ciegas. Solo aplica cuando escribimos por PostgREST.
    if (!force && db?.consultarSnapshot && meta.snapshot_id) {
      const previo = await db.consultarSnapshot(meta.id);
      if (previo === meta.snapshot_id) {
        log("  · sin cambios desde la última ingesta — salto");
        continue;
      }
    }

    const n = normalizar(items);
    const descartados = items.length - n.posiciones.length;
    if (descartados > 0) {
      log(`  · ${descartados} descartados (locales, episodios o borrados)`);
    }
    pistasTotales += n.tracks.size;

    if (dryRun) {
      log(`  · [dry-run] ${n.tracks.size} pistas, ${n.artistas.size} artistas`);
      continue;
    }

    await guardarEntidades(db, n);
    await db.upsert(
      "playlists",
      [
        {
          id: meta.id,
          name: meta.name,
          description: meta.description || null,
          image_url: meta.images?.[0]?.url ?? null,
          track_count: meta.items?.total ?? null,
          snapshot_id: meta.snapshot_id ?? null,
          colaborativa: meta.collaborative ?? null,
          publica: meta.public ?? null,
          es_propia: miId ? meta.owner?.id === miId : null,
        },
      ],
      "id"
    );
    await db.upsert(
      "playlist_tracks",
      n.posiciones.map((e) => ({ ...e, playlist_id: meta.id })),
      "playlist_id,track_id"
    );
  }

  await db?.cerrar();
  if (sqlOut) log(`\n· SQL escrito en ${sqlOut}`);

  log(`\n✓ ${pistasTotales} pistas procesadas.\n`);
}

// ── Entrada ──────────────────────────────────────────────────────────

function playlistsDeLaTaxonomia() {
  if (!fs.existsSync(TAXONOMIA)) fatal(`No encuentro ${TAXONOMIA}`);
  const { moods } = JSON.parse(fs.readFileSync(TAXONOMIA, "utf-8"));
  const ids = [...new Set(moods.flatMap((m) => m.playlists ?? []))];
  if (ids.length === 0) {
    throw new ErrorDeConfig(
      "Ningún mood declara playlists todavía.\n" +
        "  Correr primero: --listar   (y llenar el campo `playlists`)\n" +
        "  O ingestar todo de una:    --sync --todas --guardadas"
    );
  }
  return ids;
}

async function main() {
  const argv = process.argv.slice(2);

  // --sql lleva valor: hay que sacarlo ANTES de calcular los sueltos, o la
  // ruta de salida se colaría en la lista de playlists a ingestar.
  let sqlOut = null;
  const resto = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--sql") {
      sqlOut = argv[++i];
      if (!sqlOut || sqlOut.startsWith("--")) {
        throw new ErrorDeConfig("--sql necesita una ruta de archivo de salida.");
      }
    } else {
      resto.push(argv[i]);
    }
  }

  const flags = new Set(resto.filter((a) => a.startsWith("--")));
  const sueltos = resto.filter((a) => !a.startsWith("--"));

  if (flags.has("--login")) {
    await login();
    log("Siguiente: node jai-sounds/scripts/ingest_spotify.mjs --listar\n");
    return;
  }

  const modos = ["--listar", "--sync"].filter((m) => flags.has(m));
  if (modos.length !== 1) {
    throw new ErrorDeConfig(
      "Elegí un modo: --login, --listar o --sync.\n" +
        "  Ver la cabecera del archivo para el flujo completo."
    );
  }
  const modo = modos[0];

  const conUsuario = haySesion();
  const necesitaUsuario =
    modo === "--listar" || flags.has("--todas") || flags.has("--guardadas");
  if (!conUsuario && necesitaUsuario) {
    throw new ErrorDeConfig(
      "Eso necesita sesión de usuario.\n" +
        "  Correr primero: node jai-sounds/scripts/ingest_spotify.mjs --login"
    );
  }

  const token = conUsuario ? await tokenDeUsuario() : await tokenDeApp();
  const miId = conUsuario ? (await yo(token)).id : null;
  if (!conUsuario) log("· Sin sesión de usuario: solo playlists públicas por id.");

  if (modo === "--listar") return listar(token, miId);

  let fuentes;
  if (flags.has("--todas")) {
    fuentes = (await misPlaylists(token, miId)).map((p) => p.id);
    log(`· ${fuentes.length} playlists en la cuenta.`);
  } else if (sueltos.length > 0) {
    fuentes = sueltos.map(idDePlaylist);
  } else if (flags.has("--guardadas")) {
    fuentes = [];
  } else {
    fuentes = playlistsDeLaTaxonomia();
  }
  if (flags.has("--guardadas")) fuentes.push(GUARDADAS);

  await sincronizar(fuentes, token, {
    dryRun: flags.has("--dry-run"),
    force: flags.has("--force"),
    miId,
    sqlOut,
  });
}

main().catch((e) =>
  fatal(e instanceof ErrorDeConfig ? e.message : (e.stack ?? String(e)))
);
