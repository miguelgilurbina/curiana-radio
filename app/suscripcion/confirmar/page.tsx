import Link from "next/link";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Cartel } from "@/components/ui/Typography";
import Suscripcion from "@/components/landing/Suscripcion";
import SuscripcionConfirmada from "@/components/landing/SuscripcionConfirmada";
import { radio } from "@/components/senales/pieles/radio";
import { configuracion } from "@/lib/newsletter/config";
import { darDeAlta } from "@/lib/newsletter/resend";
import { normalizarEmail, TEMA } from "@/lib/newsletter/suscriptor";
import { verificar } from "@/lib/newsletter/token";
import { LIBERADA, type Seccion } from "@/lib/secciones";
import { metadatos } from "@/lib/seo";

// ── /suscripcion/confirmar?t=… : el segundo paso del doble opt-in ─────
// El enlace del correo de confirmación llega aquí. Si el token es válido y no
// venció, el contacto queda en Resend con el tema elegido; si no, se ofrece
// pedir otro enlace. Si Resend falla, el enlace sigue sirviendo y se ofrece
// reintentar. Sin token (llegó a mano o recargó tras confirmar: la página lo
// borra de la barra), se explica y se ofrece el formulario. Dinámica (cada
// visita confirma) y fuera de los buscadores: noindex y fuera del sitemap.
//
// Responde 200 también cuando el enlace caducó: es una página útil (trae el
// formulario para pedir otro) y el App Router no deja elegir otro código sin
// pasar por notFound(); el noindex la saca del índice igual.
//
// Va en la piel de la radio, como «Quién transmite» (/sobre).

export const dynamic = "force-dynamic";

export const metadata: Metadata = metadatos({
  titulo: "Confirma tu frecuencia — Curiana Radio",
  descripcion: "La confirmación de la suscripción al correo de Curiana Radio.",
  ruta: "/suscripcion/confirmar",
  noIndex: true,
});

const DATO = "font-mono text-[0.68rem] uppercase tracking-[0.24em] text-(--noche-hueso-2)";
const P = "m-0 text-body text-(--noche-hueso)";
const ENLACE =
  "text-(--noche-hueso) underline decoration-(--noche-filete-fuerte) underline-offset-4 transition-colors duration-300 hover:text-(--noche-frecuencia-tinta) hover:decoration-(--noche-frecuencia-tinta)";
const ACCION = `${DATO} transition-colors duration-300 hover:text-(--noche-frecuencia-tinta)`;

const ESTACIONES: { nombre: string; href: string; texto: string; seccion?: Seccion }[] = [
  { nombre: "Señales", href: "/senales", texto: "lo que escribe su creador." },
  {
    seccion: "kaketiana",
    nombre: "Kaketiana",
    href: "/kaketiana",
    texto: "el mundo y la lengua de los caquetíos, con cada fuente a la vista.",
  },
  { seccion: "jai-sounds", nombre: "JAI Sounds", href: "/jai-sounds", texto: "la curaduría musical." },
];

function Marco({ dato, titulo, children }: { dato: string; titulo: string; children: ReactNode }) {
  return (
    <div {...radio.atributos} data-piel={radio.id} className="min-h-screen px-6 pt-12 pb-28 animate-fade-in sm:pt-16">
      <div className="mx-auto flex max-w-[65ch] flex-col gap-12">
        <header className="flex flex-col gap-5">
          <span className={DATO}>{dato}</span>
          <Cartel as="h1" className="text-[clamp(2.4rem,6vw,3.6rem)] leading-none">
            {titulo}
          </Cartel>
        </header>
        {children}
      </div>
    </div>
  );
}

function Confirmada({ recibe }: { recibe: string }) {
  return (
    <Marco dato="88.8 · Señal confirmada" titulo="Quedaste en la frecuencia">
      <section className="flex flex-col gap-6">
        <p className="m-0 font-serif text-xl leading-relaxed italic text-(--noche-hueso-2)">
          Desde ahora te llega {recibe}.
        </p>
        <p className={P}>
          Al pie de cada correo puedes cambiar de frecuencia o dejar de recibirla, cuando quieras.
        </p>
      </section>
      <section aria-labelledby="mientras" className="flex flex-col gap-5 border-t border-(--noche-filete) pt-10">
        <h2 id="mientras" className={`m-0 ${DATO}`}>
          Mientras tanto, la señal sigue en
        </h2>
        <ul className="m-0 flex list-none flex-col gap-3 p-0">
          {ESTACIONES.filter((e) => !e.seccion || LIBERADA[e.seccion]).map((e) => (
            <li key={e.href} className="border-l-2 border-(--noche-filete) pl-4 text-body text-(--noche-hueso)">
              <Link href={e.href} className={`font-semibold ${ENLACE}`}>
                {e.nombre}
              </Link>
              : {e.texto}
            </li>
          ))}
        </ul>
        <Link href="/inicio" className={`${ACCION} mt-4 self-start`}>
          ← Volver a la radio
        </Link>
      </section>
    </Marco>
  );
}

function PedirOtro({ dato, titulo, children }: { dato: string; titulo: string; children: ReactNode }) {
  return (
    <Marco dato={dato} titulo={titulo}>
      <p className={P}>{children}</p>
      <div className="flex flex-col gap-5 rounded-2xl border border-(--noche-filete) bg-(--noche-panel) p-6 sm:p-10">
        <Suscripcion />
      </div>
    </Marco>
  );
}

function Caducada() {
  return (
    <PedirOtro dato="88.8 · Sin señal" titulo="Esta señal caducó">
      El enlace para confirmar vale 48 horas, y éste ya no sirve (o llegó cortado). Pide otro: te lo mandamos de nuevo.
    </PedirOtro>
  );
}

/** Sin enlace: alguien llegó a mano, o recargó después de confirmar (la
 *  página borra el token de la barra). Ni «caducó» ni «confirmada». */
function SinEnlace() {
  return (
    <PedirOtro dato="88.8 · En espera" titulo="Confirma tu frecuencia">
      Para quedar en la frecuencia, abre el enlace que te mandamos por correo. Si ya lo abriste, no hace falta más.
      ¿No te llegó? Pide otro:
    </PedirOtro>
  );
}

function Cortada({ reintento }: { reintento: string }) {
  return (
    <Marco dato="88.8 · Interferencia" titulo="La señal se cortó">
      <p className={P}>
        No pudimos guardar tu suscripción. No es tu enlace: sigue sirviendo. Prueba otra vez en un momento.
      </p>
      <a href={reintento} className={`${ACCION} self-start`}>
        [ Reintentar → ]
      </a>
    </Marco>
  );
}

export default async function ConfirmarSuscripcion({
  searchParams,
}: {
  searchParams: Promise<{ t?: string | string[] }>;
}) {
  const { t } = await searchParams;
  if (t === undefined) return <SinEnlace />;
  const conf = configuracion();
  const alta = conf && typeof t === "string" ? verificar(t, conf.secreto) : null;
  // el correo del token ya pasó por la validación al firmarse; se vuelve a
  // mirar por si el secreto se filtró y alguien firmó otra cosa
  if (!conf || !alta || normalizarEmail(alta.email) !== alta.email) return <Caducada />;

  let guardada = false;
  try {
    guardada = await darDeAlta(conf, alta.email, alta.tema);
  } catch (error) {
    console.error("newsletter: falló el alta del contacto", error instanceof Error ? error.message : error);
  }
  if (!guardada) return <Cortada reintento={`/suscripcion/confirmar?t=${encodeURIComponent(t as string)}`} />;

  return (
    <>
      <Confirmada recibe={TEMA[alta.tema].recibe} />
      <SuscripcionConfirmada tema={alta.tema} />
    </>
  );
}
