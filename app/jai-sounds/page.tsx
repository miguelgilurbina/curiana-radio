import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import Batea from "@/components/jai-sounds/batea/Batea";
import Canal from "@/components/jai-sounds/Canal";
import { MUSICA, VIAJE } from "@/components/jai-sounds/escrito";
import { CTA_LINEA, PORTADA_DESCUBRIENDO } from "@/components/jai-sounds/estilos";
import { datosEstacion, resumenEstaciones } from "@/lib/jai-wiki";

/** Una sección del escrito: el rótulo § de 72px y el texto a 60ch. */
function Seccion({ id, rotulo, children }: { id: string; rotulo: ReactNode; children: ReactNode }) {
  return (
    <section id={id} className="scroll-mt-16 border-t border-(--jai-rule)">
      <div className="mx-auto grid max-w-[1120px] grid-cols-[repeat(auto-fit,minmax(min(100%,72px),max-content))] gap-x-6 gap-y-4 px-[clamp(16px,4vw,32px)] py-[clamp(56px,8vw,96px)]">
        <span className="jai-dato w-[72px] pt-2 text-[10px] leading-[1.9] text-(--jai-luz-faint)">{rotulo}</span>
        <div className="flex max-w-[60ch] flex-col gap-[22px]">{children}</div>
      </div>
    </section>
  );
}

const PARRAFO = "m-0 text-[17px] leading-[1.75] text-pretty text-(--jai-luz-soft)";
const GRANDE = "jai-manifiesto m-0 text-[clamp(24px,2.6vw,30px)] leading-[1.35] text-(--jai-luz)";

// El HTML inicial lleva solo las primeras filas de la primera estación (la
// más grande tiene 282): el tracklist entero llega enseguida, ya estático.
const FILAS_INICIALES = 30;

export default function JaiSoundsPage() {
  const estaciones = resumenEstaciones();
  const primera = datosEstacion(0);
  const inicial = primera && { ...primera, filas: primera.filas.slice(0, FILAS_INICIALES), parcial: primera.filas.length > FILAS_INICIALES };

  return (
    <>
      {estaciones.length ? (
        <Batea estaciones={estaciones} inicial={inicial} />
      ) : (
        <p className="mx-auto max-w-[1120px] px-8 py-24 text-(--jai-luz-faint)">
          El dial todavía no está exportado: correr <code>npm run jai:exportar</code>.
        </p>
      )}

      {/* Debajo de la música, una sola vez y entero. */}
      <Seccion
        id="la-musica"
        rotulo={
          <>
            § 01
            <br />
            la música
          </>
        }
      >
        <p className={GRANDE}>{MUSICA.entrada}</p>
        <p className={PARRAFO}>{MUSICA.ambiente}</p>
        <p className={PARRAFO}>
          {MUSICA.nota} {MUSICA.historia} {MUSICA.ventanas}
        </p>
        <p className={`${GRANDE} mt-3 border-l-3 border-(--jai-luz) pl-[18px] font-extrabold`}>{MUSICA.cita}</p>
      </Seccion>

      <Seccion
        id="el-viaje"
        rotulo={
          <>
            § 02
            <br />
            el viaje
          </>
        }
      >
        <p className={PARRAFO}>
          {VIAJE.entrada} {VIAJE.sentir}
        </p>
        <p className={PARRAFO}>
          {VIAJE.compartir} {VIAJE.acompaname}
        </p>
        <Link
          href="/jai-sounds/descubriendo"
          className="grid grid-cols-[clamp(88px,18vw,120px)_minmax(0,1fr)] items-center gap-5 border border-(--jai-rule) p-3.5 transition-colors duration-300 hover:border-[#c9c8f5]"
        >
          <Image src={PORTADA_DESCUBRIENDO} alt="Descubriendo con Chocolate" width={240} height={240} sizes="120px" className="block aspect-square w-full object-cover" />
          <span className="flex flex-col gap-2">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">esto es · podcast</span>
            <span className="jai-orbe text-[clamp(22px,2.4vw,28px)] leading-[1.1] text-(--jai-luz)">Descubriendo con Chocolate</span>
            <span className="font-sans text-[11px] font-semibold uppercase tracking-[0.2em] text-(--jai-luz-soft)">acompáñame →</span>
          </span>
        </Link>
      </Seccion>

      <section id="el-canal" data-descubriendo-theme="orbe" className="scroll-mt-16 border-t border-(--orbe-filete) bg-(--orbe-fondo)">
        <div className="mx-auto max-w-[1120px] px-[clamp(16px,4vw,32px)] py-16">
          <Canal rotulo="al aire · el canal de curiana radio">
            <Link
              href="/jai-sounds/descubriendo"
              className={`${CTA_LINEA} border-(--orbe-borde) px-[18px] py-[14px] text-(--orbe-lavanda) hover:border-(--orbe-lavanda) hover:text-(--orbe-texto)`}
            >
              el podcast
            </Link>
          </Canal>
        </div>
      </section>

      <footer className="mx-auto flex max-w-[1120px] flex-wrap justify-between gap-5 px-[clamp(16px,4vw,32px)] pb-[72px] pt-14">
        <span className="jai-dato text-[11px] text-(--jai-luz-faint)">hasta la próxima transmisión. — curiana radio, 88.8 fm</span>
        <Link href="/archivo" className="font-sans text-xs uppercase tracking-[0.2em] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)">
          ver todas las transmisiones →
        </Link>
      </footer>
    </>
  );
}
