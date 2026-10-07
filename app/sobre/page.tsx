import Link from "next/link";
import type { Metadata } from "next";
import { Cartel } from "@/components/ui/Typography";
import Redes from "@/components/senales/Redes";
import InterruptorLuz from "@/components/senales/InterruptorLuz";
import { radio } from "@/components/senales/pieles/radio";
import { PORTAFOLIO } from "@/lib/redes";
import { LIBERADA, type Seccion } from "@/lib/secciones";
import { metadatos, tarjeta } from "@/lib/seo";

export const metadata: Metadata = metadatos({
  titulo: "Quién transmite — Curiana Radio",
  descripcion:
    "Curiana Radio es el laboratorio creativo de Miguel Gil Urbina: una radio del futuro que se sintoniza desde acá, con memoria donde casi nunca la hay.",
  ruta: "/sobre",
  imagen: tarjeta("sobre", "Quién transmite: Curiana Radio y su creador"),
});

// «Quién transmite»: lo que hay detrás de la ficción. La radio transmite
// desde después; aquí se dice quién la hace y desde dónde. Va en la piel de
// la radio (la noche, con su modo claro): lee sus tokens y sigue la luz. El copy sale de las palabras de
// Miguel (2026-10-02) y de su portafolio; es un borrador para que lo cambie.

const DATO = "font-mono text-[0.68rem] uppercase tracking-[0.24em] text-(--noche-hueso-2)";
const ACCION = `${DATO} transition-colors duration-300 hover:text-(--noche-frecuencia-tinta)`;
const P = "m-0 text-body text-(--noche-hueso)";
const ENLACE =
  "text-(--noche-hueso) underline decoration-(--noche-filete-fuerte) underline-offset-4 transition-colors duration-300 hover:text-(--noche-frecuencia-tinta) hover:decoration-(--noche-frecuencia-tinta)";

const ARISTAS: { nombre: string; href: string | null; texto: string; seccion?: Seccion }[] = [
  {
    seccion: "kaketiana",
    nombre: "Kaketiana",
    href: "/kaketiana",
    texto: "reconstruye el mundo y la lengua de los caquetíos del Golfete de Coro, con cada fuente a la vista.",
  },
  { seccion: "jai-sounds", nombre: "JAI Sounds", href: "/jai-sounds", texto: "es la curaduría musical, sin límites de género." },
  { seccion: "galeria", nombre: "La Galería", href: "/galeria", texto: "reúne las imágenes que van quedando en el camino." },
  { seccion: "buchibe", nombre: "Cuentos de Buchibe", href: null, texto: "está por correr el telón." },
  { nombre: "Señales", href: "/senales", texto: "es donde escribo yo." },
];

export default function Sobre() {
  return (
    <div {...radio.atributos} data-piel={radio.id} className="min-h-screen px-6 pt-12 pb-28 animate-fade-in sm:pt-16">
      <div className="mx-auto flex max-w-[65ch] flex-col gap-16">
        <header className="flex flex-col gap-5">
          <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-3">
            <span className={DATO}>88.8 · Fuera del aire</span>
            <InterruptorLuz
              nativo={radio.nativo}
              alterno={radio.alterno}
              activo="text-(--noche-hueso)"
              className={DATO}
            />
          </div>
          <Cartel as="h1" className="text-[clamp(2.4rem,6vw,3.6rem)] leading-none">
            Quién transmite
          </Cartel>
          <p className="m-0 font-serif text-xl leading-relaxed italic text-(--noche-hueso-2)">
            La radio transmite desde después. Detrás de la señal hay una persona, escribiendo desde acá.
          </p>
        </header>

        <section aria-labelledby="la-radio" className="flex flex-col gap-6">
          <h2 id="la-radio" className="m-0 font-serif text-[1.75rem] font-semibold text-(--noche-hueso)">
            Curiana Radio
          </h2>
          <p className={P}>
            Curiana Radio es un laboratorio creativo con una mitología propia: una radio que transmite desde el futuro
            y que, por esas cosas misteriosas de la transmisión radial, se alcanza a sintonizar desde acá. Trae otra
            perspectiva: hay recuerdo, hay memoria, donde casi nunca la hay.
          </p>
          <p className={P}>La señal tiene varias frecuencias:</p>
          <ul className="m-0 flex list-none flex-col gap-3 p-0">
            {ARISTAS.filter((a) => !a.seccion || LIBERADA[a.seccion]).map((a) => (
              <li key={a.nombre} className="border-l-2 border-(--noche-filete) pl-4 text-body text-(--noche-hueso)">
                {a.href ? (
                  <Link href={a.href} className={`font-semibold ${ENLACE}`}>
                    {a.nombre}
                  </Link>
                ) : (
                  <span className="font-semibold">{a.nombre}</span>
                )}{" "}
                {a.texto}
              </li>
            ))}
          </ul>
        </section>

        <section aria-labelledby="quien" className="flex flex-col gap-6">
          <h2 id="quien" className="m-0 font-serif text-[1.75rem] font-semibold text-(--noche-hueso)">
            Miguel Gil Urbina
          </h2>
          <p className={P}>
            Soy Miguel Gil Urbina, el creador de Curiana Radio. En el fondo, la radio es mi espacio para expresarme
            creativamente: lo que escribo en la libreta, lo que escucho, lo que imagino.
          </p>
          <p className={P}>
            Fuera del aire construyo software: soy desarrollador full stack, con foco en sistemas con inteligencia
            artificial, y trabajo desde Santiago de Chile. Curiana Radio también es eso: un lugar donde la tecnología y
            la memoria se cruzan.
          </p>
          <a
            href={PORTAFOLIO.url}
            target="_blank"
            rel="noopener noreferrer"
            className="group flex flex-col gap-2 self-start py-1 pl-5 [border-left:4px_solid_var(--e-riel)]"
          >
            <span className={DATO}>Mi trabajo como desarrollador</span>
            <span className="font-serif text-2xl font-semibold text-(--noche-hueso) transition-colors duration-300 group-hover:text-(--noche-frecuencia-tinta)">
              {PORTAFOLIO.texto} ↗
            </span>
          </a>
        </section>

        <footer className="flex flex-col gap-4 border-t border-(--noche-filete) pt-10">
          <span className={DATO}>La señal sigue en</span>
          <Redes />
          <Link href="/inicio" className={`${ACCION} mt-4 self-start`}>
            ← Volver a la radio
          </Link>
        </footer>
      </div>
    </div>
  );
}
