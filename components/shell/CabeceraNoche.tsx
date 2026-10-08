"use client";

import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Sello from "./Sello";
import { ESTACIONES, estacionActiva } from "./estaciones";
import { LIBERADA } from "@/lib/secciones";

// La cabecera de la noche: shell 1a «El dial» (design_handoff_senales_luces/
// shell/SHELL.md). La nav es una escala de sintonía y una aguja de acento
// marca dónde estás; al navegar, la aguja se desliza. Fondo sólido, sin vidrio.
// Se esconde al bajar y vuelve al subir. En móvil, el sello, el 88.8 y
// [ DIAL ], que abre el menú a pantalla completa.

const MONO = "font-mono";
const ESCALA =
  "repeating-linear-gradient(90deg, var(--noche-filete-fuerte) 0 1px, transparent 1px 14px)";
const ESCALA_VERTICAL =
  "repeating-linear-gradient(180deg, var(--noche-filete-fuerte) 0 1px, transparent 1px 12px)";

function AlAire({
  texto = "AL AIRE",
  className = "",
}: {
  texto?: string;
  className?: string;
}) {
  return (
    <span
      className={`flex items-center gap-2 ${MONO} text-[0.625rem] tracking-[0.24em] ${className}`}
    >
      <span
        aria-hidden="true"
        className="noche-pulso inline-block h-[7px] w-[7px] rounded-full bg-(--noche-acento)"
      />
      {texto}
    </span>
  );
}

function Badge() {
  return (
    <span
      className={`rounded-[2px] bg-(--noche-acento) px-2.5 py-[5px] ${MONO} text-[0.6875rem] font-bold tracking-[0.14em] whitespace-nowrap text-(--noche-fondo)`}
    >
      88.8 FM
    </span>
  );
}

export default function CabeceraNoche({
  edicion,
  aristaDeSenal,
  haySenales,
}: {
  edicion: { numero: string; slug: string };
  aristaDeSenal: Record<string, string | null>;
  /** sin señales que mostrar, SEÑALES no sale en el dial (lib/senales.ts) */
  haySenales: boolean;
}) {
  const ruta = usePathname();
  const activa = estacionActiva(ruta, aristaDeSenal);
  const estaciones = haySenales ? ESTACIONES : ESTACIONES.filter((e) => e.id !== "senales");

  // se esconde al bajar, vuelve al subir (como la nav del resto del sitio)
  const [visible, setVisible] = useState(true);
  const ultimoY = useRef(0);
  useEffect(() => {
    const alDesplazar = () => {
      const y = window.scrollY;
      setVisible(y < 10 || y < ultimoY.current || y <= 100);
      ultimoY.current = y;
    };
    window.addEventListener("scroll", alDesplazar, { passive: true });
    return () => window.removeEventListener("scroll", alDesplazar);
  }, []);

  // la aguja: se mide sobre la estación activa y se desliza a la nueva
  const nav = useRef<HTMLElement>(null);
  const [aguja, setAguja] = useState<{
    x: number;
    y: number;
    animar: boolean;
  } | null>(null);
  const medir = useCallback(
    (animar: boolean) => {
      const item = nav.current?.querySelector<HTMLElement>(
        `[data-estacion="${activa}"]`,
      );
      setAguja(
        item
          ? {
              x: item.offsetLeft + item.offsetWidth / 2,
              y: item.offsetTop - 14,
              animar,
            }
          : null,
      );
    },
    [activa],
  );
  useLayoutEffect(() => {
    // medir el DOM: la aguja no existe en el servidor
    medir(aguja !== null);
    const alCambiar = () => medir(false);
    window.addEventListener("resize", alCambiar);
    return () => window.removeEventListener("resize", alCambiar);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- sólo al cambiar de estación
  }, [medir]);

  // el menú del móvil
  const [abierto, setAbierto] = useState(false);
  const boton = useRef<HTMLButtonElement>(null);
  const cerrar = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    // al navegar, el menú se cierra
    setAbierto(false);
  }, [ruta]);
  useEffect(() => {
    if (!abierto) return;
    document.body.style.overflow = "hidden";
    cerrar.current?.focus();
    const alTeclear = (e: KeyboardEvent) => {
      if (e.key === "Escape") setAbierto(false);
    };
    window.addEventListener("keydown", alTeclear);
    const elBoton = boton.current;
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", alTeclear);
      elBoton?.focus();
    };
  }, [abierto]);

  const enlace = (activo: boolean) =>
    `${MONO} py-2.5 text-[0.6875rem] tracking-[0.24em] uppercase whitespace-nowrap transition-colors duration-300 ${
      activo
        ? "text-(--shell-hueso)"
        : "text-(--noche-hueso-2) hover:text-(--noche-acento)"
    }`;

  return (
    <>
      <header
        className={`shell-noche sticky top-0 z-50 border-b border-(--noche-filete) bg-(--noche-fondo) transition-transform duration-300 ${
          visible || abierto ? "translate-y-0" : "-translate-y-full"
        }`}
      >
        {/* Escritorio: sello · el dial · al aire */}
        <div className="hidden h-[92px] items-center gap-10 px-10 lg:flex">
          <Link href="/inicio" aria-label="Curiana Radio, a la portada">
            <Sello tamano={56} />
          </Link>
          <nav
            ref={nav}
            aria-label="Estaciones"
            className="relative flex flex-1 items-center justify-between self-stretch px-2"
            style={{
              background: `${ESCALA} left bottom 24px / 100% 7px no-repeat`,
            }}
          >
            {estaciones.map((e) =>
              e.href ? (
                <Link
                  key={e.id}
                  href={e.href}
                  data-estacion={e.id}
                  aria-current={activa === e.id ? "page" : undefined}
                  className={enlace(activa === e.id)}
                >
                  {e.nombre}
                </Link>
              ) : (
                <span
                  key={e.id}
                  data-estacion={e.id}
                  title="Pronto"
                  className={`${MONO} py-2.5 text-[0.6875rem] tracking-[0.24em] uppercase whitespace-nowrap text-(--noche-dato)`}
                >
                  {e.nombre}
                  <span className="sr-only"> (pronto)</span>
                </span>
              ),
            )}
            {aguja && (
              <span
                aria-hidden="true"
                className={`pointer-events-none absolute h-[46px] w-[2px] -translate-x-1/2 bg-(--noche-acento) ${
                  aguja.animar
                    ? "transition-[left] duration-300 ease-out motion-reduce:transition-none"
                    : ""
                }`}
                style={{ left: aguja.x, top: aguja.y }}
              />
            )}
          </nav>
          <div className="flex items-center gap-[18px]">
            <AlAire className="text-(--noche-hueso-2)" />
            <Badge />
          </div>
        </div>

        {/* Móvil: sello · 88.8 · [ DIAL ] */}
        <div className="flex h-[72px] items-center justify-between px-4 lg:hidden">
          <Link href="/inicio" aria-label="Curiana Radio, a la portada">
            <Sello tamano={48} />
          </Link>
          <div className="flex items-center gap-1.5">
            <Badge />
            <button
              ref={boton}
              type="button"
              aria-expanded={abierto}
              aria-controls="menu-noche"
              onClick={() => setAbierto(true)}
              className={`flex min-h-11 cursor-pointer items-center px-2.5 ${MONO} text-[0.6875rem] tracking-[0.2em] text-(--noche-hueso)`}
            >
              [ DIAL ]
            </button>
          </div>
        </div>
      </header>

      {/* El menú va fuera de la cabecera: su translate (esconderse al bajar)
        haría de bloque contenedor para un hijo fixed. */}
      {abierto && (
        <div
          id="menu-noche"
          role="dialog"
          aria-modal="true"
          aria-label="Estaciones de Curiana Radio"
          className="shell-noche fixed inset-0 z-[60] flex flex-col bg-(--noche-fondo) px-4 pb-7 lg:hidden"
        >
          <div className="flex h-[72px] shrink-0 items-center justify-between border-b border-(--noche-filete)">
            <Sello tamano={48} />
            <button
              ref={cerrar}
              type="button"
              onClick={() => setAbierto(false)}
              className={`flex min-h-11 cursor-pointer items-center px-2.5 ${MONO} text-[0.6875rem] tracking-[0.2em] text-(--noche-acento)`}
            >
              [ CERRAR × ]
            </button>
          </div>
          <nav
            aria-label="Estaciones"
            className="flex flex-1 flex-col justify-center gap-1 overflow-y-auto pl-7"
            style={{
              background: `${ESCALA_VERTICAL} 0 0 / 8px 100% no-repeat`,
            }}
          >
            {estaciones.map((e) => {
              const activo = activa === e.id;
              const clase = `relative font-(family-name:--font-archivo-black) text-[2rem] leading-[1.5] ${
                e.href
                  ? activo
                    ? "text-(--shell-hueso)"
                    : "text-(--noche-hueso-2)"
                  : "text-(--noche-dato)"
              }`;
              const contenido = (
                <>
                  {activo && (
                    <span
                      aria-hidden="true"
                      className="absolute top-1/2 -left-8 h-[2px] w-[22px] bg-(--noche-acento)"
                    />
                  )}
                  {e.nombre}
                </>
              );
              return e.href ? (
                <Link
                  key={e.id}
                  href={e.href}
                  aria-current={activo ? "page" : undefined}
                  className={clase}
                >
                  {contenido}
                </Link>
              ) : (
                <span key={e.id} className={clase}>
                  {contenido}
                  <span className="sr-only"> (pronto)</span>
                </span>
              );
            })}
          </nav>
          <div className="flex shrink-0 flex-col gap-3.5">
            <Link
              href={LIBERADA.archivo ? `/${edicion.slug}` : "/inicio"}
              className={`flex min-h-[52px] items-center justify-center bg-(--noche-acento) ${MONO} text-xs font-bold tracking-[0.24em] text-(--noche-fondo)`}
            >
              SINTONIZAR AHORA →
            </Link>
            <AlAire
              texto="AL AIRE · 88.8 FM"
              className="justify-center text-(--noche-dato)"
            />
          </div>
        </div>
      )}
    </>
  );
}
