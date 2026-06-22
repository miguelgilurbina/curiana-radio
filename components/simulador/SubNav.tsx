"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const TABS = [
  { href: "/simulador", label: "Resumen" },
  { href: "/simulador/personajes", label: "Personajes" },
  { href: "/simulador/lexicon", label: "Léxico" },
  { href: "/simulador/neologisms", label: "Neologismos" },
];

export default function SubNav() {
  const pathname = usePathname();
  return (
    <nav className="flex flex-wrap items-center gap-x-6 gap-y-2 border-b border-earth-200/70">
      {TABS.map((t) => {
        const active = t.href === "/simulador" ? pathname === t.href : pathname?.startsWith(t.href);
        return (
          <Link
            key={t.href}
            href={t.href}
            className={`relative -mb-px border-b-2 pb-2 font-sans text-sm tracking-wide transition-colors ${
              active
                ? "border-frequency text-deep-900"
                : "border-transparent text-earth-600 hover:text-deep-800"
            }`}
          >
            {t.label}
          </Link>
        );
      })}
    </nav>
  );
}
