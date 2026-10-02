import { Children, cloneElement, isValidElement, type ReactElement, type ReactNode } from "react";
import Link from "next/link";
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import type { CapaEpistemica } from "@/lib/sim-theme";
import { CapaGlifo } from "@/components/simulador/capa";
import { abreComoCita, slugTitulo } from "@/lib/articulo";

// Componentes MDX para la prosa larga del wiki de fuentes: notas del vault
// tal como se escriben ahí — muchas tablas (bibliografía), citas en bloque
// (extractos de crónicas) y encabezados de sección. remark-gfm habilita
// tablas GFM; sin él next-mdx-remote no las reconoce.
//
// Desde el 2026-10-02 siguen el manual de Kaketiana (design_handoff_
// kaketiana, Vistas §02): los ## llevan ancla para el sumario, la cita de una
// fuente va en serif sobre papel hundido y nuestras notas en nuestra letra, y
// las tablas son las .kt del manual.
//
// h1 se omite a propósito: el título de la página ya lo pinta la ficha
// (frontmatter `titulo`), y el export ya le quita el H1 al cuerpo.

const externo = (href: string) => /^https?:\/\//.test(href);

/** El texto de un nodo tal como lo lee el lector: para el ancla de un título
 *  y para saber cómo abre una cita en bloque. */
function textoDe(nodo: ReactNode): string {
  if (nodo == null || typeof nodo === "boolean") return "";
  if (typeof nodo === "string" || typeof nodo === "number") return String(nodo);
  if (Array.isArray(nodo)) return nodo.map(textoDe).join("");
  if (isValidElement<{ children?: ReactNode }>(nodo)) return textoDe(nodo.props.children);
  return "";
}

const CAPAS_VALIDAS = new Set<string>(["atestiguado", "reconstruido", "retroabstraido", "hipotetico"]);

/** Una voz del diccionario nombrada en el wiki (lib/fichas.ts enlazarVoces la
 *  convierte en enlace con título «voz:capa» o «retirada:capa»): se pinta con
 *  el glifo de su capa, y tachada si el proyecto la retiró. */
function Voz({ href, titulo, children }: { href: string; titulo: string; children?: ReactNode }) {
  const [tipo, capa] = titulo.split(":");
  const retirada = tipo === "retirada";
  return (
    <Link
      href={href}
      className={`sim-display font-semibold underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:text-(--sim-fuego) hover:decoration-(--sim-fuego) ${
        retirada ? "text-(--sim-ink-soft) line-through" : "text-(--sim-ink)"
      }`}
    >
      {CAPAS_VALIDAS.has(capa) && (
        <span className="mr-1">
          <CapaGlifo capa={capa as CapaEpistemica} size={9} />
        </span>
      )}
      {children}
    </Link>
  );
}

// Los enlaces van en salina (--kk-extra), el color de enlace de la dirección 6b
// del manual; el ocre queda para la forma caquetía.
function A({ href, title, children }: { href?: string; title?: string; children?: ReactNode }) {
  if (!href) return <span>{children}</span>;
  if (title && /^(voz|retirada):/.test(title)) {
    return (
      <Voz href={href} titulo={title}>
        {children}
      </Voz>
    );
  }
  if (externo(href)) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-(--kk-extra) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:decoration-(--kk-extra)"
      >
        {children}
        <span aria-hidden="true" className="ml-0.5 text-[0.7em] align-super">↗</span>
      </a>
    );
  }
  return (
    <Link
      href={href}
      className="text-(--kk-extra) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:decoration-(--kk-extra)"
    >
      {children}
    </Link>
  );
}

type ConHijos = { children?: ReactNode };

function P({ children }: ConHijos) {
  return (
    <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft) first:mt-0">
      {children}
    </p>
  );
}

/** La prosa del ensayo: sans 1.02rem / 1.8, en la columna de 65ch. */
function PEnsayo({ children }: ConHijos) {
  return (
    <p className="mt-5 font-sans text-[0.95rem] leading-[1.8] text-(--sim-ink-soft) first:mt-0 sm:text-[1.02rem]">
      {children}
    </p>
  );
}

const esParrafo = (el: ReactElement): el is ReactElement<ConHijos> => el.type === P || el.type === PEnsayo;

const ABRE = /^(\s*)["«“]/;
const CIERRA = /["»”](\s*)$/;

/** La primera o la última hoja de texto de un nodo. */
function hoja(nodo: ReactNode, lado: "inicio" | "fin"): string {
  if (typeof nodo === "string") return nodo;
  if (Array.isArray(nodo)) return nodo.length ? hoja(nodo[lado === "inicio" ? 0 : nodo.length - 1], lado) : "";
  if (isValidElement<ConHijos>(nodo)) return hoja(nodo.props.children, lado);
  return "";
}

/** Quita la comilla de la primera o la última hoja, sin tocar el marcado. */
function sinComilla(nodo: ReactNode, lado: "inicio" | "fin"): ReactNode {
  if (typeof nodo === "string") return lado === "inicio" ? nodo.replace(ABRE, "$1") : nodo.replace(CIERRA, "$1");
  if (Array.isArray(nodo)) {
    if (nodo.length === 0) return nodo;
    const i = lado === "inicio" ? 0 : nodo.length - 1;
    return nodo.map((n, j) => (j === i ? sinComilla(n, lado) : n));
  }
  if (isValidElement<ConHijos>(nodo)) return cloneElement(nodo, { children: sinComilla(nodo.props.children, lado) });
  return nodo;
}

/**
 * La cita en bloque. Si es otra voz (abre con comillas: la crónica, Oliver,
 * Miguel), va como la pide el manual: papel hundido, serif itálica, la «
 * colgada en rúbrica y el pie en mono si la última línea abre con raya; en
 * móvil rompe la columna a sangre completa. Si es una nota nuestra —un aviso,
 * una corrección, un método—, vuelve a nuestra letra con un filete al margen,
 * en rúbrica cuando avisa (⚠️).
 */
function CitaEnBloque({ children }: ConHijos) {
  const partes = Children.toArray(children).filter(isValidElement);
  const primera = textoDe(partes[0]).trimStart();

  if (abreComoCita(primera)) {
    const ultima = partes[partes.length - 1];
    const pie = partes.length > 1 && esParrafo(ultima) && textoDe(ultima).trimStart().startsWith("—") ? ultima : null;
    let cuerpo: ReactNode[] = pie ? partes.slice(0, -1) : partes;
    // La « colgada ya dice que es cita: si el texto abre Y cierra con sus
    // comillas, se le quitan. Si sólo abre (la atribución va detrás en la
    // misma línea), se dejan, para no dejar una comilla huérfana.
    if (ABRE.test(hoja(cuerpo, "inicio")) && CIERRA.test(hoja(cuerpo, "fin"))) {
      cuerpo = sinComilla(sinComilla(cuerpo, "inicio"), "fin") as ReactNode[];
    }
    return (
      <blockquote className="relative -mx-4 mt-7 border-y border-(--sim-rule) bg-(--sim-paper-deep) py-6 pl-12 pr-6 sm:mx-0 sm:border sm:pb-[26px] sm:pl-[62px] sm:pr-9 sm:pt-[30px]">
        <span
          aria-hidden="true"
          className="sim-display absolute left-3.5 top-2.5 text-[2rem] leading-none text-(--sim-rubrica) sm:left-[18px] sm:top-3.5 sm:text-[2.6rem]"
        >
          «
        </span>
        {cuerpo.map((parte, i) =>
          isValidElement(parte) && esParrafo(parte) ? (
            <p
              key={i}
              className="mt-3 font-serif text-base italic leading-[1.65] text-(--sim-ink) first:mt-0 sm:text-[1.12rem] sm:leading-[1.7]"
            >
              {parte.props.children}
            </p>
          ) : (
            parte
          )
        )}
        {pie && (
          <footer className="sim-mono mt-4 text-[0.66rem] tracking-[0.1em] text-(--sim-ink-soft)">
            {pie.props.children}
          </footer>
        )}
      </blockquote>
    );
  }

  const aviso = primera.startsWith("⚠");
  return (
    <blockquote
      className={`mt-6 border-l-2 bg-(--sim-paper-deep)/40 py-3 pl-4 pr-4 sm:pl-5 ${
        aviso ? "border-(--sim-rubrica)" : "border-(--sim-rule)"
      }`}
    >
      {children}
    </blockquote>
  );
}

export const wikiMdxComponents = {
  h2: ({ children }: ConHijos) => (
    <h2
      id={slugTitulo(textoDe(children))}
      className="sim-display mt-10 scroll-mt-8 text-xl font-semibold text-(--sim-ink) first:mt-0 md:text-2xl"
    >
      {children}
    </h2>
  ),
  h3: ({ children }: { children?: ReactNode }) => (
    <h3 className="sim-display mt-8 text-lg font-semibold text-(--sim-ink) md:text-xl">{children}</h3>
  ),
  h4: ({ children }: { children?: ReactNode }) => (
    <h4 className="mt-6 font-sans text-sm font-semibold uppercase tracking-[0.08em] text-(--sim-ink-soft)">
      {children}
    </h4>
  ),
  p: P,
  a: A,
  strong: ({ children }: { children?: ReactNode }) => (
    <strong className="font-semibold text-(--sim-ink)">{children}</strong>
  ),
  em: ({ children }: { children?: ReactNode }) => <em className="italic">{children}</em>,
  ul: ({ children }: { children?: ReactNode }) => (
    <ul className="mt-4 max-w-reading list-outside list-disc space-y-1.5 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
      {children}
    </ul>
  ),
  ol: ({ children }: { children?: ReactNode }) => (
    <ol className="mt-4 max-w-reading list-outside list-decimal space-y-1.5 pl-5 font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
      {children}
    </ol>
  ),
  li: ({ children }: { children?: ReactNode }) => <li className="pl-1">{children}</li>,
  blockquote: CitaEnBloque,
  hr: () => <hr className="my-10 border-(--sim-rule)" />,
  code: ({ children }: { children?: ReactNode }) => (
    <code className="sim-mono rounded bg-(--sim-paper-deep) px-1.5 py-0.5 text-[0.85em] text-(--sim-ink)">
      {children}
    </code>
  ),
  pre: ({ children }: { children?: ReactNode }) => (
    <pre className="sim-mono mt-4 max-w-full overflow-x-auto rounded-md border border-(--sim-rule) bg-(--sim-paper-deep) p-4 text-[0.8rem] leading-relaxed text-(--sim-ink)">
      {children}
    </pre>
  ),
  table: ({ children }: { children?: ReactNode }) => (
    <div className="mt-6 overflow-x-auto">
      <table className="w-full border-collapse font-sans text-[0.82rem] leading-snug text-(--sim-ink-soft)">
        {children}
      </table>
    </div>
  ),
  thead: ({ children }: { children?: ReactNode }) => <thead className="text-left">{children}</thead>,
  tbody: ({ children }: { children?: ReactNode }) => <tbody>{children}</tbody>,
  tr: ({ children }: { children?: ReactNode }) => (
    <tr className="border-b border-(--sim-rule) align-top">{children}</tr>
  ),
  th: ({ children }: { children?: ReactNode }) => (
    <th className="sim-mono whitespace-nowrap border-b-2 border-(--sim-ink) px-3 py-2 text-[0.6rem] font-medium uppercase tracking-[0.14em] text-(--sim-ink-soft) first:pl-0">
      {children}
    </th>
  ),
  td: ({ children }: { children?: ReactNode }) => <td className="px-3 py-2.5 first:pl-0">{children}</td>,
};

/** El ensayo (pueblo) cambia sólo el párrafo: el resto es la misma gramática. */
const ensayoMdxComponents = { ...wikiMdxComponents, p: PEnsayo };

export function WikiProse({
  source,
  variante = "referencia",
  className = "",
}: {
  source: string;
  /** «ensayo» para el pueblo (prosa larga, 65ch); «referencia» para la lengua. */
  variante?: "ensayo" | "referencia";
  className?: string;
}) {
  // break-words: el vault escribe rutas y claves largas sin espacios que en
  // el móvil ensanchaban la página; las tablas siguen con su propio scroll.
  return (
    <div className={`break-words ${className}`}>
      <MDXRemote
        source={source}
        components={variante === "ensayo" ? ensayoMdxComponents : wikiMdxComponents}
        options={{ mdxOptions: { remarkPlugins: [remarkGfm] } }}
      />
    </div>
  );
}
