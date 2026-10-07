import fs from "fs";
import path from "path";
import type {
  WikiManifest,
  WikiPagina,
  WikiIndiceEntry,
  SeccionWiki,
  Bibliografia,
  ObraBiblio,
} from "@/types/wiki";

const WIKI_DIR = path.join(process.cwd(), "content", "wiki");

// Mismo criterio que lib/galeria.ts: cachear en producción (el build no debe
// releer los mismos archivos por cada página que los referencia), no cachear
// en desarrollo — el contenido se regenera corriendo export_wiki_seed.py con
// el server vivo, y cachearlo obligaría a reiniciar para ver cada cambio.
const CACHEAR = process.env.NODE_ENV === "production";

let cacheManifest: WikiManifest | null = null;
let cacheBiblio: Bibliografia | null = null;
const cachePaginas = new Map<string, WikiPagina>();

const MANIFEST_VACIO: WikiManifest = { generado: "", n: 0, n_biblio: 0, paginas: [] };
const BIBLIO_VACIA: Bibliografia = { n: 0, obras: [] };

/** Lee un JSON del wiki. `null` si no existe — ausencia = wiki sin generar,
 *  que es un estado legítimo (clon nuevo, rama sin contenido). */
function leerJSON<T>(...segmentos: string[]): T | null {
  try {
    return JSON.parse(fs.readFileSync(path.join(WIKI_DIR, ...segmentos), "utf-8")) as T;
  } catch (err) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw err; // JSON roto SÍ debe romper el build: es contenido curado
  }
}

function leerManifest(): WikiManifest {
  if (CACHEAR && cacheManifest) return cacheManifest;
  cacheManifest = leerJSON<WikiManifest>("index.json") ?? MANIFEST_VACIO;
  return cacheManifest;
}

/** Fecha (AAAA-MM-DD) de la última exportación del vault: la del contenido. */
export function getWikiGenerado(): string {
  return leerManifest().generado;
}

/** Todos los artículos, en orden editorial. */
export function getWikiIndice(): WikiIndiceEntry[] {
  return leerManifest().paginas;
}

export function getWikiPorSeccion(seccion: SeccionWiki): WikiIndiceEntry[] {
  return leerManifest()
    .paginas.filter((p) => p.seccion === seccion)
    .sort((a, b) => a.orden - b.orden);
}

export function getWikiPagina(seccion: SeccionWiki, slug: string): WikiPagina | null {
  const clave = `${seccion}/${slug}`;
  if (CACHEAR && cachePaginas.has(clave)) return cachePaginas.get(clave)!;
  const pagina = leerJSON<WikiPagina>(seccion, `${slug}.json`);
  if (pagina && CACHEAR) cachePaginas.set(clave, pagina);
  return pagina;
}

/** Anterior y siguiente en el orden editorial de la sección. */
export function getVecinos(seccion: SeccionWiki, slug: string): {
  anterior: WikiIndiceEntry | null;
  siguiente: WikiIndiceEntry | null;
} {
  const lista = getWikiPorSeccion(seccion);
  const i = lista.findIndex((p) => p.slug === slug);
  if (i === -1) return { anterior: null, siguiente: null };
  return { anterior: lista[i - 1] ?? null, siguiente: lista[i + 1] ?? null };
}

/** Params de todas las combinaciones sección/slug, para generateStaticParams. */
export function getWikiParams(seccion?: SeccionWiki): { seccion: SeccionWiki; slug: string }[] {
  const paginas = seccion ? getWikiPorSeccion(seccion) : getWikiIndice();
  return paginas.map((p) => ({ seccion: p.seccion, slug: p.slug }));
}

export function getBibliografia(): ObraBiblio[] {
  if (!CACHEAR || !cacheBiblio) {
    cacheBiblio = leerJSON<Bibliografia>("bibliografia.json") ?? BIBLIO_VACIA;
  }
  return cacheBiblio.obras;
}

// El `genero` de una obra viene del frontmatter del vault como slug sin tildes
// («arqueo-linguistica»). Para leerlo se le devuelven palabra por palabra.
const TILDES: Record<string, string> = {
  academico: "académico",
  antropologia: "antropología",
  arqueologia: "arqueología",
  arqueometria: "arqueometría",
  botanica: "botánica",
  cronica: "crónica",
  etnografia: "etnografía",
  genetica: "genética",
  gramatica: "gramática",
  historiografia: "historiografía",
  lexico: "léxico",
  linguistica: "lingüística",
  religion: "religión",
  resenia: "reseña",
  teorico: "teórico",
};

/** «arqueo-linguistica» → «arqueo lingüística». */
export function generoLegible(genero: string | null): string | null {
  if (!genero) return null;
  return genero
    .split("-")
    .map((w) => TILDES[w] ?? w)
    .join(" ");
}

// Los grupos del filtro de la bibliografía (manual de Kaketiana, Vistas §04):
// cada `genero` del vault cae en uno. El que no esté aquí va a «otras», así
// que un género nuevo nunca desaparece del filtro: se ve sin clasificar.
export const GRUPOS_BIBLIO = [
  { clave: "cronicas", label: "Crónicas" },
  { clave: "etnohistoria", label: "Etnohistoria y etnografía" },
  { clave: "lengua", label: "Lengua" },
  { clave: "arqueologia", label: "Arqueología y ciencia" },
  { clave: "otras", label: "Sin clasificar" },
] as const;

export type GrupoBiblio = (typeof GRUPOS_BIBLIO)[number]["clave"];

const GRUPO_DE_GENERO: Record<string, GrupoBiblio> = {
  cronica: "cronicas",
  "cronica-regional": "cronicas",
  "cronica-historia-regional": "cronicas",
  etnohistoria: "etnohistoria",
  etnologia: "etnohistoria",
  etnografia: "etnohistoria",
  "etnografia-misionera": "etnohistoria",
  "etnografia-normativa": "etnohistoria",
  historiografia: "etnohistoria",
  "antropologia-religion": "etnohistoria",
  academico: "etnohistoria",
  resenia: "etnohistoria",
  "marco-teorico": "etnohistoria",
  linguistica: "lengua",
  "linguistica-comparativa": "lengua",
  "arqueo-linguistica": "lengua",
  glosario: "lengua",
  "glosario-alimentario": "lengua",
  "glosario-etnohistoria": "lengua",
  gramatica: "lengua",
  vocabulario: "lengua",
  "etnohistoria-vocabulario": "lengua",
  "etnografia-vocabularios": "lengua",
  "diccionario-colonial": "lengua",
  "diccionario-dialectal": "lengua",
  "lexico-regional": "lengua",
  arqueologia: "arqueologia",
  arqueometria: "arqueologia",
  genetica: "arqueologia",
  "ciencia-natural": "arqueologia",
  botanica: "arqueologia",
  datos: "arqueologia",
  inventario: "arqueologia",
};

export function grupoDeGenero(genero: string | null): GrupoBiblio {
  return (genero && GRUPO_DE_GENERO[genero]) || "otras";
}

// El autor y el año para la entrada de la bibliografía salen del `titulo`
// curado del vault («Oliver 1989, cap. 3 — Etnohistoria…»), no del campo
// `autor`: ése trae los nombres en formatos muy distintos (varios autores,
// notas entre paréntesis, «et al.») y no se deja invertir sin romper alguno.
const prefijoDe = (o: ObraBiblio) => o.titulo.split(" — ")[0];

/** «Oliver 1989, cap. 3» → «Oliver, cap. 3»; «Las Casas 1875 [c. 1561]» → «Las Casas»;
 *  «Breton 1665-1667» → «Breton». */
export function autorCortoDe(o: ObraBiblio): string {
  return prefijoDe(o)
    .replace(/\s*\[[^\]]*\]/g, "")
    .replace(/\s*\b\d{4}(?:\s*[-–]\s*\d{2,4})?\b/g, "")
    .replace(/\s+,/g, ",")
    .trim();
}

/** El año de la obra: el del frontmatter o, si falta, el del título. */
export function anioDe(o: ObraBiblio): string | null {
  return o.anio ?? /\b\d{4}\b/.exec(prefijoDe(o))?.[0] ?? null;
}

/** Cifras medidas para la portada. Ninguna se escribe a mano (regla 1). */
export function getCifrasWiki(): { articulos: number; obras: number; conLectura: number } {
  const obras = getBibliografia();
  return {
    articulos: leerManifest().n,
    obras: obras.length,
    conLectura: obras.filter((o) => o.lectura_url).length,
  };
}
