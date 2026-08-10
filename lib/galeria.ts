import fs from "fs";
import path from "path";
import type {
  GaleriaManifest,
  Obra,
  ObraGrid,
  Serie,
} from "@/types/galeria";

const MANIFEST_PATH = path.join(
  process.cwd(),
  "content",
  "galeria",
  "obras.json"
);

const VACIO: GaleriaManifest = { blobBase: null, series: [], obras: [] };

/**
 * El manifest se lee una vez por proceso. Con ~800 obras, releer y reparsear
 * el JSON en cada una de las ~800 llamadas a generateStaticParams/página
 * convertiría el build en minutos de E/S inútil.
 *
 * En desarrollo no se cachea: el manifest es contenido que se edita a mano
 * mientras el servidor corre (curar títulos, licencias, tags), y cachearlo
 * obligaría a reiniciar para ver cada cambio.
 */
const CACHEAR = process.env.NODE_ENV === "production";
let cache: GaleriaManifest | null = null;

function readManifest(): GaleriaManifest {
  if (CACHEAR && cache) return cache;
  let raw: string;
  try {
    raw = fs.readFileSync(MANIFEST_PATH, "utf-8");
  } catch (err) {
    // Manifest ausente = galería vacía, estado legítimo (clon nuevo, rama sin
    // contenido). Mismo criterio que lib/lexicon.ts.
    if ((err as NodeJS.ErrnoException).code === "ENOENT") {
      cache = VACIO;
      return cache;
    }
    throw err;
  }
  // JSON roto SÍ debe romper el build: es contenido curado, no dato opcional.
  const parsed = JSON.parse(raw) as Partial<GaleriaManifest>;
  cache = {
    blobBase: parsed.blobBase ?? null,
    series: parsed.series ?? [],
    obras: parsed.obras ?? [],
  };
  return cache;
}

/** Orden curatorial: el de `series` en el manifest, y dentro, `orden`. */
function ordenar(obras: Obra[], series: Serie[]): Obra[] {
  const pesoSerie = new Map(series.map((s, i) => [s.id, i]));
  return [...obras].sort((a, b) => {
    const sa = pesoSerie.get(a.serie) ?? Number.MAX_SAFE_INTEGER;
    const sb = pesoSerie.get(b.serie) ?? Number.MAX_SAFE_INTEGER;
    return sa !== sb ? sa - sb : a.orden - b.orden;
  });
}

/**
 * Proyecta el registro completo a lo que necesita el mosaico. Es la frontera
 * servidor/cliente: todo lo que no esté aquí no cruza. Que `ObraGrid` sea un
 * tipo aparte —y no un `Omit` del completo— hace que añadir un campo sensible
 * al manifest no lo filtre por descuido.
 */
function aGrid(obra: Obra): ObraGrid {
  return {
    slug: obra.slug,
    titulo: obra.titulo,
    alt: obra.alt,
    serie: obra.serie,
    orden: obra.orden,
    estado: obra.estado,
    tags: obra.tags,
    licencia: obra.licencia,
    w: obra.w,
    h: obra.h,
    anchos: obra.anchos,
    color: obra.color,
    generacion: obra.generacion,
  };
}

export function getBlobBase(): string | null {
  return readManifest().blobBase;
}

export function getSeries(): Serie[] {
  return readManifest().series;
}

/** Payload del mosaico. Es lo único que se serializa al cliente. */
export function getObrasGrid(): ObraGrid[] {
  const { obras, series } = readManifest();
  return ordenar(obras, series).map(aGrid);
}

/** Registro completo. Solo servidor — lo usa la ficha. */
export function getObra(slug: string): Obra | null {
  return readManifest().obras.find((o) => o.slug === slug) ?? null;
}

/** Slugs para generateStaticParams, sin cargar el resto del registro. */
export function getSlugs(): string[] {
  const { obras, series } = readManifest();
  return ordenar(obras, series).map((o) => o.slug);
}

/** Vecinas en el orden curatorial, para navegar de obra en obra. */
export function getVecinas(slug: string): {
  anterior: { slug: string; titulo: string } | null;
  siguiente: { slug: string; titulo: string } | null;
} {
  const { obras, series } = readManifest();
  const ordenadas = ordenar(obras, series);
  const i = ordenadas.findIndex((o) => o.slug === slug);
  if (i === -1) return { anterior: null, siguiente: null };
  const resumir = (o: Obra | undefined) =>
    o ? { slug: o.slug, titulo: o.titulo } : null;
  return {
    anterior: resumir(ordenadas[i - 1]),
    siguiente: resumir(ordenadas[i + 1]),
  };
}

/**
 * Tags para los filtros, ordenados por frecuencia. Se recortan a `limite`
 * porque con ~800 obras la cola larga son cientos de motivos con una sola
 * obra cada uno: una pared de píldoras que nadie usa.
 */
export function getTags(limite = 24): { tag: string; total: number }[] {
  const cuenta = new Map<string, number>();
  for (const obra of readManifest().obras) {
    for (const tag of obra.tags) {
      cuenta.set(tag, (cuenta.get(tag) ?? 0) + 1);
    }
  }
  return [...cuenta.entries()]
    .map(([tag, total]) => ({ tag, total }))
    .sort((a, b) => b.total - a.total || a.tag.localeCompare(b.tag, "es"))
    .slice(0, limite);
}

/**
 * Ruta del original en el bucket privado. Solo servidor: es la pieza que un
 * futuro checkout usará para firmar una descarga tras verificar el pago.
 * Nunca pasar el resultado a un componente cliente.
 */
export function getOriginalKey(slug: string): string | null {
  return readManifest().obras.find((o) => o.slug === slug)?.originalKey ?? null;
}
