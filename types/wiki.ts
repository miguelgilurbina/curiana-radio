/**
 * Kaketiana — el mundo del kaketío.
 *
 * El vault de investigación (`proyecto-linguistico-caquetío`, repo aparte)
 * exportado a JSON estático por `export_wiki_seed.py`. No se edita a mano
 * aquí.
 *
 * El eje es el objeto, no la procedencia: se publican los **resultados**
 * (ensayos y piezas de lengua), no la bitácora del minado. Las 39 obras
 * quedan como bibliografía —referencia, no artículo— porque sus notas en el
 * vault son registro de trabajo: "qué es · estado técnico · qué ha dado".
 */

export type SeccionWiki = "pueblo" | "lengua";

export const SECCIONES_WIKI: Record<SeccionWiki, { label: string; desc: string }> = {
  pueblo: {
    label: "El pueblo",
    desc: "Cómo vivían, en qué creían, cómo se organizaban y hasta dónde llegaba su mundo.",
  },
  lengua: {
    label: "La lengua",
    desc: "Cómo es el caquetío reconstruido — y cómo se reconstruye una lengua sin hablantes.",
  },
};

/** Lo mínimo para listar un artículo. `orden` es editorial, no alfabético. */
export interface WikiIndiceEntry {
  slug: string;
  seccion: SeccionWiki;
  orden: number;
  /** Del frontmatter: "ensayo", "moc", "nota-viva"… */
  tipo: string;
  titulo: string;
  resumen: string;
}

export interface WikiManifest {
  generado: string;
  n: number;
  n_biblio: number;
  paginas: WikiIndiceEntry[];
}

/** El artículo completo — solo se lee en servidor. */
export interface WikiPagina extends WikiIndiceEntry {
  frontmatter: Record<string, unknown>;
  /** Markdown con los `[[wikilinks]]` del vault ya resueltos a rutas reales. */
  cuerpo: string;
  /**
   * Las obras sobre las que se sostiene el artículo, rescatadas del preámbulo
   * interno del ensayo antes de descartarlo. Enlazan a la bibliografía.
   */
  fuentes: { slug: string; titulo: string }[];
}

/**
 * Una obra de la bibliografía. Ficha corta a propósito: la nota de minado
 * completa se queda en el vault.
 */
export interface ObraBiblio {
  slug: string;
  titulo: string;
  obra: string;
  autor: string | null;
  anio: string | null;
  publicacion: string | null;
  genero: string | null;
  /** Qué aporta, en una línea — extraído del «Qué es» de la nota. */
  aporta: string;
  /** Prosa sobre cómo conseguirla. Puede decir "solo papel". */
  acceso: string | null;
  /** Primer enlace dentro de `acceso`, si lo hay. 14 de 39 lo tienen. */
  lectura_url: string | null;
}

export interface Bibliografia {
  n: number;
  obras: ObraBiblio[];
}
