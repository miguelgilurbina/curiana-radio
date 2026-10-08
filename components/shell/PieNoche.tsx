import Link from "next/link";
import Sello from "./Sello";
import EscalaDial from "./EscalaDial";
import LuzNativa from "./LuzNativa";
import Suscripcion from "@/components/landing/Suscripcion";
import { REDES } from "@/lib/redes";
import { LIBERADA } from "@/lib/secciones";
import { SPOTIFY_SHOW } from "@/components/jai-sounds/estilos";

// El pie de la noche: shell 1a «El dial» (design_handoff_senales_luces/shell/
// SHELL.md). El sello grande con el proverbio, tres columnas —las
// estaciones, la emisora y la señal de cada mes—, la escala del dial con su
// aguja y la línea legal. Es el colofón común de la landing, Señales y
// «Quién transmite».

const OVERLINE = "font-mono text-[0.625rem] tracking-[0.3em] text-(--noche-dato)";
const ENLACE =
  "flex min-h-11 items-center text-[0.9375rem] text-(--noche-hueso-2) transition-colors duration-300 hover:text-(--noche-acento) lg:min-h-0";
const LEGAL = "font-mono text-[0.625rem] tracking-[0.24em] text-(--noche-dato)";

export default function PieNoche({
  edicion,
  haySenales,
}: {
  edicion: { numero: string };
  /** sin señales que mostrar, el enlace a Señales no sale (lib/senales.ts) */
  haySenales: boolean;
}) {
  return (
    <footer className="shell-noche border-t border-(--noche-filete) bg-(--noche-fondo) px-4 pt-12 pb-7 lg:px-10 lg:pt-[72px] lg:pb-8">
      <div className="mx-auto flex max-w-[1280px] flex-col gap-8 lg:gap-14">
        <div className="grid gap-8 lg:grid-cols-[minmax(0,1.4fr)_repeat(3,minmax(0,1fr))] lg:gap-12">
          {/* el sello y el proverbio */}
          <div className="flex items-center gap-[18px] lg:flex-col lg:items-start lg:gap-6">
            <Sello tamano={96} className="lg:hidden" />
            <Sello tamano={150} className="hidden lg:block" />
            <p className="m-0 max-w-[30ch] font-serif text-[1.0625rem] leading-[1.5] italic text-(--noche-hueso) lg:text-[1.1875rem] lg:leading-[1.55]">
              «El viento no borra, reescribe.»
            </p>
          </div>

          {/* en el móvil, las dos columnas de enlaces se juntan */}
          <div className="grid grid-cols-2 gap-x-4 gap-y-6 lg:contents">
            <nav aria-label="Estaciones" className="flex flex-col lg:gap-3.5">
              <span className={`${OVERLINE} mb-1 lg:mb-0`}>ESTACIONES</span>
              <Link href="/jai-sounds" className={ENLACE}>
                JAI Sounds
              </Link>
              <Link href="/kaketiana" className={ENLACE}>
                Kaketiana
              </Link>
              {LIBERADA.galeria && (
                <Link href="/galeria" className={ENLACE}>
                  Galería · Prompt Maker
                </Link>
              )}
              {LIBERADA.buchibe && (
                <span className={`${ENLACE} text-(--noche-dato) hover:text-(--noche-dato)`}>
                  Cuentos de Buchibe<span className="sr-only"> (pronto)</span>
                </span>
              )}
            </nav>

            <nav aria-label="La emisora" className="flex flex-col lg:gap-3.5">
              <span className={`${OVERLINE} mb-1 lg:mb-0`}>LA EMISORA</span>
              <Link href="/inicio#manifiesto" className={ENLACE}>
                Manifiesto
              </Link>
              {haySenales && (
                <Link href="/senales" className={ENLACE}>
                  Señales
                </Link>
              )}
              <Link href="/sobre" className={ENLACE}>
                Quién transmite
              </Link>
              {LIBERADA.archivo && (
                <Link href="/archivo" className={ENLACE}>
                  Ver todas las transmisiones →
                </Link>
              )}
              <a
                href={`https://open.spotify.com/show/${SPOTIFY_SHOW}`}
                target="_blank"
                rel="noopener noreferrer"
                className={ENLACE}
              >
                Spotify
              </a>
              {REDES.map((r) => (
                <a key={r.nombre} href={r.url} target="_blank" rel="noopener noreferrer" className={ENLACE}>
                  {r.nombre}
                </a>
              ))}
            </nav>
          </div>

          <div className="flex flex-col gap-3.5">
            <span className={OVERLINE}>LA SEÑAL, CADA MES</span>
            <Suscripcion variante="pie" />
          </div>
        </div>

        <EscalaDial alto={18} aguja={52} className="hidden lg:block" />
        <EscalaDial alto={14} aguja={52} paso={12} className="lg:hidden" />

        <div className={`flex flex-col gap-2 lg:flex-row lg:justify-between lg:gap-6 ${LEGAL}`}>
          <span>88.8 FM — SIEMPRE TRANSMITIENDO</span>
          <span className="hidden lg:inline">TRANSMISIÓN CULTURAL DESDE ABYA YALA</span>
          <span>{LIBERADA.archivo ? `EDICIÓN #${edicion.numero} · ` : ""}V1 LA NOCHE</span>
        </div>
        <LuzNativa className={`${LEGAL} self-start transition-colors duration-300 hover:text-(--noche-acento)`} />
      </div>
    </footer>
  );
}
