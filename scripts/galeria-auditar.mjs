#!/usr/bin/env node
/**
 * Audita las fichas escritas por los subagentes antes de fusionarlas.
 *
 *   node scripts/galeria-auditar.mjs
 *
 * Comprueba lo que un humano no va a revisar a mano en 800 fichas: que no se
 * haya colado el nombre de un artista o de una persona real, que no reaparezcan
 * las muletas que convierten la voz en plantilla, y que los textos quepan donde
 * se van a mostrar.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const SALIDAS = path.join(process.cwd(), ".galeria-trabajo", "descripciones");

/**
 * Los límites de palabra (\b) importan: sin ellos «dali» casa dentro de
 * «sandalias» y «monet» dentro de «monetario». Aprendido a la mala.
 */
const ARTISTAS = new RegExp(
  "\\b(" +
    [
      "giger", "dal[ií]", "kahlo", "picasso", "hopper", "miyazaki", "moebius",
      "rockwell", "vallotton", "van gogh", "monet", "klimt", "escher", "warhol",
      "basquiat", "caravaggio", "rembrandt", "turner", "hokusai", "mucha",
      "beksinski", "bosch", "clapton", "presley", "elvis", "bol[ií]var",
      "manaure", "al estilo de", "in the style of",
    ].join("|") +
    ")\\b",
  "i"
);

const MULETAS = new RegExp(
  "(" +
    [
      "en el pueblo", "nadie pregunta", "nadie cuenta",
      "cada vez que", "cada noche", "cada ma[ñn]ana",
      "\\bm[ií]stic", "\\bet[eé]re", "\\bon[ií]ric", "\\bsurreal",
      "\\bensue[ñn]", "\\binfinit",
    ].join("|") +
    ")",
  "i"
);

const MAX_CONCEPTO = 35;
const MAX_TITULO = 5;

function palabras(s) {
  return s.trim().split(/\s+/).length;
}

async function main() {
  const archivos = (await fs.readdir(SALIDAS))
    .filter((f) => /^salida-.*\.json$/.test(f))
    .sort();

  let n = 0;
  const hallazgos = [];

  for (const archivo of archivos) {
    const fichas = JSON.parse(
      await fs.readFile(path.join(SALIDAS, archivo), "utf-8")
    );
    for (const f of fichas) {
      if (!f.concepto) {
        hallazgos.push([archivo, f.slug, "sin concepto"]);
        continue;
      }
      n++;
      const todo = `${f.titulo} ${f.concepto} ${f.alt}`;
      const art = todo.match(ARTISTAS);
      if (art) hallazgos.push([archivo, f.slug, `nombre propio: «${art[0]}»`]);
      const mul = f.concepto.match(MULETAS);
      if (mul) hallazgos.push([archivo, f.slug, `muleta: «${mul[0]}»`]);
      if (palabras(f.concepto) > MAX_CONCEPTO)
        hallazgos.push([archivo, f.slug, `concepto de ${palabras(f.concepto)} palabras`]);
      if (palabras(f.titulo) > MAX_TITULO)
        hallazgos.push([archivo, f.slug, `título de ${palabras(f.titulo)} palabras`]);
      if (/^una?\s/i.test(f.titulo.trim()))
        hallazgos.push([archivo, f.slug, "título empieza por «Un/Una»"]);
    }
  }

  console.log(`\n${archivos.length} archivo(s) · ${n} fichas auditadas`);
  if (hallazgos.length === 0) {
    console.log("✓ Sin hallazgos.\n");
    return;
  }
  console.log(`\n⚠ ${hallazgos.length} hallazgo(s):`);
  for (const [a, s, motivo] of hallazgos) {
    console.log(`   ${a}  ${s}\n      ${motivo}`);
  }
  console.log("");
}

main().catch((err) => {
  console.error("\n✗ " + (err.stack ?? err) + "\n");
  process.exit(1);
});
