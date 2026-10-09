import { configuracion, faltantes } from "@/lib/newsletter/config";
import { correoDeConfirmacion } from "@/lib/newsletter/correo";
import { enviarConfirmacion } from "@/lib/newsletter/resend";
import { esTema, normalizarEmail } from "@/lib/newsletter/suscriptor";
import { firmar } from "@/lib/newsletter/token";
import { SITIO } from "@/lib/seo";

// ── POST /api/suscripcion: el primer paso del doble opt-in ────────────
// Recibe { email, tema, sitio, desde } del formulario y manda el correo con
// el enlace firmado de confirmación. No guarda nada: el contacto se crea en
// Resend recién cuando el lector confirma (/suscripcion/confirmar). Flujo
// completo y configuración: NEWSLETTER.md.
//
// El límite de velocidad por IP no está aquí: lo pone el Firewall de Vercel
// con una regla de rate limit sobre /api/suscripcion (NEWSLETTER.md, paso 8),
// que corta antes de que la función arranque y responde 429. Una función sin
// estado no puede contar intentos entre instancias.
//
// Las respuestas no dicen si el correo ya estaba suscrito: siempre 200 si el
// correo salió. Volver a suscribirse es la forma de cambiar de tema.
//
// `desde` (la página del formulario) llega pero no se guarda: la suscripción
// se mide al confirmar, con el tema (MEDICION.md).

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Un correo, un tema y una ruta caben de sobra. */
const MAXIMO = 2048;

function responder(estado: number, ok: boolean): Response {
  return Response.json({ ok }, { status: estado, headers: { "Cache-Control": "no-store" } });
}

/** El origen de quien postea: Origin, o el de Referer si no viene. */
function origenDe(peticion: Request): string | null {
  const origin = peticion.headers.get("origin");
  if (origin && origin !== "null") return origin;
  const referer = peticion.headers.get("referer");
  if (!referer) return null;
  try {
    return new URL(referer).origin;
  } catch {
    return null;
  }
}

/** Los orígenes desde los que se puede postear: el sitio y, en las vistas
 *  previas, la URL del deploy y la de la rama. Fuera de Vercel (next dev o
 *  next start en local), también localhost. */
function permitido(origen: string): boolean {
  const permitidos: string[] = [SITIO.url];
  if (process.env.VERCEL_ENV === "preview") {
    for (const host of [process.env.VERCEL_URL, process.env.VERCEL_BRANCH_URL]) {
      if (host) permitidos.push(`https://${host}`);
    }
  }
  if (permitidos.includes(origen)) return true;
  if (process.env.VERCEL) return false;
  try {
    const { protocol, hostname } = new URL(origen);
    return protocol === "http:" && (hostname === "localhost" || hostname === "127.0.0.1");
  } catch {
    return false;
  }
}

export async function POST(peticion: Request): Promise<Response> {
  const conf = configuracion();
  if (!conf) {
    console.error(`newsletter: la suscripción está cerrada; falta ${faltantes().join(", ")}`);
    return responder(503, false);
  }

  const tipo = peticion.headers.get("content-type")?.split(";")[0]?.trim().toLowerCase();
  if (tipo !== "application/json") return responder(415, false);

  const origen = origenDe(peticion);
  if (!origen || !permitido(origen)) return responder(403, false);

  const crudo = await peticion.text();
  if (crudo.length > MAXIMO) return responder(413, false);
  let cuerpo: unknown;
  try {
    cuerpo = JSON.parse(crudo);
  } catch {
    return responder(400, false);
  }
  if (!cuerpo || typeof cuerpo !== "object" || Array.isArray(cuerpo)) return responder(400, false);
  const { email, tema, sitio } = cuerpo as Record<string, unknown>;

  // El campo trampa: una persona no lo ve ni lo alcanza con el tabulador; un
  // bot que llena todo, sí. Se le dice que funcionó y no se hace nada.
  if (sitio != null && String(sitio).trim() !== "") return responder(200, true);

  const correo = normalizarEmail(email);
  if (!correo || !esTema(tema)) return responder(400, false);

  try {
    // El enlace vuelve a donde se pidió: en producción es SITIO.url; en una
    // vista previa, esa vista previa (cuyo secreto puede ser otro).
    const token = firmar({ email: correo, tema }, conf.secreto);
    const enlace = `${origen}/suscripcion/confirmar?t=${token}`;
    const salio = await enviarConfirmacion(conf, correo, correoDeConfirmacion(enlace, tema));
    return salio ? responder(200, true) : responder(502, false);
  } catch (error) {
    console.error("newsletter: falló el envío de la confirmación", error instanceof Error ? error.message : error);
    return responder(502, false);
  }
}
