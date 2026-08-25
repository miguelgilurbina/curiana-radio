import Link from "next/link";
import type { Metadata } from "next";
import { getWikiPorSeccion, getCifrasWiki } from "@/lib/wiki";
import { getAllPersonajes } from "@/lib/personajes";
import Masthead from "@/components/simulador/Masthead";
import { Overline } from "@/components/simulador/ui";
import { DataAside } from "@/components/simulador/prose";

export const metadata: Metadata = {
  title: "Kaketiana — el mundo del kaketío | Curiana Radio",
  description:
    "Qué sabemos del pueblo caquetío del Golfete de Coro, siglos XIV-XV: cómo vivían, en qué creían, y cómo suena una lengua que nadie habla desde hace cuatrocientos años. Cada afirmación con su fuente.",
};

// ⚠️ ANDAMIO — esta portada existe para que la ruta funcione y la navegación
// cierre. El diseño real se hace aparte (ver el brief de secciones).
// Lo único que NO es provisional aquí son las cifras: se miden, no se
// escriben a mano (regla 1 del proyecto).
export default function KaketianaPage() {
  const cifras = getCifrasWiki();
  const pueblo = getWikiPorSeccion("pueblo");
  const lengua = getWikiPorSeccion("lengua");
  const personajes = getAllPersonajes();

  return (
    <div className="mx-auto max-w-6xl px-4 pb-24 pt-8 sm:px-6 lg:px-8">
      <Masthead />

      <article className="mx-auto max-w-[760px]">
        <header>
          <Overline>El mundo del kaketío</Overline>
          <h2 className="mt-2 sim-display text-4xl font-semibold leading-tight text-(--sim-ink) md:text-5xl">
            Un pueblo del Golfete de Coro, y la lengua que hablaba
          </h2>
          <p className="mt-5 max-w-reading font-sans text-lg leading-relaxed text-(--sim-ink-soft)">
            Los caquetíos vivieron en la costa de Falcón y las islas de enfrente
            hasta que la conquista los deshizo. No dejaron escritura. Lo que queda
            son crónicas de quienes los invadieron, topónimos que nadie tradujo,
            palabras sueltas en el papiamento de Aruba y Curazao, y lo que la
            arqueología saca de la arena.
          </p>
          <p className="mt-4 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            Esto es lo que se puede reconstruir con eso — y, con el mismo cuidado,
            lo que no.
          </p>
        </header>

        <DataAside
          items={[
            { label: "Artículos", value: cifras.articulos, sub: "sobre el pueblo y su lengua" },
            { label: "Obras", value: cifras.obras, sub: `${cifras.conLectura} se pueden leer en línea` },
            { label: "Voces simuladas", value: personajes.length, sub: "personajes con arco propio" },
          ]}
        />

        {/* La etimología del nombre, que es también la declaración de método */}
        <section className="mt-10 rounded-md border border-(--sim-rule) bg-(--sim-paper-deep) px-5 py-4">
          <p className="sim-display text-xl text-(--sim-fuego)">
            Kaketiana <span className="font-sans text-base italic text-(--sim-ink-soft)">— el lugar de la gente</span>
          </p>
          <p className="mt-2 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
            De <em>kaketio</em> &lsquo;ser viviente, gente&rsquo; (Oliver 1989, Tabla A-9) y{" "}
            <em>-ana</em> &lsquo;lugar de&rsquo; (atestiguado en <em>Paraguaná</em> y{" "}
            <em>Curiana</em>). <strong className="text-(--sim-ink)">La palabra no está documentada:</strong>{" "}
            la formamos con las piezas que sí lo están. Es la misma regla que gobierna
            todo lo demás de este sitio — lo atestiguado se distingue de lo reconstruido,
            siempre.
          </p>
        </section>

        {[
          { seccion: "pueblo" as const, titulo: "El pueblo", lista: pueblo,
            desc: "Cómo vivían, en qué creían, cómo se organizaban y hasta dónde llegaba su mundo." },
          { seccion: "lengua" as const, titulo: "La lengua", lista: lengua,
            desc: "Cómo es el caquetío reconstruido — y cómo se reconstruye una lengua sin hablantes." },
        ].map((s) => (
          <section key={s.seccion} className="mt-12">
            <div className="flex items-baseline justify-between gap-4">
              <h3 className="sim-display text-2xl font-semibold text-(--sim-ink)">{s.titulo}</h3>
              <Overline>{s.lista.length} artículos</Overline>
            </div>
            <p className="mt-1 max-w-reading font-sans text-sm text-(--sim-ink-faint)">{s.desc}</p>
            <ul className="mt-4">
              {s.lista.map((p) => (
                <li key={p.slug} className="border-t border-(--sim-rule) first:border-t-0">
                  <Link href={`/kaketiana/${s.seccion}/${p.slug}`} className="group block py-3.5">
                    <h4 className="sim-display text-lg font-semibold text-(--sim-ink) transition-colors group-hover:text-(--sim-fuego)">
                      {p.titulo}
                    </h4>
                    <p className="mt-0.5 line-clamp-2 max-w-reading font-sans text-sm leading-relaxed text-(--sim-ink-soft)">
                      {p.resumen}
                    </p>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ))}

        <section className="mt-12 border-t border-(--sim-ink) pt-6">
          <h3 className="sim-display text-2xl font-semibold text-(--sim-ink)">Y un experimento</h3>
          <p className="mt-2 max-w-reading font-sans text-[0.95rem] leading-relaxed text-(--sim-ink-soft)">
            Con todo lo anterior se construyó una simulación: {personajes.length} personajes
            hablan el caquetío reconstruido, inventan palabras y se contagian entre sí. No
            prueba cómo hablaban los caquetíos — prueba qué le pasa a una lengua cuando la
            gente la usa.
          </p>
          <div className="mt-4 flex flex-wrap gap-x-6 gap-y-2 font-sans text-sm">
            {[
              { href: "/kaketiana/experimento", label: "El experimento →" },
              { href: "/kaketiana/personajes", label: "Los personajes" },
              { href: "/kaketiana/lexicon", label: "El diccionario" },
              { href: "/kaketiana/neologisms", label: "Los neologismos" },
              { href: "/kaketiana/bibliografia", label: "La bibliografía" },
            ].map((l) => (
              <Link key={l.href} href={l.href} className="font-medium text-(--sim-fuego) transition-colors hover:text-(--sim-rubrica)">
                {l.label}
              </Link>
            ))}
          </div>
        </section>
      </article>
    </div>
  );
}
