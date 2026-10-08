import { track } from "@vercel/analytics";

// ── Los eventos de engagement (Vercel Web Analytics) ──────────────────
// Las visitas por página las cuenta Vercel solo. Esto es lo que una visita no
// dice: por dónde se entra a cada arista, si alguien leyó hasta el final, si
// se suscribió, a dónde se fue, qué obra quiso ver en grande. Es la base para
// decidir qué arista puede sostenerse (ver MEDICION.md, con el embudo).
//
// Los eventos propios sólo se registran en el plan Pro (hasta 2 propiedades
// por evento). Van apagados hasta que NEXT_PUBLIC_ANALITICA_EVENTOS=1 esté en
// el entorno de Vercel. Sin cookies y sin datos personales: ningún evento
// lleva el correo ni nada que identifique, y las rutas de /suscripcion/ (que
// pueden llevar el token del enlace de confirmación) no salen nunca enteras.

/** Las aristas que se miden al entrar. Galería entra cuando se libere
 *  (lib/secciones.ts): la cabecera y el pie ya la enlazan ese día. */
export const ARISTAS_MEDIDAS = ["kaketiana", "jai-sounds", "senales", "sobre", "galeria"] as const;
export type AristaMedida = (typeof ARISTAS_MEDIDAS)[number];

/** Desde qué elemento de navegación se entra (atributo `data-desde`). */
export const DESDES = ["cabecera", "pie", "landing", "intro"] as const;
export type Desde = (typeof DESDES)[number];

type Eventos = {
  /** El formulario del newsletter salió (no-cors: el proveedor no confirma). */
  suscripcion: { desde: string };
  /** La intro El Disco: saltó el afinado o sintonizó. */
  intro: { accion: "saltar" | "sintonizar" };
  /** Entró a una arista desde un elemento de navegación (el oyente de Analitica.tsx). */
  arista: { arista: AristaMedida; desde: Desde };
  /** Llegó al final de un texto largo y se quedó un rato antes. */
  lectura: { pagina: string };
  /** Un enlace que sale del sitio: Spotify, el repo, una fuente. */
  salida: { destino: string; desde: string };
  /** JAI Sounds: pasó a otra estación de la batea. */
  estacion: { estacion: string };
  /** La galería: abrió una obra en grande (interés por la pieza). */
  obra: { obra: string };
  /** Cambió la luz con el interruptor (Señales, «Quién transmite»): la luz que eligió. */
  luz: { luz: "claro" | "oscuro" };
};

export type NombreEvento = keyof Eventos;

const ACTIVOS = process.env.NEXT_PUBLIC_ANALITICA_EVENTOS === "1";

// ── Lo que nunca sale entero ──────────────────────────────────────────

/** Las páginas del newsletter (confirmar, darse de baja) pueden llevar el
 *  token en la ruta o en la query: no se cuentan como vista y, si un evento
 *  sale de ahí, sale con la ruta recortada a /suscripcion. */
const PRIVADA = "/suscripcion";

export function esRutaPrivada(ruta: string): boolean {
  return ruta.startsWith(`${PRIVADA}/`);
}

/** Una ruta lista para ir en una propiedad: sin query, sin hash y sin lo que
 *  cuelgue de /suscripcion/. */
export function rutaPublica(ruta: string): string {
  const limpia = ruta.split(/[?#]/, 1)[0];
  return esRutaPrivada(limpia) ? PRIVADA : limpia;
}

export function medir<N extends NombreEvento>(nombre: N, datos: Eventos[N]): void {
  if (!ACTIVOS) return;
  // Cinturón y tirantes: cualquier propiedad que sea una ruta del sitio pasa
  // por rutaPublica, la ponga quien la ponga.
  const seguros = Object.fromEntries(
    Object.entries(datos).map(([k, v]) => [k, typeof v === "string" && v.startsWith("/") ? rutaPublica(v) : v]),
  );
  track(nombre, seguros);
}

/**
 * El filtro `beforeSend` de Web Analytics y de Speed Insights: lo último que
 * ve cada envío antes de salir del navegador.
 *
 * - La URL sale sin hash y sin query, salvo los `utm_*`: los enlaces de
 *   difusión los llevan (MEDICION.md, «UTM») y Web Analytics Plus los lee.
 *   Cualquier otro parámetro —el `?t=` del enlace de confirmación, un `?q=`—
 *   no sale.
 * - Bajo /suscripcion/ no se cuenta ninguna vista (ni las métricas de
 *   rendimiento); un evento propio sí sale —ahí se mide la suscripción
 *   confirmada— pero con la URL recortada a /suscripcion.
 * - Si la URL no se puede leer, no se envía: antes perder un dato que filtrar
 *   uno.
 */
export function antesDeEnviar<E extends { type: string; url: string }>(envio: E): E | null {
  let url: URL;
  try {
    url = new URL(envio.url);
  } catch {
    return null;
  }
  if (esRutaPrivada(url.pathname)) {
    if (envio.type !== "event") return null;
    url.pathname = PRIVADA;
  }
  url.hash = "";
  for (const clave of [...url.searchParams.keys()]) {
    if (!clave.startsWith("utm_")) url.searchParams.delete(clave);
  }
  return { ...envio, url: url.toString() };
}

// ── La arista de un enlace ────────────────────────────────────────────

const esArista = (v: string | undefined): v is AristaMedida =>
  (ARISTAS_MEDIDAS as readonly string[]).includes(v ?? "");
const esDesde = (v: string | undefined): v is Desde => (DESDES as readonly string[]).includes(v ?? "");

/** La arista a la que lleva una ruta del sitio, o null si no es una arista. */
export function aristaDeRuta(ruta: string): AristaMedida | null {
  const primera = ruta.split("/")[1] ?? "";
  return esArista(primera) ? primera : null;
}

/**
 * Si un clic en un enlace interno es una entrada a una arista desde un
 * elemento de navegación, qué arista y desde dónde.
 *
 * - `desde`: el `data-desde` del enlace o del contenedor más cercano que lo
 *   tenga (la nav de la cabecera, el pie, la nav de la intro). En la landing,
 *   todo enlace sin contenedor marcado cuenta como `landing`: la landing
 *   entera es navegación hacia las aristas.
 * - `arista`: el `data-arista` del enlace, si lo tiene (para un CTA cuya ruta
 *   no la nombra); si no, sale de la ruta (/kaketiana/… → kaketiana).
 */
export function entradaAArista(
  enlace: HTMLAnchorElement,
  destino: URL,
  rutaActual: string,
): Eventos["arista"] | null {
  const marcado = enlace.closest<HTMLElement>("[data-desde]")?.dataset.desde;
  const desde = marcado ?? (rutaActual === "/inicio" ? "landing" : undefined);
  if (!esDesde(desde)) return null;
  const pedida = enlace.dataset.arista;
  const arista = esArista(pedida) ? pedida : aristaDeRuta(destino.pathname);
  return arista ? { arista, desde } : null;
}
