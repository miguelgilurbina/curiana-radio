import { PORTAFOLIO } from "@/lib/redes";
import { SITIO } from "@/lib/seo";

// /.well-known/security.txt (RFC 9116): a quién avisarle si alguien encuentra
// una vulnerabilidad en el sitio. Estático: se arma al compilar.
//
// El proyecto no tiene correo público, así que los contactos son, en orden:
// la sección de contacto del portafolio de Miguel (la misma que enlaza
// «Quién transmite») y el reporte privado de vulnerabilidades del repo en
// GitHub, que funciona cuando «Private vulnerability reporting» está activado
// en los ajustes de seguridad del repo.
//
// Expires vence a un año del build, a medianoche UTC (el RFC pide menos de un
// año): cada deploy lo renueva, y si el sitio pasa un año sin desplegarse el
// archivo dice, con razón, que ya no se puede confiar en él.
export const dynamic = "force-static";

export function GET() {
  const vence = new Date();
  vence.setUTCFullYear(vence.getUTCFullYear() + 1);
  vence.setUTCHours(0, 0, 0, 0);

  const texto = [
    `# ${SITIO.nombre} — cómo reportar una vulnerabilidad`,
    `Contact: ${PORTAFOLIO.url}#contacto`,
    `Contact: ${SITIO.repo}/security/advisories/new`,
    `Expires: ${vence.toISOString()}`,
    "Preferred-Languages: es, en",
    `Canonical: ${SITIO.url}/.well-known/security.txt`,
    "",
  ].join("\n");

  return new Response(texto, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}
