import Link from "next/link";
import type { CSSProperties, ReactNode } from "react";
import type { ArchiveItem } from "@/types/edition";
import { Cartel } from "@/components/ui/Typography";
import Cenefa from "@/components/ui/Cenefa";
import { fechaLarga, type SenalResumen } from "@/lib/senales-comun";
import Etiquetas from "@/components/senales/Etiquetas";
import { PORTAFOLIO } from "@/lib/redes";
import { LIBERADA, registros } from "@/lib/secciones";
import Aparece from "./Aparece";
import Suscripcion from "./Suscripcion";
import SeguirLeyendo from "./SeguirLeyendo";

// Las secciones 02–07 de la landing v1 · la noche. El orden, el copy y las
// superficies vienen del handoff (design_handoff_landing/README.md); la
// paleta es la de la noche (BRAND_MVP.md §10). Ritmo: 112 px entre
// secciones, contenedor de 72rem, columnas de lectura de 65ch.

/** Overline "tono radio" del sistema, en hueso-2 sobre la noche */
function Overline({ children }: { children: ReactNode }) {
  return (
    <span className="inline-block text-[0.7rem] font-medium uppercase tracking-[0.18em] text-(--noche-hueso-2)">
      {children}
    </span>
  );
}

const CTA_NARANJA =
  "inline-block rounded-[2px] bg-(--noche-acento) px-7 py-[15px] text-[0.78rem] font-semibold uppercase tracking-[0.2em] whitespace-nowrap text-(--noche-fondo) transition-all duration-300 hover:bg-(--noche-hueso) hover:text-(--noche-fondo)";

// ── 02 · Manifiesto ───────────────────────────────────────────────────────
export function Manifiesto() {
  return (
    <section
      id="manifiesto"
      aria-labelledby="manifiesto-titulo"
      className="noche-gradiente noche-grano px-6 py-28"
    >
      <Aparece className="relative z-[1] mx-auto max-w-[65ch]">
        <div className="mb-8 flex flex-wrap items-baseline gap-4">
          <Cartel as="h2" className="text-[clamp(1.5rem,3vw,2.2rem)]">
            <span id="manifiesto-titulo">Manifiesto</span>
          </Cartel>
          <Overline>Renacimiento de La Curiana</Overline>
        </div>
        <p className="mb-10 font-serif text-intro italic text-(--noche-hueso-2)">
          Transmitimos desde después.
        </p>
        {/* Capitular con ::first-letter: el texto sigue diciendo "Aquí" entero */}
        <p className="mb-6 text-body text-(--noche-hueso) first-letter:float-left first-letter:pt-1.5 first-letter:pr-3.5 first-letter:font-serif first-letter:text-[4.4rem] first-letter:leading-[0.8] first-letter:font-semibold">
          Aquí la refinería es un museo de energía renovable y el viento del
          istmo es una moneda que no se agota. No hace falta convencerte de
          nada: el cambio ya pasó. Esto no es propaganda para el cambio — es
          propaganda desde después del cambio, enviada a tu tiempo como quien
          deja una señal encendida en la costa.
        </p>
        <SeguirLeyendo>
          <p className="mb-6 text-body text-(--noche-hueso)">
            Lo que suena en esta frecuencia es un sincretismo: la tecnología
            biológica y social de los caquetíos — la reciprocidad de{" "}
            <em>la buena gente</em>, la escucha como instrumento, la espiral
            como mapa — conectada a la tecnología presente de la inteligencia
            artificial. El silicio es tierra. La antena y el totumo vibran
            igual.
          </p>
          <p className="m-0 text-body text-(--noche-hueso)">
            Cada mes, una transmisión: cinco pistas comentadas al oído, un
            ensayo híbrido entre lo ancestral y lo sintético, una lengua que se
            reconstruye palabra a palabra, y el arte que va quedando en el
            camino.
          </p>
        </SeguirLeyendo>
        <blockquote className="mt-14 border-l-4 border-(--noche-acento)/30 pl-6 font-serif text-[1.875rem] leading-relaxed italic text-(--noche-hueso)">
          La tecnología más antigua es la escucha.
          <cite className="mt-4 block font-sans text-sm tracking-[0.025em] not-italic text-(--noche-hueso-2)">
            {"// transmisión continua · el silicio es tierra"}
          </cite>
        </blockquote>
      </Aparece>
    </section>
  );
}

// ── Quién transmite ──────────────────────────────────────────────────────
// Después del Manifiesto, la ficción se dice como ficción: quién hace la radio
// y desde dónde (Miguel, 2026-10-05: «una mini intro sobre Curiana Radio, y mi
// persona, linkeando mi portafolio»). La página entera está en /sobre.
const ACCION_NOCHE =
  "font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento)";

export function QuienTransmite() {
  return (
    <section
      id="quien-transmite"
      aria-labelledby="quien-transmite-titulo"
      className="bg-(--noche-hondo) px-6 py-20"
    >
      <Aparece className="mx-auto flex max-w-[65ch] flex-col gap-5">
        <div className="flex flex-wrap items-baseline gap-4">
          <Cartel as="h2" className="text-[clamp(1.4rem,3vw,2rem)]">
            <span id="quien-transmite-titulo">Quién transmite</span>
          </Cartel>
          <Overline>Fuera del aire</Overline>
        </div>
        <p className="m-0 text-body text-(--noche-hueso)">
          Curiana Radio es el laboratorio creativo de Miguel Gil Urbina: una
          radio del futuro que se sintoniza desde acá, con memoria donde casi
          nunca la hay. La ficción es el marco; la voz es suya.
        </p>
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2">
          <Link href="/sobre" className={ACCION_NOCHE}>
            CONOCER LA RADIO →
          </Link>
          <a
            href={PORTAFOLIO.url}
            target="_blank"
            rel="noopener noreferrer"
            className={ACCION_NOCHE}
          >
            {PORTAFOLIO.texto.toUpperCase()} ↗
          </a>
        </div>
      </Aparece>
    </section>
  );
}

// ── Señales ──────────────────────────────────────────────────────────────
// Lo que escribe Miguel desde acá (app/senales, lib/senales.ts): la radio
// transmite desde después, y aquí aparece quién la sintoniza. La más reciente
// va destacada; las otras dos, en tarjetas. Sin señales, la sección no sale.
const MONO_META =
  "font-mono text-[0.7rem] tracking-[0.16em] text-(--noche-hueso-2)";

function MetaSenal({ senal }: { senal: SenalResumen }) {
  return (
    <span
      className={`flex flex-wrap items-center gap-x-4 gap-y-1 ${MONO_META}`}
    >
      <time dateTime={senal.fecha}>
        {fechaLarga(senal.fecha).toUpperCase()}
      </time>
      <Etiquetas aristas={senal.aristas} enlazar={false} sello />
    </span>
  );
}

export function Senales({ senales }: { senales: SenalResumen[] }) {
  if (!senales.length) return null;
  const [destacada, ...resto] = senales;
  return (
    <section
      id="senales"
      aria-labelledby="senales-titulo"
      className="bg-(--noche-fondo) px-6 py-28"
    >
      <Aparece className="mx-auto max-w-[72rem]">
        <div className="mb-12 flex flex-wrap items-baseline gap-4">
          <Cartel as="h2" className="text-[clamp(1.6rem,3.4vw,2.5rem)]">
            <span id="senales-titulo">Señales</span>
          </Cartel>
          <Overline>
            Desde acá · escribe{" "}
            <Link
              href="/sobre"
              className="underline-offset-4 transition-colors duration-300 hover:text-(--noche-acento) hover:underline"
            >
              Miguel Gil Urbina
            </Link>
          </Overline>
        </div>

        <Link
          href={`/senales/${destacada.slug}`}
          className={`group grid gap-10 border-t border-(--noche-filete) pt-10 ${destacada.portada ? "lg:grid-cols-[1.1fr_1fr] lg:items-center" : ""}`}
        >
          {destacada.portada && (
            // eslint-disable-next-line @next/next/no-img-element -- Vercel Blob tal cual, como la galería
            <img
              src={destacada.portada.src}
              alt={destacada.portada.alt}
              loading="lazy"
              decoding="async"
              className="block aspect-[16/10] w-full bg-(--noche-panel) object-cover"
            />
          )}
          <div className="flex max-w-[60ch] flex-col gap-4">
            <MetaSenal senal={destacada} />
            <h3 className="m-0 font-serif text-[clamp(1.9rem,4vw,2.8rem)] font-semibold leading-[1.12] text-(--noche-hueso) transition-colors duration-300 group-hover:text-(--noche-acento)">
              {destacada.titulo}
            </h3>
            <p className="m-0 font-serif text-xl leading-relaxed italic text-(--noche-hueso-2)">
              {destacada.sumario}
            </p>
            <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso)">
              LEER LA SEÑAL · {destacada.minutos} MIN →
            </span>
          </div>
        </Link>

        {resto.length > 0 && (
          <div className="mt-14 grid gap-8 [grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr))]">
            {resto.map((s) => (
              <Link
                key={s.slug}
                href={`/senales/${s.slug}`}
                className="group flex flex-col gap-3 border-t border-(--noche-filete) pt-6"
              >
                <MetaSenal senal={s} />
                <h3 className="m-0 font-serif text-[1.4rem] font-semibold leading-snug text-(--noche-hueso) transition-colors duration-300 group-hover:text-(--noche-acento)">
                  {s.titulo}
                </h3>
                <p className="m-0 text-sm leading-relaxed text-(--noche-hueso-2)">
                  {s.sumario}
                </p>
              </Link>
            ))}
          </div>
        )}

        <Link
          href="/senales"
          className="mt-14 inline-block font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento)"
        >
          TODAS LAS SEÑALES →
        </Link>
      </Aparece>
    </section>
  );
}

// ── 03 · Interludio de arte ──────────────────────────────────────────────
// Cada hueco reserva el color dominante de su obra mientras carga.
const OBRAS = [
  {
    archivo: "collage-curiana-1",
    alt: "Collage Curiana — trama y semitono",
    leyenda:
      "collage-curiana-1 — trama y semitono · la espiral como cenefa · dominante #2a6fac",
    dominante: "#2a6fac",
  },
  {
    archivo: "curiana-abstract",
    alt: "Curiana Abstract — script pincel sobre arquitectura deformada",
    leyenda:
      "curiana-abstract — script pincel · arquitectura en warp · dominante #2fa89a",
    dominante: "#2fa89a",
  },
  {
    archivo: "cuentos-de-buchibe",
    alt: "Los Cuentos de Buchibe — cromo tubular sobre telón",
    leyenda:
      "cuentos-de-buchibe — cromo tubular · el telón y el monte · dominante #8c2b12",
    dominante: "#8c2b12",
  },
];

export function Interludio() {
  return (
    <section
      id="interludio"
      aria-labelledby="interludio-titulo"
      data-galeria-theme="sala"
      className="bg-(--gal-sala) px-6 py-28"
    >
      <Aparece className="mx-auto max-w-[72rem]">
        <div className="mb-12 flex flex-col gap-2.5">
          <span className="font-mono text-[0.7rem] font-medium uppercase tracking-[0.3em] text-(--gal-luz-soft)">
            Interludio · la sala
          </span>
          <Cartel
            as="h2"
            className="text-[clamp(1.6rem,3.4vw,2.5rem)] whitespace-normal sm:whitespace-nowrap"
          >
            <span id="interludio-titulo">Concept art del Renacimiento</span>
          </Cartel>
          <p className="m-0 max-w-[52ch] text-sm text-(--gal-luz-soft)">
            La interfaz calla donde el arte habla. Cada hueco reserva el color
            dominante de su obra.
          </p>
        </div>
        <div className="grid gap-7 [grid-template-columns:repeat(auto-fit,minmax(260px,1fr))]">
          {OBRAS.map((o) => (
            <figure key={o.archivo} className="m-0 flex flex-col gap-3">
              <div
                className="aspect-square"
                style={{ background: o.dominante }}
              >
                {/* eslint-disable-next-line @next/next/no-img-element -- WebP pre-generados, como la galería */}
                <img
                  src={`/landing/${o.archivo}-480.webp`}
                  srcSet={`/landing/${o.archivo}-480.webp 480w, /landing/${o.archivo}-960.webp 960w`}
                  sizes="(min-width: 72rem) 370px, (min-width: 640px) 45vw, 100vw"
                  width={960}
                  height={960}
                  alt={o.alt}
                  loading="lazy"
                  decoding="async"
                  className="block h-full w-full object-cover"
                />
              </div>
              <figcaption className="font-mono text-[0.72rem] leading-relaxed text-(--gal-luz-soft)">
                {o.leyenda}
              </figcaption>
            </figure>
          ))}
        </div>
      </Aparece>
    </section>
  );
}

// ── 04 · Las aristas ─────────────────────────────────────────────────────
// Cada tarjeta conserva su registro; sobre la noche se leen como ventanas.
const TARJETA =
  "flex min-h-[230px] flex-col gap-3.5 px-8 py-9 transition-all duration-300";

export function Aristas() {
  return (
    <section
      id="aristas"
      aria-labelledby="aristas-titulo"
      className="bg-(--noche-fondo) px-6 py-28"
    >
      <Aparece className="mx-auto max-w-[72rem]">
        <div className="mb-12 flex flex-wrap items-baseline gap-4">
          <Cartel as="h2" className="text-[clamp(1.6rem,3.4vw,2.5rem)]">
            <span id="aristas-titulo">Las aristas</span>
          </Cartel>
          <Overline>
            Una emisora ·{" "}
            {registros(
              Object.values(LIBERADA).filter(Boolean).length -
                (LIBERADA.archivo ? 1 : 0),
            )}
          </Overline>
        </div>
        <div className="grid gap-6 [grid-template-columns:repeat(auto-fit,minmax(300px,1fr))]">
          <Link
            href="/jai-sounds"
            data-jai-theme="dial"
            style={{ "--jai-hue": "212" } as CSSProperties}
            className={`${TARJETA} border-l-[3px] border-(--jai-senal) bg-(--jai-panel) hover:border-(--noche-acento) hover:shadow-xl`}
          >
            <span className="font-mono text-[0.68rem] uppercase tracking-[0.3em] text-(--jai-luz-soft)">
              I · jai · caquetío · oír, escuchar
            </span>
            <Cartel as="h3" className="text-[1.7rem]">
              JAI Sounds
            </Cartel>
            <p className="m-0 flex-1 text-sm leading-relaxed text-(--jai-luz-soft)">
              La cabina de noche. Cinco pistas por emisión, reseñadas al oído;
              un dial de estaciones cuyo color rota con cada visita.
            </p>
            <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--jai-luz)">
              ENTRAR AL DIAL →
            </span>
          </Link>

          <Link
            href="/kaketiana"
            data-sim-theme="cronista"
            data-kk-dir="sal"
            className={`${TARJETA} rounded-2xl border border-(--sim-rule) bg-(--sim-paper) hover:border-(--noche-acento) hover:shadow-lg`}
          >
            <span className="text-[0.68rem] font-medium uppercase tracking-[0.18em] text-(--sim-rubrica)">
              II · Golfete de Coro · s. XIV–XV
            </span>
            <Cartel as="h3" className="text-[1.7rem]">
              Kaketiana
            </Cartel>
            <p className="m-0 flex-1 text-sm leading-relaxed text-(--sim-ink-soft)">
              El wiki de investigación: el pueblo caquetío del Golfete de Coro y
              su lengua, reconstruidos sin fingir saber más de lo que se sabe.
              Cada afirmación, con su fuente.
            </p>
            <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--sim-ink)">
              ENTRAR A KAKETIANA →
            </span>
          </Link>

          {LIBERADA.galeria && (
            <Link
              href="/galeria"
              data-galeria-theme="sala"
              className={`${TARJETA} border border-(--gal-rule) bg-(--gal-sala) hover:border-(--noche-acento) hover:shadow-xl`}
            >
              <span className="font-mono text-[0.68rem] uppercase tracking-[0.3em] text-(--gal-luz-soft)">
                III · La sala neutra
              </span>
              <Cartel
                as="h3"
                className="text-[1.7rem] whitespace-normal sm:whitespace-nowrap"
              >
                Galería · Prompt Maker
              </Cartel>
              <p className="m-0 flex-1 text-sm leading-relaxed text-(--gal-luz-soft)">
                Cientos de visiones generadas y curadas. El prompt es código y
                se publica a la vista, junto al color dominante de cada obra.
              </p>
              <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--gal-luz)">
                RECORRER LA SALA →
              </span>
            </Link>
          )}

          {/* Buchibe aún no tiene sección: la tarjeta anuncia el telón, no enlaza. */}
          {LIBERADA.buchibe && (
            <article
              data-buchibe-theme="telon"
              className="flex min-h-[230px] flex-col overflow-hidden bg-(--buc-telon)"
            >
              <div
                aria-hidden="true"
                className="flex flex-col items-center gap-0.5 px-8 py-3.5"
                style={{
                  background:
                    "linear-gradient(180deg, var(--buc-noche), var(--buc-ultramar))",
                }}
              >
                <span className="sim-display text-[0.78rem] uppercase tracking-[0.32em] text-(--buc-oro) [font-family:var(--font-fraunces),var(--font-lora),Georgia,serif]">
                  Curiana Radio
                </span>
                <span className="sim-display text-[0.66rem] italic tracking-[0.18em] text-(--buc-oro) [font-family:var(--font-fraunces),var(--font-lora),Georgia,serif]">
                  presenta
                </span>
              </div>
              <div className="flex flex-1 flex-col gap-3.5 px-8 pt-[26px] pb-9">
                <Cartel as="h3" className="text-[1.7rem]">
                  Cuentos de Buchibe
                </Cartel>
                <p className="m-0 flex-1 text-sm leading-relaxed text-(--buc-luz)">
                  El telón. Narrativa oral del Príncipe Cayerúa: cuentos que se
                  leen — o se escuchan — bajo un cielo ultramar.
                </p>
                <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--buc-luz)">
                  CORRER EL TELÓN · PRONTO
                </span>
              </div>
            </article>
          )}
        </div>
      </Aparece>
    </section>
  );
}

// ── 05 · Última transmisión ──────────────────────────────────────────────
export function UltimaTransmision({ edicion }: { edicion: ArchiveItem }) {
  return (
    <section
      id="transmision"
      aria-labelledby="transmision-titulo"
      className="noche-gradiente noche-grano px-6 py-28"
    >
      <Aparece className="relative z-[1] mx-auto flex max-w-[72rem] flex-wrap items-center justify-center gap-14">
        {edicion.portada && (
          <div className="min-w-[280px] flex-[0_1_380px]">
            <Cenefa color="#e8c76b" fondo="#26396a" tamano={34} opacidad={0.85}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={edicion.portada}
                width={640}
                height={640}
                alt={`Portada de la Edición #${edicion.number} — ${edicion.title}`}
                className="block h-auto w-full"
              />
            </Cenefa>
          </div>
        )}
        <div className="flex max-w-[560px] flex-[1_1_420px] flex-col gap-4">
          <Overline>Última transmisión · Edición #{edicion.number}</Overline>
          <Cartel
            as="h2"
            className="text-[clamp(2rem,4.4vw,3.2rem)] leading-none whitespace-normal"
          >
            <span id="transmision-titulo">{edicion.title}</span>
          </Cartel>
          <span className="font-serif text-2xl italic text-(--noche-hueso-2)">
            {edicion.theme}
          </span>
          <p className="m-0 text-body text-(--noche-hueso)">
            {edicion.sinopsis ?? edicion.description}
          </p>
          {edicion.ficha && (
            <span className="font-mono text-[0.78rem] tracking-[0.1em] text-(--noche-hueso-2)">
              {edicion.ficha}
            </span>
          )}
          <div className="mt-3 flex flex-wrap items-center gap-5">
            <Link href={`/${edicion.slug}`} className={CTA_NARANJA}>
              Sintonizar ahora →
            </Link>
            <Link
              href="/archivo"
              className="text-sm text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento)"
            >
              Ver todas las transmisiones →
            </Link>
          </div>
        </div>
      </Aparece>
    </section>
  );
}

// ── 06 · Archivo y suscripción ───────────────────────────────────────────
export function ArchivoSuscripcion({
  ediciones,
}: {
  ediciones: ArchiveItem[];
}) {
  const ultima = ediciones.length
    ? Math.max(...ediciones.map((e) => Number(e.number)))
    : 0;
  const proxima = String(ultima + 1).padStart(2, "0");
  return (
    <section
      id="archivo"
      aria-label="Archivo y suscripción"
      className="bg-(--noche-fondo) px-6 py-28"
    >
      <Aparece className="mx-auto grid max-w-[72rem] gap-12 [grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr))]">
        <div className="flex flex-col gap-5">
          <Cartel as="h2" className="text-2xl">
            Archivo
          </Cartel>
          {ediciones.map((e) => (
            <Link
              key={e.slug}
              href={`/${e.slug}`}
              className="flex items-center gap-5 rounded-lg border border-(--noche-filete) bg-(--noche-panel) px-6 py-5 transition-all duration-300 hover:border-(--noche-acento) hover:shadow-lg"
            >
              <span className="font-mono text-[0.85rem] font-medium text-(--noche-acento)">
                #{e.number}
              </span>
              <span className="flex flex-1 flex-col gap-0.5">
                <span className="font-serif text-lg font-semibold text-(--noche-hueso)">
                  {e.title}
                </span>
                <span className="text-sm italic text-(--noche-hueso-2)">
                  {e.theme}
                </span>
              </span>
              <span aria-hidden="true" className="text-(--noche-hueso-2)">
                →
              </span>
            </Link>
          ))}
          <span className="font-mono text-[0.72rem] tracking-[0.14em] text-(--noche-hueso-2)">
            UNA EMISIÓN AL MES · LA #{proxima} YA SE ESTÁ AFINANDO
          </span>
        </div>
        <div className="flex flex-col gap-5 rounded-2xl border border-(--noche-filete) bg-(--noche-panel) p-6 sm:p-10">
          <Cartel as="h2" className="text-2xl">
            Suscríbete
          </Cartel>
          <p className="m-0 text-base leading-relaxed text-(--noche-hueso)">
            Que la próxima emisión te encuentre. Sin ruido de más: una señal al
            mes, directa a tu correo.
          </p>
          <Suscripcion />
        </div>
      </Aparece>
    </section>
  );
}

// ── 07 · Colofón ─────────────────────────────────────────────────────────
// El colofón de la landing pasó al pie común de la noche (components/shell/
// PieNoche.tsx, shell 1a): el sello, «El viento no borra, reescribe.», las
// estaciones, la suscripción y la línea legal. El burro ASCII sigue en el 404.
