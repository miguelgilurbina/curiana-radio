import test from "node:test";
import assert from "node:assert/strict";
import { esTema, normalizarEmail, TEMA_POR_DEFECTO } from "./suscriptor.ts";

// Se corre con `npm run newsletter:test`.

test("un correo normal pasa, limpio y en minúsculas", () => {
  assert.equal(normalizarEmail("lector@ejemplo.com"), "lector@ejemplo.com");
  assert.equal(normalizarEmail("  Lector.Uno@Ejemplo.COM \n"), "lector.uno@ejemplo.com");
  assert.equal(normalizarEmail("miguel+radio@correo.ejemplo.co.ve"), "miguel+radio@correo.ejemplo.co.ve");
  assert.equal(normalizarEmail("o'neil_x-y@ejemplo.org"), "o'neil_x-y@ejemplo.org");
  assert.equal(normalizarEmail("a@b.xn--p1ai"), "a@b.xn--p1ai");
});

test("lo que no es un correo no pasa", () => {
  for (const malo of [
    undefined,
    null,
    42,
    {},
    "",
    "   ",
    "sin-arroba",
    "@ejemplo.com",
    "lector@",
    "lector@ejemplo",
    "lector@ejemplo.c",
    "lector@@ejemplo.com",
    "lec tor@ejemplo.com",
    ".lector@ejemplo.com",
    "lector.@ejemplo.com",
    "lec..tor@ejemplo.com",
    "lector@-ejemplo.com",
    "lector@ejemplo-.com",
    "lector@ejemplo..com",
    "lector@ejemplo.123",
    "lector@[127.0.0.1]",
    "\"con comillas\"@ejemplo.com",
    "ñandú@ejemplo.com",
    "lector@ejémplo.com",
  ]) {
    assert.equal(normalizarEmail(malo), null, String(malo));
  }
});

test("nada que cambie la ruta de la API de Resend: / ? # % ni puntos de más", () => {
  for (const malo of [
    "a/b@ejemplo.com",
    "x@ejemplo.com/../../domains",
    "a?b=1@ejemplo.com",
    "a#b@ejemplo.com",
    "a%2fb@ejemplo.com",
    "a@ejemplo.com?x=1",
    "a@ejemplo.com#x",
    "../a@ejemplo.com",
  ]) {
    assert.equal(normalizarEmail(malo), null, malo);
  }
});

test("los topes: 64 para la parte local, 254 en total", () => {
  const local64 = "a".repeat(64);
  assert.equal(normalizarEmail(`${local64}@ejemplo.com`), `${local64}@ejemplo.com`);
  assert.equal(normalizarEmail(`${local64}a@ejemplo.com`), null);

  const dominio = `${"b".repeat(60)}.${"c".repeat(60)}.${"d".repeat(60)}.${"e".repeat(50)}.com`;
  const justo = `${"a".repeat(254 - dominio.length - 1)}@${dominio}`;
  assert.equal(justo.length, 254);
  assert.equal(normalizarEmail(justo), justo);
  assert.equal(normalizarEmail(`a${justo}`), null);
});

test("un correo larguísimo se descarta sin tardar (sin retroceso catastrófico)", () => {
  const inicio = performance.now();
  assert.equal(normalizarEmail(`${"a.".repeat(5000)}@${"b-".repeat(5000)}.com`), null);
  assert.equal(normalizarEmail(`${"a".repeat(60)}@${"b.".repeat(90)}`), null);
  assert.ok(performance.now() - inicio < 50);
});

test("los temas son la edición y cada señal; por defecto, la edición", () => {
  assert.ok(esTema("edicion"));
  assert.ok(esTema("senales"));
  for (const malo of ["", "EDICION", "señales", "diario", undefined, null, 1]) assert.equal(esTema(malo), false);
  assert.equal(TEMA_POR_DEFECTO, "edicion");
});
