#!/usr/bin/env node
/**
 * JAI Sounds · las reseñas, desde Obsidian
 * ---------------------------------------------------------------------
 * La voz de JAI se escribe en el vault de Miguel, FUERA del repo (que es
 * público): ~/OneDrive/Documents/Obsidian Vault/JAI Sounds/. Cada nota es
 * una reseña de un artista, un álbum o una canción:
 *
 *   ---
 *   spotify: https://open.spotify.com/artist/…    ← el enlace de «Compartir»
 *   estado: borrador                                ← o: publicada
 *   ---
 *   El texto de la reseña, en markdown.
 *
 * Solo sube lo `publicada`. Un borrador no sale nunca del vault (y si por
 * error llegara a la base, el público igual no lo vería: RLS).
 *
 * Uso:
 *   node jai-sounds/scripts/resenas_obsidian.mjs                 sube las publicadas
 *   node jai-sounds/scripts/resenas_obsidian.mjs --retirar       además baja de la
 *        base las que ya no están publicadas en el vault
 *   node jai-sounds/scripts/resenas_obsidian.mjs --nueva <enlace de Spotify>
 *        crea la nota en su carpeta, en borrador, con el nombre ya puesto
 *   --dry-run   muestra lo que haría
 *
 * Otro vault: variable de entorno JAI_VAULT.
 */
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import matter from "gray-matter";
import { conectar, esPrincipal, fatal, log, slugificar, todas, upsert } from "./_comun.mjs";

export const VAULT = process.env.JAI_VAULT ?? path.join(os.homedir(), "OneDrive", "Documents", "Obsidian Vault", "JAI Sounds");
const TIPOS = { artist: "artista", album: "album", track: "cancion" };
export const CARPETAS = { artista: "artistas", album: "albumes", cancion: "canciones" };
const TABLAS = { artista: "artists", album: "albums", cancion: "tracks" };

/** Del enlace o URI de Spotify, la entidad: {entidad, id} o null. */
export function entidadDeSpotify(ref) {
  const s = String(ref ?? "").trim();
  const m = s.match(/open\.spotify\.com\/(?:intl-[a-z]{2}(?:-[a-z]{2})?\/)?(artist|album|track)\/([A-Za-z0-9]{22})/) ?? s.match(/^spotify:(artist|album|track):([A-Za-z0-9]{22})$/);
  return m ? { entidad: TIPOS[m[1]], id: m[2] } : null;
}

/** Lee una nota. Devuelve la reseña o el motivo por el que no sirve. */
export function leerNota(texto, ruta) {
  let fm;
  try {
    fm = matter(texto);
  } catch (e) {
    return { ruta, error: `frontmatter ilegible: ${e.message}` };
  }
  const ent = entidadDeSpotify(fm.data.spotify);
  if (!ent) return { ruta, error: "falta `spotify:` con el enlace de Spotify del artista, álbum o canción" };
  const estado = String(fm.data.estado ?? "borrador").trim().toLowerCase();
  if (!["borrador", "publicada"].includes(estado)) return { ruta, error: `estado «${fm.data.estado}»: tiene que ser borrador o publicada` };
  const cuerpo = fm.content.trim();
  if (estado === "publicada" && !cuerpo) return { ruta, error: "publicada pero sin texto" };
  return { ruta, ...ent, estado, cuerpo };
}

/**
 * Qué subir y qué retirar. `enBase` son las filas publicadas de jai.resenas.
 * Dos notas para la misma entidad es un error: no se elige por Miguel.
 */
export function plan(notas, enBase) {
  const errores = notas.filter((n) => n.error).map((n) => `${n.ruta}: ${n.error}`);
  const publicadas = notas.filter((n) => !n.error && n.estado === "publicada");
  const porClave = new Map();
  for (const n of publicadas) {
    const k = `${n.entidad}:${n.id}`;
    if (porClave.has(k)) errores.push(`${n.ruta}: reseña duplicada de ${porClave.get(k).ruta}`);
    else porClave.set(k, n);
  }
  const retirar = enBase.filter((f) => !porClave.has(`${f.entidad}:${f.entidad_id}`));
  return { subir: [...porClave.values()], retirar, errores };
}

function listarNotas(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true, recursive: true })
    .filter((e) => e.isFile() && e.name.endsWith(".md") && !e.name.startsWith("_") && e.name !== "LEEME.md")
    .map((e) => path.join(e.parentPath ?? e.path, e.name));
}

async function nueva(ref, seco) {
  const ent = entidadDeSpotify(ref);
  if (!ent) fatal("Eso no es un enlace de Spotify de artista, álbum o canción.");
  const tipoSpotify = Object.keys(TIPOS).find((k) => TIPOS[k] === ent.entidad);
  const o = await (await fetch(`https://open.spotify.com/oembed?url=${encodeURIComponent(`https://open.spotify.com/${tipoSpotify}/${ent.id}`)}`)).json().catch(() => ({}));
  const titulo = o.title ?? ent.id;
  const dir = path.join(VAULT, CARPETAS[ent.entidad]);
  const archivo = path.join(dir, `${slugificar(titulo) || ent.id}.md`);
  if (fs.existsSync(archivo)) fatal(`Ya existe: ${archivo}`);
  const texto = `---\nspotify: https://open.spotify.com/${tipoSpotify}/${ent.id}\nestado: borrador\n---\n\n<!-- ${titulo}. Escribe aquí la reseña. Cambia a «estado: publicada» cuando quieras que salga. -->\n`;
  if (seco) return log(`[dry-run] crearía ${archivo}`);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(archivo, texto, "utf8");
  log(`✓ ${archivo}`);
}

async function main() {
  const argv = process.argv.slice(2);
  const seco = argv.includes("--dry-run");
  const i = argv.indexOf("--nueva");
  if (i >= 0) return nueva(argv[i + 1], seco);

  const archivos = listarNotas(VAULT);
  log(`▸ ${archivos.length} notas en ${VAULT}`);
  const notas = archivos.map((a) => leerNota(fs.readFileSync(a, "utf8"), path.relative(VAULT, a)));

  const db = conectar();
  const enBase = await todas(() => db.from("resenas").select("entidad, entidad_id, publicada_en").eq("estado", "publicada"));
  const { subir, retirar, errores } = plan(notas, enBase);
  errores.forEach((e) => log(`  ⚠ ${e}`));

  // Una reseña de algo que no está en el catálogo no tiene página donde vivir.
  const existentes = {};
  for (const ent of Object.keys(TABLAS)) {
    const ids = subir.filter((n) => n.entidad === ent).map((n) => n.id);
    if (!ids.length) continue;
    const { data, error } = await db.from(TABLAS[ent]).select("id").in("id", ids);
    if (error) fatal(error.message);
    data.forEach((r) => (existentes[`${ent}:${r.id}`] = true));
  }
  const fuera = subir.filter((n) => !existentes[`${n.entidad}:${n.id}`]);
  fuera.forEach((n) => log(`  ⚠ ${n.ruta}: no está en el catálogo del dial (no tendría página); no se sube`));
  const listas = subir.filter((n) => existentes[`${n.entidad}:${n.id}`]);

  const antes = new Map(enBase.map((f) => [`${f.entidad}:${f.entidad_id}`, f.publicada_en]));
  const ahora = new Date().toISOString();
  const filas = listas.map((n) => ({
    entidad: n.entidad,
    entidad_id: n.id,
    cuerpo: n.cuerpo,
    estado: "publicada",
    publicada_en: antes.get(`${n.entidad}:${n.id}`) ?? ahora,
    actualizada_en: ahora,
    nota: n.ruta.replace(/\\/g, "/"),
  }));
  log(`  publicadas: ${filas.length} · por retirar: ${retirar.length}${argv.includes("--retirar") ? "" : " (sin --retirar, se dejan)"}`);
  if (seco) return log("\n[dry-run] nada escrito.\n");

  await upsert(db, "resenas", filas, "entidad,entidad_id");
  if (argv.includes("--retirar") && retirar.length) {
    // Un vault mal configurado se ve vacío: nunca se baja todo por eso.
    if (archivos.length === 0) fatal(`El vault está vacío o no existe (${VAULT}). No retiro nada.`);
    for (const f of retirar) {
      const { error } = await db.from("resenas").delete().eq("entidad", f.entidad).eq("entidad_id", f.entidad_id);
      if (error) fatal(error.message);
    }
    log(`  · retiradas: ${retirar.length}`);
  }
  log("\n✓ reseñas al día.\n");
}

if (esPrincipal(import.meta.url)) await main();
