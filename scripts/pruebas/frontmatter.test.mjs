// lib/frontmatter.ts, el lector de frontmatter que reemplazó a gray-matter.
// Node (≥ 22.18) importa el .ts directo: le quita los tipos al cargarlo.
//   npm run pruebas
import test from "node:test";
import assert from "node:assert/strict";
import { leerFrontmatter } from "../../lib/frontmatter.ts";
import { frontmatter as copiaDeJai } from "../../jai-sounds/scripts/resenas_obsidian.mjs";

const CASOS = {
  "una señal": "---\ntitulo: Primera señal\nfecha: 2026-10-03\naristas: [kaketiana]\nportada:\n  src: https://x.public.blob.vercel-storage.com/a.webp\n  alt: Un médano\n---\n\nEl cuerpo.\n",
  "con BOM y CRLF": "﻿---\r\ntipo: reconstruido\r\n---\r\nVoz de Manaure.\r\n",
  "sin frontmatter": "# Sólo cuerpo\n\nTexto.",
  "bloque vacío": "---\n---\nCuerpo.",
  "sólo comentarios": "---\n# nada aún\n---\nCuerpo.",
  "un «---» más adelante es cuerpo": "---\na: 1\n---\nUno.\n\n---\n\nDos.",
  "«----» no abre": "----\na: 1\n----\nCuerpo.",
};

test("lee el bloque YAML y deja el cuerpo desde la línea siguiente al cierre", () => {
  const { data, content } = leerFrontmatter(CASOS["una señal"]);
  assert.equal(data.titulo, "Primera señal");
  assert.ok(data.fecha instanceof Date, "una fecha sin comillas llega como Date, como con gray-matter");
  assert.equal(data.fecha.toISOString().slice(0, 10), "2026-10-03");
  assert.deepEqual(data.aristas, ["kaketiana"]);
  assert.equal(data.portada.alt, "Un médano");
  assert.equal(content, "\nEl cuerpo.\n");
});

test("BOM, CRLF, sin frontmatter, bloque vacío y un «---» en el cuerpo", () => {
  assert.deepEqual(leerFrontmatter(CASOS["con BOM y CRLF"]), { data: { tipo: "reconstruido" }, content: "Voz de Manaure.\r\n" });
  assert.deepEqual(leerFrontmatter(CASOS["sin frontmatter"]), { data: {}, content: CASOS["sin frontmatter"] });
  assert.deepEqual(leerFrontmatter(CASOS["bloque vacío"]), { data: {}, content: "Cuerpo." });
  assert.deepEqual(leerFrontmatter(CASOS["sólo comentarios"]), { data: {}, content: "Cuerpo." });
  assert.deepEqual(leerFrontmatter(CASOS["un «---» más adelante es cuerpo"]), { data: { a: 1 }, content: "Uno.\n\n---\n\nDos." });
  assert.deepEqual(leerFrontmatter(CASOS["«----» no abre"]), { data: {}, content: CASOS["«----» no abre"] });
});

test("sin cierre, o si no es un mapa, falla en vez de leer un archivo vacío", () => {
  assert.throws(() => leerFrontmatter("---\ntitulo: x\nY el cuerpo."), /no tiene «---» de cierre/);
  assert.throws(() => leerFrontmatter("---\n- uno\n- dos\n---\nCuerpo."), /mapa clave: valor/);
  assert.throws(() => leerFrontmatter("---\nsolo texto\n---\nCuerpo."), /mapa clave: valor/);
});

test("YAML seguro: los tipos !!js/* de js-yaml 3 no existen", () => {
  assert.throws(() => leerFrontmatter('---\nf: !!js/function "function () { return 1 }"\n---\n'), /unknown tag/);
});

test("la copia de jai-sounds/scripts/resenas_obsidian.mjs lee igual", () => {
  for (const [nombre, texto] of Object.entries(CASOS)) {
    assert.deepEqual(copiaDeJai(texto), leerFrontmatter(texto), nombre);
  }
});
