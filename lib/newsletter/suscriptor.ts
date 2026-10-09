// ── Lo que llega de quien se suscribe: su correo y su tema ────────────
// Lo usan el formulario (para avisar antes de enviar) y la ruta
// /api/suscripcion (que no confía en el formulario y valida de nuevo). Sin
// imports a propósito: el formulario es un client component y las pruebas
// (suscriptor.test.mjs) lo cargan con `node --test`, sin compilar.

/** Qué recibe: la edición mensual (que trae todas las Señales del mes) o cada
 *  Señal apenas sale. Son los dos «topics» de Resend (NEWSLETTER.md). */
export const TEMAS = ["edicion", "senales"] as const;
export type Tema = (typeof TEMAS)[number];

/** Decisión de Miguel (2026-10-08): por defecto, la edición mensual. */
export const TEMA_POR_DEFECTO: Tema = "edicion";

export const TEMA: Record<Tema, { etiqueta: string; recibe: string }> = {
  edicion: {
    etiqueta: "La edición, cada mes",
    recibe: "la edición de cada mes, con todas las Señales del mes juntas",
  },
  senales: {
    etiqueta: "Cada Señal",
    recibe: "cada Señal, apenas sale al aire",
  },
};

export function esTema(valor: unknown): valor is Tema {
  return typeof valor === "string" && (TEMAS as readonly string[]).includes(valor);
}

// Más estricta que el RFC a propósito. El SDK de Resend mete el correo tal
// cual en la ruta de la API (/contacts/{email}/topics), sin codificarlo: una
// «/», un «?», un «#» o un «%» en el correo cambiarían a qué recurso se llama.
// La parte local admite letras, dígitos y . _ + - ' (sin puntos al borde ni
// dobles); el dominio, etiquetas DNS y un TLD de letras (o punycode).
const EMAIL =
  /^[a-z0-9_+'-]+(?:\.[a-z0-9_+'-]+)*@(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})$/;

/** El correo limpio (sin espacios al borde, en minúsculas) o null si no sirve.
 *  Tope de 254 caracteres (RFC 5321) y de 64 para la parte local. */
export function normalizarEmail(valor: unknown): string | null {
  if (typeof valor !== "string") return null;
  const email = valor.trim().toLowerCase();
  if (email.length > 254 || email.indexOf("@") > 64) return null;
  return EMAIL.test(email) ? email : null;
}
