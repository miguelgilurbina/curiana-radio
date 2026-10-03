import Link from "next/link";
import type { ReactNode } from "react";

// La miga del artículo, del manual de Kaketiana (Vistas §02 y §03, móvil en
// Sistema §06): «KAKETIANA / LA SECCIÓN / EL TÍTULO» en mono y, a la derecha,
// lo que el lector necesita saber de dónde está: el progreso en un ensayo
// («02 / 10»), el registro en una obra de consulta («REFERENCIA»). En móvil se
// reduce a «← LA SECCIÓN» con un control de 44px.
//
// Va pegada a la nav de la sección: anula el pt-10 de la columna interior
// (app/kaketiana/(interior)/layout.tsx), y en móvil va a sangre completa,
// como la barra del sumario que la sigue.
export default function MigaArticulo({
  seccion,
  titulo,
  derecha,
  derechaMovil,
}: {
  seccion: { label: string; href: string };
  titulo: string;
  /** Lo de la derecha en escritorio. */
  derecha: ReactNode;
  /** Lo de la derecha en móvil, si cambia. */
  derechaMovil?: ReactNode;
}) {
  return (
    <nav
      aria-label="Dónde estás"
      className="-mx-4 -mt-10 flex items-center gap-4 border-b border-(--sim-rule) px-4 py-0.5 sm:mx-0 sm:px-0 sm:py-3.5"
    >
      <ol className="kk-label hidden min-w-0 items-center gap-2 text-[0.62rem] tracking-[0.16em] text-(--sim-ink-soft) sm:flex">
        <li>
          <Link href="/kaketiana" className="transition-colors hover:text-(--sim-rubrica)">
            Kaketiana
          </Link>
        </li>
        <li aria-hidden="true" className="text-(--sim-ink-faint)">
          /
        </li>
        <li>
          <Link href={seccion.href} className="whitespace-nowrap transition-colors hover:text-(--sim-rubrica)">
            {seccion.label}
          </Link>
        </li>
        <li aria-hidden="true" className="text-(--sim-ink-faint)">
          /
        </li>
        <li aria-current="page" className="min-w-0 truncate text-(--sim-ink)">
          {titulo}
        </li>
      </ol>
      <Link
        href={seccion.href}
        className="kk-label inline-flex min-h-11 items-center text-[0.6rem] tracking-[0.12em] text-(--sim-ink-soft) sm:hidden"
      >
        ← {seccion.label}
      </Link>
      <span className="flex-1" />
      <span className="kk-label shrink-0 text-[0.6rem] tracking-[0.16em] text-(--sim-ink-soft) sm:text-[0.62rem]">
        {derechaMovil ? (
          <>
            <span className="sm:hidden">{derechaMovil}</span>
            <span className="hidden sm:inline">{derecha}</span>
          </>
        ) : (
          derecha
        )}
      </span>
    </nav>
  );
}
