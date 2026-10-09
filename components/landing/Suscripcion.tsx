import { configurado } from "@/lib/newsletter/config";
import FormularioSuscripcion from "./FormularioSuscripcion";

// La suscripción al newsletter: en la landing (06 · Archivo y suscripción), en
// el pie de la noche de todas las páginas y en /suscripcion/confirmar cuando
// un enlace caducó. Es un server component delgado: lo único que decide es si
// el formulario está abierto, que depende de variables sólo de servidor
// (lib/newsletter/config.ts). Sin Resend configurado el formulario se muestra
// deshabilitado y lo dice: nunca una confirmación que no confirmó nada.
//
// Las páginas estáticas lo resuelven al compilar: al cargar las variables en
// Vercel hay que redeployar (NEWSLETTER.md).
export default function Suscripcion({
  variante = "landing",
}: {
  variante?: "landing" | "pie";
}) {
  return <FormularioSuscripcion variante={variante} abierta={configurado()} />;
}
