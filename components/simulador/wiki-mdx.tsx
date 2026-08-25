import type { ReactNode } from "react";
import Link from "next/link";
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";

// Componentes MDX para la prosa larga del wiki de fuentes: notas del vault
// tal como se escriben ahí — muchas tablas (bibliografía), citas en bloque
// (extractos de crónicas) y encabezados de sección. remark-gfm habilita
// tablas GFM; sin él next-mdx-remote no las reconoce.
//
// h1 se omite a propósito: el título de la página ya lo pinta la ficha
// (frontmatter `titulo`), y el export ya le quita el H1 al cuerpo.

const externo = (href: string) => /^https?:\/\//.test(href);

function A({ href, children }: { href?: string; children?: ReactNode }) {
  if (!href) return <span>{children}</span>;
  if (externo(href)) {
    return (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-(--sim-fuego) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:decoration-(--sim-fuego)"
      >
        {children}
        <span aria-hidden="true" className="ml-0.5 text-[0.7em] align-super">↗</span>
      </a>
    );
  }
  return (
    <Link
      href={href}
      className="text-(--sim-fuego) underline decoration-(--sim-rule) underline-offset-2 transition-colors hover:decoration-(--sim-fuego)"
    >
      {children}
    </Link>
  );
}

export const wikiMdxComponents = {
  h2: ({ children }: { children?: ReactNode }) => (
    <h2 className="sim-display mt-10 text-xl font-semibold text-(--sim-ink) first:mt-0 md:text-2xl">
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
  p: ({ children }: { children?: ReactNode }) => (
    <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft) first:mt-0">
      {children}
    </p>
  ),
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
  blockquote: ({ children }: { children?: ReactNode }) => (
    <blockquote className="mt-5 border-l-[3px] border-(--sim-fuego)/70 pl-4 font-serif text-[1.05rem] italic leading-relaxed text-(--sim-ink) md:pl-5">
      {children}
    </blockquote>
  ),
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
    <div className="mt-5 overflow-x-auto">
      <table className="w-full border-collapse font-sans text-[0.85rem] leading-snug">{children}</table>
    </div>
  ),
  thead: ({ children }: { children?: ReactNode }) => (
    <thead className="border-b border-(--sim-ink) text-left">{children}</thead>
  ),
  tbody: ({ children }: { children?: ReactNode }) => <tbody>{children}</tbody>,
  tr: ({ children }: { children?: ReactNode }) => (
    <tr className="border-b border-(--sim-rule) align-top">{children}</tr>
  ),
  th: ({ children }: { children?: ReactNode }) => (
    <th className="whitespace-nowrap px-3 py-2 font-sans text-xs font-semibold uppercase tracking-wide text-(--sim-ink-faint) first:pl-0">
      {children}
    </th>
  ),
  td: ({ children }: { children?: ReactNode }) => (
    <td className="px-3 py-2 text-(--sim-ink-soft) first:pl-0">{children}</td>
  ),
};

export function WikiProse({ source }: { source: string }) {
  return (
    <div>
      <MDXRemote
        source={source}
        components={wikiMdxComponents}
        options={{ mdxOptions: { remarkPlugins: [remarkGfm] } }}
      />
    </div>
  );
}
