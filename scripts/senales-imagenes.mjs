#!/usr/bin/env node
/**
 * Las imágenes de una señal: de la foto de Miguel a Vercel Blob.
 *
 *   node scripts/senales-imagenes.mjs <slug> <imagen...> [--env <archivo>]
 *
 * Cada imagen sale en WebP (1600 px de ancho como máximo, nunca se amplía) y
 * se sube a `senales/<slug>/<nombre>.webp`. Al final imprime lo que hay que
 * pegar en la señal: el bloque `portada:` del frontmatter o un <Figura />.
 *
 * Las imágenes no van al repo (sincroniza a OneDrive), igual que la galería.
 * El token tampoco: se pasa por variable de entorno o con --env apuntando a
 * un archivo FUERA del repo (ver GALERIA.md, «Credenciales»).
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import sharp from "sharp";

const ANCHO_MAX = 1600;
const CALIDAD = 80;
// HEIC (las fotos del iPhone) no: sharp no trae el decodificador HEVC. Se
// exporta antes a JPG.
const EXTENSIONES = new Set([".png", ".jpg", ".jpeg", ".webp", ".avif", ".tif", ".tiff"]);

function salir(mensaje) {
  console.error(`\n✗ ${mensaje}\n`);
  process.exit(1);
}

/** El archivo de `vercel env pull`, leído sin pisar lo que ya está en el entorno. */
async function cargarEnv(ruta) {
  let texto;
  try {
    texto = await fs.readFile(ruta, "utf-8");
  } catch {
    salir(`No pude leer el archivo de entorno: ${ruta}`);
  }
  for (const linea of texto.split(/\r?\n/)) {
    const limpia = linea.trim();
    if (!limpia || limpia.startsWith("#")) continue;
    const i = limpia.indexOf("=");
    if (i === -1) continue;
    const clave = limpia.slice(0, i).trim();
    const valor = limpia.slice(i + 1).trim().replace(/^["']|["']$/g, "");
    if (!process.env[clave]) process.env[clave] = valor;
  }
}

/** «Foto del Médano (2).JPG» → «foto-del-medano-2» */
function nombreLimpio(archivo) {
  return path
    .basename(archivo, path.extname(archivo))
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

async function main() {
  const args = process.argv.slice(2);
  const opciones = { env: null };
  const posicionales = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--env") opciones.env = args[++i];
    else posicionales.push(args[i]);
  }
  const [slug, ...imagenes] = posicionales;
  if (!slug || !imagenes.length) {
    salir("Uso: node scripts/senales-imagenes.mjs <slug> <imagen...> [--env <archivo>]");
  }
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) salir(`El slug va en minúsculas con guiones: «${slug}»`);
  for (const img of imagenes) {
    const ext = path.extname(img).toLowerCase();
    if (ext === ".heic" || ext === ".heif") salir(`HEIC no se puede leer aquí: expórtala a JPG primero (${img})`);
    if (!EXTENSIONES.has(ext)) salir(`No sé leer este formato: ${img}`);
    try {
      await fs.access(img);
    } catch {
      salir(`No existe: ${img}`);
    }
  }

  if (opciones.env) await cargarEnv(opciones.env);
  const tieneRW = Boolean(process.env.BLOB_READ_WRITE_TOKEN);
  const tieneOidc = Boolean(process.env.VERCEL_OIDC_TOKEN && process.env.BLOB_STORE_ID);
  if (!tieneRW && !tieneOidc) {
    salir(
      "No hay credenciales de Blob en el entorno. Las mismas de la galería:\n" +
        '    vercel env pull "$env:TEMP\\curiana-blob.env"\n' +
        '    node scripts/senales-imagenes.mjs <slug> <imagen...> --env "$env:TEMP\\curiana-blob.env"\n' +
        "  Siempre fuera del repo: esta carpeta sincroniza a OneDrive.",
    );
  }
  const { put } = await import("@vercel/blob");

  const subidas = [];
  for (const img of imagenes) {
    const nombre = nombreLimpio(img);
    // rotate() sin argumentos respeta la orientación EXIF de las fotos del teléfono
    const { data, info } = await sharp(img)
      .rotate()
      .resize({ width: ANCHO_MAX, withoutEnlargement: true })
      .webp({ quality: CALIDAD })
      .toBuffer({ resolveWithObject: true });
    const blob = await put(`senales/${slug}/${nombre}.webp`, data, {
      access: "public",
      contentType: "image/webp",
      addRandomSuffix: false,
      allowOverwrite: true,
      cacheControlMaxAge: 31536000,
    });
    subidas.push({ nombre, url: blob.url, ancho: info.width, alto: info.height, kb: Math.round(data.length / 1024) });
    console.log(`  ✓ ${nombre}.webp · ${info.width}×${info.height} · ${Math.round(data.length / 1024)} KB`);
  }

  console.log("\nComo portada (en el frontmatter):\n");
  console.log(`portada:\n  src: ${subidas[0].url}\n  alt: "…"\n  pie: "…"`);
  console.log("\nDentro del texto:\n");
  for (const s of subidas) console.log(`<Figura src="${s.url}" alt="…" pie="…" />`);
  console.log("");
}

main().catch((err) => salir(err.message));
