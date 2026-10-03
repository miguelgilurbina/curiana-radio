// Lo que la página de un ensayo mide de su propio cuerpo, para el manual de
// Kaketiana (design_handoff_kaketiana, Vistas §02): el sumario sale de los ##
// del markdown; «este artículo» cuenta las citas de fuente y las tablas; «sobre
// qué se sostiene» junta las obras que el ensayo declara y las que enlaza.
// Nada se escribe a mano (regla 1): si el ensayo cambia en el vault, cambian
// las cifras.
//
// Sin fs ni nada de servidor: components/simulador/wiki-mdx.tsx importa de
// aquí el slug de los títulos y la regla de la cita, para que el sumario y el
// texto pintado no puedan discrepar.

export interface SeccionDelArticulo {
  id: string;
  texto: string;
}

/** El markdown en línea de un título → el texto que ve el lector. */
export function textoPlano(md: string): string {
  return md
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/[*`]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** La pregunta del artículo (frontmatter `pregunta`), si la tiene. */
export function preguntaDe(p: { frontmatter: Record<string, unknown> } | null): string | null {
  const q = p?.frontmatter.pregunta;
  return typeof q === "string" && q.trim() ? q.trim() : null;
}

/** El ancla de un título: sin tildes, en minúsculas, con guiones. */
export function slugTitulo(texto: string): string {
  return texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/**
 * Una cita en bloque es una cita de fuente —otra voz: la crónica, Oliver,
 * Miguel— cuando abre con comillas o con puntos suspensivos. Si no, es una
 * nota nuestra (un aviso, una corrección, un método) y va en nuestra letra.
 * Es la regla del manual: «cuando habla Oviedo, no hablamos nosotros».
 */
export function abreComoCita(texto: string): boolean {
  return /^["«“…]|^\.\.\./.test(texto.replace(/^[\s*_]+/, ""));
}

/**
 * En el vault, la atribución de una cita va en la línea siguiente del mismo
 * bloque («> — Oliver 1989, cap. 3, p. 278») y markdown la pega al párrafo de
 * la cita. Se separa en su propio párrafo para que la cita la tome como pie.
 */
export function pieDeCitaAparte(md: string): string {
  return md.replace(/^(>[^\n]*\S[^\n]*)\n(>\s*—\s)/gm, "$1\n>\n$2");
}

/** Las líneas del cuerpo que no están dentro de un bloque de código. */
function lineasDeProsa(md: string): string[] {
  const fuera: string[] = [];
  let enCodigo = false;
  for (const linea of md.split("\n")) {
    if (linea.trimStart().startsWith("```")) {
      enCodigo = !enCodigo;
      continue;
    }
    if (!enCodigo) fuera.push(linea);
  }
  return fuera;
}

/** El sumario: los ## del cuerpo, con el mismo ancla que les pone el h2. */
export function seccionesDe(md: string): SeccionDelArticulo[] {
  return lineasDeProsa(md)
    .map((l) => /^## (.+?)\s*#*\s*$/.exec(l)?.[1])
    .filter((t): t is string => Boolean(t))
    .map((t) => {
      const texto = textoPlano(t);
      return { id: slugTitulo(texto), texto };
    });
}

/**
 * ¿El primer párrafo de prosa va entero en cursiva? En tres ensayos es la
 * línea de sesión del vault («*Sesión 2 del programa…*»): un metadato, no el
 * arranque del texto, y la capitular pasa al párrafo siguiente.
 */
export function abreConCursiva(md: string): boolean {
  for (const l of lineasDeProsa(md)) {
    const s = l.trim();
    if (!s || /^(#|>|\||[-*+] |\d+\. |<)/.test(s)) continue;
    return /^[*_][^*_\s]/.test(s);
  }
  return false;
}

export interface MedidasDelArticulo {
  /** Citas en bloque que son otra voz (abreComoCita). */
  citas: number;
  tablas: number;
}

export function medidasDe(md: string): MedidasDelArticulo {
  const lineas = lineasDeProsa(md);
  let citas = 0;
  let tablas = 0;
  let enBloque = false;
  for (const l of lineas) {
    const esBloque = l.startsWith(">");
    if (esBloque && !enBloque && abreComoCita(l.replace(/^>\s?/, ""))) citas++;
    enBloque = esBloque;
    // La fila separadora de una tabla GFM: | --- | :--: |
    if (/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(l)) tablas++;
  }
  return { citas, tablas };
}

/**
 * Las obras sobre las que se sostiene: primero las que el export rescató del
 * preámbulo del ensayo (`fuentes`), luego las que el cuerpo enlaza, en el orden
 * en que aparecen. No se cuentan «citas»: los ensayos citan en prosa
 * («Arcaya 1920: 127») y enlazan cada obra una vez o ninguna, así que el
 * número de enlaces diría «1 cita» de una obra citada cinco veces.
 */
export function obrasDelArticulo(md: string, fuentes: { slug: string }[]): string[] {
  const orden = new Set(fuentes.map((f) => f.slug));
  for (const m of md.matchAll(/\(\/kaketiana\/bibliografia#([a-z0-9-]+)\)/g)) orden.add(m[1]);
  return [...orden];
}
