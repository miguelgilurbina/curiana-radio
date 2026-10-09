import type { Tema } from "./suscriptor";
import { SECRETO_MINIMO } from "./token";

// ── La configuración del newsletter (sólo servidor) ───────────────────
// Todo sale de variables de entorno de Vercel, ninguna NEXT_PUBLIC_: la clave
// de Resend y el secreto nunca llegan al navegador. Mientras falte alguna de
// las cinco obligatorias, configurado() es false y el formulario se muestra
// cerrado («LA SUSCRIPCIÓN ABRE PRONTO»); la ruta responde 503. Qué poner en
// cada una y dónde sacarla: NEWSLETTER.md.
//
// Se lee en cada llamada, no al cargar el módulo. Las páginas estáticas la
// leen al compilar: después de cargar las variables en Vercel hay que
// redeployar para que el formulario se abra.

const OBLIGATORIAS = [
  "RESEND_API_KEY",
  "RESEND_SEGMENT_ID",
  "RESEND_TOPIC_SENALES_ID",
  "RESEND_TOPIC_EDICION_ID",
  "SUSCRIPCION_SECRET",
] as const;

/** Decisión de Miguel (2026-10-08). */
const REMITENTE = "Curiana Radio <senales@curianaradio.com>";

export interface ConfigNewsletter {
  claveResend: string;
  /** El segmento «Newsletter» de Resend: a quién se le manda. */
  segmento: string;
  /** El ID del topic de Resend de cada tema. */
  temas: Record<Tema, string>;
  /** Firma los enlaces de confirmación (≥ 32 bytes). */
  secreto: string;
  remitente: string;
  responderA: string;
}

function leer(nombre: string): string | undefined {
  const valor = process.env[nombre]?.trim();
  return valor ? valor : undefined;
}

/** Los nombres de lo que falta (nunca los valores), para el registro. */
export function faltantes(): string[] {
  const faltan: string[] = OBLIGATORIAS.filter((nombre) => !leer(nombre));
  const secreto = leer("SUSCRIPCION_SECRET");
  if (secreto && Buffer.byteLength(secreto) < SECRETO_MINIMO) {
    faltan.push(`SUSCRIPCION_SECRET (tiene menos de ${SECRETO_MINIMO} bytes)`);
  }
  return faltan;
}

export function configurado(): boolean {
  return faltantes().length === 0;
}

export function configuracion(): ConfigNewsletter | null {
  if (!configurado()) return null;
  const remitente = leer("NEWSLETTER_FROM") ?? REMITENTE;
  return {
    claveResend: leer("RESEND_API_KEY")!,
    segmento: leer("RESEND_SEGMENT_ID")!,
    temas: {
      edicion: leer("RESEND_TOPIC_EDICION_ID")!,
      senales: leer("RESEND_TOPIC_SENALES_ID")!,
    },
    secreto: leer("SUSCRIPCION_SECRET")!,
    remitente,
    responderA: leer("NEWSLETTER_REPLY_TO") ?? remitente,
  };
}
