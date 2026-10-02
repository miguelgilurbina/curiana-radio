// Las páginas interiores de Kaketiana (artículos, diccionario, bibliografía,
// personajes, lo que no sabemos). El marco —la placa 6b y la navegación— lo
// pone app/kaketiana/layout.tsx; aquí sólo la columna. Hasta el 2026-10-02 era
// SimShell: el masthead de la era 1 y la cronología del run como barra
// lateral, que no tenían que ver con el wiki.
export default function InteriorLayout({ children }: { children: React.ReactNode }) {
  return <div className="mx-auto max-w-6xl px-4 pb-24 pt-10 sm:px-6 lg:px-8">{children}</div>;
}
