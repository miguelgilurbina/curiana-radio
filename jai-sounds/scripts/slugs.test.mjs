import test from "node:test";
import assert from "node:assert/strict";
import { slugificar } from "./_comun.mjs";
import { asignar, reglas } from "./slugs.mjs";

test("slugificar quita acentos, signos y apóstrofos", () => {
  assert.equal(slugificar("É do Brasil"), "e-do-brasil");
  assert.equal(slugificar("Tony's Gabagool (The Sopranos Playlist)"), "tonys-gabagool-the-sopranos-playlist");
  assert.equal(slugificar("Simon & Garfunkel"), "simon-y-garfunkel");
  assert.equal(slugificar("Richter: On the Nature of Daylight"), "richter-on-the-nature-of-daylight");
});

test("un alfabeto no latino cae al id de Spotify, no a una lectura inventada", () => {
  assert.equal(slugificar("プラスティック・バンブー"), "");
  const [n] = asignar([{ id: "AbC123", name: "プラスティック・バンブー", artista: "Ryuichi Sakamoto" }], [], reglas.cancion.base);
  assert.equal(n.slug, "abc123-ryuichi-sakamoto");
});

test("la canción lleva el apellido de su primer artista", () => {
  const [n] = asignar([{ id: "x", name: "On the Nature of Daylight", artista: "Max Richter" }], [], reglas.cancion.base);
  assert.equal(n.slug, "on-the-nature-of-daylight-max-richter");
});

test("un álbum que choca prueba con el artista y después numera", () => {
  const filas = [
    { id: "a", name: "Greatest Hits", artista: "Queen" },
    { id: "b", name: "Greatest Hits", artista: "ABBA" },
    { id: "c", name: "Greatest Hits", artista: "ABBA" },
  ];
  const s = asignar(filas, [], reglas.album.base, reglas.album.alterna).map((f) => f.slug);
  assert.deepEqual(s, ["greatest-hits", "greatest-hits-abba", "greatest-hits-abba-2"]);
});

test("respeta los slugs ya asignados: los nuevos no los pisan", () => {
  const s = asignar([{ id: "z", name: "Invisible" }], ["invisible"], reglas.artista.base).map((f) => f.slug);
  assert.deepEqual(s, ["invisible-2"]);
});
