/**
 * Lo que comparten los scripts del wiki de JAI Sounds: la conexión, la
 * lectura paginada, el upsert por lotes y el slug.
 *
 * Credenciales SOLO por entorno, igual que la ingesta:
 *   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
 * (`source ~/.secrets/jai.env` antes de correr). Nunca en un archivo del
 * repo: el proyecto vive en OneDrive y el repo es público.
 */
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createClient } from "@supabase/supabase-js";

export const ESQUEMA = "jai";
export const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
/** Cachés de consultas a terceros: fuera del repo y fuera de OneDrive. */
export const CACHE_DIR = path.join(os.homedir(), ".cache", "jai-sounds");

export const log = (...a) => console.log(...a);
export function fatal(msg) {
  console.error(`\n✗ ${msg}\n`);
  process.exit(1);
}

/** true si el módulo se está ejecutando como script (no importado por un test). */
export function esPrincipal(importMetaUrl) {
  return process.argv[1] && importMetaUrl === pathToFileURL(process.argv[1]).href;
}

export function trozos(arr, n) {
  const out = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}

export function conectar() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    fatal(
      "Faltan SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY en el entorno.\n" +
        "  `source ~/.secrets/jai.env` antes de correr. La service_role key\n" +
        "  nunca va en un NEXT_PUBLIC_* ni en un archivo del repo."
    );
  }
  return createClient(url, key, { auth: { persistSession: false } }).schema(ESQUEMA);
}

/** Todas las filas de una consulta, de 1000 en 1000 (el tope de PostgREST). */
export async function todas(consulta) {
  const filas = [];
  for (let desde = 0; ; desde += 1000) {
    const { data, error } = await consulta().range(desde, desde + 999);
    if (error) fatal(error.message);
    filas.push(...data);
    if (data.length < 1000) return filas;
  }
}

export async function upsert(db, tabla, filas, onConflict) {
  for (const lote of trozos(filas, 500)) {
    const { error } = await db.from(tabla).upsert(lote, { onConflict });
    if (error) fatal(`Upsert en ${ESQUEMA}.${tabla}: ${error.message}`);
  }
  if (filas.length) log(`  · ${tabla}: ${filas.length}`);
}

/** Las canciones del dial: las de las playlists marcadas en_dial. */
export async function idsDelDial(db) {
  const dial = await todas(() => db.from("playlists").select("id").eq("en_dial", true));
  if (dial.length === 0) {
    fatal("No hay estaciones marcadas en el dial. Correr antes:\n  node jai-sounds/scripts/ingest_spotify.mjs --sync --dial");
  }
  // Con orden: paginar sin él puede saltarse o repetir filas entre páginas.
  const filas = await todas(() =>
    db.from("playlist_tracks").select("track_id").in("playlist_id", dial.map((p) => p.id)).order("playlist_id").order("track_id")
  );
  return [...new Set(filas.map((f) => f.track_id))];
}

/**
 * Slug de URL: minúsculas, sin acentos, guiones. Los alfabetos que no son
 * latinos (音の旅) no tienen transliteración honesta: devuelven "" y quien
 * llama decide el respaldo.
 */
export function slugificar(texto) {
  return (texto ?? "")
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/&/g, " y ")
    .replace(/['’]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80)
    .replace(/-+$/g, "");
}

/** Caché JSON en disco con guardado periódico. */
export function cacheEnDisco(nombre) {
  fs.mkdirSync(CACHE_DIR, { recursive: true });
  const ruta = path.join(CACHE_DIR, nombre);
  const datos = fs.existsSync(ruta) ? JSON.parse(fs.readFileSync(ruta, "utf8")) : {};
  let sucios = 0;
  const guardar = () => {
    fs.writeFileSync(ruta, JSON.stringify(datos));
    sucios = 0;
  };
  return {
    ruta,
    datos,
    marcar() {
      if (++sucios >= 20) guardar();
    },
    guardar,
  };
}
