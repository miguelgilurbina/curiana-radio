import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import Canal from "@/components/jai-sounds/Canal";
import JA from "@/components/jai-sounds/JA";
import { VIAJE } from "@/components/jai-sounds/escrito";
import {
  CTA,
  CTA_LINEA,
  PORTADA_DESCUBRIENDO,
  SPOTIFY_SHOW,
} from "@/components/jai-sounds/estilos";

export const metadata: Metadata = {
  title: "Descubriendo con Chocolate — JAI Sounds | Curiana Radio",
  description:
    "Acompáñame a descubrir sonidos pasados que movieron la piel de gente muy viva. El podcast de JAI Sounds, conducido por Chocolate.",
  openGraph: {
    title: "Descubriendo con Chocolate",
    description:
      "Acompáñame a descubrir sonidos pasados. Un podcast de JAI Sounds · Curiana Radio 88.8 FM",
    type: "website",
    images: [PORTADA_DESCUBRIENDO],
  },
};

// Hereda el shell y la tipografía de JAI, pero su superficie sale de la
// portada: índigo-lavanda, un matiz fijo. Es una voz, no una estación.
const CAJA = "mx-auto w-full max-w-[1200px] px-4 sm:px-8";

export default function DescubriendoPage() {
  return (
    <div
      data-descubriendo-theme="orbe"
      className="flex min-h-screen flex-col bg-(--orbe-fondo) text-(--orbe-texto)"
    >
      {/* sub-nav de JAI */}
      <nav
        aria-label="Migas"
        className="jai-dato flex items-center gap-3.5 border-b border-(--orbe-filete) px-4 py-3.5 text-[11px] text-(--orbe-meta) sm:px-8"
      >
        <JA tamano={22} />
        <Link
          href="/jai-sounds"
          className="transition-colors duration-300 hover:text-(--orbe-texto)"
        >
          jai sounds
        </Link>
        <span aria-hidden>/</span>
        <span className="text-(--orbe-texto)" aria-current="page">
          descubriendo con chocolate
        </span>
      </nav>

      {/* hero */}
      <header
        className={`${CAJA} grid items-center gap-10 py-12 md:grid-cols-2 md:gap-14 md:py-16`}
      >
        {/* El lettering de la portada se usa como imagen; no se recompone. */}
        <Image
          src={PORTADA_DESCUBRIENDO}
          alt="Descubriendo con Chocolate — portada"
          width={1333}
          height={1330}
          sizes="(min-width: 768px) 560px, 100vw"
          priority
          className="block aspect-square w-full object-cover"
        />
        <div className="flex min-w-0 flex-col gap-6">
          <span className="jai-dato text-[11px] text-(--orbe-meta)">
            podcast · jai sounds · conducido por chocolate
          </span>
          <h1 className="jai-orbe text-[clamp(40px,5vw,64px)] leading-none text-balance text-(--orbe-texto)">
            Acompáñame a descubrir sonidos pasados
          </h1>
          <p className="max-w-[44ch] font-(family-name:--jai-display) text-xl leading-normal font-normal text-(--orbe-lavanda) [font-variation-settings:'opsz'_36,'SOFT'_50,'WONK'_1]">
            que movieron la piel de gente muy viva. Para desbloquear el
            recuerdo hermoso de días vividos y olvidados. Para revivirlos en el
            presente siempre hambriento de hermosura.
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href={`https://open.spotify.com/show/${SPOTIFY_SHOW}`}
              target="_blank"
              rel="noopener noreferrer"
              className={`${CTA} bg-(--orbe-lavanda) px-[22px] py-[14px] text-(--orbe-fondo) hover:bg-(--orbe-texto)`}
            >
              escuchar el último episodio →
            </a>
            <a
              href="#episodios"
              className={`${CTA_LINEA} border-(--orbe-borde) px-[18px] py-[14px] text-(--orbe-lavanda) hover:border-(--orbe-lavanda) hover:text-(--orbe-texto)`}
            >
              todos los episodios
            </a>
          </div>
        </div>
      </header>

      {/* § 02 el viaje */}
      <section className="border-y border-(--orbe-filete) bg-(--orbe-panel)">
        <div
          className={`${CAJA} grid gap-6 py-16 md:grid-cols-[200px_minmax(0,1fr)] md:gap-10`}
        >
          <span className="jai-dato text-[11px] leading-[1.9] text-(--orbe-meta)">
            § 02
            <br />
            el viaje
            <br />— chocolate
          </span>
          <div className="flex max-w-[65ch] flex-col gap-[22px]">
            <p className="jai-manifiesto text-[26px] leading-[1.35] text-(--orbe-texto) [font-variation-settings:'opsz'_72,'SOFT'_50,'WONK'_1]">
              {VIAJE.entrada}
            </p>
            <p className="text-[17px] leading-[1.75] text-(--orbe-lavanda)">
              {VIAJE.sentir}
            </p>
            <p className="text-[17px] leading-[1.75] text-(--orbe-lavanda)">
              {VIAJE.compartir}
            </p>
          </div>
        </div>
      </section>

      {/* episodios · spotify */}
      <section id="episodios" className={`${CAJA} scroll-mt-16 py-16`}>
        <Canal />
      </section>

      {/* cierre */}
      <section className="border-t border-(--orbe-filete)">
        <div
          className={`${CAJA} flex flex-col items-center gap-5 py-20 text-center`}
        >
          <p className="jai-orbe max-w-[24ch] text-[clamp(28px,3.6vw,44px)] leading-[1.15] text-balance text-(--orbe-texto)">
            porque para crear hay que saber sentir, y para saber sentir hay
            que vivir.
          </p>
          <span className="jai-dato text-[11px] text-(--orbe-meta)">
            esto es descubriendo con chocolate · jai sounds · 88.8 fm
          </span>
        </div>
      </section>

      <footer
        className={`${CAJA} flex flex-wrap justify-between gap-5 border-t border-(--orbe-filete) pb-12 pt-6`}
      >
        <span className="jai-dato text-[11px] text-(--orbe-meta)">
          hasta la próxima transmisión. — curiana radio, 88.8 fm
        </span>
        <Link
          href="/jai-sounds"
          className="font-sans text-xs uppercase tracking-[0.2em] text-(--orbe-lavanda) transition-colors duration-300 hover:text-white"
        >
          ← volver a jai sounds
        </Link>
      </footer>
    </div>
  );
}
