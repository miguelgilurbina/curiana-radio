import { load } from "js-yaml";

// El frontmatter de un .md/.mdx del repo: el bloque YAML entre dos líneas
// «---» al principio del archivo, y lo que sigue es el cuerpo.
//
// Reemplaza a gray-matter (segunda revisión de seguridad, 2026-10-08), que
// arrastraba js-yaml 3 → argparse 1 → sprintf-js, con un aviso moderado cuyo
// único arreglo era bajarlo a la 2.0.1; y que además evaluaba como
// JavaScript un frontmatter abierto con «---js». Aquí sólo hay YAML, y el
// `load` de js-yaml 4 es seguro por defecto: no conoce los tipos !!js/*.
//
// Hace lo mismo que gray-matter con lo que el repo escribe (medido sobre
// todos los .md/.mdx del repo antes de cambiarlo): un BOM inicial se ignora;
// sin «---» en la primera línea no hay frontmatter y todo es cuerpo; el
// cuerpo empieza en la línea que sigue al «---» de cierre; un bloque vacío
// da `data` vacía; y una fecha sin comillas (`fecha: 2026-10-03`) sigue
// llegando como Date. Dos cosas son más estrictas a propósito: un
// frontmatter que abre y no cierra, o que no es un mapa clave: valor, es un
// error y no un archivo vacío.
//
// jai-sounds/scripts/resenas_obsidian.mjs lleva una copia de estas mismas
// reglas: los scripts de Node no importan TypeScript.

const APERTURA = /^---[ \t]*\r?\n/;
const CIERRE = /^---[ \t]*$/m;

export interface ConFrontmatter {
  /**
   * La misma forma que devolvía gray-matter: cada lector valida sus campos
   * uno por uno (lib/senales.ts, lib/manaure.ts), así que aquí no se tipa.
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: Record<string, any>;
  content: string;
}

export function leerFrontmatter(fuente: string): ConFrontmatter {
  const texto = fuente.charCodeAt(0) === 0xfeff ? fuente.slice(1) : fuente;
  const apertura = APERTURA.exec(texto);
  if (!apertura) return { data: {}, content: texto };

  const resto = texto.slice(apertura[0].length);
  const cierre = CIERRE.exec(resto);
  if (!cierre) throw new Error("el frontmatter abre con «---» y no tiene «---» de cierre");

  const content = resto.slice(cierre.index + cierre[0].length).replace(/^\r?\n/, "");
  const data = load(resto.slice(0, cierre.index));
  if (data == null) return { data: {}, content };
  if (typeof data !== "object" || Array.isArray(data)) {
    throw new Error("el frontmatter tiene que ser un mapa clave: valor");
  }
  return { data: data as ConFrontmatter["data"], content };
}
