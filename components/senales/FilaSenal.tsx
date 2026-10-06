import Link from "next/link";
import type { CSSProperties } from "react";
import { ARISTAS, fechaCorta, type SenalResumen } from "@/lib/senales-comun";

// Una señal en el índice (design_handoff_senales_luces, «Índice de Señales»):
// el sello de su arista alineado a la primera línea, el título en Lora 600, el
// sumario en Lora itálica y el dato en mono. Vive en la piel de la radio, así
// que lee sus alias y sigue la luz del lector.
export default function FilaSenal({ senal }: { senal: SenalResumen }) {
  const arista = senal.aristas[0];
  const etiqueta = senal.aristas.length ? senal.aristas.map((a) => ARISTAS[a].corto).join(" · ") : "La radio";
  return (
    <Link
      href={`/senales/${senal.slug}`}
      className="group grid grid-cols-[7px_minmax(0,1fr)] gap-4 border-t border-(--e-filete) py-5 text-(--e-texto)"
    >
      <i
        aria-hidden="true"
        className="mt-[0.7em] block h-[7px] w-[7px]"
        style={{ background: `var(--sello-${arista ?? "radio"})` } as CSSProperties}
      />
      <span className="flex flex-col gap-1.5">
        <span className="font-serif text-[clamp(1.25rem,2.6vw,1.6rem)] leading-[1.25] font-semibold transition-colors duration-300 group-hover:text-(--e-enlace-hover)">
          {senal.titulo}
        </span>
        <span className="font-serif text-base leading-[1.5] italic text-(--e-texto-2)">{senal.sumario}</span>
        <span className="font-mono text-[0.6875rem] tracking-[0.24em] text-(--e-texto-2) uppercase">
          {etiqueta} · <time dateTime={senal.fecha}>{fechaCorta(senal.fecha)}</time> · {senal.minutos} min
          {senal.borrador && " · borrador"}
        </span>
      </span>
    </Link>
  );
}
