import fs from "fs";
import path from "path";
import { leerFrontmatter } from "./frontmatter";
import {
  ARISTAS,
  PIEL_DE_ARISTA,
  PIELES_IDS,
  esArista,
  esPiel,
  type Arista,
  type PielId,
  type Portada,
  type Senal,
  type SenalResumen,
} from "./senales-comun";

// Señales: el blog de Curiana Radio. La radio transmite desde después; las
// señales las escribe Miguel desde acá, firmadas. Es un solo blog: cada
// entrada lleva las aristas a las que pertenece y cada arista muestra las
// suyas (Miguel, 2026-10-03: «es un solo blog, pero el blog tiene secciones y
// las secciones se van a ir alimentando»). Sin arista, la entrada es de «la
// radio» y sale sólo en la portada y en el índice.
//
// Una entrada es un archivo: content/senales/<slug>.mdx. Las imágenes viven
// en Vercel Blob (como la galería: el repo está en OneDrive) y los videos se
// incrustan desde YouTube. El flujo de publicación está en la skill
// publicar-entrada.

const DIR = path.join(process.cwd(), "content", "senales");

export * from "./senales-comun";

// Los borradores se ven en local y en las vistas previas de Vercel (para
// revisarlos en el PR), nunca en producción.
const MOSTRAR_BORRADORES = process.env.VERCEL_ENV !== "production";

export const AUTOR = "Miguel Gil Urbina";

/** El YAML convierte `fecha: 2026-10-03` en Date; lo devolvemos a texto. */
function fechaISO(valor: unknown, archivo: string): string {
  const texto = valor instanceof Date ? valor.toISOString().slice(0, 10) : String(valor ?? "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(texto)) {
    throw new Error(`content/senales/${archivo}: «fecha» tiene que ser AAAA-MM-DD (vino «${texto}»)`);
  }
  return texto;
}

function texto(valor: unknown, campo: string, archivo: string): string {
  if (typeof valor !== "string" || !valor.trim()) {
    throw new Error(`content/senales/${archivo}: falta «${campo}»`);
  }
  return valor.trim();
}

function leer(archivo: string): Senal {
  const slug = archivo.replace(/\.mdx$/, "");
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) {
    throw new Error(`content/senales/${archivo}: el nombre del archivo es el slug y va en minúsculas con guiones`);
  }
  const { data, content } = leerFrontmatter(fs.readFileSync(path.join(DIR, archivo), "utf-8"));

  const aristas = (Array.isArray(data.aristas) ? data.aristas : []).map(String);
  const desconocida = aristas.find((a) => !esArista(a));
  if (desconocida) {
    throw new Error(
      `content/senales/${archivo}: arista «${desconocida}» no existe (las que hay: ${Object.keys(ARISTAS).join(", ")})`,
    );
  }

  // La piel: la que pida la señal, o la de su arista principal, o la radio.
  let piel: PielId = aristas.length ? PIEL_DE_ARISTA[aristas[0] as Arista] : "radio";
  if (data.piel !== undefined) {
    const pedida = String(data.piel);
    if (!esPiel(pedida)) {
      throw new Error(`content/senales/${archivo}: piel «${pedida}» no existe (las que hay: ${PIELES_IDS.join(", ")})`);
    }
    piel = pedida;
  }

  let portada: Portada | null = null;
  if (data.portada) {
    portada = {
      src: texto(data.portada.src, "portada.src", archivo),
      alt: texto(data.portada.alt, "portada.alt", archivo),
      pie: typeof data.portada.pie === "string" ? data.portada.pie : undefined,
    };
  }

  const palabras = content.split(/\s+/).filter(Boolean).length;
  return {
    slug,
    titulo: texto(data.titulo, "titulo", archivo),
    fecha: fechaISO(data.fecha, archivo),
    sumario: texto(data.sumario, "sumario", archivo),
    aristas: aristas as Arista[],
    piel,
    portada,
    autor: typeof data.autor === "string" ? data.autor : AUTOR,
    minutos: Math.max(1, Math.round(palabras / 200)),
    borrador: data.borrador === true,
    cuerpo: content,
  };
}

function todas(): Senal[] {
  if (!fs.existsSync(DIR)) return [];
  return fs
    .readdirSync(DIR)
    .filter((f) => f.endsWith(".mdx"))
    .map(leer)
    .filter((s) => MOSTRAR_BORRADORES || !s.borrador)
    .sort((a, b) => b.fecha.localeCompare(a.fecha) || a.slug.localeCompare(b.slug));
}

function resumen({ cuerpo: _cuerpo, ...r }: Senal): SenalResumen {
  return r;
}

/** Las señales publicadas, la más reciente primero; con `arista`, sólo las suyas. */
export function getSenales({ arista, limite }: { arista?: Arista; limite?: number } = {}): SenalResumen[] {
  const lista = todas()
    .filter((s) => !arista || s.aristas.includes(arista))
    .map(resumen);
  return limite ? lista.slice(0, limite) : lista;
}

/** Si este entorno muestra alguna señal: en producción, una publicada; en
 *  local y en las vistas previas, también un borrador, para revisarlo. Decide
 *  si Señales sale en la cabecera, el pie, la intro y «Quién transmite»
 *  (Miguel, 2026-10-08: no anunciar una sección vacía). /senales sigue
 *  existiendo por URL. */
export function haySenales(): boolean {
  return todas().length > 0;
}

/** Si hay alguna señal publicada (no borrador), en cualquier entorno: decide
 *  si /senales se indexa y entra al sitemap y a llms.txt. */
export function hayPublicadas(): boolean {
  return todas().some((s) => !s.borrador);
}

export function getSenal(slug: string): Senal | null {
  return todas().find((s) => s.slug === slug) ?? null;
}

/** La anterior (más vieja) y la siguiente (más nueva) a una señal. */
export function vecinas(slug: string): { anterior: SenalResumen | null; siguiente: SenalResumen | null } {
  const lista = getSenales();
  const i = lista.findIndex((s) => s.slug === slug);
  if (i < 0) return { anterior: null, siguiente: null };
  return { anterior: lista[i + 1] ?? null, siguiente: lista[i - 1] ?? null };
}
