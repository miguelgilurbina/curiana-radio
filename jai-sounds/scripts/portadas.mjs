#!/usr/bin/env node
/**
 * JAI Sounds · las portadas del dial
 * ---------------------------------------------------------------------
 * Las 23 portadas son arte propio de Miguel: viven en el repo, no se
 * enlazan a Spotify. Este script las baja una vez a 640px, las guarda como
 * webp en public/jai/portadas/<slug>.webp y llena `portada` en
 * content/jai-sounds/playlists.json.
 *
 * No pide credenciales: el oEmbed público de Spotify devuelve la portada
 * (a 300px; la misma imagen existe a 640 cambiando el prefijo del tamaño).
 *
 * Uso:  node jai-sounds/scripts/portadas.mjs [--force]
 *   --force   vuelve a bajar las que ya están (si cambiaste una en Spotify)
 */
import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";
import { RAIZ, esPrincipal, fatal, log } from "./_comun.mjs";

const DIAL = path.join(RAIZ, "content", "jai-sounds", "playlists.json");
const DESTINO = path.join(RAIZ, "public", "jai", "portadas");

/** De la miniatura de 300px, la misma imagen a 640 (portadas propias de playlist). */
export function a640(url) {
  return url.replace("ab67706c0000da84", "ab67706c0000bebb");
}

/**
 * Pone la portada en la línea de su playlist sin reformatear el archivo:
 * playlists.json va una playlist por línea a propósito, para que el diff
 * de una edición se lea de un vistazo.
 */
export function conPortada(texto, slug, ruta) {
  return texto
    .split("\n")
    .map((l) => (l.includes(`"slug": "${slug}"`) ? l.replace(/"portada": (null|"[^"]*")/, `"portada": "${ruta}"`) : l))
    .join("\n");
}

async function main() {
  const force = process.argv.includes("--force");
  let texto = fs.readFileSync(DIAL, "utf8");
  const { playlists } = JSON.parse(texto);
  fs.mkdirSync(DESTINO, { recursive: true });

  for (const p of playlists) {
    const archivo = path.join(DESTINO, `${p.slug}.webp`);
    const ruta = `/jai/portadas/${p.slug}.webp`;
    if (fs.existsSync(archivo) && !force) {
      texto = conPortada(texto, p.slug, ruta);
      continue;
    }
    const o = await (await fetch(`https://open.spotify.com/oembed?url=${encodeURIComponent(`https://open.spotify.com/playlist/${p.spotify_id}`)}`)).json();
    if (!o.thumbnail_url) fatal(`Sin portada en Spotify: ${p.nombre}`);
    let r = await fetch(a640(o.thumbnail_url));
    if (!r.ok) r = await fetch(o.thumbnail_url);
    const img = Buffer.from(await r.arrayBuffer());
    await sharp(img).resize(640, 640, { fit: "cover" }).webp({ quality: 82 }).toFile(archivo);
    texto = conPortada(texto, p.slug, ruta);
    log(`  · ${p.slug} (${Math.round(fs.statSync(archivo).size / 1024)} KB)`);
  }
  JSON.parse(texto); // que siga siendo JSON válido
  fs.writeFileSync(DIAL, texto, "utf8");
  log(`\n✓ ${playlists.length} portadas en public/jai/portadas.\n`);
}

if (esPrincipal(import.meta.url)) await main();
