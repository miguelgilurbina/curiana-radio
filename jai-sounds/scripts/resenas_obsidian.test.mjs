import test from "node:test";
import assert from "node:assert/strict";
import { entidadDeSpotify, frontmatter, leerNota, plan } from "./resenas_obsidian.mjs";

const ID = "4NHQUGzhtTLFvgF5SZesLK"; // 22 caracteres, como los de Spotify

test("reconoce enlaces de compartir, con intl y con parámetros, y URIs", () => {
  assert.deepEqual(entidadDeSpotify(`https://open.spotify.com/artist/${ID}?si=abc123`), { entidad: "artista", id: ID });
  assert.deepEqual(entidadDeSpotify(`https://open.spotify.com/intl-es/album/${ID}`), { entidad: "album", id: ID });
  assert.deepEqual(entidadDeSpotify(`spotify:track:${ID}`), { entidad: "cancion", id: ID });
  assert.equal(entidadDeSpotify(`https://open.spotify.com/playlist/${ID}`), null);
  assert.equal(entidadDeSpotify(undefined), null);
});

test("una nota sin estado es borrador", () => {
  const n = leerNota(`---\nspotify: https://open.spotify.com/track/${ID}\n---\nTexto.`, "canciones/x.md");
  assert.equal(n.estado, "borrador");
  assert.equal(n.entidad, "cancion");
});

test("una nota publicada sin texto o con estado raro no sirve", () => {
  assert.match(leerNota(`---\nspotify: spotify:artist:${ID}\nestado: publicada\n---\n   `, "a.md").error, /sin texto/);
  assert.match(leerNota(`---\nspotify: spotify:artist:${ID}\nestado: lista\n---\nhola`, "a.md").error, /borrador o publicada/);
  assert.match(leerNota(`---\nestado: publicada\n---\nhola`, "a.md").error, /falta `spotify:`/);
});

test("el plan sube solo publicadas, avisa duplicados y retira lo despublicado", () => {
  const notas = [
    leerNota(`---\nspotify: spotify:artist:${ID}\nestado: publicada\n---\nUno.`, "artistas/a.md"),
    leerNota(`---\nspotify: spotify:artist:${ID}\nestado: publicada\n---\nDos.`, "artistas/b.md"),
    leerNota(`---\nspotify: spotify:album:${"A".repeat(22)}\nestado: borrador\n---\nAún no.`, "albumes/c.md"),
  ];
  const enBase = [
    { entidad: "artista", entidad_id: ID },
    { entidad: "cancion", entidad_id: "B".repeat(22) },
  ];
  const p = plan(notas, enBase);
  assert.deepEqual(p.subir.map((n) => n.cuerpo), ["Uno."]);
  assert.equal(p.errores.length, 1);
  assert.match(p.errores[0], /duplicada/);
  assert.deepEqual(p.retirar, [{ entidad: "cancion", entidad_id: "B".repeat(22) }]);
});

test("el frontmatter se lee como lo leía gray-matter, y uno sin cierre es ilegible", () => {
  const fm = frontmatter(`﻿---\r\nspotify: spotify:track:${ID}\r\nfecha: 2026-10-08\r\n---\r\nTexto.\r\n`);
  assert.equal(fm.data.spotify, `spotify:track:${ID}`);
  assert.ok(fm.data.fecha instanceof Date);
  assert.equal(fm.content, "Texto.\r\n");
  assert.deepEqual(frontmatter("Sin frontmatter."), { data: {}, content: "Sin frontmatter." });
  assert.deepEqual(frontmatter("---\n---\nCuerpo."), { data: {}, content: "Cuerpo." });
  assert.match(leerNota(`---\nspotify: spotify:artist:${ID}\nTexto sin cierre.`, "a.md").error, /frontmatter ilegible/);
});
