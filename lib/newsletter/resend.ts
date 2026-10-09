import { Resend } from "resend";
import type { ConfigNewsletter } from "./config";
import type { Tema } from "./suscriptor";

// ── Las dos llamadas a Resend ─────────────────────────────────────────
// Mandar el correo de confirmación (al suscribirse) y dar de alta el contacto
// (al confirmar). El SDK no lanza: devuelve { data, error } con
// error = { name, statusCode, message }. Al registro va el nombre, el código y
// el mensaje con el correo tapado; el correo del lector, nunca.

type ErrorResend = { name: string; statusCode: number | null; message: string };

function registrar(que: string, error: ErrorResend, email: string): void {
  console.error(`newsletter: ${que}`, {
    name: error.name,
    statusCode: error.statusCode,
    message: String(error.message ?? "").split(email).join("<correo>"),
  });
}

/** Lo que Resend dice cuando algo ya existe. La doc de errores
 *  (resend.com/docs/api-reference/errors) no trae un código para eso: se mira
 *  el 409 y el texto, por si acaso. */
function yaExiste(error: ErrorResend): boolean {
  return error.statusCode === 409 || /already|exist/i.test(String(error.message ?? ""));
}

function noEsta(error: ErrorResend): boolean {
  return error.statusCode === 404 || error.name === "not_found";
}

export async function enviarConfirmacion(
  conf: ConfigNewsletter,
  email: string,
  correo: { subject: string; html: string; text: string },
): Promise<boolean> {
  const { error } = await new Resend(conf.claveResend).emails.send({
    from: conf.remitente,
    to: email,
    replyTo: conf.responderA,
    ...correo,
  });
  if (error) {
    registrar("Resend no mandó la confirmación", error, email);
    return false;
  }
  return true;
}

/**
 * Deja el correo suscrito al segmento del newsletter con el tema elegido (y
 * fuera del otro). Se puede llamar todas las veces que haga falta: confirmar
 * dos veces, o confirmar otro tema desde un enlace nuevo, deja el último.
 *
 * Primero pregunta si el contacto ya existe. Crear uno que ya está no da
 * error (resend-node#494: «returns a normal success response») y la doc no
 * dice si entonces aplica unsubscribed, el segmento y los temas; así que a un
 * contacto existente se le actualiza cada cosa por separado. Si dos
 * confirmaciones se cruzan y la segunda creación sí falla por duplicado, se
 * cae al mismo camino.
 */
export async function darDeAlta(conf: ConfigNewsletter, email: string, tema: Tema): Promise<boolean> {
  const resend = new Resend(conf.claveResend);
  const otro: Tema = tema === "edicion" ? "senales" : "edicion";
  const topics = [
    { id: conf.temas[tema], subscription: "opt_in" as const },
    { id: conf.temas[otro], subscription: "opt_out" as const },
  ];

  const existente = await resend.contacts.get({ email });
  if (existente.error && !noEsta(existente.error)) {
    registrar("no se pudo consultar el contacto", existente.error, email);
    return false;
  }

  if (!existente.data) {
    const creado = await resend.contacts.create({
      email,
      unsubscribed: false,
      segments: [{ id: conf.segmento }],
      topics,
    });
    if (!creado.error) return true;
    if (!yaExiste(creado.error)) {
      registrar("no se pudo crear el contacto", creado.error, email);
      return false;
    }
  }

  // Ya existía: vuelve a recibir (si se había dado de baja de todo, esta
  // confirmación es su nuevo sí), entra al segmento y toma el tema elegido.
  const reactivado = await resend.contacts.update({ email, unsubscribed: false });
  if (reactivado.error) {
    registrar("no se pudo reactivar el contacto", reactivado.error, email);
    return false;
  }
  const enSegmento = await resend.contacts.segments.add({ email, segmentId: conf.segmento });
  if (enSegmento.error && !yaExiste(enSegmento.error)) {
    registrar("no se pudo sumar el contacto al segmento", enSegmento.error, email);
    return false;
  }
  const conTema = await resend.contacts.topics.update({ email, topics });
  if (conTema.error) {
    registrar("no se pudieron poner los temas del contacto", conTema.error, email);
    return false;
  }
  return true;
}
