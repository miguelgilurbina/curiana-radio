// lib/youtube.ts: lo que sale de idYouTube va directo al src del iframe del
// <Video> de las señales, así que sólo puede salir un id de 11 caracteres.
//   npm run pruebas
import test from "node:test";
import assert from "node:assert/strict";
import { idYouTube } from "../../lib/youtube.ts";

const ID = "dQw4w9WgXcQ";

test("un id suelto pasa tal cual", () => {
  assert.equal(idYouTube(ID), ID);
  assert.equal(idYouTube(`  ${ID}\n`), ID);
  assert.equal(idYouTube("a-b_c-d_e-f"), "a-b_c-d_e-f");
});

test("de cada URL de YouTube sale el id", () => {
  for (const url of [
    `https://www.youtube.com/watch?v=${ID}`,
    `https://www.youtube.com/watch?feature=share&v=${ID}&t=42s`,
    `https://m.youtube.com/watch?v=${ID}`,
    `https://music.youtube.com/watch?v=${ID}`,
    `https://youtu.be/${ID}`,
    `https://youtu.be/${ID}?si=AbC123`,
    `youtu.be/${ID}`,
    `www.youtube.com/watch?v=${ID}`,
    `https://www.youtube.com/embed/${ID}`,
    `https://www.youtube-nocookie.com/embed/${ID}?start=10`,
    `https://www.youtube.com/shorts/${ID}`,
    `https://www.youtube.com/live/${ID}?feature=shared`,
    `http://youtube.com/v/${ID}`,
  ]) {
    assert.equal(idYouTube(url), ID, url);
  }
});

test("lo que no es un id de YouTube no llega al iframe", () => {
  for (const valor of [
    "",
    undefined,
    null,
    "corto",
    `${ID}x`, // 12 caracteres
    "dQw4w9WgXc!", // carácter fuera de [\w-]
    "../../../x?a", // ruta relativa
    `${ID}?autoplay=1`, // un id con parámetros pegados
    `${ID}"onload="alert(1)`,
    `javascript:alert('${ID}')`,
    `https://evil.example/watch?v=${ID}`, // otro host
    `https://youtube.com.evil.example/embed/${ID}`,
    `https://www.youtube.com/watch?v=${ID}x`,
    `https://www.youtube.com/embed/${ID}%22onload`,
    `https://youtu.be/`,
    `https://www.youtube.com/channel/UC1234567890`,
  ]) {
    assert.equal(idYouTube(valor), null, String(valor));
  }
});
