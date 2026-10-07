import Link from "next/link";
import { fechaLarga, getSenales, type Arista } from "@/lib/senales";

// Las señales de una arista, dentro de su sección: así cada arista se va
// alimentando del blog. Habla en el registro de la superficie donde cae
// (la placa de Kaketiana, el dial de JAI, el papel de la Galería) y no sale
// si la arista todavía no tiene señales. El título va en la display de cada
// sección: la Fraunces del cronista, la de JAI, la Lora del papel.

const TONOS = {
  kaketiana: {
    filete: "border-(--sim-rule)",
    fuente: "sim-display",
    rotulo: "kk-label text-(--sim-rubrica)",
    fecha: "text-(--sim-ink-soft)",
    titulo: "text-(--sim-ink) group-hover:text-(--sim-rubrica)",
    sumario: "text-(--sim-ink-soft)",
    accion: "text-(--kk-extra) hover:text-(--sim-rubrica)",
  },
  "jai-sounds": {
    filete: "border-(--jai-rule)",
    fuente: "font-(family-name:--jai-display)",
    rotulo: "text-(--jai-luz-soft)",
    fecha: "text-(--jai-luz-soft)",
    titulo: "text-(--jai-luz) group-hover:text-(--jai-senal)", // frequency nunca dentro de JAI
    sumario: "text-(--jai-luz-soft)",
    accion: "text-(--jai-luz-soft) hover:text-(--jai-luz)",
  },
  galeria: {
    filete: "border-earth-200",
    fuente: "font-serif",
    rotulo: "text-earth-600",
    fecha: "text-earth-600",
    titulo: "text-deep-900 group-hover:text-frequency",
    sumario: "text-earth-700",
    accion: "text-deep-700 hover:text-frequency",
  },
} as const satisfies Partial<Record<Arista, Record<string, string>>>;

export default function SenalesDeArista({
  arista,
  className = "",
}: {
  arista: keyof typeof TONOS;
  className?: string;
}) {
  const senales = getSenales({ arista, limite: 3 });
  if (!senales.length) return null;
  const t = TONOS[arista];
  const mono = "font-mono text-[0.7rem] uppercase tracking-[0.18em]";

  return (
    <section aria-labelledby={`senales-${arista}`} className={className}>
      <h2 id={`senales-${arista}`} className={`m-0 mb-6 ${mono} ${t.rotulo}`}>
        Señales · desde acá
      </h2>
      <div className="grid gap-x-8 [grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr))]">
        {senales.map((s) => (
          <Link key={s.slug} href={`/senales/${s.slug}`} className={`group flex flex-col gap-2 border-t py-6 ${t.filete}`}>
            <time dateTime={s.fecha} className={`${mono} ${t.fecha}`}>
              {fechaLarga(s.fecha)}
            </time>
            <span className={`${t.fuente} text-xl font-semibold leading-snug transition-colors duration-300 ${t.titulo}`}>
              {s.titulo}
            </span>
            <span className={`text-sm leading-relaxed ${t.sumario}`}>{s.sumario}</span>
          </Link>
        ))}
      </div>
      <Link href="/senales" className={`mt-2 inline-block ${mono} transition-colors duration-300 ${t.accion}`}>
        Todas las señales →
      </Link>
    </section>
  );
}
