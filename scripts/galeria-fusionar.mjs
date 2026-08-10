#!/usr/bin/env node
/**
 * Vuelca las fichas escritas por los subagentes al manifest.
 *
 *   node scripts/galeria-fusionar.mjs [--dry-run]
 *
 * Cada subagente escribe su propio `salida-NN.json` porque son decenas
 * corriendo a la vez y todos escribiendo el mismo obras.json lo corromperían.
 * Este script es el único que toca el manifest, y corre una sola vez al final.
 *
 * Es idempotente: se puede correr con la mitad de los lotes listos, y otra vez
 * cuando lleguen los demás.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const RAIZ = process.cwd();
const MANIFEST = path.join(RAIZ, "content", "galeria", "obras.json");
const SALIDAS = path.join(RAIZ, ".galeria-trabajo", "descripciones");

const MAX_PALABRAS_CONCEPTO = 35;
const MAX_PALABRAS_TITULO = 5;

function palabras(s) {
  return s.trim().split(/\s+/).length;
}

async function main() {
  const dryRun = process.argv.includes("--dry-run");

  const manifest = JSON.parse(await fs.readFile(MANIFEST, "utf-8"));
  const porSlug = new Map(manifest.obras.map((o) => [o.slug, o]));

  const archivos = (await fs.readdir(SALIDAS))
    .filter((f) => /^salida-.*\.json$/.test(f))
    .sort();

  if (archivos.length === 0) {
    console.error("\n✗ No hay ningún salida-*.json en " + SALIDAS + "\n");
    process.exit(1);
  }

  let escritas = 0;
  const avisos = [];
  const vistos = new Set();

  for (const archivo of archivos) {
    let fichas;
    try {
      fichas = JSON.parse(await fs.readFile(path.join(SALIDAS, archivo), "utf-8"));
    } catch (err) {
      avisos.push(`${archivo}: JSON ilegible (${err.message})`);
      continue;
    }
    if (!Array.isArray(fichas)) {
      avisos.push(`${archivo}: se esperaba un array`);
      continue;
    }

    for (const f of fichas) {
      const obra = porSlug.get(f.slug);
      if (!obra) {
        avisos.push(`${archivo}: slug desconocido «${f.slug}»`);
        continue;
      }
      if (f.error || !f.titulo || !f.concepto || !f.alt) {
        avisos.push(`${archivo}: ${f.slug} sin ficha completa`);
        continue;
      }
      // Dos lotes no deberían cubrir la misma obra; si pasa, gana el primero
      // y se avisa, en vez de sobrescribir en silencio.
      if (vistos.has(f.slug)) {
        avisos.push(`${f.slug}: duplicado entre lotes, conservo el primero`);
        continue;
      }
      vistos.add(f.slug);

      // El límite de palabras no es cosmético: el concepto se lee bajo la obra
      // en el mosaico y una frase larga rompe la altura de la fila.
      if (palabras(f.concepto) > MAX_PALABRAS_CONCEPTO) {
        avisos.push(`${f.slug}: concepto de ${palabras(f.concepto)} palabras`);
      }
      if (palabras(f.titulo) > MAX_PALABRAS_TITULO) {
        avisos.push(`${f.slug}: título de ${palabras(f.titulo)} palabras`);
      }

      obra.titulo = f.titulo.trim();
      obra.concepto = f.concepto.trim();
      obra.alt = f.alt.trim();
      escritas++;
    }
  }

  if (!dryRun) {
    await fs.writeFile(MANIFEST, JSON.stringify(manifest, null, 2) + "\n", "utf-8");
  }

  const sinDescribir = manifest.obras.filter(
    (o) => o.anchos?.length > 0 && !o.concepto?.trim()
  ).length;

  console.log(`\n${dryRun ? "[dry-run] " : ""}${archivos.length} archivo(s) de salida`);
  console.log(`✓ ${escritas} fichas escritas`);
  console.log(`  quedan sin describir: ${sinDescribir}`);
  if (avisos.length > 0) {
    console.log(`\n⚠ ${avisos.length} aviso(s):`);
    for (const a of avisos.slice(0, 20)) console.log(`   ${a}`);
  }
  console.log("");
}

main().catch((err) => {
  console.error("\n✗ " + (err.stack ?? err) + "\n");
  process.exit(1);
});
