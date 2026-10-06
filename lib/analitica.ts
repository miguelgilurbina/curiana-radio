import { track } from "@vercel/analytics";

// ── Los eventos de engagement (Vercel Web Analytics) ──────────────────
// Las visitas por página las cuenta Vercel solo. Esto es lo que una visita no
// dice: si alguien leyó hasta el final, si se suscribió, a dónde se fue, qué
// obra quiso ver en grande. Es la base para decidir qué arista puede
// sostenerse (ver MEDICION.md).
//
// Los eventos propios sólo se registran en el plan Pro (hasta 2 propiedades
// por evento); en Hobby no aparecen. Por eso van apagados hasta que
// NEXT_PUBLIC_ANALITICA_EVENTOS=1 esté en el entorno de Vercel. Sin cookies y
// sin datos personales: ningún evento lleva el correo ni nada que identifique.

type Eventos = {
  /** El formulario del newsletter salió (no-cors: el proveedor no confirma). */
  suscripcion: { desde: string };
  /** La intro El Disco: saltó el afinado o sintonizó. */
  intro: { accion: "saltar" | "sintonizar" };
  /** Llegó al final de un texto largo y se quedó un rato antes. */
  lectura: { pagina: string };
  /** Un enlace que sale del sitio: Spotify, el repo, una fuente. */
  salida: { destino: string; desde: string };
  /** JAI Sounds: pasó a otra estación de la batea. */
  estacion: { estacion: string };
  /** La galería: abrió una obra en grande (interés por la pieza). */
  obra: { obra: string };
};

export type NombreEvento = keyof Eventos;

const ACTIVOS = process.env.NEXT_PUBLIC_ANALITICA_EVENTOS === "1";

export function medir<N extends NombreEvento>(nombre: N, datos: Eventos[N]): void {
  if (!ACTIVOS) return;
  track(nombre, datos);
}
