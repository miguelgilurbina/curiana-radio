import test from "node:test";
import assert from "node:assert/strict";
import crypto from "node:crypto";
import { firmar, verificar, VIGENCIA_MS } from "./token.ts";

// Se corre con `npm run newsletter:test` (node --test; Node ≥ 22.18 quita los
// tipos de token.ts solo, sin compilar ni dependencias).

const SECRETO = "x".repeat(48);
const OTRO = "y".repeat(48);
const AHORA = Date.UTC(2026, 9, 8, 12);
const ALTA = { email: "lector@ejemplo.com", tema: "edicion" };

/** Cambia un carácter de la firma (el último), sin cambiar su largo. */
function tocarFirma(token) {
  const ultimo = token.at(-1);
  return token.slice(0, -1) + (ultimo === "0" ? "1" : "0");
}

function cuerpoDe(token) {
  return JSON.parse(Buffer.from(token.split(".")[0], "base64url").toString("utf8"));
}

test("lo que se firma se verifica: vuelven el correo y el tema", () => {
  const token = firmar(ALTA, SECRETO, AHORA);
  assert.deepEqual(verificar(token, SECRETO, AHORA), ALTA);
  assert.deepEqual(verificar(firmar({ ...ALTA, tema: "senales" }, SECRETO, AHORA), SECRETO, AHORA), {
    ...ALTA,
    tema: "senales",
  });
});

test("el token es base64url(JSON{e,t,exp}) + «.» + HMAC-SHA256 en hex", () => {
  const token = firmar(ALTA, SECRETO, AHORA);
  const [cuerpo, firma] = token.split(".");
  assert.match(cuerpo, /^[A-Za-z0-9_-]+$/);
  assert.match(firma, /^[0-9a-f]{64}$/);
  assert.deepEqual(cuerpoDe(token), { e: ALTA.email, t: ALTA.tema, exp: (AHORA + VIGENCIA_MS) / 1000 });
  assert.equal(firma, crypto.createHmac("sha256", SECRETO).update(cuerpo).digest("hex"));
});

test("caduca a las 48 horas, ni un segundo después", () => {
  const token = firmar(ALTA, SECRETO, AHORA);
  assert.deepEqual(verificar(token, SECRETO, AHORA + VIGENCIA_MS - 1000), ALTA);
  assert.equal(verificar(token, SECRETO, AHORA + VIGENCIA_MS), null);
  assert.equal(verificar(token, SECRETO, AHORA + 30 * VIGENCIA_MS), null);
});

test("una firma tocada, otro secreto o un cuerpo cambiado no pasan", () => {
  const token = firmar(ALTA, SECRETO, AHORA);
  assert.equal(verificar(tocarFirma(token), SECRETO, AHORA), null);
  assert.equal(verificar(token, OTRO, AHORA), null);

  // otro correo con la firma del original
  const [, firma] = token.split(".");
  const ajeno = Buffer.from(JSON.stringify({ ...cuerpoDe(token), e: "otra@ejemplo.com" })).toString("base64url");
  assert.equal(verificar(`${ajeno}.${firma}`, SECRETO, AHORA), null);

  // alargar la vigencia sin volver a firmar
  const eterno = Buffer.from(JSON.stringify({ ...cuerpoDe(token), exp: 9e9 })).toString("base64url");
  assert.equal(verificar(`${eterno}.${firma}`, SECRETO, AHORA + 2 * VIGENCIA_MS), null);
});

test("lo mal formado devuelve null, no lanza", () => {
  for (const basura of [
    undefined,
    null,
    42,
    "",
    ".",
    "basura",
    "abc.def",
    "a.b.c",
    `.${"0".repeat(64)}`,
    `${firmar(ALTA, SECRETO, AHORA)}0`,
    `${firmar(ALTA, SECRETO, AHORA)}.otra`,
    "x".repeat(5000),
  ]) {
    assert.equal(verificar(basura, SECRETO, AHORA), null, String(basura).slice(0, 40));
  }
});

test("un cuerpo bien firmado pero con datos raros tampoco pasa", () => {
  const firmarCuerpo = (obj) => {
    const cuerpo = Buffer.from(JSON.stringify(obj)).toString("base64url");
    return `${cuerpo}.${crypto.createHmac("sha256", SECRETO).update(cuerpo).digest("hex")}`;
  };
  const exp = (AHORA + VIGENCIA_MS) / 1000;
  assert.equal(verificar(firmarCuerpo({ e: ALTA.email, t: "diario", exp }), SECRETO, AHORA), null);
  assert.equal(verificar(firmarCuerpo({ e: 7, t: "edicion", exp }), SECRETO, AHORA), null);
  assert.equal(verificar(firmarCuerpo({ e: ALTA.email, t: "edicion", exp: "mañana" }), SECRETO, AHORA), null);
  assert.equal(verificar(firmarCuerpo(["no", "objeto"]), SECRETO, AHORA), null);
  const noJson = Buffer.from("no es json").toString("base64url");
  const firmaNoJson = crypto.createHmac("sha256", SECRETO).update(noJson).digest("hex");
  assert.equal(verificar(`${noJson}.${firmaNoJson}`, SECRETO, AHORA), null);
});

test("la firma se compara en tiempo constante (crypto.timingSafeEqual)", (t) => {
  const espia = t.mock.method(crypto, "timingSafeEqual");
  const token = firmar(ALTA, SECRETO, AHORA);

  assert.equal(verificar(tocarFirma(token), SECRETO, AHORA), null);
  assert.equal(espia.mock.callCount(), 1);
  const [a, b] = espia.mock.calls[0].arguments;
  assert.equal(a.length, b.length);

  assert.deepEqual(verificar(token, SECRETO, AHORA), ALTA);
  assert.equal(espia.mock.callCount(), 2);

  // con otro largo no se llega a comparar: timingSafeEqual lanzaría
  assert.equal(verificar(`${token.split(".")[0]}.abc`, SECRETO, AHORA), null);
  assert.equal(espia.mock.callCount(), 2);
});

test("un secreto de menos de 32 bytes no firma ni verifica", () => {
  assert.throws(() => firmar(ALTA, "corto", AHORA), /32 bytes/);
  assert.throws(() => verificar(firmar(ALTA, SECRETO, AHORA), "corto", AHORA), /32 bytes/);
});
