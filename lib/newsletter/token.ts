import crypto from "node:crypto";
import type { Tema } from "./suscriptor";

// ── El enlace de confirmación (doble opt-in) ──────────────────────────
// El correo de confirmación lleva un token firmado, no un registro en una
// base: el sitio no guarda nada hasta que el lector confirma, y entonces lo
// guarda Resend. El token es base64url(JSON{ e, t, exp }) + «.» + HMAC-SHA256
// en hex del primer tramo, con SUSCRIPCION_SECRET. Quien no tenga el secreto
// no puede fabricar uno ni cambiarle el correo, el tema o la fecha.
//
// Va firmado, no cifrado: el correo se lee si alguien decodifica el enlace.
// Por eso la página de confirmación lo borra de la barra al cargar.
//
// Sólo importa node:crypto (y un tipo): las pruebas (token.test.mjs) lo
// cargan con `node --test`, sin compilar. El import por defecto de crypto es a
// propósito: deja a la prueba vigilar timingSafeEqual.

/** El enlace vale 48 horas. */
export const VIGENCIA_MS = 48 * 60 * 60 * 1000;

/** Lo que pide el secreto como mínimo, en bytes. */
export const SECRETO_MINIMO = 32;

export interface Alta {
  email: string;
  tema: Tema;
}

function firma(cuerpo: string, secreto: string): string {
  if (Buffer.byteLength(secreto) < SECRETO_MINIMO) {
    throw new Error(`newsletter: SUSCRIPCION_SECRET necesita ${SECRETO_MINIMO} bytes o más`);
  }
  return crypto.createHmac("sha256", secreto).update(cuerpo).digest("hex");
}

/** El token para el enlace de confirmación; caduca a las 48 horas de `ahora`. */
export function firmar(alta: Alta, secreto: string, ahora = Date.now()): string {
  const exp = Math.floor((ahora + VIGENCIA_MS) / 1000);
  const cuerpo = Buffer.from(JSON.stringify({ e: alta.email, t: alta.tema, exp })).toString("base64url");
  return `${cuerpo}.${firma(cuerpo, secreto)}`;
}

/** El alta que firma el token, o null si está manipulado, mal formado o vencido. */
export function verificar(token: unknown, secreto: string, ahora = Date.now()): Alta | null {
  if (typeof token !== "string" || token.length > 1024) return null;
  // base64url no usa «.»: tiene que haber uno y sólo uno
  const punto = token.indexOf(".");
  if (punto <= 0 || punto !== token.lastIndexOf(".")) return null;
  const cuerpo = token.slice(0, punto);
  const recibida = Buffer.from(token.slice(punto + 1));
  const esperada = Buffer.from(firma(cuerpo, secreto));
  // timingSafeEqual exige el mismo largo; el largo de una firma no es secreto
  // (siempre 64), lo que no se filtra es cuántos caracteres coinciden.
  if (recibida.length !== esperada.length || !crypto.timingSafeEqual(recibida, esperada)) return null;

  let datos: unknown;
  try {
    datos = JSON.parse(Buffer.from(cuerpo, "base64url").toString("utf8"));
  } catch {
    return null;
  }
  if (!datos || typeof datos !== "object") return null;
  const { e, t, exp } = datos as Record<string, unknown>;
  if (typeof e !== "string" || (t !== "edicion" && t !== "senales") || typeof exp !== "number") return null;
  if (exp * 1000 <= ahora) return null;
  return { email: e, tema: t };
}
