"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

// La navegación de la sección, del manual de Kaketiana (design_handoff_
// kaketiana, Vistas §01 y Sistema §06): «Kaketiana» en display; El pueblo ·
// La lengua · Bibliografía en mono y en salina, que es el color de enlace de
// la dirección 6b; [ EXPERIMENTO ] en rúbrica; 88.8 FM chico. En móvil:
// «Kaketiana · 88.8 · [ ≡ ]», con el botón de 44px que abre la lista. La
// sección en que está el lector lleva la Rúbrica (subrayado almagre).
// Reemplaza al masthead de la era 1 y a su cronología lateral (2026-10-02).

const SECCIONES = [
  { href: "/kaketiana/pueblo", label: "El pueblo" },
  { href: "/kaketiana/lengua", label: "La lengua" },
  { href: "/kaketiana/bibliografia", label: "Bibliografía" },
];
const EXPERIMENTO = { href: "/kaketiana/experimento", label: "[ EXPERIMENTO ]" };

function activa(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export default function NavKaketiana() {
  const pathname = usePathname() ?? "";
  const [abierto, setAbierto] = useState(false);

  const enlace = (href: string, label: string, clase: string) => {
    const actual = activa(pathname, href);
    return (
      <Link
        key={href}
        href={href}
        aria-current={actual ? "page" : undefined}
        data-actual={actual ? "" : undefined}
        onClick={() => setAbierto(false)}
        className={`kk-nav-enlace kk-label text-[0.66rem] tracking-[0.18em] ${clase}`}
      >
        {label}
      </Link>
    );
  };

  return (
    <nav aria-label="Kaketiana" className="border-b border-(--sim-rule) bg-(--sim-paper)">
      <div className="mx-auto flex max-w-6xl items-center gap-x-7 px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/kaketiana" onClick={() => setAbierto(false)} className="sim-display text-lg font-semibold text-(--sim-ink)">
          Kaketiana
        </Link>
        <span className="flex-1" />

        {/* ≥ 768px: la fila entera */}
        <div className="hidden items-center gap-x-7 md:flex">
          {SECCIONES.map((s) => enlace(s.href, s.label, "text-(--kk-extra)"))}
          {enlace(EXPERIMENTO.href, EXPERIMENTO.label, "text-(--sim-rubrica)")}
          <Link href="/inicio" className="kk-label text-[0.6rem] tracking-[0.14em] text-(--sim-ink-soft) hover:text-(--sim-rubrica)">
            88.8 FM
          </Link>
        </div>

        {/* < 768px: Kaketiana · 88.8 · [ ≡ ] */}
        <Link href="/inicio" className="kk-label text-[0.6rem] tracking-[0.14em] text-(--sim-ink-soft) md:hidden">
          88.8
        </Link>
        <button
          type="button"
          aria-expanded={abierto}
          aria-controls="kk-nav-menu"
          onClick={() => setAbierto((a) => !a)}
          className="kk-label min-h-11 min-w-11 rounded-[2px] border border-(--sim-rule) px-2.5 text-[0.62rem] tracking-[0.14em] text-(--sim-rubrica) md:hidden"
        >
          {abierto ? "[ × ]" : "[ ≡ ]"}
          <span className="sr-only">{abierto ? "Cerrar el menú" : "Abrir el menú"}</span>
        </button>
      </div>

      <div id="kk-nav-menu" hidden={!abierto} className="kk-desplegable-cuerpo border-t border-(--sim-rule) md:hidden">
        <ul className="mx-auto flex max-w-6xl flex-col px-4 py-2 sm:px-6">
          {[...SECCIONES, EXPERIMENTO].map((s) => (
            <li key={s.href} className="border-b border-(--sim-rule)/60 last:border-b-0">
              <span className="flex min-h-11 items-center">
                {enlace(s.href, s.label, s.href === EXPERIMENTO.href ? "text-(--sim-rubrica)" : "text-(--kk-extra)")}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
