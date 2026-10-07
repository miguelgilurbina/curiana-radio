import Link from "next/link";

/** Mientras la ficha llega del servidor: esqueletos que laten, sin saltos. */
export function Cargando() {
  return (
    <div className="mx-auto flex max-w-[1120px] flex-col gap-[clamp(56px,7vw,88px)] px-[clamp(16px,4vw,32px)] pb-24 pt-[108px]">
      <section className="grid items-end gap-x-12 gap-y-10 min-[820px]:grid-cols-[minmax(0,300px)_minmax(0,1fr)]">
        <div className="jai-latido aspect-square max-w-[220px] bg-(--jai-panel) min-[820px]:max-w-none" />
        <div className="flex flex-col gap-4">
          <span className="jai-dato text-[11px] text-(--jai-luz-faint)">sintonizando · la ficha llega del servidor</span>
          <span className="jai-latido h-[52px] w-[78%] bg-(--jai-panel)" />
          <span className="jai-latido h-5 w-[40%] bg-(--jai-panel)" />
          <span className="jai-latido h-16 w-full bg-(--jai-panel)" />
        </div>
      </section>
      <section className="grid gap-x-12 gap-y-10 min-[820px]:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]">
        <div className="flex flex-col gap-2.5">
          <span className="h-2.5 w-[30%] bg-(--jai-panel)" />
          <span className="jai-latido h-[120px] bg-(--jai-panel)" />
        </div>
        <div className="jai-latido h-40 bg-(--jai-panel)" />
      </section>
    </div>
  );
}

/** Lo que no está en el dial. */
export function Perdido() {
  return (
    <div className="mx-auto max-w-[1120px] px-[clamp(16px,4vw,32px)] py-24">
      <section className="flex max-w-[60ch] flex-col gap-3.5 border-l-3 border-(--jai-luz-faint) pl-6">
        <span className="jai-dato text-[11px] text-(--jai-luz-faint)">{"// esto no está en el dial"}</span>
        <p className="jai-manifiesto m-0 text-2xl leading-[1.4] text-(--jai-luz)">El viento no borra, reescribe. Vuelve a la batea y sigue por otro disco.</p>
        <Link href="/jai-sounds" className="jai-dato text-[11px] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
          [ volver a la batea ]
        </Link>
      </section>
    </div>
  );
}
