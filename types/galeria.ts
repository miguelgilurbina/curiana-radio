/**
 * Galería visual — experimentos de imagen generados con IA.
 *
 * El manifest (`content/galeria/obras.json`) es la fuente de verdad y vive
 * versionado; los archivos de imagen NO viven en el repo. Cada obra publicada
 * tiene una escalera de variantes WebP ya redimensionadas en Vercel Blob, que
 * el navegador pide directamente al CDN.
 *
 * Ese pre-redimensionado es deliberado: pasar por la optimización de imágenes
 * de Vercel factura una transformación por cada fallo de caché y hace esperar
 * al primer visitante de cada variante. Generándolas al ingerir, la galería no
 * consume transformaciones y las imágenes salen del CDN como archivos planos.
 *
 * El esquema contempla la licencia porque el modelo de datos es lo caro de
 * cambiar después: hoy nadie cobra nada, pero cuando exista checkout no habrá
 * que re-etiquetar el catálogo entero.
 */

/** Publicada = tiene escalera en Blob. Pendiente = concepto sin render todavía. */
export type EstadoObra = "publicada" | "pendiente";

/**
 * Qué puede hacer un visitante con la imagen. Deliberadamente pocas opciones:
 * cada una es una promesa legal, no una etiqueta decorativa.
 */
export type TipoLicencia =
  /** Uso libre no comercial con atribución a Curiana Radio. */
  | "cc-by-nc"
  /** Prensa, docencia, divulgación. Sin reventa ni merchandising. */
  | "editorial"
  /** Disponible para uso comercial / impresión bajo acuerdo. */
  | "comercial"
  /** No se licencia (pieza de identidad de la radio, encargo, etc.). */
  | "reservado";

export interface LicenciaObra {
  tipo: TipoLicencia;
  /** Si la obra puede terminar en un producto físico (print, textil). */
  print: boolean;
  /** Matices que la etiqueta no captura (exclusividades, créditos exigidos). */
  notas?: string;
}

/** Proveniencia: de dónde salió la imagen. Se muestra en la ficha. */
export interface ProcedenciaObra {
  /** "Midjourney", "Nano Banana", … */
  herramienta: string;
  /** El prompt real. Parte del contenido, no un detalle técnico oculto. */
  prompt?: string;
  /** Retoque, upscaling, collage posterior. */
  posproceso?: string;
  /**
   * Id de la parrilla de origen. Midjourney entrega hasta cuatro variantes por
   * prompt: las que se hayan elegido comparten `generacion` y se distinguen
   * por `variante`. El barajado lo usa para no dejar contiguas dos obras que
   * salieron de la misma parrilla y se parecen demasiado.
   */
  generacion?: string;
  variante?: number;
}

/**
 * Lo mínimo para pintar una pieza del mosaico. Se separa del registro completo
 * porque con ~800 obras el manifest entero serializado al cliente pesa más que
 * las propias imágenes de la primera pantalla.
 */
export interface ObraGrid {
  slug: string;
  titulo: string;
  /** Texto alternativo real. Obligatorio, no opcional. */
  alt: string;
  serie: string;
  orden: number;
  estado: EstadoObra;
  tags: string[];
  /** Solo el tipo: el resto de la licencia se lee en la ficha. */
  licencia: TipoLicencia;

  /** Dimensiones de la variante mayor. Dan la proporción al motor del mosaico. */
  w: number | null;
  h: number | null;
  /**
   * Anchos disponibles en Blob, de menor a mayor. La URL se compone con
   * `blobBase` del manifest: `${blobBase}/${slug}-${ancho}.webp`. Guardar los
   * anchos y no las URLs completas ahorra ~200 KB de JSON en el cliente.
   */
  anchos: number[];
  /**
   * Color dominante (`#rrggbb`) para reservar el hueco mientras carga. Siete
   * bytes en vez de los ~400 de una miniatura borrosa en base64: a esta escala
   * la diferencia son 330 KB de JSON antes de ver la primera imagen.
   */
  color: string;
  /** Agrupa las variantes hermanas de una misma parrilla de Midjourney. */
  generacion?: string;
}

/** El registro completo. Solo se lee en servidor, para la ficha. */
export interface Obra extends ObraGrid {
  /** Statement curatorial: qué es y por qué existe. */
  concepto: string;
  anio: number;
  licenciaDetalle: LicenciaObra;
  procedencia: ProcedenciaObra;
  /** Edición del fanzine con la que dialoga, si aplica (slug de la edición). */
  edicion?: string;
  /**
   * Ruta (pathname, NO url firmada) del original en el bucket privado.
   * Se guarda solo la clave a propósito: el manifest está versionado y
   * sincroniza a OneDrive, así que nunca debe contener nada firmado ni secreto.
   * Resolver siempre en servidor. Ver lib/galeria.ts → getOriginalKey().
   */
  originalKey?: string;
}

export interface Serie {
  id: string;
  titulo: string;
  descripcion: string;
}

export interface GaleriaManifest {
  /**
   * Origen público del store de Blob, sin barra final. Se guarda una vez y no
   * por obra. `null` mientras no se haya subido nada.
   */
  blobBase: string | null;
  series: Serie[];
  obras: Obra[];
}

export const ETIQUETA_LICENCIA: Record<TipoLicencia, string> = {
  "cc-by-nc": "CC BY-NC",
  editorial: "Uso editorial",
  comercial: "Licencia comercial",
  reservado: "Derechos reservados",
};

export const DESCRIPCION_LICENCIA: Record<TipoLicencia, string> = {
  "cc-by-nc":
    "Puedes usarla y adaptarla sin fines comerciales, citando a Curiana Radio.",
  editorial:
    "Uso en prensa, docencia y divulgación. No cubre reventa ni merchandising.",
  comercial: "Disponible para uso comercial e impresión bajo acuerdo previo.",
  reservado: "Pieza de identidad de la radio. No se licencia para uso externo.",
};

/** Compone la URL de una variante concreta en Blob. */
export function urlVariante(
  blobBase: string | null,
  slug: string,
  ancho: number
): string | null {
  return blobBase ? `${blobBase}/${slug}-${ancho}.webp` : null;
}

/**
 * `srcset` completo de una obra. El navegador elige el archivo según el ancho
 * real de la pieza y la densidad de pantalla — sin intermediarios ni cómputo
 * en servidor.
 */
export function srcSetDe(blobBase: string | null, obra: ObraGrid): string {
  if (!blobBase || obra.anchos.length === 0) return "";
  return obra.anchos
    .map((a) => `${urlVariante(blobBase, obra.slug, a)} ${a}w`)
    .join(", ");
}
