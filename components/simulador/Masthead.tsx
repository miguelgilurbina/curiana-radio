import Link from "next/link";
import { Overline } from "@/components/simulador/ui";

// Masthead de revista: filete doble, nameplate en display, línea de edición.
// Habla en tokens --sim-*: sobre el pergamino es tinta parda; dentro del
// Acto I "laboratorio" se resuelve solo al registro oscuro del instrumento.
//
// El nameplate es «Kaketiana» — 'el lugar de la gente', de `kaketio` 'ser
// viviente' (Oliver 1989, Tabla A-9) y `-ana` 'lugar de' (atestiguado en
// Paraguaná y Curiana). La palabra es un compuesto nuestro sobre morfemas
// atestiguados; la portada lo declara, y por eso aquí no lleva asterisco.
export default function Masthead() {
  return (
    <header className="mb-10">
      <div className="sim-double-rule" aria-hidden="true" />
      <div className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-1 py-3">
        <Link href="/kaketiana" className="group">
          <h1 className="sim-display text-4xl font-semibold tracking-tight text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego) md:text-5xl">
            Kaketiana
          </h1>
        </Link>
        <Overline>El mundo del kaketío · 88.8 FM</Overline>
      </div>
      <div className="border-b border-(--sim-ink)" aria-hidden="true" />
      <p className="sim-mono mt-2 text-[0.65rem] uppercase tracking-[0.14em] text-(--sim-ink-faint)">
        Golfete de Coro · Siglos XIV–XV · Una crónica que se sigue escribiendo
      </p>
    </header>
  );
}
