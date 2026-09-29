import type { ReactNode } from "react";
import Image from "next/image";
import Link from "next/link";
import Canal from "@/components/jai-sounds/Canal";
import Dial from "@/components/jai-sounds/Dial";
import Difuso from "@/components/jai-sounds/Difuso";
import JA from "@/components/jai-sounds/JA";
import { MUSICA, VIAJE } from "@/components/jai-sounds/escrito";
import {
  CAJA,
  CTA_LINEA,
  PORTADA_DESCUBRIENDO,
} from "@/components/jai-sounds/estilos";
import {
  getCenso,
  getEdicionSintonizada,
  getPlaylists,
} from "@/lib/jai-sounds";

// El catálogo cambia cuando corre la ingesta, no cuando entra una visita.
export const revalidate = 3600;

/** La columna del escrito: el rótulo § a la izquierda, el texto a 60ch. */
function Parrafos({
  id,
  rotulo,
  children,
}: {
  id?: string;
  rotulo: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className="scroll-mt-16 border-t border-(--jai-rule)">
      <div
        className={`${CAJA} grid gap-4 py-14 md:grid-cols-[72px_minmax(0,1fr)] md:gap-6 md:py-20`}
      >
        <span className="jai-dato text-[10px] leading-[1.9] text-(--jai-luz-faint) md:pt-2">
          {rotulo}
        </span>
        <div className="flex max-w-[60ch] flex-col gap-[22px]">{children}</div>
      </div>
    </section>
  );
}

/**
 * Una frase del § 01 que sigue sonando más abajo, difusa hasta que pasa por
 * el centro de la pantalla. Llevan el número de su parte para que se lean
 * como un solo texto repartido, no como citas sueltas.
 */
function Interludio({
  parte,
  cita = false,
  children,
}: {
  parte: string;
  cita?: boolean;
  children: ReactNode;
}) {
  return (
    <div
      className={`${CAJA} grid gap-4 py-16 md:grid-cols-[72px_minmax(0,1fr)] md:gap-6 md:py-24`}
    >
      <span className="jai-dato text-[10px] leading-[1.9] text-(--jai-luz-faint) md:pt-3">
        § 01
        <br />
        {parte} / v
      </span>
      <Difuso
        className={`jai-manifiesto max-w-[34ch] text-[clamp(22px,2.6vw,32px)] leading-[1.35] text-(--jai-luz) ${
          cita ? "border-l-3 border-(--jai-luz) pl-[18px] font-extrabold" : ""
        }`}
      >
        {children}
      </Difuso>
    </div>
  );
}

export default async function JaiSoundsPage() {
  const playlists = getPlaylists();
  const censo = await getCenso();
  const edicion = getEdicionSintonizada("01");
  const totalPistas = playlists.reduce((s, p) => s + (p.pistas ?? 0), 0);

  return (
    <>
      {/* ── Hero: el escrito fundacional ──────────────────────────────── */}
      <section
        className={`${CAJA} grid min-h-[600px] grid-rows-[auto_1fr_auto] pt-7 md:min-h-[calc(100svh-4rem)]`}
      >
        <div className="jai-dato flex justify-between gap-4 text-[10px] text-(--jai-luz-faint)">
          <span>jai sounds · jay · oír, escuchar</span>
          <span className="hidden sm:inline">escrito fundacional</span>
        </div>
        <div className="flex flex-col justify-center gap-[26px] py-12">
          <JA tamano="clamp(88px, 9vw, 128px)" />
          <h1 className="jai-display text-[clamp(44px,7vw,96px)] leading-[0.94] text-balance text-(--jai-luz)">
            la huella humana de la vida vivida
          </h1>
          <p className="max-w-[44ch] text-base leading-[1.65] text-(--jai-luz-soft)">
            porque para crear hay que saber sentir, y para saber sentir hay que
            vivir.
          </p>
        </div>
        <div className="jai-dato flex justify-between gap-4 border-t border-(--jai-rule) pb-[22px] pt-4 text-[10px] text-(--jai-luz-faint)">
          <span>§ 01 la música · el dial · § 02 el viaje</span>
          <a
            href="#la-musica"
            className="shrink-0 transition-colors duration-300 hover:text-(--jai-luz)"
          >
            ↓ leer
          </a>
        </div>
      </section>

      {/* ── § 01 la música: el mensaje va primero ─────────────────────── */}
      <Parrafos
        id="la-musica"
        rotulo={
          <>
            § 01
            <br />
            la música
          </>
        }
      >
        <p className="jai-manifiesto text-2xl leading-[1.35] text-(--jai-luz)">
          {MUSICA.entrada}
        </p>
        <p className="text-base leading-[1.75] text-(--jai-luz-soft)">
          {MUSICA.ambiente}
        </p>
      </Parrafos>

      <Interludio parte="ii">{MUSICA.nota}</Interludio>

      {/* ── El dial y la estación sintonizada ─────────────────────────── */}
      <Dial
        estaciones={playlists.map((p) => ({
          slug: p.slug,
          nombre: p.nombre,
          descripcion: p.descripcion,
          pistas: p.pistas,
          portada: p.portada,
          spotify_id: p.spotify_id,
        }))}
        edicion={edicion}
        totalPistas={totalPistas}
        artistas={censo.artistas}
        interludio={<Interludio parte="iii">{MUSICA.historia}</Interludio>}
      />

      <Interludio parte="iv">{MUSICA.ventanas}</Interludio>
      <Interludio parte="v" cita>
        {MUSICA.cita}
      </Interludio>

      {/* ── § 02 el viaje: la voz que entrega al podcast ──────────────── */}
      <Parrafos
        id="el-viaje"
        rotulo={
          <>
            § 02
            <br />
            el viaje
          </>
        }
      >
        <p className="text-base leading-[1.75] text-(--jai-luz-soft)">
          {VIAJE.entrada} {VIAJE.sentir}
        </p>
        <p className="text-base leading-[1.75] text-(--jai-luz-soft)">
          {VIAJE.compartir} {VIAJE.acompaname}
        </p>
        <Link
          href="/jai-sounds/descubriendo"
          className="grid grid-cols-[88px_minmax(0,1fr)] items-center gap-4 border border-(--jai-rule) p-3.5 transition-colors duration-300 hover:border-[#c9c8f5] sm:grid-cols-[120px_minmax(0,1fr)] sm:gap-5"
        >
          <Image
            src={PORTADA_DESCUBRIENDO}
            alt="Descubriendo con Chocolate"
            width={240}
            height={240}
            sizes="120px"
            className="block aspect-square w-full object-cover"
          />
          <span className="flex flex-col gap-2">
            <span className="jai-dato text-[10px] text-(--jai-luz-faint)">
              esto es · podcast
            </span>
            <span className="jai-orbe text-[22px] leading-[1.1] text-(--jai-luz) sm:text-[26px]">
              Descubriendo con Chocolate
            </span>
            <span className="font-sans text-[11px] font-semibold uppercase tracking-[0.2em] text-(--jai-luz-soft)">
              acompáñame →
            </span>
          </span>
        </Link>
      </Parrafos>

      {/* ── Al final: el canal de Curiana Radio, con los episodios ──────
          Es la voz de Chocolate, así que ya lleva el color del orbe. */}
      <section
        id="el-canal"
        data-descubriendo-theme="orbe"
        className="scroll-mt-16 border-t border-(--orbe-filete) bg-(--orbe-fondo)"
      >
        <div className={`${CAJA} py-16`}>
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

      <footer
        className={`${CAJA} flex flex-wrap items-center justify-between gap-5 pb-[72px] pt-14`}
      >
        <span className="jai-dato text-[11px] text-(--jai-luz-faint)">
          hasta la próxima transmisión. — curiana radio, 88.8 fm
        </span>
        <Link
          href="/archivo"
          className="font-sans text-xs uppercase tracking-[0.2em] text-(--jai-luz-soft) transition-colors duration-300 hover:text-(--jai-luz)"
        >
          ver todas las transmisiones →
        </Link>
      </footer>
    </>
  );
}
